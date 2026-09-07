import sys, json
import s2

QUERIES = json.load(open(sys.argv[1]))
out = []
for q in QUERIES:
    res = s2.search(q["q"], limit=q.get("n", 5), venue=q.get("venue"))
    print("###", q["q"], "| venue:", q.get("venue", "-"))
    for p in res:
        b = s2.brief(p)
        print(f"   {b['year']} | {(b['venue'] or '')[:42]:42s} | {b['doi']} | {b['title'][:78]}")
        out.append(dict(cluster=q.get("c"), **b))
json.dump(out, open(sys.argv[2], "w"), indent=1)
