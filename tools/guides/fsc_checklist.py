"""PDF 檢核表：金融業運用 AI 指引落實檢核表（網站訪客留 Email 後下載）。

內容不另寫：匯入 fsc_ai_guideline.py 的六章重點、總則與平台對應，和網頁同一份來源，改指引頁內容後重跑本檔即同步。
版型用 company-report skill（奧洛母版）。

    python3 tools/guides/fsc_checklist.py          # 產生 HTML 並輸出 downloads/fsc-ai-guideline-checklist.pdf
"""
import os, re, sys, shutil, subprocess, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fsc_ai_guideline as G
from guidekit import ROOT

SKILL = os.path.expanduser('~/.claude/skills/company-report')
WORK = os.path.join(ROOT, 'tools', 'guides', 'fsc-checklist')
OUT = os.path.join(ROOT, 'downloads', 'fsc-ai-guideline-checklist.pdf')
VERSION, DATE = 'v1.0', '2026 年 11 月 23 日'
TITLE = '金融業運用 AI 指引落實檢核表'


def plain(x):
    return re.sub(r'<[^>]+>', '', x)


def items_of(block_html):
    """從總則的 gd-block 取出 (標題, [項目])。"""
    return [(plain(h), [plain(li) for li in re.findall(r'<li>(.*?)</li>', ul)])
            for h, ul in re.findall(r'<h3>(.*?)</h3><ul>(.*?)</ul>', block_html)]


STATUS = '<span class="cb">已落實</span> <span class="cb">進行中</span> <span class="cb">未開始</span>'


def check_table(caption, rows, n0=1):
    body = ''.join('<tr><td class="ref">%02d</td><td>%s</td><td class="st">%s</td><td></td></tr>' % (n0 + i, H.escape(r), STATUS)
                   for i, r in enumerate(rows))
    return ('<table class="data chk"><caption>%s</caption><thead><tr><th style="width:9mm">#</th><th>檢核項目</th>'
            '<th style="width:52mm">現況</th><th style="width:34mm">佐證紀錄／負責人</th></tr></thead><tbody>%s</tbody></table>' % (caption, body))


def page():
    general = dict(items_of(G.general))
    factors = general['風險評估六項考量因素']
    strong = general['高風險系統的加強措施']
    outsource = general['委託第三方業者']
    steps = [plain(x) for x in re.findall(r'<li>(.*?)</li>', G.answer)]

    toc = [('s01', '01', '從哪裡開始'), ('s02', '02', '總則：先分級，再決定控管程度'), ('s03', '03', '六章檢核')]
    toc += [('s04', '04', '委託第三方業者'), ('s05', '05', 'AURO NEXUS 能協助的部分'), ('sA', 'A', '附錄：出處')]
    toc_html = ''.join('<li%s><span class="num">%s</span><span class="t"><a href="#%s">%s</a></span><span class="pg" data-for="%s"></span></li>'
                       % ('' if n else ' class="sub"', n, i, t, i) for i, n, t in toc)

    chap = []
    for i, (no, name, groups) in enumerate(G.chapters, 1):
        g = dict(groups)
        chap.append('<div class="keep"><h3 id="s03-%d">%s　%s</h3>' % (i, no, name)
                    + check_table('<b>表 %d</b>　%s：指引重點' % (i + 2, no), g['指引重點'])
                    + '<p class="small"><b>落實做法參考：</b>%s　<b>應留下的紀錄：</b>%s</p></div>'
                    % ('；'.join(g['落實做法']), '；'.join(g['該留下的紀錄'])))

    platform = ''.join('<tr><td>%s</td><td>%s</td><td class="key">%s</td></tr>' % (plain(a), plain(b), plain(c)) for a, b, c in G.rows)
    tier = ''.join('<tr><td class="ref">%02d</td><td>%s</td><td class="st"><span class="cb">高</span> <span class="cb">中</span> <span class="cb">低</span></td><td></td></tr>'
                   % (i, H.escape(f)) for i, f in enumerate(factors, 1))

    return f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE} {VERSION}</title>
