#!/usr/bin/env python3
"""文案 v5（2026-10-30）：去掉格言式引言與「不是…而是…」等套句；部署段落統一為雲端、地端、客製三種方式。
套用一次即寫回各 JSON；之後直接改 JSON（或用 tools/cms 編輯器），本檔保留作為改版紀錄。"""
import io
import json
import os

HERE = os.path.dirname(__file__)
CLOUD = '公有雲的台灣區域（例如 Google Cloud 台灣區域）'


def dep(cloud, onprem, custom):
    return [{'tag': '雲端', 'title': cloud[0], 'text': cloud[1]},
            {'tag': '地端', 'title': onprem[0], 'text': onprem[1]},
            {'tag': '客製', 'title': custom[0], 'text': custom[1]}]


V5 = {
'nexus-forge': {
    'hero.tagline': '從一個部門、一個模型開始接入，之後新增的模組與部門都走同一個閘道。',
    'pain.heading': 'AI 進入企業之後，先出問題的通常是這三件事',
    'pain.statement': 'Forge 把企業內的 AI 使用集中到一個入口、一套權限與一條稽核帳，請求先檢查再送往模型。',
    'deploy': dep(
        ('公有雲 Kubernetes', '以 Helm chart 部署於%s，模型可接雲端服務或自架於雲端 GPU 主機。' % CLOUD),
        ('自有機房、模型不出機房', '部署於企業自有機房或私有雲，模型路由可限定只走地端 Ollama 或 OpenAI 相容服務（如 vLLM）。'),
        ('政策與模型清單', '權限規則、可用模型、知識庫與工具清單依貴機構規範設定；與既有身分系統的介接由奧洛團隊配合調整。')),
},
'nexus-auro': {
    'hero.sub': 'AI 代理能自己拆解任務、呼叫工具、委派子任務，也可能在迴圈裡打轉、超出預算、做出不該做的動作。Auro 為每個任務設好上限，每一步先過治理閘門，必要時暫停交人審核，任何時候都能緊急停止。',
    'hero.tagline': '步數、token 與時間都有上限，送審的步驟要等人核准才會繼續。',
    'pain.heading': 'AI 代理上線前要先回答的三個問題',
    'pain.statement': 'Auro 為每個任務設定硬上限與審核點，治理服務無法回應時一律停下，每一步都留有紀錄。',
    'diff.cards.0.title': '治理服務缺席時一律阻擋',
    'deploy': dep(
        ('公有雲 Kubernetes', '以 Helm chart 部署於%s，與 Forge 部署在同一個環境。' % CLOUD),
        ('自有機房與離線設定', '部署於企業自有機房；完全離線的設定只使用地端模型，適合隔離網路。'),
        ('流程與審核點', '依貴機構的作業流程設計任務、技能與審核關卡，由奧洛團隊協助串接既有系統。')),
},
'nexus-cdp': {
    'hero.tagline': '身分合併的規則與依據都查得到，信心值不足的交給人審。',
    'pain.heading': '客戶資料整合常卡在這三個地方',
    'pain.statement': 'AURA CDP 以信心值決定身分是否合併，分群可直接觸發旅程，同意與刪除請求都記在只能附加的帳本裡。',
    'deploy': dep(
        ('公有雲 Kubernetes', '以 Helm chart 部署於%s，提供高可用設定。' % CLOUD),
        ('自有機房或單機試點', '部署於企業自有機房或私有雲；試點可先用單一虛擬機起一套環境。'),
        ('資料來源與通路介接', '依貴機構的會員、交易與客服系統設計資料介接與身分比對規則；通路可接 LINE 官方帳號、App 推播與 WhatsApp。')),
},
'nexus-abm': {
    'hero.sub': '同一家企業的採購、技術、主管分別看了官網、下載了白皮書、參加了講座，在一般行銷工具裡卻是三筆互不相干的名單。NEXUS ABM 把他們歸到同一個企業帳號，算出這家公司的購買意圖，並說得出分數是怎麼來的。',
    'hero.tagline': '每一分意圖分數都能回溯到具體行為，業務看得到為什麼。',
    'pain.statement': 'NEXUS ABM 以企業帳號為單位計算意圖分數，並用四種歸因模型比較各接觸點的貢獻。',
    'deploy': dep(
        ('公有雲 Kubernetes', '以 Helm chart 部署於%s。' % CLOUD),
        ('自有機房', '部署於企業自有機房或私有雲，與 AURA CDP 共用客戶圖譜。'),
        ('CRM 與評分規則', '與既有 CRM 的同步、評分權重與分級門檻，依貴公司的銷售流程設定與驗證。')),
},
'nexus-insight': {
    'hero.tagline': '萃取出的知識要經人核准才會被搜尋與問答引用。',
    'pain.heading': '企業知識庫常見的三個問題',
    'pain.statement': 'Insight 在文件與問答之間加上萃取、審核與版本管理，每一項知識都有出處、核准人與版本。',
    'deploy': dep(
        ('公有雲 Kubernetes', '以 Helm chart 部署於%s。' % CLOUD),
        ('自有機房、模型內建', '部署於企業自有機房；語意向量模型打包在映像內，AI 萃取可限定只用地端模型。'),
        ('文件類型與審核角色', '依貴機構的文件種類、審核流程與權限角色調整萃取規則與核准關卡。')),
},
'nexus-library': {
    'hero.tagline': '收藏留在企業環境內，需要時可交給 Insight 建立語意索引。',
    'pain.statement': 'Library 讓個人收藏留在企業環境內、依人員劃分，並可由企業知識庫建立索引。',
    'diff.cards.2.title': '個資刪除可追溯',
    'deploy': dep(
        ('公有雲 Kubernetes', '以 Helm chart 部署於%s。' % CLOUD),
        ('自有機房', '部署於企業自有機房或私有雲；Chrome 擴充套件可由企業統一派送。'),
        ('收藏來源與介接', '依貴機構需要增加收藏入口或調整與企業知識庫的串接方式。')),
},
'nexus-mira': {
    'hero.tagline': '每一份內容的撰稿、修改與核准紀錄都寫入雜湊鏈，可匯出給稽核。',
    'pain.heading': '受監理產業用 AI 寫內容，難在這三件事',
    'pain.statement': 'MIRA 把產製、檢查與審核放在同一條流程：合規規則依產業設定，引用查不到就標「未驗證」，核准紀錄寫入雜湊鏈。',
    'deploy': dep(
        ('公有雲 Kubernetes', '以 Helm chart 部署於%s，文字生成經 Forge 送往經核准的模型。' % CLOUD),
        ('自有機房、地端生成', '部署於企業自有機房；文字與圖像生成可改接地端模型，整條流程可在隔離網路內運作。'),
        ('法規包與審核關卡', '依貴機構的產品類型、內部規範與審核層級，調整合規規則、品牌套件與核准流程。')),
},
'nexus-pulse': {
    'hero.sub': '輿情工具給的是提及次數與正負面比例，但要判斷的是大家在講什麼、往哪個方向發展、要不要處理。Pulse 用批次 AI 分析情緒、摘要與敘事，依規則觸發告警，並回頭計算處理之後的成效。',
    'hero.tagline': '每一次告警都追溯得到觸發它的訊號，處理之後也算得出變化。',
    'pain.heading': '輿情監測常見的三個斷點',
    'pain.statement': 'Pulse 把分析、告警、處理與成效回算接在一起，每一次輿情處理都查得到前因後果。',
    'deploy': dep(
        ('公有雲 Kubernetes', '以 Helm chart 部署於%s。' % CLOUD),
        ('自有機房', '部署於企業自有機房；AI 分析經 Forge 治理，可限定只用地端模型。'),
        ('訊號來源與告警規則', '依貴機構既有的輿情來源設計訊號推入方式，告警條件與通知對象可自訂。')),
},
'nexus-ai-office': {
    'slogan': '格式交給範本<br>初稿交給 AI<br><em>定稿由人決定</em>',
    'hero.tagline': '每一份文件從哪個範本、哪些資料產出，都查得到。',
    'pain.statement': 'AI-Office 把範本集中管理，初稿由受治理的 AI 產出，編修在企業環境內完成。',
    'deploy': dep(
        ('公有雲 Kubernetes', '以 Helm chart 部署於%s，線上編修服務一併部署。' % CLOUD),
        ('自有機房', '部署於企業自有機房，文件與線上編修都不經過外部文書服務。'),
        ('企業範本', '依貴公司的提案、報價與內部文件格式建立範本庫，並可串接既有資料來源。')),
},
'nexus-lisa': {
    'hero.sub': '主機系統跑了三十年，寫程式的人退休了，規格書停在上一個世紀。LISA 直接讀主機原始碼，產出繁體中文規格書，每個欄位、每段流程都附上原始碼行號，可以逐行對照查證。',
    'hero.tagline': '改寫、轉平台或上雲之前，先有一份可以逐行查證的現況規格。',
    'pain.statement': 'LISA 產出的規格書，每一句都能對回原始碼。解析採確定性方法，結果可重現、可逐行查證。',
    'diff.cards.0.title': '可追溯的規格，不是 AI 摘要',
    'deploy': dep(
        ('公有雲 Kubernetes', '以容器部署於%s，適合可將原始碼放上雲端的專案。' % CLOUD),
        ('自有機房、預設不連外', '部署於企業自有機房，部署設定預設封鎖對外連線，原始碼不離開機房。'),
        ('盤點專案', '依貴機構的程式範圍、碼頁與文件格式調整產出；也可由奧洛團隊在現場執行盤點。')),
},
'nexus-scanner': {
    'hero.sub': '原始碼、第三方套件、容器映像、雲端與基礎設施設定、對外網站，各自用不同工具掃，結果散在不同格式裡。Scanner 把這些掃描收進同一個平台，用同一套權限、同一條稽核紀錄、同一種報告格式交付。',
    'hero.tagline': '開發、資安與稽核看到的是同一份掃描結果。',
    'pain.heading': '弱點管理最花時間的是整合結果',
    'pain.statement': 'Scanner 把各類掃描放進同一個平台，以標準格式輸出，並用公開威脅情資為每一筆弱點補上修補順序的依據。',
    'diff.intro': '',
    'deploy_intro': '以容器交付，可放在公有雲的台灣區域、企業自有機房或私有雲；威脅情資需要連線更新。掃描規則與報告格式可依貴機構需求客製。',
    'deploy': dep(
        ('公有雲', '以 docker compose 或 Kubernetes 部署於%s。' % CLOUD),
        ('自有機房', '部署於企業自有機房或私有雲，掃描工作者可依負載擴充；威脅情資需可連外更新。'),
        ('掃描規則與報告', '依貴機構的開發流程設定掃描範圍、規則與報告格式，並串接 CI 與程式碼平台。')),
},
'nexus-cardea': {
    'hero.tagline': '盤點、政策檢查、到期預警與更新都在同一套系統裡完成，單機也能運作。',
    'pain.statement': 'Cardea 把憑證與 SSH 金鑰當成要治理的機器身分：盤點、檢查、預警與更新，每一步都留下紀錄。',
    'deploy': dep(
        ('雲端虛擬機或 Kubernetes', '可部署於%s的虛擬機，或以容器與 Helm chart 部署於 Kubernetes。' % CLOUD),
        ('單機、可離線', '單機設備形態部署，不需外部資料庫與雲端服務，可在隔離網路內完成盤點、檢查與預警。'),
        ('部署目標與通知', '依貴機構的設備與 CA 調整簽發與部署方式；預警可接 ServiceNow、Jira 或 Webhook。')),
},
}

