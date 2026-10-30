// 表單欄位定義。新增欄位：在這裡加一筆，並在 tools/build-module-pages.py 把它渲染出來。
// type：str 單行｜text 多行（可用 <b> <em> <br> <a>）｜tags 逗號分隔｜list 文字清單｜
//       objlist 物件清單｜pairs 兩欄清單｜rows 表格列｜select｜multi 複選｜color｜bool｜readonly
// optional：整組可開關（關掉時從 JSON 移除）。max / min：字數提示（不擋儲存）。

const ICON = { k: 'icon', label: '圖示', type: 'select', options: 'icons' };

window.MODULE_SCHEMA = [
  { sec: '發布狀態', fields: [
    { k: 'draft', label: '草稿（不產頁、不出現在總覽）', type: 'bool' },
    { k: 'updated', label: '最後更新（儲存時自動更新）', type: 'readonly' },
  ]},
  { sec: '名稱與搜尋', fields: [
    { k: 'code', label: '產品名', type: 'str', help: '頁面與總覽卡片上的主名，例如 Cardea、AURA CDP。' },
    { k: 'name_zh', label: '中文功能名', type: 'str' },
    { k: 'fullname', label: '縮寫全稱（選填）', type: 'str', help: '例如 CARDEA = Certificate Automation…，會顯示在首屏最上方。' },
    { k: 'aliases', label: '舊名／別名', type: 'tags', help: '只放進結構化資料，讓搜尋引擎知道是同一個產品。' },
    { k: 'leg', label: '能力分類（頁面上顯示）', type: 'str' },
    { k: 'title', label: '頁面標題（搜尋結果的藍字）', type: 'str', max: 45, help: '主關鍵字放最前面。' },
    { k: 'description', label: '搜尋摘要', type: 'text', min: 70, max: 160, help: '第一句寫「X 是奧洛（Aurobase）的…」，AI 引擎最常直接引用這段。' },
    { k: 'keywords', label: '目標關鍵字', type: 'tags' },
    { k: 'eyebrow', label: '英文副名', type: 'str', help: '例如 Cardea — Machine Identity & Certificate Governance。' },
    { k: 'inquiry_chip', label: '諮詢表單預設勾選', type: 'select', options: 'chips' },
  ]},
  { sec: '首屏', fields: [
    { k: 'hero.h1', label: 'H1（關鍵字型）', type: 'str', help: '格式：產品名｜主關鍵字・次關鍵字' },
    { k: 'hero.slogan', label: '主張（大字）', type: 'text', help: '用 <br> 換行、<em>…</em> 標強調色。' },
    { k: 'hero.sub', label: '副標', type: 'text' },
    { k: 'hero.tagline', label: '引言', type: 'text' },
    { k: 'hero.badges', label: '標籤', type: 'objlist', item: [ICON, { k: 'text', label: '文字', type: 'str' }] },
  ]},
  { sec: '重點摘要', fields: [
    { k: 'summary', label: '項目', type: 'pairs', cols: ['標題', '內容'], help: '一定要有「是什麼」，平台總覽的產品卡片會用它。' },
  ]},
  { sec: '定義區（給 AI 引擎引用）', fields: [
    { k: 'definition.q', label: '問題', type: 'str', help: '用使用者實際會問的句子，例如「什麼是 SSL 憑證管理？」' },
    { k: 'definition.a', label: '回答段落', type: 'list', item: 'text' },
    { k: 'audience', label: '適合誰', type: 'objlist', item: [{ k: 'who', label: '對象', type: 'str' }, { k: 'why', label: '原因', type: 'text' }] },
  ]},
  { sec: '問題', fields: [
    { k: 'pain.heading', label: '標題', type: 'str' },
    { k: 'pain.intro', label: '引言（選填）', type: 'text' },
    { k: 'pain.cards', label: '痛點卡片', type: 'objlist', item: [{ k: 'title', label: '標題', type: 'str' }, { k: 'text', label: '說明', type: 'text' }] },
    { k: 'pain.statement', label: '結論句', type: 'text' },
  ]},
  { sec: '核心能力', fields: [
    { k: 'capabilities.heading', label: '標題', type: 'str' },
    { k: 'capabilities.intro', label: '引言（選填）', type: 'text' },
    { k: 'capabilities.cards', label: '能力卡片', type: 'objlist', item: [ICON, { k: 'title', label: '標題', type: 'str' }, { k: 'items', label: '要點', type: 'list', item: 'text' }] },
  ]},
  { sec: '法規對照', optional: 'regulation', fields: [
    { k: 'regulation.heading', label: '標題', type: 'str' },
    { k: 'regulation.intro', label: '引言', type: 'text' },
    { k: 'regulation.cols', label: '欄名（兩欄）', type: 'list', item: 'str' },
    { k: 'regulation.rows', label: '對照列', type: 'rows', ncols: () => 2 },
    { k: 'regulation.sources', label: '資料來源', type: 'objlist', item: [{ k: 'name', label: '名稱', type: 'str' }, { k: 'url', label: '網址', type: 'str' }] },
    { k: 'regulation.note', label: '附註', type: 'text' },
  ]},
  { sec: '比較表', optional: 'compare', fields: [
    { k: 'compare.heading', label: '標題', type: 'str' },
    { k: 'compare.intro', label: '引言（選填）', type: 'text' },
    { k: 'compare.cols', label: '比較對象（最後一欄是我們）', type: 'list', item: 'str' },
    { k: 'compare.rows', label: '比較列（第一格是比較項目）', type: 'rows', ncols: (doc) => ((doc.compare && doc.compare.cols) || []).length + 1 },
  ]},
  { sec: '差異點', fields: [
    { k: 'diff.heading', label: '標題', type: 'str' },
    { k: 'diff.intro', label: '引言（選填）', type: 'text' },
    { k: 'diff.cards', label: '差異卡片', type: 'objlist', item: [ICON, { k: 'title', label: '標題', type: 'str' }, { k: 'text', label: '說明', type: 'text' }] },
  ]},
  { sec: '平台位置', fields: [
    { k: 'platform.heading', label: '標題', type: 'str' },
    { k: 'platform.text', label: '說明', type: 'text' },
    { k: 'platform.related', label: '相關產品連結', type: 'multi', options: 'related_options' },
  ]},
  { sec: '部署形態', fields: [
    { k: 'deploy', label: '部署卡片', type: 'objlist', item: [{ k: 'tag', label: '標籤', type: 'str' }, { k: 'title', label: '標題', type: 'str' }, { k: 'text', label: '說明', type: 'text' }] },
  ]},
  { sec: '範圍界定', fields: [
    { k: 'limits_intro', label: '引言', type: 'text' },
    { k: 'limits', label: '項目', type: 'objlist', item: [{ k: 'title', label: '標題', type: 'str' }, { k: 'text', label: '說明', type: 'text' }] },
  ]},
  { sec: '常見問題', fields: [
    { k: 'faq', label: '問答', type: 'objlist', item: [{ k: 'q', label: '問題', type: 'str' }, { k: 'a', label: '回答', type: 'text' }], help: '問題用使用者實際搜尋的問法；回答第一句直接給答案。' },
  ]},
  { sec: '結尾', fields: [
    { k: 'cta.heading', label: '標題', type: 'str' },
    { k: 'cta.text', label: '說明', type: 'text' },
  ]},
  { sec: '配色', fields: [
    { k: 'theme.deep', label: '深色（按鈕、標籤字）', type: 'color' },
    { k: 'theme.bright', label: '亮色（漸層、項目符號）', type: 'color' },
    { k: 'theme.soft', label: '深底上的強調字', type: 'color' },
    { k: 'theme.tint', label: '淺底', type: 'color' },
    { k: 'theme.ink1', label: '深底漸層 1', type: 'color' },
    { k: 'theme.ink2', label: '深底漸層 2', type: 'color' },
  ]},
];

