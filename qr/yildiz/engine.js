/* Mare Gastro · Yıldız Menüsü - recommendation engine.
   Pure functions, no DOM. Works in the browser (window.YildizEngine) and in Node (module.exports).
   Input: live menu (from /api/menu) + guest profile(s). Output: a coherent, budget-fit tasting menu
   with a personal reading and a reason for every dish. Same input -> same menu (seeded); a new
   "variant" gives a different but equally valid reading. */
(function (root) {
  'use strict';

  // ───────────────────────────── Signs ─────────────────────────────
  const SIGNS = [
    { id: 'koc', name: 'Koç', dates: '21 Mart – 19 Nisan', el: 'ates', ruler: 'Mars', rulerGen: "Mars'ın", key: 'cesaret',
      f: 'Koç kadını masaya ilk adımı atan kişidir; beklemeyi değil, ilk lokmayı sever.',
      m: 'Koç erkeği iştahını saklamaz; masada tempo onunla başlar.',
      palate: "Mars'ın ateşi damağında közü, acıyı ve cesur tatları arar. Uzun uzun bekleyen tabaklar değil, sıcak ve net lezzetler sana göre.",
      taste: { spicy: 3, grill: 3, bold: 3, meat: 2, crispy: 1, signature: 1 },
      drinks: { cocktail: 2.5, red: 2, whisky: 2, raki: 1.5, white: 0.5, rose: 0.5, sparkling: 1, none: 0 },
      cocktails: ['margarita', 'whisky-sour', 'long-island'] },
    { id: 'boga', name: 'Boğa', dates: '20 Nisan – 20 Mayıs', el: 'toprak', ruler: 'Venüs', rulerGen: "Venüs'ün", key: 'keyif',
      f: 'Boğa kadını lezzeti acele etmeden, tadını çıkararak yaşar.',
      m: 'Boğa erkeği için iyi yemek bir ödül değil, yaşam biçimidir.',
      palate: "Venüs'ün yönettiği damağın yumuşak dokuları, tereyağını, yavaş pişmiş etleri ve iyi bir tatlıyı sever. Senin için kalite, miktardan önce gelir.",
      taste: { rich: 3, slow: 3, creamy: 2, buttery: 2, earthy: 2, chocolate: 2, meat: 1, traditional: 1 },
      drinks: { red: 3, raki: 1.5, white: 1, rose: 1.5, sparkling: 1.5, cocktail: 1, whisky: 1, none: 0 },
      cocktails: ['espresso-martini', 'plum-sour'] },
    { id: 'ikizler', name: 'İkizler', dates: '21 Mayıs – 20 Haziran', el: 'hava', ruler: 'Merkür', rulerGen: "Merkür'ün", key: 'merak',
      f: 'İkizler kadını tek bir tabakla yetinmez; masada merak, sohbet ve sürpriz ister.',
      m: 'İkizler erkeği menüde en çok çeşitliliği sever; her lokmada yeni bir hikâye arar.',
      palate: "Merkür'ün hızlı zihni çıtır dokulara, ferah ve narenciyeli tatlara, paylaşılan küçük tabaklara çeker. Tekdüzelik senin damağına göre değil.",
      taste: { playful: 3, crispy: 3, fresh: 2, citrus: 2, share: 2, light: 1, herbal: 1 },
      drinks: { cocktail: 3, white: 2, rose: 1.5, raki: 1.5, sparkling: 1.5, red: 0.5, whisky: 0, none: 0 },
      cocktails: ['mojito', 'aperol-energy', 'cin-fizz'] },
    { id: 'yengec', name: 'Yengeç', dates: '21 Haziran – 22 Temmuz', el: 'su', ruler: 'Ay', rulerGen: "Ay'ın", key: 'yuva',
      f: 'Yengeç kadını için sofra, sevdikleriyle kurulan bir yuvadır.',
      m: 'Yengeç erkeği tanıdık tatlarda huzur bulur; ev sıcaklığı onun lüksüdür.',
      palate: "Ay'ın etkisindeki damağın denizi, geleneksel tarifleri ve kremalı, sarıp sarmalayan dokuları sever. Anı taşıyan tatlar seni en çok mutlu eder.",
      taste: { sea: 3, traditional: 3, creamy: 2, buttery: 2, sweet: 1, slow: 1, local: 1 },
      drinks: { raki: 3, white: 2, rose: 1.5, red: 0.5, cocktail: 0.5, sparkling: 1, whisky: 0, none: 0 },
      cocktails: ['alkollu-meyve-kokteyli', 'plum-sour'] },
    { id: 'aslan', name: 'Aslan', dates: '23 Temmuz – 22 Ağustos', el: 'ates', ruler: 'Güneş', rulerGen: "Güneş'in", key: 'ihtişam',
      f: 'Aslan kadını sahneyi sever; tabağı da en az kendisi kadar etkileyici olmalı.',
      m: 'Aslan erkeği masanın merkezindedir; sıradan bir tabak ona yakışmaz.',
      palate: 'Güneş’in burcu imza tabaklara, gösterişli sunumlara ve cömert, güçlü lezzetlere yönelir. Şefin özel tarifleri tam sana göre.',
      taste: { signature: 3, elegant: 3, bold: 2, meat: 2, grill: 2, rich: 1, share: 1 },
      drinks: { sparkling: 3, red: 2, whisky: 2, cocktail: 1.5, raki: 1, white: 1, rose: 1, none: 0 },
      cocktails: ['whisky-sour', 'espresso-martini', 'aperol-energy'] },
    { id: 'basak', name: 'Başak', dates: '23 Ağustos – 22 Eylül', el: 'toprak', ruler: 'Merkür', rulerGen: "Merkür'ün", key: 'özen',
      f: 'Başak kadını ayrıntıyı fark eder; tabağın temizliği ve dengesi onun için önemlidir.',
      m: 'Başak erkeği iyi düşünülmüş, sade ve özenli tabakları sever.',
      palate: "Merkür'ün toprak tarafı taze otlara, zeytinyağına, hafif ve dengeli tabaklara yönelir. Az ama kusursuz, senin ölçün.",
      taste: { fresh: 3, herbal: 3, light: 3, earthy: 2, local: 1, elegant: 1, citrus: 1 },
      drinks: { white: 3, rose: 1.5, raki: 1.5, cocktail: 1, red: 1, sparkling: 1, whisky: 0, none: 0 },
      cocktails: ['kuzu-kulagi-sour', 'cin-fizz'] },
    { id: 'terazi', name: 'Terazi', dates: '23 Eylül – 22 Ekim', el: 'hava', ruler: 'Venüs', rulerGen: "Venüs'ün", key: 'denge',
      f: 'Terazi kadını için güzellik ve denge, lezzet kadar önemlidir.',
      m: 'Terazi erkeği zarafeti sever; masada uyum ve estetik arar.',
      palate: "Venüs'ün hava burcu meyveli, zarif, tatlı ile ekşinin dengelendiği tabakları sever. Göze de hitap eden her şey seni çeker.",
      taste: { elegant: 3, fruity: 3, sweet: 2, fresh: 2, citrus: 1, creamy: 1 },
      drinks: { rose: 3, sparkling: 3, white: 2, cocktail: 2, red: 1, raki: 1, whisky: 0, none: 0 },
      cocktails: ['plum-sour', 'sex-on-the-beach', 'aperol-energy'] },
    { id: 'akrep', name: 'Akrep', dates: '23 Ekim – 21 Kasım', el: 'su', ruler: 'Plüton', rulerGen: "Plüton'un", key: 'derinlik',
      f: 'Akrep kadını yüzeyde kalmaz; tatların da derin ve yoğun olmasını ister.',
      m: 'Akrep erkeği yoğunluğu sever; masada da orta yol ona göre değil.',
      palate: "Plüton'un yönettiği damak çiğ ve marine tatlara, isli aromalara, koyu çikolataya ve güçlü kontrastlara çeker. Gizemli ve iddialı tabaklar senin.",
      taste: { raw: 3, bold: 3, smoky: 2, chocolate: 2, sea: 2, spicy: 1, rich: 1 },
      drinks: { red: 3, raki: 2, whisky: 2, cocktail: 1.5, white: 1, rose: 0.5, sparkling: 0.5, none: 0 },
      cocktails: ['espresso-martini', 'whisky-sour'] },
    { id: 'yay', name: 'Yay', dates: '22 Kasım – 21 Aralık', el: 'ates', ruler: 'Jüpiter', rulerGen: "Jüpiter'in", key: 'macera',
      f: 'Yay kadını sofrada maceracıdır; yeni tatlara herkesten önce “evet” der.',
      m: 'Yay erkeği cömert sofraları, paylaşılan tabakları ve uzun sohbetleri sever.',
      palate: "Jüpiter'in cömertliği ortaya konan tabaklara, baharata, közün ateşine ve yerel lezzetlere yönelir. Bol, paylaşılan ve neşeli bir masa sana göre.",
      taste: { share: 3, spicy: 2, grill: 2, local: 2, playful: 2, bold: 1 },
      drinks: { raki: 3, cocktail: 2, red: 1.5, white: 1, rose: 1, sparkling: 1, whisky: 1, none: 0 },
      cocktails: ['long-island', 'margarita', 'r-r'] },
    { id: 'oglak', name: 'Oğlak', dates: '22 Aralık – 19 Ocak', el: 'toprak', ruler: 'Satürn', rulerGen: "Satürn'ün", key: 'kalite',
      f: 'Oğlak kadını kaliteyi tanır; klasikleri ve doğru yapılmış işleri sever.',
      m: 'Oğlak erkeği için iyi bir yemek emek ve zaman ister.',
      palate: "Satürn'ün sabrı yavaş pişmiş etlere, köklü tariflere ve olgun lezzetlere yönelir. Zamanın sınadığı tatlar senin damağına göre.",
      taste: { traditional: 3, slow: 3, meat: 2, earthy: 2, elegant: 1, smoky: 1, rich: 1 },
      drinks: { red: 3, whisky: 3, raki: 1.5, white: 1, rose: 0.5, sparkling: 1, cocktail: 0.5, none: 0 },
      cocktails: ['whisky-sour', 'espresso-martini'] },
    { id: 'kova', name: 'Kova', dates: '20 Ocak – 18 Şubat', el: 'hava', ruler: 'Uranüs', rulerGen: "Uranüs'ün", key: 'özgünlük',
      f: 'Kova kadını sıra dışını sever; menüde en beklenmedik eşleşme onun favorisidir.',
      m: 'Kova erkeği alışılmışın dışına çıkmayı sever; masada da öyle.',
      palate: "Uranüs'ün etkisindeki damak beklenmedik birleşimlere, meyveli ve ekşi dokunuşlara, çiğ ve modern tabaklara yönelir. “Bu da nereden çıktı?” dedirten tatlar senin.",
      taste: { playful: 3, raw: 2, fruity: 2, citrus: 2, fresh: 1, crispy: 1 },
      drinks: { cocktail: 3, white: 1.5, sparkling: 1.5, raki: 1, rose: 1, red: 0.5, whisky: 0.5, none: 0 },
      cocktails: ['r-r', 'kuzu-kulagi-sour', 'espresso-martini'] },
    { id: 'balik', name: 'Balık', dates: '19 Şubat – 20 Mart', el: 'su', ruler: 'Neptün', rulerGen: "Neptün'ün", key: 'hayal',
      f: 'Balık kadını sofrayı bir his olarak yaşar; atmosfer ve tat birlikte akar.',
      m: 'Balık erkeği hayalperesttir; masada yumuşak, zarif ve denizden gelen tatları sever.',
      palate: "Neptün'ün damağı denize, yumuşak ve kremalı dokulara, narenciyeye ve rüya gibi tatlılara çeker. Seni bir yere götüren tabaklar en çok sana göre.",
      taste: { sea: 3, dreamy: 3, creamy: 2, sweet: 2, citrus: 1, light: 1 },
      drinks: { white: 3, rose: 2, raki: 2, cocktail: 1, sparkling: 1, red: 0.5, whisky: 0, none: 0 },
      cocktails: ['alkollu-meyve-kokteyli', 'plum-sour'] },
  ];
  const EL = { ates: 'Ateş', toprak: 'Toprak', hava: 'Hava', su: 'Su' };

  // Simplified constellation line-art, 100×100 box: [points, edges]
  const STARS = {
    koc: [[[12, 62], [48, 40], [70, 38], [86, 50]], [[0, 1], [1, 2], [2, 3]]],
    boga: [[[8, 12], [28, 34], [40, 46], [50, 58], [62, 44], [78, 30], [94, 14], [54, 80]], [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [3, 7]]],
    ikizler: [[[30, 8], [62, 10], [26, 40], [58, 42], [16, 90], [34, 88], [52, 92], [70, 86]], [[0, 1], [0, 2], [2, 4], [2, 5], [1, 3], [3, 6], [3, 7]]],
    yengec: [[[50, 12], [50, 48], [22, 86], [62, 64], [80, 84]], [[0, 1], [1, 2], [1, 3], [3, 4]]],
    aslan: [[[18, 30], [26, 14], [42, 10], [50, 24], [44, 40], [60, 58], [84, 66], [90, 46], [66, 40]], [[4, 3], [3, 2], [2, 1], [1, 0], [4, 5], [5, 6], [6, 7], [7, 8], [8, 4]]],
    basak: [[[10, 20], [28, 30], [44, 44], [58, 40], [74, 24], [62, 62], [82, 80], [40, 74]], [[0, 1], [1, 2], [2, 3], [3, 4], [2, 7], [3, 5], [5, 6]]],
    terazi: [[[50, 10], [22, 42], [78, 42], [16, 78], [84, 74]], [[0, 1], [0, 2], [1, 2], [1, 3], [2, 4]]],
    akrep: [[[8, 22], [16, 10], [22, 32], [34, 40], [44, 50], [52, 64], [58, 80], [72, 90], [86, 86], [90, 72]], [[0, 2], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]]],
    yay: [[[20, 62], [36, 46], [52, 52], [48, 74], [30, 80], [62, 34], [74, 52], [88, 42]], [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0], [1, 5], [5, 6], [2, 6], [6, 7]]],
    oglak: [[[12, 20], [30, 30], [58, 72], [78, 62], [90, 28], [52, 44]], [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 1]]],
    kova: [[[10, 30], [28, 20], [44, 34], [58, 24], [72, 40], [62, 62], [80, 84], [46, 82]], [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [5, 7]]],
    balik: [[[8, 24], [18, 10], [26, 26], [32, 50], [44, 70], [58, 84], [68, 68], [82, 62], [94, 72], [84, 84]], [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 6]]],
  };

  // ───────────────────────────── Name: meaning + numerology ─────────────────────────────
  const NAME_GROUP = {
    su: { sea: 3, light: 1, citrus: 1 },
    ates: { spicy: 2, grill: 2, bold: 2 },
    isik: { elegant: 2, citrus: 2, light: 2 },
    cicek: { fruity: 2, herbal: 2, sweet: 1, elegant: 1 },
    toprak: { earthy: 2, traditional: 2, local: 2, slow: 1 },
    ruzgar: { fresh: 2, playful: 2, crispy: 1, light: 1 },
    asil: { signature: 3, elegant: 2, rich: 1, meat: 1 },
    tatli: { sweet: 2, chocolate: 2, creamy: 1, dreamy: 1 },
    derin: { raw: 2, smoky: 1, sea: 1, bold: 1 },
    guc: { meat: 2, bold: 2, grill: 1 },
    nese: { playful: 3, fruity: 1, share: 1 },
    gok: { dreamy: 2, light: 1, elegant: 1 },
    farkli: { playful: 2, raw: 1, fruity: 1 },
  };
  const NAMES = {
    deniz: ['deniz', 'su'], derya: ['deniz', 'su'], ege: ['Ege denizi', 'su'], su: ['su', 'su'], cansu: ['can suyu', 'su'],
    nehir: ['nehir', 'su'], ırmak: ['ırmak', 'su'], irmak: ['ırmak', 'su'], yağmur: ['yağmur', 'su'], damla: ['damla', 'su'],
    pınar: ['su kaynağı', 'su'], duru: ['berrak', 'su'], selin: ['akarsu', 'su'], tuna: ['Tuna nehri', 'su'], arda: ['bir nehir adı', 'su'],
    nil: ['Nil nehri', 'su'], çağla: ['çağlayan', 'su'], ada: ['ada', 'su'], tansu: ['şafak suyu', 'su'], mavi: ['mavi', 'su'],
    ateş: ['ateş', 'ates'], alev: ['alev', 'ates'], volkan: ['yanardağ', 'ates'], şule: ['alev', 'ates'], yıldırım: ['yıldırım', 'ates'],
    güneş: ['güneş', 'isik'], nur: ['ışık', 'isik'], ilknur: ['ilk ışık', 'isik'], aynur: ['ay ışığı', 'isik'], tan: ['şafak', 'isik'],
    şafak: ['şafak', 'isik'], seher: ['tan vakti', 'isik'], umut: ['umut', 'isik'], ümit: ['umut', 'isik'], elif: ['zarif, ince', 'isik'],
    cemre: ['baharı müjdeleyen sıcaklık', 'isik'],
    ay: ['ay', 'gok'], aylin: ['ayın çevresindeki ışık halkası', 'gok'], ayla: ['ayın çevresindeki hale', 'gok'], aysel: ['ay ışığının seli', 'gok'],
    ayça: ['küçük ay', 'gok'], ilkay: ['ilk ay', 'gok'], yıldız: ['yıldız', 'gok'], gökçe: ['gök mavisi', 'gok'], gökay: ['gök ve ay', 'gok'],
    melek: ['melek', 'gok'], esin: ['ilham', 'gok'], eren: ['ermiş', 'gok'],
    gizem: ['sır', 'derin'], ela: ['ela göz', 'derin'],
    ece: ['kraliçe', 'asil'], begüm: ['hanımefendi', 'asil'], sultan: ['hükümdar', 'asil'], kaan: ['hükümdar', 'asil'], kağan: ['hükümdar', 'asil'],
    cem: ['hükümdar', 'asil'], emir: ['yönetici, buyruk', 'asil'], gökhan: ['göklerin hanı', 'asil'], kerem: ['cömertlik', 'asil'],
    onur: ['şeref', 'asil'], erdem: ['fazilet', 'asil'], zeynep: ['değerli taş', 'asil'], mehmet: ['övülmüş', 'asil'], ahmet: ['çok övülen', 'asil'],
    mustafa: ['seçilmiş', 'asil'], ali: ['yüce', 'asil'],
    mert: ['yiğit', 'guc'], efe: ['yiğit', 'guc'], batu: ['sağlam', 'guc'], tolga: ['savaş miğferi', 'guc'], alp: ['yiğit', 'guc'],
    alper: ['yiğit er', 'guc'], aslan: ['aslan', 'guc'], arslan: ['aslan', 'guc'], berk: ['sağlam, güçlü', 'guc'], doruk: ['zirve', 'guc'], kaya: ['kaya', 'guc'],
    can: ['can, ruh', 'nese'], hande: ['gülümseme', 'nese'], neşe: ['neşe', 'nese'], ezgi: ['melodi', 'nese'], seda: ['ses, yankı', 'nese'],
    ozan: ['halk şairi', 'nese'], ayşe: ['yaşayan, hayat dolu', 'nese'], büşra: ['müjde', 'nese'], yaren: ['dost', 'nese'],
    emre: ['dost, âşık', 'tatli'], sevda: ['aşk', 'tatli'], sevgi: ['sevgi', 'tatli'], ipek: ['ipek', 'tatli'], hasan: ['güzel', 'tatli'],
    hüseyin: ['küçük güzel', 'tatli'], murat: ['dilek', 'tatli'], dilek: ['dilek', 'tatli'], nazlı: ['nazlı', 'tatli'], buse: ['öpücük', 'tatli'], eda: ['naz, zarafet', 'tatli'],
    barış: ['barış', 'tatli'],
    rüzgar: ['rüzgâr', 'ruzgar'], rüzgâr: ['rüzgâr', 'ruzgar'], poyraz: ['kuzey rüzgârı', 'ruzgar'], bora: ['fırtına', 'ruzgar'],
    ceren: ['ceylan', 'ruzgar'], ceylan: ['ceylan', 'ruzgar'],
    toprak: ['toprak', 'toprak'], ilgın: ['ılgın ağacı', 'toprak'], emine: ['güvenilir', 'toprak'],
    defne: ['defne ağacı', 'cicek'], bahar: ['ilkbahar', 'cicek'], çiçek: ['çiçek', 'cicek'], gül: ['gül', 'cicek'], lale: ['lale', 'cicek'],
    nilüfer: ['nilüfer çiçeği', 'cicek'], yasemin: ['yasemin çiçeği', 'cicek'], menekşe: ['menekşe', 'cicek'], gülşen: ['gül bahçesi', 'cicek'],
    özge: ['başka, farklı', 'farkli'],
  };
  const fold = (s) => s.replace(/ç/g, 'c').replace(/ğ/g, 'g').replace(/ı/g, 'i').replace(/ö/g, 'o').replace(/ş/g, 's').replace(/ü/g, 'u').replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u');
  const NAMES_FOLD = {};
  Object.keys(NAMES).forEach((k) => { const f = fold(k); if (!NAMES_FOLD[f]) NAMES_FOLD[f] = NAMES[k]; });

  const NUM = {
    1: { t: 'Öncü', s: 'Sayın 1, öncülerin sayısı: masada ilk kararı veren sensin. Menüne iddialı bir imza tabak koyduk.', tags: { signature: 2, bold: 2 } },
    2: { t: 'Uyum', s: 'Sayın 2, uyumun ve paylaşmanın sayısı. Menünde ortaya konan, bölüşüldükçe güzelleşen tabaklar var.', tags: { share: 2, sweet: 1, creamy: 1 } },
    3: { t: 'Neşe', s: 'Sayın 3, neşenin ve ifadenin sayısı. Menüne oyunbaz, renkli tatlar ekledik.', tags: { playful: 2, fruity: 2 } },
    4: { t: 'Kök', s: 'Sayın 4, sağlam temellerin sayısı. Menünde köklü, güven veren tarifler öne çıkıyor.', tags: { traditional: 2, earthy: 2 } },
    5: { t: 'Macera', s: 'Sayın 5, maceranın ve değişimin sayısı. Menüne biraz baharat, biraz sürpriz kattık.', tags: { spicy: 2, crispy: 1, playful: 1 } },
    6: { t: 'Zarafet', s: 'Sayın 6, güzelliğin ve zarafetin sayısı. Menünde ince, kremalı ve zarif dokunuşlar var.', tags: { elegant: 2, creamy: 1, sweet: 1 } },
    7: { t: 'Derinlik', s: 'Sayın 7, sezginin ve derinliğin sayısı. Menüne denizden ve gizemli, marine tatlardan seçtik.', tags: { raw: 2, sea: 1, smoky: 1 } },
    8: { t: 'Güç', s: 'Sayın 8, gücün ve bolluğun sayısı. Menünde doyurucu, güçlü bir ana yemek seni bekliyor.', tags: { meat: 2, rich: 2 } },
    9: { t: 'Bütünlük', s: 'Sayın 9, tamamlanmanın sayısı. Menün tazeden zengine, baştan sona dengeli bir yolculuk.', tags: { fresh: 2, herbal: 1, share: 1 } },
  };
  const ALPHA = 'abcçdefgğhıijklmnoöprsştuüvyz';
  function numerology(lower) {
    let sum = 0;
    for (const ch of lower) {
      const i = ALPHA.indexOf(ch);
      if (i >= 0) sum += (i % 9) + 1;
      else if (ch === 'w') sum += 5; else if (ch === 'x') sum += 6; else if (ch === 'q') sum += 8;
    }
    while (sum > 9) sum = String(sum).split('').reduce((a, b) => a + Number(b), 0);
    return sum || 9;
  }
  const lowerTr = (s) => String(s || '').toLocaleLowerCase('tr');
  function cleanName(raw) {
    const s = String(raw || '').replace(/[^\p{L}\s'-]/gu, ' ').replace(/\s+/g, ' ').trim().slice(0, 40);
    return s.split(' ').filter(Boolean).map((w) => w.charAt(0).toLocaleUpperCase('tr') + w.slice(1).toLocaleLowerCase('tr')).join(' ');
  }
  function nameInfo(raw) {
    const display = cleanName(raw);
    const first = lowerTr(display.split(' ')[0] || '');
    const hit = NAMES[first] || NAMES_FOLD[fold(first)] || null;
    const n = numerology(lowerTr(display.replace(/\s/g, '')));
    return { display, first: display.split(' ')[0] || '', meaning: hit ? hit[0] : null, group: hit ? hit[1] : null,
      tags: hit ? NAME_GROUP[hit[1]] : {}, num: n, numInfo: NUM[n] };
  }
  // Turkish genitive suffix: Ayşe'nin, Deniz'in, Onur'un, Gül'ün
  function gen(name) {
    const l = lowerTr(name);
    const vs = l.match(/[aeıioöuü]/g);
    const v = vs ? vs[vs.length - 1] : 'e';
    const suf = { a: 'ın', ı: 'ın', e: 'in', i: 'in', o: 'un', u: 'un', ö: 'ün', ü: 'ün' }[v];
    return name + "'" + (/[aeıioöuü]$/.test(l) ? 'n' : '') + suf;
  }

  // ───────────────────────────── Menu knowledge ─────────────────────────────
  // course, flavour tags (0–3), pairing with drink style (0–3), main ingredients (repeat guard), note (faithful to the menu text)
  // pair keys: r rakı, w white, d red, o rosé, s sparkling, c cocktail, k whisky, n alcohol-free
  const P = (r, w, d, o, s, c, k, n) => ({ raki: r, white: w, red: d, rose: o, sparkling: s, cocktail: c, whisky: k, none: n });
  const FOOD = {
    // Başlangıçlar
    'kereviz-pureli-jumbo-karides-sogus': { c: 'baslangic', t: { sea: 3, fresh: 2, citrus: 2, elegant: 2, fruity: 1 }, p: P(2, 3, 0, 3, 3, 2, 0, 2), i: ['karides'], note: 'Portakallı kereviz püresi ve yeşil elmanın serinliğinde jumbo karides' },
    'dana-carpaccio': { c: 'baslangic', t: { raw: 3, meat: 2, bold: 2, elegant: 2, herbal: 1 }, p: P(1, 1, 3, 2, 2, 2, 2, 2), i: ['dana'], note: 'İncecik dana, roka, parmesan, nar ekşisi ve kapari' },
    'somon-tartar': { c: 'baslangic', t: { raw: 3, sea: 2, citrus: 1, fresh: 1, elegant: 1 }, p: P(2, 3, 0, 3, 3, 2, 0, 2), i: ['somon'], note: 'Hardal, kapari ve soğanla marine edilmiş somon küpleri' },
    'palamut-carpaccio': { c: 'baslangic', t: { raw: 3, sea: 3, local: 2, bold: 2, herbal: 1 }, p: P(3, 2, 0, 2, 1, 1, 0, 2), i: ['palamut'], note: 'Sarımsaklı vinegret, kapari ve taze otlarla palamut' },
    'peynir-tabagi': { c: 'baslangic', t: { share: 3, traditional: 2, rich: 2, local: 2, earthy: 1 }, p: P(3, 2, 3, 2, 2, 0, 2, 1), i: ['peynir'], note: 'Ezine, eski kaşar, isli ve abaza peynirinden bir Anadolu seçkisi' },
    // Mezeler
    'girit-ezme-pancar-portakal': { c: 'meze', t: { fresh: 2, citrus: 2, herbal: 2, fruity: 1, elegant: 1 }, p: P(3, 3, 1, 3, 2, 2, 0, 3), i: ['girit', 'pancar'], note: 'Girit ezme, portakal çektirme ve pancar carpaccio' },
    'gunun-zeytinyagli-enginari': { c: 'meze', t: { light: 3, herbal: 2, earthy: 2, fresh: 2, traditional: 1, local: 1 }, p: P(3, 3, 0, 2, 1, 1, 0, 3), i: ['enginar'], note: 'Zeytinyağlı enginar, iç bakla fava ve dereotu' },
    'humus': { c: 'meze', t: { earthy: 3, nutty: 2, share: 2, traditional: 1 }, p: P(2, 2, 2, 2, 1, 1, 1, 3), i: ['nohut'], note: 'Köz kırmızı biber, fındık ve sızma zeytinyağıyla humus' },
    'domates-soslu-patlican-biber-kizartmasi': { c: 'meze', t: { traditional: 3, earthy: 2, smoky: 1, rich: 1, share: 1 }, p: P(3, 1, 2, 1, 0, 0, 0, 3), i: ['patlican'], note: 'Domates soslu patlıcan ve biber kızartması' },
    'patates-cipsli-acili-atom': { c: 'meze', t: { spicy: 3, crispy: 2, playful: 2, bold: 1 }, p: P(3, 1, 1, 1, 0, 2, 1, 2), i: ['atom'], note: 'Acılı atom, çıtır patates cipsiyle' },
    'pancar-borani': { c: 'meze', t: { earthy: 2, fruity: 1, fresh: 1, playful: 1 }, p: P(3, 2, 1, 2, 1, 1, 0, 3), i: ['pancar'], note: 'Pancar borani, zeytin ve elmalı kapari salsa' },
    'havuc-tarator': { c: 'meze', t: { creamy: 2, sweet: 1, traditional: 1, nutty: 1 }, p: P(3, 2, 0, 2, 1, 1, 0, 3), i: ['havuc'], note: 'Havuç püresiyle yumuşacık tarator' },
    'dilim-ezine-peyniri': { c: 'meze', t: { traditional: 2, local: 2 }, p: P(3, 0, 0, 0, 0, 0, 0, 0), i: ['ezine'], note: 'Rakının vazgeçilmezi, bir dilim ezine peyniri' },
    // Salatalar (meze slot)
    'roka-salatasi': { c: 'meze', t: { fresh: 3, herbal: 2, light: 2, bold: 1 }, p: P(2, 3, 2, 2, 2, 2, 1, 3), i: ['roka'], note: 'Roka, küp domates, parmesan ve sarımsaklı nar ekşili sos' },
    'semizotu-salatasi': { c: 'meze', t: { fruity: 3, fresh: 2, playful: 2, local: 1, nutty: 1 }, p: P(2, 3, 1, 3, 2, 2, 0, 3), i: ['semizotu'], note: 'Çilek, ceviz, Erzincan tulumu ve nar ekşisiyle semizotu' },
    'komsu-salata': { c: 'meze', t: { fresh: 3, traditional: 2, local: 2, light: 2 }, p: P(3, 2, 2, 2, 1, 1, 0, 3), i: ['komsu', 'ezine'], note: 'Domates, salatalık, zeytin ve ezine peyniriyle limonlu komşu salata' },
    // Ara sıcaklar
    '3-lu-deniz-mahsulu-lezzeti': { c: 'ara', share: true, t: { sea: 3, share: 3, signature: 2, rich: 1 }, p: P(3, 3, 0, 2, 2, 1, 0, 2), i: ['kalamar', 'karides', 'ahtapot'], note: 'Islama kalamar, tereyağlı karides ve ahtapot güveç tek tabakta' },
    'mare-spesiyal-ahtapot-guvec': { c: 'ara', t: { sea: 3, signature: 3, buttery: 2, rich: 2, spicy: 1, bold: 1 }, p: P(3, 3, 1, 2, 1, 1, 0, 2), i: ['ahtapot'], note: 'Sarımsak ve baharatlı tereyağında, özel marine ahtapot' },
    'mare-spesiyal-islama-kalamar': { c: 'ara', t: { sea: 3, grill: 2, herbal: 2, signature: 2, fresh: 1 }, p: P(3, 3, 0, 2, 1, 2, 0, 2), i: ['kalamar'], note: 'Izgara baby kalamar, naneli hardallı sos ve küp domates' },
    'jumbo-karides-izgara': { c: 'ara', t: { grill: 3, sea: 2, bold: 1, buttery: 1, herbal: 1 }, p: P(3, 3, 0, 2, 2, 2, 0, 2), i: ['karides'], note: 'Sarımsaklı, maydanozlu tereyağıyla ızgara jumbo karides' },
    'kalamar-tava': { c: 'ara', t: { crispy: 3, sea: 2, playful: 2, share: 2, traditional: 1 }, p: P(3, 2, 0, 1, 1, 2, 0, 3), i: ['kalamar'], note: 'Tarator sosla çıtır kalamar' },
    'yaprak-ciger': { c: 'ara', t: { traditional: 3, meat: 2, bold: 2, local: 2 }, p: P(3, 0, 2, 0, 0, 0, 1, 2), i: ['ciger'], note: '200 gram yaprak ciğer' },
    'patates-terin': { c: 'ara', t: { earthy: 3, smoky: 2, elegant: 2, rich: 1 }, p: P(1, 2, 3, 1, 1, 1, 2, 2), i: ['isli', 'mantar'], note: 'Gofret patates, kestane mantarı sos ve isli et' },
    'tereyagli-karides': { c: 'ara', t: { buttery: 3, sea: 2, rich: 2, herbal: 1 }, p: P(3, 3, 0, 2, 2, 1, 0, 2), i: ['karides'], note: 'Sarımsaklı, maydanozlu tereyağında karides' },
    // Ana yemekler
    'biber-kremali-bonfile': { c: 'ana', t: { meat: 3, rich: 2, creamy: 2, elegant: 2, bold: 2, signature: 1 }, p: P(0, 0, 3, 1, 1, 1, 3, 2), i: ['dana'], note: '200 gram dana bonfile, karabiber kremalı sos ve kibrit patates' },
    'citir-somon': { c: 'ana', t: { sea: 2, crispy: 2, creamy: 1, light: 1 }, p: P(1, 3, 0, 3, 2, 1, 0, 2), i: ['somon'], note: '200 gram somon fileto, fırın patates ve hollandaise sos' },
    'deniz-mahsulleri-bugday-risotto': { c: 'ana', t: { sea: 2, creamy: 2, buttery: 2, local: 1, traditional: 1 }, p: P(1, 3, 0, 2, 2, 1, 0, 2), i: ['karides', 'midye'], note: 'Tereyağında jumbo karides ve kum midyesiyle buğday risotto' },
    'firinda-kremali-levrek': { c: 'ana', t: { sea: 3, creamy: 3, elegant: 1, herbal: 1 }, p: P(2, 3, 0, 2, 2, 1, 0, 2), i: ['levrek'], note: 'Domates, biber ve fesleğen kremalı fırın levrek' },
    'mare-spesiyal-granyoz': { c: 'ana', t: { sea: 3, signature: 3, elegant: 2, grill: 1, light: 1 }, p: P(3, 3, 0, 2, 2, 1, 0, 2), i: ['levrek'], note: 'Kaya levreği, köz biber sos, köz domates ve beurre blanc' },
    'kuzu-pirzola': { c: 'ana', t: { meat: 3, grill: 3, bold: 2, smoky: 1, spicy: 1, signature: 1 }, p: P(2, 0, 3, 1, 1, 1, 2, 2), i: ['kuzu'], note: 'Patlıcan beğendi, kibrit patates ve kıl biberle kuzu pirzola' },
    'balkabagi-soslu-kestane-dolgulu-makarna': { c: 'ana', t: { earthy: 3, smoky: 2, creamy: 2, playful: 1, sweet: 1 }, p: P(0, 2, 2, 2, 1, 1, 0, 2), i: ['kestane', 'isli'], note: 'Balkabağı soslu kestane dolgulu makarna, isli et ve mantar salsa' },
    'palamut-izgara-kofte': { c: 'ana', t: { local: 3, sea: 2, grill: 2, traditional: 2, buttery: 1 }, p: P(3, 2, 0, 1, 0, 1, 0, 2), i: ['palamut'], note: 'Tereyağlı patates püresiyle ızgara palamut köfte' },
    'kuzu-kokorec': { c: 'ana', t: { traditional: 3, local: 3, spicy: 2, bold: 2, meat: 1 }, p: P(3, 0, 1, 0, 0, 0, 0, 2), i: ['kuzu'], note: 'Karpuzlu çoban salata, taze lavaş ve köz kıl biberle kokoreç' },
    'mezgit-tempura': { c: 'ana', t: { crispy: 3, sea: 2, light: 2, playful: 2 }, p: P(2, 3, 0, 2, 2, 2, 0, 2), i: ['mezgit'], note: 'Çıtır tempura mezgit' },
    'incik-ruyasi': { c: 'ana', t: { slow: 3, meat: 3, traditional: 3, rich: 2, herbal: 1 }, p: P(1, 0, 3, 1, 1, 0, 2, 2), i: ['incik'], note: 'Keşkek yatağında yavaş pişmiş incik, nane yağı' },
    // Tatlılar
    'mare-sekerpare': { c: 'tatli', t: { traditional: 3, sweet: 2, nutty: 1, signature: 1 }, p: P(2, 2, 2, 2, 2, 2, 2, 3), i: ['geleneksel-tatli'], note: 'Fındıklı, limonlu, tereyağlı Mare şekerpare' },
    'meyve-tabagi': { c: 'tatli', t: { fresh: 3, fruity: 3, light: 3, share: 2 }, p: P(3, 2, 1, 2, 3, 2, 1, 3), i: [], note: 'Mevsim meyveleri' },
    'ormanda-bir-yuruyus': { c: 'tatli', t: { chocolate: 3, dreamy: 3, playful: 2, creamy: 1, signature: 1 }, p: P(1, 1, 3, 2, 2, 3, 2, 3), i: ['cikolata'], note: 'Çikolata mus, çıtır profiterol, Mare yapımı vanilyalı dondurma ve çilek' },
    'cerkes-peynirli-cheesecake': { c: 'tatli', t: { creamy: 3, sweet: 2, local: 2 }, p: P(1, 2, 1, 3, 3, 2, 1, 3), i: [], note: 'Çerkez peyniriyle bisküvi tabanlı cheesecake' },
    'citir-kabak-tatlisi': { c: 'tatli', t: { traditional: 3, sweet: 2, nutty: 2, local: 1, earthy: 1 }, p: P(3, 1, 1, 1, 1, 1, 1, 3), i: ['geleneksel-tatli'], note: 'Kaymak ve tahinle çıtır kabak tatlısı' },
    'cikolatali-mousse': { c: 'tatli', t: { chocolate: 3, rich: 2, dreamy: 1, fruity: 1, herbal: 1 }, p: P(0, 1, 3, 2, 2, 3, 2, 3), i: ['cikolata'], note: 'Karabuğday patlağı, nane ve çilekle çikolatalı mousse' },
  };

  // Drinks: style, who can get it (s = single, c = couple), flavour tags, note
  const DRINK = {
    // single servings
    'double-raki': { st: 'raki', for: 's', unit: 'duble', t: { traditional: 2, local: 2, sea: 1 }, note: 'Buz, su ve sohbet; mezelerle başlayan klasik' },
    'kadeh-sarap@white': { base: 'kadeh-sarap', st: 'white', for: 's', unit: 'kadeh', label: 'Kadeh Şarap · Beyaz', t: { fresh: 2, citrus: 1, sea: 1, creamy: 1 }, note: 'Angora, kadehte beyaz servis edilir' },
    'kadeh-sarap@red': { base: 'kadeh-sarap', st: 'red', for: 's', unit: 'kadeh', label: 'Kadeh Şarap · Kırmızı', t: { meat: 2, rich: 1, earthy: 1, smoky: 1 }, note: 'Angora, kadehte kırmızı servis edilir' },
    'double-viski-black-label': { st: 'whisky', for: 's', unit: 'duble', t: { smoky: 2, bold: 2, meat: 1 }, note: 'Johnnie Walker Black Label, duble' },
    'chivas-regal-18-years-double': { st: 'whisky', for: 's', unit: 'duble', t: { rich: 2, elegant: 2, slow: 1 }, note: 'Chivas Regal 18, duble' },
    // cocktails (both)
    'margarita': { st: 'cocktail', for: 'sc', t: { citrus: 2, bold: 1, spicy: 1 }, note: 'Tekila, limon ve portakal likörü' },
    'whisky-sour': { st: 'cocktail', for: 'sc', t: { citrus: 2, bold: 1, rich: 1, meat: 1 }, note: 'Bourbon, limon ve köpüklü yumurta akı' },
    'long-island': { st: 'cocktail', for: 'sc', t: { bold: 2, playful: 1, share: 1 }, note: 'Tekila, votka, cin ve rom; tam bir macera' },
    'espresso-martini': { st: 'cocktail', for: 'sc', t: { chocolate: 2, bold: 1, rich: 1 }, note: 'Votka, kahve likörü ve espresso; tatlıya eşlik eder' },
    'plum-sour': { st: 'cocktail', for: 'sc', t: { fruity: 3, elegant: 1 }, note: 'Erikli, ekşi ve zarif' },
    'mojito': { st: 'cocktail', for: 'sc', t: { fresh: 3, citrus: 2, herbal: 2 }, note: 'Lime, rom ve soda; ferah bir başlangıç' },
    'aperol-energy': { st: 'cocktail', for: 'sc', t: { playful: 2, fruity: 1, citrus: 1 }, note: 'Aperol ve triple sec, enerjik bir dokunuş' },
    'cin-fizz': { st: 'cocktail', for: 'sc', t: { fresh: 2, citrus: 2, light: 2 }, note: 'Cin ve köpüklü ferahlık' },
    'kuzu-kulagi-sour': { st: 'cocktail', for: 'sc', t: { fresh: 2, herbal: 2, playful: 2, citrus: 1 }, note: 'Kuzu kulağı, yeşil elma ve cin' },
    'r-r': { st: 'cocktail', for: 'sc', t: { herbal: 2, playful: 3, local: 2 }, note: 'Rakı, roka ve limon; rakının modern hali' },
    'sex-on-the-beach': { st: 'cocktail', for: 'sc', t: { fruity: 3, sweet: 2 }, note: 'Votka, şeftali ve portakal' },
    'alkollu-meyve-kokteyli': { st: 'cocktail', for: 'sc', t: { fruity: 3, sweet: 1, light: 1 }, note: 'Meyveli ve hafif' },
    // alcohol-free (both)
    'meyve-kokteyli': { st: 'none', for: 'sc', t: { fruity: 3, fresh: 1 }, note: 'Portakal, ananas, elma ve turunç' },
    'limonata': { st: 'none', for: 'sc', t: { citrus: 3, fresh: 2 }, note: 'Ev usulü limonata' },
    'nane-limon-frozen': { st: 'none', for: 'sc', t: { fresh: 3, herbal: 2, citrus: 1 }, note: 'Naneli, limonlu buz gibi frozen' },
    // bottles (couple)
    'beylerbeyi-gobek-20-cl': { st: 'raki', for: 'c', t: { elegant: 1, traditional: 2 }, note: '20 cl, iki kişilik kısa bir rakı sofrası' },
    'sari-zeybek-20-cl': { st: 'raki', for: 'c', t: { local: 2, traditional: 1 }, note: '20 cl, iki kişilik kısa bir rakı sofrası' },
    'beylerbeyi-gobek-35-cl': { st: 'raki', for: 'c', t: { elegant: 2, traditional: 2 }, note: '35 cl, iki kişilik masanın ideal ölçüsü' },
    'sari-zeybek-35-cl': { st: 'raki', for: 'c', t: { local: 2, traditional: 1 }, note: '35 cl, iki kişilik masanın ideal ölçüsü' },
    'efe-gobek-35-cl': { st: 'raki', for: 'c', t: { traditional: 2, bold: 1 }, note: '35 cl, iki kişilik masanın ideal ölçüsü' },
    'efe-gold-35-cl': { st: 'raki', for: 'c', t: { traditional: 2 }, note: '35 cl, iki kişilik masanın ideal ölçüsü' },
    'efe-yas-uzum-35-cl': { st: 'raki', for: 'c', t: { fruity: 1, fresh: 1, traditional: 1 }, note: '35 cl, yaş üzüm rakısı' },
    'mercan-raki-35-cl': { st: 'raki', for: 'c', t: { sea: 2, elegant: 1 }, note: '35 cl, iki kişilik masanın ideal ölçüsü' },
    'tekirdag-altinseri-35-cl': { st: 'raki', for: 'c', t: { elegant: 2, slow: 1 }, note: '35 cl, iki kişilik masanın ideal ölçüsü' },
    'tekirdag-gobek-35-cl': { st: 'raki', for: 'c', t: { traditional: 2, rich: 1 }, note: '35 cl, iki kişilik masanın ideal ölçüsü' },
    'yeni-raki-yeni-seri-35-cl': { st: 'raki', for: 'c', t: { traditional: 2, playful: 1 }, note: '35 cl, iki kişilik masanın ideal ölçüsü' },
    'tekirdag-altinseri-50-cl': { st: 'raki', for: 'c', t: { elegant: 2, slow: 2 }, note: '50 cl, uzun bir rakı sofrası için' },
    'beylerbeyi-gobek-50-cl': { st: 'raki', for: 'c', t: { elegant: 2, traditional: 2, slow: 1 }, note: '50 cl, uzun bir rakı sofrası için' },
    'baron-de-lastac-2020-beyaz': { st: 'white', for: 'c', t: { fresh: 2, citrus: 1, light: 1 }, note: 'Ferah ve hafif bir beyaz' },
    'egeo-chardonnay-2019': { st: 'white', for: 'c', t: { creamy: 3, buttery: 2, rich: 1 }, note: 'Chardonnay: kremalı ve tereyağlı tabakların eşi' },
    'egeo-fume-blanc-2020': { st: 'white', for: 'c', t: { smoky: 1, fresh: 2, sea: 2 }, note: 'Fumé Blanc: deniz ürünleriyle parlayan beyaz' },
    'egeo-sauvignon-blanc-2024': { st: 'white', for: 'c', t: { fresh: 3, citrus: 2, herbal: 2 }, note: 'Sauvignon Blanc: otlar ve narenciye kadar canlı' },
    'urla-chardonnay': { st: 'white', for: 'c', t: { creamy: 3, buttery: 2, elegant: 1 }, note: 'Chardonnay: kremalı tabakların eşi' },
    'selection-kavaklidere-beyaz': { st: 'white', for: 'c', t: { elegant: 2, fresh: 1, sea: 1 }, note: 'Zarif ve dengeli bir beyaz' },
    'khilon-beyaz': { st: 'white', for: 'c', t: { fresh: 2, local: 2, sea: 1 }, note: 'Ege’den ferah bir beyaz' },
    'baron-de-lastac-2019-kirmizi': { st: 'red', for: 'c', t: { meat: 1, fruity: 1, rich: 1 }, note: 'Yumuşak içimli bir kırmızı' },
    'sartori-merlot': { st: 'red', for: 'c', t: { creamy: 1, rich: 2, fruity: 1 }, note: 'Merlot: yuvarlak ve yumuşak' },
    'egeo-cabernet-sauvignon-2016': { st: 'red', for: 'c', t: { meat: 3, bold: 2, smoky: 1 }, note: 'Cabernet Sauvignon: güçlü etlerin eşi' },
    'urla-bogazkere': { st: 'red', for: 'c', t: { bold: 3, meat: 2, spicy: 1, local: 2 }, note: 'Boğazkere: Anadolu’nun güçlü, tanenli üzümü' },
    'urla-cabernet-sauvignon': { st: 'red', for: 'c', t: { meat: 3, bold: 2, elegant: 1 }, note: 'Cabernet Sauvignon: güçlü etlerin eşi' },
    'urla-nexus': { st: 'red', for: 'c', t: { elegant: 2, rich: 2, meat: 1 }, note: 'Urla’nın imza kırmızı harmanı' },
    'urla-tempus': { st: 'red', for: 'c', t: { slow: 2, rich: 2, earthy: 1 }, note: 'Olgun, derin bir kırmızı harman' },
    'selection-kavaklidere-kirmizi': { st: 'red', for: 'c', t: { traditional: 2, meat: 2, earthy: 1 }, note: 'Klasik ve dengeli bir kırmızı' },
    'egeo-roze-2019': { st: 'rose', for: 'c', t: { fruity: 2, fresh: 2, elegant: 2, sea: 1 }, note: 'Denizle eti aynı masada buluşturan roze' },
    'chandon-rose-sparkling': { st: 'sparkling', for: 'c', t: { elegant: 3, fruity: 2, signature: 1 }, note: 'Rose köpüklü: bu akşam bir kutlama' },
    'johnnie-walker-black-label-35-cl': { st: 'whisky', for: 'c', t: { smoky: 2, bold: 2, meat: 1 }, note: '35 cl, ikiye paylaşılan bir şişe' },
  };
  const CLOSER = { id: 'turk-kahvesi', note: 'Fincanı kapatın: gökyüzü söyledi, gerisini kahve söylesin' };

  const STYLE_NAME = { raki: 'Rakı Sofrası', white: 'Beyaz Şarap', red: 'Kırmızı Şarap', rose: 'Roze', sparkling: 'Köpüklü', cocktail: 'Kokteyl Eşliği', whisky: 'Viski', none: 'Alkolsüz Eşlik' };
  const STYLE_WHY = {
    raki: 'Rakı masası bir ritüeldir: önce mezeler, sonra deniz, en son uzun sohbet. Menünüzün her aşaması bu ritme göre kuruldu.',
    white: 'Beyaz şarabın ferah asiditesi menüdeki deniz ürünlerini ve kremalı dokuları açar; her yudum bir sonraki lokmayı tazeler.',
    red: 'Kırmızı şarabın gövdesi menünün etli, isli ve derin tabaklarıyla aynı yoğunlukta; biri diğerini büyütür.',
    rose: 'Roze, denizle eti aynı masada buluşturan en dengeli seçim; menünüzün iki ucunu birbirine bağlıyor.',
    sparkling: 'Bu akşam bir kutlama gibi başlamalı. Köpüklü, başlangıçtan tatlıya kadar her aşamaya eşlik eder.',
    cocktail: 'Kokteyller her aşamada ayrı bir sahne kurar: biri başlangıçlarla açılır, diğeri tatlıyla kapanır.',
    whisky: 'Viski acele etmeyenlerin içkisidir; güçlü ve isli tatların yanında parlar.',
    none: 'Alkolsüz eşlik: ferah, meyveli ve menünün tatlarını öne çıkaran seçimler.',
  };
  const PAIR_TEXT = {
    'ates|ates': 'İki ateş aynı masada: tempo yüksek, sohbet hararetli. Menünüzü köz, baharat ve cesur tabaklarla kurduk; birbirinizin iştahını büyüteceksiniz.',
    'toprak|toprak': 'İki toprak burcu: kaliteyi, zamanı ve emeği bilen bir masa. Menünüzde acele yok; yavaş pişmiş, köklü ve doyurucu tabaklar var.',
    'hava|hava': 'İki hava burcu: masada sohbet hiç bitmez. Menünüz paylaşılan, ferah ve sürprizli tabaklarla akıyor.',
    'su|su': 'İki su burcu: sezgisel, duygusal ve denize yakın bir masa. Menünüzü denizden gelen, yumuşak ve sarıp sarmalayan tatlarla kurduk.',
    'ates|hava': 'Hava ateşi büyütür: biriniz kıvılcımı, diğeriniz rüzgârı getiriyor. Menünüzde hareketli, paylaşılan ve hafif acılı tabaklar yan yana.',
    'su|toprak': 'Su toprağı besler: biriniz derinliği, diğeriniz sağlamlığı getiriyor. Menünüz denizle toprağı aynı masada buluşturuyor.',
    'ates|toprak': 'Ateş ile toprak: biriniz hızı, diğeriniz sabrı temsil ediyor. Menünüz közün enerjisini yavaş pişmiş tatların derinliğiyle dengeliyor.',
    'ates|su': 'Ateş ile su, zıtların çekimi. Menünüzde baharatlı ve közlü tabaklar denizin serinliğiyle dengeleniyor.',
    'hava|toprak': 'Hava ile toprak: fikirler ve gerçekler. Menünüz ferah, yaratıcı tabakları klasik ve sağlam lezzetlerle birleştiriyor.',
    'hava|su': 'Hava ile su: akıl ve sezgi. Menünüz zarif, narenciyeli ve denizden gelen tatlarla hafif bir rüya gibi ilerliyor.',
  };

  // Why a sign loves a tag. {S} sign, {R} ruler genitive
  const WHY = {
    spicy: ['{R} ateşi acıyı sever; bu tabakta tempo hiç düşmüyor.', '{SG} damağı biraz acı ister; baharat tam burada devreye giriyor.'],
    grill: ['Közün ve ateşin izi, {SG} enerjisine en çok yakışan imza.', '{R} sıcaklığı ızgarada konuşur; bu tabak doğrudan ateşten geliyor.'],
    bold: ['Net, iddialı bir tat; {S} yarım ölçüyü sevmez.', '{S} cesur tatları sever; bu tabak da kendinden emin.'],
    meat: ['{S} doyurucu ve güçlü bir merkez ister; bu tabak masanın omurgası.', '{R} gücü iyi pişmiş bir etle tamamlanır.'],
    crispy: ['Çıtır doku, {SG} hızlı zihnine eşlik eder.', 'Her lokmada ses veren bir doku; {S} için sıkıcı bir an yok.'],
    signature: ['Şefin imzası olan bu tabak, sahneyi seven {S} için seçildi.', "Mare'nin özel tarifi; {SG} ışığına yakışan bir başrol."],
    rich: ['Zengin ve dolgun; {S} lüksü tabakta da arar.', '{R} cömertliği bu tabağın dolgunluğunda.'],
    slow: ['Sabırla, yavaş pişmiş; acele etmeyen {S} için zamanın tadı.', '{S} için iyi şeyler zaman ister; bu tabak saatlerin emeği.'],
    creamy: ['Kremalı, sarıp sarmalayan bir doku; {S} için konforun tadı.', '{R} yumuşaklığı bu kadifemsi dokuda.'],
    buttery: ['Tereyağının sıcaklığı {S} için ev gibidir.', 'Tereyağıyla yuvarlanan bu tat {S} için tam bir keyif.'],
    earthy: ['Topraktan gelen derin bir tat; {S} köklerine sadıktır.', '{S} toprağın tadını tanır; bu tabak tam oradan geliyor.'],
    chocolate: ['Koyu, yoğun bir kapanış; {S} tutkusunu tatlıda da sürdürür.', '{R} gölgesi koyu çikolatada saklı.'],
    traditional: ['Köklü bir tarif; {S} için tanıdık olan en değerlisidir.', '{S} için anı taşıyan tatlar en lezzetlileridir.'],
    playful: ['Oyunbaz ve beklenmedik; {SG} merakına iyi bir cevap.', '{S} sürprizleri sever; bu tabak da tam bir sürpriz.'],
    fresh: ['Ferah ve temiz bir tat; {SG} dengesine en uygun nefes.', 'Tazeliği ilk lokmada belli; {S} için ideal bir açılış.'],
    citrus: ['Narenciyenin parlaklığı {SG} ruhunu canlandırır.', '{R} hafifliği bu canlı, ekşi dokunuşta.'],
    share: ['Ortaya konan, bölüştükçe güzelleşen bir tabak; {SG} cömertliğine göre.', '{S} için sofra paylaşınca güzelleşir.'],
    light: ['Hafif ama eksiksiz; {S} için az ve kusursuz olanı.', '{SG} damağını yormayan, dengeli bir tabak.'],
    herbal: ['Taze otların kokusu {SG} özenine yakışıyor.', 'Yeşilin ve otların dengesi; {S} için bir ayrıntı şöleni.'],
    sea: ['Denizin tuzlu, derin tadı; {S} kendini burada evinde hisseder.', '{R} çekimi denize yöneltir; bu tabak doğrudan oradan geliyor.'],
    sweet: ['Tatlı bir dokunuş; {SG} kalbini yumuşatan küçük bir an.', '{S} için tatlılık bir şefkat ifadesidir.'],
    local: ['Bu topraklardan gelen bir tat; {S} yerelin değerini bilir.', 'Yerel ve dürüst bir tabak; {SG} macera ruhuna gerçek bir durak.'],
    elegant: ['Zarif bir sunum, dengeli bir tat; {SG} estetiğine birebir.', '{R} zarafeti bu tabağın inceliğinde.'],
    fruity: ['Meyveli bir denge; {S} uyumu sever, bu tabak da tatlıyla ekşiyi buluşturuyor.', 'Beklenmedik bir meyve dokunuşu; {S} için tam bir keşif.'],
    raw: ['Çiğ ve marine; yüzeyin altını seven {S} için yoğun bir başlangıç.', '{R} gizemi saf, işlenmemiş tatlarda.'],
    smoky: ['İsli bir derinlik; {S} katmanlı tatları sever.', 'Dumanın gölgesi bu tabağa gizem katıyor; {S} için ideal.'],
    dreamy: ['Rüya gibi bir kapanış; {SG} hayal gücüne bir hediye.', '{R} hayalleri bu tatlıda vücut buluyor.'],
    nutty: ['Kuruyemişin sıcak dokusu {SG} damağına iyi gelir.', 'Fındık ve cevizin derinliği; {S} için ince bir ayrıntı.'],
  };
  const NAME_WHY = {
    su: 'denizden ve sudan gelen bu tabak adına yakışıyor', ates: 'bu tabağın ateşi adının enerjisini taşıyor',
    isik: 'bu tabağın aydınlık, ferah karakteri adınla aynı dili konuşuyor', cicek: 'bu tabağın meyveli, çiçeksi dokunuşu adına yakışıyor',
    toprak: 'topraktan gelen bu tat adının köklerine uyuyor', ruzgar: 'bu tabağın hafif ve hareketli yapısı adına benziyor',
    asil: 'şefin bu imza tabağı adının asaletine uygun', tatli: 'bu tabağın yumuşak tatlılığı adını yansıtıyor',
    derin: 'bu tabağın gizemi adına uyuyor', guc: 'bu tabağın gücü adının karakterini taşıyor', nese: 'bu tabağın neşesi adına yakışıyor',
    gok: 'bu tabağın rüya gibi hali adının gökyüzüne bakıyor', farkli: 'bu sıra dışı tabak adının anlamına birebir',
  };

  const NUM_WHY = {
    1: 'bu tabak masada ilk sözü söylüyor', 2: 'paylaşıldıkça güzelleşen bir tat', 3: 'renkli ve neşeli bir dokunuş',
    4: 'güven veren, köklü bir tarif', 5: 'menüye küçük bir macera katıyor', 6: 'zarif ve ince bir denge',
    7: 'katmanlı ve derin bir tat', 8: 'doyurucu ve güçlü bir seçim', 9: 'menünün dengesini tamamlıyor',
  };
  const FALLBACK = {
    meze: ['Rakı sofrasının klasiklerinden; masanın ritmini bu mezeler kurar.', 'Masayı açan, damağı hazırlayan bir meze; ağır tabaklardan önce iyi bir denge.', 'Sofranın sessiz kahramanı; diğer tabakların arasında köprü kurar.'],
    baslangic: ['Akşamı açan tabak; damağı uyandırır ve devamı için merak bırakır.', 'Hafif ama iddialı bir açılış; menünün tonunu belirler.'],
    ara: ['Masanın ortasına konan sıcak bir ara; sohbeti büyütür.', 'Soğuklardan ana yemeğe geçişte sıcak bir köprü.'],
    ana: ['Menünün merkezinde, içkinizle en iyi eşleşen ana yemek.', 'Akşamın doruk noktası; seçtiğimiz içkiyle tam uyumlu.'],
    tatli: ['Akşamı tatlı bir notayla kapatmak için.', 'Ağır bir akşamdan sonra dengeli bir kapanış.'],
    drink: ['Menüyle uyumlu bir eşlik.'],
  };

  // ───────────────────────────── Utilities ─────────────────────────────
  function hash(str) { let h = 2166136261; for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function rng(seed) { let a = seed >>> 0; return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const signById = (id) => SIGNS.find((s) => s.id === id);
  function signFromDate(month, day) { // month 1-12
    const md = month * 100 + day;
    if (md >= 321 && md <= 419) return 'koc'; if (md >= 420 && md <= 520) return 'boga'; if (md >= 521 && md <= 620) return 'ikizler';
    if (md >= 621 && md <= 722) return 'yengec'; if (md >= 723 && md <= 822) return 'aslan'; if (md >= 823 && md <= 922) return 'basak';
    if (md >= 923 && md <= 1022) return 'terazi'; if (md >= 1023 && md <= 1121) return 'akrep'; if (md >= 1122 && md <= 1221) return 'yay';
    if (md >= 1222 || md <= 119) return 'oglak'; if (md >= 120 && md <= 218) return 'kova'; return 'balik';
  }

  function person(p) {
    const sign = signById(p.sign);
    const ni = nameInfo(p.name);
    return { sign, name: ni.display || sign.name, first: ni.first || sign.name, gender: p.gender || null, ni };
  }
  function affinity(tags, P) {
    let s = 0;
    for (const t in tags) {
      s += tags[t] * ((P.sign.taste[t] || 0) + 0.8 * (P.ni.tags[t] || 0) + 0.5 * (P.ni.numInfo.tags[t] || 0));
    }
    return s;
  }

  // ───────────────────────────── Builder ─────────────────────────────
  const BUDGET = { single: { min: 5000, max: 6000, center: 5600 }, couple: { min: 10000, max: 12500, center: 11200 } };

  function catalog(menu) {
    const byId = {};
    (menu.items || []).forEach((it) => { if (it && it.id && it.price > 0 && !it.hidden) byId[it.id] = it; });
    return byId;
  }

  function slotsFor(mode, style) {
    const couple = mode === 'couple';
    const raki = style === 'raki', none = style === 'none';
    const S = [];
    if (couple) {
      S.push({ key: 'baslangic', label: 'Başlangıç', course: 'baslangic', min: 1, max: 2, owner: 'both' });
      S.push({ key: 'meze', label: raki ? 'Mezeler' : 'Meze ve Salata', course: 'meze', min: raki ? 3 : 2, max: raki ? 4 : 3, owner: 'both' });
      S.push({ key: 'ara', label: 'Ara Sıcak', course: 'ara', min: 1, max: 2, owner: 'both' });
      S.push({ key: 'ana0', label: 'Ana Yemek', course: 'ana', min: 1, max: 1, owner: 0 });
      S.push({ key: 'ana1', label: 'Ana Yemek', course: 'ana', min: 1, max: 1, owner: 1 });
      S.push({ key: 'tatli0', label: 'Tatlı', course: 'tatli', min: 1, max: 1, owner: 0 });
      S.push({ key: 'tatli1', label: 'Tatlı', course: 'tatli', min: 1, max: 1, owner: 1 });
      if (style === 'cocktail') S.push({ key: 'icki', label: 'Kokteyller', course: 'drink', min: 2, max: 4, owner: 'both' });
      else if (none) S.push({ key: 'icki', label: 'İçecekler', course: 'drink', min: 2, max: 4, owner: 'both', repeat: true });
      else S.push({ key: 'icki', label: STYLE_NAME[style], course: 'drink', min: 1, max: 1, owner: 'both' });
    } else {
      S.push({ key: 'baslangic', label: 'Başlangıç', course: 'baslangic', min: 1, max: 1, owner: 0 });
      S.push({ key: 'meze', label: raki ? 'Mezeler' : 'Meze ve Salata', course: 'meze', min: raki ? 2 : 1, max: raki ? 3 : 2, owner: 0 });
      S.push({ key: 'ara', label: 'Ara Sıcak', course: 'ara', min: 1, max: none ? 2 : 1, owner: 0 });
      S.push({ key: 'ana0', label: 'Ana Yemek', course: 'ana', min: 1, max: 1, owner: 0 });
      S.push({ key: 'tatli0', label: 'Tatlı', course: 'tatli', min: 1, max: 1, owner: 0 });
      if (style === 'cocktail') S.push({ key: 'icki', label: 'Kokteyller', course: 'drink', min: 1, max: 2, owner: 0 });
      else if (style === 'whisky') S.push({ key: 'icki', label: 'Viski', course: 'drink', min: 1, max: 1, owner: 0 });
      else S.push({ key: 'icki', label: none ? 'İçecekler' : STYLE_NAME[style], course: 'drink', min: 1, max: 2, owner: 0, repeat: true });
    }
    return S;
  }

  function stylesFor(mode, opts) {
    if (opts.noAlcohol) return ['none'];
    return mode === 'couple' ? ['raki', 'white', 'red', 'rose', 'sparkling', 'cocktail', 'whisky'] : ['raki', 'white', 'red', 'cocktail', 'whisky'];
  }

  function drinkPool(mode, style, byId, persons) {
    const tag = mode === 'couple' ? 'c' : 's';
    return Object.keys(DRINK).filter((k) => {
      const d = DRINK[k];
      return d.st === style && d.for.includes(tag) && byId[d.base || k];
    }).map((k) => {
      const d = DRINK[k];
      const it = byId[d.base || k];
      let fav = 0;
      if (style === 'cocktail') persons.forEach((P) => { const ix = P.sign.cocktails.indexOf(k); if (ix >= 0) fav += 3 - ix * 0.6; });
      return { id: k, menuId: d.base || k, name: d.label || it.name, price: it.price, img: it.img || null, tags: d.t, note: d.note, course: 'drink', style: d.st, fav, ing: [] };
    });
  }

  function foodPool(course, style, byId, mode) {
    return Object.keys(FOOD).filter((id) => {
      const f = FOOD[id];
      if (f.c !== course || !byId[id]) return false;
      const pr = f.p[style] == null ? 1 : f.p[style];
      if (course === 'ana' && pr < 2) return false;
      if (pr < 1) return false;
      if (f.share && mode !== 'couple') return false;
      return true;
    }).map((id) => {
      const f = FOOD[id], it = byId[id];
      return { id, menuId: id, name: it.name, price: it.price, img: it.img || null, tags: f.t, pair: f.p[style] == null ? 1 : f.p[style], ing: f.i, note: f.note, course };
    });
  }

  function solve(mode, style, persons, byId, R) {
    const slots = slotsFor(mode, style);
    const B = BUDGET[mode];
    const closer = byId[CLOSER.id];
    const closerCost = closer ? closer.price * persons.length : 0;
    const jit = {};
    const J = (id) => (jit[id] == null ? (jit[id] = R() * 3.4) : jit[id]);
    // candidate lists with per-owner scores
    const cands = slots.map((s) => {
      const pool = s.course === 'drink' ? drinkPool(mode, style, byId, persons) : foodPool(s.course, style, byId, mode);
      return pool.map((c) => {
        const owners = s.owner === 'both' ? persons : [persons[s.owner]];
        const aff = owners.reduce((a, P) => a + affinity(c.tags, P), 0) / owners.length;
        const prem = c.course === 'drink' ? 0 : Math.min(c.price, 2400) / 520;
        const base = 4 + aff / 3 + (c.pair || 0) * 1.0 + (c.fav || 0) * 1.4 + prem + J(c.id + s.key.replace(/\d/, ''));
        return Object.assign({}, c, { score: base });
      });
    });
    if (cands.some((list, i) => list.length < (slots[i].repeat ? 1 : slots[i].min))) return null;

    function evaluate(state) {
      let total = closerCost, score = 0, count = 0;
      const ingCount = {}, used = {};
      let drinkTags = {};
      state.forEach((sel, si) => {
        sel.forEach((ci, k) => {
          const c = cands[si][ci];
          total += c.price;
          score += k < slots[si].min ? c.score : c.score * 0.3; count++;
          if (c.course === 'drink') { for (const t in c.tags) drinkTags[t] = (drinkTags[t] || 0) + c.tags[t]; }
          else {
            if (used[c.id]) score -= 1e6; used[c.id] = 1;
            c.ing.forEach((g) => { ingCount[g] = (ingCount[g] || 0) + 1; });
          }
        });
      });
      for (const g in ingCount) if (ingCount[g] > 1) score -= 6 * (ingCount[g] - 1);
      // drink ↔ food chemistry
      state.forEach((sel, si) => {
        if (slots[si].course === 'drink') return;
        sel.forEach((ci) => { const c = cands[si][ci]; for (const t in c.tags) if (drinkTags[t]) score += 0.12 * c.tags[t] * Math.min(drinkTags[t], 3); });
      });
      let pen = 0;
      if (total < B.min) pen += (B.min - total) / 15;
      if (total > B.max) pen += (total - B.max) / 15;
      pen += Math.abs(total - B.center) / 220;
      return { f: score - pen, total, score, count };
    }

    function legal(state) {
      return state.every((sel, si) => sel.length >= slots[si].min && sel.length <= slots[si].max &&
        (slots[si].repeat || new Set(sel).size === sel.length));
    }

    function climb(state) {
      let cur = evaluate(state);
      for (let iter = 0; iter < 300; iter++) {
        let best = null, bestEval = cur;
        const tryState = (ns) => { if (!legal(ns)) return; const e = evaluate(ns); if (e.f > bestEval.f + 1e-9) { best = ns; bestEval = e; } };
        state.forEach((sel, si) => {
          const n = cands[si].length;
          for (let k = 0; k < sel.length; k++) {
            for (let ci = 0; ci < n; ci++) { if (ci === sel[k]) continue; const ns = state.map((x) => x.slice()); ns[si][k] = ci; tryState(ns); }
            if (sel.length > slots[si].min) { const ns = state.map((x) => x.slice()); ns[si].splice(k, 1); tryState(ns); }
          }
          if (sel.length < slots[si].max) for (let ci = 0; ci < n; ci++) { const ns = state.map((x) => x.slice()); ns[si].push(ci); tryState(ns); }
        });
        if (!best) break;
        state = best; cur = bestEval;
      }
      return { state, ev: cur };
    }

    function init(randomize) {
      return slots.map((s, si) => {
        const order = cands[si].map((c, i) => i).sort((a, b) => cands[si][b].score - cands[si][a].score);
        if (randomize) for (let i = order.length - 1; i > 0; i--) { if (R() < 0.5) { const j = Math.floor(R() * (i + 1)); [order[i], order[j]] = [order[j], order[i]]; } }
        const out = [];
        for (let k = 0; k < s.min; k++) out.push(s.repeat && order.length <= k ? order[0] : order[k % order.length]);
        return out;
      });
    }

    // Couples: the two personal mains/desserts start on different dishes
    let best = null;
    for (let r = 0; r < 4; r++) {
      const res = climb(init(r > 0));
      const ok = res.ev.total >= B.min && res.ev.total <= B.max;
      const key = (ok ? 1e6 : 0) + res.ev.f;
      if (!best || key > best.key) best = Object.assign(res, { key, ok });
    }
    return { slots, cands, closer, closerCost, best };
  }

  const fill = (tpl, P) => tpl.replace(/\{SG\}/g, P.sign.name + ' burcunun').replace(/\{S\}/g, P.sign.name + ' burcu').replace(/\{R\}/g, P.sign.rulerGen);
  function reasonFor(c, owners, usedTags, R) {
    if (c.course === 'drink') {
      const fan = owners.find((P) => P.sign.cocktails.indexOf(c.id) === 0) || owners.find((P) => P.sign.cocktails.indexOf(c.id) > 0);
      return { text: fan ? (owners.length > 1 ? fan.first + ' için: ' : '') + fan.sign.name + ' burcunun imza kokteyli.' : null, owner: fan || owners[0] };
    }
    // strongest (tag, owner, source) whose sentence hasn't been used yet in this menu
    const seen = usedTags['#tpl'] || (usedTags['#tpl'] = {});
    const opts = [];
    owners.forEach((P) => {
      for (const t in c.tags) {
        const pen = usedTags[t] ? 0.6 : 1;
        const sv = c.tags[t] * (P.sign.taste[t] || 0) * pen;
        const nv = c.tags[t] * (P.ni.tags[t] || 0) * 0.95 * pen;
        if (sv > 0) opts.push({ v: sv, t, src: 'sign', P });
        if (nv > 0 && P.ni.group) opts.push({ v: nv, t, src: 'name', P });
      }
    });
    opts.sort((a, b) => b.v - a.v);
    for (const o of opts) {
      const P = o.P;
      if (o.src === 'name') {
        if (seen['#name' + P.first]) continue;
        seen['#name' + P.first] = 1; usedTags[o.t] = (usedTags[o.t] || 0) + 1;
        const who = owners.length === 1 && P.__solo ? 'Adın' : P.first + ' adı';
        return { text: who + ' “' + P.ni.meaning + '” demek; ' + NAME_WHY[P.ni.group] + '.', owner: P, tag: o.t };
      }
      const list = WHY[o.t] || [];
      const k0 = Math.floor(R() * list.length);
      for (let k = 0; k < list.length; k++) {
        const tpl = list[(k0 + k) % list.length], key = tpl + P.sign.id;
        if (seen[key]) continue;
        seen[key] = 1; usedTags[o.t] = (usedTags[o.t] || 0) + 1;
        return { text: fill(tpl, P), owner: P, tag: o.t };
      }
    }
    const P = owners[0];
    const nt = Object.keys(P.ni.numInfo.tags).find((t) => c.tags[t]);
    if (nt && !seen['#num' + P.first]) { seen['#num' + P.first] = 1; return { text: (owners.length === 1 && P.__solo ? 'Sayın ' : P.first + ' için sayı ') + P.ni.num + ', ' + P.ni.numInfo.t.toLocaleLowerCase('tr') + ': ' + NUM_WHY[P.ni.num] + '.', owner: P }; }
    const list = FALLBACK[c.course] || FALLBACK.meze;
    for (let k = 0; k < list.length; k++) { const tpl = list[k]; if (!seen['#fb' + tpl]) { seen['#fb' + tpl] = 1; return { text: fill(tpl, P), owner: P }; } }
    return { text: null, owner: P };
  }

  /**
   * build(menu, { mode: 'single'|'couple', people: [{name, sign, gender}], noAlcohol, variant })
   */
  function build(menu, input) {
    const mode = input.mode === 'couple' ? 'couple' : 'single';
    const persons = (input.people || []).slice(0, mode === 'couple' ? 2 : 1).map(person);
    if (persons.length !== (mode === 'couple' ? 2 : 1) || persons.some((p) => !p.sign)) throw new Error('bad input');
    if (mode === 'single') persons[0].__solo = true;
    const byId = catalog(menu);
    const variant = input.variant | 0;
    const seedStr = [mode, input.noAlcohol ? 1 : 0, variant].concat(persons.map((p) => lowerTr(p.name) + '|' + p.sign.id + '|' + (p.gender || ''))).join('#');
    const styles = stylesFor(mode, input);
    const Rs = rng(hash(seedStr + '#style'));
    let pick = null;
    styles.forEach((st) => {
      const R = rng(hash(seedStr + '#' + st));
      const res = solve(mode, st, persons, byId, R);
      if (!res) return;
      const pref = persons.reduce((a, P) => a + (P.sign.drinks[st] || 0), 0) / persons.length;
      const avg = res.best.ev.score / Math.max(1, res.best.ev.count);
      const key = (res.best.ok ? 1e6 : 0) + avg * 1.5 + pref * 6 + Rs() * 5;
      if (!pick || key > pick.key) pick = { key, style: st, res };
    });
    if (!pick) throw new Error('no menu');
    const { res, style } = pick;
    const { slots, cands, best, closer } = res;
    const R = rng(hash(seedStr + '#text'));
    const usedTags = {};
    const courses = [];
    best.state.forEach((sel, si) => {
      const s = slots[si];
      const owners = s.owner === 'both' ? persons : [persons[s.owner]];
      const groupKey = s.key.replace(/\d$/, '');
      let g = courses.find((x) => x.key === groupKey);
      if (!g) { g = { key: groupKey, label: s.label, items: [] }; courses.push(g); }
      // aggregate repeats into qty
      const counts = {};
      sel.forEach((ci) => { counts[ci] = (counts[ci] || 0) + 1; });
      Object.keys(counts).forEach((ci) => {
        const c = cands[si][ci];
        const qty = counts[ci];
        const rs = reasonFor(c, owners, usedTags, R);
        g.items.push({ id: c.id, menuId: c.menuId, name: c.name, price: c.price, qty, img: c.img, note: c.note,
          why: rs.text, forName: s.owner === 'both' ? null : persons[s.owner].first, forSign: s.owner === 'both' ? null : persons[s.owner].sign.id });
      });
    });
    // couple: single label for personal courses
    courses.forEach((g) => { if (g.key === 'ana' && g.items.length > 1) g.label = 'Ana Yemekler'; if (g.key === 'tatli' && g.items.length > 1) g.label = 'Tatlılar'; });
    if (style === 'cocktail') {
      const ck = courses.find((g) => g.key === 'icki');
      if (ck && ck.items.length === 1 && ck.items[0].qty === 1) ck.label = 'Kokteyl';
    }
    if (closer) courses.push({ key: 'kapanis', label: 'Kapanış', items: [{ id: CLOSER.id, menuId: CLOSER.id, name: closer.name, price: closer.price, qty: persons.length, img: null, note: CLOSER.note, why: null }] });

    const total = courses.reduce((a, g) => a + g.items.reduce((b, it) => b + it.price * it.qty, 0), 0);
    const code = 'YM-' + (hash(courses.map((g) => g.items.map((i) => i.id + i.qty).join(',')).join('|')) % 46656).toString(36).toUpperCase().padStart(3, '0') + persons.map((p) => p.sign.name.charAt(0).toLocaleUpperCase('tr')).join('');

    // reading
    const reading = persons.map((P) => ({
      name: P.name, first: P.first, sign: P.sign.id, signName: P.sign.name, el: EL[P.sign.el], ruler: P.sign.ruler, dates: P.sign.dates,
      intro: P.gender === 'f' ? P.sign.f : P.gender === 'm' ? P.sign.m : null,
      palate: P.sign.palate, meaning: P.ni.meaning, num: P.ni.num, numTitle: P.ni.numInfo.t, numText: P.ni.numInfo.s,
    }));
    let pairText = null;
    if (mode === 'couple') {
      const k = [persons[0].sign.el, persons[1].sign.el].sort().join('|');
      pairText = PAIR_TEXT[k];
      if (persons[0].sign.id === persons[1].sign.id) pairText = 'İki ' + persons[0].sign.name + ' aynı masada: aynı dili konuşan iki damak. ' + pairText;
    }
    return {
      mode, style, styleName: STYLE_NAME[style], styleWhy: STYLE_WHY[style], courses, total, code, reading, pairText,
      ok: best.ok, budget: BUDGET[mode],
    };
  }

  const api = { SIGNS, STARS, EL, build, nameInfo, signFromDate, cleanName, gen, BUDGET, FOOD, DRINK };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.YildizEngine = api;
})(typeof window !== 'undefined' ? window : globalThis);
