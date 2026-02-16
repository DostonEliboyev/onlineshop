"""
Generate placeholder images for all products and banners.
Run with: python generate_images.py
"""
import os
import sys
import django
import random
import math

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture_shop.settings')
django.setup()

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.core.files.base import ContentFile
from io import BytesIO
from products.models import Product, ProductImage, Category
from core.models import Banner


def get_font(size):
    """Try to get a nice font, fall back to default."""
    font_paths = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()


def draw_furniture_icon(draw, cx, cy, icon_type, color, size=80):
    """Draw simple furniture-like shapes."""
    s = size
    lighter = tuple(min(c + 40, 255) for c in color[:3])
    darker = tuple(max(c - 40, 0) for c in color[:3])

    if icon_type == 'sofa':
        # Sofa shape
        draw.rounded_rectangle([cx-s, cy-s//3, cx+s, cy+s//3], radius=15, fill=lighter)
        draw.rounded_rectangle([cx-s+10, cy-s//2, cx-s+25, cy+s//3], radius=8, fill=color)
        draw.rounded_rectangle([cx+s-25, cy-s//2, cx+s-10, cy+s//3], radius=8, fill=color)
        draw.rounded_rectangle([cx-s+5, cy-s//3-15, cx+s-5, cy-s//3+5], radius=10, fill=color)
        # Legs
        for lx in [cx-s+15, cx+s-15]:
            draw.rectangle([lx-3, cy+s//3, lx+3, cy+s//3+12], fill=darker)

    elif icon_type == 'table':
        # Table top
        draw.rounded_rectangle([cx-s, cy-8, cx+s, cy+8], radius=5, fill=lighter)
        # Legs
        for lx in [cx-s+12, cx+s-12]:
            draw.rectangle([lx-4, cy+8, lx+4, cy+s//1.5], fill=color)

    elif icon_type == 'chair':
        # Seat
        draw.rounded_rectangle([cx-s//2, cy, cx+s//2, cy+15], radius=5, fill=lighter)
        # Back
        draw.rounded_rectangle([cx-s//2, cy-s//1.5, cx+s//2, cy+5], radius=8, fill=color)
        # Legs
        for lx in [cx-s//2+8, cx+s//2-8]:
            draw.rectangle([lx-3, cy+15, lx+3, cy+s//2+15], fill=darker)

    elif icon_type == 'bed':
        # Mattress
        draw.rounded_rectangle([cx-s, cy-10, cx+s, cy+20], radius=8, fill=lighter)
        # Headboard
        draw.rounded_rectangle([cx-s, cy-s//2, cx-s+15, cy+20], radius=8, fill=color)
        # Pillow
        draw.rounded_rectangle([cx-s+20, cy-5, cx-s//3, cy+10], radius=6, fill=(255, 255, 255, 200))

    elif icon_type == 'shelf':
        # Frame
        draw.rectangle([cx-s//1.5, cy-s//1.5, cx-s//1.5+8, cy+s//1.5], fill=color)
        draw.rectangle([cx+s//1.5-8, cy-s//1.5, cx+s//1.5, cy+s//1.5], fill=color)
        # Shelves
        for i in range(4):
            sy = cy - s//1.5 + i * (2*s//1.5 // 3)
            draw.rectangle([cx-s//1.5, sy, cx+s//1.5, sy+6], fill=lighter)

    elif icon_type == 'lamp':
        # Shade
        points = [(cx-s//2, cy), (cx+s//2, cy), (cx+s//4, cy-s//1.5), (cx-s//4, cy-s//1.5)]
        draw.polygon(points, fill=lighter)
        # Stand
        draw.rectangle([cx-3, cy, cx+3, cy+s//1.2], fill=color)
        # Base
        draw.ellipse([cx-s//3, cy+s//1.2-5, cx+s//3, cy+s//1.2+5], fill=color)

    else:
        # Generic box/furniture
        draw.rounded_rectangle([cx-s//1.5, cy-s//2, cx+s//1.5, cy+s//2], radius=10, fill=lighter)
        draw.rounded_rectangle([cx-s//2, cy-s//3, cx+s//2, cy+s//3], radius=8, fill=color)


def create_product_image(product_name, width=800, height=800, palette=None, icon='sofa', variant=0):
    """Create a styled product placeholder image."""
    if palette is None:
        palette = {
            'bg': (245, 240, 235),
            'primary': (140, 110, 80),
            'accent': (200, 148, 90),
        }

    img = Image.new('RGB', (width, height), palette['bg'])
    draw = ImageDraw.Draw(img)

    # Subtle gradient/texture
    for y in range(height):
        factor = 1 - (y / height) * 0.08
        r = int(palette['bg'][0] * factor)
        g = int(palette['bg'][1] * factor)
        b = int(palette['bg'][2] * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Decorative circles in background
    random.seed(hash(product_name) + variant)
    for _ in range(5):
        cx = random.randint(50, width-50)
        cy = random.randint(50, height-50)
        radius = random.randint(30, 100)
        opacity_color = tuple(list(palette['bg'][:3]))
        lighter = tuple(min(c + 8, 255) for c in opacity_color)
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=lighter)

    # Draw furniture icon in center
    draw_furniture_icon(draw, width//2, height//2 - 30, icon, palette['primary'], size=100 + variant*10)

    # Shadow under furniture
    shadow_y = height//2 + 60
    draw.ellipse([width//2-90, shadow_y, width//2+90, shadow_y+15],
                 fill=tuple(max(c-20, 0) for c in palette['bg']))

    # Product name text
    font_large = get_font(28)
    font_small = get_font(16)

    # Text background
    text_y = height - 120
    draw.rectangle([0, text_y, width, height], fill=(*palette['primary'], 200))

    # Product name
    bbox = draw.textbbox((0, 0), product_name, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, text_y + 20), product_name, fill=(255, 255, 255), font=font_large)

    # "LuxeHome" branding
    brand = "LuxeHome Furniture"
    bbox2 = draw.textbbox((0, 0), brand, font=font_small)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((width - tw2) // 2, text_y + 60), brand, fill=(200, 200, 200), font=font_small)

    # Variant indicator (for multiple images)
    if variant > 0:
        labels = ["Front View", "Side View", "Detail", "Lifestyle"]
        label = labels[variant % len(labels)]
        draw.rounded_rectangle([width-150, 15, width-15, 45], radius=12,
                               fill=palette['accent'])
        lbbox = draw.textbbox((0, 0), label, font=font_small)
        ltw = lbbox[2] - lbbox[0]
        draw.text((width - 82 - ltw//2, 19), label, fill=(255, 255, 255), font=font_small)

    buf = BytesIO()
    img.save(buf, format='JPEG', quality=90)
    return buf.getvalue()


def create_banner_image(title, width=1920, height=500, color_scheme=0):
    """Create a wide banner image."""
    schemes = [
        {'bg_start': (44, 44, 44), 'bg_end': (26, 26, 46), 'accent': (200, 148, 90)},
        {'bg_start': (45, 55, 65), 'bg_end': (25, 35, 45), 'accent': (218, 165, 32)},
        {'bg_start': (60, 40, 30), 'bg_end': (30, 20, 15), 'accent': (200, 160, 100)},
    ]
    scheme = schemes[color_scheme % len(schemes)]

    img = Image.new('RGB', (width, height), scheme['bg_start'])
    draw = ImageDraw.Draw(img)

    # Gradient background
    for x in range(width):
        t = x / width
        r = int(scheme['bg_start'][0] * (1-t) + scheme['bg_end'][0] * t)
        g = int(scheme['bg_start'][1] * (1-t) + scheme['bg_end'][1] * t)
        b = int(scheme['bg_start'][2] * (1-t) + scheme['bg_end'][2] * t)
        draw.line([(x, 0), (x, height)], fill=(r, g, b))

    # Decorative shapes
    random.seed(color_scheme * 42)
    for _ in range(12):
        cx = random.randint(width//2, width-100)
        cy = random.randint(50, height-50)
        radius = random.randint(20, 80)
        c = tuple(min(v+15, 255) for v in scheme['bg_end'])
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=c)

    # Large decorative accent circle on the right
    draw.ellipse([width-450, -50, width+50, height+50],
                 fill=tuple(max(v-5, 0) for v in scheme['bg_end']))

    # Draw a furniture icon on the right side
    icons = ['sofa', 'table', 'bed']
    draw_furniture_icon(draw, width - 250, height//2, icons[color_scheme % 3],
                       scheme['accent'], size=120)

    # Accent line
    draw.rectangle([60, height-8, 300, height], fill=scheme['accent'])

    # Title text on the left
    font_title = get_font(52)
    font_sub = get_font(22)

    draw.text((80, height//2 - 60), title, fill=(255, 255, 255), font=font_title)
    draw.text((80, height//2 + 10), "Premium Furniture Collection", fill=scheme['accent'], font=font_sub)

    buf = BytesIO()
    img.save(buf, format='JPEG', quality=90)
    return buf.getvalue()


# Product color/icon mapping
PRODUCT_STYLES = {
    'sofa': {'icon': 'sofa', 'palette': {'bg': (245, 240, 235), 'primary': (120, 120, 130), 'accent': (180, 150, 120)}},
    'coffee-table': {'icon': 'table', 'palette': {'bg': (248, 243, 238), 'primary': (160, 120, 70), 'accent': (200, 160, 100)}},
    'chair': {'icon': 'chair', 'palette': {'bg': (240, 240, 240), 'primary': (50, 50, 50), 'accent': (100, 100, 100)}},
    'bed': {'icon': 'bed', 'palette': {'bg': (245, 242, 238), 'primary': (120, 80, 50), 'accent': (180, 140, 100)}},
    'table': {'icon': 'table', 'palette': {'bg': (248, 248, 248), 'primary': (180, 180, 180), 'accent': (140, 140, 140)}},
    'outdoor': {'icon': 'sofa', 'palette': {'bg': (238, 243, 238), 'primary': (100, 80, 50), 'accent': (160, 140, 100)}},
    'shelf': {'icon': 'shelf', 'palette': {'bg': (242, 240, 238), 'primary': (60, 60, 60), 'accent': (160, 120, 80)}},
    'tv': {'icon': 'shelf', 'palette': {'bg': (248, 248, 248), 'primary': (200, 200, 200), 'accent': (160, 160, 160)}},
    'desk': {'icon': 'table', 'palette': {'bg': (245, 242, 235), 'primary': (180, 150, 100), 'accent': (200, 170, 120)}},
    'glass': {'icon': 'table', 'palette': {'bg': (245, 248, 250), 'primary': (180, 200, 210), 'accent': (200, 180, 130)}},
    'nightstand': {'icon': 'shelf', 'palette': {'bg': (248, 245, 240), 'primary': (170, 140, 90), 'accent': (200, 170, 120)}},
    'wardrobe': {'icon': 'shelf', 'palette': {'bg': (245, 242, 238), 'primary': (130, 100, 70), 'accent': (180, 150, 110)}},
}


def get_style_for_product(product):
    """Determine visual style based on product name/category."""
    name_lower = product.name.lower()
    cat_lower = product.category.slug.lower()

    for key, style in PRODUCT_STYLES.items():
        if key in name_lower or key in cat_lower:
            return style

    return {'icon': 'sofa', 'palette': {'bg': (245, 240, 235), 'primary': (140, 110, 80), 'accent': (200, 148, 90)}}


# Generate product images
print("Generating product images...")
products = Product.objects.all()

for product in products:
    existing = product.images.count()
    if existing > 0:
        print(f"  Skipping {product.name} (already has {existing} images)")
        continue

    style = get_style_for_product(product)
    num_images = random.randint(3, 5)

    for i in range(num_images):
        img_data = create_product_image(
            product.name,
            palette=style['palette'],
            icon=style['icon'],
            variant=i
        )
        filename = f"{product.slug}_{i+1}.jpg"

        pi = ProductImage(
            product=product,
            is_primary=(i == 0),
            order=i
        )
        pi.image.save(filename, ContentFile(img_data), save=True)
        print(f"  Created image {i+1}/{num_images} for {product.name}")

print(f"\nProduct images done! ({products.count()} products)")

# Generate banner images
print("\nGenerating banner images...")
banners = Banner.objects.all()

for idx, banner in enumerate(banners):
    if banner.image:
        print(f"  Skipping banner: {banner.title} (already has image)")
        continue

    img_data = create_banner_image(banner.title, color_scheme=idx)
    filename = f"banner_{idx+1}.jpg"
    banner.image.save(filename, ContentFile(img_data), save=True)
    print(f"  Created banner image: {banner.title}")

# Generate category images
print("\nGenerating category images...")
categories = Category.objects.filter(parent__isnull=True)

cat_icons = {
    'living-room': 'sofa',
    'bedroom': 'bed',
    'dining': 'table',
    'office': 'chair',
    'outdoor': 'sofa',
    'storage': 'shelf',
}

cat_colors = {
    'living-room': {'bg': (245, 240, 235), 'primary': (140, 110, 80), 'accent': (200, 148, 90)},
    'bedroom': {'bg': (240, 238, 245), 'primary': (100, 80, 120), 'accent': (160, 140, 180)},
    'dining': {'bg': (245, 242, 235), 'primary': (160, 120, 70), 'accent': (200, 160, 100)},
    'office': {'bg': (240, 242, 245), 'primary': (60, 70, 80), 'accent': (100, 120, 140)},
    'outdoor': {'bg': (235, 245, 238), 'primary': (70, 120, 80), 'accent': (120, 180, 130)},
    'storage': {'bg': (242, 240, 238), 'primary': (80, 60, 50), 'accent': (140, 110, 90)},
}

for cat in categories:
    if cat.image:
        print(f"  Skipping category: {cat.name} (already has image)")
        continue

    icon = cat_icons.get(cat.slug, 'sofa')
    palette = cat_colors.get(cat.slug, {'bg': (245, 240, 235), 'primary': (140, 110, 80), 'accent': (200, 148, 90)})

    img_data = create_product_image(cat.name, width=600, height=400, palette=palette, icon=icon)
    filename = f"category_{cat.slug}.jpg"
    cat.image.save(filename, ContentFile(img_data), save=True)
    print(f"  Created category image: {cat.name}")

print("\nAll images generated successfully!")
