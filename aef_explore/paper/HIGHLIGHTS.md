# Highlights

Five statements, each within the 85-character limit; character counts in brackets.

1. Annual embedding registers 97.5% of clearings seen 5+ times after the event  [75]
2. It registers only 51% of those seen twice or fewer: a 46.5-point gap  [68]
3. Radar does not compensate; registration falls as Sentinel-1 density rises  [73]
4. Missed events are deferred, not lost: 94-97% register the following year  [72]
5. Alert dating vintage sets the effect size, and can erase it entirely  [68]
<!-- verification: python -c "for l in open('HIGHLIGHTS.md'):
     import re; m=re.match(r'\d+\. (.+?)\s+\[(\d+)\]', l)
     if m: assert len(m.group(1))==int(m.group(2))<=85, l" -->

# Graphical abstract — specification

**Format.** Single panel, 190 mm × 95 mm at 300 dpi, no caption, legible at 50 % reduction;
minimum type 8 pt. Same palette as the manuscript figures: sequential blue for supply,
categorical blue for 2021 and orange for 2020, red only for the flagged quantity.

**Composition, left to right in three bands.**

*Left third — the mechanism.* A schematic calendar strip for one year, twelve cells, shaded by
expected clear-observation supply using the F7 ramp, with two clearing icons pinned to it: one
in July over a dark (well-observed) cell, one in November over a pale (poorly observed) cell.
A short label beneath: "when the clearing happens decides what the year's vector sees".

*Middle third — the measurement.* The registration curve from F1a, stripped to a single line
with its bootstrap band, the two clearing icons from the left band placed on it at their
respective observation counts, and the two probabilities called out: 0.98 for the July event,
0.51 for the November one. Axis labels only, no gridlines, no legend.

*Right third — the consequence.* Two stacked rows of one hundred small squares each,
representing a hundred late-year clearings. The upper row shows the year-of-event outcome —
about half filled, half hollow. The lower row shows the same hundred one year later, with
essentially all filled. Label: "deferred, not missed — 94–97 % appear the next year".

**One-line takeaway across the base.** "An annual embedding sees what the year let it see:
late-year clearings in cloudy places arrive a year late."

**What to avoid.** No map background — the point is temporal, and a map invites the reader to
look for spatial pattern that this abstract is not making. No third series. No photographic
imagery of deforestation; the argument is about observation, not about impact.
