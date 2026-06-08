"""
Build123d script: Base body with chamfer cut + through-hole,
mirrored on the opposite side in Y, shown in OCP CAD Viewer.
  - Rectangular extrude 30mm
  - Chamfer cut (big@Z=30 → small@Z=10) at original position
  - Chamfer cut mirrored in Y about rect centre
  - Cylindrical hole (Z=-10 → Z=40) at original position
  - Cylindrical hole mirrored in Y about rect centre
Requires: pip install build123d ocp-vscode numpy
"""

import numpy as np
from build123d import *
from ocp_vscode import show

# ── Helper: fit circle to 2D point cloud ─────────────────────────────────────
def fit_circle(pts):
    x = np.array([p[0] for p in pts])
    y = np.array([p[1] for p in pts])
    A = np.column_stack([2*x, 2*y, np.ones(len(x))])
    b = x**2 + y**2
    res, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    cx, cy = res[0], res[1]
    r = np.sqrt(res[2] + cx**2 + cy**2)
    return cx, cy, r

# ── Point data ────────────────────────────────────────────────────────────────
rect_points = [
    (-40.0781, -210.5469),
    ( 84.9219, -210.5469),
    ( 84.9219,  214.4531),
    (-40.0781,  214.4531),
]

chamfer_big_pts = [
    (13.3984, -176.6406), (15.5859, -177.2461), (17.8516, -177.6953),
    (20.1172, -177.9492), (22.4219, -178.0469), (24.7266, -177.9492),
    (26.9922, -177.6953), (29.2578, -177.2461), (31.4844, -176.6406),
    (33.6328, -175.8594), (35.7422, -174.9219), (37.7734, -173.8281),
    (39.6875, -172.5781), (41.5234, -171.1914), (43.2422, -169.6484),
    (44.8438, -168.0078), (46.2891, -166.2305), (47.6172, -164.3555),
    (48.7891, -162.3633), (49.8047, -160.3125), (51.3672, -155.9961),
    (50.6641, -158.1836), (51.875,  -153.75),   (52.2266, -151.4844),
    (52.4219, -149.1797), (52.4219, -146.8945), (52.2266, -144.5898),
    (51.875,  -142.3242), (51.3672, -140.0977), (50.6641, -137.8906),
    (49.8047, -135.7617), (48.7891, -133.7109), (47.6172, -131.7383),
    (46.2891, -129.8437), (44.8438, -128.0859), (43.2422, -126.4258),
    (41.5234, -124.9023), (39.6875, -123.4961), (37.7734, -122.2461),
    (35.7422, -121.1523), (33.6328, -120.2148), (31.4844, -119.4336),
    (29.2578, -118.8281), (26.9922, -118.3984), (24.7266, -118.125),
    (20.1172, -118.125),  (22.4219, -118.0469), (17.8516, -118.3984),
    (13.3984, -119.4336), (15.5859, -118.8281), (11.2109, -120.2148),
    (9.1016,  -121.1523), (5.1563,  -123.4961), (7.1094,  -122.2461),
    (3.3594,  -124.9023), (1.6406,  -126.4258), (0.0391,  -128.0859),
    (-2.7344, -131.7383), (-1.4453, -129.8437), (-4.9609, -135.7617),
    (-3.9062, -133.7109), (-5.8203, -137.8906), (-6.4844, -140.0977),
    (-7.0312, -142.3242), (-7.5391, -146.8945), (-7.3828, -144.5898),
    (-7.5391, -149.1797), (-7.3828, -151.4844), (-7.0312, -153.75),
    (-6.4844, -155.9961), (-5.8203, -158.1836), (-4.9609, -160.3125),
    (-3.9062, -162.3633), (-2.7344, -164.3555), (-1.4453, -166.2305),
    (0.0391,  -168.0078), (1.6406,  -169.6484), (3.3594,  -171.1914),
    (5.1563,  -172.5781), (7.1094,  -173.8281), (9.1016,  -174.9219),
    (11.2109, -175.8594),
]

