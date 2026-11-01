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
    'email': 'ad@aurocore.com',
    'contactPoint': {'@type': 'ContactPoint', 'contactType': 'sales', 'telephone': '+886-2-5568-4688',
                     'email': 'ad@aurocore.com', 'areaServed': 'TW', 'availableLanguage': ['zh-Hant', 'en']},
    'sameAs': ['https://www.facebook.com/AurobaseTW/'],
    'legalName': '奧洛股份有限公司',
    'description': '奧洛（Aurobase）提供 AURO NEXUS AI 治理平台與產業解決方案，代理 HCL Discover、HCL Unica、Magnolia CMS 等行銷科技產品，並提供數位廣告投放、社群經營、AI 智慧語伴與客服中心服務。',
    'areaServed': {'@type': 'Country', 'name': '台灣'},
    'knowsAbout': ['AI 治理', '生成式 AI', '地端 AI', '企業知識庫', '客戶數據平台', '行銷自動化', '數位體驗分析',
                   '資料治理', '資安弱點掃描', '數位廣告投放', '社群經營'],
}
WEBSITE = {
    '@type': 'WebSite',
    '@id': SITE + '/#website',
    'name': '奧洛 Aurobase',
    'alternateName': ['Aurobase', '奧洛'],
    'url': SITE + '/',
    'inLanguage': 'zh-Hant-TW',
    'publisher': {'@id': SITE + '/#organization'},
    # 任何頁面網址帶 ?q= 會直接打開網站搜尋（js/site-search.js）
    'potentialAction': {'@type': 'SearchAction', 'target': {'@type': 'EntryPoint', 'urlTemplate': SITE + '/?q={search_term_string}'},
                        'query-input': 'required name=search_term_string'},
}


OG_W, OG_H = 1200, 630


def og_key(rel_or_slug):
    """分享圖檔名：nexus-forge.html → nexus-forge、index.html → index、blogpost/x.html → blogpost-x。"""
    return re.sub(r'\.html$', '', rel_or_slug).replace('/', '-')


def og_image(key):
    """該頁的分享圖（tools/build-og-images.py 產生）；還沒畫的頁面用預設圖。"""
    p = 'images/og/%s.jpg' % key
    return p if os.path.exists(os.path.join(ROOT, p)) else 'images/og/default.jpg'


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


# 對外頁面不寫進度：計畫中的能力寫成「提供」，環境依賴寫成導入前提（Roger 2026-11-01）
STATUS_RE = re.compile(r'建置中|規劃中|開發中|調校中|驗證中|測試中|實測中|試營運|原型|即將推出|敬請期待|目前版本|目前階段|'
                       r'POC 階段|尚未(?:提供|支援|實作|上線|實測|部署|開放|驗證)|(?:於|在)導入時驗證|roadmap', re.I)


def status_words(d, path=''):
    """回傳 [(欄位路徑, 命中的字)]：產品 JSON 裡描述開發進度的字眼。"""
    if isinstance(d, str):
        return [(path, x.group(0)) for x in STATUS_RE.finditer(d)]
    items = d.items() if isinstance(d, dict) else enumerate(d) if isinstance(d, list) else []
    return [hit for k, v in items if not str(k).startswith('_') for hit in status_words(v, '%s.%s' % (path, k) if path else str(k))]


def validate(m, mods, pf):
    errors, warnings = [], []
    for path, w in status_words(m):
        errors.append('%s 寫了進度字眼「%s」：計畫中的能力請寫成提供的功能，環境依賴寫成導入前提' % (path, w))

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
    for it in g(m, 'shots', 'items') or []:
        if not os.path.exists(os.path.join(ROOT, it.get('src', ''))):
            errors.append('shots 的圖片「%s」不存在' % it.get('src'))
        if not it.get('alt'):
            errors.append('shots 的圖片「%s」缺替代文字（alt）' % it.get('src'))
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
    errors = ['平台總覽 %s 寫了進度字眼「%s」' % hit for hit in status_words(pf)]
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
    img = {'@type': 'ImageObject', 'url': '%s/%s' % (SITE, og_image_of(m)), 'width': OG_W, 'height': OG_H}
    published = load_modules()
    related = [{'@id': '%s/%s.html#software' % (SITE, r)} for r in m['platform']['related'] if r in published]
    audience = {'@type': 'BusinessAudience', 'audienceType': '、'.join(a['who'] for a in m['audience'])}
    keywords = ', '.join(k for k in m['keywords'] if k != 'AURO NEXUS')
    if is_solution(m):
        main = {
            '@type': 'Service',
            '@id': page_url + '#software',
            'name': full_name(m),
            'alternateName': [m['eyebrow']] + m.get('aliases', []) + ([m['fullname']] if m.get('fullname') else []),
            'serviceType': m['name_zh'],
            'category': m['industry'],
            'description': plain(m['description']),
            'audience': audience,
            'areaServed': {'@type': 'Country', 'name': '台灣'},
            'provider': {'@id': ORG['@id']},
            'url': page_url,
            'image': img,
            'keywords': keywords,
            'isRelatedTo': related,
        }
    else:
        main = {
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
            'image': img,
            'isPartOf': {'@id': SITE + '/nexus.html#platform'},
            'publisher': {'@id': ORG['@id']},
            'audience': audience,
            'keywords': keywords,
            'dateModified': m['updated'],
            'featureList': [plain(c['title']) for c in m['capabilities']['cards']],
            'isRelatedTo': related,
        }
        shots = (m.get('shots') or {}).get('items')
        if shots:
            main['screenshot'] = [{'@type': 'ImageObject', 'url': '%s/%s' % (SITE, x['src']), 'caption': plain(x['title'] + '：' + x['caption'])} for x in shots]
    if not related:
        del main['isRelatedTo']
    term = defined_term(m)
    graph = [
        main,
        {
            '@type': 'WebPage',
            '@id': page_url + '#webpage',
            'url': page_url,
            'name': m['title'],
            'description': plain(m['description']),
            'inLanguage': 'zh-Hant-TW',
            'dateModified': m['updated'],
            'about': [{'@id': page_url + '#software'}] + ([{'@id': term['@id']}] if term else []),
            'mainEntity': {'@id': page_url + '#software'},
            'primaryImageOfPage': img,
            'keywords': keywords,
            # 語音助理與 AI 摘要優先朗讀的段落：定義與重點摘要
            'speakable': {'@type': 'SpeakableSpecification', 'cssSelector': ['#what-is .define-answer', '.nm-summary']},
            'breadcrumb': {'@id': page_url + '#breadcrumb'},
            'isPartOf': {'@type': 'WebSite', '@id': SITE + '/#website', 'name': '奧洛 Aurobase', 'url': SITE + '/'},
            'publisher': {'@id': ORG['@id']},
        },
        {
            '@type': 'BreadcrumbList',
            '@id': page_url + '#breadcrumb',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': '首頁', 'item': SITE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': '產業解決方案' if is_solution(m) else 'AURO NEXUS',
                 'item': SITE + ('/nexus.html#solutions' if is_solution(m) else '/nexus.html')},
                {'@type': 'ListItem', 'position': 3, 'name': m['code'], 'item': page_url},
            ],
        },
        ORG,
    ]
    if term:
        graph.insert(2, term)
    if m.get('flow'):
        # 解決方案的運作流程：每一步做什麼、由哪些元件負責
        graph.append({
            '@type': 'HowTo',
            '@id': page_url + '#flow',
            'name': '%s的運作流程' % m['name_zh'],
            'description': plain(m.get('flow_intro') or m['description']),
            'step': [{'@type': 'HowToStep', 'position': i, 'name': plain(st['title']), 'text': plain(st.get('text', '')),
                      'url': page_url + '#flow'} for i, st in enumerate(m['flow'], 1)],
        })
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
    og_image = og_image_of(m)
    og_alt = attr('%s｜%s' % (full_name(m), plain(m['hero'].get('slogan', '')).replace(' ', '')))
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
    <meta property="og:image:width" content="{OG_W}">
    <meta property="og:image:height" content="{OG_H}">
    <meta property="og:image:alt" content="{og_alt}">
    <meta property="article:modified_time" content="{m['updated']}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{attr(title)}">
    <meta name="twitter:description" content="{attr(m.get('og_description', m['description']))}">
    <meta name="twitter:image" content="{SITE}/{og_image}">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
    <meta name="theme-color" content="{m['theme']['deep']}">

    <script type="application/ld+json">
{jsonld(m)}
</script>

    <link href="images/favicon.ico" rel="shortcut icon">
    <link rel="preload" href="WOFF2/LINESeedSans_W_Rg.woff2" as="font" type="font/woff2" crossorigin>
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


