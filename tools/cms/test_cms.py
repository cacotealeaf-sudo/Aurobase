#!/usr/bin/env python3
"""編輯器與產生器的測試：在網站的暫存複本上跑，不動到真的檔案。

    python3 -m unittest tools/cms/test_cms.py
"""
import json
import os
import shutil
import sys
import tempfile
import threading
import unittest
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
os.environ['CMS_SKIP_FONTS'] = '1'

import server  # noqa: E402

gen = server.gen
SKIP = shutil.ignore_patterns('.git', 'WOFF2', 'images', 'archive', 'blogpost', 'scss', 'fonts', 'api')


class SiteCopy(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, 'site')
        shutil.copytree(REPO, self.root, ignore=SKIP)
        gen.set_root(self.root)

    def tearDown(self):
        gen.set_root(REPO)
        shutil.rmtree(self.tmp)

    def doc(self, slug):
        with open(os.path.join(gen.SRC, slug + '.json'), encoding='utf-8') as f:
            return json.load(f)

    def page(self, name):
        with open(os.path.join(self.root, name), encoding='utf-8') as f:
            return f.read()


class GeneratorTest(SiteCopy):
    def test_current_content_passes(self):
        self.assertEqual(gen.check_all(), [])

    def test_build_is_idempotent(self):
        gen.build_all()
        first = {f: self.page(f) for f in ('nexus.html', 'nexus-forge.html', 'llms.txt', 'sitemap.xml')}
        gen.build_all()
        for f, text in first.items():
            self.assertEqual(self.page(f), text, f)

    def test_validation_catches_broken_content(self):
        mods, pf = gen.load_modules(), gen.load_platform()
        m = self.doc('nexus-cardea')
        m['summary'] = [['所屬', 'x']]
        m['platform']['related'] = ['nexus-nope']
        m['inquiry_chip'] = '不存在的選項'
        m['theme']['deep'] = 'red'
        errors, _ = gen.validate(m, mods, pf)
        joined = '\n'.join(errors)
        for needle in ('是什麼', 'nexus-nope', 'inquiry_chip', 'theme.deep'):
            self.assertIn(needle, joined)

    def test_build_refuses_to_write_when_content_is_broken(self):
        m = self.doc('nexus-forge')
        m['hero']['h1'] = ''
        with open(os.path.join(gen.SRC, 'nexus-forge.json'), 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False)
        before = self.page('nexus-forge.html')
        r = gen.build_all()
        self.assertTrue(r['errors'])
        self.assertEqual(self.page('nexus-forge.html'), before)

    def test_draft_page_is_removed_and_hidden_from_overview(self):
        gen.build_all()
        m = self.doc('nexus-library')
        m['draft'] = True
        with open(os.path.join(gen.SRC, 'nexus-library.json'), 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False)
        r = gen.build_all()
        self.assertEqual(r['errors'], [])
        self.assertIn('nexus-library.html', r['removed'])
        self.assertFalse(os.path.exists(os.path.join(self.root, 'nexus-library.html')))
        self.assertNotIn('href="nexus-library.html"', self.page('nexus.html'))
        self.assertNotIn('nexus-library.html', self.page('llms.txt'))


class AuditTest(SiteCopy):
    def test_current_content_has_no_failing_checks(self):
        mods, pf = gen.load_modules(), gen.load_platform()
        for m in mods.values():
            fails = [c['label'] for c in gen.audit(m, mods, pf)['checks'] if c['status'] == 'fail']
            self.assertEqual(fails, [], m['slug'])
        self.assertEqual([c for c in gen.audit_platform(pf)['checks'] if c['status'] == 'fail'], [])

    def test_audit_flags_missing_keyword_and_entity_sentence(self):
        mods, pf = gen.load_modules(), gen.load_platform()
        m = self.doc('nexus-cardea')
        m['hero']['h1'] = 'Cardea｜機器身分'
        m['definition']['a'] = ['沒有實體句的回答。']
        bad = {c['label'] for c in gen.audit(m, mods, pf)['checks'] if c['status'] == 'fail'}
        self.assertIn('主關鍵字出現在 H1', bad)
        self.assertTrue(any('實體句' in b for b in bad))

    def test_title_width_counts_latin_as_half(self):
        self.assertEqual(gen.disp_width('AI 治理'), 3.5)

    def test_robots_blocking_ai_bots_fails_site_check(self):
        with open(os.path.join(self.root, 'robots.txt'), 'w') as f:
            f.write('User-agent: GPTBot\nDisallow: /\n')
        checks = gen.site_checks('nexus-forge.html')
        self.assertEqual(checks[0]['status'], 'fail')


