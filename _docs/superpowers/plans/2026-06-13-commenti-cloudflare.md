# Sistema commenti + reazioni (Cloudflare) — Piano di implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (consigliato) o superpowers:executing-plans per eseguire task per task. Gli step usano checkbox (`- [ ]`).

**Goal:** Sostituire Giscus con un sistema commenti+reazioni senza login, gratis, su Cloudflare Worker + D1, mantenendo il blog su GitHub Pages.

**Architecture:** Worker (`*.workers.dev`) espone una piccola API JSON; i dati stanno in D1 (SQLite). Un widget JS nella pagina articolo legge/scrive via fetch. Anti-spam con Turnstile + honeypot + rate-limit. Moderazione post-pubblicazione via token admin.

**Tech Stack:** Cloudflare Workers, D1, Turnstile, wrangler, vanilla JS. Riferimento: spec `_docs/superpowers/specs/2026-06-13-commenti-cloudflare-design.md`.

---

## File Structure

- `comments-worker/wrangler.toml` — config Worker + binding D1.
- `comments-worker/package.json` — dipendenze dev (wrangler, vitest, @cloudflare/vitest-pool-workers).
- `comments-worker/schema.sql` — schema D1 (tabelle comments, reactions).
- `comments-worker/src/index.js` — l'intera API (routing, CORS, validazione, Turnstile, rate-limit).
- `comments-worker/test/api.test.js` — test degli endpoint (vitest-pool-workers, D1 locale).
- `assets/js/comments.js` — widget: carica e rende thread + reazioni, form, Turnstile, modalità mod.
- `assets/css/style.css` — append: stili `.rds-comments` (sezione nuova).
- `_layouts/post.html:106-133` — sostituire blocco Giscus col contenitore widget.
- `_config.yml` — aggiungere `comments-worker/` a `exclude` (fuori dal build Jekyll).

Nota: `comments-worker/` vive nel repo del blog ma è escluso dal build; è versionato insieme al blog. Segreti (Turnstile secret, ADMIN_TOKEN, IP_SALT) NON nel repo: vanno come secret del Worker e copia in `~/.secrets/credentials.yaml`.

---

## Task 1: Scaffold del Worker e schema D1

**Files:**
- Create: `comments-worker/wrangler.toml`
- Create: `comments-worker/package.json`
- Create: `comments-worker/schema.sql`
- Modify: `_config.yml` (sezione `exclude`)

- [ ] **Step 1: `wrangler.toml`**

```toml
name = "rossodisera-commenti"
main = "src/index.js"
compatibility_date = "2026-06-01"

[[d1_databases]]
binding = "DB"
database_name = "rossodisera-commenti"
database_id = "DA_RIEMPIRE_DOPO_D1_CREATE"
```

- [ ] **Step 2: `package.json`**

```json
{
  "name": "rossodisera-commenti",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "wrangler dev",
    "test": "vitest run",
    "deploy": "wrangler deploy"
  },
  "devDependencies": {
    "wrangler": "^3.80.0",
    "vitest": "^2.0.0",
    "@cloudflare/vitest-pool-workers": "^0.5.0"
  }
}
```

- [ ] **Step 3: `schema.sql`**

```sql
CREATE TABLE IF NOT EXISTS comments(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post TEXT NOT NULL,
  parent_id INTEGER,
  author TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'visible',
  ip_hash TEXT
);
CREATE INDEX IF NOT EXISTS idx_comments_post ON comments(post, status, created_at);
CREATE INDEX IF NOT EXISTS idx_comments_ip ON comments(ip_hash, created_at);

CREATE TABLE IF NOT EXISTS reactions(
  post TEXT NOT NULL,
  emoji TEXT NOT NULL,
  voter_token TEXT NOT NULL,
  created_at INTEGER NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_reactions_uniq ON reactions(post, emoji, voter_token);
```

- [ ] **Step 4: aggiungere `comments-worker/` all'`exclude` di `_config.yml`**

Trovare la chiave `exclude:` e aggiungere la voce `- comments-worker/` insieme alle altre (es. accanto a `_dev/`, `_docs/`).

- [ ] **Step 5: Commit**

```bash
git add comments-worker/wrangler.toml comments-worker/package.json comments-worker/schema.sql _config.yml
git commit -m "Scaffold worker commenti + schema D1"
```

---

## Task 2: API del Worker (codice completo)

**Files:**
- Create: `comments-worker/src/index.js`

- [ ] **Step 1: scrivere `src/index.js`**

