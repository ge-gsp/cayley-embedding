# Cayley Embedding Workbench

**Put a graph inside a Cayley graph of a finite abelian group — and find out what it costs.**

→ **[Open the workbench](https://ge-gsp.github.io/cayley-embedding/)** · runs entirely in your browser, nothing is uploaded

---

## Why this exists

Classical signal processing stands on a group. On the integers you can shift a
signal by `k`; on a grid you can shift it sideways. Translation gives you
convolution, a Fourier transform, filters, wavelets, sampling theorems — the
whole toolbox follows from the group.

A general graph has no such structure, and that is the central awkwardness of
graph signal processing. A *Cayley graph of a finite abelian group* does: its
vertices **are** the group elements, so "shift by `s`" means something exact,
the characters of the group give a genuine orthonormal Fourier basis, and the
classical constructions come back unchanged.

So the question becomes: can we place our graph inside one — and what do we
give up to get there?

## The three routes, and the trilemma

There is no single answer, because three different things can be preserved and
in general you cannot have all three.

| Route | What you do | What you pay | What it preserves |
|---|---|---|---|
| **Completion** `γ⁺` | Keep the same vertices; add edges until the graph *is* a Cayley graph | Edges added, as a fraction of edges present | Host stays at `n` vertices — the smallest possible |
| **Isometric** `ν` | Map the vertices into a larger Cayley graph, preserving **every distance** | Size of the host | The metric exactly — required for anything localised: wavelets, Gabor frames, vertex–frequency analysis |
| **Induced** `η` | Map into a larger Cayley graph preserving **adjacency and non-adjacency** | Size of the host, usually smaller than isometric | The combinatorics; distances may shrink |

Cheap host, exact metric, unchanged graph — pick two. The workbench's job is to
tell you which compromise your particular graph is cheapest in, and to say so
with certified bounds rather than a guess.

**And the question is never "is my graph already a Cayley graph?"** Of the 995
connected graphs on two to seven vertices, exactly **14** are Cayley graphs of
an abelian group — the cycles, the complete graphs, `K₃,₃`, the prism, the
octahedron and `C₇(1,2)`. Fourteen out of 995. Everything else has to choose a
route.

## What the workbench does

Paste an edge list or pick from the catalogue, and you get:

- **Linear-time screens** for all three routes — the degree bracket for `γ⁺`,
  the counting floor `η ≥ 2n − 2m/Δ`, the diameter floor for `ν`.
- **Exact `γ⁺` and `γ_△` up to eleven vertices.** Graphs on two to seven are
  looked up in the census below, recognised whatever labelling you typed. Beyond
  that the same exhaustive search runs live in your browser — every abelian
  group of order `n`, every labelling, every inverse-closed connection set —
  off the main thread, so the page stays responsive.
- **A recommendation with its reasoning shown**, which changes if you tell it
  you need distances preserved, or intend to localise, or intend to sample.
- **A circular drawing** of the graph, exportable as SVG.

A value is shown as exact only where both directions are certified; otherwise
you get a bracket. That convention is the point — the tool never implies more
than has been proved.

## The census

`data/` carries the full census: **995 connected graphs on two to seven
vertices with `γ⁺` and `γ_△` computed exactly**, by exhaustive search over
every abelian group of each order and every labelling.

| File | What it is |
|---|---|
| `census.csv` | One row per graph, with the degree data and the Theorem 2.8 bracket |
| `census.json` | The same, as records |
| `census.compact.json` | `graph6 → [n, m, γ⁺, γ_△]`, the form the workbench embeds |

Graphs are keyed by **canonical graph6** — the lexicographically least graph6
string over all `n!` labellings — so a lookup succeeds whatever labelling you
hold the graph in.

Two findings that fall straight out of the table: 14 of the 995 are abelian
Cayley graphs, and the Theorem 2.8 degree floor is **tight on 890 of 995**
(89.4%). The 105 graphs where it is not are the interesting ones.

## Running it

The workbench is a single self-contained HTML file with no build step, no
dependencies and no network calls. Download `index.html` and open it — it works
offline, including the exact search.

To rebuild the census from scratch (a few hours; needs `networkx`):

```bash
cd scripts
python3 census.py          # recomputes all 995 rows -> census_rows.json
python3 build_census.py    # joins graph6 keys -> ../data/
```

`scripts/census.py` is an independent recomputation, deliberately written
without reference to the implementation in the workbench; the JavaScript port
that runs in the browser is validated against all 995 of its rows before
release.

## Status and limits

Stated plainly, because the bounds are the product here:

- `γ⁺` and `γ_△` are **exact** to eleven vertices; beyond that you get the
  degree bracket only. The search is `(n−1)!` labellings, so twelve vertices is
  minutes and thirteen is out of reach by this method.
- `ν` and `η` are reported as **brackets**, not computed exactly. The closed
  forms for paths, stars and complete bipartite graphs are used where they
  apply. A live search for these is not implemented.
- The local order floor for `η` is NP-hard in `Δ` and is skipped above `Δ = 22`.
- Signal processing — translation, the graph Fourier transform, sampling — is
  **not** in this version. Embedding first; the signal processing that the
  embedding makes possible comes later.

## Citing

If this is useful, please cite the software and the dataset via the
`CITATION.cff` in this repository, or the archived release.

## Licence

Code is MIT. The census in `data/` is CC BY 4.0 — use it, including
commercially, with attribution.

## Authors

**Rigobert Fokam Souop** and **Laurent Bitjoka**
Laboratory of Energy, Signal, Imaging and Automation (LESIA),
National School of Agro-Industrial Sciences, University of Ngaoundéré, Cameroon.

Part of the GE-GSP framework — graph embeddings into abelian groups, and the
signal processing they make possible.
