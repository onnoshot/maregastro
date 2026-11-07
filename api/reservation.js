// Mare Gastro - Rezervasyon API (Node.js serverless, Vercel Blob)
// POST (public):   site formundan veya dashboard'dan gelen rezervasyon talebini kaydeder.
// GET (token):      tum talepleri listeler (dashboard okur).
// GET ?meta=1 (token): kayitlari okumadan sadece sayi + degisiklik imzasi doner (hafif kontrol).
// PATCH (token):    var olan bir talebi gunceller (durum, kisi, not, vb).
// DELETE (token):   bir talebi siler.
//
// Gerekli env: BLOB_READ_WRITE_TOKEN (Vercel Blob otomatik saglar), MARE_ADMIN_KEY
import { put, list, del } from '@vercel/blob';
import crypto from 'node:crypto';
import { loadClosedDays } from './closed-days.js';
import { normalizePhone, withPhone } from './_lib/phone.js';

const PREFIX = 'reservation/';
const STATUSES = ['Beklemede', 'Onaylandı', 'İptal Edildi', 'Tamamlandı', 'Gelmedi'];
const DEDUP_WINDOW_MS = 10 * 60 * 1000;
const READ_CONCURRENCY = 16;
const READ_ATTEMPTS = 3;

// Ayni kisi/tarih/saat icin kisa sure icinde (cift tikla, retry, coklu sekme)
// tekrar POST gelirse yeni kayit acmak yerine mevcut kaydi dondur.
async function findRecentDuplicate(rec) {
  try {
    const now = Date.now();
    const candidates = [];
    let cursor;
    do {
      const page = await list({ prefix: PREFIX, cursor, limit: 1000 });
      for (const b of page.blobs) {
        if (b.pathname.endsWith('.json') && now - new Date(b.uploadedAt).getTime() <= DEDUP_WINDOW_MS) candidates.push(b);
      }
      cursor = page.cursor;
    } while (cursor);

    for (const b of candidates) {
      try {
        const r = await fetch(bust(b.url), { cache: 'no-store' });
        if (!r.ok) continue;
        const j = await r.json();
        if (j.name === rec.name && normalizePhone(j.phone).phone === rec.phone && j.date === rec.date &&
            j.time === rec.time && j.guests === rec.guests && j.konaklama === rec.konaklama) {
          return j;
        }
      } catch { /* bozuk kayit atla */ }
    }
  } catch { /* dedup basarisiz olursa normal akisa devam */ }
  return null;
}

