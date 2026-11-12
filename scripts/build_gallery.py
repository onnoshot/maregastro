#!/usr/bin/env python3
"""Mare Gastro photo gallery — TR /fotograflar.html, EN/AR/RU /{lang}/photos.html.

Only real photographs of the venue, bar, dishes and chef (no AI-generated scenes).
Instagram photos (images/ig-*.webp) come from @maregastro via Composio (alias maregastro);
source post per file: data/instagram-gallery-sources.json. Photos with text overlays are skipped.
Dishes come from the live menu (/api/menu: items that have a photo), names in Turkish
as on the printed menu. Creates /images/g/<name>-800.webp (grid) and -1600.webp (lightbox).

Idempotent. Usage: python3 -I scripts/build_gallery.py
"""
import html, json, os, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "images")
OUT = os.path.join(IMG, "g")
SITE = "https://maregastro.com"
PATHS = {"tr": "/fotograflar.html", "en": "/en/photos.html", "ar": "/ar/photos.html", "ru": "/ru/photos.html"}
HOME = {"tr": "/tr/", "en": "/en/", "ar": "/ar/", "ru": "/ru/"}
FAQ = {"tr": "/sss.html", "en": "/en/faq.html", "ar": "/ar/faq.html", "ru": "/ru/faq.html"}

