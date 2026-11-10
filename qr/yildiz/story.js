/* Mare Gastro · Yıldız Menüsü - shareable story image (1080×1920, never shows prices).
   Five layouts × eight palettes × three display faces × mirror × ornament × quote = 1,920 designs,
   picked deterministically from the guest's own reading, so ten people at one table almost never
   get the same card (≈2% chance of any repeat), and the content (name, sky, dishes) always differs. */
(function (root) {
  'use strict';
  const W = 1080, H = 1920;
  const SITE_URL = 'maregastro.com/qr/yildiz';
  const LIGHT = [
    { id: 'ivory', bg: '#F4EFE6', ink: '#1E2A2F', soft: 'rgba(30,42,47,.6)', acc: '#9C7437' },
    { id: 'stone', bg: '#ECEAE6', ink: '#2B2D2A', soft: 'rgba(43,45,42,.6)', acc: '#7C6A4F' },
    { id: 'sage', bg: '#E5E9DF', ink: '#24302A', soft: 'rgba(36,48,42,.6)', acc: '#62754F' },
    { id: 'blush', bg: '#F2E6E0', ink: '#3A2626', soft: 'rgba(58,38,38,.6)', acc: '#A0635A' },
    { id: 'mist', bg: '#E6EBEE', ink: '#1C2A36', soft: 'rgba(28,42,54,.6)', acc: '#4F6B7C' },
    { id: 'sand', bg: '#EFE3CF', ink: '#2E2418', soft: 'rgba(46,36,24,.62)', acc: '#9A6A33' },
    { id: 'paper', bg: '#FBF8F2', ink: '#10202E', soft: 'rgba(16,32,46,.58)', acc: '#9C7437' },
    { id: 'clay', bg: '#EAD9CA', ink: '#352A22', soft: 'rgba(53,42,34,.6)', acc: '#8E5B3B' },
  ];
  const DARK = [
    { id: 'forest', bg: '#1F3D33', ink: '#F1E8D6', soft: 'rgba(241,232,214,.66)', acc: '#D2B27A' },
    { id: 'navy', bg: '#15243A', ink: '#EFE8DA', soft: 'rgba(239,232,218,.64)', acc: '#C9A46A' },
    { id: 'burgundy', bg: '#4A1C24', ink: '#F3E6DA', soft: 'rgba(243,230,218,.64)', acc: '#D8B07C' },
    { id: 'espresso', bg: '#33241B', ink: '#F1E6D6', soft: 'rgba(241,230,214,.64)', acc: '#CFA36A' },
    { id: 'ink', bg: '#10202E', ink: '#F4EEE3', soft: 'rgba(244,238,227,.62)', acc: '#C9A46A' },
    { id: 'olive', bg: '#36361F', ink: '#F1EBD8', soft: 'rgba(241,235,216,.64)', acc: '#D6BC7E' },
    { id: 'teal', bg: '#16393D', ink: '#ECE6D8', soft: 'rgba(236,230,216,.64)', acc: '#CDAE76' },
    { id: 'plum', bg: '#38213A', ink: '#F2E7E4', soft: 'rgba(242,231,228,.64)', acc: '#D3AE82' },
  ];
  const FONTS = [
    { fam: 'Cormorant Garamond', w: 500, k: 1.12 },
    { fam: 'Playfair Display', w: 400, k: 1 },
    { fam: 'Fraunces', w: 300, k: 1.02 },
  ];
  const LAYOUTS = ['split', 'path', 'folio', 'poster', 'arch'];
  const DARK_LAYOUT = { path: 1, folio: 1 };

  function hash(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function rng(seed) { let a = seed >>> 0; return function () { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  function design(r) {
    const key = r.reading.map((p) => p.name + '|' + p.sign + '|' + (p.birth ? p.birth.d + '.' + p.birth.m : '') + '|' + (p.gender || '')).join('#') + '#' + (r.variant | 0) + '#' + r.code;
    const h = hash(key), h2 = hash(key + '·');
    const li = h % 5, layout = LAYOUTS[li], pi = (h >>> 3) % 8, fi = (h >>> 6) % 3, flip = (h >>> 9) & 1, orn = (h >>> 10) & 1, q = h2 % 4;
    return { layout, pal: (DARK_LAYOUT[layout] ? DARK : LIGHT)[pi], font: FONTS[fi], flip, orn, q, seed: h2, id: [li, pi, fi, flip, orn, q].join('') };
  }

  // ───── helpers ─────
  const DF = (D, sz, it) => (it ? 'italic ' : '') + D.font.w + ' ' + Math.round(sz * D.font.k) + 'px "' + D.font.fam + '", Georgia, serif';
  const BF = (w, sz) => w + ' ' + Math.round(sz) + 'px Inter, -apple-system, "Helvetica Neue", Arial, sans-serif';
  function fit(x, text, fn, maxW, start, min) { let s = start; x.font = fn(s); while (x.measureText(text).width > maxW && s > min) { s -= 2; x.font = fn(s); } return s; }
  function ell(x, t, maxW) { if (x.measureText(t).width <= maxW) return t; while (t.length > 1 && x.measureText(t + '…').width > maxW) t = t.slice(0, -1); return t.replace(/[\s,·]+$/, '') + '…'; }
  function wrap(x, text, maxW) { const words = String(text).split(' '), out = []; let cur = ''; words.forEach((w) => { const t = cur ? cur + ' ' + w : w; if (x.measureText(t).width > maxW && cur) { out.push(cur); cur = w; } else cur = t; }); if (cur) out.push(cur); return out; }
  function clamp(x, text, w, max) { const ls = wrap(x, text, w); if (ls.length <= max) return ls; const out = ls.slice(0, max); out[max - 1] = ell(x, out[max - 1] + ' ' + ls[max], w); return out; }
  function spaced(x, t, X, Y, sp) { if ('letterSpacing' in x) { x.letterSpacing = sp + 'px'; x.fillText(t, X, Y); x.letterSpacing = '0px'; } else x.fillText(t, X, Y); }
  function cover(x, im, X, Y, w, h, z) { const s = Math.max(w / im.width, h / im.height) * (z || 1.04); const dw = im.width * s, dh = im.height * s; x.drawImage(im, X + (w - dw) / 2, Y + (h - dh) / 2, dw, dh); }
  function rrect(x, X, Y, w, h, R) { x.beginPath(); x.moveTo(X + R, Y); x.arcTo(X + w, Y, X + w, Y + h, R); x.arcTo(X + w, Y + h, X, Y + h, R); x.arcTo(X, Y + h, X, Y, R); x.arcTo(X, Y, X + w, Y, R); x.closePath(); }
  function grain(x, R, n, col) { x.fillStyle = col; for (let i = 0; i < n; i++) { const s = R() * 2 + .6; x.fillRect(R() * W, R() * H, s, s); } }
  const loadImg = (src) => new Promise((res) => { const im = new Image(); im.onload = () => res(im); im.onerror = () => res(null); im.src = src; });
  const LOGOS = {};
  function logo(col) {
    if (LOGOS[col]) return LOGOS[col];
    const sym = document.getElementById('logo');
    const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 692 440" width="692" height="440">' + sym.innerHTML.replace(/currentColor/g, col) + '</svg>';
    return (LOGOS[col] = loadImg('data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg)));
  }
  function stars(x, id, cx, cy, size, line, dot, halo, lw) {
    const [pts, edges] = root.YildizEngine.STARS[id];
    const P = pts.map(([px, py]) => [cx + (px / 100 - .5) * size, cy + (py / 100 - .5) * size]);
    x.strokeStyle = line; x.lineWidth = lw || Math.max(1.6, size / 90); x.lineCap = 'round';
    edges.forEach(([a, b]) => { x.beginPath(); x.moveTo(P[a][0], P[a][1]); x.lineTo(P[b][0], P[b][1]); x.stroke(); });
    const r = Math.max(3.2, size / 46);
    P.forEach(([px, py]) => { if (halo) { x.fillStyle = halo; x.beginPath(); x.arc(px, py, r * 2.1, 0, 7); x.fill(); } x.fillStyle = dot; x.beginPath(); x.arc(px, py, r, 0, 7); x.fill(); });
  }
  function signs(x, d, cx, cy, size, line, dot, halo) {
    if (d.couple) { stars(x, d.signs[0], cx - size * .36, cy, size * .64, line, dot, halo); stars(x, d.signs[1], cx + size * .36, cy, size * .64, line, dot, halo); }
    else stars(x, d.signs[0], cx, cy, size, line, dot, halo);
  }
  function qr(x, X, Y, s) {
    try {
      const q = root.qrcode(0, 'M'); q.addData('https://' + SITE_URL + '/?utm_source=story&utm_medium=social&utm_campaign=yildiz_menusu'); q.make();
      const n = q.getModuleCount(), m = s / n;
      x.fillStyle = '#FFFFFF'; rrect(x, X - 12, Y - 12, s + 24, s + 24, 10); x.fill();
      x.fillStyle = '#10202E'; for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (q.isDark(r, c)) x.fillRect(X + c * m, Y + r * m, Math.ceil(m), Math.ceil(m));
    } catch (e) {}
  }
  // QR + invitation. align: 'left' (X = left edge) or 'center' (X = centre)
  function footer(x, D, X, Y, ink, acc, align) {
    const qs = 118, gap = 30;
    x.font = BF(500, 29);
    const tw = Math.max(x.measureText('Sen de yıldızına göre').width, x.measureText(SITE_URL).width * .78);
    const total = qs + gap + tw, X0 = align === 'center' ? X - total / 2 : X;
    qr(x, X0, Y, qs);
    x.textAlign = 'left'; x.fillStyle = ink; x.font = BF(500, 29);
    x.fillText('Sen de yıldızına göre', X0 + qs + gap, Y + 38);
    x.fillText('menünü keşfet', X0 + qs + gap, Y + 76);
    x.fillStyle = acc; x.font = BF(600, 21); x.fillText(SITE_URL, X0 + qs + gap, Y + 112);
  }
  // Course list: label (display italic, accent) + dish names (+ optional note). Shrinks to fit.
  function list(x, D, rows, X, Y, w, hMax, align, ink, acc, soft) {
    const plan = (sz, notes) => {
      x.font = BF(500, sz);
      const lh = Math.round(sz * 1.24), lab = Math.round(sz * 1.18), nh = Math.round(sz * .9), gap = Math.round(sz * .95);
      let tot = 0;
      const out = rows.map((r) => { x.font = BF(500, sz); const ls = wrap(x, r.names.join(' · '), w).slice(0, 2); const h = lab + ls.length * lh + (notes && r.note ? nh : 0); tot += h + gap; return { r, ls, h }; });
      return { sz, notes, lh, lab, nh, gap, out, tot: tot - gap };
    };
    let p = null;
    for (let sz = 32; sz >= 25 && !p; sz--) { const t = plan(sz, true); if (t.tot <= hMax) p = t; }
    for (let sz = 32; sz >= 18 && !p; sz--) { const t = plan(sz, false); if (t.tot <= hMax || sz === 18) p = t; }
    x.textAlign = align; const ax = align === 'center' ? X + w / 2 : align === 'right' ? X + w : X;
    let y = Y;
    p.out.forEach((o) => {
      x.fillStyle = acc; x.font = DF(D, p.sz * .96, true); x.fillText(o.r.label, ax, y + p.lab * .72);
      let yy = y + p.lab;
      x.fillStyle = ink; x.font = BF(500, p.sz);
      o.ls.forEach((l) => { yy += p.lh * .86; x.fillText(l, ax, yy); yy += p.lh * .14; });
      if (p.notes && o.r.note) { x.fillStyle = soft; x.font = BF(300, p.sz * .66); x.fillText(ell(x, o.r.note, w), ax, yy + p.nh * .8); }
      y += o.h + p.gap;
    });
    return y;
  }

  function data(r, D, h) {
    const couple = r.mode === 'couple', a = r.reading[0], b = r.reading[1];
    const fs = h.firstSentence;
    const qs = couple
      ? [r.match.band, fs(r.pairText), r.match.insights[2].v, 'İki yıldız, tek masa: %' + r.match.score + ' uyum.']
      : [fs(a.insights[0].v), fs(a.palate), a.decan ? a.signName + ' burcunun ' + a.decan + '. dekanı' + (a.co && a.decan > 1 ? ', ' + a.co + ' etkisinde.' : '; saf ' + a.signName + '.') : fs(a.insights[1].v), a.meaning ? 'Adı “' + a.meaning + '”; sayısı ' + a.num + ', ' + a.numTitle.toLocaleLowerCase('tr') + '.' : fs(a.numText)];
    const rows = r.courses.filter((g) => g.key !== 'kapanis').map((g) => ({
      key: g.key, label: g.label, names: g.items.map((i) => (i.qty > 1 && g.key !== 'icki' ? i.qty + ' × ' : '') + i.name),
      note: g.items[0].note || '', img: (g.items.find((i) => i.img) || {}).img || null,
    }));
    let star = null; r.courses.forEach((g) => g.items.forEach((i) => { if (i.star) star = i; }));
    const photos = []; if (star) photos.push(star.img);
    r.courses.forEach((g) => g.items.forEach((i) => { if (i.img && !photos.includes(i.img) && ['ana', 'ara', 'baslangic', 'tatli'].includes(i.course)) photos.push(i.img); }));
    return {
      couple, rows, photos, quote: qs[D.q] || qs[0], signs: r.reading.map((p) => p.sign),
      title: couple ? a.first + ' & ' + b.first : a.first,
      sub: couple ? a.signName + ' & ' + b.signName + ' · %' + r.match.score + ' uyum' : h.titleOf(a) + (a.decan ? ' · ' + a.decan + '. dekan' : '') + ' · ' + a.el + ' · ' + a.ruler,
      short: couple ? a.signName + ' & ' + b.signName : a.signName + ' · ' + a.el,
    };
  }

  // ───── layouts ─────
  // 1 · Split page: paper column + full-height dish photo with stamp edge
  async function split(x, D, d, I, R) {
    const C = D.pal, PW = 610, flip = D.flip, px = flip ? W - PW : 0, fx = flip ? 0 : PW, fw = W - PW;
    x.fillStyle = C.bg; x.fillRect(0, 0, W, H); grain(x, R, 2500, 'rgba(0,0,0,.025)');
    x.save();
    x.beginPath();
    const e = flip ? fw : fx, rr = 13;
    if (D.orn === 0) {
      if (!flip) { x.moveTo(W, 0); x.lineTo(W, H); x.lineTo(e, H); for (let y = H; y > 0; y -= rr * 2) x.arc(e, y - rr, rr, Math.PI / 2, Math.PI * 1.5, false); x.lineTo(e, 0); }
      else { x.moveTo(0, 0); x.lineTo(e, 0); for (let y = 0; y < H; y += rr * 2) x.arc(e, y + rr, rr, -Math.PI / 2, Math.PI / 2, false); x.lineTo(0, H); }
      x.closePath();
    } else x.rect(fx, 0, fw, H);
    x.clip(); x.fillStyle = C.ink; x.fillRect(fx - 20, 0, fw + 40, H);
    if (I[0]) cover(x, I[0], fx - 14, 0, fw + 28, H, 1.0);
    x.restore();
    if (D.orn === 1) { x.fillStyle = C.acc; x.fillRect(flip ? fw : fx - 3, 0, 3, H); }
    const L = px + 86, TW = PW - 150;
    const lg = await logo(C.ink); if (lg) x.drawImage(lg, L, 104, 150, 95);
    x.textAlign = 'left'; x.fillStyle = C.ink;
    fit(x, d.title, (s) => DF(D, s, false), TW - 44, 150, 60); x.fillText(d.title, L, 380);
    x.fillStyle = C.acc; x.font = DF(D, 60, true); x.fillText('Yıldız Menüsü', L, 456);
    x.save(); x.translate(px + PW - 52, 120); x.rotate(Math.PI / 2); x.fillStyle = C.soft; x.font = BF(600, 20); spaced(x, d.sub, 0, 0, 3); x.restore();
    stars(x, d.signs[0], L + 74, 562, 140, C.acc, C.ink, null);
    if (d.couple) stars(x, d.signs[1], L + 250, 562, 140, C.acc, C.ink, null);
    x.fillStyle = C.soft; x.font = DF(D, 30, true);
    const ql = clamp(x, d.quote, TW, 2); ql.forEach((l, i) => x.fillText(l, L, 690 + i * 40));
    list(x, D, d.rows, L, 690 + ql.length * 40 + 40, TW, 1600 - (690 + ql.length * 40 + 40), 'left', C.ink, C.acc, C.soft);
    footer(x, D, L, 1666, C.ink, C.acc, 'left');
  }

  // 2 · Constellation path: dark ground, plated dishes joined by thin gold lines
  async function path(x, D, d, I, R) {
    const C = D.pal;
    x.fillStyle = C.bg; x.fillRect(0, 0, W, H); grain(x, R, 5000, 'rgba(255,255,255,.025)'); grain(x, R, 3000, 'rgba(0,0,0,.05)');
    for (let i = 0; i < 70; i++) { x.fillStyle = 'rgba(255,255,255,' + (.08 + R() * .25).toFixed(2) + ')'; x.beginPath(); x.arc(R() * W, R() * 470, R() * 1.8 + .4, 0, 7); x.fill(); }
    const lg = await logo(C.ink); if (lg) x.drawImage(lg, W / 2 - 72, 96, 144, 92);
    x.textAlign = 'center'; x.fillStyle = C.ink;
    fit(x, d.title, (s) => DF(D, s, false), 880, 120, 60); x.fillText(d.title, W / 2, 330);
    x.fillStyle = C.acc; x.font = DF(D, 46, true); x.fillText('Yıldız Menüsü', W / 2, 398);
    x.fillStyle = C.soft; x.font = BF(500, 23); spaced(x, d.sub, W / 2, 448, 2);
    const nodes = d.rows.slice(0, 6), n = nodes.length, top = 530, bot = 1580, step = (bot - top) / n;
    const Rp = Math.min(104, step * .4);
    const colL = !D.flip, base = colL ? 215 : W - 215, zig = colL ? 70 : -70;
    const pos = nodes.map((nd, i) => ({ nd, x: base + (i % 2 ? zig : 0), y: top + step * (i + .5) }));
    x.strokeStyle = C.acc; x.globalAlpha = .75; x.lineWidth = 2;
    for (let i = 0; i < n - 1; i++) {
      const a = pos[i], b = pos[i + 1];
      x.beginPath(); x.moveTo(a.x, a.y);
      const bend = (colL ? -1 : 1) * (D.orn === 0 ? 150 : 60);
      x.bezierCurveTo(a.x + bend, a.y + step * .45, b.x + bend, b.y - step * .45, b.x, b.y);
      x.stroke();
      const mx = (a.x + b.x) / 2 + bend * .75, my = (a.y + b.y) / 2;
      x.globalAlpha = 1; x.fillStyle = C.acc; x.beginPath(); x.arc(mx, my, 5, 0, 7); x.fill(); x.globalAlpha = .75;
    }
    x.globalAlpha = 1;
    const imgFor = {}; d.rows.forEach((r) => { if (r.img) imgFor[r.img] = I.find((im) => im && im.__src === r.img) || null; });
    pos.forEach((p, i) => {
      const im = p.nd.img ? imgFor[p.nd.img] : null;
      x.fillStyle = 'rgba(255,255,255,.07)'; x.beginPath(); x.arc(p.x, p.y, Rp + 16, 0, 7); x.fill();
      x.strokeStyle = C.acc; x.lineWidth = 1.5; x.globalAlpha = .6; x.beginPath(); x.arc(p.x, p.y, Rp + 16, 0, 7); x.stroke(); x.globalAlpha = 1;
      if (im) { x.save(); x.beginPath(); x.arc(p.x, p.y, Rp, 0, 7); x.clip(); cover(x, im, p.x - Rp, p.y - Rp, Rp * 2, Rp * 2, 1.12); x.restore(); }
      else { x.fillStyle = 'rgba(255,255,255,.05)'; x.beginPath(); x.arc(p.x, p.y, Rp, 0, 7); x.fill(); stars(x, d.signs[i % d.signs.length], p.x, p.y, Rp * 1.25, C.acc, C.ink, null, 1.6); }
      const left = colL, tx = left ? base + zig + Rp + 56 : base + zig - Rp - 56, tw = left ? W - 84 - tx : tx - 84;
      x.textAlign = left ? 'left' : 'right';
      x.fillStyle = C.acc; x.font = BF(600, 20); spaced(x, p.nd.label, tx, p.y - 34, 2);
      x.fillStyle = C.ink; let fs2 = 40; x.font = DF(D, fs2, false);
      let ls = wrap(x, p.nd.names.join(' · '), tw); while (ls.length > 2 && fs2 > 28) { fs2 -= 2; x.font = DF(D, fs2, false); ls = wrap(x, p.nd.names.join(' · '), tw); }
      ls.slice(0, 2).forEach((l, k) => x.fillText(k === 1 && ls.length > 2 ? ell(x, l + '…', tw) : l, tx, p.y + 14 + k * fs2 * 1.12));
      if (p.nd.note && ls.length < 2) { x.fillStyle = C.soft; x.font = BF(300, 21); x.fillText(ell(x, p.nd.note, tw), tx, p.y + 58); }
    });
    footer(x, D, W / 2, 1668, C.ink, C.acc, 'center');
  }

  // 3 · Leather folio: stitched leather cover with an ivory menu card
  async function folio(x, D, d, I, R) {
    const C = D.pal;
    x.fillStyle = C.bg; x.fillRect(0, 0, W, H);
    grain(x, R, 16000, 'rgba(0,0,0,.08)'); grain(x, R, 7000, 'rgba(255,255,255,.035)');
    x.strokeStyle = C.acc; x.globalAlpha = .55; x.lineWidth = 3; x.setLineDash([16, 11]); rrect(x, 44, 44, W - 88, H - 88, 26); x.stroke(); x.setLineDash([]); x.globalAlpha = 1;
    const lg = await logo(C.acc); if (lg) x.drawImage(lg, W / 2 - 80, 92, 160, 102);
    x.textAlign = 'center'; x.fillStyle = C.acc; x.font = DF(D, 38, true); x.fillText('Yıldız Menüsü', W / 2, 254);
    const cx0 = 118, cy0 = 300, cw = W - 236, ch = 1500;
    x.save(); x.shadowColor = 'rgba(0,0,0,.45)'; x.shadowBlur = 50; x.shadowOffsetY = 24; x.fillStyle = '#F6F0E4'; rrect(x, cx0, cy0, cw, ch, 8); x.fill(); x.restore();
    const INK = '#2A211B', ACC = '#8A6430', SOFT = 'rgba(42,33,27,.62)';
    x.strokeStyle = 'rgba(138,100,48,.45)'; x.lineWidth = 1.5; rrect(x, cx0 + 26, cy0 + 26, cw - 52, ch - 52, 4); x.stroke();
    if (D.orn === 1) { x.strokeStyle = 'rgba(138,100,48,.25)'; rrect(x, cx0 + 36, cy0 + 36, cw - 72, ch - 72, 3); x.stroke(); }
    signs(x, d, W / 2, cy0 + 130, 120, 'rgba(138,100,48,.85)', INK, null);
    x.fillStyle = INK; fit(x, d.title, (s) => DF(D, s, false), cw - 140, 100, 56); x.fillText(d.title, W / 2, cy0 + 300);
    x.strokeStyle = ACC; x.lineWidth = 1.5; x.beginPath(); x.moveTo(W / 2 - 150, cy0 + 344); x.lineTo(W / 2 - 14, cy0 + 344); x.moveTo(W / 2 + 14, cy0 + 344); x.lineTo(W / 2 + 150, cy0 + 344); x.stroke();
    x.save(); x.translate(W / 2, cy0 + 344); x.rotate(Math.PI / 4); x.fillStyle = ACC; x.fillRect(-5, -5, 10, 10); x.restore();
    x.fillStyle = SOFT; x.font = BF(500, 22); spaced(x, d.sub, W / 2, cy0 + 396, 2);
    x.fillStyle = INK; x.font = DF(D, 31, true);
    const ql = clamp(x, '“' + d.quote + '”', cw - 180, 2); ql.forEach((l, i) => x.fillText(l, W / 2, cy0 + 462 + i * 42));
    const ly = cy0 + 462 + ql.length * 42 + 40;
    list(x, D, d.rows, cx0 + 90, ly, cw - 180, cy0 + ch - 230 - ly, 'center', INK, ACC, SOFT);
    if (D.orn === 0) {
      const pocket = (X, Y, sx) => { x.fillStyle = C.bg; x.beginPath(); x.moveTo(X, Y); x.lineTo(X + sx * 150, Y); x.lineTo(X, Y - 150); x.closePath(); x.fill(); x.strokeStyle = C.acc; x.globalAlpha = .5; x.setLineDash([9, 7]); x.lineWidth = 2; x.beginPath(); x.moveTo(X + sx * 132, Y - 8); x.lineTo(X + sx * 8, Y - 132); x.stroke(); x.setLineDash([]); x.globalAlpha = 1; };
      pocket(cx0, cy0 + ch, 1); pocket(cx0 + cw, cy0 + ch, -1);
    }
    footer(x, D, W / 2, cy0 + ch - 190, INK, ACC, 'center');
  }

  // 4 · Editorial poster: ring, name, photo strip, centred menu
  async function poster(x, D, d, I, R) {
    const C = D.pal;
    x.fillStyle = C.bg; x.fillRect(0, 0, W, H); grain(x, R, 2500, 'rgba(0,0,0,.025)');
    x.strokeStyle = C.acc; x.globalAlpha = .4; x.lineWidth = 2; x.strokeRect(54, 54, W - 108, H - 108); x.globalAlpha = 1;
    const lg = await logo(C.ink); if (lg) x.drawImage(lg, W / 2 - 75, 118, 150, 95);
    x.textAlign = 'center'; x.fillStyle = C.acc; x.font = DF(D, 40, true); x.fillText('Yıldız Menüsü', W / 2, 280);
    const cy = 470, Rr = 140;
    if (D.orn === 0) {
      x.strokeStyle = C.acc; x.globalAlpha = .5; x.lineWidth = 1.5; x.beginPath(); x.arc(W / 2, cy, Rr, 0, 7); x.stroke();
      for (let i = 0; i < 72; i++) { const a = i / 72 * Math.PI * 2, r2 = i % 6 === 0 ? Rr - 16 : Rr - 8; x.beginPath(); x.moveTo(W / 2 + Math.cos(a) * Rr, cy + Math.sin(a) * Rr); x.lineTo(W / 2 + Math.cos(a) * r2, cy + Math.sin(a) * r2); x.stroke(); }
      x.globalAlpha = 1;
    }
    signs(x, d, W / 2, cy, D.orn === 0 ? 190 : 250, C.acc, C.ink, 'rgba(156,116,55,.16)');
    x.fillStyle = C.ink; fit(x, d.title, (s) => DF(D, s, false), 880, 108, 56); x.fillText(d.title, W / 2, 735);
    x.fillStyle = C.soft; x.font = BF(500, 24); spaced(x, d.sub, W / 2, 790, 2);
    x.fillStyle = C.ink; x.font = DF(D, 32, true);
    const ql = clamp(x, '“' + d.quote + '”', 820, 2); ql.forEach((l, i) => x.fillText(l, W / 2, 856 + i * 44));
    let y = 856 + ql.length * 44 + 22;
    const ph = I.slice(0, 3).filter(Boolean);
    if (ph.length) {
      const n = ph.length, g = 18, w = n === 1 ? 340 : (840 - g * (n - 1)) / n, h = Math.min(250, w * 1.05), X0 = (W - (w * n + g * (n - 1))) / 2;
      ph.forEach((im, i) => { const X = X0 + i * (w + g); x.save(); rrect(x, X, y, w, h, n === 3 ? 22 : 28); x.clip(); cover(x, im, X, y, w, h, 1.08); x.restore(); });
      y += h + 56;
    } else y += 30;
    list(x, D, d.rows, 120, y, 840, 1592 - y, 'center', C.ink, C.acc, C.soft);
    footer(x, D, W / 2, 1660, C.ink, C.acc, 'center');
  }

  // 5 · Arch window: the star dish framed in an arch (or circle), menu below
  async function arch(x, D, d, I, R) {
    const C = D.pal;
    x.fillStyle = C.bg; x.fillRect(0, 0, W, H); grain(x, R, 2500, 'rgba(0,0,0,.025)');
    const lg = await logo(C.ink); if (lg) x.drawImage(lg, W / 2 - 66, 84, 132, 84);
    const ax = 220, aw = 640, ay = 210, ah = 600;
    const shape = (o) => { x.beginPath(); if (D.orn === 0) { x.moveTo(ax - o, ay + ah + o); x.lineTo(ax - o, ay + aw / 2); x.arc(W / 2, ay + aw / 2, aw / 2 + o, Math.PI, 0, false); x.lineTo(ax + aw + o, ay + ah + o); x.closePath(); } else { x.arc(W / 2, ay + aw / 2, aw / 2 + o, 0, 7); } };
    x.strokeStyle = C.acc; x.globalAlpha = .55; x.lineWidth = 2; shape(18); x.stroke(); x.globalAlpha = 1;
    x.save(); shape(0); x.clip(); x.fillStyle = C.soft; x.fillRect(ax, ay, aw, ah);
    if (I[0]) cover(x, I[0], ax, ay, aw, D.orn === 0 ? ah : aw, 1.04);
    x.restore();
    const bottom = D.orn === 0 ? ay + ah : ay + aw;
    x.fillStyle = C.bg; x.beginPath(); x.arc(W / 2, bottom + 4, 74, 0, 7); x.fill();
    signs(x, d, W / 2, bottom + 4, 104, C.acc, C.ink, null);
    x.textAlign = 'center'; x.fillStyle = C.ink;
    const ty = bottom + 170; fit(x, d.title, (s) => DF(D, s, false), 880, 112, 56); x.fillText(d.title, W / 2, ty);
    x.fillStyle = C.acc; x.font = DF(D, 36, true); x.fillText('Yıldız Menüsü', W / 2, ty + 56);
    x.fillStyle = C.soft; x.font = BF(500, 22); spaced(x, d.sub, W / 2, ty + 100, 2);
    list(x, D, d.rows, 110, ty + 150, 860, 1600 - (ty + 150), 'center', C.ink, C.acc, C.soft);
    footer(x, D, W / 2, 1664, C.ink, C.acc, 'center');
  }

  const RENDER = { split, path, folio, poster, arch };
  async function render(r, helpers) {
    const D = design(r);
    if (helpers.force) { Object.assign(D, helpers.force); if (helpers.force.layout && helpers.force.pi != null) D.pal = (DARK_LAYOUT[D.layout] ? DARK : LIGHT)[helpers.force.pi]; }
    const d = data(r, D, helpers);
    try {
      await Promise.all([
        document.fonts.load(DF(D, 80, false)), document.fonts.load(DF(D, 80, true)),
        document.fonts.load(BF(500, 30)), document.fonts.load(BF(600, 20)), document.fonts.load(BF(300, 20)),
      ]);
    } catch (e) {}
    const srcs = D.layout === 'path' ? d.rows.map((x) => x.img).filter(Boolean) : d.photos.slice(0, 3);
    const I = await Promise.all(srcs.map((s) => loadImg('/images/' + encodeURI(s)).then((im) => { if (im) im.__src = s; return im; })));
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const x = c.getContext('2d');
    x.textBaseline = 'alphabetic';
    await RENDER[D.layout](x, D, d, I, rng(D.seed));
    return new Promise((res) => c.toBlob((b) => res(b), 'image/png'));
  }
  root.YildizStory = { render, design, LAYOUTS, count: LAYOUTS.length * 8 * FONTS.length * 2 * 2 * 4 };
})(window);
