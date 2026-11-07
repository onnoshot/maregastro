#!/usr/bin/env python3
"""Blog görsellerini hafifletir (idempotent).

Her blog sayfasındaki <img src="...images/<ad>.(jpg|jpeg|png|webp)"> için
images/b/<ad>.webp (en fazla 1400px genişlik, q78) üretir ve <img> etiketini ona çevirir.
Genişlik/yükseklik niteliği EKLENMEZ (CSS yalnızca yüksekliği verdiğinde boyutu bozar).
Paylaşım etiketleri (og:image, twitter:image) ve JSON-LD JPG olarak kalır (uyumluluk).

Kullanım: python3 -I scripts/optimize_blog_images.py
Blog üretildikten sonra (refresh_build.py bunu otomatik çağırır) tekrar çalıştırın.
"""
import glob, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "images")
OUT = os.path.join(IMG, "b")
MAXW, Q = 1400, 78
IMG_TAG = re.compile(r'<img\b[^>]*>')
SRC = re.compile(r'\bsrc="(?:\.\./|/)?images/(?!b/)([^"/]+)\.(jpg|jpeg|png|webp)"')


def variant(name, ext):
    """Return (webp file name, width, height) for images/<name>.<ext>, creating it if missing."""
    src = None
    for e in (ext, "webp", "jpg", "jpeg", "png"):  # prefer the referenced file, else any sibling
        p = os.path.join(IMG, "%s.%s" % (name, e))
        if os.path.exists(p):
            src = p
            break
    if not src:
        return None
    dst = os.path.join(OUT, name + ".webp")
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        im = Image.open(src)
        im = im.convert("RGBA") if (im.mode in ("RGBA", "LA", "P") and "transparency" in im.info or im.mode in ("RGBA", "LA")) else im.convert("RGB")
        if im.width > MAXW:
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        im.save(dst, "WEBP", quality=Q, method=6)
    with Image.open(dst) as im:
        return name + ".webp", im.width, im.height


def fix_tag(tag):
    if "srcset=" in tag:          # already responsive (e.g. chef portrait)
        return tag
    m = SRC.search(tag)
    if not m:
        return tag
    v = variant(m.group(1), m.group(2))
    if not v:
        return tag
    fn, w, h = v
    tag = SRC.sub('src="/images/b/%s"' % fn, tag, count=1)
    if " decoding=" not in tag:
        tag = tag.replace("<img ", '<img decoding="async" ', 1)
    return tag


def main():
    os.makedirs(OUT, exist_ok=True)
    files = glob.glob(os.path.join(ROOT, "blog", "*.html")) + glob.glob(os.path.join(ROOT, "*", "blog", "*.html"))
    changed = 0
    for f in files:
        s = open(f, encoding="utf-8").read()
        n = IMG_TAG.sub(lambda m: fix_tag(m.group(0)), s)
        if n != s:
            open(f, "w", encoding="utf-8").write(n)
            changed += 1
    size = sum(os.path.getsize(p) for p in glob.glob(os.path.join(OUT, "*.webp")))
    print("pages changed: %d · variants: %d · %.1f MB" % (changed, len(glob.glob(os.path.join(OUT, "*.webp"))), size / 1e6))


if __name__ == "__main__":
    main()
