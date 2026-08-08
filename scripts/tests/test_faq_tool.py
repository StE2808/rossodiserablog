# -*- coding: utf-8 -*-
"""Test di faq_tool. Nessun accesso ai post reali: solo fixture inline."""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from faq_tool import (find_faq_section, parse_jsonld, parse_visible, normalize,
                      render_accordion, to_accordion, sync_visible, compare)

POST_BOLD = """---
title: Prova
---

## Un paragrafo

Testo.

## Domande frequenti

**Che cos'e il pull?**

Sei tu ad andare a cercare l'informazione.

**Che cos'e il push?**

E' qualcun altro a mandartela.

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "Che cos'e il pull?",
      "acceptedAnswer": { "@type": "Answer", "text": "Sei tu ad andare a cercare l'informazione." } },
    { "@type": "Question", "name": "Che cos'e il push?",
      "acceptedAnswer": { "@type": "Answer", "text": "E' qualcun altro a mandartela." } }
  ]
}
</script>
"""

POST_NO_VISIBLE = """---
title: Prova
---

## Un paragrafo

Testo.

<script type="application/ld+json">
{
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Domanda unica?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Risposta unica."
      }
    }
  ]
}
</script>
"""


# --- find_faq_section ---

def test_find_faq_section_trova_h2():
    start, end = find_faq_section(POST_BOLD)
    assert POST_BOLD[start:end].startswith("## Domande frequenti")
    assert "<script" not in POST_BOLD[start:end]


def test_find_faq_section_assente():
    assert find_faq_section(POST_NO_VISIBLE) is None


def test_find_faq_section_intestazione_alternativa():
    testo = POST_BOLD.replace("## Domande frequenti", "## Domande e risposte")
    assert find_faq_section(testo) is not None


def test_find_faq_section_ignora_h2_narrativo():
    testo = POST_NO_VISIBLE.replace("## Un paragrafo", "## La domanda difficile")
    assert find_faq_section(testo) is None


# --- parse_jsonld ---

def test_parse_jsonld_formato_compatto():
    pairs = parse_jsonld(POST_BOLD)
    assert len(pairs) == 2
    assert pairs[0]["q"] == "Che cos'e il pull?"
    assert pairs[0]["a"] == "Sei tu ad andare a cercare l'informazione."


def test_parse_jsonld_formato_indentato():
    assert parse_jsonld(POST_NO_VISIBLE) == [{"q": "Domanda unica?", "a": "Risposta unica."}]


def test_parse_jsonld_assente():
    assert parse_jsonld("nessuno schema qui") is None


# --- parse_visible ---

def test_parse_visible_formato_grassetto():
    pairs = parse_visible(POST_BOLD)
    assert len(pairs) == 2
    assert pairs[1]["q"] == "Che cos'e il push?"
    assert pairs[1]["a"] == "E' qualcun altro a mandartela."


# --- normalize ---

def test_normalize_virgolette_curve():
    assert normalize("“ciao” e l’auto") == '"ciao" e l\'auto'


def test_normalize_caratteri_invisibili():
    assert normalize("te​sto") == "testo"


def test_normalize_toglie_i_link_markdown():
    assert normalize("con [un link](/slug/) dentro") == "con un link dentro"


def test_normalize_toglie_enfasi():
    assert normalize("il *pull* e il **push**") == "il pull e il push"


# --- render_accordion / to_accordion ---

def test_render_accordion_struttura():
    out = render_accordion([{"q": "Domanda?", "a": "Risposta."}], "## Domande frequenti")
    assert out.startswith("## Domande frequenti")
    assert '<details class="faq-item" markdown="1">' in out
    assert "<summary><h3>Domanda?</h3></summary>" in out
    assert "Risposta." in out
    assert out.rstrip().endswith("</details>")


def test_render_accordion_riga_vuota_dopo_summary():
    out = render_accordion([{"q": "D?", "a": "R."}], "## Domande frequenti")
    assert "</summary>\n\nR." in out


def test_to_accordion_conserva_intestazione_alternativa():
    testo = POST_BOLD.replace("## Domande frequenti", "## Domande e risposte")
    nuovo = to_accordion(testo)
    assert "## Domande e risposte" in nuovo
    assert "## Domande frequenti" not in nuovo


def test_to_accordion_preserva_il_testo():
    assert parse_visible(to_accordion(POST_BOLD)) == parse_visible(POST_BOLD)


def test_to_accordion_non_tocca_il_jsonld():
    assert parse_jsonld(to_accordion(POST_BOLD)) == parse_jsonld(POST_BOLD)


def test_to_accordion_idempotente():
    una = to_accordion(POST_BOLD)
    assert to_accordion(una) == una


# --- compare ---

def test_compare_ok():
    assert compare(POST_BOLD) == []


def test_compare_segnala_visibile_mancante():
    problemi = compare(POST_NO_VISIBLE)
    assert len(problemi) == 1
    assert "manca il testo visibile" in problemi[0]


def test_compare_segnala_testo_divergente():
    # solo la prima occorrenza: nel fixture il testo visibile precede il JSON-LD
    rotto = POST_BOLD.replace("Sei tu ad andare a cercare l'informazione.", "Testo diverso.", 1)
    assert any("risposta 1" in p for p in compare(rotto))


def test_compare_segnala_conteggio_diverso():
    rotto = POST_BOLD.replace("**Che cos'e il push?**\n\nE' qualcun altro a mandartela.\n", "")
    problemi = compare(rotto)
    assert any("2 nel JSON-LD" in p and "1 visibili" in p for p in problemi)


def test_compare_ignora_apostrofi_curvi():
    curvo = POST_BOLD.replace("l'informazione", "l’informazione")
    assert compare(curvo) == []


def test_compare_ignora_i_link_markdown():
    linkato = POST_BOLD.replace(
        "Sei tu ad andare a cercare l'informazione.",
        "Sei tu ad [andare a cercare](/un-articolo/) l'informazione.")
    assert compare(linkato) == []


# --- sync_visible ---

def test_sync_visible_inserisce_prima_dello_script():
    nuovo = sync_visible(POST_NO_VISIBLE)
    assert nuovo.index("## Domande frequenti") < nuovo.index("<script")


def test_sync_visible_testo_verbatim():
    assert compare(sync_visible(POST_NO_VISIBLE)) == []


def test_sync_visible_formato_accordion():
    assert "<summary><h3>Domanda unica?</h3></summary>" in sync_visible(POST_NO_VISIBLE)


def test_sync_visible_non_tocca_chi_ce_l_ha_gia():
    assert sync_visible(POST_BOLD) == POST_BOLD


def test_sync_visible_idempotente():
    una = sync_visible(POST_NO_VISIBLE)
    assert sync_visible(una) == una


# --- is_self_referential ---

def test_self_referential_riconosce_il_rimando_al_pezzo():
    from faq_tool import is_self_referential
    assert is_self_referential("Qual e la conclusione dell'articolo?")
    assert is_self_referential("Che cosa si intende per populismo in questo articolo?")


def test_self_referential_ignora_gli_articoli_di_legge():
    from faq_tool import is_self_referential
    assert not is_self_referential("Perche il piano e in tensione con l'articolo 33 della Costituzione?")
    assert not is_self_referential("Cosa prevede l'articolo 21 sulla liberta di stampa?")


def test_self_referential_falso_su_domanda_normale():
    from faq_tool import is_self_referential
    assert not is_self_referential("Cos'e la manipolazione algoritmica?")
