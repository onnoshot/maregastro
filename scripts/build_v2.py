#!/usr/bin/env python3
"""Mare Gastro v2 (light theme) builder.

Idempotent: always starts from the `main` branch copy of each language page
(git show main:<lang>/index.html), so re-running never stacks changes.

  1. Extracts the shared inline <style> block -> assets/v2/site.css after a
     dark->light colour transform, then appends assets/v2/layer.css.
  2. Injects new engagement sections (marquee, stats, ambiance gallery,
     signature dishes, reviews, occasions, mobile action bar) translated
     per language, without touching existing markup / IDs / JS.
  3. Loads GSAP + ScrollTrigger + SplitText + Lenis (self-hosted) + motion.js.

Usage:
  python3 -I scripts/build_v2.py --css   # LIVE MODE: only regenerate assets/v2/site.css
                                          # (base CSS from the last pre-v2 commit + layer.css)
  python3 -I scripts/build_v2.py         # one-time page build; refuses if pages are already v2

Since v2 went live (2026-11-07) the language pages are the source of truth:
edit tr/en/ar/ru/index.html directly, style changes go in assets/v2/layer.css,
then run --css.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["tr", "en", "ar", "ru"]
VER = "2"

PRE_V2_REF = "76e77c3"   # last commit with the original dark pages (base CSS source)

def main_copy(path, ref="main"):
    return subprocess.check_output(["git", "-C", ROOT, "show", ref + ":" + path]).decode("utf-8")

# ─────────────────────────── colour transform ───────────────────────────
INK = (16, 32, 46)          # deep sea navy used as text on ivory
IVORY = (251, 248, 242)

def _f(x):
    s = ("%.3f" % x).rstrip("0").rstrip(".")
    return s[1:] if s.startswith("0.") else s

def transform_css(css):
    out = []
    for line in css.split("\n"):
        out.append(transform_line(line))
    css = "\n".join(out)
    # tokens
    css = re.sub(r"--bg:#04080F;", "--bg:#FBF8F2;", css)
    css = re.sub(r"--navy:#08131E;", "--navy:#F2ECE1;", css)
    css = css.replace("--amber:#C8A96E;", "--amber:#9C7437;")
    css = css.replace("--amber2:#DFC08A;", "--amber2:#B08445;")
    css = css.replace("--amber3:rgba(200,169,110,.15);", "--amber3:rgba(156,116,55,.12);")
    css = css.replace("--cream:#EDE8DC;", "--cream:#10202E;")
    css = css.replace("--muted:rgba(237,232,220,.45);", "--muted:rgba(16,32,46,.62);")
    css = css.replace("--glass:rgba(16,32,46,.033);", "--glass:rgba(255,255,255,.66);")
    css = css.replace("--glassBorder:rgba(16,32,46,.054);", "--glassBorder:rgba(16,32,46,.1);")
    css = css.replace("--glassHover:rgba(16,32,46,.06);", "--glassHover:rgba(255,255,255,.92);")
    css = css.replace("#F2EEE4", "#1B2B38")
    css = css.replace("background:#0c1420", "background:#EDE6DA")
    return css

def transform_line(line):
    # which property is this declaration? (lines may hold several; handle per-declaration)
    def repl_decl(m):
        prop, val = m.group(1), m.group(2)
        is_bg = prop.startswith("background")
        is_shadow = "shadow" in prop
        def rgba(mm):
            r, g, b, a = int(mm.group(1)), int(mm.group(2)), int(mm.group(3)), float(mm.group(4))
            if (r, g, b) == (255, 255, 255):
                if is_bg:
                    return "rgba(255,255,255,%s)" % _f(min(.92, a * 11 + .1))
                if is_shadow:   # inset highlights stay white
                    return "rgba(255,255,255,%s)" % _f(min(.9, a * 8))
                return "rgba(16,32,46,%s)" % _f(a * .6)
            if (r, g, b) == (237, 232, 220):
                return "rgba(16,32,46,%s)" % _f(max(a, .12) if a < .3 else a + .1)
            if (r, g, b) in [(4, 8, 15), (5, 9, 15), (8, 19, 30), (10, 15, 20)]:
                return "rgba(251,248,242,%s)" % _f(a)
            if (r, g, b) == (0, 0, 0):
                return "rgba(16,32,46,%s)" % _f(a * .32)
            if (r, g, b) == (200, 169, 110):
                return "rgba(156,116,55,%s)" % _f(a)
            if (r, g, b) == (223, 192, 138):
                return "rgba(176,132,69,%s)" % _f(a)
            return mm.group(0)
        val = re.sub(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)", rgba, val)
        return prop + ":" + val
    return re.sub(r"([a-z-]+)\s*:\s*([^;{}]+)", repl_decl, line)

# ─────────────────────────── translations ───────────────────────────
T = {
 "tr": dict(
  marquee=["Ege & Akdeniz Mutfağı", "Sapanca Gölü", "Fine Dining", "Didi Otel Bahçesi", "Şef Doğan Anapa", "Açık & Kapalı Alan", "Canlı Müzik"],
  stats_eyebrow="Rakamlarla Mare",
  stats=[("4,9", "4.9", "Google puanı", 1), ("200+", "200", "Menüdeki lezzet", 0), ("2023", "2023", "Gourmand Ödülü", 0), ("09–00", None, "Salı – Pazar açık", 0)],
  amb_eyebrow="Mekân", amb_title="Bahçede, ışıkta, <em>göle karşı</em>",
  amb_body="Gün ışığında gölgeli kabanalar, akşam olunca mum ışığında bir teras. Fotoğraflara dokunarak büyütün.",
  amb_alts=["Mare Gastro bahçe manzarası", "Kabana oturma alanı", "Terasta misafir", "Akşam terası", "Sofra detayı", "Havuz kenarı şezlonglar"],
  sig_eyebrow="İmza Tabaklar", sig_title="Şefin <em>favorileri</em>", sig_hint="Kaydırın · bir tabağa dokunun, menüde açılsın", sig_cta="Tüm menüyü gör",
  rev_eyebrow="Misafirlerimiz", rev_title="Google'da <em>4,9</em> puan", rev_src="Google Yorumu", rev_note="", rev_all="Tüm yorumları oku", rev_all_href="/blog/mare-gastro-google-yorumlari.html",
  occ_eyebrow="Özel Anlar", occ_title="Hayatın en güzel <em>kutlamaları</em>", occ_more="Keşfet",
  occ=[("Doğum Günü", "Pasta, süsleme ve göle karşı bir masa", "sapanca-en-iyi-dogum-gunu-mekanlari.html", "mare-kutlama-kadeh.webp"),
       ("Yıldönümü", "Mum ışığında iki kişilik bir akşam", "sapanca-yildonumu-icin-en-iyi-mekan.html", "mare-romantik-kadeh.webp"),
       ("Evlilik Teklifi", "Gece terasında unutulmaz bir \"evet\"", "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari.html", "mare-gece-terasi.webp"),
       ("Kurumsal Davet", "İş yemeği ve ekip buluşmaları", "sapanca-kurumsal-etkinlik-en-iyi-mekanlar.html", "mare-grup-sofra.webp")],
  bar_rez="Rezervasyon", bar_dir="Yol Tarifi", bar_call="Ara", top="Yukarı", close="Kapat",
 ),
 "en": dict(
  marquee=["Aegean & Mediterranean Cuisine", "Lake Sapanca", "Fine Dining", "Didi Hotel Garden", "Chef Doğan Anapa", "Indoor & Outdoor", "Live Music"],
  stats_eyebrow="Mare in Numbers",
  stats=[("4.9", "4.9", "Google rating", 1), ("200+", "200", "Dishes & drinks", 0), ("2023", "2023", "Gourmand Award", 0), ("09–00", None, "Open Tuesday – Sunday", 0)],
  amb_eyebrow="The Place", amb_title="In the garden, in the light, <em>by the lake</em>",
  amb_body="Shaded cabanas by day, a candlelit terrace by night. Tap a photo to enlarge it.",
  amb_alts=["Mare Gastro garden view", "Cabana seating", "Guest on the terrace", "Evening terrace", "Table detail", "Poolside loungers"],
  sig_eyebrow="Signature Plates", sig_title="The chef's <em>favourites</em>", sig_hint="Swipe · tap a plate to open it in the menu", sig_cta="See the full menu",
  rev_eyebrow="Our Guests", rev_title="<em>4.9</em> on Google", rev_src="Google review", rev_note="Translated from Turkish", rev_all="Read all reviews", rev_all_href="/en/blog/",
  occ_eyebrow="Special Moments", occ_title="Life's finest <em>celebrations</em>", occ_more="Discover",
  occ=[("Birthday", "Cake, decoration and a table facing the lake", "sapanca-en-iyi-dogum-gunu-mekanlari.html", "mare-kutlama-kadeh.webp"),
       ("Anniversary", "A candlelit evening for two", "sapanca-yildonumu-icin-en-iyi-mekan.html", "mare-romantik-kadeh.webp"),
       ("Marriage Proposal", "An unforgettable \"yes\" on the night terrace", "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari.html", "mare-gece-terasi.webp"),
       ("Corporate Events", "Business dinners and team gatherings", "sapanca-kurumsal-etkinlik-en-iyi-mekanlar.html", "mare-grup-sofra.webp")],
  bar_rez="Reserve", bar_dir="Directions", bar_call="Call", top="Top", close="Close",
 ),
 "ar": dict(
  marquee=["مطبخ إيجه والبحر المتوسط", "بحيرة سابانجا", "مطعم فاخر", "حديقة فندق ديدي", "الشيف دوغان أنابا", "أماكن داخلية وخارجية", "موسيقى حية"],
  stats_eyebrow="ماري بالأرقام",
  stats=[("4.9", "4.9", "تقييم Google", 1), ("200+", "200", "طبق ومشروب", 0), ("2023", "2023", "جائزة Gourmand", 0), ("09–00", None, "مفتوح من الثلاثاء إلى الأحد", 0)],
  amb_eyebrow="المكان", amb_title="في الحديقة، تحت الضوء، <em>قرب البحيرة</em>",
  amb_body="أكواخ مظللة نهاراً، وتراس على ضوء الشموع ليلاً. اضغط على الصورة لتكبيرها.",
  amb_alts=["إطلالة حديقة ماري غاسترو", "جلسة الكابانا", "ضيف على التراس", "التراس مساءً", "تفاصيل المائدة", "كراسي بجانب المسبح"],
  sig_eyebrow="أطباق مميزة", sig_title="<em>مفضلات</em> الشيف", sig_hint="مرّر · اضغط على طبق لفتحه في القائمة", sig_cta="عرض القائمة كاملة",
  rev_eyebrow="ضيوفنا", rev_title="تقييم <em>4.9</em> على Google", rev_src="تقييم Google", rev_note="مترجم من التركية", rev_all="اقرأ كل التقييمات", rev_all_href="/ar/blog/",
  occ_eyebrow="لحظات خاصة", occ_title="أجمل <em>احتفالات</em> الحياة", occ_more="اكتشف",
  occ=[("عيد ميلاد", "كعكة وزينة وطاولة مطلة على البحيرة", "sapanca-en-iyi-dogum-gunu-mekanlari.html", "mare-kutlama-kadeh.webp"),
       ("ذكرى زواج", "أمسية لشخصين على ضوء الشموع", "sapanca-yildonumu-icin-en-iyi-mekan.html", "mare-romantik-kadeh.webp"),
       ("طلب زواج", "«نعم» لا تُنسى على التراس الليلي", "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari.html", "mare-gece-terasi.webp"),
       ("مناسبات الشركات", "عشاء عمل ولقاءات الفرق", "sapanca-kurumsal-etkinlik-en-iyi-mekanlar.html", "mare-grup-sofra.webp")],
  bar_rez="احجز", bar_dir="الاتجاهات", bar_call="اتصل", top="أعلى", close="إغلاق",
 ),
 "ru": dict(
  marquee=["Эгейская и средиземноморская кухня", "Озеро Сапанджа", "Fine Dining", "Сад отеля Didi", "Шеф Доган Анапа", "Зал и терраса", "Живая музыка"],
  stats_eyebrow="Mare в цифрах",
  stats=[("4,9", "4.9", "рейтинг Google", 1), ("200+", "200", "блюд и напитков", 0), ("2023", "2023", "премия Gourmand", 0), ("09–00", None, "со вторника по воскресенье", 0)],
  amb_eyebrow="Место", amb_title="В саду, в свете, <em>у озера</em>",
  amb_body="Тенистые кабаны днём и терраса при свечах вечером. Нажмите на фото, чтобы увеличить.",
  amb_alts=["Вид на сад Mare Gastro", "Кабаны", "Гость на террасе", "Вечерняя терраса", "Детали сервировки", "Шезлонги у бассейна"],
  sig_eyebrow="Фирменные блюда", sig_title="<em>Любимое</em> шефа", sig_hint="Листайте · нажмите на блюдо, чтобы открыть его в меню", sig_cta="Всё меню",
  rev_eyebrow="Наши гости", rev_title="<em>4,9</em> в Google", rev_src="Отзыв в Google", rev_note="Перевод с турецкого", rev_all="Читать все отзывы", rev_all_href="/ru/blog/",
  occ_eyebrow="Особые моменты", occ_title="Самые красивые <em>праздники</em>", occ_more="Подробнее",
  occ=[("День рождения", "Торт, украшения и стол с видом на озеро", "sapanca-en-iyi-dogum-gunu-mekanlari.html", "mare-kutlama-kadeh.webp"),
       ("Годовщина", "Вечер для двоих при свечах", "sapanca-yildonumu-icin-en-iyi-mekan.html", "mare-romantik-kadeh.webp"),
       ("Предложение руки", "Незабываемое «да» на ночной террасе", "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari.html", "mare-gece-terasi.webp"),
       ("Корпоративы", "Деловые ужины и встречи команды", "sapanca-kurumsal-etkinlik-en-iyi-mekanlar.html", "mare-grup-sofra.webp")],
  bar_rez="Бронь", bar_dir="Маршрут", bar_call="Звонок", top="Наверх", close="Закрыть",
 ),
}

# Real Google reviews (already published on /blog/mare-gastro-google-yorumlari.html)
REVIEWS = [
 ("Fikriye Erkan", {
   "tr": "Tesadüfen bulup yorumlara bakarak geldim, iyi ki gelmişim! Yemekler, hizmet, ambiyans çok iyi, canlı DJ müzikler de şahaneydi. Evlilik yıldönümümüz için geldik, bu kadarını beklemiyordum.",
   "en": "I found it by chance and came after reading the reviews, so glad I did! The food, service and ambience were excellent and the live DJ music was wonderful. We came for our wedding anniversary and didn't expect this much.",
   "ar": "وجدته بالصدفة وجئت بعد قراءة التقييمات، ويا له من قرار موفق! الطعام والخدمة والأجواء ممتازة، وموسيقى الدي جي الحية كانت رائعة. جئنا للاحتفال بذكرى زواجنا ولم نتوقع كل هذا.",
   "ru": "Нашла случайно и пришла, почитав отзывы, — и не пожалела! Еда, сервис, атмосфера на высоте, живая музыка от диджея была прекрасной. Пришли на годовщину свадьбы и не ожидали такого."}),
 ("Yasemin Babadağ", {
   "tr": "Karşılamadan başlayıp son ana kadar size kendinizi özel hissettiren, hem görsel hem lezzet şöleniyle geceyi taçlandıran bir yer olmuş. Elinize emeğinize sağlık.",
   "en": "From the welcome to the very last moment, a place that makes you feel special and crowns the night with a feast for both the eyes and the palate. Thank you for all your effort.",
   "ar": "من لحظة الاستقبال حتى آخر لحظة، مكان يجعلك تشعر بأنك مميز ويتوّج الليلة بوليمة للعين والذوق معاً. سلمت أياديكم.",
   "ru": "С первой встречи и до последней минуты здесь чувствуешь себя особенным гостем, а вечер венчает настоящий праздник для глаз и вкуса. Спасибо за ваш труд."}),
 ("Büşra Canbazoğlu", {
   "tr": "İlk gidişimize rağmen atmosfere hayran kaldık. Evlilik yıldönümümüzü unutulmaz kıldı bu mekan — ortam, sunum, hizmet, müzik dört dörtlüktü. Yemek sanata dönüşmüş halde önünüze geliyor.",
   "en": "Even on our first visit we fell in love with the atmosphere. This place made our anniversary unforgettable — setting, presentation, service and music were flawless. The food arrives as a work of art.",
   "ar": "رغم أنها زيارتنا الأولى، أُعجبنا بالأجواء كثيراً. جعل هذا المكان ذكرى زواجنا لا تُنسى — المكان والتقديم والخدمة والموسيقى كلها مثالية. الطعام يصل إليك وكأنه عمل فني.",
   "ru": "Даже в первый визит мы были очарованы атмосферой. Это место сделало нашу годовщину незабываемой — обстановка, подача, сервис и музыка безупречны. Еда подаётся как произведение искусства."}),
 ("Emel Kamsız", {
   "tr": "Sapanca'da yaşayan biri olarak gerçekten severek geldiğim yerlerden biri. Hem yemekleri hem atmosferi hem de hizmetiyle her seferinde memnun ayrılıyorum.",
   "en": "As someone who lives in Sapanca, this is one of the places I truly love coming to. I leave happy every time — the food, the atmosphere and the service.",
   "ar": "بصفتي من سكان سابانجا، هذا من الأماكن التي أحب المجيء إليها حقاً. أغادر سعيدة في كل مرة بالطعام والأجواء والخدمة.",
   "ru": "Я живу в Сапандже, и это одно из мест, куда я прихожу с удовольствием. Каждый раз ухожу довольной — и кухней, и атмосферой, и сервисом."}),
 ("Oylum Genç", {
   "tr": "Bir günlüğüne geldiğimiz Sapanca tatilimizin en başarılı kararıydı. Yemekleri, kokteylleri, çalışan personeli, ambiyansı inanılmaz iyi. Hiç düşünmeden tavsiye ediyorum.",
   "en": "The best decision of our one-day trip to Sapanca. The food, cocktails, staff and ambience are incredibly good. I recommend it without a second thought.",
   "ar": "كان أفضل قرار في رحلتنا ليوم واحد إلى سابانجا. الطعام والكوكتيلات والطاقم والأجواء رائعة بشكل لا يصدق. أنصح به دون تردد.",
   "ru": "Лучшее решение нашей однодневной поездки в Сапанджу. Еда, коктейли, персонал и атмосфера невероятно хороши. Рекомендую без раздумий."}),
 ("İnci Ogan", {
   "tr": "Tesadüfen geldik ama ambiyans da yemek de çok başarılıydı. Garsonumuz Ömer Bey tüm akşam boyunca son derece ilgiliydi. Sapanca'ya yolumuz düşerse mutlaka yeniden geleceğiz.",
   "en": "We came by chance, but both the ambience and the food were excellent. Our waiter Ömer was extremely attentive all evening. If we're in Sapanca again, we'll definitely be back.",
   "ar": "جئنا بالصدفة، لكن الأجواء والطعام كانا ممتازين. كان النادل عمر في غاية الاهتمام طوال الأمسية. إن مررنا بسابانجا مجدداً فسنعود حتماً.",
   "ru": "Зашли случайно, но и атмосфера, и еда были великолепны. Наш официант Омер был очень внимателен весь вечер. Если снова окажемся в Сапандже, обязательно вернёмся."}),
 ("Mert Efe Demir", {
   "tr": "Çok şık ve nezih bir mekan, yıl dönümümüz için burayı tercih ettik ve çok memnun kaldık. Özellikle servis ekibine teşekkür ediyorum. Kuzu incik tavsiyemdir.",
   "en": "A very elegant and refined place; we chose it for our anniversary and were delighted. Special thanks to the service team. I recommend the lamb shank.",
   "ar": "مكان أنيق وراقٍ جداً، اخترناه للاحتفال بذكرانا وكنا سعداء للغاية. شكر خاص لفريق الخدمة. أنصح بموزة الضأن.",
   "ru": "Очень элегантное и изысканное место — выбрали его для годовщины и остались в восторге. Отдельное спасибо команде сервиса. Рекомендую баранью голяшку."}),
]

AMB_IMGS = ["mare-bahce-manzarasi.webp", "mare-kabana-oturma.webp", "mare-teras-misafir.webp",
            "mare-gece-terasi.webp", "mare-sofra-detay.webp", "mare-havuz-sezlong.webp"]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ─────────────────────────── section builders ───────────────────────────
def marquee(t):
    items = "".join('<span class="mq-item">%s</span><span class="mq-star" aria-hidden="true">✦</span>' % esc(x) for x in t["marquee"])
    return ('\n<!-- ═══ V2: MARQUEE ═══ -->\n<div class="v2-marquee" aria-hidden="true"><div class="mq-track">'
            '<div class="mq-row">%s</div><div class="mq-row">%s</div></div></div>\n') % (items, items)

def stats(t):
    cells = []
    for shown, num, label, dec in t["stats"]:
        if num:
            n = '<span class="st-n" data-count="%s" data-dec="%d" data-final="%s">%s</span>' % (num, dec, esc(shown), esc(shown))
        else:
            n = '<span class="st-n st-time">%s</span>' % esc(shown)
        cells.append('<div class="st-cell">%s<span class="st-l">%s</span></div>' % (n, esc(label)))
    return ('\n<!-- ═══ V2: STATS ═══ -->\n<section class="v2-stats" aria-label="%s"><span class="v2-eyebrow v2-rv">%s</span>'
            '<div class="st-grid">%s</div></section>\n') % (esc(t["stats_eyebrow"]), esc(t["stats_eyebrow"]), "".join(cells))

def ambiance(t):
    figs = "".join('<button type="button" class="amb-fig amb-%d" data-full="/images/%s"><img loading="lazy" decoding="async" src="/images/%s" alt="%s"></button>'
                   % (i + 1, f, f, esc(t["amb_alts"][i])) for i, f in enumerate(AMB_IMGS))
    return ('\n<!-- ═══ V2: AMBIANCE ═══ -->\n<section class="v2-amb" id="ambiance"><div class="v2-wrap">'
            '<div class="v2-head"><span class="v2-eyebrow">%s</span><h2 class="v2-title v2-split">%s</h2><p class="v2-lead v2-rv">%s</p></div>'
            '<div class="amb-grid">%s</div></div></section>\n') % (esc(t["amb_eyebrow"]), t["amb_title"], esc(t["amb_body"]), figs)

def signature(t):
    return ('\n<!-- ═══ V2: SIGNATURE ═══ -->\n<section class="v2-sig" id="signature"><div class="sig-pin">'
            '<div class="v2-wrap sig-headwrap"><div class="v2-head"><span class="v2-eyebrow">%s</span><h2 class="v2-title v2-split">%s</h2>'
            '<p class="sig-hint v2-rv">%s</p></div>'
            '<a href="#menu" class="v2-btn-line v2-rv">%s <span aria-hidden="true">→</span></a></div>'
            '<div class="sig-track" id="sigTrack"></div></div></section>\n') % (
            esc(t["sig_eyebrow"]), t["sig_title"], esc(t["sig_hint"]), esc(t["sig_cta"]))

def reviews(t, lang):
    cards = []
    for name, txt in REVIEWS:
        note = ('<span class="rv-note">%s</span>' % esc(t["rev_note"])) if t["rev_note"] else ""
        cards.append('<figure class="rv-card"><div class="rv-stars" aria-label="5/5">★★★★★</div>'
                     '<blockquote>%s</blockquote><figcaption><span class="rv-av" aria-hidden="true">%s</span>'
                     '<span class="rv-who"><b>%s</b><small>%s</small></span></figcaption>%s</figure>'
                     % (esc("“" + txt[lang] + "”"), esc(name[0]), esc(name), esc(t["rev_src"]), note))
    track = "".join(cards)
    return ('\n<!-- ═══ V2: REVIEWS ═══ -->\n<section class="v2-rev" id="reviews"><div class="v2-wrap"><div class="v2-head v2-head-c">'
            '<span class="v2-eyebrow">%s</span><h2 class="v2-title v2-split">%s</h2></div></div>'
            '<div class="rev-marquee"><div class="rev-track">%s%s</div></div>'
            '<div class="v2-wrap v2-c"><a class="v2-btn-line v2-rv" href="%s">%s <span aria-hidden="true">→</span></a></div></section>\n') % (
            esc(t["rev_eyebrow"]), t["rev_title"], track, track.replace('<figure class="rv-card">', '<figure class="rv-card" aria-hidden="true">'),
            t["rev_all_href"], esc(t["rev_all"]))

def occasions(t, lang):
    base = "/blog/" if lang == "tr" else "/%s/blog/" % lang
    cards = "".join('<a class="occ-card" href="%s%s"><div class="occ-img"><img loading="lazy" decoding="async" src="/images/%s" alt="%s"></div>'
                    '<div class="occ-body"><h3>%s</h3><p>%s</p><span class="occ-more">%s <i aria-hidden="true">→</i></span></div></a>'
                    % (base, slug, img, esc(title), esc(title), esc(desc), esc(t["occ_more"]))
                    for title, desc, slug, img in t["occ"])
    return ('\n<!-- ═══ V2: OCCASIONS ═══ -->\n<section class="v2-occ" id="occasions"><div class="v2-wrap">'
            '<div class="v2-head"><span class="v2-eyebrow">%s</span><h2 class="v2-title v2-split">%s</h2></div>'
            '<div class="occ-grid">%s</div></div></section>\n') % (esc(t["occ_eyebrow"]), t["occ_title"], cards)

def chrome_top(t):
    return ('<script>(function(d){d.classList.add("v2-js");try{if(sessionStorage.getItem("mare_v2_seen"))d.classList.add("v2-seen");sessionStorage.setItem("mare_v2_seen","1")}catch(e){}'
            'setTimeout(function(){if(!d.classList.contains("v2-ready")){d.classList.add("v2-fallback");var l=document.getElementById("v2Loader");if(l)l.classList.add("done")}},4000)})(document.documentElement)</script>\n'
            '<div class="v2-loader" id="v2Loader" aria-hidden="true"><img src="/images/marelogo1.png" alt=""><span class="v2-loader-line"></span></div>\n'
            '<div class="v2-progress" id="v2Progress" aria-hidden="true"></div>\n')

def chrome_bottom(t):
    return ('\n<!-- ═══ V2: MOBILE ACTION BAR + LIGHTBOX + TOP ═══ -->\n'
            '<div class="v2-bar" id="v2Bar">'
            '<a href="#reservation" class="v2-bar-main" onclick="trackEvent(\'menu_click\',{event_label:\'mobile_bar\',element:\'reservation\'})">%s</a>'
            '<a href="https://maps.google.com/?q=40.7002438,30.222254" target="_blank" rel="noopener" onclick="trackEvent(\'directions_click\',{event_label:\'mobile_bar\'})">'
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>%s</a>'
            '<a href="tel:+905323540888" onclick="trackEvent(\'phone_click\',{event_label:\'mobile_bar\'})">'
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8 9.8a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.6 2.7.7a2 2 0 011.7 2z"/></svg>%s</a></div>\n'
            '<button type="button" class="v2-top" id="v2Top" aria-label="%s"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>\n'
            ) % (esc(t["bar_rez"]), esc(t["bar_dir"]), esc(t["bar_call"]), esc(t["top"]))

SCRIPTS = ('<script src="/assets/v2/vendor/gsap.min.js" defer></script>\n'
           '<script src="/assets/v2/vendor/ScrollTrigger.min.js" defer></script>\n'
           '<script src="/assets/v2/vendor/SplitText.min.js" defer></script>\n'
           '<script src="/assets/v2/vendor/lenis.min.js" defer></script>\n'
           '<script src="/assets/v2/motion.js?v=%s" defer></script>\n') % VER

# ─────────────────────────── page transform ───────────────────────────
def must_sub(pattern, repl, s, flags=0, count=1):
    new, n = re.subn(pattern, repl, s, count=count, flags=flags)
    if n == 0:
        sys.exit("pattern not found: %r" % pattern[:80])
    return new

def build_page(lang, base_css_holder):
    html = main_copy(lang + "/index.html")
    t = T[lang]
    # 1. main stylesheet -> external
    m = re.search(r"<style>\n:root\{.*?\n</style>", html, flags=re.S)
    if not m:
        sys.exit("main style block not found in " + lang)
    if base_css_holder[0] is None:
        base_css_holder[0] = m.group(0)[len("<style>\n"):-len("\n</style>")]
    html = html[:m.start()] + '<link rel="stylesheet" href="/assets/v2/site.css?v=%s">' % VER + html[m.end():]
    html = re.sub(r'<link href="https://fonts.googleapis.com/css2\?family=Cormorant[^"]*" rel="stylesheet">',
                  '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">', html)
    html = html.replace('<meta name="theme-color" content="#04080F">', '<meta name="theme-color" content="#FBF8F2">')
    html = html.replace('<html lang="%s"' % lang, '<html class="v2" lang="%s"' % lang, 1)
    # 2. chrome at body start
    html = must_sub(r"(<body>\n)", lambda mm: mm.group(1) + chrome_top(t), html)
    # 3. sections
    html = must_sub(r'(\n<!-- ═══ SC: )', lambda mm: stats(t) + mm.group(1), html)
    html = must_sub(r'(\n<!-- ═══ S3: )', lambda mm: signature(t) + mm.group(1), html)
    html = must_sub(r'(\n<!-- ═══ S4: )', lambda mm: reviews(t, lang) + occasions(t, lang) + mm.group(1), html)
    # 4. bottom chrome + scripts
    html = must_sub(r"(\n</body>)", lambda mm: "\n" + chrome_bottom(t) + SCRIPTS + mm.group(1), html)
    return html

def write_css(base_css):
    css = transform_css(base_css)
    with open(os.path.join(ROOT, "assets/v2/layer.css"), encoding="utf-8") as f:
        layer = f.read()
    with open(os.path.join(ROOT, "assets/v2/site.css"), "w", encoding="utf-8") as f:
        f.write("/* Mare Gastro v2 — generated by scripts/build_v2.py --css. Edit layer.css, not this file. */\n")
        f.write(css + "\n\n" + layer)
    print("site.css written")

def main():
    if "--css" in sys.argv:
        html = main_copy("tr/index.html", PRE_V2_REF)
        m = re.search(r"<style>\n:root\{.*?\n</style>", html, flags=re.S)
        write_css(m.group(0)[len("<style>\n"):-len("\n</style>")])
        return
    if "assets/v2/site.css" in main_copy("tr/index.html"):
        sys.exit("main already has the v2 pages; edit pages directly and use --css")
    holder = [None]
    for lang in LANGS:
        out = build_page(lang, holder)
        with open(os.path.join(ROOT, lang, "index.html"), "w", encoding="utf-8") as f:
            f.write(out)
        print("built", lang, len(out))
    write_css(holder[0])

if __name__ == "__main__":
    main()
