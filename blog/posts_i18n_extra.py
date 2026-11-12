# -*- coding: utf-8 -*-
"""2026-11-12: EN/AR/RU translations of the 8 builder posts that were Turkish-only
(date cluster, alcohol, live music, signature dishes). Merged into posts_i18n_data.POSTS.

Rules kept from the TR originals: Mare is "right next to Lake Sapanca" (never "on the shore"),
no prices, guest quotes are real Google reviews (translated, name kept, marked as translated),
facts as published in TR (4.9 Google rating Oct 2026, ~1.5 h from Istanbul, free parking + valet).
Cross-links use the Turkish URL; build_blog_i18n.localize_links() re-points them to the
same-language translation at build time.
"""
import html
from build_blog_i18n import L, bfig, MENU_A, REZ_A, MAPS, YT, DIDIWEB, WA, SITE

def B(slug):
    return "%s/blog/%s.html" % (SITE, slug)

WATCH = {"en": "Watch on YouTube", "ar": "شاهد على يوتيوب", "ru": "Смотреть на YouTube"}
REVIEW = {"en": "Google review, translated from Turkish", "ar": "تقييم على Google، مترجم من التركية", "ru": "отзыв в Google, перевод с турецкого"}

def V(vid, title, cap, lang):
    return ('<figure class="bvideo"><div class="bvideo-frame"><iframe src="https://www.youtube-nocookie.com/embed/%s" '
            'title="%s" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'
            '<figcaption>%s · <a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">%s</a></figcaption></figure>'
            % (vid, html.escape(title), html.escape(cap), vid, WATCH[lang]))

def Q(text, name, lang):
    return '<blockquote><p>“%s”</p><p><strong>%s</strong> · <a href="%s">%s</a></p></blockquote>' % (text, name, MAPS, REVIEW[lang])

def T(head, rows):
    th = "".join("<th>%s</th>" % h for h in head)
    tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return '<div class="btable"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, tr)

def UL(items, tag="ul"):
    return "<%s>%s</%s>" % (tag, "".join("<li><strong>%s</strong> %s</li>" % (a, b) for a, b in items), tag)

# YouTube video titles are the channel's own (Turkish) titles
VT = {
 "zseYjYW3uFk": "Lezzetli Karidesin Sırrı Kabuğunda Gizli! Şef Doğan Anapa & Kadir Çiçek | Mare Gastro Sapanca",
 "aOAyrgTBcos": "Sapanca'da Saklı Fine Dining Deneyimi: Mare Gastro",
 "GiwkPYUSVyY": "Eda Acar ve Orkestrası Mare Gastro sahnesinde! | Sapanca Canlı Müzik",
 "rhSfnoAOCIg": "Karasu Kuşkonmazı ve Kaya Levreği: Şefin İmza Tabağı Nasıl Hazırlanıyor?",
 "YAbVQG4u7LI": "Balık Suyuyla Islatılmış Ekmek ve Bebek Kalamar: Şef Doğan Anapa | Mare Gastro",
 "Asn8FZ0nFX0": "Şef Doğan Anapa'nın Sunumuyla: Mare Gastro'da İmza Tabak Kuzu İncik ve Keşkek",
 "NybLKER1j_4": "Deniz Mahsullü Buğday Risotto Nasıl Yapılır? | Mare Gastro Sapanca & Şef Doğan Anapa",
 "enOAIZfhK3s": "Özel Tarif: Ferahlatıcı Karpuz Salatası Yatağında Kuzu Kokoreç | Mare Gastro Sapanca",
}

MAPS_RATING = {"en": "rated 4.9 on Google Maps", "ar": "تقييم 4.9 على خرائط Google", "ru": "рейтинг 4,9 в Google Картах"}

EXTRA = {}

# ═══════════════════════════════ ENGLISH ═══════════════════════════════
E = "en"
EXTRA["ilk-bulusma-icin-mekan-onerisi"] = {E: {
 "cat":"date","date":"2026-10-24","read":"6 min read",
 "img":"mare-teras-misafir.webp","alt":"Guests having dinner on the terrace — a first date restaurant idea, Mare Gastro Sapanca",
 "h1":"Where to Go on a <em>First Date</em>: 6 Criteria for Choosing the Right Place",
 "title":"Where to Go on a First Date: 6 Criteria | Mare Gastro",
 "desc":"Where to go on a first date? How to pick a place that lets you talk and doesn't feel tense: 6 criteria and one suggestion from Sapanca, Mare Gastro.",
 "kw":"first date restaurant, where to go on a first date, first date ideas, first date dinner, sapanca first date, romantic restaurant sapanca",
 "lead":"A good first date place offers a sound level that doesn't drown the conversation, an atmosphere that eases the nerves and details that give you something to talk about. Below are 6 criteria for choosing the right place, and one suggestion that meets all of them: Mare Gastro in Sapanca, right next to the lake.",
 "body":[
  ("What Kind of Place Is Right for a First Date?",
   ["The best first date place is one where two people can hear each other easily, tables aren't too close together, the menu is easy to share and the setting gives you something natural to talk about. Too formal creates tension; too loud kills the conversation. What you are looking for is the balance between the two."]),
  ("6 Criteria for Choosing a First Date Place",
   [UL([("Sound level:","You should be able to talk without raising your voice. If there is live music, ask for a table away from the stage."),
        ("Table layout:","A little distance from the next table helps you relax."),
        ("A menu for sharing:","Plates ordered for the middle naturally start the “have you tried this?” conversation."),
        ("Atmosphere:","A view, a garden or an interesting story from the kitchen fills the quiet moments."),
        ("Getting there and parking:","Nobody wants to lose time looking for a parking spot on a first date."),
        ("Trust:","A place with strong reviews lowers the risk of the evening going wrong.")], "ol")]),
  ("How Does Mare Gastro Meet These Criteria?",
   [T(["Criterion","At Mare Gastro"],[
      ["Sound level","Calm on weekdays; on weekend live-music nights you can ask for a table away from the stage"],
      ["Table layout","Well-spaced tables in a large garden, quiet corners in the indoor dining room"],
      ["A menu for sharing","Starters, hot appetisers and seafood are made for sharing"],
      ["Atmosphere","Right next to the lake, among the pines; Sapanca's only fine dining restaurant"],
      ["Getting there and parking","About 1.5 hours from Istanbul, large car park at Didi Otel"],
      ["Trust",'<a href="%s">Rated 4.9 on Google Maps</a> (October 2026)' % MAPS]]),
    "In short, for anyone who wants a first date that feels more special than an ordinary coffee without becoming stiff or formal, Mare Gastro is a balanced choice.",
    "First-time guests often say the atmosphere puts them at ease from the very first minute. From a guest's Google review:",
    Q("Even though it was our first visit, we fell in love with the atmosphere. The setting, presentation, service and music were flawless. The food arrives at your table as a work of art.","Büşra Canbazoğlu",E)]),
  ("Coffee or Dinner for a First Date?",
   ["Coffee is short and low-risk; dinner means more time and a deeper conversation. If your first messages went well and you really want to take time to get to know each other, dinner is the better choice. Choosing a place outside the city, like Sapanca, turns the first date into an “event” on its own: the drive, the view and the meal give you three different things to talk about.",
    "If you prefer a shorter plan, come close to sunset and keep the evening light with starters and dessert."]),
  ("What to Avoid When Choosing a First Date Place",
   [UL([("Very loud places:","Leaning in to hear each other breaks the flow of the conversation."),
        ("Long waits:",'Turning up without a booking and waiting at the door spoils the first impression; on weekends always %s.' % L(REZ_A(E),"book a table")),
        ("Complicated menus:","Dishes that are hard to eat can make you tense; shared starters are more relaxed."),
        ("Parking trouble:","A place with parking problems starts the date badly. Didi Otel has a large car park."),
        ("No plan for afterwards:","If the evening runs long, it helps to know what comes next; a stay at Didi Otel or a walk by the lake are good options.")])]),
  ("What to Order on a First Date",
   ["On a first date, dishes that are easy to eat, easy to share and don't interrupt the conversation are ideal. At Mare Gastro a good plan is to start with starters and seafood hot appetisers, then choose a main course each. You can see the current dishes on the %s." % L(MENU_A(E),"menu"),
    "If you're looking for something to talk about, the stories behind the plates help. For example, Chef Doğan Anapa and Kadir Çiçek explain in this video why one of the most loved dishes, grilled shell-on prawns, is cooked in its shell:",
    V("zseYjYW3uFk",VT["zseYjYW3uFk"],"Chef Doğan Anapa and Kadir Çiçek: the secret of grilled shell-on prawns",E)]),
  ("Outdoor or Indoor for a First Date?",
   ["When the weather is nice, outdoor seating is a big advantage on a first date: nature and the view fill the quiet moments and the setting feels more relaxed. At Mare Gastro you can sit in the garden in summer and in the indoor dining room on cool or rainy evenings. Just mention your preference when you book; if the weather changes, the team adjusts your table."]),
  ("The Chef's Table: The Detail That Makes a First Date Memorable",
   ["What makes a first date memorable is often a small story. Behind the plates at Mare Gastro is the story of Executive Chef Doğan Anapa: a chef who moved from cinema to the kitchen, and a kitchen that reinterprets Sakarya's ıslama köfte tradition with bread soaked in fish stock and baby squid. %s" % L(B("sef-dogan-anapa"),"Read the chef's story here.")]),
  ("If It Goes Well: Ideas for a Second Date",
   ["If the first date went well, you can plan something longer for the second: the lakeside at sunset, then dinner and a night at Didi Otel. For ideas, see our %s and our %s." % (L(B("istanbula-yakin-date-mekani"),"guide to date night spots near Istanbul"), L(B("sevgiliyle-gidilecek-mekanlar-sapanca"),"places to go as a couple"))]),
 ],
 "faq":[
  ("What kind of place should you choose for a first date?","A sound level that lets you talk, well-spaced tables, dishes to share, an atmosphere that gives you something to talk about, easy access and strong reviews. A place that meets these six criteria takes the tension out of a first date."),
  ("Is there a good first date restaurant in Sapanca?","Mare Gastro, in the garden of Didi Otel right next to the lake, stands out for a first date with its 4.9 rating on Google Maps, open-air garden, indoor dining room and a menu made for sharing."),
  ("Is a restaurant with live music a good idea for a first date?","If you want to talk, a table away from the stage is best. Mare Gastro sometimes has live music at weekends; you can ask for a quieter table when you book."),
  ("What should you order on a first date?","Dishes that are easy to eat and share: starters, hot appetisers and seafood. Then everyone chooses their own main course. Mare Gastro's current menu is at maregastro.com/menu/en."),
  ("How long does it take to get to Mare Gastro from Istanbul?","Sapanca is about 1.5 hours from Istanbul; the time depends on traffic and where you set off. Didi Otel has a large car park."),
 ],
}}

