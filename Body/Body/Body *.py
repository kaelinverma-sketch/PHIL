from build123d import *
from ocp_vscode import show
import math

# ═══════════════════════════════════════════════════════════════════════════════
# 1. LARGE BOX with all cavity cuts
# ═══════════════════════════════════════════════════════════════════════════════
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

# Plate cut
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

# ═══════════════════════════════════════════════════════════════════════════════
# 2. BACK BOX with cylinder cuts and small holes
# ═══════════════════════════════════════════════════════════════════════════════
cylinders = [(754.91, 749.96), (1205.92, 749.96)]

back_box_l  =  350.94
back_box_h  =  750.00
back_box_d  =  377.50
back_box_x  =  805.0
back_box_z  =    0.0
back_box_plane = Plane(origin=(0, 790 - 377.5, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))

cyl2_r  = 321.63 / 2
hole3_r = 151.31 / 2
hole3_positions = [(754.98, 100.01), (1205.94, 100.01)]

with BuildPart() as back_box_base:
    with BuildSketch(back_box_plane):
        with Locations((back_box_x + back_box_l / 2, -(back_box_z + back_box_h / 2))):
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

# ═══════════════════════════════════════════════════════════════════════════════
# 4. DISC CUTS on main body
# ═══════════════════════════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════════════════════════
# 5. RECTANGLE CUT on top face
# ═══════════════════════════════════════════════════════════════════════════════
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



# ═══════════════════════════════════════════════════════════════════════════════
# 3. ARC HOLLOW CYLINDERS: 187 deg anti-clockwise from +Z, 10mm thick in +Y
# ═══════════════════════════════════════════════════════════════════════════════
import math

arc_outer_r  = 1333.63 / 2
arc_inner_r  = 1273.85 / 2
arc_thickness = 10.0       # mm in +Y
arc_degrees  = 187.0

# Sketch plane on XZ at ring_y, normal +Y
# local X = world X, local Y = world -Z
# world +Z = sketch angle 270 deg
# anti-clockwise in world = decreasing sketch angle
# 187 deg anti-clockwise from +Z: 270 → 270 - 187 = 83 deg
SK_START = 270.0
SK_END   = 270.0 - arc_degrees  # 83.0

def make_arc_pts(cx, cz, r, a_start, a_end):
    a_mid = (a_start + a_end) / 2
    return (
        Vector(cx + r * math.cos(math.radians(a_start)), -cz + r * math.sin(math.radians(a_start))),
        Vector(cx + r * math.cos(math.radians(a_mid)),   -cz + r * math.sin(math.radians(a_mid))),
        Vector(cx + r * math.cos(math.radians(a_end)),   -cz + r * math.sin(math.radians(a_end))),
    )

# Single arc ring at C1 (x=754.91) as separate body
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

# Mirrored arc ring at C2 (clockwise, 270 → 457)
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

# ═══════════════════════════════════════════════════════════════════════════════
# 6. COMBINE ALL
# ═══════════════════════════════════════════════════════════════════════════════
with BuildPart() as final_body:
    add(after_rect_cut.part)
    add(back_box.part)
    add(arc_ring_c1.part, mode=Mode.SUBTRACT)
    add(arc_ring_c2.part, mode=Mode.SUBTRACT)

# New cylinder d=151.31mm, depth=367.5mm at x=754.98, z=100, separate body
new_cyl_r     = 151.31 / 2
new_cyl_depth = 367.5
new_cyl_plane = Plane(origin=(0, 790 - 367.5, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))

with BuildPart() as final_body2:
    add(final_body.part)
    # C1 side
    with BuildSketch(new_cyl_plane):
        with Locations((754.98, -100.0)):
            Circle(new_cyl_r)
    extrude(amount=new_cyl_depth, both=False, mode=Mode.SUBTRACT)
    # C2 side (mirrored)
    with BuildSketch(new_cyl_plane):
        with Locations((1205.94, -100.0)):
            Circle(new_cyl_r)
    extrude(amount=new_cyl_depth, both=False, mode=Mode.SUBTRACT)

# 2 holes d=240mm and 2 holes d=173.85mm, all through in Y direction
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

