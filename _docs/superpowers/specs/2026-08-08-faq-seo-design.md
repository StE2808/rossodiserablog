# FAQ SEO: schema, struttura e domande cercabili

Data: 2026-08-08
Stato: design approvato, da implementare

## Perché

Le FAQ del blog sono nate come blocco GEO (JSON-LD FAQPage, obbligatorio su tutti gli articoli
2026) e sono state rese visibili in pagina il 2026-08-07 solo per gli articoli 2026. Le linee
guida Google per le FAQ richiedono quattro cose che oggi soddisfiamo solo in parte: testo del
JSON-LD identico al visibile, domande marcate come heading, domande che intercettano ricerche
reali, risposte brevi con link interni.

## Stato misurato (2026-08-08, su 244 post)

| Aspetto | Valore | Giudizio |
|---|---|---|
| Articoli con FAQPage JSON-LD | 123 | |
| ...senza testo visibile corrispondente | 49 (28 del 2025, 20 del 2023, 1 del 2024) | viola la regola del testo identico |
| Domande visibili | 259, tutte in grassetto | nessun heading |
| Lunghezza risposte | media 54 parole, mediana 52, 3 sopra le 80 | già in bolla |
| Link interni nelle risposte | 0 su 259 | assente |
| Domande auto-referenziali | 25 ("secondo l'articolo") | query che nessuno digita |

Le 49 FAQPage senza testo visibile sono il problema più grave: dichiarano a Google un contenuto
che in pagina non esiste. Meglio nessuna FAQ che una dichiarata e assente.

## Criteri di successo

1. Zero articoli con FAQPage JSON-LD privo del testo visibile corrispondente.
2. Tutte le FAQ visibili come menu a tendina, con la domanda in `<h3>` dentro il `<summary>`.
3. Zero domande auto-referenziali.
4. Rich Results Test valido su un campione dei tre casi (2026 già a posto, 2025 riparato, 2023 riparato).
5. Regole nuove scritte in `workflow_rossodisera.md` e `seo-geo-riferimento.md`.

I criteri 1, 2 e 3 sono verificabili da script; il 4 va verificato a mano dopo il deploy.

## Architettura

Un solo script, `_dev/faq_tool.py`, con quattro sottocomandi. La scelta di uno script invece del
lavoro a mano nasce dal volume (123 articoli) e dalle trappole già emerse nel batch del 2026-08-07,
documentate in CLAUDE.md: un duplicato creato da un criterio di riconoscimento troppo rigido e 26
file da ripulire da em-dash e virgolette curve.

| Comando | Funzione | Modifica i file |
|---|---|---|
| `audit` | Produce la tabella dello stato qui sopra | no |
| `to-accordion` | Converte le FAQ visibili da grassetto a `<details>` con `<h3>` nel `<summary>` | sì |
| `sync-visible` | Sui 49: estrae le coppie domanda/risposta dal JSON-LD e le scrive in pagina, già in accordion | sì |
| `verify` | Confronta visibile e JSON-LD, exit 1 al primo mismatch | no |

`verify` è il guardiano: gira dopo ogni comando che scrive e prima di ogni commit.

Nota sull'ordine: `to-accordion` agisce solo sui 74 articoli che hanno già le FAQ visibili in
grassetto. I 49 riparati da `sync-visible` nascono direttamente in formato accordion, quindi non
vanno ripassati.

### Regole di robustezza

Derivano tutte da errori già commessi, non sono precauzioni teoriche.

- Riconoscimento della sezione FAQ con regex `^##\s*domande` case-insensitive, mai per stringa
  esatta. Alcuni articoli usano "Domande e risposte", e alcuni H2 narrativi contengono la parola
  "domanda" senza essere FAQ.
- Scrittura sempre via Python con `open(path, 'w', encoding='utf-8')`. Mai il tool Edit: introduce
  smart quotes che rompono Jekyll.
- JSON-LD parsato con `json.loads(..., strict=False)`: alcuni blocchi contengono newline grezzi.
- Normalizzazione di em-dash e virgolette curve sul testo estratto, applicata in coppia al JSON-LD
  e al visibile per non spezzare la corrispondenza.
- `sync-visible` è verbatim: il testo esiste già nel JSON-LD, lo stiamo solo rendendo visibile.
  Zero contenuto nuovo in questa fase, coerente col guardrail "niente dati inventati".

## Formato scelto: menu a tendina

