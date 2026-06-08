"""
Slot Body - build123d
─────────────────────────────────────────────────────
56 points defining a closed slot profile (two semicircles + straight walls).
Fix: right semicircle reversed so winding is correct (no self-intersection).
Also fixed swap at idx 17↔18 in left semicircle.
Normalised to centroid, extruded Z=0 → Z=50 mm.
Viewed interactively with ocp_vscode.
"""

from build123d import *
from ocp_vscode import show, set_defaults

# ── left semicircle: top-left → bottom-left ──────────────────────────────────
_left = [
    (539834.9609, 234253.9648),(539829.1406, 234253.6328),(539823.3984, 234252.6172),
    (539817.8516, 234250.957), (539812.5,    234248.6523), (539807.4609, 234245.7422),
    (539802.8125, 234242.2656),(539798.5938, 234238.2812),(539794.8438, 234233.8281),
    (539791.6406, 234228.9648),(539789.0234, 234223.7695),(539787.0312, 234218.3203),
    (539785.7031, 234212.6562),(539785.0391, 234206.875), (539785.0391, 234201.0742),
    (539785.7031, 234195.293), (539787.0312, 234189.6289),
    (539789.0234, 234184.1602),(539791.6406, 234178.9648),  # ← fixed swap
    (539794.8438, 234174.1211),(539798.5938, 234169.668),
    (539802.8125, 234165.6641),(539807.4609, 234162.207), (539812.5,    234159.2969),
    (539817.8516, 234156.9922),(539823.3984, 234155.3125),(539829.1406, 234154.3164),
    (539834.9609, 234153.9648),
]

# ── right semicircle: top-right → bottom-right (reversed → bottom-right → top-right) ──
_right_orig = [
    (541284.9609, 234253.9648),
    (541290.7422, 234253.6328),(541296.4844, 234252.6172),
    (541302.0312, 234250.957), (541307.3828, 234248.6523),(541312.4219, 234245.7422),
    (541317.0703, 234242.2656),(541321.3281, 234238.2812),(541325.0391, 234233.8281),
    (541328.2422, 234228.9648),(541330.8594, 234223.7695),(541332.8516, 234218.3203),
    (541334.1797, 234212.6562),(541334.8438, 234206.875), (541334.8438, 234201.0742),
    (541334.1797, 234195.293), (541332.8516, 234189.6289),(541330.8594, 234184.1602),
    (541328.2422, 234178.9648),(541325.0391, 234174.1211),(541321.3281, 234169.668),
    (541317.0703, 234165.6641),(541312.4219, 234162.207), (541307.3828, 234159.2969),
    (541302.0312, 234156.9922),(541296.4844, 234155.3125),(541290.7422, 234154.3164),
    (541284.9609, 234153.9648),
]

# Reverse right semicircle → goes bottom-right UP to top-right
# Polyline close=True adds: top-right→top-left (top wall) and bottom-left→bottom-right (bottom wall)
raw_points = _left + list(reversed(_right_orig))

# ── normalise: shift centroid to origin ───────────────────────────────────────
xs = [p[0] for p in raw_points]
ys = [p[1] for p in raw_points]
ox = (min(xs) + max(xs)) / 2
oy = (min(ys) + max(ys)) / 2

print(f"Shared origin : ({ox:.3f}, {oy:.3f})")
print(f"Extents       : {max(xs)-min(xs):.1f} × {max(ys)-min(ys):.1f} mm")

pts_2d = [(x - ox, y - oy) for x, y in raw_points]

# ── build solid ───────────────────────────────────────────────────────────────
with BuildPart() as body:
    with BuildSketch(Plane(origin=(0, 0, 0), z_dir=(0, 0, 1))):
        with BuildLine():
            Polyline(*pts_2d, close=True)
        make_face()
    extrude(amount=50.0, both=False)        # Z=0 → Z=50 mm

solid = body.part
print(f"Volume        : {solid.volume:,.1f} mm³")

# ── display ───────────────────────────────────────────────────────────────────
set_defaults(axes=True, axes0=True, grid=(True, True, True), transparent=False)
show(solid, names=["Slot (Z=0→50)"], colors=["#4A90D9"])

