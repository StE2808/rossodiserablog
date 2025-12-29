#!/bin/bash

echo "=== FIX H1 → H2 nei post ==="

count=0

for file in _posts/*.md; do
  if awk '/^---$/{p++} p==2 && /^# [^#]/{found=1; exit} END{exit !found}' "$file" 2>/dev/null; then
    awk '
      BEGIN { in_fm=0; fm_count=0 }
      /^---$/ {
        fm_count++
        if (fm_count == 1) in_fm=1
        if (fm_count == 2) in_fm=0
        print
        next
      }
      in_fm { print; next }
      /^# [^#]/ { sub(/^# /, "## ") }
      { print }
    ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
    echo "  ✓ $file"
    ((count++))
  fi
done

echo ""
echo "✅ Corretti $count post"
