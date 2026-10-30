#!/usr/bin/env python3
"""產生 AURO NEXUS 產品頁（nexus-<slug>.html）、nexus.html 平台總覽、llms.txt 產品一覽與 sitemap。

內容在 tools/module-pages/<slug>.json（平台總覽在 _platform.json），共用外框在
tools/module-pages/chrome-*.html，樣式在 css/nexus-module.css。改內容後重跑：

    python3 tools/build-module-pages.py

內容有錯（缺欄位、連到不存在的產品…）時列出錯誤並以非零狀態結束，不寫任何檔案。
"draft": true 的產品不產頁、不進總覽；已產過的頁面會被移除。
新字與新圖示另跑 tools/build-font-subset.sh、tools/build-iconoir-subset.sh（GitHub Action 會代跑）。
編輯介面：python3 tools/cms/server.py。
JSON 內的文字欄位允許 <b> <em> <code> <a> 等行內標籤；結構化資料會去掉標籤。
"""
import datetime
import glob
import html
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'tools', 'module-pages')


def set_root(root):
    """讓編輯器與測試指向另一份網站目錄。"""
    global ROOT, SRC
    ROOT = os.path.normpath(root)
    SRC = os.path.join(ROOT, 'tools', 'module-pages')


SITE = 'https://aurobase.com'
ORG = {
    '@type': 'Organization',
    '@id': SITE + '/#organization',
    'name': '奧洛股份有限公司',
    'alternateName': ['Aurobase', '奧洛'],
    'url': SITE + '/',
    'logo': SITE + '/images/logo.svg',
    'address': {'@type': 'PostalAddress', 'streetAddress': '洲子街101號2樓', 'addressLocality': '內湖區',
                'addressRegion': '台北市', 'addressCountry': 'TW'},
    'telephone': '+886-2-5568-4688',
    'sameAs': ['https://www.facebook.com/AurobaseTW/'],
}


def read(p):
    with io.open(p, encoding='utf-8') as f:
        return f.read()


def plain(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def attr(s):
    return html.escape(plain(s), quote=True)


def load_modules(include_drafts=False):
    mods = {}
    for p in sorted(glob.glob(os.path.join(SRC, '*.json'))):
        if os.path.basename(p).startswith('_'):
            continue
        m = json.loads(read(p))
        if m.get('draft') and not include_drafts:
            continue
        mods[m['slug']] = m
    return mods


def load_platform():
    return json.loads(read(os.path.join(SRC, '_platform.json')))


def load_chrome():
    return read(os.path.join(SRC, 'chrome-top.html')), read(os.path.join(SRC, 'chrome-bottom.html'))


# ── 內容檢查：錯誤會擋下產頁；警告只提醒 ──

SLUG_RE = re.compile(r'^(nexus|solution)-[a-z0-9]+(-[a-z0-9]+)*$')


def is_solution(m):
    return m.get('kind') == 'solution'
THEME_KEYS = ('deep', 'bright', 'soft', 'tint', 'ink1', 'ink2')


def available_icons():
    css = read(os.path.join(ROOT, 'css', 'iconoir-subset.css'))
    return set(re.findall(r'\.iconoir-([a-z0-9-]+)::before', css))


def inquiry_chips():
    return re.findall(r'name="entry\.1863307942" value="([^"]+)"', load_chrome()[0])


def known_slugs(mods, pf):
    return set(mods) | set(pf.get('extra_modules', {}))


def validate(m, mods, pf):
    errors, warnings = [], []

    def need(path, v):
        if v is None or (isinstance(v, (str, list)) and not (v.strip() if isinstance(v, str) else v)):
            errors.append('%s 不可空白' % path)

    def g(d, *keys):
        for k in keys:
            if not isinstance(d, dict):
                return None
            d = d.get(k)
        return d

    slug = m.get('slug', '')
    if not SLUG_RE.match(slug):
        errors.append('slug 須為 nexus-（產品）或 solution-（解決方案）開頭的小寫英數與連字號')
    if is_solution(m):
        need('industry', m.get('industry'))
        need('flow', m.get('flow'))
        for i, st in enumerate(m.get('flow') or [], 1):
            need('flow[%d].title' % i, st.get('title'))
            for x in st.get('modules') or []:
                if SLUG_RE.match(x) and x not in known_slugs(mods, pf):
                    errors.append('flow[%d] 的「%s」不是已發布的產品' % (i, x))
    if m.get('file') != slug + '.html':
        errors.append('file 應為 %s.html' % slug)
    for k in ('code', 'name_zh', 'leg', 'title', 'description', 'eyebrow', 'keywords', 'updated'):
        need(k, m.get(k))
    for k in ('h1', 'slogan', 'sub', 'tagline'):
        need('hero.' + k, g(m, 'hero', k))
    theme = m.get('theme') or {}
    for k in THEME_KEYS:
        if not re.match(r'^#[0-9A-Fa-f]{6}$', theme.get(k, '')):
            errors.append('theme.%s 須為 #RRGGBB 色碼' % k)
    if '是什麼' not in dict(m.get('summary') or []):
        errors.append('重點摘要須有「是什麼」一項（平台總覽卡片會用到）')
    need('definition.q', g(m, 'definition', 'q'))
    need('definition.a', g(m, 'definition', 'a'))
    need('audience', m.get('audience'))
    for k in ('heading', 'cards', 'statement'):
        need('pain.' + k, g(m, 'pain', k))
    for sec in ('capabilities', 'diff'):
        need(sec + '.heading', g(m, sec, 'heading'))
        need(sec + '.cards', g(m, sec, 'cards'))
    need('platform.heading', g(m, 'platform', 'heading'))
    need('platform.text', g(m, 'platform', 'text'))
    need('deploy', m.get('deploy'))
    need('cta.heading', g(m, 'cta', 'heading'))
    need('cta.text', g(m, 'cta', 'text'))
    for i, f in enumerate(m.get('faq') or [], 1):
        need('faq[%d].q' % i, f.get('q'))
        need('faq[%d].a' % i, f.get('a'))
    for i, c in enumerate(g(m, 'capabilities', 'cards') or [], 1):
        need('capabilities.cards[%d].title' % i, c.get('title'))
        need('capabilities.cards[%d].items' % i, c.get('items'))
    if m.get('updated') and not re.match(r'^\d{4}-\d{2}-\d{2}$', m['updated']):
        errors.append('updated 須為 YYYY-MM-DD')
    drafts = set(load_modules(include_drafts=True)) - set(mods)
    for s in g(m, 'platform', 'related') or []:
        if s in drafts:
            warnings.append('相關產品「%s」目前是草稿，頁面上暫時不顯示這個連結' % s)
        elif s not in known_slugs(mods, pf) and s != slug:
            errors.append('platform.related 的「%s」不存在' % s)
    chip = m.get('inquiry_chip')
    if chip and chip not in inquiry_chips():
        errors.append('inquiry_chip「%s」不在諮詢表單選項裡' % chip)
    rg = m.get('regulation')
    if rg:
        if len(rg.get('cols') or []) != 2:
            errors.append('regulation.cols 須為兩欄')
        if any(len(r) != 2 for r in rg.get('rows') or []):
            errors.append('regulation.rows 每列須為兩格')
        need('regulation.sources', rg.get('sources'))
    cp = m.get('compare')
    if cp:
        n = len(cp.get('cols') or [])
        if any(len(r) != n + 1 for r in cp.get('rows') or []):
            errors.append('compare.rows 每列須為「項目」加 %d 格' % n)

    icons = available_icons()
    used = [b.get('icon') for b in g(m, 'hero', 'badges') or []]
    used += [c.get('icon') for sec in ('capabilities', 'diff') for c in g(m, sec, 'cards') or []]
    for ic in sorted(set(filter(None, used)) - icons):
        warnings.append('圖示「%s」不在目前的圖示子集，發布時 GitHub Action 會重建；若名稱打錯則不會顯示' % ic)
    if disp_width(m.get('title', '')) > 32:
        warnings.append('頁面標題約 %.0f 個全形字寬，搜尋結果只顯示約 32 個' % disp_width(m['title']))
    dl = len(plain(m.get('description', '')))
    if dl and not 70 <= dl <= 160:
        warnings.append('搜尋摘要 %d 字，建議 70～160 字' % dl)
    if len(m.get('faq') or []) < 3:
        warnings.append('常見問題少於 3 題，AI 引擎可引用的內容較少')
    return errors, warnings


def validate_platform(pf, mods):
    errors = []
    known = known_slugs(mods, pf)
    drafts = set(load_modules(include_drafts=True)) - set(mods)
    for lg in pf.get('legs') or []:
        for s in lg.get('modules') or []:
            if s not in known and s not in drafts:
                errors.append('平台分組「%s」的「%s」不存在' % (lg.get('name'), s))
    for need_text, s in (pf.get('needs') or {}).get('rows') or []:
        if s not in known and s not in drafts:
            errors.append('依需求找模組的「%s」指到不存在的「%s」' % (need_text, s))
    for k in ('title', 'description', 'h1', 'slogan', 'sub'):
        if not (pf.get(k) or '').strip():
            errors.append('平台總覽 %s 不可空白' % k)
    return errors


def url_of(m):
    return '%s/%s' % (SITE, m['file'])


def jsonld(m):
    page_url = url_of(m)
    main = {
            '@type': 'Service',
            '@id': page_url + '#software',
            'name': '%s %s' % (m['code'], m['name_zh']) if m['code'] != m['name_zh'] else m['name_zh'],
            'alternateName': [m['eyebrow']] + m.get('aliases', []),
            'serviceType': m['name_zh'],
            'description': plain(m['description']),
            'audience': {'@type': 'Audience', 'audienceType': m.get('industry', '')},
            'areaServed': {'@type': 'Country', 'name': '台灣'},
            'provider': {'@id': ORG['@id']},
            'url': page_url,
        } if is_solution(m) else None
    graph = [
        main or {
            '@type': 'SoftwareApplication',
            '@id': page_url + '#software',
            'name': '%s %s' % (m['code'], m['name_zh']),
            'alternateName': [m['eyebrow']] + m.get('aliases', []) + ([m['fullname']] if m.get('fullname') else []),
            'description': plain(m['description']),
            'applicationCategory': 'BusinessApplication',
            'applicationSubCategory': m['leg'],
            'operatingSystem': 'Linux（容器化部署）',
            'inLanguage': 'zh-Hant-TW',
            'url': page_url,
            'isPartOf': {'@id': SITE + '/nexus.html#platform'},
            'publisher': {'@id': ORG['@id']},
            'featureList': [plain(c['title']) for c in m['capabilities']['cards']],
        },
        {
            '@type': 'WebPage',
            '@id': page_url + '#webpage',
            'url': page_url,
            'name': m['title'],
            'description': plain(m['description']),
            'inLanguage': 'zh-Hant-TW',
            'dateModified': m['updated'],
            'about': {'@id': page_url + '#software'},
            'isPartOf': {'@type': 'WebSite', '@id': SITE + '/#website', 'name': '奧洛 Aurobase', 'url': SITE + '/'},
            'publisher': {'@id': ORG['@id']},
        },
        {
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': '首頁', 'item': SITE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': '產業解決方案' if is_solution(m) else 'AURO NEXUS',
                 'item': SITE + ('/nexus.html#solutions' if is_solution(m) else '/nexus.html')},
                {'@type': 'ListItem', 'position': 3, 'name': m['code'], 'item': page_url},
            ],
        },
        ORG,
    ]
    if m.get('faq'):
        graph.append({
            '@type': 'FAQPage',
            'mainEntity': [
                {'@type': 'Question', 'name': plain(f['q']),
                 'acceptedAnswer': {'@type': 'Answer', 'text': plain(f['a'])}}
                for f in m['faq']
            ],
        })
    return json.dumps({'@context': 'https://schema.org', '@graph': graph},
                      ensure_ascii=False, indent=2)


