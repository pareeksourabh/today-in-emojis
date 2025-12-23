# Phase 10 — Execution Tickets

This file tracks execution only.
All intent, rationale, and design decisions live in:
- PHASE_10_HUMANIZATION_REELS_SUBSCRIPTIONS.md
- CODEX_CONTEXT_PHASE_10.md

---

## Phase 10A — Humanization (ACTIVE)

### P10A-1 — Define Essence of the Day rules
- Define how the Essence emoji is selected
- Ensure deterministic or explainable logic
- Handle low-news or low-signal days

---

### P10A-2 — Generate Essence of the Day post
- Single, large emoji
- Minimal layout
- No headline or news text
- Optional omission of date

---

### P10A-3 — Enforce N+1 posting cadence
- Default cadence: 5 + 1 (configurable)
- Essence post must always be the final post in the sequence
- Must not break existing posting automation

---

### P10A-4 — Ensure Instagram grid column alignment
- Target consistent column placement (preferably first column)
- Account for posting order and timing
- Validate alignment across multiple days

---

### P10A-5 — Live profile validation
- Review Instagram grid visually
- Confirm rhythm and monotony break
- Confirm Essence posts act as visual anchors

---

## Phase 10A — Completed

### P10A-DONE-1 — Date padding alignment
- Date text aligned with emoji column
- No clipping or cutoff
- Verified in production

✅ **DONE — no further work required**

---

## Phase 10B — Amplification (PAUSED)

> ⚠️ These tickets are intentionally paused.
> Do NOT implement unless Phase 10A is complete and explicit instruction is given.

---

### Reels (Paused)

- P10B-R1 — Define Reel layout & animation spec
- P10B-R2 — Generate frames for Reels
- P10B-R3 — Implement spotlight animation
- P10B-R4 — Generate TTS narration
- P10B-R5 — Compose video (ffmpeg)
- P10B-R6 — Auto-post Reels with retries & logging

---

### Subscriptions (Paused)

- P10B-S1 — Subscription storage & API
- P10B-S2 — HTML email newsletter template
- P10B-S3 — Daily newsletter sender
- P10B-S4 — Channel abstraction (Email → WhatsApp)

---

## Notes
- Phase 10A must be completed and visually validated before Phase 10B begins
- No ticket in Phase 10B should be picked up prematurely
- Keep tickets small, reversible, and incremental
