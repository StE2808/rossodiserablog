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
        data = json.loads(raw, strict=False)
        return [{"q": normalize(item["name"]),
                 "a": normalize(item["acceptedAnswer"]["text"])}
                for item in data.get("mainEntity", [])]
    return None


def _parse_bold(block):
    pairs = []
    marks = list(BOLD_Q.finditer(block))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(block)
        pairs.append({"q": normalize(m.group(1)), "a": normalize(block[m.end():end])})
    return pairs


def _parse_accordion(block):
    pairs = []
    for chunk in block.split("<details")[1:]:
        qm = SUMMARY_Q.search(chunk)
        if not qm:
            continue
        answer = chunk[qm.end():].split("</details>")[0]
        pairs.append({"q": normalize(qm.group(1)), "a": normalize(answer)})
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
        out += ['<details class="faq-item" markdown="1">',
                '<summary><h3>{}</h3></summary>'.format(pair["q"]),
                "", pair["a"], "", "</details>", ""]
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
    jsonld = parse_jsonld(text)
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


def audit(posts_dir=POSTS_DIR):
    """Conta lo stato delle FAQ su tutto il corpus."""
    stats = {"totali": 0, "con_jsonld": 0, "senza_visibile": [], "grassetto": 0,
             "accordion": 0, "domande": 0, "auto_referenziali": [], "em_dash": []}
    for path in sorted(Path(posts_dir).glob("*.md")):
        text = path.read_text(encoding="utf-8")
        stats["totali"] += 1
        pairs = parse_jsonld(text)
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
            if re.search(r"articolo|nel pezzo|secondo l'autore", pair["q"], re.IGNORECASE):
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

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
