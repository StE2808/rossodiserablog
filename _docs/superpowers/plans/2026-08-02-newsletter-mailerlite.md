# Newsletter MailerLite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Attivare la newsletter di Rosso di Sera: gruppo MailerLite, dominio di invio autenticato, inoltro risposte, box di iscrizione sul sito con doppio opt-in.

**Architecture:** Form HTML/CSS custom nel sito Jekyll che invia all'endpoint pubblico del form embedded MailerLite (nessun widget esterno, nessun segreto esposto). DNS e inoltro email su Cloudflare via API. I passaggi che MailerLite espone solo in dashboard (sending domain, double opt-in, creazione form, mittente) li fa Stefano guidato passo-passo.

**Tech Stack:** Jekyll 4.3.3, MailerLite Connect API (`https://connect.mailerlite.com/api`), Cloudflare API v4 (DNS + Email Routing), curl + python3 per gli script.

**Spec di riferimento:** `_docs/superpowers/specs/2026-08-02-newsletter-mailerlite-design.md`

## Global Constraints

- Tutti i testi rivolti agli utenti in italiano; mai usare trattini lunghi (—) in nessun testo o copy.
- Mittente: solo `newsletter@rossodiserablog.it`; mai email personali come mittente; mai indirizzi email in chiaro nelle pagine del sito.
- Mai usare il tool Edit sui file `_posts/*.md` (in questo piano non si toccano post; layout, include e CSS si editano normalmente).
- Un solo record SPF (TXT `v=spf1 ...`) sull'apex del dominio.
- Prefisso classi CSS del box: `rds-nl-`.
- Credenziali SOLO da `~/.secrets/credentials.yaml` (sezioni `mailerlite`, `cloudflare`); mai committarle nel repo. L'endpoint del form MailerLite (ACCOUNT_ID/FORM_ID) è pubblico e si può committare.
- Messaggi di commit in italiano, chiusi con `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- Zone ID Cloudflare `rossodiserablog.it`: `80d3b27200f3277db263f1d5aedae81a`. Account ID: `a6edb89ea4ef70e3e030aa0aee9d1c6c`.
- I task 2, 4 (click di verifica) e 5 richiedono Stefano in dashboard: eseguirli inline nella sessione, non delegabili a subagent senza interazione.

Setup comune a tutti gli step con curl (da rifare in ogni chiamata Bash, lo stato shell non persiste):

```bash
MLTOKEN=$(python3 -c "import yaml;print(yaml.safe_load(open('/Users/ste/.secrets/credentials.yaml'))['mailerlite']['api_token'])")
CFTOKEN=$(python3 -c "import yaml;print(yaml.safe_load(open('/Users/ste/.secrets/credentials.yaml'))['cloudflare']['api_token'])")
ZONE=80d3b27200f3277db263f1d5aedae81a
ACCOUNT=a6edb89ea4ef70e3e030aa0aee9d1c6c
```

---

### Task 1: MailerLite via API: gruppo nuovo e pulizia Aenigma

**Files:**
- Nessun file del repo. Solo chiamate API MailerLite.

**Interfaces:**
- Consumes: token `mailerlite.api_token` da credentials.yaml.
- Produces: `GROUP_ID` del gruppo "Rosso di Sera Newsletter" (stringa numerica restituita dalla POST). Usato dai Task 5 (collegare il form al gruppo) e 7 (verifica iscritto). Annotarlo nella sessione.

- [ ] **Step 1: Creare il gruppo "Rosso di Sera Newsletter"**

```bash
curl -s -X POST -H "Authorization: Bearer $MLTOKEN" -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"name":"Rosso di Sera Newsletter"}' \
  https://connect.mailerlite.com/api/groups | python3 -m json.tool
```

Expected: JSON con `data.id` (annotare come GROUP_ID) e `data.name` = "Rosso di Sera Newsletter".

- [ ] **Step 2: Eliminare il gruppo "Aenigma Press Newsletter" (id 192421046673999305, 0 iscritti)**

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X DELETE -H "Authorization: Bearer $MLTOKEN" \
  https://connect.mailerlite.com/api/groups/192421046673999305
```

