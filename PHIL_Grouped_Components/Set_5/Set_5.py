"""
Single fused body — build123d

All five sections built as separate solids then fused into one body.
Pre-build strategy avoids sketch-consumption issues inside BuildPart.

  z=50.35 → 40.35  circle extrude  (r≈48mm)
  z=40.35 → 30.35  chamfer loft    (r: 48→40mm)
  z=30.35 → 20.35  circle extrude  (r≈40mm)
  z=20.35 → 10.35  chamfer loft    (r: 40→48mm)
  z=10.35 →  0.35  circle extrude  (r≈48mm)

Shared origin: ORIGIN_X=538088.7891, ORIGIN_Y=235945.5469
"""

from build123d import *
from ocp_vscode import show
from copy import copy

ORIGIN_X = 538088.7891
ORIGIN_Y = 235945.5469

def norm(pts):
    return [(p[0]-ORIGIN_X, p[1]-ORIGIN_Y, p[2]) for p in pts]

def make_face_at(pts_local, z):
    """Return a BuildSketch face at the given z height."""
    with BuildSketch(Plane.XY.offset(z)) as sk:
        with BuildLine():
            Polyline(*[Vector(x, y) for (x, y, _) in pts_local], close=True)
        make_face()
    return sk

# ── raw point data ─────────────────────────────────────────────────

raw_extrude = [
    (538180.1562, 236014.3359, 50.3498),(538182.7734, 236007.6367, 50.3498),
    (538184.375,  236000.6445, 50.3498),(538184.9219, 235993.4766, 50.3498),
    (538184.375,  235986.3086, 50.3498),(538182.7734, 235979.3164, 50.3498),
    (538180.1562, 235972.6172, 50.3498),(538176.5625, 235966.4062, 50.3498),
    (538172.0703, 235960.7812, 50.3498),(538166.7969, 235955.8984, 50.3498),
    (538160.8594, 235951.8555, 50.3498),(538154.4141, 235948.75,   50.3498),
    (538147.5391, 235946.6211, 50.3498),(538140.4297, 235945.5469, 50.3498),
    (538133.2422, 235945.5469, 50.3498),(538126.1328, 235946.6211, 50.3498),
    (538119.2969, 235948.75,   50.3498),(538112.8125, 235951.8555, 50.3498),
    (538106.875,  235955.8984, 50.3498),(538101.6016, 235960.7812, 50.3498),
    (538097.1484, 235966.4062, 50.3498),(538093.5547, 235972.6172, 50.3498),
    (538090.9375, 235979.3164, 50.3498),(538089.3359, 235986.3086, 50.3498),
    (538088.7891, 235993.4766, 50.3498),(538089.3359, 236000.6445, 50.3498),
    (538090.9375, 236007.6367, 50.3498),(538093.5547, 236014.3359, 50.3498),
    (538097.1484, 236020.5469, 50.3498),(538101.6016, 236026.1719, 50.3498),
    (538106.875,  236031.0547, 50.3498),(538112.8125, 236035.0977, 50.3498),
    (538119.2969, 236038.2227, 50.3498),(538126.1328, 236040.332,  50.3498),
    (538133.2422, 236041.4062, 50.3498),(538140.4297, 236041.4062, 50.3498),
    (538147.5391, 236040.332,  50.3498),(538154.4141, 236038.2227, 50.3498),
    (538160.8594, 236035.0977, 50.3498),(538166.7969, 236031.0547, 50.3498),
    (538172.0703, 236026.1719, 50.3498),(538176.5625, 236020.5469, 50.3498),
]

raw_outer_b2 = [
    (538166.7969, 236031.0547, 40.3498),(538172.0703, 236026.1719, 40.3498),
    (538176.5625, 236020.5469, 40.3498),(538180.1562, 236014.3359, 40.3498),
    (538182.7734, 236007.6367, 40.3498),(538184.375,  236000.6445, 40.3498),
    (538184.9219, 235993.4766, 40.3498),(538184.375,  235986.3086, 40.3498),
    (538182.7734, 235979.3164, 40.3498),(538180.1562, 235972.6172, 40.3498),
    (538176.5625, 235966.4062, 40.3498),(538172.0703, 235960.7812, 40.3498),
    (538166.7969, 235955.8984, 40.3498),(538160.8594, 235951.8555, 40.3498),
    (538154.4141, 235948.75,   40.3498),(538147.5391, 235946.6211, 40.3498),
    (538140.4297, 235945.5469, 40.3498),(538133.2422, 235945.5469, 40.3498),
    (538126.1328, 235946.6211, 40.3498),(538119.2969, 235948.75,   40.3498),
    (538112.8125, 235951.8555, 40.3498),(538106.875,  235955.8984, 40.3498),
    (538101.6016, 235960.7812, 40.3498),(538097.1484, 235966.4062, 40.3498),
    (538093.5547, 235972.6172, 40.3498),(538090.9375, 235979.3164, 40.3498),
    (538089.3359, 235986.3086, 40.3498),(538088.7891, 235993.4766, 40.3498),
    (538089.3359, 236000.6445, 40.3498),(538090.9375, 236007.6367, 40.3498),
    (538093.5547, 236014.3359, 40.3498),(538097.1484, 236020.5469, 40.3498),
    (538101.6016, 236026.1719, 40.3498),(538106.875,  236031.0547, 40.3498),
    (538112.8125, 236035.0977, 40.3498),(538119.2969, 236038.2227, 40.3498),
    (538126.1328, 236040.332,  40.3498),(538133.2422, 236041.4062, 40.3498),
    (538140.4297, 236041.4062, 40.3498),(538147.5391, 236040.332,  40.3498),
    (538154.4141, 236038.2227, 40.3498),(538160.8594, 236035.0977, 40.3498),
]

