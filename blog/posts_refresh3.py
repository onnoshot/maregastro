# -*- coding: utf-8 -*-
"""2026-11-16 SEO/GEO yenilemesi — en çok gösterim/tıklama alan 10 blog yazısı.

Seçim: Search Console (2026-08-15..11-13, 90 gün) gösterim + tıklama ve GA4 (90 gün) blog görüntüleme.
Sorunlar: uzun/kesilen başlıklar, düşük CTR, eski menü bilgisi (çocuk menüsü, ana yemek sayısı),
"göl kıyısı" ifadesi, yemek tabağı kapakları, tablo/SSS eksikliği, 200-400 kelimelik ince içerik,
sapancaya-nasil-gidilir'in DİDİ Otel'in seyahat rehberiyle çakışması.

Kullanılan bilgiler yalnızca doğrulanmış olanlar:
- Canlı menü (maregastro.com/api/menu, 10 Kasım 2026 güncellemesi): 13 başlangıç, 3 salata,
  8 ara sıcak, 11 ana yemek, 5 tatlı, 2 kahvaltı, 1 çocuk menüsü tabağı, 4 atıştırmalık; Ekstralar'da pasta.
- Çalışma saatleri Salı–Pazar 09:00–00:00, Pazartesi kapalı (site + Instagram 12 Kasım 2026).
- Açılış: Instagram @maregastro, 30 Haziran 2026 "Mare Gastro Sapanca açıldı".
- Google Haritalar puanı 4,9 (24 Ekim 2026'da okundu).
- Ücretsiz otopark + vale; açık ve kapalı alan; çoğu hafta sonu canlı müzik; Didi Otel'de konaklama.
- Fiyat rakamı YOK (kullanıcı kararı); güncel fiyatlar dijital menüde.
build_blog.py bu modülü REFRESH_TR/REFRESH_TR2'den SONRA uygular.
Anahtarlar: düz alanlar (title, desc, lead, body, faq, rel, img, alt, ...) doğrudan güncellenir;
"insert" = [(konum, [(H2, [paragraf...])])] mevcut gövdeye eklenir; "faq_add" mevcut SSS'ye eklenir.
"""
import html
from posts_refresh import L, table, quote, video, VIDEO_TITLE, Q_BDAY, Q_ANNIV1, Q_ANNIV2, Q_LOCAL, MAPS

UPDATED = "2026-11-16"
SITE = "https://maregastro.com"
MENU = SITE + "/menu/"
REZ = SITE + "/tr/#reservation"
FOTO = SITE + "/fotograflar.html"
SSS = SITE + "/sss.html"
WA = "https://wa.me/905323540888"
IG = "https://www.instagram.com/maregastro/"
TT = "https://www.tiktok.com/@maregastro"
YT = "https://www.youtube.com/@maregastro"
DIDI = "https://www.sapancadidiotel.com/"
DIDI_YOL = "https://www.sapancadidiotel.com/blog/sapancaya-nasil-gidilir/"
DIDI_KIRKPINAR = "https://www.sapancadidiotel.com/blog/kirkpinar-sapanca-konaklama/"
ADRES = "Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, 54600 Sapanca/Sakarya"
MAPS_DEST = "40.7002438,30.222254"
GPUAN = L(MAPS, "Google Haritalar'da 4,9 puan")

VIDEO_TITLE.update({
    "aOAyrgTBcos": "Sapanca'da Saklı Fine Dining Deneyimi: Mare Gastro",
    "Asn8FZ0nFX0": "Şef Doğan Anapa'nın Sunumuyla: Mare Gastro'da İmza Tabak Kuzu İncik ve Keşkek",
    "zseYjYW3uFk": "Lezzetli Karidesin Sırrı Kabuğunda Gizli! Şef Doğan Anapa & Kadir Çiçek | Mare Gastro Sapanca",
    "NybLKER1j_4": "Deniz Mahsullü Buğday Risotto Nasıl Yapılır? | Mare Gastro Sapanca & Şef Doğan Anapa",
})


def purl(slug):
    return "%s/blog/%s.html" % (SITE, slug)


def P(slug, txt):
    return L(purl(slug), txt)


def ext(url, txt):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, txt)


def fig(img, alt, caption, portrait=False):
    return ('<figure class="bbody-fig%s"><img src="/images/%s" alt="%s" loading="lazy">'
            '<figcaption>%s</figcaption></figure>' % (" bfig-portrait" if portrait else "", img, html.escape(alt), html.escape(caption)))


def igfig(img, alt, caption, url, portrait=False, label="Instagram'da izle"):
    """Mare Gastro'nun kendi Instagram paylaşımına bağlanan, yerel görselli hafif figür (üçüncü taraf script yok)."""
    return ('<figure class="bbody-fig%s"><img src="/images/%s" alt="%s" loading="lazy">'
            '<figcaption>%s · <a href="%s" target="_blank" rel="noopener">%s</a></figcaption></figure>'
            % (" bfig-portrait" if portrait else "", img, html.escape(alt), html.escape(caption), url, label))


def mapdir(origin, label):
    from urllib.parse import quote as q
    return ('<a href="https://www.google.com/maps/dir/?api=1&amp;origin=%s&amp;destination=%s" target="_blank" rel="noopener">%s</a>'
            % (q(origin), MAPS_DEST, label))


def ul(items):
    return "<ul>" + "".join("<li>%s</li>" % i for i in items) + "</ul>"


def ol(items):
    return "<ol>" + "".join("<li>%s</li>" % i for i in items) + "</ol>"


IGP = {  # Mare Gastro'nun gerçek Instagram paylaşımları (mekân/yemek/mutfak; misafir yüzü öne çıkan paylaşımlar hariç)
    "aksam": "https://www.instagram.com/p/DfoqTx5DDGS/",        # 12 Kasım 2026 · akşam, havuz ışığı, saatler
    "masa": "https://www.instagram.com/p/Dfl6_2tDK79/",         # 11 Kasım 2026 · akşamın akışı üç karede
    "ekip": "https://www.instagram.com/reel/DfkNGsDpF54/",      # 10 Kasım 2026 · Behind Every Plate
    "girit": "https://www.instagram.com/p/DfCgoIjDJ80/",        # 28 Ekim 2026 · Girit ezme, acılı atom
    "kis": "https://www.instagram.com/reel/DeHxECesoyH/",       # 5 Ekim 2026 · kış akşamları
    "mantar": "https://www.instagram.com/reel/Ddy6C7HMYLK/",    # 27 Eylül 2026 · mantar workshop
    "dogumgunu": "https://www.instagram.com/reel/DdOTIecs-1Q/", # 13 Eylül 2026 · doğum günü
    "pirzola": "https://www.instagram.com/reel/DcA_ws-oV5S/",   # 14 Ağustos 2026 · kuzu pirzola
    "risotto": "https://www.instagram.com/reel/Dbc5InUIDId/",   # 31 Temmuz 2026 · buğday risotto
    "incik": "https://www.instagram.com/reel/Da0gjGxIw5J/",     # 15 Temmuz 2026 · kuzu incik keşkek
    "acilis": "https://www.instagram.com/reel/DaN2BnVsJcr/",    # 30 Haziran 2026 · açılış
    "perembe": "https://www.instagram.com/reel/DaP39YFMpk8/",   # 1 Temmuz 2026 · perşembe canlı müzik
    "meze": "https://www.instagram.com/p/DYyYve9jJwe/",         # 26 Mayıs 2026 · meze
    "yakinda": "https://www.instagram.com/p/DYyU9VEDGkd/",      # 26 Mayıs 2026 · "Mare, yakında"
}

REFRESH_TR3 = []

# ─────────────────────────────────────────────────────────────────────────────
# 1) sapanca-en-iyi-dogum-gunu-mekanlari — tek gerçek kazanan (2,3. sıra, %36 CTR).
#    Başlık/H1 KORUNUR; yalnızca cevap-önce giriş, plan bölümü, 2 kişilik bölüm, SSS eklenir.
# ─────────────────────────────────────────────────────────────────────────────
REFRESH_TR3.append({
    "slug": "sapanca-en-iyi-dogum-gunu-mekanlari", "updated": UPDATED, "read": "9 dk",
    # Başlık ve açıklama BİLEREK korunuyor: 2,3. sıra / %36 CTR ile sitenin tek gerçek kazananı.
    "lead": "<strong>Kısa cevap:</strong> Sapanca'da gölün hemen yanında, şık ve sakin bir doğum günü akşamı için Didi Otel bahçesindeki Mare Gastro öne çıkıyor: Şef Doğan Anapa'nın Ege-Akdeniz mutfağı, açık ve kapalı alan, rezervasyonda planlanan pasta ve masa süslemesi. Kalabalık ve hareketli bir gece, çocuklu bir aile sofrası ya da doğa içinde aktivite arıyorsanız aşağıdaki karşılaştırmadaki diğer dört adres daha uygun olabilir.",
    "insert": [
        (4, [("Mare Gastro'da Doğum Günü Nasıl Planlanır? 4 Adım", [
            ol([
                "<strong>Tarihi ve kişi sayısını seçin:</strong> %s üzerinden gün, saat ve kişi sayısını girin; onay WhatsApp'tan gelir. Hafta sonu akşamları için birkaç gün önceden yazmak masanın yerini seçmeyi kolaylaştırır." % L(REZ, "Rezervasyon formu"),
                "<strong>Notu rezervasyonda bırakın:</strong> Doğum günü olduğunu, pasta, mum ya da masa süslemesi istediğinizi ve sürpriz olup olmadığını yazın. Pasta, dijital menünün Ekstralar bölümünde ayrı bir kalem olarak yer alıyor; ayrıntılar ekiple netleşiyor.",
                "<strong>Alanı seçin:</strong> Yazın ve ılık akşamlarda bahçe, serin gecelerde cam cepheli kapalı salon. İkisi de aynı mutfaktan servis alıyor.",
                "<strong>Sofrayı kurgulayın:</strong> Kalabalık masada başlangıçları ortaya söyleyip ana yemeği kişiye bırakmak akşamın akışını rahatlatıyor. Menüyü önceden %s görebilirsiniz." % L(MENU, "dijital menüde"),
            ]),
            fig("mare-k-drone-gece-bahce-1.jpg", "Mare Gastro bahçesi gece, yukarıdan görünüm — Sapanca doğum günü mekanı",
                "Akşam ışıkları yanınca Mare Gastro bahçesi"),
        ]), ("İki Kişilik Doğum Günü İçin Sapanca'da Ne Yapılır?", [
            "İki kişilik bir doğum gününde kalabalık mekanlardan çok konuşmaya izin veren bir masa önemli. Mare Gastro'da ikili masalar hem bahçede hem kapalı salonda kurulabiliyor; mum ve küçük bir pasta sürprizi rezervasyon notuyla hazırlanıyor. Akşamı uzatmak isteyenler aynı bahçedeki %s konaklayabiliyor." % ext(DIDI, "Didi Otel'de"),
            "İkili sofralar için tabak önerilerini %s, sürpriz kurgusunu ise %s anlattık." % (P("sapanca-romantik-es-dogum-gunu-yemegi", "eşe doğum günü yemeği rehberimizde"), P("sapanca-suprizli-dogum-gunu-organizasyonu", "sürprizli doğum günü yazımızda")),
        ])]),
        (99, [("Kutlamanın Türüne Göre Diğer Rehberler", [
            ul([
                P("sapanca-kalabalik-arkadas-grubu-dogum-gunu", "Kalabalık arkadaş grubuyla doğum günü"),
                P("sapanca-30-40-yas-dogum-gunu-kutlamasi", "30 ve 40 yaş doğum günü kutlaması"),
                P("sapanca-bekarliga-veda-yemegi", "Bekarlığa veda yemeği"),
                P("sapanca-mezuniyet-yemegi", "Mezuniyet yemeği"),
                P("sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri", "Doğum günü fiyatları ve menü seçenekleri"),
            ]),
        ])]),
    ],
    "faq_add": [
        ("İki kişilik doğum günü için Sapanca'da nereye gidilir?", "Sakin ve şık bir ikili akşam için Didi Otel bahçesindeki Mare Gastro uygun: bahçede ya da kapalı salonda ikili masa, rezervasyon notuyla hazırlanan mum ve pasta sürprizi, aynı bahçede konaklama imkânı."),
        ("Mare Gastro'da pasta sipariş edilebiliyor mu?", "Evet. Dijital menünün Ekstralar bölümünde pasta ayrı bir kalem olarak yer alıyor; doğum günü olduğunu rezervasyonda belirtirseniz pasta, mum ve masa süslemesi ekiple planlanır."),
    ],
})

