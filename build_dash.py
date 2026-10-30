# -*- coding: utf-8 -*-
"""Çark + etkinlik + kadran kartları.

orbit.svg     08·B  teknoloji çarkı: yetkinlik ağacındaki 33 simge üç halkada döner (portfolyodaki çarkın SVG'si)
activity.svg  00    açılışta commit kutularıyla yazılan Bedirhan Çetin imzası, sonra son 12 ayın katkı ısı haritası + proje başına son 26 haftanın haftalık commit'leri
dials.svg     11·B  ölçülmüş oranlar için kadranlar + depo başına eşit ağırlıklı dil dağılımı

Veri: `python build_dash.py --cek` GitHub API'den veri/ altına çeker (gh girişli olmalı);
argümansız çalıştırma veri/ içindekini çizer. Dil renkleri dataviz doğrulayıcısından geçti
(koyu zemin #0a0d13, komşu CVD ΔE ≥ 8,4).
"""
import collections
import datetime as dt
import json
import math
import subprocess
import sys
from pathlib import Path

from build_skilltree import TREE, fetch_path

KOK = Path(__file__).parent
ASSETS, VERI = KOK / "assets", KOK / "veri"
BG, GRID, FRAME, RULE = "#0a0d13", "#131a26", "#1c2534", "#232d3f"
ACCENT, INK, INK2, INK3, WIRE, BOX = "#e8003d", "#e6e9ef", "#8b93a7", "#5c6579", "#243044", "#0e131d"

# depo → profilde görünen ad; avellana ve venato gizli iş fikirleri, bilerek yok
PROJE = [("AnimeRank-Project", "AnimeRank"), ("ekt-akademi", "EKT Akademi"), ("aegis", "Aegis"),
         ("baldefteri", "Hapivanak"), ("asfalya", "Asfalya"), ("RepChat", "RepChat"),
         ("cakmakpen", "Çakmak Pen"), ("Kurenai", "Kurenai"), ("warden-of-the-fields", "Warden"),
         ("portfolio", "Portfolio"), ("demir-cephe", "Demir Cephe")]
