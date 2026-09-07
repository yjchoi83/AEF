# Build instructions

Everything in this directory is plain text plus PNGs, so the manuscript builds with pandoc and
a CSL style. Nothing here requires a LaTeX class from the publisher; the output is a submission
draft, not a typeset proof.

## Prerequisites

    pandoc >= 3.1
    pandoc citeproc (bundled with pandoc since 2.11 — no separate filter needed)
    a LaTeX engine for PDF output (xelatex recommended, for the degree signs and accents)

Fetch the CSL style once. Elsevier's Harvard style is the closest match to Remote Sensing of
Environment's author–year format:

    curl -L -o elsevier-harvard.csl \
      https://raw.githubusercontent.com/citation-style-language/styles/master/elsevier-harvard.csl

For the ISPRS fallback, substitute `elsevier-with-titles.csl`.

## Word-count check before building

The target is 8,000–9,500 words of main text, counted from the start of Section 1 to the end
of Section 7, excluding tables, captions and references.

    python - <<'PY'
    import re
    t = open("MANUSCRIPT.md").read()
    body = t.split("## 1. Introduction", 1)[1].split("## Figure captions")[0]
    body = re.sub(r"^\|.*$", "", body, flags=re.M)     # drop table rows
    print("main text words:", len(body.split()))
    abstract = t.split("## Abstract")[1].split("**Keywords")[0]
    print("abstract words:", len(abstract.split()))
    PY

## Citation check

Every key cited must exist in `references.bib`, and every entry in the bibliography should be
cited — a submission with dangling or orphan references is a desk-reject risk.

    python - <<'PY'
    import re
    t = open("MANUSCRIPT.md").read()
    cited = set(re.findall(r"@([A-Za-z0-9_]+)", t))
    bib = set(re.findall(r"@\w+\{([^,]+),", open("references.bib").read()))
    print("cited but missing:", sorted(cited - bib))
    print("in bib, never cited:", sorted(bib - cited))
    PY

## PDF

    pandoc MANUSCRIPT.md \
      --citeproc \
      --bibliography=references.bib \
      --csl=elsevier-harvard.csl \
      --pdf-engine=xelatex \
      -V geometry:margin=25mm \
      -V fontsize=11pt \
      -V linestretch=1.5 \
      -V colorlinks=true \
      --metadata link-citations=true \
      -o MANUSCRIPT.pdf

Line spacing of 1.5 and 25 mm margins approximate the double-spaced submission format most
Elsevier titles ask for; switch `linestretch` to 2 if the editor insists.

## DOCX, for co-authors who track changes

    pandoc MANUSCRIPT.md \
      --citeproc --bibliography=references.bib --csl=elsevier-harvard.csl \
      -o MANUSCRIPT.docx

## Supplementary file

    pandoc SUPPLEMENTARY.md --pdf-engine=xelatex -V geometry:margin=20mm \
      -o SUPPLEMENTARY.pdf

## Figures

Figures are already at submission specification and need no conversion: 300 dpi, 90 mm
(single column) or 190 mm (double column), all type at 7 pt or larger, maps carrying a
graticule, scale bar, north arrow and locator inset. `figstyle.check()` enforces all of that
at save time — it refuses to write a figure whose canvas is not a column width, whose dpi is
wrong, which contains type under 7 pt, or whose content extends past the canvas — and
`code/figure_list.py` re-checks the written files and regenerates `FIGURE_LIST.md`.

Note that figures are saved at exactly the canvas size, **not** with a tight bounding box. A
tight box crops the canvas, so the file would be narrower than the column it was drawn for and
the journal would scale it back up, changing every printed type size. To regenerate them from
source:

    OMP_NUM_THREADS=1 PYTHONPATH=code python code/fig_study_area.py   # Fig. 1
    OMP_NUM_THREADS=1 PYTHONPATH=code python code/fig_results.py f1 f2 f3 f4 f5 f7 f8
    OMP_NUM_THREADS=1 PYTHONPATH=code python code/fig_maps.py         # M1, M2
    OMP_NUM_THREADS=1 PYTHONPATH=code python code/fig_offset.py       # Fig. 7, needs Earth Engine
    python code/figure_list.py                                        # re-check, rewrite FIGURE_LIST.md

The function names inside `fig_results.py` (`f1` … `f8`) predate the renumbering and refer to
the figure's subject, not its number; each writes the correctly numbered file.

`OMP_NUM_THREADS=1` matters: the block bootstrap runs one process per core and multithreaded
BLAS inside each of them slows the whole thing by an order of magnitude.

Elsevier wants figures as separate files at submission, which they already are, named by their
figure number. If EPS is requested, `mogrify -format eps figures/*.png` is adequate for the
raster panels, but the map plates should then be regenerated with `savefig(..., format="pdf")`
to keep the vector annotation crisp.

## Regenerating the numbers

The manuscript prints re-derived values only. To rebuild them from the event tables:

    OMP_NUM_THREADS=1 PYTHONPATH=code python code/run_numbers.py <s1_2020_monthly.csv>
    python code/numbers_trace.py
    python code/supplementary.py

The run takes roughly twenty minutes on 32 cores, almost all of it in the 1,000-draw block
bootstraps of the logistic coefficient. `s1_2020_monthly.csv` is the monthly Sentinel-1 count
extraction produced by `code/extract_s1_2020.py`, which needs an authenticated Earth Engine
session.

## Bibliography

`references.bib` is generated, not hand-written:

    python code/bib_build.py     # resolves each DOI through doi.org content negotiation
    python code/bib_map.py       # writes LITERATURE_MAP.md from the resolved metadata

Adding a reference means adding one line to the `ENTRIES` table in `code/bib_build.py` — a
cluster number, a citation-key tag, a DOI and the role it plays in the argument — and re-running
both scripts. The key is rebuilt from the registered surname and year, so a key can never
disagree with the metadata it points at.

## Submission checklist

Title chosen from the three candidates in the manuscript comment, authors and acknowledgements
filled in, word count inside 8,000–9,500, abstract at or under 250 words, five highlights each
at or under 85 characters, graphical abstract drawn to the specification in `HIGHLIGHTS.md`,
figures as separate files, supplementary as one PDF, and the data-and-code statement pointing
at a public archive rather than at this working tree.
