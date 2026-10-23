# The completion census

All **995 connected graphs on two to seven vertices**, with the Cayley
completion costs computed exactly.

Source: exhaustive search over every abelian group of order *n*, every
labelling of the vertices by group elements, and every inverse-closed
connection set giving a connected host. Produced by `scripts/census.py`, an
implementation written independently of the one that runs in the workbench;
the browser port is validated against all 995 rows.

## Files

| File | Format |
|---|---|
| `census.csv` | one row per graph, all columns below |
| `census.json` | the same records as JSON |
| `census.compact.json` | `graph6 -> [n, m, gamma_plus, gamma_triangle]` |

## Columns

| Column | Meaning |
|---|---|
| `graph6` | canonical graph6: the lexicographically least graph6 string over all `n!` labellings. Key on this and a lookup succeeds whatever labelling you hold the graph in. |
| `n`, `m` | vertices, edges |
| `delta_max`, `delta_min` | maximum and minimum degree |
| `delta_star` | least `d >= delta_max` with `n*d` even — the least feasible host degree |
| `gamma_plus` | **completion cost**: minimum edges added to make the graph a Cayley graph of an abelian group on the same vertex set, divided by `m`. Zero exactly when the graph already is one. |
| `gamma_triangle` | **edit cost**: as above but paying for removals too — minimum symmetric difference, divided by `m` |
| `bound_lo`, `bound_hi` | the degree bracket of Theorem 2.8: `max(0, n*delta_star/(2m) - 1)` and `n(n-1)/(2m) - 1` |
| `is_cayley` | 1 when `gamma_plus = 0` |
| `bound_tight` | 1 when `bound_lo` equals `gamma_plus` — true for 890 of the 995 |

Values are rounded to six decimal places. Compare with a tolerance of about
`2e-6` rather than exact equality.

## Counts

| | |
|---|---|
| graphs | 995 |
| by `n` | 1, 2, 6, 21, 112, 853 for n = 2..7 |
| abelian Cayley graphs (`gamma_plus = 0`) | 14 |
| degree floor tight | 890 |

The 14: the cycles `C_2..C_7`, the complete graphs `K_2..K_7`, `K_{3,3}`, the
triangular prism, the octahedron `K_{2,2,2}`, and the circulant `C_7(1,2)`.

## Licence

CC BY 4.0. Please cite via the repository's `CITATION.cff`.
