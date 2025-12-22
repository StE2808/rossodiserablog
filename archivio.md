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
            <div class="archive-year-badge">{{ year.name }}</div>

            <div class="archive-posts">
                {% for post in year.items %}
                <article class="archive-card">
                    <div class="archive-card-header">
                        <span class="archive-date">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                                <line x1="16" y1="2" x2="16" y2="6"></line>
                                <line x1="8" y1="2" x2="8" y2="6"></line>
                                <line x1="3" y1="10" x2="21" y2="10"></line>
                            </svg>
                            {{ post.date | date: "%d %b" }}
                        </span>
                        {% if post.category %}
                        <a href="{{ '/categoria/' | append: post.category | relative_url }}" class="archive-category">{{ post.category }}</a>
                        {% endif %}
                    </div>

                    <h3 class="archive-title">
                        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                    </h3>

                    <div class="archive-card-footer">
                        <div class="archive-author">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                <circle cx="12" cy="7" r="4"></circle>
                            </svg>
                            {% if post.author == "stefano-vozzi" %}
                                Stefano Vozzi
                            {% elsif post.author == "lino-rialti" %}
                                Lino Rialti
                            {% else %}
                                {{ post.author | replace: "-", " " | capitalize }}
                            {% endif %}
                        </div>
                        {% if post.tags.size > 0 %}
                        <div class="archive-tags">
                            {% for tag in post.tags limit:2 %}
                            <span class="archive-tag">{{ tag }}</span>
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                </article>
                {% endfor %}
            </div>
        </div>

        {% endfor %}
    </div>
</section>
