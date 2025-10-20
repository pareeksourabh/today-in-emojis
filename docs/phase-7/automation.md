# Phase 7 — Automation

## Goal
Automatically refresh `data/today.json` every day from free RSS sources, mapping headlines to a set of five emojis for the homepage.

## How it works
1. GitHub Actions runs on a daily cron (00:00 UTC) or manually via the Actions tab.
2. The workflow executes `scripts/update_emojis.py`.
3. The script fetches RSS headlines, maps them to categories and lightweight sentiment, and writes `data/today.json` (and appends `data/history.json`).
4. The commit triggers the Pages deploy workflow so the site updates.

## Sources (RSS)
- BBC World
- Reuters World
- The Guardian World
- AP Top News

Edit the list in `scripts/update_emojis.py` under `RSS_SOURCES`.

## Mapping logic
- **Categories**: keyword lists map headlines to topic emojis (e.g., conflict 🪖, markets 💹, tech 🤖, natural event 🌋, sport 🏆, culture 🎭).
- **Sentiment**: tiny positive/negative word lists occasionally swap a mood emoji (🙂 / 🙁 / 😐) for variety.
- **Diversity**: ensures unique labels so the final five cover multiple topics.
- **Links**: each emoji includes the source article URL for optional reading.
- **Fallback**: writes a neutral default set if feeds fail.

## Output shape
```json
{
  "date": "YYYY-MM-DD",
  "emojis": [
    { "char": "💹", "label": "markets", "url": "https://..." },
    { "char": "🕊️", "label": "diplomacy", "url": "https://..." },
    { "char": "🌋", "label": "natural event", "url": "https://..." },
    { "char": "🏆", "label": "sport", "url": "https://..." },
    { "char": "🤖", "label": "tech", "url": "https://..." }
  ],
  "source": "rss-deterministic"
}
