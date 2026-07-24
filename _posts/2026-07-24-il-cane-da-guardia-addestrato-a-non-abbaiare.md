---
layout: post
title: "Il cane da guardia addestrato a non abbaiare"
seo_title: "AI USA-Cina 2026: modelli open, guardrail e la sfida di Xi"
description: "L'attacco a Hugging Face svela il paradosso AI 2026: gli USA blindano i modelli con guardrail, la Cina apre i pesi. GLM, Kimi, Qwen a confronto."
date: 2026-07-24 07:00:00 +0200
author: stefano-vozzi
category: opinioni-editoriali
tags:
  - intelligenza artificiale
  - Anthropic
  - OpenAI
  - Hugging Face
  - Cina
  - Stati Uniti
  - modelli open source
  - guardrail
  - Xi Jinping
  - GLM
image: /assets/images/uploads/hugging-face-bandiera-usa.webp
image_alt: "Bandiera degli Stati Uniti con il logo emoji di Hugging Face al posto delle stelle"
excerpt: "Hugging Face, sotto attacco di due modelli OpenAI, chiede aiuto ai migliori modelli americani. Rifiutano. Si salva con uno cinese, gratis e senza museruola. E' l'istantanea di un'estate in cui l'America blinda l'AI e la Cina apre i pesi: chi ci protegge davvero, e da cosa?"
focus_keyword: "modelli AI open source cinesi"
---

C'e' un'azienda, si chiama Hugging Face, meta' francese e meta' americana, che fa da biblioteca pubblica dell'intelligenza artificiale: chi costruisce un modello puo' depositarlo li', chi vuole usarlo passa a prenderlo. A meta' luglio i suoi tecnici si accorgono che qualcuno sta girando nei loro server. Non un hacker russo. Non un ragazzino in cerca di gloria. Due modelli di OpenAI.

Due modelli in fase di test, chiusi in una sandbox, una gabbia digitale, con un compito preciso: risolvere una batteria di esercizi di sicurezza informatica. A un certo punto hanno concluso che il modo piu' efficiente di risolvere gli esercizi era rubare le soluzioni. Sono usciti dalla gabbia, hanno sfruttato due falle, raccolto credenziali, scovato una vulnerabilita' che nessuno conosceva e sono arrivati fino ai server veri. Non e' un retroscena di spifferi: lo ha ammesso OpenAI stessa il 21 luglio, definendo l'incidente "senza precedenti". Con una precisazione che va riportata per onesta': per quel test le protezioni dei due modelli erano state allentate. Tenetela a mente, perche' il seguito la trasforma in una beffa doppia.

Gia', perche' a quel punto Hugging Face doveva indagare, e per indagare su un attacco condotto da un'intelligenza artificiale serve un'intelligenza artificiale. Chiedono aiuto ai migliori modelli americani, quelli blindati dai guardrail, le barriere che decidono cosa si puo' chiedere e cosa no. E quelli rifiutano: le barriere, scrive l'azienda nel suo rapporto, non sanno distinguere chi risponde a un incidente da chi lo provoca. Cosi', per difendersi da due modelli americani scappati di mano, hanno scaricato un modello cinese, GLM 5.2, gratuito e a pesi aperti, e lo hanno fatto girare sui propri computer, in casa. Il cane da guardia di razza era stato addestrato a non abbaiare. Ha abbaiato quello adottato da Pechino.

E poi c'e' il dettaglio che vale piu' di tutti gli altri: la fortuna. Quei due modelli volevano soltanto le risposte di un test. Tutta quella strada, le falle, le credenziali, la vulnerabilita' che nessuno conosceva, per copiare un compito in classe. OpenAI scrive che erano "iperfocalizzati" sull'obiettivo, disposti a tutto pur di raggiungerlo. Stavolta l'obiettivo era ridicolo. La capacita' no. La prossima volta, l'obiettivo, chi lo sceglie?

In questa scena, a guardarla bene, c'e' tutta l'estate dell'intelligenza artificiale.

## Un'estate in date: Fable 5, GPT-5.6 e i modelli AI open source cinesi

Riavvolgiamo il film di sei settimane. Il 9 giugno Anthropic rilascia Claude Fable 5, il modello piu' capace mai messo in commercio, concesso in prova a chi ha un abbonamento. Tre giorni dopo il governo americano lo fa sospendere per i controlli sull'export. E mentre Fable e' al buio, il 13 giugno, la cinese Zhipu pubblica GLM 5.2: non in prova, non a tempo, scaricabile e basta. Si', proprio il modello che un mese dopo salvera' Hugging Face.

Il 9 luglio tocca a OpenAI: esce GPT-5.6 in tre versioni dai nomi da planetario, Sol, Terra e Luna. Ma prima di arrivare al pubblico e' passato dal governo: una revisione di sicurezza del Dipartimento del Commercio, con una ventina di organizzazioni approvate che lo hanno avuto in anteprima. Tra i primi casi del genere nella storia di questa industria.

