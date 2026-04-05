# Rectilinear Steiner Minimal Tree - I1S Heuristic

## Description

This program constructs a **rectilinear Steiner minimal tree (SMT)** for a given set of terminal points using the Manhattan distance:

L = |x1 - x2| + |y1 - y2|

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

## Modified Algorithm

The modified version is quality-oriented.

Instead of selecting the next Steiner point only by immediate gain, it uses
a two-step look-ahead strategy:

1. evaluate candidate Steiner points by their immediate gain
2. keep the best candidates
3. for each candidate, estimate the best possible gain on the next step
4. choose the first point using the combined two-step gain

After the Steiner set is constructed, an additional local refinement step is applied:

* each Steiner point is tested at alternative Hanan-grid positions
* a move is accepted if it reduces the total tree length

Finally:

* remove Steiner points with degree < 3
* rebuild the final MST