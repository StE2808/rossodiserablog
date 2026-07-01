/* Ricerca full-text client-side per Rosso di Sera (MiniSearch, self-hosted).
   Carica /search-index.json una volta, costruisce l'indice in-browser e cerca live.
   Nessun backend: gira interamente nel browser sulla pagina /cerca/. */
(function () {
  var input = document.getElementById('search-input');
  var resultsEl = document.getElementById('search-results');
  var statusEl = document.getElementById('search-status');
  if (!input || !resultsEl || typeof MiniSearch === 'undefined') return;

  var mini = null;
  var docsById = {};
  var ready = false;

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  // Snippet: ritaglia il testo attorno al primo termine trovato, evidenziandolo.
  function snippet(text, terms) {
    if (!text) return '';
    var lower = text.toLowerCase();
    var pos = -1;
    for (var i = 0; i < terms.length; i++) {
      var p = lower.indexOf(terms[i].toLowerCase());
      if (p !== -1 && (pos === -1 || p < pos)) pos = p;
    }
    var start = pos === -1 ? 0 : Math.max(0, pos - 60);
    var slice = text.slice(start, start + 200);
    if (start > 0) slice = '…' + slice;
    if (start + 200 < text.length) slice = slice + '…';
    slice = esc(slice);
    terms.forEach(function (t) {
      if (!t) return;
      var re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig');
      slice = slice.replace(re, '<mark>$1</mark>');
    });
    return slice;
  }

  var authors = { 'stefano-vozzi': 'Stefano Vozzi', 'lino-rialti': 'Lino Rialti' };

  function render(results, terms) {
    if (!results.length) {
      resultsEl.innerHTML = '';
      statusEl.textContent = 'Nessun risultato.';
      return;
    }
    statusEl.textContent = results.length + (results.length === 1 ? ' risultato' : ' risultati');
    var html = results.slice(0, 40).map(function (r) {
      var d = docsById[r.id];
      var author = authors[d.author] || '';
      var cat = d.category ? d.category.replace(/-/g, ' ') : '';
      var meta = [d.dateh, author, cat].filter(Boolean).join(' · ');
      return '<article class="search-result">' +
        '<h3 class="search-result-title"><a href="' + esc(d.url) + '">' + esc(d.title) + '</a></h3>' +
        '<div class="search-result-meta">' + esc(meta) + '</div>' +
        '<p class="search-result-snippet">' + snippet(d.content || d.excerpt, terms) + '</p>' +
        '</article>';
    }).join('');
    resultsEl.innerHTML = html;
  }

  function doSearch() {
    var q = input.value.trim();
    if (!ready) return;
    if (q.length < 2) { resultsEl.innerHTML = ''; statusEl.textContent = ''; return; }
    var results = mini.search(q, { prefix: true, fuzzy: 0.2, combineWith: 'AND' });
    if (!results.length) {
      // ripiego piu permissivo se AND non trova nulla
      results = mini.search(q, { prefix: true, fuzzy: 0.2, combineWith: 'OR' });
    }
    render(results, q.split(/\s+/).filter(Boolean));
  }

  var t = null;
  input.addEventListener('input', function () {
    clearTimeout(t);
    t = setTimeout(doSearch, 120);
  });

  statusEl.textContent = 'Caricamento indice…';
  fetch(input.getAttribute('data-index'))
    .then(function (r) { return r.json(); })
    .then(function (docs) {
      docs.forEach(function (d) { docsById[d.id] = d; });
      mini = new MiniSearch({
        fields: ['title', 'tags', 'category', 'excerpt', 'content'],
        storeFields: ['id'],
        searchOptions: {
          boost: { title: 4, tags: 2, excerpt: 1.5 },
          prefix: true,
          fuzzy: 0.2
        }
      });
      mini.addAll(docs);
      ready = true;
      statusEl.textContent = '';
      input.disabled = false;
      // supporto ?q= per link diretti e ricerca da altre pagine
      var params = new URLSearchParams(window.location.search);
      var pre = params.get('q');
      if (pre) { input.value = pre; }
      if (input.value.trim()) doSearch();
      input.focus();
    })
    .catch(function () {
      statusEl.textContent = 'Impossibile caricare l\'indice di ricerca. Riprova piu tardi.';
    });
})();
