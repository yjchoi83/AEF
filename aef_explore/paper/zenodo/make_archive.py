"""Assemble the Zenodo deposit for the manuscript.

Stages every file the deposit should contain into `data/zenodo_staging/`, which is outside
version control, and writes the manifest that accompanies it. Nothing is copied into the git
tree: the event tables are already versioned here, and the map layers are large binaries that
were deliberately kept out of it.

Run from the repository root:  python aef_explore/paper/zenodo/make_archive.py
"""
import glob
import hashlib
import os
import shutil

ROOT = "."
STAGE = "data/zenodo_staging"
MANIFEST = "aef_explore/paper/zenodo/MANIFEST.md"

GROUPS = [
    ("event_tables", "Event tables — one row per clearing event, the analysis inputs", [
        ("aef_explore/stage5/TB01/P2/P2_events.csv", "2021 Brazilian events, all covariates"),
        ("aef_explore/stage5/TB01/P2b/P2b_events_2020.csv", "2020 Brazilian events"),
        ("aef_explore/stage5/TB01/P2b/P2b_offset_2021.csv", "2021 offset diagnostic"),
        ("aef_explore/paper/code/offset_2020.csv", "2020 offset diagnostic"),
        ("aef_explore/paper/code/deferral_2020.csv", "2020 to 2021 deferral"),
        ("aef_explore/paper/code/s1_post_2020_derived.csv", "2020 s1_post under both dating rules"),
        ("aef_explore/stage5/TB01/P5b/zero_bin_gee_extract.csv", "zero-observation stratum diagnostic"),
        ("aef_explore/stage5/TB01/P3/P3_table.csv", "2021 deferral and attribution"),
        ("aef_explore/stage5/TB01/P4/P4_table.csv", "Congo patches, 2024-vintage dating"),
        ("aef_explore/stage5/TB01/P5b/P4b_events_redated.csv", "Congo patches, 2021-vintage dating"),
    ]),
    ("model_code", "Model code — everything that turns the tables into the reported numbers", [
        ("aef_explore/paper/code/p2_model.py", "the event-level model and block bootstrap"),
        ("aef_explore/paper/code/run_numbers.py", "re-derives every number in the manuscript"),
        ("aef_explore/paper/code/intensity.py", "change-intensity comparison, Section 4.4"),
        ("aef_explore/paper/code/deferral_ci.py", "interval for the 2020 to 2021 deferral"),
        ("aef_explore/paper/code/numbers_trace.py", "writes NUMBERS_TRACE.md"),
        ("aef_explore/paper/code/supplementary.py", "writes SUPPLEMENTARY.md"),
        ("aef_explore/paper/numbers.json", "the re-derived numbers themselves"),
        ("aef_explore/paper/intensity_stats.json", "Section 4.4 statistics"),
    ]),
    ("extraction_code", "Extraction code — the Earth Engine and WFS steps that built the tables", [
        ("aef_explore/paper/code/extract_s1_2020.py", "monthly Sentinel-1 counts, 2020"),
        ("aef_explore/paper/code/offset_2020.py", "2020 offset diagnostic"),
        ("aef_explore/paper/code/deferral_2020.py", "2020 to 2021 deferral"),
        ("aef_explore/paper/code/get_outlines.py", "country outlines for the maps"),
    ]),
    ("figure_code", "Figure code — reproduces every figure at submission specification", [
        ("aef_explore/paper/code/figstyle.py", "shared style: 300 dpi, column widths, palette"),
        ("aef_explore/paper/code/fig_study_area.py", "Fig. 1"),
        ("aef_explore/paper/code/fig_results.py", "Figs. 2-6, 8, 9"),
        ("aef_explore/paper/code/fig_offset.py", "Fig. 7"),
        ("aef_explore/paper/code/fig_maps.py", "Figs. M1, M2"),
        ("aef_explore/paper/code/legal_amazon_states.geojson", "Legal Amazon state boundaries"),
        ("aef_explore/paper/code/legal_amazon_boundary.geojson", "Legal Amazon limit"),
        ("aef_explore/paper/code/outlines.geojson", "country outlines"),
    ]),
    ("manuscript", "Manuscript and submission files", [
        ("aef_explore/paper/MANUSCRIPT.md", "manuscript, citation keys"),
        ("aef_explore/paper/MANUSCRIPT_RSE.md", "manuscript, author-date citations and reference list"),
        ("aef_explore/paper/SUPPLEMENTARY.md", "supplementary tables"),
        ("aef_explore/paper/NUMBERS_TRACE.md", "provenance of every number"),
        ("aef_explore/paper/references.bib", "bibliography, DOI-resolved"),
        ("aef_explore/paper/LITERATURE_MAP.md", "reference clusters"),
        ("aef_explore/paper/HIGHLIGHTS.md", "highlights and graphical-abstract specification"),
        ("aef_explore/paper/build.md", "build instructions"),
    ]),
]