# ─────────────────────────────────────────────────────────────────────────────
# 2) sapancaya-nasil-gidilir — 7.052 gösterim / 6 tıklama ("sapanca yol tarifi" 7,6. sıra).
#    DİDİ Otel'in genel seyahat rehberiyle çakışmasın diye "restorana ulaşım"a yeniden konumlandırıldı.
# ─────────────────────────────────────────────────────────────────────────────
REFRESH_TR3.append({
    "slug": "sapancaya-nasil-gidilir", "updated": UPDATED, "read": "6 dk",
    "img": "mare-k-tente-giris.jpg", "alt": "Mare Gastro girişindeki lacivert MARE tentesi — Sapanca, Didi Otel bahçesi",
    "title": "Mare Gastro'ya Nasıl Gidilir? Yol Tarifi, Otopark, Vale",
    "h1": "Mare Gastro'ya Nasıl Gidilir? <em>Yol Tarifi</em>, Otopark ve Vale",
    "desc": "Mare Gastro'ya yol tarifi: Kırkpınar'da Didi Otel bahçesi. Google Haritalar'da tek tıkla rota, ücretsiz otopark ve vale, giriş ve rezervasyon bilgisi.",
    "kw": "mare gastro yol tarifi, mare gastro nerede, mare gastro adres, sapanca yol tarifi, didi otel sapanca yol tarifi, sapanca restoran otopark",
    "lead": "<strong>Kısa cevap:</strong> Mare Gastro, Sapanca'nın Kırkpınar Soğuksu mahallesinde, Didi Otel'in bahçesinde ve Sapanca Gölü'nün hemen yanında (İstasyon 3 Cad. No:55). İstanbul'dan araçla yaklaşık 1,5 saat; Google Haritalar'da \"Mare Gastro\" yazmanız ya da aşağıdaki bağlantılardan birine dokunmanız yeterli. Otopark ücretsiz, vale hizmeti var.",
    "body": [
        ("Mare Gastro Tam Olarak Nerede?", [
            "Restoran, Didi Otel'in bahçesinde yer alıyor; otel ile restoran aynı girişi ve aynı otoparkı paylaşıyor. Açık adres: <strong>%s</strong>. Navigasyonda \"Mare Gastro\" ya da \"Didi Otel Sapanca\" araması aynı noktaya götürür." % ADRES,
            table(["Bilgi", "Ayrıntı"], [
                ["Adres", ADRES],
                ["Konum", "Didi Otel bahçesi, Sapanca Gölü'nün hemen yanında"],
                ["Koordinat", "40.7002, 30.2223"],
                ["Otopark", "Ücretsiz, vale hizmeti var"],
                ["Açık olduğu günler", "Salı–Pazar 09:00–00:00, Pazartesi kapalı"],
                ["Rezervasyon", L(REZ, "Online form") + " (WhatsApp onaylı) · " + ext(WA, "WhatsApp")],
            ]),
            fig("mare-k-tente-giris.jpg", "Mare Gastro girişindeki MARE yazılı lacivert tente", "Girişte sizi lacivert MARE tentesi karşılıyor", portrait=True),
        ]),
        ("Mare Gastro Yol Tarifi: Haritada Tek Tıkla", [
            "Aşağıdaki bağlantılar Google Haritalar'ı bulunduğunuz şehirden Mare Gastro'ya rota çizili şekilde açar. Süre ve güzergâh, o anki trafiğe göre Google tarafından hesaplanır; bu yüzden aşağıdaki tabloda yalnızca yaklaşık değerler veriyoruz.",
            table(["Nereden", "Yaklaşık süre (araçla)", "Yol tarifi"], [
                ["İstanbul Anadolu Yakası", "Yaklaşık 1–1,5 saat", mapdir("Kadıköy, İstanbul", "Rotayı aç")],
                ["İstanbul Avrupa Yakası", "Trafiğe göre 2 saate kadar", mapdir("Taksim, İstanbul", "Rotayı aç")],
                ["İzmit (Kocaeli)", "Yaklaşık 30–40 dakika", mapdir("İzmit, Kocaeli", "Rotayı aç")],
                ["Adapazarı (Sakarya)", "Kısa bir şehir içi sürüş", mapdir("Adapazarı, Sakarya", "Rotayı aç")],
                ["Bursa", "Trafiğe göre değişir", mapdir("Bursa", "Rotayı aç")],
                ["Ankara", "Yaklaşık 4 saat", mapdir("Kızılay, Ankara", "Rotayı aç")],
            ]),
            "Sapanca'ya genel ulaşım seçenekleri (otoyol çıkışları, tren ve otobüs, ilçe içi ulaşım) için kardeş işletmemiz %s ayrıntılı bir rehber hazırladı. Bu sayfa ise doğrudan restorana nasıl ulaşacağınıza odaklanıyor." % ext(DIDI_YOL, "Didi Otel'in Sapanca'ya nasıl gidilir yazısında"),
        ]),
        ("Araçla Gelince Nereye Park Edilir?", [
            "Didi Otel'in otoparkı restoran misafirleri için ücretsiz. Girişte vale hizmeti var; anahtarı bırakıp doğrudan masanıza geçebilirsiniz. Akşam yemeğinde alkol almayı düşünüyorsanız aracı otoparkta bırakıp gece aynı bahçedeki Didi Otel'de kalmak en rahat seçenek.",
            "Vale ve otopark sorularının tamamını %s topladık." % P("sapanca-vale-otopark-restoran", "Sapanca'da vale ve otoparklı restoran yazımızda"),
        ]),
        ("Trenle veya Taksiyle Gelmek Mümkün mü?", [
            "Evet. Sapanca'ya trenle de ulaşılabiliyor; hangi seferlerin Sapanca ya da yakınındaki Arifiye istasyonunda durduğunu ve güncel saatleri TCDD Taşımacılık'tan kontrol etmenizi öneririz. İstasyondan restorana taksiyle geçilir; dönüşte taksi için ekipten yardım isteyebilirsiniz.",
            "Grupla geliyorsanız ve araç sayısını azaltmak istiyorsanız, rezervasyon notuna yazın; otopark ve karşılama buna göre planlanır.",
        ]),
        ("Gelmeden Önce Bilmeniz Gerekenler", [
            ul([
                "<strong>Pazartesi kapalıyız.</strong> Salı'dan Pazar'a 09:00–00:00 arası açığız.",
                "<strong>Hafta sonu rezervasyon yapın.</strong> Cuma ve Cumartesi akşamları, çoğu hafta sonu olan canlı müzik nedeniyle masalar daha hızlı doluyor.",
                "<strong>Özel gün notunu önceden bırakın.</strong> Doğum günü, yıldönümü ya da evlilik teklifi için pasta, mum ve masa süslemesi rezervasyonda planlanır.",
                "<strong>Menüye bakın.</strong> Güncel tabaklar ve fiyatlar %s." % L(MENU, "dijital menüde"),
                "<strong>Sık sorulanlar</strong> için %s bakabilirsiniz." % L(SSS, "SSS sayfamıza"),
            ]),
            "Yol üstünde bir mola ya da akşam yemeğinden önce Kırkpınar'da ne yapılacağını merak ediyorsanız %s okuyabilirsiniz." % P("kirkpinar-restoranlari", "Kırkpınar'da nerede yemek yenir rehberimizi"),
        ]),
    ],
    "faq": [
        ("Mare Gastro'nun adresi nedir?", "Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, 54600 Sapanca/Sakarya. Restoran Didi Otel'in bahçesinde, Sapanca Gölü'nün hemen yanında."),
        ("İstanbul'dan Mare Gastro'ya kaç saatte gidilir?", "Araçla yaklaşık 1,5 saat. Anadolu Yakası'ndan 1–1,5 saat, Avrupa Yakası'ndan trafiğe göre 2 saate kadar sürebilir; anlık süre için Google Haritalar rotasını kullanın."),
        ("Mare Gastro'da otopark var mı?", "Evet. Didi Otel'in otoparkı restoran misafirleri için ücretsiz ve girişte vale hizmeti var."),
        ("Mare Gastro'ya trenle gidilebilir mi?", "Evet, Sapanca'ya trenle ulaşılabiliyor; istasyondan restorana taksiyle geçilir. Sapanca veya Arifiye'de duran seferleri ve güncel saatleri TCDD Taşımacılık'tan kontrol edin."),
        ("Mare Gastro hangi gün kapalı?", "Pazartesi kapalı. Salı'dan Pazar'a 09:00–00:00 arası açık."),
        ("Navigasyona ne yazmalıyım?", "Google Haritalar'da \"Mare Gastro\" ya da \"Didi Otel Sapanca\" araması aynı girişe götürür."),
    ],
    "rel": ["sapanca-vale-otopark-restoran", "kirkpinar-restoranlari", "didi-otel-restoran"],
})

