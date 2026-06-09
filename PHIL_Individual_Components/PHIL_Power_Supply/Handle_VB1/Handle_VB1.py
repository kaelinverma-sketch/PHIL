"""
build123d script — Sweep 100x100 rectangle along path
======================================================
Profile : 100x100 mm rectangle
Path    : 454.65 in +X, 1200 in -Y, 454.65 in -X

Run with:  python sweep_profile.py
OCP CAD Viewer must be running.
"""

import os
from build123d import *
from ocp_vscode import show_object

_HERE = os.path.dirname(os.path.abspath(__file__))

# ── 1. Path ───────────────────────────────────────────────────────────────────
path_points = [
    (0.0,     0.0,    0.0),
    (454.65,  0.0,    0.0),
    (454.65, -1200.0, 0.0),
    (0.0,    -1200.0, 0.0),
]

with BuildLine() as bl:
    Polyline(*[Vector(*p) for p in path_points])
sweep_path = bl.wire()
print(f"Path: {len(sweep_path.edges())} edges | length ≈ {sweep_path.length:.1f} mm")

# ── 2. Profile face — 100x100 rectangle ──────────────────────────────────────
profile_plane = Plane(
    origin = Vector(*path_points[0]),
    x_dir  = Vector(0, 1, 0),
    z_dir  = Vector(1, 0, 0),
)

with BuildSketch(profile_plane) as sk:
    Rectangle(100, 100)

profile_face = sk.face().located(profile_plane.location)
print(f"Profile: 100×100 mm | area = {profile_face.area:.1f} mm²")

# ── 3. Sweep ──────────────────────────────────────────────────────────────────
with BuildPart() as part:
    sweep(sections=profile_face, path=sweep_path, is_frenet=True, transition=Transition.RIGHT)

solid = part.solid()
print(f"Solid: valid={solid.is_valid} | faces={len(solid.faces())} | volume ≈ {abs(solid.volume)/1e6:.2f} cm³")

# ── 4. Fillet inner Z edge — 50mm ────────────────────────────────────────────
from build123d import ShapeList
inner_z_edges = ShapeList([e for e in solid.edges()
    if abs(e.bounding_box().min.X - 404.65) < 1.0
    and abs(e.bounding_box().max.X - 404.65) < 1.0
    and (e.bounding_box().max.Z - e.bounding_box().min.Z) > 90
    and (abs(e.bounding_box().min.Y + 50) < 1.0 or abs(e.bounding_box().min.Y + 1150) < 1.0)
    and abs(e.bounding_box().max.Y - e.bounding_box().min.Y) < 1.0])

solid = solid.fillet(50, inner_z_edges)
print(f"After fillet: valid={solid.is_valid} | faces={len(solid.faces())}")

# ── Cylinder at origin ────────────────────────────────────────────────────────
with BuildPart() as cyl_part:
    with BuildSketch(Plane.XZ):
        Circle(67.5)
    extrude(amount=100)
cylinder = cyl_part.solid()
print(f"Cylinder: valid={cylinder.is_valid} | faces={len(cylinder.faces())}")

# ── 5. Fillet all X edges and Arc edges — 30mm ───────────────────────────────
def get_axis(e):
    ebb = e.bounding_box()
    dx = ebb.max.X - ebb.min.X
    dy = ebb.max.Y - ebb.min.Y
    dz = ebb.max.Z - ebb.min.Z
    if dz > max(dx, dy) * 2:   return 'Z'
    elif dy > max(dx, dz) * 2: return 'Y'
    elif dx > max(dy, dz) * 2: return 'X'
    else:                       return 'Arc'

x_and_arc = ShapeList([e for e in solid.edges() if get_axis(e) in ('X', 'Arc')])
solid = solid.fillet(30, x_and_arc)
print(f"After 30mm fillet on X+Arc edges: valid={solid.is_valid} | faces={len(solid.faces())}")

edges_1240 = ShapeList([e for e in solid.edges()
    if get_axis(e) == 'Y' and abs(e.length - 1240.0) < 1.0])
solid = solid.fillet(49.9, edges_1240)
print(f"After 49.9mm fillet on 1240mm Y edges: valid={solid.is_valid} | faces={len(solid.faces())}")

# ── Base extrude ──────────────────────────────────────────────────────────────
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
print(f"Base: valid={base_solid.is_valid} | faces={len(base_solid.faces())} | Z={base_solid.bounding_box().min.Z:.2f}..{base_solid.bounding_box().max.Z:.2f}")

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
print(f"Hole body: valid={hole_body.is_valid} | BB={hole_body.bounding_box()}")

mirror_plane = Plane(origin=Vector(0, -600, 0), x_dir=Vector(1, 0, 0), z_dir=Vector(0, 1, 0))
cylinder_mirrored = mirror(cylinder, about=mirror_plane)

hole_body_mirrored = mirror(hole_body, about=mirror_plane)

handle = solid.fuse(cylinder).fuse(cylinder_mirrored)
handle = handle.cut(hole_body).cut(hole_body_mirrored)
print(f"Handle: valid={handle.is_valid} | faces={len(handle.faces())}")

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
print(f"Extrude2: valid={extrude_solid2.is_valid} | faces={len(extrude_solid2.faces())}")

handle_copy = handle.translate(Vector(0, 0, -2.45))

base_solid = base_solid.translate(Vector(-46.209, 0, 67.494))
base_cut = base_solid.cut(handle_copy)
print(f"Base cut: valid={base_cut.is_valid} | faces={len(base_cut.faces())}")

extrude_solid2 = extrude_solid2.translate(Vector(-46.206, 0, 67.494))

show_object(handle,        name="Handle",       options={"color": (52,  152, 219), "alpha": 1.0}, clear=True)
show_object(base_cut,      name="Base_cut",     options={"color": (46,  204, 113), "alpha": 1.0})
show_object(extrude_solid2,name="Extrude_body", options={"color": (243, 156,  18), "alpha": 1.0})

# ── STEP + STL Export — pop-up file dialog ───────────────────────────────────
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)

export_path = filedialog.asksaveasfilename(
    title="Save STEP file",
    defaultextension=".step",
    filetypes=[("STEP files", "*.step *.stp"), ("All files", "*.*")],
    initialfile="model.step",
)
root.destroy()

if export_path:
    from build123d import Compound

    # ── STEP export ──────────────────────────────────────────────────────────
    export_step(Compound([handle, base_cut, extrude_solid2]), export_path)
    print(f"STEP exported to: {export_path}")

    # ── STL export — same folder, same base name ─────────────────────────────
    stl_path = os.path.splitext(export_path)[0] + ".stl"
    export_stl(Compound([handle, base_cut, extrude_solid2]), stl_path)
    print(f"STL  exported to: {stl_path}")
else:
    print("Export cancelled.")
