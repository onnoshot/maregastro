#!/usr/bin/env python3
"""Mare Gastro — official FAQ pages (TR /sss.html, EN/AR/RU /{lang}/faq.html).

Only facts already verified and published elsewhere on the site are used:
address, hours (Tue–Sun 09:00–00:00, Mon closed — owner confirmed 2026-10-25),
reservation flow, live menu categories (/api/menu, 2026-11-07), free parking + valet
(blog/sapanca-vale-otopark-restoran), vegetarian dishes (live menu), Didi Otel stay
option (reservation form), indoor+outdoor (owner), Google rating 4.9 (Maps, 2026-10-24),
~1.5 h from Istanbul (blog), chef Doğan Anapa (Gourmand 2023 Türkiye representative).
NOT stated (unverified): pets, dress code, price figures (owner decision: no numbers).

Idempotent: rewrites the four files. Usage: python3 -I scripts/build_faq.py
"""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://maregastro.com"
MAPS = "https://maps.google.com/?cid=7177941338358519695"
WA = "https://wa.me/905323540888"
UPDATED = "2026-11-07"
PATHS = {"tr": "/sss.html", "en": "/en/faq.html", "ar": "/ar/faq.html", "ru": "/ru/faq.html"}
HOME = {"tr": "/tr/", "en": "/en/", "ar": "/ar/", "ru": "/ru/"}
BLOG = {"tr": "/blog/", "en": "/en/blog/", "ar": "/ar/blog/", "ru": "/ru/blog/"}


def a(href, txt):
    return '<a href="%s">%s</a>' % (href, txt)


def bp(lang, slug):
    return "%s%s.html" % (BLOG[lang], slug)


