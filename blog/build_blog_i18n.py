# -*- coding: utf-8 -*-
"""Mare Gastro blog - EN/AR/RU translated posts (curated high-value subset).
Fully separate from build_blog.py — zero risk to the 53 Turkish posts.
Outputs to /en/blog/, /ar/blog/, /ru/blog/ (absolute asset paths throughout).
"""
import json, os, re, html

SITE = "https://maregastro.com"
IG, IGCHEF = "https://www.instagram.com/maregastro/", "https://www.instagram.com/chefdogananapa/"
DIDI, DIDIWEB = "https://www.instagram.com/didiotel/", "https://sapancadidiotel.com/"
TT, YT = "https://www.tiktok.com/@maregastro", "https://www.youtube.com/@maregastro"
WA, MAIL = "https://wa.me/905323540888", "mailto:info@maregastro.com"
MAPS = "https://maps.google.com/?cid=7177941338358519695"
OUT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # mare-gastro-web/

GTM_HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TVJ7R3TT');</script>
<!-- End Google Tag Manager -->
<script>
function trackEvent(name,params){try{window.dataLayer=window.dataLayer||[];window.dataLayer.push(Object.assign({event:name},params||{}));}catch(e){}}
</script>"""
GTM_BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TVJ7R3TT"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

IC_IG='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>'
IC_WA='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.46-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.21-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.62.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.27-.2-.57-.35M12.05 21.78h-.01a9.87 9.87 0 01-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 01-1.51-5.26C2.16 6.89 6.6 2.46 12.05 2.46c2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 012.89 6.99c0 5.45-4.43 9.43-9.88 9.43M20.46 3.49A11.82 11.82 0 0012.05.06C5.5.06.16 5.4.16 11.95c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 005.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.16-3.48-8.42"/></svg>'
IC_MAIL='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'
IC_TT='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M16.6 5.82A4.28 4.28 0 0115.54 3h-3.09v12.4a2.59 2.59 0 01-2.59 2.5c-1.42 0-2.6-1.16-2.6-2.6 0-1.72 1.66-3.01 3.37-2.48V9.66c-3.45-.46-6.47 2.22-6.47 5.64 0 3.33 2.76 5.7 5.69 5.7 3.14 0 5.69-2.55 5.69-5.7V9.01a7.35 7.35 0 004.3 1.38V7.3s-1.88.09-3.24-1.48z"/></svg>'
IC_YT='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2a3.02 3.02 0 00-2.12-2.14C19.51 3.5 12 3.5 12 3.5s-7.51 0-9.38.56A3.02 3.02 0 00.5 6.2 31.6 31.6 0 000 12a31.6 31.6 0 00.5 5.8 3.02 3.02 0 002.12 2.14C4.49 20.5 12 20.5 12 20.5s7.51 0 9.38-.56a3.02 3.02 0 002.12-2.14A31.6 31.6 0 0024 12a31.6 31.6 0 00-.5-5.8zM9.75 15.5v-7l6 3.5-6 3.5z"/></svg>'

CATS = {
 "luks":{"en":"Luxury Restaurant","ar":"مطعم فاخر","ru":"Роскошный ресторан"},
 "deniz":{"en":"Seafood","ar":"مأكولات بحرية","ru":"Морепродукты"},
 "finedining":{"en":"Fine Dining","ar":"فاين داينينغ","ru":"Высокая кухня"},
 "rehber":{"en":"Sapanca Guide","ar":"دليل سابانجا","ru":"Гид по Сапанджа"},
 "kacamak":{"en":"Weekend Trip","ar":"رحلة نهاية الأسبوع","ru":"Отдых на выходных"},
 "kurumsal":{"en":"Corporate Events","ar":"الفعاليات المؤسسية","ru":"Корпоративные мероприятия"},
 "dogumgunu":{"en":"Birthday","ar":"عيد ميلاد","ru":"День рождения"},
 "kutlama":{"en":"Celebration","ar":"احتفال","ru":"Празднование"},
 "romantik":{"en":"Special Moments","ar":"لحظات خاصة","ru":"Особые моменты"},
}

NAV_LABELS = {
 "en": {"blog":"Blog","menu":"Menu","rez":"Reservation","home":"Home","read_more":"Read Article →",
        "you_may_like":"You Might Also Like","faq_title":"Frequently Asked Questions","faq_sub":"Mare Gastro · Sapanca",
        "cta_h":"Reserve", "cta_h_em":"your table", "cta_p":"Reserve your table for an unforgettable evening by Lake Sapanca, in the garden of Didi Otel.",
        "cta_res":"Make a Reservation","cta_wa":"WhatsApp","cta_menu":"View Menu",
        "footer_tag":"Fine Dining · Sapanca · Didi Otel Garden","footer_home":"Home","footer_within":"part of",
        "breadcrumb_home":"Home"},
 "ar": {"blog":"المدونة","menu":"القائمة","rez":"الحجز","home":"الرئيسية","read_more":"اقرأ المقال ←",
        "you_may_like":"قد يعجبك أيضًا","faq_title":"الأسئلة الشائعة","faq_sub":"Mare Gastro · سابانجا",
        "cta_h":"احجز", "cta_h_em":"طاولتك", "cta_p":"احجز طاولتك لأمسية لا تُنسى على ضفاف بحيرة سابانجا، في حديقة فندق Didi Otel.",
        "cta_res":"إجراء حجز","cta_wa":"واتساب","cta_menu":"عرض القائمة",
        "footer_tag":"فاين داينينغ · سابانجا · حديقة فندق Didi Otel","footer_home":"الرئيسية","footer_within":"ضمن",
        "breadcrumb_home":"الرئيسية"},
 "ru": {"blog":"Блог","menu":"Меню","rez":"Бронирование","home":"Главная","read_more":"Читать статью →",
        "you_may_like":"Вам также может понравиться","faq_title":"Часто задаваемые вопросы","faq_sub":"Mare Gastro · Сапанджа",
        "cta_h":"Забронируйте", "cta_h_em":"столик", "cta_p":"Забронируйте столик для незабываемого вечера на озере Сапанджа, в саду отеля Didi Otel.",
        "cta_res":"Забронировать","cta_wa":"WhatsApp","cta_menu":"Посмотреть меню",
        "footer_tag":"Высокая кухня · Сапанджа · Сад отеля Didi Otel","footer_home":"Главная","footer_within":"на территории",
        "breadcrumb_home":"Главная"},
}

HTML_LANG = {"en":"en", "ar":"ar", "ru":"ru"}
LOCALE = {"en":"en_US", "ar":"ar_AR", "ru":"ru_RU"}
DIR_ATTR = {"en":"", "ar":' dir="rtl"', "ru":""}

def L(url, txt): return '<a href="%s">%s</a>' % (url, txt)
def post_url(slug, lang): return "%s/%s/blog/%s.html" % (SITE, lang, slug) if slug in SLUGS else "%s/blog/%s.html" % (SITE, slug)
def bfig(img, alt, caption):
    return ('<figure class="bbody-fig"><img src="/images/%s" alt="%s" loading="lazy">'
            '<figcaption>%s</figcaption></figure>' % (img, html.escape(alt), html.escape(caption)))
def strip_tags(s): return re.sub(r"<[^>]+>", "", s)
def MENU_A(lang): return "%s/%s/#menu" % (SITE, lang)
def REZ_A(lang): return "%s/%s/#reservation" % (SITE, lang)
def STORY_A(lang): return "%s/%s/#story" % (SITE, lang)
def CHEF_A(lang): return "%s/%s/#chef" % (SITE, lang)
def LOC_A(lang): return "%s/%s/#contact" % (SITE, lang)

SOCIAL_FOOT = (
 '<div class="bfoot-soc">'
 '<a href="%s" target="_blank" rel="noopener" aria-label="Instagram">%s</a>'
 '<a href="%s" target="_blank" rel="noopener" aria-label="Chef Instagram">%s</a>'
 '<a href="%s" target="_blank" rel="noopener" aria-label="TikTok">%s</a>'
 '<a href="%s" target="_blank" rel="noopener" aria-label="YouTube">%s</a>'
 '<a href="%s" target="_blank" rel="noopener" aria-label="WhatsApp">%s</a>'
 '<a href="%s" aria-label="Email">%s</a>'
 '</div>' % (IG, IC_IG, IGCHEF, IC_IG, TT, IC_TT, YT, IC_YT, WA, IC_WA, MAIL, IC_MAIL))

def nav_html(lang):
    t = NAV_LABELS[lang]
    return ('<nav class="bnav">'
      '<a class="logo" href="%s/%s/"><img src="/images/marelogo1.png" alt="Mare Gastro"></a>'
      '<div class="bnav-links">'
      '<a href="/%s/blog/">%s</a>'
      '<a href="%s">%s</a>'
      '<a href="%s" class="bnav-res">%s</a>'
      '</div></nav>' % (SITE, lang, lang, t["blog"], MENU_A(lang), t["menu"], REZ_A(lang), t["rez"]))

def footer_html(lang):
    t = NAV_LABELS[lang]
    return ('<footer class="bfoot">'
      '<div class="bfoot-logo"><img src="/images/marelogo1.png" alt="Mare Gastro"></div>'
      '<div class="bfoot-tag">%s</div>' % t["footer_tag"]
      + SOCIAL_FOOT +
      '<div class="bfoot-links">'
      '<a href="%s/%s/">%s</a><a href="/%s/blog/">%s</a>'
      '<a href="%s">%s</a><a href="%s">%s</a>'
      '</div>'
      '<div class="bfoot-copy">© 2026 Mare Gastro · '
      '<a href="%s" target="_blank" rel="noopener">Didi Otel</a> %s</div>'
      '</footer>' % (SITE, lang, t["footer_home"], lang, t["blog"], MENU_A(lang), t["menu"], REZ_A(lang), t["rez"], DIDI, t["footer_within"]))

def cta_html(lang):
    t = NAV_LABELS[lang]
    return ('<section class="bcta"><div class="bcta-inner">'
      '<h2>%s <em>%s</em></h2>'
      '<p>%s</p>'
      '<div class="bcta-btns">'
      '<a class="btn-gold" href="%s">%s</a>'
      '<a class="btn-wa" href="%s" target="_blank" rel="noopener">%s %s</a>'
      '<a class="btn-line" href="%s">%s</a>'
      '</div></div></section>' % (t["cta_h"], t["cta_h_em"], t["cta_p"], REZ_A(lang), t["cta_res"], WA, IC_WA, t["cta_wa"], MENU_A(lang), t["cta_menu"]))

def related_html(lang, slugs, posts_by_slug):
    t = NAV_LABELS[lang]
    cards = []
    for s in slugs:
        p = posts_by_slug[s][lang]
        cards.append(
          '<a class="brel-card" href="%s.html">'
          '<div class="brel-card-img"><img src="/images/%s" alt="%s" loading="lazy"></div>'
          '<div class="brel-card-body"><span class="brel-card-cat">%s</span>'
          '<div class="brel-card-t">%s</div></div></a>'
          % (s, p["img"], html.escape(p["alt"]), CATS[p["cat"]][lang], strip_tags(p["h1"])))
    return ('<section class="brel"><div class="brel-h">%s</div>'
            '<div class="brel-grid">%s</div></section>' % (t["you_may_like"], "".join(cards)))

def body_html(sections):
    out = []
    for h2, paras in sections:
        out.append("<h2>%s</h2>" % h2)
        for para in paras:
            if para.strip().startswith("<ul") or para.strip().startswith("<ol") or para.strip().startswith("<figure"):
                out.append(para)
            else:
                out.append("<p>%s</p>" % para)
    return "\n".join(out)

def faq_accordion(lang, faqs):
    t = NAV_LABELS[lang]
    items = []
    for q, a in faqs:
        items.append('<details><summary>%s</summary><div class="bfaq-a">%s</div></details>' % (html.escape(q), html.escape(a)))
    return ('<section class="bfaq"><h2 class="bfaq-title">%s</h2>'
            '<div class="bfaq-sub">%s</div>%s</section>' % (t["faq_title"], t["faq_sub"], "".join(items)))

def schema_graph(lang, p, slug):
    url = post_url(slug, lang)
    img = "%s/images/%s" % (SITE, p["img"])
    blog = {"@type":"BlogPosting","@id":url+"#article","headline":strip_tags(p["h1"]),
      "name":p["title"],"description":p["desc"],"image":img,"url":url,
      "datePublished":p["date"],"dateModified":p["date"],"inLanguage":lang,
      "articleSection":CATS[p["cat"]][lang],"keywords":p["kw"],
      "mainEntityOfPage":{"@type":"WebPage","@id":url},
      "author":{"@type":"Person","name":"Doğan Anapa","jobTitle":"Executive Chef","url":"%s/%s/#chef"%(SITE,lang),
        "worksFor":{"@type":"Organization","name":"Mare Gastro","url":SITE}},
      "publisher":{"@type":"Organization","name":"Mare Gastro",
        "logo":{"@type":"ImageObject","url":"%s/images/marelogo1.png"%SITE}}}
    crumb = {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":NAV_LABELS[lang]["breadcrumb_home"],"item":"%s/%s/"%(SITE,lang)},
      {"@type":"ListItem","position":2,"name":NAV_LABELS[lang]["blog"],"item":"%s/%s/blog/"%(SITE,lang)},
      {"@type":"ListItem","position":3,"name":strip_tags(p["h1"]),"item":url}]}
    faq = {"@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in p["faq"]]}
    return json.dumps({"@context":"https://schema.org","@graph":[blog, crumb, faq]}, ensure_ascii=False, indent=1)

PAGE = """<!DOCTYPE html>
<html lang="{htmllang}"{dir}>
<head>
{gtm_head}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<meta name="author" content="Mare Gastro">
<meta name="theme-color" content="#04080F">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="/images/marelogo.png">
{hreflang}
<meta property="og:type" content="article">
<meta property="og:site_name" content="Mare Gastro">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="{locale}">
<meta property="article:published_time" content="{date}">
<meta property="article:section" content="{cat}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/blog/blog.css">
<script type="application/ld+json">
{schema}
</script>
</head>
<body>
{gtm_body}
{nav}
<header class="bhero">
  <nav class="bcrumb" aria-label="breadcrumb"><a href="{site}/{lang}/">{home}</a> · <a href="/{lang}/blog/">{blogword}</a> · {cat}</nav>
  <span class="beyebrow">{cat}</span>
  <h1>{h1}</h1>
  <div class="bmeta"><span>{date_tr}</span><span class="dot"></span><span>{read}</span><span class="dot"></span><span>Mare Gastro</span></div>
