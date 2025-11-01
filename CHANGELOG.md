# Changelog

## [2025-11-01] Phase 8 — Analytics & Monitoring complete
- **Added Google Analytics 4 (GA4)** with measurement ID integration for comprehensive site analytics.
- **Implemented custom event tracking** for all user interactions:
  - `emoji_click` — Tracks clicks on news emoji links with emoji character, label, and URL.
  - `reaction_click` — Tracks user sentiment via footer reactions (❤️ Like, 🤔 Neutral, 👎 Dislike).
  - `footer_link_click` — Tracks engagement with "What's this?" GitHub README link.
- **Created GoogleAnalytics component** using Next.js Script component with optimal loading strategy.
- **Integrated analytics into layout** for automatic tracking across all pages.
- **Enabled real-time monitoring** of page views, user demographics, and custom events in GA4 dashboard.
- **Documentation**: Added `docs/phase-8/analytics.md` detailing implementation and event tracking.

## [2025-10-27 - 2025-10-31] Phase 7 Enhancements — AI Integration & Automation Fixes
- **Fixed OpenAI API integration** by migrating from deprecated `/v1/responses` endpoint to stable `/v1/chat/completions` API.
- **Resolved workflow permissions** by adding PAT token support to enable automatic Pages deployment triggers.
- **Fixed data path issue** by updating script to write to `public/data/today.json` for proper deployment.
- **Added headline title support** in emoji data structure for better hover tooltips showing full news headlines.
- **Enhanced security** with branch protection rules, CODEOWNERS file, and admin-only bypass configuration.
- **Improved debugging** with comprehensive error logging and validation for OpenAI API responses.
- **Fixed GitHub Actions workflow** YAML syntax and trigger configuration for reliable automation.

## [2025-10-18 19:07] Phase 6 — Deploy & Polish complete
- Added GitHub Pages workflow to build and deploy static site on each push and data change.
- Added explicit `next.config.js` for static export compatibility with the App Router.
- Added `robots.txt` and `sitemap.txt` under `public/` for SEO and indexing support.
- Enhanced production polish with meta tags, no-scroll layout, and minimal 404 page.
- Introduced subtle colored “What’s this?” footer chip as an opt-in link to the README.
- Verified GitHub Actions deployment pipeline for public access and data auto-refresh.

## [2025-10-18 18:22] Phase 5 — Functional Build complete
- Implemented client-side rendering of five emojis from `data/today.json` (GitHub Pages compatible).
- Added footer reactions (❤️ 🤔 👎) with `localStorage` persistence.
- Ensured one-viewport layout with minimal animation and full accessibility.
- Introduced colored "What's this?" accent link in footer for opt-in context.
- Prepared for Phase 6 — Deploy and Polish (GitHub Pages workflow + final styling).

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
