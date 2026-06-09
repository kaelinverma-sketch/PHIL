"""
Build123d script:
Body 1 - Main body:
  Rectangle cross-section: 150mm (along X) x 100mm (along Z)
  Extrusion length: 1050mm along the +Y axis
  Origin at the corner of the model (x=0, y=0, z=0)
  Hole: 32mm dia at x=73.93, z=50, cut 1060mm in +Y direction
  Extrude cut: 150mm (X) x 80mm (Z), 20mm deep in +Y at y=842.5, z=20..100
  Slot cut 1: 12.5mm (X) x 45mm (Z), 822.5mm in +Y at x=67.68, z=62.67, y=0
  Slot cut 2: 12.5mm (X) x 45mm (Z), 172.5mm in +Y at x=67.68, z=62.67, y=877.5
  Fillets 50mm: edge_front_top_long, edge_back_top_long
  Fillets 50mm: four vertical corner edges
  Fillet 10mm: slot1_end_top_x at y=822.5 and slot2_start_top_x at y=877.5
  Fillet 10mm: slot1 upper left edge
  Fillet  6mm: slot1 upper right edge (max safe)
  Fillet  4mm: pocket_exit_top_x  (max safe; requested 8mm — limited by 10mm slot end cap)
  Fillet  8mm: pocket_entry_top_x
  Fillet auto: pocket_entry_floor_x, pocket_exit_floor_x (max_fillet, capped at 8mm)
"""

from build123d import *
from ocp_vscode import show

