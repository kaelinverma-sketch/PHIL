# Chamber — build123d CAD Script

Parametric 3D model of a chamber body built entirely in Python using [build123d](https://github.com/gumyr/build123d) and visualised with [OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer).

---

## Features

- Hexagonal polygon outer profile extruded to 391.75 mm
- Inner profile pocket (open top, 30 mm floor)
- Rectangular wall frame (outer 935 × 1357.5, inner 875 × 1297.5, 50 mm tall)
- Large hollow cylinders OD=300 / ID=240 (mirrored pair) fused to body
- Small hollow cylinders OD=120 / ID=70 (mirrored pair) fused to body
- Rectangular front strip fused to body
- Through holes: ⌀240, ⌀35.62, ⌀35 (×7), ⌀70 (counterbore), ⌀60 (side, mirrored), ⌀35 (side, mirrored)
- Countersink chamfers at all stepped bore transitions
- Pentagon and pentagon-profile extrude cuts on left, right and top faces
- Engraved text (6 mm deep) on the inner floor:
  - *ETH Zurich*
  - *Cell Systems Dynamics Group*
  - *Designed by Philip Dettinger*
- STEP export with native file-save dialog on every run

---

## Requirements

```bash
pip install build123d ocp-vscode
```

- Python 3.10+
- [OCP CAD Viewer VS Code extension](https://marketplace.visualstudio.com/items?itemName=bernhard-42.ocp-cad-viewer)
- `tkinter` (bundled with standard Python)

---

## Usage

```bash
python Chamber.py
```

On run the script will:
1. Build the full chamber solid with all features
2. Display it in OCP CAD Viewer
3. Pop up a **Save As** dialog to export a `.step` file

---

## Model Overview

| Feature | Details |
|---|---|
| Overall dimensions | 1960.98 × 1983.75 × 391.75 mm |
| Outer profile | 6-point polygon |
| Inner pocket | Offset 30 mm from outer, open top |
| Wall frame height | 50 mm |
| Large bore holes | ⌀240 at (542.97, 1173.75) and mirror |
| Small bore holes | ⌀35.62 at (470.49, 413.76) and mirror |
| Top face cuts | Pentagon profiles + arrowhead (25 mm deep, −Z) |
| Side holes (Y-axis) | ⌀35 through + ⌀70 counterbore at X=50 and X=1910.96 |
| Side holes (X-axis) | ⌀60 at Y=1064.62, Z=262.49 (mirrored) |
| Text engraving | 6 mm deep, Z=30 floor, font size 79.2 |

---

## File Structure

```
Chamber.py      ← main build123d script
README.md       ← this file
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `build123d` | CAD geometry kernel (OCCT wrapper) |
| `ocp-vscode` | Live 3D viewer in VS Code |
| `tkinter` | Native file dialog for STEP export |

---

## Author

Philip Dettinger — Cell Systems Dynamics Group, ETH Zurich
