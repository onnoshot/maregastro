# -*- coding: utf-8 -*-
"""Mare Gastro blog generator — builds SEO-optimized luxury posts + index + sitemap."""
import json, os, re, html

GTM_HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TVJ7R3TT');</script>
<!-- End Google Tag Manager -->
<!-- dataLayer event helper (GTM) -->
<script>
function trackEvent(name,params){try{window.dataLayer=window.dataLayer||[];window.dataLayer.push(Object.assign({event:name},params||{}));}catch(e){}}
</script>"""

GTM_BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TVJ7R3TT"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

SITE   = "https://maregastro.com"
IG     = "https://www.instagram.com/maregastro/"
IGCHEF = "https://www.instagram.com/chefdogananapa/"
DIDI   = "https://www.instagram.com/didiotel/"
DIDIWEB= "https://sapancadidiotel.com/"
TT     = "https://www.tiktok.com/@maregastro"
YT     = "https://www.youtube.com/@maregastro"
WA     = "https://wa.me/905323540888"
MAIL   = "mailto:info@maregastro.com"
MAPS   = "https://maps.google.com/?cid=7177941338358519695"
OUT    = os.path.dirname(os.path.abspath(__file__))

# internal homepage anchors
MENU="%s/tr/#menu"%SITE; REZ="%s/tr/#reservation"%SITE; STORY="%s/tr/#story"%SITE; CHEF="%s/tr/#chef"%SITE; LOC="%s/tr/#contact"%SITE

def L(url,txt): return '<a href="%s">%s</a>'%(url,txt)
def post_url(slug): return "%s/blog/%s.html"%(SITE,slug)
def bfig(img,alt,caption):
    return ('<figure class="bbody-fig"><img src="../images/%s" alt="%s" loading="lazy">'
            '<figcaption>%s</figcaption></figure>'%(img,html.escape(alt),html.escape(caption)))

# ── SVG social icons ──
IC_IG  ='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>'
IC_WA  ='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.46-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.21-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.62.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.27-.2-.57-.35M12.05 21.78h-.01a9.87 9.87 0 01-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 01-1.51-5.26C2.16 6.89 6.6 2.46 12.05 2.46c2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 012.89 6.99c0 5.45-4.43 9.43-9.88 9.43M20.46 3.49A11.82 11.82 0 0012.05.06C5.5.06.16 5.4.16 11.95c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 005.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.16-3.48-8.42"/></svg>'
IC_MAIL='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'
IC_TT  ='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M16.6 5.82A4.28 4.28 0 0115.54 3h-3.09v12.4a2.59 2.59 0 01-2.59 2.5c-1.42 0-2.6-1.16-2.6-2.6 0-1.72 1.66-3.01 3.37-2.48V9.66c-3.45-.46-6.47 2.22-6.47 5.64 0 3.33 2.76 5.7 5.69 5.7 3.14 0 5.69-2.55 5.69-5.7V9.01a7.35 7.35 0 004.3 1.38V7.3s-1.88.09-3.24-1.48z"/></svg>'
IC_YT  ='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2a3.02 3.02 0 00-2.12-2.14C19.51 3.5 12 3.5 12 3.5s-7.51 0-9.38.56A3.02 3.02 0 00.5 6.2 31.6 31.6 0 000 12a31.6 31.6 0 00.5 5.8 3.02 3.02 0 002.12 2.14C4.49 20.5 12 20.5 12 20.5s7.51 0 9.38-.56a3.02 3.02 0 002.12-2.14A31.6 31.6 0 0024 12a31.6 31.6 0 00-.5-5.8zM9.75 15.5v-7l6 3.5-6 3.5z"/></svg>'

CATS = {
 "luks":"Lüks Restoran","deniz":"Deniz Ürünleri","finedining":"Fine Dining",
 "sef":"Şefimiz","romantik":"Özel Anlar","rehber":"Sapanca Rehberi",
 "didi":"Didi Otel","kacamak":"Hafta Sonu",
 "kahvalti":"Kahvaltı","mevsim":"Mevsim","kutlama":"Kutlama",
 "raki":"Rakı-Balık","gece":"Gece Açık","manzara":"Göl Kenarı",
 "kurumsal":"Kurumsal Etkinlik","vejetaryen":"Özel Diyet",
 "dogumgunu":"Doğum Günü","sosyal":"Arkadaş Buluşması","hikaye":"Hikayemiz",
}

POSTS = [
{
 "slug":"sapanca-luks-restoran",
 "cat":"luks","date":"2026-05-12","read":"6 dk",
 "img":"patates-terin2.jpg","alt":"Mare Gastro fine dining tabağı — Sapanca lüks restoran",
 "h1":"Sapanca'da Lüks Restoran: <em>Mare Gastro</em> ile Fine Dining",
 "title":"Sapanca'da Lüks Restoran | Mare Gastro Fine Dining",
 "desc":"Sapanca'da lüks restoran mı arıyorsunuz? Didi Otel bahçesinde, gölün hemen yanında fine dining deneyimi sunan Mare Gastro'yu keşfedin. Menü ve rezervasyon.",
 "kw":"sapanca lüks restoran, sapanca fine dining, sapanca gölün hemen yanındaki restoran, sapanca gurme restoran",
 "lead":"Sapanca Gölü'nün durgun sularına bakan, çamların gölgesine sığınmış, Didi Otel'in büyülü bahçesinde bir lüks restoran: Mare Gastro, doğanın sessizliğini fine dining inceliğiyle buluşturuyor.",
 "body":[
  ("Sapanca'da Lüks Restoran Deneyimi Nasıl Olmalı?",
   ["Bir lüks restoran, yalnızca güzel bir tabaktan ibaret değildir. Işığın masaya düşüşü, garsonun adımındaki sessizlik, şarabın bardağa dökülüş anı ve tabaktaki her dokunuşun bir hikâye anlatması gerekir. <strong>Sapanca'da lüks restoran</strong> arayanlar; manzara, hizmet ve gastronomiyi aynı anda en yüksek seviyede sunan bir mekân ararlar.",
    "Mare Gastro tam da bu beklentiyle doğdu. %s, doğayla iç içe bir konumda, sakin ve zarif bir atmosferde misafirlerini ağırlıyor; her detay, unutulmaz bir akşam için titizlikle tasarlanıyor."%L(LOC,"Sapanca'nın kalbinde")]),
  ("Gölün Hemen Yanında, Doğanın İçinde Bir Sofra",
   ["Sapanca'nın en büyülü anı, gün batımında gölün üzerine düşen altın ışıktır. Mare Gastro, Didi Otel'in yemyeşil bahçesinde konumlanarak bu anı doğrudan sofranıza taşır. Çam ağaçları, palmiyeler ve gölün serinliği eşliğinde yenen bir akşam yemeği, sıradan bir öğünden çok daha fazlasıdır.",
    "Bu yüzden Mare Gastro yalnızca bir <strong>Sapanca gölün hemen yanındaki restoran</strong> değil; doğanın ritmiyle uyumlu, dingin bir kaçış noktasıdır."]),
  ("Ege ve Akdeniz'in En Saf Lezzetleri",
   ["Lüks, sadelikte gizlidir. Mare Gastro mutfağı, Ege ve Akdeniz'in en taze malzemelerini sade ama kusursuz tabaklara dönüştürür. Deniz ürünlerinden zeytinyağlılara, ızgaralardan imza tatlılara kadar her tabak, mevsimin ve coğrafyanın hikâyesini anlatır.",
    "Menünün tamamını %s inceleyebilir, gününüze göre değişen taze seçenekleri keşfedebilirsiniz."%L(MENU,"menümüzden")]),
  ("Kadir Çiçek İmzasıyla Tasarlanan Bir Konsept",
   ["Mare Gastro'nun ışığından masasına kadar her detayı, Didi Otel bünyesinde Kadir Çiçek tarafından tasarlandı, planlandı ve büyük bir titizlikle hayata geçirildi. Mutfağın başında ise sinema geçmişini lezzete dönüştüren Yönetici Şef Doğan Anapa var. %s daha yakından tanıyabilirsiniz."%L(STORY,"Hikâyemizi")]),
 ],
 "faq":[
  ("Sapanca'da lüks restoran nerede?","Mare Gastro, Sapanca Gölü kıyısındaki Didi Otel bahçesinde yer alır. Gölün hemen yanında olmasına karşı fine dining deneyimi sunan, doğayla iç içe lüks bir restorandır."),
  ("Mare Gastro hangi günler açık?","Mare Gastro Cuma, Cumartesi ve Pazar günleri 24 saat açıktır. Pazartesi–Perşembe kapalıdır."),
  ("Mare Gastro'da rezervasyon nasıl yapılır?","Web sitesindeki üç adımlı rezervasyon formundan tarih, saat ve kişi sayısını seçerek WhatsApp üzerinden hızlıca rezervasyon oluşturabilirsiniz."),
  ("Mare Gastro İstanbul'a uzak mı?","Sapanca, İstanbul'a yaklaşık 1,5 saat mesafededir; bu da Mare Gastro'yu hafta sonu gurme kaçamakları için ideal kılar."),
 ],
 "rel":["sapanca-deniz-urunleri","sapanca-fine-dining-nedir","sapanca-is-yemegi-kurumsal-davet"],
},
{
 "slug":"sapanca-deniz-urunleri",
 "cat":"deniz","date":"2026-05-16","read":"6 dk",
 "img":"balik-izgara.jpg","alt":"Izgara balık ve deniz ürünleri — Sapanca deniz yemekleri",
 "h1":"Sapanca'da <em>Deniz Ürünleri</em>: Taze Lezzetin Adresi",
 "title":"Sapanca Deniz Ürünleri & Balık | Mare Gastro",
 "desc":"Sapanca'da deniz ürünleri ve taze balık deneyimi: ahtapot, kalamar, karides ve günün balığı. Göl kıyısında, Didi Otel bahçesinde Mare Gastro'da.",
 "kw":"sapanca deniz ürünleri, sapanca deniz yemekleri, sapanca balık restoran, sapanca deniz mahsulleri",
 "lead":"Sapanca'da deniz ürünleri denince akla taze, sade ve özenli tabaklar gelir. Mare Gastro, Ege ve Akdeniz'in deniz mahsullerini göl kıyısının huzuruyla buluşturuyor.",
 "body":[
  ("Sapanca'da Deniz Ürünleri Neden Bu Kadar Sevilir?",
   ["Göl kıyısında, doğanın içinde yenen bir deniz ürünleri sofrası, Sapanca deneyiminin vazgeçilmezidir. Serin bir akşamda, taze bir kalamar tava ya da ızgara ahtapotun keyfi; manzarayla birleştiğinde unutulmaz bir anıya dönüşür.",
    "<strong>Sapanca deniz ürünleri</strong> arayanlar için Mare Gastro, malzemenin tazeliğini ve hazırlanışındaki inceliği bir arada sunar."]),
  ("Mare Gastro'nun İmza Deniz Lezzetleri",
   ["Mare Gastro'nun deniz ürünleri seçkisi, sadeliğin gücüne inanır. Öne çıkan tabaklardan bazıları:",
    "<ul><li><strong>Ahtapot Izgara</strong> — sarımsaklı tereyağlı sos eşliğinde</li><li><strong>Jumbo Karides Izgara</strong> — maydanozlu tereyağı ile</li><li><strong>Kalamar Tava</strong> — tarator sos</li><li><strong>Çıtır Somon</strong> — kuşkonmaz ve hollandaise</li><li><strong>Günün Izgara Balığı</strong> — köz biber, bebek patates, beurre blanc</li></ul>",
    "Tüm deniz ürünleri ve ara sıcaklar için %s göz atabilirsiniz."%L(MENU,"menümüze")]),
  ("Tazelik ve Mevsim: Mutfağın İki Kuralı",
   ["Mare Gastro mutfağında deniz ürünleri günlük olarak seçilir; menü, mevsime ve günün en taze ürününe göre nazikçe değişir. Bu yüzden \"günün balığı\" her ziyarette farklı bir sürpriz olabilir.",
    "Sinema geçmişini lezzete taşıyan Yönetici Şef Doğan Anapa, her tabağı bir hikâye gibi kurgular. %s tanıyın."%L(CHEF,"Şefimizi")]),
  ("Göl Kıyısında Bir Deniz Sofrası",
   ["Sapanca Gölü'nün hemen yanında, Didi Otel'in bahçesinde yenen bir deniz ürünleri sofrası; doğa, lezzet ve huzurun nadir buluşmasıdır. %s konumumuza göz atabilirsiniz."%L(LOC,"Bizi bulmak için")]),
 ],
 "faq":[
  ("Sapanca'da en iyi deniz ürünleri nerede yenir?","Mare Gastro, Sapanca Gölü kıyısındaki Didi Otel bahçesinde taze deniz ürünleri ve fine dining sunar. Ahtapot ızgara, jumbo karides ve günün balığı öne çıkan lezzetlerdir."),
  ("Mare Gastro'da günlük taze balık var mı?","Evet. Menü mevsime ve günün en taze ürününe göre değişir; \"günün ızgara balığı\" her ziyarette farklılık gösterebilir."),
  ("Deniz ürünleri menüsünü nereden görebilirim?","Web sitemizdeki menü bölümünden başlangıçlar, ara sıcaklar ve ana yemekler dahil tüm deniz ürünlerini inceleyebilirsiniz."),
  ("Rezervasyon gerekli mi?","Özellikle hafta sonları için rezervasyon öneririz. Üç adımlı form ile WhatsApp üzerinden kolayca rezervasyon yapabilirsiniz."),
 ],
 "rel":["sapanca-luks-restoran","sapanca-vejetaryen-restoran","sapanca-romantik-aksam-yemegi"],
},
{
 "slug":"sapanca-fine-dining-nedir",
 "cat":"finedining","date":"2026-05-21","read":"7 dk",
 "img":"dana-carpaccio.jpg","alt":"Dana carpaccio — Sapanca fine dining gurme tabak",
 "h1":"Sapanca <em>Fine Dining</em>: Gurme Yemek Kültürü Rehberi",
 "title":"Fine Dining Nedir? Sapanca'da Gurme Yemek | Mare Gastro",
 "desc":"Fine dining nedir, Sapanca'da gurme bir akşam yemeği nasıl olur? Mare Gastro ile fine dining kültürünü, menü mantığını ve rezervasyon detaylarını keşfedin.",
 "kw":"sapanca fine dining, fine dining nedir, gurme restoran sapanca, sapanca gurme yemek",
 "lead":"Fine dining, bir öğünü bir deneyime dönüştürme sanatıdır. Sapanca'da bu sanatı doğanın içinde yaşamak ise apayrı bir ayrıcalıktır.",
 "body":[
  ("Fine Dining Nedir?",
   ["Fine dining; özenle seçilmiş malzeme, ince işçilikli sunum, kusursuz hizmet ve dikkatle kurgulanmış bir atmosferin bir araya geldiği üst düzey yemek deneyimidir. Burada amaç yalnızca doymak değil; tatların, dokuların ve anların bir bütün olarak hatırlanmasıdır.",
    "<strong>Sapanca fine dining</strong> deneyimi, bu inceliğe bir de gölün hemen yanında olması ve doğanın huzurunu ekler."]),
  ("Sapanca'da Fine Dining'i Özel Kılan Ne?",
   ["İyi bir fine dining mekânı, bulunduğu coğrafyayla konuşur. Mare Gastro, Ege ve Akdeniz mutfağının saf lezzetlerini Sapanca'nın doğasıyla harmanlar. Didi Otel'in bahçesinde, gün batımına karşı kurulan bir sofra; tabaktaki inceliği manzarayla taçlandırır.",
    "%s ve %s, bu deneyimin iki temel taşıdır."%(L(MENU,"Menü"),L(STORY,"konseptimiz"))]),
  ("Bir Fine Dining Akşamı Nasıl Geçer?",
   ["İyi kurgulanmış bir akşam; hafif başlangıçlarla açılır, ara sıcaklarla derinleşir, ana yemekle doruğa ulaşır ve imza bir tatlıyla kapanır. Mare Gastro'da her aşama, mevsimin malzemesine ve şefin yorumuna göre özenle planlanır.",
    "Sinema geçmişini mutfağa taşıyan Yönetici Şef Doğan Anapa için her menü, bir hikâye anlatımıdır."]),
  ("Rezervasyon ve Doğru Zamanlama",
   ["Fine dining bir aceleye gelmez. Akşamınızı sakince planlamak için %s öneririz; gün batımı saatleri özellikle büyülüdür."%L(REZ,"önceden rezervasyon")]),
 ],
 "faq":[
  ("Fine dining ne demek?","Fine dining; üst düzey malzeme, ince sunum, kusursuz hizmet ve özenli bir atmosferin bir araya geldiği gurme yemek deneyimidir. Amaç, öğünü unutulmaz bir anıya dönüştürmektir."),
  ("Sapanca'da fine dining restoran var mı?","Evet. Mare Gastro, Sapanca Gölü kıyısındaki Didi Otel bahçesinde Ege ve Akdeniz mutfağıyla fine dining deneyimi sunar."),
  ("Fine dining için kıyafet kuralı var mı?","Mare Gastro rahat-şık bir atmosfere sahiptir. Özel günler için zarif bir tercih deneyiminizi tamamlar, ancak katı bir kıyafet zorunluluğu yoktur."),
  ("Fine dining akşamı için en iyi saat hangisi?","Gün batımı saatleri Sapanca'da en büyülü andır; bu nedenle akşamüstü ve akşam rezervasyonları önerilir."),
 ],
 "rel":["sapanca-luks-restoran","sapanca-fine-dining-fiyat-rehberi","sapanca-romantik-aksam-yemegi"],
},
{
 "slug":"sef-dogan-anapa",
 "cat":"sef","date":"2026-05-26","read":"5 dk",
 "img":"dogansef.jpg","alt":"Şef Doğan Anapa — Mare Gastro Yönetici Şef, Sapanca",
 "h1":"Şef <em>Doğan Anapa</em>: Sinemadan Mutfağa Bir Yolculuk",
 "title":"Şef Doğan Anapa | Mare Gastro Sapanca Şef Restoran",
 "desc":"Sinema geçmişini lezzete dönüştüren Yönetici Şef Doğan Anapa'nın hikâyesi ve Mare Gastro mutfağının felsefesi. Sapanca'da şef imzalı fine dining.",
 "kw":"şef restoran sapanca, doğan anapa, sapanca şef menüsü, mare gastro şef",
 "lead":"Bazı şefler yemek pişirmez; hikâye anlatır. Doğan Anapa, sinemada öğrendiği anlatı sanatını Mare Gastro'nun tabaklarına taşıyor.",
 "body":[
  ("Sinemadan Gelen Bir Anlatıcı",
   ["Doğan Anapa için yemek yapmak, tıpkı film çekmek gibi bir hikâye anlatma biçimidir. Yılların sinema geçmişi, onun tabaklarındaki kompozisyona, ışığa ve duyguya yansır. Her tabak, başı ve sonu olan küçük bir öykü gibidir.",
    "Bu yaklaşım, Mare Gastro'yu bir <strong>şef restoranı</strong> kimliğine taşır: burada menü, bir şefin imzasıyla şekillenir."]),
  ("Yerel Malzeme, Evrensel Dil",
   ["Şef Doğan Anapa, Ege ve Akdeniz'in en saf malzemelerini evrensel bir gastronomi diliyle sunmaya inanır. Köz patlıcandan ahtapot ızgaraya, çıtır somondan imza tatlılara kadar her tabak; sadelik ve özenin dengesini arar.",
    "Mutfağın bütününü %s keşfedebilirsiniz."%L(MENU,"menümüzde")]),
  ("Mare Gastro Mutfağının Felsefesi",
   ["\"Yereli evrensel olarak sunmaya çalışıyorum\" diyen şef, mevsimin ritmini takip eder. Menü sabit değildir; günün en taze ürününe göre nazikçe değişir. Bu da her ziyareti biricik kılar.",
    "Mare Gastro'nun bütün konseptinin Didi Otel bünyesinde Kadir Çiçek tarafından hayata geçirildiğini, %s okuyabilirsiniz."%L(STORY,"hikâyemizden")]),
 ],
 "faq":[
  ("Mare Gastro'nun şefi kim?","Mare Gastro'nun Yönetici Şefi Doğan Anapa'dır. Sinema geçmişini mutfağa taşıyan şef, Ege ve Akdeniz lezzetlerini fine dining inceliğiyle sunar."),
  ("Şef menüsü var mı?","Menü, şefin imzasıyla ve mevsimin malzemesine göre kurgulanır. Günün en taze ürünleri doğrultusunda özel tabaklar sunulabilir."),
  ("Mare Gastro nerede?","Sapanca Gölü kıyısındaki Didi Otel bahçesinde, Sakarya'da yer alır."),
  ("Şef imzalı bir akşam için rezervasyon nasıl yapılır?","Web sitesindeki üç adımlı form ile tarih, saat ve kişi sayısını seçip WhatsApp üzerinden rezervasyon oluşturabilirsiniz."),
 ],
 "rel":["sapanca-fine-dining-nedir","sef-dogan-anapa-kimdir","sapanca-deniz-urunleri"],
},
{
 "slug":"sapanca-romantik-aksam-yemegi",
 "cat":"romantik","date":"2026-05-29","read":"6 dk",
 "img":"levrek-marin2.jpg","alt":"Zarif bir tabak — Sapanca romantik akşam yemeği",
 "h1":"Sapanca'da <em>Romantik Akşam Yemeği</em> için En İyi Mekân",
 "title":"Sapanca Romantik Akşam Yemeği | Mare Gastro Fine Dining",
 "desc":"Yıl dönümü, evlilik teklifi ya da özel bir akşam mı? Sapanca'da romantik akşam yemeği için gölün hemen yanındaki Mare Gastro'da unutulmaz bir deneyim sizi bekliyor.",
 "kw":"sapanca romantik restoran, sapanca romantik akşam yemeği, sapanca özel gün, sapanca evlilik teklifi mekanı",
 "lead":"Mum ışığı, gölün üzerine düşen son ışıklar ve özenle hazırlanmış bir sofra... Sapanca'da romantik bir akşam, doğanın içinde bambaşka bir anlam kazanır.",
 "body":[
  ("Romantik Bir Akşam İçin Doğru Atmosfer",
   ["Romantizm detaylarda gizlidir: ışığın yumuşaklığı, sesin dinginliği ve sofranın zarafeti. Mare Gastro, Didi Otel'in bahçesinde, Sapanca Gölü'ne karşı bu atmosferi doğal olarak sunar. Gün batımı saatleri ise özel anlar için adeta tasarlanmıştır.",
    "Bu yüzden Mare Gastro, <strong>Sapanca'da romantik akşam yemeği</strong> arayanların ilk tercihlerinden biridir."]),
  ("Özel Günler: Yıl Dönümü, Teklif, Kutlama",
   ["Bir yıl dönümü, evlilik teklifi ya da sürpriz bir kutlama; doğru mekânla unutulmaz olur. Mare Gastro'da imza tatlılar ve özenli sunumlar, anınızı taçlandırmak için hazırdır.",
    "Özel bir düzenleme için rezervasyon sırasında bizimle paylaşabilir, planınızı %s netleştirebilirsiniz."%L(REZ,"rezervasyon adımında")]),
  ("İki Kişilik Bir Lezzet Yolculuğu",
   ["Hafif başlangıçlar, taze deniz ürünleri ve imza ana yemeklerle ilerleyen bir akşam; ikili bir gastronomi yolculuğuna dönüşür. %s birlikte keşfedeceğiniz tatları seçebilirsiniz."%L(MENU,"Menümüzden")]),
  ("Konaklamayı da Düşünün",
   ["Akşamı uzatmak isteyenler için Mare Gastro, Didi Otel bünyesinde yer alır; göl kenarında bir gece konaklaması, romantik kaçamağı tamamlar. Rezervasyon formunda konaklama tercihinizi de belirtebilirsiniz."]),
 ],
 "faq":[
  ("Sapanca'da romantik akşam yemeği nerede yenir?","Mare Gastro, Sapanca Gölü kıyısındaki Didi Otel bahçesinde gölün hemen yanındaki, romantik bir fine dining deneyimi sunar; özellikle gün batımı saatleri idealdir."),
  ("Evlilik teklifi için uygun bir mekân mı?","Evet. Atmosferi, konumu ve özenli sunumlarıyla Mare Gastro, evlilik teklifi ve özel kutlamalar için tercih edilen bir mekândır. Özel düzenlemeleri rezervasyonda paylaşabilirsiniz."),
  ("Konaklama imkânı var mı?","Mare Gastro Didi Otel bünyesindedir; göl kenarında konaklayarak akşamınızı uzatabilirsiniz. Rezervasyon formunda konaklama tercihinizi belirtebilirsiniz."),
  ("Romantik bir akşam için en iyi saat hangisi?","Gün batımı saatleri Sapanca'da en büyülü andır ve romantik akşam yemekleri için en çok önerilen zamandır."),
 ],
 "rel":["sapanca-luks-restoran","didi-otel-restoran","sapanca-fine-dining-nedir"],
},
{
 "slug":"sapancada-ne-yenir",
 "cat":"rehber","date":"2026-06-02","read":"7 dk",
 "img":"ahtapot-izgara.jpg","alt":"Ahtapot ızgara — Sapanca'da ne yenir gurme rehberi",
 "h1":"<em>Sapanca'da Ne Yenir?</em> Gurme Bir Hafta Sonu Rehberi",
 "title":"Sapanca'da Ne Yenir? Gurme Hafta Sonu Rehberi | Mare Gastro",
 "desc":"Sapanca'da ne yenir, nerede yemek yenir? Gölün hemen yanında olmasından deniz ürünlerine, gurme bir hafta sonu için Sapanca yemek rehberi ve Mare Gastro önerileri.",
 "kw":"sapanca'da ne yenir, sapanca'da nerede yemek yenir, sapanca yemek, sapanca hafta sonu",
 "lead":"Sapanca'ya gidip de doğru sofrayı bulamadan dönmek olmaz. İşte gölün kıyısında, doğanın içinde gurme bir hafta sonu için kısa ve net bir rehber.",
 "body":[
  ("Sapanca'da Lezzet Coğrafyası",
   ["Sapanca, gölün hemen yanında olması ve doğasıyla yalnızca dinlenmek için değil, iyi yemek için de gidilen bir yerdir. Bölgede deniz ürünlerinden ızgaralara, zeytinyağlılardan tatlılara uzanan zengin bir yelpaze vardır.",
    "Eğer aradığınız sıradan bir öğün değil de bir <strong>deneyim</strong>se, %s göl kıyısındaki fine dining adresidir."%L(SITE,"Mare Gastro")]),
  ("Mutlaka Denenmesi Gereken Tatlar",
   ["Sapanca'da gurme bir gün için öneri listesi:",
    "<ul><li><strong>Taze deniz ürünleri</strong> — ahtapot ızgara, kalamar tava, jumbo karides</li><li><strong>Zeytinyağlılar</strong> — köz patlıcan, zeytinyağlı enginar, semizotu</li><li><strong>Ana yemekler</strong> — çıtır somon, günün ızgara balığı, biber kremalı bonfile</li><li><strong>İmza tatlılar</strong> — yanık cheesecake ve mevsimin sürprizleri</li></ul>",
    "Tüm seçenekleri %s görebilirsiniz."%L(MENU,"menümüzde")]),
  ("Manzara mı, Lezzet mi? İkisi de.",
   ["Sapanca'nın en güzel yanı, manzara ile lezzeti aynı sofrada buluşturabilmesidir. Mare Gastro, Didi Otel'in bahçesinde gölü arka planına alarak bu ikisini bir araya getirir. %s göz atın."%L(LOC,"Konumumuza")]),
  ("Hafta Sonu Planı: Ne Zaman Gitmeli?",
   ["Sapanca her mevsim güzeldir; ancak gün batımı saatleri yıl boyu en büyülü andır. Hafta sonu yoğunluğu için %s öneririz."%L(REZ,"önceden rezervasyon")]),
 ],
 "faq":[
  ("Sapanca'da ne yenir?","Sapanca'da taze deniz ürünleri, ızgaralar, zeytinyağlılar ve gurme tabaklar öne çıkar. Gölün hemen yanındaki fine dining için Mare Gastro, Didi Otel bahçesinde öne çıkan bir adrestir."),
  ("Sapanca'da nerede yemek yenir?","Göl kıyısında pek çok seçenek olsa da, fine dining ve özel bir akşam için Mare Gastro (Didi Otel bahçesi) tercih edilir."),
  ("Sapanca'da hafta sonu rezervasyon gerekir mi?","Hafta sonları yoğun olabilir; bu nedenle önceden rezervasyon yapmanızı öneririz. Üç adımlı formla WhatsApp üzerinden kolayca rezervasyon yapılır."),
  ("Sapanca İstanbul'a ne kadar uzak?","Sapanca, İstanbul'a yaklaşık 1,5 saat mesafededir ve hafta sonu kaçamakları için idealdir."),
 ],
 "rel":["sapanca-deniz-urunleri","sapanca-luks-restoran","istanbula-yakin-luks-restoran"],
},
{
 "slug":"didi-otel-restoran",
 "cat":"didi","date":"2026-06-04","read":"5 dk",
 "img":"header.jpg","alt":"Didi Otel bahçesi ve Mare Gastro — Sapanca",
 "h1":"<em>Didi Otel</em> Bahçesinde Gurme Deneyim: Mare Gastro",
 "title":"Didi Otel Restoran | Sapanca Mare Gastro Fine Dining",
 "desc":"Sapanca Didi Otel bünyesindeki Mare Gastro, gölün hemen yanındaki bahçede fine dining sunar. Didi Otel restoran deneyimi, konaklama ve rezervasyon detayları.",
 "kw":"didi otel restoran, sapanca didi otel, didi otel sapanca, didi otel restoran sapanca",
 "lead":"Sapanca'nın doğayla bütünleşen saklı cennetlerinden Didi Otel; bahçesinde Mare Gastro'yu ağırlayarak konaklamayı gurme bir deneyimle taçlandırıyor.",
 "body":[
  ("Didi Otel ve Mare Gastro: Doğal Bir Uyum",
   ["Didi Otel, Sapanca'nın yemyeşil dokusunda, gölün serinliğiyle iç içe bir kaçış noktasıdır. Mare Gastro ise bu bahçede, doğanın ritmine uygun bir fine dining deneyimi sunar. <strong>Didi Otel restoran</strong> arayanların aradığı incelik, tam da burada başlar.",
    "Mare Gastro'nun konsepti, Didi Otel bünyesinde Kadir Çiçek tarafından tasarlandı ve hayata geçirildi. %s daha fazlasını okuyun."%L(STORY,"Hikâyemizden")]),
  ("Bahçede Bir Akşam: Manzara ve Lezzet",
   ["Palmiyeler, çamlar ve gölün ışığı eşliğinde kurulan bir sofra; Didi Otel bahçesini olağanüstü bir yemek mekânına dönüştürür. Ege ve Akdeniz'in saf lezzetleri, bu doğal sahnede ayrı bir anlam kazanır. %s inceleyebilirsiniz."%L(MENU,"Menüyü")]),
  ("Konakla, Dinlen, Tadını Çıkar",
   ["Didi Otel'de konaklayan misafirler için Mare Gastro, akşamı tamamlayan kusursuz bir duraktır. Göl kenarında bir gece, gurme bir akşam yemeğiyle birleşince Sapanca kaçamağı eksiksiz olur. Rezervasyon formunda konaklama tercihinizi de belirtebilirsiniz."]),
 ],
 "faq":[
  ("Didi Otel'in restoranı hangisi?","Didi Otel bahçesindeki fine dining restoranı Mare Gastro'dur. Gölün hemen yanında olmasına karşı Ege ve Akdeniz mutfağı sunar."),
  ("Mare Gastro Didi Otel'in neresinde?","Mare Gastro, Sapanca'daki Didi Otel'in bahçesinde yer alır; göl kıyısının doğal dokusuyla iç içedir."),
  ("Didi Otel'de konaklayıp restoranda yemek yiyebilir miyim?","Evet. Konaklayan misafirler Mare Gastro'da akşam yemeği deneyimini yaşayabilir; rezervasyon formunda konaklama tercihinizi belirtebilirsiniz."),
  ("Mare Gastro hangi günler açık?","Cuma, Cumartesi ve Pazar günleri 24 saat açıktır; Pazartesi–Perşembe kapalıdır."),
 ],
 "rel":["sapanca-luks-restoran","sapanca-romantik-aksam-yemegi","sapanca-fine-dining-nedir"],
},
{
 "slug":"istanbula-yakin-luks-restoran",
 "cat":"kacamak","date":"2026-06-05","read":"6 dk",
 "img":"bonfile2.jpg","alt":"Biber kremalı bonfile — İstanbul'a yakın lüks restoran Sapanca",
 "h1":"İstanbul'a Yakın <em>Lüks Gastronomi</em> Kaçamağı: Sapanca",
 "title":"İstanbul'a Yakın Lüks Restoran | Sapanca Mare Gastro",
 "desc":"İstanbul'a yakın lüks bir restoran kaçamağı: yaklaşık 1,5 saat mesafedeki Sapanca'da, Didi Otel bahçesinde Mare Gastro ile fine dining. Plan ve rezervasyon.",
 "kw":"istanbul'a yakın restoran, istanbul yakını lüks restoran, sapanca hafta sonu kaçamağı, istanbul'a yakın fine dining",
 "lead":"Şehrin gürültüsünden gurme bir kaçışa: İstanbul'a yalnızca 1,5 saat mesafedeki Sapanca, lüks bir akşam yemeği için en yakın doğa cennetlerinden biri.",
 "body":[
  ("Şehre Yakın, Doğaya Açık",
   ["İstanbul'dan çıkıp kısa sürede bambaşka bir dünyaya adım atmak mümkün. Sapanca, yaklaşık 1,5 saatlik mesafesiyle <strong>İstanbul'a yakın lüks restoran</strong> arayanlar için ideal bir rota sunar. Göl, orman ve dinginlik; hafta sonu kaçamağının zemini olur.",
    "Bu rotanın gastronomik durağı ise %s — Didi Otel bahçesinde, gölün hemen yanındaki fine dining."%L(SITE,"Mare Gastro")]),
  ("Bir Günlük Kaçamak mı, Hafta Sonu mu?",
   ["Sapanca hem tek günlük bir kaçamağa hem de hafta sonu planına uygundur. Gündüz doğada yürüyüş, akşam Mare Gastro'da gurme bir sofra; dengeli ve unutulmaz bir program olur.",
    "Akşamı uzatmak isteyenler Didi Otel'de konaklayabilir; %s konaklama tercihini belirtmeniz yeterli."%L(REZ,"rezervasyon formunda")]),
  ("Lüks Bir Akşam Yemeği Neyi Hak Eder?",
   ["Yolculuğa değer bir akşam; manzara, hizmet ve lezzetin kusursuz buluşmasıdır. Ege ve Akdeniz'in saf tatları, Yönetici Şef Doğan Anapa'nın yorumuyla sofranıza gelir. %s keşfedin."%L(MENU,"Menüyü")]),
  ("Planınızı Önceden Yapın",
   ["Hafta sonu yoğunluğunda yerinizi garantilemek için %s öneririz; gün batımı saatleri özellikle hızlı dolar."%L(REZ,"önceden rezervasyon")]),
 ],
 "faq":[
  ("İstanbul'a yakın lüks bir restoran nerede?","Sapanca, İstanbul'a yaklaşık 1,5 saat mesafededir. Didi Otel bahçesindeki Mare Gastro, gölün hemen yanındaki fine dining ile şehre yakın lüks bir akşam yemeği sunar."),
  ("Sapanca İstanbul'a kaç saat?","Trafik durumuna göre yaklaşık 1,5 saat. Bu da Sapanca'yı hafta sonu kaçamakları için ideal kılar."),
  ("Tek günde gidip dönülür mü?","Evet. Sapanca tek günlük bir kaçamağa uygundur; gündüz doğa, akşam Mare Gastro'da gurme bir sofra ile keyifli bir gün geçirilebilir."),
  ("Konaklamalı bir plan mümkün mü?","Mare Gastro Didi Otel bünyesindedir; göl kenarında konaklayarak hafta sonunuzu uzatabilirsiniz. Rezervasyon formunda konaklama tercihinizi belirtin."),
 ],
 "rel":["sapanca-luks-restoran","sapancada-ne-yenir","didi-otel-restoran"],
},
{
 "slug":"sapanca-evlilik-teklifi",
 "cat":"romantik","date":"2026-06-08","read":"6 dk",
 "img":"levrek-marin.jpg","alt":"Gölün hemen yanındaki romantik masa — Sapanca evlilik teklifi mekanı Mare Gastro",
 "h1":"Sapanca'da <em>Evlilik Teklifi</em>: Gölün Hemen Yanında Unutulmaz An",
 "title":"Sapanca'da Evlilik Teklifi: Gölün Hemen Yanında Mekan | Mare Gastro",
 "desc":"Sapanca'da unutulmaz bir evlilik teklifi mi planlıyorsunuz? Gölün hemen yanındaki romantik masa, sürpriz düzenleme ve fine dining menüyle Mare Gastro'da hayalinizdeki anı yaşayın.",
 "kw":"sapanca evlilik teklifi mekanı, sapanca evlilik teklifi, sapanca sürpriz yemek organizasyonu, sapanca romantik mekan",
 "lead":"Hayatınızın en önemli sorusunu sormak için doğru sahne kadar önemli az şey vardır. Sapanca Gölü'ne karşı, mum ışığında kurulmuş bir masa; bu anı bir ömür boyu anlatacağınız bir hikâyeye dönüştürür.",
 "body":[
  ("Sapanca'da Evlilik Teklifi Nerede Yapılır?",
   ["Sapanca'da gölün hemen yanındaki, fine dining seviyesinde bir evlilik teklifi için öne çıkan adres Didi Otel bahçesindeki Mare Gastro'dur. Çam ağaçlarının arasında, gölün durgun sularına bakan zarif bir masa; sürpriz bir teklif için doğal ve büyüleyici bir sahne sunar.",
    "Şehrin kalabalığından uzakta, doğanın sessizliğiyle çevrili bu atmosfer, anın samimiyetini ve duygusunu olduğu gibi yaşamanıza imkân tanır. %s göz atarak konumumuzu inceleyebilirsiniz."%L(LOC,"İletişim bölümümüze")]),
  ("Teklif İçin En Romantik Atmosfer Nasıl Kurulur?",
   ["En etkileyici teklif anı, gün batımı saatlerinde yaşanır. Gölün üzerine düşen altın ışık, mum ışığıyla birleştiğinde tabloya dönüşür. Bu yüzden teklif planlayan çiftlere akşamüstü rezervasyonunu öneririz.",
    "Mare Gastro'nun sakin ve zarif atmosferi, doğru ışık ve dingin servis anlayışıyla romantizmi destekler. Ayrıntıları %s, planınızı birlikte netleştirebiliriz."%L(REZ,"rezervasyon sırasında bizimle paylaşırsanız")]),
  ("Sürpriz Düzenleme: Pasta, Çiçek ve İmza Tatlılar",
   ["Özel bir teklif için küçük dokunuşlar büyük fark yaratır. Mare Gastro'nun imza tatlıları, anınızı tatlı bir sürprizle taçlandırmak için idealdir; özel bir pasta, çiçek düzenlemesi veya masaya özel bir not gibi taleplerinizi rezervasyon sırasında iletebilirsiniz.",
    "Akşamı bir %s gibi kurgulamak isterseniz, taze deniz ürünleri ve şefin imza tabaklarından oluşan bir akış öneririz. Tüm seçenekleri %s görebilirsiniz."%(L(post_url("sapanca-romantik-aksam-yemegi"),"romantik akşam yemeği"),L(MENU,"menümüzde"))]),
  ("Evlilik Teklifi İçin Ne Zaman Rezervasyon Yapmalı?",
   ["Sürprizin kusursuz olması için en az birkaç gün önceden rezervasyon yapmanızı öneririz; özellikle hafta sonları ve gün batımı saatleri hızlı dolar. Mare Gastro Cuma, Cumartesi ve Pazar günleri açıktır.",
    "Erken planlama, masa yeri ve sürpriz düzenleme için bize hazırlık zamanı tanır. Üç adımlı %s tarih, saat ve kişi sayısını seçip WhatsApp üzerinden hızlıca yerinizi ayırtabilirsiniz."%L(REZ,"rezervasyon formundan")]),
 ],
 "faq":[
  ("Sapanca'da evlilik teklifi için en iyi mekan neresi?","Sapanca'da gölün hemen yanındaki, romantik bir evlilik teklifi için Didi Otel bahçesindeki Mare Gastro öne çıkar. Mum ışığında masa düzeni, gün batımı eşliği ve fine dining menü, teklif anını unutulmaz kılar."),
  ("Evlilik teklifi için sürpriz düzenleme yapılır mı?","Özel pasta, çiçek veya masaya özel dokunuş gibi taleplerinizi rezervasyon sırasında iletebilirsiniz. Mare Gastro ekibi, sürprizinizin sorunsuz ilerlemesi için planı sizinle birlikte hazırlar."),
  ("Teklif için en uygun saat hangisi?","Gün batımı saatleri Sapanca'da en büyülü andır ve evlilik teklifleri için en çok önerilen zamandır. Bu nedenle akşamüstü rezervasyonu idealdir."),
  ("Ne kadar önceden rezervasyon yapmalıyım?","Sürprizin kusursuz olması için en az birkaç gün önceden rezervasyon öneririz. Hafta sonları ve gün batımı saatleri hızlı dolduğu için erken planlama avantaj sağlar."),
 ],
 "rel":["sapanca-romantik-aksam-yemegi","sapanca-yildonumu-yemegi","didi-otel-restoran"],
},
{
 "slug":"sapanca-yildonumu-yemegi",
 "cat":"kutlama","date":"2026-06-10","read":"6 dk",
 "img":"cheesecake.jpg","alt":"İmza tatlı ve mum ışığı — Sapanca yıldönümü yemeği Mare Gastro",
 "h1":"Sapanca'da <em>Yıldönümü Yemeği</em>: Romantik Bir Kutlama Rehberi",
 "title":"Sapanca'da Yıldönümü Yemeği: Romantik Adresler | Mare Gastro",
 "desc":"Evlilik yıldönümünüzü Sapanca'da gölün hemen yanında kutlayın. Mum ışığında akşam yemeği, özel menü ve sürpriz dokunuşlarla Mare Gastro'da unutulmaz bir gece.",
 "kw":"sapanca yıldönümü yemeği, sapanca yıldönümü kutlama, sapanca romantik akşam yemeği, sapanca özel gün restoran",
 "lead":"Bir yıldönümü, paylaşılan zamanın kutlamasıdır. Sapanca'nın gölü, çamları ve dingin atmosferi; bu kutlamayı sıradan bir akşamdan çıkarıp anlamlı bir anıya dönüştürür.",
 "body":[
  ("Yıldönümü İçin Sapanca Neden İdeal?",
   ["Sapanca, İstanbul'a yaklaşık 1,5 saat mesafede olmasına rağmen bambaşka bir dünyaya açılır; bu yüzden yıldönümü gibi özel günler için ideal bir kaçamak noktasıdır. Gölün hemen yanında olması, doğanın huzuru ve fine dining inceliği bir araya gelince kutlama kendiliğinden özel olur.",
    "Mare Gastro, Didi Otel bahçesinde bu üç unsuru tek sofrada buluşturur. %s planınızı hafta sonu bir kaçamağa da dönüştürebilirsiniz."%L(post_url("istanbula-yakin-luks-restoran"),"İstanbul'a yakın bir rota olarak")]),
  ("Yıldönümü Yemeği İçin En İyi Mekan Hangisi?",
   ["Yıldönümü için ideal mekan; konumu, hizmeti ve mutfağıyla anı taçlandıran bir yer olmalıdır. Mare Gastro, gölün hemen yanında mum ışığında bir masa, taze deniz ürünleri ve şefin imza tabaklarıyla bu beklentiyi karşılar.",
    "Sinema geçmişini mutfağa taşıyan %s için her menü bir hikâye anlatımıdır; yıldönümünüz de bu hikâyenin özel bir bölümü olur."%L(CHEF,"Yönetici Şef Doğan Anapa")]),
  ("Sürpriz Pasta ve Özel Dokunuşlar Ayarlanır mı?",
   ["Özel bir pasta, masaya küçük bir sürpriz ya da imza bir tatlı; yıldönümünü kutlamanın en güzel yollarındandır. Bu tür taleplerinizi rezervasyon sırasında paylaşırsanız, akşamınız için gereken hazırlığı yapabiliriz.",
    "İmza tatlılarımız ve mevsimin sürprizleri için %s göz atabilirsiniz."%L(MENU,"menümüze")]),
  ("İstanbul'dan Yıldönümü İçin Sapanca'ya Gelmeye Değer mi?",
   ["Kesinlikle. Şehirden kısa bir sürede çıkıp göl kıyısında bir akşam geçirmek, yıldönümüne hak ettiği özel çerçeveyi verir. Akşamı uzatmak isteyenler Didi Otel'de konaklayarak kaçamağı tamamlayabilir.",
    "Konaklama tercihinizi de %s belirtebilir, gününüzü baştan sona planlayabilirsiniz."%L(REZ,"rezervasyon formunda")]),
 ],
 "faq":[
  ("Sapanca'da yıldönümü yemeği nerede yenir?","Sapanca'da gölün hemen yanındaki, romantik bir yıldönümü yemeği için Didi Otel bahçesindeki Mare Gastro öne çıkar. Mum ışığı, taze deniz ürünleri ve fine dining menü kutlamayı özel kılar."),
  ("Yıldönümü için sürpriz pasta ayarlanabilir mi?","Evet. Özel pasta veya masaya küçük sürpriz gibi taleplerinizi rezervasyon sırasında paylaşabilirsiniz; ekibimiz gerekli hazırlığı yapar."),
  ("Mare Gastro hangi günler açık?","Mare Gastro Cuma, Cumartesi ve Pazar günleri 24 saat açıktır; Pazartesi–Perşembe kapalıdır."),
  ("Yıldönümü akşamı konaklama mümkün mü?","Mare Gastro Didi Otel bünyesindedir; göl kenarında konaklayarak akşamınızı uzatabilirsiniz. Konaklama tercihinizi rezervasyon formunda belirtebilirsiniz."),
 ],
 "rel":["sapanca-ozel-gun-kutlama","sapanca-dogum-gunu-nerede-kutlanir","sapanca-romantik-aksam-yemegi"],
},
{
 "slug":"sapanca-gol-manzarali-kahvalti",
 "cat":"kahvalti","date":"2026-06-12","read":"6 dk",
 "img":"ezine-peyniri.jpg","alt":"Zengin kahvaltı sofrası — Sapanca gölün hemen yanındaki kahvaltı Mare Gastro",
 "h1":"Sapanca'da <em>Gölün Hemen Yanında Kahvaltı</em>: Güne Huzurlu Bir Başlangıç",
 "title":"Sapanca'da Gölün Hemen Yanında Kahvaltı Nerede? | Mare Gastro",
 "desc":"Sapanca'da gölün hemen yanındaki kahvaltı arayanlar için rehber. Didi Otel bahçesinde taze, zengin bir sofra ile güne huzurlu ve lezzetli bir başlangıç yapın.",
 "kw":"sapanca gölün hemen yanındaki kahvaltı, sapanca kahvaltı mekanları, sapanca serpme kahvaltı, didi otel kahvaltı",
 "lead":"Sapanca'da günün en güzel hâli, gölün üzerinde sabah sisinin dağıldığı andır. Bu manzaraya karşı kurulan zengin bir kahvaltı sofrası, hafta sonu kaçamağının en keyifli ritüelidir.",
 "body":[
  ("Sapanca'da En İyi Gölün Hemen Yanında Kahvaltı Nerede?",
   ["Sapanca'da gölün hemen yanındaki, sakin ve zarif bir kahvaltı için Didi Otel bahçesindeki Mare Gastro öne çıkar. Çamların gölgesinde, gölün serinliğiyle iç içe bir sofra; güne huzurlu bir başlangıç yapmak isteyenler için idealdir.",
    "Doğanın içinde, kalabalıktan uzak bir ortamda kahvaltı etmek isteyenler için %s konumumuza göz atabilirsiniz."%L(LOC,"Sapanca'nın bu sakin köşesinde")]),
  ("Kahvaltı Sofrasında Neler Öne Çıkar?",
   ["Mare Gastro mutfağının tazelik ve mevsim ilkesi kahvaltıya da yansır. Sofranın öne çıkan unsurları arasında yöresel peynirler ve zeytinyağlı dokunuşlar bulunur:",
    "<ul><li><strong>Ege otları</strong> ve mevsim yeşillikleri</li><li><strong>Ezine peyniri</strong> ve yöresel kahvaltılıklar</li><li><strong>Zeytinyağlılar</strong> — köz patlıcan, semizotu, enginar</li><li><strong>Taze ekmek</strong> ve ev yapımı eşlikçiler</li></ul>",
    "Mevsime göre değişen taze seçenekler için %s inceleyebilirsiniz."%L(MENU,"menümüzü")]),
  ("Kahvaltı İçin Rezervasyon Gerekir mi?",
   ["Özellikle hafta sonları gölün hemen yanındaki masaların hızlı dolması nedeniyle önceden rezervasyon öneririz. Sabahın erken saatleri, sofranızı manzaranın en sakin hâliyle birleştirir.",
    "Üç adımlı %s tarih, saat ve kişi sayısını seçerek WhatsApp üzerinden kolayca yer ayırtabilirsiniz."%L(REZ,"rezervasyon formundan")]),
  ("Kahvaltıdan Akşam Yemeğine Bir Sapanca Günü",
   ["Sapanca'da bir gün; gölün hemen yanındaki bir kahvaltıyla başlayıp doğada bir yürüyüşle devam edebilir, akşam ise fine dining bir sofrayla taçlanabilir. Mare Gastro her iki uçta da yanınızdadır.",
    "Akşam programı için %s göz atabilir, gününüzü baştan sona planlayabilirsiniz."%L(post_url("sapancada-ne-yenir"),"Sapanca'da ne yenir rehberimize")]),
 ],
 "faq":[
  ("Sapanca'da gölün hemen yanındaki kahvaltı nerede yapılır?","Sapanca'da gölün hemen yanındaki, sakin bir kahvaltı için Didi Otel bahçesindeki Mare Gastro öne çıkar. Çamların gölgesinde, göle karşı zengin bir sofra sunar."),
  ("Kahvaltı için rezervasyon gerekli mi?","Hafta sonları gölün hemen yanındaki masalar hızlı dolduğu için önceden rezervasyon önerilir. Üç adımlı form ile WhatsApp üzerinden kolayca yer ayırtabilirsiniz."),
  ("Kahvaltıda hangi lezzetler öne çıkar?","Ege otları, yöresel peynirler, zeytinyağlılar ve taze ekmek öne çıkar. Menü mevsime ve günün taze ürününe göre değişir."),
  ("Mare Gastro kahvaltı için hangi günler açık?","Mare Gastro Cuma, Cumartesi ve Pazar günleri hizmet verir; bu günlerde gölün hemen yanındaki bir kahvaltı deneyimi mümkündür."),
 ],
 "rel":["didi-otel-restoran","sapancada-ne-yenir","sapanca-gun-batimi-restoran"],
},
{
 "slug":"sapanca-hafta-sonu-rotasi",
 "cat":"kacamak","date":"2026-06-13","read":"7 dk",
 "img":"bonfile.jpg","alt":"Gurme ana yemek — Sapanca hafta sonu rotası ve akşam yemeği Mare Gastro",
 "h1":"Sapanca <em>Hafta Sonu Rotası</em>: Maşukiye, Kartepe ve Bir Akşam Yemeği",
 "title":"Sapanca Hafta Sonu Rotası: Gezi ve Gurme Plan | Mare Gastro",
 "desc":"Maşukiye, Kartepe ve göl kıyısını kapsayan bir Sapanca hafta sonu rotası. Gün gün gezi planı ve gölün hemen yanındaki bir akşam yemeğiyle Mare Gastro'da kusursuz kaçamak.",
 "kw":"sapanca hafta sonu rotası, sapanca gezi rehberi, maşukiye kartepe gezi, istanbul'a yakın hafta sonu kaçamağı",
 "lead":"Sapanca'yı bir hafta sonuna sığdırmak mümkün; üstelik göl, orman ve zirve manzarasını aynı rotada birleştirerek. İşte gezilecek yerleri gurme bir akşam yemeğiyle taçlandıran net bir plan.",
 "body":[
  ("Sapanca Hafta Sonu Rotası Nasıl Olmalı?",
   ["İdeal bir Sapanca hafta sonu; göl çevresi, Maşukiye'nin dere boyu doğası ve Kartepe'nin zirve manzarasını kapsar, akşam ise göl kıyısında fine dining bir sofrayla kapanır. Bu üçlü, doğa ve lezzeti dengeli biçimde bir araya getirir.",
    "Rotanın gastronomik durağı %s; Didi Otel bahçesinde gölün hemen yanındaki bir akşam yemeği için ideal noktadır."%L(SITE,"Mare Gastro")]),
  ("1. Gün: Göl Çevresi ve Maşukiye",
   ["İlk gün Sapanca Gölü çevresinde başlayın; göl kenarında yürüyüş ve fotoğraf molalarının ardından Maşukiye'nin dere boyu yeşilliğine geçin. Öğleden sonra doğayla iç içe dinlendiren bir programdır.",
    "Akşam ise göl kıyısına dönüp Mare Gastro'da taze deniz ürünleri ve şefin imza tabaklarından oluşan bir sofrayla günü kapatabilirsiniz. %s inceleyebilirsiniz."%L(MENU,"Menümüzü")]),
  ("2. Gün: Kartepe Zirvesi ve Gölün Hemen Yanında Kapanış",
   ["İkinci gün Kartepe'ye çıkıp zirve manzarasının tadını çıkarın; yaz aylarında yeşil yaylalar, kış aylarında kar manzarası eşlik eder. Dönüşte göl kıyısında dingin bir mola iyi gelir.",
    "Akşam yemeğini yine gölün hemen yanında planlamak isterseniz, %s gün batımı saatleri özellikle büyülüdür."%L(post_url("sapanca-gun-batimi-restoran"),"gün batımında gölün hemen yanındaki bir sofrada")]),
  ("İstanbul'dan Sapanca'ya Ulaşım ve Planlama",
   ["Sapanca, İstanbul'a yaklaşık 1,5 saat mesafededir; bu da onu hem günübirlik hem de hafta sonu kaçamakları için ideal kılar. Hafta sonu yoğunluğunda akşam yemeği masanızı önceden ayırtmanızı öneririz.",
    "Üç adımlı %s tarih ve saatinizi seçip yerinizi garantileyebilirsiniz."%L(REZ,"rezervasyon formundan")]),
 ],
 "faq":[
  ("Sapanca hafta sonu için kaç gün yeterli?","İki gün, Sapanca Gölü çevresi, Maşukiye ve Kartepe'yi rahatça kapsamak için yeterlidir. Akşamları gölün hemen yanındaki bir yemekle programı taçlandırabilirsiniz."),
  ("Sapanca, Maşukiye ve Kartepe aynı rotada gezilir mi?","Evet. Üçü birbirine yakındır ve bir hafta sonuna rahatça sığar. Göl çevresi ve Maşukiye'yi bir güne, Kartepe zirvesini diğer güne ayırmak dengeli bir plandır."),
  ("Sapanca İstanbul'a ne kadar uzak?","Sapanca, İstanbul'a yaklaşık 1,5 saat mesafededir ve hem günübirlik hem hafta sonu kaçamakları için idealdir."),
  ("Hafta sonu akşam yemeği için rezervasyon gerekir mi?","Hafta sonları yoğun olabilir; bu nedenle önceden rezervasyon öneririz. Üç adımlı form ile WhatsApp üzerinden kolayca yer ayırtabilirsiniz."),
 ],
 "rel":["istanbula-yakin-luks-restoran","sapancada-ne-yenir","sapanca-gun-batimi-restoran"],
},
{
 "slug":"sapanca-kis-restoran",
 "cat":"mevsim","date":"2026-06-15","read":"6 dk",
 "img":"karides-kremali.jpg","alt":"Sıcak kremalı tabak — Sapanca'da kışın gölün hemen yanındaki restoran Mare Gastro",
 "h1":"Sapanca'da <em>Kışın</em> Nereye Gidilir? Gölün Hemen Yanında Sıcak Bir Sofra",
 "title":"Sapanca'da Kışın Gölün Hemen Yanında Restoran | Mare Gastro",
 "desc":"Sapanca'da kışın gölün hemen yanında, sıcak bir gurme deneyimi mi arıyorsunuz? Gölün hemen yanındaki Mare Gastro'da kış atmosferi ve huzurlu bir akşam sizi bekliyor.",
 "kw":"sapanca kışın gölün hemen yanındaki restoran, sapanca kışın açık restoran, sapanca gölün hemen yanındaki mekan, sapanca kışın nereye gidilir",
 "lead":"Kışın Sapanca, bambaşka bir dinginliğe bürünür; gölün üzerine inen sis, çamların üzerindeki kar ve sıcak bir sofranın buğusu... Soğuk mevsim, doğayla iç içe bir akşam yemeği için en şiirsel zamandır.",
 "body":[
  ("Sapanca'da Kışın Restoranlar Açık mı?",
   ["Evet. Mare Gastro, Didi Otel bahçesinde kış aylarında da Cuma, Cumartesi ve Pazar günleri misafirlerini ağırlar. Kış, gölün hemen yanında olmasının en sakin ve etkileyici hâlini sunduğu için akşam yemeği deneyimini daha da özel kılar.",
    "Soğuk havada doğanın içinde sıcak bir sofra arayanlar için %s konumumuza göz atabilirsiniz."%L(LOC,"göl kıyısındaki")]),
  ("Kışın Gölün Hemen Yanında Yemek İçin En İyi Yer Neresi?",
   ["Kış aylarında gölün hemen yanındaki bu konum, Mare Gastro'nun camlarından adeta bir tabloya dönüşür. Doğanın bu sakin hâline karşı, sıcak ve özenli bir menüyle geçirilen akşam; kışın en keyifli ritüellerinden biridir.",
    "Kartepe'de kar ve kayak sonrası dingin bir akşam yemeği planlayanlar için de göl kıyısı ideal bir duraktır. %s rotanıza ekleyebilirsiniz."%L(post_url("sapanca-hafta-sonu-rotasi"),"Hafta sonu rotamızı")]),
  ("Kış Sofrasında Hangi Lezzetler Öne Çıkar?",
   ["Mare Gastro mutfağı mevsimin ritmini takip eder; kış aylarında sıcak, doyurucu ve özenli tabaklar öne çıkar. Kremalı deniz ürünleri, ızgaralar ve sıcak başlangıçlar, soğuk havaya eşlik eden lezzetlerdir.",
    "Mevsime göre değişen güncel seçenekleri %s görebilir, dilerseniz %s tanıyabilirsiniz."%(L(MENU,"menümüzde"),L(CHEF,"şefimizi"))]),
  ("Kışın Rezervasyon Önemli mi?",
   ["Kış aylarında gölün hemen yanındaki masalar, özellikle hafta sonları ve özel günlerde hızlı dolar. Sıcak ve dingin bir akşam için önceden rezervasyon yapmanızı öneririz.",
    "Üç adımlı %s tarih ve saatinizi seçip yerinizi ayırtabilirsiniz."%L(REZ,"rezervasyon formundan")]),
 ],
 "faq":[
  ("Sapanca'da kışın açık restoran var mı?","Evet. Mare Gastro, Didi Otel bahçesinde kış aylarında da Cuma, Cumartesi ve Pazar günleri hizmet verir ve gölün hemen yanındaki sıcak bir akşam yemeği sunar."),
  ("Sapanca'da kışın gölün hemen yanında yemek nerede yenir?","Gölün hemen yanındaki, Didi Otel bahçesindeki Mare Gastro kışın en etkileyici akşam yemeği adreslerinden biridir."),
  ("Kış menüsünde neler öne çıkar?","Kış aylarında kremalı deniz ürünleri, ızgaralar ve sıcak başlangıçlar öne çıkar. Menü mevsime ve günün taze ürününe göre değişir."),
  ("Kışın rezervasyon gerekir mi?","Gölün hemen yanındaki masalar kış aylarında da hızlı dolduğu için, özellikle hafta sonları önceden rezervasyon önerilir."),
 ],
 "rel":["sapanca-yilbasi-yemegi","sapanca-yazin-acik-hava-restoran","sapanca-luks-restoran"],
},
{
 "slug":"sapanca-yilbasi-yemegi",
 "cat":"mevsim","date":"2026-06-17","read":"6 dk",
 "img":"dana-carpaccio2.jpg","alt":"Şık fine dining tabağı — Sapanca yılbaşı yemeği Mare Gastro",
 "h1":"Sapanca'da <em>Yılbaşı Yemeği</em>: Gölün Hemen Yanında Yeni Yıl",
 "title":"Sapanca'da Yılbaşı Yemeği ve Yeni Yıl Menüsü | Mare Gastro",
 "desc":"Yeni yıla Sapanca gölün hemen yanında olmasında girin. Mare Gastro'da yılbaşı atmosferi, fine dining bir menü ve dingin bir kutlama için erken rezervasyon önerilir.",
 "kw":"sapanca yılbaşı yemeği, sapanca yılbaşı programı, sapanca yeni yıl menüsü, sapanca yılbaşı restoran",
 "lead":"Yeni yıla başlamanın en zarif yollarından biri, kalabalık ve gürültüden uzak, gölün hemen yanında sakin bir sofradır. Sapanca, yılbaşını dingin ve anlamlı kutlamak isteyenler için ideal bir kaçış noktasıdır.",
 "body":[
  ("Sapanca'da Yılbaşı Yemeği Nerede Yenir?",
   ["Sapanca'da gölün hemen yanındaki, sakin ve şık bir yılbaşı akşamı için Didi Otel bahçesindeki Mare Gastro öne çıkar. Büyük gala kalabalıklarından uzak, doğayla iç içe ve fine dining inceliğinde bir yeni yıl deneyimi sunar.",
    "Yeni yıla huzurlu bir çerçevede girmek isteyenler için %s konumumuza göz atabilirsiniz."%L(LOC,"göl kıyısındaki")]),
  ("Yeni Yıl İçin Nasıl Bir Atmosfer Sizi Bekliyor?",
   ["Mare Gastro'nun zarif ve dingin atmosferi, yılbaşını sevdiklerinizle sakin biçimde kutlamak için doğal bir sahne sunar. Gölün hemen yanında olması, mum ışığı ve özenli servis; geceyi unutulmaz kılan unsurlardır.",
    "Sinema geçmişini mutfağa taşıyan %s yorumuyla hazırlanan tabaklar, yeni yıl sofrasına özel bir derinlik katar."%L(CHEF,"Yönetici Şef Doğan Anapa")]),
  ("Yılbaşı Rezervasyonu Ne Zaman Yapılmalı?",
   ["Yılbaşı, yılın en yoğun gecelerinden biridir ve kontenjan sınırlıdır. Yerinizi garantilemek için mümkün olduğunca erken rezervasyon yapmanızı önemle öneririz.",
    "Güncel yılbaşı planı ve menü detayları için %s bizimle iletişime geçebilir, üç adımlı %s talebinizi iletebilirsiniz."%(L(WA,"WhatsApp üzerinden"),L(REZ,"rezervasyon formundan"))]),
  ("Yılbaşında Sapanca'da Konaklama Mümkün mü?",
   ["Mare Gastro, Didi Otel bünyesinde yer alır; göl kenarında konaklayarak yeni yıla huzurlu bir biçimde başlayabilirsiniz. Bu, yola çıkma telaşı olmadan gecenin tadını çıkarmanızı sağlar.",
    "Konaklama tercihinizi rezervasyon sırasında belirtebilirsiniz."]),
 ],
 "faq":[
  ("Sapanca'da yılbaşı yemeği nerede yenir?","Sapanca'da gölün hemen yanındaki, sakin ve şık bir yılbaşı için Didi Otel bahçesindeki Mare Gastro öne çıkar; kalabalık galalardan uzak, fine dining bir yeni yıl deneyimi sunar."),
  ("Yılbaşı rezervasyonu ne zaman yapılmalı?","Yılbaşı yılın en yoğun gecelerinden biridir ve kontenjan sınırlıdır. Yerinizi garantilemek için mümkün olduğunca erken rezervasyon önerilir."),
  ("Yeni yıl menüsü hakkında nasıl bilgi alırım?","Güncel yılbaşı planı ve menü detayları için WhatsApp üzerinden iletişime geçebilir, rezervasyon formundan talebinizi iletebilirsiniz."),
  ("Yılbaşında Sapanca'da konaklama var mı?","Mare Gastro Didi Otel bünyesindedir; göl kenarında konaklayarak yeni yıla huzurla başlayabilirsiniz. Konaklama tercihinizi rezervasyonda belirtebilirsiniz."),
 ],
 "rel":["sapanca-kis-restoran","sapanca-romantik-aksam-yemegi","sapanca-luks-restoran"],
},
{
 "slug":"sapanca-gun-batimi-restoran",
 "cat":"manzara","date":"2026-06-18","read":"5 dk",
 "img":"citir-somon.jpg","alt":"Gün batımında zarif bir tabak — Sapanca'da gün batımında gölün hemen yanındaki restoran Mare Gastro",
 "h1":"Sapanca'da <em>Gün Batımında</em> Gölün Hemen Yanında: Günün En Güzel Saati",
 "title":"Sapanca'da Gün Batımında Gölün Hemen Yanında | Mare Gastro",
 "desc":"Sapanca Gölü'nde gün batımına karşı akşam yemeği. Didi Otel bahçesinde açık hava masaları ve fine dining ile günün en güzel saatini Mare Gastro'da yaşayın.",
 "kw":"sapanca gün batımında gölün hemen yanındaki restoran, sapanca gölün hemen yanındaki akşam yemeği, sapanca açık hava restoran, sapanca gün batımı",
 "lead":"Sapanca'nın en büyülü anı, gölün üzerine altın bir ışığın yayıldığı gün batımıdır. O kısa ama unutulmaz dakikalara karşı kurulan bir sofra, akşamı bir deneyime dönüştürür.",
 "body":[
  ("Sapanca'da Gün Batımını İzleyerek Nerede Yemek Yenir?",
   ["Sapanca'da gün batımına karşı akşam yemeği için Didi Otel bahçesindeki Mare Gastro öne çıkar. Gölün üzerine düşen son ışıklar, bahçenin çam ve palmiyeleriyle birleşerek sofranıza eşsiz bir arka plan sunar.",
    "Manzara ile lezzeti aynı anda yaşamak isteyenler için %s göz atabilirsiniz."%L(LOC,"göl kıyısındaki konumumuza")]),
  ("Gün Batımı İçin En İyi Saat Hangisi?",
   ["Gün batımı saatleri mevsime göre değişir; bu nedenle akşamüstü rezervasyonu, ışığın en güzel hâlini yakalamanızı sağlar. Rezervasyon sırasında size o günün gün batımı saatine uygun bir zamanlama öneririz.",
    "Bu büyülü saati bir %s ile birleştirmek isterseniz, gün batımı özellikle idealdir."%L(post_url("sapanca-romantik-aksam-yemegi"),"romantik akşam yemeği")]),
  ("Açık Havada Gölün Hemen Yanında Bir Sofra",
   ["Uygun mevsimlerde bahçedeki açık hava masaları, gün batımını doğrudan deneyimlemenin en güzel yoludur. Gölün serinliği ve doğanın sesi eşliğinde yenen bir akşam yemeği, kapalı bir mekânın çok ötesindedir.",
    "Mevsimin taze tabaklarını %s inceleyebilirsiniz."%L(MENU,"menümüzde")]),
  ("Gün Batımı Yemeği İçin Rezervasyon Şart mı?",
   ["Gün batımı saatleri en çok talep gören zaman dilimidir ve hızlı dolar. Gölün hemen yanındaki bir masa için önceden rezervasyon yapmanızı öneririz.",
    "Üç adımlı %s tarih ve saatinizi seçerek yerinizi ayırtabilirsiniz."%L(REZ,"rezervasyon formundan")]),
 ],
 "faq":[
  ("Sapanca'da gün batımında gölün hemen yanında yemek nerede yenir?","Didi Otel bahçesindeki Mare Gastro, Sapanca Gölü'nün hemen yanında gün batımında bir akşam yemeği sunar; açık hava masaları ve fine dining menüyle günün en güzel saatini değerlendirir."),
  ("Gün batımı için en iyi saat hangisi?","Gün batımı saatleri mevsime göre değişir. Akşamüstü rezervasyonu, ışığın en güzel hâlini yakalamak için idealdir; rezervasyonda size uygun zamanlamayı öneririz."),
  ("Açık hava masası mevcut mu?","Uygun mevsimlerde bahçedeki açık hava masaları, gün batımını doğrudan deneyimlemek için tercih edilir. Tercihinizi rezervasyon sırasında belirtebilirsiniz."),
  ("Gün batımı yemeği için rezervasyon gerekli mi?","Gün batımı saatleri hızlı dolduğu için önceden rezervasyon önerilir. Üç adımlı form ile WhatsApp üzerinden kolayca yer ayırtabilirsiniz."),
 ],
 "rel":["sapanca-romantik-aksam-yemegi","sapanca-gol-manzarali-kahvalti","sapancada-ne-yenir"],
},
{
 "slug":"sapanca-raki-balik",
 "cat":"raki","date":"2026-06-20","read":"7 dk",
 "img":"kalamar-tava.jpg","alt":"Kalamar tava ve mezeler — Sapanca rakı balık sofrası Mare Gastro",
 "h1":"Sapanca'da <em>Rakı-Balık</em> Sofrası ve Doğru Meze Rehberi",
 "title":"Sapanca'da Rakı-Balık Sofrası ve Meze Rehberi | Mare Gastro",
 "desc":"Sapanca'da gölün hemen yanındaki bir rakı-balık sofrası nasıl kurulur? Doğru meze seçimi, taze deniz ürünleri ve Mare Gastro'nun Ege esintili önerileriyle eksiksiz bir rehber.",
 "kw":"sapanca rakı balık, sapanca rakı balık mekanları, rakı yanına meze, sapanca balık restoran",
 "lead":"Rakı-balık, Türk sofra kültürünün en köklü ritüellerinden biridir; acele etmeden, sohbetle ve doğru mezelerle kurulur. Sapanca'nın gölün hemen yanında olması ise bu sofraya dinginlik ve zarafet katar.",
 "body":[
  ("İyi Bir Rakı-Balık Sofrası Nasıl Kurulur?",
   ["İyi bir rakı-balık sofrasının üç temeli vardır: taze balık, dengeli mezeler ve acele etmeyen bir tempo. Soğuk mezelerle başlanır, ara sıcaklarla devam edilir ve sofra ızgara balıkla doruğa ulaşır. Sapanca'da bu ritüeli gölün hemen yanında yaşamak, deneyimi bambaşka bir seviyeye taşır.",
    "Mare Gastro, bu klasik sofrayı Ege esintili bir incelikle yorumlar. %s tüm seçenekleri görebilirsiniz."%L(MENU,"menümüzden")]),
  ("Rakının Yanına Hangi Mezeler Yakışır?",
   ["Dengeli bir meze seçkisi, sofranın kalbidir. Ege mutfağının zeytinyağlıları ve taze otları, rakının yanında ferah bir denge kurar:",
    "<ul><li><strong>Köz patlıcan</strong> ve zeytinyağlı sebzeler</li><li><strong>Semizotu</strong> ve mevsim yeşillikleri</li><li><strong>Enginar</strong> ve bakla gibi zeytinyağlılar</li><li><strong>Deniz mahsulü mezeleri</strong> — karides söğüş, ahtapot</li></ul>",
    "Bu mezeler, ağır değil ferah bir başlangıç sunar; böylece sofra dengesini sona kadar korur."]),
  ("Hangi Balık ve Deniz Ürünleri Tercih Edilmeli?",
   ["Sofranın ana karakteri taze balıktır. Mare Gastro mutfağında deniz ürünleri günlük olarak seçilir; mevsime göre ızgara balık, ahtapot ızgara, kalamar tava ve jumbo karides öne çıkar. Tazelik, doğru pişirme kadar önemlidir.",
    "Deniz ürünlerinin tamamı ve mevsimin günün balığı için %s tanıyabilirsiniz."%L(post_url("sapanca-deniz-urunleri"),"deniz ürünleri rehberimizi")]),
  ("Gölün Hemen Yanında Bir Rakı-Balık Akşamı",
   ["Rakı-balık acele etmeyen bir sofradır; bu yüzden manzara ve atmosfer önemlidir. Didi Otel bahçesinde, gölün serinliğine karşı kurulan bir sofra, sohbetin ve lezzetin tadını uzatır. %s göz atabilirsiniz."%L(LOC,"Konumumuza")]),
 ],
 "faq":[
  ("Sapanca'da rakı-balık nerede yenir?","Sapanca'da gölün hemen yanındaki, Ege esintili bir rakı-balık sofrası için Didi Otel bahçesindeki Mare Gastro öne çıkar; taze deniz ürünleri ve dengeli mezelerle klasik sofrayı incelikle yorumlar."),
  ("Rakının yanına hangi mezeler yakışır?","Köz patlıcan, semizotu, enginar gibi zeytinyağlılar ve karides söğüş, ahtapot gibi deniz mezeleri rakının yanında ferah bir denge kurar."),
  ("Balık taze mi, mevsime göre mi değişir?","Mare Gastro mutfağında deniz ürünleri günlük olarak seçilir ve menü mevsime göre değişir; günün balığı her ziyarette farklılık gösterebilir."),
  ("Rakı-balık sofrası için rezervasyon gerekir mi?","Özellikle hafta sonları için rezervasyon öneririz. Üç adımlı form ile WhatsApp üzerinden kolayca yer ayırtabilirsiniz."),
 ],
 "rel":["sapanca-deniz-urunleri","sapanca-gece-acik-restoran","sapancada-ne-yenir"],
},
{
 "slug":"sapanca-gece-acik-restoran",
 "cat":"gece","date":"2026-06-21","read":"5 dk",
 "img":"jumbo-karides.jpg","alt":"Gece servisi — Sapanca gece açık restoran Mare Gastro",
 "h1":"Sapanca'da <em>Gece Açık</em> Restoran: Geç Saatte Bir Sofra",
 "title":"Sapanca'da Gece Açık Restoran: Geç Saatte Yemek | Mare Gastro",
 "desc":"Sapanca'da gece geç saatte açık restoran mı arıyorsunuz? Didi Otel bahçesinde Cuma–Pazar 24 saat hizmet veren Mare Gastro'da geç saatte gölün hemen yanındaki bir sofra.",
 "kw":"sapanca gece açık restoran, sapanca geç saatte yemek, sapanca 24 saat restoran, sapanca gece yemek nerede yenir",
 "lead":"Yolculuk uzadığında, sohbet derinleştiğinde ya da gece henüz bitmediğinde; açık bir mutfak ve gölün hemen yanındaki bir masa paha biçilmezdir. Sapanca'da geç saatlerde de sofra kurabileceğiniz bir adres var.",
 "body":[
  ("Sapanca'da Gece Geç Saatte Açık Restoran Var mı?",
   ["Evet. Mare Gastro, Didi Otel bahçesinde Cuma, Cumartesi ve Pazar günleri 24 saat açıktır; bu da Sapanca'da gece geç saatte yemek arayanlar için ender bir imkândır. İstanbul'dan geç yola çıkanlar ya da geceyi uzatmak isteyenler için ideal bir duraktır.",
    "Geç saatte gölün hemen yanındaki bir sofra için %s göz atabilirsiniz."%L(LOC,"konumumuza")]),
  ("Geç Saatte Hangi Lezzetler Sunuluyor?",
   ["Gece servisinde de mutfağın tazelik ilkesi değişmez. Taze deniz ürünleri, ızgaralar ve şefin imza tabakları, günün hangi saati olursa olsun aynı özenle hazırlanır.",
    "Güncel seçenekleri %s görebilir, dilerseniz bir %s sofranızı zenginleştirebilirsiniz."%(L(MENU,"menümüzde"),L(post_url("sapanca-raki-balik"),"rakı-balık sofrasıyla"))]),
  ("Kimler İçin İdeal Bir Gece Adresi?",
   ["Geç saatte açık bir restoran; yolculuğu uzayan hafta sonu misafirleri, geceyi sevdikleriyle uzatmak isteyen çiftler ve geç bir akşam yemeği planlayanlar için idealdir. Sapanca'nın sakin gecesi, gölün hemen yanında olmasıyla birleşince huzur verir.",
    "Geceyi tamamlamak isteyenler Didi Otel'de konaklayabilir; %s konaklama tercihinizi belirtebilirsiniz."%L(REZ,"rezervasyon formunda")]),
  ("Gece İçin Rezervasyon Yapmalı mıyım?",
   ["Geç saatte sorunsuz bir deneyim için, özellikle hafta sonları önceden rezervasyon öneririz. Böylece masanız ve mutfak hazırlığı sizin için ayarlanır.",
    "Üç adımlı %s tarih ve saatinizi kolayca seçebilirsiniz."%L(REZ,"rezervasyon formundan")]),
 ],
 "faq":[
  ("Sapanca'da gece açık restoran var mı?","Evet. Mare Gastro, Didi Otel bahçesinde Cuma, Cumartesi ve Pazar günleri 24 saat açıktır ve geç saatte gölün hemen yanındaki bir akşam yemeği sunar."),
  ("Mare Gastro hangi saatlerde açık?","Mare Gastro Cuma, Cumartesi ve Pazar günleri 24 saat hizmet verir; Pazartesi–Perşembe kapalıdır."),
  ("Geç saatte tam menü servisi var mı?","Gece servisinde de taze deniz ürünleri, ızgaralar ve şefin imza tabakları aynı özenle sunulur. Menü mevsime göre değişir."),
  ("Gece için rezervasyon gerekir mi?","Geç saatte sorunsuz bir deneyim için, özellikle hafta sonları önceden rezervasyon önerilir."),
 ],
 "rel":["sapanca-raki-balik","sapanca-deniz-urunleri","didi-otel-restoran"],
},
{
 "slug":"sapanca-ozel-gun-kutlama",
 "cat":"kutlama","date":"2026-06-22","read":"6 dk",
 "img":"tereyagli-karides.jpg","alt":"Özel gün sofrası — Sapanca doğum günü ve kutlama mekanı Mare Gastro",
 "h1":"Sapanca'da <em>Özel Gün Kutlaması</em>: Doğum Günü ve Anlamlı Anlar",
 "title":"Sapanca'da Doğum Günü ve Özel Gün Kutlaması | Mare Gastro",
 "desc":"Sapanca'da doğum günü, kutlama veya sürpriz mi planlıyorsunuz? Gölün hemen yanındaki Mare Gastro'da özel masa, imza tatlılar ve sıcak bir atmosferle unutulmaz bir gün.",
 "kw":"sapanca özel gün kutlama, sapanca doğum günü mekanı, sapanca kutlama restoran, sapanca sürpriz organizasyon",
 "lead":"Bir doğum günü, terfi ya da küçük bir başarı; hayatın anlamlı anları kutlanmayı hak eder. Sapanca'nın gölün hemen yanında olması ve dingin atmosferi, bu anları sıcacık bir sofrada ölümsüzleştirir.",
 "body":[
  ("Sapanca'da Doğum Günü ve Özel Günler Nerede Kutlanır?",
   ["Sapanca'da gölün hemen yanındaki, sıcak ve özenli bir kutlama için Didi Otel bahçesindeki Mare Gastro öne çıkar. Doğum günü, terfi, mezuniyet ya da küçük bir aile kutlaması; doğanın içinde, zarif bir sofrada anlamını bulur.",
    "Sevdiklerinizle anlamlı bir gün için %s göz atabilirsiniz."%L(LOC,"konumumuza")]),
  ("Sürpriz Pasta ve Süsleme Ayarlanır mı?",
   ["Özel bir pasta, masaya küçük bir süsleme ya da imza bir tatlı; kutlamayı taçlandırmanın en güzel yollarındandır. Bu tür taleplerinizi rezervasyon sırasında paylaşırsanız, günü sizin için özenle hazırlarız.",
    "İmza tatlılarımız ve mevsimin sürprizleri için %s inceleyebilirsiniz."%L(MENU,"menümüze")]),
  ("Kaç Kişilik Gruplar Ağırlanır?",
   ["Mare Gastro, ikili romantik kutlamalardan kalabalık aile ve arkadaş gruplarına kadar farklı büyüklükte masaları ağırlar. Grup büyüklüğünüzü ve özel isteklerinizi önceden paylaşmanız, en uygun düzeni hazırlamamızı sağlar.",
    "Daha büyük organizasyonlar için %s detayları netleştirebiliriz."%L(WA,"WhatsApp üzerinden")]),
  ("Kutlama İçin Ne Kadar Önceden Rezervasyon Gerekir?",
   ["Sürpriz ve süsleme içeren kutlamalar için en az birkaç gün önceden rezervasyon öneririz; böylece hazırlık için yeterli zaman olur. Hafta sonu masaları hızlı dolduğundan erken planlama avantaj sağlar.",
    "Üç adımlı %s tarih, saat ve kişi sayısını seçerek WhatsApp üzerinden yerinizi ayırtabilirsiniz."%L(REZ,"rezervasyon formundan")]),
 ],
 "faq":[
  ("Sapanca'da doğum günü nerede kutlanır?","Sapanca'da gölün hemen yanındaki, sıcak bir doğum günü veya özel gün kutlaması için Didi Otel bahçesindeki Mare Gastro öne çıkar; özel masa, imza tatlılar ve zarif bir atmosfer sunar."),
  ("Sürpriz pasta ve süsleme ayarlanabilir mi?","Evet. Özel pasta, masaya süsleme veya küçük sürprizler gibi taleplerinizi rezervasyon sırasında paylaşabilirsiniz; ekibimiz günü özenle hazırlar."),
  ("Kaç kişilik gruplar ağırlanıyor?","Mare Gastro ikili kutlamalardan kalabalık aile ve arkadaş gruplarına kadar farklı büyüklükte masaları ağırlar. Grup büyüklüğünüzü önceden paylaşmanız önerilir."),
  ("Kutlama için ne kadar önceden rezervasyon gerekir?","Sürpriz ve süsleme içeren kutlamalar için en az birkaç gün önceden rezervasyon önerilir; hafta sonu masaları hızlı dolar."),
 ],
 "rel":["sapanca-dogum-gunu-nerede-kutlanir","sapanca-yildonumu-yemegi","sapanca-evlilik-teklifi"],
},
{
 "slug":"sef-dogan-anapa-kimdir",
 "cat":"sef","date":"2026-07-02","read":"5 dk",
 "img":"dogansef.jpg","alt":"Şef Doğan Anapa portresi — Mare Gastro Yönetici Şefi, Sapanca",
 "h1":"Şef <em>Doğan Anapa</em> Kimdir? Mare Gastro'nun Yönetici Şefi",
 "title":"Şef Doğan Anapa Kimdir? Mare Gastro Yönetici Şefi | Mare Gastro",
 "desc":"Şef Doğan Anapa kimdir, hangi restoranın şefidir? Sapanca'daki Mare Gastro'nun Yönetici Şefi Doğan Anapa hakkında bilmeniz gereken her şey.",
 "kw":"Doğan Anapa, Doğan Anapa şef, Doğan Anapa hangi restoran, Doğan Anapa Mare Gastro, Doğan Anapa Sapanca",
 "lead":"Adı Sapanca'nın gastronomi sahnesinde sıkça anılan Doğan Anapa, bugün göl kıyısında farklı bir hikâye yazıyor. İşte şefin bugünkü adresi ve mutfak anlayışı hakkında bilmeniz gerekenler.",
 "body":[
  ("Doğan Anapa Şu Anda Hangi Restoranın Şefi?",
   ["Doğan Anapa, Sapanca'da Didi Otel bahçesinde yer alan Mare Gastro'nun Yönetici Şefi'dir. Gölün hemen yanında olmasına karşı kurulan mutfağında, taze deniz ürünleri ve mevsimsel tabaklarla fine dining bir deneyim sunar.",
    "Sapanca'da yıllardır farklı mutfaklarda deneyim kazanan Anapa, bugün Mare Gastro'da kendi imzasını taşıyan bir menüyü hayata geçiriyor. %s göz atarak güncel çalışmalarını takip edebilirsiniz."%L(IG,"Mare Gastro'nun Instagram hesabından")]),
  ("Doğan Anapa'nın Mutfak Yolculuğu Nasıl Başladı?",
   ["Doğan Anapa'nın mutfağa bakışı, klasik bir şef hikâyesinden farklı bir yerden besleniyor: sinema geçmişi. Bu bakış açısı, her tabağı bir sahne, her menüyü bir anlatı gibi kurgulamasına zemin hazırlıyor.",
    "Şefin sinemadan mutfağa uzanan %s tüm detaylarıyla okuyabilirsiniz; bu yazıda odak noktamız bugünkü adresi ve mutfak anlayışı."%L(post_url("sef-dogan-anapa"),"tam hikâyesini")]),
  ("Doğan Anapa'nın Mutfak Anlayışı Nedir?",
   ["Anapa'nın mutfağı, taze ve yerel malzemeye sadakat üzerine kurulu. Sapanca Gölü'nün huzurlu atmosferini tabağa taşıyan bir yaklaşımla, deniz ürünlerini sade ama etkileyici sunumlarla buluşturuyor.",
    "Mevsimsellik onun için bir kural: menü, yılın hangi döneminde olduğunuza göre şekilleniyor. %s bu anlayışın en somut örneklerini görebilirsiniz."%L(MENU,"Güncel menümüzde")]),
  ("Doğan Anapa'nın İmza Tabakları Nelerdir?",
   ["Şefin mutfağında öne çıkan tabaklar arasında ızgara ve marine deniz ürünleri, zarif sunumlu ana yemekler ve mevsime göre değişen başlangıçlar yer alıyor. Her tabak, sadelik ile lezzet yoğunluğunu dengelemeyi hedefliyor.",
    "İmza tabakları yakından tanımak ve %s isterseniz, ekibimiz size eşlik etmekten memnuniyet duyar."%L(REZ,"bir akşam yemeği için rezervasyon yapmak")]),
 ],
 "faq":[
  ("Doğan Anapa hangi restoranın şefi?","Doğan Anapa, Sapanca'da Didi Otel bahçesinde yer alan Mare Gastro'nun Yönetici Şefi'dir."),
  ("Doğan Anapa'nın mutfak tarzı nedir?","Taze ve yerel malzemeye dayalı, mevsimsel ve deniz ürünleri ağırlıklı bir fine dining anlayışı benimser; sinema geçmişinden gelen anlatı odaklı bir yaklaşımla her menüyü kurgular."),
  ("Doğan Anapa'nın imza yemekleri nelerdir?","Izgara ve marine deniz ürünleri, zarif sunumlu ana yemekler ve mevsime göre değişen başlangıçlar şefin mutfağında öne çıkan tabaklar arasındadır."),
  ("Şef Doğan Anapa ile ilgili güncel gelişmeleri nereden takip edebilirim?","Mare Gastro'nun Instagram hesabından mutfaktan kareler ve güncel menü paylaşımlarını takip edebilirsiniz."),
 ],
 "rel":["sef-dogan-anapa","sapanca-fine-dining-nedir","sapanca-deniz-urunleri"],
},
{
 "slug":"sapanca-yazin-acik-hava-restoran",
 "cat":"mevsim","date":"2026-07-04","read":"6 dk",
 "img":"mare-ambiance.jpg","alt":"Bahçede akşam ışıkları — Sapanca'da yazın açık hava restoranı Mare Gastro",
 "h1":"Sapanca'da <em>Yazın Açık Hava</em> Restoranı: Bahçede Bir Akşam",
 "title":"Sapanca'da Yazın Açık Hava Restoranı | Mare Gastro Bahçesi",
 "desc":"Sapanca'da yaz akşamlarını açık havada, gölün hemen yanında geçirmek isteyenler için Mare Gastro'nun çam ağaçlı bahçesi eşsiz bir seçenek sunar.",
 "kw":"Sapanca açık hava restoran, Sapanca yazın nereye gidilir, Sapanca bahçede yemek, Sapanca teras restoran, Sapanca yaz akşamı",
 "lead":"Yaz akşamları Sapanca'nın en güzel halini gösterdiği zamandır. Çam kokusu, gölün serinliği ve alacakaranlıkta değişen gökyüzü; açık havada geçirilen bir akşam yemeğini unutulmaz kılar.",
 "body":[
  ("Sapanca'da Yazın Açık Havada Yemek Yenecek Bir Yer Var mı?",
   ["Evet. Didi Otel bahçesinde yer alan Mare Gastro, çam ağaçlarının arasında, gölün hemen yanında açık hava masalarıyla yaz akşamları için ideal bir adres sunar.",
    "Şehrin sıcağından ve gürültüsünden uzakta, doğanın içinde serinleyerek yemek yeme fikri, yaz aylarında Sapanca'yı tercih eden misafirlerin en çok aradığı deneyimlerden biri."]),
  ("Yaz Akşamları İçin Neden Mare Gastro Bahçesi?",
   ["Bahçenin konumu, gölün en sakin noktalarından birine bakıyor. Gün boyunca sıcaktan yorulan bir günün ardından, akşamüstü esen hafif rüzgâr ve gölgeli çam ağaçları, açık hava sofrasına ayrı bir konfor katıyor.",
    "%s bu atmosferin fotoğraflarını ve akşam hazırlıklarından kareleri düzenli olarak paylaşıyoruz."%L(IG,"Instagram hesabımızda")]),
  ("Açık Havada Rezervasyon İçin En İyi Saat Hangisi?",
   ["Yaz aylarında gün batımı saatleri, hem sıcaklığın düştüğü hem de gökyüzünün gölün üzerine altın bir ışık düşürdüğü en etkileyici zaman dilimidir. Bu saatler için masalar hızlı doluyor.",
    "%s göz atarak gün batımına özel önerilerimizi de inceleyebilirsiniz."%L(post_url("sapanca-gun-batimi-restoran"),"Gün batımı restoranı yazımıza")]),
  ("Yaz Menüsünde Neler Öne Çıkıyor?",
   ["Sıcak aylarda mutfağımız daha hafif, taze ve serinletici tabaklara ağırlık veriyor: soğuk mezeler, taze salatalar ve hafif marine deniz ürünleri yaz akşamlarının vazgeçilmezleri arasında.",
    "%s güncel yaz seçeneklerini görebilir, açık hava masası talebinizi rezervasyon sırasında iletebilirsiniz."%L(MENU,"Menümüze göz atarak")]),
 ],
 "faq":[
  ("Mare Gastro'da açık hava masası var mı?","Evet, Didi Otel bahçesinde çam ağaçları arasında, gölün hemen yanında açık hava masaları bulunur."),
  ("Yazın hangi saatlerde rezervasyon önerilir?","Gün batımı saatleri hem serinlik hem de manzara açısından en çok tercih edilen zaman dilimidir; bu saatler için erken rezervasyon önerilir."),
  ("Yağmur ya da olumsuz hava durumunda alternatif var mı?","Mare Gastro'nun kapalı alanları da gölün hemen yanında olma hissini koruyacak şekilde tasarlanmıştır; hava durumuna göre masanız iç mekâna alınabilir."),
  ("Mare Gastro haftanın hangi günleri açık?","Mare Gastro Cuma, Cumartesi ve Pazar günleri 24 saat açıktır; Pazartesi–Perşembe kapalıdır."),
 ],
 "rel":["sapanca-kis-restoran","sapanca-gun-batimi-restoran","sapanca-gol-manzarali-kahvalti"],
},
{
 "slug":"sapanca-fine-dining-fiyat-rehberi",
 "cat":"rehber","date":"2026-07-06","read":"6 dk",
 "img":"koz-patlican.jpg","alt":"Zarif sunulan bir başlangıç tabağı — Sapanca fine dining fiyat rehberi Mare Gastro",
 "h1":"Sapanca'da <em>Fine Dining</em> Ne Kadar Tutar? Şeffaf Bir Rehber",
 "title":"Sapanca'da Fine Dining Ne Kadar Tutar? Fiyat Rehberi | Mare Gastro",
 "desc":"Sapanca'da fine dining bir akşam yemeğine neler dahil olur, fiyat neye göre değişir? Mare Gastro'dan misafirlerine yol gösteren şeffaf bir rehber.",
 "kw":"Sapanca restoran fiyatları, Sapanca fine dining fiyat, kişi başı ne kadar, Sapanca gölün hemen yanındaki restoran ücret, Mare Gastro fiyat",
 "lead":"Sapanca'da fine dining bir akşam planlarken akla gelen ilk sorulardan biri fiyat. Mare Gastro'da sabit bir liste yerine, deneyimi şekillendiren unsurları anlamanız için bu rehberi hazırladık.",
 "body":[
  ("Sapanca'da Fine Dining Fiyatı Neye Göre Değişir?",
   ["Fine dining bir akşam yemeğinin fiyatı; seçtiğiniz tabaklara, kişi sayısına, mevsime ve içecek tercihinize göre değişir. Mare Gastro'da sabit bir menü fiyatı yerine, à la carte bir yapı benimseniyor.",
    "Bu nedenle en net bilgiyi, %s planınızı paylaştığınızda alabilirsiniz."%L(REZ,"rezervasyon sırasında ekibimizle görüşerek")]),
  ("Kişi Başı Ücrete Neler Dahildir?",
   ["Bir akşam yemeği deneyimi; başlangıç, ana yemek ve tatlıdan oluşan bir akış, gölün hemen yanındaki bir masa ve özenli servisi kapsar. Deniz ürünleri ağırlıklı tabaklar, mevsime göre fiyat aralığını etkileyen ana unsurlardan biridir.",
    "%s inceleyerek hangi tabakların bütçenize uygun olduğunu önceden görebilirsiniz."%L(MENU,"Güncel menümüzü")]),
  ("Fiyat/Performans Açısından Nelere Dikkat Etmeli?",
   ["Fine dining bir deneyimde fiyatı belirleyen tek unsur porsiyon değil; malzemenin tazeliği, sunumun özeni ve mekânın atmosferi de deneyimin bir parçasıdır. Sapanca Gölü'nün hemen yanında olması ve Didi Otel bahçesinin sakinliği, bu deneyime eklenen değerlerden.",
    "Şefin mutfak anlayışını yakından tanımak için %s okuyabilirsiniz."%L(post_url("sef-dogan-anapa-kimdir"),"Doğan Anapa yazımızı")]),
  ("Güncel Fiyat Bilgisini Nereden Öğrenebilirim?",
   ["Mare Gastro sitede sabit bir fiyat listesi yayınlamaz, çünkü menü mevsimsel olarak güncellenir. En güncel ve net bilgi için rezervasyon sırasında ekibimizle iletişime geçmenizi öneririz.",
    "%s veya WhatsApp üzerinden birkaç dakika içinde bilgi alabilirsiniz."%L(REZ,"Rezervasyon formu")]),
 ],
 "faq":[
  ("Mare Gastro'da sabit bir fiyat listesi var mı?","Hayır. Menü mevsimsel olarak güncellendiği için sabit bir fiyat listesi yerine, güncel bilgi rezervasyon sırasında paylaşılır."),
  ("Kuver ücreti var mı?","Kuver ve servis detayları rezervasyon sırasında netleştirilir; ekibimiz tüm sorularınızı yanıtlar."),
  ("İçecekler fiyata dahil mi?","İçecekler à la carte olarak menüden ayrıca seçilir ve fiyata dahil değildir."),
  ("Güncel fiyat bilgisini nasıl öğrenebilirim?","Rezervasyon formunu doldurarak ya da WhatsApp üzerinden ekibimizle iletişime geçerek güncel bilgi alabilirsiniz."),
 ],
 "rel":["sapanca-fine-dining-nedir","sapanca-luks-restoran","istanbula-yakin-luks-restoran"],
},
{
 "slug":"sapanca-is-yemegi-kurumsal-davet",
 "cat":"kurumsal","date":"2026-07-08","read":"6 dk",
 "img":"mare-aerial.jpg","alt":"Kuş bakışı göl manzarası — Sapanca'da iş yemeği ve kurumsal davet mekanı Mare Gastro",
 "h1":"Sapanca'da <em>İş Yemeği</em> ve Kurumsal Davet İçin Zarif Bir Adres",
 "title":"Sapanca'da İş Yemeği ve Kurumsal Davet | Mare Gastro",
 "desc":"Sapanca'da toplantı sonrası iş yemeği veya kurumsal davet için gölün hemen yanındaki, zarif bir mekan arıyorsanız Mare Gastro'yu keşfedin.",
 "kw":"Sapanca iş yemeği, kurumsal davet Sapanca, toplantı sonrası restoran, özel davet Sapanca, gölün hemen yanındaki kurumsal etkinlik",
 "lead":"İş görüşmeleri ve kurumsal davetler, doğru atmosferde çok daha akıcı ilerler. Sapanca Gölü'nün hemen yanında, sakin ve zarif bir sofra; iş yemeklerine hak ettiği ciddiyeti ve konforu katar.",
 "body":[
  ("Sapanca'da İş Yemeği İçin Uygun Bir Restoran Var mı?",
   ["Evet. Didi Otel bahçesindeki Mare Gastro, gölün hemen yanında sakin atmosferi ve özenli servisiyle iş yemekleri ve kurumsal davetler için tercih edilen bir adres.",
    "İstanbul'a yaklaşık 1,5 saat mesafede olması, şehir dışına çıkıp aynı gün dönmek isteyen ekipler için de pratik bir rota sunuyor."]),
  ("Kurumsal Davetler İçin Mare Gastro Neden Uygun?",
   ["Şehrin gürültüsünden uzak, sakin bir ortamda geçen bir yemek; iş görüşmelerinin daha rahat ilerlemesini sağlar. Gölün hemen yanında olması ve bahçenin dinginliği, resmi bir toplantıyı bile keyifli bir anıya dönüştürebilir.",
    "%s göz atarak, kurumsal davetiniz için şehir dışı bir alternatif olarak Sapanca'yı değerlendirebilirsiniz."%L(post_url("istanbula-yakin-luks-restoran"),"İstanbul'a yakın lüks restoran yazımıza")]),
  ("Toplantı Sonrası veya Şirket Etkinliği İçin Rezervasyon Nasıl Yapılır?",
   ["Grup rezervasyonlarında kişi sayısını ve etkinliğin niteliğini önceden bizimle paylaşmanız, masa düzenini ve servis akışını buna göre planlamamızı sağlar.",
    "%s katılımcı sayısı ve tarih bilgisini ileterek talebinizi oluşturabilirsiniz."%L(REZ,"Rezervasyon formundan")]),
  ("Kurumsal Davetlerde Menü Nasıl Planlanır?",
   ["Grup davetlerinde menü, katılımcı sayısına ve etkinliğin süresine göre birlikte planlanır; özel diyet talepleri de bu aşamada değerlendirilir.",
    "%s inceleyerek ekibinize uygun tabakları önceden belirleyebilirsiniz."%L(MENU,"Menümüzü")]),
 ],
 "faq":[
  ("Mare Gastro'da grup rezervasyonu yapılır mı?","Evet, kişi sayısını ve tarih bilgisini önceden ileterek grup rezervasyonu oluşturabilirsiniz."),
  ("İş yemeği için özel masa ayrılabilir mi?","Talebinizi rezervasyon sırasında belirttiğinizde, gölün hemen yanındaki sakin bir masa ayarlanabilir."),
  ("Kaç kişilik gruplara hizmet veriliyor?","Grup büyüklüğüne göre masa ve servis düzeni planlanır; kalabalık davetler için önceden bilgi verilmesi önerilir."),
  ("Kurumsal davet için ne kadar önceden rezervasyon gerekir?","Özellikle hafta sonları için birkaç gün önceden rezervasyon yapılması, planlamanın sorunsuz ilerlemesini sağlar."),
 ],
 "rel":["sapanca-luks-restoran","istanbula-yakin-luks-restoran","sapanca-fine-dining-nedir"],
},
{
 "slug":"sapanca-vejetaryen-restoran",
 "cat":"vejetaryen","date":"2026-07-09","read":"5 dk",
 "img":"enginar.jpg","alt":"Zarif sunulan enginar tabağı — Sapanca'da vejetaryen fine dining Mare Gastro",
 "h1":"Sapanca'da <em>Vejetaryen</em> Dostu Fine Dining: Mare Gastro Menüsü",
 "title":"Sapanca'da Vejetaryen Restoran Arayanlara: Mare Gastro Menüsü",
 "desc":"Sapanca'da vejetaryen veya vegan seçenekleri olan fine dining bir restoran arıyorsanız Mare Gastro'nun bitki bazlı tabaklarını keşfedin.",
 "kw":"Sapanca vejetaryen restoran, Sapanca vegan menü, glutensiz menü Sapanca, özel diyet restoran Sapanca, et yemeyenler için Sapanca restoran",
 "lead":"Et yemeyen ya da özel bir diyet uygulayan misafirler için de fine dining bir akşam mümkün. Mare Gastro'nun mutfağı, bitki bazlı tabaklarda da aynı özeni ve sunum kalitesini sürdürüyor.",
 "body":[
  ("Sapanca'da Vejetaryen Yemek Yiyebileceğim Bir Restoran Var mı?",
   ["Evet. Mare Gastro, deniz ürünleri ağırlıklı menüsünün yanında, vejetaryen misafirler için de özenle hazırlanmış tabaklar sunuyor. Didi Otel bahçesindeki sakin atmosfer, her misafire aynı kaliteyi yaşatmayı hedefliyor.",
    "%s güncel bitki bazlı seçenekleri görebilirsiniz."%L(MENU,"Menümüze göz atarak")]),
  ("Mare Gastro'nun Bitki Bazlı Tabakları Nelerdir?",
   ["Közlenmiş patlıcan, enginar, humus ve mevsim salataları; mutfağımızın vejetaryen misafirler için öne çıkan tabakları arasında. Bu tabaklar, et içeren menüyle aynı özenle, taze ve yerel malzemelerle hazırlanıyor.",
    "Şefin mevsimsel yaklaşımı hakkında daha fazla bilgi için %s okuyabilirsiniz."%L(post_url("sef-dogan-anapa-kimdir"),"Doğan Anapa yazımızı")]),
  ("Vegan ve Glutensiz Talepler Karşılanıyor mu?",
   ["Vegan veya glutensiz gibi özel diyet taleplerinizi rezervasyon sırasında iletmeniz, mutfağımızın akşamınızı buna göre hazırlamasına imkân tanır.",
    "%s diyet tercihinizi paylaşarak, size en uygun tabakları önceden planlayabiliriz."%L(REZ,"Rezervasyon formunda")]),
  ("Vejetaryen Misafirler İçin Rezervasyon Önerisi",
   ["Özellikle kalabalık bir grupta farklı diyet tercihleri varsa, bu bilgiyi önceden paylaşmanız servis akışını kolaylaştırır ve herkesin aynı kalitede bir akşam yaşamasını sağlar.",
    "%s takip ederek mevsimsel bitki bazlı tabaklarımızdan ilham alabilirsiniz."%L(IG,"Instagram hesabımızı")]),
 ],
 "faq":[
  ("Mare Gastro'da vejetaryen menü var mı?","Evet, közlenmiş patlıcan, enginar, humus ve mevsim salataları gibi özenle hazırlanmış vejetaryen tabaklar sunulur."),
  ("Vegan seçenek sunuluyor mu?","Vegan tercihinizi rezervasyon sırasında belirttiğinizde, mutfağımız size uygun tabaklar hazırlar."),
  ("Glutensiz talepler karşılanabiliyor mu?","Glutensiz talepler, önceden bildirilmesi durumunda mutfağımız tarafından değerlendirilir."),
  ("Diyet tercihimi nasıl iletebilirim?","Rezervasyon formunda veya WhatsApp üzerinden diyet tercihinizi ekibimizle paylaşabilirsiniz."),
 ],
 "rel":["sapanca-deniz-urunleri","sapanca-fine-dining-nedir","sapanca-luks-restoran"],
},
{
 "slug":"sapanca-dogum-gunu-nerede-kutlanir",
 "cat":"dogumgunu","date":"2026-07-15","read":"7 dk",
 "img":"hero-mare-1.webp","alt":"Didi Otel bahçesinde akşam ışıkları — Sapanca'da doğum günü kutlama mekanı Mare Gastro",
 "h1":"Sapanca'da <em>Doğum Günü</em> Nerede Kutlanır? 2026 Rehberi",
 "title":"Sapanca'da Doğum Günü Nerede Kutlanır? | Mare Gastro Rehberi",
 "desc":"Sapanca'da doğum günü kutlamak için en iyi mekan hangisi? Gölün hemen yanında olması, canlı müzik, pasta süslemesi ve Didi Otel güvencesiyle Mare Gastro'yu keşfedin.",
 "kw":"sapanca doğum günü nerede kutlanır, sapanca doğum günü mekanları, sapanca doğum günü restoranı, sapanca doğum günü yeri, sapanca doğum günü kutlama mekanı",
 "lead":"Sapanca'da bir doğum günü kutlamak için doğru mekanı seçmek, günün nasıl hatırlanacağını belirler. Bu rehberde Sapanca'da doğum günü mekanı ararken nelere dikkat etmeniz gerektiğini ve Mare Gastro'nun bu listeyi neden eksiksiz karşıladığını anlatıyoruz.",
 "body":[
  ("Sapanca'da Doğum Günü Mekanı Seçerken Nelere Dikkat Edilmeli?",
   ["<strong>Sapanca'da doğum günü</strong> kutlayacak bir mekan ararken göz önünde bulundurmanız gereken birkaç kriter var; bu kriterler günün akışını ve anının kalitesini doğrudan etkiler.",
    "<ul><li><strong>Atmosfer ve manzara</strong> — göl kıyısında mı, doğayla iç içe mi?</li><li><strong>Kapasite</strong> — ikili bir kutlamaya da, kalabalık bir gruba da uygun mu?</li><li><strong>Pasta ve süsleme desteği</strong> — özel taleplere açık mı?</li><li><strong>Ulaşım ve otopark</strong> — İstanbul'a yakın mı, geniş otopark var mı?</li><li><strong>Güvenilirlik</strong> — kurumsal, bilinen bir işletme mi yoksa amatör bir organizasyon mu?</li><li><strong>Atmosfer detayı</strong> — canlı müzik gibi kutlamayı taçlandıran unsurlar var mı?</li></ul>"]),
  ("Mare Gastro: Sapanca'da Doğum Günü İçin Eksiksiz Bir Adres",
   ["Mare Gastro, Sapanca Gölü kıyısındaki Didi Otel'in bahçesinde konumlanan bir fine dining restoranı. Çam ağaçları, gölün sakinliği ve özenli bir servis anlayışı, doğum günü kutlamalarını sıradan bir akşam yemeğinden çok daha fazlasına dönüştürüyor.",
    bfig("mare-bahce-manzarasi.webp","Mare Gastro'nun Didi Otel bahçesindeki manzarası — Sapanca","Didi Otel bahçesinden Mare Gastro'nun genel görünümü"),
    "%s bu deneyimin nasıl tasarlandığını daha yakından okuyabilirsiniz."%L(STORY,"Hikâyemizi")]),
  ("Ulaşım, Otopark ve Didi Otel Güvencesi",
   ["İstanbul'dan yaklaşık 1,5 saat mesafede olan Sapanca, doğum günü kutlaması için hem kolay ulaşılabilir hem de şehrin kalabalığından uzak bir seçenek. Mare Gastro'nun konumu, geniş otopark imkânıyla kalabalık gruplar için bile pratik bir çözüm sunuyor.",
    "Mare Gastro, Sapanca'da kurulu, bilinen ve güvenilir bir otel işletmesi olan Didi Otel bünyesinde faaliyet gösteriyor; bu da organizasyonunuzu amatör bir mekâna değil, kurumsal bir adrese emanet etmeniz anlamına geliyor. İsteyen misafirler, kutlama sonrası %s da imkân buluyor."%L(SITE+"/tr/","Didi Otel'de konaklama yapma")]),
  ("Canlı Müzik Eşliğinde Bir Doğum Günü Sofrası",
   ["Mare Gastro'da hafta sonu akşamları genellikle canlı müzik atmosferi eşlik ediyor; bu detay, Sapanca'da pek çok mekânda bulamayacağınız, kutlamayı gerçek bir deneyime dönüştüren bir unsur.",
    "Doğa, gölün hemen yanında olması, mutfak ve müziğin bir araya geldiği bu atmosfer, Mare Gastro'yu Sapanca'da eşsiz kılan detaylardan biri."]),
  ("Kutlama Türünüze Göre Öneriler",
   ["Her doğum günü kutlaması farklıdır. Planladığınız kutlama türüne göre hazırladığımız detaylı rehberlere göz atabilirsiniz:",
    "<ul><li>%s</li><li>%s</li><li>%s</li><li>%s</li><li>%s</li><li>%s</li><li>%s</li><li>%s</li><li>%s</li></ul>"%(
      L(post_url("sapanca-suprizli-dogum-gunu-organizasyonu"),"Sürpriz doğum günü organizasyonu"),
      L(post_url("sapanca-gol-manzarali-dogum-gunu-mekanlari"),"Gölün hemen yanındaki doğum günü mekanları"),
      L(post_url("sapanca-kalabalik-arkadas-grubu-dogum-gunu"),"Kalabalık arkadaş grubuyla kutlama"),
      L(post_url("sapanca-romantik-es-dogum-gunu-yemegi"),"Eşe özel romantik doğum günü yemeği"),
      L(post_url("sapanca-dogum-gunu-pastasi-suslemeli-mekan"),"Doğum günü pastası ve masa süslemesi"),
      L(post_url("sapanca-gece-dogum-gunu-kutlamasi-hafta-sonu"),"Gece kutlaması ve hafta sonu saatleri"),
      L(post_url("sapanca-30-40-yas-dogum-gunu-kutlamasi"),"30, 40, 50 yaş kutlamaları"),
      L(post_url("sapanca-istanbuldan-dogum-gunu-kacamagi"),"İstanbul'dan doğum günü kaçamağı"),
      L(post_url("sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri"),"Fiyatlar ve menü seçenekleri"))]),
  ("Rezervasyon Nasıl Yapılır?",
   ["Üç adımlı %s tarih, saat ve kişi sayısını seçerek WhatsApp üzerinden hızlıca yerinizi ayırtabilirsiniz. Pasta, süsleme veya oturma düzeniyle ilgili özel taleplerinizi de bu aşamada iletebilirsiniz."%L(REZ,"rezervasyon formundan")]),
 ],
 "faq":[
  ("Sapanca'da doğum günü nerede kutlanır?","Sapanca Gölü kıyısındaki Didi Otel bahçesinde yer alan Mare Gastro, gölün hemen yanında olması, canlı müzik atmosferi ve pasta/süsleme desteğiyle Sapanca'da doğum günü kutlamak için öne çıkan bir adrestir."),
  ("Mare Gastro doğum günü kutlamaları için uygun mu?","Evet. İkili kutlamalardan kalabalık gruplara kadar farklı büyüklükte masalar ağırlanır; özel pasta, süsleme ve hafta sonu canlı müzik atmosferi sunulur."),
  ("Sapanca'da doğum günü mekanına ulaşım kolay mı?","Evet. Sapanca, İstanbul'a yaklaşık 1,5 saat mesafededir ve Mare Gastro'nun bulunduğu Didi Otel'de geniş otopark imkânı vardır."),
  ("Kutlama sonrası Sapanca'da konaklanabilir mi?","Evet. Mare Gastro'nun bulunduğu Didi Otel bünyesinde isteyen misafirler için konaklama seçeneği mevcuttur."),
 ],
 "rel":["sapanca-ozel-gun-kutlama","sapanca-suprizli-dogum-gunu-organizasyonu","sapanca-gol-manzarali-dogum-gunu-mekanlari"],
},
{
 "slug":"sapanca-suprizli-dogum-gunu-organizasyonu",
 "cat":"dogumgunu","date":"2026-07-16","read":"6 dk",
 "img":"patates-terin.webp","alt":"Zarif sunulan bir başlangıç tabağı — Sapanca'da sürpriz doğum günü organizasyonu Mare Gastro",
 "h1":"Sapanca'da <em>Sürpriz Doğum Günü</em> Organizasyonu Nasıl Yapılır?",
 "title":"Sapanca'da Sürpriz Doğum Günü Organizasyonu | Mare Gastro",
 "desc":"Sapanca'da sürpriz doğum günü mü planlıyorsunuz? Mare Gastro'da özel masa, pasta süslemesi ve canlı müzik eşliğinde unutulmaz bir sürpriz nasıl organize edilir?",
 "kw":"sapanca sürpriz doğum günü, sapanca doğum günü sürprizi, sapanca sürpriz organizasyon mekanı, sapanca sürpriz parti restoran",
 "lead":"Bir sürpriz doğum günü, doğru mekan ve doğru planlamayla unutulmaz bir anıya dönüşür. Sapanca'da Mare Gastro, sürpriz organizasyonların her adımında misafirlerine eşlik ediyor.",
 "body":[
  ("Sürpriz Doğum Günü İçin Neden Sapanca?",
   ["Sapanca, İstanbul'dan kolay ulaşılabilen ama şehrin telaşından uzak bir konumda olduğu için sürpriz organizasyonlar için ideal. Kutlanacak kişiyi şehir dışına \"bir gezi\" bahanesiyle çıkarmak, sürprizin en doğal yollarından biri.",
    "Didi Otel'in bahçesindeki Mare Gastro, gölün hemen yanında olması ve sakin atmosferiyle sürprizin etkisini bir kat daha artırıyor.",
    bfig("mare-kutlama-kadeh.webp","Mare Gastro'da kadeh kaldırarak kutlama anı — Sapanca doğum günü sürprizi","Mare Gastro'da bir kutlama anı")]),
  ("Mare Gastro'da Sürpriz Nasıl Planlanır?",
   ["Sürpriz detaylarınızı %s paylaştığınızda, ekibimiz kutlanacak kişi masaya gelene kadar her şeyi sizin adınıza hazırlar: özel masa düzeni, süsleme ve zamanlama."%L(REZ,"rezervasyon sırasında"),
    "Grup büyüklüğü, sürpriz anının şekli (pasta getirilmesi, mumların söndürülmesi, kısa bir kutlama konuşması gibi) rezervasyon sırasında netleştirilirse, o an kusursuz akar."]),
  ("Pasta, Süsleme ve Küçük Detaylar",
   ["Masaya küçük bir süsleme, özel bir pasta ya da imza bir tatlı; sürprizi taçlandıran en güzel detaylardandır. Bu taleplerinizi önceden paylaşırsanız, günü sizin için özenle hazırlarız.",
    "İmza tatlılarımız için %s göz atabilirsiniz."%L(MENU,"menümüze")]),
  ("Sürprizi Taçlandıran Canlı Müzik Atmosferi",
   ["Mare Gastro'da hafta sonu akşamları genellikle eşlik eden canlı müzik, sürpriz anının hemen ardından oluşan o sıcak atmosferi güçlendiriyor. Sapanca'da pek çok mekânda rastlayamayacağınız bu detay, günü gerçek bir kutlamaya dönüştürüyor."]),
  ("Ne Zaman Rezervasyon Yapmalısınız?",
   ["Sürpriz içeren kutlamalar için en az birkaç gün önceden rezervasyon öneririz; böylece hazırlık için yeterli zaman oluşur. Hafta sonu masaları hızlı dolduğundan erken planlama avantaj sağlar.",
    "%s tarih, saat ve kişi sayısını seçerek WhatsApp üzerinden yerinizi ayırtabilirsiniz."%L(REZ,"Üç adımlı rezervasyon formundan")]),
 ],
 "faq":[
  ("Sapanca'da sürpriz doğum günü nerede organize edilir?","Didi Otel bahçesindeki Mare Gastro, gölün hemen yanında olması, özel masa düzeni ve pasta/süsleme desteğiyle sürpriz doğum günü organizasyonları için uygun bir adrestir."),
  ("Mare Gastro sürpriz pasta ve süsleme ayarlıyor mu?","Evet. Rezervasyon sırasında talebinizi paylaştığınızda, ekibimiz özel pasta ve masa süslemesini sizin için hazırlar."),
  ("Sürpriz için kutlanacak kişiye nasıl gizli kalınır?","Detayları önceden ekibimizle paylaşırsanız, kutlanacak kişi masaya gelene kadar tüm hazırlıklar sizin adınıza gizlice tamamlanır."),
  ("Sürpriz organizasyon için kaç gün önceden rezervasyon gerekir?","Süsleme ve pasta içeren sürprizler için en az birkaç gün önceden rezervasyon yapılması önerilir."),
 ],
 "rel":["sapanca-dogum-gunu-nerede-kutlanir","sapanca-dogum-gunu-pastasi-suslemeli-mekan","sapanca-ozel-gun-kutlama"],
},
{
 "slug":"sapanca-gol-manzarali-dogum-gunu-mekanlari",
 "cat":"dogumgunu","date":"2026-07-17","read":"6 dk",
 "img":"mare-aerial.webp","alt":"Kuş bakışı göl manzarası — Sapanca'da gölün hemen yanındaki doğum günü kutlama mekanı Mare Gastro",
 "h1":"Sapanca'da <em>Gölün Hemen Yanında</em> Doğum Günü Kutlama Mekanları",
 "title":"Sapanca Gölün Hemen Yanında Doğum Günü Mekanı | Mare Gastro",
 "desc":"Sapanca Gölü'nün hemen yanında doğum günü kutlamak isteyenler için Mare Gastro: Didi Otel bahçesinde göl kıyısında fine dining bir kutlama deneyimi.",
 "kw":"sapanca gölün hemen yanındaki doğum günü, sapanca gölü kenarında doğum günü, sapanca gölün hemen yanındaki kutlama mekanı, sapanca göl kıyısı restoran doğum günü",
 "lead":"Sapanca Gölü'nün suları, günün her saatinde farklı bir ışık oyunu sunar. Bir doğum günü kutlamasını bu manzaraya karşı yaşamak, anıyı bambaşka bir seviyeye taşır.",
 "body":[
  ("Neden Gölün Hemen Yanında Bir Doğum Günü?",
   ["Kapalı, sıradan bir mekânda geçen bir doğum günü ile gölün üzerine düşen ışığa karşı kutlanan bir doğum günü arasındaki fark, fotoğraflardan çok anının kendisinde hissedilir. <strong>Sapanca'da gölün hemen yanındaki doğum günü</strong> arayanlar, bu farkı fark ediyor.",
    "Mare Gastro, tam olarak bu deneyimi sunmak için Didi Otel'in göl kıyısındaki bahçesinde konumlandı."]),
  ("Didi Otel Bahçesi: Sapanca Gölü'nün Hemen Yanında",
   ["Çam ağaçlarının gölgesinde, gölün serinliğine açılan masalarda kutlanan bir doğum günü, doğanın kendisini davetli listenize eklemiş gibi hissettirir. %s bu atmosferin nasıl tasarlandığını okuyabilirsiniz."%L(STORY,"Hikâyemizden"),
    bfig("mare-bahce-havuz-yolu.webp","Didi Otel bahçesinden yürüyüş yolu — Sapanca gölün hemen yanındaki doğum günü mekanı","Didi Otel bahçesinde bir yürüyüş yolu")]),
  ("Gün Batımı mı, Gece mi? Hangi Saat Daha Etkileyici?",
   ["Gün batımı saatlerinde gölün üzerine düşen altın ışık, fotoğraf karelerine yansıyan en etkileyici anlardan biri. Gece saatlerinde ise ışıklandırma ve genellikle eşlik eden canlı müzik, aynı manzarayı daha samimi bir atmosfere dönüştürüyor.",
    "Hangi saati tercih ederseniz edin, %s göz atarak konumumuzu netleştirebilirsiniz."%L(LOC,"konumumuza")]),
  ("Gölün Hemen Yanındaki Masalarda Rezervasyon Önerileri",
   ["Gölün hemen yanındaki masalar, özellikle hafta sonu akşamlarında hızlı dolduğundan erken rezervasyon öneriyoruz. %s manzara tercihinizi belirtirseniz, size en uygun masayı ayırırız."%L(REZ,"Rezervasyon sırasında")]),
 ],
 "faq":[
  ("Sapanca'da gölün hemen yanındaki doğum günü mekanı var mı?","Evet. Mare Gastro, Sapanca Gölü kıyısındaki Didi Otel bahçesinde yer alır ve doğum günü kutlamaları için gölün hemen yanındaki masalar sunar."),
  ("Gün batımı saatinde masa ayırtabilir miyim?","Evet, rezervasyon sırasında gün batımı saatine denk gelecek bir masa talep edebilirsiniz."),
  ("Gece gölün hemen yanında bir kutlama mümkün mü?","Evet. Mare Gastro hafta sonu 24 saat açık olup gece saatlerinde ışıklandırma ve genellikle canlı müzik eşliğinde gölün hemen yanındaki bir kutlama sunar."),
  ("Gölün hemen yanındaki masalar için ne kadar önceden rezervasyon gerekir?","Özellikle hafta sonları için birkaç gün önceden rezervasyon yapmanızı öneririz."),
 ],
 "rel":["sapanca-dogum-gunu-nerede-kutlanir","sapanca-gun-batimi-restoran","sapanca-romantik-es-dogum-gunu-yemegi"],
},
{
 "slug":"sapanca-kalabalik-arkadas-grubu-dogum-gunu",
 "cat":"dogumgunu","date":"2026-07-18","read":"6 dk",
 "img":"3lu-deniz-mahsulu.webp","alt":"Paylaşımlık deniz ürünleri tabağı — Sapanca'da kalabalık grup doğum günü kutlaması Mare Gastro",
 "h1":"Sapanca'da <em>Kalabalık Arkadaş Grubuyla</em> Doğum Günü Kutlama Mekanları",
 "title":"Sapanca'da Kalabalık Doğum Günü Mekanı | Mare Gastro",
 "desc":"Sapanca'da kalabalık bir arkadaş grubuyla doğum günü kutlamak için Mare Gastro: geniş masa düzeni, paylaşımlık tabaklar ve gölün hemen yanında olması.",
 "kw":"sapanca kalabalık doğum günü, sapanca grup rezervasyonu restoran, sapanca arkadaş grubu mekan, sapanca kalabalık masa restoran",
 "lead":"Kalabalık bir arkadaş grubuyla doğum günü kutlamak, doğru mekan seçilmediğinde organizasyonu zorlaştırabilir. Mare Gastro, farklı büyüklükte grupları aynı özenle ağırlayacak şekilde tasarlandı.",
 "body":[
  ("Kalabalık Gruplar İçin Mekan Seçerken Nelere Dikkat Edilmeli?",
   ["Kalabalık bir <strong>Sapanca doğum günü</strong> kutlamasında mekanın kapasitesi, oturma düzeni esnekliği, otopark imkânı ve grup menüsü seçenekleri kritik önem taşır. Bu detaylar önceden netleşmezse, organizasyon günün kendisinden daha stresli hale gelebilir."]),
  ("Mare Gastro'da Grup Masaları Nasıl Düzenlenir?",
   ["Grup büyüklüğünüzü %s paylaştığınızda, ekibimiz Didi Otel bahçesinde en uygun oturma düzenini sizin için hazırlar. İkili kutlamalardan geniş arkadaş gruplarına kadar farklı ölçekte masalar ağırlanır."%L(WA,"WhatsApp üzerinden"),
    bfig("mare-grup-sofra.webp","Paylaşımlık mezelerle donatılmış grup sofrası — Sapanca kalabalık doğum günü","Mare Gastro'da bir grup sofrası")]),
  ("Paylaşımlık Tabaklar ve Grup Menüsü",
   ["Deniz ürünleri ağırlıklı paylaşımlık tabaklar, kalabalık bir masada herkesin farklı lezzetleri tadabilmesine imkân tanır. %s grup için uygun seçenekleri önceden inceleyebilirsiniz."%L(MENU,"Menümüzden")]),
  ("Otopark ve Ulaşım: Kalabalık Gruplar İçin Pratik Bilgiler",
   ["Farklı araçlarla gelen kalabalık bir grup için otopark, göz ardı edilmemesi gereken bir detay. Didi Otel bünyesindeki geniş otopark imkânı, bu konuda ekstra bir planlama yapmanıza gerek bırakmıyor.",
    "Sapanca'nın İstanbul'a yaklaşık 1,5 saat mesafede olması da grubun farklı noktalardan kolayca buluşabilmesini sağlıyor."]),
 ],
 "faq":[
  ("Sapanca'da kalabalık bir grupla doğum günü kutlanabilir mi?","Evet. Mare Gastro, Didi Otel bahçesinde farklı büyüklükte grupları ağırlayacak esnek masa düzenleri sunar."),
  ("Grup rezervasyonu nasıl yapılır?","Grup büyüklüğünüzü ve özel taleplerinizi WhatsApp üzerinden veya rezervasyon formundan paylaşarak en uygun düzeni ayarlayabilirsiniz."),
  ("Kalabalık gruplar için otopark yeterli mi?","Evet, Didi Otel bünyesinde geniş otopark imkânı bulunur."),
  ("Grup için paylaşımlık menü seçeneği var mı?","Evet, deniz ürünleri ağırlıklı paylaşımlık tabaklar grup kutlamaları için uygun seçenekler arasındadır."),
 ],
 "rel":["sapanca-dogum-gunu-nerede-kutlanir","sapanca-istanbuldan-dogum-gunu-kacamagi","sapanca-is-yemegi-kurumsal-davet"],
},
{
 "slug":"sapanca-romantik-es-dogum-gunu-yemegi",
 "cat":"dogumgunu","date":"2026-07-19","read":"6 dk",
 "img":"dana-carpaccio2.webp","alt":"Şık fine dining tabağı — Sapanca'da eşe özel romantik doğum günü yemeği Mare Gastro",
 "h1":"Sapanca'da Eşinizin <em>Doğum Günü</em> İçin Romantik Bir Akşam Yemeği",
 "title":"Sapanca'da Eşe Özel Doğum Günü Yemeği | Mare Gastro",
 "desc":"Eşinizin doğum gününü Sapanca'da romantik bir akşam yemeğiyle kutlamak için Mare Gastro: gölün hemen yanında olması, mum ışığı ve imza tatlılarla özel bir sofra.",
 "kw":"sapanca eş doğum günü, sapanca romantik doğum günü yemeği, sapanca sevgiliye doğum günü sürprizi, sapanca çift doğum günü mekanı",
 "lead":"Eşinizin ya da sevgilinizin doğum gününü kutlamak için Sapanca'da romantik bir akşam yemeği arıyorsanız, doğru atmosfer her şeyi değiştirir.",
 "body":[
  ("Romantik Bir Doğum Günü Yemeği İçin Sapanca Neden İdeal?",
   ["Şehrin gürültüsünden uzak, gölün sakinliğine karşı geçirilen bir akşam; eşinize ya da sevgilinize doğum gününde vermek isteyeceğiniz en anlamlı hediyelerden biri olabilir. <strong>Sapanca'da romantik doğum günü yemeği</strong> arayan çiftler için Mare Gastro, bu atmosferi eksiksiz sunuyor."]),
  ("Mum Işığında İkili Bir Masa",
   ["Didi Otel bahçesinde, gölün hemen yanında yer alan ikili bir masa; mum ışığı ve özenli servisle doğum gününü sade ama unutulmaz bir akşama dönüştürür. %s isterseniz, size özel bir masa düzeni hazırlarız."%L(REZ,"Rezervasyon sırasında belirttiğinizde"),
    bfig("mare-romantik-kadeh.webp","İkili kadeh kaldırma anı — Sapanca'da eşe özel romantik doğum günü yemeği","Mare Gastro'da romantik bir kadeh anı")]),
  ("İmza Tatlı ile Kutlamayı Taçlandırmak",
   ["Akşamın sonunda paylaşılan bir imza tatlı, kutlamanın en tatlı anına dönüşür. %s eşinize sürpriz yapabileceğiniz seçenekleri inceleyebilirsiniz."%L(MENU,"Menümüzden")]),
  ("Canlı Müzik Eşliğinde Romantik Bir Akşam",
   ["Mare Gastro'da hafta sonu akşamlarına genellikle eşlik eden canlı müzik, romantik bir doğum günü yemeğini Sapanca'da eşsiz kılan detaylardan biri. Göl, mum ışığı ve müziğin birleştiği bu atmosfer, kelimelerden daha fazlasını anlatıyor."]),
 ],
 "faq":[
  ("Sapanca'da eşime romantik bir doğum günü yemeği nerede ayarlayabilirim?","Didi Otel bahçesindeki Mare Gastro, gölün hemen yanında olması, mum ışığı ve imza tatlılarla romantik bir doğum günü yemeği için uygun bir adrestir."),
  ("İkili masalar için özel bir düzen ayarlanıyor mu?","Evet, rezervasyon sırasında talebinizi belirttiğinizde gölün hemen yanındaki ikili bir masa düzeni hazırlanır."),
  ("Romantik kutlama için canlı müzik oluyor mu?","Mare Gastro'da hafta sonu akşamlarına genellikle canlı müzik eşlik eder."),
  ("Sürpriz bir tatlı ayarlanabilir mi?","Evet, imza tatlılarımız ve sürpriz detaylar için rezervasyon sırasında talebinizi paylaşabilirsiniz."),
 ],
 "rel":["sapanca-dogum-gunu-nerede-kutlanir","sapanca-romantik-aksam-yemegi","sapanca-evlilik-teklifi"],
},
{
 "slug":"sapanca-dogum-gunu-pastasi-suslemeli-mekan",
 "cat":"dogumgunu","date":"2026-07-20","read":"6 dk",
 "img":"cheesecake.webp","alt":"İmza tatlı ve mum ışığı — Sapanca'da doğum günü pastası ve masa süslemesi Mare Gastro",
 "h1":"Sapanca'da <em>Doğum Günü Pastası</em> ve Masa Süslemesi Yapan Restoranlar",
 "title":"Sapanca'da Doğum Günü Pastası Ayarlayan Restoran | Mare Gastro",
 "desc":"Sapanca'da doğum günü pastası ve masa süslemesi hizmeti sunan restoran mı arıyorsunuz? Mare Gastro'da rezervasyon sırasında talep ederek özel bir sofra hazırlatabilirsiniz.",
 "kw":"sapanca doğum günü pastası, sapanca masa süsleme restoran, sapanca pasta getirme kuralları restoran, sapanca doğum günü süslemesi",
 "lead":"Bir doğum günü kutlamasının en özel anı, mumların üflendiği o saniyedir. Sapanca'da bu anı hazırlayan bir restoran seçmek, kutlamanın kalitesini belirler.",
 "body":[
  ("Mare Gastro'da Doğum Günü Pastası ve Süsleme Nasıl Ayarlanır?",
   ["Özel bir pasta, masaya küçük bir süsleme ya da mumlar; rezervasyon sırasında talebinizi paylaştığınızda ekibimiz tarafından özenle hazırlanır. %s detayları netleştirebilirsiniz."%L(REZ,"Rezervasyon formundan veya WhatsApp üzerinden"),
    bfig("mare-kabana-oturma.webp","Özenle hazırlanmış oturma köşesi — Sapanca doğum günü pastası ve süsleme","Mare Gastro'da özel hazırlanmış bir köşe")]),
  ("Kendi Pastanızı Getirebilir misiniz?",
   ["Kendi pastanızı getirmek isterseniz, bu talebinizi rezervasyon sırasında iletmeniz servis ekibimizin hazırlıklı olmasını sağlar; pastanın saklanması ve servis zamanlaması buna göre planlanır.",
    "Detaylar için %s ekibimizle iletişime geçebilirsiniz."%L(WA,"WhatsApp üzerinden")]),
  ("İmza Tatlılarımızla Pastasız Bir Kutlama",
   ["Klasik bir doğum günü pastası yerine, Mare Gastro'nun imza tatlılarıyla da unutulmaz bir kutlama yapmak mümkün. %s mevsime göre değişen tatlı seçeneklerini keşfedebilirsiniz."%L(MENU,"Menümüzden")]),
  ("Süsleme ve Sürpriz Detaylar İçin Zamanlama",
   ["Süsleme ve pasta içeren kutlamalar için en az birkaç gün önceden rezervasyon yapmanızı öneririz; böylece hazırlık için yeterli zaman oluşur ve gün, hayal ettiğiniz gibi akar."]),
 ],
 "faq":[
  ("Mare Gastro'da doğum günü pastası ayarlanabilir mi?","Evet, rezervasyon sırasında talebinizi paylaştığınızda özel pasta ve masa süslemesi ekibimiz tarafından hazırlanır."),
  ("Kendi pastamı restorana getirebilir miyim?","Evet, ancak bu talebinizi rezervasyon sırasında önceden bildirmeniz servis ekibinin hazırlıklı olmasını sağlar."),
  ("Pasta istemiyorum, alternatif tatlı var mı?","Evet, cheesecake gibi imza tatlılarımız pastasız bir kutlama için de özel bir seçenek sunar."),
  ("Süsleme için ne kadar önceden haber vermeliyim?","En az birkaç gün önceden rezervasyon ve talep bildirmenizi öneririz."),
 ],
 "rel":["sapanca-suprizli-dogum-gunu-organizasyonu","sapanca-dogum-gunu-nerede-kutlanir","sapanca-yildonumu-yemegi"],
},
{
 "slug":"sapanca-gece-dogum-gunu-kutlamasi-hafta-sonu",
 "cat":"dogumgunu","date":"2026-07-21","read":"6 dk",
 "img":"kalamar-tava.webp","alt":"Akşam servisi ve mumlu masalar — Sapanca'da gece doğum günü kutlaması Mare Gastro",
 "h1":"Sapanca'da <em>Gece Doğum Günü</em> Kutlaması: Hafta Sonu 24 Saat Açık",
 "title":"Sapanca'da Gece Açık Doğum Günü Mekanı | Mare Gastro",
 "desc":"Sapanca'da gece doğum günü kutlamak isteyenler için Mare Gastro Cuma, Cumartesi ve Pazar günleri 24 saat açık; geç saatlerde bile sıcak bir kutlama mümkün.",
 "kw":"sapanca gece açık doğum günü, sapanca hafta sonu doğum günü, sapanca gece yemek mekanı, sapanca 24 saat açık restoran doğum günü",
 "lead":"Herkesin takvimi gündüz saatlerine uymayabilir. Sapanca'da gece geç saatlerde bir doğum günü kutlamak isteyenler için Mare Gastro'nun hafta sonu 24 saat açık olması büyük bir avantaj.",
 "body":[
  ("Sapanca'da Gece Doğum Günü Kutlamak Mümkün mü?",
   ["Evet. <strong>Sapanca'da gece doğum günü</strong> kutlamak isteyenler için Mare Gastro, hafta sonu boyunca hizmet veriyor; iş çıkışı geç bir kutlama ya da gece yarısına uzayan bir sofra mümkün."]),
  ("Cuma, Cumartesi, Pazar: 24 Saat Açık Ayrıcalığı",
   ["Mare Gastro Cuma, Cumartesi ve Pazar günleri 24 saat açıktır; Pazartesi–Perşembe kapalıdır. Bu esneklik, Sapanca'da doğum günü planlayan misafirlere saat kaygısı olmadan kutlama imkânı tanır.",
    bfig("mare-teras-misafir.webp","Didi Otel terasında bir misafir — Sapanca'da gece doğum günü kutlaması","Mare Gastro terasından bir kare")]),
  ("Gece Atmosferi: Işıklar, Müzik ve Göl",
   ["Gece saatlerinde ışıklandırılan bahçe, gölün karanlıkta yansıyan ışıkları ve genellikle eşlik eden canlı müzik; Mare Gastro'yu Sapanca'da gece kutlamaları için eşsiz bir adrese dönüştürüyor."]),
  ("Gece Rezervasyonunda Dikkat Edilmesi Gerekenler",
   ["Geç saat rezervasyonlarında masa ve otopark planlamasının netleşmesi için %s tercih ettiğiniz saati önceden belirtmenizi öneririz."%L(REZ,"rezervasyon formunda")]),
 ],
 "faq":[
  ("Sapanca'da gece doğum günü kutlanabilir mi?","Evet. Mare Gastro Cuma, Cumartesi ve Pazar günleri 24 saat açık olduğu için gece geç saatlerde de doğum günü kutlaması yapılabilir."),
  ("Mare Gastro hangi günler 24 saat açık?","Cuma, Cumartesi ve Pazar günleri 24 saat açıktır; Pazartesi–Perşembe kapalıdır."),
  ("Gece kutlamalarında canlı müzik oluyor mu?","Hafta sonu akşamlarına genellikle canlı müzik atmosferi eşlik eder."),
  ("Gece için otopark sorun olur mu?","Hayır, Didi Otel bünyesinde geniş otopark imkânı geceleri de kullanılabilir."),
 ],
 "rel":["sapanca-gece-acik-restoran","sapanca-dogum-gunu-nerede-kutlanir","sapanca-gol-manzarali-dogum-gunu-mekanlari"],
},
{
 "slug":"sapanca-30-40-yas-dogum-gunu-kutlamasi",
 "cat":"dogumgunu","date":"2026-07-22","read":"6 dk",
 "img":"izgara-kofte.webp","alt":"Zarif ana yemek sunumu — Sapanca'da 30 ve 40 yaş doğum günü kutlaması Mare Gastro",
 "h1":"Sapanca'da <em>30, 40, 50 Yaş</em> Doğum Günü Kutlamaları İçin En İyi Mekan",
 "title":"Sapanca'da Yuvarlak Yaş Doğum Günü Kutlaması | Mare Gastro",
 "desc":"30, 40 veya 50 yaş gibi yuvarlak yaş doğum günlerini Sapanca'da kutlamak için Mare Gastro: gölün hemen yanında olması, canlı müzik ve zarif bir sofra.",
 "kw":"sapanca 30 yaş doğum günü, sapanca 40 yaş kutlama, sapanca yuvarlak yaş kutlaması mekan, sapanca 50 yaş doğum günü restoran",
 "lead":"30, 40 ya da 50 yaş gibi yuvarlak yaş günleri, hayatın özel dönüm noktalarıdır ve hak ettikleri kutlamayı bulmalıdır. Sapanca'da bu anlamlı günleri kutlamak için Mare Gastro'nun sunduğu atmosfer tam da bu ağırlığa uygun.",
 "body":[
  ("Yuvarlak Yaş Kutlamaları Neden Farklı Planlanmalı?",
   ["<strong>Sapanca'da 30 yaş doğum günü</strong> ya da 40, 50 yaş gibi bir dönüm noktasını kutlamak, sıradan bir akşam yemeğinden daha fazla özen ister. Mekanın atmosferi, kutlamanın ağırlığıyla eşleşmeli."]),
  ("Mare Gastro'da Milestone Bir Doğum Günü",
   ["Didi Otel bahçesindeki gölün hemen yanındaki sofra, kurumsal ve güvenilir bir işletmenin sunduğu özenli servisle birleşince; yuvarlak yaş kutlamaları için aranan ciddiyeti ve zarafeti bir arada sunuyor. %s bu deneyimin arkasındaki anlayışı okuyabilirsiniz."%L(STORY,"Hikâyemizden"),
    bfig("mare-teras-misafir2.webp","Didi Otel terasında zarif bir an — Sapanca'da yuvarlak yaş doğum günü kutlaması","Mare Gastro terasında bir misafir")]),
  ("Kalabalık mı, Özel mi? Kutlama Şeklinizi Belirleyin",
   ["Bazı yuvarlak yaş kutlamaları geniş bir davetli listesiyle, bazıları ise sadece en yakınlarla kutlanmak ister. Mare Gastro her iki formatı da esnek masa düzenleriyle karşılıyor; %s tercihinizi paylaşmanız yeterli."%L(WA,"WhatsApp üzerinden")]),
  ("Anıyı Kalıcı Kılmak: Fotoğraf, Müzik ve Detaylar",
   ["Gün batımı ışığı, hafta sonu eşlik eden canlı müzik ve özel pasta/süsleme detayları; bu özel yaş gününü yıllarca hatırlanacak bir anıya dönüştürüyor."]),
 ],
 "faq":[
  ("Sapanca'da 30 veya 40 yaş doğum günü nerede kutlanır?","Didi Otel bahçesindeki Mare Gastro, gölün hemen yanında olması ve özenli servisiyle yuvarlak yaş doğum günü kutlamaları için uygun bir adrestir."),
  ("Yuvarlak yaş kutlamaları için özel bir hazırlık yapılıyor mu?","Evet, talebinize göre özel pasta, süsleme ve masa düzeni rezervasyon sırasında hazırlanır."),
  ("Kalabalık bir davetli listesiyle kutlama yapılabilir mi?","Evet, Mare Gastro farklı büyüklükte grupları ağırlayacak esnek masa düzenleri sunar."),
  ("Bu tür kutlamalar için ne kadar önceden rezervasyon gerekir?","Özellikle hafta sonları için birkaç gün önceden rezervasyon yapmanızı öneririz."),
 ],
 "rel":["sapanca-dogum-gunu-nerede-kutlanir","sapanca-kalabalik-arkadas-grubu-dogum-gunu","sapanca-dogum-gunu-pastasi-suslemeli-mekan"],
},
{
 "slug":"sapanca-istanbuldan-dogum-gunu-kacamagi",
 "cat":"dogumgunu","date":"2026-07-23","read":"6 dk",
 "img":"hero-mare-2.webp","alt":"Bahçede akşam atmosferi — İstanbul'dan Sapanca'ya doğum günü kaçamağı Mare Gastro",
 "h1":"İstanbul'dan <em>Sapanca'ya Doğum Günü Kaçamağı</em>: Nereye Gidilir?",
 "title":"İstanbul'dan Sapanca'ya Doğum Günü Kaçamağı | Mare Gastro",
 "desc":"İstanbul'dan yaklaşık 1,5 saat mesafedeki Sapanca'da doğum günü kaçamağı planlıyorsanız Mare Gastro, kolay ulaşım ve isteyenler için konaklama seçeneğiyle ideal bir adres.",
 "kw":"istanbuldan sapanca doğum günü, sapanca doğum günü kaçamağı, istanbula yakın doğum günü mekanı, istanbuldan bir günlük sapanca gezisi doğum günü",
 "lead":"İstanbul'un kalabalığından uzaklaşıp doğum gününü doğayla iç içe kutlamak isteyenler için Sapanca, ulaşımı kolay bir kaçamak noktası.",
 "body":[
  ("İstanbul'dan Sapanca'ya Ulaşım Ne Kadar Sürer?",
   ["Sapanca, İstanbul'a yaklaşık 1,5 saat mesafede; bu da <strong>İstanbul'dan doğum günü kaçamağı</strong> planlayanlar için Sapanca'yı pratik bir seçenek haline getiriyor. Yol boyunca trafik kaygısı yaşamadan, akşama yetişecek şekilde yola çıkabilirsiniz."]),
  ("Neden Bir Günlük Kaçamak İçin Sapanca?",
   ["Gölün hemen yanında olması, doğanın sessizliği ve İstanbul'un telaşından uzak bir atmosfer; bir günlük bir kaçamağı doğum günü kutlamasına dönüştürmek için ideal bir zemin sunuyor. Mare Gastro, bu kaçamağın merkezinde yer alıyor."]),
  ("İsterseniz Kalın: Didi Otel'de Konaklama Seçeneği",
   ["Akşam yemeğinin ardından İstanbul'a dönmek yerine gecelemek isteyenler için, Mare Gastro'nun bulunduğu Didi Otel bünyesinde konaklama seçeneği mevcut; böylece kaçamağınızı bir güne sığdırmak zorunda kalmazsınız.",
    bfig("mare-havuz-sezlong.webp","Didi Otel havuz başı şezlongları — İstanbul'dan Sapanca'ya doğum günü kaçamağı","Didi Otel havuz alanı")]),
  ("Otopark ve Pratik Bilgiler",
   ["Kendi aracınızla gelmeyi planlıyorsanız, Didi Otel'in geniş otopark imkânı ekstra bir planlama derdi bırakmıyor. %s güncel yol tarifi ve konum bilgisine ulaşabilirsiniz."%L(LOC,"Konum sayfamızdan")]),
 ],
 "faq":[
  ("İstanbul'dan Sapanca'ya ulaşım ne kadar sürer?","Sapanca, İstanbul'a yaklaşık 1,5 saat mesafededir."),
  ("Sapanca'da doğum günü kaçamağı için nereye gidilmeli?","Didi Otel bahçesindeki Mare Gastro, gölün hemen yanında olması ve kolay ulaşımıyla İstanbul'dan doğum günü kaçamağı için uygun bir adrestir."),
  ("Akşam yemeğinden sonra Sapanca'da konaklanabilir mi?","Evet, Mare Gastro'nun bulunduğu Didi Otel bünyesinde isteyen misafirler için konaklama seçeneği mevcuttur."),
  ("Otopark imkânı var mı?","Evet, Didi Otel bünyesinde geniş otopark imkânı bulunur."),
 ],
 "rel":["sapanca-dogum-gunu-nerede-kutlanir","istanbula-yakin-luks-restoran","sapanca-hafta-sonu-rotasi"],
},
{
 "slug":"sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri",
 "cat":"dogumgunu","date":"2026-07-24","read":"6 dk",
 "img":"dana-carpaccio.webp","alt":"Dana carpaccio — Sapanca'da doğum günü kutlama menüsü fiyat rehberi Mare Gastro",
 "h1":"Sapanca'da <em>Doğum Günü</em> Kutlama Fiyatları ve Menü Seçenekleri",
 "title":"Sapanca'da Doğum Günü Fiyatları ve Menü | Mare Gastro",
 "desc":"Sapanca'da doğum günü kutlamanın bütçesi ne kadar tutar? Mare Gastro'nun menü yapısı, imza tatlıları ve rezervasyon sürecini bu rehberde bulabilirsiniz.",
 "kw":"sapanca doğum günü fiyatları, sapanca doğum günü kutlama ücreti, sapanca doğum günü menü fiyat, sapanca fine dining doğum günü bütçe",
 "lead":"Sapanca'da doğum günü kutlamak için bütçe planlaması yaparken, mekanın sunduğu deneyimin kalitesiyle fiyatını birlikte değerlendirmek gerekir.",
 "body":[
  ("Sapanca'da Doğum Günü Kutlaması Fiyatı Neye Göre Değişir?",
   ["<strong>Sapanca'da doğum günü fiyatları</strong>, seçilen tabaklara, kişi sayısına, mevsime ve varsa pasta/süsleme taleplerine göre değişir. Mare Gastro'da sabit bir menü fiyatı yerine à la carte bir yapı benimseniyor.",
    "En net bilgiyi %s planınızı paylaştığınızda alabilirsiniz."%L(REZ,"rezervasyon sırasında ekibimizle görüşerek")]),
  ("Kişi Başı Ücrete Neler Dahildir?",
   ["Bir doğum günü sofrası; başlangıç, ana yemek ve tatlıdan oluşan bir akış, gölün hemen yanındaki bir masa ve özenli servisi kapsar. Özel pasta veya süsleme talep ederseniz, bu detay rezervasyon sırasında bütçenize göre netleştirilir.",
    bfig("mare-sofra-detay.webp","Özenle hazırlanmış sofra detayı — Sapanca doğum günü menü ve fiyat rehberi","Mare Gastro'da bir sofra detayı"),
    "%s hangi tabakların bütçenize uygun olduğunu önceden görebilirsiniz."%L(MENU,"Güncel menümüzü inceleyerek")]),
  ("Fiyat/Performans Açısından Nelere Dikkat Etmeli?",
   ["Bir doğum günü kutlamasında fiyatı belirleyen tek unsur porsiyon değildir; malzemenin tazeliği, gölün hemen yanında olması, Didi Otel'in kurumsal güvencesi ve hafta sonu canlı müzik atmosferi de deneyime eklenen değerler arasındadır."]),
  ("Güncel Fiyat Bilgisini Nereden Öğrenebilirim?",
   ["Mare Gastro sitede sabit bir fiyat listesi yayınlamaz; menü mevsimsel olarak güncellenir. %s veya WhatsApp üzerinden birkaç dakika içinde güncel bilgi alabilirsiniz."%L(REZ,"Rezervasyon formu")]),
 ],
 "faq":[
  ("Sapanca'da doğum günü kutlamasının sabit bir fiyatı var mı?","Hayır. Menü mevsimsel olarak güncellendiği için sabit bir fiyat listesi yerine, güncel bilgi rezervasyon sırasında paylaşılır."),
  ("Pasta ve süsleme fiyata dahil mi?","Pasta ve süsleme talepleri rezervasyon sırasında ayrıca değerlendirilir ve netleştirilir."),
  ("İçecekler fiyata dahil mi?","İçecekler à la carte olarak menüden ayrıca seçilir ve fiyata dahil değildir."),
  ("Güncel fiyat bilgisini nasıl öğrenebilirim?","Rezervasyon formunu doldurarak ya da WhatsApp üzerinden ekibimizle iletişime geçerek güncel bilgi alabilirsiniz."),
 ],
 "rel":["sapanca-dogum-gunu-nerede-kutlanir","sapanca-fine-dining-fiyat-rehberi","sapanca-30-40-yas-dogum-gunu-kutlamasi"],
},
{
 "slug":"sapanca-en-iyi-dogum-gunu-mekanlari",
 "cat":"dogumgunu","date":"2026-08-17","read":"7 dk",
 "img":"mare-kutlama-kadeh.webp","alt":"Kutlama kadehleri — Sapanca'da doğum günü için en iyi mekanlar karşılaştırması",
 "h1":"Sapanca'da Doğum Günü İçin <em>En İyi 5 Mekan</em>",
 "title":"Sapanca'da Doğum Günü İçin En İyi 5 Mekan | Mare Gastro",
 "desc":"Sapanca'da doğum günü kutlamak için en iyi 5 mekanı karşılaştırdık: göl manzarası, atmosfer ve kutlamaya uygunluk açısından Mare Gastro, Sasa Sapanca, Menzara, Green Blue ve Natürköy.",
 "kw":"sapanca en iyi doğum günü mekanları, sapanca doğum günü nerede kutlanır, sapanca göl kenarı restoran karşılaştırma, sapanca kutlama mekanları",
 "lead":"Sapanca'da doğum günü kutlayacağınız mekanı seçerken manzara, atmosfer, mutfak ve kutlamaya ne kadar uygun olduğu birlikte değerlendirilmeli. Bölgenin öne çıkan 5 adresini bu kriterlere göre karşılaştırdık.",
 "body":[
  ("Sapanca'da Doğum Günü Mekanı Seçerken Nelere Bakılmalı?",
   ["Sapanca Gölü çevresinde onlarca restoran var, ama her biri her kutlamaya uygun değil. Bir <strong>doğum günü mekanı</strong> seçerken dört şey öne çıkar: göl manzarası olup olmadığı, atmosferin kutlamaya (mum, pasta, sürpriz) izin verip vermediği, grup büyüklüğüne uygunluk ve mutfağın kalitesi.",
    "Aşağıdaki liste, bu kriterlere göre Sapanca'nın bilinen adreslerinden beşini karşılaştırıyor — sıralama Mare Gastro'nun kendi blogunda hazırlanmış olsa da, her mekanın gerçek ve doğrulanabilir özelliklerine dayanıyor."]),
  ("1. Mare Gastro — Gölün Hemen Yanında Fine Dining Kutlama",
   ["Didi Otel bahçesinde, gölün hemen kıyısında konumlanan Mare Gastro; doğum günlerine özel <strong>pasta ve masa süslemesi</strong> desteği sunan, Yönetici Şef Doğan Anapa imzalı Ege-Akdeniz mutfağıyla fine dining bir deneyim sunuyor. Cuma-Cumartesi-Pazar 24 saat açık olması, gece geç saatte planlanan kutlamalar için de esneklik sağlıyor.",
    bfig("mare-grup-sofra.webp","Gölün hemen yanında hazırlanmış bir grup sofrası — Mare Gastro doğum günü kutlaması","Mare Gastro'da bir kutlama sofrası"),
    "Öne çıkanlar: göl manzarası, %s, canlı müzik (hafta sonu), imza tatlılar."%L(MENU,"à la carte menü")]),
  ("2. Sasa Sapanca — Canlı Müzik Eşliğinde Göl Kıyısında",
   ["Göl kıyısında konumlanan Sasa Sapanca, dünya mutfağından geniş bir menü (mezeler, burger, taco, kırmızı et, balık) ve canlı müzik eşliğinde romantik bir akşam yemeği atmosferi sunuyor. Geniş menü yelpazesi, farklı damak tatlarına sahip kalabalık bir grubu ağırlamak isteyenler için pratik bir seçenek."]),
  ("3. Menzara — Karadeniz Mutfağı ve Balkon Manzarası",
   ["2010'dan beri hizmet veren Menzara, göl manzaralı balkonu ve Karadeniz ağırlıklı mutfağıyla (taş fırın ekmek, balık, ızgara) öne çıkıyor. Daha samimi, ev sıcaklığında bir kutlama atmosferi arayanlar için tercih edilen adreslerden."]),
  ("4. Green Blue — Aile ve Çocuklu Kutlamalar İçin Geniş Bahçe",
   ["Deniz ürünleri ağırlıklı menüsü ve geniş bahçesiyle Green Blue, özellikle çocuklu aile kutlamalarında pratik bir seçim. Bahçedeki çocuk oyun alanı, küçük yaş grubu doğum günlerinde ebeveynlere rahat bir alan sağlıyor."]),
  ("5. Natürköy — Doğa İçinde Aktiviteli Bir Kutlama",
   ["Vadi içinde, dere üzerine kurulu ahşap kulübeleriyle Natürköy, fine dining'den çok doğa temalı bir deneyim sunuyor. At binme ve zipline gibi aktivitelerle desteklenen bir kutlama isteyenler, özellikle gençlik grupları için bu adresi değerlendirebilir."]),
  ("Hangi Mekanı Seçmelisiniz?",
   ["Romantik ya da zarif bir fine dining kutlaması için göl manzarası ve mutfak kalitesi öne çıkan %s; canlı müzikli kalabalık bir akşam için Sasa Sapanca; samimi bir aile sofrası için Menzara; çocuklu kutlama için Green Blue; aktiviteli bir gün için Natürköy tercih edilebilir."%L(REZ,"Mare Gastro")]),
 ],
 "faq":[
  ("Sapanca'da doğum günü için en iyi mekan hangisi?","Bu, aradığınız deneyime göre değişir. Gölün hemen yanında fine dining bir kutlama için Mare Gastro, canlı müzikli kalabalık bir akşam için Sasa Sapanca, çocuklu aile kutlaması için Green Blue öne çıkan seçeneklerdir."),
  ("Mare Gastro doğum günü için pasta veya süsleme ayarlıyor mu?","Evet. Rezervasyon sırasında talebinizi ilettiğinizde pasta ve masa süslemesi detayları birlikte planlanır."),
  ("Sapanca'da göl manzaralı doğum günü mekanı hangileri?","Mare Gastro, Sasa Sapanca ve Menzara göl kıyısında veya göl manzaralı; Green Blue ve Natürköy daha çok bahçe/doğa odaklı bir atmosfer sunar."),
  ("Kalabalık bir arkadaş grubuyla doğum günü için hangi mekan uygun?","Geniş menü seçenekleri ve canlı müzik atmosferiyle Sasa Sapanca, ya da özel bir sofra için Mare Gastro değerlendirilebilir."),
 ],
 "rel":["sapanca-dogum-gunu-nerede-kutlanir","sapanca-gol-manzarali-dogum-gunu-mekanlari","sapanca-kalabalik-arkadas-grubu-dogum-gunu"],
},
{
 "slug":"sapanca-arkadaslarla-bulusma-mekani",
 "cat":"sosyal","date":"2026-08-17","read":"6 dk",
 "img":"mare-grup-sofra.webp","alt":"Arkadaş grubu sofrası — Sapanca'da arkadaşlarla buluşma ve keyifli akşam mekanı Mare Gastro",
 "h1":"Sapanca'da <em>Arkadaşlarla Buluşmak</em> İçin En İyi Mekan Önerisi",
 "title":"Sapanca'da Arkadaşlarla Buluşma Mekanı | Mare Gastro",
 "desc":"Vesilesiz, sadece keyifli bir akşam için Sapanca'da arkadaşlarla buluşulacak en iyi mekan nasıl seçilir? Göl manzarası, uzun sofra ve canlı müzik kriterleriyle bir rehber.",
 "kw":"sapanca arkadaşlarla buluşma mekanı, sapanca arkadaşlarla eğlenmek, sapanca akşam yemeği arkadaş grubu, sapanca göl kenarı akşam",
 "lead":"Özel bir vesile olmadan, sadece arkadaşlarla bir araya gelip keyifli bir akşam geçirmek için Sapanca'da doğru mekanı seçmek; göl manzarası, uzun bir sofraya imkan tanıyan düzen ve rahat bir atmosfer gerektirir.",
 "body":[
  ("Arkadaş Buluşması İçin Mekan Seçerken Nelere Dikkat Edilir?",
   ["Bir doğum günü ya da yıldönümü gibi özel bir tarih olmadan, sadece <strong>arkadaşlarla buluşmak</strong> için gidilecek mekan farklı kriterlere göre seçilir: uzun sohbetlere izin veren bir oturma düzeni, grubun tamamının rahat edeceği geniş bir menü ve gecenin ilerleyen saatlerine kadar açık kalabilen bir atmosfer.",
    "Sapanca'da bu ölçütlere uyan mekanlardan biri, gölün hemen kıyısındaki Mare Gastro."]),
  ("Neden Gölün Hemen Yanında Bir Sofra?",
   ["Sapanca Gölü'nün manzarası, kalabalık bir arkadaş sofrasına kendiliğinden bir atmosfer katıyor. Didi Otel bahçesinde kurulan masalar, hem sohbetin rahat aktığı hem de gün batımının eşlik ettiği bir ortam sunuyor.",
    bfig("mare-teras-misafir2.webp","Gölün hemen yanında teras sofrası — Sapanca'da arkadaşlarla akşam yemeği","Mare Gastro terasında bir akşam")]),
  ("Geniş Bir Grup İçin Menü Nasıl Planlanır?",
   ["Farklı damak zevklerine sahip bir arkadaş grubunu ağırlarken, à la carte bir menünün esnekliği önemlidir. %s deniz ürünlerinden ızgaraya, mezelerden imza tatlılara kadar geniş bir yelpaze sunuyor; grubun her üyesi kendi tercihini yapabiliyor."%L(MENU,"Mare Gastro'nun menüsü")]),
  ("Gece Geç Saate Kadar Sürecek Bir Buluşma İçin",
   ["Sohbetin uzadığı akşamlarda mekanın kapanış saati önemli bir detaydır. Mare Gastro, Cuma-Cumartesi-Pazar günleri 24 saat açık olduğu için, arkadaş buluşmasının ne zaman biteceğine dair bir kaygı taşımadan planlama yapılabilir. Hafta sonu canlı müzik de atmosfere eşlik ediyor."]),
  ("Rezervasyon Nasıl Yapılır?",
   ["Kalabalık bir grup için masa ayırtmak, %s üzerinden birkaç dakika sürer. Kişi sayısını belirttiğinizde, ekibimiz size en uygun düzeni hazırlar."%L(REZ,"üç adımlı rezervasyon formu")]),
 ],
 "faq":[
  ("Sapanca'da arkadaşlarla buluşmak için en iyi mekan neresi?","Göl manzarası, geniş menü seçenekleri ve gece geç saate kadar açık olma özelliğiyle Mare Gastro, arkadaş grubu buluşmaları için uygun bir adres."),
  ("Kalabalık bir arkadaş grubu için rezervasyon yapılabilir mi?","Evet, rezervasyon formunda kişi sayısını belirterek grubunuza uygun bir masa düzeni talep edebilirsiniz."),
  ("Sapanca'da gece geç saate kadar açık restoran var mı?","Mare Gastro, Cuma-Cumartesi-Pazar günleri 24 saat açık; hafta içi ise 18:00-00:00 arası hizmet veriyor."),
  ("Arkadaş buluşmasında canlı müzik oluyor mu?","Hafta sonu akşamlarında canlı müzik atmosfere eşlik ediyor."),
 ],
 "rel":["sapanca-kalabalik-arkadas-grubu-dogum-gunu","sapanca-gece-acik-restoran","sapanca-hafta-sonu-rotasi"],
},
{
 "slug":"sapancanin-en-iyi-restorani",
 "cat":"rehber","date":"2026-08-17","read":"7 dk",
 "img":"mare-aerial.jpg","alt":"Havadan görünüm — Sapanca'nın en iyi restoranları karşılaştırması Mare Gastro",
 "h1":"Sapanca'nın <em>En İyi Restoranı</em> Hangisi? Karşılaştırmalı Rehber",
 "title":"Sapanca'nın En İyi Restoranı Hangisi? | Mare Gastro",
 "desc":"Sapanca'nın en iyi restoranını ararken göl manzarası, mutfak kalitesi ve atmosfer neye göre karşılaştırılır? Mare Gastro, Sasa Sapanca, Menzara, Green Blue ve Natürköy'ü inceledik.",
 "kw":"sapanca en iyi restoran, sapanca en iyi restoranlar, sapanca gölü restoran, sapanca fine dining restoran",
 "lead":"\"Sapanca'nın en iyi restoranı hangisi?\" sorusunun tek bir cevabı yok — aranan deneyime göre değişiyor. Bölgenin öne çıkan adreslerini mutfak, konum ve atmosfer açısından karşılaştırdık.",
 "body":[
  ("Sapanca'da \"En İyi Restoran\" Neye Göre Belirlenir?",
   ["Sapanca'nın restoran haritası oldukça geniş: göl kıyısı kahvaltı mekanlarından fine dining adreslere kadar farklı segmentler bir arada. \"En iyi\" tanımı da buna göre değişir — bazıları için bu, mutfağın kalitesi; bazıları için manzara, bazıları için ise atmosfer ve hizmet anlamına gelir.",
    "Bu rehberde, bölgenin tekrar tekrar öne çıkan adreslerini bu üç eksende karşılaştırdık."]),
  ("Fine Dining Arayanlar İçin: Mare Gastro",
   ["Didi Otel bahçesinde, gölün hemen kıyısında yer alan Mare Gastro; Yönetici Şef Doğan Anapa imzasıyla Ege ve Akdeniz mutfağını fine dining bir sunumla buluşturuyor. Bölgede gerçek anlamda <strong>fine dining</strong> iddiası taşıyan az sayıdaki adresten biri.",
    bfig("hero-mare-1.jpg","Gölün hemen yanında fine dining sofrası — Sapanca'nın en iyi restoranı karşılaştırması","Mare Gastro'da bir akşam sofrası"),
    "%s ve gölü karşınıza alan bir masa, deneyimin iki temel unsuru."%L(MENU,"Mevsimsel à la carte menü")]),
  ("Dünya Mutfağı ve Canlı Müzik Arayanlar İçin: Sasa Sapanca",
   ["Göl kıyısındaki Sasa Sapanca, mezelerden burger ve tacoya kadar geniş bir dünya mutfağı menüsü ve hafta sonu canlı müzik eşliğinde bir atmosfer sunuyor. Farklı damak tatlarını bir arada ağırlamak isteyenler için pratik bir seçenek."]),
  ("Yöresel Lezzet Arayanlar İçin: Menzara",
   ["2010'dan beri hizmet veren Menzara, Karadeniz mutfağı ağırlıklı menüsü ve göl manzaralı balkonuyla daha samimi, ev sıcaklığında bir deneyim sunuyor."]),
  ("Aile ve Geniş Bahçe Arayanlar İçin: Green Blue",
   ["Deniz ürünleri ağırlıklı menüsü ve çocuk oyun alanlı geniş bahçesiyle Green Blue, aile ziyaretleri için tercih edilen adreslerden."]),
  ("Doğa ve Aktivite Arayanlar İçin: Natürköy",
   ["Vadi içinde, dere üzerine kurulu ahşap kulübeleriyle Natürköy, fine dining'den çok doğa temalı bir deneyim sunuyor; at binme ve zipline gibi aktivitelerle destekleniyor."]),
  ("Sonuç: Hangi Restoran Sizin İçin Doğru?",
   ["Gölün hemen yanında fine dining bir akşam için %s, geniş menü ve canlı müzik için Sasa Sapanca, yöresel lezzet için Menzara, aile ziyareti için Green Blue, doğa deneyimi için Natürköy öne çıkıyor. Sapanca'nın \"en iyisi\", aslında aradığınız deneyimle birlikte tanımlanıyor."%L(REZ,"Mare Gastro")]),
 ],
 "faq":[
  ("Sapanca'nın en iyi restoranı hangisi?","Bu, aranan deneyime bağlı. Fine dining ve göl manzarası için Mare Gastro, geniş dünya mutfağı ve canlı müzik için Sasa Sapanca, yöresel lezzet için Menzara öne çıkan adreslerdir."),
  ("Sapanca'da fine dining restoran var mı?","Evet. Mare Gastro, Didi Otel bahçesinde gölün hemen yanında, Şef Doğan Anapa imzasıyla fine dining bir deneyim sunuyor."),
  ("Sapanca'da göl manzaralı restoranlar hangileri?","Mare Gastro, Sasa Sapanca ve Menzara göl kıyısında veya göl manzaralı konumdadır."),
  ("Sapanca'da restoran seçerken nelere dikkat etmeli?","Aradığınız deneyime göre mutfak tipi (fine dining, dünya mutfağı, yöresel), konum (göl manzarası) ve atmosfer (canlı müzik, aile dostu, doğa) birlikte değerlendirilmeli."),
 ],
 "rel":["sapanca-luks-restoran","sapanca-fine-dining-nedir","sapancada-ne-yenir"],
},
{
 "slug":"sapanca-sevgililer-gunu-yemegi",
 "cat":"kutlama","date":"2026-08-17","read":"6 dk",
 "img":"mare-romantik-kadeh.webp","alt":"İkili kadeh kaldırma anı — Sapanca'da Sevgililer Günü yemeği Mare Gastro",
 "h1":"Sapanca'da <em>Sevgililer Günü</em> Yemeği: Gölün Hemen Yanında Romantik Bir Akşam",
 "title":"Sapanca'da Sevgililer Günü Yemeği | Mare Gastro",
 "desc":"14 Şubat'ta Sapanca'da romantik bir Sevgililer Günü yemeği için Mare Gastro: gölün hemen yanında mum ışığı, fine dining menü ve erken rezervasyon önerisi.",
 "kw":"sapanca sevgililer günü, sapanca sevgililer günü yemeği, sapanca 14 şubat restoran, sapanca romantik akşam yemeği sevgililer günü",
 "lead":"Sevgililer Günü'nde Sapanca'da nereye gidileceğini düşünüyorsanız, gölün hemen yanında, mum ışığında bir sofra bu özel akşamı unutulmaz kılabilir.",
 "body":[
  ("Sapanca'da Sevgililer Günü İçin Neden Gölün Hemen Yanı?",
   ["14 Şubat akşamı, yılın en çok rezervasyon alan gecelerinden biri. <strong>Sapanca'da Sevgililer Günü</strong> için doğru mekanı seçerken, atmosferin kalabalık ve gürültülü değil, sakin ve mahrem olması önemli. Didi Otel bahçesinde, gölün hemen kıyısında kurulan Mare Gastro sofraları, bu sakinliği doğal olarak sunuyor.",
    "Kış ayında gölün üzerine düşen ışıklar ve mum aydınlatması, kalabalık şehir restoranlarında bulunması zor bir atmosfer yaratıyor."]),
  ("Sevgililer Günü Akşamı Nasıl Geçer?",
   ["Mare Gastro'da sabit bir "+"\"Sevgililer Günü menüsü\""+" yerine, à la carte bir yapı benimseniyor — bu da çiftlerin kendi tercihlerine göre bir akşam kurgulamasına imkan tanıyor. Başlangıçlardan imza tatlılara kadar %s, romantik bir akşamın her aşamasını kapsıyor."%L(MENU,"güncel menü"),
    bfig("mare-sekerpare.webp","İmza tatlı detayı — Sapanca'da Sevgililer Günü akşam yemeği Mare Gastro","Mare Gastro'nun imza tatlılarından biri")]),
  ("Rezervasyonu Ne Zaman Yapmalı?",
   ["14 Şubat gibi özel tarihlerde masalar hızla doluyor. Sevgililer Günü için %s en az birkaç gün önceden yapılması, göl kenarındaki tercih ettiğiniz saati garantilemenin en güvenli yolu."%L(REZ,"rezervasyon")]),
  ("Sürpriz Planlıyorsanız",
   ["Bir sürpriz teklif ya da özel bir jest planlıyorsanız, rezervasyon sırasında bu detayı ekibimizle paylaşmanız yeterli — masa düzeni ve zamanlama buna göre planlanır."]),
 ],
 "faq":[
  ("Sapanca'da Sevgililer Günü için nereye gidilmeli?","Gölün hemen yanında, sakin ve romantik bir atmosfer arıyorsanız Mare Gastro, Didi Otel bahçesindeki konumuyla öne çıkan bir seçenek."),
  ("Sevgililer Günü'ne özel sabit bir menü var mı?","Hayır, Mare Gastro à la carte bir yapı benimser; çiftler kendi tercihlerine göre bir akşam kurgulayabilir."),
  ("Sevgililer Günü rezervasyonu ne zaman yapılmalı?","Talebin yoğun olduğu bir tarih olduğu için en az birkaç gün önceden rezervasyon yapılması önerilir."),
  ("Sevgililer Günü'nde sürpriz teklif planlanabilir mi?","Evet, rezervasyon sırasında ekibimizle paylaştığınız detaylara göre masa düzeni ve zamanlama planlanabilir."),
 ],
 "rel":["sapanca-romantik-aksam-yemegi","sapanca-evlilik-teklifi","sapanca-yildonumu-yemegi"],
},
{
 "slug":"sapanca-nisan-yemegi",
 "cat":"romantik","date":"2026-08-17","read":"6 dk",
 "img":"hero-mare-2.jpg","alt":"Gölün hemen yanında zarif sofra — Sapanca'da nişan yemeği Mare Gastro",
 "h1":"Sapanca'da <em>Nişan Yemeği</em>: Gölün Hemen Yanında Zarif Bir Kutlama",
 "title":"Sapanca'da Nişan Yemeği | Mare Gastro Fine Dining",
 "desc":"Nişan sonrası ailece veya çift olarak kutlama yemeği için Sapanca'da Mare Gastro: gölün hemen yanında zarif bir sofra, geniş menü ve rezervasyon kolaylığı.",
 "kw":"sapanca nişan yemeği, sapanca nişan sonrası yemek, sapanca nişan kutlaması restoran, sapanca ailece nişan yemeği",
 "lead":"Nişan töreninin ardından ailece ya da yakın çevreyle oturulacak bir kutlama yemeği için Sapanca'da gölün hemen yanında bir sofra, günün anlamına yakışan bir kapanış sunar.",
 "body":[
  ("Nişan Yemeği İçin Neden Sapanca?",
   ["Nişan töreni genellikle kalabalık ve hareketli geçer; törenin ardından ailenin ve yakın çevrenin bir araya geldiği <strong>nişan yemeği</strong> ise daha sakin, oturaklı bir atmosfer ister. Sapanca'nın göl manzarası ve Didi Otel bahçesinin sakinliği, bu geçişi kolaylaştırıyor.",
    "Nişan yemeği, evlilik teklifinin kendisinden farklı bir andır — burada odak artık iki ailenin ve yakın çevrenin birlikte kutlamasıdır."]),
  ("Kalabalık Bir Aile Sofrası Nasıl Planlanır?",
   ["Nişan yemeğine genellikle iki aile ve yakın çevre katılır; bu da geniş bir grup için masa düzeni gerektirir. %s'nun geniş à la carte menüsü, farklı damak zevklerine sahip kalabalık bir sofrayı rahatça ağırlıyor."%L(MENU,"Mare Gastro")]),
  ("Zarif Bir Atmosfer İçin Detaylar",
   ["Gölün hemen yanındaki masa düzeni, mum ışığı ve hafta sonu canlı müzik, nişan yemeğine görsel ve duygusal bir bütünlük katıyor.",
    bfig("mare-teras-misafir2.webp","Didi Otel terasında zarif bir kutlama anı — Sapanca'da nişan yemeği","Mare Gastro terasında bir aile kutlaması")]),
  ("Rezervasyon ve Grup Planlaması",
   ["Kalabalık bir aile grubu için %s üzerinden kişi sayısını belirterek rezervasyon yapabilir, ekibimizden size uygun masa düzenini talep edebilirsiniz."%L(REZ,"rezervasyon formu")]),
 ],
 "faq":[
  ("Sapanca'da nişan yemeği için hangi mekan uygun?","Gölün hemen yanında, geniş bir aile grubunu ağırlayabilecek bir atmosfer arıyorsanız Mare Gastro, Didi Otel bahçesindeki konumuyla öne çıkıyor."),
  ("Nişan yemeği için kaç kişilik rezervasyon yapılabilir?","Kişi sayısını rezervasyon formunda belirttiğinizde, ekibimiz grubunuza uygun bir masa düzeni hazırlar."),
  ("Nişan yemeği ile evlilik teklifi yemeği aynı mı?","Hayır. Evlilik teklifi daha mahrem, iki kişilik bir andır; nişan yemeği ise törenin ardından ailelerin ve yakın çevrenin bir araya geldiği daha kalabalık bir kutlamadır."),
  ("Nişan yemeğinde canlı müzik oluyor mu?","Hafta sonu akşamlarında canlı müzik atmosfere eşlik ediyor."),
 ],
 "rel":["sapanca-evlilik-teklifi","sapanca-kalabalik-arkadas-grubu-dogum-gunu","sapanca-yildonumu-yemegi"],
},
{
 "slug":"sapancaya-nasil-gidilir",
 "cat":"rehber","date":"2026-08-17","read":"5 dk",
 "img":"header.webp","alt":"Mare Gastro girişi — Sapanca'ya nasıl gidilir, Didi Otel bahçesi yol tarifi",
 "h1":"Sapanca'ya ve Mare Gastro'ya <em>Nasıl Gidilir?</em>",
 "title":"Sapanca'ya Nasıl Gidilir? Mare Gastro Yol Tarifi",
 "desc":"İstanbul, Kocaeli ve Ankara yönünden Sapanca'ya nasıl gidilir? Mare Gastro'nun Didi Otel bahçesindeki konumu, adresi ve ulaşım bilgileri.",
 "kw":"sapancaya nasıl gidilir, sapanca yol tarifi, mare gastro adres, sapanca didi otel nasıl gidilir, sapanca ulaşım",
 "lead":"Sapanca, İstanbul'a yaklaşık 1,5 saat mesafede, D-100 ve TEM otoyolu üzerinden kolayca ulaşılabilen bir gölkenarı kasabası. Mare Gastro'ya ulaşım da bir o kadar pratik.",
 "body":[
  ("Mare Gastro'nun Adresi Neresi?",
   ["Mare Gastro, Sapanca'da <strong>Didi Otel</strong> bahçesinde, gölün hemen kıyısında yer alıyor. Açık adres: Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, 54600 Sapanca/Sakarya."]),
  ("İstanbul'dan Sapanca'ya Nasıl Gidilir?",
   ["İstanbul'un Anadolu yakasından TEM Otoyolu üzerinden Sapanca'ya araçla yaklaşık 1-1,5 saat sürüyor. Avrupa yakasından gelenler için süre trafiğe bağlı olarak 2 saate kadar uzayabilir. %s bu kısa mesafede kolay bir hafta sonu kaçamağı sunuyor."%L(REZ,"Bir akşam rezervasyonu")]),
  ("Kocaeli ve Ankara Yönünden Ulaşım",
   ["Kocaeli/İzmit yönünden Sapanca'ya araçla yaklaşık 30-40 dakika, Ankara yönünden ise TEM Otoyolu üzerinden yaklaşık 4 saat sürüyor. Otoyol çıkışından sonra Sapanca Gölü çevresini takip eden yol, Didi Otel'e ve Mare Gastro'ya yönlendiriyor."]),
  ("Toplu Taşıma ile Ulaşım",
   ["Sapanca'ya İstanbul'dan tren (YHT ile Arifiye/Sapanca istasyonu) ya da şehirlerarası otobüs seferleriyle de ulaşılabiliyor. Gölün etrafındaki mesafe göz önüne alındığında, otel/restorana ulaşım için taksi ya da araç kiralama pratik bir seçenek."]),
  ("Rezervasyon ve İletişim",
   ["Yol tarifinde veya rezervasyonda yardım için %s üzerinden ekibimize ulaşabilirsiniz."%L(WA,"WhatsApp")]),
 ],
 "faq":[
  ("Mare Gastro'nun adresi nedir?","Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, 54600 Sapanca/Sakarya — Didi Otel bahçesinde, gölün hemen kıyısında."),
  ("İstanbul'dan Sapanca'ya kaç saatte gidilir?","Anadolu yakasından yaklaşık 1-1,5 saat, Avrupa yakasından trafiğe bağlı olarak 2 saate kadar sürebilir."),
  ("Sapanca'ya trenle gidilebilir mi?","Evet, YHT ile Arifiye/Sapanca istasyonuna ulaşım mümkün; oradan otel/restorana taksi ile geçilebilir."),
  ("Mare Gastro'ya araçla gidince nereye park edilir?","Restoranın vale ve ücretsiz otopark imkanı bulunuyor."),
 ],
 "rel":["sapanca-hafta-sonu-rotasi","istanbula-yakin-luks-restoran","sapanca-istanbuldan-dogum-gunu-kacamagi"],
},
{
 "slug":"mare-gastro-hikayesi",
 "cat":"hikaye","date":"2026-08-17","read":"6 dk",
 "img":"dogansef.webp","alt":"Şef Doğan Anapa mutfakta — Mare Gastro'nun hikayesi ve felsefesi",
 "h1":"Mare Gastro'nun <em>Hikayesi</em>: Gölün Kıyısında Bir Fine Dining Felsefesi",
 "title":"Mare Gastro'nun Hikayesi ve Felsefesi | Sapanca",
 "desc":"Mare Gastro nasıl doğdu? Didi Otel bahçesinde, Şef Doğan Anapa imzasıyla şekillenen Ege-Akdeniz mutfağının ve gölün hemen yanındaki fine dining felsefesinin hikayesi.",
 "kw":"mare gastro hikayesi, mare gastro felsefesi, mare gastro kimdir, sapanca mare gastro restoran hikayesi, didi otel mare gastro",
 "lead":"Bir restoranı sadece menüsü değil, arkasındaki hikaye ve felsefe de tanımlar. Mare Gastro'nun hikayesi; Sapanca Gölü, Didi Otel bahçesi ve bir şefin mutfağa taşıdığı bakış açısıyla şekilleniyor.",
 "body":[
  ("Mare Gastro Nerede ve Nasıl Doğdu?",
   ["Mare Gastro, Sapanca Gölü'nün hemen kıyısındaki <strong>Didi Otel</strong>'in bahçesinde, %s felsefesiyle hayata geçirildi: gölün doğal dokusunu bozmadan, ona bir fine dining deneyimi eklemek."%L(STORY,"Kadir Çiçek tarafından tasarlanan bir konsept")]),
  ("Neden \"Mare\"?",
   ["İsim, Akdeniz'in ruhuna bir gönderme. Mare Gastro'nun mutfağı, Ege ve Akdeniz'in taze, sade ve malzemeye saygılı anlayışını; Sapanca Gölü'nün huzurlu atmosferiyle birleştiriyor.",
    bfig("mare-bahce-manzarasi.webp","Didi Otel bahçesinden Mare Gastro'nun genel görünümü — Sapanca","Mare Gastro'nun göl kıyısındaki konumu")]),
  ("Mutfağın Arkasındaki İsim: Doğan Anapa",
   ["Yönetici Şef %s, sinema sektöründeki geçmişinden mutfağa taşıdığı hikaye anlatıcılığıyla tanınıyor. Her menü, onun için bir sahne kurgusu gibi işliyor — başlangıçtan tatlıya, bir akışın parçası."%L(CHEF,"Doğan Anapa")]),
  ("Fine Dining ama Gösterişsiz",
   ["Mare Gastro'nun felsefesi, ağır ve gösterişli bir fine dining anlayışından çok; malzemenin kalitesini öne çıkaran, sade ve içten bir sunuma dayanıyor. Gölün manzarası zaten kendi başına bir sahne kurduğu için, tabaktaki sunum bu sakinliği bozmadan tamamlıyor."]),
  ("Bugün Mare Gastro",
   ["Bugün Mare Gastro, Cuma-Cumartesi-Pazar günleri 24 saat açık, hafta sonu canlı müzik eşliğinde, %s ile Sapanca'da fine dining arayanların adresi haline geldi."%L(MENU,"mevsimsel bir menü")]),
 ],
 "faq":[
  ("Mare Gastro kimin projesi?","Mare Gastro, Didi Otel bahçesinde Kadir Çiçek tarafından tasarlanan bir konsept olarak hayata geçirildi; mutfağın başında Yönetici Şef Doğan Anapa var."),
  ("Mare Gastro'nun mutfak anlayışı nedir?","Ege ve Akdeniz mutfağının sade, malzemeye saygılı anlayışı; taze deniz ürünleri ve mevsimsel tabaklarla öne çıkıyor."),
  ("Mare Gastro nerede yer alıyor?","Sapanca Gölü'nün hemen kıyısında, Didi Otel'in bahçesinde."),
  ("Şef Doğan Anapa'nın geçmişi nedir?","Sinema sektöründen mutfağa geçiş yapan Doğan Anapa, bu hikaye anlatıcılığını menü kurgusuna da taşıyor."),
 ],
 "rel":["sef-dogan-anapa-kimdir","sef-dogan-anapa","didi-otel-restoran"],
},
{
 "slug":"sapanca-evcil-hayvan-dostu-restoran",
 "cat":"rehber","date":"2026-08-17","read":"5 dk",
 "img":"mare-bahce-havuz-yolu.webp","alt":"Didi Otel bahçesinden yürüyüş yolu — Sapanca'da evcil hayvan dostu restoran Mare Gastro",
 "h1":"Sapanca'da <em>Evcil Hayvan Dostu</em> Restoran: Mare Gastro",
 "title":"Sapanca'da Evcil Hayvan Dostu Restoran | Mare Gastro",
 "desc":"Sapanca'da köpeğinizle veya kediyle gidebileceğiniz evcil hayvan dostu bir restoran mı arıyorsunuz? Mare Gastro, Didi Otel bahçesinde geniş açık alanıyla dostlarınızı ağırlıyor.",
 "kw":"sapanca evcil hayvan dostu restoran, sapanca köpekle gidilecek restoran, sapanca pet friendly restoran, sapanca evcil dostu mekan",
 "lead":"Dört ayaklı dostunuzu geride bırakmak istemiyorsanız, Sapanca'da evcil hayvan dostu bir restoran arayışınızda Mare Gastro'nun geniş bahçesi iyi bir seçenek sunuyor.",
 "body":[
  ("Mare Gastro'ya Evcil Hayvanla Gidilebilir mi?",
   ["Evet. Mare Gastro, Didi Otel'in geniş bahçesinde konumlanan açık alan düzeniyle <strong>evcil hayvan dostu</strong> bir restoran deneyimi sunuyor. Köpeğiniz veya kediniz, gölün hemen yanındaki masanızda sizinle birlikte olabilir."]),
  ("Neden Açık Alan Avantajlı?",
   ["Gölün hemen kıyısındaki geniş bahçe düzeni, hem dostunuzun rahatça hareket edebileceği bir alan hem de sizin için huzurlu bir sofra sunuyor. Kapalı, dar bir mekana kıyasla açık hava atmosferi, evcil hayvanlı bir akşam yemeği için doğal olarak daha uygun."]),
  ("Rezervasyon Sırasında Ne Yapmalı?",
   ["Evcil hayvanınızla geleceğinizi %s sırasında belirtmeniz, size bahçede uygun bir masa ayarlanmasına yardımcı olur."%L(REZ,"rezervasyon")]),
 ],
 "faq":[
  ("Mare Gastro'ya köpeğimle gidebilir miyim?","Evet, Mare Gastro'nun geniş bahçe alanı evcil hayvan dostu bir düzene sahiptir."),
  ("Evcil hayvanlar restoranın hangi bölümünde olabilir?","Gölün hemen yanındaki açık bahçe alanında dostunuzla birlikte oturabilirsiniz."),
  ("Rezervasyon sırasında evcil hayvan bilgisi vermeli miyim?","Evet, önceden belirtmeniz size uygun bir masa ayarlanmasını kolaylaştırır."),
 ],
 "rel":["sapanca-yazin-acik-hava-restoran","sapanca-hafta-sonu-rotasi","sapancada-ne-yenir"],
},
{
 "slug":"sapanca-vale-otopark-restoran",
 "cat":"rehber","date":"2026-08-17","read":"4 dk",
 "img":"hero-mare-1.webp","alt":"Mare Gastro girişi — Sapanca'da vale ve ücretsiz otopark hizmeti sunan restoran",
 "h1":"Sapanca'da <em>Vale ve Ücretsiz Otopark</em> Hizmeti Sunan Restoran",
 "title":"Sapanca'da Vale ve Ücretsiz Otopark | Mare Gastro",
 "desc":"Sapanca'da araçla gidip park sorunu yaşamadan yemek yiyebileceğiniz bir restoran mı arıyorsunuz? Mare Gastro, vale hizmeti ve ücretsiz otoparkıyla konforlu bir varış sunuyor.",
 "kw":"sapanca vale hizmeti restoran, sapanca ücretsiz otopark restoran, sapanca otoparklı restoran, sapanca valeli restoran",
 "lead":"Sapanca'da özellikle hafta sonu akşamları park yeri bulmak sıkıntılı olabilir. Mare Gastro, vale hizmeti ve ücretsiz otoparkıyla bu konuda içinizi rahatlatıyor.",
 "body":[
  ("Mare Gastro'da Vale Hizmeti Var mı?",
   ["Evet. Didi Otel bahçesindeki Mare Gastro'ya araçla geldiğinizde, <strong>vale hizmeti</strong> aracınızı sizin adınıza park ediyor — özellikle kalabalık hafta sonu akşamlarında park yeri aramakla vakit kaybetmenize gerek kalmıyor."]),
  ("Otopark Ücretli mi?",
   ["Hayır, Mare Gastro'nun otoparkı ücretsiz. Rezervasyonunuzla gelen misafirler için ek bir otopark ücreti alınmıyor."]),
  ("Kalabalık Bir Akşamda Ne Beklemeli?",
   ["Hafta sonu ve özel günlerde (Sevgililer Günü, yılbaşı gibi) talebin yüksek olduğu akşamlarda, vale hizmeti sayesinde varışınız yine de sorunsuz geçiyor. %s planlamanızı kolaylaştırıyor."%L(REZ,"Önceden rezervasyon yapmak")]),
 ],
 "faq":[
  ("Mare Gastro'da vale hizmeti var mı?","Evet, restorana araçla gelen misafirler için vale hizmeti sunuluyor."),
  ("Otopark ücretli mi?","Hayır, Mare Gastro'nun otoparkı ücretsizdir."),
  ("Hafta sonu akşamları park yeri bulma sorunu yaşanır mı?","Vale hizmeti sayesinde yoğun akşamlarda da park sorunu yaşanmıyor."),
 ],
 "rel":["sapancaya-nasil-gidilir","sapanca-hafta-sonu-rotasi","sapanca-gece-acik-restoran"],
},
{
 "slug":"sapanca-istanbula-yakin-evlilik-teklifi-mekanlari",
 "cat":"romantik","date":"2026-08-26","read":"8 dk",
 "img":"ai-golde-teklif-sofrasi.jpg","alt":"Gölün hemen yanında gün batımında evlilik teklifi sofrası — İstanbul'a yakın evlilik teklifi mekanı Mare Gastro",
 "h1":"İstanbul'a Yakın <em>Evlilik Teklifi</em> İçin En İyi 5 Mekan",
 "title":"İstanbul'a Yakın Evlilik Teklifi İçin En İyi 5 Mekan | Mare Gastro",
 "desc":"İstanbul'a yakın, unutulmaz bir evlilik teklifi için en iyi 5 mekanı karşılaştırdık: mahremiyet, göl manzarası, sürpriz organizasyonu ve Google yorumları açısından Mare Gastro, Sasa Sapanca, Menzara, Green Blue ve Natürköy.",
 "kw":"istanbula yakın evlilik teklifi mekanları, sapanca evlilik teklifi mekanı, istanbul yakını romantik mekan, sapanca sürpriz teklif mekanı",
 "lead":"İstanbul'a çok uzaklaşmadan, hayatınızın en önemli sorusunu sorabileceğiniz sahneyi ararken mahremiyet, manzara ve doğru organizasyon birlikte düşünülmeli. İstanbul'a yaklaşık 1,5 saat mesafedeki Sapanca'nın öne çıkan 5 adresini bu kriterlere göre karşılaştırdık.",
 "body":[
  ("İstanbul'a Yakın Bir Evlilik Teklifi Mekanı Seçerken Nelere Bakılmalı?",
   ["İstanbul'dan bir günlük mesafede, sürpriz bir teklife uygun bir mekan ararken beş şey öne çıkar: %s ulaşım süresi, göl manzarası olup olmadığı, mahremiyet sunan özel bir köşenin varlığı, sürpriz organizasyona (pasta, çiçek, müzik) izin verilip verilmediği ve mekanın %s gerçek misafir memnuniyeti."%(L(post_url("istanbula-yakin-luks-restoran"),"İstanbul'a"),L(MAPS,"Google yorumlarındaki")),
    "Aşağıdaki liste, bu kriterlere göre Sapanca'nın öne çıkan 5 adresini karşılaştırıyor — sıralama Mare Gastro'nun kendi blogunda hazırlanmış olsa da, her mekanın gerçek ve doğrulanabilir özelliklerine dayanıyor."]),
  ("1. Mare Gastro — İstanbul'a 1,5 Saat, Gölün Hemen Yanında Mahrem Bir Sahne",
   ["%s bahçesinde, gölün hemen kıyısında konumlanan Mare Gastro; İstanbul'a yaklaşık 1,5 saat mesafede olmasına karşın şehrin kalabalığından tamamen kopuk bir atmosfer sunuyor. Çam ağaçlarının arasındaki özel köşe masalar, teklif anının mahremiyetini korurken gölün manzarası sahneyi tamamlıyor."%L(DIDIWEB,"Didi Otel"),
    bfig("mare-romantik-kadeh.webp","İkili kadeh kaldırma anı — İstanbul'a yakın evlilik teklifi mekanı Mare Gastro","Mare Gastro'da bir kutlama anı"),
    "Rezervasyon sırasında iletilen talepler doğrultusunda özel pasta, çiçek düzenlemesi ve masaya özel bir not gibi sürpriz detaylar planlanıyor — konuyu %s adımlarıyla daha ayrıntılı okuyabilirsiniz."%L(post_url("sapanca-evlilik-teklifi"),"evlilik teklifi rehberimizde"),
    "Öne çıkanlar: göl manzarası, %s, mahrem köşe masalar, imza tatlılar, isteyenler için Didi Otel'de konaklama seçeneği."%L(MENU,"à la carte menü")]),
  ("2. Sasa Sapanca — Canlı Müzik Eşliğinde Göl Kıyısında",
   ["Göl kıyısında konumlanan Sasa Sapanca, dünya mutfağından geniş bir menü (mezeler, burger, taco, kırmızı et, balık) ve canlı müzik eşliğinde bir akşam yemeği atmosferi sunuyor. Canlı müzik ve kalabalık masa düzeni, geniş bir menü arayanlar için avantaj olsa da, mahrem bir teklif anı için daha sessiz bir köşe planlamak gerekebilir."]),
  ("3. Menzara — Karadeniz Mutfağı ve Balkon Manzarası",
   ["2010'dan beri hizmet veren Menzara, göl manzaralı balkonu ve Karadeniz ağırlıklı mutfağıyla (taş fırın ekmek, balık, ızgara) öne çıkıyor. Daha samimi, ev sıcaklığında bir atmosfer arayan çiftler için değerlendirilebilecek adreslerden."]),
  ("4. Green Blue — Aile ve Çocuklu Kutlamalar İçin Geniş Bahçe",
   ["Deniz ürünleri ağırlıklı menüsü ve geniş bahçesiyle Green Blue, özellikle çocuklu aile ziyaretlerinde pratik bir seçim. Aile odaklı atmosferi, mahrem bir teklif anından çok toplu kutlamalar için uygun."]),
  ("5. Natürköy — Doğa İçinde Sürpriz Bir Teklif Sahnesi",
   ["Vadi içinde, dere üzerine kurulu ahşap kulübeleriyle Natürköy, fine dining'den çok doğa temalı bir deneyim sunuyor. At binme ve zipline gibi aktivitelerin ardından doğa içinde sürpriz bir teklif kurgulamak isteyen çiftler için değerlendirilebilir."]),
  ("Mare Gastro'yu İstanbul'a Yakın Evlilik Teklifi İçin Öne Çıkaran Detaylar",
   ["Beş mekanı yan yana koyduğumuzda, Mare Gastro'yu öne çıkaran fark birkaç kriterin aynı anda karşılanması:",
    "<ul><li><strong>Mesafe:</strong> İstanbul'a yaklaşık 1,5 saat — bir günlük bir teklif planı için idealdir.</li><li><strong>Mahremiyet:</strong> Çam ağaçları arasındaki özel köşe masalar, teklif anını meraklı gözlerden korur.</li><li><strong>Sürpriz organizasyonu:</strong> Pasta, çiçek ve masa süslemesi rezervasyon sürecinin standart bir parçası.</li><li><strong>Konaklama güvencesi:</strong> %s bahçesinde olması, akşamı bir gece konaklamayla uzatma imkanı sunar.</li><li><strong>Misafir memnuniyeti:</strong> %s bölgenin özel gün mekanları arasında en çok övülenlerden biri.</li></ul>"%(L(DIDIWEB,"Didi Otel"),L(MAPS,"Google yorumlarında"))]),
  ("Google Yorumlarında Mare Gastro Neden Öne Çıkıyor?",
   ["Bir teklif anını emanet edeceğiniz mekanı seçmeden önce %s göz atmanızı öneririz. Misafirler en çok gölün hemen kenarındaki manzarayı, sürpriz organizasyondaki özeni ve servis ekibinin o ana gösterdiği ilgiyi övüyor. Güncel kutlama anlarını %s ve %s hesaplarından takip edebilirsiniz."%(L(MAPS,"Mare Gastro'nun Google Haritalar sayfasındaki yorumlarına"),L(IG,"Instagram"),L(YT,"YouTube"))]),
  ("Hangi Mekanı Seçmelisiniz?",
   ["İstanbul'a yakın, mahrem ve göl manzaralı bir evlilik teklifi için %s listedeki en eksiksiz seçenek; canlı müzikli kalabalık bir akşam için Sasa Sapanca; samimi bir sofra için Menzara; aile ziyareti için Green Blue; doğa temalı bir sürpriz için Natürköy tercih edilebilir."%L(REZ,"Mare Gastro"),
    "Teklif öncesi %s ve %s göz atarak akşamınızı baştan sona planlayabilirsiniz."%(L(post_url("sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri"),"fiyat ve menü seçeneklerine"),L(post_url("didi-otel-restoran"),"Didi Otel bahçesindeki restoran deneyimine"))]),
 ],
 "faq":[
  ("İstanbul'a en yakın evlilik teklifi mekanı hangisi?","İstanbul'a yaklaşık 1,5 saat mesafedeki Sapanca'da, gölün hemen yanındaki Didi Otel bahçesinde konumlanan Mare Gastro; mahrem köşe masaları ve sürpriz organizasyon desteğiyle en çok tercih edilen adreslerden biri."),
  ("Mare Gastro'da sürpriz teklif organizasyonu yapılıyor mu?","Evet. Rezervasyon sırasında iletilen talepler doğrultusunda özel pasta, çiçek düzenlemesi ve masaya özel bir not gibi sürpriz detaylar planlanır."),
  ("İstanbul'dan Sapanca'ya ne kadar sürede gidilir?","Trafik durumuna göre yaklaşık 1,5 saat sürer; bu da Sapanca'yı bir günlük teklif planları için ideal kılar."),
  ("Mare Gastro'nun Google yorumlarındaki puanı nasıl?","Mare Gastro, Sapanca'daki özel gün mekanları arasında Google yorumlarında en çok övülen adreslerden biri. Güncel yorumları Google Haritalar'daki işletme sayfasından görebilirsiniz."),
  ("Teklif sonrası konaklama mümkün mü?","Mare Gastro, Didi Otel bünyesindedir; akşamı bir gece konaklamayla uzatmak isteyenler rezervasyon formunda konaklama tercihini belirtebilir."),
 ],
 "rel":["sapanca-evlilik-teklifi","istanbula-yakin-luks-restoran","sapanca-romantik-aksam-yemegi"],
},
{
 "slug":"sapanca-istanbula-yakin-luks-dogum-gunu-mekanlari",
 "cat":"dogumgunu","date":"2026-08-26","read":"8 dk",
 "img":"ai-luks-dogum-gunu-terasi.jpg","alt":"Gölün hemen yanında akşam ışıklarıyla süslü doğum günü sofrası — İstanbul'a yakın lüks doğum günü mekanı Mare Gastro",
 "h1":"İstanbul'a Yakın Doğum Günü İçin En İyi 5 <em>Lüks Mekan</em>",
 "title":"İstanbul'a Yakın Doğum Günü İçin En İyi 5 Lüks Mekan | Mare Gastro",
 "desc":"İstanbul'a yakın, lüks bir doğum günü kutlaması için en iyi 5 mekanı karşılaştırdık: ulaşım, fine dining seviyesi, kutlama hizmeti ve Google yorumları açısından Mare Gastro, Sasa Sapanca, Menzara, Green Blue ve Natürköy.",
 "kw":"istanbula yakın doğum günü lüks mekanları, istanbul yakını lüks doğum günü mekanı, sapanca doğum günü kaçamağı, istanbula yakın fine dining kutlama",
 "lead":"İstanbul'dan uzaklaşmadan lüks bir doğum günü kutlaması ararken ulaşım süresi, fine dining seviyesi ve kutlamaya özel hizmet birlikte değerlendirilmeli. İstanbul'a yaklaşık 1,5 saat mesafedeki Sapanca'nın öne çıkan 5 adresini bu kriterlere göre karşılaştırdık.",
 "body":[
  ("İstanbul'a Yakın Lüks Bir Doğum Günü Mekanı Seçerken Nelere Bakılmalı?",
   ["Şehrin dışına çıkıp lüks bir doğum günü kutlaması planlarken dört şey öne çıkar: İstanbul'a ulaşım süresi, mekanın gerçek anlamda fine dining seviyesinde olup olmadığı, pasta/süsleme gibi kutlama hizmetlerinin sunulup sunulmadığı ve %s gerçek misafir memnuniyeti."%L(MAPS,"Google yorumlarındaki"),
    "Aşağıdaki liste, bu kriterlere göre Sapanca'nın öne çıkan 5 adresini karşılaştırıyor — sıralama Mare Gastro'nun kendi blogunda hazırlanmış olsa da, her mekanın gerçek ve doğrulanabilir özelliklerine dayanıyor."]),
  ("1. Mare Gastro — İstanbul'a Yakın, Google Yorumlarında Öne Çıkan Lüks Kutlama",
   ["%s bahçesinde, gölün hemen kıyısında konumlanan Mare Gastro; İstanbul'a yaklaşık 1,5 saatlik mesafeye karşın gerçek bir fine dining standardı taşıyor. %s imzalı Ege-Akdeniz mutfağı, doğum günlerine özel pasta ve masa süslemesi desteğiyle birleşiyor."%(L(DIDIWEB,"Didi Otel"),L(post_url("sef-dogan-anapa-kimdir"),"Yönetici Şef Doğan Anapa")),
    bfig("mare-kutlama-kadeh.webp","Kutlama kadehleri — İstanbul'a yakın lüks doğum günü mekanı Mare Gastro","Mare Gastro'da bir kutlama anı"),
    "Bu özenin karşılığı %s da yansıyor: misafirler en çok göl manzarasını, servis kalitesini ve pasta/süsleme detaylarındaki inceliği övüyor."%L(MAPS,"Google yorumlarına"),
    "Öne çıkanlar: göl manzarası, %s, %s, isteyenler için Didi Otel'de konaklama seçeneği."%(L(post_url("sapanca-dogum-gunu-pastasi-suslemeli-mekan"),"pasta ve masa süslemesi"),L(MENU,"à la carte menü"))]),
  ("2. Sasa Sapanca — Canlı Müzik Eşliğinde Göl Kıyısında",
   ["Göl kıyısında konumlanan Sasa Sapanca, dünya mutfağından geniş bir menü (mezeler, burger, taco, kırmızı et, balık) ve canlı müzik eşliğinde bir akşam yemeği atmosferi sunuyor. Geniş menü yelpazesi, farklı damak tatlarına sahip kalabalık bir grubu ağırlamak isteyenler için pratik bir seçenek."]),
  ("3. Menzara — Karadeniz Mutfağı ve Balkon Manzarası",
   ["2010'dan beri hizmet veren Menzara, göl manzaralı balkonu ve Karadeniz ağırlıklı mutfağıyla (taş fırın ekmek, balık, ızgara) öne çıkıyor. Daha samimi, ev sıcaklığında bir kutlama atmosferi arayanlar için tercih edilen adreslerden."]),
  ("4. Green Blue — Aile ve Çocuklu Kutlamalar İçin Geniş Bahçe",
   ["Deniz ürünleri ağırlıklı menüsü ve geniş bahçesiyle Green Blue, özellikle çocuklu aile kutlamalarında pratik bir seçim. Bahçedeki çocuk oyun alanı, küçük yaş grubu doğum günlerinde ebeveynlere rahat bir alan sağlıyor."]),
  ("5. Natürköy — Doğa İçinde Aktiviteli Bir Kutlama",
   ["Vadi içinde, dere üzerine kurulu ahşap kulübeleriyle Natürköy, fine dining'den çok doğa temalı bir deneyim sunuyor. At binme ve zipline gibi aktivitelerle desteklenen bir kutlama isteyenler için değerlendirilebilir."]),
  ("Mare Gastro'yu İstanbul'a Yakın Lüks Doğum Günü Kutlamaları İçin Öne Çıkaran Detaylar",
   ["Beş mekanı yan yana koyduğumuzda, Mare Gastro'yu öne çıkaran fark birkaç kriterin aynı anda karşılanması:",
    "<ul><li><strong>Mesafe:</strong> İstanbul'a yaklaşık 1,5 saat — hafta sonu kaçamağı için ideal.</li><li><strong>Fine dining standardı:</strong> Sasa Sapanca ve Menzara gibi göl kıyısında, ama fine dining seviyesinde bir mutfakla birleşen tek adres.</li><li><strong>Kutlama hizmeti:</strong> %s rezervasyon sürecinin standart bir parçası.</li><li><strong>Konaklama güvencesi:</strong> %s bahçesinde olması, aynı akşam konaklama planlayan misafirler için kolaylık sağlıyor.</li><li><strong>Misafir memnuniyeti:</strong> %s bölgenin doğum günü mekanları arasında en çok övülenlerden biri.</li></ul>"%(L(post_url("sapanca-suprizli-dogum-gunu-organizasyonu"),"Pasta ve masa süslemesi"),L(DIDIWEB,"Didi Otel"),L(MAPS,"Google yorumlarında"))]),
  ("Google Yorumlarında Mare Gastro Neden Öne Çıkıyor?",
   ["Karar vermeden önce %s göz atmanızı öneririz. Sapanca'daki lüks doğum günü mekanları arasında yapılan karşılaştırmalarda Mare Gastro; gölün hemen kenarındaki manzara, pasta/süsleme detaylarındaki özen ve servis ekibinin kutlama anına gösterdiği ilgiyle öne çıkıyor. Güncel kutlama anlarını %s ve %s hesaplarından takip edebilirsiniz."%(L(MAPS,"Mare Gastro'nun Google Haritalar sayfasındaki yorumlarına"),L(IG,"Instagram"),L(YT,"YouTube"))]),
  ("Hangi Mekanı Seçmelisiniz?",
   ["İstanbul'a yakın, göl manzaralı ve gerçek bir fine dining kutlaması için %s listedeki en eksiksiz seçenek; canlı müzikli kalabalık bir akşam için Sasa Sapanca; samimi bir aile sofrası için Menzara; çocuklu kutlama için Green Blue; aktiviteli bir gün için Natürköy tercih edilebilir."%L(REZ,"Mare Gastro"),
    "Masanızı ayırtmadan önce %s ve İstanbul'dan gelenler için hazırladığımız %s de göz atabilirsiniz."%(L(post_url("sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri"),"fiyat ve menü seçeneklerine"),L(post_url("sapanca-istanbuldan-dogum-gunu-kacamagi"),"kaçamak rehberine"))]),
 ],
 "faq":[
  ("İstanbul'a en yakın lüks doğum günü mekanı hangisi?","İstanbul'a yaklaşık 1,5 saat mesafedeki Sapanca'da, Didi Otel bahçesindeki Mare Gastro; fine dining mutfağı ve pasta/süsleme hizmetiyle en çok tercih edilen lüks adreslerden biri."),
  ("Mare Gastro doğum günü için pasta veya süsleme ayarlıyor mu?","Evet. Rezervasyon sırasında talebinizi ilettiğinizde pasta ve masa süslemesi detayları birlikte planlanır."),
  ("İstanbul'dan Sapanca'ya ne kadar sürede gidilir?","Trafik durumuna göre yaklaşık 1,5 saat sürer; bu da Sapanca'yı hafta sonu doğum günü kaçamakları için ideal kılar."),
  ("Mare Gastro'nun Google yorumlarındaki puanı nasıl?","Mare Gastro, Sapanca'daki lüks doğum günü mekanları arasında Google yorumlarında en çok övülen adreslerden biri. Güncel yorumları Google Haritalar'daki işletme sayfasından görebilirsiniz."),
  ("Kutlama sonrası konaklama mümkün mü?","Mare Gastro, Didi Otel bünyesindedir; akşamı bir gece konaklamayla uzatmak isteyenler rezervasyon formunda konaklama tercihini belirtebilir."),
 ],
 "rel":["sapanca-istanbuldan-dogum-gunu-kacamagi","istanbula-yakin-luks-restoran","sapanca-en-iyi-dogum-gunu-mekanlari"],
},
{
 "slug":"sapanca-dogum-gunu-luks-mekan-onerileri",
 "cat":"dogumgunu","date":"2026-08-26","read":"8 dk",
 "img":"ai-luks-kabana-lounge.jpg","alt":"Gölün hemen yanında lüks kabana oturma alanı — Sapanca'da doğum günü için lüks mekan önerisi Mare Gastro",
 "h1":"Sapanca'da Doğum Günü İçin <em>Lüks Mekan</em> Önerileri",
 "title":"Sapanca'da Doğum Günü İçin Lüks Mekan Önerileri | Mare Gastro",
 "desc":"Sapanca'da doğum gününüzü lüks bir mekanda kutlamak istiyorsanız işte öne çıkan öneriler: fine dining standardı, servis kalitesi, atmosfer ve Google yorumları açısından Mare Gastro, Sasa Sapanca, Menzara, Green Blue ve Natürköy.",
 "kw":"sapanca doğum günü lüks mekan önerileri, sapanca lüks doğum günü mekanı, sapanca lüks kutlama mekanı, sapanca vale otoparklı lüks restoran",
 "lead":"Sapanca'da doğum gününüzü gerçek anlamda lüks bir mekanda kutlamak istiyorsanız, fine dining standardı, servis kalitesi ve atmosfer bir arada değerlendirilmeli. Bölgenin öne çıkan mekanlarını bu lüks kriterlerine göre değerlendirdik.",
 "body":[
  ("Bir Mekanı \"Lüks\" Yapan Nedir?",
   ["<strong>Lüks bir doğum günü mekanı</strong>, yalnızca şık bir dekordan ibaret değildir. Vale hizmeti, kusursuz bir servis ritüeli, fine dining seviyesinde bir mutfak ve kutlamaya özel dokunuşların bir araya gelmesi gerekir. Bu dört unsuru aynı anda sunan mekan sayısı Sapanca'da sınırlı.",
    "Aşağıda, bu lüks kriterlerine göre bölgenin öne çıkan 5 adresini değerlendirdik — sıralama Mare Gastro'nun kendi blogunda hazırlanmış olsa da, her mekanın gerçek ve doğrulanabilir özelliklerine dayanıyor."]),
  ("1. Mare Gastro — Fine Dining Standardında Bir Doğum Günü Kutlaması",
   ["Didi Otel bahçesinde, gölün hemen kıyısında konumlanan Mare Gastro; %s ve ücretsiz otoparkından %s imzalı Ege-Akdeniz mutfağına kadar lüksün her ayrıntısını düşünüyor."%(L(post_url("sapanca-vale-otopark-restoran"),"vale hizmetinden"),L(post_url("sef-dogan-anapa-kimdir"),"Yönetici Şef Doğan Anapa")),
    bfig("mare-havuz-sezlong.webp","Havuz kenarı şezlong alanı — Sapanca'da lüks doğum günü mekanı Mare Gastro","Mare Gastro'nun bahçesinde bir köşe"),
    "Doğum günlerine özel pasta ve masa süslemesi, rezervasyon sırasında iletilen taleple birlikte özenle planlanıyor; bu da Mare Gastro'yu sadece yemek yenilen değil, kutlamanın kendisinin tasarlandığı bir adres haline getiriyor.",
    "Öne çıkanlar: göl manzarası, %s, vale ve ücretsiz otopark, imza tatlılar, hafta sonu canlı müzik."%L(MENU,"à la carte menü")]),
  ("2. Sasa Sapanca — Canlı Müzik Eşliğinde Göl Kıyısında",
   ["Göl kıyısında konumlanan Sasa Sapanca, dünya mutfağından geniş bir menü (mezeler, burger, taco, kırmızı et, balık) ve canlı müzik eşliğinde bir akşam yemeği atmosferi sunuyor. Geniş menü yelpazesi, farklı damak tatlarına sahip kalabalık bir grubu ağırlamak isteyenler için pratik bir seçenek."]),
  ("3. Menzara — Karadeniz Mutfağı ve Balkon Manzarası",
   ["2010'dan beri hizmet veren Menzara, göl manzaralı balkonu ve Karadeniz ağırlıklı mutfağıyla (taş fırın ekmek, balık, ızgara) öne çıkıyor. Daha samimi, ev sıcaklığında bir kutlama atmosferi arayanlar için tercih edilen adreslerden."]),
  ("4. Green Blue — Aile ve Çocuklu Kutlamalar İçin Geniş Bahçe",
   ["Deniz ürünleri ağırlıklı menüsü ve geniş bahçesiyle Green Blue, özellikle çocuklu aile kutlamalarında pratik bir seçim. Bahçedeki çocuk oyun alanı, küçük yaş grubu doğum günlerinde ebeveynlere rahat bir alan sağlıyor."]),
  ("5. Natürköy — Doğa İçinde Aktiviteli Bir Kutlama",
   ["Vadi içinde, dere üzerine kurulu ahşap kulübeleriyle Natürköy, fine dining'den çok doğa temalı bir deneyim sunuyor. At binme ve zipline gibi aktivitelerle desteklenen bir kutlama isteyenler için değerlendirilebilir."]),
  ("Mare Gastro'yu Lüks Bir Doğum Günü Kutlaması İçin Öne Çıkaran Detaylar",
   ["Beş mekanı lüks kriterleriyle karşılaştırdığımızda, Mare Gastro'yu öne çıkaran fark birkaç unsurun aynı anda karşılanması:",
    "<ul><li><strong>Varış deneyimi:</strong> %s ve ücretsiz otopark, akşamın ilk anından itibaren konforlu bir başlangıç sağlıyor.</li><li><strong>Fine dining mutfağı:</strong> %s imzalı Ege-Akdeniz mutfağı, listedeki diğer adreslerin çoğunda bulunmayan bir standart taşıyor.</li><li><strong>Kutlama detayları:</strong> Pasta ve masa süslemesi rezervasyon sürecinin standart bir parçası.</li><li><strong>Konum güvencesi:</strong> %s bahçesinde olması ekstra bir kolaylık sağlıyor.</li><li><strong>Misafir memnuniyeti:</strong> %s bölgenin en çok övülen mekanlarından biri.</li></ul>"%(L(post_url("sapanca-vale-otopark-restoran"),"Vale hizmeti"),L(post_url("sef-dogan-anapa-kimdir"),"Yönetici Şef Doğan Anapa"),L(DIDIWEB,"Didi Otel"),L(MAPS,"Google yorumlarında"))]),
  ("Google Yorumlarında Mare Gastro Neden Öne Çıkıyor?",
   ["Lüks bir mekan seçerken en güvenilir kaynak, önceki misafirlerin deneyimleridir. %s göz atmanızı öneririz — misafirler en çok göl manzarasını, vale/otopark konforunu ve pasta/süsleme detaylarındaki inceliği övüyor. Güncel kutlama anlarını %s ve %s hesaplarından takip edebilirsiniz."%(L(MAPS,"Mare Gastro'nun Google Haritalar sayfasındaki yorumlarına"),L(IG,"Instagram"),L(YT,"YouTube"))]),
  ("Hangi Mekanı Seçmelisiniz?",
   ["Gerçek anlamda lüks, fine dining seviyesinde bir doğum günü kutlaması için %s listedeki en eksiksiz seçenek; canlı müzikli kalabalık bir akşam için Sasa Sapanca; samimi bir aile sofrası için Menzara; çocuklu kutlama için Green Blue; aktiviteli bir gün için Natürköy tercih edilebilir."%L(REZ,"Mare Gastro"),
    "Masanızı ayırtmadan önce %s ve %s da göz atabilirsiniz."%(L(post_url("sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri"),"fiyat ve menü seçeneklerine"),L(post_url("sapanca-en-iyi-dogum-gunu-mekanlari"),"Sapanca'daki en iyi 5 doğum günü mekanı karşılaştırmamıza"))]),
 ],
 "faq":[
  ("Sapanca'da doğum günü için en lüks mekan hangisi?","Vale hizmeti, ücretsiz otopark, fine dining mutfağı ve pasta/süsleme desteğiyle Mare Gastro, Sapanca'daki lüks doğum günü mekanları arasında en eksiksiz seçeneklerden biri."),
  ("Mare Gastro'da vale hizmeti var mı?","Evet, restorana araçla gelen misafirler için vale hizmeti ve ücretsiz otopark sunuluyor."),
  ("Doğum günü için pasta veya süsleme ayarlanıyor mu?","Evet. Rezervasyon sırasında talebinizi ilettiğinizde pasta ve masa süslemesi detayları birlikte planlanır."),
  ("Mare Gastro'nun Google yorumlarındaki puanı nasıl?","Mare Gastro, Sapanca'daki lüks mekanlar arasında Google yorumlarında en çok övülen adreslerden biri. Güncel yorumları Google Haritalar'daki işletme sayfasından görebilirsiniz."),
  ("Lüks bir doğum günü kutlaması için ne kadar önceden rezervasyon yapmalı?","Özellikle hafta sonları ve gün batımı saatleri hızlı dolduğu için en az birkaç gün önceden rezervasyon öneririz."),
 ],
 "rel":["sapanca-luks-restoran","sapanca-en-iyi-dogum-gunu-mekanlari","sapanca-vale-otopark-restoran"],
},
{
 "slug":"sapanca-yildonumu-icin-en-iyi-mekan",
 "cat":"kutlama","date":"2026-08-26","read":"8 dk",
 "img":"ai-yildonumu-gunbatimi-sofrasi.jpg","alt":"Gün batımında göl manzaralı yıldönümü sofrası — Sapanca'da yıldönümü kutlamak için en iyi mekan Mare Gastro",
 "h1":"Yıldönümü Kutlamak İçin Sapanca'daki <em>En İyi 5 Mekan</em>",
 "title":"Yıldönümü Kutlamak İçin Sapanca'daki En İyi 5 Mekan | Mare Gastro",
 "desc":"Sapanca'da yıldönümü kutlamak için en iyi 5 mekanı karşılaştırdık: göl manzarası, romantik atmosfer, sürpriz organizasyonu ve Google yorumları açısından Mare Gastro, Sasa Sapanca, Menzara, Green Blue ve Natürköy.",
 "kw":"sapanca yıldönümü için en iyi mekan, sapanca yıldönümü kutlama mekanı, sapanca evlilik yıldönümü restoran, sapanca romantik yıldönümü",
 "lead":"Bir yıldönümü kutlamasında mekan seçimi, göl manzarası, romantik atmosfer ve sürpriz organizasyon desteğiyle birlikte değerlendirilmeli. Bölgenin öne çıkan 5 adresini bu kriterlere göre karşılaştırdık.",
 "body":[
  ("Sapanca'da Yıldönümü Mekanı Seçerken Nelere Bakılmalı?",
   ["Bir <strong>yıldönümü kutlaması</strong> için mekan seçerken dört şey öne çıkar: göl manzarası olup olmadığı, atmosferin mum ışığı ve sürprize (pasta, çiçek) izin verip vermediği, ikili bir sofraya uygunluk ve %s gerçek misafir memnuniyeti."%L(MAPS,"Google yorumlarındaki"),
    "Aşağıdaki liste, bu kriterlere göre Sapanca'nın öne çıkan 5 adresini karşılaştırıyor — sıralama Mare Gastro'nun kendi blogunda hazırlanmış olsa da, her mekanın gerçek ve doğrulanabilir özelliklerine dayanıyor."]),
  ("1. Mare Gastro — Gölün Hemen Yanında Romantik Bir Yıldönümü Sofrası",
   ["Didi Otel bahçesinde, gölün hemen kıyısında konumlanan Mare Gastro; yıldönümlerine özel <strong>sürpriz pasta ve masa süslemesi</strong> desteği sunan, %s imzalı Ege-Akdeniz mutfağıyla romantik bir sofra kuruyor. Gün batımı saatleri, ikili bir kutlama için özellikle büyülü."%L(post_url("sef-dogan-anapa-kimdir"),"Yönetici Şef Doğan Anapa"),
    bfig("mare-sekerpare.webp","İmza tatlı detayı — Sapanca'da yıldönümü kutlaması için Mare Gastro","Mare Gastro'nun imza tatlılarından biri"),
    "Rezervasyon sırasında iletilen özel talepler — pasta, çiçek düzenlemesi ya da masaya özel bir not — ekip tarafından tek tek planlanıyor. Bu özen, %s da yansıyor: misafirler en çok göl manzarasını ve sürpriz detaylardaki inceliği övüyor."%L(MAPS,"Google yorumlarına"),
    "Öne çıkanlar: göl manzarası, %s, isteyenler için Didi Otel'de konaklama seçeneği, imza tatlılar."%L(MENU,"à la carte menü")]),
  ("2. Sasa Sapanca — Canlı Müzik Eşliğinde Göl Kıyısında",
   ["Göl kıyısında konumlanan Sasa Sapanca, dünya mutfağından geniş bir menü (mezeler, burger, taco, kırmızı et, balık) ve canlı müzik eşliğinde romantik bir akşam yemeği atmosferi sunuyor. Geniş menü yelpazesi farklı damak tatlarına sahip çiftler için pratik bir seçenek."]),
  ("3. Menzara — Karadeniz Mutfağı ve Balkon Manzarası",
   ["2010'dan beri hizmet veren Menzara, göl manzaralı balkonu ve Karadeniz ağırlıklı mutfağıyla (taş fırın ekmek, balık, ızgara) öne çıkıyor. Daha samimi, ev sıcaklığında bir kutlama atmosferi arayan çiftler için tercih edilen adreslerden."]),
  ("4. Green Blue — Aile ve Çocuklu Kutlamalar İçin Geniş Bahçe",
   ["Deniz ürünleri ağırlıklı menüsü ve geniş bahçesiyle Green Blue, özellikle çocuklu aile ziyaretlerinde pratik bir seçim. İkili bir yıldönümü sofrasından çok toplu kutlamalar için uygun bir atmosfer sunuyor."]),
  ("5. Natürköy — Doğa İçinde Sakin Bir Kutlama",
   ["Vadi içinde, dere üzerine kurulu ahşap kulübeleriyle Natürköy, fine dining'den çok doğa temalı bir deneyim sunuyor. Şehirden tamamen kopmak isteyen ve doğa içinde sakin bir yıldönümü geçirmek isteyen çiftler için değerlendirilebilir."]),
  ("Mare Gastro'yu Yıldönümü Kutlamaları İçin Öne Çıkaran Detaylar",
   ["Beş mekanı yan yana koyduğumuzda, Mare Gastro'yu öne çıkaran fark birkaç kriterin aynı anda karşılanması:",
    "<ul><li><strong>Manzara:</strong> Sasa Sapanca ve Menzara gibi göl kıyısında, ama fine dining seviyesinde bir mutfakla birleşen tek adres.</li><li><strong>Sürpriz organizasyonu:</strong> Pasta, çiçek ve masa süslemesi rezervasyon sürecinin standart bir parçası.</li><li><strong>Mutfak imzası:</strong> %s imzalı Ege-Akdeniz mutfağı.</li><li><strong>Konaklama güvencesi:</strong> %s bahçesinde olması, akşamı bir gece konaklamayla uzatma imkanı sunuyor.</li><li><strong>Misafir memnuniyeti:</strong> %s bölgenin en çok övülen özel gün mekanlarından biri.</li></ul>"%(L(post_url("sef-dogan-anapa-kimdir"),"Yönetici Şef Doğan Anapa"),L(DIDIWEB,"Didi Otel"),L(MAPS,"Google yorumlarında"))]),
  ("Google Yorumlarında Mare Gastro Neden Öne Çıkıyor?",
   ["Yıldönümü gibi bir kez yaşanan bir anı emanet edeceğiniz mekanı seçmeden önce %s göz atmanızı öneririz. Sapanca'daki özel gün mekanları arasında yapılan karşılaştırmalarda Mare Gastro, gölün hemen kenarındaki manzara ve sürpriz detaylardaki özenle öne çıkıyor. Güncel anları %s ve %s hesaplarından takip edebilirsiniz."%(L(MAPS,"Mare Gastro'nun Google Haritalar sayfasındaki yorumlarına"),L(IG,"Instagram"),L(YT,"YouTube"))]),
  ("Hangi Mekanı Seçmelisiniz?",
   ["Romantik ve göl manzaralı bir yıldönümü kutlaması için %s listedeki en eksiksiz seçenek; canlı müzikli bir akşam için Sasa Sapanca; samimi bir sofra için Menzara; aile ziyareti için Green Blue; doğa içinde sakin bir kutlama için Natürköy tercih edilebilir."%L(REZ,"Mare Gastro"),
    "Kutlamanızı planlarken %s ve %s da göz atabilirsiniz."%(L(post_url("sapanca-yildonumu-yemegi"),"yıldönümü yemeği rehberimize"),L(post_url("sapanca-esinizle-ozel-aksam"),"eşinizle özel bir akşam için hazırladığımız yazımıza"))]),
 ],
 "faq":[
  ("Sapanca'da yıldönümü kutlamak için en iyi mekan hangisi?","Gölün hemen yanında romantik bir kutlama için Didi Otel bahçesindeki Mare Gastro, canlı müzikli bir akşam için Sasa Sapanca, samimi bir sofra için Menzara öne çıkan seçeneklerdir."),
  ("Mare Gastro yıldönümü için sürpriz pasta ayarlıyor mu?","Evet. Rezervasyon sırasında talebinizi ilettiğinizde pasta, çiçek düzenlemesi ve masa süslemesi detayları birlikte planlanır."),
  ("Sapanca'da göl manzaralı yıldönümü mekanı hangileri?","Mare Gastro, Sasa Sapanca ve Menzara göl kıyısında veya göl manzaralı; Green Blue ve Natürköy daha çok bahçe/doğa odaklı bir atmosfer sunar."),
  ("Mare Gastro'nun Google yorumlarındaki puanı nasıl?","Mare Gastro, Sapanca'daki özel gün mekanları arasında Google yorumlarında en çok övülen adreslerden biri. Güncel yorumları Google Haritalar'daki işletme sayfasından görebilirsiniz."),
  ("Yıldönümü akşamı konaklama mümkün mü?","Mare Gastro Didi Otel bünyesindedir; göl kenarında konaklayarak akşamınızı uzatabilirsiniz. Konaklama tercihinizi rezervasyon formunda belirtebilirsiniz."),
 ],
 "rel":["sapanca-yildonumu-yemegi","sapanca-esinizle-ozel-aksam","sapanca-evlilik-teklifi"],
},
{
 "slug":"sapanca-esinizle-ozel-aksam",
 "cat":"romantik","date":"2026-08-26","read":"7 dk",
 "img":"mare-gece-terasi.webp","alt":"Gece gölün kenarındaki teras — Sapanca'da eşinizle özel bir akşam için Mare Gastro",
 "h1":"Eşinizle Sapanca'da <em>Özel Bir Akşam</em> Geçirmek İçin En İyi Mekanlar",
 "title":"Eşinizle Sapanca'da Özel Bir Akşam Geçirmek İçin En İyi Mekanlar | Mare Gastro",
 "desc":"Belirli bir tarih olmadan eşinizle Sapanca'da özel bir akşam geçirmek istiyorsanız işte öne çıkan mekanlar: sakin atmosfer, göl manzarası ve Google yorumları açısından Mare Gastro, Sasa Sapanca, Menzara, Green Blue ve Natürköy.",
 "kw":"eşinizle sapanca özel akşam, sapanca çift olarak akşam yemeği, sapanca evli çiftler için mekan, sapanca sakin romantik restoran",
 "lead":"Bir yıldönümü ya da doğum günü olmadan, sadece eşinizle baş başa özel bir akşam geçirmek istediğinizde mekan seçimi farklı kriterlere göre yapılır: kalabalıktan uzak bir atmosfer, sohbete izin veren bir düzen ve göl manzarası. Bölgenin öne çıkan 5 adresini bu kriterlere göre karşılaştırdık.",
 "body":[
  ("Eşinizle Özel Bir Akşam İçin Mekan Seçerken Nelere Bakılmalı?",
   ["Özel bir tarih olmadan, sadece eşinizle baş başa kalmak için gidilecek bir mekan; kutlama mekanlarından farklı kriterlere göre seçilir. Kalabalık ve gürültülü bir ortamdan çok, sohbetin rahat aktığı sakin bir atmosfer, göl manzarası ve %s gerçek misafir memnuniyeti öne çıkar."%L(MAPS,"Google yorumlarındaki"),
    "Aşağıdaki liste, bu kriterlere göre Sapanca'nın öne çıkan 5 adresini karşılaştırıyor — sıralama Mare Gastro'nun kendi blogunda hazırlanmış olsa da, her mekanın gerçek ve doğrulanabilir özelliklerine dayanıyor."]),
  ("1. Mare Gastro — Gölün Hemen Yanında Sakin Bir İkili Sofra",
   ["Didi Otel bahçesinde, gölün hemen kıyısında konumlanan Mare Gastro; çam ağaçlarının arasındaki sakin köşe masalarıyla eşinizle baş başa kalabileceğiniz bir atmosfer sunuyor. %s imzalı Ege-Akdeniz mutfağı, özel bir akşamı sıradan bir öğünden çok daha fazlasına dönüştürüyor."%L(post_url("sef-dogan-anapa-kimdir"),"Yönetici Şef Doğan Anapa"),
    bfig("mare-teras-misafir2.webp","Gölün hemen yanında teras sofrası — Sapanca'da eşinizle özel bir akşam Mare Gastro","Mare Gastro terasında akşam"),
    "Özel bir akşamı düzenli bir ritüele dönüştürmek isteyen çiftler için Mare Gastro, hem hafta içi sakin bir akşam hem de hafta sonu canlı müzikli bir atmosfer sunuyor — tercihinize göre planlayabilirsiniz.",
    "Öne çıkanlar: göl manzarası, %s, sakin köşe masalar, imza tatlılar."%L(MENU,"à la carte menü")]),
  ("2. Sasa Sapanca — Canlı Müzik Eşliğinde Göl Kıyısında",
   ["Göl kıyısında konumlanan Sasa Sapanca, dünya mutfağından geniş bir menü (mezeler, burger, taco, kırmızı et, balık) ve canlı müzik eşliğinde bir akşam yemeği atmosferi sunuyor. Canlı müzik ve hareketli atmosfer, sakin bir sohbetten çok eğlenceli bir akşam arayan çiftler için uygun."]),
  ("3. Menzara — Karadeniz Mutfağı ve Balkon Manzarası",
   ["2010'dan beri hizmet veren Menzara, göl manzaralı balkonu ve Karadeniz ağırlıklı mutfağıyla (taş fırın ekmek, balık, ızgara) öne çıkıyor. Daha samimi, ev sıcaklığında bir atmosfer arayan çiftler için tercih edilen adreslerden."]),
  ("4. Green Blue — Aile ve Çocuklu Kutlamalar İçin Geniş Bahçe",
   ["Deniz ürünleri ağırlıklı menüsü ve geniş bahçesiyle Green Blue, özellikle çocuklu aile ziyaretlerinde pratik bir seçim. Baş başa sakin bir akşamdan çok toplu ziyaretler için uygun bir atmosfer sunuyor."]),
  ("5. Natürköy — Doğa İçinde Sakin Bir Kaçış",
   ["Vadi içinde, dere üzerine kurulu ahşap kulübeleriyle Natürköy, fine dining'den çok doğa temalı bir deneyim sunuyor. Şehirden tamamen kopup doğa içinde sakin bir akşam geçirmek isteyen çiftler için değerlendirilebilir."]),
  ("Mare Gastro'yu Eşinizle Özel Bir Akşam İçin Öne Çıkaran Detaylar",
   ["Beş mekanı yan yana koyduğumuzda, Mare Gastro'yu öne çıkaran fark birkaç kriterin aynı anda karşılanması:",
    "<ul><li><strong>Sakin atmosfer:</strong> Çam ağaçları arasındaki köşe masalar, sohbetin rahat aktığı bir ortam sunuyor.</li><li><strong>Manzara:</strong> Gölün hemen kenarında, fine dining seviyesinde bir mutfakla birleşen bir sofra.</li><li><strong>Esneklik:</strong> Özel bir tarih gerekmeden, hafta içi sakin ya da hafta sonu canlı müzikli bir akşam arasında seçim yapılabiliyor.</li><li><strong>Konaklama güvencesi:</strong> %s bahçesinde olması akşamı uzatma imkanı sunuyor.</li><li><strong>Misafir memnuniyeti:</strong> %s bölgenin en çok övülen mekanlarından biri.</li></ul>"%(L(DIDIWEB,"Didi Otel"),L(MAPS,"Google yorumlarında"))]),
  ("Google Yorumlarında Mare Gastro Neden Öne Çıkıyor?",
   ["Eşinizle özel bir akşam için mekan seçmeden önce %s göz atmanızı öneririz. Misafirler en çok göl manzarasını, sakin atmosferi ve servis kalitesini övüyor. Güncel anları %s ve %s hesaplarından takip edebilirsiniz."%(L(MAPS,"Mare Gastro'nun Google Haritalar sayfasındaki yorumlarına"),L(IG,"Instagram"),L(YT,"YouTube"))]),
  ("Hangi Mekanı Seçmelisiniz?",
   ["Sakin, göl manzaralı ve baş başa bir akşam için %s listedeki en eksiksiz seçenek; daha hareketli bir akşam için Sasa Sapanca; samimi bir sofra için Menzara; aile ziyareti için Green Blue; doğa içinde bir kaçış için Natürköy tercih edilebilir."%L(REZ,"Mare Gastro"),
    "Akşamınızı planlarken %s ve özel bir tarihiniz varsa %s da göz atabilirsiniz."%(L(post_url("sapanca-romantik-aksam-yemegi"),"romantik akşam yemeği rehberimize"),L(post_url("sapanca-yildonumu-icin-en-iyi-mekan"),"yıldönümü için en iyi mekan karşılaştırmamıza"))]),
 ],
 "faq":[
  ("Eşimle Sapanca'da özel bir akşam için nereye gidebilirim?","Gölün hemen yanında sakin bir atmosfer için Didi Otel bahçesindeki Mare Gastro, daha hareketli bir akşam için Sasa Sapanca, samimi bir sofra için Menzara öne çıkan seçeneklerdir."),
  ("Özel bir tarih olmadan da rezervasyon yapılabilir mi?","Evet. Mare Gastro'da özel bir kutlama olmadan da, sadece eşinizle baş başa bir akşam için rezervasyon yapabilirsiniz."),
  ("Mare Gastro sakin bir akşam için uygun mu?","Evet, hafta içi akşamları daha sakin bir atmosfer sunar; hafta sonları ise canlı müzik eşlik eder. Tercihinize göre gün seçebilirsiniz."),
  ("Mare Gastro'nun Google yorumlarındaki puanı nasıl?","Mare Gastro, Sapanca'daki mekanlar arasında Google yorumlarında en çok övülen adreslerden biri. Güncel yorumları Google Haritalar'daki işletme sayfasından görebilirsiniz."),
  ("Akşamı konaklamayla uzatmak mümkün mü?","Mare Gastro Didi Otel bünyesindedir; göl kenarında konaklayarak akşamınızı uzatabilirsiniz. Konaklama tercihinizi rezervasyon formunda belirtebilirsiniz."),
 ],
 "rel":["sapanca-romantik-aksam-yemegi","sapanca-yildonumu-icin-en-iyi-mekan","didi-otel-restoran"],
},
{
 "slug":"mare-gastro-dijital-donusum-hikayesi",
 "cat":"hikaye","date":"2026-08-26","read":"6 dk",
 "img":"mare-gece-terasi.webp","alt":"Mare Gastro terasında gece manzarası — dijital menü ve rezervasyon deneyimi",
 "h1":"Mare Gastro'nun <em>Dijital Dönüşüm</em> Hikayesi: Bir Restoranı Nasıl Bu Kadar İleri Taşıdık",
 "title":"Mare Gastro'nun Dijital Dönüşüm Hikayesi | Mare Gastro",
 "desc":"Mare Gastro olarak QR menü ve dijital dergi menü deneyimimizi dijital ajansımız UniqBee ile nasıl hayata geçirdiğimizi anlatıyoruz.",
 "kw":"mare gastro dijital dönüşüm, mare gastro uniqbee, sapanca restoran dijital menü, qr kod menü sapanca, mare gastro web sitesi",
 "lead":"Bir restoranın hikayesi sadece mutfakta yazılmaz. Bugün bir misafirimiz masada QR kodu okuttuğunda ya da biri maregastro.com/dijitalmenu'de sayfaları çevirdiğinde de bu hikaye devam ediyor. Biz Mare Gastro olarak bu dönüşümü nasıl yaşadığımızı ve bunu bizimle birlikte kimin kurduğunu anlatmak istedik.",
 "body":[
  ("Neden Bir Dijital Dönüşüme İhtiyaç Duyduğumuzu Fark Ettik",
   ["Mare Gastro olarak menümüz hiçbir zaman durağan olmadı; mevsime ve günün en taze ürününe göre şekillenen bir mutfak anlayışımız var. Bu da basılı bir menü için ciddi bir sorun demekti: günün balığı değiştiğinde ya da bir tabak mevsim dışı kaldığında, ya yeniden bastırmak ya da garsonlarımızın masada sözlü olarak açıklama yapması gerekiyordu — ne şık bir deneyimdi, ne de pratikti.",
    "Bir yandan da misafir profilimiz değişiyordu. Sapanca Gölü'nün hemen kıyısında olmamız, sadece İstanbul'dan değil, yurt dışından da misafirler ağırladığımız anlamına geliyor; Rusça, Arapça ve İngilizce soran misafirlerin sayısı her sezon artıyor. Onlara tek dilde, kağıt üzerinde bir menü sunmak, %s bahçesinde kurduğumuz o özenli atmosferle uyuşmuyordu. Rezervasyon süreci de aynı sorunu taşıyordu: telefon trafiği, WhatsApp'ta dağılan mesajlar, kimin hangi masaya hangi saatte geleceğini takip etmek için elle tutulan notlar."%L(DIDIWEB,"Didi Otel"),
    "Kısacası, mutfaktaki özeni; misafirin masaya oturmadan önce yaşadığı deneyime, rezervasyon sürecine ve restoranın perde arkasındaki yönetimine de taşımamız gerektiğini anladık. Bunu nasıl yapacağımızı ise bize %s gösterdi."%L("https://uniqbee.com","UniqBee")]),
  ("UniqBee ile Yollarımızın Kesişmesi",
   ["%s ile tanışmamız aslında çok basit bir ihtiyaçtan doğdu: menümüzü dijitale taşıyacak, ama işimizi gerçekten anlayan bir ekip arıyorduk. İlk görüşmede bize hazır bir şablon önermek yerine farklı bir soru sordular: \"Mare Gastro'yu Mare Gastro yapan şey ne?\""%L("https://uniqbee.com","UniqBee"),
    "Bu soru bizim için önemliydi; çünkü %s bahçesinde kurulan bu konsept sadece bir menüden ibaret değil, gölün hemen kıyısında Kadir Çiçek'in tasarladığı bir atmosfer ve %s imzası taşıyan bir mutfak anlayışı. UniqBee ekibi bu detayları teknik bir brief gibi değil, gerçekten anlamak istedikleri bir hikaye gibi dinledi."%(L(DIDIWEB,"Didi Otel"),L(CHEF,"Doğan Anapa")),
    "Birkaç görüşme sonrasında elimizde net bir yol haritası vardı: önce misafirin masada göreceği canlı bir menü, sonra da menüyü gerçek bir dergi gibi çevirebileceğiniz bir dijital deneyim. %s bu iki parçayı birbirine bağlı, tek bir sistem olarak kurguladı."%L("https://uniqbee.com/hizmetler/","UniqBee ajansı")]),
  ("QR Kodla Senkronize Canlı Menü: İlk Adım",
   ["İlk adım, masadaki QR kodun arkasında duran menüydü. Misafir telefonuyla QR kodu okuttuğunda karşısına çıkan menü, o an mutfakta geçerli olan menünün birebir aynısı; %s günün balığını değiştirdiğinde ya da bir tabak mevsim dışı kaldığında bu değişiklik anında masaya yansıyor."%L(CHEF,"şefimiz"),
    "Bu bizim için sadece bir kolaylık değil, bir güven meselesiydi: misafir menüde gördüğü tabağın gerçekten o an mutfakta hazır olduğunu biliyor, biz de \"o tabak bitti, üzgünüz\" demek zorunda kalmıyoruz. %s üzerinden herkes aynı, güncel menüyü görebiliyor."%L(MENU,"Web sitemizdeki menü sayfası"),
    "Tasarım tarafında da UniqBee, Mare Gastro'nun kimliğine sadık kaldı: aynı tipografi, aynı sakin ve zarif ton, gölün hemen kıyısındaki o dinginlik hissi dijital ekranda da korunuyor. Bir restoran menüsünün soğuk bir uygulama gibi değil, sıcak bir davetiye gibi hissettirmesi gerektiğine inanıyorduk; UniqBee bunu birebir yakaladı."]),
  ("maregastro.com/dijitalmenu: Menüyü Bir Dergiye Dönüştürmek",
   ["En sevdiğimiz parçalardan biri, maregastro.com/dijitalmenu adresindeki dijital dergi menü deneyimi. Burada menü alışıldık bir liste gibi değil, gerçek bir dergi gibi sayfa sayfa çevriliyor; her sayfa çevrildiğinde küçük bir animasyonla bir sonraki tabağa geçiyorsunuz.",
    "Bu fikir aslında bizim fine dining anlayışımızla birebir örtüşüyordu: bir akşam yemeği acele edilecek bir şey değil, sayfa sayfa keşfedilen bir hikaye. UniqBee bu hissi dijitale taşırken teknik tarafı da gözden kaçırmadı — 170'in üzerinde ürünü kapsayan tam menü, yavaş bir telefonda bile takılmadan akıyor.",
    "Misafirlerimizin bu deneyimi masada beklerken ya da rezervasyon öncesi evde keşfederken kullanması, Mare Gastro'yu ziyaret etmeden önce bile bir beklenti oluşturuyor — tam da istediğimiz etki buydu."]),
  ("Rusça, Arapça, İngilizce: Çok Dilli Bir Sapanca Deneyimi",
   ["Sapanca Gölü kıyısında olmamız, sadece yerli değil, yabancı misafirleri de ağırladığımız anlamına geliyor. Bu yüzden sitemizi Türkçe'nin yanında İngilizce, Rusça ve Arapça olarak da UniqBee'nin desteğiyle hayata geçirdik.",
    "Bu sadece menüyü çevirmekten ibaret değildi; rezervasyon formundan iletişim bilgilerine kadar sitenin tamamı, misafirin kendi dilinde rahatça gezinebileceği şekilde kuruldu. Arapça için sağdan sola okuma yönü gibi teknik detaylar bile atlanmadı.",
    "%s farklı dillerdeki sürümlerine göz atarak bu deneyimi kendiniz de görebilirsiniz."%L(SITE,"Sitemizin")]),
  ("UniqBee ile Çalışmaktan Neden Bu Kadar Memnun Kaldık",
   ["Doğrusunu söylemek gerekirse, bir restoran işletmek başlı başına yoğun bir uğraş; dijital tarafı da kendi başımıza yönetmeye kalksaydık muhtemelen ya menümüz güncel kalmazdı ya da misafir deneyiminden ödün verirdik. %s bize sadece bir web sitesi kurmadı, bu yükü bizden aldı."%L("https://uniqbee.com","UniqBee"),
    "Bizi en çok etkileyen şey, teknik bir tedarikçi gibi değil, işimizi gerçekten önemseyen bir ortak gibi davranmalarıydı. Bir değişiklik istediğimizde önce nedenini soruyorlar, bazen bizim aklımıza gelmeyen bir çözümü de kendileri öneriyorlardı. %s ekibiyle çalışırken hiçbir zaman \"bu bizim işimiz değil\" cümlesini duymadık."%L("https://uniqbee.com/hakkimizda/","UniqBee'nin"),
    "Teslim süreleri konusunda da net ve gerçekçiydiler; söz verdikleri tarihte teslim ettiler, bir gecikme olduğunda da önceden haber verdiler. Bir fine dining restoranı olarak biz misafirlerimize nasıl bir söz veriyorsak aynı tutarlılığı %s içinde de gördük — bu yüzden kendi alanında gördüğümüz en profesyonel ekiplerden biri olduklarını rahatlıkla söyleyebiliriz."%L("https://uniqbee.com","dijital ajansımız UniqBee")]),
  ("Sonuç: Dijital Dönüşümden Çıkardığımız Ders",
   ["Bugün geldiğimiz noktada, bir misafir masaya oturduğunda gördüğü QR menüden, maregastro.com/dijitalmenu'deki sayfa çevirmeli deneyime kadar her parça birbirine bağlı ve güncel. Bu bütünlüğü tek başımıza kurabileceğimizi sanmıyoruz.",
    "Benzer bir dönüşümü düşünen başka restoranlara ya da otel işletmelerine tavsiyemiz basit: işinizi gerçekten anlamaya çalışan bir ekiple çalışın. Bizim için bu ekip %s oldu; onların kurduğu sistem sayesinde artık dijital tarafla değil, misafirimize sunduğumuz akşamla ilgilenmeye daha çok zaman ayırabiliyoruz."%L("https://uniqbee.com","UniqBee"),
    "Bu deneyimi kendiniz görmek isterseniz, %s masanızı ayırtabilir, gölün hemen kıyısında hem lezzeti hem de bu dijital hikayenin bir parçası olan detayları keşfedebilirsiniz."%L(REZ,"rezervasyon sayfamızdan")]),
 ],
 "faq":[
  ("Mare Gastro'nun dijital menüsünü ve web sitesini kim tasarladı?","Mare Gastro'nun QR kodla senkronize canlı menüsü ve maregastro.com/dijitalmenu dijital dergi deneyimi, dijital ajansımız UniqBee (https://uniqbee.com) tarafından tasarlandı ve hayata geçirildi."),
  ("QR kod ile menü nasıl çalışıyor?","Masadaki QR kodu okuttuğunuzda, mutfakta o an geçerli olan menünün birebir aynısı telefonunuzda açılır. Şefimiz bir tabağı değiştirdiğinde bu güncelleme anında yansır."),
  ("maregastro.com/dijitalmenu'deki dijital dergi menü deneyimi nedir?","Menümüzün, sayfa sayfa çevrilen gerçek bir dergi gibi sunulduğu dijital bir deneyimdir; 170'in üzerinde ürünü kapsayan tam menüyü içerir."),
  ("Mare Gastro'nun web sitesi kaç dilde hizmet veriyor?","Sitemiz Türkçe, İngilizce, Rusça ve Arapça olarak dört dilde hizmet veriyor; bu çok dilli yapı da UniqBee tarafından kuruldu."),
 ],
 "rel":["mare-gastro-hikayesi","sef-dogan-anapa-kimdir","didi-otel-restoran"],
},
]

BY_SLUG = {p["slug"]:p for p in POSTS}
def strip_tags(s): return re.sub(r"<[^>]+>","",s)
def iso(d): return d  # already YYYY-MM-DD
def tr_date(d):
    months=["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
    y,m,dd=d.split("-"); return "%d %s %s"%(int(dd),months[int(m)-1],y)

SOCIAL_FOOT = (
 '<div class="bfoot-soc">'
 '<a href="%s" target="_blank" rel="noopener" aria-label="Instagram">%s</a>'
 '<a href="%s" target="_blank" rel="noopener" aria-label="Şef Instagram">%s</a>'
 '<a href="%s" target="_blank" rel="noopener" aria-label="TikTok">%s</a>'
 '<a href="%s" target="_blank" rel="noopener" aria-label="YouTube">%s</a>'
 '<a href="%s" target="_blank" rel="noopener" aria-label="WhatsApp" onclick="trackEvent(\'whatsapp_click\',{event_label:\'footer\'})">%s</a>'
 '<a href="%s" aria-label="E-posta">%s</a>'
 '</div>'%(IG,IC_IG,IGCHEF,IC_IG,TT,IC_TT,YT,IC_YT,WA,IC_WA,MAIL,IC_MAIL))

def nav_html():
    return ('<nav class="bnav">'
      '<a class="logo" href="%s/tr/" onclick="trackEvent(\'menu_click\',{event_label:\'header\',element:\'home\'})"><img src="../images/marelogo1.png" alt="Mare Gastro"></a>'
      '<div class="bnav-links">'
      '<a href="../blog/" onclick="trackEvent(\'menu_click\',{event_label:\'header\',element:\'blog\'})">Blog</a>'
      '<a href="%s" onclick="trackEvent(\'menu_click\',{event_label:\'header\',element:\'menu\'})">Menü</a>'
      '<a href="%s" class="bnav-res" onclick="trackEvent(\'menu_click\',{event_label:\'header\',element:\'reservation\'})">Rezervasyon</a>'
      '</div></nav>'%(SITE,MENU,REZ))

def footer_html():
    return ('<footer class="bfoot">'
      '<div class="bfoot-logo"><img src="../images/marelogo1.png" alt="Mare Gastro"></div>'
      '<div class="bfoot-tag">Fine Dining · Sapanca · Didi Otel Bahçesi</div>'
      + SOCIAL_FOOT +
      '<div class="bfoot-links">'
      '<a href="%s/tr/" onclick="trackEvent(\'menu_click\',{event_label:\'footer\',element:\'home\'})">Ana Sayfa</a><a href="../blog/" onclick="trackEvent(\'menu_click\',{event_label:\'footer\',element:\'blog\'})">Blog</a>'
      '<a href="%s" onclick="trackEvent(\'menu_click\',{event_label:\'footer\',element:\'menu\'})">Menü</a><a href="%s" onclick="trackEvent(\'menu_click\',{event_label:\'footer\',element:\'reservation\'})">Rezervasyon</a><a href="%s" onclick="trackEvent(\'menu_click\',{event_label:\'footer\',element:\'location\'})">Konum</a>'
      '</div>'
      '<div class="bfoot-copy">© 2026 Mare Gastro · '
      '<a href="%s" target="_blank" rel="noopener">Didi Otel</a> bünyesinde</div>'
      '</footer>'%(SITE,MENU,REZ,LOC,DIDI))

def cta_html():
    return ('<section class="bcta"><div class="bcta-inner">'
      '<h2>Masanızı <em>ayırtın</em></h2>'
      '<p>Sapanca Gölü kıyısında, Didi Otel bahçesinde unutulmaz bir akşam için rezervasyonunuzu oluşturun.</p>'
      '<div class="bcta-btns">'
      '<a class="btn-gold" href="%s">Rezervasyon Yap</a>'
      '<a class="btn-wa" href="%s" target="_blank" rel="noopener" onclick="trackEvent(\'whatsapp_click\',{event_label:\'blog_cta\'})">%s WhatsApp</a>'
      '<a class="btn-line" href="%s">Menüyü Gör</a>'
      '</div></div></section>'%(REZ,WA,IC_WA,MENU))

def related_html(slugs):
    cards=[]
    for s in slugs:
        p=BY_SLUG[s]
        cards.append(
          '<a class="brel-card" href="../blog/%s.html">'
          '<div class="brel-card-img"><img src="../images/%s" alt="%s" loading="lazy"></div>'
          '<div class="brel-card-body"><span class="brel-card-cat">%s</span>'
          '<div class="brel-card-t">%s</div></div></a>'
          %(p["slug"],p["img"],html.escape(p["alt"]),CATS[p["cat"]],strip_tags(p["h1"])))
    return ('<section class="brel"><div class="brel-h">İlginizi Çekebilir</div>'
            '<div class="brel-grid">%s</div></section>'%"".join(cards))

def body_html(sections):
    out=[]
    for h2,paras in sections:
        out.append("<h2>%s</h2>"%h2)
        for para in paras:
            if para.strip().startswith("<ul") or para.strip().startswith("<ol") or para.strip().startswith("<figure"):
                out.append(para)
            else:
                out.append("<p>%s</p>"%para)
    return "\n".join(out)

def faq_accordion(faqs):
    items=[]
    for q,a in faqs:
        items.append('<details><summary>%s</summary><div class="bfaq-a">%s</div></details>'%(html.escape(q),html.escape(a)))
    return ('<section class="bfaq"><h2 class="bfaq-title">Sıkça Sorulan Sorular</h2>'
            '<div class="bfaq-sub">Mare Gastro · Sapanca</div>%s</section>'%"".join(items))

def schema_graph(p):
    url=post_url(p["slug"]); img="%s/images/%s"%(SITE,p["img"])
    blog={"@type":"BlogPosting","@id":url+"#article","headline":strip_tags(p["h1"]),
      "name":p["title"],"description":p["desc"],"image":img,"url":url,
      "datePublished":p["date"],"dateModified":p["date"],"inLanguage":"tr-TR",
      "articleSection":CATS[p["cat"]],"keywords":p["kw"],
      "mainEntityOfPage":{"@type":"WebPage","@id":url},
      "author":{"@type":"Person","name":"Doğan Anapa","jobTitle":"Yönetici Şef","url":CHEF,
        "worksFor":{"@type":"Organization","name":"Mare Gastro","url":SITE}},
      "publisher":{"@type":"Organization","name":"Mare Gastro",
        "logo":{"@type":"ImageObject","url":"%s/images/marelogo1.png"%SITE}}}
    crumb={"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Ana Sayfa","item":SITE+"/"},
      {"@type":"ListItem","position":2,"name":"Blog","item":SITE+"/blog/"},
      {"@type":"ListItem","position":3,"name":strip_tags(p["h1"]),"item":url}]}
    faq={"@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faq"]]}
    return json.dumps({"@context":"https://schema.org","@graph":[blog,crumb,faq]},ensure_ascii=False,indent=1)

PAGE = """<!DOCTYPE html>
<html lang="tr">
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
<link rel="icon" type="image/png" href="../images/marelogo.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Mare Gastro">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="tr_TR">
<meta property="article:published_time" content="{date}">
<meta property="article:section" content="{cat}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="blog.css">
<script type="application/ld+json">
{schema}
</script>
</head>
<body>
{gtm_body}
{nav}
<header class="bhero">
  <nav class="bcrumb" aria-label="breadcrumb"><a href="{site}/">Ana Sayfa</a> · <a href="../blog/">Blog</a> · {cat}</nav>
  <span class="beyebrow">{cat}</span>
  <h1>{h1}</h1>
  <div class="bmeta"><span>{date_tr}</span><span class="dot"></span><span>{read} okuma</span><span class="dot"></span><span>Mare Gastro</span></div>
