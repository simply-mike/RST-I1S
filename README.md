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

1. each Steiner point is tested at alternative Hanan-grid positions
2. a move is accepted if it reduces the total tree length

Finally:

1. remove Steiner points with degree < 3
2. rebuild the final MST

---

## Experimental Results

The algorithms were evaluated on a set of benchmark test cases.

| Test | Base Length | Modified Length | Gain | Base Time (ms) | Modified Time (ms) |
| ---- | ----------- | --------------- | ---- | -------------- | ------------------ |
| 0005 | 179         | 179             | 0    | 0.277          | 1.082              |
| 0006 | 179         | 179             | 0    | 0.587          | 2.080              |
| 0007 | 204         | 202             | 2    | 2.484          | 14.325             |
| 0008 | 202         | 202             | 0    | 2.046          | 9.246              |
| 0009 | 227         | 220             | 7    | 4.963          | 32.053             |
| 0010 | 267         | 267             | 0    | 8.561          | 45.918             |
| 0011 | 246         | 246             | 0    | 14.585         | 72.855             |
| 0012 | 274         | 274             | 0    | 19.712         | 105.125            |
| 0013 | 209         | 209             | 0    | 25.984         | 146.970            |
| 0014 | 297         | 296             | 1    | 19.279         | 126.776            |
| 0015 | 293         | 293             | 0    | 49.942         | 275.813            |
| 0016 | 261         | 261             | 0    | 46.634         | 244.650            |
| 0017 | 341         | 341             | 0    | 107.927        | 618.001            |
| 0018 | 337         | 337             | 0    | 123.052        | 718.888            |
| 0019 | 304         | 300             | 4    | 85.829         | 664.411            |
| 0020 | 332         | 332             | 0    | 110.556        | 633.748            |
| 0021 | 352         | 352             | 0    | 240.313        | 1365.260           |
| 0022 | 345         | 345             | 0    | 351.328        | 2195.130           |
| 0023 | 397         | 397             | 0    | 319.340        | 1946.737           |
| 0024 | 355         | 355             | 0    | 347.044        | 1980.560           |
| 0025 | 397         | 397             | 0    | 582.024        | 3459.632           |
| 0026 | 389         | 389             | 0    | 332.000        | 2112.320           |
| 0027 | 392         | 392             | 0    | 616.757        | 3708.742           |
| 0028 | 409         | 407             | 2    | 448.066        | 2950.477           |
| 0029 | 366         | 366             | 0    | 964.785        | 6424.124           |
| 0030 | 432         | 432             | 0    | 1237.358       | 7899.764           |

### Summary
1. The modified algorithm improves solution quality on a subset of test cases.
2. Maximum observed improvement: 7 units (test 0009).
3. Most cases show identical results, indicating that the base I1S already reaches a strong local optimum.
4. The modified algorithm consistently increases runtime due to additional look-ahead and refinement steps.