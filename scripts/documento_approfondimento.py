#!/usr/bin/env python3
"""Approfondimento scritto come documento unico (19/11/2026, idea di Stefano).

Invece di compilare decine di caselle nel CMS, l'approfondimento si scrive di seguito,
con titoletti fissi che fanno da segnaposto. Nel front matter restano solo le caselle
«di servizio» (titolo, autore, categoria, date, foto di copertina, SEO); il corpo del file
è il documento. Questo script lo legge e ricava i campi che il layout numero.html usa:
catenaccio, punto, tema, movimenti, domande.

Il formato del documento:

    Catenaccio: una o due frasi sotto il titolo.
    Il punto: il riassunto nel riquadro della copertina.

    ## Apertura: Titolo del tema
    Sottotitolo: la frase sotto il titolo del tema.

    Primo paragrafo dell'apertura.

    Secondo paragrafo.

    ## Capire: titolo del primo movimento
    Indice: la riga che compare nell'indice
    Sommario: prima voce; seconda voce
    Colonne: 3

    ### Titolo di un blocco
    Testo del blocco (anche più paragrafi). Se il titolo finisce con «?»
    il blocco è una domanda e finisce nelle FAQ per Google.

    ### Frase rossa
    La frase grande,
    anche su due righe.
    Sotto: la riga piccola sotto la frase.
    Foto: /assets/images/....jpg
    Descrizione foto: cosa si vede (per chi non vede)
    Foto generata: no
    Foto intera: sì
    Didascalia: crediti della foto.

    ### Tabella: Titolo della tabella
    Didascalia: sottotitolo della tabella.

    Numero: 474
    Unità: iPhone
    Cosa: cosa dice il numero
    Fonte: [nome](link), data

    Numero: 99
    Unità: smartphone
    Cosa: ...
    Fonte: ...

    Limite: la nota sui limiti dei dati.

Ogni voce della tabella sono quattro righe (Numero, Unità, Cosa, Fonte), separate da una riga
vuota. «Fonte:» in pagina lo aggiunge lo script. Le tabelle col pipe (| a | b |) funzionano ancora.

    ## Domande
    - Prima domanda finale?
    - Seconda?

Frase rossa e Tabella si mettono in fondo al loro movimento.

Uso:
  python3 scripts/documento_approfondimento.py --applica _numeri _posts/approfondimenti
      (nel build: per ogni file col documento nel corpo, scrive i campi nel front matter e svuota il corpo)
  python3 scripts/documento_approfondimento.py --verso-documento FILE
      (stampa il documento ricavato da un approfondimento già fatto a caselle)
"""
import argparse, re, sys
from pathlib import Path
import yaml

CAMPI_DOC = ('catenaccio', 'punto', 'tema', 'movimenti', 'domande')
# Righe in cima al testo preparato con l'IA: riempiono le caselle di servizio solo se sono vuote.
SERVIZIO = {'titolo': 'title', 'tema breve': 'tema_breve', 'titolo seo': 'seo_title',
            'meta description': 'description', 'parola chiave': 'focus_keyword',
            'idea per la foto di copertina': 'idea_foto'}
SI = {'sì', 'si', 'yes', 'true', 'vero'}


def _bool(v):
    return v.strip().lower() in SI


def _paragrafi(righe):
    """Righe → paragrafi (separati da righe vuote), ognuno su una riga sola se andava a capo."""
    out, cur = [], []
    for r in righe:
        if r.strip():
            cur.append(r.rstrip())
        elif cur:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def _unisci(p):
    """Un paragrafo: le righe di un elenco (1. / - ) restano a capo, le altre si uniscono."""
    if any(re.match(r'^\s*(\d+\.|[-*])\s', r) for r in p):
        return '\n'.join(p)
    return ' '.join(p)


class _Dumper(yaml.SafeDumper):
    pass


def _stringa(dumper, s):
    # Jekyll (YAML di Ruby) legge «28,7» o «1,234» come numeri interi: tra virgolette restano testo.
    if re.fullmatch(r'[-+]?[\d.,_:]+', s):
        return dumper.represent_scalar('tag:yaml.org,2002:str', s, style='"')
    return dumper.represent_str(s)


_Dumper.add_representer(str, _stringa)


