#!/usr/bin/env python3
"""Cartoline social di un articolo o approfondimento (19/11/2026).

Fa due immagini nella grafica della rivista, prese dal front matter del post:
  - orizzontale 1200x675 (x2): X e Facebook, e anteprima del link
  - verticale 1080x1350: Instagram
Le salva in assets/images/social/<slug>-orizzontale.jpg e <slug>-verticale.jpg
(pubbliche dopo il push: Buffer vuole un URL).

Uso:  python3 scripts/cartoline.py _posts/approfondimenti/2026-11-19-chi-ce-nella-folla.md
Serve Google Chrome. Le immagini dei post devono esistere in locale (originali jpg/png).
"""
import sys, re, html, subprocess, tempfile, pathlib
import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
FONTS = ('https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900'
         '&family=Arvo:wght@700&family=Gloock&family=Rock+Salt'
         '&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap')
MESI = 'gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre'.split()
AUTORI = {'stefano-vozzi': 'Stefano Vozzi', 'lino-rialti': 'Lino Rialti'}

CSS = """
:root{--carta:#f1efea;--ink:#121212;--rosso:#c23c3c;--rosso-marca:#8b1a1a}
*{box-sizing:border-box}html,body{margin:0;background:var(--carta);color:var(--ink)}
.c{position:relative;overflow:hidden;background:var(--carta)}
.testata{display:flex;align-items:center;gap:14px;margin:0}
.testata img{width:138px;height:auto;margin:-10px -6px -10px -12px}
.testata span{font:700 49px/.95 'Arvo',serif}
.testata .blog{display:inline-block;margin-left:.45em;vertical-align:.35em;font:400 22px/1 'Rock Salt',cursive;color:var(--rosso);transform:rotate(-8deg)}
.riga{display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--ink);padding-top:8px;font:500 14px 'Archivo'}
.riga span{white-space:nowrap}
.riga b{color:var(--rosso-marca);text-transform:uppercase;letter-spacing:.05em}
h1{font:400 64px/1 'Gloock',serif;letter-spacing:-.01em;margin:0}
.cat{font:400 22px/1.4 'Source Serif 4',serif;margin:0}
.firma{font:500 15px 'Archivo';margin:0}
.foto{background:#2a2a2a;overflow:hidden}.foto img{width:100%;height:100%;object-fit:cover;display:block}
.url{font:700 14px 'Archivo';letter-spacing:.06em;text-transform:uppercase;color:var(--rosso-marca)}
/* orizzontale */
.o{width:1200px;height:675px;display:grid;grid-template-columns:5fr 7fr}
.o .sx{padding:36px 40px 32px;display:flex;flex-direction:column;gap:18px;border-right:5px solid var(--rosso)}
.o .giu{margin-top:auto;display:flex;flex-direction:column;gap:14px}
.o .piede{display:flex;justify-content:space-between;align-items:baseline}
/* verticale */
.v{width:1080px;height:1350px;display:grid;grid-template-rows:740px 1fr}
.v .foto{border-bottom:6px solid var(--rosso)}
.v .sotto{padding:36px 56px 44px;display:flex;flex-direction:column;gap:22px}
.v .riga{font-size:17px}
.v h1{font-size:104px}
.v.lungo h1{font-size:68px}
.o.lungo h1{font-size:46px}
.v .firma{font-size:18px}
.v .cat{font-size:28px}
.v .piede{margin-top:auto;display:flex;justify-content:space-between;align-items:center}
.v .url{font-size:17px}
"""


def leggi(post):
    testo = open(post, encoding='utf-8').read()
    _, fm_txt, corpo = testo.split('---', 2)
    fm = yaml.safe_load(fm_txt)
    if '## ' in corpo:  # approfondimento scritto come documento: catenaccio & co. stanno nel corpo
        sys.path.insert(0, str(REPO / 'scripts'))
        from documento_approfondimento import analizza
        fm = {**analizza(corpo), **fm}
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', pathlib.Path(post).stem)
    return fm, slug