raw_inner_b2_b3 = [
    (538158.7109, 236026.9727, 30.3498),(538163.9453, 236022.9102, 30.3498),
    (538168.3984, 236018.0469, 30.3498),(538172.0312, 236012.5195, 30.3498),
    (538174.6875, 236006.4648, 30.3498),(538176.2891, 236000.0586, 30.3498),
    (538176.8359, 235993.4766, 30.3498),(538176.2891, 235986.8945, 30.3498),
    (538174.6875, 235980.4883, 30.3498),(538172.0312, 235974.4336, 30.3498),
    (538168.3984, 235968.9062, 30.3498),(538163.9453, 235964.043,  30.3498),
    (538158.7109, 235960.0,    30.3498),(538152.9297, 235956.8555, 30.3498),
    (538146.6797, 235954.707,  30.3498),(538140.1562, 235953.6133, 30.3498),
    (538133.5547, 235953.6133, 30.3498),(538127.0312, 235954.707,  30.3498),
    (538120.7812, 235956.8555, 30.3498),(538114.9609, 235960.0,    30.3498),
    (538109.7656, 235964.043,  30.3498),(538105.2734, 235968.9062, 30.3498),
    (538101.6797, 235974.4336, 30.3498),(538099.0234, 235980.4883, 30.3498),
    (538097.3828, 235986.8945, 30.3498),(538096.8359, 235993.4766, 30.3498),
    (538097.3828, 236000.0586, 30.3498),(538099.0234, 236006.4648, 30.3498),
    (538101.6797, 236012.5195, 30.3498),(538105.2734, 236018.0469, 30.3498),
    (538109.7656, 236022.9102, 30.3498),(538114.9609, 236026.9727, 30.3498),
    (538120.7812, 236030.1172, 30.3498),(538127.0312, 236032.2461, 30.3498),
    (538133.5547, 236033.3398, 30.3498),(538140.1562, 236033.3398, 30.3498),
    (538146.6797, 236032.2461, 30.3498),(538152.9297, 236030.1172, 30.3498),
]

raw_inner_b4 = [
    (538174.6875, 236006.4648, 20.3498),(538176.2891, 236000.0586, 20.3498),
    (538176.8359, 235993.4766, 20.3498),(538176.2891, 235986.8945, 20.3498),
    (538174.6875, 235980.4883, 20.3498),(538172.0312, 235974.4336, 20.3498),
    (538168.3984, 235968.9062, 20.3498),(538163.9453, 235964.043,  20.3498),
    (538158.7109, 235960.0,    20.3498),(538152.9297, 235956.8555, 20.3498),
    (538146.6797, 235954.707,  20.3498),(538140.1562, 235953.6133, 20.3498),
    (538133.5547, 235953.6133, 20.3498),(538127.0312, 235954.707,  20.3498),
    (538120.7812, 235956.8555, 20.3498),(538114.9609, 235960.0,    20.3498),
    (538109.7656, 235964.043,  20.3498),(538105.2734, 235968.9062, 20.3498),
    (538101.6797, 235974.4336, 20.3498),(538099.0234, 235980.4883, 20.3498),
    (538097.3828, 235986.8945, 20.3498),(538096.8359, 235993.4766, 20.3498),
    (538097.3828, 236000.0586, 20.3498),(538099.0234, 236006.4648, 20.3498),
    (538101.6797, 236012.5195, 20.3498),(538105.2734, 236018.0469, 20.3498),
    (538109.7656, 236022.9102, 20.3498),(538114.9609, 236026.9727, 20.3498),
    (538120.7812, 236030.1172, 20.3498),(538127.0312, 236032.2461, 20.3498),
    (538133.5547, 236033.3398, 20.3498),(538140.1562, 236033.3398, 20.3498),
    (538146.6797, 236032.2461, 20.3498),(538152.9297, 236030.1172, 20.3498),
    (538158.7109, 236026.9727, 20.3498),(538163.9453, 236022.9102, 20.3498),
    (538168.3984, 236018.0469, 20.3498),(538172.0312, 236012.5195, 20.3498),
]

raw_outer_b4_b5 = [
    (538184.375,  236000.6445, 10.3498),(538184.9219, 235993.4766, 10.3498),
    (538184.375,  235986.3086, 10.3498),(538182.7734, 235979.3164, 10.3498),
    (538180.1562, 235972.6172, 10.3498),(538176.5625, 235966.4062, 10.3498),
    (538172.0703, 235960.7812, 10.3498),(538166.7969, 235955.8984, 10.3498),
    (538160.8594, 235951.8555, 10.3498),(538154.4141, 235948.75,   10.3498),
    (538147.5391, 235946.6211, 10.3498),(538140.4297, 235945.5469, 10.3498),
    (538133.2422, 235945.5469, 10.3498),(538126.1328, 235946.6211, 10.3498),
    (538119.2969, 235948.75,   10.3498),(538112.8125, 235951.8555, 10.3498),
    (538106.875,  235955.8984, 10.3498),(538101.6016, 235960.7812, 10.3498),
    (538097.1484, 235966.4062, 10.3498),(538093.5547, 235972.6172, 10.3498),
    (538090.9375, 235979.3164, 10.3498),(538089.3359, 235986.3086, 10.3498),
    (538088.7891, 235993.4766, 10.3498),(538089.3359, 236000.6445, 10.3498),
    (538090.9375, 236007.6367, 10.3498),(538093.5547, 236014.3359, 10.3498),
    (538097.1484, 236020.5469, 10.3498),(538101.6016, 236026.1719, 10.3498),
    (538106.875,  236031.0547, 10.3498),(538112.8125, 236035.0977, 10.3498),
    (538119.2969, 236038.2227, 10.3498),(538126.1328, 236040.332,  10.3498),
    (538133.2422, 236041.4062, 10.3498),(538140.4297, 236041.4062, 10.3498),
    (538147.5391, 236040.332,  10.3498),(538154.4141, 236038.2227, 10.3498),
    (538160.8594, 236035.0977, 10.3498),(538166.7969, 236031.0547, 10.3498),
    (538172.0703, 236026.1719, 10.3498),(538176.5625, 236020.5469, 10.3498),
    (538180.1562, 236014.3359, 10.3498),(538182.7734, 236007.6367, 10.3498),
]

# normalise
pts_extrude     = norm(raw_extrude)
pts_outer_b2    = norm(raw_outer_b2)
pts_inner_b2_b3 = norm(raw_inner_b2_b3)
pts_inner_b4    = norm(raw_inner_b4)
pts_outer_b4_b5 = norm(raw_outer_b4_b5)

# ══════════════════════════════════════════════════════════════════
# Pre-build all five solids outside BuildPart
# ══════════════════════════════════════════════════════════════════

# Body 1 — circle extrude z=50.35 → 40.35
with BuildPart() as b1:
    with BuildSketch(Plane.XY.offset(pts_extrude[0][2])):
        with BuildLine():
            Polyline(*[Vector(x, y) for (x, y, _) in pts_extrude], close=True)
        make_face()
    extrude(amount=10, dir=(0, 0, -1))

# Body 2 — chamfer loft z=40.35 → 30.35
with BuildPart() as b2:
    with BuildSketch(Plane.XY.offset(pts_outer_b2[0][2])):
        with BuildLine():
            Polyline(*[Vector(x, y) for (x, y, _) in pts_outer_b2], close=True)
        make_face()
    with BuildSketch(Plane.XY.offset(pts_inner_b2_b3[0][2])):
        with BuildLine():
            Polyline(*[Vector(x, y) for (x, y, _) in pts_inner_b2_b3], close=True)
        make_face()
    loft(ruled=True)

