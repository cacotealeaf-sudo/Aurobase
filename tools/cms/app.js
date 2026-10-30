// AURO NEXUS 產品頁編輯器：表單由 schema.js 產生，改動即時送到 /api/preview 渲染。
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const state = { meta: null, id: null, doc: null, saved: '', schema: null, errors: [], warnings: [], timer: null, seq: 0 };

  async function api(method, url, body) {
    const r = await fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
    const data = await r.json().catch(() => ({}));
    return { ok: r.ok, status: r.status, data };
  }

  function toast(msg, kind = 'ok', ms = 4200) {
    const t = $('#toast');
    t.textContent = msg; t.className = 'toast ' + kind; t.hidden = false;
    clearTimeout(toast.t); toast.t = setTimeout(() => { t.hidden = true; }, ms);
  }

  // ── 路徑存取：'hero.badges' ──
  const getp = (o, p) => p.split('.').reduce((a, k) => (a == null ? undefined : a[k]), o);
  function setp(o, p, v) {
    const ks = p.split('.'); let cur = o;
    ks.slice(0, -1).forEach((k) => { if (cur[k] == null || typeof cur[k] !== 'object') cur[k] = {}; cur = cur[k]; });
    cur[ks[ks.length - 1]] = v;
  }
  function delp(o, p) {
    const ks = p.split('.'); const parent = getp(o, ks.slice(0, -1).join('.')) ?? (ks.length === 1 ? o : null);
    if (parent) delete parent[ks[ks.length - 1]];
  }

  const isDirty = () => state.doc && JSON.stringify(state.doc) !== state.saved;

  // ── 側欄 ──
  async function loadMeta() {
    const r = await api('GET', '/api/state');
    state.meta = r.data;
    const navP = $('#navPlatform'); const navM = $('#navModules');
    navP.innerHTML = ''; navM.innerHTML = '';
    navP.append(navItem('_platform', '平台總覽', 'nexus.html'));
    r.data.modules.forEach((m) => navM.append(navItem(m.slug, m.code, m.name_zh, m.draft)));
    const g = r.data.git_dirty;
    $('#gitStatus').innerHTML = g.length
      ? `<b>${g.length} 個檔案尚未 commit</b><span>發布：commit 後 push 到 main</span>`
      : '<b>沒有未 commit 的變更</b>';
    highlightNav();
  }
  function navItem(id, title, sub, draft) {
    const li = document.createElement('li');
    const b = document.createElement('button');
    b.type = 'button'; b.dataset.id = id; b.setAttribute('aria-label', `${title} ${sub || ''}${draft ? '（草稿）' : ''}`);
    b.innerHTML = `<span>${esc(title)}${draft ? '<i class="tag-draft">草稿</i>' : ''}</span><small>${esc(sub || '')}</small>`;
    b.onclick = () => openDoc(id);
    li.append(b); return li;
  }
  function highlightNav() {
    document.querySelectorAll('.side nav button').forEach((b) => b.classList.toggle('on', b.dataset.id === state.id));
  }
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  // ── 開啟一頁 ──
  async function openDoc(id) {
    if (isDirty() && !confirm('目前的修改還沒儲存，要放棄嗎？')) return;
    const r = await api('GET', '/api/doc/' + id);
    if (!r.ok) return toast((r.data.errors || ['讀取失敗']).join('、'), 'err');
    state.id = id; state.doc = r.data; state.saved = JSON.stringify(r.data);
    state.schema = id === '_platform' ? window.PLATFORM_SCHEMA : window.MODULE_SCHEMA;
    $('#docTitle').textContent = id === '_platform' ? '平台總覽（nexus.html 上方區塊）' : `${r.data.code} ${r.data.name_zh}`;
    $('#docMeta').textContent = id === '_platform' ? 'tools/module-pages/_platform.json' : `aurobase.com/${r.data.file}　·　tools/module-pages/${id}.json`;
    $('#openLive').href = '/site/' + (id === '_platform' ? 'nexus.html' : r.data.file);
    history.replaceState(null, '', '#' + id);
    renderForm(); state.saved = JSON.stringify(state.doc); // 表單會補齊空清單，補完才算原始狀態
    highlightNav(); refreshDirty(); preview(true);
  }

  // ── 表單 ──
  function renderForm() {
    const form = $('#form'); const y = form.scrollTop;
    form.innerHTML = '';
    state.schema.forEach((sec) => {
      const fs = document.createElement('fieldset');
      const lg = document.createElement('legend'); lg.textContent = sec.sec; fs.append(lg);
      if (sec.optional) {
        const on = state.doc[sec.optional] != null;
        const sw = document.createElement('label'); sw.className = 'switch';
        sw.innerHTML = `<input type="checkbox" ${on ? 'checked' : ''}> 這一頁要放${esc(sec.sec)}`;
        sw.querySelector('input').onchange = (e) => {
          if (e.target.checked) state.doc[sec.optional] = sec.optional === 'regulation'
            ? { heading: '', intro: '', cols: ['', ''], rows: [['', '']], sources: [{ name: '', url: '' }], note: '' }
            : { heading: '', intro: '', cols: ['', ''], rows: [['', '', '']] };
          else delete state.doc[sec.optional];
          changed(true);
        };
        fs.append(sw);
        if (!on) { form.append(fs); return; }
      }
      sec.fields.forEach((f) => fs.append(field(f, state.doc)));
      form.append(fs);
    });
    form.scrollTop = y;
  }

  function wrap(f, input) {
    const w = document.createElement('div'); w.className = 'field';
    const l = document.createElement('label'); l.className = 'lbl'; l.textContent = f.label; w.append(l, input);
    if (f.help) { const h = document.createElement('p'); h.className = 'help'; h.textContent = f.help; w.append(h); }
    return w;
  }

  // 搜尋結果的顯示寬度：中文字算 1，英數與半形標點算 0.5（與產生器的 disp_width 相同）
  const dispWidth = (t) => [...t].reduce((n, ch) => n + (ch.codePointAt(0) < 0x2E80 ? 0.5 : 1), 0);

  function counter(f, el, getText) {
    if (!f.max && !f.min) return null;
    const c = document.createElement('span'); c.className = 'count';
    const upd = () => {
      const t = getText().replace(/<[^>]+>/g, '');
      const n = f.width ? Math.round(dispWidth(t)) : t.length;
      c.textContent = `${n} ${f.width ? '格' : '字'}` + (f.max ? ` / 建議 ${f.min ? f.min + '～' : ''}${f.max}` : '');
      c.classList.toggle('warn', (f.max && n > f.max) || (f.min && n > 0 && n < f.min));
    };
    el.addEventListener('input', upd); upd(); return c;
  }

  function textInput(f, obj, key, multiline) {
    const el = document.createElement(multiline ? 'textarea' : 'input');
    if (!multiline) el.type = 'text';
    el.value = getp(obj, key) ?? '';
    el.oninput = () => { setp(obj, key, el.value); if (multiline) grow(el); changed(); };
    if (multiline) { el.rows = 2; requestAnimationFrame(() => grow(el)); }
    return el;
  }
  const grow = (el) => { el.style.height = 'auto'; el.style.height = el.scrollHeight + 2 + 'px'; };

  function options(f) {
    const src = typeof f.options === 'string' ? state.meta[f.options] : f.options;
    return src || [];
  }

  function field(f, obj) {
    const v = getp(obj, f.k);
    switch (f.type) {
      case 'str':
      case 'text': {
        const el = textInput(f, obj, f.k, f.type === 'text');
        const w = wrap(f, el); const c = counter(f, el, () => el.value); if (c) w.querySelector('.lbl').append(c);
        return w;
      }
      case 'readonly': {
        const el = document.createElement('p'); el.className = 'ro'; el.textContent = v || '（尚未儲存）';
        return wrap(f, el);
      }
      case 'bool': {
        const w = document.createElement('label'); w.className = 'switch';
        w.innerHTML = `<input type="checkbox" ${v ? 'checked' : ''}> ${esc(f.label)}`;
        w.querySelector('input').onchange = (e) => { if (e.target.checked) setp(obj, f.k, true); else delp(obj, f.k); changed(); };
        return w;
      }
      case 'tags': {
        const el = document.createElement('input'); el.type = 'text';
        el.value = (v || []).join('、');
        el.oninput = () => { setp(obj, f.k, el.value.split(/[、,，]\s*/).map((s) => s.trim()).filter(Boolean)); changed(); };
        const w = wrap(f, el); const h = document.createElement('p'); h.className = 'help'; h.textContent = (f.help ? f.help + ' ' : '') + '以頓號或逗號分隔。';
        w.querySelector('.help')?.remove(); w.append(h); return w;
      }
      case 'select': {
        const el = document.createElement('select');
        const opts = options(f); const cur = v ?? '';
        if (!opts.includes(cur)) el.append(new Option(cur ? `${cur}（不在清單）` : '（未選）', cur));
        opts.forEach((o) => el.append(new Option(o, o)));
        el.value = cur;
        el.onchange = () => { setp(obj, f.k, el.value); changed(); };
        return wrap(f, el);
      }
      case 'multi': {
        const box = document.createElement('div'); box.className = 'multi';
        const cur = new Set(v || []);
        options(f).forEach((o) => {
          const l = document.createElement('label');
          l.innerHTML = `<input type="checkbox" ${cur.has(o) ? 'checked' : ''}> ${esc(o.replace(/^nexus-/, ''))}`;
          l.querySelector('input').onchange = (e) => {
            const arr = (getp(obj, f.k) || []).filter((x) => x !== o);
            if (e.target.checked) arr.push(o);
            setp(obj, f.k, arr); changed();
          };
          box.append(l);
        });
        return wrap(f, box);
      }
      case 'color': {
        const box = document.createElement('div'); box.className = 'color';
        const pick = document.createElement('input'); pick.type = 'color';
        const txt = document.createElement('input'); txt.type = 'text'; txt.maxLength = 7;
        pick.value = txt.value = v || '#000000';
        pick.oninput = () => { txt.value = pick.value.toUpperCase(); setp(obj, f.k, txt.value); changed(); };
        txt.oninput = () => { if (/^#[0-9A-Fa-f]{6}$/.test(txt.value)) { pick.value = txt.value; setp(obj, f.k, txt.value.toUpperCase()); changed(); } };
        box.append(pick, txt); return wrap(f, box);
      }
      case 'list': return listField(f, obj, (arr, i) => {
        const el = document.createElement(f.item === 'text' ? 'textarea' : 'input');
        if (f.item !== 'text') el.type = 'text'; else { el.rows = 2; requestAnimationFrame(() => grow(el)); }
        el.value = arr[i] ?? '';
        el.oninput = () => { arr[i] = el.value; if (f.item === 'text') grow(el); changed(); };
        return el;
      }, () => '');
      case 'objlist': return listField(f, obj, (arr, i) => {
        const card = document.createElement('div'); card.className = 'obj';
        f.item.forEach((sf) => card.append(field(sf, arr[i])));
        return card;
      }, () => Object.fromEntries(f.item.map((sf) => [sf.k, sf.type === 'list' ? [''] : (sf.type === 'select' ? (options(sf)[0] || '') : '')])));
      case 'pairs': return listField(f, obj, (arr, i) => {
        const row = document.createElement('div'); row.className = 'pair';
        [0, 1].forEach((j) => {
          const el = document.createElement(j ? 'textarea' : 'input'); if (!j) el.type = 'text'; else el.rows = 1;
          el.placeholder = f.cols[j]; el.value = arr[i][j] ?? '';
          el.oninput = () => { arr[i][j] = el.value; changed(); };
          row.append(el);
        });
        return row;
      }, () => ['', '']);
      case 'rows': {
        const n = f.ncols(state.doc);
        return listField(f, obj, (arr, i) => {
          const row = document.createElement('div'); row.className = 'cells'; row.style.setProperty('--n', n);
          while (arr[i].length < n) arr[i].push('');
          if (arr[i].length > n) arr[i].length = n;
          for (let j = 0; j < n; j++) {
            const el = document.createElement('textarea'); el.rows = 2; el.value = arr[i][j] ?? '';
            el.oninput = () => { arr[i][j] = el.value; changed(); };
            row.append(el);
          }
          return row;
        }, () => Array(n).fill(''));
      }
      default: return wrap(f, document.createTextNode('（不支援的欄位類型）'));
    }
  }

  function listField(f, obj, renderItem, blank) {
    if (!Array.isArray(getp(obj, f.k))) setp(obj, f.k, []);
    const arr = getp(obj, f.k);
    const box = document.createElement('div'); box.className = 'list';
    arr.forEach((_, i) => {
      const item = document.createElement('div'); item.className = 'item';
      const tools = document.createElement('div'); tools.className = 'item-tools';
      tools.innerHTML = '<button type="button" title="上移">↑</button><button type="button" title="下移">↓</button><button type="button" title="刪除" class="del">✕</button>';
      const [up, down, del] = tools.querySelectorAll('button');
      up.disabled = i === 0; down.disabled = i === arr.length - 1;
      up.onclick = () => { [arr[i - 1], arr[i]] = [arr[i], arr[i - 1]]; changed(true); };
      down.onclick = () => { [arr[i + 1], arr[i]] = [arr[i], arr[i + 1]]; changed(true); };
      del.onclick = () => { arr.splice(i, 1); changed(true); };
      item.append(renderItem(arr, i), tools);
      box.append(item);
    });
    const add = document.createElement('button'); add.type = 'button'; add.className = 'btn-add'; add.textContent = '＋ 新增一項';
    add.onclick = () => { arr.push(blank()); changed(true); };
    box.append(add);
    return wrap(f, box);
  }

  // ── 變更、預覽、儲存 ──
  function changed(structural) {
    if (structural) renderForm();
    refreshDirty();
    clearTimeout(state.timer); state.timer = setTimeout(preview, 450);
  }
  function refreshDirty() {
    const d = isDirty();
    $('#dirty').hidden = !d;
    const blocked = state.errors.length && !(state.doc && state.doc.draft);
    $('#btnSave').disabled = !d || blocked;
    $('#btnSave').title = blocked ? '先修正上方的錯誤' : '';
  }

  async function preview(first) {
    if (!state.doc) return;
    const seq = ++state.seq;
    const r = await api('POST', '/api/preview/' + state.id, state.doc);
    if (seq !== state.seq) return; // 有更新的請求在路上
    state.errors = r.data.errors || []; state.warnings = r.data.warnings || [];
    state.audit = r.data.audit || null;
    showIssues(); refreshDirty(); renderSeo();
    const frame = $('#frame');
    let y = 0; try { y = frame.contentWindow.scrollY; } catch (e) { /* 首次載入 */ }
    frame.onload = () => {
      try {
        const w = frame.contentWindow;
        const loader = w.document.getElementById('ftco-loader'); if (loader) loader.classList.remove('show');
        if (!first) w.scrollTo(0, y);
      } catch (e) { /* ignore */ }
    };
    frame.srcdoc = r.data.html || '';
  }

  function showIssues() {
    const box = $('#issues');
    const e = state.errors; const w = state.warnings;
    if (!e.length && !w.length) { box.hidden = true; return; }
    box.hidden = false;
    box.innerHTML = (e.length ? `<p class="err-h">需要修正（${e.length}）${state.doc.draft ? '　草稿仍可儲存' : ''}</p><ul>${e.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>` : '')
      + (w.length ? `<p class="warn-h">建議（${w.length}）</p><ul class="warn">${w.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>` : '');
  }

  async function save() {
    $('#btnSave').disabled = true; $('#btnSave').textContent = '產頁中…';
    const r = await api('PUT', '/api/doc/' + state.id, state.doc);
    $('#btnSave').textContent = '儲存並產頁';
    if (!r.ok) {
      state.errors = r.data.errors || ['儲存失敗']; showIssues(); refreshDirty();
      return toast(r.data.saved ? '已存檔，但整站產頁被其他頁面的錯誤擋下' : '沒有儲存：請先修正錯誤', 'err', 6000);
    }
    const id = state.id; state.saved = '';
    state.doc = null; await loadMeta(); await openDoc(id);
    const parts = [`已產生 ${r.data.written.length} 個檔案`];
    if (r.data.removed.length) parts.push(`移除 ${r.data.removed.join('、')}`);
    if (r.data.font) parts.push(r.data.font);
    toast(parts.join('；'));
  }

  // ── SEO / GEO 面板 ──
  const ICONS = { pass: '✓', warn: '△', fail: '✗', info: 'ℹ' };
  function renderSeo() {
    const a = state.audit; const badge = $('#seoBadge');
    if (!a) { badge.textContent = ''; return; }
    const bad = a.checks.filter((c) => c.status === 'fail' || c.status === 'warn').length;
    badge.textContent = bad ? String(bad) : '✓';
    badge.className = bad ? (a.checks.some((c) => c.status === 'fail') ? 'b-fail' : 'b-warn') : 'b-pass';
    const panel = $('#seoPanel');
    if (panel.hidden) return;
    const keepQ = panel.querySelector('#kwInput')?.value;
    const keepOut = panel.querySelector('#kwOut')?.innerHTML || '';
    const groups = ['SEO', 'GEO', '全站'];
    const kw = ((state.doc.keywords || []).filter((k) => k !== 'AURO NEXUS')[0]) || state.doc.code || '';
    panel.innerHTML = `
      <div class="scores">${groups.map((g) => { const [p, t] = a.score[g] || [0, 0];
        return `<div class="score ${p === t ? 'full' : ''}"><b>${p}<small>/${t}</small></b><span>${g}</span></div>`; }).join('')}</div>
      <section class="serp" aria-label="搜尋結果預覽">
        <p class="serp-h">Google 搜尋結果預覽</p>
        <div class="serp-url">${esc(a.serp.url)}</div>
        <div class="serp-title">${esc(cut(a.serp.title, 32))}</div>
        <div class="serp-desc">${esc(cut(a.serp.description, 78))}</div>
      </section>
      ${groups.map((g) => `<section class="checks"><h3>${g}</h3><ul>${a.checks.filter((c) => c.group === g).map((c) =>
        `<li class="c-${c.status}"><i>${ICONS[c.status]}</i><div><b>${esc(c.label)}</b>${c.detail ? `<span>${esc(c.detail)}</span>` : ''}</div></li>`).join('')}</ul></section>`).join('')}
      <section class="kwtool">
        <h3>找關鍵字與常見問法（Google 台灣搜尋建議）</h3>
        <div class="kw-row"><input id="kwInput" type="text" value="${esc(keepQ ?? kw)}" aria-label="種子關鍵字">
          <button type="button" data-mode="keywords">搜尋建議</button><button type="button" data-mode="questions">常見問法</button></div>
        <p class="help">點「搜尋建議」的結果會加進目標關鍵字；點「常見問法」的結果會新增一題常見問題（回答再自己寫）。</p>
        <div id="kwOut" class="chips">${keepOut}</div>
      </section>
      ${a.llms ? `<section><h3>llms.txt 裡的這一行</h3><pre>${esc(a.llms)}</pre></section>` : ''}
      ${a.jsonld ? `<details><summary>結構化資料（JSON-LD）</summary><pre>${esc(a.jsonld)}</pre></details>` : ''}`;
    panel.querySelectorAll('.kw-row button').forEach((b) => b.onclick = () => lookup(b.dataset.mode));
    panel.querySelectorAll('#kwOut button').forEach(bindChip);
  }
  // 依顯示寬度截斷，模擬搜尋結果的「…」
  function cut(t, max) { let w = 0; let out = ''; for (const ch of t) { w += ch.codePointAt(0) < 0x2E80 ? 0.5 : 1; if (w > max) return out + ' …'; out += ch; } return out; }

  async function lookup(mode) {
    const q = $('#kwInput').value.trim(); const out = $('#kwOut');
    out.innerHTML = '<span class="help">查詢中…</span>';
    const r = await api('GET', `/api/suggest?mode=${mode}&q=${encodeURIComponent(q)}`);
    if (!r.ok) { out.innerHTML = `<span class="help">${esc((r.data.errors || ['查詢失敗']).join('、'))}</span>`; return; }
    out.innerHTML = r.data.suggestions.map((x) => `<button type="button" data-mode="${mode}" data-v="${esc(x)}">${esc(x)}</button>`).join('');
    out.querySelectorAll('button').forEach(bindChip);
  }
  function bindChip(b) {
    const v = b.dataset.v; const doc = state.doc;
    const has = b.dataset.mode === 'keywords' ? (doc.keywords || []).includes(v) : (doc.faq || []).some((f) => f.q.startsWith(v));
    b.classList.toggle('on', has);
    b.onclick = () => {
      if (b.dataset.mode === 'keywords') {
        doc.keywords = doc.keywords || [];
        if (doc.keywords.includes(v)) doc.keywords = doc.keywords.filter((k) => k !== v);
        else {
          // 新關鍵字放在品牌詞「AURO NEXUS」之前（品牌詞固定排最後）
          const brand = doc.keywords.indexOf('AURO NEXUS');
          doc.keywords.splice(brand === -1 ? doc.keywords.length : brand, 0, v);
        }
      } else {
        doc.faq = doc.faq || [];
        if (!has) doc.faq.push({ q: /[？?]$/.test(v) ? v : v + '？', a: '' });
      }
      changed(true);
      toast(b.dataset.mode === 'keywords' ? '已更新目標關鍵字' : '已新增一題常見問題，記得寫回答', 'ok', 2200);
    };
  }

  // ── 新增產品精靈 ──
  function openWizard() {
    const dlg = $('#wizard'); const f = $('#wizForm');
    f.reset(); $('#wizErr').textContent = '';
    const sel = f.platform_leg; sel.innerHTML = '';
    state.meta.legs.forEach((l) => sel.append(new Option(l, l)));
    let touched = false;
    f.slug.oninput = () => { touched = true; $('[data-slug]').textContent = f.slug.value || 'nexus-…'; };
    f.code.oninput = () => {
      if (touched) return;
      const s = f.code.value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
      f.slug.value = s ? 'nexus-' + s.replace(/^nexus-/, '') : '';
      $('[data-slug]').textContent = f.slug.value || 'nexus-…';
    };
    dlg.showModal();
  }
  async function submitWizard(e) {
    e.preventDefault();
    const f = $('#wizForm');
    if (!f.reportValidity()) return;
    const body = Object.fromEntries(new FormData(f).entries());
    const r = await api('POST', '/api/new', body);
    if (!r.ok) { $('#wizErr').textContent = (r.data.errors || ['建立失敗']).join('、'); return; }
    $('#wizard').close();
    await loadMeta(); state.doc = null; await openDoc(r.data.slug);
    toast('草稿已建立：逐欄填完、取消「草稿」後儲存就會發布');
  }

  // ── 啟動 ──
  // 桌機預覽以 1440px 寬渲染再等比縮小，網站才會是桌機版排版
  function fitFrame() {
    const wrap = $('.frame-wrap'); const frame = $('#frame');
    if (wrap.classList.contains('mobile')) { frame.style.cssText = ''; return; }
    const k = Math.min(1, wrap.clientWidth / 1440);
    frame.style.flex = 'none'; frame.style.width = '1440px'; frame.style.height = (wrap.clientHeight / k) + 'px';
    frame.style.transform = `scale(${k})`; frame.style.transformOrigin = '0 0';
  }
  window.addEventListener('resize', fitFrame);
  document.querySelectorAll('#devSeg button').forEach((b) => b.onclick = () => {
    document.querySelectorAll('#devSeg button').forEach((x) => x.classList.toggle('on', x === b));
    $('.frame-wrap').classList.toggle('mobile', b.dataset.w === 'mobile');
    fitFrame();
  });
  document.querySelectorAll('#viewTabs button').forEach((b) => b.onclick = () => {
    document.querySelectorAll('#viewTabs button').forEach((x) => x.classList.toggle('on', x === b));
    const seo = b.dataset.view === 'seo';
    $('#seoPanel').hidden = !seo; $('.frame-wrap').hidden = seo; $('#devSeg').hidden = seo;
    if (seo) renderSeo(); else fitFrame();
  });
  fitFrame();
  $('#btnSave').onclick = save;
  $('#btnNew').onclick = openWizard;
  $('#wizOk').onclick = submitWizard;
  $('#wizCancel').onclick = () => $('#wizard').close();
  document.addEventListener('keydown', (e) => { if ((e.metaKey || e.ctrlKey) && e.key === 's') { e.preventDefault(); if (!$('#btnSave').disabled) save(); } });
  window.addEventListener('beforeunload', (e) => { if (isDirty()) { e.preventDefault(); e.returnValue = ''; } });

  loadMeta().then(() => openDoc(decodeURIComponent(location.hash.slice(1)) || '_platform'));
})();
