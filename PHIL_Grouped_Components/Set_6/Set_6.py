"""
Power Box – Left + Back + Right + Front + Bottom Plates (1 fused body)
           with 4 hexagonal extrude-cuts in +Z direction (27.5 mm deep)


 Left Plate   : YZ plane (x=0),      normal (-1,0,0)  → extrude +X
 Back Plate   : XZ plane (y=45.0),   normal ( 0,1,0)  → extrude -Y
 Right Plate  : YZ plane (x=1240),   normal (+1,0,0)  → extrude -X
 Front Plate  : XZ plane (y=1192.5), normal ( 0,-1,0) → extrude +Y
 Bottom Plate : XY plane (z=0),      normal ( 0,0,-1) → extrude +Z (47.5 mm)
 Cut 1–4      : hexagons at z=47.5                    → cut +Z 27.5 mm
"""


import json
import os
from build123d import *
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from ocp_vscode import show_object, show, reset_show


EXTRUDE_DEPTH     = 47.5   # mm – plates (default)
RIGHT_PLATE_DEPTH = 45.0   # mm – right plate only
CUT_EXTRUDE_DEPTH = 27.5   # mm – hex cuts
HERE = os.path.dirname(__file__)


# ── Helper: build solid from JSON profile ──────────────────────────────────────
def build_solid(json_path: str, extrude_dir: tuple, depth: float = None) -> Solid:
   if depth is None:
       depth = EXTRUDE_DEPTH
   
   with open(json_path) as f:
       data = json.load(f)


   wire_defs = list(data.values())[0][0]


   def segments_to_wire(segments):
       edges = [
           Edge.make_line(
               Vector(s["start"][0], s["start"][1], s["start"][2]),
               Vector(s["end"][0],   s["end"][1],   s["end"][2])
           )
           for s in segments
       ]
       return Wire(Wire._make_wire(edges))


   outer_wire = None
   hole_wires = []
   for wd in wire_defs:
       w = segments_to_wire(wd["segments"])
       if wd["is_outer"]:
           outer_wire = w
       else:
           hole_wires.append(w)




   mf = BRepBuilderAPI_MakeFace(outer_wire.wrapped, True)
   for hw in hole_wires:
       mf.Add(hw.wrapped)


   if not mf.IsDone():
       raise RuntimeError(f"BRepBuilderAPI_MakeFace failed for {json_path}")


   face = Face(mf.Face())
   solid = extrude(face, amount=depth, dir=extrude_dir)
   return solid




# ── Helper: build hexagonal cut tool from 6 XY points ─────────────────────────
def build_hex_cut_tool(pts6: list, label: str) -> Solid:
   """Build a hex prism 27.5 mm in -Z using Wire.make_polygon (fast)."""
   verts = [Vector(p[0], p[1], p[2]) for p in pts6]
   wire = Wire.make_polygon(verts, close=True)
   mf = BRepBuilderAPI_MakeFace(wire.wrapped, True)
   if not mf.IsDone():
       raise RuntimeError(f"BRepBuilderAPI_MakeFace failed for {label}")
   face = Face(mf.Face())
   return extrude(face, amount=CUT_EXTRUDE_DEPTH, dir=(0, 0, -1))




# ── Build the 5 plates and fuse into one box ───────────────────────────────────
left_plate = build_solid(os.path.join(HERE, "Left Plate.json"),     (1,  0,  0))


back_plate = build_solid(os.path.join(HERE, "Back Plate.json"),     (0, -1,  0))


right_plate = build_solid(os.path.join(HERE, "Right Plate.json"),   (-1,  0,  0), depth=RIGHT_PLATE_DEPTH)


front_plate = build_solid(os.path.join(HERE, "Front Plate.json"),   (0,  1,  0))


bottom_plate = build_solid(os.path.join(HERE, "Bottom Plate.json"), (0, 0, 1))


power_box = left_plate.fuse(back_plate, right_plate, front_plate, bottom_plate,
                           glue=False, tol=1e-3)
if not isinstance(power_box, Solid): power_box = power_box.solids()[0]
# (clean deferred to end)




# ── Cut 4 hexagonal pockets into the box (+Z, 27.5 mm deep from z=47.5) ───────
all_points = [
   (352.6953, 986.4844, 47.5),
   (335.3711, 1016.4844, 47.5),
   (352.6953, 1046.4844, 47.5),
   (387.3242, 1046.4844, 47.5),
   (404.6484, 1016.4844, 47.5),
   (387.3242, 986.4844, 47.5),


   (352.6953, 646.4844, 47.5),
   (387.3242, 646.4844, 47.5),
   (404.6484, 616.4844, 47.5),
   (387.3242, 586.4844, 47.5),
   (352.6953, 586.4844, 47.5),
   (335.3711, 616.4844, 47.5),


   (885.3711, 771.4844, 47.5),
   (902.6953, 801.4844, 47.5),
   (937.3242, 801.4844, 47.5),
   (954.6484, 771.4844, 47.5),
   (937.3242, 741.4844, 47.5),
   (902.6953, 741.4844, 47.5),


   (902.6953, 1041.4844, 47.5),
   (885.3711, 1071.4844, 47.5),
   (902.6953, 1101.4844, 47.5),
   (937.3242, 1101.4844, 47.5),
   (954.6484, 1071.4844, 47.5),
   (937.3242, 1041.4844, 47.5),
]


hex_groups = [all_points[i:i+6] for i in range(0, len(all_points), 6)]


hex_tools = [build_hex_cut_tool(hex_groups[i], f"Cut {i+1}") for i in range(len(hex_groups))]
hex_compound = Compound(hex_tools)
power_box = power_box.cut(hex_compound)
if not isinstance(power_box, Solid): power_box = power_box.solids()[0]


# ── Cut 2 rectangular pockets 1204.3 mm in -Z using make_box (fast) ────────────
rect_tool_1 = Solid.make_box(30, 56.9922, 1204.3,
   Plane(origin=Vector(25.0, 623.9844, 677.4599)))
rect_tool_2 = Solid.make_box(30, 56.9922, 1204.3,
   Plane(origin=Vector(1185.0, 623.9844, 677.4599)))
rect_compound = Compound([rect_tool_1, rect_tool_2])
power_box = power_box.cut(rect_compound)
if not isinstance(power_box, Solid): power_box = power_box.solids()[0]




# ── Loft body: Outer (y=0) → Inner (y=-100) ───────────────────────────────────


def pts_to_wire(pts):
   edges = []
   for i in range(len(pts)):
       a = pts[i]; b = pts[(i + 1) % len(pts)]
       edges.append(Edge.make_line(Vector(*a), Vector(*b)))
   return Wire(Wire._make_wire(edges))


