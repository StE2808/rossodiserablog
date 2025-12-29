#!/bin/bash

echo "=== AUDIT SEO POST ==="
echo ""

echo "📝 Post SENZA description:"
grep -L "^description:" _posts/*.md 2>/dev/null || echo "  (tutti hanno il campo)"
echo ""

echo "🖼️  Post SENZA image_alt:"
grep -L "^image_alt:" _posts/*.md 2>/dev/null || echo "  (tutti hanno il campo)"
echo ""

echo "⚠️  Post con possibile doppio H1 (iniziano con #):"
for file in _posts/*.md; do
  # Salta il front matter e controlla la prima riga di contenuto
  if awk '/^---$/{p++} p==2{getline; if(/^#[^#]/){print FILENAME; exit}}' "$file" 2>/dev/null; then
    :
  fi
done
echo ""

echo "📊 Post senza campo description valorizzato:"
for file in _posts/*.md; do
  desc=$(grep "^description:" "$file" 2>/dev/null | cut -d'"' -f2 | cut -d"'" -f2)
  if [ -z "$desc" ] || [ "$desc" = "" ]; then
    echo "  - $file"
  fi
done

echo ""
echo "=== FINE AUDIT ==="
