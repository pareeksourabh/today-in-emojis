# Codex Context — Today in Emojis (Phase 3)

You are working inside the Today in Emojis repository.

## Product intent
We generate daily emoji-based news summaries and post them. The current output looks bot-run. Phase 3 adds human polish, Reels, and an owned subscriber channel.

## What to build next (Phase 3)
1) **Image polish**: shift the date text slightly right with left padding so the date aligns visually with the first emoji column.
2) **Reels**: generate 1–2 short (5–10s) vertical videos per day.
   - 5 emojis on screen
   - highlight/spotlight one emoji at a time in sequence
   - add voice narration (TTS for now) that matches the emoji sequence
   - auto-post as Instagram Reels (fallback to silent video if audio fails)
3) **Subscription manager**:
   - user can subscribe/unsubscribe
   - start with email newsletter (daily)
   - design must be multi-channel-ready so we can later switch the same subscriber base to WhatsApp
   - include a channel abstraction (EmailChannel implemented, WhatsAppChannel stubbed)

## Constraints
- Prioritize automation and reliability. No manual editing.
- Keep visuals clean and consistent with existing brand.
- Keep Phase 3 changes modular: separate reels pipeline from images pipeline where sensible.
- Add logging, sane defaults, and configuration toggles (e.g., reels_per_day, duration, fps).

## Outputs expected
- Updated image generator with date alignment fix.
- New reel generator producing mp4 + metadata.
- Posting automation for reels.
- Subscription endpoints + storage + daily HTML email sender.
- Documentation updates explaining how to run each pipeline locally.
