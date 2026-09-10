"""Dispatch Ilyra v690-v2 obligation-graph requests."""

from __future__ import annotations

import json
import sys

from ghc_family_obligation_graph_x1 import run as run_x1
from ghc_family_obligation_graph_x2 import run as run_x2


def main() -> None:
    request = json.load(sys.stdin)
    result = run_x2(request)
    if result.get("error") == "unknown_operation":
        result = run_x1(request)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result.get("ok") else 2)


if __name__ == "__main__":
    main()
