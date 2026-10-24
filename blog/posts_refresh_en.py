# -*- coding: utf-8 -*-
"""EN versions of the 2026-10-24 GEO/AEO refresh (see posts_refresh.py for sourcing rules)."""
from posts_refresh import (L, purl, anchor, table, video, fig, MAPS, DIJITAL, UPDATED,
                           Q_BDAY, Q_ANNIV1, Q_ANNIV2, Q_LOCAL)

LANG = "en"


def q(txt, who):
    return ('<blockquote><p>"%s"</p><p><strong>%s</strong> · %s (translated from Turkish)</p></blockquote>'
            % (txt, who, L(MAPS, "Google review")))


T_BDAY = "We came for dinner on my wife's birthday. Being at the table looked after by our waiter Muhammed added as much to our evening as the food did. We chose the chef's interpretation dishes and have no regrets at all."
T_ANNIV1 = "We went with my wife for our anniversary. The atmosphere and service are truly outstanding. You must try the food and the flavour of the meze. I'll definitely be back as soon as possible."
T_ANNIV2 = "Even though it was our first visit, we fell in love with the atmosphere. This place made our wedding anniversary unforgettable — the setting, presentation, service and music were flawless. The food arrives at your table like art."
T_LOCAL = "As someone who lives in Sapanca, this is one of the places I genuinely love to come back to. I leave happy every time — the food, the atmosphere and the service."

_menu = L(anchor(LANG, "menu"), "our current menu")
_rez = L(anchor(LANG, "reservation"), "reservation form")
_dij = L(DIJITAL, "digital menu")
_g = L(MAPS, "rated 4.9 on Google Maps")

