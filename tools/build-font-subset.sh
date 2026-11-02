#!/usr/bin/env bash
# 重建 LINE Seed TW 子集字型，並由 cmap 重寫子集與完整檔的 unicode-range
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
import glob
site = set()
for f in glob.glob('*.html') + glob.glob('blogpost/*.html') + glob.glob('*.txt') \
       + glob.glob('css/*.css') + glob.glob('js/*.js') + glob.glob('search-index.json'):
    site |= set(ord(c) for c in io.open(f, encoding='utf-8', errors='ignore').read())

def unicode_range(path, gap=1):
    """由字型的 cmap 產生 unicode-range。gap > 1 時把相距不到 gap 的段落併起來讓 CSS 變短，
    但站上用到、字型卻沒有的字一律切出去，不讓 range 宣稱有這個字。"""
    cm = set(TTFont(path).getBestCmap())
    order = sorted(cm)
    ranges = [[order[0], order[0]]]
    for cp in order[1:]:
        if cp - ranges[-1][1] <= gap:
            ranges[-1][1] = cp
        else:
            ranges.append([cp, cp])
    out = []
    for a, b in ranges:
        for hole in sorted(c for c in site if a <= c <= b and c not in cm):
            if hole > a:
                out.append((a, hole - 1))
            a = hole + 1
        if a <= b:
            out.append((a, b))
    return ','.join('U+%X' % a if a == b else 'U+%X-%X' % (a, b) for a, b in out), len(cm), len(out)

# 子集與完整檔都要宣告 unicode-range，而且都由字型實際的 cmap 產生。
# 完整檔若沒宣告，瀏覽器會把它當成「什麼字都有」：網頁出現兩支檔案都沒有的符號（例如選單的 ⌕ ▾）時，
# 每一頁都會為了找這個字多下載 3.3 MB。完整檔的 range 併段縮短，CSS 才不會多出 70 KB。
for name, gap in (('Rg.subset', 1), ('Bd.subset', 1), ('Rg', 64), ('Bd', 64), ('Th', 64), ('Eb', 64)):
    ur, nchar, nrange = unicode_range('WOFF2/LINESeedTW_OTF_%s.woff2' % name, gap)
    src = r"src: url\('\.\./WOFF2/LINESeedTW_OTF_%s\.woff2'\) format\('woff2'\);" % re.escape(name)
    css, n = re.subn('(' + src + r')(\n  unicode-range: [^;]+;)?', lambda m: m.group(1) + '\n  unicode-range: ' + ur + ';', css)
    assert n == 1, '%s 的 @font-face 沒找到' % name
    print('%s 含 %d 字 / %d 段 range' % (name, nchar, nrange))
io.open(p, 'w', encoding='utf-8').write(css)
PY

ls -la WOFF2/LINESeedTW_OTF_*.subset.woff2
