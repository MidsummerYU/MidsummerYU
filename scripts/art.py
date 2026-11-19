import math
import sys
from io import BytesIO
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

FONT_DIR = Path(sys.argv[1])
OUT_DIR = Path(sys.argv[2])

THEMES = {
    "light": dict(bg1="#ffffff", bg2="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#59636e", faint="#8c959f", accent="#a8803a", rule="#d8dee4", glow="0.07"),
    "dark": dict(bg1="#0d1117", bg2="#141a23", border="#30363d", text="#f0f6fc",
                 muted="#9198a1", faint="#6e7681", accent="#d9b36c", rule="#262c36", glow="0.07"),
}


class Face:
    def __init__(self, path, axes, key):
        self.key = key
        tt = instantiateVariableFont(TTFont(path), axes)
        buf = BytesIO()
        tt.save(buf)
        self.tt = TTFont(BytesIO(buf.getvalue()))
        self.hb_font = hb.Font(hb.Face(buf.getvalue()))
        self.upem = self.tt["head"].unitsPerEm
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()

    def _shape(self, text):
        b = hb.Buffer()
        b.add_str(text)
        b.guess_segment_properties()
        hb.shape(self.hb_font, b, {"kern": True, "liga": True})
        return b.glyph_infos, b.glyph_positions

    def width(self, text, size, tracking=0.0):
        _, pos = self._shape(text)
        return sum(p.x_advance for p in pos) * size / self.upem + tracking * max(len(pos) - 1, 0)

    def uses(self, text, size, x, y, tracking=0.0):
        infos, pos = self._shape(text)
        s = size / self.upem
        out, cx = [], x
        for info, p in zip(infos, pos):
            gid = f"{self.key}{info.codepoint}"
            if gid not in GLYPHS:
                pen = SVGPathPen(self.glyphs, ntos=lambda v: f"{v:.0f}")
                self.glyphs[self.order[info.codepoint]].draw(pen)
                GLYPHS[gid] = pen.getCommands()
            if GLYPHS[gid]:
                out.append(f'<use href="#{gid}" transform="translate({cx + p.x_offset * s:.1f} {y - p.y_offset * s:.1f}) '
                           f'scale({s:.5f} {-s:.5f})"/>')
            cx += p.x_advance * s + tracking
        return "".join(out)

    def wrap(self, text, size, max_w):
        lines, cur = [], ""
        for word in text.split():
            trial = f"{cur} {word}".strip()
            if cur and self.width(trial, size) > max_w:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        if cur:
            lines.append(cur)
        return lines


GLYPHS = {}

INTER = FONT_DIR / "Inter.ttf"
REG = Face(INTER, {"wght": 400, "opsz": 14}, "r")
MED = Face(INTER, {"wght": 600, "opsz": 20}, "m")
CAPS = Face(INTER, {"wght": 600, "opsz": 14}, "c")
DISPLAY = Face(INTER, {"wght": 650, "opsz": 32}, "d")

CAPS_TRACK = 1.8


def text(face, s, size, x, y, fill, tracking=0.0):
    return f'<g fill="{fill}">{face.uses(s, size, x, y, tracking)}</g>'


def label(s, x, y, fill, size=13):
    return text(CAPS, s.upper(), size, x, y, fill, CAPS_TRACK)