# ══════════════════════════════════════════════════════════════════════════════
# BODY 2 – HOLE  (XZ-plane profile, extruded 120 mm in +Y direction)
# All 24 pts share Y=234153.9648 — profile lies in the XZ plane.
# Sketch placed on a plane at that Y, facing +Y, so extrude goes into the model.
# Profile is a ~15×15 mm circular shape centred at X≈541084.96, Z≈25.
# ══════════════════════════════════════════════════════════════════════════════

_hole_raw = [
    (541088.7109, 18.5048),(541090.2344, 19.6967),(541091.4453, 21.25),
    (541092.1875, 23.0589),(541092.4609, 25.0),   (541092.1875, 26.9412),
    (541091.4453, 28.75),  (541090.2344, 30.3033),(541088.7109, 31.4952),
    (541086.875,  32.2445),(541084.9609, 32.5),   (541083.0078, 32.2445),
    (541081.2109, 31.4952),(541079.6484, 30.3033),(541078.4375, 28.75),
    (541077.6953, 26.9412),(541077.4609, 25.0),   (541077.6953, 23.0589),
    (541078.4375, 21.25),  (541079.6484, 19.6967),(541081.2109, 18.5048),
    (541083.0078, 17.7556),(541084.9609, 17.5),   (541086.875,  17.7556),
]

# Normalise: sketch X = -(x - ox), sketch Y = z (world Z maps correctly to +Z)
_hole_pts = [(-(x - ox), z) for x, z in _hole_raw]

# Plane at Y=234153.9648, facing +Y, with x_dir=(-1,0,0) so sketch Y = world +Z
_hole_y = 234153.9648 - oy

with BuildPart() as hole_body:
    with BuildSketch(Plane(
        origin=(0, _hole_y, 0),
        z_dir=(0, 1, 0),     # sketch normal = +Y → extrude in +Y
        x_dir=(-1, 0, 0),    # sketch X = world -X; sketch Y = world +Z
    )):
        with BuildLine():
            Polyline(*_hole_pts, close=True)
        make_face()
    extrude(amount=120.0, both=False)   # 120 mm in +Y direction

hole_solid = hole_body.part

# Replicate 9 more copies spaced 35 mm apart in -X direction
# Total: 10 cylinders, each 35 mm apart
_all_holes = hole_solid
for i in range(1, 10):
    _copy = hole_solid.moved(Location((-i * 50, 0, 0)))
    _all_holes = _all_holes.fuse(_copy)

print(f"All holes volume: {_all_holes.volume:,.1f} mm³")

# ══════════════════════════════════════════════════════════════════════════════
# BODY 3 – EXTRUDE  (XZ-plane profile, extruded 120 mm in +Y direction)
# Same structure as hole body — Y=234153.9648 constant, profile in XZ plane.
# Centred at X≈540034.96, Z≈25.
# ══════════════════════════════════════════════════════════════════════════════

_extrude2_raw = [
    (540031.2109, 31.4952),(540029.6484, 30.3033),(540028.4375, 28.75),
    (540027.6953, 26.9412),(540027.4609, 25.0),   (540027.6953, 23.0589),
    (540028.4375, 21.25),  (540029.6484, 19.6967),(540031.2109, 18.5048),
    (540033.0078, 17.7556),(540034.9609, 17.5),   (540036.875,  17.7556),
    (540038.7109, 18.5048),(540040.2344, 19.6967),(540041.4453, 21.25),
    (540042.1875, 23.0589),(540042.4609, 25.0),   (540042.1875, 26.9412),
    (540041.4453, 28.75),  (540040.2344, 30.3033),(540038.7109, 31.4952),
    (540036.875,  32.2445),(540034.9609, 32.5),   (540033.0078, 32.2445),
]

_extrude2_pts = [(-(x - ox), z) for x, z in _extrude2_raw]

with BuildPart() as extrude2_body:
    with BuildSketch(Plane(
        origin=(0, _hole_y, 0),
        z_dir=(0, 1, 0),
        x_dir=(-1, 0, 0),
    )):
        with BuildLine():
            Polyline(*_extrude2_pts, close=True)
        make_face()
    extrude(amount=120.0, both=False)   # 120 mm in +Y direction

extrude2_solid = extrude2_body.part

