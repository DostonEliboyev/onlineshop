"""
Seed script to populate the database with sample furniture data.
Run with: python manage.py shell < seed_data.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture_shop.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Banner
from products.models import Category, Product, ProductImage

# Create superuser if not exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@luxehome.com', 'admin123')
    print("Superuser 'admin' created (password: admin123)")

# Create categories
categories_data = [
    ('Living Room', 'living-room'),
    ('Bedroom', 'bedroom'),
    ('Dining', 'dining'),
    ('Office', 'office'),
    ('Outdoor', 'outdoor'),
    ('Storage', 'storage'),
]

categories = {}
for name, slug in categories_data:
    cat, created = Category.objects.get_or_create(name=name, slug=slug)
    categories[slug] = cat
    if created:
        print(f"Category created: {name}")

# Subcategories
subcats_data = [
    ('Sofas', 'sofas', 'living-room'),
    ('Coffee Tables', 'coffee-tables', 'living-room'),
    ('TV Stands', 'tv-stands', 'living-room'),
    ('Beds', 'beds', 'bedroom'),
    ('Nightstands', 'nightstands', 'bedroom'),
    ('Wardrobes', 'wardrobes', 'bedroom'),
    ('Dining Tables', 'dining-tables', 'dining'),
    ('Dining Chairs', 'dining-chairs', 'dining'),
    ('Desks', 'desks', 'office'),
    ('Office Chairs', 'office-chairs', 'office'),
    ('Bookshelves', 'bookshelves', 'storage'),
]

for name, slug, parent_slug in subcats_data:
    cat, created = Category.objects.get_or_create(
        name=name, slug=slug, parent=categories[parent_slug]
    )
    categories[slug] = cat
    if created:
        print(f"  Subcategory created: {name}")

# Create sample products
products_data = [
    {
        'name': 'Modern Velvet Sofa',
        'slug': 'modern-velvet-sofa',
        'category': 'sofas',
        'description': 'Luxurious 3-seater velvet sofa with solid wood legs. Perfect for modern living rooms with its clean lines and plush comfort. Features high-density foam cushions and a durable hardwood frame.',
        'price': 1299.99,
        'old_price': 1599.99,
        'material': 'fabric',
        'color': 'grey',
        'dimensions': '220x90x85 cm',
        'weight': 45,
        'stock': 15,
        'is_featured': True,
    },
    {
        'name': 'Scandinavian Oak Coffee Table',
        'slug': 'scandinavian-oak-coffee-table',
        'category': 'coffee-tables',
        'description': 'Minimalist coffee table crafted from solid oak wood. Features tapered legs and a smooth natural finish. Includes a lower shelf for additional storage.',
        'price': 449.99,
        'old_price': None,
        'material': 'wood',
        'color': 'natural',
        'dimensions': '110x60x45 cm',
        'weight': 18,
        'stock': 25,
        'is_featured': True,
    },
    {
        'name': 'Leather Executive Office Chair',
        'slug': 'leather-executive-office-chair',
        'category': 'office-chairs',
        'description': 'Premium leather office chair with ergonomic design. Features adjustable height, tilt mechanism, and padded armrests. Perfect for long working hours.',
        'price': 699.99,
        'old_price': 899.99,
        'material': 'leather',
        'color': 'black',
        'dimensions': '65x65x120 cm',
        'weight': 22,
        'stock': 30,
        'is_featured': True,
    },
    {
        'name': 'Walnut King Size Bed Frame',
        'slug': 'walnut-king-size-bed-frame',
        'category': 'beds',
        'description': 'Elegant king-size bed frame made from premium walnut wood. Slatted base for optimal mattress support. Headboard features a beautiful grain pattern.',
        'price': 1899.99,
        'old_price': 2299.99,
        'material': 'wood',
        'color': 'brown',
        'dimensions': '200x180x110 cm',
        'weight': 65,
        'stock': 8,
        'is_featured': True,
    },
    {
        'name': 'Marble Top Dining Table',
        'slug': 'marble-top-dining-table',
        'category': 'dining-tables',
        'description': 'Stunning dining table with genuine marble top and black metal legs. Seats 6-8 people comfortably. The natural marble pattern makes each table unique.',
        'price': 2499.99,
        'old_price': None,
        'material': 'marble',
        'color': 'white',
        'dimensions': '180x90x75 cm',
        'weight': 80,
        'stock': 5,
        'is_featured': True,
    },
    {
        'name': 'Rattan Garden Lounge Set',
        'slug': 'rattan-garden-lounge-set',
        'category': 'outdoor',
        'description': 'Complete outdoor lounge set including 2-seater sofa, 2 armchairs, and coffee table. Weather-resistant rattan weave with waterproof cushions.',
        'price': 1599.99,
        'old_price': 1999.99,
        'material': 'rattan',
        'color': 'brown',
        'dimensions': '200x150x80 cm',
        'weight': 40,
        'stock': 10,
        'is_featured': True,
    },
    {
        'name': 'Industrial Metal Bookshelf',
        'slug': 'industrial-metal-bookshelf',
        'category': 'bookshelves',
        'description': '5-tier industrial bookshelf with metal frame and solid wood shelves. Perfect for displaying books, plants, and decorative items.',
        'price': 349.99,
        'old_price': 449.99,
        'material': 'metal',
        'color': 'black',
        'dimensions': '80x35x180 cm',
        'weight': 25,
        'stock': 20,
        'is_featured': False,
    },
    {
        'name': 'Velvet Dining Chair Set of 4',
        'slug': 'velvet-dining-chair-set',
        'category': 'dining-chairs',
        'description': 'Set of 4 elegant dining chairs with velvet upholstery and gold-finished metal legs. Comfortable padding and a modern design that elevates any dining space.',
        'price': 599.99,
        'old_price': 799.99,
        'material': 'fabric',
        'color': 'green',
        'dimensions': '45x55x85 cm each',
        'weight': 6,
        'stock': 12,
        'is_featured': True,
    },
    {
        'name': 'Minimalist TV Stand',
        'slug': 'minimalist-tv-stand',
        'category': 'tv-stands',
        'description': 'Clean-lined TV stand with cable management and soft-close drawers. Fits TVs up to 65 inches. Made from engineered wood with a matte white finish.',
        'price': 399.99,
        'old_price': None,
        'material': 'wood',
        'color': 'white',
        'dimensions': '160x40x50 cm',
        'weight': 30,
        'stock': 18,
        'is_featured': False,
    },
    {
        'name': 'Oak Nightstand with Drawer',
        'slug': 'oak-nightstand-drawer',
        'category': 'nightstands',
        'description': 'Compact nightstand crafted from solid oak. Features one drawer and an open shelf. Rounded edges and a warm natural finish.',
        'price': 199.99,
        'old_price': 249.99,
        'material': 'wood',
        'color': 'natural',
        'dimensions': '45x35x55 cm',
        'weight': 10,
        'stock': 35,
        'is_featured': False,
    },
    {
        'name': 'Standing Desk - Adjustable Height',
        'slug': 'standing-desk-adjustable',
        'category': 'desks',
        'description': 'Electric height-adjustable standing desk with memory presets. Bamboo top with steel frame. Smooth and quiet motor for effortless transitions between sitting and standing.',
        'price': 799.99,
        'old_price': 999.99,
        'material': 'wood',
        'color': 'natural',
        'dimensions': '140x70x65-130 cm',
        'weight': 35,
        'stock': 14,
        'is_featured': True,
    },
    {
        'name': 'Glass Console Table',
        'slug': 'glass-console-table',
        'category': 'living-room',
        'description': 'Elegant console table with tempered glass top and gold-finished metal frame. Perfect for entryways and living rooms.',
        'price': 329.99,
        'old_price': None,
        'material': 'glass',
        'color': 'natural',
        'dimensions': '120x35x80 cm',
        'weight': 15,
        'stock': 22,
        'is_featured': False,
    },
]

for p_data in products_data:
    cat_slug = p_data.pop('category')
    p_data['category'] = categories[cat_slug]
    product, created = Product.objects.get_or_create(
        slug=p_data['slug'],
        defaults=p_data
    )
    if created:
        print(f"Product created: {product.name}")

# Create banners
banners_data = [
    {
        'title': 'Elevate Your Living Space',
        'subtitle': 'Discover our premium furniture collection designed for modern homes.',
        'order': 1,
    },
    {
        'title': 'Up to 30% Off Selected Items',
        'subtitle': 'Limited time offers on sofas, beds, and dining sets. Shop now!',
        'order': 2,
    },
    {
        'title': 'New Arrivals for 2026',
        'subtitle': 'Fresh designs that bring warmth and character to every room.',
        'order': 3,
    },
]

for b_data in banners_data:
    banner, created = Banner.objects.get_or_create(
        title=b_data['title'],
        defaults=b_data
    )
    if created:
        print(f"Banner created: {banner.title}")

print("\nSeed data complete!")
print("Admin login: username='admin', password='admin123'")
print("Run the server: python manage.py runserver")