# 100 m map layers, matched by pattern because they are tiled
RASTERS = [("map_layers_100m", "Map layers — the demonstration regions, GeoTIFF", [
    ("data/products/*_ang2021_x100_100m_r*.tif", "2020-2021 angular change x100, Int16, 100 m"),
    ("data/products/*_reg2021_100m_r*.tif", "registration mask, 100 m"),
    ("data/products/*_defer2022_100m_r*.tif", "registers in 2022 having not in 2021, 100 m"),
    ("data/products/*_obs_supply_x10_200m.tif", "monthly clear-observation supply x10, 200 m"),
    ("data/products/*_deferral_risk_x1000_200m.tif", "deferral risk x1000, 200 m"),
])]


def sha(path, n=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(n)
            if not b:
                break
            h.update(b)
    return h.hexdigest()[:16]


def human(nbytes):
    for unit in ("B", "kB", "MB", "GB"):
        if nbytes < 1024 or unit == "GB":
            return f"{nbytes:.0f} {unit}" if unit == "B" else f"{nbytes:.1f} {unit}"
        nbytes /= 1024


def main():
    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    rows, total, missing = [], 0, []
    for folder, title, items in GROUPS:
        os.makedirs(f"{STAGE}/{folder}", exist_ok=True)
        rows.append((None, title))
        for src, note in items:
            if not os.path.exists(src):
                missing.append(src)
                continue
            dst = f"{STAGE}/{folder}/{os.path.basename(src)}"
            shutil.copy2(src, dst)
            size = os.path.getsize(src)
            total += size
            rows.append((f"{folder}/{os.path.basename(src)}", f"{note} | {human(size)} | `{sha(src)}`"))
    for folder, title, patterns in RASTERS:
        os.makedirs(f"{STAGE}/{folder}", exist_ok=True)
        rows.append((None, title))
        for pat, note in patterns:
            files = sorted(glob.glob(pat))
            if not files:
                missing.append(pat)
                continue
            n, size = len(files), sum(os.path.getsize(f) for f in files)
            total += size
            for f in files:
                shutil.copy2(f, f"{STAGE}/{folder}/{os.path.basename(f)}")
            rows.append((f"{folder}/{os.path.basename(pat)}",
                         f"{note} | {n} file(s), {human(size)} | —"))
    lines = ["# Zenodo deposit — manifest", "",
             f"Assembled by `make_archive.py` into `{STAGE}/` (outside version control). "
             f"Total **{human(total)}** across "
             f"{sum(1 for r in rows if r[0])} entries.", "",
             "| file | contents | size | sha256 (16) |", "|---|---|---|---|"]
    for path, note in rows:
        if path is None:
            lines.append(f"| | **{note}** | | |")
        else:
            lines.append(f"| `{path}` | {note} |")
    if missing:
        lines += ["", "**Missing at assembly time** (regenerate before depositing):", ""]
        lines += [f"- `{m}`" for m in missing]
    open(MANIFEST, "w").write("\n".join(lines) + "\n")
    print(f"staged {sum(1 for r in rows if r[0])} entries, {human(total)}, into {STAGE}")
    if missing:
        print("MISSING:", missing)


if __name__ == "__main__":
    main()
