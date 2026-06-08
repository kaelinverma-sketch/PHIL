# Elbow Right — build123d CAD Script

A parametric CAD model of a mechanical elbow-right component, built entirely in Python using [build123d](https://github.com/gumyr/build123d) and viewable in [OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer).

---

## Overall Dimensions

| Parameter | Value |
|---|---|
| Total length (X) | ~817mm |
| Total width (Y) | ~233mm |
| Total height (Z) | 100mm |
| Main body height | 100mm |
| Connector tab height | 40mm (z = 60–100mm) |
| Semi-circular end radius | ~100mm |

---

## Methodology

### Coordinate System
All profiles are defined in real-world survey coordinates (easting ~540,000 / northing ~233,000). A shared global origin is computed from the minimum X and Y across all profiles and subtracted before building, keeping all geometry near `(0, 0, 0)` to avoid floating-point precision issues in OpenCASCADE.

### Profile Cleaning
Raw point data frequently contained out-of-sequence (rogue) points that caused self-intersecting wires. Each profile was inspected for direction reversals and large positional jumps, and rogue points were removed before use. For circular profiles, points were sorted by angle around their centroid to guarantee a valid closed wire.

### Boolean Workflow
The model is built as a sequence of boolean operations on extruded 2D sketches:

```
result = (Shape1 + Shape2 + Shape3)   ← fused main body
       - cutter                        ← top 50mm pocket cut
       - extrude5                      ← hexagonal cut
       - hollow_cylinder               ← annular groove (z=45–50mm)
       - extrude7                      ← elliptical cut (z=31.5–50mm)
       - extrude8                      ← diagonal slot cut (z=70–100mm)
       - hole1 - hole2                 ← two through-holes (±120mm)
       - extrude10                     ← two counter-bore cuts (z=0–50mm)
       - extrude11                     ← two chamfer lofts (z=50–67.5mm)
       - hole12a - hole12b             ← two small through-holes (±120mm)
       - cutter13                      ← small profile cut (5mm)
       - extrude14                     ← engraved 'R' (top face)
       - extrude15                     ← engraved 'TOP' (top face)
       - extrude16                     ← engraved 'BOTTOM' (bottom face)
       - extrude17                     ← engraved 'RIGHT' (bottom face)
```

### Shape Descriptions

| Shape | Description | Height |
|---|---|---|
| Shape 1 | Large rounded-rectangle outline (main body) | 100mm |
| Shape 2 | Notched rectangle / connector tab | 40mm (offset to z=60) |
| Shape 3 | Rectangle with semicircular end | 100mm |
| Shape 4 | Cutter profile (0.5mm Shapely buffer, coplanar-face fix) | 50mm cut from z=50 |
| Shape 5 | Hexagonal cut | 30mm |
| Shape 6 | Hollow cylinder (annular groove) | 5mm at z=45 |
| Shape 7 | Ellipse cut | 18.5mm from z=31.5 |
| Shape 8 | Diagonal slot cut | 30mm from z=70 |
| Shape 9 | Two circular through-holes | 240mm (±120mm) |
| Shape 10 | Two counter-bore rings | 50mm |
| Shape 11 | Two chamfer lofts (outer→inner taper) | 17.5mm from z=50 |
| Shape 12 | Two small through-holes | 240mm (±120mm) |
| Shape 13 | Small profile cut | 5mm |
| Shape 14 | Engraved 'R' text (100mm font) | 5mm from z=95 |
| Shape 15 | Engraved 'TOP' text (50mm font) | 5mm from z=95 |
| Shape 16 | Engraved 'BOTTOM' text (70mm font) | 5mm into bottom face |
| Shape 17 | Engraved 'RIGHT' text (30mm font) | 5mm into bottom face |
| Shape 18 | Rectangular box (separate body) | 57.5mm |

### Chamfer Technique
The chamfer rings (Shape 11) use `loft()` between two sketch planes — the outer (larger) profile at `z=50` and the inner (smaller) profile at `z=67.5` — to create a true tapered/conical wall rather than a straight hollow cylinder.

### Text Engraving
Text is created using build123d's `Text()` primitive with `Align.MIN, Align.MAX` to anchor the top-left corner at the origin, then rotated and translated into position before being subtracted from the model.

### Export
On each run, a `tkinter` file dialog prompts for a save location and exports the final result as a STEP file using `export_step()`.

---

## Requirements

```
pip install build123d ocp-vscode shapely
```

- Python 3.11+
- [build123d](https://github.com/gumyr/build123d)
- [ocp-vscode](https://github.com/bernhard-42/vscode-ocp-cad-viewer) (VS Code extension for viewing)
- [Shapely](https://shapely.readthedocs.io/) (used for profile validation and offset)

---

## Usage

```bash
python Elbow_Right_Master.py
```

The model renders in OCP CAD Viewer. A save dialog then prompts for the STEP export location.

---

## File Structure

```
Elbow_Right_Master.py   ← main script
README.md               ← this file
```
