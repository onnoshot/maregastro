#!/usr/bin/env python3
"""Mare Gastro çok-dilli site üretici.
Tek kaynak: ../index.html (Türkçe template) + i18n/{tr,en,ar,ru}.json
Üretir: /tr /en /ar /ru index.html  +  kök / dil-seçim açılış ekranı.
Idempotent: her çalıştırmada sıfırdan üretir.
"""
import json, re, os, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))      # .../i18n
PROJ = os.path.dirname(ROOT)                            # proje kökü
SITE = "https://maregastro.com"
LANGS = ["tr", "en", "ar", "ru"]
LOCALE   = {"tr": "tr_TR", "en": "en_US", "ar": "ar_AR", "ru": "ru_RU"}
JSLOCALE = {"tr": "tr-TR", "en": "en-US", "ar": "ar-SA", "ru": "ru-RU"}
LANGNAME = {"tr": "Türkçe", "en": "English", "ar": "العربية", "ru": "Русский"}
FLAG     = {"tr": "🇹🇷", "en": "🇬🇧", "ar": "🇸🇦", "ru": "🇷🇺"}
RTL = {"ar"}

tr = json.load(open(f"{ROOT}/tr.json", encoding="utf-8"))
strings = {}
for l in LANGS:
    strings[l] = json.load(open(f"{ROOT}/{l}.json", encoding="utf-8")) if l != "tr" else tr

src = open(f"{ROOT}/source.html", encoding="utf-8").read()

# ── 1. Göreli yolları mutlak yap (alt klasörlerden /images ve /blog çalışsın) ──
src = src.replace('"images/', '"/images/').replace("'images/", "'/images/").replace("(images/", "(/images/")
src = src.replace('href="blog/"', 'href="/blog/"')

# ── 2. WhatsApp mesaj template literal'ini koru (ekibe Türkçe gitsin) ──
m = re.search(r"const msg=`[^`]*`;", src)
WAMSG = m.group(0)
src = src.replace(WAMSG, "@@WAMSG@@")

# ── 2b. MENU_I18N JS objesini koru (4 dili kendi içinde barındırır,
#         tokenizer'ın "Başlangıçlar" gibi metinleri yanlış dille değiştirmesini önler) ──
m2 = re.search(r"const MENU_I18N = \{.*?\n\};", src, re.S)
MENUI18N = m2.group(0)
src = src.replace(MENUI18N, "@@MENUI18N@@")

# ── 2c. Menu JSON-LD şeması — canlı /api/menu'den (yoksa yerel seed'ten) üretilir.
#         @@MENUSCHEMA@@ zaten source.html'de literal placeholder; tokenizer'dan
#         etkilenmemesi için içerik tokenizasyondan SONRA (WAMSG ile aynı yerde) basılır. ──
def load_menu_data():
    try:
        with urllib.request.urlopen(SITE + "/api/menu", timeout=6) as r:
            j = json.loads(r.read().decode("utf-8"))
            if j.get("data") and j["data"].get("items"):
                return j["data"]
    except Exception as e:
        print("ℹ️  Canlı /api/menu alınamadı (%s), yerel seed kullanılıyor." % e)
    return json.load(open(f"{PROJ}/data/menu-data.seed.json", encoding="utf-8"))

def build_menu_schema():
    menu = load_menu_data()
    cats_by_id = {c["id"]: c for c in menu["categories"]}
    sections = []
    for c in menu["categories"]:
        items = [it for it in menu["items"] if it["cat"] == c["id"]]
        if not items:
            continue
        menu_items = []
        for it in items:
            mi = {"@type": "MenuItem", "name": it["name"]}
            if it.get("desc"):
                mi["description"] = it["desc"]
            if it.get("price"):
                mi["offers"] = {"@type": "Offer", "price": str(it["price"]), "priceCurrency": "TRY"}
            menu_items.append(mi)
        sections.append({"@type": "MenuSection", "name": c.get("name_tr", c["id"]), "hasMenuItem": menu_items})
    schema = {
        "@context": "https://schema.org",
        "@type": "Menu",
        "name": "Mare Gastro Menü",
        "inLanguage": "tr",
        "url": SITE + "/#menu",
        "hasMenuSection": sections,
    }
    return json.dumps(schema, ensure_ascii=False, indent=1)

