# -*- coding: utf-8 -*-
"""Profil kartı üreteci — mevcut teknik-çizim diline sadık SVG'ler.

Tasarım sözleşmesi (mevcut kartlardan çıkarıldı, bozulmaz):
  genişlik 1000 · zemin #0a0d13 · ızgara #131a26 · çerçeve #1c2534
  vurgu #e8003d · metin #e6e9ef/#8b93a7/#5c6579
  başlık şeridi "NN — BÖLÜM · ALT BAŞLIK" · Georgia/Segoe UI/monospace üçlüsü

Grafik kuralları (veri görselleştirme rehberi):
  tek seri = tek renk (sıra/rank'e göre renk YOK) · ince marklar · yuvarlatılmış
  veri uçları · geri planda ızgara · seçili doğrudan etiketler · legend gereksiz
  (başlık seriyi adlandırıyor) · azaltılmış hareket tercihi desteklenir
"""
import csv
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"
BG, GRID, FRAME = "#0a0d13", "#131a26", "#1c2534"
ACCENT, INK, INK2, INK3 = "#e8003d", "#e6e9ef", "#8b93a7", "#5c6579"
RULE = "#232d3f"

HEAD = '''<svg width="1000" height="{h}" viewBox="0 0 1000 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">
  <defs>
    <pattern id="{gid}" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="{grid}" stroke-width="1"/>
    </pattern>
    <style>
      .lbl {{ font-family:'Segoe UI',Helvetica,Arial,sans-serif; }}
      .data {{ font-family:'SF Mono',Consolas,'Cascadia Code',monospace; }}
      .title {{ font-family:'Segoe UI Semibold','Segoe UI',Helvetica,Arial,sans-serif; font-weight:600; }}
      .disp {{ font-family:Georgia,'Times New Roman',serif; }}
      {extra_css}
      @media (prefers-reduced-motion: reduce) {{ * {{ animation:none !important; }} }}
    </style>
  </defs>
  <rect width="1000" height="{h}" fill="{bg}"/>
  <rect width="1000" height="{h}" fill="url(#{gid})"/>
  <rect x="0.5" y="0.5" width="999" height="{hh}" fill="none" stroke="{frame}"/>
  <rect x="42" y="31" width="6" height="6" fill="{accent}"/>
  <text x="58" y="38" class="data" font-size="10.5" fill="{ink3}" letter-spacing="3">{eyebrow}</text>
  <line x1="32" y1="56" x2="968" y2="56" stroke="{rule}" stroke-width="1"/>
'''


def head(h, label, gid, eyebrow, extra_css=""):
    return HEAD.format(h=h, hh=h - 1, label=label, gid=gid, eyebrow=eyebrow, grid=GRID,
                       bg=BG, frame=FRAME, accent=ACCENT, ink3=INK3, rule=RULE,
                       extra_css=extra_css)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ----------------------------------------------------------------- 08 · TELEMETRY
