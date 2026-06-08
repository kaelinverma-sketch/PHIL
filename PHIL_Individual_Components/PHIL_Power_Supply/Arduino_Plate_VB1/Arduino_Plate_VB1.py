"""
Build123d - Combined script (single fused body):
  1. Base rectangle extruded 50 mm
  2. 5 hexagonal cut-outs from bottom face, 30 mm deep
  3. 6 hollow cylinders fused onto top face (Z=50), extruded 20 mm upward
  4. 6 frustum cone cuts from bottom face (Z=0) upward 20 mm

All coordinates share the same normalisation origin (base rect min X/Y).

Run : python Arduino_Plate.py
Needs: build123d, ocp-vscode
Place profiles.json in the same folder as this script.
"""

import json
import math
import os
from build123d import *
from ocp_vscode import show

# ═══════════════════════════════════════════════════════════════════════════════
# RAW DATA
# ═══════════════════════════════════════════════════════════════════════════════

BASE_PTS = [
    (542044.6875, 235915.9766, 50.0),
    (543241.7578, 235915.9766, 50.0),
    (543241.7578, 237098.9648, 50.0),
    (542044.6875, 237098.9648, 50.0),
]
BASE_HEIGHT = 50.0

CUT_PTS_RAW = [
    (542324.6875, 236179.3359, 30.0),
    (542294.6875, 236196.6406, 30.0),
    (542294.6875, 236231.2891, 30.0),
    (542324.6875, 236248.6133, 30.0),
    (542354.6875, 236231.2891, 30.0),
    (542354.6875, 236196.6406, 30.0),

    (542364.6875, 236676.6406, 30.0),
    (542364.6875, 236711.2891, 30.0),
    (542334.6875, 236728.6133, 30.0),
    (542304.6875, 236711.2891, 30.0),
    (542304.6875, 236676.6406, 30.0),
    (542334.6875, 236659.3359, 30.0),

    (542814.6875, 236526.6406, 30.0),
    (542844.6875, 236509.3359, 30.0),
    (542874.6875, 236526.6406, 30.0),
    (542874.6875, 236561.2891, 30.0),
    (542844.6875, 236578.6133, 30.0),
    (542814.6875, 236561.2891, 30.0),

    (543054.6875, 236711.2891, 30.0),
    (543084.6875, 236728.6133, 30.0),
    (543114.6875, 236711.2891, 30.0),
    (543114.6875, 236676.6406, 30.0),
    (543084.6875, 236659.3359, 30.0),
    (543054.6875, 236676.6406, 30.0),

    (542814.6875, 236246.6406, 30.0),
    (542844.6875, 236229.3359, 30.0),
    (542874.6875, 236246.6406, 30.0),
    (542874.6875, 236281.2891, 30.0),
    (542844.6875, 236298.6133, 30.0),
    (542814.6875, 236281.2891, 30.0),
]
CUT_HEIGHT = 30.0
CUT_N      = 6

PROFILE_HEIGHT = 20.0

# Cone parameters
CONE_ANGLE    = 70.0
CONE_HEIGHT   = 20.0
CONE_BOTTOM_R = 35.0   # wide base (dia 70) at Z=0
CONE_TOP_R    = CONE_BOTTOM_R - CONE_HEIGHT * math.tan(math.radians(CONE_ANGLE / 2.0))

# ═══════════════════════════════════════════════════════════════════════════════
# SHARED NORMALISATION ORIGIN
# ═══════════════════════════════════════════════════════════════════════════════
MIN_X = min(p[0] for p in BASE_PTS)
MIN_Y = min(p[1] for p in BASE_PTS)

def norm2d(pts_raw):
    return [(p[0] - MIN_X, p[1] - MIN_Y) for p in pts_raw]

print(f"Normalisation origin : ({MIN_X}, {MIN_Y})")
print(f"Cone frustum: bottom_r={CONE_BOTTOM_R} mm  top_r={CONE_TOP_R:.4f} mm  height={CONE_HEIGHT} mm")

# ═══════════════════════════════════════════════════════════════════════════════
# LOAD profiles.json
# ═══════════════════════════════════════════════════════════════════════════════
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH  = os.path.join(SCRIPT_DIR, "profiles.json")

if not os.path.exists(JSON_PATH):
    raise FileNotFoundError(
        f"profiles.json not found at:\n  {JSON_PATH}\n"
        "Please place profiles.json in the same folder as this script."
    )

with open(JSON_PATH) as f:
    data = json.load(f)

def profile_to_points(profile):
    return [
        (seg["start"][0] - MIN_X, seg["start"][1] - MIN_Y)
        for seg in profile["segments"]
    ]

def get_center(face_groups):
    outer_p = next(p for p in face_groups[0] if p["is_outer"])
    segs = outer_p["segments"]
    xs = [s["start"][0] - MIN_X for s in segs]
    ys = [s["start"][1] - MIN_Y for s in segs]
    return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)