PLATFORM = {
    'tagline': '先從一個模組開始，之後新增的模組都共用同一套權限、模型與稽核軌跡。',
    'summary': [
        ['是什麼', '以治理底座串起 14 個模組的企業 AI 平台。'],
        ['治理底座', '<a href="nexus-forge.html">Forge</a>：權限與政策檢查、模型路由、可離線驗證的稽核軌跡。'],
        ['部署', '可雲、可地、可客製：公有雲台灣區域、企業自有機房或隔離網路，流程與規則可依需求調整。'],
        ['適用', '金融、醫療、公部門等受監理產業，以及重視資料主權的企業。'],
    ],
    'deploy_intro': '同一套平台可以放在公有雲、企業自有機房或隔離網路；三種方式使用相同的權限、模型路由與稽核軌跡，之後也可以搬移。',
    'deploy': dep(
        ('公有雲台灣區域', '部署於%s的 Kubernetes，資料留在台灣，適合要快速上線的企業。' % CLOUD),
        ('自有機房、可離線', '部署於企業自有機房或私有雲，模型可限定只用地端，適合金融與受監理產業。'),
        ('依流程客製', '模組之間可以組合成專案方案；權限規則、審核流程與既有系統介接，由奧洛工程團隊依需求開發。')),
    'diff.2': {'icon': 'server', 'title': '雲端與地端用同一套', 'text': '公有雲與自有機房部署的是同一套平台與治理規則，日後搬移不需要重新導入。'},
    'faq_add': {'q': 'AURO NEXUS 可以放在公有雲嗎？', 'a': '可以。AURO NEXUS 可部署於公有雲的台灣區域（例如 Google Cloud 台灣區域），也可部署於企業自有機房或隔離網路，三種方式使用同一套權限、模型路由與稽核軌跡。'},
}


