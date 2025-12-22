# Struttura Progetto - Rosso di Sera Blog

## Struttura Directory

```
rossodiserablog/
│
├── Doc/                                    # Documentazione del progetto
│   ├── claude_code_report_blog_aggiornato.md
│   ├── report_blog.md
│   ├── ROSSO_DI_SERA_DOCUMENTAZIONE.md
│   └── ultima sessione claude code.rtf
│
├── _authors/                               # Profili degli autori
│   ├── lino-rialti.md
│   └── ste2808.md
│
├── _layouts/                               # Template HTML Jekyll
│   ├── default.html
│   ├── home.html
│   └── post.html
│
├── _posts/                                 # Articoli del blog (140+ post)
│   ├── 2023-09-04-*.md                    # Articoli settembre 2023
│   ├── 2023-10-*.md                       # Articoli ottobre 2023
│   ├── 2023-11-*.md                       # Articoli novembre 2023
│   ├── 2023-12-*.md                       # Articoli dicembre 2023
│   ├── 2024-01-*.md                       # Articoli 2024
│   ├── 2024-02-*.md
│   ├── 2024-03-*.md
│   ├── 2024-04-*.md
│   ├── 2024-05-*.md
│   ├── 2024-06-*.md
│   ├── 2024-11-*.md
│   └── 2025-*.md                          # Articoli 2025 (fino a settembre)
│
├── admin/                                  # CMS Admin Panel
│   ├── config.yml                         # Configurazione Sveltia CMS
│   └── index.html                         # Interfaccia admin
│
├── assets/                                 # Risorse statiche
│   ├── css/
│   │   └── style.css                      # Stili personalizzati
│   └── images/                            # Immagini
│       ├── 2023/                          # Immagini anno 2023
│       ├── 2024/                          # Immagini anno 2024
│       ├── 2025/                          # Immagini anno 2025
│       ├── uploads/                       # Upload CMS
│       └── logo_trasparenza.png           # Logo del sito
│
├── .claude/                                # Configurazione Claude Code
│   └── settings.local.json
│
├── .git/                                   # Repository Git
│
├── _config.yml                             # Configurazione principale Jekyll
├── archivio.md                             # Pagina archivio
├── autori.md                               # Pagina autori
├── Gemfile                                 # Dipendenze Ruby/Jekyll
├── index.html                              # Homepage
├── README.md                               # Documentazione progetto
├── robots.txt                              # Istruzioni per crawler
└── .gitignore                              # File Git da ignorare

```

## Statistiche

- **Totale articoli**: circa 140+ post dal settembre 2023 a settembre 2025
- **Autori**: 2 (lino-rialti, ste2808)
- **Layout disponibili**: 3 (default, home, post)
- **CMS**: Sveltia CMS con autenticazione Cloudflare OAuth
- **Framework**: Jekyll (generatore di siti statici)

## File di configurazione principali

- `_config.yml` - Configurazione Jekyll
- `admin/config.yml` - Configurazione CMS
- `Gemfile` - Dipendenze Ruby
- `.gitignore` - Esclusioni Git

## Rami Git

- **Branch corrente**: main
- **Ultimo commit**: "Migrato a Sveltia CMS con Cloudflare OAuth" (f41ae58)
