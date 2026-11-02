"""以 security.html 為底產生深色版型的指南頁（head、樣式、內文換掉，選單與頁尾沿用）。"""
import re, io
import os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ARROW = '<svg class="idx-arrow" width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 9L9 3M4 3h5v5"/></svg>'
STYLE = '''    <style>
/* ══════════════════════════════════════════════
   GUIDE PAGE — Scoped Styles（指南頁共用）
   Shared tokens/base/sections/cards/footer: css/aurora-theme.css
   ══════════════════════════════════════════════ */
.gd-hero .idx-aurora-body { padding-top: 140px; padding-bottom: 130px; }
.gd-meta { font-family: var(--idx-mono); font-size: 12px; color: var(--idx-muted); margin-top: 18px; }
.gd-answer { border: 1px solid var(--idx-line-2); border-left: 3px solid var(--idx-accent); background: var(--idx-surface); padding: 28px 32px; max-width: 920px; }
.gd-answer p { font-size: 16px; line-height: 1.95; margin: 0 0 12px; }
.gd-answer ol, .gd-answer ul { margin: 0; padding-left: 20px; font-size: 15px; line-height: 1.95; color: var(--idx-text-2); }
.gd-tag { display: inline-block; font-family: var(--idx-mono); font-size: 11px; color: var(--idx-accent); border: 1px solid var(--idx-accent); border-radius: 3px; padding: 1px 6px; margin-right: 6px; vertical-align: 2px; }
.gd-cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }
.gd-block h3 { font-size: 18px; margin: 0 0 10px; }
.gd-block ul { margin: 0; padding-left: 18px; font-size: 14px; line-height: 1.9; color: var(--idx-text-2); }
.gd-card .gd-sub { font-family: var(--idx-mono); font-size: 12px; color: var(--idx-muted); margin: 6px 0 2px; }
.gd-card ul { margin: 0; padding-left: 18px; font-size: 14px; line-height: 1.85; color: var(--idx-text-2); }
.gd-card ul li + li { margin-top: 4px; }
.gd-table { width: 100%; border-collapse: collapse; font-size: 14px; line-height: 1.8; }
.gd-table th, .gd-table td { border-bottom: 1px solid var(--idx-line); padding: 14px 12px; text-align: left; vertical-align: top; }
.gd-table th { font-family: var(--idx-mono); font-size: 12px; font-weight: 400; color: var(--idx-muted); border-bottom: 2px solid var(--idx-line-2); }
.gd-table td:first-child { color: var(--idx-ink); min-width: 180px; }
.gd-note { max-width: 920px; font-size: 15px; line-height: 1.9; }
.gd-note + .gd-note { margin-top: 12px; }
.gd-src { font-size: 14px; line-height: 2; padding-left: 18px; color: var(--idx-text-2); }
.gd-check { counter-reset: gd; display: grid; gap: 16px; }
.gd-check article { counter-increment: gd; }
.gd-check .idx-card-title::before { content: counter(gd, decimal-leading-zero) ' '; font-family: var(--idx-mono); color: var(--idx-accent); margin-right: 6px; }
@media (max-width: 991.98px) { .gd-hero .idx-aurora-body { padding-top: 112px; padding-bottom: 110px; } }
@media (max-width: 767.98px) {
  .gd-answer { padding: 22px 20px; }
  .gd-table thead { display: none; }
  .gd-table tr { display: block; border-bottom: 1px solid var(--idx-line); padding: 10px 0; }
  .gd-table td { display: block; border: 0; padding: 4px 0; }
}
</style>'''


def section(sid, num, eyebrow, title, inner, more=None, last=False):
    m = '<a href="%s" class="idx-more">%s%s</a>' % (more[0], more[1], ARROW) if more else ''
    return '''
  <section id="%s" class="idx-section idx-wrap%s">
    <div class="idx-sec-head">
      <div class="idx-sec-title-group">
        <span class="idx-sec-num">%s</span>
        <div>
          <div class="idx-eyebrow">// %s — %s</div>
          <h2 class="idx-sec-title">%s</h2>
        </div>
      </div>
      %s
    </div>
    <div class="idx-rule"></div>
%s
  </section>
''' % (sid, ' sec-last' if last else '', num, num, eyebrow, title, m, inner)


def build(out, title, desc, keywords, tag, h1, lead, meta, sections, primary, ghost):
    s = io.open(ROOT + '/security.html', encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, s, 1)
    s = re.sub(r'<meta name="description" content="[^"]*">', lambda m: '<meta name="description" content="%s">' % desc, s, 1)
    s = re.sub(r'<meta name="keywords" content="[^"]*">', lambda m: '<meta name="keywords" content="%s">' % ','.join(keywords), s, 1)
    s = s.replace('https://aurobase.com/security.html', 'https://aurobase.com/' + out)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', lambda m: '<meta property="og:title" content="%s">' % title, s)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', lambda m: '<meta property="og:description" content="%s">' % desc, s)
    i = s.index('    <style>'); j = s.index('</style>', i) + len('</style>')
    s = s[:i] + STYLE + s[j:]
    i = s.index('  <div class="idx-page">') + len('  <div class="idx-page">'); j = s.index('  <!-- Footer -->')
    hero = '''

  <section class="idx-aurora idx-hero gd-hero">
    <canvas data-aurora="hero" aria-hidden="true"></canvas>
    <div class="idx-aurora-body idx-wrap">
      <div class="idx-tagpair"><span>AUROBASE 指南</span><span>%s</span></div>
      <h1 class="idx-hero-title">%s</h1>
      <div class="idx-rule"></div>
      <p class="idx-hero-desc">%s</p>
      <div class="idx-hero-actions">
        <a href="%s" class="idx-btn idx-btn-primary">%s%s</a>
        <a href="%s" class="idx-btn idx-btn-ghost">%s</a>
      </div>
      <p class="gd-meta">%s</p>
    </div>
  </section>
''' % (tag, ''.join('<span>%s</span>' % x for x in h1), lead, primary[0], primary[1], ARROW, ghost[0], ghost[1], meta)
    # 產生器會在頁尾前插入常見問題，這裡不寫
    s = s[:i] + hero + ''.join(sections) + '\n' + s[j:]
    s = re.sub(r'\n  <!-- PAGE-FAQ:BEGIN.*?<!-- PAGE-FAQ:END -->', '', s, flags=re.S)
    io.open(ROOT + '/' + out, 'w', encoding='utf-8').write(s)
