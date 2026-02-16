import os, django, requests, time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture_shop.settings')
django.setup()
from django.core.files.base import ContentFile
from core.models import Banner

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Vivid, high-contrast furniture interior images
BANNER_URLS = [
    'https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1920&q=85',
    'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=1920&q=85',
    'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=1920&q=85',
]

banners = list(Banner.objects.all())
for idx, banner in enumerate(banners):
    if idx >= len(BANNER_URLS):
        break
    url = BANNER_URLS[idx]
    print(f"Downloading banner {idx+1}: {banner.title}...", end=" ")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
        if resp.status_code == 200 and len(resp.content) > 5000:
            banner.image.save(f"banner_vivid_{idx+1}.jpg", ContentFile(resp.content), save=True)
            print(f"OK ({len(resp.content)//1024} KB)")
        else:
            print(f"FAILED status={resp.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")
    time.sleep(0.5)

print("\nDone! Banner images replaced with vivid photos.")
