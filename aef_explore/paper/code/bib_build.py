"""Build references.bib from a curated DOI list, using DOI content negotiation.

Every entry is fetched from doi.org (Crossref / DataCite), so authors, year, journal, volume
and pages are the registered metadata rather than anything typed here.  The DOI list itself is
the curated part: each line is (cluster, citation key, DOI, one-line role in the argument).
Entries that fail to resolve are reported and left out -- the bibliography contains only
references that resolved.
"""
import json, os, re, sys, time, unicodedata
import urllib.request

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cache", "doi")

# cluster, key, DOI, role
ENTRIES = [
 (1, "brown2025alphaearth", "10.48550/arXiv.2507.22291", "the embedding product under test"),
 (1, "jakubik2023prithvi", "10.48550/arXiv.2310.18660", "geospatial foundation model"),
 (1, "cong2022satmae", "10.48550/arXiv.2207.08051", "temporal masked autoencoding for EO"),
 (1, "marsocci2024pangaea", "10.48550/arXiv.2412.04204", "benchmark for geospatial FMs"),
 (1, "hong2024spectralgpt", "10.1109/TPAMI.2024.3362475", "spectral foundation model"),
 (1, "sun2023ringmo", "10.1109/TGRS.2022.3194732", "masked-image-modelling FM in TGRS"),
 (1, "szwarcman2024prithvi2", "10.1109/TGRS.2025.3642610", "multitemporal FM successor"),
 (1, "manas2021seco", "10.1109/ICCV48922.2021.00928", "seasonal contrast pretraining"),
 (2, "hansen2013forest", "10.1126/science.1244693", "the annual forest-loss product family"),
 (2, "brown2022dynamicworld", "10.1038/s41597-022-01307-4", "near-real-time land cover"),
 (2, "zhu2014ccdc", "10.1016/J.RSE.2014.01.011", "continuous change detection"),
 (2, "verbesselt2010bfast", "10.1016/J.RSE.2009.08.014", "break detection in time series"),
 (2, "kennedy2010landtrendr", "10.1016/J.RSE.2010.07.008", "temporal segmentation"),
 (2, "zhu2020cold", "10.1016/J.RSE.2019.03.009", "continuous land-disturbance monitoring"),
 (2, "abercrombie2022hmm", "10.1109/TGRS.2021.3123738", "temporal consistency of annual maps"),
 (2, "zhang2020thirtym", "10.1016/j.isprsjprs.2020.01.012", "annual land-surface change detection"),
 (3, "reiche2021radd", "10.1088/1748-9326/abd0a8", "the alert product used for dating"),
 (3, "hansen2016glad", "10.1088/1748-9326/11/3/034008", "Landsat-based alerts"),
 (3, "diniz2015deterb", "10.1109/JSTARS.2015.2437075", "the reference map used here"),
 (3, "doblas2022deterr", "10.3390/rs14153658", "radar-based operational alerts"),
 (3, "reiche2024integrating", "10.1088/1748-9326/ad2d82", "alert integration and timeliness"),
 (3, "tang2019nrt", "10.1016/J.RSE.2019.02.003", "near-real-time algorithms and assessment"),
 (3, "bullock2022timeliness", "10.1016/j.rse.2022.113043", "timeliness assessment framework"),
 (3, "assis2019terrabrasilis", "10.3390/ijgi8110513", "the DETER/PRODES data infrastructure"),
 (4, "whitcraft2015cloud", "10.1016/J.RSE.2014.10.009", "cloud cover and optical observability"),
 (4, "sudmanns2019coverage", "10.1080/17538947.2019.1572799", "Sentinel-2 coverage dynamics"),
 (4, "prudente2020limitations", "10.1016/J.RSASE.2020.100414", "cloud limits in South America"),
 (4, "zhang2026optical", "10.1109/JSTARS.2026.3701406", "working around optical observation gaps"),
 (5, "reiche2018improving", "10.1016/J.RSE.2017.10.034", "SAR-optical fusion for alerts"),
 (5, "ballere2021sar", "10.1016/j.rse.2020.112159", "SAR benefit over optical in the tropics"),
 (5, "doblas2020widearea", "10.3390/rs12193263", "wide-area SAR monitoring"),
 (5, "mermoz2021cusum", "10.1016/j.jag.2021.102532", "Sentinel-1 CuSum forest-cover loss"),
 (6, "curtis2018drivers", "10.1126/science.aau3445", "why loss year and driver matter"),
 (6, "lambin2023supplychains", "10.1146/annurev-environ-112321-121436", "supply-chain cut-off dates"),
 (6, "tyukavina2018congo", "10.1126/sciadv.aat2993", "Congo Basin loss attribution"),
 (7, "roberts2017crossvalidation", "10.1111/ECOG.02881", "blocked validation with autocorrelation"),
 (7, "ploton2020spatial", "10.1038/s41467-020-18321-y", "spatial validation of large-scale models"),
 (7, "meyer2022machine", "10.1038/s41467-022-29838-9", "assessing global ML maps"),
 (7, "valavi2018blockcv", "10.1111/2041-210X.13107", "spatial block cross-validation tooling"),
 (8, "olofsson2014good", "10.1016/J.RSE.2014.02.015", "area estimation and accuracy practice"),
 (8, "stehman2019key", "10.1016/J.RSE.2019.05.018", "rigorous accuracy assessment"),
 (8, "mcroberts2018imperfect", "10.1016/J.ISPRSJPRS.2018.06.002", "imperfect reference data"),
 (8, "ye2018obia", "10.1016/J.ISPRSJPRS.2018.04.002", "object-based accuracy assessment"),
 (9, "chen2021bit", "10.1109/TGRS.2021.3095166", "transformer change detection"),
 (9, "saha2019dcva", "10.1109/TGRS.2018.2886643", "unsupervised deep change vector analysis"),
 (9, "daudt2018siamese", "10.1109/ICIP.2018.8451652", "siamese change detection"),
 (9, "chen2020dasnet", "10.1109/JSTARS.2020.3037893", "attention-based change detection"),
 (9, "chen2024changemamba", "10.1109/TGRS.2024.3417253", "state-space change detection"),
 (9, "bergamasco2023sartscc", "10.1109/TGRS.2023.3243900", "SAR time-series change detection"),
 (9, "zhu2022contrastive", "10.1109/TGRS.2022.3147513", "contrastive representations for RS"),
 (9, "wang2022largescale", "10.1016/j.isprsjprs.2022.08.012", "large-scale deep change detection"),
 (3, "wang2020lstm", "10.1109/JSTARS.2020.2988324", "sequence models for near-real-time disturbance"),
 (9, "li2024transformermad", "10.1109/JSTARS.2024.3349775", "unsupervised multivariate alteration detection"),
 (10, "kalamandeen2018pervasive", "10.1038/s41598-018-19358-2", "small-clearing dynamics in Amazonia"),
 (10, "picoli2018bigearth", "10.1016/J.ISPRSJPRS.2018.08.007", "Brazilian time-series monitoring"),
 (10, "lima2019quality", "10.1016/J.ISPRSJPRS.2021.04.014", "class noise in image time series"),
 (11, "vancutsem2021tmf", "10.1126/sciadv.abe1603", "the Congo event set"),
 (1, "wang2026harvesting", "10.1016/j.jag.2026.105258", "how AlphaEarth is currently evaluated: downstream label accuracy"),
 (1, "anon2026cloudprior", "10.1109/ICETIS70504.2026.11633492", "the assumption that AEF embeddings are robust to observational gaps"),
 (3, "chen2026operational", "10.3389/frsen.2026.1818592", "intercomparison of operational disturbance products in Brazil"),
 (2, "cohen2021disturbance", "10.1016/j.rse.2020.112244", "what governs detectability in a time series: agent and severity, not history"),
 (12, "carroll2006measurement", "10.1201/9781420010138", "attenuation from covariate error"),
]


