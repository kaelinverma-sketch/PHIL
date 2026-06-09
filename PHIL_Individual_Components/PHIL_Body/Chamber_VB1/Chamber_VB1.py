"""
Build123d script: Extruded polygon body with inner profile cut + separate rectangle body
─────────────────────────────────────────────────────────────────────────────────────────
Outer profile  : (0,0), (0,500), (420.47,1983.75), (1540.67,1983.75),
                 (1960.98,500), (1960.98,0)
Extrusion height: 391.75

Cut profile    : (100,0), (100,486.11), (496.09,1883.75), (1464.88,1883.75),
                 (1860.98,486.11), (1860.98,0)
Cut depth      : 361.75, offset +30 in Z (pocket from Z=30 to Z=391.75, open top)

Rectangle body : 1760.98 x 30, extruded 40 mm — at x=100, z=30

Run with:
    python extruded_body_with_cut.py

Requires:
    pip install build123d ocp-vscode
"""

from build123d import *
from ocp_vscode import show, set_defaults, Camera

# ── Viewer defaults ──────────────────────────────────────────────────────────
set_defaults(reset_camera=Camera.RESET, axes=True, axes0=True, grid=(True, True, True))

# ── Geometry constants ───────────────────────────────────────────────────────
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

# ── Body 1: Main extruded polygon with profile cut ───────────────────────────
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

# ── Body 2: Separate rectangle — 1760.98 x 30, extruded 40 mm ───────────────
with BuildPart() as rect_body:
    with BuildSketch(Plane(origin=(99, 0, 29), z_dir=(0, 0, 1))):
        Rectangle(1762, 30, align=(Align.MIN, Align.MIN))
    extrude(amount=40)

# ── Body 3: Box 875 x 1297.5, extruded 391.75 mm, moved x=542.97, y=525 ─────
with BuildPart() as box_body:
    with BuildSketch(Plane(origin=(542.97, 525, 0), z_dir=(0, 0, 1))):
        Rectangle(875, 1297.5, align=(Align.MIN, Align.MIN))
    extrude(amount=391.75)

# ── Body 4: Cylinder — dia 240, height 391.75, at (542.97, 1173.75) ──────────
with BuildPart() as cyl_body:
    with BuildSketch(Plane(origin=(542.97, 1173.75, 0), z_dir=(0, 0, 1))):
        Circle(120)
    extrude(amount=391.75)

# ── Body 5: Mirrored cylinder — at (1417.97, 1173.75) ────────────────────────
with BuildPart() as cyl_body_mirror:
    with BuildSketch(Plane(origin=(1417.97, 1173.75, 0), z_dir=(0, 0, 1))):
        Circle(120)
    extrude(amount=391.75)

# ── Cut box and both cylinders from main body ─────────────────────────────────
main_solid = part.part.solids()[0]
main_solid = main_solid.cut(box_body.part.solids()[0])
main_solid = main_solid.cut(cyl_body.part.solids()[0])
main_solid = main_solid.cut(cyl_body_mirror.part.solids()[0])

# ── Body 6: Outer box — 935 x 1357.5, extruded 50 mm, moved x=512.97, y=495 ─
with BuildPart() as outer_box:
    with BuildSketch(Plane(origin=(512.97, 495, 0), z_dir=(0, 0, 1))):
        Rectangle(935, 1357.5, align=(Align.MIN, Align.MIN))
    extrude(amount=50)

# ── Body 7: Inner box — 875 x 1297.5, extruded 50 mm, moved x=542.97, y=525 ─
with BuildPart() as inner_box:
    with BuildSketch(Plane(origin=(542.97, 525, 0), z_dir=(0, 0, 1))):
        Rectangle(875, 1297.5, align=(Align.MIN, Align.MIN))
    extrude(amount=50)

# ── Body 8: Large hollow cylinder L ──────────────────────────────────────────
with BuildPart() as hollow_cyl:
    with BuildSketch(Plane(origin=(542.97, 1173.75, 0), z_dir=(0, 0, 1))):
        Circle(150)
        Circle(120, mode=Mode.SUBTRACT)
    extrude(amount=50)

# ── Body 9: Large hollow cylinder R ──────────────────────────────────────────
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

