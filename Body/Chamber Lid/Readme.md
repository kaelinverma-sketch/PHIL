# Chamber Lid — Parametric CAD Model

A fully parametric **Chamber Lid** modelled in Python using [build123d](https://github.com/gumyr/build123d), designed for the **Cell Systems Dynamics Group, ETH Zurich**.

> Designed by Philip Dettinger

---

## Overview

The script constructs a multi-step chamber lid geometry through a sequence of boolean operations — extrusions, subtractions, holes, chamfers, and engraved text — all driven by precise coordinate and dimension inputs. The final model is previewed in [OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer) and exported to STEP format via a save dialog.

---

## Overall Dimensions

| Feature | Value |
|---|---|
| Outer footprint (XY) | 1960.98 mm × 1983.75 mm |
| Total height (Z) | 105.75 mm |
| Base profile | 6-point polygon (trapezoid-like) |

---

## Methodology

### 1. Base Body (Body 1)
A 6-point closed polygon is sketched in the XY plane and extruded to **105.75 mm** in Z. This forms the outer shell of the lid.

Vertices: `(0,0)` → `(0,500)` → `(420.27,1983.75)` → `(1540.47,1983.75)` → `(1960.98,500)` → `(1960.98,0)`

### 2. Inner Recess (Body 2 cut)
A second, inset polygon (offset ~100 mm on each side) is extruded to **55.75 mm**, offset **+50 mm** in Z, and subtracted from Body 1 — creating a stepped inner recess in the top face.

### 3. Central Pocket (Box 1 cut)
A **965 × 1415 × 110 mm** box, positioned at `(497.97, 466.25, 0)`, is subtracted to create the main central cavity.

### 4. Shallow Ledge (Box 2 cut)
A **1005 × 1455 × 30 mm** box, positioned at `(477.97, 446.25, 0)`, is subtracted to create a shallow stepped ledge around the central pocket.

### 5. Mounting Holes
Five counterbored holes are cut at the following XY centres:

| Hole | X | Y |
|---|---|---|
| 1 | 50.01 | 243.07 |
| 2 | 249.04 | 1184.93 |
| 3 | 980.48 | 1933.77 |
| 4 | 1712.93 | 1184.93 |
| 5 | 1910.98 | 243.07 |

Each hole consists of three coaxial features:
- **Counterbore**: Ø70 mm × 30 mm deep
- **Chamfer**: conical frustum Ø70 mm → Ø35.62 mm × 20 mm, offset +30 mm in Z
- **Through-hole**: Ø35.62 mm, full depth

### 6. Hollow Rectangular Wall (separate body)
A hollow rectangular frame — outer **990 × 1440 mm**, inner **965 × 1415 mm**, height **27.5 mm**, wall thickness **12.5 mm** — is created as a separate body and positioned at `(485.47, 453.75, 0)`.

### 7. Engraved Text
Three lines of text are engraved into the base face (cut in +Z, 6 mm deep), positioned at `(400, 343, 0)`:

```
ETH Zurich
Cell Systems Dynamics Group
Designed by Philip Dettinger
```

Font size: **83.14 mm** (69.28 mm × 1.2), left-aligned, line spacing 1.5×.

---

## Dependencies

```bash
pip install build123d ocp-vscode
```

| Package | Purpose |
|---|---|
| `build123d` | Parametric CAD modelling |
| `ocp-vscode` | In-editor 3D viewer (OCP CAD Viewer) |
| `tkinter` | Save dialog for STEP export (bundled with Python) |

---

## Usage

```bash
python Chamber_Lid.py
```

1. The model renders in **OCP CAD Viewer**.
2. A **Save As** dialog appears — choose a location and filename to export the model as a `.step` file.
3. Cancelling the dialog skips the export without error.

---

## Output

The script produces two named bodies in the viewer:

- `final_result` — the main lid with all cuts, holes, chamfers, and engraved text
- `hollow_wall` — the separate rectangular wall frame

Both are combined and exported together in the STEP file.

---

## License

For internal use — Cell Systems Dynamics Group, ETH Zurich.
