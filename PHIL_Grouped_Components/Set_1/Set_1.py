"""
Assembly: Pump Mount + Main Body
Both scripts are fully inlined. Final result shown as a named Compound.
"""

from build123d import *
from ocp_vscode import show, Camera
import math

# ╔══════════════════════════════════════════════════════════════════════════════
# PART A — PUMP MOUNT (cylinder_with_loft.py)
# ╔══════════════════════════════════════════════════════════════════════════════

big_dia     = 194.93
small_dia   = 150.0
cyl1_height = 150.0
loft_height = 100.0
cyl2_height = 450.0
hemi_dia    = 121.13

big_r   = big_dia   / 2
small_r = small_dia / 2
hemi_r  = hemi_dia  / 2

cyl1_top_z    =  cyl1_height / 2
cyl1_bottom_z = -cyl1_height / 2
loft_bottom_z  = cyl1_bottom_z - loft_height
cyl2_bottom_z  = loft_bottom_z - cyl2_height
cyl2_center_z  = loft_bottom_z - cyl2_height / 2

hole_data = [
    (-0.267,  44.303, 9.0),
    (-0.267,  19.303, 9.0),
    (18.750,   5.487, 9.0),
    (42.524,  13.209, 9.0),
    (-43.068, 13.209, 9.0),
    (-19.289,  5.487, 9.0),
    (-12.023, -16.875, 9.0),
    (11.484,  -16.875, 9.0),
    (-26.725, -37.104, 9.0),
]
hole_j         = (26.183, -37.104, 9.0)
cut_depth      = 1000.0
cut_both_depth = 1000.0

with BuildPart() as _pm_part:
    Cylinder(radius=big_r, height=cyl1_height)
    with BuildSketch(Plane.XY.offset(cyl1_bottom_z)):
        Circle(big_r)
    with BuildSketch(Plane.XY.offset(loft_bottom_z)):
        Circle(small_r)
    loft(ruled=False)
    with BuildSketch(Plane.XY.offset(cyl2_center_z)):
        Circle(small_r)
    extrude(amount=cyl2_height / 2, both=True)
    with BuildSketch(Plane.XY.offset(cyl1_top_z)):
        for cx, cy, r in hole_data:
            with Locations((cx, cy)):
                Circle(r)
    extrude(amount=cut_depth, dir=(0, 0, -1), mode=Mode.SUBTRACT)
    jx, jy, jr = hole_j
    with BuildSketch(Plane.XY.offset(cyl1_top_z)):
        with Locations((jx, jy)):
            Circle(jr)
    extrude(amount=cut_both_depth, dir=(0, 0, -1), both=True, mode=Mode.SUBTRACT)

with BuildPart() as _hemi_part:
    with Locations((0, 0, cyl1_top_z)):
        Sphere(radius=hemi_r)
    with BuildSketch(Plane.XY.offset(cyl1_top_z)):
        Rectangle(hemi_dia * 4, hemi_dia * 4)
    extrude(amount=hemi_r + 1, dir=(0, 0, -1), mode=Mode.SUBTRACT)

_rotated_hemi   = _hemi_part.part.rotate(Axis((0, 0, cyl1_top_z), (1, 0, 0)), 180)
_translated_hemi = _rotated_hemi.translate((108.62, 0, 21.37))
_hemi_copy2     = _translated_hemi.rotate(Axis.Z, 120)
_hemi_copy3     = _translated_hemi.rotate(Axis.Z, 240)

_cut_result = _pm_part.part - _translated_hemi - _hemi_copy2 - _hemi_copy3

with BuildPart() as _sphere_part:
    with Locations((0, 0, cyl1_top_z)):
        Sphere(radius=22.5)

_translated_sphere = _sphere_part.part.translate((97.7, 0, -75))
_sphere_copy2      = _translated_sphere.rotate(Axis.Z, 120)
_sphere_copy3      = _translated_sphere.rotate(Axis.Z, 240)

_cut_result = _cut_result - _translated_sphere - _sphere_copy2 - _sphere_copy3

_sphere_union1 = _translated_sphere
_sphere_union2 = _translated_sphere.rotate(Axis.Z, 120)
_sphere_union3 = _translated_sphere.rotate(Axis.Z, 240)

pump_mount = _cut_result + _sphere_union1 + _sphere_union2 + _sphere_union3

print("✓ Pump Mount built")

# ╔══════════════════════════════════════════════════════════════════════════════
# PART B — MAIN BODY (Body__.py)
# ╔══════════════════════════════════════════════════════════════════════════════

length  = 1960.94
width   =  790.00
height  = 1070.00
length2  =  40.0
width2   = 100.0
depth2   =  55.0
offset_y = 250.0
x_positions = [275.0, 735.0, 1185.94, 1644.10]

with BuildPart() as box_part:
    with BuildSketch(Plane.XY):
        with Locations((length / 2, width / 2)):
            Rectangle(length, width)
    extrude(amount=height)
    with BuildSketch(Plane.XY):
        for x0 in x_positions:
            with Locations((x0 + length2 / 2, offset_y + width2 / 2)):
                Rectangle(length2, width2)
    extrude(amount=depth2, mode=Mode.SUBTRACT)
    length3   = 1860.94
    width3    =  322.50
    height3   = 1020.00
    offset3_x =    50.0
    offset3_y =    50.0
    offset3_z =    50.0
    cut_plane = Plane.XY.offset(offset3_z)
    with BuildSketch(cut_plane):
        with Locations((offset3_x + length3 / 2, offset3_y + width3 / 2)):
            Rectangle(length3, width3)
    extrude(amount=height3, mode=Mode.SUBTRACT)

