# Albero hero in stile logo — Design

**Data**: 2026-06-10
**Stato**: approvato da Stefano (brainstorming con companion visivo, mockup v7)
**Mockup di riferimento**: `.superpowers/brainstorm/9658-1781071326/content/volo-uccellino-v7.html`

## Obiettivo

Sostituire l'albero stilizzato "a ventaglio" nell'hero della homepage con un albero che richiama quello del logo (`/assets/images/logo_trasparenza.png`): silhouette scura, tronco robusto che si biforca, rami organici asimmetrici, uccellino e linee d'orizzonte. Aggiungere la sequenza animata completa, che culmina con l'uccellino che vola dall'albero al logo nella navbar.

## Decisioni prese (e alternative scartate)

1. **Forma**: organica in stile logo, generata proceduralmente con seme fisso (mulberry32, seed 42, ricorsione a 9 livelli). Scartate: forma attuale con opacità maggiorata, variante dorata, variante con foglie.
2. **Trattamento**: silhouette scura `rgba(26,8,8,0.88)` come il logo, con uccellino in cima e 3 linee d'orizzonte alla base. Scartata: filigrana bianca traslucida con forma nuova.
3. **Animazione**: crescita progressiva ramo per ramo + volo finale dell'uccellino verso il logo. Scartate: dissolvenza sobria, uccellino che arriva in volo.

## Sequenza animata

| Tempo | Evento |
|-------|--------|
| 0–3 s | L'albero si disegna dal tronco verso le punte (stroke-dashoffset, ritardo per livello di profondità: `(9 - depth) * 280 + (i % 7) * 35` ms, durata 0.6 s per segmento) |
| ~2.4 s | Le 3 linee d'orizzonte si disegnano (ritardi 2400/2550/2700 ms, durata 0.9 s) |
| ~3.1 s | L'uccellino appare in dissolvenza sulla cima (0.7 s) |
| ~4.2 s | L'albero inizia a oscillare (rotate 0.8°, 5 s, infinito, origine alla base del tronco) |
| ~5.4 s | L'uccellino decolla: traiettoria ad arco verso il logo della navbar (2 s, Web Animations API); negli ultimi millimetri (offset 0.92→1) si rimpicciolisce rapidamente fino a scala 0 e sparisce "dentro" il logo |
| ~7.4 s | A fine volo (`onfinish`, fallback a 8.4 s) compaiono "Esplora gli articoli" (replay del suo fadeInUp) e l'indicatore "Scorri" (dissolvenza 0.9 s) — classe `hero-cta-pending` rimossa da `.hero`. Con reduced-motion o senza JS restano sempre visibili (aggiunta 2026-06-10 pomeriggio) |

## Requisiti vincolanti

- **Niente flash iniziale**: i path devono nascere già nascosti nel markup SVG (`pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"`), mai inseriti visibili e nascosti dopo. La scena parte vuota.
- **Orizzonte fermo**: le linee d'orizzonte stanno in un gruppo SVG separato (`<g class="horizon-g">`), fuori dal gruppo che oscilla.
- **Uccellino che svanisce**: il volo termina con scala 0 e opacità 0 sul bordo superiore del logo; l'uccellino NON resta appoggiato sul logo.
- **Testo hero più in alto**: l'intero blocco `.hero-content` (titolo, tagline e bottone "Esplora gli articoli") va posizionato al **40%** dell'altezza dell'hero (nel mockup: `top: 40%` con `translate(-50%, -50%)`), così non copre l'uccellino in cima all'albero. Nel CSS reale l'hero usa flex centering: sostituire con posizionamento equivalente al 40%.
- **Punto di atterraggio del volo**: calcolato a runtime dalle posizioni reali (cima dell'albero → centro-alto del cerchio del logo, `lRect.height * 0.13`), perché navbar e hero sono responsive.

## Architettura dell'implementazione

### File toccati

- `_layouts/home.html` — sostituire l'SVG `.hero-tree` attuale (70 path) con un contenitore vuoto `<div id="hero-tree-holder" class="hero-tree" aria-hidden="true">`; aggiungere il tag `<script defer>` per `hero-tree.js`.
- `assets/css/style.css` — rimuovere le ~75 regole di animazione attuali (`.tree-trunk`, `.branch-main-*`, `.branch-primary-*`, `.branch-secondary-*`, `.twig-*`, keyframes `grow-trunk`/`grow-branch`, `sway`); aggiungere le nuove regole (sway del solo gruppo albero, posizione testo hero al 40%, stile `.hero-flybird`, responsive).
- `assets/js/hero-tree.js` (nuovo) — genera l'SVG a runtime (stesso algoritmo dei mockup approvati, seed 42, deterministico) e orchestra la sequenza: avvio transizioni (doppio rAF), classe `swaying` a 4.2 s, volo dell'uccellino a 5.4 s con Web Animations API. Caricato con `defer` solo dalla homepage.

### Scelte tecniche

- **Generazione a runtime, non path statici** (deciso 2026-06-10 in fase di piano): l'albero approvato conta **1068 segmenti**; come markup statico peserebbe ~200KB di HTML sulla homepage. Il generatore deterministico (~2KB di JS, identico a quello dei mockup approvati) produce lo stesso identico albero nel browser. I path nascono già "nascosti" (`pathLength="1"`, `stroke-dasharray/offset: 1` nel markup generato), quindi nessun flash.
- **Animazione di crescita via transizioni CSS** con delay inline per segmento, come nei mockup.
- **`prefers-reduced-motion`**: se attivo, l'albero viene generato già completo (offset 0, nessuna transizione), niente oscillazione né volo; l'uccellino resta fermo sulla cima.
- **Fallback senza JS**: senza JavaScript l'albero non appare (l'hero mostra gradiente e testo). Accettato: è un elemento puramente decorativo e l'alternativa (markup statico) costa 200KB a ogni visitatore.
- **Responsive**: mantenere la regola esistente (albero ridotto su mobile, oggi 300px); il calcolo del volo a runtime assorbe le differenze di layout. Su mobile la navbar mostra comunque il logo, quindi il volo resta valido.

## Test / verifica

1. `bundle exec jekyll serve` → homepage: la scena parte vuota, nessun flash dell'albero completo (verificare con hard refresh e cache disabilitata).
2. Sequenza completa entro ~7.5 s; orizzonte immobile durante l'oscillazione.
3. L'uccellino sparisce esattamente sul logo a larghezze diverse (desktop, ~768px, mobile).
4. Con `prefers-reduced-motion` attivo: albero statico completo, nessun movimento.
5. Pagine non-home: nessun errore JS (lo script non deve girare dove l'albero non esiste).

## Fuori scope

- Nessuna modifica al logo, alla navbar o ad altre pagine.
- Nessuna modifica a colori/gradiente dell'hero.
- Il vecchio albero "a ventaglio" non viene conservato.
