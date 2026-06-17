# Set_3 — CAD Assembly Script

**Project:** PHIL — ETH Zurich Cell Systems Dynamics Group
**Author:** Softage (kaelin.verma@softage.ai)
**Script:** `Set3.py` / `Set_3_master.py`
**Toolchain:** Python 3.11 · build123d · OpenCASCADE (OCC) · OCP CAD Viewer

---

## Overview

`Set_3_master.py` programmatically reconstructs a complex multi-body CAD assembly from real-world survey coordinate data. It produces **three solid bodies**:

| Body | Description |
|---|---|
| `my_part` | Main cylinder solid (Solid 1, positive-X side) |
| `my_part_mirrored` | YZ-plane mirror of Solid 1 (Solid 2, negative-X side) |
| `profile_solid` | Separate frame/bracket body from `profiles.json` |

All coordinates are sourced from external survey text files and a JSON profile, translated into build123d/OCC geometry.

---

## Overall Dimensions

| Dimension | Value |
|---|---|
| Total height (Z) | **397.5 mm** |
| Outer diameter (Profile 1, Z=0–25) | ~528 mm (±264 mm in X/Y) |
| Outer diameter (Profile 3, Z=30–397.5) | ~472 mm (±236 mm in X) |
| Base transition height | 30 mm |
| Profile solid height | 27.5 mm |
| Profile solid outer span | ~335 mm (±167 mm) |
| Profile solid inner cutout diameter | ~93 mm (r≈46.5, centred ±80 mm) |

---

## Methodology

### 1. Coordinate-Driven Profile Construction

All 2D cross-sections are defined by survey point lists in (X, Y, Z) format. A custom `sort_and_sanitize_points()` function applies a **Nearest-Neighbour algorithm** to order points into a non-self-intersecting closed boundary before building wires.

For **non-convex profiles**, OCC's `BRepBuilderAPI_MakeFace` is called directly with an explicit `gp_Pln`, bypassing build123d's `make_face()` which fails on concave geometry.

### 2. Three-Stage Main Body Extrusion

The main cylinder is built in three stacked extrusions inside a `BuildPart` context:

| Stage | Z Range | Height | Profile |
|---|---|---|---|
| Profile 1 | 0 → 25 mm | 25 mm | Outer circular arc with inner D-shape |
| Profile 2 | 25 → 30 mm | 5 mm | Transition profile (narrowing) |
| Profile 3 | 30 → 397.5 mm | 367.5 mm | Final outer cylinder profile |

### 3. Boolean Cut Operations

All cuts are applied sequentially. Cuts inside `BuildPart` use `extrude(mode=Mode.SUBTRACT)`; post-context cuts use `BRepAlgoAPI_Cut` directly.

| Cut | Plane | Depth | Description |
|---|---|---|---|
| Cut v1 (rect) | Z=397.5 | −370 mm | Rectangular through-cut |
| Cut v1 (circ) | Z=397.5 | −370 mm | Circular through-cut |
| Cut v2 (pocket 1) | Z=397.5 | −48.5 mm | Oval pocket |
| Cut v2 (pocket 2) | Z=397.5 | −48.5 mm | Oval pocket (mirrored) |
| Cut v3 (slanted) | 45° diagonal plane | −25 mm | Notch on diagonal face |
| Cut v4b | Z=322.5 | +25 mm | 6-point polygon cut |
| Cut v4 | Z=347.5 | −25 mm | 8-point octagonal cut |
| Cut v5 | Z=322.5 | −222.5 mm | Circular deep pocket |
| Cut v5b | Z=322.5 | −222.5 mm | Secondary circular deep pocket |
| Cut Outer | 45° diagonal plane | −50 mm | r=30 mm circular cut |
| Cut Inner | 45° diagonal plane | +50 mm | r=17.5 mm circular cut |
| Chamfer Loft | 45° diagonal plane | — | Truncated cone (ThruSections) |
| Top flat cut | Z=397.5 | −5 mm | L-shaped notch (6 points) |
| Big R cut | XZ plane | +50 mm | Font-size-140 letter R |
| Big L cut | XZ plane | +50 mm | Font-size-140 letter L (Solid 2) |