plate_l  = 1960.94
plate_h  =   640.0
plate_t  =   372.5
plate_z  =  1070.0
with BuildPart() as box_with_plate_cut:
    add(box_part.part)
    xz_plane = Plane(origin=(0, 0, plate_z), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
    with BuildSketch(xz_plane):
        with Locations((plate_l / 2, plate_h / 2)):
            Rectangle(plate_l, plate_h)
    extrude(amount=plate_t, mode=Mode.SUBTRACT)

cylinders = [(754.91, 749.96), (1205.92, 749.96)]
back_box_l  =  350.94
back_box_h  =  750.00
back_box_d  =  377.50
back_box_x  =  805.0
back_box_plane = Plane(origin=(0, 790 - 377.5, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
cyl2_r  = 321.63 / 2
hole3_r = 151.31 / 2
hole3_positions = [(754.98, 100.01), (1205.94, 100.01)]

with BuildPart() as back_box_base:
    with BuildSketch(back_box_plane):
        with Locations((back_box_x + back_box_l / 2, -(0 + back_box_h / 2))):
            Rectangle(back_box_l, back_box_h)
    extrude(amount=back_box_d)

with BuildPart() as back_box:
    add(back_box_base.part)
    for cx, cz in cylinders:
        with BuildSketch(back_box_plane):
            with Locations((cx, -cz)):
                Circle(cyl2_r)
        extrude(amount=back_box_d, both=False, mode=Mode.SUBTRACT)
    hole3_plane = Plane(origin=(0, 790, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
    with BuildSketch(hole3_plane):
        for cx, cz in hole3_positions:
            with Locations((cx, -cz)):
                Circle(hole3_r)
    extrude(amount=-back_box_d, both=False, mode=Mode.SUBTRACT)

cyl_r       = 1430.91 / 2
cyl_depth   =  376.5
back_y      =  790.0
back_plane  = Plane(origin=(0, back_y - 367.5, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
ring_y      = back_y - 367.5 - 10
ring_plane  = Plane(origin=(0, ring_y, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
disc_plane  = Plane(origin=(0, ring_y + 10, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
hollow_depth = 377.5
outer_r2 = 470.0 / 2
inner_r2 = 260.0 / 2

with BuildPart() as after_disc_cuts:
    add(box_with_plate_cut.part)
    for cx, cz in cylinders:
        with BuildSketch(back_plane):
            with Locations((cx, -cz)):
                Circle(cyl_r)
        extrude(amount=cyl_depth, mode=Mode.SUBTRACT)
    for cx, cz in cylinders:
        with BuildSketch(ring_plane):
            with Locations((cx, -cz)):
                Circle(outer_r2)
                Circle(inner_r2, mode=Mode.SUBTRACT)
        extrude(amount=hollow_depth, both=False, mode=Mode.SUBTRACT)
    for cx, cz in cylinders:
        with BuildSketch(disc_plane):
            with Locations((cx, -cz)):
                Circle(cyl_r)
        extrude(amount=hollow_depth, both=False, mode=Mode.SUBTRACT)

rect_l  = 1500.0
rect_w  =  400.0
rect_h  =  400.0
top_z   = 1070.0
rect_cx = length / 2
rect_cy = width  / 2

with BuildPart() as after_rect_cut:
    add(after_disc_cuts.part)
    with BuildSketch(Plane.XY.offset(top_z)):
        with Locations((rect_cx, rect_cy)):
            Rectangle(rect_l, rect_w)
    extrude(amount=rect_h, mode=Mode.SUBTRACT)

arc_outer_r  = 1333.63 / 2
arc_inner_r  = 1273.85 / 2
arc_thickness = 10.0
arc_degrees  = 187.0
SK_START = 270.0
SK_END   = 270.0 - arc_degrees

def make_arc_pts(cx, cz, r, a_start, a_end):
    a_mid = (a_start + a_end) / 2
    return (
        Vector(cx + r * math.cos(math.radians(a_start)), -cz + r * math.sin(math.radians(a_start))),
        Vector(cx + r * math.cos(math.radians(a_mid)),   -cz + r * math.sin(math.radians(a_mid))),
        Vector(cx + r * math.cos(math.radians(a_end)),   -cz + r * math.sin(math.radians(a_end))),
    )

cx1, cz1 = cylinders[0]
p1o, p2o, p3o = make_arc_pts(cx1, cz1, arc_outer_r, SK_START, SK_END)
p1i, p2i, p3i = make_arc_pts(cx1, cz1, arc_inner_r, SK_END, SK_START)
with BuildPart() as arc_ring_c1:
    with BuildSketch(ring_plane):
        with BuildLine():
            ThreePointArc(p1o, p2o, p3o)
            Line(p3o, p1i)
            ThreePointArc(p1i, p2i, p3i)
            Line(p3i, p1o)
        make_face()
    extrude(amount=arc_thickness, both=False)

cx2, cz2 = cylinders[1]
p1o, p2o, p3o = make_arc_pts(cx2, cz2, arc_outer_r, SK_START, SK_START + arc_degrees)
p1i, p2i, p3i = make_arc_pts(cx2, cz2, arc_inner_r, SK_START + arc_degrees, SK_START)
with BuildPart() as arc_ring_c2:
    with BuildSketch(ring_plane):
        with BuildLine():
            ThreePointArc(p1o, p2o, p3o)
            Line(p3o, p1i)
            ThreePointArc(p1i, p2i, p3i)
            Line(p3i, p1o)
        make_face()
    extrude(amount=arc_thickness, both=False)

with BuildPart() as final_body:
    add(after_rect_cut.part)
    add(back_box.part)
    add(arc_ring_c1.part, mode=Mode.SUBTRACT)
    add(arc_ring_c2.part, mode=Mode.SUBTRACT)

new_cyl_r     = 151.31 / 2
new_cyl_depth = 367.5
new_cyl_plane = Plane(origin=(0, 790 - 367.5, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))

with BuildPart() as final_body2:
    add(final_body.part)
    with BuildSketch(new_cyl_plane):
        with Locations((754.98, -100.0)):
            Circle(new_cyl_r)
    extrude(amount=new_cyl_depth, both=False, mode=Mode.SUBTRACT)
    with BuildSketch(new_cyl_plane):
        with Locations((1205.94, -100.0)):
            Circle(new_cyl_r)
    extrude(amount=new_cyl_depth, both=False, mode=Mode.SUBTRACT)

holes_240 = [(754.99, 750.02), (1205.94, 750.02)]
holes_173 = [(295.9,  750.02), (1665.03, 750.02)]

with BuildPart() as final_body3:
    add(final_body2.part)
    with BuildSketch(Plane.XZ.offset(0)):
        for cx, cz in holes_240:
            with Locations((cx, cz)):
                Circle(240.0 / 2)
        for cx, cz in holes_173:
            with Locations((cx, cz)):
                Circle(173.85 / 2)
    extrude(amount=-width, both=False, mode=Mode.SUBTRACT)

holes_35 = [(1910.94, 480.01), (1910.94, 1020.0), (50.0, 480.01), (50.0, 1020.0)]

with BuildPart() as final_body4:
    add(final_body3.part)
    with BuildSketch(Plane.XZ.offset(0)):
        for cx, cz in holes_35:
            with Locations((cx, cz)):
                Circle(35.0 / 2)
    extrude(amount=-width, both=False, mode=Mode.SUBTRACT)

profile_pts = [
    Vector(0, 0),
    Vector(50, 0),
    Vector(78.75, 16.6),
    Vector(78.75, 49.8),
    Vector(50, 66.4),
    Vector(0, 66.4),
]

plane1  = Plane(origin=(1013.67, 725, 700),   x_dir=(0, 0, -1), z_dir=(0, 1, 0))
plane2  = Plane(origin=(0,       725, 513.2),  x_dir=(1, 0, 0),  z_dir=(0, 1, 0))
plane3  = Plane(origin=(366.8,   725, 0),      x_dir=(0, 0, 1),  z_dir=(0, 1, 0))
plane1m = Plane(origin=(1960.94, 725, 1053.2), x_dir=(-1, 0, 0), z_dir=(0, 1, 0))
plane2m = Plane(origin=(1960.94, 725, 513.2),  x_dir=(-1, 0, 0), z_dir=(0, 1, 0))
plane3m = Plane(origin=(1594.14, 725, 0),      x_dir=(0, 0, -1), z_dir=(0, 1, 0))
profile_pts_m12 = [Vector(p.X, -p.Y) for p in profile_pts]
profile_pts_m3  = [Vector(p.X, -p.Y) for p in profile_pts]

with BuildPart() as final_body5:
    add(final_body4.part)
    for plane in [plane1, plane2, plane3]:
        with BuildSketch(plane):
            with BuildLine():
                Polyline(*profile_pts, close=True)
            make_face()
        extrude(amount=25, mode=Mode.SUBTRACT)
    for plane in [plane1m, plane2m]:
        with BuildSketch(plane):
            with BuildLine():
                Polyline(*profile_pts_m12, close=True)
            make_face()
        extrude(amount=25, mode=Mode.SUBTRACT)
    plane3_copy = Plane(origin=(1527.73, 725, 0), x_dir=(0, 0, 1), z_dir=(0, 1, 0))
    with BuildSketch(plane3_copy):
        with BuildLine():
            Polyline(*profile_pts, close=True)
        make_face()
    extrude(amount=25, mode=Mode.SUBTRACT)

back_holes = [(854.99, 219.5), (1105.94, 219.5), (980.47, 650.0)]
back_hole_plane = Plane(origin=(0, 790, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))

with BuildPart() as final_body6:
    add(final_body5.part)
    with BuildSketch(back_hole_plane):
        for cx, cz in back_holes:
            with Locations((cx, -cz)):
                Circle(35.0 / 2)
    extrude(amount=-127.5, both=False, mode=Mode.SUBTRACT)

with BuildPart() as final_body7:
    add(final_body6.part)
    with BuildSketch(plane1):
        with BuildLine():
            Polyline(*profile_pts, close=True)
        make_face()
    extrude(amount=25, mode=Mode.SUBTRACT)

with BuildPart() as final_body8:
    add(final_body7.part)
    box_plane = Plane(origin=(906.95, 790, 800), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
    with BuildSketch(box_plane):
        with Locations((146.99 / 2, 100.0 / 2)):
            Rectangle(146.99, 100.0)
    extrude(amount=-377.5, mode=Mode.SUBTRACT)

with BuildPart() as final_body9:
    add(final_body8.part)
    with BuildSketch(Plane(origin=(805, 725, 252.7), x_dir=(1, 0, 0), z_dir=(0, 1, 0))):
        with BuildLine():
            Polyline(*profile_pts, close=True)
        make_face()
    extrude(amount=25, mode=Mode.SUBTRACT)
    with BuildSketch(Plane(origin=(805 + 350.94, 725, 252.7 - 66.4), x_dir=(-1, 0, 0), z_dir=(0, 1, 0))):
        with BuildLine():
            Polyline(*profile_pts, close=True)
        make_face()
    extrude(amount=25, mode=Mode.SUBTRACT)

with BuildPart() as final_body10:
    add(final_body9.part)
    with BuildSketch(Plane.XY):
        with Locations((980.64, 595)):
            Circle(157.02 / 2)
    extrude(amount=700, mode=Mode.SUBTRACT)

with BuildPart() as final_body11:
    add(final_body10.part)
    with BuildSketch(Plane.XY):
        with Locations((980.64, 595)):
            Circle(244.07 / 2)
    extrude(amount=150, mode=Mode.SUBTRACT)

chamfer_h     = 37.0
chamfer_slant = 42.0
chamfer_w     = math.sqrt(chamfer_slant**2 - chamfer_h**2)
hole_r        = 244.07 / 2

with BuildPart() as final_body12:
    add(final_body11.part)
    with BuildSketch(Plane(origin=(980.64, 595, chamfer_h), x_dir=(1, 0, 0), z_dir=(0, 1, 0))):
        with BuildLine():
            Polyline(Vector(hole_r, 0), Vector(hole_r + chamfer_w, chamfer_h), Vector(hole_r, chamfer_h), close=True)
        make_face()
    revolve(axis=Axis((980.64, 595, 0), (0, 0, 1)), revolution_arc=360, mode=Mode.SUBTRACT)

chamfer2_h       = 85.0
chamfer2_r_start = 244.07 / 2
chamfer2_r_end   = 157.02 / 2

with BuildPart() as final_body13:
    add(final_body12.part)
    with BuildSketch(Plane(origin=(980.64, 595, 235), x_dir=(1, 0, 0), z_dir=(0, 1, 0))):
        with BuildLine():
            Polyline(Vector(chamfer2_r_end, 0), Vector(chamfer2_r_start, chamfer2_h), Vector(chamfer2_r_end, chamfer2_h), close=True)
        make_face()
    revolve(axis=Axis((980.64, 595, 0), (0, 0, 1)), revolution_arc=360, mode=Mode.SUBTRACT)

with BuildPart() as cyl_body:
    with BuildSketch(Plane.XY):
        with Locations((980.64, 595)):
            Circle(47.0 / 2)
    extrude(amount=98.5)
    slant_plane = Plane(origin=(980.64, 595, 75), x_dir=(0, 1, 0), z_dir=(math.sqrt(2)/2, 0, math.sqrt(2)/2))
    with BuildSketch(slant_plane):
        Rectangle(500, 500)
    extrude(amount=150, mode=Mode.SUBTRACT)

R_arc  = 122.0
arc_cx = 980.64
arc_cy = 595.0 + R_arc
arc_z  = 75.0
arc_mid_x = arc_cx + R_arc * math.cos(math.radians(307.5))
arc_mid_y = arc_cy + R_arc * math.sin(math.radians(307.5))
arc_end_x = arc_cx + R_arc * math.cos(math.radians(345.0))
arc_end_y = arc_cy + R_arc * math.sin(math.radians(345.0))
rev_end_x = arc_cx + R_arc * math.cos(math.radians(195.0))
rev_end_y = arc_cy + R_arc * math.sin(math.radians(195.0))
rev_mid_x = arc_cx + R_arc * math.cos(math.radians(232.5))
rev_mid_y = arc_cy + R_arc * math.sin(math.radians(232.5))
rev_tan_x = -math.sin(math.radians(195))
rev_tan_y =  math.cos(math.radians(195))

with BuildLine() as arc_path:
    ThreePointArc((rev_end_x, rev_end_y, arc_z), (rev_mid_x, rev_mid_y, arc_z), (980.64, 595, arc_z))
    ThreePointArc((980.64, 595, arc_z), (arc_mid_x, arc_mid_y, arc_z), (arc_end_x, arc_end_y, arc_z))

with BuildPart() as arc_cyl_body:
    with BuildSketch(Plane(origin=(rev_end_x, rev_end_y, arc_z), x_dir=(0, 0, 1), z_dir=(rev_tan_x, rev_tan_y, 0))):
        Circle(47.0 / 2)
    sweep(path=arc_path)
    with BuildSketch(slant_plane):
        Rectangle(500, 500)
    extrude(amount=-150, mode=Mode.SUBTRACT)
    fillet(arc_cyl_body.edges().filter_by(GeomType.CIRCLE).sort_by(SortBy.LENGTH)[0:1], radius=20)

with BuildPart() as joined_cyl:
    add(cyl_body.part)
    add(arc_cyl_body.part)

cyl_cx = 980.64 + 50.07
cyl_cy = 595.0  - 101.0
hole_cx, hole_cy = 980.64, 595.0
_dx = cyl_cx - hole_cx
_dy = cyl_cy - hole_cy

with BuildPart() as joined_cyl_moved:
    add(joined_cyl.part.moved(Location((50.07, -101, 0))))

with BuildPart() as joined_cyl_rotated:
    add(joined_cyl_moved.part.moved(
        Location((cyl_cx, cyl_cy, 0)) * Rotation(0, 0, 30) * Location((-cyl_cx, -cyl_cy, 0))
    ))

c120_x = hole_cx + _dx*math.cos(math.radians(120)) - _dy*math.sin(math.radians(120))
c120_y = hole_cy + _dx*math.sin(math.radians(120)) + _dy*math.cos(math.radians(120))
c240_x = hole_cx + _dx*math.cos(math.radians(240)) - _dy*math.sin(math.radians(240))
c240_y = hole_cy + _dx*math.sin(math.radians(240)) + _dy*math.cos(math.radians(240))

with BuildPart() as cyl_replica_120:
    add(joined_cyl_rotated.part.moved(
        Location((c120_x, c120_y, 0)) * Rotation(0, 0, 1) * Location((-c120_x, -c120_y, 0)) *
        Location((hole_cx, hole_cy, 0)) * Rotation(0, 0, 120) * Location((-hole_cx, -hole_cy, 0))
    ))

with BuildPart() as cyl_replica_240:
    add(joined_cyl_rotated.part.moved(
        Location((c240_x, c240_y, 0)) * Rotation(0, 0, 1) * Location((-c240_x, -c240_y, 0)) *
        Location((hole_cx, hole_cy, 0)) * Rotation(0, 0, 240) * Location((-hole_cx, -hole_cy, 0))
    ))

with BuildPart() as final_body14:
    add(final_body13.part)
    add(joined_cyl_rotated.part,  mode=Mode.SUBTRACT)
    add(cyl_replica_120.part,     mode=Mode.SUBTRACT)
    add(cyl_replica_240.part,     mode=Mode.SUBTRACT)

plane_left_top       = Plane(origin=(0,       725,         1053.2),        x_dir=( 1, 0, 0), z_dir=(0, 1, 0))
plane_left_top_copy  = Plane(origin=(0,       725 - 302.5, 1053.2),        x_dir=( 1, 0, 0), z_dir=(0, 1, 0))
plane_right_top      = Plane(origin=(1960.94, 725,         1053.2),        x_dir=(-1, 0, 0), z_dir=(0, 1, 0))
plane_right_top_copy = Plane(origin=(1960.94, 725 - 302.5, 1053.2),        x_dir=(-1, 0, 0), z_dir=(0, 1, 0))
plane_left_mid       = Plane(origin=(0,       725,         1053.2 - 540),  x_dir=( 1, 0, 0), z_dir=(0, 1, 0))
plane_left_mid_copy  = Plane(origin=(0,       725 - 302.5, 1053.2 - 540),  x_dir=( 1, 0, 0), z_dir=(0, 1, 0))
plane_right_mid      = Plane(origin=(1960.94, 725,         1053.2 - 540),  x_dir=(-1, 0, 0), z_dir=(0, 1, 0))
plane_right_mid_copy = Plane(origin=(1960.94, 725 - 302.5, 1053.2 - 540),  x_dir=(-1, 0, 0), z_dir=(0, 1, 0))

with BuildPart() as final_body15:
    add(final_body14.part)
    for plane in [plane_left_top, plane_left_top_copy, plane_left_mid, plane_left_mid_copy]:
        with BuildSketch(plane):
            with BuildLine():
                Polyline(*profile_pts, close=True)
            make_face()
        extrude(amount=25, mode=Mode.SUBTRACT)
    for plane in [plane_right_top, plane_right_top_copy, plane_right_mid, plane_right_mid_copy]:
        with BuildSketch(plane):
            with BuildLine():
                Polyline(*profile_pts_m12, close=True)
            make_face()
        extrude(amount=25, mode=Mode.SUBTRACT)

with BuildPart() as profile_body:
    with BuildSketch(Plane.XY.offset(1020)):
        with BuildLine():
            Polyline(*profile_pts, close=True)
        make_face()
    extrude(amount=25)

with BuildPart() as profile_body_moved:
    add(profile_body.part.moved(Location((0, 501.82, 0))))

with BuildPart() as profile_body_copy:
    add(profile_body.part.moved(Location((0, 501.82 + 105, 0))))

profile_pts_mirror = [Vector(1960.94 - p.X, p.Y) for p in profile_pts]

with BuildPart() as profile_body_right:
    with BuildSketch(Plane.XY.offset(1020)):
        with BuildLine():
            Polyline(*profile_pts_mirror, close=True)
        make_face()
    extrude(amount=25)

with BuildPart() as profile_body_right_moved:
    add(profile_body_right.part.moved(Location((0, 501.82, 0))))

with BuildPart() as profile_body_right_copy:
    add(profile_body_right.part.moved(Location((0, 501.82 + 105, 0))))

with BuildPart() as final_body16:
    add(final_body15.part)
    add(profile_body_moved.part,       mode=Mode.SUBTRACT)
    add(profile_body_copy.part,        mode=Mode.SUBTRACT)
    add(profile_body_right_moved.part, mode=Mode.SUBTRACT)
    add(profile_body_right_copy.part,  mode=Mode.SUBTRACT)

with BuildPart() as final_body17:
    add(final_body16.part)
    with BuildSketch(Plane.XY.offset(1070)):
        with Locations((50, 535), (50, 640), (1910.94, 535), (1910.94, 640)):
            Circle(35.0 / 2)
    extrude(amount=-24, mode=Mode.SUBTRACT)

with BuildPart() as box_top_raw:
    Box(38, 367.5, 40, align=(Align.MIN, Align.MIN, Align.MIN))

with BuildPart() as box_top:
    add(box_top_raw.part.moved(Location((100, 422.5, 1032))))

with BuildPart() as box_top_mirror:
    add(box_top_raw.part.moved(Location((1960.94 - 100 - 38, 422.5, 1032))))

with BuildPart() as final_body18:
    add(final_body17.part)
    add(box_top.part,        mode=Mode.SUBTRACT)
    add(box_top_mirror.part, mode=Mode.SUBTRACT)

front_hole_plane = Plane(origin=(0, 0, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
front_holes = [(294.98, 425), (754.98, 425), (1205.96, 425), (1664.10, 425)]

with BuildPart() as final_body19:
    add(final_body18.part)
    with BuildSketch(front_hole_plane):
        for cx, cz in front_holes:
            with Locations((cx, -cz)):
                Circle(100.0 / 2)
    extrude(amount=55, mode=Mode.SUBTRACT)

text_plane = Plane(origin=(50, 0, 200), x_dir=(1, 0, 0), z_dir=(0, -1, 0))

with BuildPart() as final_body20:
    add(final_body19.part)
    def spaced(txt): return " ".join(txt)
    with BuildSketch(text_plane):
        with Locations((0, 103.359375)):
            Text(spaced("Designed by Philip Dettinger"), font_size=69.3,
                 text_align=(TextAlign.LEFT, TextAlign.CENTER))
        with Locations((0, 0)):
            Text(spaced("Cell System Dyanmics Group"), font_size=69.3,
                 text_align=(TextAlign.LEFT, TextAlign.CENTER))
        with Locations((0, -103.359375)):
            Text(spaced("ETH Zurich"), font_size=69.3,
                 text_align=(TextAlign.LEFT, TextAlign.CENTER))
    extrude(amount=-6, mode=Mode.SUBTRACT)

back_text_plane = Plane(origin=(1460.96, 422.5, 750), x_dir=(0, 0, 1), z_dir=(0, 1, 0))

with BuildPart() as right_text_body:
    with BuildSketch(back_text_plane):
        Text("RIGHT", font_size=69.3, text_align=(TextAlign.LEFT, TextAlign.BOTTOM))
    extrude(amount=-3)

left_text_plane = Plane(origin=(449.96, 422.5, 750), x_dir=(0, 0, 1), z_dir=(0, 1, 0))

with BuildPart() as left_text_body:
    with BuildSketch(left_text_plane):
        Text("LEFT", font_size=69.3, text_align=(TextAlign.LEFT, TextAlign.BOTTOM))
    extrude(amount=-3)

with BuildPart() as final_body21:
    add(final_body20.part)
    add(right_text_body.part, mode=Mode.SUBTRACT)
    add(left_text_body.part,  mode=Mode.SUBTRACT)

main_body = final_body21.part

print("✓ Main Body built")

# ╔══════════════════════════════════════════════════════════════════════════════
# ASSEMBLY — position pump mount on top of main body
# ╔══════════════════════════════════════════════════════════════════════════════
# Pump mount: bottom at Z=-625, centred at origin.
# Place it over the 244.07mm hole at (980.64, 595) on body top face (Z=1070).
# Translate so pump bottom (Z=-625) sits at body top (Z=1070).

pump_offset_x = 980.64
pump_offset_y = 595.0
pump_offset_z = 1070.0 - (-625.0)   # = 1695.0

positioned_pump = pump_mount.translate((pump_offset_x, pump_offset_y + 524.71, pump_offset_z - 1070))




# ╔══════════════════════════════════════════════════════════════════════════════
# PART C — BODY TOP (Body_Top.py)
# ╔══════════════════════════════════════════════════════════════════════════════

_LENGTH    = 1960.94
_WIDTH     =  640.00
_HEIGHT    =  372.50
_T         =   50.00

_CUT1_LEN  =  940.94
_CUT1_WID  =  540.00
_CUT2_LEN  =  650.94
_CUT2_WID  =   50.00
_SLOT_W    =  100.04
_SLOT_RH   =  126.26
_SLOT_R    = _SLOT_W / 2
_SLOT_TOT  = _SLOT_RH + _SLOT_W
_SLOT_DEP  =   50.00
_TAB_X     =  60.00
_TAB_Y     = 140.00
_TAB_Z     =  50.00
_tab_ox    =  45.00
_tab_oy    = 225.00
_tab_oz    = _HEIGHT - _TAB_Z
_HOLE_D    = 233.47
_HOLE_R    = _HOLE_D / 2
_HOLE_CX   = 294.99
_HOLE_CY   = 320.38
_cx        = _LENGTH / 2
_cy        = _WIDTH  / 2
_cut1_x    = _cx - _CUT1_LEN / 2
_cut1_y    = _cy - _CUT1_WID / 2
_cut2_x    = _cx - _CUT2_LEN / 2
_cut2_y    = 0
_slot_r_cx = _LENGTH - 754.98
_slot_cz   = _HEIGHT / 2

with BuildPart() as _slot_build_bt:
    with BuildSketch(Plane.XY) as _sk_bt:
        SlotOverall(width=_SLOT_TOT, height=_SLOT_W)
    extrude(_sk_bt.sketch, amount=_SLOT_DEP)

_slot_right = (
    _slot_build_bt.part
    .rotate(Axis.Z, 90)
    .rotate(Axis.X, -90)
    .translate(Vector(_slot_r_cx, _WIDTH - _SLOT_DEP, _slot_cz))
)
_mirror_plane_slot = Plane(origin=(_LENGTH / 2, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
_slot_left = _slot_right.mirror(_mirror_plane_slot)

_H4_D = 35.00
_H4_R = _H4_D / 2
_H4_CENTRES = [
    (140.00, 165.39),
    (449.99, 165.39),
    (140.00, 475.37),
    (449.99, 475.37),
]

with BuildPart() as _bt_part:
    Box(_LENGTH, _WIDTH, _HEIGHT, align=(Align.MIN, Align.MIN, Align.MIN))

    with Locations((0, _T, 0)):
        Box(_LENGTH, _WIDTH - 2*_T, _HEIGHT - _T,
            align=(Align.MIN, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)

    with Locations((_cut1_x, _cut1_y, 0)):
        Box(_CUT1_LEN, _CUT1_WID, _HEIGHT,
            align=(Align.MIN, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)

    with Locations((_cut2_x, _cut2_y, 0)):
        Box(_CUT2_LEN, _CUT2_WID, _HEIGHT,
            align=(Align.MIN, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)

    add(_slot_right, mode=Mode.SUBTRACT)
    add(_slot_left,  mode=Mode.SUBTRACT)

    with Locations((_tab_ox, _tab_oy, _tab_oz)):
        Box(_TAB_X, _TAB_Y, _TAB_Z,
            align=(Align.MIN, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)

    with BuildSketch(Plane(origin=(_HOLE_CX, _HOLE_CY, _HEIGHT),
                           x_dir=(1,0,0), z_dir=(0,0,1))) as _hole_sk:
        Circle(_HOLE_R)
    extrude(_hole_sk.sketch, amount=-_T, mode=Mode.SUBTRACT)

    with BuildSketch(Plane(origin=(_HOLE_CX, _HOLE_CY, _HEIGHT - _T + 23.5),
                           x_dir=(1,0,0), z_dir=(0,0,1))) as _cb_sk:
        Circle(185.0)
    extrude(_cb_sk.sketch, amount=-23.5, mode=Mode.SUBTRACT)

    with BuildSketch(Plane(origin=(_LENGTH - _HOLE_CX, _HOLE_CY, _HEIGHT - _T + 23.5),
                           x_dir=(1,0,0), z_dir=(0,0,1))) as _cb_m_sk:
        Circle(185.0)
    extrude(_cb_m_sk.sketch, amount=-23.5, mode=Mode.SUBTRACT)

    for _hx, _hy in _H4_CENTRES:
        with BuildSketch(Plane(origin=(_hx, _hy, _HEIGHT),
                               x_dir=(1,0,0), z_dir=(0,0,1))) as _h4_sk:
            Circle(_H4_R)
        extrude(_h4_sk.sketch, amount=-_T, mode=Mode.SUBTRACT)

    _H4_SIDE = 24.0 / 2**0.5
    _z_top   = _HEIGHT - _T + 17
    for _hx, _hy in _H4_CENTRES:
        with BuildSketch(Plane(origin=(_hx, _hy, 0),
                               x_dir=(1,0,0), z_dir=(0,0,1))) as _cs_sk:
            with BuildLine():
                Line((_H4_R, _z_top), (_H4_R + _H4_SIDE, _z_top))
                Line((_H4_R + _H4_SIDE, _z_top), (_H4_R, _z_top - _H4_SIDE))
                Line((_H4_R, _z_top - _H4_SIDE), (_H4_R, _z_top))
            make_face()
        revolve(_cs_sk.sketch, axis=Axis((_hx, _hy, 0), (0,0,1)),
                revolution_arc=360, mode=Mode.SUBTRACT)

    _tab_mx = _LENGTH - _tab_ox - _TAB_X
    with Locations((_tab_mx, _tab_oy, _tab_oz)):
        Box(_TAB_X, _TAB_Y, _TAB_Z,
            align=(Align.MIN, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)

    _hole_mx = _LENGTH - _HOLE_CX
    with BuildSketch(Plane(origin=(_hole_mx, _HOLE_CY, _HEIGHT),
                           x_dir=(1,0,0), z_dir=(0,0,1))) as _hole_m_sk:
        Circle(_HOLE_R)
    extrude(_hole_m_sk.sketch, amount=-_T, mode=Mode.SUBTRACT)

    for _hx, _hy in _H4_CENTRES:
        _hx_m = _LENGTH - _hx
        with BuildSketch(Plane(origin=(_hx_m, _hy, _HEIGHT),
                               x_dir=(1,0,0), z_dir=(0,0,1))) as _h4m_sk:
            Circle(_H4_R)
        extrude(_h4m_sk.sketch, amount=-_T, mode=Mode.SUBTRACT)

# Corner post (Body 2)
_POST_X = 100.00
_POST_Y =  50.00
_POST_Z = 322.50

with BuildPart() as _body2_bt:
    with BuildSketch(Plane.XY) as _post_sk:
        with BuildLine():
            Line((0, 50), (100, 50))
            RadiusArc((100, 50), (50, 100), radius=-50)
            Line((50, 100), (0, 100))
            Line((0, 100), (0, 50))
        make_face()
    extrude(_post_sk.sketch, amount=_POST_Z)

_mirror_plane_x_bt = Plane(origin=(_LENGTH/2, 0, 0), x_dir=(0,1,0), z_dir=(1,0,0))
_mirror_plane_y_bt = Plane(origin=(0, _WIDTH/2, 0), x_dir=(1,0,0), z_dir=(0,1,0))
_body2_right  = _body2_bt.part.mirror(_mirror_plane_x_bt)
_body2_back_l = _body2_bt.part.mirror(_mirror_plane_y_bt)
_body2_back_r = _body2_right.mirror(_mirror_plane_y_bt)

_hl_x = 49.98;          _hl_y = 49.99
_hr_x = _LENGTH - 49.98; _hr_y = 49.99
_bl_x = 49.98;           _bl_y = _WIDTH - 49.99
_br_x = _LENGTH - 49.98; _br_y = _WIDTH - 49.99

with _bt_part:
    add(_body2_bt.part,   mode=Mode.ADD)
    add(_body2_right,     mode=Mode.ADD)
    add(_body2_back_l,    mode=Mode.ADD)
    add(_body2_back_r,    mode=Mode.ADD)

    for _hx, _hy in [(_hl_x,_hl_y),(_hr_x,_hr_y),(_bl_x,_bl_y),(_br_x,_br_y)]:
        with BuildSketch(Plane(origin=(_hx, _hy, _HEIGHT),
                               x_dir=(1,0,0), z_dir=(0,0,1))) as _dh_sk:
            Circle(35.0)
        extrude(_dh_sk.sketch, amount=-322.5, mode=Mode.SUBTRACT)

    for _hx, _hy in [(_hl_x,_hl_y),(_hr_x,_hr_y),(_bl_x,_bl_y),(_br_x,_br_y)]:
        with BuildSketch(Plane(origin=(_hx, _hy, _HEIGHT),
                               x_dir=(1,0,0), z_dir=(0,0,1))) as _sh_sk:
            Circle(17.5)
        extrude(_sh_sk.sketch, amount=-_HEIGHT, mode=Mode.SUBTRACT)

_TOP_SLANT = 24.0
_TOP_SIDE  = _TOP_SLANT / 2**0.5

with _bt_part:
    for _hx, _hy in [(140.00,165.39),(449.99,165.39),(140.00,475.37),(449.99,475.37)]:
        with Locations((_hx, _hy, _HEIGHT - _TOP_SIDE - 50 + 16.9)):
            Cone(bottom_radius=_H4_R + _TOP_SIDE, top_radius=_H4_R,
                 height=_TOP_SIDE,
                 align=(Align.CENTER, Align.CENTER, Align.MIN),
                 mode=Mode.SUBTRACT)
    for _hx, _hy in [(140.00,165.39),(449.99,165.39),(140.00,475.37),(449.99,475.37)]:
        with Locations((_LENGTH - _hx, _hy, _HEIGHT - _TOP_SIDE - 50 + 16.9)):
            Cone(bottom_radius=_H4_R + _TOP_SIDE, top_radius=_H4_R,
                 height=_TOP_SIDE,
                 align=(Align.CENTER, Align.CENTER, Align.MIN),
                 mode=Mode.SUBTRACT)

with _bt_part:
    with BuildSketch(Plane(origin=(0, 325, 347.5),
                           x_dir=(0,1,0), z_dir=(1,0,0))) as _lh_sk:
        Circle(7.5)
    extrude(_lh_sk.sketch, amount=55, mode=Mode.SUBTRACT)

    with BuildSketch(Plane(origin=(0, 256.02, 347.5),
                           x_dir=(0,1,0), z_dir=(1,0,0))) as _lh2_sk:
        Circle(7.5)
    extrude(_lh2_sk.sketch, amount=55, mode=Mode.SUBTRACT)

    for _rcy in [325, 256.02]:
        with BuildSketch(Plane(origin=(_LENGTH, _rcy, 347.5),
                               x_dir=(0,1,0), z_dir=(-1,0,0))) as _rh_sk:
            Circle(7.5)
        extrude(_rh_sk.sketch, amount=55, mode=Mode.SUBTRACT)

with _bt_part:
    with BuildSketch(Plane(origin=(319.32, 525.26, _HEIGHT),
                           x_dir=(1,0,0), z_dir=(0,0,1))) as _txt_sk:
        Text('Z1', font_size=100, font='Arial', font_style=FontStyle.BOLD,
             text_align=(TextAlign.CENTER, TextAlign.CENTER))
    extrude(_txt_sk.sketch, amount=-10, mode=Mode.SUBTRACT)

    with BuildSketch(Plane(origin=(_LENGTH - 319.32, 525.26, _HEIGHT),
                           x_dir=(1,0,0), z_dir=(0,0,1))) as _txt2_sk:
        Text('Z2', font_size=100, font='Arial', font_style=FontStyle.BOLD,
             text_align=(TextAlign.CENTER, TextAlign.CENTER))
    extrude(_txt2_sk.sketch, amount=-10, mode=Mode.SUBTRACT)

body_top = _bt_part.part

print("✓ Body Top built")

# ╔══════════════════════════════════════════════════════════════════════════════
# ASSEMBLY — Main Body + Pump Mount + Body Top
# ╔══════════════════════════════════════════════════════════════════════════════

pump_offset_x = 980.64
pump_offset_y = 595.0
pump_offset_z = 1070.0 - (-625.0)   # 1695.0
positioned_pump = pump_mount.translate((pump_offset_x, pump_offset_y + 524.71, pump_offset_z - 1070))

# Body Top sits on top of Main Body (Main Body top face = Z=1070)
# Body Top bottom face is at Z=0, so translate it up by 1070
# Rotate Body Top 180° about X-axis through its own centre, then translate
_bt_cx = _LENGTH / 2   # 980.47
_bt_cy = _WIDTH  / 2   # 320.0
_bt_cz = _HEIGHT / 2   # 186.25
body_top_rotated    = body_top.rotate(Axis((_bt_cx, _bt_cy, _bt_cz), (1, 0, 0)), 180)
body_top_positioned = body_top_rotated.translate((0, 795, 0))

# ╔══════════════════════════════════════════════════════════════════════════════
# PART D — ELBOW LEFT (Elbow_left.py)
# ╔══════════════════════════════════════════════════════════════════════════════
import math as _math
import math as _math2
import math as _math3
import math as _math4
import math as _math5
import math as _math6
import math as _math7


# Profile points at Z=60, extruded 100mm upward (Z=60 to Z=160)
# Offset so that point (-10.4688, -17.8125) moves to origin (0, 0)
x_offset = 10.4688
y_offset = 17.8125

raw_pts = [
    (-10.4688, 117.832), (-10.4688, -17.8125), (-14.2578, -22.8125),
    (-18.2812, -27.5977), (-22.5781, -32.168), (-27.1094, -36.4844),
    (-31.8359, -40.5664), (-36.7969, -44.3945), (-41.9531, -47.9297),
    (-47.3047, -51.1914), (-52.8125, -54.1797), (-58.4766, -56.8359),
    (-64.2969, -59.2188), (-70.1953, -61.2695), (-76.2109, -62.9883),
    (-82.3047, -64.3945), (-88.4766, -65.4688), (-94.6875, -66.2305),
    (-100.9375, -66.6406), (-107.2266, -66.6992), (-113.4766, -66.4453),
    (-119.6875, -65.8398), (-125.8984, -64.9219), (-132.0312, -63.6523),
    (-138.0859, -62.0703), (-144.0625, -60.1562), (-149.8828, -57.9297),
    (-155.625, -55.3906), (-161.2109, -52.5586), (-166.6406, -49.4141),
    (-171.875, -45.9961), (-176.9141, -42.3047), (-181.7578, -38.3398),
    (-186.4062, -34.1211), (-190.7812, -29.6484), (-194.9219, -24.9609),
    (-198.8281, -20.0586), (-202.4609, -14.9414), (-205.7812, -9.6484),
    (-208.8672, -4.1992), (-211.6016, 1.4258), (-214.0625, 7.1875),
    (-216.2109, 13.0859), (-218.0078, 19.0625), (-219.5312, 25.1562),
    (-220.7031, 31.3086), (-221.5234, 37.5), (-222.0312, 43.75),
    (-222.1875, 50.0), (-222.0312, 56.2695), (-221.5234, 62.5),
    (-220.7031, 68.7109), (-219.5312, 74.8633), (-218.0078, 80.9375),
    (-216.2109, 86.9336), (-214.0625, 92.8125), (-211.6016, 98.5742),
    (-208.8672, 104.1992), (-205.7812, 109.668), (-202.4609, 114.9609),
    (-198.8281, 120.0781), (-194.9219, 124.9805), (-190.7812, 129.668),
    (-186.4062, 134.1211), (-181.7578, 138.3398), (-176.9141, 142.3047),
    (-171.875, 146.0156), (-166.6406, 149.4336), (-161.2109, 152.5586),
    (-155.625, 155.4102), (-149.8828, 157.9492), (-144.0625, 160.1758),
    (-138.0859, 162.0898), (-132.0312, 163.6719), (-125.8984, 164.9414),
    (-119.6875, 165.8594), (-113.4766, 166.4648), (-107.2266, 166.7188),
    (-100.9375, 166.6406), (-94.6875, 166.2305), (-88.4766, 165.4883),
    (-82.3047, 164.4141), (-76.2109, 163.0078), (-70.1953, 161.2695),
    (-64.2969, 159.2188), (-58.4766, 156.8555), (-52.8125, 154.1797),
    (-47.3047, 151.2109), (-41.9531, 147.9492), (-36.7969, 144.3945),
    (-31.8359, 140.5859), (-27.1094, 136.5039), (-22.5781, 132.1875),
    (-18.2812, 127.6172), (-14.2578, 122.832),
]

# Shift so (-10.4688, -17.8125) lands at (0, 0), then move -17.81 in Y
pts = [(x + x_offset, y + y_offset - 17.81) for x, y in raw_pts]

with BuildPart() as arc_body:
    with BuildSketch(Plane.XY.offset(10)):  # moved -50 in Z
        with BuildLine():
            Polyline(*pts, close=True)
        make_face()
    extrude(amount=100)

# ── New separate body from Cut.txt (Z=60, extruded 100mm) ────────────────────
# Points reordered into a proper closed profile:
# X shifted so flat face is exactly 140mm from YZ plane (X=0)
x_shift = 140 - 129.5312  # = 10.4688
raw_new_pts = [
    (129.5312, 0.0),      # bottom-left corner
    (491.1328, 0.0),      # bottom-right (start of arc)
    (494.5703, -3.4375),  # arc curving down
    (498.2422, -6.6406),
    (502.1094, -9.5898),
    (506.1719, -12.2852),
    (510.3906, -14.6875),
    (514.7656, -16.8164),
    (519.2969, -18.6523),
    (523.9062, -20.1758),
    (528.5938, -21.3867),
    (533.3984, -22.2852),
    (538.2422, -22.8711),
    (543.0859, -23.125),
    (547.9688, -23.0664),
    (552.8125, -22.6758),
    (557.6172, -21.9531),
    (562.3828, -20.9375),
    (567.0703, -19.5898),
    (571.6406, -17.9297),
    (576.0938, -15.9766),
    (580.3906, -13.7305),
    (584.5703, -11.2109),
    (588.5547, -8.418),
    (592.3438, -5.3516),
    (592.5781, -2.1094),  # rightmost point
    (550.8594, -2.1094),  # return along near-flat top
    (546.9531, -2.4414),
    (543.0469, -2.4805),
    (539.1016, -2.207),
    (535.2344, -1.6602),
    (531.4062, -0.8203),
    (527.6562,  0.293),
    (523.9844,  1.6992),
    (520.4297,  3.3594),
    (517.0312,  5.293),
    (132.7344, 100.0),    # top-right of left section
    (129.5312, 100.0),    # top-left corner
]
new_pts = [(x + x_shift, y) for x, y in raw_new_pts]

with BuildPart() as new_body:
    with BuildSketch(Plane.XY.offset(10)):  # moved -50 in Z
        with BuildLine():
            Polyline(*new_pts, close=True)
        make_face()
    extrude(amount=100)

# ── New body from Cut.txt (Z=10, extruded 50mm upward to Z=60) ───────────────
# Profile: straight top edge (132.73->407.93 at Y=100), left arc going up to peak,
# right side arc going down, bottom flat back.
# Points reordered into proper closed loop:
body3_pts = [
    (132.7344, 100.0),      # top-left start
    (407.9297, 100.0),      # straight line across top-left
    (410.9766, 104.9609),   # top arc begins, curving up-right
    (414.2969, 109.7266),
    (417.9297, 114.2773),
    (421.7969, 118.6328),
    (425.8984, 122.7539),
    (430.2344, 126.6211),
    (434.8047, 130.2148),
    (439.5703, 133.5547),
    (444.5312, 136.6016),
    (449.6484, 139.375),
    (454.9219, 141.8359),
    (460.3125, 143.9844),
    (465.8594, 145.8008),
    (471.4844, 147.3047),
    (477.1484, 148.4961),
    (482.9297, 149.3359),
    (488.7109, 149.8438),
    (494.5312, 150.0),      # top peak
    (500.3516, 149.8438),
    (506.1328, 149.3359),
    (511.875,  148.4961),
    (517.5781, 147.3047),
    (523.2031, 145.8008),
    (528.75,   143.9844),
    (534.1406, 141.8359),
    (539.4141, 139.375),
    (544.5312, 136.6016),
    (549.4922, 133.5547),
    (554.2578, 130.2148),
    (558.7891, 126.6211),
    (563.1641, 122.7539),
    (567.2656, 118.6328),
    (571.1328, 114.2773),
    (574.7266, 109.7266),
    (578.0859, 104.9609),
    (581.1328, 100.0),
    (583.9062, 94.8828),
    (586.3672, 89.6094),
    (588.5156, 84.2188),
    (590.3125, 78.6914),
    (591.8359, 73.0664),
    (593.0078, 67.3633),
    (593.8672, 61.6211),
    (594.375,  55.8203),
    (594.5312, 50.0),       # rightmost point
    (594.4141, 36.9727),
    (594.0234, 23.9258),
    (593.4375, 10.8984),
    (592.5781, -2.1094),    # bottom-right
    (550.8594, -2.1094),    # bottom flat going left
    (546.9531, -2.4414),
    (543.0469, -2.4805),
    (539.1016, -2.207),
    (535.2344, -1.6602),
    (531.4062, -0.8203),
    (527.6562,  0.293),
    (523.9844,  1.6992),
    (520.4297,  3.3594),
    (517.0312,  5.293),     # bottom-left of arc section
]

body3_pts = [(x + 10.4688, y) for x, y in body3_pts]

with BuildPart() as body3:
    with BuildSketch(Plane.XY.offset(10)):   # sketch at Z=10
        with BuildLine():
            Polyline(*body3_pts, close=True)
        make_face()
    extrude(amount=50)                       # extrude to Z=60

# ── Body 4: connector profile at Z=0, extruded 40mm ─────────────────────────
body4_pts = [
    (-10.4688, 117.832),   # top of left vertical edge
    (-10.4688, -17.8125),  # bottom of left vertical edge
    (-7.5781,  -13.5352),  # bottom arc curving right
    (-4.8438,   -9.1406),
    (-2.3047,   -4.6094),
    (0.0,        0.0),     # bottom-right corner
    (129.5312,   0.0),     # bottom straight across
    (129.5312, 100.0),     # right vertical edge top
    (0.0,      100.0),     # top straight across
    (-2.3047,  104.6289),  # top arc curving left
    (-4.8438,  109.1602),
    (-7.5781,  113.5547),  # closes back to start
]

body4_pts = [(x + 10.4688, y) for x, y in body4_pts]  # shift +10.4688 in X

with BuildPart() as body4:
    with BuildSketch(Plane.XY.offset(10)):  # sketch at Z=10 (moved +10 in Z)
        with BuildLine():
            Polyline(*body4_pts, close=True)
        make_face()
    extrude(amount=40)                      # extrude to Z=40

# ── Boolean union: merge all 4 bodies into one ───────────────────────────────
combined_all_solid = arc_body.solid() + new_body.solid() + body3.solid() + body4.solid()

# ── Hole cut: circular profile at Z=10, cut 35mm deep ────────────────────────
import math as _math

hole_raw = [
    (565.7422, 14.5117), (568.8281, 16.5625), (571.7188, 18.8672),
    (574.4141, 21.4258), (576.875, 24.2188), (579.0234, 27.2266),
    (580.9375, 30.4102), (582.5391, 33.75), (583.8672, 37.2266),
    (584.8438, 40.8008), (585.5078, 44.4531), (585.8203, 48.1445),
    (585.8203, 51.8555), (585.5078, 55.5664), (584.8438, 59.1992),
    (583.8672, 62.793), (582.5391, 66.25), (580.9375, 69.6094),
    (579.0234, 72.793), (576.875, 75.7812), (574.4141, 78.5742),
    (571.7188, 81.1523), (568.8281, 83.457), (565.7422, 85.5078),
    (562.4609, 87.2656), (559.0625, 88.7109), (555.5469, 89.8633),
    (551.9141, 90.6836), (548.2422, 91.1914), (544.5312, 91.3477),
    (540.8203, 91.1914), (537.1484, 90.6836), (533.5156, 89.8633),
    (530.0, 88.7109), (526.6016, 87.2656), (523.3203, 85.5078),
    (520.2344, 83.457), (517.3047, 81.1523), (514.6484, 78.5742),
    (512.1875, 75.7812), (510.0, 72.793), (508.125, 69.6094),
    (506.5234, 66.25), (505.1953, 62.793), (504.2188, 59.1992),
    (503.5547, 55.5664), (503.2031, 51.8555), (503.2031, 48.1445),
    (503.5547, 44.4531), (504.2188, 40.8008), (505.1953, 37.2266),
    (506.5234, 33.75), (508.125, 30.4102), (510.0, 27.2266),
    (512.1875, 24.2188), (514.6484, 21.4258), (517.3047, 18.8672),
    (520.2344, 16.5625), (523.3203, 14.5117), (526.6016, 12.7539),
    (530.0, 11.2891), (533.5156, 10.1562), (537.1484, 9.3164),
    (540.8203, 8.8281), (544.5312, 8.6523), (548.2422, 8.8281),
    (551.9141, 9.3164), (555.5469, 10.1562), (559.0625, 11.2891),
    (562.4609, 12.7539),
]

# Sort by angle around center for a clean closed loop
_cx, _cy = 544.5117, 50.0
hole_pts = sorted(hole_raw, key=lambda p: _math.atan2(p[1] - _cy, p[0] - _cx))
hole_pts = [(x + 10.4688, y) for x, y in hole_pts]  # move +10.4688 in X

# (intermediate combined_all removed)

# ── Through-hole cut using inner.txt profile, shifted +10.4688 in X ─────────
inner_raw = [
    (553.2031, 31.9922), (550.8203, 31.0352), (548.3594, 30.3711),
    (545.8203, 30.0391), (543.2422, 30.0391), (540.7031, 30.3711),
    (538.2422, 31.0352), (535.8594, 31.9922), (533.6328, 33.2422),
    (531.5625, 34.7852), (529.7266, 36.5625), (528.125, 38.5742),
    (526.7969, 40.7617), (525.7422, 43.1055), (525.0391, 45.5664),
    (524.6094, 48.0859), (524.5312, 50.6445), (525.3516, 55.7031),
    (526.25, 58.1055), (527.4219, 60.3711), (528.9062, 62.4805),
    (530.625, 64.375), (532.5781, 66.0352), (534.7266, 67.4414),
    (537.0312, 68.5547), (539.4531, 69.3555), (541.9531, 69.8438),
    (544.5312, 70.0), (547.0703, 69.8438), (549.6094, 69.3555),
    (552.0312, 68.5547), (554.3359, 67.4414), (556.4844, 66.0352),
    (558.4375, 64.375), (560.1562, 62.4805), (561.6406, 60.3711),
    (562.8125, 58.1055), (563.7109, 55.7031), (564.2578, 53.2031),
    (564.5312, 50.6445), (564.4531, 48.0859), (564.0234, 45.5664),
    (563.2812, 43.1055), (562.2656, 40.7617), (560.9375, 38.5742),
    (559.3359, 36.5625), (557.5, 34.7852), (555.4297, 33.2422),
]

# Sort by angle around center, then shift +10.4688 in X
_icx, _icy = 544.5312, 50.0
inner_pts = sorted(inner_raw, key=lambda p: _math.atan2(p[1] - _icy, p[0] - _icx))
inner_pts = [(x + 10.4688, y) for x, y in inner_pts]

# ── Chamfer body: loft from outer circle (Z=-40, r≈35) to inner circle (Z=-25, r≈20) ──
# Moved +10.4688 in X after construction
import math as _math2

_ccx, _ccy = 544.5312, 50.0

inner_raw_c = [
    (553.2031, 31.9922), (550.8203, 31.0352), (548.3594, 30.3711),
    (545.8203, 30.0391), (543.2422, 30.0391), (540.7031, 30.3711),
    (538.2422, 31.0352), (535.8594, 31.9922), (533.6328, 33.2422),
    (531.5625, 34.7852), (529.7266, 36.5625), (528.125, 38.5742),
    (526.7969, 40.7617), (525.7422, 43.1055), (525.0391, 45.5664),
    (524.6094, 48.0859), (524.5312, 50.6445), (525.3516, 55.7031),
    (526.25, 58.1055), (527.4219, 60.3711), (528.9062, 62.4805),
    (530.625, 64.375), (532.5781, 66.0352), (534.7266, 67.4414),
    (537.0312, 68.5547), (539.4531, 69.3555), (541.9531, 69.8438),
    (544.5312, 70.0), (547.0703, 69.8438), (549.6094, 69.3555),
    (552.0312, 68.5547), (554.3359, 67.4414), (556.4844, 66.0352),
    (558.4375, 64.375), (560.1562, 62.4805), (561.6406, 60.3711),
    (562.8125, 58.1055), (563.7109, 55.7031), (564.2578, 53.2031),
    (564.5312, 50.6445), (564.4531, 48.0859), (564.0234, 45.5664),
    (563.2812, 43.1055), (562.2656, 40.7617), (560.9375, 38.5742),
    (559.3359, 36.5625), (557.5, 34.7852), (555.4297, 33.2422),
]

outer_raw_c = [
    (534.375, 16.5234), (531.1328, 17.6758), (528.0469, 19.1406),
    (525.0781, 20.8984), (522.3438, 22.9492), (519.7656, 25.2539),
    (517.4609, 27.8125), (513.6719, 33.5156), (512.1875, 36.6211),
    (511.0547, 39.8438), (510.1953, 43.1836), (509.6875, 46.582),
    (509.5312, 50.0), (509.6875, 53.4375), (510.1953, 56.8359),
    (511.0547, 60.1758), (512.1875, 63.3984), (515.4297, 69.4531),
    (517.4609, 72.207), (519.7656, 74.7656), (522.3438, 77.0703),
    (525.0781, 79.1016), (528.0469, 80.8789), (531.1328, 82.3438),
    (534.375, 83.4961), (537.6953, 84.3359), (541.0938, 84.8438),
    (544.5312, 85.0), (547.9688, 84.8438), (551.3672, 84.3359),
    (554.6875, 83.4961), (557.9297, 82.3438), (561.0156, 80.8789),
    (563.9844, 79.1016), (566.7188, 77.0703), (569.2578, 74.7656),
    (571.6016, 72.207), (573.6328, 69.4531), (575.3906, 66.5039),
    (576.875, 63.3984), (578.0078, 60.1758), (578.8672, 56.8359),
    (579.375, 53.4375), (579.5312, 50.0), (579.375, 46.582),
    (578.8672, 43.1836), (578.0078, 39.8438), (576.875, 36.6211),
    (575.3906, 33.5156), (573.6328, 30.5664), (571.6016, 27.8125),
    (569.2578, 25.2539), (566.7188, 22.9492), (563.9844, 20.8984),
    (561.0156, 19.1406), (557.9297, 17.6758), (554.6875, 16.5234),
    (551.3672, 15.6836), (547.9688, 15.1758), (544.5312, 15.0),
    (541.0938, 15.1758), (537.6953, 15.6836),
]

# Sort both by angle around shared center
inner_c = sorted(inner_raw_c, key=lambda p: _math2.atan2(p[1]-_ccy, p[0]-_ccx))
outer_c = sorted(outer_raw_c, key=lambda p: _math2.atan2(p[1]-_ccy, p[0]-_ccx))

# Chamfer: outer (r≈35) at Z=10 (bottom), inner (r≈20) at Z=25 (top)
# Loft bottom->top for correct normals
wire_outer_c = Wire.make_polygon([Vector(x, y, 10) for x, y in outer_c], close=True)
wire_inner_c = Wire.make_polygon([Vector(x, y, 25) for x, y in inner_c], close=True)

chamfer_solid = Solid.make_loft([wire_outer_c, wire_inner_c])

# Shift +10.4688 in X
chamfer_cutter = chamfer_solid.moved(Location(Vector(10.4688, 0, 0)))

# combined_all built below with t cut included

# ── T-body from Cut.txt at Z=-40, extruded 30mm upward ───────────────────────
# 8 points correctly ordered as a 45°-rotated T-shape polygon
# Edges alternate between ~40mm (short) and ~15mm (notch) segments
t_pts = [
    (-25.0,      158.0),     # A - top (updated)
    (4.0,        130.0),     # H - top-right (updated)
    (-124.375,    2.832),   # G - stem right (long edge 161mm)
    (-113.75,    -7.7734),  # F - notch right (short edge 15mm)
    (-142.0312, -36.0742),  # E - bottom-right (short edge 40mm)
    (-191.5625,  13.4375),  # D - bottom-left (long edge 70mm)
    (-163.2422,  41.7188),  # C - notch left (short edge 40mm)
    (-152.6562,  31.1133),  # B - notch inner (short edge 15mm)
]

t_pts = [(x + 10.4688, y) for x, y in t_pts]  # shift +10.4688 in X

# combined_all rebuilt below with all cuts

# ── Two extruded bodies from hole.txt at Z=60, extruded 50mm, shifted +10.4688 in X ──
import math as _math3

h_all = [
    (-158.3984, 134.3359), (-161.7969, 133.8281), (-168.3594, 131.8359),
    (-171.4844, 130.3711), (-174.4141, 128.6133), (-177.1875, 126.5625),
    (-179.7266, 124.2578), (-182.0312, 121.6992), (-184.0625, 118.9453),
    (-185.8203, 115.9961), (-187.3047, 112.8906), (-188.4766, 109.668),
    (-189.2969, 106.3281), (-189.8047, 102.9297), (-189.9609, 99.5117),
    (-189.8047, 96.0742), (-189.2969, 92.6758), (-188.4766, 89.3359),
    (-187.3047, 86.1133), (-185.8203, 83.0078), (-184.0625, 80.0586),
    (-182.0312, 77.3047), (-179.7266, 74.7656), (-177.1875, 72.4414),
    (-174.4141, 70.4102), (-171.4844, 68.6328), (-168.3594, 67.168),
    (-165.1172, 66.0156), (-161.7969, 65.1758), (-158.3984, 64.668),
    (-154.9609, 64.5117), (-151.5234, 64.668), (-148.125, 65.1758),
    (-144.8047, 66.0156), (-141.5625, 67.168), (-138.4766, 68.6328),
    (-135.5078, 70.4102), (-132.7734, 72.4414), (-127.9297, 77.3047),
    (-125.8594, 80.0586), (-124.1016, 83.0078), (-122.6172, 86.1133),
    (-121.4844, 89.3359), (-120.625, 92.6758), (-120.1562, 96.0742),
    (-120.1562, 102.9297), (-120.625, 106.3281), (-121.4844, 109.668),
    (-122.6172, 112.8906), (-124.1016, 115.9961), (-125.8594, 118.9453),
    (-127.9297, 121.6992), (-130.2344, 124.2578), (-132.7734, 126.5625),
    (-135.5078, 128.6133), (-138.4766, 130.3711), (-141.5625, 131.8359),
    (-144.8047, 132.9883), (-148.125, 133.8281), (-151.5234, 134.3359),
    (-154.9609, 134.5117), (-165.1172, 132.9883),
    (-21.1328, -2.9297), (-20.9766, 0.5078), (-21.6406, -6.3281),
    (-22.5, -9.6484), (-23.6328, -12.8906), (-25.1172, -15.9961),
    (-26.875, -18.9258), (-28.9062, -21.6992), (-31.2109, -24.2383),
    (-33.7891, -26.543), (-36.5234, -28.5938), (-21.1328, 3.9453),
    (-21.6406, 7.3438), (-22.5, 10.6641), (-23.6328, 13.9062),
    (-25.1172, 17.0117), (-26.875, 19.9609), (-28.9062, 22.7148),
    (-31.2109, 25.2539), (-33.7891, 27.5586), (-36.5234, 29.6094),
    (-39.4922, 31.3867), (-42.5781, 32.8516), (-45.8203, 34.0039),
    (-49.1406, 34.8438), (-52.5391, 35.332), (-39.4922, -30.3516),
    (-42.5781, -31.8164), (-45.8203, -32.9883), (-49.1406, -33.8086),
    (-52.5391, -34.3164), (-55.9766, -34.4922), (-59.4141, -34.3164),
    (-62.8125, -33.8086), (-66.1328, -32.9883), (-69.375, -31.8164),
    (-72.4609, -30.3516), (-75.4297, -28.5938), (-78.1641, -26.543),
    (-83.0469, -21.6992), (-80.7422, -24.2383), (-85.0781, -18.9258),
    (-86.8359, -15.9961), (-88.3203, -12.8906), (-89.4531, -9.6484),
    (-90.3125, -6.3281), (-90.8203, -2.9297), (-90.9766, 0.5078),
    (-90.8203, 3.9453), (-90.3125, 7.3438), (-89.4531, 10.6641),
    (-88.3203, 13.9062), (-86.8359, 17.0117), (-85.0781, 19.9609),
    (-83.0469, 22.7148), (-80.7422, 25.2539), (-78.1641, 27.5586),
    (-75.4297, 29.6094), (-72.4609, 31.3867), (-69.375, 32.8516),
    (-66.1328, 34.0039), (-62.8125, 34.8438), (-59.4141, 35.332),
    (-55.9766, 35.5078),
]

h1_raw = [(x, y) for x, y in h_all if x < -100]
h2_raw = [(x, y) for x, y in h_all if x > -100]

h1_cx, h1_cy = -155.06, 99.51
h2_cx, h2_cy = -55.98, 0.51

h1_pts = [(x + 10.4688, y) for x, y in sorted(h1_raw, key=lambda p: _math3.atan2(p[1]-h1_cy, p[0]-h1_cx))]
h2_pts = [(x + 10.4688, y) for x, y in sorted(h2_raw, key=lambda p: _math3.atan2(p[1]-h2_cy, p[0]-h2_cx))]

# Cut hole 1 and hole 2 into combined_all, 50mm upward from Z=60

# ── Two extruded bodies from inner.txt, both +Z and -Z, shifted +10.4688 in X ─
import math as _math4

inner2_all = [
    (-145.9375, 114.5117), (-148.125, 115.6055), (-152.8516, 116.875),
    (-150.4297, 116.4062), (-155.2734, 117.0117), (-157.6953, 116.7969),
    (-160.0781, 116.2305), (-162.3828, 115.3711), (-164.4922, 114.1797),
    (-166.4453, 112.7148), (-168.1641, 110.9766), (-169.6484, 109.043),
    (-170.8203, 106.8945), (-171.7188, 104.6289), (-172.2656, 102.2461),
    (-172.4609, 99.8047), (-172.3438, 97.3633), (-171.875, 94.9805),
    (-171.0938, 92.6758), (-169.9609, 90.4883), (-168.5547, 88.4961),
    (-166.9141, 86.6992), (-165.0, 85.1758), (-162.9297, 83.9062),
    (-160.6641, 82.9492), (-158.3203, 82.3242), (-155.8984, 82.0312),
    (-153.4375, 82.0703), (-148.7109, 83.1641), (-151.0156, 82.4609),
    (-146.4844, 84.1992), (-144.4531, 85.5273), (-142.5781, 87.1289),
    (-140.9766, 88.9648), (-139.6484, 91.0156), (-138.6328, 93.2422),
    (-137.9297, 95.5664), (-137.5391, 97.9883), (-137.5, 100.4297),
    (-137.7734, 102.8516), (-138.4375, 105.1953), (-139.375, 107.4414),
    (-140.625, 109.5508), (-142.1875, 111.4453), (-143.9453, 113.1055),
    (-46.4453, -14.1602), (-44.4922, -12.6953), (-42.7734, -10.9766),
    (-41.2891, -9.0234), (-40.1172, -6.8945), (-39.2578, -4.6094),
    (-38.6719, -2.2266), (-38.4766, 0.1953), (-38.5938, 2.6367),
    (-39.0625, 5.0391), (-39.8828, 7.3438), (-40.9766, 9.5312),
    (-44.0234, 13.3008), (-45.9375, 14.8438), (-48.0469, 16.0938),
    (-50.2734, 17.0508), (-52.6172, 17.6953), (-55.0391, 17.9883),
    (-57.5, 17.9492), (-59.9219, 17.5586), (-62.2266, 16.8555),
    (-64.4531, 15.8203), (-66.5234, 14.4922), (-68.3594, 12.8906),
    (-69.9609, 11.0352), (-71.2891, 8.9844), (-72.3047, 6.7773),
    (-73.0078, 4.4531), (-73.3984, 2.0312), (-73.4375, -0.4102),
    (-73.1641, -2.832), (-72.5391, -5.1953), (-71.5625, -7.4414),
    (-48.5938, -15.3516), (-50.8594, -16.2305), (-53.2422, -16.7773),
    (-55.6641, -16.9922), (-58.125, -16.8555), (-60.5078, -16.3867),
    (-62.8125, -15.6055), (-66.9922, -13.0859), (-68.7891, -11.4258),
    (-65.0, -14.4922), (-70.3125, -9.5312), (-42.3828, 11.5234),
]

i2_c1 = [(x, y) for x, y in inner2_all if x < -100]
i2_c2 = [(x, y) for x, y in inner2_all if x > -100]

i2_c1cx, i2_c1cy = -154.9805, 99.5215
i2_c2cx, i2_c2cy = -55.9570, 0.4980

i2_h1_pts = [(x + 10.4688, y) for x, y in sorted(i2_c1, key=lambda p: _math4.atan2(p[1]-i2_c1cy, p[0]-i2_c1cx))]
i2_h2_pts = [(x + 10.4688, y) for x, y in sorted(i2_c2, key=lambda p: _math4.atan2(p[1]-i2_c2cy, p[0]-i2_c2cx))]

# Cut both directions from Z=-7.5 into combined_all

# ── Two chamfer lofts: inner (Z=-7.5, r≈17.5) → outer (Z=10, r≈35) ──────────
# Both shifted +10.4688 in X | height = 17.5mm
import math as _math5

_inner_all_c = [
    (-145.9375, 114.5117), (-148.125, 115.6055), (-152.8516, 116.875),
    (-150.4297, 116.4062), (-155.2734, 117.0117), (-157.6953, 116.7969),
    (-160.0781, 116.2305), (-162.3828, 115.3711), (-164.4922, 114.1797),
    (-166.4453, 112.7148), (-168.1641, 110.9766), (-169.6484, 109.043),
    (-170.8203, 106.8945), (-171.7188, 104.6289), (-172.2656, 102.2461),
    (-172.4609, 99.8047), (-172.3438, 97.3633), (-171.875, 94.9805),
    (-171.0938, 92.6758), (-169.9609, 90.4883), (-168.5547, 88.4961),
    (-166.9141, 86.6992), (-165.0, 85.1758), (-162.9297, 83.9062),
    (-160.6641, 82.9492), (-158.3203, 82.3242), (-155.8984, 82.0312),
    (-153.4375, 82.0703), (-148.7109, 83.1641), (-151.0156, 82.4609),
    (-146.4844, 84.1992), (-144.4531, 85.5273), (-142.5781, 87.1289),
    (-140.9766, 88.9648), (-139.6484, 91.0156), (-138.6328, 93.2422),
    (-137.9297, 95.5664), (-137.5391, 97.9883), (-137.5, 100.4297),
    (-137.7734, 102.8516), (-138.4375, 105.1953), (-139.375, 107.4414),
    (-140.625, 109.5508), (-142.1875, 111.4453), (-143.9453, 113.1055),
    (-46.4453, -14.1602), (-44.4922, -12.6953), (-42.7734, -10.9766),
    (-41.2891, -9.0234), (-40.1172, -6.8945), (-39.2578, -4.6094),
    (-38.6719, -2.2266), (-38.4766, 0.1953), (-38.5938, 2.6367),
    (-39.0625, 5.0391), (-39.8828, 7.3438), (-40.9766, 9.5312),
    (-44.0234, 13.3008), (-45.9375, 14.8438), (-48.0469, 16.0938),
    (-50.2734, 17.0508), (-52.6172, 17.6953), (-55.0391, 17.9883),
    (-57.5, 17.9492), (-59.9219, 17.5586), (-62.2266, 16.8555),
    (-64.4531, 15.8203), (-66.5234, 14.4922), (-68.3594, 12.8906),
    (-69.9609, 11.0352), (-71.2891, 8.9844), (-72.3047, 6.7773),
    (-73.0078, 4.4531), (-73.3984, 2.0312), (-73.4375, -0.4102),
    (-73.1641, -2.832), (-72.5391, -5.1953), (-71.5625, -7.4414),
    (-48.5938, -15.3516), (-50.8594, -16.2305), (-53.2422, -16.7773),
    (-55.6641, -16.9922), (-58.125, -16.8555), (-60.5078, -16.3867),
    (-62.8125, -15.6055), (-66.9922, -13.0859), (-68.7891, -11.4258),
    (-65.0, -14.4922), (-70.3125, -9.5312), (-42.3828, 11.5234),
]

_outer_all_c = [
    (-177.1875, 126.5625), (-179.7266, 124.2578), (-182.0312, 121.6992),
    (-184.0625, 118.9453), (-185.8203, 115.9961), (-187.3047, 112.8906),
    (-188.4766, 109.668), (-189.2969, 106.3281), (-189.8047, 102.9297),
    (-189.9609, 99.5117), (-189.8047, 96.0742), (-189.2969, 92.6758),
    (-188.4766, 89.3359), (-187.3047, 86.1133), (-185.8203, 83.0078),
    (-184.0625, 80.0586), (-182.0312, 77.3047), (-179.7266, 74.7656),
    (-177.1875, 72.4414), (-174.4141, 70.4102), (-171.4844, 68.6328),
    (-168.3594, 67.168), (-165.1172, 66.0156), (-161.7969, 65.1758),
    (-158.3984, 64.668), (-154.9609, 64.5117), (-151.5234, 64.668),
    (-148.125, 65.1758), (-144.8047, 66.0156), (-141.5625, 67.168),
    (-138.4766, 68.6328), (-135.5078, 70.4102), (-132.7734, 72.4414),
    (-130.2344, 74.7656), (-127.9297, 77.3047), (-125.8594, 80.0586),
    (-124.1016, 83.0078), (-122.6172, 86.1133), (-121.4844, 89.3359),
    (-120.625, 92.6758), (-120.1562, 96.0742), (-119.9609, 99.5117),
    (-120.1562, 102.9297), (-120.625, 106.3281), (-121.4844, 109.668),
    (-124.1016, 115.9961), (-122.6172, 112.8906), (-125.8594, 118.9453),
    (-127.9297, 121.6992), (-130.2344, 124.2578), (-135.5078, 128.6133),
    (-132.7734, 126.5625), (-138.4766, 130.3711), (-141.5625, 131.8359),
    (-144.8047, 132.9883), (-148.125, 133.8281), (-154.9609, 134.5117),
    (-151.5234, 134.3359), (-158.3984, 134.3359), (-161.7969, 133.8281),
    (-174.4141, 128.6133), (-171.4844, 130.3711), (-168.3594, 131.8359),
    (-165.1172, 132.9883),
    (-72.4609, 31.3867), (-75.4297, 29.6094), (-78.1641, 27.5586),
    (-80.7422, 25.2539), (-69.375, 32.8516), (-83.0469, 22.7148),
    (-85.0781, 19.9609), (-86.8359, 17.0117), (-88.3203, 13.9062),
    (-89.4531, 10.6641), (-90.3125, 7.3438), (-90.8203, 3.9453),
    (-90.9766, 0.5078), (-90.8203, -2.9297), (-90.3125, -6.3281),
    (-89.4531, -9.6484), (-88.3203, -12.8906), (-86.8359, -15.9961),
    (-85.0781, -18.9258), (-83.0469, -21.6992), (-80.7422, -24.2383),
    (-78.1641, -26.543), (-75.4297, -28.5938), (-69.375, -31.8164),
    (-72.4609, -30.3516), (-66.1328, -32.9883), (-62.8125, -33.8086),
    (-59.4141, -34.3164), (-55.9766, -34.4922), (-52.5391, -34.3164),
    (-49.1406, -33.8086), (-42.5781, -31.8164), (-45.8203, -32.9883),
    (-39.4922, -30.3516), (-36.5234, -28.5938), (-33.7891, -26.543),
    (-31.2109, -24.2383), (-28.9062, -21.6992), (-26.875, -18.9258),
    (-25.1172, -15.9961), (-23.6328, -12.8906), (-22.5, -9.6484),
    (-21.6406, -6.3281), (-21.1328, -2.9297), (-20.9766, 0.5078),
    (-21.1328, 3.9453), (-21.6406, 7.3438), (-22.5, 10.6641),
    (-23.6328, 13.9062), (-25.1172, 17.0117), (-26.875, 19.9609),
    (-28.9062, 22.7148), (-31.2109, 25.2539), (-33.7891, 27.5586),
    (-36.5234, 29.6094), (-39.4922, 31.3867), (-42.5781, 32.8516),
    (-45.8203, 34.0039), (-49.1406, 34.8438), (-55.9766, 35.5078),
    (-52.5391, 35.332), (-59.4141, 35.332), (-62.8125, 34.8438),
    (-66.1328, 34.0039),
]

# Separate and sort each by angle
_ic1 = [(x,y) for x,y in _inner_all_c if x < -100]
_ic2 = [(x,y) for x,y in _inner_all_c if x > -100]
_oc1 = [(x,y) for x,y in _outer_all_c if x < -100]
_oc2 = [(x,y) for x,y in _outer_all_c if x > -100]

_ic1cx, _ic1cy = -154.9805, 99.5215
_ic2cx, _ic2cy = -55.9570, 0.4980
_oc1cx, _oc1cy = -154.9609, 99.5117
_oc2cx, _oc2cy = -55.9766, 0.5078

_dx = 10.4688

ic1_s = [(x+_dx,y) for x,y in sorted(_ic1, key=lambda p: _math5.atan2(p[1]-_ic1cy, p[0]-_ic1cx))]
ic2_s = [(x+_dx,y) for x,y in sorted(_ic2, key=lambda p: _math5.atan2(p[1]-_ic2cy, p[0]-_ic2cx))]
oc1_s = [(x+_dx,y) for x,y in sorted(_oc1, key=lambda p: _math5.atan2(p[1]-_oc1cy, p[0]-_oc1cx))]
oc2_s = [(x+_dx,y) for x,y in sorted(_oc2, key=lambda p: _math5.atan2(p[1]-_oc2cy, p[0]-_oc2cx))]

# Loft chamfer cutters: inner (Z=42.5) → outer (Z=60.0)
w_ic1 = Wire.make_polygon([Vector(x, y, 42.5) for x, y in ic1_s], close=True)
w_oc1 = Wire.make_polygon([Vector(x, y, 60.0) for x, y in oc1_s], close=True)
chamfer_cut1 = Solid.make_loft([w_ic1, w_oc1])

w_ic2 = Wire.make_polygon([Vector(x, y, 42.5) for x, y in ic2_s], close=True)
w_oc2 = Wire.make_polygon([Vector(x, y, 60.0) for x, y in oc2_s], close=True)
chamfer_cut2 = Solid.make_loft([w_ic2, w_oc2])

# ── h2_c1_pts / h2_c2_pts: holes from hole.txt (Z=0, -Z cut, +10.4688 X) ─────
import math as _math6

_hole2_raw = [
    (31.0156, 57.3633), (29.4531, 57.5), (26.4062, 56.8164),
    (25.0391, 56.0352), (23.9062, 54.9609), (23.0078, 53.6914),
    (22.3828, 52.2461), (22.0703, 50.7031), (22.0703, 49.1406),
    (22.4219, 47.6172), (23.0859, 46.1914), (24.0234, 44.9219),
    (25.1953, 43.8867), (26.5625, 43.125), (28.0469, 42.6562),
    (29.6094, 42.5), (31.1719, 42.6953), (32.6562, 43.1836),
    (33.9844, 43.9844), (35.1562, 45.0391), (36.0547, 46.3281),
    (36.6797, 47.7734), (36.9922, 49.2969), (36.9922, 50.8789),
    (36.6406, 52.4023), (35.9766, 53.8281), (35.0391, 55.0781),
    (32.5, 56.8945), (33.8672, 56.1133), (27.8906, 57.3242),
    (87.9688, 57.3438), (86.4844, 56.8555), (85.1172, 56.0742),
    (83.9453, 55.0195), (83.0469, 53.75), (82.3828, 52.3242),
    (82.0703, 50.8008), (82.0703, 49.2188), (82.3828, 47.6953),
    (83.0469, 46.25), (83.9453, 44.9805), (85.1172, 43.9453),
    (86.4844, 43.1641), (87.9688, 42.6758), (89.5312, 42.5),
    (91.0938, 42.6758), (92.5781, 43.1641), (93.9453, 43.9453),
    (95.1172, 44.9805), (96.0156, 46.25), (96.6797, 47.6953),
    (96.9922, 49.2188), (96.9922, 50.8008), (96.6797, 52.3242),
    (96.0156, 53.75), (95.1172, 55.0195), (93.9453, 56.0742),
    (92.5781, 56.8555), (91.0938, 57.3438), (89.5312, 57.5),
]
_h2c1_raw = [(x, y) for x, y in _hole2_raw if x < 60]
_h2c2_raw = [(x, y) for x, y in _hole2_raw if x > 60]
h2_c1_pts = [(x + 10.4688, y) for x, y in sorted(_h2c1_raw, key=lambda p: _math6.atan2(p[1]-50.0, p[0]-29.5312))]
h2_c2_pts = [(x + 10.4688, y) for x, y in sorted(_h2c2_raw, key=lambda p: _math6.atan2(p[1]-50.0, p[0]-89.5312))]

# ── h3_c1_pts / h3_c2_pts: holes from hole.txt (Z=0, +Z cut, +10.4688 X) ─────
import math as _math7

_hole3_raw = [
    (29.4531, 57.5), (27.8906, 57.3242), (26.4062, 56.8164),
    (25.0391, 56.0352), (23.9062, 54.9609), (23.0078, 53.6914),
    (22.0703, 50.7031), (22.0703, 49.1406), (22.4219, 47.6172),
    (23.0859, 46.1914), (31.0156, 57.3633), (32.5, 56.8945),
    (33.8672, 56.1133), (35.0391, 55.0781), (35.9766, 53.8281),
    (36.6406, 52.4023), (36.9922, 50.8789), (36.9922, 49.2969),
    (36.6797, 47.7734), (36.0547, 46.3281), (35.1562, 45.0391),
    (33.9844, 43.9844), (31.1719, 42.6953), (29.6094, 42.5),
    (32.6562, 43.1836), (28.0469, 42.6562), (26.5625, 43.125),
    (24.0234, 44.9219), (25.1953, 43.8867), (22.3828, 52.2461),
    (91.0938, 42.6758), (92.5781, 43.1641), (93.9453, 43.9453),
    (95.1172, 44.9805), (96.0156, 46.25), (96.6797, 47.6953),
    (96.9922, 49.2188), (96.9922, 50.8008), (96.6797, 52.3242),
    (96.0156, 53.75), (95.1172, 55.0195), (93.9453, 56.0742),
    (92.5781, 56.8555), (91.0938, 57.3438), (89.5312, 57.5),
    (87.9688, 57.3438), (86.4844, 56.8555), (85.1172, 56.0742),
    (83.9453, 55.0195), (83.0469, 53.75), (82.3828, 52.3242),
    (82.0703, 50.8008), (82.0703, 49.2188), (82.3828, 47.6953),
    (83.0469, 46.25), (83.9453, 44.9805), (85.1172, 43.9453),
    (86.4844, 43.1641), (87.9688, 42.6758), (89.5312, 42.5),
]
_h3c1_raw = [(x, y) for x, y in _hole3_raw if x < 60]
_h3c2_raw = [(x, y) for x, y in _hole3_raw if x > 60]
h3_c1_pts = [(x + 10.4688, y) for x, y in sorted(_h3c1_raw, key=lambda p: _math7.atan2(p[1]-50.0, p[0]-29.5312))]
h3_c2_pts = [(x + 10.4688, y) for x, y in sorted(_h3c2_raw, key=lambda p: _math7.atan2(p[1]-50.0, p[0]-89.5312))]

# ── Single combined_all: union + all cuts ────────────────────────────────────

# ── New body from Cut.txt: 6-point profile at Z=-40, extruded, +10.4688 in X ─
cut_raw = [
    (173.5938, 20.0),
    (173.5938, 82.4805),
    (185.3906, 82.4805),
    (185.3906, 33.2227),
    (273.5547, 33.2227),
    (273.5547, 20.0),
]
cut_pts = [(x + 10.4688, y) for x, y in cut_raw]  # +10.4688 in X

with BuildPart() as combined_all:
    add(combined_all_solid)
    # TOP text: cut first on clean solid for performance, 5mm in +Z from Z=10
    with BuildSketch(Plane(origin=(376.06, 35, 10), x_dir=(1,0,0), z_dir=(0,0,-1))):
        Text("TOP", font_size=52.5, align=(Align.CENTER, Align.CENTER))
    extrude(amount=-5, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(25)):
        with BuildLine():
            Polyline(*hole_pts, close=True)
        make_face()
    extrude(amount=35, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(-50)):
        with BuildLine():
            Polyline(*inner_pts, close=True)
        make_face()
    extrude(amount=500, mode=Mode.SUBTRACT)
    add(chamfer_cutter, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(10)):
        with BuildLine():
            Polyline(*t_pts, close=True)
        make_face()
    extrude(amount=30, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(60)):
        with BuildLine():
            Polyline(*h1_pts, close=True)
        make_face()
    extrude(amount=50, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(60)):
        with BuildLine():
            Polyline(*h2_pts, close=True)
        make_face()
    extrude(amount=50, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(-7.5)):
        with BuildLine():
            Polyline(*i2_h1_pts, close=True)
        make_face()
    extrude(amount=500, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(-7.5)):
        with BuildLine():
            Polyline(*i2_h1_pts, close=True)
        make_face()
    extrude(amount=-500, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(-7.5)):
        with BuildLine():
            Polyline(*i2_h2_pts, close=True)
        make_face()
    extrude(amount=500, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(-7.5)):
        with BuildLine():
            Polyline(*i2_h2_pts, close=True)
        make_face()
    extrude(amount=-500, mode=Mode.SUBTRACT)
    add(chamfer_cut1, mode=Mode.SUBTRACT)
    add(chamfer_cut2, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(0)):
        with BuildLine():
            Polyline(*h2_c1_pts, close=True)
        make_face()
    extrude(amount=-500, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(0)):
        with BuildLine():
            Polyline(*h2_c2_pts, close=True)
        make_face()
    extrude(amount=-500, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(0)):
        with BuildLine():
            Polyline(*h3_c1_pts, close=True)
        make_face()
    extrude(amount=50, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(0)):
        with BuildLine():
            Polyline(*h3_c2_pts, close=True)
        make_face()
    extrude(amount=50, mode=Mode.SUBTRACT)
    with BuildSketch(Plane(origin=(-95, 50, 105), x_dir=(1,0,0), z_dir=(0,0,1))):
        Text("LEFT", font_size=35, align=(Align.CENTER, Align.CENTER))
    extrude(amount=5, mode=Mode.SUBTRACT)
    with BuildSketch(Plane(origin=(230, 28, 105), x_dir=(1,0,0), z_dir=(0,0,1))):
        Text("BOTTOM", font_size=35, align=(Align.CENTER, Align.CENTER))
    extrude(amount=5, mode=Mode.SUBTRACT)
    # Cut profile from Cut.txt: +10.4688+5 in X, cut 50mm upward from Z=-40
    with BuildSketch(Plane.XY.offset(-35)):
        with BuildLine():
            Polyline(*cut_pts, close=True)
        make_face()
    extrude(amount=50, mode=Mode.SUBTRACT)   # cut 50mm upward to Z=15 (moved +5 in Z)



elbow_left = combined_all.part.translate((731.72, 919.71, 0))

print("✓ Elbow Left built")

# ╔══════════════════════════════════════════════════════════════════════════════
# ASSEMBLY — All parts
# ╔══════════════════════════════════════════════════════════════════════════════

# ╔══════════════════════════════════════════════════════════════════════════════
# PART E — ELBOW RIGHT (Elbow_Right.py)
# ╔══════════════════════════════════════════════════════════════════════════════


# ---------------------------------------------------------------------------
# SHAPE 1 — large rounded-rectangle outline, extruded 100mm
# ---------------------------------------------------------------------------
_er_shape1_points = [
    (540813.2812, 233918.75),
    (540813.2812, 233783.1055),
    (540817.0703, 233778.1055),
    (540821.0938, 233773.3203),
    (540825.3906, 233768.75),
    (540829.9219, 233764.4336),
    (540834.6875, 233760.3516),
    (540839.6484, 233756.5234),
    (540844.8047, 233752.9883),
    (540850.1562, 233749.7266),
    (540855.6641, 233746.7383),
    (540861.3281, 233744.082),
    (540867.1094, 233741.6992),
    (540873.0078, 233739.6484),
    (540879.0234, 233737.9297),
    (540885.1562, 233736.5234),
    (540891.3281, 233735.4492),
    (540897.5391, 233734.6875),
    (540903.7891, 233734.2773),
    (540910.0391, 233734.2188),
    (540916.2891, 233734.4727),
    (540922.5391, 233735.0781),
    (540928.7109, 233735.9961),
    (540940.8984, 233738.8477),
    (540946.875,  233740.7617),
    (540952.7344, 233742.9883),
    (540958.4375, 233745.5273),
    (540964.0234, 233748.3594),
    (540969.4531, 233751.5039),
    (540979.7266, 233758.6133),
    (540989.2188, 233766.7969),
    (540993.6328, 233771.2695),
    (540997.7734, 233775.957),
    (541001.6406, 233780.8594),
    (541005.2734, 233785.9766),
    (541008.6328, 233791.2695),
    (541011.6797, 233796.7188),
    (541014.4531, 233802.3438),
    (541016.875,  233808.1055),
    (541019.0234, 233814.0039),
    (541020.8594, 233819.9805),
    (541022.3438, 233826.0742),
    (541023.5156, 233832.2266),
    (541024.3359, 233838.418),
    (541024.8438, 233844.668),
    (541025.0391, 233850.918),
    (541024.8438, 233857.1875),
    (541024.3359, 233863.418),
    (541023.5156, 233869.6289),
    (541022.3438, 233875.7812),
    (541020.8594, 233881.8555),
    (541019.0234, 233887.8516),
    (541016.875,  233893.7305),
    (541014.4531, 233899.4922),
    (541011.6797, 233905.1172),
    (541008.6328, 233910.5859),
    (541005.2734, 233915.8789),
    (541001.6406, 233920.9961),
    (540997.7734, 233925.8984),
    (540993.6328, 233930.5859),
    (540989.2188, 233935.0391),
    (540979.7266, 233943.2227),
    (540974.6875, 233946.9336),
    (540969.4531, 233950.3516),
    (540964.0234, 233953.4766),
    (540958.4375, 233956.3281),
    (540952.7344, 233958.8672),
    (540946.875,  233961.0938),
    (540940.8984, 233963.0078),
    (540934.8438, 233964.5898),
    (540928.7109, 233965.8594),
    (540922.5391, 233966.7773),
    (540916.2891, 233967.3828),
    (540910.0391, 233967.6367),
    (540903.7891, 233967.5586),
    (540897.5391, 233967.1484),
    (540891.3281, 233966.4062),
    (540885.1562, 233965.332),
    (540879.0234, 233963.9258),
    (540873.0078, 233962.1875),
    (540867.1094, 233960.1367),
    (540861.3281, 233957.7734),
    (540855.6641, 233955.0977),
    (540850.1562, 233952.1289),
    (540844.8047, 233948.8672),
    (540839.6484, 233945.3125),
    (540834.6875, 233941.5039),
    (540829.9219, 233937.4219),
    (540825.3906, 233933.1055),
    (540821.0938, 233928.5352),
    (540817.0703, 233923.75),
]

# ---------------------------------------------------------------------------
# SHAPE 2 — notched rectangle with angled tab, extruded 40mm
# ---------------------------------------------------------------------------
_er_shape2_points = [
    (540813.2812, 233783.1055),
    (540810.3906, 233787.3828),
    (540807.6562, 233791.7773),
    (540805.1562, 233796.3086),
    (540802.8125, 233800.918),
    (540673.2812, 233800.918),
    (540673.2812, 233900.918),
    (540802.8125, 233900.918),
    (540805.1562, 233905.5469),
    (540807.6562, 233910.0781),
    (540810.3906, 233914.4727),
    (540813.2812, 233918.75),
]

# ---------------------------------------------------------------------------
# SHAPE 3 — rectangle + semicircular end, extruded 100mm
# (8 rogue points removed: original indices 3,4,8,10,30,47,54,63)
# ---------------------------------------------------------------------------
_er_shape3_points = [
    (540673.2812, 233900.918),
    (540673.2812, 233800.918),
    (540394.8828, 233800.918),
    (540384.8828, 233786.6406),
    (540381.0156, 233782.3047),
    (540376.9141, 233778.1836),
    (540368.0078, 233770.7031),
    (540363.2422, 233767.3828),
    (540358.2812, 233764.3164),
    (540353.1641, 233761.5625),
    (540347.8906, 233759.1016),
    (540342.5,    233756.9531),
    (540336.9922, 233755.1172),
    (540331.3672, 233753.6133),
    (540325.6641, 233752.4414),
    (540319.9219, 233751.6016),
    (540314.1016, 233751.0938),
    (540308.2812, 233750.918),
    (540302.5,    233751.0938),
    (540296.6797, 233751.6016),
    (540290.9375, 233752.4414),
    (540285.2344, 233753.6133),
    (540279.6094, 233755.1172),
    (540274.1016, 233756.9531),
    (540268.6719, 233759.1016),
    (540258.2812, 233764.3164),
    (540253.3594, 233767.3828),
    (540248.5938, 233770.7031),
    (540244.0234, 233774.3164),
    (540239.6875, 233778.1836),
    (540235.5469, 233782.3047),
    (540231.6797, 233786.6406),
    (540228.0859, 233791.2109),
    (540224.7656, 233795.9766),
    (540221.6797, 233800.918),
    (540218.9453, 233806.0352),
    (540216.4844, 233811.3086),
    (540214.3359, 233816.7188),
    (540212.5,    233822.2461),
    (540210.9766, 233827.8711),
    (540209.8047, 233833.5547),
    (540208.4766, 233845.1172),
    (540208.2812, 233850.918),
    (540208.4375, 233864.7852),
    (540208.8281, 233878.6328),
    (540209.5312, 233892.4609),
    (540210.5078, 233906.2891),
    (540218.2422, 233912.1484),
    (540222.4219, 233914.668),
    (540226.7188, 233916.9141),
    (540231.2109, 233918.8672),
    (540235.7812, 233920.5273),
    (540240.4297, 233921.8555),
    (540245.1953, 233922.8906),
    (540250.0391, 233923.6133),
    (540259.7266, 233924.0625),
    (540264.6094, 233923.8086),
    (540269.4141, 233923.2227),
    (540274.2188, 233922.3242),
    (540278.9062, 233921.1133),
    (540283.5547, 233919.5703),
    (540288.0469, 233917.7539),
    (540292.4219, 233915.625),
    (540296.6406, 233913.2031),
    (540300.7031, 233910.5273),
    (540304.5703, 233907.5586),
    (540308.2422, 233904.3555),
]

# ---------------------------------------------------------------------------
# SHAPE 4 — new profile, extruded 50mm (kept separate)
# (3 rogue points removed: original indices 41, 48, 59)
# ---------------------------------------------------------------------------
_er_shape4_points = [
    (540670.5859, 233800.918),
    (540308.2812, 233890.0977),
    (540285.8203, 233895.6445),
    (540282.1875, 233897.6758),
    (540278.4375, 233899.3945),
    (540274.5703, 233900.8398),
    (540270.5859, 233901.9727),
    (540266.5234, 233902.7734),
    (540262.4219, 233903.2617),
    (540258.2812, 233903.418),
    (540210.2734, 233903.418),
    (540209.4141, 233890.3125),
    (540208.7891, 233877.1875),
    (540208.2812, 233850.918),
    (540208.4766, 233845.1172),
    (540208.9844, 233839.3164),
    (540209.8047, 233833.5547),
    (540210.9766, 233827.8711),
    (540212.5,    233822.2461),
    (540214.3359, 233816.7188),
    (540216.4844, 233811.3086),
    (540218.9453, 233806.0352),
    (540221.6797, 233800.918),
    (540224.7656, 233795.9766),
    (540228.0859, 233791.2109),
    (540231.6797, 233786.6406),
    (540235.5469, 233782.3047),
    (540239.6875, 233778.1836),
    (540244.0234, 233774.3164),
    (540248.5938, 233770.7031),
    (540253.3594, 233767.3828),
    (540258.2812, 233764.3164),
    (540263.3984, 233761.5625),
    (540268.6719, 233759.1016),
    (540274.1016, 233756.9531),
    (540279.6094, 233755.1172),
    (540285.2344, 233753.6133),
    (540290.9375, 233752.4414),
    (540296.6797, 233751.6016),
    (540302.5,    233751.0938),
    (540308.2812, 233750.918),
    # (540319.9219, 233751.6016) <-- REMOVED: out-of-sequence
    (540314.1016, 233751.0938),
    (540325.6641, 233752.4414),
    (540331.3672, 233753.6133),
    (540336.9922, 233755.1172),
    (540342.5,    233756.9531),
    (540347.8906, 233759.1016),
    # (540358.2812, 233764.3164) <-- REMOVED: out-of-sequence
    (540353.1641, 233761.5625),
    (540363.2422, 233767.3828),
    (540368.0078, 233770.7031),
    (540372.5781, 233774.3164),
    (540376.9141, 233778.1836),
    (540381.0156, 233782.3047),
    (540384.8828, 233786.6406),
    (540388.5156, 233791.2109),
    (540391.8359, 233795.9766),
    (540394.8828, 233800.918),
    # (540208.4375, 233864.0625) <-- REMOVED: out-of-sequence
]

# ---------------------------------------------------------------------------
# Shared origin — translate ALL shapes using the global min X and Y
# ---------------------------------------------------------------------------
_er_all_pts = _er_shape1_points + _er_shape2_points + _er_shape3_points + _er_shape4_points
_er_ox = min(p[0] for p in _er_all_pts)
_er_oy = min(p[1] for p in _er_all_pts)

def _er_to_vec(pts):
    return [Vector(x - _er_ox, y - _er_oy) for x, y in pts]

# ---------------------------------------------------------------------------
# Build and extrude Shape 1 — 100mm
# ---------------------------------------------------------------------------
with BuildSketch() as _er_sk1:
    with BuildLine():
        Polyline(*_er_to_vec(_er_shape1_points), close=True)
    make_face()
_er_extrude1 = extrude(_er_sk1.sketch, amount=100)

# ---------------------------------------------------------------------------
# Build and extrude Shape 2 — 40mm
# ---------------------------------------------------------------------------
with BuildSketch() as _er_sk2:
    with BuildLine():
        Polyline(*_er_to_vec(_er_shape2_points), close=True)
    make_face()
_er_extrude2 = extrude(_er_sk2.sketch, amount=40)
_er_extrude2 = _er_extrude2.translate(Vector(0, 0, 60))

# ---------------------------------------------------------------------------
# Build and extrude Shape 3 — 100mm
# ---------------------------------------------------------------------------
with BuildSketch() as _er_sk3:
    with BuildLine():
        Polyline(*_er_to_vec(_er_shape3_points), close=True)
    make_face()
_er_extrude3 = extrude(_er_sk3.sketch, amount=100)


# ---------------------------------------------------------------------------
# Build Shape 4 as a cutting tool.
# The profile is expanded outward by 0.5mm (via shapely buffer) so its walls
# never land exactly on Shape 3's faces — this eliminates the small coplanar
# residual faces that appear when _er_cutter and solid share an exact boundary.
# Placed at z=50, extruded 51mm up (z=50→101) to cut the top 50mm of the
# combined body with a 1mm overcut at the top for a clean open face.
# ---------------------------------------------------------------------------
_er_shape4_cutter_points = [
    (540674.7092, 233800.418),
    (540395.1619, 233800.418),
    (540392.2542, 233795.7023),
    (540388.9168, 233790.9121),
    (540385.2654, 233786.3184),
    (540381.3796, 233781.9617),
    (540377.2580, 233777.8203),
    (540372.8998, 233773.9334),
    (540368.3060, 233770.3015),
    (540363.5106, 233766.9604),
    (540353.3953, 233761.1186),
    (540348.0890, 233758.6424),
    (540342.6718, 233756.4833),
    (540337.1360, 233754.6381),
    (540331.4822, 233753.1265),
    (540325.7435, 233751.9473),
    (540314.1382, 233750.5947),
    (540308.2811, 233750.4178),
    (540302.4706, 233750.5945),
    (540296.6217, 233751.1048),
    (540290.8509, 233751.9487),
    (540285.1194, 233753.1265),
    (540279.4656, 233754.6381),
    (540273.9304, 233756.4831),
    (540268.4740, 233758.6422),
    (540263.1740, 233761.1154),
    (540258.0303, 233763.8836),
    (540253.0841, 233766.9652),
    (540248.2956, 233770.3015),
    (540243.7017, 233773.9334),
    (540239.3445, 233777.8196),
    (540235.1836, 233781.9608),
    (540231.2962, 233786.3194),
    (540227.6839, 233790.9132),
    (540224.3482, 233795.7011),
    (540221.2467, 233800.6675),
    (540218.4979, 233805.8115),
    (540216.0251, 233811.1104),
    (540213.8659, 233816.5476),
    (540212.0211, 233822.1018),
    (540210.4900, 233827.7552),
    (540209.3119, 233833.4689),
    (540208.4875, 233839.2593),
    (540207.9773, 233845.0870),
    (540207.7810, 233850.9144),
    (540208.2893, 233877.2042),
    (540208.9149, 233890.3408),
    (540209.8051, 233903.9180),
    (540258.2906, 233903.9180),
    (540262.4609, 233903.7606),
    (540266.6014, 233903.2676),
    (540270.7028, 233902.4593),
    (540274.7264, 233901.3152),
    (540278.6294, 233899.8565),
    (540282.4140, 233898.1220),
    (540286.0055, 233896.1138),
    (540308.4009, 233890.5832),
    (540674.7092, 233800.418),  # close back to start
]

with BuildSketch() as _er_sk4:
    with BuildLine():
        Polyline(*_er_to_vec(_er_shape4_cutter_points), close=False)  # already closed
    make_face()
_er_cutter = extrude(_er_sk4.sketch, amount=50)
_er_cutter = _er_cutter.translate(Vector(0, 0, 50))

# ---------------------------------------------------------------------------
# SHAPE 5 — hexagonal profile, extruded 30mm (separate body)
# ---------------------------------------------------------------------------
_er_shape5_points = [
    (540291.4844, 233850.918),
    (540274.8828, 233879.668),
    (540241.6797, 233879.668),
    (540225.1172, 233850.918),
    (540241.6797, 233822.168),
    (540274.8828, 233822.168),
]

with BuildSketch() as _er_sk5:
    with BuildLine():
        Polyline(*_er_to_vec(_er_shape5_points), close=True)
    make_face()
_er_extrude5 = extrude(_er_sk5.sketch, amount=30)

# ---------------------------------------------------------------------------
# SHAPE 6 — hollow cylinder: outer ring minus inner ring, extruded 5mm
# Both profiles sorted by angle around centroid to ensure no self-intersection
# ---------------------------------------------------------------------------
_er_outer_points = [
    (540213.2812, 233850.918),
    (540213.4766, 233847.0508),
    (540213.9453, 233843.2227),
    (540214.8047, 233839.4336),
    (540217.3828, 233832.1484),
    (540219.1797, 233828.7109),
    (540221.2109, 233825.4297),
    (540223.5547, 233822.3242),
    (540226.1328, 233819.4531),
    (540228.9453, 233816.7969),
    (540231.9922, 233814.4141),
    (540235.2344, 233812.2852),
    (540238.6328, 233810.4492),
    (540242.1875, 233808.9062),
    (540245.8594, 233807.6758),
    (540249.6484, 233806.7578),
    (540253.4766, 233806.1914),
    (540257.3438, 233805.9375),
    (540261.2109, 233806.0156),
    (540265.0391, 233806.4258),
    (540268.8672, 233807.1875),
    (540272.5781, 233808.2422),
    (540276.1719, 233809.6289),
    (540279.6875, 233811.3281),
    (540286.1328, 233815.5664),
    (540291.7969, 233820.8594),
    (540294.2578, 233823.8477),
    (540296.4453, 233827.0508),
    (540298.3594, 233830.4102),
    (540299.9609, 233833.9258),
    (540301.25,   233837.5781),
    (540302.2656, 233841.3086),
    (540302.9297, 233845.1367),
    (540303.2422, 233848.9844),
    (540303.2422, 233852.8516),
    (540302.2656, 233860.5273),
    (540301.25,   233864.2773),
    (540299.9609, 233867.9297),
    (540298.3594, 233871.4453),
    (540294.2578, 233877.9883),
    (540291.7969, 233880.9961),
    (540289.0625, 233883.75),
    (540286.1328, 233886.2695),
    (540283.0078, 233888.5352),
    (540279.6875, 233890.5273),
    (540276.1719, 233892.207),
    (540272.5781, 233893.5938),
    (540268.8672, 233894.668),
    (540265.0391, 233895.4102),
    (540261.2109, 233895.8398),
    (540257.3438, 233895.918),
    (540253.4766, 233895.6641),
    (540249.6484, 233895.0781),
    (540245.8594, 233894.1797),
    (540242.1875, 233892.9492),
    (540238.6328, 233891.4062),
    (540235.2344, 233889.5703),
    (540231.9922, 233887.4414),
    (540228.9453, 233885.0391),
    (540226.1328, 233882.4023),
    (540223.5547, 233879.5117),
    (540221.2109, 233876.4258),
    (540219.1797, 233873.1445),
    (540215.9375, 233866.1133),
    (540214.8047, 233862.4219),
    (540213.9453, 233858.6328),
    (540213.4766, 233854.7852),
]

_er_inner_points = [
    (540228.4766, 233847.7344),
    (540228.9844, 233844.5898),
    (540229.8047, 233841.5039),
    (540230.9766, 233838.5352),
    (540232.4609, 233835.7031),
    (540234.2188, 233833.0273),
    (540236.25,   233830.5664),
    (540238.5547, 233828.3398),
    (540241.0547, 233826.3672),
    (540243.75,   233824.6875),
    (540246.6406, 233823.2812),
    (540249.6484, 233822.207),
    (540252.7344, 233821.4453),
    (540255.8984, 233821.0156),
    (540259.1016, 233820.9375),
    (540262.2656, 233821.1914),
    (540265.4297, 233821.7773),
    (540268.4766, 233822.6953),
    (540271.4062, 233823.9453),
    (540274.2188, 233825.4883),
    (540276.8359, 233827.3242),
    (540279.2188, 233829.4336),
    (540281.4062, 233831.7773),
    (540283.2812, 233834.3359),
    (540284.9219, 233837.0898),
    (540286.25,   233840.0),
    (540287.2266, 233843.0273),
    (540287.9297, 233846.1523),
    (540288.2422, 233849.3359),
    (540288.2422, 233852.5195),
    (540286.25,   233861.8555),
    (540284.9219, 233864.7656),
    (540283.2812, 233867.5),
    (540281.4062, 233870.0781),
    (540279.2188, 233872.4219),
    (540276.8359, 233874.5117),
    (540274.2188, 233876.3477),
    (540271.4062, 233877.9102),
    (540268.4766, 233879.1406),
    (540265.4297, 233880.0586),
    (540262.2656, 233880.6641),
    (540259.1016, 233880.918),
    (540255.8984, 233880.8203),
    (540252.7344, 233880.4102),
    (540249.6484, 233879.6484),
    (540246.6406, 233878.5547),
    (540243.75,   233877.168),
    (540241.0547, 233875.4688),
    (540238.5547, 233873.4961),
    (540236.25,   233871.2695),
    (540232.4609, 233866.1523),
    (540230.9766, 233863.3203),
    (540229.8047, 233860.3516),
    (540228.9844, 233857.2656),
    (540228.4766, 233854.1211),
    (540228.2812, 233850.918),
]

with BuildSketch() as _er_sk6:
    with BuildLine():
        Polyline(*_er_to_vec(_er_outer_points), close=True)
    make_face()
    with BuildLine():
        Polyline(*_er_to_vec(_er_inner_points), close=True)
    make_face(mode=Mode.SUBTRACT)

_er_hollow_cylinder = extrude(_er_sk6.sketch, amount=5)
_er_hollow_cylinder = _er_hollow_cylinder.translate(Vector(0, 0, 45))

# ---------------------------------------------------------------------------
# Fuse shapes 1+2+3, cut shape 4 and shape 5; shape 6 separate
# ---------------------------------------------------------------------------
# _er_result computed below after all shapes are defined

# ---------------------------------------------------------------------------
# SHAPE 7 — ellipse/circle profile, extruded 18.5mm (separate body)
# Points sorted by angle around centroid to ensure clean wire
# ---------------------------------------------------------------------------
_er_shape7_points = [
    (540244.8047, 233850.918),
    (540244.9609, 233848.8086),
    (540245.4688, 233846.7578),
    (540246.25,   233844.8047),
    (540247.3828, 233842.9883),
    (540248.75,   233841.3867),
    (540250.3516, 233840.0),
    (540252.1484, 233838.8867),
    (540254.1406, 233838.0859),
    (540256.1719, 233837.5977),
    (540258.2812, 233837.4219),
    (540260.3906, 233837.5977),
    (540262.4609, 233838.0859),
    (540264.4141, 233838.8867),
    (540266.25,   233840.0),
    (540267.8516, 233841.3867),
    (540269.2188, 233842.9883),
    (540270.3125, 233844.8047),
    (540271.1328, 233846.7578),
    (540271.6406, 233848.8086),
    (540271.7969, 233850.918),
    (540271.6406, 233853.0273),
    (540271.1328, 233855.0977),
    (540270.3125, 233857.0508),
    (540269.2188, 233858.8672),
    (540267.8516, 233860.4688),
    (540266.25,   233861.8555),
    (540264.4141, 233862.9492),
    (540262.4609, 233863.7695),
    (540260.3906, 233864.2578),
    (540258.2812, 233864.4336),
    (540256.1719, 233864.2578),
    (540254.1406, 233863.7695),
    (540252.1484, 233862.9492),
    (540250.3516, 233861.8555),
    (540248.75,   233860.4688),
    (540247.3828, 233858.8672),
    (540246.25,   233857.0508),
    (540245.4688, 233855.0977),
    (540244.9609, 233853.0273),
]

with BuildSketch() as _er_sk7:
    with BuildLine():
        Polyline(*_er_to_vec(_er_shape7_points), close=True)
    make_face()
_er_extrude7 = extrude(_er_sk7.sketch, amount=18.5)
_er_extrude7 = _er_extrude7.translate(Vector(0, 0, 31.5))

# ---------------------------------------------------------------------------
# SHAPE 8 — diagonal profile, extruded 30mm (separate body)
# ---------------------------------------------------------------------------
_er_shape8_points = [
    (540822.5131, 233736.8458),
    (540955.4688, 233869.8242),
    (540966.0938, 233859.2188),
    (540994.375,  233887.5),
    (540944.8828, 233936.9922),
    (540916.6016, 233908.7109),
    (540927.1875, 233898.1055),
    (540794.2294, 233765.1247),
]

with BuildSketch() as _er_sk8:
    with BuildLine():
        Polyline(*_er_to_vec(_er_shape8_points), close=True)
    make_face()
_er_extrude8 = extrude(_er_sk8.sketch, amount=30)
_er_extrude8 = _er_extrude8.translate(Vector(0, 0, 70))

# ---------------------------------------------------------------------------
# SHAPE 9 — two circular holes, extruded 240mm centred at z=-120
# so they cut 120mm in both +Z and -Z directions
# Cluster 1: circle centred ~(540858.8, 233900.4)
# Cluster 2: circle centred ~(540957.8, 233801.4)
# ---------------------------------------------------------------------------
_er_hole1_points = [
    (540841.4062, 233898.5938),
    (540841.8359, 233896.1914),
    (540842.5781, 233893.8672),
    (540843.6328, 233891.6797),
    (540845.0,    233889.6484),
    (540846.6406, 233887.832),
    (540848.5156, 233886.2695),
    (540850.5859, 233884.9609),
    (540852.8125, 233883.9844),
    (540855.1562, 233883.3008),
    (540857.5781, 233882.9688),
    (540860.0,    233882.9688),
    (540862.4219, 233883.3008),
    (540864.7656, 233883.9844),
    (540867.0312, 233884.9609),
    (540869.1016, 233886.2695),
    (540870.9375, 233887.832),
    (540872.5781, 233889.6484),
    (540873.9453, 233891.6797),
    (540875.0391, 233893.8672),
    (540875.7812, 233896.1914),
    (540876.2109, 233898.5938),
    (540876.2891, 233901.0352),
    (540876.0156, 233903.457),
    (540875.4297, 233905.8203),
    (540874.5312, 233908.0859),
    (540873.3203, 233910.2148),
    (540871.7969, 233912.1289),
    (540870.0391, 233913.8281),
    (540868.0859, 233915.2539),
    (540865.8984, 233916.4062),
    (540863.6328, 233917.2461),
    (540861.25,   233917.7539),
    (540858.7891, 233917.9297),
    (540856.3672, 233917.7539),
    (540853.9844, 233917.2461),
    (540851.6797, 233916.4062),
    (540849.5312, 233915.2539),
    (540847.5391, 233913.8281),
    (540845.7812, 233912.1289),
    (540844.2969, 233910.2148),
    (540843.0859, 233908.0859),
    (540842.1484, 233905.8203),
    (540841.5625, 233903.457),
    (540841.3281, 233901.0352),
]

_er_hole2_points = [
    (540940.3906, 233799.5898),
    (540940.8203, 233797.1875),
    (540941.5625, 233794.8633),
    (540942.6562, 233792.6758),
    (540943.9844, 233790.6445),
    (540945.625,  233788.8477),
    (540947.5,    233787.2656),
    (540949.5703, 233785.9766),
    (540951.7969, 233784.9805),
    (540954.1406, 233784.3164),
    (540956.5625, 233783.9648),
    (540959.0234, 233783.9648),
    (540961.4453, 233784.3164),
    (540963.7891, 233784.9805),
    (540966.0156, 233785.9766),
    (540968.0859, 233787.2656),
    (540969.9609, 233788.8477),
    (540971.6016, 233790.6445),
    (540972.9297, 233792.6758),
    (540974.0234, 233794.8633),
    (540974.7656, 233797.1875),
    (540975.1953, 233799.5898),
    (540975.2734, 233802.0312),
    (540975.0391, 233804.4727),
    (540974.4531, 233806.8359),
    (540973.5156, 233809.1016),
    (540972.3047, 233811.2109),
    (540970.7812, 233813.1445),
    (540969.0234, 233814.8242),
    (540967.0703, 233816.2695),
    (540964.9219, 233817.4219),
    (540962.6172, 233818.2422),
    (540960.2344, 233818.75),
    (540957.8125, 233818.9258),
    (540955.3516, 233818.75),
    (540952.9688, 233818.2422),
    (540950.6641, 233817.4219),
    (540948.5156, 233816.2695),
    (540946.5625, 233814.8242),
    (540944.8047, 233813.1445),
    (540943.2812, 233811.2109),
    (540942.0703, 233809.1016),
    (540941.1328, 233806.8359),
    (540940.5469, 233804.4727),
    (540940.3125, 233802.0312),
]

# Place at z=-120, extrude 240mm → cuts from -120 to +120 (both directions)
with BuildSketch(Plane.XY.offset(-120)) as _er_sk9a:
    with BuildLine():
        Polyline(*_er_to_vec(_er_hole1_points), close=True)
    make_face()
_er_hole1 = extrude(_er_sk9a.sketch, amount=240)

with BuildSketch(Plane.XY.offset(-120)) as _er_sk9b:
    with BuildLine():
        Polyline(*_er_to_vec(_er_hole2_points), close=True)
    make_face()
_er_hole2 = extrude(_er_sk9b.sketch, amount=240)

# ---------------------------------------------------------------------------
# SHAPE 10 — two outer ring profiles extruded as a single separate body
# Profile A: large circle centred ~(540858.8, 233900.4)
# Profile B: large circle centred ~(540957.8, 233801.4)
# ---------------------------------------------------------------------------
_er_outer10a_points = [
    (540823.9844, 233896.9922),
    (540824.4531, 233893.5938),
    (540825.3125, 233890.2539),
    (540826.4453, 233887.0312),
    (540827.9297, 233883.9258),
    (540829.6875, 233880.9766),
    (540831.7578, 233878.2227),
    (540834.0625, 233875.6641),
    (540836.6016, 233873.3594),
    (540839.3359, 233871.3281),
    (540842.3047, 233869.5508),
    (540845.3906, 233868.0859),
    (540848.6328, 233866.9336),
    (540851.9531, 233866.0938),
    (540855.3516, 233865.5859),
    (540858.7891, 233865.4297),
    (540862.2266, 233865.5859),
    (540865.625,  233866.0938),
    (540868.9453, 233866.9336),
    (540872.1875, 233868.0859),
    (540875.3125, 233869.5508),
    (540878.2422, 233871.3281),
    (540881.0156, 233873.3594),
    (540883.5547, 233875.6641),
    (540885.8594, 233878.2227),
    (540887.8906, 233880.9766),
    (540889.6484, 233883.9258),
    (540891.1328, 233887.0312),
    (540892.3047, 233890.2539),
    (540893.125,  233893.5938),
    (540893.6328, 233896.9922),
    (540893.7891, 233900.4297),
    (540893.6328, 233903.8477),
    (540893.125,  233907.2461),
    (540892.3047, 233910.5859),
    (540891.1328, 233913.8086),
    (540889.6484, 233916.9141),
    (540887.8906, 233919.8633),
    (540885.8594, 233922.6172),
    (540883.5547, 233925.1758),
    (540881.0156, 233927.4805),
    (540878.2422, 233929.5312),
    (540875.3125, 233931.2891),
    (540872.1875, 233932.7539),
    (540868.9453, 233933.9062),
    (540865.625,  233934.7461),
    (540862.2266, 233935.2539),
    (540858.7891, 233935.4297),
    (540855.3516, 233935.2539),
    (540851.9531, 233934.7461),
    (540848.6328, 233933.9062),
    (540845.3906, 233932.7539),
    (540842.3047, 233931.2891),
    (540839.3359, 233929.5312),
    (540836.6016, 233927.4805),
    (540834.0625, 233925.1758),
    (540831.7578, 233922.6172),
    (540829.6875, 233919.8633),
    (540827.9297, 233916.9141),
    (540826.4453, 233913.8086),
    (540825.3125, 233910.5859),
    (540824.4531, 233907.2461),
    (540823.9844, 233903.8477),
    (540823.7891, 233900.4297),
]

_er_outer10b_points = [
    (540922.8125, 233801.4258),
    (540922.9688, 233797.9883),
    (540923.4766, 233794.5898),
    (540924.2969, 233791.2695),
    (540925.4688, 233788.0273),
    (540926.9141, 233784.9219),
    (540928.7109, 233781.9727),
    (540930.7422, 233779.2188),
    (540933.0469, 233776.6797),
    (540935.5859, 233774.375),
    (540938.3594, 233772.3242),
    (540941.2891, 233770.5664),
    (540944.4141, 233769.082),
    (540947.6172, 233767.9297),
    (540950.9766, 233767.1094),
    (540954.375,  233766.6016),
    (540957.8125, 233766.4258),
    (540961.2109, 233766.6016),
    (540964.6094, 233767.1094),
    (540967.9688, 233767.9297),
    (540971.1719, 233769.082),
    (540974.2969, 233770.5664),
    (540977.2266, 233772.3242),
    (540980.0,    233774.375),
    (540982.5391, 233776.6797),
    (540984.8438, 233779.2188),
    (540986.9141, 233781.9727),
    (540988.6719, 233784.9219),
    (540990.1172, 233788.0273),
    (540991.2891, 233791.2695),
    (540992.1094, 233794.5898),
    (540992.6172, 233797.9883),
    (540992.8125, 233801.4258),
    (540992.6172, 233804.8633),
    (540992.1094, 233808.2617),
    (540991.2891, 233811.582),
    (540990.1172, 233814.8242),
    (540988.6719, 233817.9297),
    (540986.9141, 233820.8789),
    (540984.8438, 233823.6328),
    (540982.5391, 233826.1719),
    (540980.0,    233828.4766),
    (540977.2266, 233830.5273),
    (540974.2969, 233832.2852),
    (540971.1719, 233833.7695),
    (540967.9688, 233834.9219),
    (540964.6094, 233835.7617),
    (540961.2109, 233836.25),
    (540957.8125, 233836.4258),
    (540954.375,  233836.25),
    (540950.9766, 233835.7617),
    (540947.6172, 233834.9219),
    (540944.4141, 233833.7695),
    (540941.2891, 233832.2852),
    (540938.3594, 233830.5273),
    (540935.5859, 233828.4766),
    (540933.0469, 233826.1719),
    (540930.7422, 233823.6328),
    (540928.7109, 233820.8789),
    (540926.9141, 233817.9297),
    (540925.4688, 233814.8242),
    (540924.2969, 233811.582),
    (540923.4766, 233808.2617),
    (540922.9688, 233804.8633),
]

with BuildSketch() as _er_sk10:
    with BuildLine():
        Polyline(*_er_to_vec(_er_outer10a_points), close=True)
    make_face()
    with BuildLine():
        Polyline(*_er_to_vec(_er_outer10b_points), close=True)
    make_face()
_er_extrude10 = extrude(_er_sk10.sketch, amount=50)

# ---------------------------------------------------------------------------
# SHAPE 11 — two hollow chamfer rings (outer - inner), extruded 17.5mm
# Placed at z=50 (on top of _er_extrude10 which sits at z=0..50)
# Ring A: centred ~(540858.8, 233900.4)
# Ring B: centred ~(540957.8, 233801.4)
# ---------------------------------------------------------------------------
_er_outer11a_points = [
    (540823.9844, 233896.9922),(540824.4531, 233893.5938),(540825.3125, 233890.2539),
    (540826.4453, 233887.0312),(540827.9297, 233883.9258),(540829.6875, 233880.9766),
    (540831.7578, 233878.2227),(540834.0625, 233875.6641),(540836.6016, 233873.3594),
    (540839.3359, 233871.3281),(540842.3047, 233869.5508),(540845.3906, 233868.0859),
    (540848.6328, 233866.9336),(540851.9531, 233866.0938),(540855.3516, 233865.5859),
    (540858.7891, 233865.4297),(540862.2266, 233865.5859),(540865.625,  233866.0938),
    (540868.9453, 233866.9336),(540872.1875, 233868.0859),(540875.3125, 233869.5508),
    (540878.2422, 233871.3281),(540881.0156, 233873.3594),(540883.5547, 233875.6641),
    (540885.8594, 233878.2227),(540887.8906, 233880.9766),(540889.6484, 233883.9258),
    (540891.1328, 233887.0312),(540892.3047, 233890.2539),(540893.125,  233893.5938),
    (540893.6328, 233896.9922),(540893.7891, 233900.4297),(540893.6328, 233903.8477),
    (540893.125,  233907.2461),(540892.3047, 233910.5859),(540891.1328, 233913.8086),
    (540889.6484, 233916.9141),(540887.8906, 233919.8633),(540885.8594, 233922.6172),
    (540883.5547, 233925.1758),(540881.0156, 233927.4805),(540878.2422, 233929.5312),
    (540875.3125, 233931.2891),(540872.1875, 233932.7539),(540868.9453, 233933.9062),
    (540865.625,  233934.7461),(540862.2266, 233935.2539),(540858.7891, 233935.4297),
    (540855.3516, 233935.2539),(540851.9531, 233934.7461),(540848.6328, 233933.9062),
    (540845.3906, 233932.7539),(540842.3047, 233931.2891),(540839.3359, 233929.5312),
    (540836.6016, 233927.4805),(540834.0625, 233925.1758),(540831.7578, 233922.6172),
    (540829.6875, 233919.8633),(540827.9297, 233916.9141),(540826.4453, 233913.8086),
    (540825.3125, 233910.5859),(540824.4531, 233907.2461),(540823.9844, 233903.8477),
    (540823.7891, 233900.4297),
]

_er_inner11a_points = [
    (540841.4453, 233898.2812),(540841.9141, 233895.8984),(540842.6953, 233893.5938),
    (540843.7891, 233891.4062),(540845.1953, 233889.4141),(540846.875,  233887.6172),
    (540848.75,   233886.0938),(540850.8594, 233884.8242),(540853.0859, 233883.8672),
    (540855.4688, 233883.2422),(540857.8906, 233882.9492),(540860.3125, 233882.9883),
    (540862.7344, 233883.3789),(540865.0781, 233884.082), (540867.2656, 233885.1172),
    (540869.3359, 233886.4453),(540871.1719, 233888.0469),(540872.7734, 233889.8828),
    (540874.1016, 233891.9336),(540875.1172, 233894.1602),(540875.8594, 233896.4844),
    (540876.25,   233898.9062),(540876.2891, 233901.3477),(540875.9766, 233903.7695),
    (540875.3516, 233906.1133),(540874.375,  233908.3594),(540873.125,  233910.4688),
    (540871.6016, 233912.3633),(540869.8047, 233914.0234),(540867.8125, 233915.4297),
    (540865.625,  233916.5234),(540863.3203, 233917.3242),(540860.9375, 233917.793),
    (540858.4766, 233917.9102),(540856.0547, 233917.7148),(540853.6719, 233917.1484),
    (540851.4062, 233916.2891),(540849.2578, 233915.0977),(540847.3047, 233913.6328),
    (540845.5859, 233911.8945),(540844.1406, 233909.9609),(540842.9297, 233907.8125),
    (540842.0703, 233905.5469),(540841.5234, 233903.1641),(540841.2891, 233900.7227),
]

_er_outer11b_points = [
    (540922.8125, 233801.4258),(540922.9688, 233797.9883),(540923.4766, 233794.5898),
    (540924.2969, 233791.2695),(540925.4688, 233788.0273),(540926.9141, 233784.9219),
    (540928.7109, 233781.9727),(540930.7422, 233779.2188),(540933.0469, 233776.6797),
    (540935.5859, 233774.375), (540938.3594, 233772.3242),(540941.2891, 233770.5664),
    (540944.4141, 233769.082), (540947.6172, 233767.9297),(540950.9766, 233767.1094),
    (540954.375,  233766.6016),(540957.8125, 233766.4258),(540961.2109, 233766.6016),
    (540964.6094, 233767.1094),(540967.9688, 233767.9297),(540971.1719, 233769.082),
    (540974.2969, 233770.5664),(540977.2266, 233772.3242),(540980.0,    233774.375),
    (540982.5391, 233776.6797),(540984.8438, 233779.2188),(540986.9141, 233781.9727),
    (540988.6719, 233784.9219),(540990.1172, 233788.0273),(540991.2891, 233791.2695),
    (540992.1094, 233794.5898),(540992.6172, 233797.9883),(540992.8125, 233801.4258),
    (540992.6172, 233804.8633),(540992.1094, 233808.2617),(540991.2891, 233811.582),
    (540990.1172, 233814.8242),(540988.6719, 233817.9297),(540986.9141, 233820.8789),
    (540984.8438, 233823.6328),(540982.5391, 233826.1719),(540980.0,    233828.4766),
    (540977.2266, 233830.5273),(540974.2969, 233832.2852),(540971.1719, 233833.7695),
    (540967.9688, 233834.9219),(540964.6094, 233835.7617),(540961.2109, 233836.25),
    (540957.8125, 233836.4258),(540954.375,  233836.25),  (540950.9766, 233835.7617),
    (540947.6172, 233834.9219),(540944.4141, 233833.7695),(540941.2891, 233832.2852),
    (540938.3594, 233830.5273),(540935.5859, 233828.4766),(540933.0469, 233826.1719),
    (540930.7422, 233823.6328),(540928.7109, 233820.8789),(540926.9141, 233817.9297),
    (540925.4688, 233814.8242),(540924.2969, 233811.582), (540923.4766, 233808.2617),
    (540922.9688, 233804.8633),
]

_er_inner11b_points = [
    (540940.3125, 233800.5078),(540940.625,  233798.0859),(540941.25,   233795.7227),
    (540942.1875, 233793.4766),(540943.4766, 233791.3867),(540945.0,    233789.4922),
    (540946.7969, 233787.832), (540948.7891, 233786.4258),(540950.9375, 233785.3125),
    (540953.2812, 233784.5312),(540955.6641, 233784.0625),(540958.0859, 233783.9258),
    (540960.5469, 233784.1406),(540962.8906, 233784.6875),(540965.1953, 233785.5664),
    (540967.3438, 233786.7578),(540969.2578, 233788.2227),(540971.0156, 233789.9414),
    (540972.4609, 233791.8945),(540973.6719, 233794.0234),(540974.5312, 233796.3086),
    (540975.0781, 233798.6914),(540975.2734, 233801.1133),(540975.1562, 233803.5547),
    (540974.6875, 233805.957), (540973.9062, 233808.2617),(540972.8125, 233810.4492),
    (540971.4062, 233812.4414),(540969.7266, 233814.2188),(540967.8125, 233815.7617),
    (540965.7422, 233817.0117),(540963.4766, 233817.9688),(540961.1328, 233818.6133),
    (540958.7109, 233818.9062),(540956.25,   233818.8672),(540953.8672, 233818.4766),
    (540951.5234, 233817.7734),(540949.2969, 233816.7383),(540947.2656, 233815.4102),
    (540945.4297, 233813.8086),(540943.8281, 233811.9531),(540942.5,    233809.9023),
    (540941.4453, 233807.6953),(540940.7422, 233805.3711),(540940.3516, 233802.9492),
]

# Chamfer ring A: loft from outer profile at z=50 to inner profile at z=67.5
with BuildSketch(Plane.XY.offset(50)) as _er_sk11a_bot:
    with BuildLine():
        Polyline(*_er_to_vec(_er_outer11a_points), close=True)
    make_face()

with BuildSketch(Plane.XY.offset(67.5)) as _er_sk11a_top:
    with BuildLine():
        Polyline(*_er_to_vec(_er_inner11a_points), close=True)
    make_face()

_er_chamfer_a = loft([_er_sk11a_bot.sketch, _er_sk11a_top.sketch])

# Chamfer ring B: loft from outer profile at z=50 to inner profile at z=67.5
with BuildSketch(Plane.XY.offset(50)) as _er_sk11b_bot:
    with BuildLine():
        Polyline(*_er_to_vec(_er_outer11b_points), close=True)
    make_face()

with BuildSketch(Plane.XY.offset(67.5)) as _er_sk11b_top:
    with BuildLine():
        Polyline(*_er_to_vec(_er_inner11b_points), close=True)
    make_face()

_er_chamfer_b = loft([_er_sk11b_bot.sketch, _er_sk11b_top.sketch])

_er_extrude11 = _er_chamfer_a + _er_chamfer_b

# ---------------------------------------------------------------------------
# SHAPE 12 — two through-holes in both Z directions (z=-120 to z=120)
# Hole A centred ~(540773.29, 233850.92), Hole B centred ~(540713.29, 233850.92)
# ---------------------------------------------------------------------------
_er_hole12a_points = [
    (540765.8203, 233850.1367),(540766.1719, 233848.6133),(540766.7969, 233847.168),
    (540767.7344, 233845.8984),(540768.9062, 233844.8633),(540770.2344, 233844.082),
    (540771.7188, 233843.5938),(540773.2812, 233843.418),(540774.8438, 233843.5938),
    (540776.3281, 233844.082),(540777.6953, 233844.8633),(540778.8672, 233845.8984),
    (540779.8047, 233847.168),(540780.4297, 233848.6133),(540780.7422, 233850.1367),
    (540780.7422, 233851.6992),(540780.4297, 233853.2422),(540779.8047, 233854.668),
    (540778.8672, 233855.9375),(540777.6953, 233856.9922),(540776.3281, 233857.7734),
    (540774.8438, 233858.2617),(540773.2812, 233858.418),(540771.7188, 233858.2617),
    (540770.2344, 233857.7734),(540768.9062, 233856.9922),(540767.7344, 233855.9375),
    (540766.7969, 233854.668),(540766.1719, 233853.2422),(540765.8203, 233851.6992),
]

_er_hole12b_points = [
    (540705.8203, 233850.1367),(540706.1719, 233848.6133),(540706.7969, 233847.168),
    (540707.7344, 233845.8984),(540708.9062, 233844.8633),(540710.2344, 233844.082),
    (540711.7188, 233843.5938),(540713.2812, 233843.418),(540714.8438, 233843.5938),
    (540716.3281, 233844.082),(540717.6953, 233844.8633),(540718.8672, 233845.8984),
    (540719.8047, 233847.168),(540720.4297, 233848.6133),(540720.7422, 233850.1367),
    (540720.7422, 233851.6992),(540720.4297, 233853.2422),(540719.8047, 233854.668),
    (540718.8672, 233855.9375),(540717.6953, 233856.9922),(540716.3281, 233857.7734),
    (540714.8438, 233858.2617),(540713.2812, 233858.418),(540711.7188, 233858.2617),
    (540710.2344, 233857.7734),(540708.9062, 233856.9922),(540707.7344, 233855.9375),
    (540706.7969, 233854.668),(540706.1719, 233853.2422),(540705.8203, 233851.6992),
]

with BuildSketch(Plane.XY.offset(-120)) as _er_sk12a:
    with BuildLine():
        Polyline(*_er_to_vec(_er_hole12a_points), close=True)
    make_face()
_er_hole12a = extrude(_er_sk12a.sketch, amount=240)

with BuildSketch(Plane.XY.offset(-120)) as _er_sk12b:
    with BuildLine():
        Polyline(*_er_to_vec(_er_hole12b_points), close=True)
    make_face()
_er_hole12b = extrude(_er_sk12b.sketch, amount=240)

# ---------------------------------------------------------------------------
# SHAPE 13 — small profile, extruded in -Z direction (downward cut)
# ---------------------------------------------------------------------------
_er_shape13_points = [
    (540282.4219, 233892.0312),
    (540286.7578, 233892.0312),
    (540285.3516, 233892.9688),
    (540283.9062, 233893.8672),
    (540282.4219, 233894.707),
]

with BuildSketch() as _er_sk13:
    with BuildLine():
        Polyline(*_er_to_vec(_er_shape13_points), close=True)
    make_face()
_er_cutter13 = extrude(_er_sk13.sketch, amount=6)

# ---------------------------------------------------------------------------
# SHAPE 14 — letter "R" text, font size 100mm, placed at origin, extruded 5mm
# ---------------------------------------------------------------------------
with BuildSketch() as _er_sk14:
    Text("R", font_size=120, align=(Align.MIN, Align.MAX))
_er_extrude14 = extrude(_er_sk14.sketch, amount=6)
_er_extrude14 = _er_extrude14.rotate(Axis.Z, 90)
_er_extrude14 = _er_extrude14.translate(Vector(432.32, 76.68, 95))

# ---------------------------------------------------------------------------
# SHAPE 15 — text 'TOP', font size 50mm, same position as R
# ---------------------------------------------------------------------------
with BuildSketch() as _er_sk15:
    Text("TOP", font_size=65, align=(Align.MIN, Align.MAX))
_er_extrude15 = extrude(_er_sk15.sketch, amount=6)
_er_extrude15 = _er_extrude15.rotate(Axis.Z, 180)
_er_extrude15 = _er_extrude15.translate(Vector(432.32 - 9, 108, 95))

# ---------------------------------------------------------------------------
# SHAPE 16 — text 'BOTTOM', font size 70mm, on bottom face (z=0), extruded downward 5mm
# ---------------------------------------------------------------------------
with BuildSketch(Plane.XY.offset(0)) as _er_sk16:
    Text("BOTTOM", font_size=70, align=(Align.MIN, Align.MAX))
_er_extrude16 = extrude(_er_sk16.sketch, amount=-6)
_er_extrude16 = _er_extrude16.rotate(Axis.X, 180)
_er_extrude16 = _er_extrude16.rotate(Axis.Z, 180)
_er_extrude16 = _er_extrude16.translate(Vector(447.75, 142, 0))

# ---------------------------------------------------------------------------
# SHAPE 17 — text 'RIGHT', font size 30mm, same plane as BOTTOM (z=0), extruded downward 5mm
# ---------------------------------------------------------------------------
with BuildSketch(Plane.XY.offset(0)) as _er_sk17:
    Text("RIGHT", font_size=30, align=(Align.MIN, Align.MAX))
_er_extrude17 = extrude(_er_sk17.sketch, amount=-6)
_er_extrude17 = _er_extrude17.rotate(Axis.X, 180)
_er_extrude17 = _er_extrude17.rotate(Axis.Z, 180)
_er_extrude17 = _er_extrude17.translate(Vector(750, 130, 0))

# ---------------------------------------------------------------------------
# SHAPE 18 — rectangular box, extruded 57.5mm (separate body)
# ---------------------------------------------------------------------------
_er_shape18_points = [
    (540808.2812, 233905.918),
    (540808.2812, 233798.1055),
    (540678.2812, 233798.1055),
    (540678.2812, 233905.918),
]

with BuildSketch() as _er_sk18:
    with BuildLine():
        Polyline(*_er_to_vec(_er_shape18_points), close=True)
    make_face()
_er_extrude18 = extrude(_er_sk18.sketch, amount=57.5)

# ---------------------------------------------------------------------------
# Final _er_result — fuse 1+2+3, cut 4, 5, 6, 7
# ---------------------------------------------------------------------------
_er_result_main = _er_extrude1 + _er_extrude2 + _er_extrude3 - _er_cutter - _er_extrude5 - _er_hollow_cylinder - _er_extrude7 - _er_extrude8 - _er_hole1 - _er_hole2 - _er_extrude10 - _er_extrude11 - _er_hole12a - _er_hole12b - _er_cutter13 - _er_extrude14 - _er_extrude15 - _er_extrude16 - _er_extrude17
_er_result = Compound([_er_result_main, _er_extrude18])


elbow_right = _er_result.translate((639.93, 1140.25, 0))

print("✓ Elbow Right built")

# ╔══════════════════════════════════════════════════════════════════════════════
# ASSEMBLY — All parts
# ╔══════════════════════════════════════════════════════════════════════════════

# ╔══════════════════════════════════════════════════════════════════════════════
# PART F — HANDS (HANDS.py — Hand1, Hand2, Hand3)
# ╔══════════════════════════════════════════════════════════════════════════════
import math as _math


# ══════════════════════════════════════════════════════════════════════════════
# SHARED ASSEMBLY ORIGIN  (= Hand1 centroid in world coords)
# All three models normalise to their own centroid, then are moved to sit at
# their correct world offset relative to this assembly origin.
# ══════════════════════════════════════════════════════════════════════════════

ASM_OX = 540716.7578
ASM_OY = 234098.9648

# ──────────────────────────────────────────────────────────────────────────────
# Helper: translate a completed Compound/Solid by a world offset
# ──────────────────────────────────────────────────────────────────────────────
def _offset(solid, world_ox, world_oy):
    """Move a solid built at its own local origin to the correct assembly position."""
    dx = world_ox - ASM_OX
    dy = world_oy - ASM_OY
    return solid.moved(Location((dx, dy, 0)))


# ══════════════════════════════════════════════════════════════════════════════
# ██   ██  █████  ███    ██ ██████      ██
# ██   ██ ██   ██ ████   ██ ██   ██    ███
# ███████ ███████ ██ ██  ██ ██   ██     ██
# ██   ██ ██   ██ ██  ██ ██ ██   ██     ██
# ██   ██ ██   ██ ██   ████ ██████      ██
# HAND 1 — End fitting (slot + cut + annular + chamfers + holes + text)
# Local centroid: ox=540716.7578  oy=234098.9648
# ══════════════════════════════════════════════════════════════════════════════

_h1_ox = 540716.7578
_h1_oy = 234098.9648

_slot_raw = [
    (541444.2188, 234148.9648, 50.0),(541449.8047, 234148.6523, 50.0),
    (541455.3516, 234147.7148, 50.0),(541460.7422, 234146.1719, 50.0),
    (541465.8984, 234144.0234, 50.0),(541470.8203, 234141.3086, 50.0),
    (541475.3906, 234138.0664, 50.0),(541479.5703, 234134.3359, 50.0),
    (541483.3203, 234130.1562, 50.0),(541486.5625, 234125.5664, 50.0),
    (541489.2578, 234120.6641, 50.0),(541491.4062, 234115.4883, 50.0),
    (541492.9688, 234110.0977, 50.0),(541493.9062, 234104.5703, 50.0),
    (541494.2188, 234098.9648, 50.0),(541493.8672, 234093.2031, 50.0),
    (541492.8906, 234087.5,    50.0),(541491.2109, 234081.9531, 50.0),
    (541488.9453, 234076.6406, 50.0),(541486.0547, 234071.6211, 50.0),
    (541482.6172, 234066.9727, 50.0),(541478.6719, 234062.7344, 50.0),
    (541474.2578, 234059.0039, 50.0),(541469.4531, 234055.8008, 50.0),
    (541464.2969, 234053.1836, 50.0),(541458.8672, 234051.1719, 50.0),
    (541453.2422, 234049.7852, 50.0),(541447.5,    234049.082,  50.0),
    (541441.7188, 234049.043,  50.0),(539989.2188, 234048.9648, 50.0),
    (539983.3984, 234049.3164, 50.0),(539977.6953, 234050.3125, 50.0),
    (539972.1094, 234051.9922, 50.0),(539966.7578, 234054.2969, 50.0),
    (539961.7578, 234057.207,  50.0),(539957.0703, 234060.6641, 50.0),
    (539952.8516, 234064.668,  50.0),(539949.1016, 234069.1211, 50.0),
    (539945.8984, 234073.9648, 50.0),(539943.3203, 234079.1602, 50.0),
    (539941.3281, 234084.6289, 50.0),(539939.9609, 234090.293,  50.0),
    (539939.2969, 234096.0742, 50.0),(539939.2969, 234101.875,  50.0),
    (539939.9609, 234107.6562, 50.0),(539941.3281, 234113.3203, 50.0),
    (539943.3203, 234118.7695, 50.0),(539945.8984, 234123.9648, 50.0),
    (539949.1016, 234128.8281, 50.0),(539952.8516, 234133.2812, 50.0),
    (539957.0703, 234137.2656, 50.0),(539961.7578, 234140.7422, 50.0),
    (539966.7578, 234143.6523, 50.0),(539972.1094, 234145.957,  50.0),
    (539977.6953, 234147.6172, 50.0),(539983.3984, 234148.6328, 50.0),
    (539989.2188, 234148.9648, 50.0),
]

_cut_raw = [
    (541494.2188, 234098.9648, 40.0),(541494.2188, 234198.9648, 40.0),
    (541493.9062, 234204.7266, 40.0),(541493.0078, 234210.4102, 40.0),
    (541491.5234, 234215.9766, 40.0),(541489.4531, 234221.3477, 40.0),
    (541486.8359, 234226.4648, 40.0),(541483.7109, 234231.3086, 40.0),
    (541480.0781, 234235.7812, 40.0),(541476.0156, 234239.8438, 40.0),
    (541471.5234, 234243.4766, 40.0),(541466.7188, 234246.6016, 40.0),
    (541466.7188, 234238.3789, 40.0),(541471.25,   234234.7852, 40.0),
    (541475.3516, 234230.6836, 40.0),(541478.8672, 234226.0938, 40.0),
    (541481.875,  234221.1328, 40.0),(541484.2188, 234215.8398, 40.0),
    (541485.9375, 234210.3125, 40.0),(541486.9531, 234204.6094, 40.0),
    (541487.2656, 234198.8281, 40.0),(541486.9141, 234193.0469, 40.0),
    (541485.8594, 234187.3438, 40.0),(541484.1016, 234181.8164, 40.0),
    (541481.7188, 234176.543,  40.0),(541478.7109, 234171.6016, 40.0),
    (541475.1172, 234167.0508, 40.0),(541471.0156, 234162.9492, 40.0),
    (541466.4844, 234159.3945, 40.0),(541461.5234, 234156.3867, 40.0),
    (541456.2109, 234154.0234, 40.0),(541450.7031, 234152.3047, 40.0),
    (541445.0,    234151.2695, 40.0),(541439.2188, 234150.918,  40.0),
    (541433.4375, 234151.2695, 40.0),(541427.7344, 234152.3047, 40.0),
    (541422.1875, 234154.0234, 40.0),(541416.9141, 234156.3867, 40.0),
    (541411.9531, 234159.3945, 40.0),(541407.3828, 234162.9492, 40.0),
    (541403.2812, 234167.0508, 40.0),(541399.7266, 234171.6016, 40.0),
    (541396.7188, 234176.543,  40.0),(541394.3359, 234181.8164, 40.0),
    (541392.5781, 234187.3438, 40.0),(541391.5234, 234193.0469, 40.0),
    (541391.1719, 234198.8281, 40.0),(541391.4844, 234204.6094, 40.0),
    (541392.5,    234210.3125, 40.0),(541394.2188, 234215.8398, 40.0),
    (541396.5625, 234221.1328, 40.0),(541399.5312, 234226.0938, 40.0),
    (541403.0859, 234230.6836, 40.0),(541407.1875, 234234.7852, 40.0),
    (541411.7188, 234238.3789, 40.0),(541411.7188, 234246.6016, 40.0),
    (541406.875,  234243.4766, 40.0),(541402.4219, 234239.8438, 40.0),
    (541398.3594, 234235.7812, 40.0),(541394.7266, 234231.3086, 40.0),
    (541391.6016, 234226.4648, 40.0),(541388.9844, 234221.3477, 40.0),
    (541386.9141, 234215.9766, 40.0),(541385.4297, 234210.4102, 40.0),
    (541384.5312, 234204.7266, 40.0),(541384.2188, 234198.9648, 40.0),
    (541383.9062, 234193.0859, 40.0),(541382.9297, 234187.5,    40.0),
    (541381.3672, 234182.0703, 40.0),(541379.1797, 234176.8555, 40.0),
    (541376.4453, 234171.9336, 40.0),(541373.125,  234167.3242, 40.0),
    (541369.3359, 234163.1445, 40.0),(541365.1172, 234159.3945, 40.0),
    (541360.4688, 234156.1719, 40.0),(541355.5078, 234153.4766, 40.0),
    (541350.2344, 234151.3672, 40.0),(541344.8047, 234149.8633, 40.0),
    (541339.2188, 234148.9648, 40.0),
]

def _h1_norm(pts):
    return [(x - _h1_ox, y - _h1_oy) for x, y, _ in pts]

_slot_pts = _h1_norm(_slot_raw)
_cut_pts  = _h1_norm(_cut_raw)

# --- Slot (Body 1) ---
with BuildPart() as _sp:
    with BuildSketch(Plane(origin=(0, 0, 0), z_dir=(0, 0, 1))):
        with BuildLine(): Polyline(*_slot_pts, close=True)
        make_face()
    extrude(amount=50.0)
_h1_joined = _sp.part

# --- Cut (Body 2) ---
with BuildPart() as _cp:
    with BuildSketch(Plane(origin=(0, 0, 10), z_dir=(0, 0, 1))):
        with BuildLine(): Polyline(*_cut_pts, close=True)
        make_face()
    extrude(amount=30.0)
_h1_joined = _h1_joined.fuse(_cp.part)

# --- Extrude ring (Body 3) ---
_extrude_raw = [
    (541466.7188,234228.0273),(541470.2344,234224.2383),(541473.2031,234220.0586),
    (541475.625,234215.5078),(541477.4609,234210.6836),(541478.6328,234205.6836),
    (541479.1797,234200.5664),(541479.0625,234195.4102),(541478.2812,234190.3125),
    (541476.8359,234185.3711),(541474.7656,234180.6641),(541472.1094,234176.2305),
    (541468.9453,234172.207),(541465.2344,234168.5938),(541461.1328,234165.5078),
    (541456.6406,234162.9688),(541451.875,234161.0352),(541446.9141,234159.7266),
    (541441.7969,234159.0625),(541436.6406,234159.0625),(541431.5234,234159.7266),
    (541426.5625,234161.0352),(541421.7969,234162.9688),(541417.3047,234165.5078),
    (541413.1641,234168.5938),(541409.4922,234172.207),(541406.2891,234176.2305),
    (541403.6719,234180.6641),(541401.6016,234185.3711),(541400.1562,234190.3125),
    (541399.375,234195.4102),(541399.2578,234200.5664),(541399.7656,234205.6836),
    (541400.9766,234210.6836),(541402.7734,234215.5078),(541405.2344,234220.0586),
    (541408.2031,234224.2383),(541411.7188,234228.0273),
]
_extrude_pts = [(x - _h1_ox, y - _h1_oy) for x, y in _extrude_raw]
with BuildPart() as _ep:
    with BuildSketch(Plane(origin=(0, 0, 0), z_dir=(0, 0, 1))):
        with BuildLine(): Polyline(*_extrude_pts, close=True)
        make_face()
    extrude(amount=30.0)
_h1_extrude_solid = _ep.part

# --- Annular ring (Body 4) ---
def _h1_sort_angle(pts):
    cx = sum(p[0] for p in pts)/len(pts); cy = sum(p[1] for p in pts)/len(pts)
    return sorted(pts, key=lambda p: _math.atan2(p[1]-cy, p[0]-cx))

_outer_raw = [
    (541466.7188,234238.3789),(541471.25,234234.7852),(541475.3516,234230.6836),
    (541478.8672,234226.0938),(541481.875,234221.1328),(541484.2188,234215.8398),
    (541485.9375,234210.3125),(541486.9531,234204.6094),(541487.2656,234198.8281),
    (541486.9141,234193.0469),(541484.1016,234181.8164),(541481.7188,234176.543),
    (541478.7109,234171.6016),(541475.1172,234167.0508),(541471.0156,234162.9492),
    (541466.4844,234159.3945),(541461.5234,234156.3867),(541456.2109,234154.0234),
    (541450.7031,234152.3047),(541445.0,234151.2695),(541439.2188,234150.918),
    (541433.4375,234151.2695),(541427.7344,234152.3047),(541422.1875,234154.0234),
    (541416.9141,234156.3867),(541411.9531,234159.3945),(541407.3828,234162.9492),
    (541403.2812,234167.0508),(541399.7266,234171.6016),(541396.7188,234176.543),
    (541394.3359,234181.8164),(541392.5781,234187.3438),(541391.5234,234193.0469),
    (541391.1719,234198.8281),(541391.4844,234204.6094),(541392.5,234210.3125),
    (541394.2188,234215.8398),(541396.5625,234221.1328),(541399.5312,234226.0938),
    (541403.0859,234230.6836),(541407.1875,234234.7852),(541411.7188,234238.3789),
]
_inner_raw = [
    (541411.7188,234228.0273),(541408.2031,234224.2383),(541405.2344,234220.0586),
    (541402.7734,234215.5078),(541400.9766,234210.6836),(541399.7656,234205.6836),
    (541399.2578,234200.5664),(541399.375,234195.4102),(541400.1562,234190.3125),
    (541401.6016,234185.3711),(541403.6719,234180.6641),(541406.2891,234176.2305),
    (541409.4922,234172.207),(541413.1641,234168.5938),(541417.3047,234165.5078),
    (541421.7969,234162.9688),(541426.5625,234161.0352),(541431.5234,234159.7266),
    (541436.6406,234159.0625),(541441.7969,234159.0625),(541446.9141,234159.7266),
    (541451.875,234161.0352),(541456.6406,234162.9688),(541461.1328,234165.5078),
    (541465.2344,234168.5938),(541468.9453,234172.207),(541472.1094,234176.2305),
    (541474.7656,234180.6641),(541476.8359,234185.3711),(541478.2812,234190.3125),
    (541479.0625,234195.4102),(541479.1797,234200.5664),(541478.6328,234205.6836),
    (541477.4609,234210.6836),(541475.625,234215.5078),(541473.2031,234220.0586),
    (541470.2344,234224.2383),(541466.7188,234228.0273),
]
_outer_pts = _h1_sort_angle([(x-_h1_ox, y-_h1_oy) for x,y in _outer_raw])
_inner_pts = _h1_sort_angle([(x-_h1_ox, y-_h1_oy) for x,y in _inner_raw])
with BuildPart() as _ap:
    with BuildSketch(Plane(origin=(0,0,10), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_outer_pts, close=True)
        make_face()
    extrude(amount=30.0)
    with BuildSketch(Plane(origin=(0,0,10), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_inner_pts, close=True)
        make_face()
    extrude(amount=30.0, mode=Mode.SUBTRACT)
_h1_joined = _h1_joined.fuse(_ap.part)

# --- New extrude (Body 5) ---
_new_extrude_raw = [
    (541466.7188,234246.6016),(541466.7188,234238.3789),(541466.7188,234235.6055),
    (541466.7188,234232.9688),(541466.7188,234230.4297),(541466.7188,234228.0273),
    (541470.2344,234224.2383),(541473.2031,234220.0586),(541475.625,234215.5078),
    (541477.4609,234210.6836),(541478.6328,234205.6836),(541479.1797,234200.5664),
    (541479.0625,234195.4102),(541478.2812,234190.3125),(541476.8359,234185.3711),
    (541474.7656,234180.6641),(541472.1094,234176.2305),(541468.9453,234172.207),
    (541465.2344,234168.5938),(541461.1328,234165.5078),(541456.6406,234162.9688),
    (541451.875,234161.0352),(541446.9141,234159.7266),(541441.7969,234159.0625),
    (541436.6406,234159.0625),(541431.5234,234159.7266),(541426.5625,234161.0352),
    (541421.7969,234162.9688),(541417.3047,234165.5078),(541413.1641,234168.5938),
    (541409.4922,234172.207),(541406.2891,234176.2305),(541403.6719,234180.6641),
    (541401.6016,234185.3711),(541400.1562,234190.3125),(541399.375,234195.4102),
    (541399.2578,234200.5664),(541399.7656,234205.6836),(541400.9766,234210.6836),
    (541402.7734,234215.5078),(541405.2344,234220.0586),(541408.2031,234224.2383),
    (541411.7188,234228.0273),(541411.7188,234230.4297),(541411.7188,234232.9688),
    (541411.7188,234235.6055),(541411.7188,234238.3789),(541411.7188,234246.6016),
]
_ne_pts = [(x-_h1_ox, y-_h1_oy) for x,y in _new_extrude_raw]
with BuildPart() as _nep:
    with BuildSketch(Plane(origin=(0,0,10), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_ne_pts, close=True)
        make_face()
    extrude(amount=30.0)
_h1_joined = _h1_joined.fuse(_nep.part)

# --- Chamfer ring (loft outer→inner) ---
_chamfer_outer_raw = [
    (541466.7188,234238.3789),(541471.25,234234.7852),(541475.3516,234230.6836),
    (541478.8672,234226.0938),(541481.875,234221.1328),(541484.2188,234215.8398),
    (541485.9375,234210.3125),(541486.9531,234204.6094),(541487.2656,234198.8281),
    (541486.9141,234193.0469),(541485.8594,234187.3438),(541484.1016,234181.8164),
    (541481.7188,234176.543),(541478.7109,234171.6016),(541475.1172,234167.0508),
    (541471.0156,234162.9492),(541466.4844,234159.3945),(541461.5234,234156.3867),
    (541456.2109,234154.0234),(541450.7031,234152.3047),(541445.0,234151.2695),
    (541439.2188,234150.918),(541433.4375,234151.2695),(541427.7344,234152.3047),
    (541422.1875,234154.0234),(541416.9141,234156.3867),(541411.9531,234159.3945),
    (541407.3828,234162.9492),(541403.2812,234167.0508),(541399.7266,234171.6016),
    (541396.7188,234176.543),(541394.3359,234181.8164),(541392.5781,234187.3438),
    (541391.5234,234193.0469),(541391.1719,234198.8281),(541391.4844,234204.6094),
    (541392.5,234210.3125),(541394.2188,234215.8398),(541396.5625,234221.1328),
    (541403.0859,234230.6836),(541399.5312,234226.0938),(541407.1875,234234.7852),
    (541411.7188,234238.3789),
]
_chamfer_inner_raw = [
    (541466.7188,234228.0273),(541470.2344,234224.2383),(541473.2031,234220.0586),
    (541475.625,234215.5078),(541477.4609,234210.6836),(541478.6328,234205.6836),
    (541479.1797,234200.5664),(541479.0625,234195.4102),(541478.2812,234190.3125),
    (541476.8359,234185.3711),(541474.7656,234180.6641),(541472.1094,234176.2305),
    (541468.9453,234172.207),(541465.2344,234168.5938),(541461.1328,234165.5078),
    (541456.6406,234162.9688),(541451.875,234161.0352),(541446.9141,234159.7266),
    (541441.7969,234159.0625),(541436.6406,234159.0625),(541431.5234,234159.7266),
    (541426.5625,234161.0352),(541421.7969,234162.9688),(541417.3047,234165.5078),
    (541413.1641,234168.5938),(541409.4922,234172.207),(541406.2891,234176.2305),
    (541403.6719,234180.6641),(541401.6016,234185.3711),(541400.1562,234190.3125),
    (541399.375,234195.4102),(541399.2578,234200.5664),(541399.7656,234205.6836),
    (541400.9766,234210.6836),(541405.2344,234220.0586),(541408.2031,234224.2383),
    (541402.7734,234215.5078),(541411.7188,234228.0273),
]
_co_pts = [(x-_h1_ox, y-_h1_oy) for x,y in _chamfer_outer_raw]
_ci_pts = [(x-_h1_ox, y-_h1_oy) for x,y in _chamfer_inner_raw]
with BuildPart() as _chp:
    with BuildSketch(Plane(origin=(0,0,10), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_co_pts, close=True)
        make_face()
    with BuildSketch(Plane(origin=(0,0,20), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_ci_pts, close=True)
        make_face()
    loft()
_chamfer_solid = _chp.part
_chamfer_mirrored = mirror(_chamfer_solid, about=Plane(origin=(0,0,25), z_dir=(0,0,1)))

_h1_joined = _h1_joined.fuse(_nep.part)
_h1_joined = _h1_joined.cut(_chamfer_solid).cut(_chamfer_mirrored)

# --- New extrude 2 cut ---
_ne2_raw = [
    (541466.7188,234246.6016),(541466.7188,234238.3789),(541466.7188,234235.6055),
    (541466.7188,234232.9688),(541466.7188,234230.4297),(541466.7188,234228.0273),
    (541470.2344,234224.2383),(541473.2031,234220.0586),(541475.625,234215.5078),
    (541477.4609,234210.6836),(541478.6328,234205.6836),(541479.1797,234200.5664),
    (541479.0625,234195.4102),(541478.2812,234190.3125),(541476.8359,234185.3711),
    (541474.7656,234180.6641),(541472.1094,234176.2305),(541468.9453,234172.207),
    (541465.2344,234168.5938),(541461.1328,234165.5078),(541456.6406,234162.9688),
    (541451.875,234161.0352),(541446.9141,234159.7266),(541441.7969,234159.0625),
    (541436.6406,234159.0625),(541431.5234,234159.7266),(541426.5625,234161.0352),
    (541421.7969,234162.9688),(541417.3047,234165.5078),(541413.1641,234168.5938),
    (541409.4922,234172.207),(541406.2891,234176.2305),(541403.6719,234180.6641),
    (541401.6016,234185.3711),(541400.1562,234190.3125),(541399.375,234195.4102),
    (541399.2578,234200.5664),(541399.7656,234205.6836),(541400.9766,234210.6836),
    (541402.7734,234215.5078),(541405.2344,234220.0586),(541408.2031,234224.2383),
    (541411.7188,234228.0273),(541411.7188,234230.4297),(541411.7188,234232.9688),
    (541411.7188,234235.6055),(541411.7188,234238.3789),(541411.7188,234246.6016),
]
_ne2_pts = [(x-_h1_ox, y-_h1_oy) for x,y in _ne2_raw]
with BuildPart() as _ne2p:
    with BuildSketch(Plane(origin=(0,0,0), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_ne2_pts, close=True)
        make_face()
    extrude(amount=50.0)
_h1_joined = _h1_joined.cut(_ne2p.part)

# --- Hollow disk 1 cut ---
def _sort_angle_2d(pts):
    cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
    return sorted(pts, key=lambda p: _math.atan2(p[1]-cy, p[0]-cx))

_disk_outer_raw = [
    (540010.5078,234059.3359),(540015.1953,234062.2461),(540019.5312,234065.7227),
    (540023.3984,234069.6875),(540026.7188,234074.1211),(540029.4922,234078.9062),
    (540031.6406,234084.0234),(540033.1641,234089.3359),(540034.0234,234094.8242),
    (540034.1797,234100.3516),(540032.5,234111.2891),(540033.6719,234105.8789),
    (540030.6641,234116.5039),(540028.2031,234121.4648),(540025.1172,234126.0938),
    (540021.5234,234130.293),(540017.4219,234134.0234),(540008.0078,234139.8438),
    (540012.8906,234137.2266),(540002.8516,234141.8555),(539997.5,234143.2031),
    (539991.9922,234143.8867),(539986.4453,234143.8867),(539980.9375,234143.2031),
    (539975.5859,234141.8555),(539965.5078,234137.2266),(539970.3906,234139.8438),
    (539956.9141,234130.293),(539961.0156,234134.0234),(540005.4688,234057.0117),
    (540000.1953,234055.332),(539994.7266,234054.3164),(539989.2188,234053.9648),
    (539983.6719,234054.3164),(539978.2422,234055.332),(539967.9297,234059.3359),
    (539972.9688,234057.0117),(539963.2031,234062.2461),(539958.9062,234065.7227),
    (539955.0391,234069.6875),(539951.7188,234074.1211),(539948.9453,234078.9062),
    (539946.7578,234084.0234),(539945.2734,234089.3359),(539944.4141,234094.8242),
    (539944.2188,234100.3516),(539944.7656,234105.8789),(539945.9375,234111.2891),
    (539947.7734,234116.5039),(539950.2344,234121.4648),(539953.3203,234126.0938),
]
_disk_inner_raw = [
    (539984.7266,234128.6328),(539980.3906,234127.6367),(539976.2109,234125.9961),
    (539972.3047,234123.75),(539968.8281,234120.957),(539965.7422,234117.6758),
    (539963.2422,234113.9648),(539961.2891,234109.9414),(539959.9609,234105.6445),
    (539959.2969,234101.2109),(539959.2969,234096.7383),(539959.9609,234092.3047),
    (539961.2891,234088.0078),(539963.2422,234083.9648),(539965.7422,234080.2734),
    (539968.8281,234076.9727),(539972.3047,234074.1797),(539976.2109,234071.9336),
    (539980.3906,234070.3125),(539984.7266,234069.3164),(539989.2188,234068.9648),
    (539993.6719,234069.3164),(539998.0469,234070.3125),(540002.2266,234071.9336),
    (540006.1328,234074.1797),(539989.2188,234128.9648),(539993.6719,234128.6328),
    (539998.0469,234127.6367),(540002.2266,234125.9961),(540006.1328,234123.75),
    (540009.6094,234120.957),(540012.6562,234117.6758),(540015.1953,234113.9648),
    (540017.1484,234109.9414),(540018.4766,234105.6445),(540019.1406,234101.2109),
    (540019.1406,234096.7383),(540018.4766,234092.3047),(540017.1484,234088.0078),
    (540015.1953,234083.9648),(540012.6562,234080.2734),(540009.6094,234076.9727),
]
_do_pts = _sort_angle_2d([(x-_h1_ox, y-_h1_oy) for x,y in _disk_outer_raw])
_di_pts = _sort_angle_2d([(x-_h1_ox, y-_h1_oy) for x,y in _disk_inner_raw])
with BuildPart() as _d1p:
    with BuildSketch(Plane(origin=(0,0,45), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_do_pts, close=True)
        make_face()
    extrude(amount=10.0)
    with BuildSketch(Plane(origin=(0,0,45), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_di_pts, close=True)
        make_face()
    extrude(amount=10.0, mode=Mode.SUBTRACT)
_h1_joined = _h1_joined.cut(_d1p.part)

# --- Hollow disk 2 cut ---
_disk2_outer_raw = [
    (541400.2344,234121.4648),(541403.3203,234126.0938),(541406.9141,234130.293),
    (541411.0156,234134.0234),(541415.5078,234137.2266),(541425.5859,234141.8555),
    (541420.3906,234139.8438),(541430.9375,234143.2031),(541436.4453,234143.8867),
    (541441.9922,234143.8867),(541447.5,234143.2031),(541452.8516,234141.8555),
    (541458.0078,234139.8438),(541462.8906,234137.2266),(541467.4219,234134.0234),
    (541471.5234,234130.293),(541475.1172,234126.0938),(541478.2031,234121.4648),
    (541480.6641,234116.5039),(541483.6719,234105.8789),(541482.5,234111.2891),
    (541484.1797,234100.3516),(541484.0234,234094.8242),(541483.1641,234089.3359),
    (541481.6406,234084.0234),(541479.4922,234078.9062),(541476.7188,234074.1211),
    (541473.3984,234069.6875),(541469.5312,234065.7227),(541465.1953,234062.2461),
    (541460.5078,234059.3359),(541455.4688,234057.0117),(541450.1953,234055.332),
    (541444.7266,234054.3164),(541439.2188,234053.9648),(541433.6719,234054.3164),
    (541422.9688,234057.0117),(541428.2422,234055.332),(541417.9297,234059.3359),
    (541413.2031,234062.2461),(541408.9062,234065.7227),(541405.0391,234069.6875),
    (541401.7188,234074.1211),(541398.9453,234078.9062),(541396.7578,234084.0234),
    (541395.2734,234089.3359),(541394.4141,234094.8242),(541394.2188,234100.3516),
    (541394.7656,234105.8789),(541395.9375,234111.2891),(541397.7734,234116.5039),
]
_disk2_inner_raw = [
    (541434.7266,234069.3164),(541439.2188,234068.9648),(541443.6719,234069.3164),
    (541448.0469,234070.3125),(541452.2266,234071.9336),(541456.1328,234074.1797),
    (541459.6094,234076.9727),(541462.6562,234080.2734),(541465.1953,234083.9648),
    (541467.1484,234088.0078),(541468.4766,234092.3047),(541469.1406,234096.7383),
    (541469.1406,234101.2109),(541468.4766,234105.6445),(541467.1484,234109.9414),
    (541465.1953,234113.9648),(541462.6562,234117.6758),(541459.6094,234120.957),
    (541456.1328,234123.75),(541452.2266,234125.9961),(541448.0469,234127.6367),
    (541430.3906,234070.3125),(541426.2109,234071.9336),(541422.3047,234074.1797),
    (541418.8281,234076.9727),(541415.7422,234080.2734),(541413.2422,234083.9648),
    (541411.2891,234088.0078),(541409.9609,234092.3047),(541409.2969,234096.7383),
    (541409.2969,234101.2109),(541409.9609,234105.6445),(541411.2891,234109.9414),
    (541413.2422,234113.9648),(541415.7422,234117.6758),(541418.8281,234120.957),
    (541422.3047,234123.75),(541426.2109,234125.9961),(541430.3906,234127.6367),
    (541434.7266,234128.6328),(541439.2188,234128.9648),(541443.6719,234128.6328),
]
_d2o_pts = _sort_angle_2d([(x-_h1_ox, y-_h1_oy) for x,y in _disk2_outer_raw])
_d2i_pts = _sort_angle_2d([(x-_h1_ox, y-_h1_oy) for x,y in _disk2_inner_raw])
with BuildPart() as _d2p:
    with BuildSketch(Plane(origin=(0,0,45), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_d2o_pts, close=True)
        make_face()
    extrude(amount=10.0)
    with BuildSketch(Plane(origin=(0,0,45), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_d2i_pts, close=True)
        make_face()
    extrude(amount=10.0, mode=Mode.SUBTRACT)
_h1_joined = _h1_joined.cut(_d2p.part)

# --- Hole 1 cut ---
_hole_raw = [
    (541447.6172,234088.418),(541449.7656,234090.5469),(541451.3672,234093.1055),
    (541452.3828,234095.9766),(541452.6953,234098.9648),(541452.3828,234101.9727),
    (541451.3672,234104.8242),(541449.7656,234107.3828),(541447.6172,234109.5312),
    (541445.0781,234111.1328),(541442.2266,234112.1289),(541439.2188,234112.4805),
    (541436.2109,234112.1289),(541433.3594,234111.1328),(541430.7812,234109.5312),
    (541427.0703,234104.8242),(541426.0547,234101.9727),(541425.7031,234098.9648),
    (541428.6719,234107.3828),(541427.0703,234093.1055),(541426.0547,234095.9766),
    (541445.0781,234086.8164),(541442.2266,234085.8203),(541439.2188,234085.4688),
    (541436.2109,234085.8203),(541433.3594,234086.8164),(541430.7812,234088.418),
    (541428.6719,234090.5469),
]
_hcx = sum(p[0] for p in _hole_raw)/len(_hole_raw)
_hcy = sum(p[1] for p in _hole_raw)/len(_hole_raw)
_hole_pts = sorted([(x-_h1_ox, y-_h1_oy) for x,y in _hole_raw],
    key=lambda p: _math.atan2(p[1]-(_hcy-_h1_oy), p[0]-(_hcx-_h1_ox)))
with BuildPart() as _hp:
    with BuildSketch(Plane(origin=(0,0,31.5), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_hole_pts, close=True)
        make_face()
    extrude(amount=18.5)
_h1_joined = _h1_joined.cut(_hp.part)

# --- Hole 2 cut ---
_hole2_raw = [
    (539980.7812,234088.418),(539983.3594,234086.8164),(539986.2109,234085.8203),
    (539989.2188,234085.4688),(539992.2266,234085.8203),(539995.0781,234086.8164),
    (539997.6172,234088.418),(539999.7656,234090.5469),(540001.3672,234093.1055),
    (540002.3828,234095.9766),(539978.6719,234090.5469),(539977.0703,234093.1055),
    (539976.0547,234095.9766),(539975.7031,234098.9648),(539976.0547,234101.9727),
    (539977.0703,234104.8242),(539978.6719,234107.3828),(539980.7812,234109.5312),
    (539983.3594,234111.1328),(539986.2109,234112.1289),(539992.2266,234112.1289),
    (539989.2188,234112.4805),(539995.0781,234111.1328),(539997.6172,234109.5312),
    (540001.3672,234104.8242),(539999.7656,234107.3828),(540002.6953,234098.9648),
    (540002.3828,234101.9727),
]
_h2cx = sum(p[0] for p in _hole2_raw)/len(_hole2_raw)
_h2cy = sum(p[1] for p in _hole2_raw)/len(_hole2_raw)
_hole2_pts = sorted([(x-_h1_ox, y-_h1_oy) for x,y in _hole2_raw],
    key=lambda p: _math.atan2(p[1]-(_h2cy-_h1_oy), p[0]-(_h2cx-_h1_ox)))
with BuildPart() as _h2p:
    with BuildSketch(Plane(origin=(0,0,31.5), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_hole2_pts, close=True)
        make_face()
    extrude(amount=18.5)
_h1_joined = _h1_joined.cut(_h2p.part)

# --- Cut2 (hexagon 1) ---
_cut2_pts = [(x-_h1_ox, y-_h1_oy) for x,y in [
    (539989.2188,234065.7812),(539960.4688,234082.3828),(539960.4688,234115.5664),
    (539989.2188,234132.168),(540017.9688,234115.5664),(540017.9688,234082.3828),
]]
with BuildPart() as _c2p:
    with BuildSketch(Plane(origin=(0,0,0), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_cut2_pts, close=True)
        make_face()
    extrude(amount=30.0)
_h1_joined = _h1_joined.cut(_c2p.part)

# --- Cut3 (hexagon 2) ---
_cut3_pts = [(x-_h1_ox, y-_h1_oy) for x,y in [
    (541439.2188,234065.7812),(541410.4688,234082.3828),(541410.4688,234115.5664),
    (541439.2188,234132.168),(541467.9688,234115.5664),(541467.9688,234082.3828),
]]
with BuildPart() as _c3p:
    with BuildSketch(Plane(origin=(0,0,0), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_cut3_pts, close=True)
        make_face()
    extrude(amount=30.0)
_h1_joined = _h1_joined.cut(_c3p.part)

# --- Text: BOTTOM (bottom face) ---
with BuildPart() as _tbp:
    with BuildSketch(Plane(origin=(-200,0,0), z_dir=(0,0,1))):
        Text("BOTTOM", font_size=50, align=(Align.CENTER, Align.CENTER))
    extrude(amount=5.0)
_tb_solid = mirror(_tbp.part, about=Plane(origin=(-200,0,0), z_dir=(0,1,0)))
_h1_joined = _h1_joined.cut(_tb_solid)

# --- Text: TOP LEFT (top face) ---
with BuildPart() as _ttp:
    with BuildSketch(Plane(origin=(-200,0,50), z_dir=(0,0,1))):
        Text("TOP                       LEFT", font_size=50, align=(Align.CENTER, Align.CENTER))
    extrude(amount=-5.0)
_h1_joined = _h1_joined.cut(_ttp.part)

print(f"Hand1 volume : {_h1_joined.volume:,.1f} mm³")

# Apply world offset (Hand1 is the assembly origin — no translation needed)
hand1_solid = _h1_joined.translate((1133, 1499.92, 0))


# ══════════════════════════════════════════════════════════════════════════════
# ██   ██  █████  ███    ██ ██████     ██████
# ██   ██ ██   ██ ████   ██ ██   ██        ██
# ███████ ███████ ██ ██  ██ ██   ██     █████
# ██   ██ ██   ██ ██  ██ ██ ██   ██    ██
# ██   ██ ██   ██ ██   ████ ██████     ███████
# HAND 2 — Bracket body (55-pt profile + arc cut + chamfer loft)
# Local centroid: ox=541430.9375  oy=234188.6328
# World offset from Hand1: (+714.18, +89.67)
# ══════════════════════════════════════════════════════════════════════════════

_h2_ox = 541430.9375
_h2_oy = 234188.6328

_h2_raw = [
    (541342.3828,234153.9648),(541342.3828,234229.5508),(541342.6953,234235.1367),
    (541343.6328,234240.6641),(541345.1562,234246.0547),(541347.3047,234251.2305),
    (541350.0391,234256.1523),(541353.2812,234260.7227),(541356.9922,234264.9023),
    (541361.1719,234268.6328),(541365.7812,234271.875),(541370.6641,234274.5898),
    (541375.8594,234276.7383),(541381.25,234278.2812),(541386.7578,234279.2188),
    (541392.3828,234279.5508),(541469.4922,234279.5508),(541475.0781,234279.2188),
    (541480.625,234278.2812),(541486.0156,234276.7383),(541491.1719,234274.5898),
    (541496.0938,234271.875),(541500.6641,234268.6328),(541504.8438,234264.9023),
    (541508.5938,234260.7227),(541511.8359,234256.1523),(541514.5312,234251.2305),
    (541516.6797,234246.0547),(541518.2422,234240.6641),(541519.1797,234235.1367),
    (541519.4922,234229.5508),(541519.4922,234137.7734),(541519.1406,234131.9727),
    (541518.1641,234126.2695),(541516.4844,234120.7031),(541514.1797,234115.3711),
    (541511.2891,234110.3516),(541507.8516,234105.6836),(541503.8672,234101.4648),
    (541499.4141,234097.7148),(541499.2188,234103.9062),(541498.3203,234110.0391),
    (541496.7188,234116.0352),(541494.4922,234121.8164),(541491.6016,234127.3047),
    (541488.1641,234132.4414),(541484.1016,234137.1484),(541479.6094,234141.3867),
    (541474.6094,234145.0781),(541469.2578,234148.1836),(541463.5938,234150.6836),
    (541457.6562,234152.5391),(541451.6016,234153.7109),(541445.3906,234154.1797),
    (541439.2188,234153.9648),
]
_h2_pts = [(x-_h2_ox, y-_h2_oy) for x,y in _h2_raw]

with BuildPart() as _h2b:
    with BuildSketch(Plane(origin=(0,0,0), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_h2_pts, close=True)
        make_face()
    extrude(amount=40.0)
_h2_solid = _h2b.part

def _p2(x, y): return (x-_h2_ox, y-_h2_oy)

# Body 2 cut (47-segment polyline)
_b2_pts = [
    (541429.453,234146.298),(541429.453,234153.965),(541424.102,234155.469),
    (541418.984,234157.617),(541414.141,234160.352),(541409.648,234163.672),
    (541405.625,234167.48),(541402.07,234171.758),(541399.062,234176.445),
    (541396.641,234181.445),(541394.844,234186.719),(541393.672,234192.148),
    (541393.203,234197.695),(541393.359,234203.262),(541394.219,234208.75),
    (541395.742,234214.102),(541397.852,234219.238),(541400.625,234224.082),
    (541403.945,234228.555),(541407.734,234232.598),(541412.031,234236.133),
    (541416.719,234239.141),(541416.719,234254.648),(541410.859,234251.914),
    (541405.312,234248.555),(541400.156,234244.609),(541395.469,234240.137),
    (541391.289,234235.195),(541387.695,234229.824),(541384.648,234224.102),
    (541382.266,234218.066),(541380.547,234211.836),(541379.492,234205.43),
    (541379.141,234198.965),(541378.867,234193.77),(541378.008,234188.613),
    (541376.523,234183.613),(541374.492,234178.809),(541371.914,234174.277),
    (541368.828,234170.059),(541365.273,234166.25),(541361.289,234162.871),
    (541356.953,234159.961),(541352.305,234157.578),(541347.422,234155.762),
    (541342.383,234154.531),(541342.383,234140.0),
]
with BuildPart() as _b2p:
    with BuildSketch(Plane(origin=(0,0,7.5), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*[_p2(x,y) for x,y in _b2_pts], close=True)
        make_face()
    extrude(amount=32.5)
_h2_solid = _h2_solid.cut(_b2p.part)

# Body 3 cut (arc profile)
with BuildPart() as _b3p:
    with BuildSketch(Plane(origin=(0,0,7.5), z_dir=(0,0,1))):
        with BuildLine():
            Line(_p2(541449.023,234151.003), _p2(541492.168,234109.978))
            RadiusArc(_p2(541492.168,234109.978), _p2(541499.414,234100.215), -35.5)
            Line(_p2(541499.414,234100.215), _p2(541499.414,234148.965))
            Line(_p2(541499.414,234148.965), _p2(541499.258,234148.965))
            Line(_p2(541499.258,234148.965), _p2(541499.258,234198.965))
            Line(_p2(541499.258,234198.965), _p2(541498.906,234205.43))
            Line(_p2(541498.906,234205.43),  _p2(541497.891,234211.836))
            Line(_p2(541497.891,234211.836), _p2(541496.172,234218.066))
            Line(_p2(541496.172,234218.066), _p2(541493.75,234224.102))
            Line(_p2(541493.75,234224.102),  _p2(541490.742,234229.824))
            Line(_p2(541490.742,234229.824), _p2(541487.109,234235.195))
            Line(_p2(541487.109,234235.195), _p2(541482.93,234240.137))
            Line(_p2(541482.93,234240.137),  _p2(541478.242,234244.609))
            Line(_p2(541478.242,234244.609), _p2(541473.125,234248.555))
            Line(_p2(541473.125,234248.555), _p2(541467.578,234251.914))
            Line(_p2(541467.578,234251.914), _p2(541461.719,234254.648))
            Line(_p2(541461.719,234254.648), _p2(541461.719,234239.141))
            Line(_p2(541461.719,234239.141), _p2(541466.406,234236.133))
            Line(_p2(541466.406,234236.133), _p2(541470.664,234232.598))
            Line(_p2(541470.664,234232.598), _p2(541474.492,234228.555))
            Line(_p2(541474.492,234228.555), _p2(541477.812,234224.082))
            Line(_p2(541477.812,234224.082), _p2(541480.547,234219.258))
            Line(_p2(541480.547,234219.258), _p2(541482.695,234214.121))
            Line(_p2(541482.695,234214.121), _p2(541484.219,234208.77))
            Line(_p2(541484.219,234208.77),  _p2(541485.039,234203.281))
            Line(_p2(541485.039,234203.281), _p2(541485.234,234197.734))
            Line(_p2(541485.234,234197.734), _p2(541484.766,234192.188))
            Line(_p2(541484.766,234192.188), _p2(541483.594,234186.758))
            Line(_p2(541483.594,234186.758), _p2(541481.797,234181.484))
            Line(_p2(541481.797,234181.484), _p2(541479.414,234176.484))
            Line(_p2(541479.414,234176.484), _p2(541476.406,234171.816))
            Line(_p2(541476.406,234171.816), _p2(541472.852,234167.52))
            Line(_p2(541472.852,234167.52),  _p2(541468.828,234163.711))
            Line(_p2(541468.828,234163.711), _p2(541464.336,234160.391))
            Line(_p2(541464.336,234160.391), _p2(541459.531,234157.637))
            Line(_p2(541459.531,234157.637), _p2(541454.375,234155.508))
            Line(_p2(541454.375,234155.508), _p2(541449.023,234153.984))
            Line(_p2(541449.023,234153.984), _p2(541449.023,234151.003))
        make_face()
    extrude(amount=32.5)
_h2_solid = _h2_solid.cut(_b3p.part)

# Body 5 cut
_b5_pts = [
    (541399.856,234153.965),(541399.856,234140.0),(541481.105,234140.0),
    (541482.344,234138.945),(541486.562,234134.414),(541490.273,234129.434),
    (541493.398,234124.082),(541495.898,234118.418),(541497.773,234112.5),
    (541498.945,234106.406),(541499.414,234100.215),(541499.414,234148.965),
    (541499.258,234148.965),(541499.258,234198.965),(541498.906,234205.43),
    (541497.891,234211.836),(541496.172,234218.066),(541493.75,234224.102),
    (541490.742,234229.824),(541487.109,234235.195),(541482.93,234240.137),
    (541478.242,234244.609),(541473.125,234248.555),(541467.578,234251.914),
    (541461.719,234254.648),(541461.719,234225.879),(541465.234,234222.48),
    (541468.281,234218.633),(541470.703,234214.395),(541472.539,234209.863),
    (541473.75,234205.098),(541474.258,234200.234),(541474.102,234195.332),
    (541473.242,234190.527),(541471.758,234185.859),(541469.609,234181.465),
    (541466.875,234177.402),(541463.594,234173.75),(541459.844,234170.605),
    (541455.703,234168.008),(541451.211,234166.016),(541446.523,234164.668),
    (541441.68,234163.984),(541436.758,234163.984),(541431.914,234164.668),
    (541427.227,234166.016),(541422.734,234168.008),(541418.594,234170.605),
    (541414.844,234173.75),(541411.562,234177.402),(541408.828,234181.465),
    (541406.68,234185.859),(541405.156,234190.527),(541404.336,234195.332),
    (541404.18,234200.234),(541404.688,234205.098),(541405.859,234209.863),
    (541407.695,234214.395),(541410.156,234218.633),(541413.203,234222.48),
    (541416.719,234225.879),(541416.719,234239.141),(541416.719,234254.648),
    (541410.859,234251.914),(541405.312,234248.555),(541400.156,234244.609),
    (541395.469,234240.137),(541391.289,234235.195),(541387.695,234229.824),
    (541384.648,234224.102),(541382.266,234218.066),(541380.547,234211.836),
    (541379.492,234205.43),(541379.141,234198.965),(541378.867,234193.77),
    (541378.008,234188.613),(541376.523,234183.613),(541374.492,234178.809),
    (541371.914,234174.277),(541368.828,234170.059),(541365.273,234166.25),
    (541361.289,234162.871),(541356.953,234159.961),(541352.305,234157.578),
    (541347.422,234155.762),(541342.383,234154.531),(541342.383,234153.965),
]
with BuildPart() as _b5p:
    with BuildSketch(Plane(origin=(0,0,7.5), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*[_p2(x,y) for x,y in _b5_pts], close=True)
        make_face()
    extrude(amount=32.5)
_h2_solid = _h2_solid.cut(_b5p.part)

# Chamfer loft (fuse)
import math as _mc

def _h2_sort_angle(pts):
    cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
    return sorted(pts, key=lambda p: _mc.atan2(p[1]-cy, p[0]-cx))

def _h2_resample(pts, n):
    pts=list(pts)+[pts[0]]; dists=[0]
    for i in range(1,len(pts)):
        dx=pts[i][0]-pts[i-1][0]; dy=pts[i][1]-pts[i-1][1]
        dists.append(dists[-1]+_mc.sqrt(dx*dx+dy*dy))
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

_h2_ch_outer = [
    (541416.7188,234239.1406),(541461.7188,234239.1406),(541412.0312,234236.1328),
    (541407.7344,234232.5977),(541403.9453,234228.5547),(541400.625,234224.082),
    (541397.8516,234219.2383),(541395.7422,234214.1016),(541394.2188,234208.75),
    (541393.3594,234203.2617),(541393.2031,234197.6953),(541393.6719,234192.1484),
    (541394.8438,234186.7188),(541396.6406,234181.4453),(541399.0625,234176.4453),
    (541402.0703,234171.7578),(541405.625,234167.4805),(541409.6484,234163.6719),
    (541414.1406,234160.3516),(541418.9844,234157.6172),(541424.1016,234155.4688),
    (541429.4531,234153.9648),(541434.375,234153.9648),(541439.2188,234153.9648),
    (541444.2188,234154.1992),(541449.0234,234153.9844),(541454.375,234155.5078),
    (541459.5312,234157.6367),(541464.3359,234160.3906),(541468.8281,234163.7109),
    (541472.8516,234167.5195),(541476.4062,234171.8164),(541479.4141,234176.4844),
    (541481.7969,234181.4844),(541483.5938,234186.7578),(541484.7656,234192.1875),
    (541485.2344,234197.7344),(541485.0391,234203.2812),(541484.2188,234208.7695),
    (541482.6953,234214.1211),(541480.5469,234219.2578),(541477.8125,234224.082),
    (541474.4922,234228.5547),(541470.6641,234232.5977),(541466.4062,234236.1328),
]
_h2_ch_inner = [
    (541416.7188,234232.0508),(541412.6172,234228.8281),(541408.9453,234225.1172),
    (541405.7812,234220.957),(541403.2031,234216.4258),(541401.25,234211.6016),
    (541399.9219,234206.543),(541399.2969,234201.3672),(541399.2969,234196.1523),
    (541401.4062,234185.957),(541400.0,234190.9961),(541403.3984,234181.1523),
    (541406.0156,234176.6406),(541409.2188,234172.5195),(541412.9297,234168.8281),
    (541417.0703,234165.6641),(541421.5625,234163.0664),(541426.4062,234161.0742),
    (541431.4453,234159.7266),(541436.6016,234159.0625),(541441.8359,234159.0625),
    (541446.9922,234159.7266),(541452.0312,234161.0742),(541456.8359,234163.0664),
    (541461.3672,234165.6641),(541465.5078,234168.8281),(541469.2188,234172.5195),
    (541472.3828,234176.6406),(541475.0391,234181.1523),(541477.0312,234185.957),
    (541478.3984,234190.9961),(541479.1016,234196.1523),(541479.1406,234201.3672),
    (541478.4766,234206.543),(541477.1875,234211.6016),(541475.1953,234216.4258),
    (541472.6172,234220.957),(541469.4922,234225.1172),(541465.8203,234228.8281),
    (541461.7188,234232.0508),
]
_N = 50
_h2_co = _h2_resample(_h2_sort_angle(_h2_ch_outer), _N)
_h2_ci = _h2_resample(_h2_sort_angle(_h2_ch_inner), _N)
_h2_co_n = [(x-_h2_ox, y-_h2_oy) for x,y in _h2_co]
_h2_ci_n = [(x-_h2_ox, y-_h2_oy) for x,y in _h2_ci]

with BuildPart() as _h2_chp:
    with BuildSketch(Plane(origin=(0,0,7.5), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_h2_co_n, close=True)
        make_face()
    with BuildSketch(Plane(origin=(0,0,15.0), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_h2_ci_n, close=True)
        make_face()
    loft(ruled=True)
_h2_solid = _h2_solid.fuse(_h2_chp.part)

print(f"Hand2 volume : {_h2_solid.volume:,.1f} mm³")

# Apply world offset
hand2_solid = _offset(_h2_solid, _h2_ox, _h2_oy).translate((1133, 1499.92, 0))


# ══════════════════════════════════════════════════════════════════════════════
# ██   ██  █████  ███    ██ ██████     ██████
# ██   ██ ██   ██ ████   ██ ██   ██        ██
# ███████ ███████ ██ ██  ██ ██   ██     █████
# ██   ██ ██   ██ ██  ██ ██ ██   ██         ██
# ██   ██ ██   ██ ██   ████ ██████     ██████
# HAND 3 — Long slot bar (1450 mm × 100 mm slot + 10× holes + chamfers + text)
# Local centroid: ox=540559.9415  oy=234155.4785
# World offset from Hand1: (−156.82, +56.51)
# ══════════════════════════════════════════════════════════════════════════════

_h3_ox = 540559.9415
_h3_oy = 234155.4785

# --- Left and right semicircles → slot profile ---
_h3_left = [
    (539834.9609,234253.9648),(539829.1406,234253.6328),(539823.3984,234252.6172),
    (539817.8516,234250.957),(539812.5,234248.6523),(539807.4609,234245.7422),
    (539802.8125,234242.2656),(539798.5938,234238.2812),(539794.8438,234233.8281),
    (539791.6406,234228.9648),(539789.0234,234223.7695),(539787.0312,234218.3203),
    (539785.7031,234212.6562),(539785.0391,234206.875),(539785.0391,234201.0742),
    (539785.7031,234195.293),(539787.0312,234189.6289),(539789.0234,234184.1602),
    (539791.6406,234178.9648),(539794.8438,234174.1211),(539798.5938,234169.668),
    (539802.8125,234165.6641),(539807.4609,234162.207),(539812.5,234159.2969),
    (539817.8516,234156.9922),(539823.3984,234155.3125),(539829.1406,234154.3164),
    (539834.9609,234153.9648),
]
_h3_right_orig = [
    (541284.9609,234253.9648),(541290.7422,234253.6328),(541296.4844,234252.6172),
    (541302.0312,234250.957),(541307.3828,234248.6523),(541312.4219,234245.7422),
    (541317.0703,234242.2656),(541321.3281,234238.2812),(541325.0391,234233.8281),
    (541328.2422,234228.9648),(541330.8594,234223.7695),(541332.8516,234218.3203),
    (541334.1797,234212.6562),(541334.8438,234206.875),(541334.8438,234201.0742),
    (541334.1797,234195.293),(541332.8516,234189.6289),(541330.8594,234184.1602),
    (541328.2422,234178.9648),(541325.0391,234174.1211),(541321.3281,234169.668),
    (541317.0703,234165.6641),(541312.4219,234162.207),(541307.3828,234159.2969),
    (541302.0312,234156.9922),(541296.4844,234155.3125),(541290.7422,234154.3164),
    (541284.9609,234153.9648),
]
_h3_raw = _h3_left + list(reversed(_h3_right_orig))
_h3_pts = [(x-_h3_ox, y-_h3_oy) for x,y in _h3_raw]

with BuildPart() as _h3b:
    with BuildSketch(Plane(origin=(0,0,0), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_h3_pts, close=True)
        make_face()
    extrude(amount=50.0)
_h3_solid = _h3b.part

# --- Hole row (10× circular holes, XZ-plane profile extruded 120 mm in +Y) ---
_h3_hole_raw = [
    (541088.7109,18.5048),(541090.2344,19.6967),(541091.4453,21.25),
    (541092.1875,23.0589),(541092.4609,25.0),(541092.1875,26.9412),
    (541091.4453,28.75),(541090.2344,30.3033),(541088.7109,31.4952),
    (541086.875,32.2445),(541084.9609,32.5),(541083.0078,32.2445),
    (541081.2109,31.4952),(541079.6484,30.3033),(541078.4375,28.75),
    (541077.6953,26.9412),(541077.4609,25.0),(541077.6953,23.0589),
    (541078.4375,21.25),(541079.6484,19.6967),(541081.2109,18.5048),
    (541083.0078,17.7556),(541084.9609,17.5),(541086.875,17.7556),
]
_h3_hole_pts = [(-(x-_h3_ox), z) for x,z in _h3_hole_raw]
_h3_hole_y = 234153.9648 - _h3_oy

with BuildPart() as _h3hp:
    with BuildSketch(Plane(origin=(0,_h3_hole_y,0), z_dir=(0,1,0), x_dir=(-1,0,0))):
        with BuildLine(): Polyline(*_h3_hole_pts, close=True)
        make_face()
    extrude(amount=120.0)
_h3_hole_one = _h3hp.part
_h3_all_holes = _h3_hole_one
for i in range(1, 10):
    _h3_all_holes = _h3_all_holes.fuse(_h3_hole_one.moved(Location((-i*50,0,0))))
_h3_solid = _h3_solid.cut(_h3_all_holes)

# --- Extrude row (10× circles, +X direction) ---
_h3_ext2_raw = [
    (540031.2109,31.4952),(540029.6484,30.3033),(540028.4375,28.75),
    (540027.6953,26.9412),(540027.4609,25.0),(540027.6953,23.0589),
    (540028.4375,21.25),(540029.6484,19.6967),(540031.2109,18.5048),
    (540033.0078,17.7556),(540034.9609,17.5),(540036.875,17.7556),
    (540038.7109,18.5048),(540040.2344,19.6967),(540041.4453,21.25),
    (540042.1875,23.0589),(540042.4609,25.0),(540042.1875,26.9412),
    (540041.4453,28.75),(540040.2344,30.3033),(540038.7109,31.4952),
    (540036.875,32.2445),(540034.9609,32.5),(540033.0078,32.2445),
]
_h3_ext2_pts = [(-(x-_h3_ox), z) for x,z in _h3_ext2_raw]
with BuildPart() as _h3ep:
    with BuildSketch(Plane(origin=(0,_h3_hole_y,0), z_dir=(0,1,0), x_dir=(-1,0,0))):
        with BuildLine(): Polyline(*_h3_ext2_pts, close=True)
        make_face()
    extrude(amount=120.0)
_h3_ext2_one = _h3ep.part
_h3_all_ext2 = _h3_ext2_one
for i in range(1, 10):
    _h3_all_ext2 = _h3_all_ext2.fuse(_h3_ext2_one.moved(Location((i*50,0,0))))
_h3_solid = _h3_solid.cut(_h3_all_ext2)

# --- Text: TOP RIGHT (bottom face, Z=0) ---
# Y offset +48.49 mm centres the text on the slot body in local space
_h3_text_y = 48.49
with BuildPart() as _h3t2p:
    with BuildSketch(Plane(origin=(-285, _h3_text_y, 0), z_dir=(0,0,1))):
        Text("TOP                          RIGHT", font_size=65, align=(Align.CENTER, Align.CENTER))
    extrude(amount=5.0)
_h3_t2 = mirror(_h3t2p.part, about=Plane(origin=(-285, _h3_text_y, 0), z_dir=(0,1,0)))
_h3_solid = _h3_solid.cut(_h3_t2)

# --- Chamfer 1 (left end) ---
import math as _mc2

def _h3_sort_a(pts):
    cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
    return sorted(pts, key=lambda p: _mc2.atan2(p[1]-cy, p[0]-cx))

def _h3_resamp(pts, n):
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

_ch1_outer = [
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
_ch1_inner = [
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
_h3N = 50
_ch1_o = [(x-_h3_ox, y-_h3_oy) for x,y in _h3_resamp(_h3_sort_a(_ch1_outer), _h3N)]
_ch1_i = [(x-_h3_ox, y-_h3_oy) for x,y in _h3_resamp(_h3_sort_a(_ch1_inner), _h3N)]
with BuildPart() as _ch1p:
    with BuildSketch(Plane(origin=(0,0,0), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_ch1_o, close=True)
        make_face()
    with BuildSketch(Plane(origin=(0,0,13.5), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_ch1_i, close=True)
        make_face()
    loft(ruled=True)
_h3_solid = _h3_solid.cut(_ch1p.part)

# --- Chamfer 2 (right end) ---
_ch2_outer = [
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
_ch2_inner = [
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
_ch2_o = [(x-_h3_ox, y-_h3_oy) for x,y in _h3_resamp(_h3_sort_a(_ch2_outer), _h3N)]
_ch2_i = [(x-_h3_ox, y-_h3_oy) for x,y in _h3_resamp(_h3_sort_a(_ch2_inner), _h3N)]
with BuildPart() as _ch2p:
    with BuildSketch(Plane(origin=(0,0,0), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_ch2_o, close=True)
        make_face()
    with BuildSketch(Plane(origin=(0,0,13.5), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_ch2_i, close=True)
        make_face()
    loft(ruled=True)
_h3_solid = _h3_solid.cut(_ch2p.part)

# --- Hole cylinder 2 (top face, -Z) ---
_h3_hole2_raw = [
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
_h3_hole2_pts = _h3_sort_a([(x-_h3_ox, y-_h3_oy) for x,y in _h3_hole2_raw])
with BuildPart() as _h3h2p:
    with BuildSketch(Plane(origin=(0,0,50), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_h3_hole2_pts, close=True)
        make_face()
    extrude(amount=-35.0)
_h3_solid = _h3_solid.cut(_h3h2p.part)

# --- Extrude cylinder 2 (right end, top face, -Z) ---
_h3_ecyl2_raw = [
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
_h3_ecyl2_pts = _h3_sort_a([(x-_h3_ox, y-_h3_oy) for x,y in _h3_ecyl2_raw])
with BuildPart() as _h3ec2p:
    with BuildSketch(Plane(origin=(0,0,50), z_dir=(0,0,1))):
        with BuildLine(): Polyline(*_h3_ecyl2_pts, close=True)
        make_face()
    extrude(amount=-35.0)
_h3_solid = _h3_solid.cut(_h3ec2p.part)

# --- Text: BOTTOM (top face, Z=50) ---
with BuildPart() as _h3txtp:
    with BuildSketch(Plane(origin=(-167, _h3_text_y, 50), z_dir=(0,0,1))):
        Text("BOTTOM", font_size=65, align=(Align.CENTER, Align.CENTER))
    extrude(amount=-5.0)
_h3_solid = _h3_solid.cut(_h3txtp.part)

print(f"Hand3 volume : {_h3_solid.volume:,.1f} mm³")

# Apply world offset
hand3_solid = _offset(_h3_solid, _h3_ox, _h3_oy).translate((1133, 1499.92, 0))



print("✓ Hands built")

# ╔══════════════════════════════════════════════════════════════════════════════
# ASSEMBLY — All parts
# ╔══════════════════════════════════════════════════════════════════════════════

show(
    main_body,
    positioned_pump,
    body_top_positioned,
    elbow_left,
    elbow_right,
    hand1_solid,
    hand2_solid,
    hand3_solid,
    names=["Main_Body", "Pump_Mount", "Body_Top", "Elbow_Left", "Elbow_Right",
           "Hand1", "Hand2", "Hand3"],
    colors=["#5588AA", "#CC7733", "#AA5577", "#77AA55", "#AA7755",
            "#4A90D9", "#E67E22", "#27AE60"],
    reset_camera=Camera.RESET,
)

print("\n✓ Assembly complete")
print(f"  Main Body   — origin (0, 0, 0)")
print(f"  Pump Mount  — translated ({pump_offset_x}, {pump_offset_y}, {pump_offset_z})")
print(f"  Body Top    — translated (0, +795, 0)")
print(f"  Elbow Left  — translated (731.72, +919.71, 0)")
print(f"  Elbow Right — translated (639.93, +1140.25, 0)")
print(f"  Hand1       — assembly origin")
print(f"  Hand2       — offset (+714.18, +89.67)")
print(f"  Hand3       — offset (-156.82, +56.51)")

# ╔══════════════════════════════════════════════════════════════════════════════
# EXPORT — Single STEP file to Desktop
# ╔══════════════════════════════════════════════════════════════════════════════
import os
from pathlib import Path

_desktop = Path.home() / "Desktop"
_step_path = _desktop / "Assembly.step"

_assembly_compound = Compound(
    label="Assembly",
    children=[
        Compound(label="Main_Body",   children=[main_body]),
        Compound(label="Pump_Mount",  children=[positioned_pump]),
        Compound(label="Body_Top",    children=[body_top_positioned]),
        Compound(label="Elbow_Left",  children=[elbow_left]),
        Compound(label="Elbow_Right", children=[elbow_right]),
        Compound(label="Hand1",       children=[hand1_solid]),
        Compound(label="Hand2",       children=[hand2_solid]),
        Compound(label="Hand3",       children=[hand3_solid]),
    ]
)

export_step(_assembly_compound, str(_step_path))
print(f"\n✓ STEP exported to: {_step_path}")