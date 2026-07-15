#!/usr/bin/env python3
"""Validate the append-only Tamar v645-v7 Method Flow state."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys

from ghc_family_v645_v7_runtime import PHASE, ROOT, TRUTH_BOUNDARY, read_json, write_json


FAMILY_RUNNER = ROOT / "scripts/ghc_family_method_flow_state.py"
LEDGER = PHASE / "method-flow/method-flow-state.json"
X2_LEDGER = PHASE / "method-flow/method-flow-state-x2.json"

INCIDENTS = [
    {
        "number": 10,
        "negative_id": "V6457-X2-N01",
        "title": "Classify scanner-definition literals before privacy evidence credit",
        "failure": "The first evidence validation treated a privacy-scanner definition literal as confirmed private material and the child returned nonzero.",
        "failed": "Scan every owner file and classify every regular-expression self-match as repository private content.",
        "recovery": "Retain every candidate, mark only the exact scanner-definition line as definition context, and require zero confirmed content hits.",
        "observed": "The same full owner scope retained one scanner-definition candidate and returned zero confirmed private-content hits.",
        "guard": "Keep candidate and confirmed counts separate; context recovery may never remove a path or pattern class from scope.",
        "rollback": "Give the failed scan zero privacy credit and preserve its receipt before rerunning unchanged scope.",
    },
    {
        "number": 11,
        "negative_id": "V6457-X2-N02",
        "title": "Load scoped test files by exact repository path",
        "failure": "The first scoped validation resolved nine dotted test names through the wrong package surface and produced nine import errors with zero test credit.",
        "failed": "Use dotted tests.* module names in an environment where another tests package may shadow the repository directory.",
        "recovery": "Load each unchanged scoped test file through its exact repository path and a unique module name.",
        "observed": "All bounded recent-round and current-packet tests loaded from the intended files and ran without import errors.",
        "guard": "File-launched validators must bind scoped tests to exact owner-reviewed paths, not an ambiguous package name.",
        "rollback": "Retain the nine import errors as one evidence-free attempt and do not change the test sources to make loading pass.",
    },
]


def call(*args: str) -> None:
    subprocess.run(
        [sys.executable, str(FAMILY_RUNNER), *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def main() -> int:
    shutil.copyfile(LEDGER, X2_LEDGER)
    for incident in INCIDENTS:
        number = incident["number"]
        method_id = f"V6457-M{number:02d}"
        fail_id = f"V6457-W{number:02d}-F"
        pass_id = f"V6457-W{number:02d}-P"
        record = {
            "method_id": method_id,
            "title": incident["title"],
            "failure_signature": incident["failure"],
            "trigger_preconditions": ["v645-v7 x2 evidence validation", "same-owner local tooling"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_local_tooling",
            "candidate_workaround": incident["recovery"],
            "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": incident["guard"],
            "rollback": incident["rollback"],
            "rollback_witness_required": True,
            "side_effect_budget": ["owner_candidate_receipts_only", "no_ref_change", "no_remote_change"],
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["private_material", "destructive_action", "sibling_lane", "host_change"],
            "retained_negative_ids": [incident["negative_id"]],
            "scope_boundary": "Same-owner operational recovery only; no scientific, authority, production, accessibility-complete, security-complete, or independent-reproduction credit.",
        }
        failed = {"witness_id": fail_id, "method_id": method_id, "procedure": incident["failed"], "scope": "single owner-local evidence validation", "expected": "bounded validation completes without false credit", "observed": incident["failure"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [incident["negative_id"]], "boundary": TRUTH_BOUNDARY}
        passed = {"witness_id": pass_id, "method_id": method_id, "procedure": incident["recovery"], "scope": "single owner-local evidence validation", "expected": "bounded validation completes without false credit", "observed": incident["observed"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [incident["negative_id"]], "boundary": TRUTH_BOUNDARY}
        record_rel = f"method-flow/v6457-m{number:02d}-method-record.json"
        fail_rel = f"method-flow/v6457-w{number:02d}-f-witness.json"
        pass_rel = f"method-flow/v6457-w{number:02d}-p-witness.json"
        write_json(record_rel, record)
        write_json(fail_rel, failed)
        write_json(pass_rel, passed)
        call("record", "--ledger", str(X2_LEDGER), "--record-file", str(PHASE / record_rel))
        call("witness", "--ledger", str(X2_LEDGER), "--witness-file", str(PHASE / fail_rel))
        call("witness", "--ledger", str(X2_LEDGER), "--witness-file", str(PHASE / pass_rel))
        call("set-state", "--ledger", str(X2_LEDGER), "--method-id", method_id, "--state", "preferred", "--note", "Bounded passing witness recorded for the declared trigger only")
    call("validate", "--ledger", str(X2_LEDGER), "--receipt", str(PHASE / "method-flow/method-flow-x2-validation.json"))
    call(
        "summarize",
        "--ledger",
        str(X2_LEDGER),
        "--json-output",
        str(PHASE / "method-flow/method-flow-summary-x2.json"),
        "--markdown-output",
        str(PHASE / "method-flow/method-flow-summary-x2.md"),
    )
    ledger = read_json("method-flow/method-flow-state-x2.json")
    counts = ledger["counts"]
    payload = {
        "schema": "ghc.family.v645-v7.method-flow-runner.v1",
        "family_runner_used": True,
        "methods": counts["methods"],
        "failed_witnesses": counts["witness_results"]["fail"],
        "passing_witnesses": counts["witness_results"]["pass"],
        "preferred_methods": counts["states"]["preferred"],
        "operational_negatives_retained": counts["methods"],
        "failure_erasure_count": 0,
        "x2_operational_incidents_at_execution_build": len(INCIDENTS),
        "retained_negative_ids": [row["negative_id"] for row in INCIDENTS],
        "same_owner_only": True,
        "independent_reproduction": False,
        "result": "pass",
        "boundary": TRUTH_BOUNDARY,
    }
    write_json("prototypes/runner-witnesses/ghc_family_v645_v7_method_flow_runner.json", payload)
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
