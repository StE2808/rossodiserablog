# Report Implementazione CMS + SEO - Rosso di Sera

Data inizio: 19 Dicembre 2024
Data ultimo aggiornamento: 19 Dicembre 2025

## Stato: COMPLETATO E FUNZIONANTE ✅

### Checklist
- [x] Step 0: Setup iniziale
- [x] Step 1: Creazione admin/index.html
- [x] Step 2: Creazione admin/config.yml
- [x] Step 3: Cartella uploads
- [x] Step 4: Meta SEO in default.html
- [x] Step 5: Schema.org in post.html
- [x] Step 6: robots.txt
- [x] Step 7: Commit e push finale
- [x] Step 8: Migrazione a GitHub OAuth (tentativo con Netlify - fallito per limiti)
- [x] Step 9: Verifica admin/index.html
- [x] Step 10: Migrazione a Sveltia CMS
- [x] Step 11: Configurazione Cloudflare Workers OAuth (risolto!)
- [x] Step 12: Primo articolo pubblicato dal CMS

---

## Log attività

### Step 0 - Setup iniziale
- Clonata repository
- Creato questo file report
- Prossimo: Step 1

### Step 1 - admin/index.html
- Creata cartella admin/
- Creato file admin/index.html con Decap CMS e Netlify Identity
- Prossimo: Step 2

### Step 2 - admin/config.yml
- Creato file admin/config.yml
- Configurati campi: title, date, author, tags, image, excerpt, SEO fields
- Aggiunta collection autori
- Backend: git-gateway (per Netlify)
- Prossimo: Step 3

### Step 3 - Cartella uploads
- Creata cartella assets/images/uploads/
- Aggiunto .gitkeep per mantenerla nel repo
- Prossimo: Step 4

### Step 4 - Meta SEO in default.html
- Modificato og:type per essere dinamico (article per post, website altrimenti)
- Aggiunti meta tag og:site_name e og:locale
- Corretti meta tag Twitter (da property a name)
- Aggiunto script Netlify Identity per redirect post-login
- File modificato: _layouts/default.html
- Prossimo: Step 5

### Step 5 - Schema.org in post.html
- Migliorato JSON-LD Schema.org esistente
- Aggiunto supporto per keywords (tags)
- Modificato dateModified per usare last_modified_at con fallback
- Usato jsonify per headline e description
- File modificato: _layouts/post.html
- Prossimo: Step 6

### Step 6 - robots.txt
- Creato robots.txt
- Permette indicizzazione completa del sito
- Blocca indicizzazione pannello /admin/
- Punta alla sitemap (generata automaticamente da jekyll-sitemap)
- Prossimo: Step 7

### Step 7 - Completamento
- Tutti i file creati/modificati con successo
- Push finale effettuato

### Step 8 - Tentativo GitHub OAuth con Netlify
- Modificato backend in admin/config.yml da git-gateway a github
- Rimosso Netlify Identity script da default.html e admin/index.html
- **PROBLEMA**: Sito Netlify bloccato per superamento limiti piano gratuito
- Errore: "Site not available - usage limits reached"
- Decisione: Abbandonare Netlify, usare Cloudflare Workers

### Step 9 - Verifica admin/index.html
- Verificato che file admin/index.html esiste ed è corretto
- Il file contiene il pannello Decap CMS
- Nessuna modifica necessaria

### Step 10 - Migrazione a Sveltia CMS
- Sostituito Decap CMS con Sveltia CMS (più moderno e veloce)
- Modificato admin/index.html per caricare Sveltia invece di Decap
- Primo tentativo OAuth con Cloudflare Worker custom (`rossodisera`)
- **PROBLEMA**: Errore "Invalid state key" persistente

### Step 11 - Risoluzione OAuth con Cloudflare Workers (SUCCESSO!)
- Eliminato worker custom `rossodisera`
- Deploy del worker ufficiale `sveltia-cms-auth` da https://github.com/sveltia/sveltia-cms-auth
- Configurazione corretta delle variabili d'ambiente su Cloudflare:
  - `GITHUB_CLIENT_ID`: Ov23liiOMLsgZeSv0Zes
  - `GITHUB_CLIENT_SECRET`: [nascosto]
  - `ALLOWED_DOMAINS`: ste2808.github.io
- Creata nuova GitHub OAuth App con callback URL corretto
- Semplificato admin/config.yml (rimossi campi che causavano errori di parsing)
- **RISULTATO**: Login OAuth funzionante! ✅

### Step 12 - Primo articolo pubblicato
- Creato articolo "Il vento nei capelli" direttamente dal CMS
- Caricata immagine di copertina
- Verificata pubblicazione su GitHub Pages
- URL: https://ste2808.github.io/rossodiserablog/2025/12/19/il-vento-nei-capelli/
- **IL CMS È COMPLETAMENTE OPERATIVO!** 🎉

---

## Riepilogo file creati/modificati