def head(m):
    title = m['title']
    page_url = url_of(m)
    og_image = m.get('og_image', 'images/nexus-chat.webp')
    return f'''<!DOCTYPE html>
<html lang="zh-Hant-TW">
  <head>
    <title>{html.escape(title)}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="{attr(m['description'])}">
    <meta name="keywords" content="{attr(','.join(m['keywords']))}">
    <link rel="canonical" href="{page_url}">
    <link rel="alternate" hreflang="zh-Hant-TW" href="{page_url}">
    <meta property="og:title" content="{attr(title)}">
    <meta property="og:description" content="{attr(m.get('og_description', m['description']))}">
    <meta property="og:url" content="{page_url}">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="zh_TW">
    <meta property="og:site_name" content="奧洛 Aurobase">
    <meta property="og:image" content="{SITE}/{og_image}">
    <meta name="twitter:card" content="summary_large_image">

    <script type="application/ld+json">
{jsonld(m)}
</script>

    <link href="images/favicon.ico" rel="shortcut icon">
    <link rel="preload" href="WOFF2/LINESeedSans_W_Rg.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="WOFF2/LINESeedTW_OTF_Rg.subset.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="css/line-seed-font.css">
    <link rel="stylesheet" href="css/open-iconic-bootstrap.min.css">
    <link rel="stylesheet" href="css/animate.css">
    <link rel="stylesheet" href="css/owl.carousel.min.css">
    <link rel="stylesheet" href="css/owl.theme.default.min.css">
    <link rel="stylesheet" href="css/magnific-popup.css">
    <link rel="stylesheet" href="css/ionicons.min.css">
    <link rel="stylesheet" href="css/flaticon.css">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/inquiry-modal.css">
    <link rel="stylesheet" href="css/iconoir-subset.css">
    <link rel="stylesheet" href="css/nexus-module.css">

'''


