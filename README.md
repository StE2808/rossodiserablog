# Rosso di Sera Blog

Un blog Jekyll pronto per GitHub Pages.

## Struttura

```
rossodiserablog/
├── _config.yml          # Configurazione del sito
├── _posts/              # Tutti gli articoli (176 file)
├── _layouts/            # Template delle pagine
├── _authors/            # Profili autori
├── assets/css/          # Fogli di stile
├── CNAME                # Dominio personalizzato
├── index.html           # Homepage
├── archivio.md          # Pagina archivio
└── autori.md            # Pagina autori
```

## Come pubblicare su GitHub Pages

1. Vai su https://github.com/StE2808/rossodiserablog
2. Clicca su "Add file" → "Upload files"
3. Trascina tutti i file di questa cartella
4. Clicca "Commit changes"

## Attivare GitHub Pages

1. Vai in "Settings" → "Pages"
2. Source: seleziona "Deploy from a branch"
3. Branch: seleziona "main" e "/ (root)"
4. Clicca "Save"

## Configurare il dominio

Per usare www.rossodiserablog.it:

1. Acquista il dominio da un registrar
2. Configura i DNS:
   - Record A: 185.199.108.153
   - Record A: 185.199.109.153
   - Record A: 185.199.110.153
   - Record A: 185.199.111.153
   - CNAME www → ste2808.github.io

3. In GitHub Settings → Pages, inserisci il dominio

## Aggiungere nuovi articoli

Crea un file in `_posts/` con formato:
```
YYYY-MM-DD-titolo-articolo.md
```

Contenuto:
```markdown
---
layout: post
title: "Titolo dell'articolo"
date: 2025-01-15 10:00:00 +0100
author: lino-rialti
tags: ["tag1", "tag2"]
---

Contenuto dell'articolo in Markdown...
```

## Autori

- `lino-rialti` - Lino Rialti
- `ste2808` - StE2808

---

Creato con ❤️ da Claude
