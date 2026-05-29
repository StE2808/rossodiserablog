#!/usr/bin/env python3
"""
Fix YAML front matter dei post Jekyll (problemi introdotti da Sveltia CMS).

Normalizza, SOLO nel front matter:
  - smart quotes Unicode (U+201C/D, U+2018/9) → dritte
  - zero-width spaces (U+200B/200C/200D/FEFF) → rimossi
  - scalari single-quoted con apostrofi e/o doppie → riquotati JSON-safe
    (double-quoted con escape): è l'unica forma sempre YAML-valida quando il
    valore contiene insieme apostrofi (l'inserimento) e doppie ("Uccelli").

Questa logica è gemella del blocco inline nel CI (.github/workflows/jekyll.yml).
Sintomo che risolve: schede articolo in home con solo la data, title/excerpt vuoti.
"""

import glob
import re
import json
import sys

try:
    import yaml  # validazione opzionale (presente in locale)
except ImportError:
    yaml = None

REPLACEMENTS = {
    '“': '"', '”': '"',
    '‘': "'", '’': "'",
    '​': '', '‌': '', '‍': '', '﻿': '',
}


def fix_single_quoted_apostrophes(fm):
    """Riquota gli scalari single-quoted come stringhe double-quoted JSON-safe.
    Gestisce i valori con apostrofi E doppie insieme, caso che spezzava il YAML."""
    out = []
    for line in fm.split('\n'):
        m = re.match(r"^(\s*\w[\w_]*:\s*)'(.*)'(\s*)$", line)
        if m:
            key, value, trail = m.group(1), m.group(2), m.group(3)
            # single-quoted è valido se ogni apostrofo interno è raddoppiato ('');
            # se dopo aver rimosso le coppie resta un apostrofo singolo, il YAML è rotto.
            if "'" in value.replace("''", ""):
                unescaped = value.replace("''", "'")  # YAML: '' = apostrofo letterale
                line = f'{key}{json.dumps(unescaped, ensure_ascii=False)}{trail}'
        out.append(line)
    return '\n'.join(out)


def fix_front_matter(fm):
    for bad, good in REPLACEMENTS.items():
        fm = fm.replace(bad, good)
    return fix_single_quoted_apostrophes(fm)


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False, True  # nessun front matter: niente da fare

    fm_fixed = fix_front_matter(parts[1])
    valid = True
    if yaml is not None:
        try:
            yaml.safe_load(fm_fixed)
        except yaml.YAMLError:
            valid = False

    if fm_fixed != parts[1]:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('---' + fm_fixed + '---' + parts[2])
        return True, valid

    return False, valid


def main():
    print("Fix YAML front matter nei post Jekyll...\n")
    fixed_count = 0
    total = 0
    broken = []

    for filepath in glob.glob('_posts/*.md'):
        total += 1
        changed, valid = process_file(filepath)
        if changed:
            fixed_count += 1
            print(f"✓ Fixed: {filepath}")
        if not valid:
            broken.append(filepath)

    print(f"\nPost processati: {total}")
    print(f"Post corretti:   {fixed_count}")
    print(f"Post invariati:  {total - fixed_count}")

    if broken:
        print("\n⚠️  Front matter ANCORA invalido dopo il fix:")
        for b in broken:
            print(f"   - {b}")
        sys.exit(1)


if __name__ == '__main__':
    main()
