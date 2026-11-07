#!/usr/bin/env python3
"""IndexNow: Bing / Yandex / Seznam / Naver'e değişen URL'leri bildirir (ChatGPT & Copilot aramaları Bing dizinini kullanır).

Kullanım:
  python3 -I scripts/indexnow.py https://maregastro.com/sss.html https://maregastro.com/blog/x.html
  python3 -I scripts/indexnow.py --since 2026-11-07     # sitemap'te lastmod >= tarih olan URL'ler
Anahtar dosyası sitenin kökünde: /1c88314831f504f2de33a57b70d3b5e4.txt (silmeyin; anahtar değişirse bu sabit de değişmeli).
Tekrar çalıştırmak güvenlidir (idempotent): aynı URL'yi yeniden bildirmek zararsızdır.
"""
import json, re, sys, urllib.request

HOST = "maregastro.com"
KEY = "1c88314831f504f2de33a57b70d3b5e4"
KEY_LOCATION = "https://%s/%s.txt" % (HOST, KEY)


def from_sitemap(since):
    xml = urllib.request.urlopen("https://%s/sitemap.xml" % HOST, timeout=30).read().decode()
    return [loc for loc, mod in re.findall(r"<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>", xml) if mod >= since]


def submit(urls):
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION, "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return "%s %s" % (e.code, e.read()[:200])


if __name__ == "__main__":
    args = sys.argv[1:]
    urls = from_sitemap(args[1]) if args[:1] == ["--since"] else args
    if not urls:
        sys.exit("URL yok")
    for i in range(0, len(urls), 1000):
        print(len(urls[i:i + 1000]), "URL ->", submit(urls[i:i + 1000]))
