#!/usr/bin/env python3
"""
Generate a daily emoji image for Instagram posting.

Reads the 5 emojis from public/data/today.json and creates
a 1080x1080px image suitable for Instagram posts.

Supports:
- macOS: Swift/AppKit rendering
- Linux: Noto Color Emoji font
- Fallback: Pillow with system fonts

Output: public/images/daily/YYYY-MM-DD.png
"""

import os
import sys
import json
import subprocess
import tempfile
from datetime import date
from PIL import Image, ImageDraw, ImageFont

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

def generate_with_pillow_noto(emoji_chars, output_path):
    """Generate image using Pillow with Noto Color Emoji font (Linux)."""

    img = Image.new('RGB', (SIZE, SIZE), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Noto Color Emoji font paths (common locations)
    noto_fonts = [
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
        "/usr/share/fonts/noto-emoji/NotoColorEmoji.ttf",
        "/usr/share/fonts/google-noto-emoji/NotoColorEmoji.ttf",
        "/usr/local/share/fonts/NotoColorEmoji.ttf",
    ]

    emoji_font = None
    for font_path in noto_fonts:
        if os.path.exists(font_path):
            try:
                emoji_font = ImageFont.truetype(font_path, 109)
                print(f"[info] Using Noto Color Emoji: {font_path}")
                break
            except Exception as e:
                print(f"[warn] Failed to load {font_path}: {e}", file=sys.stderr)
                continue

    if not emoji_font:
        print("[warn] Noto Color Emoji not found", file=sys.stderr)
        return False

    # Draw emojis in a row
    emoji_y = SIZE // 2
    spacing = 180
    start_x = SIZE // 2 - (len(emoji_chars) - 1) * spacing // 2

    for i, char in enumerate(emoji_chars):
        x = start_x + i * spacing

        try:
            # Get bounding box to center each emoji
            bbox = draw.textbbox((0, 0), char, font=emoji_font)
            char_width = bbox[2] - bbox[0]
            char_height = bbox[3] - bbox[1]

            # Center the emoji at this position
            draw_x = x - char_width // 2
            draw_y = emoji_y - char_height // 2

            draw.text((draw_x, draw_y), char, font=emoji_font, embedded_color=True)
        except Exception as e:
            print(f"[warn] Error drawing emoji {char}: {e}", file=sys.stderr)
            # Try without embedded_color
            try:
                draw.text((draw_x, draw_y), char, font=emoji_font, fill='#000000')
            except:
                pass

    img.save(output_path, 'PNG')
    return True

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

def generate_with_pango(emoji_chars, output_path):
    """Generate image using Pango/Cairo via ImageMagick (Linux)."""

    emoji_text = " ".join(emoji_chars)

    try:
        # Check if ImageMagick is available
        result = subprocess.run(['which', 'convert'], capture_output=True, text=True)
        if result.returncode != 0:
            return False

        # Use ImageMagick with Pango for better emoji support
        cmd = [
            'convert',
            '-size', f'{SIZE}x{SIZE}',
            'xc:white',
            '-gravity', 'center',
            '-font', 'Noto-Color-Emoji',
            '-pointsize', '100',
            '-annotate', '0', emoji_text,
            output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0 and os.path.exists(output_path):
            return True
        else:
            if result.stderr:
                print(f"[info] ImageMagick error: {result.stderr}", file=sys.stderr)
            return False

    except Exception as e:
        print(f"[info] Pango/ImageMagick failed: {e}", file=sys.stderr)
        return False

def generate_fallback(emoji_chars, output_path):
    """Fallback: generate image with emoji characters as text."""

    img = Image.new('RGB', (SIZE, SIZE), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Try any available font
    fallback_fonts = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
    ]

    text_font = None
    for font_path in fallback_fonts:
        if os.path.exists(font_path):
            try:
                text_font = ImageFont.truetype(font_path, 80)
                break
            except:
                continue

    if not text_font:
        text_font = ImageFont.load_default()

    emoji_text = "  ".join(emoji_chars)

    try:
        bbox = draw.textbbox((0, 0), emoji_text, font=text_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except:
        text_width = len(emoji_text) * 60
        text_height = 80

    x = (SIZE - text_width) // 2
    y = (SIZE - text_height) // 2

    draw.text((x, y), emoji_text, font=text_font, fill='#000000')
    img.save(output_path, 'PNG')

    return True

def main():
    print("[info] Loading emoji data...")
    data = load_emoji_data()

    emojis = data.get('emojis', [])
    emoji_chars = [e.get('char', '?') for e in emojis]
    print(f"[info] Emojis: {' '.join(emoji_chars)}")
    print(f"[info] Platform: {sys.platform}")

    # Prepare output path
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Use timestamp if available, otherwise date
    timestamp = data.get('timestamp', '')
    if timestamp:
        # Convert timestamp to filename-safe format: 2025-11-22T08:00:00Z -> 2025-11-22-0800
        filename_base = timestamp.replace(':', '').replace('T', '-').replace('Z', '')[:15]
    else:
        filename_base = data.get('date', date.today().isoformat())

    output_path = os.path.join(OUTPUT_DIR, f"{filename_base}.png")

    print("[info] Generating image...")

    # Try different rendering methods
    success = False

    # Method 1: Swift (macOS only)
    if sys.platform == 'darwin':
        print("[info] Trying Swift/AppKit rendering...")
        success = generate_with_swift(emoji_chars, output_path)
        if success:
            print("[success] Generated with Swift/AppKit")

    # Method 2: Pillow with Noto Color Emoji (Linux)
    if not success and sys.platform == 'linux':
        print("[info] Trying Pillow with Noto Color Emoji...")
        success = generate_with_pillow_noto(emoji_chars, output_path)
        if success:
            print("[success] Generated with Pillow/Noto")

    # Method 3: ImageMagick with Pango (Linux)
    if not success:
        print("[info] Trying ImageMagick/Pango rendering...")
        success = generate_with_pango(emoji_chars, output_path)
        if success:
            print("[success] Generated with ImageMagick/Pango")

    # Method 4: Fallback
    if not success:
        print("[warn] Using fallback rendering (emojis may appear as boxes)")
        success = generate_fallback(emoji_chars, output_path)
        if success:
            print("[success] Generated with fallback")

    if success and os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"[success] Image saved: {output_path} ({file_size} bytes)")
        print(f"OUTPUT_PATH={output_path}")
        return 0
    else:
        print("[error] Failed to generate image", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
