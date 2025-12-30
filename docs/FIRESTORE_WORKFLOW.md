# Manual Firestore Workflow Guide

## Overview

This workflow allows you to post pre-curated editions from Google Cloud Firestore to Instagram **without** calling Reuters or OpenAI. Perfect for manually curated content, pre-approved posts, or emergency situations.

## Quick Start

### 1. Setup GCP & Firestore

**A. Create a service account with Firestore read access:**

```bash
# In Google Cloud Console:
1. Go to IAM & Admin → Service Accounts
2. Create a new service account (e.g., "today-in-emojis-reader")
3. Grant role: "Cloud Datastore Viewer" or "Cloud Datastore User"
4. Create a JSON key
5. Download the JSON key file
```

**B. Create required Firestore composite index:**

The workflow query requires a composite index. You have two options:

**Option 1: Create via error link (easiest)**
1. Run the workflow once (it will fail with an index error)
2. Copy the index creation URL from the error message
3. Click the URL to open Firebase Console
4. Click "Create Index" button
5. Wait 2-5 minutes for index to build
6. Re-run the workflow

**Option 2: Create manually**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to Firestore Database → Indexes tab
4. Click "Create Index"
5. Configure:
   - Collection ID: `editions` (or your collection name)
   - Fields to index:
     - `post_type` → Ascending
     - `timestamp` → Descending
   - Query scope: Collection
6. Click "Create"
7. Wait for index to build (status: "Building" → "Enabled")

**Option 3: Use Firebase CLI**
```bash
# Create firestore.indexes.json
{
  "indexes": [
    {
      "collectionGroup": "editions",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "post_type", "order": "ASCENDING" },
        { "fieldPath": "timestamp", "order": "DESCENDING" }
      ]
    }
  ]
}

# Deploy index
firebase deploy --only firestore:indexes
```

**Store the JSON key in GitHub Secrets:**

```
Settings → Secrets and variables → Actions → New repository secret
Name: GCP_SA_KEY_JSON
Value: [paste entire JSON content]
```

### 2. Add Required Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `GCP_SA_KEY_JSON` | Full service account JSON | `{"type": "service_account", ...}` |
| `GCP_PROJECT_ID` | Your GCP project ID | `my-project-123` |
| `FIRESTORE_COLLECTION` | Firestore collection name | `editions` |
| `INSTAGRAM_ACCESS_TOKEN` | Instagram API token (existing) | Already set |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID` | Instagram account ID (existing) | Already set |

### 3. Firestore Data Structure

Each document in your Firestore collection should follow this schema:

```json
{
  "date": "2025-12-30",
  "timestamp": "2025-12-30T08:33:49Z",
  "post_type": "normal",
  "emojis": [
    {
      "char": "🌍",
      "label": "china military drills near taiwan",
      "url": "https://www.nytimes.com/...",
      "title": "China Mobilizes Forces Near Taiwan for Live-Fire Drill",
      "summary": "The exercises ended months of relative calm..."
    },
    {
      "char": "👩‍⚕️",
      "label": "bangladesh's first female pm dies",
      "url": "https://www.bbc.com/...",
      "title": "Bangladesh's first female prime minister...",
      "summary": "For decades, Zia and ousted PM Sheikh Hasina..."
    }
    // ... 3 more emojis (total 5)
  ]
}
```

**Required fields:**
- `date` (string): ISO date format (YYYY-MM-DD)
- `timestamp` (string): ISO timestamp with timezone (YYYY-MM-DDTHH:MM:SSZ)
- `post_type` (string): Must be "normal"
- `emojis` (array): Exactly 5 emoji objects

**Each emoji object requires:**
- `char` (string): The emoji character
- `label` (string): Short description (lowercase, for caption)
- `url` (string): Source article URL (optional but recommended)
- `title` (string): Article headline (optional but recommended)
- `summary` (string): Article summary (optional but recommended)

### 4. Run the Workflow

**Via GitHub UI:**

1. Go to your repository
2. Click **Actions** tab
3. Select **"Manual Firestore Update & Instagram Post"** workflow
4. Click **"Run workflow"** dropdown
5. Choose branch: `main`
6. Choose whether to skip Instagram posting:
   - `false` = Normal run (fetch, generate images, post to Instagram)
   - `true` = Test mode (fetch and generate images only, skip Instagram)
7. Click **"Run workflow"** button

**What happens:**

```
1. ✓ Checkout repository
2. ✓ Setup Python and dependencies
3. ✓ Write GCP credentials to file
4. ✓ Fetch latest normal edition from Firestore
5. ✓ Update public/data/today.json
6. ✓ Prepare normal post
7. ✓ Generate 6 carousel images (summary + 5 details)
8. ✓ Commit and push changes
9. ✓ Wait 180s for GitHub Pages
10. ✓ Post to Instagram (if not skipped)
11. ✓ Commit Instagram log
12. ✓ Cleanup credentials
```

## Workflow Details

### Query Logic

The workflow fetches the **latest normal edition** using this Firestore query:

```python
collection(FIRESTORE_COLLECTION)
  .where('post_type', '==', 'normal')
  .order_by('timestamp', direction='DESCENDING')
  .limit(1)
