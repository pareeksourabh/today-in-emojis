#!/usr/bin/env python3
"""
Update local JSON file from Firestore edition data.

This script reads the fetched Firestore edition data and updates the local
JSON file (public/data/today.json) that is used by the website and posting pipeline.

The script maintains the same JSON format and structure as the AI-generated content,
ensuring compatibility with all downstream consumers.

Usage:
    python scripts/update_local_json_from_firestore.py
"""

import os
import sys
import json
from datetime import datetime

# File paths
FIRESTORE_DATA_FILE = "/tmp/firestore_edition.json"
LOCAL_JSON_FILE = "public/data/today.json"
HISTORY_FILE = "data/history.json"


def load_firestore_edition():
    """Load the fetched Firestore edition data."""
    if not os.path.exists(FIRESTORE_DATA_FILE):
        print(f"[error] Firestore data file not found: {FIRESTORE_DATA_FILE}", file=sys.stderr)
        print("[error] Run firestore_fetch_latest.py first", file=sys.stderr)
        sys.exit(1)

    try:
        with open(FIRESTORE_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"[error] Failed to load Firestore data: {e}", file=sys.stderr)
        sys.exit(1)


def validate_edition_data(data):
    """Validate the edition data structure."""
    required_fields = ['date', 'timestamp', 'emojis', 'post_type']

    for field in required_fields:
        if field not in data:
            print(f"[error] Missing required field: {field}", file=sys.stderr)
            return False

    if not isinstance(data['emojis'], list):
        print("[error] 'emojis' field must be a list", file=sys.stderr)
        return False

    if len(data['emojis']) != 5:
        print(f"[warn] Expected 5 emojis, got {len(data['emojis'])}", file=sys.stderr)

    # Validate each emoji
    for i, emoji in enumerate(data['emojis']):
        if not isinstance(emoji, dict):
            print(f"[error] Emoji {i} is not a dictionary", file=sys.stderr)
            return False

        if 'char' not in emoji or 'label' not in emoji:
            print(f"[error] Emoji {i} missing 'char' or 'label'", file=sys.stderr)
            return False

    return True


def update_local_json(edition_data):
    """Update the local JSON file with Firestore edition data."""
    # Remove edition_id (internal field)
    if 'edition_id' in edition_data:
        edition_id = edition_data.pop('edition_id')
        print(f"[info] Edition ID: {edition_id}")

    # Ensure source field indicates Firestore origin
    if 'source' not in edition_data or edition_data['source'] == 'ai-openai':
        edition_data['source'] = 'firestore-manual'

    # Create output directory if needed
    os.makedirs(os.path.dirname(LOCAL_JSON_FILE), exist_ok=True)

    # Write to local JSON file
    try:
        with open(LOCAL_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(edition_data, f, indent=2, ensure_ascii=False)
            f.write('\n')  # Add trailing newline

        print(f"[success] Updated {LOCAL_JSON_FILE}")
        return True

    except Exception as e:
        print(f"[error] Failed to write local JSON: {e}", file=sys.stderr)
        return False


def update_history(edition_data):
    """Update history.json with the new edition (optional)."""
    # This maintains compatibility with the existing pipeline
    # History is updated but not critical for the workflow

    try:
        # Load existing history
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)

        # Add new entry (without edition_id)
        history_entry = {
            'date': edition_data['date'],
            'timestamp': edition_data['timestamp'],
            'emojis': edition_data['emojis'],
            'source': edition_data.get('source', 'firestore-manual')
        }

        # Check if this date already exists
        existing_dates = [entry.get('date') for entry in history]
        if edition_data['date'] in existing_dates:
            print(f"[info] Date {edition_data['date']} already in history, skipping")
            return True

        # Add to history
        history.append(history_entry)

        # Keep last 30 days
        history = history[-30:]

        # Write history
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
            f.write('\n')

        print(f"[success] Updated {HISTORY_FILE}")
        return True

    except Exception as e:
        print(f"[warn] Failed to update history: {e}", file=sys.stderr)
        # Non-critical, continue
        return True


def main():
    """Main entry point."""
    print("[info] Starting local JSON update from Firestore...")

    # Load Firestore edition data
    print(f"[info] Loading Firestore data from {FIRESTORE_DATA_FILE}...")
    edition_data = load_firestore_edition()

    # Validate data
    print("[info] Validating edition data...")
    if not validate_edition_data(edition_data):
        print("[error] Edition data validation failed", file=sys.stderr)
        sys.exit(1)

    print("[success] Edition data validated")
    print(f"[info] Date: {edition_data['date']}")
    print(f"[info] Timestamp: {edition_data['timestamp']}")
    print(f"[info] Post type: {edition_data['post_type']}")
    print(f"[info] Emojis: {' '.join([e['char'] for e in edition_data['emojis']])}")

    # Update local JSON
    print(f"[info] Updating {LOCAL_JSON_FILE}...")
    if not update_local_json(edition_data):
        sys.exit(1)

    # Update history
    print(f"[info] Updating {HISTORY_FILE}...")
    update_history(edition_data)

    print("\n[success] Local JSON files updated successfully!")
    print(f"[info] Updated files:")
    print(f"  - {LOCAL_JSON_FILE}")
    print(f"  - {HISTORY_FILE}")

    # Print emoji summary
    print(f"\n[info] Emoji summary:")
    for i, emoji in enumerate(edition_data['emojis'], 1):
        print(f"  {i}. {emoji['char']} - {emoji['label']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