# venue photos (real), alt text per language
VENUE = [
 ("hero-mare-1", {"tr": "Mare Gastro girişi, gece aydınlatmasıyla", "en": "Mare Gastro entrance lit at night", "ar": "مدخل Mare Gastro مضاءً ليلاً", "ru": "Вход в Mare Gastro вечером"}),
 ("mare-ambiance", {"tr": "Akşam Mare Gastro'nun ışıkları", "en": "Mare Gastro lights in the evening", "ar": "أضواء Mare Gastro في المساء", "ru": "Огни Mare Gastro вечером"}),
 ("mare-aerial", {"tr": "Havadan Mare Gastro ve Didi Otel bahçesi", "en": "Aerial view of Mare Gastro and the Didi Otel garden", "ar": "منظر جوي لـ Mare Gastro وحديقة Didi Otel", "ru": "Mare Gastro и сад Didi Otel с высоты"}),
 ("mare-gece-terasi", {"tr": "Gece terası ve kurulu masalar", "en": "The night terrace with set tables", "ar": "التراس الليلي والطاولات المعدّة", "ru": "Ночная терраса с накрытыми столами"}),
 ("header", {"tr": "Bahçede Mare Gastro tabelası ve yeşillikler", "en": "The Mare Gastro sign among the garden greenery", "ar": "لافتة Mare Gastro بين خضرة الحديقة", "ru": "Вывеска Mare Gastro в зелени сада"}),
 ("mare-bahce-havuz-yolu", {"tr": "Havuza giden bahçe yolu", "en": "Garden path to the pool", "ar": "ممر الحديقة المؤدي إلى المسبح", "ru": "Садовая дорожка к бассейну"}),
 ("mare-bahce-manzarasi", {"tr": "Gündüz bahçe ve kabanalar", "en": "The garden and cabanas by day", "ar": "الحديقة والأكواخ نهاراً", "ru": "Сад и кабаны днём"}),
 ("mare-havuz-sezlong", {"tr": "Havuz kenarı şezlonglar", "en": "Poolside loungers", "ar": "كراسي الاستلقاء بجانب المسبح", "ru": "Шезлонги у бассейна"}),
 ("mare-kabana-oturma", {"tr": "Perdeli kabana oturma alanı", "en": "Curtained cabana seating", "ar": "جلسة الكابانا بالستائر", "ru": "Кабаны с занавесями"}),
 ("mare-kutlama-kadeh", {"tr": "Terasta kadeh kaldıran misafirler", "en": "Guests raising a glass on the terrace", "ar": "ضيوف يرفعون الكؤوس على التراس", "ru": "Гости поднимают бокалы на террасе"}),
 ("mare-romantik-kadeh", {"tr": "İki kişilik akşam yemeğinde kadehler", "en": "A toast at dinner for two", "ar": "نخب في عشاء لشخصين", "ru": "Тост за ужином на двоих"}),
 ("mare-grup-sofra", {"tr": "Paylaşımlık mezelerle kalabalık sofra", "en": "A shared table of meze", "ar": "مائدة مشتركة من المقبلات", "ru": "Общий стол с мезе"}),
 ("mare-sofra-detay", {"tr": "Sofradan mezeler", "en": "Meze on the table", "ar": "مقبلات على المائدة", "ru": "Мезе на столе"}),
 ("ig-gunduz-tente", {"tr": "Gündüz Mare Gastro tentesi", "en": "The Mare Gastro awning by day", "ar": "مظلة Mare Gastro نهاراً", "ru": "Навес Mare Gastro днём"}),
 ("ig-gece-zeytin-agaclari", {"tr": "Zeytin ağaçları arasında gece Mare Gastro", "en": "Mare Gastro at night among the olive trees", "ar": "Mare Gastro ليلاً بين أشجار الزيتون", "ru": "Mare Gastro ночью среди оливковых деревьев"}),
]
BAR = [
 ("ig-bar-kokteyl-hazirlik", {"tr": "Barda imza kokteyl hazırlığı", "en": "Preparing a signature cocktail at the bar", "ar": "تحضير كوكتيل مميز في البار", "ru": "Фирменный коктейль готовится у бара"}),
 ("ig-kokteyl-serefe", {"tr": "İmza kokteyllerle şerefe", "en": "Cheers with signature cocktails", "ar": "نخب بالكوكتيلات المميزة", "ru": "Тост с фирменными коктейлями"}),
 ("ig-gece-kadeh", {"tr": "Gece kadehler kalkıyor", "en": "Glasses raised at night", "ar": "رفع الكؤوس ليلاً", "ru": "Бокалы поднимаются вечером"}),
 ("ig-imza-kokteyl", {"tr": "İmza kokteyl", "en": "Signature cocktail", "ar": "كوكتيل مميز", "ru": "Фирменный коктейль"}),
 ("ig-bar-kokteyl", {"tr": "Barda bir kokteyl", "en": "A cocktail at the bar", "ar": "كوكتيل في البار", "ru": "Коктейль у бара"}),
 ("ig-aksam-bar", {"tr": "Akşam barda", "en": "Evening at the bar", "ar": "مساء في البار", "ru": "Вечер у бара"}),
]
IG_DISHES = [
 ("ig-koy-salatasi", {"tr": "Köy salatası: domates, biber, salatalık, beyaz peynir, zeytin", "en": "Village salad: tomato, pepper, cucumber, white cheese, olives", "ar": "سلطة القرية: طماطم، فلفل، خيار، جبن أبيض، زيتون", "ru": "Деревенский салат: томаты, перец, огурец, белый сыр, оливки"}),
 ("ig-zeytinyaglilar", {"tr": "Zeytinyağlılar ve mezeler", "en": "Olive-oil dishes and meze", "ar": "أطباق بزيت الزيتون ومقبلات", "ru": "Блюда на оливковом масле и мезе"}),
 ("ig-akdeniz-mezeleri", {"tr": "Akdeniz mezeleri: taze fasulye, pancar carpaccio, közlenmiş patlıcan, enginar", "en": "Mediterranean meze: green beans, beetroot carpaccio, roasted aubergine, artichoke", "ar": "مقبلات متوسطية: فاصوليا خضراء، كارباتشيو الشمندر، باذنجان مشوي، خرشوف", "ru": "Средиземноморские мезе: стручковая фасоль, карпаччо из свёклы, печёный баклажан, артишок"}),
 ("ig-citir-kalamar", {"tr": "Çıtır kalamar", "en": "Crispy calamari", "ar": "كاليماري مقرمش", "ru": "Хрустящие кальмары"}),
 ("ig-balik-tabagi", {"tr": "Mare Gastro mutfağından bir balık tabağı", "en": "A fish plate from the Mare Gastro kitchen", "ar": "طبق سمك من مطبخ Mare Gastro", "ru": "Рыбное блюдо с кухни Mare Gastro"}),
 ("ig-tabak-1", {"tr": "Mare Gastro mutfağından bir tabak", "en": "A plate from the Mare Gastro kitchen", "ar": "طبق من مطبخ Mare Gastro", "ru": "Блюдо с кухни Mare Gastro"}),
 ("ig-yanik-cheesecake", {"tr": "Yanık yüzlü cheesecake", "en": "Burnt Basque cheesecake", "ar": "تشيز كيك محروق الوجه", "ru": "Баскский чизкейк"}),
]
CHEF = [("dogansef", {"tr": "Yönetici Şef Doğan Anapa", "en": "Executive Chef Doğan Anapa", "ar": "الشيف التنفيذي دوغان أنابا", "ru": "Шеф-повар Доган Анапа"})]

