# Build123d Structural Profile Model

A parametric CAD model built with [build123d](https://github.com/gumyr/build123d), a Python-based CAD library using OpenCASCADE. The script generates a structural profile with a through-hole, a pocket cut, two longitudinal slots, and a series of fillets — and exports the result as a STEP file via a GUI save dialog.

---

## Requirements

- Python 3.10+
- [build123d](https://github.com/gumyr/build123d) — `pip install build123d`
- [ocp-vscode](https://github.com/bernhard-42/vscode-ocp-cad-viewer) — `pip install ocp-vscode`
- OCP CAD Viewer extension for VS Code (for live 3D preview)
- `tkinter` (included with most Python installations)

---

## Usage

```bash
python rectangle_extrude.py
```

On each run the model is built and displayed in the OCP CAD Viewer, then a **Save As** dialog prompts you to choose the STEP export location and filename.

---

## Overall Dimensions

| Parameter | Value |
|---|---|
| Length (Y) | 1050 mm |
| Width (X) | 150 mm |
| Height (Z) | 100 mm |
| Origin | Corner of model at (0, 0, 0) |

---

## Features

### Main body
A rectangular profile extruded along the Y axis.

- Cross-section: 150 mm (X) × 100 mm (Z)
- Length: 1050 mm along +Y

### Through-hole
A circular hole running the full length of the body.

- Diameter: 32 mm
- Centre position: X = 73.93 mm, Z = 50 mm
- Cut depth: 1060 mm in +Y (through entire body)

### Pocket cut
A rectangular step cut into the top face of the body.

- Width: 150 mm (X) × 80 mm (Z)
- Depth: 20 mm in +Y
- Position: Y = 842.5 mm to Y = 862.5 mm, Z = 20 mm to Z = 100 mm

### Slot cut 1
A longitudinal slot running from the start of the body.

- Cross-section: 12.5 mm (X) × 45 mm (Z)
- Length: 822.5 mm in +Y
- Position: X = 67.68 mm, Z = 62.67 mm, Y = 0 to Y = 822.5 mm

### Slot cut 2
A second longitudinal slot running to the end of the body, separated from slot 1 by a 55 mm land.

- Cross-section: 12.5 mm (X) × 45 mm (Z)
- Length: 172.5 mm in +Y
- Position: X = 67.68 mm, Z = 62.67 mm, Y = 877.5 mm to Y = 1050 mm

---

## Methodology

The script follows a standard subtractive solid modelling workflow using build123d's `BuildPart` context manager.

**1. Base extrusion** — A rectangle is sketched on the `XZ` plane and extruded 1050 mm in the +Y direction using `Plane.XZ` (whose normal points in −Y, so `extrude(amount=-1050)` moves in +Y). The rectangle is aligned with `Align.MIN` on both axes to place the corner at the world origin.

**2. Subtractive operations** — Each feature (hole, pocket, slots) is added as a `Mode.SUBTRACT` extrusion, sketched on a custom `Plane` positioned at the relevant Y offset with the appropriate normal direction.

**3. Fillet ordering** — Fillets are applied in a deliberate sequence because each fillet modifies the topology, changing which edges exist and how much curvature adjacent edges can accept. Larger fillets are applied first (50 mm corner and top-long edges), followed by smaller feature fillets. Where a requested radius exceeded the geometric maximum, the largest safe value is used and documented in comments.

**4. Export** — After the model is complete, `export_step()` writes a STEP AP203 file. The save path is chosen at runtime via `tkinter.filedialog.asksaveasfilename`.

---

## Fillet Summary

| # | Edge | Radius | Notes |
|---|---|---|---|
| 1 | `edge_front_top_long`, `edge_back_top_long` | 50 mm | Top longitudinal edges at x=0 and x=150 |
| 2 | Four vertical corner edges | 50 mm | Z-direction edges at all four body corners |
| 3 | `slot1_end_top_x`, `slot2_start_top_x` | 10 mm | Slot end cap top edges at y=822.5 and y=877.5 |
| 4 | `slot1_upper_left` | 10 mm | Slot 1 upper left long edge |
| 5 | `slot1_upper_right` | 6 mm | Slot 1 upper right long edge (max safe) |
| 6 | `pocket_exit_top_x` | 4 mm | Pocket exit top edge (max safe — limited by slot end cap fillets) |
| 7 | `pocket_entry_top_x` | 8 mm | Pocket entry top edge |
| 8 | `pocket_entry_floor_x` | 8 mm | Pocket entry floor edge |
| 9 | `pocket_exit_floor_x` | 8 mm | Pocket exit floor edge |
| 10 | `hole_arc_y842` | 10 mm | Hole circle at y=842.5 |
| 11 | `hole_arc_y1050` | 6 mm | Hole circle at y=1050 (max safe — constrained by 50 mm corner fillets) |

---

## File Structure

```
.
├── rectangle_extrude.py   # Main CAD script
└── README.md              # This file
```

---

## License

MIT