DEPLOY_INTRO = '以容器交付，同一套系統可以放在公有雲的台灣區域、企業自有機房或私有雲；流程、規則與既有系統的介接，可依貴機構需求客製。'
DEPLOY_STRIP = ('<a class="nm-modes" href="#deploy" aria-label="部署方式：雲端、地端、客製">'
                '<span>雲端</span><span>地端</span><span>客製</span></a>')


def theme_style(t):
    return ';'.join('--m-%s:%s' % (k, v) for k, v in t.items())


def section(cls, label, heading, inner, intro=None, dark=False, sid=None):
    sid_attr = f' id="{sid}"' if sid else ''
    dark_cls = ' nm-dark' if dark else ''
    pad = 'px-3 px-md-5' if dark else 'px-3 px-md-0'
    intro_html = f'\n                            <p class="section-intro">{intro}</p>' if intro else ''
    return f'''
            <section{sid_attr} class="{cls} nm-section{dark_cls}">
                <div class="container-fluid {pad}">
                    <div class="row justify-content-start">
                        <div class="col-md-12">
                            <p class="section-label">{label}</p>
                            <h2 class="section-heading">{heading}</h2>{intro_html}
{inner}
                        </div>
                    </div>
                </div>
            </section>
'''


def cards(items, render, cols='col-lg-4 col-md-6 mb-4'):
    out = ['                            <div class="row">']
    for it in items:
        out.append(f'                                <div class="{cols}">{render(it)}</div>')
    out.append('                            </div>')
    return '\n'.join(out)


def body(m, mods):
    h = m['hero']
    crumbs = f'''<nav class="nm-crumbs" aria-label="麵包屑"><ol>
                        <li><a href="index.html">首頁</a></li>
                        <li><a href="{'nexus.html#solutions' if is_solution(m) else 'nexus.html'}">{'產業解決方案' if is_solution(m) else 'AURO NEXUS'}</a></li>
                        <li><span aria-current="page">{m['code']}</span></li>
                    </ol></nav>'''
    badges = ''.join(
        f'<span class="nm-badge"><i class="iconoir-{b["icon"]}"></i> {b["text"]}</span>'
        for b in h.get('badges', []))
    summary = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in m['summary'])
    out = [f'''
<!-- ╔══ {m['code']} — {m['name_zh']}（由 tools/build-module-pages.py 產生，請改 JSON 不要直接改本檔）══╗ -->

            <section class="nm-hero nm-section nm-dark">
                <div class="container-fluid px-3 px-md-5">
                    {crumbs}
                    <div class="row align-items-center">
                        <div class="col-lg-7">
                            <p class="nm-family">{('AURO NEXUS 產業解決方案 · ' + m['industry']) if is_solution(m) else 'AURO NEXUS 產品家族'}{(' · <span lang="en">' + m['fullname'] + '</span>') if m.get('fullname') else ''}</p>
                            <h1 class="eyebrow">{h['h1']}</h1>
                            <p class="hero-slogan">{h['slogan']}</p>
                            <p class="hero-sub">{h['sub']}</p>
                            <p class="hero-tagline">{h['tagline']}</p>
                            <div class="hero-actions">
                                <a href="contact.html" class="btn-nm-primary">預約產品簡報</a>
                                <a href="#capabilities" class="btn-nm-outline">看核心能力</a>
                            </div>
                            <div class="nm-badges">{badges}</div>
                            {DEPLOY_STRIP}
                        </div>
                        <div class="col-lg-5 mt-5 mt-lg-0">
                            <aside class="nm-summary">
                                <h2>重點摘要</h2>
                                <dl>{summary}</dl>
                            </aside>
                        </div>
                    </div>
                </div>
            </section>
''']

    df = m['definition']
    aud = ''.join(f'<li><b>{a["who"]}</b><span>{a["why"]}</span></li>' for a in m['audience'])
    out.append(section('nm-define', 'DEFINITION', df['q'],
        f'''                            <div class="row">
                                <div class="col-lg-7 mb-4"><div class="define-answer">{''.join('<p>%s</p>' % s for s in df['a'])}</div></div>
                                <div class="col-lg-5 mb-4"><div class="audience"><h3>適合誰</h3><ul>{aud}</ul></div></div>
                            </div>''', sid='what-is'))

    if m.get('flow'):
        out.append(flow_section(m, mods))

    p = m['pain']
    out.append(section('nm-pain', 'THE PROBLEM', p['heading'],
        cards(enumerate(p['cards'], 1), lambda ic: f'''
                                    <div class="pain-card"><div class="pain-number">{ic[0]:02d}</div>
                                        <h3>{ic[1]['title']}</h3><p>{ic[1]['text']}</p></div>''')
        + f'\n                            <div class="pain-statement">{p["statement"]}</div>',
        intro=p.get('intro')))

    c = m['capabilities']
    out.append(section('nm-cap', 'CAPABILITIES', c['heading'],
        cards(c['cards'], lambda it: f'''
                                    <div class="cap-card"><div class="icon-wrap"><i class="iconoir-{it['icon']}"></i></div>
                                        <h3>{it['title']}</h3><ul>{''.join('<li>%s</li>' % li for li in it['items'])}</ul></div>'''),
        intro=c.get('intro'), sid='capabilities'))

    rg = m.get('regulation')
    if rg:
        rows = ''.join(f'<tr><th scope="row">{r[0]}</th><td>{r[1]}</td></tr>' for r in rg['rows'])
        src = ' '.join(f'<a href="{s["url"]}" target="_blank" rel="noopener">{s["name"]}</a>' for s in rg['sources'])
        out.append(section('nm-reg', 'REGULATORY MAPPING', rg['heading'],
            f'''                            <div class="nm-table-wrap"><table class="nm-table">
                                <thead><tr><th scope="col">{rg['cols'][0]}</th><th scope="col">{rg['cols'][1]}</th></tr></thead>
                                <tbody>{rows}</tbody></table></div>
                            <p class="nm-source">資料來源：{src}。{rg.get('note', '')}</p>''',
            intro=rg.get('intro')))

    cp = m.get('compare')
    if cp:
        head = ''.join(f'<th scope="col"{" class=is-us" if i == len(cp["cols"]) - 1 else ""}>{c}</th>' for i, c in enumerate(cp['cols']))
        rows = ''.join('<tr><th scope="row">%s</th>%s</tr>' % (r[0], ''.join(
            f'<td{" class=is-us" if i == len(r) - 2 else ""}>{v}</td>' for i, v in enumerate(r[1:]))) for r in cp['rows'])
        out.append(section('nm-compare', 'COMPARISON', cp['heading'],
            f'''                            <div class="nm-table-wrap"><table class="nm-table nm-table-compare">
                                <thead><tr><th scope="col"></th>{head}</tr></thead>
                                <tbody>{rows}</tbody></table></div>''',
            intro=cp.get('intro')))

    d = m['diff']
    out.append(section('nm-diff', "WHAT'S DIFFERENT", d['heading'],
        cards(d['cards'], lambda it: f'''
                                    <div class="diff-card"><i class="iconoir-{it['icon']} diff-icon"></i>
                                        <h3>{it['title']}</h3><p>{it['text']}</p></div>'''),
        intro=d.get('intro'), dark=True))

    pl = m['platform']
    links = []
    for s in pl['related']:
        r = mods.get(s)
        if r:
            links.append(f'<a class="nm-link" href="{r["file"]}"><b>{r["code"]}</b><span>{r["name_zh"]}</span></a>')
        elif s == 'nexus-saga':
            links.append('<a class="nm-link" href="nexus-saga.html"><b>SAGA</b><span>非結構化資料治理</span></a>')
        elif s == 'nexus-geo':
            links.append('<a class="nm-link" href="nexus-geo.html"><b>NEXUS GEO</b><span>生成式搜尋能見度</span></a>')
        # 不存在的產品在 validate() 就會被擋下；草稿預覽時略過
    links.append('<a class="nm-link" href="nexus.html#platform"><b>AURO NEXUS</b><span>平台總覽與全部模組</span></a>')
    out.append(section('nm-platform', 'ON THE PLATFORM', pl['heading'],
        f'                            <div class="platform-text">{pl["text"]}</div>\n'
        f'                            <div class="nm-links">{"".join(links)}</div>'))

    out.append(deploy_section(m['deploy'], m.get('deploy_intro', DEPLOY_INTRO)))

    if m.get('limits'):
        items = '\n'.join(
            f'''                                    <div class="limit-item"><div class="limit-index">{i}</div>
                                        <div><h3>{it['title']}</h3><p>{it['text']}</p></div></div>'''
            for i, it in enumerate(m['limits'], 1))
        out.append(section('nm-limits', 'SCOPE', '範圍界定',
            f'                            <div class="row"><div class="col-lg-10">\n{items}\n                            </div></div>',
            intro=m.get('limits_intro')))

    if m.get('faq'):
        items = '\n'.join(
            f'''                                    <div class="faq-item"><h3>{f['q']}</h3><p>{f['a']}</p></div>'''
            for f in m['faq'])
        out.append(section('nm-faq', 'FAQ', '常見問題',
            f'                            <div class="row"><div class="col-lg-10">\n{items}\n                            </div></div>'))

    cta = m['cta']
    out.append(f'''
            <section class="nm-cta">
                <div class="container">
                    <h2>{cta['heading']}</h2>
                    <p>{cta['text']}</p>
                    <a class="btn-cta" href="contact.html">預約產品簡報</a>
                    <p class="nm-updated">最後更新：<time datetime="{m['updated']}">{m['updated']}</time></p>
                </div>
            </section>

''')
    return ''.join(out)


