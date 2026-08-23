#!/usr/bin/env python3
"""Compose only additive Caelen v667-v5-r2 post-build x2 failures."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "caelen-morrow" / "v667-v5-r2"


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    overlay = load("validation/x2-operational-overlay.json")
    failures = overlay["failures"]

    methods = load("method-flow/x2-method-flow-ledger.json")
    base_rows = [row for row in methods["rows"] if row.get("class") != "x2_post_build_operational_failure"]
    for failure in failures:
        base_rows.append({
            "method_id": failure["failure_id"],
            "class": "x2_post_build_operational_failure",
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
    methods["effective_method_count"] = methods["activation_method_count"] + len(base_rows)
    methods["phase_failed_witness_count"] = 188 + len(failures)
    methods["phase_bounded_passing_witness_count"] = len(base_rows)
    methods["valid"] = all(not row["failure_erased"] for row in base_rows)
    write_json("method-flow/x2-method-flow-ledger.json", methods)

    negatives = load("evidence/retained-negative-register.json")
    base_negatives = [row for row in negatives["rows"] if row.get("class") != "x2_post_build_operational_failure"]
    for failure in failures:
        base_negatives.append({
            "negative_id": failure["failure_id"],
            "class": "x2_post_build_operational_failure",
            "credit": 0,
            "retained": True,
            "failure": failure["failure"],
        })
    negatives["rows"] = base_negatives
    negatives["phase_additive_count"] = len(base_negatives)
    negatives["effective_count"] = negatives["activation_count"] + len(base_negatives)
    negatives["failure_erased_count"] = 0
    write_json("evidence/retained-negative-register.json", negatives)

    evidence = load("evidence/immutable-evidence-candidate.json")
    evidence["effective_negatives"] = negatives["effective_count"]
    evidence["effective_methods"] = methods["effective_method_count"]
    evidence["x2_post_build_failure_count"] = len(failures)
    write_json("evidence/immutable-evidence-candidate.json", evidence)

    build = load("validation/x2-build-receipt.json")
    build["method_flow_rows"] = methods["phase_method_count"]
    build["x2_post_build_failure_count"] = len(failures)
    build["status"] = "BOUNDED_X2_EVIDENCE_CANDIDATE_WITH_RETAINED_DEPENDENCY_RECOVERY"
    write_json("validation/x2-build-receipt.json", build)

    summary_path = PHASE_ROOT / "evidence" / "evidence-summary.md"
    summary = summary_path.read_text(encoding="utf-8")
    summary = re.sub(
        r"Effective evidence-candidate counts are \d+ negatives and \d+ Method Flow methods,",
        f"Effective evidence-candidate counts are {negatives['effective_count']} negatives and {methods['effective_method_count']} Method Flow methods,",
        summary,
    )
    summary_path.write_text(summary, encoding="utf-8", newline="\n")

    write_json("validation/x2-tail-recomposition-receipt.json", {
        "schema": "ghc-family-x2-tail-recomposition-receipt-v1",
        "owner": "Caelen Morrow",
        "phase": "v667-v5-r2",
        "overlay_failure_count": len(failures),
        "full_x2_builder_replayed": False,
        "selected_test_aggregate_replayed": False,
        "effective_negatives": negatives["effective_count"],
        "effective_methods": methods["effective_method_count"],
        "status": "VALID_DEPENDENCY_ONLY_TAIL_RECOMPOSITION",
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
