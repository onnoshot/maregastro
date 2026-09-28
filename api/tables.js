// Mare Gastro - Masa Duzeni API (Node.js serverless, Vercel Blob)
// GET  ?resource=layout               (token): masa yerlesim planini (fiziksel masalar) doner.
// PUT  ?resource=layout               (token): masa yerlesim planini tumuyle degistirir.
// GET  ?resource=plan&date=YYYY-MM-DD (token): o gune ait masa atamalarini doner.
// PUT  ?resource=plan&date=YYYY-MM-DD (token): o gune ait masa atamalarini tumuyle degistirir.
//
// Gerekli env: BLOB_READ_WRITE_TOKEN (Vercel Blob otomatik saglar), MARE_ADMIN_KEY
import { put, list } from '@vercel/blob';

const LAYOUT_PATH = 'tables/layout.json';
const PLAN_PREFIX = 'tables/plan/';
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

async function loadDoc(path) {
  const res = await list({ prefix: path, limit: 1 });
  const hit = res.blobs.find((x) => x.pathname === path);
  if (!hit) return null;
  const r = await fetch(bust(hit.url), { cache: 'no-store' });
  return r.ok ? await r.json() : null;
}
async function saveDoc(path, data) {
  await put(path, JSON.stringify(data), {
    access: 'public', contentType: 'application/json', addRandomSuffix: false,
    allowOverwrite: true, cacheControlMaxAge: 0,
  });
}

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') { cors(res); return res.status(204).end(); }
  if (!authed(req)) return send(res, 401, { error: 'Yetkisiz' });

  const resource = (req.query && req.query.resource) || 'layout';

  if (resource === 'layout') {
    if (req.method === 'GET') {
      try {
        const data = await loadDoc(LAYOUT_PATH);
        return send(res, 200, { ok: true, tables: (data && data.tables) || [] });
      } catch (e) {
        return send(res, 500, { error: 'Yerlesim alinamadi: ' + (e.message || e) });
      }
    }
    if (req.method === 'PUT') {
      let b;
      try { b = await readJson(req); } catch (e) { return send(res, 400, { error: 'Gecersiz istek' }); }
      if (!b || !Array.isArray(b.tables)) return send(res, 400, { error: 'Gecersiz yerlesim verisi (tables gerekli)' });
      try {
        await saveDoc(LAYOUT_PATH, { tables: b.tables, updatedAt: new Date().toISOString() });
        return send(res, 200, { ok: true });
      } catch (e) {
        return send(res, 500, { error: 'Yerlesim kaydedilemedi: ' + (e.message || e) });
      }
    }
    return send(res, 405, { error: 'Method Not Allowed' });
  }

  if (resource === 'plan') {
    const date = String((req.query && req.query.date) || '').trim();
    if (!DATE_RE.test(date)) return send(res, 400, { error: 'Gecersiz tarih (YYYY-MM-DD gerekli)' });
    const path = PLAN_PREFIX + date + '.json';

    if (req.method === 'GET') {
      try {
        const data = await loadDoc(path);
        return send(res, 200, { ok: true, date, assignments: (data && data.assignments) || {} });
      } catch (e) {
        return send(res, 500, { error: 'Plan alinamadi: ' + (e.message || e) });
      }
    }
    if (req.method === 'PUT') {
      let b;
      try { b = await readJson(req); } catch (e) { return send(res, 400, { error: 'Gecersiz istek' }); }
      if (!b || typeof b.assignments !== 'object' || Array.isArray(b.assignments) || b.assignments === null) {
        return send(res, 400, { error: 'Gecersiz plan verisi (assignments gerekli)' });
      }
      try {
        await saveDoc(path, { date, assignments: b.assignments, updatedAt: new Date().toISOString() });
        return send(res, 200, { ok: true });
      } catch (e) {
        return send(res, 500, { error: 'Plan kaydedilemedi: ' + (e.message || e) });
      }
    }
    return send(res, 405, { error: 'Method Not Allowed' });
  }

  return send(res, 400, { error: 'Bilinmeyen resource' });
}
