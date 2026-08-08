#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manutenzione delle FAQ dei post.

Sottocomandi:
  audit         stampa lo stato delle FAQ su tutto il corpus
  to-accordion  converte le FAQ visibili dal grassetto al menu a tendina
  sync-visible  rende visibile il testo che esiste solo nel JSON-LD
  verify        confronta JSON-LD e testo visibile, esce 1 se qualcosa non combacia

I file dei post vengono sempre riscritti in UTF-8 esplicito: il tool Edit
introduce smart quotes che rompono Jekyll.
"""

import argparse
import json
import re
import sys
from pathlib import Path

POSTS_DIR = Path(__file__).resolve().parent.parent / "_posts"

FAQ_H2 = re.compile(r"^##\s*domande.*$", re.IGNORECASE | re.MULTILINE)
SCRIPT_BLOCK = re.compile(
    r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE)
BOLD_Q = re.compile(r"^\*\*(.+?)\*\*\s*$", re.MULTILINE)
SUMMARY_Q = re.compile(r"<summary><h3>(.*?)</h3></summary>", re.DOTALL)
MD_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
MD_EMPHASIS = re.compile(r"(\*{1,2})(.+?)\1")

INVISIBLE = dict.fromkeys(map(ord, "​‌‍﻿"), None)
QUOTES = {"“": '"', "”": '"', "‘": "'", "’": "'"}


class FaqJsonError(ValueError):
    """JSON-LD della FAQPage malformato: va segnalato, non fatto esplodere."""


def normalize(s):
    """Riduce il testo alla sua forma confrontabile.

    Toglie la sintassi markdown (link ed enfasi) e uniforma virgolette curve e
    caratteri invisibili: il testo visibile puo' contenere markup che nel
    JSON-LD non c'e', pur essendo lo stesso testo agli occhi di Google.
    """
    s = MD_LINK.sub(r"\1", s)
    s = MD_EMPHASIS.sub(r"\2", s)
    for bad, good in QUOTES.items():
        s = s.replace(bad, good)
    s = s.translate(INVISIBLE)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def find_faq_section(text):
    """Restituisce (start, end) della sezione FAQ visibile, o None se assente.

    Il criterio e' l'H2 che *inizia* con "domande": cercare la sola parola
    darebbe falsi positivi sugli H2 narrativi tipo "La domanda difficile".
    """
    m = FAQ_H2.search(text)
    if not m:
        return None
    start = m.start()
    after_heading = m.end()
    stop = re.search(r"^<script|^##\s", text[after_heading:], re.IGNORECASE | re.MULTILINE)
    end = after_heading + stop.start() if stop else len(text)
    return start, end


def parse_jsonld(text):
    """Estrae le coppie domanda/risposta dal blocco FAQPage, o None se assente."""
    for m in SCRIPT_BLOCK.finditer(text):
        raw = m.group(1).strip()
        if "FAQPage" not in raw:
            continue
        try:
            data = json.loads(raw, strict=False)
        except json.JSONDecodeError as e:
            raise FaqJsonError("JSON-LD malformato ({})".format(e))
        return [{"q": normalize(item["name"]),
                 "a": normalize(item["acceptedAnswer"]["text"])}
                for item in data.get("mainEntity", [])]
    return None


def _pair(question, answer):
    """Costruisce una coppia con forma confrontabile e forma da riscrivere."""
    return {"q": normalize(question), "a": normalize(answer),
            "q_raw": _collapse(question), "a_raw": _collapse(answer)}


def _collapse(s):
    """Ricompone il testo su una riga sola senza toccarne il markup."""
    return re.sub(r"\s+", " ", s).strip()


def _parse_bold(block):
    """Estrae le coppie dal formato grassetto.

    Ogni coppia porta sia la forma normalizzata (per il confronto) sia quella
    grezza (per la riscrittura): normalize() spoglia link e corsivi, che nel
    testo visibile vanno invece conservati.
    """
    pairs = []
    marks = list(BOLD_Q.finditer(block))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(block)
        pairs.append(_pair(m.group(1), block[m.end():end]))
    return pairs


def _parse_accordion(block):
    pairs = []
    for chunk in block.split("<details")[1:]:
        qm = SUMMARY_Q.search(chunk)
        if not qm:
            continue
        answer = chunk[qm.end():].split("</details>")[0]
        pairs.append(_pair(qm.group(1), answer))
    return pairs


def parse_visible(text):
    """Estrae le coppie domanda/risposta dal testo visibile, in entrambi i formati."""
    span = find_faq_section(text)
    if not span:
        return []
    block = text[span[0]:span[1]]
    return _parse_accordion(block) if "<summary>" in block else _parse_bold(block)


def render_accordion(pairs, heading="## Domande frequenti"):
    """Costruisce il blocco FAQ come menu a tendina."""
    out = [heading.rstrip(), ""]
    for pair in pairs:
        domanda = pair.get("q_raw") or pair["q"]
        risposta = pair.get("a_raw") or pair["a"]
        out += ['<details class="faq-item" markdown="1">',
                '<summary><h3>{}</h3></summary>'.format(domanda),
                "", risposta, "", "</details>", ""]
    return "\n".join(out).rstrip() + "\n"


def to_accordion(text):
    """Converte la sezione FAQ visibile dal formato grassetto al menu a tendina."""
    span = find_faq_section(text)
    if not span:
        return text
    block = text[span[0]:span[1]]
    if "<summary>" in block:
        return text
    pairs = _parse_bold(block)
    if not pairs:
        return text
    heading = FAQ_H2.search(text).group(0)
    return text[:span[0]] + render_accordion(pairs, heading) + "\n" + text[span[1]:].lstrip("\n")


def sync_visible(text):
    """Rende visibile, verbatim, il testo che esiste gia' nel JSON-LD."""
    pairs = parse_jsonld(text)
    if not pairs or find_faq_section(text):
        return text
    target = next((m for m in SCRIPT_BLOCK.finditer(text) if "FAQPage" in m.group(1)), None)
    if not target:
        return text
    return (text[:target.start()].rstrip("\n") + "\n\n"
            + render_accordion(pairs) + "\n" + text[target.start():])