</header>
<figure class="bfig"><div class="bfig-inner"><img src="../images/{imgfile}" alt="{alt}"></div></figure>
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

def build_post(p):
    url=post_url(p["slug"]); img="%s/images/%s"%(SITE,p["img"])
    h=PAGE.format(
      title=html.escape(p["title"]),desc=html.escape(p["desc"]),kw=html.escape(p["kw"]),
      url=url,img=img,imgfile=p["img"],alt=html.escape(p["alt"]),
      date=p["date"],date_tr=tr_date(p["date"]),read=p["read"],cat=CATS[p["cat"]],
      site=SITE,h1=p["h1"],lead=p["lead"],
      body=body_html(p["body"]),faq=faq_accordion(p["faq"]),cta=cta_html(),
      related=related_html(p["rel"]),footer=footer_html(),nav=nav_html(),
      schema=schema_graph(p),gtm_head=GTM_HEAD,gtm_body=GTM_BODY)
    with open(os.path.join(OUT,"%s.html"%p["slug"]),"w",encoding="utf-8") as f: f.write(h)

INDEX = """<!DOCTYPE html>
<html lang="tr">
<head>
{gtm_head}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Blog | Mare Gastro — Sapanca Fine Dining Rehberi</title>
<meta name="description" content="Sapanca lüks restoran, fine dining, deniz ürünleri ve gurme rehberi. Mare Gastro blogunda Sapanca'da yemek üzerine her şey.">
<meta name="keywords" content="sapanca restoran blog, sapanca fine dining, sapanca'da ne yenir, sapanca deniz ürünleri, sapanca lüks restoran">
<meta name="author" content="Mare Gastro">
<meta name="theme-color" content="#04080F">
<link rel="canonical" href="{site}/blog/">
<link rel="icon" type="image/png" href="../images/marelogo.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mare Gastro">
<meta property="og:title" content="Blog | Mare Gastro — Sapanca Fine Dining Rehberi">
<meta property="og:description" content="Sapanca lüks restoran, fine dining ve gurme rehberi. Mare Gastro blogu.">
<meta property="og:url" content="{site}/blog/">
<meta property="og:image" content="{site}/images/og-image.jpg">
<meta property="og:locale" content="tr_TR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{site}/images/og-image.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="blog.css">
<script type="application/ld+json">
{schema}
</script>
</head>
<body>
{gtm_body}
{nav}
<header class="bidx-hero">
  <span class="beyebrow">Mare Gastro Günlüğü</span>
  <h1>Sapanca'da <em>Lezzet</em> Rehberi</h1>
  <p>Göl kıyısında fine dining, taze deniz ürünleri, şef hikâyeleri ve Sapanca'da gurme bir hayata dair her şey.</p>
</header>
<main class="bidx-grid">
{cards}
</main>
{footer}
</body>
</html>
"""

