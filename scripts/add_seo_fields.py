#!/usr/bin/env python3
"""
Script per aggiungere campi SEO mancanti ai post del blog.

Usage:
    python3 scripts/add_seo_fields.py           # Esegue le modifiche
    python3 scripts/add_seo_fields.py --dry-run # Mostra cosa farebbe senza modificare
"""

import argparse
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


def parse_front_matter(content: str) -> Tuple[Dict, str, str]:
    """
    Estrae front matter YAML e contenuto da un file markdown.

    Returns:
        Tuple[Dict, str, str]: (front_matter_dict, front_matter_raw, body)
    """
    # Trova i delimitatori del front matter
    parts = content.split('---', 2)

    if len(parts) < 3:
        raise ValueError("Front matter non trovato o malformato")

    front_matter_raw = parts[1]
    body = parts[2].strip()

    # Parsa il front matter come dizionario mantenendo l'ordine
    front_matter = {}
    for line in front_matter_raw.strip().split('\n'):
        if ':' in line and not line.strip().startswith('#'):
            key = line.split(':', 1)[0].strip()
            value = line.split(':', 1)[1].strip()
            # Rimuovi quotes se presenti
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            front_matter[key] = value

    return front_matter, front_matter_raw, body


def get_first_sentences(text: str, num_sentences: int = 2) -> str:
    """Estrae le prime N frasi dal testo."""
    # Rimuovi markdown headers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    # Rimuovi link markdown
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Rimuovi bold/italic
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^\*]+)\*', r'\1', text)
    # Rimuovi spazi multipli
    text = re.sub(r'\s+', ' ', text).strip()

    # Trova le prime N frasi
    sentences = re.split(r'[.!?]\s+', text)
    return '. '.join(sentences[:num_sentences]).strip()


def truncate_description(text: str, max_length: int = 155) -> str:
    """Tronca il testo a max_length caratteri, tagliando all'ultimo spazio."""
    if len(text) <= max_length:
        return text

    # Trova l'ultimo spazio prima di max_length
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')

    if last_space > 0:
        truncated = truncated[:last_space]

    # Aggiungi ... se troncato
    return truncated.rstrip('.,;:!?') + '...'


def generate_description(front_matter: Dict, body: str) -> str:
    """Genera una description basata su excerpt o contenuto."""
    # Usa excerpt se esiste
    if 'excerpt' in front_matter and front_matter['excerpt']:
        text = front_matter['excerpt']
        # Rimuovi quotes se presenti
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        return truncate_description(text, 155)

    # Altrimenti usa le prime 2 frasi del contenuto
    first_sentences = get_first_sentences(body, 2)
    return truncate_description(first_sentences, 155)


def add_seo_fields_to_front_matter(front_matter_raw: str, front_matter: Dict, body: str) -> Tuple[str, List[str]]:
    """
    Aggiunge campi SEO mancanti al front matter.

    Returns:
        Tuple[str, List[str]]: (new_front_matter, fields_added)
    """
    fields_added = []
    lines = front_matter_raw.strip().split('\n')
    new_lines = []

    # Trova la posizione dove inserire i nuovi campi (dopo image: se presente)
    insert_position = None
    for i, line in enumerate(lines):
        if line.strip().startswith('image:'):
            insert_position = i + 1
            break

    # Se non c'è image:, inserisci prima di excerpt: o alla fine
    if insert_position is None:
        for i, line in enumerate(lines):
            if line.strip().startswith('excerpt:'):
                insert_position = i
                break

    if insert_position is None:
        insert_position = len(lines)

    # Genera i nuovi campi
    new_fields = []

    # Aggiungi image_alt se mancante
    if 'image_alt' not in front_matter and 'image' in front_matter:
        new_fields.append('image_alt: "Immagine di copertina dell\'articolo"')
        fields_added.append('image_alt')

    # Aggiungi description se mancante
    if 'description' not in front_matter:
        description = generate_description(front_matter, body)
        new_fields.append(f'description: "{description}"')
        fields_added.append('description')

    # Ricostruisci il front matter
    new_lines = lines[:insert_position] + new_fields + lines[insert_position:]

    return '\n'.join(new_lines), fields_added


def process_file(filepath: Path, dry_run: bool = False) -> Tuple[bool, List[str]]:
    """
    Processa un singolo file markdown.

    Returns:
        Tuple[bool, List[str]]: (modified, fields_added)
    """
    try:
        # Leggi il file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parsa front matter e body
        front_matter, front_matter_raw, body = parse_front_matter(content)

        # Aggiungi campi SEO mancanti
        new_front_matter, fields_added = add_seo_fields_to_front_matter(
            front_matter_raw, front_matter, body
        )

        # Se non ci sono modifiche, ritorna
        if not fields_added:
            return False, []

        # Ricostruisci il file
        new_content = f"---\n{new_front_matter}\n---\n{body}"

        # Salva solo se non è dry-run
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

        return True, fields_added

    except Exception as e:
        print(f"❌ Errore processando {filepath.name}: {e}")
        return False, []


def main():
    parser = argparse.ArgumentParser(
        description='Aggiunge campi SEO mancanti (description, image_alt) ai post del blog'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Mostra cosa farebbe senza modificare i file'
    )
    args = parser.parse_args()

    # Directory dei post
    posts_dir = Path('_posts')

    if not posts_dir.exists():
        print(f"❌ Directory {posts_dir} non trovata!")
        return

    # Trova tutti i file .md
    md_files = sorted(posts_dir.glob('*.md'))

    print(f"{'🔍 DRY RUN - ' if args.dry_run else ''}Processando {len(md_files)} file...\n")

    # Statistiche
    modified_count = 0
    description_added = 0
    image_alt_added = 0

    # Processa ogni file
    for filepath in md_files:
        modified, fields_added = process_file(filepath, args.dry_run)

        if modified:
            modified_count += 1
            print(f"{'📝' if args.dry_run else '✅'} {filepath.name}")

            for field in fields_added:
                print(f"   └─ Aggiunto: {field}")
                if field == 'description':
                    description_added += 1
                elif field == 'image_alt':
                    image_alt_added += 1

    # Stampa riepilogo
    print(f"\n{'─' * 50}")
    print(f"📊 RIEPILOGO {'(DRY RUN)' if args.dry_run else ''}")
    print(f"{'─' * 50}")
    print(f"File totali:           {len(md_files)}")
    print(f"File modificati:       {modified_count}")
    print(f"Campo 'description':   +{description_added}")
    print(f"Campo 'image_alt':     +{image_alt_added}")

    if args.dry_run:
        print(f"\n💡 Esegui senza --dry-run per applicare le modifiche")
    else:
        print(f"\n✅ Modifiche applicate con successo!")


if __name__ == '__main__':
    main()