</header>
<figure class="bfig"><div class="bfig-inner"><img src="/images/{imgfile}" alt="{alt}"></div></figure>
<article class="bwrap">
  <p class="blead">{lead}</p>
  <div class="bbody">
{body}
  </div>
  <div class="bdivider"></div>
</article>
{faq}
{cta}
{related}
{footer}
</body>
</html>
"""

def build_post(lang, slug, p, posts_by_slug):
    url = post_url(slug, lang)
    img = "%s/images/%s" % (SITE, p["img"])
    hreflang_links = ['<link rel="alternate" hreflang="tr" href="%s/blog/%s.html">' % (SITE, slug)]
    for l2 in ("en", "ar", "ru"):
        hreflang_links.append('<link rel="alternate" hreflang="%s" href="%s/%s/blog/%s.html">' % (l2, SITE, l2, slug))
    hreflang_links.append('<link rel="alternate" hreflang="x-default" href="%s/blog/%s.html">' % (SITE, slug))
    h = PAGE.format(
      htmllang=HTML_LANG[lang], dir=DIR_ATTR[lang],
      title=html.escape(p["title"]), desc=html.escape(p["desc"]), kw=html.escape(p["kw"]),
      url=url, img=img, imgfile=p["img"], alt=html.escape(p["alt"]),
      date=p["date"], date_tr=p["date"], read=p["read"], cat=CATS[p["cat"]][lang],
      site=SITE, lang=lang, home=NAV_LABELS[lang]["breadcrumb_home"], blogword=NAV_LABELS[lang]["blog"],
      h1=p["h1"], lead=p["lead"],
      body=body_html(p["body"]), faq=faq_accordion(lang, p["faq"]), cta=cta_html(lang),
      related=related_html(lang, p["rel"], posts_by_slug), footer=footer_html(lang), nav=nav_html(lang),
      hreflang="\n".join(hreflang_links),
      schema=schema_graph(lang, p, slug), gtm_head=GTM_HEAD, gtm_body=GTM_BODY, locale=LOCALE[lang])
    out_dir = os.path.join(OUT_ROOT, lang, "blog")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "%s.html" % slug), "w", encoding="utf-8") as f:
        f.write(h)

INDEX_TITLE = {"en":"Blog | Mare Gastro — Sapanca Fine Dining Guide",
               "ar":"المدونة | Mare Gastro — دليل الطعام الفاخر في سابانجا",
               "ru":"Блог | Mare Gastro — Гид по high-end кухне в Сапанджа"}
INDEX_DESC = {"en":"Sapanca luxury restaurant, fine dining, seafood and gourmet guide. Everything about dining in Sapanca, from Mare Gastro's blog.",
              "ar":"دليل المطاعم الفاخرة والمأكولات البحرية في سابانجا. كل ما يتعلق بالطعام في سابانجا من مدونة Mare Gastro.",
              "ru":"Гид по роскошным ресторанам, высокой кухне и морепродуктам Сапанджа. Все о ресторанах Сапанджа из блога Mare Gastro."}
INDEX_H1 = {"en":'Sapanca <em>Dining</em> Guide', "ar":'دليل <em>الطعام</em> في سابانجا', "ru":'Гид по <em>ресторанам</em> Сапанджа'}
INDEX_SUB = {"en":"Fine dining by the lake, fresh seafood, chef stories, and everything about gourmet life in Sapanca.",
             "ar":"فاين داينينغ على ضفاف البحيرة، مأكولات بحرية طازجة، وكل ما يخص الحياة الفاخرة في سابانجا.",
             "ru":"Высокая кухня у озера, свежие морепродукты и все о гастрономической жизни в Сапанджа."}
INDEX_EYEBROW = {"en":"Mare Gastro Journal", "ar":"مجلة Mare Gastro", "ru":"Журнал Mare Gastro"}

INDEX = """<!DOCTYPE html>
<html lang="{htmllang}"{dir}>
<head>
{gtm_head}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}/{lang}/blog/">
<link rel="icon" type="image/png" href="/images/marelogo.png">
{hreflang}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mare Gastro">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}/{lang}/blog/">
<meta property="og:image" content="{site}/images/og-image.jpg">
<meta property="og:locale" content="{locale}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/blog/blog.css">
</head>
<body>
{gtm_body}
{nav}
<header class="bidx-hero">
  <span class="beyebrow">{eyebrow}</span>
  <h1>{h1}</h1>
  <p>{sub}</p>