```js
const ALLOWED_ORIGIN = 'https://rossodiserablog.it';
const RATE_LIMIT = 5;            // commenti per finestra
const RATE_WINDOW_MS = 3600000;  // 1 ora
const MAX_NAME = 50, MAX_BODY = 2000;
const EMOJIS = ['👍', '❤️', '😄', '🎉'];

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin === ALLOWED_ORIGIN ? ALLOWED_ORIGIN : '',
    'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
  };
}
function json(data, status, headers) {
  return new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json', ...headers } });
}
async function sha256(s) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}
async function verifyTurnstile(token, ip, secret) {
  const form = new FormData();
  form.append('secret', secret);
  form.append('response', token || '');
  if (ip) form.append('remoteip', ip);
  const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
  const d = await r.json();
  return d.success === true;
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const origin = req.headers.get('Origin') || '';
    const ch = corsHeaders(origin);
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: ch });
    if (origin && origin !== ALLOWED_ORIGIN) return json({ error: 'forbidden' }, 403, ch);

    const ip = req.headers.get('CF-Connecting-IP') || '';
    const ipHash = await sha256(ip + (env.IP_SALT || ''));

    try {
      // LISTA COMMENTI
      if (url.pathname === '/comments' && req.method === 'GET') {
        const post = url.searchParams.get('post') || '';
        const { results } = await env.DB.prepare(
          "SELECT id, parent_id, author, body, created_at FROM comments WHERE post=? AND status='visible' ORDER BY created_at ASC"
        ).bind(post).all();
        return json({ comments: results }, 200, ch);
      }

      // NUOVO COMMENTO
      if (url.pathname === '/comments' && req.method === 'POST') {
        const b = await req.json();
        if (b.hp) return json({ ok: true }, 200, ch); // honeypot pieno: finto successo
        const author = (b.author || '').trim().slice(0, MAX_NAME);
        const body = (b.body || '').trim().slice(0, MAX_BODY);
        const post = (b.post || '').slice(0, 300);
        if (!author || !body || !post) return json({ error: 'campi mancanti' }, 400, ch);
        if (!(await verifyTurnstile(b.turnstileToken, ip, env.TURNSTILE_SECRET)))
          return json({ error: 'verifica anti-spam fallita' }, 403, ch);
        const since = Date.now() - RATE_WINDOW_MS;
        const rl = await env.DB.prepare('SELECT COUNT(*) AS n FROM comments WHERE ip_hash=? AND created_at>?').bind(ipHash, since).all();
        if (rl.results[0].n >= RATE_LIMIT) return json({ error: 'troppi commenti, riprova più tardi' }, 429, ch);
        const now = Date.now();
        const parent = b.parent_id ? Number(b.parent_id) : null;
        const res = await env.DB.prepare(
          "INSERT INTO comments(post,parent_id,author,body,created_at,status,ip_hash) VALUES(?,?,?,?,?,'visible',?)"
        ).bind(post, parent, author, body, now, ipHash).run();
        return json({ comment: { id: res.meta.last_row_id, parent_id: parent, author, body, created_at: now } }, 201, ch);
      }

      // CONTEGGI REAZIONI
      if (url.pathname === '/reactions' && req.method === 'GET') {
        const post = url.searchParams.get('post') || '';
        const voter = url.searchParams.get('voter') || '';
        const { results } = await env.DB.prepare(
          'SELECT emoji, COUNT(*) AS n, MAX(CASE WHEN voter_token=? THEN 1 ELSE 0 END) AS mine FROM reactions WHERE post=? GROUP BY emoji'
        ).bind(voter, post).all();
        return json({ reactions: results }, 200, ch);
      }

      // TOGGLE REAZIONE
      if (url.pathname === '/react' && req.method === 'POST') {
        const b = await req.json();
        const post = (b.post || '').slice(0, 300);
        const emoji = b.emoji;
        const voter = (b.voter_token || '').slice(0, 64);
        if (!EMOJIS.includes(emoji) || !post || !voter) return json({ error: 'dati non validi' }, 400, ch);
        const ex = await env.DB.prepare('SELECT rowid FROM reactions WHERE post=? AND emoji=? AND voter_token=?').bind(post, emoji, voter).all();
        if (ex.results.length) {
          await env.DB.prepare('DELETE FROM reactions WHERE post=? AND emoji=? AND voter_token=?').bind(post, emoji, voter).run();
        } else {
          await env.DB.prepare('INSERT INTO reactions(post,emoji,voter_token,created_at) VALUES(?,?,?,?)').bind(post, emoji, voter, Date.now()).run();
        }
        return json({ ok: true }, 200, ch);
      }

      // CANCELLA (MODERAZIONE)
      const del = url.pathname.match(/^\/comments\/(\d+)$/);
      if (del && req.method === 'DELETE') {
        const auth = req.headers.get('Authorization') || '';
        if (auth !== 'Bearer ' + env.ADMIN_TOKEN) return json({ error: 'unauthorized' }, 401, ch);
        await env.DB.prepare("UPDATE comments SET status='hidden' WHERE id=?").bind(Number(del[1])).run();
        return json({ ok: true }, 200, ch);
      }

      return json({ error: 'not found' }, 404, ch);
    } catch (e) {
      return json({ error: 'server' }, 500, ch);
    }
  }
};
```

