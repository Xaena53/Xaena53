# -*- coding: utf-8 -*-
"""README'deki her assets/ görseline içerik özetinden ?v= ekler.

GitHub görselleri raw/camo önbelleğinden verir; dosya adı aynı kalınca profil eski sürümü
göstermeye devam eder. Kartları yeniden ürettikten sonra commit'ten önce çalıştır.
"""
import hashlib
import re
from pathlib import Path

KOK = Path(__file__).parent
readme = KOK / "README.md"
s = readme.read_text(encoding="utf-8")


def damga(m):
    yol = m.group(1)
    v = hashlib.sha1((KOK / yol).read_bytes()).hexdigest()[:8]
    return f'src="{yol}?v={v}"'


yeni = re.sub(r'src="(assets/[^"?]+)(?:\?v=[0-9a-f]+)?"', damga, s)
readme.write_text(yeni, encoding="utf-8")
print(len(re.findall(r'\?v=', yeni)), "görsel damgalandı")