# Body 3 — circle extrude z=30.35 → 20.35
with BuildPart() as b3:
    with BuildSketch(Plane.XY.offset(pts_inner_b2_b3[0][2])):
        with BuildLine():
            Polyline(*[Vector(x, y) for (x, y, _) in pts_inner_b2_b3], close=True)
        make_face()
    extrude(amount=10, dir=(0, 0, -1))

# Body 4 — chamfer loft z=20.35 → 10.35
with BuildPart() as b4:
    with BuildSketch(Plane.XY.offset(pts_inner_b4[0][2])):
        with BuildLine():
            Polyline(*[Vector(x, y) for (x, y, _) in pts_inner_b4], close=True)
        make_face()
    with BuildSketch(Plane.XY.offset(pts_outer_b4_b5[0][2])):
        with BuildLine():
            Polyline(*[Vector(x, y) for (x, y, _) in pts_outer_b4_b5], close=True)
        make_face()
    loft(ruled=True)

# Body 5 — circle extrude z=10.35 → 0.35
with BuildPart() as b5:
    with BuildSketch(Plane.XY.offset(pts_outer_b4_b5[0][2])):
        with BuildLine():
            Polyline(*[Vector(x, y) for (x, y, _) in pts_outer_b4_b5], close=True)
        make_face()
    extrude(amount=10, dir=(0, 0, -1))

# ══════════════════════════════════════════════════════════════════
# Fuse all into one body
# ══════════════════════════════════════════════════════════════════
s1 = b1.part.solids()[0]
s2 = b2.part.solids()[0]
s3 = b3.part.solids()[0]
s4 = b4.part.solids()[0]
s5 = b5.part.solids()[0]

result = s1.fuse(s2).fuse(s3).fuse(s4).fuse(s5).solids()[0]

# Copy translated slightly in X so both are visible
result_copy = copy(result)


# ══════════════════════════════════════════════════════════════════
# NEW BODY — extrude.txt circle z=50.35 → 80.35 (+30mm in +Z)
# Points sorted by angle (source file had 4 out-of-order points)
# Fused with result_copy (the red body)
# ══════════════════════════════════════════════════════════════════
import math

raw_new = [
    (538166.7969, 235955.8984, 50.3498),(538172.0703, 235960.7812, 50.3498),
    (538176.5625, 235966.4062, 50.3498),(538180.1562, 235972.6172, 50.3498),
    (538182.7734, 235979.3164, 50.3498),(538184.375,  235986.3086, 50.3498),
    (538184.9219, 235993.4766, 50.3498),(538184.375,  236000.6445, 50.3498),
    (538182.7734, 236007.6367, 50.3498),(538180.1562, 236014.3359, 50.3498),
    (538176.5625, 236020.5469, 50.3498),(538172.0703, 236026.1719, 50.3498),
    (538166.7969, 236031.0547, 50.3498),(538160.8594, 236035.0977, 50.3498),
    (538154.4141, 236038.2227, 50.3498),(538147.5391, 236040.332,  50.3498),
    (538140.4297, 236041.4062, 50.3498),(538133.2422, 236041.4062, 50.3498),
    (538126.1328, 236040.332,  50.3498),(538119.2969, 236038.2227, 50.3498),
    (538112.8125, 236035.0977, 50.3498),(538106.875,  236031.0547, 50.3498),
    (538101.6016, 236026.1719, 50.3498),(538097.1484, 236020.5469, 50.3498),
    (538093.5547, 236014.3359, 50.3498),(538090.9375, 236007.6367, 50.3498),
    (538089.3359, 236000.6445, 50.3498),(538089.3359, 235986.3086, 50.3498),
    (538090.9375, 235979.3164, 50.3498),(538088.7891, 235993.4766, 50.3498),
    (538093.5547, 235972.6172, 50.3498),(538097.1484, 235966.4062, 50.3498),
    (538101.6016, 235960.7812, 50.3498),(538106.875,  235955.8984, 50.3498),
    (538112.8125, 235951.8555, 50.3498),(538119.2969, 235948.75,   50.3498),
    (538126.1328, 235946.6211, 50.3498),(538133.2422, 235945.5469, 50.3498),
    (538140.4297, 235945.5469, 50.3498),(538147.5391, 235946.6211, 50.3498),
    (538154.4141, 235948.75,   50.3498),(538160.8594, 235951.8555, 50.3498),
]

# Sort by angle around centroid to fix out-of-order points
pts_new_raw = [(p[0], p[1]) for p in raw_new]
cx = sum(p[0] for p in pts_new_raw) / len(pts_new_raw)
cy = sum(p[1] for p in pts_new_raw) / len(pts_new_raw)
pts_new_raw_sorted = sorted(pts_new_raw, key=lambda p: math.atan2(p[1]-cy, p[0]-cx))

pts_new = [(p[0]-ORIGIN_X, p[1]-ORIGIN_Y, 50.3498) for p in pts_new_raw_sorted]
z_new = pts_new[0][2]  # 50.3498

with BuildPart() as b_new:
    with BuildSketch(Plane.XY.offset(z_new)):
        with BuildLine():
            Polyline(*[Vector(x, y) for (x, y, _) in pts_new], close=True)
        make_face()
    extrude(amount=30, dir=(0, 0, 1))

s_new = b_new.part.solids()[0]

# Fuse new body with the red copy
result_copy_fused = result_copy.fuse(s_new).solids()[0]


# ══════════════════════════════════════════════════════════════════
# CUT TOOL — Cut.txt circle r≈8.5mm, centred at (48.06, 47.93)
# Sketch at z=50.3498, extruded both directions 70mm
# Cuts z=-19.65 → z=120.35 — passes through both bodies entirely
# ══════════════════════════════════════════════════════════════════

raw_cut = [
    (538145.3516, 235993.4766, 50.3498),(538145.0391, 235995.6836, 50.3498),
    (538144.2188, 235997.7344, 50.3498),(538142.8516, 235999.4922, 50.3498),
    (538141.0938, 236000.8398, 50.3498),(538139.0625, 236001.6797, 50.3498),
    (538136.8359, 236001.9727, 50.3498),(538134.6484, 236001.6797, 50.3498),
    (538132.5781, 236000.8398, 50.3498),(538130.8203, 235999.4922, 50.3498),
    (538129.4922, 235997.7344, 50.3498),(538128.6328, 235995.6836, 50.3498),
    (538128.3594, 235993.4766, 50.3498),(538128.6328, 235991.2695, 50.3498),
    (538129.4922, 235989.2383, 50.3498),(538130.8203, 235987.4609, 50.3498),
    (538132.5781, 235986.1133, 50.3498),(538134.6484, 235985.2734, 50.3498),
    (538136.8359, 235984.9805, 50.3498),(538139.0625, 235985.2734, 50.3498),
    (538141.0938, 235986.1133, 50.3498),(538142.8516, 235987.4609, 50.3498),
    (538144.2188, 235989.2383, 50.3498),(538145.0391, 235991.2695, 50.3498),
]

