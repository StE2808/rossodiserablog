# Istruzioni per Claude Code - Aggiornamento Rosso di Sera

## Panoramica del progetto

**Repository**: `https://github.com/StE2808/rossodiserablog`
**Branch**: `main`
**Tecnologie**: Jekyll + GitHub Pages + Sveltia CMS

---

## TASK 1: Aggiungere il campo Categoria al CMS

### File da modificare: `admin/config.yml`

Aggiungere il campo `category` nella sezione `fields` della collection `posts`, **dopo** il campo `author`:

```yaml
      - label: "Categoria"
        name: "category"
        widget: "select"
        options:
          - { label: "Società", value: "societa" }
          - { label: "Politica", value: "politica" }
          - { label: "Cronaca", value: "cronaca" }
          - { label: "Cultura", value: "cultura" }
          - { label: "Diritti Umani", value: "diritti-umani" }
          - { label: "Economia", value: "economia" }
          - { label: "Ambiente", value: "ambiente" }
          - { label: "Salute", value: "salute" }
          - { label: "Scuola", value: "scuola" }
          - { label: "Arte & Artisti", value: "arte-artisti" }
          - { label: "Altro", value: "altro" }
        required: true
```

### Posizione esatta nel file

Il campo va inserito dopo questo blocco:

```yaml
      - label: "Autore"
        name: "author"
        widget: "select"
        options:
          - { label: "Lino Rialti", value: "lino-rialti" }
          - { label: "StE2808", value: "ste2808" }
        required: true
```

---

## TASK 2: Nuovo Design del Blog

### Sostituire completamente i seguenti file con il nuovo design moderno:

### 2.1 File: `_layouts/default.html`

```html
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% if page.title %}{{ page.title }} | {% endif %}Rosso di Sera</title>
    <meta name="description" content="{{ page.excerpt | default: site.description | strip_html | truncate: 160 }}">
    
    <!-- SEO -->
    {% seo %}
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
    
    <!-- CSS -->
    <link rel="stylesheet" href="{{ '/assets/css/style.css' | relative_url }}">
</head>
<body>
    <!-- NAVBAR -->
    <nav class="navbar">
        <a href="{{ '/' | relative_url }}" class="navbar-brand">
            <img src="{{ '/assets/images/logo_trasparenza.png' | relative_url }}" alt="Rosso di Sera" class="navbar-logo">
            <span class="navbar-title">Rosso di Sera</span>
        </a>
        <ul class="navbar-links">
            <li><a href="{{ '/' | relative_url }}">Home</a></li>
            <li><a href="{{ '/archivio' | relative_url }}">Archivio</a></li>
            <li><a href="{{ '/autori' | relative_url }}">Autori</a></li>
            <li><a href="{{ '/contatti' | relative_url }}">Contatti</a></li>
        </ul>
    </nav>

    {{ content }}

    <!-- FOOTER -->
    <footer>
        <div class="footer-content">
            <div class="footer-brand">
                <h3>Rosso di Sera</h3>
                <p>Un blog di pensiero critico, riflessioni sulla società contemporanea e uno sguardo attento sul mondo che ci circonda. Una luce nel mondo digitale.</p>
            </div>
            <div class="footer-section">
                <h4>Navigazione</h4>
                <ul>
                    <li><a href="{{ '/' | relative_url }}">Home</a></li>
                    <li><a href="{{ '/archivio' | relative_url }}">Archivio</a></li>
                    <li><a href="{{ '/autori' | relative_url }}">Autori</a></li>
                    <li><a href="{{ '/contatti' | relative_url }}">Contatti</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h4>Categorie</h4>
                <ul>
                    <li><a href="#">Società</a></li>
                    <li><a href="#">Politica</a></li>
                    <li><a href="#">Cultura</a></li>
                    <li><a href="#">Economia</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h4>Autori</h4>
                <ul>
                    <li><a href="#">Lino Rialti</a></li>
                    <li><a href="#">Stefano Vozzi</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© {{ 'now' | date: "%Y" }} Rosso di Sera. Tutti i diritti riservati.</p>
            <div class="social-links">
                <a href="https://github.com/StE2808/rossodiserablog" aria-label="GitHub">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                    </svg>
                </a>
                <a href="{{ '/feed.xml' | relative_url }}" aria-label="RSS">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M4 11a9 9 0 019 9M4 4a16 16 0 0116 16"/>
                        <circle cx="5" cy="19" r="1"/>
                    </svg>
                </a>
            </div>
        </div>
    </footer>

    <script>
        // Navbar scroll effect
        const navbar = document.querySelector('.navbar');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    </script>
</body>
</html>
```

