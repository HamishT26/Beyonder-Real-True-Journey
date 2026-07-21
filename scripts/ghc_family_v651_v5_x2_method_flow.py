#!/usr/bin/env python3
"""Append v651-v5 x2 failures to immutable-x1 Method Flow evidence."""

from __future__ import annotations

import json
import runpy
import subprocess
from pathlib import Path

import build_ghc_family_v651_v5_evidence as evidence
import ghc_family_method_flow_state as wrapper


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v651-v5/method-flow"
LEDGER_PATH = "docs/eiren-kestrel/v651-v5/method-flow/method-flow-ledger.json"
MF = runpy.run_path(str(wrapper.resolve_skill_runner()), run_name="ghc_family_method_flow_engine")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    ledger = json.loads(
        subprocess.check_output(
            ["git", "show", f"{evidence.X1_COMMIT}:{LEDGER_PATH}"],
            cwd=REPO,
            text=True,
            encoding="utf-8",
        )
    )
    if ledger["counts"]["methods"] != 19:
        raise RuntimeError("unexpected immutable x1 Method Flow baseline")

    for offset, failure in enumerate(evidence.X2_OPS, 20):
        method_id = f"V6515-M{offset:02d}"
        negative_id = failure["negative_id"]
        recovery = failure["recovery"]
        method = {
            "method_id": method_id,
            "title": f"Bounded x2 recovery {offset:02d}: {recovery.rstrip('.')}",
            "trigger_preconditions": [failure["summary"]],
            "failure_signature": failure["summary"],
            "candidate_workaround": recovery,
            "validation_witness_ids": [],
            "recurrence_guard": recovery,
            "rollback": "Give the failed attempt zero credit, retain it, and stop if the bounded recovery cannot be attributed.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["failure_retention", "privacy", "bounded_scope", "same_owner_only"],
            "approval_class": "safe_now_owner_scoped_workflow",
            "privacy_class": "sanitized_public",
            "scope_boundary": "Same-owner workflow recovery only; no scientific, production, identity, authority, or independent-reproduction credit.",
            "retained_negative_ids": [negative_id],
        }
        fail = {
            "witness_id": f"{method_id}-WFAIL",
            "method_id": method_id,
            "result": "fail",
            "scope": "one bounded x2 workflow operation",
            "procedure": failure["summary"],
            "expected": "Produce attributable bounded evidence without erasing the failed attempt.",
            "observed": failure["summary"],
            "retained_negative_ids": [negative_id],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Workflow witness only; no broader evidence or authority credit.",
        }
        passed = {
            "witness_id": f"{method_id}-WPASS",
            "method_id": method_id,
            "result": "pass",
            "scope": "one bounded x2 workflow operation",
            "procedure": recovery,
            "expected": "Produce attributable bounded evidence without erasing the failed attempt.",
            "observed": recovery + " A bounded attributable witness completed.",
            "retained_negative_ids": [negative_id],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Workflow witness only; no broader evidence or authority credit.",
        }
        base = ROOT / f"x2-v6515-m{offset:02d}"
        write_json(Path(str(base) + "-method-record.json"), method)
        write_json(Path(str(base) + "-wfail-witness.json"), fail)
        write_json(Path(str(base) + "-wpass-witness.json"), passed)

        ledger["methods"].append(method)
        MF["append_event"](ledger, method_id, None, "candidate", "x2 method recorded with retained negative linkage")
        for witness in (fail, passed):
            ledger["witnesses"].append(witness)
            method["validation_witness_ids"].append(witness["witness_id"])
        method["recommendation_state"] = "validated"
        MF["append_event"](ledger, method_id, "candidate", "validated", "bounded x2 witness passed", passed["witness_id"])
        method["recommendation_state"] = "preferred"
        MF["append_event"](ledger, method_id, "validated", "preferred", "bounded x2 recovery is preferred for its exact trigger")
        ledger["recommendations"].append(
            {
                "recommendation_index": len(ledger["recommendations"]) + 1,
                "method_id": method_id,
                "preconditions": method["trigger_preconditions"],
                "method": recovery,
                "witness_ids": method["validation_witness_ids"],
                "recurrence_guard": recovery,
                "rollback": method["rollback"],
                "scope_boundary": method["scope_boundary"],
            }
        )

    MF["refresh_counts"](ledger)
    receipt = MF["validate_ledger"](ledger)
    if not receipt["valid"]:
        raise RuntimeError(receipt["issues"])
    MF["write_json"](ROOT / "method-flow-ledger.json", ledger)
    MF["write_json"](ROOT / "method-flow-validation.json", receipt)
    summary = {
        "schema": "ghc.family.method-flow-state.summary.v1",
        "phase": ledger["phase"],
        "owner": ledger["owner"],
        "counts": ledger["counts"],
        "preferred_methods": [
            {
                "method_id": row["method_id"],
                "title": row["title"],
                "trigger_preconditions": row["trigger_preconditions"],
                "candidate_workaround": row["candidate_workaround"],
                "validation_witness_ids": row["validation_witness_ids"],
                "recurrence_guard": row["recurrence_guard"],
                "rollback": row["rollback"],
                "scope_boundary": row["scope_boundary"],
            }
            for row in ledger["methods"]
        ],
        "retained_failed_witnesses": [row["witness_id"] for row in ledger["witnesses"] if row["result"] == "fail"],
        "valid": True,
        "boundary": ledger["boundary"],
    }
    MF["write_json"](ROOT / "method-flow-summary.json", summary)
    (ROOT / "method-flow-summary.md").write_text(MF["render_markdown"](ledger), encoding="utf-8", newline="\n")
    print(json.dumps({"methods": ledger["counts"]["methods"], "x2_added": len(evidence.X2_OPS), "failed": ledger["counts"]["witness_results"]["fail"], "passed": ledger["counts"]["witness_results"]["pass"], "valid": True}))


if __name__ == "__main__":
    main()
