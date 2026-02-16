"""Download 3 rich, dark-toned furniture photos and set them as banners."""
import os, django, requests, time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture_shop.settings')
django.setup()

from PIL import Image, ImageEnhance, ImageDraw
from django.core.files.base import ContentFile
from core.models import Banner
from io import BytesIO

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Pexels free images - direct photo URLs (dark interiors, clearly furniture)
URLS = [
    # Dark elegant living room with sofa
    "https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg?auto=compress&cs=tinysrgb&w=1920",
    # Cozy dark bedroom
    "https://images.pexels.com/photos/1648776/pexels-photo-1648776.jpeg?auto=compress&cs=tinysrgb&w=1920",
    # Modern dining room
    "https://images.pexels.com/photos/1457842/pexels-photo-1457842.jpeg?auto=compress&cs=tinysrgb&w=1920",
]

BACKUP_URLS = [
    "https://images.pexels.com/photos/276583/pexels-photo-276583.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/1643383/pexels-photo-1643383.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/2079249/pexels-photo-2079249.jpeg?auto=compress&cs=tinysrgb&w=1920",
]

def download(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 20000:
            img = Image.open(BytesIO(r.content))
            if img.size[0] >= 800:
                return r.content, img.size
        print(f"    Bad response: status={r.status_code}, size={len(r.content)}")
    except Exception as e:
        print(f"    Error: {e}")
    return None, None

def make_banner(raw_data, idx):
    """Crop to 1920x600, boost colors, add subtle left gradient."""
    img = Image.open(BytesIO(raw_data)).convert('RGB')
    W, H = 1920, 600
    
    # Scale up to cover 1920x600
    w, h = img.size
    scale = max(W / w, H / h)
    img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    
    # Center crop
    w, h = img.size
    left = (w - W) // 2
    top = (h - H) // 2
    img = img.crop((left, top, left + W, top + H))
    
    # Boost saturation and contrast
    img = ImageEnhance.Color(img).enhance(1.2)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    
    # Darken slightly for text readability
    img = ImageEnhance.Brightness(img).enhance(0.85)
    
    # Add left gradient for text area
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(W):
        if x < W * 0.5:
            alpha = int(160 * (1 - x / (W * 0.5)))
        else:
            alpha = 0
        draw.line([(x, 0), (x, H)], fill=(0, 0, 0, alpha))
    
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    buf = BytesIO()
    img.save(buf, format='JPEG', quality=93)
    return buf.getvalue()


# Clean old banners
banner_dir = r'e:\lession\media\banners'
if os.path.exists(banner_dir):
    for f in os.listdir(banner_dir):
        os.remove(os.path.join(banner_dir, f))
    print("Cleaned old banner files.\n")

banners = list(Banner.objects.all().order_by('order'))

for idx in range(3):
    banner = banners[idx] if idx < len(banners) else None
    if not banner:
        break
    
    print(f"Banner {idx+1}: {banner.title}")
    
    # Try primary URL, then backup
    raw = None
    for url in [URLS[idx], BACKUP_URLS[idx]]:
        print(f"  Downloading from: {url[:70]}...")
        raw, size = download(url)
        if raw:
            print(f"  Downloaded: {size[0]}x{size[1]}, {len(raw)//1024}KB")
            break
        time.sleep(1)
    
    if not raw:
        print(f"  FAILED - skipping")
        continue
    
    # Create banner
    banner_data = make_banner(raw, idx)
    result = Image.open(BytesIO(banner_data))
    
    # Verify it's colorful (not grey)
    pixels = list(result.resize((50, 50)).getdata())
    avg_r = sum(p[0] for p in pixels) / len(pixels)
    avg_g = sum(p[1] for p in pixels) / len(pixels)
    avg_b = sum(p[2] for p in pixels) / len(pixels)
    print(f"  Final: {result.size[0]}x{result.size[1]}, avg_color=({avg_r:.0f},{avg_g:.0f},{avg_b:.0f})")
    
    # Save
    fname = f"banner_{idx+1}.jpg"
    banner.image.save(fname, ContentFile(banner_data), save=True)
    print(f"  Saved: {banner.image.name}\n")

print("All banners done!")
