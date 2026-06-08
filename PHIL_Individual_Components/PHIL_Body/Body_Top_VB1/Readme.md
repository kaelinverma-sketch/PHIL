# Body Top — Parametric CAD Model

A fully parametric enclosure body modelled in Python using [build123d](https://github.com/gumyr/build123d), an open-source code-based CAD library built on OpenCASCADE. The script generates a complex mechanical body with all features driven by variables, making it easy to modify dimensions and regenerate.

---

## Overall Dimensions

| Parameter | Value |
|-----------|-------|
| Length (X) | 1960.94 mm |
| Width (Y) | 640.00 mm |
| Height (Z) | 372.50 mm |
| Wall / top thickness | 50 mm |

The body sits with one corner at the world origin `(0, 0, 0)`.

---

## Methodology

The model is built entirely in Python through sequential boolean operations inside a single `BuildPart` context. Each feature is added or subtracted from the previous state, following a logical construction order:

**1. Base solid** — A full rectangular box at the world origin.

**2. Hollow shell** — The interior is removed by boolean subtraction, leaving 50 mm walls on the front and back faces (±Y), a 50 mm top face, and open left, right, and bottom faces.

**3. Extrude cuts** — Two rectangular through-cuts are applied: a centred 940.94 × 540 mm slot through the full height, and a 650.94 × 50 mm opening centred on the front wall.

**4. Slot cuts (back face)** — Two true slot profiles (rectangle + semicircular ends, 100.04 × 226.30 mm total) are cut 50 mm deep into the back face, one on each side, symmetrical about the model centre.

**5. Top face features** — A series of cuts on the 50 mm thick top wall:
- A 60 × 140 mm rectangular pocket
- A Ø233.47 mm circular through-hole
- A Ø370 mm × 23.5 mm counterbore on the underside of the top wall, concentric with the large hole
- 4 × Ø35 mm holes in a rectangular pattern around the large hole, each with a 24 mm slant conical countersink
- All top-face features are mirrored symmetrically about X = LENGTH/2

**6. Corner posts** — Four solid bodies (100 × 50 × 322.5 mm with a convex quarter-circle fillet on the inner corner, r = 50 mm) are placed at each corner of the model, offset 50 mm from the front/back edges. Each post is unioned into the main body. A Ø70 mm × 322.5 mm blind hole and a Ø35 mm through-hole are drilled concentrically at each post.

**7. Side face holes** — Two Ø15 mm × 55 mm holes are drilled into each of the left and right faces at Z = 347.5 mm, centred at Y = 325 mm and Y = 256.02 mm respectively.

**8. Chamfer cuts** — Conical countersinks (slant 24 mm, 45°) are applied at Z ≈ 322–339 mm on the four Ø35 mm holes, on both the left and right sides.

**9. Text emboss** — "Z1" and "Z2" are engraved 10 mm deep into the top face using 100 mm Bold Arial text, placed symmetrically at X = 319.32 and X = 1641.62, Y = 525.26.

---

## Features at a Glance

| Feature | Count | Details |
|---------|-------|---------|
| Hollow shell | 1 | Open left/right/bottom, T=50 mm |
| Rectangular extrude cuts | 2 | Through full height |
| Back-face slot cuts | 2 | Slotted profile, 50 mm deep |
| Large circular hole | 2 | Ø233.47 mm, mirrored |
| Counterbore | 2 | Ø370 mm × 23.5 mm, mirrored |
| Small bolt holes | 8 | Ø35 mm, 4 per side, mirrored |
| Conical countersinks | 8 | 24 mm slant, 45°, mirrored |
| Corner posts | 4 | 100×50×322.5 mm, fillet r=50 |
| Corner cylinder bores | 4 | Ø70 mm × 322.5 mm |
| Corner through-holes | 4 | Ø35 mm full height |
| Side face holes | 4 | Ø15 mm × 55 mm per side |
| Text emboss | 2 | Z1, Z2 engraved 10 mm deep |

---

## Requirements

```bash
pip install build123d ocp-vscode
```

- **Python** 3.10+
- **build123d** — parametric CAD kernel
- **ocp-vscode** — OCP CAD Viewer extension for VS Code (optional, for live 3D preview)

---

## Usage

```bash
python Body_Top.py
```

On run the script will:
1. Build the full model
2. Display it in the OCP CAD Viewer panel (if open in VS Code)
3. Open a **save dialog** prompting you to choose a location for the exported `.step` file

To open the OCP CAD Viewer panel first:
> VS Code → `Cmd/Ctrl+Shift+P` → `OCP CAD Viewer: Open Viewer`

---

## Key Variables

All dimensions are defined at the top of the script for easy modification:

```python
LENGTH    = 1960.94   # mm  outer X
WIDTH     =  640.00   # mm  outer Y
HEIGHT    =  372.50   # mm  outer Z
T         =   50.00   # mm  wall / top thickness
```

---
