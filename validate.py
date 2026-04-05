from collections import deque

from steiner_types import Node, Edge


def validate_solution(nodes: list[Node], edges: list[Edge]) -> None:
    if not nodes:
        raise ValueError("Node list is empty")

    # coordinates must be integers
    if any(not isinstance(n.x, int) or not isinstance(n.y, int) for n in nodes):
        raise ValueError("All coordinates must be integers")

    # node ids must be unique
    node_ids = [n.id for n in nodes]
    if len(node_ids) != len(set(node_ids)):
        raise ValueError("Duplicate node ids detected")

    # edge ids must be unique
    edge_ids = [e.id for e in edges]
    if len(edge_ids) != len(set(edge_ids)):
        raise ValueError("Duplicate edge ids detected")

    # node type must be valid
    for n in nodes:
        if n.type not in {"t", "s"}:
            raise ValueError(f"Invalid node type for id={n.id}: {n.type}")

    # tree edge count
    if len(edges) != len(nodes) - 1:
        raise ValueError(f"Invalid tree: expected {len(nodes)-1} edges, got {len(edges)}")

    id_to_node = {n.id: n for n in nodes}
    adj = {n.id: [] for n in nodes}
    deg = {n.id: 0 for n in nodes}

    seen_edges = set()

    for e in edges:
        if e.u not in id_to_node or e.v not in id_to_node:
            raise ValueError("Edge references unknown node id")

        if e.u == e.v:
            raise ValueError("Self-loop detected")

        uv = tuple(sorted((e.u, e.v)))
        if uv in seen_edges:
            raise ValueError(f"Duplicate edge detected: {uv}")
        seen_edges.add(uv)

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