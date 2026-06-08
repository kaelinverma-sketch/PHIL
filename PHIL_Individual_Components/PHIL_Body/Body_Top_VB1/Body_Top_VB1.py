"""
Build123d script — single hollow body with all features:

BODY — Hollow open box:
  Outer dimensions : 1960.94 x 640.00 x 372.50 mm  (X, Y, Z)
  Wall thickness   : 50 mm
  Face convention  (XZ plane = FRONT):
    Solid faces : front (Y=0), back (Y=640), top (Z=372.5)
    Open  faces : left (X=0), right (X=1960.94), bottom (Z=0)
  Corner at world origin (0, 0, 0)

EXTRUDE CUT 1  : 940.94 x 540.00 x 372.50 mm, centred in X and Y, full height.
EXTRUDE CUT 2  : 650.94 x 50.00 x 372.50 mm, centred in X, through front wall.
SLOT CUT RIGHT : 100.04 wide x 226.30 tall, 50 mm deep, back face, centre X=1205.96.
SLOT CUT LEFT  : Mirror of right slot, centre X=754.98 mm.
BOSS           : 60(X) x 140(Y) x 50(Z) mm, on top face at X=50, Y=225, Z=322.5.
HOLE           : Dia 233.47 mm, centre X=294.99, Y=320.38, through top wall (50 mm).

HOW TO USE WITH OCP CAD VIEWER:
  1. In VS Code: Cmd/Ctrl+Shift+P -> "OCP CAD Viewer: Open Viewer"
  2. Wait for the 3D panel to load
  3. Run:  python box_hollow_ocp.py

Install:  pip install build123d ocp-vscode
"""

from build123d import *

# ---------------------------------------------------------------------------
# Dimensions
# ---------------------------------------------------------------------------
LENGTH    = 1960.94
WIDTH     =  640.00
HEIGHT    =  372.50
T         =   50.00

CUT1_LEN  =  940.94
CUT1_WID  =  540.00

CUT2_LEN  =  650.94
CUT2_WID  =   50.00

SLOT_W    =  100.04
SLOT_RH   =  126.26
SLOT_R    = SLOT_W / 2
SLOT_TOT  = SLOT_RH + SLOT_W       # 226.30 mm
SLOT_DEP  =   50.00

TAB_X     =  60.00
TAB_Y     = 140.00
TAB_Z     =  50.00
tab_ox    =  45.00
tab_oy    = 225.00
tab_oz    = HEIGHT - TAB_Z          # 322.50 mm

HOLE_D    = 233.47
HOLE_R    = HOLE_D / 2              # 116.735 mm
HOLE_CX   = 294.99
HOLE_CY   = 320.38

# ---------------------------------------------------------------------------
# Positions
# ---------------------------------------------------------------------------
cx        = LENGTH / 2
cy        = WIDTH  / 2
cut1_x    = cx - CUT1_LEN / 2
cut1_y    = cy - CUT1_WID / 2
cut2_x    = cx - CUT2_LEN / 2
cut2_y    = 0

slot_r_cx = LENGTH - 754.98        # 1205.96 mm
slot_cz   = HEIGHT / 2             # 186.25 mm

# ---------------------------------------------------------------------------
# Slot tool solids
# ---------------------------------------------------------------------------
with BuildPart() as _slot_build:
    with BuildSketch(Plane.XY) as _sk:
        SlotOverall(width=SLOT_TOT, height=SLOT_W)
    extrude(_sk.sketch, amount=SLOT_DEP)

slot_right = (
    _slot_build.part
    .rotate(Axis.Z, 90)
    .rotate(Axis.X, -90)
    .translate(Vector(slot_r_cx, WIDTH - SLOT_DEP, slot_cz))
)