# Replicate 9 more copies spaced 50 mm apart in +X direction (center-to-center)
_all_extrude2 = extrude2_solid
for i in range(1, 10):
    _copy2 = extrude2_solid.moved(Location((i * 50, 0, 0)))
    _all_extrude2 = _all_extrude2.fuse(_copy2)

print(f"All extrude2 volume : {_all_extrude2.volume:,.1f} mm³")

# Cut both red and green cylinders from blue slot body
solid = solid.cut(_all_holes)
print(f"After red cuts  : {solid.volume:,.1f} mm³")
solid = solid.cut(_all_extrude2)
print(f"After green cuts: {solid.volume:,.1f} mm³")

# ══════════════════════════════════════════════════════════════════════════════
# TEXT – 'TOP                                RIGHT' on bottom face (Z=0)
# Font size 65, extruded +5mm in +Z direction (engraved into bottom face)
# Shifted -167mm in X, mirrored about XZ plane for bottom readability
# ══════════════════════════════════════════════════════════════════════════════

with BuildPart() as text2_part:
    with BuildSketch(Plane(origin=(-285, 0, 0), z_dir=(0, 0, 1))):
        Text("TOP                          RIGHT", font_size=65, align=(Align.CENTER, Align.CENTER))
    extrude(amount=5.0, both=False)         # Z=0 → Z=5 mm (+Z into body)

# Mirror about XZ plane so text reads correctly from below
text2_solid = mirror(text2_part.part, about=Plane(origin=(-285, 0, 0), z_dir=(0, 1, 0)))

# Cut into bottom face in +Z direction
solid = solid.cut(text2_solid)
print(f"After top text  : {solid.volume:,.1f} mm³")

set_defaults(axes=True, axes0=True, grid=(True, True, True), transparent=False)
show(
    solid,
    names=["Slot (all cuts + text)"],
    colors=["#4A90D9"],
)

# ══════════════════════════════════════════════════════════════════════════════
# CHAMFER BODY – loft outer(Z=0, larger) → inner(Z=13.5, smaller)
# Both profiles angle-sorted and resampled to 50 pts for clean ruled loft.
# Separate body shown in orange.
# ══════════════════════════════════════════════════════════════════════════════

import math as _mc2

def _sort_a(pts):
    cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
    return sorted(pts, key=lambda p: _mc2.atan2(p[1]-cy, p[0]-cx))

def _resamp(pts, n):
    pts=list(pts)+[pts[0]]; dists=[0]
    for i in range(1,len(pts)):
        dx=pts[i][0]-pts[i-1][0]; dy=pts[i][1]-pts[i-1][1]
        dists.append(dists[-1]+_mc2.sqrt(dx*dx+dy*dy))
    total=dists[-1]; result=[]
    for j in range(n):
        t=j/n*total
        for i in range(1,len(dists)):
            if dists[i]>=t:
                s=(t-dists[i-1])/(dists[i]-dists[i-1])
                result.append((pts[i-1][0]+s*(pts[i][0]-pts[i-1][0]),
                                pts[i-1][1]+s*(pts[i][1]-pts[i-1][1])))
                break
    return result

_ch_outer_raw = [
    (539808.9453,234180.5469),(539805.9375,234184.3945),(539803.4766,234188.6328),
    (539801.6406,234193.1641),(539799.9609,234202.7539),(539800.4688,234197.8906),
    (539800.1172,234207.6367),(539800.9766,234212.4414),(539802.5,234217.0898),
    (539804.6484,234221.4648),(539807.3828,234225.5273),(539810.625,234229.1406),
    (539814.375,234232.2852),(539818.5156,234234.8828),(539822.9688,234236.8555),
    (539827.6562,234238.2031),(539832.5,234238.8867),(539837.3828,234238.8867),
    (539842.2266,234238.2031),(539846.9141,234236.8555),(539851.3672,234234.8828),
    (539855.5078,234232.2852),(539859.2578,234229.1406),(539862.5391,234225.5273),
    (539865.2734,234221.4648),(539867.3828,234217.0898),(539868.9062,234212.4414),
    (539869.7656,234207.6367),(539869.9219,234202.7539),(539869.4141,234197.8906),
    (539868.2422,234193.1641),(539866.4062,234188.6328),(539863.9453,234184.3945),
    (539860.9375,234180.5469),(539857.4609,234177.168),(539853.4766,234174.2969),
    (539849.1797,234171.9922),(539844.6094,234170.332),(539839.8047,234169.3164),
    (539834.9609,234168.9648),(539830.0781,234169.3164),(539820.7031,234171.9922),
    (539825.3125,234170.332),(539816.4062,234174.2969),(539812.4609,234177.168),
]

