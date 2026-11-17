---
layout: default
title: Gli approfondimenti
seo_title: "Approfondimenti di Rosso di Sera: un tema scavato a fondo"
description: "Tutti gli approfondimenti di Rosso di Sera, dal più recente: ogni volta un tema di politica, società o tecnologia spiegato a blocchi, con dati e fonti."
permalink: /approfondimenti/
# Finché non esce il primo approfondimento vero: nascosta. Al primo, togliere le due righe sotto e aggiungere il link nella barra.
noindex: true
sitemap: false
---
{%- comment -%} Lo scaffale degli arretrati (17/11/2026): tutti gli approfondimenti, dal più recente. Il più recente è anche in copertina nella home. {%- endcomment -%}
{%- assign tutti = site.posts | where: "approfondimento", true -%}
<style>
.scaffale{max-width:1100px;margin:0 auto;padding:2rem 16px 4rem}
.scaffale-griglia{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:2rem;margin-top:2rem}
.scaffale-griglia article a{color:inherit;text-decoration:none;display:block}
.scaffale-griglia img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;filter:grayscale(1);transition:filter .3s}
.scaffale-griglia a:hover img,.scaffale-griglia a:focus-visible img{filter:none}
.scaffale-griglia .n{font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;color:#c0392b;margin:.8rem 0 .3rem}
.scaffale-griglia h2{font-size:1.3rem;line-height:1.25;margin:0 0 .5rem}
.scaffale-griglia p{font-size:.95rem;line-height:1.5;margin:0}
</style>
<section class="scaffale">
  <header class="section-header">
    <span class="section-label">Gli arretrati</span>
    <h1 class="section-title">Gli approfondimenti</h1>
    <p>Ogni volta un tema scavato a fondo, a blocchi, con i dati e le fonti. Il più recente è anche in copertina nella home.</p>
  </header>
  {%- if tutti.size > 0 %}
  <div class="scaffale-griglia">
  {%- for a in tutti %}
    <article>
      <a href="{{ a.url | relative_url }}">
        {% if a.image %}<img src="{{ a.image | relative_url }}" alt="" loading="lazy" width="520" height="650">{% endif %}
        <div class="n">N. {{ a.numero }}{% if a.tema_breve %} · {{ a.tema_breve }}{% endif %} · <time datetime="{{ a.date | date_to_xmlschema }}">{{ a.date | date: "%d/%m/%Y" }}</time></div>
        <h2>{{ a.title }}</h2>
        <p>{{ a.punto | default: a.description }}</p>
      </a>
    </article>
  {%- endfor %}
  </div>
  {%- else %}
  <p>Il primo approfondimento sta per uscire.</p>
  {%- endif %}
</section>
