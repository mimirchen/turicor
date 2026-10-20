#!/usr/bin/env python3
"""Generate the Turicor logo files (SVG) from the locked geometry.

Geometry A, T height 100 = cap height. Crossbar 18..82 x 0..12 (corners r2.5).
Sector apex 44..56 at y=12, bottom 24..76 on an arc r84 centred at the apex;
corners r2.5. Red dot at (50,79) r5. Wordmark: Instrument Sans 600 'uricor',
tracking -0.025em, cap height 720/1000 scaled so cap = 100.
"""
import sys, os, pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb

FONT_DIR = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
STEM = sys.argv[3]  # e.g. 2026-10-20_turicor

INK = "#1A1B1E"; CREAM = "#ECEAE3"; SEAL = "#CE4A33"

# ---- T glyph (geometry A, micro-rounded) in a 100-high box, x from 18 to 82
T_CROSSBAR = "M20.5 0H79.5A2.5 2.5 0 0 1 82 2.5V9.5A2.5 2.5 0 0 1 79.5 12H20.5A2.5 2.5 0 0 1 18 9.5V2.5A2.5 2.5 0 0 1 20.5 0Z"
T_SECTOR_INSET = "M46.5 14.5H53.5L73.6 89.8A81.5 81.5 0 0 1 26.4 89.8Z"  # stroked w5 round-join => outer edge = sharp geometry with r2.5 corners
T_PATCH = "M44 10H56V14H44Z"
DOT = (50, 79, 5)

def t_glyph(color, dot=None, hole=False, mask_id=None):
    """Return SVG markup for the T (+dot) in T-space (x 18..82, y 0..100)."""
    body = (f'<path d="{T_CROSSBAR}" fill="{color}"/>'
            f'<path d="{T_SECTOR_INSET}" fill="{color}" stroke="{color}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="{T_PATCH}" fill="{color}"/>')
    if hole:
        body = f'<g mask="url(#{mask_id})">{body}</g>'
    if dot:
        body += f'<circle cx="{DOT[0]}" cy="{DOT[1]}" r="{DOT[2]}" fill="{dot}"/>'
    return body

def hole_mask(mask_id, x, y, w, h):
    return (f'<mask id="{mask_id}" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff"/>'
            f'<circle cx="{DOT[0]}" cy="{DOT[1]}" r="{DOT[2]}" fill="#000"/></mask>')

# ---- text to paths via HarfBuzz + fontTools
def shape(font_path, text, size_per_em, tracking_em=0.0):
    """Return (list of (path_d, x_advance_start), total_width) with y flipped, scaled so 1em = size_per_em."""
    import io
    tt = TTFont(font_path)
    tt.flavor = None  # HarfBuzz needs a raw sfnt, not WOFF
    bio = io.BytesIO(); tt.save(bio); data = bio.getvalue()
    upem = tt["head"].unitsPerEm
    glyphset = tt.getGlyphSet()
    face = hb.Face(data); hbfont = hb.Font(face); hbfont.scale = (upem, upem)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True})
    s = size_per_em / upem
    order = tt.getGlyphOrder()
    x = 0.0; out = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gname = order[info.codepoint]
        pen = SVGPathPen(glyphset)
        tpen = TransformPen(pen, (s, 0, 0, -s, x + pos.x_offset * s, -pos.y_offset * s))
        glyphset[gname].draw(tpen)
        d = pen.getCommands()
        if d: out.append(d)
        x += pos.x_advance * s + tracking_em * size_per_em
    x -= tracking_em * size_per_em  # no tracking after last glyph
    return out, x, tt

IS = next(FONT_DIR.glob("is_2.woff"))
NS = next(FONT_DIR.glob("NotoSansSC-500-subset.bin"))

# Instrument Sans: cap 720/1000. We want cap height == 100 => em = 100/0.72
EM_IS = 100 / 0.72
TRACK = -0.025
paths_uricor, w_uricor, tt_is = shape(IS, "uricor", EM_IS, TRACK)
# left side bearing of 'u' is already inside the advance; wordmark starts at T x=18.
T_W = 64  # 18..82
GAP = 0.02 * EM_IS  # margin-right .02em in the concept page
# The T sits at x 0..64 (shifted by -18); text starts at 64 + GAP
X_TEXT = T_W + GAP
WM_W = X_TEXT + w_uricor
# vertical: cap top y=0, baseline y=100; descender of 'uricor' none. Keep a 0..100 box.

def wordmark_svg(fg, dot, hole=False, bg=None):
    pad = 10
    vb_w, vb_h = WM_W + 2*pad, 100 + 2*pad
    mid = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w:.1f} {vb_h:.1f}" width="{vb_w:.1f}" height="{vb_h:.1f}">'
    body = ""
    if bg: body += f'<rect width="100%" height="100%" fill="{bg}"/>'
    if hole: body += hole_mask("h", 18, 0, 64, 100)
    body += f'<g transform="translate({pad - 18} {pad})">' + t_glyph(fg, dot, hole, "h") + '</g>'
    body += f'<g transform="translate({pad + X_TEXT:.2f} {pad + 100})" fill="{fg}">' + "".join(f'<path d="{d}"/>' for d in paths_uricor) + '</g>'
    return mid + body + "</svg>"

