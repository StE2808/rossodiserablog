#!/usr/bin/env python3
"""Pubblica gli approfondimenti arrivati alla data (17/11/2026).

Il CMS scrive gli approfondimenti in _numeri/ : sono anteprime (noindex, fuori da
sitemap e home, fascia «Anteprima» con il pulsante Pubblica). Quando nel CMS si
accende «Pubblica» e la data di pubblicazione è arrivata, questo script sposta il
file in _posts/approfondimenti/AAAA-MM-GG-<nome>.md, dove diventa un post vero.

Gira nel workflow jekyll.yml (a ogni push e ogni ora). Tocca solo le righe di primo
livello del front matter, il resto del file resta byte per byte.

Uso: python3 scripts/pubblica_approfondimenti.py [--ora "AAAA-MM-GG HH:MM"] [--prova]
Scrive in $GITHUB_OUTPUT «fatti=1» se ha spostato qualcosa.
"""
import argparse, os, re, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROMA = ZoneInfo("Europe/Rome")
DA_TOGLIERE = {"layout", "permalink", "prova", "sitemap", "uscita", "uscita_prevista",
               "pubblica", "data_pubblicazione", "date"}


def leggi_data(v):
    v = v.strip().strip('"\'')
    for fmt in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z",
                "%Y-%m-%dT%H:%M%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            d = datetime.strptime(v.replace("Z", "+0000"), fmt)
            return d if d.tzinfo else d.replace(tzinfo=ROMA)
        except ValueError:
            pass
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", default=".")
    ap.add_argument("--ora")
    ap.add_argument("--prova", action="store_true", help="dice cosa farebbe, non tocca niente")
    a = ap.parse_args()
    R = Path(a.radice)
    ora = leggi_data(a.ora) if a.ora else datetime.now(ROMA)
    fatti = 0
    for f in sorted((R / "_numeri").glob("*.md")):
        testo = f.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?\n)---\n", testo, re.S)
        if not m:
            continue
        fm = m.group(1)
        top = dict(re.findall(r"^([A-Za-z_][\w]*):[ \t]*(.*)$", fm, re.M))
        if top.get("pubblica", "").strip().lower() != "true":
            continue
        if top.get("prova", "").strip().lower() == "true":
            print(f"{f.name}: è una prova fatta a mano (prova: true), non si pubblica")
            continue
        quando = leggi_data(top.get("data_pubblicazione", "")) if top.get("data_pubblicazione") else None
        if not quando:
            print(f"{f.name}: «Pubblica» acceso ma manca la data di pubblicazione, salto")
            continue
        if quando > ora:
            print(f"{f.name}: programmato per {quando:%d/%m/%Y %H:%M}, non ancora")
            continue
        if not top.get("category", "").strip():
            print(f"{f.name}: manca la categoria, salto")
            continue
        righe, salta = [], False
        for r in fm.splitlines(keepends=True):
            k = re.match(r"^([A-Za-z_][\w]*):", r)
            if k:
                salta = k.group(1) in DA_TOGLIERE
            elif not r.startswith((" ", "\t", "-")) and r.strip():
                salta = False
            if not salta:
                righe.append(r)
        q = quando.astimezone(ROMA)
        nuovo_fm = f"date: {q:%Y-%m-%d %H:%M:%S %z}\n" + "".join(righe)
        dest = R / "_posts" / "approfondimenti" / f"{q:%Y-%m-%d}-{f.stem}.md"
        print(f"{f.name}: pubblicato come {dest.relative_to(R)}")
        if not a.prova:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text("---\n" + nuovo_fm + "---\n" + testo[m.end():], encoding="utf-8")
            f.unlink()
        fatti += 1
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as o:
            o.write(f"fatti={1 if fatti else 0}\n")
    print(f"Approfondimenti pubblicati: {fatti}")


if __name__ == "__main__":
    sys.exit(main())
