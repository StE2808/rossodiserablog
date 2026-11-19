---
layout: rivista-pagina
title: Autori
seo_title: "Gli autori di Rosso di Sera"
description: "Chi scrive su Rosso di Sera: Lino Rialti, giornalista dal 1992, e Stefano Vozzi, nella comunicazione dal 1991."
permalink: /autori/
---
{% include testa-pagina.html etichetta="Chi scrive" titolo="Gli autori" %}
<div class="p-autori">
{%- for author in site.authors %}
{%- assign lista_au = site.posts | where: "author", author.short_name %}
<section class="p-autore" id="{{ author.short_name }}">
<div class="et">{{ author.position }}</div>
<h2><a href="{{ author.url | relative_url }}">{{ author.name }}</a></h2>
<div class="p-bio">{{ author.content }}</div>
<p class="meta">{{ lista_au.size }} articoli · <a href="{{ author.url | relative_url }}">tutti i suoi articoli</a></p>
<h3 class="et">Gli ultimi</h3>
<ul>{% for post in lista_au limit: 5 %}<li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>{% endfor %}</ul>
</section>
{%- endfor %}
</div>