outer_pts = [
   (300.0,  0.0,   1876.7599),
   (300.0,  0.0,   1676.7599),
   (0.0,    0.0,   1676.7599),
   (0.0,    0.0,   1876.7599),
]
inner_pts = [
   (100.0, -100.0, 1876.7599),
   (100.0, -100.0, 1776.7599),
   (200.0, -100.0, 1776.7599),
   (200.0, -100.0, 1876.7599),
]


outer_wire = pts_to_wire(outer_pts)
inner_wire = pts_to_wire(inner_pts)


loft_body = Solid.make_loft([outer_wire, inner_wire], ruled=False)


# (loft bodies collected below for fusing)


# ── Loft body 2: Outer (y=0) → Inner (y=-100), lower Z range ─────────────────


outer_pts_2 = [
   (0.0,   0.0,   983.5168),
   (300.0, 0.0,   983.5168),
   (300.0, 0.0,   583.5168),
   (0.0,   0.0,   583.5168),
]
inner_pts_2 = [
   (100.0, -100.0, 883.5168),
   (100.0, -100.0, 683.5168),
   (200.0, -100.0, 683.5168),
   (200.0, -100.0, 883.5168),
]


loft_body_2 = Solid.make_loft([pts_to_wire(outer_pts_2), pts_to_wire(inner_pts_2)], ruled=False)




# ── Loft body 3: Outer (y=0) → Inner (y=-100), bottom Z range ────────────────


outer_pts_3 = [
   (0.0,   0.0,   300.0),
   (300.0, 0.0,   300.0),
   (300.0, 0.0,   0.0),
   (0.0,   0.0,   0.0),
]
inner_pts_3 = [
   (100.0, -100.0, 200.0),
   (100.0, -100.0, 100.0),
   (200.0, -100.0, 100.0),
   (200.0, -100.0, 200.0),
]


loft_body_3 = Solid.make_loft([pts_to_wire(outer_pts_3), pts_to_wire(inner_pts_3)], ruled=False)




# ── Mirror all 3 loft bodies onto the right side (x mirrored about x=1240) ───


def mirror_x(pts, cx=1240):
   """Mirror points by reflecting x about cx: x_new = cx - x"""
   return [(cx - p[0], p[1], p[2]) for p in pts]


# Mirrored Loft 1
outer_pts_1m = mirror_x(outer_pts)
inner_pts_1m = mirror_x(inner_pts)
loft_body_1m = Solid.make_loft([pts_to_wire(outer_pts_1m), pts_to_wire(inner_pts_1m)], ruled=False)




# Mirrored Loft 2
outer_pts_2m = mirror_x(outer_pts_2)
inner_pts_2m = mirror_x(inner_pts_2)
loft_body_2m = Solid.make_loft([pts_to_wire(outer_pts_2m), pts_to_wire(inner_pts_2m)], ruled=False)




# Mirrored Loft 3
outer_pts_3m = mirror_x(outer_pts_3)
inner_pts_3m = mirror_x(inner_pts_3)
loft_body_3m = Solid.make_loft([pts_to_wire(outer_pts_3m), pts_to_wire(inner_pts_3m)], ruled=False)




# ── Fuse all 6 loft bodies into the Power Box ─────────────────────────────────
power_box = power_box.fuse(
   loft_body, loft_body_2, loft_body_3,
   loft_body_1m, loft_body_2m, loft_body_3m,
   glue=False, tol=1e-3
)
if not isinstance(power_box, Solid): power_box = power_box.solids()[0]
# (clean deferred to end)




# ── Loft body 4: Front face (y=1240) → outer (y=1340) ────────────────────────


outer_pts_4 = [
   (770.0, 1240.0, 677.5),
   (770.0, 1240.0, 480.0),
   (470.0, 1240.0, 480.0),
   (470.0, 1240.0, 677.5),
]
inner_pts_4 = [
   (670.0, 1340.0, 677.5),
   (570.0, 1340.0, 677.5),
   (570.0, 1340.0, 580.0),
   (670.0, 1340.0, 580.0),
]


loft_body_4 = Solid.make_loft([pts_to_wire(outer_pts_4), pts_to_wire(inner_pts_4)], ruled=False)


power_box = power_box.fuse(loft_body_4, glue=False, tol=1e-3)
if not isinstance(power_box, Solid): power_box = power_box.solids()[0]
# (clean deferred to end)




# ── Solid cylinder: r≈35, centre (620,1290), z=640, extruded 200mm in -Z ──────
import math as _math2


cylinder_points = [
   (620.0,1255.0,640.0),(613.9258,1255.5078,640.0),(626.0938,1255.5078,640.0),
   (631.9727,1257.1094,640.0),(637.5,1259.6875,640.0),(642.5,1263.1641,640.0),
   (608.0273,1257.1094,640.0),(602.5,1259.6875,640.0),(646.8164,1267.5,640.0),
   (597.5,1263.1641,640.0),(593.2031,1267.5,640.0),(589.6875,1272.5,640.0),
   (587.1094,1278.0078,640.0),(585.5469,1283.9062,640.0),(585.0,1290.0,640.0),
   (585.5469,1296.0547,640.0),(587.1094,1301.9531,640.0),(589.6875,1307.5,640.0),
   (593.2031,1312.5,640.0),(597.5,1316.7969,640.0),(602.5,1320.3125,640.0),
   (608.0273,1322.8906,640.0),(613.9258,1324.4531,640.0),(620.0,1325.0,640.0),
   (626.0938,1324.4531,640.0),(631.9727,1322.8906,640.0),(637.5,1320.3125,640.0),
   (642.5,1316.7969,640.0),(646.8164,1312.5,640.0),(650.3125,1307.5,640.0),
   (652.8906,1301.9531,640.0),(654.4727,1296.0547,640.0),(655.0,1290.0,640.0),
   (654.4727,1283.9062,640.0),(652.8906,1278.0078,640.0),(650.3125,1272.5,640.0),
]
_cyl_cx, _cyl_cy = 620.0, 1290.0
cylinder_points = sorted(cylinder_points,
   key=lambda p: _math2.atan2(p[1] - _cyl_cy, p[0] - _cyl_cx))


cyl_edges = [Edge.make_line(Vector(*cylinder_points[i]),
            Vector(*cylinder_points[(i+1)%len(cylinder_points)]))
            for i in range(len(cylinder_points))]
cyl_wire = Wire(Wire._make_wire(cyl_edges))
cyl_mf = BRepBuilderAPI_MakeFace(cyl_wire.wrapped, True)
if not cyl_mf.IsDone():
   raise RuntimeError("BRepBuilderAPI_MakeFace failed for cylinder profile")
