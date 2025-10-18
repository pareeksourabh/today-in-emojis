# Phase 5 — Functional Build

## What this delivers
- Client-side render of five emojis from `./data/today.json` (works on GitHub Pages).
- Footer reactions with localStorage persistence under key `tie:reaction:v1`.
- One-viewport layout (no scroll), minimal animations, accessible buttons.

## Files added
- `pages/index.tsx` — header → emoji row → footer
- `components/EmojiRow.tsx` — renders five emojis with optional links
- `components/Footer.tsx` — Like / Neutral / Dislike + credits + links
- `utils/storage.ts` — localStorage helpers
- `styles/globals.css` — Tailwind v4 import + page styles
- `next.config.js` — static export enabled
- `data/today.json` — sample data for development

## Run locally
```bash
npm install
npm run dev
```

## Build & export
```bash
npm run build   # outputs to ./out for GitHub Pages workflow
```

## Notes
- Emojis can include optional `url` to open the source in a new tab.
- Reactions are local-only by design for MVP (no backend).