_ch_inner_raw = [
    (539853.8672,234214.1602),(539855.3906,234210.625),(539856.25,234206.8555),
    (539856.4062,234203.0078),(539855.8984,234199.1797),(539854.7266,234195.5273),
    (539852.8906,234192.1289),(539850.4688,234189.1211),(539847.5781,234186.582),
    (539844.2578,234184.6094),(539840.6641,234183.2422),(539833.0078,234182.5586),
    (539836.875,234182.5586),(539829.2188,234183.2422),(539825.625,234184.6094),
    (539822.3047,234186.582),(539819.4141,234189.1211),(539816.9922,234192.1289),
    (539815.1562,234195.5273),(539813.9844,234199.1797),(539813.4766,234203.0078),
    (539813.6328,234206.8555),(539814.4922,234210.625),(539816.0156,234214.1602),
    (539818.125,234217.3828),(539820.7812,234220.1562),(539823.9062,234222.4219),
    (539827.3828,234224.1016),(539831.0938,234225.1172),(539834.9609,234225.4688),
    (539838.7891,234225.1172),(539842.5,234224.1016),(539845.9766,234222.4219),
    (539849.1016,234220.1562),(539851.7578,234217.3828),
]

_N = 50
_ch_o = [(x - ox, y - oy) for x,y in _resamp(_sort_a(_ch_outer_raw), _N)]
_ch_i = [(x - ox, y - oy) for x,y in _resamp(_sort_a(_ch_inner_raw), _N)]

with BuildPart() as chamfer_part:
    with BuildSketch(Plane(origin=(0, 0, 0), z_dir=(0, 0, 1))):    # outer at Z=0
        with BuildLine():
            Polyline(*_ch_o, close=True)
        make_face()
    with BuildSketch(Plane(origin=(0, 0, 13.5), z_dir=(0, 0, 1))): # inner at Z=13.5
        with BuildLine():
            Polyline(*_ch_i, close=True)
        make_face()
    loft(ruled=True)                                                 # linear taper

chamfer_solid = chamfer_part.part
print(f"Chamfer volume  : {chamfer_solid.volume:,.1f} mm³")

# ══════════════════════════════════════════════════════════════════════════════
# CHAMFER 2 – loft outer(Z=0, larger) → inner(Z=13.5, smaller), separate body
# ══════════════════════════════════════════════════════════════════════════════

_ch2_outer_raw = [
    (541258.9453,234227.3828),(541262.4609,234230.7812),(541266.4062,234233.6523),
    (541270.7031,234235.9375),(541275.3125,234237.6172),(541280.0781,234238.6328),
    (541284.9609,234238.9648),(541289.8047,234238.6328),(541294.6094,234237.6172),
    (541299.1797,234235.9375),(541303.4766,234233.6523),(541307.4609,234230.7812),
    (541310.9375,234227.3828),(541255.9375,234223.5352),(541253.4766,234219.3164),
    (541250.4688,234210.0586),(541251.6406,234214.7852),(541249.9609,234205.1953),
    (541250.1172,234200.3125),(541250.9766,234195.5078),(541252.5,234190.8594),
    (541254.6484,234186.4648),(541257.3828,234182.4219),(541260.625,234178.7891),
    (541264.375,234175.6641),(541313.9453,234223.5352),(541316.4062,234219.3164),
    (541318.2422,234214.7852),(541319.9219,234205.1953),(541319.4141,234210.0586),
    (541319.7656,234200.3125),(541318.9062,234195.5078),(541317.3828,234190.8594),
    (541312.5391,234182.4219),(541315.2734,234186.4648),(541309.2578,234178.7891),
    (541305.5078,234175.6641),(541301.3672,234173.0664),(541296.9141,234171.0742),
    (541287.3828,234169.0625),(541292.2266,234169.7461),(541282.5,234169.0625),
    (541277.6562,234169.7461),(541272.9688,234171.0742),(541268.5156,234173.0664),
]

