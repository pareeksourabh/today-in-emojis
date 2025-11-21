#!/usr/bin/env python3
"""
Generate a profile image for Today in Emojis Instagram account.
Version 2: Better emoji handling for macOS.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

OUTPUT_DIR = "public/images"
SIZE = 1080

def create_profile_with_text():
    """Create a clean, minimal profile image with text-based design."""

    img = Image.new('RGB', (SIZE, SIZE), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Create subtle gradient background
    for y in range(SIZE):
        for x in range(SIZE):
            dx = x - SIZE // 2
            dy = y - SIZE // 2
            distance = (dx * dx + dy * dy) ** 0.5
            max_distance = (SIZE // 2) * 1.4
            factor = min(distance / max_distance, 1.0)

            # Soft blue gradient
            r = int(240 + (255 - 240) * factor)
            g = int(248 + (255 - 248) * factor)
            b = 255

            img.putpixel((x, y), (r, g, b))

    draw = ImageDraw.Draw(img)

    # Find a good font
    fonts = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]

    title_font = None
    tagline_font = None

    for font_path in fonts:
        if os.path.exists(font_path):
            try:
                title_font = ImageFont.truetype(font_path, 120)
                tagline_font = ImageFont.truetype(font_path, 42)
                break
            except Exception:
                continue

    if not title_font:
        title_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()

    # Draw "TIE" or stylized text
    title = "TiE"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (SIZE - text_width) // 2
    y = (SIZE - text_height) // 2 - 80

    # Draw with nice color
    draw.text((x, y), title, font=title_font, fill='#2563EB')

    # Tagline
    tagline = "today in emojis"
    bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    text_width = bbox[2] - bbox[0]
    x = (SIZE - text_width) // 2
    y = SIZE // 2 + 60

    draw.text((x, y), tagline, font=tagline_font, fill='#64748B')

    # Small decorative dots representing emojis
    dot_y = SIZE // 2 + 160
    dot_colors = ['#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6']
    dot_size = 20
    spacing = 50
    start_x = SIZE // 2 - (len(dot_colors) * spacing) // 2

    for i, color in enumerate(dot_colors):
        cx = start_x + i * spacing
        draw.ellipse([cx - dot_size//2, dot_y - dot_size//2,
                      cx + dot_size//2, dot_y + dot_size//2],
                     fill=color)

    output_path = os.path.join(OUTPUT_DIR, "profile-text.png")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"[success] Text-based profile: {output_path}")
    return output_path


def create_globe_profile():
    """Create profile with a stylized globe design."""

    img = Image.new('RGB', (SIZE, SIZE), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    center = SIZE // 2

    # Background gradient
    for y in range(SIZE):
        for x in range(SIZE):
            dx = x - center
            dy = y - center
            distance = (dx * dx + dy * dy) ** 0.5
            max_distance = center * 1.2
            factor = min(distance / max_distance, 1.0)
            r = int(248 + (255 - 248) * factor)
            g = int(250 + (255 - 250) * factor)
            b = 255
            img.putpixel((x, y), (r, g, b))

    draw = ImageDraw.Draw(img)

    # Draw stylized globe
    globe_radius = 280
    globe_color = '#3B82F6'  # Blue
    land_color = '#22C55E'   # Green

    # Ocean (main circle)
    draw.ellipse([center - globe_radius, center - globe_radius - 60,
                  center + globe_radius, center + globe_radius - 60],
                 fill=globe_color)

    # Simplified continents (abstract shapes)
    # North America / Europe area
    draw.ellipse([center - 180, center - 200, center - 20, center - 80],
                 fill=land_color)

    # Africa / South America area
    draw.ellipse([center - 60, center - 100, center + 80, center + 40],
                 fill=land_color)

    # Asia / Australia area
    draw.ellipse([center + 40, center - 140, center + 180, center - 20],
                 fill=land_color)

    draw.ellipse([center + 60, center + 20, center + 140, center + 100],
                 fill=land_color)

    # Add subtle highlight
    highlight_radius = globe_radius - 40
    for i in range(20):
        alpha = int(255 * (1 - i/20) * 0.1)
        x_offset = -80 + i * 2
        y_offset = -80 + i * 2
        # This is simplified - just adds some depth

    # Tagline
    fonts = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]

    tagline_font = None
    for font_path in fonts:
        if os.path.exists(font_path):
            try:
                tagline_font = ImageFont.truetype(font_path, 48)
                break
            except Exception:
                continue

    if tagline_font:
        tagline = "feel the day"
        bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
        text_width = bbox[2] - bbox[0]
        x = (SIZE - text_width) // 2
        y = SIZE - 160
        draw.text((x, y), tagline, font=tagline_font, fill='#64748B')

    output_path = os.path.join(OUTPUT_DIR, "profile-globe.png")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"[success] Globe profile: {output_path}")
    return output_path


def create_minimal_emoji_dots():
    """Create ultra-minimal design with 5 colored dots."""

    img = Image.new('RGB', (SIZE, SIZE), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Five dots representing 5 emojis
    colors = ['#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6']
    dot_radius = 60
    spacing = 160

    center_y = SIZE // 2
    start_x = SIZE // 2 - (len(colors) - 1) * spacing // 2

    for i, color in enumerate(colors):
        cx = start_x + i * spacing
        draw.ellipse([cx - dot_radius, center_y - dot_radius,
                      cx + dot_radius, center_y + dot_radius],
                     fill=color)

    output_path = os.path.join(OUTPUT_DIR, "profile-dots.png")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"[success] Minimal dots profile: {output_path}")
    return output_path


if __name__ == "__main__":
    print("Generating profile image options...\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate all options
    create_globe_profile()
    create_profile_with_text()
    create_minimal_emoji_dots()

    print(f"\n[done] Generated 3 profile image options in {OUTPUT_DIR}/")
    print("\nOptions created:")
    print("  1. profile-globe.png   - Stylized globe design")
    print("  2. profile-text.png    - 'TiE' text with dots")
    print("  3. profile-dots.png    - Minimal 5 colored dots")
    print("\nChoose the one you like best for your Instagram profile!")
