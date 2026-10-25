# -*- coding: utf-8 -*-
"""2026-10-24 GEO/AEO yenilemesi — en çok trafik alan 5 blog yazısı (GA4, son 90 gün).

build_blog.py (TR) ve posts_i18n_data.py (EN/AR/RU) bu modülü okuyup ilgili yazıların
alanlarını günceller. Yalnızca doğrulanmış bilgiler:
- Google puanı 4,9 (Google Haritalar, 24 Ekim 2026'da okundu)
- Alıntılar blog/mare-gastro-google-yorumlari.html'deki gerçek Google yorumlarından birebir
- Tabak adları/içerikleri canlı menüden (maregastro.com/api/menu, 24 Ekim 2026)
- Çalışma saati VERİLMEZ (kaynaklar çelişkili); fiyat rakamı VERİLMEZ (kullanıcı kararı),
  güncel fiyatlar için dijital menüye yönlendirilir.
"""
import html

SITE = "https://maregastro.com"
MAPS = "https://maps.google.com/?cid=7177941338358519695"
DIJITAL = SITE + "/dijitalmenu"
UPDATED = "2026-10-24"
SLUGS = ["sapanca-en-iyi-dogum-gunu-mekanlari", "sapanca-yildonumu-icin-en-iyi-mekan",
         "sapanca-fine-dining-fiyat-rehberi", "sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri",
         "sef-dogan-anapa-kimdir"]


def L(url, txt):
    return '<a href="%s">%s</a>' % (url, txt)


def purl(slug, lang="tr"):
    return "%s/blog/%s.html" % (SITE, slug) if lang == "tr" else "%s/%s/blog/%s.html" % (SITE, lang, slug)


def anchor(lang, a):
    return "%s/%s/#%s" % (SITE, lang, a)


def table(head, rows):
    th = "".join("<th>%s</th>" % h for h in head)
    tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return '<div class="btable"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, tr)


QUOTE_LABEL = {"tr": "Google yorumu", "en": "Google review", "ar": "تقييم على Google", "ru": "Отзыв в Google"}


def quote(txt, who, lang):
    return '<blockquote><p>"%s"</p><p><strong>%s</strong> · %s</p></blockquote>' % (txt, who, L(MAPS, QUOTE_LABEL[lang]))


WATCH = {"tr": "YouTube'da izle", "en": "Watch on YouTube", "ar": "شاهد على YouTube", "ru": "Смотреть на YouTube"}
VIDEO_TITLE = {
    "GiwkPYUSVyY": "Eda Acar ve Orkestrası Mare Gastro sahnesinde! | Sapanca Canlı Müzik",
    "rhSfnoAOCIg": "Karasu Kuşkonmazı ve Kaya Levreği: Şefin İmza Tabağı Nasıl Hazırlanıyor?",
    "YAbVQG4u7LI": "Balık Suyuyla Islatılmış Ekmek ve Bebek Kalamar: Şef Doğan Anapa | Mare Gastro",
}


def video(vid, caption, lang):
    return ('<figure class="bvideo"><div class="bvideo-frame"><iframe src="https://www.youtube-nocookie.com/embed/%s" '
            'title="%s" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'
            '<figcaption>%s · <a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">%s</a></figcaption></figure>'
            % (vid, html.escape(VIDEO_TITLE[vid]), html.escape(caption), vid, WATCH[lang]))


def fig(img, alt, caption):
    return ('<figure class="bbody-fig"><img src="/images/%s" alt="%s" loading="lazy">'
            '<figcaption>%s</figcaption></figure>' % (img, html.escape(alt), html.escape(caption)))


# Gerçek Google yorumları (birebir, mare-gastro-google-yorumlari.html)
Q_BDAY = ("Eşimin doğum günü için akşam yemeğine geldik. Muhammed garsonun ilgilendiği masada olmak, en az lezzetler kadar akşamımıza katkı sağladı. Şef yorumu olan yemekleri tercih ettik ve hiç pişman değiliz.", "Ardata Girgin")
Q_ANNIV1 = ("Eşimle yıl dönümümüz için gittik. Gerçekten atmosferi ve hizmeti muhteşem. Yemeklerin lezzetini, mezelerin aromasını kesinlikle denemelisiniz. En kısa sürede tekrar gideceğim kesin.", "Furkan Kavakcı")
Q_ANNIV2 = ("İlk gidişimize rağmen atmosfere hayran kaldık. Evlilik yıldönümümüzü unutulmaz kıldı bu mekan — ortam, sunum, hizmet, müzik dört dörtlüktü. Yemek sanata dönüşmüş halde önünüze geliyor.", "Büşra Canbazoğlu")
Q_DJ = ("Tesadüfen bulup yorumlara bakarak geldim, iyi ki gelmişim! Yemekler, hizmet, ambiyans çok iyi, canlı DJ müzikler de şahaneydi. Evlilik yıldönümümüz için geldik, bu kadarını beklemiyordum. Bizimle ilgilenen Süleyman Bey'e ayrıca teşekkürler.", "Fikriye Erkan")
Q_LOCAL = ("Sapanca'da yaşayan biri olarak gerçekten severek geldiğim yerlerden biri. Hem yemekleri hem atmosferi hem de hizmetiyle her seferinde memnun ayrılıyorum. Kesinlikle favorilerimden.", "Emel Kamsız")
Q_CHEF = Q_BDAY

