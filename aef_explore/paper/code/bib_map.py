"""Write LITERATURE_MAP.md from the verified bibliography metadata."""
import json
from collections import Counter, defaultdict

CLUSTERS = {
 1: ("Geospatial foundation models and embedding products",
     "What the object under test is, and what the field currently asks of it."),
 2: ("Temporal semantics of annual composites and products",
     "The prior art on when a change enters an annual product -- the question this paper asks of embeddings."),
 3: ("Deforestation alert systems and their latency",
     "Where the event dates come from, and how their own latency propagates into this study."),
 4: ("Cloud cover and optical observation supply in the tropics",
     "The mechanism the paper identifies as binding."),
 5: ("SAR-optical fusion for deforestation",
     "The obvious remedy, and the evidence on whether it compensates."),
 6: ("Loss-year attribution, carbon accounting and regulatory cut-offs",
     "Why the year a clearing is assigned to has consequences outside remote sensing."),
 7: ("Spatial cross-validation and block bootstrap",
     "The inference machinery: why every CI here is blocked."),
 8: ("Reference-data quality, polygon geometry and positional error",
     "Why the reference map is a measurement instrument, not ground truth."),
 9: ("Change detection with learned representations",
     "The methodological neighbourhood of angular change in an embedding space."),
 10: ("Amazon deforestation dynamics and seasonality",
      "Why the calendar month of a clearing is not random."),
 11: ("Congo Basin forest monitoring",
      "The second region, and why its reference data are a different kind of object."),
 12: ("Measurement error, attenuation and lower-bound reasoning",
      "Why a dating error makes the reported effect a lower bound."),
}
VENUE_TARGETS = {"Remote Sensing of Environment": 8,
                 "IEEE Transactions on Geoscience and Remote Sensing": 6,
                 "IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing": 4,
                 "ISPRS Journal of Photogrammetry and Remote Sensing": 5}
MDPI = ("Remote Sensing", "ISPRS International Journal of Geo-Information", "Sensors",
        "Forests", "Land", "Sustainability")


def main():
    meta = json.load(open("aef_explore/paper/code/bib_meta.json"))
    by = defaultdict(list)
    for m in meta:
        by[m["cluster"]].append(m)
    venues = Counter(m["venue"] for m in meta)
    lines = ["# Literature map — every reference, its cluster and the job it does",
             "",
             f"**{len(meta)} references**, all resolved by DOI content negotiation from doi.org "
             "(Crossref / DataCite); `references.bib` holds the registered metadata verbatim. "
             "Candidates were found with the Semantic Scholar Graph API (cached under "
             "`cache/`, one request per second); the curation — which candidate answers which "
             "part of the argument — is in the `ENTRIES` table of `code/bib_build.py`.", ""]
    lines += ["## Venue distribution", "",
              "| venue | n | target |", "|---|---|---|"]
    for v, n in venues.most_common():
        tgt = VENUE_TARGETS.get(v)
        mark = f"≥ {tgt} ✔" if tgt and n >= tgt else (f"≥ {tgt} ✘" if tgt else "—")
        lines.append(f"| {v} | {n} | {mark} |")
    mdpi = sum(n for v, n in venues.items() if v in MDPI)
    lines += ["", f"MDPI titles: **{mdpi}** (ceiling 5) ✔" if mdpi <= 5 else
              f"MDPI titles: **{mdpi}** (ceiling 5) ✘", ""]
    lines += ["## Clusters", ""]
    for c in sorted(by):
        name, why = CLUSTERS[c]
        lines += [f"### {c}. {name}", "", f"*{why}*", "",
                  "| reference | venue, year | what it supplies |", "|---|---|---|"]
        for m in sorted(by[c], key=lambda x: x["year"]):
            au = m["author"].split(" and ")[0].split(",")[0]
            more = " et al." if " and " in m["author"] else ""
            lines.append(f"| `{m['key']}` — {au}{more} | {m['venue']}, {m['year']} | {m['role']} |")
        lines.append("")
    open("aef_explore/paper/LITERATURE_MAP.md", "w").write("\n".join(lines) + "\n")
    print("clusters", sorted(by), "n", len(meta), "mdpi", mdpi)


if __name__ == "__main__":
    main()
