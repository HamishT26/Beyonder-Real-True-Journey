"""Family-current bounded phonograph-cylinder record runner bank for Caelen Morrow v682-v5."""

from __future__ import annotations

import json
from typing import Any


def run_contract(runner_index: int, fixture_kind: str) -> dict[str, Any]:
    if runner_index < 1 or runner_index > 10:
        raise ValueError("runner index must be 1..10")
    if fixture_kind not in {"positive", "invalid"}:
        raise ValueError("fixture kind must be positive or invalid")
    fixture = {
        "synthetic": True,
        "real_row_count": 0,
        "observation_status": "absent",
        "authority_status": "reserved",
        "boundary": "owner_local_zero_row_only",
    }
    if fixture_kind == "invalid":
        fixture["authority_status"] = "granted_by_runner"
    reasons: list[str] = []
    if fixture["synthetic"] is not True:
        reasons.append("synthetic_boundary_missing")
    if fixture["real_row_count"] != 0:
        reasons.append("real_rows_forbidden")
    if fixture["observation_status"] != "absent":
        reasons.append("observation_promotion_forbidden")
    if fixture["authority_status"] != "reserved":
        reasons.append("authority_promotion_forbidden")
    if fixture["boundary"] != "owner_local_zero_row_only":
        reasons.append("boundary_mismatch")
    return {
        "accepted": not reasons,
        "fixture_kind": fixture_kind,
        "reasons": reasons,
        "runner": f"ghc_family_cylinder_archive_runner_{runner_index:02d}.py",
        "scope": "bounded_synthetic_structure_only",
    }


def main(runner_index: int) -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", choices=("positive", "invalid"), required=True)
    args = parser.parse_args()
    result = run_contract(runner_index, args.fixture)
    print(json.dumps(result, separators=(",", ":")))
    expected = (
        result["accepted"] if args.fixture == "positive" else not result["accepted"]
    )
    return 0 if expected else 1