// Site tarihi her dilde Turkce bicimde gonderir: "3 Kasım 2026".
const TR_AYLAR = ['ocak', 'şubat', 'mart', 'nisan', 'mayıs', 'haziran', 'temmuz', 'ağustos', 'eylül', 'ekim', 'kasım', 'aralık'];
function trDateToIso(s) {
  const m = String(s || '').trim().match(/^(\d{1,2})\s+(\S+)\s+(\d{4})$/);
  if (!m) return '';
  const mi = TR_AYLAR.indexOf(m[2].toLocaleLowerCase('tr-TR'));
  if (mi < 0) return '';
  return m[3] + '-' + String(mi + 1).padStart(2, '0') + '-' + m[1].padStart(2, '0');
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

async function listRecords() {
  const blobs = [];
  let cursor;
  do {
    const r = await list({ prefix: PREFIX, cursor, limit: 1000 });
    for (const b of r.blobs) if (b.pathname.endsWith('.json')) blobs.push(b);
    cursor = r.hasMore ? r.cursor : undefined;
  } while (cursor);
  return blobs;
}

// Eklenen, duzenlenen veya silinen her kayitta degisir.
function signature(blobs) {
  const parts = blobs.map((b) => b.pathname + ':' + new Date(b.uploadedAt).getTime()).sort();
  return crypto.createHash('sha1').update(parts.join('\n')).digest('hex');
}

// Gecici ag/sunucu hatalarinda yeniden dener. Liste ile okuma arasinda silinen (404)
// ve bozuk kayit icin { skip: true }, tum denemeler basarisizsa { failed: true } doner.
async function readRecord(blob) {
  for (let attempt = 1; attempt <= READ_ATTEMPTS; attempt++) {
    try {
      const r = await fetch(bust(blob.url), { cache: 'no-store' });
      if (r.status === 404) return { skip: true };
      if (r.ok) {
        const text = await r.text();
        try { return { item: JSON.parse(text) }; }
        catch (e) { console.error('Bozuk kayit:', blob.pathname); return { skip: true }; }
      }
    } catch (e) { /* yeniden dene */ }
    if (attempt < READ_ATTEMPTS) await new Promise((done) => setTimeout(done, 150 * attempt));
  }
  return { failed: true };
}

async function readRecords(blobs) {
  const results = new Array(blobs.length);
  let next = 0;
  async function worker() {
    while (next < blobs.length) {
      const i = next++;
      results[i] = await readRecord(blobs[i]);
    }
  }
  await Promise.all(Array.from({ length: Math.min(READ_CONCURRENCY, blobs.length) }, worker));
  return results;
}

async function tgSend(text) {
  const token = process.env.TG_BOT_TOKEN;
  const chatIds = String(process.env.TG_CHAT_ID || '').split(',').map(s => s.trim()).filter(Boolean);
  if (!token || !chatIds.length) return;
  await Promise.all(chatIds.map(chatId =>
    fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, text, parse_mode: 'HTML', disable_web_page_preview: true }),
    }).catch(() => { /* bildirim hatasi akisi bozmaz */ })
  ));
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
      name: String(b.name).trim(), phone: normalizePhone(b.phone).phone, email: String(b.email || '').trim(),
      date: String(b.date).trim(), time: String(b.time).trim(),
      guests: Number(b.guests) || null, konaklama: String(b.konaklama || '').trim(),
      channel: String(b.channel || 'Doğrudan').trim().slice(0, 40),
      note: String(b.note || '').trim().slice(0, 500),
      status,
      source: isManual ? 'manual' : 'site',
      referrer: String(b.referrer || '').trim().slice(0, 300),
      utm: String(b.utm || '').trim().slice(0, 60),
      utmMedium: String(b.utmMedium || '').trim().slice(0, 60),
      campaign: String(b.campaign || '').trim().slice(0, 80),
      term: String(b.term || '').trim().slice(0, 80),
      landing: String(b.landing || '').trim().slice(0, 120),
      click: String(b.click || '').trim().slice(0, 12),
      bill: Number(b.bill) > 0 ? Number(b.bill) : null,
      // 'paid' = reklamdan geldi, 'organic' = ucretsiz, '' = belirlenemedi.
      // Siteden gelen kayitlarda reklam click-id'leri / utm_medium'dan tureltilir,
      // dashboard'dan elle eklenende kullanici secer. Uydurma deger uretmiyoruz.
      adPaid: ['paid', 'organic'].includes(String(b.adPaid || '')) ? String(b.adPaid) : '',
    };
    if (!isManual) {
      // Panelden kapatilan gunlere siteden talep alinmaz (tum masalar dolu).
      const iso = trDateToIso(rec.date);
      if (iso) {
        try {
          if ((await loadClosedDays()).includes(iso)) {
            return send(res, 409, { error: 'Bu tarihte tum masalar dolu', closed: true });
          }
        } catch { /* kapali gun listesi okunamazsa talebi kaybetme */ }
      }
      const dup = await findRecentDuplicate(rec);
      if (dup) return send(res, 200, { ok: true, id: dup.id, item: withPhone(dup), dedup: true });
    }
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
        'Telefon: ' + normalizePhone(rec.phone).phoneDisplay + '\n' +
        (rec.email ? 'E-posta: ' + rec.email + '\n' : '') +
        'Tarih: ' + rec.date + '  Saat: ' + rec.time + '\n' +
        'Kisi: ' + (rec.guests || '-') + '  Konaklama: ' + (rec.konaklama || '-') + '\n' +
        'Kaynak: ' + rec.channel +
        (rec.note ? '\nNot: ' + rec.note : '')
      );
    }
    return send(res, 200, { ok: true, id: rec.id, item: withPhone(rec) });
  }

  if (req.method === 'GET') {
    if (!authed(req)) return send(res, 401, { error: 'Yetkisiz' });
    try {
      const blobs = await listRecords();
      const sig = signature(blobs);
      if (req.query && req.query.meta) return send(res, 200, { ok: true, count: blobs.length, sig });
      const results = await readRecords(blobs);
      const out = results.filter((x) => x.item).map((x) => withPhone(x.item));
      const failed = results.filter((x) => x.failed).length;
      if (failed) console.error('Okunamayan kayit sayisi:', failed, '/', blobs.length);
      out.sort((a, b) => (b.createdAt || '').localeCompare(a.createdAt || ''));
      return send(res, 200, { ok: true, count: out.length, items: out, sig, partial: failed > 0, failed });
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
      const editable = ['name', 'phone', 'email', 'date', 'time', 'guests', 'konaklama', 'channel', 'adPaid', 'note', 'status', 'bill'];
      const next = { ...cur };
      for (const k of editable) {
        if (b[k] === undefined) continue;
        if (k === 'guests') next.guests = Number(b.guests) || null;
        else if (k === 'bill') next.bill = Number(b.bill) > 0 ? Number(b.bill) : null;
        else if (k === 'status') next.status = STATUSES.includes(b.status) ? b.status : cur.status;
        else if (k === 'phone') next.phone = normalizePhone(b.phone).phone;
        else if (k === 'adPaid') next.adPaid = ['paid', 'organic'].includes(String(b.adPaid || '')) ? String(b.adPaid) : '';
        else next[k] = String(b[k]).trim();
      }
      next.updatedAt = new Date().toISOString();
      // Ilk durum degisikligi, talebe donus suresini olcer.
      if (!next.respondedAt && (cur.status || 'Beklemede') === 'Beklemede' && next.status !== 'Beklemede') next.respondedAt = next.updatedAt;
      await put(PREFIX + id + '.json', JSON.stringify(next), {
        access: 'public', contentType: 'application/json', addRandomSuffix: false,
        allowOverwrite: true, cacheControlMaxAge: 0,
      });
      return send(res, 200, { ok: true, item: withPhone(next) });
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
