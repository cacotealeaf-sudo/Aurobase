"""關於奧洛（about.html）。內容只用網站上已公開的事實；改完跑 python3 tools/guides/about_page.py，
再跑 tools/build-module-pages.py（補常見問題與結構化資料，設定在 _pages.json）。"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guidekit import build, section

answer = '''    <div class="gd-answer">
      <p><b>奧洛 Aurobase</b>（奧洛股份有限公司）位於台北內湖，自有產品 <a href="nexus.html">AURO NEXUS</a> 是可部署於企業自有機房的 AI 治理平台：每一次 AI 呼叫都先檢查權限與政策，並留下可離線驗證的稽核紀錄，讓金融與受監理產業在自有環境導入生成式 AI。</p>
      <p>奧洛也代理 HCL Discover、HCL Unica、Magnolia CMS 等行銷科技產品，並提供 Google、Meta 廣告投放與社群經營服務。</p>
    </div>'''


def card(meta, title, href, items):
    return ('      <article class="idx-card gd-card"><div class="idx-card-meta"><span>// %s</span></div>'
            '<h3 class="idx-card-title"><a href="%s">%s</a></h3><ul>%s</ul></article>'
            % (meta, href, title, ''.join('<li>%s</li>' % x for x in items)))


lines = '    <div class="idx-grid">\n' + '\n'.join([
    card('自有產品', 'AURO NEXUS AI 治理平台', 'nexus.html', [
        '以 <a href="nexus-forge.html">Forge</a> 治理底座串起 AI 編排、客戶資料、知識、內容與行銷智能、合規治理、生產力、現代化與安全等模組',
        '推論前檢查權限與政策，可限定只用地端模型',
        '雜湊鏈稽核軌跡，證據包可離線驗證']),
    card('產業解決方案', '由平台模組組成的方案', 'nexus.html#solutions', [
        '公部門：<a href="solution-police-record.html">警詢筆錄 AI 輔助</a>',
        '金融保險：<a href="solution-telesales.html">電話與視訊銷售對話智能</a>',
        '社福長照：<a href="ai-companion.html">AI 智慧語伴</a>',
        '跨產業：<a href="solution-ai-ocr.html">AI OCR 智慧文件辨識</a>',
        '數位行銷：<a href="solution-digital-trail.html">數位軌跡行銷資料整合</a>']),
    card('代理與導入', '行銷科技產品', 'solution.html', [
        'HCL Discover 數位體驗分析', 'HCL Unica 行銷自動化', 'Magnolia CMS 內容管理系統']),
    card('服務', '數位行銷與客服中心', 'marketing.html', [
        'Google、Meta、LINE 廣告投放', '社群經營與 LINE 官方帳號', '客服中心系統建置與外包服務（<a href="https://aurocore.com/" target="_blank" rel="noopener">AUROCORE</a>）']),
]) + '\n    </div>'

deploy = '''    <div class="gd-cols">
      <div class="gd-block"><h3>公有雲台灣區域</h3><ul><li>資料留在台灣，適合要快速上線的企業</li></ul></div>
      <div class="gd-block"><h3>企業自有機房或隔離網路</h3><ul><li>模型可限定只用地端，適合金融與受監理產業</li></ul></div>
      <div class="gd-block"><h3>依流程客製</h3><ul><li>權限規則、審核流程與既有系統介接，由奧洛工程團隊依需求開發</li></ul></div>
    </div>
    <p class="gd-note" style="margin-top:24px">三種方式使用同一套權限、模型路由與稽核軌跡，日後可以搬移。資料處理方式見<a href="security.html">資安與資料處理</a>。</p>'''

partners = [('Google', '廣告投放夥伴'), ('Meta', 'Facebook・Instagram 廣告夥伴'), ('LINE', 'LINE 廣告與官方帳號夥伴'),
            ('HCL Software', '數位體驗分析與行銷自動化夥伴'), ('Magnolia', 'CMS 企業夥伴'), ('精誠資訊', '系統整合與通路夥伴'),
            ('零壹科技', '事業夥伴')]
partner_table = ('    <table class="gd-table"><thead><tr><th>夥伴</th><th>合作關係</th></tr></thead><tbody>'
                 + ''.join('<tr><td>%s</td><td>%s</td></tr>' % p for p in partners) + '</tbody></table>')

facts = [('公司名稱', '奧洛股份有限公司'), ('品牌', '奧洛 Aurobase'), ('地址', '114 台北市內湖區洲子街101號2樓'),
         ('電話', '<a href="tel:+886-2-5568-4688">+886-2-5568-4688</a>'),
         ('Email', '<a href="mailto:ad@aurocore.com">ad@aurocore.com</a>'),
         ('粉絲專頁', '<a href="https://www.facebook.com/AurobaseTW/" target="_blank" rel="noopener">facebook.com/AurobaseTW</a>')]
fact_table = ('    <table class="gd-table"><tbody>' + ''.join('<tr><td>%s</td><td>%s</td></tr>' % f for f in facts) + '</tbody></table>'
              '\n    <p class="gd-note" style="margin-top:24px">延伸閱讀：<a href="fsc-ai-guideline.html">金融業運用 AI 指引怎麼落實</a>・'
              '<a href="llm-gateway-guide.html">地端 LLM 閘道選型清單</a>・<a href="security.html">資安與資料處理</a></p>')

sections = [
    section('ab-answer', '01', '認識奧洛', '奧洛 Aurobase 是什麼公司', answer),
    section('ab-lines', '02', '產品與服務', '四條產品與服務線', lines),
    section('ab-deploy', '03', '部署方式', '雲端、地端、隔離網路', deploy),
    section('ab-partners', '04', '事業夥伴', '合作夥伴', partner_table),
    section('ab-facts', '05', '公司資訊', '聯絡與公司資料', fact_table, last=True),
]
build('about.html',
      '關於奧洛｜奧洛 Aurobase：AI 治理平台與行銷科技',
      '奧洛 Aurobase（奧洛股份有限公司）位於台北內湖，開發可部署於企業自有機房的 AURO NEXUS AI 治理平台，並代理 HCL Discover、HCL Unica、Magnolia CMS 等行銷科技產品，提供廣告投放與社群經營服務。',
      ['關於奧洛', '奧洛 Aurobase', '奧洛股份有限公司', 'AURO NEXUS', 'AI 治理平台', '地端 AI', '行銷科技', '台北內湖'],
      '關於奧洛', ['關於奧洛<em>.</em>'],
      '可治理的 AI 平台，加上行銷科技與數位行銷服務。',
      '奧洛股份有限公司 ・ 台北市內湖區',
      sections, ('#ab-lines', '看產品與服務'), ('contact.html', '聯絡我們'), kicker='AUROBASE')
print('ok')
