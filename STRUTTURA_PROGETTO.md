# Struttura Progetto Rosso di Sera Blog

## Informazioni Generali
- **Nome**: Rosso di Sera
- **Tagline**: Una luce nel mondo digitale
- **URL**: https://ste2808.github.io/rossodiserablog
- **Piattaforma**: Jekyll (static site generator)
- **Lingua**: Italiano (it_IT)
- **Timezone**: Europe/Rome

## Struttura Directory

```
rossodiserablog/
│
├── _authors/                    # Profili degli autori
│   ├── lino-rialti.md
│   └── stefano-vozzi.md
│
├── _layouts/                    # Template HTML
│   ├── category.html           # Layout per pagine categoria
│   ├── default.html            # Layout di base
│   ├── home.html               # Layout homepage
│   └── post.html               # Layout articoli singoli
│
├── _posts/                      # Articoli del blog (181 post)
│   └── YYYY-MM-DD-titolo.md    # Formato standard Jekyll
│       ├── 2023/               # Articoli dal 2023
│       ├── 2024/               # Articoli dal 2024
│       └── 2025/               # Articoli dal 2025
│
├── admin/                       # CMS Sveltia/Netlify
│   ├── config.yml              # Configurazione CMS
│   └── index.html              # Interfaccia admin
│
├── assets/                      # Risorse statiche
│   ├── css/
│   │   └── style.css           # Stili principali
│   └── images/
│       ├── logo_trasparenza.png
│       ├── 2023/               # Immagini per anno
│       │   ├── 09/
│       │   ├── 10/
│       │   ├── 11/
│       │   └── 12/
│       ├── 2024/
│       │   ├── 01/
│       │   ├── 02/
│       │   ├── 03/
│       │   ├── 04/
│       │   ├── 05/
│       │   ├── 06/
│       │   └── 11/
│       ├── 2025/
│       │   ├── 01/
│       │   ├── 02/
│       │   ├── 03/
│       │   ├── 04/
│       │   ├── 05/
│       │   ├── 06/
│       │   ├── 07/
│       │   ├── 08/
│       │   └── 09/
│       └── uploads/            # Upload CMS
│
├── categoria/                   # Pagine categoria
│   ├── altro.md
│   ├── ambiente.md
│   ├── arte-artisti.md
│   ├── cronaca.md
│   ├── cultura.md
│   ├── diritti-umani.md
│   ├── economia.md
│   ├── politica.md
│   ├── salute.md
│   ├── scuola.md
│   └── societa.md
│
├── .claude/                     # Configurazione Claude Code
├── .git/                        # Repository Git
├── dipassaggio/                 # File temporanei/backup
│
├── _config.yml                  # Configurazione Jekyll
├── .gitignore                   # File esclusi da Git
├── archivio.md                  # Pagina archivio
├── autori.md                    # Pagina autori
├── contatti.md                  # Pagina contatti
├── Gemfile                      # Dipendenze Ruby
├── index.html                   # Homepage
├── README.md                    # Documentazione progetto
├── report_blog.md               # Report progetto
└── robots.txt                   # Istruzioni per crawler

```

## Configurazione (_config.yml)

### Impostazioni Base
- **Title**: Rosso di Sera
- **Description**: Blog di riflessioni, cultura e tecnologia
- **Autori**: Lino Rialti & Stefano Vozzi
- **Email**: s.vozzi@gmail.com

### Build Settings
- **Markdown**: kramdown
- **Permalink**: /:year/:month/:day/:title/
- **Paginazione**: 12 articoli per pagina

### Plugin Jekyll
1. jekyll-paginate
2. jekyll-seo-tag
3. jekyll-sitemap
4. jekyll-feed

### Collections
- **authors**: profili autori con output dedicato

## Categorie Blog

Il blog organizza i contenuti in 11 categorie tematiche:

1. **Altro** - Contenuti vari
2. **Ambiente** - Tematiche ambientali e clima
3. **Arte e Artisti** - Cultura artistica
4. **Cronaca** - Notizie e attualità
5. **Cultura** - Riflessioni culturali
6. **Diritti Umani** - Tematiche sociali e diritti
7. **Economia** - Economia e finanza
8. **Politica** - Analisi politica
9. **Salute** - Salute e benessere
10. **Scuola** - Educazione e formazione
11. **Società** - Temi sociali

## Gestione Contenuti

### CMS Sveltia (admin/)
- Interfaccia grafica per gestione contenuti
- Configurazione in `admin/config.yml`
- Upload immagini in `assets/images/uploads/`

### Articoli (_posts/)
- Formato: `YYYY-MM-DD-titolo.md`
- Front matter YAML con metadati
- Oltre 180 articoli pubblicati dal 2023

### Immagini
- Organizzate per anno e mese
- Path: `/assets/images/YYYY/MM/`
- Logo in `/assets/images/logo_trasparenza.png`

## Funzionalità SEO

- SEO tag automatici (jekyll-seo-tag)
- Sitemap XML (jekyll-sitemap)
- Feed RSS (jekyll-feed)
- Schema.org markup
- Social media metadata

## Deploy

- **Hosting**: GitHub Pages
- **Repository**: https://github.com/StE2808/rossodiserablog
- **Trigger**: `.deploy-trigger` (file per forzare rebuild)

## Note Tecniche

- Jekyll genera sito statico da markdown
- Build automatico su GitHub Pages
- Nessun database, tutto in file markdown
- Versionamento completo con Git
