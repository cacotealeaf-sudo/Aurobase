"""新聞稿：奧洛 Aurobase 推出 AURO NEXUS AI 治理平台（press-auro-nexus.html）。
不放進選單、首頁、新聞中心與站內搜尋；只列在 sitemap 與 llms.txt，讓搜尋引擎與 AI 找得到，也可直接把網址或檔案寄給媒體與合作夥伴。
內容只用網站上已公開的事實。發稿日改 DATE／DATE_ZH，並同步 _pages.json 的 date。
改完跑 python3 tools/guides/press_auro_nexus.py，再跑 tools/build-module-pages.py。"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guidekit import build, section

DATE_ZH = '2026 年 11 月 22 日'

body = '''    <div class="gd-answer">
      <p>【%s，台北】奧洛 Aurobase（奧洛股份有限公司）推出 <a href="nexus.html">AURO NEXUS</a> AI 治理平台。平台以 <a href="nexus-forge.html">Forge</a> 為治理底座，串起 AI Agent、客戶數據平台、企業知識庫、AI 內容產製、源碼檢測與 SSL 憑證管理等 14 個模組。各模組的 AI 呼叫在送往模型之前，先完成權限與政策檢查；模型可以限定只用地端；每一次呼叫都寫入雜湊鏈稽核軌跡，證據包附獨立驗證工具，稽核人員不需要連上平台就能查驗。</p>
      <p>金管會於 113 年 6 月 20 日發布〈金融業運用人工智慧（AI）指引〉，屬行政指導性質，以治理及問責、保護隱私及客戶權益、系統穩健與安全、透明及可解釋等六項原則為架構。指引第三章指出，在沒有適當管控機制的情況下，金融機構人員不得向生成式 AI 提供未經客戶同意提供的資訊；適當的管控機制例如採用封閉型部署的模型。</p>
      <p>企業各部門各自採購、各自串接 AI 工具時，資訊、資安與法遵單位很難掌握每一次 AI 使用的權限、資料與核准紀錄。AURO NEXUS 讓這些 AI 使用經過同一個入口：不符合政策的請求不會到達模型，含個人資料的請求可以只送往地端模型，事後可以逐筆查驗。</p>
    </div>''' % DATE_ZH

points = '''    <div class="gd-cols">
      <div class="gd-block"><h3>先檢查，再推論</h3><ul><li>AI 請求在送往模型之前就完成權限與政策檢查</li><li>不符合政策的請求不會到達模型</li></ul></div>
      <div class="gd-block"><h3>證據可以離線驗證</h3><ul><li>稽核軌跡以雜湊鏈保護</li><li>證據包附獨立驗證工具，稽核人員不需要連上平台就能查驗</li></ul></div>
      <div class="gd-block"><h3>雲端與地端用同一套</h3><ul><li>公有雲台灣區域、企業自有機房或隔離網路，使用相同的權限、模型路由與稽核軌跡</li><li>日後搬移不需要重新導入</li></ul></div>
    </div>
    <p class="gd-note" style="margin-top:24px">企業不需要一次導入全部模組，可以從最急的需求開始，例如先以 Forge 統一管理企業內的 AI 使用；之後新增的模組共用同一個治理底座。資料處理方式見<a href="security.html">資安與資料處理</a>。</p>'''

legs = [
    ('治理底座', '所有 AI 呼叫的必經入口與稽核軌跡', [('Forge', 'nexus-forge.html')]),
    ('AI 編排', '有預算、有閘門、可人工審核的 AI Agent', [('Auro', 'nexus-auro.html')]),
    ('客戶資料', '身分解析、單一客戶視圖與 B2B 帳號經營', [('AURA CDP', 'nexus-cdp.html'), ('NEXUS ABM', 'nexus-abm.html')]),
    ('知識', '可追溯出處的企業知識庫與個人收藏', [('Insight', 'nexus-insight.html'), ('Library', 'nexus-library.html')]),
    ('內容與行銷智能', '受監理產業的內容產製、輿情分析與 AI 搜尋能見度', [('MIRA', 'nexus-mira.html'), ('Pulse', 'nexus-pulse.html'), ('NEXUS GEO', 'nexus-geo.html')]),
    ('合規治理', '非結構化資料的分級、保存與稽核', [('SAGA', 'nexus-saga.html')]),
    ('生產力', '依範本產出提案書、報價單與週報', [('NEXUS AI-Office', 'nexus-ai-office.html')]),
    ('現代化', '讀懂大型主機程式，產出繁體中文規格書', [('LISA', 'nexus-lisa.html')]),
    ('安全', '源碼檢測、弱點掃描與 SSL 憑證管理', [('Scanner', 'nexus-scanner.html'), ('Cardea', 'nexus-cardea.html')]),
]
module_table = ('    <table class="gd-table"><thead><tr><th>能力</th><th>做什麼</th><th>模組</th></tr></thead><tbody>'
                + ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (n, t, '、'.join('<a href="%s">%s</a>' % (f, n) for n, f in ms))
                          for n, t, ms in legs) + '</tbody></table>'
                '\n    <p class="gd-note" style="margin-top:24px">產業解決方案由平台模組組成：公部門的<a href="solution-police-record.html">警詢筆錄 AI 輔助</a>、'
                '金融保險的<a href="solution-telesales.html">電話與視訊銷售對話智能</a>、社福長照的<a href="ai-companion.html">AI 智慧語伴</a>，'
                '以及跨產業的<a href="solution-ai-ocr.html">AI OCR 智慧文件辨識</a>。</p>')

deploy = '''    <div class="gd-cols">
      <div class="gd-block"><h3>公有雲台灣區域</h3><ul><li>部署於公有雲台灣區域的 Kubernetes，資料留在台灣</li><li>適合要快速上線的企業</li></ul></div>
      <div class="gd-block"><h3>企業自有機房或隔離網路</h3><ul><li>平台與模型都在企業環境內，模型可限定只用地端</li><li>適合金融與受監理產業</li></ul></div>
      <div class="gd-block"><h3>依流程客製</h3><ul><li>模組可組合成專案方案</li><li>權限規則、審核流程與既有系統介接，由奧洛工程團隊依需求開發</li></ul></div>
    </div>'''

about = '''    <div class="gd-answer">
      <p><b>關於奧洛 Aurobase</b></p>
      <p>奧洛 Aurobase（奧洛股份有限公司）位於台北內湖，自有產品 AURO NEXUS 是可部署於企業自有機房的 AI 治理平台，協助金融與受監理產業在自有環境導入生成式 AI。奧洛也代理 HCL Discover、HCL Unica、Magnolia CMS 等行銷科技產品，並提供 Google、Meta、LINE 廣告投放與社群經營服務。事業夥伴包括 Google、Meta、LINE、HCL Software、Magnolia、精誠資訊與零壹科技。網站：<a href="index.html">aurobase.com</a></p>
    </div>
    <table class="gd-table" style="margin-top:24px"><tbody>
      <tr><td>媒體聯絡</td><td>奧洛 Aurobase</td></tr>
      <tr><td>電話</td><td><a href="tel:+886-2-5568-4688">+886-2-5568-4688</a></td></tr>
      <tr><td>Email</td><td><a href="mailto:ad@aurocore.com">ad@aurocore.com</a></td></tr>
      <tr><td>地址</td><td>114 台北市內湖區洲子街101號2樓</td></tr>
    </tbody></table>
    <p class="gd-note" style="margin-top:24px">延伸閱讀：<a href="about.html">關於奧洛</a>・<a href="fsc-ai-guideline.html">金融業運用 AI 指引怎麼落實</a>・<a href="llm-gateway-guide.html">地端 LLM 閘道選型清單</a></p>'''

sections = [
    section('pr-body', '01', '新聞稿', '每一次 AI 呼叫，先檢查、可查驗', body),
    section('pr-points', '02', '平台特點', '三個設計原則', points),
    section('pr-modules', '03', '平台模組', '一個治理底座，14 個模組', module_table),
    section('pr-deploy', '04', '部署方式', '雲端、地端、隔離網路', deploy),
    section('pr-about', '05', '關於奧洛', '公司簡介與媒體聯絡', about, last=True),
]
build('press-auro-nexus.html',
      '奧洛 Aurobase 推出 AURO NEXUS AI 治理平台｜新聞稿',
      '奧洛 Aurobase 推出 AURO NEXUS AI 治理平台：以 Forge 治理底座串起 14 個模組，AI 呼叫在推論前先檢查權限與政策、可限定只用地端模型，並寫入可離線驗證的雜湊鏈稽核軌跡，協助金融與受監理產業在自有環境導入生成式 AI。',
      ['奧洛 Aurobase', 'AURO NEXUS', 'AI 治理平台', '地端 AI', '生成式 AI 治理', '金融業運用 AI 指引', 'AI 稽核軌跡', '新聞稿'],
      '新聞稿', ['奧洛 Aurobase 推出<br>AURO NEXUS AI 治理平台<em>.</em>'],
      '每一次 AI 呼叫先檢查權限與政策、可限定只用地端模型、證據可離線驗證，協助金融與受監理產業在自有環境導入生成式 AI。',
      '新聞稿 ・ %s ・ 台北' % DATE_ZH,
      sections, ('nexus.html', '了解 AURO NEXUS'), ('contact.html', '聯絡我們'), kicker='AUROBASE')
print('ok')
