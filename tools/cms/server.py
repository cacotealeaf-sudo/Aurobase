#!/usr/bin/env python3
"""AURO NEXUS 產品頁編輯器（本機用）。

    python3 tools/cms/server.py            # 開 http://127.0.0.1:8899

表單改文案、即時預覽、新增產品精靈；按「儲存」會寫回 tools/module-pages/*.json，
並跑 tools/build-module-pages.py 重新產頁（與字型子集）。只聽 127.0.0.1，不對外。
發布仍走 git：commit 後 push 到 main，GitHub Action 會再產一次頁並觸發 Pages 建置。
"""
import argparse
import copy
import importlib.util
import io
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))


def load_generator():
    spec = importlib.util.spec_from_file_location('build_module_pages', os.path.join(HERE, '..', 'build-module-pages.py'))
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    return g


gen = load_generator()

# 新產品的起始內容：結構齊全、文字留空，存成草稿後再逐欄填。
TEMPLATE = {
    'slug': '', 'file': '', 'code': '', 'name_zh': '', 'leg': '', 'draft': True,
    'title': '', 'description': '', 'keywords': [], 'eyebrow': '', 'updated': '',
    'inquiry_chip': 'NEXUS AI 自動化平台',
    'theme': {},
    'hero': {'h1': '', 'slogan': '', 'sub': '', 'tagline': '', 'badges': []},
    'summary': [['是什麼', ''], ['所屬', '']],
    'definition': {'q': '', 'a': ['', '']},
    'audience': [{'who': '', 'why': ''}],
    'pain': {'heading': '', 'intro': '', 'cards': [{'title': '', 'text': ''} for _ in range(3)], 'statement': ''},
    'capabilities': {'heading': '核心能力', 'intro': '', 'cards': [{'icon': 'shield-check', 'title': '', 'items': ['']}]},
    'diff': {'heading': '差異點', 'cards': [{'icon': 'shield-check', 'title': '', 'text': ''}]},
    'platform': {'heading': '在 AURO NEXUS 平台上的位置', 'text': '', 'related': ['nexus-forge']},
    'deploy': [{'tag': '', 'title': '', 'text': ''}],
    'faq': [{'q': '', 'a': ''}],
    'cta': {'heading': '', 'text': ''},
}


def json_dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + '\n'


def doc_path(doc_id):
    if doc_id != '_platform' and not gen.SLUG_RE.match(doc_id):
        raise ValueError('不合法的頁面代號')
    return os.path.join(gen.SRC, doc_id + '.json')


def git_dirty():
    try:
        out = subprocess.run(['git', 'status', '--short'], cwd=gen.ROOT, capture_output=True, text=True, timeout=10).stdout
        return [l for l in out.splitlines() if l.strip()]
    except Exception:
        return []


def rebuild_fonts():
    if os.environ.get('CMS_SKIP_FONTS'):
        return '略過字型子集（CMS_SKIP_FONTS）'
    if not shutil.which('pyftsubset'):
        return '本機沒有 pyftsubset，字型子集留給 GitHub Action 重建（新字暫時會載入完整字型）'
    r = subprocess.run(['bash', os.path.join(gen.ROOT, 'tools', 'build-font-subset.sh')],
                       cwd=gen.ROOT, capture_output=True, text=True, timeout=180)
    return '字型子集已重建' if r.returncode == 0 else '字型子集重建失敗：' + r.stderr[-300:]


GTM_RE = re.compile(r'<!-- Google Tag Manager -->\s*<script>.*?</script>|<noscript><iframe src="https://www\.googletagmanager\.com.*?</noscript>', re.S)


REL_URL_RE = re.compile(r'\b(href|src)="(?!https?:|//|#|/|mailto:|tel:|data:|javascript:)')


def with_base(html_text):
    # 預覽以 srcdoc 顯示：相對路徑改從 /site/ 取（Chrome 的預先載入不一定套用 <base>，所以直接改寫屬性）；
    # 拿掉 GTM，本機預覽不送流量統計
    html_text = REL_URL_RE.sub(lambda m: '%s="/site/' % m.group(1), GTM_RE.sub('', html_text))
    return html_text.replace('<head>', '<head>\n    <base href="/site/">', 1)


