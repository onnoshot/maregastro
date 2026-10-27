// Mare Gastro - Kapali Gunler API (Node.js serverless, Vercel Blob)
// GET (public): kapatilmis gunlerin listesini doner (site takvimi okur).
// PUT (token):  { date: 'YYYY-MM-DD', closed: true|false } ile bir gunu kapatir / acar.
//
// Kapali gunlerde site takvimi o gunu "tum masalar dolu" olarak pasif gosterir,
// /api/reservation da siteden gelen talepleri reddeder.
// Gerekli env: BLOB_READ_WRITE_TOKEN (Vercel Blob otomatik saglar), MARE_ADMIN_KEY
import { put, list } from '@vercel/blob';

export const CLOSED_PATH = 'closed-days.json';
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

function cors(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, PUT, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, x-admin-key');
}
function send(res, status, body) {
  cors(res);
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
  res.setHeader('CDN-Cache-Control', 'no-store');
  res.setHeader('Vercel-CDN-Cache-Control', 'no-store');
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
function bust(url) { return url + (url.includes('?') ? '&' : '?') + '_cb=' + Date.now(); }

export async function loadClosedDays() {
  const r = await list({ prefix: CLOSED_PATH, limit: 1 });
  const hit = r.blobs.find((x) => x.pathname === CLOSED_PATH);
  if (!hit) return [];
  const j = await fetch(bust(hit.url), { cache: 'no-store' });
  if (!j.ok) return [];
  const data = await j.json();
  return Array.isArray(data.days) ? data.days.filter((d) => DATE_RE.test(d)) : [];
}

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') { cors(res); return res.status(204).end(); }

  if (req.method === 'GET') {
    try {
      const todayIso = new Date().toISOString().slice(0, 10);
      const all = await loadClosedDays();
      // Site icin gecmis gunler gereksiz; panel ?all=1 ile hepsini alir.
      const days = req.query && req.query.all ? all : all.filter((d) => d >= todayIso);
      return send(res, 200, { ok: true, days });
    } catch (e) {
      return send(res, 500, { error: 'Kapali gunler alinamadi: ' + (e.message || e) });
    }
  }

  if (req.method === 'PUT') {
    if (!authed(req)) return send(res, 401, { error: 'Yetkisiz' });
    let b;
    try { b = await readJson(req); } catch (e) { return send(res, 400, { error: 'Gecersiz istek' }); }
    const date = String((b && b.date) || '').trim();
    if (!DATE_RE.test(date)) return send(res, 400, { error: 'Gecersiz tarih (YYYY-MM-DD gerekli)' });
    try {
      const set = new Set(await loadClosedDays());
      if (b.closed) set.add(date); else set.delete(date);
      const days = [...set].sort();
      await put(CLOSED_PATH, JSON.stringify({ days, updatedAt: new Date().toISOString() }), {
        access: 'public', contentType: 'application/json', addRandomSuffix: false,
        allowOverwrite: true, cacheControlMaxAge: 0,
      });
      return send(res, 200, { ok: true, days });
    } catch (e) {
      return send(res, 500, { error: 'Kaydedilemedi: ' + (e.message || e) });
    }
  }

  return send(res, 405, { error: 'Method Not Allowed' });
}