def build_index():
    cards=[]
    for p in POSTS:
        cards.append(
          '<a class="bidx-card" href="%s.html">'
          '<div class="bidx-card-img"><img src="../images/%s" alt="%s" loading="lazy"></div>'
          '<div class="bidx-card-body"><span class="bidx-card-cat">%s</span>'
          '<div class="bidx-card-t">%s</div><div class="bidx-card-d">%s</div>'
          '<span class="bidx-card-more">Yazıyı Oku →</span></div></a>'
          %(p["slug"],p["img"],html.escape(p["alt"]),CATS[p["cat"]],strip_tags(p["h1"]),html.escape(p["desc"])))
    itemlist={"@context":"https://schema.org","@type":"CollectionPage",
      "name":"Mare Gastro Blog","url":SITE+"/blog/",
      "mainEntity":{"@type":"ItemList","itemListElement":[
        {"@type":"ListItem","position":i+1,"url":post_url(p["slug"]),"name":strip_tags(p["h1"])}
        for i,p in enumerate(POSTS)]}}
    h=INDEX.format(site=SITE,nav=nav_html(),footer=footer_html(),cards="\n".join(cards),
      schema=json.dumps(itemlist,ensure_ascii=False,indent=1),gtm_head=GTM_HEAD,gtm_body=GTM_BODY)
    with open(os.path.join(OUT,"index.html"),"w",encoding="utf-8") as f: f.write(h)