mirror_plane = Plane(origin=(LENGTH / 2, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
slot_left = slot_right.mirror(mirror_plane)

# ---------------------------------------------------------------------------
# Main body — all operations
# ---------------------------------------------------------------------------
with BuildPart() as part:

    # Step 1 — solid outer box
    Box(LENGTH, WIDTH, HEIGHT,
        align=(Align.MIN, Align.MIN, Align.MIN))

    # Step 2 — hollow out (open left/right/bottom, keep front/back/top)
    with Locations((0, T, 0)):
        Box(LENGTH, WIDTH - 2 * T, HEIGHT - T,
            align=(Align.MIN, Align.MIN, Align.MIN),
            mode=Mode.SUBTRACT)

    # Step 3 — extrude cut 1 (centred rectangular slot)
    with Locations((cut1_x, cut1_y, 0)):
        Box(CUT1_LEN, CUT1_WID, HEIGHT,
            align=(Align.MIN, Align.MIN, Align.MIN),
            mode=Mode.SUBTRACT)

    # Step 4 — extrude cut 2 (front wall slot, centred in X)
    with Locations((cut2_x, cut2_y, 0)):
        Box(CUT2_LEN, CUT2_WID, HEIGHT,
            align=(Align.MIN, Align.MIN, Align.MIN),
            mode=Mode.SUBTRACT)

    # Step 5 — slot cut right (back face)
    add(slot_right, mode=Mode.SUBTRACT)

    # Step 6 — slot cut left (mirrored, back face)
    add(slot_left, mode=Mode.SUBTRACT)

    # Step 7 — rectangular cut on top face
    with Locations((tab_ox, tab_oy, tab_oz)):
        Box(TAB_X, TAB_Y, TAB_Z,
            align=(Align.MIN, Align.MIN, Align.MIN),
            mode=Mode.SUBTRACT)

    # Step 8 — circular hole through top wall
    with BuildSketch(Plane(origin=(HOLE_CX, HOLE_CY, HEIGHT),
                           x_dir=(1, 0, 0), z_dir=(0, 0, 1))) as hole_sk:
        Circle(HOLE_R)
    extrude(hole_sk.sketch, amount=-T, mode=Mode.SUBTRACT)

    # Step 8b — counterbore dia 370mm, depth 23.5mm, cut from bottom of top face
    #   Same centre as the 233.47mm hole: X=294.99, Y=320.38
    #   Z: HEIGHT-T+23.5 = 346.0 down to HEIGHT-T = 322.5
    with BuildSketch(Plane(origin=(HOLE_CX, HOLE_CY, HEIGHT - T + 23.5),
                           x_dir=(1, 0, 0), z_dir=(0, 0, 1))) as cb_sk:
        Circle(185.0)   # radius = 370/2 = 185 mm
    extrude(cb_sk.sketch, amount=-23.5, mode=Mode.SUBTRACT)

    # Step 8b mirror — same cut mirrored to right side (X = LENGTH - HOLE_CX = 1665.95)
    with BuildSketch(Plane(origin=(LENGTH - HOLE_CX, HOLE_CY, HEIGHT - T + 23.5),
                           x_dir=(1, 0, 0), z_dir=(0, 0, 1))) as cb_m_sk:
        Circle(185.0)
    extrude(cb_m_sk.sketch, amount=-23.5, mode=Mode.SUBTRACT)

    # Step 9 — 4 holes (dia 35 mm) on top face, through full top wall (50 mm)
    #   Centres: (140, 165.39), (449.99, 165.39), (140, 475.37), (449.99, 475.37)
    H4_D = 35.00
    H4_R = H4_D / 2   # 17.5 mm
    H4_CENTRES = [
        (140.00, 165.39),
        (449.99, 165.39),
        (140.00, 475.37),
        (449.99, 475.37),
    ]
    for hx, hy in H4_CENTRES:
        with BuildSketch(Plane(origin=(hx, hy, HEIGHT),
                               x_dir=(1, 0, 0), z_dir=(0, 0, 1))) as h4_sk:
            Circle(H4_R)
        extrude(h4_sk.sketch, amount=-T, mode=Mode.SUBTRACT)

    # Step 9b — true 45° conical countersink on the 4 step-9 holes
    #   Slant edge = 24mm, each side = 24/sqrt(2) ≈ 16.97mm
    #   Z top of cone = HEIGHT - T + 17 = 339.5mm
    #   Built by revolving a right-triangle profile 360° around hole axis
    _H4_SIDE = 24.0 / 2**0.5   # 16.97 mm
    _z_top   = HEIGHT - T + 17  # 339.5 mm
    for hx, hy in H4_CENTRES:
        with BuildSketch(Plane(origin=(hx, hy, 0),
                               x_dir=(1, 0, 0), z_dir=(0, 0, 1))) as _cs_sk:
            with BuildLine():
                Line((H4_R,          _z_top),           (H4_R + _H4_SIDE, _z_top))
                Line((H4_R + _H4_SIDE, _z_top),         (H4_R,            _z_top - _H4_SIDE))
                Line((H4_R,          _z_top - _H4_SIDE), (H4_R,           _z_top))
            make_face()
        revolve(_cs_sk.sketch, axis=Axis((hx, hy, 0), (0, 0, 1)),
                revolution_arc=360, mode=Mode.SUBTRACT)

    # Step 10 — mirror steps 7, 8, 9 onto the top right face
    # Mirror plane: perpendicular to X, passing through X = LENGTH/2
    top_mirror = Plane(origin=(LENGTH / 2, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))

    # Mirror step 7 — rectangular cut
    tab_mx = LENGTH - tab_ox - TAB_X   # mirrored X corner = 1960.94 - 50 - 60 = 1850.94
    with Locations((tab_mx, tab_oy, tab_oz)):
        Box(TAB_X, TAB_Y, TAB_Z,
            align=(Align.MIN, Align.MIN, Align.MIN),
            mode=Mode.SUBTRACT)

    # Mirror step 8 — large circular hole
    hole_mx = LENGTH - HOLE_CX         # mirrored centre X = 1960.94 - 294.99 = 1665.95
    with BuildSketch(Plane(origin=(hole_mx, HOLE_CY, HEIGHT),
                           x_dir=(1, 0, 0), z_dir=(0, 0, 1))) as hole_m_sk:
        Circle(HOLE_R)
    extrude(hole_m_sk.sketch, amount=-T, mode=Mode.SUBTRACT)

    # Mirror step 9 — 4 small holes
    for hx, hy in H4_CENTRES:
        hx_m = LENGTH - hx             # mirror X about LENGTH/2
        with BuildSketch(Plane(origin=(hx_m, hy, HEIGHT),
                               x_dir=(1, 0, 0), z_dir=(0, 0, 1))) as h4m_sk:
            Circle(H4_R)
        extrude(h4m_sk.sketch, amount=-T, mode=Mode.SUBTRACT)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
bb = part.part.bounding_box()
slot_l_cx = LENGTH - slot_r_cx
print("=== Final body ===")
print(f"  X : {bb.min.X:.3f}  ->  {bb.max.X:.3f}")
print(f"  Y : {bb.min.Y:.3f}  ->  {bb.max.Y:.3f}")
print(f"  Z : {bb.min.Z:.3f}  ->  {bb.max.Z:.3f}")
print(f"  Faces : {len(part.faces())}")
print(f"\nStep 2  Hollow          : wall/top T={T} mm")
print(f"Step 3  Cut 1           : {CUT1_LEN} x {CUT1_WID} x {HEIGHT} mm, centred")
print(f"Step 4  Cut 2           : {CUT2_LEN} x {CUT2_WID} x {HEIGHT} mm, front wall")
print(f"Step 5  Slot right      : centre X={slot_r_cx:.3f}, Z={slot_cz:.3f}")
print(f"Step 6  Slot left       : centre X={slot_l_cx:.3f}, Z={slot_cz:.3f}")
print(f"Step 7  Boss            : {TAB_X}x{TAB_Y}x{TAB_Z} mm @ ({tab_ox},{tab_oy},{tab_oz:.1f})")
print(f"Step 8  Hole (top face) : dia={HOLE_D} mm, centre ({HOLE_CX},{HOLE_CY})")
print(f"Step 9  4x holes        : dia=35 mm at (140,165.39),(449.99,165.39),(140,475.37),(449.99,475.37)")
print(f"Step 10 Mirror (right)  : steps 7,8,9 mirrored about X={LENGTH/2:.2f} mm")
print(f"Corner posts            : 4x (front-left, front-right, back-left, back-right)")
print(f"Deep holes (dia 70mm)   : 4x centres ({49.98},{49.99}), ({LENGTH-49.98:.2f},{49.99}), ({49.98},{WIDTH-49.99:.2f}), ({LENGTH-49.98:.2f},{WIDTH-49.99:.2f})")

# ---------------------------------------------------------------------------
# Body 2 — corner post: 100mm(X) x 50mm(Y) x 322.5mm(Z), fillet r=50 on far corner
# Placed at front-left corner: X=0, Y=0, Z=0
# ---------------------------------------------------------------------------
POST_X = 100.00   # mm along X
POST_Y =  50.00   # mm along Y
POST_Z = 322.50   # mm height

# Profile: 100x50 rectangle with a 50mm quarter-circle fillet on the far corner
# Body sits at X=0->100, Y=50->100 (shifted +50 in Y)
# Far corner (diagonal from origin) = (X=100, Y=100)
# Arc from (100,50) to (50,100) with r=50, centre at (50,50)
with BuildPart() as body2:
    with BuildSketch(Plane.XY) as _post_sk:
        with BuildLine():
            Line((0, 50), (100, 50))           # bottom edge
            RadiusArc((100, 50), (50, 100), radius=-50) # quarter-circle fillet r=50, bulges outward
            Line((50, 100), (0, 100))          # top edge
            Line((0, 100), (0, 50))            # left edge
        make_face()
    extrude(_post_sk.sketch, amount=POST_Z)

# ---------------------------------------------------------------------------
# Combine Body 1 and Body 2 into a single body (union)
# ---------------------------------------------------------------------------

# Mirror planes
_mirror_plane_x = Plane(origin=(LENGTH / 2, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
_mirror_plane_y = Plane(origin=(0, WIDTH / 2, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))

# Front-left body2, front-right (X mirror), back-left (Y mirror), back-right (XY mirror)
body2_right  = body2.part.mirror(_mirror_plane_x)
body2_back_l = body2.part.mirror(_mirror_plane_y)
body2_back_r = body2_right.mirror(_mirror_plane_y)

# Hole centres:
#   front-left  : (49.98,       49.99)
#   front-right : (LENGTH-49.98, 49.99)
#   back-left   : (49.98,       WIDTH-49.99)
#   back-right  : (LENGTH-49.98, WIDTH-49.99)
_hl_x = 49.98;         _hl_y = 49.99
_hr_x = LENGTH - 49.98; _hr_y = 49.99
_bl_x = 49.98;          _bl_y = WIDTH - 49.99
_br_x = LENGTH - 49.98; _br_y = WIDTH - 49.99

with part:
    # Union all four corner posts
    add(body2.part,   mode=Mode.ADD)   # front-left
    add(body2_right,  mode=Mode.ADD)   # front-right
    add(body2_back_l, mode=Mode.ADD)   # back-left
    add(body2_back_r, mode=Mode.ADD)   # back-right

    # Deep holes (dia 70mm, depth 322.5mm) at all four corners
    for _hx, _hy in [(_hl_x, _hl_y), (_hr_x, _hr_y), (_bl_x, _bl_y), (_br_x, _br_y)]:
        with BuildSketch(Plane(origin=(_hx, _hy, HEIGHT),
                               x_dir=(1, 0, 0), z_dir=(0, 0, 1))) as _dh_sk:
            Circle(35.0)
        extrude(_dh_sk.sketch, amount=-322.5, mode=Mode.SUBTRACT)

    # Step 12 — 35mm dia through-holes at same centres as the 70mm cylinders, full height
    for _hx, _hy in [(_hl_x, _hl_y), (_hr_x, _hr_y), (_bl_x, _bl_y), (_br_x, _br_y)]:
        with BuildSketch(Plane(origin=(_hx, _hy, HEIGHT),
                               x_dir=(1, 0, 0), z_dir=(0, 0, 1))) as _sh_sk:
            Circle(17.5)   # radius = 35/2 = 17.5 mm
        extrude(_sh_sk.sketch, amount=-HEIGHT, mode=Mode.SUBTRACT)

bb_final = part.part.bounding_box()
print("\n=== Combined body (Body 1 + Body 2) ===")
print(f"  X : {bb_final.min.X:.3f}  ->  {bb_final.max.X:.3f}")
print(f"  Y : {bb_final.min.Y:.3f}  ->  {bb_final.max.Y:.3f}")
print(f"  Z : {bb_final.min.Z:.3f}  ->  {bb_final.max.Z:.3f}")
print(f"  Faces : {len(part.faces())}")

# ---------------------------------------------------------------------------
# Body 3 — chamfer cones as separate solid body
#   4x hollow cone frustums (annular rings) on top edges of the 4 step-9 holes
#   Slant = 15mm, each side = 15/sqrt(2) ≈ 10.607mm
#   Bottom (wide): r = H4_R + side, at Z = HEIGHT - side = 361.893mm
#   Top   (narrow): r = H4_R,       at Z = HEIGHT = 372.5mm
# ---------------------------------------------------------------------------
_TOP_SLANT = 24.0
_TOP_SIDE  = _TOP_SLANT / 2**0.5   # 16.971 mm

# Apply chamfer cuts directly into the main body (part)
with part:
    for hx, hy in [
        (140.00, 165.39), (449.99, 165.39),
        (140.00, 475.37), (449.99, 475.37),
    ]:
        # Cone frustum cut — slant=24mm, shifted to Z=322.429->339.4
        with Locations((hx, hy, HEIGHT - _TOP_SIDE - 50 + 16.9)):
            Cone(bottom_radius=H4_R + _TOP_SIDE, top_radius=H4_R,
                 height=_TOP_SIDE,
                 align=(Align.CENTER, Align.CENTER, Align.MIN),
                 mode=Mode.SUBTRACT)

    # Mirror chamfer cuts on the right side (X = LENGTH - hx)
    for hx, hy in [
        (140.00, 165.39), (449.99, 165.39),
        (140.00, 475.37), (449.99, 475.37),
    ]:
        with Locations((LENGTH - hx, hy, HEIGHT - _TOP_SIDE - 50 + 16.9)):
            Cone(bottom_radius=H4_R + _TOP_SIDE, top_radius=H4_R,
                 height=_TOP_SIDE,
                 align=(Align.CENTER, Align.CENTER, Align.MIN),
                 mode=Mode.SUBTRACT)

# ---------------------------------------------------------------------------
# Left face hole — dia 15mm, centre Y=325, Z=347.5, depth 55mm in +X direction
# ---------------------------------------------------------------------------
with part:
    # Plane on left face (X=0), normal pointing +X to drill into body
    # Hole 1: Y=325, Z=347.5
    with BuildSketch(Plane(origin=(0, 325, 347.5),
                           x_dir=(0, 1, 0), z_dir=(1, 0, 0))) as _lh_sk:
        Circle(7.5)   # radius = 15/2 = 7.5 mm
    extrude(_lh_sk.sketch, amount=55, mode=Mode.SUBTRACT)

    # Hole 2: Y=256.02, Z=347.5
    with BuildSketch(Plane(origin=(0, 256.02, 347.5),
                           x_dir=(0, 1, 0), z_dir=(1, 0, 0))) as _lh2_sk:
        Circle(7.5)
    extrude(_lh2_sk.sketch, amount=55, mode=Mode.SUBTRACT)

    # Mirror holes on right face (X=LENGTH), drilling 55mm inward in -X direction
    # z_dir=(-1,0,0) so normal points -X (into the body from right face)
    for cy in [325, 256.02]:
        with BuildSketch(Plane(origin=(LENGTH, cy, 347.5),
                               x_dir=(0, 1, 0), z_dir=(-1, 0, 0))) as _rh_sk:
            Circle(7.5)
        extrude(_rh_sk.sketch, amount=55, mode=Mode.SUBTRACT)



# ---------------------------------------------------------------------------
# 'Z1' emboss cut — text engraved 10mm deep into top face
#   Centre  : X=319.32, Y=525.26
#   Depth   : 10 mm downward from top face (Z=372.5 -> Z=362.5)
# ---------------------------------------------------------------------------
_txt_cx = 319.32   # mm  centre X
_txt_cy = 525.26   # mm  centre Y

with part:
    # Z1 emboss cut (left side)
    with BuildSketch(Plane(origin=(_txt_cx, _txt_cy, HEIGHT),
                           x_dir=(1, 0, 0), z_dir=(0, 0, 1))) as _txt_sk:
        Text('Z1', font_size=100, font='Arial', font_style=FontStyle.BOLD,
             text_align=(TextAlign.CENTER, TextAlign.CENTER))
    extrude(_txt_sk.sketch, amount=-10, mode=Mode.SUBTRACT)

    # Z2 emboss cut — mirrored to right side (X = LENGTH - _txt_cx)
    _txt2_cx = LENGTH - _txt_cx   # 1960.94 - 319.32 = 1641.62 mm
    with BuildSketch(Plane(origin=(_txt2_cx, _txt_cy, HEIGHT),
                           x_dir=(1, 0, 0), z_dir=(0, 0, 1))) as _txt2_sk:
        Text('Z2', font_size=100, font='Arial', font_style=FontStyle.BOLD,
             text_align=(TextAlign.CENTER, TextAlign.CENTER))
    extrude(_txt2_sk.sketch, amount=-10, mode=Mode.SUBTRACT)

print(f"\nZ1 emboss cut: centre ({_txt_cx}, {_txt_cy}), depth 10mm")
print(f"Z2 emboss cut: centre ({LENGTH - _txt_cx:.2f}, {_txt_cy}), depth 10mm")

# ---------------------------------------------------------------------------
# OCP CAD Viewer
# ---------------------------------------------------------------------------
try:
    from ocp_vscode import show, set_defaults, Camera

    set_defaults(
        axes=True,
        axes0=True,
        grid=(True, True, True),
        transparent=False,
        ambient_intensity=1.0,
        direct_intensity=1.1,
    )

    show(
        part,
        names=["Combined Body"],
        colors=["#5588AA"],
        alphas=[1.0],
        reset_camera=Camera.RESET,
    )
    print("\n✅ Model sent to OCP CAD Viewer.")

except RuntimeError as e:
    print("\n⚠️  OCP CAD Viewer is not running.")
    print("    -> Cmd/Ctrl+Shift+P  ->  'OCP CAD Viewer: Open Viewer'")
    print("    -> Wait for the 3D panel, then re-run.\n")
    print(f"    (Error: {e})")

except ImportError:
    print("\n⚠️  ocp-vscode not installed.  Run:  pip install ocp-vscode")

# ---------------------------------------------------------------------------
# Export — popup dialog asks for STEP file save location every run
# ---------------------------------------------------------------------------
import tkinter as tk
from tkinter import filedialog
import os

def ask_export_path(default_name="combined_body.step"):
    """Open a save-file dialog and return the chosen path, or None if cancelled."""
    root = tk.Tk()
    root.withdraw()                      # hide the empty root window
    root.attributes("-topmost", True)    # bring dialog to front
    path_chosen = filedialog.asksaveasfilename(
        title="Save STEP file",
        defaultextension=".step",
        filetypes=[("STEP files", "*.step *.stp"), ("All files", "*.*")],
        initialfile=default_name,
        initialdir=os.path.expanduser("~"),
    )
    root.destroy()
    return path_chosen if path_chosen else None

step_path = ask_export_path("combined_body.step")

if step_path:
    export_step(part.part, step_path)
    print(f"\n✅ Exported STEP: {step_path}")
else:
    print("\n⚠️  Export cancelled — no file saved.")