def scheda(fm):
    e = html.escape
    a, m, g = (int(x) for x in str(fm['date'])[:10].split('-'))  # la data può arrivare come stringa
    data = f"{g} {MESI[m - 1]} {a}"
    if fm.get('approfondimento') or 'numero' in fm:
        et = f"Approfondimento · N. {fm.get('numero', '')}"
        if fm.get('tema_breve'):
            et += f" · {fm['tema_breve']}"
        sotto = fm.get('catenaccio') or fm.get('description', '')
    else:
        cats = yaml.safe_load(open(REPO / '_data/categorie.yml', encoding='utf-8')) or {}
        c = fm.get('category', '')
        voce = cats.get(c)
        et = voce.get('nome', c) if isinstance(voce, dict) else c
        sotto = fm.get('description', '')
    img = REPO / str(fm.get('image', '')).lstrip('/')
    return dict(et=e(et), data=e(data), titolo=e(fm['title']), sotto=e(sotto),
                autore=e(AUTORI.get(fm.get('author', ''), fm.get('author', ''))),
                img=img.as_uri() if img.is_file() else '',
                logo=(REPO / 'assets/images/numeri/logo-testata.png').as_uri())


def pagina(s, verticale):
    testata = ('<p class="testata"><img alt="" src="%s"><span>Rosso<br>di Sera<b class="blog">blog</b></span></p>'
               % s['logo'])
    riga = '<div class="riga"><b>%s</b><span>%s</span></div>' % (s['et'], s['data'])
    foto = '<div class="foto">%s</div>' % ('<img alt="" src="%s">' % s['img'] if s['img'] else '')
    lungo = ' lungo' if len(s['titolo']) > 55 else ''
    if verticale:
        corpo = ('<div class="c v' + lungo + '">' + foto + '<div class="sotto">' + riga
                 + '<h1>%s</h1><p class="cat">%s</p><p class="firma">di %s</p>' % (s['titolo'], s['sotto'], s['autore'])
                 + '<div class="piede">' + testata + '<span class="url">rossodiserablog.it</span></div></div></div>')
    else:
        corpo = ('<div class="c o' + lungo + '"><div class="sx">' + testata + '<div class="giu">' + riga
                 + '<h1>%s</h1><p class="cat">%s</p>' % (s['titolo'], s['sotto'])
                 + '<div class="piede"><p class="firma">di %s</p><span class="url">rossodiserablog.it</span></div>'
                 % s['autore'] + '</div></div>' + foto + '</div>')
    return ('<!doctype html><html lang="it"><head><meta charset="utf-8">'
            '<link href="%s" rel="stylesheet"><style>%s</style></head><body>%s</body></html>' % (FONTS, CSS, corpo))


def scatta(html_txt, w, h, scala, uscita):
    with tempfile.TemporaryDirectory() as tmp:
        f = pathlib.Path(tmp) / 'c.html'
        f.write_text(html_txt, encoding='utf-8')
        png = pathlib.Path(tmp) / 'c.png'
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--allow-file-access-from-files', f'--force-device-scale-factor={scala}',
                        '--virtual-time-budget=8000', f'--window-size={w},{h}',
                        f'--screenshot={png}', f.as_uri()], check=True, capture_output=True)
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '88', str(png), '--out', str(uscita)],
                       check=True, capture_output=True)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out = REPO / 'assets/images/social'
    out.mkdir(parents=True, exist_ok=True)
    for post in sys.argv[1:]:
        fm, slug = leggi(post)
        s = scheda(fm)
        if not s['img']:
            print(f'ATTENZIONE {slug}: immagine non trovata in locale ({fm.get("image")})')
        o = out / f'{slug}-orizzontale.jpg'
        v = out / f'{slug}-verticale.jpg'
        scatta(pagina(s, False), 1200, 675, 2, o)
        scatta(pagina(s, True), 1080, 1350, 1, v)
        print(o.relative_to(REPO))
        print(v.relative_to(REPO))


if __name__ == '__main__':
    main()
