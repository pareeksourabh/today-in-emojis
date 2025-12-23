#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a local dry-run sequence of images (including essence) without posting.
"""

import argparse
import copy
import json
import os
import subprocess
import tempfile
import sys

DEFAULT_INPUT = "public/data/today.json"
DEFAULT_OUTPUT_DIR = "public/images/dry-run"
DEFAULT_CADENCE_N = 6


def load_base_data(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "date": "2025-01-01",
        "timestamp": "2025-01-01T00:00:00Z",
        "emojis": [
            {"char": "🌍", "label": "world", "title": "Global headlines", "summary": "A mix of global news."},
            {"char": "💡", "label": "insight", "title": "Tech breakthrough", "summary": "Innovation spotlight."},
            {"char": "🤝", "label": "together", "title": "Diplomacy", "summary": "A new agreement emerges."},
            {"char": "🌱", "label": "growth", "title": "Markets shift", "summary": "Economic signals are mixed."},
            {"char": "😐", "label": "neutral", "title": "Politics", "summary": "Developments continue."},
        ],
        "source": "dry-run",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run image generation sequence")
    parser.add_argument("--count", type=int, default=6, help="Number of images to generate")
    parser.add_argument("--cadence", type=int, default=DEFAULT_CADENCE_N, help="Essence cadence N")
    parser.add_argument("--input", type=str, default=DEFAULT_INPUT, help="Input today.json path")
    parser.add_argument("--output-dir", type=str, default=DEFAULT_OUTPUT_DIR, help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    base_data = load_base_data(args.input)

    for i in range(1, args.count + 1):
        data = copy.deepcopy(base_data)
        is_essence = (i % args.cadence) == 0
        data["post_type"] = "essence" if is_essence else "normal"
        data["cadence"] = {"n": args.cadence, "sequence_index": i}

        if is_essence:
            data["essence"] = {
                "emotion_label": "reflective",
                "emoji": "🙂",
                "rationale": "Dry run sample for the essence post.",
            }
        else:
            data.pop("essence", None)

        output_path = os.path.join(args.output_dir, f"dry-run-{i:02d}-{data['post_type']}.png")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            temp_path = tmp.name

        try:
            subprocess.run(
                [sys.executable, "scripts/generate_emoji_image.py", "--input", temp_path, "--output", output_path],
                check=True,
            )
            print(f"[info] Generated {output_path}")
        finally:
            try:
                os.unlink(temp_path)
            except Exception:
                pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
