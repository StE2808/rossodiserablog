# Rosso di Sera - Documentazione Completa del Progetto

**Ultimo aggiornamento: 22 Dicembre 2024**

---

## Panoramica

**Rosso di Sera** è un blog Jekyll ospitato su GitHub Pages con un CMS (Sveltia CMS) che permette di scrivere articoli direttamente dal browser.

- **URL Blog**: https://ste2808.github.io/rossodiserablog/
- **URL CMS**: https://ste2808.github.io/rossodiserablog/admin/
- **Repository**: https://github.com/StE2808/rossodiserablog
- **Articoli**: 177 (176 migrati + 1 nuovo)
- **Autori**: Stefano Vozzi, Lino Rialti

---

## Architettura del Sistema

```
UTENTE (Browser)
      │
      ▼
SVELTIA CMS (/admin/)
      │ OAuth
      ▼
CLOUDFLARE WORKERS (sveltia-cms-auth.s-vozzi.workers.dev)
      │
      ▼
GITHUB (Repository rossodiserablog)
      │ GitHub Actions
      ▼
GITHUB PAGES (Hosting)
      │
      ▼
GISCUS (Commenti via GitHub Discussions)
```

---

## Stack Tecnologico

| Componente | Tecnologia | Note |
|------------|------------|------|
| Generatore statico | Jekyll | Con plugin SEO |
| Hosting | GitHub Pages | Gratuito |
| CMS | Sveltia CMS | Fork moderno di Decap CMS |
| Autenticazione | GitHub OAuth | Via Cloudflare Workers |
| OAuth Proxy | Cloudflare Workers | Gratuito, senza limiti |
| Form Contatti | Google Apps Script | Salva su Google Sheets + notifica email |
| Commenti | Giscus | Basato su GitHub Discussions |

---

## Stato Attuale del Progetto

### ✅ Completato

- Design moderno con identità bordeaux
- CMS Sveltia funzionante con autenticazione OAuth
- 177 articoli migrati da WordPress
- SEO completo (Open Graph, Twitter Cards, Schema.org, Sitemap, RSS)
- Pagina Contatti con form funzionante
- Notifiche email per nuovi messaggi (a scrivi.rossodisera@gmail.com)
- Layout responsive (desktop/mobile)
- **Sistema commenti Giscus** (basato su GitHub Discussions)

### 📲 Da Fare (Prima del Go-Live)

1. **Menu hamburger mobile** - La navbar su mobile non ha navigazione
2. **Pagine categorie** - I link nel footer (Società, Politica, Cultura, Economia) puntano a `#`
3. **Tempo di lettura** - Mostrare "X min di lettura" negli articoli

### 📲 Da Fare (Nice to Have)

4. **Pagina "Chi siamo"** - Storia del blog e presentazione autori
5. **Ricerca articoli** - Campo di ricerca per l'archivio
6. **Pulsante "Torna su"** - Per articoli lunghi
7. **Articoli correlati** - Suggerimenti a fine articolo
8. **Newsletter** - Form iscrizione per ricevere nuovi articoli
9. **Dark mode** - Tema scuro per lettura serale

### 📲 Da Fare (Per il Lancio)

- Acquisto dominio personalizzato
- Configurazione DNS
- Aggiornamento URL in `_config.yml`
- Aggiornamento `ALLOWED_DOMAINS` su Cloudflare

---

## Sistema Commenti (Giscus)

