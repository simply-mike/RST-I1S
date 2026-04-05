import argparse
import time
from pathlib import Path

from io_utils import load_terminals, save_output_json, make_output_path
from i1s_base import run_i1s_base
from i1s_mod import run_i1s_modified
from validate import validate_solution


def parse_args():
    parser = argparse.ArgumentParser(description="Rectilinear Steiner Tree, I1S heuristic")
    parser.add_argument("input_json", help="Path to input json file")
    parser.add_argument("-m", "--modified", action="store_true", help="Use modified algorithm")
    return parser.parse_args()


def main():
    args = parse_args()

    input_path = Path(args.input_json)
    terminals = load_terminals(input_path)

    t0 = time.perf_counter()
    if args.modified:
        nodes, edges, total_length = run_i1s_modified(terminals)
    else:
        nodes, edges, total_length = run_i1s_base(terminals)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    validate_solution(nodes, edges)

    output_path = make_output_path(input_path)
    save_output_json(output_path, nodes, edges)

    mode = "modified" if args.modified else "base"
    print(f"mode={mode}")
    print(f"nodes={len(nodes)} edges={len(edges)}")
    print(f"length={total_length}")
    print(f"time_ms={elapsed_ms:.3f}")
    print(f"output={output_path}")


if __name__ == "__main__":
    main()