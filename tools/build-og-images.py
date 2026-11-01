#!/usr/bin/env python3
"""產生每一頁的社群分享圖（Open Graph，1200×630 JPEG），放在 images/og/。

    python3 tools/build-og-images.py          # 只重畫內容有變的圖
    python3 tools/build-og-images.py --all    # 全部重畫

用 Chrome 無頭模式截圖，字型取自 WOFF2/ 的 LINE Seed，本機與 GitHub Action 畫出來一樣。
找不到 Chrome 時不做任何事（頁面會沿用 images/og/default.png）。
內容來源：產品與解決方案取自產品 JSON；平台總覽取自 _platform.json；其他頁面取自 _pages.json 的 og_card。
"""
import hashlib
import html
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
OUT = os.path.join(ROOT, 'images', 'og')
MANIFEST = os.path.join(OUT, 'manifest.json')
VERSION = '2'   # 改版面時加一，所有圖都會重畫

spec = importlib.util.spec_from_file_location('gen', os.path.join(HERE, 'build-module-pages.py'))
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

DEFAULT_THEME = {'deep': '#B8320F', 'bright': '#E63109', 'soft': '#F59A7E', 'ink1': '#140906', 'ink2': '#26100A'}

TEMPLATE = '''<!DOCTYPE html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><style>
@font-face {{ font-family: Seed; src: url("{font_rg}") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: Seed; src: url("{font_bd}") format("woff2"); font-weight: 700; }}
* {{ margin: 0; box-sizing: border-box; }}
html, body {{ width: 1200px; height: 630px; overflow: hidden; }}
body {{ font-family: Seed, sans-serif; color: #fff; padding: 72px 84px;
  background: radial-gradient(circle at 85% 15%, {bright}55 0, transparent 45%), linear-gradient(135deg, {ink1} 0%, {ink2} 55%, {deep} 140%);
  display: flex; flex-direction: column; }}
.kicker {{ font-size: 26px; letter-spacing: 0.08em; color: {soft}; font-weight: 700; }}
.title {{ font-size: {title_size}px; font-weight: 700; line-height: 1.1; margin-top: 26px; letter-spacing: -0.01em; }}
.sub {{ font-size: 40px; font-weight: 700; margin-top: 14px; color: rgba(255,255,255,0.92); }}
.tag {{ font-size: 30px; line-height: 1.55; margin-top: 30px; color: rgba(255,255,255,0.78); max-width: 980px; }}
.foot {{ margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end; font-size: 24px; color: rgba(255,255,255,0.7); }}
.brand {{ font-weight: 700; font-size: 30px; color: #fff; letter-spacing: 0.04em; }}
.bar {{ position: absolute; left: 0; top: 0; bottom: 0; width: 14px; background: {bright}; }}
</style></head><body><div class="bar"></div>
<div class="kicker">{kicker}</div>
<div class="title">{title}</div>
{sub}
{tag}
<div class="foot"><span class="brand">奧洛 Aurobase</span><span>aurobase.com</span></div>
</body></html>'''


def text(s):
    return html.escape(re.sub(r'\s+', ' ', gen.plain(re.sub(r'<br\s*/?>', '', s or ''))).strip())


def cards():
    """回傳 {圖檔名: 卡片內容}。圖檔名與 build-module-pages.py 的 og_key() 一致。"""
    out = {}
    for m in gen.load_modules().values():
        sol = gen.is_solution(m)
        out[m['slug']] = {
            'kicker': ('AURO NEXUS 產業解決方案 · ' + m['industry']) if sol else 'AURO NEXUS 產品家族',
            'title': m['code'] if m['code'] not in m['name_zh'] else m['name_zh'],
            'sub': '' if m['code'] in m['name_zh'] else m['name_zh'],
            'tag': m['hero'].get('slogan', ''),
            'theme': m['theme'],
        }
    pf = gen.load_platform()
    out['nexus'] = {'kicker': 'AURO NEXUS', 'title': 'AI 治理平台', 'sub': '可雲・可地・可客製', 'tag': pf.get('slogan', ''),
                    'theme': {'deep': '#2B3A8C', 'bright': '#4659C9', 'soft': '#8FA0F0', 'ink1': '#0C0F1F', 'ink2': '#141A35'}}
    for rel, cfg in gen.load_pages_cfg().items():
        c = cfg.get('og_card')
        if c:
            out[gen.og_key(rel)] = dict(c, theme=c.get('theme', DEFAULT_THEME))
    for rel, cfg in gen.load_pages_cfg().items():
        if cfg.get('type') == 'BlogPosting':
            page = gen.read(os.path.join(ROOT, rel))
            img = re.search(r'<meta name="article-image" content="\.\./([^"]+)"', page) or re.search(r'src="\.\./(images/image_[^"]+)"', page)
            if img:
                out[gen.og_key(rel)] = {'photo': img.group(1)}
    out['default'] = {'kicker': 'AI 治理平台・數位行銷・行銷科技', 'title': '奧洛 Aurobase',
                      'sub': '', 'tag': '讓企業在自有環境裡導入 AI，並保留可稽核的證據。', 'theme': DEFAULT_THEME}
    return out


