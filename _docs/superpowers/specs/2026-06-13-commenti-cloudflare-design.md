# Sistema commenti + reazioni self-hosted (Cloudflare) — Design

**Data**: 2026-06-13
**Stato**: approvato da Stefano (brainstorming)
**Sostituisce**: Giscus (commenti via GitHub Discussions, richiede login GitHub)

## Obiettivo

Permettere a lettori **senza account** di commentare e reagire sotto gli articoli, mantenendo il blog dov'è (GitHub Pages + Cloudflare). Costo zero, niente pubblicità né tracciamento (coerente coi valori del blog), gestito su infrastruttura già nostra (Cloudflare).

## Decisioni prese (brainstorming 2026-06-13)

- **Stack**: Cloudflare Worker (API) + Cloudflare D1 (SQLite) + Turnstile (anti-bot). Tutto su free tier.
- **Login**: nessuno. Il lettore inserisce solo un nome + testo.
- **v1 include**: commenti **con risposte** (thread annidati) + **reazioni** a livello articolo (emoji con conteggi).
- **Apparizione**: commenti **visibili subito** (post-moderazione). Avvertenza accettata: è la config più esposta allo spam; mitigata con Turnstile + rate-limit + honeypot + cancellazione rapida. Se lo spam diventa fastidioso → interruttore verso pre-moderazione.
- **Il blog resta su GitHub**: cambia solo il "motore" dei commenti (da Giscus al nostro Worker).

## Architettura

```
articolo (GitHub Pages) ──fetch/POST──► Cloudflare Worker (API) ──► Cloudflare D1
  assets/js/comments.js                  verifica Turnstile,         comments, reactions
  blocco in _layouts/post.html           rate-limit, honeypot, CORS
```

- **Worker** su URL `*.workers.dev` (niente DNS in v1; CORS ristretto all'origine `https://rossodiserablog.it`). Sottodominio dedicato `commenti.rossodiserablog.it` rinviato a dopo.

## Modello dati (D1)

**comments**
| campo | tipo | note |
|-------|------|------|
| id | INTEGER PK | |
| post | TEXT | path articolo (es. `/titolo-articolo/`) |
| parent_id | INTEGER NULL | per le risposte annidate |
| author | TEXT | nome (max 50) |
| body | TEXT | testo (max 2000) |
| created_at | INTEGER | epoch ms |
| status | TEXT | `visible` \| `hidden` (default visible) |
| ip_hash | TEXT | sha256(ip + salt); solo anti-abuso, mai mostrato |

**reactions**
| campo | tipo | note |
|-------|------|------|
| post | TEXT | path articolo |
| emoji | TEXT | es. 👍 ❤️ 😄 🎉 |
| voter_token | TEXT | id anonimo casuale salvato in localStorage |
| created_at | INTEGER | |

UNIQUE(post, emoji, voter_token) → un like per emoji per visitatore (toggle). Conteggi via `GROUP BY emoji`.

## API (Worker)

- `GET /comments?post=<path>` → lista commenti `visible` dell'articolo (per costruire i thread lato client).
- `POST /comments` `{post, parent_id?, author, body, turnstileToken, hp}` → valida Turnstile, honeypot (`hp` deve essere vuoto), rate-limit per `ip_hash`, lunghezze; inserisce `visible`; ritorna il commento.
- `GET /reactions?post=<path>` → conteggi per emoji + quali ha messo il `voter_token`.
- `POST /react` `{post, emoji, voter_token}` → toggle reazione.
- `DELETE /comments/:id` (header `Authorization: Bearer <ADMIN_TOKEN>`) → imposta `hidden`.

Anti-spam: Turnstile server-side, honeypot, rate-limit (max ~5 commenti/ora per ip_hash via D1), max lunghezza, niente HTML nel body (escape lato render).

## Frontend

- `assets/js/comments.js`: legge il `post` dal path, carica reazioni + commenti, rende la barra emoji (conteggi, stato attivo) e la lista a thread con pulsante "Rispondi", form (nome + testo + Turnstile invisibile + honeypot nascosto), nota privacy breve. Niente cookie di tracciamento; solo un `voter_token` random in localStorage per le reazioni.
- `_layouts/post.html`: sostituire il blocco Giscus (righe ~106-133) con il contenitore `#commenti` + `<script>` del widget + script Turnstile. Mantenere il titolo "Commenti".
- **Moderazione**: aprendo l'articolo con `#mod=<ADMIN_TOKEN>` il widget mostra un pulsante "elimina" accanto a ogni commento (chiama `DELETE` con il bearer). Nessuna pagina extra in v1.

## Privacy / GDPR

Si salvano: nome, testo, data, hash dell'IP (anti-abuso). Nessuna profilazione, nessun cookie pubblicitario. Turnstile è privacy-friendly. Riga di nota sotto al form. Path di cancellazione su richiesta: eliminare la riga in D1.

## Deploy live — prerequisiti

- **Token Cloudflare** (custom API token) con scope: *Account → Workers Scripts: Edit*, *Account → D1: Edit*, *Account → Turnstile: Edit*, *Account → Account Settings: Read*. (Niente DNS/Zone in v1.)
- **Turnstile**: creare un widget per il dominio → site key (pubblica, va nel JS) + secret key (segreto, va nel Worker). Creabile via API col token sopra, oppure a mano dal dashboard.
- **ADMIN_TOKEN**: stringa segreta scelta da Stefano, salvata come secret del Worker.
- Le chiavi/segreti vanno in `~/.secrets/credentials.yaml`, mai nel repo.

## Fuori scope v1 (eventuale futuro)

- Notifiche email a nuovo commento (es. Resend free tier).
- Sottodominio dedicato `commenti.rossodiserablog.it`.
- Reazioni sui singoli commenti (v1: solo a livello articolo).
- Migrazione dei vecchi commenti da GitHub Discussions (oggi pochi/nulli).

## Test / verifica

1. In locale (`wrangler dev` + D1 locale): GET vuoto, POST commento → appare; risposta annidata; reazione toggle; rate-limit oltre soglia; honeypot pieno → rifiutato; Turnstile mancante → rifiutato.
2. `DELETE` con token giusto nasconde, con token errato 401.
3. CORS: richieste da origine diversa rifiutate.
4. In pagina: il widget rende thread e reazioni, niente errori console; Giscus rimosso; cache-busting `?v=` sul nuovo JS.