def setpath(m, path, v):
    ks = path.split('.')
    cur = m
    for k in ks[:-1]:
        cur = cur[int(k)] if k.isdigit() else cur[k]
    last = ks[-1]
    if last.isdigit():
        cur[int(last)] = v
    else:
        cur[last] = v


def main():
    for slug, upd in V5.items():
        p = os.path.join(HERE, slug + '.json')
        m = json.load(io.open(p, encoding='utf-8'))
        for k, v in upd.items():
            if k == 'slogan':
                m['hero']['slogan'] = v
            elif k == 'diff.intro' and not v:
                m['diff'].pop('intro', None)
            else:
                setpath(m, k, v)
        io.open(p, 'w', encoding='utf-8').write(json.dumps(m, ensure_ascii=False, indent=2) + '\n')
        print('patched', slug)
    p = os.path.join(HERE, '_platform.json')
    pf = json.load(io.open(p, encoding='utf-8'))
    pf['tagline'] = PLATFORM['tagline']
    pf['summary'] = PLATFORM['summary']
    pf['deploy_intro'] = PLATFORM['deploy_intro']
    pf['deploy'] = PLATFORM['deploy']
    pf['diff'][2] = PLATFORM['diff.2']
    if not any(f['q'] == PLATFORM['faq_add']['q'] for f in pf['faq']):
        pf['faq'].insert(3, PLATFORM['faq_add'])
    io.open(p, 'w', encoding='utf-8').write(json.dumps(pf, ensure_ascii=False, indent=2) + '\n')
    print('patched _platform')


if __name__ == '__main__':
    main()
