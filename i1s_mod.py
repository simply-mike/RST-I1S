from steiner_types import Node, Edge
from geometry import hanan_candidates
from mst import prim_mst, degrees_from_mst_edges
from i1s_base import run_i1s_base


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
    base_nodes, _, _ = run_i1s_base(terminals)

    refined_nodes = _local_refine(base_nodes)
    refined_terminals, refined_steiners = _extract_steiners(refined_nodes)

    pruned_steiners = _prune_steiner_points(refined_terminals, refined_steiners)
    final_nodes = refined_terminals + pruned_steiners

    edges, total = _rebuild_edges(final_nodes)
    return final_nodes, edges, total