def _etichetta(riga, ammesse):
    m = re.match(r'^([A-Za-zÀ-ÿ ]+?):\s?(.*)$', riga)
    if m and m.group(1).strip().lower() in ammesse:
        return m.group(1).strip().lower(), m.group(2).strip()
    return None


def _sezioni(righe, livello):
    """Divide le righe ai titoli del livello dato ('## ' o '### '): [(titolo|None, righe)]."""
    out, titolo, cur = [], None, []
    for r in righe:
        if r.startswith(livello) and not r.startswith(livello + '#'):
            out.append((titolo, cur)); titolo, cur = r[len(livello):].strip(), []
        else:
            cur.append(r)
    out.append((titolo, cur))
    return out


def _frase(righe):
    d = {'type': 'frase'}
    grande, mappa = [], {'sotto': 'sotto', 'foto': 'image', 'descrizione foto': 'image_alt',
                         'foto generata': 'generata', 'foto intera': 'adatta', 'didascalia': 'didascalia'}
    for r in righe:
        e = _etichetta(r, mappa)
        if e:
            k = mappa[e[0]]
            d[k] = _bool(e[1]) if k in ('generata', 'adatta') else e[1]
        elif r.strip():
            grande.append(r.strip())
    d['grande'] = '\n'.join(grande) + '\n'
    ordine = ['type', 'grande', 'sotto', 'image', 'image_alt', 'generata', 'adatta', 'didascalia']
    return {k: d[k] for k in ordine if k in d}


def _tabella(titolo, righe):
    d = {'type': 'dati', 'titolo': titolo, 'colonna': 'Numero'}
    mappa = {'didascalia': 'didascalia', 'colonna': 'colonna', 'limite': 'limite'}
    voce_k = {'numero': 'cifra', 'cifra': 'cifra', 'unità': 'unita', 'unita': 'unita', 'cosa': 'testo', 'fonte': 'fonte'}
    celle, voci, cur = [], [], {}
    for r in righe + ['']:
        e = _etichetta(r, set(mappa) | set(voce_k))
        if e and e[0] in voce_k:
            k = voce_k[e[0]]
            if k == 'cifra' and cur:
                voci.append(cur); cur = {}
            cur[k] = e[1]
            continue
        if not r.strip() and cur:
            voci.append(cur); cur = {}
        if e:
            d[mappa[e[0]]] = e[1]
        elif r.strip().startswith('|'):
            c = [x.strip() for x in r.strip().strip('|').split('|')]
            if all(re.fullmatch(r':?-{2,}:?', x) for x in c):
                continue
            celle.append(c)
    righe_t = [{'cifra': c[0], 'unita': c[1], 'testo': c[2], 'fonte': c[3]} for c in celle[1:]]
    for v in voci:
        f = v.get('fonte', '')
        if f and not f.lower().startswith('fonte'):
            f = 'Fonte: ' + f
        righe_t.append({'cifra': v.get('cifra', ''), 'unita': v.get('unita', ''), 'testo': v.get('testo', ''), 'fonte': f})
    d['righe'] = righe_t
    ordine = ['type', 'titolo', 'didascalia', 'colonna', 'righe', 'limite']
    return {k: d[k] for k in ordine if k in d}


def pulisci(corpo):
    """Toglie lo «sporco» tipico delle IA (ChatGPT, Grok, Gemini...): blocco di codice con chiacchiere
    intorno, titoletti ed etichette in grassetto, spazi strani."""
    t = corpo.replace('\r\n', '\n').replace('\u00a0', ' ')
    m = re.search(r'```[^\n]*\n(.*?)```', t, re.S)
    if m and '## ' in m.group(1):
        t = m.group(1)
    out = []
    for r in t.split('\n'):
        r = re.sub(r'^\s*(#{2,3})\s*\*\*(.*?)\*\*\s*$', r'\1 \2', r)   # ## **Titolo**
        r = re.sub(r'^\s*(#{2,3})(?=[^#\s])', r'\1 ', r)                # ##Titolo
        r = re.sub(r'^\s*(#{2,3}) ', r'\1 ', r)                          #   ## Titolo
        r = re.sub(r'^\s*\*\*([^*]+?):\*\*\s*', r'\1: ', r)              # **Etichetta:** testo
        r = re.sub(r'^\s*\*\*([^*]+?)\*\*\s*:\s*', r'\1: ', r)          # **Etichetta**: testo
        out.append(r.rstrip())
    return '\n'.join(out)


