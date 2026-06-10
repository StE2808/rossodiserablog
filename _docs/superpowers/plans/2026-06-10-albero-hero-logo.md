# Albero Hero in Stile Logo — Piano di Implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sostituire l'albero stilizzato dell'hero della homepage con una silhouette in stile logo (uccellino e orizzonte inclusi) animata: crescita progressiva, oscillazione, volo finale dell'uccellino verso il logo della navbar.

**Architecture:** L'albero (1068 segmenti, generatore deterministico mulberry32 seed 42) viene generato a runtime da `assets/js/hero-tree.js` dentro un contenitore vuoto in `_layouts/home.html`. I path nascono già nascosti (`pathLength="1"`, dasharray/offset 1) con transizioni CSS inline; il JS dà il via, attiva l'oscillazione a 4.2 s e lancia il volo a 5.4 s con Web Animations API. Il CSS perde le ~120 righe del vecchio albero e guadagna le regole nuove.

**Tech Stack:** Jekyll 4.3.3 (sito statico), vanilla JS (nessuna dipendenza), CSS transitions + Web Animations API.

**Spec di riferimento:** `_docs/superpowers/specs/2026-06-10-albero-hero-logo-design.md`
**Mockup approvato:** `.superpowers/brainstorm/9658-1781071326/content/volo-uccellino-v7.html` (testo hero al 40%)

**Nota di verifica:** il progetto non ha framework di test JS. Le verifiche sono: `node --check` per la sintassi, build Jekyll, grep sull'output buildato, controllo visivo nel browser (checklist finale).

---

### Task 1: Creare `assets/js/hero-tree.js`

**Files:**
- Create: `assets/js/hero-tree.js`

- [ ] **Step 1: Scrivere il file completo**

Creare `assets/js/hero-tree.js` con esattamente questo contenuto (è il codice dei mockup approvati, adattato al DOM reale del sito):

```js
/**
 * Albero hero in stile logo — Rosso di Sera
 * Genera la silhouette (deterministico, seed 42) e orchestra la sequenza:
 * crescita → orizzonte → uccellino → oscillazione → volo verso il logo navbar.
 * Spec: _docs/superpowers/specs/2026-06-10-albero-hero-logo-design.md
 */
(function () {
  'use strict';

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

  // doppio rAF: lo stato nascosto viene renderizzato prima del via
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { showAll(false); });
  });

  setTimeout(function () { treeGroup.classList.add('swaying'); }, 4200);
  setTimeout(flight, 5400);

  function flight() {
    var logo = document.querySelector('.navbar-logo');
    if (!logo || !Element.prototype.animate) return;
    var heroRect = hero.getBoundingClientRect();
    var mRect = svg.querySelector('#hero-top-marker').getBoundingClientRect();
    var lRect = logo.getBoundingClientRect();

    var startX = mRect.left - heroRect.left - 15;
    var startY = mRect.top - heroRect.top - 20;
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
      { transform: 'translate(' + startX + 'px,' + startY + 'px) scaleX(-1) scale(1)', opacity: 1, offset: 0 },
      { transform: 'translate(' + (startX + dx * 0.35) + 'px,' + (startY + dy * 0.55 - 60) + 'px) scaleX(-1) scale(0.85)', opacity: 1, offset: 0.45 },
      { transform: 'translate(' + (startX + dx * 0.8) + 'px,' + (startY + dy * 0.95 - 25) + 'px) scaleX(-1) scale(0.68)', opacity: 1, offset: 0.8 },
      { transform: 'translate(' + (startX + dx * 0.96) + 'px,' + (startY + dy * 0.99 - 5) + 'px) scaleX(-1) scale(0.5)', opacity: 1, offset: 0.92 },
      { transform: 'translate(' + endX + 'px,' + endY + 'px) scaleX(-1) scale(0)', opacity: 0, offset: 1 }
    ], { duration: 2000, easing: 'cubic-bezier(0.35, 0.2, 0.35, 1)', fill: 'forwards' });
  }
})();
```

- [ ] **Step 2: Verificare la sintassi**