MENUSCHEMA = build_menu_schema()

# ── 3. hreflang + dil değiştirici işaretçileri ──
src = re.sub(r'(<link rel="canonical"[^>]*>)', r"\1\n@@HREFLANG@@", src, count=1)
src = src.replace('<div class="nav-right">', '<div class="nav-right">@@LANGSW@@', 1)

# ── 4. Tokenizasyon (uzun→kısa, &amp;/& toleranslı) ──
template = src
notfound = []
for key, s in sorted(tr.items(), key=lambda kv: -len(kv[1])):
    if key in ("js_wa_msg", "js_wa_default"):   # JS'te özel ele alınır / korunur
        continue
    token = "@@%s@@" % key
    for cand in (s, s.replace("&amp;", "&"), s.replace("&", "&amp;")):
        if cand and cand in template:
            template = template.replace(cand, token)
            break
    else:
        notfound.append((key, s))

if notfound:
    print("⚠️  Bulunamayan src (token uygulanmadı):")
    for k, s in notfound:
        print("   ", k, "=>", repr(s[:60]))

# ── 5. hreflang bloğu (tüm sayfalarda aynı) ──
hreflang = "\n".join(
    ['<link rel="alternate" hreflang="%s" href="%s/%s/">' % (l, SITE, l) for l in LANGS]
    + ['<link rel="alternate" hreflang="x-default" href="%s/">' % SITE]
)

# ── 6. Dil değiştirici (bayraklı, mini dropdown) ──
def langsw(cur):
    items = "".join(
        '<a href="/%s/" class="%s">%s %s</a>' % (l, "on" if l == cur else "", FLAG[l], LANGNAME[l])
        for l in LANGS
    )
    return (
        '<style>'
        '.langsw{position:relative;display:flex;align-items:center}'
        '.langsw-btn{display:flex;align-items:center;gap:6px;background:var(--glass);border:1px solid var(--glassBorder);'
        'color:var(--cream);font-family:var(--sf);font-size:12px;letter-spacing:.04em;padding:7px 11px;border-radius:100px;transition:background .25s var(--ease)}'
        '.langsw-btn:hover{background:var(--glassHover)}'
        '.langsw-btn .chev{width:9px;height:9px;opacity:.6;transition:transform .3s var(--ease)}'
        '.langsw.open .chev{transform:rotate(180deg)}'
        '.langsw-menu{position:absolute;top:calc(100% + 8px);right:0;min-width:150px;background:rgba(8,19,30,.92);'
        'backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border:1px solid var(--glassBorder);border-radius:14px;'
        'padding:6px;opacity:0;visibility:hidden;transform:translateY(-6px);transition:all .28s var(--ease);z-index:120;box-shadow:0 18px 50px rgba(0,0,0,.5)}'
        '.langsw.open .langsw-menu{opacity:1;visibility:visible;transform:translateY(0)}'
        '.langsw-menu a{display:flex;align-items:center;gap:9px;padding:9px 12px;border-radius:9px;color:var(--cream);'
        'text-decoration:none;font-size:13px;letter-spacing:.02em;transition:background .2s}'
        '.langsw-menu a:hover{background:var(--glass)}'
        '.langsw-menu a.on{color:var(--amber2)}'
        '[dir=rtl] .langsw-menu{right:auto;left:0}'
        '@media(max-width:880px){.langsw{display:none}}'
        '.mob-langs{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 4px;padding-top:18px;border-top:1px solid var(--glassBorder)}'
        '.mob-langs a{display:flex;align-items:center;gap:7px;font-size:14px;color:var(--muted);text-decoration:none;padding:7px 12px;border:1px solid var(--glassBorder);border-radius:100px}'
        '.mob-langs a.on{color:var(--amber2);border-color:rgba(200,169,110,.4)}'
        '</style>'
        '<div class="langsw" id="langsw">'
        '<button class="langsw-btn" onclick="document.getElementById(\'langsw\').classList.toggle(\'open\')" aria-label="Language">'
        + FLAG[cur] + ' ' + LANGNAME[cur]
        + '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>'
        '</button>'
        '<div class="langsw-menu">' + items + '</div>'
        '</div>'
        '<script>document.addEventListener("click",function(e){var s=document.getElementById("langsw");if(s&&!s.contains(e.target))s.classList.remove("open")})</script>'
    )

