/* Anteprima degli approfondimenti dentro Sveltia (19/11/2026).
 *
 * Rifà in JavaScript quello che fa il sito:
 *   - analizza(): legge il documento unico, come scripts/documento_approfondimento.py
 *   - pagina():   impagina come _layouts/numero.html, con /assets/css/numero.css
 * Sono COPIE: se cambia il layout o il parser, va cambiato anche qui.
 * Il controllo è scripts/controlla_anteprima.py (confronta con le pagine vere di racket e Folla).
 * Senza il «Leggi anche» automatico, la newsletter e i commenti: dipendono dal sito.
 */
(function (radice) {
  'use strict';

  var SI = ['sì', 'si', 'yes', 'true', 'vero'];
  var ROMANI = ['I', 'II', 'III', 'IV', 'V', 'VI'];
  var MESI = 'gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre'.split(' ');
  var GIORNI = 'domenica lunedì martedì mercoledì giovedì venerdì sabato'.split(' ');
  var AUTORI = { 'stefano-vozzi': 'Stefano Vozzi', 'lino-rialti': 'Lino Rialti' };
  var GENERATA = 'Illustrazione generata: la scena non rappresenta un luogo reale.';

  /* ---------- il parser (copia di documento_approfondimento.py) ---------- */

  function bool(v) { return SI.indexOf(String(v).trim().toLowerCase()) >= 0; }

  function paragrafi(righe) {
    var out = [], cur = [];
    righe.forEach(function (r) {
      if (r.trim()) cur.push(r.replace(/\s+$/, ''));
      else if (cur.length) { out.push(cur); cur = []; }
    });
    if (cur.length) out.push(cur);
    return out;
  }

  function unisci(p) {
    var elenco = p.some(function (r) { return /^\s*(\d+\.|[-*])\s/.test(r); });
    return p.join(elenco ? '\n' : ' ');
  }

  function testo(righe) { return paragrafi(righe).map(unisci).join('\n\n'); }

  function etichetta(riga, ammesse) {
    var m = /^([A-Za-zÀ-ÿ ]+?):\s?(.*)$/.exec(riga);
    if (m && ammesse.indexOf(m[1].trim().toLowerCase()) >= 0) return [m[1].trim().toLowerCase(), m[2].trim()];
    return null;
  }

  function sezioni(righe, livello) {
    var out = [], titolo = null, cur = [];
    righe.forEach(function (r) {
      if (r.indexOf(livello) === 0 && r.indexOf(livello + '#') !== 0) {
        out.push([titolo, cur]); titolo = r.slice(livello.length).trim(); cur = [];
      } else cur.push(r);
    });
    out.push([titolo, cur]);
    return out;
  }

  function frase(righe) {
    var d = { type: 'frase' }, grande = [];
    var mappa = { 'sotto': 'sotto', 'foto': 'image', 'descrizione foto': 'image_alt',
      'foto generata': 'generata', 'foto intera': 'adatta', 'didascalia': 'didascalia' };
    righe.forEach(function (r) {
      var e = etichetta(r, Object.keys(mappa));
      if (e) { var k = mappa[e[0]]; d[k] = (k === 'generata' || k === 'adatta') ? bool(e[1]) : e[1]; }
      else if (r.trim()) grande.push(r.trim());
    });
    d.grande = grande.join('\n');
    return d;
  }

  function tabella(titolo, righe) {
    var d = { type: 'dati', titolo: titolo, colonna: 'Numero' };
    var mappa = { 'didascalia': 'didascalia', 'colonna': 'colonna', 'limite': 'limite' };
    var voceK = { 'numero': 'cifra', 'cifra': 'cifra', 'unità': 'unita', 'unita': 'unita', 'cosa': 'testo', 'fonte': 'fonte' };
    var ammesse = Object.keys(mappa).concat(Object.keys(voceK));
    var celle = [], voci = [], cur = {};
    righe.concat(['']).forEach(function (r) {
      var e = etichetta(r, ammesse);
      if (e && voceK[e[0]]) {
        var k = voceK[e[0]];
        if (k === 'cifra' && Object.keys(cur).length) { voci.push(cur); cur = {}; }
        cur[k] = e[1];
        return;
      }
      if (!r.trim() && Object.keys(cur).length) { voci.push(cur); cur = {}; }
      if (e) d[mappa[e[0]]] = e[1];
      else if (r.trim().indexOf('|') === 0) {
        var c = r.trim().replace(/^\||\|$/g, '').split('|').map(function (x) { return x.trim(); });
        if (c.every(function (x) { return /^:?-{2,}:?$/.test(x); })) return;
        celle.push(c);
      }
    });
    var out = celle.slice(1).map(function (c) { return { cifra: c[0], unita: c[1], testo: c[2], fonte: c[3] }; });
    voci.forEach(function (v) {
      var f = v.fonte || '';
      if (f && f.toLowerCase().indexOf('fonte') !== 0) f = 'Fonte: ' + f;
      out.push({ cifra: v.cifra || '', unita: v.unita || '', testo: v.testo || '', fonte: f });
    });
    d.righe = out;
    return d;
  }

  function analizza(corpo) {
    var righe = String(corpo || '').replace(/\r\n/g, '\n').split('\n');
    var campi = {}, movimenti = [];
    sezioni(righe, '## ').forEach(function (s) {
      var titolo = s[0], blocco = s[1];
      if (titolo === null) {
        blocco.forEach(function (r) {
          var e = etichetta(r, ['catenaccio', 'il punto']);
          if (e) campi[e[0] === 'catenaccio' ? 'catenaccio' : 'punto'] = e[1];
        });
        return;
      }
      var i = titolo.indexOf(':');
      var nome = (i >= 0 ? titolo.slice(0, i) : titolo).trim();
      if (nome.toLowerCase() === 'apertura') {
        var tema = { titolo: i >= 0 ? titolo.slice(i + 1).trim() : '' }, t = [];
        blocco.forEach(function (r) {
          var e = etichetta(r, ['sottotitolo']);
          if (e) tema.catenaccio = e[1]; else t.push(r);
        });
        tema.apertura = testo(t);
        campi.tema = tema;
      } else if (nome.toLowerCase() === 'domande') {
        campi.domande = blocco.filter(function (r) { return r.trim().charAt(0) === '-'; })
          .map(function (r) { return r.trim().slice(1).trim(); });
      } else {
        var m = { nome: nome, titolo: titolo, blocchi: [], dopo: [] };
        var parti = sezioni(blocco, '### ');
        parti[0][1].forEach(function (r) {
          var e = etichetta(r, ['indice', 'sommario', 'colonne']);
          if (!e) return;
          if (e[0] === 'sommario') m.sommario = e[1].split(';').map(function (x) { return x.trim(); }).filter(Boolean);
          else if (e[0] === 'colonne') m.colonne = parseInt(e[1], 10);
          else m.indice = e[1];
        });
        parti.slice(1).forEach(function (p) {
          var t2 = p[0], rr = p[1], l = t2.toLowerCase();
          if (l === 'frase rossa') m.dopo.push(frase(rr));
          else if (l.indexOf('tabella') === 0) {
            var j = t2.indexOf(':');
            m.dopo.push(tabella(j >= 0 ? t2.slice(j + 1).trim() : '', rr));
          } else m.blocchi.push({ titolo: t2, tipo: /\?$/.test(t2) ? 'domanda' : 'testo', testo: testo(rr) });
        });
        movimenti.push(m);
      }
    });
    if (movimenti.length) campi.movimenti = movimenti;
    return campi;
  }

  /* ---------- l'impaginazione (copia di _layouts/numero.html) ---------- */

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function slugify(s) { return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, ''); }
  function md(s, opz) {
    var mk = opz.markdown || function (x) { return '<p>' + esc(x) + '</p>'; };
    return mk(String(s || ''));
  }
  function mdRiga(s, opz) { return md(s, opz).replace(/<\/?p>/g, '').trim(); }

  function dataEstesa(v) {
    if (!v) return '';
    var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(v));
    var d = m ? new Date(+m[1], +m[2] - 1, +m[3]) : new Date(v);
    if (isNaN(d)) return '';
    var g = GIORNI[d.getDay()];
    return g.charAt(0).toUpperCase() + g.slice(1) + ' ' + d.getDate() + ' ' + MESI[d.getMonth()] + ' ' + d.getFullYear();
  }

  function pagina(fm, opz) {
    opz = opz || {};
    var img = opz.immagine || function (p) { return p; };
    var p = Object.assign({}, fm, analizza(fm.body));
    var autore = AUTORI[p.author] || p.author || '';
    var h = [];
    h.push('<div class="numero">');
    h.push('<div class="prova anteprima"><span>Anteprima dentro Sveltia: quasi uguale alla pagina vera. Quella esatta è su /anteprima/ dopo il salvataggio.</span></div>');
    h.push('<main id="contenuto">');
    // copertina
    h.push('<section class="cop"><div class="sx">');
    h.push('<p class="testata"><a><img alt="" src="' + esc(img('/assets/images/numeri/logo-testata.png')) + '" width="512" height="512"><span>Rosso<br>di Sera<b class="blog">blog</b></span></a></p>');
    h.push('<div class="uscita"><span>Approfondimento · N. ' + esc(p.numero) + (p.tema_breve ? ' · ' + esc(p.tema_breve) : '') + '</span><span><time>' + esc(dataEstesa(p.uscita || p.data_pubblicazione || p.date)) + '</time></span></div>');
    h.push('<h1>' + esc(p.title) + '</h1>');
    if (p.catenaccio) h.push('<div class="cat">' + esc(p.catenaccio) + '</div>');
    h.push('<p class="firma">di <a>' + esc(autore) + '</a></p>');
    h.push(p.punto ? '<aside aria-label="Il punto" class="punto"><b>Il punto</b><p>' + esc(p.punto) + '</p></aside>' : '<hr class="filetto">');
    h.push('<div class="somm">');
    (p.movimenti || []).forEach(function (m) {
      h.push('<div class="r"><span class="et">' + esc(m.nome) + '</span>' + (m.sommario || []).map(function (s) { return '<span>' + esc(s) + '</span>'; }).join('') + '</div>');
    });
    h.push('</div></div>');
    if (p.image) {
      h.push('<figure class="foto"><img alt="' + esc(p.image_alt) + '" src="' + esc(img(p.image)) + '">');
      if (p.image_generata) h.push('<figcaption>' + GENERATA + '</figcaption>');
      else if (p.image_caption) h.push('<figcaption>' + esc(p.image_caption) + '</figcaption>');
      h.push('</figure>');
    } else h.push('<figure class="foto ph"><b>Immagine di copertina in arrivo</b></figure>');
    h.push('</section>');
    // leggi anche
    h.push('<aside class="rubriche"><h2>Leggi anche</h2><div class="rub-grid">');
    var la = (p.leggi_anche || []).slice(0, 4);
    if (la.length) la.forEach(function (r) { h.push('<div class="rub"><span>' + esc(r.rubrica || '') + '</span><a>' + esc(r.titolo) + '</a></div>'); });
    else h.push('<div class="rub"><span>Sul sito</span><a>Qui escono gli ultimi quattro articoli</a></div>');
    h.push('</div></aside>');
    // tema
    var tema = p.tema || {};
    h.push('<section class="tema"><div><div class="et">Il tema</div><h2>' + esc(tema.titolo) + '</h2>');
    if (tema.catenaccio) h.push('<div class="cat">' + esc(tema.catenaccio) + '</div>');
    h.push('<hr class="filetto"><div class="corpo">' + md(tema.apertura, opz) + '</div></div>');
    h.push('<nav aria-label="In questo numero" class="indice">');
    (p.movimenti || []).forEach(function (m, i) {
      h.push('<div><a href="#' + slugify(m.nome) + '"><b>' + ROMANI[i] + '</b><strong>' + esc(m.nome) + '</strong><span>' + esc(m.indice) + '</span></a></div>');
    });
    h.push('</nav></section>');
    // movimenti
    var n = 0;
    (p.movimenti || []).forEach(function (m, i) {
      h.push('<div class="mov" id="' + slugify(m.nome) + '"><b>' + ROMANI[i] + '</b><h2>' + esc(m.titolo || m.nome) + '</h2></div>');
      h.push('<section class="blocchi" style="--col:' + (m.colonne || m.blocchi.length) + '">');
      m.blocchi.forEach(function (b) {
        n += 1;
        h.push('<article class="blocco"><div class="n">' + (n < 10 ? '0' : '') + n + '</div>');
        if (b.tipo === 'domanda') h.push('<details class="faq-item" open><summary><h3>' + esc(b.titolo) + '</h3></summary><div class="testo">' + md(b.testo, opz) + '</div></details>');
        else h.push('<h3>' + esc(b.titolo) + '</h3><div class="testo">' + md(b.testo, opz) + '</div>');
        h.push('</article>');
      });
      h.push('</section>');
      m.dopo.forEach(function (d) {
        if (d.type === 'frase') {
          h.push('<section class="frase"><div class="rossa"><p class="grande">' + esc(d.grande).replace(/\n/g, '<br />\n') + '</p><hr class="filetto">');
          if (d.sotto) h.push('<div class="sotto">' + esc(d.sotto) + '</div>');
          h.push('</div>');
          if (d.image) {
            h.push('<figure class="foto-f' + (d.adatta ? ' intera' : '') + '"><img alt="' + esc(d.image_alt) + '" src="' + esc(img(d.image)) + '">');
            if (d.generata) h.push('<figcaption>' + GENERATA + '</figcaption>');
            else if (d.didascalia) h.push('<figcaption>' + mdRiga(d.didascalia, opz) + '</figcaption>');
            h.push('</figure>');
          }
          h.push('</section>');
        } else if (d.type === 'dati') {
          h.push('<section class="dato"><h2>' + esc(d.titolo) + '</h2><div class="tabella-scroll"><table>');
          if (d.didascalia) h.push('<caption>' + esc(d.didascalia) + '</caption>');
          h.push('<thead><tr><th scope="col">' + esc(d.colonna || 'Importo') + '</th><th scope="col">Che cosa misura</th><th scope="col">Fonte</th></tr></thead><tbody>');
          d.righe.forEach(function (r) {
            h.push('<tr><th scope="row"><span class="cifra">' + esc(r.cifra) + '</span><span class="unita">' + esc(r.unita) + '</span></th><td>' + mdRiga(r.testo, opz) + '</td><td><div class="fonte">' + mdRiga(r.fonte, opz) + '</div></td></tr>');
          });
          h.push('</tbody></table></div>');
          if (d.limite) h.push('<p class="limite">' + esc(d.limite) + '</p>');
          h.push('</section>');
        }
      });
    });
    // domande
    h.push('<section class="domande"><div class="et">Da portarsi a casa</div>');
    (p.domande || []).forEach(function (q, i) { h.push('<p class="' + (i ? 'q' : 'q1') + '">' + esc(q) + '</p>'); });
    if (p.articolo_origine && p.articolo_origine.url) h.push('<p class="dopo">Il ragionamento per intero: <a>' + esc(p.articolo_origine.titolo) + '</a></p>');
    h.push('</section></main></div>');
    return h.join('\n');
  }

  var api = { analizza: analizza, pagina: pagina };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; return; }
  radice.RDSAnteprima = api;

  /* ---------- l'aggancio a Sveltia ---------- */
  var CMS = radice.CMS;
  if (!CMS) return;
  var crea = radice.h || (CMS.React && CMS.React.createElement);
  if (!crea) return;
  var SITO = 'https://rossodiserablog.it';
  CMS.registerPreviewStyle('https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Arvo:wght@700&family=Gloock&family=Rock+Salt&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&display=swap');
  CMS.registerPreviewStyle(SITO + '/assets/css/numero.css');
  CMS.registerPreviewStyle('body{margin:0}.prova.anteprima{position:sticky;top:0;z-index:5}', { raw: true });

  function dati(entry) {
    if (!entry) return {};
    if (entry.toJS) { var j = entry.toJS(); return j.data || {}; }
    if (entry.getIn) { var d = entry.getIn(['data']); return d && d.toJS ? d.toJS() : (d || {}); }
    return entry.data || {};
  }

  function Anteprima(props) {
    var fm = dati(props.entry);
    var html = pagina(fm, {
      markdown: function (s) { return radice.marked ? radice.marked.parse(s) : '<p>' + esc(s) + '</p>'; },
      immagine: function (p) {
        try {
          var a = props.getAsset && props.getAsset(p);
          var u = a && (typeof a === 'string' ? a : (a.url || (a.toString && a.toString())));
          if (u && u !== '[object Object]') return u;
        } catch (e) { /* prende l'indirizzo del sito */ }
        return /^https?:/.test(p) ? p : SITO + p;
      }
    });
    return crea('div', { dangerouslySetInnerHTML: { __html: html } });
  }
  CMS.registerPreviewTemplate('numeri', Anteprima);
  CMS.registerPreviewTemplate('approfondimenti_usciti', Anteprima);
})(typeof window !== 'undefined' ? window : this);
