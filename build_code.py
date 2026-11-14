# -*- coding: utf-8 -*-
"""Kendini yazan kod paneli (assets/code.svg).

Her satır kendi karakter sayısı kadar steps() ile dolar; karet aynı ritimle atlar.
Satırları değiştirmek için yalnız SATIRLAR listesini düzenle, zamanlama kendiliğinden çıkar.
"""
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"
CW = 7.45            # 13 px monospace'te bir karakterin genişliği
X0, Y0, DY = 56, 118, 22
SURE = 17            # saniye, döngü
YAZ_SONU = 74.0      # yazma bu yüzdede biter, kalanı bekleme + sönme

# (sınıf, metin) parçaları; sınıflar: kw anahtar kelime, fn ad, str dize, pn noktalama/düz
SATIRLAR = [
    [("kw", "export async function "), ("fn", "onayAl"), ("pn", "(server, ozet, confirm) {")],
    [("pn", "  "), ("kw", "const"), ("pn", " net = "), ("kw", "await "), ("fn", "networkTrust"), ("pn", "(ozet.risk);")],
    [("pn", "  "), ("kw", "if"), ("pn", " (net.swapped) "), ("kw", "return "), ("fn", "refuse"), ("pn", "("), ("str", "'sim-swap'"), ("pn", ");")],
    [("pn", "  "), ("kw", "if"), ("pn", " ("), ("fn", "canElicit"), ("pn", "(server))")],
    [("pn", "    "), ("kw", "return "), ("fn", "askHuman"), ("pn", "(server, ozet);")],
    [("pn", "  "), ("kw", "if"), ("pn", " (!confirm) "), ("kw", "return "), ("fn", "refuse"), ("pn", "("), ("str", "'no-consent'"), ("pn", ");")],
    [("pn", "  "), ("kw", "return "), ("fn", "approve"), ("pn", "("), ("str", "'confirm'"), ("pn", ", net);")],
    [("pn", "}")],
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    n = [sum(len(t) for _, t in s) for s in SATIRLAR]
    ara = 0.9                                   # satırlar arası duraklama, yüzde
    yazma = YAZ_SONU - ara * len(SATIRLAR)
    birim = yazma / sum(n)
    zaman, t = [], ara
    for k in n:
        bas, son = t, t + k * birim
        zaman.append((bas, son))
        t = son + ara

    clip, kf, cls, car = [], [], [], [f"0%{{transform:translate({X0}px,{Y0}px);}}"]
    for i, ((bas, son), k) in enumerate(zip(zaman, n), 1):
        y = Y0 + (i - 1) * DY
        w = round(k * CW)
        clip.append(f'<clipPath id="cl{i}"><rect class="clipL{i}" x="{X0}" y="{y}" width="0" height="18"/></clipPath>')
        kf.append(f"@keyframes clipL{i} {{ 0%{{width:0;}} {bas:.1f}%{{width:0;animation-timing-function:steps({k},end);}} "
                  f"{son:.1f}%{{width:{w}px;}} 100%{{width:{w}px;}} }}")
        cls.append(f".clipL{i}{{animation:clipL{i} {SURE}s linear infinite;}}")
        car.append(f"{bas:.1f}%{{transform:translate({X0}px,{y}px);animation-timing-function:steps({k},end);}}")
        car.append(f"{son:.1f}%{{transform:translate({X0 + w}px,{y}px);}}")
    son_y = Y0 + (len(SATIRLAR) - 1) * DY
    car.append(f"100%{{transform:translate({X0 + round(n[-1] * CW)}px,{son_y}px);}}")
    hepsi = ",".join(f".clipL{i}" for i in range(1, len(SATIRLAR) + 1))

    govde = []
    for i, s in enumerate(SATIRLAR, 1):
        y = Y0 + 14 + (i - 1) * DY
        parca = "".join(f'<tspan class="{c}">{esc(t)}</tspan>' for c, t in s)
        govde.append(f'    <g clip-path="url(#cl{i})"><text x="{X0}" y="{y}" class="data" font-size="13" xml:space="preserve">{parca}</text></g>')
    for i in range(1, len(SATIRLAR) + 1):
        y = Y0 + 14 + (i - 1) * DY
        govde.append(f'    <text x="944" y="{y}" text-anchor="end" class="data" font-size="10" fill="#3f4759">{i}</text>')

    H = 380
    svg = f'''<svg width="1000" height="{H}" viewBox="0 0 1000 {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Live build — the Aegis approval gate typing itself out">
  <defs>
    <pattern id="g6" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="#131a26" stroke-width="1"/>
    </pattern>
    {chr(10).join("    " + c for c in clip).strip()}
    <style>
      .lbl  {{ font-family:'Segoe UI',Helvetica,Arial,sans-serif; }}
      .data {{ font-family:'SF Mono',Consolas,'Cascadia Code',monospace; }}
      .kw   {{ fill:#7f93bd; }}
      .fn   {{ fill:#eef1f6; }}
      .str  {{ fill:#e8003d; }}
      .pn   {{ fill:#6b7488; }}
      {chr(10).join("      " + k for k in kf).strip()}
      {" ".join(cls)}
      @keyframes bodyVis {{ 0%{{opacity:0;}} 1%{{opacity:1;}} 90.2%{{opacity:1;}} 96.1%,100%{{opacity:0;}} }}
      .body {{ animation: bodyVis {SURE}s linear infinite; }}
      @keyframes caretMove {{ {" ".join(car)} }}
      @keyframes caretVis {{ 0%,0.9%{{opacity:0;}} 1.4%{{opacity:1;}} 90.2%{{opacity:1;}} 96.1%,100%{{opacity:0;}} }}
      .caret {{ animation: caretMove {SURE}s linear infinite, caretVis {SURE}s linear infinite; }}
      @keyframes caretBlink {{ 0%,100%{{ opacity:1; }} 50%{{ opacity:.15; }} }}
      .caretBlink {{ animation: caretBlink 0.95s step-end infinite; }}
      @media (prefers-reduced-motion: reduce) {{
        {hepsi} {{ animation:none !important; width:420px !important; }}
        .body,.caret,.caretBlink {{ animation:none !important; opacity:1; }}
        .caret {{ display:none; }}
      }}
    </style>
  </defs>

  <rect width="1000" height="{H}" fill="#0a0d13"/>
  <rect width="1000" height="{H}" fill="url(#g6)"/>
  <rect x="0.5" y="0.5" width="999" height="{H-1}" fill="none" stroke="#1c2534"/>

  <text x="32" y="38" class="data" font-size="10.5" fill="#5c6579" letter-spacing="3">10 — LIVE BUILD</text>
  <text x="32" y="60" class="lbl" font-size="18" font-weight="700" fill="#eef1f6">onayAl() — the Aegis approval gate</text>
  <text x="32" y="80" class="lbl" font-size="12" fill="#8993a8">simplified from src/approval.ts · the network is asked first, then the human, and the agent's own flag comes last</text>

  <rect x="32" y="98" width="936" height="234" fill="#0d1119" stroke="#232d3f" stroke-width="1"/>
  <path d="M32 98h10M32 98v10M968 98h-10M968 98v10M32 332h10M32 332v-10M968 332h-10M968 332v-10" stroke="#3a4560" stroke-width="1" fill="none"/>
  <text x="52" y="98" class="data" font-size="9" fill="#4d5567" transform="translate(0,-4)">approval.ts</text>

  <g class="body">
{chr(10).join(govde)}
  </g>

  <g class="caret">
    <rect class="caretBlink" x="0" y="0" width="7" height="15" fill="#e8003d"/>
  </g>

  <g>
    <rect x="782" y="340" width="186" height="30" fill="none" stroke="#232d3f" stroke-width="1"/>
    <text x="790" y="359" class="data" font-size="9" fill="#5c6579">DWG NO.</text>
    <text x="960" y="359" class="data" font-size="9" fill="#8993a8" text-anchor="end">XR-013 · REV 10.26</text>
  </g>
</svg>
'''
    (ASSETS / "code.svg").write_text(svg, encoding="utf-8")
    print("code.svg", len(svg), "bayt")


if __name__ == "__main__":
    main()