# ── Fuse outer box, hollow cylinders and small cylinders into main solid ──────
main_solid = main_solid.fuse(outer_box.part.solids()[0])
main_solid = main_solid.fuse(hollow_cyl.part.solids()[0])
main_solid = main_solid.fuse(hollow_cyl_mirror.part.solids()[0])
main_solid = main_solid.fuse(small_cyl_left.part.solids()[0])
main_solid = main_solid.fuse(small_cyl_right.part.solids()[0])

# ── Subtract inner box from combined solid ────────────────────────────────────
main_solid = main_solid.cut(inner_box.part.solids()[0])

# ── Through hole dia=240 at (542.97, 1173.75) ────────────────────────────────
with BuildPart() as hole_left:
    with BuildSketch(Plane(origin=(542.97, 1173.75, 0), z_dir=(0, 0, 1))):
        Circle(120)
    extrude(amount=391.75)

main_solid = main_solid.cut(hole_left.part.solids()[0])

# ── Mirrored hole dia=240 at (1417.97, 1173.75) ──────────────────────────────
with BuildPart() as hole_right:
    with BuildSketch(Plane(origin=(1417.97, 1173.75, 0), z_dir=(0, 0, 1))):
        Circle(120)
    extrude(amount=391.75)

main_solid = main_solid.cut(hole_right.part.solids()[0])

# ── Through holes dia=35.62 ───────────────────────────────────────────────────
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

# ── Chamfer cones at small hole positions ────────────────────────────────────
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

# ── Holes dia=70 at hole 3 and 5, depth=341.75 ───────────────────────────────
for hx, hy in [(470.49, 1933.76), (1490.5, 1933.76)]:
    with BuildPart() as hole_70:
        with BuildSketch(Plane(origin=(hx, hy, 391.75), z_dir=(0, 0, 1))):
            Circle(35)
        extrude(amount=-341.75)
    main_solid = main_solid.cut(hole_70.part.solids()[0])

# ── Chamfer at hole 3 and 5 ───────────────────────────────────────────────────
for hx, hy in [(470.49, 1933.76), (1490.5, 1933.76)]:
    with BuildPart() as chamfer_top:
        with BuildSketch(Plane(origin=(hx, hy, 32.5), z_dir=(0, 0, 1))):
            Circle(35)
        with BuildSketch(Plane(origin=(hx, hy, 50), z_dir=(0, 0, 1))):
            Circle(17.81)
        loft(ruled=True)
    main_solid = main_solid.cut(chamfer_top.part.solids()[0])

# ── Extract final solid safely ────────────────────────────────────────────────
if hasattr(main_solid, 'solids'):
    main_solid = main_solid.solids()[0]

# ── Pentagon profile bodies ───────────────────────────────────────────────────
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

# ── Cut profile bodies ────────────────────────────────────────────────────────
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

# ── Holes dia=70 at hole 3 and 5, depth=341.75 (second pass) ─────────────────
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

main_solid = main_solid.cut(penta_body.part.solids()[0])
main_solid = main_solid.cut(penta_body_mirror.part.solids()[0])

# ── Through holes dia=35 at 7 positions ──────────────────────────────────────
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

# ── Emboss text ───────────────────────────────────────────────────────────────
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

text_compound = Compound([])

# ── Through holes dia=35 in Y direction ──────────────────────────────────────
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

# ── Hole dia=60 in X direction ────────────────────────────────────────────────
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

combined = Compound([main_solid])

show(combined, names=["Combined Body"])

print("✓ Parts created successfully.")
print(f"  Bounding box : {combined.bounding_box()}")
print(f"  Volume       : {combined.volume:.4f} mm³")

# ── STEP + STL Export — pop-up dialog ────────────────────────────────────────
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()
root.lift()
root.attributes('-topmost', True)

export_path = filedialog.asksaveasfilename(
    title="Export STEP file",
    defaultextension=".step",
    filetypes=[("STEP files", "*.step *.stp"), ("All files", "*.*")],
    initialfile="chamber.step",
)
root.destroy()

if export_path:
    # ── STEP export ──────────────────────────────────────────────────────────
    export_step(combined, export_path)
    print(f"✓ STEP exported to: {export_path}")

    # ── STL export — same folder, same base name ─────────────────────────────
    stl_path = os.path.splitext(export_path)[0] + ".stl"
    export_stl(combined, stl_path)
    print(f"✓ STL  exported to: {stl_path}")
else:
    print("⚠ Export cancelled — no file saved.")