T = {
 "tr": dict(title="Mare Gastro Fotoğrafları | Sapanca Bahçe, Teras ve Tabaklar",
  desc="Mare Gastro'dan gerçek fotoğraflar: Sapanca'da Didi Otel bahçesi, gece terası, havuz ve kabanalar, Şef Doğan Anapa ve menüdeki tabaklar.",
  h1="Mare Gastro <em>Fotoğrafları</em>", lead="Bahçeden, terastan ve mutfaktan gerçek kareler. Büyütmek için bir fotoğrafa dokunun.",
  venue="Mekân", bar="Bar ve Kokteyller", dishes="Tabaklar", chef="Şef", rez="Rezervasyon Yap", ig="Instagram'da daha fazlası", back="Ana sayfa", crumb="Fotoğraflar", close="Kapat", prev="Önceki", next="Sonraki"),
 "en": dict(title="Mare Gastro Photos | Garden, Terrace and Dishes in Sapanca",
  desc="Real photos of Mare Gastro: the Didi Otel garden in Sapanca, the night terrace, pool and cabanas, Chef Doğan Anapa and dishes from the menu.",
  h1="Mare Gastro <em>Photos</em>", lead="Real moments from the garden, the terrace and the kitchen. Tap a photo to enlarge it.",
  venue="The Place", bar="Bar & Cocktails", dishes="Dishes", chef="Chef", rez="Book a Table", ig="More on Instagram", back="Home", crumb="Photos", close="Close", prev="Previous", next="Next"),
 "ar": dict(title="صور Mare Gastro | الحديقة والتراس والأطباق في سابانجا",
  desc="صور حقيقية من Mare Gastro: حديقة Didi Otel في سابانجا، التراس الليلي، المسبح والأكواخ، الشيف دوغان أنابا وأطباق من القائمة.",
  h1="صور <em>Mare Gastro</em>", lead="لقطات حقيقية من الحديقة والتراس والمطبخ. اضغط على الصورة لتكبيرها.",
  venue="المكان", bar="البار والكوكتيلات", dishes="الأطباق", chef="الشيف", rez="احجز طاولة", ig="المزيد على إنستغرام", back="الرئيسية", crumb="الصور", close="إغلاق", prev="السابق", next="التالي"),
 "ru": dict(title="Фото Mare Gastro | Сад, терраса и блюда в Сапандже",
  desc="Настоящие фото Mare Gastro: сад отеля Didi Otel в Сапандже, ночная терраса, бассейн и кабаны, шеф Доган Анапа и блюда из меню.",
  h1="Фото <em>Mare Gastro</em>", lead="Настоящие кадры из сада, с террасы и с кухни. Нажмите на фото, чтобы увеличить.",
  venue="Место", bar="Бар и коктейли", dishes="Блюда", chef="Шеф", rez="Забронировать", ig="Больше в Instagram", back="Главная", crumb="Фото", close="Закрыть", prev="Назад", next="Далее"),
}


def src_for(name):
    for ext in ("webp", "jpg", "jpeg", "png"):
        p = os.path.join(IMG, "%s.%s" % (name, ext))
        if os.path.exists(p):
            return p
    return None