- [ ] **Step 2: Commit**

```bash
git add comments-worker/src/index.js
git commit -m "API Worker commenti: comments, reactions, react, delete"
```

---

## Task 3: Test degli endpoint (TDD sul comportamento)

**Files:**
- Create: `comments-worker/test/api.test.js`
- Create: `comments-worker/vitest.config.js`

- [ ] **Step 1: `vitest.config.js`**

```js
import { defineWorkersConfig } from '@cloudflare/vitest-pool-workers/config';
export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: './wrangler.toml' },
        miniflare: { d1Databases: { DB: 'test-db' }, bindings: { TURNSTILE_SECRET: '1x0000000000000000000000000000000AA', ADMIN_TOKEN: 'testadmin', IP_SALT: 's' } },
      },
    },
  },
});
```

Nota: `1x0000...AA` è la **secret key di test Turnstile** che restituisce sempre success.

- [ ] **Step 2: scrivere i test (devono fallire: niente schema applicato ancora nel test env)**

```js
import { env, createExecutionContext, waitOnExecutionContext } from 'cloudflare:test';
import { beforeAll, describe, it, expect } from 'vitest';
import worker from '../src/index.js';
import { readFileSync } from 'node:fs';

const ORIGIN = 'https://rossodiserablog.it';
const POST = '/articolo-test/';

beforeAll(async () => {
  const schema = readFileSync(new URL('../schema.sql', import.meta.url), 'utf8');
  for (const stmt of schema.split(';').map(s => s.trim()).filter(Boolean)) {
    await env.DB.prepare(stmt).run();
  }
});

async function call(method, path, body, headers = {}) {
  const req = new Request('https://w.dev' + path, {
    method,
    headers: { Origin: ORIGIN, 'Content-Type': 'application/json', ...headers },
    body: body ? JSON.stringify(body) : undefined,
  });
  const ctx = createExecutionContext();
  const res = await worker.fetch(req, env, ctx);
  await waitOnExecutionContext(ctx);
  return res;
}

describe('commenti', () => {
  it('lista vuota all’inizio', async () => {
    const res = await call('GET', '/comments?post=' + POST);
    expect(res.status).toBe(200);
    expect((await res.json()).comments).toEqual([]);
  });

  it('crea un commento e lo rilegge', async () => {
    const r = await call('POST', '/comments', { post: POST, author: 'Mario', body: 'Ciao', turnstileToken: 'x' });
    expect(r.status).toBe(201);
    const list = await (await call('GET', '/comments?post=' + POST)).json();
    expect(list.comments.length).toBe(1);
    expect(list.comments[0].author).toBe('Mario');
  });

  it('rifiuta honeypot pieno senza salvare', async () => {
    const before = (await (await call('GET', '/comments?post=' + POST)).json()).comments.length;
    const r = await call('POST', '/comments', { post: POST, author: 'Bot', body: 'spam', hp: 'x', turnstileToken: 'x' });
    expect(r.status).toBe(200);
    const after = (await (await call('GET', '/comments?post=' + POST)).json()).comments.length;
    expect(after).toBe(before);
  });

  it('blocca origine non consentita', async () => {
    const req = new Request('https://w.dev/comments?post=' + POST, { headers: { Origin: 'https://evil.com' } });
    const ctx = createExecutionContext();
    const res = await worker.fetch(req, env, ctx);
    await waitOnExecutionContext(ctx);
    expect(res.status).toBe(403);
  });

  it('DELETE richiede token admin', async () => {
    const noauth = await call('DELETE', '/comments/1');
    expect(noauth.status).toBe(401);
    const ok = await call('DELETE', '/comments/1', null, { Authorization: 'Bearer testadmin' });
    expect(ok.status).toBe(200);
  });
});

describe('reazioni', () => {
  it('toggle aggiunge e rimuove', async () => {
    await call('POST', '/react', { post: POST, emoji: '👍', voter_token: 'v1' });
    let r = await (await call('GET', '/reactions?post=' + POST + '&voter=v1')).json();
    expect(r.reactions.find(x => x.emoji === '👍').n).toBe(1);
    await call('POST', '/react', { post: POST, emoji: '👍', voter_token: 'v1' });
    r = await (await call('GET', '/reactions?post=' + POST + '&voter=v1')).json();
    expect(r.reactions.find(x => x.emoji === '👍')?.n || 0).toBe(0);
  });
});
```

