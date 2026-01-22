---
layout: default
title: Archivio
permalink: /archivio/
---

<section class="archive-section">
    <header class="section-header">
        <span class="section-label">Tutti gli articoli</span>
        <h1 class="section-title">Archivio Completo</h1>
    </header>

    <div class="archive-container">
        {% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
        {% for year in posts_by_year %}

        <div class="archive-year-section">
            <h2 class="archive-year-title">{{ year.name }}</h2>

            {% assign posts_by_month = year.items | group_by_exp: "post", "post.date | date: '%m'" %}
            {% for month in posts_by_month %}

            {% assign month_name = month.items[0].date | date: "%B" %}
            <div class="archive-month-section">
                <h3 class="archive-month-title">{{ month_name }} {{ year.name }}</h3>

                <div class="archive-grid">
                    {% for post in month.items %}
                    <article class="related-card">
                        {% if post.image %}
                        <a href="{{ post.url | relative_url }}" class="related-image-link">
                            <img src="{{ post.image | relative_url }}" alt="{{ post.image_alt | default: post.title }}" loading="lazy">
                        </a>
                        {% endif %}
                        <div class="related-content">
                            {% if post.category %}
                            <a href="{{ '/categoria/' | append: post.category | relative_url }}" class="archive-category-tag">{{ post.category | replace: "-", " " }}</a>
                            {% endif %}
                            <h4 class="related-card-title">
                                <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                            </h4>
                            <div class="archive-card-meta">
                                <span class="related-date">{{ post.date | date: "%d %B %Y" }}</span>
                                <span class="archive-author">
                                    {% if post.author == "stefano-vozzi" %}
                                        Stefano Vozzi
                                    {% elsif post.author == "lino-rialti" %}
                                        Lino Rialti
                                    {% else %}
                                        {{ post.author | replace: "-", " " | capitalize }}
                                    {% endif %}
                                </span>
                            </div>
                        </div>
                    </article>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>

        {% endfor %}
    </div>
</section>