pts_cut = norm(raw_cut)
z_cut = pts_cut[0][2]  # 50.3498

# Build the cut tool — extrude 70mm in both +Z and -Z from sketch plane
with BuildPart() as cut_tool:
    with BuildSketch(Plane.XY.offset(z_cut)):
        with BuildLine():
            Polyline(*[Vector(x, y) for (x, y, _) in pts_cut], close=True)
        make_face()
    extrude(amount=70, both=True)

cut_solid = cut_tool.part.solids()[0]

# Apply cut to both bodies
result_cut        = result.cut(cut_solid).solids()[0].moved(Location((970, 850, 0)))
result_copy_cut   = result_copy_fused.cut(cut_solid).solids()[0]
result_copy_moved = result_copy_cut.moved(Location((1092, 864.5, 0)))


# ══════════════════════════════════════════════════════════════════
# CHAMBER LID — imported as separate assembly part
# ══════════════════════════════════════════════════════════════════

# ---------------------------------------------------------------------------
# Body 1
# ---------------------------------------------------------------------------
pts1 = [
    (0,       0),
    (0,       500),
    (420.27,  1983.75),
    (1540.47, 1983.75),
    (1960.98, 500),
    (1960.98, 0),
]

with BuildSketch() as sk1:
    with BuildLine():
        Polyline(*pts1, close=True)
    make_face()

with BuildPart() as lid_part1:
    add(sk1.sketch)
    extrude(amount=105.75)

# ---------------------------------------------------------------------------
# Body 2
# ---------------------------------------------------------------------------
pts2 = [
    (100,     0),
    (100,     486.11),
    (496.09,  1883.75),
    (1464.88, 1883.75),
    (1860.98, 486.11),
    (1860.98, 0),
]

with BuildSketch() as sk2:
    with BuildLine():
        Polyline(*pts2, close=True)
    make_face()

with BuildPart() as lid_part2:
    add(sk2.sketch)
    extrude(amount=55.75)

lid_part2_moved = lid_part2.part.moved(Location((0, 0, 50)))
lid_result = lid_part1.part - lid_part2_moved

# ---------------------------------------------------------------------------
# Box cuts
# ---------------------------------------------------------------------------
with BuildPart() as lid_part3:
    Box(965, 1415, 110, align=(Align.MIN, Align.MIN, Align.MIN))
box_moved = lid_part3.part.moved(Location((497.97, 466.25, 0)))
lid_result = lid_result - box_moved

with BuildPart() as lid_part4:
    Box(1005, 1455, 30, align=(Align.MIN, Align.MIN, Align.MIN))
box2_moved = lid_part4.part.moved(Location((477.97, 446.25, 0)))
lid_result = lid_result - box2_moved

# ---------------------------------------------------------------------------
# Holes
# ---------------------------------------------------------------------------
hole_locations = [
    (50.01,   243.07),
    (249.04,  1184.93),
    (980.48,  1933.77),
    (1712.93, 1184.93),
    (1910.98, 243.07),
]

for x, y in hole_locations:
    with BuildPart() as hole:
        with Locations([(x, y, 0)]):
            Cylinder(radius=35, height=30, align=(Align.CENTER, Align.CENTER, Align.MIN))
    lid_result = lid_result - hole.part

for x, y in hole_locations:
    with BuildPart() as small_hole:
        with Locations([(x, y, 0)]):
            Cylinder(radius=35.62/2, height=1000, align=(Align.CENTER, Align.CENTER, Align.MIN))
    lid_result = lid_result - small_hole.part