cyl_face = Face(cyl_mf.Face())
cyl_tool = extrude(cyl_face, amount=200, dir=(0, 0, -1))
power_box = power_box.cut(cyl_tool)
# (clean deferred to end)




# ── Two solid cylinders from hole.txt: r=30, z=1826.76, extruded 60mm +Z ──────
import math as _math3


_all_hole_pts = [
   (147.2461,-20.1172,1826.7599),(141.7969,-21.1328,1826.7599),(136.6406,-23.1641,1826.7599),
   (131.9336,-26.0547,1826.7599),(127.832,-29.8047,1826.7599),(152.7734,-20.1172,1826.7599),
   (158.2227,-21.1328,1826.7599),(163.3789,-23.1641,1826.7599),(168.0859,-26.0547,1826.7599),
   (172.168,-29.8047,1826.7599),(175.5078,-34.2188,1826.7599),(177.9883,-39.1797,1826.7599),
   (179.4922,-44.4922,1826.7599),(180.0,-50.0,1826.7599),(179.4922,-55.5078,1826.7599),
   (177.9883,-60.8594,1826.7599),(175.5078,-65.7812,1826.7599),(172.168,-70.2344,1826.7599),
   (168.0859,-73.9453,1826.7599),(163.3789,-76.875,1826.7599),(158.2227,-78.8672,1826.7599),
   (152.7734,-79.8828,1826.7599),(147.2461,-79.8828,1826.7599),(141.7969,-78.8672,1826.7599),
   (136.6406,-76.875,1826.7599),(131.9336,-73.9453,1826.7599),(127.832,-70.2344,1826.7599),
   (124.4922,-65.7812,1826.7599),(122.0312,-60.8594,1826.7599),(120.5078,-55.5078,1826.7599),
   (120.0,-50.0,1826.7599),(120.5078,-44.4922,1826.7599),(122.0312,-39.1797,1826.7599),
   (124.4922,-34.2188,1826.7599),
   (1067.832,-29.8047,1826.7599),(1064.4922,-34.2188,1826.7599),(1062.0312,-39.1797,1826.7599),
   (1060.5078,-44.4922,1826.7599),(1060.0,-50.0,1826.7599),(1060.5078,-55.5078,1826.7599),
   (1076.6406,-76.875,1826.7599),(1071.9336,-73.9453,1826.7599),(1067.832,-70.2344,1826.7599),
   (1064.4922,-65.7812,1826.7599),(1062.0312,-60.8594,1826.7599),(1081.7969,-78.8672,1826.7599),
   (1087.2461,-79.8828,1826.7599),(1092.7734,-79.8828,1826.7599),(1098.2227,-78.8672,1826.7599),
   (1103.3789,-76.875,1826.7599),(1108.0859,-73.9453,1826.7599),(1112.168,-70.2344,1826.7599),
   (1115.5078,-65.7812,1826.7599),(1117.9883,-60.8594,1826.7599),(1119.4922,-55.5078,1826.7599),
   (1120.0,-50.0,1826.7599),(1119.4922,-44.4922,1826.7599),(1117.9883,-39.1797,1826.7599),
   (1115.5078,-34.2188,1826.7599),(1112.168,-29.8047,1826.7599),(1108.0859,-26.0547,1826.7599),
   (1103.3789,-23.1641,1826.7599),(1092.7734,-20.1172,1826.7599),(1098.2227,-21.1328,1826.7599),
   (1087.2461,-20.1172,1826.7599),(1081.7969,-21.1328,1826.7599),(1076.6406,-23.1641,1826.7599),
   (1071.9336,-26.0547,1826.7599),
]


def _make_circle_solid(pts, cx, cy, label):
   sorted_pts = sorted(pts, key=lambda p: _math3.atan2(p[1]-cy, p[0]-cx))
   edges = [Edge.make_line(Vector(*sorted_pts[i]), Vector(*sorted_pts[(i+1)%len(sorted_pts)]))
            for i in range(len(sorted_pts))]
   wire = Wire(Wire._make_wire(edges))
   mf = BRepBuilderAPI_MakeFace(wire.wrapped, True)
   if not mf.IsDone():
       raise RuntimeError(f"Face failed for {label}")
   face = Face(mf.Face())
   solid = extrude(face, amount=60, dir=(0, 0, 1))
   return solid


cyl_pts_1 = [p for p in _all_hole_pts if p[0] < 500]
cyl_pts_2 = [p for p in _all_hole_pts if p[0] > 500]


cyl_solid_1 = _make_circle_solid(cyl_pts_1, 150.0, -50.0, "Cylinder A")
cyl_solid_2 = _make_circle_solid(cyl_pts_2, 1090.0, -50.0, "Cylinder B")
power_box = power_box.cut(cyl_solid_1).cut(cyl_solid_2)
# (clean deferred to end)




# ── Through-hole: r≈15, centre (620,1290), z=677.5, cut 50mm in both ±Z ───────
import math as _math4


_th_points = [
   (632.9883,1282.5,677.5),(634.4922,1286.0938,677.5),(635.0,1290.0,677.5),
   (634.4922,1293.8672,677.5),(632.9883,1297.5,677.5),(630.6055,1300.5859,677.5),
   (627.5,1302.9688,677.5),(623.8867,1304.4922,677.5),(620.0,1305.0,677.5),
   (630.6055,1279.375,677.5),(627.5,1276.9922,677.5),(623.8867,1275.5078,677.5),
   (620.0,1275.0,677.5),(616.1328,1275.5078,677.5),(612.5,1276.9922,677.5),
   (609.3945,1279.375,677.5),(607.0117,1282.5,677.5),(605.5078,1286.0938,677.5),
   (605.0,1290.0,677.5),(605.5078,1293.8672,677.5),(607.0117,1297.5,677.5),
   (609.3945,1300.5859,677.5),(612.5,1302.9688,677.5),(616.1328,1304.4922,677.5),
]
_th_cx, _th_cy = 620.0, 1290.0
_th_pts = sorted(_th_points, key=lambda p: _math4.atan2(p[1]-_th_cy, p[0]-_th_cx))
_th_edges = [Edge.make_line(Vector(*_th_pts[i]), Vector(*_th_pts[(i+1)%len(_th_pts)]))
            for i in range(len(_th_pts))]
_th_wire = Wire(Wire._make_wire(_th_edges))
_th_mf = BRepBuilderAPI_MakeFace(_th_wire.wrapped, True)
if not _th_mf.IsDone():
   raise RuntimeError("BRepBuilderAPI_MakeFace failed for through-hole")