def analizza(corpo):
    righe = pulisci(corpo).split('\n')
    campi, movimenti = {}, []
    for titolo, blocco in _sezioni(righe, '## '):
        if titolo is None:
            for r in blocco:
                e = _etichetta(r, {'catenaccio', 'il punto'} | set(SERVIZIO))
                if e and e[1]:
                    campi[SERVIZIO.get(e[0]) or ('catenaccio' if e[0] == 'catenaccio' else 'punto')] = e[1]
            continue
        nome = titolo.split(':', 1)[0].strip()
        if nome.lower() == 'apertura':
            tema = {'titolo': titolo.split(':', 1)[1].strip() if ':' in titolo else ''}
            testo = []
            for r in blocco:
                e = _etichetta(r, {'sottotitolo'})
                if e:
                    tema['catenaccio'] = e[1]
                else:
                    testo.append(r)
            tema['apertura'] = '\n\n'.join(_unisci(p) for p in _paragrafi(testo)) + '\n'
            campi['tema'] = tema
        elif nome.lower() == 'domande':
            voce = re.compile(r'^([-*•]|\d+[.)])\s*')
            campi['domande'] = [voce.sub('', r.strip()) for r in blocco if voce.match(r.strip())]
        else:
            m = {'nome': nome, 'titolo': titolo}
            parti = _sezioni(blocco, '### ')
            for r in parti[0][1]:
                e = _etichetta(r, {'indice', 'sommario', 'colonne'})
                if e:
                    if e[0] == 'sommario':
                        m['sommario'] = [x.strip() for x in e[1].split(';') if x.strip()]
                    elif e[0] == 'colonne':
                        m['colonne'] = int(e[1])
                    else:
                        m['indice'] = e[1]
            blocchi, dopo = [], []
            for t, rr in parti[1:]:
                if t.lower() == 'frase rossa':
                    dopo.append(_frase(rr))
                elif t.lower().startswith('tabella'):
                    dopo.append(_tabella(t.split(':', 1)[1].strip() if ':' in t else '', rr))
                else:
                    blocchi.append({'titolo': t, 'tipo': 'domanda' if t.endswith('?') else 'testo',
                                    'testo': '\n\n'.join(_unisci(p) for p in _paragrafi(rr))})
            m['blocchi'] = blocchi
            if dopo:
                m['dopo'] = dopo
            ordine = ['nome', 'titolo', 'indice', 'sommario', 'colonne', 'blocchi', 'dopo']
            movimenti.append({k: m[k] for k in ordine if k in m})
    if movimenti:
        campi['movimenti'] = movimenti
    return campi


def verso_documento(fm):
    """Il giro contrario: da un approfondimento a caselle al documento (per migrare e per le prove)."""
    o = []
    if fm.get('catenaccio'): o.append('Catenaccio: ' + fm['catenaccio'])
    if fm.get('punto'): o.append('Il punto: ' + fm['punto'])
    t = fm.get('tema') or {}
    if t:
        o += ['', '## Apertura: ' + t.get('titolo', '')]
        if t.get('catenaccio'): o.append('Sottotitolo: ' + t['catenaccio'])
        o += ['', t.get('apertura', '').strip()]
    for m in fm.get('movimenti', []):
        o += ['', '## ' + m['titolo']]
        if m.get('indice'): o.append('Indice: ' + m['indice'])
        if m.get('sommario'): o.append('Sommario: ' + '; '.join(m['sommario']))
        if m.get('colonne'): o.append('Colonne: ' + str(m['colonne']))
        for b in m.get('blocchi', []):
            o += ['', '### ' + b['titolo'], b['testo'].strip()]
        for d in m.get('dopo', []):
            if d.get('type') == 'frase':
                o += ['', '### Frase rossa', d.get('grande', '').strip()]
                for k, et in (('sotto', 'Sotto'), ('image', 'Foto'), ('image_alt', 'Descrizione foto')):
                    if d.get(k): o.append(f'{et}: {d[k]}')
                for k, et in (('generata', 'Foto generata'), ('adatta', 'Foto intera')):
                    if k in d: o.append(f'{et}: {"sì" if d[k] else "no"}')
                if d.get('didascalia'): o.append('Didascalia: ' + d['didascalia'])
            elif d.get('type') == 'dati':
                o += ['', '### Tabella: ' + d.get('titolo', '')]
                if d.get('didascalia'): o.append('Didascalia: ' + d['didascalia'])
                if d.get('colonna', 'Importo') != 'Numero': o.append('Colonna: ' + d.get('colonna', 'Importo'))  # senza, il layout scriveva Importo
                for r in d.get('righe', []):
                    fonte = re.sub(r'^Fonte:\s*', '', r['fonte'])
                    o += ['', f"Numero: {r['cifra']}", f"Unità: {r['unita']}", f"Cosa: {r['testo']}", f"Fonte: {fonte}"]
                o.append('')
                if d.get('limite'): o.append('Limite: ' + d['limite'])
    if fm.get('domande'):
        o += ['', '## Domande'] + ['- ' + q for q in fm['domande']]
    return '\n'.join(o) + '\n'


