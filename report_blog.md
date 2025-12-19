# Report Implementazione CMS + SEO - Rosso di Sera

Data inizio: 19 Dicembre 2024

## Stato: IN CORSO

### Checklist
- [x] Step 0: Setup iniziale
- [x] Step 1: Creazione admin/index.html
- [x] Step 2: Creazione admin/config.yml
- [x] Step 3: Cartella uploads
- [x] Step 4: Meta SEO in default.html
- [ ] Step 5: Schema.org in post.html
- [ ] Step 6: robots.txt
- [ ] Step 7: Commit e push finale

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
