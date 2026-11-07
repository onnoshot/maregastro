// Mare Gastro - Site trafik/ziyaretci istatistikleri (GA4 Data API)
// GET (token): dashboard'un Genel Bakis sayfasi icin ziyaretci sayisi, trafik kaynagi,
// donusum event'leri (whatsapp_click/phone_click/availability_check/menu_click),
// en cok ziyaret edilen sayfalar ve cihaz dagilimi.
//
// Performans: tum raporlar tek bir batchRunReports cagrisinda toplanir (6 rapor / 1 istek),
// erisim token'i sicak lambda calistirmalari arasinda modul kapsaminda onbelleklenir.
//
// Gerekli env: GA_SA_JSON (Google servis hesabi JSON anahtari, analytics.readonly yetkili,
// bu GA4 property'de Goruntuleyici olarak eklenmis olmali), MARE_ADMIN_KEY
import { JWT } from 'google-auth-library';

const PROPERTY_ID = '542527885';
const CONVERSION_EVENTS = ['whatsapp_click', 'phone_click', 'availability_check', 'menu_click', 'reservation_submit_click'];

const INSIGHT_EVENTS = [...CONVERSION_EVENTS, 'form_start', 'form_details_start', 'form_error'];
// Ziyaretci yolculugu (2026-11-07'den itibaren): her adim ayri olay adi oldugu icin
// GA4'te ozel boyut tanimlamadan raporlanabilir.
const JOURNEY_STEPS = [
  ['view_story', 'Hikayeyi gördü'], ['view_chef', 'Şefi gördü'], ['view_signature', 'İmza tabaklara geldi'],
  ['view_menu', 'Menüye ulaştı'], ['menu_category_click', 'Menüde kategori açtı'], ['view_reviews', 'Yorumlara geldi'],
  ['view_occasions', 'Özel anlara geldi'], ['view_reservation', 'Rezervasyona ulaştı'], ['rez_date_select', 'Tarih seçti'],
  ['rez_step_2', 'Bilgi adımına geçti'], ['rez_step_3', 'Onay adımına geçti'], ['reservation_submit_click', 'WhatsApp ile onayladı'],
];
const JOURNEY_EXTRA = ['view_contact', 'menu_group_click', 'digital_menu_open', 'signature_dish_click', 'signature_all_menu_click',
  'occasion_click', 'reviews_more_click', 'events_info_open', 'rez_time_select', 'rez_guests_change', 'rez_stay_select',
  'language_switch', 'instagram_click', 'email_click', 'tripadvisor_click', 'didi_hotel_click', 'directions_click', 'blog_click',
  'whatsapp_click', 'phone_click', 'menu_click', 'availability_check', 'form_start', 'form_details_start', 'form_error',
  'engaged_30s', 'engaged_90s', 'engaged_180s', 'engaged_300s'];
const JOURNEY_EVENTS = [...JOURNEY_STEPS.map((x) => x[0]), ...JOURNEY_EXTRA];
const JOURNEY_SINCE = '2026-11-07';
let journeyCache = null;
let journeyCacheExpiry = 0;
const AI_SOURCES_RE = 'chatgpt|openai|perplexity|gemini|bard|copilot|claude|anthropic|deepseek|grok|meta\\.ai|you\\.com|mistral';
const SEARCH_SITES = ['sc-domain:maregastro.com', 'https://maregastro.com/', 'https://www.maregastro.com/'];

function cors(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, x-admin-key');
}
function send(res, status, body) {
  cors(res);
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
  res.status(status).setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify(body));
}
function authed(req) {
  const need = process.env.MARE_ADMIN_KEY || '';
  if (!need) return true;
  return req.headers['x-admin-key'] === need;
}

// Sicak lambda calistirmalari arasinda paylasilan modul-kapsamli token onbellegi.
let cachedToken = null;
let cachedTokenExpiry = 0;
let insightsCache = null;
let insightsCacheExpiry = 0;
let searchCache = null;
let searchCacheExpiry = 0;
async function getToken(sa) {
  if (cachedToken && Date.now() < cachedTokenExpiry) return cachedToken;
  const client = new JWT({ email: sa.client_email, key: sa.private_key, scopes: ['https://www.googleapis.com/auth/analytics.readonly'] });
  const { token } = await client.getAccessToken();
  cachedToken = token;
  cachedTokenExpiry = Date.now() + 50 * 60 * 1000; // Google token'lari ~1 saat gecerli, 50dk sonra yenile
  return token;
}