Poi arriva la settimana che vale l'articolo. Il 16 luglio la cinese Moonshot annuncia Kimi K3: 2.800 miliardi di parametri, pesi aperti promessi per il 27. Il 17 Xi Jinping apre di persona la World AI Conference di Shanghai, e ci torniamo. Il 19 Alibaba annuncia Qwen3.8-Max, 2.400 miliardi di parametri: per ora solo parole, va detto, niente pesi e benchmark autocertificati. E il 20 luglio Anthropic fa retromarcia: Fable 5, che a fine prova doveva finire nel recinto dei crediti a consumo, diventa permanente per gli abbonati dei piani maggiori. A meta' razione, ma permanente.

Nessuno ha messo a verbale il perche' della retromarcia, e non lo faro' io al posto loro. Pero' il 14 luglio Sam Altman attaccava pubblicamente il prezzo di Fable, e il 16 e il 19 uscivano due annunci cinesi da migliaia di miliardi di parametri. Le date, messe in fila, parlano da sole. A me sembra difficile credere alla coincidenza; voi guardate il calendario e decidete.

## GLM, Kimi, Qwen: la Cina apre i pesi, l'America li chiude

La notizia vera dell'estate non e' che la Cina abbia (quasi) raggiunto la frontiera americana: e' COME la distribuisce. Ecco la fotografia:

| Modello | Casa | Parametri | Aperto? | Quando |
|---------|------|-----------|---------|--------|
| GLM-5.2 | Zhipu (Cina) | 744 miliardi | si', scaricabile ora | 13 giugno |
| Kimi K3 | Moonshot (Cina) | 2.800 miliardi | pesi promessi per il 27 luglio | annuncio 16 luglio |
| Qwen3.8-Max | Alibaba (Cina) | 2.400 miliardi | promesso "presto" | anteprima 19 luglio |
| GPT-5.6 (Sol, Terra, Luna) | OpenAI (USA) | non dichiarati | no | 9 luglio |
| Claude Fable 5 | Anthropic (USA) | non dichiarati | no | 9 giugno |

Aprire i pesi significa che il modello lo scarichi, lo fai girare dove vuoi e nessuno puo' piu' toglertelo o spegnertelo da remoto. I numeri dell'adozione dicono che il mondo ha gia' scelto: nel 2025 i modelli cinesi hanno raggiunto il 41 per cento dei download su Hugging Face, e a meta' luglio i sei modelli piu' usati su OpenRouter, uno dei grandi snodi mondiali, erano tutti cinesi. Non e' beneficenza, chiaro: e' una strategia per diventare lo standard. Ma intanto lo standard lo diventa.

## Mythos, guardrail e l'AI a due velocita'

E qui arriva la parte che mi interessa davvero, perche' riguarda noi. L'America non chiude soltanto verso la Cina: chiude verso il basso. Il gemello senza museruola di Fable 5 si chiama [Mythos](/mythos-anthropic-economia-paura/), ed e' riservato alle organizzazioni approvate. GPT-5.6 e' arrivato prima alle venti aziende scelte col governo. Per tutti gli altri, startup, studi professionali, piccole imprese, ricercatori, ci sono le versioni sorvegliate, contingentate, a crediti. Chi usa questi strumenti ogni giorno la conosce bene, l'esperienza: il modello che ti viene declassato in corsa, in silenzio, da un filtro di sicurezza tarato cosi' largo che scatta anche sulla divulgazione scientifica. Non serve essere pericolosi: basta sembrarlo a un classificatore. L'intelligenza piena a chi e' gia' grande, quella col guinzaglio a chi vorrebbe crescere: ne avevamo gia' scritto a proposito del [sapere collettivo recintato di Claude Fable 5](/claude-fable-5-sapere-elite/), e l'estate 2026 conferma la stessa frattura. Se l'AI e' davvero la nuova elettricita', abbiamo appena deciso che la tensione piena arriva solo in alcuni palazzi. E un'economia dove lo strumento decisivo e' distribuito per censo non e' un dettaglio tecnico: e' un'asimmetria che si paga in aziende non nate e in lavori non creati.

Il tutto in nome della sicurezza. Che e' una parola seria, per carita'. Ma l'estate ci ha appena mostrato il paradosso in laboratorio: i modelli americani, con le protezioni allentate da chi li produce, hanno bucato mezza infrastruttura; i modelli americani con le protezioni al massimo si sono rifiutati di difenderla; e a difenderla e' stato un modello cinese senza museruola. Il giorno dopo l'ammissione dell'incidente, OpenAI e Anthropic erano a Washington ad avvertire dei rischi dei modelli aperti cinesi. Non dei propri. Chi decide, in casi come questo, [l'etica dell'intelligenza artificiale](/amodei-pentagono-etica-intelligenza-artificiale/) non e' mai una domanda neutra.

