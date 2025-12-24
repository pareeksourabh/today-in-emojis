# Today in Emojis — Phase 10C: Cloud Content Store + Hybrid Migration

## Purpose
Improve asset quality and long-term scalability while keeping disruption low.

- Cloud becomes the **Source of Truth** for content (“editions”) and assets.
- GitHub remains:
  - code repo
  - orchestration (initially)
  - static website hosting
- The website remains **100% static** by consuming a daily exported JSON committed into the repo.

This phase is designed to enable subscriptions next (PII never in GitHub).

---

## Principles
1) **Cloud is SoT** for:
   - daily editions (emoji news + essence)
   - render metadata
   - asset URLs
2) **GitHub is a cache/export** for the static website:
   - last-30-days.json committed once/day
3) **Parallel run first**:
   - no disruptions while we validate quality and correctness
4) **Minimal retention**:
   - assets retained 30 days (auto deletion)
   - website shows last 30 days
5) **PII rule**:
   - subscriber data never enters GitHub (repo or secrets as a datastore)

---

## Target Architecture (End State)
### Producer (Cloud Scheduled Job)
- Fetch news
- Generate edition content (emojis + summaries + essence)
- Render images (normal + essence)
- Store:
  - edition JSON in cloud database
  - images in cloud object storage (30-day lifecycle)
- Return public asset URLs

### Instagram Poster (Cutover)
- Posts to Instagram from cloud-generated assets (URL download/upload if needed)

### Website Exporter (GitHub Actions)
- Runs once/day
- Fetches last 30 days of editions from cloud
- Writes `public/last-30-days.json` (or equivalent)
- Commits JSON only
- Static site reads from this file (no browser calls to cloud)

---

## Migration Order (Agreed)
### Step 1 — Parallel Cloud Build (No user-visible change)
- Cloud producer runs independently:
  - generates images 5x/day + 1 essence/day
  - stores images in cloud storage
  - stores editions in cloud database
- Existing GitHub pipeline continues to:
  - generate images the old way
  - post to Instagram the old way
  - keep website unchanged

**Goal:** Validate image quality + data correctness in cloud for 7–14 days.

---

### Step 2 — Cutover Instagram to Cloud (Website unchanged)
- Switch Instagram posting to use cloud-generated assets.
- Website still uses old GitHub data until Step 3.

Temporary mismatch is acceptable:
- Instagram may show “cloud edition”
- Website may show “github edition”

**Goal:** Improve public-facing quality immediately while keeping the site stable.

---

### Step 3 — Cutover Website to Cloud Export (Static)
- Add/enable a GitHub Action that exports last 30 days from cloud once/day.
- Commit JSON export only (no images).
- Update site to read `last-30-days.json`.

After this:
- Instagram and website both reflect cloud SoT.

---

## Retention Policy
- Cloud storage objects auto-delete after 30 days.
- Website displays last 30 days from exported JSON.
- If an asset URL 404s (expired), site must degrade gracefully.

---

## Definition of Done (Phase 10C Complete)
- Cloud database contains editions as SoT
- Cloud storage contains assets with 30-day lifecycle deletion
- Instagram posts use cloud assets
- GitHub repo no longer stores images
- Website shows last 30 days via committed JSON export
- Clear docs exist for local testing + safe rollback

---

## Rollback Strategy
- Step 1: No rollback needed (parallel only)
- Step 2: Re-point IG poster back to old generator if cloud fails
- Step 3: Re-point site to old “today-only” data source if export fails
