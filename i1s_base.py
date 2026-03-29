from steiner_types import Node, Edge
from geometry import hanan_candidates
from mst import prim_mst, degrees_from_mst_edges


def _next_node_id(nodes: list[Node]) -> int:
    return max(n.id for n in nodes) + 1 if nodes else 1


def _build_final_edges(nodes: list[Node], mst_edges_idx: list[tuple[int, int]]) -> list[Edge]:
    edges = []
    next_edge_id = 1
    for i, j in mst_edges_idx:
        u = nodes[i].id
        v = nodes[j].id
        if u > v:
            u, v = v, u
        edges.append(Edge(id=next_edge_id, u=u, v=v))
        next_edge_id += 1
    return edges


def _prune_steiner_points(terminals: list[Node], steiners: list[Node]) -> list[Node]:
    changed = True
    current = steiners[:]

    while changed:
        changed = False
        nodes = terminals + current
        mst_edges, _ = prim_mst(nodes)
        deg = degrees_from_mst_edges(nodes, mst_edges)

        filtered = []
        for s in current:
            if deg.get(s.id, 0) >= 3:
                filtered.append(s)
            else:
                changed = True
        current = filtered

    return current


def _best_candidate(terminals: list[Node], steiners: list[Node]) -> tuple[Node | None, int]:
    current_nodes = terminals + steiners
    _, current_len = prim_mst(current_nodes)

    candidates = hanan_candidates(current_nodes, _next_node_id(current_nodes))
    if not candidates:
        return None, 0

    best = None
    best_gain = 0

    for cand in candidates:
        trial_nodes = current_nodes + [cand]
        _, trial_len = prim_mst(trial_nodes)
        gain = current_len - trial_len

        if gain > best_gain:
            best = cand
            best_gain = gain
        elif gain == best_gain and gain > 0 and best is not None:
            # deterministic tie-break
            if (cand.x, cand.y, cand.id) < (best.x, best.y, best.id):
                best = cand

    return best, best_gain


def run_i1s_base(terminals: list[Node]) -> tuple[list[Node], list[Edge], int]:
    steiners: list[Node] = []

    while True:
        best, gain = _best_candidate(terminals, steiners)
        if best is None or gain <= 0:
            break

        steiners.append(best)
        steiners = _prune_steiner_points(terminals, steiners)

    final_nodes = terminals + steiners
    mst_edges_idx, total_length = prim_mst(final_nodes)
    final_edges = _build_final_edges(final_nodes, mst_edges_idx)
    return final_nodes, final_edges, total_length