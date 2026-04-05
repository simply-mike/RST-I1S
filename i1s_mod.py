from steiner_types import Node, Edge
from geometry import hanan_candidates
from mst import prim_mst, degrees_from_mst_edges
from i1s_base import run_i1s_base


def _next_node_id(nodes: list[Node]) -> int:
    return max(n.id for n in nodes) + 1 if nodes else 1


def _total_len(nodes: list[Node]) -> int:
    _, total = prim_mst(nodes)
    return total


def _extract_steiners(nodes: list[Node]) -> tuple[list[Node], list[Node]]:
    terminals = [n for n in nodes if n.type == "t"]
    steiners = [n for n in nodes if n.type == "s"]
    return terminals, steiners


def _rebuild_edges(nodes: list[Node]) -> tuple[list[Edge], int]:
    mst_edges_idx, total = prim_mst(nodes)
    edges = []
    next_edge_id = 1
    for i, j in mst_edges_idx:
        u = nodes[i].id
        v = nodes[j].id
        if u > v:
            u, v = v, u
        edges.append(Edge(id=next_edge_id, u=u, v=v))
        next_edge_id += 1
    return edges, total


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


def _evaluate_candidates(terminals: list[Node], steiners: list[Node]) -> list[tuple[int, Node, int]]:
    current_nodes = terminals + steiners
    _, current_len = prim_mst(current_nodes)

    candidates = hanan_candidates(current_nodes, _next_node_id(current_nodes))
    scored = []

    for cand in candidates:
        trial_nodes = current_nodes + [cand]
        _, trial_len = prim_mst(trial_nodes)
        gain = current_len - trial_len
        scored.append((gain, cand, trial_len))

    scored.sort(key=lambda t: (-t[0], t[1].x, t[1].y, t[1].id))
    return scored


def _best_candidate_lookahead(
    terminals: list[Node],
    steiners: list[Node],
    top_k: int = 5,
) -> tuple[Node | None, int]:
    scored = _evaluate_candidates(terminals, steiners)
    if not scored:
        return None, 0

    top = [item for item in scored if item[0] > 0][:top_k]
    if not top:
        return None, 0

    best_first = None
    best_first_gain = 0
    best_total_gain = -1

    for first_gain, first_cand, _ in top:
        trial_steiners = steiners + [first_cand]
        trial_steiners = _prune_steiner_points(terminals, trial_steiners)

        second_scored = _evaluate_candidates(terminals, trial_steiners)
        second_gain = 0
        for g, _, _ in second_scored:
            if g > second_gain:
                second_gain = g

        total_gain = first_gain + second_gain

        if total_gain > best_total_gain:
            best_total_gain = total_gain
            best_first = first_cand
            best_first_gain = first_gain
        elif total_gain == best_total_gain and best_first is not None:
            if (first_gain > best_first_gain) or (
                first_gain == best_first_gain and
                (first_cand.x, first_cand.y, first_cand.id) <
                (best_first.x, best_first.y, best_first.id)
            ):
                best_first = first_cand
                best_first_gain = first_gain

    return best_first, best_first_gain


def _local_refine(nodes: list[Node]) -> list[Node]:
    terminals, steiners = _extract_steiners(nodes)
    if not steiners:
        return nodes

    improved = True
    current_nodes = nodes[:]
    current_best = _total_len(current_nodes)

    while improved:
        improved = False
        terminals, steiners = _extract_steiners(current_nodes)

        for idx, s in enumerate(steiners):
            others = terminals + steiners[:idx] + steiners[idx + 1 :]
            candidates = hanan_candidates(others, s.id)

            best_node = s
            best_len = current_best

            for cand in candidates:
                moved = Node(id=s.id, x=cand.x, y=cand.y, type="s")
                trial_nodes = terminals + steiners[:idx] + [moved] + steiners[idx + 1 :]
                trial_len = _total_len(trial_nodes)

                if trial_len < best_len:
                    best_len = trial_len
                    best_node = moved

            if best_node != s:
                steiners[idx] = best_node
                current_nodes = terminals + steiners
                current_best = best_len
                improved = True

    return current_nodes


def run_i1s_modified(terminals: list[Node]) -> tuple[list[Node], list[Edge], int]:
    steiners: list[Node] = []

    while True:
        best, gain = _best_candidate_lookahead(terminals, steiners, top_k=5)
        if best is None or gain <= 0:
            break

        steiners.append(best)
        steiners = _prune_steiner_points(terminals, steiners)

    nodes_after_lookahead = terminals + steiners
    refined_nodes = _local_refine(nodes_after_lookahead)

    refined_terminals, refined_steiners = _extract_steiners(refined_nodes)
    refined_steiners = _prune_steiner_points(refined_terminals, refined_steiners)

    final_nodes = refined_terminals + refined_steiners
    edges, total = _rebuild_edges(final_nodes)
    return final_nodes, edges, total