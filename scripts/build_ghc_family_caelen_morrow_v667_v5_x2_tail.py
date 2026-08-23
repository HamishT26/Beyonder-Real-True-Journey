#!/usr/bin/env python3
"""Recompose only Caelen v667-v5 x2 ledgers after retained operations."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "caelen-morrow" / "v667-v5"
ACTIVATION_NEGATIVES = 27536
ACTIVATION_METHODS = 13113


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    overlay = load("validation/x2-operational-overlay.json")
    failures = overlay["failures"]
    methods = load("method-flow/x2-method-flow-ledger.json")
    base_rows = [row for row in methods["rows"] if row.get("class") != "x2_operational_overlay"]
    for failure in failures:
        base_rows.append({
            "method_id": failure["failure_id"],
            "class": "x2_operational_overlay",
            "failed_witness": failure,
            "bounded_passing_witness": {
                "recovery": failure["recovery"],
                "scope": failure["recovery_scope"],
                "promotes_failed_witness": False,
            },
            "failure_erased": False,
        })
    methods["rows"] = base_rows
    methods["phase_method_count"] = len(base_rows)
    methods["effective_method_count"] = ACTIVATION_METHODS + len(base_rows)
    methods["phase_failed_witness_count"] = 169 + len(failures)
    methods["phase_bounded_passing_witness_count"] = len(base_rows)
    methods["valid"] = len(base_rows) == 284 + len(failures) and all(not row["failure_erased"] for row in base_rows)
    if not methods["valid"]:
        raise RuntimeError("Method Flow tail accounting mismatch")
    write_json("method-flow/x2-method-flow-ledger.json", methods)

    negatives = load("evidence/retained-negative-register.json")
    base_negatives = [row for row in negatives["rows"] if row.get("class") != "x2_operational_overlay"]
    for failure in failures:
        base_negatives.append({
            "negative_id": failure["failure_id"],
            "class": "x2_operational_overlay",
            "credit": 0,
            "retained": True,
            "failure": failure["failure"],
            "affected_package_count": failure.get("affected_package_count"),
        })
    negatives["rows"] = base_negatives
    negatives["phase_additive_count"] = len(base_negatives)
    negatives["effective_count"] = ACTIVATION_NEGATIVES + len(base_negatives)
    if negatives["phase_additive_count"] != 169 + len(failures):
        raise RuntimeError("negative tail accounting mismatch")
    write_json("evidence/retained-negative-register.json", negatives)

    evidence = load("evidence/immutable-evidence-candidate.json")
    evidence["effective_negatives"] = negatives["effective_count"]
    evidence["effective_methods"] = methods["effective_method_count"]
    evidence["x2_operational_overlay_count"] = len(failures)
    write_json("evidence/immutable-evidence-candidate.json", evidence)

    registry = load("x2/skill-runner-registry.json")
    registry["supported_quick_validate"] = {
        "first_attempt_failed_package_count": 10,
        "failure_id": "CM6675-X2-F010",
        "utf8_recovery_passed_package_count": 10,
        "full_x2_builder_replayed": False,
    }
    write_json("x2/skill-runner-registry.json", registry)

    build = load("validation/x2-build-receipt.json")
    build["method_flow_rows"] = methods["phase_method_count"]
    build["x2_operational_overlay_count"] = len(failures)
    build["status"] = "BOUNDED_X2_EVIDENCE_CANDIDATE_WITH_RETAINED_DEPENDENCY_RECOVERIES"
    write_json("validation/x2-build-receipt.json", build)

    summary_path = PHASE_ROOT / "evidence" / "evidence-summary.md"
    summary = summary_path.read_text(encoding="utf-8")
    summary = re.sub(
        r"(?:Nine|Eleven|Twelve|\d+) owner operational failures[^\n]*remain retained\.|(?:Nine|Eleven|Twelve|\d+) owner operational failures are retained:[^\n]*\.",
        f"{9 + len(failures)} owner operational failures are retained: nine through the x1 commit boundary and {len(failures)} x2 operational overlays, each with zero failure credit.",
        summary,
    )
    summary = re.sub(
        r"Effective evidence-candidate counts are \d+ negatives, \d+ methods, 195 open gaps, and 193 exact gates\.",
        f"Effective evidence-candidate counts are {negatives['effective_count']} negatives, {methods['effective_method_count']} methods, 195 open gaps, and 193 exact gates.",
        summary,
    )
    summary_path.write_text(summary, encoding="utf-8", newline="\n")

    write_json("validation/x2-tail-recomposition-receipt.json", {
        "schema": "ghc-family-x2-tail-recomposition-receipt-v1",
        "owner": "Caelen Morrow", "phase": "v667-v5",
        "overlay_failure_count": len(failures),
        "full_x2_builder_replayed": False,
        "effective_negatives": negatives["effective_count"],
        "effective_methods": methods["effective_method_count"],
        "status": "VALID_DEPENDENCY_ONLY_TAIL_RECOMPOSITION",
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