def module_chip(x, mods, cls='nm-chip'):
    """流程步驟裡的模組：已發布的產品連到產品頁，其他文字照原樣顯示。"""
    r = mods.get(x)
    if r and not is_solution(r):
        return f'<a class="{cls}" href="{r["file"]}">{r["code"]}</a>'
    return f'<span class="{cls}">{x}</span>'


def flow_section(m, mods):
    steps = ''.join(f'''
                                <li class="flow-step"><span class="flow-n">{i:02d}</span><h3>{st['title']}</h3><p>{st.get('text', '')}</p>
                                    <div class="flow-mods">{''.join(module_chip(x, mods) for x in st.get('modules') or [])}</div></li>'''
        for i, st in enumerate(m['flow'], 1))
    return section('nm-flow', 'HOW IT WORKS', m.get('flow_heading', '運作流程'),
        f'                            <ol class="flow">{steps}\n                            </ol>',
        intro=m.get('flow_intro'), sid='flow')


def deploy_section(items, intro):
    return section('nm-deploy', 'DEPLOYMENT', '部署：可雲、可地、可客製',
        cards(items, lambda it: f'''
                                    <div class="deploy-card"><span class="deploy-tag">{it['tag']}</span>
                                        <h3>{it['title']}</h3><p>{it['text']}</p></div>'''),
        intro=intro, sid='deploy')


SMOOTH = '''    <script>
    $(function(){
        $('a[href="#capabilities"], a[href="#deploy"]').on('click', function(e){
            e.preventDefault();
            $('html, body').animate({ scrollTop: $($(this).attr('href')).offset().top - 50 }, 600);
        });
    });
    </script>
'''


def build(m, mods, top, bottom):
    chip = m.get('inquiry_chip')
    t = top
    if chip:
        needle = f'value="{chip}">'
        assert needle in t, '%s: inquiry_chip「%s」不在諮詢表單選項裡' % (m['slug'], chip)
        t = t.replace(needle, f'value="{chip}" checked>', 1)
    t = t.replace('  <body>', f'  <body style="{theme_style(m["theme"])}">', 1)
    t = NAV_RE.sub(lambda x: x.group(1) + nav_html(m['file'], '', load_platform(), mods), t, count=1)
    b = bottom.replace('  </body>', SMOOTH + '  </body>', 1)
    return head(m) + '    ' + t.lstrip() + body(m, mods) + b


# ── nexus.html 平台總覽：只改 OVERVIEW 標記之間與 head 的 SEO 欄位，其餘舊段落不動 ──

BEGIN, END = '<!-- NEXUS-OVERVIEW:BEGIN（由 tools/build-module-pages.py 產生）-->', '<!-- NEXUS-OVERVIEW:END -->'


def overview_mods(pf, mods):
    def get(slug):
        if slug in mods:
            m = mods[slug]
            return {'code': m['code'], 'name_zh': m['name_zh'], 'file': m['file'],
                    'what': plain(dict(m['summary'])['是什麼'])}
        return pf['extra_modules'].get(slug)
    return get


def live(pf, mods, slugs):
    """略過草稿與不存在的產品。"""
    get = overview_mods(pf, mods)
    return [s for s in slugs if get(s)]


