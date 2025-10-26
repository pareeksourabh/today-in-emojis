# Phase 7 — Automation (AI)

## Goal
Use an LLM to pick the day’s 5 most important and diverse stories from public RSS headlines and assign a single emoji to each. Output is `data/today.json`.

## How it works
- GitHub Actions (daily cron) runs `scripts/update_emojis_ai.py`.
- The script fetches ~40 headlines from BBC/Reuters/Guardian/AP.
- Claude 3.5 Sonnet selects 5 diverse items and returns strict JSON: `[{"emoji","label","url"} × 5]`.
- The script validates JSON and URLs (must match inputs), writes `data/today.json`, and appends `data/history.json`.

## Secrets
- Add `ANTHROPIC_API_KEY` under **Settings → Secrets and variables → Actions**.
- Optional: switch to OpenAI by setting `PROVIDER="openai"` in the script and adding `OPENAI_API_KEY`.

## Safety & Fallbacks
- Strict schema validation; one retry on parse failure.
- If the model fails, we write a neutral `fallback` payload for the day (site won’t break).
