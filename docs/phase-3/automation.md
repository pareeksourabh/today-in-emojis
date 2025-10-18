# Automation Plan — Daily Rotation

## Approach
- Use GitHub Actions with a daily CRON (UTC midnight) to:
  1. (MVP) Copy a placeholder set or rotate from a local list.
  2. (Later) Fetch top stories via a free RSS/News API, map to emojis, update `/data/today.json`.

## GitHub Actions Workflow
File: `.github/workflows/daily.yml`
```yaml
name: Daily Emoji Rotation

on:
  schedule:
    - cron: "0 0 * * *"   # daily at 00:00 UTC
  workflow_dispatch:

jobs:
  rotate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set date
        id: d
        run: echo "DATE=$(date -u +'%Y-%m-%d')" >> $GITHUB_ENV

      - name: Write placeholder today.json
        run: |
          cat > data/today.json <<'JSON'
          {
            "date": "${ env.DATE }",
            "emojis": [
              { "char": "😐", "label": "neutral mood", "url": "" },
              { "char": "💰", "label": "markets", "url": "" },
              { "char": "🏆", "label": "sport highlight", "url": "" },
              { "char": "🌋", "label": "nature event", "url": "" },
              { "char": "🌸", "label": "culture/soft vibe", "url": "" }
            ]
          }
          JSON

      - name: Commit changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add data/today.json
          git commit -m "chore(data): rotate today.json for ${ env.DATE }" || echo "No changes"
          git push
```

## Notes
- The placeholder step ensures the site always updates daily (even before we wire real sources).
- Later, replace the "Write placeholder" step with a small Node/TS script that reads RSS or Trends and maps to emojis.
