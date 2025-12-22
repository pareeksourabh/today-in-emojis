# Phase 3 Tickets (copy into GitHub Issues)

## P10-A1 — Align date padding in image template
- Shift date text right; align with first emoji column
- Verify on multiple sample outputs
- Update tests/examples if present

## P10-B1 — Reel layout spec
- Define positions for emojis, title/date (if any), and spotlight overlay
- Define timing per emoji and total duration (5–10s)

## P10-B2 — Frame generator for reels
- Generate frames (Pillow or equivalent)
- Maintain same visual identity as static images

## P10-B3 — Spotlight animation
- Implement highlight per emoji in sequence
- Subtle scale/pulse + vignette/spotlight overlay

## P10-B4 — TTS narration
- Build script for 5 emojis
- Generate audio (TTS) with a consistent voice
- Handle failures (fallback to silent reel)

## P10-B5 — Video composition
- Assemble frames into mp4
- Merge audio + video via ffmpeg
- Ensure vertical format 1080x1920 and codec compatibility

## P10-B6 — Auto-post Reels
- Add scheduled job for 1–2 reels/day
- Retry + logging + safe failure modes

## P10-C1 — Subscription storage + API
- Subscribe endpoint + unsubscribe endpoint
- Store subscriber status + timestamps
- Capture consent basics

## P10-C2 — Email newsletter template
- HTML email template optimized for mobile
- Render daily content from pipeline outputs

## P10-C3 — Daily newsletter sender
- Send to active subscribers daily
- Track success/failure

## P10-C4 — Channel abstraction
- Implement EmailChannel
- Stub WhatsAppChannel with interface + TODOs (no sending yet)
