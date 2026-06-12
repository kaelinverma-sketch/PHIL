# Set_2_Assembly

Parametric 3D assembly script for the PHIL project (ETH Zurich — Cell Systems Dynamics Group).  
Built programmatically using **build123d** and visualised with **OCP CAD Viewer** in VS Code.

---

## Files

| File | Description |
|------|-------------|
| `Set_2_Assembly.py` | Combined assembly script (both bodies + export) |
| `Set_2_Assembly.step` | Exported STEP file (full assembly) |
| `Set_2_Assembly.stl` | Exported STL file (full assembly) |

---

## Assembly Overview

The assembly consists of **two independent solid bodies**:

| Body | Name | Source |
|------|------|--------|
| Part 1 | Plate Body | `Set_2_1.py` |
| Part 2 | Disc / Cover Body | `Set_2.py` |

Both are shown as separate named entries in the OCP CAD Viewer tree and exported together as a single compound into STEP and STL formats.

---

## Overall Dimensions

### Part 1 — Plate Body (after translation)

| Dimension | Value |
|-----------|-------|
| Length (X) | ~1840.9 mm |
| Width (Y) | ~570.0 mm |
| Height (Z) | ~100.0 mm (base Z=8.5409 → top Z=108.5409) |
| Cylinder height above base | 73.5 mm |
| Translation applied | −894.2 mm in X, +572 mm in Y |

### Part 2 — Disc / Cover Body

| Dimension | Value |
|-----------|-------|
| Length (X) | ~1961.0 mm (−954.2 to +1006.7) |
| Width (Y) | ~1070.0 mm (−502.5 to +567.5) |
| Height (Z) | 80.0 mm (Z=0 → Z=80) |

---

## Methodology

### Part 1 — Plate Body (`Set_2_1`)

All raw coordinates are given in a global survey coordinate system and translated to a local origin via:

```python
ORIGIN_X = 542143.75
ORIGIN_Y = 233673.9648
lx = lambda x: x - ORIGIN_X
ly = lambda y: y - ORIGIN_Y
```

The body is built through the following sequential operations:

#### 1. Base Extrude — Shape 1
A **48-point closed racetrack polyline** profile (rounded ends, straight sides with a notched tab extension) is sketched at `Z=8.5409` and extruded **+50 mm** upward to `Z=58.5409`.

#### 2. Upper Block — Shape 2
An **8-point notched rectangle** is sketched at `Z=108.5409` and extruded **−50 mm** downward to `Z=58.5409`. This is then **fused** with Shape 1 to form the unified plate solid.

#### 3. Circular Hole Cuts — Set 1
**8 circular through-holes** (r=17.5 mm) are cut from `Z=8.5409` downward 55 mm, arranged in a 4×2 grid pattern across the plate.

#### 4. Hollow Cylinders
Two **hollow annular cylinders** (wall thickness ~29 mm, height 73.5 mm) are built at the two primary bore centres:
- Cylinder 1 at local `(236.8, 259.6)` — r_outer=181.5131, r_inner=152.4775
- Cylinder 2 at local `(1605.9, 259.8)` — r_outer=181.5131, r_inner=152.3022

These are **fused** into the main body, then the inner bores are **cut** through 75 mm depth.

#### 5. D-Shaped Profile Cuts
Four large **D-shaped cutouts** (semicircular arc + rectangular tab) are cut into the top face region:
- 2 cuts from `Z=58.5409` downward −55 mm (upper D-cuts)
- 2 cuts from `Z=8.5409` upward +100 mm (lower D-cuts)

Each D-profile is a large closed polyline tracing the semicircular bore perimeter and a straight rectangular tab up to the notch edge.

#### 6. Side-Wall Slots
Two elongated **slot profiles** are cut through the left and right walls of the plate:
- Left slot: at `Z=43.5409`, depth +50 mm, flush with the left wall (X=0)
- Right slot: at `Z=43.5409`, depth +75 mm, flush with the right wall (X=1840.9)

Both slots include a rounded central lobe that follows the oval bore profile.

#### 7. Stepped Circular Holes — Set 2 & 3
A second set of **8 circular holes** in a 4×2 grid:
- Inner bore: r=17.5 mm from `Z=76.0409`, depth +75 mm
- Outer countersink: r=35.0 mm from `Z=58.5409`, depth −75 mm
- **Conical chamfer loft** connecting outer (r=35, Z=58.5409) to inner (r=17.5, Z=76.0409)

#### 8. Helical Threads
**6 helical thread solids** are generated using the OCC kernel (`BRepOffsetAPI_MakePipeShell`) and fused into the body:
- 3 starts per cylinder × 2 cylinders = 6 thread solids
- Helix: diameter=343 mm (r=171.5), pitch=120 mm, height=73.5 mm
- Profile: equilateral triangle, 31 mm side, apex pointing inward radially
- Angular offset between starts: 0°, 120°, 240°
- Circle cuts at both cylinder centres applied before fusing threads

