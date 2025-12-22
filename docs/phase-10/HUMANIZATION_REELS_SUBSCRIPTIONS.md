# Today in Emojis — Phase 3: Humanization + Reels + Subscriptions

## Why this phase exists
Right now the Instagram profile feels bot-run. We want to:
1) Add subtle human polish to visuals (small layout fixes).
2) Increase engagement via short Reels (5–10s) with a “spotlight per emoji” + voice narration.
3) Add a subscription manager (start with email newsletter; design so we can switch to WhatsApp later).

## Goals (Outcome-driven)
- Feed feels more “real” and intentionally designed (not templated spam).
- Reels become the primary growth lever (shareable, higher reach than images).
- We start capturing an owned audience (subscribers) for future monetization and channel flexibility.

## Non-goals (for this phase)
- No complex content personalization.
- No manual editing workflow; must be automated.
- No paid monetization features yet (just the foundation).

---

## Scope A — Image layout polish (quick win)
### Change A1: Date padding/alignment
**Problem:** Date text on top-left looks slightly “off” and contributes to bot-like grid feel.  
**Change:** Shift the date slightly right by adding left padding so it visually aligns with the first emoji column (date left edge aligned to first emoji left edge).

**Definition of Done**
- Date alignment matches emoji column across all generated image sizes.
- No visual regressions on grid view (9/12 tile Instagram grid).

---

## Scope B — Reels generation + posting (core change)
### Overview
We will generate **1–2 videos per day** (configurable) instead of only static images.

Each Reel:
- Duration: **5–10 seconds**
- Shows the same “5 emojis” set
- Highlights one emoji at a time (spotlight/pulse/zoom) in sequence
- Background: optional subtle motion or minimal static background
- Audio: news narration (voiceover), one line per emoji or short combined script

### Video Format (v1)
- 1080x1920 (vertical)
- 30 fps (or 24 fps) – choose one and standardize
- Simple animation: spotlight overlay + slight scale on active emoji
- Transition timing: ~1 sec per emoji (tuneable)

### Audio (v1)
- Use TTS voice for now (human-like voice), later can switch to recorded voice.
- Script options:
  1) One sentence per emoji, timed to highlight
  2) One short paragraph, still highlighting per emoji

**Definition of Done**
- A single command/job produces:
  - `reel.mp4` + metadata (caption, hashtags, alt text)
  - Posts to Instagram as Reel automatically
- Reel output is deterministic and consistent with the daily news pipeline
- If audio generation fails, fallback to silent Reel (still posts) + log error

---

## Scope C — Subscription manager (owned audience)
### Overview
Users can subscribe via a simple web UI. We store subscribers and send a daily email digest.

Key requirement: **multi-channel-ready**
- Start with email newsletter
- Architecture must allow switching to WhatsApp later without rewriting everything

### Data Model (v1)
Subscriber:
- id
- email (required for v1)
- status (active/unsubscribed)
- created_at, updated_at
- preferred_channel (email now; whatsapp later)
- verification_state (optional: pending/verified)

Events/Logs:
- subscription_created
- subscription_confirmed (if double opt-in used)
- unsubscribed
- delivery_success / delivery_failed

### Newsletter (v1)
- Frequency: once/day (configurable)
- Beautifully formatted HTML email
- Contains the “top emojis + summaries” for the day
- Links back to site and Instagram

**Definition of Done**
- Subscribe/unsubscribe works
- Daily email job sends to all active subscribers
- Email template looks clean on mobile + Gmail + Apple Mail
- Channel abstraction exists (EmailChannel implemented; WhatsAppChannel stubbed)

---

## Implementation approach (suggested)
### Reels generation
- Generate frames (Pillow) OR build a simple video via ffmpeg filtergraph
- Compose audio via TTS
- Merge audio + video via ffmpeg
- Output: mp4 ready for Instagram

### Posting
- Continue using current automation style (cron/GitHub Actions/etc.)
- Add a separate scheduler for reels (1–2 per day)
- Ensure rate limits & failure retries

### Subscriptions
- Simple web form endpoint
- Store in DB (or a lightweight store)
- Daily job composes email + sends
- Maintain channel abstraction from day 1

---

## Acceptance Criteria (Phase 3 complete)
1) Static image generator updated: date alignment polish shipped.
2) Reel generator shipped:
   - consistent 5–10 sec reels
   - emoji spotlight sequence
   - TTS narration
   - auto-posting pipeline
3) Subscription manager shipped:
   - users can subscribe/unsubscribe
   - daily HTML newsletter sent
   - architecture supports adding WhatsApp channel later without redesign

---

## Risks / watch-outs
- Instagram posting APIs and constraints: reels upload requirements, rate limits
- TTS voice quality vs “human” feel: pick a high-quality voice early
- Compliance: email unsubscribe, consent tracking, anti-spam basics
- Reliability: fallbacks when audio/video fails

---

## Phase 3 Task List (engineering checklist)
### A) Image polish
- [ ] Locate date rendering code
- [ ] Add left padding / alignment rule
- [ ] Verify across sample days
- [ ] Update screenshots in README

### B) Reels
- [ ] Define reel layout spec (positions, timings, typography)
- [ ] Implement frame generator
- [ ] Implement spotlight animation
- [ ] Implement TTS script generation
- [ ] Implement ffmpeg composition (video+audio)
- [ ] Implement reel posting job
- [ ] Add monitoring logs + failure fallback

### C) Subscriptions
- [ ] Add subscribe endpoint + storage
- [ ] Add unsubscribe endpoint
- [ ] Create HTML email template
- [ ] Add daily send job
- [ ] Add Channel interface (EmailChannel now, WhatsAppChannel later)