_th_face = Face(_th_mf.Face())
_th_tool = extrude(_th_face, amount=50, dir=(0,0,1)).fuse(
          extrude(_th_face, amount=50, dir=(0,0,-1)))
power_box = power_box.cut(_th_tool)
# (clean deferred to end)




# ── Chamfer loft: outer r≈35 (z=640) → inner r≈15 (z=670), height=30mm ───────
import math as _math5


_outer_chamfer_raw = [
   (654.4727,1283.9062,640.0),(652.8906,1278.0078,640.0),(650.3125,1272.5,640.0),
   (646.8164,1267.5,640.0),(642.5,1263.1641,640.0),(655.0,1290.0,640.0),
   (654.4727,1296.0547,640.0),(650.3125,1307.5,640.0),(652.8906,1301.9531,640.0),
   (646.8164,1312.5,640.0),(642.5,1316.7969,640.0),(637.5,1320.3125,640.0),
   (631.9727,1322.8906,640.0),(626.0938,1324.4531,640.0),(613.9258,1324.4531,640.0),
   (620.0,1325.0,640.0),(608.0273,1322.8906,640.0),(602.5,1320.3125,640.0),
   (597.5,1316.7969,640.0),(593.2031,1312.5,640.0),(589.6875,1307.5,640.0),
   (587.1094,1301.9531,640.0),(585.5469,1296.0547,640.0),(585.0,1290.0,640.0),
   (585.5469,1283.9062,640.0),(587.1094,1278.0078,640.0),(589.6875,1272.5,640.0),
   (593.2031,1267.5,640.0),(597.5,1263.1641,640.0),(602.5,1259.6875,640.0),
   (608.0273,1257.1094,640.0),(613.9258,1255.5078,640.0),(620.0,1255.0,640.0),
   (626.0938,1255.5078,640.0),(631.9727,1257.1094,640.0),(637.5,1259.6875,640.0),
]
_inner_chamfer_raw = [
   (632.9883,1282.5,677.5),(634.4922,1286.0938,677.5),(635.0,1290.0,677.5),
   (634.4922,1293.8672,677.5),(632.9883,1297.5,677.5),(630.6055,1300.5859,677.5),
   (627.5,1302.9688,677.5),(623.8867,1304.4922,677.5),(620.0,1305.0,677.5),
   (630.6055,1279.375,677.5),(627.5,1276.9922,677.5),(623.8867,1275.5078,677.5),
   (620.0,1275.0,677.5),(616.1328,1275.5078,677.5),(612.5,1276.9922,677.5),
   (609.3945,1279.375,677.5),(607.0117,1282.5,677.5),(605.5078,1286.0938,677.5),
   (605.0,1290.0,677.5),(605.5078,1293.8672,677.5),(607.0117,1297.5,677.5),
   (609.3945,1300.5859,677.5),(612.5,1302.9688,677.5),(616.1328,1304.4922,677.5),
]


_chf_cx, _chf_cy = 620.0, 1290.0
_outer_chf = sorted(_outer_chamfer_raw, key=lambda p: _math5.atan2(p[1]-_chf_cy, p[0]-_chf_cx))
_inner_chf = sorted([(p[0], p[1], 670.0) for p in _inner_chamfer_raw],
                   key=lambda p: _math5.atan2(p[1]-_chf_cy, p[0]-_chf_cx))


def _chf_wire(pts):
   edges = [Edge.make_line(Vector(*pts[i]), Vector(*pts[(i+1)%len(pts)]))
            for i in range(len(pts))]
   return Wire(Wire._make_wire(edges))


chamfer_body = Solid.make_loft([_chf_wire(_outer_chf), _chf_wire(_inner_chf)], ruled=False)
power_box = power_box.cut(chamfer_body)
# (clean deferred to end)




# ── Chamfer loft (YZ plane): outer r≈37.5 (x=1240) → inner r≈30 (x=1231.43) ─
import math as _math6


_outer_yz_raw = [
   (1240.0,202.5781,497.8421),(1240.0,206.4062,502.7296),(1240.0,209.3359,508.1765),
   (1240.0,211.3281,514.0344),(1240.0,212.3828,520.1434),(1240.0,212.3828,526.3369),
   (1240.0,211.3281,532.4458),(1240.0,209.3359,538.3037),(1240.0,202.5781,548.6382),
   (1240.0,206.4062,543.7507),(1240.0,198.0469,552.8329),(1240.0,192.8516,556.2204),
   (1240.0,181.1719,560.2286),(1240.0,187.1875,558.7083),(1240.0,175.0,560.7401),
   (1240.0,168.8281,560.2286),(1240.0,162.8125,558.7083),(1240.0,157.1484,556.2204),
   (1240.0,151.9531,552.8329),(1240.0,147.4219,548.6382),(1240.0,143.5938,543.7507),
   (1240.0,140.6641,538.3037),(1240.0,138.6328,532.4458),(1240.0,137.6172,526.3369),
   (1240.0,137.6172,520.1434),(1240.0,138.6328,514.0344),(1240.0,140.6641,508.1765),
   (1240.0,143.5938,502.7296),(1240.0,147.4219,497.8421),(1240.0,151.9531,493.6473),
   (1240.0,157.1484,490.2598),(1240.0,162.8125,487.772),(1240.0,168.8281,486.2516),
   (1240.0,175.0,485.7401),(1240.0,181.1719,486.2516),(1240.0,187.1875,487.772),
   (1240.0,192.8516,490.2598),(1240.0,198.0469,493.6473),
]
_inner_yz_raw = [
   (1231.4258,190.7812,497.7336),(1231.4258,195.1953,501.0699),(1231.4258,198.9453,505.1611),
   (1231.4258,201.8359,509.868),(1231.4258,203.8672,515.0302),(1231.4258,204.8828,520.4721),
   (1231.4258,204.8828,526.0082),(1231.4258,203.8672,531.45),(1231.4258,201.8359,536.6123),
   (1231.4258,195.1953,545.4104),(1231.4258,198.9453,541.3192),(1231.4258,190.7812,548.7466),
   (1231.4258,185.8203,551.2143),(1231.4258,180.5078,552.7293),(1231.4258,175.0,553.2401),
   (1231.4258,169.4922,552.7293),(1231.4258,164.1406,551.2143),(1231.4258,159.2188,548.7466),
   (1231.4258,154.7656,545.4104),(1231.4258,151.0547,541.3192),(1231.4258,148.125,536.6123),
   (1231.4258,146.1328,531.45),(1231.4258,145.1172,526.0082),(1231.4258,145.1172,520.4721),
   (1231.4258,146.1328,515.0302),(1231.4258,148.125,509.868),(1231.4258,151.0547,505.1611),
   (1231.4258,154.7656,501.0699),(1231.4258,159.2188,497.7336),(1231.4258,164.1406,495.266),
   (1231.4258,169.4922,493.7509),(1231.4258,175.0,493.2401),(1231.4258,180.5078,493.7509),
   (1231.4258,185.8203,495.266),
]