REFRESH = {
"sapanca-en-iyi-dogum-gunu-mekanlari": {
 "updated": UPDATED, "read": "8 min read",
 "title": "Best Birthday Restaurants in Sapanca: 5 Venues Compared (2026) | Mare Gastro",
 "desc": "Where to celebrate a birthday in Sapanca? We compared 5 venues on lake views, atmosphere, group size and food — including Mare Gastro, rated 4.9 on Google.",
 "lead": "Choosing a birthday venue in Sapanca means weighing the view, the atmosphere, your group size and the kitchen together. We compared five of the area's best-known places against those four criteria. Updated 24 October 2026.",
 "body": [
  ("Quick Answer: Where Should You Celebrate a Birthday in Sapanca?", [
   "For an elegant lakeside fine dining birthday, <strong>Mare Gastro</strong> in the garden of Didi Otel (%s); for a lively group night with live music, <strong>Sasa Sapanca</strong>; for a relaxed family table, <strong>Menzara</strong>; for a celebration with children, <strong>Green Blue</strong>; and for nature and activities, <strong>Natürköy</strong>. The right choice depends on the kind of celebration you want." % _g,
  ]),
  ("The 5 Venues at a Glance", [
   table(["Venue", "Known for", "Best for", "Setting"], [
    ["Mare Gastro", "Aegean-Mediterranean cuisine by Executive Chef Doğan Anapa; cake and table decoration on request", "Romantic or elegant birthdays, tables of 2–12", "Lakeside, indoor and outdoor seating"],
    ["Sasa Sapanca", "Broad international menu, live music", "Large groups of friends", "Lakeside"],
    ["Menzara", "Black Sea cuisine, open since 2010", "Relaxed family dinners", "Lake-view balcony"],
    ["Green Blue", "Seafood, children's play area", "Family birthdays with kids", "Large garden"],
    ["Natürköy", "Horse riding, zipline and other activities", "Young groups, daytime celebrations", "Valley and stream-side cabins"],
   ]),
   "This comparison was written on Mare Gastro's own blog; for every venue we only list features that can be verified. Prices and opening hours change, so please confirm them directly with each venue.",
  ]),
  ("What to Look for in a Sapanca Birthday Venue", [
   "There are dozens of restaurants around Lake Sapanca, but not every one suits every celebration. Four criteria matter most:",
   "<ul><li><strong>View:</strong> right on the lake, or garden and nature focused?</li><li><strong>Celebration support:</strong> will the team plan a cake, candles, table decoration or a surprise?</li><li><strong>Group size:</strong> a table for two, or fifteen friends?</li><li><strong>Kitchen:</strong> à la carte fine dining, or a broad casual menu?</li></ul>",
  ]),
  ("1. Mare Gastro — Fine Dining Right by the Lake", [
   "Mare Gastro is a fine dining restaurant on the shore of Lake Sapanca, in the garden of Didi Otel. Executive Chef Doğan Anapa runs an à la carte Aegean-Mediterranean menu, and birthday requests such as a cake or table decoration are planned with the team when you book.",
   fig("mare-kutlama-kadeh.webp", "A birthday celebration at Mare Gastro", "A celebration table at Mare Gastro"),
   "The menu lists 13 starters, 8 warm small plates and 8 main courses (October 2026). Popular choices for birthday tables include the Mare Special Meagre Fish (with beurre blanc), Beef Tenderloin in Pepper Cream Sauce and the signature dessert A Walk in the Forest (chocolate mousse, crispy choux pastry, house-made vanilla ice cream). See every dish on %s." % _menu,
   q(T_BDAY, Q_BDAY[1]),
   "Mare Gastro also hosts live music evenings, and guests regularly mention live music and DJ sets in their reviews. As it is part of Didi Otel, you can stay overnight by the lake after the celebration.",
  ]),
  ("2. Sasa Sapanca — Lakeside with Live Music", [
   "On the lakeshore, Sasa Sapanca offers a broad international menu — meze, burgers, tacos, red meat and fish — with live music. A practical option for hosting a large group with different tastes.",
  ]),
  ("3. Menzara — Black Sea Cuisine and a Balcony View", [
   "Open since 2010, Menzara is known for its lake-view balcony and Black Sea cooking: stone-oven bread, fish and grills. A good fit if you want a warm, homely celebration.",
  ]),
  ("4. Green Blue — A Big Garden for Family Birthdays", [
   "With a seafood-led menu and a large garden, Green Blue stands out for family celebrations with children. The playground gives parents of younger birthday guests some breathing room.",
  ]),
  ("5. Natürköy — An Active Birthday in Nature", [
   "Set in a valley with wooden cabins over a stream, Natürköy is a nature experience rather than fine dining. Worth considering for young groups who want horse riding or zipline as part of the day.",
  ]),
  ("Which One Should You Choose?", [
   "<ul><li><strong>Romantic or elegant evening:</strong> Mare Gastro</li><li><strong>Big, lively night out:</strong> Sasa Sapanca</li><li><strong>Relaxed family table:</strong> Menzara</li><li><strong>Celebration with kids:</strong> Green Blue</li><li><strong>Daytime activities:</strong> Natürköy</li></ul>",
   "Planning a celebration at Mare Gastro? Send your group size and cake or decoration request through the %s. For budgeting, see our guide to %s." % (_rez, L(purl("sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri", LANG), "birthday prices and menu options in Sapanca")),
  ]),
 ],
 "faq": [
  ("What is the best birthday restaurant in Sapanca?", "It depends on the celebration. For a lakeside fine dining birthday, Mare Gastro in the garden of Didi Otel; for a lively group night with live music, Sasa Sapanca; for a family celebration with children, Green Blue."),
  ("Can Mare Gastro arrange a birthday cake or decoration?", "Yes. Share your request when you book and the team will plan the cake and table decoration with you."),
  ("Which Sapanca restaurants have a lake view for a birthday?", "Mare Gastro, Sasa Sapanca and Menzara are on the lakeshore or have lake views; Green Blue and Natürköy are more garden and nature focused."),
  ("Where can a large group of friends celebrate a birthday in Sapanca?", "Sasa Sapanca suits large groups with its broad menu and live music; Mare Gastro suits groups who want a more refined table. Book ahead for larger groups."),
  ("What is Mare Gastro's Google rating?", "Mare Gastro is rated 4.9 on Google Maps as of 24 October 2026. Reviews most often praise the atmosphere, the service and special-occasion arrangements."),
  ("Can I stay overnight in Sapanca after the birthday dinner?", "Yes. Mare Gastro is in the garden of Didi Otel, so you can note an overnight stay on the reservation form."),
 ],
},
"sapanca-yildonumu-icin-en-iyi-mekan": {
 "updated": UPDATED, "read": "8 min read",
 "title": "Best Anniversary Restaurants in Sapanca: 5 Venues Compared (2026) | Mare Gastro",
 "desc": "Where to celebrate a wedding anniversary in Sapanca, near Istanbul? 5 venues compared on lake views, romance and surprise arrangements — with real Google reviews.",
 "lead": "For an anniversary evening, the right venue combines a lake view, a romantic atmosphere and help with surprises. We compared five of Sapanca's best-known places against those criteria. Updated 24 October 2026.",
 "body": [
  ("Quick Answer: Where to Celebrate an Anniversary in Sapanca", [
   "For a romantic, candle-lit anniversary dinner by the lake, <strong>Mare Gastro</strong> (%s); for an evening with live music, <strong>Sasa Sapanca</strong>; for a cosy table, <strong>Menzara</strong>. Couples who want to escape the city entirely can consider <strong>Natürköy</strong> for a quiet day in nature. Sapanca is about 1.5 hours' drive from Istanbul." % _g,
  ]),
  ("The 5 Venues at a Glance", [
   table(["Venue", "Romantic setting", "Surprise support", "Stay overnight"], [
    ["Mare Gastro", "Lakeside, candle-lit, indoor and outdoor seating", "Cake, flowers and table decoration planned when booking", "Part of Didi Otel"],
    ["Sasa Sapanca", "Lakeside, live music", "Ask the venue", "—"],
    ["Menzara", "Lake-view balcony", "Ask the venue", "—"],
    ["Green Blue", "Large garden, family atmosphere", "Ask the venue", "—"],
    ["Natürköy", "Valley, stream-side cabins", "Ask the venue", "Cabin stays"],
   ]),
   "This comparison was written on Mare Gastro's own blog; for the other venues we list only verifiable features and recommend asking them directly about surprise arrangements.",
  ]),
  ("What Makes a Good Anniversary Venue?", [
   "<ul><li><strong>View:</strong> a lake view at sunset does more for an anniversary than anything else.</li><li><strong>Atmosphere:</strong> candlelight and a calm table layout matter for a table for two.</li><li><strong>Surprises:</strong> will the team plan a cake, flowers or a personal note in advance?</li><li><strong>Real guest experience:</strong> what do couples who celebrated there say in their Google reviews?</li></ul>",
  ]),
  ("1. Mare Gastro — A Romantic Table Right by the Lake", [
   "Mare Gastro is a fine dining restaurant on the shore of Lake Sapanca, in the garden of Didi Otel. Cake, flower arrangements and table decoration for anniversaries are planned one by one when you book, and the kitchen is led by Executive Chef Doğan Anapa's Aegean-Mediterranean menu.",
   fig("mare-romantik-kadeh.webp", "A couple toasting by the lake at Mare Gastro", "An anniversary evening at Mare Gastro"),
   "Couples who celebrated their anniversary here mostly mention the atmosphere, the service and the music:",
   q(T_ANNIV2, Q_ANNIV2[1]),
   q(T_ANNIV1, Q_ANNIV1[1]),
   "Popular dishes for a table for two include Bonito Carpaccio, Chilled Jumbo Shrimp with Celeriac Purée, Oven-Baked Sea Bass in Cream Sauce and Circassian Cheese Cheesecake. As Mare Gastro is part of Didi Otel, you can extend the evening with a lakeside stay.",
  ]),
  ("2. Sasa Sapanca — Lakeside with Live Music", [
   "On the lakeshore, Sasa Sapanca offers a broad international menu and live music for a livelier dinner. A practical choice for couples with different tastes.",
  ]),
  ("3. Menzara — Black Sea Cuisine and a Balcony View", [
   "Open since 2010, Menzara's lake-view balcony and Black Sea cooking suit couples looking for a cosier, homely anniversary table.",
  ]),
  ("4. Green Blue — Large Garden, Family Atmosphere", [
   "With a seafood-led menu and a large garden, Green Blue is better suited to family celebrations than to a quiet table for two.",
  ]),
  ("5. Natürköy — A Quiet Celebration in Nature", [
   "With wooden cabins over a stream in a valley, Natürköy offers a nature experience rather than fine dining — an option for couples who want to switch off completely.",
  ]),
  ("Which One Should You Choose?", [
   "If you want a lake view, fine dining, surprise arrangements and an overnight stay in one place, Mare Gastro is the most complete option on this list. For a livelier evening with live music choose Sasa Sapanca, for a cosy table Menzara, and for quiet nature Natürköy.",
   "Send your plans through the %s, and see our guide to %s." % (_rez, L(purl("sapanca-istanbula-yakin-evlilik-teklifi-mekanlari", LANG), "proposal venues near Istanbul")),
  ]),
 ],
 "faq": [
  ("What is the best place to celebrate an anniversary in Sapanca?", "For a romantic lakeside fine dining evening, Mare Gastro in the garden of Didi Otel; for live music, Sasa Sapanca; for a cosy table, Menzara."),
  ("Can Mare Gastro arrange a surprise cake for an anniversary?", "Yes. Share your request when you book and the cake, flowers and table decoration are planned with the team."),
  ("Which romantic restaurants in Sapanca have a lake view?", "Mare Gastro, Sasa Sapanca and Menzara are on the lakeshore or have lake views; Green Blue and Natürköy are garden and nature focused."),
  ("How far is Sapanca from Istanbul?", "Sapanca is about a 1.5-hour drive from Istanbul, which makes it a popular anniversary getaway."),
  ("What is Mare Gastro's Google rating?", "Mare Gastro is rated 4.9 on Google Maps as of 24 October 2026; couples celebrating anniversaries most often praise the atmosphere, service and music."),
  ("Can we stay overnight after an anniversary dinner?", "Yes. Mare Gastro is part of Didi Otel; note your stay on the reservation form."),
 ],
},
"sapanca-fine-dining-fiyat-rehberi": {
 "updated": UPDATED, "read": "6 min read",
 "title": "Fine Dining Prices in Sapanca: What Affects the Bill? (2026) | Mare Gastro",
 "desc": "How much does fine dining cost in Sapanca, what is included per person and where can you see current prices? A transparent 2026 guide from Mare Gastro.",
 "lead": "Price is one of the first questions when planning a fine dining evening in Sapanca. Mare Gastro serves an à la carte menu; here is what shapes the bill and where to see current prices. Updated 24 October 2026.",
 "body": [
  ("Quick Answer: How Much Does Fine Dining Cost in Sapanca?", [
   "The bill for a fine dining evening in Sapanca depends on the dishes you choose, the number of guests, the season and drinks. Mare Gastro has no fixed set menu; you order à la carte, and current dish-by-dish prices are listed on Mare Gastro's %s. Drinks are charged separately." % _dij,
  ]),
  ("5 Things That Shape the Price", [
   table(["Factor", "Effect on the bill", "At Mare Gastro"], [
    ["Dish choice", "The biggest factor", "13 starters, 8 warm small plates, 8 mains, 5 desserts (October 2026)"],
    ["Main ingredient", "Seafood and red meat cost more", "Meagre, jumbo shrimp, beef tenderloin, lamb chops"],
    ["Group size and sharing", "Sharing starters lowers the per-person cost", "Starters can be ordered for the table"],
    ["Drinks", "Wine and rakı change the bill significantly", "Separate wine, rakı and cocktail lists"],
    ["Season", "The menu changes with the season", "Some dishes leave the menu out of season"],
   ]),
  ]),
  ("What Is Included Per Person?", [
   "A fine dining bill is made up of the dishes you order — usually a starter or shared meze, a main course and a dessert. At Mare Gastro this comes with a table right by the lake, a choice of indoor or outdoor seating and attentive service.",
   "For example, the Mare Special Meagre Fish is 200 g of meagre with roasted baby potatoes, charred green pepper sauce, charred tomato and beurre blanc; the Beef Tenderloin in Pepper Cream Sauce is 200 g of tenderloin with black pepper cream sauce and matchstick fries. Portion weights printed on the menu make value easy to judge in advance.",
  ]),
  ("How to Judge Value for Money", [
   "<ul><li><strong>Portion and ingredients:</strong> dishes with listed weights and ingredients make clear what you pay for.</li><li><strong>Freshness:</strong> with seafood, freshness is the real reason for price differences.</li><li><strong>Setting:</strong> a lakeside table and a quiet garden are part of the experience.</li><li><strong>Guest experience:</strong> check real reviews — Mare Gastro is %s.</li></ul>" % _g,
   q(T_LOCAL, Q_LOCAL[1]),
  ]),
  ("Where Can I See Current Prices?", [
   "Current dish-by-dish prices are listed on Mare Gastro's %s, and the main site shows each dish's ingredients on %s. For large groups or special occasions, contact the team through the %s or WhatsApp." % (_dij, _menu, _rez),
   "To get to know the chef's approach, read %s." % L(purl("sef-dogan-anapa-kimdir", LANG), "Who Is Chef Doğan Anapa?"),
  ]),
 ],
 "faq": [
  ("How much does fine dining cost per person in Sapanca?", "It depends on the dishes, drinks and number of guests. Mare Gastro has an à la carte menu; current dish prices are on its digital menu at maregastro.com/dijitalmenu."),
  ("Does Mare Gastro have a set menu?", "No. There is no fixed set menu; starters, warm small plates, mains and desserts are ordered à la carte."),
  ("Where can I see Mare Gastro's current prices?", "Current dish-by-dish prices are listed on Mare Gastro's digital menu (maregastro.com/dijitalmenu)."),
  ("Are drinks included in the price?", "No. Wine, rakı, cocktails and other drinks are ordered and charged separately."),
  ("Is there a cover charge?", "Cover and service details are confirmed when you book; the team will answer any questions."),
  ("What affects a fine dining bill the most?", "Dish choice is the biggest factor; seafood and red meat mains and your wine choice affect the total most."),
 ],
},
"sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri": {
 "updated": UPDATED, "read": "7 min read",
 "title": "Birthday Dinner Prices & Menu Options in Sapanca (2026) | Mare Gastro",
 "desc": "How much does a birthday dinner cost in Sapanca? Mare Gastro's à la carte menu, dishes for a celebration table, the cake and decoration process and current prices.",
 "lead": "When budgeting a birthday in Sapanca, weigh what a venue offers alongside its price. Here is Mare Gastro's menu structure, dishes suited to a celebration table and how booking works. Updated 24 October 2026.",
 "body": [
  ("Quick Answer: How Much Does a Birthday Dinner Cost in Sapanca?", [
   "It depends on the number of guests, the dishes, drinks and any cake or decoration requests. Mare Gastro has no fixed birthday package: you order from the à la carte menu, and current dish-by-dish prices are on the %s. Cake and decoration are planned separately when you book." % _dij,
  ]),
  ("Menu Options for a Birthday Table", [
   table(["Course", "Good choices for a celebration (October 2026)"], [
    ["Sharing starters", "Beetroot Borani, Carrot Tarator, Spicy Atom Dip with Potato Chips, Hummus, Cheese Plate"],
    ["Warm small plates", "Trio of Seafood Delights, Fried Calamari, Buttered Shrimp"],
    ["Main courses", "Mare Special Meagre Fish, Beef Tenderloin in Pepper Cream Sauce, Lamb Chops, Crispy Salmon"],
    ["Desserts", "A Walk in the Forest, Circassian Cheese Cheesecake, Crispy Pumpkin Dessert, Mare Şekerpare"],
    ["Kids' menu", "Grilled Meatballs, Pasta with Tomato Sauce"],
   ]),
   "For larger tables, ordering starters and warm plates to share and choosing mains individually balances both the budget and the flow of the evening.",
  ]),
  ("What Determines the Price?", [
   "<ul><li><strong>Number of guests:</strong> the biggest factor in the total.</li><li><strong>Dish choice:</strong> seafood and red meat mains raise the bill.</li><li><strong>Drinks:</strong> wine, rakı and cocktails are charged separately.</li><li><strong>Cake and decoration:</strong> confirmed separately when booking.</li><li><strong>Season:</strong> the menu is updated with the seasons.</li></ul>",
  ]),
  ("How Are the Cake and Decoration Arranged?", [
   "When booking, share the number of guests, the date and your cake or table decoration request; the details are finalised with the team. Guest reviews mention this care:",
   q(T_BDAY, Q_BDAY[1]),
   "Birthday evenings can also come with live music — here is one of the live music nights on the Mare Gastro stage.",
   video("GiwkPYUSVyY", "A live music evening at Mare Gastro", LANG),
  ]),
  ("Where Can I Get Current Prices?", [
   "Current dish-by-dish prices are on Mare Gastro's %s. To plan around group size and special requests, contact the team through the %s or WhatsApp." % (_dij, _rez),
   "To compare venues, see %s." % L(purl("sapanca-en-iyi-dogum-gunu-mekanlari", LANG), "the 5 best birthday restaurants in Sapanca"),
  ]),
 ],
 "faq": [
  ("How much does a birthday dinner cost in Sapanca?", "It depends on the number of guests, dishes and drinks. Mare Gastro has an à la carte menu; current dish prices are on its digital menu at maregastro.com/dijitalmenu."),
  ("Does Mare Gastro offer a birthday package?", "No. Instead of a fixed package you order à la carte; cake and decoration requests are planned separately when booking."),
  ("Are cake and decoration included in the price?", "No, cake and decoration requests are discussed and confirmed separately when you book."),
  ("Are drinks included?", "No. Drinks are ordered from the menu and charged separately."),
  ("Is there a kids' menu?", "Yes. The kids' menu includes Grilled Meatballs and Pasta with Tomato Sauce."),
  ("How can I get up-to-date prices?", "See dish prices on the digital menu, and for group plans contact the team through the reservation form or WhatsApp."),
 ],
},
"sef-dogan-anapa-kimdir": {
 "updated": UPDATED, "read": "6 min read",
 "title": "Who Is Chef Doğan Anapa? Which Restaurant Does He Lead? | Mare Gastro",
 "desc": "Who is Chef Doğan Anapa and which restaurant is he chef at today? The cooking philosophy, signature dishes and videos of Mare Gastro's Executive Chef in Sapanca.",
 "lead": "Doğan Anapa is the Executive Chef of Mare Gastro, in the garden of Didi Otel in Sapanca. Here is what to know about where he cooks today, his approach and his signature dishes. Updated 24 October 2026.",
 "body": [
  ("Quick Answer: Who Is Doğan Anapa?", [
   "Doğan Anapa is the Executive Chef of <strong>Mare Gastro</strong>, located in the garden of Didi Otel in Sapanca, Turkey. He leads a seafood-focused Aegean-Mediterranean fine dining kitchen built on fresh, seasonal produce, and is known for a storytelling approach shaped by his background in cinema.",
  ]),
  ("Doğan Anapa at a Glance", [
   table(["", ""], [
    ["Role", "Executive Chef, Mare Gastro"],
    ["Restaurant", "Mare Gastro — Didi Otel garden, Sapanca/Sakarya"],
    ["Cuisine", "Aegean-Mediterranean, seafood-focused, seasonal fine dining"],
    ["Background", "Comes to cooking with a narrative eye shaped by cinema"],
    ["Follow", L("https://www.instagram.com/chefdogananapa/", "@chefdogananapa") + " · " + L("https://www.youtube.com/@maregastro", "Mare Gastro on YouTube")],
   ]),
  ]),
  ("Which Restaurant Is Doğan Anapa Chef At Today?", [
   "Doğan Anapa runs the kitchen of Mare Gastro, in the garden of Didi Otel by Lake Sapanca. He cooks an à la carte menu that, as of October 2026, lists 13 starters, 8 warm small plates and 8 main courses. The concept was created within Didi Otel by Kadir Çiçek.",
  ]),
  ("What Is Doğan Anapa's Cooking Philosophy?", [
   "His kitchen rests on three principles: fresh local produce, seasonality and simple but striking presentation. He takes inspiration from regional food traditions and turns them into fine dining plates. The Mare Special Grilled Baby Calamari, for example, is inspired by Adapazarı's ıslama köfte tradition: grilled baby calamari on bread soaked in fish stock.",
   video("YAbVQG4u7LI", "Chef Doğan Anapa preparing the ıslama calamari", LANG),
  ]),
  ("What Are Doğan Anapa's Signature Dishes?", [
   "<ul><li><strong>Mare Special Meagre Fish:</strong> 200 g meagre, roasted baby potatoes, charred green pepper sauce, charred tomato, beurre blanc.</li><li><strong>Mare Special Grilled Baby Calamari:</strong> three grilled baby calamari, mint and mustard sauce, diced tomato.</li><li><strong>Seafood Wheat Risotto:</strong> jumbo shrimp and clams in garlic butter, aged Thracian kashar cheese.</li><li><strong>Bonito Carpaccio:</strong> garlic vinaigrette, red and spring onion, capers, parsley, dill.</li><li><strong>A Walk in the Forest:</strong> chocolate mousse, crispy choux pastry, house-made vanilla ice cream, strawberry.</li></ul>",
   "The chef walks through his signature plate pairing sea bass with Karasu asparagus:",
   video("rhSfnoAOCIg", "Sea bass with Karasu asparagus", LANG),
   "See the current versions on %s. Guests mention the chef's recommendations in their reviews too:" % _menu,
   q(T_BDAY, Q_BDAY[1]),
  ]),
  ("Doğan Anapa's Culinary Journey", [
   "Doğan Anapa's view of food is shaped by his background in cinema: he composes each plate like a scene and each menu like a story. Read the full story in %s." % L(purl("sef-dogan-anapa", LANG), "Chef Doğan Anapa: From Cinema to the Kitchen"),
   "To taste his dishes, book a table through the %s." % _rez,
  ]),
 ],
 "faq": [
  ("Which restaurant is Doğan Anapa the chef of?", "Doğan Anapa is the Executive Chef of Mare Gastro, in the garden of Didi Otel in Sapanca."),
  ("What is Doğan Anapa's cooking style?", "Seafood-focused Aegean-Mediterranean fine dining built on fresh, local and seasonal produce, with a storytelling approach shaped by his background in cinema."),
  ("What are Doğan Anapa's signature dishes?", "Highlights include the Mare Special Meagre Fish with beurre blanc, Mare Special Grilled Baby Calamari, Seafood Wheat Risotto, Bonito Carpaccio and the A Walk in the Forest dessert."),
  ("Where is Mare Gastro?", "Mare Gastro is at Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, Sapanca/Sakarya, in the garden of Didi Otel on the shore of Lake Sapanca."),
  ("Where can I watch Chef Doğan Anapa's cooking videos?", "Mare Gastro's YouTube channel (@maregastro) publishes videos of the chef preparing signature dishes; follow @chefdogananapa on Instagram."),
 ],
},
}
