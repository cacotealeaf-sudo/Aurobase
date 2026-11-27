#!/usr/bin/env bash
# 重建宙黑體 F 版（Zev Hei TC）網站子集，並由子集的 cmap 重寫 css/fonts.css 的 unicode-range
#
# 何時要跑：新增/修改頁面文字之後（尤其是新增部落格文章）。CI 發現站上有子集沒有的字時會自動跑。
# 沒跑也不會壞：子集沒有的字會用系統字（蘋方／正黑）顯示，不會去下載完整字型。
#
# 來源：tools/fonts/ZevHeiTC-F-VF.woff2（完整字集，可變字型 wght 300–900，不發布）
# 需求：pip install fonttools brotli
set -euo pipefail
cd "$(dirname "$0")/.."

SRC=tools/fonts/ZevHeiTC-F-VF.woff2
OUT=WOFF2/ZevHeiTC-F.subset.woff2
CHARS=$(mktemp)
trap 'rm -f "$CHARS"' EXIT

python3 - "$CHARS" <<'PY'
import glob, io, sys
chars = set()
for f in glob.glob('*.html') + glob.glob('blogpost/*.html') + glob.glob('*.txt') \
       + glob.glob('css/*.css') + glob.glob('js/*.js') + glob.glob('search-index.json'):
    try:
        chars |= set(io.open(f, encoding='utf-8', errors='ignore').read())
    except Exception:
        pass
extra  = set(chr(c) for c in range(0x20, 0x7F))
extra |= set(chr(c) for c in range(0x2000, 0x206F))   # 一般標點
extra |= set(chr(c) for c in range(0x3000, 0x3040))   # CJK 標點 / 注音
extra |= set(chr(c) for c in range(0xFF00, 0xFFF0))   # 全形
extra |= set('©®™°±×÷—–…‧・※§¶€$¥£¢№←→↑↓✓✔✗●○■□▲△★☆')
io.open(sys.argv[1], 'w', encoding='utf-8').write(''.join(sorted(chars | extra)))
print('掃描到 %d 個不重複字元（站上實際用字 %d）' % (len(chars | extra), len(chars)))
PY

# kern/liga/calt 給拉丁字（Mona Sans）用；name 表整份保留，OFL 要求授權資訊跟著字型走
pyftsubset "$SRC" \
  --text-file="$CHARS" --flavor=woff2 \
  --layout-features=kern,liga,calt,ccmp,locl --no-hinting --desubroutinize \
  --name-IDs='*' --name-languages='*' \
  --output-file="$OUT"

python3 - "$OUT" <<'PY'
import io, os, re, sys
from fontTools.ttLib import TTFont
path = sys.argv[1]
cm = sorted(TTFont(path).getBestCmap())
ranges = [[cm[0], cm[0]]]
for cp in cm[1:]:
    if cp == ranges[-1][1] + 1:
        ranges[-1][1] = cp
    else:
        ranges.append([cp, cp])
ur = ','.join('U+%X' % a if a == b else 'U+%X-%X' % (a, b) for a, b in ranges)
p = 'css/fonts.css'
css = io.open(p, encoding='utf-8').read()
src = r"src: url\('\.\./WOFF2/ZevHeiTC-F\.subset\.woff2'\) format\('woff2'\);"
css, n = re.subn('(' + src + r')(\n  unicode-range: [^;]+;)?', lambda m: m.group(1) + '\n  unicode-range: ' + ur + ';', css)
assert n == 1, 'css/fonts.css 裡找不到 ZevHeiTC-F.subset.woff2 的 @font-face'
io.open(p, 'w', encoding='utf-8').write(css)
print('子集 %d 字 / %d 段 range / %d KB' % (len(cm), len(ranges), os.path.getsize(path) // 1024))
PY
