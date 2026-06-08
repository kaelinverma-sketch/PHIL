# CAD Model — build123d

A parametric solid built with [build123d](https://github.com/gumyr/build123d), featuring a slot cut, circular hole cuts, and fillets. The final model is exported as a STEP file for use in any CAD environment.

---

## Overall Dimensions

| Dimension | Value |
|---|---|
| Width (X) | 105 mm |
| Length (Y) | 425 mm |
| Height (Z) | 125 mm |
| Volume | ≈ 1,850,480 mm³ |

**Bounding box:** X: −105 to 0 · Y: −212.5 to +212.5 · Z: 0 to 125

---

## File Structure

```
├── extrude_cut.py      # Main build script
├── extrude.txt         # H-profile base polygon points
├── Cut.txt             # Slot cut profile points (YZ plane)
├── hole.txt            # Circular hole profile points (YZ plane at X=-50)
├── h_profile_model.step  # Exported STEP file (written to Desktop on run)
└── README.md
```

---

## Dependencies

```bash
pip install build123d ocp-vscode
```

- **build123d** — Python CAD library (OpenCASCADE kernel)
- **ocp-vscode** — OCP CAD Viewer for in-editor 3D preview

---

## Running the Script

```bash
python extrude_cut.py
```

The script will:
1. Build the solid and display it in the OCP CAD Viewer
2. Export `h_profile_model.step` to `~/Desktop/`

---

## Methodology

### Step 1 — Base H-Profile Extrusion

The H-shaped cross-section is defined by 12 polygon vertices in the XY plane (from `extrude.txt`). The profile consists of two flanges connected by a central web, with a rectangular notch on the web side. The polygon is closed with `Polyline(..., close=True)`, filled into a face with `make_face()`, then extruded **125 mm along +Z**.

```
H cross-section (XY plane):
  Flanges : Y = ±62.5 to ±212.5,  X = −50 to −75
  Web     : Y = −62.5 to +62.5,   X = −50 to   0
  Stub    : Y = −20   to  +20,    X = −75 to −105
```

**Key coordinate fix:** The profile points were used directly as supplied. No reordering was needed for the base polygon.

---

### Step 2 — Slot Cut (Cut.txt)

The slot profile is defined by 38 points lying on the YZ plane (X = 0 constant). The shape is an open-top slot:

- **Left wall:** Y = −22.5, Z from 104.99 down to 42.49
- **Semicircular floor:** centre (Y = 0, Z = 42.49), R = 22.5 mm
- **Right wall:** Y = +22.5, Z from 42.49 up to 104.99
- **Top:** closed automatically by `Polyline(..., close=True)`

**Point ordering fix:** One arc point (`[36] = (22.4219, 40.4718)`) was out of angular order. All 35 arc points (indices 1–36) are sorted by angle relative to the semicircle centre before building the wire, preventing a self-intersecting profile.

The sketch plane is offset **+20.02 mm in Z** (`origin = (0, 0, 20.02)`) while keeping the normal along +X. The profile is extruded **±150 mm along X** (`both=True`) to cut all the way through.

```
Slot dimensions:
  Width  : 45 mm  (Y: −22.5 to +22.5)
  Height : 85 mm  (Z: 20.01 to 104.99, after offset: 40.03 to 124.99)
  Depth  : 150 mm each side along X
```

---

### Step 3 — Circular Hole Cuts (hole.txt)

Two circular holes are defined by 110 sampled points lying on a plane at X = −50 (constant). Centres and radii are derived analytically from the point cloud:

```
  Centre = ( (max + min) / 2 ) for Y and Z independently
  Radius = (max_Y − min_Y) / 2
```

| | Y centre | Z centre | Radius |
|---|---|---|---|
| Hole 1 | −150.0 mm | 42.4777 mm | 13.5 mm |
| Hole 2 | +150.0 mm | 42.4777 mm | 13.5 mm |

The sketch plane is `Plane(origin=(-50, 0, 20.02), x_dir=(0,1,0), z_dir=(1,0,0))` — positioned at the flange face (X = −50) with the same Z offset as the slot, normal along +X. `Circle(radius=13.5)` gives clean cylindrical geometry. Extruded **±100 mm along X**.

**Key insight:** Placing the sketch on `Plane.YZ` (X = 0) would miss the solid entirely — the flanges only exist at X = −50 to −75. The `z_dir=Vector(1,0,0)` parameter is critical; using `z_dir=(0,0,1)` rotates the normal to Z and cuts in the wrong direction.

---

### Step 4 — Fillet: 25 mm Flange Edges (along X)

All 6 edges that run along the X axis with length ≈ 25 mm (the flange thickness edges, X: −50 ↔ −75) are selected programmatically and filleted with **R = 20 mm**.

Selection filter:
```python
e.geom_type == GeomType.LINE
and abs(e.start_point().Y - e.end_point().Y) < 0.01   # constant Y
and abs(e.start_point().Z - e.end_point().Z) < 0.01   # constant Z
and abs(e.length - 25.0) < 1.0                         # length ≈ 25 mm
```

---

### Step 5 — Fillet: Stub Side Wall Edge (along Y at X = −105)

The 40 mm edge along Y at X = −105 (the outer face of the central stub) is filleted with **R = 20 mm**.

A tiny slot-remnant edge (~2 mm) also sits at X = −105 after the slot cut. It is excluded by adding `e.length > 5.0` to the filter — attempting to fillet it at R = 20 mm would fail as the radius exceeds the edge length.

---

### Step 6 — STEP Export

```python
export_step(part.part, os.path.expanduser("~/Desktop/h_profile_model.step"))
```

Uses build123d's built-in `export_step()` function. The STEP AP214 format is compatible with CATIA, SolidWorks, Fusion 360, FreeCAD, and all major CAD tools.

---
