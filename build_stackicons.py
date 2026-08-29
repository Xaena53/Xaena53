# -*- coding: utf-8 -*-
"""Teknoloji simgeleri kartı — gerçek marka logoları, profilin çizim dilinde.

Neden hazır rozet servisi (shields.io / skillicons) kullanılmadı: onlar dış
sunucudan gelen, kendi renk ve köşe diline sahip görsellerdir; bu profilin
teknik-çizim estetiğini bozar ve dış servis çökerse profil delik görünür.
Logolar simple-icons'tan (CC0 path verisi) SVG'ye GÖMÜLÜR — dış bağımlılık yok.

Marka adları ve logoları ilgili şirketlerin ticari markalarıdır; burada yalnızca
kullanılan teknolojiyi adlandırmak için yer alır.
"""
import re
import urllib.request
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"
BG, GRID, FRAME = "#0a0d13", "#131a26", "#1c2534"
ACCENT, INK, INK2, INK3 = "#e8003d", "#e6e9ef", "#8b93a7", "#5c6579"
RULE = "#232d3f"
CDN = "https://cdn.jsdelivr.net/npm/simple-icons@13/icons/{}.svg"

# (simple-icons slug, görünen ad, renk) — koyu zeminde görünmeyen siyah logolar
# (Express, WebRTC) bilinçli olarak açık griye çekildi
TECH = [
    ("nodedotjs", "Node.js", "#5FA04E"),
    ("express", "Express", "#cfd6e4"),
    ("postgresql", "PostgreSQL / PostGIS", "#5A8DEE"),
    ("docker", "Docker", "#2496ED"),
    ("githubactions", "GitHub Actions", "#4C8EFF"),
    ("maplibre", "MapLibre", "#6C9BE0"),
    ("python", "Python", "#4B8BBE"),
    ("pytorch", "PyTorch", "#EE4C2C"),
    ("opencv", "OpenCV", "#7B5CF0"),
    ("ffmpeg", "FFmpeg", "#3FA34D"),
    ("webrtc", "WebRTC", "#cfd6e4"),
    ("claude", "MCP / Claude", "#D97757"),
]


def fetch_path(slug: str) -> str:
    """simple-icons SVG'sinden tek path verisini çıkarır (24x24 viewBox)."""
    cache = Path(f"/tmp/si_{slug}.svg")
    if cache.exists() and cache.stat().st_size > 200:
        svg = cache.read_text(encoding="utf-8")
    else:
        with urllib.request.urlopen(CDN.format(slug), timeout=30) as r:
            svg = r.read().decode("utf-8")
        cache.write_text(svg, encoding="utf-8")
    m = re.search(r'<path d="([^"]+)"', svg)
    if not m:
        raise RuntimeError(f"path bulunamadı: {slug}")
    return m.group(1)


def build():
    cols, rows = 4, 3
    cell_w, cell_h = 234, 46
    x0, y0 = 42, 86
    H = y0 + rows * cell_h + 34

    out = [
        f'<svg width="1000" height="{H}" viewBox="0 0 1000 {H}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="Technology stack — {", ".join(t[1] for t in TECH)}">',
        '  <defs>',
        '    <pattern id="gti" width="28" height="28" patternUnits="userSpaceOnUse">',
        f'      <path d="M28 0H0V28" fill="none" stroke="{GRID}" stroke-width="1"/>',
        '    </pattern>',
        "    <style>",
        "      .lbl { font-family:'Segoe UI',Helvetica,Arial,sans-serif; }",
        "      .data { font-family:'SF Mono',Consolas,'Cascadia Code',monospace; }",
        "      .title { font-family:'Segoe UI Semibold','Segoe UI',Helvetica,Arial,sans-serif; font-weight:600; }",
        "    </style>",
        '  </defs>',
        f'  <rect width="1000" height="{H}" fill="{BG}"/>',
        f'  <rect width="1000" height="{H}" fill="url(#gti)"/>',
        f'  <rect x="0.5" y="0.5" width="999" height="{H-1}" fill="none" stroke="{FRAME}"/>',
        f'  <rect x="42" y="31" width="6" height="6" fill="{ACCENT}"/>',
        f'  <text x="58" y="38" class="data" font-size="10.5" fill="{INK3}" letter-spacing="3">12 — TOOLING · WORKING SET</text>',
        f'  <line x1="32" y1="56" x2="968" y2="56" stroke="{RULE}" stroke-width="1"/>',
        f'  <text x="42" y="76" class="lbl" font-size="10.5" fill="{INK3}">what these systems are actually built with</text>',
    ]

    for i, (slug, name, color) in enumerate(TECH):
        cx = x0 + (i % cols) * cell_w
        cy = y0 + (i // cols) * cell_h
        d = fetch_path(slug)
        # 24x24 logoyu 22px'e ölçekle, hücrenin soluna yerleştir
        out.append(f'  <g transform="translate({cx},{cy}) scale(0.92)">')
        out.append(f'    <path d="{d}" fill="{color}"/>')
        out.append('  </g>')
        out.append(f'  <text x="{cx+34}" y="{cy+16}" class="lbl" font-size="12" fill="{INK}">{name}</text>')

    out.append(f'  <line x1="32" y1="{H-28}" x2="968" y2="{H-28}" stroke="#161d2b"/>')
    out.append(f'  <text x="42" y="{H-11}" class="data" font-size="9" fill="{INK3}">'
               'Logos are trademarks of their respective owners · icon paths from simple-icons (CC0)</text>')
    out.append("</svg>")
    (ASSETS / "techicons.svg").write_text("\n".join(out), encoding="utf-8")
    print(f"techicons.svg: {(ASSETS / 'techicons.svg').stat().st_size} bayt, {len(TECH)} simge")


if __name__ == "__main__":
    build()
