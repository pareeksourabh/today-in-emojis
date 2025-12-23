# Codex Context — Today in Emojis (Phase 10)

You are working inside the Today in Emojis repository.

This is a mature project. Phase 10 represents a late-stage evolution focused on identity and humanization, not foundational refactors.

---

## Product Intent

Today in Emojis generates daily emoji-based news summaries and posts them automatically.

The system is reliable and consistent, but still risks feeling algorithmic.

**Phase 10 exists to make the product feel human, intentional, and emotionally resonant — before scaling reach or monetization.**

---

## Phase Structure (Critical)

Phase 10 is intentionally split:

- **Phase 10A — Humanization & Emotional Identity (ACTIVE)**
- **Phase 10B — Amplification: Reels & Subscriptions (PAUSED)**

⚠️ **Only Phase 10A is currently active.**  
Reels and Subscriptions must NOT be implemented unless explicitly instructed.

---

## What to Build Now (Phase 10A ONLY)

### 1) Essence of the Day (Primary Focus)

Introduce a recurring post that captures the *emotional essence of the entire day* using a single emoji.

Key characteristics:
- One large emoji
- No news summary
- No explanation
- Acts as a pause or reflection

This post is NOT informational.  
It is emotional and symbolic.

---

### 2) Posting Cadence Rule

- After every **N posts**, publish **one Essence of the Day post**
- Default: **5 + 1** (every 6th post)
- Cadence must be configurable
- Logic must not break existing posting automation

---

### 3) Instagram Grid Awareness (Non-negotiable)

Instagram profiles use a **3-column grid**.

Essence posts must:
- Appear consistently in the **same column**
- Preferably the **first column**
- Create a predictable vertical rhythm when scrolling the profile

Posting order and timing must be designed with grid placement in mind.

---

### 4) Visual Tone (Essence Posts)

Essence posts should:
- Have more breathing space than regular posts
- Feel calmer and less dense
- Avoid headline or news layout patterns
- Optionally omit date text to feel timeless

The goal is visual contrast and emotional grounding.

---

## Already Completed (Do NOT redo)

- **Date padding/alignment fix**  
  This work is DONE, committed, and verified in production.

Do not propose or implement further changes here unless explicitly requested.

---

## What NOT to Build Yet (Phase 10B — PAUSED)

### Reels
- No video generation
- No spotlight animations
- No TTS narration
- No Reel posting pipelines

### Subscriptions
- No subscribe/unsubscribe endpoints
- No email newsletters
- No WhatsApp or channel abstractions

These are intentionally deferred until Phase 10A is complete and validated visually on Instagram.

---

## Constraints

- Automation only — no manual curation
- Minimal, safe, incremental changes
- Do not refactor working pipelines unnecessarily
- Preserve existing posting frequency unless explicitly changed
- Log decisions and edge cases clearly

---

## How to Work (Process Rules)

Before writing code:
1. Explain your understanding of the task
2. Explain how it affects posting order and grid placement
3. Identify edge cases (e.g. low-post days)
4. Ask for confirmation if assumptions are required

Do not implement speculative features.
Do not merge Phase 10B ideas into Phase 10A.

---

## Expected Outputs for Phase 10A

- Automatic generation of Essence of the Day posts
- Correct N+1 posting cadence
- Predictable Instagram grid alignment
- A live profile that feels authored, rhythmic, and human

Only after this is achieved do we proceed to amplification.