- [ ] **Step 3: installare ed eseguire**

```bash
cd comments-worker && npm install && npm test
```
Expected: tutti i test PASS (Turnstile usa la test key che ritorna sempre success).

- [ ] **Step 4: Commit**

```bash
git add comments-worker/test/api.test.js comments-worker/vitest.config.js comments-worker/package-lock.json
git commit -m "Test endpoint commenti e reazioni (vitest-pool-workers)"
```

---

## Task 4: Deploy live su Cloudflare

Prerequisito: in `~/.secrets/credentials.yaml` esiste `cloudflare.commenti_deploy_token` con scope Workers Scripts/D1/Turnstile/Account Settings (vedi spec). Esportare per wrangler:

- [ ] **Step 1: esportare il token e creare il D1**

```bash
export CLOUDFLARE_API_TOKEN="$(python3 -c "import yaml;print(yaml.safe_load(open('$HOME/.secrets/credentials.yaml'))['cloudflare']['commenti_deploy_token'])")"
cd comments-worker
npx wrangler d1 create rossodisera-commenti
```
Copiare il `database_id` restituito dentro `wrangler.toml` (campo `database_id`).

- [ ] **Step 2: applicare lo schema al D1 remoto**

```bash
npx wrangler d1 execute rossodisera-commenti --remote --file ./schema.sql
```

- [ ] **Step 3: creare il widget Turnstile** (via dashboard o API). Annotare **site key** (pubblica) e **secret key**. Salvare entrambe in `~/.secrets/credentials.yaml` sotto `cloudflare.turnstile_commenti` (site_key, secret_key).

- [ ] **Step 4: impostare i secret del Worker**

```bash
echo "<TURNSTILE_SECRET>" | npx wrangler secret put TURNSTILE_SECRET
echo "<ADMIN_TOKEN scelto da Stefano>" | npx wrangler secret put ADMIN_TOKEN
echo "<stringa casuale>" | npx wrangler secret put IP_SALT
```

- [ ] **Step 5: deploy e smoke test**

```bash
npx wrangler deploy
# annotare l'URL *.workers.dev restituito, es. https://rossodisera-commenti.<acct>.workers.dev
curl -s "https://<URL>/comments?post=/test/" -H "Origin: https://rossodiserablog.it"
```
Expected: `{"comments":[]}`.

- [ ] **Step 6: salvare l'URL del Worker** in `~/.secrets/credentials.yaml` (`cloudflare.commenti_worker_url`) e committare `wrangler.toml` aggiornato col `database_id`.

```bash
git add comments-worker/wrangler.toml
git commit -m "Configura database_id D1 commenti"
```

---

## Task 5: Widget frontend

**Files:**
- Create: `assets/js/comments.js`
- Modify: `assets/css/style.css` (append sezione `.rds-comments`)

- [ ] **Step 1: `assets/js/comments.js`** (sostituire `WORKER_URL` e `TURNSTILE_SITEKEY` coi valori reali del deploy; SITEKEY è pubblica)

```js
(function () {
  var WORKER = 'https://REPLACE.workers.dev';
  var SITEKEY = 'REPLACE_TURNSTILE_SITEKEY';
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
      '<button type="submit">Invia</button><p class="rds-note">Nessun account richiesto. Salviamo nome e testo; nessun tracciamento pubblicitario.</p>';
    f.onsubmit = function (ev) {
      ev.preventDefault();
      var token = (f.querySelector('[name="cf-turnstile-response"]') || {}).value || '';
      api('/comments', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ post: POST, parent_id: parentId || null, author: f.querySelector('.rds-name').value, body: f.querySelector('.rds-text').value, hp: f.querySelector('.rds-hp').value, turnstileToken: token })
      }).then(function (r) {
        if (r.ok) { loadComments(); if (parentId) mountEl.innerHTML = ''; else f.reset(); }
        else alert(r.data.error || 'Errore'); 
      });
    };
    mountEl.appendChild(f);
    if (window.turnstile) window.turnstile.render(f.querySelector('.cf-turnstile'));
  }

  root.querySelector('.rds-list').addEventListener('click', function (ev) {
    var id = ev.target.getAttribute('data-id');
    if (ev.target.classList.contains('rds-reply')) {
      var holder = ev.target.parentElement.querySelector('.rds-reply-form') || (function () { var d = document.createElement('div'); d.className = 'rds-reply-form'; ev.target.parentElement.insertBefore(d, ev.target.nextSibling); return d; })();
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
```

