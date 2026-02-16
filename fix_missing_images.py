import os, django, requests, time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture_shop.settings')
django.setup()
from django.core.files.base import ContentFile
from products.models import Product, ProductImage

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

fixes = {
    'oak-nightstand-drawer': [
        'https://images.unsplash.com/photo-1631679706909-1844bbd07221?w=800&q=80',
    ],
    'rattan-garden-lounge-set': [
        'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80',
        'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80',
    ],
    'leather-executive-office-chair': [
        'https://images.unsplash.com/photo-1596162954151-cdcb4c0f70a8?w=800&q=80',
    ],
}

for slug, urls in fixes.items():
    product = Product.objects.get(slug=slug)
    current_count = product.images.count()
    print(f"\n[{product.name}] Adding {len(urls)} more images...")
    for i, url in enumerate(urls):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
            if resp.status_code == 200 and len(resp.content) > 1000:
                pi = ProductImage(product=product, is_primary=False, order=current_count + i)
                pi.image.save(f"{slug}_fix_{i+1}.jpg", ContentFile(resp.content), save=True)
                print(f"  OK - {len(resp.content)//1024} KB")
            else:
                print(f"  Failed: status={resp.status_code}")
        except Exception as e:
            print(f"  Error: {e}")
        time.sleep(0.5)

print("\nFinal counts:")
for p in Product.objects.all():
    print(f"  {p.name}: {p.images.count()} images")
