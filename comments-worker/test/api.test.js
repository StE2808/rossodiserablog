import { env, createExecutionContext, waitOnExecutionContext } from 'cloudflare:test';
import { beforeAll, describe, it, expect } from 'vitest';
import worker from '../src/index.js';

const ORIGIN = 'https://rossodiserablog.it';
const POST = '/articolo-test/';

// Schema inline: nel runtime Workers non c'è fs per leggere schema.sql.
// Tenere allineato con ../schema.sql.
const SCHEMA = [
  "CREATE TABLE IF NOT EXISTS comments(id INTEGER PRIMARY KEY AUTOINCREMENT, post TEXT NOT NULL, parent_id INTEGER, author TEXT NOT NULL, body TEXT NOT NULL, created_at INTEGER NOT NULL, status TEXT NOT NULL DEFAULT 'visible', ip_hash TEXT)",
  "CREATE INDEX IF NOT EXISTS idx_comments_post ON comments(post, status, created_at)",
  "CREATE INDEX IF NOT EXISTS idx_comments_ip ON comments(ip_hash, created_at)",
  "CREATE TABLE IF NOT EXISTS reactions(post TEXT NOT NULL, emoji TEXT NOT NULL, voter_token TEXT NOT NULL, created_at INTEGER NOT NULL)",
  "CREATE UNIQUE INDEX IF NOT EXISTS idx_reactions_uniq ON reactions(post, emoji, voter_token)",
];

beforeAll(async () => {
  for (const stmt of SCHEMA) {
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
