"""Public bounded runner for ghc-family-obligation-graph-reachability."""

from __future__ import annotations

import json
import sys

from ghc_family_obligation_graph_core_x1 import run as run_x1
from ghc_family_obligation_graph_core_x2 import run as run_x2

ALLOWED = ['transitive_reduction', 'critical_path']


def main() -> None:
    request = json.load(sys.stdin)
    if not isinstance(request, dict) or request.get("operation") not in ALLOWED:
        result = {"ok": False, "error": "operation_outside_runner_group", "original_success_credit": 0}
    else:
        result = run_x2(request)
        if result.get("error") == "unknown_operation":
            result = run_x1(request)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result.get("ok") else 2)


if __name__ == "__main__":
    main()
