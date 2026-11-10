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
  const letterVal = (ch) => { const i = ALPHA.indexOf(ch); if (i >= 0) return (i % 9) + 1; return ch === 'w' ? 5 : ch === 'x' ? 6 : ch === 'q' ? 8 : 0; };
  function numerology(lower) {
    let sum = 0;
    for (const ch of lower) sum += letterVal(ch);
    const total = sum;
    while (sum > 9) sum = String(sum).split('').reduce((a, b) => a + Number(b), 0);
    return { n: sum || 9, total };
  }
  const lowerTr = (s) => String(s || '').toLocaleLowerCase('tr');
  function cleanName(raw) {
    const s = String(raw || '').replace(/[^\p{L}\s'-]/gu, ' ').replace(/\s+/g, ' ').trim().slice(0, 40);
    return s.split(' ').filter(Boolean).map((w) => w.charAt(0).toLocaleUpperCase('tr') + w.slice(1).toLocaleLowerCase('tr')).join(' ');
  }
  function nameInfo(raw) {
    const display = cleanName(raw);
    const first = lowerTr(display.split(' ')[0] || '');
    const ext = root.YildizNames ? root.YildizNames.lookup(first) : null;
    const hit = ext && ext.meaning ? [ext.meaning, ext.group] : NAMES[first] || NAMES_FOLD[fold(first)] || (ext ? [null, ext.group] : null);
    const flat = lowerTr(display.replace(/\s/g, ''));
    const nr = numerology(flat), n = nr.n;
    const digits = Array.from(flat).map((ch) => ({ ch: ch.toLocaleUpperCase('tr'), v: letterVal(ch) })).filter((d) => d.v);
    return { display, first: display.split(' ')[0] || '', meaning: hit ? hit[0] : null, group: hit ? hit[1] : null,
      tags: hit ? NAME_GROUP[hit[1]] : {}, num: n, numTotal: nr.total, digits, multi: display.split(' ').length > 1, numInfo: NUM[n] };
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
    'roka-salatasi': { c: 'meze', sal: 1, t: { fresh: 3, herbal: 2, light: 2, bold: 1 }, p: P(2, 3, 2, 2, 2, 2, 1, 3), i: ['roka'], note: 'Roka, küp domates, parmesan ve sarımsaklı nar ekşili sos' },
    'semizotu-salatasi': { c: 'meze', sal: 1, t: { fruity: 3, fresh: 2, playful: 2, local: 1, nutty: 1 }, p: P(2, 3, 1, 3, 2, 2, 0, 3), i: ['semizotu'], note: 'Çilek, ceviz, Erzincan tulumu ve nar ekşisiyle semizotu' },
    'komsu-salata': { c: 'meze', sal: 1, t: { fresh: 3, traditional: 2, local: 2, light: 2 }, p: P(3, 2, 2, 2, 1, 1, 0, 3), i: ['komsu', 'ezine'], note: 'Domates, salatalık, zeytin ve ezine peyniriyle limonlu komşu salata' },
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
  // drinks without a menu photo get a serving shot in the menu style (no brand labels)
  const DRINK_IMG = { 'whisky-s': 'yz-viski-duble.webp', 'whisky-c': 'yz-viski-sise.webp', 'cocktail-s': 'yz-kokteyl.webp', 'none-s': 'yz-alkolsuz.webp', 'raki-s': 'yz-raki-duble.webp', 'raki-c': 'yz-raki-sise.webp', 'white-s': 'yz-beyaz-kadeh.webp', 'white-c': 'yz-beyaz-sise.webp', 'red-s': 'yz-kirmizi-kadeh.webp', 'red-c': 'yz-kirmizi-sise.webp', 'rose-c': 'yz-roze-sise.webp', 'sparkling-c': 'yz-kopuklu-sise.webp' };
  const CLOSER = { id: 'turk-kahvesi', img: 'turk-kahvesi-2026.webp', note: 'Bizden ikram. Fincanı kapatın: gökyüzü söyledi, gerisini kahve söylesin' };

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
    meze: ['Rakı sofrasının klasiklerinden; masanın ritmini bu mezeler kurar.', 'Masayı açan, damağı hazırlayan bir meze; ağır tabaklardan önce iyi bir denge.', 'Sofranın sessiz kahramanı; diğer tabakların arasında köprü kurar.', 'Renkleri ve dokusuyla masaya canlılık katan, paylaşılmaya hazır bir tabak.', 'Mezeler arasında dengeyi kuran, damağı dinlendiren bir seçim.', 'Zeytinyağının ve sebzenin sade gücü; menünün nefes aldığı an.', 'Küçük ama karakterli; her lokmada ayrı bir tat bırakır.'],
    baslangic: ['Akşamı açan tabak; damağı uyandırır ve devamı için merak bırakır.', 'Hafif ama iddialı bir açılış; menünün tonunu belirler.'],
    ara: ['Masanın ortasına konan sıcak bir ara; sohbeti büyütür.', 'Soğuklardan ana yemeğe geçişte sıcak bir köprü.'],
    ana: ['Menünün merkezinde, içkinizle en iyi eşleşen ana yemek.', 'Akşamın doruk noktası; seçtiğimiz içkiyle tam uyumlu.'],
    tatli: ['Akşamı tatlı bir notayla kapatmak için.', 'Ağır bir akşamdan sonra dengeli bir kapanış.'],
    drink: ['Menüyle uyumlu bir eşlik.'],
  };

  // ───────────────────────────── Lux tone (no astrology on screen) ─────────────────────────────
  const PERSONA = {
    koc: ['Cesur Damak', 'Net, iddialı ve sıcak tatları seversiniz; közün ve baharatın enerjisi sizi masaya bağlar.'],
    boga: ['Keyif Ustası', 'Lezzeti acele etmeden yaşarsınız; tereyağı, yavaş pişmiş et ve iyi bir tatlı sizin için akşamın özüdür.'],
    ikizler: ['Meraklı Kâşif', 'Tek tabakla yetinmezsiniz; çıtır dokular, narenciye ve paylaşılan küçük tabaklar sizi mutlu eder.'],
    yengec: ['Sofra Ruhu', 'Tanıdık tatlarda huzur bulursunuz; deniz, geleneksel tarifler ve sarıp sarmalayan dokular sizin alanınız.'],
    aslan: ['İmza Avcısı', 'Şefin imza tabaklarına, cömert ve etkileyici sunumlara yönelirsiniz; sıradan bir tabak size yakışmaz.'],
    basak: ['İnce Damak', 'Ayrıntıyı fark edersiniz; taze otlar, zeytinyağı ve dengeli, hafif tabaklar size göre.'],
    terazi: ['Zarafet Tutkunu', 'Tatlı ile ekşinin dengelendiği, göze de hitap eden zarif tabakları seversiniz.'],
    akrep: ['Yoğunluk Arayan', 'Marine ve çiğ tatlar, isli aromalar ve güçlü kontrastlar sizi çeker; orta yol size göre değil.'],
    yay: ['Sofra Gezgini', 'Cömert, paylaşılan masalar, baharat ve yerel lezzetler sizin keyfiniz.'],
    oglak: ['Klasik Tutkunu', 'Zamanın sınadığı tariflere, yavaş pişmiş etlere ve olgun lezzetlere değer verirsiniz.'],
    kova: ['Özgün Seçici', 'Beklenmedik eşleşmeleri, meyveli ve ekşi dokunuşları, modern tabakları seversiniz.'],
    balik: ['Deniz Romantiği', 'Denizden gelen, yumuşak ve kremalı tatlar; narenciye ve hafif bir kapanış size iyi gelir.'],
  };
  const LUX_WHY = {
    spicy: ['Baharatın sıcaklığı, net tatları seven damak profilinizle örtüşüyor.', 'Ölçülü bir acı, akşamın temposunu yükseltiyor.'],
    grill: ['Közün izi, bu tabağı menünün en karakterli anlarından biri yapıyor.', 'Ateşte pişmenin dumanlı derinliği damak profilinize karşılık veriyor.'],
    bold: ['İddialı ve net bir tat; yarım ölçüyü sevmeyen damaklar için.', 'Kendinden emin bir tabak; menüye güçlü bir vurgu katıyor.'],
    meat: ['Menünün omurgası: doyurucu ve güçlü bir merkez.', 'İyi pişmiş et, damak profilinizdeki güç tarafına karşılık veriyor.'],
    crispy: ['Çıtır dokusu her lokmaya canlılık katıyor.', 'Doku oyunu sevenler için; hafif ve hareketli.'],
    signature: ['Şefimizin imza tabaklarından; Mare mutfağını en iyi anlatanlardan biri.', 'Mare’nin özel tarifi; menünün başrolü.'],
    rich: ['Zengin ve dolgun; konforlu bir lüks.', 'Dolgun yapısı akşamı uzun ve keyifli kılıyor.'],
    slow: ['Sabırla, saatlerce pişmiş; zamanın tadı.', 'Yavaş pişirmenin derinliği damakta uzun kalıyor.'],
    creamy: ['Kadifemsi, sarıp sarmalayan bir doku.', 'Kremalı dokusu menüye yumuşak bir geçiş sağlıyor.'],
    buttery: ['Tereyağının sıcaklığı tabağı yuvarlıyor.', 'Tereyağıyla bağlanan bu tat, damak profilinizdeki konfor arayışına uyuyor.'],
    earthy: ['Topraktan gelen derin bir tat.', 'Sebzenin ve toprağın sade gücü.'],
    chocolate: ['Koyu ve yoğun bir kapanış.', 'Çikolatanın derinliği akşamı imzalıyor.'],
    traditional: ['Köklü bir tarif; tanıdık olanın en iyisi.', 'Anadolu mutfağından gelen, güven veren bir klasik.'],
    playful: ['Oyunbaz ve beklenmedik; merakı besleyen bir tabak.', 'Menüye küçük bir sürpriz katıyor.'],
    fresh: ['Ferah ve temiz; damağı açan bir nefes.', 'Tazeliğiyle menünün ağır tabaklarını dengeliyor.'],
    citrus: ['Narenciyenin parlaklığı tadı canlandırıyor.', 'Ekşi ve canlı bir dokunuş; damağı her lokmada tazeliyor.'],
    share: ['Ortaya konan, bölüştükçe güzelleşen bir tabak.', 'Paylaşmak için tasarlanmış; masayı bir araya getiriyor.'],
    light: ['Hafif ama eksiksiz; az ve kusursuz.', 'Damağı yormayan, dengeli bir seçim.'],
    herbal: ['Taze otların kokusu tabağa incelik katıyor.', 'Yeşilin dengesi; ayrıntıyı sevenler için.'],
    sea: ['Denizin tuzlu, derin tadı; Mare’nin özü.', 'Ege kıyılarından ilham alan bir deniz lezzeti.'],
    sweet: ['Tatlı bir dokunuş; akşamı yumuşatan küçük bir an.', 'Ölçülü bir tatlılık, menüye denge katıyor.'],
    local: ['Bu topraklardan gelen dürüst bir lezzet.', 'Yerel mutfağın karakterini taşıyan bir tabak.'],
    elegant: ['Zarif bir sunum, dengeli bir tat.', 'İnce işçiliğiyle menünün en şık anlarından.'],
    fruity: ['Meyveli bir denge; tatlı ile ekşiyi buluşturuyor.', 'Beklenmedik bir meyve dokunuşu.'],
    raw: ['Çiğ ve marine; saf ve yoğun bir açılış.', 'Ürünün kendi tadını en saf haliyle gösteriyor.'],
    smoky: ['İsli bir derinlik, katmanlı bir tat.', 'Dumanın gölgesi tabağa karakter katıyor.'],
    dreamy: ['Akşamı imzalayan, unutulmayacak bir kapanış.', 'Hafif ve etkileyici bir final.'],
    nutty: ['Kuruyemişin sıcak dokusu ince bir ayrıntı.', 'Fındık ve cevizin derinliği tabağı tamamlıyor.'],
  };
  const LUX_NAME_WHY = {
    su: 'denizden gelen bu tabak adınıza yakışıyor', ates: 'bu tabağın sıcaklığı adınızın enerjisini taşıyor', isik: 'bu tabağın aydınlık, ferah karakteri adınızla aynı dili konuşuyor',
    cicek: 'bu tabağın zarif dokunuşu adınıza yakışıyor', toprak: 'topraktan gelen bu tat adınızın köklerine uyuyor', ruzgar: 'bu tabağın hafif ve hareketli yapısı adınıza benziyor',
    asil: 'şefin bu imza tabağı adınızın asaletine uygun', tatli: 'bu tabağın yumuşaklığı adınızı yansıtıyor', derin: 'bu tabağın derinliği adınıza uyuyor',
    guc: 'bu tabağın gücü adınızın karakterini taşıyor', nese: 'bu tabağın neşesi adınıza yakışıyor', gok: 'bu tabağın inceliği adınızın anlamına uyuyor', farkli: 'bu sıra dışı tabak adınızın anlamına birebir',
  };
  const AXIS_LIKES = { deniz: 'denizi', ates: 'közü ve baharatı', toprak: 'köklü tatları', ferah: 'ferah ve yeşil tatları', kadife: 'kremalı ve tatlı dokuları', merak: 'sürprizli tabakları' };
  const LUX_AXIS_TOP = {
    deniz: 'Damak profilinizin merkezinde deniz var; tuzlu, iyot kokulu tatlar sizi en çok mutlu ediyor.',
    ates: 'Közün dumanı ve baharatın sıcaklığı öne çıkıyor; net ve iddialı tatlar sizin alanınız.',
    toprak: 'Köklü, sabırla pişmiş tatlar size iyi geliyor; tanıdık olanın en iyisini arıyorsunuz.',
    ferah: 'Ferah, yeşil ve narenciyeli tatlar enerjinizi tazeliyor; hafiflik sizin için bir lüks.',
    kadife: 'Yumuşak, kremalı ve tatlı dokular konfor alanınız; iyi bir kapanış sizin için şart.',
    merak: 'Sürprizli ve gösterişli tabaklar merakınızı besliyor; sıradan olan sizi sıkıyor.',
  };
  const LUX_AXIS_LOW = {
    deniz: 'Deniz ürünleri sizin için küçük bir keşif; menüde ölçülü yer aldı.', ates: 'Acı ve köz ilk tercihiniz değil; menüde dengeli tutuldu.',
    toprak: 'Ağır ve köklü tatlar yerine daha hafif bir ritim size iyi geliyor.', ferah: 'Ferah tatlar sizin için bir mola; menünün dengesini onlar kuruyor.',
    kadife: 'Tatlı ve kremalı olan sizi yormamalı; kapanış ölçülü seçildi.', merak: 'Gösterişten çok özü seviyorsunuz; menü sade ve net kuruldu.',
  };
  function luxMatch(A, B, pa, pb) {
    const diff = pa.reduce((s, a, i) => s + Math.abs(a.v - pb[i].v), 0) / pa.length;
    const score = Math.round(Math.max(72, Math.min(96, 97 - diff * 0.45)));
    const ta = pa.slice().sort((x, y) => y.v - x.v), tb = pb.slice().sort((x, y) => y.v - x.v);
    const shared = ta.slice(0, 2).find((a) => tb.slice(0, 2).some((b) => b.id === a.id));
    const band = score >= 90 ? 'Neredeyse aynı dili konuşan iki damak.' : score >= 84 ? 'Birbirini tamamlayan iki damak.' : 'Farklılıkların zenginleştirdiği bir masa.';
    const ka = pa.find((x) => x.id === 'kadife').v, kb = pb.find((x) => x.id === 'kadife').v;
    return {
      score, band,
      insights: [
        { k: 'Ortak noktanız', v: shared ? 'İkiniz de ' + AXIS_LIKES[shared.id] + ' seviyorsunuz; menünün omurgasını bu kurdu.' : 'Damaklarınız farklı yönlere bakıyor; menü ikisini de ağırlayacak şekilde kuruldu.' },
        { k: 'Farkınız', v: A.first + ' ' + AXIS_LIKES[ta[0].id] + ', ' + B.first + ' ' + AXIS_LIKES[tb[0].id] + ' öne çıkarıyor.' },
        { k: 'Tatlı anı', v: ka === kb ? 'Tatlıya ikiniz de aynı hevesle bakıyorsunuz; bu yüzden iki ayrı tatlı seçtik.' : (ka > kb ? A.first : B.first) + ' tatlıyı ilk ister, son lokmayı ' + (ka > kb ? B.first : A.first) + ' alır.' },
      ],
    };
  }

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
  const DAYS_IN = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  const validDate = (m, d) => m >= 1 && m <= 12 && d >= 1 && d <= DAYS_IN[m - 1];

  // Sky details: decans (triplicity), cusps, modality
  const START = { koc: [3, 21], boga: [4, 20], ikizler: [5, 21], yengec: [6, 21], aslan: [7, 23], basak: [8, 23], terazi: [9, 23], akrep: [10, 23], yay: [11, 22], oglak: [12, 22], kova: [1, 20], balik: [2, 19] };
  const ORDER = ['koc', 'boga', 'ikizler', 'yengec', 'aslan', 'basak', 'terazi', 'akrep', 'yay', 'oglak', 'kova', 'balik'];
  const TRIP = { ates: ['koc', 'aslan', 'yay'], toprak: ['boga', 'basak', 'oglak'], hava: ['ikizler', 'terazi', 'kova'], su: ['yengec', 'akrep', 'balik'] };
  const MOD = { koc: 'Öncü', yengec: 'Öncü', terazi: 'Öncü', oglak: 'Öncü', boga: 'Sabit', aslan: 'Sabit', akrep: 'Sabit', kova: 'Sabit', ikizler: 'Değişken', basak: 'Değişken', yay: 'Değişken', balik: 'Değişken' };
  const doy = (m, d) => Math.round((Date.UTC(2001, m - 1, d) - Date.UTC(2001, 0, 1)) / 864e5);
  function astroFromDate(m, d) {
    if (m === 2 && d === 29) d = 28;
    const id = signFromDate(m, d);
    let off = doy(m, d) - doy(START[id][0], START[id][1]); if (off < 0) off += 365;
    const i = ORDER.indexOf(id), next = ORDER[(i + 1) % 12], prev = ORDER[(i + 11) % 12];
    let toNext = doy(START[next][0], START[next][1]) - doy(m, d); if (toNext <= 0) toNext += 365;
    return { id, decan: off < 10 ? 1 : off < 20 ? 2 : 3, cusp: off <= 1 ? prev : toNext <= 2 ? next : null };
  }

  // Diet flags per dish: s seafood, r red meat, o offal, w raw, h spicy
  const FLAGS = {
    'kereviz-pureli-jumbo-karides-sogus': 's', 'dana-carpaccio': 'rw', 'somon-tartar': 'sw', 'palamut-carpaccio': 'sw',
    'patates-cipsli-acili-atom': 'h', '3-lu-deniz-mahsulu-lezzeti': 's', 'mare-spesiyal-ahtapot-guvec': 's', 'mare-spesiyal-islama-kalamar': 's',
    'jumbo-karides-izgara': 's', 'kalamar-tava': 's', 'yaprak-ciger': 'ro', 'patates-terin': 'r', 'tereyagli-karides': 's',
    'biber-kremali-bonfile': 'r', 'citir-somon': 's', 'deniz-mahsulleri-bugday-risotto': 's', 'firinda-kremali-levrek': 's', 'mare-spesiyal-granyoz': 's',
    'kuzu-pirzola': 'r', 'balkabagi-soslu-kestane-dolgulu-makarna': 'r', 'palamut-izgara-kofte': 's', 'kuzu-kokorec': 'roh', 'mezgit-tempura': 's', 'incik-ruyasi': 'r',
  };
  const DIETS = {
    noSea: { f: 's', label: 'Deniz ürünü yok' }, noRed: { f: 'r', label: 'Kırmızı et yok' }, noOffal: { f: 'o', label: 'Sakatat yok' },
    noRaw: { f: 'w', label: 'Çiğ yok' }, noSpicy: { f: 'h', label: 'Acısız' }, veg: { f: 'sro', label: 'Vejetaryen' },
  };
  function dietMask(diet) { let m = ''; (diet || []).forEach((k) => { if (DIETS[k]) m += DIETS[k].f; }); return m; }
  const allowed = (id, mask) => { const f = FLAGS[id] || ''; for (const ch of f) if (mask.includes(ch)) return false; return true; };

  // Names shown on shareable images must be names
  const BAD_SUB = ['orospu', 'yarrak', 'siktir', 'sikis', 'amcik', 'pezeven', 'kahpe', 'gavat', 'yavsak', 'serefsiz', 'ibne', 'gerizekali', 'fuck', 'shit', 'bitch', 'porno', 'kaltak', 'surtuk', 'dalyarak', 'amina koy', 'aminakoy'];
  const BAD_WORD = ['amk', 'aq', 'oc', 'got', 'sik', 'am', 'pic', 'salak', 'aptal', 'mal', 'dangalak', 'it', 'esek', 'eşek', 'kopek', 'domuz', 'test', 'deneme', 'asd', 'asdf', 'qwe', 'xxx'];
  function nameOk(raw) {
    const d = cleanName(raw);
    const f = fold(lowerTr(d));
    const flat = f.replace(/\s/g, '');
    if (flat.length < 2 || flat.length > 30) return false;
    if (/(.)\1\1/.test(flat)) return false;
    if (BAD_SUB.some((b) => flat.includes(b.replace(/\s/g, '')))) return false;
    if (f.split(' ').some((w) => BAD_WORD.includes(w))) return false;
    return true;
  }

  function person(p) {
    let id = p.sign, decan = null, cuspId = null, birth = null;
    if (p.month && p.day && validDate(+p.month, +p.day)) {
      const a = astroFromDate(+p.month, +p.day); id = a.id; decan = a.decan; cuspId = a.cusp; birth = { d: +p.day, m: +p.month };
    }
    const sign = signById(id);
    if (!sign) return { sign: null };
    const ni = nameInfo(p.name);
    const tri = TRIP[sign.el];
    const co = decan ? signById(tri[(tri.indexOf(sign.id) + decan - 1) % 3]) : null;
    const cusp = cuspId ? signById(cuspId) : null;
    const extra = {}, extraSrc = {};
    if (co && co.id !== sign.id) for (const t in co.taste) { extra[t] = (extra[t] || 0) + co.taste[t] * 0.45; extraSrc[t] = 'co'; }
    if (cusp) for (const t in cusp.taste) { extra[t] = (extra[t] || 0) + cusp.taste[t] * 0.3; if (!extraSrc[t]) extraSrc[t] = 'cusp'; }
    return { sign, name: ni.display || sign.name, first: ni.first || sign.name, gender: p.gender || null, ni, decan, co, cusp, extra, extraSrc, birth };
  }
  function affinity(tags, P) {
    let s = 0;
    for (const t in tags) s += tags[t] * ((P.sign.taste[t] || 0) + (P.extra[t] || 0) + 0.8 * (P.ni.tags[t] || 0) + 0.5 * (P.ni.numInfo.tags[t] || 0));
    return s;
  }

  // ───────────────────────────── Analysis ─────────────────────────────
  const AXES = [
    { id: 'deniz', label: 'Deniz', tags: ['sea', 'raw'] },
    { id: 'ates', label: 'Ateş ve köz', tags: ['spicy', 'grill', 'bold', 'smoky'] },
    { id: 'toprak', label: 'Toprak ve gelenek', tags: ['earthy', 'traditional', 'slow', 'local', 'meat'] },
    { id: 'ferah', label: 'Ferahlık', tags: ['fresh', 'citrus', 'herbal', 'light', 'fruity'] },
    { id: 'kadife', label: 'Kadife ve tatlı', tags: ['creamy', 'buttery', 'rich', 'sweet', 'chocolate', 'dreamy'] },
    { id: 'merak', label: 'Merak ve gösteriş', tags: ['playful', 'crispy', 'share', 'signature', 'elegant'] },
  ];
  const AXIS_TOP = {
    deniz: 'Damağının pusulası denizi gösteriyor; tuzlu, iyot kokulu tatlar seni en çok mutlu eder.',
    ates: 'Közün dumanı ve baharatın sıcaklığı seni çağırıyor; net ve iddialı tatlar senin alanın.',
    toprak: 'Köklü, sabırla pişmiş tatlar sana iyi gelir; tanıdık olanın en iyisini ararsın.',
    ferah: 'Ferah, yeşil ve narenciyeli tatlar enerjini tazeler; hafiflik senin için bir lüks.',
    kadife: 'Yumuşak, kremalı ve tatlı dokular senin konfor alanın; iyi bir kapanış senin için şart.',
    merak: 'Sürprizli ve gösterişli tabaklar merakını besler; masada sıradan olan seni sıkar.',
  };
  const AXIS_LOW = {
    deniz: 'Denizden gelen tatlar senin için küçük bir keşif; menüde ölçülü bir dokunuş var.',
    ates: 'Acı ve köz ilk tercihin değil; menüde bu taraf dengeli tutuldu.',
    toprak: 'Ağır ve köklü tatlar yerine daha hafif bir ritim sana iyi gelir.',
    ferah: 'Ferah tatlar senin için bir mola; menünün dengesini onlar kuruyor.',
    kadife: 'Tatlı ve kremalı olan seni yormamalı; kapanış bu yüzden ölçülü.',
    merak: 'Gösterişten çok özü seversin; menü sade ve net kuruldu.',
  };
  function profile(P) {
    const raw = AXES.map((a) => a.tags.reduce((s, t) => s + (P.sign.taste[t] || 0) + (P.extra[t] || 0) + 0.8 * (P.ni.tags[t] || 0) + 0.5 * (P.ni.numInfo.tags[t] || 0), 0) / Math.sqrt(a.tags.length));
    const mx = Math.max.apply(null, raw), mn = Math.min.apply(null, raw);
    return AXES.map((a, i) => ({ id: a.id, label: a.label, v: Math.round(34 + 62 * (raw[i] - mn) / ((mx - mn) || 1)) }));
  }
  function decanText(P) {
    if (!P.decan) return null;
    if (P.decan === 1 || !P.co || P.co.id === P.sign.id) return P.sign.name + ' burcunun 1. dekanındasın: saf ' + P.sign.name + '. ' + P.sign.rulerGen + ' etkisi en güçlü halinde; burcunun özelliklerini en net taşıyanlardansın.';
    return P.sign.name + ' burcunun ' + P.decan + '. dekanındasın: ' + P.co.name + ' etkisi. ' + P.sign.name + ' enerjine ' + gen(P.co.name) + ' ' + P.co.key + ' duygusu karışıyor; menünde bu ikinci sesin de izi var.';
  }
  function cuspText(P) {
    if (!P.cusp) return null;
    const a = ORDER.indexOf(P.sign.id), b = ORDER.indexOf(P.cusp.id);
    const first = (b === (a + 1) % 12) ? P.sign : P.cusp, second = first === P.sign ? P.cusp : P.sign;
    return 'Doğum günün ' + first.name + '–' + second.name + ' geçişine çok yakın; iki burcun izini birlikte taşıyorsun. Menünde ' + gen(P.cusp.name) + ' damağından da bir dokunuş var.';
  }
  const EL_SCORE = { 'ates|ates': 86, 'toprak|toprak': 88, 'hava|hava': 84, 'su|su': 90, 'ates|hava': 93, 'su|toprak': 92, 'ates|toprak': 71, 'ates|su': 68, 'hava|toprak': 70, 'hava|su': 74 };
  function compat(A, B, profA, profB) {
    let s = EL_SCORE[[A.sign.el, B.sign.el].sort().join('|')];
    const ma = MOD[A.sign.id], mb = MOD[B.sign.id];
    s += ma === mb ? -3 : 3;
    if (A.sign.ruler === B.sign.ruler) s += 3;
    if ((A.ni.num + B.ni.num) % 3 === 0) s += 2;
    s = Math.max(61, Math.min(97, s));
    const band = s >= 90 ? 'Gökyüzünde nadir görülen bir uyum.' : s >= 80 ? 'Birbirini tamamlayan bir uyum.' : s >= 70 ? 'Farklılıkların tat kattığı bir uyum.' : 'Zıtların çekimi: bu masada kimse sıkılmaz.';
    let lead;
    if (ma === 'Öncü' && mb !== 'Öncü') lead = A.first + ' seçer, ' + B.first + ' onaylar. Öncü burçlar masada ilk sözü söyler.';
    else if (mb === 'Öncü' && ma !== 'Öncü') lead = B.first + ' seçer, ' + A.first + ' onaylar. Öncü burçlar masada ilk sözü söyler.';
    else if (ma === 'Öncü') lead = 'İkiniz de ilk sözü söylemek istersiniz; menüyü bu yüzden yıldızlar seçti.';
    else if (ma === 'Sabit' && mb === 'Sabit') lead = 'İkiniz de sevdiğinden kolay vazgeçmezsiniz; menüde ikinizin de favorisi var.';
    else lead = 'Kararı birbirinize bırakırsınız; menüyü bu yüzden yıldızlar seçti.';
    const ka = profA.find((x) => x.id === 'kadife').v, kb = profB.find((x) => x.id === 'kadife').v;
    const sweet = ka === kb ? 'Tatlıyı ikiniz de aynı anda istersiniz; bu yüzden iki ayrı tatlı seçtik.' : (ka > kb ? A.first : B.first) + ' tatlıyı ilk ister, son lokmayı ' + (ka > kb ? B.first : A.first) + ' alır.';
    const els = [A.sign.el, B.sign.el];
    const rhythm = els.includes('ates') && els.includes('su') ? 'Biri hızlandırır, diğeri yavaşlatır; akşamın temposu kendiliğinden dengelenir.'
      : els.includes('ates') ? 'Masada tempo yüksek; ilk tabaklar çabuk biter, sohbet hızlı akar.'
      : els.includes('su') ? 'Sohbet derinleşir, akşam uzar; menü bu yüzden acele ettirmeyen bir sırayla kuruldu.'
      : els.includes('hava') ? 'Konudan konuya geçen, paylaşılan tabaklarla büyüyen bir akşam.'
      : 'Sakin, kaliteli ve uzun bir akşam; her aşamanın tadını çıkarırsınız.';
    return { score: s, band, insights: [{ k: 'Menüyü kim seçer?', v: lead }, { k: 'Tatlıyı kim ister?', v: sweet }, { k: 'Masanın ritmi', v: rhythm }] };
  }
  function pairLine(style, c) {
    const t = c.tags || {};
    switch (style) {
      case 'raki': return t.sea ? 'Rakının anasonu denizin tuzuyla en eski dostluğu kurar.' : 'Rakının anasonu bu tabağın yağını ve baharatını dengeler.';
      case 'white': return t.creamy || t.buttery ? 'Beyazın canlı asiditesi kremayı hafifletir, her lokmayı tazeler.' : 'Beyaz şarap bu tabağın tazeliğini öne çıkarır.';
      case 'red': return t.meat ? 'Kırmızının taneni etin yağını dengeler; tat damakta daha uzun kalır.' : 'Kırmızının gövdesi bu tabağın derinliğine eşlik eder.';
      case 'rose': return 'Roze bu tabağın hem tazeliğine hem gövdesine eşlik eder.';
      case 'sparkling': return 'Köpüklünün kabarcıkları damağı temizler; her lokma ilk lokma gibi olur.';
      case 'cocktail': return 'Kokteylin ekşi ve canlı yapısı tabağın tadını açar.';
      case 'whisky': return t.smoky || t.meat ? 'Viskinin isli notası bu tabakla aynı dilden konuşur.' : 'Viski bu tabağın gücüne yavaş yavaş eşlik eder.';
      default: return 'Ferah eşlik, tabağın tadını öne çıkarır.';
    }
  }

  // ───────────────────────────── Builder ─────────────────────────────
  const BUDGET = { single: { min: 4000, max: 6000, center: 5000 }, couple: { min: 8000, max: 12000, center: 10000 } };
  const BUDGET_LUX = { single: { min: 5000, max: 6000, center: 5600 }, couple: { min: 10000, max: 12500, center: 11200 } };

  function catalog(menu) {
    const byId = {};
    (menu.items || []).forEach((it) => { if (it && it.id && it.price > 0 && !it.hidden) byId[it.id] = it; });
    return byId;
  }

  // a realistic dinner: single = starter/salad/main/dessert (rakı table: mezes + hot starter); couple shares the cold side, main and dessert are personal
  // one drink per guest: a single glass for one, a bottle or one glass each for two
  function servingsFor(mode, st) { if (mode === 'couple') return (st === 'cocktail' || st === 'none' || st === 'whisky') ? 2 : 1; return 1; }
  function slotsYz(mode, style) {
    const raki = style === 'raki', S = [], n = servingsFor(mode, style);
    const drink = { key: 'icki', label: style === 'none' ? 'İçecek' : 'İçki', course: 'drink', min: n, max: n, owner: mode === 'couple' ? 'both' : 0, repeat: true, same: true };
    if (mode === 'couple') {
      S.push({ key: 'baslangic', label: 'Başlangıç', course: 'baslangic', min: 1, max: 1, owner: 'both' });
      S.push({ key: 'meze', label: raki ? 'Mezeler' : 'Meze', course: 'meze', min: raki ? 2 : 1, max: raki ? 3 : 1, owner: 'both' });
      S.push({ key: 'salata', label: 'Salata', course: 'salata', min: 1, max: 1, owner: 'both' });
      S.push({ key: 'ara', label: 'Ara Sıcak', course: 'ara', min: 1, max: 1, owner: 'both' });
      S.push({ key: 'ana0', label: 'Ana Yemek', course: 'ana', min: 1, max: 1, owner: 0 });
      S.push({ key: 'ana1', label: 'Ana Yemek', course: 'ana', min: 1, max: 1, owner: 1 });
      S.push({ key: 'tatli0', label: 'Tatlı', course: 'tatli', min: 1, max: 1, owner: 0 });
      S.push({ key: 'tatli1', label: 'Tatlı', course: 'tatli', min: 1, max: 1, owner: 1 });
    } else {
      if (raki) S.push({ key: 'meze', label: 'Mezeler', course: 'meze', min: 2, max: 2, owner: 0 });
      else S.push({ key: 'baslangic', label: 'Başlangıç', course: 'baslangic', min: 1, max: 1, owner: 0 });
      S.push({ key: 'salata', label: 'Salata', course: 'salata', min: 1, max: 1, owner: 0 });
      if (raki) S.push({ key: 'ara', label: 'Ara Sıcak', course: 'ara', min: 1, max: 1, owner: 0 });
      S.push({ key: 'ana0', label: 'Ana Yemek', course: 'ana', min: 1, max: 1, owner: 0 });
      S.push({ key: 'tatli0', label: 'Tatlı', course: 'tatli', min: 1, max: 1, owner: 0 });
    }
    S.push(drink);
    return S;
  }
  // food budget (drinks come on top, so a wine or rakı table naturally costs more than an alcohol-free one)
  const FOOD_BUDGET = {
    single: { def: { min: 2800, max: 4400, center: 3500 }, raki: { min: 3600, max: 5200, center: 4300 } },
    couple: { def: { min: 6000, max: 9000, center: 7200 }, raki: { min: 7000, max: 10200, center: 8400 } },
  };
  function slotsFor(mode, style, lux) {
    if (!lux) return slotsYz(mode, style);
    const couple = mode === 'couple';
    const raki = style === 'raki', none = style === 'none';
    const S = [];
    if (couple) {
      S.push({ key: 'baslangic', label: 'Başlangıç', course: 'baslangic', min: 1, max: 2, owner: 'both' });
      S.push({ key: 'meze', label: lux ? (raki ? 'Mezeler' : 'Meze ve Salata') : 'Mezeler', course: 'meze', min: lux ? (raki ? 3 : 2) : (raki ? 2 : 1), max: lux ? (raki ? 4 : 3) : (raki ? 3 : 2), owner: 'both' });
      if (!lux) S.push({ key: 'salata', label: 'Salata', course: 'salata', min: 1, max: 1, owner: 'both' });
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
      S.push({ key: 'meze', label: lux ? (raki ? 'Mezeler' : 'Meze ve Salata') : (raki ? 'Mezeler' : 'Meze'), course: 'meze', min: lux ? (raki ? 2 : 1) : 1, max: lux ? (raki ? 3 : 2) : (raki ? 2 : 1), owner: 0 });
      if (!lux) S.push({ key: 'salata', label: 'Salata', course: 'salata', min: 1, max: 1, owner: 0 });
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
      return { id: k, menuId: d.base || k, name: d.label || it.name, price: it.price, img: it.img || DRINK_IMG[d.st + (d.for === 'c' ? '-c' : '-s')] || null, tags: d.t, note: (!d.base && String(it.desc || '').trim()) || d.note, course: 'drink', style: d.st, fav, ing: [] };
    });
  }

  function foodPool(course, style, byId, mode, mask, ignorePair, lux) {
    return Object.keys(FOOD).filter((id) => {
      const f = FOOD[id];
      const fc = f.sal && !lux ? 'salata' : f.c;
      if (fc !== course || !byId[id] || !allowed(id, mask)) return false;
      if (f.share && mode !== 'couple') return false;
      if (ignorePair) return true;
      const pr = f.p[style] == null ? 1 : f.p[style];
      if (course === 'ana' && pr < 2) return false;
      return pr >= 1;
    }).map((id) => {
      const f = FOOD[id], it = byId[id];
      return { id, menuId: id, name: it.name, price: it.price, img: it.img || null, tags: f.t, pair: f.p[style] == null ? 1 : f.p[style], ing: f.i, note: String(it.desc || '').trim() || f.note, course };
    });
  }


  // ── guest choices (Yıldız): a second drink option, a second salad, an optional dessert ──
  const BOTTLE = { raki: 1, white: 1, red: 1, rose: 1, sparkling: 1, whisky: 1 };
  const optLabel = (items) => items.map((i) => i.name).join(' + ');
  function drinkItem(c, qty, why) {
    return { id: c.id, menuId: c.menuId, name: c.name, price: c.price, qty, img: c.img, note: c.note, why: why || null, pct: null, tags: [], pair: null, course: 'drink', score: 0, forName: null, forSign: null };
  }
  function drinkAlt(mode, style, persons, byId, input, cur) {
    const pref = (st) => persons.reduce((a, P) => a + (P.sign.drinks[st] || 0) + (P.co ? (P.co.drinks[st] || 0) * 0.3 : 0), 0) / persons.length;
    const curIds = cur.map((i) => i.id), curCost = cur.reduce((a, i) => a + i.price * i.qty, 0);
    let opts = style === 'none' ? [] : stylesFor(mode, input).filter((st) => st !== style).map((st) => ({ st, pool: drinkPool(mode, st, byId, persons) })).filter((x) => x.pool.length);
    if (!opts.length) { const same = drinkPool(mode, style, byId, persons).filter((c) => !curIds.includes(c.id)); if (same.length) opts = [{ st: style, pool: same }]; }
    if (!opts.length) return null;
    opts.sort((a, b) => pref(b.st) - pref(a.st));
    const { st, pool } = opts[0], n = servingsFor(mode, st);
    const rank = pool.map((c) => {
      const aff = persons.reduce((a, P) => a + affinity(c.tags, P), 0) / persons.length;
      return { c, k: aff / 3 + (c.fav || 0) * 1.4 - Math.abs(c.price * n - curCost) / 600 };
    }).sort((x, y) => y.k - x.k);
    const item = drinkItem(rank[0].c, n);
    return { style: st, label: item.name, items: [item] };
  }


  function solve(mode, style, persons, byId, R, mask, lux) {
    let slots = slotsFor(mode, style, lux);
    const B = Object.assign({}, lux ? BUDGET_LUX[mode] : FOOD_BUDGET[mode][style === 'raki' ? 'raki' : 'def']);
    const closer = byId[CLOSER.id];
    const closerCost = 0; // Türk kahvesi her menüde ikram
    const jit = {};
    const J = (id) => (jit[id] == null ? (jit[id] = R() * 3.4) : jit[id]);
    const dropped = [];
    const pools = [];
    const keep = [];
    for (const s of slots) {
      let pool;
      if (s.course === 'drink') pool = drinkPool(mode, style, byId, persons);
      else {
        pool = foodPool(s.course, style, byId, mode, mask, false, lux);
        if (!pool.length) {
          // empty because of the guest's diet -> drop the course; empty because of the drink -> this drink doesn't fit
          if (foodPool(s.course, style, byId, mode, mask, true, lux).length) return null;
          if (!dropped.includes(s.course)) dropped.push(s.course);
          continue;
        }
      }
      if (!pool.length) return null;
      pools.push(pool); keep.push(Object.assign({}, s));
    }
    slots = keep;
    if (dropped.length) {
      // give the room to cold starters so the table still feels complete
      const mz = slots.find((s) => s.key === 'meze');
      if (mz) { mz.min += dropped.length; mz.max += dropped.length * 2; if (dropped.includes('ana')) mz.label = 'Meze ve Salata Seçkisi'; }
    }
    slots.forEach((s, i) => { if (!s.repeat) { s.max = Math.min(s.max, pools[i].length); s.min = Math.min(s.min, s.max); } });
    // personal courses for a couple must still be two different dishes
    const cands = slots.map((s, si) => pools[si].map((c) => {
      const owners = s.owner === 'both' ? persons : [persons[s.owner]];
      const aff = owners.reduce((a, P) => a + affinity(c.tags, P), 0) / owners.length;
      const prem = c.course === 'drink' ? (lux ? 0 : -c.price / 1500) : Math.min(c.price, 2400) / (lux ? 520 : 1100);
      const base = 4 + aff / 3 + (c.pair || 0) * 1.0 + (c.fav || 0) * 1.4 + prem + J(c.id + s.key.replace(/\d/, ''));
      return Object.assign({}, c, { score: base });
    }));
    // budget that the menu can actually reach with these dishes
    let reach = closerCost;
    slots.forEach((s, si) => {
      if (!lux && s.course === 'drink') return;
      const prices = cands[si].map((c) => c.price).sort((a, b) => b - a);
      reach += s.repeat ? prices[0] * s.max : prices.slice(0, s.max).reduce((a, b) => a + b, 0);
    });
    let light = false;
    if (reach * 0.94 < B.min) { light = true; B.min = Math.round(reach * 0.55 / 10) * 10; B.center = Math.round(reach * 0.72 / 10) * 10; B.max = Math.min(B.max, reach); }

    function evaluate(state) {
      let total = closerCost, btot = closerCost, score = 0, count = 0;
      const ingCount = {}, used = {};
      const drinkTags = {};
      state.forEach((sel, si) => {
        sel.forEach((ci, k) => {
          const c = cands[si][ci];
          total += c.price; if (lux || c.course !== 'drink') btot += c.price;
          score += k < slots[si].min ? c.score : c.score * 0.3; count++;
          if (c.course === 'drink') { for (const t in c.tags) drinkTags[t] = (drinkTags[t] || 0) + c.tags[t]; }
          else {
            if (used[c.id]) score -= 1e6; used[c.id] = 1;
            c.ing.forEach((g) => { ingCount[g] = (ingCount[g] || 0) + 1; });
          }
        });
      });
      for (const g in ingCount) if (ingCount[g] > 1) score -= 6 * (ingCount[g] - 1);
      state.forEach((sel, si) => {
        if (slots[si].course === 'drink') return;
        sel.forEach((ci) => { const c = cands[si][ci]; for (const t in c.tags) if (drinkTags[t]) score += 0.12 * c.tags[t] * Math.min(drinkTags[t], 3); });
      });
      let pen = 0;
      state.forEach((sel, si) => { if (slots[si].same && new Set(sel).size > 1) score -= 1e6; });
      if (btot < B.min) pen += (B.min - btot) / 15;
      if (btot > B.max) pen += (btot - B.max) / 15;
      pen += Math.abs(btot - B.center) / (lux ? 220 : 90);
      return { f: score - pen, total, btot, score, count };
    }
    const legal = (state) => state.every((sel, si) => sel.length >= slots[si].min && sel.length <= slots[si].max && (slots[si].repeat || new Set(sel).size === sel.length));
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
        for (let k = 0; k < s.min; k++) out.push(s.same ? order[0] : order[k % order.length]);
        return out;
      });
    }
    let best = null;
    for (let r = 0; r < 4; r++) {
      const res = climb(init(r > 0));
      const ok = res.ev.btot >= B.min && res.ev.btot <= B.max && res.ev.f > -1e5;
      const key = (ok ? 1e6 : 0) + res.ev.f;
      if (!best || key > best.key) best = Object.assign(res, { key, ok });
    }
    return { slots, cands, closer, closerCost, best, dropped, light, budget: B };
  }

  const fillS = (tpl, S) => tpl.replace(/\{SG\}/g, S.name + ' burcunun').replace(/\{S\}/g, S.name + ' burcu').replace(/\{R\}/g, S.rulerGen);
  const fill = (tpl, P) => fillS(tpl, P.sign);
  function reasonLux(c, owners, usedTags, R) {
    const solo = owners.length === 1 && owners[0].__solo;
    if (c.course === 'drink') {
      const fan = owners.find((P) => P.sign.cocktails.indexOf(c.id) === 0) || owners.find((P) => P.sign.cocktails.indexOf(c.id) > 0);
      return { text: fan ? (owners.length > 1 ? fan.first + ' için: ' : '') + 'damak profilinize en uygun kokteyl.' : null, owner: fan || owners[0] };
    }
    const seen = usedTags['#tpl'] || (usedTags['#tpl'] = {});
    const opts = [];
    owners.forEach((P) => {
      for (const t in c.tags) {
        const pen = usedTags[t] ? 0.6 : 1;
        const sv = c.tags[t] * ((P.sign.taste[t] || 0) + (P.extra[t] || 0)) * pen;
        const nv = c.tags[t] * (P.ni.tags[t] || 0) * 0.95 * pen;
        if (sv > 0) opts.push({ v: sv, t, src: 'taste', P });
        if (nv > 0 && P.ni.group) opts.push({ v: nv, t, src: 'name', P });
      }
    });
    opts.sort((a, b) => b.v - a.v);
    for (const o of opts) {
      const P = o.P;
      if (o.src === 'name') {
        if (seen['#name' + P.first]) continue;
        seen['#name' + P.first] = 1; usedTags[o.t] = (usedTags[o.t] || 0) + 1;
        return { text: (solo ? 'Adınız' : P.first + ' adı') + ' “' + P.ni.meaning + '” anlamına geliyor; ' + LUX_NAME_WHY[P.ni.group] + '.', owner: P };
      }
      const list = LUX_WHY[o.t] || [];
      const k0 = Math.floor(R() * list.length);
      for (let k = 0; k < list.length; k++) {
        const tpl = list[(k0 + k) % list.length];
        if (seen[tpl]) continue;
        seen[tpl] = 1; usedTags[o.t] = (usedTags[o.t] || 0) + 1;
        return { text: tpl, owner: P };
      }
    }
    const list = FALLBACK[c.course] || FALLBACK.meze;
    for (const tpl of list) if (!seen['#fb' + tpl]) { seen['#fb' + tpl] = 1; return { text: tpl.replace('{S} burcu', 'Damağınız'), owner: owners[0] }; }
    return { text: null, owner: owners[0] };
  }
  function reasonFor(c, owners, usedTags, R) {
    if (c.course === 'drink') {
      const fan = owners.find((P) => P.sign.cocktails.indexOf(c.id) === 0) || owners.find((P) => P.sign.cocktails.indexOf(c.id) > 0);
      return { text: fan ? (owners.length > 1 ? fan.first + ' için: ' : '') + fan.sign.name + ' burcunun imza kokteyli.' : null, owner: fan || owners[0] };
    }
    const seen = usedTags['#tpl'] || (usedTags['#tpl'] = {});
    const opts = [];
    owners.forEach((P) => {
      for (const t in c.tags) {
        const pen = usedTags[t] ? 0.6 : 1;
        const sv = c.tags[t] * (P.sign.taste[t] || 0) * pen;
        const xv = c.tags[t] * (P.extra[t] || 0) * pen * 1.15;
        const nv = c.tags[t] * (P.ni.tags[t] || 0) * 0.95 * pen;
        if (sv > 0) opts.push({ v: sv, t, src: 'sign', P });
        if (xv > 0) opts.push({ v: xv, t, src: 'extra', P });
        if (nv > 0 && P.ni.group) opts.push({ v: nv, t, src: 'name', P });
      }
    });
    opts.sort((a, b) => b.v - a.v);
    const solo = owners.length === 1 && owners[0].__solo;
    for (const o of opts) {
      const P = o.P;
      if (o.src === 'name') {
        if (seen['#name' + P.first]) continue;
        seen['#name' + P.first] = 1; usedTags[o.t] = (usedTags[o.t] || 0) + 1;
        const who = solo ? 'Adın' : P.first + ' adı';
        return { text: who + ' “' + P.ni.meaning + '” demek; ' + NAME_WHY[P.ni.group] + '.', owner: P, tag: o.t };
      }
      const S = o.src === 'extra' ? (P.extraSrc[o.t] === 'co' ? P.co : P.cusp) : P.sign;
      if (!S) continue;
      const list = WHY[o.t] || [];
      const k0 = Math.floor(R() * list.length);
      for (let k = 0; k < list.length; k++) {
        const tpl = list[(k0 + k) % list.length], key = tpl + S.id;
        if (seen[key]) continue;
        if (o.src === 'extra' && seen['#extra' + P.first]) break;
        seen[key] = 1; usedTags[o.t] = (usedTags[o.t] || 0) + 1;
        if (o.src === 'extra') {
          seen['#extra' + P.first] = 1;
          const lead = P.extraSrc[o.t] === 'co' ? (solo ? 'Dekanındaki ' : gen(P.first) + ' dekanındaki ') + S.name + ' etkisi: ' : (solo ? 'Burç geçişindeki ' : gen(P.first) + ' burç geçişindeki ') + S.name + ' etkisi: ';
          return { text: lead + fillS(tpl, S), owner: P, tag: o.t };
        }
        return { text: fillS(tpl, S), owner: P, tag: o.t };
      }
    }
    const P = owners[0];
    const nt = Object.keys(P.ni.numInfo.tags).find((t) => c.tags[t]);
    if (nt && !seen['#num' + P.first]) { seen['#num' + P.first] = 1; return { text: (solo ? 'Sayın ' : P.first + ' için sayı ') + P.ni.num + ', ' + P.ni.numInfo.t.toLocaleLowerCase('tr') + ': ' + NUM_WHY[P.ni.num] + '.', owner: P }; }
    const list = FALLBACK[c.course] || FALLBACK.meze;
    for (let k = 0; k < list.length; k++) { const tpl = list[k]; if (!seen['#fb' + tpl]) { seen['#fb' + tpl] = 1; return { text: fill(tpl, P), owner: P }; } }
    return { text: null, owner: P };
  }

  const TAG_TR = { sea: 'Deniz', raw: 'Çiğ', spicy: 'Acı', grill: 'Köz', bold: 'Güçlü', smoky: 'İsli', earthy: 'Toprak', traditional: 'Geleneksel', slow: 'Yavaş pişmiş', local: 'Yerel', meat: 'Et', fresh: 'Ferah', citrus: 'Narenciye', herbal: 'Taze ot', light: 'Hafif', fruity: 'Meyveli', creamy: 'Kremalı', buttery: 'Tereyağlı', rich: 'Zengin', sweet: 'Tatlı', chocolate: 'Çikolata', dreamy: 'Rüya gibi', playful: 'Oyunbaz', crispy: 'Çıtır', share: 'Paylaşımlık', signature: 'Şefin imzası', elegant: 'Zarif', nutty: 'Kuruyemiş' };
  const topTags = (tags) => Object.keys(tags || {}).sort((a, b) => tags[b] - tags[a]).slice(0, 2).map((t) => TAG_TR[t]).filter(Boolean);

  /**
   * build(menu, { mode: 'single'|'couple', people: [{ name, day, month | sign, gender }], noAlcohol, diet: [...], variant })
   */
  function build(menu, input) {
    const mode = input.mode === 'couple' ? 'couple' : 'single';
    const persons = (input.people || []).slice(0, mode === 'couple' ? 2 : 1).map(person);
    if (persons.length !== (mode === 'couple' ? 2 : 1) || persons.some((p) => !p.sign)) throw new Error('bad input');
    if (mode === 'single') persons[0].__solo = true;
    const byId = catalog(menu);
    const variant = input.variant | 0;
    const diet = (input.diet || []).filter((k) => DIETS[k]).sort();
    const mask = dietMask(diet);
    const seedStr = [mode, input.noAlcohol ? 1 : 0, variant, diet.join(',')].concat(persons.map((p) => lowerTr(p.name) + '|' + p.sign.id + '|' + (p.decan || 0) + '|' + (p.gender || ''))).join('#');
    const styles = stylesFor(mode, input);
    const Rs = rng(hash(seedStr + '#style'));
    let pick = null;
    styles.forEach((st) => {
      const R = rng(hash(seedStr + '#' + st));
      const res = solve(mode, st, persons, byId, R, mask, input.tone === 'lux');
      if (!res) return;
      const pref = persons.reduce((a, P) => a + (P.sign.drinks[st] || 0) + (P.co ? (P.co.drinks[st] || 0) * 0.3 : 0), 0) / persons.length;
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
    const seenIds = {};
    Object.keys(FOOD).forEach((id) => { if (byId[id]) seenIds[id] = 1; });
    Object.keys(DRINK).forEach((k) => { const b = DRINK[k].base || k; if (byId[b]) seenIds[b] = 1; });
    const scanned = Object.keys(seenIds).length;
    best.state.forEach((sel, si) => {
      const s = slots[si];
      const owners = s.owner === 'both' ? persons : [persons[s.owner]];
      const groupKey = s.key.replace(/\d$/, '');
      let g = courses.find((x) => x.key === groupKey);
      if (!g) { g = { key: groupKey, label: s.label, items: [] }; courses.push(g); }
      const sc = cands[si].map((c) => c.score), mx = Math.max.apply(null, sc), mn = Math.min.apply(null, sc);
      const counts = {};
      sel.forEach((ci) => { counts[ci] = (counts[ci] || 0) + 1; });
      Object.keys(counts).forEach((ci) => {
        const c = cands[si][ci];
        const rs = (input.tone === 'lux' ? reasonLux : reasonFor)(c, owners, usedTags, R);
        const pct = Math.round(78 + 20 * ((c.score - mn) / ((mx - mn) || 1)));
        g.items.push({ id: c.id, menuId: c.menuId, name: c.name, price: c.price, qty: counts[ci], img: c.img, note: c.note,
          why: rs.text, pct: c.course === 'drink' ? null : pct, tags: c.course === 'drink' ? [] : topTags(c.tags),
          pair: c.course === 'ana' ? pairLine(style, c) : null, course: c.course, score: c.score,
          forName: s.owner === 'both' ? null : persons[s.owner].first, forSign: s.owner === 'both' ? null : persons[s.owner].sign.id });
      });
    });
    courses.forEach((g) => { if (g.key === 'ana' && g.items.length > 1) g.label = 'Ana Yemekler'; if (g.key === 'tatli' && g.items.length > 1) g.label = 'Tatlılar'; });
    if (style === 'cocktail') { const ck = courses.find((g) => g.key === 'icki'); if (ck && ck.items.length === 1 && ck.items[0].qty === 1) ck.label = 'Kokteyl'; }
    if (input.tone !== 'lux') {
      const ic = courses.find((g) => g.key === 'icki');
      if (ic) {
        const alt = drinkAlt(mode, style, persons, byId, input, ic.items);
        if (alt) { ic.choice = [{ style, label: ic.items[0].name, items: ic.items }, alt]; ic.label = style === 'none' ? 'İçecek' : 'İçki'; }
      }
      const si = slots.findIndex((x) => x.key === 'salata'), sg = courses.find((g) => g.key === 'salata');
      if (si >= 0 && sg && sg.items.length) {
        const cur = sg.items[0], other = cands[si].filter((c) => c.id !== cur.id).sort((a, b) => b.score - a.score)[0];
        if (other) {
          const owners = slots[si].owner === 'both' ? persons : [persons[slots[si].owner]];
          const sc = cands[si].map((c) => c.score), mx = Math.max.apply(null, sc), mn = Math.min.apply(null, sc);
          const rs = reasonFor(other, owners, usedTags, R);
          const alt = { id: other.id, menuId: other.menuId, name: other.name, price: other.price, qty: cur.qty, img: other.img, note: other.note, why: rs.text, pct: Math.round(78 + 20 * ((other.score - mn) / ((mx - mn) || 1))), tags: topTags(other.tags), pair: null, course: 'salata', score: other.score, forName: null, forSign: null };
          sg.choice = [{ label: cur.name, items: [cur] }, { label: alt.name, items: [alt] }];
        }
      }
      courses.forEach((g) => { if (g.key === 'tatli') g.optional = true; });
    }
    if (closer) courses.push({ key: 'kapanis', label: 'Kapanış', items: [{ id: CLOSER.id, menuId: CLOSER.id, name: closer.name, price: 0, listPrice: closer.price, free: true, qty: persons.length, img: CLOSER.img, note: input.tone === 'lux' ? 'Bizden ikram. Akşamı Türk kahvesi ve sohbetle kapatın' : CLOSER.note, why: null, pct: null, tags: [] }] });

    // the star dish: best-fitting hot course with a photo
    let star = null;
    courses.forEach((g) => g.items.forEach((it) => {
      if (!it.img || !['ana', 'ara', 'baslangic'].includes(it.course)) return;
      const k = it.pct * 10 + (it.course === 'ana' ? 6 : it.course === 'ara' ? 3 : 0) + it.price / 1000;
      if (!star || k > star.k) star = { k, it };
    }));
    if (star) { star.it.star = true; if (!star.it.pair) star.it.pair = pairLine(style, { tags: (FOOD[star.it.id] || {}).t }); }

    const total = courses.reduce((a, g) => a + g.items.reduce((b, it) => b + it.price * it.qty, 0), 0);
    const code = 'YM-' + (hash(courses.map((g) => g.items.map((i) => i.id + i.qty).join(',')).join('|')) % 46656).toString(36).toUpperCase().padStart(3, '0') + persons.map((p) => fold(lowerTr(p.sign.name.charAt(0))).toUpperCase()).join('');

    const profiles = persons.map(profile);
    const reading = persons.map((P, i) => {
      const prof = profiles[i].slice().sort((a, b) => b.v - a.v);
      return {
        name: P.name, first: P.first, sign: P.sign.id, signName: P.sign.name, el: EL[P.sign.el], ruler: P.sign.ruler, dates: P.sign.dates, mod: MOD[P.sign.id],
        gender: P.gender, decan: P.decan, co: P.co ? P.co.name : null, cusp: P.cusp ? P.cusp.name : null, birth: P.birth,
        intro: P.gender === 'f' ? P.sign.f : P.gender === 'm' ? P.sign.m : null,
        palate: P.sign.palate, decanText: decanText(P), cuspText: cuspText(P),
        meaning: P.ni.meaning, num: P.ni.num, numTotal: P.ni.numTotal, digits: P.ni.digits, numTitle: P.ni.numInfo.t, numText: P.ni.numInfo.s,
        profile: profiles[i], persona: PERSONA[P.sign.id][0], personaText: PERSONA[P.sign.id][1],
        insights: input.tone === 'lux'
          ? [{ k: 'Öne çıkan', v: LUX_AXIS_TOP[prof[0].id] }, { k: 'İkinci tercih', v: LUX_AXIS_TOP[prof[1].id] }, { k: 'Keşif alanı', v: LUX_AXIS_LOW[prof[prof.length - 1].id] }]
          : [{ k: 'Güçlü yönün', v: AXIS_TOP[prof[0].id] }, { k: 'İkinci sesin', v: AXIS_TOP[prof[1].id] }, { k: 'Keşif alanın', v: AXIS_LOW[prof[prof.length - 1].id] }],
      };
    });
    let pairText = null, match = null;
    if (mode === 'couple') {
      const k = [persons[0].sign.el, persons[1].sign.el].sort().join('|');
      pairText = PAIR_TEXT[k];
      if (persons[0].sign.id === persons[1].sign.id) pairText = 'İki ' + persons[0].sign.name + ' aynı masada: aynı dili konuşan iki damak. ' + pairText;
      match = input.tone === 'lux' ? luxMatch(persons[0], persons[1], profiles[0], profiles[1]) : compat(persons[0], persons[1], profiles[0], profiles[1]);
      if (input.tone === 'lux') pairText = 'Ortak tabaklar ikinizin damak profiline göre, ana yemek ve tatlılar her birinize ayrı seçildi.';
    }
    const notes = [];
    if (res.dropped.includes('ana')) notes.push('Menümüzde tercihine uygun bir ana yemek bulunmadığı için ana yemek yerine zengin bir meze ve salata seçkisi hazırladık.');
    if (res.dropped.includes('ara')) notes.push('Tercihine uygun bir ara sıcak bulunmadığından yerine ek bir soğuk başlangıç koyduk.');
    if (res.dropped.includes('baslangic')) notes.push('Tercihine uygun bir başlangıç bulunmadığından mezelerle açılış yaptık.');
    if (res.light) notes.push('Tercihlerin doğrultusunda menü daha hafif tutuldu; indirim yine menünün tamamına uygulanır.');
    return {
      mode, style, styleName: STYLE_NAME[style], styleWhy: STYLE_WHY[style], courses, total, code, reading, pairText, match,
      ok: best.ok, budget: res.budget, lux: input.tone === 'lux', diet: diet.map((k) => DIETS[k].label), notes, scanned,
    };
  }

  const api = { SIGNS, STARS, EL, MOD, DIETS, build, nameInfo, nameOk, signFromDate, astroFromDate, validDate, cleanName, gen, BUDGET, FOOD, DRINK };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.YildizEngine = api;
})(typeof window !== 'undefined' ? window : globalThis);
