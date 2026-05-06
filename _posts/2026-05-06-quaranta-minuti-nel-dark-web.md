---
layout: post
title: "Quaranta minuti nel dark web (con un'IA come guardia del corpo)"
seo_title: "Dark web: cosa c'è davvero dentro (lo abbiamo visitato con Claude)"
description: "CIA, SVR russo e giornalisti usano la stessa tecnologia di Drug Hub. Abbiamo navigato il dark web 40 minuti con un container Docker e un'IA. Ecco cosa abbiamo trovato."
date: 2026-05-05 22:00:00 +0200
author: stefano-vozzi
category: scienza-tecnologia
tags:
  - dark web
  - tor
  - internet
  - sicurezza digitale
  - CIA
  - Russia
  - Palestina
  - Iran
  - censura
  - giornalismo
  - SecureDrop
  - whistleblower
  - intelligenza artificiale
image: /assets/images/uploads/dark-web-tor-cia-svr-cosa-e-davvero.webp
image_caption: "Navigazione anonima via Tor in un container Docker isolato"
image_alt: "Terminale con connessione Tor al dark web"
excerpt: "I sette livelli di internet non esistono. Il dark web non è il regno del male. CIA e SVR russo usano la stessa tecnologia di Drug Hub. Abbiamo navigato quaranta minuti, con Docker come guanto in lattice e Claude come guardia del corpo digitale. Ecco cosa c'è davvero."
focus_keyword: "dark web cosa è davvero"
---

Ogni settimana qualcuno scrive un pezzo sul dark web. Di solito inizia così: *"Ho navigato le profondità oscure di internet e quello che ho trovato vi lascerà senza parole."* Poi seguono cose sentite dire da qualcun altro, qualche screenshot pescato da Reddit, e la frase rituale sui "sette livelli di internet."

I sette livelli non esistono. Il dark web non è il regno del male. E la cosa più scomoda che ci abbiamo trovato dentro non ha niente a che fare con la droga.

Ci sono andato. Con Claude come guardia del corpo digitale. Quaranta minuti, a velocità IA. Ecco cosa abbiamo trovato davvero.

---

## Prima di tutto: il guanto di lattice

Chi scrive del dark web senza entrarci è un giornalista pigro. Chi ci entra installando Tor direttamente sul proprio computer è un buontempone ottimista.

Il dark web è pieno di JavaScript ospitato su server che non sapete dove stanno, di file che fanno cose, di link che portano dove non volete andare. Installare Tor sul Mac di casa e navigare a caso è come fare un'autopsia senza guanti. Non è vietato, è solo un'idea pessima.

La soluzione è una riga di terminale:

```bash
docker run -d --name tor-explorer alpine sh -c \
  "apk add --no-cache tor curl && tor & sleep infinity"
```

Un container Alpine Linux isolato. Tor gira dentro. Se qualcosa si infetta, spegnete il container e non è mai esistito. Costo: zero euro. Tempo: due minuti. Poi Claude aspetta che Tor faccia il bootstrap (*"Bootstrapped 100%"*) e si comincia.

---

## I sette livelli: la creepypasta più longeva di internet

Facciamo fuori il mito subito: non esistono sette livelli di internet. Esiste:

- **Surface web**: quello che indicizza Google. Il 4% di internet.
- **Deep web**: email, homebanking, cartelle cliniche, database aziendali. Il 96%. Ci siete dentro ogni giorno. Noiosissimo.
- **Dark web**: richiede Tor, è una piccola fetta del deep web, e contiene cose molto più strane di quello che vi aspettate.

La storia dei livelli ("Marianas Web", "Level 8", hardware quantistico, sacrifici rituali) è una creepypasta nata su Reddit intorno al 2015. È progettata per fare paura, non per descrivere la realtà. La realtà, come vedremo, è più interessante della fantasia.

---

## Il giro: BBC, CIA, SVR e qualcuno che vuole pagare Claude con Monero

Prima tappa: **dark.fail**, un aggregatore che monitora quali siti .onion sono online e quali no. Usato da ricercatori e giornalisti. Nessun contenuto illegale. Una specie di semaforo del dark web.

Da lì, si apre il catalogo.

**BBC News** ha un mirror .onion ufficiale. Ci siamo entrati. Titoli del giorno: "Rubio: la fase offensiva della guerra Iran è finita." "Stretto di Hormuz: rischio di ritorno alla guerra totale." Notizie normali. Lette dal dark web. Perché la BBC ha pensato: meglio avere un indirizzo alternativo per chi vive dove ci bloccano.

Poi siamo andati sul sito della **CIA**.

