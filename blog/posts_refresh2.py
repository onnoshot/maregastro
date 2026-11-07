# -*- coding: utf-8 -*-
"""2026-11-07 Search Console yenilemesi — marka dışı aramalarda 7-12. sırada duran 3 yazı.

Search Console (2026-08-07..11-05): "sapanca en iyi restoranlar" ~11. sıra,
"sapanca lüks restoranlar" ~10. sıra, "sapancaya nasıl gidilir" 7-10. sıra.
Yalnızca başlık, açıklama, cevap-önce giriş paragrafı ve güncelleme tarihi değişir;
gövde metni aynı kalır. Kullanılan bilgiler sitede zaten doğrulanmış olanlardır:
Google puanı 4,9 (24 Ekim 2026), Salı–Pazar 12:00–00:00 / Pazartesi kapalı,
İstanbul'a ~1,5 saat, Didi Otel bahçesi, Şef Doğan Anapa, ücretsiz otopark + vale.
"""

UPDATED = "2026-11-07"
SLUGS = ["sapancanin-en-iyi-restorani", "sapanca-luks-restoran", "sapancaya-nasil-gidilir"]

REFRESH_TR2 = [
    {
        "slug": "sapancanin-en-iyi-restorani", "updated": UPDATED,
        "title": "Sapanca'nın En İyi Restoranları (2026 Rehberi) | Mare Gastro",
        "desc": "Sapanca'da en iyi restoran hangisi? Göl manzarası, mutfak ve atmosfere göre 2026 karşılaştırması. Fine dining için Mare Gastro: Şef Doğan Anapa, Google'da 4,9.",
        "lead": "<strong>Kısa cevap:</strong> Sapanca'da fine dining arıyorsanız Mare Gastro, Didi Otel bahçesinde gölün hemen yanında, Yönetici Şef Doğan Anapa'nın Ege ve Akdeniz mutfağıyla öne çıkıyor; Google'da 4,9 puanlı (Ekim 2026) ve Salı–Pazar 12:00–00:00 açık. Ama \"en iyi\" aranan deneyime göre değişir; bölgenin öne çıkan adreslerini mutfak, konum ve atmosfer açısından karşılaştırdık.",
    },
    {
        "slug": "sapanca-luks-restoran", "updated": UPDATED,
        "title": "Sapanca Lüks Restoran: Gölün Yanında Fine Dining | Mare Gastro",
        "desc": "Sapanca'da lüks restoran mı arıyorsunuz? Didi Otel bahçesinde, gölün hemen yanında fine dining: Şef Doğan Anapa, Google'da 4,9, ücretsiz otopark ve vale.",
        "lead": "<strong>Kısa cevap:</strong> Sapanca'da lüks bir akşam yemeği için Mare Gastro, Didi Otel'in bahçesinde gölün hemen yanında fine dining sunuyor: Yönetici Şef Doğan Anapa imzalı Ege ve Akdeniz mutfağı, açık ve kapalı alan, ücretsiz otopark ve vale hizmeti. Salı'dan Pazar'a 12:00–00:00 arası açık; rezervasyon site üzerinden üç adımda, WhatsApp onaylı.",
    },
    {
        "slug": "sapancaya-nasil-gidilir", "updated": UPDATED,
        "title": "Sapanca'ya Nasıl Gidilir? İstanbul, Ankara Yol Tarifi | Mare Gastro",
        "desc": "İstanbul'dan yaklaşık 1,5 saat: Sapanca'ya İstanbul, Kocaeli ve Ankara yönünden nasıl gidilir? Mare Gastro'nun Didi Otel bahçesindeki adresi, harita ve otopark bilgisi.",
        "lead": "<strong>Kısa cevap:</strong> Sapanca, İstanbul'a yaklaşık 1,5 saat mesafede; D-100 ve TEM otoyolu üzerinden kolayca ulaşılır. Mare Gastro, Didi Otel bahçesinde (Kırkpınar Soğuksu, İstasyon 3 Cad. No:55, Sapanca/Sakarya) yer alır; otopark ücretsizdir ve vale hizmeti vardır. Aşağıda İstanbul, Kocaeli ve Ankara yönünden yol tarifini bulabilirsiniz.",
    },
]
