// Mare Gastro - QR menu page, server-rendered for search engines and AI crawlers.
// /qr/ (tr) and /qr/en/ (en) are rewritten here. The app template (qr/app.html) gets:
//   - per-language title, description, canonical, hreflang, Open Graph
//   - Restaurant + Menu (sections, items, TRY offers) + BreadcrumbList JSON-LD
//   - the whole menu as plain semantic HTML inside <main> (crawlers that don't run JS see it)
//   - the menu + QR settings inlined, so the app paints instantly without an extra fetch
// Edge-cached for 2 minutes; the client still refreshes from /api in the background.
import fs from 'node:fs';
import path from 'node:path';
import { list } from '@vercel/blob';

const SITE = 'https://maregastro.com';
const URLS = { tr: SITE + '/qr/', en: SITE + '/qr/en/' };
let TEMPLATE = null;

const COPY = {
  tr: {
    title: 'Mare Gastro Menü ve Fiyatlar | Sapanca Restoran',
    desc: 'Mare Gastro güncel menüsü ve fiyatları: Ege ve Akdeniz mutfağı, deniz ürünleri, ana yemekler, tatlılar, şarap, rakı ve kokteyller. Sapanca, Didi Otel bahçesi.',
    h1: 'Menü', h1sr: 'Mare Gastro Sapanca menü ve fiyatlar', home: 'Ana Sayfa', homeUrl: SITE + '/tr/',
    menuName: 'Mare Gastro Menü', ogLocale: 'tr_TR',
  },
  en: {
    title: 'Mare Gastro Menu & Prices | Restaurant in Sapanca',
    desc: 'Mare Gastro menu with current prices: Aegean and Mediterranean cuisine, seafood, mains, desserts, wine, rakı and cocktails. Sapanca, in the garden of Didi Hotel.',
    h1: 'Menu', h1sr: 'Mare Gastro Sapanca menu and prices', home: 'Home', homeUrl: SITE + '/en/',
    menuName: 'Mare Gastro Menu', ogLocale: 'en_GB',
  },
};
const CAT_EN = { yemek: 'Food', icecek: 'Drinks', b: 'Starters', s: 'Salads', a: 'Small Plates', n: 'Main Courses', kahvalti: 'Breakfast', t: 'Desserts', c: 'Kids', extra: 'Extras', sarap: 'Wines', 'kokteyl-al': 'Cocktails', 'kokteyl-sz': 'Non-Alcoholic Cocktails', raki: 'Rakı', viski: 'Whisky', votka: 'Vodka', cin: 'Gin', tekila: 'Tequila', rom: 'Rum', likor: 'Liqueurs', bira: 'Beer', 'soguk-kahve': 'Iced Coffee', 'soguk-icecek': 'Cold Drinks', milkshake: 'Milkshakes', frozen: 'Frozen', sampanya: 'Champagne', atistirmalik: 'Snacks', havuz: 'Pool Menu', 'sicak-icecek': 'Hot Drinks' };
const GROUP_TR = { yemek: 'Yemekler', icecek: 'İçecekler' };

const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const tidy = (s) => String(s || '').replace(/\s*,\s*/g, ', ').replace(/\s{2,}/g, ' ').replace(/[\s,;]+$/, '').trim();
const money = (n) => Number(n).toLocaleString('tr-TR') + ' ₺';
const inlineJson = (o) => JSON.stringify(o).replace(/</g, '\\u003c').replace(/\u2028/g, '\\u2028').replace(/\u2029/g, '\\u2029');

async function blobJson(p) {
  const res = await list({ prefix: p, limit: 1 });
  const hit = res.blobs.find((x) => x.pathname === p);
  if (!hit) return null;
  const r = await fetch(hit.url + '?_cb=' + Date.now(), { cache: 'no-store' });
  return r.ok ? r.json() : null;
}
function template() {
  if (!TEMPLATE) TEMPLATE = fs.readFileSync(path.join(process.cwd(), 'qr', 'app.html'), 'utf8');
  return TEMPLATE;
}
const nm = (it, lang) => (lang === 'en' && it.name_en) || it.name;
const ds = (it, lang) => tidy((lang === 'en' && it.desc_en) || it.desc);
const catName = (c, lang) => (lang === 'en' ? CAT_EN[c.id] : c.name_tr) || c.name_tr || c.id;

