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
    tests = [("AdsPilot", 646), ("EKT Akademi", 270), ("Asfalya", 213),
             ("MangaRank", 70), ("RepChat e2e", 40)]
    curve_csv = Path(r"C:/Asfalya/pipeline/runs/asfalya-v1/results.csv")
    curve = []
    if curve_csv.exists():
        for r in csv.DictReader(curve_csv.open()):
            ep = int(list(r.values())[0].strip())
            m = float(next(v for k, v in r.items() if "mAP50(B)" in k.strip()))
            curve.append((ep, m))

    H = 320
    s = [head(H, "Verified engineering metrics — test suites and model training", "g8m",
              "10 — TELEMETRY · VERIFIED METRICS")]
    s.append(f'<line x1="500" y1="56" x2="500" y2="{H-30}" stroke="#161d2b" stroke-width="1"/>')

    # --- sol panel: yatay çubuklar (tek seri => tek renk; rank'e göre renk yok)
    s.append(f'<text x="42" y="82" class="title" font-size="12" fill="{INK}" letter-spacing="1.5">AUTOMATED TEST SUITES</text>')
    s.append(f'<text x="42" y="98" class="data" font-size="9.5" fill="{INK3}">passing · per project</text>')
    x0, wmax, top, step, bh = 168, 232, 118, 27, 13
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
    px0, px1, py0, py1 = 546, 950, 130, 252   # çizim alanı
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
    s.append(f'<text x="42" y="{py1+46}" class="lbl" font-size="10.5" fill="{INK2}">Per-class recall — manholes 0.82 · alligator cracks 0.65 · potholes 0.42. Measured on held-out data, not estimated.</text>')
    s.append("</svg>")
    (ASSETS / "metrics.svg").write_text("\n".join(s), encoding="utf-8")


# ----------------------------------------------------------------- 04 · ASFALYA
def build_asfalya():
    H = 250
    css = "@keyframes flow{0%{stroke-dashoffset:14}100%{stroke-dashoffset:0}} .fl{stroke-dasharray:5 9;animation:flow 1.4s linear infinite}"
    s = [head(H, "Asfalya — vehicle-mounted road damage detection pipeline", "g4a",
              "04 — ASFALYA · MUNICIPAL ROAD INTELLIGENCE", css)]
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
             ("213", "tests passing")]
    for i, (v, k) in enumerate(notes):
        x = 42 + i * 235
        s.append(f'<text x="{x}" y="220" class="data" font-size="16" fill="{INK}">{v}</text>')
        s.append(f'<text x="{x}" y="234" class="lbl" font-size="10" fill="{INK3}">{k}</text>')
    s.append("</svg>")
    (ASSETS / "pipeline-asfalya.svg").write_text("\n".join(s), encoding="utf-8")


# ----------------------------------------------------------------- 05 · ADSPILOT
def build_adspilot():
    # 268, 230 değil: alttaki künye satırı y=248'de duruyor ve 230'luk viewBox onu
    # tamamen kırpıyordu — kartın en güçlü iddiası (hackathon kısa listesi, ilk canlı
    # CAMARA çağrısı) hiç görünmüyordu.
    H = 282
    s = [head(H, "AdsPilot — Google Ads automation with safety gates", "g5a",
              "05 — ADSPILOT · GUARDED AD AUTOMATION")]
    s.append(f'<text x="42" y="86" class="disp" font-size="21" fill="{INK}">AdsPilot</text>')
    s.append(f'<text x="42" y="106" class="lbl" font-size="11.5" fill="{INK2}">An MCP server that lets a model run Google Ads — behind gates that refuse to spend without consent</text>')

    gates = [("CAMPAIGNS START PAUSED", "no silent spend"),
             ("BUDGET RAISE NEEDS CONSENT", "cuts are free"),
             ("ACCOUNT OWNER SETS CEILING", "model cannot lift it"),
             ("SITE DATA IS UNTRUSTED", "prompt-injection guard")]
    for i, (t, sub) in enumerate(gates):
        x, y = 42 + (i % 2) * 470, 132 + (i // 2) * 46
        s.append(f'<rect x="{x}" y="{y}" width="446" height="36" fill="#0e131d" stroke="#243044"/>')
        s.append(f'<rect x="{x}" y="{y}" width="3" height="36" fill="{ACCENT}"/>')
        s.append(f'<text x="{x+14}" y="{y+16}" class="data" font-size="10" fill="{INK}" letter-spacing="1">{t}</text>')
        s.append(f'<text x="{x+14}" y="{y+29}" class="lbl" font-size="9.5" fill="{INK3}">{sub}</text>')
    s.append(f'<text x="42" y="{132+2*46+26}" class="lbl" font-size="10.5" fill="{INK2}">646 tests · 94% line coverage · every gate mutation-verified · AGPL-3.0</text>')
    s.append(f'<text x="42" y="{132+2*46+42}" class="lbl" font-size="10.5" fill="{INK2}">Shortlisted at the GSMA MENA Ignite hackathon · first live CAMARA network-API call executed</text>')
    s.append("</svg>")
    (ASSETS / "pipeline-adspilot.svg").write_text("\n".join(s), encoding="utf-8")


# ----------------------------------------------------------------- 09 · OPEN SOURCE
def build_opensource():
    H = 210
    s = [head(H, "Open source contributions and shipped systems", "g9o",
              "11 — CONTRIBUTIONS · SHIPPED SYSTEMS")]
    s.append(f'<text x="42" y="82" class="title" font-size="12" fill="{INK}" letter-spacing="1.5">UPSTREAM CONTRIBUTIONS</text>')
    items = [("microsoft/vscode", "PR #329128 — de-duplicated find-input history"),
             ("nasa/openmct", "issue #6313 — Y-axis label fix")]
    for i, (repo, what) in enumerate(items):
        y = 106 + i * 30
        s.append(f'<rect x="42" y="{y-9}" width="4" height="4" fill="{ACCENT}"/>')
        s.append(f'<text x="58" y="{y-5}" class="data" font-size="11.5" fill="{INK}">{esc(repo)}</text>')
        s.append(f'<text x="230" y="{y-5}" class="lbl" font-size="11" fill="{INK2}">{esc(what)}</text>')

    s.append(f'<line x1="32" y1="168" x2="968" y2="168" stroke="{RULE}"/>')
    live = [("ektakademi.com", "LIVE"), ("cakmakpen.com.tr", "LIVE"),
            ("RepChat", "IN PRODUCTION"), ("Asfalya", "PILOT PREP")]
    for i, (name, state) in enumerate(live):
        x = 42 + i * 235
        col = "#2e9e4f" if state in ("LIVE", "IN PRODUCTION") else "#d7a032"
        s.append(f'<circle cx="{x+4}" cy="190" r="3.5" fill="{col}"/>')
        s.append(f'<text x="{x+16}" y="194" class="lbl" font-size="11.5" fill="{INK}">{esc(name)}</text>')
        s.append(f'<text x="{x+16}" y="206" class="data" font-size="8.5" fill="{INK3}" letter-spacing="1">{state}</text>')
    s.append("</svg>")
    (ASSETS / "opensource.svg").write_text("\n".join(s), encoding="utf-8")


if __name__ == "__main__":
    build_metrics()
    build_asfalya()
    build_adspilot()
    build_opensource()
    for f in ("metrics.svg", "pipeline-asfalya.svg", "pipeline-adspilot.svg", "opensource.svg"):
        print(f"{f}: {(ASSETS / f).stat().st_size} bayt")
