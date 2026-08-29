# -*- coding: utf-8 -*-
"""Yetkinlik ağacı — gerçek projelerden çıkarılmış teknoloji haritası.

Veri kaynağı UYDURMA DEĞİL: her satır, depolardaki package.json / pyproject.toml
bağımlılıklarından ve GitHub dil istatistiklerinden çıkarıldı. Her dalın yanında
o teknolojinin HANGİ projede kullanıldığı yazar — iddia değil kanıt.

Logolar simple-icons'tan (CC0) SVG'ye gömülür; dış servis bağımlılığı yoktur.
Marka adları/logoları sahiplerinin ticari markasıdır.
"""
import re
import urllib.request
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"
BG, GRID, FRAME = "#0a0d13", "#131a26", "#1c2534"
ACCENT, INK, INK2, INK3 = "#e8003d", "#e6e9ef", "#8b93a7", "#5c6579"
RULE, WIRE, BOX = "#232d3f", "#243044", "#0e131d"
CDN = "https://cdn.jsdelivr.net/npm/simple-icons@13/icons/{}.svg"

# (kategori, kanıt = nerede kullanıldığı, [(slug, ad, renk), ...])
# Siyah marka renkleri (Express, Socket.IO, JWT, WebRTC, OpenAI) koyu zeminde
# görünmediği için açık griye çekildi — tanınırlık korunur, okunurluk kazanılır
TREE = [
    ("LANGUAGES", "every repository", [
        ("javascript", "JavaScript", "#F7DF1E"),
        ("typescript", "TypeScript", "#3178C6"),
        ("python", "Python", "#4B8BBE"),
    ]),
    ("BACKEND · API", "Asfalya · RepChat · EKT Akademi · AdsPilot", [
        ("nodedotjs", "Node.js", "#5FA04E"),
        ("express", "Express", "#cfd6e4"),
        ("fastapi", "FastAPI", "#12A594"),
        ("socketdotio", "Socket.IO", "#cfd6e4"),
        ("claude", "MCP", "#D97757"),
    ]),
    ("DATA · AUTH", "PostGIS in Asfalya · Mongo in AnimeRank", [
        ("postgresql", "PostgreSQL", "#5A8DEE"),
        ("mongodb", "MongoDB", "#47A248"),
        ("supabase", "Supabase", "#3ECF8E"),
        ("redis", "Redis", "#FF4438"),
        ("jsonwebtokens", "JWT", "#cfd6e4"),
    ]),
    ("ML · VISION", "Asfalya detector · Patina restoration", [
        ("pytorch", "PyTorch", "#EE4C2C"),
        ("opencv", "OpenCV", "#7B5CF0"),
        ("nvidia", "CUDA", "#76B900"),
        ("openai", "LLM APIs", "#cfd6e4"),
    ]),
    ("MEDIA · STREAMING", "AnimeRank HLS · RepChat calls · Kurenai", [
        ("ffmpeg", "FFmpeg", "#3FA34D"),
        ("webrtc", "WebRTC", "#cfd6e4"),
    ]),
    ("FRONTEND", "Asfalya map panel · AnimeRank player UI", [
        ("react", "React", "#61DAFB"),
        ("tailwindcss", "Tailwind", "#38BDF8"),
        ("maplibre", "MapLibre", "#6C9BE0"),
    ]),
    ("OPS · DELIVERY", "every repo ships behind CI", [
        ("docker", "Docker", "#2496ED"),
        ("githubactions", "Actions", "#4C8EFF"),
        ("nginx", "nginx", "#009639"),
        ("linux", "Linux", "#E5B93C"),
        ("git", "Git", "#F05032"),
    ]),
]


def esc(t: str) -> str:
    """XML kaçışlama — kanıt satırlarında & geçiyor (AnimeRank & MangaRank)."""
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fetch_path(slug: str) -> str:
    cache = Path(f"/tmp/si_{slug}.svg")
    if cache.exists() and cache.stat().st_size > 200:
        svg = cache.read_text(encoding="utf-8")
    else:
        with urllib.request.urlopen(CDN.format(slug), timeout=30) as r:
            svg = r.read().decode("utf-8")
        cache.write_text(svg, encoding="utf-8")
    m = re.search(r'<path d="([^"]+)"', svg)
    if not m:
        raise RuntimeError(f"path yok: {slug}")
    return m.group(1)


