#!/usr/bin/env python3
"""
Generate a daily emoji image for Instagram posting.

Design:
- 1080x1080px square canvas
- Warm neutral background
- Centered white card with rounded corners and border
- Date in top-left of card
- 5 emojis centered on card
- No text besides date

Usage:
  python scripts/generate_emoji_image.py           # Use today.json
  python scripts/generate_emoji_image.py --test    # Generate test image

Output: public/images/daily/YYYY-MM-DD-HHMM.png
"""

import os
import sys
import json
import subprocess
import tempfile
import argparse
from datetime import date, datetime

# Configuration
INPUT_FILE = "public/data/today.json"
OUTPUT_DIR = "public/images/daily"
SIZE = 1080

# Design constants
BG_COLOR = (245, 243, 238)      # Outer background (#F5F3EE)
CARD_COLOR = (255, 255, 255)    # Inner card (white)
BORDER_COLOR = (220, 216, 208)  # Subtle border
TEXT_COLOR = (60, 60, 60)       # Date text color

PADDING_OUTER = 80              # Margin from canvas edge to card
CARD_RADIUS = 60                # Rounded corners
CARD_BORDER_WIDTH = 2           # Border thickness

# Font config
DATE_FONT_SIZE = 40
EMOJI_FONT_SIZE = 108  # 60% of 180