def compare(text):
    """Confronta JSON-LD e testo visibile. Restituisce la lista dei problemi."""
    try:
        jsonld = parse_jsonld(text)
    except FaqJsonError as e:
        return [str(e)]
    if jsonld is None:
        return []
    visible = parse_visible(text)
    if not visible:
        return ["manca il testo visibile della FAQPage"]
    if len(jsonld) != len(visible):
        return ["conteggio diverso: {} nel JSON-LD, {} visibili".format(len(jsonld), len(visible))]
    problemi = []
    for i, (j, v) in enumerate(zip(jsonld, visible), start=1):
        if j["q"] != v["q"]:
            problemi.append("domanda {} diversa: JSON-LD {!r} contro visibile {!r}".format(i, j["q"], v["q"]))
        if j["a"] != v["a"]:
            problemi.append("risposta {} diversa: JSON-LD {!r} contro visibile {!r}".format(i, j["a"][:60], v["a"][:60]))
    return problemi


# "articolo 33 della Costituzione" parla di una norma, non del pezzo: va esclusa
ARTICOLO_NORMA = re.compile(r"articol[oi]\s+(\d|[IVX]+\b|della costituzione)", re.IGNORECASE)
SELF_REF = re.compile(r"\barticol[oi]\b|nel pezzo|secondo l'autore", re.IGNORECASE)


def is_self_referential(question):
    """Vero se la domanda rimanda al pezzo invece di stare in piedi da sola."""
    if ARTICOLO_NORMA.search(question):
        return False
    return bool(SELF_REF.search(question))


