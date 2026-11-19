---
layout: rivista-pagina
title: Gli approfondimenti
seo_title: "Approfondimenti di Rosso di Sera: un tema scavato a fondo"
description: "Tutti gli approfondimenti di Rosso di Sera, dal più recente: ogni volta un tema di politica, società o tecnologia spiegato a blocchi, con dati e fonti."
permalink: /approfondimenti/
---
{%- comment -%} Lo scaffale degli arretrati (17/11/2026, veste a rivista dal 19/11): tutti gli approfondimenti, dal più recente. Il più recente è anche in copertina nella home. {%- endcomment -%}
{%- assign tutti = site.posts | where: "approfondimento", true -%}
{% include testa-pagina.html etichetta="Gli arretrati" titolo="Gli approfondimenti" intro="Ogni volta un tema scavato a fondo, a blocchi, con i dati e le fonti. Il più recente è anche in copertina nella home." %}
{%- if tutti.size > 0 %}
<div class="scaffale">
{%- for a in tutti %}
<article>
<a href="{{ a.url | relative_url }}">
{% if a.image %}<img src="{{ a.image | relative_url }}" alt="" loading="lazy" width="520" height="650">{% endif %}
<div class="et">N. {{ a.numero }}{% if a.tema_breve %} · {{ a.tema_breve }}{% endif %}</div>
<h2>{{ a.title }}</h2>
<p>{{ a.punto | default: a.description }}</p>
</a>
</article>
{%- endfor %}
</div>
{%- else %}
<p class="p-vuoto">Il primo approfondimento sta per uscire.</p>
{%- endif %}
