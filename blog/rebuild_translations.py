# -*- coding: utf-8 -*-
"""Rebuild every EN/AR/RU translated post + the three blog indexes, and selected TR posts.

Usage: python3 -I blog/rebuild_translations.py [tr-slug ...]

- Translations: all posts in posts_i18n_data.POSTS (idempotent; body links are localized by
  build_blog_i18n.localize_links).
- TR: only the slugs given on the command line. Their existing hreflang block is kept; when a
  TR post has a translation but no hreflang yet, the full tr/en/ar/ru/x-default set is added.
- Never runs build_blog.py's __main__ (that would drop hreflang + multilingual sitemap entries).
- Finishes with scripts/optimize_blog_images.py, like refresh_build.py.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_blog as B
import build_blog_i18n as I
import posts_i18n_data as P

SITE = "https://maregastro.com"
HREF_RE = re.compile(r'(?:<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?)+')


def tr_hreflang(slug):
    links = ['<link rel="alternate" hreflang="tr" href="%s/blog/%s.html">' % (SITE, slug)]
    links += ['<link rel="alternate" hreflang="%s" href="%s/%s/blog/%s.html">' % (l, SITE, l, slug) for l in ("en", "ar", "ru")]
    links.append('<link rel="alternate" hreflang="x-default" href="%s/blog/%s.html">' % (SITE, slug))
    return "\n".join(links) + "\n"


def build_tr(slug):
    path = os.path.join(B.OUT, slug + ".html")
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    m = HREF_RE.search(old)
    block = m.group(0) if m else (tr_hreflang(slug) if slug in P.POSTS else "")
    B.build_post(B.BY_SLUG[slug])
    new = open(path, encoding="utf-8").read()
    if block and 'hreflang="' not in new:
        new = re.sub(r'(<link rel="canonical" href="[^"]+">\n)', lambda c: c.group(1) + block, new, count=1)
        open(path, "w", encoding="utf-8").write(new)


for slug in sys.argv[1:]:
    build_tr(slug)

I.SLUGS = set(P.POSTS.keys())
for slug, per_lang in P.POSTS.items():
    for lang in ("en", "ar", "ru"):
        per_lang[lang]["rel"] = I.REL_MAP[slug]
        I.build_post(lang, slug, per_lang[lang], P.POSTS)
for lang in ("en", "ar", "ru"):
    I.build_index(lang, list(P.POSTS.keys()), P.POSTS)
print("TR rebuilt: %d · translations: %d posts x 3 + 3 indexes" % (len(sys.argv) - 1, len(P.POSTS)))

subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(HERE), "scripts", "optimize_blog_images.py")], check=False)
