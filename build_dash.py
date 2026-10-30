# -*- coding: utf-8 -*-
"""Çark + etkinlik + kadran kartları.

orbit.svg     08·B  teknoloji çarkı: yetkinlik ağacındaki 33 simge üç halkada döner (portfolyodaki çarkın SVG'si)
activity.svg  11·C  son 12 ayın katkı ısı haritası + proje başına son 26 haftanın haftalık commit'leri
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


# ----------------------------------------------------------------- 11·C ETKİNLİK
def activity():
    tak = json.loads((VERI / "takvim.json").read_text(encoding="utf-8"))["data"]["viewer"][
        "contributionsCollection"]["contributionCalendar"]
    hafta = tak["weeks"]
    gunler = [g for w in hafta for g in w["contributionDays"]]
    sayilar = [g["contributionCount"] for g in gunler]
    aktif = sum(1 for c in sayilar if c)
    pozitif = sorted(c for c in sayilar if c)
    esikler = [pozitif[int(len(pozitif) * q)] for q in (0.25, 0.5, 0.75)] if pozitif else [1, 2, 3]
    # tek renkli sıralı rampa: boş → vurgunun dört adımı
    rampa = ["#111826", "#4a1424", "#7a1030", "#b00836", ACCENT]

    def seviye(c):
        if c == 0:
            return 0
        return 1 + sum(c > e for e in esikler)

    # en uzun ardışık aktif gün serisi
    seri = en = 0
    for c in sayilar:
        seri = seri + 1 if c else 0
        en = max(en, seri)

    hw = json.loads((VERI / "haftalik.json").read_text(encoding="utf-8"))
    satirlar = sorted(((ad, hw["seri"][d]) for d, ad in PROJE), key=lambda t: -sum(t[1]))
    top = 254
    H = top + len(satirlar) * 24 + 40
    css = ("@keyframes tara{0%{transform:translateX(0);opacity:0;}6%{opacity:.9;}94%{opacity:.9;}100%{transform:translateX(742px);opacity:0;}}"
           " .tarayici{animation:tara 9s linear infinite;}")
    s = head(H, f"Activity — {tak['totalContributions']:,} contributions in the past year and weekly commits per project",
             "gac", "11·C — ACTIVITY · COMMITS", css)

    # sol künye
    s.append(f'  <text x="42" y="104" class="disp" font-size="34" fill="{INK}">{tak["totalContributions"]:,}</text>')
    s.append(f'  <text x="42" y="122" class="lbl" font-size="10.5" fill="{INK2}">contributions, past 12 months</text>')
    for k, (v, e) in enumerate(((str(aktif), "active days"), (str(max(sayilar)), "busiest day"), (f"{en} days", "longest streak"))):
        y = 146 + k * 24
        s.append(f'  <text x="42" y="{y}" class="data" font-size="13" fill="{INK}">{v}</text>')
        s.append(f'  <text x="42" y="{y+12}" class="lbl" font-size="9" fill="{INK3}">{e}</text>')

    # ısı haritası
    x0, y0, c, g = 216, 84, 11, 3
    ay_once, son_etiket = None, -9
    for wi, w in enumerate(hafta):
        ilk = w["contributionDays"][0]["date"]
        if ilk[5:7] != ay_once and wi < len(hafta) - 2 and wi - son_etiket >= 3:
            ay_once, son_etiket = ilk[5:7], wi
            s.append(f'  <text x="{x0 + wi*(c+g)}" y="{y0-6}" class="data" font-size="8.5" fill="{INK3}">'
                     f'{dt.date.fromisoformat(ilk).strftime("%b")}</text>')
        for gun in w["contributionDays"]:
            di = (dt.date.fromisoformat(gun["date"]).isoweekday()) % 7
            s.append(f'  <rect x="{x0 + wi*(c+g)}" y="{y0 + di*(c+g)}" width="{c}" height="{c}" rx="2" '
                     f'fill="{rampa[seviye(gun["contributionCount"])]}"><title>{gun["date"]}: {gun["contributionCount"]}</title></rect>')
    for di, ad in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        s.append(f'  <text x="{x0-8}" y="{y0 + di*(c+g) + 9}" text-anchor="end" class="data" font-size="8" fill="{INK3}">{ad}</text>')
    s.append(f'  <rect class="tarayici" x="{x0-2}" y="{y0-2}" width="2" height="{7*(c+g)+1}" fill="{INK}" opacity="0"/>')
    # rampa açıklaması
    ly = y0 + 7 * (c + g) + 14
    s.append(f'  <text x="{x0+742}" y="{ly+9}" text-anchor="end" class="data" font-size="8.5" fill="{INK3}">more</text>')
    for k, r in enumerate(reversed(rampa)):
        s.append(f'  <rect x="{x0+742-30-(k+1)*14}" y="{ly}" width="{c}" height="{c}" rx="2" fill="{r}"/>')
    s.append(f'  <text x="{x0+742-30-5*14-6}" y="{ly+9}" text-anchor="end" class="data" font-size="8.5" fill="{INK3}">less</text>')

    # proje başına haftalık commit
    s.append(f'  <line x1="32" y1="{top-36}" x2="968" y2="{top-36}" stroke="{RULE}"/>')
    s.append(f'  <text x="42" y="{top-16}" class="title" font-size="12" fill="{INK}" letter-spacing="1.5">COMMITS PER WEEK · LAST 26 WEEKS</text>')
    s.append(f'  <text x="958" y="{top-16}" text-anchor="end" class="data" font-size="9" fill="{INK3}">each row scaled to its own busiest week · total on the right</text>')
    bx, bw, bh = 170, 22, 16
    for k, (ad, say) in enumerate(satirlar):
        y = top + k * 24
        mx = max(say) or 1
        s.append(f'  <text x="158" y="{y+12}" text-anchor="end" class="lbl" font-size="11" fill="{INK2}">{esc(ad)}</text>')
        s.append(f'  <line x1="{bx}" y1="{y+bh}" x2="{bx+26*bw}" y2="{y+bh}" stroke="#161d2b"/>')
        for wi, v in enumerate(say):
            if v:
                h = max(2, round(bh * v / mx))
                s.append(f'  <rect x="{bx + wi*bw + 1}" y="{y+bh-h}" width="{bw-2}" height="{h}" rx="1.5" fill="{ACCENT}" '
                         f'opacity="{0.35 + 0.65*v/mx:.2f}"><title>{esc(ad)}, week {wi+1}: {v}</title></rect>')
        s.append(f'  <text x="{bx+26*bw+16}" y="{y+12}" class="data" font-size="11" fill="{INK}">{sum(say):,}</text>')
        aktif_h = sum(1 for v in say if v)
        s.append(f'  <text x="958" y="{y+12}" text-anchor="end" class="data" font-size="9" fill="{INK3}">{aktif_h}/26 weeks active</text>')
    bas = dt.date.fromisoformat(hw["baslangic"])
    s.append(f'  <text x="{bx}" y="{H-18}" class="data" font-size="8.5" fill="{INK3}">{bas.strftime("%d %b %Y")}</text>')
    s.append(f'  <text x="{bx+26*bw}" y="{H-18}" text-anchor="end" class="data" font-size="8.5" fill="{INK3}">this week</text>')
    s.append("</svg>")
    (ASSETS / "activity.svg").write_text("\n".join(s), encoding="utf-8")
    print("activity.svg", tak["totalContributions"], "katkı,", len(satirlar), "proje")


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