Run: `node --check assets/js/hero-tree.js && echo SINTASSI_OK`
Expected: `SINTASSI_OK`

- [ ] **Step 3: Verificare il determinismo del generatore**

Run:
```bash
node -e "
function mulberry32(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;var t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}
var rnd=mulberry32(42);
console.log(rnd().toFixed(6), rnd().toFixed(6));
"
```
Expected: `0.601104 0.448291` (se i primi due numeri sono questi, il PRNG è identico a quello dei mockup approvati)

- [ ] **Step 4: Commit**

```bash
git add assets/js/hero-tree.js
git commit -m "Aggiungi script albero hero in stile logo

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Sostituire l'SVG statico in `_layouts/home.html`

**Files:**
- Modify: `_layouts/home.html:8-106` (il blocco `<svg class="hero-tree">...</svg>`)
- Modify: `_layouts/home.html` (fondo del file, aggiunta `<script>`)

- [ ] **Step 1: Sostituire il blocco SVG con il contenitore**

In `_layouts/home.html` il blocco da riga 8 (`<svg class="hero-tree" viewBox="0 0 400 500" ...>`) a riga 106 (`</svg>`) va sostituito con questa singola riga:

```html
    <div id="hero-tree-holder" class="hero-tree" aria-hidden="true"></div>
```

Il commento `<!-- Albero che cresce -->` alla riga 7 resta. Verificare che subito dopo il contenitore ci sia ancora `<div class="hero-content">`.

- [ ] **Step 2: Aggiungere lo script in fondo al file**

In fondo a `_layouts/home.html` (dopo l'ultima riga esistente, fuori da ogni `<section>`), aggiungere:

```html

<script src="{{ '/assets/js/hero-tree.js' | relative_url }}" defer></script>
```

- [ ] **Step 3: Verificare che il vecchio albero sia sparito dal layout**

Run: `grep -c "tree-branch\|tree-trunk\|twig-" _layouts/home.html || echo NESSUN_RESIDUO`
Expected: `NESSUN_RESIDUO` (grep non trova nulla ed esce con errore, quindi stampa la stringa)

Run: `grep -c "hero-tree-holder\|hero-tree.js" _layouts/home.html`
Expected: `2` (una occorrenza per il contenitore, una per lo script)

- [ ] **Step 4: Commit**

```bash
git add _layouts/home.html
git commit -m "Sostituisci SVG albero hero con contenitore per generazione runtime

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Aggiornare `assets/css/style.css`

**Files:**
- Modify: `assets/css/style.css:332-453` (blocco vecchio albero, da `/* Albero hero */` alla chiusura di `@keyframes sway`)
- Modify: `assets/css/style.css:455` (regola `.hero-content`)

**Attenzione:** i numeri di riga si riferiscono allo stato attuale del file; dopo le sostituzioni slittano. Identificare i blocchi tramite il loro contenuto, non solo la riga.

- [ ] **Step 1: Sostituire il blocco del vecchio albero**

Il blocco da eliminare inizia con il commento `/* Albero hero */` (riga ~332) e termina con la chiusura di `@keyframes sway` (riga ~453):

```css
@keyframes sway {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(1deg); }
    75% { transform: rotate(-1deg); }
}
```

Contiene: `.hero-tree`, `.tree-group`, `.tree-trunk`, `.tree-branch`, tutte le `.branch-main-*`, `.branch-primary-*`, `.branch-secondary-*`, `.twig-1`...`.twig-45`, e i keyframes `grow-trunk`, `grow-branch`, `sway`. L'intero blocco va sostituito con:

```css
/* Albero hero (stile logo, generato a runtime da hero-tree.js) */
.hero-tree {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 500px;
    pointer-events: none;
    z-index: 1;
}

.hero-tree svg {
    width: 100%;
    height: auto;
    display: block;
}

.hero-tree .tree-g.swaying {
    animation: hero-sway 5s ease-in-out infinite;
    transform-origin: 200px 462px;
}

@keyframes hero-sway {
    0%, 100% { transform: rotate(0deg); }
    50% { transform: rotate(0.8deg); }
}

/* Uccellino in volo verso il logo (creato da hero-tree.js) */
.hero-flybird {
    position: absolute;
    top: 0;
    left: 0;
    width: 30px;
    height: 22px;
    z-index: 1001;
    pointer-events: none;
}

.hero-flybird svg {
    width: 100%;
    height: 100%;
    overflow: visible;
}

@media (prefers-reduced-motion: reduce) {
    .hero-tree .tree-g.swaying { animation: none; }
}
```