### Nuovi file:
- `admin/index.html` - Pannello amministrazione Sveltia CMS
- `admin/config.yml` - Configurazione CMS
- `assets/images/uploads/.gitkeep` - Cartella per upload immagini
- `robots.txt` - File per SEO e crawler
- `report_blog.md` - Questo file di report

### File modificati:
- `_layouts/default.html` - Meta tag SEO (Open Graph, Twitter Cards)
- `_layouts/post.html` - Schema.org JSON-LD

---

## Architettura finale

```
┌─────────────────────────────────────────────────────────┐
│                    UTENTE                                │
│         (Browser: PC, iPad, iPhone)                      │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              SVELTIA CMS                                 │
│     https://ste2808.github.io/rossodiserablog/admin/    │
└─────────────────────┬───────────────────────────────────┘
                      │ OAuth
                      ▼
┌─────────────────────────────────────────────────────────┐
│           CLOUDFLARE WORKERS                             │
│     https://sveltia-cms-auth.s-vozzi.workers.dev        │
│     (Gestisce autenticazione GitHub OAuth)               │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  GITHUB                                  │
│     Repository: StE2808/rossodiserablog                  │
│     (Storage articoli, immagini, configurazioni)         │
└─────────────────────┬───────────────────────────────────┘
                      │ GitHub Actions
                      ▼
┌─────────────────────────────────────────────────────────┐
│              GITHUB PAGES                                │
│     https://ste2808.github.io/rossodiserablog/          │
│     (Hosting sito statico)                               │
└─────────────────────────────────────────────────────────┘
```

---

## Configurazioni esterne

### GitHub OAuth App
- **Nome**: Rosso di Sera CMS
- **Client ID**: Ov23liiOMLsgZeSv0Zes
- **Homepage URL**: https://ste2808.github.io/rossodiserablog/
- **Callback URL**: https://sveltia-cms-auth.s-vozzi.workers.dev/callback
- **Posizione**: https://github.com/settings/developers

### Cloudflare Workers
- **Worker**: sveltia-cms-auth
- **URL**: https://sveltia-cms-auth.s-vozzi.workers.dev
- **Variabili d'ambiente**:
  - GITHUB_CLIENT_ID
  - GITHUB_CLIENT_SECRET
  - ALLOWED_DOMAINS
- **Dashboard**: https://dash.cloudflare.com/

---

## Come usare il CMS

### Accesso
1. Vai su https://ste2808.github.io/rossodiserablog/admin/
2. Clicca "Sign In with GitHub"
3. Autorizza l'app (solo la prima volta)
4. Sei dentro!

### Creare un nuovo articolo
1. Clicca "Articoli" → "New"
2. Compila i campi:
   - Titolo
   - Data
   - Autore
   - Tag (opzionale)
   - Immagine copertina (opzionale)
   - Sunto (per SEO e card homepage)
   - Contenuto (Markdown)
3. Clicca "Save" → "Publish"
4. Aspetta 1-2 minuti per il deploy

### Aggiungere altri autori
1. L'autore deve avere un account GitHub
2. Vai su https://github.com/StE2808/rossodiserablog/settings/access
3. "Add people" → Inserisci username GitHub
4. Assegna ruolo "Write"
5. L'autore accetta l'invito e può usare il CMS

---

## Problemi risolti durante l'implementazione

| Problema | Causa | Soluzione |
|----------|-------|-----------|
| Netlify "Site not available" | Limiti piano gratuito superati | Migrato a Cloudflare Workers |
| "Invalid state key" OAuth | Worker con nome custom | Usato worker ufficiale `sveltia-cms-auth` |
| "Configuration file could not be parsed" | YAML con sintassi complessa | Semplificato config.yml |
| admin/index.html 404 | File non pushato su GitHub | Force push con `git add -f` |

---

## Vantaggi della soluzione finale

- ✅ **Gratuito al 100%**: GitHub Pages + Cloudflare Workers (free tier)
- ✅ **Nessun limite di build**: A differenza di Netlify (300 min/mese)
- ✅ **Multi-dispositivo**: Funziona da PC, tablet, smartphone
- ✅ **Multi-autore**: Chiunque con accesso GitHub può scrivere
- ✅ **SEO ottimizzato**: Open Graph, Twitter Cards, Schema.org, Sitemap
- ✅ **Veloce**: Sveltia CMS è più performante di Decap/Netlify CMS
- ✅ **Open source**: Nessun vendor lock-in

---

## Link utili

- **Blog**: https://ste2808.github.io/rossodiserablog/
- **CMS Admin**: https://ste2808.github.io/rossodiserablog/admin/
- **Repository**: https://github.com/StE2808/rossodiserablog
- **Cloudflare Dashboard**: https://dash.cloudflare.com/
- **GitHub OAuth Apps**: https://github.com/settings/developers
- **Sveltia CMS Docs**: https://github.com/sveltia/sveltia-cms

---

Data completamento: 19 Dicembre 2025
Primo articolo pubblicato: "Il vento nei capelli"