_ch2_inner_raw = [
    (541283.0078,234225.3906),(541286.875,234225.3906),(541290.6641,234224.707),
    (541294.2578,234223.3398),(541297.5781,234221.3672),(541300.4688,234218.8281),
    (541302.8906,234215.8203),(541304.7266,234212.4219),(541279.2188,234224.707),
    (541272.3047,234221.3672),(541275.625,234223.3398),(541269.4141,234218.8281),
    (541266.9922,234215.8203),(541265.1562,234212.4219),(541263.9844,234208.75),
    (541263.4766,234204.9414),(541263.6328,234201.0938),(541264.4922,234197.3242),
    (541266.0156,234193.7891),(541268.125,234190.5664),(541270.7812,234187.7734),
    (541273.9062,234185.5078),(541277.3828,234183.8477),(541281.0938,234182.8125),
    (541284.9609,234182.4805),(541288.7891,234182.8125),(541292.5,234183.8477),
    (541295.9766,234185.5078),(541299.1016,234187.7734),(541301.7578,234190.5664),
    (541303.8672,234193.7891),(541305.3906,234197.3242),(541306.25,234201.0938),
    (541306.4062,234204.9414),(541305.8984,234208.75),
]

_ch2_o = [(x - ox, y - oy) for x,y in _resamp(_sort_a(_ch2_outer_raw), _N)]
_ch2_i = [(x - ox, y - oy) for x,y in _resamp(_sort_a(_ch2_inner_raw), _N)]

with BuildPart() as chamfer2_part:
    with BuildSketch(Plane(origin=(0, 0, 0), z_dir=(0, 0, 1))):
        with BuildLine():
            Polyline(*_ch2_o, close=True)
        make_face()
    with BuildSketch(Plane(origin=(0, 0, 13.5), z_dir=(0, 0, 1))):
        with BuildLine():
            Polyline(*_ch2_i, close=True)
        make_face()
    loft(ruled=True)

chamfer2_solid = chamfer2_part.part
print(f"Chamfer 2 volume: {chamfer2_solid.volume:,.1f} mm³")

# Cut both chamfers from blue slot body in same +Z direction
solid = solid.cut(chamfer_solid)
print(f"After chamfer 1 cut : {solid.volume:,.1f} mm³")
solid = solid.cut(chamfer2_solid)
print(f"After chamfer 2 cut : {solid.volume:,.1f} mm³")

# ══════════════════════════════════════════════════════════════════════════════
# TEXT – 'TOP                                RIGHT' on bottom face (Z=0)
# Font size 65, extruded +5mm in +Z direction (engraved into bottom face)
# Shifted -167mm in X, mirrored about XZ plane for bottom readability
# ══════════════════════════════════════════════════════════════════════════════

with BuildPart() as text2_part:
    with BuildSketch(Plane(origin=(-285, 0, 0), z_dir=(0, 0, 1))):
        Text("TOP                          RIGHT", font_size=65, align=(Align.CENTER, Align.CENTER))
    extrude(amount=5.0, both=False)         # Z=0 → Z=5 mm (+Z into body)

# Mirror about XZ plane so text reads correctly from below
text2_solid = mirror(text2_part.part, about=Plane(origin=(-285, 0, 0), z_dir=(0, 1, 0)))

# Cut into bottom face in +Z direction
solid = solid.cut(text2_solid)
print(f"After top text  : {solid.volume:,.1f} mm³")

set_defaults(axes=True, axes0=True, grid=(True, True, True), transparent=False)
show(
    solid,
    names=["Slot (all cuts + text)"],
    colors=["#4A90D9"],
)

# ══════════════════════════════════════════════════════════════════════════════
# HOLE CYLINDER – XY plane profile at Z=50, angle-sorted, separate body
# ══════════════════════════════════════════════════════════════════════════════

