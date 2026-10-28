# Turicor brand files (v1, 2026-10-20)

Decision record: `decisions.md` entry 2026-10-20. Concept history: https://claude.ai/artifact/VnmxWzyDVgTZEwSWkQUVmW (v1 three directions, v2 ratios, v3 colour, v4 corners, v5 rounded faces).

## What the logo is
A wordmark, not a pictorial mark. "Turicor" set in **Instrument Sans 600**, tracking −0.025 em, with one modified letter: the **T**. Its crossbar is the TEE probe; its stem opens downward into the ultrasound sector; the red dot is the clip (coaptation) point. The square version for favicon, app icon and social avatars is that T alone.

Chinese name: **图灵心** (Noto Sans SC 500, tracking 0.24 em), used only in the lockup.

## Geometry (T height = 100 = cap height)
| Part | Numbers |
|---|---|
| Crossbar (probe) | x 18–82, y 0–12, corner radius 2.5 |
| Sector apex | x 44–56 at y 12 |
| Sector bottom | x 24–76 on an arc of radius 84 centred on the apex; corner radius 2.5; opening angle 36° |
| Dot | centre (50, 79), radius 5 |
| Gap T → u | 0.02 em |
| Square icon | T at 56 % of the square's height, centred, top at 22 %; corner radius 22 % |

## Colours
| Token | Hex | Use |
|---|---|---|
| ink | `#1A1B1E` | wordmark on light backgrounds; icon background |
| cream | `#ECEAE3` | wordmark on ink; icon glyph on ink / red |
| seal | `#CE4A33` | the dot, and the single-colour red version |

Rules: the wordmark is always one colour (cream on dark, ink on light). The dot is the only accent. No gradients, no shadows, no outlines. On a red background the dot becomes a hole. At 16 px the dot is dropped.

## Files
| File | Use |
|---|---|
| `2026-10-20_turicor_wordmark_v1_cream.svg` / `_ink.svg` | primary wordmark, dark / light backgrounds |
| `2026-10-20_turicor_wordmark_v1_mono.svg` | single colour, no dot (fax, engraving, grey partner walls) |
| `2026-10-20_turicor_wordmark_v1_red.svg` | all red, dot as hole (stamps, red posters) |
| `2026-10-20_turicor_wordmark_v1_cream_2400.png` / `_ink_2400.png` | same, transparent PNG 2400 px wide, for decks and documents |
| `2026-10-20_turicor_lockup_cn_v1_cream.svg` / `_ink.svg` | Turicor · 图灵心 horizontal lockup |
| `2026-10-20_turicor_T_v1_*.svg` | the T alone, no background (ink / cream / red-hole) |
| `2026-10-20_turicor_icon_v1_*.svg` and `*_512.png` | rounded square app icon (ink / cream / red backgrounds) |
| `2026-10-20_turicor_social_v1_ink_1200.png` / `_400.png` (and `_cream_`) | **LinkedIn / X / WeChat avatars and company-page logos**: square to the edge, no rounded corners (the platform adds its own frame or circle). Upload the 1200 one; 400 is the LinkedIn minimum |
| `favicon.svg`, `favicon.ico`, `favicon-16.png`, `favicon-32.png` | browser tab (square, no dot) |
| `apple-touch-icon.png` | iOS home screen, 180 px, square (iOS rounds it) |
| `2026-10-20_turicor_logo_generator_v1.py` | regenerates every SVG from the numbers above |

Minimum sizes: wordmark 80 px wide on screen / 20 mm in print; icon 16 px. Clear space around the wordmark: the height of the T on every side.

## Regenerating
The script needs `fonttools` and `uharfbuzz` (`pip install --user fonttools uharfbuzz`) and the two font files, which are not kept in the repo: Instrument Sans 600 (latin subset) and a Noto Sans SC 500 subset for 图灵心, both from Google Fonts (Open Font License). Download them into an empty folder, then:

```bash
python3 2026-10-20_turicor_logo_generator_v1.py <font folder> <output folder> 2026-10-20_turicor
```

PNGs were rendered from the SVGs with headless Chrome (`--default-background-color=00000000` for transparency) and `favicon.ico` was assembled with Pillow.

## Still open
- Deck master (`10_fundraising/pitch/2026-10-12_Turicor_master_v1.potx`) still uses a text wordmark; replace with `..._wordmark_v1_ink_2400.png`.
- `og-image.jpg` stays the product shot on purpose; a brand-only share image is not made.
- Trademark: see the 2026-10-20 decision entry for the search result and what to check before filing.
