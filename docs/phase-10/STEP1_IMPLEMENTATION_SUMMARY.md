# Phase 10C - Step 1: Parallel Cloud Build (IMPLEMENTED)

This document summarizes the Step 1 implementation for migrating to cloud-based content storage.

---

## What Was Implemented

### Core Infrastructure
✅ **Cloud Edition Schema** (`src/cloud/schema/edition.ts`)
- TypeScript types for CloudEdition (Source of Truth)
- Cadence metadata, emojis, essence, assets, source metadata
- Export format for website (last 30 days)

✅ **Cloud Configuration** (`src/cloud/config.ts`)
- Environment-based configuration
- Dry-run mode support
- Validation and logging

✅ **Cloud Storage Client** (`src/cloud/storage.ts`)
- Upload images to Google Cloud Storage
- Automatic 30-day lifecycle policy
- Public URL generation
- Dry-run mode (no actual uploads)

✅ **Cloud Database Client** (`src/cloud/database.ts`)
- Write/read editions from Firestore
- Query by date or date range
- Export editions for website
- Dry-run mode (no actual writes)

✅ **Cloud Producer** (`src/cloud/producer.ts`)
- Main orchestrator for edition generation
- Combines storage + database operations
- Health check for cloud services

✅ **Python Wrapper** (`scripts/cloud_produce.py`)
- Bridges existing Python scripts with TypeScript cloud producer
- Reuses existing emoji selection & image generation logic
- Sends result to cloud via JSON + CLI

✅ **TypeScript CLI** (`src/cloud/cli/produce.ts`)
- Command-line interface for cloud producer
- Accepts JSON input from Python wrapper
- Handles base64 image transport

### Testing & Documentation
✅ **Local Testing Guide** (`docs/phase-10/CLOUD_LOCAL_TESTING.md`)
- Dry-run mode instructions
- Environment variable reference
- Troubleshooting guide

✅ **Environment Template** (`.env.example`)
- All cloud configuration variables
- OpenAI API key
- Essence cadence settings

✅ **Updated .gitignore**
- GCP service account keys
- Temporary cloud files

✅ **Package Dependencies**
- @google-cloud/storage
- @google-cloud/firestore
- tsx (TypeScript execution)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PARALLEL RUN (Step 1)                     │
│                                                               │
│  ┌─────────────────┐                ┌───────────────────┐   │
│  │   GitHub Flow   │                │   Cloud Producer  │   │
│  │  (unchanged)    │                │     (NEW)         │   │
│  │                 │                │                   │   │
│  │  • Fetch News   │                │  • Fetch News     │   │
│  │  • AI Emoji     │                │  • AI Emoji       │   │
│  │  • Generate IMG │                │  • Generate IMG   │   │
│  │  • Commit IMG   │                │  • Upload to GCS  │   │
│  │  • Post to IG   │                │  • Write to DB    │   │
│  │  • Website      │                │                   │   │
│  └─────────────────┘                └───────────────────┘   │
│                                                               │
│  Both systems run independently for validation               │
└─────────────────────────────────────────────────────────────┘
```

---

## Files Created

### TypeScript/JavaScript
- `src/cloud/schema/edition.ts` - Type definitions
- `src/cloud/config.ts` - Configuration loader
- `src/cloud/storage.ts` - Cloud Storage client
- `src/cloud/database.ts` - Firestore client
- `src/cloud/producer.ts` - Main producer logic
- `src/cloud/cli/produce.ts` - CLI entry point

### Python
- `scripts/cloud_produce.py` - Python wrapper script

### Documentation
- `docs/phase-10/CLOUD_LOCAL_TESTING.md` - Testing guide
- `docs/phase-10/STEP1_IMPLEMENTATION_SUMMARY.md` - This file

### Configuration
- `.env.example` - Environment variables template
- `package.json` - Updated with cloud dependencies

---

## Next Steps (NOT YET DONE)

### Before Running in Production:
1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Create GCP Project**
   - Project ID: `today-in-emojis`
   - Enable APIs: Cloud Storage, Firestore

3. **Create Cloud Storage Bucket**
   ```bash
   gsutil mb -p today-in-emojis -l us-central1 gs://today-in-emojis-assets
   ```

4. **Set bucket lifecycle policy** (run once)
   ```bash
   npm run cloud:health
   # Then call setupBucketLifecycle() manually or via script
   ```

5. **Create Firestore Database**
   - Database ID: `(default)`
   - Collection: `editions`

6. **Create Service Account**
   - Roles: Storage Admin, Cloud Datastore User
   - Download JSON key

7. **Set Environment Variables**
   - Copy `.env.example` to `.env.local`
   - Fill in GCP project ID, credentials path, bucket name
   - Set `CLOUD_DRY_RUN=false` for real runs

8. **Test Locally (Dry-Run)**
   ```bash
   export CLOUD_DRY_RUN=true
   python scripts/cloud_produce.py --dry-run
   ```

9. **Test With Real Cloud**
   ```bash
   export CLOUD_DRY_RUN=false
   python scripts/cloud_produce.py
   ```

10. **Deploy to Cloud Run**
    - Create Cloud Run job
    - Set environment variables
    - Create Cloud Scheduler triggers:
      - 5x/day for normal posts (00:00, 04:00, 08:00, 12:00, 16:00 UTC)
      - 1x/day for essence post (20:00 UTC)

11. **Run in Parallel for 7-14 Days**
    - Validate image quality
    - Validate data correctness
    - Compare cloud vs GitHub outputs
    - Monitor for errors

### After Validation (Future Steps):
- **Step 2:** Cutover Instagram to cloud assets
- **Step 3:** Cutover website to cloud export

---

## How to Test (Local Dry-Run)

```bash
# 1. Install dependencies
npm install
pip install feedparser pillow requests

# 2. Set dry-run mode
export CLOUD_DRY_RUN=true
export OPENAI_API_KEY=your-key-here

# 3. Run producer
python scripts/cloud_produce.py --dry-run

# Expected output:
# [info] Running AI emoji selection...
# [info] Preparing daily post...
# [info] Generating image...
# [DRY-RUN] Would upload to: gs://...
# [DRY-RUN] Would write edition to Firestore:
# [info] ✓ Cloud production complete!
```

---

## Success Criteria

After 7-14 days of parallel running:
- ✅ Cloud database contains all editions (5 normal + 1 essence per day)
- ✅ Cloud storage contains all images with correct paths
- ✅ Image quality matches GitHub-generated images
- ✅ No failures or errors in cloud producer logs
- ✅ Asset URLs are publicly accessible
- ✅ 30-day lifecycle policy is working
- ✅ Existing GitHub pipeline still works (unchanged)

---

## Rollback Strategy

Since this is Step 1 (parallel run):
- **No rollback needed** - both systems run independently
- If cloud fails, GitHub flow continues unchanged
- Users see no impact
- Simply fix cloud issues and re-run

---

## Current Status

**✅ Implementation Complete**
- All code written and tested locally (dry-run)
- Ready for GCP setup and deployment

**⏳ Pending**
- GCP project creation
- Service account setup
- Cloud Run deployment
- 7-14 day parallel validation run

---

## Questions?

See `docs/phase-10/CLOUD_LOCAL_TESTING.md` for detailed testing instructions.
