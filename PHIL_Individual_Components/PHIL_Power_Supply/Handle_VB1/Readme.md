# master_script.py — README

## Overview

This script builds a 3-body CAD assembly using **build123d** (Python CAD library) and
displays it in **OCP CAD Viewer**. On completion it exports all bodies to a single STEP
file via a native macOS save dialog.

---

## Bodies

| Body | Colour | Description |
|------|--------|-------------|
| `Handle` | Blue | U-shaped swept bar with two through-holes |
| `Base` | Green | Flat base plate with handle pocket cut |
| `Extrude_body` | Yellow | Small extruded profile at end of base |

---

## Overall Dimensions (mm)

### Handle (Blue)
| Axis | Min | Max | Span |
|------|-----|-----|------|
| X | -112.82 | 504.65 | **617.47** |
| Y | -1250.00 | 50.00 | **1300.00** |
| Z | -67.50 | 67.50 | **135.00** |
| Volume | | | **21.07 cm³** |

### Base (Green)
| Axis | Min | Max | Span |
|------|-----|-----|------|
| X | -27.15 | 500.47 | **527.62** |
| Y | -1250.00 | 50.00 | **1300.00** |
| Z | -67.50 | -42.50 | **25.00** |
| Volume | | | **3.88 cm³** |

### Extrude Body (Yellow)
| Axis | Min | Max | Span |
|------|-----|-----|------|
| X | -112.85 | -63.86 | **48.98** |
| Y | -1250.00 | -1150.00 | **100.00** |
| Z | -67.50 | -42.50 | **25.00** |
| Volume | | | **0.07 cm³** |

---

## Methodology

### 1. Handle — Swept Rectangle with Fillets and Drilled Holes

**Profile:** 100×100 mm rectangle placed at the path start, normal aligned to +X.

**Path:** Open polyline through 4 points forming a U-shape:
- Start: `(0, 0, 0)`
- Corner 1: `(454.65, 0, 0)` — +X leg
- Corner 2: `(454.65, -1200, 0)` — -Y leg (1200 mm)
- End: `(0, -1200, 0)` — -X return leg (454.65 mm)

**Sweep:** `is_frenet=True`, `Transition.RIGHT` for sharp corners.

**Fillets applied in order:**
1. `50 mm` on the two inner concave Z edges at `x=404.65` (inner bend corners, -Y facing)
2. `30 mm` on all X-axis edges and Arc edges (top/bottom horizontal edges and existing arcs)
3. `49.9 mm` on the two 1240 mm Y-axis outer edges (geometric maximum; r=50 equals half profile width)

**Cylinders:** Two cylinders, diameter `135 mm`, length `100 mm`, extruded along Y:
- Start cylinder: centred at `X=-45.32, Z=0`, `Y=-50..50`
- End cylinder: mirrored about `Y=-600` plane → `Y=-1250..-1150`
- Both fused into the handle body.

**Through-holes:** `29.95 mm` diameter drilled through both cylinder centres along Y axis. Second hole mirrored from first using the same `Y=-600` mirror plane.

**Final handle** = sweep + 2 cylinders fused, then 2 holes cut.

---

### 2. Base — Extruded Profile with Handle Pocket

**Profile:** 38-point closed polygon loaded from `extrude.txt`, lying at `z=-134.9943`
(face normal = -Z). Points reordered to form a valid closed boundary.

**Extrude:** 25 mm in `+Z` direction.

**Translation:** `(-46.209, 0, +67.494)` to align with the assembly.

**Handle pocket cut:** A copy of the handle body shifted `-2.45 mm` in Z is used as a
boolean cut tool, creating a pocket in the base that matches the handle cross-section.

---

### 3. Extrude Body — Small End Profile

**Profile:** 11-point closed polygon from `extrude.txt` (second file), lying at `y=-1250`
(face normal = -Y). Points reordered: first 3 define the outer boundary, remaining points
(reversed) define the curved inner edge.

**Extrude:** 100 mm in `+Y` direction.

**Translation:** `(-46.206, 0, +67.494)` to align with the assembly.

---

## Export

All three bodies are exported as a single STEP assembly file. A native macOS save dialog
(`osascript`) appears before the viewer opens, asking for the save location. On Linux,
`zenity` is used as a fallback.

```
export_step(Compound([handle, base_cut, extrude_solid2]), path)
```

---

## Dependencies

```
pip install build123d ocp-vscode
```

- **build123d** — parametric CAD kernel (OpenCASCADE wrapper)
- **ocp-vscode** — OCP CAD Viewer integration for display
- **Python 3.10+**

---

## File Structure

```
master_script.py   — main script
extrude.txt        — base profile points (38 pts) and end profile points (11 pts)
README.md          — this file
```
