# Rosso di Sera - Documentazione Completa del Progetto

## Panoramica

**Rosso di Sera** è un blog Jekyll ospitato su GitHub Pages con un CMS (Sveltia CMS) che permette di scrivere articoli direttamente dal browser.

- **URL Blog**: https://ste2808.github.io/rossodiserablog/
- **URL CMS**: https://ste2808.github.io/rossodiserablog/admin/
- **Repository**: https://github.com/StE2808/rossodiserablog
- **Articoli**: 177 (176 migrati + 1 nuovo)
- **Autori**: StE2808, Lino Rialti (wqqz9pqy6z-cpu)

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
          - { label: "StE2808", value: "ste2808" }
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
│   └── post.html            # Articolo singolo (con Schema.org)
├── _authors/
│   ├── lino-rialti.md
│   └── ste2808.md
├── admin/
│   ├── index.html           # Pannello Sveltia CMS
│   └── config.yml           # Configurazione CMS
├── assets/
│   ├── css/style.css        # Stile personalizzato
│   └── images/              # Immagini articoli + uploads
├── index.html               # Homepage
├── archivio.md              # Pagina archivio
├── autori.md                # Pagina autori
├── robots.txt               # SEO
├── Gemfile                  # Dipendenze Ruby
└── report_blog.md           # Report implementazione
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

### 19 Dicembre 2024 (continuazione)
- Migrazione a Sveltia CMS
- Setup Cloudflare Workers per OAuth
- Risoluzione errori configurazione
- **SUCCESSO**: CMS funzionante!
- Primo articolo pubblicato: "Il vento nei capelli"

### 20 Dicembre 2024
- Aggiunto Lino come collaboratore (wqqz9pqy6z-cpu)
- Test pubblicazione multi-autore

---

## Problemi Noti e Soluzioni

| Problema | Causa | Soluzione |
|----------|-------|-----------|
| Titolo con `%20` | Copia/incolla da URL | Scrivere titolo a mano |
| "Invalid state key" OAuth | Worker con nome custom | Usare worker ufficiale `sveltia-cms-auth` |
| "Configuration could not be parsed" | YAML complesso | Semplificare config.yml |
| Netlify limiti superati | Piano gratuito | Usare Cloudflare Workers |
| admin/index.html 404 | File non pushato | `git add -f admin/index.html` |

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
- **Repository**: https://github.com/StE2808/rossodiserablog
- **Cloudflare**: https://dash.cloudflare.com/
- **GitHub OAuth**: https://github.com/settings/developers
- **Sveltia CMS Docs**: https://github.com/sveltia/sveltia-cms
- **Sveltia Auth Docs**: https://github.com/sveltia/sveltia-cms-auth

---

## Note per Future Modifiche

### Aggiungere un nuovo autore al dropdown CMS
Modifica `admin/config.yml`, sezione `options` del campo autore:
```yaml
options:
  - { label: "Lino Rialti", value: "lino-rialti" }
  - { label: "StE2808", value: "ste2808" }
  - { label: "Nuovo Autore", value: "nuovo-autore" }
```

### Cambiare dominio (es. rossodiserablog.it)
1. Compra dominio
2. Configura DNS (A records verso GitHub)
3. Crea file `CNAME` con `www.rossodiserablog.it`
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

---

*Documento generato il 20 Dicembre 2024*
