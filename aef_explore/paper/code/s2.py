"""Semantic Scholar client for the P6 bibliography: cached, rate-limited, backing off.

The API key is read from $S2_API_KEY and sent as `x-api-key`; it is never written to the
cache or to any committed file.  Responses are cached under `aef_explore/paper/cache/` keyed
by a hash of the request path, so re-runs cost nothing and the bibliography is reproducible.
"""
import hashlib, json, os, sys, time
import urllib.parse, urllib.request

BASE = "https://api.semanticscholar.org/graph/v1"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cache")
FIELDS = ("title,year,venue,publicationVenue,externalIds,authors,citationCount,"
          "publicationTypes,abstract,openAccessPdf,journal")
_last = [0.0]


def _get(path, tries=6):
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha1(path.encode()).hexdigest()[:24]
    fp = os.path.join(CACHE, key + ".json")
    if os.path.exists(fp):
        return json.load(open(fp))
    for attempt in range(tries):
        wait = 1.1 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(BASE + path,
                                     headers={"x-api-key": os.environ["S2_API_KEY"]})
        _last[0] = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.load(r)
            json.dump(data, open(fp, "w"))
            return data
        except Exception as e:
            code = getattr(e, "code", None)
            if attempt == tries - 1:
                return {"error": repr(e)[:200]}
            time.sleep((2 ** attempt) * (3 if code == 429 else 1))
    return {}


def search(query, limit=10, venue=None, year=None):
    q = {"query": query, "limit": limit, "fields": FIELDS}
    if venue:
        q["venue"] = venue
    if year:
        q["year"] = year
    return _get("/paper/search?" + urllib.parse.urlencode(q)).get("data", []) or []


def by_id(pid):
    return _get(f"/paper/{urllib.parse.quote(pid, safe='')}?fields={FIELDS}")


def brief(p):
    ids = p.get("externalIds") or {}
    return dict(title=p.get("title"), year=p.get("year"), venue=p.get("venue"),
                doi=ids.get("DOI"), arxiv=ids.get("ArXiv"), corpus=p.get("paperId"),
                n_cit=p.get("citationCount"),
                authors=[a.get("name") for a in (p.get("authors") or [])][:12])


if __name__ == "__main__":
    for p in search(sys.argv[1], limit=int(sys.argv[2]) if len(sys.argv) > 2 else 5,
                    venue=sys.argv[3] if len(sys.argv) > 3 else None):
        b = brief(p)
        print(f"{b['year']} | {b['venue']} | {b['doi']} | {b['title'][:90]}")
