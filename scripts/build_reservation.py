#!/usr/bin/env python3
"""Mare Gastro — reservation landing pages (TR /rezervasyon.html, EN/AR/RU /{lang}/reservation.html).

Purpose: a crawlable, answer-first page for "Mare Gastro rezervasyon / Sapanca restoran rezervasyon"
queries (Google + AI assistants). The booking itself still happens in the 3-step form on the home
page (/{lang}/#reservation) or on WhatsApp — this page links there, it does not duplicate the form.

Facts used (all verified on the live site, 2026-11-12):
- form steps: Tarih → Bilgiler (saat, kişi, ad, telefon, e-posta, konaklama) → Onay (WhatsApp)
- time slots 09:00–00:00 every 30 min; open Tue–Sun 09:00–00:00, Monday closed
- 10+ guests = private organisation; stay option at Didi Otel; free parking + valet
- phone / WhatsApp +90 532 354 08 88, info@maregastro.com, address in Kırkpınar Soğuksu
NOT stated: deposits, cancellation fees, price figures, minimum spend, dress code.

Idempotent. Usage: python3 -I scripts/build_reservation.py
"""
import html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_faq import CSS, GTM_HEAD, GTM_BODY, SITE, MAPS, WA  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = "2026-11-12"
PATHS = {"tr": "/rezervasyon.html", "en": "/en/reservation.html", "ar": "/ar/reservation.html", "ru": "/ru/reservation.html"}
HOME = {"tr": "/tr/", "en": "/en/", "ar": "/ar/", "ru": "/ru/"}
FORM = {l: h + "#reservation" for l, h in HOME.items()}
MENU = {"tr": "/menu/", "en": "/menu/en/", "ar": "/menu/ar/", "ru": "/menu/ru/"}
FAQ = {"tr": "/sss.html", "en": "/en/faq.html", "ar": "/ar/faq.html", "ru": "/ru/faq.html"}
BLOG = {"tr": "/blog/", "en": "/en/blog/", "ar": "/ar/blog/", "ru": "/ru/blog/"}
TEL = "tel:+905323540888"
PHONE = "+90 532 354 08 88"
MAIL = "info@maregastro.com"
ADDR = "Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, 54600 Sapanca/Sakarya"


def a(href, txt, ext=False):
    return '<a href="%s"%s>%s</a>' % (href, ' target="_blank" rel="noopener"' if ext else "", txt)


def bp(lang, slug):
    return "%s%s.html" % (BLOG[lang], slug)