# ─────────────────────────────────────────────────────────────────────────────
# 3) sapanca-fine-dining-fiyat-rehberi — 2.828 gösterim, 3,5. sıra; başlık 73 karakter (kesiliyor).
# ─────────────────────────────────────────────────────────────────────────────
REFRESH_TR3.append({
    "slug": "sapanca-fine-dining-fiyat-rehberi", "updated": UPDATED, "read": "8 dk",
    "title": "Sapanca Fine Dining Fiyatları 2026: Hesabı Ne Belirler?",
    "desc": "Sapanca'da fine dining ne kadar tutar? Hesabı belirleyen 5 kalem, örnek sipariş kurguları ve güncel fiyatları nerede göreceğiniz. Mare Gastro'dan şeffaf rehber.",
    "kw": "sapanca fine dining fiyat, fine dining fiyatları, sapanca restoran fiyatları, mare gastro menü fiyat, mare gastro fiyat, sapanca akşam yemeği fiyat",
    "lead": "<strong>Kısa cevap:</strong> Sapanca'da fine dining bir akşamın tutarı, seçilen tabaklara, içeceklere ve kişi sayısına göre değişir; sabit bir kişi başı rakam yoktur. Mare Gastro'da set menü yerine à la carte sipariş veriliyor ve her tabağın güncel fiyatı %s yazılı; hesabı en çok ana yemek ile içecek seçimi belirliyor." % L(MENU, "dijital menüde"),
    "body": [
        ("Sapanca'da Fine Dining Ne Kadar Tutar?", [
            "Bu soruya tek bir rakamla cevap veren her kaynak, ya eski ya da eksik bilgi verir: fiyatlar mevsimle, malzemeyle ve enflasyonla değişiyor. Doğru cevap, hesabın hangi kalemlerden oluştuğunu bilmek ve güncel fiyatı mekanın kendi menüsünden görmek.",
            "Mare Gastro'da fiyatları bu yazıya bilerek koymuyoruz; menü 10 Kasım 2026'da son kez güncellendi ve tabak tabak fiyatlar her zaman %s. Böylece okuduğunuz rakam ile masada göreceğiniz rakam hiçbir zaman farklı olmaz." % L(MENU, "maregastro.com/menu adresinde güncel"),
        ]),
        ("Hesabı Belirleyen 5 Kalem Nedir?", [
            table(["Kalem", "Hesaba etkisi", "Mare Gastro'da (Kasım 2026)"], [
                ["Ana yemek", "En belirleyici kalem", "11 ana yemek: kaya levreği, bonfile, kuzu pirzola, somon, risotto, incik dahil"],
                ["Başlangıç ve meze", "Paylaşılınca kişi başı düşer", "13 başlangıç, 3 salata; çoğu ortaya söylenebilir"],
                ["Ara sıcak", "Deniz ürünleri hesabı yükseltir", "8 ara sıcak: ıslama kalamar, ahtapot güveç, jumbo karides"],
                ["İçecek", "Şarap ve rakı hesabı ciddi şekilde etkiler", "Şarap, rakı, şampanya ve kokteyl listesi ayrı"],
                ["Tatlı ve ekstralar", "Küçük ama toplamda hissedilir", "5 tatlı; pasta ve çerez Ekstralar'da"],
            ]),
            "Kategori sayıları canlı menüden 16 Kasım 2026'da sayıldı; menü mevsime göre değiştiği için sayılar da zamanla değişebilir.",
        ]),
        ("Bir Akşamın Hesabı Nasıl Kurgulanır?", [
            "Fiyat vermeden de bütçe planlamak mümkün: aşağıdaki üç kurgu, masada en sık gördüğümüz sipariş düzenleri. Güncel fiyatları %s bu kurgulara uygulayarak kendi tahmininizi birkaç dakikada çıkarabilirsiniz." % L(MENU, "dijital menüdeki"),
            table(["Akşam türü", "Tipik sipariş", "Bütçeyi dengeleyen ipucu"], [
                ["İki kişilik akşam", "2 paylaşılan başlangıç + 2 ana yemek + 1 tatlı", "Tatlıyı ortaya söylemek"],
                ["Meze ağırlıklı sofra", "4–5 başlangıç + 1–2 ara sıcak, ana yemek yok", "Ara sıcakta 3'lü Deniz Mahsülü Lezzeti ile çeşitliliği tek tabakta toplamak"],
                ["Kalabalık kutlama", "Ortaya başlangıçlar + kişiye göre ana yemek + pasta", "Başlangıçları masa sayısına göre ortaya söylemek"],
            ]),
            "Paylaşımlı sofranın nasıl kurulacağını %s, meze seçimini %s ayrıntılı anlattık." % (P("sapanca-meze-cesitleri", "Sapanca meze rehberimizde"), P("fine-dining-adabi", "fine dining adabı yazımızda")),
        ]),
        ("Kişi Başı Ücrete Neler Dahildir?", [
            "Fine dining hesabı sipariş ettiğiniz tabaklardan oluşur. Mare Gastro'da buna gölün hemen yanındaki bir masa, bahçe ya da cam cepheli kapalı salon seçeneği, ücretsiz otopark ve vale eşlik ediyor. İçecekler menüden ayrıca seçilir ve ayrıca hesaplanır.",
            "Menüde gramajı yazılı tabaklar karşılaştırmayı kolaylaştırır. Örneğin Mare Spesiyal Granyöz 200 gr kaya levreği, fırınlanmış baby patates, köz yeşil biber sos, köz domates ve beurre blanc sosla; Biber Kremalı Bonfile 200 gr dana bonfile, karabiber kremalı sos ve kibrit patatesle geliyor.",
            igfig("mare-k-ic-salon-gece-masa-duzeni.jpg", "Mare Gastro kapalı salonunda kurulu fine dining masaları", "Akşam servisi öncesi kurulan masalar", IGP["masa"], portrait=True, label="Instagram'da gör"),
        ]),
        ("Fiyat/Performansı Nasıl Değerlendirmeli?", [
            ul([
                "<strong>Gramaj ve içerik:</strong> Menüde gramajı ve garnitürü yazılı tabaklar, neye ödediğinizi netleştirir.",
                "<strong>Malzeme:</strong> Deniz ürünlerinde tazelik ve kırmızı ette kesim, fiyat farkının asıl nedenidir.",
                "<strong>Ortam ve servis:</strong> Gölün hemen yanında bir masa, sakin bir bahçe ve özenli servis deneyimin parçasıdır.",
                "<strong>Gerçek yorumlar:</strong> Mare Gastro'nun %s (24 Ekim 2026); yorumları %s." % (GPUAN, P("mare-gastro-google-yorumlari", "derlediğimiz yazıda okuyabilirsiniz")),
            ]),
            quote(Q_LOCAL[0], Q_LOCAL[1], "tr"),
        ]),
        ("Güncel Fiyatları Nereden Görebilirim?", [
            "Ürün ürün güncel fiyatlar %s listeleniyor. Kalabalık grup veya özel gün planları için %s ya da %s üzerinden ekiple görüşebilirsiniz. Fine dining'in ne olduğunu ve bir akşamın nasıl aktığını merak ediyorsanız %s yazımız iyi bir başlangıç." % (L(MENU, "dijital menüde"), L(REZ, "rezervasyon formu"), ext(WA, "WhatsApp"), P("sapanca-fine-dining-nedir", "fine dining nedir")),
        ]),
    ],
    "faq": [
        ("Sapanca'da fine dining kişi başı ne kadar?", "Tutar seçilen tabaklara, içeceklere ve kişi sayısına göre değişir; sabit bir kişi başı rakam yoktur. Mare Gastro'da à la carte menü var ve güncel tabak fiyatları maregastro.com/menu adresindeki dijital menüde yer alıyor."),
        ("Mare Gastro'da set menü var mı?", "Hayır. Mare Gastro'da sabit bir set menü yok; başlangıç, ara sıcak, ana yemek ve tatlılar à la carte olarak seçiliyor."),
        ("Mare Gastro'nun güncel fiyatlarını nereden görebilirim?", "Ürün bazında güncel fiyatlar Mare Gastro'nun dijital menüsünde (maregastro.com/menu) listeleniyor; menü en son 10 Kasım 2026'da güncellendi."),
        ("İçecekler fiyata dahil mi?", "Hayır. Şarap, rakı, kokteyl ve diğer içecekler menüden ayrıca seçilir ve ayrıca hesaplanır."),
        ("Fine dining hesabını en çok ne etkiler?", "Ana yemek ve içecek seçimi. Deniz ürünleri ve kırmızı et ağırlıklı tabaklar ile şarap tercihi hesabı en çok etkileyen kalemlerdir; başlangıçları paylaşmak kişi başı tutarı düşürür."),
        ("Mare Gastro'da otopark ücretli mi?", "Hayır. Otopark ücretsiz ve vale hizmeti var."),
    ],
    "rel": ["fine-dining-adabi", "sapanca-fine-dining-nedir", "sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri"],
})

