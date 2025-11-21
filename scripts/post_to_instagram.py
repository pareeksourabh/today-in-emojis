#!/usr/bin/env python3
"""
Post the daily emoji image to Instagram.

Uses the Instagram Graph API to publish images.
Requires the image to be publicly accessible via URL.

Environment variables:
- INSTAGRAM_ACCESS_TOKEN: Page access token with instagram_content_publish permission
- INSTAGRAM_BUSINESS_ACCOUNT_ID: Instagram business account ID
"""

import os
import sys
import json
import time
import requests
from datetime import date

# Configuration
INPUT_FILE = "public/data/today.json"
IMAGE_DIR = "public/images/daily"
GRAPH_API_VERSION = "v18.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

# For GitHub Pages hosting
GITHUB_PAGES_BASE = "https://todayinemojis.com"

def get_env_vars():
    """Get required environment variables."""
    access_token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
    account_id = os.environ.get('INSTAGRAM_BUSINESS_ACCOUNT_ID')

    if not access_token:
        print("[error] INSTAGRAM_ACCESS_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    if not account_id:
        print("[error] INSTAGRAM_BUSINESS_ACCOUNT_ID not set", file=sys.stderr)
        sys.exit(1)

    return access_token, account_id

def load_emoji_data():
    """Load today's emoji data for caption generation."""
    if not os.path.exists(INPUT_FILE):
        print(f"[error] Input file not found: {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_image_url(data):
    """Get the public URL for today's image."""
    img_date = data.get('date', date.today().isoformat())

    # The image will be hosted on GitHub Pages after commit
    image_url = f"{GITHUB_PAGES_BASE}/images/daily/{img_date}.png"

    return image_url

def generate_caption(data):
    """Generate Instagram caption from emoji data."""
    emojis = data.get('emojis', [])

    # Get emoji characters and labels
    emoji_chars = ' '.join([e.get('char', '') for e in emojis])
    labels = [e.get('label', '') for e in emojis]

    # Build caption
    caption_parts = [
        f"Today's vibe {emoji_chars}",
        "",
        "Feel the day. Don't read it.",
        "",
    ]

    # Add labels
    for i, label in enumerate(labels, 1):
        if label:
            caption_parts.append(f"{i}. {label}")

    caption_parts.extend([
        "",
        "#TodayInEmojis #DailyVibes #NewsInEmojis #Minimalism #FiveEmojis #WorldNews #DailyMood",
        "",
        "todayinemojis.com"
    ])

    return '\n'.join(caption_parts)

def create_media_container(account_id, access_token, image_url, caption):
    """Create a media container for the image."""
    url = f"{GRAPH_API_BASE}/{account_id}/media"

    params = {
        'image_url': image_url,
        'caption': caption,
        'access_token': access_token
    }

    print(f"[info] Creating media container...")
    print(f"[info] Image URL: {image_url}")

    response = requests.post(url, params=params)

    if response.status_code != 200:
        print(f"[error] Failed to create media container: {response.status_code}", file=sys.stderr)
        print(f"[error] Response: {response.text}", file=sys.stderr)
        return None

    data = response.json()
    container_id = data.get('id')

    if not container_id:
        print(f"[error] No container ID in response: {data}", file=sys.stderr)
        return None

    print(f"[success] Media container created: {container_id}")
    return container_id

def check_container_status(account_id, access_token, container_id):
    """Check if the media container is ready for publishing."""
    url = f"{GRAPH_API_BASE}/{container_id}"

    params = {
        'fields': 'status_code',
        'access_token': access_token
    }

    max_attempts = 10
    for attempt in range(max_attempts):
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"[warn] Status check failed: {response.status_code}", file=sys.stderr)
            time.sleep(5)
            continue

        data = response.json()
        status = data.get('status_code')

        if status == 'FINISHED':
            print(f"[success] Container ready for publishing")
            return True
        elif status == 'ERROR':
            print(f"[error] Container processing failed: {data}", file=sys.stderr)
            return False
        elif status == 'IN_PROGRESS':
            print(f"[info] Container processing... (attempt {attempt + 1}/{max_attempts})")
            time.sleep(5)
        else:
            print(f"[info] Container status: {status}")
            time.sleep(3)

    print(f"[error] Container processing timed out", file=sys.stderr)
    return False

def publish_media(account_id, access_token, container_id):
    """Publish the media container to Instagram."""
    url = f"{GRAPH_API_BASE}/{account_id}/media_publish"

    params = {
        'creation_id': container_id,
        'access_token': access_token
    }

    print(f"[info] Publishing to Instagram...")

    response = requests.post(url, params=params)

    if response.status_code != 200:
        print(f"[error] Failed to publish: {response.status_code}", file=sys.stderr)
        print(f"[error] Response: {response.text}", file=sys.stderr)
        return None

    data = response.json()
    media_id = data.get('id')

    if not media_id:
        print(f"[error] No media ID in response: {data}", file=sys.stderr)
        return None

    print(f"[success] Published to Instagram! Media ID: {media_id}")
    return media_id

def main():
    print("[info] Starting Instagram post...")

    # Get credentials
    access_token, account_id = get_env_vars()

    # Load emoji data
    data = load_emoji_data()
    print(f"[info] Posting emojis for {data.get('date', 'unknown date')}")

    # Get image URL
    image_url = get_image_url(data)

    # Generate caption
    caption = generate_caption(data)
    print(f"[info] Caption generated ({len(caption)} chars)")

    # Create media container
    container_id = create_media_container(account_id, access_token, image_url, caption)
    if not container_id:
        print("[error] Failed to create media container", file=sys.stderr)
        sys.exit(1)

    # Wait for container to be ready
    if not check_container_status(account_id, access_token, container_id):
        print("[error] Container not ready for publishing", file=sys.stderr)
        sys.exit(1)

    # Publish
    media_id = publish_media(account_id, access_token, container_id)
    if not media_id:
        print("[error] Failed to publish to Instagram", file=sys.stderr)
        sys.exit(1)

    print(f"\n[done] Successfully posted to Instagram!")
    print(f"[info] View at: https://instagram.com/todayinemojis")

    return 0

if __name__ == "__main__":
    sys.exit(main())
