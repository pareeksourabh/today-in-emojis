#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update data/today.json by fetching news headlines from free RSS feeds,
mapping them to 5 representative emojis, and appending data/history.json.

- Free: public RSS (no paid APIs)
- Transparent: deterministic keyword mapping (with tiny mood heuristic)
- Safe: no secrets; optional AI layer can be added later via Actions secrets
"""
import os, json, re, random, datetime, sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

try:
    import feedparser  # pip install feedparser
except Exception:
    print("Missing dependency 'feedparser'. Install it first.", file=sys.stderr)
    sys.exit(1)

# -----------------------------
# Config
# -----------------------------
RSS_SOURCES = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.reutersagency.com/feed/?best-sectors=world&post_type=best",
    "https://www.theguardian.com/world/rss",
    # AP can be inconsistent as RSS; feedparser handles some HTML pages too.
    "https://apnews.com/hub/ap-top-news?utm_source=apnews.com&utm_medium=referral&utm_campaign=ap_rss",
]

MAX_ITEMS = 40           # total headlines to consider
PICK_COUNT = 5           # final emoji count
OUTPUT_TODAY = "data/today.json"
OUTPUT_HISTORY = "data/history.json"

# keywords -> (emoji, label)
CATEGORY_KEYWORDS = [
    (["war","conflict","clash","missile","strike","shell","offensive","bomb","drone","raid","troop","battle","fighting"], "🪖", "conflict"),
    (["ceasefire","peace","talks","deal","agreement","accord","truce","diplomacy","negotiation"], "🕊️", "diplomacy"),
    (["election","vote","ballot","parliament","congress","senate","candidate","campaign","polls","referendum"], "🗳️", "politics"),
    (["inflation","stocks","markets","market","interest rate","fed","ecb","boj","rbi","bond","economy","recession","gdp"], "💹", "markets"),
    (["ai","artificial intelligence","tech","technology","startup","software","chip","semiconductor","robot","data","cyber"], "🤖", "tech"),
    (["earthquake","quake","flood","wildfire","hurricane","typhoon","storm","volcano","eruption","tsunami","heatwave","drought"], "🌋", "natural event"),
    (["covid","virus","disease","outbreak","vaccine","health","hospital"], "🩺", "health"),
    (["football","soccer","basketball","tennis","cricket","golf","olympics","world cup","fifa","nba","grand slam","tournament","match"], "🏆", "sport"),
    (["culture","art","film","movie","music","festival","award","oscars","grammys","book","exhibit","museum"], "🎭", "culture"),
    (["space","nasa","spacex","launch","rocket","asteroid","moon","mars","satellite","iss"], "🚀", "space"),
    (["energy","oil","gas","electric","power","renewable","solar","wind","nuclear"], "⚡", "energy"),
    (["crime","trial","court","lawsuit","verdict","charge","arrest","sentence"], "⚖️", "legal"),
]

NEGATIVE_WORDS = {"dead","death","kill","killed","attack","blast","crash","collapse","crisis","decline","drop","ban","sanction","fear","worry","concern","tragic","hostage","strike","flee","famine","shortage"}
POSITIVE_WORDS = {"rise","gain","growth","record","peace","resolve","win","wins","victory","award","recover","recovery","boost","surge","deal","agreement","truce"}

MOOD_EMOJIS = {"positive": "🙂","negative": "🙁","neutral": "😐"}

SAFE_DEFAULTS = [
    {"char": "😐", "label": "neutral", "url": ""},
    {"char": "💡", "label": "insight", "url": ""},
    {"char": "🤝", "label": "together", "url": ""},
    {"char": "🌱", "label": "growth", "url": ""},
    {"char": "🌍", "label": "world", "url": ""},
]

USER_AGENT = "Mozilla/5.0 (compatible; TodayInEmojis/1.0; +https://github.com)"

def normalize(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def categorize(headline: str):
    h = normalize(headline)
    for keywords, emoji, label in CATEGORY_KEYWORDS:
        for kw in keywords:
            if kw in h:
                return emoji, label
    if any(k in h for k in ["china","india","europe","africa","america","asia","russia","ukraine","gaza","israel","middle east"]):
        return "🌍", "world"
    return "📰", "news"

def mood_of(headline: str):
    h = normalize(headline)
    pos = sum(1 for w in POSITIVE_WORDS if w in h)
    neg = sum(1 for w in NEGATIVE_WORDS if w in h)
    if pos > neg and pos > 0:
        return MOOD_EMOJIS["positive"]
    if neg > pos and neg > 0:
        return MOOD_EMOJIS["negative"]
    return MOOD_EMOJIS["neutral"]

def fetch_feed(url: str):
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=20) as resp:
            data = resp.read()
        return feedparser.parse(data)
    except (URLError, HTTPError) as e:
        print(f"[warn] fetch failed: {url} -> {e}", file=sys.stderr)
        return {"entries": []}

def unique_by_label(items):
    seen = set()
    out = []
    for it in items:
        key = it["label"]
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out

def main():
    entries = []
    for url in RSS_SOURCES:
        feed = fetch_feed(url)
        for e in feed.get("entries", []):
            title = e.get("title") or ""
            link = e.get("link") or ""
            if not title or not link:
                continue
            entries.append({"title": title, "link": link})
            if len(entries) >= MAX_ITEMS:
                break
        if len(entries) >= MAX_ITEMS:
            break

    # Fallback
    if not entries:
        print("[warn] No entries found; writing safe defaults.")
        data = {"date": datetime.date.today().isoformat(), "emojis": SAFE_DEFAULTS, "source": "fallback"}
        os.makedirs(os.path.dirname(OUTPUT_TODAY), exist_ok=True)
        with open(OUTPUT_TODAY, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return 0

    # Map to emojis
    mapped = []
    random.shuffle(entries)
    for item in entries:
        title = item["title"]
        link = item["link"]
        emoji, label = categorize(title)
        mood = mood_of(title)
        char = emoji
        # Occasionally swap to mood for variety if non-neutral
        if mood != MOOD_EMOJIS["neutral"] and random.random() < 0.35:
            char = mood
        mapped.append({"char": char, "label": label, "url": link, "title": title})

    # Diversity by label then trim to PICK_COUNT
    diverse = unique_by_label(mapped)
    if len(diverse) < PICK_COUNT:
        labels = {x["label"] for x in diverse}
        for it in mapped:
            if it["label"] in labels:
                continue
            diverse.append(it)
            labels.add(it["label"])
            if len(diverse) >= PICK_COUNT:
                break

    selected = diverse[:PICK_COUNT]
    public = [{"char": it["char"], "label": it["label"], "url": it["url"]} for it in selected]

    today = datetime.date.today().isoformat()
    data = {"date": today, "emojis": public, "source": "rss-deterministic"}

    # Write today.json
    os.makedirs(os.path.dirname(OUTPUT_TODAY), exist_ok=True)
    with open(OUTPUT_TODAY, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Append history.json
    try:
        hist = []
        if os.path.exists(OUTPUT_HISTORY):
            with open(OUTPUT_HISTORY, "r", encoding="utf-8") as f:
                hist = json.load(f)
                if not isinstance(hist, list):
                    hist = []
        hist.append({"date": today, "emojis": public, "meta": {"total_candidates": len(entries)}})
        with open(OUTPUT_HISTORY, "w", encoding="utf-8") as f:
            json.dump(hist, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[warn] Could not append history: {e}", file=sys.stderr)

    # Log selections for visibility
    print("[info] Selected:")
    for it in selected:
        print(f" - {it['char']} {it['label']}: {it['title']} -> {it['url']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