_hole2_raw = [
    (539832.3047,234245.2344),(539827.0312,234244.5508),(539821.9141,234243.2227),
    (539816.9922,234241.2305),(539812.3828,234238.6328),(539808.125,234235.4492),
    (539804.3359,234231.7773),(539801.0156,234227.6367),(539837.5781,234245.2344),
    (539842.8516,234244.5508),(539847.9688,234243.2227),(539852.8906,234241.2305),
    (539857.5,234238.6328),(539861.7578,234235.4492),(539865.5469,234231.7773),
    (539868.8672,234227.6367),(539871.6016,234223.1055),(539873.75,234218.2617),
    (539875.2734,234213.1641),(539798.2812,234223.1055),(539796.1328,234218.2617),
    (539794.6484,234213.1641),(539795.3125,234192.207),(539794.1406,234197.3633),
    (539793.6328,234202.6562),(539793.7891,234207.9492),(539797.1484,234187.2266),
    (539799.5703,234182.5391),(539802.6172,234178.1836),(539806.1719,234174.2773),
    (539810.1953,234170.8398),(539814.6484,234167.9492),(539819.4141,234165.6445),
    (539829.6484,234162.9688),(539824.4531,234163.9648),(539834.9609,234162.6172),
    (539840.2344,234162.9688),(539845.4297,234163.9648),(539850.4688,234165.6445),
    (539855.2344,234167.9492),(539859.6875,234170.8398),(539863.7109,234174.2773),
    (539867.2656,234178.1836),(539870.3125,234182.5391),(539872.7734,234187.2266),
    (539874.5703,234192.207),(539875.7812,234197.3633),(539876.2891,234202.6562),
    (539876.0938,234207.9492),
]

_hole2_pts = _sort_a([(x - ox, y - oy) for x,y in _hole2_raw])

with BuildPart() as hole2_part:
    with BuildSketch(Plane(origin=(0, 0, 50), z_dir=(0, 0, 1))):
        with BuildLine():
            Polyline(*_hole2_pts, close=True)
        make_face()
    extrude(amount=-35.0, both=False)       # Z=50 → Z=15 mm (-Z direction)

hole2_solid = hole2_part.part
print(f"Hole2 volume    : {hole2_solid.volume:,.1f} mm³")

# ══════════════════════════════════════════════════════════════════════════════
# EXTRUDE CYLINDER 2 – XY plane profile at Z=50, extruded 35mm in -Z direction
# ══════════════════════════════════════════════════════════════════════════════

_extrude_cyl2_raw = [
    (541297.9688,234164.7266),(541302.8906,234166.7188),(541307.5,234169.3164),
    (541311.7578,234172.4805),(541315.5469,234176.1719),(541318.8672,234180.3125),
    (541321.6016,234184.8438),(541323.75,234189.6875),(541325.2734,234194.7656),
    (541326.0938,234200.0),(541326.2891,234205.293),(541325.7812,234210.5664),
    (541324.5703,234215.7422),(541322.7734,234220.7031),(541320.3125,234225.4102),
    (541317.2656,234229.7461),(541313.7109,234233.6719),(541309.6875,234237.1094),
    (541305.2344,234240.0),(541300.4688,234242.3047),(541295.4297,234243.9648),
    (541290.2344,234244.9805),(541284.9609,234245.3125),(541279.6484,234244.9805),
    (541274.4531,234243.9648),(541269.4141,234242.3047),(541264.6484,234240.0),
    (541260.1953,234237.1094),(541256.1719,234233.6719),(541252.6172,234229.7461),
    (541249.5703,234225.4102),(541247.1484,234220.7031),(541292.8516,234163.3789),
    (541287.5781,234162.7148),(541282.3047,234162.7148),(541277.0312,234163.3789),
    (541271.9141,234164.7266),(541266.9922,234166.7188),(541262.3828,234169.3164),
    (541258.125,234172.4805),(541254.3359,234176.1719),(541251.0156,234180.3125),
    (541248.2812,234184.8438),(541246.1328,234189.6875),(541244.6484,234194.7656),
    (541243.7891,234200.0),(541243.6328,234205.293),(541244.1406,234210.5664),
    (541245.3125,234215.7422),
]

_extrude_cyl2_pts = _sort_a([(x - ox, y - oy) for x,y in _extrude_cyl2_raw])

with BuildPart() as extrude_cyl2_part:
    with BuildSketch(Plane(origin=(0, 0, 50), z_dir=(0, 0, 1))):
        with BuildLine():
            Polyline(*_extrude_cyl2_pts, close=True)
        make_face()
    extrude(amount=-35.0, both=False)       # Z=50 → Z=15 mm (-Z direction)

