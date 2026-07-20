#!/usr/bin/env python3
"""Bounded runtime for Ilyra Fen v650-v2 proposal contracts."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


REQUIRED = {
    "proposal_id",
    "bounded",
    "protected_gates",
    "required_obligations",
    "production",
    "authority_credit",
    "stage20",
    "real_rows",
    "real_people",
}


def evaluate(fixture: dict[str, Any], expected_proposal_id: str | None = None) -> dict[str, Any]:
    """Evaluate a synthetic contract without granting external evidence credit."""
    missing = sorted(REQUIRED - set(fixture))
    reasons: list[str] = []
    if missing:
        reasons.append("missing_required_fields")
    if expected_proposal_id and fixture.get("proposal_id") != expected_proposal_id:
        reasons.append("proposal_id_mismatch")
    if fixture.get("bounded") is not True:
        reasons.append("unbounded_fixture")
    if not fixture.get("protected_gates"):
        reasons.append("missing_protected_gates")
    if not fixture.get("required_obligations"):
        reasons.append("missing_required_obligations")
    if fixture.get("production") is not False:
        reasons.append("production_promotion")
    if fixture.get("authority_credit") is not False:
        reasons.append("authority_promotion")
    if fixture.get("stage20") is not False:
        reasons.append("stage20_promotion")
    if fixture.get("real_rows") != 0:
        reasons.append("unsupported_real_rows")
    if fixture.get("real_people") != 0:
        reasons.append("unsupported_participant_evidence")
    accepted = not reasons
    return {
        "schema": "ghc.family.v650-v2.runtime-result.v1",
        "proposal_id": fixture.get("proposal_id"),
        "accepted": accepted,
        "rejected": not accepted,
        "reasons": sorted(set(reasons)),
        "bounded": True,
        "external_side_effects": False,
        "authority_credit": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def mutation_fixtures(valid: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Return the five preregistered rejecting mutation classes."""
    rows: list[tuple[str, dict[str, Any]]] = []
    missing = deepcopy(valid)
    missing["required_obligations"] = []
    rows.append(("missing_obligation", missing))
    production = deepcopy(valid)
    production["production"] = True
    rows.append(("production_promotion", production))
    empirical = deepcopy(valid)
    empirical["real_rows"] = 1
    rows.append(("unsupported_real_row", empirical))
    authority = deepcopy(valid)
    authority["authority_credit"] = True
    rows.append(("authority_promotion", authority))
    stage20 = deepcopy(valid)
    stage20["stage20"] = True
    rows.append(("stage20_promotion", stage20))
    return rows


def runner_main(expected_proposal_id: str | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    result = evaluate(payload, expected_proposal_id)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(runner_main())
