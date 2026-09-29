#!/usr/bin/env python3
"""Bind the successful one-shot X2 model session into Method Flow."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X2 = ROOT / "x2"
receipt = json.loads((X2 / "laboratory" / "receipt.json").read_text(encoding="utf-8"))
if receipt["model_invocations"] != 15 or receipt["successes"] != 15 or receipt["replays"] != 0:
    raise SystemExit("unexpected X2 laboratory receipt")

boundary = (
    "Fifteen finite synthetic current-laboratory model invocations only. No observation, "
    "measurement, empirical confirmation, production readiness, independent reproduction, "
    "professional or authority evidence, or Stage 20 credit. NOT_READY_FOR_STAGE_20."
)
flow_path = X2 / "method-flow.json"
flow = json.loads(flow_path.read_text(encoding="utf-8"))
if any(item["method_id"] == "LI7082-X2-M027" for item in flow["methods"]):
    raise SystemExit("X2 laboratory already recorded")
witness_ids = ["LI7082-X2-LAB-W001"] + [f"LI7082-X2-LAB-W{i:03d}" for i in range(2, 17)]
flow["methods"].append(
    {
        "method_id": "LI7082-X2-M027",
        "title": "Current v20 X2 laboratory entrypoint recovery and one-shot model session",
        "failure_signature": "The operations module is mistaken for the declared file-writing runner, or a saved model is replayed, lacks rows, or promotes a synthetic result into an empirical claim.",
        "trigger_preconditions": ["immutable pushed X1", "distinct X2 request set", "empty X2 result directory"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_scoped",
        "candidate_workaround": "Retain the zero-result module invocation, use the declared runner.txt file-writing entrypoint, then bind request/result digests without replay.",
        "validation_witness_ids": witness_ids,
        "recurrence_guard": "Refuse execution if any X2 model result already exists.",
        "rollback": "Discard only incomplete uncommitted X2 model outputs; never rerun a successful saved model.",
        "recommendation_state": "validated",
        "supersedes": [],
        "protected_gates": ["no_model_replay", "no_empirical_promotion", "no_stage20"],
        "retained_negative_ids": ["LI7082-X2-N003"],
        "scope_boundary": boundary,
    }
)
flow["witnesses"].append(
    {
        "witness_id": witness_ids[0],
        "method_id": "LI7082-X2-M027",
        "procedure": "first X2 heat invocation through operations.js",
        "scope": "current v20 laboratory X2",
        "expected": "exclusive saved heat result",
        "observed": "operations.js returned zero as a module but wrote no result; the session stopped with zero successful model results.",
        "result": "fail",
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": ["LI7082-X2-N003"],
        "boundary": boundary,
    }
)
for witness_id, record in zip(witness_ids[1:], receipt["records"]):
    flow["witnesses"].append(
        {
            "witness_id": witness_id,
            "method_id": "LI7082-X2-M027",
            "procedure": "current v20 laboratory model invocation",
            "scope": record["model"],
            "expected": "one saved finite result with empirical_claim false",
            "observed": f"rows={record['rows']}; request={record['request_sha256']}; result={record['result_sha256']}",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["LI7082-X2-N003"],
            "boundary": boundary,
        }
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
    json.dumps(flow, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)

summary_path = X2 / "summary.json"
summary = json.loads(summary_path.read_text(encoding="utf-8"))
summary["models"] = 15
summary["model_replays"] = 0
summary["laboratory_initial_failures"] = 1
summary_path.write_text(
    json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)

failure_path = X2 / "failure-ledger.json"
failure = json.loads(failure_path.read_text(encoding="utf-8"))
failure["x2"]["operational"].append(
    {
        "id": "LI7082-X2-N003",
        "failure": "The first X2 heat invocation used operations.js directly; it returned zero as a module but wrote no declared result, and the session stopped with zero successful models.",
        "recovery": "Use the release's declared laboratory/runner.txt file-writing entrypoint for the still-unexecuted fifteen-model session.",
        "original_success_credit": 0,
    }
)
failure["x2"]["laboratory_model_failures"] = 1
failure["total_failed_witnesses"] = flow["counts"]["witness_results"]["fail"]
failure_path.write_text(
    json.dumps(failure, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)
