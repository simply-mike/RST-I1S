from collections import deque

from steiner_types import Node, Edge


def validate_solution(nodes: list[Node], edges: list[Edge]) -> None:
    if any(not isinstance(n.x, int) or not isinstance(n.y, int) for n in nodes):
        raise ValueError("All coordinates must be integers")

    if len(edges) != len(nodes) - 1:
        raise ValueError(f"Invalid tree: expected {len(nodes)-1} edges, got {len(edges)}")

    id_to_node = {n.id: n for n in nodes}
    adj = {n.id: [] for n in nodes}
    deg = {n.id: 0 for n in nodes}

    for e in edges:
        if e.u not in id_to_node or e.v not in id_to_node:
            raise ValueError("Edge references unknown node id")
        if e.u == e.v:
            raise ValueError("Self-loop detected")

        adj[e.u].append(e.v)
        adj[e.v].append(e.u)
        deg[e.u] += 1
        deg[e.v] += 1

    # connectedness
    start = nodes[0].id
    q = deque([start])
    seen = {start}
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)

    if len(seen) != len(nodes):
        raise ValueError("Graph is not connected")

    # Steiner degree >= 3
    for n in nodes:
        if n.type == "s" and deg[n.id] < 3:
            raise ValueError(f"Steiner point id={n.id} has degree {deg[n.id]} < 3")