# --- guardia sulla conservazione dei fatti ---
#
# Riscrivere una risposta a mano puo' far cadere per distrazione un dato, una
# data o un nome. La guardia estrae da ogni risposta l'insieme dei suoi fatti
# verificabili e controlla che la riscrittura non ne perda nessuno.

NUMERO = re.compile(r"\d+(?:[.,]\d+)*\s*%?")
NOME_PROPRIO = re.compile(r"\b[A-ZÀ-ÖØ-Ý][A-Za-zÀ-ÿ'’]{2,}")
CIT_APICE = re.compile(r"(?<![A-Za-zÀ-ÿ])['’]([^'’]{4,})['’](?![A-Za-zÀ-ÿ])")
CIT_DOPPIA = re.compile(r"[\"«]([^\"»]{4,})[\"»]")
PAROLA = re.compile(r"[\wÀ-ÿ'’]+")
ELISIONE = re.compile(r"^\w{1,2}['’]")

# Numeri scritti in lettere: "un ciclo in sei fasi" e' un fatto quanto "6 fasi".
NUMERALI = {"due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove",
            "dieci", "undici", "dodici", "tredici", "quattordici", "quindici",
            "sedici", "diciassette", "diciotto", "diciannove", "venti", "trenta",
            "quaranta", "cinquanta", "sessanta", "cento", "mille", "milioni",
            "miliardi", "decine", "centinaia", "migliaia"}

# Parole che capitano maiuscole a inizio frase senza essere nomi propri, piu' i
# termini auto-referenziali che la riscrittura deve proprio poter togliere.
STOP_MAIUSCOLE = {
    "articolo", "articoli", "autore", "pezzo", "testo",
    "che", "chi", "come", "cosa", "quando", "quanto", "quale", "quali", "perche",
    "perché", "dove", "mentre", "secondo", "ogni", "ogni", "anche", "ancora",
    "sono", "erano", "sarebbe", "essere", "stato", "stata", "state", "stati",
    "questo", "questa", "questi", "queste", "quello", "quella", "quelli",
    "quelle", "loro", "suoi", "sue", "nel", "nella", "nelle", "nei", "negli",
    "del", "della", "delle", "dei", "degli", "dal", "dalla", "dalle", "dai",
    "con", "senza", "per", "tra", "fra", "sopra", "sotto", "dopo", "prima",
    "poi", "quindi", "infine", "invece", "oppure", "ma", "però", "pero",
    "non", "più", "piu", "meno", "molto", "poco", "tutto", "tutta", "tutti",
    "tutte", "entrambi", "entrambe", "altro", "altra", "altri", "altre",
    "una", "uno", "gli", "gli", "gli", "lui", "lei", "essi", "esse",
    "oggi", "ieri", "domani", "sempre", "mai", "già", "gia", "solo", "soltanto",
    "come", "così", "cosi", "tanto", "forse", "davvero", "proprio", "vero",
    "esiste", "esistono", "serve", "servono", "resta", "restano", "rimane",
    "significa", "vuol", "dire", "fare", "avere", "può", "puo", "possono",
    "deve", "devono", "viene", "vengono", "hanno", "sono", "era", "sarà",
    "sara", "nessuno", "nulla", "niente", "qualcuno", "qualcosa",
}


def _tocca_minuscolo(token):
    """Riduce un token alla sua chiave confrontabile, senza elisione iniziale."""
    return ELISIONE.sub("", token.lower()).strip("'’")


