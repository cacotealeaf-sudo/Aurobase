/* 全站搜尋：平台總覽「依需求找模組」與側欄「搜尋」共用同一套比對。
 * 索引 search-index.json 由 tools/build-module-pages.py 產生；考題在 tools/search-eval/，
 * GitHub Action 會用同一份程式跑考題，命中率掉下來就不發布。 */
(function (root) {
  'use strict';

  // 不具區別力的兩字組：出現在大多數需求句裡，比對時略過
  var STOP = ('我們 我想 想要 需要 希望 如何 怎麼 怎樣 可以 能夠 能不 一個 這個 那個 公司 企業 我們的 幫我 協助 ' +
    '有沒 沒有 什麼 系統 平台 工具 方案 解決 一下 一些 目前 現在 是否 要求 問題 東西 相關 處理 想知 知道 ' +
    '要做 要有 做好 能做 有沒有 嗎 哪裡 哪些 哪個 多少 為什 什麼 怎麼 請問 謝謝').split(' ');

  function norm(s) {
    s = String(s || '');
    if (s.normalize) s = s.normalize('NFKC');
    return s.toLowerCase().replace(/臺/g, '台');
  }

  function terms(q) {
    q = norm(q);
    var out = [], m, re = /[a-z0-9][a-z0-9.+#-]*/g;
    // 英文詞去掉常見字尾，讓 governance／governed、automation／automated 對得上
    while ((m = re.exec(q))) if (m[0].length > 1) out.push(m[0].length > 5 ? m[0].replace(/(ations?|ances?|ences?|ings?|ments?|ed|es|s)$/, '') : m[0]);
    q.split(/[^㐀-鿿]+/).forEach(function (run) {
      if (run.length === 1) out.push(run);
      for (var i = 0; i + 1 < run.length; i++) {
        var b = run.substr(i, 2);
        if (STOP.indexOf(b) < 0) out.push(b);
      }
    });
    return out.filter(function (t, i, a) { return a.indexOf(t) === i; });
  }

  // entries: [{k: 主要文字（名稱、需求、搜尋用詞，命中加倍）, s: 其餘文字}, ...]，k、s 已正規化
  function rank(q, entries) {
    var ts = terms(q);
    if (!ts.length) return [];
    var n = entries.length;
    var idf = ts.map(function (t) {
      var df = 0;
      entries.forEach(function (e) { if (e.k.indexOf(t) >= 0 || e.s.indexOf(t) >= 0) df++; });
      return df ? Math.log(1 + n / df) : 0;
    });
    // 整句（去空白）出現在名稱或搜尋用詞裡，例如直接輸入產品名：額外加分，排到最前面
    var phrase = norm(q).replace(/\s+/g, '');
    var maxIdf = Math.max.apply(null, idf.concat([0]));
    var scored = entries.map(function (e, i) {
      var sc = 0, hit = 0;
      if (phrase.length >= 3 && e.k.replace(/\s+/g, '').indexOf(phrase) >= 0) sc += 2 * maxIdf;
      ts.forEach(function (t, j) {
        if (!idf[j]) return;
        if (e.k.indexOf(t) >= 0) { sc += 2 * idf[j]; hit++; }
        else if (e.s.indexOf(t) >= 0) { sc += idf[j]; hit++; }
      });
      return { i: i, score: sc, hit: hit };
    }).filter(function (r) { return r.hit > 0; });
    if (!scored.length) return [];
    scored.sort(function (a, b) { return b.score - a.score || a.i - b.i; });
    // 分數太低、或遠低於最高分的結果是雜訊
    var floor = Math.max(1.2, scored[0].score * 0.34);
    return scored.filter(function (r) { return r.score >= floor; });
  }

  var api = { norm: norm, terms: terms, rank: rank };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; return; }
  root.AuroSearch = api;

  /* ── 側欄「搜尋網站」 ── */
  var script = document.currentScript;
  var base = script ? script.src.replace(/js\/site-search\.js.*$/, '') : '';
  var index = null, loading = null;

  function load() {
    if (index) return Promise.resolve(index);
    if (!loading) loading = fetch(base + 'search-index.json').then(function (r) { return r.json(); }).then(function (d) {
      index = d.map(function (e) { e.k = norm(e.k); e.s = norm(e.s); return e; });
      return index;
    });
    return loading;
  }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function href(u) { return /^https?:/.test(u) ? u : base + u; }

  function build() {
    var d = document.createElement('div');
    d.className = 'ss-overlay';
    d.hidden = true;
    d.innerHTML =
      '<div class="ss-dialog" role="dialog" aria-modal="true" aria-labelledby="ss-title">' +
      '<div class="ss-head"><h2 id="ss-title">搜尋產品與服務</h2><button type="button" class="ss-close" aria-label="關閉">×</button></div>' +
      '<input type="search" class="ss-input" autocomplete="off" aria-label="描述您的需求" placeholder="例如：會員資料整合、程式弱點掃描、Google 廣告代操">' +
      '<p class="ss-msg" aria-live="polite"></p><ul class="ss-results"></ul>' +
      '<div class="ss-none" hidden><p>沒有找到直接對應的產品或服務。您的需求可能需要組合或客製，直接告訴我們，我們會回覆建議的做法。</p>' +
      '<a class="ss-ask" href="' + base + 'contact.html">把這個需求告訴我們</a></div>' +
      '<p class="ss-hint">可以直接打一句話，例如「想讓員工安全地使用 ChatGPT」。</p></div>';
    document.body.appendChild(d);
    var input = d.querySelector('.ss-input'), list = d.querySelector('.ss-results'), msg = d.querySelector('.ss-msg'),
      none = d.querySelector('.ss-none'), ask = d.querySelector('.ss-ask'), last = null, timer;

    function close() { d.hidden = true; document.documentElement.classList.remove('ss-open'); if (last) last.focus(); }
    function run() {
      var v = input.value.trim();
      if (!v) { list.innerHTML = ''; msg.textContent = ''; none.hidden = true; return; }
      load().then(function (idx) {
        var res = rank(v, idx).slice(0, 8);
        list.innerHTML = res.map(function (r) {
          var e = idx[r.i];
          return '<li><a href="' + esc(href(e.u)) + '"' + (/^https?:/.test(e.u) ? ' target="_blank" rel="noopener"' : '') + '>' +
            '<span class="ss-cat">' + esc(e.c) + '</span><b>' + esc(e.t) + '</b><span class="ss-desc">' + esc(e.d) + '</span></a></li>';
        }).join('');
        msg.textContent = res.length ? '找到 ' + res.length + ' 個相關結果，最相關的排在前面。' : '';
        none.hidden = res.length > 0;
      });
    }
    input.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(run, 80); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { var a = list.querySelector('a'); if (a) a.click(); }
    });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    d.addEventListener('click', function (e) { if (e.target === d) close(); });
    d.querySelector('.ss-close').addEventListener('click', close);
    ask.addEventListener('click', function (e) {
      var modal = document.getElementById('myModal'), t = document.getElementById('f06');
      if (!modal || !window.jQuery) return;   // 沒有詢問表單的頁面就前往聯絡我們
      e.preventDefault();
      if (t && input.value.trim() && !t.value) t.value = input.value.trim();
      close();
      window.jQuery(modal).modal('show');
    });
    return function open(trigger, value) {
      last = trigger || document.activeElement;
      d.hidden = false;
      document.documentElement.classList.add('ss-open');
      load();
      if (value) { input.value = value; run(); }
      input.focus();
      input.select();
    };
  }

  var opener = null;
  function open(t, v) { if (!opener) opener = build(); opener(t, v); }
  // 網址帶 ?q=：直接打開搜尋（平台總覽的「依需求找模組」自己處理，不重複開視窗）
  document.addEventListener('DOMContentLoaded', function () {
    var m = /[?&]q=([^&#]*)/.exec(location.search);
    if (m && !document.getElementById('finder')) open(null, decodeURIComponent(m[1].replace(/\+/g, ' ')));
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.nav-search-btn');
    if (b) { e.preventDefault(); open(b); }
  });
  document.addEventListener('keydown', function (e) {
    var tag = (e.target.tagName || '').toLowerCase();
    if (e.key === '/' && tag !== 'input' && tag !== 'textarea' && !e.target.isContentEditable) { e.preventDefault(); open(); }
  });
})(typeof window !== 'undefined' ? window : this);
