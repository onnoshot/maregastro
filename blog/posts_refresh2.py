# -*- coding: utf-8 -*-
"""2026-11-07 Search Console yenilemesi — marka dışı aramalarda 7-12. sırada duran 3 yazı.

Search Console (2026-08-07..11-05): "sapanca en iyi restoranlar" ~11. sıra,
"sapanca lüks restoranlar" ~10. sıra, "sapancaya nasıl gidilir" 7-10. sıra.
Yalnızca başlık, açıklama, cevap-önce giriş paragrafı ve güncelleme tarihi değişir;
gövde metni aynı kalır. Kullanılan bilgiler sitede zaten doğrulanmış olanlardır:
Google puanı 4,9 (24 Ekim 2026), Salı–Pazar 09:00–00:00 / Pazartesi kapalı,
İstanbul'a ~1,5 saat, Didi Otel bahçesi, Şef Doğan Anapa, ücretsiz otopark + vale.
"""

UPDATED = "2026-11-07"
SLUGS = ["sapancanin-en-iyi-restorani", "sapanca-luks-restoran", "sapancaya-nasil-gidilir",
         "sapancada-ne-yenir", "sapanca-romantik-aksam-yemegi", "sapanca-gol-manzarali-kahvalti"]

REFRESH_TR2 = [
    {
        "slug": "sapancanin-en-iyi-restorani", "updated": UPDATED,
        "title": "Sapanca'nın En İyi Restoranları (2026 Rehberi) | Mare Gastro",
        "desc": "Sapanca'da en iyi restoran hangisi? Göl manzarası, mutfak ve atmosfere göre 2026 karşılaştırması. Fine dining için Mare Gastro: Şef Doğan Anapa, Google'da 4,9.",
        "lead": "<strong>Kısa cevap:</strong> Sapanca'da fine dining arıyorsanız Mare Gastro, Didi Otel bahçesinde gölün hemen yanında, Yönetici Şef Doğan Anapa'nın Ege ve Akdeniz mutfağıyla öne çıkıyor; Google'da 4,9 puanlı (Ekim 2026) ve Salı–Pazar 09:00–00:00 açık. Ama \"en iyi\" aranan deneyime göre değişir; bölgenin öne çıkan adreslerini mutfak, konum ve atmosfer açısından karşılaştırdık.",
    },
    {
        "slug": "sapanca-luks-restoran", "updated": UPDATED,
        "title": "Sapanca Lüks Restoran: Gölün Yanında Fine Dining | Mare Gastro",
        "desc": "Sapanca'da lüks restoran mı arıyorsunuz? Didi Otel bahçesinde, gölün hemen yanında fine dining: Şef Doğan Anapa, Google'da 4,9, ücretsiz otopark ve vale.",
        "lead": "<strong>Kısa cevap:</strong> Sapanca'da lüks bir akşam yemeği için Mare Gastro, Didi Otel'in bahçesinde gölün hemen yanında fine dining sunuyor: Yönetici Şef Doğan Anapa imzalı Ege ve Akdeniz mutfağı, açık ve kapalı alan, ücretsiz otopark ve vale hizmeti. Salı'dan Pazar'a 09:00–00:00 arası açık; rezervasyon site üzerinden üç adımda, WhatsApp onaylı.",
    },
    {
        "slug": "sapancaya-nasil-gidilir", "updated": UPDATED,
        "title": "Sapanca Yol Tarifi: İstanbul ve Ankara'dan Nasıl Gidilir? | Mare Gastro",
        "h1": "<em>Sapanca Yol Tarifi</em>: İstanbul, Ankara ve Bursa'dan Mare Gastro'ya",
        "desc": "İstanbul'dan yaklaşık 1,5 saat: Sapanca'ya İstanbul, Kocaeli ve Ankara yönünden nasıl gidilir? Mare Gastro'nun Didi Otel bahçesindeki adresi, harita ve otopark bilgisi.",
        "lead": "<strong>Kısa cevap:</strong> Sapanca, İstanbul'a yaklaşık 1,5 saat mesafede; D-100 ve TEM otoyolu üzerinden kolayca ulaşılır. Mare Gastro, Didi Otel bahçesinde (Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, Sapanca/Sakarya) yer alır; otopark ücretsizdir ve vale hizmeti vardır. Aşağıda İstanbul, Kocaeli ve Ankara yönünden yol tarifini bulabilirsiniz.",
    },
]