EXTRA["istanbula-yakin-date-mekani"] = {E: {
 "cat":"date","date":"2026-10-24","read":"6 min read",
 "img":"mare-romantik-kadeh.webp","alt":"A couple raising their glasses by the lake — date night spot near Istanbul, Mare Gastro Sapanca",
 "h1":"A <em>Date Night Spot</em> Near Istanbul: A Fine Dining Evening in Sapanca",
 "title":"Date Night Spot Near Istanbul: Sapanca | Mare Gastro",
 "desc":"A date night spot near Istanbul: 1.5 hours away, rated 4.9 on Google, with indoor and outdoor seating. Plan a fine dining date at Mare Gastro in Sapanca.",
 "kw":"date night near istanbul, date spot outside istanbul, romantic restaurant near istanbul, sapanca date night, sapanca fine dining, weekend date istanbul",
 "lead":"If you are looking for a date night spot near Istanbul, here is the short answer: Sapanca is about 1.5 hours from the city, and Mare Gastro, right next to the lake, is the only restaurant in the area with a fine dining concept. With a 4.9 rating on Google Maps, an open-air garden, an indoor dining room and the option to stay at Didi Otel, you can turn a date into a full getaway.",
 "body":[
  ("What Is the Best Date Night Spot Near Istanbul?",
   ["For a date that truly takes you away from the city crowds without an exhausting drive, Sapanca stands out. Among the options in the area, Mare Gastro is the first address for couples looking for fine dining, thanks to its setting in the garden of Didi Otel, the Aegean-Mediterranean cuisine of Executive Chef Doğan Anapa and its %s." % L(MAPS,"4.9 rating on Google Maps"),
    "As of October 2026, a Google Maps search for “fine dining Sapanca” shows Mare Gastro as the first restaurant. That is not the restaurant's own claim; it is the result of the ratings and reviews guests have left."]),
  ("What Makes a Good Date Night Spot?",
   ["A good date spot offers four things at once: a setting that doesn't drown out the conversation, a view or a story that stays with you, a kitchen you can trust and attentive service. When one of them is missing, what you remember about the evening is not the food but that missing detail.",
    "Guest reviews focus on exactly these four points. What a first-time guest wrote on Google comes very close to the recipe for a good date night:",
    Q("From the welcome to the very last moment, it makes you feel special and crowns the night with a feast for the eyes and the palate.","Yasemin Babadağ",E),
    "The picture is similar on the service side; in the reviews you see guests thanking the waiters by name. For more examples, see our %s." % L(B("mare-gastro-google-yorumlari"),"collection of Google reviews")]),
  ("Why Leave Istanbul for a Date?",
   ["In Istanbul a date often means traffic, parking trouble and a noisy dining room. A date outside the city makes the journey part of the experience: conversation along the way, sunset right next to the lake and a dinner you don't have to rush.",
    T(["Criterion","Date in Istanbul","Date at Mare Gastro in Sapanca"],[
      ["Getting there","Traffic and parking trouble","About 1.5 hours, large car park at Didi Otel"],
      ["Atmosphere","Crowded, noisy dining rooms","A garden among the pines, right next to the lake"],
      ["Kitchen","Lots of choice, fine dining is expensive and crowded","Sapanca's only fine dining restaurant, chef's signature plates"],
      ["Weather","Stuck indoors","Open-air garden in summer, indoor dining room on cool evenings and in winter"],
      ["End of the evening","Traffic on the way home","Option to stay at Didi Otel in the same garden"]])]),
  ("How Long Does It Take From Istanbul to Sapanca?",
   ["From Istanbul's Asian side, Sapanca is about 1.5 hours via the TEM or the Northern Marmara Motorway; the time depends on traffic and where you set off. Leaving on a weekend afternoon and arriving in time for sunset is the nicest plan for a date.",
    "We cover every way of getting there in our %s. Mare Gastro's address: Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, Sapanca/Sakarya (garden of Didi Otel)." % L(B("sapancaya-nasil-gidilir"),"guide to getting to Sapanca")]),
  ("What Is a Date Night at Mare Gastro Like?",
   ["A date night at Mare Gastro usually opens with starters and hot appetisers to share, continues with the chef's seafood or meat plates and ends with signature desserts. Shared plates start the conversation naturally; for couples on their first visit, that is a small ice-breaker.",
    V("aOAyrgTBcos",VT["aOAyrgTBcos"],"A short glimpse of an evening at Mare Gastro",E),
    "You can browse the current dishes on our %s; the menu changes with the season and the freshest produce of the day." % L(MENU_A(E),"menu"),
    "Weekend evenings are often accompanied by live music. If you want a quieter date, just say so when you book and our team will arrange a quieter corner for you."]),
  ("Indoor or Outdoor? Is It Right for a Date in Every Season?",
   ["Yes. Mare Gastro has both an open-air garden and an indoor dining room. In summer you dine outdoors under the pine trees in the cool air from the lake; on cool and rainy days you are welcomed indoors with the same kitchen. That way your date plan doesn't depend on the weather.",
    V("GiwkPYUSVyY",VT["GiwkPYUSVyY"],"Live music in the garden on summer evenings: Eda Acar and her orchestra",E)]),
  ("The Name Behind the Kitchen: Chef Doğan Anapa",
   ["Mare Gastro's kitchen is run by Executive Chef Doğan Anapa. Coming from a background in film, the chef builds every menu like a story and interprets local produce (such as Karasu asparagus and Sakarya's ıslama tradition) with Aegean-Mediterranean technique. The whole concept was designed by Kadir Çiçek within Didi Otel.",
    "To get to know the chef better, read %s and watch his recipes on %s." % (L(B("sef-dogan-anapa-kimdir"),"Who is Chef Doğan Anapa?"), L(YT,"our YouTube channel"))]),
  ("If You Want to Make It Longer: Staying at Didi Otel",
   ["Mare Gastro is in the garden of %s. Instead of driving back to Istanbul after dinner, you can stay at the hotel in the same garden and start the next day with a lake view. You can mention that you'd like to stay in the booking form." % L(DIDIWEB,"Didi Otel"),
    "We explain step by step how to plan dinner and a stay together in our %s." % L(B("sapanca-sevgiliyle-yemek-ve-konaklama"),"guide to a night in Sapanca as a couple")]),
  ("Weekday or Weekend Date?",
   ["Both have their own charm. Weekday evenings are calmer, a good choice if you want a long conversation for two. Weekends are livelier and often come with live music. We recommend the calm for a first date and the weekend for a celebratory evening. You can check current opening hours on our %s or %s." % (L(MAPS,"Google Maps profile"), L(WA,"WhatsApp line"))]),
  ("A Quick Checklist for a Date Near Istanbul",
   [UL([("Booking:","For weekends, %s in advance." % L(REZ_A(E),"book a table")),
        ("Timing:","Set off so that you arrive in time for sunset."),
        ("Preference:","Garden or indoor dining room, a quiet corner or live music: mention it when you book."),
        ("Celebration:","If it is a special day, let our team know in advance."),
        ("Getting home:","If you'd rather not face the long drive back, consider staying at Didi Otel.")])]),
 ],
 "faq":[
  ("Where is a good date night spot near Istanbul?","Sapanca is about 1.5 hours from Istanbul. Mare Gastro, in the garden of Didi Otel right next to the lake, is one of the standout restaurants for a date near Istanbul, with a 4.9 rating on Google Maps and a fine dining concept."),
  ("Is there a fine dining restaurant in Sapanca?","Yes. Mare Gastro is the only restaurant in Sapanca with a fine dining concept. Its kitchen is run by Executive Chef Doğan Anapa, who interprets Aegean and Mediterranean cuisine with local produce."),
  ("Does Mare Gastro have indoor and outdoor seating?","Yes. In summer you are served in the open-air garden under the pine trees, and on cool and rainy days in the indoor dining room. You can state your preference when you book."),
  ("Can we stay in Sapanca after the date?","Mare Gastro is in the garden of Didi Otel. After dinner you can stay at the hotel in the same garden; just mention it in the booking form."),
  ("How do I book at Mare Gastro?","Use the three-step form on maregastro.com to choose the date, time and party size and confirm via WhatsApp. We recommend booking in advance for weekends."),
 ],
}}

