---
layout: rivista-pagina
title: Archivio
seo_title: "Archivio di Rosso di Sera: tutti gli articoli"
description: "Tutti gli articoli di Rosso di Sera, mese per mese: politica italiana, esteri, società, opinioni, scienza, cultura ed economia."
permalink: /archivio/
---
{%- assign mesi_a = "gennaio,febbraio,marzo,aprile,maggio,giugno,luglio,agosto,settembre,ottobre,novembre,dicembre" | split: "," -%}
{%- capture conta -%}{{ site.posts.size }} articoli{%- endcapture -%}
{% include testa-pagina.html etichetta="Tutti gli articoli" titolo="Archivio" conta=conta intro="Mese per mese, dal più recente. Per argomento, scegli una categoria." %}
<nav class="p-categorie" aria-label="Categorie">
{%- for c in site.data.categorie %}{% unless c[1].tolta %}<a href="{{ '/categoria/' | append: c[0] | append: '/' | relative_url }}">{{ c[1].nome }}</a>{% endunless %}{% endfor -%}
</nav>
{%- assign per_mese = site.posts | group_by_exp: "x", "x.date | date: '%Y-%m'" -%}
{%- for m in per_mese %}
{%- assign im_a = m.items[0].date | date: "%-m" | minus: 1 %}
<section class="p-mese" aria-labelledby="m-{{ m.name }}">
<h2 id="m-{{ m.name }}" class="mov"><span class="sole" aria-hidden="true"></span>{{ mesi_a[im_a] | capitalize }} {{ m.items[0].date | date: "%Y" }}<i>{{ m.items.size }}</i></h2>
{% include elenco-articoli.html lista=m.items %}
</section>
{%- endfor %}
