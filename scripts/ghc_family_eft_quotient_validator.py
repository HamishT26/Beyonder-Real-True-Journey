#!/usr/bin/env python3
"""Validate typed synthetic EFT operator-quotient fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def evaluate(case: dict) -> dict:
    reasons: list[str] = []
    if not isinstance(case.get("mass_dimension"), int) or case["mass_dimension"] < 0:
        reasons.append("invalid_mass_dimension")
    if case.get("uses_field_redefinition") and not case.get("field_redefinition_invertible"):
        reasons.append("noninvertible_field_redefinition")
    if case.get("uses_field_redefinition") and not case.get("perturbative_order_consistent"):
        reasons.append("field_redefinition_order_mismatch")
    redundant = bool(case.get("total_derivative") or case.get("equation_of_motion_redundant") or case.get("field_redefinition_redundant"))
    if redundant and case.get("claimed_independent"):
        reasons.append("redundant_operator_claimed_independent")
    if case.get("claim_scope") not in {"synthetic_structure", "formal_model_only"}:
        reasons.append("overpromoted_claim_scope")
    accepted = not reasons
    return {"case_id": case["case_id"], "accepted": accepted, "reasons": reasons, "redundant": redundant}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    fixtures = json.loads(args.fixtures.read_text(encoding="utf-8"))
    results = [evaluate(case) for case in fixtures["cases"]]
    expected = {case["case_id"]: case["expected_accepted"] for case in fixtures["cases"]}
    checks = [item["accepted"] == expected[item["case_id"]] for item in results]
    receipt = {
        "schema": "ghc.family.eft-quotient-validation.v1", "case_count": len(results),
        "passed_expectation_count": sum(checks), "valid": all(checks), "results": results,
        "boundary": "Synthetic operator classification is not an S-matrix calculation, empirical GMUT confirmation, or Theory-of-Everything result.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"cases": len(results), "valid": receipt["valid"]}, indent=2))
    if not receipt["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