EXTRA["sevgiliyle-gidilecek-mekanlar-sapanca"] = {E: {
 "cat":"romantik","date":"2026-10-24","read":"6 min read",
 "img":"mare-bahce-manzarasi.webp","alt":"Lake view from the Didi Otel garden — places to go as a couple in Sapanca, Mare Gastro",
 "h1":"Places to Go as a Couple: <em>A Sapanca Guide</em> for Two",
 "title":"Places to Go as a Couple: Sapanca Guide | Mare Gastro",
 "desc":"Places to go as a couple: we planned a full day in Sapanca. The lakeside, nature routes and, for the evening, Mare Gastro, rated 4.9 on Google.",
 "kw":"places to go as a couple, romantic places sapanca, things to do in sapanca for couples, sapanca romantic day trip, romantic restaurant sapanca, couples getaway near istanbul",
 "lead":"A list of places to go as a couple is really the plan for a day: a little nature during the day, a view at sunset and a good table in the evening. Sapanca brings all three together about 1.5 hours from Istanbul. Below you'll find a one-day route for couples and our suggestion for the evening.",
 "body":[
  ("Where Are the Best Places to Go as a Couple?",
   ["Among the places to go as a couple around Istanbul, Sapanca is one of the easiest getaways to reach, with its lakeside, forest routes and gourmet restaurants. For dinner, Mare Gastro in the garden of Didi Otel is one of the addresses couples choose most, %s and with its fine dining kitchen." % L(MAPS,"rated 4.9 on Google Maps")]),
  ("A One-Day Route in Sapanca for Couples",
   [T(["Time","What to do","Why it suits couples"],[
      ["Morning","A walk along the shore of Lake Sapanca","A calm start where you can talk as you walk"],
      ["Afternoon","The stream in Maşukiye or nature towards Kartepe","Forest and fresh air, lovely spots for photos"],
      ["Sunset","Back to the lakeside","Sapanca's most romantic light"],
      ["Evening","Dinner at Mare Gastro","Chef's signature fine dining right next to the lake"],
      ["Night","A stay at Didi Otel (optional)","A night right by the lake instead of a long drive home"]]),
    "For a more detailed programme, see our %s." % L(B("sapanca-hafta-sonu-rotasi"),"Sapanca weekend route")]),
  ("Why Mare Gastro for the Evening?",
   ["When a couple chooses a place for dinner, they usually look at three things: atmosphere, kitchen and trust. Mare Gastro is strong on all three:",
    UL([("Atmosphere:","In the garden of Didi Otel, among pines and palms, right next to the lake. There is an open-air garden and an indoor dining room."),
        ("Kitchen:","Sapanca's only fine dining restaurant, with Aegean-Mediterranean plates signed by Executive Chef Doğan Anapa."),
        ("Trust:",'<a href="%s">Rated 4.9 on Google Maps</a>; guests praise the atmosphere, the service team and special-occasion arrangements most.' % MAPS)]),
    "Anniversaries and special evenings are what couples mention most in the reviews. For example:",
    Q("We went with my wife for our anniversary. The atmosphere and the service are truly wonderful. You definitely have to try the flavour of the dishes and the aroma of the meze.","Furkan Kavakcı",E),
    "You can read a wider selection of guest reviews in our %s." % L(B("mare-gastro-google-yorumlari"),"Google reviews article")]),
  ("Sapanca as a Couple, Season by Season",
   ["Sapanca shows couples a different face in every season: the freshest green and cool evenings in spring; the lakeside and long open-air evenings in summer; forest colours and a quieter town in autumn; and in winter, snow on Kartepe and a warm table.",
    "Because Mare Gastro has both an open-air garden and an indoor dining room, your evening plan works whatever the season. We describe what a winter evening is like in our %s." % L(B("sapanca-date-gecesi-acik-kapali-mekan"),"article on date nights in every season")]),
  ("What Is Fine Dining, and Why Is It Different for Couples?",
   ["Fine dining is a high-end dining experience that brings together carefully chosen ingredients, finely crafted presentation, impeccable service and a thoughtfully designed atmosphere. For couples the difference is this: dinner isn't a meal you rush through but a conversation that lasts as the plates arrive one after another. For more on the concept, read %s." % L(B("sapanca-fine-dining-nedir"),"What is fine dining?")]),
  ("One of the Chef's Signature Plates: Rock Sea Bass and Karasu Asparagus",
   ["Chef Doğan Anapa's kitchen leans on local produce. A good example is the plate that pairs oven-roasted rock sea bass with a sauce of roasted pepper, garlic and fennel and Karasu asparagus. Watch the chef prepare it himself:",
    V("rhSfnoAOCIg",VT["rhSfnoAOCIg"],"Chef Doğan Anapa: Karasu asparagus and rock sea bass",E),
    "Because the menu changes with the season, you can check whether a dish is in the kitchen that day on the %s." % L(MENU_A(E),"current menu")]),
  ("Celebrating a Special Day Together?",
   ["For a special day such as an anniversary, a birthday or a proposal, just leave the team a note when you book; the table setting, a cake or the surprise moment is planned in advance. Our guides by occasion: %s, %s and %s." % (L(B("sapanca-yildonumu-yemegi"),"anniversary dinner"), L(B("sapanca-evlilik-teklifi"),"marriage proposal"), L(B("sapanca-romantik-es-dogum-gunu-yemegi"),"a birthday dinner for your partner"))]),
  ("What to Look For When Choosing a Place as a Couple",
   [UL([("Sound and privacy:","Ask for a table where you can talk just the two of you."),
        ("Weather:","A place with both indoor and outdoor seating removes the risk of your plan falling through."),
        ("Getting there:","After a long drive, choose a place without parking trouble."),
        ("Staying over:","If you're out of town, being able to stay at the same place makes the evening easier."),
        ("Reviews:","Look at recent guest reviews more than photos.")])]),
 ],
 "faq":[
  ("Where are good places to go as a couple?","For getaways near Istanbul, Sapanca stands out: a walk along the lake, nature towards Maşukiye and Kartepe, sunset and dinner. For the evening, Mare Gastro in the garden of Didi Otel is an address chosen by couples looking for fine dining."),
  ("Where can couples have dinner in Sapanca?","Mare Gastro, in the garden of Didi Otel right next to the lake, is one of the standout restaurants for a couple's dinner in Sapanca, with a 4.9 rating on Google Maps, an open-air garden and an indoor dining room."),
  ("Can couples visit Sapanca as a day trip?","Yes. Sapanca is about 1.5 hours from Istanbul, so a day trip works. If you'd rather not drive back, you can stay at Didi Otel, where Mare Gastro is located."),
  ("Does Mare Gastro arrange special occasions?","Yes. For anniversaries, birthdays and proposals, just leave the team a note when you book; the table and the surprise moment are planned in advance."),
  ("Who is Mare Gastro's chef?","Mare Gastro's Executive Chef is Doğan Anapa. Coming from a background in film, the chef interprets Aegean-Mediterranean cuisine with local produce such as Karasu asparagus and shares his recipes on YouTube."),
 ],
}}

EXTRA["sapanca-sevgiliyle-yemek-ve-konaklama"] = {E: {
 "cat":"didi","date":"2026-10-24","read":"6 min read",
 "img":"mare-bahce-havuz-yolu.webp","alt":"Pool path in the Didi Otel garden — dinner and an overnight stay for couples in Sapanca",
 "h1":"A Night in Sapanca as a Couple: <em>Dinner and a Stay</em> in One Place",
 "title":"Sapanca for Couples: Dinner + Overnight Stay | Mare Gastro",
 "desc":"Want to plan dinner and a stay in Sapanca in one place? Dine at Mare Gastro in the garden of Didi Otel and stay in the same garden.",
 "kw":"sapanca hotel with restaurant, sapanca dinner and stay, didi otel sapanca, romantic weekend sapanca, sapanca couples hotel and restaurant",
 "lead":"If you are planning a night in Sapanca with your partner, the biggest convenience is having dinner and your stay in the same place. Mare Gastro is in the garden of Didi Otel: after dinner you walk to your room in the same garden without getting into the car. Here is the plan, step by step.",
 "body":[
  ("Can You Have Dinner and Stay in the Same Place in Sapanca?",
   ["Yes. Mare Gastro is a fine dining restaurant located in the garden of Didi Otel in Sapanca. You can have dinner at Mare Gastro and stay in the same property, at Didi Otel. That removes the most tiring part of an evening out of town: the drive back."]),
  ("Why Plan Dinner and a Stay Together?",
   [T(["","Dinner only","Dinner + stay at Didi Otel"],[
      ["Pace of the evening","Watching the clock and the drive home","No rush, the evening lasts as long as you like"],
      ["Getting there","A 1.5-hour drive back to Istanbul at night","A few steps from the garden to your room"],
      ["Next day","Up early and back to work","A morning with a lake view and breakfast"],
      ["Celebration","A single moment","A full weekend getaway"]])]),
  ("How to Plan One Night",
   [UL([("Booking:","Choose the date, time and party size in the %s and mention in the same form that you'd like to stay." % L(REZ_A(E),"booking form")),
        ("Arrival:","Arrive in the afternoon and settle in at Didi Otel; there is a large car park on site."),
        ("Sunset:","Wait for the evening in the garden or right next to the lake."),
        ("Dinner:","At Mare Gastro, in the open-air garden if the weather allows, in the indoor dining room on cool days."),
        ("Morning:","Breakfast with a lake view; for ideas see our %s." % L(B("sapanca-gol-manzarali-kahvalti"),"article on lake-view breakfast"))], "ol")]),
  ("What Makes Mare Gastro Different in Sapanca?",
   ["Mare Gastro is the only restaurant in Sapanca with a fine dining concept. The concept was designed by Kadir Çiçek within Didi Otel, and Executive Chef Doğan Anapa leads the kitchen. %s, and in October 2026 it was the first restaurant in a Google search for “fine dining Sapanca”." % L(MAPS,"Rated 4.9 on Google Maps"),
    "The chef's kitchen talks to the region. Watch the recipe in which, inspired by Sakarya's famous ıslama köfte, he serves grilled baby squid on bread soaked in fish stock:",
    V("YAbVQG4u7LI",VT["YAbVQG4u7LI"],"Chef Doğan Anapa: baby squid inspired by the ıslama tradition",E)]),
  ("Which Special Days Does This Plan Suit?",
   ["A night that combines dinner and a stay is the plan couples choose most for their special days. If you mention the occasion when you book, the team prepares the table setting and the surprise moment accordingly:",
    UL([("Anniversary:","Details in our %s." % L(B("sapanca-yildonumu-yemegi"),"anniversary article")),
        ("Marriage proposal:","Planning steps in our %s." % L(B("sapanca-evlilik-teklifi"),"proposal guide")),
        ("Your partner's birthday:","Ideas in our %s." % L(B("sapanca-romantik-es-dogum-gunu-yemegi"),"romantic birthday dinner article")),
        ("Valentine's Day:","Suggestions in our %s." % L(B("sapanca-sevgililer-gunu-yemegi"),"Valentine's Day article"))]),
    "What one of our guests wrote about their wedding anniversary:",
    Q("We came for our wedding anniversary and I didn't expect this much. The food, the service and the ambience are excellent.","Fikriye Erkan",E)]),
  ("What to Do in the Morning",
   ["The best part of staying over is the next morning. A lake-view breakfast, then a walk along the shore of Lake Sapanca and a short nature route towards Maşukiye or Kartepe round off the day before the drive home. One guest wrote that they came back for breakfast the morning after dinner:",
    Q("We came for rakı and dinner last night and came back again today for breakfast. A very enjoyable place, the ambience and the music are great.","Rümeysa Aslan",E),
    "All our route suggestions are in our %s." % L(B("sapanca-hafta-sonu-rotasi"),"weekend route article")]),
  ("Open-Air Garden and Indoor Dining Room: Which Season?",
   ["Any season. In summer in the open-air garden under the pines, with the cool air from the lake; in autumn and winter in the warm indoor dining room, with the same kitchen. For a plan made for the winter months, read our %s." % L(B("sapanca-date-gecesi-acik-kapali-mekan"),"article on date nights in every season")]),
  ("About Didi Otel",
   ["Didi Otel is a hotel in Sapanca known for its corporate structure; Mare Gastro is in its garden. For rooms and stays, visit %s, and read more about the restaurant in our %s." % (L(DIDIWEB,"Didi Otel's website"), L(B("didi-otel-restoran"),"article on the Didi Otel restaurant"))]),
 ],
 "faq":[
  ("Is there a romantic hotel with a restaurant in Sapanca?","Yes. The fine dining restaurant Mare Gastro is in the garden of Didi Otel. You can have dinner at Mare Gastro and stay in the same property."),
  ("Can I dine at Mare Gastro and stay at Didi Otel?","Yes. Mare Gastro is part of Didi Otel and sits in its garden. You can mention your stay in the Mare Gastro booking form; for room details see Didi Otel's website."),
  ("What should we plan for a night in Sapanca as a couple?","Arrive in the afternoon and check in, enjoy the lakeside at sunset, have dinner at Mare Gastro in the evening and a lake-view breakfast the next morning: an easy plan for couples."),
  ("Is Mare Gastro open in winter?","Mare Gastro also has an indoor dining room; on cool and rainy days guests are served indoors. You can confirm current opening hours on the Google Maps profile or the WhatsApp line."),
  ("Is there parking at Didi Otel?","Yes, Didi Otel has a large car park, and Mare Gastro guests can use it too."),
 ],
}}

