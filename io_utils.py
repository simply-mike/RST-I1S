import json
from pathlib import Path

from steiner_types import Node, Edge


def load_terminals(path: Path) -> list[Node]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("node", [])
    terminals = []

    for item in nodes:
        if item.get("type") != "t":
            continue
        terminals.append(
            Node(
                id=int(item["id"]),
                x=int(item["x"]),
                y=int(item["y"]),
                type="t",
            )
        )

    if not terminals:
        raise ValueError("No terminal nodes found in input JSON")

    return terminals


def make_output_path(input_path: Path) -> Path:
    stem = input_path.stem
    return Path.cwd() / f"{stem}_out.json"


def save_output_json(path: Path, nodes: list[Node], edges: list[Edge]) -> None:
    incident: dict[int, list[int]] = {node.id: [] for node in nodes}
    for edge in edges:
        incident[edge.u].append(edge.id)
        incident[edge.v].append(edge.id)

    node_items = []
    for node in sorted(nodes, key=lambda n: n.id):
        node_items.append(
            {
                "id": node.id,
                "x": node.x,
                "y": node.y,
                "type": node.type,
                "edges": sorted(incident[node.id]),
            }
        )

    edge_items = []
    for edge in sorted(edges, key=lambda e: e.id):
        edge_items.append(
            {
                "id": edge.id,
                "vertices": [edge.u, edge.v],
            }
        )

    out = {
        "node": node_items,
        "edge": edge_items,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)