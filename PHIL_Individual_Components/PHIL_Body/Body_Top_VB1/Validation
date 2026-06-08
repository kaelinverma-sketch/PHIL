"""
volumetric_validation.py

Place this script inside any part folder and run it:
    python volumetric_validation.py

What it does:
- Looks in its own folder for a pair of files sharing the same stem:
    {stem}.stl / {stem}.step / {stem}.stp      ← output (your CAD export)
    source_{stem}.stl / source_{stem}.step / source_{stem}.stp  ← reference
- Any combination of formats is supported (e.g. output=STEP, source=STL)
- Computes absolute and percentage volume difference
- Logs result to volumetric_validation.log in the same folder

Requires:
    pip install numpy-stl build123d
"""

import logging
from datetime import datetime
from pathlib import Path

import numpy as np
from stl import mesh


LOG_FILE = "volumetric_validation.log"

# Extensions recognised per format group
STL_EXTS  = {".stl"}
STEP_EXTS = {".step", ".stp"}
ALL_EXTS  = STL_EXTS | STEP_EXTS


# ── Logging setup ─────────────────────────────────────────────────────────────

def setup_logging(folder: Path) -> logging.Logger:
    log = logging.getLogger("vol_validation")
    log.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        "%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fh = logging.FileHandler(folder / LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(fmt)
    log.addHandler(fh)
    log.addHandler(ch)
    return log


# ── Volume calculation ────────────────────────────────────────────────────────

def _stl_volume(path: Path) -> float:
    """Signed-tetrahedron volume sum for a closed STL mesh (vectorised)."""
    m = mesh.Mesh.from_file(str(path))
    v0 = m.vectors[:, 0, :]
    v1 = m.vectors[:, 1, :]
    v2 = m.vectors[:, 2, :]
    # dot(v0, cross(v1, v2)) / 6 for every triangle, then sum
    crosses = np.cross(v1, v2)
    signed_vols = np.einsum("ij,ij->i", v0, crosses) / 6.0
    return abs(float(signed_vols.sum()))


def _step_volume(path: Path) -> float:
    """Volume of a STEP file via build123d Shape mass properties (mm³)."""
    # Import here so the script still works without build123d when only STLs are used
    from build123d import Shape
    shape = Shape.import_step(str(path))
    vol = shape.volume          # build123d returns mm³ for mm-unit files
    if vol is None or vol == 0:
        raise ValueError("build123d returned zero/None volume — check STEP file integrity.")
    return abs(float(vol))


def compute_volume(path: Path) -> float:
    """Dispatch to the correct volume routine based on file extension."""
    ext = path.suffix.lower()
    if ext in STL_EXTS:
        return _stl_volume(path)
    if ext in STEP_EXTS:
        return _step_volume(path)
    raise ValueError(f"Unsupported file extension: {ext!r}")


def format_label(path: Path) -> str:
    return f"{path.name} ({path.suffix.upper().lstrip('.')})"


# ── Pair detection ────────────────────────────────────────────────────────────

def find_pair(folder: Path):
    """
    Scan folder for a matched output + source file sharing the same stem.

    Supported combos (any mix):
        {stem}.stl          ↔  source_{stem}.stl
        {stem}.step / .stp  ↔  source_{stem}.step / .stp
        {stem}.stl          ↔  source_{stem}.step / .stp   (cross-format)
        {stem}.step / .stp  ↔  source_{stem}.stl            (cross-format)

    Returns (output_file, source_file, stem) or (None, None, None).
    """
    all_files = [f for f in folder.iterdir() if f.suffix.lower() in ALL_EXTS]

    # Separate output and source files
    source_files = {f for f in all_files if f.stem.startswith("source_")}
    output_files = all_files  # source files that happen to match are ignored below

    # Build stem → source_file map  (strip "source_" prefix from stem)
    source_map: dict[str, Path] = {}
    for sf in source_files:
        bare_stem = sf.stem[len("source_"):]   # remove "source_" prefix
        source_map[bare_stem] = sf

    # Find first output file whose stem has a matching source
    for of in output_files:
        if of.stem.startswith("source_"):
            continue
        if of.stem in source_map:
            return of, source_map[of.stem], of.stem

    return None, None, None


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    folder = Path(__file__).parent.resolve()
    log = setup_logging(folder)

    log.info("=" * 60)
    log.info(f"volumetric_validation.py started — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info(f"Folder : {folder}")

    output_file, source_file, stem = find_pair(folder)

    if output_file is None:
        log.error(
            "No matching pair found. Expected files like:\n"
            "  {stem}.stl/.step/.stp  AND  source_{stem}.stl/.step/.stp"
        )
        return

    log.info(f"Stem   : {stem}")
    log.info(f"Output : {format_label(output_file)}")
    log.info(f"Source : {format_label(source_file)}")

    try:
        vol_output = compute_volume(output_file)
        vol_source = compute_volume(source_file)

        abs_diff = abs(vol_output - vol_source)
        pct_diff = (abs_diff / vol_source * 100.0) if vol_source != 0 else float("inf")

        log.info(f"Source volume : {vol_source:>14.2f} mm³")
        log.info(f"Output volume : {vol_output:>14.2f} mm³")
        log.info(f"Difference    : {abs_diff:>14.2f} mm³  ({pct_diff:.4f}%)")

    except Exception as e:
        log.error(f"Failed to compute volume: {e}")

    log.info("=" * 60)
    log.info(f"Log saved to: {folder / LOG_FILE}")


if __name__ == "__main__":
    main()