def og_image_of(m):
    """產品頁的分享圖：JSON 指定的 og_image 優先（例如 SAGA 用實機畫面），否則用 build-og-images.py 畫的卡片。"""
    return m.get('og_image') or og_image(og_key(m['slug']))


def defined_term(m):
    """把「什麼是 X？」的定義段落做成 DefinedTerm，讓 AI 引擎拿得到名詞與一句話定義。"""
    q = plain(m['definition']['q'])
    hit = re.match(r'^(?:什麼是|何謂)(.+?)[？?]$', q) or re.match(r'^(.+?)\s*是什麼[？?]$', q)
    if not hit:
        return None   # 問題不是在定義名詞（例如「第一步該做什麼？」），就不硬做詞條
    name = hit.group(1).strip()
    return {'@type': 'DefinedTerm', '@id': url_of(m) + '#term', 'name': name,
            'description': plain(m['definition']['a'][0]), 'url': url_of(m) + '#what-is',
            'inDefinedTermSet': {'@type': 'DefinedTermSet', '@id': SITE + '/nexus.html#glossary', 'name': 'AURO NEXUS 名詞解釋'}}


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
                                <a href="contact.html" class="btn-nm-primary" data-toggle="modal" data-target="#myModal">預約產品簡報</a>
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
    # 3 欄排到最後一列只剩一張時（4、7 張），大螢幕改排 4 欄
    cap_cols = 'col-xl-3 col-lg-4 col-md-6 mb-4' if len(c['cards']) % 3 == 1 and len(c['cards']) > 3 else 'col-lg-4 col-md-6 mb-4'
    out.append(section('nm-cap', 'CAPABILITIES', c['heading'],
        cards(c['cards'], cols=cap_cols, render=lambda it: f'''
                                    <div class="cap-card"><div class="icon-wrap"><i class="iconoir-{it['icon']}"></i></div>
                                        <h3>{it['title']}</h3><ul>{''.join('<li>%s</li>' % li for li in it['items'])}</ul></div>'''),
        intro=c.get('intro'), sid='capabilities'))

    sh = m.get('shots')
    if sh:
        figs = ''.join(f'''
                                <figure class="nm-shot"><a href="{it['src']}" target="_blank" rel="noopener"><img src="{it['src']}" alt="{attr(it['alt'])}" loading="lazy"></a>
                                    <figcaption><b>{it['title']}</b>{it['caption']}</figcaption></figure>''' for it in sh['items'])
        note = f'\n                            <p class="nm-source">{sh["note"]}</p>' if sh.get('note') else ''
        out.append(section('nm-shots', 'PLATFORM SCREENS', sh['heading'],
            f'                            <div class="nm-shot-grid">{figs}\n                            </div>{note}',
            intro=sh.get('intro'), sid='screens'))

    ev = m.get('evidence')
    if ev:
        tiles = ''.join(f'<div class="nm-metric"><b>{x["value"]}</b><span>{x["label"]}</span><p>{x["text"]}</p></div>' for x in ev.get('metrics', []))
        items = ''.join(f'<div class="nm-proof"><h3>{x["title"]}</h3><p>{x["text"]}</p></div>' for x in ev.get('items', []))
        out.append(section('nm-evidence', 'MEASURED', ev['heading'],
            f'                            <div class="nm-metrics">{tiles}</div>\n                            <div class="nm-proofs">{items}</div>',
            intro=ev.get('intro')))

    rg = m.get('regulation')
    if rg:
        rows = ''.join(f'<tr><th scope="row">{r[0]}</th><td data-label="{attr(rg["cols"][1])}">{r[1]}</td></tr>' for r in rg['rows'])
        src = '；'.join(f'<a href="{s["url"]}" target="_blank" rel="noopener">{s["name"]}</a>' for s in rg['sources'])
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
            f'<td data-label="{attr(cp["cols"][i])}"{" class=is-us" if i == len(r) - 2 else ""}>{v}</td>' for i, v in enumerate(r[1:]))) for r in cp['rows'])
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
        out.append(section('nm-limits', 'BEFORE YOU START', '導入前提',
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
                    <a class="btn-cta" href="contact.html" data-toggle="modal" data-target="#myModal">預約產品簡報</a>
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


def need_index(need, slug, mods, primary):
    """「依需求找模組」搜尋框比對用的文字。primary：需求敘述、產品名、關鍵字與搜尋用詞（命中加倍計分）；
    其餘：搜尋摘要、產品定義、適合對象與能力標題。"""
    m = mods.get(slug) or {}
    if primary:
        parts = [need, m.get('code', ''), m.get('name_zh', ''), m.get('eyebrow', ''), m.get('fullname', '')]
        parts += m.get('aliases', []) + m.get('keywords', []) + m.get('search_terms', [])
    else:
        parts = [plain(m.get('description', '')), plain(dict(m.get('summary', [])).get('是什麼', ''))]
        parts += [a['who'] + a['why'] for a in m.get('audience', [])]
        parts += [c['title'] for c in (m.get('capabilities') or {}).get('cards', [])]
        parts += [plain(f['q']) for f in m.get('faq', [])]
    return ' '.join(p for p in parts if p and p != 'AURO NEXUS').lower()


SEARCH_INDEX = 'search-index.json'


def search_entries(mods, pf):
    """全站搜尋索引：已發布的產品與解決方案自動產生，其他頁面的服務取自 _search.json，新聞取自各篇標題。"""
    needs = {}
    for need, slug in pf['needs']['rows']:
        needs.setdefault(slug, []).append(need)
    out = []
    for slug, m in mods.items():
        out.append({'t': full_name(m), 'u': m['file'], 'c': '產業解決方案' if is_solution(m) else '平台模組',
                    'd': plain(dict(m['summary'])['是什麼']),
                    'k': need_index(' '.join(needs.get(slug, [])), slug, mods, True),
                    's': need_index('', slug, mods, False)})
    for e in json.loads(read(os.path.join(SRC, '_search.json')))['entries']:
        out.append({'t': e['title'], 'u': e['url'], 'c': e['cat'], 'd': e['desc'],
                    'k': ' '.join([e['title']] + e['terms']).lower(), 's': e['desc'].lower()})
    for rel, cfg in sorted(load_pages_cfg().items()):
        if cfg.get('type') != 'BlogPosting' or not os.path.exists(os.path.join(ROOT, rel)):
            continue
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', read(os.path.join(ROOT, rel)), re.S)
        title = plain(h1.group(1)) if h1 else rel
        out.append({'t': title, 'u': rel, 'c': '新聞中心', 'd': cfg['description'],
                    'k': title.lower(), 's': cfg['description'].lower()})
    return out


def update_search_index(mods, pf):
    p = os.path.join(ROOT, SEARCH_INDEX)
    text = json.dumps(search_entries(mods, pf), ensure_ascii=False, separators=(',', ':')) + '\n'
    if not os.path.exists(p) or read(p) != text:
        io.open(p, 'w', encoding='utf-8').write(text)


# 需求搜尋：比對交給 js/site-search.js（與側欄全站搜尋同一套），這裡只負責顯示與排序表格列。
# 搜尋框裡打的字會在「把這個需求告訴我們」時帶進詢問表單；網址帶 ?q= 時直接帶入搜尋。
FINDER_JS = r"""document.addEventListener('DOMContentLoaded',function(){
var box=document.getElementById('finder'),S=window.AuroSearch;if(!box||!S)return;
var q=box.querySelector('#nm-finder-q'),clr=box.querySelector('.nm-finder-clear'),msg=box.querySelector('.nm-finder-msg'),
none=box.querySelector('.nm-finder-none'),tb=box.querySelector('.nm-table-needs tbody'),wrap=box.querySelector('.nm-table-wrap');
var rows=[].slice.call(tb.rows),order=rows.slice();
var entries=rows.map(function(r){return {k:S.norm(r.getAttribute('data-key')),s:S.norm(r.getAttribute('data-search'))};});
function run(){var v=q.value.trim();clr.hidden=!v;
 if(!v){order.forEach(function(r){r.hidden=false;tb.appendChild(r);});msg.textContent='';none.hidden=true;wrap.hidden=false;return;}
 var res=S.rank(v,entries);rows.forEach(function(r){r.hidden=true;});
 res.forEach(function(x){rows[x.i].hidden=false;tb.appendChild(rows[x.i]);});
 msg.textContent=res.length?'找到 '+res.length+' 個相關的模組或方案，最相關的排在前面。':'';
 none.hidden=res.length>0;wrap.hidden=!res.length;}
q.addEventListener('input',run);
clr.addEventListener('click',function(){q.value='';run();q.focus();});
box.querySelector('.nm-finder-ask').addEventListener('click',function(){var t=document.getElementById('f06');if(t&&q.value.trim()&&!t.value)t.value=q.value.trim();});
var m=/[?&]q=([^&#]*)/.exec(location.search);if(m){q.value=decodeURIComponent(m[1].replace(/\+/g,' '));run();}
});"""


def full_name(x):
    """代號加中文名；解決方案的代號常常就是中文名，不重複寫兩次。"""
    return x['name_zh'] if x['code'] in x['name_zh'] else f"{x['code']} {x['name_zh']}"


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
                                <a href="contact.html" class="btn-nm-primary" data-toggle="modal" data-target="#myModal">預約平台簡報</a>
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
                                <div class="col-xl-3 col-lg-4 col-md-6 mb-4"><div class="leg-card"><p class="leg-name">{lg['name']}</p><p class="leg-text">{lg['text']}</p>{''.join(mod_link(s) for s in live(pf, mods, lg['modules']))}</div></div>'''
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
            # 卡片上的模組標籤取自「由哪些平台模組組成」，每張卡的依據一致
            used = [x for x in m['platform']['related'] if x in mods and not is_solution(mods[x])]
            return (f'<div class="sol-card"><span class="sol-ind">{m["industry"]}</span>'
                    f'<h3><a href="{m["file"]}">{m["name_zh"]}</a></h3><p>{plain(dict(m["summary"])["是什麼"])}</p>'
                    f'<div class="flow-mods">{"".join(module_chip(x, mods) for x in used)}</div></div>')
        out.append(section('nm-cap', 'SOLUTIONS', pf.get('solutions_heading', '產業解決方案'),
            cards(sols, sol_card, cols='col-lg-6 mb-4'), intro=pf.get('solutions_intro'), sid='solutions'))

    nd = pf['needs']
    rows = ''.join(f'<tr data-key="{attr(need_index(need, s, mods, True))}" data-search="{attr(need_index(need, s, mods, False))}"><th scope="row">{need}</th><td><a href="{get(s)["file"]}">{full_name(get(s))}</a></td></tr>'
                   for need, s in nd['rows'] if get(s))
    out.append(section('nm-compare', 'WHERE TO START', nd['heading'],
        f'''                            <form class="nm-finder" role="search" onsubmit="return false">
                                <label for="nm-finder-q">用一句話描述您的需求</label>
                                <div class="nm-finder-row"><input id="nm-finder-q" type="search" autocomplete="off" placeholder="例如：想讓員工安全地使用 ChatGPT、把會員資料整合起來、掃描程式弱點">
                                <button type="button" class="nm-finder-clear" hidden>清除</button></div>
                                <p class="nm-finder-msg" aria-live="polite"></p>
                            </form>
                            <div class="nm-table-wrap"><table class="nm-table nm-table-needs">
                                <thead><tr><th scope="col">您的需求</th><th scope="col">對應模組</th></tr></thead>
                                <tbody>{rows}</tbody></table></div>
                            <div class="nm-finder-none" hidden><p>沒有找到直接對應的模組。您的需求可能需要組合幾個模組或客製，直接告訴我們，我們會回覆建議的做法。</p>
                                <a href="contact.html" class="btn-nm-primary nm-finder-ask" data-toggle="modal" data-target="#myModal">把這個需求告訴我們</a></div>
                            <script>{FINDER_JS}</script>''', intro=nd['intro'], sid='finder'))

    out.append(section('nm-diff', "WHAT'S DIFFERENT", '平台的三個設計',
        cards(pf['diff'], lambda it: f'''
                                    <div class="diff-card"><i class="iconoir-{it['icon']} diff-icon"></i>
                                        <h3>{it['title']}</h3><p>{it['text']}</p></div>'''), dark=True))

    # 名詞解釋：各產品頁「什麼是…」的第一句定義，連回該頁（結構化資料的 DefinedTermSet 指向這裡）
    terms = [(t, m) for t, m in ((defined_term(m), m) for m in mods.values()) if t]
    if terms:
        def first_sentence(x):
            x = plain(x)
            return x[:x.index('。') + 1] if '。' in x else x
        rows = ''.join(f'<div class="gl-item"><dt><a href="{m["file"]}#what-is">{t["name"]}</a></dt>'
                       f'<dd>{first_sentence(m["definition"]["a"][0])}<span class="gl-src">見 <a href="{m["file"]}">{full_name(m)}</a></span></dd></div>'
                       for t, m in sorted(terms, key=lambda x: x[0]['name']))
        out.append(section('nm-glossary', 'GLOSSARY', 'AURO NEXUS 名詞解釋',
            f'                            <dl class="gl-list">{rows}</dl>',
            intro='平台上常見的名詞，一句話說明；完整說明在各產品頁。', sid='glossary'))

    items = '\n'.join(f'''                                    <div class="faq-item"><h3>{f['q']}</h3><p>{f['a']}</p></div>''' for f in pf['faq'])
    out.append(section('nm-faq', 'FAQ', '關於 AURO NEXUS 的常見問題',
        f'                            <div class="row"><div class="col-lg-10">\n{items}\n                            </div></div>'))
    return BEGIN + '\n<div class="nm-overview" style="--m-deep:#2B3A8C;--m-bright:#4659C9;--m-soft:#8FA0F0;--m-tint:#ECEFFC;--m-ink1:#0C0F1F;--m-ink2:#141A35">' + ''.join(out) + '</div>\n' + END


def solutions(mods):
    order = {'公部門': 0, '金融保險': 1, '跨產業': 2}
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
         'image': {'@type': 'ImageObject', 'url': '%s/%s' % (SITE, og_image('nexus')), 'width': OG_W, 'height': OG_H},
         'hasPart': [{'@type': 'SoftwareApplication', 'name': '%s %s' % (get(s)['code'], get(s)['name_zh']),
                      'url': '%s/%s' % (SITE, get(s)['file'])} for s in slugs]},
        # 各產品頁「什麼是…」的定義彙整成名詞集，讓 AI 引擎知道這些名詞在哪裡被定義
        {'@type': 'DefinedTermSet', '@id': SITE + '/nexus.html#glossary', 'name': 'AURO NEXUS 名詞解釋',
         'hasDefinedTerm': [{'@id': t['@id']} for t in (defined_term(m) for m in mods.values()) if t]},
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
    s = apply_social(s, 'nexus.html', og_image('nexus'))
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
    # 需求對照：讓 AI 引擎直接回答「我要做 X，該看哪一個」——與平台總覽「依需求找模組」同一份資料
    b += ['### 依需求找模組', '']
    b += ['- %s → [%s](%s)' % (need, full_name(get(s)), get(s)['file']) for need, s in pf['needs']['rows'] if get(s)]
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


LLMS_FULL = 'llms-full.txt'


def llms_full(mods, pf):
    """llms-full.txt：每個產品與解決方案的完整內容（定義、能力、運作流程、範圍、部署、常見問題），給 AI 引擎一次讀完。"""
    def li(items):
        return ['- ' + plain(x) for x in items]
    out = ['# 奧洛 Aurobase — AURO NEXUS 產品與解決方案完整說明', '',
           '> ' + ''.join(plain(x) for x in pf['definition']['a']), '',
           '公司：奧洛股份有限公司（Aurobase）｜網站：%s｜電話：+886-2-5568-4688｜Email：ad@aurocore.com' % SITE,
           '本檔由網站內容自動產生，與各產品頁一致。精簡索引見 %s/llms.txt。' % SITE, '']
    order = [s for lg in pf['legs'] for s in live(pf, mods, lg['modules'])] + [m['slug'] for m in solutions(mods)]
    for slug in order:
        m = mods[slug]
        out += ['', '## %s' % full_name(m), '', '網址：%s' % url_of(m),
                ('類別：產業解決方案（%s）' % m['industry']) if is_solution(m) else ('類別：平台模組（%s）' % m['leg']),
                '最後更新：%s' % m['updated'], '', plain(m['description']), '',
                '### %s' % plain(m['definition']['q'])] + [plain(x) for x in m['definition']['a']]
        out += ['', '### 適合誰'] + ['- %s：%s' % (a['who'], a['why']) for a in m['audience']]
        if m.get('flow'):
            out += ['', '### 運作流程'] + ['%d. %s：%s' % (i, plain(st['title']), plain(st.get('text', ''))) for i, st in enumerate(m['flow'], 1)]
        out += ['', '### ' + plain(m['capabilities']['heading'])]
        for c in m['capabilities']['cards']:
            out += ['- **%s**：%s。' % (plain(c['title']), '；'.join(plain(x).rstrip('。') for x in c['items']))]
        out += ['', '### ' + plain(m['diff']['heading'])] + ['- **%s**：%s' % (plain(c['title']), plain(c['text'])) for c in m['diff']['cards']]
        if m.get('compare'):
            cp = m['compare']
            out += ['', '### ' + plain(cp['heading'])] + ['- %s：%s' % (plain(r[0]), '｜'.join('%s：%s' % (plain(cp['cols'][i]), plain(v)) for i, v in enumerate(r[1:]))) for r in cp['rows']]
        out += ['', '### 部署：可雲、可地、可客製'] + ['- %s｜%s：%s' % (d['tag'], plain(d['title']), plain(d['text'])) for d in m['deploy']]
        if m.get('limits'):
            out += ['', '### 導入前提'] + ['- **%s**：%s' % (plain(x['title']), plain(x['text'])) for x in m['limits']]
        if m.get('faq'):
            out += ['', '### 常見問題'] + sum([['**問：%s**' % plain(f['q']), '答：%s' % plain(f['a']), ''] for f in m['faq']], [])
    out += ['', '## 其他服務與代理產品', '']
    for e in json.loads(read(os.path.join(SRC, '_search.json')))['entries']:
        if e['cat'] in ('數位行銷服務', '代理產品', 'AI 智慧語伴', '客服中心'):
            u = e['url'] if e['url'].startswith('http') else '%s/%s' % (SITE, e['url'])
            out.append('- [%s](%s)（%s）：%s' % (e['title'], u, e['cat'], e['desc']))
    for rel, cfg in load_pages_cfg().items():
        if cfg.get('faq'):
            title = html.unescape(re.search(r'<title>(.*?)</title>', read(os.path.join(ROOT, rel)), re.S).group(1)) if os.path.exists(os.path.join(ROOT, rel)) else rel
            out += ['', '### %s：常見問題（%s/%s）' % (re.sub(r'\s*[｜|].*$', '', title), SITE, rel), '']
            out += sum([['**問：%s**' % f['q'], '答：%s' % f['a'], ''] for f in cfg['faq']], [])
    return '\n'.join(re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).split('\n')).rstrip() + '\n'


def update_llms_full(mods, pf):
    p = os.path.join(ROOT, LLMS_FULL)
    text = llms_full(mods, pf)
    if not os.path.exists(p) or read(p) != text:
        io.open(p, 'w', encoding='utf-8').write(text)


HOME_BEGIN, HOME_END = '<!-- HOME-CATALOG:BEGIN -->', '<!-- HOME-CATALOG:END -->'
ARROW = ('<svg class="idx-arrow" width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" '
         'stroke-width="1.8" aria-hidden="true"><path d="M3 9L9 3M4 3h5v5"/></svg>')


def home_catalog(mods, pf):
    """首頁的全產品、全服務目錄：平台模組依能力分組、產業解決方案、代理產品、服務。新產品上架會自動出現。"""
    get = overview_mods(pf, mods)
    entries = json.loads(read(os.path.join(SRC, '_search.json')))['entries']

    def sec(num, sid, eyebrow, title, more, inner, intro=''):
        more_html = ('<a href="%s" class="idx-more">%s%s</a>' % (more[0], more[1], ARROW)) if more else ''
        intro_html = '\n    <p class="hc-intro">%s</p>' % intro if intro else ''
        return f'''
  <section id="{sid}" class="idx-section idx-wrap">
    <div class="idx-sec-head">
      <div class="idx-sec-title-group">
        <span class="idx-sec-num">{num}</span>
        <div>
          <div class="idx-eyebrow">// {num} — {eyebrow}</div>
          <h2 class="idx-sec-title">{title}</h2>
        </div>
      </div>
      {more_html}
    </div>
    <div class="idx-rule"></div>{intro_html}
{inner}
  </section>
'''

    def card(meta, title, href, desc, cta='了解更多', external=False):
        ext = ' target="_blank" rel="noopener"' if external else ''
        return (f'      <article class="idx-card is-compact"><div class="idx-card-meta"><span>// {meta}</span></div>'
                f'<h3 class="idx-card-title"><a href="{href}" class="idx-card-link"{ext}>{title}</a></h3>'
                f'<p class="idx-card-desc">{desc}</p><span class="idx-card-cta" aria-hidden="true">{cta}{ARROW}</span></article>')

    legs = []
    for lg in pf['legs']:
        slugs = live(pf, mods, lg['modules'])
        if not slugs:
            continue
        links = ''.join(f'<a class="hc-mod" href="{get(x)["file"]}"><b>{get(x)["code"]}</b><span>{get(x)["name_zh"]}</span>'
                        f'<small>{get(x)["what"]}</small></a>' for x in slugs)
        legs.append(f'      <div class="hc-leg"><p class="hc-leg-name">{lg["name"]}</p>{links}</div>')
    n = sum(len(live(pf, mods, lg['modules'])) for lg in pf['legs'])
    out = [HOME_BEGIN, sec('01', 'idx-catalog', '自有產品', 'AURO NEXUS AI 治理平台', ('nexus.html', '平台總覽'),
                           '    <div class="hc-legs">\n' + '\n'.join(legs) + '\n    </div>',
                           '以 Forge 治理底座串起 %d 個模組：每一次 AI 呼叫都經過權限與政策檢查並留下紀錄，可部署於雲端、地端，也可依需求客製。' % n)]
    sols = solutions(mods)
    if sols:
        out.append(sec('02', 'idx-solutions', '由平台模組組成', '產業解決方案', ('nexus.html#solutions', '全部方案'),
                       '    <div class="idx-grid">\n' + '\n'.join(card(m['industry'], full_name(m), m['file'], plain(dict(m['summary'])['是什麼'])) for m in sols) + '\n    </div>'))
    agency = [e for e in entries if e['cat'] == '代理產品']
    out.append(sec('03', 'idx-agency', '代理與導入', '代理產品', ('solution.html', '代理產品總覽'),
                   '    <div class="idx-grid">\n' + '\n'.join(card('代理產品', e['title'], e['url'], e['desc']) for e in agency) + '\n    </div>'))
    mk = [e for e in entries if e['cat'] == '數位行銷服務' and '#' in e['url']]
    svc = [card('數位行銷服務', '數位行銷', 'marketing.html',
                '廣告投放、社群經營與網站數據分析的整合行銷服務。').replace(
               '<span class="idx-card-cta"', '<div class="hc-sublinks">%s</div><span class="idx-card-cta"' %
               ''.join('<a href="%s">%s</a>' % (e['url'], e['title']) for e in mk), 1)]
    for e in entries:
        if e['cat'] in ('AI 智慧語伴', '客服中心'):
            ext = e['url'].startswith('http')
            svc.append(card(e['cat'], e['title'], e['url'], e['desc'], '前往 AUROCORE' if ext else '了解更多', ext))
    out.append(sec('04', 'idx-services', '服務', '數位行銷、AI 語伴與客服中心', ('marketing.html', '數位行銷服務'),
                   '    <div class="idx-grid">\n' + '\n'.join(svc) + '\n    </div>'))
    out.append(HOME_END)
    return '\n'.join(out)


def update_home(mods, pf):
    p = os.path.join(ROOT, 'index.html')
    s = read(p)
    if HOME_BEGIN not in s:
        return
    t = s[:s.index(HOME_BEGIN)] + home_catalog(mods, pf) + s[s.index(HOME_END) + len(HOME_END):]
    if t != s:
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
    # 移除已不存在（刪除或改回草稿）的產品頁與解決方案頁
    def gone(mo):
        f = mo.group(1)
        return '' if not os.path.exists(os.path.join(ROOT, f)) else mo.group(0)
    t = re.sub(r'[ \t]*<url><loc>%s/((?:nexus|solution)-[a-z0-9-]+\.html)</loc>.*?</url>\n?' % re.escape(SITE), gone, t)

    # 每一頁附上分享圖與實機畫面（圖片搜尋與 AI 摘要用），新聞文章補上日期
    pages = load_pages_cfg()
    by_file = {m['file']: m for m in mods.values()}

    def enrich(mo):
        loc, rest = mo.group(1), mo.group(2)
        rest = re.sub(r'<image:image>.*?</image:image>', '', rest)
        rel = loc[len(SITE) + 1:] or 'index.html'
        m, cfg = by_file.get(rel), pages.get(rel, {})
        if cfg.get('type') == 'BlogPosting' and '<lastmod>' not in rest:
            rest = '<lastmod>%s</lastmod>' % cfg.get('modified', cfg['date']) + rest
        imgs = [og_image_of(m) if m else og_image(og_key(rel))]
        imgs += [x['src'] for x in ((m or {}).get('shots') or {}).get('items', [])]
        tags = ''.join('<image:image><image:loc>%s/%s</image:loc></image:image>' % (SITE, i) for i in imgs if not i.endswith('default.jpg'))
        return '<url><loc>%s</loc>%s%s</url>' % (loc, rest, tags)
    t = re.sub(r'<url><loc>([^<]+)</loc>(.*?)</url>', enrich, t)
    if 'xmlns:image=' not in t:
        t = t.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">', 1)
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
    pl_text = (m.get('platform') or {}).get('text', '')
    rel = len(set((m.get('platform') or {}).get('related') or []) |
              {re.sub(r'\.html.*$', '', h) for h in re.findall(r'href="([a-z0-9-]+\.html)', pl_text)} - {m.get('slug')})
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


NOT_INDEXED = ('404.html',)   # 不收錄、不稽核的頁面（404 頁標 noindex）


def site_pages():
    pages = sorted(glob.glob(os.path.join(ROOT, '*.html'))) + sorted(glob.glob(os.path.join(ROOT, 'blogpost', '*.html')))
    return [r for r in (os.path.relpath(p, ROOT) for p in pages) if r not in NOT_INDEXED]


def page_audit(rel):
    """單一 HTML 頁的 SEO / GEO 檢查（全站共用，不分是否由產生器產出）。"""
    s = read(os.path.join(ROOT, rel))
    C = []
    head = s[:s.find('</head>')] if '</head>' in s else s
    m = re.search(r'<title>(.*?)</title>', head, re.S)
    title = html.unescape(m.group(1).strip()) if m else ''
    C.append(_chk('SEO', 'pass' if title and disp_width(title) <= 32 else ('warn' if title else 'fail'), '頁面標題',
                  '%s（%.0f 格）' % (title, disp_width(title)) if title else '沒有 <title>'))
    m = re.search(r'<meta name="description" content="([^"]*)"', head)
    desc = html.unescape(m.group(1)) if m else ''
    C.append(_chk('SEO', 'pass' if 70 <= len(desc) <= 160 else ('warn' if desc else 'fail'), '搜尋摘要（meta description）',
                  '%d 字（建議 70～160）' % len(desc) if desc else '沒有 meta description'))
    want = SITE + '/' + ('' if rel == 'index.html' else rel)
    m = re.search(r'<link rel="canonical" href="([^"]*)"', head)
    can = m.group(1) if m else ''
    C.append(_chk('SEO', 'pass' if can in (want, SITE + '/' + rel) else 'fail', 'canonical 指向本頁正式網址',
                  can or '沒有 canonical'))
    lang = re.search(r'<html[^>]*\blang="([^"]+)"', s)
    C.append(_chk('SEO', 'pass' if lang and lang.group(1).lower().startswith('zh-hant') else 'warn', '語言標記 zh-Hant-TW',
                  lang.group(1) if lang else '沒有 lang'))
    body = strip_comments(s)
    h1 = len(re.findall(r'<h1[\s>]', body))
    C.append(_chk('SEO', 'pass' if h1 == 1 else 'fail', '只有一個 H1', '%d 個' % h1))
    og = [k for k in ('og:title', 'og:description', 'og:image', 'og:url') if 'property="%s"' % k not in head]
    C.append(_chk('SEO', 'pass' if not og else 'warn', '社群分享資訊（Open Graph）', '缺：' + '、'.join(og) if og else ''))
    m = re.search(r'<meta property="og:image" content="([^"]*)"', head)
    ogi = m.group(1) if m else ''
    local = ogi[len(SITE) + 1:] if ogi.startswith(SITE + '/') else ''
    prob = ('沒有分享圖' if not ogi else 'SVG 在 Facebook、LINE 不會顯示' if ogi.lower().endswith('.svg')
            else '圖檔不存在：' + local if local and not os.path.exists(os.path.join(ROOT, local))
            else '缺 og:image:width／height' if 'og:image:width' not in head else '')
    C.append(_chk('SEO', 'pass' if not prob else 'warn', '社群分享圖（點陣圖、附尺寸）', prob or local))
    C.append(_chk('SEO', 'pass' if 'name="twitter:card"' in head and 'max-image-preview:large' in head else 'warn',
                  'Twitter 卡片與大圖預覽'))
    imgs = re.findall(r'<img\b[^>]*>', body)
    noalt = [i for i in imgs if not re.search(r'\balt="[^"]+"', i)]
    C.append(_chk('SEO', 'pass' if not noalt else 'warn', '圖片都有替代文字（alt）',
                  '%d 張缺 alt' % len(noalt) if noalt else '%d 張圖' % len(imgs)))
    broken = []
    base = os.path.dirname(os.path.join(ROOT, rel))
    for h in re.findall(r'href="([^"#?:]+\.html)(?:[#?][^"]*)?"', body):
        if not os.path.exists(os.path.normpath(os.path.join(base, h))):
            broken.append(h)
    C.append(_chk('SEO', 'pass' if not broken else 'fail', '站內連結都有效', '、'.join(sorted(set(broken))[:5])))
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    types, bad = [], 0
    for b in blocks:
        try:
            d = json.loads(b)
            for n in d.get('@graph', [d]):
                t = n.get('@type')
                types += t if isinstance(t, list) else [t]
        except ValueError:
            bad += 1
    C.append(_chk('GEO', 'fail' if bad else ('pass' if blocks else 'warn'), '結構化資料（JSON-LD）',
                  '有 %d 段無法解析' % bad if bad else ('、'.join(sorted(set(filter(None, types)))) if blocks else '沒有結構化資料')))
    C.append(_chk('GEO', 'pass' if 'Organization' in types or '"@id": "%s/#organization"' % SITE in s else 'warn',
                  '結構化資料標明奧洛（Organization）'))
    has_faq_html = bool(re.search(r'常見問題|FAQ', s))
    C.append(_chk('GEO', 'pass' if (not has_faq_html or 'FAQPage' in types) else 'warn', '頁面上的常見問題有 FAQPage 結構化資料'))
    sm = read(os.path.join(ROOT, 'sitemap.xml'))
    C.append(_chk('全站', 'pass' if ('<loc>%s</loc>' % want) in sm or ('<loc>%s/%s</loc>' % (SITE, rel)) in sm else 'warn',
                  'sitemap.xml 收錄這一頁'))
    llms = read(os.path.join(ROOT, 'llms.txt'))
    C.append(_chk('全站', 'pass' if '(%s)' % rel in llms or rel == 'index.html' else 'warn', 'llms.txt 收錄這一頁'))
    if not rel.startswith('blogpost/'):   # 新聞稿是當時的紀錄，不改寫
        txt = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)\b.*?</\1>', '', body, flags=re.S)))
        hits = sorted(set(x.group(0) for x in STATUS_RE.finditer(txt)))
        C.append(_chk('全站', 'fail' if hits else 'pass', '內容不寫開發進度（建置中、規劃中…）', '、'.join(hits)))
    score = {}
    for g in ('SEO', 'GEO', '全站'):
        rows = [c for c in C if c['group'] == g]
        score[g] = [sum(c['status'] == 'pass' for c in rows), len(rows)]
    return {'page': rel, 'title': title, 'checks': C, 'score': score}


def site_audit():
    return [page_audit(rel) for rel in site_pages()]


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
    lines.append('')
    lines.append('── 全站逐頁 ──')
    for a in site_audit():
        sc = '  '.join('%s %d/%d' % (g, *v) for g, v in a['score'].items())
        lines.append('%-34s %s' % (a['page'], sc))
        for c in a['checks']:
            if c['status'] in ('fail', 'warn'):
                lines.append('    %s %s %s' % ('✗' if c['status'] == 'fail' else '△', c['label'], c['detail']))
    return '\n'.join(lines)


# ── 手寫頁：依 _pages.json 補搜尋摘要、結構化資料與單一 H1 ──

LD_BEGIN, LD_END = '<!-- SITE-LD:BEGIN（由 tools/build-module-pages.py 依 _pages.json 產生）-->', '<!-- SITE-LD:END -->'
LOGO_H1_RE = re.compile(r'<h1>(\s*<a href="(?:\.\./)?index\.html">\s*<img[^>]*>\s*</a>\s*)</h1>', re.S)
BLOG_BANNER_RE = re.compile(r'<h1 style="color:#d9e0e7;">新聞中心</h1>')


def strip_comments(s):
    return re.sub(r'<!--.*?-->', '', s, flags=re.S)


def static_ld(rel, cfg, s):
    url = SITE + '/' + ('' if rel == 'index.html' else rel)
    title = html.unescape(re.search(r'<title>(.*?)</title>', s, re.S).group(1).strip())
    desc = html.unescape((re.search(r'<meta name="description" content="([^"]*)"', s) or [None, ''])[1])
    page = {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': title, 'description': desc,
            'inLanguage': 'zh-Hant-TW', 'isPartOf': {'@type': 'WebSite', '@id': SITE + '/#website', 'name': '奧洛 Aurobase', 'url': SITE + '/'},
            'publisher': {'@id': ORG['@id']}}
    graph = [page, ORG]
    if rel == 'index.html':
        graph.append(WEBSITE)
    if cfg.get('faq'):
        graph.append({'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
            {'@type': 'Question', 'name': f['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in cfg['faq']]})
    page['primaryImageOfPage'] = {'@type': 'ImageObject', 'url': '%s/%s' % (SITE, og_image(og_key(rel))), 'width': OG_W, 'height': OG_H}
    if cfg.get('keywords'):
        page['keywords'] = ', '.join(cfg['keywords'])
    t = cfg.get('type', 'WebPage')
    if t == 'ContactPage':
        page['@type'] = 'ContactPage'
        page['about'] = {'@id': ORG['@id']}
    elif t == 'Service':
        graph.append({'@type': 'Service', 'name': cfg['name'], 'serviceType': cfg.get('service_type', cfg['name']),
                      'description': desc, 'provider': {'@id': ORG['@id']}, 'areaServed': {'@type': 'Country', 'name': '台灣'},
                      'url': url, **({'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': cfg['name'], 'itemListElement': [
                          {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': x}} for x in cfg['items']]}} if cfg.get('items') else {})})
    elif t == 'ItemList':
        graph.append({'@type': 'ItemList', 'name': cfg['name'], 'itemListElement': [
            {'@type': 'ListItem', 'position': i, 'name': x} for i, x in enumerate(cfg['items'], 1)]})
    elif t == 'Blog':
        posts = []
        for r, c in sorted(load_pages_cfg().items()):
            if c.get('type') == 'BlogPosting' and os.path.exists(os.path.join(ROOT, r)):
                ps = read(os.path.join(ROOT, r))
                posts.append({'@type': 'BlogPosting', 'headline': re.sub(r'｜.*$', '', html.unescape(re.search(r'<title>(.*?)</title>', ps, re.S).group(1).strip())),
                              'url': SITE + '/' + r, 'datePublished': c['date']})
        graph.append({'@type': 'Blog', '@id': url + '#blog', 'name': cfg['name'], 'url': url, 'publisher': {'@id': ORG['@id']}, 'blogPost': posts})
    elif t == 'BlogPosting':
        cat = re.search(r'<a class="color-orange">([^<]+)</a>', s)
        graph.append({'@type': 'BlogPosting', '@id': url + '#article', 'headline': re.sub(r'｜.*$', '', title), 'description': desc,
                      'datePublished': cfg['date'], 'dateModified': cfg.get('modified', cfg['date']), 'inLanguage': 'zh-Hant-TW',
                      'mainEntityOfPage': {'@id': url + '#webpage'}, 'author': {'@id': ORG['@id']}, 'publisher': {'@id': ORG['@id']},
                      'image': page['primaryImageOfPage'], 'isPartOf': {'@id': SITE + '/blog.html#blog'},
                      **({'articleSection': cat.group(1).strip()} if cat else {}),
                      **({'keywords': ', '.join(cfg['keywords'])} if cfg.get('keywords') else {})})
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=2)


REL_BEGIN, REL_END = '<!-- RELATED:BEGIN（由 tools/build-module-pages.py 依 _pages.json 產生）-->', '<!-- RELATED:END -->'
FAQ_BEGIN, FAQ_END = '<!-- PAGE-FAQ:BEGIN（由 tools/build-module-pages.py 依 _pages.json 產生）-->', '<!-- PAGE-FAQ:END -->'
SOCIAL_BEGIN, SOCIAL_END = '<!-- SOCIAL-META:BEGIN（由 tools/build-module-pages.py 產生）-->', '<!-- SOCIAL-META:END -->'
SOCIAL_STRIP = re.compile(r'[ \t]*<meta (?:property="og:(?:image[^"]*|locale|type)"|name="(?:twitter:[^"]*|robots|theme-color|article-[^"]*)"|property="article:[^"]*")[^>]*>\n?')


def apply_social(t, rel, image, og_type='website', date=None, modified=None):
    """手寫頁面的社群與搜尋 meta：分享圖、Twitter 卡片、語系、大圖預覽，集中在一個區塊由產生器維護。"""
    title = html.unescape(re.search(r'<title>(.*?)</title>', t, re.S).group(1).strip())
    desc = html.unescape((re.search(r'<meta name="description" content="([^"]*)"', t) or [None, ''])[1])
    url = SITE + '/' + ('' if rel == 'index.html' else rel)
    lines = ['<meta property="og:type" content="%s">' % og_type,
             '<meta property="og:locale" content="zh_TW">',
             '<meta property="og:image" content="%s/%s">' % (SITE, image),
             '<meta property="og:image:width" content="%d">' % OG_W,
             '<meta property="og:image:height" content="%d">' % OG_H,
             '<meta property="og:image:alt" content="%s">' % attr(re.sub(r'｜.*$', '', title)),
             '<meta name="twitter:card" content="summary_large_image">',
             '<meta name="twitter:title" content="%s">' % attr(title),
             '<meta name="twitter:description" content="%s">' % attr(desc),
             '<meta name="twitter:image" content="%s/%s">' % (SITE, image),
             '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
             '<link rel="alternate" hreflang="zh-Hant-TW" href="%s">' % url]
    if og_type == 'article':
        lines += ['<meta property="article:published_time" content="%s">' % date,
                  '<meta property="article:modified_time" content="%s">' % (modified or date),
                  '<meta property="article:author" content="奧洛 Aurobase">']
    block = SOCIAL_BEGIN + '\n    ' + '\n    '.join(lines) + '\n    ' + SOCIAL_END
    if SOCIAL_BEGIN in t:
        return t[:t.index(SOCIAL_BEGIN)] + block + t[t.index(SOCIAL_END) + len(SOCIAL_END):]
    t = SOCIAL_STRIP.sub('', t)
    t = re.sub(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', t)
    return re.sub(r'(<link rel="canonical" href="[^"]*">)', lambda x: x.group(1) + '\n    ' + block, t, count=1)


def load_pages_cfg():
    p = os.path.join(SRC, '_pages.json')
    return json.loads(read(p))['pages'] if os.path.exists(p) else {}


def update_static_pages():
    changed = []
    for rel, cfg in load_pages_cfg().items():
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        s = read(p)
        t = s
        if cfg.get('description'):
            d = attr(cfg['description'])
            t = re.sub(r'(<meta name="description" content=")[^"]*', lambda x: x.group(1) + d, t, count=1)
            t = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda x: x.group(1) + d, t, count=1)
        if cfg.get('title'):
            ti = html.escape(cfg['title'], quote=False)
            t = re.sub(r'<title>.*?</title>', lambda x: '<title>%s</title>' % ti, t, count=1, flags=re.S)
            t = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda x: x.group(1) + attr(cfg['title']), t, count=1)
        if cfg.get('keywords'):
            kw = attr(','.join(cfg['keywords']))
            t = re.sub(r'(<meta name="keywords" content=")[^"]*', lambda x: x.group(1) + kw, t, count=1)
        if cfg.get('type') == 'BlogPosting':
            t = apply_social(t, rel, og_image(og_key(rel)), 'article', cfg['date'], cfg.get('modified'))
        else:
            t = apply_social(t, rel, og_image(og_key(rel)))
        # 舊版手寫的 Organization／Article 結構化資料與產生的版本重複，拿掉
        t = re.sub(r'[ \t]*<script type="application/ld\+json">\s*\{\s*"@context": "https://schema\.org",\s*"@type": "(?:Organization|Article)".*?</script>\n?', '', t, flags=re.S)
        t = LOGO_H1_RE.sub(lambda x: '<div class="aside-logo">%s</div>' % x.group(1), t)
        t = BLOG_BANNER_RE.sub('<p class="h1" style="color:#d9e0e7;">新聞中心</p>', t)
        # 標誌不再是 H1 後，沒有 H1 的頁面把橫幅標題升為 H1（加 .h2 / .h3 保留原本大小）
        if not re.search(r'<h1[\s>]', strip_comments(t)):
            t, n = re.subn(r'<h2 style="color:#d9e0e7;">(.*?)</h2>', r'<h1 class="h2" style="color:#d9e0e7;">\1</h1>', t, count=1)
            if not n:
                t = re.sub(r'<h3 (style="color:#28282c; text-indent: 0\.35em;")>(.*?)</h3>', r'<h1 class="h3" \1>\2</h1>', t, count=1)
        if cfg.get('type') == 'BlogPosting':
            alt = attr(re.sub(r'｜.*$', '', re.search(r'<title>(.*?)</title>', t, re.S).group(1)))
            t = re.sub(r'(<img loading="lazy" src="\.\./images/[^"]+") alt=""', lambda x: '%s alt="%s"' % (x.group(1), alt), t)
        if cfg.get('related'):
            links = ''.join('<li><a href="../%s">%s</a></li>' % (attr(x['url']), html.escape(x['label'])) for x in cfg['related'])
            rb = (REL_BEGIN + '\n<aside class="pg-related" aria-label="延伸閱讀"><h2>延伸閱讀</h2><ul>%s</ul></aside>\n' % links + REL_END)
            if REL_BEGIN in t:
                t = t[:t.index(REL_BEGIN)] + rb + t[t.index(REL_END) + len(REL_END):]
            else:
                t = t.replace('<!-- <div class="tag-widget post-tag-container', rb + '\n<!-- <div class="tag-widget post-tag-container', 1)
        if cfg.get('faq'):
            items = ''.join('<div class="pg-faq-item"><h3>%s</h3><p>%s</p></div>' % (html.escape(f['q']), html.escape(f['a'])) for f in cfg['faq'])
            fb = (FAQ_BEGIN + '\n<section id="faq" class="ftco-section pg-faq"><div class="row justify-content-end"><div class="col-md-10">'
                  '<div class="pg-faq-wrap"><p class="pg-faq-label">FAQ</p><h2>常見問題</h2>%s</div></div></div></section>\n' % items + FAQ_END)
            if FAQ_BEGIN in t:
                t = t[:t.index(FAQ_BEGIN)] + fb + t[t.index(FAQ_END) + len(FAQ_END):]
            else:
                t = re.sub(r'([ \t]*<footer id="footer-sec")', lambda x: fb + '\n' + x.group(1), t, count=1)
        block = LD_BEGIN + '\n    <script type="application/ld+json">\n' + static_ld(rel, cfg, t) + '\n</script>\n    ' + LD_END
        if LD_BEGIN in t:
            t = t[:t.index(LD_BEGIN)] + block + t[t.index(LD_END) + len(LD_END):]
        else:
            t = t.replace('</head>', '    %s\n  </head>' % block, 1)
        if t != s:
            io.open(p, 'w', encoding='utf-8').write(t)
            changed.append(rel)
    return changed


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
    nav_changed = update_nav(mods, pf) + update_static_pages()
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
    update_search_index(mods, pf)
    update_llms_full(mods, pf)
    update_home(mods, pf)
    written += ['nexus.html', 'llms.txt', 'sitemap.xml', SEARCH_INDEX, LLMS_FULL] + [f for f in nav_changed if f not in written]
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
                    # 選單空間有限：拿掉「NEXUS 」前綴（ABM、GEO、AI-Office），頁面本身的名稱不變
                    links = ''.join('<a href="%s%s"%s>%s</a>' % (prefix, get(s)['file'], cur(get(s)['file']), re.sub(r'^NEXUS ', '', get(s)['code'])) for s in slugs)
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
    search = ('<button type="button" class="nav-search-btn" aria-haspopup="dialog">'
              '<span aria-hidden="true">⌕</span> 搜尋產品與服務</button>'
              '<script defer src="%sjs/site-search.js"></script>' % prefix)
    return NAV_BEGIN + '\n' + search + ''.join(out) + '\n' + NAV_TOGGLE_JS + '\n' + NAV_END


def nav_pages():
    pages = sorted(glob.glob(os.path.join(ROOT, '*.html'))) + sorted(glob.glob(os.path.join(ROOT, 'blogpost', '*.html')))
    return [p for p in pages if os.path.basename(p) not in NOT_INDEXED] + [os.path.join(SRC, 'chrome-top.html')]


CJK_PRELOAD_RE = re.compile(r'[ \t]*<link rel="preload" href="[./]*WOFF2/LINESeedTW_OTF_(?:Rg|Bd)\.subset\.woff2"[^>]*>\n?')
LOADER_RE = re.compile(r'[ \t]*(?:<!-- loader -->\s*)?<div id="ftco-loader"[^>]*>.*?</svg>\s*</div>\n?', re.S)


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
        # 全螢幕載入轉圈：內容本來就在 HTML 裡，轉圈只會讓訪客多等到所有程式載完才看得到頁面
        t = LOADER_RE.sub('', t)
        # 中文字型子集約 300 KB：預先載入會和畫面需要的 CSS 搶頻寬，首次繪製在慢速網路慢 1 秒以上；
        # 字型已設 font-display: swap，不預載也會先用系統字顯示、載到再換
        t = CJK_PRELOAD_RE.sub('', t)
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
