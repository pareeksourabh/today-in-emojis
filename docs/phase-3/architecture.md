# Phase 3 — Architecture & Build Plan

## Goals
- Build a zero-scroll one-pager that shows a title, five emojis, and a footer with reactions and links.
- Keep it free-tier friendly, minimal, and automatable.

## Tech Stack (Zero-Cost)
- **Framework:** Next.js (React) — free
- **Styling:** Tailwind CSS — free
- **Hosting:** Start with Github pages then move to Vercel (Hobby) — free
- **Automation:** GitHub Actions (CRON) — free
- **Data:** Flat JSON in `/data/today.json`; archive in `/data/archive/YYYY-MM-DD.json`
- **Feedback:** Phase 1 — `localStorage` only (no backend)
- **Links:** Optional per-emoji `url` field

## Directory Structure
```
/ (repo root)
├─ data/
│  ├─ today.json                   # current day's emoji set
│  └─ archive/                     # historical snapshots (optional later)
│     └─ 2025-10-18.json
├─ docs/
│  └─ phase-3/
│     ├─ architecture.md
│     ├─ data-schema.md
│     └─ automation.md
├─ pages/                          # or app/ if using Next 13+ app router
│  └─ index.tsx                    # renders title, 5 emojis, footer
├─ components/
│  ├─ EmojiRow.tsx                 # maps over 5 emojis
│  └─ Footer.tsx                   # reactions + credits + links
├─ public/
│  └─ favicon.ico
├─ styles/
│  └─ globals.css
└─ .github/
   └─ workflows/
      └─ daily.yml                 # scheduled job to rotate /data/today.json
```

## Rendering Flow
1. `getStaticProps` (or a simple client-side fetch) reads `/data/today.json`
2. `index.tsx` renders:
   - Header: "TODAY IN EMOJIS"
   - EmojiRow: five emojis, each optionally wrapped in `<a href>`
   - Footer: three reaction buttons, credits, links
3. CSS ensures everything fits in one viewport height (no scroll).

## State & Interactions
- **Reactions:** `localStorage` key: `tie:reaction:v1` with values: `"like" | "neutral" | "dislike"`
- **Hover:** CSS transform scale; **Click:** toggle stored reaction
- **Accessibility:** `role="button"`, `aria-pressed`, focus states, keyboard activation

## Performance & Accessibility
- No external fonts required (optional Inter via Google Fonts); system fonts acceptable.
- Keep bundle small; no heavy dependencies.
- Add `prefers-reduced-motion` CSS to disable animation if user prefers.
