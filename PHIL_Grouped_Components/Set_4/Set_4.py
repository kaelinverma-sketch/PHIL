"""
Assembly: Chamber + Screw as separate bodies
─────────────────────────────────────────────
Chamber : main_solid + rect_body  (as built in Chamber.py)
Screw   : body                    (as built in Screw.py, centered at origin)

Both bodies are shown together and exported as a single STEP file
via save-as dialog.

Run with:
    python Assembly.py

Requires:
    pip install build123d ocp-vscode
"""

from build123d import *
from ocp_vscode import show, set_defaults, Camera
from pathlib import Path
import math

set_defaults(reset_camera=Camera.RESET, axes=True, axes0=True, grid=(True, True, True))

# ══════════════════════════════════════════════════════════════════════════════
# CHAMBER
# ══════════════════════════════════════════════════════════════════════════════

# ── Geometry constants ────────────────────────────────────────────────────────
OUTER_COORDS = [
    (0,       0),
    (0,       500),
    (420.47,  1983.75),
    (1540.67, 1983.75),
    (1960.98, 500),
    (1960.98, 0),
]

CUT_COORDS = [
    (100,     0),
    (100,     486.11),
    (496.09,  1883.75),
    (1464.88, 1883.75),
    (1860.98, 486.11),
    (1860.98, 0),
]

EXTRUSION_HEIGHT = 391.75
CUT_HEIGHT       = 361.75

# ── Body 1: Main extruded polygon with profile cut ────────────────────────────
with BuildPart() as part:
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*OUTER_COORDS, close=True)
        make_face()
    extrude(amount=EXTRUSION_HEIGHT)

    with BuildSketch(Plane.XY.offset(30)):
        with BuildLine():
            Polyline(*CUT_COORDS, close=True)
        make_face()
    extrude(amount=CUT_HEIGHT, mode=Mode.SUBTRACT)

# ── Body 2: Separate rectangle ────────────────────────────────────────────────
with BuildPart() as rect_body:
    with BuildSketch(Plane(origin=(99, 0, 29), z_dir=(0, 0, 1))):
        Rectangle(1762, 30, align=(Align.MIN, Align.MIN))
    extrude(amount=40)

# ── Body 3: Box cut ───────────────────────────────────────────────────────────
with BuildPart() as box_body:
    with BuildSketch(Plane(origin=(542.97, 525, 0), z_dir=(0, 0, 1))):
        Rectangle(875, 1297.5, align=(Align.MIN, Align.MIN))
    extrude(amount=391.75)

# ── Body 4: Cylinder L ───────────────────────────────────────────────────────
with BuildPart() as cyl_body:
    with BuildSketch(Plane(origin=(542.97, 1173.75, 0), z_dir=(0, 0, 1))):
        Circle(120)
    extrude(amount=391.75)

# ── Body 5: Cylinder R ───────────────────────────────────────────────────────
with BuildPart() as cyl_body_mirror:
    with BuildSketch(Plane(origin=(1417.97, 1173.75, 0), z_dir=(0, 0, 1))):
        Circle(120)
    extrude(amount=391.75)

main_solid = part.part.solids()[0]
main_solid = main_solid.cut(box_body.part.solids()[0])
main_solid = main_solid.cut(cyl_body.part.solids()[0])
main_solid = main_solid.cut(cyl_body_mirror.part.solids()[0])

# ── Body 6: Outer box flange ──────────────────────────────────────────────────
with BuildPart() as outer_box:
    with BuildSketch(Plane(origin=(512.97, 495, 0), z_dir=(0, 0, 1))):
        Rectangle(935, 1357.5, align=(Align.MIN, Align.MIN))
    extrude(amount=50)

# ── Body 7: Inner box ─────────────────────────────────────────────────────────
with BuildPart() as inner_box:
    with BuildSketch(Plane(origin=(542.97, 525, 0), z_dir=(0, 0, 1))):
        Rectangle(875, 1297.5, align=(Align.MIN, Align.MIN))
    extrude(amount=50)

# ── Body 8: Hollow cylinder L ────────────────────────────────────────────────
with BuildPart() as hollow_cyl:
    with BuildSketch(Plane(origin=(542.97, 1173.75, 0), z_dir=(0, 0, 1))):
        Circle(150)
        Circle(120, mode=Mode.SUBTRACT)
    extrude(amount=50)

# ── Body 9: Hollow cylinder R ────────────────────────────────────────────────
with BuildPart() as hollow_cyl_mirror:
    with BuildSketch(Plane(origin=(1417.97, 1173.75, 0), z_dir=(0, 0, 1))):
        Circle(150)
        Circle(120, mode=Mode.SUBTRACT)
    extrude(amount=50)

# ── Body 10: Small hollow cylinder L ─────────────────────────────────────────
with BuildPart() as small_cyl_left:
    with BuildSketch(Plane(origin=(470.49, 413.75, 0), z_dir=(0, 0, 1))):
        Circle(60)
        Circle(35, mode=Mode.SUBTRACT)
    extrude(amount=50)

# ── Body 11: Small hollow cylinder R ─────────────────────────────────────────
with BuildPart() as small_cyl_right:
    with BuildSketch(Plane(origin=(1490.49, 413.75, 0), z_dir=(0, 0, 1))):
        Circle(60)
        Circle(35, mode=Mode.SUBTRACT)
    extrude(amount=50)

main_solid = main_solid.fuse(outer_box.part.solids()[0])
main_solid = main_solid.fuse(hollow_cyl.part.solids()[0])
main_solid = main_solid.fuse(hollow_cyl_mirror.part.solids()[0])
main_solid = main_solid.fuse(small_cyl_left.part.solids()[0])
main_solid = main_solid.fuse(small_cyl_right.part.solids()[0])
main_solid = main_solid.cut(inner_box.part.solids()[0])

# ── Through holes Ø240 ───────────────────────────────────────────────────────
with BuildPart() as hole_left:
    with BuildSketch(Plane(origin=(542.97, 1173.75, 0), z_dir=(0, 0, 1))):
        Circle(120)
    extrude(amount=391.75)
main_solid = main_solid.cut(hole_left.part.solids()[0])