def extract_facts(text):
    """Insieme dei fatti verificabili di un testo.

    Numeri, percentuali, nomi propri, citazioni fra virgolette e numerali in
    lettere: cio' che una riscrittura non ha il diritto di far sparire.
    """
    fatti = set()
    for m in NUMERO.finditer(text):
        fatti.add(re.sub(r"\s+", "", m.group(0)))
    for m in NOME_PROPRIO.finditer(text):
        chiave = _tocca_minuscolo(m.group(0))
        if chiave and chiave not in STOP_MAIUSCOLE and not chiave.isdigit():
            fatti.add(chiave)
    for regex in (CIT_APICE, CIT_DOPPIA):
        for m in regex.finditer(text):
            citazione = _collapse(m.group(1)).lower()
            if citazione and citazione not in STOP_MAIUSCOLE:
                fatti.add(citazione)
    for parola in PAROLA.findall(text.lower()):
        if parola in NUMERALI:
            fatti.add(parola)
    return fatti


def facts_lost(prima, dopo):
    """Fatti presenti nella versione originale e spariti dalla riscrittura."""
    return sorted(extract_facts(prima) - extract_facts(dopo))


def conta_parole(text):
    """Conta le parole di una risposta, punteggiatura esclusa."""
    return len(PAROLA.findall(text))


def snapshot(posts_dir=POSTS_DIR):
    """Fotografa domande e risposte di tutto il corpus, file per file."""
    foto = {}
    for path in sorted(Path(posts_dir).glob("*.md")):
        try:
            pairs = parse_jsonld(path.read_text(encoding="utf-8"))
        except FaqJsonError:
            continue
        if pairs:
            foto[path.name] = [{"q": p["q"], "a": p["a"]} for p in pairs]
    return foto


MIN_PAROLE = 40
MAX_PAROLE = 80


def check_against(foto, posts_dir=POSTS_DIR, min_parole=MIN_PAROLE, max_parole=MAX_PAROLE):
    """Confronta il corpus attuale con una fotografia precedente.

    Segnala tre cose: fatti spariti, risposte fuori dalla forbice di lunghezza
    consigliata da Google e coppie comparse o scomparse.
    """
    problemi = []
    attuale = snapshot(posts_dir)
    for nome, prima in sorted(foto.items()):
        dopo = attuale.get(nome)
        if dopo is None:
            problemi.append((nome, 0, "la FAQPage e' sparita"))
            continue
        if len(prima) != len(dopo):
            problemi.append((nome, 0, "conteggio cambiato: {} -> {}".format(len(prima), len(dopo))))
            continue
        for i, (a, b) in enumerate(zip(prima, dopo), start=1):
            persi = facts_lost(a["a"], b["a"])
            if persi:
                problemi.append((nome, i, "fatti persi: {}".format(", ".join(persi))))
            if a["q"] != b["q"] and facts_lost(a["q"], b["q"]):
                problemi.append((nome, i, "fatti persi nella domanda: {}".format(
                    ", ".join(facts_lost(a["q"], b["q"])))))
            n = conta_parole(b["a"])
            if not min_parole <= n <= max_parole:
                problemi.append((nome, i, "risposta di {} parole (fuori da {}-{})".format(
                    n, min_parole, max_parole)))
    return problemi


def audit(posts_dir=POSTS_DIR):
    """Conta lo stato delle FAQ su tutto il corpus."""
    stats = {"totali": 0, "con_jsonld": 0, "senza_visibile": [], "grassetto": 0,
             "accordion": 0, "domande": 0, "auto_referenziali": [], "em_dash": []}
    for path in sorted(Path(posts_dir).glob("*.md")):
        text = path.read_text(encoding="utf-8")
        stats["totali"] += 1
        try:
            pairs = parse_jsonld(text)
        except FaqJsonError:
            stats.setdefault("json_rotto", []).append(path.name)
            continue
        if pairs is None:
            continue
        stats["con_jsonld"] += 1
        span = find_faq_section(text)
        if not span:
            stats["senza_visibile"].append(path.name)
        else:
            block = text[span[0]:span[1]]
            stats["accordion" if "<summary>" in block else "grassetto"] += 1
        for pair in pairs:
            stats["domande"] += 1
            if is_self_referential(pair["q"]):
                stats["auto_referenziali"].append((path.name, pair["q"]))
            if "—" in pair["a"] or "—" in pair["q"]:
                stats["em_dash"].append(path.name)
    return stats


