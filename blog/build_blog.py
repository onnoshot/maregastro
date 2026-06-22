# -*- coding: utf-8 -*-
"""Mare Gastro blog generator — builds SEO-optimized luxury posts + index + sitemap."""
import json, os, re, html

SITE   = "https://maregastro.com"
IG     = "https://www.instagram.com/maregastrosapanca/"
IGCHEF = "https://www.instagram.com/chefdogananapa/"
DIDI   = "https://www.instagram.com/didiotel/"
WA     = "https://wa.me/905323540888"
MAIL   = "mailto:info@maregastro.com"
OUT    = os.path.dirname(os.path.abspath(__file__))

# internal homepage anchors
MENU="%s/tr/#menu"%SITE; REZ="%s/tr/#reservation"%SITE; STORY="%s/tr/#story"%SITE; CHEF="%s/tr/#chef"%SITE; LOC="%s/tr/#contact"%SITE

def L(url,txt): return '<a href="%s">%s</a>'%(url,txt)
def post_url(slug): return "%s/blog/%s.html"%(SITE,slug)

# ── SVG social icons ──
IC_IG  ='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>'
IC_WA  ='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.46-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.21-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.62.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.27-.2-.57-.35M12.05 21.78h-.01a9.87 9.87 0 01-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 01-1.51-5.26C2.16 6.89 6.6 2.46 12.05 2.46c2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 012.89 6.99c0 5.45-4.43 9.43-9.88 9.43M20.46 3.49A11.82 11.82 0 0012.05.06C5.5.06.16 5.4.16 11.95c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 005.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.16-3.48-8.42"/></svg>'
IC_MAIL='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'

CATS = {
 "luks":"Lüks Restoran","deniz":"Deniz Ürünleri","finedining":"Fine Dining",
 "sef":"Şefimiz","romantik":"Özel Anlar","rehber":"Sapanca Rehberi",
 "didi":"Didi Otel","kacamak":"Hafta Sonu",
}