with BuildPart() as hole_right:
    with BuildSketch(Plane(origin=(1417.97, 1173.75, 0), z_dir=(0, 0, 1))):
        Circle(120)
    extrude(amount=391.75)
main_solid = main_solid.cut(hole_right.part.solids()[0])

# ── Through holes Ø35.62 ─────────────────────────────────────────────────────
with BuildPart() as small_hole_left:
    with BuildSketch(Plane(origin=(470.49, 413.76, 0), z_dir=(0, 0, 1))):
        Circle(17.81)
    extrude(amount=391.75)

with BuildPart() as small_hole_right:
    with BuildSketch(Plane(origin=(1490.48, 413.76, 0), z_dir=(0, 0, 1))):
        Circle(17.81)
    extrude(amount=391.75)

main_solid = main_solid.cut(small_hole_left.part.solids()[0])
main_solid = main_solid.cut(small_hole_right.part.solids()[0])

# ── Chamfer cones at small holes ─────────────────────────────────────────────
with BuildPart() as chamfer_left:
    with BuildSketch(Plane(origin=(470.49, 413.76, 14.5), z_dir=(0, 0, 1))):
        Circle(17.81)
    with BuildSketch(Plane(origin=(470.49, 413.76, 32), z_dir=(0, 0, 1))):
        Circle(35)
    loft(ruled=True)

with BuildPart() as chamfer_right:
    with BuildSketch(Plane(origin=(1490.48, 413.76, 14.5), z_dir=(0, 0, 1))):
        Circle(17.81)
    with BuildSketch(Plane(origin=(1490.48, 413.76, 32), z_dir=(0, 0, 1))):
        Circle(35)
    loft(ruled=True)

main_solid = main_solid.cut(chamfer_left.part.solids()[0])
main_solid = main_solid.cut(chamfer_right.part.solids()[0])

# ── Ø70 holes depth=341.75 at holes 3 & 5 ────────────────────────────────────
for hx, hy in [(470.49, 1933.76), (1490.5, 1933.76)]:
    with BuildPart() as hole_70:
        with BuildSketch(Plane(origin=(hx, hy, 391.75), z_dir=(0, 0, 1))):
            Circle(35)
        extrude(amount=-341.75)
    main_solid = main_solid.cut(hole_70.part.solids()[0])

# ── Chamfer at holes 3 & 5 ────────────────────────────────────────────────────
for hx, hy in [(470.49, 1933.76), (1490.5, 1933.76)]:
    with BuildPart() as chamfer_top:
        with BuildSketch(Plane(origin=(hx, hy, 32.5), z_dir=(0, 0, 1))):
            Circle(35)
        with BuildSketch(Plane(origin=(hx, hy, 50), z_dir=(0, 0, 1))):
            Circle(17.81)
        loft(ruled=True)
    main_solid = main_solid.cut(chamfer_top.part.solids()[0])

if hasattr(main_solid, 'solids'):
    main_solid = main_solid.solids()[0]

# ── Pentagon cutouts ──────────────────────────────────────────────────────────
PENTA_COORDS = [
    (0,     0),
    (65.9,  0),
    (81.76, 27.5),
    (65.9,  55),
    (0,     55),
]

with BuildPart() as penta_body:
    with BuildSketch(Plane(origin=(0, 270.57, 341.7), z_dir=(0, 0, 1))):
        with BuildLine():
            lines = [Line((PENTA_COORDS[i][0], PENTA_COORDS[i][1]),
                          (PENTA_COORDS[(i+1) % len(PENTA_COORDS)][0],
                           PENTA_COORDS[(i+1) % len(PENTA_COORDS)][1]))
                     for i in range(len(PENTA_COORDS))]
        make_face()
    extrude(amount=-25)

PENTA_COORDS_MIRROR = [
    (1960.98, 0),
    (1895.08, 0),
    (1879.22, 27.5),
    (1895.08, 55),
    (1960.98, 55),
]

with BuildPart() as penta_body_mirror:
    with BuildSketch(Plane(origin=(0, 270.57, 341.7), z_dir=(0, 0, 1))):
        with BuildLine():
            lines = [Line((PENTA_COORDS_MIRROR[i][0], PENTA_COORDS_MIRROR[i][1]),
                          (PENTA_COORDS_MIRROR[(i+1) % len(PENTA_COORDS_MIRROR)][0],
                           PENTA_COORDS_MIRROR[(i+1) % len(PENTA_COORDS_MIRROR)][1]))
                     for i in range(len(PENTA_COORDS_MIRROR))]
        make_face()
    extrude(amount=-25)

# ── Side cut profiles ─────────────────────────────────────────────────────────
CUT_PROFILE_COORDS = [
    (183,    1157.44),
    (263.91, 1157.44),
    (279.8,  1184.94),
    (263.91, 1212.44),
    (198,    1212.44),
]

with BuildPart() as cut_profile_body:
    with BuildSketch(Plane(origin=(0, 0, 341.7), z_dir=(0, 0, 1))):
        with BuildLine():
            lines = [Line((CUT_PROFILE_COORDS[i][0], CUT_PROFILE_COORDS[i][1]),
                          (CUT_PROFILE_COORDS[(i+1) % len(CUT_PROFILE_COORDS)][0],
                           CUT_PROFILE_COORDS[(i+1) % len(CUT_PROFILE_COORDS)][1]))
                     for i in range(len(CUT_PROFILE_COORDS))]
        make_face()
    extrude(amount=-25)

main_solid = main_solid.cut(cut_profile_body.part.solids()[0])

CUT_PROFILE_COORDS_MIRROR = [
    (1777.98, 1157.44),
    (1697.07, 1157.44),
    (1681.18, 1184.94),
    (1697.07, 1212.44),
    (1762.98, 1212.44),
]

with BuildPart() as cut_profile_body_mirror:
    with BuildSketch(Plane(origin=(0, 0, 341.7), z_dir=(0, 0, 1))):
        with BuildLine():
            lines = [Line((CUT_PROFILE_COORDS_MIRROR[i][0], CUT_PROFILE_COORDS_MIRROR[i][1]),
                          (CUT_PROFILE_COORDS_MIRROR[(i+1) % len(CUT_PROFILE_COORDS_MIRROR)][0],
                           CUT_PROFILE_COORDS_MIRROR[(i+1) % len(CUT_PROFILE_COORDS_MIRROR)][1]))
                     for i in range(len(CUT_PROFILE_COORDS_MIRROR))]
        make_face()
    extrude(amount=-25)

