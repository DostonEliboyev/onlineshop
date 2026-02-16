"""Download dark/rich furniture banner images that work well as hero backgrounds."""
import os, django, requests, time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture_shop.settings')
django.setup()
from django.core.files.base import ContentFile
from core.models import Banner
from PIL import Image
from io import BytesIO

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Dark, rich interior images that work as hero banner backgrounds
URLS = [
    # Dark modern living room
    'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=1920&q=90',
    # Moody dark bedroom
    'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=1920&q=90',
    # Dark luxury dining
    'https://images.unsplash.com/photo-1600210491369-e753d80a41f3?w=1920&q=90',
]

FALLBACK_URLS = [
    'https://images.unsplash.com/photo-1631679706909-1844bbd07221?w=1920&q=90',
    'https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=1920&q=90',
    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1920&q=90',
]

def download(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
        if resp.status_code == 200 and len(resp.content) > 10000:
            return resp.content
    except:
        pass
    return None

def check_brightness(img_data):
    """Check if image is dark enough for a banner."""
    img = Image.open(BytesIO(img_data))
    img = img.resize((100, 100))
    pixels = list(img.getdata())
    avg_brightness = sum(sum(p[:3]) / 3 for p in pixels) / len(pixels)
    return avg_brightness

banners = list(Banner.objects.all())
for idx, banner in enumerate(banners):
    print(f"\n[{banner.title}]")
    
    # Try primary URL first, then fallback
    all_urls = []
    if idx < len(URLS):
        all_urls.append(URLS[idx])
    if idx < len(FALLBACK_URLS):
        all_urls.append(FALLBACK_URLS[idx])
    
    for url in all_urls:
        print(f"  Trying: {url[:60]}...", end=" ")
        data = download(url)
        if data:
            brightness = check_brightness(data)
            print(f"OK ({len(data)//1024}KB, brightness={brightness:.0f})")
            
            # Save with a new timestamp to bust cache
            import hashlib
            h = hashlib.md5(data).hexdigest()[:8]
            fname = f"banner_hero_{idx+1}_{h}.jpg"
            banner.image.save(fname, ContentFile(data), save=True)
            print(f"  Saved as: {fname}")
            break
        else:
            print("FAILED, trying next...")
        time.sleep(0.5)

# Verify
print("\n--- Final check ---")
for b in Banner.objects.all():
    if b.image:
        img = Image.open(b.image.path)
        print(f"{b.title}: {img.size[0]}x{img.size[1]}, file={b.image.name}")