_yz_cy, _yz_cz = 175.0, 523.24
_outer_yz = sorted(_outer_yz_raw, key=lambda p: _math6.atan2(p[2]-_yz_cz, p[1]-_yz_cy))
_inner_yz = sorted(_inner_yz_raw, key=lambda p: _math6.atan2(p[2]-_yz_cz, p[1]-_yz_cy))


def _yz_wire(pts):
   edges = [Edge.make_line(Vector(*pts[i]), Vector(*pts[(i+1)%len(pts)])) for i in range(len(pts))]
   return Wire(Wire._make_wire(edges))


yz_chamfer_body = Solid.make_loft([_yz_wire(_outer_yz), _yz_wire(_inner_yz)], ruled=False)


# ── Mirror YZ chamfer to left plate (x=0): reflect x about x=620 ──────────────


_outer_yz_m = [(1240.0 - p[0], p[1], p[2]) for p in _outer_yz_raw]
_inner_yz_m = [(1240.0 - p[0], p[1], p[2]) for p in _inner_yz_raw]


_outer_yz_ms = sorted(_outer_yz_m, key=lambda p: _math6.atan2(p[2]-_yz_cz, p[1]-_yz_cy))
_inner_yz_ms = sorted(_inner_yz_m, key=lambda p: _math6.atan2(p[2]-_yz_cz, p[1]-_yz_cy))


yz_chamfer_mirror = Solid.make_loft([_yz_wire(_outer_yz_ms), _yz_wire(_inner_yz_ms)], ruled=False)




# ── Hollow cylinder: outer r≈37.5 (x=0) inner r≈30 (x=45.0), extrude +X ──────
import math as _math8


_hc_outer_raw = [
   (0.0,175.0,485.7401),(0.0,168.8281,486.2516),(0.0,162.8125,487.772),
   (0.0,157.1484,490.2598),(0.0,151.9531,493.6473),(0.0,147.4219,497.8421),
   (0.0,143.5938,502.7296),(0.0,140.6641,508.1765),(0.0,138.6328,514.0344),
   (0.0,137.6172,520.1434),(0.0,137.6172,526.3369),(0.0,138.6328,532.4458),
   (0.0,140.6641,538.3037),(0.0,143.5938,543.7507),(0.0,147.4219,548.6382),
   (0.0,151.9531,552.8329),(0.0,157.1484,556.2204),(0.0,162.8125,558.7083),
   (0.0,168.8281,560.2286),(0.0,175.0,560.7401),(0.0,181.1719,560.2286),
   (0.0,187.1875,558.7083),(0.0,192.8516,556.2204),(0.0,198.0469,552.8329),
   (0.0,202.5781,548.6382),(0.0,206.4062,543.7507),(0.0,209.3359,538.3037),
   (0.0,211.3281,532.4458),(0.0,212.3828,520.1434),(0.0,212.3828,526.3369),
   (0.0,211.3281,514.0344),(0.0,209.3359,508.1765),(0.0,206.4062,502.7296),
   (0.0,202.5781,497.8421),(0.0,198.0469,493.6473),(0.0,192.8516,490.2598),
   (0.0,187.1875,487.772),(0.0,181.1719,486.2516),
]
_hc_inner_raw = [
   (45.0,185.8203,495.266),(45.0,190.7812,497.7336),(45.0,195.1953,501.0699),
   (45.0,198.9453,505.1611),(45.0,201.8359,509.868),(45.0,203.8672,515.0302),
   (45.0,204.8828,520.4721),(45.0,204.8828,526.0082),(45.0,203.8672,531.45),
   (45.0,201.8359,536.6123),(45.0,198.9453,541.3192),(45.0,195.1953,545.4104),
   (45.0,190.7812,548.7466),(45.0,180.5078,552.7293),(45.0,185.8203,551.2143),
   (45.0,175.0,553.2401),(45.0,169.4922,552.7293),(45.0,164.1406,551.2143),
   (45.0,159.2188,548.7466),(45.0,154.7656,545.4104),(45.0,151.0547,541.3192),
   (45.0,148.125,536.6123),(45.0,146.1328,531.45),(45.0,145.1172,526.0082),
   (45.0,145.1172,520.4721),(45.0,146.1328,515.0302),(45.0,148.125,509.868),
   (45.0,180.5078,493.7509),(45.0,175.0,493.2401),(45.0,169.4922,493.7509),
   (45.0,164.1406,495.266),(45.0,159.2188,497.7336),(45.0,154.7656,501.0699),
   (45.0,151.0547,505.1611),
]


_hc_cy, _hc_cz = 175.0, 523.24
_hc_outer_s = sorted(_hc_outer_raw, key=lambda p: _math8.atan2(p[2]-_hc_cz, p[1]-_hc_cy))
_hc_inner_s = sorted(_hc_inner_raw, key=lambda p: _math8.atan2(p[2]-_hc_cz, p[1]-_hc_cy), reverse=True)
_hc_inner_proj = [(0.0, p[1], p[2]) for p in _hc_inner_s]


def _hc_wire(pts):
   edges = [Edge.make_line(Vector(*pts[i]), Vector(*pts[(i+1)%len(pts)])) for i in range(len(pts))]
   return Wire(Wire._make_wire(edges))


_hc_mf = BRepBuilderAPI_MakeFace(_hc_wire(_hc_outer_s).wrapped, True)
_hc_mf.Add(_hc_wire(_hc_inner_proj).wrapped)
if not _hc_mf.IsDone():
   raise RuntimeError("BRepBuilderAPI_MakeFace failed for hollow cylinder")
_hc_face = Face(_hc_mf.Face())
hollow_cylinder = extrude(_hc_face, amount=45.0, dir=(1, 0, 0))




# ── Mirror hollow cylinder to right side (x=1240) and fuse both into Power Box ─
_hc_outer_m = [(1240.0 - p[0], p[1], p[2]) for p in _hc_outer_s]
_hc_inner_m = [(1195.0 - (p[0] - 0.0), p[1], p[2]) for p in _hc_inner_proj]


_hc_outer_ms = sorted(_hc_outer_m, key=lambda p: _math8.atan2(p[2]-_hc_cz, p[1]-_hc_cy))
_hc_inner_ms = sorted([(1240.0, p[1], p[2]) for p in _hc_inner_raw],
                      key=lambda p: _math8.atan2(p[2]-_hc_cz, p[1]-_hc_cy), reverse=True)