### 2.2 File: `_layouts/home.html`

```html
---
layout: default
---

<!-- HERO -->
<section class="hero">
    <div class="hero-decoration"></div>
    <div class="hero-decoration"></div>
    <div class="hero-decoration"></div>
    
    <div class="hero-content">
        <p class="hero-subtitle">Un blog di pensiero critico</p>
        <p class="hero-tagline">Una luce nel mondo digitale</p>
        <a href="#articoli" class="hero-cta">
            Esplora gli articoli
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14M5 12l7 7 7-7"/>
            </svg>
        </a>
    </div>

    <div class="scroll-indicator">
        <span></span>
        <p>Scorri</p>
    </div>
</section>

<!-- ARTICOLI -->
<section class="articles-section" id="articoli">
    <header class="section-header">
        <span class="section-label">Ultimi articoli</span>
        <h2 class="section-title">Pensieri e Riflessioni</h2>
    </header>

    <div class="articles-grid">
        {% for post in site.posts limit:10 %}
        <article class="article-card">
            {% if post.image %}
            <div class="article-image">
                <img src="{{ post.image | relative_url }}" alt="{{ post.title }}">
                {% if post.category %}
                <span class="article-category">{{ post.category }}</span>
                {% endif %}
            </div>
            {% endif %}
            <div class="article-content">
                <div class="article-meta">
                    <div class="article-author">
                        <div class="author-avatar">
                            {% assign author_initials = post.author | slice: 0, 2 | upcase %}
                            {{ author_initials }}
                        </div>
                        <span>{{ post.author | replace: "-", " " | capitalize }}</span>
                    </div>
                    <span>•</span>
                    <span>{{ post.date | date: "%d %B %Y" }}</span>
                </div>
                <h3 class="article-title">
                    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                </h3>
                <p class="article-excerpt">{{ post.excerpt | strip_html | truncate: 150 }}</p>
                {% if post.tags.size > 0 %}
                <div class="article-tags">
                    {% for tag in post.tags limit:3 %}
                    <span class="article-tag">{{ tag }}</span>
                    {% endfor %}
                </div>
                {% endif %}
            </div>
        </article>
        {% endfor %}
    </div>

    <div class="load-more-wrapper">
        <a href="{{ '/archivio' | relative_url }}" class="load-more-btn">
            Vedi tutti gli articoli
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
        </a>
    </div>
</section>
```

### 2.3 File: `_layouts/post.html`

```html
---
layout: default
---

<article class="post-single">
    <header class="post-header">
        {% if page.category %}
        <span class="post-category">{{ page.category }}</span>
        {% endif %}
        <h1 class="post-title">{{ page.title }}</h1>
        <div class="post-meta">
            <div class="post-author">
                <div class="author-avatar">
                    {% assign author_initials = page.author | slice: 0, 2 | upcase %}
                    {{ author_initials }}
                </div>
                <span>{{ page.author | replace: "-", " " | capitalize }}</span>
            </div>
            <span class="post-date">{{ page.date | date: "%d %B %Y" }}</span>
        </div>
    </header>

    {% if page.image %}
    <div class="post-featured-image">
        <img src="{{ page.image | relative_url }}" alt="{{ page.title }}">
    </div>
    {% endif %}

    <div class="post-content">
        {{ content }}
    </div>

    {% if page.tags.size > 0 %}
    <footer class="post-footer">
        <div class="post-tags">
            <span class="tags-label">Tag:</span>
            {% for tag in page.tags %}
            <span class="tag">{{ tag }}</span>
            {% endfor %}
        </div>
    </footer>
    {% endif %}

    <nav class="post-navigation">
        {% if page.previous.url %}
        <a href="{{ page.previous.url | relative_url }}" class="nav-prev">
            <span class="nav-label">← Precedente</span>
            <span class="nav-title">{{ page.previous.title | truncate: 50 }}</span>
        </a>
        {% endif %}
        {% if page.next.url %}
        <a href="{{ page.next.url | relative_url }}" class="nav-next">
            <span class="nav-label">Successivo →</span>
            <span class="nav-title">{{ page.next.title | truncate: 50 }}</span>
        </a>
        {% endif %}
    </nav>
</article>
```

