#!/usr/bin/env python3
"""把 tools/module-pages/*.json 匯出成一份 Markdown 文案總表，給非工程人員逐字審閱。

    python3 tools/export-module-copy.py <輸出路徑.md>
"""
import io
import json
import os
import re
import sys

SRC = os.path.join(os.path.dirname(__file__), 'module-pages')
ORDER = ['nexus-forge', 'nexus-auro', 'nexus-cdp', 'nexus-abm', 'nexus-insight', 'nexus-library',
         'nexus-mira', 'nexus-pulse', 'nexus-ai-office', 'nexus-lisa', 'nexus-scanner', 'nexus-cardea']


def t(s):
    return re.sub(r'<br\s*/?>', ' / ', re.sub(r'<(?!br)[^>]+>', '', s))


def load(name):
    return json.load(io.open(os.path.join(SRC, name), encoding='utf-8'))


def platform(out):
    pf = load('_platform.json')
    out += ['## AURO NEXUS 平台總覽（nexus.html 上方新增區塊）', '',
            f"**頁面標題**：{pf['title']}  ", f"**搜尋摘要**：{t(pf['description'])}", '',
            f"**H1**：{t(pf['h1'])}  ", f"**主張**：{t(pf['slogan'])}  ", f"**副標**：{t(pf['sub'])}  ",
            f"**引言**：{t(pf['tagline'])}", '', f"**定義區｜{pf['definition']['q']}**", '']
    out += [t(x) + '\n' for x in pf['definition']['a']]
    out += ['**能力架構**', ''] + [f"- {lg['name']}：{lg['text']}（{'、'.join(lg['modules'])}）" for lg in pf['legs']]
    out += ['', f"**{pf['needs']['heading']}**", '', t(pf['needs']['intro']), '']
    out += [f"- {need} → {slug}" for need, slug in pf['needs']['rows']]
    out += ['', '**平台的三個承諾**', ''] + [f"- {d['title']}：{t(d['text'])}" for d in pf['diff']]
    out += ['', '**常見問題**', ''] + [f"- Q：{t(f['q'])}  \n  A：{t(f['a'])}" for f in pf['faq']]
    out += ['', '---', '']


def module(out, m):
    h = m['hero']
    name = m['name_zh'] if m['code'] == m['name_zh'] else f"{m['code']} {m['name_zh']}"
    out += [f"## {name}（{m.get('industry') or m['leg']}）", f"網址：{m['file']}", '',
            f"**頁面標題**：{m['title']}  ", f"**搜尋摘要**：{t(m['description'])}  ",
            f"**目標關鍵字**：{'、'.join(k for k in m['keywords'] if k != 'AURO NEXUS')}", '',
            f"**H1**：{t(h['h1'])}  ", f"**主張**：{t(h['slogan'])}  ", f"**副標**：{t(h['sub'])}  ",
            f"**引言**：{t(h['tagline'])}", '', '**重點摘要**', '']
    out += [f"- {k}：{t(v)}" for k, v in m['summary']]
    d = m['definition']
    out += ['', f"**定義區｜{d['q']}**", ''] + [t(x) + '\n' for x in d['a']]
    if m.get('flow'):
        out += [f"**運作流程｜{m.get('flow_heading', '運作流程')}**", '']
        out += [f"{i}. {st['title']}：{t(st.get('text', ''))}（{'、'.join(st.get('modules') or [])}）" for i, st in enumerate(m['flow'], 1)]
        out.append('')
    out += ['**適合誰**', ''] + [f"- {a['who']}：{a['why']}" for a in m['audience']]
    p = m['pain']
    out += ['', f"**問題｜{t(p['heading'])}**", ''] + ([t(p['intro']), ''] if p.get('intro') else [])
    out += [f"{i}. {c['title']}：{t(c['text'])}" for i, c in enumerate(p['cards'], 1)] + ['', f"> {t(p['statement'])}"]
    c = m['capabilities']
    out += ['', f"**核心能力｜{t(c['heading'])}**", ''] + ([t(c['intro']), ''] if c.get('intro') else [])
    out += [f"- {cd['title']}：" + '；'.join(t(x) for x in cd['items']) for cd in c['cards']]
    if m.get('regulation'):
        r = m['regulation']
        out += ['', f"**法規對照｜{r['heading']}**", '', t(r['intro']), '',
                f"| {r['cols'][0]} | {r['cols'][1]} |", '|---|---|']
        out += [f"| {a} | {t(b)} |" for a, b in r['rows']]
        out += ['', f"資料來源：{'；'.join(x['name'] for x in r['sources'])}。{r.get('note', '')}"]
    if m.get('compare'):
        cp = m['compare']
        out += ['', f"**比較表｜{cp['heading']}**", '', '| | ' + ' | '.join(cp['cols']) + ' |',
                '|' + '---|' * (len(cp['cols']) + 1)]
        out += ['| ' + ' | '.join(t(x) for x in row) + ' |' for row in cp['rows']]
    out += ['', '**差異點**', ''] + [f"- {x['title']}：{t(x['text'])}" for x in m['diff']['cards']]
    out += ['', f"**平台位置**：{t(m['platform']['text'])}", '', '**部署形態**', '']
    out += [f"- {x['tag']}｜{x['title']}：{t(x['text'])}" for x in m['deploy']]
    if m.get('limits'):
        out += ['', '**範圍界定**', ''] + [f"- {x['title']}：{t(x['text'])}" for x in m['limits']]
    out += ['', '**常見問題**', ''] + [f"- Q：{t(f['q'])}  \n  A：{t(f['a'])}" for f in m['faq']]
    out += ['', f"**結尾**：{t(m['cta']['heading'])}——{t(m['cta']['text'])}", '', '---', '']


def main():
    dst = sys.argv[1]
    out = ['# AURO NEXUS 平台與模組頁文案總表', '',
           '> 由 tools/module-pages/*.json 匯出。要改哪一頁哪一段，直接標出來。', '']
    platform(out)
    for slug in ORDER:
        module(out, load(slug + '.json'))
    out += ['# 產業解決方案', '']
    for p in sorted(os.listdir(SRC)):
        if p.startswith('solution-') and p.endswith('.json'):
            module(out, load(p))
    io.open(dst, 'w', encoding='utf-8').write('\n'.join(out))
    print('wrote', dst)


if __name__ == '__main__':
    main()