outer_pts = [
    (12.1094, -158.9258), (13.3594, -159.9805), (14.6875, -160.8984),
    (16.1328, -161.6602), (17.6563, -162.2461), (19.2188, -162.6953),
    (20.8203, -162.9492), (22.4219, -163.0469), (24.0625, -162.9492),
    (25.6641, -162.6953), (27.2266, -162.2461), (28.7109, -161.6602),
    (30.1563, -160.8984), (31.5234, -159.9805), (32.7344, -158.9258),
    (33.8672, -157.7539), (34.8438, -156.4648), (35.7031, -155.0586),
    (36.3672, -153.5937), (36.875,  -152.0508), (37.2266, -150.4687),
    (37.4219, -148.8477), (37.4219, -147.2266), (37.2266, -145.6055),
    (36.875,  -144.0234), (36.3672, -142.4805), (35.7031, -141.0156),
    (34.8438, -139.6289), (33.8672, -138.3203), (32.7344, -137.1484),
    (31.5234, -136.0937), (30.1563, -135.1953), (28.7109, -134.4336),
    (27.2266, -133.8281), (25.6641, -133.3984), (24.0625, -133.125),
    (22.4219, -133.0469), (20.8203, -133.125),  (19.2188, -133.3984),
    (17.6563, -133.8281), (16.1328, -134.4336), (14.6875, -135.1953),
    (13.3594, -136.0937), (12.1094, -137.1484), (11.0156, -138.3203),
    (10.0,    -139.6289), (9.1797,  -141.0156), (8.5156,  -142.4805),
    (7.9688,  -144.0234), (7.6172,  -145.6055), (7.4609,  -147.2266),
    (7.4609,  -148.8477), (7.6172,  -150.4687), (7.9688,  -152.0508),
    (8.5156,  -153.5937), (9.1797,  -155.0586), (10.0,    -156.4648),
    (11.0156, -157.7539),
]

inner_pts = [
    (14.8047, -159.1797), (16.1328, -159.9805), (17.5391, -160.625),
    (18.9844, -161.0937), (20.5078, -161.4062), (22.0313, -161.543),
    (23.5938, -161.4844), (25.1172, -161.2695), (26.6016, -160.8789),
    (28.0469, -160.3125), (29.4141, -159.5898), (30.6641, -158.7305),
    (31.8359, -157.7148), (32.8906, -156.582),  (33.7891, -155.332),
    (34.5313, -154.0039), (35.1563, -152.5781), (35.5859, -151.0937),
    (35.8594, -149.5703), (35.9375, -148.0469), (35.8594, -146.5039),
    (35.5859, -144.9805), (35.1563, -143.4961), (34.5313, -142.0898),
    (33.7891, -140.7422), (32.8906, -139.4922), (31.8359, -138.3594),
    (30.6641, -137.3437), (29.4141, -136.4844), (28.0469, -135.7617),
    (26.6016, -135.1953), (25.1172, -134.8047), (23.5938, -134.5898),
    (22.0313, -134.5508), (20.5078, -134.668),  (18.9844, -134.9805),
    (17.5391, -135.4492), (16.1328, -136.0937), (14.8047, -136.8945),
    (13.5938, -137.832),  (12.5,    -138.9062), (11.5234, -140.0977),
    (10.6641, -141.4062), (10.0,    -142.793),  (9.4922,  -144.2383),
    (9.1406,  -145.7422), (8.9453,  -147.2656), (8.9453,  -148.8086),
    (9.1406,  -150.332),  (9.4922,  -151.8359), (10.0,    -153.3008),
    (10.6641, -154.668),  (11.5234, -155.9766), (12.5,    -157.168),
    (13.5938, -158.2422),
]

# ── Fit circles ───────────────────────────────────────────────────────────────
cx_big, cy_big, r_big   = fit_circle(chamfer_big_pts)
cx_out, cy_out, r_outer = fit_circle(outer_pts)
cx_in,  cy_in,  r_inner = fit_circle(inner_pts)
avg_cx = (cx_big + cx_out) / 2
avg_cy = (cy_big + cy_out) / 2