_hc_inner_mproj = [(1240.0, p[1], p[2]) for p in _hc_inner_ms]


_hc_mf2 = BRepBuilderAPI_MakeFace(_hc_wire(_hc_outer_ms).wrapped, True)
_hc_mf2.Add(_hc_wire(_hc_inner_mproj).wrapped)
if not _hc_mf2.IsDone():
   raise RuntimeError("BRepBuilderAPI_MakeFace failed for mirrored hollow cylinder")
_hc_face2 = Face(_hc_mf2.Face())
hollow_cylinder_mirror = extrude(_hc_face2, amount=45.0, dir=(-1, 0, 0))


power_box = power_box.fuse(hollow_cylinder, glue=False, tol=1e-3)
if not isinstance(power_box, Solid): power_box = power_box.solids()[0]
power_box = power_box.fuse(hollow_cylinder_mirror, glue=False, tol=1e-3)
if not isinstance(power_box, Solid): power_box = power_box.solids()[0]
# (clean deferred to end)


power_box = power_box.cut(yz_chamfer_body)
if not isinstance(power_box, Solid): power_box = power_box.solids()[0]
power_box = power_box.cut(yz_chamfer_mirror)
if not isinstance(power_box, Solid): power_box = power_box.solids()[0]
# (clean deferred to end)




# ── Hollow cylinder 2: outer r≈37.5 (x=0) inner r≈30 (x=8.57), +X 50mm ───────
import math as _math9


_hc2_outer_raw = [
   (0.0,397.4219,497.8421),(0.0,401.9531,493.6473),(0.0,393.5938,502.7296),
   (0.0,390.6641,508.1765),(0.0,388.6328,514.0344),(0.0,387.6172,520.1434),
   (0.0,387.6172,526.3369),(0.0,388.6328,532.4458),(0.0,390.6641,538.3037),
   (0.0,393.5938,543.7507),(0.0,397.4219,548.6382),(0.0,401.9531,552.8329),
   (0.0,407.1484,556.2204),(0.0,412.8125,558.7083),(0.0,418.8281,560.2286),
   (0.0,425.0,560.7401),(0.0,431.1719,560.2286),(0.0,437.1875,558.7083),
   (0.0,442.8516,556.2204),(0.0,448.0469,552.8329),(0.0,452.5781,548.6382),
   (0.0,456.4062,543.7507),(0.0,459.3359,538.3037),(0.0,461.3281,532.4458),
   (0.0,462.3828,526.3369),(0.0,462.3828,520.1434),(0.0,461.3281,514.0344),
   (0.0,459.3359,508.1765),(0.0,456.4062,502.7296),(0.0,452.5781,497.8421),
   (0.0,448.0469,493.6473),(0.0,442.8516,490.2598),(0.0,437.1875,487.772),
   (0.0,431.1719,486.2516),(0.0,425.0,485.7401),(0.0,418.8281,486.2516),
   (0.0,412.8125,487.772),(0.0,407.1484,490.2598),
]
_hc2_inner_raw = [
   (8.5742,419.4922,493.7509),(8.5742,414.1406,495.266),(8.5742,409.2188,497.7336),
   (8.5742,404.7656,501.0699),(8.5742,401.0547,505.1611),(8.5742,398.125,509.868),
   (8.5742,396.1328,515.0302),(8.5742,395.1172,520.4721),(8.5742,395.1172,526.0082),
   (8.5742,396.1328,531.45),(8.5742,398.125,536.6123),(8.5742,401.0547,541.3192),
   (8.5742,404.7656,545.4104),(8.5742,409.2188,548.7466),(8.5742,414.1406,551.2143),
   (8.5742,419.4922,552.7293),(8.5742,425.0,553.2401),(8.5742,430.5078,552.7293),
   (8.5742,435.8203,551.2143),(8.5742,440.7812,548.7466),(8.5742,425.0,493.2401),
   (8.5742,430.5078,493.7509),(8.5742,440.7812,497.7336),(8.5742,435.8203,495.266),
   (8.5742,445.1953,501.0699),(8.5742,448.9453,505.1611),(8.5742,451.8359,509.868),
   (8.5742,453.8672,515.0302),(8.5742,454.8828,520.4721),(8.5742,454.8828,526.0082),
   (8.5742,453.8672,531.45),(8.5742,451.8359,536.6123),(8.5742,448.9453,541.3192),
   (8.5742,445.1953,545.4104),
]


_hc2_cy, _hc2_cz = 425.0, 523.24
_hc2_outer_s = sorted(_hc2_outer_raw, key=lambda p: _math9.atan2(p[2]-_hc2_cz, p[1]-_hc2_cy))
_hc2_inner_s = sorted(_hc2_inner_raw, key=lambda p: _math9.atan2(p[2]-_hc2_cz, p[1]-_hc2_cy), reverse=True)
_hc2_inner_proj = [(0.0, p[1], p[2]) for p in _hc2_inner_s]


def _hc2_wire(pts):
   edges = [Edge.make_line(Vector(*pts[i]), Vector(*pts[(i+1)%len(pts)])) for i in range(len(pts))]
   return Wire(Wire._make_wire(edges))


_hc2_mf = BRepBuilderAPI_MakeFace(_hc2_wire(_hc2_outer_s).wrapped, True)
_hc2_mf.Add(_hc2_wire(_hc2_inner_proj).wrapped)
if not _hc2_mf.IsDone():
   raise RuntimeError("BRepBuilderAPI_MakeFace failed for hollow cylinder 2")
_hc2_face = Face(_hc2_mf.Face())
hollow_cylinder_2 = extrude(_hc2_face, amount=50, dir=(1, 0, 0))


# ── Fuse hollow cylinder 2 into Power Box ─────────────────────────────────────
power_box = power_box.fuse(hollow_cylinder_2, glue=False, tol=1e-3)
# (clean deferred to end)


# ── Chamfer loft: outer r≈37.5 (x=0) → inner r≈30 (x=8.57), height=8.55mm ────
import math as _math10


