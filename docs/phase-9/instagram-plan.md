# Phase 9: Instagram Integration & Image Generation

**Status:** WIP (Work in Progress)
**Started:** 2025-11-19
**Goal:** Automatically generate emoji images and post to Instagram daily

---

## Overview

Extend the daily automation workflow to:
1. Generate a visual image containing the 5 daily emojis
2. Automatically post the image to Instagram
3. Expand reach beyond the website to social media

This phase transforms Today in Emojis from a web-only experience into a multi-platform daily vibe-check.

---

## Technical Architecture

### Components

```
Daily Workflow (Enhanced):
1. [00:00 UTC] GitHub Actions triggers
2. Python fetches headlines (existing)
3. AI selects 5 emojis (existing)
4. ✨ NEW: Generate image from emojis
5. ✨ NEW: Post image to Instagram
6. Commit and deploy to GitHub Pages (existing)
```

### Tech Stack Additions

**Image Generation:**
- **Pillow (PIL)** - Python imaging library
- Canvas: 1080x1080px (Instagram square format)
- Format: PNG with transparency support

**Instagram Integration:**
- **Instagram Graph API** - Facebook's official API
- **Requests** library for HTTP calls
- Long-lived access tokens (60-day refresh)

---

## Implementation Plan

### Step 1: Image Generation Script

**File:** `scripts/generate_emoji_image.py`

**Features:**
- Read from `public/data/today.json`
- Generate 1080x1080px canvas
- Render 5 emojis in artistic layout
- Add date watermark
- Optional: Add subtle branding/tagline
- Save to `public/images/today-YYYY-MM-DD.png`

**Design Principles:**
- Minimal, clean aesthetic (matching website)
- High contrast for mobile viewing
- Instant emotional impact
- No text clutter (emojis speak for themselves)

**Layout Options:**
1. **Horizontal Row:** 5 emojis in a line (simple, clean)
2. **Grid:** 2x2 + 1 center (balanced)
3. **Artistic:** Scattered with varying sizes (dynamic)

**Dependencies:**
```bash
pip install pillow
```

---

### Step 2: Instagram API Setup

**Prerequisites:**
1. Convert Instagram account to Business/Creator account
2. Create Facebook Page and link to Instagram
3. Create Facebook Developer App
4. Generate access tokens

**Required Secrets (GitHub Actions):**
- `INSTAGRAM_ACCESS_TOKEN` - Long-lived user access token
- `INSTAGRAM_BUSINESS_ACCOUNT_ID` - Instagram business account ID

**API Endpoints:**
- Container Creation: `/media`
- Container Publishing: `/media_publish`

**Process:**
1. Upload image to Instagram (create media container)
2. Add caption with emoji labels and hashtags
3. Publish container to feed

---

### Step 3: Instagram Posting Script

**File:** `scripts/post_to_instagram.py`

**Features:**
- Read image path and emoji data
- Upload to Instagram Graph API
- Generate caption from emoji labels
- Add relevant hashtags
- Handle rate limits (25 posts/day)
- Implement error handling and retries
- Log success/failure

**Caption Template:**
```
Today's vibe 🌍

[emoji labels as text]

#TodayInEmojis #DailyVibes #EmotionalIntelligence #Minimalism #NewsInEmojis

todayinemojis.com
```

**Error Handling:**
- API failures: Log error, save image for manual posting
- Rate limits: Respect Instagram limits
- Invalid tokens: Alert via workflow output

---

### Step 4: GitHub Actions Workflow Update

**File:** `.github/workflows/daily-emoji.yml`

**New Steps:**
```yaml
- name: Install image dependencies
  run: pip install pillow requests

- name: Generate emoji image
  run: python scripts/generate_emoji_image.py

- name: Post to Instagram
  env:
    INSTAGRAM_ACCESS_TOKEN: ${{ secrets.INSTAGRAM_ACCESS_TOKEN }}
    INSTAGRAM_BUSINESS_ACCOUNT_ID: ${{ secrets.INSTAGRAM_BUSINESS_ACCOUNT_ID }}
  run: python scripts/post_to_instagram.py
  continue-on-error: true  # Don't fail workflow if Instagram fails

- name: Commit images
  run: |
    git add public/images/*.png || true
    git commit -m "chore(auto): Generated image $(date -u +'%Y-%m-%d')" || echo "No new images"
    git push
```

**Workflow Logic:**
1. Only generate image if emoji selection successful
2. Only post to Instagram if image generation successful
3. Continue workflow even if Instagram posting fails
4. Commit generated images to repo (for archival)

---

### Step 5: Alternative Approaches

**Option A: Instagram Graph API (Recommended)**
- ✅ Full automation
- ✅ Business account features
- ⚠️ Requires Facebook Developer setup
- ⚠️ Token refresh every 60 days

**Option B: Instagram Basic Display API**
- ✅ Simpler OAuth
- ❌ Limited to user posts only
- ❌ Cannot post media (read-only for most use cases)
- ❌ Not suitable for automation

**Option C: Third-Party Services**
- Buffer API, Later.com API
- ✅ Easier setup
- ❌ Paid services (not free-tier)
- ❌ Against "zero-cost stack" principle

**Option D: Manual Posting (Fallback)**
- Generate images automatically
- Save to `public/images/archive/`
- Post manually when convenient
- ✅ No API complexity
- ❌ Not fully automated

---

## Image Design Specifications

### Canvas
- **Size:** 1080x1080px (Instagram square)
- **Background:** Gradient or solid (match website theme)
- **Format:** PNG (supports transparency)

