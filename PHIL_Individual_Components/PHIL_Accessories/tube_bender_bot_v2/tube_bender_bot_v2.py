"""
Build123d script: Five independent extruded bodies + one fused body in OCP CAD Viewer.

Body 1 — XY plane, rectangle,         extruded  18 mm along +Z
Body 2 — XZ plane, trapezoid,         extruded 100 mm along +Y
Body 3 — XZ plane, trapezoid,         extruded  60 mm along +Y
Body 4 — XZ plane, trapezoid,         extruded 100 mm along +Y
Body 5 — XZ plane, curved 21-pt poly, extruded   7 mm along +Y  (separate)
"""

from build123d import *
from ocp_vscode import show

# ─────────────────────────────────────────────────────────────────────────────
# BODY 1 — XY plane, rectangle, 18 mm along +Z
# ─────────────────────────────────────────────────────────────────────────────
points1 = [
    (-95.0342, -85.5005, -95.1652),
    (-95.0342,  78.4985, -95.1652),
    ( 34.9658,  78.4985, -95.1652),
    ( 34.9658, -85.5005, -95.1652),
]
xy_pts = [(p[0], p[1]) for p in points1]

with BuildSketch(Plane.XY.offset(-95.1652)) as sk1:
    with BuildLine():
        Polyline(*xy_pts, close=True)
    make_face()

body1 = extrude(sk1.sketch, amount=18)

# ─────────────────────────────────────────────────────────────────────────────
# BODY 2 — XZ plane, trapezoid, 100 mm along +Y
# ─────────────────────────────────────────────────────────────────────────────
points2 = [
    (-65.0342, -53.501, -77.1652),
    (-65.0342, -53.501, -38.5325),
    ( 34.9658, -53.501, -77.1652),
    ( 34.9658, -53.501, -56.1652),
]
ordered2 = [points2[0], points2[1], points2[3], points2[2]]
xz_pts2  = [(p[0], p[2]) for p in ordered2]

with BuildSketch(Plane.XZ.offset(-53.501)) as sk2:
    with BuildLine():
        Polyline(*xz_pts2, close=True)
    make_face()

body2 = extrude(sk2.sketch, amount=100)

# ─────────────────────────────────────────────────────────────────────────────
# BODY 3 — XZ plane, trapezoid, 60 mm along +Y
# ─────────────────────────────────────────────────────────────────────────────
points3 = [
    ( 34.9658, -33.501, -56.1652),
    ( 34.9658, -33.501, -36.1652),
    (-65.0342, -33.501, -18.5325),
    (-65.0342, -33.501, -38.5325),
]
ordered3 = [points3[3], points3[2], points3[1], points3[0]]
xz_pts3  = [(p[0], p[2]) for p in ordered3]

with BuildSketch(Plane.XZ.offset(-33.501)) as sk3:
    with BuildLine():
        Polyline(*xz_pts3, close=True)
    make_face()

body3 = extrude(sk3.sketch, amount=60)

# ─────────────────────────────────────────────────────────────────────────────
# BODY 4 — XZ plane, trapezoid, 100 mm along +Y
# ─────────────────────────────────────────────────────────────────────────────
points4 = [
    (-65.0342, -53.501,  11.4675),
    (-65.0342, -53.501, -18.5325),
    ( 34.9658, -53.501,  -6.1652),
    ( 34.9658, -53.501, -36.1652),
]
ordered4 = [points4[1], points4[0], points4[2], points4[3]]
xz_pts4  = [(p[0], p[2]) for p in ordered4]

with BuildSketch(Plane.XZ.offset(-53.501)) as sk4:
    with BuildLine():
        Polyline(*xz_pts4, close=True)
    make_face()

body4 = extrude(sk4.sketch, amount=100)

# ─────────────────────────────────────────────────────────────────────────────
# FUSED BODY — Boolean union of bodies 1–4
# ─────────────────────────────────────────────────────────────────────────────
fused = body1 + body2 + body3 + body4

# ─────────────────────────────────────────────────────────────────────────────
# BODY 5 — XZ plane, curved 21-pt polygon, 7 mm along +Y  (separate body)
# Y constant = -6.9995
# ─────────────────────────────────────────────────────────────────────────────
points5 = [
    ( 34.9658, -6.9995, -11.684 ),
    ( 34.9658, -6.9995,  -2.0   ),
    (-34.9658, -6.9995,  10.0   ),
    (-34.9658, -6.9995, -10.0715),
    (-34.8047, -6.9995,  -9.1285),
    (-34.5557, -6.9995,  -8.205 ),
    (-34.2236, -6.9995,  -7.3093),
    (-33.8037, -6.9995,  -6.4498),
    (-33.3008, -6.9995,  -5.6343),
    (-32.7295, -6.9995,  -4.8702),
    (-32.0801, -6.9995,  -4.1646),
    (-31.3721, -6.9995,  -3.5238),
    (-30.6055, -6.9995,  -2.9537),
    (-29.7852, -6.9995,  -2.4596),
    (-28.9258, -6.9995,  -2.046 ),
    (-28.0273, -6.9995,  -1.7166),
    (-27.0996, -6.9995,  -1.4745),
    (-26.1572, -6.9995,  -1.3218),
    (-25.2002, -6.9995,  -1.2601),
    (-24.248,  -6.9995,  -1.2897),
    (-23.2959, -6.9995,  -1.4106),
]
xz_pts5 = [(p[0], p[2]) for p in points5]