# ══════════════════════════════════════════════════════════════════════
# TÜRKÇE
# ══════════════════════════════════════════════════════════════════════
_tr_menu = L(anchor("tr", "menu"), "güncel menümüzde")
_tr_rez = L(anchor("tr", "reservation"), "rezervasyon formu")
_tr_dij = L(DIJITAL, "dijital menüde")
_tr_g = L(MAPS, "Google Haritalar'da 4,9 puan")

REFRESH_TR = [
{
 "slug": "sapanca-en-iyi-dogum-gunu-mekanlari", "updated": UPDATED, "read": "8 dk",
 "title": "Sapanca'da Doğum Günü İçin En İyi 5 Mekan (2026) | Mare Gastro",
 "desc": "Sapanca'da doğum günü nerede kutlanır? 5 mekanı manzara, atmosfer, grup ve mutfak açısından karşılaştırdık. Google'da 4,9 puanlı Mare Gastro ve alternatifleri.",
 "lead": "Sapanca'da doğum günü mekanı seçerken manzara, atmosfer, grup büyüklüğü ve mutfak birlikte değerlendirilmeli. Bölgenin öne çıkan 5 adresini bu dört kritere göre karşılaştırdık ve 24 Ekim 2026'da güncelledik.",
 "body": [
  ("Kısa Cevap: Sapanca'da Doğum Günü Nerede Kutlanır?", [
   "Göl kenarında şık bir fine dining kutlaması için <strong>Mare Gastro</strong> (Didi Otel bahçesi, %s), canlı müzikli kalabalık bir akşam için <strong>Sasa Sapanca</strong>, samimi bir aile sofrası için <strong>Menzara</strong>, çocuklu kutlama için <strong>Green Blue</strong>, doğa ve aktivite için <strong>Natürköy</strong> öne çıkıyor. Doğru seçim, kutlamanın tarzına bağlı." % _tr_g,
  ]),
  ("5 Mekan Bir Bakışta", [
   table(["Mekan", "Öne çıkan", "En uygun kutlama", "Ortam"], [
    ["Mare Gastro", "Şef Doğan Anapa imzalı Ege-Akdeniz mutfağı, pasta ve masa süslemesi desteği", "Romantik veya zarif doğum günü, 2–12 kişilik sofralar", "Göl kıyısı, açık ve kapalı alan"],
    ["Sasa Sapanca", "Geniş dünya mutfağı menüsü, canlı müzik", "Kalabalık arkadaş grubu", "Göl kıyısı"],
    ["Menzara", "Karadeniz mutfağı, 2010'dan beri hizmet", "Samimi aile sofrası", "Göl manzaralı balkon"],
    ["Green Blue", "Deniz ürünleri, çocuk oyun alanı", "Çocuklu aile kutlaması", "Geniş bahçe"],
    ["Natürköy", "At binme, zipline gibi aktiviteler", "Gençlik grupları, gündüz kutlaması", "Vadi ve dere kenarı"],
   ]),
   "Bu karşılaştırma Mare Gastro'nun kendi blogunda hazırlandı; her mekan için yalnızca doğrulanabilir özellikleri yazdık. Fiyat ve çalışma saatleri değişebildiği için her mekandan güncel bilgiyi doğrudan almanızı öneririz.",
  ]),
  ("Sapanca'da Doğum Günü Mekanı Seçerken Nelere Bakılmalı?", [
   "Sapanca Gölü çevresinde onlarca restoran var, ama her biri her kutlamaya uygun değil. Dört kriter öne çıkıyor:",
   "<ul><li><strong>Manzara:</strong> Göl kıyısında mı, yoksa bahçe/doğa odaklı mı?</li><li><strong>Kutlama desteği:</strong> Pasta, mum, masa süslemesi ve sürpriz için ekip planlama yapıyor mu?</li><li><strong>Grup büyüklüğü:</strong> İkili bir sofra mı, 15 kişilik bir arkadaş grubu mu?</li><li><strong>Mutfak:</strong> À la carte fine dining mi, geniş ve gündelik bir menü mü?</li></ul>",
  ]),
  ("1. Mare Gastro — Gölün Hemen Yanında Fine Dining Kutlama", [
   "Mare Gastro, Sapanca'da Didi Otel bahçesinde, göl kıyısında yer alan bir fine dining restoran. Yönetici Şef Doğan Anapa'nın Ege-Akdeniz mutfağıyla à la carte servis yapıyor; doğum günü için pasta ve masa süslemesi talepleri rezervasyon sırasında ekiple birlikte planlanıyor.",
   fig("mare-kutlama-kadeh.webp", "Mare Gastro'da bir doğum günü kutlaması", "Mare Gastro'da bir kutlama sofrası"),
   "Menüde 13 başlangıç, 8 ara sıcak ve 8 ana yemek yer alıyor (Ekim 2026). Doğum günü sofralarında sık tercih edilenler arasında Mare Spesiyal Granyöz (kaya levreği, beurre blanc sos), Biber Kremalı Bonfile ve imza tatlı Ormanda Bir Yürüyüş (çikolata mus, çıtır profiterol, ev yapımı vanilyalı dondurma) var. Tüm tabakları %s görebilirsiniz." % _tr_menu,
   quote(Q_BDAY[0], Q_BDAY[1], "tr"),
   "Canlı müzik akşamları da düzenleniyor; misafir yorumlarında canlı müzik ve DJ performansları sıkça geçiyor. Didi Otel bünyesinde olduğu için kutlama sonrası göl kenarında konaklamak da mümkün.",
  ]),
  ("2. Sasa Sapanca — Canlı Müzik Eşliğinde Göl Kıyısında", [
   "Göl kıyısındaki Sasa Sapanca; mezeler, burger, taco, kırmızı et ve balık gibi dünya mutfağından geniş bir menü ve canlı müzik sunuyor. Farklı damak zevklerine sahip kalabalık bir grubu ağırlamak için pratik bir seçenek.",
  ]),
  ("3. Menzara — Karadeniz Mutfağı ve Balkon Manzarası", [
   "2010'dan beri hizmet veren Menzara, göl manzaralı balkonu ve taş fırın ekmek, balık ve ızgara ağırlıklı Karadeniz mutfağıyla biliniyor. Ev sıcaklığında, samimi bir kutlama arayanlar için uygun.",
  ]),
  ("4. Green Blue — Çocuklu Aile Kutlamaları İçin Geniş Bahçe", [
   "Deniz ürünleri ağırlıklı menüsü ve geniş bahçesiyle Green Blue, çocuklu aile kutlamalarında öne çıkıyor. Bahçedeki çocuk oyun alanı, küçük yaş grubu doğum günlerinde ebeveynlere rahat bir alan sağlıyor.",
  ]),
  ("5. Natürköy — Doğa İçinde Aktiviteli Bir Kutlama", [
   "Vadi içinde, dere üzerine kurulu ahşap kulübeleriyle Natürköy, fine dining yerine doğa temalı bir deneyim sunuyor. At binme ve zipline gibi aktivitelerle desteklenen bir kutlama isteyen gençlik grupları için değerlendirilebilir.",
  ]),
  ("Hangi Mekanı Seçmelisiniz?", [
   "<ul><li><strong>Romantik veya zarif bir akşam:</strong> Mare Gastro</li><li><strong>Kalabalık ve hareketli bir gece:</strong> Sasa Sapanca</li><li><strong>Samimi aile sofrası:</strong> Menzara</li><li><strong>Çocuklu kutlama:</strong> Green Blue</li><li><strong>Gündüz aktivite:</strong> Natürköy</li></ul>",
   "Mare Gastro'da kutlama planlıyorsanız %s üzerinden kişi sayısını ve pasta/süsleme talebinizi iletebilirsiniz. Bütçe planı için %s yazımıza da göz atın." % (_tr_rez, L(purl("sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri"), "doğum günü fiyatları ve menü seçenekleri")),
  ]),
 ],
 "faq": [
  ("Sapanca'da doğum günü için en iyi mekan hangisi?", "Kutlamanın tarzına bağlı. Göl kenarında fine dining bir doğum günü için Didi Otel bahçesindeki Mare Gastro, canlı müzikli kalabalık bir akşam için Sasa Sapanca, çocuklu aile kutlaması için Green Blue öne çıkıyor."),
  ("Mare Gastro doğum günü için pasta veya süsleme ayarlıyor mu?", "Evet. Rezervasyon sırasında talebinizi ilettiğinizde pasta ve masa süslemesi detayları ekiple birlikte planlanır."),
  ("Sapanca'da göl manzaralı doğum günü mekanları hangileri?", "Mare Gastro, Sasa Sapanca ve Menzara göl kıyısında veya göl manzaralı; Green Blue ve Natürköy daha çok bahçe ve doğa odaklı bir atmosfer sunar."),
  ("Kalabalık bir arkadaş grubuyla doğum günü için hangi mekan uygun?", "Geniş menüsü ve canlı müziğiyle Sasa Sapanca, ya da daha özel ve şık bir sofra için Mare Gastro değerlendirilebilir. Kalabalık gruplarda önceden rezervasyon yapmak önemli."),
  ("Mare Gastro'nun Google puanı kaç?", "Mare Gastro'nun Google Haritalar puanı 24 Ekim 2026 itibarıyla 4,9. Misafirler yorumlarda en çok atmosferi, servisi ve özel gün organizasyonunu öne çıkarıyor."),
  ("Doğum günü kutlamasından sonra Sapanca'da konaklayabilir miyim?", "Evet. Mare Gastro, Didi Otel bahçesinde yer aldığı için konaklama tercihinizi rezervasyon formunda belirtebilirsiniz."),
 ],
},
{
 "slug": "sapanca-yildonumu-icin-en-iyi-mekan", "updated": UPDATED, "read": "8 dk",
 "title": "Sapanca'da Yıldönümü İçin En İyi 5 Mekan (2026) | Mare Gastro",
 "desc": "Sapanca'da evlilik yıldönümü nerede kutlanır? 5 mekanı göl manzarası, romantik atmosfer ve sürpriz desteğine göre karşılaştırdık. Gerçek Google yorumlarıyla.",
 "lead": "Bir yıldönümü akşamında mekan seçimi; göl manzarası, romantik atmosfer ve sürpriz organizasyonu birlikte değerlendirilerek yapılmalı. Sapanca'nın öne çıkan 5 adresini bu kriterlere göre karşılaştırdık ve 24 Ekim 2026'da güncelledik.",
 "body": [
  ("Kısa Cevap: Sapanca'da Yıldönümü Nerede Kutlanır?", [
   "Göl kenarında, mum ışığında romantik bir yıldönümü yemeği için <strong>Mare Gastro</strong> (%s), canlı müzikli bir akşam için <strong>Sasa Sapanca</strong>, samimi bir sofra için <strong>Menzara</strong> öne çıkıyor. Şehirden tamamen uzaklaşmak isteyen çiftler için <strong>Natürköy</strong> doğa içinde sakin bir alternatif." % _tr_g,
  ]),
  ("5 Mekan Bir Bakışta", [
   table(["Mekan", "Romantik atmosfer", "Sürpriz desteği", "Konaklama"], [
    ["Mare Gastro", "Göl kıyısı, mum ışığı, açık ve kapalı alan", "Pasta, çiçek ve masa süslemesi rezervasyonda planlanır", "Didi Otel bünyesinde"],
    ["Sasa Sapanca", "Göl kıyısı, canlı müzik", "Mekana sorulmalı", "—"],
    ["Menzara", "Göl manzaralı balkon", "Mekana sorulmalı", "—"],
    ["Green Blue", "Geniş bahçe, aile odaklı", "Mekana sorulmalı", "—"],
    ["Natürköy", "Vadi, dere kenarı kulübeler", "Mekana sorulmalı", "Kulübe konaklama"],
   ]),
   "Karşılaştırma Mare Gastro'nun kendi blogunda hazırlandı; diğer mekanlar için yalnızca doğrulanabilir özellikleri yazdık ve sürpriz desteği gibi detayları doğrudan mekana sormanızı öneriyoruz.",
  ]),
  ("Sapanca'da Yıldönümü Mekanı Seçerken Nelere Bakılmalı?", [
   "<ul><li><strong>Manzara:</strong> Gün batımında göl manzarası, yıldönümü akşamını en çok güzelleştiren detay.</li><li><strong>Atmosfer:</strong> Mum ışığı ve sakin bir masa düzeni ikili sofra için önemli.</li><li><strong>Sürpriz organizasyonu:</strong> Pasta, çiçek ya da masaya özel bir not için ekip önceden plan yapıyor mu?</li><li><strong>Gerçek misafir deneyimi:</strong> Google yorumlarında yıldönümü kutlayan çiftler ne anlatıyor?</li></ul>",
  ]),
  ("1. Mare Gastro — Gölün Hemen Yanında Romantik Bir Yıldönümü Sofrası", [
   "Mare Gastro, Didi Otel bahçesinde, Sapanca Gölü kıyısında yer alan bir fine dining restoran. Yıldönümü için pasta, çiçek düzenlemesi ve masa süslemesi talepleri rezervasyon sırasında tek tek planlanıyor; mutfakta Yönetici Şef Doğan Anapa'nın Ege-Akdeniz menüsü var.",
   fig("mare-romantik-kadeh.webp", "Mare Gastro'da gölün yanında kadeh tokuşturan çift", "Mare Gastro'da yıldönümü akşamı"),
   "Yorumlarda yıldönümünü Mare Gastro'da kutlayan çiftler en çok atmosferi, servisi ve müziği anıyor:",
   quote(Q_ANNIV2[0], Q_ANNIV2[1], "tr"),
   quote(Q_ANNIV1[0], Q_ANNIV1[1], "tr"),
   "İkili sofralarda sık tercih edilen tabaklar arasında Palamut Carpaccio, Kereviz Püreli Jumbo Karides Söğüş, Fırında Kremalı Levrek ve Çerkes Peynirli Cheesecake var. Didi Otel bünyesinde olduğu için akşamı göl kenarında konaklayarak uzatabilirsiniz.",
  ]),
  ("2. Sasa Sapanca — Canlı Müzik Eşliğinde Göl Kıyısında", [
   "Göl kıyısındaki Sasa Sapanca, dünya mutfağından geniş bir menü ve canlı müzikle hareketli bir akşam yemeği atmosferi sunuyor. Farklı damak zevkleri olan çiftler için pratik bir seçenek.",
  ]),
  ("3. Menzara — Karadeniz Mutfağı ve Balkon Manzarası", [
   "2010'dan beri hizmet veren Menzara, göl manzaralı balkonu ve Karadeniz ağırlıklı mutfağıyla daha samimi, ev sıcaklığında bir yıldönümü sofrası arayan çiftlere hitap ediyor.",
  ]),
  ("4. Green Blue — Geniş Bahçe, Aile Atmosferi", [
   "Deniz ürünleri ağırlıklı menüsü ve geniş bahçesiyle Green Blue, ikili bir sofradan çok ailece yapılan kutlamalar için uygun bir atmosfer sunuyor.",
  ]),
  ("5. Natürköy — Doğa İçinde Sakin Bir Kutlama", [
   "Vadi içinde, dere üzerine kurulu ahşap kulübeleriyle Natürköy, fine dining yerine doğa temalı bir deneyim sunuyor. Şehirden tamamen kopmak isteyen çiftler için değerlendirilebilir.",
  ]),
  ("Hangi Mekanı Seçmelisiniz?", [
   "Göl manzarası, fine dining mutfak, sürpriz organizasyonu ve konaklama imkânını bir arada arıyorsanız Mare Gastro bu listedeki en eksiksiz seçenek. Canlı müzikli hareketli bir akşam için Sasa Sapanca, samimi bir sofra için Menzara, doğa içinde sakinlik için Natürköy tercih edilebilir.",
   "Planınızı %s üzerinden iletebilir, %s ve %s yazılarımıza da göz atabilirsiniz." % (_tr_rez, L(purl("sapanca-yildonumu-yemegi"), "yıldönümü yemeği rehberimiz"), L(purl("sapanca-esinizle-ozel-aksam"), "eşinizle özel bir akşam")),
  ]),
 ],
 "faq": [
  ("Sapanca'da yıldönümü kutlamak için en iyi mekan hangisi?", "Göl kenarında romantik bir fine dining akşamı için Didi Otel bahçesindeki Mare Gastro, canlı müzikli bir akşam için Sasa Sapanca, samimi bir sofra için Menzara öne çıkan seçenekler."),
  ("Mare Gastro yıldönümü için sürpriz pasta ayarlıyor mu?", "Evet. Rezervasyon sırasında talebinizi ilettiğinizde pasta, çiçek düzenlemesi ve masa süslemesi ekiple birlikte planlanır."),
  ("Sapanca'da göl manzaralı romantik restoranlar hangileri?", "Mare Gastro, Sasa Sapanca ve Menzara göl kıyısında veya göl manzaralı; Green Blue ve Natürköy daha çok bahçe ve doğa odaklı."),
  ("Mare Gastro'nun Google yorumlarındaki puanı kaç?", "24 Ekim 2026 itibarıyla Google Haritalar puanı 4,9. Yıldönümü kutlayan çiftler yorumlarda en çok atmosferi, servisi ve müziği öne çıkarıyor."),
  ("Yıldönümü akşamı Sapanca'da konaklama mümkün mü?", "Evet. Mare Gastro, Didi Otel bünyesinde yer alıyor; konaklama tercihinizi rezervasyon formunda belirtebilirsiniz."),
  ("Yıldönümü için ne kadar önceden rezervasyon yapmalıyım?", "Hafta sonları ve özel günlerde göl kenarındaki masalar hızlı doluyor; birkaç gün önceden rezervasyon yapmanız ve sürpriz taleplerinizi o sırada iletmeniz önerilir."),
 ],
},
{
 "slug": "sapanca-fine-dining-fiyat-rehberi", "updated": UPDATED, "read": "6 dk",
 "title": "Sapanca'da Fine Dining Fiyatları: Neye Göre Değişir? (2026) | Mare Gastro",
 "desc": "Sapanca'da fine dining fiyatı neye göre değişir, kişi başı neler dahildir, güncel fiyatlar nereden görülür? Mare Gastro'dan şeffaf bir 2026 rehberi.",
 "lead": "Sapanca'da fine dining bir akşam planlarken ilk sorulardan biri fiyat. Mare Gastro'da à la carte bir menü var; hesabı neyin belirlediğini ve güncel fiyatları nereden görebileceğinizi bu rehberde topladık. Son güncelleme: 24 Ekim 2026.",
 "body": [
  ("Kısa Cevap: Sapanca'da Fine Dining Ne Kadar Tutar?", [
   "Sapanca'da fine dining bir akşamın tutarı; seçilen tabaklara, kişi sayısına, mevsime ve içeceklere göre değişir. Mare Gastro'da sabit bir set menü yok, à la carte sipariş veriliyor. Tabak tabak güncel fiyatlar Mare Gastro'nun %s yer alıyor; içecekler ayrıca hesaplanıyor." % _tr_dij,
  ]),
  ("Fiyatı Belirleyen 5 Unsur", [
   table(["Unsur", "Hesaba etkisi", "Mare Gastro'da"], [
    ["Tabak seçimi", "En belirleyici unsur", "13 başlangıç, 8 ara sıcak, 8 ana yemek, 5 tatlı (Ekim 2026)"],
    ["Ana malzeme", "Deniz ürünleri ve kırmızı et fiyatı yükseltir", "Kaya levreği, jumbo karides, dana bonfile, kuzu pirzola"],
    ["Kişi sayısı ve paylaşım", "Mezeler paylaşılınca kişi başı düşer", "Başlangıçlar masaya ortaya söylenebilir"],
    ["İçecekler", "Şarap ve rakı hesabı ciddi şekilde etkiler", "Şarap, rakı ve kokteyl listesi ayrı"],
    ["Mevsim", "Menü mevsime göre değişir", "Bazı tabaklar sezon dışında menüden çıkar"],
   ]),
  ]),
  ("Kişi Başı Ücrete Neler Dahildir?", [
   "Bir fine dining akşamında hesap, sipariş ettiğiniz tabaklardan oluşur: genellikle bir başlangıç ya da paylaşılan mezeler, bir ana yemek ve bir tatlı. Mare Gastro'da buna gölün hemen yanındaki masa, açık ve kapalı alan seçeneği ve özenli servis eşlik ediyor.",
   "Örneğin Mare Spesiyal Granyöz; 200 gr kaya levreği, fırınlanmış baby patates, köz yeşil biber sos, köz domates ve beurre blanc sosla geliyor. Biber Kremalı Bonfile 200 gr dana bonfile, karabiber kremalı sos ve kibrit patatesle servis ediliyor. Gramajların menüde yazılı olması, fiyat/performansı önceden değerlendirmenizi kolaylaştırıyor.",
  ]),
  ("Fiyat/Performans Açısından Nelere Dikkat Etmeli?", [
   "<ul><li><strong>Gramaj ve içerik:</strong> Menüde gramajı ve içeriği yazılı tabaklar, neye ödediğinizi netleştirir.</li><li><strong>Malzemenin tazeliği:</strong> Deniz ürünlerinde tazelik, fiyat farkının asıl nedenidir.</li><li><strong>Atmosfer:</strong> Göl kıyısında bir masa ve sakin bir bahçe, deneyimin parçasıdır.</li><li><strong>Misafir deneyimi:</strong> Fiyatı tartarken gerçek yorumlara bakın; Mare Gastro'nun %s.</li></ul>" % _tr_g,
   quote(Q_LOCAL[0], Q_LOCAL[1], "tr"),
  ]),
  ("Güncel Fiyatları Nereden Görebilirim?", [
   "Ürün ürün güncel fiyatlar Mare Gastro'nun %s listeleniyor; ana sitedeki %s tabakların içeriklerini görebilirsiniz. Kalabalık grup veya özel gün planlarınız için %s ya da WhatsApp üzerinden ekiple görüşebilirsiniz." % (_tr_dij, L(anchor("tr", "menu"), "menüde"), _tr_rez),
   "Şefin mutfak anlayışını tanımak için %s yazımızı okuyabilirsiniz." % L(purl("sef-dogan-anapa-kimdir"), "Şef Doğan Anapa kimdir"),
  ]),
 ],
 "faq": [
  ("Sapanca'da fine dining kişi başı ne kadar?", "Tutar seçilen tabaklara, içeceklere ve kişi sayısına göre değişir. Mare Gastro'da à la carte menü var; güncel tabak fiyatları maregastro.com/dijitalmenu adresindeki dijital menüde yer alıyor."),
  ("Mare Gastro'da set menü var mı?", "Hayır. Mare Gastro'da sabit bir set menü yok; başlangıç, ara sıcak, ana yemek ve tatlılar à la carte olarak seçiliyor."),
  ("Mare Gastro'nun güncel fiyatlarını nereden görebilirim?", "Ürün bazında güncel fiyatlar Mare Gastro'nun dijital menüsünde (maregastro.com/dijitalmenu) listeleniyor."),
  ("İçecekler fiyata dahil mi?", "Hayır. Şarap, rakı, kokteyl ve diğer içecekler menüden ayrıca seçilir ve ayrıca hesaplanır."),
  ("Kuver ücreti var mı?", "Kuver ve servis detayları rezervasyon sırasında netleştirilir; ekip tüm sorularınızı yanıtlar."),
  ("Fine dining fiyatını en çok ne etkiler?", "En belirleyici unsur tabak seçimidir; deniz ürünleri ve kırmızı et ağırlıklı tabaklar ile şarap tercihi hesabı en çok etkileyen kalemlerdir."),
 ],
},
{
 "slug": "sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri", "updated": UPDATED, "read": "7 dk",
 "videos": ["GiwkPYUSVyY"],
 "title": "Sapanca'da Doğum Günü Fiyatları ve Menü Seçenekleri (2026) | Mare Gastro",
 "desc": "Sapanca'da doğum günü kutlaması ne kadar tutar? Mare Gastro'nun à la carte menüsü, kutlamaya uygun tabakları, pasta ve süsleme süreci ve güncel fiyat bilgisi.",
 "lead": "Sapanca'da doğum günü bütçesi planlarken mekanın sunduğu deneyimle fiyatını birlikte değerlendirmek gerekir. Mare Gastro'nun menü yapısını, kutlamaya uygun tabakları ve rezervasyon sürecini bu rehberde topladık. Son güncelleme: 24 Ekim 2026.",
 "body": [
  ("Kısa Cevap: Sapanca'da Doğum Günü Kutlaması Ne Kadar Tutar?", [
   "Tutar; kişi sayısına, seçilen tabaklara, içeceklere ve pasta/süsleme taleplerine göre değişir. Mare Gastro'da sabit bir doğum günü paketi yok; à la carte menüden sipariş veriliyor ve güncel fiyatlar tabak tabak %s yer alıyor. Pasta ve süsleme rezervasyon sırasında ayrıca planlanıyor." % _tr_dij,
  ]),
  ("Doğum Günü Sofrası İçin Menü Seçenekleri", [
   table(["Bölüm", "Kutlamaya uygun örnekler (Ekim 2026)"], [
    ["Paylaşımlık başlangıçlar", "Pancar Borani, Havuç Tarator, Patates Cipsli Acılı Atom, Humus, Peynir Tabağı"],
    ["Ara sıcaklar", "3'lü Deniz Mahsülü Lezzeti, Kalamar Tava, Tereyağlı Karides"],
    ["Ana yemekler", "Mare Spesiyal Granyöz, Biber Kremalı Bonfile, Kuzu Pirzola, Çıtır Somon"],
    ["Tatlılar", "Ormanda Bir Yürüyüş, Çerkes Peynirli Cheesecake, Çıtır Kabak Tatlısı, Mare Şekerpare"],
    ["Çocuk menüsü", "Izgara Köfte, Domates Soslu Makarna"],
   ]),
   "Kalabalık sofralarda başlangıçları ve ara sıcakları ortaya söyleyip ana yemekleri kişiye göre seçmek hem bütçeyi hem de akşamın akışını dengeler.",
  ]),
  ("Fiyatı Neler Belirler?", [
   "<ul><li><strong>Kişi sayısı:</strong> Toplam tutarı en çok etkileyen unsur.</li><li><strong>Tabak seçimi:</strong> Deniz ürünleri ve kırmızı et ağırlıklı ana yemekler hesabı yükseltir.</li><li><strong>İçecekler:</strong> Şarap, rakı ve kokteyller ayrıca hesaplanır.</li><li><strong>Pasta ve süsleme:</strong> Talebinize göre rezervasyon sırasında ayrıca netleşir.</li><li><strong>Mevsim:</strong> Menü mevsime göre güncellenir.</li></ul>",
  ]),
  ("Pasta ve Süsleme Nasıl Planlanıyor?", [
   "Rezervasyon sırasında kişi sayısını, tarihi ve pasta ya da masa süslemesi talebinizi iletirsiniz; detaylar ekiple birlikte netleştirilir. Misafir yorumları da bu özene dikkat çekiyor:",
   quote(Q_BDAY[0], Q_BDAY[1], "tr"),
   "Doğum günü akşamları canlı müzikle de renklenebiliyor; Mare Gastro sahnesinde düzenlenen canlı müzik akşamlarından birini aşağıda izleyebilirsiniz.",
   video("GiwkPYUSVyY", "Mare Gastro'da canlı müzik akşamı", "tr"),
  ]),
  ("Güncel Fiyat Bilgisini Nereden Öğrenebilirim?", [
   "Ürün ürün güncel fiyatlar Mare Gastro'nun %s listeleniyor. Kişi sayısı ve özel taleplerle birlikte bir plan yapmak için %s ya da WhatsApp üzerinden ekiple görüşebilirsiniz." % (_tr_dij, _tr_rez),
   "Mekan karşılaştırması için %s yazımıza bakabilirsiniz." % L(purl("sapanca-en-iyi-dogum-gunu-mekanlari"), "Sapanca'da doğum günü için en iyi 5 mekan"),
  ]),
 ],
 "faq": [
  ("Sapanca'da doğum günü kutlaması ne kadar tutar?", "Kişi sayısına, seçilen tabaklara ve içeceklere göre değişir. Mare Gastro'da à la carte menü var; güncel tabak fiyatları maregastro.com/dijitalmenu adresindeki dijital menüde yer alıyor."),
  ("Mare Gastro'da doğum günü paketi var mı?", "Hayır. Sabit bir paket yerine à la carte menüden seçim yapılıyor; pasta ve süsleme talepleri rezervasyon sırasında ayrıca planlanıyor."),
  ("Pasta ve süsleme fiyata dahil mi?", "Hayır, pasta ve süsleme talepleri rezervasyon sırasında ayrıca değerlendirilir ve netleştirilir."),
  ("İçecekler fiyata dahil mi?", "Hayır. İçecekler menüden ayrıca seçilir ve ayrıca hesaplanır."),
  ("Çocuklar için menü var mı?", "Evet. Çocuk menüsünde Izgara Köfte ve Domates Soslu Makarna bulunuyor."),
  ("Güncel fiyat bilgisini nasıl öğrenebilirim?", "Dijital menüden ürün bazında fiyatları görebilir, kalabalık grup planları için rezervasyon formu veya WhatsApp üzerinden ekiple görüşebilirsiniz."),
 ],
},
{
 "slug": "sef-dogan-anapa-kimdir", "updated": UPDATED, "read": "6 dk",
 "videos": ["YAbVQG4u7LI", "rhSfnoAOCIg"],
 "title": "Şef Doğan Anapa Kimdir? Hangi Restoranın Şefi? | Mare Gastro",
 "desc": "Şef Doğan Anapa kimdir, şu anda hangi restoranın şefi? Sapanca'daki Mare Gastro'nun Yönetici Şefi Doğan Anapa'nın mutfak anlayışı, imza tabakları ve videoları.",
 "lead": "Doğan Anapa, Sapanca'da Didi Otel bahçesindeki Mare Gastro'nun Yönetici Şefi. Şefin bugünkü adresi, mutfak anlayışı ve imza tabakları hakkında bilmeniz gerekenleri derledik. Son güncelleme: 24 Ekim 2026.",
 "body": [
  ("Kısa Cevap: Doğan Anapa Kimdir?", [
   "Doğan Anapa, Sapanca'da Didi Otel bahçesinde yer alan <strong>Mare Gastro</strong>'nun Yönetici Şefi'dir. Taze ve mevsimsel malzemeye dayanan, deniz ürünleri ağırlıklı bir Ege-Akdeniz fine dining mutfağı yürütüyor. Sinema geçmişinden gelen anlatı odaklı bakışı, tabaklarını bir sahne gibi kurgulamasıyla biliniyor.",
  ]),
  ("Doğan Anapa Hakkında Temel Bilgiler", [
   table(["", ""], [
    ["Görevi", "Yönetici Şef, Mare Gastro"],
    ["Restoran", "Mare Gastro — Didi Otel bahçesi, Sapanca/Sakarya"],
    ["Mutfak", "Ege-Akdeniz, deniz ürünleri ağırlıklı, mevsimsel fine dining"],
    ["Geçmişi", "Mutfağa sinema geçmişinden gelen anlatı odaklı bir bakışla yöneliyor"],
    ["Takip", L("https://www.instagram.com/chefdogananapa/", "@chefdogananapa") + " · " + L("https://www.youtube.com/@maregastro", "Mare Gastro YouTube")],
   ]),
  ]),
  ("Doğan Anapa Şu Anda Hangi Restoranın Şefi?", [
   "Doğan Anapa bugün Sapanca'da, Didi Otel bahçesindeki Mare Gastro'nun mutfağını yönetiyor. Gölün hemen yanında kurulan mutfakta à la carte bir menü hazırlıyor; Ekim 2026 itibarıyla menüde 13 başlangıç, 8 ara sıcak ve 8 ana yemek bulunuyor. Konsept, Didi Otel bünyesinde Kadir Çiçek tarafından hayata geçirildi.",
  ]),
  ("Doğan Anapa'nın Mutfak Anlayışı Nedir?", [
   "Anapa'nın mutfağı üç ilke üzerine kurulu: taze ve yerel malzeme, mevsimsellik ve sade ama etkileyici sunum. Bölgenin mutfak geleneklerinden ilham alıp bunları fine dining tabaklara dönüştürüyor. Örneğin Mare Spesiyal Islama Kalamar, Adapazarı'nın ıslama köfte geleneğinden ilham alıyor: balık suyuyla ıslatılmış ekmek üzerinde ızgara bebek kalamar.",
   video("YAbVQG4u7LI", "Şef Doğan Anapa, ıslama kalamarı hazırlıyor", "tr"),
  ]),
  ("Doğan Anapa'nın İmza Tabakları Nelerdir?", [
   "<ul><li><strong>Mare Spesiyal Granyöz:</strong> 200 gr kaya levreği, fırınlanmış baby patates, köz yeşil biber sos, köz domates ve beurre blanc sos.</li><li><strong>Mare Spesiyal Islama Kalamar:</strong> 3 adet ızgara baby kalamar, naneli hardallı sos ve küp domates.</li><li><strong>Deniz Mahsülleri Buğday Risotto:</strong> Sarımsaklı tereyağında jumbo karides ve kum midyesi, Trakya eski kaşar.</li><li><strong>Palamut Carpaccio:</strong> Sarımsaklı vinegret, kırmızı ve yeşil soğan, kapari, maydanoz, dereotu.</li><li><strong>Ormanda Bir Yürüyüş:</strong> Çikolata mus, çıtır profiterol hamuru, Mare yapımı vanilyalı dondurma ve çilek.</li></ul>",
   "Şef, kaya levreğini Karasu kuşkonmazıyla buluşturduğu imza tabağını adım adım anlatıyor:",
   video("rhSfnoAOCIg", "Kaya levreği ve Karasu kuşkonmazı", "tr"),
   "Tabakların güncel hallerini %s görebilirsiniz. Misafirler de yorumlarda şefin önerdiği tabakları anıyor:" % _tr_menu,
   quote(Q_BDAY[0], Q_BDAY[1], "tr"),
  ]),
  ("Doğan Anapa'nın Mutfak Yolculuğu", [
   "Doğan Anapa'nın mutfağa bakışı sinema geçmişinden besleniyor; her tabağı bir sahne, her menüyü bir anlatı gibi kurguluyor. Şefin sinemadan mutfağa uzanan hikâyesini %s yazımızda okuyabilirsiniz." % L(purl("sef-dogan-anapa"), "Şef Doğan Anapa"),
   "Şefin tabaklarını denemek için %s üzerinden masa ayırtabilirsiniz." % _tr_rez,
  ]),
 ],
 "faq": [
  ("Doğan Anapa hangi restoranın şefi?", "Doğan Anapa, Sapanca'da Didi Otel bahçesinde yer alan Mare Gastro'nun Yönetici Şefi'dir."),
  ("Doğan Anapa'nın mutfak tarzı nedir?", "Taze, yerel ve mevsimsel malzemeye dayanan, deniz ürünleri ağırlıklı bir Ege-Akdeniz fine dining mutfağı; sinema geçmişinden gelen anlatı odaklı bir yaklaşımla menüyü kurguluyor."),
  ("Doğan Anapa'nın imza yemekleri nelerdir?", "Mare Spesiyal Granyöz (kaya levreği, beurre blanc), Mare Spesiyal Islama Kalamar, Deniz Mahsülleri Buğday Risotto, Palamut Carpaccio ve Ormanda Bir Yürüyüş tatlısı öne çıkan tabaklar arasında."),
  ("Mare Gastro nerede?", "Mare Gastro, Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, Sapanca/Sakarya adresinde, Didi Otel bahçesinde, Sapanca Gölü kıyısında."),
  ("Şef Doğan Anapa'nın yemek videolarını nereden izleyebilirim?", "Mare Gastro'nun YouTube kanalında (@maregastro) şefin imza tabaklarını hazırladığı videolar yayınlanıyor; Instagram'da @chefdogananapa hesabını takip edebilirsiniz."),
 ],
},
]