# ── 7. Mobil menüye de dil linkleri (switcher mobilde gizli) ──
def mob_langs(cur):
    return '<div class="mob-langs">' + "".join(
        '<a href="/%s/" class="%s">%s %s</a>' % (l, "on" if l == cur else "", FLAG[l], LANGNAME[l]) for l in LANGS
    ) + '</div>'

# ── 8. Her dil için üret ──
for l in LANGS:
    out = template
    d = strings[l]
    # token değişimi
    out = out.replace("@@HREFLANG@@", hreflang)
    out = out.replace("@@LANGSW@@", langsw(l))
    out = out.replace("@@WAMSG@@", WAMSG)
    out = out.replace("@@MENUI18N@@", MENUI18N)
    out = out.replace("@@MENUSCHEMA@@", MENUSCHEMA)
    # JS tek-tırnak bağlamına giren tokenler (alert / textContent / onclick selK)
    JS_CTX = {"js_gnote_ozel", "js_gnote_yalniz", "js_gnote_kisilik",
              "js_alert_tarih", "js_alert_saat", "js_alert_konaklama",
              "js_kisi_suffix", "rez_kopt1_v", "rez_kopt2_v"}
    for key, val in d.items():
        safe = val.replace("\\", "\\\\").replace("'", "\\'") if key in JS_CTX else val
        out = out.replace("@@%s@@" % key, safe)
    # kalan tokenler? (eksik çeviri tespiti)
    leftover = re.findall(r"@@[\w]+@@", out)
    if leftover:
        print("⚠️  [%s] yerine konmayan token:" % l, set(leftover))

    # <html lang / dir>
    if l in RTL:
        out = out.replace('<html lang="tr">', '<html lang="%s" dir="rtl">' % l, 1)
    else:
        out = out.replace('<html lang="tr">', '<html lang="%s">' % l, 1)
    # canonical + og:url + og:locale + JS locale
    out = out.replace('href="%s/"' % SITE, 'href="%s/%s/"' % (SITE, l))            # canonical
    out = out.replace('content="%s/"' % SITE, 'content="%s/%s/"' % (SITE, l))      # og:url
    out = out.replace('content="tr_TR"', 'content="%s"' % LOCALE[l])
    out = out.replace("'tr-TR'", "'%s'" % JSLOCALE[l])
    # NOT: Menu şemasının "inLanguage" alanı kasıtlı olarak "tr" kalır —
    # yemek içerikleri (isim/açıklama) tüm site dillerinde SADECE Türkçe.
    # mobil dil linkleri (mobil menü açılışına ekle)
    out = re.sub(r'(<div class="mob-menu"[^>]*>)', lambda m: m.group(1) + mob_langs(l), out, count=1)

    os.makedirs(f"{PROJ}/{l}", exist_ok=True)
    open(f"{PROJ}/{l}/index.html", "w", encoding="utf-8").write(out)
    # JS doğrulama (inline script'ler, ld+json ve src hariç) — node varsa
    import subprocess
    bad = 0
    for sc in re.findall(r'<script(?![^>]*\bsrc=)(?![^>]*ld\+json)[^>]*>(.*?)</script>', out, re.S):
        if not sc.strip():
            continue
        open("/tmp/_chk.js", "w").write(sc)
        try:
            if subprocess.run(["node", "--check", "/tmp/_chk.js"], capture_output=True).returncode != 0:
                bad += 1
        except FileNotFoundError:
            bad = -1
            break
    flag = "  ⚠️ JS HATASI!" if bad > 0 else ("" if bad == 0 else "  (node yok, JS doğrulanmadı)")
    print("✓ /%s/index.html  (%d bytes)%s" % (l, len(out), flag))

