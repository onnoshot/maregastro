// Web Push: panelde "Bildirimleri aç" diyen her cihazin abonelik kaydi Blob'da
// push-subs/<hash>.json olarak durur. Yeni rezervasyonda hepsine bildirim gider;
// suresi dolmus (404/410) abonelikler otomatik silinir.
import webpush from 'web-push';
import { put, list, del } from '@vercel/blob';
import crypto from 'node:crypto';

export const SUB_PREFIX = 'push-subs/';

export function vapidReady() {
  const { VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY } = process.env;
  if (!VAPID_PUBLIC_KEY || !VAPID_PRIVATE_KEY) return false;
  webpush.setVapidDetails(process.env.VAPID_SUBJECT || 'mailto:info@maregastro.com', VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY);
  return true;
}

export function subKey(endpoint) {
  return SUB_PREFIX + crypto.createHash('sha256').update(String(endpoint)).digest('hex').slice(0, 32) + '.json';
}

export function validSub(s) {
  return s && typeof s.endpoint === 'string' && /^https:\/\//.test(s.endpoint) &&
    s.keys && typeof s.keys.p256dh === 'string' && typeof s.keys.auth === 'string';
}

export async function saveSub(sub, label) {
  const rec = { endpoint: sub.endpoint, keys: { p256dh: sub.keys.p256dh, auth: sub.keys.auth },
    label: String(label || '').slice(0, 80), savedAt: new Date().toISOString() };
  await put(subKey(sub.endpoint), JSON.stringify(rec), {
    access: 'public', contentType: 'application/json', addRandomSuffix: false, allowOverwrite: true, cacheControlMaxAge: 0,
  });
}

export async function removeSub(endpoint) {
  const key = subKey(endpoint);
  const page = await list({ prefix: key, limit: 1 });
  if (page.blobs.length) await del(page.blobs[0].url);
}

async function loadSubs() {
  const out = [];
  let cursor;
  do {
    const page = await list({ prefix: SUB_PREFIX, cursor, limit: 1000 });
    for (const b of page.blobs) {
      try {
        const r = await fetch(b.url + '?t=' + Date.now(), { cache: 'no-store' });
        if (r.ok) out.push({ url: b.url, sub: await r.json() });
      } catch { /* bozuk kaydi atla */ }
    }
    cursor = page.cursor;
  } while (cursor);
  return out;
}

async function sendOne(entry, payload) {
  try {
    await webpush.sendNotification(entry.sub, JSON.stringify(payload), { TTL: 6 * 3600, urgency: 'high' });
    return true;
  } catch (e) {
    if (e && (e.statusCode === 404 || e.statusCode === 410)) {
      try { await del(entry.url); } catch { /* sonra tekrar denenir */ }
    }
    return false;
  }
}

// Tum abone cihazlara gonderir. Hata akisi asla bozmaz.
export async function pushAll(payload) {
  try {
    if (!vapidReady()) return { sent: 0, total: 0 };
    const subs = await loadSubs();
    const results = await Promise.all(subs.map(s => sendOne(s, payload)));
    return { sent: results.filter(Boolean).length, total: subs.length };
  } catch { return { sent: 0, total: 0 }; }
}

// Tek cihaza (panelden "Deneme bildirimi").
export async function pushOne(sub, payload) {
  if (!vapidReady()) throw new Error('VAPID anahtarlari tanimli degil');
  await webpush.sendNotification(sub, JSON.stringify(payload), { TTL: 600, urgency: 'high' });
}
