#!/usr/bin/env python3
"""產生 AURO NEXUS 模組介紹頁（nexus-<slug>.html）。

內容在 tools/module-pages/<slug>.json，共用外框在 tools/module-pages/chrome-*.html，
樣式在 css/nexus-module.css。改內容後重跑：

    python3 tools/build-module-pages.py

再跑 tools/build-font-subset.sh（新字）與 tools/build-iconoir-subset.sh（新圖示）。
JSON 內的文字欄位允許 <b> <em> <code> <a> 等行內標籤；結構化資料會去掉標籤。
"""
import glob
import html
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
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
    return io.open(p, encoding='utf-8').read()


def plain(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def attr(s):
    return html.escape(plain(s), quote=True)


def load_modules():
    mods = {}
    for p in sorted(glob.glob(os.path.join(SRC, '*.json'))):
        if os.path.basename(p).startswith('_'):
            continue
        m = json.loads(read(p))
        mods[m['slug']] = m
    return mods


def url_of(m):
    return '%s/%s' % (SITE, m['file'])


def jsonld(m):
    page_url = url_of(m)
    graph = [
        {
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
                {'@type': 'ListItem', 'position': 2, 'name': 'AURO NEXUS', 'item': SITE + '/nexus.html'},
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
                        <li><a href="nexus.html">AURO NEXUS</a></li>
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
                            <p class="nm-family">AURO NEXUS 產品家族{(' · <span lang="en">' + m['fullname'] + '</span>') if m.get('fullname') else ''}</p>
                            <h1 class="eyebrow">{h['h1']}</h1>
                            <p class="hero-slogan">{h['slogan']}</p>
                            <p class="hero-sub">{h['sub']}</p>
                            <p class="hero-tagline">{h['tagline']}</p>
                            <div class="hero-actions">
                                <a href="contact.html" class="btn-nm-primary">預約產品簡報</a>
                                <a href="#capabilities" class="btn-nm-outline">看核心能力</a>
                            </div>
                            <div class="nm-badges">{badges}</div>
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
        else:
            sys.exit('%s: platform.related 指到不存在的模組 %s' % (m['slug'], s))
    links.append('<a class="nm-link" href="nexus.html#platform"><b>AURO NEXUS</b><span>平台總覽與全部模組</span></a>')
    out.append(section('nm-platform', 'ON THE PLATFORM', pl['heading'],
        f'                            <div class="platform-text">{pl["text"]}</div>\n'
        f'                            <div class="nm-links">{"".join(links)}</div>'))

    out.append(section('nm-deploy', 'DEPLOYMENT', '部署形態',
        cards(m['deploy'], lambda it: f'''
                                    <div class="deploy-card"><span class="deploy-tag">{it['tag']}</span>
                                        <h3>{it['title']}</h3><p>{it['text']}</p></div>''')))

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


SMOOTH = '''    <script>
    $(function(){
        $('a[href="#capabilities"]').on('click', function(e){
            e.preventDefault();
            $('html, body').animate({ scrollTop: $('#capabilities').offset().top - 50 }, 600);
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
        return pf['extra_modules'][slug]
    return get


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

    def mod_link(slug):
        x = get(slug)
        return f'<a class="leg-mod" href="{x["file"]}"><b>{x["code"]}</b><span>{x["name_zh"]}</span><small>{x["what"]}</small></a>'
    base = pf['legs'][0]
    legs = ''.join(f'''
                                <div class="col-lg-4 col-md-6 mb-4"><div class="leg-card"><p class="leg-name">{lg['name']}</p><p class="leg-text">{lg['text']}</p>{''.join(mod_link(s) for s in lg['modules'])}</div></div>'''
        for lg in pf['legs'][1:])
    n = sum(len(lg['modules']) for lg in pf['legs'])
    out.append(section('nm-legs', 'ARCHITECTURE', f'一個治理底座，{n} 個模組',
        f'''                            <div class="row">{legs}
                            </div>
                            <div class="leg-base"><p class="leg-name">{base['name']}</p><p class="leg-text">{base['text']}所有模組的 AI 呼叫都經過這一層。</p>{''.join(mod_link(s) for s in base['modules'])}</div>''',
        intro='上層的每一個模組各自解決一類問題；下層的治理底座讓它們共用同一套權限、模型與稽核軌跡。', sid='modules'))

    nd = pf['needs']
    rows = ''.join(f'<tr><th scope="row">{need}</th><td><a href="{get(s)["file"]}">{get(s)["code"]} {get(s)["name_zh"]}</a></td></tr>' for need, s in nd['rows'])
    out.append(section('nm-compare', 'WHERE TO START', nd['heading'],
        f'''                            <div class="nm-table-wrap"><table class="nm-table">
                                <thead><tr><th scope="col">您的需求</th><th scope="col">對應模組</th></tr></thead>
                                <tbody>{rows}</tbody></table></div>''', intro=nd['intro']))

    out.append(section('nm-diff', "WHAT'S DIFFERENT", '平台的三個承諾',
        cards(pf['diff'], lambda it: f'''
                                    <div class="diff-card"><i class="iconoir-{it['icon']} diff-icon"></i>
                                        <h3>{it['title']}</h3><p>{it['text']}</p></div>'''), dark=True))

    items = '\n'.join(f'''                                    <div class="faq-item"><h3>{f['q']}</h3><p>{f['a']}</p></div>''' for f in pf['faq'])
    out.append(section('nm-faq', 'FAQ', '關於 AURO NEXUS 的常見問題',
        f'                            <div class="row"><div class="col-lg-10">\n{items}\n                            </div></div>'))
    return BEGIN + '\n<div class="nm-overview" style="--m-deep:#2B3A8C;--m-bright:#4659C9;--m-soft:#8FA0F0;--m-tint:#ECEFFC;--m-ink1:#0C0F1F;--m-ink2:#141A35">' + ''.join(out) + '</div>\n' + END


def overview_jsonld(pf, mods, old_faq):
    get = overview_mods(pf, mods)
    url = SITE + '/nexus.html'
    slugs = [s for lg in pf['legs'] for s in lg['modules']]
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


def build_overview(mods):
    pf = json.loads(read(os.path.join(SRC, '_platform.json')))
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
    io.open(p, 'w', encoding='utf-8').write(s)
    print('updated nexus.html overview')


LLMS_BEGIN, LLMS_END = '<!-- MODULES:BEGIN（由 tools/build-module-pages.py 產生）-->', '<!-- MODULES:END -->'


def update_llms(mods):
    pf = json.loads(read(os.path.join(SRC, '_platform.json')))
    get = overview_mods(pf, mods)
    b = ['## AURO NEXUS 產品一覽', '', ''.join(plain(x) for x in pf['definition']['a']), '',
         '平台總覽：[AURO NEXUS](nexus.html)', '']
    for lg in pf['legs']:
        b.append('### ' + lg['name'])
        for slug in lg['modules']:
            x = get(slug)
            desc = plain(mods[slug]['description']) if slug in mods else x['what']
            b.append('- [%s %s](%s): %s' % (x['code'], x['name_zh'], x['file'], desc))
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


def main():
    top = read(os.path.join(SRC, 'chrome-top.html'))
    bottom = read(os.path.join(SRC, 'chrome-bottom.html'))
    mods = load_modules()
    for m in mods.values():
        out = os.path.join(ROOT, m['file'])
        io.open(out, 'w', encoding='utf-8').write(build(m, mods, top, bottom))
        print('wrote', m['file'])
    build_overview(mods)
    update_llms(mods)
    update_sitemap(mods)


if __name__ == '__main__':
    main()
