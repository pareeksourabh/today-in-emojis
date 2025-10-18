# Data Schema — `data/today.json`

## Shape
```json
{
  "date": "YYYY-MM-DD",
  "emojis": [
    {
      "char": "😀",
      "label": "joy",
      "url": "https://news.example.com/story-1"
    },
    {
      "char": "🔥",
      "label": "heatwave",
      "url": "https://news.example.com/story-2"
    }
  ]
}
```

- `date`: ISO date of the set
- `emojis`: ordered list of five items
  - `char`: the emoji to render
  - `label`: short accessible label (for screen readers / tooltips)
  - `url`: optional; clicking emoji opens link in new tab

## Example (`data/today.json`)
```json
{
  "date": "2025-10-18",
  "emojis": [
    { "char": "😐", "label": "neutral mood", "url": "" },
    { "char": "💰", "label": "markets", "url": "" },
    { "char": "🏆", "label": "sport highlight", "url": "" },
    { "char": "🌋", "label": "nature event", "url": "" },
    { "char": "🌸", "label": "culture/soft vibe", "url": "" }
  ]
}
```

## Archive Strategy
- Snapshot the previous `today.json` into `data/archive/YYYY-MM-DD.json` at the start of each rotation (optional; not shown on main page).
