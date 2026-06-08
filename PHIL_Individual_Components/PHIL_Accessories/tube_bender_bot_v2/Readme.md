# Build123d CAD Model — Extruded & Cut Body

A parametric CAD script built with [build123d](https://github.com/gumyr/build123d) that constructs a prismatic body from a rectangular base and removes material through a series of parallelogram profile cuts. The finished model is previewed in the OCP CAD Viewer and exported to STEP via a file-save dialog.

---

## Overall Dimensions

| Axis | Range | Size |
|------|-------|------|
| X | −130.0 → 0.0 mm | **130.0 mm** |
| Y | −163.999 → 0.001 mm | **164.0 mm** |
| Z | −118.177 → 0.0 mm | **118.177 mm** |

**Final volume:** ~1,779,135 mm³

---

## Requirements

| Package | Purpose |
|---------|---------|
| `build123d` | CAD kernel and modelling API |
| `ocp-vscode` | OCP CAD Viewer integration for VS Code |
| `python3-tk` | Native file-save dialog (STEP export) |

Install Python packages:

```bash
pip install build123d ocp-vscode
```

Install tkinter (Linux):

```bash
sudo apt install python3-tk
```

tkinter is bundled with Python on Windows and macOS.

---

## Usage

1. Open the folder in **VS Code** with the [OCP CAD Viewer extension](https://github.com/bernhard-42/vscode-ocp-cad-viewer) installed and the viewer panel open.
2. Run the script:

```bash
python extrude_body.py
```

3. The model renders in the OCP CAD Viewer.
4. A **Save As** dialog appears — choose a folder and filename to export the STEP file.

---

## Methodology

### Coordinate System

All input geometry is defined in a **right-handed world coordinate system (X, Y, Z)**:

- **X** — width axis (−130 → 0)
- **Y** — height / extrusion axis (−163.999 → 0)
- **Z** — depth axis (−118.177 → 0)

Each set of input points shares a **constant Y value**, meaning every profile is a flat polygon lying in the **XZ plane** at a specific height. Sketches are therefore placed on a plane with:

```
Plane(origin=(0, y, 0), x_dir=(1,0,0), z_dir=(0,1,0))  →  normal = +Y
```

Because the sketch v-axis resolves to `−world_Z`, all polygon Z coordinates are negated before being passed to the sketcher via the `to_sketch()` helper:

```python
def to_sketch(pts_xz):
    return [(x, -z) for x, z in pts_xz]
```

### Operations

#### Step 1 — Base Body

A **130 × 118.177 mm rectangle** is sketched in the XZ plane at `Y = −163.999` and extruded **164 mm** along +Y.

```
X: −130.0 → 0.0
Y: −163.999 → 0.001
Z: −118.177 → 0.0
```

#### Step 2 — Cut #1

A **parallelogram** profile (two slanted sides, ~101.5 mm long) is sketched at `Y = −133.999` and used to remove material over **104 mm** of height.

| Corner | X | Z |
|--------|---|---|
| 0 | 0.0 | −48.9725 |
| 1 | −100.0 | −31.3398 |
| 2 | −100.0 | −62.5442 |
| 3 | 0.0 | −80.1769 |

#### Step 3 — Cut #2

A second **parallelogram** profile sketched at `Y = −113.999`, cutting **64 mm** deep. This profile sits immediately below Cut #1 in Z, continuing the staircase.

| Corner | X | Z |
|--------|---|---|
| 0 | 0.0 | −80.1769 |
| 1 | −100.0 | −62.5442 |
| 2 | −100.0 | −80.5442 |
| 3 | 0.0 | −98.1769 |

#### Step 4 — Cut #3

A third **parallelogram** profile at `Y = −133.999`, cutting **104 mm** deep. Covers the deepest Z band down to the base floor.

| Corner | X | Z |
|--------|---|---|
| 0 | 0.0 | −98.1769 |
| 1 | −100.0 | −80.5442 |
| 2 | −100.0 | −118.1769 |
| 3 | 0.0 | −118.1769 |

#### Step 5 — Cut #4

A narrow **parallelogram** profile at `Y = −85.498`, cutting only **7 mm** deep. Located in the upper-Z region of the body, this is a shallow finishing cut.

| Corner | X | Z |
|--------|---|---|
| 0 | 0.0 | −47.1461 |
| 1 | −76.6504 | −33.6301 |
| 2 | −76.8066 | −40.4404 |
| 3 | 0.0 | −54.5716 |

#### Step 6 — Boolean Subtraction

All four cut tools are subtracted from the base body in a single chained boolean operation:

```python
result = base_part.part - cut1_part.part - cut2_part.part \
                        - cut3_part.part - cut4_part.part
```

#### Step 7 — STEP Export

After viewing, a native **file-save dialog** (tkinter) prompts the user for an output path. The model is written using build123d's `export_step()` function.

---

## Volume Reduction Summary

| After step | Volume (mm³) |
|------------|-------------|
| Base extrude | 2,519,531 |
| − Cut #1 | 2,195,005 |
| − Cut #2 | 2,079,805 |
| − Cut #3 | 1,780,115 |
| − Cut #4 | **1,779,135** |

---

## File Structure

```
.
├── extrude_body.py   # Main CAD script
└── README.md         # This file
```

---

## License

MIT
