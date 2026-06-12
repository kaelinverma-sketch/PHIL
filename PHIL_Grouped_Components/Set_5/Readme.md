# Set_5 — Multi-Part CAD Assembly

**PHIL Project** | Cell Systems Dynamics Group, ETH Zurich
Original designs by Philip Dettinger | Programmatic reconstruction by Softage (softage.ai)

---

## Overview

`Set_5.py` is a build123d Python script that constructs and assembles 9 parametric CAD bodies from real-world survey coordinates and geometric profiles. All bodies are displayed together in the OCP CAD Viewer and exported as a single compound to `Set_5.step` and `Set_5.stl`.

---

## Files

| File | Description |
|------|-------------|
| `Set_5.py` | Main assembly script |
| `Set_5.step` | STEP export of full assembly |
| `Set_5.stl` | STL export of full assembly |

---

## Assembly Parts

| # | Name | Colour | Description |
|---|------|--------|-------------|
| 1 | Blue Body | `#5588CC` | Revolved stack + cut, moved (+970, +850, 0) |
| 2 | Red Body | `#CC5533` | Copy of Blue Body + top extrude, moved (+1092, +864.5, 0) |
| 3 | Chamber Lid | `#44AA66` | Extruded polygon lid with box cuts, holes, chamfers, text |
| 4 | Hollow Wall | `#AAAAAA` | Rectangular hollow wall frame |
| 5 | Handle | `#3498DB` | Swept 100×100 rectangle along U-path with fillets and cylinders |
| 6 | Base Cut | `#2ECC71` | Handle base plate with handle cutout, moved (+952.5, +1771.3, 0) |
| 7 | Extrude Body | `#F39C12` | Handle bracket extrude, moved (+952.5, +1771.3, 0) |
| 8 | USB Back VB1 | `#E74C3C` | H-profile with slot cut, circular holes, fillets, moved (+1222.15, +1193.8, 0) |
| 9 | USB Front VB1 | `#9B59B6` | Rectangular base with lofted chamfer cuts, holes, corner fillets, cut profile, moved (+1001, +1191.8, 0) |

---

## Overall Dimensions

| Part | Approx. X (mm) | Approx. Y (mm) | Approx. Z (mm) |
|------|---------------|---------------|---------------|
| Blue Body (revolved stack) | ~96 dia | ~96 dia | ~50 |
| Red Body (+ top extrude) | ~96 dia | ~96 dia | ~80 |
| Chamber Lid | ~1961 | ~1984 | ~106 |
| Hollow Wall | ~990 | ~1440 | ~27.5 |
| Handle | ~555 | ~1300 | ~135 |
| Base Cut | ~528 | ~1300 | ~25 |
| Extrude Body | ~50 | ~100 | ~25 |
| USB Back VB1 | ~300 | ~425 | ~125 |
| USB Front VB1 | ~125 | ~425 | ~30 |

---

## Methodology

### Coordinate System

All bodies using real-world survey coordinates are normalised to a shared local origin:

```python
ORIGIN_X = 538088.7891
ORIGIN_Y = 235945.5469
```

Z values are used directly as sketch plane heights.

---

### Blue Body & Red Body (Parts 1 & 2)

**Construction — 5 stacked sections, pre-built then fused:**

The profile originates from survey coordinates where all points share a constant Y value, defining a circular cross-section in the XY plane at successive Z levels.

1. **Body 1** — `extrude.txt` (42 pts, r≈48mm) sketched at z=50.35, extruded 10mm in −Z → z=40.35
2. **Body 2** — Chamfer loft between `Outer.txt` (42 pts, r≈48mm, z=40.35) and `inner.txt` (38 pts, r≈40mm, z=30.35) using `loft(ruled=True)`
3. **Body 3** — `inner.txt` circle (r≈40mm) sketched at z=30.35, extruded 10mm in −Z → z=20.35
4. **Body 4** — Chamfer loft between inner profile (r≈40mm, z=20.35) and outer profile (r≈48mm, z=10.35)
5. **Body 5** — `Outer.txt` circle (r≈48mm) sketched at z=10.35, extruded 10mm in −Z → z=0.35

All five sections are built in independent `BuildPart` contexts, extracted with `.solids()[0]`, then fused via `.fuse()` chaining.

**Cut tool** — `Cut.txt` (24 pts, r≈8.5mm) extruded `both=True` 70mm from z=50.35, cutting z=−19.65→120.35 through the full stack.

**Red Body** is a `copy()` of the fused Blue Body, additionally fused with a new 30mm upward extrude from `extrude.txt` (sorted by angle to fix 4 out-of-order source points).

---

### Chamber Lid (Part 3)

**Construction:**

