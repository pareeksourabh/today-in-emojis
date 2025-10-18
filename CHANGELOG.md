# Changelog

## [2025-10-18 18:22] Phase 5 — Functional Build complete
- Implemented client-side rendering of five emojis from `data/today.json` (GitHub Pages compatible).
- Added footer reactions (❤️ 🤔 👎) with `localStorage` persistence.
- Ensured one-viewport layout with minimal animation and full accessibility.
- Introduced colored “What’s this?” accent link in footer for opt-in context.
- Prepared for Phase 6 — Deploy and Polish (GitHub Pages workflow + final styling).

## [2025-10-18 17:19] Phase 5 — Functional Build complete
- Implemented client-side rendering of five emojis from `data/today.json` (GitHub Pages compatible).
- Added footer reactions (Like / Neutral / Dislike) with localStorage persistence.
- Ensured one-viewport layout with minimal animations and accessible controls.
- Included `next.config.js` for static export and Tailwind v4 globals.
- Added developer notes in `docs/phase-5/build-notes.md`.

## [2025-10-18 17:09] Phase 4 — MVP Scaffold complete
- Initialized **Next.js + React + Tailwind v4** environment for the one-page app.
- Added `dev`, `build`, and `start` npm scripts to `package.json`.
- Configured **Tailwind v4** with zero-config setup using `@import "tailwindcss"` in `globals.css`.
- Expanded `.gitignore` to exclude `node_modules`, build artifacts, cache, and temporary files.
- Included `next-env.d.ts` to enable TypeScript IntelliSense and environment typings.
- Verified `npm run dev` local environment and baseline page render.
- Prepared structure for future components: header, emoji row, and footer reactions.
- Marks completion of **MVP scaffolding**, paving the way for Phase 5 — Functional Build.

## [2025-10-18 16:26] Phase 3 — Architecture & Build plan locked
- Added technical stack definition and directory structure.
- Documented data schema (`data/today.json`) and archive approach.
- Added GitHub Actions daily rotation workflow (`.github/workflows/daily.yml`).
- Seeded `data/today.json` example for development.

## [2025-10-18 15:33 +08] Phase 2 — Design locked
- Added visual moodboard outlining color, typography, spacing, and motion principles.
- Created schematic wireframe (`design/wireframe-onepager.png`) for one-pager layout.
- Documented detailed design specs (`design/specs.md`).
- Established second milestone commit following Phase 1 - Discovery.

## [2025-10-18 13:58 +08] Phase 1 — Discovery locked
- Added Manifesto, Positioning, Taglines.
- Seeded README with experience principles and folder structure.