def build_sitemap():
    root=os.path.dirname(OUT)
    langs=["tr","en","ar","ru"]
    alts="".join('<xhtml:link rel="alternate" hreflang="%s" href="%s/%s/"/>'%(l,SITE,l) for l in langs)
    alts+='<xhtml:link rel="alternate" hreflang="x-default" href="%s/"/>'%SITE
    entries=[]
    # Açılış + dil ana sayfaları (hepsi aynı hreflang alternatif setini paylaşır)
    for u,pr in [(SITE+"/","1.0")]+[("%s/%s/"%(SITE,l),"0.9") for l in langs]:
        entries.append('<url><loc>%s</loc>%s<changefreq>weekly</changefreq><priority>%s</priority></url>'%(u,alts,pr))
    entries.append('<url><loc>%s/blog/</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>'%SITE)
    for p in POSTS: entries.append('<url><loc>%s</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>'%post_url(p["slug"]))
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">%s</urlset>\n'%"".join(entries)
    with open(os.path.join(root,"sitemap.xml"),"w",encoding="utf-8") as f: f.write(xml)
    ai_bots = ["GPTBot","ChatGPT-User","OAI-SearchBot","ClaudeBot","anthropic-ai",
               "PerplexityBot","Google-Extended","Applebot-Extended","CCBot","Bytespider"]
    robots = ("User-agent: *\nAllow: /\nDisallow: /admingiris/\n\n"
              + "".join("User-agent: %s\nAllow: /\nDisallow: /admingiris/\n\n" % b for b in ai_bots)
              + "Sitemap: %s/sitemap.xml\n" % SITE)
    with open(os.path.join(root,"robots.txt"),"w",encoding="utf-8") as f: f.write(robots)