def overview_html(pf, mods):
    get = overview_mods(pf, mods)
    summary = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in pf['summary'])
    out = [f'''
            <section id="platform" class="nm-hero nm-section nm-dark">
                <div class="container-fluid px-3 px-md-5">
                    <div class="row align-items-center">
                        <div class="col-lg-7">
                            <h1 class="eyebrow">{pf['h1']}</h1>
                            <p class="hero-slogan">{pf['slogan']}</p>
                            <p class="hero-sub">{pf['sub']}</p>
                            <p class="hero-tagline">{pf['tagline']}</p>
                            <div class="hero-actions">
                                <a href="contact.html" class="btn-nm-primary">預約平台簡報</a>
                                <a href="#modules" class="btn-nm-outline">看全部模組</a>
                            </div>
                            {DEPLOY_STRIP}
                        </div>
                        <div class="col-lg-5 mt-5 mt-lg-0">
                            <aside class="nm-summary"><h2>重點摘要</h2><dl>{summary}</dl></aside>
                        </div>
                    </div>
                </div>
            </section>
''']
    df = pf['definition']
    aud = ''.join(f'<li><b>{a["who"]}</b><span>{a["why"]}</span></li>' for a in pf['audience'])
    out.append(section('nm-define', 'DEFINITION', df['q'],
        f'''                            <div class="row">
                                <div class="col-lg-7 mb-4"><div class="define-answer">{''.join('<p>%s</p>' % x for x in df['a'])}</div></div>
                                <div class="col-lg-5 mb-4"><div class="audience"><h3>適合誰</h3><ul>{aud}</ul></div></div>
                            </div>'''))

    if pf.get('deploy'):
        out.append(deploy_section(pf['deploy'], pf.get('deploy_intro', DEPLOY_INTRO)))

    def mod_link(slug):
        x = get(slug)
        return f'<a class="leg-mod" href="{x["file"]}"><b>{x["code"]}</b><span>{x["name_zh"]}</span><small>{x["what"]}</small></a>'
    base = pf['legs'][0]
    legs = ''.join(f'''
                                <div class="col-lg-4 col-md-6 mb-4"><div class="leg-card"><p class="leg-name">{lg['name']}</p><p class="leg-text">{lg['text']}</p>{''.join(mod_link(s) for s in live(pf, mods, lg['modules']))}</div></div>'''
        for lg in pf['legs'][1:] if live(pf, mods, lg['modules']))
    n = sum(len(live(pf, mods, lg['modules'])) for lg in pf['legs'])
    out.append(section('nm-legs', 'ARCHITECTURE', f'一個治理底座，{n} 個模組',
        f'''                            <div class="row">{legs}
                            </div>
                            <div class="leg-base"><p class="leg-name">{base['name']}</p><p class="leg-text">{base['text']}所有模組的 AI 呼叫都經過這一層。</p>{''.join(mod_link(s) for s in live(pf, mods, base['modules']))}</div>''',
        intro='上層的每一個模組各自解決一類問題；下層的治理底座讓它們共用同一套權限、模型與稽核軌跡。', sid='modules'))

    sols = solutions(mods)
    if sols:
        def sol_card(m):
            used = []
            for st in m['flow']:
                used += [x for x in st.get('modules') or [] if x in mods and x not in used]
            return (f'<div class="sol-card"><span class="sol-ind">{m["industry"]}</span>'
                    f'<h3><a href="{m["file"]}">{m["name_zh"]}</a></h3><p>{plain(dict(m["summary"])["是什麼"])}</p>'
                    f'<div class="flow-mods">{"".join(module_chip(x, mods) for x in used)}</div></div>')
        out.append(section('nm-cap', 'SOLUTIONS', pf.get('solutions_heading', '產業解決方案'),
            cards(sols, sol_card), intro=pf.get('solutions_intro'), sid='solutions'))

    nd = pf['needs']
    rows = ''.join(f'<tr><th scope="row">{need}</th><td><a href="{get(s)["file"]}">{get(s)["code"]} {get(s)["name_zh"]}</a></td></tr>' for need, s in nd['rows'] if get(s))
    out.append(section('nm-compare', 'WHERE TO START', nd['heading'],
        f'''                            <div class="nm-table-wrap"><table class="nm-table">
                                <thead><tr><th scope="col">您的需求</th><th scope="col">對應模組</th></tr></thead>
                                <tbody>{rows}</tbody></table></div>''', intro=nd['intro']))

    out.append(section('nm-diff', "WHAT'S DIFFERENT", '平台的三個設計',
        cards(pf['diff'], lambda it: f'''
                                    <div class="diff-card"><i class="iconoir-{it['icon']} diff-icon"></i>
                                        <h3>{it['title']}</h3><p>{it['text']}</p></div>'''), dark=True))

    items = '\n'.join(f'''                                    <div class="faq-item"><h3>{f['q']}</h3><p>{f['a']}</p></div>''' for f in pf['faq'])
    out.append(section('nm-faq', 'FAQ', '關於 AURO NEXUS 的常見問題',
        f'                            <div class="row"><div class="col-lg-10">\n{items}\n                            </div></div>'))
    return BEGIN + '\n<div class="nm-overview" style="--m-deep:#2B3A8C;--m-bright:#4659C9;--m-soft:#8FA0F0;--m-tint:#ECEFFC;--m-ink1:#0C0F1F;--m-ink2:#141A35">' + ''.join(out) + '</div>\n' + END


def solutions(mods):
    order = {'公部門': 0, '金融保險': 1}
    return sorted((m for m in mods.values() if is_solution(m)), key=lambda m: (order.get(m['industry'], 9), m['name_zh']))


def overview_jsonld(pf, mods, old_faq):
    get = overview_mods(pf, mods)
    url = SITE + '/nexus.html'
    slugs = live(pf, mods, [s for lg in pf['legs'] for s in lg['modules']])
    graph = [
        {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': pf['title'],
         'description': plain(pf['description']), 'inLanguage': 'zh-Hant-TW', 'dateModified': pf['updated'],
         'about': {'@id': url + '#platform'}, 'publisher': {'@id': ORG['@id']}},
        {'@type': 'SoftwareApplication', '@id': url + '#platform', 'name': 'AURO NEXUS',
         'alternateName': ['AURO NEXUS AI 治理平台', 'NEXUS'], 'description': plain(pf['description']),
         'applicationCategory': 'BusinessApplication', 'operatingSystem': 'Linux（容器化部署）',
         'inLanguage': 'zh-Hant-TW', 'url': url, 'publisher': {'@id': ORG['@id']},
         'hasPart': [{'@type': 'SoftwareApplication', 'name': '%s %s' % (get(s)['code'], get(s)['name_zh']),
                      'url': '%s/%s' % (SITE, get(s)['file'])} for s in slugs]},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': '首頁', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'AURO NEXUS', 'item': url}]},
        ORG,
        {'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': plain(f['q']), 'acceptedAnswer': {'@type': 'Answer', 'text': plain(f['a'])}}
            for f in pf['faq']] + old_faq},
    ]
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=2)


def build_overview(mods, pf=None, write=True):
    pf = pf or load_platform()
    p = os.path.join(ROOT, 'nexus.html')
    s = read(p)
    # 舊段落（NEXUS OS / CDP / Voice）的 FAQ 仍在頁面上，結構化資料一併保留（_platform.json legacy_faq）
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    old_faq = pf['legacy_faq']
    s = s[:m.start(1)] + '\n' + overview_jsonld(pf, mods, old_faq) + '\n' + s[m.end(1):]
    title = html.escape(pf['title'])
    s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda x: x.group(1) + attr(pf['description']), s, count=1)
    s = re.sub(r'(<meta name="keywords" content=")[^"]*', lambda x: x.group(1) + attr(','.join(pf['keywords'])), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda x: x.group(1) + title, s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda x: x.group(1) + attr(pf['description']), s, count=1)
    block = overview_html(pf, mods)
    if BEGIN in s:
        s = s[:s.index(BEGIN)] + block + s[s.index(END) + len(END):]
    else:
        anchor = '<div id="colorlib-main">'
        assert anchor in s
        s = s.replace(anchor, anchor + '\n' + block + '\n', 1)
    if write:
        io.open(p, 'w', encoding='utf-8').write(s)
    return s