# ─────────────────────────────────────────────────────────────────────────────
# 4) mare-gastro-hikayesi — 3.342 gösterim / 4 tıklama; 240 kelime; kapak şef portresi.
#    Marka aramaları (yorumlar, fotoğraflar, menü) bu sayfaya da düşüyor → marka "hub"ına çevrildi.
# ─────────────────────────────────────────────────────────────────────────────
REFRESH_TR3.append({
    "slug": "mare-gastro-hikayesi", "updated": UPDATED, "read": "7 dk",
    "img": "mare-k-drone-gece-bahce-3.jpg", "alt": "Mare Gastro bahçesi gece, yukarıdan — Didi Otel, Sapanca Gölü'nün hemen yanında",
    "title": "Mare Gastro Sapanca: Hikayemiz, Şefimiz ve Mutfağımız",
    "h1": "Mare Gastro'nun <em>Hikayesi</em>: Sapanca'da Bir Fine Dining Mutfağı",
    "desc": "Mare Gastro, Haziran 2026'da Didi Otel bahçesinde açıldı. Şef Doğan Anapa'nın Ege-Akdeniz mutfağı, menü, fotoğraflar, yorumlar ve rezervasyon tek sayfada.",
    "kw": "mare gastro, mare gastro sapanca, mare gastro hikayesi, mare gastro yorumlar, mare gastro fotoğraflar, mare gastro şef",
    "lead": "<strong>Kısa cevap:</strong> Mare Gastro, Sapanca Gölü'nün hemen yanında, Didi Otel'in bahçesinde 30 Haziran 2026'da kapılarını açan bir fine dining restoranı. Mutfağın başında Yönetici Şef Doğan Anapa var; menü Ege ve Akdeniz mutfağını bölgenin yerel ürünleriyle yorumluyor. Salı'dan Pazar'a 09:00–00:00 arası açık.",
    "body": [
        ("Mare Gastro Nedir, Nerede?", [
            "Mare Gastro, Sapanca'nın Kırkpınar Soğuksu mahallesinde, %s bahçesinde yer alan bir restoran." % ext(DIDI, "Didi Otel'in") + " Konsept, Didi Otel bünyesinde Kadir Çiçek tarafından tasarlandı; amaç gölün hemen yanındaki bu bahçeye, doğanın dokusunu bozmadan bir fine dining mutfağı eklemekti.",
            table(["Bilgi", "Mare Gastro"], [
                ["Açılış", "30 Haziran 2026 (%s)" % ext(IGP["acilis"], "Instagram duyurusu")],
                ["Konum", "Didi Otel bahçesi, Kırkpınar, Sapanca; gölün hemen yanında"],
                ["Mutfak", "Ege ve Akdeniz, yerel ürünle; à la carte"],
                ["Yönetici Şef", P("sef-dogan-anapa-kimdir", "Doğan Anapa")],
                ["Çalışma saatleri", "Salı–Pazar 09:00–00:00, Pazartesi kapalı"],
                ["Oturma", "Açık bahçe ve cam cepheli kapalı salon"],
                ["Google puanı", "%s (24 Ekim 2026)" % GPUAN],
            ]),
        ]),
        ("Neden \"Mare\"?", [
            "Mare, İtalyancada ve Latincede \"deniz\" demek. İsim, mutfağın yönünü anlatıyor: Ege ve Akdeniz'in taze, sade ve malzemeye saygılı anlayışı. Sapanca bir göl kasabası; ama menünün omurgası deniz ürünleri, zeytinyağlılar ve mevsim sebzeleri.",
            "Bu yön ilk günden belliydi. Açılıştan önce, Mayıs 2026'da paylaşılan ilk karelerde zeytinyağlı taze fasulye, pancar carpaccio, közlenmiş patlıcan ve enginar vardı; altında tek bir cümle: \"Mare, yakında.\" (%s)" % ext(IGP["yakinda"], "Instagram"),
        ]),
        ("Mutfağın Arkasında Kim Var?", [
            "Yönetici Şef Doğan Anapa, sinema sektöründeki geçmişinden mutfağa taşıdığı anlatı duygusuyla tanınıyor; her menüyü başı ve sonu olan bir akış gibi kuruyor. Yerel ürünü merkeze alıyor: Karasu kuşkonmazı, Trakya eski kaşarı, Adapazarı'nın ıslama geleneği ve keşkek, menüde kendine yer buluyor.",
            igfig("mare-k-mutfak-sef-ekip.jpg", "Mare Gastro mutfağında Şef Doğan Anapa ve ekip çalışırken", "Behind Every Plate: bir tabağın arkasındaki ekip", IGP["ekip"]),
            "Şefin hikâyesini %s, imza tabakların nasıl hazırlandığını %s anlattık." % (P("sef-dogan-anapa-kimdir", "Şef Doğan Anapa kimdir yazımızda"), P("mare-gastro-imza-tabaklar-nasil-hazirlaniyor", "imza tabaklar yazımızda")),
        ]),
        ("Açılıştan Bugüne: Kısa Bir Zaman Çizelgesi", [
            table(["Tarih", "Ne oldu?"], [
                ["Mayıs 2026", "İlk tabak fotoğrafları ve \"Mare, yakında\" duyurusu"],
                ["30 Haziran 2026", "Mare Gastro Sapanca açıldı"],
                ["Temmuz 2026", "Canlı müzik akşamları başladı (%s); şefin tarif videoları %s yayımlanmaya başladı" % (ext(IGP["perembe"], "duyuru"), ext(YT, "YouTube'da"))],
                ["Eylül 2026", "Mikolog Jilber Barutçiyan ile doğa ve mantar workshop'u (%s)" % ext(IGP["mantar"], "Instagram")],
                ["Ekim 2026", "Google Haritalar puanı 4,9 (24 Ekim)"],
                ["Kasım 2026", "Menü güncellendi: 13 başlangıç, 8 ara sıcak, 11 ana yemek, 5 tatlı (10 Kasım)"],
            ]),
        ]),
        ("Fine Dining ama Gösterişsiz: Mutfak Felsefesi", [
            "Mare Gastro'nun anlayışı ağır, seremonili bir fine dining'den çok malzemenin kalitesini öne çıkaran sade bir sunuma dayanıyor. Tabakta az ama doğru malzeme, dengeli bir sos ve mevsime uygun bir garnitür; gerisini bahçenin sakinliği tamamlıyor.",
            "Bu yüzden kıyafet kuralı yok, menü à la carte ve sofra paylaşılabilir. Mezeler ortaya söylenir, ana yemek kişiye göre seçilir. %s ve %s bu yaklaşımı ayrıntılı anlatıyor." % (P("ege-akdeniz-mutfagi-nedir", "Ege ve Akdeniz mutfağı yazımız"), P("fine-dining-adabi", "fine dining adabı rehberimiz")),
            video("Asn8FZ0nFX0", "Şef Doğan Anapa kuzu incik ve keşkeği anlatıyor", "tr"),
        ]),
        ("Misafirler Mare Gastro'yu Nasıl Anlatıyor?", [
            "Google yorumlarında en sık geçen üç konu atmosfer, servis ve özel gün kutlamaları. Gerçek yorumlardan bir seçkiyi %s topladık." % P("mare-gastro-google-yorumlari", "Mare Gastro Google yorumları yazımızda"),
            quote(Q_ANNIV2[0], Q_ANNIV2[1], "tr"),
        ]),
        ("Fotoğraflar, Menü ve Rezervasyon", [
            ul([
                "<strong>Fotoğraflar:</strong> Mekân, bahçe ve tabak fotoğrafları %s; günlük paylaşımlar %s, %s ve %s." % (L(FOTO, "fotoğraf galerimizde"), ext(IG, "Instagram"), ext(TT, "TikTok"), ext(YT, "YouTube")),
                "<strong>Menü:</strong> Güncel tabaklar ve fiyatlar %s." % L(MENU, "dijital menüde"),
                "<strong>Rezervasyon:</strong> %s, onay WhatsApp'tan." % L(REZ, "Üç adımlı online form"),
                "<strong>Ulaşım:</strong> %s." % P("sapancaya-nasil-gidilir", "Mare Gastro'ya nasıl gidilir"),
                "<strong>Sık sorulanlar:</strong> %s." % L(SSS, "SSS sayfası"),
            ]),
        ]),
    ],
    "faq": [
        ("Mare Gastro ne zaman açıldı?", "Mare Gastro Sapanca, 30 Haziran 2026'da açıldı; açılış Instagram hesabından duyuruldu."),
        ("Mare Gastro kimin projesi?", "Mare Gastro, Didi Otel bünyesinde Kadir Çiçek tarafından tasarlanan bir konsept olarak hayata geçirildi; mutfağın başında Yönetici Şef Doğan Anapa var."),
        ("Mare Gastro'nun mutfak anlayışı nedir?", "Ege ve Akdeniz mutfağının sade, malzemeye saygılı anlayışı; deniz ürünleri, zeytinyağlılar ve Karasu kuşkonmazı, Trakya eski kaşarı gibi yerel ürünlerle mevsimsel tabaklar."),
        ("Mare Gastro nerede?", "Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, Sapanca/Sakarya; Didi Otel'in bahçesinde, Sapanca Gölü'nün hemen yanında."),
        ("Mare Gastro'nun fotoğraflarını nerede görebilirim?", "maregastro.com/fotograflar.html adresindeki galeride ve @maregastro Instagram, TikTok ve YouTube hesaplarında."),
        ("Mare Gastro yorumları nasıl?", "24 Ekim 2026 itibarıyla Google Haritalar puanı 4,9. Misafirler en çok atmosferi, servisi ve özel gün kutlamalarını öne çıkarıyor."),
    ],
    "rel": ["sef-dogan-anapa-kimdir", "mare-gastro-imza-tabaklar-nasil-hazirlaniyor", "ege-akdeniz-mutfagi-nedir"],
})

