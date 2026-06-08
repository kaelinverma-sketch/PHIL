# Build123d Parametric CAD Model

A Python script that constructs a multi-body parametric solid model using [build123d](https://github.com/gumyr/build123d), visualised live in [OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer), and exported to STEP format.

---

## Requirements

```bash
pip install build123d ocp-vscode
```

- Python 3.10+
- `tkinter` (included in the Python standard library)
- VS Code with the [OCP CAD Viewer extension](https://marketplace.visualstudio.com/items?itemName=bernhard-42.ocp-vscode) for live visualisation

---

## Usage

```bash
python extrude_both.py
```

On every run a **Save As** dialog will appear prompting you to choose the export location and filename for the `.step` output. Cancelling skips the export without error.

---

## Methodology

The script builds each body independently from a set of 3D coordinate points, detects the constant axis to identify the sketch plane, constructs a closed 2D polygon from the remaining two axes, extrudes it to the required height, and finally combines everything using Boolean operations.

### Step-by-step

1. **Plane detection** — for each set of input points the constant axis is identified (X, Y, or Z). That axis becomes the extrusion direction and the other two define the sketch plane.

2. **Sketch construction** — points are projected onto the sketch plane, wound into the correct CCW order where needed, and fed into a `Polyline` inside a `BuildSketch` context. `make_face()` converts the closed wire into a filled face.

3. **Extrusion** — `extrude(sketch, amount=N)` produces a solid body along the detected axis.

4. **Boolean union** — Bodies 1–4 are merged into a single solid with `body1 + body2 + body3 + body4`.

5. **Extrude-cut (profile)** — A 21-point irregular polygon sketched on the XZ plane is extruded 7 mm along +Y and subtracted from the fused solid (`fused - cut_tool`).

6. **Extrude-cut (cylinder)** — A 46-point circular profile (Ø10 mm) is sketched on the XY plane, translated to position (−38.5, +3.5) in XY, extruded 80 mm along +Z, and subtracted from the result.

7. **Visualisation** — `show()` from `ocp_vscode` renders the final body live in OCP CAD Viewer.

8. **STEP export** — `export_step()` writes the final solid to a user-chosen path via a `tkinter` file dialog.

---

## Model Overview

### Individual bodies (before Boolean ops)

| Body | Shape | Sketch Plane | Extrusion | Dimensions (X × Y × Z) |
|------|-------|-------------|-----------|------------------------|
| Body 1 | Rectangle | XY @ Z = −95.165 | 18 mm along +Z | 130 × 164 × 18 mm |
| Body 2 | Trapezoid | XZ @ Y = −53.501 | 100 mm along +Y | 100 × 100 × 38.6 mm |
| Body 3 | Trapezoid | XZ @ Y = −33.501 | 60 mm along +Y | 100 × 60 × 37.6 mm |
| Body 4 | Trapezoid | XZ @ Y = −53.501 | 100 mm along +Y | 100 × 100 × 47.6 mm |

### Boolean cuts

| Cut | Shape | Direction | Depth | Position |
|-----|-------|-----------|-------|----------|
| Profile cut | 21-pt irregular polygon | +Y | 7 mm | XZ @ Y = −6.9995 |
| Cylinder cut | Ø10 mm circle | +Z | 80 mm | Centre (−38.5, +3.5), base Z = −58.205 |

### Overall bounding box (final model)

| Axis | Range | Total span |
|------|-------|-----------|
| X | −95.03 → +34.97 | **130.00 mm** |
| Y | −85.50 → +78.50 | **164.00 mm** |
| Z | −95.17 → +21.79 | **116.96 mm** |

---

## File Structure

```
.
├── extrude_both.py   # Main script — builds, visualises, and exports the model
└── README.md         # This file
```

---

## License

MIT
