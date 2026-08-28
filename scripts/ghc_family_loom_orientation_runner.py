from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}
RUNNER_ID = "IF6738-RUNNER-002"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()
    try:
        row = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
        if row.get("owner") != "Ilyra Fen" or row.get("phase") != "v673-v8":
            raise ValueError("owner or phase mismatch")
        if row.get("external_actions") != 0:
            raise ValueError("external action prohibited")
        if row.get("outcome") not in ALLOWED:
            raise ValueError("outcome label rejected")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"passed": False, "runner": RUNNER_ID, "reason": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps({"passed": True, "runner": RUNNER_ID}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