Expected: `204`.

- [ ] **Step 3: Eliminare il form "aenigmapress-signup" (id 192421754859160744)**

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X DELETE -H "Authorization: Bearer $MLTOKEN" \
  https://connect.mailerlite.com/api/forms/192421754859160744
```

Expected: `204`. Se risponde `404`/`405` (endpoint non disponibile): aggiungere la cancellazione manuale alla lista dashboard del Task 5, Step 4.

- [ ] **Step 4: Verificare lo stato finale**

```bash
curl -s -H "Authorization: Bearer $MLTOKEN" -H "Accept: application/json" https://connect.mailerlite.com/api/groups | \
  python3 -c "import json,sys;print([g['name'] for g in json.load(sys.stdin)['data']])"
```

Expected: `['Rosso di Sera Newsletter']`.

---

### Task 2: Dashboard MailerLite: aggiungere il sending domain (Stefano)

**Files:** nessuno. Task manuale guidato, gate umano.

**Interfaces:**
- Produces: elenco dei record DNS richiesti da MailerLite (tipo, nome, valore per ciascuno; tipicamente 2-3 record tra CNAME DKIM e TXT SPF, più eventuale record di verifica). Consumato dal Task 3.

- [ ] **Step 1: Guidare Stefano in dashboard**

Dare a Stefano queste istruzioni:
1. Login su https://dashboard.mailerlite.com con l'account `s.vozzi@gmail.com`.
2. Andare su **Settings (icona ingranaggio) → Domains** (a seconda della versione: "Domains" o "Sender domains").
3. Cliccare **Add domain** / **Authenticate a domain** e inserire `rossodiserablog.it`.
4. MailerLite mostra una tabella di record DNS da creare (DKIM, SPF, a volte un record di verifica). NON chiudere la pagina.
5. Copiare e incollare in chat, per ogni record: **tipo** (TXT/CNAME), **nome/host** e **valore** esatti.

- [ ] **Step 2: Registrare i record ricevuti**

Trascrivere i record in una nota della sessione (serviranno identici nel Task 3). Verifica di completezza: c'è almeno un record DKIM (di solito CNAME con `_domainkey` nel nome) e uno SPF (TXT che inizia con `v=spf1`). Se MailerLite non chiede SPF, procedere solo con ciò che chiede.

---

### Task 3: Record DNS su Cloudflare via API (DKIM, SPF, DMARC)

**Files:** nessun file del repo. Solo API Cloudflare.

**Interfaces:**
- Consumes: record DNS dal Task 2 (tipo, nome, valore).
- Produces: record attivi nella zona; dominio verificabile in MailerLite (verifica fatta nel Task 5).

- [ ] **Step 1: Creare ogni record richiesto da MailerLite**

Per ogni record del Task 2, sostituire NOME e VALORE (il nome può essere relativo, es. `litesrv._domainkey`, Cloudflare lo completa col dominio):

```bash
# Record CNAME (esempio DKIM)
curl -s -X POST -H "Authorization: Bearer $CFTOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records" \
  -d '{"type":"CNAME","name":"NOME","content":"VALORE","ttl":3600,"proxied":false}' | \
  python3 -c "import json,sys;d=json.load(sys.stdin);print('OK' if d['success'] else d['errors'])"

# Record TXT (esempio SPF)
curl -s -X POST -H "Authorization: Bearer $CFTOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records" \
  -d '{"type":"TXT","name":"NOME","content":"\"VALORE\"","ttl":3600}' | \
  python3 -c "import json,sys;d=json.load(sys.stdin);print('OK' if d['success'] else d['errors'])"
```

Expected: `OK` per ogni record.

- [ ] **Step 2: Aggiungere il record DMARC base**

```bash
curl -s -X POST -H "Authorization: Bearer $CFTOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records" \
  -d '{"type":"TXT","name":"_dmarc","content":"\"v=DMARC1; p=none\"","ttl":3600}' | \
  python3 -c "import json,sys;d=json.load(sys.stdin);print('OK' if d['success'] else d['errors'])"
