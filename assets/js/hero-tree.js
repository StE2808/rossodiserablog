/**
 * Albero hero in stile logo — Rosso di Sera
 * Genera la silhouette (deterministico, seed 42) e orchestra la sequenza:
 * crescita → orizzonte → uccellino → oscillazione → volo verso il logo navbar.
 * Spec: _docs/superpowers/specs/2026-06-10-albero-hero-logo-design.md
 */
(function () {
  'use strict';

  window.__heroVer = 'svgflight-2026-07-05';

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

  // Overlay SVG per il volo, creato subito (non al decollo) e animato via
  // requestAnimationFrame sull'attributo transform. Il vecchio approccio
  // (div HTML creato al decollo + Web Animations API + filter drop-shadow)
  // su iOS/iPadOS WebKit avanzava nel layout ma non veniva mai dipinto dal
  // compositor: volo invisibile su iPhone/iPad, ok su desktop. L'SVG statico
  // ridipinto frame per frame invece dipinge ovunque.
  var SVGNS = 'http://www.w3.org/2000/svg';
  var flySvg = document.createElementNS(SVGNS, 'svg');
  flySvg.setAttribute('class', 'hero-flysvg');
  flySvg.setAttribute('aria-hidden', 'true');
  var flyBird = document.createElementNS(SVGNS, 'g');
  flyBird.innerHTML = birdShape(DARK);
  flyBird.setAttribute('visibility', 'hidden');
  flySvg.appendChild(flyBird);
  hero.appendChild(flySvg);

  // cubic-bezier(0.35, 0.2, 0.35, 1): stesso easing del volo precedente,
  // risolto in JS (Newton) perché l'animazione gira su requestAnimationFrame
  function cubicBezier(p1x, p1y, p2x, p2y) {
    var cx = 3 * p1x, bx = 3 * (p2x - p1x) - cx, ax = 1 - cx - bx;
    var cy = 3 * p1y, by = 3 * (p2y - p1y) - cy, ay = 1 - cy - by;
    function sampleX(t) { return ((ax * t + bx) * t + cx) * t; }
    function solveX(x) {
      var t = x, i, d;
      for (i = 0; i < 5; i++) {
        d = (3 * ax * t + 2 * bx) * t + cx;
        if (Math.abs(d) < 1e-6) break;
        t -= (sampleX(t) - x) / d;
      }
      return t;
    }
    return function (x) {
      if (x <= 0) return 0;
      if (x >= 1) return 1;
      var t = solveX(x);
      return ((ay * t + by) * t + cy) * t;
    };
  }
  var flyEase = cubicBezier(0.35, 0.2, 0.35, 1);

  // doppio rAF: lo stato nascosto viene renderizzato prima del via
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { showAll(false); });
  });

  setTimeout(function () { treeGroup.classList.add('swaying'); }, 4200);
  setTimeout(flight, 5400);

  function flight() {
    var logo = document.querySelector('.navbar-logo');
    var svgRect = svg.getBoundingClientRect();
    if (!logo || !svgRect.width) { revealCta(); return; }
    var heroRect = hero.getBoundingClientRect();
    var lRect = logo.getBoundingClientRect();

    // Posizione della cima dell'albero: calcolata dal box dell'<svg> (elemento
    // affidabile e fuori dal gruppo che oscilla) mappato sul viewBox 0 0 400 500.
    // Evita getBoundingClientRect() sul marker SVG (circle r=1 fill=none): su
    // WebKit/iOS i sotto-elementi SVG non disegnati restituiscono coordinate
    // errate/zero, il volo partiva ma fuori schermo. Vedi backup 2026-06-13.
    var scale = svgRect.width / 400;

    // coordinate in px relativi all'hero, riferite al centro del corpo (13,13)
    var startX = svgRect.left + TOP[0] * scale - heroRect.left;
    var startY = svgRect.top + (TOP[1] - 5) * scale - heroRect.top;
    // atterraggio: bordo alto del cerchio del logo, come nel logo originale
    var endX = lRect.left - heroRect.left + lRect.width / 2;
    var endY = lRect.top - heroRect.top + lRect.height * 0.13;
    var dx = endX - startX, dy = endY - startY;

    // stessi keyframe e archi del volo precedente
    var KF = [
      { t: 0,    x: startX,             y: startY,                  s: 1.5, o: 1 },
      { t: 0.45, x: startX + dx * 0.35, y: startY + dy * 0.55 - 60, s: 1.3, o: 1 },
      { t: 0.8,  x: startX + dx * 0.8,  y: startY + dy * 0.95 - 25, s: 1.0, o: 1 },
      { t: 0.92, x: startX + dx * 0.96, y: startY + dy * 0.99 - 5,  s: 0.6, o: 1 },
      { t: 1,    x: endX,               y: endY,                    s: 0,   o: 0 }
    ];

    function apply(p) {
      var i = 1;
      while (i < KF.length - 1 && p > KF[i].t) i++;
      var a = KF[i - 1], b = KF[i];
      var u = flyEase((p - a.t) / (b.t - a.t));
      var x = a.x + (b.x - a.x) * u, y = a.y + (b.y - a.y) * u;
      var s = a.s + (b.s - a.s) * u, o = a.o + (b.o - a.o) * u;
      flyBird.setAttribute('opacity', o.toFixed(3));
      // scale(-s, s): specchiato in orizzontale attorno al centro del corpo,
      // come lo scaleX(-1) del volo precedente
      flyBird.setAttribute('transform',
        'translate(' + x.toFixed(2) + ' ' + y.toFixed(2) + ')' +
        ' scale(' + (-s).toFixed(4) + ' ' + s.toFixed(4) + ')' +
        ' translate(-13 -13)');
    }

    treeBird.style.transition = 'opacity 0.15s';
    treeBird.style.opacity = '0';
    apply(0);
    flyBird.setAttribute('visibility', 'visible');

    var DURATION = 2600, t0 = null;
    function frame(now) {
      if (t0 === null) t0 = now;
      var p = Math.min((now - t0) / DURATION, 1);
      apply(p);
      if (p < 1) {
        requestAnimationFrame(frame);
      } else {
        flyBird.setAttribute('visibility', 'hidden');
        revealCta();
      }
    }
    requestAnimationFrame(frame);
  }
})();
