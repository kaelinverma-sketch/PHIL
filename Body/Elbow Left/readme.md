# Elbow Left — Parametric CAD Model

A fully parametric **Elbow Left** body modelled in Python using [build123d](https://github.com/gumyr/build123d) and visualised with [OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer). All geometry is constructed programmatically from coordinate point clouds, polyline profiles, and boolean operations — no GUI required.

---

## Requirements

```bash
pip install build123d ocp-vscode
```

> Python 3.10+ recommended. Run inside VS Code with the OCP CAD Viewer extension installed for live 3D preview.

---

## Usage

```bash
python Elbow_left.py
```

On completion the script:
1. Displays the finished model in the OCP CAD Viewer
2. Opens a **Save As** dialog to export the model as a `.step` file to a location of your choice

---

## Methodology

The model is built entirely through **code-driven CAD** — no imported geometry, no mesh files. The workflow follows these stages:

### 1. Profile Construction
Each body cross-section is defined as an ordered list of 2D coordinate points (sourced from external `Cut.txt` / `hole.txt` files). Points are:
- Sorted by angle around their centroid where needed (circular profiles)
- Offset in X/Y/Z to align with the intended coordinate system
- Closed via `Polyline(..., close=True)` into a sketch face

### 2. Extrusion
Sketch faces are extruded using `extrude(amount=..., mode=Mode.ADD)` to create solid volumes at their respective Z heights.

### 3. Boolean Union
The four primary bodies are merged into a single solid:
```python
combined_all_solid = arc_body.solid() + new_body.solid() + body3.solid() + body4.solid()
```

### 4. Boolean Cuts
All holes, slots, chamfers, and text engravings are applied sequentially to `combined_all` using `mode=Mode.SUBTRACT`:
- **Circular holes** — sorted point-cloud circles at various Z heights
- **Through-holes** — ±500mm extrusions to guarantee full penetration
- **Chamfer lofts** — `Solid.make_loft()` between inner/outer wire profiles at different Z levels
- **T-slot cut** — 45°-rotated 8-point polygon profile
- **Text engravings** — build123d `Text()` objects cut into surfaces ("LEFT", "BOTTOM", "TOP")
- **Profile cuts** — arbitrary polyline profiles from coordinate files

### 5. Export
```python
export_step(combined_all.part, export_path)
```
Exports a STEP AP214 file compatible with all major CAD platforms (Fusion 360, SolidWorks, FreeCAD, etc.).

---

## Overall Dimensions

| Dimension | Value |
|---|---|
| Overall X span | ≈ −222 mm to +605 mm (~827 mm) |
| Overall Y span | ≈ −84 mm to +184 mm (~268 mm) |
| Overall Z span | Z = 10 mm to Z = 110 mm (100 mm height) |
| Arc body (left) | Radius ≈ 222 mm, height 100 mm |
| Rectangular body (right) | ≈ 463 mm × 100 mm × 100 mm |
| Arc profile body (body3) | Span ≈ 143–605 mm in X, 50 mm tall |
| Connector body (body4) | ≈ 140 mm × 100 mm × 40 mm |
| Main circular hole | Ø ≈ 82.6 mm, centre at X ≈ 555, Y = 50 |
| Inner through-holes (×2) | Ø ≈ 35 mm each |
| Small holes (×4) | Ø ≈ 14.9 mm each |
| Chamfer loft 1 | Ø 40 mm → Ø 70 mm over 17.5 mm |
| Chamfer loft 2 | Ø 35 mm → Ø 70 mm over 17.5 mm |
| T-slot cut | 45°-rotated, ~162 mm stem, ~70 mm bar |
| Text "LEFT" | Font size 35, engraved 5 mm deep |
| Text "BOTTOM" | Font size 35, engraved 5 mm deep |
| Text "TOP" | Font size 52.5, engraved 5 mm deep |

> All units are **millimetres (mm)**.

---

## File Structure

```
Elbow_left.py       # Main script — run this
README.md           # This file
```

Coordinate data is embedded directly in the script from the following source files (now inlined):

| Source | Contents |
|---|---|
| `Cut.txt` (various) | Polyline profiles for body outlines and slot cuts |
| `hole.txt` (various) | Circular hole point clouds |
| `inner.txt` | Small inner hole profiles |
| `Outer.txt` | Large outer chamfer ring profiles |

---

## Key build123d Patterns Used

```python
# Sketch from point cloud
with BuildSketch(Plane.XY.offset(z)):
    with BuildLine():
        Polyline(*pts, close=True)
    make_face()
extrude(amount=h)

# Boolean subtract
extrude(amount=depth, mode=Mode.SUBTRACT)

# Loft chamfer
wire_a = Wire.make_polygon([Vector(x, y, z1) for x, y in pts_a], close=True)
wire_b = Wire.make_polygon([Vector(x, y, z2) for x, y in pts_b], close=True)
chamfer = Solid.make_loft([wire_a, wire_b])
add(chamfer, mode=Mode.SUBTRACT)

# Text engraving
with BuildSketch(Plane(origin=(x, y, z), x_dir=(1,0,0), z_dir=(0,0,1))):
    Text("LABEL", font_size=35, align=(Align.CENTER, Align.CENTER))
extrude(amount=5, mode=Mode.SUBTRACT)
```

---

## License

MIT — free to use, modify, and distribute.