# ─────────────────────────────────────────────────────────────────────────────
# 5) sapancanin-en-iyi-restorani — 1.825 gösterim; "sapanca en iyi restoranlar" 11,6. sıra.
# ─────────────────────────────────────────────────────────────────────────────
REFRESH_TR3.append({
    "slug": "sapancanin-en-iyi-restorani", "updated": UPDATED, "read": "9 dk",
    "title": "Sapanca'nın En İyi Restoranları: 2026 Karşılaştırması",
    "desc": "Sapanca'da en iyi restoran hangisi? Fine dining, yöresel mutfak, canlı müzik ve aile için 5 adresi tabloyla karşılaştırdık; seçmeden önce 6 soru.",
    "kw": "sapanca en iyi restoranlar, sapanca en iyi restoran, sapanca restoranları, sapanca restoran önerileri, sapanca lüks restoranlar, sapanca'da nerede yemek yenir",
    "lead": "<strong>Kısa cevap:</strong> Sapanca'da en iyi restoran, aradığınız deneyime göre değişir. Gölün hemen yanında fine dining için Mare Gastro (Didi Otel bahçesi, Şef Doğan Anapa, %s), dünya mutfağı ve canlı müzik için Sasa Sapanca, yöresel sofra için Menzara, çocuklu aile için Green Blue, doğa ve aktivite için Natürköy öne çıkıyor. Aşağıda beşini aynı kriterlerle karşılaştırdık." % GPUAN,
    "insert": [
        (1, [("5 Restoran Bir Bakışta", [
            table(["Restoran", "Mutfak", "Ortam", "En uygun"], [
                ["Mare Gastro", "Ege-Akdeniz fine dining, à la carte", "Gölün hemen yanı; bahçe ve kapalı salon", "Özel akşam, kutlama, şef mutfağı"],
                ["Sasa Sapanca", "Geniş dünya mutfağı", "Göl kıyısı, canlı müzik", "Kalabalık ve hareketli gece"],
                ["Menzara", "Karadeniz ağırlıklı yöresel", "Göl manzaralı balkon", "Samimi aile sofrası"],
                ["Green Blue", "Deniz ürünleri ağırlıklı", "Geniş bahçe, çocuk oyun alanı", "Çocuklu aileler"],
                ["Natürköy", "Doğa temalı", "Vadi, dere üzerindeki kulübeler", "Gündüz, aktiviteyle birlikte"],
            ]),
            "Karşılaştırmayı Mare Gastro olarak kendi blogumuzda hazırladık; diğer mekanlar için yalnızca doğrulanabilir genel özellikleri yazdık. Çalışma saati, fiyat ve rezervasyon koşullarını her mekandan doğrudan teyit edin.",
        ]), ("Restoran Seçmeden Önce Sormanız Gereken 6 Soru", [
            ol([
                "<strong>Ne kutluyorsunuz?</strong> Doğum günü, yıldönümü ya da sıradan bir akşam; kutlama desteği her mekanda yok.",
                "<strong>Kaç kişisiniz?</strong> İkili masa ile 15 kişilik sofra aynı mekanda aynı rahatlıkta kurulmayabilir.",
                "<strong>Hava kapanırsa ne olacak?</strong> Açık ve kapalı alanı olan mekan planı bozulmaktan korur.",
                "<strong>Alkol servisi var mı?</strong> Rakı-balık ya da şarap eşliğinde bir akşam istiyorsanız önceden sorun.",
                "<strong>Saat kaçta kapanıyor?</strong> İstanbul'dan akşam çıkanlar için geç saat önemli.",
                "<strong>Park nasıl?</strong> Hafta sonu Sapanca'da park yeri, akşamın keyfini doğrudan etkiliyor.",
            ]),
            "Mare Gastro için cevaplar kısaca: kutlama desteği var, ikili masadan kalabalık sofraya kadar plan yapılıyor, açık ve kapalı alan var, alkol servisi var, Salı–Pazar 00:00'a kadar açık, otopark ücretsiz ve vale var.",
        ])]),
        (2, [("Mare Gastro Menüsünde Neler Var?", [
            "10 Kasım 2026 itibarıyla menüde 13 başlangıç, 3 salata, 8 ara sıcak, 11 ana yemek ve 5 tatlı var. Öne çıkanlar: Mare Spesiyal Islama Kalamar (Adapazarı ıslama geleneğinden ilham), Deniz Mahsülleri Buğday Risotto (Trakya eski kaşarıyla), Mare Spesiyal Granyöz (kaya levreği), Kuzu Pirzola ve imza tatlı Ormanda Bir Yürüyüş.",
            igfig("kuzu-pirzola-2026.webp", "Mare Gastro'da kuzu pirzola, patlıcan beğendi ve kıl biberle", "Şef Doğan Anapa'nın sunumuyla Kuzu Pirzola", IGP["pirzola"]),
            "Akşam yemeği planını saat ve bölgeye göre kurmak isterseniz %s, meze ağırlıklı bir sofra için %s, et tabakları için %s okuyabilirsiniz." % (P("sapanca-aksam-yemegi-rehberi", "Sapanca akşam yemeği rehberimizi"), P("sapanca-meze-cesitleri", "meze rehberimizi"), P("sapanca-et-restorani", "et restoranı yazımızı")),
        ])]),
    ],
    "faq": [
        ("Sapanca'nın en iyi restoranı hangisi?", "Aranan deneyime bağlı. Gölün hemen yanında fine dining için Mare Gastro, dünya mutfağı ve canlı müzik için Sasa Sapanca, yöresel lezzet için Menzara, çocuklu aile için Green Blue, doğa ve aktivite için Natürköy öne çıkan adreslerdir."),
        ("Sapanca'da fine dining restoran var mı?", "Evet. Mare Gastro, Didi Otel bahçesinde gölün hemen yanında, Yönetici Şef Doğan Anapa imzasıyla à la carte fine dining sunuyor; Google Haritalar puanı 4,9 (24 Ekim 2026)."),
        ("Sapanca'da göl manzaralı restoranlar hangileri?", "Mare Gastro gölün hemen yanında; Sasa Sapanca göl kıyısında, Menzara göl manzaralı bir balkona sahip. Green Blue ve Natürköy daha çok bahçe ve doğa odaklı."),
        ("Sapanca'da geç saate kadar açık restoran var mı?", "Mare Gastro Salı'dan Pazar'a gece yarısına (00:00) kadar açık; Pazartesi kapalı."),
        ("Sapanca'da restoran seçerken nelere dikkat etmeli?", "Kutlama türü, kişi sayısı, açık/kapalı alan, alkol servisi, kapanış saati ve otopark. Bu altı soru, Sapanca'da doğru restoranı seçmenin en hızlı yolu."),
    ],
    "rel": ["sapanca-aksam-yemegi-rehberi", "sapanca-luks-restoran", "kirkpinar-restoranlari"],
})

# ─────────────────────────────────────────────────────────────────────────────
# 6) sapanca-gece-acik-restoran — 1.785 gösterim / 10 tıklama; 263 kelime.
# ─────────────────────────────────────────────────────────────────────────────
REFRESH_TR3.append({
    "slug": "sapanca-gece-acik-restoran", "updated": UPDATED, "read": "6 dk",
    "img": "mare-k-ic-salon-gece-cam-cephe.jpg", "alt": "Mare Gastro kapalı salonu gece, cam cephe ve havuz ışığı — Sapanca gece açık restoran",
    "title": "Sapanca'da Gece Açık Restoran: 00:00'a Kadar Mare Gastro",
    "h1": "Sapanca'da <em>Gece Açık</em> Restoran: Gece Yarısına Kadar Bir Sofra",
    "desc": "Sapanca'da gece açık restoran mı arıyorsunuz? Mare Gastro Salı–Pazar 00:00'a kadar açık: canlı müzik, kokteyl, şef mutfağı ve ücretsiz otopark.",
    "kw": "sapanca gece açık restoran, sapanca gece mekanları, sapanca geç saate kadar açık restoran, sapanca gece yemek, sapanca akşam mekanları",
    "lead": "<strong>Kısa cevap:</strong> Evet, Sapanca'da gece yarısına kadar açık bir restoran var: Mare Gastro, Didi Otel bahçesinde Salı'dan Pazar'a 09:00–00:00 arası hizmet veriyor, Pazartesi kapalı. Gece servisinde şefin à la carte menüsü, kokteyl ve şarap listesi var; çoğu hafta sonu akşamlara canlı müzik eşlik ediyor.",
    "body": [
        ("Sapanca'da Gece Geç Saatte Açık Restoran Var mı?", [
            "Sapanca'daki restoranların önemli bir kısmı kahvaltı ve gündüz odaklı çalışıyor; akşam ilerledikçe seçenekler azalıyor. Mare Gastro ise sabah 09:00'da kahvaltıyla açılıp gece yarısı kapanan bir düzende çalışıyor. İstanbul'dan iş çıkışı yola düşenler ya da akşamı uzatmak isteyenler için bu, oturup acele etmeden yemek yiyebilmek demek.",
            igfig("mare-k-ic-salon-gece-cam-cephe.jpg", "Mare Gastro salonu gece, cam cepheye vuran havuz ışığı", "\"Akşam uzasın, biz buradayız\": Mare Gastro'da bir gece", IGP["aksam"], portrait=True, label="Instagram'da gör"),
        ]),
        ("Mare Gastro'da Bir Gün Nasıl Akar?", [
            table(["Saat", "Ne var?"], [
                ["09:00", "Kapılar açılır; serpme kahvaltı ve Brioche Benedict"],
                ["Gün içi", "À la carte menü, salatalar, atıştırmalıklar"],
                ["Akşam", "Başlangıçlar, ara sıcaklar, ana yemekler; kokteyl, şarap ve rakı"],
                ["Hafta sonu akşamları", "Çoğu hafta sonu canlı müzik"],
                ["00:00", "Kapanış (Salı–Pazar); Pazartesi kapalı"],
            ]),
            "Geç bir saatte gelecekseniz mutfağın son sipariş saatini rezervasyon notunda sormanızı öneririz; ekip planlamayı buna göre yapar.",
        ]),
        ("Geç Saatte Neler Yenir, Neler İçilir?", [
            "Gece sofrasında en sık görülen düzen, birkaç paylaşılan başlangıç ve bir ara sıcakla açılıp bir ana yemekle devam etmek. Islama kalamar, ahtapot güveç ve jumbo karides gibi ara sıcaklar gece masasına iyi gidiyor; ağır bir akşam yemeği istemeyenler için Humus, Girit Ezme ya da Pancar Borani gibi başlangıçlar yeterli olabilir.",
            "İçki tarafında rakı, şarap, şampanya ve imza kokteyller var; ayrıntılı liste %s. Rakı eşliğinde uzun bir gece planlıyorsanız %s okuyabilirsiniz." % (P("sapanca-alkollu-restoran", "alkollü restoran yazımızda"), P("sapanca-raki-balik", "rakı-balık rehberimizi")),
        ]),
        ("Gece Mekanı mı, Restoran mı?", [
            "\"Sapanca gece mekanları\" araması genellikle iki farklı isteği kapsıyor: geç saate kadar oturulabilen bir restoran ya da müzikli bir eğlence mekanı. Mare Gastro birincisi: gece kulübü değil, canlı müzik eşliğinde yemek yenen bir restoran. Müzik, sohbeti bastırmayacak seviyede tutuluyor.",
            "Hafta sonu canlı müzik programını %s takip edebilirsiniz; geçmiş sahnelerden biri aşağıda." % P("sapanca-canli-muzik-mekanlari", "canlı müzik yazımızdan"),
            video("GiwkPYUSVyY", "Mare Gastro sahnesinde canlı müzik akşamı", "tr"),
        ]),
        ("Gece Yemeğinden Sonra Nerede Kalınır?", [
            "Gece yarısı İstanbul'a dönmek yerine aynı bahçedeki %s konaklamak en pratik seçenek; aracınız ücretsiz otoparkta kalır. Konaklama tercihinizi rezervasyonda belirtebilirsiniz." % ext(DIDI, "Didi Otel'de"),
        ]),
        ("Gece İçin Rezervasyon Yapmalı mıyım?", [
            "Hafta içi akşamlarında genellikle yer bulunuyor; Cuma ve Cumartesi geceleri, canlı müzik olan akşamlarda masalar daha hızlı doluyor. %s tarih ve saati seçip geliş saatinizi not olarak yazmanız yeterli." % L(REZ, "Rezervasyon formundan"),
        ]),
    ],
    "faq": [
        ("Sapanca'da gece açık restoran var mı?", "Evet. Mare Gastro, Didi Otel bahçesinde Salı'dan Pazar'a gece yarısına (00:00) kadar açık; Pazartesi kapalı."),
        ("Mare Gastro hangi saatlerde açık?", "Salı–Pazar 09:00–00:00. Sabah kahvaltıyla açılır, gece yarısı kapanır; Pazartesi kapalıdır."),
        ("Geç saatte mutfak açık mı?", "Mutfak akşam boyunca à la carte servis veriyor. Geç bir saatte gelecekseniz son sipariş saatini rezervasyonda sormanız önerilir."),
        ("Mare Gastro gece kulübü mü?", "Hayır. Mare Gastro bir restoran; çoğu hafta sonu canlı müzik eşliğinde akşam yemeği sunuyor, müzik sohbeti bastırmayacak seviyede."),
        ("Gece için rezervasyon gerekir mi?", "Cuma ve Cumartesi geceleri ile canlı müzik olan akşamlarda önceden rezervasyon önerilir."),
    ],
    "rel": ["sapanca-alkollu-restoran", "sapanca-canli-muzik-mekanlari", "sapanca-aksam-yemegi-rehberi"],
})

