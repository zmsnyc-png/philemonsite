#!/usr/bin/env python3
"""Philemon 1 v3 — fine ink line, figurative, scalloped feather texture (bird-rider ref)."""
import random, math

random.seed(5)

INK = "#1a1a1a"
W, H = 1000, 780

def jit(p, a):
    return (p[0] + random.uniform(-a, a), p[1] + random.uniform(-a, a))

def subdiv(pts, step):
    out = []
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]; x1, y1 = pts[i + 1]
        d = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(d / step))
        for k in range(n):
            t = k / n
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    out.append(pts[-1])
    return out

def cr_path(pts, closed=False):
    if closed:
        P = [pts[-1]] + pts + [pts[0], pts[1]]
    else:
        P = [pts[0]] + pts + [pts[-1]]
    d = f"M {P[1][0]:.1f} {P[1][1]:.1f} "
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C {c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f} "
    if closed:
        d += "Z"
    return d

def wob(pts, amp=1.0, closed=False, step=14):
    pts = subdiv(pts, step)
    if closed:
        pts = pts[:-1]
    pts = [jit(p, amp) for p in pts]
    return cr_path(pts, closed)

DEFS = []
EL = []

def add(d, fill="none", sw=2.4, stroke=INK, clip=None):
    EL.append((d, fill, sw, stroke, clip))

def rot(p, th):
    return (p[0] * math.cos(th) - p[1] * math.sin(th), p[0] * math.sin(th) + p[1] * math.cos(th))

# ================= WINGS (drawn first, behind figure) =================
# right wing: inner scaled mass; long primaries fan out beyond it
rwing = [
    (525, 235), (630, 198), (745, 192), (800, 238),
    (735, 330), (640, 362), (560, 345), (528, 300),
]
rwing.append(rwing[0])
rw_d = wob(rwing, amp=1.8, closed=True, step=22)

# left wing: mirrored, mostly behind the figure
lwing = [
    (485, 225), (380, 188), (265, 182), (210, 228),
    (275, 320), (370, 352), (450, 335), (482, 290),
]
lwing.append(lwing[0])
lw_d = wob(lwing, amp=1.8, closed=True, step=22)

DEFS.append(f'<clipPath id="cwR"><path d="{rw_d}"/></clipPath>')
DEFS.append(f'<clipPath id="cwL"><path d="{lw_d}"/></clipPath>')

add(lw_d, fill="white", sw=2.6)
add(rw_d, fill="white", sw=2.6)

def scale_arc(cx, cy, w=13, h=12, th=0.0, flip=1):
    pts = []
    n = 8
    for i in range(n + 1):
        t = math.pi * i / n
        lx, ly = -w * math.cos(t), flip * h * math.sin(t)
        gx, gy = rot((lx, ly), th)
        pts.append((cx + gx, cy + gy))
    pts = [jit(p, 0.7) for p in pts]
    return cr_path(pts)

# scallop rows, right wing
thr = math.radians(-7)
ox, oy = 548, 228
for r in range(16):
    v = -58 + r * 15
    for c in range(20):
        u = 4 + c * 26 + (13 if r % 2 else 0)
        g = rot((u, v), thr)
        add(scale_arc(ox + g[0], oy + g[1], th=thr), sw=1.4, clip="cwR")

# scallop rows, left wing (flip bulge so scales face down)
thl = math.radians(182)
ox2, oy2 = 502, 218
for r in range(16):
    v = -145 + r * 15
    for c in range(20):
        u = 4 + c * 26 + (13 if r % 2 else 0)
        g = rot((u, v), thl)
        add(scale_arc(ox2 + g[0], oy2 + g[1], th=thl, flip=-1), sw=1.4, clip="cwL")

# long flight feathers at the tips (white fill covers scales beneath)
def feather(ax, ay, ang_deg, L, Wd=24):
    th = math.radians(ang_deg)
    prof = [(0, Wd/2), (L*0.45, Wd*0.46), (L*0.88, Wd*0.20), (L, 0),
            (L*0.88, -Wd*0.20), (L*0.45, -Wd*0.46), (0, -Wd/2)]
    pts = []
    for lx, ly in prof:
        gx, gy = rot((lx, ly), th)
        pts.append((ax + gx, ay + gy))
    pts.append(pts[0])
    return wob(pts, amp=1.2, closed=True, step=16)

for ang, L in [(52, 135), (40, 170), (28, 200), (16, 222), (6, 232), (-5, 222)]:
    add(feather(745, 252, ang, L), fill="white", sw=2.0)
for ang, L in [(128, 135), (140, 170), (152, 200), (164, 222), (174, 232), (185, 222)]:
    add(feather(265, 242, ang, L), fill="white", sw=2.0)

# small barbs along the leading edges (scratchy ticks like the ref)
for t in range(8):
    f = t / 7
    x = 545 + (790 - 545) * f
    y = 235 - 44 * math.sin(f * math.pi)
    add(wob([(x, y), (x - 5, y - 9)], amp=0.6, step=6), sw=1.6)
    x2 = 465 - (465 - 222) * f
    y2 = 225 - 42 * math.sin(f * math.pi)
    add(wob([(x2, y2), (x2 + 4, y2 - 9)], amp=0.6, step=6), sw=1.6)

# ================= FIGURE (over the wings) =================
# robe / body, white fill to occlude wings
robe = [
    (492, 192), (470, 240), (456, 310), (452, 400), (458, 500), (464, 596),  # front
    (515, 604), (566, 598),                                                  # hem
    (558, 480), (548, 350), (540, 250), (516, 196),                          # back
]
robe.append(robe[0])
add(wob(robe, amp=1.2, closed=True, step=18), fill="white", sw=2.6)

