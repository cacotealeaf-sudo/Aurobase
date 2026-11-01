# AURO NEXUS 產品頁編輯器

改產品頁文案、新增產品，不用碰 HTML。

## 開啟

```bash
python3 tools/cms/server.py
```

瀏覽器開 <http://127.0.0.1:8899>。只在本機執行，不對外開放。

## 改文案

1. 左側選一頁（平台總覽或任一產品）。
2. 在中間的表單修改，右側會即時預覽；上方切換「桌機／手機」。
3. 表單上方會列出「需要修正」（擋儲存）與「建議」（只提醒，例如標題太長、常見問題太少）。
4. 按「儲存並產頁」（或 ⌘S）：寫回 `tools/module-pages/*.json`，重新產生所有產品頁、`nexus.html` 平台總覽、`llms.txt`、`sitemap.xml`，並重建字型子集。

## SEO / GEO

右側切到「SEO / GEO」分頁，會隨著修改即時更新：

- **分數**：SEO、GEO、全站三組檢查各通過幾項。
- **Google 搜尋結果預覽**：標題與摘要超過顯示寬度會被截成「…」（英數字算半格）。
- **檢查清單**：主關鍵字有沒有放進標題前段、H1、摘要；摘要長度；內部連結；有沒有和別頁搶同一個主關鍵字；
  定義區的「X 是奧洛（Aurobase）…」實體句；常見問題數量與回答長度、回答單獨被引用時看不看得懂；
  比較表／法規對照；可查證的外部來源；更新日期；robots.txt 是否放行 AI 爬蟲；llms.txt 與 sitemap 是否收錄。
- **找關鍵字與常見問法**：查 Google 台灣的搜尋建議。點「搜尋建議」的結果加進目標關鍵字，點「常見問法」的結果新增一題常見問題。
- **llms.txt 這一行**與**結構化資料（JSON-LD）**的實際內容。

全站報告：`python3 tools/build-module-pages.py --audit`。GitHub Action 每次產頁也會把報告寫進執行摘要。

## 新增產品

1. 按「＋ 新增產品」，填產品名、中文功能名、網址代號、平台分組、需求一句話。
2. 建好的是**草稿**：不產頁、不出現在總覽。逐欄把內容填完。
3. 取消「草稿」後儲存，才會發布；產品會自動放進平台總覽的分組，以及「依需求找模組」表格。

想暫時下架某個產品：勾回「草稿」再儲存，頁面會被移除，其他頁面連到它的連結也會暫時隱藏。

## 網站搜尋

每頁側欄的「搜尋產品與服務」與平台總覽的「依需求找模組」用同一份索引 `search-index.json`，產頁時自動重建：

- 平台模組與產業解決方案：取自產品 JSON。表單裡的「需求搜尋用詞」放客戶描述需求時常用的說法（例如「憑證過期」「COBOL」），只用於比對，不會顯示在頁面上。
- 其他頁面的服務與代理產品：在 `tools/module-pages/_search.json` 增減。
- 考題：`tools/search-eval/queries.json` 是模擬潛在客戶的搜尋說法，`node tools/search-eval/run.js --verbose` 會列出每題的前三名。GitHub Action 發布前會跑一次，命中率低於門檻就不發布。新增產品或服務時，順手補幾題。

## 發布

編輯器只改本機檔案。發布方式：

```bash
git add -A && git commit -m "content: 更新產品頁文案"
git push origin main
```

推到 main 後，GitHub Action（`.github/workflows/build-product-pages.yml`）會再跑一次測試與產頁、重建字型與圖示子集，有差異就自動 commit，並請 GitHub Pages 重新建置。內容有錯時 Action 會失敗，不會發布壞掉的頁面。

## 給開發者

- 版面在 `tools/build-module-pages.py`；表單欄位在 `tools/cms/schema.js`。新增欄位要兩邊都改。
- 測試：`python3 tools/cms/test_cms.py`（在暫存複本上跑，不動到真的檔案）。