# ─────────────────────────────────────────────────────────────────────────────
# 7) sapanca-luks-restoran — 1.498 gösterim, 3,3. sıra; "mare gastro fotoğraflar" sorguları da düşüyor.
# ─────────────────────────────────────────────────────────────────────────────
REFRESH_TR3.append({
    "slug": "sapanca-luks-restoran", "updated": UPDATED, "read": "7 dk",
    "videos": ["aOAyrgTBcos"],
    "title": "Sapanca Lüks Restoran: Gölün Hemen Yanında Fine Dining",
    "desc": "Sapanca'da lüks restoran: Didi Otel bahçesinde Mare Gastro. Şef Doğan Anapa'nın Ege-Akdeniz mutfağı, Google'da 4,9, ücretsiz otopark, vale ve fotoğraflar.",
    "lead": "<strong>Kısa cevap:</strong> Sapanca'da lüks bir akşam yemeği için Mare Gastro, Didi Otel'in bahçesinde gölün hemen yanında fine dining sunuyor: Yönetici Şef Doğan Anapa imzalı Ege ve Akdeniz mutfağı, açık bahçe ve cam cepheli kapalı salon, ücretsiz otopark ve vale. Salı'dan Pazar'a 09:00–00:00 arası açık; Google Haritalar puanı 4,9 (24 Ekim 2026).",
    "body": [
        ("Sapanca'da Lüks Restoranı Ne Belirler?", [
            "\"Lüks\" kelimesi çoğu zaman yalnızca dekor ya da fiyatla eşleştiriliyor. Oysa misafirin akşamı hatırlamasını sağlayan şeyler daha somut: mutfağın imzası, servisin dikkati, masanın konumu ve küçük ayrıntıların önceden düşünülmüş olması.",
            table(["Ölçüt", "Neden önemli?", "Mare Gastro'da"], [
                ["Şef mutfağı", "Menü bir imza taşır, tabaklar tutarlıdır", "Yönetici Şef Doğan Anapa; Ege-Akdeniz, yerel ürün"],
                ["Konum ve manzara", "Akşamın sahnesi", "Didi Otel bahçesi, gölün hemen yanı"],
                ["Mekân", "Her havada aynı kalite", "Açık bahçe + cam cepheli kapalı salon"],
                ["Servis", "Özel günler önceden planlanır", "Pasta, mum, masa süslemesi rezervasyonda"],
                ["Erişim", "Park ve ulaşım akşamı bozmasın", "Ücretsiz otopark, vale; İstanbul'a ~1,5 saat"],
                ["İçki listesi", "Yemekle uyum", "Şarap, şampanya, rakı ve imza kokteyller"],
            ]),
        ]),
        ("Gölün Hemen Yanında Bir Bahçe, Cam Cepheli Bir Salon", [
            "Mare Gastro, Didi Otel'in palmiyeler ve çamlarla çevrili bahçesinde. Yaz akşamları bahçede, serin günlerde ise havuzun ışığının cama vurduğu kapalı salonda oturuluyor. Akşamın ışığı ve sakinliği, burayı Sapanca'nın kalabalık sahil şeridinden ayıran şey.",
            fig("mare-k-ic-salon-gece-avize-palmiye.jpg", "Mare Gastro iç salonu gece, sıcak ışık ve palmiyeler", "Kapalı salonda bir akşam", portrait=True),
            "Mekânın tüm fotoğraflarını %s görebilirsiniz; günlük paylaşımlar %s ve %s hesaplarımızda." % (L(FOTO, "fotoğraf galerimizde"), ext(IG, "Instagram"), ext(TT, "TikTok")),
        ]),
        ("Mutfakta Neler Var?", [
            "Menü à la carte ve mevsime göre değişiyor. 10 Kasım 2026 itibarıyla 13 başlangıç, 3 salata, 8 ara sıcak, 11 ana yemek ve 5 tatlı var. Lüks bir akşam için sık tercih edilenler:",
            ul([
                "<strong>Kereviz Püreli Jumbo Karides Söğüş</strong> — portakallı kereviz püresi, yeşil elma",
                "<strong>Palamut Carpaccio</strong> — sarımsaklı vinaigrette, kapari, dereotu",
                "<strong>Mare Spesiyal Granyöz</strong> — 200 gr kaya levreği, köz yeşil biber sos, beurre blanc",
                "<strong>Biber Kremalı Bonfile</strong> — 200 gr dana bonfile, karabiber kremalı sos",
                "<strong>Ormanda Bir Yürüyüş</strong> — çikolata mus, çıtır profiterol, vanilyalı dondurma",
            ]),
            "Tüm tabaklar ve güncel fiyatlar %s." % L(MENU, "dijital menüde"),
            video("aOAyrgTBcos", "Sapanca'da saklı bir fine dining akşamı", "tr"),
        ]),
        ("Konseptin Arkasında Kim Var?", [
            "Mare Gastro'nun ışığından masa düzenine kadar konsepti Didi Otel bünyesinde Kadir Çiçek tarafından tasarlandı. Mutfakta ise sinema geçmişini tabağa taşıyan Yönetici Şef Doğan Anapa var. Hikâyenin tamamı %s." % P("mare-gastro-hikayesi", "Mare Gastro'nun hikayesi yazımızda"),
        ]),
        ("Lüks Bir Akşam İçin Pratik İpuçları", [
            ul([
                "Hafta sonu akşamları için birkaç gün önceden %s." % L(REZ, "rezervasyon yapın"),
                "Özel gün varsa (doğum günü, yıldönümü, teklif) notunu rezervasyonda bırakın.",
                "Kıyafet kuralı yok; rahat-şık bir tercih akşama yakışır. Ayrıntılar %s." % P("fine-dining-adabi", "fine dining adabı yazımızda"),
                "Gece İstanbul'a dönmek istemiyorsanız aynı bahçedeki %s." % ext(DIDI, "Didi Otel'de kalabilirsiniz"),
            ]),
        ]),
    ],
    "faq": [
        ("Sapanca'da lüks restoran nerede?", "Mare Gastro, Sapanca'nın Kırkpınar bölgesinde, Didi Otel bahçesinde ve Sapanca Gölü'nün hemen yanında yer alan bir fine dining restoranı."),
        ("Mare Gastro hangi günler açık?", "Salı'dan Pazar'a 09:00–00:00 arası açık; Pazartesi kapalı."),
        ("Mare Gastro'da kıyafet kuralı var mı?", "Hayır, katı bir kıyafet kuralı yok. Rahat-şık bir tercih özel günlerde akşamı tamamlar."),
        ("Mare Gastro'nun fotoğraflarını nerede görebilirim?", "Web sitesindeki fotoğraf galerisinde (maregastro.com/fotograflar.html) ve @maregastro Instagram, TikTok, YouTube hesaplarında."),
        ("Mare Gastro'da rezervasyon nasıl yapılır?", "Web sitesindeki üç adımlı formdan tarih, saat ve kişi sayısını seçerek; onay WhatsApp üzerinden gelir."),
        ("Mare Gastro İstanbul'a uzak mı?", "Sapanca, İstanbul'a araçla yaklaşık 1,5 saat mesafede."),
    ],
    "rel": ["istanbula-yakin-luks-restoran", "sapanca-fine-dining-fiyat-rehberi", "fine-dining-adabi"],
})

# ─────────────────────────────────────────────────────────────────────────────
# 8) sapanca-yildonumu-icin-en-iyi-mekan — 34 tıklama, GA4'te 2. sırada. Yapı korunur, eklenir.
# ─────────────────────────────────────────────────────────────────────────────
REFRESH_TR3.append({
    "slug": "sapanca-yildonumu-icin-en-iyi-mekan", "updated": UPDATED, "read": "9 dk",
    "desc": "Sapanca'da evlilik yıldönümü nerede kutlanır? 5 mekanı manzara, atmosfer ve sürpriz desteğine göre karşılaştırdık; gerçek yorumlar ve akşam planı.",
    "lead": "<strong>Kısa cevap:</strong> Sapanca'da evlilik yıldönümü için gölün hemen yanında, mum ışığında bir akşam arıyorsanız Didi Otel bahçesindeki Mare Gastro öne çıkıyor: Şef Doğan Anapa'nın Ege-Akdeniz mutfağı, rezervasyonda planlanan pasta, çiçek ve masa süslemesi, aynı bahçede konaklama. Canlı müzikli bir gece için Sasa Sapanca, samimi bir sofra için Menzara, doğa içinde sakinlik için Natürköy de değerlendirilebilir.",
    "insert": [
        (4, [("Yıldönümü Akşamı Saat Saat: Örnek Bir Plan", [
            table(["Saat", "Plan"], [
                ["Öğleden sonra", "Sapanca'ya varış; aracı ücretsiz otoparka bırakın, isterseniz Didi Otel'e giriş yapın"],
                ["Gün batımına doğru", "Bahçede bir kadeh; yaz aylarında akşam ışığı en güzel bu saatlerde"],
                ["Akşam yemeği", "Paylaşılan iki başlangıç, iki ana yemek; rezervasyonda istenen pasta ya da çiçek bu bölümde masaya gelir"],
                ["Gece", "Hafta sonuysa canlı müzik; akşamı acele etmeden gece yarısına kadar uzatmak mümkün"],
            ]),
            "İkili sofralar için tabak önerisi: Kereviz Püreli Jumbo Karides Söğüş ya da Palamut Carpaccio ile açılıp Mare Spesiyal Granyöz veya Biber Kremalı Bonfile ile devam etmek, tatlıda Çerkes Peynirli Cheesecake'i paylaşmak.",
            igfig("mare-k-ic-salon-gece-masa-duzeni.jpg", "Mare Gastro'da akşam için kurulmuş ikili masalar", "Akşamın akışı: sizi bekleyen masa", IGP["masa"], portrait=True, label="Instagram'da gör"),
        ])]),
        (99, [("Yıldönümüne Yakın Diğer Rehberler", [
            ul([
                P("sapanca-yildonumu-yemegi", "Sapanca'da yıldönümü yemeği: menü ve hazırlık"),
                P("sapanca-esinizle-ozel-aksam", "Eşinizle özel bir akşam"),
                P("sapanca-sevgiliyle-yemek-ve-konaklama", "Akşam yemeği ve konaklama bir arada"),
                P("sapanca-evlilik-teklifi", "Sapanca'da evlilik teklifi"),
            ]),
        ])]),
    ],
    "faq_add": [
        ("Yıldönümü için Mare Gastro'da en sakin masa nerede?", "Rezervasyonda yıldönümü olduğunu ve sakin bir köşe istediğinizi belirtin; ekip mevsime göre bahçede ya da kapalı salonda uygun masayı ayırır."),
    ],
})