def state():
    allm = gen.load_modules(include_drafts=True)
    pf = gen.load_platform()
    return {
        'modules': [{'slug': s, 'code': m.get('code') or s, 'name_zh': m.get('name_zh', ''), 'file': m.get('file'),
                     'draft': bool(m.get('draft')), 'updated': m.get('updated', ''), 'kind': m.get('kind', 'product')}
                    for s, m in sorted(allm.items(), key=lambda kv: kv[1].get('code', kv[0]).lower())],
        'legs': [lg['name'] for lg in pf['legs']],
        'industries': sorted({m['industry'] for m in allm.values() if m.get('industry')}),
        'related_options': sorted(set(allm) | set(pf.get('extra_modules', {}))),
        'chips': gen.inquiry_chips(),
        'icons': sorted(gen.available_icons()),
        'git_dirty': git_dirty(),
    }


def preview(doc_id, body):
    if doc_id == '_platform':
        mods = gen.load_modules()
        errors = gen.validate_platform(body, mods)
        return {'html': with_base(gen.build_overview(mods, body, write=False)), 'errors': errors, 'warnings': [],
                'audit': gen.audit_platform(body)}
    mods = gen.load_modules()
    pf = gen.load_platform()
    m = copy.deepcopy(body)
    errors, warnings = gen.validate(m, mods, pf)
    mods = dict(mods)
    mods[m['slug']] = m
    try:
        page = gen.render_module(m, mods)
    except Exception as e:  # 欄位還沒填完時，渲染可能失敗；錯誤清單已說明缺什麼
        page = '<!doctype html><meta charset="utf-8"><body style="font:15px sans-serif;padding:2rem;color:#555">' \
               '預覽暫時無法產生：%s</body>' % gen.html.escape(repr(e))
    return {'html': with_base(page), 'errors': errors, 'warnings': warnings, 'audit': gen.audit(m, mods, pf)}


SUGGEST_URL = 'https://suggestqueries.google.com/complete/search?client=firefox&hl=zh-TW&gl=tw&ie=utf-8&oe=utf-8&q='
QUESTION_PATTERNS = ['{q}', '{q} 是什麼', '什麼是 {q}', '{q} 推薦', '{q} 比較', '{q} 費用', '{q} 導入', '{q} 優缺點']


def google_suggest(q):
    """Google 台灣的搜尋建議。用 curl 取，避開部分 Python 安裝缺少根憑證的問題。"""
    url = SUGGEST_URL + urllib.parse.quote(q)
    try:
        out = subprocess.run(['curl', '-s', '--max-time', '6', url], capture_output=True, timeout=10).stdout
        return json.loads(out.decode('utf-8'))[1]
    except Exception:
        return []


def suggest(q, mode):
    q = q.strip()[:60]
    if not q:
        return 400, {'errors': ['請輸入關鍵字']}
    patterns = QUESTION_PATTERNS if mode == 'questions' else ['{q}', '{q} ']
    seen, out = set(), []
    for pat in patterns:
        for s in google_suggest(pat.format(q=q)):
            if s not in seen:
                seen.add(s)
                out.append(s)
    if not out:
        return 502, {'errors': ['沒有取得搜尋建議（可能是網路連不到 Google）']}
    return 200, {'suggestions': out[:40]}