POSTS = [
{
 "slug":"sapanca-luks-restoran",
 "cat":"luks","date":"2026-05-12","read":"6 dk",
 "img":"patates-terin2.jpg","alt":"Mare Gastro fine dining tabağı — Sapanca lüks restoran",
 "h1":"Sapanca'da Lüks Restoran: <em>Mare Gastro</em> ile Fine Dining",
 "title":"Sapanca'da Lüks Restoran | Mare Gastro Fine Dining",
 "desc":"Sapanca'da lüks restoran mı arıyorsunuz? Didi Otel bahçesinde, göl manzarasına karşı fine dining deneyimi sunan Mare Gastro'yu keşfedin. Menü ve rezervasyon.",
 "kw":"sapanca lüks restoran, sapanca fine dining, sapanca göl manzaralı restoran, sapanca gurme restoran",
 "lead":"Sapanca Gölü'nün durgun sularına bakan, çamların gölgesine sığınmış, Didi Otel'in büyülü bahçesinde bir lüks restoran: Mare Gastro, doğanın sessizliğini fine dining inceliğiyle buluşturuyor.",
 "body":[
  ("Sapanca'da Lüks Restoran Deneyimi Nasıl Olmalı?",
   ["Bir lüks restoran, yalnızca güzel bir tabaktan ibaret değildir. Işığın masaya düşüşü, garsonun adımındaki sessizlik, şarabın bardağa dökülüş anı ve tabaktaki her dokunuşun bir hikâye anlatması gerekir. <strong>Sapanca'da lüks restoran</strong> arayanlar; manzara, hizmet ve gastronomiyi aynı anda en yüksek seviyede sunan bir mekân ararlar.",
    "Mare Gastro tam da bu beklentiyle doğdu. %s, doğayla iç içe bir konumda, sakin ve zarif bir atmosferde misafirlerini ağırlıyor; her detay, unutulmaz bir akşam için titizlikle tasarlanıyor."%L(LOC,"Sapanca'nın kalbinde")]),
  ("Göl Manzarası ve Doğanın İçinde Bir Sofra",
   ["Sapanca'nın en büyülü anı, gün batımında gölün üzerine düşen altın ışıktır. Mare Gastro, Didi Otel'in yemyeşil bahçesinde konumlanarak bu anı doğrudan sofranıza taşır. Çam ağaçları, palmiyeler ve gölün serinliği eşliğinde yenen bir akşam yemeği, sıradan bir öğünden çok daha fazlasıdır.",
    "Bu yüzden Mare Gastro yalnızca bir <strong>Sapanca göl manzaralı restoran</strong> değil; doğanın ritmiyle uyumlu, dingin bir kaçış noktasıdır."]),
  ("Ege ve Akdeniz'in En Saf Lezzetleri",
   ["Lüks, sadelikte gizlidir. Mare Gastro mutfağı, Ege ve Akdeniz'in en taze malzemelerini sade ama kusursuz tabaklara dönüştürür. Deniz ürünlerinden zeytinyağlılara, ızgaralardan imza tatlılara kadar her tabak, mevsimin ve coğrafyanın hikâyesini anlatır.",
    "Menünün tamamını %s inceleyebilir, gününüze göre değişen taze seçenekleri keşfedebilirsiniz."%L(MENU,"menümüzden")]),
  ("Kadir Çiçek İmzasıyla Tasarlanan Bir Konsept",
   ["Mare Gastro'nun ışığından masasına kadar her detayı, Didi Otel bünyesinde Kadir Çiçek tarafından tasarlandı, planlandı ve büyük bir titizlikle hayata geçirildi. Mutfağın başında ise sinema geçmişini lezzete dönüştüren Yönetici Şef Doğan Anapa var. %s daha yakından tanıyabilirsiniz."%L(STORY,"Hikâyemizi")]),
 ],
 "faq":[
  ("Sapanca'da lüks restoran nerede?","Mare Gastro, Sapanca Gölü kıyısındaki Didi Otel bahçesinde yer alır. Göl manzarasına karşı fine dining deneyimi sunan, doğayla iç içe lüks bir restorandır."),
  ("Mare Gastro hangi günler açık?","Mare Gastro Cuma, Cumartesi ve Pazar günleri 24 saat açıktır. Pazartesi–Perşembe kapalıdır."),
  ("Mare Gastro'da rezervasyon nasıl yapılır?","Web sitesindeki üç adımlı rezervasyon formundan tarih, saat ve kişi sayısını seçerek WhatsApp üzerinden hızlıca rezervasyon oluşturabilirsiniz."),
  ("Mare Gastro İstanbul'a uzak mı?","Sapanca, İstanbul'a yaklaşık 1,5 saat mesafededir; bu da Mare Gastro'yu hafta sonu gurme kaçamakları için ideal kılar."),
 ],
 "rel":["sapanca-deniz-urunleri","sapanca-fine-dining-nedir","didi-otel-restoran"],
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
   ["Sapanca Gölü manzarasına karşı, Didi Otel'in bahçesinde yenen bir deniz ürünleri sofrası; doğa, lezzet ve huzurun nadir buluşmasıdır. %s konumumuza göz atabilirsiniz."%L(LOC,"Bizi bulmak için")]),
 ],
 "faq":[
  ("Sapanca'da en iyi deniz ürünleri nerede yenir?","Mare Gastro, Sapanca Gölü kıyısındaki Didi Otel bahçesinde taze deniz ürünleri ve fine dining sunar. Ahtapot ızgara, jumbo karides ve günün balığı öne çıkan lezzetlerdir."),
  ("Mare Gastro'da günlük taze balık var mı?","Evet. Menü mevsime ve günün en taze ürününe göre değişir; \"günün ızgara balığı\" her ziyarette farklılık gösterebilir."),
  ("Deniz ürünleri menüsünü nereden görebilirim?","Web sitemizdeki menü bölümünden başlangıçlar, ara sıcaklar ve ana yemekler dahil tüm deniz ürünlerini inceleyebilirsiniz."),
  ("Rezervasyon gerekli mi?","Özellikle hafta sonları için rezervasyon öneririz. Üç adımlı form ile WhatsApp üzerinden kolayca rezervasyon yapabilirsiniz."),
 ],
 "rel":["sapanca-luks-restoran","sapancada-ne-yenir","sapanca-romantik-aksam-yemegi"],
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
    "<strong>Sapanca fine dining</strong> deneyimi, bu inceliğe bir de göl manzarası ve doğanın huzurunu ekler."]),
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
 "rel":["sapanca-luks-restoran","sef-dogan-anapa","sapanca-romantik-aksam-yemegi"],
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
 "rel":["sapanca-fine-dining-nedir","sapanca-luks-restoran","sapanca-deniz-urunleri"],
},
{
 "slug":"sapanca-romantik-aksam-yemegi",
 "cat":"romantik","date":"2026-05-29","read":"6 dk",
 "img":"levrek-marin2.jpg","alt":"Zarif bir tabak — Sapanca romantik akşam yemeği",
 "h1":"Sapanca'da <em>Romantik Akşam Yemeği</em> için En İyi Mekân",
 "title":"Sapanca Romantik Akşam Yemeği | Mare Gastro Fine Dining",
 "desc":"Yıl dönümü, evlilik teklifi ya da özel bir akşam mı? Sapanca'da romantik akşam yemeği için göl manzaralı Mare Gastro'da unutulmaz bir deneyim sizi bekliyor.",
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
  ("Sapanca'da romantik akşam yemeği nerede yenir?","Mare Gastro, Sapanca Gölü kıyısındaki Didi Otel bahçesinde göl manzaralı, romantik bir fine dining deneyimi sunar; özellikle gün batımı saatleri idealdir."),
  ("Evlilik teklifi için uygun bir mekân mı?","Evet. Atmosferi, manzarası ve özenli sunumlarıyla Mare Gastro, evlilik teklifi ve özel kutlamalar için tercih edilen bir mekândır. Özel düzenlemeleri rezervasyonda paylaşabilirsiniz."),
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
 "desc":"Sapanca'da ne yenir, nerede yemek yenir? Göl manzarasından deniz ürünlerine, gurme bir hafta sonu için Sapanca yemek rehberi ve Mare Gastro önerileri.",
 "kw":"sapanca'da ne yenir, sapanca'da nerede yemek yenir, sapanca yemek, sapanca hafta sonu",
 "lead":"Sapanca'ya gidip de doğru sofrayı bulamadan dönmek olmaz. İşte gölün kıyısında, doğanın içinde gurme bir hafta sonu için kısa ve net bir rehber.",
 "body":[
  ("Sapanca'da Lezzet Coğrafyası",
   ["Sapanca, göl manzarası ve doğasıyla yalnızca dinlenmek için değil, iyi yemek için de gidilen bir yerdir. Bölgede deniz ürünlerinden ızgaralara, zeytinyağlılardan tatlılara uzanan zengin bir yelpaze vardır.",
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
  ("Sapanca'da ne yenir?","Sapanca'da taze deniz ürünleri, ızgaralar, zeytinyağlılar ve gurme tabaklar öne çıkar. Göl manzaralı fine dining için Mare Gastro, Didi Otel bahçesinde öne çıkan bir adrestir."),
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
 "desc":"Sapanca Didi Otel bünyesindeki Mare Gastro, göl manzaralı bahçede fine dining sunar. Didi Otel restoran deneyimi, konaklama ve rezervasyon detayları.",
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
  ("Didi Otel'in restoranı hangisi?","Didi Otel bahçesindeki fine dining restoranı Mare Gastro'dur. Göl manzarasına karşı Ege ve Akdeniz mutfağı sunar."),
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
    "Bu rotanın gastronomik durağı ise %s — Didi Otel bahçesinde, göl manzaralı fine dining."%L(SITE,"Mare Gastro")]),
  ("Bir Günlük Kaçamak mı, Hafta Sonu mu?",
   ["Sapanca hem tek günlük bir kaçamağa hem de hafta sonu planına uygundur. Gündüz doğada yürüyüş, akşam Mare Gastro'da gurme bir sofra; dengeli ve unutulmaz bir program olur.",
    "Akşamı uzatmak isteyenler Didi Otel'de konaklayabilir; %s konaklama tercihini belirtmeniz yeterli."%L(REZ,"rezervasyon formunda")]),
  ("Lüks Bir Akşam Yemeği Neyi Hak Eder?",
   ["Yolculuğa değer bir akşam; manzara, hizmet ve lezzetin kusursuz buluşmasıdır. Ege ve Akdeniz'in saf tatları, Yönetici Şef Doğan Anapa'nın yorumuyla sofranıza gelir. %s keşfedin."%L(MENU,"Menüyü")]),
  ("Planınızı Önceden Yapın",
   ["Hafta sonu yoğunluğunda yerinizi garantilemek için %s öneririz; gün batımı saatleri özellikle hızlı dolar."%L(REZ,"önceden rezervasyon")]),
 ],
 "faq":[
  ("İstanbul'a yakın lüks bir restoran nerede?","Sapanca, İstanbul'a yaklaşık 1,5 saat mesafededir. Didi Otel bahçesindeki Mare Gastro, göl manzaralı fine dining ile şehre yakın lüks bir akşam yemeği sunar."),
  ("Sapanca İstanbul'a kaç saat?","Trafik durumuna göre yaklaşık 1,5 saat. Bu da Sapanca'yı hafta sonu kaçamakları için ideal kılar."),
  ("Tek günde gidip dönülür mü?","Evet. Sapanca tek günlük bir kaçamağa uygundur; gündüz doğa, akşam Mare Gastro'da gurme bir sofra ile keyifli bir gün geçirilebilir."),
  ("Konaklamalı bir plan mümkün mü?","Mare Gastro Didi Otel bünyesindedir; göl kenarında konaklayarak hafta sonunuzu uzatabilirsiniz. Rezervasyon formunda konaklama tercihinizi belirtin."),
 ],
 "rel":["sapanca-luks-restoran","sapancada-ne-yenir","didi-otel-restoran"],
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
 '<a href="%s" target="_blank" rel="noopener" aria-label="WhatsApp">%s</a>'
 '<a href="%s" aria-label="E-posta">%s</a>'
 '</div>'%(IG,IC_IG,IGCHEF,IC_IG,WA,IC_WA,MAIL,IC_MAIL))

