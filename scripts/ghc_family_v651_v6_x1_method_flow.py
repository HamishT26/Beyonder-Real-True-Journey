#!/usr/bin/env python3
"""Materialize Elaren v651-v6 x1 Method Flow through the family-current engine."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import ghc_family_method_flow_state as wrapper


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/elaren-kestrel/v651-v6/method-flow"
LEDGER = ROOT / "method-flow-ledger.json"
MF = runpy.run_path(str(wrapper.resolve_skill_runner()), run_name="ghc_family_method_flow_engine")


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    method_paths = sorted((ROOT / "records").glob("m??-method.json"))
    if len(method_paths) != 5:
        raise RuntimeError(f"expected five x1 methods, observed {len(method_paths)}")
    ledger = MF["new_ledger"]("v651-v6", "Elaren Kestrel")
    for method_path in method_paths:
        method = read(method_path)
        ledger["methods"].append(method)
        MF["append_event"](ledger, method["method_id"], None, "candidate", "method recorded after retained failure")
        stem = method_path.name.removesuffix("-method.json")
        for label in ("fail", "pass"):
            witness = read(ROOT / "records" / f"{stem}-{label}.json")
            ledger["witnesses"].append(witness)
            method["validation_witness_ids"].append(witness["witness_id"])
            if witness["result"] == "pass":
                method["recommendation_state"] = "validated"
                MF["append_event"](ledger, method["method_id"], "candidate", "validated", "bounded recovery witness passed", witness["witness_id"])
        if method["recommendation_state"] != "validated":
            raise RuntimeError(f"method lacks passing witness: {method['method_id']}")
        method["recommendation_state"] = "preferred"
        MF["append_event"](ledger, method["method_id"], "validated", "preferred", "preferred only for the declared trigger")
        ledger["recommendations"].append({
            "recommendation_index": len(ledger["recommendations"]) + 1,
            "method_id": method["method_id"],
            "preconditions": method["trigger_preconditions"],
            "method": method["candidate_workaround"],
            "witness_ids": method["validation_witness_ids"],
            "recurrence_guard": method["recurrence_guard"],
            "rollback": method["rollback"],
            "scope_boundary": method["scope_boundary"],
        })
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
        "preferred_methods": [{key: row[key] for key in ("method_id", "title", "trigger_preconditions", "candidate_workaround", "validation_witness_ids", "recurrence_guard", "rollback", "scope_boundary")} for row in ledger["methods"]],
        "retained_failed_witnesses": [row["witness_id"] for row in ledger["witnesses"] if row["result"] == "fail"],
        "valid": True,
        "boundary": ledger["boundary"],
    }
    MF["write_json"](ROOT / "method-flow-summary.json", summary)
    (ROOT / "method-flow-summary.md").write_text(MF["render_markdown"](ledger), encoding="utf-8", newline="\n")
    print(json.dumps({"methods": 5, "failed_witnesses": 5, "passing_witnesses": 5, "preferred": 5, "valid": True}))


if __name__ == "__main__":
    main()
