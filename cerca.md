---
layout: default
title: Cerca
permalink: /cerca/
description: "Cerca tra tutti gli articoli di Rosso di Sera per parola chiave, autore o tema."
sitemap: false
---

<section class="search-section">
    <header class="section-header">
        <span class="section-label">Cerca nel blog</span>
        <h1 class="section-title">Cerca</h1>
    </header>

    <div class="search-box">
        <input
            type="search"
            id="search-input"
            data-index="{{ '/search-index.json' | relative_url }}"
            placeholder="Cerca per parola, autore o tema…"
            autocomplete="off"
            aria-label="Cerca tra gli articoli"
            disabled>
    </div>

    <p id="search-status" class="search-status" aria-live="polite"></p>
    <div id="search-results" class="search-results"></div>
</section>

<script src="{{ '/assets/js/vendor/minisearch.min.js' | relative_url }}?v={{ site.time | date: '%s' }}"></script>
<script src="{{ '/assets/js/search.js' | relative_url }}?v={{ site.time | date: '%s' }}"></script>
