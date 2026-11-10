// Mare Gastro - QR Menu settings API (Vercel Blob)
// Holds only what the QR menu adds on top of menu-data.json: showcase sections
// (featured / best seller / chef's favourite) and per-item discounts.
// Kept separate from menu/menu-data.json so Menulux syncs (which PUT the whole
// menu) can never wipe discounts or showcases.
// GET (public): current settings.  PUT (x-admin-key): replace settings.
import { put, list } from '@vercel/blob';

const PATH = 'menu/qr-config.json';
const KINDS = ['featured', 'bestseller', 'chef'];

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

const str = (v, max) => String(v == null ? '' : v).slice(0, max);
const isDate = (v) => /^\d{4}-\d{2}-\d{2}$/.test(String(v || ''));

// Only known fields survive, so a bad client can't bloat or break the file.
function clean(b) {
  const showcases = (Array.isArray(b.showcases) ? b.showcases : [])
    .filter((s) => s && KINDS.includes(s.kind))
    .slice(0, 6)
    .map((s) => ({
      id: str(s.id || s.kind, 40),
      kind: s.kind,
      active: s.active !== false,
      title: str(s.title, 60),
      items: (Array.isArray(s.items) ? s.items : []).slice(0, 12)
        .filter((x) => x && x.id)
        .map((x) => ({ id: str(x.id, 120), tagline: str(x.tagline, 90) })),
    }));
  const discounts = {};
  const src = b.discounts && typeof b.discounts === 'object' ? b.discounts : {};
  Object.keys(src).slice(0, 150).forEach((id) => {
    const d = src[id] || {};
    const type = d.type === 'price' ? 'price' : 'percent';
    const value = Number(d.value);
    if (!Number.isFinite(value) || value <= 0) return;
    if (type === 'percent' && value >= 100) return;
    discounts[str(id, 120)] = {
      type, value,
      active: d.active !== false,
      until: isDate(d.until) ? d.until : '',
      label: str(d.label, 30),
    };
  });
  return { showcases, discounts };
}

async function load() {
  const res = await list({ prefix: PATH, limit: 1 });
  const hit = res.blobs.find((x) => x.pathname === PATH);
  if (!hit) return null;
  const r = await fetch(bust(hit.url), { cache: 'no-store' });
  return r.ok ? await r.json() : null;
}

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') { cors(res); return res.status(204).end(); }

  if (req.method === 'GET') {
    try {
      const data = await load();
      return send(res, 200, { ok: true, data: data || { showcases: [], discounts: {} } });
    } catch (e) {
      return send(res, 500, { error: 'QR ayarlari alinamadi: ' + (e.message || e) });
    }
  }

  if (req.method === 'PUT') {
    if (!authed(req)) return send(res, 401, { error: 'Yetkisiz' });
    let b;
    try { b = await readJson(req); } catch (e) { return send(res, 400, { error: 'Gecersiz istek' }); }
    if (!b || typeof b !== 'object') return send(res, 400, { error: 'Gecersiz veri' });
    try {
      const data = clean(b);
      data.updatedAt = new Date().toISOString();
      await put(PATH, JSON.stringify(data), {
        access: 'public', contentType: 'application/json', addRandomSuffix: false,
        allowOverwrite: true, cacheControlMaxAge: 0,
      });
      return send(res, 200, { ok: true, data });
    } catch (e) {
      return send(res, 500, { error: 'QR ayarlari kaydedilemedi: ' + (e.message || e) });
    }
  }

  return send(res, 405, { error: 'Method Not Allowed' });
}
