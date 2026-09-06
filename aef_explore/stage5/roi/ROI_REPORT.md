# TB01 Custom Satellite Embeddings — ROI Report

**Asset ID:** `projects/alpha-earth-app/assets/TB01_custom_embedding_roi`
**Public ACL:** verified by read-back — `{"owners": [], "readers": [], "writers": [], "all_users_can_read": true}`
**DETER:** INPE TerraBrasilis WFS `deter-amz:deter_amz`, 2021 `DESMATAMENTO_CR`+`DESMATAMENTO_VEG` (37,938 polygons); counts = polygon centroids inside box.
**Forest 2020:** Hansen GFC v1.11, treecover2000 >= 30% minus loss through 2020, mean at 300 m.
**Clear obs:** S2_SR_HARMONIZED 2021, SCL-masked per-pixel count of clear observations, mean at 100 m.

## Final boxes (80 x 80 km each)
- **Box A** `BoxA_BR163_Para` — bbox **-56.3, -5.2, -55.5788, -4.4765** — DETER 631 — forest 68.1% — clear obs 32.7 — 6428.5 km2
- **Box B** `BoxB_Roraima` — bbox **-60.6, 0.6, -59.8812, 1.3235** — DETER 227 — forest 68.1% — clear obs 30.4 — 6429.1 km2

Both fully inside the Brazilian Legal Amazon (A entirely in Para, B entirely in Roraima); no overlap.

## Box B search — top 5 by lowest clear-obs (AM/RR/AP, >= 150 DETER 2021 events, forest >= 60%, inside Legal Amazon)
| id | state(s) | DETER 2021 | forest 2020 | clear obs | ratio to Box A | bbox W,S,E,N | pick |
|---|---|---|---|---|---|---|---|
| C12 | Roraima | 227 | 68.1% | 30.4 | 0.93 | -60.6, 0.6, -59.8812, 1.3235 | **Box B**
| C3 | Amazonas | 626 | 90.3% | 35.7 | 1.09 | -63.25, -7.25, -62.5261, -6.5265 |
| C7 | Acre/Amazonas | 382 | 68.8% | 36.0 | 1.10 | -68.0, -9.6, -67.2719, -8.8765 |
| C4 | Amazonas | 550 | 62.5% | 37.6 | 1.15 | -67.25, -9.2, -66.5227, -8.4765 |
| C13 | Amazonas | 219 | 89.7% | 37.7 | 1.15 | -60.7, -7.55, -59.9757, -6.8265 |

**No candidate reached the <= 70% target.** Per the fallback rule Box B is the lowest-ratio candidate with >= 150 events: C12, Roraima, **achieved ratio 0.931** (30.4 vs 32.7 clear observations). C12 is also the required explicit Roraima candidate; its Dec-Mar dry season is out of phase with Box A's, so clearing and observation timing differ even though the annual observation counts are close.

## Area budget
Per box 6428.5 + 6429.1 km2 = total **12857.6 km2**; cumulative = 12857.6 x 20 embeddings = **257,153 km2** < 300,000 km2.

## Methods note — observability bias of alert-based references
Across all 17 distinct candidate boxes evaluated, DETER 2021 event count vs 2021 clear-observation count gives Pearson r = **0.25** (p = 0.33), Spearman rho = 0.07 (p = 0.79) — positive but weak and not statistically significant at n = 17. The candidate set is range-restricted (all boxes were pre-selected as high-alert-density), which attenuates the correlation; it therefore bounds rather than demonstrates the bias. The stronger operational evidence is the search outcome itself: no box in Amazonas/Roraima/Amapa with >= 150 alerts had <= 70% of Box A's observations, i.e. low-observability terrain does not produce high alert counts. TB01 should state that DETER supervision is conditioned on optical visibility and cannot be treated as an unbiased label set.
