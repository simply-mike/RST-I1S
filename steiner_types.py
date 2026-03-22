from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    id: int
    x: int
    y: int
    type: str  # "t" / "s"


@dataclass(frozen=True)
class Edge:
    id: int
    u: int
    v: int