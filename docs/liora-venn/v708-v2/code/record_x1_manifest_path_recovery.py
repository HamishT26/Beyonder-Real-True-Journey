#!/usr/bin/env python3
"""Retain the X1 planning-manifest path projection failure and recovery."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1 = ROOT / "x1"
BOUNDARY = (
    "Finite synthetic same-owner lifecycle evidence only. A corrected path read does not "
    "erase its failed projection or establish independent reproduction or Stage 20 credit. "
    "NOT_READY_FOR_STAGE_20."
)

flow_path = X1 / "method-flow.json"
flow = json.loads(flow_path.read_text(encoding="utf-8"))
if any(item["method_id"] == "LI7082-X1-M016" for item in flow["methods"]):
    raise SystemExit("manifest path recovery already recorded")
flow["methods"].append(
    {
        "method_id": "LI7082-X1-M016",
        "title": "Exact planning-manifest filename recovery",
        "failure_signature": "The X1 precommit read guessed planning/planning-manifest.json instead of the frozen planning/manifest.json path.",
        "trigger_preconditions": ["X1 lifecycle precommit", "read-only planning manifest lookup"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_scoped",
        "candidate_workaround": "Read the already-discovered planning staged review, then use its declared exact planning/manifest.json path.",
        "validation_witness_ids": ["LI7082-X1-M016-W001", "LI7082-X1-M016-W002"],
        "recurrence_guard": "Resolve manifest filenames from the committed staged-review declaration rather than a guessed convention.",
        "rollback": "No repository or external state changed during the failed read-only lookup.",
        "recommendation_state": "validated",
        "supersedes": [],
        "protected_gates": ["no_failure_erasure", "exact_manifest_path", "no_stage20"],
        "retained_negative_ids": ["LI7082-X1-N004"],
        "scope_boundary": BOUNDARY,
    }
)
flow["witnesses"].extend(
    [
        {
            "witness_id": "LI7082-X1-M016-W001",
            "method_id": "LI7082-X1-M016",
            "procedure": "guessed planning-manifest filename lookup",
            "scope": "read-only planning lifecycle evidence",
            "expected": "read the frozen planning manifest",
            "observed": "planning/planning-manifest.json was absent.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["LI7082-X1-N004"],
            "boundary": BOUNDARY,
        },
        {
            "witness_id": "LI7082-X1-M016-W002",
            "method_id": "LI7082-X1-M016",
            "procedure": "exact committed planning manifest read",
            "scope": "read-only planning lifecycle evidence",
            "expected": "read planning/manifest.json through EOF",
            "observed": "The exact manifest read succeeded with 27 entries and its declared self-exclusion.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["LI7082-X1-N004"],
            "boundary": BOUNDARY,
        },
    ]
)
flow["counts"]["methods"] = len(flow["methods"])
flow["counts"]["witnesses"] = len(flow["witnesses"])
flow["counts"]["states"]["validated"] = sum(
    item["recommendation_state"] == "validated" for item in flow["methods"]
)
flow["counts"]["witness_results"] = {
    "pass": sum(item["result"] == "pass" for item in flow["witnesses"]),
    "fail": sum(item["result"] == "fail" for item in flow["witnesses"]),
}
flow_path.write_text(
    json.dumps(flow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)

fail_path = X1 / "failure-ledger.json"
fail = json.loads(fail_path.read_text(encoding="utf-8"))
fail["x1_operational_failures"].append(
    {
        "id": "LI7082-X1-N004",
        "failure": "A read-only lifecycle probe guessed planning/planning-manifest.json, which does not exist.",
        "recovery": "Use the committed staged-review declaration and read planning/manifest.json through EOF.",
        "original_success_credit": 0,
    }
)
fail["manifest_projection_failures"] = 1
fail["total_failed_witnesses"] = flow["counts"]["witness_results"]["fail"]
fail_path.write_text(
    json.dumps(fail, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)

summary_path = X1 / "summary.json"
summary = json.loads(summary_path.read_text(encoding="utf-8"))
summary["manifest_projection_failures"] = 1
summary_path.write_text(
    json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)