#### 9. Swept Profile Cuts
Four **rotational swept cuts** around the cylinder axes using `BRepOffsetAPI_MakePipeShell` with circular spine paths (r=171.5 mm):
- Two **5-point trapezoidal profiles** (one per cylinder) — undercut groove at base
- Two **4-point rectangular profiles** (one per cylinder) — step ledge cut

#### 10. Text Embosses / Cuts
Five text features engraved at 5 mm depth into the top face (`Z=108.5409`):
- `"RIGHT"` — rotated 270°, centred on left panel zone
- `"LEFT"` — rotated 270°, shifted +782 mm in X from RIGHT
- `"R"` — mirrored (x_dir=−1), near the 6-point profile cut zone
- `"TOP"` — rotated 270°, centred on the full plate
- **6-point slot profile** — small rectangular notch cut −5 mm

---

### Part 2 — Disc / Cover Body (`Set_2`)

Built entirely in local centred coordinates (no origin offset). The body is constructed inside a single `BuildPart` context using sequential `Mode.SUBTRACT` extrudes.

#### 1. Base Rectangle
A simple **4-point closed rectangle** is extruded from `Z=0` to `Z=80`:
- X: −954.2 to +1006.7 mm (~1961 mm wide)
- Y: −502.5 to +567.5 mm (~1070 mm deep)

#### 2. Cut 1 — Top Contour Profile
A large **closed polyline profile** (~190 points) tracing the outer oval boundary of the disc is cut downward 10 mm from `Z=80`. This creates the sculpted top-face silhouette.

#### 3. Cuts 2 & 3 — Left and Right Outer Profiles
Two matching **curved boundary profiles** (the left and right halves of the disc perimeter) are cut upward +20 mm from `Z=50`. These open up the sides to follow the oval contour.

#### 4. Cut 4 — Central Oval Profile
A **double-lobe oval profile** (inner boundary of the disc, ~200 points) is cut upward +20 mm from `Z=50`, hollowing out the central region and leaving the disc rim.

#### 5. Cut 5 — Four Square Pockets
**4 rectangular pockets** (~52.5×52.5 mm each) are cut 70 mm deep from `Z=80` downward to `Z=10`. Positioned at the four outer corners of the disc.

#### 6. Cut 6 — 9 Through-Circular Holes
**9 circular holes** (polyline-approximated circles) cut **bidirectionally** ±80 mm from `Z=70` — i.e. full through-holes across the 80 mm body height. Positioned around the disc perimeter and centre.

#### 7. Cut 7 — 9 Bottom Circular Holes
**9 circular holes** (same pattern, slightly larger radius) cut upward +20 mm from `Z=0` — counterbore pockets on the bottom face.

#### 8. Cut 8 — 9 Lofted Chamfer Cuts
**9 conical chamfer solids** built outside the `BuildPart` context (pre-built strategy to avoid OCC kernel auto-fuse issues) and subtracted one by one:
- Outer ring profile at `Z=20`
- Inner ring profile at `Z=37.5`
- `loft(ruled=True)` generates the tapered cone between the two rings
- Applied with `part_2.part = part_2.part - solid`

---

## Positioning

The Plate Body is translated after construction (non-destructively, using `.moved()`):

```python
fused_positioned = fused.moved(Location((-894.2, 572, 0)))
```

| Axis | Offset |
|------|--------|
| X | −894.2 mm |
| Y | +572.0 mm |
| Z | 0 mm (unchanged) |

The Disc Body remains at its original local origin.

---

## Export

Both bodies are combined into a single `Compound` and exported automatically to the Desktop:

```python
assembly_compound = Compound([fused_positioned.solids()[0], part_2.part.solids()[0]])
export_step(assembly_compound, "~/Desktop/Set_2_Assembly.step")
export_stl(assembly_compound,  "~/Desktop/Set_2_Assembly.stl")
```

---

## Requirements

| Package | Purpose |
|---------|---------|
| `build123d` | Parametric CAD geometry kernel |
| `ocp-vscode` | OCP CAD Viewer integration for VS Code |
| `OCP` (opencascade) | Low-level BRep operations (helix, sweep, loft) |

**Python:** 3.11+ recommended (required for `ocp-vscode` 3.4.0+).  
**Interpreter:** Use the `ocp-fresh` venv or equivalent Homebrew Python 3.11 environment.  
**OCP Viewer port:** 3940

---

## Project Context

Part of the **PHIL** project developed for the  
**Cell Systems Dynamics Group, ETH Zurich**  
Original design by Philip Dettinger.  
Programmatic reconstruction by Softage (softage.ai).