def variants(name):
    src = src_for(name)
    if not src:
        return None
    out = {}
    for w in (800, 1600):
        dst = os.path.join(OUT, "%s-%d.webp" % (name, w))
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            im = Image.open(src).convert("RGB")
            if im.width > w:
                im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            im.save(dst, "WEBP", quality=80 if w == 800 else 82, method=6)
        with Image.open(dst) as im:
            out[w] = ("/images/g/%s-%d.webp" % (name, w), im.width, im.height)
    return out


def menu_dishes():
    try:
        d = json.load(urllib.request.urlopen(SITE + "/api/menu", timeout=20))["data"]
    except Exception:
        d = json.load(open(os.path.join(ROOT, "data", "menu-data.seed.json"), encoding="utf-8"))
        d = d.get("data", d)
    food = [c["id"] for c in d["categories"] if c["group"] == "yemek"]
    seen, out = set(), []
    for cid in food:
        for it in d["items"]:
            if it["cat"] == cid and it.get("img"):
                name = it["img"].rsplit(".", 1)[0]
                if name not in seen:
                    seen.add(name)
                    out.append((name, it["name"]))
    return out


def tile(name, alt, v, cls):
    s8, s16 = v[800], v[1600]
    return ('<a class="g-item %s" href="%s" data-w="%d" data-h="%d"><img src="%s" width="%d" height="%d" '
            'loading="lazy" decoding="async" alt="%s"><span class="g-cap">%s</span></a>') % (
        cls, s16[0], s16[1], s16[2], s8[0], s8[1], s8[2], html.escape(alt), html.escape(alt))