T = {
 "tr": dict(
  title="Sık Sorulan Sorular | Mare Gastro Sapanca",
  desc="Mare Gastro hakkında resmi bilgiler: adres, çalışma saatleri, rezervasyon, menü, çocuk menüsü, vejetaryen seçenekler, otopark, konaklama ve özel günler.",
  h1="Sık Sorulan <em>Sorular</em>", lead="Mare Gastro hakkında en çok sorulanların resmi ve güncel cevapları.",
  updated="Son güncelleme: 7 Kasım 2026", rez="Rezervasyon Yap", wa="WhatsApp ile Yaz", back="Ana sayfa", crumb="Sık Sorulan Sorular",
  qa=[
   ("Mare Gastro nerede?", "Mare Gastro, Sapanca'da Didi Otel'in bahçesinde, Sapanca Gölü'nün hemen yanında. Adres: Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, 54600 Sapanca/Sakarya. " + a(MAPS, "Google Haritalar'da aç") + "."),
   ("Çalışma saatleri nedir?", "Salı'dan Pazar'a 09:00–00:00 arası açığız. Pazartesi kapalıyız."),
   ("Nasıl rezervasyon yapabilirim?", "Sitedeki " + a(HOME["tr"] + "#reservation", "rezervasyon formundan") + " üç adımda tarih, saat ve kişi sayısını seçip WhatsApp üzerinden onaylayabilirsiniz. Telefon ve WhatsApp: " + a("tel:+905323540888", "+90 532 354 08 88") + "."),
   ("Nasıl bir mutfağınız var?", "Yönetici Şef Doğan Anapa'nın imzasıyla, deniz ürünleri ağırlıklı Ege ve Akdeniz mutfağı sunuyoruz. Menüde başlangıçlar, salatalar, ara sıcaklar, ana yemekler, kahvaltılar, tatlılar ve atıştırmalıklar bulunur."),
   ("Menüyü ve fiyatları nereden görebilirim?", "Güncel menü ve fiyatlar " + a("/qr/", "dijital menümüzde") + " ve " + a(HOME["tr"] + "#menu", "sitemizin menü bölümünde") + " yer alır."),
   ("Çocuk menüsü var mı?", "Evet. Menümüzde çocuklar için ayrı bir Çocuk Menüsü bölümü bulunur."),
   ("Vejetaryen seçenekleriniz var mı?", "Evet. Humus, zeytinyağlı enginar, patlıcan biber kızartması ve mevsim salataları gibi et içermeyen tabaklarımız var. Vegan veya glutensiz taleplerinizi rezervasyon sırasında iletirseniz mutfağımız buna göre hazırlanır."),
   ("Alkollü içecek servisi var mı?", "Evet. Şaraplar, şampanyalar, rakılar, alkollü ve alkolsüz kokteyller, biralar ve sıcak-soğuk içecekler menümüzde yer alır."),
   ("Otopark var mı?", "Evet. Otoparkımız ücretsizdir ve vale hizmeti vardır."),
   ("Konaklama yapabilir miyim?", "Mare Gastro, Didi Otel'in bünyesindedir. Rezervasyon formunda konaklama isteğinizi belirtebilir, Didi Otel'de gölün hemen yanında bir gece geçirebilirsiniz. " + a("https://sapancadidiotel.com/", "Didi Otel")),
   ("Açık alanınız var mı?", "Evet. Hem açık hem kapalı oturma alanımız var; bahçede açık havada yemek yiyebilirsiniz."),
   ("Canlı müzik oluyor mu?", "Hafta sonu akşamlarında canlı müzik atmosfere eşlik ediyor. Özel etkinlikler rezervasyon bölümündeki takvimde görünür."),
   ("Doğum günü, yıldönümü veya evlilik teklifi için uygun mu?", "Evet. Özel gün kutlamaları için rezervasyon sırasında notunuzu iletin, ekibimiz hazırlığı sizinle planlasın. Fikir almak için: " + a(bp("tr", "sapanca-en-iyi-dogum-gunu-mekanlari"), "doğum günü") + ", " + a(bp("tr", "sapanca-yildonumu-icin-en-iyi-mekan"), "yıldönümü") + ", " + a(bp("tr", "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari"), "evlilik teklifi") + "."),
   ("İstanbul'dan ne kadar sürede gelinir?", "Sapanca, İstanbul'a yaklaşık 1,5 saat mesafededir. Ayrıntılı yol tarifi için " + a(bp("tr", "sapancaya-nasil-gidilir"), "Sapanca'ya nasıl gidilir") + " yazımıza bakabilirsiniz."),
   ("Şefiniz kim?", "Yönetici Şefimiz Doğan Anapa; Gourmand 2023 Türkiye temsilcisi. Sinema geçmişinden gelen anlatı odaklı bir bakışla mevsimsel bir mutfak yürütüyor. " + a(bp("tr", "sef-dogan-anapa-kimdir"), "Şef Doğan Anapa kimdir?")),
   ("Misafir yorumlarınız nasıl?", "Google Haritalar'da 4,9 puanımız var (Ekim 2026). Gerçek misafir yorumlarından bir seçkiyi " + a(bp("tr", "mare-gastro-google-yorumlari"), "Google yorumları") + " yazımızda okuyabilirsiniz."),
  ]),
 "en": dict(
  title="Frequently Asked Questions | Mare Gastro Sapanca",
  desc="Official answers about Mare Gastro: location, opening hours, reservations, menu, kids' menu, vegetarian options, parking, staying at Didi Otel and special occasions.",
  h1="Frequently Asked <em>Questions</em>", lead="Official, up-to-date answers to the questions we hear most about Mare Gastro.",
  updated="Last updated: 7 November 2026", rez="Book a Table", wa="Message on WhatsApp", back="Home", crumb="FAQ",
  qa=[
   ("Where is Mare Gastro?", "Mare Gastro is in the garden of Didi Otel in Sapanca, right by Lake Sapanca. Address: Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, 54600 Sapanca/Sakarya, Türkiye. " + a(MAPS, "Open in Google Maps") + "."),
   ("What are your opening hours?", "We are open Tuesday to Sunday, 09:00–00:00. We are closed on Mondays."),
   ("How do I make a reservation?", "Use the three-step " + a(HOME["en"] + "#reservation", "reservation form") + " to choose your date, time and party size, then confirm via WhatsApp. Phone and WhatsApp: " + a("tel:+905323540888", "+90 532 354 08 88") + "."),
   ("What kind of cuisine do you serve?", "Seafood-focused Aegean and Mediterranean cuisine by Executive Chef Doğan Anapa. The menu has starters, salads, hot appetisers, main courses, breakfast plates, desserts and snacks."),
   ("Where can I see the menu and prices?", "The current menu and prices are in our " + a("/qr/en/", "digital menu") + " and in the " + a(HOME["en"] + "#menu", "menu section") + " of our website."),
   ("Do you have a kids' menu?", "Yes. Our menu has a separate Kids' Menu section."),
   ("Do you have vegetarian options?", "Yes. Meat-free dishes include hummus, artichoke in olive oil, fried aubergine and peppers in tomato sauce and seasonal salads. Let us know about vegan or gluten-free needs when you book and the kitchen will prepare accordingly."),
   ("Do you serve alcohol?", "Yes. Wines, champagnes, rakı, cocktails (with and without alcohol), beers and hot and cold drinks are on the menu."),
   ("Is there parking?", "Yes. Parking is free and valet service is available."),
   ("Can I stay overnight?", "Mare Gastro is part of Didi Otel. You can mention that you would like to stay when you book and spend a night by the lake at " + a("https://sapancadidiotel.com/", "Didi Otel") + "."),
   ("Do you have outdoor seating?", "Yes. We have both indoor and outdoor seating, including tables in the garden."),
   ("Is there live music?", "Live music accompanies weekend evenings. Special events are shown in the calendar of the reservation section."),
   ("Can I celebrate a birthday, anniversary or proposal?", "Yes. Add a note when you book and our team will plan it with you. Ideas: " + a(bp("en", "sapanca-en-iyi-dogum-gunu-mekanlari"), "birthdays") + ", " + a(bp("en", "sapanca-yildonumu-icin-en-iyi-mekan"), "anniversaries") + ", " + a(bp("en", "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari"), "proposals") + "."),
   ("How far is it from Istanbul?", "Sapanca is about 1.5 hours from Istanbul by car. See our " + a(bp("en", "sapancaya-nasil-gidilir"), "directions guide") + "."),
   ("Who is your chef?", "Our Executive Chef is Doğan Anapa, Gourmand 2023 Türkiye representative, who runs a seasonal kitchen with a storyteller's eye shaped by his background in film. " + a(bp("en", "sef-dogan-anapa-kimdir"), "Who is Chef Doğan Anapa?")),
   ("What do guests say?", "We are rated 4.9 on Google Maps (October 2026)."),
  ]),
 "ar": dict(
  title="الأسئلة الشائعة | Mare Gastro سابانجا",
  desc="إجابات رسمية عن Mare Gastro: الموقع، ساعات العمل، الحجز، القائمة، قائمة الأطفال، الخيارات النباتية، مواقف السيارات، الإقامة في Didi Otel والمناسبات الخاصة.",
  h1="الأسئلة <em>الشائعة</em>", lead="إجابات رسمية ومحدّثة لأكثر الأسئلة شيوعاً عن Mare Gastro.",
  updated="آخر تحديث: 7 نوفمبر 2026", rez="احجز طاولة", wa="راسلنا على واتساب", back="الرئيسية", crumb="الأسئلة الشائعة",
  qa=[
   ("أين يقع Mare Gastro؟", "يقع Mare Gastro في حديقة فندق Didi Otel في سابانجا، بجوار بحيرة سابانجا مباشرة. العنوان: Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, 54600 Sapanca/Sakarya، تركيا. " + a(MAPS, "افتح في خرائط Google") + "."),
   ("ما هي ساعات العمل؟", "نفتح من الثلاثاء إلى الأحد من 09:00 حتى 00:00. نغلق يوم الاثنين."),
   ("كيف أحجز طاولة؟", "استخدم " + a(HOME["ar"] + "#reservation", "نموذج الحجز") + " المكوّن من ثلاث خطوات لاختيار التاريخ والوقت وعدد الأشخاص، ثم أكّد عبر واتساب. الهاتف وواتساب: " + a("tel:+905323540888", "‎+90 532 354 08 88") + "."),
   ("ما نوع المطبخ لديكم؟", "مطبخ بحر إيجه والبحر المتوسط مع تركيز على المأكولات البحرية بتوقيع الشيف التنفيذي دوغان أنابا. تضم القائمة المقبلات والسلطات والمقبلات الساخنة والأطباق الرئيسية وأطباق الفطور والحلويات والوجبات الخفيفة."),
   ("أين أجد القائمة والأسعار؟", "القائمة والأسعار المحدّثة موجودة في " + a("/qr/?lang=ar", "القائمة الرقمية") + " وفي " + a(HOME["ar"] + "#menu", "قسم القائمة") + " على موقعنا."),
   ("هل لديكم قائمة للأطفال؟", "نعم. تضم قائمتنا قسماً خاصاً بالأطفال."),
   ("هل لديكم خيارات نباتية؟", "نعم. من الأطباق الخالية من اللحوم: الحمص، الخرشوف بزيت الزيتون، الباذنجان والفلفل المقلي بصلصة الطماطم والسلطات الموسمية. أخبرونا عند الحجز بطلبات الطعام النباتي الصرف أو الخالي من الغلوتين ليحضّر المطبخ وفقاً لذلك."),
   ("هل تقدّمون المشروبات الكحولية؟", "نعم. تضم القائمة النبيذ والشمبانيا والعرق والكوكتيلات (الكحولية وغير الكحولية) والبيرة والمشروبات الساخنة والباردة."),
   ("هل يوجد موقف للسيارات؟", "نعم. موقف السيارات مجاني وتتوفر خدمة صفّ السيارات."),
   ("هل يمكنني الإقامة؟", "Mare Gastro جزء من فندق Didi Otel. يمكنكم ذكر رغبتكم في الإقامة عند الحجز وقضاء ليلة بجوار البحيرة في " + a("https://sapancadidiotel.com/", "Didi Otel") + "."),
   ("هل توجد جلسات في الهواء الطلق؟", "نعم. لدينا جلسات داخلية وخارجية، بما في ذلك طاولات في الحديقة."),
   ("هل توجد موسيقى حية؟", "ترافق الموسيقى الحية أمسيات عطلة نهاية الأسبوع. تظهر الفعاليات الخاصة في تقويم قسم الحجز."),
   ("هل يمكنني الاحتفال بعيد ميلاد أو ذكرى زواج أو طلب زواج؟", "نعم. أضيفوا ملاحظة عند الحجز وسيخطط فريقنا للمناسبة معكم. أفكار: " + a(bp("ar", "sapanca-en-iyi-dogum-gunu-mekanlari"), "أعياد الميلاد") + "، " + a(bp("ar", "sapanca-yildonumu-icin-en-iyi-mekan"), "ذكرى الزواج") + "، " + a(bp("ar", "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari"), "طلب الزواج") + "."),
   ("كم تبعد عن إسطنبول؟", "تبعد سابانجا نحو ساعة ونصف بالسيارة عن إسطنبول. راجعوا " + a(bp("ar", "sapancaya-nasil-gidilir"), "دليل الوصول") + "."),
   ("من هو الشيف؟", "الشيف التنفيذي دوغان أنابا، ممثل تركيا في جوائز Gourmand لعام 2023، يدير مطبخاً موسمياً بنظرة قصصية مستمدة من خلفيته السينمائية. " + a(bp("ar", "sef-dogan-anapa-kimdir"), "من هو الشيف دوغان أنابا؟")),
   ("ماذا يقول الضيوف؟", "تقييمنا 4.9 على خرائط Google (أكتوبر 2026)."),
  ]),
 "ru": dict(
  title="Частые вопросы | Mare Gastro, Сапанджа",
  desc="Официальные ответы о Mare Gastro: адрес, часы работы, бронирование, меню, детское меню, вегетарианские блюда, парковка, проживание в Didi Otel и праздники.",
  h1="Частые <em>вопросы</em>", lead="Официальные и актуальные ответы на самые частые вопросы о Mare Gastro.",
  updated="Обновлено: 7 ноября 2026", rez="Забронировать", wa="Написать в WhatsApp", back="Главная", crumb="Частые вопросы",
  qa=[
   ("Где находится Mare Gastro?", "Mare Gastro находится в саду отеля Didi Otel в Сапандже, прямо у озера Сапанджа. Адрес: Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, 54600 Sapanca/Sakarya, Турция. " + a(MAPS, "Открыть в Google Картах") + "."),
   ("Какие часы работы?", "Мы открыты со вторника по воскресенье с 09:00 до 00:00. В понедельник закрыто."),
   ("Как забронировать столик?", "Воспользуйтесь " + a(HOME["ru"] + "#reservation", "формой бронирования") + " из трёх шагов: выберите дату, время и число гостей и подтвердите через WhatsApp. Телефон и WhatsApp: " + a("tel:+905323540888", "+90 532 354 08 88") + "."),
   ("Какая у вас кухня?", "Эгейская и средиземноморская кухня с акцентом на морепродукты от шеф-повара Догана Анапы. В меню закуски, салаты, горячие закуски, основные блюда, завтраки, десерты и снеки."),
   ("Где посмотреть меню и цены?", "Актуальное меню и цены — в нашем " + a("/qr/?lang=ru", "цифровом меню") + " и в " + a(HOME["ru"] + "#menu", "разделе меню") + " на сайте."),
   ("Есть ли детское меню?", "Да. В меню есть отдельный раздел для детей."),
   ("Есть ли вегетарианские блюда?", "Да. Блюда без мяса: хумус, артишок в оливковом масле, жареные баклажаны и перец в томатном соусе, сезонные салаты. Сообщите о веганских или безглютеновых пожеланиях при бронировании, и кухня всё подготовит."),
   ("Подаёте ли вы алкоголь?", "Да. В меню вина, шампанское, ракы, коктейли (алкогольные и безалкогольные), пиво, горячие и холодные напитки."),
   ("Есть ли парковка?", "Да. Парковка бесплатная, работает валет-сервис."),
   ("Можно ли остановиться на ночь?", "Mare Gastro находится в отеле Didi Otel. При бронировании укажите, что хотите остаться, и проведите ночь у озера в " + a("https://sapancadidiotel.com/", "Didi Otel") + "."),
   ("Есть ли места на открытом воздухе?", "Да. Есть и зал, и открытая терраса со столиками в саду."),
   ("Бывает ли живая музыка?", "Живая музыка звучит по вечерам в выходные. Специальные события отмечены в календаре раздела бронирования."),
   ("Можно ли отметить день рождения, годовщину или сделать предложение?", "Да. Оставьте комментарий при бронировании, и наша команда всё спланирует вместе с вами. Идеи: " + a(bp("ru", "sapanca-en-iyi-dogum-gunu-mekanlari"), "день рождения") + ", " + a(bp("ru", "sapanca-yildonumu-icin-en-iyi-mekan"), "годовщина") + ", " + a(bp("ru", "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari"), "предложение руки") + "."),
   ("Сколько ехать из Стамбула?", "Сапанджа примерно в 1,5 часах езды от Стамбула. Подробнее — в нашем " + a(bp("ru", "sapancaya-nasil-gidilir"), "маршруте") + "."),
   ("Кто ваш шеф?", "Шеф-повар Доган Анапа — представитель Турции на Gourmand 2023; он ведёт сезонную кухню с повествовательным взглядом, сформированным опытом в кино. " + a(bp("ru", "sef-dogan-anapa-kimdir"), "Кто такой шеф Доган Анапа?")),
   ("Что говорят гости?", "Наш рейтинг в Google Картах — 4,9 (октябрь 2026)."),
  ]),
}

