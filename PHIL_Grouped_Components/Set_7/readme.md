# Power Box Right — Parametric CAD Assembly

A fully parametric build123d Python script that reconstructs a multi-plate industrial power supply enclosure from JSON face geometry exports, including extruded protrusions, chamfers, and precision hole cuts.

---

## Overall Dimensions

| Axis | Range | Span |
|------|-------|------|
| X | -1340 → 100 | **1440 mm** |
| Y | 0 → 1240 | **1240 mm** |
| Z | 0 → 1980 | **1980 mm** |

---

## File Structure

```
Power Box Right/
├── Box Right.py          ← main script (master_script.py)
├── Back.json             ← Back Plate face geometry
├── Front.json            ← Front Plate face geometry
├── Left.json             ← Left Plate face geometry
├── Right.json            ← Right Plate face geometry
└── Bottom.json           ← Bottom Plate face geometry
```

---

## Methodology

### 1. Face Geometry Import
Each plate is defined by a JSON file exported from a CAD source. Each file contains:
- A face key encoding the face normal, e.g. `Face_1_n(1.0,0.0,0.0)`
- One or more wire loops (`is_outer: true/false`) made up of line segments
- Real-world XYZ coordinates preserved from the original CAD model

The face normal determines the sketch plane and extrude direction automatically.

### 2. Sketch Plane Construction
For each face, a `build123d` `Plane` is constructed using the face normal as `z_dir`:

| Plate | Normal | Sketch Plane | Extrude Direction |
|-------|--------|-------------|-------------------|
| Back | `(1,0,0)` | YZ at X=0 | −X → 47.5mm |
| Front | `(-1,0,0)` | YZ at X=−1240 | −X → 47.5mm |
| Left | `(0,-1,0)` | XZ at Y=0 | +Y → 47.5mm |
| Right | `(0,1,0)` | XZ at Y=1240 | −Y → 45mm |
| Bottom | `(0,0,-1)` | XY at Z=0 | +Z → 47.5mm |

### 3. Wire & Face Construction
Segments from each JSON wire are converted to `build123d` edges and closed into a `Wire`. Outer wires form the boundary; inner wires (`is_outer: false`) are punched as holes using `Face.make_holes()`.

### 4. Extrusion
Faces are extruded using `extrude(face, amount)`. The sign of `amount` controls direction relative to the sketch plane normal.

### 5. Boolean Fusion
All plate bodies are fused into a single solid using `.fuse()` with `tol=1e-3` to handle near-coincident faces.

### 6. Protrusion Bodies (Lofts)
External protrusions on the Back and Front plate sides are built as **loft solids** between two rectangular faces at different X positions, creating a tapered transition:

| Group | Side | X Range | Y Range | Z Range |
|-------|------|---------|---------|---------|
| Back bodies 1–3 | +X | 0 → 100 | 470–770 | 480–1877.5 |
| Front bodies 1–4 | −X | −1340 → −1240 | 0–1240 | 0–780.74 |
| Circular bodies | −X | −1314.84 → −1265.12 | 125–175 / 1065–1115 | 780.74–828.24 |

### 7. Chamfer Cuts
Chamfered hole entries are built as **loft solids** between an outer (large diameter) circle and an inner (small diameter) circle, then subtracted from the assembly using `.cut()`:

| Chamfer | Plane | Height | Direction |
|---------|-------|--------|-----------|
| 1 & 2 | Y=0 face | 8.57mm | +Y |
| A | Y=1240 face | 8.57mm | −Y |
| B & C | X=−1240 face | 8.59mm | +X |
| Z ×4 | Z=0 face | 30mm | +Z |
| hole/inner | Z=640–670 | 30mm | +Z |

### 8. Hole & Profile Cuts
Circular holes and shaped profiles are extruded from their face plane and subtracted:

| Cut | Profile | Height | Z Range |
|-----|---------|--------|---------|
| Hole 1 | Circle ⌀30mm | 6mm | 784–790 |
| Hole 2 | Circle ⌀70mm | 145.5mm | 494.5–640 |
| Hole 3 | Circle ⌀30mm | 40mm both dirs | 630–710 |
| Hole 4 | Circle ⌀30mm | 6mm | 1871.5–1877.5 |
| Hex cut 1 | Hexagon | 175.5mm | 790–965.5 |
| Hex cut 2 | Hexagon | 190mm | 1680–1870 |
| Profile cut 1 | Arc + rectangle | 105mm | 677.5–782.5 |
| Profile cut 2 | Arc + rectangle | 100mm | 1877.5–1977.5 |

---

## Dependencies

```bash
pip install build123d ocp-vscode
```

- **Python**: 3.11+
- **build123d**: parametric CAD kernel
- **ocp-vscode**: OCP CAD Viewer integration for VS Code (port 3939)

---

## Running

```bash
# Start OCP CAD Viewer backend first (in a separate terminal)
python3 -m ocp_vscode --backend --port 3939

# Run the script
python3 "Box Right.py"
```