def build():
    row_h = 74
    top = 104
    H = top + len(TREE) * row_h + 52
    spine_x, branch_x, label_x, icon_x = 60, 96, 108, 330
    icon_step = 128

    o = [
        f'<svg width="1000" height="{H}" viewBox="0 0 1000 {H}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="Skill tree — languages, backend, data, machine learning, media, operations">',
        '  <defs>',
        '    <pattern id="gst" width="28" height="28" patternUnits="userSpaceOnUse">',
        f'      <path d="M28 0H0V28" fill="none" stroke="{GRID}" stroke-width="1"/>',
        '    </pattern>',
        "    <style>",
        "      .lbl{font-family:'Segoe UI',Helvetica,Arial,sans-serif;}",
        "      .data{font-family:'SF Mono',Consolas,'Cascadia Code',monospace;}",
        "      .title{font-family:'Segoe UI Semibold','Segoe UI',Helvetica,Arial,sans-serif;font-weight:600;}",
        "    </style>",
        '  </defs>',
        f'  <rect width="1000" height="{H}" fill="{BG}"/>',
        f'  <rect width="1000" height="{H}" fill="url(#gst)"/>',
        f'  <rect x="0.5" y="0.5" width="999" height="{H-1}" fill="none" stroke="{FRAME}"/>',
        f'  <rect x="42" y="31" width="6" height="6" fill="{ACCENT}"/>',
        f'  <text x="58" y="38" class="data" font-size="10.5" fill="{INK3}" letter-spacing="3">07 — CAPABILITY TREE · DRAWN FROM SHIPPED REPOSITORIES</text>',
        f'  <line x1="32" y1="56" x2="968" y2="56" stroke="{RULE}" stroke-width="1"/>',
        f'  <text x="42" y="78" class="lbl" font-size="10.5" fill="{INK3}">'
        'each branch lists where the tooling is actually used — not a wishlist</text>',
    ]

    y_first = top + row_h // 2
    y_last = top + (len(TREE) - 1) * row_h + row_h // 2
    # omurga
    o.append(f'  <line x1="{spine_x}" y1="{y_first}" x2="{spine_x}" y2="{y_last}" stroke="{WIRE}" stroke-width="1.5"/>')
    o.append(f'  <circle cx="{spine_x}" cy="{y_first-24}" r="4" fill="{ACCENT}"/>')
    o.append(f'  <line x1="{spine_x}" y1="{y_first-20}" x2="{spine_x}" y2="{y_first}" stroke="{WIRE}" stroke-width="1.5"/>')

    for i, (cat, proof, items) in enumerate(TREE):
        cy = top + i * row_h + row_h // 2
        # dal
        o.append(f'  <line x1="{spine_x}" y1="{cy}" x2="{branch_x}" y2="{cy}" stroke="{WIRE}" stroke-width="1.5"/>')
        o.append(f'  <rect x="{spine_x-3}" y="{cy-3}" width="6" height="6" fill="{ACCENT}"/>')
        # kategori + kanıt
        o.append(f'  <text x="{label_x}" y="{cy-2}" class="title" font-size="11.5" fill="{INK}" letter-spacing="1.4">{esc(cat)}</text>')
        o.append(f'  <text x="{label_x}" y="{cy+14}" class="data" font-size="8.5" fill="{INK3}">{esc(proof)}</text>')
        # simgeler
        for j, (slug, name, color) in enumerate(items):
            ix = icon_x + j * icon_step
            d = fetch_path(slug)
            o.append(f'  <g transform="translate({ix},{cy-11}) scale(0.88)"><path d="{d}" fill="{color}"/></g>')
            o.append(f'  <text x="{ix+30}" y="{cy+4}" class="lbl" font-size="11" fill="{INK2}">{esc(name)}</text>')
        if i < len(TREE) - 1:
            o.append(f'  <line x1="{label_x}" y1="{cy+row_h//2-6}" x2="968" y2="{cy+row_h//2-6}" stroke="#161d2b"/>')

    o.append(f'  <line x1="32" y1="{H-30}" x2="968" y2="{H-30}" stroke="#161d2b"/>')
    o.append(f'  <text x="42" y="{H-13}" class="data" font-size="9" fill="{INK3}">'
             'Logos are trademarks of their respective owners · icon paths from simple-icons (CC0)</text>')
    o.append("</svg>")
    (ASSETS / "skilltree.svg").write_text("\n".join(o), encoding="utf-8")
    total = sum(len(t[2]) for t in TREE)
    print(f"skilltree.svg: {(ASSETS/'skilltree.svg').stat().st_size} bayt · {len(TREE)} dal · {total} simge")


if __name__ == "__main__":
    build()