class EditorTest(SiteCopy):
    def test_new_product_starts_as_draft_and_publishes_into_overview(self):
        code, body = server.create({'slug': 'nexus-vault', 'code': 'Vault', 'name_zh': '金鑰管理',
                                    'platform_leg': '安全', 'need': '集中管理金鑰與系統密碼'})
        self.assertEqual(code, 200, body)
        m = self.doc('nexus-vault')
        self.assertTrue(m['draft'])
        self.assertEqual(gen.build_all()['errors'], [])
        self.assertNotIn('nexus-vault', self.page('nexus.html'))

        # 草稿缺欄位也能存；取消草稿時才會擋
        m['draft'] = False
        code, body = server.save('nexus-vault', m)
        self.assertEqual(code, 422)

        donor = self.doc('nexus-cardea')
        for k in ('title', 'description', 'keywords', 'eyebrow', 'hero', 'summary', 'definition', 'audience',
                  'pain', 'capabilities', 'diff', 'platform', 'deploy', 'faq', 'cta'):
            m[k] = donor[k]
        code, body = server.save('nexus-vault', m)
        self.assertEqual(code, 200, body)
        self.assertTrue(os.path.exists(os.path.join(self.root, 'nexus-vault.html')))
        pf = gen.load_platform()
        self.assertIn('nexus-vault', next(lg for lg in pf['legs'] if lg['name'] == '安全')['modules'])
        self.assertIn(['集中管理金鑰與系統密碼', 'nexus-vault'], pf['needs']['rows'])
        self.assertIn('href="nexus-vault.html"', self.page('nexus.html'))
        self.assertIn('nexus-vault.html', self.page('sitemap.xml'))

    def test_create_rejects_bad_or_existing_slug(self):
        base = {'code': 'X', 'name_zh': 'x', 'platform_leg': '安全', 'need': 'x'}
        self.assertEqual(server.create(dict(base, slug='Vault'))[0], 400)
        self.assertEqual(server.create(dict(base, slug='nexus-forge'))[0], 409)

    def test_save_updates_date_only_when_content_changes(self):
        m = self.doc('nexus-forge')
        m['updated'] = '2000-01-01'
        with open(os.path.join(gen.SRC, 'nexus-forge.json'), 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False)
        self.assertEqual(server.save('nexus-forge', dict(m))[0], 200)
        self.assertEqual(self.doc('nexus-forge')['updated'], '2000-01-01')
        m['cta']['heading'] = '改過的標題'
        self.assertEqual(server.save('nexus-forge', m)[0], 200)
        self.assertEqual(self.doc('nexus-forge')['updated'], gen.today())
        self.assertIn('改過的標題', self.page('nexus-forge.html'))

    def test_doc_ids_cannot_escape_the_content_folder(self):
        with self.assertRaises(ValueError):
            server.doc_path('../../etc/passwd')

    def test_http_preview_rewrites_assets_and_drops_analytics(self):
        srv = server.make_server(self.root, 0)
        t = threading.Thread(target=srv.serve_forever, daemon=True)
        t.start()
        try:
            port = srv.server_address[1]
            m = self.doc('nexus-scanner')
            req = urllib.request.Request('http://127.0.0.1:%d/api/preview/nexus-scanner' % port,
                                         data=json.dumps(m).encode(), method='POST',
                                         headers={'Content-Type': 'application/json'})
            out = json.loads(urllib.request.urlopen(req).read())
            self.assertEqual(out['errors'], [])
            self.assertIn('href="/site/css/nexus-module.css"', out['html'])
            self.assertNotIn('googletagmanager', out['html'])
            r = urllib.request.urlopen('http://127.0.0.1:%d/site/css/nexus-module.css' % port)
            self.assertEqual(r.status, 200)
            with self.assertRaises(urllib.error.HTTPError):
                urllib.request.urlopen('http://127.0.0.1:%d/site/../../etc/passwd' % port)
        finally:
            srv.shutdown()
            srv.server_close()


if __name__ == '__main__':
    unittest.main()