# Y midpoint of the rectangular face — mirror axis
rect_y_min = -210.5469
rect_y_max =  214.4531
mirror_y   = (rect_y_min + rect_y_max) / 2   # ≈ 1.953

# Mirrored Y centres (reflect about mirror_y)
avg_cy_mir = 2 * mirror_y - avg_cy
cy_in_mir  = 2 * mirror_y - cy_in

print(f"Chamfer Big → centre ({cx_big:.3f}, {cy_big:.3f}), radius {r_big:.3f} mm")
print(f"Outer       → centre ({cx_out:.3f}, {cy_out:.3f}), radius {r_outer:.3f} mm")
print(f"Inner       → centre ({cx_in:.3f},  {cy_in:.3f}),  radius {r_inner:.3f} mm")
print(f"Mirror Y axis: {mirror_y:.3f}")
print(f"Chamfer mirrored centre Y: {avg_cy_mir:.3f}")
print(f"Hole mirrored centre Y:    {cy_in_mir:.3f}")

EXTRUDE_HEIGHT = 30
CHAMFER_HEIGHT = 20
Z_TOP          = EXTRUDE_HEIGHT  # 30

HOLE_Z_START = -10
HOLE_Z_END   =  40
HOLE_HEIGHT  = HOLE_Z_END - HOLE_Z_START  # 50 mm

# ── 1. BASE BODY ──────────────────────────────────────────────────────────────
with BuildPart() as base_part:
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*rect_points, close=True)
        make_face()
    extrude(amount=EXTRUDE_HEIGHT)

base_solid = base_part.part

# ── Helper: build chamfer loft tool at a given (cx, cy) ──────────────────────
def make_chamfer_tool(cx, cy):
    with BuildPart() as cp:
        with BuildSketch(Plane.XY):
            Circle(r_big)
        with BuildSketch(Plane(origin=(0, 0, -CHAMFER_HEIGHT), z_dir=(0, 0, 1))):
            Circle(r_outer)
        loft()
    return cp.part.moved(Location((cx, cy, Z_TOP)))

# ── Helper: build cylindrical hole tool at a given (cx, cy) ──────────────────
def make_hole_tool(cx, cy):
    with BuildPart() as hp:
        with BuildSketch(Plane(origin=(cx, cy, HOLE_Z_START), z_dir=(0, 0, 1))):
            Circle(r_inner)
        extrude(amount=HOLE_HEIGHT)
    return hp.part

# ── 2. Original chamfer + hole ────────────────────────────────────────────────
chamfer_tool_orig = make_chamfer_tool(avg_cx, avg_cy)
hole_tool_orig    = make_hole_tool(cx_in, cy_in)

# ── 3. Mirrored chamfer + hole (reflected in Y about rect centre) ─────────────
chamfer_tool_mir  = make_chamfer_tool(avg_cx, avg_cy_mir)
hole_tool_mir     = make_hole_tool(cx_in, cy_in_mir)

# ── 4. CUT PROFILE (Cut.txt) — extrude cut Z=-10 → Z=50 ─────────────────────
cut_profile_pts = [
    (92.538,  24.4531), (22.4219, 24.4531), (20.4688, 24.375),
    (18.5156, 24.1211), (16.6016, 23.6914), (14.7266, 23.1055),
    (12.9297, 22.3438), (11.1719, 21.4453), (9.5313,  20.3906),
    (7.9688,  19.1992), (6.5234,  17.8711), (5.1953,  16.4258),
    (3.9844,  14.8633), (2.9297,  13.2031), (2.0313,  11.4648),
    (1.2891,   9.6484), (0.7031,   7.793),  (0.2734,   5.8594),
    (0.0,      3.9258), (-0.0781,  1.9531), (0.0,      0.0),
    (0.2734,  -1.9531), (0.7031,  -3.8672), (1.2891,  -5.7422),
    (2.0313,  -7.5391), (2.9297,  -9.2969), (3.9844, -10.9375),
    (5.1953, -12.5),    (6.5234, -13.9453), (7.9688, -15.2734),
    (9.5313, -16.4648), (12.9297,-18.4375), (11.1719,-17.5195),
    (14.7266,-19.1797), (16.6016,-19.7656), (18.5156,-20.1953),
    (20.4688,-20.4492), (22.4219,-20.5469), (92.538, -20.5469),
]