extrude_cyl2_solid = extrude_cyl2_part.part

# Cut red and green from blue in same -Z direction
solid = solid.cut(hole2_solid)
print(f"After red cut   : {solid.volume:,.1f} mm³")
solid = solid.cut(extrude_cyl2_solid)
print(f"After green cut : {solid.volume:,.1f} mm³")

# ══════════════════════════════════════════════════════════════════════════════
# TEXT – 'TOP                                RIGHT' on bottom face (Z=0)
# Font size 65, extruded +5mm in +Z direction (engraved into bottom face)
# Shifted -167mm in X, mirrored about XZ plane for bottom readability
# ══════════════════════════════════════════════════════════════════════════════

with BuildPart() as text2_part:
    with BuildSketch(Plane(origin=(-285, 0, 0), z_dir=(0, 0, 1))):
        Text("TOP                          RIGHT", font_size=65, align=(Align.CENTER, Align.CENTER))
    extrude(amount=5.0, both=False)         # Z=0 → Z=5 mm (+Z into body)

# Mirror about XZ plane so text reads correctly from below
text2_solid = mirror(text2_part.part, about=Plane(origin=(-285, 0, 0), z_dir=(0, 1, 0)))

# Cut into bottom face in +Z direction
solid = solid.cut(text2_solid)
print(f"After top text  : {solid.volume:,.1f} mm³")

set_defaults(axes=True, axes0=True, grid=(True, True, True), transparent=False)
show(
    solid,
    names=["Slot (all cuts + text)"],
    colors=["#4A90D9"],
)

# ══════════════════════════════════════════════════════════════════════════════
# TEXT – 'BOTTOM' on top face (Z=50), font size 50, separate body
# Extruded 2mm upward (+Z) as raised lettering
# ══════════════════════════════════════════════════════════════════════════════

with BuildPart() as text_part:
    with BuildSketch(Plane(origin=(-167, 0, 50), z_dir=(0, 0, 1))):
        Text("BOTTOM", font_size=65, align=(Align.CENTER, Align.CENTER))
    extrude(amount=-5.0, both=False)        # Z=50 → Z=45 mm (-Z direction)

text_solid = text_part.part

# Cut BOTTOM text into top face in -Z direction, 5mm deep (Z=50→45)
solid = solid.cut(text_solid)
print(f"After text cut  : {solid.volume:,.1f} mm³")

# ══════════════════════════════════════════════════════════════════════════════
# TEXT – 'TOP                                RIGHT' on bottom face (Z=0)
# Font size 65, extruded +5mm in +Z direction (engraved into bottom face)
# Shifted -167mm in X, mirrored about XZ plane for bottom readability
# ══════════════════════════════════════════════════════════════════════════════

with BuildPart() as text2_part:
    with BuildSketch(Plane(origin=(-285, 0, 0), z_dir=(0, 0, 1))):
        Text("TOP                          RIGHT", font_size=65, align=(Align.CENTER, Align.CENTER))
    extrude(amount=5.0, both=False)         # Z=0 → Z=5 mm (+Z into body)

# Mirror about XZ plane so text reads correctly from below
text2_solid = mirror(text2_part.part, about=Plane(origin=(-285, 0, 0), z_dir=(0, 1, 0)))

# Cut into bottom face in +Z direction
solid = solid.cut(text2_solid)
print(f"After top text  : {solid.volume:,.1f} mm³")

set_defaults(axes=True, axes0=True, grid=(True, True, True), transparent=False)
show(
    solid,
    names=["Slot (all cuts + text)"],
    colors=["#4A90D9"],
)

# ══════════════════════════════════════════════════════════════════════════════
# EXPORT — STEP file with pop-up file dialog for save location
# ══════════════════════════════════════════════════════════════════════════════

import tkinter as tk
from tkinter import filedialog

_root = tk.Tk()
_root.withdraw()
_root.attributes("-topmost", True)

_export_path = filedialog.asksaveasfilename(
    title="Export model as STEP",
    defaultextension=".step",
    filetypes=[("STEP files", "*.step *.stp"), ("All files", "*.*")],
    initialfile="slot_body.step",
)
_root.destroy()

if _export_path:
    export_step(solid, _export_path)
    print(f"Model exported to: {_export_path}")
else:
    print("Export cancelled.")