EXTRA["sapanca-date-gecesi-acik-kapali-mekan"] = {E: {
 "cat":"mevsim","date":"2026-10-24","updated":"2026-11-12","read":"6 min read",
 "img":"mare-kabana-oturma.webp","alt":"Cabana seating in the garden — a date night restaurant with indoor and outdoor seating, Mare Gastro Sapanca",
 "h1":"Date Night in Every Season: A Romantic Restaurant in Sapanca With <em>Indoor and Outdoor</em> Seating",
 "title":"Sapanca Date Night: Indoor & Outdoor Seating | Mare Gastro",
 "desc":"A date plan that rain, winter or a summer night won't spoil: a Sapanca fine dining restaurant with an open-air garden and an indoor dining room, rated 4.9 on Google.",
 "kw":"sapanca restaurant with indoor seating, sapanca winter date, romantic indoor restaurant sapanca, sapanca outdoor restaurant, rainy day date, sapanca date night",
 "lead":"The weather is the most common reason date plans fall apart. If you don't want to dream of an evening outdoors and get caught in the rain, or be stuck in crowded indoor rooms in winter, choose a place with both outdoor and indoor seating. In Sapanca, Mare Gastro serves the same fine dining kitchen in two different settings.",
 "body":[
  ("Is There a Romantic Restaurant in Sapanca With Indoor and Outdoor Seating?",
   ["Yes. Mare Gastro, in the garden of Didi Otel, has both an open-air garden under the pine trees and an indoor dining room. In summer you dine outdoors in the cool air from the lake; on cool, rainy or winter evenings you are welcomed indoors by the same kitchen and the same service team. Being the only restaurant in Sapanca with a fine dining concept is another plus for a date."]),
  ("A Date Plan for Each Season",
   [T(["Season","Where to sit","Our suggestion"],[
      ["Spring","Open-air garden, indoor dining room in the cooler hours","Come before sunset and move inside as the evening cools"],
      ["Summer","Open-air garden","A long evening with the cool lake air and weekend live music"],
      ["Autumn","Indoor dining room or a sheltered outdoor area","A daytime route through Sapanca's autumn colours, warm plates in the evening"],
      ["Winter","Indoor dining room","A warm dinner after a snowy day on Kartepe"]])]),
  ("A Winter Date: What to Eat",
   ["Slow-cooked, hearty plates suit cold weather. One of the dishes that best shows Chef Doğan Anapa's approach is lamb shank cooked for 3 hours in a 180-degree oven, served with keşkek, its own stock and mint oil:",
    V("Asn8FZ0nFX0",VT["Asn8FZ0nFX0"],"Chef Doğan Anapa: lamb shank and keşkek",E),
    "Because the menu changes with the season, you can check which plates are on that evening on the %s. We also describe our winter kitchen in our %s." % (L(MENU_A(E),"current menu"), L(B("sapanca-kis-restoran"),"article on winter restaurants in Sapanca"))]),
  ("A Summer Night Date: The Open-Air Garden",
   ["On summer evenings Mare Gastro's garden brings together the cool air from the lake, the scent of pine and, at weekends, often live music. For an open-air date we suggest arriving a little before sunset. More in our %s." % L(B("sapanca-yazin-acik-hava-restoran"),"guide to open-air restaurants in summer"),
    "What guests write about the outdoor area confirms this:",
    Q("A very pleasant and peaceful place, outdoors and close to nature.","Ümmühan Tahta",E)]),
  ("5 Questions to Ask When Choosing a Place With Indoor and Outdoor Seating",
   [UL([("Is the same menu served indoors?","In some places the indoor area is just a back-up room. At Mare Gastro the same kitchen serves both areas."),
        ("Can the table be moved if the weather turns?","Mention your preference when you book and the team will adjust your table."),
        ("Is the indoor area good for conversation?","On live-music evenings, ask for a table away from the stage."),
        ("Can the outdoor area be used on cool evenings?","On spring and autumn evenings we suggest bringing a cardigan."),
        ("What to do after dinner?","The option of staying at Didi Otel in the same garden makes the evening easier.")], "ol")]),
  ("A Sample Date Programme for a Winter Evening",
   ["In the winter months a date day in Sapanca might look like this: leave Istanbul around midday, enjoy a snowy view towards Kartepe in the afternoon, take a short walk by the lake in the late afternoon and have the chef's warm signature plates in Mare Gastro's indoor dining room in the evening. You can spend the night %s and head back after a lake-view breakfast the next morning." % L(B("sapanca-sevgiliyle-yemek-ve-konaklama"),"at Didi Otel")]),
  ("Why Mare Gastro? The Short Answer",
   [UL([("Two settings, one kitchen:","Open-air garden and indoor dining room."),
        ("Fine dining:","Sapanca's only fine dining restaurant, signed by Executive Chef Doğan Anapa."),
        ("Trust:",'<a href="%s">Rated 4.9 on Google Maps</a> (October 2026).' % MAPS),
        ("Location:","Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, Sapanca/Sakarya (garden of Didi Otel); about 1.5 hours from Istanbul."),
        ("Stay:","You can stay at Didi Otel in the same garden.")])]),
  ("How to Choose Indoor or Outdoor When You Book",
   ["Choose the date, time and party size in the %s and send it on WhatsApp; then simply write “garden” or “indoor dining room” in the same WhatsApp conversation. If the weather changes, our team lets you know and adjusts your table. For a quick question you can write to our %s." % (L(REZ_A(E),"booking form"), L(WA,"WhatsApp line"))]),
 ],
 "faq":[
  ("Which romantic restaurant in Sapanca has indoor seating?","Mare Gastro, in the garden of Didi Otel, has both an open-air garden and an indoor dining room. On cool, rainy and winter evenings guests are served indoors with the same fine dining kitchen."),
  ("Where to go for a date in Sapanca in winter?","Kartepe or the lakeside during the day and a restaurant with an indoor dining room in the evening make a good plan. On winter evenings Mare Gastro serves the chef's warm signature plates indoors."),
  ("Can you dine outdoors at Mare Gastro?","Yes. When the weather allows you can dine in the open-air garden under the pine trees, right next to the lake; at weekends there is often live music."),
  ("What happens to my booking if it rains?","If you booked the garden and the weather turns, the team moves your table to the indoor dining room. Just mention your preference in the WhatsApp conversation where we confirm your booking."),
  ("What is Mare Gastro's Google rating?","As of October 2026 Mare Gastro is rated 4.9 on Google Maps. You can see the current rating and reviews on its Google Maps page."),
 ],
}}

