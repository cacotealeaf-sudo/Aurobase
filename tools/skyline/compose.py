"""Run: python3 tools/skyline/compose.py out.json, then paste into js/aurora.js SKYLINE.
Original geometric Taipei skyline as polylines (w=1509, h=323, y down).
Each building is an outline from its left foot to its right foot; symmetric ones are
described as a left half (outer -> centre) and mirrored. One continuous line runs
along the ground between them; the bridge arch and cables are separate strokes."""
import json, sys
import numpy as np

W, H, B = 1509, 323, 316


def mirror(xc, half):
    """half: [(dx, y)] from the outer foot to the centre (dx <= 0)."""
    left = [(xc + dx, y) for dx, y in half]
    right = [(xc - dx, y) for dx, y in reversed(half) if dx != 0]
    return left + right


def roof(tip, inner, flick, n=6):
    """Chinese eave from the tip inward: flat near the tip, steep near the ridge."""
    (tx, ty), (ix, iy) = tip, inner
    pts = [(tx - 3, ty - flick), (tx, ty)]
    for s in np.linspace(0, 1, n)[1:]:
        pts.append((tx + (ix - tx) * s, ty - (ty - iy) * s * s))
    return pts


def temple(xc):
    h = [(-92, B), (-92, 300), (-80, 300), (-80, 270), (-104, 270)]
    h += roof((-108, 266), (-52, 240), 7)
    h += [(-48, 240), (-48, 230), (-68, 230)]
    h += roof((-72, 226), (-46, 214), 5)
    # swallowtail ridge (燕尾): ends flick up and out, then a flat ridge to the centre
    h += [(-50, 203), (-42, 210), (-6, 210), (-4, 204), (0, 200)]
    return mirror(xc, h)


def cks_hall(xc):
    h = [(-84, B), (-84, 304), (-76, 304), (-76, 296), (-62, 296), (-62, 262), (-80, 262)]
    h += roof((-84, 258), (-40, 238), 6)
    h += [(-38, 238), (-38, 226), (-54, 226)]
    h += roof((-58, 222), (-6, 202), 5)
    h += [(-3, 198), (0, 186)]
    return mirror(xc, h)


def presidential(xc):
    h = [(-80, B), (-80, 252), (-68, 252), (-68, 264), (-18, 264), (-18, 196),
         (-12, 196), (-12, 182), (-8, 182), (-2, 166), (0, 156)]
    return mirror(xc, h)


def taipei101(xc):
    h = [(-34, B), (-24, 246)]
    yb = 246
    for _ in range(8):
        h += [(-21, yb), (-27, yb - 22)]
        yb -= 22
    h += [(-16, yb), (-16, 58), (-11, 58), (-11, 46), (-7, 46), (-7, 36), (-2, 36), (-1, 14), (0, 4)]
    return mirror(xc, h)


def pagoda(xc):
    h = [(-22, B), (-22, 300)]
    yb = 300
    for k in range(6):
        bw, ew = 17 - 1.6 * k, 26 - 2.2 * k
        top = yb - 14
        h += [(-bw, yb), (-bw, top), (-ew, top), (-ew - 3, top - 5)]
        yb = top - 8
        h += [(-(17 - 1.6 * (k + 1)), yb)]
    h += [(-3, yb), (-3, yb - 6), (-1, yb - 8), (0, yb - 24)]
    return mirror(xc, h)


def dome_top(x0, x1, y, rise, n=9):
    xc, r = (x0 + x1) / 2, (x1 - x0) / 2
    return [(xc - r * np.cos(a), y - rise * np.sin(a)) for a in np.linspace(0, np.pi, n)]


buildings = [
    temple(130),
    [(252, B), (252, 166), (262, 166), (262, 154), (272, 154), (272, 144), (279, 144), (279, 128),
     (281, 128), (281, 144), (288, 144), (288, 154), (298, 154), (298, 166), (308, 166),
     (308, 196), (344, 196), (344, B)],
    [(352, B), (352, 298), (612, 298), (612, B)],                       # bridge deck
    [(620, B), (620, 232), (640, 232), (640, 210), (646, 210), (646, 202), (662, 202),
     (662, 210), (668, 210), (668, B)],
    cks_hall(760),
    presidential(940),
    [(1034, B), (1034, 182), (1080, 152), (1080, B)],
    [(1092, B)] + dome_top(1092, 1130, 176, 12) + [(1130, B)],
    [(1150, B)] + dome_top(1150, 1190, 150, 20)[:5] + [(1169, 128), (1170, 112), (1171, 128)]
    + dome_top(1150, 1190, 150, 20)[4:] + [(1190, B)],
    [(1204, B), (1204, 262), (1222, 262), (1222, 244), (1282, 244), (1282, 262), (1300, 262), (1300, B)],
    taipei101(1352),
    [(1396, B), (1396, 276), (1430, 276), (1430, B)],
    pagoda(1466),
]

line = [(0, B)]
for b in buildings:
    line += b
line.append((W, B))

# Bridge: asymmetric arch + a fan of cables down to the deck
ax0, ax1, apx, apy, deck = 372, 600, 520, 184, 298
def arch_y(x):
    u = (x - apx) / ((apx - ax0) if x < apx else (ax1 - apx))
    return apy + (deck - apy) * u * u
arch = [(x, arch_y(x)) for x in np.linspace(ax0, ax1, 21)]
cables = [[(x, arch_y(x)), (x - 46, deck)] for x in np.linspace(ax0 + 57, ax0 + 166, 5)]


def flat(pts):
    out = []
    for x, y in pts:
        for v in (x, y):
            v = round(float(v), 1)
            out.append(int(v) if v == int(v) else v)
    return out


data = {'w': W, 'h': H, 'front': [flat(line), flat(arch)] + [flat(c) for c in cables]}
json.dump(data, open(sys.argv[1], 'w'), separators=(',', ':'))
print(sum(len(l) for l in data['front']) // 2, 'points')
