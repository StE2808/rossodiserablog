# CLAUDE.md

Questo file fornisce indicazioni a Claude Code (claude.ai/code) quando lavora con il codice in questo repository.

## Requisiti Linguistici

**Tutti i contenuti rivolti agli utenti devono essere in italiano.** Questo include:
- Contenuti dei post, titoli ed excerpt
- Meta description e campi SEO
- Commenti nei template e layout (dove appaiono nell'output renderizzato)
- I messaggi di commit devono essere in italiano quando si fanno modifiche ai contenuti

I commenti nel codice e la documentazione tecnica possono essere in inglese.

## Panoramica Progetto

**Rosso di Sera** è un blog politico e culturale italiano basato su Jekyll. Il sito presenta contenuti multi-autore con forte ottimizzazione SEO, integrazione con Sveltia CMS per la gestione dei contenuti e layout personalizzati per post, categorie e autori.

## Stack Tecnologico

- **Generatore Sito Statico**: Jekyll 4.3.3
- **CMS**: Sveltia CMS (basato su GitHub, con editorial workflow attivo)
- **Hosting**: GitHub Pages (presumibile dalla struttura del repo)
- **Formato Contenuti**: Markdown con front matter YAML
- **Plugin**: jekyll-seo-tag, jekyll-sitemap, jekyll-feed, jekyll-paginate

## Comandi di Sviluppo

### Sviluppo Locale
```bash
bundle install              # Installa dipendenze Ruby
bundle exec jekyll serve    # Avvia server di sviluppo locale (http://localhost:4000)
bundle exec jekyll build    # Compila il sito nella directory _site/
```

### Script di Manutenzione SEO
```bash
./scripts/seo-audit.sh      # Verifica i post per campi SEO mancanti (description, image_alt, ecc.)
./scripts/fix-h1-to-h2.sh   # Corregge i post che iniziano erroneamente con H1 invece di H2
```

### Script di Utilità (in _dev/)
```bash
python3 _dev/migrate_categories.py  # Migra le categorie da WordPress al formato Jekyll
python3 _dev/fix_societa.py         # Corregge problemi di encoding Unicode nei post
```

## Architettura dei Contenuti

### Post (_posts/)
- Formato nome file: `YYYY-MM-DD-slug.md`
- Campi obbligatori nel front matter:
  - `layout: post` (sempre)
  - `title`: Titolo editoriale (può essere creativo)
  - `date`: Data di pubblicazione con timezone
  - `author`: Deve corrispondere a un file in `_authors/` (es. "lino-rialti", "stefano-vozzi")
  - `category`: Una delle 15 categorie predefinite (vedi admin/config.yml)
  - `excerpt`: Testo di anteprima per le card e il feed RSS

- Campi SEO specifici (fortemente raccomandati):
  - `seo_title`: Max 60 caratteri, intento di ricerca utente (default a `title` se vuoto)
  - `description`: 120-155 caratteri, meta description per risultati di ricerca
  - `image_alt`: Descrivi cosa è visibile nell'immagine (accessibilità + SEO)
  - `focus_keyword`: Parola chiave principale per posizionamento SEO (appare nel JSON-LD Schema.org)

- Campi opzionali:
  - `image`: Percorso immagine di copertina
  - `tags`: Array di tag

### Autori (_authors/)
- Nome file: `username.md` (es. `lino-rialti.md`)
- Front matter:
  - `short_name`: Slug username
  - `name`: Nome completo da visualizzare
  - `position`: Descrizione ruolo
  - `bio`: Biografia opzionale
  - `avatar`: Immagine profilo opzionale

### Categorie (categoria/)
- 15 categorie predefinite come pagine standalone
- Ogni categoria è un semplice file markdown con front matter
- Categorie: politica-interna, politica-estera, cronaca-bianca, cronaca-nera, cronaca-rosa, cronaca-giudiziaria, economia-finanza, cultura-spettacolo, scienza-tecnologia, lifestyle-moda, opinioni-editoriali, inchieste-dossier, societa, ambiente, diritti-umani

### Layout (_layouts/)
- `default.html`: Layout base con meta tag SEO, markup Schema.org Organization
- `post.html`: Layout articolo con JSON-LD Schema.org Article, calcolo tempo di lettura
- `home.html`: Homepage con griglia post paginata
- `category.html`: Pagine archivio categorie

## Linee Guida SEO (Critiche)

Il sito ha requisiti SEO rigorosi. Quando crei o modifichi post:

1. **Uso Focus Keyword**: Deve apparire in:
   - Titolo SEO (o titolo normale)
   - Meta description
   - Prime 100 parole del contenuto
   - Almeno un heading H2

2. **Lunghezza Campi**:
   - `seo_title`: Max 60 caratteri
   - `description`: 120-155 caratteri
   - Immagini: Minimo 1200x630px per condivisione social

3. **Struttura Contenuto**:
   - Mai usare H1 (`#`) nel contenuto del post (il titolo è già H1)
   - Inizia il contenuto con heading H2 (`##`)
   - Includi link interni ad altri post del blog

4. **Alt Text**: Descrivi cosa è visibile nell'immagine, non l'argomento dell'articolo

Fai riferimento a `guida-autori.md` per la checklist SEO completa che seguono gli autori.

## Configurazione CMS (admin/config.yml)

- **Backend**: GitHub (branch: main)
- **Autenticazione**: Sveltia CMS con proxy Cloudflare Workers (`sveltia-cms-auth.s-vozzi.workers.dev`)
- **Editorial Workflow**: Abilitato (bozza → revisione → pubblicato)
- **Media**: Caricati in `assets/images/uploads/`
- **Locale**: Italiano (it)
- **Collezioni**: Post e Autori

Quando modifichi la configurazione CMS:
- Mantieni le categorie sincronizzate con la directory `categoria/`
- Aggiorna le opzioni autori quando aggiungi nuovi autori
- Mantieni le etichette e i suggerimenti dei campi in italiano

## Dettagli di Configurazione Importanti

### Configurazione Jekyll (_config.yml)
- **Struttura permalink**: `/:title/` (nessuna data negli URL)
- **Paginazione**: 12 post per pagina
- **Timezone**: Europe/Rome
- **Lingua**: it_IT
- **Feed**: Feed RSS solo excerpt su `/feed.xml`
- **Directory escluse**: `_dev/`, `_docs/`, node_modules, vendor

### Comportamento Front Matter
- I post usano `layout: post` di default
- `seo_title` sovrascrive `title` per i meta tag quando presente (vedi `_layouts/post.html:5-9`)
- `description` è usata per meta description; ripiego su excerpt troncato
- I nomi degli autori sono mappati nel JSON-LD Schema (stefano-vozzi → "Stefano Vozzi", lino-rialti → "Lino Rialti")

## Note di Sviluppo

### Lavorare con i Post
- I post sono datati dal 2023-09 in poi (180+ articoli)
- Mai committare post con informazioni sensibili
- Usa lo script di audit SEO prima di committare gruppi di post
- Controlla problemi H1/H2 con lo script di fix

### File Media
- Archivia in `assets/images/` (legacy) o `assets/images/uploads/` (caricati via CMS)
- Logo su `/assets/images/logo_trasparenza.png` (usato in Schema.org)
- Ottimizza le immagini prima del caricamento (il sito usa dimensioni grandi per condivisione social)

### Workflow Git
- Branch principale: `main`
- Il CMS crea branch per l'editorial workflow
- Il sito si autodeploya al push su main (trigger di deployment: `.deploy-trigger`)

### Note sulla Struttura Directory
- `_dev/`: Script di sviluppo, report migrazioni (escluso dal build)
- `_docs/`: Documentazione (escluso dal build)
- `dipassaggio/`: Scopo sconosciuto (contenuto legacy?)
- `scripts/`: Script di automazione produzione per manutenzione SEO
- `admin/`: Configurazione e UI di Sveltia CMS

## Dati Strutturati Schema.org

Il sito implementa markup Schema.org ricco:
- **Organization**: A livello sito in `default.html`
- **Article**: Per post in `post.html` con autore, editore, date, keywords
- Usa il campo `focus_keyword` per le keyword Schema (ripiego sulla categoria)

## Task Comuni

### Aggiungere un Nuovo Autore
1. Crea `_authors/username.md` con il front matter richiesto
2. Aggiorna `admin/config.yml` → collections → posts → fields → author → options
3. Aggiorna la mappatura nome autore in `_layouts/post.html` (sezione Schema.org)

### Aggiungere una Nuova Categoria
1. Crea `categoria/category-slug.md`
2. Aggiungi a `admin/config.yml` → collections → posts → fields → category → options
3. Aggiorna l'elenco categorie in questo documento

### Correggere Problemi SEO su Scala
1. Esegui `./scripts/seo-audit.sh` per identificare i problemi
2. Correggi i post manualmente o con script
3. Esegui `./scripts/fix-h1-to-h2.sh` per problemi di gerarchia heading
4. Verifica con un'altra esecuzione dell'audit