function schema(menu, lang) {
  const C = COPY[lang];
  const sections = menu.categories.map((c) => {
    const items = menu.items.filter((it) => it.cat === c.id);
    if (!items.length) return null;
    return {
      '@type': 'MenuSection',
      name: catName(c, lang),
      hasMenuItem: items.map((it) => {
        const mi = { '@type': 'MenuItem', name: nm(it, lang) };
        const d = ds(it, lang);
        if (d) mi.description = d;
        if (it.img) mi.image = SITE + '/images/' + it.img;
        if (it.price != null) mi.offers = { '@type': 'Offer', price: String(it.price), priceCurrency: 'TRY' };
        return mi;
      }),
    };
  }).filter(Boolean);
  return [
    {
      '@context': 'https://schema.org',
      '@type': 'Restaurant',
      '@id': SITE + '/#restaurant',
      name: 'Mare Gastro',
      url: lang === 'en' ? SITE + '/en/' : SITE + '/tr/',
      image: SITE + '/images/og-image.jpg',
      servesCuisine: lang === 'en' ? ['Aegean', 'Mediterranean', 'Seafood', 'Fine Dining'] : ['Ege', 'Akdeniz', 'Deniz Ürünleri', 'Fine Dining'],
      priceRange: '$$$',
      telephone: '+905323540888',
      email: 'info@maregastro.com',
      address: { '@type': 'PostalAddress', streetAddress: 'Kırkpınar Soğuksu, İstasyon 3 Cad. No:55', addressLocality: 'Sapanca', addressRegion: 'Sakarya', postalCode: '54600', addressCountry: 'TR' },
      geo: { '@type': 'GeoCoordinates', latitude: 40.7002438, longitude: 30.222254 },
      openingHoursSpecification: [{ '@type': 'OpeningHoursSpecification', dayOfWeek: ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], opens: '09:00', closes: '00:00' }],
      acceptsReservations: true,
      currenciesAccepted: 'TRY',
      hasMap: 'https://maps.google.com/?cid=7177941338358519695',
      sameAs: ['https://www.instagram.com/maregastro/', 'https://www.tiktok.com/@maregastro', 'https://www.youtube.com/@maregastro'],
      hasMenu: { '@id': URLS[lang] + '#menu' },
    },
    {
      '@context': 'https://schema.org',
      '@type': 'Menu',
      '@id': URLS[lang] + '#menu',
      name: C.menuName,
      url: URLS[lang],
      inLanguage: lang,
      ...(menu.updatedAt ? { dateModified: menu.updatedAt } : {}),
      hasMenuSection: sections,
    },
    {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: C.home, item: C.homeUrl },
        { '@type': 'ListItem', position: 2, name: C.h1, item: URLS[lang] },
      ],
    },
  ];
}

// Plain, semantic copy of the menu. The app replaces it with the same content on load.
function menuHtml(menu, lang) {
  const C = COPY[lang];
  let h = '<section class="sec" id="s-menu-ssr"><div class="sh"><div><div class="eb">Mare Gastro</div><h1 class="st">' + esc(C.h1) + '<span class="sr"> · ' + esc(C.h1sr) + '</span></h1></div></div>';
  menu.groups.forEach((g) => {
    h += '<h2 class="sr">' + esc(lang === 'en' ? CAT_EN[g.id] : GROUP_TR[g.id] || g.id) + '</h2>';
    menu.categories.filter((c) => c.group === g.id).forEach((c) => {
      const items = menu.items.filter((it) => it.cat === c.id);
      if (!items.length) return;
      h += '<div class="cat"><h3>' + esc(catName(c, lang)) + '</h3><ul class="list" style="list-style:none">';
      items.forEach((it) => {
        const d = ds(it, lang);
        h += '<li class="it compact' + (d ? ' has-desc' : '') + '"><div class="t"><h4>' + esc(nm(it, lang)) + '</h4>' + (d ? '<p>' + esc(d) + '</p>' : '') + '</div><span class="lead"></span><span class="rt"><span class="price">' + (it.price != null ? money(it.price) : '') + '</span></span></li>';
      });
      h += '</ul></div>';
    });
  });
  return h + '</section>';
}

function head(lang, menu) {
  const C = COPY[lang];
  const ld = schema(menu, lang).map((o) => '<script type="application/ld+json">' + inlineJson(o) + '</script>').join('\n');
  return [
    '<title>' + esc(C.title) + '</title>',
    '<meta name="description" content="' + esc(C.desc) + '">',
    '<meta name="robots" content="index, follow, max-image-preview:large">',
    '<link rel="canonical" href="' + URLS[lang] + '">',
    '<link rel="alternate" hreflang="tr" href="' + URLS.tr + '">',
    '<link rel="alternate" hreflang="en" href="' + URLS.en + '">',
    '<link rel="alternate" hreflang="x-default" href="' + URLS.tr + '">',
    '<meta property="og:type" content="website">',
    '<meta property="og:site_name" content="Mare Gastro">',
    '<meta property="og:title" content="' + esc(C.title) + '">',
    '<meta property="og:description" content="' + esc(C.desc) + '">',
    '<meta property="og:url" content="' + URLS[lang] + '">',
    '<meta property="og:image" content="' + SITE + '/images/og-image.jpg">',
    '<meta property="og:locale" content="' + C.ogLocale + '">',
    '<meta name="twitter:card" content="summary_large_image">',
    ld,
  ].join('\n');
}

export default async function handler(req, res) {
  const lang = req.query.lang === 'en' ? 'en' : 'tr';
  let html = template();
  try {
    const [menu, cfg] = await Promise.all([blobJson('menu/menu-data.json'), blobJson('menu/qr-config.json').catch(() => null)]);
    if (menu && Array.isArray(menu.items)) {
      html = html
        .replace('<html lang="tr">', '<html lang="' + lang + '">')
        .replace(/<title>[\s\S]*?<\/title>\s*/, '')
        .replace(/<meta name="description"[^>]*>\s*/, '')
        .replace(/<meta name="robots"[^>]*>\s*/, '')
        .replace('</head>', head(lang, menu) + '\n<script id="qrData" type="application/json">' + inlineJson({ lang, menu, cfg: cfg || { showcases: [], discounts: {} } }) + '</script>\n</head>')
        .replace(/<main id="main">[\s\S]*?<\/main>/, '<main id="main">' + menuHtml(menu, lang) + '</main>');
    }
  } catch (e) {
    // Template alone still works: the app fetches the menu itself.
  }
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'public, max-age=0, must-revalidate');
  res.setHeader('CDN-Cache-Control', 'public, s-maxage=120, stale-while-revalidate=600');
  res.setHeader('Content-Language', lang);
  res.status(200).end(html);
}
