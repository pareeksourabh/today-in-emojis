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
6. Commit triggers Pages deployment workflow
7. Site rebuilds with new emojis (no approval needed)
8. New emojis live within 2-3 minutes
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

### Deploy Your Own

1. **Fork this repo**
2. **Add secrets** (Settings → Secrets and variables → Actions):
   - `OPENAI_API_KEY` — Your OpenAI API key
   - `PAT` — Personal Access Token (for auto-deployment)
3. **Enable GitHub Pages** (Settings → Pages → Deploy from GitHub Actions)
4. **Enable workflows** (Actions → Enable workflows)
5. **Run manually** or wait for midnight UTC

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
│   └── update_emojis_ai.py # AI emoji generator
├── public/
│   └── data/
│       └── today.json      # Current emoji data (deployed)
├── data/
│   ├── today.json          # Legacy path
│   └── history.json        # Historical archive
├── .github/
│   ├── workflows/
│   │   ├── daily-emoji.yml # Daily update automation
│   │   └── pages.yml       # Deployment workflow
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

**Current Phase:** Phase 8 — Analytics & Monitoring (Complete)

### Phase Summary
- **Phase 1-2:** Discovery & Design
- **Phase 3-4:** Architecture & MVP Scaffold
- **Phase 5-6:** Functional Build & Deployment
- **Phase 7:** AI Integration & Automation
- **Phase 8:** Analytics & Monitoring (Current)

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
