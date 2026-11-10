/* Yıldız Menüsü · isim sözlüğü + kök yorumu
   Satır: ad|anlam|köken|grup|not   (grup = engine NAME_GROUP anahtarı)
   Köken kodları ORIGIN'de. Emin olunmayan isimler sözlüğe yazılmaz; kök yorumuna bırakılır. */
(function (root) {
  const ORIGIN = { T: 'Türkçe', A: 'Arapça', F: 'Farsça', Y: 'Yunanca', L: 'Latince', Ib: 'İbranice', Lz: 'Lazca', Gr: 'Gürcüce', S: 'Slav kökenli', M: 'Moğolca', K: 'Kürtçe', Al: 'Cermen kökenli', It: 'İtalyanca', Fr: 'Fransızca', Is: 'İskandinav', Kl: 'Kelt kökenli', Sk: 'Sanskritçe', Ar: 'Aramice', Ç: 'Çince kökenli', AF: 'Arapça-Farsça', TF: 'Türkçe-Farsça', TA: 'Türkçe-Arapça' };
  const RAW = `
abdullah|Allah'ın kulu|A|asil|
abdurrahman|Rahman'ın kulu|A|asil|
adem|toprak; ilk insan|Ib|toprak|Hz. Âdem'in adı; kökü toprakla ilişkilendirilir.
adil|adaletli, doğru|A|asil|
adnan|yerleşik, yurt tutan|A|toprak|
afra|beyaz ile kırmızı karışımı renk|A|cicek|
ahu|ceylan|F|ruzgar|
akın|ileri atılış, coşkun hareket|T|ruzgar|
akif|kendini ibadete veren, kararlı|A|derin|
alara|su perisi|T|su|
alican|yüce ve candan|TA|asil|
alihan|yüce hükümdar|TA|asil|
alize|ılık deniz rüzgârı|Fr|ruzgar|Tropik denizlerde esen düzenli rüzgârın adı.
almila|elma rengi; elma gibi|T|cicek|
alper|yiğit er|T|guc|
alperen|yiğit ve ermiş|T|guc|
alparslan|yiğit aslan|T|guc|Büyük Selçuklu hükümdarının adı.
altan|kızıl şafak|T|isik|
altay|altın ay; Altay dağları|T|guc|
amine|güvenilir|A|toprak|
anıl|anılan, hatırlanan|T|asil|
arda|Meriç'in kolu olan bir ırmak|T|su|
arya|ezgi; soylu|F|nese|
asel|bal gibi tatlı|A|tatli|
asena|Türk efsanesinde yol gösteren dişi kurt|T|guc|Göktürklerin türeyiş destanındaki bozkurt.
asil|soylu|A|asil|
aslı|asıl, öz; Kerem ile Aslı'nın kahramanı|A|tatli|
asya|Asya kıtası; doğu|T|toprak|
aşkın|aşan, üstün|T|gok|
ata|baba, cet|T|toprak|
atakan|ata kanından|T|asil|
atilla|Hun hükümdarının adı|T|guc|
atlas|Atlas dağları; ipek kumaş|Y|guc|
avşar|bir Oğuz boyu|T|toprak|
ayaz|soğuk ve açık hava|T|ruzgar|
aybike|ay gibi güzel hanım|T|gok|
aybüke|ay gibi güzel ve bilge kadın|T|gok|
aydan|aydan gelen, ay gibi|T|gok|
aydın|aydınlık; ışıklı|T|isik|
ayhan|ay gibi parlak hükümdar|T|gok|
ayla|ayın çevresindeki ışık halkası|T|gok|
aylin|ayın çevresindeki ışık halkası|T|gok|
aysu|ay ve su; ay gibi güzel su|T|gok|
aysun|ay gibi|T|gok|
aytaç|ay tacı|T|gok|
ayten|ay tenli, ay gibi ak|T|gok|
aytekin|ay gibi parlak prens|T|gok|
aytül|ay gibi güzel|T|gok|
ayşegül|yaşayan gül|A|cicek|
azad|özgür|F|ruzgar|
aziz|değerli, yüce|A|asil|
azize|değerli, saygın kadın|A|asil|
azra|bakire; el değmemiş|A|isik|
bahadır|yiğit, cesur|M|guc|
bahar|ilkbahar|F|cicek|
bahri|denizle ilgili|A|su|
baki|kalıcı, sonsuz|A|derin|
baran|yağmur|F|su|
barış|barış, uzlaşma|T|tatli|
bartu|güzel yüzlü yiğit|T|guc|
basri|gören, bakan; Basralı|A|derin|
batu|sağlam, güçlü|T|guc|
batuhan|sağlam hükümdar|T|guc|
bayram|bayram, şenlik|T|nese|
bedirhan|dolunay gibi hükümdar|AF|gok|
behiye|güzel, parlak|A|isik|
bekir|ilk doğan, genç|A|asil|
belgin|açık, belirgin|T|isik|
belinay|ay belirdi|T|gok|
belma|ay parçası|T|gok|
beren|güçlü, akıllı|T|guc|
berfin|kardelen çiçeği|K|cicek|
berk|sağlam, güçlü|T|guc|
berkay|güçlü ay|T|guc|
berkant|sağlam yemin|T|guc|
berna|genç, delikanlı|T|nese|
beste|bestelenmiş ezgi|F|nese|
betül|kendini Allah'a adamış|A|derin|
beyza|beyaz, ak; yumurta|A|isik|
bilal|ıslatan, serinleten|A|su|İlk müezzin Bilal-i Habeşi'nin adı.
bilge|bilgili, bilgin|T|derin|
binnur|bin nur, çok ışıklı|TA|isik|
bora|fırtına; sert kuzey rüzgârı|T|ruzgar|
burak|şimşek; Miraç'ta Hz. Muhammed'i taşıyan binek|A|ates|
burcu|güzel koku|T|cicek|
burçin|ceylan|T|ruzgar|
burhan|kanıt|A|derin|
bülent|yüksek, yüce|F|asil|
büşra|müjde|A|nese|
cafer|küçük dere|A|su|
can|can, ruh|F|nese|
canan|sevgili|F|tatli|
caner|candan er|FT|nese|
cansu|can suyu|FT|su|
celal|ululuk, büyüklük|A|asil|
celil|ulu, yüce|A|asil|
cem|hükümdar; toplanma|F|asil|
cemal|güzellik|A|tatli|
cemile|güzel|A|tatli|
cemil|güzel|A|tatli|
cemre|baharı müjdeleyen sıcaklık|A|isik|Halk takviminde havaya, suya ve toprağa düşen sıcaklık.
cengiz|güçlü, kudretli|M|guc|
ceren|ceylan|T|ruzgar|
cevdet|cömertlik, iyilik|A|tatli|
ceyda|uzun boylu, güzel|A|tatli|
ceylan|ceylan|T|ruzgar|
cihan|dünya, evren|F|gok|
coşkun|coşkulu, taşkın|T|ates|
çağan|bayram, şenlik|T|nese|
çağatay|Çağatay Han; bir Türk boyu|T|asil|
çağdaş|aynı çağda yaşayan|T|farkli|
çağla|çağlayan, şırıl şırıl akan; ham badem|T|su|
çağlar|çağlayan|T|su|
çağrı|davet; eski Türkçede doğan kuşu|T|guc|Selçuklu Devleti'nin kurucularından Çağrı Bey'in adı.
çelik|çelik|T|guc|
çiğdem|kır çiçeği|T|cicek|
çınar|çınar ağacı|F|toprak|
damla|damla|T|su|
davut|sevgili|Ib|tatli|Hz. Davut'un adı.
defne|defne ağacı|Y|cicek|
demet|çiçek demeti|T|cicek|
demir|demir|T|guc|
deniz|deniz|T|su|
derin|derin|T|derin|
derya|deniz|F|su|
dicle|Dicle nehri|A|su|
dila|gönül, kalp|F|tatli|
dilan|gönüller|F|tatli|
dilara|gönül süsleyen, sevgili|F|tatli|
dilek|dilek|T|tatli|
dilruba|gönül alan|F|tatli|
doğa|doğa, tabiat|T|toprak|
doğan|doğan kuşu; yeni doğan|T|guc|Doğan, şahin cinsinden avcı bir kuştur; Oğuz boylarının ongun kuşlarındandır.
doğu|doğu yönü; güneşin doğduğu yer|T|isik|
doruk|zirve|T|guc|
dudu|kadın, hanım; papağan|F|nese|
duru|berrak, saf|T|su|
duygu|duygu|T|tatli|
dünya|dünya|A|toprak|
ebru|kaş; su üstüne yapılan renkli desen|F|su|
ece|kraliçe, büyük hanım|T|asil|
ecrin|ödül, sevap|A|isik|
eda|naz, zarafet|A|tatli|
edibe|edebi olan, terbiyeli|A|derin|
efe|yiğit|T|guc|
efsun|büyü|F|derin|
ege|Ege denizi|T|su|
ekin|ekin, tahıl|T|toprak|
ekrem|çok cömert|A|asil|
ela|ela göz|A|derin|
elçin|halkın elçisi|T|asil|
elif|Arap alfabesinin ilk harfi; zarif, ince|A|isik|
elvan|renkler, renk renk|A|cicek|
elvin|ışık saçan|T|isik|
emel|istek, arzu|A|tatli|
emin|güvenilir|A|toprak|
emine|güvenilir|A|toprak|
emir|buyruk; yönetici|A|asil|
emre|dost, âşık|T|tatli|
enes|dost, yakın|A|tatli|
engin|geniş, açık deniz|T|su|
enis|dost|A|tatli|
ensar|yardımcılar|A|tatli|
erdal|erkek ve güçlü dal|T|guc|
erdem|fazilet|T|asil|
erdi|yetişti, olgunlaştı|T|toprak|
eren|ermiş|T|gok|
ergin|olgun, erişkin|T|toprak|
erhan|er ve hükümdar|T|asil|
erkan|erlerin kanından|T|guc|
erol|er ol, yiğit ol|T|guc|
ersin|yiğitsin|T|guc|
ertan|şafak yiğidi|T|isik|
ertuğrul|yiğit sancaktar|T|guc|Osmanlı'nın kurucusu Osman Bey'in babası.
esin|ilham|T|gok|
esma|isimler|A|derin|
esra|yolculuk; Miraç gecesi|A|gok|
eylül|eylül ayı|A|toprak|
ezgi|melodi|T|nese|
fadime|sütten kesilmiş|A|toprak|
fahri|onurla ilgili|A|asil|
faruk|haklı ile haksızı ayıran|A|asil|
fatih|fetheden|A|guc|
fatma|sütten kesilmiş; Hz. Fatıma'nın adı|A|toprak|
fehmi|anlayışlı|A|derin|
ferhat|yalnız, eşsiz|F|tatli|Ferhat ile Şirin hikâyesinin kahramanı.
feride|eşsiz, tek|A|asil|
ferit|eşsiz, tek|A|asil|
feyza|bolluk|A|toprak|
feyzullah|Allah'ın lütfu|A|asil|
fikret|düşünce|A|derin|
filiz|filiz|T|cicek|
fulya|nergis türünden sarı çiçek|T|cicek|
funda|çalı çiçeği|T|cicek|
furkan|iyiyi kötüden ayıran|A|derin|
gamze|gamze|T|nese|
gizem|sır|T|derin|
gonca|açmamış çiçek|F|cicek|
gökay|gök ve ay|T|gok|
gökberk|gök gibi sağlam|T|gok|
gökçe|gök mavisi; güzel|T|gok|
gökhan|göklerin hanı|T|asil|
göksel|gökle ilgili|T|gok|
göktuğ|gökyüzünün sancağı|T|gok|
gökşen|gök gibi şen|T|gok|
gönül|gönül|T|tatli|
gubaz|Lazların tarihî kral adı|Lz|asil|Lazika (Kolhis) krallarından I. ve II. Gubaz'ın adı; 5. ve 6. yüzyıl.
gül|gül|F|cicek|
gülay|gül ve ay|FT|cicek|
gülbahar|gül ve bahar|F|cicek|
gülcan|gül gibi can|F|cicek|
gülçin|gül derleyen|F|cicek|
gülden|gül gibi|FT|cicek|
güler|gülen|T|nese|
gülsüm|tombul yanaklı|A|tatli|
gülşen|gül bahçesi|F|cicek|
gülten|gül tenli|FT|cicek|
güven|güven|T|toprak|
habib|sevgili|A|tatli|
hacer|taş|Ib|toprak|
hakan|hükümdar|T|asil|
hakkı|doğru, gerçek|A|asil|
halil|candan dost|A|tatli|
halime|yumuşak huylu|A|tatli|
halil ibrahim|Hz. İbrahim'in lakabı; candan dost|A|tatli|
halit|kalıcı, ölümsüz|A|derin|
hamdi|övgüyle ilgili|A|asil|
hamza|aslan|A|guc|
hande|gülümseme|F|nese|
hanife|doğru yolda olan|A|asil|
harun|dağ; yüce|Ib|guc|
hasan|güzel|A|tatli|
hatice|erken doğan|A|toprak|
hayati|yaşamla ilgili|A|nese|
hayri|hayırla ilgili|A|tatli|
hazal|kuru yaprak|T|toprak|
helin|kuş yuvası|K|toprak|
hilal|yeni ay|A|gok|
hira|Hira dağı|A|gok|
hülya|hayal|A|gok|
hüma|cennet kuşu; mutluluk kuşu|F|gok|
hüseyin|küçük güzel|A|tatli|
ılgın|ılgın ağacı|T|toprak|
ırmak|ırmak|T|su|
ışık|ışık|T|isik|
ibrahim|ulusların babası|Ib|asil|
ilayda|ilk ay ışığı|T|gok|
ilhan|ülkenin hanı|T|asil|
ilkay|ilk ay|T|gok|
ilker|ilk er|T|guc|
ilknur|ilk ışık|TA|isik|
ilyas|Hz. İlyas'ın adı|Ib|derin|
irem|cennet bahçesi|A|cicek|
ipek|ipek|T|tatli|
ismail|Allah işitir|Ib|derin|
iclal|saygınlık|A|asil|
kaan|hükümdar|T|asil|
kader|alın yazısı|A|derin|
kadir|güçlü, kudretli; değer bilen|A|guc|Arapça kadr kökünden; Kadir Gecesi'nin de adıdır.
kadriye|değerli, saygın|A|asil|
kağan|hükümdar|T|asil|
kamil|olgun, eksiksiz|A|derin|
kardelen|kardelen çiçeği|T|cicek|
kaya|kaya|T|guc|
kayra|iyilik, lütuf|T|tatli|
kemal|olgunluk, mükemmellik|A|asil|
kenan|Kenan ülkesi|Ib|toprak|
kerem|cömertlik|A|asil|
kerim|cömert|A|asil|
kevser|cennet ırmağı|A|su|
kezban|ev hanımı, hanım|T|toprak|
kıvanç|övünç, sevinç|T|nese|
koray|ateş gibi parlak ay|T|ates|
korkmaz|korkusuz|T|guc|
kubilay|Moğol hükümdarının adı|M|asil|
kutay|kutlu ay; ipek|T|gok|
kübra|en büyük|A|asil|
lale|lale|F|cicek|
latife|şaka, nükte; ince|A|nese|
leman|parıltı|A|isik|
lerzan|titreyen|F|derin|
levent|yakışıklı, yiğit|F|guc|
leyla|gece; Leyla ile Mecnun'un kahramanı|A|derin|
lütfiye|lütufkâr|A|tatli|
lütfi|lütufla ilgili|A|tatli|
mahir|usta, becerikli|A|asil|
mahmut|övülmüş|A|asil|
mavi|mavi|T|su|
medine|şehir; Medine|A|toprak|
mehmet|övülmüş|A|asil|
mehtap|ay ışığı|F|gok|
melda|güzel, zarif|A|tatli|
melek|melek|A|gok|
melike|melike, kraliçe|A|asil|
melis|bal|Y|tatli|
melisa|bal arısı; oğul otu|Y|cicek|
meltem|yaz serin rüzgârı|T|ruzgar|
meral|ceylan, geyik|T|ruzgar|
merve|Mekke'de bir tepe|A|toprak|
meryem|Hz. İsa'nın annesi|Ib|isik|
mert|yiğit|F|guc|
mesut|mutlu|A|nese|
metin|sağlam, dayanıklı|A|guc|
mevlüt|doğum|A|isik|
mihriban|güneş gibi, şefkatli|F|isik|
mine|kır çiçeği; mine işi|F|cicek|
miraç|göğe yükseliş|A|gok|
mira|prenses; ışık|F|isik|
miray|ay gibi|FT|gok|
muhammed|çok övülmüş|A|asil|
muhammet|çok övülmüş|A|asil|
murat|dilek, istek|A|tatli|
mustafa|seçilmiş|A|asil|
mutlu|mutlu|T|nese|
müge|inci çiçeği|T|cicek|
münevver|aydınlatılmış|A|isik|
naciye|kurtulmuş|A|isik|
nail|ulaşan, kavuşan|A|tatli|
naz|naz|F|tatli|
nazan|nazlı|F|tatli|
nazlı|nazlı|F|tatli|
necati|kurtuluş|A|isik|
necla|geniş gözlü|A|derin|
nehir|nehir|A|su|
nergis|nergis çiçeği|F|cicek|
nermin|yumuşak|F|tatli|
nesrin|yaban gülü|F|cicek|
neslihan|soylu nesilden gelen|AT|asil|
neşe|neşe|F|nese|
nevin|yeni, taze|F|cicek|
nihal|fidan|F|cicek|
nil|Nil nehri; mavi|A|su|
nilay|Nil ve ay|T|gok|
nilsu|Nil suyu|T|su|
nilüfer|nilüfer çiçeği|F|cicek|
nisa|kadınlar|A|tatli|
nisan|nisan ayı|Ar|cicek|
nur|ışık|A|isik|
nuray|ay ışığı|AT|isik|
nurcan|ışıklı can|AF|isik|
nuri|ışıkla ilgili|A|isik|
nursel|ışık seli|AT|isik|
nurten|ışık tenli|AT|isik|
nuh|Hz. Nuh'un adı; dinlenme|Ib|su|
oğuz|Oğuzlar; Oğuz Kağan|T|guc|
oğuzhan|Oğuzların hükümdarı|T|asil|
okan|anlayışlı|T|derin|
oktay|ok gibi ay; Ögeday Han|T|guc|
onur|şeref|T|asil|
orhan|kumandan|T|asil|
orkun|Orhun nehri; Orhun Yazıtları|T|toprak|
osman|yavru kartal; Osmanlı'nın kurucusu|A|guc|
ozan|halk şairi|T|nese|
ömer|yaşayan, ömürlü|A|asil|
öykü|hikâye|T|derin|
özge|başka, farklı|T|farkli|
özgür|özgür|T|ruzgar|
özlem|özlem|T|tatli|
özkan|öz kanından|T|asil|
pakize|temiz, saf|F|isik|
pelin|pelin otu|T|cicek|
pembe|pembe|F|cicek|
pervin|Ülker yıldız kümesi|F|gok|
pınar|kaynak suyu|T|su|
poyraz|kuzey rüzgârı|Y|ruzgar|
rabia|dördüncü; bahar|A|cicek|
rahmi|merhametle ilgili|A|tatli|
ramazan|Ramazan ayı; kızgın sıcak|A|ates|
rana|güzel|A|tatli|
rasim|resim yapan|A|farkli|
recep|Recep ayı; saygı|A|asil|
remzi|simgesel|A|derin|
reşat|doğru yolda olmak|A|asil|
rıza|hoşnutluk|A|tatli|
rukiye|yükselen|A|gok|
rüya|rüya|A|gok|
rüzgar|rüzgâr|F|ruzgar|
rüzgâr|rüzgâr|F|ruzgar|
sabri|sabırlı|A|toprak|
sadık|bağlı, sadık|A|toprak|
safiye|saf, temiz|A|isik|
sahra|çöl|A|ates|
saliha|iyi, yararlı|A|tatli|
salih|iyi, yararlı|A|tatli|
sami|yüce|A|asil|
saniye|ikinci; değerli|A|isik|
sarp|sarp, aşılması zor|T|guc|
savaş|savaş|T|guc|
seda|ses, yankı|A|nese|
sedef|inci kabuğu|F|su|
sefa|gönül şenliği|A|nese|
selcan|sel gibi coşkun can|TF|su|
selçuk|Selçuklu beyi; Selçuk Bey|T|asil|
selim|sağlam, kusursuz|A|guc|
selin|akarsu|T|su|
selma|barış içinde, esen|A|tatli|
sema|gökyüzü|A|gok|
semra|esmer|A|derin|
sena|övgü|A|isik|
serap|ılgım, yanılsama|A|derin|
serdar|komutan, başbuğ|F|guc|
seren|direk; önder|T|asil|
serhat|sınır|F|toprak|
serkan|başta gelen, önder kan|FT|guc|
sertaç|baştaki taç|F|asil|
sevda|aşk|A|tatli|
sevgi|sevgi|T|tatli|
sevil|sevil, sevgi gör|T|tatli|
sevim|sevimli|T|tatli|
sevinç|sevinç|T|nese|
seyhan|Seyhan nehri|T|su|
sezen|sezgisi güçlü|T|derin|
sezer|sezen, anlayan|T|derin|
sezgin|sezgisi güçlü|T|derin|
sibel|kâhin kadın|Y|derin|
simge|sembol|T|derin|
sinan|mızrak ucu|A|guc|
sinem|göğüs, gönül|F|tatli|
songül|son gül|TF|cicek|
su|su|T|su|
suna|erkek ördek; güzel|T|su|
sude|aşınmış; saf|F|su|
sultan|hükümdar|A|asil|
suat|mutluluk|A|nese|
süheyla|Süheyl yıldızı|A|gok|Gökyüzünün en parlak yıldızlarından Canopus'un Arapçadaki adı.
süleyman|esenlik, huzur|Ib|asil|
sümeyye|yüce|A|asil|
şahin|şahin kuşu|F|guc|
şebnem|çiy|F|su|
şeyma|benli, güzel|A|tatli|
şengül|şen gül|TF|cicek|
şenol|şen ol|T|nese|
şerife|şerefli|A|asil|
şermin|utangaç|F|tatli|
şevket|güç, ihtişam|A|guc|
şeyda|tutkun|F|tatli|
şimal|kuzey|A|ruzgar|
şirin|tatlı, sevimli|F|tatli|
şule|alev|A|ates|
şükrü|şükürle ilgili|A|tatli|
taha|Kuran'da bir sure|A|derin|
tahir|temiz|A|isik|
talha|bir tür ağaç|A|toprak|
tamer|hurmacı|A|toprak|
tan|şafak|T|isik|
taner|şafak yiğidi|T|isik|
tanju|güzel güneş|T|isik|
tansel|şafak seli|T|isik|
tansu|şafak suyu|T|su|
tarık|sabah yıldızı|A|gok|Kuran'da sabah yıldızı anlamında geçer.
tayfun|kasırga, şiddetli fırtına|Ç|ruzgar|Uzak Doğu'nun tropik kasırgaları için kullanılan söz.
taylan|yakışıklı, endamlı|T|guc|
tayyar|uçan, hızlı|A|ruzgar|
tekin|prens; eşsiz|T|asil|
temel|temel|T|toprak|
teoman|Hun hükümdarı Teoman|T|asil|
tolga|savaş miğferi|T|guc|
tolgahan|miğferli hükümdar|T|guc|
toprak|toprak|T|toprak|
tuba|cennet ağacı|A|cicek|
tufan|büyük sel|A|su|
tuğba|cennet ağacı|A|cicek|
tuğçe|küçük sancak|T|asil|
tuğrul|doğan kuşu; Tuğrul Bey|T|guc|Büyük Selçuklu'nun kurucusu Tuğrul Bey'in adı.
tuna|Tuna nehri|T|su|
tunç|tunç; dayanıklı|T|guc|
turan|Türk yurdu|T|toprak|
turgay|tarla kuşu|T|ruzgar|
tülay|tül gibi ay ışığı|T|gok|
tülin|tül gibi ince|T|tatli|
tümay|dolunay|T|gok|
türkan|Türk kanından|T|asil|
uğur|şans, iyi talih|T|nese|
uluç|aslan; ulu|T|guc|
umut|umut|T|isik|
utku|zafer|T|guc|
ülkü|ideal|T|gok|
ümit|umut|F|isik|
ümran|bayındırlık|A|toprak|
ünal|ün alan|T|asil|
vahit|tek, eşsiz|A|asil|
vedat|sevgi|A|tatli|
veli|dost, ermiş|A|gok|
volkan|yanardağ|L|ates|
vural|vuran, yiğit|T|guc|
yağız|yağız, esmer; yiğit|T|guc|
yağmur|yağmur|T|su|
yakup|Hz. Yakup'un adı|Ib|derin|
yaprak|yaprak|T|cicek|
yaren|dost|F|nese|
yasemin|yasemin çiçeği|F|cicek|
yasin|Kuran'da bir sure|A|derin|
yavuz|güçlü, yaman|T|guc|
yaşar|yaşayan|T|nese|
yekta|tek, eşsiz|F|asil|
yelda|yılın en uzun gecesi|Ar|derin|21 Aralık gecesi, kış gündönümü.
yeliz|rüzgâr, yel|T|ruzgar|
yeşim|yeşim taşı|T|asil|Yeşil renkli, kıymetli bir süs taşı; Doğu'da şans ve uzun ömür taşı sayılır.
yiğit|yiğit|T|guc|
yıldırım|yıldırım|T|ates|
yıldız|yıldız|T|gok|
yılmaz|yılmayan, korkusuz|T|guc|
yunus|yunus balığı; Hz. Yunus|Ib|su|
yusuf|Hz. Yusuf'un adı; güzellik simgesi|Ib|tatli|
yüksel|yüksel|T|gok|
zafer|başarı|A|guc|
zehra|parlak, aydınlık|A|isik|
zekeriya|Hz. Zekeriya'nın adı|Ib|derin|
zeki|zeki|A|derin|
zeliha|Hz. Yusuf kıssasındaki Züleyha|A|tatli|
zerrin|altından, altın renkli|F|isik|
zeynep|değerli taş; güzel kokulu ağaç|A|asil|
ziya|ışık|A|isik|
zübeyde|öz, seçkin|A|asil|
züleyha|Hz. Yusuf kıssasının kahramanı|Ib|tatli|
zümra|topluluk|A|toprak|
nesibe|soylu|A|asil|
ayşe|yaşayan, hayat dolu|A|nese|
emine|güvenilir|A|toprak|
hilmi|yumuşak huylu|A|tatli|
nihat|tabiat, yaratılış|F|toprak|
ercan|er ve can|TF|guc|
erkan|erlerin kanından|T|guc|
gürkan|gür kanlı, güçlü|T|guc|
özcan|öz can|TF|nese|
kaan|hükümdar|T|asil|
umay|Türk inancında koruyucu kadın ruhu|T|gok|Eski Türklerde çocukları ve anneleri koruyan iyilik ruhu.
almira|prenses|A|asil|
alina|ışıltılı, soylu|Y|isik|
ada|ada|T|su|
lina|palmiye; narin|A|cicek|
lara|neşeli; Lara plajı|L|nese|
mila|sevgili, sevimli|S|tatli|
sare|saf, temiz|F|isik|
nehir|nehir|A|su|
masal|masal|T|gok|
ecrin|ödül|A|isik|
eflin|ılık rüzgâr|T|ruzgar|
duru|berrak|T|su|
asude|sakin, huzurlu|F|su|
öykü|hikâye|T|derin|
zümrüt|yeşil değerli taş|A|asil|
mercan|mercan|A|su|
inci|inci|T|su|
derin|derin|T|derin|
alya|yüce, yüksek|A|gok|
eymen|uğurlu, kutlu|A|nese|
miraç|göğe yükseliş|A|gok|
aras|Aras nehri|T|su|
çınar|çınar ağacı|F|toprak|
kerem|cömertlik|A|asil|
yağız|yiğit, esmer|T|guc|
ayaz|açık soğuk hava|T|ruzgar|
alparslan|yiğit aslan|T|guc|
eymen|uğurlu|A|nese|
göktuğ|göğün sancağı|T|gok|
emir|buyruk|A|asil|
ömer asaf|yaşayan ve bilge|A|asil|
mert|yiğit|F|guc|
kuzey|kuzey yönü|T|ruzgar|
deniz|deniz|T|su|
barış|barış|T|tatli|
umut|umut|T|isik|
batu|sağlam|T|guc|
egemen|bağımsız, hâkim|T|asil|
tuna|Tuna nehri|T|su|
koray|ateşli ay|T|ates|
cenk|savaş|F|guc|
cenker|savaşçı er|FT|guc|
çetin|zorlu, dayanıklı|T|guc|
gürsel|gür sel, coşkun|T|su|
gürol|güçlü ol|T|guc|
hakan|hükümdar|T|asil|
kutlu|kutlu, uğurlu|T|nese|
mete|Hun hükümdarı Mete Han|T|asil|
oya|iğne oyası|T|cicek|
serpil|serpilip gelişen|T|cicek|
sevtap|sevgi dolu|T|tatli|
tijen|güzel|T|tatli|
ufuk|ufuk|A|gok|
ünzile|indirilmiş|A|gok|
yonca|yonca|T|cicek|
alev|alev|T|ates|
ateş|ateş|F|ates|
güneş|güneş|T|isik|
aynur|ay ışığı|TA|isik|
şafak|şafak|A|isik|
seher|tan vakti|A|isik|
gülbin|bin gül|F|cicek|
gülnur|gül ışığı|FA|cicek|
nurgül|ışık gülü|AF|cicek|
gülizar|gül yanaklı|F|cicek|
ahmet|çok övülen|A|asil|
ali|yüce|A|asil|
yaşar|yaşayan|T|nese|
valeriya|güçlü, sağlıklı|L|guc|Latince valere (güçlü olmak) kökünden gelen Valeria adının Rusça söylenişi.
valeria|güçlü, sağlıklı|L|guc|Latince valere (güçlü olmak) kökünden.
valeri|güçlü, sağlıklı|L|guc|
valentina|güçlü, sağlıklı|L|guc|Latince valens (güçlü) kökünden.
anna|lütuf, zarafet|Ib|tatli|İbranice Hanna adından.
anastasia|yeniden doğuş|Y|isik|
anastasiya|yeniden doğuş|Y|isik|
natalia|doğum günü; Noel'de doğan|L|isik|
natalya|doğum günü; Noel'de doğan|L|isik|
nataşa|doğum günü; Noel'de doğan|L|isik|
olga|kutsal, mübarek|Is|asil|
elena|ışık, parlak|Y|isik|
yelena|ışık, parlak|Y|isik|
helen|ışık, parlak|Y|isik|
irina|barış|Y|tatli|
irena|barış|Y|tatli|
ekaterina|saf, temiz|Y|isik|
katerina|saf, temiz|Y|isik|
maria|deniz damlası; sevilen|Ib|su|
mariya|deniz damlası; sevilen|Ib|su|
marina|denizden gelen|L|su|
sofia|bilgelik|Y|derin|
sofya|bilgelik|Y|derin|
sophia|bilgelik|Y|derin|
victoria|zafer|L|guc|
viktoriya|zafer|L|guc|
tatiana|Tatius soyundan; düzen|L|asil|
tatyana|Tatius soyundan; düzen|L|asil|
svetlana|ışıklı, aydınlık|S|isik|
lyudmila|halkın sevgilisi|S|tatli|
ludmila|halkın sevgilisi|S|tatli|
oksana|misafirperver|Y|tatli|
alina|soylu, ışıltılı|Al|isik|
alexandra|insanları koruyan|Y|guc|
aleksandra|insanları koruyan|Y|guc|
alexander|insanları koruyan|Y|guc|
aleksandr|insanları koruyan|Y|guc|
daria|iyiliğe sahip olan|F|asil|
darya|iyiliğe sahip olan; deniz|F|su|
polina|güneş tanrısı Apollon'a ait|Y|isik|
kristina|Hristiyan|Y|isik|
julia|genç, taze|L|nese|
yulia|genç, taze|L|nese|
eva|hayat veren|Ib|nese|
diana|ilahi, göksel|L|gok|
nadia|umut|S|isik|
nadya|umut|S|isik|
nadejda|umut|S|isik|
vera|inanç; gerçek|S|derin|
milena|sevgili, zarif|S|tatli|
mila|sevgili|S|tatli|
lilia|zambak|L|cicek|
liliya|zambak|L|cicek|
lily|zambak|L|cicek|
rose|gül|L|cicek|
rosa|gül|L|cicek|
emma|bütün, evrensel|Al|toprak|
emily|çalışkan|L|toprak|
olivia|zeytin ağacı|L|toprak|
amelia|çalışkan|Al|toprak|
charlotte|özgür|Fr|ruzgar|
chloe|yeşil filiz|Y|cicek|
grace|zarafet|L|tatli|
isabella|ant içmiş, adanmış|Ib|asil|
mia|benim; sevgili|It|tatli|
nina|küçük kız; zarif|S|tatli|
laura|defne|L|cicek|
lucia|ışık|L|isik|
luna|ay|L|gok|
stella|yıldız|L|gok|
estella|yıldız|L|gok|
aurora|şafak|L|isik|
selena|ay|Y|gok|
irene|barış|Y|tatli|
margarita|inci|Y|su|
dmitri|toprak ana Demeter'e adanmış|Y|toprak|
dmitry|toprak ana Demeter'e adanmış|Y|toprak|
ivan|Tanrı lütufkârdır|Ib|tatli|
mikhail|Tanrı'ya benzer kim var|Ib|gok|
sergey|hizmetkâr; koruyucu|L|toprak|
andrey|cesur, erkekçe|Y|guc|
andrei|cesur, erkekçe|Y|guc|
nikolai|halkın zaferi|Y|guc|
nikolay|halkın zaferi|Y|guc|
vladimir|dünyayı yöneten|S|asil|
pavel|küçük, alçakgönüllü|L|toprak|
igor|savaşçı|Is|guc|
oleg|kutsal|Is|asil|
maxim|en büyük|L|guc|
maksim|en büyük|L|guc|
artem|sağlam, sağlıklı|Y|guc|
artyom|sağlam, sağlıklı|Y|guc|
denis|Dionysos'a adanmış|Y|nese|
roman|Romalı|L|asil|
anton|paha biçilmez|L|asil|
yuri|çiftçi|Y|toprak|
george|çiftçi, toprak işleyen|Y|toprak|
david|sevgili|Ib|tatli|
daniel|Tanrı yargıçtır|Ib|derin|
michael|Tanrı'ya benzer kim var|Ib|gok|
john|Tanrı lütufkârdır|Ib|tatli|
peter|kaya|Y|guc|
thomas|ikiz|Ar|farkli|
james|topuktan tutan|Ib|farkli|
lucas|ışık|L|isik|
leo|aslan|L|guc|
leon|aslan|Y|guc|
luka|ışık|L|isik|
mark|savaşçı|L|guc|
marko|savaşçı|L|guc|
noah|huzur, dinlenme|Ib|su|
adam|toprak|Ib|toprak|
sebastian|saygıdeğer|Y|asil|
nino|sevgili|Gr|tatli|Gürcülerin aziz kabul ettiği Nino'nun adı.
tamara|hurma ağacı|Ib|toprak|Gürcistan'ın en ünlü kraliçesinin adı.
giorgi|çiftçi|Gr|toprak|
nana|sevgili, anne|Gr|tatli|
mzia|güneş|Gr|isik|
havva|hayat veren; ilk kadın|Ib|nese|Hz. Havva'nın adı.
hayriye|hayırlı, iyilik dolu|A|tatli|
şükran|şükür, minnet|A|tatli|
arzu|istek, dilek|F|tatli|
musa|sudan çıkarılmış|Ib|su|Hz. Musa'nın adı.
asiye|teselli eden|A|tatli|
ismet|namus, temizlik|A|isik|
döndü|geri döndü; dönüş|T|toprak|
keziban|hanım, ev hanımı|T|toprak|
muzaffer|zafer kazanmış|A|guc|
şaban|Şaban ayı|A|asil|
arif|bilen, anlayışlı|A|derin|
nuriye|ışıklı|A|isik|
sedat|doğruluk|A|asil|
remziye|simgeli, anlamlı|A|derin|
selahattin|dinin iyiliği|A|asil|Kudüs'ü alan Selahaddin Eyyubi'nin adı.
hanım|hanım, kadın|T|asil|
zekiye|zeki, temiz|A|derin|
perihan|perilerin hükümdarı|F|gok|
yeter|yeter, yeterli|T|toprak|
nazmiye|düzenli, şiirli|A|nese|
emrah|yol gösteren|F|tatli|
huriye|cennet kızı|A|gok|
hikmet|bilgelik|A|derin|
makbule|kabul edilmiş, beğenilen|A|tatli|
isa|Hz. İsa'nın adı; kurtarıcı|Ib|isik|
nuran|ışıklı, parlak|A|isik|
muharrem|Muharrem ayı; kutsal|A|asil|
ayfer|ay ışıltısı|TF|gok|
nurettin|dinin ışığı|A|isik|
hamide|övülen|A|asil|
güllü|güllü, gül gibi|FT|cicek|
meliha|güzel, sevimli|A|tatli|
neriman|yiğit, cesur|F|guc|
rahime|merhametli|A|tatli|
irfan|bilgi, kültür|A|derin|
kazım|öfkesini yenen|A|toprak|
saadet|mutluluk|A|nese|
ihsan|iyilik, bağış|A|tatli|
müzeyyen|süslenmiş|A|cicek|
abdulkadir|Kadir olan Allah'ın kulu|A|guc|
hediye|armağan|A|tatli|
arife|bilen, tanıyan; bayram arifesi|A|derin|
gülseren|gül seren, gül saçan|FT|cicek|
melahat|güzellik, sevimlilik|A|tatli|
sadiye|mutlu|A|nese|
muammer|uzun ömürlü|A|toprak|
zahide|dünyadan el etek çekmiş|A|derin|
nazife|temiz|A|isik|
nimet|lütuf, bolluk|A|tatli|
veysel|Veysel Karani; dost|A|toprak|
fikriye|düşünceli|A|derin|
birgül|tek gül|TF|cicek|
elmas|elmas|A|asil|
cennet|cennet|A|cicek|
nevzat|yeni doğan|F|isik|
reyhan|fesleğen|A|cicek|
hafize|koruyan, ezberleyen|A|derin|
sebahat|güzellik, yüz aklığı|A|isik|
habibe|sevgili|A|tatli|
raziye|razı olan, hoşnut|A|tatli|
şükriye|şükreden|A|tatli|
bedriye|dolunay gibi|A|gok|
nebahat|uyanıklık, soyluluk|A|asil|
durmuş|yaşayan, kalıcı|T|toprak|
semiha|cömert|A|tatli|
kıymet|değer|A|asil|
enver|çok parlak, nurlu|A|isik|
şenay|şen ay|T|gok|
nilgün|Nil gibi güzel gün|T|su|
servet|zenginlik|A|asil|
selda|yürek, gönül|F|tatli|
niyazi|yalvaran, dilekçi|F|tatli|
birsen|bir tanesin|T|tatli|
hatun|hanım, soylu kadın|T|asil|
idris|Hz. İdris'in adı; çok okuyan|A|derin|
tahsin|güzelleştirme, beğenme|A|tatli|
eyüp|Hz. Eyüp'ün adı; sabırlı|Ib|toprak|
haydar|aslan|A|guc|Hz. Ali'nin lakabı.
aliye|yüce|A|asil|
nejla|geniş gözlü|A|derin|
sabriye|sabırlı|A|toprak|
gülizar|gül yanaklı|F|cicek|
suzan|yakan, yanan|F|ates|
sakine|sakin, huzurlu|A|su|
cuma|cuma günü; toplanma|A|asil|
fevzi|zafer, kurtuluş|A|guc|
yalçın|sarp, dik|T|guc|
kamile|olgun, eksiksiz|A|derin|
soner|son yiğit|T|guc|
öznur|öz ışık|TA|isik|
nursen|ışıksın|AT|isik|
nezahat|temizlik, saflık|A|isik|
turgut|ayakta duran, kalıcı|T|guc|
hasibe|soylu, değerli|A|asil|
yücel|yücel, yüksel|T|gok|
hamit|şükreden, öven|A|asil|
izzet|değer, saygınlık|A|asil|
salim|sağlam, esen|A|guc|
saime|oruçlu|A|derin|
naime|nimet içinde yaşayan|A|tatli|
fuat|gönül, yürek|A|tatli|
rıdvan|hoşnutluk; cennet kapısı|A|cicek|
adile|adaletli|A|asil|
sait|mutlu|A|nese|
fahrettin|dinin övüncü|A|asil|
fahriye|övünç, onur|A|asil|
şefika|şefkatli|A|tatli|
zuhal|Satürn gezegeni|A|gok|
figen|feryat eden; içli|F|derin|
mevlüde|doğmuş|A|isik|
sabiha|sabah güzeli|A|isik|
duran|duran, kalıcı|T|toprak|
ergun|olgun|T|toprak|
kasım|bölüştüren; kasım ayı|A|toprak|
fidan|fidan|T|cicek|
dilber|gönül alan, güzel|F|tatli|
beyhan|bey ve han, soylu|T|asil|
senem|güzel, put gibi güzel|A|tatli|
resul|elçi|A|asil|
necmettin|dinin yıldızı|A|gok|
şerif|şerefli|A|asil|
önder|önder|T|guc|
muhittin|dini dirilten|A|asil|
selami|esenlikle ilgili|A|tatli|
hidayet|doğru yol|A|isik|
yahya|Hz. Yahya'nın adı; yaşar|Ib|nese|
gülşah|güllerin şahı|F|cicek|
mukaddes|kutsal|A|asil|
şakir|şükreden|A|tatli|
necdet|yiğitlik, cesaret|A|guc|
şeref|onur|A|asil|
seval|soru|A|derin|
nazım|düzenleyen; şair|A|nese|
rıfat|yücelik|A|asil|
günay|gün ve ay|T|isik|
birol|bir ol, eşsiz ol|T|asil|
asuman|gökyüzü|F|gok|
kudret|güç|A|guc|
vesile|aracı, yol|A|tatli|
tevfik|başarı, uygunluk|A|isik|
azime|kararlı|A|guc|
bahriye|denizle ilgili|A|su|
firdevs|cennet bahçesi|A|cicek|
seyfettin|dinin kılıcı|A|guc|
hüsnü|güzellikle ilgili|A|tatli|
halise|saf, temiz|A|isik|
satılmış|adanmış|T|toprak|
selime|sağlam, kusursuz|A|guc|
nurdan|ışıktan|AT|isik|
cüneyt|küçük asker|A|guc|
naile|ulaşan, kavuşan|A|tatli|
muhsin|iyilik eden|A|tatli|
vildan|cennet hizmetkârları; çocuklar|A|gok|
nazmi|düzenli; şiirle ilgili|A|nese|
mediha|övülmüş|A|asil|
müslüm|Müslüman, teslim olan|A|toprak|
samet|ebedî, sonsuz|A|derin|
zöhre|Venüs gezegeni; parlak|A|gok|
fırat|Fırat nehri|A|su|
nedim|sohbet arkadaşı|A|nese|Lale Devri şairi Nedim'in adı.
süreyya|Ülker yıldız kümesi|A|gok|
handan|güleç|F|nese|
sabahat|güzellik, yüz aklığı|A|isik|
özgül|öz gül|TF|cicek|
sefer|yolculuk|A|ruzgar|
naci|kurtulmuş|A|isik|
bünyamin|Hz. Yakup'un oğlu; uğurlu oğul|Ib|nese|
nezaket|incelik|A|tatli|
cevat|cömert|A|tatli|
aysen|ay gibisin|T|gok|
eşref|en şerefli|A|asil|
güner|güneş gibi yiğit|T|isik|
ferdi|tek, eşsiz|A|asil|
aykut|kutlu ay|T|gok|
gülistan|gül bahçesi|F|cicek|
gülser|gül başlı; güllerin başı|F|cicek|
nagihan|ansızın|F|farkli|
fikri|düşünceyle ilgili|A|derin|
ilhami|ilhamla ilgili|A|gok|
sezai|layık|A|asil|
erdinç|er dinç, güçlü|T|guc|
selver|kavak; uzun boylu|F|toprak|
bedia|eşsiz güzel|A|tatli|
adalet|adalet|A|asil|
nurullah|Allah'ın nuru|A|isik|
münire|parlak, aydınlık|A|isik|
neziha|temiz, saf|A|isik|
nurhayat|hayatın ışığı|A|isik|
çiçek|çiçek|T|cicek|
nusret|yardım, zafer|A|guc|
alaattin|dinin yüceliği|A|asil|
asım|koruyan|A|guc|
nalan|inleyen, ağlayan|F|derin|
serdal|ser dal, baş dal|FT|toprak|
faik|üstün|A|asil|
necmi|yıldızla ilgili|A|gok|
olcay|mutluluk, talih|T|nese|
necip|soylu|A|asil|
gündoğdu|gün doğdu|T|isik|
selvi|servi ağacı|F|toprak|
bircan|tek can|TF|nese|
mürüvvet|insanlık, cömertlik|A|tatli|
didem|gözüm|F|tatli|
hıdır|Hızır; yeşil, bereket|A|cicek|
talip|isteyen|A|tatli|
banu|hanım, kadın|F|asil|
refik|arkadaş, yoldaş|A|tatli|
zarife|zarif, nazik|A|tatli|
halim|yumuşak huylu|A|tatli|
gurbet|gurbet|A|derin|
nefise|değerli, güzel|A|asil|
berrin|en temiz, saf|A|isik|
gülümser|gülümseyen|T|nese|
şehriban|şehrin hanımı|F|asil|
menekşe|menekşe|F|cicek|
mümin|inanan|A|toprak|
mükerrem|saygın, değerli|A|asil|
abdulkerim|Kerim olan Allah'ın kulu|A|asil|
gözde|en sevilen|T|tatli|
fethi|fetihle ilgili|A|guc|
raşit|doğru yolda olan|A|asil|
halide|ölümsüz|A|derin|
reşit|ergin, doğru yolda|A|asil|
galip|üstün gelen|A|guc|
şevki|şevkle ilgili|A|ates|
yadigar|hatıra|F|tatli|
nadir|az bulunur, eşsiz|A|farkli|
şemsi|güneşle ilgili|A|isik|
mikail|baş meleklerden biri|Ib|gok|
binnaz|bin naz|TF|tatli|
mukadder|takdir edilmiş|A|derin|
lokman|Lokman Hekim; bilge|A|derin|
kerime|cömert, değerli|A|asil|
nergiz|nergis çiçeği|F|cicek|
zeynel|Zeynelabidin; süs|A|asil|
seçil|seçkin ol|T|asil|
müjgan|kirpikler|F|tatli|
şener|şen er|T|nese|
kiraz|kiraz|Y|cicek|
ender|pek az, nadir|F|farkli|
seyit|efendi, soylu|A|asil|
gazi|savaştan dönen kahraman|A|guc|
ömür|hayat, yaşam|A|nese|
özden|özden gelen, içten|T|tatli|
kamuran|bahtiyar, mutlu|F|nese|
kadri|değerli|A|asil|
turhan|soylu bey|T|asil|
mualla|yüce|A|asil|
haluk|iyi huylu|A|tatli|
mithat|övme, övgü|A|asil|
rüstem|İran destanlarının kahramanı|F|guc|
ethem|kara, esmer|A|derin|
mücahit|çaba gösteren|A|guc|
altun|altın|T|isik|
avni|yardımla ilgili|A|tatli|
ilgaz|Ilgaz dağı; akın|T|guc|
aysima|ay yüzlü|TF|gok|
simay|ay yüzlü|FT|gok|
asımgül|koruyan gül|AF|cicek|
bengü|sonsuz, ebedî|T|derin|
bengisu|ölümsüzlük suyu, ab-ı hayat|T|su|
ilkim|ilk kişi; ilkim|T|isik|
dilay|gönül ayı|FT|gok|
nisa|kadınlar|A|tatli|
öykü|hikâye|T|derin|
ezel|başlangıcı olmayan zaman|A|derin|
alaz|alev|T|ates|
kayra|lütuf|T|tatli|
aren|cesur, yiğit|T|guc|
ozan|şair|T|nese|
tibet|Tibet; yüksek ülke|T|gok|
kuzey|kuzey|T|ruzgar|
çağan|bayram|T|nese|
toygar|tarla kuşu|T|ruzgar|
tunahan|Tuna'nın hükümdarı|T|su|
yiğithan|yiğit hükümdar|T|guc|
kaan|hükümdar|T|asil|
metehan|Mete Han|T|asil|
hakan|hükümdar|T|asil|
sarper|sarp er, yiğit|T|guc|
cihangir|dünyayı fetheden|F|guc|
selenay|ay gibi|YT|gok|
duygu|duygu|T|tatli|
pelinsu|pelin ve su|T|su|
`;
  const fold = (s) => s.replace(/ç/g, 'c').replace(/ğ/g, 'g').replace(/ı/g, 'i').replace(/i̇/g, 'i').replace(/ö/g, 'o').replace(/ş/g, 's').replace(/ü/g, 'u').replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u');
  const DICT = {}, FOLD = {};
  RAW.split('\n').forEach((ln) => {
    const p = ln.trim().split('|'); if (p.length < 4 || !p[0]) return;
    const e = { meaning: p[1], origin: ORIGIN[p[2]] || p[2], group: p[3], note: p[4] || '', kind: 'dict' };
    if (!DICT[p[0]]) DICT[p[0]] = e;
    const f = fold(p[0]); if (!FOLD[f]) FOLD[f] = e;
  });

  // Kök yorumu: ön kökler ve son ekler (öz Türkçe ve Farsça bileşik adlar için)
  const PRE = [
    ['gök', 'gökyüzü', 'gok'], ['gün', 'gün, güneş', 'isik'], ['ay', 'ay', 'gok'], ['yıldız', 'yıldız', 'gok'], ['nur', 'ışık', 'isik'], ['gül', 'gül', 'cicek'],
    ['su', 'su', 'su'], ['deniz', 'deniz', 'su'], ['sel', 'sel, coşkun akış', 'su'], ['ser', 'baş, önde olan', 'asil'], ['can', 'can, ruh', 'nese'],
    ['alp', 'yiğit', 'guc'], ['er', 'yiğit, er', 'guc'], ['tan', 'şafak', 'isik'], ['tuğ', 'sancak', 'asil'], ['kut', 'kut, uğur', 'nese'],
    ['bil', 'bilgi', 'derin'], ['ilk', 'ilk', 'isik'], ['ak', 'ak, temiz', 'isik'], ['kara', 'güçlü, ulu', 'guc'], ['demir', 'demir', 'guc'],
    ['tay', 'tay, genç at', 'ruzgar'], ['bay', 'zengin, varlıklı', 'asil'], ['ata', 'ata', 'toprak'], ['öz', 'öz, saf', 'isik'], ['us', 'akıl', 'derin'],
    ['uz', 'usta', 'derin'], ['sev', 'sevgi', 'tatli'], ['bal', 'bal', 'tatli'], ['çağ', 'çağ, zaman', 'farkli'], ['dur', 'duru, berrak', 'su'],
    ['sim', 'gümüş', 'isik'], ['zer', 'altın', 'isik'], ['mah', 'ay', 'gok'], ['şah', 'hükümdar', 'asil'], ['dil', 'gönül', 'tatli'], ['naz', 'naz', 'tatli'],
    ['han', 'hükümdar', 'asil'], ['ece', 'kraliçe', 'asil'], ['yel', 'rüzgâr', 'ruzgar'], ['bora', 'fırtına', 'ruzgar'], ['kar', 'kar', 'ruzgar'],
    ['ateş', 'ateş', 'ates'], ['od', 'ateş', 'ates'], ['ılk', 'ılık', 'ruzgar'], ['bulut', 'bulut', 'gok'], ['yağmur', 'yağmur', 'su'], ['gür', 'gür, bereketli', 'guc'],
    ['ten', 'ten', 'tatli'], ['el', 'el, yurt', 'toprak'], ['ülkü', 'ideal', 'gok'], ['ön', 'ön, öncü', 'guc'], ['sun', 'sunan, armağan', 'tatli'],
    ['ırmak', 'ırmak', 'su'], ['nil', 'Nil, mavi', 'su'], ['mel', 'melek, zarif', 'tatli'], ['ayt', 'ay', 'gok'], ['şen', 'şen, neşeli', 'nese'],
  ];
  const SUF = [
    ['han', 'hükümdar', 'asil'], ['kan', 'kan, soy', 'asil'], ['can', 'can', 'nese'], ['nur', 'ışık', 'isik'], ['gül', 'gül', 'cicek'], ['su', 'su', 'su'],
    ['ay', 'ay', 'gok'], ['er', 'yiğit', 'guc'], ['tan', 'şafak', 'isik'], ['bay', 'zengin', 'asil'], ['bek', 'bey', 'asil'], ['bey', 'bey', 'asil'],
    ['alp', 'yiğit', 'guc'], ['tekin', 'prens', 'asil'], ['naz', 'naz', 'tatli'], ['dil', 'gönül', 'tatli'], ['şah', 'hükümdar', 'asil'], ['sel', 'sel', 'su'],
    ['nil', 'Nil, mavi', 'su'], ['gin', 'o niteliği taşıyan', null], ['gın', 'o niteliği taşıyan', null], ['kin', 'o niteliği taşıyan', null], ['kın', 'o niteliği taşıyan', null],
    ['gün', 'gün, güneş', 'isik'], ['ten', 'ten', 'tatli'], ['taç', 'taç', 'asil'], ['ece', 'kraliçe', 'asil'], ['çe', 'küçük, sevimli', null], ['ça', 'küçük, sevimli', null],
    ['tuğ', 'sancak', 'asil'], ['demir', 'demir', 'guc'], ['ata', 'ata', 'toprak'], ['naz', 'naz', 'tatli'], ['sun', 'sunan', 'tatli'], ['ışık', 'ışık', 'isik'], ['sima', 'yüz, çehre', 'tatli'], ['nay', 'ay', 'gok'], ['su', 'su', 'su'],
  ];
  const ADJ = {"sel": "sel gibi coşkun", "ser": "önde olan, öncü", "er": "yiğit, mert", "ay": "ay gibi parlak", "gün": "güneş gibi aydınlık", "gök": "gök gibi engin", "su": "su gibi berrak", "tan": "şafak gibi aydınlık", "can": "candan, içten", "alp": "yiğit, cesur", "bil": "bilgili, bilge", "kut": "kutlu, uğurlu", "ak": "ak, temiz", "sev": "sevecen", "öz": "özü temiz", "ilk": "ilk olan, öncü", "gür": "gür, bereketli", "demir": "demir gibi sağlam", "kara": "güçlü, ulu", "nur": "ışıl ışıl", "gül": "gül gibi", "bay": "varlıklı, cömert", "tuğ": "sancak taşıyan, önder", "us": "akıllı", "uz": "usta", "dur": "duru, berrak", "yel": "rüzgâr gibi", "şen": "şen, neşeli", "el": "halkına bağlı", "ön": "öncü", "sun": "cömert", "kar": "kar gibi ak", "od": "ateşli"};
  function roots(w) {
    let best = null;
    for (const [p, pm, pg] of PRE) {
      if (!w.startsWith(p) || w.length <= p.length) continue;
      const rest = w.slice(p.length);
      for (const [s, sm, sg] of SUF) {
        if (rest === s) { const c = { parts: [[p, pm], ['-' + s, sm]], group: pg || sg, score: p.length + s.length + 2 }; if (!best || c.score > best.score) best = c; }
      }
      const restDict = DICT[rest] || FOLD[fold(rest)];
      if (restDict && rest.length >= 2) { const c = { parts: [[p, pm], [rest, restDict.meaning]], group: pg || restDict.group, score: w.length + 1 }; if (!best || c.score > best.score) best = c; }
    }
    if (best) return best;
    for (const [s, sm, sg] of SUF) {
      if (!w.endsWith(s) || w.length - s.length < 2 || !sg) continue;
      const head = w.slice(0, w.length - s.length), hd = DICT[head] || FOLD[fold(head)];
      if (hd) return { parts: [[head, hd.meaning], ['-' + s, sm]], group: hd.group, score: w.length };
    }
    return null;
  }
  const cap = (s) => s.charAt(0).toLocaleUpperCase('tr') + s.slice(1);
  function rootsText(r) {
    const a = r.parts[0], b = r.parts[1];
    if (b[0].startsWith('-') && /niteliği/.test(b[1])) return cap(ADJ[a[0]] || a[1].split(', ').pop());
    if (b[0].startsWith('-') && /küçük/.test(b[1])) return 'Küçük, sevimli ' + a[1].split(',')[0];
    return cap(a[1].split(/[,;]/)[0]) + ' ve ' + b[1].split(/[,;]/)[0];
  }
  // Ses karakteri: ünlü uyumu ve sesli/sessiz dengesi (sözlükte olmayan adlar için yorum)
  function sound(w) {
    const v = w.match(/[aeıioöuü]/g) || [], front = v.filter((c) => 'eiöü'.includes(c)).length, round = v.filter((c) => 'oöuü'.includes(c)).length;
    const soft = (w.match(/[lmnyrvs]/g) || []).length, hard = (w.match(/[kptçşgbdz]/g) || []).length;
    const tone = front > v.length / 2 ? 'ince ve parlak' : 'derin ve sıcak';
    const flow = soft >= hard ? 'akıcı, yumuşak' : 'net, güçlü';
    const group = soft >= hard ? (front > v.length / 2 ? 'isik' : 'tatli') : (front > v.length / 2 ? 'ruzgar' : 'guc');
    return { text: 'Adının sesi ' + tone + '; ünsüzleri ' + flow + '.', group, round };
  }
  function lookup(raw) {
    const w = String(raw || '').trim().split(/\s+/)[0].toLocaleLowerCase('tr');
    if (!w) return null;
    const d = DICT[w] || FOLD[fold(w)];
    if (d) return Object.assign({ word: w }, d);
    const r = roots(w);
    if (r) return { word: w, kind: 'roots', meaning: rootsText(r), parts: r.parts, group: r.group || 'farkli', origin: 'Türkçe', note: '' };
    const s = sound(w);
    return { word: w, kind: 'sound', meaning: null, group: s.group, origin: null, note: s.text };
  }
  root.YildizNames = { lookup, size: Object.keys(DICT).length, ORIGIN, _dict: DICT };
})(typeof window !== 'undefined' ? window : globalThis);
