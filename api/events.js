// Mare Gastro - Etkinlik API (Node.js serverless, Vercel Blob)
// GET (public):     tum etkinlikleri listeler (site + dashboard okur, auth gerekmez).
// POST (token):     yeni etkinlik ekler (sadece dashboard).
// PATCH (token):    var olan bir etkinligi gunceller.
// DELETE (token):   bir etkinligi siler.
//
// Gerekli env: BLOB_READ_WRITE_TOKEN (Vercel Blob otomatik saglar), MARE_ADMIN_KEY
import { put, list, del } from '@vercel/blob';
import crypto from 'node:crypto';

const PREFIX = 'event/';
const CATEGORIES = ['ozel-gun', 'kampanya', 'etkinlik'];
const ICONS = ['star', 'sparkle', 'music', 'headphones', 'wine', 'utensils', 'gift'];
const HEX_RE = /^#[0-9a-fA-F]{6}$/;
function sanitizeColor(v, fallback) { return HEX_RE.test(v || '') ? v : fallback; }
function sanitizeRecurDays(v) {
  if (!Array.isArray(v)) return [];
  return [...new Set(v.map(Number).filter((n) => Number.isInteger(n) && n >= 0 && n <= 6))];
}
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
function sanitizeEndDate(v, date) {
  const s = String(v || '').trim();
  return DATE_RE.test(s) && s >= date ? s : '';
}

function cors(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS');
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
function makeId() { return crypto.randomBytes(8).toString('hex'); }
async function readJson(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const raw = Buffer.concat(chunks).toString('utf8');
  return raw ? JSON.parse(raw) : {};
}
function bust(url) { return url + (url.includes('?') ? '&' : '?') + '_cb=' + Date.now(); }

async function findBlob(id) {
  const path = PREFIX + id + '.json';
  const r = await list({ prefix: path, limit: 1 });
  return r.blobs.find((b) => b.pathname === path) || null;
}

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') { cors(res); return res.status(204).end(); }

  if (req.method === 'POST') {
    if (!authed(req)) return send(res, 401, { error: 'Yetkisiz' });
    let b;
    try { b = await readJson(req); } catch (e) { return send(res, 400, { error: 'Gecersiz istek' }); }
    for (const k of ['title', 'date']) {
      if (!b[k] || !String(b[k]).trim()) return send(res, 400, { error: 'Eksik alan: ' + k });
    }
    const rec = {
      id: makeId(), createdAt: new Date().toISOString(),
      title: String(b.title).trim().slice(0, 120),
      date: String(b.date).trim(),
      time: String(b.time || '').trim(),
      endDate: sanitizeEndDate(b.endDate, String(b.date).trim()),
      category: CATEGORIES.includes(b.category) ? b.category : 'etkinlik',
      icon: ICONS.includes(b.icon) ? b.icon : 'star',
      color: sanitizeColor(b.color, '#C8A96E'),
      description: String(b.description || '').trim().slice(0, 300),
      instagram_url: /^https:\/\//.test(b.instagram_url || '') ? String(b.instagram_url).trim().slice(0, 300) : '',
      recurring: !!b.recurring,
      recurDays: b.recurring ? sanitizeRecurDays(b.recurDays) : [],
    };
    try {
      await put(PREFIX + rec.id + '.json', JSON.stringify(rec), {
        access: 'public', contentType: 'application/json', addRandomSuffix: false,
        allowOverwrite: true, cacheControlMaxAge: 0,
      });
    } catch (e) {
      return send(res, 500, { error: 'Kayit yazilamadi: ' + (e.message || e) });
    }
    return send(res, 200, { ok: true, id: rec.id, item: rec });
  }

  if (req.method === 'GET') {
    try {
      const out = [];
      let cursor;
      do {
        const r = await list({ prefix: PREFIX, cursor, limit: 1000 });
        for (const it of r.blobs) {
          if (!it.pathname.endsWith('.json')) continue;
          try { const j = await fetch(bust(it.url), { cache: 'no-store' }); if (j.ok) out.push(await j.json()); }
          catch (e) { /* bozuk kayit atla */ }
        }
        cursor = r.cursor;
      } while (cursor);
      out.sort((a, b) => (a.date || '').localeCompare(b.date || '') || (a.time || '').localeCompare(b.time || ''));
      return send(res, 200, { ok: true, count: out.length, items: out });
    } catch (e) {
      return send(res, 500, { error: 'Liste alinamadi: ' + (e.message || e) });
    }
  }

  if (req.method === 'PATCH') {
    if (!authed(req)) return send(res, 401, { error: 'Yetkisiz' });
    let b;
    try { b = await readJson(req); } catch (e) { return send(res, 400, { error: 'Gecersiz istek' }); }
    const id = String(b.id || '').trim();
    if (!id) return send(res, 400, { error: 'id gerekli' });
    try {
      const blob = await findBlob(id);
      if (!blob) return send(res, 404, { error: 'Kayit bulunamadi' });
      const r = await fetch(bust(blob.url), { cache: 'no-store' });
      if (!r.ok) return send(res, 500, { error: 'Kayit okunamadi' });
      const cur = await r.json();
      const editable = ['title', 'date', 'time', 'endDate', 'category', 'icon', 'color', 'description', 'instagram_url', 'recurring', 'recurDays'];
      const next = { ...cur };
      for (const k of editable) {
        if (b[k] === undefined) continue;
        if (k === 'category') next.category = CATEGORIES.includes(b.category) ? b.category : cur.category;
        else if (k === 'icon') next.icon = ICONS.includes(b.icon) ? b.icon : cur.icon;
        else if (k === 'color') next.color = sanitizeColor(b.color, cur.color);
        else if (k === 'title') next.title = String(b.title).trim().slice(0, 120);
        else if (k === 'description') next.description = String(b.description).trim().slice(0, 300);
        else if (k === 'instagram_url') next.instagram_url = /^https:\/\//.test(b.instagram_url || '') ? String(b.instagram_url).trim().slice(0, 300) : '';
        else if (k === 'recurring') next.recurring = !!b.recurring;
        else if (k === 'recurDays') next.recurDays = sanitizeRecurDays(b.recurDays);
        else if (k === 'endDate') continue; // below, after date is finalized
        else next[k] = String(b[k]).trim();
      }
      next.endDate = sanitizeEndDate(b.endDate !== undefined ? b.endDate : next.endDate, next.date);
      if (!next.recurring) next.recurDays = [];
      next.updatedAt = new Date().toISOString();
      await put(PREFIX + id + '.json', JSON.stringify(next), {
        access: 'public', contentType: 'application/json', addRandomSuffix: false,
        allowOverwrite: true, cacheControlMaxAge: 0,
      });
      return send(res, 200, { ok: true, item: next });
    } catch (e) {
      return send(res, 500, { error: 'Guncellenemedi: ' + (e.message || e) });
    }
  }

  if (req.method === 'DELETE') {
    if (!authed(req)) return send(res, 401, { error: 'Yetkisiz' });
    let id = req.query && req.query.id;
    if (!id) { try { const b = await readJson(req); id = b.id; } catch (e) { /* yok say */ } }
    id = String(id || '').trim();
    if (!id) return send(res, 400, { error: 'id gerekli' });
    try {
      const blob = await findBlob(id);
      if (!blob) return send(res, 404, { error: 'Kayit bulunamadi' });
      await del(blob.url);
      return send(res, 200, { ok: true });
    } catch (e) {
      return send(res, 500, { error: 'Silinemedi: ' + (e.message || e) });
    }
  }

  return send(res, 405, { error: 'Method Not Allowed' });
}