with BuildSketch(Plane.XZ.offset(-6.9995)) as sk5:
    with BuildLine():
        Polyline(*xz_pts5, close=True)
    make_face()

# Extrude-cut: subtract the sketch profile from the fused body along +Y (7 mm)
cut_tool = extrude(sk5.sketch, amount=7)
result    = fused - cut_tool

# ─────────────────────────────────────────────────────────────────────────────
# Show result
# ─────────────────────────────────────────────────────────────────────────────
show(result,
     names=["Fused_with_cut"],
     colors=["#4A90D9"])

# ─────────────────────────────────────────────────────────────────────────────
# Console summary
# ─────────────────────────────────────────────────────────────────────────────
print("✅  Extrude-cut applied successfully.")
print(f"\n  Result body (fused 1–4 minus cut)")
print(f"    Bounding box : {result.bounding_box()}")
print(f"    Volume       : {result.volume:.2f} mm³")

# ─────────────────────────────────────────────────────────────────────────────
# BODY 6 — XY plane, curved 46-pt profile, 80 mm along +Z  (separate body)
# Z constant = -58.2052
# ─────────────────────────────────────────────────────────────────────────────
points6 = [
    (-37.5146, -8.396,   -58.2052),
    (-36.8604, -8.2129,  -58.2052),
    (-36.2354, -7.9395,  -58.2052),
    (-35.6494, -7.5854,  -58.2052),
    (-35.1221, -7.1558,  -58.2052),
    (-34.6533, -6.6553,  -58.2052),
    (-34.2627, -6.0986,  -58.2052),
    (-33.9502, -5.4932,  -58.2052),
    (-33.7207, -4.8486,  -58.2052),
    (-33.5791, -4.1821,  -58.2052),
    (-33.5352, -3.501,   -58.2052),
    (-33.5791, -2.8198,  -58.2052),
    (-33.7207, -2.1509,  -58.2052),
    (-33.9502, -1.5088,  -58.2052),
    (-34.2627, -0.9033,  -58.2052),
    (-35.1221,  0.1538,  -58.2052),
    (-34.6533, -0.3442,  -58.2052),
    (-35.6494,  0.5835,  -58.2052),
    (-36.2354,  0.9399,  -58.2052),
    (-36.8604,  1.2109,  -58.2052),
    (-37.5146,  1.394,   -58.2052),
    (-38.1934,  1.4868,  -58.2052),
    (-38.877,   1.4868,  -58.2052),
    (-39.5508,  1.394,   -58.2052),
    (-40.21,    1.2109,  -58.2052),
    (-40.835,   0.9399,  -58.2052),
    (-41.416,   0.5835,  -58.2052),
    (-41.9482,  0.1538,  -58.2052),
    (-42.4121, -0.3442,  -58.2052),
    (-42.8076, -0.9033,  -58.2052),
    (-43.1201, -1.5088,  -58.2052),
    (-43.3496, -2.1509,  -58.2052),
    (-43.4863, -2.8198,  -58.2052),
    (-43.5352, -3.501,   -58.2052),
    (-43.4863, -4.1821,  -58.2052),
    (-43.3496, -4.8486,  -58.2052),
    (-43.1201, -5.4932,  -58.2052),
    (-42.8076, -6.0986,  -58.2052),
    (-42.4121, -6.6553,  -58.2052),
    (-41.9482, -7.1558,  -58.2052),
    (-41.416,  -7.5854,  -58.2052),
    (-40.835,  -7.9395,  -58.2052),
    (-40.21,   -8.2129,  -58.2052),
    (-39.5508, -8.396,   -58.2052),
    (-38.877,  -8.4888,  -58.2052),
    (-38.1934, -8.4888,  -58.2052),
]
# Shift to origin then offset: +3.5 mm in X, +38.5 mm in Y — Z unchanged
cx6, cy6 = -38.5352, -3.501
xy_pts6 = [(p[0] - cx6 - 38.5, p[1] - cy6 + 3.5) for p in points6]

with BuildSketch(Plane.XY.offset(-58.2052)) as sk6:
    with BuildLine():
        Polyline(*xy_pts6, close=True)
    make_face()

# Extrude-cut: subtract cylinder from result along +Z (80 mm)
cut6   = extrude(sk6.sketch, amount=80)
result = result - cut6

# ─────────────────────────────────────────────────────────────────────────────
# Show result + body6 separately
# ─────────────────────────────────────────────────────────────────────────────
show(result,
     names=["Final_result"],
     colors=["#4A90D9"])

print(f"\n  Final result (with cylinder cut → 80 mm along Z)")
print(f"    Bounding box : {result.bounding_box()}")
print(f"    Volume       : {result.volume:.2f} mm³")

# ─────────────────────────────────────────────────────────────────────────────
# Export to STEP + STL — pop-up file dialog to choose save location
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()                         # hide the empty root window
root.attributes('-topmost', True)       # dialog appears on top

export_path = filedialog.asksaveasfilename(
    title="Save STEP file",
    defaultextension=".step",
    filetypes=[("STEP files", "*.step *.stp"), ("All files", "*.*")],
    initialfile="model.step",
)

if export_path:
    # ── STEP export ──────────────────────────────────────────────────────────
    export_step(result, export_path)
    print(f"\n✅  STEP file saved to: {export_path}")

    # ── STL export — same folder, same base name ─────────────────────────────
    base      = os.path.splitext(export_path)[0]
    stl_path  = base + ".stl"
    export_stl(result, stl_path)
    print(f"✅  STL  file saved to: {stl_path}")
else:
    print("\n⚠️  Export cancelled — no file saved.")