def frame(w, h, t, glow=None):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">', "<defs>",
           f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg1"]}"/>'
           f'<stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>',
           f'<clipPath id="card"><rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18"/></clipPath>']
    if glow:
        out.append(f'<radialGradient id="glow" cx="{glow[0]}" cy="{glow[1]}" r="{glow[2]}">'
                   f'<stop offset="0" stop-color="{t["accent"]}" stop-opacity="{t["glow"]}"/>'
                   f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient>')
    out.append("</defs>")
    out.append(f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" fill="url(#bg)" stroke="{t["border"]}"/>')
    if glow:
        out.append(f'<rect width="{w}" height="{h}" fill="url(#glow)" clip-path="url(#card)"/>')
    return out


def fade(begin, dur=1.2, rise=8):
    return (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{begin}s" dur="{dur}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {rise}" to="0 0" begin="{begin}s" '
            f'dur="{dur}s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1" keyTimes="0;1"/>')


def ribbon(t, x0=560, x1=1175, cy=182):
    strands, points, frames, period = 30, 44, 10, 14
    span = x1 - x0

    def point(u, s, phi):
        yc = cy + 58 * math.sin(2 * math.pi * 1.1 * u + phi) + 14 * math.sin(2 * math.pi * 2.3 * u - phi)
        w = 62 * math.sin(math.pi * u) ** 0.85
        th = 2 * math.pi * 0.85 * u + phi
        return x0 + span * u + 0.3 * w * math.sin(th) * s, yc + w * math.cos(th) * s

    out = [f'<linearGradient id="silk" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{x1}" y2="0">'
           f'<stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/>'
           f'<stop offset="0.3" stop-color="{t["accent"]}" stop-opacity="1"/>'
           f'<stop offset="0.75" stop-color="{t["accent"]}" stop-opacity="1"/>'
           f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></linearGradient>']
    out.append('<g fill="none" stroke="url(#silk)" stroke-linecap="round">')
    for i in range(strands):
        s = -1 + 2 * i / (strands - 1)
        ds = []
        for f in range(frames + 1):
            phi = 2 * math.pi * f / frames
            pts = [point(k / (points - 1), s, phi) for k in range(points)]
            ds.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts))
        op = 0.22 + 0.6 * abs(s) ** 1.6
        width = 1.1 if abs(s) > 0.97 else 0.6
        out.append(f'<path d="{ds[0]}" stroke-width="{width}" opacity="{op:.2f}">'
                   f'<animate attributeName="d" dur="{period}s" repeatCount="indefinite" values="{";".join(ds)}"/></path>')
    out.append("</g>")
    return out


def banner(t):
    w, h = 1200, 360
    out = frame(w, h, t, glow=(0.74, 0.5, 0.45))
    out.append('<g clip-path="url(#card)"><g opacity="0">'
               '<animate attributeName="opacity" from="0" to="1" begin="0.3s" dur="2.4s" fill="freeze"/>')
    out += ribbon(t)
    out.append("</g></g>")
    x0 = 76
    out.append(fade(0.1, 1.4, 10))
    out.append(text(DISPLAY, "Yumeng Ye", 80, x0 - 4, 176, t["text"], -2.0))
    out.append("</g>")
    out.append(f'<line x1="{x0 + 2}" y1="214" x2="{x0 + 74}" y2="214" stroke="{t["accent"]}" stroke-width="2" '
               f'stroke-dasharray="72" stroke-dashoffset="72"><animate attributeName="stroke-dashoffset" from="72" to="0" '
               f'begin="0.9s" dur="0.9s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" keyTimes="0;1"/></line>')
    out.append(fade(1.1, 1.2, 6))
    out.append(text(CAPS, "AI ENGINEER", 15, x0 + 2, 255, t["text"], 2.6))
    cw = CAPS.width("AI ENGINEER", 15, 2.6)
    out.append(f'<circle cx="{x0 + 2 + cw + 15:.1f}" cy="249.5" r="2" fill="{t["accent"]}"/>')
    out.append(text(CAPS, "PARIS", 15, x0 + 2 + cw + 30, 255, t["text"], 2.6))
    out.append(text(REG, "LLMs, agents, retrieval, evaluation and fine-tuning", 20, x0 + 2, 292, t["muted"]))
    out.append("</g></svg>")
    return "".join(out)


CONTRIBUTIONS = [
    ("genspark-ai/genoffice", "AI office suite · Excel engine on WebAssembly, PowerPoint, PDF", "15 merged"),
]


def card_open_source(t):
    w, h = 1200, 164 + 54 * len(CONTRIBUTIONS)
    out = frame(w, h, t)
    out.append(fade(0.1, 1.0, 6))
    out.append(label("Open source", 76, 70, t["accent"]))
    out.append(text(REG, "Tools I use, and help improve", 19, 76, 104, t["muted"]))
    for k, (repo, what, count) in enumerate(CONTRIBUTIONS):
        y = 158 + k * 54
        out.append(f'<line x1="76" y1="{y - 34}" x2="{w - 76}" y2="{y - 34}" stroke="{t["rule"]}"/>')
        out.append(text(MED, repo, 21, 76, y, t["text"]))
        out.append(text(REG, what, 17, 400, y, t["muted"]))
        cw = CAPS.width(count.upper(), 13, CAPS_TRACK)
        out.append(label(count, w - 76 - cw, y - 2, t["accent"]))
    out.append("</g></svg>")
    return "".join(out)


def card_small(t, kicker, title, body, tags, link):
    w, h = 590, 390
    out = frame(w, h, t)
    out.append(fade(0.1, 1.0, 6))
    x, maxw = 44, w - 88
    out.append(label(kicker, x, 66, t["accent"], 14))
    y = 114
    for line in MED.wrap(title, 30, maxw):
        out.append(text(MED, line, 30, x, y, t["text"], -0.4))
        y += 38
    y += 10
    for line in REG.wrap(body, 20, maxw):
        out.append(text(REG, line, 20, x, y, t["muted"]))
        y += 30
    out.append(text(CAPS, "  ·  ".join(tags).upper(), 12, x, h - 94, t["faint"], 1.2))
    out.append(f'<line x1="{x}" y1="{h - 72}" x2="{w - x}" y2="{h - 72}" stroke="{t["rule"]}"/>')
    out.append(text(MED, link, 19, x, h - 36, t["accent"]))
    out.append("</g></svg>")
    return "".join(out)


def card_stack(t):
    rows = [("Languages", "Python · TypeScript · SQL"),
            ("AI & agents", "Pydantic AI · LangGraph · MCP · RAG · LLM evaluation · Claude Code"),
            ("Machine learning", "PyTorch · Transformers · LoRA · SFT · DPO · vision-language models"),
            ("Backend & web", "FastAPI · PostgreSQL · Redis · React · Next.js · Playwright"),
            ("Cloud & infra", "Docker · Kubernetes · GCP · AWS · Azure")]
    w, h = 1200, 120 + 46 * len(rows)
    out = frame(w, h, t)
    out.append(fade(0.1, 1.0, 6))
    out.append(label("Stack", 76, 70, t["accent"]))
    for k, (name, items) in enumerate(rows):
        y = 124 + k * 46
        out.append(label(name, 76, y, t["muted"], 12))
        out.append(text(REG, items, 18, 330, y + 1, t["text"]))
        if k < len(rows) - 1:
            out.append(f'<line x1="76" y1="{y + 19}" x2="{w - 76}" y2="{y + 19}" stroke="{t["rule"]}"/>')
    out.append("</g></svg>")
    return "".join(out)


def pill(t, s):
    tw = CAPS.width(s.upper(), 13, CAPS_TRACK)
    w, h = int(tw + 56), 46
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="23" fill="{t["bg1"]}" stroke="{t["border"]}"/>'
            f'{label(s, 28, 28, t["text"])}</svg>')


def with_glyphs(svg):
    used = sorted({g for g in GLYPHS if f'href="#{g}"' in svg})
    defs = "<defs>" + "".join(f'<path id="{g}" d="{GLYPHS[g]}"/>' for g in used) + "</defs>"
    head_end = svg.index(">") + 1
    return svg[:head_end] + defs + svg[head_end:]


OUT_DIR.mkdir(parents=True, exist_ok=True)
for name, t in THEMES.items():
    files = {
        "banner": banner(t),
        "open-source": card_open_source(t),
        "research": card_small(
            t, "Research  ·  Hugging Face", "Vision-language model for nuclear regulation",
            "Fine-tuned a small vision-language model to find the right page in regulatory documents read as images. "
            "First author.",
            ["SmolVLM", "Fine-tuning", "Document retrieval"], "Read the article  →"),
        "competition": card_small(
            t, "Competition  ·  Polimi × Huawei", "Huawei Signal Processing Competition",
            "Denoising real audio recordings corrupted by different kinds of noise, with adaptive filtering and "
            "spectral analysis. 2024.",
            ["MATLAB", "Adaptive filters", "Spectral analysis"], "View the repository  →"),
        "stack": card_stack(t),
        "linkedin": pill(t, "LinkedIn"),
        "huggingface": pill(t, "Hugging Face"),
    }
    for key, svg in files.items():
        (OUT_DIR / f"{key}-{name}.svg").write_text(with_glyphs(svg))
print("ok")