for x, y in hole_locations:
    with BuildPart() as chamfer_body:
        with Locations([(x, y, 0)]):
            Cone(
                bottom_radius=35,
                top_radius=35.62 / 2,
                height=20,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
    chamfer_moved = chamfer_body.part.moved(Location((0, 0, 30)))
    lid_result = lid_result - chamfer_moved

# ---------------------------------------------------------------------------
# Hollow wall
# ---------------------------------------------------------------------------
with BuildPart() as wall_body:
    Box(990, 1440, 27.5, align=(Align.MIN, Align.MIN, Align.MIN))
    with Locations([(12.5, 12.5, 0)]):
        Box(965, 1415, 27.5, align=(Align.MIN, Align.MIN, Align.MIN),
            mode=Mode.SUBTRACT)

wall_moved = wall_body.part.moved(Location((485.47, 453.75, 0)))

# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------
lines = [
    "ETH Zurich",
    "Cell Systems Dynamics Group",
    "Designed by Philip Dettinger",
]

text_height   = 69.28 * 1.2
line_spacing  = text_height * 1.5
text_parts    = []

for i, line in enumerate(lines):
    with BuildPart() as text_part:
        with BuildSketch(Plane(origin=(0,0,0), x_dir=(1,0,0), z_dir=(0,0,-1))) as ts:
            Text(line, font_size=text_height, align=(Align.MIN, Align.CENTER))
        extrude(amount=6, dir=(0, 0, 1))
    moved = text_part.part.moved(Location((0, -i * line_spacing, 0)))
    text_parts.append(moved)

text_body = text_parts[0]
for tp in text_parts[1:]:
    text_body = text_body.fuse(tp)
text_body = text_body.moved(Location((400, 343, 0)))
lid_result = lid_result - text_body

# ══════════════════════════════════════════════════════════════════
# Show full assembly — all parts together
# ══════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════
# HANDLE — imported as assembly part (no export, show_object → show)
# ══════════════════════════════════════════════════════════════════

# ── Path ─────────────────────────────────────────────────────────
path_points = [
    (0.0,     0.0,    0.0),
    (454.65,  0.0,    0.0),
    (454.65, -1200.0, 0.0),
    (0.0,    -1200.0, 0.0),
]

with BuildLine() as bl:
    Polyline(*[Vector(*p) for p in path_points])
sweep_path = bl.wire()

# ── Profile face — 100x100 rectangle ─────────────────────────────
profile_plane = Plane(
    origin = Vector(*path_points[0]),
    x_dir  = Vector(0, 1, 0),
    z_dir  = Vector(1, 0, 0),
)
with BuildSketch(profile_plane) as sk:
    Rectangle(100, 100)
profile_face = sk.face().located(profile_plane.location)

# ── Sweep ─────────────────────────────────────────────────────────
with BuildPart() as h_part:
    sweep(sections=profile_face, path=sweep_path, is_frenet=True, transition=Transition.RIGHT)
h_solid = h_part.solid()

# ── Fillet inner Z edge — 50mm ────────────────────────────────────
inner_z_edges = ShapeList([e for e in h_solid.edges()
    if abs(e.bounding_box().min.X - 404.65) < 1.0
    and abs(e.bounding_box().max.X - 404.65) < 1.0
    and (e.bounding_box().max.Z - e.bounding_box().min.Z) > 90
    and (abs(e.bounding_box().min.Y + 50) < 1.0 or abs(e.bounding_box().min.Y + 1150) < 1.0)
    and abs(e.bounding_box().max.Y - e.bounding_box().min.Y) < 1.0])
h_solid = h_solid.fillet(50, inner_z_edges)

# ── Cylinder at origin ────────────────────────────────────────────
with BuildPart() as cyl_part:
    with BuildSketch(Plane.XZ):
        Circle(67.5)
    extrude(amount=100)
cylinder = cyl_part.solid()

# ── Fillet X + Arc edges — 30mm ──────────────────────────────────
def get_axis(e):
    ebb = e.bounding_box()
    dx = ebb.max.X - ebb.min.X
    dy = ebb.max.Y - ebb.min.Y
    dz = ebb.max.Z - ebb.min.Z
    if dz > max(dx, dy) * 2:   return 'Z'
    elif dy > max(dx, dz) * 2: return 'Y'
    elif dx > max(dy, dz) * 2: return 'X'
    else:                       return 'Arc'

x_and_arc = ShapeList([e for e in h_solid.edges() if get_axis(e) in ('X', 'Arc')])
h_solid = h_solid.fillet(30, x_and_arc)

edges_1240 = ShapeList([e for e in h_solid.edges()
    if get_axis(e) == 'Y' and abs(e.length - 1240.0) < 1.0])
h_solid = h_solid.fillet(49.9, edges_1240)

# ── Base extrude ──────────────────────────────────────────────────
extrude_points = [
    (19.0625, 50.0, -134.9943), (19.0625, -50.0, -134.9943),
    (546.6797, 50.0, -134.9943), (546.6797, -1250.0, -134.9943),
    (19.0625, -1250.0, -134.9943), (19.0625, -1150.0, -134.9943),
    (400.8594, -1150.0, -134.9943), (406.0938, -1149.7266, -134.9943),
    (411.25, -1148.9063, -134.9943), (416.3281, -1147.5391, -134.9943),
    (421.2109, -1145.6641, -134.9943), (425.8594, -1143.3008, -134.9943),
    (430.2734, -1140.4492, -134.9943), (434.3359, -1137.1484, -134.9943),
    (438.0078, -1133.457, -134.9943), (441.3281, -1129.375, -134.9943),
    (444.1797, -1125.0, -134.9943), (446.5625, -1120.332, -134.9943),
    (448.4375, -1115.4492, -134.9943), (449.7656, -1110.3906, -134.9943),
    (450.5859, -1105.2148, -134.9943), (450.8594, -1100.0, -134.9943),
    (450.8594, -100.0, -134.9943), (450.5859, -94.7656, -134.9943),
    (449.7656, -89.5898, -134.9943), (448.4375, -84.5313, -134.9943),
    (446.5625, -79.6484, -134.9943), (444.1797, -75.0, -134.9943),
    (441.3281, -70.6055, -134.9943), (438.0078, -66.543, -134.9943),
    (434.3359, -62.832, -134.9943), (430.2734, -59.5313, -134.9943),
    (425.8594, -56.6992, -134.9943), (421.2109, -54.3164, -134.9943),
    (416.3281, -52.4414, -134.9943), (411.25, -51.0938, -134.9943),
    (406.0938, -50.2734, -134.9943), (400.8594, -50.0, -134.9943),
]
ordered_pts = ([extrude_points[0], extrude_points[2], extrude_points[3],
                extrude_points[4], extrude_points[5]] + extrude_points[6:] + [extrude_points[1]])

base_plane = Plane(origin=Vector(0, 0, -134.9943), x_dir=Vector(1, 0, 0), z_dir=Vector(0, 0, -1))
with BuildPart() as base_part:
    with BuildSketch(base_plane):
        with BuildLine():
            Polyline(*[Vector(p[0], -p[1], 0) for p in ordered_pts], close=True)
        make_face()
    extrude(amount=-25)
base_solid = base_part.solid()

cylinder = cylinder.translate(Vector(-45.32, 50, 0))

hole_plane = Plane(origin=Vector(-45.32, -60, 0), x_dir=Vector(1, 0, 0), z_dir=Vector(0, -1, 0))
with BuildPart() as hole_part:
    with BuildSketch(hole_plane):
        Circle(29.95 / 2)
    extrude(amount=120)
hole_tool = hole_part.solid()

with BuildPart() as hole_body_part:
    with BuildSketch(Plane(origin=Vector(-45.32, -50, 0), x_dir=Vector(1, 0, 0), z_dir=Vector(0, 1, 0))):
        Circle(29.95 / 2)
    extrude(amount=100)
hole_body = hole_body_part.solid()

mirror_plane = Plane(origin=Vector(0, -600, 0), x_dir=Vector(1, 0, 0), z_dir=Vector(0, 1, 0))
cylinder_mirrored = mirror(cylinder, about=mirror_plane)
hole_body_mirrored = mirror(hole_body, about=mirror_plane)

handle = h_solid.fuse(cylinder).fuse(cylinder_mirrored)
handle = handle.cut(hole_body).cut(hole_body_mirrored)

extrude_pts2 = [
    (-66.6406, -1250.0, -109.9943), (-66.6406, -1250.0, -134.9943),
    (-17.6562, -1250.0, -134.9943), (-54.7656, -1250.0, -109.9943),
    (-51.1328, -1250.0, -114.3702), (-47.1484, -1250.0, -118.4365),
    (-42.8516, -1250.0, -122.1664), (-38.2812, -1250.0, -125.5353),
    (-33.4375, -1250.0, -128.5209), (-28.3594, -1250.0, -131.1035),
    (-23.0859, -1250.0, -133.2661),
]
ordered_pts2 = [extrude_pts2[0], extrude_pts2[1], extrude_pts2[2]] + list(reversed(extrude_pts2[3:]))

plane2 = Plane(origin=Vector(0, -1250, 0), x_dir=Vector(1, 0, 0), z_dir=Vector(0, 1, 0))
with BuildPart() as part2:
    with BuildSketch(plane2):
        with BuildLine():
            Polyline(*[Vector(p[0], -p[2], 0) for p in ordered_pts2], close=True)
        make_face()
    extrude(amount=100)
extrude_solid2 = part2.solid()

handle_copy = handle.translate(Vector(0, 0, -2.45))
base_solid = base_solid.translate(Vector(-46.209, 0, 67.494))
base_cut = base_solid.cut(handle_copy)
extrude_solid2 = extrude_solid2.translate(Vector(-46.206, 0, 67.494))

# Move handle, base_cut, extrude_solid2 by +1771.3 in Y then +952.5 in X
handle        = handle.translate(Vector(952.5, 1771.3, 0))
base_cut      = base_cut.translate(Vector(952.5, 1771.3, 0))
extrude_solid2 = extrude_solid2.translate(Vector(952.5, 1771.3, 0))



# ══════════════════════════════════════════════════════════════════
# USB BACK VB1 — H-profile + Slot Cut + Hole Cuts + Fillets
# ══════════════════════════════════════════════════════════════════

usb_back_cut_raw = [
    (0.0, -22.5,    104.9887),
    (0.0, -22.5,     42.4887),
    (0.0, -22.4023,  40.4718),
    (0.0, -22.1289,  38.4711),
    (0.0, -21.6797,  36.5028),
    (0.0, -21.0547,  34.5827),
    (0.0, -20.2539,  32.7263),
    (0.0, -19.3164,  30.9484),
    (0.0, -18.2031,  29.2635),
    (0.0, -16.9336,  27.6851),
    (0.0, -15.5469,  26.2258),
    (0.0, -14.0234,  24.8975),
    (0.0, -12.3828,  23.7108),
    (0.0, -10.6445,  22.6753),
    (0.0,  -8.8281,  21.7993),
    (0.0,  -6.9531,  21.0899),
    (0.0,  -5.0,     20.5528),
    (0.0,  -3.0078,  20.1923),
    (0.0,  -0.9961,  20.0113),
    (0.0,   1.0156,  20.0113),
    (0.0,   3.0273,  20.1923),
    (0.0,   5.0195,  20.5528),
    (0.0,   6.9531,  21.0899),
    (0.0,   8.8477,  21.7993),
    (0.0,  10.6641,  22.6753),
    (0.0,  12.4023,  23.7108),
    (0.0,  14.043,   24.8975),
    (0.0,  15.5664,  26.2258),
    (0.0,  16.9531,  27.6851),
    (0.0,  18.2031,  29.2635),
    (0.0,  19.3164,  30.9484),
    (0.0,  20.2734,  32.7263),
    (0.0,  21.0742,  34.5827),
    (0.0,  21.6992,  36.5028),
    (0.0,  22.1484,  38.4711),
    (0.0,  22.5,     42.4887),
    (0.0,  22.4219,  40.4718),
    (0.0,  22.5,    104.9887),
]

USB_BACK_ARC_CY, USB_BACK_ARC_CZ = 0.0, 42.4887
usb_back_arc_sorted = sorted(
    [(p[1], p[2]) for p in usb_back_cut_raw[1:37]],
    key=lambda p: math.atan2(p[0] - USB_BACK_ARC_CY, -(p[1] - USB_BACK_ARC_CZ))
)
usb_back_profile_yz = [(-22.5, 104.9887)] + usb_back_arc_sorted + [(22.5, 104.9887)]

usb_back_base_pts = [
    (-50.0, -212.5), (-75.0, -212.5), (-75.0,  -20.0), (-105.0,  -20.0),
    (-105.0,  20.0), (-75.0,   20.0), (-75.0,  212.5),  (-50.0,  212.5),
    (-50.0,   62.5), (  0.0,   62.5), (  0.0,  -62.5),  (-50.0,  -62.5),
]

USB_BACK_HOLE_R  = 13.5
USB_BACK_HOLE_Z  = 42.4777
USB_BACK_HOLE_Y1 = -150.0
USB_BACK_HOLE_Y2 =  150.0

with BuildPart() as usb_back_part:

    # 1. Base H-profile solid — 125 mm along +Z
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*usb_back_base_pts, close=True)
        make_face()
    extrude(amount=125)

    # 2. Slot cut
    with BuildSketch(Plane(origin=Vector(0, 0, 20.02), x_dir=Vector(0, 1, 0), z_dir=Vector(1, 0, 0))) as usb_back_cut_sk:
        with BuildLine():
            Polyline(*usb_back_profile_yz, close=True)
        make_face()
    extrude(usb_back_cut_sk.sketch, amount=150, both=True, mode=Mode.SUBTRACT)

    # 3. Circular hole cuts
    usb_back_hole_plane = Plane(origin=Vector(-50, 0, 20.02), x_dir=Vector(0, 1, 0), z_dir=Vector(1, 0, 0))
    with BuildSketch(usb_back_hole_plane) as usb_back_hole_sk:
        with Locations((USB_BACK_HOLE_Y1, USB_BACK_HOLE_Z), (USB_BACK_HOLE_Y2, USB_BACK_HOLE_Z)):
            Circle(radius=USB_BACK_HOLE_R)
    extrude(usb_back_hole_sk.sketch, amount=100, both=True, mode=Mode.SUBTRACT)

    # 4. Fillet 25mm X-axis flange edges
    usb_back_edges_25 = [
        e for e in usb_back_part.part.edges()
        if e.geom_type == GeomType.LINE
        and abs(e.start_point().Y - e.end_point().Y) < 0.01
        and abs(e.start_point().Z - e.end_point().Z) < 0.01
        and abs(e.length - 25.0) < 1.0
    ]
    fillet(usb_back_edges_25, radius=20)

    # 5. Fillet Y-axis edge at X=-105
    usb_back_edges_y105 = [
        e for e in usb_back_part.part.edges()
        if e.geom_type == GeomType.LINE
        and abs(e.start_point().X - (-105.0)) < 0.01
        and abs(e.end_point().X   - (-105.0)) < 0.01
        and abs(e.start_point().Z -  e.end_point().Z) < 0.01
        and e.length > 5.0
    ]
    fillet(usb_back_edges_y105, radius=20)