# ── 9. Kök açılış (dil-seçim) ekranı ── (minimalist + animasyonlu)
PROMPT = {"tr": "Dilinizi seçin", "en": "Select your language", "ar": "اختر لغتك", "ru": "Выберите язык"}

cards = "".join(
    '<a href="/{l}/" class="lc" style="--i:{i}" lang="{l}"{rtl} aria-label="{name}">'
    '<span class="lc-flag">{flag}</span>'
    '<span class="lc-name">{name}</span>'
    '</a>'.format(l=l, i=i, flag=FLAG[l], name=LANGNAME[l], rtl=' dir="rtl"' if l in RTL else "")
    for i, l in enumerate(LANGS)
)

GA = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-LMZ66PTR0T"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-LMZ66PTR0T');
</script>"""

splash = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
__GA__
<title>Mare Gastro | Sapanca Göl Manzaralı Fine Dining Restoran</title>
<meta name="description" content="Sapanca göl manzaralı lüks fine dining restoran. Mare Gastro, Didi Otel bahçesinde. Dilinizi seçin, Select your language.">
<meta name="theme-color" content="#04080F">
<link rel="canonical" href="__SITE__/">
<link rel="icon" type="image/svg+xml" href="/images/mare.svg">
<link rel="icon" type="image/png" href="/images/marelogo.png">
<link rel="apple-touch-icon" href="/images/marelogo.png">
__HREFLANG__
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#04080F;--amber:#C8A96E;--amber2:#DFC08A;--cream:#EDE8DC;--muted:rgba(237,232,220,.45);
--glass:rgba(255,255,255,.045);--glassBorder:rgba(255,255,255,.08);--ease:cubic-bezier(.19,1,.22,1);
--sf:-apple-system,BlinkMacSystemFont,'SF Pro Display','Helvetica Neue',sans-serif;--ital:'Cormorant Garamond',serif}
html,body{height:100%;overflow:hidden;max-width:100%}
body{background:var(--bg);color:var(--cream);font-family:var(--sf);overflow:hidden;
display:flex;align-items:center;justify-content:center;min-height:100svh;position:relative}
/* tek yumuşak nefes alan glow */
.aura{position:fixed;width:90vmax;height:90vmax;left:50%;top:50%;border-radius:50%;pointer-events:none;z-index:0;
background:radial-gradient(circle,rgba(200,169,110,.12),rgba(40,80,110,.06) 38%,transparent 66%);
transform:translate(-50%,-50%);animation:breathe 11s ease-in-out infinite}
@keyframes breathe{0%,100%{transform:translate(-50%,-50%) scale(1);opacity:.85}50%{transform:translate(-50%,-50%) scale(1.16);opacity:1}}
.par{position:fixed;bottom:-8px;width:2px;height:2px;background:rgba(200,169,110,.45);border-radius:50%;z-index:1;animation:rise linear infinite}
@keyframes rise{0%{transform:translateY(0);opacity:0}12%{opacity:.6}100%{transform:translateY(-104vh);opacity:0}}
.wrap{position:relative;z-index:3;width:100%;max-width:600px;min-width:0;padding:30px 22px;text-align:center}
.logo{width:172px;max-width:56%;margin:0 auto 22px;display:block;
animation:logoIn 1.3s var(--ease) both}
@keyframes logoIn{from{opacity:0;transform:translateY(12px) scale(.94);filter:blur(8px)}to{opacity:1;transform:none;filter:blur(0)}}
.divider{width:0;height:1px;margin:0 auto 20px;background:linear-gradient(90deg,transparent,var(--amber),transparent);
animation:draw 1.4s var(--ease) .5s forwards}
@keyframes draw{to{width:150px}}
.prompt{font-family:var(--ital);font-style:italic;font-size:clamp(19px,3.2vw,25px);color:var(--cream);
margin-bottom:34px;min-height:1.3em;letter-spacing:.01em;transition:opacity .5s var(--ease);
animation:fadeUp 1.1s var(--ease) .7s both}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;width:100%;min-width:0}
@media(max-width:560px){.cards{grid-template-columns:repeat(2,minmax(0,1fr));gap:11px}.wrap{padding:26px 16px}.lc{padding:20px 8px 16px}}
.lc{position:relative;min-width:0;display:flex;flex-direction:column;align-items:center;gap:11px;
text-decoration:none;color:var(--cream);background:var(--glass);border:1px solid var(--glassBorder);
border-radius:18px;padding:24px 10px 18px;overflow:hidden;
backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);
transition:transform .5s var(--ease),border-color .5s var(--ease),background .5s var(--ease),box-shadow .5s var(--ease);
animation:cardIn .9s var(--ease) calc(.85s + var(--i)*.12s) both}
@keyframes cardIn{from{opacity:0;transform:translateY(22px) scale(.96);filter:blur(6px)}to{opacity:1;transform:none;filter:blur(0)}}
.lc::after{content:"";position:absolute;top:0;left:-120%;width:60%;height:100%;
background:linear-gradient(100deg,transparent,rgba(255,255,255,.12),transparent);transform:skewX(-18deg);transition:left .8s var(--ease)}
.lc:hover{transform:translateY(-6px);border-color:rgba(200,169,110,.5);background:rgba(255,255,255,.07);
box-shadow:0 20px 44px rgba(0,0,0,.4),0 0 0 1px rgba(200,169,110,.12)}
.lc:hover::after{left:130%}
.lc-flag{font-size:38px;line-height:1;filter:drop-shadow(0 4px 8px rgba(0,0,0,.35));
transition:transform .5s var(--ease)}
.lc:hover .lc-flag{transform:scale(1.16) translateY(-2px)}
.lc-name{font-size:15px;font-weight:500;letter-spacing:.02em;position:relative;padding-bottom:4px}
.lc-name::after{content:"";position:absolute;left:50%;bottom:0;width:0;height:1px;background:var(--amber2);transition:width .5s var(--ease),left .5s var(--ease)}
.lc:hover .lc-name::after{width:100%;left:0}
.lc:hover .lc-name{color:var(--amber2)}
.foot{margin-top:36px;font-size:10.5px;letter-spacing:.22em;color:var(--muted);text-transform:uppercase;
animation:fadeUp 1.1s var(--ease) 1.5s both}
.foot a{color:var(--amber);text-decoration:none;opacity:.85}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.divider{width:150px}}
</style>
</head>
<body>
<div class="aura"></div>
<div class="wrap">
<img class="logo" src="/images/marelogo1.png" alt="Mare Gastro" onerror="this.onerror=null;this.src='/images/marelogo.png'">
<div class="divider"></div>
<div class="prompt" id="prompt">__PROMPT0__</div>
<div class="cards">
__CARDS__
</div>
<div class="foot">Sapanca · Didi Otel · <a href="https://www.instagram.com/maregastrosapanca/" target="_blank" rel="noopener">Instagram</a></div>
</div>
<script>
(function(){var n=window.innerWidth<600?9:16,b=document.body;for(var i=0;i<n;i++){var p=document.createElement('div');p.className='par';var s=1+Math.random()*2;p.style.left=Math.random()*100+'vw';p.style.width=p.style.height=s+'px';p.style.animationDuration=(15+Math.random()*15)+'s';p.style.animationDelay=(-Math.random()*22)+'s';p.style.opacity=.25+Math.random()*.45;b.appendChild(p)}})();
(function(){var P=__PROMPTS__,i=0,el=document.getElementById('prompt');setInterval(function(){i=(i+1)%P.length;el.style.opacity=0;setTimeout(function(){el.textContent=P[i];el.style.opacity=1},480)},2800)})();
</script>
</body>
</html>"""

import json as _json
splash = (splash
          .replace("__GA__", GA)
          .replace("__SITE__", SITE)
          .replace("__HREFLANG__", hreflang)
          .replace("__CARDS__", cards)
          .replace("__PROMPT0__", PROMPT["tr"])
          .replace("__PROMPTS__", _json.dumps([PROMPT[l] for l in LANGS], ensure_ascii=False)))
open(f"{PROJ}/index.html", "w", encoding="utf-8").write(splash)
print("✓ /index.html  (açılış / dil-seçim, %d bytes)" % len(splash))

print("\nTamam. Diller:", ", ".join(LANGS))
