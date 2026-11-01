#!/usr/bin/env node
// 用網站上同一份搜尋程式（js/site-search.js）跑模擬客戶考題，印出命中率與答錯的題目。
//   node tools/search-eval/run.js            # 低於門檻時結束碼為 1（GitHub Action 會擋下發布）
//   node tools/search-eval/run.js --verbose  # 列出每一題的前三名
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..', '..');
const S = require(path.join(root, 'js', 'site-search.js'));
const idx = JSON.parse(fs.readFileSync(path.join(root, 'search-index.json'), 'utf8'))
  .map((e) => Object.assign({}, e, { k: S.norm(e.k), s: S.norm(e.s) }));
const exam = JSON.parse(fs.readFileSync(path.join(__dirname, 'queries.json'), 'utf8'));
const TOP3_MIN = 0.95, TOP1_MIN = 0.85;
const verbose = process.argv.includes('--verbose');

let n = 0, top1 = 0, top3 = 0;
const misses = [];
for (const [persona, qs] of Object.entries(exam.personas)) {
  for (const [q, expect] of qs) {
    const res = S.rank(q, idx).slice(0, 3).map((r) => idx[r.i].u);
    n++;
    if (expect.includes(res[0])) top1++;
    if (res.some((u) => expect.includes(u))) top3++;
    else misses.push(`  ✗ [${persona}] ${q}\n      期望 ${expect.join(' / ')}\n      得到 ${res.join(' / ') || '（無結果）'}`);
    if (verbose) console.log(`${expect.includes(res[0]) ? '✓' : res.some((u) => expect.includes(u)) ? '△' : '✗'} ${q} → ${res.join(' / ')}`);
  }
}
const noise = exam.no_match.filter((q) => S.rank(q, idx).length);
const r1 = top1 / n, r3 = top3 / n;
console.log(`模擬客戶考題 ${n} 題：前三名命中 ${(r3 * 100).toFixed(1)}%（門檻 ${TOP3_MIN * 100}%），第一名命中 ${(r1 * 100).toFixed(1)}%（門檻 ${TOP1_MIN * 100}%）`);
if (misses.length) console.log('前三名沒有正確答案的題目：\n' + misses.join('\n'));
if (noise.length) console.log('不相關的問題卻有結果：' + noise.join('、'));
process.exit(r3 >= TOP3_MIN && r1 >= TOP1_MIN && !noise.length ? 0 : 1);
