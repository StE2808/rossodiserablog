# Newsletter MailerLite — Design

**Data**: 2026-08-02
**Stato**: approvato da Stefano (sessione 2026-08-02)
**Contesto**: attivazione della newsletter del blog con l'account MailerLite già esistente (creato 2026-07-08 per Aenigma Press, destinato a Rosso di Sera per decisione del 2026-08-02). Riferimento: CLAUDE.md, sezione "In sospeso → Newsletter".

## Decisioni prese

| Decisione | Scelta |
|---|---|
| Mittente | `newsletter@rossodiserablog.it` |
| Risposte dei lettori | Inoltro via Cloudflare Email Routing a `scrivi.rossodisera@gmail.com` |
| Posizione form | Fine articolo (prima dei commenti) + homepage (dopo la griglia post) |
| Opt-in | Doppio opt-in, email di conferma in italiano |
| Resti Aenigma Press | Eliminare gruppo "Aenigma Press Newsletter" e form "aenigmapress-signup" |
| Approccio form | Form HTML/CSS custom del sito che invia all'endpoint pubblico del form embedded MailerLite (no widget ufficiale, no Worker proxy) |

## Stato di partenza (rilevato 2026-08-02)

- **MailerLite**: 1 gruppo ("Aenigma Press Newsletter", 0 iscritti), 1 form embedded ("aenigmapress-signup"). Nessun sending domain configurato.
- **DNS `rossodiserablog.it` (Cloudflare)**: solo 2 CNAME verso `ste2808.github.io` (apex + www). Nessun MX, nessun SPF/TXT: il dominio non ha alcuna email, i record per MailerLite ed Email Routing si aggiungono senza conflitti.
- **Sito Jekyll**: nessun riferimento a newsletter in layout, include o asset.

## Architettura e flusso

```
Lettore → box newsletter (post.html / home.html)
       → POST endpoint pubblico form MailerLite (fetch; fallback POST nativo senza JS)
       → MailerLite invia email di conferma (doppio opt-in, in italiano)
       → click di conferma → iscritto nel gruppo "Rosso di Sera Newsletter"

Campagne: dashboard MailerLite, mittente newsletter@rossodiserablog.it
Risposte: newsletter@ → Cloudflare Email Routing → scrivi.rossodisera@gmail.com
```

## Componenti

### 1. MailerLite — via API (token in `~/.secrets/credentials.yaml`, sezione `mailerlite`)
- Creare il gruppo **"Rosso di Sera Newsletter"** (`POST /api/groups`).
- Eliminare il gruppo "Aenigma Press Newsletter" (`DELETE /api/groups/192421046673999305`).
- Eliminare il form "aenigmapress-signup" (`DELETE /api/forms/192421754859160744`); se l'API non lo consente, farlo in dashboard.

### 2. MailerLite — in dashboard (Stefano, guidato passo-passo)
Operazioni che l'API non espone:
1. Aggiungere il sending domain `rossodiserablog.it` (Settings → Domains) e passare i record DNS richiesti.
2. Attivare il doppio opt-in; tradurre in italiano email di conferma e pagina di ringraziamento.
3. Creare un form **embedded** "rosso-di-sera-signup" collegato al gruppo nuovo. Serve solo per ottenere l'endpoint di subscribe: la grafica sarà quella del sito. Passare lo snippet HTML generato.
4. A dominio verificato, impostare `newsletter@rossodiserablog.it` come mittente predefinito.

Vincolo dal CLAUDE.md: mai email personali come mittente; mai indirizzi email in chiaro nelle pagine del sito.

### 3. Cloudflare — via API (token `cloudflare.api_token`, zona `80d3b27200f3277db263f1d5aedae81a`)
- Inserire i record DKIM/SPF esattamente come richiesti dalla dashboard MailerLite, più un **DMARC base** (`_dmarc` TXT `v=DMARC1; p=none`): Gmail e Yahoo lo richiedono per i bulk sender.
- Attivare **Email Routing** sulla zona (aggiunge gli MX di Cloudflare; oggi non esistono MX, quindi nessun conflitto). Regola: `newsletter@rossodiserablog.it` → `scrivi.rossodisera@gmail.com`. La destinazione va verificata con un click dall'email che Cloudflare manda a quella Gmail.
- **Vincolo SPF**: un solo record SPF per l'apex. Se sia MailerLite sia Email Routing richiedono un include SPF, fondere in un unico TXT (es. `v=spf1 include:_spf.mx.cloudflare.net include:<include MailerLite> ~all`).

### 4. Sito Jekyll
- Nuovo **`_includes/newsletter-box.html`**: titolo, una riga di presentazione, campo email + bottone "Iscriviti", honeypot anti-bot, messaggi di stato in italiano (successo: "Controlla la posta per confermare l'iscrizione"; errore: invito a riprovare). Invio via fetch con progressive enhancement: senza JavaScript il form fa un POST nativo all'endpoint MailerLite (pagina di conferma MailerLite).
- Inclusione in **`_layouts/post.html`** (dopo il contenuto, prima del blocco commenti) e **`_layouts/home.html`** (dopo la griglia dei post e la paginazione, prima della fine del contenuto della pagina).
- CSS in `assets/css/style.css`, sezione dedicata (prefisso classi `rds-nl-`), palette e stile del sito, responsive.
- Riga di trasparenza sotto il form: "Niente spam, cancellazione con un click in ogni email." Il consenso GDPR è coperto dal doppio opt-in.
- Testi rivolti agli utenti tutti in italiano.

## Gestione errori

- Fetch fallito o endpoint irraggiungibile → messaggio di errore nel box, il form resta compilabile; in assenza di JS il POST nativo funziona comunque.
- Honeypot compilato → invio silenziosamente scartato lato client.
- Email non valida → validazione HTML5 (`type="email" required`) prima dell'invio.

## Test end-to-end

1. Record DNS verificati con `dig` + check verde nella dashboard MailerLite.
2. Iscrizione di prova dal sito → email di conferma ricevuta → click → iscritto presente nel gruppo (verifica via API).
3. Email di prova a `newsletter@rossodiserablog.it` → arriva su `scrivi.rossodisera@gmail.com`.
4. Box renderizzato correttamente su post e homepage, desktop e mobile.

## Fuori scope (v1)

- Automazione RSS-to-email (invio automatico a ogni nuovo post) — possibile evoluzione futura.
- Pagina `/newsletter/` dedicata e form nel footer.
- Contenuto e cadenza delle campagne.
- Migrazione iscritti (non ce ne sono).

## A fine lavoro

- Aggiornare il CLAUDE.md: rimuovere la voce da "In sospeso", aggiungere sezione operativa "Newsletter (MailerLite)" con gruppo, endpoint, record DNS e procedura campagne.
- Salvare in `credentials.yaml` eventuali nuovi identificativi (group id, form id) nella sezione `mailerlite`.