EXTRA["sapanca-alkollu-restoran"] = {E: {
 "cat":"raki","date":"2026-11-07","updated":"2026-11-12","read":"6 min read",
 "img":"ig-imza-kokteyl.webp","alt":"A signature cocktail at the Mare Gastro bar, a restaurant serving alcohol in Sapanca",
 "h1":"A <em>Restaurant Serving Alcohol</em> in Sapanca: Rakı, Wine and Cocktails",
 "title":"Restaurant Serving Alcohol in Sapanca: Rakı, Wine | Mare Gastro",
 "desc":"Looking for a restaurant in Sapanca that serves alcohol? Mare Gastro has 31 rakı options, 32 wines, champagne and 12 signature cocktails, a garden and weekend live music.",
 "kw":"sapanca restaurant alcohol, sapanca bar restaurant, sapanca cocktails, sapanca wine, sapanca rakı, kırkpınar restaurant",
 "lead":"<strong>Short answer:</strong> for a dinner with drinks in Sapanca, Mare Gastro, in the garden of Didi Otel right next to the lake, serves rakı, wine and cocktails alongside its fine dining kitchen. As of November 2026 the menu lists 31 rakı options, 32 wines, 4 champagnes and sparkling wines and 12 cocktails; weekend evenings come with live music.",
 "body":[
  ("Is There a Restaurant in Sapanca That Serves Alcohol?",
   ["Yes. There are restaurants in Sapanca that serve alcohol; Mare Gastro in Kırkpınar is one of them and serves drinks as part of a dining experience. The restaurant is open Tuesday to Sunday, 09:00–00:00, and closed on Mondays.",
    "The menu ranges from a rakı and fish table to dinner with wine or a cocktail at sunset. For the current list and prices see our %s; the menu is updated with the season." % L(MENU_A(E),"digital menu")]),
  ("What Drinks Are on the Menu?",
   ["The table below was taken from our live menu on 12 November 2026. Different bottle sizes of the same drink (e.g. 20, 35, 50 and 70 cl rakı) are counted as separate options.",
    T(["Category","Options","Examples"],[
      ["Rakı","31","Beylerbeyi Göbek, Sarı Zeybek, Efe Gold, Efe Yaş Üzüm (20–70 cl)"],
      ["Wine","32","Kavaklıdere 1929 Cabernet, Pendore Öküzgözü, Urla Tempus, Egeo Chardonnay (wine by the glass included)"],
      ["Champagne and sparkling","4","Moët & Chandon, Chandon Rosé, Bottega White Gold, Martini Brut"],
      ["Cocktails","12","Kuzu Kulağı Sour, R.R. (rakı, rocket, lemon), Espresso Martini, Whisky Sour"],
      ["Whisky","9","9 options on the menu"],
      ["Liqueur","9","9 options on the menu"],
      ["Gin / Vodka / Tequila / Rum","8 / 6 / 5 / 2","In cocktails and served neat"],
      ["Beer","7","7 options on the menu"]])]),
  ("Is It Good for Rakı and Fish?",
   ["Yes. Mare Gastro's kitchen is seafood-focused and its starters are very close to the meze of a rakı table: hummus, beetroot borani, carrot tarator, Cretan cheese spread, a cheese plate, the artichoke in olive oil of the day and bonito carpaccio among them. Hot appetisers include fried calamari and the Mare Special Islama Calamari.",
    "For meze choices and how to set the table, see our %s." % L(B("sapanca-raki-balik"),"Sapanca rakı and fish guide")]),
  ("What Are the Signature Cocktails?",
   ["Alongside the classics, the cocktail menu has recipes with a local touch. <strong>Kuzu Kulağı Sour</strong> is made with sorrel, and <strong>R.R.</strong> with rakı, rocket and lemon. Espresso Martini, Whisky Sour, Mojito and Margarita are also on the menu, as well as a non-alcoholic cocktail, cold drinks and hot drinks.",
    bfig("ig-kokteyl-serefe.webp","Cheers with signature cocktails at Mare Gastro","Signature cocktails at Mare Gastro")]),
  ("Is There Live Music?",
   ["Weekend evenings come with live music, and guest artists take the stage on special nights. We have collected the summer 2026 programme and current events in our %s." % L(B("sapanca-canli-muzik-mekanlari"),"Sapanca live music guide")]),
  ("Can You Drink Outdoors?",
   ["Yes. Mare Gastro has an open-air garden and an indoor dining room. In summer you are welcomed in the garden, and on cool and rainy days indoors, with the same menu."]),
  ("Can You Stay Over After Drinking?",
   ["Mare Gastro is in the garden of %s. Instead of driving after dinner you can stay at the hotel in the same garden; just mention it in the booking form. Parking is free and valet service is available." % L(DIDIWEB,"Didi Otel")]),
 ],
 "faq":[
  ("Is there a restaurant in Sapanca that serves alcohol?","Yes. Mare Gastro in Kırkpınar is a fine dining restaurant serving rakı, wine, champagne and cocktails; it is open Tuesday to Sunday, 09:00–00:00."),
  ("How many kinds of rakı does Mare Gastro have?","As of November 2026 the menu lists 31 rakı options across different brands and bottle sizes."),
  ("What is on the wine list?","There are 32 options including wine by the glass; Kavaklıdere 1929 Cabernet, Pendore Öküzgözü, Urla Tempus and Egeo Chardonnay are some of them."),
  ("Are there cocktails?","Yes. There are 12 cocktails, including Kuzu Kulağı Sour and R.R. made with rakı, plus a non-alcoholic cocktail."),
  ("Where can I see the prices?","Current prices are in the digital menu at maregastro.com/menu/en."),
 ],
}}

EXTRA["sapanca-canli-muzik-mekanlari"] = {E: {
 "cat":"gece","date":"2026-11-07","read":"6 min read",
 "img":"mare-gece-terasi.webp","alt":"Mare Gastro's terrace at night, a live music venue in Sapanca",
 "h1":"<em>Live Music</em> in Sapanca: Evenings With Music at Mare Gastro",
 "title":"Live Music in Sapanca: Dinner With Live Music | Mare Gastro",
 "desc":"Dinner with live music in Sapanca: live music at Mare Gastro on weekends, guest artists and special nights. Current programme and reservations.",
 "kw":"sapanca live music, live music restaurant sapanca, sapanca music venues, sapanca night out, kırkpınar live music",
 "lead":"<strong>Short answer:</strong> for dinner with live music in Sapanca, Mare Gastro's weekend evenings come with live music, and guest artists take the stage on special nights. In summer 2026, Eda Acar and her orchestra played in the open-air garden on Saturday nights. The current programme is on our Instagram account and in the booking calendar.",
 "body":[
  ("Where Is There Live Music in Sapanca?",
   ["Venues with live music in Sapanca are mostly around the lake and in Kırkpınar. Mare Gastro brings a fine dining kitchen and live music together in the same evening in the garden of Didi Otel: food, cocktails and the stage in one garden.",
    "The restaurant is open Tuesday to Sunday, 09:00–00:00; live-music evenings are usually at weekends."]),
  ("Who Played in Summer 2026?",
   ["The programme below was compiled from posts on the @maregastro Instagram account. Artists and days change with the season; this table shows a past programme.",
    T(["Date","Artist","Note"],[
      ["July 2026, every Thursday","@asyaarslanofficial","Live music on Thursday evenings"],
      ["10 July 2026","Gökçe Erdoğan","21:00"],
      ["July 2026, Saturday nights","Eda Acar and her orchestra","In the open-air garden"],
      ["30 August 2026","@ezgiayce feat. @apigitar","A special night with the chef's set menu"]]),
    V("GiwkPYUSVyY",VT["GiwkPYUSVyY"],"Eda Acar and her orchestra on the Mare Gastro stage",E)]),
  ("Where Can I Find the Current Live Music Programme?",
   ["Artists and special nights are announced on %s. In the %s on our website, days with special events are marked in colour; tap a day to see the details of the event." % (L("https://www.instagram.com/maregastro/","our Instagram account"), L(REZ_A(E),"booking calendar"))]),
  ("Is It Hard to Get a Table on a Live Music Night?",
   ["The number of tables can be limited on special nights. That's why %s for a live-music evening; choosing the date, time and party size and confirming on WhatsApp takes only a few minutes." % L(REZ_A(E),"we recommend booking in advance")]),
  ("What If I Want a Quieter Table?",
   ["Just mention it when you book; our team will try to arrange a quieter corner away from the stage. For an evening for two, also see our %s." % L(B("sapanca-romantik-aksam-yemegi"),"romantic dinner guide")]),
  ("What Happens Besides Music?",
   ["Mare Gastro also hosts events other than music from time to time. For example, in September 2026 there was a workshop on wild mushrooms with mycologist Jilber Barutçiyan (@mushroomsofturkey). Upcoming events appear in the calendar in the booking section."]),
 ],
 "faq":[
  ("Is there a restaurant with live music in Sapanca?","Yes. At Mare Gastro weekend evenings come with live music, and guest artists take the stage on special nights."),
  ("Which days is there live music at Mare Gastro?","Live music is usually on weekend evenings. The current programme is on our Instagram account and in the booking calendar."),
  ("Do I need to book for a live music evening?","Booking in advance is recommended, as the number of tables can be limited on special nights."),
  ("Is the live music outdoors?","In summer the stage is set up in the open-air garden; in cooler weather it continues in the indoor dining room."),
 ],
}}