main_solid = main_solid.cut(cut_profile_body_mirror.part.solids()[0])

if hasattr(main_solid, 'solids'):
    main_solid = main_solid.solids()[0]

# ── Ø70 holes at holes 3 & 5 (repeated block from original) ──────────────────
for hx, hy in [(470.49, 1933.76), (1490.5, 1933.76)]:
    with BuildPart() as hole_70:
        with BuildSketch(Plane(origin=(hx, hy, 391.75), z_dir=(0, 0, 1))):
            Circle(35)
        extrude(amount=-341.75)
    main_solid = main_solid.cut(hole_70.part.solids()[0])

for hx, hy in [(470.49, 1933.76), (1490.5, 1933.76)]:
    with BuildPart() as chamfer_top:
        with BuildSketch(Plane(origin=(hx, hy, 32.5), z_dir=(0, 0, 1))):
            Circle(35)
        with BuildSketch(Plane(origin=(hx, hy, 50), z_dir=(0, 0, 1))):
            Circle(17.81)
        loft(ruled=True)
    main_solid = main_solid.cut(chamfer_top.part.solids()[0])

if hasattr(main_solid, 'solids'):
    main_solid = main_solid.solids()[0]

# ── Top cut profile ───────────────────────────────────────────────────────────
TOP_CUT_COORDS = [
    (952.97,  1985),
    (952.97,  1917.87),
    (980.47,  1901.99),
    (1007.97, 1917.87),
    (1007.97, 1985),
]

with BuildPart() as top_cut_body:
    with BuildSketch(Plane(origin=(0, 0, 341.75), z_dir=(0, 0, 1))):
        with BuildLine():
            lines = [Line((TOP_CUT_COORDS[i][0], TOP_CUT_COORDS[i][1]),
                          (TOP_CUT_COORDS[(i+1) % len(TOP_CUT_COORDS)][0],
                           TOP_CUT_COORDS[(i+1) % len(TOP_CUT_COORDS)][1]))
                     for i in range(len(TOP_CUT_COORDS))]
        make_face()
    extrude(amount=-25)

main_solid = main_solid.cut(top_cut_body.part.solids()[0])

# ── Pentagon cuts ─────────────────────────────────────────────────────────────
main_solid = main_solid.cut(penta_body.part.solids()[0])
main_solid = main_solid.cut(penta_body_mirror.part.solids()[0])

# ── 7× Ø35 through holes ─────────────────────────────────────────────────────
HOLE_35_POSITIONS = [
    (50.1,    243.07),
    (248.04,  1184.92),
    (470.49,  1933.76),
    (980.48,  1933.76),
    (1490.5,  1933.76),
    (1712.91, 1184.92),
    (1910.96, 243.07),
]

for hx, hy in HOLE_35_POSITIONS:
    with BuildPart() as hole_35:
        with BuildSketch(Plane(origin=(hx, hy, 0), z_dir=(0, 0, 1))):
            Circle(17.5)
        extrude(amount=391.75)
    main_solid = main_solid.cut(hole_35.part.solids()[0])

# ── Ø70 holes at holes 3 & 5 (third pass) ────────────────────────────────────
for hx, hy in [(470.49, 1933.76), (1490.5, 1933.76)]:
    with BuildPart() as hole_70:
        with BuildSketch(Plane(origin=(hx, hy, 391.75), z_dir=(0, 0, 1))):
            Circle(35)
        extrude(amount=-341.75)
    main_solid = main_solid.cut(hole_70.part.solids()[0])

for hx, hy in [(470.49, 1933.76), (1490.5, 1933.76)]:
    with BuildPart() as chamfer_top:
        with BuildSketch(Plane(origin=(hx, hy, 32.5), z_dir=(0, 0, 1))):
            Circle(35)
        with BuildSketch(Plane(origin=(hx, hy, 50), z_dir=(0, 0, 1))):
            Circle(17.81)
        loft(ruled=True)
    main_solid = main_solid.cut(chamfer_top.part.solids()[0])

# ── Text emboss ───────────────────────────────────────────────────────────────
TEXT_LINES = [
    "ETH Zurich",
    "Cell Systems Dynamics Group",
    "Designed by Philip Dettinger",
]
FONT_SIZE    = 79.2
TEXT_DEPTH   = 6
LINE_SPACING = FONT_SIZE * 1.2

text_parts = []
for i, line in enumerate(TEXT_LINES):
    y_pos = (len(TEXT_LINES) - 1 - i) * LINE_SPACING + 141
    with BuildPart() as tp:
        with BuildSketch(Plane(origin=(1696.69, y_pos, 30), z_dir=(0, 0, 1), x_dir=(-1, 0, 0))):
            Text(line, font_size=FONT_SIZE, align=(Align.MIN, Align.MIN))
        extrude(amount=-TEXT_DEPTH)
    for s in tp.part.solids():
        text_parts.append(s)

for ts in text_parts:
    main_solid = main_solid.cut(ts)

# ── Side holes in Y direction ─────────────────────────────────────────────────
SIDE_HOLES = [
    (50,      230),
    (1910.96, 211.8),
]

for hx, hz in SIDE_HOLES:
    with BuildPart() as side_hole:
        with BuildSketch(Plane(origin=(hx, 0, hz), z_dir=(0, 1, 0))):
            Circle(17.5)
        extrude(amount=1983.75)
    main_solid = main_solid.cut(side_hole.part.solids()[0])

for hx, hz in SIDE_HOLES:
    with BuildPart() as side_hole_70:
        with BuildSketch(Plane(origin=(hx, 95, hz), z_dir=(0, 1, 0))):
            Circle(35)
        extrude(amount=1705)
    main_solid = main_solid.cut(side_hole_70.part.solids()[0])

for hx, hz in SIDE_HOLES:
    with BuildPart() as side_chamfer:
        with BuildSketch(Plane(origin=(hx, 77.5, hz), z_dir=(0, 1, 0))):
            Circle(17.81)
        with BuildSketch(Plane(origin=(hx, 95, hz), z_dir=(0, 1, 0))):
            Circle(35)
        loft(ruled=True)
    main_solid = main_solid.cut(side_chamfer.part.solids()[0])