usb_back_solid = usb_back_part.part.solids()[0].moved(Location((1222.15, 1193.8, 0)))

# ══════════════════════════════════════════════════════════════════
# Show full assembly — all parts
# ══════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════
# USB FRONT VB1 — Base + chamfer cuts + holes + fillets + cut profile
# ══════════════════════════════════════════════════════════════════
import numpy as np

def usb_fit_circle(pts):
    x = np.array([p[0] for p in pts])
    y = np.array([p[1] for p in pts])
    A = np.column_stack([2*x, 2*y, np.ones(len(x))])
    b = x**2 + y**2
    res, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    cx, cy = res[0], res[1]
    r = np.sqrt(res[2] + cx**2 + cy**2)
    return cx, cy, r

usb_front_rect_points = [
    (-40.0781, -210.5469),
    ( 84.9219, -210.5469),
    ( 84.9219,  214.4531),
    (-40.0781,  214.4531),
]

usb_front_chamfer_big_pts = [
    (13.3984,-176.6406),(15.5859,-177.2461),(17.8516,-177.6953),(20.1172,-177.9492),
    (22.4219,-178.0469),(24.7266,-177.9492),(26.9922,-177.6953),(29.2578,-177.2461),
    (31.4844,-176.6406),(33.6328,-175.8594),(35.7422,-174.9219),(37.7734,-173.8281),
    (39.6875,-172.5781),(41.5234,-171.1914),(43.2422,-169.6484),(44.8438,-168.0078),
    (46.2891,-166.2305),(47.6172,-164.3555),(48.7891,-162.3633),(49.8047,-160.3125),
    (51.3672,-155.9961),(50.6641,-158.1836),(51.875,-153.75),(52.2266,-151.4844),
    (52.4219,-149.1797),(52.4219,-146.8945),(52.2266,-144.5898),(51.875,-142.3242),
    (51.3672,-140.0977),(50.6641,-137.8906),(49.8047,-135.7617),(48.7891,-133.7109),
    (47.6172,-131.7383),(46.2891,-129.8437),(44.8438,-128.0859),(43.2422,-126.4258),
    (41.5234,-124.9023),(39.6875,-123.4961),(37.7734,-122.2461),(35.7422,-121.1523),
    (33.6328,-120.2148),(31.4844,-119.4336),(29.2578,-118.8281),(26.9922,-118.3984),
    (24.7266,-118.125),(20.1172,-118.125),(22.4219,-118.0469),(17.8516,-118.3984),
    (13.3984,-119.4336),(15.5859,-118.8281),(11.2109,-120.2148),(9.1016,-121.1523),
    (5.1563,-123.4961),(7.1094,-122.2461),(3.3594,-124.9023),(1.6406,-126.4258),
    (0.0391,-128.0859),(-2.7344,-131.7383),(-1.4453,-129.8437),(-4.9609,-135.7617),
    (-3.9062,-133.7109),(-5.8203,-137.8906),(-6.4844,-140.0977),(-7.0312,-142.3242),
    (-7.5391,-146.8945),(-7.3828,-144.5898),(-7.5391,-149.1797),(-7.3828,-151.4844),
    (-7.0312,-153.75),(-6.4844,-155.9961),(-5.8203,-158.1836),(-4.9609,-160.3125),
    (-3.9062,-162.3633),(-2.7344,-164.3555),(-1.4453,-166.2305),(0.0391,-168.0078),
    (1.6406,-169.6484),(3.3594,-171.1914),(5.1563,-172.5781),(7.1094,-173.8281),
    (9.1016,-174.9219),(11.2109,-175.8594),
]