# ─────────────────────────────────────────────────────────────────────────────
# 9) didi-otel-restoran — 1.081 gösterim; 199 kelime; "göl kıyısının" ifadesi; garip SSS cümlesi.
# ─────────────────────────────────────────────────────────────────────────────
REFRESH_TR3.append({
    "slug": "didi-otel-restoran", "updated": UPDATED, "read": "6 dk",
    "title": "Didi Otel Restoranı: Mare Gastro | Sapanca Fine Dining",
    "h1": "<em>Didi Otel</em> Restoranı: Bahçedeki Fine Dining, Mare Gastro",
    "desc": "Didi Otel'in restoranı Mare Gastro: otelin bahçesinde, gölün hemen yanında fine dining. Otelde kalın ya da kalmayın; saatler, menü ve rezervasyon.",
    "kw": "didi otel restoran, didi otel sapanca restoran, didi otel mare gastro, sapanca otel restoranı, didi restaurant",
    "lead": "<strong>Kısa cevap:</strong> Didi Otel'in restoranı Mare Gastro; otelin Sapanca'daki bahçesinde, gölün hemen yanında yer alıyor. Restoran yalnızca otel misafirlerine değil herkese açık: Salı'dan Pazar'a 09:00–00:00 arası kahvaltı, öğle ve akşam yemeği, Şef Doğan Anapa'nın à la carte Ege-Akdeniz menüsüyle.",
    "body": [
        ("Didi Otel ile Mare Gastro'nun İlişkisi Ne?", [
            "Mare Gastro, Didi Otel bünyesinde açılan ve otelin bahçesinde hizmet veren restoran. Konsepti Didi Otel bünyesinde Kadir Çiçek tasarladı, mutfağı Yönetici Şef Doğan Anapa yönetiyor. Otel ile restoran aynı girişi, aynı otoparkı ve aynı bahçeyi paylaşıyor; ama Mare Gastro'nun kendi menüsü, kendi rezervasyon sistemi ve kendi ekibi var.",
            "Otelin odaları ve konaklama bilgisi için %s; restoranın menüsü ve rezervasyonu için bu site." % ext(DIDI, "sapancadidiotel.com"),
        ]),
        ("Otel Misafiri Olmadan Gelinebilir mi?", [
            table(["", "Didi Otel misafiri", "Dışarıdan gelen misafir"], [
                ["Restorana giriş", "Evet", "Evet"],
                ["Rezervasyon", "Önerilir (özellikle hafta sonu)", "Önerilir (özellikle hafta sonu)"],
                ["Otopark", "Ücretsiz", "Ücretsiz, vale hizmeti var"],
                ["Menü", "Aynı à la carte menü", "Aynı à la carte menü"],
                ["Özel gün hazırlığı", "Rezervasyonda planlanır", "Rezervasyonda planlanır"],
            ]),
            "Kısacası Mare Gastro bir \"otel restoranı\" gibi yalnızca konuklara değil, Sapanca'ya akşam yemeği için gelen herkese hizmet veriyor.",
        ]),
        ("Bahçede Bir Akşam: Konum ve Atmosfer", [
            "Palmiyeler ve çamlarla çevrili bahçe, havuzun çevresinde açık hava masaları ve cam cepheli bir kapalı salondan oluşuyor. Yazın bahçe, serin akşamlarda salon tercih ediliyor; ikisi de aynı mutfaktan servis alıyor.",
            fig("mare-k-didi-otel-havuz-cephe.jpg", "Didi Otel cephesi ve havuz, Sapanca", "Didi Otel ve havuz; Mare Gastro aynı bahçede", ),
        ]),
        ("Menüde Neler Var?", [
            "10 Kasım 2026 itibarıyla menü 13 başlangıç, 3 salata, 8 ara sıcak, 11 ana yemek ve 5 tatlıdan oluşuyor; sabahları serpme kahvaltı ve Brioche Benedict var. Çocuklar için Izgara Köfte, gün içinde hamburger, tost ve patates tava gibi atıştırmalıklar da bulunuyor.",
            igfig("girit-ezme-pancar-portakal-2026.webp", "Mare Gastro'da portakal çektirmeli ve pancar dilimli Girit ezme", "Girit Ezme, Pancar, Portakal: geleneksel bir mezenin Mare yorumu", IGP["girit"], label="Instagram'da gör"),
            "Güncel tabaklar ve fiyatlar %s. Kahvaltı ayrıntıları için %s bakabilirsiniz." % (L(MENU, "dijital menüde"), P("sapanca-gol-manzarali-kahvalti", "kahvaltı yazımıza")),
        ]),
        ("Konaklama ve Akşam Yemeğini Birlikte Planlamak", [
            "Akşam yemeğinden sonra İstanbul'a dönmek yerine gecelemek isteyenler için en kolay yol, aynı bahçedeki Didi Otel. Doğum günü, yıldönümü ya da evlilik teklifi gibi özel akşamlarda yemek ve konaklamayı birlikte planlamak, ulaşım derdini ortadan kaldırıyor. Bunu %s ayrıntılı anlattık." % P("sapanca-sevgiliyle-yemek-ve-konaklama", "akşam yemeği ve konaklama yazımızda"),
            "Çocuklu aileler için restoran tarafındaki seçenekleri %s topladık." % P("sapanca-cocuklu-aile-restorani", "çocuklu aile restoranı rehberimizde"),
        ]),
    ],
    "faq": [
        ("Didi Otel'in restoranı hangisi?", "Didi Otel'in bahçesindeki restoran Mare Gastro. Gölün hemen yanında, Şef Doğan Anapa'nın Ege ve Akdeniz mutfağını à la carte sunuyor."),
        ("Mare Gastro Didi Otel'in neresinde?", "Otelin bahçesinde; otel ile aynı girişi ve otoparkı paylaşıyor. Adres: Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, Sapanca/Sakarya."),
        ("Otelde kalmadan Mare Gastro'da yemek yenebilir mi?", "Evet. Mare Gastro herkese açık; otel misafiri olmadan da rezervasyon yapıp gelebilirsiniz. Otopark ücretsiz."),
        ("Mare Gastro hangi günler açık?", "Salı'dan Pazar'a 09:00–00:00 arası açık; Pazartesi kapalı."),
        ("Didi Otel'de kahvaltı Mare Gastro'da mı yapılıyor?", "Mare Gastro'nun kahvaltı menüsü (serpme kahvaltı ve Brioche Benedict) Salı–Pazar 09:00'dan itibaren herkese açık. Otel konaklamasına dahil kahvaltı koşulları için Didi Otel'e danışın."),
    ],
    "rel": ["sapanca-sevgiliyle-yemek-ve-konaklama", "sapanca-luks-restoran", "sapanca-cocuklu-aile-restorani"],
})

