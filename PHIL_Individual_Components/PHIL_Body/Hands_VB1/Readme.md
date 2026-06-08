# Hand Assembly — build123d

A parametric 3D assembly of three surveyed structural components modelled in Python using [build123d](https://github.com/gumyr/build123d). All geometry is derived from real-world survey point clouds; no dimensions were manually entered. The script produces a single STEP file suitable for downstream CAD, FEA, or manufacturing workflows.

---

## Repository structure

```
Hand_Assembly.py   ← single-file assembly script (this repo)
Hand1.py           ← end fitting (standalone model)
Hand2.py           ← bracket body (standalone model)
Hand3.py           ← long slot bar (standalone model)
README.md          ← this file
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `build123d` | Parametric solid modelling kernel (OCC wrapper) |
| `ocp_vscode` | Interactive 3D viewer inside VS Code |
| `tkinter` | Native file-save dialog for STEP export |

Install with:

```bash
pip install build123d
pip install ocp-vscode
```

---

## Components

### Hand 1 — End Fitting

The end fitting that terminates one end of the slot bar. It is the most geometrically complex part, combining boolean fuses and subtractions to produce a slotted body with a raised annular collar, chamfered transitions, hexagonal bolt pockets, and circular through-holes.

**Key features:**
- Slot base profile (57 pts) extruded full height
- C-shaped cut profile (79 pts) fused on top, forming the open collar
- Annular ring (outer 42 pts / inner 38 pts) subtracted to leave a hollow sleeve
- Two chamfer lofts (outer → inner taper) cut at top and bottom of collar
- Two hollow disk cuts at Z = 45–55 mm (one each side of centre-line)
- Two hexagonal bolt pockets (57.5 mm across flats), 30 mm deep
- Two circular through-holes ⌀27 mm, from Z = 31.5 → 50 mm
- Engraved text: **BOTTOM** on bottom face, **TOP LEFT** on top face

**Overall dimensions:**

| Dimension | Value |
|---|---|
| Slot length (X) | 1554.9 mm |
| Slot width (Y) | 100.0 mm |
| Height (Z) | 50.0 mm |
| Collar outer diameter | ≈ 96 × 88 mm |
| Collar Z range | 10 – 40 mm |
| Hex pocket width | 57.5 mm across flats |
| Through-hole diameter | ≈ 27 mm |

---

### Hand 2 — Bracket Body

A compact bracket with a rounded rectangular outer profile, cut away on the inside by three distinct profiles — a straight polyline pocket, an arc-bounded pocket (RadiusArc, r = 35.5 mm), and a channel cut — with a chamfer loft blending the outer edge down to the inner wall.

**Key features:**
- 55-point closed outer profile extruded 40 mm
- Straight polyline pocket (47 segs, Z = 7.5 → 40 mm) subtracted
- Arc pocket (38 segs including one RadiusArc, Z = 7.5 → 40 mm) subtracted
- Channel cut (87-seg closed profile, Z = 7.5 → 40 mm) subtracted
- Chamfer loft (outer 45 pts → inner 40 pts, both resampled to 50 pts) fused at base

**Overall dimensions:**

| Dimension | Value |
|---|---|
| Outer width (X) | 177.1 mm |
| Outer depth (Y) | 181.8 mm |
| Height (Z) | 40.0 mm |
| Chamfer loft height | 7.5 mm (Z = 7.5 → 15 mm) |

---

### Hand 3 — Long Slot Bar

A long slotted bar with semicircular ends, a row of ten circular through-holes on one face, chamfered pockets at each end, and two large cylindrical bores sunk from the top face. This is the longest part in the assembly and establishes the primary axis.

**Key features:**
- Closed slot profile (56 pts: two 28-pt semicircles + straight walls) extruded 50 mm
- 10 × circular through-holes (⌀15 mm, 50 mm pitch) cut through the full width in Y
- 10 × matching circular through-holes on the opposite side (+X row, 50 mm pitch)
- Chamfer loft at left end (outer 44 pts → inner 35 pts, Z = 0 → 13.5 mm)
- Chamfer loft at right end (outer 44 pts → inner 35 pts, Z = 0 → 13.5 mm)
- Left bore ⌀ ≈ 83 mm, sunk 35 mm from top face (Z = 50 → 15 mm)
- Right bore ⌀ ≈ 83 mm, sunk 35 mm from top face (Z = 50 → 15 mm)
- Engraved text: **BOTTOM** on top face, **TOP RIGHT** on bottom face

**Overall dimensions:**

| Dimension | Value |
|---|---|
| Total length (X) | 1549.8 mm |
| Width (Y) | 100.0 mm |
| Height (Z) | 50.0 mm |
| Semicircle radius | 50.0 mm |
| Hole diameter | 15.0 mm |
| Hole pitch | 50.0 mm |
| Number of holes (each row) | 10 |
| End bore diameter | ≈ 83 mm |
| End bore depth | 35 mm |

---

## Assembly

### Coordinate system

All three parts were surveyed in a projected coordinate system with large absolute values (easting ≈ 540 000 – 541 500, northing ≈ 234 050 – 234 280). To avoid floating-point precision issues in the CAD kernel, each part is normalised to its own local origin before geometry is built, then translated back to its correct relative position.

**Assembly origin** = Hand 1 slot centroid:

```
ASM_OX = 540716.7578
ASM_OY = 234098.9648
```

**Part offsets relative to assembly origin:**

| Part | World centroid (easting, northing) | Offset (dx, dy) mm |
|---|---|---|
| Hand 1 | (540716.76, 234099.0) | (0, 0) — origin |
| Hand 2 | (541430.94, 234188.6) | (+714.2, +89.7) |
| Hand 3 | (540559.94, 234155.5) | (−156.8, +56.5) |

**Assembly bounding box (in local assembly coordinates):**

| Axis | Range | Total span |
|---|---|---|
| X | −931.7 → +802.7 mm | **1734.5 mm** |
| Y | −50.0 → +180.6 mm | **≈ 231 mm** |
| Z | 0 → 55 mm | **55 mm** |

---

## Methodology

### 1. Survey data ingestion

All profile shapes were captured as point clouds in a projected survey coordinate system (likely a national grid). Raw points are stored as Python tuples directly in the script — no external files are required. This makes the script fully self-contained and version-control friendly.

### 2. Normalisation

Each part normalises its survey points to a local origin at the bounding-box centroid of its primary (largest) profile:

```python
ox = (min(xs) + max(xs)) / 2
oy = (min(ys) + max(ys)) / 2
pts_local = [(x - ox, y - oy) for x, y in raw_pts]
```

This eliminates large-number cancellation errors in the OCC kernel and keeps sketches centred near the world origin during construction.

### 3. Profile construction

Profiles are built with `BuildLine` → `Polyline` (straight segments) or a mix of `Line` and `RadiusArc` calls where the source data contains circular arcs. All profiles are closed with `close=True` or by explicit closure segments, then converted to faces with `make_face()`.

Annular (ring) profiles and hollow disks are constructed by building the outer solid first, then subtracting the inner profile in a second `extrude(..., mode=Mode.SUBTRACT)` pass — this avoids the need to build compound wire sketches.

### 4. Chamfer lofts

Tapered chamfered edges are produced with `loft(ruled=True)` between two sketches at different Z heights. Where the outer and inner profiles have different point counts they are:
1. Angle-sorted from their centroid using `atan2` to establish consistent winding
2. Resampled to a common count (50 points) by arc-length interpolation

This ensures the loft kernel can match corresponding vertices cleanly.

### 5. Point-order corrections

Several source profiles contained swapped adjacent vertices, causing self-intersecting wires that would fail `make_face()`. These are corrected in-place with comments marking the swap locations (e.g. indices 59↔60 in the Hand 1 cut profile, 19↔20 and 50↔51 in the Hand 2 outer profile).

### 6. Assembly positioning

After each part is fully constructed in its local coordinate space, a single `Location` translation moves it to its correct world position:

```python
def _offset(solid, world_ox, world_oy):
    dx = world_ox - ASM_OX
    dy = world_oy - ASM_OY
    return solid.moved(Location((dx, dy, 0)))
```

Z is not adjusted — all three parts share Z = 0 as their base plane.

### 7. Text engraving

Text is extruded as a solid and then subtracted from the body face. Text on the bottom face (Z = 0) is mirrored about the XZ plane after extrusion so it reads correctly when viewed from below. Text on the top face uses a negative extrude direction.

### 8. Export

The three positioned solids are wrapped in a `Compound` and exported as a single STEP file via `export_step()`. A `tkinter` file-save dialog is presented at runtime so the user can choose the output location.

---

## Usage

```bash
# Run interactively (requires ocp_vscode viewer running in VS Code)
python Hand_Assembly.py
```

A file-save dialog will appear at the end. Choose a `.step` destination to export the full assembly.

To run each part in isolation:

```bash
python Hand1.py   # end fitting only
python Hand2.py   # bracket only
python Hand3.py   # long slot bar only
```

---

## Notes

- The survey coordinate values are in **millimetres** (consistent with a local engineering survey at 1:1 scale).
- All Z heights are measured from the underside (bottom face) of each part.
- The `ocp_vscode` `show()` call at the end of the script is optional — remove it if running headlessly or in a CI environment.
- Profile point counts and ordering are documented inline throughout the script.
