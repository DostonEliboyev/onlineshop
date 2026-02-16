"""
Create 3 beautiful banner images for the homepage slideshow.
Uses the best available downloaded photos, crops to 1920x600 banner size,
and applies a subtle dark gradient so white text is readable.
"""
import os, django, glob, shutil
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture_shop.settings')
django.setup()

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from django.core.files.base import ContentFile
from core.models import Banner
from io import BytesIO

BANNER_DIR = r'e:\lession\media\banners'
TARGET_W, TARGET_H = 1920, 600


def make_banner(source_path, output_name, darken=0.65, saturation=1.3, warmth=1.05):
    """
    Open a source photo, crop/resize to 1920x600, boost colors,
    add a left-side gradient for text, save as high-quality JPEG.
    """
    img = Image.open(source_path).convert('RGB')
    
    # Resize to at least 1920 wide, keeping aspect ratio
    w, h = img.size
    scale = max(TARGET_W / w, TARGET_H / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    
    # Center crop to 1920x600
    left = (new_w - TARGET_W) // 2
    top = (new_h - TARGET_H) // 2
    img = img.crop((left, top, left + TARGET_W, top + TARGET_H))
    
    # Boost saturation for richer colors
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(saturation)
    
    # Slight contrast boost
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.1)
    
    # Apply a left-to-right dark gradient overlay for text readability
    gradient = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)
    for x in range(TARGET_W):
        # Left side darker, right side nearly transparent
        if x < TARGET_W * 0.45:
            alpha = int(180 * (1 - x / (TARGET_W * 0.45)))
        else:
            alpha = 0
        draw.line([(x, 0), (x, TARGET_H)], fill=(0, 0, 0, alpha))
    
    # Composite
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, gradient)
    img = img.convert('RGB')
    
    # Save
    buf = BytesIO()
    img.save(buf, format='JPEG', quality=92)
    return buf.getvalue()


# Pick the best source images (largest/richest ones we downloaded)
# Banner 1: hero_1 (modern kitchen/interior - brightness 110, nice and dark)
# Banner 2: hero_2 (cozy room - brightness 126)  
# Banner 3: real_2 or vivid_2 (1920x1080, good ratio)

sources = [
    os.path.join(BANNER_DIR, 'banner_hero_1_c90fa208.jpg'),
    os.path.join(BANNER_DIR, 'banner_hero_2_63383862.jpg'),
    os.path.join(BANNER_DIR, 'banner_hero_3_1eab45a9.jpg'),
]

# Verify sources exist, use fallbacks
for i, src in enumerate(sources):
    if not os.path.exists(src):
        # Find any available banner image
        avail = sorted(glob.glob(os.path.join(BANNER_DIR, '*.jpg')), 
                       key=os.path.getsize, reverse=True)
        if avail:
            sources[i] = avail[min(i, len(avail)-1)]

print("Creating beautiful banner images...")
print(f"Target size: {TARGET_W}x{TARGET_H}\n")

banner_files = []
for i, src in enumerate(sources):
    print(f"Banner {i+1}: Using source {os.path.basename(src)}")
    img_data = make_banner(src, f"banner_final_{i+1}.jpg")
    banner_files.append((f"banner_final_{i+1}.jpg", img_data))
    
    # Verify the result
    result = Image.open(BytesIO(img_data))
    print(f"  Result: {result.size[0]}x{result.size[1]}, {len(img_data)//1024} KB")

# Clean up old banner files
print("\nCleaning up old banner files...")
old_files = glob.glob(os.path.join(BANNER_DIR, '*.jpg'))
for f in old_files:
    os.remove(f)
    print(f"  Removed: {os.path.basename(f)}")

# Save new banners and update database
print("\nSaving final banners to database...")
banners = list(Banner.objects.all().order_by('order'))
for idx, banner in enumerate(banners):
    if idx < len(banner_files):
        fname, data = banner_files[idx]
        banner.image.save(fname, ContentFile(data), save=True)
        print(f"  [{banner.title}] -> {banner.image.name}")

print("\nDone! 3 beautiful furniture banners created.")
print("Hard-refresh your browser (Ctrl+Shift+R) to see them.")
