#!/usr/bin/env python3
"""Detailed bounded evidence validator for Orin Thale v653-v7."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import ghc_family_v653_v2_detailed_validator as base
import ghc_family_v653_v7_phase_data as data
from ghc_family_v653_v7_validation_common import PHASE, read_json, write_json


base.data = data
base.PHASE = PHASE
base.read_json = read_json
base.write_json = write_json


def validate():
    result = base.validate()
    gates = read_json(PHASE / "exact-open-gate-register-x2.json")
    workflow = read_json(
        PHASE / "workflow/x2-refinement/workflow-plan-validation.json"
    )
    workflow_issues = read_json(
        PHASE / "workflow/x2-refinement/workflow-plan-issues.json"
    )
    for row in result["checks"]:
        if row["name"] == "aggregate:gates":
            row["passed"] = (
                gates["effective_open_gaps"] == 76
                and gates["effective_exact_gates"] == 77
                and gates["none_silently_closed"]
            )
            row["detail"] = gates
        elif row["name"] == "aggregate:workflow":
            row["passed"] = (
                workflow["status"] == "valid"
                and workflow["valid"]
                and workflow["policy_checks"] == 20
                and workflow["policy_checks_passed"] == 20
                and workflow_issues["counts"]["errors"] == 0
                and workflow_issues["counts"]["warnings"] == 0
                and workflow_issues["counts"]["issues"] == 0
                and not workflow_issues["issues"]
            )
            row["detail"] = {
                "frozen_x1_status": "valid",
                "additive_x2_confirmation_status": workflow["status"],
                "stop_after_closeout_route_confirmed": True,
            }
    result["schema"] = "ghc.family.v653-v7.detailed-validation.v1"
    result["passed_count"] = sum(row["passed"] for row in result["checks"])
    result["valid"] = all(row["passed"] for row in result["checks"])
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = validate()
    if args.receipt:
        write_json(args.receipt, result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