# 2 through holes d=35mm at x=1910.94, z=480.01 and z=1020
holes_35 = [(1910.94, 480.01), (1910.94, 1020.0), (50.0, 480.01), (50.0, 1020.0)]

with BuildPart() as final_body4:
    add(final_body3.part)
    with BuildSketch(Plane.XZ.offset(0)):
        for cx, cz in holes_35:
            with Locations((cx, cz)):
                Circle(35.0 / 2)
    extrude(amount=-width, both=False, mode=Mode.SUBTRACT)

# Profile points (X, Z coords — sketch on XZ plane, extrude in +Y)
profile_pts = [
    Vector(0, 0),
    Vector(50, 0),
    Vector(78.75, 16.6),
    Vector(78.75, 49.8),
    Vector(50, 66.4),
    Vector(0, 66.4),
]

# Original planes (left/front side)
plane1  = Plane(origin=(1013.67, 725, 700), x_dir=(0, 0, -1), z_dir=(0, 1, 0))
plane2  = Plane(origin=(0,       725, 513.2),  x_dir=(1, 0, 0),  z_dir=(0, 1, 0))
plane3  = Plane(origin=(366.8,   725, 0),      x_dir=(0, 0, 1),  z_dir=(0, 1, 0))

# Mirrored planes (right side of same face, x_dir flipped)
plane1m = Plane(origin=(1960.94, 725, 1053.2), x_dir=(-1, 0, 0), z_dir=(0, 1, 0))
plane2m = Plane(origin=(1960.94, 725, 513.2),  x_dir=(-1, 0, 0), z_dir=(0, 1, 0))
plane3m = Plane(origin=(1594.14, 725, 0),      x_dir=(0, 0, -1), z_dir=(0, 1, 0))

# Mirror pts for planes 1m & 2m: negate Y (local Y flips from -Z to +Z)
profile_pts_m12 = [Vector(p.X, -p.Y) for p in profile_pts]
# Mirror pts for plane3m: negate Y (local Y flips from +X to -X)
profile_pts_m3  = [Vector(p.X, -p.Y) for p in profile_pts]

with BuildPart() as final_body5:
    add(final_body4.part)
    # Originals
    for plane in [plane1, plane2, plane3]:
        with BuildSketch(plane):
            with BuildLine():
                Polyline(*profile_pts, close=True)
            make_face()
        extrude(amount=25, mode=Mode.SUBTRACT)
    # Mirrors 1 & 2
    for plane in [plane1m, plane2m]:
        with BuildSketch(plane):
            with BuildLine():
                Polyline(*profile_pts_m12, close=True)
            make_face()
        extrude(amount=25, mode=Mode.SUBTRACT)
    # Copy of yellow profile at x=1527.73, same orientation
    plane3_copy = Plane(origin=(1527.73, 725, 0), x_dir=(0, 0, 1), z_dir=(0, 1, 0))
    with BuildSketch(plane3_copy):
        with BuildLine():
            Polyline(*profile_pts, close=True)
        make_face()
    extrude(amount=25, mode=Mode.SUBTRACT)

# 3 holes d=35mm on back face (Y=790), depth=127.5mm in -Y, coords are (X, Z)
back_holes = [(854.99, 219.5), (1105.94, 219.5), (980.47, 650.0)]
back_hole_plane = Plane(origin=(0, 790, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))

with BuildPart() as final_body6:
    add(final_body5.part)
    with BuildSketch(back_hole_plane):
        for cx, cz in back_holes:
            with Locations((cx, -cz)):
                Circle(35.0 / 2)
    extrude(amount=-127.5, both=False, mode=Mode.SUBTRACT)

# Profile 1 cut into final body
with BuildPart() as final_body7:
    add(final_body6.part)
    with BuildSketch(plane1):
        with BuildLine():
            Polyline(*profile_pts, close=True)
        make_face()
    extrude(amount=25, mode=Mode.SUBTRACT)

