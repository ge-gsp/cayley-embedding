"""Build the published census dataset.

census.py iterates networkx's graph_atlas_g() filtered to 2 <= n <= 7 and
connected, in that order, so the i-th computed row is the i-th such graph.
Identity is recovered by replaying that iteration and checked on (n, m).

Each graph is keyed by its canonical graph6: the lexicographically least
graph6 string over all n! labellings, computed on adjacency bitmasks.
"""
import csv, json, itertools, os, networkx as nx
from networkx.generators.atlas import graph_atlas_g

OUT = os.path.join(os.path.dirname(__file__), '..', 'data')


def g6_from_bits(n, bits):
    out = [chr(n + 63)]
    for k in range(0, len(bits), 6):
        chunk = bits[k:k + 6] + [0] * max(0, 6 - len(bits[k:k + 6]))
        v = 0
        for b in chunk:
            v = (v << 1) | b
        out.append(chr(v + 63))
    return "".join(out)


def canon(n, edges):
    adjm = [0] * n
    for u, v in edges:
        adjm[u] |= 1 << v
        adjm[v] |= 1 << u
    best = None
    for p in itertools.permutations(range(n)):
        inv = [0] * n
        for i, q in enumerate(p):
            inv[q] = i
        bits = []
        for j in range(1, n):
            aj = adjm[inv[j]]
            for i in range(j):
                bits.append((aj >> inv[i]) & 1)
        s = g6_from_bits(n, bits)
        if best is None or s < best:
            best = s
    return best


rows = json.load(open(os.path.join(os.path.dirname(__file__), 'census_rows.json')))
graphs = [G for G in graph_atlas_g()
          if 2 <= G.number_of_nodes() <= 7 and nx.is_connected(G)]
assert len(graphs) == len(rows) == 995, (len(graphs), len(rows))

recs, compact, bad = [], {}, 0
for G, r in zip(graphs, rows):
    Gc = nx.convert_node_labels_to_integers(G)
    n, m = Gc.number_of_nodes(), Gc.number_of_edges()
    if n != r['n'] or m != r['m']:
        bad += 1
        continue
    deg = [d for _, d in Gc.degree()]
    D, dmin = max(deg), min(deg)
    Dstar = D if (n * D) % 2 == 0 else D + 1       # least d >= D with nd even
    key = canon(n, list(Gc.edges()))
    gp, gt = round(r['gp'], 6), round(r['gt'], 6)
    recs.append(dict(
        graph6=key, n=n, m=m, delta_max=D, delta_min=dmin, delta_star=Dstar,
        gamma_plus=gp, gamma_triangle=gt,
        bound_lo=round(max(0.0, n * Dstar / (2 * m) - 1), 6),
        bound_hi=round(n * (n - 1) / (2 * m) - 1, 6),
        is_cayley=int(gp == 0.0),
        bound_tight=int(abs(max(0.0, n * Dstar / (2 * m) - 1) - gp) < 2e-6)))
    compact[key] = [n, m, gp, gt]

assert bad == 0, f"{bad} (n,m) join mismatches"
assert len(compact) == 995, f"{len(compact)} distinct canonical keys"

recs.sort(key=lambda d: (d['n'], d['m'], d['graph6']))
fields = list(recs[0].keys())
with open(os.path.join(OUT, 'census.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(recs)
json.dump(recs, open(os.path.join(OUT, 'census.json'), 'w'), indent=1)
json.dump(compact, open(os.path.join(OUT, 'census.compact.json'), 'w'),
          separators=(',', ':'))

print(f"rows                 : {len(recs)}")
print(f"abelian Cayley graphs: {sum(r['is_cayley'] for r in recs)}")
print(f"Thm 2.8 floor tight  : {sum(r['bound_tight'] for r in recs)}")
for nm in ('census.csv', 'census.json', 'census.compact.json'):
    print(f"  {nm:22s} {os.path.getsize(os.path.join(OUT, nm)):>8d} bytes")
