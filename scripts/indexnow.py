"""IndexNow (20/11/2026): avvisa Bing, Yandex e gli altri motori degli URL nuovi o cambiati.

  python3 scripts/indexnow.py confronta _site/sitemap.xml   -> stampa gli URL nuovi o con lastmod cambiato
                                                                rispetto alla sitemap online (prima del deploy)
  python3 scripts/indexnow.py corpo _site/sitemap.xml       -> lo stesso, già nel JSON da mandare (usato dal workflow)
  python3 scripts/indexnow.py invia URL [URL ...]            -> li manda a api.indexnow.org

La chiave è il file <chiave>.txt nella radice del repo (è pubblica per costruzione, non è un segreto).
Nel workflow: il confronto nel job build, l'invio nel job deploy, dopo la messa online.
"""
import glob, json, os, re, sys, urllib.request

SITO = "https://rossodiserablog.it"

def leggi(xml):
    return dict(re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", xml))

def confronta(percorso):
    nuova = leggi(open(percorso, encoding="utf-8").read())
    try:
        req = urllib.request.Request(SITO + "/sitemap.xml", headers={"User-Agent": "rossodisera-indexnow/1.0"})
        online = leggi(urllib.request.urlopen(req, timeout=30).read().decode())
    except Exception as e:
        print(f"sitemap online illeggibile ({e}): niente invio", file=sys.stderr)
        return
    if not online:
        return
    for url, data in nuova.items():
        if online.get(url) != data and "/authors/" not in url:  # gli autori cambiano data a ogni build
            print(url)

def corpo(urls):
    urls = [u for u in urls if u.startswith(SITO)][:1000]
    if not urls:
        return None
    chiave = [os.path.basename(f)[:-4] for f in glob.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}\.txt", os.path.basename(f))]
    if not chiave:
        sys.exit("IndexNow: manca il file della chiave")
    return {"host": "rossodiserablog.it", "key": chiave[0], "keyLocation": f"{SITO}/{chiave[0]}.txt", "urlList": urls}

def invia(urls):
    corpo_ = corpo(urls)
    if not corpo_:
        print("IndexNow: niente da inviare"); return
    urls = corpo_["urlList"]; corpo_json = corpo_
    req = urllib.request.Request("https://api.indexnow.org/indexnow", json.dumps(corpo_json).encode(),
                                 {"Content-Type": "application/json; charset=utf-8"})
    try:
        r = urllib.request.urlopen(req, timeout=30)
        print(f"IndexNow: {len(urls)} URL inviati, risposta {r.status}")
    except urllib.error.HTTPError as e:
        print(f"IndexNow: errore {e.code} {e.read()[:200]!r}")  # non blocca il deploy

if __name__ == "__main__":
    if sys.argv[1:2] == ["confronta"]:
        confronta(sys.argv[2])
    elif sys.argv[1:2] == ["corpo"]:   # JSON pronto per curl (riga vuota se non c'è niente)
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            confronta(sys.argv[2])
        c = corpo(buf.getvalue().split())
        print(json.dumps(c) if c else "")
    elif sys.argv[1:2] == ["invia"]:
        invia(sys.argv[2:])