### 2.4 File: `assets/css/style.css`

Sostituire completamente con questo CSS:

```css
/* ============================================
   ROSSO DI SERA - CSS MODERNO
   ============================================ */

:root {
    --rosso-primario: #8B1A1A;
    --rosso-scuro: #5C1010;
    --rosso-accent: #C23C3C;
    --crema: #FAF6F1;
    --crema-scuro: #EDE4D8;
    --testo: #2A2A2A;
    --testo-chiaro: #6B6B6B;
    --ombra: rgba(139, 26, 26, 0.15);
    --ombra-forte: rgba(0, 0, 0, 0.2);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: 'Outfit', sans-serif;
    background: var(--crema);
    color: var(--testo);
    line-height: 1.7;
    overflow-x: hidden;
}

/* ============================================
   NAVBAR
============================================ */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.navbar.scrolled {
    background: rgba(139, 26, 26, 0.95);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    padding: 0.7rem 2rem;
    box-shadow: 0 4px 30px var(--ombra);
}

.navbar-brand {
    display: flex;
    align-items: center;
    gap: 1rem;
    text-decoration: none;
    color: white;
}

.navbar-logo {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: contain;
    transition: transform 0.3s ease;
}

.navbar:hover .navbar-logo {
    transform: rotate(-10deg) scale(1.05);
}

.navbar-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.3rem;
    font-weight: 600;
    letter-spacing: 1px;
}

.navbar-links {
    display: flex;
    gap: 2rem;
    list-style: none;
}

.navbar-links a {
    color: rgba(255,255,255,0.85);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 400;
    letter-spacing: 0.5px;
    position: relative;
    transition: color 0.3s ease;
}

.navbar-links a::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--crema);
    transition: width 0.3s ease;
}

.navbar-links a:hover {
    color: white;
}

.navbar-links a:hover::after {
    width: 100%;
}

/* ============================================
   HERO
============================================ */
.hero {
    min-height: 100vh;
    background: linear-gradient(165deg, var(--rosso-scuro) 0%, var(--rosso-primario) 40%, var(--rosso-accent) 100%);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
        radial-gradient(circle at 20% 80%, rgba(255,255,255,0.03) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255,255,255,0.05) 0%, transparent 40%),
        radial-gradient(circle at 40% 40%, rgba(0,0,0,0.1) 0%, transparent 30%);
    pointer-events: none;
}

.hero-decoration {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.1);
    animation: float 20s infinite ease-in-out;
}

.hero-decoration:nth-child(1) {
    width: 600px;
    height: 600px;
    top: -200px;
    right: -200px;
    animation-delay: 0s;
}

.hero-decoration:nth-child(2) {
    width: 400px;
    height: 400px;
    bottom: -100px;
    left: -100px;
    animation-delay: -5s;
}

.hero-decoration:nth-child(3) {
    width: 200px;
    height: 200px;
    top: 30%;
    left: 10%;
    animation-delay: -10s;
}

@keyframes float {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    25% { transform: translate(20px, -20px) rotate(5deg); }
    50% { transform: translate(0, -40px) rotate(0deg); }
    75% { transform: translate(-20px, -20px) rotate(-5deg); }
}

.hero-content {
    text-align: center;
    color: white;
    z-index: 10;
    padding: 2rem;
    max-width: 900px;
}

.hero-subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 600;
    letter-spacing: 2px;
    margin-bottom: 1rem;
    animation: fadeInUp 1s ease 0.2s both;
}

.hero-tagline {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1.2rem, 3vw, 1.6rem);
    font-style: italic;
    opacity: 0.85;
    margin-bottom: 3rem;
    animation: fadeInUp 1s ease 0.4s both;
}

.hero-cta {
    display: inline-flex;
    align-items: center;
    gap: 0.8rem;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.3);
    color: white;
    padding: 1rem 2.5rem;
    font-size: 0.95rem;
    font-weight: 500;
    letter-spacing: 1px;
    text-decoration: none;
    border-radius: 50px;
    transition: all 0.4s ease;
    animation: fadeInUp 1s ease 0.6s both;
}

.hero-cta:hover {
    background: white;
    color: var(--rosso-primario);
    transform: translateY(-3px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

.hero-cta svg {
    transition: transform 0.3s ease;
}

.hero-cta:hover svg {
    transform: translateY(3px);
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(40px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.scroll-indicator {
    position: absolute;
    bottom: 3rem;
    left: 50%;
    transform: translateX(-50%);
    animation: bounce 2s infinite;
}

.scroll-indicator span {
    display: block;
    width: 2px;
    height: 40px;
    background: linear-gradient(to bottom, rgba(255,255,255,0.8), transparent);
    margin: 0 auto 0.5rem;
}

.scroll-indicator p {
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.6);
}

@keyframes bounce {
    0%, 100% { transform: translateX(-50%) translateY(0); }
    50% { transform: translateX(-50%) translateY(10px); }
}

/* ============================================
   SEZIONE ARTICOLI
============================================ */
.articles-section {
    padding: 6rem 2rem;
    max-width: 1400px;
    margin: 0 auto;
}

.section-header {
    text-align: center;
    margin-bottom: 4rem;
}

.section-label {
    font-size: 0.8rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--rosso-primario);
    margin-bottom: 1rem;
    display: block;
}

.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2.5rem, 5vw, 3.5rem);
    font-weight: 600;
    color: var(--testo);
}

/* Grid 2 colonne */
.articles-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
}

.article-card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    opacity: 0;
    transform: translateY(60px);
    animation: cardAppear 0.8s ease forwards;
}

.article-card:nth-child(1) { animation-delay: 0.1s; }
.article-card:nth-child(2) { animation-delay: 0.2s; }
.article-card:nth-child(3) { animation-delay: 0.3s; }
.article-card:nth-child(4) { animation-delay: 0.4s; }
.article-card:nth-child(5) { animation-delay: 0.5s; }
.article-card:nth-child(6) { animation-delay: 0.6s; }
.article-card:nth-child(7) { animation-delay: 0.7s; }
.article-card:nth-child(8) { animation-delay: 0.8s; }
.article-card:nth-child(9) { animation-delay: 0.9s; }
.article-card:nth-child(10) { animation-delay: 1s; }

@keyframes cardAppear {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.article-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 30px 60px rgba(139, 26, 26, 0.15);
}

.article-image {
    position: relative;
    height: 220px;
    overflow: hidden;
}

.article-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}

.article-card:hover .article-image img {
    transform: scale(1.08);
}

.article-category {
    position: absolute;
    top: 1rem;
    left: 1rem;
    background: var(--rosso-primario);
    color: white;
    padding: 0.4rem 1rem;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-radius: 20px;
}

.article-content {
    padding: 1.8rem;
}

.article-meta {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
    font-size: 0.85rem;
    color: var(--testo-chiaro);
}

.article-author {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.author-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--rosso-primario), var(--rosso-accent));
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 0.7rem;
    font-weight: 600;
}

.article-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-weight: 600;
    line-height: 1.3;
    margin-bottom: 0.8rem;
    color: var(--testo);
    transition: color 0.3s ease;
}

.article-title a {
    color: inherit;
    text-decoration: none;
}

.article-card:hover .article-title {
    color: var(--rosso-primario);
}

.article-excerpt {
    font-size: 0.95rem;
    color: var(--testo-chiaro);
    line-height: 1.7;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.article-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1.2rem;
}

.article-tag {
    background: var(--crema-scuro);
    color: var(--testo-chiaro);
    padding: 0.3rem 0.8rem;
    font-size: 0.75rem;
    border-radius: 15px;
    transition: all 0.3s ease;
}

.article-tag:hover {
    background: var(--rosso-primario);
    color: white;
}

/* ============================================
   LOAD MORE BUTTON
============================================ */
.load-more-wrapper {
    text-align: center;
    margin-top: 4rem;
}

.load-more-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.8rem;
    background: transparent;
    border: 2px solid var(--rosso-primario);
    color: var(--rosso-primario);
    padding: 1rem 2.5rem;
    font-family: 'Outfit', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
    letter-spacing: 1px;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.4s ease;
    text-decoration: none;
}

.load-more-btn:hover {
    background: var(--rosso-primario);
    color: white;
    transform: translateY(-3px);
    box-shadow: 0 15px 30px var(--ombra);
}

/* ============================================
   POST SINGOLO
============================================ */
.post-single {
    max-width: 800px;
    margin: 0 auto;
    padding: 8rem 2rem 4rem;
}

.post-header {
    text-align: center;
    margin-bottom: 3rem;
}

.post-category {
    display: inline-block;
    background: var(--rosso-primario);
    color: white;
    padding: 0.4rem 1.2rem;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-radius: 20px;
    margin-bottom: 1.5rem;
}

.post-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 700;
    line-height: 1.2;
    color: var(--testo);
    margin-bottom: 1.5rem;
}

.post-meta {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    color: var(--testo-chiaro);
    font-size: 0.95rem;
}

.post-author {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.post-featured-image {
    margin-bottom: 3rem;
    border-radius: 20px;
    overflow: hidden;
}

.post-featured-image img {
    width: 100%;
    height: auto;
}

.post-content {
    font-size: 1.1rem;
    line-height: 1.9;
}

.post-content p {
    margin-bottom: 1.5rem;
}

.post-content h2 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    margin: 2.5rem 0 1rem;
    color: var(--testo);
}

.post-content h3 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    margin: 2rem 0 1rem;
    color: var(--testo);
}

.post-content img {
    max-width: 100%;
    height: auto;
    border-radius: 10px;
    margin: 2rem 0;
}

.post-content blockquote {
    border-left: 4px solid var(--rosso-primario);
    padding-left: 1.5rem;
    margin: 2rem 0;
    font-style: italic;
    color: var(--testo-chiaro);
}

.post-footer {
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid var(--crema-scuro);
}

.post-tags {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
}

.tags-label {
    font-weight: 500;
    margin-right: 0.5rem;
}

.tag {
    background: var(--crema-scuro);
    color: var(--testo-chiaro);
    padding: 0.4rem 1rem;
    font-size: 0.85rem;
    border-radius: 20px;
}

.post-navigation {
    display: flex;
    justify-content: space-between;
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid var(--crema-scuro);
    gap: 2rem;
}

.nav-prev, .nav-next {
    flex: 1;
    text-decoration: none;
    color: var(--testo);
    padding: 1rem;
    border-radius: 10px;
    transition: background 0.3s ease;
}

.nav-prev:hover, .nav-next:hover {
    background: var(--crema-scuro);
}

.nav-next {
    text-align: right;
}

.nav-label {
    display: block;
    font-size: 0.8rem;
    color: var(--testo-chiaro);
    margin-bottom: 0.3rem;
}

.nav-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    font-weight: 600;
}

/* ============================================
   FOOTER
============================================ */
footer {
    background: var(--testo);
    color: white;
    padding: 5rem 2rem 2rem;
    margin-top: 4rem;
}

.footer-content {
    max-width: 1400px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 4rem;
}

.footer-brand h3 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    margin-bottom: 1rem;
}

.footer-brand p {
    color: rgba(255,255,255,0.6);
    font-size: 0.95rem;
    line-height: 1.8;
}

.footer-section h4 {
    font-size: 0.85rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    color: rgba(255,255,255,0.4);
}

.footer-section ul {
    list-style: none;
}

.footer-section li {
    margin-bottom: 0.8rem;
}

.footer-section a {
    color: rgba(255,255,255,0.7);
    text-decoration: none;
    transition: color 0.3s ease;
}

.footer-section a:hover {
    color: var(--rosso-accent);
}

.footer-bottom {
    max-width: 1400px;
    margin: 4rem auto 0;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.4);
}

.social-links {
    display: flex;
    gap: 1rem;
}

.social-links a {
    width: 40px;
    height: 40px;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255,255,255,0.6);
    transition: all 0.3s ease;
}

.social-links a:hover {
    background: var(--rosso-primario);
    border-color: var(--rosso-primario);
    color: white;
}

/* ============================================
   RESPONSIVE
============================================ */
@media (max-width: 1024px) {
    .footer-content {
        grid-template-columns: 1fr 1fr;
        gap: 3rem;
    }
}

@media (max-width: 768px) {
    .navbar-links {
        display: none;
    }

    .articles-grid {
        grid-template-columns: 1fr;
    }

    .footer-content {
        grid-template-columns: 1fr;
        text-align: center;
    }

    .footer-bottom {
        flex-direction: column;
        gap: 1.5rem;
    }

    .post-single {
        padding: 6rem 1rem 3rem;
    }

    .post-navigation {
        flex-direction: column;
    }

    .nav-next {
        text-align: left;
    }
}
```