usb_front_outer_pts = [
    (12.1094,-158.9258),(13.3594,-159.9805),(14.6875,-160.8984),(16.1328,-161.6602),
    (17.6563,-162.2461),(19.2188,-162.6953),(20.8203,-162.9492),(22.4219,-163.0469),
    (24.0625,-162.9492),(25.6641,-162.6953),(27.2266,-162.2461),(28.7109,-161.6602),
    (30.1563,-160.8984),(31.5234,-159.9805),(32.7344,-158.9258),(33.8672,-157.7539),
    (34.8438,-156.4648),(35.7031,-155.0586),(36.3672,-153.5937),(36.875,-152.0508),
    (37.2266,-150.4687),(37.4219,-148.8477),(37.4219,-147.2266),(37.2266,-145.6055),
    (36.875,-144.0234),(36.3672,-142.4805),(35.7031,-141.0156),(34.8438,-139.6289),
    (33.8672,-138.3203),(32.7344,-137.1484),(31.5234,-136.0937),(30.1563,-135.1953),
    (28.7109,-134.4336),(27.2266,-133.8281),(25.6641,-133.3984),(24.0625,-133.125),
    (22.4219,-133.0469),(20.8203,-133.125),(19.2188,-133.3984),(17.6563,-133.8281),
    (16.1328,-134.4336),(14.6875,-135.1953),(13.3594,-136.0937),(12.1094,-137.1484),
    (11.0156,-138.3203),(10.0,-139.6289),(9.1797,-141.0156),(8.5156,-142.4805),
    (7.9688,-144.0234),(7.6172,-145.6055),(7.4609,-147.2266),(7.4609,-148.8477),
    (7.6172,-150.4687),(7.9688,-152.0508),(8.5156,-153.5937),(9.1797,-155.0586),
    (10.0,-156.4648),(11.0156,-157.7539),
]

usb_front_inner_pts = [
    (14.8047,-159.1797),(16.1328,-159.9805),(17.5391,-160.625),(18.9844,-161.0937),
    (20.5078,-161.4062),(22.0313,-161.543),(23.5938,-161.4844),(25.1172,-161.2695),
    (26.6016,-160.8789),(28.0469,-160.3125),(29.4141,-159.5898),(30.6641,-158.7305),
    (31.8359,-157.7148),(32.8906,-156.582),(33.7891,-155.332),(34.5313,-154.0039),
    (35.1563,-152.5781),(35.5859,-151.0937),(35.8594,-149.5703),(35.9375,-148.0469),
    (35.8594,-146.5039),(35.5859,-144.9805),(35.1563,-143.4961),(34.5313,-142.0898),
    (33.7891,-140.7422),(32.8906,-139.4922),(31.8359,-138.3594),(30.6641,-137.3437),
    (29.4141,-136.4844),(28.0469,-135.7617),(26.6016,-135.1953),(25.1172,-134.8047),
    (23.5938,-134.5898),(22.0313,-134.5508),(20.5078,-134.668),(18.9844,-134.9805),
    (17.5391,-135.4492),(16.1328,-136.0937),(14.8047,-136.8945),(13.5938,-137.832),
    (12.5,-138.9062),(11.5234,-140.0977),(10.6641,-141.4062),(10.0,-142.793),
    (9.4922,-144.2383),(9.1406,-145.7422),(8.9453,-147.2656),(8.9453,-148.8086),
    (9.1406,-150.332),(9.4922,-151.8359),(10.0,-153.3008),(10.6641,-154.668),
    (11.5234,-155.9766),(12.5,-157.168),(13.5938,-158.2422),
]

