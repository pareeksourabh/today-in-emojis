#!/usr/bin/env python3
"""
Fetch the latest normal edition from Firestore.

This script connects to Google Cloud Firestore, queries for the most recent
"normal" post edition, and returns the data in a normalized format.

Environment variables required:
- GOOGLE_APPLICATION_CREDENTIALS: Path to GCP service account JSON
- GCP_PROJECT_ID: Google Cloud project ID
- FIRESTORE_COLLECTION: Firestore collection name (e.g., "editions")

Usage:
    python scripts/firestore_fetch_latest.py
"""

import os
import sys
import json
from datetime import datetime

def fetch_latest_normal_edition():
    """
    Fetch the latest normal edition from Firestore.

    Returns:
        dict: Normalized edition data with keys:
            - date (str): ISO date
            - timestamp (str): ISO timestamp
            - emojis (list): List of emoji dicts with char, label, url, title, summary
            - source (str): Data source identifier
            - post_type (str): "normal"
            - edition_id (str): Firestore document ID
    """
    try:
        from google.cloud import firestore
    except ImportError:
        print("[error] google-cloud-firestore not installed", file=sys.stderr)
        print("[error] Run: pip install google-cloud-firestore", file=sys.stderr)
        sys.exit(1)

    # Get configuration from environment
    project_id = os.environ.get('GCP_PROJECT_ID')
    collection_name = os.environ.get('FIRESTORE_COLLECTION')
    credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

    if not project_id:
        print("[error] GCP_PROJECT_ID environment variable not set", file=sys.stderr)
        sys.exit(1)

    if not collection_name:
        print("[error] FIRESTORE_COLLECTION environment variable not set", file=sys.stderr)
        sys.exit(1)

    if not credentials_path:
        print("[error] GOOGLE_APPLICATION_CREDENTIALS environment variable not set", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(credentials_path):
        print(f"[error] Credentials file not found: {credentials_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[info] Connecting to Firestore...")
    print(f"[info] Project ID: {project_id}")
    print(f"[info] Collection: {collection_name}")

    # Initialize Firestore client
    try:
        db = firestore.Client(project=project_id)
    except Exception as e:
        print(f"[error] Failed to initialize Firestore client: {e}", file=sys.stderr)
        sys.exit(1)

    # Query for latest normal edition
    print(f"[info] Querying for latest normal edition...")

    try:
        query = (
            db.collection(collection_name)
            .where('post_type', '==', 'normal')
            .order_by('timestamp', direction=firestore.Query.DESCENDING)
            .limit(1)
        )

        docs = list(query.stream())

        if not docs:
            print("[error] No normal editions found in Firestore", file=sys.stderr)
            sys.exit(1)

        doc = docs[0]
        data = doc.to_dict()
        edition_id = doc.id

        print(f"[success] Found edition: {edition_id}")
        print(f"[info] Date: {data.get('date')}")
        print(f"[info] Timestamp: {data.get('timestamp')}")
        print(f"[info] Post type: {data.get('post_type')}")
        print(f"[info] Emojis count: {len(data.get('emojis', []))}")

        # Validate required fields
        if 'emojis' not in data or not isinstance(data['emojis'], list):
            print("[error] Edition missing 'emojis' field or invalid format", file=sys.stderr)
            sys.exit(1)

        if len(data['emojis']) != 5:
            print(f"[warn] Expected 5 emojis, got {len(data['emojis'])}", file=sys.stderr)

        # Normalize the data
        normalized = {
            'date': data.get('date'),
            'timestamp': data.get('timestamp'),
            'emojis': data.get('emojis', []),
            'source': data.get('source', 'firestore-manual'),
            'post_type': data.get('post_type', 'normal'),
            'edition_id': edition_id
        }

        # Validate emoji structure
        for i, emoji in enumerate(normalized['emojis']):
            required_fields = ['char', 'label']
            for field in required_fields:
                if field not in emoji:
                    print(f"[warn] Emoji {i} missing required field: {field}", file=sys.stderr)

        return normalized

    except Exception as e:
        print(f"[error] Firestore query failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    print("[info] Starting Firestore fetch...")

    edition = fetch_latest_normal_edition()

    # Output as JSON for consumption by other scripts
    print("\n[info] Edition data (JSON):")
    print(json.dumps(edition, indent=2, ensure_ascii=False))

    # Also write to a temp file for easy consumption
    output_file = "/tmp/firestore_edition.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(edition, f, indent=2, ensure_ascii=False)

    print(f"\n[success] Edition data written to: {output_file}")
    print(f"[info] Edition ID: {edition['edition_id']}")
    print(f"[info] Date: {edition['date']}")
    print(f"[info] Emojis: {' '.join([e.get('char', '?') for e in edition['emojis']])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
