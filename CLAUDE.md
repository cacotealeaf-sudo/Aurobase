# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Aurobase (奧洛科技)** — Taiwanese digital marketing and AI solutions company website. Multi-page static HTML site with a PHP backend for form submissions. Hosted on GitHub Pages at `aurobase.com`.

## Development

No build system. All HTML, CSS, and JS are edited directly. To preview locally:

```bash
# Simple static server (Python)
python3 -m http.server 8000

# PHP backend requires a PHP server for form submission
php -S localhost:8000
```

CSS is compiled from SCSS source at `scss/style.scss` → `css/style.css`. If you need to recompile:

```bash
sass scss/style.scss css/style.css --style=expanded
```

## Architecture

### Page Structure

Each HTML page is self-contained with shared nav/footer patterns (no templating engine — copy-paste with modifications). Pages:

| File | Purpose |
|------|---------|
| `index.html` | Homepage — services overview |
| `marketing.html` | Digital marketing services |
| `solution.html` | Marketing automation & CDP products |
| `ai-companion.html` | AI voice companion for elder care |
| `nexus.html` | AURO NEXUS platform (newest, 72KB) |
| `contact.html` | Contact form + inquiry modal |
| `blog.html` + `blogpost/` | Blog listing + 4 articles |

### CSS Architecture

- **`css/style.css`** (8,987 lines) — primary stylesheet. Combines Bootstrap 4.1 base with custom Aurobase styles.
- Primary brand color: `#ff4816` (orange)
- Typography: LINE Seed TW (WOFF2 fonts in `/WOFF2/`)
- Bootstrap 4 grid (xs/sm/md/lg/xl breakpoints)
- Avoid inline styles; use `css/style.css` or scoped `<style>` blocks in pages as last resort.

### JavaScript Stack

jQuery 3.2.1 based — no modern framework. Key custom scripts:

- **`js/main_optimized.js`** — navigation, carousels, AOS scroll animations
- **`js/qform.js`** — submits inquiry forms to Google Forms; manages checkbox state for service selection
- **`js/form-validator.js`** — client-side validation (email, phone, name)
- **`js/rate-limiter.js`** — prevents duplicate submissions via localStorage

### Form Submission Flow

```
User → modal form → form-validator.js → rate-limiter.js → qform.js
  → Google Forms (direct) OR api/submit-form.php (PHP fallback)
  → submit-form.php: server-side validation, sanitization, rate limiting by IP, logs to /logs/
```

The inquiry modal appears on all pages and submits service interest checkboxes alongside contact info.

### PHP Backend (`/api/`)

- `api/submit-form.php` — handles form POST, validates, submits to Google Forms via cURL
- `api/config/config.php` — reads credentials from `api/config/.env` (git-ignored)
- `api/config/.env.example` — template for environment setup
- Rate limit: 1 submission per 60 seconds per IP (file-based, stored in `/logs/`)

### Assets

- Images: `/images/` — prefer WebP with PNG fallback for new images
- System UI mockups: `/system_ui/` — NEXUS product screenshots added by team
- Fonts: `/WOFF2/` (LINESeedTW variants), `/fonts/`

## SEO / Analytics

- Google Tag Manager: `GTM-MB9RNG8` (in every page `<head>`)
- JSON-LD structured data on index.html (FAQ schema, Organization)
- OG meta tags on all pages
- Canonical URLs set per page
- `robots.txt`, `sitemap.xml` in root

## Deployment

Push to `main` branch → GitHub Pages auto-deploys to `aurobase.com` (CNAME). PHP backend requires a separate server; GitHub Pages only serves static files.

## Language

All pages are Traditional Chinese (`lang="zh-hant-TW"`). All UI copy should be in zh-Hant-TW unless explicitly English (e.g., product names like "AURO NEXUS").