LLMS_BEGIN, LLMS_END = '<!-- MODULES:BEGIN（由 tools/build-module-pages.py 產生）-->', '<!-- MODULES:END -->'


def update_llms(mods, pf=None):
    pf = pf or load_platform()
    get = overview_mods(pf, mods)
    b = ['## AURO NEXUS 產品一覽', '', ''.join(plain(x) for x in pf['definition']['a']), '',
         '平台總覽：[AURO NEXUS](nexus.html)', '']
    for lg in pf['legs']:
        b.append('### ' + lg['name'])
        slugs = live(pf, mods, lg['modules'])
        if not slugs:
            b.pop()
            continue
        for slug in slugs:
            x = get(slug)
            desc = plain(mods[slug]['description']) if slug in mods else x['what']
            b.append('- [%s %s](%s): %s' % (x['code'], x['name_zh'], x['file'], desc))
        b.append('')
    sols = solutions(mods)
    if sols:
        b.append('### 產業解決方案（由平台模組組成）')
        for m in sols:
            b.append('- [%s](%s): %s' % (m['name_zh'], m['file'], plain(m['description'])))
        b.append('')
    block = LLMS_BEGIN + '\n' + '\n'.join(b) + LLMS_END
    p = os.path.join(ROOT, 'llms.txt')
    t = read(p)
    if LLMS_BEGIN in t:
        t = t[:t.index(LLMS_BEGIN)] + block + t[t.index(LLMS_END) + len(LLMS_END):]
    else:
        a, e = t.index('## AURO NEXUS 模組一覽'), t.index('### NEXUS SAGA（資料治理）')
        t = t[:a] + block + '\n\n' + t[e:]
    io.open(p, 'w', encoding='utf-8').write(t)


def update_sitemap(mods):
    p = os.path.join(ROOT, 'sitemap.xml')
    t = read(p)
    for m in mods.values():
        loc = '%s/%s' % (SITE, m['file'])
        entry = '<url><loc>%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>' % (loc, m['updated'])
        if '<loc>%s</loc>' % loc in t:
            t = re.sub(r'<url><loc>%s</loc>.*?</url>' % re.escape(loc), entry, t)
        else:
            t = t.replace('</urlset>', '  %s\n</urlset>' % entry)
    io.open(p, 'w', encoding='utf-8').write(t)


# ── SEO / GEO 稽核：編輯器的檢查面板與 GitHub Action 的報告共用 ──

AI_BOTS = ('GPTBot', 'ClaudeBot', 'PerplexityBot', 'Google-Extended')


def disp_width(text):
    """搜尋結果的顯示寬度：中文字算 1，英數與半形標點算 0.5。Google 標題約顯示 32 個全形字寬。"""
    return sum(0.5 if ord(ch) < 0x2E80 else 1 for ch in text)


def _chk(group, status, label, detail=''):
    return {'group': group, 'status': status, 'label': label, 'detail': detail}


def site_checks(file):
    out = []
    robots = read(os.path.join(ROOT, 'robots.txt')) if os.path.exists(os.path.join(ROOT, 'robots.txt')) else ''
    blocked = [b for b in AI_BOTS if re.search(r'User-agent:\s*%s\s*\n(?:[^\n]*\n)*?Disallow:\s*/\s*$' % b, robots, re.M)]
    missing = [b for b in AI_BOTS if b not in robots]
    if blocked:
        out.append(_chk('全站', 'fail', 'robots.txt 擋住了 AI 爬蟲', '、'.join(blocked)))
    else:
        out.append(_chk('全站', 'pass' if not missing else 'warn', 'robots.txt 允許 AI 爬蟲',
                        '未明確列出：' + '、'.join(missing) if missing else '、'.join(AI_BOTS)))
    llms = os.path.join(ROOT, 'llms.txt')
    out.append(_chk('全站', 'pass' if os.path.exists(llms) and '(%s)' % file in read(llms) else 'warn',
                    'llms.txt 收錄這一頁', '儲存並產頁後會自動加入'))
    sm = os.path.join(ROOT, 'sitemap.xml')
    out.append(_chk('全站', 'pass' if os.path.exists(sm) and '/%s</loc>' % file in read(sm) else 'warn',
                    'sitemap.xml 收錄這一頁', '儲存並產頁後會自動加入'))
    return out