def save(doc_id, body):
    path = doc_path(doc_id)
    old = json.loads(gen.read(path)) if os.path.exists(path) else None
    if doc_id == '_platform':
        errors = gen.validate_platform(body, gen.load_modules())
        if errors:
            return 422, {'errors': errors}
        if old != body:
            body['updated'] = gen.today()
        io.open(path, 'w', encoding='utf-8').write(json_dump(body))
    else:
        if body.get('slug') != doc_id:
            return 400, {'errors': ['slug 不可修改']}
        if not body.get('draft'):
            mods = gen.load_modules()
            mods.pop(doc_id, None)
            errors, _ = gen.validate(body, mods, gen.load_platform())
            if errors:
                return 422, {'errors': errors}
        if old is not None and {k: v for k, v in old.items() if k != 'updated'} != \
                {k: v for k, v in body.items() if k != 'updated'}:
            body['updated'] = gen.today()
        body['updated'] = body.get('updated') or gen.today()
        io.open(path, 'w', encoding='utf-8').write(json_dump(body))
        if not body.get('draft'):
            place_on_platform(body)
    r = gen.build_all()
    if r['errors']:
        return 422, {'errors': r['errors'], 'saved': True}
    r['font'] = rebuild_fonts()
    r['git_dirty'] = git_dirty()
    return 200, r


def place_on_platform(m):
    """第一次發布時，產品放進精靈選的平台分組；產品與解決方案都放進「依需求找模組」表。"""
    pf = gen.load_platform()
    slug = m['slug']
    changed = False
    if not gen.is_solution(m) and not any(slug in lg['modules'] for lg in pf['legs']):
        leg = next((lg for lg in pf['legs'] if lg['name'] == m.get('platform_leg')), pf['legs'][-1])
        leg['modules'].append(slug)
        changed = True
    if m.get('platform_need') and not any(s == slug for _, s in pf['needs']['rows']):
        pf['needs']['rows'].append([m['platform_need'], slug])
        changed = True
    if changed:
        pf['updated'] = gen.today()
        io.open(os.path.join(gen.SRC, '_platform.json'), 'w', encoding='utf-8').write(json_dump(pf))


