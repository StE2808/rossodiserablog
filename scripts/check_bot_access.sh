#!/usr/bin/env bash
# Chi riesce davvero a leggere il sito.
#
# Il robots.txt e' una richiesta gentile, il firewall e' una porta: quando i due
# dicono cose diverse vince il firewall. Questo script chiede al server, non al
# robots.txt. Scoperto cosi' il 2026-08-09 che Cloudflare rispondeva 403 a
# ChatGPT, Perplexity e Claude mentre il robots.txt li invitava a entrare.
#
# Uso: ./scripts/check_bot_access.sh [url]

set -u
URL="${1:-https://rossodiserablog.it/la-scimmia-di-forbes/}"

echo "Accesso al sito per user agent: $URL"
echo

prova() {
  local etichetta="$1" atteso="$2" ua="$3"
  local code
  code=$(curl -s -o /dev/null -w "%{http_code}" -A "$ua" --max-time 20 "$URL")
  local esito="ok "
  [ "$code" != "$atteso" ] && esito="KO "
  printf "%s %-18s %-28s %s (atteso %s)\n" "$esito" "$etichetta" "$4" "$code" "$atteso"
}

echo "── devono entrare: motori di ricerca ─────────────────────────"
prova Googlebot 200 "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" "ricerca"
prova bingbot   200 "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"  "ricerca, usato da ChatGPT"
prova Applebot  200 "Mozilla/5.0 (compatible; Applebot/0.1; +http://www.apple.com/go/applebot)" "ricerca"
prova browser   200 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36" "lettore umano"

echo
echo "── devono entrare: citazione AI (il senso del lavoro GEO) ────"
prova OAI-SearchBot    200 "Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)" "ChatGPT Search"
prova ChatGPT-User     200 "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot" "ChatGPT su richiesta"
prova PerplexityBot    200 "Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)" "Perplexity"
prova Claude-SearchBot 200 "Mozilla/5.0 (compatible; Claude-SearchBot/1.0)" "Claude con ricerca"

echo
echo "── devono restare fuori: addestramento ───────────────────────"
prova GPTBot    403 "Mozilla/5.0 (compatible; GPTBot/1.0; +https://openai.com/gptbot)" "training OpenAI"
prova ClaudeBot 403 "Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)" "training Anthropic"
prova CCBot     403 "CCBot/2.0 (https://commoncrawl.org/faq/)" "Common Crawl"

echo
echo "Le righe KO sono quelle da sistemare in Cloudflare (Security, sezione Bot)."
