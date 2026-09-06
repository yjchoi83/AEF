# Stage-4 N — Novelty re-verification: TB01, TB02, TC01

Session note: Semantic Scholar and arXiv were both persistently rate-limited (HTTP 429) for
most of this session, including >15 spaced retries (sleeps of 10-20s between calls, plus one
successful cooldown probe) on both hosts; OpenAlex returned a daily budget-exhaustion error
(unrelated to this session's usage) and was unusable throughout. Only one broad arXiv query
("all:AlphaEarth", run early in the session before rate-limiting set in) returned data. All
other targeted mechanism queries below returned 429 and are marked unresolved [U-429] — they
were NOT used to argue anything; per rule they simply could not contribute evidence either way.
This is recorded honestly rather than papered over; coverage below is thinner than the 6-9
queries/topic target for that reason.

## TB01 (GO) — Within-year timing in annual embeddings

Queries attempted (topic-specific):
- [arXiv] all:embedding AND all:deforestation — 429 [U-429]
- [arXiv] all:AlphaEarth AND all:deforestation — 429 [U-429]
- [arXiv] all:annual AND all:composite AND all:change — 429 [U-429]
- [arXiv] all:foundation AND all:model AND all:timing — 429 [U-429]
- [arXiv] all:phenology AND all:annual AND all:embedding — 429 [U-429]
- [arXiv] all:AlphaEarth AND all:forest — 429 [U-429]
- [arXiv] all:AlphaEarth (broad, run pre-rate-limit) — 200, verified, see table
- [S2] "AlphaEarth annual embedding within-year timing" and 6 other phrase queries — could not
  be distinguished from 429 (jq silently empties `.data[]?` on an error object too), so NOT
  claimed as zero-hit evidence; treated as [U-429].

| Title | Year | Venue | ID | V/U | Relation |
|---|---|---|---|---|---|
| Tree species mapping in Denmark: comparison of spectral-temporal features with GFM embeddings | 2026 | arXiv | arXiv:2609.03480 | V | IRRELEVANT (species mapping, no within-year timing) |
| Do Satellites See Commuters? A Critical Benchmark of Vision Foundation Models | 2026 | arXiv | arXiv:2609.00661 | V | IRRELEVANT |
| BEACON: Behavioral/Semantic Enrichment of AlphaEarth Embeddings via Tri-Modal Contrastive Learning | 2026 | arXiv | arXiv:2608.29553 | V | IRRELEVANT |
| Cross-View Urban Sensing: Streetscape Perception via AlphaEarth Embeddings | 2026 | arXiv | arXiv:2608.16310 | V | IRRELEVANT |
| Evaluating AlphaEarth Foundations Embeddings for Wildfire Susceptibility Mapping | 2026 | arXiv | arXiv:2608.12663 | V | ADJACENT (annual-embedding change signal, but hazard susceptibility not event-month recovery) |
| Above-ground Biomass Estimation with Geospatial Foundation Models | 2026 | arXiv | arXiv:2608.04792 | V | IRRELEVANT (structural regression target) |

Verdict: **SURVIVES** (low-confidence due to thin coverage). No verified paper measures
event-month recoverability or within-year mixing of an annual embedding product. The one clean
hit set (broad "AlphaEarth" arXiv query) contains no candidate on this mechanism — all are
IRRELEVANT/ADJACENT application papers. Mechanism-specific queries (timing, phenology, event
date) could not be run due to rate-limiting; this is a coverage gap, not evidence of survival,
and should be re-run next session. No mandatory new citation/baseline identified this pass
beyond the base AlphaEarth Foundations paper (already known, not re-verified this pass since
the query for it also 429'd).

## TB02 (C-GO) — Observation-availability artefacts (Sentinel-1B outage)

Queries attempted:
- [arXiv] all:Sentinel-1B — 429 [U-429]
- [arXiv] all:Sentinel-1B AND all:outage — 429 [U-429]
- [arXiv] all:SAR AND all:gap AND all:change — 429 [U-429]
- [arXiv] all:sensor AND all:outage AND all:foundation — 429 [U-429]
- [arXiv] all:missing AND all:observation AND all:change — 429 [U-429]
- [arXiv] all:AlphaEarth AND all:change AND all:detection — 429 [U-429]
- [S2] "Sentinel-1B outage SAR data gap change detection" and 6 related mechanism queries —
  [U-429] (same ambiguity issue as above, not claimed as zero-hit).

No table rows — every query targeting this topic's mechanism returned 429; the one clean
broad-query result set from TB01 (generic "AlphaEarth") contains no Sentinel-1B / SAR-outage /
observation-availability paper among its titles, but that query was not designed to surface
this mechanism and is not strong evidence either way.

Verdict: **SURVIVES** (unverified this pass — insufficient query coverage). No kill or
threatening reference was found, but none of the targeted queries executed successfully, so
this is an absence-of-attempt result, not an absence-of-evidence result. Must re-run before
finalizing Stage 4 for this topic.

## TC01 (C-GO) — Dimension-level attribution of static/climate-input dependence

Queries attempted:
- [arXiv] all:static AND all:covariate AND all:foundation — 429 [U-429]
- [arXiv] all:terrain AND all:leakage AND all:embedding — 429 [U-429]
- [arXiv] all:terrain AND all:leakage — 429 [U-429]
- [arXiv] all:dimension AND all:ablation AND all:transfer — 429 [U-429]
- [arXiv] all:AlphaEarth AND all:terrain — 429 [U-429]
- [arXiv] all:foundation AND all:interpretability AND all:dimension — 429 [U-429]
- [S2] "static covariate leakage foundation model geospatial" and 6 related mechanism queries —
  [U-429] (same ambiguity issue, not claimed as zero-hit).

No table rows — every query targeting this topic's mechanism returned 429. The generic
"AlphaEarth" broad-query result set (TB01 table) contains no dimension-attribution / terrain-
decodability / static-leakage paper, but again this is a byproduct of a differently-aimed query,
not a targeted search.

Verdict: **SURVIVES** (unverified this pass — insufficient query coverage). No kill or
threatening reference found; flag for mandatory re-query next session once rate limits clear.

## Summary of coverage gap

Both Semantic Scholar and arXiv (export.arxiv.org) returned HTTP 429 for the overwhelming
majority of calls attempted in this session, including after multiple 10-20s backoff retries
and one confirmed successful recovery window that closed again immediately. Per rule 3.1, no
argument was built on unverifiable data; all 429 responses are recorded as [U-429] and excluded
from the verdicts, which are therefore "no kill found, coverage incomplete" rather than a clean
SURVIVES with full 6-9-query coverage per topic. Re-run recommended in a later, less-throttled
session before this item is marked closed.
