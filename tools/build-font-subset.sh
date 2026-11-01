#!/usr/bin/env bash
# 重建 LINE Seed TW Regular 子集字型 + 對應的 unicode-range
#
# 何時要跑：新增/修改頁面文字之後（尤其是新增部落格文章）。
# 沒跑也不會壞——子集沒涵蓋的字會自動 fallback 去載完整的 3.3 MB 檔，
# 只是那次載入會變重。
#
# 需求：pip install fonttools brotli
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - <<'PY'
import glob, io
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
io.open('/tmp/subset_chars.txt', 'w', encoding='utf-8').write(''.join(sorted(chars | extra)))
print('掃描到 %d 個不重複字元（站上實際用字 %d）' % (len(chars | extra), len(chars)))
PY

for W in Rg Bd; do
  pyftsubset "WOFF2/LINESeedTW_OTF_$W.woff2" \
    --text-file=/tmp/subset_chars.txt --flavor=woff2 \
    --layout-features='' --no-hinting --desubroutinize \
    --output-file="WOFF2/LINESeedTW_OTF_$W.subset.woff2"
done

python3 - <<'PY'
import io, re
from fontTools.ttLib import TTFont
p = 'css/line-seed-font.css'
css = io.open(p, encoding='utf-8').read()
for W in ('Rg', 'Bd'):
    cm = sorted(TTFont('WOFF2/LINESeedTW_OTF_%s.subset.woff2' % W).getBestCmap().keys())
    ranges, s, e = [], cm[0], cm[0]
    for cp in cm[1:]:
        if cp == e + 1:
            e = cp
        else:
            ranges.append((s, e)); s = e = cp
    ranges.append((s, e))
    ur = ','.join('U+%X' % a if a == b else 'U+%X-%X' % (a, b) for a, b in ranges)
    css, n = re.subn(
        r"(src: url\('\.\./WOFF2/LINESeedTW_OTF_%s\.subset\.woff2'\) format\('woff2'\);\n  unicode-range: )[^;]+;" % W,
        lambda m: m.group(1) + ur + ';', css)
    assert n == 1, '%s 的 unicode-range 區塊沒找到' % W
    print('%s 子集含 %d 字 / %d 段 range' % (W, len(cm), len(ranges)))
io.open(p, 'w', encoding='utf-8').write(css)
PY

ls -la WOFF2/LINESeedTW_OTF_*.subset.woff2