def audit(m, mods, pf):
    """回傳 {'checks': [...], 'score': {...}, 'serp': {...}, 'jsonld': str, 'llms': str}。"""
    C = []
    kws = [k for k in m.get('keywords') or [] if k != 'AURO NEXUS']
    kw = kws[0] if kws else ''
    code = m.get('code', '')
    title, desc = m.get('title', ''), plain(m.get('description', ''))
    h1 = plain((m.get('hero') or {}).get('h1', ''))
    low = lambda x: x.lower()

    # SEO
    w = disp_width(title)
    C.append(_chk('SEO', 'pass' if 0 < w <= 32 else 'warn', '頁面標題長度',
                  '%.0f 個全形字寬（搜尋結果約顯示 32 個，超過的會被截成…）' % w))
    if not kw:
        C.append(_chk('SEO', 'fail', '設定主關鍵字', '目標關鍵字的第一個就是主關鍵字'))
    else:
        pos = low(title).find(low(kw))
        C.append(_chk('SEO', 'pass' if 0 <= pos <= 12 else ('warn' if pos > 12 else 'fail'),
                      '主關鍵字「%s」放在標題前段' % kw, '目前在第 %d 字' % (pos + 1) if pos >= 0 else '標題裡沒有主關鍵字'))
        C.append(_chk('SEO', 'pass' if low(kw) in low(h1) else 'fail', '主關鍵字出現在 H1', h1))
        C.append(_chk('SEO', 'pass' if low(kw) in low(desc) else 'fail', '主關鍵字出現在搜尋摘要'))
        twins = [x['code'] for x in mods.values() if x.get('slug') != m.get('slug')
                 and [k for k in x.get('keywords') or [] if k != 'AURO NEXUS'][:1] == [kw]]
        C.append(_chk('SEO', 'warn' if twins else 'pass', '主關鍵字不和其他頁重複',
                      '和 %s 搶同一個主關鍵字' % '、'.join(twins) if twins else ''))
    C.append(_chk('SEO', 'pass' if 70 <= len(desc) <= 160 else 'warn', '搜尋摘要長度', '%d 字（建議 70～160）' % len(desc)))
    C.append(_chk('SEO', 'pass' if 5 <= len(kws) <= 15 else 'warn', '目標關鍵字數量', '%d 個（建議 5～15）' % len(kws)))
    rel = len((m.get('platform') or {}).get('related') or [])
    C.append(_chk('SEO', 'pass' if rel >= 2 else 'warn', '連到其他產品頁（內部連結）', '%d 個' % rel))

    # GEO
    df = m.get('definition') or {}
    answers = [plain(x) for x in df.get('a') or []]
    entity = re.compile(r'%s[^。]{0,12}是[^。]{0,6}奧洛' % re.escape(code)) if code else None
    C.append(_chk('GEO', 'pass' if df.get('q', '').strip().endswith(('？', '?')) else 'warn', '定義區用問句開頭',
                  df.get('q', '')))
    C.append(_chk('GEO', 'pass' if entity and any(entity.search(a) for a in answers) else 'fail',
                  '定義區有「%s 是奧洛（Aurobase）…」的實體句' % code, 'AI 引擎靠這句把產品和公司連起來'))
    C.append(_chk('GEO', 'pass' if code and desc.startswith(code) else 'warn', '搜尋摘要以產品名開頭定義',
                  desc[:30] + '…' if desc else ''))
    faq = m.get('faq') or []
    C.append(_chk('GEO', 'pass' if len(faq) >= 4 else 'warn', '常見問題至少 4 題', '%d 題' % len(faq)))
    bad_len = [i + 1 for i, f in enumerate(faq) if not 40 <= len(plain(f.get('a', ''))) <= 220]
    C.append(_chk('GEO', 'pass' if faq and not bad_len else 'warn', '回答長度適合被引用（40～220 字）',
                  '第 %s 題需調整' % '、'.join(map(str, bad_len)) if bad_len else ''))
    names = [low(x) for x in [code, kw] + (m.get('aliases') or []) if x]
    ctx = [i + 1 for i, f in enumerate(faq) if not any(n in low(plain(f.get('a', '') + f.get('q', ''))) for n in names)]
    C.append(_chk('GEO', 'pass' if faq and len(ctx) <= len(faq) // 2 else 'warn', '問答單獨被引用時看得懂（提到產品名或關鍵字）',
                  '第 %s 題沒提到' % '、'.join(map(str, ctx)) if ctx else ''))
    C.append(_chk('GEO', 'pass' if m.get('compare') or m.get('regulation') else 'warn', '有比較表或法規對照表',
                  'AI 引擎常直接引用表格'))
    srcs = [x for x in (m.get('regulation') or {}).get('sources') or [] if x.get('url')]
    C.append(_chk('GEO', 'pass' if srcs else 'info', '引用可查證的外部來源', '%d 個' % len(srcs)))
    try:
        age = (datetime.date.today() - datetime.date.fromisoformat(m.get('updated', ''))).days
        C.append(_chk('GEO', 'pass' if age <= 180 else 'warn', '內容更新日期', '%s（%d 天前）' % (m['updated'], age)))
    except ValueError:
        C.append(_chk('GEO', 'warn', '內容更新日期', '未設定'))
    C.append(_chk('GEO', 'pass' if len(m.get('audience') or []) >= 2 else 'warn', '「適合誰」至少 2 種對象'))
    tags = {d.get('tag') for d in m.get('deploy') or []}
    lack = [t for t in ('雲端', '地端', '客製') if t not in tags]
    C.append(_chk('GEO', 'fail' if lack else 'pass', '部署段落寫明雲端、地端、客製三種方式',
                  '缺：' + '、'.join(lack) if lack else '部署卡片的標籤要用「雲端」「地端」「客製」'))
    C += site_checks(m.get('file', ''))

    score = {}
    for g in ('SEO', 'GEO', '全站'):
        rows = [c for c in C if c['group'] == g and c['status'] != 'info']
        score[g] = [sum(c['status'] == 'pass' for c in rows), len(rows)]
    try:
        ld = jsonld(m)
    except Exception as e:  # 草稿缺欄位時
        ld = '（結構化資料暫時無法產生：%r）' % e
    return {'checks': C, 'score': score, 'jsonld': ld,
            'serp': {'title': title, 'url': 'aurobase.com › %s' % m.get('file', ''), 'description': desc},
            'llms': '- [%s %s](%s): %s' % (code, m.get('name_zh', ''), m.get('file', ''), desc)}


def audit_platform(pf):
    C = []
    kw = (pf.get('keywords') or [''])[0]
    title, desc, h1 = pf.get('title', ''), plain(pf.get('description', '')), plain(pf.get('h1', ''))
    C.append(_chk('SEO', 'pass' if disp_width(title) <= 32 else 'warn', '頁面標題長度', '%.0f 個全形字寬（建議 32 內）' % disp_width(title)))
    C.append(_chk('SEO', 'pass' if kw and title.startswith(kw) else 'warn', '主關鍵字「%s」放在標題開頭' % kw))
    C.append(_chk('SEO', 'pass' if kw and kw in h1 else 'fail', '主關鍵字出現在 H1'))
    C.append(_chk('SEO', 'pass' if 70 <= len(desc) <= 200 else 'warn', '搜尋摘要長度', '%d 字' % len(desc)))
    answers = ''.join(plain(x) for x in (pf.get('definition') or {}).get('a') or [])
    C.append(_chk('GEO', 'pass' if re.search(r'AURO NEXUS[^。]{0,4}是[^。]{0,6}奧洛', answers) else 'fail',
                  '定義區有「AURO NEXUS 是奧洛（Aurobase）…」的實體句'))
    C.append(_chk('GEO', 'pass' if len(pf.get('faq') or []) >= 4 else 'warn', '常見問題至少 4 題', '%d 題' % len(pf.get('faq') or [])))
    C.append(_chk('GEO', 'pass' if (pf.get('needs') or {}).get('rows') else 'warn', '「依需求找模組」表格'))
    C += site_checks('nexus.html')
    score = {}
    for g in ('SEO', 'GEO', '全站'):
        rows = [c for c in C if c['group'] == g and c['status'] != 'info']
        score[g] = [sum(c['status'] == 'pass' for c in rows), len(rows)]
    return {'checks': C, 'score': score, 'jsonld': '', 'llms': '',
            'serp': {'title': title, 'url': 'aurobase.com › nexus.html', 'description': desc}}


def audit_report():
    """給 GitHub Action 與命令列看的文字報告。"""
    mods, pf = load_modules(), load_platform()
    lines = []
    for name, a in [('平台總覽', audit_platform(pf))] + [(m['code'], audit(m, mods, pf)) for m in mods.values()]:
        sc = '  '.join('%s %d/%d' % (g, *v) for g, v in a['score'].items())
        lines.append('%-18s %s' % (name, sc))
        for c in a['checks']:
            if c['status'] in ('fail', 'warn'):
                lines.append('    %s %s %s' % ('✗' if c['status'] == 'fail' else '△', c['label'], c['detail']))
    return '\n'.join(lines)


GENERATED_MARK = '（由 tools/build-module-pages.py 產生，請改 JSON 不要直接改本檔）'


def render_module(m, mods):
    top, bottom = load_chrome()
    return build(m, mods, top, bottom)


def check_all(mods=None, pf=None):
    mods = load_modules() if mods is None else mods
    pf = pf or load_platform()
    errors = []
    for m in mods.values():
        errors += ['%s：%s' % (m['slug'], e) for e in validate(m, mods, pf)[0]]
    errors += validate_platform(pf, mods)
    return errors


