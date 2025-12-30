#!/bin/bash

# Converti tutte le immagini esistenti in WebP e aggiorna i riferimenti nei post

echo "=== Conversione immagini esistenti in WebP ==="

# 1. Converti immagini in tutte le directory
converted=0
for img in assets/images/{2023,2024,2025,uploads}/*.{jpg,jpeg,png,JPG,JPEG,PNG} assets/images/{2023,2024,2025,uploads}/*/*.{jpg,jpeg,png,JPG,JPEG,PNG}; do
    if [ -f "$img" ]; then
        webp_file="${img%.*}.webp"
        if [ ! -f "$webp_file" ]; then
            cwebp -q 80 "$img" -o "$webp_file"
            echo "✓ Convertita: $img"
            ((converted++))
        fi
    fi
done

echo ""
echo "Totale convertite: $converted"

# 2. Aggiorna riferimenti nei post
echo ""
echo "=== Aggiornamento riferimenti nei post ==="

for post in _posts/*.md; do
    # Sostituisci .jpg, .jpeg, .png con .webp nei campi image
    sed -i '' -E 's/\.(jpg|jpeg|png)(["\)]|$)/.webp\2/gi' "$post"
done

echo "✓ Riferimenti aggiornati in tutti i post"

# 3. Rimuovi originali
echo ""
echo "=== Rimozione immagini originali ==="

removed=0
for img in assets/images/{2023,2024,2025,uploads}/*.{jpg,jpeg,png,JPG,JPEG,PNG} assets/images/{2023,2024,2025,uploads}/*/*.{jpg,jpeg,png,JPG,JPEG,PNG}; do
    if [ -f "$img" ]; then
        webp_file="${img%.*}.webp"
        if [ -f "$webp_file" ]; then
            rm "$img"
            echo "✓ Rimossa: $img"
            ((removed++))
        fi
    fi
done

echo ""
echo "Totale rimosse: $removed"

echo ""
echo "=== Completato! ==="