### Emojis
- **Size:** 180-220px each (large, impactful)
- **Arrangement:** Horizontal row with equal spacing
- **Padding:** 80px margins

### Typography
- **Date:** Top-right corner, subtle
- **Tagline (optional):** "Today's vibe" at top
- **Font:** System font (Arial/Helvetica)
- **Size:** 32-48px for text, 180-220px for emojis

### Color Scheme
- **Background:** White (#FFFFFF) or subtle gradient
- **Text:** Dark gray (#333333)
- **Accent:** Match website (minimal color)

### Example Layout
```
┌─────────────────────────────────┐
│  Today's vibe        2025-11-19 │
│                                  │
│                                  │
│    🌍  💡  🤝  🌱  😐          │
│                                  │
│                                  │
│                                  │
│         todayinemojis.com        │
└─────────────────────────────────┘
```

---

## Privacy & Compliance

**Instagram Requirements:**
- Must comply with Instagram Terms of Service
- Cannot automate user actions (likes, follows)
- Posting own content is permitted
- Respect rate limits (25 posts/day)

**Data Handling:**
- No personal data collected
- Images generated from public news data
- Same privacy principles as website

---

## Testing Strategy

### Local Testing
1. Generate test images with sample emoji data
2. Verify image quality and layout
3. Test Instagram API with test account
4. Validate caption formatting

### Production Testing
1. Use `workflow_dispatch` to trigger manually
2. Monitor first few automated posts
3. Check Instagram post quality
4. Verify workflow error handling

---

## Success Metrics

**Technical:**
- ✅ Images generated successfully every day
- ✅ Instagram posts published automatically
- ✅ Workflow completes without errors
- ✅ Images archived in repository

**Engagement (Optional Monitoring):**
- Instagram followers
- Post engagement (likes, comments)
- Website traffic from Instagram
- Cross-platform brand awareness

---

## Maintenance & Monitoring

**Token Refresh:**
- Instagram access tokens expire after 60 days
- Set calendar reminder to refresh tokens
- Document token refresh process
- Consider automating token refresh

**Error Monitoring:**
- Check GitHub Actions logs weekly
- Set up notifications for workflow failures
- Monitor Instagram API deprecations

**Content Quality:**
- Periodically review generated images
- Adjust design if needed
- Ensure emojis render correctly

---

## Documentation Requirements

**Setup Guide:** `docs/phase-9/setup-instagram.md`
- Step-by-step Instagram Business account setup
- Facebook Developer App configuration
- Access token generation
- GitHub Secrets configuration

**Troubleshooting:** `docs/phase-9/troubleshooting.md`
- Common errors and solutions
- Token expiration handling
- Image generation issues
- Instagram API error codes

**Design Guide:** `docs/phase-9/image-design.md`
- Design specifications
- Color palette
- Typography guidelines
- Layout variations

---

## Future Enhancements (Post-Phase 9)

**Phase 9.1 - Enhanced Visuals:**
- Multiple layout templates
- Seasonal themes
- Dynamic backgrounds
- Story format (1080x1920px)

**Phase 9.2 - Multi-Platform:**
- Twitter/X integration
- Threads integration
- Bluesky integration
- RSS feed with images

**Phase 9.3 - Analytics:**
- Instagram Insights API
- Cross-platform engagement tracking
- Popular emoji patterns
- Optimal posting times

---

## Dependencies

**Python Packages:**
```
pillow>=10.0.0      # Image generation
requests>=2.31.0    # HTTP requests for Instagram API
python-dotenv>=1.0  # Environment variables (local testing)
```

**External Services:**
- Instagram Business Account (free)
- Facebook Developer Account (free)
- Facebook Page (free)

**GitHub Secrets:**
- `INSTAGRAM_ACCESS_TOKEN` (generated from Facebook Developer)
- `INSTAGRAM_BUSINESS_ACCOUNT_ID` (from Instagram account)

---

## Risk Assessment

**Low Risk:**
- Image generation (controlled, local)
- Archival of generated images

**Medium Risk:**
- Instagram API changes
- Token expiration
- Rate limiting

**Mitigation:**
- Continue-on-error for Instagram steps
- Manual fallback option
- Comprehensive error logging
- Regular token refresh reminders

---

## Timeline Estimate

**Setup:** 2-3 hours
- Instagram Business account setup
- Facebook Developer App setup
- Token generation

**Development:** 4-6 hours
- Image generation script: 2-3 hours
- Instagram posting script: 2-3 hours

**Integration:** 1-2 hours
- Workflow updates
- Testing and debugging

**Documentation:** 1-2 hours
- Setup guides
- Troubleshooting docs

**Total:** ~8-13 hours for complete implementation

---

## Checklist

### Setup
- [ ] Create Instagram Business account
- [ ] Create Facebook Page and link to Instagram
- [ ] Create Facebook Developer App
- [ ] Generate long-lived access token
- [ ] Add secrets to GitHub repository

### Development
- [ ] Create `scripts/generate_emoji_image.py`
- [ ] Create `scripts/post_to_instagram.py`
- [ ] Test image generation locally
- [ ] Test Instagram posting with test account

### Integration
- [ ] Update `.github/workflows/daily-emoji.yml`
- [ ] Add image generation step
- [ ] Add Instagram posting step
- [ ] Test workflow end-to-end

### Documentation
- [ ] Create setup guide
- [ ] Create troubleshooting guide
- [ ] Update README.md with Instagram link
- [ ] Update CHANGELOG.md

### Deployment
- [ ] Run first automated post
- [ ] Monitor for errors
- [ ] Adjust design if needed
- [ ] Set token refresh reminder

---

**Next Steps:** Begin with Instagram account setup and image generation script development.