DIL_DEPO = [d for d, _ in PROJE] + ["mhrs-veri", "avellana"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def gh(*a):
    return subprocess.run(["gh", "api", *a], capture_output=True, text=True, encoding="utf-8", check=True).stdout


def cek():
    VERI.mkdir(exist_ok=True)
    q = ("{viewer{contributionsCollection{contributionCalendar{totalContributions "
         "weeks{contributionDays{date contributionCount}}}}}}")
    (VERI / "takvim.json").write_text(gh("graphql", "-f", f"query={q}"), encoding="utf-8")
    bugun = dt.date.today()
    bas = bugun - dt.timedelta(days=bugun.isoweekday() % 7 + 25 * 7)   # 26 hafta, pazar başlangıçlı
    haftalik = {}
    for depo, _ in PROJE:
        satir = gh(f"repos/Xaena53/{depo}/commits?since={bas}T00:00:00Z&per_page=100", "--paginate",
                   "--jq", ".[].commit.author.date").split()
        say = [0] * 26
        for t in satir:
            i = (dt.date.fromisoformat(t[:10]) - bas).days // 7
            if 0 <= i < 26:
                say[i] += 1
        haftalik[depo] = say
    (VERI / "haftalik.json").write_text(json.dumps(dict(baslangic=str(bas), seri=haftalik)), encoding="utf-8")
    diller = {d: json.loads(gh(f"repos/Xaena53/{d}/languages")) for d in DIL_DEPO}
    (VERI / "diller.json").write_text(json.dumps(diller), encoding="utf-8")
    print("veri çekildi:", bas, "→", bugun)


def head(h, label, gid, eyebrow, css=""):
    return [f'<svg width="1000" height="{h}" viewBox="0 0 1000 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(label)}">',
            '  <defs>',
            f'    <pattern id="{gid}" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{GRID}" stroke-width="1"/></pattern>',
            "    <style>",
            "      .lbl{font-family:'Segoe UI',Helvetica,Arial,sans-serif;}",
            "      .data{font-family:'SF Mono',Consolas,'Cascadia Code',monospace;}",
            "      .title{font-family:'Segoe UI Semibold','Segoe UI',Helvetica,Arial,sans-serif;font-weight:600;}",
            "      .disp{font-family:Georgia,'Times New Roman',serif;}",
            f"      {css}",
            "      @media (prefers-reduced-motion: reduce){*{animation:none !important;}}",
            "    </style>",
            "  </defs>",
            f'  <rect width="1000" height="{h}" fill="{BG}"/>',
            f'  <rect width="1000" height="{h}" fill="url(#{gid})"/>',
            f'  <rect x="0.5" y="0.5" width="999" height="{h-1}" fill="none" stroke="{FRAME}"/>',
            f'  <rect x="42" y="31" width="6" height="6" fill="{ACCENT}"/>',
            f'  <text x="58" y="38" class="data" font-size="10.5" fill="{INK3}" letter-spacing="3">{eyebrow}</text>',
            f'  <line x1="32" y1="56" x2="968" y2="56" stroke="{RULE}" stroke-width="1"/>']


# ----------------------------------------------------------------- 08·B ÇARK
def orbit():
    gruplar = {k: v for k, _, v in TREE}
    halkalar = [  # (yarıçap, saniye, yön, simgeler, etiket)
        (86, 90, 1, gruplar["LANGUAGES"] + gruplar["GAME ENGINES"], "languages · engines"),
        (152, 130, -1, gruplar["BACKEND · API"] + gruplar["DATA"], "backend · data"),
        (218, 170, 1, gruplar["ML · VISION"] + gruplar["MEDIA · REAL-TIME"] + gruplar["FRONTEND"]
         + gruplar["OPS · DELIVERY"], "vision · media · frontend · ops"),
    ]
    cx, cy, H = 300, 312, 566
    css = ["@keyframes don{to{transform:rotate(360deg);}} @keyframes ters{to{transform:rotate(-360deg);}}"]
    for i, (_, sn, yon, _, _) in enumerate(halkalar):
        a, b = ("don", "ters") if yon > 0 else ("ters", "don")
        css.append(f".h{i}{{transform-origin:{cx}px {cy}px;animation:{a} {sn}s linear infinite;}}"
                   f" .h{i} .k{{transform-origin:0px 0px;animation:{b} {sn}s linear infinite;}}")
    toplam = sum(len(h[3]) for h in halkalar)
    s = head(H, f"Toolchain orbit — {toplam} technologies on three rotating rings", "gob",
             "08·B — TOOLCHAIN · ORBIT", " ".join(css))
    for r, *_ in halkalar:
        s.append(f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{WIRE}" stroke-width="1" stroke-dasharray="2 5"/>')
    # merkez
    s.append(f'  <circle cx="{cx}" cy="{cy}" r="44" fill="{BOX}" stroke="{WIRE}"/>')
    s.append(f'  <text x="{cx}" y="{cy+8}" text-anchor="middle" class="disp" font-size="34" fill="{INK}">{toplam}</text>')
    s.append(f'  <text x="{cx}" y="{cy+25}" text-anchor="middle" class="data" font-size="8.5" fill="{INK3}" letter-spacing="1.5">TOOLS</text>')
    for i, (r, _, _, simgeler, _) in enumerate(halkalar):
        s.append(f'  <g class="h{i}">')
        for j, (slug, ad, renk) in enumerate(simgeler):
            aci = 2 * math.pi * j / len(simgeler) - math.pi / 2 + i * 0.35
            x, y = cx + r * math.cos(aci), cy + r * math.sin(aci)
            s.append(f'    <g transform="translate({x:.1f},{y:.1f})"><g class="k"><title>{esc(ad)}</title>'
                     f'<rect x="-17" y="-17" width="34" height="34" rx="8" fill="{BOX}" stroke="{WIRE}"/>'
                     f'<path transform="translate(-9,-9) scale(0.75)" fill="{renk}" d="{fetch_path(slug)}"/></g></g>')
        s.append("  </g>")
    # sağ panel: halka künyesi
    x0 = 600
    s.append(f'  <text x="{x0}" y="96" class="title" font-size="12" fill="{INK}" letter-spacing="1.5">THREE RINGS, INSIDE OUT</text>')
    s.append(f'  <text x="{x0}" y="113" class="lbl" font-size="10.5" fill="{INK3}">the same 33 tools as the capability tree, ringed by layer</text>')
    y = 150
    for i, (r, sn, yon, simgeler, etiket) in enumerate(halkalar):
        s.append(f'  <line x1="{x0}" y1="{y-18}" x2="958" y2="{y-18}" stroke="#161d2b"/>')
        s.append(f'  <text x="{x0}" y="{y}" class="data" font-size="10" fill="{INK3}" letter-spacing="1.5">RING {i+1}</text>')
        s.append(f'  <text x="{x0+62}" y="{y}" class="lbl" font-size="12" fill="{INK}">{esc(etiket)}</text>')
        s.append(f'  <text x="958" y="{y}" text-anchor="end" class="data" font-size="12" fill="{INK}">{len(simgeler)}</text>')
        adlar = [a for _, a, _ in simgeler]
        satirlar, cur = [], ""
        for a in adlar:
            ek = (" · " if cur else "") + a
            if len(cur + ek) > 54:
                satirlar.append(cur)
                cur = a
            else:
                cur += ek
        satirlar.append(cur)
        for k, t in enumerate(satirlar):
            s.append(f'  <text x="{x0+62}" y="{y+18+k*15}" class="data" font-size="9.5" fill="{INK2}">{esc(t)}</text>')
        s.append(f'  <text x="{x0+62}" y="{y+22+len(satirlar)*15}" class="data" font-size="8.5" fill="{INK3}">'
                 f'r {r} · one turn per {sn} s · {"clockwise" if yon > 0 else "counter-clockwise"}</text>')
        y += 52 + len(satirlar) * 15 + 22
    s.append(f'  <text x="{x0}" y="{H-28}" class="lbl" font-size="9" fill="{INK3}">Logos are trademarks of their owners · icon paths from simple-icons (CC0)</text>')
    s.append("</svg>")
    (ASSETS / "orbit.svg").write_text("\n".join(s), encoding="utf-8")
    print("orbit.svg", toplam, "simge")


# ----------------------------------------------------------------- 00 ETKİNLİK
# İmza commit kutularıyla yazılır. 7 satırlık ızgarada el yazısı okunmaz; bu yüzden her commit kutusu
# 3×3 alt kutuya bölünür (3 px kutu + 1 px boşluk = 11 px, büyük kutuyla birebir hizalı) ve imza bu
# 159×21'lik ızgaraya basılır. Alt kutular kalemin gerçek çizim sırasıyla yanar; sonra her biri kendi
# büyük kutusunun merkezine toplanır ve imza commit haritasına dönüşür.
# Harfler Allura'dan (SIL OFL 1.1, google/fonts): bu çözünürlükte en okunur el yazısı o çıktı.
# Font yalnız derlemede okunur. Boş alt ızgara tek bir <pattern> ile çizilir.
FONT = VERI / "font" / "Allura-Regular.ttf"
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/allura/Allura-Regular.ttf"
IMZA = "Bedirhan Çetin"
ALT, ALT_BOS = 3, 1          # alt kutu kenarı ve aralığı (px)


def imza_hucre(x0, y0, c, g, sutun, t0, rampa, sure=2.6):
    """Döndürür: (svg satırları, css, yazım bitiş anı, {(hafta, gün): toplanma gecikmesi için anahtar})."""
    import numpy as np
    from fontTools.pens.basePen import BasePen
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.recordingPen import DecomposingRecordingPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont
    from PIL import Image, ImageDraw, ImageFont

    if not FONT.exists():
        FONT.parent.mkdir(parents=True, exist_ok=True)
        import urllib.request
        urllib.request.urlretrieve(FONT_URL, FONT)
    f = TTFont(FONT)
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm

    class Duz(BasePen):
        """Konturu kırık çizgiye açar (kalemin geçtiği noktalar, sırasıyla)."""
        def __init__(self):
            super().__init__(None)
            self.yollar, self.cur = [], []

        def _moveTo(self, p):
            self.cur = [p]

        def _lineTo(self, p):
            self.cur.append(p)

        def _curveToOne(self, a, b, p):
            s0 = self.cur[-1]
            for i in range(1, 13):
                t = i / 12
                u = 1 - t
                self.cur.append((u**3*s0[0] + 3*u*u*t*a[0] + 3*u*t*t*b[0] + t**3*p[0],
                                 u**3*s0[1] + 3*u*u*t*a[1] + 3*u*t*t*b[1] + t**3*p[1]))

        def _qCurveToOne(self, a, p):
            s0 = self.cur[-1]
            for i in range(1, 9):
                t = i / 8
                u = 1 - t
                self.cur.append((u*u*s0[0] + 2*u*t*a[0] + t*t*p[0], u*u*s0[1] + 2*u*t*a[1] + t*t*p[1]))

        def _closePath(self):
            self.cur.append(self.cur[0])
            self.yollar.append(self.cur)
            self.cur = []

        _endPath = _closePath

    # harfler: (ilerleme, kayıt)
    harfler, ilerle = [], 0
    for ch in IMZA:
        ad = cmap[ord(ch)]
        if ch != " ":
            rp = DecomposingRecordingPen(gs)
            gs[ad].draw(rp)
            harfler.append((ch, ilerle, rp.value))
        ilerle += gs[ad].width

    def oynat(kayit, pen):
        for op, args in kayit:
            getattr(pen, op)(*args)

    bp = BoundsPen(gs)
    for _, dx, k in harfler:
        oynat(k, TransformPen(bp, (1, 0, 0, 1, dx, 0)))
    xmin, ymin, xmax, ymax = bp.bounds

    gen, yuk = sutun * (c + g) - g, 7 * (c + g) - g          # ızgaranın piksel boyutu
    kx, ky, kw, kh = 30, 1, gen - 60, yuk - 2               # imza kutusu (ızgaraya göre)
    s = min(kw / (xmax - xmin), kh / (ymax - ymin))
    ox = kx + (kw - (xmax - xmin) * s) / 2 - xmin * s
    oy = ky + kh / 2 + (ymax + ymin) / 2 * s                  # taban çizgisi (y aşağı)

    # kalem yolları: harf sırası, harf içinde konturlar
    yollar = []
    for _, dx, k in harfler:
        d = Duz()
        oynat(k, TransformPen(d, (s, 0, 0, -s, ox + dx * s, oy)))
        yollar += [y for y in d.yollar if len(y) > 2]
    # zamanlama: her yol uzunluğu oranında süre alır, yollar biraz üst üste biner (el akışı)
    def uzunluk(y):
        a = np.asarray(y)
        return float(np.hypot(*np.diff(a, axis=0).T).sum())

    tum = yollar
    uz = [uzunluk(y) for y in tum]
    birim = sure / (sum(uz) * 0.6)
    noktalar, t = [], t0
    for i, (y, u) in enumerate(zip(tum, uz)):
        d = u * birim
        a = np.asarray(y)
        kum = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(a, axis=0).T))])
        for (px, py), k in zip(a, kum):
            noktalar.append((t + d * k / max(kum[-1], 1e-6), px, py))
        t += d * 0.6
    yazim_son = max(n[0] for n in noktalar)
    N = np.asarray(noktalar)

    # raster: yüksek çözünürlükte doldur, alt kutu başına kaplama oranı
    K = 8
    im = Image.new("L", (gen * K, yuk * K), 0)
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(str(FONT), round(s * upm * K))
    for ch, dx, _ in harfler:
        dr.text(((ox + dx * s) * K, oy * K), ch, font=font, fill=255, anchor="ls", stroke_width=round(0.6 * K), stroke_fill=255)
    m = np.asarray(im, dtype=np.float32) / 255

    def alt_konum(i):            # alt kutu indeksi → ızgaraya göre piksel
        return (i // 3) * (c + g) + (i % 3) * (ALT + ALT_BOS)

    rect, kutular = [], {}
    for sc in range(sutun * 3):
        ax = alt_konum(sc)
        for sr in range(21):
            ay = alt_konum(sr)
            kap = float(m[ay*K:(ay+ALT)*K, ax*K:(ax+ALT)*K].mean())
            if kap < 0.10:
                continue
            sev = 2 + (kap > 0.22) + (kap > 0.45)
            cx, cy = ax + ALT / 2, ay + ALT / 2
            tz = float(N[np.argmin((N[:, 1] - cx) ** 2 + (N[:, 2] - cy) ** 2), 0])
            wi, di = sc // 3, sr // 3
            # toplanırken alt kutu büyük kutunun merkezine kayar
            mx, my = wi * (c + g) + c / 2, di * (c + g) + c / 2
            rect.append((tz, wi, di, f'x="{x0+ax}" y="{y0+ay}" width="{ALT}" height="{ALT}" rx="0.8" fill="{rampa[sev]}" '
                                     f'style="--dx:{mx-cx:.1f}px;--dy:{my-cy:.1f}px;animation-delay:{tz:.2f}s,TOPLA_{wi}_{di}s"'))
            kutular[(wi, di)] = True

    # kalem ucu: yazım boyunca 90 anahtar karede yolu izler
    ks = []
    for q in np.linspace(0, 1, 90):
        tq = t0 + q * (yazim_son - t0)
        j = int(np.argmin(np.abs(N[:, 0] - tq)))
        ks.append(f"{q*100:.1f}%{{transform:translate({x0+N[j,1]:.1f}px,{y0+N[j,2]:.1f}px);}}")
    css = (
        "@keyframes yak{0%{opacity:0;transform:scale(.2);}55%{opacity:1;transform:scale(1.6);}100%{opacity:1;transform:scale(1);}}"
        " @keyframes topla{from{opacity:1;transform:translate(0,0) scale(1);}"
        "to{opacity:0;transform:translate(var(--dx),var(--dy)) scale(2.6);}}"
        " .sc{opacity:0;transform-box:fill-box;transform-origin:center;animation-name:yak,topla;"
        "animation-duration:.4s,.75s;animation-timing-function:cubic-bezier(.2,.8,.3,1),cubic-bezier(.5,0,.3,1);"
        "animation-fill-mode:forwards,forwards;}"
        f" @keyframes ucyol{{{''.join(ks)}}}"
        " @keyframes ucgor{0%{opacity:0;}4%{opacity:1;}94%{opacity:1;}100%{opacity:0;}}"
        f" .ucu{{animation:ucyol {yazim_son-t0:.2f}s linear {t0:.2f}s both,ucgor {yazim_son-t0:.2f}s linear {t0:.2f}s both;}}"
    )
    uc = (f'<g class="ucu"><circle r="7" fill="{ACCENT}" opacity=".22"/>'
          f'<circle r="2.4" fill="#ffffff"/></g>')
    desen = ('<defs><pattern id="altiz" x="{x}" y="{y}" width="{p}" height="{p}" patternUnits="userSpaceOnUse">'.format(x=x0, y=y0, p=c + g)
             + "".join(f'<rect x="{i*(ALT+ALT_BOS)}" y="{j*(ALT+ALT_BOS)}" width="{ALT}" height="{ALT}" rx="0.8" fill="{rampa[0]}"/>'
                       for i in range(3) for j in range(3))
             + f'</pattern></defs><rect class="altiz" x="{x0}" y="{y0}" width="{gen}" height="{yuk}" fill="url(#altiz)"/>')
    return sorted(rect), uc, css, yazim_son, desen


def activity():
    tak = json.loads((VERI / "takvim.json").read_text(encoding="utf-8"))["data"]["viewer"][
        "contributionsCollection"]["contributionCalendar"]
    hafta = tak["weeks"]
    sayilar = [g["contributionCount"] for w in hafta for g in w["contributionDays"]]
    aktif = sum(1 for c in sayilar if c)
    pozitif = sorted(c for c in sayilar if c)
    esikler = [pozitif[int(len(pozitif) * q)] for q in (0.25, 0.5, 0.75)] if pozitif else [1, 2, 3]
    rampa = ["#111826", "#4a1424", "#7a1030", "#b00836", ACCENT]   # tek renkli sıralı rampa

    def seviye(c):
        return 0 if c == 0 else 1 + sum(c > e for e in esikler)

    seri = en = 0
    for c in sayilar:
        seri = seri + 1 if c else 0
        en = max(en, seri)

    hw = json.loads((VERI / "haftalik.json").read_text(encoding="utf-8"))
    satirlar = sorted(((ad, hw["seri"][d]) for d, ad in PROJE), key=lambda t: -sum(t[1]))

    # zaman çizelgesi (saniye): imza yazılır → bekler → tarama çizgisinin ilk geçişi haritayı açar
    # (çizginin ulaştığı sütunda imza kutuları toplanır, boş kutular ve commit'ler kıvılcımla çıkar)
    # → çubuklar yükselir → çizgi her TUR saniyede bir dolaşıp commit'li hücreleri parlatır
    x0, y0, c, g = 216, 84, 11, 3
    alt_kutular, uc, imza_css, imza_bit, desen = imza_hucre(x0, y0, c, g, len(hafta), 0.3, rampa)
    gezi = len(hafta) * (c + g)
    ILK0, ILK = imza_bit + 1.0, 3.8       # ilk geçiş: başlangıç ve süre
    TUR, TARA0 = 9, ILK0 + ILK + 1.6      # sonraki turlar
    CUBUK0 = ILK0 + ILK + 0.2

    def varis(x):                         # çizginin ilk geçişte x'e vardığı an
        return ILK0 + ILK * (x - x0 + 2) / gezi

    top = 254
    H = top + len(satirlar) * 24 + 40
    css = (
        f"{imza_css}"
        f" @keyframes sonuk{{to{{opacity:0;}}}} .altiz{{animation:sonuk .6s ease-in-out {ILK0+ILK:.2f}s forwards;}}"
        " @keyframes belir{0%{opacity:0;transform:scale(.3);}45%{opacity:1;transform:scale(1.3);}100%{opacity:1;transform:scale(1);}}"
        " @keyframes bosgel{from{opacity:0;}to{opacity:1;}}"
        " @keyframes flas{0%{opacity:0;transform:scale(1);}12%{opacity:.95;transform:scale(1.55);}"
        "40%{opacity:.45;transform:scale(1.15);}100%{opacity:0;transform:scale(1);}}"
        " @keyframes yuksel{from{transform:scaleY(0);}to{transform:scaleY(1);}}"
        " @keyframes sol{from{opacity:0;}to{opacity:1;}}"
        f" @keyframes tara{{0%{{transform:translateX(0);opacity:0;}}6%{{opacity:.8;}}94%{{opacity:.8;}}"
        f"100%{{transform:translateX({gezi}px);opacity:0;}}}}"
        f" @keyframes tara1{{0%{{transform:translateX(0);opacity:0;}}3%{{opacity:1;}}96%{{opacity:1;}}"
        f"100%{{transform:translateX({gezi}px);opacity:0;}}}}"
        " .ge,.cb,.bs{transform-box:fill-box;transform-origin:center;}"
        " .ge{opacity:0;animation:belir .55s cubic-bezier(.2,.8,.3,1) forwards;}"
        " .bs{opacity:0;animation:bosgel .25s ease-out forwards;}"
        " .cb{transform-origin:bottom;transform:scaleY(0);animation:yuksel .7s cubic-bezier(.2,.8,.2,1) forwards;}"
        " .sl{opacity:0;animation:sol .8s ease-out forwards;}"
        f" .tarayici{{opacity:0;animation:tara1 {ILK}s linear {ILK0:.2f}s,tara {TUR}s linear {TARA0:.2f}s infinite;}}"
        " @keyframes kivilcim{0%{opacity:0;transform:scale(1);}1.2%{opacity:.9;transform:scale(1.45);}"
        "4%{opacity:.5;transform:scale(1.15);}10%{opacity:0;transform:scale(1);}100%{opacity:0;}}"
        " .kv{opacity:0;transform-box:fill-box;transform-origin:center;animation:flas .9s ease-out,kivilcim var(--t) linear infinite;}"
        " @keyframes yanip{0%,100%{opacity:.35;}50%{opacity:1;}} .bas{animation:yanip .9s ease-in-out infinite;}"
        " @media (prefers-reduced-motion: reduce){.sc,.ucu,.altiz{display:none;}.kv,.tarayici{opacity:0 !important;}"
        ".ge,.sl,.bs{opacity:1 !important;transform:none !important;}.cb{transform:none !important;}}"
    )
    s = head(H, f"Activity — signed BEDİRHAN ÇETİN, then {tak['totalContributions']:,} contributions in the past year "
                "and weekly commits per project", "gac", "00 — ACTIVITY · COMMITS", css)

    # sol künye — dönüşle birlikte belirir
    s.append(f'  <g class="sl" style="animation-delay:{ILK0:.2f}s">')
    s.append(f'  <text x="42" y="104" class="disp" font-size="34" fill="{INK}">{tak["totalContributions"]:,}</text>')
    s.append(f'  <text x="42" y="122" class="lbl" font-size="10.5" fill="{INK2}">contributions, past 12 months</text>')
    for k, (v, e) in enumerate(((str(aktif), "active days"), (str(max(sayilar)), "busiest day"), (f"{en} days", "longest streak"))):
        y = 146 + k * 24
        s.append(f'  <text x="42" y="{y}" class="data" font-size="13" fill="{INK}">{v}</text>')
        s.append(f'  <text x="42" y="{y+12}" class="lbl" font-size="9" fill="{INK3}">{e}</text>')
    s.append("  </g>")

    # ısı haritası: boş ızgara (sabit) + gerçek hücreler (dalga) + imza hücreleri (yazılır, söner)
    ay_once, son_etiket = None, -9
    bos, gercek = [], []
    for wi, w in enumerate(hafta):
        ilk = w["contributionDays"][0]["date"]
        if ilk[5:7] != ay_once and wi < len(hafta) - 2 and wi - son_etiket >= 3:
            ay_once, son_etiket = ilk[5:7], wi
            s.append(f'  <text class="sl data" style="animation-delay:{varis(x0 + wi*(c+g)):.2f}s" x="{x0 + wi*(c+g)}" y="{y0-6}" '
                     f' font-size="8.5" fill="{INK3}">{dt.date.fromisoformat(ilk).strftime("%b")}</text>')
        for gun in w["contributionDays"]:
            di = dt.date.fromisoformat(gun["date"]).isoweekday() % 7
            x, y = x0 + wi * (c + g), y0 + di * (c + g)
            bos.append(f'<rect class="bs" style="animation-delay:{varis(x):.2f}s" x="{x}" y="{y}" width="{c}" height="{c}" rx="2"/>')
            sv = seviye(gun["contributionCount"])
            if sv:
                gercek.append(f'<rect class="ge" style="animation-delay:{varis(x):.2f}s" x="{x}" y="{y}" width="{c}" height="{c}" '
                              f'rx="2" fill="{rampa[sv]}"><title>{gun["date"]}: {gun["contributionCount"]}</title></rect>')
    # katman sırası: alt ızgara → (çizgiyle gelen) boş kutular onu örter → commit'ler → imza kutuları
    s.append("  " + desen)
    s.append(f'  <g fill="{rampa[0]}">' + "".join(bos) + "</g>")
    s.append("  <g>" + "".join(gercek) + "</g>")
    parca = []
    for _, wi, di, oz in alt_kutular:
        topla = varis(x0 + wi * (c + g)) - 0.12      # çizgi gelmeden hemen önce kendi kutusuna toplanır
        parca.append(f'<rect class="sc" {oz.replace(f"TOPLA_{wi}_{di}", f"{topla:.2f}")}/>')
    s.append("  <g>" + "".join(parca) + "</g>")
    s.append("  " + uc)
    # tarayıcı geçerken dolu hücreler kıvılcımlanır: ilk geçişte bir kez (flas), sonra her turda
    kv = []
    for wi, w in enumerate(hafta):
        for gun in w["contributionDays"]:
            if gun["contributionCount"]:
                di = dt.date.fromisoformat(gun["date"]).isoweekday() % 7
                x, y = x0 + wi * (c + g), y0 + di * (c + g)
                t = TARA0 + TUR * (x - x0 + 2) / gezi
                kv.append(f'<rect class="kv" style="--t:{TUR}s;animation-delay:{varis(x):.2f}s,{t:.2f}s" x="{x}" y="{y}" width="{c}" height="{c}" rx="2"/>')
    s.append('  <g fill="#ffd2dc">' + "".join(kv) + "</g>")
    for di, ad in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        s.append(f'  <text class="sl data" style="animation-delay:{ILK0:.2f}s" x="{x0-8}" y="{y0 + di*(c+g) + 9}" '
                 f'text-anchor="end" font-size="8" fill="{INK3}">{ad}</text>')
    yuk = 7 * (c + g) + 1
    s.append(f'  <defs><linearGradient id="iz" x1="0" x2="1"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/>'
             f'<stop offset="1" stop-color="{ACCENT}" stop-opacity=".28"/></linearGradient></defs>')
    s.append(f'  <g class="tarayici"><rect x="{x0-64}" y="{y0-2}" width="62" height="{yuk}" fill="url(#iz)"/>'
             f'<rect x="{x0-2}" y="{y0-2}" width="2" height="{yuk}" fill="#ffffff"/>'
             f'<circle class="bas" cx="{x0-1}" cy="{y0-6}" r="3" fill="{ACCENT}"/>'
             f'<circle class="bas" cx="{x0-1}" cy="{y0+yuk+2}" r="3" fill="{ACCENT}"/></g>')
    sag = x0 + len(hafta) * (c + g) - g
    ly = y0 + 7 * (c + g) + 14
    s.append(f'  <g class="sl" style="animation-delay:{ILK0+ILK:.2f}s">')
    s.append(f'  <text x="{sag}" y="{ly+9}" text-anchor="end" class="data" font-size="8.5" fill="{INK3}">more</text>')
    for k, r in enumerate(reversed(rampa)):
        s.append(f'  <rect x="{sag-30-(k+1)*14}" y="{ly}" width="{c}" height="{c}" rx="2" fill="{r}"/>')
    s.append(f'  <text x="{sag-30-5*14-6}" y="{ly+9}" text-anchor="end" class="data" font-size="8.5" fill="{INK3}">less</text>')
    s.append("  </g>")

    # proje başına haftalık commit — çubuklar sırayla yükselir
    s.append(f'  <line x1="32" y1="{top-36}" x2="968" y2="{top-36}" stroke="{RULE}"/>')
    s.append(f'  <text x="42" y="{top-16}" class="title" font-size="12" fill="{INK}" letter-spacing="1.5">COMMITS PER WEEK · LAST 26 WEEKS</text>')
    s.append(f'  <text x="958" y="{top-16}" text-anchor="end" class="data" font-size="9" fill="{INK3}">each row scaled to its own busiest week · total on the right</text>')
    bx, bw, bh = 170, 22, 16
    for k, (ad, say) in enumerate(satirlar):
        y = top + k * 24
        mx = max(say) or 1
        t0 = CUBUK0 + k * 0.07
        s.append(f'  <g class="sl" style="animation-delay:{t0:.2f}s">')
        s.append(f'  <text x="158" y="{y+12}" text-anchor="end" class="lbl" font-size="11" fill="{INK2}">{esc(ad)}</text>')
        s.append(f'  <line x1="{bx}" y1="{y+bh}" x2="{bx+26*bw}" y2="{y+bh}" stroke="#161d2b"/>')
        s.append("  </g>")
        for wi, v in enumerate(say):
            if v:
                h = max(2, round(bh * v / mx))
                s.append(f'  <rect class="cb" style="animation-delay:{t0 + 0.15 + wi*0.018:.2f}s" x="{bx + wi*bw + 1}" y="{y+bh-h}" '
                         f'width="{bw-2}" height="{h}" rx="1.5" fill="{ACCENT}" opacity="{0.35 + 0.65*v/mx:.2f}">'
                         f'<title>{esc(ad)}, week {wi+1}: {v}</title></rect>')
        s.append(f'  <g class="sl" style="animation-delay:{t0+0.6:.2f}s">')
        s.append(f'  <text x="{bx+26*bw+16}" y="{y+12}" class="data" font-size="11" fill="{INK}">{sum(say):,}</text>')
        s.append(f'  <text x="958" y="{y+12}" text-anchor="end" class="data" font-size="9" fill="{INK3}">'
                 f'{sum(1 for v in say if v)}/26 weeks active</text>')
        s.append("  </g>")
    bas = dt.date.fromisoformat(hw["baslangic"])
    s.append(f'  <text x="{bx}" y="{H-18}" class="data" font-size="8.5" fill="{INK3}">{bas.strftime("%d %b %Y")}</text>')
    s.append(f'  <text x="{bx+26*bw}" y="{H-18}" text-anchor="end" class="data" font-size="8.5" fill="{INK3}">this week</text>')
    s.append("</svg>")
    (ASSETS / "activity.svg").write_text("\n".join(s), encoding="utf-8")
    print("activity.svg", tak["totalContributions"], "katkı,", len(satirlar), "proje,", len(alt_kutular), "alt kutu, imza biter", round(imza_bit, 2), "sn")


# ----------------------------------------------------------------- 11·B KADRANLAR
def dials():
    kadran = [  # (değer 0–1, büyük yazı, başlık, alt satır, hedef)
        (0.8319, "83.2%", "Aegis", "line coverage · 1,765 tests", None),
        (0.632, "0.632", "Asfalya", "mAP@50 · five damage classes", None),
        (0.871, "87.1%", "Asfalya", "multi-pass capture · target 85%", 0.85),
        (1.0, "34/34", "Warden", "UE5 automation tests passing", None),
    ]
    diller = json.loads((VERI / "diller.json").read_text(encoding="utf-8"))
    pay = collections.Counter()
    for d in diller.values():
        t = sum(d.values())
        for k, v in (d.items() if t else []):
            pay[k] += v / t
    n = sum(pay.values())
    sira = ["Python", "HTML", "JavaScript", "TypeScript", "Luau", "C++", "CSS"]
    renk = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9"]   # doğrulanmış sıra
    dilim = [(k, pay[k] / n) for k in sira] + [("Other", sum(v for k, v in pay.items() if k not in sira) / n)]

    H = 306
    css = ("@keyframes dol{from{stroke-dashoffset:var(--L);}} .yay{animation:dol 2.2s cubic-bezier(.2,.7,.2,1) both;}"
           " @keyframes nefes{0%,100%{opacity:.35;}50%{opacity:1;}} .uc{animation:nefes 2.6s ease-in-out infinite;}")
    s = head(H, "Telemetry dials — measured ratios, and the language mix across repositories", "gdi",
             "11·B — TELEMETRY · DIALS", css)
    R, sw = 46, 7
    tam = 2 * math.pi * R * 0.75                      # 270° yay
    for i, (v, buyuk, bas, alt, hedef) in enumerate(kadran):
        cx, cy = 104 + i * 150, 156
        L = tam
        s.append(f'  <g transform="rotate(135 {cx} {cy})">')
        s.append(f'    <circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#161d2b" stroke-width="{sw}" stroke-linecap="round" '
                 f'stroke-dasharray="{tam:.1f} 999"/>')
        s.append(f'    <circle class="yay" style="--L:{L:.1f}" cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{ACCENT}" '
                 f'stroke-width="{sw}" stroke-linecap="round" stroke-dasharray="{tam*v:.1f} 999" stroke-dashoffset="0"/>')
        s.append("  </g>")
        uc = math.radians(135 + 270 * v)
        s.append(f'  <circle class="uc" cx="{cx + R*math.cos(uc):.1f}" cy="{cy + R*math.sin(uc):.1f}" r="5.5" fill="none" stroke="{ACCENT}" stroke-width="1.5"/>')
        if hedef:
            ha = math.radians(135 + 270 * hedef)
            s.append(f'  <line x1="{cx + (R-9)*math.cos(ha):.1f}" y1="{cy + (R-9)*math.sin(ha):.1f}" '
                     f'x2="{cx + (R+9)*math.cos(ha):.1f}" y2="{cy + (R+9)*math.sin(ha):.1f}" stroke="{INK}" stroke-width="2"/>')
        s.append(f'  <text x="{cx}" y="{cy+6}" text-anchor="middle" class="data" font-size="17" fill="{INK}">{buyuk}</text>')
        s.append(f'  <text x="{cx}" y="{cy+64}" text-anchor="middle" class="title" font-size="12" fill="{INK}">{esc(bas)}</text>')
        for k, parca in enumerate(alt.split(" · ")):
            s.append(f'  <text x="{cx}" y="{cy+80+k*13}" text-anchor="middle" class="lbl" font-size="9.5" fill="{INK3}">{esc(parca)}</text>')
    s.append(f'  <text x="42" y="{H-22}" class="lbl" font-size="9.5" fill="{INK3}">White tick marks a target. Every value comes from a test run or an evaluation on held-out data.</text>')

    # dil dağılımı: yatay %100 yığılmış çubuk + doğrudan etiketli liste
    x0, x1 = 656, 958
    s.append(f'  <line x1="{x0-28}" y1="76" x2="{x0-28}" y2="{H-40}" stroke="#161d2b"/>')
    s.append(f'  <text x="{x0}" y="92" class="title" font-size="12" fill="{INK}" letter-spacing="1.5">LANGUAGE MIX</text>')
    s.append(f'  <text x="{x0}" y="108" class="lbl" font-size="9.5" fill="{INK3}">{len(diller)} repositories, each weighted equally</text>')
    x, gen = x0, x1 - x0
    for (ad, p), r in zip(dilim, renk + ["#3a4560"]):
        w = gen * p
        if w >= 1:
            s.append(f'  <rect x="{x:.1f}" y="124" width="{max(1, w-2):.1f}" height="14" rx="2" fill="{r}"><title>{ad} {p*100:.1f}%</title></rect>')
        x += w
    for k, ((ad, p), r) in enumerate(zip(dilim, renk + ["#3a4560"])):
        col, row = k % 2, k // 2
        lx, ly = x0 + col * 156, 168 + row * 30
        s.append(f'  <rect x="{lx}" y="{ly-9}" width="10" height="10" rx="2" fill="{r}"/>')
        s.append(f'  <text x="{lx+16}" y="{ly}" class="lbl" font-size="11" fill="{INK2}">{ad}</text>')
        s.append(f'  <text x="{lx+140}" y="{ly}" text-anchor="end" class="data" font-size="11" fill="{INK}">{p*100:.1f}%</text>')
    s.append("</svg>")
    (ASSETS / "dials.svg").write_text("\n".join(s), encoding="utf-8")
    print("dials.svg", ", ".join(f"{a} {p*100:.1f}" for a, p in dilim))


if __name__ == "__main__":
    if "--cek" in sys.argv:
        cek()
    orbit()
    activity()
    dials()
