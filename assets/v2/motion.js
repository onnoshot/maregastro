/* Mare Gastro v2 — motion layer (GSAP + ScrollTrigger + SplitText + Lenis).
   Never replaces existing logic; only wraps goTo/openMob/closeMob for smooth scroll. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  var RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var DESKTOP = window.matchMedia('(min-width: 900px)');
  var RTL = root.getAttribute('dir') === 'rtl' || d.body.getAttribute('dir') === 'rtl';
  var hasG = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };

  root.classList.add('v2-ready');

  /* ── Loader ── */
  var loader = $('#v2Loader');
  function hideLoader() { if (loader) loader.classList.add('done'); }
  if (root.classList.contains('v2-seen') || RM) hideLoader();
  // motion.js is deferred, so the DOM is ready here; don't wait for video/images (hurt LCP)
  else { setTimeout(hideLoader, 350); setTimeout(hideLoader, 900); }

  /* ── Smooth scroll (Lenis) ── */
  var lenis = null;
  if (!RM && typeof window.Lenis !== 'undefined') {
    lenis = new window.Lenis({ lerp: 0.1, wheelMultiplier: 1, smoothWheel: true, syncTouch: false,
      prevent: function (node) { return !!(node.closest && node.closest('.time-list,.ev-pop-list,.mob-menu,.langsw-menu,.mc-detail-ig,iframe,.v2-lb')); } });
    if (hasG) {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(0);
    }
  }
  function navOffset() { return -(($('nav') || {}).offsetHeight || 60) - 18; }
  window.goTo = function (id) {
    var el = typeof id === 'string' ? d.querySelector(id) : id;
    if (!el) return;
    var off = el.id === 'home' ? 0 : navOffset();
    if (lenis) lenis.scrollTo(el, { offset: off, duration: 1.4 });
    else window.scrollTo({ top: el.getBoundingClientRect().top + window.pageYOffset + off, behavior: RM ? 'auto' : 'smooth' });
  };
  ['openMob', 'closeMob'].forEach(function (fn) {
    var orig = window[fn];
    if (typeof orig !== 'function') return;
    window[fn] = function () { orig.apply(this, arguments); if (lenis) { fn === 'openMob' ? lenis.stop() : lenis.start(); } };
  });

  /* ── Scroll-linked chrome: progress, nav state, mobile bar, top button ── */
  var prog = $('#v2Progress'), nav = $('nav'), bar = $('#v2Bar'), topBtn = $('#v2Top');
  var hero = $('#home'), rez = $('#reservation');
  function onScroll() {
    var y = window.pageYOffset || root.scrollTop;
    var max = root.scrollHeight - window.innerHeight;
    if (prog) prog.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
    var heroH = hero ? hero.offsetHeight : 600;
    if (bar) {
      var r = rez ? rez.getBoundingClientRect() : null;
      var inRez = r && r.top < window.innerHeight * .75 && r.bottom > window.innerHeight * .25;
      bar.classList.toggle('show', y > heroH * .6 && !inRez);
    }
    if (topBtn) topBtn.classList.toggle('show', y > window.innerHeight * 1.5);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (topBtn) topBtn.addEventListener('click', function () { window.goTo('#home'); });

  /* ── Generic reveals (.v2-rv) ── */
  var rvObs = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); rvObs.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  $$('.v2-rv').forEach(function (el, i) {
    var sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
    el.style.transitionDelay = Math.min(sib, 6) * 0.08 + 's';
    rvObs.observe(el);
  });

  /* ── Visitor journey tracking (distinct event names → readable in GA4 without custom dimensions) ── */
  var T = function (n, p) { try { if (typeof trackEvent === 'function') trackEvent(n, p || {}); } catch (e) {} };
  var SECTION_EVENTS = { story: 'view_story', chef: 'view_chef', signature: 'view_signature', menu: 'view_menu',
    reviews: 'view_reviews', occasions: 'view_occasions', reservation: 'view_reservation', contact: 'view_contact' };
  var seenSec = {};
  var secObs = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      var id = e.target.id; if (seenSec[id] || !e.isIntersecting) return;
      var need = Math.min(e.boundingClientRect.height * 0.35, window.innerHeight * 0.4);
      if (e.intersectionRect.height >= need) { seenSec[id] = 1; T(SECTION_EVENTS[id]); secObs.unobserve(e.target); }
    });
  }, { threshold: [0, 0.1, 0.2, 0.35, 0.5, 0.75, 1] });
  Object.keys(SECTION_EVENTS).forEach(function (id) { var el = d.getElementById(id); if (el) secObs.observe(el); });

  // visible time on page (tab in foreground)
  var visMs = 0, visT0 = d.visibilityState === 'visible' ? Date.now() : 0, timeMarks = [30, 90, 180, 300], timeSent = {};
  d.addEventListener('visibilitychange', function () {
    if (d.visibilityState === 'visible') visT0 = Date.now(); else if (visT0) { visMs += Date.now() - visT0; visT0 = 0; }
  });
  setInterval(function () {
    var sec = (visMs + (visT0 ? Date.now() - visT0 : 0)) / 1000;
    timeMarks.forEach(function (m) { if (sec >= m && !timeSent[m]) { timeSent[m] = 1; T('engaged_' + m + 's'); } });
  }, 5000);

  // clicks — only where the markup has no inline trackEvent already
  var onceSent = {};
  function once(n, p) { if (onceSent[n]) return; onceSent[n] = 1; T(n, p); }
  d.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target : null; if (!t) return;
    var el = t.closest('a,button,.kopt,.mc-daynum');
    if (!el) return;
    var inline = (el.getAttribute('onclick') || '').indexOf('trackEvent') > -1;
    var href = el.getAttribute('href') || '';
    if (el.matches('.mtab')) return T('menu_category_click', { event_label: el.getAttribute('data-c') || '' });
    if (el.matches('.mgroup-btn')) return T('menu_group_click', { event_label: el.getAttribute('data-g') || '' });
    if (el.matches('.m-dergi-btn')) return T('digital_menu_open');
    if (el.matches('.occ-card')) { var h = el.querySelector('h3'); return T('occasion_click', { event_label: h ? h.textContent : href }); }
    if (el.closest('#reviews') && el.matches('.v2-btn-line')) return T('reviews_more_click');
    if (el.closest('#signature') && el.matches('.v2-btn-line')) return T('signature_all_menu_click');
    if (el.matches('.ev-info-btn')) return T('events_info_open');
    if (el.matches('.mc-daynum')) return T('rez_date_select');
    if (el.closest('.time-list') && el.matches('.tpill')) return T('rez_time_select', { event_label: el.textContent.trim() });
    if (el.matches('.gcnt-btn')) return once('rez_guests_change');
    if (el.matches('.kopt')) return T('rez_stay_select', { event_label: (el.querySelector('h4') || el).textContent.replace(/\s+/g, ' ').trim() });
    if (inline) return;
    if (el.closest('.langsw-menu,.mob-langs')) return T('language_switch', { event_label: href });
    if (/instagram\.com/.test(href)) return T('instagram_click', { event_label: href });
    if (/^mailto:/.test(href)) return T('email_click');
    if (/tripadvisor\./.test(href)) return T('tripadvisor_click');
    if (/sapancadidiotel\.com/.test(href)) return T('didi_hotel_click');
    if (/^tel:/.test(href)) return T('phone_click', { event_label: 'page' });
    if (/(^|\/)blog\//.test(href)) return T('blog_click', { event_label: href });
  }, true);

  /* ── Counters ── */
  function runCount(el) {
    var to = parseFloat(el.getAttribute('data-count')), dec = +el.getAttribute('data-dec') || 0;
    var fin = el.getAttribute('data-final'), from = to >= 1900 ? to - 23 : 0, t0 = null, dur = 1600;
    var sep = (root.lang === 'tr' || root.lang === 'ru') ? ',' : '.';
    if (RM) { el.textContent = fin; return; }
    (function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur), e = 1 - Math.pow(1 - p, 4);
      var v = from + (to - from) * e;
      el.textContent = p < 1 ? (dec ? v.toFixed(dec).replace('.', sep) : Math.round(v)) : fin;
      if (p < 1) requestAnimationFrame(step);
    })(performance.now());
  }
  var cObs = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { runCount(e.target); cObs.unobserve(e.target); } });
  }, { threshold: 0.6 });
  $$('.st-n[data-count]').forEach(function (el) { cObs.observe(el); });

  /* ── Lightbox (ambiance) ── */
  var lb = $('#v2Lb');
  function closeLb() { if (!lb) return; lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true'); if (lenis) lenis.start(); }
  $$('.amb-fig').forEach(function (b) {
    b.addEventListener('click', function () {
      if (!lb) return;
      var img = $('img', lb), src = $('img', b);
      img.src = b.getAttribute('data-full'); img.alt = src ? src.alt : '';
      lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false'); if (lenis) lenis.stop();
      if (typeof trackEvent === 'function') trackEvent('gallery_open', { event_label: img.alt });
    });
  });
  if (lb) { lb.addEventListener('click', function (e) { if (e.target === lb || e.target.closest('.v2-lb-x')) closeLb(); }); }
  d.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLb(); });

  /* ── Signature dishes (built from the live menu the page already fetched) ── */
  var FEATURED_CATS = ['b', 'a', 'n', 't', 's', 'kahvalti'];
  var CHEF_PICKS = [
    'kereviz-pureli-jumbo-karides-sogus', 'dana-carpaccio', 'roka-salatasi',
    'mare-spesiyal-ahtapot-guvec', 'biber-kremali-bonfile', 'citir-somon', 'ormanda-bir-yuruyus'
  ];
  function menuData() { try { return (typeof MENU_DATA !== 'undefined' && MENU_DATA) ? MENU_DATA : null; } catch (e) { return null; } }
  function buildSignature(data) {
    var track = $('#sigTrack');
    if (!track || track.children.length) return;
    // Chef-picked dishes, shown in menu order (category order, then item order).
    var catOrder = data.categories.map(function (c) { return c.id; });
    var picks = data.items
      .map(function (it, i) { return { it: it, i: i }; })
      .filter(function (o) { return o.it.img && CHEF_PICKS.indexOf(o.it.id) > -1; })
      .sort(function (a, b) { return (catOrder.indexOf(a.it.cat) - catOrder.indexOf(b.it.cat)) || (a.i - b.i); })
      .map(function (o) { return o.it; });
    if (!picks.length) {
      var byCat = {}, round = 0;
      data.items.forEach(function (it) { if (it.img && FEATURED_CATS.indexOf(it.cat) > -1) (byCat[it.cat] = byCat[it.cat] || []).push(it); });
      while (picks.length < 10 && round < 6) {
        FEATURED_CATS.forEach(function (c) { var a = byCat[c]; if (a && a[round] && picks.length < 10) picks.push(a[round]); });
        round++;
      }
    }
    var lab = function (id) { try { return mLabel(id); } catch (e) { return ''; } };
    var txt = function (it, f) { try { return mText(it, f); } catch (e) { return it[f] || ''; } };
    var esc = function (s) { return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
    track.innerHTML = picks.map(function (it, i) {
      return '<button type="button" class="sig-card" data-cat="' + esc(it.cat) + '">' +
        '<span class="sig-num">' + String(i + 1).padStart(2, '0') + '</span>' +
        '<div class="sig-img"><img loading="lazy" decoding="async" src="/images/' + (CHEF_PICKS.indexOf(it.id) > -1 ? 'sig/' + esc(it.id) + '.webp?v=1' : esc(it.img)) + '" alt="' + esc(txt(it, 'name')) + '"></div>' +
        '<div class="sig-body"><span class="sig-cat">' + esc(lab(it.cat)) + '</span><span class="sig-name">' + esc(txt(it, 'name')) + '</span>' +
        (txt(it, 'desc') ? '<span class="sig-desc">' + esc(txt(it, 'desc')) + '</span>' : '') + '</div></button>';
    }).join('');
    $$('.sig-card', track).forEach(function (card) {
      card.addEventListener('click', function () {
        var cid = card.getAttribute('data-cat');
        var cat = data.categories.filter(function (c) { return c.id === cid; })[0];
        try {
          if (cat && typeof curGroup !== 'undefined' && cat.group !== curGroup) { switchGroup(cat.group); setTimeout(function () { switchCat(cid); }, 320); }
          else switchCat(cid);
        } catch (e) {}
        if (typeof trackEvent === 'function') trackEvent('signature_dish_click', { event_label: cid });
        setTimeout(function () { window.goTo('#menu'); }, 420);
      });
    });
    setupSignaturePin();
  }
  var sigTries = 0;
  (function waitMenu() {
    var data = menuData();
    if (data && data.items) buildSignature(data);
    else if (sigTries++ < 60) setTimeout(waitMenu, 250);
    else { var s = $('#signature'); if (s) s.style.display = 'none'; }
  })();

  var sigST = null;
  function setupSignaturePin() {
    if (!hasG || RM) return;
    var sec = $('#signature'), track = $('#sigTrack');
    if (!sec || !track) return;
    ScrollTrigger.matchMedia({
      '(min-width: 900px)': function () {
        track.classList.add('pinned');
        var dist = function () { return Math.max(0, track.scrollWidth - window.innerWidth); };
        var tw = gsap.to(track, { x: function () { return (RTL ? 1 : -1) * dist(); }, ease: 'none',
          scrollTrigger: { trigger: sec, start: 'top top', end: function () { return '+=' + dist(); }, pin: true, scrub: 0.6, invalidateOnRefresh: true, anticipatePin: 1 } });
        sigST = tw.scrollTrigger;
        return function () { track.classList.remove('pinned'); gsap.set(track, { clearProps: 'x' }); };
      }
    });
    ScrollTrigger.refresh();
  }

  /* ── TripAdvisor badge: give the injected link an accessible name ── */
  var ta = $('.kfoot-ta');
  if (ta && 'MutationObserver' in window) {
    var nameTa = function () { $$('a', ta).forEach(function (x) { if (!x.textContent.trim() && !x.getAttribute('aria-label')) x.setAttribute('aria-label', 'Mare Gastro TripAdvisor'); }); };
    nameTa(); new MutationObserver(nameTa).observe(ta, { childList: true, subtree: true });
  }

  /* ── GSAP-powered motion: set up after load, when the browser is idle (keeps the main thread free for first paint) ── */
  if (!hasG || RM) { $$('.v2-split').forEach(function (el) { el.classList.add('in'); }); return; }
  function heavyMotion() {
  gsap.registerPlugin(ScrollTrigger);
  if (window.SplitText) gsap.registerPlugin(SplitText);

  // Hero: video drifts & scales, content lifts & fades as you scroll away
  if (hero) {
    gsap.to('#hbg', { yPercent: 12, scale: 1.08, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('#home .hc', { yPercent: -18, opacity: 0, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: '70% top', scrub: true } });
    var hb = $('#hbg'); if (hb) hb.style.transform = '';
  }

  // Headline line reveals
  var heads = $$('.v2-split, .a-title, .sc-name, .m-title, .r-title, .k-title');
  function revealHeads() {
    heads.forEach(function (h) {
      if (!window.SplitText) return;
      var st = new SplitText(h, { type: 'lines', mask: 'lines', linesClass: 'v2-line' });
      gsap.from(st.lines, { yPercent: 110, duration: 1.15, ease: 'expo.out', stagger: 0.09,
        scrollTrigger: { trigger: h, start: 'top 86%', once: true } });
    });
  }
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(revealHeads); else revealHeads();

  // Image curtain reveals
  $$('.aimg, .sc-frame, .kmap').forEach(function (el) {
    gsap.fromTo(el, { clipPath: 'inset(14% 8% 14% 8% round 22px)', opacity: 0.4 },
      { clipPath: 'inset(0% 0% 0% 0% round 18px)', opacity: 1, duration: 1.4, ease: 'expo.out',
        scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
  });

  // Ambiance: staggered rise + inner parallax
  $$('.amb-fig').forEach(function (fig, i) {
    gsap.from(fig, { y: 70, opacity: 0, duration: 1.2, ease: 'expo.out', delay: (i % 3) * 0.08,
      scrollTrigger: { trigger: fig, start: 'top 92%', once: true } });
    var img = $('img', fig);
    if (img) gsap.fromTo(img, { yPercent: -6 }, { yPercent: 6, ease: 'none', scrollTrigger: { trigger: fig, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  // Section background parallax for chef / reservation decorative layers
  // Occasion cards: rise in + pointer tilt (desktop)
  $$('.occ-card').forEach(function (c, i) {
    gsap.from(c, { y: 80, opacity: 0, rotate: i % 2 ? 1.5 : -1.5, duration: 1.2, ease: 'expo.out', delay: i * 0.08,
      scrollTrigger: { trigger: '.occ-grid', start: 'top 85%', once: true } });
    if (!window.matchMedia('(hover:hover)').matches) return;
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      gsap.to(c, { rotateY: x * 8, rotateX: -y * 8, transformPerspective: 900, duration: .5, ease: 'power3.out' });
    });
    c.addEventListener('pointerleave', function () { gsap.to(c, { rotateY: 0, rotateX: 0, duration: .8, ease: 'expo.out' }); });
  });

  // Chef quotes card + stats float in
  gsap.from('.st-cell', { y: 40, opacity: 0, duration: 1, ease: 'expo.out', stagger: 0.1, scrollTrigger: { trigger: '.v2-stats', start: 'top 80%', once: true } });

  // Menu: re-measure when panels/tabs change height
  var mp = $('#mPanels');
  if (mp && 'ResizeObserver' in window) {
    var rT; var doRefresh = function () { if (lenis && lenis.isScrolling) { rT = setTimeout(doRefresh, 300); return; } ScrollTrigger.refresh(); };
    new ResizeObserver(function () { clearTimeout(rT); rT = setTimeout(doRefresh, 250); }).observe(mp);
  }
  ScrollTrigger.refresh();
  }
  var startHeavy = function () { (window.requestIdleCallback || function (f) { setTimeout(f, 1); })(heavyMotion, { timeout: 1500 }); };
  if (d.readyState === 'complete') startHeavy(); else window.addEventListener('load', startHeavy);
})();
