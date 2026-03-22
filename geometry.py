from steiner_types import Node


def manhattan(a: Node, b: Node) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def point_key(node: Node) -> tuple[int, int]:
    return (node.x, node.y)


def unique_xy(nodes: list[Node]) -> list[Node]:
    seen = set()
    result = []
    for node in nodes:
        key = (node.x, node.y)
        if key not in seen:
            seen.add(key)
            result.append(node)
    return result


def hanan_candidates(nodes: list[Node], next_id_start: int) -> list[Node]:
    xs = sorted({n.x for n in nodes})
    ys = sorted({n.y for n in nodes})
    existing = {(n.x, n.y) for n in nodes}

    candidates = []
    next_id = next_id_start
    for x in xs:
        for y in ys:
            if (x, y) in existing:
                continue
            candidates.append(Node(id=next_id, x=x, y=y, type="s"))
            next_id += 1
    return candidates