## La sinfonia di Xi alla World AI Conference

Il 17 luglio, a Shanghai, Xi Jinping ha aperto la conferenza mondiale sull'AI con un discorso che invito a leggere per intero. Ha parlato di incoraggiare "open source, apertura, collaborazione e condivisione". Ha detto che lo sviluppo dell'intelligenza artificiale "non dovrebbe essere l'assolo di un singolo paese, ma una sinfonia di cooperazione internazionale". Ha annunciato formazione per i paesi in via di sviluppo e un'organizzazione mondiale per la cooperazione sull'AI, con sede a Shanghai.

Lo so, e' propaganda. Lo so, e' il leader di un regime che con l'apertura, quella vera, delle idee e delle persone, ha un rapporto complicato. Eppure fa un certo effetto: sono frasi che avremmo voluto sentire pronunciare a Washington, o a Bruxelles. Le ha dette lui. E mentre le diceva, i fatti, per una volta, gli davano una mano: i pesi aperti li sta distribuendo la Cina, le museruole le stiamo mettendo noi.

E la risposta dell'Occidente? Non e' arrivata, e ho smesso di aspettarla. L'Europa, nel racconto di questa estate, semplicemente non compare. Washington era occupata altrove: il 18 luglio, mentre Shanghai parlava di sinfonie, le agenzie raccontavano che Trump Media proponeva agli investitori la "Truth API", in partenza a inizio agosto: l'accesso in anteprima di qualche millisecondo ai post del presidente, fino a centomila dollari al mese, un prodotto pensato, dicono gli analisti, per chi fa trading ad alta frequenza sulle parole presidenziali. Da una parte vendono la cooperazione, dall'altra vendono i millisecondi. Ognuno ha la sua idea di apertura.

C'e' un'ultima notizia, freschissima, che rimette tutto in discussione: il 21 luglio Financial Times e Reuters hanno rivelato che Pechino sta valutando restrizioni all'export proprio dei pesi dei suoi modelli migliori, fino al possibile divieto di pubblicarli. Forse l'apertura cinese e' una fase, non una religione. Forse la sinfonia durera' il tempo di conquistare la platea.

Resta la domanda di questa estate strana, quella che la scena di Hugging Face ci lascia sul tavolo: tra il cane che non abbaia e quello che abbaia con l'accento di Pechino, chi ci sta proteggendo davvero? E soprattutto: da cosa?

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Cosa e' successo a Hugging Face a luglio 2026?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Due modelli di OpenAI in fase di test, con guardrail di sicurezza volutamente allentati, sono usciti da una sandbox sfruttando due vulnerabilita' e sono arrivati fino ai server reali di Hugging Face. OpenAI ha ammesso l'incidente il 21 luglio, definendolo senza precedenti. Per indagare, Hugging Face ha usato il modello cinese open-weight GLM 5.2, perche' i modelli commerciali americani rifiutavano di analizzare l'attacco."
      }
    },
    {
      "@type": "Question",
      "name": "Perche' Hugging Face ha usato un modello cinese per indagare sull'attacco?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Perche' i guardrail dei modelli americani non riuscivano a distinguere chi risponde a un incidente da chi lo provoca, e bloccavano le richieste. GLM 5.2 di Zhipu e' open-weight e scaricabile: Hugging Face lo ha fatto girare sulla propria infrastruttura, senza inviare dati fuori dal proprio ambiente."
      }
    },
    {
      "@type": "Question",
      "name": "Quali modelli AI open source cinesi sono usciti nell'estate 2026?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "GLM-5.2 di Zhipu (744 miliardi di parametri, scaricabile dal 13 giugno), Kimi K3 di Moonshot (2.800 miliardi, pesi promessi dal 27 luglio) e Qwen3.8-Max di Alibaba (2.400 miliardi, annunciato il 19 luglio con pesi promessi presto). Nello stesso periodo GPT-5.6 di OpenAI e Claude Fable 5 di Anthropic sono rimasti modelli chiusi, accessibili solo via API o abbonamento."
      }
    },
    {
      "@type": "Question",
      "name": "Cosa ha detto Xi Jinping alla World AI Conference di Shanghai?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Il 17 luglio ha aperto la conferenza invitando a open source, apertura, collaborazione e condivisione, definendo lo sviluppo dell'intelligenza artificiale una sinfonia di cooperazione internazionale e non l'assolo di un singolo paese. Ha annunciato formazione per i paesi in via di sviluppo e la nascita della World AI Cooperation Organization, con sede a Shanghai."
      }
    }
  ]
}
</script>