EXTRA["mare-gastro-imza-tabaklar-nasil-hazirlaniyor"] = {E: {
 "cat":"sef","date":"2026-11-07","read":"8 min read",
 "img":"mare-sofra-detay.webp","alt":"Signature plates from the Mare Gastro table, Chef Doğan Anapa",
 "h1":"How Are Mare Gastro's <em>Signature Plates</em> Made?",
 "title":"Chef Doğan Anapa's Signature Plates and Recipes | Mare Gastro",
 "desc":"Islama calamari, seafood wheat risotto, lamb kokoreç on watermelon salad: Chef Doğan Anapa explains how his signature plates are made, with videos.",
 "kw":"chef doğan anapa recipes, mare gastro signature dish, islama calamari, wheat risotto recipe, lamb kokoreç watermelon salad, sapanca fine dining menu",
 "lead":"<strong>Short answer:</strong> Mare Gastro's signature plates come from Executive Chef Doğan Anapa's way of interpreting the local flavours of Sakarya with Aegean-Mediterranean technique. Islama calamari is inspired by Adapazarı's ıslama köfte, and lamb shank with keşkek by the region's keşkek tradition. Below we summarise six plates in the chef's own words from his videos.",
 "body":[
  ("Mare Special Islama Calamari",
   ["In the chef's words, the idea for the plate comes from Adapazarı's famous ıslama köfte: where the bread for ıslama köfte is soaked in bone broth, here it is soaked in <strong>fish stock</strong>. Grilled baby squid is placed on bread soaked in fish stock and turned in sweet paprika and butter.",
    "It is finished with the chef's own <strong>mint and mustard sauce</strong>, and diced tomato and spring onion for freshness and acidity. As of November 2026 it is on the menu among the hot appetisers as “Mare Special Islama Calamari”.",
    V("YAbVQG4u7LI",VT["YAbVQG4u7LI"],"Chef Doğan Anapa explains islama calamari",E)]),
  ("Seafood Wheat Risotto",
   ["Instead of rice, <strong>whole wheat berries</strong> are used. The wheat is cooked slowly with small shrimp and pieces of baby squid in garlic, parsley and butter and finished with white wine. On top go separately cooked shell-on jumbo prawns and clams.",
    "The chef's choice: the prawns are cooked just enough to stay slightly firm, and instead of parmesan the dish is finished with a local cheese, <strong>aged Thracian kaşar</strong>. It is on the menu among the main courses.",
    V("NybLKER1j_4",VT["NybLKER1j_4"],"Seafood wheat risotto",E)]),
  ("Lamb Kokoreç on a Bed of Watermelon Salad",
   ["To balance the richness of the kokoreç, the plate sits on a salad of tomato, watermelon and basil with a touch of vinegar. On top come pieces of grilled lavash, then kokoreç that is first cooked slowly <strong>in a 160 °C oven</strong> and then turned in butter on the grill.",
    "It is seasoned with cumin, chilli flakes, thyme and salt and served with roasted green pepper. Lamb Kokoreç is on the menu among the main courses.",
    V("enOAIZfhK3s",VT["enOAIZfhK3s"],"Lamb kokoreç on a bed of watermelon salad",E)]),
  ("Grilled Shell-On Tiger Prawns",
   ["The tiger prawns are split in half and cooked in the shell; according to the chef, prawns gain much more flavour inside their shell. The sauce is simple: garlic, butter, salt and parsley. They are served with lime and lemon.",
    "In the video the recipe is prepared together with Kadir Çiçek, Chairman of the Board of Didi Otel. On the menu you'll find “Grilled Jumbo Prawns” and “Prawns in Butter” among the hot appetisers.",
    V("zseYjYW3uFk",VT["zseYjYW3uFk"],"Grilled shell-on prawns with Chef Doğan Anapa and Kadir Çiçek",E)]),
  ("Lamb Shank on Keşkek",
   ["The lamb shank is cooked slowly in a cast-iron pot in the oven at <strong>180 °C for about 2.5–3 hours</strong>, with onion, garlic, dried herbs such as thyme, mint and basil, stock and various acids. The keşkek is made with wheat, chickpeas, onion, chicken and butter; as the chef points out, keşkek is a much-loved dish in Adapazarı.",
    "The plate is finished with the shank's own sauce and mint oil. This dish was on the summer menu; since the menu changes with the season, check the current menu.",
    V("Asn8FZ0nFX0",VT["Asn8FZ0nFX0"],"Lamb shank on keşkek",E)]),
  ("Rock Sea Bass and Karasu Asparagus",
   ["The thick rock sea bass first goes on the grill and then continues cooking in the oven. Under the fish are two “hidden sauces”: one with roasted green pepper, garlic and fennel, and one with vinegar and tarragon. Alongside are oven-roasted potatoes and tomatoes, and on top fresh asparagus from Karasu, basil, pickled onion and lemon.",
    "This plate was also on the summer menu; today you can check the menu for the current fish dishes.",
    V("rhSfnoAOCIg",VT["rhSfnoAOCIg"],"Rock sea bass and Karasu asparagus",E)]),
  ("What Do These Plates Have in Common?",
   ["Three common threads: local produce (Karasu asparagus, aged Thracian kaşar), references to the region's food culture (ıslama, keşkek) and a balance of acidity (vinegar-based sauces, mint oil, tomato). We describe the chef's approach in more detail in %s." % L(B("sef-dogan-anapa-kimdir"),"Who is Chef Doğan Anapa?"),
    "For the current menu see our %s, and for all the videos %s." % (L(MENU_A(E),"digital menu"), L(YT,"our YouTube channel"))]),
 ],
 "faq":[
  ("What are Mare Gastro's signature plates?","Islama calamari, seafood wheat risotto, lamb kokoreç on watermelon salad and grilled shell-on prawns stand out. Lamb shank and rock sea bass were on the summer menu."),
  ("What is islama calamari?","A plate inspired by Adapazarı's ıslama köfte: grilled baby squid on bread soaked in fish stock, with a mint and mustard sauce."),
  ("Which cheese is used in the wheat risotto?","Instead of parmesan, a local cheese is used: aged Thracian kaşar."),
  ("Are these plates always on the menu?","The menu changes with the season. For the current dishes see maregastro.com/menu/en."),
 ],
}}

# ── Google reviews page (TR original is hand-built: blog/mare-gastro-google-yorumlari.html) ──
GMAPS_REVIEWS = MAPS
_REV = [  # (name, en, ar, ru) — real 5-star Google reviews quoted on the TR page, translated
 ("Fikriye Erkan","I found it by chance and came after reading the reviews, and I'm so glad I did! The food, the service and the ambience are excellent, and the live DJ music was wonderful too. We came for our wedding anniversary and I didn't expect this much. Special thanks to Süleyman Bey, who looked after us.",
  "وجدته بالصدفة وجئت بعد قراءة التقييمات، ويا لحسن الحظ! الطعام والخدمة والأجواء ممتازة، وموسيقى الدي جي الحية كانت رائعة أيضًا. جئنا في ذكرى زواجنا ولم أتوقع كل هذا. شكر خاص للسيد سليمان الذي اهتم بنا.",
  "Нашла случайно и пришла, прочитав отзывы, — и очень рада! Еда, сервис и атмосфера отличные, живой DJ тоже был прекрасен. Пришли на годовщину свадьбы, и я не ожидала такого. Отдельное спасибо Сулейману-бею, который о нас заботился."),
 ("Furkan Kavakcı","We went with my wife for our anniversary. The atmosphere and the service are truly wonderful. You definitely have to try the flavour of the dishes and the aroma of the meze. I'll certainly be back soon.",
  "ذهبنا مع زوجتي في ذكرى زواجنا. الأجواء والخدمة رائعة حقًا. يجب أن تجربوا طعم الأطباق ونكهة المقبلات. سأعود قريبًا بالتأكيد.",
  "Ходили с женой на нашу годовщину. Атмосфера и сервис действительно великолепны. Обязательно попробуйте вкус блюд и аромат мезе. Скоро точно вернусь."),
 ("Ardata Girgin","We came for dinner for my wife's birthday. Being at the table looked after by our waiter Muhammed added as much to our evening as the food did. We chose the chef's interpretation dishes and don't regret it at all.",
  "جئنا للعشاء في عيد ميلاد زوجتي. وجودنا على الطاولة التي اهتم بها النادل محمد أضاف إلى أمسيتنا بقدر ما أضافت النكهات. اخترنا أطباق الشيف ولم نندم إطلاقًا.",
  "Пришли на ужин в честь дня рождения жены. Столик, который обслуживал официант Мухаммед, добавил вечеру не меньше, чем сами блюда. Выбрали блюда в авторской интерпретации шефа и ничуть не пожалели."),
 ("Ümmühan Tahta","A very pleasant and peaceful place, outdoors and close to nature. The friendly smile and kind manner of Muhammed Bey, who looked after us, made our experience even better.",
  "مكان ممتع وهادئ جدًا في الهواء الطلق وفي قلب الطبيعة. ابتسامة السيد محمد الذي اهتم بنا ولطفه جعلا تجربتنا أجمل.",
  "Очень приятное и спокойное место на свежем воздухе, в окружении природы. Улыбка и вежливость Мухаммеда-бея, который нас обслуживал, сделали впечатление ещё лучше."),
 ("Yasemin Babadağ","From the welcome to the very last moment, it makes you feel special and crowns the night with a feast for the eyes and the palate. Well done to everyone.",
  "من الاستقبال حتى اللحظة الأخيرة يجعلك تشعر بأنك مميز، ويتوّج الليلة بوليمة للعين والذوق. سلمت أيديكم.",
  "С момента встречи и до последней минуты здесь дают почувствовать себя особенным и венчают вечер праздником и для глаз, и для вкуса. Спасибо за труд."),
 ("Büşra Canbazoğlu","Even though it was our first visit, we fell in love with the atmosphere. This place made our wedding anniversary unforgettable: the setting, presentation, service and music were flawless. The food arrives at your table as a work of art.",
  "رغم أنها زيارتنا الأولى، أُعجبنا بالأجواء كثيرًا. جعل هذا المكان ذكرى زواجنا لا تُنسى: المكان والتقديم والخدمة والموسيقى كانت مثالية. الطعام يصل إليك وكأنه عمل فني.",
  "Хотя это был наш первый визит, мы влюбились в атмосферу. Это место сделало нашу годовщину свадьбы незабываемой: обстановка, подача, сервис и музыка были безупречны. Еда подаётся как произведение искусства."),
 ("Emel Kamsız","As someone who lives in Sapanca, this is one of the places I really love coming to. I leave happy every time, with the food, the atmosphere and the service. Definitely one of my favourites.",
  "بصفتي من سكان سابانجا، هذا من الأماكن التي أحب المجيء إليها حقًا. أغادر راضية في كل مرة بفضل الطعام والأجواء والخدمة. بالتأكيد من أماكني المفضلة.",
  "Я живу в Сапандже, и это одно из мест, куда я по-настоящему люблю приходить. Каждый раз ухожу довольной — и едой, и атмосферой, и сервисом. Определённо одно из любимых мест."),
 ("Rümeysa Aslan","We came for rakı and dinner last night and came back again today for breakfast. A very enjoyable place, the ambience and the music are great. The beef carpaccio was delicious.",
  "جئنا أمس مساءً للراكي والعشاء، وعدنا اليوم للفطور. مكان ممتع جدًا، والأجواء والموسيقى رائعة. كان كارباتشو اللحم لذيذًا جدًا.",
  "Вчера вечером пришли на раки и ужин, а сегодня снова вернулись на завтрак. Очень приятное место, атмосфера и музыка прекрасные. Карпаччо из говядины было очень вкусным."),
 ("İnci Ogan","We came by chance, but both the ambience and the food were excellent. Our waiter Ömer Bey was extremely attentive all evening. If we're ever in Sapanca again, we'll definitely be back.",
  "جئنا بالصدفة، لكن الأجواء والطعام كانا ممتازين. كان النادل السيد عمر مهتمًا جدًا طوال الأمسية. إذا عدنا إلى سابانجا فسنأتي مجددًا بالتأكيد.",
  "Зашли случайно, но и атмосфера, и еда были на высоте. Наш официант Омер-бей был очень внимателен весь вечер. Если снова окажемся в Сапандже, обязательно вернёмся."),
 ("Mert Efe Demir","A very stylish and refined place; we chose it for our anniversary and were very happy. Special thanks to the service team. I recommend the lamb shank.",
  "مكان أنيق وراقٍ جدًا، اخترناه لذكرى زواجنا وكنا سعداء جدًا. شكر خاص لفريق الخدمة. أنصح بموزة الخروف.",
  "Очень стильное и изысканное место; выбрали его на годовщину и остались очень довольны. Отдельное спасибо команде сервиса. Рекомендую баранью голяшку."),
 ("Oylum Genç","It was the best decision of our one-day trip to Sapanca. The food, the cocktails, the staff and the ambience are incredibly good. I recommend it without hesitation.",
  "كان أنجح قرار في رحلتنا ليوم واحد إلى سابانجا. الطعام والكوكتيلات والموظفون والأجواء رائعة بشكل لا يُصدَّق. أنصح به دون تردد.",
  "Это было лучшее решение нашей однодневной поездки в Сапанджу. Еда, коктейли, персонал и атмосфера невероятно хороши. Рекомендую не раздумывая."),
]
_RI = {"en": 1, "ar": 2, "ru": 3}