# Chinese lockup: Turicor | 图灵心, wordmark 32px, rule, cn 23px tracking .24em (from concept page) => scale to wordmark cap 100: ratio 100/(32*.72)=4.34
R = 100 / (32 * 0.72)
CN_EM = 23 * R
CN_TRACK = 0.24
paths_cn, w_cn, tt_ns = shape(NS, "图灵心", CN_EM, CN_TRACK)
GAP_LOCK = 16 * R
RULE_H = 1.5 * 32 * R

def lockup_svg(fg, dot, bg=None):
    pad = 10
    x_rule = WM_W + GAP_LOCK
    x_cn = x_rule + 1 * R + GAP_LOCK + 0.1 * CN_EM
    total_w = x_cn + w_cn
    # vertical centring: wordmark cap box 0..100 centred at 50; CN glyphs: centre ideographic box (ascender ~0.88em, descender ~0.12em for Noto) -> baseline at 50 + (0.88-0.12)/2*em
    cn_baseline = 50 + 0.38 * CN_EM
    vb_w, vb_h = total_w + 2*pad, 100 + 2*pad
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w:.1f} {vb_h:.1f}" width="{vb_w:.1f}" height="{vb_h:.1f}">'
    if bg: s += f'<rect width="100%" height="100%" fill="{bg}"/>'
    s += f'<g transform="translate({pad - 18} {pad})">' + t_glyph(fg, dot) + '</g>'
    s += f'<g transform="translate({pad + X_TEXT:.2f} {pad + 100})" fill="{fg}">' + "".join(f'<path d="{d}"/>' for d in paths_uricor) + '</g>'
    s += f'<rect x="{pad + x_rule:.2f}" y="{pad + 50 - RULE_H/2:.2f}" width="{1*R:.2f}" height="{RULE_H:.2f}" fill="{fg}" fill-opacity="0.35"/>'
    s += f'<g transform="translate({pad + x_cn:.2f} {pad + cn_baseline:.2f})" fill="{fg}">' + "".join(f'<path d="{d}"/>' for d in paths_cn) + '</g>'
    return s + "</svg>"

def mark_svg(fg, dot, hole=False, bg=None, rounded=True, size=512, with_dot=True):
    """Square app icon / favicon: T centred, T height 56% of the square (concept page: x=31 y=22 w=38 h=56 on 100)."""
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="{size}" height="{size}">'
    if bg:
        s += f'<rect width="100" height="100" rx="{22 if rounded else 0}" fill="{bg}"/>'
    if hole: s += hole_mask("h", 18, 0, 64, 100)
    # T-space 64x100 -> box 38x56 at (31,22): scale 0.56 (38/64=0.594, 56/100=0.56; keep aspect with 0.56 => width 35.8, x=32.1)
    sc = 0.56; w = 64*sc; x0 = (100 - w)/2; y0 = 22
    s += f'<g transform="translate({x0:.2f} {y0}) scale({sc}) translate(-18 0)">' + t_glyph(fg, dot if with_dot else None, hole, "h") + '</g>'
    return s + "</svg>"

def t_only_svg(fg, dot, hole=False):
    pad = 4
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {64+2*pad} {100+2*pad}" width="{64+2*pad}" height="{100+2*pad}">'
    if hole: s += hole_mask("h", 18, 0, 64, 100)
    s += f'<g transform="translate({pad-18} {pad})">' + t_glyph(fg, dot, hole, "h") + '</g></svg>'
    return s

files = {
    f"{STEM}_wordmark_v1_ink.svg":   wordmark_svg(INK, SEAL),
    f"{STEM}_wordmark_v1_cream.svg": wordmark_svg(CREAM, SEAL),
    f"{STEM}_wordmark_v1_mono.svg":  wordmark_svg(INK, None),
    f"{STEM}_wordmark_v1_red.svg":   wordmark_svg(SEAL, None, hole=True),
    f"{STEM}_lockup_cn_v1_ink.svg":  lockup_svg(INK, SEAL),
    f"{STEM}_lockup_cn_v1_cream.svg":lockup_svg(CREAM, SEAL),
    f"{STEM}_T_v1_ink.svg":          t_only_svg(INK, SEAL),
    f"{STEM}_T_v1_cream.svg":        t_only_svg(CREAM, SEAL),
    f"{STEM}_T_v1_red.svg":          t_only_svg(SEAL, None, hole=True),
    f"{STEM}_icon_v1_ink.svg":       mark_svg(CREAM, SEAL, bg=INK),
    f"{STEM}_icon_v1_cream.svg":     mark_svg(INK, SEAL, bg=CREAM),
    f"{STEM}_icon_v1_red.svg":       mark_svg(CREAM, None, hole=True, bg=SEAL),
    # favicon: square (browsers round it themselves), no dot (16 px rule), ink bg
    "favicon.svg":                   mark_svg(CREAM, SEAL, bg=INK, rounded=False, with_dot=False),
}
for name, svg in files.items():
    (OUT / name).write_text(svg, encoding="utf-8")
    print(name, len(svg))
print("wordmark box", round(WM_W,1), "x 100; T font cap=", tt_is["OS/2"].sCapHeight)