# ── X-direction holes Ø60 ─────────────────────────────────────────────────────
with BuildPart() as x_hole:
    with BuildSketch(Plane(origin=(141, 1064.62, 262.49), z_dir=(1, 0, 0))):
        Circle(30)
    extrude(amount=139)
main_solid = main_solid.cut(x_hole.part.solids()[0])

with BuildPart() as x_hole_mirror:
    with BuildSketch(Plane(origin=(1680.98, 1064.62, 262.49), z_dir=(1, 0, 0))):
        Circle(30)
    extrude(amount=139)
main_solid = main_solid.cut(x_hole_mirror.part.solids()[0])

if hasattr(main_solid, 'solids'):
    main_solid = main_solid.solids()[0]

main_solid = main_solid.fuse(rect_body.part.solids()[0])
if hasattr(main_solid, 'solids'):
    main_solid = main_solid.solids()[0]

chamber_solid = main_solid

# ══════════════════════════════════════════════════════════════════════════════
# SCREW
# ══════════════════════════════════════════════════════════════════════════════

PITCH        = 120
REVS         = 5
HEIGHT       = PITCH * REVS
CREST_RADIUS = 168

h_tooth    = 24.55
flat_root  = 28.12
flat_crest = 6.95
dz_flank   = (PITCH - flat_root - flat_crest) / 2
ROOT_RADIUS  = CREST_RADIUS - h_tooth
HELIX_RADIUS = CREST_RADIUS

V4 = (  0.0000,   3.7966)
V0 = (  0.0000,  -3.1574)
V1 = ( -8.5547,  -6.9363)
V8 = (-24.5483, -14.0613)
V6 = (-24.5483,  14.0613)

with BuildSketch(Plane.XZ) as sk:
    with BuildLine():
        Polyline(
            (V4[0], V4[1]),
            (V0[0], V0[1]),
            (V1[0], V1[1]),
            (V8[0], V8[1]),
            (V6[0], V6[1]),
            close=True,
        )
    make_face()

profile_face = sk.face().moved(Location((HELIX_RADIUS, 0, 0)))
profile_face = profile_face.rotate(Axis.X, 90)

helix1 = Helix(pitch=PITCH, height=HEIGHT, radius=HELIX_RADIUS)
helix2 = Helix(pitch=PITCH, height=HEIGHT, radius=HELIX_RADIUS).rotate(Axis.Z, 120)
helix3 = Helix(pitch=PITCH, height=HEIGHT, radius=HELIX_RADIUS).rotate(Axis.Z, 240)

thread1 = sweep(sections=profile_face,                     path=helix1, is_frenet=True)
thread2 = sweep(sections=profile_face.rotate(Axis.Z, 120), path=helix2, is_frenet=True)
thread3 = sweep(sections=profile_face.rotate(Axis.Z, 240), path=helix3, is_frenet=True)

thread1 = thread1.moved(Location((0, 0, -200)))
thread2 = thread2.moved(Location((0, 0, -200)))
thread3 = thread3.moved(Location((0, 0, -200)))

cut_cyl = Cylinder(radius=300 / 2, height=1000)

thread1_cut = thread1 - cut_cyl
thread2_cut = thread2 - cut_cyl
thread3_cut = thread3 - cut_cyl