- [ ] **Step 2: Posizionare il testo hero al 40%**

La regola `.hero-content` (subito dopo il blocco appena sostituito) attualmente è:

```css
.hero-content {
    text-align: center;
    color: white;
    z-index: 10;
    padding: 2rem;
    max-width: 900px;
```

Va modificata aggiungendo il posizionamento assoluto al 40% (l'hero resta `display: flex` ma la regola assoluta vince):

```css
.hero-content {
    position: absolute;
    top: 40%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    text-align: center;
    color: white;
    z-index: 10;
    padding: 2rem;
    max-width: 900px;
```

(le righe successive della regola restano invariate)

- [ ] **Step 3: Verificare che non restino residui del vecchio albero**

Run: `grep -c "twig-\|branch-main\|branch-primary\|branch-secondary\|grow-trunk\|grow-branch\|tree-trunk\|tree-group" assets/css/style.css || echo NESSUN_RESIDUO`
Expected: `NESSUN_RESIDUO`

Run: `grep -c "hero-sway\|hero-flybird\|tree-g.swaying" assets/css/style.css`
Expected: `4` (`.tree-g.swaying`, `hero-sway` ×2 — regola e keyframes —, `.hero-flybird`; il selettore `.hero-flybird svg` aggiunge la quinta occorrenza: accettare `4` o `5`)

Verificare anche che la regola responsive `.hero-tree { width: 300px; }` (riga ~1360, dentro la media query) sia ancora presente e invariata:

Run: `grep -n "width: 300px" assets/css/style.css`
Expected: una riga dentro la sezione `/* Albero responsive */`

- [ ] **Step 4: Commit**

```bash
git add assets/css/style.css
git commit -m "Sostituisci CSS albero hero: regole nuovo albero, testo hero al 40%

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Build, verifica e controllo visivo

**Files:** nessuna modifica (solo verifica)

- [ ] **Step 1: Build Jekyll**

Run: `bundle exec jekyll build 2>&1 | tail -3`
Expected: `done in X.XXX seconds.` senza errori

- [ ] **Step 2: Verificare l'output buildato**

Run: `grep -c "hero-tree-holder" _site/index.html && grep -c "hero-tree.js" _site/index.html`
Expected: `1` e `1`

Run: `test -f _site/assets/js/hero-tree.js && echo JS_PRESENTE`
Expected: `JS_PRESENTE`

- [ ] **Step 3: Controllo visivo nel browser (manuale, con Stefano)**

Run: `bundle exec jekyll serve` e aprire `http://localhost:4000` con hard refresh (Cmd+Shift+R). Checklist dalla spec:

1. La scena parte vuota: nessun flash dell'albero completo
2. Sequenza: crescita (0-3 s) → orizzonte → uccellino (~3 s) → oscillazione (~4 s) → volo verso il logo (~5,4 s) con rimpicciolimento finale fino a sparire sul logo
3. Le linee d'orizzonte restano immobili mentre l'albero oscilla
4. Il testo hero non copre l'uccellino sulla cima
5. Ridurre la finestra (~768px e ~375px): l'albero si ridimensiona, il volo arriva comunque sul logo
6. macOS: Impostazioni di Sistema → Accessibilità → Schermo → "Riduci velocità animazioni" attivo → ricaricare: albero già completo e fermo, uccellino fermo sulla cima, nessun volo
7. Aprire un articolo qualsiasi: nessun errore nella console JS (lo script non gira fuori dalla homepage)

- [ ] **Step 4: Push (solo dopo l'ok visivo di Stefano)**

```bash
git pull --rebase && git push
```

Il push su `main` fa partire il deploy automatico su GitHub Pages. Verificare dopo qualche minuto su `https://rossodiserablog.it` con hard refresh.
