"""
Build123d script:
  1. Extrude rectangular base body (extrude.txt) 164 mm along +Y
  2. Cut #1 — parallelogram, Y=-133.999, 104 mm
  3. Cut #2 — parallelogram, Y=-113.999, 64 mm
  4. Cut #3 — parallelogram, Y=-133.999, 104 mm
  5. Cut #4 — parallelogram, Y=-85.498,  7 mm

Coordinate mapping:
  - sketch_u = world_X,  sketch_v = -world_Z  (to_sketch handles this)
"""

from build123d import *
from ocp_vscode import show

def xz_plane(y: float) -> Plane:
    return Plane(origin=(0, y, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))

def to_sketch(pts_xz):
    return [(x, -z) for x, z in pts_xz]

# ---------------------------------------------------------------------------
# 1. BASE BODY — 164 mm
# ---------------------------------------------------------------------------
base_pts = [(-130.0, 0.0), (0.0, 0.0), (0.0, -118.1769), (-130.0, -118.1769)]
with BuildPart() as base_part:
    with BuildSketch(xz_plane(-163.999)):
        Polygon(to_sketch(base_pts), align=None)
    extrude(amount=164.0)

# ---------------------------------------------------------------------------
# 2. CUT #1 — Y=-133.999, 104 mm
# ---------------------------------------------------------------------------
cut1_pts = [(0.0,-48.9725), (-100.0,-31.3398), (-100.0,-62.5442), (0.0,-80.1769)]
with BuildPart() as cut1_part:
    with BuildSketch(xz_plane(-133.999)):
        Polygon(to_sketch(cut1_pts), align=None)
    extrude(amount=104.0)

# ---------------------------------------------------------------------------
# 3. CUT #2 — Y=-113.999, 64 mm
# ---------------------------------------------------------------------------
cut2_pts = [(0.0,-80.1769), (-100.0,-62.5442), (-100.0,-80.5442), (0.0,-98.1769)]
with BuildPart() as cut2_part:
    with BuildSketch(xz_plane(-113.999)):
        Polygon(to_sketch(cut2_pts), align=None)
    extrude(amount=64.0)

# ---------------------------------------------------------------------------
# 4. CUT #3 — Y=-133.999, 104 mm
# ---------------------------------------------------------------------------
cut3_pts = [(0.0,-98.1769), (-100.0,-80.5442), (-100.0,-118.1769), (0.0,-118.1769)]
with BuildPart() as cut3_part:
    with BuildSketch(xz_plane(-133.999)):
        Polygon(to_sketch(cut3_pts), align=None)
    extrude(amount=104.0)

# ---------------------------------------------------------------------------
# 5. CUT #4 — Y=-85.498, 7 mm
#    CCW order: pt0 -> pt2 -> pt3 -> pt1
# ---------------------------------------------------------------------------
cut4_pts = [
    (   0.0,     -47.1461),
    ( -76.6504,  -33.6301),
    ( -76.8066,  -40.4404),
    (   0.0,     -54.5716),
]
with BuildPart() as cut4_part:
    with BuildSketch(xz_plane(-85.498)):
        Polygon(to_sketch(cut4_pts), align=None)
    extrude(amount=7.0)

# ---------------------------------------------------------------------------
# Boolean cuts
# ---------------------------------------------------------------------------
result = (base_part.part - cut1_part.part - cut2_part.part
          - cut3_part.part - cut4_part.part)

# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------
bb = result.bounding_box()
print(f"Solids : {len(result.solids())}")
print(f"X: {bb.min.X:.4f} → {bb.max.X:.4f}  (expected -130.0 → 0.0)")
print(f"Y: {bb.min.Y:.4f} → {bb.max.Y:.4f}  (expected -163.999 → 0.001)")
print(f"Z: {bb.min.Z:.4f} → {bb.max.Z:.4f}  (expected -118.177 → 0.0)")
print(f"Volume : {result.volume:.2f} mm³")

show(result)

# ---------------------------------------------------------------------------
# STEP Export — pop-up dialog to choose save location
# ---------------------------------------------------------------------------
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()          # hide the empty root window
root.attributes('-topmost', True)  # bring dialog to front

export_path = filedialog.asksaveasfilename(
    title="Save STEP file",
    defaultextension=".step",
    filetypes=[("STEP files", "*.step *.stp"), ("All files", "*.*")],
    initialfile="model.step",
)
root.destroy()

if export_path:
    export_step(result, export_path)
    print(f"STEP exported → {export_path}")
else:
    print("Export cancelled.")