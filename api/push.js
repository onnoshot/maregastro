// Mare Gastro - Panel push bildirim aboneligi
// GET                      : VAPID public key (herkese acik, sir degil)
// POST   (token) {sub,label}: cihazi abone eder
// POST   (token) ?test=1    : {sub} cihazina deneme bildirimi yollar
// DELETE (token) {endpoint} : aboneligi siler
import { saveSub, removeSub, validSub, pushOne } from './_lib/push.js';

function cors(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, x-admin-key');
}
function send(res, status, body) {
  cors(res);
  res.setHeader('Cache-Control', 'no-store');
  res.status(status).setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify(body));
}
function authed(req) {
  const need = process.env.MARE_ADMIN_KEY || '';
  if (!need) return true;
  return req.headers['x-admin-key'] === need;
}
async function readJson(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const raw = Buffer.concat(chunks).toString('utf8');
  return raw ? JSON.parse(raw) : {};
}

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') { cors(res); return res.status(204).end(); }
  if (req.method === 'GET') return send(res, 200, { publicKey: process.env.VAPID_PUBLIC_KEY || '' });
  if (!authed(req)) return send(res, 401, { error: 'Yetkisiz' });

  let b;
  try { b = await readJson(req); } catch { return send(res, 400, { error: 'Gecersiz istek' }); }

  if (req.method === 'POST') {
    if (!validSub(b.sub)) return send(res, 400, { error: 'Gecersiz abonelik' });
    try {
      if (req.query && req.query.test) {
        await pushOne(b.sub, { title: 'Bildirimler açık', body: 'Yeni rezervasyon geldiğinde bu cihaza böyle haber verilecek.', tag: 'mare-test', url: '/#rez' });
      } else {
        await saveSub(b.sub, b.label);
      }
      return send(res, 200, { ok: true });
    } catch (e) {
      return send(res, 502, { error: 'Bildirim gonderilemedi: ' + (e.body || e.message || e) });
    }
  }

  if (req.method === 'DELETE') {
    if (!b.endpoint) return send(res, 400, { error: 'endpoint gerekli' });
    try { await removeSub(b.endpoint); return send(res, 200, { ok: true }); }
    catch (e) { return send(res, 500, { error: String(e.message || e) }); }
  }

  return send(res, 405, { error: 'Desteklenmeyen istek' });
}