def build_metrics():
    """Sol: test paketleri (yatay çubuk) · Sağ: gerçek model eğitim eğrisi."""
    # Her sayı o reponun kendi kaydından: Aegis README rozeti, EKT docs/FAZ-BITIS-BRIFINGI,
    # Asfalya docs/HAZIRLIK-PROGRAMI, Demir Cephe scripts/check.sh, Warden tools/RunTests.ps1
    tests = [("Aegis", 1765), ("EKT Akademi", 327), ("Asfalya", 320),
             ("Demir Cephe", 204), ("MangaRank", 70), ("Warden (UE5)", 34)]
    curve_csv = Path(r"C:/Asfalya/pipeline/runs/asfalya-v1/results.csv")
    curve = []
    if curve_csv.exists():
        for r in csv.DictReader(curve_csv.open()):
            ep = int(list(r.values())[0].strip())
            m = float(next(v for k, v in r.items() if "mAP50(B)" in k.strip()))
            curve.append((ep, m))

    H = 340
    s = [head(H, "Verified engineering metrics — test suites and model training", "g8m",
              "12 — TELEMETRY · VERIFIED METRICS")]
    s.append(f'<line x1="500" y1="56" x2="500" y2="{H-30}" stroke="#161d2b" stroke-width="1"/>')

    # --- sol panel: yatay çubuklar (tek seri => tek renk; rank'e göre renk yok)
    s.append(f'<text x="42" y="82" class="title" font-size="12" fill="{INK}" letter-spacing="1.5">AUTOMATED TEST SUITES</text>')
    s.append(f'<text x="42" y="98" class="data" font-size="9.5" fill="{INK3}">passing · per project</text>')
    x0, wmax, top, step, bh = 168, 232, 118, 24, 12
    mx = max(v for _, v in tests)
    for i, (name, val) in enumerate(tests):
        y = top + i * step
        w = max(3, round(wmax * val / mx))
        s.append(f'<text x="160" y="{y+10}" text-anchor="end" class="lbl" font-size="11.5" fill="{INK2}">{esc(name)}</text>')
        s.append(f'<rect x="{x0}" y="{y}" width="{wmax}" height="{bh}" fill="#111826"/>')
        s.append(f'<rect x="{x0}" y="{y}" width="{w}" height="{bh}" rx="3" fill="{ACCENT}"/>')
        s.append(f'<text x="{x0+w+9}" y="{y+10}" class="data" font-size="11" fill="{INK}">{val}</text>')
    total = sum(v for _, v in tests)
    s.append(f'<line x1="42" y1="{top+len(tests)*step+6}" x2="458" y2="{top+len(tests)*step+6}" stroke="#161d2b"/>')
    s.append(f'<text x="42" y="{top+len(tests)*step+26}" class="data" font-size="10" fill="{INK3}" letter-spacing="1.5">TOTAL</text>')
    s.append(f'<text x="458" y="{top+len(tests)*step+26}" text-anchor="end" class="data" font-size="13" fill="{INK}">{total} passing</text>')

    # --- sağ panel: eğitim eğrisi (gerçek koşu verisi)
    s.append(f'<text x="530" y="82" class="title" font-size="12" fill="{INK}" letter-spacing="1.5">MODEL TRAINING — ROAD DAMAGE DETECTOR</text>')
    s.append(f'<text x="530" y="98" class="data" font-size="9.5" fill="{INK3}">mAP@50 · 40 epochs · RDD2022 · 35,984 images</text>')
    px0, px1, py0, py1 = 546, 950, 130, 272   # çizim alanı
    ymin, ymax = 0.20, 0.70
    fx = lambda e: px0 + (px1 - px0) * (e - 1) / max(1, (len(curve) - 1))
    fy = lambda v: py1 - (py1 - py0) * (v - ymin) / (ymax - ymin)
    for gv in (0.2, 0.4, 0.6):
        yy = fy(gv)
        s.append(f'<line x1="{px0}" y1="{yy:.1f}" x2="{px1}" y2="{yy:.1f}" stroke="#161d2b" stroke-width="1"/>')
        s.append(f'<text x="{px0-8}" y="{yy+3.5:.1f}" text-anchor="end" class="data" font-size="9" fill="{INK3}">{gv:.1f}</text>')
    if curve:
        pts = " ".join(f"{fx(e):.1f},{fy(v):.1f}" for e, v in curve)
        area = f"{px0},{py1} " + pts + f" {fx(curve[-1][0]):.1f},{py1}"
        s.append(f'<polygon points="{area}" fill="{ACCENT}" opacity="0.10"/>')
        s.append(f'<polyline points="{pts}" fill="none" stroke="{ACCENT}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
        ex, ey = fx(curve[-1][0]), fy(curve[-1][1])
        s.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{ACCENT}" stroke="{BG}" stroke-width="2"/>')
        s.append(f'<text x="{ex-6:.1f}" y="{ey-12:.1f}" text-anchor="end" class="data" font-size="12" fill="{INK}">{curve[-1][1]:.3f}</text>')
        s.append(f'<text x="{px0}" y="{py1+18}" class="data" font-size="9" fill="{INK3}">epoch 1</text>')
        s.append(f'<text x="{px1}" y="{py1+18}" text-anchor="end" class="data" font-size="9" fill="{INK3}">epoch {curve[-1][0]}</text>')
    s.append(f'<line x1="32" y1="{py1+26}" x2="968" y2="{py1+26}" stroke="#161d2b"/>')
    s.append(f'<text x="42" y="{py1+46}" class="lbl" font-size="10.5" fill="{INK2}">Per-class recall — manholes 0.82 · alligator cracks 0.65 · potholes 0.42. Measured on held-out data.</text>')
    s.append("</svg>")
    (ASSETS / "metrics.svg").write_text("\n".join(s), encoding="utf-8")


# ----------------------------------------------------------------- 04 · ASFALYA
def build_asfalya():
    H = 250
    css = "@keyframes flow{0%{stroke-dashoffset:14}100%{stroke-dashoffset:0}} .fl{stroke-dasharray:5 9;animation:flow 1.4s linear infinite}"
    s = [head(H, "Asfalya — vehicle-mounted road damage detection pipeline", "g4a",
              "01 — ASFALYA · MUNICIPAL ROAD INTELLIGENCE", css)]
    s.append(f'<text x="42" y="86" class="disp" font-size="21" fill="{INK}">Asfalya</text>')
    s.append(f'<text x="42" y="106" class="lbl" font-size="11.5" fill="{INK2}">Phone cameras on municipal buses → damage map for the public works team</text>')

    boxes = [(42, "CAPTURE", "Android · 2 fps + GPS"), (256, "PRIVACY", "face + plate blur"),
             (470, "DETECT", "YOLO11 · RTX 5070"), (684, "GEO", "GPS interp · OSM match")]
    for x, t, sub in boxes:
        s.append(f'<rect x="{x}" y="132" width="190" height="54" fill="#0e131d" stroke="#243044"/>')
        s.append(f'<rect x="{x}" y="132" width="3" height="54" fill="{ACCENT}"/>')
        s.append(f'<text x="{x+14}" y="154" class="title" font-size="12" fill="{INK}" letter-spacing="1.2">{t}</text>')
        s.append(f'<text x="{x+14}" y="171" class="data" font-size="9.5" fill="{INK3}">{sub}</text>')
    for x in (232, 446, 660):
        s.append(f'<line class="fl" x1="{x}" y1="159" x2="{x+24}" y2="159" stroke="{ACCENT}" stroke-width="1.6"/>')
    s.append(f'<rect x="874" y="132" width="84" height="54" fill="#0e131d" stroke="#243044"/>')
    s.append(f'<text x="916" y="154" text-anchor="middle" class="title" font-size="12" fill="{INK}">MAP</text>')
    s.append(f'<text x="916" y="171" text-anchor="middle" class="data" font-size="9" fill="{INK3}">PostGIS</text>')
    s.append(f'<line class="fl" x1="850" y1="159" x2="874" y2="159" stroke="{ACCENT}" stroke-width="1.6"/>')

    notes = [("35,984", "images trained on"), ("0.63", "mAP@50"), ("13/s", "frames processed"),
             ("320", "tests passing")]
    for i, (v, k) in enumerate(notes):
        x = 42 + i * 235
        s.append(f'<text x="{x}" y="220" class="data" font-size="16" fill="{INK}">{v}</text>')
        s.append(f'<text x="{x}" y="234" class="lbl" font-size="10" fill="{INK3}">{k}</text>')
    s.append("</svg>")
    (ASSETS / "pipeline-asfalya.svg").write_text("\n".join(s), encoding="utf-8")


# ----------------------------------------------------------------- 05 · AEGIS
def build_aegis():
    H = 300
    s = [head(H, "Aegis — network-verified approvals for AI agents that spend money", "g5a",
              "02 — AEGIS · NETWORK-VERIFIED AD AUTOMATION")]
    s.append(f'<text x="42" y="86" class="disp" font-size="21" fill="{INK}">Aegis</text>')
    s.append(f'<text x="42" y="106" class="lbl" font-size="11.5" fill="{INK2}">An MCP server that runs real Google Ads and Meta campaigns and asks the mobile network about the approver before money moves</text>')

    gates = [("NETWORK CHECK RUNS FIRST", "CAMARA SIM-swap · fail-closed"),
             ("THE SERVER ASKS THE HUMAN", "MCP elicitation · the agent's own flag is ignored"),
             ("CAMPAIGNS START PAUSED", "on Google Ads and on Meta"),
             ("OWNER SETS THE CEILING", "raises need consent · cuts go through")]
    for i, (t, sub) in enumerate(gates):
        x, y = 42 + (i % 2) * 470, 132 + (i // 2) * 46
        s.append(f'<rect x="{x}" y="{y}" width="446" height="36" fill="#0e131d" stroke="#243044"/>')
        s.append(f'<rect x="{x}" y="{y}" width="3" height="36" fill="{ACCENT}"/>')
        s.append(f'<text x="{x+14}" y="{y+16}" class="data" font-size="10" fill="{INK}" letter-spacing="1">{t}</text>')
        s.append(f'<text x="{x+14}" y="{y+29}" class="lbl" font-size="9.5" fill="{INK3}">{esc(sub)}</text>')
    notes = [("1,765", "automated tests"), ("83%", "line coverage"), ("3 of 3", "integrations called live"),
             ("AGPL-3.0", "open source")]
    for i, (v, k) in enumerate(notes):
        x = 42 + i * 235
        s.append(f'<text x="{x}" y="252" class="data" font-size="16" fill="{INK}">{v}</text>')
        s.append(f'<text x="{x}" y="266" class="lbl" font-size="10" fill="{INK3}">{k}</text>')
    s.append(f'<text x="42" y="288" class="lbl" font-size="10" fill="{INK3}">Shortlisted at the GSMA MENA Ignite hackathon · Google Ads, Meta and five of six CAMARA links verified against the real APIs (Nokia Network-as-Code, simulator mode)</text>')
    s.append("</svg>")
    (ASSETS / "pipeline-aegis.svg").write_text("\n".join(s), encoding="utf-8")


# ----------------------------------------------------------------- 06 · NÖBETÇİ MEMUR
def build_nobetci():
    """Oyun döngüsü (oku → karşılaştır → karar ver → eve dön → son) + ölçülmüş sayılar.

    Sayılar oyunun kendi deposundan: tools/saglamlik.sh (4.322 denetim), tools/dil/kaynak.json
    (955 metin), data/vatandaslar.json (89 sabit kimlik), README "Sonlar" (yedi gün, yedi son).
    """
    H = 300
    css = "@keyframes flow{0%{stroke-dashoffset:14}100%{stroke-dashoffset:0}} .fl{stroke-dasharray:5 9;animation:flow 1.4s linear infinite}"
    s = [head(H, "Nöbetçi Memur — a document-inspection game set in a 1984 registry office, playable in the browser",
              "g6n", "06 — NÖBETÇİ MEMUR · PLAYABLE IN THE BROWSER", css)]
    s.append(f'<text x="42" y="86" class="disp" font-size="21" fill="{INK}">Nöbetçi Memur</text>')
    s.append(f'<text x="42" y="106" class="lbl" font-size="11.5" fill="{INK2}">A document-inspection game: window 2 of a small-town registry office, January 1984 · seven working days, seven endings</text>')

    boxes = [(42, "READ", "papers slide onto the desk"), (256, "COMPARE", "click two facts · a line is drawn"),
             (470, "DECIDE", "approve · reject · refer"), (684, "GO HOME", "rent · coal · food · medicine")]
    for x, t, sub in boxes:
        s.append(f'<rect x="{x}" y="132" width="190" height="54" fill="#0e131d" stroke="#243044"/>')
        s.append(f'<rect x="{x}" y="132" width="3" height="54" fill="{ACCENT}"/>')
        s.append(f'<text x="{x+14}" y="154" class="title" font-size="12" fill="{INK}" letter-spacing="1.2">{t}</text>')
        s.append(f'<text x="{x+14}" y="171" class="data" font-size="9.5" fill="{INK3}">{esc(sub)}</text>')
    for x in (232, 446, 660):
        s.append(f'<line class="fl" x1="{x}" y1="159" x2="{x+24}" y2="159" stroke="{ACCENT}" stroke-width="1.6"/>')
    s.append(f'<rect x="874" y="132" width="84" height="54" fill="#0e131d" stroke="#243044"/>')
    s.append(f'<text x="916" y="154" text-anchor="middle" class="title" font-size="12" fill="{INK}">ENDING</text>')
    s.append(f'<text x="916" y="171" text-anchor="middle" class="data" font-size="9" fill="{INK3}">1 of 7</text>')
    s.append(f'<line class="fl" x1="850" y1="159" x2="874" y2="159" stroke="{ACCENT}" stroke-width="1.6"/>')

    notes = [("4,322", "automated robustness checks"), ("955", "strings · Turkish, English, Russian"),
             ("89", "citizens with a fixed identity"), ("7 × 7", "working days × endings")]
    for i, (v, k) in enumerate(notes):
        x = 42 + i * 235
        s.append(f'<text x="{x}" y="222" class="data" font-size="16" fill="{INK}">{v}</text>')
        s.append(f'<text x="{x}" y="236" class="lbl" font-size="10" fill="{INK3}">{esc(k)}</text>')
    s.append(f'<line x1="32" y1="254" x2="968" y2="254" stroke="#161d2b"/>')
    s.append(f'<circle cx="46" cy="272" r="3.5" fill="#2e9e4f"/>')
    s.append(f'<text x="58" y="276" class="lbl" font-size="10.5" fill="{INK2}">Godot 4.3 · GDScript · rules and people in JSON · Windows build and a WebAssembly build served from GitHub Pages</text>')
    s.append(f'<text x="958" y="276" text-anchor="end" class="data" font-size="9" fill="{INK3}" letter-spacing="1">PLAYABLE</text>')
    s.append("</svg>")
    (ASSETS / "pipeline-nobetci.svg").write_text("\n".join(s), encoding="utf-8")


# ----------------------------------------------------------------- 06 · WORK INDEX
def build_work():
    rows = [
        ("EKT Akademi", "training platform · whole backend behind an existing static front end",
         "Node 22 · Express 5 · PostgreSQL · Prisma", "LIVE"),
        ("Warden of the Fields", "first-person open-world survival game",
         "Unreal Engine 5.8 · C++", "IN DEVELOPMENT"),
        ("Demir Cephe", "combined-arms war game with tanks, aircraft and infantry",
         "Roblox · Luau · Rojo", "IN DEVELOPMENT"),
        ("Hapivanak", "honey store with PayTR checkout and batch traceability",
         "TanStack Start · Cloudflare Workers · D1", "LIVE"),
        ("Çakmak Pen", "23-page corporate site for a joinery company",
         "static multi-page site · no build step", "LIVE"),
        ("MHRS Data Module", "synthetic hospital-appointment database for a six-team course project",
         "Python · SQLite · Faker", "TEAM"),
    ]
    top, step = 86, 36
    H = top + len(rows) * step + 10
    s = [head(H, "More work — shipped and in progress", "g6w", "08 — INDEX · MORE WORK")]
    for i, (name, what, stack, state) in enumerate(rows):
        y = top + i * step
        if i:
            s.append(f'<line x1="42" y1="{y-13}" x2="958" y2="{y-13}" stroke="#161d2b"/>')
        col = "#2e9e4f" if state == "LIVE" else ("#d7a032" if state == "IN DEVELOPMENT" else "#5f7fbf")
        s.append(f'<circle cx="46" cy="{y+5}" r="3.5" fill="{col}"/>')
        s.append(f'<text x="60" y="{y+9}" class="title" font-size="12.5" fill="{INK}">{esc(name)}</text>')
        s.append(f'<text x="250" y="{y+3}" class="lbl" font-size="11" fill="{INK2}">{esc(what)}</text>')
        s.append(f'<text x="250" y="{y+17}" class="data" font-size="9.5" fill="{INK3}">{esc(stack)}</text>')
        s.append(f'<text x="958" y="{y+9}" text-anchor="end" class="data" font-size="9" fill="{INK3}" letter-spacing="1">{state}</text>')
    s.append("</svg>")
    (ASSETS / "work.svg").write_text("\n".join(s), encoding="utf-8")


# ----------------------------------------------------------------- 09 · OPEN SOURCE
def build_opensource():
    H = 250
    s = [head(H, "Open source contributions and shipped systems", "g9o",
              "13 — CONTRIBUTIONS · SHIPPED SYSTEMS")]
    s.append(f'<text x="42" y="82" class="title" font-size="12" fill="{INK}" letter-spacing="1.5">UPSTREAM CONTRIBUTIONS</text>')
    items = [("microsoft/vscode", "PR #329128 — shared find-input toggle navigation · merged"),
             ("nasa/openmct", "PR #8393 — plot Y-axis label follows edits · in review"),
             ("PreMiD/Activities", "PR #11384 — Discord activity card for AnimeRank · in review")]
    for i, (repo, what) in enumerate(items):
        y = 106 + i * 30
        s.append(f'<rect x="42" y="{y-9}" width="4" height="4" fill="{ACCENT}"/>')
        s.append(f'<text x="58" y="{y-5}" class="data" font-size="11.5" fill="{INK}">{esc(repo)}</text>')
        s.append(f'<text x="230" y="{y-5}" class="lbl" font-size="11" fill="{INK2}">{esc(what)}</text>')

    s.append(f'<line x1="32" y1="198" x2="968" y2="198" stroke="{RULE}"/>')
    live = [("ektakademi.com", "LIVE"), ("cakmakpen.com.tr", "LIVE"), ("kurenai.shop", "LIVE"),
            ("RepChat", "IN PRODUCTION"), ("Asfalya", "PILOT PREP")]
    for i, (name, state) in enumerate(live):
        x = 42 + i * 188
        col = "#2e9e4f" if state in ("LIVE", "IN PRODUCTION") else "#d7a032"
        s.append(f'<circle cx="{x+4}" cy="220" r="3.5" fill="{col}"/>')
        s.append(f'<text x="{x+16}" y="224" class="lbl" font-size="11.5" fill="{INK}">{esc(name)}</text>')
        s.append(f'<text x="{x+16}" y="236" class="data" font-size="8.5" fill="{INK3}" letter-spacing="1">{state}</text>')
    s.append("</svg>")
    (ASSETS / "opensource.svg").write_text("\n".join(s), encoding="utf-8")


if __name__ == "__main__":
    build_metrics()
    build_asfalya()
    build_aegis()
    build_nobetci()
    build_work()
    build_opensource()
    for f in ("metrics.svg", "pipeline-asfalya.svg", "pipeline-aegis.svg", "pipeline-nobetci.svg", "work.svg", "opensource.svg"):
        print(f"{f}: {(ASSETS / f).stat().st_size} bayt")
