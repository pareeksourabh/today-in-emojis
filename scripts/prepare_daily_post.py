#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepare today's post type (normal vs essence) and enrich today.json with essence data.
"""

import os
import sys
import json
import time
import http.client
from datetime import date

INPUT_FILE = "public/data/today.json"
POSTED_LOG = "data/instagram_posted.json"

DEFAULT_CADENCE_N = 6
DEFAULT_PALETTE = ["😢", "😡", "😨", "😮", "🙂", "❤️", "😔", "😤", "😬", "🙏", "🌍", "⚖️"]
DEFAULT_TEMPERATURE = 0.7
DEFAULT_FALLBACK_EMOJI = "🌍"

OPENAI_MODEL = "gpt-4o-mini"


def load_today(path: str) -> dict:
    if not os.path.exists(path):
        print(f"[error] Input file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_today(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_posted_count_today(path: str, today_date: str) -> int:
    """Count how many posts have already been posted today (same date)."""
    if not os.path.exists(path):
        return 0
    try:
        with open(path, "r", encoding="utf-8") as f:
            posted = json.load(f)
            timestamps = posted.get("timestamps", [])
            if not isinstance(timestamps, list):
                return 0
            # Count timestamps that match today's date
            count = sum(1 for ts in timestamps if ts.startswith(today_date))
            return count
    except Exception as e:
        print(f"[warn] Could not read posted log: {e}", file=sys.stderr)
    return 0


def load_total_posted_count(path: str) -> int:
    """Count total posts across all time (for grid column calculation)."""
    if not os.path.exists(path):
        return 0
    try:
        with open(path, "r", encoding="utf-8") as f:
            posted = json.load(f)
            timestamps = posted.get("timestamps", [])
            if isinstance(timestamps, list):
                return len(timestamps)
    except Exception as e:
        print(f"[warn] Could not read posted log: {e}", file=sys.stderr)
    return 0


def parse_palette(value):
    if not value:
        return DEFAULT_PALETTE
    raw = value.replace(",", " ").split()
    palette = [p.strip() for p in raw if p.strip()]
    return palette or DEFAULT_PALETTE


def normalize_json_text(raw: str) -> str:
    if not isinstance(raw, str):
        raise ValueError("LLM response is not text")
    text = raw.strip()
    if text.startswith("```"):
        parts = text.split("```")
        for part in parts:
            candidate = part.strip()
            if not candidate:
                continue
            if candidate.lower().startswith("json"):
                candidate = candidate[4:].strip()
            if candidate:
                return candidate
        return ""
    if text and text[0] not in "[{":
        for marker in ("[", "{"):
            idx = text.find(marker)
            if idx != -1:
                return text[idx:].strip()
        return text
    return text


def openai_essence_call(items: list, palette: list, temperature: float) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing")

    system = (
        "You interpret the overall emotional essence of the day from the provided news items. "
        "Choose one emoji from the allowed palette, a short emotion label, and a 1-2 line rationale. "
        "Be opinionated but stay within the palette."
    )
    user_payload = {
        "task": (
            "Select a single emotion emoji representing the overall vibe of the day. "
            "Return JSON only, using the required schema."
        ),
        "items": items,
        "palette": palette,
        "rules": [
            "Emoji must be one of the provided palette options.",
            "Rationale must be 1-2 lines.",
            "Return JSON only."
        ],
    }

    schema = {
        "type": "object",
        "properties": {
            "emotion_label": {"type": "string", "minLength": 1, "maxLength": 64},
            "emoji": {"type": "string", "enum": palette},
            "rationale": {"type": "string", "minLength": 1, "maxLength": 240},
        },
        "required": ["emotion_label", "emoji", "rationale"],
        "additionalProperties": False,
    }

    body = json.dumps({
        "model": OPENAI_MODEL,
        "temperature": temperature,
        "max_tokens": 200,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "essence_selection",
                "schema": schema,
                "strict": True,
            }
        },
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
        ],
    })

    conn = http.client.HTTPSConnection("api.openai.com", timeout=30)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    conn.request("POST", "/v1/chat/completions", body=body.encode("utf-8"), headers=headers)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()

    if resp.status < 200 or resp.status >= 300:
        error_msg = data.decode("utf-8", "ignore")
        raise RuntimeError(f"OpenAI error {resp.status}: {error_msg[:200]}")

    payload = json.loads(data.decode("utf-8"))
    choices = payload.get("choices", [])
    if not choices:
        raise RuntimeError("OpenAI response missing choices")

    message = choices[0].get("message", {})
    text = message.get("content", "").strip()
    if not text:
        raise RuntimeError("OpenAI response empty")

    return text


def validate_essence(raw: str, palette: list) -> dict:
    cleaned = normalize_json_text(raw)
    data = json.loads(cleaned)
    if not isinstance(data, dict):
        raise ValueError("Essence response must be an object")
    label = data.get("emotion_label")
    emoji = data.get("emoji")
    rationale = data.get("rationale")
    if not isinstance(label, str) or not label.strip():
        raise ValueError("Essence label missing")
    if not isinstance(emoji, str) or emoji not in palette:
        raise ValueError("Essence emoji not in palette")
    if not isinstance(rationale, str) or not rationale.strip():
        raise ValueError("Essence rationale missing")
    return {
        "emotion_label": label.strip(),
        "emoji": emoji,
        "rationale": rationale.strip(),
    }


def build_items_for_llm(emojis: list) -> list:
    items = []
    for it in emojis:
        title = (it.get("title") or "").strip()
        summary = (it.get("summary") or "").strip()
        if not summary:
            summary = title
        items.append({"title": title, "summary": summary})
    return items


def main() -> int:
    data = load_today(INPUT_FILE)
    try:
        cadence_n = int(os.environ.get("ESSENCE_CADENCE_N", DEFAULT_CADENCE_N))
    except ValueError:
        cadence_n = DEFAULT_CADENCE_N
    if cadence_n <= 0:
        cadence_n = DEFAULT_CADENCE_N
    palette = parse_palette(os.environ.get("ESSENCE_EMOJI_PALETTE"))
    temperature = float(os.environ.get("ESSENCE_TEMPERATURE", DEFAULT_TEMPERATURE))
    fallback_emoji = os.environ.get("ESSENCE_FALLBACK_EMOJI", DEFAULT_FALLBACK_EMOJI)

    # Get today's date from the data
    today_date = data.get("date", date.today().isoformat())

    # Count posts from today only (for essence cadence)
    posts_today = load_posted_count_today(POSTED_LOG, today_date)
    sequence_index = posts_today + 1  # This is the Nth post of the day
    should_post_essence = sequence_index == cadence_n

    # Count total posts across all time (for grid column calculation)
    total_posted_count = load_total_posted_count(POSTED_LOG)
    grid_column = ((total_posted_count + 1 - 1) % 3) + 1

    data["cadence"] = {
        "n": cadence_n,
        "sequence_index": sequence_index,
        "grid_column": grid_column,
        "posted_count": total_posted_count,
    }

    if not should_post_essence:
        data["post_type"] = "normal"
        if "essence" in data:
            del data["essence"]
        save_today(INPUT_FILE, data)
        print(f"[info] Cadence: N={cadence_n}, sequence_index={sequence_index} -> normal post")
        return 0

    emojis = data.get("emojis", [])
    items = build_items_for_llm(emojis)
    essence = None
    failure = None

    try:
        raw = openai_essence_call(items, palette, temperature)
        essence = validate_essence(raw, palette)
    except Exception as e:
        failure = str(e)

    if essence is None:
        essence = {
            "emotion_label": "neutral",
            "emoji": fallback_emoji,
            "rationale": "Mixed signals across the day; using a neutral default.",
        }
        print(f"[warn] Essence selection failed: {failure}", file=sys.stderr)

    data["post_type"] = "essence"
    data["essence"] = {
        **essence,
        "palette": palette,
        "temperature": temperature,
        "fallback": failure is not None,
    }

    save_today(INPUT_FILE, data)

    print(f"[info] Cadence: N={cadence_n}, sequence_index={sequence_index} -> essence post")
    print(f"[info] Grid column: {grid_column}")
    print(f"[info] Essence label: {essence['emotion_label']}")
    print(f"[info] Essence emoji: {essence['emoji']}")
    print(f"[info] Essence rationale: {essence['rationale']}")
    print(f"[info] Date: {data.get('date', date.today().isoformat())}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
