# 🌍 Today in Emojis

**Today's vibe — in five emojis.**
*(Feel the day. Don't read it.)*

[![Live Site](https://img.shields.io/badge/Live-Site-blue)](https://todayinemojis.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Manifesto

> The world no longer asks for your opinion — it asks for your attention.
> Every scroll, every click, every play is a toll on your time.
>
> **Today in Emojis** is a quiet refusal.
> A daily vibe-check of the planet — distilled into five tiny symbols.
> No words. No headlines. No ads.
> Just emotion, felt instantly.
>
> Because you don't owe the world your time.
> But you can still sense its pulse.

---

## What It Does

**Today in Emojis** is a minimalist, AI-powered experiment that captures the world's daily mood in **five emojis**.

Every day at midnight UTC:
- 🤖 **AI scans** top news from BBC, Reuters, The Guardian, and NY Times
- 🎯 **Selects 5 stories** representing diverse topics and global events
- 📰 **Assigns one emoji** to each story that captures its essence
- 🌐 **Updates the site** automatically via GitHub Actions

Each emoji is **clickable** — hover to see the headline, click to read the full story (if you must).

---

## Experience Principles

- **Instant emotion:** Page loads → five emojis appear instantly
- **No scroll:** Everything fits on one screen (desktop & mobile)
- **No text clutter:** Just emojis, reactions, and a subtle link
- **AI-curated:** Smart selection of diverse, important stories
- **Interactive:** Click emojis to read, share your reaction
- **Zero-cost stack:** Runs entirely on free-tier services
- **Privacy-first:** Minimal analytics, no tracking cookies
- **Open-source:** Transparent automation and AI prompts

---

## Features

### 🎨 Core Experience
- **Five Daily Emojis** — AI-selected to represent global news
- **Clickable Links** — Each emoji links to the original news article
- **Hover Tooltips** — See full headline without clicking
- **Reaction Buttons** — Share your vibe: ❤️ Like, 🤔 Neutral, 👎 Dislike
- **Persistent Reactions** — Your reaction saved locally

### 🤖 Automation
- **Daily Updates** — Runs automatically at 00:00 UTC via GitHub Actions
- **AI Selection** — OpenAI GPT-4o-mini analyzes and curates news
- **RSS Aggregation** — Pulls from 4 major news sources
- **Auto-Deployment** — Changes trigger GitHub Pages rebuild

### 📊 Analytics (Phase 8)
- **Google Analytics 4** — Privacy-friendly tracking
- **Custom Events:**
  - `emoji_click` — Which stories people read
  - `reaction_click` — Daily sentiment (Like/Neutral/Dislike)
  - `footer_link_click` — Engagement with project info

### 📸 Instagram Integration (Phase 9)
- **Automated Posting** — Daily posts to Instagram via Graph API
- **Carousel Posts** — Normal posts feature 6 slides:
  - Slide 1: Summary image with all 5 emojis
  - Slides 2-6: Detail images (one emoji + label per slide)
- **Essence Posts** — Single large emoji capturing the day's emotional essence
- **Smart Rendering** — Multi-fallback image generation (Swift, Playwright, Pango/Cairo, Pillow)
- **Duplicate Prevention** — Tracks posted timestamps to avoid re-posting

### 🔒 Security
- **Branch Protection** — Admin-only direct pushes
- **Code Owners** — Automatic review requests
- **Secret Management** — API keys stored as GitHub Secrets
- **Automated Workflows** — Run with minimal permissions

---

## Tech Stack

### Frontend
- **Next.js 15** (App Router) — React framework
- **Tailwind CSS v4** — Styling
- **TypeScript** — Type safety
- **Static Export** — Deployed as pure HTML/CSS/JS

### Backend / Automation
- **Python 3.9+** — Data processing scripts
- **OpenAI API** (GPT-4o-mini) — AI curation
- **GitHub Actions** — Workflow automation
- **RSS Feed Parsing** — News aggregation

### Hosting & Deployment
- **GitHub Pages** — Static site hosting
- **GitHub Actions** — CI/CD pipeline
- **Google Analytics 4** — Usage analytics

### Data Sources
- BBC News World RSS
- Reuters (via Google News)
- The Guardian World RSS
- NY Times World RSS

---

## How It Works

### Daily Workflow

```
1. [00:00 UTC] GitHub Actions triggers daily-emoji.yml
2. Python script fetches 40 headlines (10 from each source)
3. Headlines sent to OpenAI API with strict JSON schema
4. AI selects 5 diverse stories and assigns emojis
5. Script validates response and writes to public/data/today.json
6. Generate Instagram carousel images (6 total):
   - Summary image: All 5 emojis
   - Detail images: One per emoji with label
7. Commit images and data to GitHub
8. Wait 180s for GitHub Pages to deploy images
9. Post to Instagram as carousel (normal) or single image (essence)
10. Site rebuilds with new emojis (no approval needed)
11. New emojis live within 2-3 minutes
```

### Instagram Posting Workflow

**Normal Posts (5x daily):**
```
1. Generate 6 carousel images (summary + 5 details)
2. Upload all 6 to GitHub Pages
3. Wait for deployment
4. Create Instagram carousel container with 6 images
5. Publish carousel post with caption
6. Track timestamp to prevent duplicates
```

**Essence Posts (1x daily at 20:00 UTC):**
```
1. AI analyzes day's 5 emojis to select essence emoji
2. Generate single large essence image
3. Upload to GitHub Pages
4. Create Instagram single-image post
5. Publish with emotion-focused caption
6. No duplicate tracking (always posts)
```

### AI Prompt (Simplified)

> "From these 40 headlines, choose 5 unique, important items across different topics.
> Assign exactly one emoji to each that captures the story's essence.
> Ensure topic diversity (politics, tech, culture, disasters, etc.).
> Return strict JSON with emoji, label, and URL."

---

## Setup & Development

### Prerequisites
- Node.js 20+
- Python 3.9+
- OpenAI API key (for AI curation)
- GitHub account (for deployment)

### Local Development

```bash
# Clone the repo
git clone https://github.com/pareeksourabh/today-in-emojis.git
cd today-in-emojis

# Install dependencies
npm install
pip3 install feedparser

# Run development server
npm run dev

# Visit http://localhost:3000
```

### Run the Emoji Generator Locally

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="sk-..."

# Generate today's emojis
python3 scripts/update_emojis_ai.py

# Check the output
cat public/data/today.json
```

### Generate Instagram Images Locally

```bash
# Generate test carousel (summary + 5 detail images)
python3 scripts/generate_emoji_image.py --test --carousel

# Generate from existing data
python3 scripts/generate_emoji_image.py

# Output images saved to: public/images/daily/
```

**Carousel Image Structure:**
- **Summary image:** `YYYY-MM-DD-HHMM.png` — All 5 emojis on a card
- **Detail images:** `YYYY-MM-DD-HHMM-detail-{1-5}.png` — Individual emoji + label per slide

### Deploy Your Own

1. **Fork this repo**
2. **Add secrets** (Settings → Secrets and variables → Actions):
   - `OPENAI_API_KEY` — Your OpenAI API key
   - `PAT` — Personal Access Token (for auto-deployment)
   - `INSTAGRAM_ACCESS_TOKEN` — Instagram Graph API access token
   - `INSTAGRAM_BUSINESS_ACCOUNT_ID` — Instagram business account ID
3. **Enable GitHub Pages** (Settings → Pages → Deploy from GitHub Actions)
4. **Enable workflows** (Actions → Enable workflows)
5. **Run manually** or wait for midnight UTC

### Manual Firestore Workflow (Alternative Data Source)

If you have pre-curated editions stored in Google Cloud Firestore, you can use the manual workflow to fetch and post them without calling Reuters or OpenAI.

**Setup:**

1. **Add GCP secrets** (Settings → Secrets and variables → Actions):
   - `GCP_SA_KEY_JSON` — Full service account JSON with Firestore read access
   - `GCP_PROJECT_ID` — Your Google Cloud project ID
   - `FIRESTORE_COLLECTION` — Firestore collection name (e.g., "editions")

2. **Create Firestore composite index** (one-time):
   - The workflow will fail with an index creation link on first run
   - Click the link, then "Create Index" button
   - Wait 2-5 minutes for index to build
   - Or manually create index on: `post_type` (Ascending) + `timestamp` (Descending)

3. **Firestore data structure** — Each document should have:
   ```json
   {
     "date": "2025-12-30",
     "timestamp": "2025-12-30T08:33:49Z",
     "post_type": "normal",
     "emojis": [
       {
         "char": "🌍",
         "label": "description",
         "url": "https://...",
         "title": "Headline",
         "summary": "Article summary"
       }
     ]
   }
   ```

4. **Run the workflow:**
   - Go to Actions → "Manual Firestore Update & Instagram Post"
   - Click "Run workflow"
   - Choose whether to skip Instagram posting (for testing)

**What it does:**
- Fetches latest "normal" edition from Firestore (by timestamp DESC)
- Updates `public/data/today.json` with Firestore data
- Generates 6-image carousel (summary + 5 detail images)
- Posts to Instagram (unless skipped)
- No calls to Reuters or OpenAI

**Use cases:**
- Manually curated content
- Pre-approved editions
- Testing with known data
- Emergency posts when AI is unavailable

---

## Project Structure

```
today-in-emojis/
├── app/                      # Next.js App Router
│   ├── layout.tsx           # Root layout with GA4
│   ├── page.tsx             # Main page (emoji display)
│   └── not-found.tsx        # 404 page
├── components/              # React components
│   ├── EmojiRow.tsx        # Emoji display with click tracking
│   ├── Footer.tsx          # Reactions + links with tracking
│   └── GoogleAnalytics.tsx # GA4 integration
├── styles/
│   └── globals.css         # Tailwind styles
├── scripts/
│   ├── update_emojis_ai.py              # AI emoji generator (Reuters + OpenAI)
│   ├── prepare_daily_post.py            # Post type preparation (normal/essence)
│   ├── generate_emoji_image.py          # Image generation (carousel/single)
│   ├── post_to_instagram.py             # Instagram posting (carousel/single)
│   ├── firestore_fetch_latest.py        # Fetch editions from Firestore (manual workflow)
│   └── update_local_json_from_firestore.py  # Update local JSON from Firestore data
├── public/
│   ├── data/
│   │   └── today.json           # Current emoji data (deployed)
│   └── images/
│       └── daily/               # Generated Instagram images
├── data/
│   ├── today.json          # Legacy path
│   └── history.json        # Historical archive
├── .github/
│   ├── workflows/
│   │   ├── daily-emoji.yml                      # Daily update automation (AI)
│   │   ├── daily-emoji-essence.yml              # Daily essence post
│   │   ├── manual_firestore_update_and_post.yml # Manual Firestore workflow
│   │   └── pages.yml                            # Deployment workflow
│   └── CODEOWNERS          # Code review settings
├── docs/                    # Phase documentation
│   ├── phase-1/ ... phase-8/
│   └── ...
├── CHANGELOG.md            # Detailed change history
├── LICENSE                 # MIT License
└── README.md              # This file
```

---

## Analytics & Privacy

### What We Track
- **Page views** — How many times the site is visited
- **Emoji clicks** — Which news stories interest people
- **Reactions** — Daily sentiment (Like/Neutral/Dislike)
- **Footer links** — Engagement with project info

### What We DON'T Track
- No personal information
- No cross-site tracking
- No advertising pixels
- No social media trackers

### Privacy
- IP addresses automatically anonymized by GA4
- First-party cookies only
- GDPR compliant
- Data used solely to improve the experience

---

## Contributing

This is a personal experiment, but contributions are welcome!

### Ways to Contribute
- **Report bugs** — Open an issue
- **Suggest features** — Open an issue with [Feature] tag
- **Improve AI prompts** — Submit a PR with prompt improvements
- **Add data sources** — Suggest new RSS feeds
- **Enhance analytics** — Propose new tracking events

### Guidelines
- Keep it minimal — every feature should serve the core experience
- Respect privacy — no invasive tracking
- Maintain speed — page must load instantly
- Stay free — no paid services in core functionality

---

## History

For detailed development history, see [CHANGELOG.md](CHANGELOG.md).

**Current Phase:** Phase 9 — Instagram Integration & Image Generation (Complete)

### Phase Summary
- **Phase 1-2:** Discovery & Design
- **Phase 3-4:** Architecture & MVP Scaffold
- **Phase 5-6:** Functional Build & Deployment
- **Phase 7:** AI Integration & Automation
- **Phase 8:** Analytics & Monitoring (Complete)
- **Phase 9:** Instagram Integration & Image Generation (Current - WIP)

---

## Inspiration

This project is inspired by:
- The minimalism movement in tech
- Attention economy critiques
- Daily art projects (e.g., Daily Minimal)
- Information diet philosophy
- The power of symbols over words

---

## License

MIT — see [LICENSE](LICENSE).

Feel free to fork, modify, and deploy your own version!

---

## Credits

**Built by Sourabh Pareek**
Concept, design, and implementation captured through iterative development phases.

**Powered by:**
- OpenAI GPT-4o-mini for AI curation
- GitHub Pages for hosting
- Next.js and React for frontend
- Love for minimalism and mindful media consumption

---

## Links

- **Live Site:** https://todayinemojis.com
- **Source Code:** https://github.com/pareeksourabh/today-in-emojis
- **Issues:** https://github.com/pareeksourabh/today-in-emojis/issues

---

**Feel today. Don't read it.** 🌍✨