# ═══════════════════════════════════════════════════════════════════════════════
# PRE-BUILD cone cutters OUTSIDE BuildPart (avoids auto-add into context)
# ═══════════════════════════════════════════════════════════════════════════════
# Only cut cones under cylinders that sit directly above a hexagon (dist < 50 mm)
hex_centers = []
for i in range(0, len(CUT_PTS_RAW), CUT_N):
    grp = CUT_PTS_RAW[i:i+CUT_N]
    hx = (min(p[0] for p in grp) + max(p[0] for p in grp)) / 2 - MIN_X
    hy = (min(p[1] for p in grp) + max(p[1] for p in grp)) / 2 - MIN_Y
    hex_centers.append((hx, hy))

cone_cutters = []
for face_key, face_groups in data.items():
    cx, cy = get_center(face_groups)
    nearest_dist = min(math.hypot(cx-hx, cy-hy) for hx,hy in hex_centers)
    if nearest_dist > 50:
        print(f"  Skipping cone at ({cx:.2f}, {cy:.2f}) — no matching hexagon (dist={nearest_dist:.2f})")
        continue
    # Wide base flush at Z=0, tip pointing upward
    c = Cone(height=CONE_HEIGHT, bottom_radius=CONE_BOTTOM_R, top_radius=CONE_TOP_R)
    c = c.translate(Vector(cx, cy, CONE_HEIGHT / 2))
    cone_cutters.append((cx, cy, c))
    print(f"  Cone cutter prepared at ({cx:.2f}, {cy:.2f})")

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════
with BuildPart() as part:

    # ── 1. Base rectangle ────────────────────────────────────────────────────
    base_local = norm2d(BASE_PTS)
    with BuildSketch(Plane.XY):
        with BuildLine():
            for i in range(4):
                Line(base_local[i], base_local[(i + 1) % 4])
        make_face()
    extrude(amount=BASE_HEIGHT)
    print("Base extruded.")

    # ── 2. Hex cuts from bottom face (Z=0) upward 30 mm ──────────────────────
    hexagons = [
        norm2d(CUT_PTS_RAW[i : i + CUT_N])
        for i in range(0, len(CUT_PTS_RAW), CUT_N)
    ]
    for idx, hex_pts in enumerate(hexagons):
        with BuildSketch(Plane.XY):
            with BuildLine():
                for i in range(CUT_N):
                    Line(hex_pts[i], hex_pts[(i + 1) % CUT_N])
            make_face()
        extrude(amount=CUT_HEIGHT, mode=Mode.SUBTRACT)
        print(f"  Hex cut {idx + 1} applied.")

    # ── 3. Hollow cylinders fused onto top face (Z=50) upward 20 mm ──────────
    top_plane = Plane.XY.offset(BASE_HEIGHT)

    for face_idx, (face_key, face_groups) in enumerate(data.items()):
        group     = face_groups[0]
        outer_p   = next(p for p in group if p["is_outer"])
        inner_p   = next(p for p in group if not p["is_outer"])
        outer_pts = profile_to_points(outer_p)
        inner_pts = profile_to_points(inner_p)

        with BuildSketch(top_plane):
            with BuildLine():
                for i in range(len(outer_pts)):
                    Line(outer_pts[i], outer_pts[(i + 1) % len(outer_pts)])
            make_face()
            with BuildLine():
                for i in range(len(inner_pts)):
                    Line(inner_pts[i], inner_pts[(i + 1) % len(inner_pts)])
            make_face(mode=Mode.SUBTRACT)
        extrude(amount=PROFILE_HEIGHT, mode=Mode.ADD)
        print(f"  Cylinder {face_idx + 1} ({face_key}) fused.")

# ── 4. Subtract cone cutters using direct boolean outside BuildPart ───────────
result = part.part
for idx, (cx, cy, cutter) in enumerate(cone_cutters):
    result = result - cutter
    print(f"  Cone cut {idx + 1} applied at ({cx:.2f}, {cy:.2f})")

print(f"\nFinal bbox : {result.bounding_box()}")

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT — pop-up folder picker, then save as STEP
# ═══════════════════════════════════════════════════════════════════════════════
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()                      # hide the empty root window
root.attributes("-topmost", True)    # bring dialog to front

export_dir = filedialog.askdirectory(
    title="Select folder to save Arduino_Plate.step"
)

if export_dir:
    step_path = os.path.join(export_dir, "Arduino_Plate.step")
    export_step(result, step_path)
    print(f"\nSTEP exported to: {step_path}")
else:
    print("\nExport cancelled — no folder selected.")

# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════
show(
    result,
    names=["Arduino Plate"],
    colors=["#4488CC"],
    alphas=[1.0],
)