```

Expected: `OK`.

- [ ] **Step 3: Verificare la propagazione**

```bash
dig +short TXT rossodiserablog.it @1.1.1.1
dig +short TXT _dmarc.rossodiserablog.it @1.1.1.1
# più un dig per ogni record DKIM col nome esatto del Task 2, es.:
# dig +short CNAME litesrv._domainkey.rossodiserablog.it @1.1.1.1
```

Expected: ogni record risponde col valore inserito (su 1.1.1.1 la propagazione è immediata, è l'authoritative di Cloudflare).

---

### Task 4: Cloudflare Email Routing: newsletter@ verso scrivi.rossodisera@gmail.com

**Files:** nessun file del repo. API Cloudflare account-level e zone-level.

**Interfaces:**
- Consumes: `CFTOKEN`, `ZONE`, `ACCOUNT`.
- Produces: inoltro attivo `newsletter@rossodiserablog.it` → `scrivi.rossodisera@gmail.com`; record MX/SPF di Cloudflare nella zona.

**Attenzione**: il token Cloudflare in credentials.yaml è zone-level (DNS). La creazione della destination address è account-level e può rispondere 403. In quel caso usare il fallback dashboard (Step 5).

- [ ] **Step 1: Creare la destination address (parte l'email di verifica)**

```bash
curl -s -X POST -H "Authorization: Bearer $CFTOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT/email/routing/addresses" \
  -d '{"email":"scrivi.rossodisera@gmail.com"}' | python3 -m json.tool
```

Expected: `success: true`. Se `403` → Step 5 (fallback dashboard).

- [ ] **Step 2: Abilitare Email Routing sulla zona (aggiunge MX + SPF di Cloudflare)**

```bash
curl -s -X POST -H "Authorization: Bearer $CFTOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE/email/routing/dns" | python3 -m json.tool
```

Expected: `success: true` e record MX (`route1/2/3.mx.cloudflare.net`) creati. Se l'endpoint risponde errore → Step 5.

- [ ] **Step 3: GATE Stefano: click di verifica**

Chiedere a Stefano di aprire la casella `scrivi.rossodisera@gmail.com` e cliccare il link nell'email di verifica di Cloudflare. Confermare in chat prima di proseguire.

- [ ] **Step 4: Creare la regola di inoltro**

```bash
curl -s -X POST -H "Authorization: Bearer $CFTOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE/email/routing/rules" \
  -d '{"actions":[{"type":"forward","value":["scrivi.rossodisera@gmail.com"]}],"matchers":[{"type":"literal","field":"to","value":"newsletter@rossodiserablog.it"}],"enabled":true,"name":"Inoltro newsletter"}' | \
  python3 -c "import json,sys;d=json.load(sys.stdin);print('OK' if d['success'] else d['errors'])"
```

Expected: `OK`.

- [ ] **Step 5 (solo se un passo API ha risposto 403/errore): fallback dashboard**

Guidare Stefano: dash.cloudflare.com → zona `rossodiserablog.it` → **Email → Email Routing** → "Get started"/"Enable": inserire destinazione `scrivi.rossodisera@gmail.com`, confermare l'email di verifica, creare la regola custom address `newsletter@rossodiserablog.it` → forward alla destinazione. Cloudflare aggiunge MX e SPF da solo (accettare "Add records automatically").

- [ ] **Step 6: Fondere gli SPF se ora sono due**

```bash
curl -s -H "Authorization: Bearer $CFTOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records?type=TXT&name=rossodiserablog.it" | \
  python3 -c "
import json,sys
for r in json.load(sys.stdin)['result']:
    if 'v=spf1' in r['content']:
        print(r['id'], r['content'])"
```

Se escono DUE record `v=spf1` (uno MailerLite, uno Cloudflare `include:_spf.mx.cloudflare.net`): aggiornarne uno col merge degli include e cancellare l'altro. Esempio con gli id trovati (RECORD_ID_TENUTO, RECORD_ID_DOPPIO) e gli include reali:

```bash
curl -s -X PATCH -H "Authorization: Bearer $CFTOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records/RECORD_ID_TENUTO" \
  -d '{"content":"\"v=spf1 include:_spf.mx.cloudflare.net include:INCLUDE_MAILERLITE ~all\""}'