# fold lines (start below the beard to keep the chest clean)
add(wob([(500, 330), (496, 440), (502, 560)], amp=1.2, step=20), sw=1.8)
add(wob([(526, 320), (530, 450), (524, 582)], amp=1.2, step=20), sw=1.8)
add(wob([(478, 430), (482, 560)], amp=1.2, step=20), sw=1.8)
# hem line
add(wob([(464, 596), (515, 588), (566, 598)], amp=1.0, step=16), sw=1.8)

# bare feet below the hem
foot1 = [(482, 598), (476, 620), (458, 628), (478, 633), (492, 626), (494, 604)]
foot1.append(foot1[0])
add(wob(foot1, amp=0.8, closed=True, step=10), fill="white", sw=2.2)
foot2 = [(522, 600), (518, 624), (500, 632), (520, 637), (534, 629), (536, 606)]
foot2.append(foot2[0])
add(wob(foot2, amp=0.8, closed=True, step=10), fill="white", sw=2.2)

# head in profile, facing left
head = [
    (505, 128), (482, 116), (458, 132), (446, 150),   # crown, forehead
    (443, 160), (434, 172),                            # brow, nose bridge to tip
    (444, 179), (439, 186),                            # under nose, lips
    (447, 196), (466, 205), (492, 203), (512, 188),   # chin, jaw, back of jaw
    (517, 162), (514, 140),
]
head.append(head[0])
add(wob(head, amp=0.9, closed=True, step=12), fill="white", sw=2.4)

# eye and nostril (minimal, like the ref rider's face)
add(wob([(451, 162), (461, 164)], amp=0.3, step=6), sw=1.8)
EL.append((f'M {455.5} {161.5} a 1.5 1.5 0 1 0 0.1 0', INK, 0, "none", None))
EL.append((f'M {441} {176} a 1.2 1.2 0 1 0 0.1 0', INK, 0, "none", None))

# hair at the back of the head
add(wob([(504, 128), (514, 150), (516, 172)], amp=0.8, step=10), sw=1.6)

# two small horns
horn1 = [(462, 127), (455, 106), (452, 88), (463, 104), (473, 122)]
horn1.append(horn1[0])
add(wob(horn1, amp=0.7, closed=True, step=9), fill="white", sw=2.0)
horn2 = [(486, 121), (485, 100), (488, 82), (496, 100), (499, 117)]
horn2.append(horn2[0])
add(wob(horn2, amp=0.7, closed=True, step=9), fill="white", sw=2.0)

# beard: one wide soft shape covering the chest, simple pointed tip
beard = [
    (443, 188), (422, 235), (410, 292), (410, 340),   # front edge
    (426, 366), (444, 372),                           # tip
    (460, 348), (470, 300), (476, 250), (480, 212),   # back edge up
    (468, 203), (452, 197),
]
beard.append(beard[0])
add(wob(beard, amp=1.0, closed=True, step=14), fill="white", sw=2.2)
# two calm strands
add(wob([(444, 212), (430, 268), (424, 330)], amp=1.0, step=16), sw=1.5)
add(wob([(460, 214), (450, 272), (446, 336)], amp=1.0, step=16), sw=1.5)

# ================= ARM below the beard, reaching forward with the keys =================
add(wob([(502, 252), (472, 292), (436, 314)], amp=1.0, step=14), sw=2.4)
add(wob([(508, 268), (482, 304), (446, 326)], amp=1.0, step=14), sw=2.4)
hand = [(436, 314), (424, 318), (418, 328), (428, 334), (440, 330), (444, 322)]
hand.append(hand[0])
add(wob(hand, amp=0.7, closed=True, step=8), fill="white", sw=2.2)

# ================= one clear key on a ring =================
EL.append((cr_path(subdiv([(408 + 11 * math.cos(2 * math.pi * i / 12), 348 + 11 * math.sin(2 * math.pi * i / 12)) for i in range(13)], 6), closed=False), "none", 1.9, INK, None))
a = math.radians(95)
bcx, bcy = 408 + 19 * math.cos(a), 348 + 19 * math.sin(a)
pts = [(bcx + 9 * math.cos(2 * math.pi * i / 12), bcy + 9 * math.sin(2 * math.pi * i / 12)) for i in range(13)]
add(cr_path([jit(p, 0.5) for p in pts]), sw=1.8)  # bow
sx, sy = bcx + 9 * math.cos(a), bcy + 9 * math.sin(a)
ex, ey = sx + 46 * math.cos(a), sy + 46 * math.sin(a)
add(wob([(sx, sy), (ex, ey)], amp=0.6, step=8), sw=1.8)  # shaft
pa = a - math.pi / 2
for f, ln in ((0.68, 11), (0.94, 14)):
    tx, ty = sx + 46 * f * math.cos(a), sy + 46 * f * math.sin(a)
    add(wob([(tx, ty), (tx + ln * math.cos(pa), ty + ln * math.sin(pa))], amp=0.4, step=5), sw=1.8)

# ================= assemble =================
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">']
parts.append(f'<rect width="{W}" height="{H}" fill="white"/>')
parts.append("<defs>" + "".join(DEFS) + "</defs>")
for d, fill, sw, stroke, clip in EL:
    cl = f' clip-path="url(#{clip})"' if clip else ""
    if sw > 0:
        parts.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{cl}/>')
    else:
        parts.append(f'<path d="{d}" fill="{fill}" stroke="none"{cl}/>')
parts.append("</svg>")

with open("philemon_01.svg", "w") as f:
    f.write("\n".join(parts))
print("ok", len(EL), "paths")
