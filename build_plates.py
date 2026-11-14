# -*- coding: utf-8 -*-
"""Ekran levhaları — gerçek ürün ekran görüntülerini profilin teknik çizim diline oturtur.

Kaynak: portfolyodaki yayınlanmış ekran görüntüleri (xaena53.github.io/portfolio).
Yerleşim 1000 birimlik tuvalde tasarlanır, K katıyla raster'a basılır (retina için 2x).
Asfalya tespit kareleri Mapillary (CC BY-SA) kaynaklı; levhada kaynak notu yazar.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

KAYNAK = Path(r"C:/Users/pc/.gemini/antigravity/scratch/xaena53-portfolio/assets/projects")
ASSETS = Path(__file__).parent / "assets"
K = 2
BG, GRID, FRAME, RULE = "#0a0d13", "#131a26", "#1c2534", "#232d3f"
ACCENT, INK, INK2, INK3, TICK, WIRE = "#e8003d", "#e6e9ef", "#8b93a7", "#5c6579", "#3a4560", "#243044"
F = r"C:/Windows/Fonts/"


def font(ad, boy):
    return ImageFont.truetype(F + ad, round(boy * K))


MONO, LBL, BAS, DISP = "consola.ttf", "segoeui.ttf", "seguisb.ttf", "georgiab.ttf"


class Levha:
    def __init__(self, h, kas, baslik, alt, dwg):
        self.h = h
        self.im = Image.new("RGB", (1000 * K, h * K), BG)
        self.d = ImageDraw.Draw(self.im)
        for x in range(0, 1000, 28):
            self.d.line([(x * K, 0), (x * K, h * K)], fill=GRID, width=1)
        for y in range(0, h, 28):
            self.d.line([(0, y * K), (1000 * K, y * K)], fill=GRID, width=1)
        self.d.rectangle([0, 0, 1000 * K - 1, h * K - 1], outline=FRAME, width=K)
        self.kutu(42, 31, 6, 6, ACCENT)
        self.yaz(58, 30, kas, MONO, 10.5, INK3, aralik=3)
        self.yaz(42, 46, baslik, DISP, 21, INK)
        self.yaz(42, 76, alt, LBL, 11.5, INK2)
        # künye kutusu sağ üstte
        self.d.rectangle([782 * K, 34 * K, 968 * K, 64 * K], outline=RULE, width=1)
        self.yaz(790, 44, "DWG NO.", MONO, 9, INK3)
        self.yaz(960, 44, dwg, MONO, 9, INK2, sag=True)

    def kutu(self, x, y, w, h, renk):
        self.d.rectangle([x * K, y * K, (x + w) * K - 1, (y + h) * K - 1], fill=renk)

    def yaz(self, x, y, metin, ad, boy, renk, aralik=0, sag=False):
        f = font(ad, boy)
        if aralik:
            cx = x * K
            for ch in metin:
                self.d.text((cx, y * K), ch, font=f, fill=renk)
                cx += f.getlength(ch) + aralik * K
            return
        if sag:
            x = x - f.getlength(metin) / K
        self.d.text((x * K, y * K), metin, font=f, fill=renk)

    def ekran(self, dosya, x, y, w, h, etiket=None, not_=None, odak=(0.5, 0.5), telefon=False):
        src = Image.open(KAYNAK / dosya).convert("RGB")
        if telefon:
            # cihaz çerçevesi: yuvarlatılmış gövde + iç ekran
            r = 18
            self.d.rounded_rectangle([x * K, y * K, (x + w) * K, (y + h) * K], radius=r * K,
                                     fill="#0e131d", outline=WIRE, width=K)
            ix, iy, iw, ih = x + 7, y + 16, w - 14, h - 32
            img = ImageOps.fit(src, (iw * K, ih * K), Image.LANCZOS, centering=odak)
            maske = Image.new("L", img.size, 0)
            ImageDraw.Draw(maske).rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1], radius=6 * K, fill=255)
            self.im.paste(img, (ix * K, iy * K), maske)
            self.d.rounded_rectangle([(x + w / 2 - 14) * K, (y + 6) * K, (x + w / 2 + 14) * K, (y + 9) * K],
                                     radius=2 * K, fill=WIRE)
        else:
            img = ImageOps.fit(src, (w * K, h * K), Image.LANCZOS, centering=odak)
            self.im.paste(img, (x * K, y * K))
            self.d.rectangle([x * K, y * K, (x + w) * K - 1, (y + h) * K - 1], outline=WIRE, width=1)
            # köşe işaretleri, çizim dilindeki gibi
            t = 9
            for cx, cy, sx, sy in ((x - 4, y - 4, 1, 1), (x + w + 4, y - 4, -1, 1),
                                   (x - 4, y + h + 4, 1, -1), (x + w + 4, y + h + 4, -1, -1)):
                self.d.line([(cx * K, cy * K), ((cx + sx * t) * K, cy * K)], fill=TICK, width=K)
                self.d.line([(cx * K, cy * K), (cx * K, (cy + sy * t) * K)], fill=TICK, width=K)
        if etiket:
            ey = y + h + 10
            self.kutu(x, ey + 3, 14, 14, ACCENT)
            self.yaz(x + 3.6, ey + 3.2, etiket[0], BAS, 9.5, "#ffffff")
            self.yaz(x + 22, ey + 2, etiket[1], LBL, 11, INK)
            if not_:
                self.yaz(x + 22, ey + 18, not_, MONO, 9, INK3)

    def kaydet(self, ad):
        self.im.save(ASSETS / ad, quality=86, optimize=True, progressive=True)
        print(ad, self.im.size, (ASSETS / ad).stat().st_size // 1024, "KB")


def asfalya():
    L = Levha(522, "01·A — ASFALYA · FROM THE FIELD", "What the pipeline produces",
              "the damage map the public works desk works from, built from frames like the two on the right", "XR-004·A")
    L.ekran("asfalya-3.jpg", 42, 110, 590, 360, ("A", "Damage map of Eskişehir, demo dataset"),
            "neighbourhood score card · MapLibre + PostGIS")
    L.ekran("asfalya-1.jpg", 656, 110, 302, 140, ("B", "Alligator crack, confidence 0.72"),
            "frame: Mapillary, CC BY-SA", odak=(0.5, 0.55))
    L.ekran("asfalya-2.jpg", 656, 302, 302, 168, ("C", "Transverse and longitudinal cracks"),
            "frame: Mapillary, CC BY-SA", odak=(0.5, 0.6))
    L.kaydet("plate-asfalya.jpg")


def repchat():
    L = Levha(506, "05·A — REPCHAT · IN PRODUCTION", "Operator panel and widget",
              "the panel an agent works in, and the widget a visitor sees on their phone", "XR-011·A")
    L.ekran("repchat-4.jpg", 42, 110, 600, 343, ("A", "Operator inbox"),
            "priority tags · live thread · per-user file permissions")
    L.ekran("repchat-2.jpg", 674, 102, 136, 300, ("B", "Category picker"), telefon=True, odak=(0.5, 0.0))
    L.ekran("repchat-3.jpg", 826, 102, 136, 300, ("C", "Email code"), telefon=True, odak=(0.5, 0.0))
    L.kaydet("plate-repchat.jpg")


def warden():
    L = Levha(716, "08·A — WARDEN OF THE FIELDS · IN ENGINE", "Unreal Engine 5.8 captures",
              "editor captures from the vertical slice", "XR-020·A")
    L.ekran("warden-1.jpg", 42, 110, 916, 390, ("A", "Village square during a work cycle"),
            odak=(0.5, 0.55))
    for i, (f, e) in enumerate((("warden-2.jpg", "The general store"), ("warden-3.jpg", "The tavern at dusk"),
                                ("warden-4.jpg", "Village and fields from above"))):
        L.ekran(f, 42 + i * 316, 552, 284, 118, ("BCD"[i], e), odak=(0.5, 0.5))
    L.kaydet("plate-warden.jpg")


def musteri():
    L = Levha(342, "08·B — CLIENT WORK · LIVE", "Sites running for real clients",
              "ektakademi.com and cakmakpen.com.tr, both in production", "XR-021·A")
    for i, (f, e, n) in enumerate((("ekt-1.jpg", "EKT Akademi, home", "Node · Express 5 · PostgreSQL"),
                                   ("ekt-3.jpg", "EKT Akademi, programme page", "dynamic catalogue from the API"),
                                   ("cakmakpen-1.jpg", "Çakmak Pen, home", "static multi-page site"))):
        L.ekran(f, 42 + i * 312, 110, 292, 182, ("ABC"[i], e), n, odak=(0.5, 0.0))
    L.kaydet("plate-clients.jpg")


def kurenai():
    L = Levha(430, "04·A — KURENAI · OUTPUT", "Signs translated in place",
              "the kurenai.shop typeset engine: OCR finds on-screen text and redraws it in Turkish", "XR-012·A")
    L.ekran("kurenai-1.jpg", 42, 110, 440, 248, ("A", "kurenai.shop"), "landing page · quality score card",
            odak=(0.5, 0.0))
    L.ekran("kurenai-cell.jpg", 518, 110, 440, 248, ("B", "Station sign replaced in Turkish"),
            "before / after slider · Turkish set in perspective")
    L.kaydet("plate-kurenai.jpg")


def nobetci():
    L = Levha(716, "06·A — NÖBETÇİ MEMUR · IN GAME", "Seven days at window 2",
              "captures from the English build; the game also runs in Turkish and Russian", "XR-026·A")
    L.ekran("nobetci-1.jpg", 42, 110, 600, 338, ("A", "Inspection mode: click two facts, a line joins them"),
            "surname on the identity card against the residence certificate")
    L.ekran("nobetci-3.jpg", 666, 110, 292, 146, ("B", "Day 5: X-ray alarm on a handbag"), odak=(0.0, 1.0))
    L.ekran("nobetci-5.jpg", 666, 302, 292, 146, ("C", "Evening: the wage against the bills"), odak=(0.5, 0.35))
    for i, (f, e) in enumerate((("nobetci-4.jpg", "Reference book of seals"), ("nobetci-6.jpg", "The screen between days"),
                                ("nobetci-2.jpg", "Main menu"))):
        L.ekran(f, 42 + i * 316, 508, 284, 160, ("DEF"[i], e), odak=(0.5, 0.5))
    L.kaydet("plate-nobetci.jpg")


if __name__ == "__main__":
    asfalya()
    repchat()
    warden()
    musteri()
    kurenai()
    nobetci()