curl -s -o /dev/null -w "%{http_code}\n" -X DELETE -H "Authorization: Bearer $CFTOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records/RECORD_ID_DOPPIO"
```

Verifica finale: `dig +short TXT rossodiserablog.it @1.1.1.1` mostra UN solo `v=spf1` con entrambi gli include.

- [ ] **Step 7: Test dell'inoltro**

Chiedere a Stefano di mandare (da qualunque casella) un'email a `newsletter@rossodiserablog.it` e confermare che arriva su `scrivi.rossodisera@gmail.com`. Non proseguire finché non arriva.

---

### Task 5: Dashboard MailerLite: verifica dominio, doppio opt-in in italiano, form, mittente (Stefano)

**Files:** nessuno. Task manuale guidato, gate umano.

**Interfaces:**
- Consumes: GROUP_ID / nome gruppo dal Task 1; record DNS attivi dal Task 3.
- Produces: endpoint del form per il Task 6, nel formato `https://assets.mailerlite.com/jsonp/ACCOUNT_ID/forms/FORM_ID/subscribe` (ricavato dallo snippet embedded che Stefano incolla in chat). Mittente predefinito impostato.

- [ ] **Step 1: Verificare il dominio**

Stefano: Settings → Domains → `rossodiserablog.it` → cliccare **Verify** / **Check records**. Expected: spunte verdi su tutti i record. Se un record risulta rosso: ricontrollare nome/valore con `dig` e correggere via API (Task 3, Step 1), poi ripetere.

- [ ] **Step 2: Creare il form embedded "rosso-di-sera-signup"**

Stefano: **Forms → Embedded forms → Create embedded form**, nome `rosso-di-sera-signup`, collegarlo al gruppo **Rosso di Sera Newsletter**. Nelle impostazioni del form attivare il **Double opt-in**.

- [ ] **Step 3: Tradurre in italiano l'email di conferma e la thank you page**

Nell'editor del double opt-in (email di conferma + pagina di ringraziamento), inserire questi testi:

Email di conferma:
- Oggetto: `Conferma la tua iscrizione a Rosso di Sera`
- Testo: `Ciao! Per completare l'iscrizione alla newsletter di Rosso di Sera clicca il pulsante qui sotto. Se non hai richiesto tu l'iscrizione, ignora questa email.`
- Pulsante: `Confermo l'iscrizione`

Pagina di ringraziamento (dopo il click):
- Titolo: `Iscrizione confermata!`
- Testo: `Benvenuto nella newsletter di Rosso di Sera. Da adesso riceverai un'email quando esce un nuovo articolo. A presto!`

- [ ] **Step 4: Copiare lo snippet e chiudere la pulizia**

1. Dalla pagina del form, copiare lo **snippet HTML** (tab "Embed" / "HTML code") e incollarlo in chat: da lì si estraggono ACCOUNT_ID e FORM_ID dell'action `https://assets.mailerlite.com/jsonp/ACCOUNT_ID/forms/FORM_ID/subscribe`.
2. Solo se il Task 1 Step 3 è fallito: eliminare a mano il form `aenigmapress-signup` (Forms → Embedded → cestino).

- [ ] **Step 5: Impostare il mittente predefinito**

Stefano: Settings → **Default sender** (o "Senders"): nome `Rosso di Sera`, email `newsletter@rossodiserablog.it` (disponibile ora che il dominio è verificato). Salvare.

---

### Task 6: Sito Jekyll: box newsletter in post e homepage

**Files:**
- Create: `_includes/newsletter-box.html` (la directory `_includes/` non esiste ancora, crearla)
- Modify: `_layouts/post.html` (riga ~106, prima del blocco `<!-- Sezione Commenti -->`)
- Modify: `_layouts/home.html` (riga ~95, dopo la chiusura di `.articles-section`, prima del tag script di hero-tree)
- Modify: `assets/css/style.css` (append in fondo, dopo la sezione search, ~riga 1744)

