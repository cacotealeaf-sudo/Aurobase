# New Index Page Design Spec

## Overview

Redesign `index.html` to include an interactive entry overlay (need-assessment quiz) and a modernized content layout inspired by `aurobase-real.html`, while keeping the existing colorlib sidebar layout and white + orange (#F96D00) brand identity.

## Architecture: Entry Overlay Inline (方案 A)

Entry overlay lives inside `index.html` as a `position: fixed` layer covering only the `#colorlib-main` area (right of sidebar). The sidebar remains visible and functional at all times.

```
+----------------+------------------------------------------+
|                |                                          |
|  #colorlib-    |  #colorlib-main                          |
|  aside (340px) |                                          |
|                |  +-- Entry Overlay (fixed) -----------+  |
|  Logo          |  | (covers main area only)            |  |
|  Nav           |  | Boot -> Quiz -> redirect to page   |  |
|  Social        |  +------------------------------------+  |
|                |                                          |
|                |  +-- Page Content (underneath) -------+  |
|                |  | Hero / Ticker / Services / ...     |  |
|                |  +------------------------------------+  |
+----------------+------------------------------------------+
```

## Entry Overlay

### Visibility Rules

- **First visit**: overlay is visible, covers `#colorlib-main`
- **Skip**: user clicks "Skip" -> overlay fades out, homepage content revealed
- **Quiz complete**: redirect to recommended sub-page via `window.location`
- **Return visit**: `localStorage` key `aurobase_entry_done=true` -> overlay hidden, homepage shown directly
- **Re-trigger**: small floating button (above existing inquiry float button) allows re-opening overlay

### Visual Style

White background + orange accent, matching existing brand. Uses LINE Seed TW font (already loaded). No emoji — single-color icons from Flaticon/Ionicons.

| Role | Color |
|------|-------|
| Background | `#ffffff` |
| Primary accent | `#F96D00` |
| Text (primary) | `#28282c` |
| Text (secondary) | `#999` |
| Borders | `rgba(0,0,0,0.06)` |
| Progress bar / highlights | `#F96D00` |

### Three Stages

#### Stage 1: Boot Animation

- Brand logo "AUROBASE" in large text, tagline below
- Sequential boot messages fade in (same concept as `aurobase-entry.html`):
  - `// 系統初始化...`
  - `// 載入數位行銷模組`
  - `// 連接 MarTech 平台`
  - `// 啟動 AI 分析引擎`
  - `// 版圖資料庫就緒`
  - `// 準備診斷系統`
- Thin progress bar fills from 0% to 100% in orange
- CTA button appears when complete: "開始診斷您的需求 ->"

#### Stage 2: Quiz (3 Questions)

Progress indicator: 3 dots at top (done / active / pending).

**Q1 — 核心挑戰**: 您目前最大的挑戰是？
| Code | Label | Key |
|------|-------|-----|
| 01 | 廣告效益 | ads |
| 02 | 客戶數據 | data |
| 03 | 服務效率 | service |
| 04 | AI 應用 | ai |

**Q2 — 企業規模**: 您的組織規模？
| Code | Label | Key |
|------|-------|-----|
| A | 中型企業 | sme |
| B | 大型企業 | enterprise |
| C | 集團組織 | group |
| D | 新創公司 | startup |

**Q3 — 成效期望**: 您希望多快看到成效？
| Code | Label | Key |
|------|-------|-----|
| I | 立即見效 | fast |
| II | 中期布局 | mid |
| III | 長期戰略 | long |
| IV | 尚在評估 | explore |

Options displayed in 2x2 grid. Each option card has: code label, title, short description. Selected state: orange left border + light orange background. "Next" button appears only after selection.

#### Stage 3: Result & Redirect

Shows recommended page(s) based on answers. Primary recommendation determined by Q1 answer:

| Q1 Answer | Primary Redirect |
|-----------|-----------------|
| ads (廣告效益) | `marketing.html` |
| data (客戶數據) | `solution.html` |
| service (服務效率) | `contact.html` |
| ai (AI 應用) | `ai-companion.html` |

Q2/Q3 serve as supplementary weight — if answers strongly suggest a secondary recommendation, show it alongside primary. Display 1-2 recommended "territory" cards with direct links. User can also click "重新診斷" to restart or "進入首頁" to dismiss overlay.

### Re-trigger Button

Positioned above the existing inquiry float button (bottom-right). Single-color icon (e.g., Flaticon compass or target icon) + text "需求診斷". Small, unobtrusive. Clicking it re-opens the overlay and resets quiz state.

```
                         +------------+
                         | [icon] 需求診斷 |  <- re-trigger
                         +------------+
                         +------------+
                         | [icon] 填單諮詢 |  <- existing
                         +------------+
```

## Homepage Content Sections

All content inside `#colorlib-main`, below the overlay. White background, orange accents. Styles go in a scoped `<style>` block inside `index.html` (following nexus.html pattern — not in `css/style.css`).

### Section 1: Hero

Two-column layout inside `#colorlib-main`.

```
+---------------------------+------------------------+
| Left (55%)                | Right (45%)            |
|                           |                        |
| Eyebrow: 您最專業的科技行銷顧問 | Label: // 核心服務版圖  |
|                           |                        |
| H1: 數位整合              | +-- 數位行銷 ----------+ |
|     行銷                  | | Google·FB·SEO·社群   | |
|     解決方案 (orange)      | +---------------------+ |
|                           | +-- MarTech -+-- 客服 -+ |
| Description paragraph     | | CDP·CXA    | CTI·CRM | |
|                           | +-----------+---------+ |
| [填寫諮詢表單]  了解服務 -> | +-- AI語伴 -+-- 諮詢 -+ |
|                           | | 語音互動   | 聯絡我們 | |
|                           | +-----------+---------+ |
+---------------------------+------------------------+
```

- Service cards on right are clickable, link to sub-pages
- Hover: left orange border appears (scaleY transition)
- Responsive: stacks vertically on mobile

### Section 2: Ticker

Horizontal scrolling marquee. Light gray background (`#f8f8f8`), top/bottom 1px border.
Orange symbols (◈ ⊞ ⬡ ◉ ⇌), dark gray text. CSS `@keyframes` infinite scroll.
Content duplicated for seamless loop.

### Section 3: Core Services

Section header: `// 01 — 核心服務` + title + "了解更多 ->" link to `marketing.html`.

Grid layout with 1px gap separator:
- **Featured card (full width)**: 數位行銷 — left side has description + tags, right side has 3 feature bullet points (Collisions / Communication / Collaboration)
- **Half-width cards**: 客服中心, AI 智慧語伴 — each with description + tags

Cards: white bg, hover -> slight gray (`#fafafa`). Tags in small bordered pills.

### Section 4: Solutions Grid

Section header: `// 02 — 解決方案 & 產品` + "查看全部 ->" link to `solution.html`.

3-column grid:
- Row 1: Acoustic CXA | CDP | HCL Unica
- Row 2: Magnolia CMS | AI 智慧語伴 (span 2 columns)

Each card: orange badge label, product name, subtitle, description, feature list with "—" prefix in orange.

### Section 5: Marquee

Large decorative text scrolling. Outlined text in `rgba(0,0,0,0.06)` stroke, key words ("AUROBASE", "AI 智慧") filled in orange. Background white with subtle radial gradient.

### Section 6: Partners

Label: `// 事業夥伴`. Five equal-width cells in a row:
Magnolia | HCL Software | 朋昶數位 | Acoustic | Google

Text only (no logo images). Gray text, hover -> dark text. Separated by 1px vertical borders.

### Section 7: CTA

Orange gradient background (mapping from real page's red gradient to orange tones).
White text. Large title "歡迎填寫諮詢表單", subtitle, button "立即諮詢 ->", contact info.
Subtle grain texture overlay for depth.

### Section 8: FAQ

Accordion-style expand/collapse. Reuse existing 3 FAQ items from current `index.html` JSON-LD:
1. 奧洛提供哪些數位行銷服務？
2. 什麼是數位整合行銷？
3. 行銷自動化能為企業帶來什麼效益？

Keep the JSON-LD structured data intact for SEO.

### Section 9: Footer

Copy from existing site footer pattern. Company info + copyright.

## Responsive Behavior

- **Desktop (>992px)**: sidebar visible, full layout as described
- **Tablet (768-992px)**: sidebar collapses (existing behavior), content sections reduce to 2-column where applicable
- **Mobile (<768px)**: Hero stacks vertically (text above, cards below). Service grid becomes single column. Solutions grid becomes single column. Partner cells wrap. Entry overlay goes full-screen.

## SEO Preservation

- Keep all existing `<head>` meta tags, JSON-LD, OG tags, canonical URL
- Keep GTM snippet
- Keep inquiry modal (`#myModal`) and floating button
- FAQ JSON-LD stays intact

## Files Modified

- `index.html` — full rewrite of `#colorlib-main` content + add entry overlay + scoped `<style>` block
- No changes to `css/style.css`, sidebar, nav, or other pages

## Not In Scope

- Changes to other pages (marketing.html, solution.html, etc.)
- Changes to sidebar navigation
- Changes to the inquiry modal
- New images or assets (text-based design only)
- NEXUS product pages