### 4. Diagonal Plane Convention

Cuts on the 45° diagonal plane use:
```
x_dir = (1, -1, 0)   # in-plane horizontal
z_dir = (-1, -1, 0)  # inward normal
```
This convention is consistent across all diagonal-plane operations (Cut v3, Cut Outer, Cut Inner, Chamfer Loft).

### 5. Chamfer Loft

A ruled loft (`BRepOffsetAPI_ThruSections`, `solid=True`, `ruled=True`) connects:
- Outer circle: r=30 mm at `(179.33, 60.09, 100.0)` on the diagonal plane
- Inner circle: r=17.5 mm at `(167.55, 48.31, 100.0)` on the diagonal plane

This creates a linear chamfer (truncated cone) subtracted from the body.

### 6. Fillets

| Fillet | Location | Radius |
|---|---|---|
| Rectangular cut edges | Z=30 (bottom of rect cut) | 20 mm |
| Top face rect cut edges | Z=397.5 | 20 mm |

Edge selection uses centre-point proximity matching (tolerance 2–5 mm).

### 7. Auxiliary Extrusions & Fusions

- **Extrude Part**: convex profile (62-point arc) extruded 50.2 mm from Z=0, fused into `my_part`
- **Cut Extrude**: 41-point convex profile cut 55 mm from Z=0
- **8-point non-convex cut**: 45 mm from Z=0, built with OCC `BRepBuilderAPI_MakeFace` + `gp_Pln`

### 8. Text Engravings

| Text | Size | Location | Body |
|---|---|---|---|
| "TOP" | 70 pt | Side wall at X=+225, Z≈0–5 | Solid 1 |
| "TOP" (mirrored) | 70 pt | Side wall at X=−225, Z≈0–5 | Solid 2 |
| "R" | 34 pt | Top face at (170, −15, 397.5) | Solid 1 only |
| "L" | 34 pt | Top face at (−200, −10, 397.5) | Solid 2 only |
| "R" (large) | 140 pt | XZ plane at (120, −152, 210), 50 mm deep | Solid 1 |
| "L" (large) | 140 pt | XZ plane at (−120, −152, 210), 50 mm deep | Solid 2 |

Text faces are assembled with `BRepBuilderAPI_MakeFace` using `_wire_area` sorting to correctly identify outer contours vs. counter holes (e.g. the bowl of "R").

### 9. Mirroring

`my_part_mirrored` is created by reflecting `my_part` through the **YZ plane** using `gp_Trsf.SetMirror`. The mirror is applied **after** all cuts to `my_part`, so:
- Unique cuts (R, TOP) are applied to `my_part` after mirroring
- Unique cuts (L, TOP mirrored) are applied separately to `my_part_mirrored`

### 10. Profile Solid (`profiles.json`)

A separate frame body is extruded from a JSON profile (`Face_1_n(0.0,0.0,-1.0)`) containing 198 line segments. The single closed loop encodes three wires:

| Wire | Indices | Description |
|---|---|---|
| Outer frame | 0–50 + 92–149 + 191–197 | Full outer boundary |
| Right hole | 51–91 | Circular cutout, centre (+80, 0), r≈46.5 |
| Left hole | 150–190 | Circular cutout, centre (−80, 0), r≈46.5 |

The outer solid is extruded 27.5 mm in +Z, then the two hole solids are boolean-cut out.

---

## Export

The assembly is exported to the Desktop as:

```
/Users/softage/Desktop/Set_3.step
/Users/softage/Desktop/Set_3.stl
```

All three bodies (`my_part`, `my_part_mirrored`, `profile_solid`) are combined into a `Compound` before export.

---

## Dependencies

```
build123d
OCP (OpenCASCADE Python bindings)
ocp_vscode (OCP CAD Viewer)
numpy
tkinter (stdlib)
json (stdlib)
```

## Environment

- macOS (Apple Silicon)
- Python 3.11 via Homebrew
- OCP CAD Viewer on port 3940
- Virtual environment: `.venv`