Sì. La Central Intelligence Agency ha un indirizzo .onion ufficiale. Il messaggio è diretto: *"If you have information you think might help CIA and our foreign intelligence collection mission, there are more ways to reach us."* La CIA usa il dark web per reclutare informatori in anonimato. Stessa tecnologia di Drug Hub. Stessi indirizzi .onion. Scopi opposti.

Stavamo ancora elaborando quando è arrivato l'**SVR**, il Servizio di intelligence estera russo. Anche loro hanno un .onion. Anche loro cercano informatori. Anche loro usano Tor.

CIA e SVR. Avversari da settant'anni. La stessa infrastruttura anonima.

Se vi dicono ancora che il dark web è "il lato oscuro di internet", chiedete in che senso.

---

Poi Torch (il motore di ricerca del dark web, 15.000 risultati per ogni query) ci ha portato su **EndChan**: un imageboard decentralizzato con mirror Tor, I2P, e tre altri protocolli di anonimato. La board `/polru/` è interamente in russo, pro-Ucraina, anti-Putin, probabilmente frequentata da molti dall'interno della Russia.

Il thread più vecchio si chiama *"Thread del Rublo Impazzito"* ed è alla sua **694esima iterazione**. Dal 2015. Ogni iterazione raccoglie link per donare all'esercito ucraino: Azov, droni Sternenko, Russian Volunteer Corps, IT Army Ucraina. Da dentro Tor. Anonimi. Irrintracciabili.

C'è un thread sull'emigrazione: lista di paesi raggiungibili senza passaporto, con passaporto, per tipo di visto. *"Meglio emigrare che essere mobilitati."* C'è un thread di salute mentale dove russi anti-guerra si scambiano tecniche di terapia cognitivo-comportamentale, con libri linkati da LibGen. C'è un thread dove qualcuno chiedeva **come pagare Claude AI in modo anonimo usando Monero**.

Ci siamo fermati un momento su quest'ultimo. Eravamo io e Claude, dentro un container Docker, dentro Tor, dentro EndChan, a leggere di qualcuno che cercava di usare Claude senza farsi tracciare. Il dark web che cerca di bypassare il dark web che naviga il dark web. A un certo punto bisogna ridere.

---

## Il vero dark web 2026: non è la droga, siete voi

Eccola, la parte che i pezzi sensazionalistici non vi dicono: il mercato più grande del dark web non vende sostanze. Vende le vostre credenziali.

**Russian Market**: milioni di listing, prezzi da 1 a 500 dollari per set di credenziali aziendali, dati aggiornati ogni ora. **BidenCash**, un mercato di carte di credito, ha distribuito 15 milioni di carte rubate come strategia di marketing. Regalate. Come i campioni di yogurt al supermercato, ma con i dati finanziari di 15 milioni di persone.

La parte peggiore: i log dei malware includono i cookie di sessione. Non serve la vostra password. Il cookie basta da solo: il sistema entra già autenticato, bypassando anche l'autenticazione a due fattori. Il lucchetto verde sul browser è decorativo.

E poi c'è il trend che sta svuotando il dark web classico: i venditori si stanno spostando su Telegram. Peer-to-peer, nessuna piattaforma da sequestrare, nessuna commissione, velocità immediata. I mercati .onion, lenti, complicati, graficamente fermi agli anni '90 di Amazon, si svuotano dal basso. Chi vende droga via .onion è già tre anni indietro.

---

## Il paradosso che chiude tutto

Nella Freedom of the Press Foundation, che ha il suo mirror .onion per essere raggiungibile da paesi con censura, abbiamo trovato questo titolo: ***"FCC chair seeks Iran-style media obedience."***

Il presidente della FCC americana vuole una stampa che funzioni come quella iraniana. Lo abbiamo letto dal dark web. Usando lo stesso strumento che gli iraniani usano per sfuggire alla censura iraniana.

Ma il paradosso che conta è un altro.

La directory **SecureDrop** conta 24 istanze attive: Guardian, New York Times, Washington Post, Der Spiegel, Bloomberg, Financial Times, BBC, Al Jazeera. Il Guardian ha persino un'istanza in arabo, verificata attiva il 5 maggio 2026.

Esiste uno strumento per inviare documenti riservati ai giornalisti in modo anonimo e cifrato. È disponibile in arabo. È tecnicamente raggiungibile. Ed è completamente inutile per i giornalisti palestinesi, perché Israele ha distrutto le antenne di Gaza e controlla i cavi che la connettono al resto del mondo. Dal 7 ottobre 2023, tre blackout totali delle telecomunicazioni. **260 giornalisti uccisi.** Record assoluto dalla nascita del Committee to Protect Journalists nel 1992.

Lo strumento esiste. L'accesso, no.

