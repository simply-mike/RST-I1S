from steiner_types import Node
from geometry import manhattan

# mst with prim's algo
def prim_mst(nodes: list[Node]) -> tuple[list[tuple[int, int]], int]:
    n = len(nodes)
    if n == 0:
        return [], 0
    if n == 1:
        return [], 0

    in_tree = [False] * n
    best_dist = [10**18] * n
    parent = [-1] * n

    best_dist[0] = 0
    total = 0
    edges: list[tuple[int, int]] = []

    for _ in range(n):
        u = -1
        u_dist = 10**18
        for i in range(n):
            if not in_tree[i] and best_dist[i] < u_dist:
                u = i
                u_dist = best_dist[i]

        if u == -1:
            raise RuntimeError("MST failed: graph appears disconnected")

        in_tree[u] = True
        total += 0 if parent[u] == -1 else best_dist[u]
        if parent[u] != -1:
            a, b = parent[u], u
            if a > b:
                a, b = b, a
            edges.append((a, b))

        for v in range(n):
            if in_tree[v] or v == u:
                continue
            d = manhattan(nodes[u], nodes[v])
            if d < best_dist[v]:
                best_dist[v] = d
                parent[v] = u

    return edges, total


def degrees_from_mst_edges(nodes: list[Node], mst_edges: list[tuple[int, int]]) -> dict[int, int]:
    deg = {node.id: 0 for node in nodes}
    for i, j in mst_edges:
        deg[nodes[i].id] += 1
        deg[nodes[j].id] += 1
    return deg