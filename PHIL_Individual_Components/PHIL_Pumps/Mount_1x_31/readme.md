# Mount 1x — Parametric CAD Model

A fully parametric pump mount assembly modelled in Python using [build123d](https://github.com/gumyr/build123d), an open-source code-based CAD library built on top of OpenCASCADE (OCC).

---

## Overall Dimensions

| Feature | Value |
|---|---|
| Body 1 total length (X) | 797.5 mm (-420 to +377.5) |
| Body 1 total width (Y) | 420 mm (±210) |
| Body 1 step height (Z) | 120.625 mm (low shelf) / 200.625 mm (high shelf) |
| Body 1 base thickness | 25 mm |
| Body 2 (separate body) length (X) | 226.25 mm (382.5 to 608.75) |
| Body 2 total width (Y) | 420 mm (±210) |
| Body 2 extrude height (Z) | 88.63 mm (from Z=-25) |
| Extrude solid height (Z) | 100 mm (from Z=120.625) |
| Main circular bore diameter | 350 mm (radius 175 mm) |
| Outer cylinder bore diameter | ~120 mm (radius ~60 mm, ×2) |
| Inner cylinder bore diameter | 30 mm (radius 15 mm, ×2) |
| Chamfer entry — outer diameter | 100 mm (radius 50 mm) |
| Chamfer entry — inner diameter | 50 mm (radius 25 mm) |
| Chamfer height | 30 mm |

---

## File Structure

```
Mount 1x/
├── Mount.py          # Main build123d script
├── Cut.txt           # XZ profile for Y-direction cut on Body 2
├── extrude.txt       # Loft profile at X=377.5 (YZ plane)
├── extrude_2.txt     # Loft profile at X=227.5 (YZ plane)
├── Outer.txt         # Outer cylinder bore profile
├── inner.txt         # Inner cylinder bore profile
└── README.md         # This file
```

---

## Methodology

### 1. Profile-Based Construction
All geometry is driven by 2D point arrays (polylines) read directly into `build123d` sketches. This makes it straightforward to update any profile by editing the coordinate data without restructuring the model logic.

### 2. Body 1 — Main Mount
- **Base extrude**: The stepped L-shaped cross-section (`points1`) is sketched on the XZ plane and extruded ±210 mm in Y to form the main block.
- **Corner fillets**: Outer corners filleted at 50 mm; vertical step corners at 40 mm; horizontal step edge at 40 mm.
- **Chamfer entries**: Two conical loft cuts (radius 25→50 mm over 30 mm height) applied early on clean geometry for OCC stability.
- **Top face fillet**: 30 mm fillet applied on the flat top face before subtractions.
- **Bore cutouts**: The large circular bore (`points2`, R≈175 mm) is subtracted at Z=48. Six smaller circular bores (`hole1–hole6`) are cut through from Z=-25. A central bore (`hole7`, R=112.5 mm) is cut 25 mm deep. Two oval bores (`hole10`) are cut symmetrically in ±Y.
- **Step pocket**: A rectangular pocket is cut at Z=108.125 creating the upper shelf. Two circular counterbores (`hole8`, `hole9`) are cut from Z=120.625.
- **Loft subtractions**: Four loft solids (`loft_pos`, `loft_neg`, `rect_loft_neg`, `rect_loft_pos`) are pre-built and subtracted to create tapered slot features.
- **Extrude solid**: A profile (`extrude_points`) is extruded +100 mm from Z=120.625 and added to the body, then cut symmetrically on ±Y sides.
- **Loft body cuts**: Two loft bodies (`loft_body_cut`, `loft_body_mirror_cut`) pre-built from YZ profiles at X=227.5 and X=377.5, subtracted from Body 1.

### 3. Body 2 — Separate Pump Body
- **Base extrude**: The large arc profile (`new_body_profile`) is sketched on the XY plane at Z=-25 and extruded 88.63 mm upward.
- **Top face fillet**: 30 mm fillet applied on the two long straight edges (length >100 mm) at the top face.
- **Y-direction cut**: An XZ-plane profile (`cut_xz_points`) at Y=-210 is cut 500 mm in the +Y direction.
- **Outer cylinder cuts**: Two circular bores (R≈60 mm) subtracted using pre-built `outer_body`.
- **Inner cylinder cuts**: Two circular bores (R=15 mm, center at X=452.5, Y=±155) cut ±50 mm in both Z directions.
- **Loft body cuts**: Same loft bodies used to cut matching profiles into Body 2.

### 4. Pre-Built Subtraction Strategy
To avoid OCC segmentation faults from complex boolean operations on accumulated geometry, all major subtraction solids are built as independent `BuildPart` contexts first, then subtracted via `add(..., mode=Mode.SUBTRACT)`. This is the same pattern used by build123d's own examples for robust boolean operations.

### 5. Loft Bodies (Solids 3 & 4)
Two loft solids are constructed from YZ-plane profiles at X=227.5 (`loft_body_profile1`) and X=377.5 (`loft_body_profile2`), then mirrored about the XZ plane. These are used as subtraction tools against Body 1.

### 6. Export
The final assembly is exported as a single STEP file to the desktop using `build123d`'s `export_step()` function with both bodies combined into a `Compound`.

---

## Dependencies

```bash
pip install build123d
pip install ocp-vscode  # for in-editor 3D preview
```

### Recommended Environment
- Python 3.11
- build123d 0.7+
- OCP (OpenCASCADE Python bindings)
- VS Code + OCP CAD Viewer extension for live preview

---

## Running

```bash
python Mount.py
```

The script will:
1. Build all geometry in sequence
2. Display the model in the OCP VS Code viewer
3. Export `Mount.step` to your Desktop

---

## Notes
- All coordinates are in **millimetres**
- The coordinate system origin is at the centre of the base face
- X = length axis, Y = width axis, Z = height axis
- Fillet operations are applied on isolated geometry where possible to prevent OCC kernel crashes