CSS = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#FBF8F2;--sand:#F3EDE2;--ink:#10202E;--ink2:#2A3A48;--muted:rgba(16,32,46,.74);--amber:#9C7437;--amber-ink:#7A5A27;--line:rgba(16,32,46,.1);
--sf:-apple-system,BlinkMacSystemFont,'SF Pro Display','SF Pro Text','Helvetica Neue',Inter,Arial,sans-serif}
html{background:var(--bg)}body{font-family:var(--sf);color:var(--ink);background:var(--bg);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--amber-ink)}
.top{position:sticky;top:0;z-index:5;background:rgba(251,248,242,.88);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-bottom:1px solid var(--line)}
.top-in{max-width:1180px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.top img{height:28px;width:auto;filter:brightness(0);opacity:.86;display:block}
.btn{display:inline-flex;align-items:center;justify-content:center;height:44px;padding:0 20px;border-radius:999px;font-size:14px;font-weight:600;text-decoration:none;white-space:nowrap}
.btn-p{background:var(--ink);color:#fff}.btn-s{background:#fff;color:var(--ink);border:1px solid rgba(16,32,46,.18)}
main{max-width:1180px;margin:0 auto;padding:36px 20px 80px}
.crumb{font-size:12.5px;color:var(--muted);margin-bottom:16px}.crumb a{color:var(--muted)}
h1{font-size:clamp(2rem,5vw,3rem);font-weight:600;letter-spacing:-.03em;line-height:1.06;margin-bottom:10px}
h1 em{font-style:normal;color:var(--amber)}
.lead{font-size:16.5px;color:var(--ink2);margin-bottom:28px;max-width:640px}
h2{font-size:12px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--amber-ink);margin:34px 0 14px}
.grid{columns:2;column-gap:10px}
@media(min-width:900px){.grid{columns:3 280px;column-gap:16px}}
.g-item{display:block;break-inside:avoid;margin:0 0 10px;border-radius:16px;overflow:hidden;position:relative;background:#EDE6DA;box-shadow:0 1px 2px rgba(16,32,46,.04),0 10px 26px -16px rgba(16,32,46,.3)}
@media(min-width:900px){.g-item{margin-bottom:16px}}
.g-item img{display:block;width:100%;height:auto;transition:transform .8s cubic-bezier(.22,1,.36,1)}
.g-item:hover img{transform:scale(1.04)}
.g-cap{position:absolute;left:0;right:0;bottom:0;padding:22px 12px 10px;font-size:12.5px;font-weight:500;color:#fff;background:linear-gradient(to top,rgba(8,16,24,.72),transparent);opacity:0;transition:opacity .3s}
.g-item:hover .g-cap,.g-item:focus-visible .g-cap{opacity:1}
.g-dish .g-cap{opacity:1;font-weight:600}
.cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px}
.lb{position:fixed;inset:0;z-index:50;background:rgba(10,18,26,.94);display:none;align-items:center;justify-content:center;padding:56px 12px}
.lb.open{display:flex}
.lb img{max-width:100%;max-height:100%;border-radius:12px;object-fit:contain}
.lb p{position:absolute;left:0;right:0;bottom:14px;text-align:center;color:#F3EDE2;font-size:14px;padding:0 60px}
.lb button{position:absolute;width:48px;height:48px;border-radius:50%;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.08);color:#fff;font-size:22px;cursor:pointer}
.lb .x{top:12px;right:12px}.lb .pv{left:12px;top:50%;transform:translateY(-50%)}.lb .nx{right:12px;top:50%;transform:translateY(-50%)}
[dir=rtl] .lb .pv{left:auto;right:12px}[dir=rtl] .lb .nx{right:auto;left:12px}
footer{border-top:1px solid var(--line);background:var(--sand);padding:28px 20px;text-align:center;font-size:12.5px;color:var(--muted)}
footer a{color:var(--ink2);margin:0 8px;text-decoration:none;font-weight:600}
@media(max-width:560px){.top-in .btn-s{display:none}}"""

JS = """(function(){var lb=document.getElementById('lb'),im=lb.querySelector('img'),cap=lb.querySelector('p'),items=[].slice.call(document.querySelectorAll('.g-item')),i=0;
function show(n){i=(n+items.length)%items.length;var a=items[i];im.src=a.getAttribute('href');im.alt=a.querySelector('img').alt;cap.textContent=im.alt;}
function open(n){show(n);lb.classList.add('open');document.body.style.overflow='hidden';if(typeof trackEvent==='function')trackEvent('gallery_open',{event_label:im.alt});}
function close(){lb.classList.remove('open');document.body.style.overflow='';}
items.forEach(function(a,n){a.addEventListener('click',function(e){e.preventDefault();open(n);});});
lb.querySelector('.x').onclick=close;lb.querySelector('.pv').onclick=function(){show(i-1)};lb.querySelector('.nx').onclick=function(){show(i+1)};
lb.addEventListener('click',function(e){if(e.target===lb)close();});
document.addEventListener('keydown',function(e){if(!lb.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1);});})();"""

GTM_HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TVJ7R3TT');</script>
<!-- End Google Tag Manager -->
<script>var MARE_GTM_EVENTS=['phone_click','menu_click','whatsapp_click','availability_check'];function gtag(){window.dataLayer.push(arguments);}
function trackEvent(n,p){try{window.dataLayer=window.dataLayer||[];p=Object.assign({page_lang:document.documentElement.lang||''},p||{});window.dataLayer.push(Object.assign({event:n},p));if(MARE_GTM_EVENTS.indexOf(n)<0)gtag('event',n,Object.assign({send_to:'G-LMZ66PTR0T'},p));}catch(e){}}</script>"""


def page(lang, venue, dishes, chef, bar):
    t = T[lang]
    url = SITE + PATHS[lang]
    rtl = ' dir="rtl"' if lang == "ar" else ""
    alts = "".join('<link rel="alternate" hreflang="%s" href="%s%s">\n' % (l, SITE, p) for l, p in PATHS.items())
    alts += '<link rel="alternate" hreflang="x-default" href="%s%s">\n' % (SITE, PATHS["tr"])
    imgs = [(v[1600][0], alt) for _, alt, v in venue + bar + chef + dishes]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ImageGallery", "@id": url + "#gallery", "url": url, "name": html.unescape(t["title"]), "inLanguage": lang,
         "about": {"@type": "Restaurant", "name": "Mare Gastro", "url": SITE + HOME[lang]},
         "image": [{"@type": "ImageObject", "contentUrl": SITE + u, "caption": c, "creditText": "Mare Gastro",
                    "copyrightNotice": "© Mare Gastro"} for u, c in imgs]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Mare Gastro", "item": SITE + HOME[lang]},
            {"@type": "ListItem", "position": 2, "name": t["crumb"], "item": url}]}]}
    g = lambda rows, cls: "".join(tile(n, a, v, cls) for n, a, v in rows)
    return f"""<!DOCTYPE html>
<html lang="{lang}"{rtl}>
<head>
{GTM_HEAD}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="robots" content="index, follow, max-image-preview:large">
<title>{html.escape(t['title'])}</title>
<meta name="description" content="{html.escape(t['desc'])}">
<meta name="theme-color" content="#FBF8F2">
<link rel="canonical" href="{url}">
{alts}<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mare Gastro">
<meta property="og:title" content="{html.escape(t['title'])}">
<meta property="og:description" content="{html.escape(t['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/g/mare-aerial-1600.webp">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TVJ7R3TT" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<header class="top"><div class="top-in"><a href="{HOME[lang]}" aria-label="Mare Gastro"><img src="/images/marelogo-w560.png" alt="Mare Gastro"></a>
<div style="display:flex;gap:8px"><a class="btn btn-s" href="https://www.instagram.com/maregastro/" target="_blank" rel="noopener" onclick="trackEvent('instagram_click',{{event_label:'gallery_header'}})">Instagram</a><a class="btn btn-p" href="{HOME[lang]}#reservation">{t['rez']}</a></div></div></header>
<main>
<nav class="crumb"><a href="{HOME[lang]}">{t['back']}</a> · {t['crumb']}</nav>
<h1>{t['h1']}</h1>
<p class="lead">{t['lead']}</p>
<h2>{t['venue']}</h2>
<div class="grid">{g(venue, 'g-venue')}</div>
<h2>{t['bar']}</h2>
<div class="grid">{g(bar, 'g-bar')}</div>
<h2>{t['chef']}</h2>
<div class="grid">{g(chef, 'g-chef')}</div>
<h2>{t['dishes']}</h2>
<div class="grid">{g(dishes, 'g-dish')}</div>
<div class="cta"><a class="btn btn-p" href="{HOME[lang]}#reservation">{t['rez']}</a><a class="btn btn-s" href="https://www.instagram.com/maregastro/" target="_blank" rel="noopener" onclick="trackEvent('instagram_click',{{event_label:'gallery_footer'}})">{t['ig']}</a></div>
</main>
<div class="lb" id="lb" role="dialog" aria-modal="true"><button type="button" class="x" aria-label="{t['close']}">×</button><button type="button" class="pv" aria-label="{t['prev']}">‹</button><img alt=""><button type="button" class="nx" aria-label="{t['next']}">›</button><p></p></div>
<footer>© 2026 Mare Gastro · Didi Otel · Sapanca<br><a href="{HOME[lang]}#menu">Menu</a><a href="{FAQ[lang]}">FAQ</a><a href="https://www.instagram.com/maregastro/" target="_blank" rel="noopener">Instagram</a></footer>
<script>{JS}</script>
</body>
</html>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    dishes_raw = menu_dishes()
    for lang in PATHS:
        venue = [(n, a[lang], variants(n)) for n, a in VENUE if variants(n)]
        chef = [(n, a[lang], variants(n)) for n, a in CHEF if variants(n)]
        bar = [(n, a[lang], variants(n)) for n, a in BAR if variants(n)]
        dishes = [(n, a[lang], variants(n)) for n, a in IG_DISHES if variants(n)] + [(n, label, variants(n)) for n, label in dishes_raw if variants(n)]
        out = os.path.join(ROOT, PATHS[lang].lstrip("/"))
        open(out, "w", encoding="utf-8").write(page(lang, venue, dishes, chef, bar))
        print("wrote", PATHS[lang], "venue", len(venue), "bar", len(bar), "chef", len(chef), "dishes", len(dishes))


if __name__ == "__main__":
    main()