```

**Important:** Ensure your Firestore collection has a composite index for:
- `post_type` (ascending)
- `timestamp` (descending)

### File Updates

The workflow updates these local files:

1. **`public/data/today.json`** - Main data file (used by website)
2. **`data/history.json`** - Historical archive (last 30 entries)
3. **`public/images/daily/*.png`** - Generated carousel images (6 images)
4. **`data/instagram_posted.json`** - Instagram posting log (if posted)

### Generated Images

For each run, **6 images** are generated:

1. **Summary image** (`YYYY-MM-DD-HHMM.png`):
   - All 5 emojis on a white card
   - Date in top-left corner
   - Clean, minimalist design

2. **Detail images** (`YYYY-MM-DD-HHMM-detail-{1-5}.png`):
   - One emoji per image
   - Label text below emoji
   - Pure white background
   - Premium, minimal design

### Instagram Post

The workflow creates a **6-slide carousel post** with:

- **Slide 1:** Summary (all 5 emojis)
- **Slides 2-6:** Individual emoji + label

**Caption format:**
```
Today's vibe 🌍 👩‍⚕️ 💼 🚨 🌍

Feel the day. Don't read it.

🌍 China military drills near taiwan
👩‍⚕️ Bangladesh's first female pm dies
💼 Trump claims us hit venezuelan facility
🚨 Train derailment in mexico kills 13
🌍 More than 3000 migrants died in 2025

#TodayInEmojis #DailyVibes #NewsInEmojis #Minimalism #FiveEmojis #WorldNews #DailyMood

todayinemojis.com
```

## Error Handling

### Workflow Fails Before Instagram Posting If:

1. **Firestore fetch fails:**
   - Invalid credentials
   - Collection doesn't exist
   - No normal editions found
   - Network error

2. **Data validation fails:**
   - Missing required fields
   - Wrong number of emojis (not 5)
   - Invalid data types

3. **Image generation fails:**
   - Playwright installation failed
   - Missing system fonts
   - Disk space issues

**Result:** Workflow exits with error code 1, no Instagram post is made

### Non-Critical Failures (Continue):

1. **History update fails:**
   - Workflow continues (non-critical)
   - Warning logged

2. **Instagram post fails:**
   - Marked as `continue-on-error: true`
   - Images still committed to repo
   - Log still updated

## Testing

### Test Mode (Skip Instagram)

Run the workflow with `skip_instagram: true` to:

- ✓ Test Firestore connection
- ✓ Validate data format
- ✓ Generate images
- ✓ Commit to repository
- ✗ Skip Instagram posting

**Perfect for:**
- Validating Firestore setup
- Testing image generation
- Dry-run before production

### Local Testing

You can test the scripts locally:

```bash
# 1. Install dependencies
pip install google-cloud-firestore

# 2. Set environment variables
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/gcp-sa.json"
export GCP_PROJECT_ID="your-project-id"
export FIRESTORE_COLLECTION="editions"

# 3. Fetch from Firestore
python scripts/firestore_fetch_latest.py

# 4. Update local JSON
python scripts/update_local_json_from_firestore.py

# 5. Verify
cat public/data/today.json
```

## Comparison: AI vs. Firestore Workflows

| Feature | AI Workflow (daily-emoji.yml) | Firestore Workflow (manual) |
|---------|-------------------------------|----------------------------|
| **Trigger** | Cron schedule (5x daily) | Manual (workflow_dispatch) |
| **Data Source** | Reuters RSS + OpenAI | Google Cloud Firestore |
| **API Calls** | Yes (Reuters, OpenAI) | Yes (Firestore read-only) |
| **Cost** | OpenAI API usage | Firestore read operations |
| **Control** | Automated AI selection | Manually curated content |
| **Approval** | None (auto-posts) | Manual trigger required |
| **Use Case** | Daily automation | Special posts, emergencies |

## Troubleshooting

### "Firestore query failed: 400 The query requires an index"

**Cause:** Missing composite index for the query (post_type + timestamp)

**Fix (Easiest):**
1. The error message contains a direct link to create the index
2. Copy the URL from the error (looks like: `https://console.firebase.google.com/v1/r/project/.../firestore/indexes?create_composite=...`)
3. Open the URL in your browser
4. Click "Create Index" button
5. Wait 2-5 minutes for the index to build (status will show "Building" then "Enabled")
6. Re-run the workflow

**Alternative Fix (Manual):**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project → Firestore Database → Indexes
3. Click "Create Index"
4. Set:
   - Collection: Your collection name (e.g., "editions")
   - Field 1: `post_type` (Ascending)
   - Field 2: `timestamp` (Descending)
5. Click "Create" and wait for it to build

**Note:** This is a **one-time setup**. Once the index is created, the workflow will work indefinitely.

### "Firestore query failed: 403 Permission Denied"

**Cause:** Service account lacks Firestore read permission

**Fix:**
1. Go to GCP Console → IAM & Admin → IAM
2. Find your service account
3. Add role: "Cloud Datastore Viewer" or "Cloud Datastore User"
4. Wait 1-2 minutes for propagation

### "No normal editions found in Firestore"

**Cause:** Collection is empty or no documents with `post_type: "normal"`

**Fix:**
1. Verify collection name in `FIRESTORE_COLLECTION` secret
2. Check Firestore console for documents
3. Ensure at least one document has `post_type: "normal"`
4. Verify `timestamp` field exists and is sortable

### "Edition missing 'emojis' field"

**Cause:** Document doesn't match expected schema

**Fix:**
1. Check document structure in Firestore console
2. Ensure `emojis` field is an array with 5 objects
3. Validate each emoji has `char` and `label` fields

### "Image not accessible after 10 attempts"

**Cause:** GitHub Pages hasn't deployed images yet

**Fix:**
- Workflow waits 180 seconds (3 minutes)
- If still failing, increase wait time in workflow
- Check GitHub Pages deployment status

### "Instagram posting failed: 400 Bad Request"

**Cause:** Invalid Instagram credentials or carousel format

**Fix:**
1. Verify `INSTAGRAM_ACCESS_TOKEN` is valid (check expiration)
2. Verify `INSTAGRAM_BUSINESS_ACCOUNT_ID` is correct
3. Check Instagram Graph API status
4. Review workflow logs for specific error message

## Security Notes

- ✓ Service account credentials are write-only in GitHub Secrets
- ✓ Credentials are written to `./gcp-sa.json` with `chmod 600`
- ✓ Credentials are deleted after workflow completes (even on failure)
- ✓ Firestore access is **read-only** (no writes to cloud)
- ✓ All changes are committed with git attribution

## FAQ

**Q: Can I schedule this workflow to run automatically?**

A: Yes, but it's not recommended. Add a `schedule` trigger to the workflow YAML if needed. However, the design intent is manual triggering for curated content.

**Q: Can I use this for essence posts?**

A: Not currently. The workflow queries for `post_type: "normal"` only. Essence posts still use the AI workflow.

**Q: What if I have multiple normal editions with the same timestamp?**

A: The workflow fetches the first one returned by Firestore (order is not guaranteed if timestamps are identical). Use unique timestamps.

**Q: Can I test without Instagram credentials?**

A: Yes! Run with `skip_instagram: true` to test everything except posting to Instagram.

**Q: How do I add more than 5 emojis?**

A: The current design expects exactly 5 emojis (for Instagram carousel compatibility). To change this, you'd need to modify the image generation and Instagram posting code.

## Support

For issues or questions:
- Check workflow logs in GitHub Actions
- Review Firestore console for data validation
- Test scripts locally with provided commands
- Open an issue on GitHub with workflow run ID

---

**Ready to post?** Go to Actions → "Manual Firestore Update & Instagram Post" → Run workflow! 🚀
