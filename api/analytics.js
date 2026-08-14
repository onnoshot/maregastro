// Mare Gastro - Site trafik/ziyaretci istatistikleri (GA4 Data API)
// GET (token): dashboard'un Genel Bakis sayfasi icin ziyaretci sayisi + trafik kaynagi verisi.
//
// Gerekli env: GA_SA_JSON (Google servis hesabi JSON anahtari, analytics.readonly yetkili,
// bu GA4 property'de Goruntuleyici olarak eklenmis olmali), MARE_ADMIN_KEY
import { JWT } from 'google-auth-library';

const PROPERTY_ID = '542527885';

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

async function ga(token, body) {
  const r = await fetch(`https://analyticsdata.googleapis.com/v1beta/properties/${PROPERTY_ID}:runReport`, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error('ga4 ' + r.status + ' ' + (await r.text()).slice(0, 200));
  return r.json();
}

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') { cors(res); return res.status(204).end(); }
  if (req.method !== 'GET') return send(res, 405, { error: 'Method Not Allowed' });
  if (!authed(req)) return send(res, 401, { error: 'Yetkisiz' });
  if (!process.env.GA_SA_JSON) return send(res, 503, { error: 'GA_SA_JSON ayarli degil' });

  try {
    const sa = JSON.parse(process.env.GA_SA_JSON);
    const client = new JWT({ email: sa.client_email, key: sa.private_key, scopes: ['https://www.googleapis.com/auth/analytics.readonly'] });
    const { token } = await client.getAccessToken();

    const dailyR = await ga(token, {
      dateRanges: [{ startDate: '29daysAgo', endDate: 'today' }],
      dimensions: [{ name: 'date' }], metrics: [{ name: 'activeUsers' }],
      orderBys: [{ dimension: { dimensionName: 'date' } }],
    });
    const daily = (dailyR.rows || []).map((row) => {
      const d = row.dimensionValues[0].value;
      return { date: `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}`, users: parseInt(row.metricValues[0].value, 10) };
    });

    const totR = await ga(token, {
      dateRanges: [
        { startDate: 'today', endDate: 'today', name: 'today' },
        { startDate: '6daysAgo', endDate: 'today', name: 'd7' },
        { startDate: '29daysAgo', endDate: 'today', name: 'd30' },
      ], metrics: [{ name: 'activeUsers' }],
    });
    const totals = { today: 0, d7: 0, d30: 0 };
    (totR.rows || []).forEach((row) => { totals[row.dimensionValues[0].value] = parseInt(row.metricValues[0].value, 10); });

    const chR = await ga(token, {
      dateRanges: [{ startDate: '29daysAgo', endDate: 'today' }],
      dimensions: [{ name: 'sessionDefaultChannelGroup' }], metrics: [{ name: 'sessions' }],
      orderBys: [{ metric: { metricName: 'sessions' }, desc: true }], limit: 8,
    });
    const channels = (chR.rows || []).map((row) => ({ name: row.dimensionValues[0].value, sessions: parseInt(row.metricValues[0].value, 10) }));

    return send(res, 200, { ok: true, updatedAt: new Date().toISOString(), totals, daily, channels });
  } catch (e) {
    return send(res, 500, { error: 'GA4 verisi alinamadi: ' + (e.message || e) });
  }
}
