import math
import sys
from pathlib import Path

OUT_DIR = Path(sys.argv[1])

ACCENTS = {"light": "#a8803a", "dark": "#d9b36c"}

W, H = 1200, 240
STRANDS, POINTS, FRAMES, PERIOD = 30, 56, 10, 14


def point(u, s, phi, x0=40, x1=1160, cy=120):
    yc = cy + 52 * math.sin(2 * math.pi * 1.3 * u + phi) + 12 * math.sin(2 * math.pi * 2.6 * u - phi)
    w = 58 * math.sin(math.pi * u) ** 0.85
    th = 2 * math.pi * 1.1 * u + phi
    return x0 + (x1 - x0) * u + 0.3 * w * math.sin(th) * s, yc + w * math.cos(th) * s


def banner(accent):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
           '<defs><linearGradient id="silk" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="1160" y2="0">',
           f'<stop offset="0" stop-color="{accent}" stop-opacity="0"/>',
           f'<stop offset="0.25" stop-color="{accent}"/><stop offset="0.75" stop-color="{accent}"/>',
           f'<stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient></defs>',
           '<g fill="none" stroke="url(#silk)" stroke-linecap="round" opacity="0">',
           '<animate attributeName="opacity" from="0" to="1" begin="0.2s" dur="2.4s" fill="freeze"/>']
    for i in range(STRANDS):
        s = -1 + 2 * i / (STRANDS - 1)
        ds = []
        for f in range(FRAMES + 1):
            phi = 2 * math.pi * f / FRAMES
            pts = [point(k / (POINTS - 1), s, phi) for k in range(POINTS)]
            ds.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts))
        opacity = 0.22 + 0.6 * abs(s) ** 1.6
        width = 1.1 if abs(s) > 0.97 else 0.6
        out.append(f'<path d="{ds[0]}" stroke-width="{width}" opacity="{opacity:.2f}">'
                   f'<animate attributeName="d" dur="{PERIOD}s" repeatCount="indefinite" values="{";".join(ds)}"/></path>')
    out.append("</g></svg>")
    return "".join(out)


OUT_DIR.mkdir(parents=True, exist_ok=True)
for theme, accent in ACCENTS.items():
    (OUT_DIR / f"ribbon-{theme}.svg").write_text(banner(accent))