def cmd_audit(args):
    s = audit()
    print("post totali:             {}".format(s["totali"]))
    print("con FAQPage JSON-LD:     {}".format(s["con_jsonld"]))
    print("  senza testo visibile:  {}".format(len(s["senza_visibile"])))
    print("  visibile in grassetto: {}".format(s["grassetto"]))
    print("  visibile in accordion: {}".format(s["accordion"]))
    print("domande totali:          {}".format(s["domande"]))
    print("auto-referenziali:       {}".format(len(s["auto_referenziali"])))
    print("file con em-dash:        {}".format(len(set(s["em_dash"]))))
    if s.get("json_rotto"):
        print("JSON-LD MALFORMATO:      {}".format(len(s["json_rotto"])))
        for n in s["json_rotto"]:
            print("  {}".format(n))
    return 0


def cmd_verify(args):
    rotti = 0
    for path in sorted(POSTS_DIR.glob("*.md")):
        problemi = compare(path.read_text(encoding="utf-8"))
        if problemi:
            rotti += 1
            print("\n{}".format(path.name))
            for p in problemi:
                print("  - {}".format(p))
    print("\nfile non conformi: {}".format(rotti))
    return 1 if rotti else 0


def cmd_snapshot(args):
    Path(args.out).write_text(
        json.dumps(snapshot(), ensure_ascii=False, indent=1), encoding="utf-8")
    print("fotografia salvata in {}".format(args.out))
    return 0


def cmd_check(args):
    foto = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    problemi = check_against(foto)
    for nome, i, msg in problemi:
        print("{}  (risposta {})\n  - {}".format(nome, i, msg))
    print("\nsegnalazioni: {}".format(len(problemi)))
    return 1 if problemi else 0


def _apply(transform, args, verbo, verbo_dry):
    paths = [POSTS_DIR / n for n in args.file] if getattr(args, "file", None) else sorted(POSTS_DIR.glob("*.md"))
    toccati = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        nuovo = transform(text)
        if nuovo != text:
            if not args.dry_run:
                path.write_text(nuovo, encoding="utf-8")
            toccati.append(path.name)
    print("{}: {}".format(verbo_dry if args.dry_run else verbo, len(toccati)))
    for n in toccati:
        print("  {}".format(n))
    return 0


def cmd_to_accordion(args):
    return _apply(to_accordion, args, "convertiti", "da convertire")


def cmd_sync_visible(args):
    return _apply(sync_visible, args, "sincronizzati", "da sincronizzare")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("audit", help="stampa lo stato delle FAQ").set_defaults(func=cmd_audit)
    sub.add_parser("verify", help="confronta JSON-LD e testo visibile").set_defaults(func=cmd_verify)

    p_acc = sub.add_parser("to-accordion", help="converte le FAQ visibili in menu a tendina")
    p_acc.add_argument("--file", nargs="*", help="nomi di file specifici in _posts")
    p_acc.add_argument("--dry-run", action="store_true")
    p_acc.set_defaults(func=cmd_to_accordion)

    p_sync = sub.add_parser("sync-visible", help="rende visibile il testo del JSON-LD")
    p_sync.add_argument("--file", nargs="*", help="nomi di file specifici in _posts")
    p_sync.add_argument("--dry-run", action="store_true")
    p_sync.set_defaults(func=cmd_sync_visible)

    p_snap = sub.add_parser("facts-snapshot", help="fotografa i fatti delle FAQ")
    p_snap.add_argument("--out", required=True, help="file JSON da scrivere")
    p_snap.set_defaults(func=cmd_snapshot)

    p_check = sub.add_parser("facts-check", help="verifica che nessun fatto sia sparito")
    p_check.add_argument("baseline", help="file JSON prodotto da facts-snapshot")
    p_check.set_defaults(func=cmd_check)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