with BuildPart() as body1:
    with BuildSketch(Plane.XZ):
        Rectangle(150, 100, align=(Align.MIN, Align.MIN))
    extrude(amount=-1050)

    with BuildSketch(Plane.XZ):
        with Locations((73.93, 50)):
            Circle(16)
    extrude(amount=-1060, mode=Mode.SUBTRACT)

    with BuildSketch(Plane(origin=(0, 842.5, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))):
        with Locations((75, -60)):
            Rectangle(150, 80)
    extrude(amount=20, mode=Mode.SUBTRACT)

    with BuildSketch(Plane(origin=(67.68, 0, 62.67), x_dir=(1, 0, 0), z_dir=(0, -1, 0))):
        Rectangle(12.5, 45, align=(Align.MIN, Align.MIN))
    extrude(amount=-822.5, mode=Mode.SUBTRACT)

    with BuildSketch(Plane(origin=(67.68, 877.5, 62.67), x_dir=(1, 0, 0), z_dir=(0, -1, 0))):
        Rectangle(12.5, 45, align=(Align.MIN, Align.MIN))
    extrude(amount=-172.5, mode=Mode.SUBTRACT)

    # Fillet 1: top long edges — 50mm
    edges = body1.part.edges()
    edge_front_top_long = edges.filter_by_position(Axis.X, 0,     0.01).filter_by_position(Axis.Z, 99.9, 100.1)
    edge_back_top_long  = edges.filter_by_position(Axis.X, 149.9, 150.1).filter_by_position(Axis.Z, 99.9, 100.1)
    fillet(edge_front_top_long + edge_back_top_long, radius=50)

    # Fillet 2: four vertical corner edges — 50mm
    edges = body1.part.edges()
    edge_corner_x0_y0      = edges.filter_by_position(Axis.X, 0,     0.01).filter_by_position(Axis.Y, 0,      0.01)
    edge_corner_x0_y1050   = edges.filter_by_position(Axis.X, 0,     0.01).filter_by_position(Axis.Y, 1049.9, 1050.1)
    edge_corner_x150_y0    = edges.filter_by_position(Axis.X, 149.9, 150.1).filter_by_position(Axis.Y, 0,      0.01)
    edge_corner_x150_y1050 = edges.filter_by_position(Axis.X, 149.9, 150.1).filter_by_position(Axis.Y, 1049.9, 1050.1)
    fillet(edge_corner_x0_y0 + edge_corner_x0_y1050 + edge_corner_x150_y0 + edge_corner_x150_y1050, radius=50)

    # Fillet 3: slot end cap top edges — 10mm
    edges = body1.part.edges()
    slot1_end_top_x   = edges.filter_by_position(Axis.Y, 822.4, 822.6).filter_by_position(Axis.Z, 99.9, 100.1)
    slot2_start_top_x = edges.filter_by_position(Axis.Y, 877.4, 877.6).filter_by_position(Axis.Z, 99.9, 100.1)
    fillet(slot1_end_top_x + slot2_start_top_x, radius=10)

    # Fillet 4: slot1 upper left edge — 10mm
    edges = body1.part.edges()
    slot1_upper_left = edges.filter_by_position(Axis.X, 67.6, 67.8).filter_by_position(Axis.Z, 99.9, 100.1)
    fillet(slot1_upper_left, radius=10)

    # Fillet 5: slot1 upper right edge — 6mm (max safe)
    edges = body1.part.edges()
    slot1_upper_right = edges.filter_by_position(Axis.X, 80.1, 80.3).filter_by_position(Axis.Z, 99.9, 100.1)
    fillet(slot1_upper_right, radius=6)

    # Fillet 6: pocket exit top edge — 4mm (max safe after 10mm slot end cap fillet)
    edges = body1.part.edges()
    pocket_exit_top_x = edges.filter_by_position(Axis.Y, 862.4, 862.6).filter_by_position(Axis.Z, 99.9, 100.1)
    fillet(pocket_exit_top_x, radius=4)

    # Fillet 7: pocket entry top edge — 8mm
    edges = body1.part.edges()
    pocket_entry_top_x = edges.filter_by_position(Axis.Y, 842.4, 842.6).filter_by_position(Axis.Z, 99.9, 100.1)
    fillet(pocket_entry_top_x, radius=8)

    # Fillet 8: pocket entry floor edge — auto (max_fillet, capped at 8mm)
    edges = body1.part.edges()
    pocket_entry_floor_x = edges.filter_by_position(Axis.Y, 842.4, 842.6).filter_by_position(Axis.Z, 19.9, 20.1)
    r8 = min(8, body1.part.max_fillet(pocket_entry_floor_x, tolerance=0.5, max_iterations=20))
    print(f"Fillet 8 (pocket_entry_floor_x) radius: {r8:.3f} mm")
    fillet(pocket_entry_floor_x, radius=r8)

    # Fillet 9: pocket exit floor edge — auto (max_fillet, capped at 8mm)
    edges = body1.part.edges()
    pocket_exit_floor_x = edges.filter_by_position(Axis.Y, 862.4, 862.6).filter_by_position(Axis.Z, 19.9, 20.1)
    r9 = min(8, body1.part.max_fillet(pocket_exit_floor_x, tolerance=0.5, max_iterations=20))
    print(f"Fillet 9 (pocket_exit_floor_x)  radius: {r9:.3f} mm")
    fillet(pocket_exit_floor_x, radius=r9)

    # Fillet 10: hole arc at y=842.5 — 10mm
    edges = body1.part.edges()
    hole_arc_y842 = edges.filter_by(GeomType.CIRCLE).filter_by_position(Axis.Y, 842.4, 842.6) \
                         .filter_by_position(Axis.X, 57.9, 89.9).filter_by_position(Axis.Z, 34.0, 66.0)
    fillet(hole_arc_y842, radius=10)

    # Fillet 11: hole arc at y=1050 — 6mm (max safe; requested 10mm)
    edges = body1.part.edges()
    hole_arc_y1050 = edges.filter_by(GeomType.CIRCLE).filter_by_position(Axis.Y, 1049.9, 1050.1) \
                          .filter_by_position(Axis.X, 57.9, 89.9)
    fillet(hole_arc_y1050, radius=6)

show(body1, axes=True, axes0=True, grid=(True, True, True), transparent=False)

# ---------------------------------------------------------------------------
# STEP + STL Export — pop-up dialog to choose save location
# ---------------------------------------------------------------------------
import tkinter as tk
from tkinter import filedialog
import os

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
    # ── STEP export ──────────────────────────────────────────────────────────
    export_step(body1.part, export_path)
    print(f"STEP exported to: {export_path}")

    # ── STL export — same folder, same base name ─────────────────────────────
    stl_path = os.path.splitext(export_path)[0] + ".stl"
    export_stl(body1.part, stl_path)
    print(f"STL  exported to: {stl_path}")
else:
    print("Export cancelled.")