### Configurazione
- **Sistema**: Giscus (https://giscus.app)
- **Backend**: GitHub Discussions
- **Categoria**: "Commenti" (tipo Announcement)
- **Mapping**: pathname (ogni articolo = una discussion)
- **Tema**: light
- **Lingua**: italiano

### Parametri Giscus
```html
<script src="https://giscus.app/client.js"
        data-repo="StE2808/rossodiserablog"
        data-repo-id="R_kgDOQodhxA"
        data-category="Commenti"
        data-category-id="DIC_kwDOQodhxM4C0HE9"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="light"
        data-lang="it"
        crossorigin="anonymous"
        async>
</script>
```

### Moderazione Commenti
1. Vai su https://github.com/StE2808/rossodiserablog/discussions
2. Trova la discussion corrispondente all'articolo
3. Clicca sui tre puntini (⋯) accanto al commento
4. Seleziona "Delete" per eliminare o "Hide" per nascondere

### App Giscus
- **Installazione**: https://github.com/apps/giscus
- **Configurata su**: solo repository `rossodiserablog`

---

## Form Contatti

### Configurazione
- **Google Sheet**: "Contatti Rosso di Sera"
- **Apps Script URL**: `https://script.google.com/macros/s/AKfycbwswRnizxmMA4yo0DOWYogwbPgn9fWUVMvMU85mxmV3AWokstm5BvLhfRmR3bXFNWH0/exec`
- **Email notifiche**: scrivi.rossodisera@gmail.com

### Funzionamento
1. Utente compila form su /contatti/
2. Dati inviati a Google Apps Script
3. Script salva riga in Google Sheets (Data, Nome, Email, Messaggio)
4. Script invia email di notifica

---

## File Chiave del Progetto

### admin/index.html
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex" />
  <title>Pannello Amministrazione - Rosso di Sera</title>
</head>
<body>
  <script src="https://unpkg.com/@sveltia/cms/dist/sveltia-cms.js"></script>
</body>
</html>
```

### admin/config.yml
```yaml
backend:
  name: github
  repo: StE2808/rossodiserablog
  branch: main
  base_url: https://sveltia-cms-auth.s-vozzi.workers.dev

publish_mode: editorial_workflow

media_folder: "assets/images/uploads"
public_folder: "/assets/images/uploads"

locale: 'it'

slug:
  encoding: "ascii"
  clean_accents: true
  sanitize_replacement: "-"

collections:
  - name: "posts"
    label: "Articoli"
    folder: "_posts"
    create: true
    slug: "{{year}}-{{month}}-{{day}}-{{slug}}"
    fields:
      - label: "Layout"
        name: "layout"
        widget: "hidden"
        default: "post"
      - label: "Titolo"
        name: "title"
        widget: "string"
        required: true
      - label: "Data pubblicazione"
        name: "date"
        widget: "datetime"
        format: "YYYY-MM-DD HH:mm:ss ZZ"
        required: true
      - label: "Autore"
        name: "author"
        widget: "select"
        options:
          - { label: "Lino Rialti", value: "lino-rialti" }
          - { label: "Stefano Vozzi", value: "stefano-vozzi" }
        required: true
      - label: "Tag"
        name: "tags"
        widget: "list"
        required: false
      - label: "Immagine copertina"
        name: "image"
        widget: "image"
        required: false
      - label: "Sunto"
        name: "excerpt"
        widget: "text"
        required: true
      - label: "Contenuto"
        name: "body"
        widget: "markdown"
        required: true

  - name: "authors"
    label: "Autori"
    folder: "_authors"
    create: true
    slug: "{{slug}}"
    fields:
      - label: "Nome completo"
        name: "name"
        widget: "string"
        required: true
      - label: "Username"
        name: "username"
        widget: "string"
        required: true
      - label: "Bio"
        name: "bio"
        widget: "text"
        required: false
      - label: "Immagine profilo"
        name: "avatar"
        widget: "image"
        required: false
```

---

## Configurazioni Esterne

### GitHub OAuth App
- **Nome**: Rosso di Sera CMS
- **Client ID**: `Ov23liiOMLsgZeSv0Zes`
- **Callback URL**: `https://sveltia-cms-auth.s-vozzi.workers.dev/callback`
- **Gestione**: https://github.com/settings/developers

### Cloudflare Workers
- **Worker**: `sveltia-cms-auth`
- **URL**: `https://sveltia-cms-auth.s-vozzi.workers.dev`
- **Variabili d'ambiente**:
  - `GITHUB_CLIENT_ID`: Ov23liiOMLsgZeSv0Zes
  - `GITHUB_CLIENT_SECRET`: [nascosto]
  - `ALLOWED_DOMAINS`: ste2808.github.io
- **Dashboard**: https://dash.cloudflare.com/

---

## Struttura Repository

```
rossodiserablog/
├── _config.yml              # Configurazione Jekyll
├── _posts/                  # 177 articoli Markdown
├── _layouts/
│   ├── default.html         # Layout base (con meta SEO)
│   ├── home.html            # Homepage con card
│   └── post.html            # Articolo singolo (con Schema.org + Giscus)
├── _authors/
│   ├── lino-rialti.md
│   └── stefano-vozzi.md
├── admin/
│   ├── index.html           # Pannello Sveltia CMS
│   └── config.yml           # Configurazione CMS
├── assets/
│   ├── css/style.css        # Stile personalizzato
│   └── images/              # Immagini articoli + uploads
├── index.html               # Homepage
├── archivio.md              # Pagina archivio
├── autori.md                # Pagina autori
├── contatti.md              # Pagina contatti con form
├── robots.txt               # SEO
├── Gemfile                  # Dipendenze Ruby
└── ROSSO_DI_SERA_DOCUMENTAZIONE.md
```

---

## Come Usare il CMS

### Accesso
1. Vai su https://ste2808.github.io/rossodiserablog/admin/
2. Clicca "Sign In with GitHub"
3. Autorizza l'app (solo prima volta)

### Creare un Articolo
1. Clicca "Articoli" → "New"
2. Compila:
   - **Titolo**: Scrivi a mano (non copiare con %20!)
   - **Data**: Seleziona data/ora
   - **Autore**: Scegli dal menu
   - **Tag**: Opzionale
   - **Immagine**: Opzionale, drag & drop
   - **Sunto**: Breve descrizione per card e SEO
   - **Contenuto**: Testo in Markdown
3. Clicca "Save" → "Publish"
4. Aspetta 1-2 minuti per il deploy

### Aggiungere un Nuovo Autore
1. L'autore crea account su https://github.com/signup
2. Tu vai su https://github.com/StE2808/rossodiserablog/settings/access
3. "Add people" → Inserisci username → Ruolo "Write" o "Collaborator"
4. L'autore accetta l'invito
5. Può accedere al CMS

---

## Cronologia del Progetto

### 14 Dicembre 2024
- Migrazione 176 articoli da JavaScript a Jekyll/Markdown
- Upload su GitHub in 6 blocchi
- Fix cartelle `_posts` duplicate

### 16 Dicembre 2024
- Restyling completo del design
- Aggiunta logo e header personalizzato
- Fix formattazione Markdown (4 spazi → blocchi codice)
- Risolto problema HTML entities negli apostrofi
- Copiato 436 immagini

### 19 Dicembre 2024
- Setup iniziale Decap CMS
- Tentativo Netlify Identity (fallito - limiti superati)
- Migrazione a GitHub OAuth
- Problemi "Invalid state key"
- Migrazione a Sveltia CMS
- Setup Cloudflare Workers per OAuth
- **SUCCESSO**: CMS funzionante!
- Primo articolo pubblicato: "Il vento nei capelli"

### 20 Dicembre 2024
- Aggiunto Lino come collaboratore
- Test pubblicazione multi-autore

### 21 Dicembre 2024
- Creata pagina Contatti con form
- Implementato Google Apps Script per salvataggio messaggi
- Configurata notifica email automatica a scrivi.rossodisera@gmail.com
- Aggiornata documentazione con roadmap funzionalità

### 22 Dicembre 2024
- **Implementato sistema commenti Giscus**
- Creata categoria "Commenti" su GitHub Discussions (tipo Announcement)
- Installata app Giscus sul repository
- Integrato widget commenti in `_layouts/post.html`
- Tema light per integrazione con design del blog
- Navigazione articoli spostata sotto i commenti

---

## Problemi Noti e Soluzioni

| Problema | Causa | Soluzione |
|----------|-------|-----------|
| Titolo con `%20` | Copia/incolla da URL | Scrivere titolo a mano |
| "Invalid state key" OAuth | Worker con nome custom | Usare worker ufficiale `sveltia-cms-auth` |
| "Configuration could not be parsed" | YAML complesso | Semplificare config.yml |
| Netlify limiti superati | Piano gratuito | Usare Cloudflare Workers |
| admin/index.html 404 | File non pushato | `git add -f admin/index.html` |
| Giscus "Nessuna categoria trovata" | Cache o categoria non salvata | Inserire nome categoria manualmente |

---

## SEO Implementato

- ✅ Open Graph (Facebook)
- ✅ Twitter Cards
- ✅ Schema.org JSON-LD (BlogPosting)
- ✅ Sitemap XML automatico
- ✅ Feed RSS
- ✅ robots.txt
- ✅ Canonical URLs
- ✅ Meta description da excerpt

---

## Link Utili

- **Blog**: https://ste2808.github.io/rossodiserablog/
- **CMS**: https://ste2808.github.io/rossodiserablog/admin/
- **Contatti**: https://ste2808.github.io/rossodiserablog/contatti/
- **Repository**: https://github.com/StE2808/rossodiserablog
- **Discussions (Commenti)**: https://github.com/StE2808/rossodiserablog/discussions
- **Cloudflare**: https://dash.cloudflare.com/
- **GitHub OAuth**: https://github.com/settings/developers
- **Google Sheet Contatti**: Google Sheets → "Contatti Rosso di Sera"
- **Sveltia CMS Docs**: https://github.com/sveltia/sveltia-cms
- **Sveltia Auth Docs**: https://github.com/sveltia/sveltia-cms-auth
- **Giscus**: https://giscus.app

---

## Note per Future Modifiche

### Aggiungere un nuovo autore al dropdown CMS
Modifica `admin/config.yml`, sezione `options` del campo autore:
```yaml
options:
  - { label: "Lino Rialti", value: "lino-rialti" }
  - { label: "Stefano Vozzi", value: "stefano-vozzi" }
  - { label: "Nuovo Autore", value: "nuovo-autore" }
```

### Cambiare dominio (es. rossodisera.it)
1. Compra dominio
2. Configura DNS (A records verso GitHub)
3. Crea file `CNAME` con `www.rossodisera.it`
4. GitHub Settings → Pages → Custom domain
5. Aggiorna `_config.yml` con nuovo URL
6. Aggiorna `ALLOWED_DOMAINS` su Cloudflare

### Rigenerare OAuth Secret
1. GitHub → Settings → Developer settings → OAuth Apps
2. "Rosso di Sera CMS" → Generate new client secret
3. Copia il nuovo secret
4. Cloudflare → Workers → sveltia-cms-auth → Settings → Variables
5. Aggiorna `GITHUB_CLIENT_SECRET`
6. Distribuisci

### Modificare email notifiche contatti
1. Google Sheets → "Contatti Rosso di Sera" → Estensioni → Apps Script
2. Modifica `var emailDestinatario = "nuova@email.com";`
3. Salva e fai nuovo deployment

### Cambiare tema Giscus
Modifica `_layouts/post.html`, attributo `data-theme`:
- `light` - tema chiaro
- `dark` - tema scuro
- `preferred_color_scheme` - segue preferenze sistema
- `noborder_light` - chiaro senza bordi
- URL di un CSS custom per tema personalizzato