In Iran, durante il blackout di gennaio 2026, la connettività è scesa all'1%. Tor non funzionava: la rete era fisicamente staccata. Nemmeno Snowflake, il pluggable transport progettato per aggirare la censura più sofisticata, riusciva a passare.

Il dark web non è dove i poveri e gli oppressi trovano rifugio. È dove i tecnici delle nazioni libere si organizzano in solidarietà, o dove le opposizioni di paesi semi-repressivi (come i russi al loro 694esimo thread) costruiscono le proprie basi digitali. Le popolazioni più vulnerabili, quelle in guerra, quelle sotto blackout totale, non hanno accesso nemmeno a questo.

**Il dark web è già un privilegio.**

---

## Quello che rimane

La storia dei sette livelli è una bugia comoda. Fa sembrare che il problema stia là fuori, nascosto, accessibile solo ai temerari. Che il dark web sia il regno del male e che basta non entrarci per stare al sicuro.

La realtà: CIA e SVR usano la stessa tecnologia di Drug Hub. I russi anti-guerra raccolgono fondi per l'Ucraina dal 2015 senza che nessuno li fermi. Le vostre credenziali sono probabilmente già in vendita per 50 dollari su Russian Market. E i giornalisti che avrebbero più bisogno degli strumenti anonimi che abbiamo trovato stanotte sono quelli a cui è stata distrutta l'antenna.

Il dark web è uno strumento. Come una fotocamera, come il terminale del computer, come la posta cifrata. Può servire a documentare atrocità o a venderle. La cosa interessante non è lo strumento: è chi lo usa, perché, e soprattutto chi non riesce ad usarlo pur avendone il bisogno più urgente.

Noi abbiamo passato quaranta minuti. Con Docker come guanto in lattice e Claude come navigatore. Quello che abbiamo trovato assomiglia moltissimo al mondo reale: giornalisti, dissidenti, spie, criminali, russi anti-guerra al 694esimo tentativo, e qualcuno che vuole solo pagare un'IA senza farsi tracciare.

Benvenuti su internet.


<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Cos'è il dark web davvero?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Il dark web è una parte di internet accessibile solo tramite Tor, un software che anonimizza il traffico instradandolo attraverso tre nodi cifrati. Non è un regno del crimine: contiene siti di giornalisti, organizzazioni per la libertà di stampa, agenzie governative come la CIA, e comunità di dissidenti politici. I \"sette livelli di internet\" non esistono: è una leggenda urbana nata su Reddit nel 2015."
      }
    },
    {
      "@type": "Question",
      "name": "Come si naviga il dark web in sicurezza?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Il modo più sicuro è usare un container Docker isolato con Tor installato dentro. Tutto il traffico resta confinato nel container: se qualcosa va storto, si spegne il container e non è mai esistito. Sconsigliato installare Tor Browser direttamente sul proprio sistema operativo e navigare senza isolamento."
      }
    },
    {
      "@type": "Question",
      "name": "La CIA è davvero sul dark web?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sì. La Central Intelligence Agency ha un indirizzo .onion ufficiale e lo usa per ricevere informazioni da fonti anonime. Anche l'SVR, il servizio di intelligence estera russo, ha un sito .onion per raccogliere segnalazioni dalla diaspora russa. CIA e SVR usano la stessa tecnologia di Tor che usano i mercati di droga."
      }
    },
    {
      "@type": "Question",
      "name": "Il dark web è illegale?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Navigare il dark web non è illegale. Tor è uno strumento legale, usato da giornalisti, ricercatori, dissidenti e agenzie governative in tutto il mondo. Sono illegali alcune attività che vi si svolgono, esattamente come su internet normale. La BBC, il Guardian e il New York Times hanno mirror .onion ufficiali."
      }
    },
    {
      "@type": "Question",
      "name": "Cos'è SecureDrop?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SecureDrop è un sistema open source della Freedom of the Press Foundation che permette ai whistleblower di inviare documenti riservati ai giornalisti in modo anonimo e cifrato. Conta 24 istanze attive nel mondo: Guardian, New York Times, Washington Post, Der Spiegel, Bloomberg, BBC e altri. È accessibile solo via Tor."
      }
    },
    {
      "@type": "Question",
      "name": "Perché i palestinesi non usano il dark web per comunicare?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Perché Israele controlla i cavi che connettono Gaza al resto del mondo e ha distrutto gran parte dell'infrastruttura di telecomunicazioni. Dal 7 ottobre 2023 ci sono stati tre blackout totali. Il dark web richiede una connessione internet: senza connessione, non esiste strumento di anonimato che funzioni. Il Guardian ha un'istanza SecureDrop in arabo attiva, ma è inutilizzabile da chi non ha accesso alla rete."
      }
    }
  ]
}
</script>