_chf2_outer_raw = [
   (0.0,397.4219,497.8421),(0.0,401.9531,493.6473),(0.0,393.5938,502.7296),
   (0.0,390.6641,508.1765),(0.0,388.6328,514.0344),(0.0,387.6172,520.1434),
   (0.0,387.6172,526.3369),(0.0,388.6328,532.4458),(0.0,390.6641,538.3037),
   (0.0,393.5938,543.7507),(0.0,397.4219,548.6382),(0.0,401.9531,552.8329),
   (0.0,407.1484,556.2204),(0.0,412.8125,558.7083),(0.0,418.8281,560.2286),
   (0.0,425.0,560.7401),(0.0,431.1719,560.2286),(0.0,437.1875,558.7083),
   (0.0,442.8516,556.2204),(0.0,448.0469,552.8329),(0.0,452.5781,548.6382),
   (0.0,456.4062,543.7507),(0.0,459.3359,538.3037),(0.0,461.3281,532.4458),
   (0.0,462.3828,526.3369),(0.0,462.3828,520.1434),(0.0,461.3281,514.0344),
   (0.0,459.3359,508.1765),(0.0,456.4062,502.7296),(0.0,452.5781,497.8421),
   (0.0,448.0469,493.6473),(0.0,442.8516,490.2598),(0.0,437.1875,487.772),
   (0.0,431.1719,486.2516),(0.0,425.0,485.7401),(0.0,418.8281,486.2516),
   (0.0,412.8125,487.772),(0.0,407.1484,490.2598),
]
_chf2_inner_raw = [
   (8.5742,419.4922,493.7509),(8.5742,414.1406,495.266),(8.5742,409.2188,497.7336),
   (8.5742,404.7656,501.0699),(8.5742,401.0547,505.1611),(8.5742,398.125,509.868),
   (8.5742,396.1328,515.0302),(8.5742,395.1172,520.4721),(8.5742,395.1172,526.0082),
   (8.5742,396.1328,531.45),(8.5742,398.125,536.6123),(8.5742,401.0547,541.3192),
   (8.5742,404.7656,545.4104),(8.5742,409.2188,548.7466),(8.5742,414.1406,551.2143),
   (8.5742,419.4922,552.7293),(8.5742,425.0,553.2401),(8.5742,430.5078,552.7293),
   (8.5742,435.8203,551.2143),(8.5742,440.7812,548.7466),(8.5742,425.0,493.2401),
   (8.5742,430.5078,493.7509),(8.5742,440.7812,497.7336),(8.5742,435.8203,495.266),
   (8.5742,445.1953,501.0699),(8.5742,448.9453,505.1611),(8.5742,451.8359,509.868),
   (8.5742,453.8672,515.0302),(8.5742,454.8828,520.4721),(8.5742,454.8828,526.0082),
   (8.5742,453.8672,531.45),(8.5742,451.8359,536.6123),(8.5742,448.9453,541.3192),
   (8.5742,445.1953,545.4104),
]


_chf2_cy, _chf2_cz = 425.0, 523.24
_chf2_outer_s = sorted(_chf2_outer_raw, key=lambda p: _math10.atan2(p[2]-_chf2_cz, p[1]-_chf2_cy))
_chf2_inner_s = sorted(_chf2_inner_raw, key=lambda p: _math10.atan2(p[2]-_chf2_cz, p[1]-_chf2_cy))


def _chf2_wire(pts):
   edges = [Edge.make_line(Vector(*pts[i]), Vector(*pts[(i+1)%len(pts)])) for i in range(len(pts))]
   return Wire(Wire._make_wire(edges))


chamfer_2 = Solid.make_loft([_chf2_wire(_chf2_outer_s), _chf2_wire(_chf2_inner_s)], ruled=False)


power_box = power_box.cut(chamfer_2)
# (clean deferred to end)




# ── Back-face chamfer lofts: Outer.txt (y=0, big dia) → inner.txt (y=8.55, small dia) ──
# Two separate bodies, one per circle (x≈365 and x≈865). NOT fused into power_box.
import math as _math13


_back_outer_all = [
   (341.9727,-0.0,552.8329),(337.4219,-0.0,548.6382),(333.6133,-0.0,543.7507),
   (330.6641,-0.0,538.3037),(328.6523,-0.0,532.4458),(327.6367,-0.0,526.3369),
   (327.6367,-0.0,520.1434),(328.6523,-0.0,514.0344),(330.6641,-0.0,508.1765),
   (333.6133,-0.0,502.7296),(337.4219,-0.0,497.8421),(347.168,-0.0,490.2598),
   (352.832,-0.0,487.772),(341.9727,-0.0,493.6473),(358.8281,-0.0,486.2516),
   (365.0,-0.0,485.7401),(371.1719,-0.0,486.2516),(377.1875,-0.0,487.772),
   (382.8516,-0.0,490.2598),(388.0469,-0.0,493.6473),(392.5977,-0.0,497.8421),
   (396.4062,-0.0,502.7296),(399.3555,-0.0,508.1765),(401.3672,-0.0,514.0344),
   (402.3828,-0.0,520.1434),(402.3828,-0.0,526.3369),(401.3672,-0.0,532.4458),
   (399.3555,-0.0,538.3037),(396.4062,-0.0,543.7507),(392.5977,-0.0,548.6382),
   (388.0469,-0.0,552.8329),(382.8516,-0.0,556.2204),(377.1875,-0.0,558.7083),
   (371.1719,-0.0,560.2286),(365.0,-0.0,560.7401),(358.8281,-0.0,560.2286),
   (352.832,-0.0,558.7083),(347.168,-0.0,556.2204),
   (858.8281,0.0,560.2286),(852.832,0.0,558.7083),(847.168,0.0,556.2204),
   (841.9727,0.0,552.8329),(837.4219,0.0,548.6382),(833.6133,0.0,543.7507),
   (830.6641,0.0,538.3037),(828.6523,0.0,532.4458),(827.6367,0.0,526.3369),
   (828.6523,0.0,514.0344),(827.6367,0.0,520.1434),(830.6641,0.0,508.1765),
   (833.6133,0.0,502.7296),(837.4219,0.0,497.8421),(841.9727,0.0,493.6473),
   (847.168,0.0,490.2598),(852.832,0.0,487.772),(858.8281,0.0,486.2516),
   (865.0,0.0,485.7401),(871.1719,0.0,486.2516),(877.1875,0.0,487.772),
   (882.8516,0.0,490.2598),(888.0469,0.0,493.6473),(892.5977,0.0,497.8421),
   (896.4062,0.0,502.7296),(899.3555,0.0,508.1765),(901.3672,0.0,514.0344),
   (902.3828,0.0,520.1434),(902.3828,0.0,526.3369),(901.3672,0.0,532.4458),
   (899.3555,0.0,538.3037),(896.4062,0.0,543.7507),(892.5977,0.0,548.6382),
   (888.0469,0.0,552.8329),(882.8516,0.0,556.2204),(877.1875,0.0,558.7083),
   (871.1719,0.0,560.2286),(865.0,0.0,560.7401),
]


