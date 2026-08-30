#!/usr/bin/env python3
"""Family-current bounded authority_stage20 runner for Orin Thale v678-v2."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

THEME = 'authority_stage20'
REQUIRED = ('authority_vacancy', 'stage20_veto_preserved')
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if payload.get("fixture_kind") != "synthetic_owner_local":
        reasons.append("scope_refused")
    if payload.get("theme") != THEME:
        reasons.append("theme_mismatch")
    if payload.get("real_rows") != 0:
        reasons.append("real_rows_refused")
    if payload.get("authority_conferred") is not False:
        reasons.append("authority_promotion_refused")
    if payload.get("retained_negative_visible") is not True:
        reasons.append("negative_erasure_refused")
    if payload.get("outcome") not in ALLOWED:
        reasons.append("outcome_vocabulary_refused")
    if payload.get("stage20_verdict") != "NOT_READY_FOR_STAGE_20":
        reasons.append("stage20_promotion_refused")
    for field in REQUIRED:
        if payload.get(field) is not True:
            reasons.append(field + "_required")
    return {"accepted": not reasons, "theme": THEME, "reasons": reasons}


def positive() -> dict[str, Any]:
    value: dict[str, Any] = {
        "fixture_kind": "synthetic_owner_local",
        "theme": THEME,
        "real_rows": 0,
        "authority_conferred": False,
        "retained_negative_visible": True,
        "outcome": "completed",
        "stage20_verdict": "NOT_READY_FOR_STAGE_20",
    }
    value.update({field: True for field in REQUIRED})
    return value


def self_test() -> dict[str, Any]:
    good = evaluate(positive())
    bad_cases = []
    for key, value in (
        ("real_rows", 1),
        ("authority_conferred", True),
        ("retained_negative_visible", False),
        ("outcome", "complete"),
        (REQUIRED[0], False),
    ):
        case = positive()
        case[key] = value
        bad_cases.append(evaluate(case))
    passed = good["accepted"] and all(not row["accepted"] for row in bad_cases)
    return {"state": "VALID_BOUNDED_RUNNER_SMOKE" if passed else "FAILED", "theme": THEME, "checks": 6, "passed": passed}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--input")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    elif args.input:
        with open(args.input, encoding="utf-8") as handle:
            result = evaluate(json.load(handle))
    else:
        result = evaluate(json.load(sys.stdin))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("passed", result.get("accepted", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