# New box cut: 146.99mm (X) x 100mm (Z) x 377.5mm (-Y)
with BuildPart() as final_body8:
    add(final_body7.part)
    box_plane = Plane(origin=(906.95, 790, 800), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
    with BuildSketch(box_plane):
        with Locations((146.99 / 2, 100.0 / 2)):
            Rectangle(146.99, 100.0)
    extrude(amount=-377.5, mode=Mode.SUBTRACT)

# Profile copy and mirror as extrude cuts
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

# Hole d=157.02mm on bottom face (z=0) at x=980.64, y=595, depth=700mm
with BuildPart() as final_body10:
    add(final_body9.part)
    with BuildSketch(Plane.XY):
        with Locations((980.64, 595)):
            Circle(157.02 / 2)
    extrude(amount=700, mode=Mode.SUBTRACT)

# Hole d=244.07mm on bottom face (z=0) at x=980.64, y=595, depth=150mm
with BuildPart() as final_body11:
    add(final_body10.part)
    with BuildSketch(Plane.XY):
        with Locations((980.64, 595)):
            Circle(244.07 / 2)
    extrude(amount=150, mode=Mode.SUBTRACT)

# Chamfer on 244.07mm hole entry at bottom face: height=37mm, slant=42mm
chamfer_h = 37.0
chamfer_slant = 42.0
chamfer_w = math.sqrt(chamfer_slant**2 - chamfer_h**2)
hole_r = 244.07 / 2

# Chamfer as standalone solid for positioning analysis
with BuildPart() as chamfer_solid:
    with BuildSketch(Plane(origin=(980.64, 595, chamfer_h), x_dir=(1, 0, 0), z_dir=(0, 1, 0))):
        with BuildLine():
            Polyline(
                Vector(hole_r, 0),
                Vector(hole_r + chamfer_w, chamfer_h),
                Vector(hole_r, chamfer_h),
                close=True,
            )
        make_face()
    revolve(axis=Axis((980.64, 595, 0), (0, 0, 1)), revolution_arc=360)

with BuildPart() as final_body12:
    add(final_body11.part)
    with BuildSketch(Plane(origin=(980.64, 595, chamfer_h), x_dir=(1, 0, 0), z_dir=(0, 1, 0))):
        with BuildLine():
            Polyline(
                Vector(hole_r, 0),
                Vector(hole_r + chamfer_w, chamfer_h),
                Vector(hole_r, chamfer_h),
                close=True,
            )
        make_face()
    revolve(axis=Axis((980.64, 595, 0), (0, 0, 1)), revolution_arc=360, mode=Mode.SUBTRACT)

# Second chamfer: d=244.07mm → d=157.02mm over height=85mm, standalone solid
chamfer2_h       = 85.0
chamfer2_r_start = 244.07 / 2   # 122.035mm
chamfer2_r_end   = 157.02 / 2   #  78.51mm

with BuildPart() as chamfer2_solid:
    with BuildSketch(Plane(origin=(980.64, 595, 235), x_dir=(1, 0, 0), z_dir=(0, 1, 0))):
        with BuildLine():
            Polyline(
                Vector(chamfer2_r_end,   0),
                Vector(chamfer2_r_start, chamfer2_h),
                Vector(chamfer2_r_end,   chamfer2_h),
                close=True,
            )
        make_face()
    revolve(axis=Axis((980.64, 595, 0), (0, 0, 1)), revolution_arc=360)

with BuildPart() as final_body13:
    add(final_body12.part)
    with BuildSketch(Plane(origin=(980.64, 595, 235), x_dir=(1, 0, 0), z_dir=(0, 1, 0))):
        with BuildLine():
            Polyline(
                Vector(chamfer2_r_end,   0),
                Vector(chamfer2_r_start, chamfer2_h),
                Vector(chamfer2_r_end,   chamfer2_h),
                close=True,
            )
        make_face()
    revolve(axis=Axis((980.64, 595, 0), (0, 0, 1)), revolution_arc=360, mode=Mode.SUBTRACT)

# Cylinder d=47mm, h=98.5mm with 45° slant cut at z=75mm
with BuildPart() as cyl_body:
    with BuildSketch(Plane.XY):
        with Locations((980.64, 595)):
            Circle(47.0 / 2)
    extrude(amount=98.5)
    # 45° cut: plane passes through centre at z=75, normal tilted 45° in XZ plane
    slant_plane = Plane(
        origin=(980.64, 595, 75),
        x_dir=(0, 1, 0),
        z_dir=(math.sqrt(2) / 2, 0, math.sqrt(2) / 2),
    )
    with BuildSketch(slant_plane):
        Rectangle(500, 500)
    extrude(amount=150, mode=Mode.SUBTRACT)

# Curved cylinder: d=47mm swept along arc R=122mm, 75deg each way in XY plane at z=75
# Same centre used for both directions — path goes from reverse-end → start → forward-end
R_arc  = 122.0
arc_cx = 980.64
arc_cy = 595.0 + R_arc   # 717.0  (centre offset +R in Y, tangent at 270° = +X)
arc_z  = 75.0

# Forward arc: 270° → 345° CCW (+X direction)
arc_mid_x = arc_cx + R_arc * math.cos(math.radians(307.5))
arc_mid_y = arc_cy + R_arc * math.sin(math.radians(307.5))
arc_end_x = arc_cx + R_arc * math.cos(math.radians(345.0))
arc_end_y = arc_cy + R_arc * math.sin(math.radians(345.0))

# Reverse arc: 270° → 195° CW (−X direction), same centre
rev_end_x = arc_cx + R_arc * math.cos(math.radians(195.0))
rev_end_y = arc_cy + R_arc * math.sin(math.radians(195.0))
rev_mid_x = arc_cx + R_arc * math.cos(math.radians(232.5))
rev_mid_y = arc_cy + R_arc * math.sin(math.radians(232.5))

# Tangent at reverse-end (195°) pointing CCW toward start (270°)
rev_tan_x = -math.sin(math.radians(195))   #  sin(15°) ≈  0.2588
rev_tan_y =  math.cos(math.radians(195))   # -cos(15°) ≈ -0.9659

# Combined path: reverse-end → start → forward-end
with BuildLine() as arc_path:
    ThreePointArc(
        (rev_end_x, rev_end_y, arc_z),
        (rev_mid_x, rev_mid_y, arc_z),
        (980.64,    595,       arc_z),
    )
    ThreePointArc(
        (980.64,    595,       arc_z),
        (arc_mid_x, arc_mid_y, arc_z),
        (arc_end_x, arc_end_y, arc_z),
    )

with BuildPart() as arc_cyl_body:
    # Profile at the reverse-end, normal = tangent direction at that point
    with BuildSketch(Plane(
        origin=(rev_end_x, rev_end_y, arc_z),
        x_dir=(0, 0, 1),
        z_dir=(rev_tan_x, rev_tan_y, 0),
    )):
        Circle(47.0 / 2)
    sweep(path=arc_path)
    # Same 45° slant cut as orange cylinder — removes the −X extension, keeps original +X arc
    with BuildSketch(slant_plane):
        Rectangle(500, 500)
    extrude(amount=-150, mode=Mode.SUBTRACT)
    # Fillet the flat end cap face edge (smallest circle = end cap of the sweep)
    fillet(arc_cyl_body.edges().filter_by(GeomType.CIRCLE).sort_by(SortBy.LENGTH)[0:1], radius=20)

with BuildPart() as joined_cyl:
    add(cyl_body.part)
    add(arc_cyl_body.part)

# Move combined cylinder: +50.07 in X, -101 in Y from current position
with BuildPart() as joined_cyl_moved:
    add(joined_cyl.part.moved(Location((50.07, -101, 0))))

# Rotate around Z (X→Y) about the cylinder's current centre position
cyl_cx = 980.64 + 50.07   # 1030.71
cyl_cy = 595.0  - 101.0   # 494.0

with BuildPart() as joined_cyl_rotated:
    add(joined_cyl_moved.part.moved(
        Location((cyl_cx, cyl_cy, 0)) *
        Rotation(0, 0, 30) *
        Location((-cyl_cx, -cyl_cy, 0))
    ))

# Replicate combined cylinder at 120° and 240° around centre of 244.07mm hole
hole_cx, hole_cy = 980.64, 595.0

# Centres of each replica (original centre rotated around hole)
_dx = cyl_cx - hole_cx   # 50.07
_dy = cyl_cy - hole_cy   # -101.0
c120_x = hole_cx + _dx * math.cos(math.radians(120)) - _dy * math.sin(math.radians(120))
c120_y = hole_cy + _dx * math.sin(math.radians(120)) + _dy * math.cos(math.radians(120))
c240_x = hole_cx + _dx * math.cos(math.radians(240)) - _dy * math.sin(math.radians(240))
c240_y = hole_cy + _dx * math.sin(math.radians(240)) + _dy * math.cos(math.radians(240))

with BuildPart() as cyl_replica_120:
    add(joined_cyl_rotated.part.moved(
        Location((c120_x, c120_y, 0)) *
        Rotation(0, 0, 1) *
        Location((-c120_x, -c120_y, 0)) *
        Location((hole_cx, hole_cy, 0)) *
        Rotation(0, 0, 120) *
        Location((-hole_cx, -hole_cy, 0))
    ))

with BuildPart() as cyl_replica_240:
    add(joined_cyl_rotated.part.moved(
        Location((c240_x, c240_y, 0)) *
        Rotation(0, 0, 1) *
        Location((-c240_x, -c240_y, 0)) *
        Location((hole_cx, hole_cy, 0)) *
        Rotation(0, 0, 240) *
        Location((-hole_cx, -hole_cy, 0))
    ))

with BuildPart() as final_body14:
    add(final_body13.part)
    add(joined_cyl_rotated.part, mode=Mode.SUBTRACT)
    add(cyl_replica_120.part, mode=Mode.SUBTRACT)
    add(cyl_replica_240.part, mode=Mode.SUBTRACT)

# Profile 1 cuts: left/right face, top (z=1053.2) and mid (z=513.2), two Y positions each
plane_left_top       = Plane(origin=(0,       725,         1053.2), x_dir=( 1, 0, 0), z_dir=(0, 1, 0))
plane_left_top_copy  = Plane(origin=(0,       725 - 302.5, 1053.2), x_dir=( 1, 0, 0), z_dir=(0, 1, 0))
plane_right_top      = Plane(origin=(1960.94, 725,         1053.2), x_dir=(-1, 0, 0), z_dir=(0, 1, 0))
plane_right_top_copy = Plane(origin=(1960.94, 725 - 302.5, 1053.2), x_dir=(-1, 0, 0), z_dir=(0, 1, 0))

plane_left_mid       = Plane(origin=(0,       725,         1053.2 - 540), x_dir=( 1, 0, 0), z_dir=(0, 1, 0))
plane_left_mid_copy  = Plane(origin=(0,       725 - 302.5, 1053.2 - 540), x_dir=( 1, 0, 0), z_dir=(0, 1, 0))
plane_right_mid      = Plane(origin=(1960.94, 725,         1053.2 - 540), x_dir=(-1, 0, 0), z_dir=(0, 1, 0))
plane_right_mid_copy = Plane(origin=(1960.94, 725 - 302.5, 1053.2 - 540), x_dir=(-1, 0, 0), z_dir=(0, 1, 0))

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

# Mirrored profile on right face (x=1960.94): flip X of profile points
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

# Separate box: 38mm (X) x 367.5mm (Y) x 40mm (Z), corner at origin then moved
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

# Text emboss on front face (y=0), outward in -Y direction
# Plane: local X = world X (text runs left→right), local Y = world +Z (text goes up)
text_plane = Plane(origin=(50, 0, 200), x_dir=(1, 0, 0), z_dir=(0, -1, 0))

with BuildPart() as final_body20:
    add(final_body19.part)
    def spaced(txt): return " ".join(txt)


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

# "Right" text on back face (y=790), facing outward (+Y), running along +Z axis
# x_dir=(0,0,1): text advances in +Z; z_dir=(0,1,0): normal faces outward (+Y)
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

show(
    final_body21,
    names=["Final Body"],
    colors=["#5588AA"],
)

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)
export_path = filedialog.asksaveasfilename(
    title="Export STEP file",
    defaultextension=".step",
    filetypes=[("STEP files", "*.step *.stp"), ("All files", "*.*")],
    initialfile="Body.step",
)
root.destroy()

if export_path:
    export_step(final_body20.part, export_path)
    print(f"Exported to: {export_path}")
else:
    print("Export cancelled.")