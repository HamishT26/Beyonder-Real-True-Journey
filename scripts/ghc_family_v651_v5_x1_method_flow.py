#!/usr/bin/env python3
"""Materialize Eiren v651-v5 x1 Method Flow through the family-current engine."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import ghc_family_method_flow_state as wrapper


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v651-v5/method-flow"
LEDGER = ROOT / "method-flow-ledger.json"
MF = runpy.run_path(str(wrapper.resolve_skill_runner()), run_name="ghc_family_method_flow_engine")


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    method_paths = sorted(ROOT.glob("v6515-m??-method-record.json"))
    if not method_paths:
        raise RuntimeError("no x1 Method Flow inputs")

    ledger = MF["new_ledger"]("v651-v5", "Eiren Kestrel")
    for method_path in method_paths:
        method = read(method_path)
        if method["recommendation_state"] != "candidate":
            raise RuntimeError(f"method must begin candidate: {method['method_id']}")
        ledger["methods"].append(method)
        MF["append_event"](ledger, method["method_id"], None, "candidate", "method recorded with retained negative linkage")

        prefix = method_path.name.removesuffix("-method-record.json")
        for label in ("wfail", "wpass"):
            witness = read(ROOT / f"{prefix}-{label}-witness.json")
            ledger["witnesses"].append(witness)
            method["validation_witness_ids"].append(witness["witness_id"])
            if witness["result"] == "pass":
                method["recommendation_state"] = "validated"
                MF["append_event"](
                    ledger,
                    method["method_id"],
                    "candidate",
                    "validated",
                    "bounded witness passed",
                    witness["witness_id"],
                )

        if method["recommendation_state"] != "validated":
            raise RuntimeError(f"method lacks passing witness: {method['method_id']}")
        method["recommendation_state"] = "preferred"
        MF["append_event"](ledger, method["method_id"], "validated", "preferred", "bounded recovery is preferred for its exact trigger")
        ledger["recommendations"].append(
            {
                "recommendation_index": len(ledger["recommendations"]) + 1,
                "method_id": method["method_id"],
                "preconditions": method["trigger_preconditions"],
                "method": method["candidate_workaround"],
                "witness_ids": method["validation_witness_ids"],
                "recurrence_guard": method["recurrence_guard"],
                "rollback": method["rollback"],
                "scope_boundary": method["scope_boundary"],
            }
        )

    MF["refresh_counts"](ledger)
    receipt = MF["validate_ledger"](ledger)
    if not receipt["valid"]:
        raise RuntimeError(receipt["issues"])
    MF["write_json"](LEDGER, ledger)
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
    print(json.dumps({"methods": len(method_paths), "failed_witnesses": len(method_paths), "passing_witnesses": len(method_paths), "preferred": len(method_paths), "valid": True}))


if __name__ == "__main__":
    main()