def load_emoji_data():
    """Load today's emoji data from JSON file."""
    if not os.path.exists(INPUT_FILE):
        print(f"[error] Input file not found: {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data


def get_test_data():
    """Generate test data for local testing."""
    return {
        "date": date.today().isoformat(),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "emojis": [
            {"char": "🌍", "label": "world"},
            {"char": "💡", "label": "idea"},
            {"char": "🚀", "label": "launch"},
            {"char": "🎯", "label": "target"},
            {"char": "✨", "label": "sparkle"},
        ],
        "source": "test",
    }


def format_date(date_str):
    """Format date as '22 Nov 2025'."""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.strftime("%-d %b %Y")
    except:
        return date_str


def generate_with_swift(emoji_chars, date_str, output_path):
    """Generate image using Swift/AppKit - native macOS rendering."""

    emoji_text = " ".join(emoji_chars)
    formatted_date = format_date(date_str)

    # Card dimensions
    card_x = PADDING_OUTER
    card_y = PADDING_OUTER
    card_w = SIZE - 2 * PADDING_OUTER
    card_h = SIZE - 2 * PADDING_OUTER

    # Convert RGB tuples to normalized values
    bg_r, bg_g, bg_b = BG_COLOR[0]/255, BG_COLOR[1]/255, BG_COLOR[2]/255
    border_r, border_g, border_b = BORDER_COLOR[0]/255, BORDER_COLOR[1]/255, BORDER_COLOR[2]/255
    text_r, text_g, text_b = TEXT_COLOR[0]/255, TEXT_COLOR[1]/255, TEXT_COLOR[2]/255

    swift_code = f'''
import Cocoa

let size = NSSize(width: {SIZE}, height: {SIZE})
let image = NSImage(size: size)

image.lockFocus()

// Background
NSColor(calibratedRed: {bg_r}, green: {bg_g}, blue: {bg_b}, alpha: 1.0).setFill()
NSRect(origin: .zero, size: size).fill()

// Card with rounded corners
let cardRect = NSRect(x: {card_x}, y: {card_y}, width: {card_w}, height: {card_h})
let cardPath = NSBezierPath(roundedRect: cardRect, xRadius: {CARD_RADIUS}, yRadius: {CARD_RADIUS})

// Card fill first (so border draws on top)
NSColor.white.setFill()
cardPath.fill()

// Card border
NSColor(calibratedRed: {border_r}, green: {border_g}, blue: {border_b}, alpha: 1.0).setStroke()
cardPath.lineWidth = {CARD_BORDER_WIDTH}
cardPath.stroke()

// Date text (top-left of card)
let dateText = "{formatted_date}"
let dateFont = NSFont.systemFont(ofSize: {DATE_FONT_SIZE}, weight: .regular)
let dateAttributes: [NSAttributedString.Key: Any] = [
    .font: dateFont,
    .foregroundColor: NSColor(calibratedRed: {text_r}, green: {text_g}, blue: {text_b}, alpha: 1.0)
]
let datePoint = NSPoint(x: {card_x + 40}, y: {SIZE - card_y - 70})
dateText.draw(at: datePoint, withAttributes: dateAttributes)

// Emojis (centered on card)
let emojiText = "{emoji_text}"
let emojiFont = NSFont.systemFont(ofSize: {EMOJI_FONT_SIZE})
let emojiAttributes: [NSAttributedString.Key: Any] = [
    .font: emojiFont
]

let emojiSize = emojiText.size(withAttributes: emojiAttributes)
let emojiX = ({SIZE} - emojiSize.width) / 2
let emojiY = ({SIZE} - emojiSize.height) / 2

emojiText.draw(at: NSPoint(x: emojiX, y: emojiY), withAttributes: emojiAttributes)

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
        with tempfile.NamedTemporaryFile(mode='w', suffix='.swift', delete=False) as f:
            f.write(swift_code)
            swift_path = f.name

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


def generate_with_pillow(emoji_chars, date_str, output_path):
    """Generate image using Pillow with Noto Color Emoji (Linux)."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new('RGB', (SIZE, SIZE), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Card dimensions
    card_x = PADDING_OUTER
    card_y = PADDING_OUTER
    card_w = SIZE - 2 * PADDING_OUTER
    card_h = SIZE - 2 * PADDING_OUTER

    # Draw card with rounded corners
    card_rect = [card_x, card_y, card_x + card_w, card_y + card_h]

    # Draw card
    draw.rounded_rectangle(card_rect, radius=CARD_RADIUS,
                          fill=CARD_COLOR, outline=BORDER_COLOR,
                          width=CARD_BORDER_WIDTH)

    # Find emoji fonts
    noto_fonts = [
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
        "/usr/share/fonts/noto-emoji/NotoColorEmoji.ttf",
        "/usr/share/fonts/google-noto-emoji/NotoColorEmoji.ttf",
    ]

    emoji_font = None
    for font_path in noto_fonts:
        if os.path.exists(font_path):
            try:
                emoji_font = ImageFont.truetype(font_path, EMOJI_FONT_SIZE)
                break
            except:
                continue

    # Find text fonts
    text_fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
    ]

    text_font = None
    for font_path in text_fonts:
        if os.path.exists(font_path):
            try:
                text_font = ImageFont.truetype(font_path, DATE_FONT_SIZE)
                break
            except:
                continue

    if not text_font:
        text_font = ImageFont.load_default()

    # Draw date
    formatted_date = format_date(date_str)
    draw.text((card_x + 40, card_y + 30), formatted_date,
              font=text_font, fill=TEXT_COLOR)

    # Draw emojis
    emoji_text = " ".join(emoji_chars)

    if emoji_font:
        try:
            bbox = draw.textbbox((0, 0), emoji_text, font=emoji_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (SIZE - text_width) // 2
            y = (SIZE - text_height) // 2
            draw.text((x, y), emoji_text, font=emoji_font, embedded_color=True)
        except Exception as e:
            print(f"[warn] Emoji drawing error: {e}", file=sys.stderr)
            # Fallback to text
            draw.text((SIZE//2, SIZE//2), emoji_text, font=text_font,
                     fill=TEXT_COLOR, anchor='mm')
    else:
        # No emoji font, just draw as text
        if text_font:
            draw.text((SIZE//2, SIZE//2), emoji_text, font=text_font,
                     fill=TEXT_COLOR, anchor='mm')

    img.save(output_path, 'PNG')
    return True


def main():
    parser = argparse.ArgumentParser(description='Generate emoji image for Instagram')
    parser.add_argument('--test', action='store_true',
                       help='Generate test image with sample data')
    parser.add_argument('--output', type=str,
                       help='Custom output path')
    args = parser.parse_args()

    # Load data
    if args.test:
        print("[info] Using test data...")
        data = get_test_data()
    else:
        print("[info] Loading emoji data...")
        data = load_emoji_data()

    emojis = data.get('emojis', [])
    emoji_chars = [e.get('char', '?') for e in emojis]
    date_str = data.get('date', date.today().isoformat())

    print(f"[info] Emojis: {' '.join(emoji_chars)}")
    print(f"[info] Date: {date_str}")
    print(f"[info] Platform: {sys.platform}")

    # Prepare output path
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if args.output:
        output_path = args.output
    elif args.test:
        output_path = os.path.join(OUTPUT_DIR, "test.png")
    else:
        timestamp = data.get('timestamp', '')
        if timestamp:
            filename_base = timestamp.replace(':', '').replace('T', '-').replace('Z', '')[:15]
        else:
            filename_base = date_str
        output_path = os.path.join(OUTPUT_DIR, f"{filename_base}.png")

    print(f"[info] Output: {output_path}")
    print("[info] Generating image...")

    # Try rendering methods
    success = False

    # Method 1: Swift (macOS)
    if sys.platform == 'darwin':
        print("[info] Trying Swift/AppKit rendering...")
        success = generate_with_swift(emoji_chars, date_str, output_path)
        if success:
            print("[success] Generated with Swift/AppKit")

    # Method 2: Pillow (Linux)
    if not success:
        print("[info] Trying Pillow rendering...")
        success = generate_with_pillow(emoji_chars, date_str, output_path)
        if success:
            print("[success] Generated with Pillow")

    if success and os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"[success] Image saved: {output_path} ({file_size} bytes)")

        # Open image on macOS for quick preview
        if args.test and sys.platform == 'darwin':
            subprocess.run(['open', output_path])

        print(f"OUTPUT_PATH={output_path}")
        return 0
    else:
        print("[error] Failed to generate image", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