**Interfaces:**
- Consumes: endpoint del form dal Task 5 (sostituire ACCOUNT_ID e FORM_ID reali nell'action).
- Produces: include `newsletter-box.html` riusabile; classi CSS `rds-nl-*`.

- [ ] **Step 1: Creare `_includes/newsletter-box.html`**

Contenuto completo (sostituire ACCOUNT_ID e FORM_ID con i valori reali del Task 5):

```html
<section class="rds-nl" aria-label="Iscrizione alla newsletter">
    <h3 class="rds-nl-title">La newsletter di Rosso di Sera</h3>
    <p class="rds-nl-text">Un'email quando esce un nuovo articolo. Niente spam, cancellazione con un click in ogni email.</p>
    <form class="rds-nl-form" action="https://assets.mailerlite.com/jsonp/ACCOUNT_ID/forms/FORM_ID/subscribe" method="post" target="_blank">
        <div class="rds-nl-row">
            <input type="email" name="fields[email]" class="rds-nl-input" placeholder="la-tua@email.it" aria-label="Il tuo indirizzo email" autocomplete="email" required>
            <button type="submit" class="rds-nl-btn">Iscriviti</button>
        </div>
        <input type="text" name="website" class="rds-nl-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <input type="hidden" name="ml-submit" value="1">
        <input type="hidden" name="anticsrf" value="true">
        <p class="rds-nl-status" role="status" aria-live="polite"></p>
    </form>
</section>
<script>
(function () {
    document.querySelectorAll('.rds-nl-form').forEach(function (form) {
        if (form.dataset.nlReady) { return; }
        form.dataset.nlReady = '1';
        form.addEventListener('submit', function (ev) {
            ev.preventDefault();
            var status = form.querySelector('.rds-nl-status');
            var hp = form.querySelector('.rds-nl-hp');
            if (hp && hp.value) { return; }
            var btn = form.querySelector('.rds-nl-btn');
            btn.disabled = true;
            status.textContent = 'Invio in corso...';
            fetch(form.action, { method: 'POST', body: new FormData(form) })
                .then(function (r) { return r.json(); })
                .then(function (d) {
                    if (d && d.success) {
                        form.querySelector('.rds-nl-row').hidden = true;
                        status.textContent = 'Quasi fatto! Controlla la posta e clicca il link di conferma.';
                    } else {
                        throw new Error('subscribe failed');
                    }
                })
                .catch(function () {
                    btn.disabled = false;
                    status.textContent = 'Qualcosa non ha funzionato. Riprova tra poco.';
                });
        });
    });
})();
</script>
```

Nota progressive enhancement: senza JavaScript il form fa il POST nativo all'endpoint MailerLite in una nuova scheda (pagina di conferma di MailerLite). L'honeypot `website` blocca i bot solo nel percorso JS; il doppio opt-in filtra il resto.

- [ ] **Step 2: Includere il box in `_layouts/post.html`**

Con Edit, inserire PRIMA della riga `<!-- Sezione Commenti (self-hosted Cloudflare) -->`:

```html
    {% include newsletter-box.html %}

```

- [ ] **Step 3: Includere il box in `_layouts/home.html`**

Con Edit, inserire dopo `</section>` che chiude `.articles-section` e prima di `<script src="{{ '/assets/js/hero-tree.js' ...`:

```html
<!-- NEWSLETTER -->
<div class="rds-nl-home">
    {% include newsletter-box.html %}
</div>

```

- [ ] **Step 4: Aggiungere il CSS in fondo a `assets/css/style.css`**

```css
/* ===== Newsletter (MailerLite) ===== */
.rds-nl {
    background: #fff;
    border: 2px solid var(--crema-scuro);
    border-radius: 14px;
    padding: 1.8rem 1.6rem;
    margin: 2.5rem 0;
    box-shadow: 0 4px 14px var(--ombra);
}
.rds-nl-title {
    color: var(--rosso-primario);
    font-size: 1.3rem;
    margin-bottom: 0.4rem;
}
.rds-nl-text {
    color: var(--testo-chiaro);
    font-size: 0.95rem;
    margin-bottom: 1rem;
}
.rds-nl-row {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
}
.rds-nl-input {
    flex: 1 1 220px;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    font-family: inherit;
    color: var(--testo);
    background: var(--crema);
    border: 2px solid var(--crema-scuro);
    border-radius: 10px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.rds-nl-input:focus {
    outline: none;
    border-color: var(--rosso-accent);
    box-shadow: 0 0 0 3px rgba(194, 60, 60, 0.15);
}
.rds-nl-btn {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-family: inherit;
    font-weight: 600;
    color: #fff;
    background: var(--rosso-primario);
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: background 0.2s;
}
.rds-nl-btn:hover { background: var(--rosso-scuro); }
.rds-nl-btn:disabled { opacity: 0.6; cursor: default; }
.rds-nl-hp {
    position: absolute;
    left: -9999px;
    width: 0;
    height: 0;
    opacity: 0;
}
.rds-nl-status {
    min-height: 1.2em;
    margin: 0.6rem 0 0;
    font-size: 0.9rem;
    color: var(--testo-chiaro);
}
.rds-nl-home {
    max-width: 760px;
    margin: 0 auto;
    padding: 0 2rem 4rem;
}
```

- [ ] **Step 5: Build locale e verifica**

```bash
cd "/Users/ste/Desktop/Scrittura e Libri/Blog/rossodiserablog" && bundle exec jekyll build 2>&1 | tail -3
grep -c "rds-nl-form" _site/index.html
grep -c "rds-nl-form" _site/tecnica-feynman/index.html
```

Expected: build senza errori; `grep -c` = 1 sia in `_site/index.html` sia nella pagina di un post (il box c'è una volta sola per pagina).

- [ ] **Step 6: Test manuale locale (facoltativo ma raccomandato)**

`bundle exec jekyll serve`, aprire `http://localhost:4000`, verificare resa del box in home e in un articolo (desktop + viewport mobile con gli strumenti sviluppatore). NON iscriversi ancora: il test di iscrizione si fa in produzione al Task 7.

- [ ] **Step 7: Commit**

```bash
cd "/Users/ste/Desktop/Scrittura e Libri/Blog/rossodiserablog" && \
git add _includes/newsletter-box.html _layouts/post.html _layouts/home.html assets/css/style.css && \
git commit -m "Newsletter: box di iscrizione MailerLite in articoli e homepage

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: Deploy e test end-to-end

**Files:** nessuna modifica (solo push, verifiche e un'iscrizione di prova).

**Interfaces:**
- Consumes: GROUP_ID (Task 1), endpoint form (Task 5), sito deployato.
- Produces: newsletter verificata funzionante in produzione.

- [ ] **Step 1: Push e attesa deploy**

```bash
cd "/Users/ste/Desktop/Scrittura e Libri/Blog/rossodiserablog" && git push origin main
```

Attendere il workflow "Build and Deploy Jekyll Site" (2-3 minuti), poi:

```bash
curl -s https://rossodiserablog.it/ | grep -c "rds-nl-form"
```

Expected: `1`.

- [ ] **Step 2: Iscrizione di prova**

Stefano (o io via browser se disponibile): aprire un articolo su rossodiserablog.it, inserire `s.vozzi@gmail.com` nel box, cliccare Iscriviti. Expected: messaggio "Quasi fatto! Controlla la posta e clicca il link di conferma."

- [ ] **Step 3: Conferma doppio opt-in**

Stefano: aprire l'email "Conferma la tua iscrizione a Rosso di Sera" su s.vozzi@gmail.com e cliccare "Confermo l'iscrizione". Expected: pagina "Iscrizione confermata!".

- [ ] **Step 4: Verificare l'iscritto nel gruppo via API**

```bash
curl -s -H "Authorization: Bearer $MLTOKEN" -H "Accept: application/json" \
  "https://connect.mailerlite.com/api/groups/GROUP_ID/subscribers" | \
  python3 -c "import json,sys;print([(s['email'], s['status']) for s in json.load(sys.stdin)['data']])"
```

Expected: `[('s.vozzi@gmail.com', 'active')]`.

- [ ] **Step 5: Verifica finale DNS e mittente**

```bash
dig +short MX rossodiserablog.it @1.1.1.1
dig +short TXT rossodiserablog.it @1.1.1.1
dig +short TXT _dmarc.rossodiserablog.it @1.1.1.1
```

Expected: MX di Cloudflare presenti; UN solo record `v=spf1` con gli include di Cloudflare e MailerLite; DMARC presente. In dashboard MailerLite il dominio resta verde e il mittente predefinito è `newsletter@rossodiserablog.it`.

---

### Task 8: Documentazione: CLAUDE.md, credentials.yaml, memoria

**Files:**
- Modify: `CLAUDE.md` (sezione "In sospeso" e nuova sezione operativa)
- Modify: `~/.secrets/credentials.yaml` (sezione `mailerlite`, fuori repo)
- Modify: memoria persistente (`MEMORY.md` + nuovo file progetto)

**Interfaces:**
- Consumes: GROUP_ID, FORM_ID, endpoint, esiti dei task precedenti.

- [ ] **Step 1: Aggiornare CLAUDE.md**

1. Rimuovere da "## In sospeso" la voce "### Newsletter — account MailerLite disponibile (2026-08-02)".
2. Aggiungere (dopo la sezione "## Social Media — Buffer") una sezione:

```markdown
## Newsletter (MailerLite, attiva dal 2026-08-02)

- **Account**: s.vozzi@gmail.com (token API in credentials.yaml, sezione `mailerlite`).
- **Gruppo**: "Rosso di Sera Newsletter" (id in credentials.yaml, `newsletter_group_id`).
- **Form**: embedded "rosso-di-sera-signup"; il sito usa un form custom (`_includes/newsletter-box.html`, incluso in post.html e home.html, classi `rds-nl-*` in style.css) che invia all'endpoint pubblico del form. Doppio opt-in attivo, email di conferma in italiano.
- **Mittente**: `newsletter@rossodiserablog.it` (dominio autenticato: DKIM/SPF/DMARC su Cloudflare). Mai email personali come mittente.
- **Risposte**: Cloudflare Email Routing inoltra `newsletter@` a `scrivi.rossodisera@gmail.com`.
- **Campagne**: si creano e inviano dalla dashboard MailerLite (l'invio non è nel workflow di pubblicazione articoli).
- **Iscritti via API**: `GET https://connect.mailerlite.com/api/groups/<group_id>/subscribers` con Bearer token.
```

(Adattare i dettagli a ciò che è stato davvero fatto, inclusi eventuali fallback usati.)

- [ ] **Step 2: Aggiornare credentials.yaml (via Edit, file fuori repo)**

Nella sezione `mailerlite:` aggiungere:

```yaml
  newsletter_group_id: 'GROUP_ID'
  newsletter_form_id: 'FORM_ID'
  newsletter_form_endpoint: https://assets.mailerlite.com/jsonp/ACCOUNT_ID/forms/FORM_ID/subscribe
  newsletter_sender: newsletter@rossodiserablog.it
```

E aggiornare la `note:` esistente segnalando che l'account è ora operativo per Rosso di Sera.

- [ ] **Step 3: Aggiornare la memoria persistente**

Creare `/Users/ste/.claude/projects/-Users-ste-Desktop-Scrittura-e-Libri-Blog-rossodiserablog/memory/project_newsletter_mailerlite.md` con frontmatter (`type: project`) e il riassunto operativo (gruppo, mittente, inoltro, dove sono le chiavi), poi aggiungere la riga indice in `MEMORY.md`.

- [ ] **Step 4: Commit e push**

```bash
cd "/Users/ste/Desktop/Scrittura e Libri/Blog/rossodiserablog" && git add CLAUDE.md && \
git commit -m "Docs: newsletter MailerLite attiva, aggiornato CLAUDE.md

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" && git push origin main
```

Expected: push ok; il CI parte ma non tocca nulla di rilevante (CLAUDE.md non influisce sul build).
