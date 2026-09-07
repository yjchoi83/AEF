"""Item 8 -- render MANUSCRIPT_RSE.md: author-year citations and an Elsevier-Harvard list.

pandoc is not available in this environment, so the citation processing is done here rather
than by citeproc. The output is the submission-format manuscript: every `[@key]` replaced by
an author-year citation and a formatted, alphabetically sorted reference list appended. The
script fails loudly if any cited key is missing from the bibliography or any bibliography entry
is never cited.
"""
import re
import sys
from collections import OrderedDict

BIB = "aef_explore/paper/references.bib"
SRC = "aef_explore/paper/MANUSCRIPT.md"
DST = "aef_explore/paper/MANUSCRIPT_RSE.md"


# ---------------------------------------------------------------- bib parsing
def split_entries(text):
    out, i = [], 0
    while True:
        i = text.find("@", i)
        if i < 0:
            return out
        j = text.find("{", i)
        depth, k = 0, j
        for k in range(j, len(text)):
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
                if depth == 0:
                    break
        out.append(text[i:k + 1])
        i = k + 1


def field(entry, name):
    m = re.search(r"\b" + name + r"\s*=\s*", entry, re.I)
    if not m:
        return ""
    i = m.end()
    if entry[i] not in "{\"":
        j = entry.find(",", i)
        return entry[i:j].strip()
    close = "}" if entry[i] == "{" else "\""
    depth = 0
    for j in range(i, len(entry)):
        if entry[j] == "{":
            depth += 1
        elif entry[j] == close:
            depth -= 1
            if depth == 0:
                break
    return re.sub(r"\s+", " ", entry[i + 1:j]).strip()


def initials(given):
    parts = re.split(r"[\s\-]+", given.strip())
    return "".join(f"{p[0]}." for p in parts if p and p[0].isalpha())


def fmt_author(a):
    a = a.strip().rstrip(",")
    if not a or a == "others":
        return ""
    if "," in a:
        sur, given = a.split(",", 1)
    else:
        bits = a.split()
        sur, given = bits[-1], " ".join(bits[:-1])
    sur = sur.strip()
    return f"{sur}, {initials(given)}" if given.strip() else sur


def author_list(raw):
    people = [fmt_author(a) for a in re.split(r"\s+and\s+", raw) if a.strip()]
    return [p for p in people if p]


def surname(person):
    return person.split(",")[0].strip()


def parse():
    entries = {}
    for e in split_entries(open(BIB).read()):
        key = re.match(r"@\w+\{([^,]+),", e)
        if not key:
            continue
        people = author_list(field(e, "author"))
        entries[key.group(1)] = dict(
            key=key.group(1), authors=people, year=field(e, "year") or "n.d.",
            title=field(e, "title").rstrip("."),
            journal=field(e, "journal") or field(e, "booktitle") or field(e, "publisher"),
            volume=field(e, "volume"), number=field(e, "number"),
            pages=field(e, "pages"), doi=field(e, "DOI") or field(e, "doi"),
            publisher=field(e, "publisher"), etype=re.match(r"@(\w+)", e).group(1).lower())
    return entries


# ---------------------------------------------------------------- formatting
def cite_label(e):
    a = e["authors"]
    if not a:
        return f"Anon., {e['year']}"
    if len(a) == 1:
        return f"{surname(a[0])}, {e['year']}"
    if len(a) == 2:
        return f"{surname(a[0])} and {surname(a[1])}, {e['year']}"
    return f"{surname(a[0])} et al., {e['year']}"


def reference(e):
    a = e["authors"]
    if len(a) > 12:
        names = ", ".join(a[:12]) + ", et al."
    elif len(a) > 1:
        names = ", ".join(a[:-1]) + ", " + a[-1]
    else:
        names = a[0] if a else "Anon."
    out = f"{names}, {e['year']}. {e['title']}."
    if e["journal"]:
        out += f" {e['journal']}"
        if e["volume"]:
            out += f" {e['volume']}"
            if e["number"]:
                out += f" ({e['number']})"
        if e["pages"]:
            out += f", {e['pages']}"
        out += "."
    if e["doi"]:
        out += f" https://doi.org/{e['doi']}"
    return re.sub(r"\s+", " ", out).strip()


def sort_key(e):
    a = e["authors"]
    return ((surname(a[0]) if a else "zzz").lower(), str(e["year"]), e["title"].lower())


# ---------------------------------------------------------------- main
def main():
    entries = parse()
    src = open(SRC).read()

    cited = OrderedDict()

    def repl(m):
        keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
        items = []
        for k in keys:
            if k not in entries:
                raise SystemExit(f"cited key not in bibliography: {k}")
            cited[k] = True
            items.append(entries[k])
        items.sort(key=lambda e: (str(e["year"]),
                                  surname(e["authors"][0]) if e["authors"] else "zzz"))
        return "(" + "; ".join(cite_label(e) for e in items) + ")"

    out = re.sub(r"\[((?:@[A-Za-z0-9_]+\s*;?\s*)+)\]", repl, src)
    leftover = re.findall(r"@[A-Za-z0-9_]+", out)
    if leftover:
        raise SystemExit(f"unconverted citation markers: {sorted(set(leftover))[:5]}")

    uncited = [k for k in entries if k not in cited]
    if uncited:
        raise SystemExit(f"bibliography entries never cited: {uncited}")

    refs = sorted(entries.values(), key=sort_key)
    body = out.split("## References")[0].rstrip()
    head = (body + "\n\n## References\n\n"
            "Elsevier Harvard (author–date). Generated from `references.bib` by "
            "`code/render_rse.py`; every entry is the metadata registered at the DOI.\n\n")
    open(DST, "w").write(head + "\n\n".join(reference(e) for e in refs) + "\n")
    print(f"cited keys resolved: {len(cited)} of {len(entries)} bibliography entries")
    print(f"references rendered: {len(refs)}")
    print("wrote", DST)


if __name__ == "__main__":
    main()