### 2.5 File: `index.html` (nella root)

Sostituire il contenuto con:

```html
---
layout: home
---
```

---

## TASK 3: Creare pagina Contatti (opzionale)

### File da creare: `contatti.md`

```markdown
---
layout: default
title: Contatti
---

<div class="contact-page">
    <div class="contact-header">
        <h1>Contattaci</h1>
        <p>Hai domande, suggerimenti o vuoi collaborare? Scrivici!</p>
    </div>
    
    <form action="https://formspree.io/f/TUOCODICE" method="POST" class="contact-form">
        <div class="form-group">
            <label for="name">Nome</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" required>
        </div>
        <div class="form-group">
            <label for="message">Messaggio</label>
            <textarea id="message" name="message" rows="6" required></textarea>
        </div>
        <button type="submit" class="submit-btn">Invia messaggio</button>
    </form>
</div>
```

**Nota**: Per il form funzionante, registrarsi su https://formspree.io e sostituire `TUOCODICE` con l'endpoint fornito.

---

## TASK 4: Modificare visualizzazione autore Ste2808 → Stefano Vozzi

### 4.1 File: `admin/config.yml`

Nella sezione autori, modificare la label:

```yaml
      - label: "Autore"
        name: "author"
        widget: "select"
        options:
          - { label: "Lino Rialti", value: "lino-rialti" }
          - { label: "Stefano Vozzi", value: "ste2808" }
        required: true
```

