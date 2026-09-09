#!/usr/bin/env bash
# 重建 css/iconoir-subset.css —— 只保留站上實際使用的 iconoir 圖示。
#
# 何時要跑：頁面新增或改用了新的 iconoir 圖示之後。
# 若引用了子集裡沒有的圖示，該圖示會不顯示（mask 為 none），不會整頁壞掉。
# 腳本結束會列出「頁面有引用但 iconoir 沒有」的名稱，可用來抓錯字。
set -euo pipefail
cd "$(dirname "$0")/.."

curl -fsS https://cdn.jsdelivr.net/gh/iconoir-icons/iconoir@main/css/iconoir.css -o /tmp/iconoir-full.css

python3 - <<'PY'
import re, io, glob
css = io.open('/tmp/iconoir-full.css', encoding='utf-8').read()

used = set()
for f in glob.glob('*.html') + glob.glob('blogpost/*.html'):
    used |= set(re.findall(r'iconoir-[a-z0-9-]+', io.open(f, encoding='utf-8').read()))
used.discard('iconoir-icons')      # class 名稱片段，不是圖示
used.discard('iconoir-subset')     # 本檔檔名

head = css[:css.index('*[class^=')]
m = re.search(r"\*\[class\^='iconoir-'\]::before,\s*\*\[class\*=' iconoir-'\]::before\s*\{[^}]*\}", css, re.S)
assert m, '找不到 iconoir 基礎規則，上游格式可能變了'

out = [head.rstrip(),
       '\n/* 本檔為 iconoir 子集：只保留本站實際使用的圖示。\n'
       '   重建：tools/build-iconoir-subset.sh */\n',
       m.group(0), '']
found = set()
for name in sorted(used):
    r = re.search(r"\.%s::before\s*\{[^}]*\}" % re.escape(name), css, re.S)
    if r:
        out.append(r.group(0)); found.add(name)

io.open('css/iconoir-subset.css', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('抽出 %d 個圖示' % len(found))
missing = sorted(used - found)
if missing:
    print('⚠ 頁面有引用但 iconoir 沒有這些名稱（可能是錯字）：', ', '.join(missing))
PY

ls -la css/iconoir-subset.css
