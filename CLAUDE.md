# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Aurobase (奧洛科技)** — Taiwanese digital marketing and AI solutions company website. Multi-page static HTML site with a PHP backend for form submissions. Hosted on GitHub Pages at `aurobase.com`.

## Development

No build system. All HTML, CSS, and JS are edited directly. To preview locally:

```bash
python3 -m http.server 8000
# PHP form submission requires:
php -S localhost:8000
```

CSS is compiled from SCSS:

```bash
sass scss/style.scss css/style.css --style=expanded
```

Only edit `scss/style.scss` — `scss/bootstrap/` is vendored Bootstrap 4.1, do not modify.

## Deployment

Say **"push"** to commit and publish to GitHub. Remote is already configured:

```
https://github.com/cacotealeaf-sudo/Aurobase  (origin/main)
```

GitHub Pages auto-deploys to `aurobase.com` on push to `main`. PHP backend requires a separate server.

## Page Structure

| File | Purpose |
|------|---------|
| `index.html` | Homepage |
| `marketing.html` | Digital marketing services |
| `solution.html` | Marketing automation & CDP products |
| `ai-companion.html` | AI voice companion for elder care |
| `nexus.html` | AURO NEXUS platform hub (1,500+ lines) |
| `nexus-geo.html` | NEXUS GEO standalone page (GEO color: `#384FB5`/`#3F58CA`) |
| `contact.html` | Contact form + inquiry modal |
| `blog.html` + `blogpost/` | Blog listing + articles |

## nexus.html Architecture

Four product sections follow the pattern **Product Banner → Pain Section → Feature Section → FAQ Section**, separated by large HTML comments (`╔══ NEXUS X ══╗`):

1. **NEXUS OS** (`id="nexus-v4"`)
2. **NEXUS CDP** (`id="nexus-cdp"`) — includes a tabbed panel with CDP / GEO sub-tabs
3. **NEXUS Voice** (`id="nexus-voice"`)

The page has a large scoped `<style>` block at the top (~450 lines). Add new nexus-only styles there, not in `css/style.css`.

### section-label / section-heading pattern

These two utility classes are **defined inside nexus.html's scoped `<style>`** (not in global CSS):

- `.section-label` — default `color: #F96D00`, `font-size: 0.78rem`, uppercase
- `.section-heading` — default `color: #28282c` (dark), `font-size: 1.6rem`

**On dark-background sections, the heading defaults to dark and becomes invisible.** Always add explicit overrides with `!important` for any dark section:

```css
.my-dark-section .section-label  { color: rgba(255,255,255,0.5) !important; }
.my-dark-section .section-heading { color: #fff !important; }
```

nexus-geo.html has its own scoped `<style>` block that follows this same pattern.

## CSS Architecture

- **`css/style.css`** — primary stylesheet (Bootstrap 4.1 base + custom styles). Do not edit directly; edit `scss/style.scss` and recompile.
- Primary brand color: `#F96D00` (orange)
- GEO product color: `#384FB5` (dark) / `#3F58CA` (light)
- Typography: LINE Seed TW (WOFF2 in `/WOFF2/`)
- Bootstrap 4 grid (xs/sm/md/lg/xl)
- Prefer page-scoped `<style>` blocks over inline styles or additions to `css/style.css`

## Page Layout System

All pages use a left-sidebar layout via `#colorlib-page`:

```
#colorlib-page
  ├── #colorlib-aside  (340px fixed sidebar — nav + logo)
  └── #colorlib-main   (remaining width, margin-left: 340px)
```

The nav sidebar and footer are copy-pasted across pages (no templating engine). When adding a new page, copy both from an existing page and update the `class="active"` nav item.

## JavaScript

jQuery 3.2.1 — no modern framework. `js/main.js` is legacy; `js/main_optimized.js` is the active version (navigation, AOS animations, carousels).

Custom scripts:
- `js/qform.js` — submits to Google Forms, manages checkbox state
- `js/form-validator.js` — client-side validation (email, phone, name)
- `js/rate-limiter.js` — 1 submission per 60s via localStorage

## Inquiry Modal

The floating button + `#myModal` form appears on every page. The modal form submits service-interest checkboxes + contact info to Google Forms via `qform.js`. When creating a new product page, pre-check the relevant service checkbox in the modal by adding `checked` to its `<input>`.

## PHP Backend (`/api/`)

- `api/submit-form.php` — validates + submits to Google Forms via cURL; rate-limits by IP (1/60s), logs to `/logs/`
- `api/config/.env` — git-ignored; use `api/config/.env.example` as template

## SEO / Analytics

- Google Tag Manager: `GTM-MB9RNG8` — must be in `<head>` of every page
- JSON-LD FAQ schema on nexus-geo.html and index.html
- OG meta + canonical URL required on every page

## Language

All UI copy in Traditional Chinese (`lang="zh-hant-TW"`). Product names (AURO NEXUS, NEXUS GEO, etc.) stay in English.