T = {
 "tr": dict(
  title="Mare Gastro Rezervasyon | Sapanca Restoran Masa Ayırtma",
  desc="Mare Gastro'da masa ayırtın: 3 adımlı form, WhatsApp veya telefon (+90 532 354 08 88). Salı–Pazar 09:00–00:00. Özel gün, grup ve konaklama seçenekleri.",
  h1="Mare Gastro'da <em>Rezervasyon</em>",
  lead="Mare Gastro'da masanızı sitedeki üç adımlı formdan, WhatsApp'tan ya da telefonla ayırtabilirsiniz. Salı'dan Pazar'a 09:00–00:00 arası açığız, Pazartesi kapalıyız. Talebiniz WhatsApp üzerinden onaylanır.",
  updated="Son güncelleme: 12 Kasım 2026", back="Ana sayfa", crumb="Rezervasyon",
  form="Rezervasyon Formunu Aç", wa="WhatsApp ile Yaz", call="Ara",
  steps_h="Rezervasyon Nasıl Yapılır?",
  steps=[("Tarih", "Takvimden gelmek istediğiniz günü seçin. Kapalı günler takvimde görünür."),
         ("Bilgiler", "Saati (09:00–00:00, yarım saat aralıklarla), kişi sayısını, adınızı, telefonunuzu ve konaklama tercihinizi girin."),
         ("Onay", "Bilgilerinizi kontrol edin ve WhatsApp ile gönderin. Ekibimiz rezervasyonunuzu WhatsApp üzerinden onaylar.")],
  facts_h="Kısa Bilgiler",
  facts=[("Çalışma saatleri", "Salı–Pazar 09:00–00:00 · Pazartesi kapalı"),
         ("Telefon ve WhatsApp", a(TEL, PHONE)),
         ("E-posta", a("mailto:" + MAIL, MAIL)),
         ("Adres", ADDR + " · " + a(MAPS, "Yol tarifi", True)),
         ("Otopark", "Ücretsiz otopark ve vale hizmeti"),
         ("Menü", a(MENU["tr"], "Güncel menü ve fiyatlar"))],
  qa=[
   ("Mare Gastro'da nasıl rezervasyon yapılır?", "En hızlı yol sitedeki " + a(FORM["tr"], "rezervasyon formu") + ": tarih, saat ve kişi sayısını seçip WhatsApp ile gönderirsiniz, ekibimiz WhatsApp'tan onaylar. Dilerseniz doğrudan " + a(WA, "WhatsApp'tan yazabilir", True) + " ya da " + a(TEL, PHONE) + " numarasını arayabilirsiniz."),
   ("Hangi gün ve saatler için rezervasyon yapabilirim?", "Salı'dan Pazar'a 09:00 ile 00:00 arasında, yarım saatlik aralıklarla rezervasyon alıyoruz. Pazartesi kapalıyız. Kahvaltı, öğle ve akşam yemeği için aynı form kullanılır."),
   ("Kalabalık grup veya özel organizasyon için ne yapmalıyım?", "Formda 10 ve üzeri kişi seçtiğinizde talebiniz özel organizasyon olarak değerlendirilir. Detayları WhatsApp'tan konuşup planlıyoruz. Fikir için: " + a(bp("tr", "sapanca-toplu-organizasyon-grup-yemegi"), "grup yemekleri") + " ve " + a(bp("tr", "sapanca-is-yemegi-kurumsal-davet"), "kurumsal davetler") + "."),
   ("Doğum günü, yıl dönümü veya evlilik teklifi için nasıl hazırlık yapılır?", "Rezervasyon sırasında ya da WhatsApp'tan kutlamanızı anlatın; masa düzeni, pasta ve menü gibi detayları sizinle birlikte planlıyoruz. Örnekler: " + a(bp("tr", "sapanca-dogum-gunu-nerede-kutlanir"), "doğum günü") + ", " + a(bp("tr", "sapanca-yildonumu-icin-en-iyi-mekan"), "yıl dönümü") + ", " + a(bp("tr", "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari"), "evlilik teklifi") + ", " + a(bp("tr", "sapanca-nisan-yemegi"), "nişan yemeği") + "."),
   ("Konaklamayı da aynı rezervasyonla ayarlayabilir miyim?", "Evet. Formdaki konaklama adımında \"Konaklamak istiyorum\" seçeneğini işaretlerseniz Didi Otel'de gölün hemen yanında konaklama talebiniz de iletilir. " + a("https://sapancadidiotel.com/", "Didi Otel", True)),
   ("Rezervasyonum ne zaman onaylanır?", "Form WhatsApp'a gönderildikten sonra ekibimiz en kısa sürede WhatsApp üzerinden dönüş yapar ve rezervasyonu onaylar."),
   ("Mare Gastro'ya nasıl gelinir, otopark var mı?", "Mare Gastro, Sapanca'da Didi Otel'in bahçesinde, Sapanca Gölü'nün hemen yanında. İstanbul'dan yaklaşık 1,5 saat. Otopark ücretsiz, vale hizmeti var. " + a(bp("tr", "sapancaya-nasil-gidilir"), "Sapanca'ya nasıl gidilir?")),
   ("Menüyü rezervasyondan önce görebilir miyim?", "Evet. Güncel menü ve fiyatlar " + a(MENU["tr"], "dijital menümüzde") + " yer alır. Diğer sorular için " + a(FAQ["tr"], "Sık Sorulan Sorular") + " sayfamıza bakabilirsiniz."),
  ]),
 "en": dict(
  title="Mare Gastro Reservations | Book a Table in Sapanca",
  desc="Book a table at Mare Gastro in Sapanca: 3-step online form, WhatsApp or phone (+90 532 354 08 88). Open Tue–Sun 09:00–00:00. Celebrations, groups and stays.",
  h1="Reservations at <em>Mare Gastro</em>",
  lead="Book your table at Mare Gastro with the three-step form on our website, on WhatsApp or by phone. We are open Tuesday to Sunday, 09:00–00:00, and closed on Mondays. Every request is confirmed on WhatsApp.",
  updated="Last updated: 12 November 2026", back="Home", crumb="Reservations",
  form="Open the Booking Form", wa="Message on WhatsApp", call="Call",
  steps_h="How to Book",
  steps=[("Date", "Pick the day you would like to come. Closed days are shown in the calendar."),
         ("Details", "Choose a time (09:00–00:00, every half hour), party size, your name, phone and whether you would like to stay overnight."),
         ("Confirm", "Check your details and send them on WhatsApp. Our team confirms your booking on WhatsApp.")],
  facts_h="At a Glance",
  facts=[("Opening hours", "Tue–Sun 09:00–00:00 · Closed on Mondays"),
         ("Phone & WhatsApp", a(TEL, PHONE)),
         ("Email", a("mailto:" + MAIL, MAIL)),
         ("Address", ADDR + ", Türkiye · " + a(MAPS, "Directions", True)),
         ("Parking", "Free parking and valet service"),
         ("Menu", a(MENU["en"], "Current menu and prices"))],
  qa=[
   ("How do I book a table at Mare Gastro?", "The quickest way is the " + a(FORM["en"], "booking form") + " on our website: choose the date, time and party size, send it on WhatsApp and our team confirms there. You can also " + a(WA, "message us on WhatsApp", True) + " directly or call " + a(TEL, PHONE) + "."),
   ("Which days and times can I book?", "We take bookings Tuesday to Sunday between 09:00 and 00:00, every half hour. We are closed on Mondays. Breakfast, lunch and dinner all use the same form."),
   ("What about large groups or private events?", "Selecting 10 or more guests in the form marks your request as a private organisation, and we plan the details with you on WhatsApp. Ideas: " + a(bp("en", "sapanca-toplu-organizasyon-grup-yemegi"), "group dinners") + " and " + a(bp("en", "sapanca-is-yemegi-kurumsal-davet"), "corporate dinners") + "."),
   ("Can you help with a birthday, anniversary or proposal?", "Yes. Tell us about the occasion when you book or on WhatsApp and we will plan the table setting, cake and menu with you. Ideas: " + a(bp("en", "sapanca-dogum-gunu-nerede-kutlanir"), "birthdays") + ", " + a(bp("en", "sapanca-yildonumu-icin-en-iyi-mekan"), "anniversaries") + ", " + a(bp("en", "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari"), "proposals") + ", " + a(bp("en", "sapanca-nisan-yemegi"), "engagement dinners") + "."),
   ("Can I arrange an overnight stay with the same booking?", "Yes. Choose \"I would like to stay\" in the form and your request for a room at Didi Otel, right by the lake, is passed on too. " + a("https://sapancadidiotel.com/", "Didi Otel", True)),
   ("When is my booking confirmed?", "Once the form is sent on WhatsApp, our team replies there as soon as possible and confirms your table."),
   ("How do I get there, and is there parking?", "Mare Gastro is in the garden of Didi Otel in Sapanca, right next to Lake Sapanca, about 1.5 hours from Istanbul. Parking is free and valet service is available. " + a(bp("en", "sapancaya-nasil-gidilir"), "How to get to Sapanca")),
   ("Can I see the menu before booking?", "Yes. The current menu and prices are in our " + a(MENU["en"], "digital menu") + ". For other questions see our " + a(FAQ["en"], "FAQ") + "."),
  ]),
 "ar": dict(
  title="حجز طاولة في Mare Gastro | مطعم في سابانجا",
  desc="احجز طاولتك في Mare Gastro في سابانجا: نموذج من 3 خطوات أو واتساب أو هاتف (+90 532 354 08 88). من الثلاثاء إلى الأحد 09:00–00:00. مناسبات ومجموعات وإقامة.",
  h1="الحجز في <em>Mare Gastro</em>",
  lead="يمكنك حجز طاولتك في Mare Gastro عبر النموذج المكوّن من ثلاث خطوات على موقعنا أو عبر واتساب أو بالهاتف. نفتح من الثلاثاء إلى الأحد من 09:00 حتى 00:00، ونغلق يوم الاثنين. يتم تأكيد كل طلب عبر واتساب.",
  updated="آخر تحديث: 12 نوفمبر 2026", back="الرئيسية", crumb="الحجز",
  form="افتح نموذج الحجز", wa="راسلنا على واتساب", call="اتصل",
  steps_h="كيف تحجز؟",
  steps=[("التاريخ", "اختر اليوم الذي تريد الحضور فيه. تظهر أيام الإغلاق في التقويم."),
         ("التفاصيل", "اختر الوقت (09:00–00:00 كل نصف ساعة) وعدد الأشخاص واسمك وهاتفك وما إذا كنت ترغب في الإقامة."),
         ("التأكيد", "راجع بياناتك وأرسلها عبر واتساب. يؤكد فريقنا حجزك عبر واتساب.")],
  facts_h="معلومات سريعة",
  facts=[("ساعات العمل", "الثلاثاء–الأحد 09:00–00:00 · مغلق يوم الاثنين"),
         ("الهاتف وواتساب", '<span dir="ltr">' + a(TEL, PHONE) + "</span>"),
         ("البريد الإلكتروني", a("mailto:" + MAIL, MAIL)),
         ("العنوان", '<span dir="ltr">' + ADDR + "</span> · " + a(MAPS, "الاتجاهات", True)),
         ("موقف السيارات", "موقف مجاني وخدمة صف السيارات"),
         ("القائمة", a(MENU["ar"], "القائمة والأسعار الحالية"))],
  qa=[
   ("كيف أحجز طاولة في Mare Gastro؟", "أسرع طريقة هي " + a(FORM["ar"], "نموذج الحجز") + " على موقعنا: اختر التاريخ والوقت وعدد الأشخاص وأرسله عبر واتساب، ويؤكد فريقنا الحجز هناك. يمكنك أيضًا " + a(WA, "مراسلتنا على واتساب", True) + " مباشرة أو الاتصال على " + '<span dir="ltr">' + a(TEL, PHONE) + "</span>."),
   ("ما الأيام والأوقات المتاحة للحجز؟", "نستقبل الحجوزات من الثلاثاء إلى الأحد بين 09:00 و00:00 كل نصف ساعة. نغلق يوم الاثنين. يُستخدم النموذج نفسه للإفطار والغداء والعشاء."),
   ("ماذا عن المجموعات الكبيرة أو المناسبات الخاصة؟", "عند اختيار 10 أشخاص أو أكثر في النموذج يُعامل طلبك كتنظيم خاص، ونخطط التفاصيل معك عبر واتساب. أفكار: " + a(bp("ar", "sapanca-toplu-organizasyon-grup-yemegi"), "عشاء المجموعات") + " و" + a(bp("ar", "sapanca-is-yemegi-kurumsal-davet"), "الدعوات المؤسسية") + "."),
   ("هل تساعدون في أعياد الميلاد وذكرى الزواج وطلب الزواج؟", "نعم. أخبرنا عن المناسبة عند الحجز أو عبر واتساب وسنخطط معك ترتيب الطاولة والكعكة والقائمة. أفكار: " + a(bp("ar", "sapanca-dogum-gunu-nerede-kutlanir"), "أعياد الميلاد") + "، " + a(bp("ar", "sapanca-yildonumu-icin-en-iyi-mekan"), "ذكرى الزواج") + "، " + a(bp("ar", "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari"), "طلب الزواج") + "، " + a(bp("ar", "sapanca-nisan-yemegi"), "عشاء الخطوبة") + "."),
   ("هل يمكنني ترتيب الإقامة مع الحجز نفسه؟", "نعم. اختر «أرغب في الإقامة» في النموذج وسيصلنا طلب إقامتك في فندق Didi Otel بجوار البحيرة مباشرة. " + a("https://sapancadidiotel.com/", "Didi Otel", True)),
   ("متى يتم تأكيد حجزي؟", "بعد إرسال النموذج عبر واتساب يرد فريقنا هناك في أقرب وقت ويؤكد طاولتك."),
   ("كيف أصل وهل يوجد موقف سيارات؟", "يقع Mare Gastro في حديقة فندق Didi Otel في سابانجا، بجوار بحيرة سابانجا مباشرة، على بعد نحو ساعة ونصف من إسطنبول. الموقف مجاني مع خدمة صف السيارات. " + a(bp("ar", "sapancaya-nasil-gidilir"), "كيف تصل إلى سابانجا")),
   ("هل يمكنني رؤية القائمة قبل الحجز؟", "نعم. القائمة والأسعار الحالية موجودة في " + a(MENU["ar"], "القائمة الرقمية") + ". لأسئلة أخرى راجع " + a(FAQ["ar"], "الأسئلة الشائعة") + "."),
  ]),
 "ru": dict(
  title="Бронирование Mare Gastro | Ресторан в Сапандже",
  desc="Забронируйте столик в Mare Gastro в Сапандже: форма из 3 шагов, WhatsApp или телефон (+90 532 354 08 88). Вт–Вс 09:00–00:00. Праздники, группы и проживание.",
  h1="Бронирование в <em>Mare Gastro</em>",
  lead="Забронировать столик в Mare Gastro можно через форму из трёх шагов на сайте, в WhatsApp или по телефону. Мы работаем со вторника по воскресенье с 09:00 до 00:00, в понедельник выходной. Каждая заявка подтверждается в WhatsApp.",
  updated="Обновлено: 12 ноября 2026", back="Главная", crumb="Бронирование",
  form="Открыть форму бронирования", wa="Написать в WhatsApp", call="Позвонить",
  steps_h="Как забронировать",
  steps=[("Дата", "Выберите день визита. Нерабочие дни отмечены в календаре."),
         ("Детали", "Укажите время (09:00–00:00, каждые полчаса), число гостей, имя, телефон и нужно ли проживание."),
         ("Подтверждение", "Проверьте данные и отправьте их в WhatsApp. Наша команда подтвердит бронирование в WhatsApp.")],
  facts_h="Коротко",
  facts=[("Часы работы", "Вт–Вс 09:00–00:00 · Пн выходной"),
         ("Телефон и WhatsApp", a(TEL, PHONE)),
         ("Эл. почта", a("mailto:" + MAIL, MAIL)),
         ("Адрес", ADDR + ", Турция · " + a(MAPS, "Маршрут", True)),
         ("Парковка", "Бесплатная парковка и услуги парковщика"),
         ("Меню", a(MENU["ru"], "Актуальное меню и цены"))],
  qa=[
   ("Как забронировать столик в Mare Gastro?", "Быстрее всего через " + a(FORM["ru"], "форму бронирования") + " на сайте: выберите дату, время и число гостей, отправьте в WhatsApp, и наша команда подтвердит бронь там же. Также можно " + a(WA, "написать нам в WhatsApp", True) + " или позвонить по номеру " + a(TEL, PHONE) + "."),
   ("На какие дни и время можно забронировать?", "Мы принимаем брони со вторника по воскресенье с 09:00 до 00:00, каждые полчаса. В понедельник выходной. Для завтрака, обеда и ужина используется одна и та же форма."),
   ("А если нас много или это частное мероприятие?", "Если в форме выбрать 10 и более гостей, заявка считается частным мероприятием, и мы обсуждаем детали с вами в WhatsApp. Идеи: " + a(bp("ru", "sapanca-toplu-organizasyon-grup-yemegi"), "групповые ужины") + " и " + a(bp("ru", "sapanca-is-yemegi-kurumsal-davet"), "корпоративные ужины") + "."),
   ("Поможете с днём рождения, годовщиной или предложением руки?", "Да. Расскажите о поводе при бронировании или в WhatsApp, и мы вместе спланируем сервировку, торт и меню. Идеи: " + a(bp("ru", "sapanca-dogum-gunu-nerede-kutlanir"), "день рождения") + ", " + a(bp("ru", "sapanca-yildonumu-icin-en-iyi-mekan"), "годовщина") + ", " + a(bp("ru", "sapanca-istanbula-yakin-evlilik-teklifi-mekanlari"), "предложение руки") + ", " + a(bp("ru", "sapanca-nisan-yemegi"), "ужин на помолвку") + "."),
   ("Можно ли сразу забронировать и проживание?", "Да. Выберите в форме «Хочу остановиться», и ваша заявка на номер в отеле Didi Otel прямо у озера тоже будет передана. " + a("https://sapancadidiotel.com/", "Didi Otel", True)),
   ("Когда подтверждается бронирование?", "После отправки формы в WhatsApp наша команда отвечает там как можно скорее и подтверждает столик."),
   ("Как добраться и есть ли парковка?", "Mare Gastro находится в саду отеля Didi Otel в Сапандже, прямо у озера Сапанджа, примерно в 1,5 часа от Стамбула. Парковка бесплатная, есть парковщик. " + a(bp("ru", "sapancaya-nasil-gidilir"), "Как добраться до Сапанджи")),
   ("Можно ли посмотреть меню до бронирования?", "Да. Актуальное меню и цены — в нашем " + a(MENU["ru"], "цифровом меню") + ". Другие вопросы — в разделе " + a(FAQ["ru"], "FAQ") + "."),
  ]),
}

