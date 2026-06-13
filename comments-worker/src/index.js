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