1. **Body 1** — 6-point polygon extruded 105.75mm in +Z
2. **Body 2** — Inner 6-point polygon extruded 55.75mm, translated +50mm in Z, subtracted from Body 1
3. **Box cut 1** — `Box(965, 1415, 110)` translated to (497.97, 466.25, 0), subtracted
4. **Box cut 2** — `Box(1005, 1455, 30)` translated to (477.97, 446.25, 0), subtracted
5. **Holes** — 5 × `Cylinder(r=35, h=30)` counterbore cuts at specified XY locations
6. **Through-holes** — 5 × `Cylinder(r=17.81, h=1000)` through-hole cuts
7. **Chamfer cones** — 5 × `Cone(r_bottom=35, r_top=17.81, h=20)` loft frustums offset +30mm in Z
8. **Text** — Three lines ("ETH Zurich", "Cell Systems Dynamics Group", "Designed by Philip Dettinger") embossed using `Text()` on a custom plane, extruded 6mm, fused and translated to (400, 343, 0)

**Hollow Wall** — `Box(990, 1440, 27.5)` with inner `Box(965, 1415, 27.5)` subtracted (`Mode.SUBTRACT`), translated to (485.47, 453.75, 0).

---

### Handle (Parts 5, 6, 7)

**Construction:**

1. **Sweep** — 100×100mm rectangle profile swept along a 3-edge U-shaped path (454.65 in +X → 1200 in −Y → 454.65 in −X) using `sweep(is_frenet=True, transition=Transition.RIGHT)`
2. **Inner Z fillet** — 50mm radius fillet on inner corner Z-edges (at x≈404.65)
3. **Cylinders** — Two `Circle(r=67.5)` extruded 100mm in XZ plane, translated to (−45.32, ±50, 0), mirrored about Y=−600 plane
4. **X + Arc fillets** — 30mm radius fillet on all X-axis and arc edges
5. **Y-edge fillet** — 49.9mm radius on 1240mm-long Y edges
6. **Hole cuts** — Two `Circle(r=14.975)` cylinders subtracted from handle at cylinder centres
7. **Base plate** — 38-point profile extruded −25mm from z=−134.99, translated (−46.209, 0, +67.494), cut with a copy of the handle translated −2.45mm in Z
8. **Bracket** — 11-point profile extruded 100mm from Y=−1250 plane, translated (−46.206, 0, +67.494)

All three handle bodies translated (+952.5, +1771.3, 0).

---

### USB Back VB1 (Part 8)

**Construction:**

1. **H-profile base** — 12-point H-cross-section extruded 125mm in +Z from XY plane
2. **Slot cut** — 38-point arc profile (sorted by angular order) on a YZ plane at z=20.02, extruded ±150mm in both X directions (`both=True`, `Mode.SUBTRACT`)
3. **Circular hole cuts** — Two `Circle(r=13.5)` sketched at (Y=±150, Z=42.48) on a plane at x=−50, extruded ±100mm (`both=True`, `Mode.SUBTRACT`)
4. **Flange fillets** — 20mm fillet on all 25mm-length X-axis edges (H-profile flange thickness edges)
5. **Side wall fillet** — 20mm fillet on Y-axis edge at X=−105 (stub side wall, length > 5mm)

Translated (+1222.15, +1193.8, 0).

---

### USB Front VB1 (Part 9)

**Construction:**

1. **Rectangular base** — 4-point rectangle (125×425mm) extruded 30mm in +Z
2. **Circle fitting** — `numpy.linalg.lstsq` least-squares circle fit applied to three point clouds (chamfer big, outer, inner) to extract centres and radii
3. **Chamfer lofts (×2)** — `loft()` between `Circle(r_big)` at z=30 and `Circle(r_outer)` at z=10, applied at original and Y-mirrored centre positions, subtracted from base
4. **Hole cuts (×2)** — `Circle(r_inner)` extruded from z=−10 to z=40 at original and mirrored centres, subtracted
5. **Corner fillets** — 20mm fillet on 4 vertical edges parallel to Z with length = 30mm
6. **Top face fillets** — 20mm fillet on outer rectangular perimeter edges at z=30
7. **Cut profile** — 39-point open slot profile extruded from z=−10 to z=50 (60mm), subtracted after fillets

Translated (+1001, +1191.8, 0).

---

## Requirements

| Package | Purpose |
|---------|---------|
| `build123d` | Parametric CAD geometry kernel |
| `ocp-vscode` | OCP CAD Viewer integration (port 3940) |
| `numpy` | Circle fitting for USB Front VB1 |

**Python:** 3.11 (Homebrew)
**Venv:** `/Users/softage/Downloads/PHIL-main 2/PHIL_Printable_Files/PHIL_Individual_Components/.venv/`
**OCP Viewer port:** 3940

---

## Running

```bash
cd "/Users/softage/Downloads/PHIL-main 2/PHIL_Printable_Files/PHIL_Individual_Components"
source .venv/bin/activate
python Set_5.py
```

Exports `Set_5.step` and `Set_5.stl` to `~/Desktop/` on completion.

---

## Project Context

Part of the **PHIL** project developed for the
**Cell Systems Dynamics Group, ETH Zurich**
Original design by Philip Dettinger.
Programmatic reconstruction by Softage (softage.ai).
