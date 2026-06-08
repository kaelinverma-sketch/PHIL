# Parametric CAD Model — build123d

A multi-body parametric solid model built entirely in Python using [build123d](https://github.com/gumyr/build123d), exported as a STEP file for use in any CAD application.

---

## Repository Contents

| File | Description |
|------|-------------|
| `extrude_shape.py` | Full build script — runs end-to-end to reconstruct and export the model |
| `model.step` | Exported STEP file (AP203, millimetres) |
| `README.md` | This file |

---

## Requirements

```bash
pip install build123d ocp_vscode
```

- Python 3.10+
- [build123d](https://github.com/gumyr/build123d) — geometry kernel
- [ocp_vscode](https://github.com/bernhard-42/vscode-ocp-cad-viewer) — live viewer (optional; viewer warnings are harmless without VS Code open)

Run the script:

```bash
python extrude_shape.py
```

The model is rebuilt from scratch each run and exported as `model.step` to `~/Desktop/`.

---

## Overall Dimensions

| Dimension | Value |
|-----------|-------|
| Overall width (X) | **345.14 mm** |
| Overall depth (Y) | **695.41 mm** |
| Overall height (Z) | **96.25 mm** |
| Bounding box X | −172.57 → +172.57 mm |
| Bounding box Y | −347.71 → +347.71 mm |
| Bounding box Z | 0 → 96.25 mm |

---

## Model Structure

The model comprises three separate bodies combined into a single compound, with six sets of subtractive operations applied across them.

### Body 1 — Lower Ring (negative Y)

| Property | Value |
|----------|-------|
| Profile | 100-point closed polyline — large elliptical ring |
| Centre | (0, −175) mm |
| Footprint | 345 × 345 mm |
| Extrusion height | 50 mm (+Z) |
| Z range | 0 → 50 mm |
| Volume (after cuts) | ~3,837,327 mm³ |

### Body 2 — Central Collar

| Property | Value |
|----------|-------|
| Profile | 190-point closed polyline — double-lobe figure-eight |
| Centre | (0, −175) mm |
| Footprint | 242 × 241 mm |
| Extrusion height | 46.25 mm (−Z from top face) |
| Z range | 50 → 96.25 mm |
| Volume (after cuts) | ~1,121,637 mm³ |

### Body 3 — Upper Ring (positive Y)

| Property | Value |
|----------|-------|
| Profile | 99-point closed polyline — large elliptical ring (mirror of Body 1 in Y) |
| Centre | (0, +175) mm |
| Footprint | 345 × 345 mm |
| Extrusion height | 65 mm (+Z) |
| Z range | 0 → 65 mm |
| Volume (after cuts) | ~4,608,803 mm³ |

---

## Cut Operations

### Cut 1 — Central Through-Hole (Body 1)
Single circular pocket centred at (0, −175) mm, 31-point profile, radius ≈ 26 mm.
Depth: 60 mm in +Z (full through-cut of Body 1).

### Cut 2 — Radial Pockets × 8 (Body 1, bottom face)
Eight circular pockets arranged symmetrically at ±93.7 mm and ±132.5 mm radii.
Each pocket: 40-point profile, radius ≈ 30 mm. Depth: 35 mm from bottom face (+Z).

| Pocket | Centre (X, Y) |
|--------|---------------|
| 1 | (−132.5, −175.1) |
| 2 | (−93.7, −268.8) |
| 3 | (0, −307.6) |
| 4 | (93.6, −268.8) |
| 5 | (132.5, −175.1) |
| 6 | (93.6, −81.4) |
| 7 | (0, −42.6) |
| 8 | (−93.7, −81.4) |

### Cut 3 — Top-Face Counter-Bores × 8 (Body 1, top face)
Same 8 positions as Cut 2. 30-point profiles, radius ≈ 30 mm.
Depth: 13.5 mm from top face (z = 50 → z = 36.5 mm).

### Cut 4 — Both-Direction Through-Cut (Bodies 1 & 2)
Single circular profile centred at (0, −175) mm, radius ≈ 26 mm.
Sketch plane at z = 48.125 mm; cut extends ±100 mm, punching through both bodies.

### Cut 5 — Radial Pockets × 9 (Body 3, bottom face)
Nine pockets on the upper ring: eight circular (radius ≈ 30 mm) matching the Body 1
radial pattern but mirrored to positive Y, plus one larger central pocket (radius ≈ 52 mm)
centred at (0, +175) mm. Depth: 100 mm (+Z, full through-cut).

| Pocket | Centre (X, Y) | Radius |
|--------|---------------|--------|
| 1 | (−93.7, 81.4) | ~30 mm |
| 2 | (0, 42.6) | ~30 mm |
| 3 | (−132.5, 175.1) | ~30 mm |
| 4 | (−93.7, 268.8) | ~30 mm |
| 5 | (93.6, 81.4) | ~30 mm |
| 6 | (132.5, 175.1) | ~30 mm |
| 7 | (93.6, 268.8) | ~30 mm |
| 8 | (0, 307.6) | ~30 mm |
| 9 | (0, 175.1) | ~52 mm |

### Cut 6 — Hexagonal Pockets × 8 (Body 3, top face)
Eight regular hexagons, circumradius ≈ 34.6 mm, arranged at the same 8 radial positions
as Cut 5 (loops 1–8). Sketch plane at z = 65 mm (Body 3 top face); depth: 50 mm downward.

| Hex | Centre (X, Y) |
|-----|---------------|
| 1 | (93.6, 81.4) |
| 2 | (0, 42.6) |
| 3 | (−93.7, 81.4) |
| 4 | (−132.5, 175.1) |
| 5 | (−93.7, 268.8) |
| 6 | (0, 307.6) |
| 7 | (93.6, 268.8) |
| 8 | (132.5, 175.1) |

---

## Methodology

### Coordinate Source
All geometry is derived from point arrays extracted from the original design files
(`extrude.txt` and `Cut.txt`). Each file contains XYZ coordinates at a constant Z value
that encodes the face from which the feature originates:

| Source Z | Interpretation |
|----------|----------------|
| `z = −48.125` | Bottom face of original model → sketch on `Plane.XY` (z = 0), extrude +Z |
| `z = +1.875` | Top face of original model → sketch on top face (z = 50 or z = 65), extrude −Z |
| `z = +16.875` | Top face of Body 3 → sketch at z = 65, extrude −Z |
| `z = +48.125` | Mid-plane → sketch at z = 48.125, `both=True` extrusion |

### Point Ordering Fixes
Several input files contained vertices in non-sequential angular order, causing
self-intersecting polygons that fail face construction. These are corrected by sorting
points by their angle from the profile centroid before building the polyline:

```python
cx = sum(p[0] for p in pts) / len(pts)
cy = sum(p[1] for p in pts) / len(pts)
pts = sorted(pts, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
```

Affected profiles: Body 3 outer profile (2 points), Cut 2 Loop 3, Cut 5 Loop 6, Cut 6 Hex 4, Cut 6 full polygon.

### Build Strategy
Each body is built inside its own `BuildPart` context. Cuts are applied by re-entering
the relevant context with `with part:` after the body is complete. All three bodies are
combined into a `Compound` for display and STEP export.

```python
# Example pattern used throughout
with BuildPart() as part:
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*profile_pts, close=True)
        make_face()
    extrude(amount=50)

# Re-enter to subtract features
with part:
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*cut_pts, close=True)
        make_face()
    extrude(amount=35, mode=Mode.SUBTRACT)

# Combine all bodies
combined = Compound([part.part.solids()[0],
                     part2.part.solids()[0],
                     part3.part.solids()[0]])

# Export
export_step(combined, "~/Desktop/model.step")
```

### Volume Summary

| Component | Volume |
|-----------|--------|
| Body 1 (after all cuts) | 3,837,327 mm³ |
| Body 2 (after cuts) | 1,121,637 mm³ |
| Body 3 (after all cuts) | 4,608,803 mm³ |
| **Combined total** | **9,567,744 mm³** |

---
