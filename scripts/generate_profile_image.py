#!/usr/bin/env python3
"""
Generate a profile image for Today in Emojis Instagram account.

Creates a minimal, clean profile picture with the globe emoji
that matches the project's aesthetic.

Output: 1080x1080px PNG (Instagram recommended size)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
OUTPUT_DIR = "public/images"
OUTPUT_FILE = "profile-image.png"
SIZE = 1080  # Instagram profile images are displayed at 320x320 but uploaded larger

def create_profile_image():
    """Create a minimal profile image with globe emoji."""

    # Create canvas with white background
    img = Image.new('RGB', (SIZE, SIZE), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Try to load a font that supports emojis
    # Fall back to default if not available
    emoji_size = 400

    # For emoji rendering, we'll use a different approach
    # Create a gradient background for visual interest

    # Simple radial-ish gradient (light blue to white)
    for y in range(SIZE):
        for x in range(SIZE):
            # Distance from center
            dx = x - SIZE // 2
            dy = y - SIZE // 2
            distance = (dx * dx + dy * dy) ** 0.5
            max_distance = (SIZE // 2) * 1.2

            # Gradient factor (0 at center, 1 at edges)
            factor = min(distance / max_distance, 1.0)

            # Color interpolation (center: light blue, edge: white)
            r = int(230 + (255 - 230) * factor)
            g = int(240 + (255 - 240) * factor)
            b = int(255)

            img.putpixel((x, y), (r, g, b))

    # Redraw on the gradient
    draw = ImageDraw.Draw(img)

    # Try to find a font that can render emojis
    # Common emoji font locations
    emoji_fonts = [
        "/System/Library/Fonts/Apple Color Emoji.ttc",  # macOS
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",  # Linux
        "C:\\Windows\\Fonts\\seguiemj.ttf",  # Windows
        "/System/Library/Fonts/AppleColorEmoji.ttf",  # macOS alternative
    ]

    font = None
    for font_path in emoji_fonts:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, emoji_size)
                break
            except Exception:
                continue

    # Draw the globe emoji
    emoji = "🌍"

    if font:
        # Get text bounding box for centering
        bbox = draw.textbbox((0, 0), emoji, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (SIZE - text_width) // 2
        y = (SIZE - text_height) // 2 - 40  # Slight upward offset

        draw.text((x, y), emoji, font=font, embedded_color=True)
    else:
        # Fallback: Draw a simple globe representation
        # This is a simplified version if emoji fonts aren't available
        print("[info] Emoji font not found, creating simplified globe design")

        # Draw a circle (globe)
        center = SIZE // 2
        radius = 200

        # Globe circle
        draw.ellipse(
            [center - radius, center - radius - 40,
             center + radius, center + radius - 40],
            fill='#4A90D9',
            outline='#2E5A8A',
            width=8
        )

        # Simple continent shapes (abstract)
        # This is a very simplified representation
        draw.ellipse(
            [center - 80, center - 100, center + 40, center - 20],
            fill='#6AB04C'
        )
        draw.ellipse(
            [center - 40, center - 40, center + 100, center + 60],
            fill='#6AB04C'
        )

    # Add subtle text at bottom
    try:
        # Try to load a clean sans-serif font
        text_fonts = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNSText.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
        ]

        text_font = None
        for font_path in text_fonts:
            if os.path.exists(font_path):
                try:
                    text_font = ImageFont.truetype(font_path, 48)
                    break
                except Exception:
                    continue

        if text_font:
            # Add tagline
            tagline = "feel the day"
            bbox = draw.textbbox((0, 0), tagline, font=text_font)
            text_width = bbox[2] - bbox[0]
            x = (SIZE - text_width) // 2
            y = SIZE - 150

            draw.text((x, y), tagline, font=text_font, fill='#666666')
    except Exception as e:
        print(f"[info] Could not add tagline: {e}")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save the image
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    img.save(output_path, 'PNG', quality=95)

    print(f"[success] Profile image created: {output_path}")
    print(f"[info] Size: {SIZE}x{SIZE}px")

    return output_path


def create_alternative_designs():
    """Create a few alternative profile image designs."""

    designs = [
        {
            "name": "profile-dark.png",
            "bg_color": "#1a1a2e",
            "text_color": "#ffffff",
            "accent": "#4a90d9"
        },
        {
            "name": "profile-gradient.png",
            "bg_color": "gradient",
            "text_color": "#333333",
            "accent": "#667eea"
        }
    ]

    for design in designs:
        img = Image.new('RGB', (SIZE, SIZE), color='#FFFFFF')
        draw = ImageDraw.Draw(img)

        if design["bg_color"] == "gradient":
            # Purple to pink gradient
            for y in range(SIZE):
                r = int(102 + (236 - 102) * y / SIZE)
                g = int(126 + (72 - 126) * y / SIZE)
                b = int(234 + (153 - 234) * y / SIZE)
                for x in range(SIZE):
                    img.putpixel((x, y), (r, g, b))
        else:
            img = Image.new('RGB', (SIZE, SIZE), color=design["bg_color"])

        draw = ImageDraw.Draw(img)

        # Try to draw emoji
        emoji_fonts = [
            "/System/Library/Fonts/Apple Color Emoji.ttc",
            "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
        ]

        for font_path in emoji_fonts:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, 400)
                    emoji = "🌍"
                    bbox = draw.textbbox((0, 0), emoji, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    x = (SIZE - text_width) // 2
                    y = (SIZE - text_height) // 2 - 40
                    draw.text((x, y), emoji, font=font, embedded_color=True)
                    break
                except Exception:
                    continue

        output_path = os.path.join(OUTPUT_DIR, design["name"])
        img.save(output_path, 'PNG', quality=95)
        print(f"[success] Alternative design created: {output_path}")


if __name__ == "__main__":
    # Check for Pillow
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow is required. Install with: pip install pillow")
        exit(1)

    # Create main profile image
    create_profile_image()

    # Optionally create alternatives
    # create_alternative_designs()

    print("\n[done] Profile image generation complete!")
    print("Upload the image to Instagram as your profile picture.")