def _quotes(lang, names):
    return [Q(r[_RI[lang]], r[0], lang) for r in _REV if r[0] in names]

EXTRA["mare-gastro-google-yorumlari"] = {"en": {
 "cat":"hikaye","date":"2026-08-26","read":"5 min read",
 "img":"mare-gece-terasi.webp","alt":"Mare Gastro's terrace at night — what guests say in their Google reviews",
 "h1":"Mare Gastro <em>Google Reviews</em>: What Our Guests Say",
 "title":"Mare Gastro Google Reviews: What Our Guests Say | Mare Gastro",
 "desc":"What guests say in Mare Gastro's Google reviews about the atmosphere, the service team and birthday and anniversary celebrations. Real reviews, translated.",
 "kw":"mare gastro reviews, mare gastro google reviews, sapanca restaurant reviews, mare gastro rating, sapanca fine dining reviews",
 "lead":"The most honest introduction to a restaurant is not the story it tells about itself but what guests write on Google after they leave the table. We looked at Mare Gastro's reviews: real experiences, shared under real names, about the atmosphere, the service team and special-day celebrations. The reviews were written in Turkish; below we quote them in translation.",
 "body":[
  ("Why Look at Google Reviews?",
   ["A venue's photos, menu and its own story are always presented at their best, and that's normal. Google reviews do something different: they leave a record outside the brand's control, written voluntarily by a guest after the meal. When you are looking for a fine dining evening or a place for a special celebration in Sapanca, these reviews are the most reliable way to see whether a restaurant's promise matches what it actually delivers.",
    "In this article we have gathered real examples from the reviews guests posted with their own accounts on Mare Gastro's Google Maps page. No name or text has been made up. Mare Gastro is %s (October 2026)." % L(MAPS,"rated 4.9 on Google Maps")]),
  ("The 3 Things Guests Mention Most",
   ["When you put dozens of reviews side by side, three themes keep coming back:",
    UL([("Atmosphere and setting:","the open-air veranda, the natural surroundings right next to the lake and evenings with live music."),
        ("The service team:","a team that guests thank by name in their reviews, for its personal attention."),
        ("Special occasions:","birthdays and wedding anniversaries, once-in-a-lifetime moments, handled with care.")])] + _quotes("en", ["Ümmühan Tahta"])),
  ("What Guests Say About Birthday and Anniversary Celebrations",
   ["One phrase appears in the reviews far more often than any other: “we came for our anniversary”. Fikriye Erkan, Furkan Kavakcı and Büşra Canbazoğlu all wrote about anniversary evenings:"] + _quotes("en", ["Fikriye Erkan","Furkan Kavakcı","Büşra Canbazoğlu","Mert Efe Demir"]) +
   ["The picture is similar for birthdays:"] + _quotes("en", ["Ardata Girgin"]) +
   ["It shows that Mare Gastro is more than a place to eat: it is an address where the special day itself is designed.",
    bfig("mare-kutlama-kadeh.webp","A celebration moment at Mare Gastro","A celebration moment at Mare Gastro")]),
  ("The Service Team Is Named Again and Again",
   ["One of the clearest signs that a restaurant is really good is whether guests mention staff by name. In Mare Gastro's reviews these names come up again and again: Muhammed Bey is praised for his attention at the welcome and with bookings, Süleyman Bey accompanies guests on special-day celebrations, and Ömer Bey is thanked for explaining the menu dish by dish and answering every question throughout the evening. That's no coincidence: personal attention to every guest is at the heart of Mare Gastro's service."] + _quotes("en", ["İnci Ogan","Yasemin Babadağ"]) +
   [bfig("mare-grup-sofra.webp","An evening table at Mare Gastro","An evening table at Mare Gastro")]),
  ("More From Our Guests",
   _quotes("en", ["Emel Kamsız","Rümeysa Aslan","Oylum Genç"])),
  ("Behind the Kitchen and the Concept: Chef Doğan Anapa and Kadir Çiçek",
   ["Two names stand behind the atmosphere and flavours praised in the reviews. Mare Gastro was created as a concept designed by Kadir Çiçek, with the idea of adding a fine dining experience to the lake's natural setting without disturbing it. At the head of the kitchen is Executive Chef Doğan Anapa, who brought his path from film to the kitchen into the simple, ingredient-led approach of Aegean and Mediterranean cuisine. Phrases that appear often in the reviews, such as “the aroma of the meze”, “beef carpaccio”, “lamb shank” and “the chef's interpretation dishes”, show how this philosophy reaches the table. More in %s." % L(B("sef-dogan-anapa-kimdir"),"Who is Chef Doğan Anapa?")]),
  ("If You Want to See the Reviews Yourself",
   ["This page shows a selection of real 5-star reviews from Mare Gastro's Google Maps page, and we update it as new reviews come in. For the full and most recent list, go straight to %s. You can follow celebration photos on %s and behind-the-scenes posts on %s." % (L(MAPS,"Mare Gastro's Google Maps page"), L("https://www.instagram.com/maregastro/","Instagram"), L("https://www.instagram.com/chefdogananapa/","Chef Doğan Anapa's account")),
    "If you are thinking of celebrating your own special day at Mare Gastro, see our %s or our %s." % (L(B("sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri"),"birthday prices and menu options"), L(B("sapanca-yildonumu-icin-en-iyi-mekan"),"anniversary guide"))]),
 ],
 "faq":[
  ("What is Mare Gastro's Google rating?","As of October 2026 Mare Gastro is rated 4.9 on Google Maps. The current rating and all reviews are on its Google Maps page."),
  ("What do guests praise most in the reviews?","The atmosphere and setting right next to the lake, the service team (often named personally) and the care taken with birthdays and wedding anniversaries."),
  ("Are the reviews on this page real?","Yes. They are real 5-star reviews posted on Mare Gastro's Google Maps page under the guests' own names; on this page they are quoted in translation from Turkish."),
 ],
}}

EXTRA["mare-gastro-google-yorumlari"]["ar"] = {
 "cat":"hikaye","date":"2026-08-26","read":"5 دقائق قراءة",
 "img":"mare-gece-terasi.webp","alt":"شرفة Mare Gastro ليلًا — ماذا يقول الضيوف في تقييمات Google",
 "h1":"تقييمات <em>Google</em> لـMare Gastro: ماذا يقول ضيوفنا؟",
 "title":"تقييمات Google لـMare Gastro: ماذا يقول الضيوف؟ | Mare Gastro",
 "desc":"كيف يصف الضيوف في تقييمات Google الأجواء وفريق الخدمة واحتفالات أعياد الميلاد وذكرى الزواج في Mare Gastro؟ تقييمات حقيقية مترجمة من التركية.",
 "kw":"تقييمات mare gastro, تقييمات google mare gastro, تقييمات مطاعم سابانجا, تقييم mare gastro, آراء الفاين داينينغ سابانجا",
 "lead":"أصدق تعريف بالمطعم ليس القصة التي يرويها عن نفسه، بل ما يكتبه الضيوف على Google بعد مغادرة الطاولة. نظرنا في تقييمات Mare Gastro: تجارب حقيقية بأسماء حقيقية عن الأجواء وفريق الخدمة واحتفالات الأيام الخاصة. كُتبت التقييمات بالتركية، ونقتبسها أدناه مترجمة.",
 "body":[
  ("لماذا تنظر إلى تقييمات Google؟",
   ["صور المكان وقائمته وقصته تُعرض دائمًا في أفضل حالاتها، وهذا طبيعي. أما تقييمات Google فتفعل شيئًا مختلفًا: تترك سجلًا خارج سيطرة العلامة، يكتبه الضيف بإرادته بعد الطعام. عند البحث عن أمسية فاين داينينغ أو مكان لاحتفال خاص في سابانجا، تكون هذه التقييمات أوثق طريقة لمعرفة ما إذا كان وعد المطعم يطابق ما يقدمه فعلًا.",
    "جمعنا في هذا المقال أمثلة حقيقية من تقييمات نشرها الضيوف بحساباتهم على صفحة Mare Gastro في خرائط Google، دون اختلاق أي اسم أو نص. يحمل Mare Gastro %s (أكتوبر 2026)." % L(MAPS,"تقييم 4.9 على خرائط Google")]),
  ("أكثر 3 أشياء يذكرها الضيوف",
   ["عند وضع عشرات التقييمات جنبًا إلى جنب تتكرر ثلاثة مواضيع:",
    UL([("الأجواء والمكان:","الشرفة المفتوحة، والطبيعة بجوار البحيرة مباشرة، والأمسيات مع الموسيقى الحية."),
        ("فريق الخدمة:","فريق يشكره الضيوف بالاسم في تقييماتهم على اهتمامه الشخصي."),
        ("المناسبات الخاصة:","أعياد الميلاد وذكرى الزواج، لحظات لا تتكرر، تُستقبل بعناية.")])] + _quotes("ar", ["Ümmühan Tahta"])),
  ("ماذا يقول الضيوف عن احتفالات عيد الميلاد وذكرى الزواج؟",
   ["عبارة واحدة تتكرر في التقييمات أكثر من غيرها: «جئنا في ذكرى زواجنا». كتب كل من Fikriye Erkan وFurkan Kavakcı وBüşra Canbazoğlu عن أمسيات ذكرى الزواج:"] + _quotes("ar", ["Fikriye Erkan","Furkan Kavakcı","Büşra Canbazoğlu","Mert Efe Demir"]) +
   ["والصورة مشابهة في أعياد الميلاد:"] + _quotes("ar", ["Ardata Girgin"]) +
   ["وهذا يُظهر أن Mare Gastro أكثر من مكان للطعام: إنه عنوان يُصمَّم فيه اليوم الخاص نفسه.",
    bfig("mare-kutlama-kadeh.webp","لحظة احتفال في Mare Gastro","لحظة احتفال في Mare Gastro")]),
  ("أسماء فريق الخدمة تتكرر في التقييمات",
   ["من أوضح العلامات على جودة المطعم أن يذكر الضيوف أسماء العاملين. وفي تقييمات Mare Gastro تتكرر هذه الأسماء: يُمدح السيد محمد على اهتمامه في الاستقبال والحجوزات، ويرافق السيد سليمان الضيوف في احتفالات الأيام الخاصة، ويُشكر السيد عمر على شرحه القائمة طبقًا طبقًا والإجابة عن كل سؤال طوال الأمسية. ليس هذا صدفة: الاهتمام الشخصي بكل ضيف في قلب خدمة Mare Gastro."] + _quotes("ar", ["İnci Ogan","Yasemin Babadağ"]) +
   [bfig("mare-grup-sofra.webp","سفرة مسائية في Mare Gastro","سفرة مسائية في Mare Gastro")]),
  ("المزيد من ضيوفنا",
   _quotes("ar", ["Emel Kamsız","Rümeysa Aslan","Oylum Genç"])),
  ("وراء المطبخ والمفهوم: الشيف Doğan Anapa وKadir Çiçek",
   ["يقف اسمان وراء الأجواء والنكهات التي تُمدح في التقييمات. وُلد Mare Gastro كمفهوم صممه Kadir Çiçek بفكرة إضافة تجربة فاين داينينغ إلى طبيعة البحيرة دون الإخلال بها. وعلى رأس المطبخ الشيف التنفيذي Doğan Anapa، الذي نقل رحلته من السينما إلى المطبخ إلى نهج مطبخ إيجه والمتوسط البسيط القائم على احترام المكونات. والعبارات المتكررة في التقييمات مثل «نكهة المقبلات» و«كارباتشو اللحم» و«موزة الخروف» و«أطباق الشيف» دليل على وصول هذه الفلسفة إلى الطاولة. المزيد في %s." % L(B("sef-dogan-anapa-kimdir"),"من هو الشيف Doğan Anapa؟")]),
  ("إن أردت رؤية التقييمات بنفسك",
   ["تعرض هذه الصفحة مختارات من تقييمات حقيقية بخمس نجوم من صفحة Mare Gastro على خرائط Google، ونحدّثها مع وصول تقييمات جديدة. للقائمة الكاملة والأحدث انتقل مباشرة إلى %s. يمكنك متابعة صور الاحتفالات على %s وكواليس المطبخ على %s." % (L(MAPS,"صفحة Mare Gastro على خرائط Google"), L("https://www.instagram.com/maregastro/","إنستغرام"), L("https://www.instagram.com/chefdogananapa/","حساب الشيف Doğan Anapa")),
    "إن كنت تفكر في الاحتفال بيومك الخاص في Mare Gastro، راجع %s أو %s." % (L(B("sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri"),"أسعار وخيارات قائمة عيد الميلاد"), L(B("sapanca-yildonumu-icin-en-iyi-mekan"),"دليل ذكرى الزواج"))]),
 ],
 "faq":[
  ("ما تقييم Mare Gastro على Google؟","اعتبارًا من أكتوبر 2026 يحمل Mare Gastro تقييم 4.9 على خرائط Google. التقييم الحالي وكل الآراء في صفحته على خرائط Google."),
  ("ما أكثر ما يمدحه الضيوف في التقييمات؟","الأجواء والمكان بجوار البحيرة مباشرة، وفريق الخدمة (الذي يُذكر غالبًا بالاسم)، والعناية بأعياد الميلاد وذكرى الزواج."),
  ("هل التقييمات في هذه الصفحة حقيقية؟","نعم. إنها تقييمات حقيقية بخمس نجوم منشورة على صفحة Mare Gastro في خرائط Google بأسماء أصحابها؛ ونقتبسها هنا مترجمة من التركية."),
 ],
}

