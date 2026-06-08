# Power Box – CAD Model

A parametric 3D CAD model of a power distribution box designed in [build123d](https://github.com/CadQuery/build123d), an open-source Python-based CAD library. This model features multiple components including perforated plates, hex pockets, cylindrical features, and lofted surfaces.

---

## Overview

The Power Box is a complex assembly consisting of:
- **5 fused structural plates** (left, back, right, front, bottom)
- **4 hexagonal pockets** for component mounting
- **2 rectangular slots** for cable routing
- **Multiple cylindrical features** (solid, hollow, and through-holes)
- **Lofted transitions** for smooth aerodynamic surfaces
- **Embossed text** identifying design credits

**Design Team:** Cell Systems Dynamics Group, ETH Zurich  
**Designer:** Phillip Dettinger

---

## Overall Dimensions

| Dimension | Value | Unit |
|-----------|-------|------|
| **Length (X)** | 1240 | mm |
| **Width (Y)** | 1192.5 | mm |
| **Height (Z)** | 1876.76 | mm |
| **Left Plate Thickness** | 47.5 | mm |
| **Back Plate Thickness** | 47.5 | mm |
| **Right Plate Thickness** | 45.0 | mm |
| **Front Plate Thickness** | 47.5 | mm |
| **Bottom Plate Thickness** | 47.5 | mm |

### Key Features

#### Hexagonal Pockets (4x)
- **Depth:** 27.5 mm
- **Location:** Z = 47.5 mm from bottom
- **Arrangement:** Distributed across upper surface
- **Purpose:** Component mounting points

#### Rectangular Slots (2x)
- **Dimensions:** 30 × 56.99 × 1204.3 mm (W × D × L)
- **Locations:** Left and right sides (X = 25 mm and 1185 mm)
- **Purpose:** Cable routing and management

#### Cylindrical Features
- **Large cylinder (XY plane):** Ø ~70 mm, depth 200 mm
- **Side cylinders (2x):** Ø ~60 mm, extruded 60 mm
- **Through-hole (center):** Ø ~30 mm, 50 mm depth (±Z)
- **Hollow cylinders (4x):** Various radii and extrusion lengths

#### Lofted Surfaces (6x)
- Smooth transitions from outer plate edges to inner cores
- Creates aesthetic aerodynamic form
- Mirrored left/right for symmetry
- Multiple Z-height ranges (1876.76–0 mm)

#### Embossed Text
- **Content:** 3 lines (designer, group, institution)
- **Font Size:** 100 mm
- **Depth:** 3 mm
- **Orientation:** 90° CW rotation, runs in -Z direction
- **Location:** Back face (Y = 3 mm offset)

---

## Methodology

### Architecture

The CAD model is built using a **modular, parametric approach**:

1. **Plate Generation** – Five plates built from JSON profile definitions and extruded in specific directions
2. **Fusing** – All plates combined into a single solid body using Boolean operations
3. **Subtractive Features** – Pockets, slots, and holes cut sequentially using Boolean subtraction
4. **Additive Features** – Lofted surfaces fused into the main body using Boolean union
5. **Surface Finishing** – Text embossing and chamfering for refined edges
6. **Export** – Final model cleaned and exported to STEP format

### Parametric Design

All critical dimensions are defined as **constants** at the top of the script for easy modification:

```python
EXTRUDE_DEPTH     = 47.5   # mm – default plate thickness
RIGHT_PLATE_DEPTH = 45.0   # mm – right plate exception
CUT_EXTRUDE_DEPTH = 27.5   # mm – hex pocket depth
```

Plate profiles are loaded from **JSON files**, allowing non-destructive design iteration.

### Design Principles

- **Modularity:** Each major feature (plates, cuts, lofts) is independently defined
- **Symmetry:** Left/right features are mirrored to maintain balance
- **Boolean Operations:** Complex shapes created through union and subtraction
- **Parametric Profiles:** 2D outlines stored externally (JSON) for easy modification
- **Tolerance Management:** 1e-3 mm tolerance for Boolean operations

### File Organization

```
├── power_box.py                 # Main CAD script
├── Left Plate.json              # Profile definition (XY plane)
├── Back Plate.json              # Profile definition (YZ plane)
├── Right Plate.json             # Profile definition (YZ plane)
├── Front Plate.json             # Profile definition (YZ plane)
├── Bottom Plate.json            # Profile definition (XY plane)
└── README.md                    # This file
```

---

## Installation & Setup

### Prerequisites

- **Python 3.9+**
- **build123d** library
- **OCP (Open Cascade) wrapper**

### Installation

```bash
# Install build123d
pip install build123d

# Install OCP (if not included)
pip install ocp-core

# Optional: VS Code plugin for visualization
pip install ocp-vscode
```

### Running the Script

```bash
python power_box.py
```

**Output:**
- Displays 3D model in OCP VSCode viewer
- Exports STEP file to Desktop: `~/Desktop/Power Box.step`

---

## Features in Detail

### Hexagonal Pockets

Four hexagonal mounting pockets distributed across the upper surface at Z = 47.5 mm:

```python
all_points = [
    # Hex 1 (top-right)
    (352.6953, 986.4844, 47.5),
    (335.3711, 1016.4844, 47.5),
    # ... 4 more vertices per hexagon
    
    # Hex 2 (bottom-right)
    # Hex 3 (left)
    # Hex 4 (right)
]
```

Each hexagon is cut 27.5 mm deep into the solid.

### Rectangular Cable Slots

Two slots for cable management at opposite sides:

```python
rect_tool_1 = Solid.make_box(30, 56.9922, 1204.3,
   Plane(origin=Vector(25.0, 623.9844, 677.4599)))
rect_tool_2 = Solid.make_box(30, 56.9922, 1204.3,
   Plane(origin=Vector(1185.0, 623.9844, 677.4599)))
```

**Dimensions:** 30 mm wide × 56.99 mm deep × 1204.3 mm tall

### Lofted Surfaces

Six smooth transition surfaces (3 per side) create the aerodynamic profile:

- **Loft 1:** Upper region (Z = 1876.76–1676.76 mm)
- **Loft 2:** Middle region (Z = 983.52–583.52 mm)
- **Loft 3:** Lower region (Z = 300–0 mm)

Each loft transitions from outer plate edge (large diameter) to inner core (small diameter) across a 100 mm offset in Y direction.

### Cylindrical Features

#### Solid Cylinder (Center Front)
- **Center:** (620, 1290) mm
- **Radius:** ~35 mm
- **Depth:** 200 mm (in -Z direction)

#### Top Through-Hole
- **Center:** (620, 1290) mm
- **Radius:** ~15 mm
- **Depth:** 50 mm (±Z from Z = 677.5 mm)

#### Side Cylinders (2x)
- **Radius:** ~30 mm
- **Centers:** (150, -50) and (1090, -50) mm
- **Extrusion:** 60 mm in +Z direction

#### Hollow Cylinders (4x)
- Complex annular geometry for mounting and structural support
- Distributed across left/right plates
- Mirrored for symmetry

### Chamfered Edges

Four chamfered loft bodies smooth the transitions at key edges:

1. **Front center chamfer:** Outer Ø ~70 mm → Inner Ø ~30 mm, 30 mm height
2. **YZ right chamfer:** Outer Ø ~75 mm → Inner Ø ~60 mm
3. **YZ left chamfer:** Mirror of #2
4. **Back face chamfers (2x):** Two separate lofts (x ≈ 365 and 865 mm)

---

## Boolean Operations Summary

### Fuses (Union)
1. All 5 plates merged into `power_box`
2. 6 lofted bodies fused in
3. 1 front loft body fused in
4. 2 hollow cylinders fused in
5. 1 hollow cylinder (#2) fused in

### Cuts (Subtraction)
1. 4 hexagonal pockets (compound cut)
2. 2 rectangular slots (compound cut)
3. 1 large center cylinder
4. 2 side cylinders (compound cut)
5. 1 through-hole (union of ±Z extrusions)
6. 1 chamfer loft (center)
7. 1 YZ right chamfer loft
8. 1 YZ left chamfer loft
9. 2 back face chamfers
10. Embossed text (3 lines)

---

## Export & Formats

### STEP Format
The model is exported to **STEP** (.step) format:
- **Location:** `~/Desktop/Power Box.step`
- **Compatibility:** Importable in Fusion 360, FreeCAD, SolidWorks, etc.
- **Benefits:** Preserves full geometry for manufacturing and further refinement

### Visualization
Built-in OCP VSCode plugin displays the model in real-time with:
- **Color:** #5b8fa8 (Steel blue)
- **Opacity:** Fully opaque (alpha = 1.0)

---

## Customization

### Modifying Plate Thickness

Edit constants at the top of the script:

```python
EXTRUDE_DEPTH     = 47.5   # Change for all plates (except exceptions)
RIGHT_PLATE_DEPTH = 45.0   # Change for right plate only
```

### Modifying Pocket Depth

```python
CUT_EXTRUDE_DEPTH = 27.5   # Hex pocket depth
```

### Modifying Dimensions

Geometry is defined through:
1. **JSON plate profiles** – Edit external JSON files
2. **Point arrays** – Modify coordinate lists for cylindrical/lofted features
3. **Plane origins** – Adjust coordinate vectors for positioning

---

## Performance Notes

- **Build time:** ~30–60 seconds (depending on system)
- **Triangle count:** ~50,000–100,000 (for visualization)
- **File size (STEP):** ~2–5 MB
- **Memory usage:** ~500 MB–1 GB

---

## License

This CAD model is provided as-is for educational and research purposes by the **Cell Systems Dynamics Group, ETH Zurich**.

For commercial use or modifications, please contact the design team.

---

## Authors

- **Designer:** Phillip Dettinger
- **Institution:** Cell Systems Dynamics Group, ETH Zurich
- **CAD Framework:** build123d (Python-based parametric CAD)

---

## References

- [build123d Documentation](https://build123d.readthedocs.io/)
- [OCP (Open Cascade) Bindings](https://github.com/CadQuery/ocp)
- [CadQuery](https://cadquery.readthedocs.io/)

---

## Support & Issues

For questions or issues:
1. Check the methodology section above
2. Review the inline comments in `power_box.py`
3. Consult build123d documentation
4. Contact the design team
