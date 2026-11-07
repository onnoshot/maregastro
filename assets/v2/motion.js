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
  else { window.addEventListener('load', function () { setTimeout(hideLoader, 250); }); setTimeout(hideLoader, 1600); }

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
  function menuData() { try { return (typeof MENU_DATA !== 'undefined' && MENU_DATA) ? MENU_DATA : null; } catch (e) { return null; } }
  function buildSignature(data) {
    var track = $('#sigTrack');
    if (!track || track.children.length) return;
    var byCat = {};
    data.items.forEach(function (it) { if (it.img && FEATURED_CATS.indexOf(it.cat) > -1) (byCat[it.cat] = byCat[it.cat] || []).push(it); });
    var picks = [], round = 0;
    while (picks.length < 10 && round < 6) {
      FEATURED_CATS.forEach(function (c) { var a = byCat[c]; if (a && a[round] && picks.length < 10) picks.push(a[round]); });
      round++;
    }
    var lab = function (id) { try { return mLabel(id); } catch (e) { return ''; } };
    var txt = function (it, f) { try { return mText(it, f); } catch (e) { return it[f] || ''; } };
    var esc = function (s) { return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
    track.innerHTML = picks.map(function (it, i) {
      return '<button type="button" class="sig-card" data-cat="' + esc(it.cat) + '">' +
        '<span class="sig-num">' + String(i + 1).padStart(2, '0') + '</span>' +
        '<div class="sig-img"><img loading="lazy" decoding="async" src="/images/' + esc(it.img) + '" alt="' + esc(txt(it, 'name')) + '"></div>' +
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

  /* ── GSAP-powered motion ── */
  if (!hasG || RM) { $$('.v2-split').forEach(function (el) { el.classList.add('in'); }); return; }
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
  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