def fetch(doi):
    os.makedirs(CACHE, exist_ok=True)
    fp = os.path.join(CACHE, re.sub(r"[^A-Za-z0-9]", "_", doi) + ".bib")
    if os.path.exists(fp):
        return open(fp).read()
    req = urllib.request.Request("https://doi.org/" + doi,
                                 headers={"Accept": "application/x-bibtex",
                                          "User-Agent": "TB01-paper/1.0 (mailto:noreply@example.org)"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                txt = r.read().decode("utf-8", "replace")
            open(fp, "w").write(txt)
            time.sleep(0.3)
            return txt
        except Exception as e:
            if attempt == 3:
                return ""
            time.sleep(2 * (attempt + 1))
    return ""


def clean(bib):
    """Strip publisher markup that Crossref sometimes embeds in titles."""
    bib = re.sub(r"</?scp>", "", bib)
    bib = re.sub(r"</?i>|</?b>|</?sub>|</?sup>", "", bib)
    bib = re.sub(r"\s{2,}", " ", bib)
    return bib


def rekey(bib, key):
    """Rewrite the citation key as surname + registered year + the curated tag, so a key can
    never disagree with the metadata it points at."""
    m = re.match(r"([a-z]+)(\d{4})(.*)", key)
    tag = m.group(3) if m else key
    author = field(bib, "author")
    surname = re.split(r",| and ", author)[0].strip().split()[-1] if author else (m.group(1) if m else "anon")
    surname = unicodedata.normalize("NFKD", surname).encode("ascii", "ignore").decode()
    surname = re.sub(r"[^A-Za-z]", "", surname).lower() or "anon"
    year = field(bib, "year") or (m.group(2) if m else "0000")
    new = f"{surname}{year}{tag}"
    return re.sub(r"^(@\w+\{)[^,]+,", r"\1" + new + ",", bib.strip(), count=1), new


def field(bib, name):
    """Read one BibTeX field, tolerating brace nesting and either delimiter."""
    m = re.search(r"\b" + name + r"\s*=\s*", bib, re.I)
    if not m:
        return ""
    i = m.end()
    if bib[i] not in "{\"":
        j = bib.find(",", i)
        return bib[i:j].strip()
    close = "}" if bib[i] == "{" else "\""
    depth, j = 0, i
    for j in range(i, len(bib)):
        if bib[j] == "{":
            depth += 1
        elif bib[j] == close:
            depth -= 1
            if depth == 0:
                break
    return re.sub(r"\s+", " ", bib[i + 1:j]).strip()


def main():
    out, meta, failed = [], [], []
    for cluster, key, doi, role in ENTRIES:
        bib = fetch(doi)
        if not bib.strip().startswith("@"):
            failed.append((key, doi))
            continue
        entry, key = rekey(clean(bib), key)
        out.append(entry)
        meta.append(dict(cluster=cluster, key=key, doi=doi, role=role,
                         title=field(bib, "title"), year=field(bib, "year"),
                         venue=field(bib, "journal") or field(bib, "booktitle")
                         or field(bib, "publisher"),
                         author=field(bib, "author")))
    with open("aef_explore/paper/references.bib", "w") as f:
        f.write("% TB01 manuscript bibliography.\n"
                "% Every entry is the registered DOI metadata, fetched by content negotiation\n"
                "% from doi.org; see LITERATURE_MAP.md for the cluster each entry serves.\n\n")
        f.write("\n\n".join(out) + "\n")
    json.dump(meta, open("aef_explore/paper/code/bib_meta.json", "w"), indent=1)
    print("entries", len(out), "failed", failed)
    from collections import Counter
    print(Counter(m["venue"][:52] for m in meta).most_common())


if __name__ == "__main__":
    main()