// Search Console: ayni servis hesabi, sitede kullanici olarak eklenmisse calisir.
async function searchReport(sa) {
  const client = new JWT({ email: sa.client_email, key: sa.private_key, scopes: ['https://www.googleapis.com/auth/webmasters.readonly'] });
  const { token } = await client.getAccessToken();
  const day = (n) => new Date(Date.now() - n * 864e5).toISOString().slice(0, 10);
  const query = async (site, body) => {
    const r = await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(site)}/searchAnalytics/query`, {
      method: 'POST', headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' }, body: JSON.stringify(body),
    });
    return { status: r.status, json: await r.json().catch(() => ({})) };
  };
  // Veri 2-3 gun gecikmeli gelir, pencere buna gore kaydirilir.
  const cur = { startDate: day(31), endDate: day(3) }, prev = { startDate: day(60), endDate: day(32) };
  for (const site of SEARCH_SITES) {
    const q = await query(site, { ...cur, dimensions: ['query'], rowLimit: 12 });
    if (q.status !== 200) continue;
    const [totals, before] = await Promise.all([query(site, cur), query(site, prev)]);
    return {
      ok: true, site, startDate: cur.startDate, endDate: cur.endDate,
      queries: (q.json.rows || []).map((x) => ({ query: x.keys[0], clicks: x.clicks, impressions: x.impressions, position: x.position })),
      totals: (totals.json.rows || [])[0] || {}, previous: (before.json.rows || [])[0] || {},
    };
  }
  return { ok: false, needsAccess: true };
}

async function gaBatch(token, requests) {
  const r = await fetch(`https://analyticsdata.googleapis.com/v1beta/properties/${PROPERTY_ID}:batchRunReports`, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' },
    body: JSON.stringify({ requests }),
  });
  if (!r.ok) throw new Error('ga4 ' + r.status + ' ' + (await r.text()).slice(0, 300));
  const j = await r.json();
  return j.reports || [];
}

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') { cors(res); return res.status(204).end(); }
  if (req.method !== 'GET') return send(res, 405, { error: 'Method Not Allowed' });
  if (!authed(req)) return send(res, 401, { error: 'Yetkisiz' });
  if (!process.env.GA_SA_JSON) return send(res, 503, { error: 'GA_SA_JSON ayarli degil' });

  try {
    const sa = JSON.parse(process.env.GA_SA_JSON);
    const token = await getToken(sa);

    // ── ?month=YYYY-MM → sadece o ayin trafik kaynagi kirilimi ──
    // Dashboard'un Aylik Rapor sayfasindaki "Ucretli / Ucretsiz Dagilimi" tablosu
    // bunu kullaniyor. Tek rapor doner, 30 gunluk genel bakis sorgularini calistirmaz.
    const monthParam = String((req.query && req.query.month) || '').trim();
    if (monthParam) {
      const m = monthParam.match(/^(\d{4})-(0[1-9]|1[0-2])$/);
      if (!m) return send(res, 400, { error: 'Gecersiz month (YYYY-MM bekleniyor)' });
      const y = Number(m[1]), mo = Number(m[2]);
      const startDate = `${m[1]}-${m[2]}-01`;
      // Ayin son gunu = bir sonraki ayin 0. gunu. Icinde bulundugumuz ay (veya ileri
      // bir ay) sorulursa GA4 gelecek tarihli endDate'i reddedebiliyor, o yuzden
      // bugune kirpiyoruz.
      const lastDay = new Date(Date.UTC(y, mo, 0)).getUTCDate();
      const monthEnd = `${m[1]}-${m[2]}-${String(lastDay).padStart(2, '0')}`;
      const todayIso = new Date().toISOString().slice(0, 10);
      const endDate = monthEnd > todayIso ? todayIso : monthEnd;
      if (endDate < startDate) return send(res, 200, { ok: true, month: monthParam, startDate, endDate: startDate, channels: [] });
      const [chOnlyR] = await gaBatch(token, [{
        dateRanges: [{ startDate, endDate }],
        dimensions: [{ name: 'sessionDefaultChannelGroup' }], metrics: [{ name: 'sessions' }],
        orderBys: [{ metric: { metricName: 'sessions' }, desc: true }], limit: 25,
      }]);
      const monthChannels = (chOnlyR.rows || []).map((row) => ({
        name: row.dimensionValues[0].value, sessions: parseInt(row.metricValues[0].value, 10),
      }));
      return send(res, 200, { ok: true, month: monthParam, startDate, endDate, channels: monthChannels });
    }

    // ── ?realtime=1 → son 30 dakika: su an sitede olanlar ve yaptiklari ──
    if (String((req.query && req.query.realtime) || '') === '1') {
      const rt = async (body) => {
        const r = await fetch(`https://analyticsdata.googleapis.com/v1beta/properties/${PROPERTY_ID}:runRealtimeReport`, {
          method: 'POST', headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' }, body: JSON.stringify(body),
        });
        if (!r.ok) throw new Error('ga4 realtime ' + r.status + ' ' + (await r.text()).slice(0, 200));
        return r.json();
      };
      const [tot, dev, geo, evs, pages] = await Promise.all([
        rt({ metrics: [{ name: 'activeUsers' }] }),
        rt({ dimensions: [{ name: 'deviceCategory' }], metrics: [{ name: 'activeUsers' }] }),
        rt({ dimensions: [{ name: 'city' }], metrics: [{ name: 'activeUsers' }], limit: 8 }),
        rt({ dimensions: [{ name: 'minutesAgo' }, { name: 'eventName' }], metrics: [{ name: 'eventCount' }], limit: 400 }),
        rt({ dimensions: [{ name: 'unifiedScreenName' }], metrics: [{ name: 'activeUsers' }], limit: 8 }),
      ]);
      const pairs = (rep) => (rep.rows || []).map((row) => ({ name: row.dimensionValues[0].value, value: Number(row.metricValues[0].value) }));
      const stream = (evs.rows || []).map((row) => ({ minutesAgo: Number(row.dimensionValues[0].value), name: row.dimensionValues[1].value, count: Number(row.metricValues[0].value) }))
        .filter((e) => !['session_start', 'first_visit', 'user_engagement', 'scroll', 'click'].includes(e.name))
        .sort((x, y) => x.minutesAgo - y.minutesAgo);
      const activeUsers = tot.rows && tot.rows[0] ? Number(tot.rows[0].metricValues[0].value) : 0;
      return send(res, 200, { ok: true, updatedAt: new Date().toISOString(), activeUsers, devices: pairs(dev), cities: pairs(geo), pages: pairs(pages), stream });
    }

    // ── ?journey=1 → Ziyaretci Yolculugu: adim adim huni, bolum erisimi, dil kirilimi, kalma suresi ──
    if (String((req.query && req.query.journey) || '') === '1') {
      if (journeyCache && Date.now() < journeyCacheExpiry) return send(res, 200, journeyCache);
      // Olcum 2026-11-07'de basladi: pencere en fazla 30 gun, ama bu tarihten once baslamaz
      // (aksi halde huni tabani 30 gunluk, adimlar birkac gunluk olur ve oranlar yaniltir).
      const iso = (t) => new Date(t).toISOString().slice(0, 10);
      const startMs = Math.max(Date.parse(JOURNEY_SINCE), Date.now() - 29 * 864e5);
      const spanDays = Math.round((Date.now() - startMs) / 864e5) + 1;
      const d30 = { startDate: iso(startMs), endDate: 'today' };
      const compare = [{ ...d30, name: 'cur' }, { startDate: iso(startMs - spanDays * 864e5), endDate: iso(startMs - 864e5), name: 'prev' }];
      const inList = { filter: { fieldName: 'eventName', inListFilter: { values: JOURNEY_EVENTS } } };
      const [evR, langR, baseR, dayR] = await gaBatch(token, [
        { dateRanges: compare, dimensions: [{ name: 'eventName' }], metrics: [{ name: 'totalUsers' }, { name: 'eventCount' }], dimensionFilter: inList, limit: 200 },
        { dateRanges: [d30], dimensions: [{ name: 'eventName' }, { name: 'pagePath' }], metrics: [{ name: 'totalUsers' }],
          dimensionFilter: { andGroup: { expressions: [
            { filter: { fieldName: 'eventName', inListFilter: { values: [...JOURNEY_STEPS.map((x) => x[0]), 'page_view'] } } },
            { filter: { fieldName: 'pagePath', inListFilter: { values: ['/tr/', '/en/', '/ar/', '/ru/'] } } },
          ] } }, limit: 500 },
        { dateRanges: compare, metrics: [{ name: 'totalUsers' }],
          dimensionFilter: { filter: { fieldName: 'pagePath', inListFilter: { values: ['/tr/', '/en/', '/ar/', '/ru/'] } } } },
        { dateRanges: [d30], dimensions: [{ name: 'date' }, { name: 'eventName' }], metrics: [{ name: 'totalUsers' }],
          dimensionFilter: { filter: { fieldName: 'eventName', inListFilter: { values: ['view_menu', 'view_reservation', 'rez_step_3', 'reservation_submit_click'] } } },
          orderBys: [{ dimension: { dimensionName: 'date' } }], limit: 400 },
      ]);
      const events = {};
      (evR.rows || []).forEach((row) => {
        const n = row.dimensionValues[0].value, period = row.dimensionValues[1].value;
        const o = events[n] = events[n] || { users: { cur: 0, prev: 0 }, count: { cur: 0, prev: 0 } };
        o.users[period] = Number(row.metricValues[0].value); o.count[period] = Number(row.metricValues[1].value);
      });
      const base = { cur: 0, prev: 0 };
      (baseR.rows || []).forEach((row) => { base[row.dimensionValues[0].value] = Number(row.metricValues[0].value); });
      const byLang = {};
      (langR.rows || []).forEach((row) => {
        const n = row.dimensionValues[0].value, lang = row.dimensionValues[1].value.replace(/\//g, '');
        (byLang[lang] = byLang[lang] || {})[n] = Number(row.metricValues[0].value);
      });
      const daily = (dayR.rows || []).map((row) => {
        const d = row.dimensionValues[0].value;
        return { date: `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}`, name: row.dimensionValues[1].value, users: Number(row.metricValues[0].value) };
      });
      journeyCache = { ok: true, updatedAt: new Date().toISOString(), since: JOURNEY_SINCE, startDate: d30.startDate, days: spanDays, steps: JOURNEY_STEPS, base, events, byLang, daily };
      journeyCacheExpiry = Date.now() + 5 * 60 * 1000;
      return send(res, 200, journeyCache);
    }

    if (String((req.query && req.query.search) || '') === '1') {
      if (searchCache && Date.now() < searchCacheExpiry) return send(res, 200, searchCache);
      const report = await searchReport(sa);
      if (report.ok) { searchCache = report; searchCacheExpiry = Date.now() + 30 * 60 * 1000; }
      return send(res, 200, report);
    }

    // ── ?insights=1 → Analiz sekmesi: saat/gun deseni, sehir, dil, giris sayfasi,
    // yeni-geri donen ayrimi ve onceki 30 gune gore karsilastirma. Sekme acilinca
    // istenir, dashboard ilk acilisini yavaslatmaz; 5 dk onbelleklenir.
    if (String((req.query && req.query.insights) || '') === '1') {
      if (insightsCache && Date.now() < insightsCacheExpiry) return send(res, 200, insightsCache);
      const d30 = { startDate: '29daysAgo', endDate: 'today' };
      const compare = [{ ...d30, name: 'cur' }, { startDate: '59daysAgo', endDate: '30daysAgo', name: 'prev' }];
      const top = (dim, metric, limit) => ({
        dateRanges: [d30], dimensions: [{ name: dim }], metrics: [{ name: metric }],
        orderBys: [{ metric: { metricName: metric }, desc: true }], limit,
      });
      const [[hourR, dowR, cityR, langR, nvrR], [landR, srcR, sumR, evCmpR, evDayR], [menuR, aiR]] = await Promise.all([
        gaBatch(token, [
          top('hour', 'activeUsers', 24), top('dayOfWeek', 'activeUsers', 7),
          top('city', 'sessions', 10), top('language', 'sessions', 6), top('newVsReturning', 'activeUsers', 3),
        ]),
        gaBatch(token, [
          { ...top('landingPage', 'sessions', 8), metrics: [{ name: 'sessions' }, { name: 'engagementRate' }] },
          top('sessionSourceMedium', 'sessions', 10),
          { dateRanges: compare, metrics: ['sessions', 'activeUsers', 'engagedSessions', 'averageSessionDuration', 'screenPageViewsPerSession'].map((name) => ({ name })) },
          {
            dateRanges: compare, dimensions: [{ name: 'eventName' }], metrics: [{ name: 'eventCount' }],
            dimensionFilter: { filter: { fieldName: 'eventName', inListFilter: { values: INSIGHT_EVENTS } } },
          },
          {
            dateRanges: [d30], dimensions: [{ name: 'date' }, { name: 'eventName' }], metrics: [{ name: 'eventCount' }],
            dimensionFilter: { filter: { fieldName: 'eventName', inListFilter: { values: CONVERSION_EVENTS } } },
            orderBys: [{ dimension: { dimensionName: 'date' } }], limit: 200,
          },
        ]),
        gaBatch(token, [{
          dateRanges: [d30], dimensions: [{ name: 'pageTitle' }], metrics: [{ name: 'eventCount' }],
          dimensionFilter: { filter: { fieldName: 'eventName', stringFilter: { value: 'menu_section_view' } } },
          orderBys: [{ metric: { metricName: 'eventCount' }, desc: true }], limit: 14,
        }, {
          // Yapay zeka asistanlarindan gelen ziyaretler (ChatGPT, Gemini, Perplexity, Copilot, Claude...)
          dateRanges: [{ startDate: '89daysAgo', endDate: 'today', name: 'cur' }, { startDate: '179daysAgo', endDate: '90daysAgo', name: 'prev' }],
          dimensions: [{ name: 'sessionSource' }, { name: 'landingPage' }], metrics: [{ name: 'sessions' }],
          dimensionFilter: { filter: { fieldName: 'sessionSource', stringFilter: { matchType: 'PARTIAL_REGEXP', value: AI_SOURCES_RE, caseSensitive: false } } },
          limit: 200,
        }]),
      ]);
      const pairs = (rep) => (rep.rows || []).map((row) => ({ name: row.dimensionValues[0].value, value: Number(row.metricValues[0].value) }));
      const summary = { cur: {}, prev: {} };
      (sumR.rows || []).forEach((row) => {
        const metrics = {};
        (sumR.metricHeaders || []).forEach((m, i) => { metrics[m.name] = Number(row.metricValues[i].value); });
        summary[row.dimensionValues[0].value] = metrics;
      });
      const eventCompare = {};
      (evCmpR.rows || []).forEach((row) => {
        const name = row.dimensionValues[0].value;
        eventCompare[name] = eventCompare[name] || { cur: 0, prev: 0 };
        eventCompare[name][row.dimensionValues[1].value] = Number(row.metricValues[0].value);
      });
      const eventDaily = (evDayR.rows || []).map((row) => {
        const d = row.dimensionValues[0].value;
        return { date: `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}`, name: row.dimensionValues[1].value, count: Number(row.metricValues[0].value) };
      });
      insightsCache = {
        ok: true, updatedAt: new Date().toISOString(),
        hours: pairs(hourR), weekdays: pairs(dowR), cities: pairs(cityR), languages: pairs(langR), audience: pairs(nvrR),
        landings: (landR.rows || []).map((row) => ({ path: row.dimensionValues[0].value, sessions: Number(row.metricValues[0].value), engagement: Number(row.metricValues[1].value) })),
        sources: pairs(srcR), summary, eventCompare, eventDaily, menuSections: pairs(menuR),
        aiVisits: (aiR.rows || []).map((row) => ({ source: row.dimensionValues[0].value, landing: row.dimensionValues[1].value, period: row.dimensionValues[2] ? row.dimensionValues[2].value : 'cur', sessions: Number(row.metricValues[0].value) })),
      };
      insightsCacheExpiry = Date.now() + 5 * 60 * 1000;
      return send(res, 200, insightsCache);
    }

    // GA4 batchRunReports istek basina en fazla 5 rapor kabul ediyor; 6 raporu
    // iki gruba bolup PARALEL (Promise.all) cagiriyoruz — sirali olsaydi 2x yavas olurdu.
    const [[dailyR, totR, chR], [evR, pageR, devR]] = await Promise.all([
      gaBatch(token, [
        { // 0: gunluk ziyaretci trendi
          dateRanges: [{ startDate: '29daysAgo', endDate: 'today' }],
          dimensions: [{ name: 'date' }], metrics: [{ name: 'activeUsers' }],
          orderBys: [{ dimension: { dimensionName: 'date' } }],
        },
        { // 1: bugun / 7 gun / 30 gun toplamlari
          dateRanges: [
            { startDate: 'today', endDate: 'today', name: 'today' },
            { startDate: '6daysAgo', endDate: 'today', name: 'd7' },
            { startDate: '29daysAgo', endDate: 'today', name: 'd30' },
          ], metrics: [{ name: 'activeUsers' }],
        },
        { // 2: trafik kaynaklari
          dateRanges: [{ startDate: '29daysAgo', endDate: 'today' }],
          dimensions: [{ name: 'sessionDefaultChannelGroup' }], metrics: [{ name: 'sessions' }],
          orderBys: [{ metric: { metricName: 'sessions' }, desc: true }], limit: 8,
        },
      ]),
      gaBatch(token, [
        { // 3: donusum event'leri
          dateRanges: [{ startDate: '29daysAgo', endDate: 'today' }],
          dimensions: [{ name: 'eventName' }], metrics: [{ name: 'eventCount' }],
          dimensionFilter: { filter: { fieldName: 'eventName', inListFilter: { values: CONVERSION_EVENTS } } },
        },
        { // 4: en cok ziyaret edilen sayfalar
          dateRanges: [{ startDate: '29daysAgo', endDate: 'today' }],
          dimensions: [{ name: 'pagePath' }], metrics: [{ name: 'screenPageViews' }],
          orderBys: [{ metric: { metricName: 'screenPageViews' }, desc: true }], limit: 10,
        },
        { // 5: cihaz dagilimi
          dateRanges: [{ startDate: '29daysAgo', endDate: 'today' }],
          dimensions: [{ name: 'deviceCategory' }], metrics: [{ name: 'activeUsers' }],
          orderBys: [{ metric: { metricName: 'activeUsers' }, desc: true }],
        },
      ]),
    ]);

    const daily = (dailyR.rows || []).map((row) => {
      const d = row.dimensionValues[0].value;
      return { date: `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}`, users: parseInt(row.metricValues[0].value, 10) };
    });

    const totals = { today: 0, d7: 0, d30: 0 };
    (totR.rows || []).forEach((row) => { totals[row.dimensionValues[0].value] = parseInt(row.metricValues[0].value, 10); });

    const channels = (chR.rows || []).map((row) => ({ name: row.dimensionValues[0].value, sessions: parseInt(row.metricValues[0].value, 10) }));

    const eventCounts = {};
    (evR.rows || []).forEach((row) => { eventCounts[row.dimensionValues[0].value] = parseInt(row.metricValues[0].value, 10); });
    const events = CONVERSION_EVENTS.map((name) => ({ name, count: eventCounts[name] || 0 }));

    const pages = (pageR.rows || []).map((row) => ({ path: row.dimensionValues[0].value, views: parseInt(row.metricValues[0].value, 10) }));

    const devices = (devR.rows || []).map((row) => ({ name: row.dimensionValues[0].value, users: parseInt(row.metricValues[0].value, 10) }));

    return send(res, 200, { ok: true, updatedAt: new Date().toISOString(), totals, daily, channels, events, pages, devices });
  } catch (e) {
    return send(res, 500, { error: 'GA4 verisi alinamadi: ' + (e.message || e) });
  }
}