window.PLATFORM_SCHEMA = [
  { sec: '名稱與搜尋', fields: [
    { k: 'updated', label: '最後更新（儲存時自動更新）', type: 'readonly' },
    { k: 'title', label: '頁面標題', type: 'str', max: 45 },
    { k: 'description', label: '搜尋摘要', type: 'text', min: 70, max: 160 },
    { k: 'keywords', label: '目標關鍵字', type: 'tags' },
  ]},
  { sec: '首屏', fields: [
    { k: 'h1', label: 'H1', type: 'str' },
    { k: 'slogan', label: '主張（大字）', type: 'text' },
    { k: 'sub', label: '副標', type: 'text' },
    { k: 'tagline', label: '引言', type: 'text' },
    { k: 'summary', label: '重點摘要', type: 'pairs', cols: ['標題', '內容'] },
  ]},
  { sec: '定義區', fields: [
    { k: 'definition.q', label: '問題', type: 'str' },
    { k: 'definition.a', label: '回答段落', type: 'list', item: 'text' },
    { k: 'audience', label: '適合誰', type: 'objlist', item: [{ k: 'who', label: '對象', type: 'str' }, { k: 'why', label: '原因', type: 'text' }] },
  ]},
  { sec: '能力架構', fields: [
    { k: 'legs', label: '能力分組（第一組是治理底座，顯示在最下方）', type: 'objlist', item: [
      { k: 'name', label: '名稱', type: 'str' }, { k: 'text', label: '一句話', type: 'str' },
      { k: 'modules', label: '產品', type: 'multi', options: 'related_options' }] },
  ]},
  { sec: '依需求找模組', fields: [
    { k: 'needs.heading', label: '標題', type: 'str' },
    { k: 'needs.intro', label: '引言', type: 'text' },
    { k: 'needs.rows', label: '需求 → 產品代號', type: 'rows', ncols: () => 2 },
  ]},
  { sec: '平台的承諾', fields: [
    { k: 'diff', label: '卡片', type: 'objlist', item: [ICON, { k: 'title', label: '標題', type: 'str' }, { k: 'text', label: '說明', type: 'text' }] },
  ]},
  { sec: '常見問題', fields: [
    { k: 'faq', label: '問答', type: 'objlist', item: [{ k: 'q', label: '問題', type: 'str' }, { k: 'a', label: '回答', type: 'text' }] },
  ]},
];