Le FAQ sono rese come fisarmonica, formato esplicitamente valido per Google (il testo dentro un
accordion è considerato in chiaro). Verificato con kramdown 2.5.2 il 2026-08-08:

```html
<details class="faq-item" markdown="1">
<summary><h3>Domanda?</h3></summary>

Risposta in markdown, link interni compresi.

</details>
```

Esiti del test di rendering:

- `markdown="1"` fa processare il contenuto come markdown: corsivi, grassetti e link interni
  funzionano dentro il `details`.
- L'`<h3>` dentro il `<summary>` viene emesso intatto, quindi accordion e heading coesistono e
  soddisfiamo entrambi i punti della guida Google.
- Kramdown converte gli apostrofi dritti in curvi nel rendering HTML. La corrispondenza col
  JSON-LD è quindi semantica e non byte a byte. Vale già oggi per le FAQ in grassetto degli
  articoli 2026, che risultano valide, quindi non è un ostacolo.

Serve una regola CSS per `.faq-item` in `style.css`: l'`h3` dentro il `summary` è display block e
manderebbe a capo l'indicatore di apertura.

## Le 25 domande auto-referenziali

Sono domande scritte per chi ha appena letto il pezzo, non per chi cerca: "Qual è la conclusione
dell'articolo sull'accumulo patologico?". Vanno riscritte come query plausibili, per esempio
"Perché l'accumulo di ricchezza estrema è un problema economico?".

Vincolo: la riscrittura tocca entrambe le copie, JSON-LD e visibile, nella stessa operazione.
Cambiare solo una delle due romperebbe la regola d'oro proprio mentre cerchiamo di rispettarla.
Cambia la formulazione della domanda; la risposta resta identica.

## Link interni nelle risposte

Un link markdown `[ancora](/slug/)` nel testo visibile non rompe la corrispondenza col JSON-LD:
Google confronta il testo, non il markup, e l'anchor text resta parte della frase. Condizione
necessaria: l'ancora deve essere composta da parole già presenti nella risposta, mai aggiunte.

Applicazione opportunistica sui 25 articoli già toccati per la riscrittura delle domande, più
regola per gli articoli futuri. Nessuna passata dedicata sui 259: sarebbe scope creep, e il
lavoro di internal linking ha già un suo filone aperto.

## Ordine di esecuzione

1. `audit` e sviluppo dello script, più la regola CSS `.faq-item`.
2. Pilota: `to-accordion` su un solo articolo, push, verifica in produzione. Jekyll non è
   installato in locale (c'è solo il Ruby di sistema 2.6, senza le gem), quindi il rendering reale
   si vede solo dopo il deploy: il pilota sostituisce il build locale come rete di sicurezza.
3. `to-accordion` sui restanti 73 articoli con FAQ visibile.
4. `sync-visible` sui 49 articoli.
5. `verify` a zero mismatch, poi push, attendendo che il run GitHub Actions risulti `completed`.
   Verificare con curl che l'URL risponda 200 non basta: il sito resta online con la versione
   vecchia per tutta la build.
6. Rich Results Test su tre URL, uno per anno.
7. Riscrittura delle 25 domande, in coppia JSON-LD più visibile, con revisione prima del commit.
8. Aggiornamento di `workflow_rossodisera.md`, `seo-geo-riferimento.md` e `CLAUDE.md`.

## Fase in coda: batch data-driven su Search Console

Quando Search Console torna interrogabile, riscrivere le domande degli articoli che hanno
impression reali, dove il guadagno esiste. Sul resto del corpus sarebbe lavoro a vuoto: su un
dominio nato a fine dicembre 2025 l'on-page pesa circa il 15 per cento (regola 85/15).

Bug trovato il 2026-08-08: il `config.toml` del CLI conteneva un campo `auth_header` con un access
token scaduto, iniettato a mano, che aveva la precedenza sui token freschi e causava HTTP 401 anche
subito dopo un login riuscito. Campo rimosso, backup in `config.toml.bak`. Se il 401 si ripresenta
dopo una re-iniezione da credentials.yaml, controllare per prima cosa quel campo.

## Fuori scope

- Ancore linkabili sulle singole domande: kramdown non genera gli id automatici sugli heading
  scritti come HTML raw dentro il `summary`. Recuperabili in futuro scrivendo l'id a mano.
- Aggiunta di FAQPage agli articoli che non ce l'hanno (121 post, soprattutto 2024 e 2023): è il
  batch GEO arretrato, ha una sua pianificazione.
- Riscrittura delle domande non auto-referenziali fuori dal perimetro data-driven.
