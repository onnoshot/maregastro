// Mare Gastro - Menu API (Node.js serverless, Vercel Blob)
// GET (public):  guncel menu-data.json'u doner (site + dashboard okur).
// PUT (token):   menu-data.json'u tumuyle degistirir (dashboard yazar).
//
// Gerekli env: BLOB_READ_WRITE_TOKEN (Vercel Blob otomatik saglar), MARE_ADMIN_KEY
import { put, list } from '@vercel/blob';

const PATH = 'menu/menu-data.json';

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
  if (!need) return true; // anahtar tanimli degilse acik (ilk kurulum)
  return req.headers['x-admin-key'] === need;
}
async function readJson(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const raw = Buffer.concat(chunks).toString('utf8');
  return raw ? JSON.parse(raw) : {};
}
// Blob CDN URL'i onbellekte tutar; taze veri icin cache-bust query ekleriz.
function bust(url) { return url + (url.includes('?') ? '&' : '?') + '_cb=' + Date.now(); }

async function loadMenu() {
  const res = await list({ prefix: PATH, limit: 1 });
  const hit = res.blobs.find((x) => x.pathname === PATH);
  if (!hit) return null;
  const r = await fetch(bust(hit.url), { cache: 'no-store' });
  return r.ok ? await r.json() : null;
}
async function saveMenu(data) {
  await put(PATH, JSON.stringify(data), {
    access: 'public', contentType: 'application/json', addRandomSuffix: false,
    allowOverwrite: true, cacheControlMaxAge: 0,
  });
}

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') { cors(res); return res.status(204).end(); }

  if (req.method === 'GET') {
    try {
      const data = await loadMenu();
      return send(res, 200, { ok: true, data });
    } catch (e) {
      return send(res, 500, { error: 'Menu alinamadi: ' + (e.message || e) });
    }
  }

  if (req.method === 'PUT') {
    if (!authed(req)) return send(res, 401, { error: 'Yetkisiz' });
    let b;
    try { b = await readJson(req); } catch (e) { return send(res, 400, { error: 'Gecersiz istek' }); }
    if (!b || !Array.isArray(b.groups) || !Array.isArray(b.categories) || !Array.isArray(b.items)) {
      return send(res, 400, { error: 'Gecersiz menu verisi (groups/categories/items gerekli)' });
    }
    try {
      b.updatedAt = new Date().toISOString();
      await saveMenu(b);
      return send(res, 200, { ok: true });
    } catch (e) {
      return send(res, 500, { error: 'Menu kaydedilemedi: ' + (e.message || e) });
    }
  }

  return send(res, 405, { error: 'Method Not Allowed' });
}
