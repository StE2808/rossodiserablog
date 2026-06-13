/**
 * Albero hero in stile logo — Rosso di Sera
 * Genera la silhouette (deterministico, seed 42) e orchestra la sequenza:
 * crescita → orizzonte → uccellino → oscillazione → volo verso il logo navbar.
 * Spec: _docs/superpowers/specs/2026-06-10-albero-hero-logo-design.md
 */
(function () {
  'use strict';

  window.__heroVer = 'svgrect-2026-06-13';

  var hero = document.querySelector('.hero');
  var holder = document.getElementById('hero-tree-holder');
  if (!hero || !holder) return;

  var DARK = 'rgba(26,8,8,0.88)';

  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function generateTree(seed) {
    var rnd = mulberry32(seed);
    var segs = [];
    function branch(x, y, angle, len, width, depth) {
      if (depth === 0 || len < 6) return;
      var a = angle + (rnd() - 0.5) * 0.25;
      var ex = x + Math.cos(a) * len, ey = y + Math.sin(a) * len;
      var cx = x + Math.cos(a + (rnd() - 0.5) * 0.5) * len * 0.5;
      var cy = y + Math.sin(a + (rnd() - 0.5) * 0.5) * len * 0.5;
      segs.push({
        d: 'M' + x.toFixed(1) + ' ' + y.toFixed(1) +
           ' Q' + cx.toFixed(1) + ' ' + cy.toFixed(1) +
           ' ' + ex.toFixed(1) + ' ' + ey.toFixed(1),
        w: width, depth: depth, tip: [ex, ey]
      });
      var n = depth > 6 ? 2 : (rnd() < 0.3 ? 3 : 2);
      for (var i = 0; i < n; i++) {
        var sign = i === 0 ? -1 : (i === 1 ? 1 : (rnd() < 0.5 ? -1 : 1));
        var na = a + sign * (0.25 + rnd() * 0.45);
        na = na + (-Math.PI / 2 - na) * 0.12;
        branch(ex, ey, na, len * (0.72 + rnd() * 0.12), width * 0.62, depth - 1);
      }
    }
    branch(200, 462, -Math.PI / 2, 80, 14, 9);
    return segs;
  }

  var SEGS = generateTree(42);
  var TOP = SEGS.reduce(function (b, s) {
    return (!b || s.tip[1] < b.tip[1]) ? s : b;
  }, null).tip;

  function birdShape(color) {
    return '<g fill="' + color + '">' +
      '<ellipse cx="13" cy="13" rx="7" ry="4.5"/>' +
      '<circle cx="19" cy="9" r="3"/>' +
      '<path d="M21.5 9 l5 1.2 l-5 1.2 z"/>' +
      '<path d="M7 12 l-7 4 l7 0.5 z"/></g>';
  }

  // I path nascono già nascosti (pathLength/dasharray/dashoffset = 1):
  // niente flash dell'albero completo prima dell'animazione
  function treeSVG() {
    var s = '<svg viewBox="0 0 400 500" xmlns="http://www.w3.org/2000/svg">';
    s += '<g class="tree-g">';
    SEGS.forEach(function (seg, i) {
      var delay = (9 - seg.depth) * 280 + (i % 7) * 35;
      s += '<path class="seg" d="' + seg.d + '" stroke="' + DARK +
           '" stroke-width="' + seg.w.toFixed(1) +
           '" fill="none" stroke-linecap="round" pathLength="1"' +
           ' stroke-dasharray="1" stroke-dashoffset="1"' +
           ' style="transition: stroke-dashoffset 0.6s ease-out ' + delay + 'ms"/>';
    });
    s += '<circle id="hero-top-marker" cx="' + TOP[0] + '" cy="' + TOP[1] + '" r="1" fill="none"/>';
    s += '<g class="tree-bird" style="opacity:0; transition: opacity 0.7s ease-in 3100ms"' +
         ' transform="translate(' + (TOP[0] - 13) + ',' + (TOP[1] - 18) + ')">' +
         birdShape(DARK) + '</g>';
    s += '</g>';
    s += '<g class="horizon-g">';
    var ys = [448, 454, 459], ws = [150, 110, 70];
    for (var i = 0; i < 3; i++) {
      s += '<path class="hz" d="M' + (200 - ws[i]) + ' ' + ys[i] +
           ' L' + (200 + ws[i]) + ' ' + ys[i] +
           '" stroke="rgba(26,8,8,0.5)" stroke-width="' + (2 - i * 0.5) +
           '" stroke-linecap="round" fill="none" pathLength="1"' +
           ' stroke-dasharray="1" stroke-dashoffset="1"' +
           ' style="transition: stroke-dashoffset 0.9s ease-out ' + (2400 + i * 150) + 'ms"/>';
    }
    s += '</g></svg>';
    return s;
  }

  holder.innerHTML = treeSVG();
  var svg = holder.querySelector('svg');
  var treeGroup = svg.querySelector('.tree-g');
  var segEls = svg.querySelectorAll('.seg');
  var hzEls = svg.querySelectorAll('.hz');
  var treeBird = svg.querySelector('.tree-bird');

  function showAll(instant) {
    segEls.forEach(function (p) {
      if (instant) p.style.transition = 'none';
      p.style.strokeDashoffset = '0';
    });
    hzEls.forEach(function (p) {
      if (instant) p.style.transition = 'none';
      p.style.strokeDashoffset = '0';
    });
    if (instant) treeBird.style.transition = 'none';
    treeBird.style.opacity = '1';
  }

  var reduced = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) {
    showAll(true);
    return;
  }

  // CTA e "Scorri" restano nascosti fino alla fine del volo
  hero.classList.add('hero-cta-pending');
  function revealCta() { hero.classList.remove('hero-cta-pending'); }
  setTimeout(revealCta, 8400); // rete di sicurezza se il volo non parte

  // doppio rAF: lo stato nascosto viene renderizzato prima del via
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { showAll(false); });
  });

  setTimeout(function () { treeGroup.classList.add('swaying'); }, 4200);
  setTimeout(flight, 5400);

  function flight() {
    var logo = document.querySelector('.navbar-logo');
    if (!logo || !Element.prototype.animate) { revealCta(); return; }
    var heroRect = hero.getBoundingClientRect();
    var lRect = logo.getBoundingClientRect();

    // Posizione della cima dell'albero: calcolata dal box dell'<svg> (elemento
    // affidabile e fuori dal gruppo che oscilla) mappato sul viewBox 0 0 400 500.
    // Evita getBoundingClientRect() sul marker SVG (circle r=1 fill=none): su
    // WebKit/iOS i sotto-elementi SVG non disegnati restituiscono coordinate
    // errate/zero, il volo partiva ma fuori schermo. Vedi backup 2026-06-13.
    var svgRect = svg.getBoundingClientRect();
    if (!svgRect.width) { revealCta(); return; }
    var scale = svgRect.width / 400;
    var markerLeft = svgRect.left + TOP[0] * scale;
    var markerTop = svgRect.top + TOP[1] * scale;

    var startX = markerLeft - heroRect.left - 15;
    var startY = markerTop - heroRect.top - 20;
    // atterraggio: bordo alto del cerchio del logo, come nel logo originale
    var endX = lRect.left - heroRect.left + lRect.width / 2 - 9;
    var endY = lRect.top - heroRect.top + lRect.height * 0.13 - 18;

    treeBird.style.transition = 'opacity 0.15s';
    treeBird.style.opacity = '0';

    var fb = document.createElement('div');
    fb.className = 'hero-flybird';
    fb.innerHTML = '<svg viewBox="0 0 30 22">' + birdShape(DARK) + '</svg>';
    hero.appendChild(fb);

    var dx = endX - startX, dy = endY - startY;
    fb.animate([
      { transform: 'translate(' + startX + 'px,' + startY + 'px) scaleX(-1) scale(1.5)', opacity: 1, offset: 0 },
      { transform: 'translate(' + (startX + dx * 0.35) + 'px,' + (startY + dy * 0.55 - 60) + 'px) scaleX(-1) scale(1.3)', opacity: 1, offset: 0.45 },
      { transform: 'translate(' + (startX + dx * 0.8) + 'px,' + (startY + dy * 0.95 - 25) + 'px) scaleX(-1) scale(1.0)', opacity: 1, offset: 0.8 },
      { transform: 'translate(' + (startX + dx * 0.96) + 'px,' + (startY + dy * 0.99 - 5) + 'px) scaleX(-1) scale(0.6)', opacity: 1, offset: 0.92 },
      { transform: 'translate(' + endX + 'px,' + endY + 'px) scaleX(-1) scale(0)', opacity: 0, offset: 1 }
    ], { duration: 2600, easing: 'cubic-bezier(0.35, 0.2, 0.35, 1)', fill: 'forwards' })
      .onfinish = revealCta;
  }
})();
