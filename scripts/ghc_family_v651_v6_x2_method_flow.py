#!/usr/bin/env python3
"""Append v651-v6 x2 failures to a copy of the frozen x1 Method Flow ledger."""

from __future__ import annotations

import copy
import json
import runpy
from pathlib import Path

import ghc_family_method_flow_state as wrapper


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/elaren-kestrel/v651-v6/method-flow"
MF = runpy.run_path(str(wrapper.resolve_skill_runner()), run_name="ghc_family_method_flow_engine")


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    ledger = copy.deepcopy(read(ROOT / "method-flow-ledger.json"))
    paths = sorted((ROOT / "x2-records").glob("m??-method.json"))
    if len(paths) != 1:
        raise RuntimeError(f"expected one x2 method, observed {len(paths)}")
    for path in paths:
        method = read(path)
        ledger["methods"].append(method)
        MF["append_event"](ledger, method["method_id"], None, "candidate", "x2 method recorded after retained validator failure")
        stem = path.name.removesuffix("-method.json")
        for label in ("fail", "pass"):
            witness = read(ROOT / "x2-records" / f"{stem}-{label}.json")
            ledger["witnesses"].append(witness)
            method["validation_witness_ids"].append(witness["witness_id"])
            if witness["result"] == "pass":
                method["recommendation_state"] = "validated"
                MF["append_event"](ledger, method["method_id"], "candidate", "validated", "bounded schema recovery passed", witness["witness_id"])
        method["recommendation_state"] = "preferred"
        MF["append_event"](ledger, method["method_id"], "validated", "preferred", "preferred only for declared Method Flow schema reads")
        ledger["recommendations"].append({"recommendation_index": len(ledger["recommendations"]) + 1, "method_id": method["method_id"], "preconditions": method["trigger_preconditions"], "method": method["candidate_workaround"], "witness_ids": method["validation_witness_ids"], "recurrence_guard": method["recurrence_guard"], "rollback": method["rollback"], "scope_boundary": method["scope_boundary"]})
    MF["refresh_counts"](ledger)
    receipt = MF["validate_ledger"](ledger)
    if not receipt["valid"]:
        raise RuntimeError(receipt["issues"])
    MF["write_json"](ROOT / "x2-method-flow-ledger.json", ledger)
    MF["write_json"](ROOT / "x2-method-flow-validation.json", receipt)
    summary = {"schema": "ghc.family.method-flow-state.summary.v1", "phase": ledger["phase"], "owner": ledger["owner"], "counts": ledger["counts"], "new_x2_methods": [row["method_id"] for row in ledger["methods"] if row["method_id"] == "V6516-M06"], "valid": True, "boundary": ledger["boundary"]}
    MF["write_json"](ROOT / "x2-method-flow-summary.json", summary)
    (ROOT / "x2-method-flow-summary.md").write_text(MF["render_markdown"](ledger), encoding="utf-8", newline="\n")
    print(json.dumps({"methods": ledger["counts"]["methods"], "witnesses": ledger["counts"]["witness_results"], "preferred": ledger["counts"]["states"]["preferred"], "valid": True}))


if __name__ == "__main__":
    main()
