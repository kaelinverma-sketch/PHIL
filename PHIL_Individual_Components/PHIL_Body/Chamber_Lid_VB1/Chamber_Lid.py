"""
Build123d script: Two extruded bodies from polygon profiles.
Viewable with OCP CAD Viewer (pip install ocp-vscode or jupyter-cadquery).

Body 1 coordinates (x, y):
  (0, 0), (0, 500), (420.27, 1983.75), (1540.47, 1983.75), (1960.98, 500), (1960.98, 0)
  Extrude depth: 105.75 mm

Body 2 coordinates (x, y):
  (100, 0), (100, 486.11), (496.09, 1883.75), (1464.88, 1883.75), (1860.98, 486.11), (1860.98, 0)
  Extrude depth: 55.75 mm  |  Z offset: +50 mm
"""

from build123d import *
from ocp_vscode import show

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

with BuildPart() as part1:
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

with BuildPart() as part2:
    add(sk2.sketch)
    extrude(amount=55.75)

# Move body 2 by 50 mm in the Z direction
part2_moved = part2.part.moved(Location((0, 0, 50)))

# ---------------------------------------------------------------------------
# Cut body 2 from body 1
# ---------------------------------------------------------------------------
result = part1.part - part2_moved

# ---------------------------------------------------------------------------
# Body 3 — Box 965 x 1415, extruded to height 110
# ---------------------------------------------------------------------------
with BuildPart() as part3:
    Box(965, 1415, 110, align=(Align.MIN, Align.MIN, Align.MIN))

# Move the box by 497.97 in X and 466.25 in Y
box_moved = part3.part.moved(Location((497.97, 466.25, 0)))

# ---------------------------------------------------------------------------
# Cut the box from the result (body1 already cut by body2)
# ---------------------------------------------------------------------------
result = result - box_moved

# ---------------------------------------------------------------------------
# Box 2 — 1005 x 1455, extruded to height 30, then cut from result
# ---------------------------------------------------------------------------
with BuildPart() as part4:
    Box(1005, 1455, 30, align=(Align.MIN, Align.MIN, Align.MIN))

box2_moved = part4.part.moved(Location((477.97, 446.25, 0)))
result = result - box2_moved

# ---------------------------------------------------------------------------
# Holes — 70mm diameter, 30mm deep at specified XY locations
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
    result = result - hole.part

# Smaller through-holes — 35.62mm diameter at the same positions
for x, y in hole_locations:
    with BuildPart() as small_hole:
        with Locations([(x, y, 0)]):
            Cylinder(radius=35.62/2, height=1000, align=(Align.CENTER, Align.CENTER, Align.MIN))
    result = result - small_hole.part

# ---------------------------------------------------------------------------
# Chamfer cones at all hole positions, offset +30mm in Z, cut from result
# Cone frustum: big dia=70 (r=35) at bottom, small dia=35.62 (r=17.81) at top, height=20
# ---------------------------------------------------------------------------
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
    result = result - chamfer_moved

# ---------------------------------------------------------------------------
# Hollow rectangular wall — outer 1440x990, inner 1415x965 (separate body)
# ---------------------------------------------------------------------------
with BuildPart() as wall_body:
    Box(990, 1440, 27.5, align=(Align.MIN, Align.MIN, Align.MIN))
    with Locations([(12.5, 12.5, 0)]):
        Box(965, 1415, 27.5, align=(Align.MIN, Align.MIN, Align.MIN),
            mode=Mode.SUBTRACT)

# Move hollow wall by 485.47 in X and 453.75 in Y
wall_moved = wall_body.part.moved(Location((485.47, 453.75, 0)))

# ---------------------------------------------------------------------------
# Text — on the back face (Y=0 plane), extruding in -Y direction
# Text runs along X axis, lines stack along Z axis
# ---------------------------------------------------------------------------
lines = [
    "ETH Zurich",
    "Cell Systems Dynamics Group",
    "Designed by Philip Dettinger",
]

text_height = 69.28 * 1.2  # increased by 20% = 83.136
line_spacing = text_height * 1.5
extrude_depth = 6
text_parts = []

# Text is sketched in the XY plane, center aligned, extruded in +Z
for i, line in enumerate(lines):
    with BuildPart() as text_part:
        with BuildSketch(Plane(origin=(0,0,0), x_dir=(1,0,0), z_dir=(0,0,-1))) as ts:
            Text(line, font_size=text_height, align=(Align.MIN, Align.CENTER))
        extrude(amount=extrude_depth, dir=(0, 0, 1))
    # Stack lines along Y
    moved = text_part.part.moved(Location((0, -i * line_spacing, 0)))
    text_parts.append(moved)

# Combine all text lines into one body
text_body = text_parts[0]
for tp in text_parts[1:]:
    text_body = text_body.fuse(tp)

# ---------------------------------------------------------------------------
# Display all bodies in OCP CAD Viewer
# ---------------------------------------------------------------------------
# Move text by 400 in X and 343 in Y
text_body = text_body.moved(Location((400, 343, 0)))

# Cut text from result
result = result - text_body

show(result, wall_moved, names=["final_result", "hollow_wall"])

# ---------------------------------------------------------------------------
# Export to STEP — pop-up dialog to choose save location
# ---------------------------------------------------------------------------
import tkinter as tk
from tkinter import filedialog
from build123d import Compound, export_step

root = tk.Tk()
root.withdraw()  # Hide the root window
root.lift()
root.attributes("-topmost", True)

export_path = filedialog.asksaveasfilename(
    title="Export STEP file",
    defaultextension=".step",
    filetypes=[("STEP files", "*.step *.stp"), ("All files", "*.*")],
    initialfile="Chamber_Lid.step",
)

if export_path:
    all_bodies = Compound([result, wall_moved])
    export_step(all_bodies, export_path)
    print(f"Exported STEP file to: {export_path}")
else:
    print("Export cancelled.")

root.destroy()