- [ ] **Step 2: stili in `assets/css/style.css`** (append in fondo)

```css
/* Commenti (sistema self-hosted Cloudflare) */
.rds-comments { margin-top: 2rem; }
.rds-reactions { display: flex; gap: .5rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.rds-react { border: 1px solid var(--ombra, #ccc); background: transparent; border-radius: 999px; padding: .3rem .8rem; cursor: pointer; font-size: 1rem; }
.rds-react.mine { background: rgba(139,26,26,.1); border-color: var(--rosso-primario, #8b1a1a); }
.rds-comment { padding: .8rem 0; border-top: 1px solid rgba(0,0,0,.08); }
.rds-meta { font-size: .85rem; color: #666; margin-bottom: .3rem; }
.rds-body { line-height: 1.6; }
.rds-children { margin-left: 1.5rem; border-left: 2px solid rgba(0,0,0,.06); padding-left: 1rem; }
.rds-reply, .rds-del { background: none; border: none; color: var(--rosso-primario, #8b1a1a); cursor: pointer; font-size: .8rem; padding: .2rem 0; }
.rds-form { display: flex; flex-direction: column; gap: .6rem; margin: 1rem 0; }
.rds-form input, .rds-form textarea { padding: .6rem; border: 1px solid #ccc; border-radius: 6px; font: inherit; }
.rds-form textarea { min-height: 90px; resize: vertical; }
.rds-form button[type=submit] { align-self: flex-start; background: var(--rosso-primario, #8b1a1a); color: #fff; border: none; border-radius: 6px; padding: .5rem 1.2rem; cursor: pointer; }
.rds-note { font-size: .75rem; color: #888; }
.rds-empty { color: #888; }
```

- [ ] **Step 3: Commit**

```bash
git add assets/js/comments.js assets/css/style.css
git commit -m "Widget commenti + reazioni (frontend)"
```

---

## Task 6: Sostituire Giscus in post.html

**Files:**
- Modify: `_layouts/post.html:106-133`

- [ ] **Step 1: rimpiazzare il blocco `<section class="post-comments">` (lo script salva-titolo + i due `<script>` Giscus) con:**

```html
    <!-- Sezione Commenti (self-hosted Cloudflare) -->
    <section class="post-comments rds-comments">
        <h3 class="comments-title">Commenti</h3>
        <div id="rds-comments">
            <div class="rds-reactions"></div>
            <div class="rds-newform"></div>
            <div class="rds-list"></div>
        </div>
        <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
        <script src="{{ '/assets/js/comments.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
    </section>
```

- [ ] **Step 2: verifica build locale o deploy**: la pagina articolo mostra reazioni + form + lista, nessun riferimento a giscus.app.

```bash
grep -c giscus _layouts/post.html   # atteso 0
```

- [ ] **Step 3: Commit**

```bash
git add _layouts/post.html
git commit -m "Sostituisci Giscus col widget commenti self-hosted"
```

---

## Task 7: Verifica end-to-end in produzione

- [ ] Aprire un articolo sul sito (hard refresh). Verificare: barra reazioni con conteggi; click su un'emoji incrementa/decrementa (toggle); scrivere un commento (Turnstile compare) → appare nella lista; "Rispondi" crea un thread annidato.
- [ ] Test moderazione: aprire l'articolo con `#mod=<ADMIN_TOKEN>` → compaiono i pulsanti "elimina"; eliminare un commento di prova → sparisce dopo reload.
- [ ] Test anti-spam: una POST senza token Turnstile (via curl) → 403; oltre 5 commenti/ora dallo stesso IP → 429.
- [ ] Console del browser senza errori.

---

## Self-Review (fatto)

- **Copertura spec**: D1 (T1), API comments/reactions/react/delete (T2), anti-spam Turnstile+honeypot+rate-limit (T2), test (T3), deploy+Turnstile+secret (T4), widget thread+reazioni+nota privacy+mod (T5), sostituzione Giscus (T6), verifica (T7). Tutto coperto.
- **Placeholder**: i soli segnaposto sono valori che si conoscono solo a deploy fatto (`database_id`, `WORKER` url, `SITEKEY`, `ADMIN_TOKEN`), esplicitamente marcati `REPLACE`/`DA_RIEMPIRE`.
- **Coerenza tipi/nomi**: binding `DB`, campi tabella, nomi endpoint e classi CSS (`.rds-*`) coerenti tra Worker, test, widget e post.html.