def nav_html():
    return ('<nav class="bnav">'
      '<a class="logo" href="%s/tr/"><img src="../images/marelogo1.png" alt="Mare Gastro"></a>'
      '<div class="bnav-links">'
      '<a href="../blog/">Blog</a>'
      '<a href="%s">Menü</a>'
      '<a href="%s" class="bnav-res">Rezervasyon</a>'
      '</div></nav>'%(SITE,MENU,REZ))

def footer_html():
    return ('<footer class="bfoot">'
      '<div class="bfoot-logo"><img src="../images/marelogo1.png" alt="Mare Gastro"></div>'
      '<div class="bfoot-tag">Fine Dining · Sapanca · Didi Otel Bahçesi</div>'
      + SOCIAL_FOOT +
      '<div class="bfoot-links">'
      '<a href="%s/tr/">Ana Sayfa</a><a href="../blog/">Blog</a>'
      '<a href="%s">Menü</a><a href="%s">Rezervasyon</a><a href="%s">Konum</a>'
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
      '<a class="btn-wa" href="%s" target="_blank" rel="noopener">%s WhatsApp</a>'
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
            if para.strip().startswith("<ul") or para.strip().startswith("<ol"):
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
      "author":{"@type":"Organization","name":"Mare Gastro","url":SITE},
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
      schema=schema_graph(p))
    with open(os.path.join(OUT,"%s.html"%p["slug"]),"w",encoding="utf-8") as f: f.write(h)

INDEX = """<!DOCTYPE html>
<html lang="tr">
<head>
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
      schema=json.dumps(itemlist,ensure_ascii=False,indent=1))
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
    robots="User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n"%SITE
    with open(os.path.join(root,"robots.txt"),"w",encoding="utf-8") as f: f.write(robots)

if __name__=="__main__":
    for p in POSTS: build_post(p)
    build_index(); build_sitemap()
    print("Built %d posts + index + sitemap + robots"%len(POSTS))
