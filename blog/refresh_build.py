# -*- coding: utf-8 -*-
"""Rebuild ONLY the refreshed posts (posts_refresh*.py) in TR/EN/AR/RU.

Never run build_blog.py's full __main__ for this: it drops the hreflang links and the
multilingual sitemap/llms.txt entries that were added in a separate step.
TR pages keep their existing hreflang block (copied from the current file).
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_blog as B
import build_blog_i18n as I
import posts_i18n_data as P
from posts_refresh import SLUGS

HREF_RE = re.compile(r'(?:<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?)+')

for slug in SLUGS:
    path = os.path.join(B.OUT, slug + ".html")
    old = open(path, encoding="utf-8").read()
    m = HREF_RE.search(old)
    B.build_post(B.BY_SLUG[slug])
    if m:
        new = open(path, encoding="utf-8").read()
        if 'hreflang="' not in new:
            new = re.sub(r'(<link rel="canonical" href="[^"]+">\n)', lambda c: c.group(1) + m.group(0), new, count=1)
            open(path, "w", encoding="utf-8").write(new)

I.SLUGS = set(P.POSTS.keys())
for slug in SLUGS:
    for lang in ("en", "ar", "ru"):
        data = P.POSTS[slug][lang]
        data["rel"] = I.REL_MAP[slug]
        I.build_post(lang, slug, data, P.POSTS)

print("Rebuilt %d posts x 4 languages" % len(SLUGS))