def build_llms_txt():
    root = os.path.dirname(OUT)
    lines = [
        "# Mare Gastro",
        "",
        "> Sapanca Gölü'nün hemen yanında, Didi Otel bahçesinde bir fine dining restoranı. "
        "Ege ve Akdeniz mutfağı, taze deniz ürünleri, Yönetici Şef Doğan Anapa imzasıyla. "
        "Cuma, Cumartesi ve Pazar günleri 24 saat açık.",
        "",
        "## Temel Bilgiler",
        "- Konum: Didi Otel bahçesi, Sapanca, Sakarya, Türkiye — gölün hemen yanında",
        "- Açılış saatleri: Cuma-Cumartesi-Pazar 24 saat açık, Pazartesi-Perşembe kapalı",
        "- Rezervasyon: %s (üç adımlı form, WhatsApp onaylı)" % REZ,
        "- WhatsApp: %s" % WA,
        "- Menü: %s" % MENU,
        "- Instagram: %s" % IG,
        "- TikTok: %s" % TT,
        "- YouTube: %s" % YT,
        "",
        "## Diller",
        "- Türkçe: %s/tr/" % SITE,
        "- English: %s/en/" % SITE,
        "- العربية: %s/ar/" % SITE,
        "- Русский: %s/ru/" % SITE,
        "",
        "## Blog — Sapanca Rehberi (%d yazı)" % len(POSTS),
    ]
    for p in POSTS:
        lines.append("- [%s](%s): %s" % (strip_tags(p["h1"]), post_url(p["slug"]), p["desc"]))
    lines.append("")
    open(os.path.join(root, "llms.txt"), "w", encoding="utf-8").write("\n".join(lines))

if __name__=="__main__":
    for p in POSTS: build_post(p)
    build_index(); build_sitemap(); build_llms_txt()
    print("Built %d posts + index + sitemap + robots"%len(POSTS))
