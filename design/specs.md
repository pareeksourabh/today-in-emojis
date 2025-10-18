# Phase 2 — One-Pager Design Specs

## Layout Overview
A single static viewport page with three sections:
1. Header — site title
2. Center — emoji row (five)
3. Footer — reactions and credits

Layout schematic:

---------------------------------
TODAY IN EMOJIS  (Header)

[   Emoji 1   Emoji 2   Emoji 3   Emoji 4   Emoji 5   ]

[ Like | Neutral | Dislike ]  •  Built by Sourabh  •  [GitHub] [README]
---------------------------------

### Header
- Font: Inter, uppercase, 600 weight
- Size: 20px desktop / 16px mobile
- Margin-top: 24px

### Emoji Row
- 5 emojis in one centered row
- Size: 120px desktop / 80px mobile
- Gap: 32px desktop / 16px mobile
- Optional click → link to story

### Footer
- Font-size: 14px desktop / 12px mobile
- Reaction buttons: 3 icons
- Gap between reactions: 16px
- Divider • between sections
- Links: GitHub, README

### Responsiveness
- Entire layout fits 700px height (no scroll)
- Center alignment via flexbox
- Mobile padding: 16px

### Interactions
| Element | Interaction | Animation |
|----------|--------------|------------|
| Emoji | Hover → scale(1.1) | 120ms |
| Reaction | Click → scale(1.2) bounce | 100ms |
| Load | Fade-in | 300ms |

### Notes
- Minimal text, only emojis and credits visible.
- Each pixel should justify its presence.
- Test on Chrome and Safari (desktop/mobile).