def chrome():
    for c in (os.environ.get('CHROME'), '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
              shutil.which('google-chrome'), shutil.which('google-chrome-stable'), shutil.which('chromium'), shutil.which('chromium-browser')):
        if c and os.path.exists(c):
            return c
    return None


def crop_photo(src, dest):
    """新聞文章用自己的配圖：等比放大後置中裁成 1200×630。"""
    from PIL import Image
    im = Image.open(os.path.join(ROOT, src)).convert('RGB')
    r = max(1200 / im.width, 630 / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - 1200) // 2, (im.height - 630) // 2
    im.crop((x, y, x + 1200, y + 630)).save(dest, 'JPEG', quality=86, optimize=True, progressive=True)


def render(exe, card, dest):
    t = dict(DEFAULT_THEME, **card['theme'])
    title = text(card['title'])
    page = TEMPLATE.format(
        font_rg='file://' + os.path.join(ROOT, 'WOFF2', 'LINESeedTW_OTF_Rg.woff2'),
        font_bd='file://' + os.path.join(ROOT, 'WOFF2', 'LINESeedTW_OTF_Bd.woff2'),
        kicker=text(card['kicker']), title=title, title_size=96 if len(title) <= 12 else 76,
        sub='<div class="sub">%s</div>' % text(card['sub']) if card.get('sub') else '',
        tag='<div class="tag">%s</div>' % text(card['tag']) if card.get('tag') else '',
        **{k: t[k] for k in ('deep', 'bright', 'soft', 'ink1', 'ink2')})
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, 'card.html')
        with open(src, 'w', encoding='utf-8') as f:
            f.write(page)
        shot = os.path.join(tmp, 'card.png')
        subprocess.run([exe, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-sandbox',
                        '--force-device-scale-factor=1', '--window-size=1200,630', '--virtual-time-budget=3000',
                        '--screenshot=' + shot, 'file://' + src], check=True, capture_output=True, timeout=60)
        # 存成 JPEG：社群平台都支援，檔案約 PNG 的四分之一
        from PIL import Image
        Image.open(shot).convert('RGB').save(dest, 'JPEG', quality=86, optimize=True, progressive=True)


def main():
    exe = chrome()
    if not exe:
        print('找不到 Chrome，略過分享圖')
        return
    os.makedirs(OUT, exist_ok=True)
    seen = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    done = {}
    for key, card in sorted(cards().items()):
        h = hashlib.sha1((VERSION + json.dumps(card, ensure_ascii=False, sort_keys=True)).encode()).hexdigest()[:12]
        dest = os.path.join(OUT, key + '.jpg')
        done[key] = h
        if '--all' not in sys.argv and seen.get(key) == h and os.path.exists(dest):
            continue
        if card.get('photo'):
            # 用配圖的內容雜湊判斷要不要重裁（檔案時間在每次 checkout 都不同，不能用）
            with open(os.path.join(ROOT, card['photo']), 'rb') as f:
                h = hashlib.sha1(h.encode() + f.read()).hexdigest()[:12]
            done[key] = h
            if '--all' not in sys.argv and seen.get(key) == h and os.path.exists(dest):
                continue
            crop_photo(card['photo'], dest)
        else:
            render(exe, card, dest)
        print('畫好', os.path.relpath(dest, ROOT))
    for key in set(seen) - set(done):
        p = os.path.join(OUT, key + '.jpg')
        if os.path.exists(p):
            os.remove(p)
            print('移除', os.path.relpath(p, ROOT))
    with open(MANIFEST, 'w', encoding='utf-8') as f:
        json.dump(done, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')


if __name__ == '__main__':
    main()