</header>
<main class="bidx-grid">
{cards}
</main>
{footer}
</body>
</html>
"""

def build_index(lang, slugs, posts_by_slug):
    ordered = sorted(slugs, key=lambda s: posts_by_slug[s][lang]["date"], reverse=True)
    cards = []
    for s in ordered:
        p = posts_by_slug[s][lang]
        cards.append(
          '<a class="bidx-card" href="%s.html">'
          '<div class="bidx-card-img"><img src="/images/%s" alt="%s" loading="lazy"></div>'
          '<div class="bidx-card-body"><span class="bidx-card-cat">%s</span>'
          '<div class="bidx-card-t">%s</div><div class="bidx-card-d">%s</div>'
          '<span class="bidx-card-more">%s</span></div></a>'
          % (s, p["img"], html.escape(p["alt"]), CATS[p["cat"]][lang], strip_tags(p["h1"]),
             html.escape(p["desc"]), NAV_LABELS[lang]["read_more"]))
    hreflang_links = ['<link rel="alternate" hreflang="tr" href="%s/blog/">' % SITE]
    for l2 in ("en", "ar", "ru"):
        hreflang_links.append('<link rel="alternate" hreflang="%s" href="%s/%s/blog/">' % (l2, SITE, l2))
    hreflang_links.append('<link rel="alternate" hreflang="x-default" href="%s/blog/">' % SITE)
    h = INDEX.format(site=SITE, lang=lang, htmllang=HTML_LANG[lang], dir=DIR_ATTR[lang],
      title=html.escape(INDEX_TITLE[lang]), desc=html.escape(INDEX_DESC[lang]),
      nav=nav_html(lang), footer=footer_html(lang), cards="\n".join(cards),
      eyebrow=INDEX_EYEBROW[lang], h1=INDEX_H1[lang], sub=INDEX_SUB[lang],
      hreflang="\n".join(hreflang_links), locale=LOCALE[lang],
      gtm_head=GTM_HEAD, gtm_body=GTM_BODY)
    out_dir = os.path.join(OUT_ROOT, lang, "blog")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(h)

SLUGS = set()  # populated by posts_i18n_data module before build

REL_MAP = {
 "sapanca-luks-restoran": ["sapancanin-en-iyi-restorani","sapanca-fine-dining-nedir","sapanca-deniz-urunleri"],
 "sapanca-deniz-urunleri": ["sapanca-luks-restoran","sapanca-fine-dining-nedir","sapancaya-nasil-gidilir"],
 "sapanca-fine-dining-nedir": ["sapanca-luks-restoran","sapancanin-en-iyi-restorani","sapanca-deniz-urunleri"],
 "sapanca-hafta-sonu-rotasi": ["sapancaya-nasil-gidilir","sapanca-luks-restoran","sapanca-istanbula-yakin-evlilik-teklifi-mekanlari"],
 "sapanca-kurumsal-etkinlik-en-iyi-mekanlar": ["sapanca-istanbula-yakin-sirket-etkinligi-mekani","sapanca-luks-restoran","sapanca-hafta-sonu-rotasi"],
 "sapanca-istanbula-yakin-sirket-etkinligi-mekani": ["sapanca-kurumsal-etkinlik-en-iyi-mekanlar","sapancaya-nasil-gidilir","sapanca-hafta-sonu-rotasi"],
 "sapanca-en-iyi-dogum-gunu-mekanlari": ["sapanca-yildonumu-icin-en-iyi-mekan","sapanca-istanbula-yakin-luks-dogum-gunu-mekanlari","sapancanin-en-iyi-restorani"],
 "sapancanin-en-iyi-restorani": ["sapanca-luks-restoran","sapanca-en-iyi-dogum-gunu-mekanlari","sapanca-fine-dining-nedir"],
 "sapancaya-nasil-gidilir": ["sapanca-hafta-sonu-rotasi","sapanca-istanbula-yakin-evlilik-teklifi-mekanlari","sapanca-luks-restoran"],
 "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari": ["sapanca-istanbula-yakin-luks-dogum-gunu-mekanlari","sapanca-yildonumu-icin-en-iyi-mekan","sapancaya-nasil-gidilir"],
 "sapanca-istanbula-yakin-luks-dogum-gunu-mekanlari": ["sapanca-istanbula-yakin-evlilik-teklifi-mekanlari","sapanca-en-iyi-dogum-gunu-mekanlari","sapancaya-nasil-gidilir"],
 "sapanca-yildonumu-icin-en-iyi-mekan": ["sapanca-istanbula-yakin-evlilik-teklifi-mekanlari","sapanca-en-iyi-dogum-gunu-mekanlari","sapancanin-en-iyi-restorani"],
}

def run(posts_by_slug):
    global SLUGS
    SLUGS = set(posts_by_slug.keys())
    for slug, per_lang in posts_by_slug.items():
        for lang in ("en", "ar", "ru"):
            per_lang[lang]["rel"] = REL_MAP[slug]
            build_post(lang, slug, per_lang[lang], posts_by_slug)
    for lang in ("en", "ar", "ru"):
        build_index(lang, list(posts_by_slug.keys()), posts_by_slug)
    print("Built %d posts x 3 languages + 3 index pages" % len(posts_by_slug))
