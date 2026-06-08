# Master Screw — Parametric CAD Model

A complex parametric screw/coupling component built entirely in **build123d** (Python CAD library). The model combines helical thread geometry, boolean operations, loft transitions, revolve features, and multi-profile extrude cuts into a single solid body.

---

## Requirements

```bash
pip install build123d ocp-vscode
```

Run in VS Code with the [OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer) extension installed.

```bash
python master_screw.py
```

---

## Methodology

The model is built programmatically in a strict sequence of geometric operations:

### 1. Thread Profile
The thread cross-section is a **5-vertex asymmetric pentagon** derived from a reference STEP file. The profile is sketched in the `XZ` plane, shifted to the helix radius, then rotated 90° around the X axis to align with the Frenet frame of the helix.

```
Crest (X=0) ──────── at helix radius 168mm
     │\
     │  \  upper flank
     │    \
Root (X=-24.548mm) ── root flat 28.12mm
     │    /
     │  /  lower flank (with knee at X=-8.555mm)
     │/
```

### 2. Triple-Start Helical Sweep
Three identical thread profiles are swept along three separate helices, each rotated **120° apart** around the Z axis. This creates a triple-start thread geometry for high lead-per-revolution advancement.

- Each helix: pitch=120mm, 5 revolutions, height=600mm
- Helix centreline: ⌀336mm
- Inner cut cylinder (⌀300mm) removes material inside the thread roots

### 3. Core Cylinder
A solid cylinder (⌀300mm × 343mm) forms the main body, starting at Z=0. The three thread helices are fused to it with boolean union.

### 4. Boolean Cuts — Faces
- **Top face** (Z=343): ⌀400mm × 600mm cylinder cut in +Z
- **Bottom face** (Z=0): ⌀400mm × 600mm cylinder cut in −Z

### 5. Chamfer Revolves
A triangular profile is revolved 360° around the Z axis to create a chamfer/undercut feature. The chamfer is cut at Z=+388.5mm and mirrored about Z=171.5mm for the opposing end.

### 6. Loft Transitions (3 bodies)
Three smooth loft bodies transition between circular cross-sections of decreasing size along the X axis. Each is built using `Edge.make_spline(periodic=True)` for smooth curves, then `Solid.make_loft()`. All three lofts are cut into the main body.

| Loft | X range | Profile change |
|------|---------|---------------|
| Loft 1 | −174.6 → −99.6 mm | Large → medium |
| Loft 2 | −99.6 → −83.0 mm | Medium → small |
| Loft 3 | −83.0 → −18.0 mm | Small → small (translate) |

### 7. Extrude Cuts
Multiple profile-based cuts are applied:

| Cut | Profile | Direction | Z range |
|-----|---------|-----------|---------|
| Hexagonal (cut_solid) | 6-point polygon | +Z | Z=258.5→343mm |
| Circular (cut2_solid) | ~⌀52mm circle | +Z | Z=0→350mm |
| YZ profile (cut3_solid) | 6-point polygon | +X (25mm) | Z≈+389mm |
| Circular (cut4_solid) | ~⌀52mm circle | +Z | Z=0→20mm |
| Large circle (cut5_solid) | ~⌀170mm circle | +Z | Z=343→388.5mm |
| Hexagonal (cut6_solid) | 6-point polygon | +Z | Z=343→393mm |
| Blade 1 | Top fin (~120°) | +Z | Z=0→350mm |
| Blade 2 | Right fin (~0°) | +Z | Z=0→350mm |
| Blade 3 | Bottom fin (~240°) | +Z | Z=0→350mm |

### 8. Fillet
An **11mm fillet** is applied to the 6 hexagonal edges at Z=388.5mm on the `cut5_solid` body before it is fused into the main body.

---

## Overall Dimensions

| Dimension | Value |
|-----------|-------|
| Overall X span | ~383mm (−183mm to +200mm) |
| Overall Y span | ~366mm (−183mm to +183mm) |
| Overall Z span | ~1143mm (−600mm to +543mm) |
| Core cylinder diameter | ⌀300mm |
| Core cylinder height | 343mm |
| Thread crest diameter | ⌀334.375mm |
| Thread root diameter | ⌀285.278mm |
| Thread pitch | 120mm |
| Thread starts | 3 |

---

## Thread Profile Dimensions

| Parameter | Value |
|-----------|-------|
| Crest flat (axial) | 6.954mm |
| Root flat (axial) | 28.123mm |
| Tooth depth (radial) | 24.548mm |
| Helix radius | 168mm |
| Profile vertices | 5 (asymmetric pentagon) |
| Lower flank knee radius | 158.633mm |

---

## File Structure

```
master_screw.py      # Main build script
master_screw.step    # Exported STEP file
README.md            # This file
```

---

## Key build123d APIs Used

- `Helix` — helical path generation
- `sweep(..., is_frenet=True)` — profile sweep along helix
- `Solid.make_loft()` — smooth loft between wire profiles
- `Edge.make_spline(periodic=True)` — smooth closed spline curves
- `Solid.extrude()` — directional extrude with explicit vector
- `revolve()` — 360° revolve of 2D profile
- `mirror()` — mirror about a defined plane
- `fillet()` — edge filleting
- `export_step()` — STEP file export
