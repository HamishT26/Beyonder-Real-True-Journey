#!/usr/bin/env python3
"""Append the X1 laboratory output-directory failure and isolated recovery."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1 = ROOT / "x1"
BOUNDARY = "Finite synthetic same-owner and current-laboratory evidence only. No observation, empirical confirmation, production readiness, independent reproduction, professional or authority claim. NOT_READY_FOR_STAGE_20."

flow_path = X1 / "method-flow.json"
flow = json.loads(flow_path.read_text(encoding="utf-8"))
if any(item["method_id"] == "LI7082-X1-M013" for item in flow["methods"]):
    raise SystemExit("lab recovery already recorded")
flow["methods"].append({
    "method_id": "LI7082-X1-M013",
    "title": "Current-laboratory result-directory recovery",
    "failure_signature": "The laboratory runner receives an output path whose parent does not exist and refuses before saving a model result.",
    "trigger_preconditions": ["X1 current-laboratory model session", "provided runner uses exclusive output creation"],
    "privacy_class": "sanitized_public",
    "approval_class": "safe_now_owner_scoped",
    "candidate_workaround": "Create only the declared result parent, preserve the failed heat request/refusal, then run the previously unexecuted model set.",
    "validation_witness_ids": ["LI7082-X1-M013-W001", "LI7082-X1-M013-W002"],
    "recurrence_guard": "Preflight request and output parent directories before invoking an exclusive-create runner.",
    "rollback": "Discard only uncommitted laboratory outputs and return to the planning head.",
    "recommendation_state": "validated",
    "supersedes": [],
    "protected_gates": ["no_failure_erasure", "no_model_replay", "no_empirical_promotion", "no_stage20"],
    "retained_negative_ids": ["LI7082-X1-N002"],
    "scope_boundary": BOUNDARY,
})
flow["witnesses"].extend([
    {"witness_id":"LI7082-X1-M013-W001","method_id":"LI7082-X1-M013","procedure":"first heat model invocation","scope":"current v20 laboratory X1","expected":"exclusive result write","observed":"Runner refused because the declared result parent did not exist; zero model results had been written.","result":"fail","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":["LI7082-X1-N002"],"boundary":BOUNDARY},
    {"witness_id":"LI7082-X1-M013-W002","method_id":"LI7082-X1-M013","procedure":"isolated parent-directory recovery and one model session","scope":"current v20 laboratory X1","expected":"fifteen distinct saved model results","observed":"15/15 results saved, empirical_claim false throughout, replay count zero.","result":"pass","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":["LI7082-X1-N002"],"boundary":BOUNDARY},
])
flow["counts"]["methods"] = len(flow["methods"])
flow["counts"]["witnesses"] = len(flow["witnesses"])
flow["counts"]["states"]["validated"] = sum(item["recommendation_state"] == "validated" for item in flow["methods"])
flow["counts"]["witness_results"] = {"pass": sum(item["result"] == "pass" for item in flow["witnesses"]), "fail": sum(item["result"] == "fail" for item in flow["witnesses"])}
flow_path.write_text(json.dumps(flow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

fail_path = X1 / "failure-ledger.json"
fail = json.loads(fail_path.read_text(encoding="utf-8"))
fail["x1_operational_failures"].append({"id":"LI7082-X1-N002","failure":"The first laboratory heat invocation supplied an output under an absent parent directory and the exclusive-create runner refused before saving any model.","recovery":"Create the declared results parent only, retain the failed request/refusal, and execute the previously unexecuted fifteen-model session once.","original_success_credit":0})
fail["laboratory_model_failures"] = 1
fail["total_failed_witnesses"] = flow["counts"]["witness_results"]["fail"]
fail_path.write_text(json.dumps(fail, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

summary_path = X1 / "summary.json"
summary = json.loads(summary_path.read_text(encoding="utf-8"))
summary["models"] = 15
summary["current_laboratory_models"] = 15
summary["rough_set_coordinate_projections"] = 15
summary["model_count_credit"] = 15
summary["laboratory_initial_failures"] = 1
summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