_back_inner_all = [
   (344.8047,-0.0,545.4104),(341.0742,-0.0,541.3192),(338.1445,-0.0,536.6123),
   (336.1523,-0.0,531.45),(335.1367,-0.0,526.0082),(335.1367,-0.0,520.4721),
   (336.1523,-0.0,515.0302),(338.1445,-0.0,509.868),(341.0742,-0.0,505.1611),
   (344.8047,-0.0,501.0699),(349.2188,-0.0,497.7336),(359.4922,-0.0,493.7509),
   (354.1602,-0.0,495.266),(365.0,-0.0,493.2401),(370.5273,-0.0,493.7509),
   (375.8398,-0.0,495.266),(380.8008,-0.0,497.7336),(385.2148,-0.0,501.0699),
   (388.9453,-0.0,505.1611),(391.8555,-0.0,509.868),(393.8672,-0.0,515.0302),
   (394.8828,-0.0,520.4721),(394.8828,-0.0,526.0082),(393.8672,-0.0,531.45),
   (391.8555,-0.0,536.6123),(388.9453,-0.0,541.3192),(385.2148,-0.0,545.4104),
   (380.8008,-0.0,548.7466),(375.8398,-0.0,551.2143),(370.5273,-0.0,552.7293),
   (365.0,-0.0,553.2401),(359.4922,-0.0,552.7293),(354.1602,-0.0,551.2143),
   (349.2188,-0.0,548.7466),
   (835.1367,0.0,526.0082),(838.1445,0.0,536.6123),(841.0742,0.0,541.3192),
   (836.1523,0.0,531.45),(844.8047,0.0,545.4104),(849.2188,0.0,548.7466),
   (854.1602,0.0,551.2143),(859.4922,0.0,552.7293),(865.0,0.0,553.2401),
   (870.5273,0.0,552.7293),(875.8398,0.0,551.2143),(880.8008,0.0,548.7466),
   (885.2148,0.0,545.4104),(888.9453,0.0,541.3192),(891.8555,0.0,536.6123),
   (893.8672,0.0,531.45),(894.8828,0.0,526.0082),(894.8828,0.0,520.4721),
   (893.8672,0.0,515.0302),(891.8555,0.0,509.868),(888.9453,0.0,505.1611),
   (885.2148,0.0,501.0699),(880.8008,0.0,497.7336),(875.8398,0.0,495.266),
   (870.5273,0.0,493.7509),(865.0,0.0,493.2401),(859.4922,0.0,493.7509),
   (854.1602,0.0,495.266),(849.2188,0.0,497.7336),(844.8047,0.0,501.0699),
   (841.0742,0.0,505.1611),(838.1445,0.0,509.868),(836.1523,0.0,515.0302),
   (835.1367,0.0,520.4721),
]


_BACK_CHAMFER_H = 8.55  # mm, extrude in +Y


def _make_back_chamfer(outer_pts, inner_pts, cx, cz, label):
   """Loft outer ring (y=0, big dia) → inner ring (y=8.55, small dia) in +Y."""
   # Sort both rings by angle around their centre
   o_s = sorted(outer_pts, key=lambda p: _math13.atan2(p[2]-cz, p[0]-cx))
   i_s = sorted(inner_pts, key=lambda p: _math13.atan2(p[2]-cz, p[0]-cx))
   # Shift inner ring to y=8.55
   i_shifted = [(p[0], _BACK_CHAMFER_H, p[2]) for p in i_s]


   def _w(pts):
       edges = [Edge.make_line(Vector(*pts[j]), Vector(*pts[(j+1)%len(pts)]))
                for j in range(len(pts))]
       return Wire(Wire._make_wire(edges))


   return Solid.make_loft([_w(o_s), _w(i_shifted)], ruled=False)


# Split by x < 600 → circle at x=365, x >= 600 → circle at x=865
_bo1 = [p for p in _back_outer_all if p[0] < 600]
_bo2 = [p for p in _back_outer_all if p[0] >= 600]
_bi1 = [p for p in _back_inner_all if p[0] < 600]
_bi2 = [p for p in _back_inner_all if p[0] >= 600]


back_chamfer_1 = _make_back_chamfer(_bo1, _bi1, 365.0, 523.24, "Back Chamfer 1 (x=365)")
back_chamfer_2 = _make_back_chamfer(_bo2, _bi2, 865.0, 523.24, "Back Chamfer 2 (x=865)")


# Cut both chamfer bodies from the power box
power_box = power_box.cut(back_chamfer_1)
if not isinstance(power_box, Solid): power_box = power_box.solids()[0]
power_box = power_box.cut(back_chamfer_2)
if not isinstance(power_box, Solid): power_box = power_box.solids()[0]




try:
   # ── Text: rotated 90° CW, runs in -Z, lines stack in X, left-aligned ───────────
   _font_h       = 100
   _txt_depth    = 3
   _line_spacing = 25
   _x_centre     = 621.25
   _y_face       = 3.0   # moved 3mm in +Y
   _z_start      = 362.5 + 1183.7   # moved 1183.7mm in +Z
   _total_h      = 3 * _font_h + 2 * _line_spacing
   _x_top = _x_centre + _total_h / 2 - _font_h / 2
   _x_mid = _x_centre
   _x_bot = _x_centre - _total_h / 2 + _font_h / 2


   _text_lines = [
       ("Designed by Phillip Dettinger", _x_top),
       ("Cell Systems Dynamics Group",   _x_mid),
       ("ETH Zurich",                    _x_bot),
   ]


   _txt_tools = []
   for _txt, _x_pos in _text_lines:
       _plane = Plane(origin=Vector(_x_pos, _y_face, _z_start),
                      x_dir=Vector(0, 0, -1),   # text runs in -Z (90° CW from +X)
                      z_dir=Vector(0, -1, 0))   # normal = -Y (outward)
       with BuildSketch(_plane) as _sk:
           Text(_txt, font_size=_font_h, align=(Align.MIN, Align.CENTER))
       _txt_tools.append(extrude(_sk.sketch, amount=_txt_depth))
   _txt_compound = Compound(_txt_tools)
   power_box = power_box.cut(_txt_compound)
   if not isinstance(power_box, Solid): power_box = power_box.solids()[0]
   power_box = power_box.clean()


   # ── Export STEP file to Desktop ───────────────────────────────────────────────
   import os as _os
   _desktop = _os.path.join(_os.path.expanduser("~"), "Desktop")
   _step_path = _os.path.join(_desktop, "Power Box.step")
   export_step(power_box, _step_path)
   print(f"STEP exported: {_step_path}")


   # ── Display ───────────────────────────────────────────────────────────────────
   show_object(power_box, name="Power Box", options={"color": "#5b8fa8", "alpha": 1.0})


   print("Success")
except Exception as e:
   print(f"Failure: {e}")
   