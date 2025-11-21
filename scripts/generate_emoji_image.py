#!/usr/bin/env python3
"""
Generate a daily emoji image for Instagram posting.

Reads the 5 emojis from public/data/today.json and creates
a 1080x1080px image suitable for Instagram posts.

Uses macOS sips/textutil for proper emoji rendering, or falls back to Pillow.

Output: public/images/daily/YYYY-MM-DD.png
"""

import os
import sys
import json
import subprocess
import tempfile
from datetime import date
from PIL import Image

# Configuration
INPUT_FILE = "public/data/today.json"
OUTPUT_DIR = "public/images/daily"
SIZE = 1080  # Instagram square format

def load_emoji_data():
    """Load today's emoji data from JSON file."""
    if not os.path.exists(INPUT_FILE):
        print(f"[error] Input file not found: {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data

def generate_with_html(emoji_chars, output_path):
    """Generate image using HTML rendering via wkhtmltoimage or similar."""

    emoji_html = "".join([f'<span style="font-size: 120px; margin: 0 10px;">{e}</span>' for e in emoji_chars])

    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            width: {SIZE}px;
            height: {SIZE}px;
            display: flex;
            justify-content: center;
            align-items: center;
            background: white;
            font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
        }}
        .emoji-container {{
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
        }}
    </style>
</head>
<body>
    <div class="emoji-container">
        {emoji_html}
    </div>
</body>
</html>'''

    # Write HTML to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_content)
        html_path = f.name

    try:
        # Try using wkhtmltoimage if available
        result = subprocess.run(
            ['which', 'wkhtmltoimage'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            subprocess.run([
                'wkhtmltoimage',
                '--width', str(SIZE),
                '--height', str(SIZE),
                '--quality', '100',
                html_path,
                output_path
            ], check=True)
            return True
    except Exception as e:
        print(f"[info] wkhtmltoimage not available: {e}", file=sys.stderr)
    finally:
        os.unlink(html_path)

    return False

def generate_with_pillow(emoji_chars, output_path):
    """Generate image using Pillow - emojis may appear as text/boxes."""
    from PIL import ImageDraw, ImageFont

    img = Image.new('RGB', (SIZE, SIZE), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Try emoji fonts
    emoji_fonts = [
        "/System/Library/Fonts/Apple Color Emoji.ttc",
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
        "C:\\Windows\\Fonts\\seguiemj.ttf",
    ]

    emoji_font = None
    for font_path in emoji_fonts:
        if os.path.exists(font_path):
            try:
                emoji_font = ImageFont.truetype(font_path, 120)
                break
            except Exception:
                continue

    if not emoji_font:
        # Use any available font
        try:
            emoji_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
        except:
            emoji_font = ImageFont.load_default()

    # Draw emojis in a row
    emoji_text = "  ".join(emoji_chars)

    try:
        bbox = draw.textbbox((0, 0), emoji_text, font=emoji_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except:
        text_width = len(emoji_text) * 80
        text_height = 120

    x = (SIZE - text_width) // 2
    y = (SIZE - text_height) // 2

    try:
        draw.text((x, y), emoji_text, font=emoji_font, embedded_color=True)
    except TypeError:
        # embedded_color not supported in older Pillow
        draw.text((x, y), emoji_text, font=emoji_font, fill='#000000')

    img.save(output_path, 'PNG')
    return True

def generate_with_imagemagick(emoji_chars, output_path):
    """Generate image using ImageMagick - best emoji support."""

    emoji_text = " ".join(emoji_chars)

    try:
        # Check if convert (ImageMagick) is available
        result = subprocess.run(['which', 'convert'], capture_output=True, text=True)

        if result.returncode != 0:
            return False

        # Use ImageMagick to create the image
        subprocess.run([
            'convert',
            '-size', f'{SIZE}x{SIZE}',
            'xc:white',
            '-gravity', 'center',
            '-font', 'Apple-Color-Emoji',
            '-pointsize', '120',
            '-annotate', '0', emoji_text,
            output_path
        ], check=True)

        return True
    except Exception as e:
        print(f"[info] ImageMagick failed: {e}", file=sys.stderr)
        return False

def generate_with_swift(emoji_chars, output_path):
    """Generate image using Swift/AppKit - native macOS rendering."""

    emoji_text = " ".join(emoji_chars)

    swift_code = f'''
import Cocoa

let size = NSSize(width: {SIZE}, height: {SIZE})
let image = NSImage(size: size)

image.lockFocus()

// White background
NSColor.white.setFill()
NSRect(origin: .zero, size: size).fill()

// Draw emojis
let text = "{emoji_text}"
let font = NSFont.systemFont(ofSize: 120)
let attributes: [NSAttributedString.Key: Any] = [
    .font: font
]

let textSize = text.size(withAttributes: attributes)
let x = (size.width - textSize.width) / 2
let y = (size.height - textSize.height) / 2

text.draw(at: NSPoint(x: x, y: y), withAttributes: attributes)

image.unlockFocus()

// Save as PNG
if let tiffData = image.tiffRepresentation,
   let bitmapRep = NSBitmapImageRep(data: tiffData),
   let pngData = bitmapRep.representation(using: .png, properties: [:]) {{
    try? pngData.write(to: URL(fileURLWithPath: "{output_path}"))
    print("Success")
}}
'''

    try:
        # Write Swift code to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.swift', delete=False) as f:
            f.write(swift_code)
            swift_path = f.name

        # Run Swift
        result = subprocess.run(
            ['swift', swift_path],
            capture_output=True,
            text=True
        )

        os.unlink(swift_path)

        if result.returncode == 0 and os.path.exists(output_path):
            return True
        else:
            if result.stderr:
                print(f"[info] Swift error: {result.stderr}", file=sys.stderr)
            return False

    except Exception as e:
        print(f"[info] Swift rendering failed: {e}", file=sys.stderr)
        return False

def main():
    print("[info] Loading emoji data...")
    data = load_emoji_data()

    emojis = data.get('emojis', [])
    emoji_chars = [e.get('char', '?') for e in emojis]
    print(f"[info] Emojis: {' '.join(emoji_chars)}")

    # Prepare output path
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img_date = data.get('date', date.today().isoformat())
    output_path = os.path.join(OUTPUT_DIR, f"{img_date}.png")

    print("[info] Generating image...")

    # Try different rendering methods
    success = False

    # Method 1: Swift (best for macOS)
    if sys.platform == 'darwin':
        print("[info] Trying Swift/AppKit rendering...")
        success = generate_with_swift(emoji_chars, output_path)
        if success:
            print("[success] Generated with Swift/AppKit")

    # Method 2: ImageMagick
    if not success:
        print("[info] Trying ImageMagick rendering...")
        success = generate_with_imagemagick(emoji_chars, output_path)
        if success:
            print("[success] Generated with ImageMagick")

    # Method 3: Pillow fallback
    if not success:
        print("[info] Using Pillow fallback...")
        success = generate_with_pillow(emoji_chars, output_path)
        if success:
            print("[success] Generated with Pillow (emojis may appear as text)")

    if success and os.path.exists(output_path):
        print(f"[success] Image saved: {output_path}")
        print(f"OUTPUT_PATH={output_path}")
        return 0
    else:
        print("[error] Failed to generate image", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