EXTRA["mare-gastro-google-yorumlari"]["ru"] = {
 "cat":"hikaye","date":"2026-08-26","read":"5 мин чтения",
 "img":"mare-gece-terasi.webp","alt":"Ночная терраса Mare Gastro — что гости пишут в отзывах Google",
 "h1":"Отзывы о Mare Gastro в <em>Google</em>: что говорят гости",
 "title":"Отзывы о Mare Gastro в Google: что говорят гости | Mare Gastro",
 "desc":"Как гости описывают в отзывах Google атмосферу, команду сервиса и празднование дней рождения и годовщин в Mare Gastro? Реальные отзывы в переводе с турецкого.",
 "kw":"отзывы mare gastro, отзывы google mare gastro, отзывы о ресторанах сапанджи, рейтинг mare gastro, отзывы fine dining сапанджа",
 "lead":"Самая честная рекомендация ресторана — не история, которую он рассказывает о себе, а то, что гости пишут в Google, встав из-за стола. Мы изучили отзывы о Mare Gastro: реальный опыт под реальными именами — об атмосфере, команде сервиса и праздновании особых дней. Отзывы написаны на турецком; ниже мы цитируем их в переводе.",
 "body":[
  ("Зачем смотреть отзывы в Google?",
   ["Фотографии заведения, меню и его собственная история всегда показаны с лучшей стороны — это нормально. Отзывы в Google делают другое: оставляют запись, которую бренд не контролирует и которую гость пишет добровольно после ужина. Если вы ищете вечер высокой кухни или место для особого праздника в Сапандже, эти отзывы — самый надёжный способ понять, совпадает ли обещание ресторана с тем, что он действительно предлагает.",
    "В этой статье мы собрали реальные примеры отзывов, которые гости оставили со своих аккаунтов на странице Mare Gastro в Google Картах. Ни одно имя и ни один текст не придуманы. У Mare Gastro %s (октябрь 2026)." % L(MAPS,"рейтинг 4,9 в Google Картах")]),
  ("3 вещи, о которых гости пишут чаще всего",
   ["Если положить рядом десятки отзывов, постоянно повторяются три темы:",
    UL([("Атмосфера и место:","открытая веранда, природа прямо у озера и вечера с живой музыкой."),
        ("Команда сервиса:","команда, которую гости благодарят по именам за личное внимание."),
        ("Особые события:","дни рождения и годовщины свадьбы — неповторимые моменты, к которым относятся с заботой.")])] + _quotes("ru", ["Ümmühan Tahta"])),
  ("Что гости говорят о праздновании дней рождения и годовщин",
   ["Одна фраза встречается в отзывах чаще всех остальных: «пришли на нашу годовщину». Об этом писали Фикрие Эркан, Фуркан Каваклы и Бюшра Джанбазоглу:"] + _quotes("ru", ["Fikriye Erkan","Furkan Kavakcı","Büşra Canbazoğlu","Mert Efe Demir"]) +
   ["Похожая картина и с днями рождения:"] + _quotes("ru", ["Ardata Girgin"]) +
   ["Это показывает, что Mare Gastro — не просто место, где едят, а адрес, где проектируют сам особый день.",
    bfig("mare-kutlama-kadeh.webp","Момент праздника в Mare Gastro","Момент праздника в Mare Gastro")]),
  ("Имена команды сервиса звучат снова и снова",
   ["Один из самых явных признаков действительно хорошего ресторана — гости называют сотрудников по именам. В отзывах о Mare Gastro эти имена повторяются: Мухаммеда-бея хвалят за внимание при встрече и бронировании, Сулейман-бей сопровождает гостей на праздниках, а Омеру-бею благодарны за то, что весь вечер рассказывал о меню блюдо за блюдом и отвечал на каждый вопрос. Это не случайность: личное внимание к каждому гостю — в центре сервиса Mare Gastro."] + _quotes("ru", ["İnci Ogan","Yasemin Babadağ"]) +
   [bfig("mare-grup-sofra.webp","Вечерний стол в Mare Gastro","Вечерний стол в Mare Gastro")]),
  ("Ещё отзывы наших гостей",
   _quotes("ru", ["Emel Kamsız","Rümeysa Aslan","Oylum Genç"])),
  ("За кухней и концепцией: шеф Доган Анапа и Кадир Чичек",
   ["За атмосферой и вкусами, которые хвалят в отзывах, стоят два имени. Mare Gastro появился как концепция Кадира Чичека — добавить к природе озера опыт высокой кухни, не нарушая её. Во главе кухни — шеф-повар Доган Анапа, перенёсший свой путь из кино на кухню в простой, уважающий продукт подход эгейской и средиземноморской кухни. Часто встречающиеся в отзывах слова — «аромат мезе», «карпаччо из говядины», «баранья голяшка», «блюда в интерпретации шефа» — показывают, как эта философия доходит до стола. Подробнее — в статье %s." % L(B("sef-dogan-anapa-kimdir"),"«Кто такой шеф Доган Анапа?»")]),
  ("Если хотите увидеть отзывы сами",
   ["На этой странице — подборка реальных отзывов с пятью звёздами со страницы Mare Gastro в Google Картах; мы обновляем её по мере появления новых. Полный и самый свежий список — прямо на %s. Фото праздников — в %s, закулисье кухни — в %s." % (L(MAPS,"странице Mare Gastro в Google Картах"), L("https://www.instagram.com/maregastro/","Instagram"), L("https://www.instagram.com/chefdogananapa/","аккаунте шефа Догана Анапы")),
    "Если думаете отметить свой особый день в Mare Gastro, загляните в %s или %s." % (L(B("sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri"),"цены и варианты меню на день рождения"), L(B("sapanca-yildonumu-icin-en-iyi-mekan"),"гид по годовщине"))]),
 ],
 "faq":[
  ("Какой рейтинг у Mare Gastro в Google?","По состоянию на октябрь 2026 года у Mare Gastro рейтинг 4,9 в Google Картах. Актуальный рейтинг и все отзывы — на его странице в Google Картах."),
  ("Что гости хвалят чаще всего?","Атмосферу и место прямо у озера, команду сервиса (часто называя сотрудников по именам) и заботу о днях рождения и годовщинах свадьбы."),
  ("Отзывы на этой странице настоящие?","Да. Это реальные отзывы с пятью звёздами на странице Mare Gastro в Google Картах, оставленные под собственными именами гостей; здесь они приведены в переводе с турецкого."),
 ],
}
