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
EMOJI_GAP = 20

# Essence design constants
ESSENCE_BG_COLOR = (242, 241, 236)
ESSENCE_TEXT_COLOR = (70, 70, 70)
ESSENCE_EMOJI_FONT_SIZE = 320
ESSENCE_DATE_FONT_SIZE = 36
ESSENCE_DATE_TOP_PADDING = 70

# Detail image design constants (for carousel detail slides)
DETAIL_BG_COLOR = (255, 255, 255)      # Pure white background
DETAIL_TEXT_COLOR = (40, 40, 40)       # Dark text for contrast
DETAIL_EMOJI_SIZE = 240                # Large emoji for single display
DETAIL_LABEL_SIZE = 36                 # Refined label text size
DETAIL_PADDING = 120                   # Generous padding from edges


def load_emoji_data(path=INPUT_FILE):
    """Load today's emoji data from JSON file."""
    if not os.path.exists(path):
        print(f"[error] Input file not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
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
let emojiText = "{emoji_text}"
let emojiFont = NSFont.systemFont(ofSize: {EMOJI_FONT_SIZE})
let emojiAttributes: [NSAttributedString.Key: Any] = [
    .font: emojiFont
]

let emojiSize = emojiText.size(withAttributes: emojiAttributes)
let emojiX = ({SIZE} - emojiSize.width) / 2
let emojiY = ({SIZE} - emojiSize.height) / 2

let dateAttributes: [NSAttributedString.Key: Any] = [
    .font: dateFont,
    .foregroundColor: NSColor(calibratedRed: {text_r}, green: {text_g}, blue: {text_b}, alpha: 1.0)
]
let datePoint = NSPoint(x: emojiX, y: {SIZE - card_y - 70})
dateText.draw(at: datePoint, withAttributes: dateAttributes)

// Emojis (centered on card)

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


def generate_essence_with_swift(emoji_char, date_str, output_path):
    """Generate essence image using Swift/AppKit - native macOS rendering."""

    formatted_date = format_date(date_str)

    bg_r, bg_g, bg_b = ESSENCE_BG_COLOR[0]/255, ESSENCE_BG_COLOR[1]/255, ESSENCE_BG_COLOR[2]/255
    text_r, text_g, text_b = ESSENCE_TEXT_COLOR[0]/255, ESSENCE_TEXT_COLOR[1]/255, ESSENCE_TEXT_COLOR[2]/255

    swift_code = f'''
import Cocoa

let size = NSSize(width: {SIZE}, height: {SIZE})
let image = NSImage(size: size)

image.lockFocus()

NSColor(calibratedRed: {bg_r}, green: {bg_g}, blue: {bg_b}, alpha: 1.0).setFill()
NSRect(origin: .zero, size: size).fill()

let emojiText = "{emoji_char}"
let emojiFont = NSFont.systemFont(ofSize: {ESSENCE_EMOJI_FONT_SIZE})
let emojiAttributes: [NSAttributedString.Key: Any] = [
    .font: emojiFont
]
let emojiSize = emojiText.size(withAttributes: emojiAttributes)
let emojiX = ({SIZE} - emojiSize.width) / 2
let emojiY = ({SIZE} - emojiSize.height) / 2
emojiText.draw(at: NSPoint(x: emojiX, y: emojiY), withAttributes: emojiAttributes)

let dateText = "{formatted_date}"
let dateFont = NSFont.systemFont(ofSize: {ESSENCE_DATE_FONT_SIZE}, weight: .regular)
let dateAttributes: [NSAttributedString.Key: Any] = [
    .font: dateFont,
    .foregroundColor: NSColor(calibratedRed: {text_r}, green: {text_g}, blue: {text_b}, alpha: 1.0)
]
let dateSize = dateText.size(withAttributes: dateAttributes)
let dateX = ({SIZE} - dateSize.width) / 2
let dateY = {SIZE} - CGFloat({ESSENCE_DATE_TOP_PADDING}) - dateSize.height
dateText.draw(at: NSPoint(x: dateX, y: dateY), withAttributes: dateAttributes)

image.unlockFocus()

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


def generate_detail_with_swift(emoji_char, label_text, date_str, output_path):
    """Generate detail image (single emoji + label) using Swift/AppKit."""

    # Capitalize label
    label_text = label_text.strip()
    if label_text:
        label_text = label_text[0].upper() + label_text[1:]

    # Convert RGB tuples to normalized values
    bg_r, bg_g, bg_b = DETAIL_BG_COLOR[0]/255, DETAIL_BG_COLOR[1]/255, DETAIL_BG_COLOR[2]/255
    text_r, text_g, text_b = DETAIL_TEXT_COLOR[0]/255, DETAIL_TEXT_COLOR[1]/255, DETAIL_TEXT_COLOR[2]/255

    swift_code = f'''
import Cocoa

let size = NSSize(width: {SIZE}, height: {SIZE})
let image = NSImage(size: size)

image.lockFocus()

// Pure white background
NSColor(calibratedRed: {bg_r}, green: {bg_g}, blue: {bg_b}, alpha: 1.0).setFill()
NSRect(origin: .zero, size: size).fill()

// Emoji (centered, slightly above middle)
let emojiText = "{emoji_char}"
let emojiFont = NSFont.systemFont(ofSize: {DETAIL_EMOJI_SIZE})
let emojiAttributes: [NSAttributedString.Key: Any] = [
    .font: emojiFont
]
let emojiSize = emojiText.size(withAttributes: emojiAttributes)
let emojiX = ({SIZE} - emojiSize.width) / 2
let emojiY = ({SIZE} - emojiSize.height) / 2 + 50
emojiText.draw(at: NSPoint(x: emojiX, y: emojiY), withAttributes: emojiAttributes)

// Label (below emoji, refined typography)
let labelText = "{label_text}"
let labelFont = NSFont.systemFont(ofSize: {DETAIL_LABEL_SIZE}, weight: .medium)
let labelAttributes: [NSAttributedString.Key: Any] = [
    .font: labelFont,
    .foregroundColor: NSColor(calibratedRed: {text_r}, green: {text_g}, blue: {text_b}, alpha: 1.0)
]
let labelSize = labelText.size(withAttributes: labelAttributes)
let labelX = ({SIZE} - labelSize.width) / 2
let labelY = emojiY - 100
labelText.draw(at: NSPoint(x: labelX, y: labelY), withAttributes: labelAttributes)

image.unlockFocus()

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


def generate_with_pango_cairo(emoji_chars, date_str, output_path):
    """Generate image using Pango/Cairo for proper emoji support on Linux."""

    emoji_text = " ".join(emoji_chars)
    formatted_date = format_date(date_str)

    # Card dimensions
    card_x = PADDING_OUTER
    card_y = PADDING_OUTER
    card_w = SIZE - 2 * PADDING_OUTER
    card_h = SIZE - 2 * PADDING_OUTER
    date_left = compute_date_left(len(emoji_chars))

    # Convert colors to hex
    bg_hex = '#{:02x}{:02x}{:02x}'.format(*BG_COLOR)
    card_hex = '#{:02x}{:02x}{:02x}'.format(*CARD_COLOR)
    border_hex = '#{:02x}{:02x}{:02x}'.format(*BORDER_COLOR)
    text_hex = '#{:02x}{:02x}{:02x}'.format(*TEXT_COLOR)

    try:
        # Check if convert (ImageMagick) is available
        result = subprocess.run(['which', 'convert'], capture_output=True, text=True)
        if result.returncode != 0:
            print("[info] ImageMagick not available", file=sys.stderr)
            return False

        # Build ImageMagick command with Pango
        cmd = [
            'convert',
            '-size', f'{SIZE}x{SIZE}',
            f'xc:{bg_hex}',
            # Draw rounded rectangle for card
            '-fill', card_hex,
            '-stroke', border_hex,
            '-strokewidth', str(CARD_BORDER_WIDTH),
            '-draw', f'roundrectangle {card_x},{card_y} {card_x+card_w},{card_y+card_h} {CARD_RADIUS},{CARD_RADIUS}',
            # Draw date text
            '-font', 'DejaVu-Sans',
            '-pointsize', str(DATE_FONT_SIZE),
            '-fill', text_hex,
            '-annotate', f'+{date_left}+{card_y+50}', formatted_date,
            # Draw emojis using pango for color emoji support
            '-gravity', 'center',
            '-font', 'Noto-Color-Emoji',
            '-pointsize', str(EMOJI_FONT_SIZE),
            f'pango:<span font="{EMOJI_FONT_SIZE}">{emoji_text}</span>',
            output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0 and os.path.exists(output_path):
            return True
        else:
            if result.stderr:
                print(f"[info] ImageMagick/Pango error: {result.stderr}", file=sys.stderr)
            return False

    except Exception as e:
        print(f"[info] Pango/Cairo rendering failed: {e}", file=sys.stderr)
        return False


def generate_essence_with_pango_cairo(emoji_char, date_str, output_path):
    """Generate essence image using Pango/Cairo for proper emoji support on Linux."""

    formatted_date = format_date(date_str)

    bg_hex = '#{:02x}{:02x}{:02x}'.format(*ESSENCE_BG_COLOR)
    text_hex = '#{:02x}{:02x}{:02x}'.format(*ESSENCE_TEXT_COLOR)

    try:
        result = subprocess.run(['which', 'convert'], capture_output=True, text=True)
        if result.returncode != 0:
            print("[info] ImageMagick not available", file=sys.stderr)
            return False

        cmd = [
            'convert',
            '-size', f'{SIZE}x{SIZE}',
            f'xc:{bg_hex}',
            '-gravity', 'center',
            '-font', 'Noto-Color-Emoji',
            '-pointsize', str(ESSENCE_EMOJI_FONT_SIZE),
            f'pango:<span font="{ESSENCE_EMOJI_FONT_SIZE}">{emoji_char}</span>',
            '-font', 'DejaVu-Sans',
            '-pointsize', str(ESSENCE_DATE_FONT_SIZE),
            '-fill', text_hex,
            '-gravity', 'north',
            '-annotate', f'+0+{ESSENCE_DATE_TOP_PADDING}', formatted_date,
            output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and os.path.exists(output_path):
            return True
        else:
            if result.stderr:
                print(f"[info] ImageMagick/Pango error: {result.stderr}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"[info] Pango/Cairo rendering failed: {e}", file=sys.stderr)
        return False


def compute_date_left(num_emojis):
    """Estimate the left edge of the emoji row so the date aligns with column one."""
    if num_emojis <= 0:
        return PADDING_OUTER

    row_width = (num_emojis * EMOJI_FONT_SIZE) + (max(num_emojis - 1, 0) * EMOJI_GAP)
    estimated_left = int(round((SIZE - row_width) / 2))
    return max(PADDING_OUTER, estimated_left)


def generate_with_playwright(emoji_chars, date_str, output_path):
    """Generate image using Playwright for reliable headless browser rendering."""

    emoji_text = " ".join(emoji_chars)
    formatted_date = format_date(date_str)
    card_x = PADDING_OUTER
    card_y = PADDING_OUTER
    date_left_in_card = compute_date_left(len(emoji_chars)) - card_x
    date_left_in_card = max(0, date_left_in_card)

    # Convert colors to hex
    bg_hex = '#{:02x}{:02x}{:02x}'.format(*BG_COLOR)
    card_hex = '#{:02x}{:02x}{:02x}'.format(*CARD_COLOR)
    border_hex = '#{:02x}{:02x}{:02x}'.format(*BORDER_COLOR)
    text_hex = '#{:02x}{:02x}{:02x}'.format(*TEXT_COLOR)

    # Wrap each emoji in a span
    emoji_spans = ''.join([f'<span class="emoji">{e}</span>' for e in emoji_chars])

    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            width: {SIZE}px;
            height: {SIZE}px;
            overflow: hidden;
        }}
        body {{
            background: {bg_hex};
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}
        .card {{
            width: {SIZE - 2*PADDING_OUTER}px;
            height: {SIZE - 2*PADDING_OUTER}px;
            background: {card_hex};
            border: {CARD_BORDER_WIDTH}px solid {border_hex};
            border-radius: {CARD_RADIUS}px;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .date {{
            position: absolute;
            top: 30px;
            left: {date_left_in_card}px;
            font-size: {DATE_FONT_SIZE}px;
            color: {text_hex};
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}
        .emojis {{
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            align-items: center;
            justify-content: center;
            gap: {EMOJI_GAP}px;
        }}
        .emoji {{
            font-size: {EMOJI_FONT_SIZE}px;
            line-height: 1;
            display: inline-block;
            vertical-align: middle;
            font-family: 'Noto Color Emoji', 'Apple Color Emoji', 'Segoe UI Emoji', sans-serif;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="date">{formatted_date}</div>
        <div class="emojis">{emoji_spans}</div>
    </div>
</body>
<script>
    const card = document.querySelector('.card');
    const date = document.querySelector('.date');
    const emojis = document.querySelector('.emojis');
    if (card && date && emojis) {{
        const cardRect = card.getBoundingClientRect();
        const emojiRect = emojis.getBoundingClientRect();
        const relativeLeft = emojiRect.left - cardRect.left;
        date.style.left = `${{relativeLeft}}px`;
    }}
</script>
</html>'''

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': SIZE, 'height': SIZE})
            page.set_content(html_content)
            page.wait_for_timeout(100)
            page.screenshot(path=output_path, full_page=False)
            browser.close()

        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            return True
        return False

    except ImportError:
        print("[info] Playwright not installed", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[info] Playwright rendering failed: {e}", file=sys.stderr)
        return False


def generate_essence_with_playwright(emoji_char, date_str, output_path):
    """Generate essence image using Playwright for reliable headless browser rendering."""

    formatted_date = format_date(date_str)

    bg_hex = '#{:02x}{:02x}{:02x}'.format(*ESSENCE_BG_COLOR)
    text_hex = '#{:02x}{:02x}{:02x}'.format(*ESSENCE_TEXT_COLOR)

    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            width: {SIZE}px;
            height: {SIZE}px;
            overflow: hidden;
        }}
        body {{
            background: {bg_hex};
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            position: relative;
        }}
        .emoji {{
            font-size: {ESSENCE_EMOJI_FONT_SIZE}px;
            line-height: 1;
            font-family: 'Noto Color Emoji', 'Apple Color Emoji', 'Segoe UI Emoji', sans-serif;
        }}
        .date {{
            position: absolute;
            top: {ESSENCE_DATE_TOP_PADDING}px;
            left: 50%;
            transform: translateX(-50%);
            font-size: {ESSENCE_DATE_FONT_SIZE}px;
            color: {text_hex};
        }}
    </style>
</head>
<body>
    <div class="emoji">{emoji_char}</div>
    <div class="date">{formatted_date}</div>
</body>
</html>'''

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': SIZE, 'height': SIZE})
            page.set_content(html_content)
            page.wait_for_timeout(100)
            page.screenshot(path=output_path, full_page=False)
            browser.close()

        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            return True
        return False

    except ImportError:
        print("[info] Playwright not installed", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[info] Playwright rendering failed: {e}", file=sys.stderr)
        return False


def generate_detail_with_playwright(emoji_char, label_text, date_str, output_path):
    """Generate detail image (single emoji + label) using Playwright."""

    # Capitalize label
    label_text = label_text.strip()
    if label_text:
        label_text = label_text[0].upper() + label_text[1:]

    bg_hex = '#{:02x}{:02x}{:02x}'.format(*DETAIL_BG_COLOR)
    text_hex = '#{:02x}{:02x}{:02x}'.format(*DETAIL_TEXT_COLOR)

    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            width: {SIZE}px;
            height: {SIZE}px;
            overflow: hidden;
        }}
        body {{
            background: {bg_hex};
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
            padding: {DETAIL_PADDING}px;
        }}
        .emoji {{
            font-size: {DETAIL_EMOJI_SIZE}px;
            line-height: 1;
            font-family: 'Noto Color Emoji', 'Apple Color Emoji', 'Segoe UI Emoji', sans-serif;
            margin-bottom: 40px;
        }}
        .label {{
            font-size: {DETAIL_LABEL_SIZE}px;
            font-weight: 500;
            color: {text_hex};
            letter-spacing: 0.3px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="emoji">{emoji_char}</div>
    <div class="label">{label_text}</div>
</body>
</html>'''

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': SIZE, 'height': SIZE})
            page.set_content(html_content)
            page.wait_for_timeout(100)
            page.screenshot(path=output_path, full_page=False)
            browser.close()

        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            return True
        return False

    except ImportError:
        print("[info] Playwright not installed", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[info] Playwright rendering failed: {e}", file=sys.stderr)
        return False


def generate_with_pillow(emoji_chars, date_str, output_path):
    """Generate image using Pillow - fallback with limited emoji support."""
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

    emoji_text = " ".join(emoji_chars)
    formatted_date = format_date(date_str)
    emoji_x = compute_date_left(len(emoji_chars))

    try:
        emoji_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", EMOJI_FONT_SIZE)
        bbox = draw.textbbox((0, 0), emoji_text, font=emoji_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        emoji_x = (SIZE - text_width) // 2
        emoji_y = (SIZE - text_height) // 2
        draw.text((emoji_x, emoji_y), emoji_text, font=emoji_font, embedded_color=True)
    except Exception as e:
        print(f"[warn] Emoji font failed: {e}", file=sys.stderr)
        # Just draw text centered
        emoji_y = SIZE // 2
        draw.text((SIZE//2, SIZE//2), emoji_text, font=text_font,
                 fill=TEXT_COLOR, anchor='mm')

    # Draw date after computing emoji start so it aligns to the first emoji column
    draw.text((emoji_x, card_y + 30), formatted_date,
              font=text_font, fill=TEXT_COLOR)

    img.save(output_path, 'PNG')
    return True


def generate_essence_with_pillow(emoji_char, date_str, output_path):
    """Generate essence image using Pillow - fallback with limited emoji support."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new('RGB', (SIZE, SIZE), color=ESSENCE_BG_COLOR)
    draw = ImageDraw.Draw(img)

    text_fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
    ]

    text_font = None
    for font_path in text_fonts:
        if os.path.exists(font_path):
            try:
                text_font = ImageFont.truetype(font_path, ESSENCE_DATE_FONT_SIZE)
                break
            except:
                continue

    if not text_font:
        text_font = ImageFont.load_default()

    formatted_date = format_date(date_str)

    try:
        emoji_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", ESSENCE_EMOJI_FONT_SIZE)
        bbox = draw.textbbox((0, 0), emoji_char, font=emoji_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        emoji_x = (SIZE - text_width) // 2
        emoji_y = (SIZE - text_height) // 2
        draw.text((emoji_x, emoji_y), emoji_char, font=emoji_font, embedded_color=True)
    except Exception as e:
        print(f"[warn] Emoji font failed: {e}", file=sys.stderr)
        draw.text((SIZE//2, SIZE//2), emoji_char, font=text_font,
                 fill=ESSENCE_TEXT_COLOR, anchor='mm')

    date_bbox = draw.textbbox((0, 0), formatted_date, font=text_font)
    date_w = date_bbox[2] - date_bbox[0]
    date_x = (SIZE - date_w) // 2
    date_y = ESSENCE_DATE_TOP_PADDING
    draw.text((date_x, date_y), formatted_date, font=text_font, fill=ESSENCE_TEXT_COLOR)

    img.save(output_path, 'PNG')
    return True


def generate_detail_image(emoji_char, label_text, date_str, output_path):
    """
    Generate a detail image (single emoji + label) using available rendering method.
    Returns True on success, False on failure.
    """
    success = False

    # Method 1: Swift (macOS)
    if sys.platform == 'darwin':
        success = generate_detail_with_swift(emoji_char, label_text, date_str, output_path)
        if success:
            return True

    # Method 2: Playwright (best cross-platform)
    if not success:
        success = generate_detail_with_playwright(emoji_char, label_text, date_str, output_path)
        if success:
            return True

    # Method 3: Pillow fallback
    # For simplicity, reuse essence rendering as fallback for detail images
    # (shows just emoji without label, but ensures we have something)
    if not success:
        print(f"[warn] Using simplified fallback for detail image", file=sys.stderr)
        success = generate_essence_with_pillow(emoji_char, date_str, output_path)

    return success


def main():
    parser = argparse.ArgumentParser(description='Generate emoji image for Instagram')
    parser.add_argument('--test', action='store_true',
                       help='Generate test image with sample data')
    parser.add_argument('--input', type=str,
                       help='Custom input JSON path')
    parser.add_argument('--output', type=str,
                       help='Custom output path')
    parser.add_argument('--carousel', action='store_true',
                       help='Generate carousel images (summary + 5 detail images)')
    args = parser.parse_args()

    # Load data
    if args.test:
        print("[info] Using test data...")
        data = get_test_data()
    else:
        print("[info] Loading emoji data...")
        data = load_emoji_data(args.input or INPUT_FILE)

    emojis = data.get('emojis', [])
    emoji_chars = [e.get('char', '?') for e in emojis]
    date_str = data.get('date', date.today().isoformat())
    post_type = data.get('post_type', 'normal')
    essence = data.get('essence', {}) if isinstance(data.get('essence'), dict) else {}
    essence_emoji = essence.get('emoji') or (emoji_chars[0] if emoji_chars else '?')

    print(f"[info] Date: {date_str}")
    print(f"[info] Platform: {sys.platform}")
    print(f"[info] Post type: {post_type}")

    if post_type == 'essence':
        emotion_label = essence.get('emotion_label', 'unknown')
        print(f"[info] Essence emoji: {essence_emoji}")
        print(f"[info] Essence emotion: {emotion_label}")
        print(f"[info] Source emojis analyzed: {' '.join(emoji_chars)}")
    else:
        print(f"[info] Emojis to render: {' '.join(emoji_chars)}")

    # Prepare output path
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Compute filename_base for all paths
    timestamp = data.get('timestamp', '')
    if timestamp:
        filename_base = timestamp.replace(':', '').replace('T', '-').replace('Z', '')[:15]
    else:
        filename_base = date_str

    if args.output:
        output_path = args.output
    elif args.test:
        output_path = os.path.join(OUTPUT_DIR, "test.png")
        filename_base = "test"  # Override for test mode
    else:
        output_path = os.path.join(OUTPUT_DIR, f"{filename_base}.png")

    print(f"[info] Output path: {output_path}")

    # Determine if we should generate carousel images
    generate_carousel = args.carousel or (post_type == 'normal' and not args.test)

    if post_type == 'essence':
        print("[info] Generating essence image (single large emoji)...")

        # Try rendering methods for essence
        success = False

        if sys.platform == 'darwin':
            print("[info] Trying Swift/AppKit rendering...")
            success = generate_essence_with_swift(essence_emoji, date_str, output_path)
            if success:
                print("[success] Generated with Swift/AppKit")

        if not success:
            print("[info] Trying Playwright rendering...")
            success = generate_essence_with_playwright(essence_emoji, date_str, output_path)
            if success:
                print("[success] Generated with Playwright")

        if not success:
            print("[info] Trying Pango/Cairo rendering...")
            success = generate_essence_with_pango_cairo(essence_emoji, date_str, output_path)
            if success:
                print("[success] Generated with Pango/Cairo")

        if not success:
            print("[info] Trying Pillow rendering (fallback)...")
            success = generate_essence_with_pillow(essence_emoji, date_str, output_path)
            if success:
                print("[warn] Generated with Pillow - emojis may not render correctly")

        if not success:
            print("[error] Failed to generate essence image", file=sys.stderr)
            return 1

    elif generate_carousel:
        print("[info] Generating carousel images (summary + 5 detail images)...")

        # Generate summary image (image 1)
        print("[info] Generating summary image (1/6)...")
        success = False

        if sys.platform == 'darwin':
            success = generate_with_swift(emoji_chars, date_str, output_path)
        if not success:
            success = generate_with_playwright(emoji_chars, date_str, output_path)
        if not success:
            success = generate_with_pango_cairo(emoji_chars, date_str, output_path)
        if not success:
            success = generate_with_pillow(emoji_chars, date_str, output_path)

        if not success:
            print("[error] Failed to generate summary image", file=sys.stderr)
            return 1

        print(f"[success] Summary image generated: {output_path}")

        # Generate detail images (images 2-6)
        for i, emoji in enumerate(emojis, 1):
            emoji_char = emoji.get('char', '?')
            label = emoji.get('label', '')

            # Detail image path
            detail_filename = filename_base + f"-detail-{i}.png"
            detail_path = os.path.join(OUTPUT_DIR, detail_filename)

            print(f"[info] Generating detail image {i+1}/6 ({emoji_char} - {label})...")

            detail_success = generate_detail_image(emoji_char, label, date_str, detail_path)

            if not detail_success:
                print(f"[error] Failed to generate detail image {i}", file=sys.stderr)
                return 1

            print(f"[success] Detail image {i} generated: {detail_path}")

        print(f"[success] Generated 6 carousel images for {timestamp}")

    else:
        print("[info] Generating normal image (5 emojis grid)...")

        success = False

        if sys.platform == 'darwin':
            print("[info] Trying Swift/AppKit rendering...")
            success = generate_with_swift(emoji_chars, date_str, output_path)
            if success:
                print("[success] Generated with Swift/AppKit")

        if not success:
            print("[info] Trying Playwright rendering...")
            success = generate_with_playwright(emoji_chars, date_str, output_path)
            if success:
                print("[success] Generated with Playwright")

        if not success:
            print("[info] Trying Pango/Cairo rendering...")
            success = generate_with_pango_cairo(emoji_chars, date_str, output_path)
            if success:
                print("[success] Generated with Pango/Cairo")

        if not success:
            print("[info] Trying Pillow rendering (fallback)...")
            success = generate_with_pillow(emoji_chars, date_str, output_path)
            if success:
                print("[warn] Generated with Pillow - emojis may not render correctly")

        if not success:
            print("[error] Failed to generate image", file=sys.stderr)
            return 1

    if os.path.exists(output_path):
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
