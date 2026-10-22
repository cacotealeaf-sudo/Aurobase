/* ASCII aurora on a monospace cell grid (technique after stackedlol/ascii-sharks).
 * Curtains and palettes are lookup tables; every lit cell falls into one
 * (hue, alpha) bucket so each bucket is drawn with a single fillStyle.
 * Palette stops run from the bright lower hem (index 0) up to the fading rays. */
var AURORA_PALETTES = {
  aurobase: [[255, 150, 100], [255, 72, 22], [232, 75, 34], [178, 38, 44], [110, 26, 52]],
  ember:    [[255, 214, 170], [255, 150, 60], [255, 72, 22], [200, 50, 30], [120, 40, 40]],
  natural:  [[70, 255, 165], [45, 230, 195], [70, 195, 245], [135, 125, 255], [215, 105, 235]]
};
var AURORA_SLOTS = {
  hero: { curtains: 3, horizon: 0.58, ridge: true, bias: true, gain: 1 },
  cta:  { curtains: 2, horizon: 0.74, ridge: true, bias: false, gain: 0.55 }
};
var CURTAINS = [
  { off:  0.00, amp: 0.075, f1: 0.0085, s1:  0.11, f2: 0.021, s2:  0.07, h: 0.30 },
  { off: -0.10, amp: 0.090, f1: 0.0065, s1: -0.08, f2: 0.017, s2:  0.05, h: 0.24 },
  { off:  0.07, amp: 0.050, f1: 0.0110, s1:  0.06, f2: 0.027, s2: -0.09, h: 0.18 }
];
var GLYPHS = '.:-+=tS%X#@' + "'/\\_^";
var RAMP_LEN = 11;
var G_DOT = 0, G_PLUS = 3, G_TICK = 11, G_UP = 12, G_DOWN = 13, G_FLAT = 14, G_PEAK = 15;
var HUES = 10, LEVELS = 6, PALE_RGB = [214, 212, 208];
var SKY = '#0b0b0d';

function auroraClamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }
function auroraSmooth(a, b, x) { var t = auroraClamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); }
function auroraHash(x, y, z) {
  var h = Math.imul(x | 0, 0x27d4eb2d) ^ Math.imul(y | 0, 0x165667b1) ^ Math.imul(z | 0, 0x9e3779b1);
  h = Math.imul(h ^ (h >>> 15), 0x85ebca6b);
  h ^= h >>> 13;
  return (h >>> 0) / 4294967296;
}
function auroraStyles(stops) {
  var out = [];
  for (var h = 0; h <= HUES; h++) {
    var rgb = PALE_RGB;
    if (h < HUES) {
      var p = (h / (HUES - 1)) * (stops.length - 1), i = Math.min(stops.length - 2, Math.floor(p)), f = p - i;
      rgb = [0, 1, 2].map(function (k) { return Math.round(stops[i][k] + (stops[i + 1][k] - stops[i][k]) * f); });
    }
    for (var l = 0; l < LEVELS; l++) out.push('rgba(' + rgb.join(',') + ',' + ((l + 1) / LEVELS).toFixed(3) + ')');
  }
  return out;
}

