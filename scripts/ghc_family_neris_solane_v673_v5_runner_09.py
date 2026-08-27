"""Family-current bounded runner 09 for Neris Solane v673-v5."""

from __future__ import annotations

import argparse
import json

from ghc_family_neris_solane_v673_v5_authority_gate import evaluate
from ghc_family_neris_solane_v673_v5_relation_graph import transition
from ghc_family_neris_solane_v673_v5_tide_gauge_record import (
    synthetic_record,
    validate_record,
)

RUNNER_NAME = "ghc_family_tide_gauge_gmut_symbolic"


def smoke() -> dict[str, object]:
    record = validate_record(synthetic_record("tg-syn-009"))
    move = transition("planned", "represented")
    gate = evaluate("validate_schema")
    return {
        "runner": RUNNER_NAME,
        "valid": bool(record["valid"] and move["accepted"] and gate["permitted"]),
        "synthetic": True,
        "real_rows": 0,
        "network_calls": 0,
        "global_install": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if not args.smoke:
        raise SystemExit("runner is fail-closed; use --smoke for the bounded owner-local witness")
    print(json.dumps(smoke(), sort_keys=True))


if __name__ == "__main__":
    main()