EXTRA_CSS = """
.steps{display:grid;gap:12px;margin:8px 0 28px;counter-reset:s}
.step{background:#fff;border:1px solid rgba(16,32,46,.06);border-radius:18px;padding:18px 20px 18px 64px;position:relative;box-shadow:0 1px 2px rgba(16,32,46,.04),0 8px 22px -14px rgba(16,32,46,.18)}
.step::before{counter-increment:s;content:counter(s);position:absolute;left:20px;top:18px;width:30px;height:30px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font-size:14px;font-weight:600}
[dir=rtl] .step{padding:18px 64px 18px 20px}[dir=rtl] .step::before{left:auto;right:20px}
.step h3{font-size:16px;font-weight:600;margin-bottom:2px}.step p{font-size:15px;color:var(--ink2)}
h2.sec{font-size:22px;font-weight:600;letter-spacing:-.02em;margin:34px 0 12px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;margin-bottom:8px}
.fact{background:var(--sand);border-radius:14px;padding:14px 16px}.fact dt{font-size:12px;font-weight:600;color:var(--amber);margin-bottom:2px}.fact dd{font-size:14.5px;color:var(--ink)}
.cta.top-cta{margin:4px 0 30px}"""


def page(lang):
    t = T[lang]
    rtl = ' dir="rtl"' if lang == "ar" else ""
    url = SITE + PATHS[lang]
    alts = "".join('<link rel="alternate" hreflang="%s" href="%s%s">\n' % (l, SITE, p) for l, p in PATHS.items())
    alts += '<link rel="alternate" hreflang="x-default" href="%s%s">\n' % (SITE, PATHS["tr"])
    strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s))
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": t["title"], "description": t["desc"],
         "inLanguage": lang, "dateModified": UPDATED, "about": {"@id": SITE + "/#restaurant"},
         "breadcrumb": {"@id": url + "#breadcrumb"}},
        {"@type": "Restaurant", "@id": SITE + "/#restaurant", "name": "Mare Gastro", "url": SITE + HOME[lang],
         "telephone": "+905323540888", "email": MAIL, "acceptsReservations": True,
         "hasMenu": SITE + MENU[lang],
         "address": {"@type": "PostalAddress", "streetAddress": "Kırkpınar Soğuksu, İstasyon 3 Cad. No:55",
                     "addressLocality": "Sapanca", "addressRegion": "Sakarya", "postalCode": "54600", "addressCountry": "TR"},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "09:00", "closes": "00:00"}],
         "potentialAction": [
             {"@type": "ReserveAction", "name": t["form"],
              "target": {"@type": "EntryPoint", "urlTemplate": SITE + FORM[lang], "inLanguage": lang,
                         "actionPlatform": ["http://schema.org/DesktopWebPlatform", "http://schema.org/MobileWebPlatform"]},
              "result": {"@type": "FoodEstablishmentReservation", "name": t["crumb"]}},
             {"@type": "ReserveAction", "name": t["wa"],
              "target": {"@type": "EntryPoint", "urlTemplate": WA}}]},
        {"@type": "HowTo", "@id": url + "#howto", "name": strip(t["steps_h"]) + " · Mare Gastro", "inLanguage": lang,
         "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": d, "url": SITE + FORM[lang]} for i, (n, d) in enumerate(t["steps"])]},
        {"@type": "FAQPage", "@id": url + "#faq", "url": url, "inLanguage": lang, "dateModified": UPDATED,
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(ans)}} for q, ans in t["qa"]]},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Mare Gastro", "item": SITE + HOME[lang]},
            {"@type": "ListItem", "position": 2, "name": t["crumb"], "item": url}]},
    ]}
    steps = "".join('<li class="step"><h3>%s</h3><p>%s</p></li>' % (html.escape(n), html.escape(d)) for n, d in t["steps"])
    facts = "".join('<div class="fact"><dt>%s</dt><dd>%s</dd></div>' % (html.escape(k), v) for k, v in t["facts"])
    qa = "".join('<section class="qa"><h3 style="font-size:17px;font-weight:600;letter-spacing:-.015em;margin-bottom:6px">%s</h3><p>%s</p></section>\n' % (html.escape(q), ans) for q, ans in t["qa"])
    faq_h = {"tr": "Sık Sorulan Sorular", "en": "Frequently Asked Questions", "ar": "الأسئلة الشائعة", "ru": "Частые вопросы"}[lang]
    btns = ('<div class="cta%%s"><a class="btn btn-p" href="%s">%s</a><a class="btn btn-s" href="%s" target="_blank" rel="noopener">%s</a><a class="btn btn-s" href="%s">%s</a></div>'
            % (FORM[lang], t["form"], WA, t["wa"], TEL, t["call"]))
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
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body>
{GTM_BODY}
<header class="top"><div class="top-in"><a href="{HOME[lang]}" aria-label="Mare Gastro"><img src="/images/marelogo1.png" alt="Mare Gastro"></a>
<div style="display:flex;gap:8px"><a class="btn btn-s" href="{WA}" target="_blank" rel="noopener">{t['wa']}</a><a class="btn btn-p" href="{FORM[lang]}">{t['form']}</a></div></div></header>
<main>
<nav class="crumb" aria-label="breadcrumb"><a href="{HOME[lang]}">{t['back']}</a> · {t['crumb']}</nav>
<h1>{t['h1']}</h1>
<p class="lead">{t['lead']}</p>
<p class="upd">{t['updated']}</p>
{btns % ' top-cta'}
<h2 class="sec">{t['steps_h']}</h2>
<ol class="steps" style="list-style:none">{steps}</ol>
<h2 class="sec">{t['facts_h']}</h2>
<dl class="facts">{facts}</dl>
<h2 class="sec">{faq_h}</h2>
{qa}{btns % ''}
</main>
<footer>© 2026 Mare Gastro · Didi Otel · Sapanca<br><a href="{MENU[lang]}">Menu</a><a href="{FAQ[lang]}">FAQ</a><a href="{BLOG[lang]}">Blog</a><a href="https://www.instagram.com/maregastro/" target="_blank" rel="noopener">Instagram</a></footer>
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