CUT_Z_START = -10
CUT_Z_END   =  50
CUT_HEIGHT  = CUT_Z_END - CUT_Z_START  # 60 mm

cut_plane = Plane(origin=(0, 0, CUT_Z_START), z_dir=(0, 0, 1))

with BuildPart() as cut_tool_part:
    with BuildSketch(cut_plane):
        with BuildLine():
            Polyline(*cut_profile_pts, close=True)
        make_face()
    extrude(amount=CUT_HEIGHT)

cut_tool = cut_tool_part.part

# ── 5. Apply chamfer + hole cuts (before fillets) ────────────────────────────
cut_body = (base_solid
            - chamfer_tool_orig
            - hole_tool_orig
            - chamfer_tool_mir
            - hole_tool_mir)

# ── 6. Fillet the 4 vertical corner edges (along Z axis) ─────────────────────
FILLET_R = 20  # mm

# Rebuild in BuildPart context so we can use fillet()
with BuildPart() as filleted_part:
    add(cut_body)
    # Select the 4 vertical edges at the rect corners (parallel to Z axis)
    corner_edges = (
        filleted_part.edges()
        .filter_by(Axis.Z)          # keep only edges parallel to Z
        .filter_by(lambda e:        # keep only the 4 straight corner edges
            e.geom_type == GeomType.LINE and
            abs(e.length - EXTRUDE_HEIGHT) < 0.1
        )
    )
    fillet(corner_edges, radius=FILLET_R)

    # Fillet only the outer rectangular perimeter edges at Z=30
    # Exclude: circular arcs (chamfer), cut profile edges (not on outer rect boundary)
    rect_x_min, rect_x_max = -40.0781, 84.9219
    rect_y_min2, rect_y_max2 = -210.5469, 214.4531
    tol = 1.0  # mm tolerance for boundary check

    def on_outer_rect(e):
        if e.geom_type != GeomType.LINE:
            return False
        if abs(e.center().Z - EXTRUDE_HEIGHT) > 0.1:
            return False
        cx = e.center().X
        cy = e.center().Y
        # Must lie on one of the 4 outer rect sides
        on_left   = abs(cx - rect_x_min) < tol
        on_right  = abs(cx - rect_x_max) < tol
        on_bottom = abs(cy - rect_y_min2) < tol
        on_top    = abs(cy - rect_y_max2) < tol
        return on_left or on_right or on_bottom or on_top

    top_face_edges = filleted_part.edges().filter_by(on_outer_rect)
    fillet(top_face_edges, radius=FILLET_R)

# ── 7. Apply cut profile AFTER fillets ───────────────────────────────────────
final_body = filleted_part.part - cut_tool

# ── 8. Display ────────────────────────────────────────────────────────────────
show(
    final_body,
    colors=["#4A90D9"],
    alphas=[1.0],
    names=["Base — chamfer + hole × 2 + corner fillets 20mm"],
)

print(f"\nOriginal  chamfer @ ({avg_cx:.2f}, {avg_cy:.2f})")
print(f"Mirrored  chamfer @ ({avg_cx:.2f}, {avg_cy_mir:.2f})")
print(f"Original  hole    @ ({cx_in:.2f},  {cy_in:.2f})")
print(f"Mirrored  hole    @ ({cx_in:.2f},  {cy_in_mir:.2f})")
print(f"Corner fillets: r={FILLET_R} mm on 4 vertical edges")

# ── 9. Export to STEP on Desktop ──────────────────────────────────────────────
import os
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
step_path = os.path.join(desktop, "USB_Front.step")
export_step(final_body, step_path)
print(f"STEP exported → {step_path}")
print("Done.")