cx_big, cy_big, r_big   = usb_fit_circle(usb_front_chamfer_big_pts)
cx_out, cy_out, r_outer = usb_fit_circle(usb_front_outer_pts)
cx_in,  cy_in,  r_inner = usb_fit_circle(usb_front_inner_pts)
usb_avg_cx = (cx_big + cx_out) / 2
usb_avg_cy = (cy_big + cy_out) / 2

usb_mirror_y   = (-210.5469 + 214.4531) / 2
usb_avg_cy_mir = 2 * usb_mirror_y - usb_avg_cy
usb_cy_in_mir  = 2 * usb_mirror_y - cy_in

USB_FRONT_EXTRUDE_H = 30
USB_FRONT_CHAMFER_H = 20
USB_FRONT_Z_TOP     = 30
USB_FRONT_HOLE_H    = 50   # Z=-10 → Z=40

# Base body
with BuildPart() as usb_front_base:
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*usb_front_rect_points, close=True)
        make_face()
    extrude(amount=USB_FRONT_EXTRUDE_H)
usb_front_base_solid = usb_front_base.part

# Chamfer tool helper
def usb_make_chamfer(cx, cy):
    with BuildPart() as cp:
        with BuildSketch(Plane.XY):
            Circle(r_big)
        with BuildSketch(Plane(origin=(0, 0, -USB_FRONT_CHAMFER_H), z_dir=(0, 0, 1))):
            Circle(r_outer)
        loft()
    return cp.part.moved(Location((cx, cy, USB_FRONT_Z_TOP)))

# Hole tool helper
def usb_make_hole(cx, cy):
    with BuildPart() as hp:
        with BuildSketch(Plane(origin=(cx, cy, -10), z_dir=(0, 0, 1))):
            Circle(r_inner)
        extrude(amount=USB_FRONT_HOLE_H)
    return hp.part

usb_chamfer_orig = usb_make_chamfer(usb_avg_cx, usb_avg_cy)
usb_hole_orig    = usb_make_hole(cx_in, cy_in)
usb_chamfer_mir  = usb_make_chamfer(usb_avg_cx, usb_avg_cy_mir)
usb_hole_mir     = usb_make_hole(cx_in, usb_cy_in_mir)

usb_front_cut_body = (usb_front_base_solid
    - usb_chamfer_orig - usb_hole_orig
    - usb_chamfer_mir  - usb_hole_mir)

# Fillets
with BuildPart() as usb_front_filleted:
    add(usb_front_cut_body)
    corner_edges = (
        usb_front_filleted.edges()
        .filter_by(Axis.Z)
        .filter_by(lambda e:
            e.geom_type == GeomType.LINE and
            abs(e.length - USB_FRONT_EXTRUDE_H) < 0.1)
    )
    fillet(corner_edges, radius=20)
    def usb_on_outer_rect(e):
        if e.geom_type != GeomType.LINE: return False
        if abs(e.center().Z - USB_FRONT_Z_TOP) > 0.1: return False
        cx = e.center().X; cy = e.center().Y
        return (abs(cx - (-40.0781)) < 1.0 or abs(cx - 84.9219) < 1.0 or
                abs(cy - (-210.5469)) < 1.0 or abs(cy - 214.4531) < 1.0)
    fillet(usb_front_filleted.edges().filter_by(usb_on_outer_rect), radius=20)

# Cut profile
usb_front_cut_profile_pts = [
    (92.538,24.4531),(22.4219,24.4531),(20.4688,24.375),(18.5156,24.1211),
    (16.6016,23.6914),(14.7266,23.1055),(12.9297,22.3438),(11.1719,21.4453),
    (9.5313,20.3906),(7.9688,19.1992),(6.5234,17.8711),(5.1953,16.4258),
    (3.9844,14.8633),(2.9297,13.2031),(2.0313,11.4648),(1.2891,9.6484),
    (0.7031,7.793),(0.2734,5.8594),(0.0,3.9258),(-0.0781,1.9531),(0.0,0.0),
    (0.2734,-1.9531),(0.7031,-3.8672),(1.2891,-5.7422),(2.0313,-7.5391),
    (2.9297,-9.2969),(3.9844,-10.9375),(5.1953,-12.5),(6.5234,-13.9453),
    (7.9688,-15.2734),(9.5313,-16.4648),(12.9297,-18.4375),(11.1719,-17.5195),
    (14.7266,-19.1797),(16.6016,-19.7656),(18.5156,-20.1953),(20.4688,-20.4492),
    (22.4219,-20.5469),(92.538,-20.5469),
]

with BuildPart() as usb_front_cut_tool:
    with BuildSketch(Plane(origin=(0, 0, -10), z_dir=(0, 0, 1))):
        with BuildLine():
            Polyline(*usb_front_cut_profile_pts, close=True)
        make_face()
    extrude(amount=60)
usb_front_cut_solid = usb_front_cut_tool.part

usb_front_final = (usb_front_filleted.part - usb_front_cut_solid).moved(Location((1001, 1191.8, 0)))

# ══════════════════════════════════════════════════════════════════
# Show full assembly — all parts
# ══════════════════════════════════════════════════════════════════
show(
    result_cut,
    result_copy_moved,
    lid_result,
    wall_moved,
    handle,
    base_cut,
    extrude_solid2,
    usb_back_solid,
    usb_front_final,
    names=[
        "Blue Body (cut)",
        "Red Body (moved -X 103.28)",
        "Chamber Lid",
        "Hollow Wall",
        "Handle",
        "Base Cut",
        "Extrude Body",
        "USB Back VB1",
        "USB Front VB1",
    ],
    colors=["#5588CC", "#CC5533", "#44AA66", "#AAAAAA", "#3498DB", "#2ECC71", "#F39C12", "#E74C3C", "#9B59B6"],
)

# ══════════════════════════════════════════════════════════════════
# Export — STEP + STL to Desktop as 'Set_5'
# ══════════════════════════════════════════════════════════════════
import os
from build123d import Compound, export_step, export_stl

desktop = os.path.expanduser("~/Desktop")
step_path = os.path.join(desktop, "Set_5.step")
stl_path  = os.path.join(desktop, "Set_5.stl")

all_bodies = Compound([
    result_cut,
    result_copy_moved,
    lid_result,
    wall_moved,
    handle,
    base_cut,
    extrude_solid2,
    usb_back_solid,
    usb_front_final,
])

export_step(all_bodies, step_path)
print(f"STEP exported to: {step_path}")

export_stl(all_bodies, str(stl_path))
print(f"STL  exported to: {stl_path}")