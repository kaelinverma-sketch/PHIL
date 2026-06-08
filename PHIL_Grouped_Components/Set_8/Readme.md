# Arduino Plate — Parametric CAD Model

A fully parametric **build123d** script that constructs an Arduino mounting plate with hexagonal cut-outs, fused hollow cylinders, and frustum cone cuts — all exported to STEP format via a GUI folder picker.

---

## File Structure

```
Arduino Plate/
├── Arduino Plate.py   # Main build script
├── profiles.json      # Hollow cylinder face profiles (outer + inner loops)
└── README.md
```

---

## Requirements

```bash
pip install build123d ocp-vscode
```

- **Python** 3.10+
- **build123d** — parametric CAD kernel
- **ocp-vscode** — OCP CAD Viewer for in-editor 3D preview
- **tkinter** — built into Python standard library (used for the STEP export dialog)

---

## Usage

```bash
python "Arduino Plate.py"
```

On each run:
1. The model is built and all operations are printed to the console.
2. A **folder picker dialog** appears — select where to save the STEP file.
3. `Arduino_Plate.step` is written to the chosen folder.
4. The model opens in the **OCP CAD Viewer**.

---

## profiles.json — Format & Usage

`profiles.json` defines the **6 hollow cylinder cross-sections** as closed polygon loops derived from a CAD face export.

### Structure

```json
{
  "Face_1_n(0.0,0.0,1.0)": [
    [
      {
        "is_outer": true,
        "seg_count": 42,
        "segments": [
          { "type": "line", "start": [x, y, z], "end": [x, y, z] },
          ...
        ]
      },
      {
        "is_outer": false,
        "seg_count": 30,
        "segments": [ ... ]
      }
    ]
  ],
  "Face_2_n(0.0,0.0,1.0)": [ ... ],
  ...
}
```

### Key Fields

| Field | Description |
|---|---|
| `Face_N_n(0,0,1)` | Face key — one entry per hollow cylinder |
| `is_outer: true` | Outer wall boundary of the cylinder |
| `is_outer: false` | Inner bore boundary (creates the hollow) |
| `seg_count` | Number of line segments in the loop |
| `segments[].start/end` | 3D survey coordinates of each segment vertex |

### How it's used in the script

- All XY coordinates are **normalised** by subtracting the base plate's minimum X/Y (survey origin → local mm origin).
- The `start` point of each segment is extracted in order to reconstruct the closed polygon.
- Two `BuildLine` + `make_face` calls per cylinder create the annular (ring) cross-section — outer face first, then inner face subtracted with `Mode.SUBTRACT`.
- The sketch is placed on `Plane.XY.offset(50)` (top face of base plate) and extruded **+20 mm upward** with `Mode.ADD` to fuse into the base solid.

---

## Methodology

### Coordinate Normalisation

All input coordinates are in a projected survey system (values ~542,000 / 236,000). To avoid floating-point precision issues in the CAD kernel, a **shared local origin** is established:

```
MIN_X = min X of base rectangle corners
MIN_Y = min Y of base rectangle corners
local_x = raw_x − MIN_X
local_y = raw_y − MIN_Y
```

This is applied consistently to **all** geometry (base plate, hex cuts, cylinder profiles, cone placement) so every feature lands in the correct relative position.

### Build Sequence

All geometry is constructed in a single `BuildPart` context (steps 1–3), followed by direct boolean subtraction for the cone cuts (step 4):

```
Step 1 │ Base plate rectangle      → extrude +50 mm          (Mode.ADD)
Step 2 │ 5 × hexagonal pockets     → extrude +30 mm from Z=0 (Mode.SUBTRACT)
Step 3 │ 6 × hollow cylinders      → extrude +20 mm from Z=50(Mode.ADD / fused)
Step 4 │ 5 × frustum cone cuts     → boolean subtract         (outside BuildPart)
Step 5 │ STEP export + OCP display
```

> **Why step 4 is outside `BuildPart`:** build123d's context manager auto-registers any `Cone()` call made inside `with BuildPart()` as an additive body. To use cones purely as cutters, they are constructed outside the context and subtracted via `result = result - cutter`.

### Cone–Hexagon Matching

Only cylinders whose centre lies within **50 mm** of a hexagon centre receive a cone cut. This filters out Face_6, which has no corresponding hexagonal pocket:

```python
nearest_dist = min(hypot(cx−hx, cy−hy) for hx, hy in hex_centers)
if nearest_dist > 50: skip
```

---

## Overall Dimensions

| Feature | Value |
|---|---|
| **Base plate** | 1197.07 × 1182.99 × 50.0 mm |
| **Overall model height** | 70.0 mm (plate 50 mm + cylinders 20 mm) |
| **Hexagonal pockets** | 5 off — 60 × 69.28 mm span, 30 mm deep from bottom face |
| **Hollow cylinders** | 6 off — ~60 × 60 mm outer, ~30 × 30 mm inner, 15 mm wall, 20 mm tall |
| **Frustum cone cuts** | 5 off — ⌀70 mm base, ⌀42 mm top, 20 mm deep from bottom face, 70° full angle |
| **Coordinate origin** | (542044.6875, 235915.9766) survey → (0, 0) local |

### Section View (Z axis)

```
Z = 70 ┤ ▔▔▔▔▔▔  Cylinder tops
Z = 50 ┤ ════════ Top face of base plate / cylinder base
       │          (hollow cylinders fused above)
Z = 30 ┤ - - - -  Hex pocket floor
Z = 20 ┤ · · · ·  Cone cut top (⌀42 mm)
Z =  0 ┤ ════════ Bottom face — cone base (⌀70 mm) & hex entry
```

---

## STEP Export

A `tkinter` folder picker dialog is shown on every run. The file is saved as:

```
<selected_folder>/Arduino_Plate.step
```

If the dialog is cancelled, the export is skipped and the viewer still opens.

---

## License

MIT — free to use and modify.