# ─────────────────────────────────────────────────────────────────────────────
# 10) sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri — 803 gösterim / 15 tıklama.
#     Eski bilgi: çocuk menüsünde "Domates Soslu Makarna" artık yok; ana yemek sayısı değişti.
# ─────────────────────────────────────────────────────────────────────────────
REFRESH_TR3.append({
    "slug": "sapanca-dogum-gunu-fiyatlari-ve-menu-secenekleri", "updated": UPDATED, "read": "8 dk",
    "title": "Sapanca Doğum Günü Fiyatları ve Menü Seçenekleri (2026)",
    "desc": "Sapanca'da doğum günü kutlaması ne kadar tutar? Hesabı belirleyen kalemler, kalabalık sofra kurguları, pasta ve süsleme süreci; güncel fiyatlar dijital menüde.",
    "lead": "<strong>Kısa cevap:</strong> Sapanca'da doğum günü kutlamasının tutarı kişi sayısına, seçilen tabaklara, içeceklere ve pasta/süsleme talebine göre değişir; sabit bir paket fiyatı yoktur. Mare Gastro'da à la carte menüden sipariş veriliyor, tabak tabak güncel fiyatlar %s ve pasta Ekstralar bölümünde ayrı bir kalem olarak yer alıyor." % L(MENU, "dijital menüde"),
    "body": [
        ("Sapanca'da Doğum Günü Kutlaması Ne Kadar Tutar?", [
            "Tek bir rakam vermek yanıltıcı olur: aynı masada iki kişi meze ağırlıklı bir akşam geçirirken başka bir masada on kişi ana yemek, şarap ve pasta ile kutlama yapabiliyor. Bu yüzden fiyatı yazıya değil, her zaman güncel olan %s bırakıyoruz. Aşağıdaki tablolar, bütçeyi nasıl planlayacağınızı gösteriyor." % L(MENU, "dijital menüye"),
        ]),
        ("Doğum Günü Sofrası İçin Menü Seçenekleri", [
            table(["Bölüm", "Kutlamaya uygun örnekler (Kasım 2026)"], [
                ["Paylaşımlık başlangıçlar", "Pancar Borani, Havuç Tarator, Patates Cipsli Acılı Atom, Humus, Girit Ezme, Peynir Tabağı"],
                ["Ara sıcaklar", "3'lü Deniz Mahsülü Lezzeti, Mare Spesiyal Islama Kalamar, Kalamar Tava, Tereyağlı Karides"],
                ["Ana yemekler", "Mare Spesiyal Granyöz, Biber Kremalı Bonfile, Kuzu Pirzola, Çıtır Somon, Deniz Mahsülleri Buğday Risotto"],
                ["Tatlılar", "Ormanda Bir Yürüyüş, Çerkes Peynirli Cheesecake, Çıtır Kabak Tatlısı, Mare Şekerpare"],
                ["Çocuklar için", "Izgara Köfte (çocuk menüsü); atıştırmalıklarda hamburger, tost, patates tava"],
                ["Ekstralar", "Pasta, çerez, süzme yoğurt"],
            ]),
            "Menü 10 Kasım 2026'da güncellendi; mevsime göre değişebilir.",
        ]),
        ("Kalabalık Sofrada Bütçe Nasıl Kurgulanır?", [
            table(["Kutlama", "Sık görülen kurgu", "Bütçeyi dengeleyen ipucu"], [
                ["2 kişi", "2 başlangıç + 2 ana yemek + pasta ya da tatlı", "Başlangıçları paylaşmak"],
                ["4–6 kişi", "Ortaya 4–5 başlangıç + 1 ara sıcak + kişiye göre ana yemek", "Ara sıcakta 3'lü Deniz Mahsülü Lezzeti"],
                ["8 kişi ve üzeri", "Ortaya başlangıç ve ara sıcak; ana yemek kişiye göre; pasta", "Kişi sayısını ve menü tercihini önceden bildirmek"],
            ]),
            "Kalabalık gruplar için ayrıntılı plan %s." % P("sapanca-kalabalik-arkadas-grubu-dogum-gunu", "arkadaş grubuyla doğum günü yazımızda"),
        ]),
        ("Fiyatı Neler Belirler?", [
            ul([
                "<strong>Kişi sayısı:</strong> Toplam tutarı en çok etkileyen unsur.",
                "<strong>Tabak seçimi:</strong> Deniz ürünleri ve kırmızı et ağırlıklı ana yemekler hesabı yükseltir.",
                "<strong>İçecekler:</strong> Şarap, rakı ve kokteyller ayrıca hesaplanır.",
                "<strong>Pasta ve süsleme:</strong> Pasta Ekstralar'da ayrı kalem; süsleme talebi rezervasyonda netleşir.",
                "<strong>Mevsim:</strong> Menü mevsime göre güncellenir.",
            ]),
        ]),
        ("Pasta ve Süsleme Nasıl Planlanıyor?", [
            "Rezervasyon sırasında kişi sayısını, tarihi ve pasta, mum ya da masa süslemesi talebinizi iletirsiniz; detaylar ekiple birlikte netleştirilir. Sürpriz olacaksa bunu da notta belirtin: pasta, doğum günü sahibinin haberi olmadan doğru zamanda masaya gelir.",
            quote(Q_BDAY[0], Q_BDAY[1], "tr"),
            "Doğum günü akşamları çoğu hafta sonu canlı müzikle de renkleniyor; sahneden bir kesit aşağıda.",
            video("GiwkPYUSVyY", "Mare Gastro'da canlı müzik akşamı", "tr"),
        ]),
        ("Güncel Fiyat Bilgisini Nereden Öğrenebilirim?", [
            "Ürün ürün güncel fiyatlar %s. Kişi sayısı ve özel taleplerle birlikte plan yapmak için %s ya da %s üzerinden ekiple görüşebilirsiniz." % (L(MENU, "dijital menüde listeleniyor"), L(REZ, "rezervasyon formu"), ext(WA, "WhatsApp")),
            "Mekan karşılaştırması için %s; bekarlığa veda ve mezuniyet gibi diğer kutlamalar için %s ve %s yazılarımıza bakabilirsiniz." % (P("sapanca-en-iyi-dogum-gunu-mekanlari", "Sapanca'da doğum günü için en iyi 5 mekan"), P("sapanca-bekarliga-veda-yemegi", "bekarlığa veda"), P("sapanca-mezuniyet-yemegi", "mezuniyet yemeği")),
        ]),
    ],
    "faq": [
        ("Sapanca'da doğum günü kutlaması ne kadar tutar?", "Kişi sayısına, seçilen tabaklara, içeceklere ve pasta talebine göre değişir. Mare Gastro'da à la carte menü var; güncel tabak fiyatları maregastro.com/menu adresindeki dijital menüde yer alıyor."),
        ("Mare Gastro'da doğum günü paketi var mı?", "Hayır. Sabit bir paket yerine à la carte menüden seçim yapılıyor; pasta ve süsleme talepleri rezervasyon sırasında planlanıyor."),
        ("Mare Gastro'da pasta sipariş edilebilir mi?", "Evet. Pasta, dijital menünün Ekstralar bölümünde ayrı bir kalem olarak yer alıyor; doğum günü olduğunu rezervasyonda belirtmeniz yeterli."),
        ("İçecekler fiyata dahil mi?", "Hayır. İçecekler menüden ayrıca seçilir ve ayrıca hesaplanır."),
        ("Çocuklar için menü var mı?", "Evet. Çocuk menüsünde Izgara Köfte var (Kasım 2026); ayrıca hamburger, tost ve patates tava gibi atıştırmalıklar bulunuyor."),
        ("Güncel fiyat bilgisini nasıl öğrenebilirim?", "Dijital menüden ürün bazında fiyatları görebilir, kalabalık grup planları için rezervasyon formu veya WhatsApp üzerinden ekiple görüşebilirsiniz."),
    ],
    "rel": ["sapanca-en-iyi-dogum-gunu-mekanlari", "sapanca-kalabalik-arkadas-grubu-dogum-gunu", "sapanca-bekarliga-veda-yemegi"],
})





# ─────────────────────────────────────────────────────────────────────────────
# Ek bölümler: ince kalan yenilenmiş yazılar (gövde sonuna, SSS'den önce)
# ─────────────────────────────────────────────────────────────────────────────
_MORE = {
    "sapanca-gece-acik-restoran": [
        ("İstanbul'dan Akşam Çıkıp Gece Yemeğine: Örnek Plan", [
            table(["Saat", "Plan"], [
                ["18:30", "İstanbul Anadolu Yakası'ndan çıkış (trafiğe göre değişir)"],
                ["20:00", "Sapanca'ya varış; aracı ücretsiz otoparka bırakın, vale var"],
                ["20:15", "Başlangıçlar ve bir kokteyl"],
                ["21:00", "Ana yemek; hafta sonuysa canlı müzik"],
                ["22:30", "Tatlı, kahve; isteyen için gece aynı bahçedeki Didi Otel"],
            ]),
            "Hafta içi akşamları trafik genellikle daha akıcı; hafta sonu ise Cuma akşamı çıkışlarında yol süresi uzayabiliyor. Anlık süre için %s rotasını kullanın." % P("sapancaya-nasil-gidilir", "Mare Gastro yol tarifi sayfasındaki"),
        ]),
        ("Gece Yemeği İçin 4 Öneri", [
            ol([
                "<strong>Rezervasyonda geliş saatinizi yazın.</strong> Masa ve mutfak buna göre hazırlanır.",
                "<strong>Paylaşımlı başlangıçlarla açın.</strong> Geç saatte ağır bir ana yemek yerine birkaç meze ve bir ara sıcak da yeterli olabilir.",
                "<strong>Dönüşü baştan düşünün.</strong> Alkol alınacaksa şoför ya da konaklama planlayın.",
                "<strong>Yanınıza bir ceket alın.</strong> Bahçede oturacaksanız göl çevresinde geceler serinliyor.",
            ]),
        ]),
    ],
    "sapanca-luks-restoran": [
        ("Lüks Bir Akşam İçin Örnek Menü Akışı", [
            table(["Aşama", "Öneri (Kasım 2026 menüsü)"], [
                ["Karşılama", "Bahçede bir kadeh şampanya ya da imza kokteyl"],
                ["Başlangıç", "Kereviz Püreli Jumbo Karides Söğüş, Palamut Carpaccio"],
                ["Ara sıcak", "Mare Spesiyal Ahtapot Güveç"],
                ["Ana yemek", "Mare Spesiyal Granyöz ya da Biber Kremalı Bonfile"],
                ["Tatlı", "Ormanda Bir Yürüyüş"],
                ["Kapanış", "Türk kahvesi ya da bir likör"],
            ]),
            "Mare Gastro'da sabit bir tadım menüsü yok; bu akış à la carte menüden kurulmuş bir öneri. Şarap seçimi için ekipten öneri isteyebilirsiniz.",
        ]),
        ("Özel Gün Hazırlığı Nasıl Yapılıyor?", [
            "Doğum günü, yıldönümü ya da evlilik teklifi gibi akşamlarda pasta, mum, çiçek ve masa süslemesi rezervasyon notuyla planlanıyor; pasta dijital menünün Ekstralar bölümünde ayrı bir kalem. Teklif planlıyorsanız %s, yıldönümü için %s ayrıntılı anlattık." % (P("sapanca-evlilik-teklifi", "evlilik teklifi yazımızda"), P("sapanca-yildonumu-icin-en-iyi-mekan", "yıldönümü rehberimizde")),
        ]),
    ],
    "didi-otel-restoran": [
        ("Didi Otel'de Kalanlar İçin Örnek Akşam Planı", [
            table(["Saat", "Plan"], [
                ["Öğleden sonra", "Otele giriş, bahçede dinlenme"],
                ["Gün batımı", "Bahçede bir içecek; kışın 17:30, yazın 20:30 civarı"],
                ["Akşam", "Mare Gastro'da akşam yemeği; hafta sonuysa canlı müzik"],
                ["Ertesi sabah", "09:00'dan itibaren kahvaltı menüsü"],
            ]),
            "Otelde kalıyorsanız akşam yemeği için de rezervasyon yapmanızı öneririz; hafta sonu akşamları restoran dışarıdan gelen misafirlerle de doluyor.",
        ]),
        ("Sık Karıştırılan Konular", [
            ul([
                "<strong>Rezervasyonlar ayrı:</strong> Oda rezervasyonu Didi Otel'den, masa rezervasyonu Mare Gastro'dan yapılıyor.",
                "<strong>Menü herkese aynı:</strong> Otel misafiri ya da dışarıdan gelen misafir için aynı à la carte menü geçerli.",
                "<strong>Pazartesi:</strong> Restoran Pazartesi kapalı; otelin kendi düzeni için Didi Otel'e danışın.",
            ]),
        ]),
    ],
    "sapancaya-nasil-gidilir": [
        ("Varınca: Giriş, Vale ve Masaya Geçiş", [
            "Didi Otel'in girişine geldiğinizde vale aracınızı alıyor; kendiniz park etmek isterseniz otopark da ücretsiz. Restoranın girişini lacivert MARE tentesinden tanıyabilirsiniz. Rezervasyonunuz varsa adınızı söylemeniz yeterli; ekip sizi bahçedeki ya da kapalı salondaki masanıza yönlendiriyor.",
        ]),
        ("Hafta Sonu Trafiği İçin İpuçları", [
            ul([
                "Cuma akşamı İstanbul çıkışı en yoğun zaman; mümkünse 17:00'den önce ya da 20:00'den sonra yola çıkın.",
                "Pazar akşamı İstanbul yönüne dönüş trafiği yoğunlaşıyor; akşam yemeğini geç saate kaydırmak dönüşü rahatlatabiliyor.",
                "Gecikecekseniz %s haber verin; masanız tutulur." % ext(WA, "WhatsApp'tan"),
            ]),
        ]),
    ],
}
for _r in REFRESH_TR3:
    if _r["slug"] in _MORE and "body" in _r:
        _r["body"] = list(_r["body"]) + _MORE[_r["slug"]]
