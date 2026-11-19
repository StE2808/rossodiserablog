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


def analizza(corpo):
    righe = corpo.replace('\r\n', '\n').split('\n')
    campi, movimenti = {}, []
    for titolo, blocco in _sezioni(righe, '## '):
        if titolo is None:
            for r in blocco:
                e = _etichetta(r, {'catenaccio', 'il punto'})
                if e:
                    campi['catenaccio' if e[0] == 'catenaccio' else 'punto'] = e[1]
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
            tema['apertura'] = '\n\n'.join(' '.join(p) for p in _paragrafi(testo)) + '\n'
            campi['tema'] = tema
        elif nome.lower() == 'domande':
            campi['domande'] = [r.strip()[1:].strip() for r in blocco if r.strip().startswith('-')]
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
                                    'testo': '\n\n'.join(' '.join(p) for p in _paragrafi(rr))})
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
                if d.get('colonna') and d['colonna'] != 'Numero': o.append('Colonna: ' + d['colonna'])
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


def applica(cartelle):
    fatti = 0
    for c in cartelle:
        for f in sorted(Path(c).glob('*.md')):
            testo = f.read_text(encoding='utf-8')
            fm_txt, corpo = dividi(testo)
            if fm_txt is None or '## ' not in corpo:
                continue
            campi = analizza(corpo)
            fm = yaml.safe_load(fm_txt) or {}
            presenti = [k for k in campi if k in fm]
            if presenti:
                print(f'ATTENZIONE {f}: {presenti} sia nelle caselle sia nel documento, vince il documento')
                righe = fm_txt.split('\n'); tenute, salta = [], False
                for r in righe:
                    chiave = re.match(r'^([A-Za-z_]+):', r)
                    if chiave:
                        salta = chiave.group(1) in campi
                    if not salta:
                        tenute.append(r)
                fm_txt = '\n'.join(tenute)
            nuovo = '---\n' + fm_txt.rstrip('\n') + '\n' + yaml.safe_dump(
                campi, allow_unicode=True, sort_keys=False, width=10000) + '---\n'
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