core = Cylinder(radius=300 / 2, height=343,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

core_body = core
threads   = thread1_cut + thread2_cut + thread3_cut

top_cut = Cylinder(radius=350 / 2, height=200,
                   align=(Align.CENTER, Align.CENTER, Align.MIN))
top_cut = top_cut.moved(Location((0, 0, 343)))

bot_cut = Cylinder(radius=350 / 2, height=230,
                   align=(Align.CENTER, Align.CENTER, Align.MAX))
bot_cut = bot_cut.moved(Location((0, 0, 0)))

core_body = core_body - top_cut - bot_cut

with BuildPart() as revolve_part:
    with BuildSketch(Plane.XZ) as rsk:
        with BuildLine():
            Polyline(
                (168.0051, -25.0),
                (168.0051, -62.8597),
                (129.9732, -25.0),
                close=True,
            )
        make_face()
    revolve(axis=Axis.Z, revolution_arc=360)

revolve_top = revolve_part.part.moved(Location((0, 0, 388.5)))
mirror_plane = Plane((0, 0, 171.5), (1, 0, 0), (0, 0, 1))
revolve_bot  = mirror(revolve_top, about=mirror_plane)

core_body = core_body - revolve_top - revolve_bot

# ── Loft bodies ───────────────────────────────────────────────────────────────
def sort_by_angle(pts):
    cy = sum(p[1] for p in pts) / len(pts)
    cz = sum(p[2] for p in pts) / len(pts)
    return sorted(pts, key=lambda p: math.atan2(p[2] - cz, p[1] - cy))

def make_smooth_wire(pts):
    vecs = [Vector(p) for p in sort_by_angle(pts)]
    e = Edge.make_spline(vecs, periodic=True)
    return Wire([e])

extrude2_pts = [
    (-99.6484,-0.1514,-258.4958),(-99.6484,4.5418,-258.8651),(-99.6484,9.1193,-259.9641),
    (-99.6484,13.4686,-261.7657),(-99.6484,17.4825,-264.2254),(-99.6484,21.0623,-267.2828),
    (-99.6484,24.1196,-270.8625),(-99.6484,26.5794,-274.8764),(-99.6484,28.3809,-279.2257),
    (-99.6484,29.4799,-283.8033),(-99.6484,29.8492,-288.4964),(-99.6484,29.4799,-293.1895),
    (-99.6484,28.3809,-297.7671),(-99.6484,26.5794,-302.1164),(-99.6484,24.1196,-306.1303),
    (-99.6484,21.0623,-309.71),(-99.6484,17.4825,-312.7674),(-99.6484,13.4686,-315.2271),
    (-99.6484,9.1193,-317.0287),(-99.6484,4.5418,-318.1276),(-99.6484,-0.1514,-318.497),
    (-99.6484,-4.8445,-318.1276),(-99.6484,-9.4221,-317.0287),(-99.6484,-13.7714,-315.2271),
    (-99.6484,-17.7853,-312.7674),(-99.6484,-21.365,-309.71),(-99.6484,-24.4224,-306.1303),
    (-99.6484,-26.8821,-302.1164),(-99.6484,-28.6836,-297.7671),(-99.6484,-29.7826,-293.1895),
    (-99.6484,-30.152,-288.4964),(-99.6484,-29.7826,-283.8033),(-99.6484,-28.6836,-279.2257),
    (-99.6484,-26.8821,-274.8764),(-99.6484,-24.4224,-270.8625),(-99.6484,-21.365,-267.2828),
    (-99.6484,-17.7853,-264.2254),(-99.6484,-13.7714,-261.7657),(-99.6484,-9.4221,-259.9641),
    (-99.6484,-4.8445,-258.8651),
]
extrude_pts = [
    (-174.6484,-0.1514,-238.3996),(-174.6484,6.1274,-238.7946),(-174.6484,12.3072,-239.9735),
    (-174.6484,18.2905,-241.9176),(-174.6484,23.9829,-244.5962),(-174.6484,29.2948,-247.9672),
    (-174.6484,34.1422,-251.9774),(-174.6484,38.4489,-256.5635),(-174.6484,42.1468,-261.6532),
    (-174.6484,45.1776,-267.1662),(-174.6484,47.4935,-273.0156),(-174.6484,49.0581,-279.1092),
    (-174.6484,49.8466,-291.642),(-174.6484,49.8466,-285.3508),(-174.6484,49.0581,-297.8836),
    (-174.6484,47.4935,-303.9772),(-174.6484,45.1776,-309.8266),(-174.6484,42.1468,-315.3396),
    (-174.6484,38.4489,-320.4293),(-174.6484,29.2948,-329.0256),(-174.6484,34.1422,-325.0154),
    (-174.6484,23.9829,-332.3965),(-174.6484,12.3072,-337.0193),(-174.6484,18.2905,-335.0752),
    (-174.6484,6.1274,-338.1982),(-174.6484,-0.1514,-338.5932),(-174.6484,-6.4302,-338.1982),
    (-174.6484,-12.6099,-337.0193),(-174.6484,-18.5932,-335.0752),(-174.6484,-24.2857,-332.3965),
    (-174.6484,-29.5975,-329.0256),(-174.6484,-34.445,-325.0154),(-174.6484,-38.7516,-320.4293),
    (-174.6484,-42.4495,-315.3396),(-174.6484,-45.4803,-309.8266),(-174.6484,-47.7963,-303.9772),
    (-174.6484,-49.3608,-297.8836),(-174.6484,-50.1493,-291.642),(-174.6484,-50.1493,-285.3508),
    (-174.6484,-49.3608,-279.1092),(-174.6484,-47.7963,-273.0156),(-174.6484,-45.4803,-267.1662),
    (-174.6484,-42.4495,-261.6532),(-174.6484,-38.7516,-256.5635),(-174.6484,-34.445,-251.9774),
    (-174.6484,-29.5975,-247.9672),(-174.6484,-24.2857,-244.5962),(-174.6484,-18.5932,-241.9176),
    (-174.6484,-12.6099,-239.9735),(-174.6484,-6.4302,-238.7946),
]

w1 = make_smooth_wire(extrude2_pts)
w2 = make_smooth_wire(extrude_pts)
loft_body = Solid.make_loft([w1, w2]).moved(Location((0, 0, 388.5)))

extrude2_pts_b = [
    (-99.6484,-0.1514,-258.4958),(-99.6484,4.5418,-258.8651),(-99.6484,9.1193,-259.9641),
    (-99.6484,13.4686,-261.7657),(-99.6484,17.4825,-264.2254),(-99.6484,21.0623,-267.2828),
    (-99.6484,24.1196,-270.8625),(-99.6484,26.5794,-274.8764),(-99.6484,28.3809,-279.2257),
    (-99.6484,29.4799,-283.8033),(-99.6484,29.8492,-288.4964),(-99.6484,29.4799,-293.1895),
    (-99.6484,28.3809,-297.7671),(-99.6484,26.5794,-302.1164),(-99.6484,24.1196,-306.1303),
    (-99.6484,21.0623,-309.71),(-99.6484,17.4825,-312.7674),(-99.6484,13.4686,-315.2271),
    (-99.6484,9.1193,-317.0287),(-99.6484,4.5418,-318.1276),(-99.6484,-0.1514,-318.497),
    (-99.6484,-4.8445,-318.1276),(-99.6484,-9.4221,-317.0287),(-99.6484,-13.7714,-315.2271),
    (-99.6484,-17.7853,-312.7674),(-99.6484,-21.365,-309.71),(-99.6484,-24.4224,-306.1303),
    (-99.6484,-26.8821,-302.1164),(-99.6484,-28.6836,-297.7671),(-99.6484,-29.7826,-293.1895),
    (-99.6484,-30.152,-288.4964),(-99.6484,-29.7826,-283.8033),(-99.6484,-28.6836,-279.2257),
    (-99.6484,-26.8821,-274.8764),(-99.6484,-24.4224,-270.8625),(-99.6484,-21.365,-267.2828),
    (-99.6484,-17.7853,-264.2254),(-99.6484,-13.7714,-261.7657),(-99.6484,-9.4221,-259.9641),
    (-99.6484,-4.8445,-258.8651),
]
inner_pts_b = [
    (-82.9684,-0.1514,-271.0651),(-82.9684,5.9736,-272.1766),(-82.9684,2.9611,-271.3452),
    (-82.9684,8.7891,-273.5325),(-82.9684,11.3174,-275.3694),(-82.9684,13.477,-277.6281),
    (-82.9684,15.1986,-280.2362),(-82.9684,16.4268,-283.1098),(-82.9684,17.1222,-286.1565),
    (-82.9684,17.2624,-289.2784),(-82.9684,16.8429,-292.3752),(-82.9684,15.8772,-295.3473),
    (-82.9684,14.3963,-298.0993),(-82.9684,12.4479,-300.5425),(-82.9684,10.0945,-302.5986),
    (-82.9684,7.4118,-304.2015),(-82.9684,4.486,-305.2995),(-82.9684,1.4112,-305.8575),
    (-82.9684,-1.7139,-305.8575),(-82.9684,-4.7887,-305.2995),(-82.9684,-7.7145,-304.2015),
    (-82.9684,-10.3972,-302.5986),(-82.9684,-12.7506,-300.5425),(-82.9684,-14.6991,-298.0993),
    (-82.9684,-16.18,-295.3473),(-82.9684,-17.1457,-292.3752),(-82.9684,-17.5651,-289.2784),
    (-82.9684,-17.4249,-286.1565),(-82.9684,-16.7296,-283.1098),(-82.9684,-15.5013,-280.2362),
    (-82.9684,-13.7797,-277.6281),(-82.9684,-11.6201,-275.3694),(-82.9684,-9.0919,-273.5325),
    (-82.9684,-6.2763,-272.1766),(-82.9684,-3.2639,-271.3452),
]

w1b = make_smooth_wire(extrude2_pts_b)
w2b = make_smooth_wire(inner_pts_b)
loft_body2 = Solid.make_loft([w1b, w2b]).moved(Location((0, 0, 388.5)))

extrude2_pts_c = [
    (-82.9684,-0.1514,-271.0651),(-82.9684,-3.2639,-271.3452),(-82.9684,-6.2763,-272.1766),
    (-82.9684,-9.0919,-273.5325),(-82.9684,-11.6201,-275.3694),(-82.9684,-13.7797,-277.6281),
    (-82.9684,-15.5013,-280.2362),(-82.9684,-16.7296,-283.1098),(-82.9684,-17.4249,-286.1565),
    (-82.9684,-17.5651,-289.2784),(-82.9684,-17.1457,-292.3752),(-82.9684,-16.18,-295.3473),
    (-82.9684,-14.6991,-298.0993),(-82.9684,-12.7506,-300.5425),(-82.9684,-10.3972,-302.5986),
    (-82.9684,-7.7145,-304.2015),(-82.9684,-4.7887,-305.2995),(-82.9684,-1.7139,-305.8575),
    (-82.9684,1.4112,-305.8575),(-82.9684,4.486,-305.2995),(-82.9684,7.4118,-304.2015),
    (-82.9684,10.0945,-302.5986),(-82.9684,12.4479,-300.5425),(-82.9684,14.3963,-298.0993),
    (-82.9684,15.8772,-295.3473),(-82.9684,16.8429,-292.3752),(-82.9684,17.2624,-289.2784),
    (-82.9684,17.1222,-286.1565),(-82.9684,16.4268,-283.1098),(-82.9684,15.1986,-280.2362),
    (-82.9684,13.477,-277.6281),(-82.9684,11.3174,-275.3694),(-82.9684,8.7891,-273.5325),
    (-82.9684,5.9736,-272.1766),(-82.9684,2.9611,-271.3452),
]
extrude_pts_c = [
    (-17.9684,-3.2639,-271.3452),(-17.9684,-6.2763,-272.1766),(-17.9684,-9.0919,-273.5325),
    (-17.9684,-11.6201,-275.3694),(-17.9684,-13.7797,-277.6281),(-17.9684,-15.5013,-280.2362),
    (-17.9684,-16.7296,-283.1098),(-17.9684,-17.4249,-286.1565),(-17.9684,-17.5651,-289.2784),
    (-17.9684,-17.1457,-292.3752),(-17.9684,-16.18,-295.3473),(-17.9684,-14.6991,-298.0993),
    (-17.9684,-12.7506,-300.5425),(-17.9684,-10.3972,-302.5986),(-17.9684,-7.7145,-304.2015),
    (-17.9684,-4.7887,-305.2995),(-17.9684,-1.7139,-305.8575),(-17.9684,1.4112,-305.8575),
    (-17.9684,4.486,-305.2995),(-17.9684,7.4118,-304.2015),(-17.9684,10.0945,-302.5986),
    (-17.9684,12.4479,-300.5425),(-17.9684,14.3963,-298.0993),(-17.9684,15.8772,-295.3473),
    (-17.9684,16.8429,-292.3752),(-17.9684,17.2624,-289.2784),(-17.9684,17.1222,-286.1565),
    (-17.9684,16.4268,-283.1098),(-17.9684,15.1986,-280.2362),(-17.9684,13.477,-277.6281),
    (-17.9684,11.3174,-275.3694),(-17.9684,8.7891,-273.5325),(-17.9684,5.9736,-272.1766),
    (-17.9684,2.9611,-271.3452),(-17.9684,-0.1514,-271.0651),
]

w1c = make_smooth_wire(extrude2_pts_c)
w2c = make_smooth_wire(extrude_pts_c)
loft_body3 = Solid.make_loft([w1c, w2c]).moved(Location((0, 0, 388.5)))

body = core_body + threads

top_cut2 = Cylinder(radius=400 / 2, height=600,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
top_cut2 = top_cut2.moved(Location((0, 0, 343)))
body = body - top_cut2

bot_cut2 = Cylinder(radius=400 / 2, height=600,
                    align=(Align.CENTER, Align.CENTER, Align.MAX))
bot_cut2 = bot_cut2.moved(Location((0, 0, 0)))
body = body - bot_cut2

with BuildPart() as chamfer_part:
    with BuildSketch(Plane.XZ) as csk:
        with BuildLine():
            Polyline(
                (168.0051, -25.0),
                (129.9732, -25.0),
                (168.0051, -62.8597),
                close=True,
            )
        make_face()
    revolve(axis=Axis.Z, revolution_arc=360)

chamfer_solid = chamfer_part.part.moved(Location((0, 0, 388.5)))
chamfer_mirror = mirror(chamfer_solid, about=Plane((0, 0, 171.5), (1, 0, 0), (0, 0, 1)))
body = body - chamfer_solid - chamfer_mirror

body = body - loft_body - loft_body2 - loft_body3

import math as _math

cut_pts_xy = [
    (-15.9766, 29.8828),
    (-33.3203, -0.1172),
    (-15.9766, -30.1172),
    (35.9766, -0.1172),
    (18.6328, -30.1172),
    (18.6328, 29.8828),
]
_cx = sum(p[0] for p in cut_pts_xy) / len(cut_pts_xy)
_cy = sum(p[1] for p in cut_pts_xy) / len(cut_pts_xy)
cut_pts_sorted = sorted(cut_pts_xy, key=lambda p: _math.atan2(p[1]-_cy, p[0]-_cx))

with BuildSketch(Plane.XY) as cut_sk:
    with BuildLine():
        Polyline(*cut_pts_sorted, close=True)
    make_face()

cut_solid = extrude(cut_sk.face(), amount=85).moved(Location((0, 0, 343 - 85 + 45.5)))
body = body - cut_solid

cut2_pts_xy = [
    (-19.4922,-17.168),(-17.7734,-18.9844),(-15.8984,-20.625),(-13.8281,-22.0703),
    (-11.6797,-23.3203),(-9.375,-24.375),(-7.0312,-25.1953),(-4.5703,-25.7812),
    (-2.1094,-26.1328),(0.3906,-26.25),(2.9297,-26.1133),(5.3906,-25.7617),
    (7.8125,-25.1562),(10.1953,-24.3359),(12.4609,-23.2812),(14.6484,-22.0117),
    (16.6797,-20.5469),(18.5547,-18.9062),(20.2734,-17.0703),(21.8359,-15.0977),
    (23.1641,-12.9688),(24.2969,-10.7422),(25.2344,-8.3984),(25.8984,-5.9961),
    (26.3672,-3.5352),(26.5625,-1.0352),(26.5625,1.4844),(26.2891,3.9648),
    (25.8203,6.4258),(25.0781,8.8281),(24.1016,11.1523),(22.9297,13.3594),
    (21.5625,15.4688),(20.0,17.4219),(18.2422,19.2188),(16.3281,20.8398),
    (14.2578,22.2656),(12.0703,23.4961),(9.8047,24.4922),(7.4219,25.293),
    (4.9609,25.8398),(2.5,26.1719),(-0.0391,26.25),(-2.5391,26.0938),
    (-5.0,25.7031),(-7.4219,25.0781),(-9.8047,24.2188),(-12.0703,23.1445),
    (-14.2188,21.8555),(-16.2109,20.3711),(-18.0859,18.6914),(-19.8047,16.8359),
]

with BuildSketch(Plane.XY) as cut2_sk:
    with BuildLine():
        Polyline(*cut2_pts_xy, close=True)
    make_face()

cut2_solid = extrude(cut2_sk.face(), amount=350)
body = body - cut2_solid

cut3_pts_3d = [
    (-49.6484, 33.0469, -288.5),
    (-49.6484, 16.4453, -259.75),
    (-49.6484, -16.7578, -259.75),
    (-49.6484, -33.3594, -288.5),
    (-49.6484, -33.3594, -388.5),
    (-49.6484, 33.0469, -388.5),
]

cut3_wire = Wire.make_polygon([Vector(*p) for p in cut3_pts_3d], close=True)
cut3_face = Face(cut3_wire)
cut3_solid = Solid.extrude(cut3_face, direction=Vector(25, 0, 0)).moved(Location((-25, 0, 388.5)))
body = body - cut3_solid

cut4_pts_xy = [
    (-19.8047,-16.8359),(-21.3281,-14.8047),(-22.6562,-12.6562),(-23.75,-10.3906),
    (-24.6484,-8.0078),(-25.3125,-5.5664),(-25.7031,-3.0859),(-25.8984,-0.5469),
    (-25.8203,1.9727),(-25.5078,4.4922),(-24.9609,6.9531),(-24.1797,9.3555),
    (-23.1641,11.6797),(-21.9141,13.8867),(-20.5078,15.957),(-18.8672,17.8906),
    (-17.0312,19.668),(-15.0781,21.25),(-12.9688,22.6367),(-10.7031,23.8086),
    (-8.3594,24.7656),(-5.9375,25.4883),(-3.4766,25.9766),(-0.9375,26.2305),
    (1.5625,26.2305),(4.1016,25.9961),(6.5625,25.5078),(9.0234,24.7852),
    (11.3672,23.8477),(13.5938,22.6758),(15.7031,21.2891),(17.6953,19.707),
    (19.4922,17.9492),(21.1328,16.0352),(22.5781,13.9453),(23.8281,11.7383),
    (24.8438,9.4336),(25.6641,7.0312),(26.2109,4.5508),(26.5234,2.0508),
    (26.6016,-0.4883),(26.4453,-3.0078),(26.0156,-5.5078),(25.3516,-7.9492),
    (24.4922,-10.3125),(23.3984,-12.5977),(22.0703,-14.7461),(20.5469,-16.7773),
    (18.8281,-18.6328),(16.9531,-20.332),(14.9219,-21.8359),(12.7344,-23.125),
    (10.4688,-24.2188),(8.0859,-25.0781),(5.625,-25.7031),(3.125,-26.0938),
    (0.625,-26.25),(-1.9141,-26.1523),(-4.4141,-25.8008),(-6.875,-25.2148),
    (-9.2969,-24.4141),(-11.6016,-23.3594),(-13.7891,-22.1094),(-15.8594,-20.6445),
    (-17.7734,-18.9844),(-19.8047,-17.168),(-19.4922,-17.168),
]

with BuildSketch(Plane.XY) as cut4_sk:
    with BuildLine():
        Polyline(*cut4_pts_xy, close=True)
    make_face()

cut4_solid = extrude(cut4_sk.face(), amount=20)
body = body - cut4_solid

cut5_pts_xy = [
    (-68.5547,47.2656),(-71.0156,43.3984),(-73.2422,39.4336),(-75.2734,35.332),
    (-77.1094,31.1328),(-78.6719,26.8359),(-80.0,22.4609),(-81.1328,18.0273),
    (-81.9922,13.5352),(-82.5781,9.0039),(-82.9688,4.4531),(-83.0859,-0.1172),
    (-82.9688,-4.6875),(-82.5781,-9.2383),(-81.9922,-13.7695),(-81.1328,-18.2617),
    (-80.0,-22.6953),(-78.6719,-27.0703),(-77.1094,-31.3672),(-75.2734,-35.5664),
    (-73.2422,-39.6484),(-71.0156,-43.6328),(-68.5547,-47.4805),(-65.8594,-51.1914),
    (-63.0078,-54.7656),(-59.9609,-58.1641),(-56.7188,-61.4062),(-53.3203,-64.4531),
    (-49.7656,-67.3242),(-46.0547,-69.9805),(-42.1875,-72.4414),(-38.2031,-74.707),
    (-34.1016,-76.7383),(-29.9219,-78.5352),(-25.625,-80.1172),(-21.25,-81.4453),
    (-16.8359,-82.5586),(-12.3438,-83.418),(-7.8125,-84.043),(-3.2422,-84.4141),
    (1.3281,-84.5312),(5.8984,-84.4141),(10.4688,-84.043),(15.0,-83.418),
    (19.4922,-82.5586),(23.9062,-81.4453),(28.2812,-80.1172),(32.5781,-78.5352),
    (36.7578,-76.7383),(40.8594,-74.707),(44.8438,-72.4414),(48.7109,-69.9805),
    (52.4219,-67.3242),(55.9766,-64.4531),(59.375,-61.4062),(62.6172,-58.1641),
    (65.6641,-54.7656),(68.5156,-51.1914),(71.2109,-47.4805),(73.6719,-43.6328),
    (75.8984,-39.6484),(77.9297,-35.5664),(79.7656,-31.3672),(81.3281,-27.0703),
    (82.6562,-22.6953),(83.7891,-18.2617),(84.6484,-13.7695),(85.2344,-9.2383),
    (85.625,-4.6875),(85.7422,-0.1172),(85.625,4.4531),(85.2344,9.0039),
    (84.6484,13.5352),(83.7891,18.0273),(82.6562,22.4609),(81.3281,26.8359),
    (79.7656,31.1328),(77.9297,35.332),(75.8984,39.4336),(73.6719,43.3984),
    (71.2109,47.2656),(68.5156,50.9766),(65.6641,54.5312),(62.6172,57.9297),
    (59.375,61.1719),(55.9766,64.2188),(52.4219,67.0898),(48.7109,69.7656),
    (44.8438,72.2266),(40.8594,74.4727),(36.7578,76.5039),(32.5781,78.3008),
    (28.2812,79.8828),(23.9062,81.2305),(19.4922,82.3242),(15.0,83.1836),
    (10.4688,83.8086),(5.8984,84.1797),(1.3281,84.2969),(-3.2422,84.1797),
    (-7.8125,83.8086),(-12.3438,83.1836),(-16.8359,82.3242),(-21.25,81.2305),
    (-25.625,79.8828),(-29.9219,78.3008),(-34.1016,76.5039),(-38.2031,74.4727),
    (-42.1875,72.2266),(-46.0547,69.7656),(-49.7656,67.0898),(-53.3203,64.2188),
    (-56.7188,61.1719),(-59.9609,57.9297),(-63.0078,54.5312),(-65.8594,50.9766),
]

with BuildSketch(Plane.XY) as cut5_sk:
    with BuildLine():
        Polyline(*cut5_pts_xy, close=True)
    make_face()

cut5_solid = extrude(cut5_sk.face(), amount=45.5).moved(Location((0, 0, 343)))

cut6_pts_xy = [
    (-15.9766, -30.1172),
    (18.6328, -30.1172),
    (35.9766, -0.1172),
    (18.6328, 29.8828),
    (-15.9766, 29.8828),
    (-33.3203, -0.1172),
]

with BuildSketch(Plane.XY) as cut6_sk:
    with BuildLine():
        Polyline(*cut6_pts_xy, close=True)
    make_face()

cut6_solid = extrude(cut6_sk.face(), amount=50).moved(Location((0, 0, 343)))
body = body - cut6_solid

cut5_solid = cut5_solid - cut6_solid
body = body - cut6_solid

hex_fillet_edges = [
    e for e in cut5_solid.edges()
    if abs(e.center().Z - 388.5) < 1.0
    and (e.center().X**2 + e.center().Y**2)**0.5 < 50
]
print(f"Hex fillet edges found: {len(hex_fillet_edges)}")
if len(hex_fillet_edges) == 6:
    cut5_solid = fillet(hex_fillet_edges, radius=11)

body = body + cut5_solid

blade1_pts = [
    (-103.4265,149.8189),(-87.5,122.1875),(-84.4531,124.3359),(-81.3672,126.3867),
    (-78.2031,128.3984),(-74.9609,130.3125),(-71.6797,132.1484),(-68.3203,133.9062),
    (-64.9609,135.6055),(-61.5234,137.1875),(-77.4183,164.7697),
]
blade2_pts = [
    (150.0846,15.0),(150.2734,13.3008),(150.6641,7.2852),(150.8594,1.2695),
    (150.7812,-4.7461),(150.4688,-10.7617),(150.0822,-15.0),(173.1875,-15.0),(172.9922,15.0),
]
blade3_pts = [
    (-98.5633,-141.2978),(-72.6054,-156.3534),(-61.5234,-137.1875),(-64.9609,-135.5859),
    (-68.3203,-133.9062),(-71.6797,-132.1289),(-74.9609,-130.293),(-78.2031,-128.3789),
    (-81.3672,-126.3867),(-84.4531,-124.3164),(-87.5,-122.1875),
]

blade_solids = []
for pts in [blade1_pts, blade2_pts, blade3_pts]:
    with BuildSketch(Plane.XY) as bsk:
        with BuildLine():
            Polyline(*pts, close=True)
        make_face()
    blade_solids.append(extrude(bsk.face(), amount=350))

body = body - blade_solids[0] - blade_solids[1] - blade_solids[2]

screw_solid = body.moved(Location((821.31, 1006.38, 0)))
screw_solid_copy = body.moved(Location((821.31 + 350, 1006.38, 0)))

# ══════════════════════════════════════════════════════════════════════════════
# ASSEMBLY — show as separate bodies
# ══════════════════════════════════════════════════════════════════════════════
show(chamber_solid, screw_solid, screw_solid_copy, names=["Chamber", "Screw", "Screw Copy"])

print("✓ Assembly created successfully.")
print(f"  Chamber bounding box : {chamber_solid.bounding_box()}")
print(f"  Screw bounding box   : {screw_solid.bounding_box()}")



# ── Export all three bodies to a single STEP file ─────────────────────────────
from pathlib import Path

export_path = Path(__file__).parent / "assembly.step"
export_step(Compound([chamber_solid, screw_solid, screw_solid_copy]), export_path)
print(f"✓ STEP file exported to: {export_path}")