# 2026-11-07 (2. tur): Search Console'da 9-17. sıradaki 3 yazı için cevap-önce giriş
REFRESH_TR2 += [
    {
        "slug": "sapancada-ne-yenir", "updated": UPDATED,
        "title": "Sapanca'da Ne Yenir? Yerel Lezzetler ve Öneriler (2026) | Mare Gastro",
        "desc": "Sapanca'da ne yenir? Adapazarı ıslama köftesi ve keşkek gibi yerel tatlar, gölün hemen yanında deniz ürünleri ve Mare Gastro'da şefin bu tatlara getirdiği yorumlar.",
        "lead": "<strong>Kısa cevap:</strong> Sapanca'da bölgenin iki klasiği öne çıkar: Adapazarı'nın ıslama köftesi ve keşkek. Gölün hemen yanında ise deniz ürünleri, mezeler ve serpme kahvaltı aranır. Mare Gastro'da Şef Doğan Anapa bu yerel tatları yorumluyor; örneğin ıslama köfteden ilham alan Islama Kalamar menüde.",
    },
    {
        "slug": "sapanca-romantik-aksam-yemegi", "updated": UPDATED,
        "title": "Sapanca Romantik Akşam Yemeği: Gölün Hemen Yanında Fine Dining (2026) | Mare Gastro",
        "desc": "Sapanca'da romantik akşam yemeği için Mare Gastro: Didi Otel bahçesinde açık ve kapalı alan, Google'da 4,9, özel gün hazırlığı ve aynı bahçede konaklama.",
        "lead": "<strong>Kısa cevap:</strong> Sapanca'da romantik bir akşam yemeği için Mare Gastro, Didi Otel bahçesinde gölün hemen yanında fine dining sunuyor: açık bahçe ve kapalı salon, Google'da 4,9 puan (Ekim 2026), Salı–Pazar 09:00–00:00. Rezervasyonda not bırakırsanız ekip özel gün hazırlığını sizinle planlar ve sakin bir köşe ayarlar; gece aynı bahçedeki Didi Otel'de kalabilirsiniz.",
    },
    {
        "slug": "sapanca-gol-manzarali-kahvalti", "updated": UPDATED,
        "title": "Sapanca Kahvaltı Yerleri: Serpme Kahvaltı ve Kuymak (2026) | Mare Gastro",
        "desc": "Sapanca'da kahvaltı nerede yapılır? Mare Gastro'da serpme kahvaltı, tabak kahvaltı, kuymak ve Brioche Benedict; Didi Otel bahçesinde, Salı–Pazar 09:00'dan itibaren.",
        "lead": "<strong>Kısa cevap:</strong> Sapanca'da kahvaltı için Mare Gastro'nun kahvaltı menüsünde Serpme Kahvaltı, Tabak Kahvaltı, Kuymak ve Brioche Benedict var. Restoran Didi Otel bahçesinde, Salı'dan Pazar'a 09:00'dan itibaren açık; Pazartesi kapalı. Hafta sonu masalar çabuk dolduğu için rezervasyon önerilir.",
    },
]

MAPS_DEST = "40.7002438,30.222254"
def _dir(origin, label):
    from urllib.parse import quote
    return '<a href="https://www.google.com/maps/dir/?api=1&amp;origin=%s&amp;destination=%s" target="_blank" rel="noopener">%s</a>' % (quote(origin), MAPS_DEST, label)

# Gövdeye eklenen bölümler: {slug: (konum_indeksi, [(H2, [paragraf, ...]), ...])}
EXTRA_SECTIONS = {
    "sapancaya-nasil-gidilir": (1, [
        ("Sapanca Yol Tarifi: Haritada Tek Tıkla", [
            "Bulunduğunuz şehirden Mare Gastro'ya Google Haritalar yol tarifini doğrudan açmak için aşağıdaki bağlantılara dokunun. Süre ve rota, trafiğe göre Google tarafından anlık hesaplanır.",
            "<ul><li>" + "</li><li>".join([
                _dir("Kadıköy, İstanbul", "İstanbul Anadolu Yakası'ndan yol tarifi"),
                _dir("Taksim, İstanbul", "İstanbul Avrupa Yakası'ndan yol tarifi"),
                _dir("İzmit, Kocaeli", "İzmit'ten yol tarifi"),
                _dir("Adapazarı, Sakarya", "Adapazarı'ndan yol tarifi"),
                _dir("Bursa", "Bursa'dan yol tarifi"),
                _dir("Kızılay, Ankara", "Ankara'dan yol tarifi"),
            ]) + "</li></ul>",
            "Adres: Kırkpınar, İstasyon 3 Cad. No:55, Sapanca/Sakarya (Didi Otel bahçesi). Otopark ücretsiz, vale hizmeti var.",
        ]),
    ]),
    "sapancada-ne-yenir": (1, [
        ("Sapanca'nın Yerel Tatları Mare Gastro'da Nasıl Yorumlanıyor?", [
            "Şef Doğan Anapa bölgenin yemek kültürünü Ege-Akdeniz tekniğiyle yeniden yorumluyor. <strong>Islama Kalamar</strong>, Adapazarı ıslama köftesindeki ekmeği kemik suyu yerine balık suyuyla ıslatıp üzerine ızgara bebek kalamar koyuyor. Yaz menüsündeki keşkek üstünde kuzu incik ise bölgede çok sevilen keşkeği fine dining tabağına taşıdı.",
            "Altı imza tabağın nasıl hazırlandığını şefin kendi anlatımı ve videolarıyla <a href=\"https://maregastro.com/blog/mare-gastro-imza-tabaklar-nasil-hazirlaniyor.html\">imza tabaklar yazımızda</a> topladık.",
        ]),
    ]),
}
