# Rectilinear Steiner Minimal Tree - I1S heuristic

## Description

This program constructs a **rectilinear Steiner minimal tree (SMT)** for a given set of terminal points using the Manhattan distance:

L = |x_1 - x_2| + |y_1 - y_2|

The solution is based on the **Iterated 1-Steiner (I1S)** heuristic.

---

## Usage

```bash
python main.py input.json
python main.py -m input.json
```

* without `-m`: base algorithm
* with `-m`: modified algorithm

The output is written to:

```
<input_name>_out.json
```

---

## Algorithm

### Base Algorithm (I1S)

1. Initialization:

   * input set of terminals P
   * Steiner set S = ∅

2. Hanan grid construction:

   * collect all unique x and y coordinates
   * generate candidate Steiner points

3. Candidate evaluation:

   * for each candidate x, compute the gain:
     Δ = L(MST(P ∪ S)) − L(MST(P ∪ S ∪ {x}))

4. Point insertion:

   * select the candidate with maximum Δ > 0
   * add it to S

5. Pruning:

   * build MST over P ∪ S
   * remove all Steiner points with degree < 3

6. Iteration:

   * repeat until no improving candidate exists

7. Final result:

   * MST over P ∪ S


### Modified Algorithm

The modified version is quality-oriented.

Instead of selecting the next Steiner point only by immediate gain, it uses
a two-step look-ahead strategy:

1. evaluate candidate Steiner points by their immediate gain;
2. keep the best candidates;
3. for each such candidate, estimate the best possible gain on the next step;
4. choose the first point according to the combined two-step gain.

After the Steiner set is constructed, an additional local refinement step is applied:
- each Steiner point is tested at alternative Hanan-grid positions;
- a move is accepted if it reduces the total tree length.

Finally, Steiner points with degree < 3 are removed and the final MST is rebuilt.

---

## Notes

* The SMT problem is NP-complete
* The I1S algorithm is heuristic
* Global optimality is not guaranteed

---
