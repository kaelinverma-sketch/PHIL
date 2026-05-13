# Body — Parametric CAD Model

**Designed by Philip Dettinger · Cell System Dynamics Group · ETH Zurich**

This script generates a complex multi-cavity structural body using [build123d](https://github.com/gumyr/build123d), a Python-based constructive solid geometry (CSG) library. The final geometry is exported as a STEP file via an interactive save dialog.

---

## Overview

The model is a large rectangular enclosure with two large cylindrical disc bores, a rear mounting block, arc-ring cutouts, profiled slot features, labelled text embosses, and a family of through-holes. It is built entirely through sequential boolean operations (extrusion, subtraction, revolve, sweep) accumulated across ~21 intermediate `BuildPart` stages.

---

## Overall Dimensions

| Dimension | Value |
|---|---|
| Length (X) | 1960.94 mm |
| Width (Y) | 790.00 mm |
| Height (Z) | 1070.00 mm |

---

## Methodology

The model is constructed by chaining named `BuildPart` bodies, each adding or subtracting geometry from the previous stage. The pipeline proceeds as follows:

### 1. Main Box (`box_part`)
A solid rectangular block of **1960.94 × 790 × 1070 mm** is created as the base. Four rectangular slot pockets (40 × 100 mm, depth 55 mm) are subtracted from the top face at evenly spaced X positions. A large internal cavity (1860.94 × 322.5 mm, depth 1020 mm) is subtracted from the bottom, inset 50 mm on all sides, leaving a thick perimeter wall.

### 2. Plate Cut (`box_with_plate_cut`)
A rear plate relief is subtracted from the top face — a 1960.94 × 640 mm rectangle cut 372.5 mm deep in the Y direction from the rear, starting at Z = 1070.

### 3. Disc Cuts (`after_disc_cuts`)
Two large cylindrical bores (Ø 1430.91 mm) are subtracted from the rear face at centres X = 754.91 and X = 1205.92, Z = 749.96 (depth 376.5 mm). Annular ring cuts (outer Ø 470 mm, inner Ø 260 mm) are then subtracted concentrically, followed by a second full-disc cut at the same centres, creating a stepped pocket profile around each bore.

### 4. Top Rectangle Cut (`after_rect_cut`)
A centred rectangular pocket (1500 × 400 mm, depth 400 mm) is subtracted from the top face (Z = 1070).

### 5. Arc-Ring Bodies (`arc_ring_c1`, `arc_ring_c2`)
Two 10 mm-thick arc-ring solids are constructed geometrically using `ThreePointArc` and `make_face` on the ring plane. Each spans **187°** around its respective disc centre (anti-clockwise and clockwise respectively), with outer radius 666.82 mm and inner radius 636.93 mm. These are subtracted from the main body during final assembly.

### 6. Back Box (`back_box`)
A separate rear protrusion block (350.94 × 377.5 × 750 mm) is built at the back face (Y = 790). Two cylindrical through-holes (Ø 321.63 mm) are subtracted at the disc centres, and two smaller pilot holes (Ø 151.31 mm) are drilled from the rear face inward.

### 7. Axial Holes — Main Body (`final_body2` → `final_body4`)
Multiple sets of through-holes are drilled through the body in the Y-direction:
- 2 × Ø 151.31 mm at disc centres, depth 367.5 mm (from rear)
- 2 × Ø 240 mm and 2 × Ø 173.85 mm, fully through in Y
- 4 × Ø 35 mm (side bolting holes at X = 50 and X = 1910.94, two heights each)

### 8. Profile Slot Cuts (`final_body5` → `final_body9`)
A custom 6-point trapezoidal profile (50 × 66.4 mm with chamfered corner) is used as a swept cross-section for guide-rail or key-slot cuts on multiple faces and orientations. Cuts are applied symmetrically on left/right/front/rear faces using mirrored profile point sets and mirrored sketch planes.

### 9. Back-Face Holes & Box Cut (`final_body6`, `final_body8`)
Three Ø 35 mm holes are drilled 127.5 mm deep from the rear face at specific XZ coordinates. A 146.99 × 100 × 377.5 mm rectangular slot is also subtracted from the rear face.

### 10. Bottom Bore & Chamfers (`final_body10` → `final_body13`)
A central bottom bore at (X=980.64, Y=595) is created in two stages:
- Ø 157.02 mm, depth 700 mm
- Ø 244.07 mm, depth 150 mm (counterbore entry)

Two revolved chamfer profiles are then subtracted to create a smooth lead-in: a 37 mm entry chamfer and an 85 mm transitional taper from Ø 244.07 mm down to Ø 157.02 mm.

### 11. Central Cylinder Assembly (`cyl_body`, `arc_cyl_body`, `joined_cyl`)
A Ø 47 mm × 98.5 mm cylinder is built at the bore centre, with a 45° slant cut applied at Z = 75 mm. A swept arc cylinder (same Ø 47 mm, swept along a 150°-total arc of radius 122 mm at Z = 75 mm) is constructed and joined to the straight cylinder. The combined body is given a 20 mm fillet on the sweep end-cap edge.

### 12. Rotational Replication (`final_body14`)
The joined cylinder assembly is translated (+50.07 mm X, −101 mm Y) and rotated 30° about the bore centre (X=980.64, Y=595). Two replicas are then placed at 120° and 240° around the same centre, and all three are subtracted from the body — creating a three-lobe pattern of cylinder cuts.

### 13. Profile Cuts on Top/Mid Levels (`final_body15`, `final_body16`)
The trapezoidal profile is applied again at top-level (Z=1053.2) and mid-level (Z=513.2), at two Y offsets each, on both left and right faces — giving eight total profile slot cuts. Four mirrored profile extrusions are also subtracted from the top face at Z=1020 (two per side, offset in Y).

### 14. Top Face Detail Holes (`final_body17`)
Four Ø 35 mm holes (depth 24 mm) are drilled from the top face (Z=1070) at corner positions near X=50 and X=1910.94, at Y=535 and Y=640.

### 15. Top Box Cuts (`final_body18`)
Two 38 × 367.5 × 40 mm rectangular pockets are subtracted symmetrically near the left and right ends of the top face (Z=1032), inset 100 mm from each end.

### 16. Front Face Holes (`final_body19`)
Four Ø 100 mm holes (depth 55 mm) are drilled through the front face (Y=0) at Z=425, spaced along X.

### 17. Text Embossing (`final_body20`, `final_body21`)
Three lines of spaced text are engraved 6 mm deep into the front face:
- `D e s i g n e d   b y   P h i l i p   D e t t i n g e r`
- `C e l l   S y s t e m   D y n a m i c s   G r o u p`
- `E T H   Z u r i c h`

"RIGHT" and "LEFT" orientation labels (font size 69.3) are engraved 3 mm deep into the rear face, running vertically along Z.

### 18. Final Assembly & Export (`final_body21`)
All component bodies are merged (disc cuts applied, back box added, arc rings subtracted). The final geometry is displayed in OCP VSCode viewer and exported to a user-selected STEP file via a Tkinter save dialog.

---

## Dependencies

| Package | Purpose |
|---|---|
| `build123d` | Parametric CSG modelling |
| `ocp_vscode` | In-editor 3D preview (OCP CAD Viewer) |
| `tkinter` | Native file save dialog for STEP export |
| `math` | Arc point calculations |

Install build123d:
```bash
pip install build123d
```

OCP VSCode viewer setup: https://github.com/bernhard-42/vscode-ocp-cad-viewer

---

## Usage

```bash
python Body__.py
```