GTM_HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TVJ7R3TT');</script>
<!-- End Google Tag Manager -->"""
GTM_BODY = """<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TVJ7R3TT" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>"""

CSS = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#FBF8F2;--sand:#F3EDE2;--ink:#10202E;--ink2:#2A3A48;--muted:rgba(16,32,46,.64);--amber:#9C7437;--line:rgba(16,32,46,.1);
--sf:-apple-system,BlinkMacSystemFont,'SF Pro Display','SF Pro Text','Helvetica Neue',Inter,Arial,sans-serif}
html{background:var(--bg)}body{font-family:var(--sf);color:var(--ink);background:var(--bg);line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:var(--amber)}
.top{position:sticky;top:0;z-index:5;background:rgba(251,248,242,.88);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-bottom:1px solid var(--line)}
.top-in{max-width:880px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.top img{height:28px;filter:brightness(0);opacity:.86;display:block}
.btn{display:inline-flex;align-items:center;justify-content:center;height:44px;padding:0 20px;border-radius:999px;font-size:14px;font-weight:600;text-decoration:none;white-space:nowrap}
.btn-p{background:var(--ink);color:#fff}.btn-s{background:#fff;color:var(--ink);border:1px solid rgba(16,32,46,.18)}
main{max-width:880px;margin:0 auto;padding:40px 20px 80px}
.crumb{font-size:12.5px;color:var(--muted);margin-bottom:18px}.crumb a{color:var(--muted)}
h1{font-size:clamp(2rem,5vw,3rem);font-weight:600;letter-spacing:-.03em;line-height:1.06;margin-bottom:12px}
h1 em{font-style:normal;color:var(--amber)}
.lead{font-size:17px;color:var(--ink2);margin-bottom:6px}.upd{font-size:12.5px;color:var(--muted);margin-bottom:28px}
.qa{background:#fff;border:1px solid rgba(16,32,46,.06);border-radius:18px;padding:20px 22px;margin-bottom:12px;box-shadow:0 1px 2px rgba(16,32,46,.04),0 8px 22px -14px rgba(16,32,46,.18)}
.qa h2{font-size:17px;font-weight:600;letter-spacing:-.015em;margin-bottom:6px}
.qa p{font-size:15px;color:var(--ink2)}
.cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px}
footer{border-top:1px solid var(--line);background:var(--sand);padding:28px 20px;text-align:center;font-size:12.5px;color:var(--muted)}
footer a{color:var(--ink2);margin:0 8px;text-decoration:none;font-weight:600}
@media(max-width:560px){.top-in .btn-s{display:none}.qa{padding:16px 16px}}"""


def page(lang):
    t = T[lang]
    rtl = ' dir="rtl"' if lang == "ar" else ""
    url = SITE + PATHS[lang]
    alts = "".join('<link rel="alternate" hreflang="%s" href="%s%s">\n' % (l, SITE, p) for l, p in PATHS.items())
    alts += '<link rel="alternate" hreflang="x-default" href="%s%s">\n' % (SITE, PATHS["tr"])
    strip = lambda s: html.unescape(__import__("re").sub(r"<[^>]+>", "", s))
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "FAQPage", "@id": url + "#faq", "url": url, "inLanguage": lang, "dateModified": UPDATED,
         "about": {"@type": "Restaurant", "name": "Mare Gastro", "url": SITE + HOME[lang]},
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(ans)}} for q, ans in t["qa"]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Mare Gastro", "item": SITE + HOME[lang]},
            {"@type": "ListItem", "position": 2, "name": t["crumb"], "item": url}]},
    ]}
    qa = "".join('<section class="qa"><h2>%s</h2><p>%s</p></section>\n' % (html.escape(q), ans) for q, ans in t["qa"])
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
<meta property="og:image" content="{SITE}/images/og-mare-mekan.jpg">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
{GTM_BODY}
<header class="top"><div class="top-in"><a href="{HOME[lang]}" aria-label="Mare Gastro"><img src="/images/marelogo1.png" alt="Mare Gastro"></a>
<div style="display:flex;gap:8px"><a class="btn btn-s" href="{WA}" target="_blank" rel="noopener">{t['wa']}</a><a class="btn btn-p" href="{HOME[lang]}#reservation">{t['rez']}</a></div></div></header>
<main>
<nav class="crumb"><a href="{HOME[lang]}">{t['back']}</a> · {t['crumb']}</nav>
<h1>{t['h1']}</h1>
<p class="lead">{t['lead']}</p>
<p class="upd">{t['updated']}</p>
{qa}<div class="cta"><a class="btn btn-p" href="{HOME[lang]}#reservation">{t['rez']}</a><a class="btn btn-s" href="{WA}" target="_blank" rel="noopener">{t['wa']}</a></div>
</main>
<footer>© 2026 Mare Gastro · Didi Otel · Sapanca<br><a href="{HOME[lang]}#menu">Menu</a><a href="{BLOG[lang]}">Blog</a><a href="https://www.instagram.com/maregastro/" target="_blank" rel="noopener">Instagram</a></footer>
</body>
</html>
"""


def main():
    for lang, p in PATHS.items():
        out = os.path.join(ROOT, p.lstrip("/"))
        with open(out, "w", encoding="utf-8") as f:
            f.write(page(lang))
        print("wrote", p)


if __name__ == "__main__":
    main()
