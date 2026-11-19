#!/usr/bin/env python3
"""Controlla che l'anteprima di Sveltia (admin/anteprima-approfondimento.js) non si scosti dal sito (19/11/2026).

Due prove, per ogni approfondimento scritto come documento:
  1. il parser in JavaScript dà gli stessi campi di scripts/documento_approfondimento.py;
  2. l'impaginazione in JavaScript ha la stessa struttura e lo stesso testo della pagina costruita da Jekyll
     (da «cop» a «domande», senza «Leggi anche»: quello lo decide il sito).

Uso:  python3 scripts/controlla_anteprima.py CARTELLA_DEL_BUILD [FILE.md ...]
      (senza file: tutti quelli in _numeri e _posts/approfondimenti)
Serve node; per la prova 2 serve anche marked: MARKED=/percorso/node_modules/marked (versione di admin/index.html).
"""
import json, os, re, subprocess, sys
from html.parser import HTMLParser
from pathlib import Path
import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'scripts'))
import documento_approfondimento as doc

NODE = r"""
const a = require(process.argv[1]);
let mk = null; try { mk = require(process.env.MARKED || 'marked'); } catch (e) {}
const fm = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const out = { campi: a.analizza(fm.body) };
if (mk) out.html = a.pagina(fm, { markdown: s => mk.marked.parse(s) });
process.stdout.write(JSON.stringify(out));
"""
VUOTI = ('img', 'br', 'hr', 'input', 'meta', 'link')


class Struttura(HTMLParser):
    """Raccoglie (tag.classe) degli elementi con classe e il testo, dentro <main>, saltando le parti del sito."""
    SALTA = {'rubriche', 'azioni', 'commenti', 'prova'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.dentro, self.salta, self.forma, self.testo = False, 0, [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'main':
            self.dentro = True
        if not self.dentro:
            return
        classi = set((a.get('class') or '').split())
        if self.salta:
            self.salta += 0 if tag in VUOTI else 1
            return
        if classi & self.SALTA and tag not in VUOTI:
            self.salta = 1
            return
        if classi:
            self.forma.append(tag + '.' + '.'.join(sorted(classi)))

    def handle_endtag(self, tag):
        if tag == 'main':
            self.dentro = False
        if self.salta:
            self.salta -= 1

    def handle_data(self, d):
        if self.dentro and not self.salta:
            self.testo.append(d)


def leggi(html_txt):
    s = Struttura(); s.feed(html_txt)
    t = ' '.join(s.testo)
    t = t.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'").replace('…', '...').replace('–', '-')
    t = re.sub(r'Uscita prevista: ', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return s.forma, t


def pagina_vera(build, f, fm):
    if fm.get('permalink'):
        return Path(build) / fm['permalink'].strip('/') / 'index.html'
    nome = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', Path(f).stem)
    sotto = 'anteprima' if '_numeri' in str(f) else 'approfondimenti'
    return Path(build) / sotto / nome / 'index.html'


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    build, files = sys.argv[1], sys.argv[2:]
    if not files:
        files = sorted(str(p) for c in ('_numeri', '_posts/approfondimenti') for p in (REPO / c).glob('*.md'))
    errori = 0
    for f in files:
        fm_txt, corpo = doc.dividi(Path(f).read_text(encoding='utf-8'))
        if '## ' not in corpo:
            continue
        fm = yaml.safe_load(fm_txt) or {}
        fm['body'] = corpo
        r = subprocess.run(['node', '-e', NODE, str(REPO / 'admin/anteprima-approfondimento.js')],
                           input=json.dumps(fm, default=str), capture_output=True, text=True, check=True)
        out = json.loads(r.stdout)
        py = json.loads(json.dumps(doc.analizza(corpo)))
        js = out['campi']
        for m in js.get('movimenti', []):  # il JS mette sempre «dopo», il Python solo se c'è
            if not m.get('dopo'):
                m.pop('dopo', None)
        for m in py.get('movimenti', []):
            for d in m.get('dopo', []):
                if 'grande' in d:
                    d['grande'] = d['grande'].rstrip('\n')
        if 'tema' in py:
            py['tema']['apertura'] = py['tema']['apertura'].rstrip('\n')
        nome = Path(f).name
        if py != js:
            errori += 1
            print(f'DIVERSO {nome}: il parser JavaScript non dà gli stessi campi del Python')
            for k in sorted(set(py) | set(js)):
                if py.get(k) != js.get(k):
                    print(f'   campo {k}:\n     py {json.dumps(py.get(k), ensure_ascii=False)[:300]}\n     js {json.dumps(js.get(k), ensure_ascii=False)[:300]}')
        else:
            print(f'ok parser   {nome}')
        if 'html' not in out:
            print('   (prova 2 saltata: manca marked, vedi MARKED)')
            continue
        vera = pagina_vera(build, f, fm)
        if not vera.is_file():
            print(f'   (prova 2 saltata: non trovo {vera})')
            continue
        f1, t1 = leggi(vera.read_text(encoding='utf-8'))
        f2, t2 = leggi(out['html'])
        if f1 != f2:
            errori += 1
            i = next((i for i, (x, y) in enumerate(zip(f1, f2)) if x != y), min(len(f1), len(f2)))
            print(f'DIVERSO {nome}: struttura, dal pezzo {i}\n   sito       {f1[i:i+4]}\n   anteprima  {f2[i:i+4]}')
        elif t1 != t2:
            errori += 1
            i = next((i for i, (x, y) in enumerate(zip(t1, t2)) if x != y), min(len(t1), len(t2)))
            print(f'DIVERSO {nome}: testo\n   sito       ...{t1[max(0, i-80):i+80]}\n   anteprima  ...{t2[max(0, i-80):i+80]}')
        else:
            print(f'ok pagina   {nome}')
    sys.exit(1 if errori else 0)


if __name__ == '__main__':
    main()