<meta name="author" content="奧洛股份有限公司">
<link rel="stylesheet" href="{SKILL}/brand/report.css">
<style>
  /* 字型讀 repo 內的宙黑體完整檔（tools/fonts/）。品牌樣式表 report.css 指定的是舊字族名稱，
     這裡把那幾個名稱都指到宙黑體，PDF 才會跟網站同一套字。 */
  @font-face {{ font-family: 'Zev Hei TC'; font-weight: 300 900; src: url('file://{ROOT}/tools/fonts/ZevHeiTC-F-VF.woff2') format('woff2'); }}
  @font-face {{ font-family: 'LINE Seed TW'; font-weight: 300 900; src: url('file://{ROOT}/tools/fonts/ZevHeiTC-F-VF.woff2') format('woff2'); }}
  @font-face {{ font-family: 'LINE Seed Sans'; font-weight: 300 900; src: url('file://{ROOT}/tools/fonts/ZevHeiTC-F-VF.woff2') format('woff2'); }}
  html {{ --doc-title: '{TITLE} {VERSION}'; --doc-confidential: '公開文件'; }}
  table.chk td.st {{ white-space: nowrap; }}
  table.chk td.st .cb + .cb {{ margin-left: 2.4mm; }}
  table.chk td {{ vertical-align: top; }}
  p.small {{ font-size: 9pt; line-height: 1.7; color: #555; margin-top: 2mm; }}
  nav.toc li.sub .t {{ padding-left: 6mm; font-size: .95em; }}
</style>
</head>
<body>

<section class="cover">
  <img class="logo" src="{SKILL}/brand/logo.svg" alt="奧洛 Aurobase">
  <div class="doc-kind">// 檢核表　CHECKLIST</div>
  <h1>金融業運用 AI 指引<br>落實檢核表</h1>
  <p class="subtitle">依金管會〈金融業運用人工智慧（AI）指引〉原文整理：先分級，再逐章檢核控制措施與應留下的紀錄</p>
  <div class="rule"></div>
  <dl class="meta">
    <dt>依據</dt><dd>金管會，113 年 6 月 20 日發布（行政指導）</dd>
    <dt>文件版本</dt><dd>{VERSION}</dd>
    <dt>發行日期</dt><dd>{DATE}</dd>
    <dt>機密等級</dt><dd>公開文件</dd>
  </dl>
  <div class="band">
    <div class="wordmark">AUROBASE<small>奧洛股份有限公司　·　台北市內湖區洲子街101號2樓　·　+886-2-5568-4688</small></div>
    <div class="conf">PUBLIC</div>
  </div>
</section>

<h2 class="plain">文件資訊</h2>
<table class="kv">
  <tr><th>文件名稱</th><td>{TITLE}</td></tr>
  <tr><th>撰寫單位</th><td>奧洛股份有限公司</td></tr>
  <tr><th>線上版本</th><td>aurobase.com/fsc-ai-guideline.html（內容與本檢核表同一來源）</td></tr>
  <tr><th>使用方式</th><td>每一列勾選現況，並在右欄寫下佐證紀錄的位置或負責人。條文以金管會公布的版本為準。</td></tr>
  <tr><th>聯絡方式</th><td>+886-2-5568-4688　·　ad@aurocore.com</td></tr>
</table>

<h3>修訂紀錄</h3>
<table class="data">
  <thead><tr><th style="width:16mm">版本</th><th style="width:28mm">日期</th><th>修訂內容</th></tr></thead>
  <tbody><tr><td class="ref">{VERSION}</td><td class="ref">2026-11-23</td><td>首次發行</td></tr></tbody>
</table>

<h2 class="plain" style="margin-top:9mm">目次</h2>
<nav class="toc"><ol>{toc_html}</ol></nav>

<div class="page-break">
<h2 class="plain">摘要</h2>
<p class="lead">{plain(re.search(r'<p>(.*?)</p>', G.answer).group(1))}</p>
<div class="stats">
  <div class="stat"><div class="n">6</div><div class="l">項風險評估因素，用來替每個 AI 系統分級</div></div>
  <div class="stat"><div class="n">{sum(len(dict(c[2])['指引重點']) for c in G.chapters)}</div><div class="l">項六章檢核項目，各附應留下的紀錄</div></div>
  <div class="stat"><div class="n"><em>{len(outsource)}</em></div><div class="l">項委外檢核，採購與續約前逐項確認</div></div>
</div>
<div class="callout">
  <span class="label">本檢核表的定位</span>
  <p>本表依指引原文整理並改寫，標示「實務建議」的內容為奧洛的建議做法。是否符合指引，由主管機關與貴機構法遵認定。</p>
</div>
</div>

<div class="page-break">
<h2 class="sec" id="s01"><span class="num">01</span><span class="t">從哪裡開始</span></h2>
<p class="lead">實務建議：依下列順序進行，前一步的產出就是下一步的輸入。</p>
<div class="flow">{''.join('<div class="step%s"><b>%d</b>%s</div>' % (' hot' if i == 1 else '', i, H.escape(s)) for i, s in enumerate(steps, 1))}</div>
</div>

<h2 class="sec" id="s02"><span class="num">02</span><span class="t">總則：先分級，再決定控管程度</span></h2>
<p>每一個 AI 系統依下列六項因素評估；風險高低由貴機構綜合判斷，指引所舉例子僅供說明，不是分級規範。AI 系統生命週期分為{('、'.join(general['AI 系統生命週期四階段']))}四個階段，各階段都適用下列控管。</p>
<table class="data chk"><caption><b>表 1</b>　風險評估六項考量因素（每個 AI 系統填一份）</caption>
<thead><tr><th style="width:9mm">#</th><th>考量因素</th><th style="width:40mm">評估</th><th style="width:46mm">說明</th></tr></thead><tbody>{tier}</tbody></table>
<div class="keep">{check_table('<b>表 2</b>　評為高風險的系統：加強措施', strong)}</div>

<div>
<h2 class="sec" id="s03"><span class="num">03</span><span class="t">六章檢核</span></h2>
<p class="lead">每一章列出指引重點，下方附落實做法參考與應留下的紀錄。</p>
{''.join(chap)}
</div>

<div class="keep"><h2 class="sec" id="s04"><span class="num">04</span><span class="t">委託第三方業者</span></h2>
<p>使用外部模型、雲端服務或委外開發時，採購與續約前逐項確認。</p>
{check_table('<b>表 9</b>　委外與採購檢核', outsource)}</div>

<div>
<h2 class="sec" id="s05"><span class="num">05</span><span class="t">AURO NEXUS 能協助的部分</span></h2>
<p>下表是奧洛 AURO NEXUS 平台提供的控管措施與對應的指引章節。AI 治理架構與負責主管、公平性評估方法、對客戶的揭露內容、替代方案與員工培訓，由貴機構依自身情況決定；平台提供的是控管措施的執行與紀錄。</p>
<table class="data"><caption><b>表 10</b>　平台能力與指引對應</caption>
<thead><tr><th>平台能力</th><th style="width:58mm">對應指引</th><th style="width:26mm">模組</th></tr></thead><tbody>{platform}</tbody></table>
<div class="callout brand">
  <span class="label">想在您的環境裡驗證</span>
  <p>告訴我們目前怎麼使用 AI、資料放在哪裡，以及法遵或稽核最在意的項目，業務會安排一場線上簡報或需求訪談。<br>+886-2-5568-4688　·　ad@aurocore.com　·　aurobase.com/nexus.html</p>
</div>
</div>

<h2 class="sec" id="sA"><span class="num">A</span><span class="t">附錄：出處</span></h2>
<ol>
  <li>金融監督管理委員會，〈金融業運用人工智慧(AI)指引〉，113 年 6 月 20 日，金管會主管法規共用系統（law.fsc.gov.tw，法規編號 GL003920）。</li>
  <li>金融監督管理委員會新聞稿，〈金管會發布「金融業運用人工智慧(AI)指引」〉，113 年 6 月 20 日，金管會全球資訊網。</li>
</ol>
<p class="small">本文件結束</p>
</body>
</html>
'''


if __name__ == '__main__':
    os.makedirs(WORK, exist_ok=True)
    src = os.path.join(WORK, 'fsc-ai-guideline-checklist.html')
    open(src, 'w', encoding='utf-8').write(page())
    # 使用者自己的 Chrome 開著時，headless Chrome 共用同一個設定檔會卡住不出 PDF：包一層指定獨立的 --user-data-dir
    import tempfile
    tmp = tempfile.mkdtemp()
    wrapper = os.path.join(tmp, 'chrome')
    open(wrapper, 'w').write('#!/bin/sh\nexec "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --user-data-dir="%s/profile" "$@"\n' % tmp)
    os.chmod(wrapper, 0o755)
    subprocess.run([os.path.join(SKILL, 'scripts', 'build.sh'), src], check=True, env=dict(os.environ, CHROME=wrapper))
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copy(src[:-5] + '.pdf', OUT)
    print('wrote', os.path.relpath(OUT, ROOT))
