"""Bounded Ilyra v690-v2 runner pair 09."""

from __future__ import annotations

import json
import sys

from ghc_family_obligation_graph_x2 import run

ALLOWED = ['obligation_reservation', 'provenance_path_digest']


def main() -> None:
    request = json.load(sys.stdin)
    if not isinstance(request, dict) or request.get("operation") not in ALLOWED:
        result = {"ok": False, "error": "operation_outside_runner_group", "original_success_credit": 0}
    else:
        result = run(request)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result.get("ok") else 2)


if __name__ == "__main__":
    main()
