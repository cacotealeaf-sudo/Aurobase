/* ASCII aurora on a monospace cell grid (technique after stackedlol/ascii-sharks).
 * Curtains and palettes are lookup tables; every lit cell falls into one
 * (hue, alpha) bucket so each bucket is drawn with a single fillStyle.
 * Palette stops run from the bright lower hem (index 0) up to the fading rays. */
var AURORA_PALETTES = {
  aurobase: [[255, 150, 140], [255, 62, 52], [255, 38, 36], [178, 24, 36], [110, 20, 44]],
  ember:    [[255, 214, 170], [255, 150, 60], [255, 72, 22], [200, 50, 30], [120, 40, 40]],
  natural:  [[70, 255, 165], [45, 230, 195], [70, 195, 245], [135, 125, 255], [215, 105, 235]]
};
var AURORA_SLOTS = {
  // skyline = the tallest the skyline may get, as a share of the canvas height (0 = none).
  hero: { curtains: 3, horizon: 0.58, skyline: 0.42, bias: true, gain: 1 },
  cta:  { curtains: 2, horizon: 0.74, skyline: 0.30, bias: false, gain: 0.55 }
};
var CURTAINS = [
  { off:  0.00, amp: 0.075, f1: 0.0085, s1:  0.11, f2: 0.021, s2:  0.07, h: 0.30 },
  { off: -0.10, amp: 0.090, f1: 0.0065, s1: -0.08, f2: 0.017, s2:  0.05, h: 0.24 },
  { off:  0.07, amp: 0.050, f1: 0.0110, s1:  0.06, f2: 0.027, s2: -0.09, h: 0.18 }
];
var GLYPHS = '.:-+=tS%X#@' + "'";
var RAMP_LEN = 11;
var G_DOT = 0, G_PLUS = 3, G_TICK = 11;
// Dashed like the old ASCII ridge: dash and gap are fractions of a grid cell, width is in CSS px.
var SKY_LINE = { width: 1.4, dash: 0.7, gap: 0.3 };
var SKY_LAYERS = [{ key: 'hills', rgba: 'rgba(214,212,208,0.42)' }];
var SKY_DROP = 10; // CSS px the ridge sits below its fitted position
var SKY_STRETCH = 1.3; // wide canvases may widen the drawing this much before it is centred
var HUES = 10, LEVELS = 6, PALE_RGB = [214, 212, 208];
var SKY = '#0b0b0d';

/* Mountain ridge (Guanyin Shan left, Yangmingshan right) as a flat x,y polyline in a
 * 1509x323 frame, y down. */
