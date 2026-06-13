(function () {
  var WORKER = 'https://rossodisera-commenti.s-vozzi.workers.dev';
  var SITEKEY = '0x4AAAAAADkHTaUCiljuvtPi';
  var root = document.getElementById('rds-comments');
  if (!root) return;
  var POST = location.pathname;
  var voter = localStorage.getItem('rds_voter');
  if (!voter) { voter = Math.random().toString(36).slice(2) + Date.now().toString(36); localStorage.setItem('rds_voter', voter); }
  var modToken = (location.hash.match(/mod=([^&]+)/) || [])[1];
  var EMOJIS = ['👍', '❤️', '😄', '🎉'];

  function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
  function api(path, opts) { return fetch(WORKER + path, opts).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, status: r.status, data: j }; }); }); }

  function renderReactions(list) {
    var bar = root.querySelector('.rds-reactions'); bar.innerHTML = '';
    EMOJIS.forEach(function (e) {
      var info = list.find(function (x) { return x.emoji === e; }) || { n: 0, mine: 0 };
      var b = document.createElement('button');
      b.className = 'rds-react' + (info.mine ? ' mine' : '');
      b.innerHTML = e + ' <span>' + info.n + '</span>';
      b.onclick = function () {
        api('/react', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ post: POST, emoji: e, voter_token: voter }) })
          .then(loadReactions);
      };
      bar.appendChild(b);
    });
  }
  function loadReactions() { api('/reactions?post=' + encodeURIComponent(POST) + '&voter=' + voter).then(function (r) { renderReactions(r.data.reactions || []); }); }

  function buildTree(items) {
    var byId = {}, roots = [];
    items.forEach(function (c) { c.children = []; byId[c.id] = c; });
    items.forEach(function (c) { (c.parent_id && byId[c.parent_id] ? byId[c.parent_id].children : roots).push(c); });
    return roots;
  }
  function renderComment(c) {
    var el = document.createElement('div'); el.className = 'rds-comment';
    var d = new Date(c.created_at).toLocaleDateString('it-IT');
    el.innerHTML = '<div class="rds-meta"><strong>' + esc(c.author) + '</strong> · ' + d +
      (modToken ? ' <button class="rds-del" data-id="' + c.id + '">elimina</button>' : '') +
      '</div><div class="rds-body">' + esc(c.body).replace(/\n/g, '<br>') + '</div>' +
      '<button class="rds-reply" data-id="' + c.id + '">Rispondi</button>';
    var kids = document.createElement('div'); kids.className = 'rds-children';
    c.children.forEach(function (ch) { kids.appendChild(renderComment(ch)); });
    el.appendChild(kids);
    return el;
  }
  function loadComments() {
    api('/comments?post=' + encodeURIComponent(POST)).then(function (r) {
      var list = root.querySelector('.rds-list'); list.innerHTML = '';
      var tree = buildTree(r.data.comments || []);
      if (!tree.length) list.innerHTML = '<p class="rds-empty">Nessun commento. Scrivi il primo!</p>';
      tree.forEach(function (c) { list.appendChild(renderComment(c)); });
    });
  }

  function showForm(parentId, mountEl) {
    var f = document.createElement('form'); f.className = 'rds-form';
    f.innerHTML =
      '<input class="rds-name" type="text" placeholder="Il tuo nome" maxlength="50" required>' +
      '<textarea class="rds-text" placeholder="Scrivi un commento…" maxlength="2000" required></textarea>' +
      '<input type="text" class="rds-hp" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px">' +
      '<div class="cf-turnstile" data-sitekey="' + SITEKEY + '"></div>' +
      '<button type="submit">Invia</button>' +
      '<p class="rds-note">Nessun account richiesto. Salviamo nome e testo; nessun tracciamento pubblicitario.</p>';
    f.onsubmit = function (ev) {
      ev.preventDefault();
      var btn = f.querySelector('button[type=submit]');
      var token = (f.querySelector('[name="cf-turnstile-response"]') || {}).value || '';
      btn.disabled = true;
      api('/comments', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ post: POST, parent_id: parentId || null, author: f.querySelector('.rds-name').value, body: f.querySelector('.rds-text').value, hp: f.querySelector('.rds-hp').value, turnstileToken: token })
      }).then(function (r) {
        btn.disabled = false;
        if (r.ok) { loadComments(); if (parentId) mountEl.innerHTML = ''; else { f.reset(); if (window.turnstile) window.turnstile.reset(f.querySelector('.cf-turnstile')); } }
        else alert(r.data.error || 'Errore, riprova.');
      });
    };
    mountEl.appendChild(f);
    if (window.turnstile) window.turnstile.render(f.querySelector('.cf-turnstile'));
  }

  root.querySelector('.rds-list').addEventListener('click', function (ev) {
    var id = ev.target.getAttribute('data-id');
    if (ev.target.classList.contains('rds-reply')) {
      var parent = ev.target.parentElement;
      var holder = parent.querySelector('.rds-reply-form');
      if (!holder) { holder = document.createElement('div'); holder.className = 'rds-reply-form'; parent.insertBefore(holder, ev.target.nextSibling); }
      if (!holder.children.length) showForm(Number(id), holder); else holder.innerHTML = '';
    }
    if (ev.target.classList.contains('rds-del')) {
      api('/comments/' + id, { method: 'DELETE', headers: { Authorization: 'Bearer ' + modToken } }).then(loadComments);
    }
  });

  loadReactions();
  loadComments();
  showForm(null, root.querySelector('.rds-newform'));
})();