def dividi(testo):
    m = re.match(r'^---\n(.*?)\n---\n?(.*)$', testo, re.S)
    return (m.group(1), m.group(2)) if m else (None, testo)


def seconda_foto(campi, fm):
    """La casella «Seconda foto» va accanto alla prima frase rossa (e vince su una foto scritta nel testo)."""
    if not fm.get('foto2'):
        return
    for m in campi.get('movimenti', []):
        for x in m.get('dopo', []):
            if x.get('type') == 'frase':
                for k in ('image', 'image_alt', 'generata', 'adatta', 'didascalia'):
                    x.pop(k, None)
                x['image'] = fm['foto2']
                if fm.get('foto2_alt'): x['image_alt'] = fm['foto2_alt']
                x['generata'] = bool(fm.get('foto2_generata', True))
                if fm.get('foto2_intera'): x['adatta'] = True
                if fm.get('foto2_didascalia'): x['didascalia'] = fm['foto2_didascalia']
                return
    print('ATTENZIONE: c\'è la seconda foto ma nel testo manca la frase rossa, la foto non esce')


def applica(cartelle):
    fatti = 0
    for c in cartelle:
        for f in sorted(Path(c).glob('*.md')):
            testo = f.read_text(encoding='utf-8')
            fm_txt, corpo = dividi(testo)
            if fm_txt is None or '## ' not in pulisci(corpo):
                continue
            if 'ECCO IL MIO ARTICOLO' in corpo:  # nella casella c'è ancora il prompt, non la risposta dell'IA
                print(f'ATTENZIONE {f}: nella casella c\'è ancora il prompt, non il testo dell\'IA: lo salto')
                continue
            campi = analizza(corpo)
            fm = yaml.safe_load(fm_txt) or {}
            seconda_foto(campi, fm)
            for k in SERVIZIO.values():  # le caselle di servizio già riempite vincono sul testo
                if k in campi and fm.get(k) not in (None, ''):
                    del campi[k]
            presenti = [k for k in campi if k in fm]
            pieni = [k for k in presenti if fm.get(k) not in (None, '', [], {})]
            if pieni:
                print(f'ATTENZIONE {f}: {pieni} sia nelle caselle sia nel documento, vince il documento')
            n_dv = corpo.count('DA VERIFICARE')
            if n_dv:
                print(f'ATTENZIONE {f}: {n_dv} punti [DA VERIFICARE]')
            if presenti:
                righe = fm_txt.split('\n'); tenute, salta = [], False
                for r in righe:
                    chiave = re.match(r'^([A-Za-z_]+):', r)
                    if chiave:
                        salta = chiave.group(1) in campi
                    if not salta:
                        tenute.append(r)
                fm_txt = '\n'.join(tenute)
            nuovo = '---\n' + fm_txt.rstrip('\n') + '\n' + yaml.dump(
                campi, Dumper=_Dumper, allow_unicode=True, sort_keys=False, width=10000) + '---\n'
            f.write_text(nuovo, encoding='utf-8')
            fatti += 1
            print(f'documento → caselle: {f}')
    print(f'approfondimenti scritti come documento: {fatti}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--applica', nargs='+', metavar='CARTELLA')
    ap.add_argument('--verso-documento', metavar='FILE')
    a = ap.parse_args()
    if a.applica:
        applica(a.applica)
    elif a.verso_documento:
        fm_txt, _ = dividi(Path(a.verso_documento).read_text(encoding='utf-8'))
        sys.stdout.write(verso_documento(yaml.safe_load(fm_txt)))
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
