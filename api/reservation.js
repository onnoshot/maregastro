// Mare Gastro - Rezervasyon API (Node.js serverless, Vercel Blob)
// POST (public):   site formundan veya dashboard'dan gelen rezervasyon talebini kaydeder.
// GET (token):      tum talepleri listeler (dashboard okur).
// PATCH (token):    var olan bir talebi gunceller (durum, kisi, not, vb).
// DELETE (token):   bir talebi siler.
//
// Gerekli env: BLOB_READ_WRITE_TOKEN (Vercel Blob otomatik saglar), MARE_ADMIN_KEY
import { put, list, del } from '@vercel/blob';
import crypto from 'node:crypto';

const PREFIX = 'reservation/';
const STATUSES = ['Beklemede', 'Onaylandı', 'İptal Edildi', 'Tamamlandı'];

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

async function tgSend(text) {
  const token = process.env.TG_BOT_TOKEN, chatId = process.env.TG_CHAT_ID;
  if (!token || !chatId) return;
  try {
    await fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, text, parse_mode: 'HTML', disable_web_page_preview: true }),
    });
  } catch (e) { /* bildirim hatasi akisi bozmaz */ }
}

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') { cors(res); return res.status(204).end(); }

  if (req.method === 'POST') {
    let b;
    try { b = await readJson(req); } catch (e) { return send(res, 400, { error: 'Gecersiz istek' }); }
    for (const k of ['name', 'phone', 'date', 'time']) {
      if (!b[k] || !String(b[k]).trim()) return send(res, 400, { error: 'Eksik alan: ' + k });
    }
    const isManual = authed(req) && !!req.headers['x-admin-key'];
    const status = STATUSES.includes(b.status) ? b.status : (isManual ? 'Onaylandı' : 'Beklemede');
    const rec = {
      id: makeId(), createdAt: new Date().toISOString(),
      name: String(b.name).trim(), phone: String(b.phone).trim(), email: String(b.email || '').trim(),
      date: String(b.date).trim(), time: String(b.time).trim(),
      guests: Number(b.guests) || null, konaklama: String(b.konaklama || '').trim(),
      channel: String(b.channel || 'Doğrudan').trim().slice(0, 40),
      note: String(b.note || '').trim().slice(0, 500),
      status,
      source: isManual ? 'manual' : 'site',
      referrer: String(b.referrer || '').trim().slice(0, 300),
      utm: String(b.utm || '').trim().slice(0, 60),
    };
    try {
      await put(PREFIX + rec.id + '.json', JSON.stringify(rec), {
        access: 'public', contentType: 'application/json', addRandomSuffix: false,
        allowOverwrite: true, cacheControlMaxAge: 0,
      });
    } catch (e) {
      return send(res, 500, { error: 'Kayit yazilamadi: ' + (e.message || e) });
    }
    {
      await tgSend(
        '<b>Yeni Rezervasyon Talebi</b>' + (isManual ? ' (dashboard\'dan elle eklendi)' : ' (siteden)') + '\n' +
        'Ad Soyad: ' + rec.name + '\n' +
        'Telefon: ' + rec.phone + '\n' +
        (rec.email ? 'E-posta: ' + rec.email + '\n' : '') +
        'Tarih: ' + rec.date + '  Saat: ' + rec.time + '\n' +
        'Kisi: ' + (rec.guests || '-') + '  Konaklama: ' + (rec.konaklama || '-') + '\n' +
        'Kaynak: ' + rec.channel +
        (rec.note ? '\nNot: ' + rec.note : '')
      );
    }
    return send(res, 200, { ok: true, id: rec.id, item: rec });
  }

  if (req.method === 'GET') {
    if (!authed(req)) return send(res, 401, { error: 'Yetkisiz' });
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
      out.sort((a, b) => (b.createdAt || '').localeCompare(a.createdAt || ''));
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
      const editable = ['name', 'phone', 'email', 'date', 'time', 'guests', 'konaklama', 'channel', 'note', 'status'];
      const next = { ...cur };
      for (const k of editable) {
        if (b[k] === undefined) continue;
        if (k === 'guests') next.guests = Number(b.guests) || null;
        else if (k === 'status') next.status = STATUSES.includes(b.status) ? b.status : cur.status;
        else next[k] = String(b[k]).trim();
      }
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
