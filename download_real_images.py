"""
Download real furniture images from Unsplash for all products, banners, and categories.
"""
import os
import django
import requests
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture_shop.settings')
django.setup()

from django.core.files.base import ContentFile
from products.models import Product, ProductImage, Category
from core.models import Banner

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def download_image(url, retries=3):
    """Download image from URL with retries."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
            if resp.status_code == 200 and len(resp.content) > 1000:
                return resp.content
            print(f"    Attempt {attempt+1} failed: status={resp.status_code}, size={len(resp.content)}")
        except Exception as e:
            print(f"    Attempt {attempt+1} error: {e}")
        time.sleep(1)
    return None


# Real furniture image URLs from Unsplash (free to use)
PRODUCT_IMAGES = {
    'modern-velvet-sofa': [
        'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80',
        'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=800&q=80',
        'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=800&q=80',
        'https://images.unsplash.com/photo-1567016432779-094069958ea5?w=800&q=80',
    ],
    'scandinavian-oak-coffee-table': [
        'https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?w=800&q=80',
        'https://images.unsplash.com/photo-1611967164521-abae8fba4668?w=800&q=80',
        'https://images.unsplash.com/photo-1532372576444-dda954194ad0?w=800&q=80',
    ],
    'leather-executive-office-chair': [
        'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=800&q=80',
        'https://images.unsplash.com/photo-1589364025530-3047cfa3a883?w=800&q=80',
        'https://images.unsplash.com/photo-1541558869434-2840d308329a?w=800&q=80',
    ],
    'walnut-king-size-bed-frame': [
        'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&q=80',
        'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&q=80',
        'https://images.unsplash.com/photo-1588046130717-0eb0c9a3ba15?w=800&q=80',
        'https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80',
    ],
    'marble-top-dining-table': [
        'https://images.unsplash.com/photo-1617806118233-18e1de247200?w=800&q=80',
        'https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800&q=80',
        'https://images.unsplash.com/photo-1604578762246-41134e37f9cc?w=800&q=80',
    ],
    'rattan-garden-lounge-set': [
        'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800&q=80',
        'https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=800&q=80',
        'https://images.unsplash.com/photo-1595659379706-6be068143afc?w=800&q=80',
    ],
    'industrial-metal-bookshelf': [
        'https://images.unsplash.com/photo-1594620302200-9a762244a156?w=800&q=80',
        'https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800&q=80',
        'https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=800&q=80',
    ],
    'velvet-dining-chair-set': [
        'https://images.unsplash.com/photo-1551298370-9d3d53740c72?w=800&q=80',
        'https://images.unsplash.com/photo-1503602642458-232111445657?w=800&q=80',
        'https://images.unsplash.com/photo-1549497538-303791108f95?w=800&q=80',
    ],
    'minimalist-tv-stand': [
        'https://images.unsplash.com/photo-1615874959474-d609969a20ed?w=800&q=80',
        'https://images.unsplash.com/photo-1611269154421-4e27233ac5c7?w=800&q=80',
        'https://images.unsplash.com/photo-1593696140826-c58b021acf8b?w=800&q=80',
    ],
    'oak-nightstand-drawer': [
        'https://images.unsplash.com/photo-1532323544230-7191fd51bc1b?w=800&q=80',
        'https://images.unsplash.com/photo-1543248939-4296e1a4d044?w=800&q=80',
        'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=800&q=80',
    ],
    'standing-desk-adjustable': [
        'https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=800&q=80',
        'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=800&q=80',
        'https://images.unsplash.com/photo-1611269154421-4e27233ac5c7?w=800&q=80',
    ],
    'glass-console-table': [
        'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80',
        'https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?w=800&q=80',
        'https://images.unsplash.com/photo-1618220179428-22790b461013?w=800&q=80',
    ],
}

BANNER_IMAGES = [
    'https://images.unsplash.com/photo-1618219908412-a29a1bb7b86e?w=1920&q=80',
    'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=1920&q=80',
    'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=1920&q=80',
]

CATEGORY_IMAGES = {
    'living-room': 'https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=800&q=80',
    'bedroom': 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&q=80',
    'dining': 'https://images.unsplash.com/photo-1617806118233-18e1de247200?w=800&q=80',
    'office': 'https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=800&q=80',
    'outdoor': 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800&q=80',
    'storage': 'https://images.unsplash.com/photo-1594620302200-9a762244a156?w=800&q=80',
}


# --- PRODUCTS ---
print("=" * 50)
print("Downloading REAL product images...")
print("=" * 50)

for product in Product.objects.all():
    slug = product.slug
    urls = PRODUCT_IMAGES.get(slug, [])

    if not urls:
        print(f"\n[SKIP] No URLs for: {product.name}")
        continue

    # Delete old placeholder images
    old_count = product.images.count()
    if old_count > 0:
        product.images.all().delete()
        print(f"\n[{product.name}] Removed {old_count} old placeholder images")
    else:
        print(f"\n[{product.name}]")

    for i, url in enumerate(urls):
        print(f"  Downloading image {i+1}/{len(urls)}...", end=" ")
        img_data = download_image(url)
        if img_data:
            pi = ProductImage(
                product=product,
                is_primary=(i == 0),
                order=i
            )
            ext = 'jpg'
            filename = f"{slug}_real_{i+1}.{ext}"
            pi.image.save(filename, ContentFile(img_data), save=True)
            print(f"OK ({len(img_data)//1024} KB)")
        else:
            print("FAILED")
        time.sleep(0.3)


# --- BANNERS ---
print("\n" + "=" * 50)
print("Downloading REAL banner images...")
print("=" * 50)

for idx, banner in enumerate(Banner.objects.all()):
    if idx < len(BANNER_IMAGES):
        url = BANNER_IMAGES[idx]
        print(f"\n[Banner: {banner.title}]")
        print(f"  Downloading...", end=" ")
        img_data = download_image(url)
        if img_data:
            banner.image.save(f"banner_real_{idx+1}.jpg", ContentFile(img_data), save=True)
            print(f"OK ({len(img_data)//1024} KB)")
        else:
            print("FAILED")
        time.sleep(0.3)


# --- CATEGORIES ---
print("\n" + "=" * 50)
print("Downloading REAL category images...")
print("=" * 50)

for cat in Category.objects.filter(parent__isnull=True):
    url = CATEGORY_IMAGES.get(cat.slug)
    if url:
        print(f"\n[Category: {cat.name}]")
        print(f"  Downloading...", end=" ")
        img_data = download_image(url)
        if img_data:
            cat.image.save(f"category_real_{cat.slug}.jpg", ContentFile(img_data), save=True)
            print(f"OK ({len(img_data)//1024} KB)")
        else:
            print("FAILED")
        time.sleep(0.3)


print("\n" + "=" * 50)
print("ALL DONE! Real images downloaded for all products.")
print("Refresh your browser to see the results.")
print("=" * 50)