var SKYLINE = {
  w: 1509, h: 323,
  hills: [
    [0,237.1,3,237.3,6,236.8,9,235.7,12,234.4,15,233.2,18,232.2,21,231.3,24,230.3,27,228.8,30,226.7,33,224.1,36,221.3,39,218.6,42,216.5,45,215.1,48,214.4,51,214.1,54,214,57,213.7,60,213.4,63,212.8,66,211.8,69,210.7,72,209.8,75,208.8,78,207.7,81,205.9,84,203.5,87,200.3,90,196.5,93,192.7,96,189.2,99,186.2,102,183.8,105,181.9,108,180.1,111,178.3,114,176.5,117,174.9,120,173.8,123,173.2,126,172.8,129,172.7,132,172.6,135,172.2,138,171.3,141,169.8,144,167.9,147,165.9,150,164.2,153,163.1,156,162.6,159,162.5,162,162.5,165,162.3,168,162,171,161.7,174,161.7,177,162.3,180,163.7,183,165.9,186,168.4,189,171,192,173.2,195,174.7,198,175.6,201,176,204,176.2,207,176.5,210,177.2,213,177.9,216,178.5,219,178.5,222,177.9,225,176.7,228,175.1,231,173.6,234,172.4,237,171.8,240,171.5,243,171.3,246,171,249,170.3,252,169.5,255,169,258,169.2,261,170.3,264,172.3,267,175.2,270,178.4,273,181.6,276,184.4,279,186.7,282,188.7,285,190.6,288,192.5,291,194.5,294,196.4,297,197.9,300,198.5,303,198.5,306,197.9,309,197.1,312,196.5,315,196.3,318,196.7,321,197.7,324,198.9,327,200.1,330,201,333,201.6,336,202.1,339,202.7,342,203.7,345,205.2,348,207.3,351,209.4,354,211.3,357,212.7,360,213.4,363,213.6,366,213.6,369,213.7,372,214,375,214.5,378,215.1,381,215.3,384,215.2,387,214.6,390,213.8,393,213.1,396,212.9,399,213.3,402,214.4,405,215.9,408,217.5,411,218.8,414,219.8,417,220.4,420,221.1,423,221.9,426,223.2,429,224.9,432,226.8,435,228.5,438,229.6,441,230.1,444,230,447,229.7,450,229.4,453,229.5,456,230,459,230.7,462,231.3,465,231.6,468,231.4,471,230.7,474,230,477,229.5,480,229.5,483,230,486,230.8,489,231.7,492,232.1,495,232,498,231.4,501,230.5,504,229.5,507,228.9,510,228.6,513,228.6,516,228.5,519,228,522,227,525,225.6,528,224,531,222.5,534,221.5,537,221.2,540,221.4,543,221.8,546,222.2,549,222.2,552,221.9,555,221.4,558,221.1,561,221.3,564,221.8,567,222.6,570,223.3,573,223.6,576,223.3,579,222.3,582,220.8,585,219.1,588,217.7,591,216.6,594,216,597,215.4,600,214.6,603,213.5,606,211.9,609,210.2,612,208.5,615,207.4,618,206.8,621,206.8,624,207.2,627,207.5,630,207.4,633,207,636,206.2,639,205.3,642,204.8,645,204.7,648,205.1,651,205.7,654,206.1,657,206.1,660,205.6,663,204.7,666,203.8,669,203.2,672,203.2,675,203.8,678,204.8,681,205.9,684,206.7,687,207.1,690,207.3,693,207.4,696,207.9,699,208.8,702,210.1,705,211.7,708,213.2,711,214.2,714,214.6,717,214.4,720,213.9,723,213.4,726,213.3,729,213.5,732,214,735,214.4,738,214.4,741,213.9,744,213.1,747,212.4,750,212,753,212.3,756,213.2,759,214.7,762,216.4,765,217.9,768,219,771,219.7,774,220.3,777,220.9,780,221.9,783,223.4,786,225.1,789,226.8,792,228.1,795,228.8,798,229,801,228.8,804,228.7,807,228.9,810,229.6,813,230.8,816,232,819,233.1,822,233.8,825,234,828,233.9,831,233.9,834,234.2,837,234.9,840,236,843,237.1,846,238,849,238.2,852,237.8,855,236.9,858,235.9,861,235,864,234.5,867,234.3,870,234.2,873,233.9,876,233.2,879,231.9,882,230.4,885,228.9,888,227.8,891,227.4,894,227.5,897,228,900,228.4,903,228.5,906,228.2,909,227.6,912,227,915,226.6,918,226.7,921,227.2,924,227.9,927,228.5,930,228.5,933,228,936,226.7,939,225.2,942,223.6,945,222.4,948,221.5,951,220.8,954,220.1,957,218.9,960,217.3,963,215.3,966,213.2,969,211.4,972,210.2,975,209.5,978,209.1,981,208.8,984,208.2,987,207.1,990,205.6,993,204,996,202.6,999,201.6,1002,201.2,1005,201.2,1008,201.3,1011,201.2,1014,200.5,1017,199.2,1020,197.5,1023,195.8,1026,194.4,1029,193.5,1032,192.9,1035,192.4,1038,191.6,1041,190.3,1044,188.6,1047,186.7,1050,184.9,1053,183.5,1056,182.6,1059,182.2,1062,181.8,1065,181.2,1068,180.3,1071,178.9,1074,177.4,1077,176,1080,175.2,1083,174.9,1086,174.7,1089,174.5,1092,173.9,1095,172.8,1098,171,1101,169,1104,166.9,1107,165.2,1110,164,1113,163.3,1116,162.7,1119,161.9,1122,160.8,1125,159.1,1128,157.2,1131,155.3,1134,153.7,1137,152.7,1140,152.3,1143,152.1,1146,151.9,1149,151.5,1152,150.7,1155,149.5,1158,148.1,1161,147,1164,146.3,1167,146.1,1170,146.1,1173,146.1,1176,145.8,1179,145.1,1182,144,1185,142.9,1188,142.1,1191,141.8,1194,142.1,1197,142.5,1200,143,1203,143,1206,142.6,1209,141.7,1212,140.8,1215,140.2,1218,140.3,1221,141,1224,142.2,1227,143.5,1230,144.7,1233,145.5,1236,146.1,1239,146.7,1242,147.5,1245,148.9,1248,150.7,1251,152.8,1254,154.8,1257,156.3,1260,157.1,1263,157.2,1266,156.9,1269,156.7,1272,157.2,1275,158.2,1278,159.7,1281,161.3,1284,162.6,1287,163.4,1290,163.7,1293,163.8,1296,163.8,1299,164.2,1302,165,1305,166,1308,166.9,1311,167.5,1314,167.7,1317,167.8,1320,167.8,1323,168.1,1326,169,1329,170.5,1332,172.5,1335,174.6,1338,176.6,1341,178,1344,179,1347,179.6,1350,180.2,1353,181,1356,182.3,1359,184,1362,185.7,1365,187.2,1368,188.3,1371,188.9,1374,189.1,1377,189.4,1380,190,1383,191.2,1386,192.7,1389,194.4,1392,195.8,1395,196.7,1398,197,1401,196.7,1404,196.6,1407,196.8,1410,197.7,1413,199.1,1416,200.8,1419,202.4,1422,203.6,1425,204.3,1428,204.6,1431,204.9,1434,205.4,1437,206.4,1440,207.8,1443,209.5,1446,211,1449,212,1452,212.6,1455,212.6,1458,212.4,1461,212.3,1464,212.8,1467,214.1,1470,215.9,1473,217.7,1476,219.2,1479,220.3,1482,220.9,1485,221.3,1488,221.8,1491,222.6,1494,223.7,1497,224.9,1500,225.9,1503,226.4,1506,226.1,1509,225.3]
  ]
};

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
  var energy = new Float32Array(0), tmp = energy, glyph = new Uint8Array(0), ridge = new Int16Array(0), sky = null;
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
    placeSkyline();
    font = '700 ' + Math.round(cw * 1.45) + 'px "Space Mono", ui-monospace, Menlo, monospace';
    paintBackground();
  }

  // Bottom-aligned, as wide as the canvas unless that would make it taller than o.skyline.
  // ridge[c] = first row hidden behind the skyline in column c, so aurora glyphs stop above it.
  function placeSkyline() {
    ridge = new Int16Array(cols).fill(rows);
    sky = null;
    if (!o.skyline) return;
    var sy = Math.min(W / SKYLINE.w, (H * o.skyline) / SKYLINE.h);
    var sx = Math.min(W / SKYLINE.w, sy * SKY_STRETCH);
    sky = { sx: sx, sy: sy, ox: (W - SKYLINE.w * sx) / 2, oy: H + 2 + SKY_DROP - SKYLINE.h * sy };
    var pad = SKY_LINE.width * 2;
    SKY_LAYERS.forEach(function (layer) { SKYLINE[layer.key].forEach(function (l) {
      for (var i = 2; i < l.length; i += 2) {
        var x0 = sky.ox + l[i - 2] * sx, y0 = sky.oy + l[i - 1] * sy;
        var x1 = sky.ox + l[i] * sx, y1 = sky.oy + l[i + 1] * sy;
        var n = Math.max(1, Math.ceil(Math.abs(x1 - x0) / (cw / 2)));
        for (var k = 0; k <= n; k++) {
          var c = Math.floor((x0 + (x1 - x0) * k / n) / cw);
          var r = Math.floor((y0 + (y1 - y0) * k / n - pad) / ch);
          if (c >= 0 && c < cols && r < ridge[c]) ridge[c] = Math.max(0, r);
        }
      }
    }); });
  }

  function paintSkyline(g) {
    if (!sky) return;
    g.lineCap = 'butt'; g.lineJoin = 'miter';
    g.lineWidth = SKY_LINE.width;
    g.setLineDash([cw * SKY_LINE.dash, cw * SKY_LINE.gap]);
    SKY_LAYERS.forEach(function (layer) {
      g.strokeStyle = layer.rgba;
      SKYLINE[layer.key].forEach(function (l) {
        g.beginPath(); // one path per stroke so each starts on a dash
        g.moveTo(sky.ox + l[0] * sky.sx, sky.oy + l[1] * sky.sy);
        for (var i = 2; i < l.length; i += 2) g.lineTo(sky.ox + l[i] * sky.sx, sky.oy + l[i + 1] * sky.sy);
        g.stroke();
      });
    });
    g.setLineDash([]);
  }

  function paintBackground() {
    var g = bg.getContext('2d');
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.fillStyle = SKY;
    g.fillRect(0, 0, W, H);
    if (o.showGrid) {
      g.strokeStyle = 'rgba(255,255,255,0.032)';
      g.lineWidth = 1 / dpr;
      g.beginPath();
      for (var c = 0; c <= cols; c++) { g.moveTo(c * cw, 0); g.lineTo(c * cw, H); }
      for (var r = 0; r <= rows; r++) { g.moveTo(0, r * ch); g.lineTo(W, r * ch); }
      g.stroke();
    }
    paintSkyline(g);
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

  // Behind the skyline: no aurora, only a sparse scatter of dim ticks (lit windows).
  function cellRidge(c, r) {
    if (r === ridge[c] || auroraHash(c, r, 11) < 0.95) return -1;
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
