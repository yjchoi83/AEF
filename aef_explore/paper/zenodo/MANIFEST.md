# Zenodo deposit — manifest

Assembled by `make_archive.py` into `data/zenodo_staging/` (outside version control). Total **43.5 MB** across 43 entries.

| file | contents | size | sha256 (16) |
|---|---|---|---|
| | **Event tables — one row per clearing event, the analysis inputs** | | |
| `event_tables/P2_events.csv` | 2021 Brazilian events, all covariates | 7.1 MB | `acdeed2cf4f6d9cb` |
| `event_tables/P2b_events_2020.csv` | 2020 Brazilian events | 7.1 MB | `09a2bb8778be5ac9` |
| `event_tables/P2b_offset_2021.csv` | 2021 offset diagnostic | 74.6 kB | `678e18120c6cf6f8` |
| `event_tables/offset_2020.csv` | 2020 offset diagnostic | 66.6 kB | `c9b98e1264d7fad3` |
| `event_tables/deferral_2020.csv` | 2020 to 2021 deferral | 58.4 kB | `d9bb6b7e5319bfce` |
| `event_tables/s1_post_2020_derived.csv` | 2020 s1_post under both dating rules | 1.5 MB | `1bd2049f973a04f9` |
| `event_tables/zero_bin_gee_extract.csv` | zero-observation stratum diagnostic | 264.4 kB | `506a533708b5d718` |
| `event_tables/P3_table.csv` | 2021 deferral and attribution | 1.9 MB | `535b0d8fa965e8dd` |
| `event_tables/P4_table.csv` | Congo patches, 2024-vintage dating | 334.3 kB | `f45ecf03ca682ed8` |
| `event_tables/P4b_events_redated.csv` | Congo patches, 2021-vintage dating | 676.8 kB | `26768b9897f60549` |
| | **Model code — everything that turns the tables into the reported numbers** | | |
| `model_code/p2_model.py` | the event-level model and block bootstrap | 11.8 kB | `878259c7931f55d6` |
| `model_code/run_numbers.py` | re-derives every number in the manuscript | 4.0 kB | `1ca05b8ec83a6c62` |
| `model_code/intensity.py` | change-intensity comparison, Section 4.4 | 6.8 kB | `dad1b7e5aa26e4a7` |
| `model_code/deferral_ci.py` | interval for the 2020 to 2021 deferral | 798 B | `5d9917acac3ea190` |
| `model_code/numbers_trace.py` | writes NUMBERS_TRACE.md | 13.6 kB | `670615e41bd897be` |
| `model_code/supplementary.py` | writes SUPPLEMENTARY.md | 15.7 kB | `686b6c1bd835d8c5` |
| `model_code/numbers.json` | the re-derived numbers themselves | 23.1 kB | `e4c0cdacce2ea685` |
| `model_code/intensity_stats.json` | Section 4.4 statistics | 2.7 kB | `8cdf2c7cac1eebe4` |
| | **Extraction code — the Earth Engine and WFS steps that built the tables** | | |
| `extraction_code/extract_s1_2020.py` | monthly Sentinel-1 counts, 2020 | 2.2 kB | `73633335556f9b95` |
| `extraction_code/offset_2020.py` | 2020 offset diagnostic | 4.4 kB | `c5e26812beba81ae` |
| `extraction_code/deferral_2020.py` | 2020 to 2021 deferral | 4.3 kB | `8600cfdab1aea8d9` |
| `extraction_code/get_outlines.py` | country outlines for the maps | 1.0 kB | `8757b80d7d78717d` |
| | **Figure code — reproduces every figure at submission specification** | | |
| `figure_code/figstyle.py` | shared style: 300 dpi, column widths, palette | 1.8 kB | `521f99882d828bbe` |
| `figure_code/fig_study_area.py` | Fig. 1 | 7.5 kB | `4fb5e47b67cb71e1` |
| `figure_code/fig_results.py` | Figs. 2-6, 8, 9 | 19.3 kB | `15d1c730c22c1551` |
| `figure_code/fig_offset.py` | Fig. 7 | 6.4 kB | `db76bc5bc2f02e0f` |
| `figure_code/fig_maps.py` | Figs. M1, M2 | 6.6 kB | `37f101180692f751` |
| `figure_code/legal_amazon_states.geojson` | Legal Amazon state boundaries | 323.7 kB | `22111af725d4ae90` |
| `figure_code/legal_amazon_boundary.geojson` | Legal Amazon limit | 41.3 kB | `2d577ad7aac7153f` |
| `figure_code/outlines.geojson` | country outlines | 188.1 kB | `e6623fd40da6b3f1` |
| | **Manuscript and submission files** | | |
| `manuscript/MANUSCRIPT.md` | manuscript, citation keys | 65.6 kB | `f1b6046503de79a4` |
| `manuscript/MANUSCRIPT_RSE.md` | manuscript, author-date citations and reference list | 83.4 kB | `762c3ec65115ead2` |
| `manuscript/SUPPLEMENTARY.md` | supplementary tables | 15.4 kB | `b0a6cd78ac0493d8` |
| `manuscript/NUMBERS_TRACE.md` | provenance of every number | 10.4 kB | `31eeee5589fdc26e` |
| `manuscript/references.bib` | bibliography, DOI-resolved | 34.4 kB | `7f78aa39d2f36e70` |
| `manuscript/LITERATURE_MAP.md` | reference clusters | 16.0 kB | `3ed1d99d4bff22e4` |
| `manuscript/HIGHLIGHTS.md` | highlights and graphical-abstract specification | 2.8 kB | `1859d61514d3cff6` |
| `manuscript/build.md` | build instructions | 5.4 kB | `6528c79257a8fa36` |
| | **Map layers — the demonstration regions, GeoTIFF** | | |
| `map_layers_100m/*_ang2021_x100_100m_r*.tif` | 2020-2021 angular change x100, Int16, 100 m | 20 file(s), 7.7 MB | — |
| `map_layers_100m/*_reg2021_100m_r*.tif` | registration mask, 100 m | 20 file(s), 254.4 kB | — |
| `map_layers_100m/*_defer2022_100m_r*.tif` | registers in 2022 having not in 2021, 100 m | 20 file(s), 135.0 kB | — |
| `map_layers_100m/*_obs_supply_x10_200m.tif` | monthly clear-observation supply x10, 200 m | 2 file(s), 8.4 MB | — |
| `map_layers_100m/*_deferral_risk_x1000_200m.tif` | deferral risk x1000, 200 m | 2 file(s), 7.2 MB | — |
