# USB Front Panel — build123d CAD Script

Parametric 3D model of a USB front panel enclosure face, built entirely in Python using [build123d](https://github.com/gumyr/build123d). The script reconstructs geometry from raw point-cloud data, fits analytical circles via least-squares, and applies Boolean operations and fillets to produce a production-ready STEP file.

---

## Overall Dimensions

| Parameter | Value |
|---|---|
| Width (X) | 125.0 mm (−40.08 → +84.92) |
| Depth (Y) | 425.0 mm (−210.55 → +214.45) |
| Height (Z) | 30.0 mm (Z = 0 → Z = 30) |
| Corner fillet radius | 20.0 mm |
| Top face fillet radius | 20.0 mm |

---

## Features & Geometry

### Countersink / Chamfer Cuts × 2
Two conical countersink pockets cut into the top face (Z = 30), mirrored symmetrically in Y.

| Parameter | Value |
|---|---|
| Centre (original) | X ≈ 22.4, Y ≈ −148.0 |
| Centre (mirrored) | X ≈ 22.4, Y ≈ +152.0 |
| Large opening radius | ≈ 30.0 mm at Z = 30 |
| Small base radius | ≈ 15.0 mm at Z = 10 |
| Depth | 20 mm (Z = 30 → Z = 10) |

### Through Holes × 2
Cylindrical holes bored through the full body, mirrored in Y to match the countersinks.

| Parameter | Value |
|---|---|
| Radius | ≈ 13.5 mm |
| Extent | Z = −10 → Z = 40 (50 mm total) |
| Centre (original) | X ≈ 22.4, Y ≈ −148.0 |
| Centre (mirrored) | X ≈ 22.4, Y ≈ +152.0 |

### Slot Cut (USB aperture)
A D-shaped slot with a semicircular left end and straight right edge, cut through the full height of the body.

| Parameter | Value |
|---|---|
| Profile | Semicircle (r ≈ 22.5 mm) + straight top/bottom edges |
| Slot width (Y span) | ≈ 45.0 mm (−20.55 → +24.45) |
| Slot depth (X span) | ≈ 92.5 mm (0 → 92.5) |
| Extent | Z = −10 → Z = 50 (60 mm total) |
| Applied | After fillets (clean sharp edges on cut) |

---

## Methodology

### 1. Point Cloud → Analytical Circle (Least-Squares Fit)
All circular features (chamfer big, outer, inner) are defined as raw XY point clouds exported from a source CAD tool. The script fits a circle to each cloud using the **algebraic least-squares** method:

Given points $(x_i, y_i)$, the general circle equation $x^2 + y^2 = 2c_x x + 2c_y y + r^2 - c_x^2 - c_y^2$ is rewritten as a linear system $A \mathbf{p} = \mathbf{b}$ and solved with `numpy.linalg.lstsq`, yielding centre $(c_x, c_y)$ and radius $r$. This approach is robust to noise and does not require a good initial guess.

### 2. Base Body
A closed rectangular polyline is extruded 30 mm along Z using `BuildSketch` + `extrude()`.

### 3. Conical Chamfer Tool
Two circular sketches (large at Z = 0, small at Z = −20) are lofted to create a truncated cone. The solid is then translated to `(avg_cx, avg_cy, 30)` so the large face sits flush with the top of the base. The tool is subtracted from the base as a Boolean cut.

### 4. Y-Mirror of Chamfer & Hole
The mirror axis is the Y midpoint of the rectangular face:

```
mirror_y = (rect_y_min + rect_y_max) / 2  ≈ +1.953 mm
cy_mirrored = 2 × mirror_y − cy_original
```

Both the chamfer tool and hole tool are reconstructed at the mirrored Y centre and subtracted independently.

### 5. Cylindrical Through-Hole
A circle of radius `r_inner` is extruded from Z = −10 to Z = 40. The tool is placed at the fitted inner circle centre and subtracted from the body, creating a through-hole with 10 mm clearance beyond each face.

### 6. Fillets
Fillets are applied in two passes inside a single `BuildPart` context after all chamfer/hole cuts:

- **Vertical corner edges** — filtered by `Axis.Z` parallelism and exact length match (`== EXTRUDE_HEIGHT`), radius 20 mm.
- **Top face perimeter edges** — filtered by Z centre ≈ 30 mm, `GeomType.LINE` only (excludes chamfer arcs), and edge centre lying on one of the 4 outer rect boundaries (tolerance 1 mm), radius 20 mm.

### 7. Slot Cut (applied after fillets)
The USB slot profile is a closed polyline (semicircle + two straight edges + closing line). It is extruded 60 mm and subtracted **after** fillets so its edges remain sharp and unaffected by the fillet passes.

### 8. STEP Export
The final solid is exported to `~/Desktop/USB_Front.step` using build123d's `export_step()`.

---

## File Structure

```
.
├── USB_Front.py          # Main build123d script
├── extrude.txt           # Base rectangle corner points
├── Chamfer_Big.txt       # Large chamfer opening point cloud
├── Outer.txt             # Small chamfer base point cloud
├── inner.txt             # Through-hole point cloud
├── Cut.txt               # USB slot profile points
└── README.md             # This file
```

---

## Requirements

```bash
pip install build123d ocp-vscode numpy
```

| Package | Purpose |
|---|---|
| `build123d` | Parametric CAD kernel (OCCT wrapper) |
| `ocp-vscode` | OCP CAD Viewer for in-editor 3D preview |
| `numpy` | Least-squares circle fitting |

---

## Usage

```bash
python USB_Front.py
```