def build_all():
    """檢查全部內容、產生全部頁面。有錯誤時不寫任何檔案並回傳錯誤清單。"""
    mods = load_modules()
    pf = load_platform()
    errors = check_all(mods, pf)
    if errors:
        return {'errors': errors, 'written': [], 'removed': []}
    nav_changed = update_nav(mods, pf)
    top, bottom = load_chrome()
    written, removed = [], []
    for m in mods.values():
        io.open(os.path.join(ROOT, m['file']), 'w', encoding='utf-8').write(build(m, mods, top, bottom))
        written.append(m['file'])
    for slug, m in load_modules(include_drafts=True).items():
        p = os.path.join(ROOT, m['file'])
        if slug not in mods and os.path.exists(p) and GENERATED_MARK in read(p):
            os.remove(p)
            removed.append(m['file'])
    build_overview(mods, pf)
    update_llms(mods, pf)
    update_sitemap(mods)
    written += ['nexus.html', 'llms.txt', 'sitemap.xml'] + [f for f in nav_changed if f not in written]
    return {'errors': [], 'written': written, 'removed': removed}


def today():
    return datetime.date.today().isoformat()


# ── 全站左側選單：所有頁面（含部落格文章與產品頁外框）共用同一份結構 ──

NAV_BEGIN, NAV_END = '<!-- SITE-NAV:BEGIN（由 tools/build-module-pages.py 依 _nav.json 產生）-->', '<!-- SITE-NAV:END -->'
NAV_TOGGLE_JS = ("<script>document.querySelectorAll('.nav-sub-toggle').forEach(function(b){b.addEventListener('click',function(){"
                 "var o=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',o);"
                 "document.getElementById(b.getAttribute('aria-controls')).hidden=!o;});});</script>")
NAV_RE = re.compile(r'(<nav id="colorlib-main-menu"[^>]*>\s*)(?:' + re.escape(NAV_BEGIN) + r'.*?' + re.escape(NAV_END) + r'|<ul>.*?</ul>)', re.S)


def nav_html(page, prefix, pf, mods):
    """page：目前頁面檔名（決定哪一項是 active、子選單是否展開）；prefix：部落格文章頁為 '../'。"""
    nav = json.loads(read(os.path.join(SRC, '_nav.json')))
    get = overview_mods(pf, mods)
    out = ['<ul>']
    for it in nav['items']:
        if it.get('type') == 'platform':
            here = page == 'nexus.html' or page.startswith('nexus-')
            cur = lambda f: ' aria-current="page"' if f == page else ''
            legs = []
            for lg in pf['legs']:
                slugs = live(pf, mods, lg['modules'])
                if slugs:
                    links = ''.join('<a href="%s%s"%s>%s</a>' % (prefix, get(s)['file'], cur(get(s)['file']), get(s)['code']) for s in slugs)
                    legs.append('<li class="nav-leg"><span class="nav-leg-name">%s</span><span class="nav-leg-links">%s</span></li>' % (lg['name'], links))
            out.append(
                '<li class="has-sub%s"><div class="nav-row"><a href="%s%s">%s</a>'
                '<button type="button" class="nav-sub-toggle" aria-expanded="%s" aria-controls="nav-sub-platform" '
                'aria-label="展開%s的產品">▾</button></div>'
                '<ul class="nav-sub" id="nav-sub-platform"%s><li class="nav-all"><a href="%snexus.html#platform"%s>%s</a></li>%s</ul></li>'
                % (' active' if here else '', prefix, it['href'], it['label'], 'true' if here else 'false', it['label'],
                   '' if here else ' hidden', prefix, cur('nexus.html'), it['overview_label'], ''.join(legs)))
        elif it.get('type') == 'solutions':
            sols = solutions(mods)
            here = page.startswith('solution-')
            cur = lambda f: ' aria-current="page"' if f == page else ''
            groups = {}
            for m in sols:
                groups.setdefault(m['industry'], []).append(m)
            rows = ''.join('<li class="nav-leg"><span class="nav-leg-name">%s</span><span class="nav-leg-links">%s</span></li>'
                           % (ind, ''.join('<a href="%s%s"%s>%s</a>' % (prefix, m['file'], cur(m['file']), m['nav_label'] if m.get('nav_label') else m['name_zh']) for m in ms))
                           for ind, ms in groups.items())
            out.append(
                '<li class="has-sub%s"><div class="nav-row"><a href="%s%s">%s</a>'
                '<button type="button" class="nav-sub-toggle" aria-expanded="%s" aria-controls="nav-sub-solutions" '
                'aria-label="展開%s">▾</button></div><ul class="nav-sub" id="nav-sub-solutions"%s>%s</ul></li>'
                % (' active' if here else '', prefix, it['href'], it['label'], 'true' if here else 'false', it['label'],
                   '' if here else ' hidden', rows))
        elif it.get('external'):
            out.append('<li><a href="%s" target="_blank" rel="noopener">%s<span class="nav-ext" aria-hidden="true">↗</span></a></li>'
                       % (it['href'], it['label']))
        else:
            out.append('<li%s><a href="%s%s">%s</a></li>' % (' class="active"' if it['href'] == page else '', prefix, it['href'], it['label']))
    out.append('</ul>')
    return NAV_BEGIN + '\n' + ''.join(out) + '\n' + NAV_TOGGLE_JS + '\n' + NAV_END


def nav_pages():
    pages = sorted(glob.glob(os.path.join(ROOT, '*.html'))) + sorted(glob.glob(os.path.join(ROOT, 'blogpost', '*.html')))
    return pages + [os.path.join(SRC, 'chrome-top.html')]


def update_nav(mods, pf=None):
    """改寫每一頁的左側選單，並確保載入 css/site-nav.css。回傳有變動的檔案。"""
    pf = pf or load_platform()
    changed = []
    for p in nav_pages():
        s = read(p)
        if 'id="colorlib-main-menu"' not in s:
            continue
        in_blog = os.path.basename(os.path.dirname(p)) == 'blogpost'
        prefix = '../' if in_blog else ''
        # 產品頁外框（chrome-top）只放通用版本；build() 產頁時再換成標出該產品的版本
        block = nav_html(os.path.basename(p), prefix, pf, mods)
        t = NAV_RE.sub(lambda m: m.group(1) + block, s, count=1)
        link = '<link rel="stylesheet" href="%scss/site-nav.css">' % prefix
        if link not in t and '</head>' in t:
            t = t.replace('</head>', '    %s\n  </head>' % link, 1)
        if t != s:
            io.open(p, 'w', encoding='utf-8').write(t)
            changed.append(os.path.relpath(p, ROOT))
    return changed


def main():
    if '--audit' in sys.argv:
        print(audit_report())
        return
    r = build_all()
    if r['errors']:
        print('內容有錯，未產生任何檔案：', file=sys.stderr)
        for e in r['errors']:
            print('  - ' + e, file=sys.stderr)
        sys.exit(1)
    for f in r['written']:
        print('wrote', f)
    for f in r['removed']:
        print('removed', f)


if __name__ == '__main__':
    main()
