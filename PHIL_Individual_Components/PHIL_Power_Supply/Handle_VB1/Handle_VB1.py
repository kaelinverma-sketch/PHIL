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
# Start at origin, go +X 454.65, then -Y 1200, then -X 454.65
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
# Path starts at origin going in +X direction → profile normal = +X
# Plane: origin = path start, x_dir = +Y, z_dir = +X (normal)
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

# ── 4. Fillet inner Z edge — 50mm at x=404.65, y=-50 ────────────────────────
# Inner concave corner of the bend facing -Y direction
from build123d import ShapeList
inner_z_edges = ShapeList([e for e in solid.edges()
    if abs(e.bounding_box().min.X - 404.65) < 1.0
    and abs(e.bounding_box().max.X - 404.65) < 1.0
    and (e.bounding_box().max.Z - e.bounding_box().min.Z) > 90
    and (abs(e.bounding_box().min.Y + 50) < 1.0 or abs(e.bounding_box().min.Y + 1150) < 1.0)
    and abs(e.bounding_box().max.Y - e.bounding_box().min.Y) < 1.0])

solid = solid.fillet(50, inner_z_edges)
print(f"After fillet: valid={solid.is_valid} | faces={len(solid.faces())}")

# ── 4. Cylinder at origin, diameter=135mm, extruded 100mm in +Y ──────────────
# Sketch on XZ plane (normal=+Y), extrude in +Y direction
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

# ── Fillet 1240mm Y edges — 49.9mm (r=50 is geometrically impossible on 100mm profile) ──
edges_1240 = ShapeList([e for e in solid.edges()
    if get_axis(e) == 'Y' and abs(e.length - 1240.0) < 1.0])
solid = solid.fillet(49.9, edges_1240)
print(f"After 49.9mm fillet on 1240mm Y edges: valid={solid.is_valid} | faces={len(solid.faces())}")

# ── Base extrude from extrude.txt — 25mm in +Z ───────────────────────────────
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
# Reorder into a closed polygon: outer boundary then inner cutout edge back
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

# ── Hole through cylinder centre — diameter 29.95mm ───────────────────────────
# Cylinder centre axis at X=-45.32, Z=0, running along Y
# Drill through full Y extent (-50 to 50) plus margin
hole_plane = Plane(origin=Vector(-45.32, -60, 0), x_dir=Vector(1, 0, 0), z_dir=Vector(0, -1, 0))
with BuildPart() as hole_part:
    with BuildSketch(hole_plane):
        Circle(29.95 / 2)
    extrude(amount=120)  # longer than cylinder height to ensure full cut
hole_tool = hole_part.solid()
# Cut applied to handle after fuse (see below)



# ── Hole body — 29.95mm diameter through cylinder centre ─────────────────────
# Cylinder centre: X=-45.32, Z=0, Y=-50..50 (after translation)
with BuildPart() as hole_body_part:
    with BuildSketch(Plane(origin=Vector(-45.32, -50, 0), x_dir=Vector(1, 0, 0), z_dir=Vector(0, 1, 0))):
        Circle(29.95 / 2)
    extrude(amount=100)
hole_body = hole_body_part.solid()
print(f"Hole body: valid={hole_body.is_valid} | BB={hole_body.bounding_box()}")

# Remove old hole cut and redo using hole_body as the cut tool on handle
# (replaces the earlier cylinder.cut — handle is built after this point so we store hole_body for later)

# Mirror cylinder to the other end of the sweep (about Y=-600 midplane)
mirror_plane = Plane(origin=Vector(0, -600, 0), x_dir=Vector(1, 0, 0), z_dir=Vector(0, 1, 0))
cylinder_mirrored = mirror(cylinder, about=mirror_plane)

# ── 6. Join all bodies into one Handle, then cut hole ───────────────────────
# Mirror hole to the other cylinder end (same mirror plane as cylinder_mirrored)
hole_body_mirrored = mirror(hole_body, about=mirror_plane)

handle = solid.fuse(cylinder).fuse(cylinder_mirrored)
handle = handle.cut(hole_body).cut(hole_body_mirrored)
print(f"Handle: valid={handle.is_valid} | faces={len(handle.faces())}")

# ── New extrude from extrude.txt (second file) — 100mm in -Y ────────────────
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

# ── 7. Display ────────────────────────────────────────────────────────────────
handle_copy = handle.translate(Vector(0, 0, -2.45))

base_solid = base_solid.translate(Vector(-46.209, 0, 67.494))
base_cut = base_solid.cut(handle_copy)
print(f"Base cut: valid={base_cut.is_valid} | faces={len(base_cut.faces())}")

# ── Ask export paths BEFORE displaying (show_object blocks on macOS) ────────
import subprocess, sys
from build123d import export_step

def ask_save_path(title, default_name):
    if sys.platform == "darwin":
        script = f'''
tell application "Finder" to activate
set filePath to POSIX path of (choose file name with prompt "{title}" default name "{default_name}" default location (path to desktop))
return filePath
        '''
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        path = result.stdout.strip()
        if path and not path.endswith((".step", ".stp")):
            path += ".step"
        return path or None
    else:
        result = subprocess.run(
            ["zenity", "--file-selection", "--save",
             f"--title={title}", f"--filename={default_name}",
             "--file-filter=STEP files | *.step *.stp"],
            capture_output=True, text=True)
        return result.stdout.strip() or None

path_export = ask_save_path("Save All Bodies as STEP", "model.step")

show_object(handle,   name="Handle",   options={"color": (52,  152, 219), "alpha": 1.0}, clear=True)
show_object(base_cut,      name="Base_cut",    options={"color": (46,  204, 113), "alpha": 1.0})
extrude_solid2 = extrude_solid2.translate(Vector(-46.206, 0, 67.494))
show_object(extrude_solid2, name="Extrude_body", options={"color": (243, 156,  18), "alpha": 1.0})

# ── Export all 3 bodies in one STEP file ─────────────────────────────────────
if path_export:
    from build123d import Compound
    export_step(Compound([handle, base_cut, extrude_solid2]), path_export)
    print(f"All bodies exported to: {path_export}")
else:
    print("Export cancelled.")