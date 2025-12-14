---
layout: default
title: Archivio
permalink: /archivio/
---

<h1 class="page-title">Archivio Completo</h1>

<div class="archive-list">
{% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
{% for year in posts_by_year %}
    <h2 class="archive-year">{{ year.name }}</h2>
    <ul class="archive-posts">
    {% for post in year.items %}
        <li>
            <span class="archive-date">{{ post.date | date: "%d %b" }}</span>
            <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
            <span class="archive-author">— {{ post.author | replace: "-", " " | capitalize }}</span>
        </li>
    {% endfor %}
    </ul>
{% endfor %}
</div>

<style>
.page-title {
    font-family: 'Playfair Display', serif;
    color: #8b1a1a;
    text-align: center;
    margin-bottom: 2rem;
}

.archive-year {
    color: #6b1414;
    border-bottom: 2px solid #f5ede4;
    padding-bottom: 0.5rem;
    margin: 2rem 0 1rem;
}

.archive-posts {
    list-style: none;
}

.archive-posts li {
    padding: 0.75rem 0;
    border-bottom: 1px solid #f0f0f0;
}

.archive-date {
    display: inline-block;
    width: 60px;
    color: #888;
    font-size: 0.9rem;
}

.archive-posts a {
    color: #333;
    text-decoration: none;
    font-weight: 500;
}

.archive-posts a:hover {
    color: #8b1a1a;
}

.archive-author {
    color: #888;
    font-size: 0.85rem;
    font-style: italic;
}
</style>