**Nota**: Il `value` resta `ste2808` per non rompere i post esistenti, cambia solo la `label` visualizzata nel CMS.

### 4.2 File: `_authors/ste2808.md`

Aggiornare il nome visualizzato:

```yaml
---
name: Stefano Vozzi
username: ste2808
bio: "Co-fondatore di Rosso di Sera"
---
```

### 4.3 File: `_layouts/home.html` e `_layouts/post.html`

Aggiungere una mappatura per convertire lo slug in nome completo. Nel file `home.html`, sostituire la riga:

```html
<span>{{ post.author | replace: "-", " " | capitalize }}</span>
```

Con:

```html
{% if post.author == "ste2808" %}
  <span>Stefano Vozzi</span>
{% elsif post.author == "lino-rialti" %}
  <span>Lino Rialti</span>
{% else %}
  <span>{{ post.author | replace: "-", " " | capitalize }}</span>
{% endif %}
```

Stessa modifica nel file `post.html` per la sezione `.post-author`.

---

## TASK 5: Commit e Push

```bash
# Dalla cartella del repository
git add .
git commit -m "Nuovo design moderno + campo categoria nel CMS"
git push origin main
```

---

## Checklist finale

- [ ] `admin/config.yml` aggiornato con campo categoria
- [ ] `admin/config.yml` label autore cambiata in "Stefano Vozzi"
- [ ] `_authors/ste2808.md` aggiornato con nome "Stefano Vozzi"
- [ ] `_layouts/default.html` sostituito
- [ ] `_layouts/home.html` sostituito (con mappatura autori)
- [ ] `_layouts/post.html` sostituito (con mappatura autori)
- [ ] `assets/css/style.css` sostituito
- [ ] `index.html` aggiornato
- [ ] (Opzionale) `contatti.md` creato
- [ ] Commit e push eseguiti
- [ ] Verificare il sito dopo il deploy (1-2 minuti)

---

## Note importanti

1. **Backup**: Prima di sovrascrivere, fare backup dei file esistenti se necessario
2. **Logo**: Il nuovo design usa `/assets/images/logo_trasparenza.png` - assicurarsi che esista
3. **Font**: I nuovi font (Cormorant Garamond + Outfit) vengono caricati da Google Fonts
4. **Responsive**: Il design è già responsive (2 colonne desktop, 1 colonna mobile)

---

*Documento generato il 20 Dicembre 2024*