def create(body):
    slug = (body.get('slug') or '').strip()
    solution = body.get('kind') == 'solution'
    prefix = 'solution-' if solution else 'nexus-'
    if not gen.SLUG_RE.match(slug) or not slug.startswith(prefix):
        return 400, {'errors': ['代號須為 %s 開頭的小寫英數與連字號，例如 %s' % (prefix, prefix + ('ai-record' if solution else 'vault'))]}
    if os.path.exists(doc_path(slug)) or os.path.exists(os.path.join(gen.ROOT, slug + '.html')):
        return 409, {'errors': ['%s 已經存在' % slug]}
    required = (('code', '名稱'), ('name_zh', '中文名稱'), ('industry', '產業'), ('need', '需求一句話')) if solution else \
        (('code', '產品名'), ('name_zh', '中文功能名'), ('platform_leg', '平台分組'), ('need', '需求一句話'))
    for k, label in required:
        if not (body.get(k) or '').strip():
            return 400, {'errors': ['%s 不可空白' % label]}
    pf = gen.load_platform()
    m = copy.deepcopy(TEMPLATE)
    m.update({'slug': slug, 'file': slug + '.html', 'code': body['code'].strip(), 'name_zh': body['name_zh'].strip(),
              'leg': body.get('platform_leg', ''), 'platform_leg': body.get('platform_leg', ''), 'platform_need': body['need'].strip(),
              'updated': gen.today()})
    m['eyebrow'] = m['code']
    m['hero']['h1'] = '%s｜%s' % (m['code'], m['name_zh']) if m['code'] != m['name_zh'] else m['name_zh']
    if solution:
        m.update({'kind': 'solution', 'industry': body['industry'].strip(), 'leg': body['industry'].strip() + '解決方案',
                  'flow_heading': '運作流程', 'flow': [{'title': '', 'text': '', 'modules': ['nexus-forge']}]})
        m.pop('platform_leg', None)
        m['summary'][1] = ['組成', '']
        m['platform']['heading'] = '由哪些平台模組組成'
    else:
        m['summary'][1][1] = 'AURO NEXUS 平台「%s」能力。' % body['platform_leg']
    # 配色沿用同分組既有產品，讓同一條能力腿看起來是一家人
    allm = gen.load_modules(include_drafts=True)
    leg = next((lg for lg in pf['legs'] if lg['name'] == body.get('platform_leg')), None)
    sib = next((allm[s] for s in (leg['modules'] if leg else []) if s in allm), None)
    m['theme'] = dict(sib['theme']) if sib else dict(allm['nexus-forge']['theme'])
    io.open(doc_path(slug), 'w', encoding='utf-8').write(json_dump(m))
    return 200, {'slug': slug}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def send(self, code, body, ctype='application/json; charset=utf-8'):
        data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def body(self):
        n = int(self.headers.get('Content-Length') or 0)
        return json.loads(self.rfile.read(n).decode('utf-8') or 'null')

    def static(self, base, rel):
        path = os.path.normpath(os.path.join(base, rel))
        if not path.startswith(os.path.normpath(base) + os.sep) or not os.path.isfile(path):
            return self.send(404, {'error': 'not found'})
        ctype = mimetypes.guess_type(path)[0] or 'application/octet-stream'
        if ctype.startswith('text/') or ctype in ('application/javascript', 'application/json'):
            ctype += '; charset=utf-8'
        with open(path, 'rb') as f:
            self.send(200, f.read(), ctype)

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        p = urllib.parse.unquote(url.path)
        try:
            if p in ('/', '/index.html'):
                return self.static(HERE, 'index.html')
            if p.startswith('/cms/'):
                return self.static(HERE, p[len('/cms/'):])
            if p.startswith('/site/'):
                rel = p[len('/site/'):] or 'index.html'
                full = os.path.normpath(os.path.join(gen.ROOT, rel))
                if rel.endswith('.html') and full.startswith(gen.ROOT + os.sep) and os.path.isfile(full):
                    # 本機瀏覽網站頁面時拿掉 GTM，不送流量統計與轉換事件
                    return self.send(200, GTM_RE.sub('', gen.read(full)).encode('utf-8'), 'text/html; charset=utf-8')
                return self.static(gen.ROOT, rel)
            if p == '/api/state':
                return self.send(200, state())
            if p == '/api/suggest':
                qs = urllib.parse.parse_qs(url.query)
                return self.send(*suggest(qs.get('q', [''])[0], qs.get('mode', ['keywords'])[0]))
            m = re.match(r'^/api/doc/([\w-]+)$', p)
            if m:
                path = doc_path(m.group(1))
                if not os.path.exists(path):
                    return self.send(404, {'errors': ['找不到 %s' % m.group(1)]})
                return self.send(200, json.loads(gen.read(path)))
            self.send(404, {'error': 'not found'})
        except ValueError as e:
            self.send(400, {'errors': [str(e)]})

    def do_POST(self):
        p = urllib.parse.urlparse(self.path).path
        try:
            m = re.match(r'^/api/preview/([\w-]+)$', p)
            if m:
                doc_path(m.group(1))
                return self.send(200, preview(m.group(1), self.body()))
            if p == '/api/new':
                return self.send(*create(self.body()))
            self.send(404, {'error': 'not found'})
        except ValueError as e:
            self.send(400, {'errors': [str(e)]})

    def do_PUT(self):
        p = urllib.parse.urlparse(self.path).path
        m = re.match(r'^/api/doc/([\w-]+)$', p)
        if not m:
            return self.send(404, {'error': 'not found'})
        try:
            return self.send(*save(m.group(1), self.body()))
        except ValueError as e:
            self.send(400, {'errors': [str(e)]})


class Server(ThreadingHTTPServer):
    # 預覽頁一次會發出四十多個資源請求；預設等待佇列只有 5，超過會被系統重設連線
    request_queue_size = 128
    daemon_threads = True


def make_server(root=DEFAULT_ROOT, port=8899):
    gen.set_root(root)
    return Server(('127.0.0.1', port), Handler)


def main():
    ap = argparse.ArgumentParser(description='AURO NEXUS 產品頁編輯器')
    ap.add_argument('--port', type=int, default=8899)
    ap.add_argument('--root', default=DEFAULT_ROOT, help='網站 repo 根目錄')
    a = ap.parse_args()
    srv = make_server(a.root, a.port)
    print('產品頁編輯器：http://127.0.0.1:%d   （Ctrl+C 結束）' % a.port)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