function createAurora(canvas, initial) {
  var ctx = canvas.getContext('2d', { alpha: false });
  var bg = document.createElement('canvas');
  var o = {}, styles = [], font = '';
  var W = 0, H = 0, dpr = 1, cw = 10, ch = 15, cols = 0, rows = 0;
  var energy = new Float32Array(0), tmp = energy, glyph = new Uint8Array(0), ridge = new Int16Array(0);
  var yb = new Float32Array(0), ray = yb, fold = yb;
  var buckets = []; for (var b = 0; b < (HUES + 1) * LEVELS; b++) buckets.push([]);
  var t = 8 + Math.random() * 30, last = 0, raf = 0, visible = true, dead = false;
  var pointer = { x: 0, y: 0, px: 0, py: 0, active: false };
  var rings = [];
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  function setOptions(next) {
    var key = JSON.stringify(next);
    if (key === o._key) return;
    o = Object.assign({}, next, { _key: key });
    styles = auroraStyles(AURORA_PALETTES[o.palette] || AURORA_PALETTES.aurobase);
    resize();
  }

  function resize() {
    var r = canvas.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;
    W = r.width; H = r.height; dpr = Math.min(window.devicePixelRatio || 1, 2);
    cw = auroraClamp(Math.round(W / o.density), 7, 14); ch = Math.round(cw * 1.5);
    cols = Math.ceil(W / cw); rows = Math.ceil(H / ch);
    canvas.width = bg.width = Math.round(W * dpr);
    canvas.height = bg.height = Math.round(H * dpr);
    var n = cols * rows, m = CURTAINS.length * cols;
    energy = new Float32Array(n); tmp = new Float32Array(n); glyph = new Uint8Array(n);
    yb = new Float32Array(m); ray = new Float32Array(m); fold = new Float32Array(m);
    ridge = new Int16Array(cols);
    var scale = o.horizon > 0.7 ? 0.7 : 1;
    for (var c = 0; c < cols; c++) {
      var x = c * cw;
      var hgt = 0.10 + 0.05 * Math.sin(x * 0.0042 + 1.3) + 0.03 * Math.sin(x * 0.011) + 0.014 * Math.sin(x * 0.031 + 2);
      ridge[c] = o.ridge ? rows - Math.round(rows * hgt * scale) : rows;
    }
    font = '700 ' + Math.round(cw * 1.45) + 'px "Space Mono", ui-monospace, Menlo, monospace';
    paintBackground();
  }

  function paintBackground() {
    var g = bg.getContext('2d');
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.fillStyle = SKY;
    g.fillRect(0, 0, W, H);
    if (!o.showGrid) return;
    g.strokeStyle = 'rgba(255,255,255,0.032)';
    g.lineWidth = 1 / dpr;
    g.beginPath();
    for (var c = 0; c <= cols; c++) { g.moveTo(c * cw, 0); g.lineTo(c * cw, H); }
    for (var r = 0; r <= rows; r++) { g.moveTo(0, r * ch); g.lineTo(W, r * ch); }
    g.stroke();
  }

  function deposit(c, r, amount) {
    if (c < 0 || r < 0 || c >= cols || r >= rows) return;
    var i = r * cols + c;
    energy[i] = Math.min(1.4, energy[i] + amount);
  }

  function step(dt) {
    t += dt;
    if (pointer.active) {
      var speed = Math.hypot(pointer.x - pointer.px, pointer.y - pointer.py) / Math.max(dt, 1e-3);
      var pc = Math.floor(pointer.x / cw), pr = Math.floor(pointer.y / ch);
      var amt = (0.12 + Math.min(0.5, speed / 1600)) * dt * 60;
      for (var dy = -1; dy <= 1; dy++) for (var dx = -2; dx <= 2; dx++) deposit(pc + dx, pr + dy, amt * (dx === 0 && dy === 0 ? 0.5 : 0.18));
      pointer.px = pointer.x; pointer.py = pointer.y;
    }
    rings = rings.filter(function (g) {
      g.r += 34 * dt; g.life -= dt * 0.9;
      var steps = Math.ceil(Math.PI * 2 * g.r);
      for (var s = 0; s < steps; s++) {
        var a = (s / steps) * Math.PI * 2;
        deposit(Math.round(g.c + Math.cos(a) * g.r), Math.round(g.row + Math.sin(a) * g.r * 0.66), 0.32 * g.life);
      }
      return g.life > 0;
    });
    var keep = Math.pow(0.955, dt * 60);
    for (var r = 1; r < rows - 1; r++) {
      for (var c = 1; c < cols - 1; c++) {
        var i = r * cols + c;
        tmp[i] = (energy[i] * 0.6 + (energy[i - 1] + energy[i + 1] + energy[i - cols] + energy[i + cols]) * 0.1) * keep;
      }
    }
    var swap = energy; energy = tmp; tmp = swap;
  }

  function computeCurtains() {
    var n = Math.min(o.curtains, CURTAINS.length);
    for (var k = 0; k < n; k++) {
      var cu = CURTAINS[k];
      for (var c = 0; c < cols; c++) {
        var x = c * cw, j = k * cols + c;
        var wave = 0.6 * Math.sin(x * cu.f1 + t * cu.s1) + 0.4 * Math.sin(x * cu.f2 - t * cu.s2 + k * 1.7);
        yb[j] = rows * (o.horizon + cu.off + cu.amp * wave);
        var s = 0.5 + 0.5 * Math.sin(x * 0.11 + 1.5 * Math.sin(x * 0.031 - t * 0.4) + t * (0.9 + 0.3 * k));
        ray[j] = 0.25 + 0.75 * s * s;
        var env = 0.5 + 0.5 * Math.sin(x * 0.0045 - t * 0.12 + k * 2.1);
        var bias = o.bias ? 0.12 + 0.88 * auroraSmooth(0.3, 0.75, x / W) : 1;
        fold[j] = (0.25 + 0.75 * env * env) * bias * o.intensity * o.gain;
      }
    }
    return n;
  }

  function cellStar(c, r) {
    var hsh = auroraHash(c, r, 7);
    if (hsh < 0.986) return -1;
    var tw = 0.5 + 0.5 * Math.sin(t * (0.8 + hsh * 3) + hsh * 40);
    glyph[r * cols + c] = hsh > 0.997 ? G_PLUS : G_DOT;
    return HUES * LEVELS + Math.min(LEVELS - 1, Math.floor(tw * 4));
  }

  function cellRidge(c, r) {
    var top = ridge[c];
    if (r === top) {
      var prev = c > 0 ? ridge[c - 1] : top, next = c < cols - 1 ? ridge[c + 1] : top;
      glyph[r * cols + c] = next < top ? G_UP : prev < top ? G_DOWN : (next > top && prev > top ? G_PEAK : G_FLAT);
      return HUES * LEVELS + 2;
    }
    if (auroraHash(c, r, 11) < 0.94) return -1;
    glyph[r * cols + c] = auroraHash(c, r, 13) > 0.5 ? G_TICK : G_DOT;
    return HUES * LEVELS;
  }

  function cellAurora(c, r, n, frame) {
    var v = 0, u = 0;
    for (var k = 0; k < n; k++) {
      var j = k * cols + c, d = yb[j] - r, hk = rows * CURTAINS[k].h;
      var a = d >= 0 ? Math.exp(-d / hk) * ray[j] : Math.exp(-(d * d) / 2.2);
      a *= fold[j];
      v += a; u += a * Math.min(1, Math.max(0, d) / (hk * 1.6));
    }
    u = v > 0 ? u / v : 0;
    var i = r * cols + c, e = Math.min(1, energy[i]);
    if (e > 0.01) { v += e; u = u * (1 - e); }
    if (v < 0.05) return cellStar(c, r);
    v = Math.min(v, 1);
    var gi = Math.floor(v * (RAMP_LEN - 1));
    if (auroraHash(c, r, frame) > 0.88) gi = Math.min(gi + 1, RAMP_LEN - 1);
    glyph[i] = gi;
    return Math.round(u * (HUES - 1)) * LEVELS + Math.min(LEVELS - 1, Math.floor(Math.pow(v, 0.8) * LEVELS));
  }

  function render() {
    if (!cols) return;
    var n = computeCurtains(), frame = Math.floor(t * 7);
    for (var b = 0; b < buckets.length; b++) buckets[b].length = 0;
    for (var r = 0; r < rows; r++) {
      for (var c = 0; c < cols; c++) {
        var bucket = r >= ridge[c] ? cellRidge(c, r) : cellAurora(c, r, n, frame);
        if (bucket >= 0) buckets[bucket].push(r * cols + c);
      }
    }
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.drawImage(bg, 0, 0);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.font = font; ctx.textBaseline = 'top';
    for (var q = 0; q < buckets.length; q++) {
      var list = buckets[q];
      if (!list.length) continue;
      ctx.fillStyle = styles[q];
      for (var z = 0; z < list.length; z++) {
        var idx = list[z];
        ctx.fillText(GLYPHS[glyph[idx]], (idx % cols) * cw, ((idx / cols) | 0) * ch);
      }
    }
  }

  function frame(now) {
    // Reduced motion still drifts, at half speed, so the page never looks frozen.
    var dt = Math.min(0.05, (now - last) / 1000) * (reduce.matches ? 0.5 : 1);
    last = now;
    step(dt);
    render();
    raf = requestAnimationFrame(frame);
  }

  function schedule() {
    cancelAnimationFrame(raf);
    if (dead) return;
    if (!visible) { render(); return; }
    last = performance.now();
    raf = requestAnimationFrame(frame);
  }

  function local(e) {
    var r = canvas.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
    return { x: x, y: y, inside: x >= 0 && y >= 0 && x <= r.width && y <= r.height };
  }
  function onMove(e) {
    var p = local(e);
    if (!pointer.active) { pointer.px = p.x; pointer.py = p.y; }
    pointer.x = p.x; pointer.y = p.y; pointer.active = p.inside && e.pointerType !== 'touch';
  }
  function onDown(e) {
    var p = local(e);
    if (p.inside) rings.push({ c: p.x / cw, row: p.y / ch, r: 0, life: 1 });
  }
  function onLeave() { pointer.active = false; }

  var ro = new ResizeObserver(resize);
  var io = new IntersectionObserver(function (es) { visible = es[0].isIntersecting; schedule(); });
  ro.observe(canvas); io.observe(canvas);
  window.addEventListener('pointermove', onMove, { passive: true });
  window.addEventListener('pointerdown', onDown, { passive: true });
  window.addEventListener('blur', onLeave);
  reduce.addEventListener('change', schedule);
  if (document.fonts && document.fonts.load) document.fonts.load('700 16px "Space Mono"').then(function () { if (!dead) render(); });

  setOptions(initial);
  schedule();

  return {
    setOptions: setOptions,
    destroy: function () {
      dead = true;
      cancelAnimationFrame(raf);
      ro.disconnect(); io.disconnect();
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerdown', onDown);
      window.removeEventListener('blur', onLeave);
      reduce.removeEventListener('change', schedule);
    }
  };
}

// Every <canvas data-aurora="hero|cta"> on the page gets its own instance.
var AURORA_OPTIONS = { palette: 'aurobase', intensity: 1, density: 130, showGrid: true };
Array.prototype.forEach.call(document.querySelectorAll('canvas[data-aurora]'), function (el) {
  var slot = AURORA_SLOTS[el.getAttribute('data-aurora')];
  if (slot) createAurora(el, Object.assign({}, slot, AURORA_OPTIONS));
});
