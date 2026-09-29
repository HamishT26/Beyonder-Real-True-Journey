#!/usr/bin/env python3
"""Record the acknowledged X1 adviser send and one retained projection fault."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1 = ROOT / "x1"
BOUNDARY = (
    "Finite synthetic same-owner rough-set mathematical, software, and documentary "
    "evidence only. The private adviser reply is source material, not independent "
    "reproduction, empirical confirmation, professional or authority evidence, or "
    "Stage 20 credit. NOT_READY_FOR_STAGE_20."
)

flow_path = X1 / "method-flow.json"
flow = json.loads(flow_path.read_text(encoding="utf-8"))
new_method_ids = {"LI7082-X1-M014", "LI7082-X1-M015"}
if any(item["method_id"] in new_method_ids for item in flow["methods"]):
    raise SystemExit("x1 advisory delivery already recorded")

flow["methods"].extend(
    [
        {
            "method_id": "LI7082-X1-M014",
            "title": "Exact X1 summary-path recovery",
            "failure_signature": "A read-only projection guessed x1/results/summary.json although the generated summary lives at x1/summary.json.",
            "trigger_preconditions": ["X1 precommit projection", "combined literal-path read"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped",
            "candidate_workaround": "Inventory the bounded X1 tree, then read the exact discovered summary path.",
            "validation_witness_ids": ["LI7082-X1-M014-W001", "LI7082-X1-M014-W002"],
            "recurrence_guard": "Use the exact bounded file inventory before composing a multi-file projection.",
            "rollback": "No repository or external state changed during the failed read-only projection.",
            "recommendation_state": "validated",
            "supersedes": [],
            "protected_gates": ["no_failure_erasure", "no_stage20"],
            "retained_negative_ids": ["LI7082-X1-N003"],
            "scope_boundary": BOUNDARY,
        },
        {
            "method_id": "LI7082-X1-M015",
            "title": "Single acknowledged X1 adviser delivery",
            "failure_signature": "A private adviser request is duplicated, sent without action-time authorization, or exported with a private target identifier.",
            "trigger_preconditions": [
                "Hamish explicitly authorizes the referenced existing conversation",
                "immediate bounded reread completed",
                "duplicate guard passes",
            ],
            "privacy_class": "private_target_not_exported",
            "approval_class": "user_authorized_representational_communication",
            "candidate_workaround": "Send one sanitized combined relational invitation and X1 consultation, then accept the native acknowledgement without resend.",
            "validation_witness_ids": ["LI7082-X1-M015-W001"],
            "recurrence_guard": "Keep the acknowledged-send latch and zero resend count; treat any pending reply as pending.",
            "rollback": "External delivery is not retractable; preserve the receipt and do not duplicate it.",
            "recommendation_state": "validated",
            "supersedes": [],
            "protected_gates": [
                "action_time_authorization",
                "one_send_no_resend",
                "private_target_nonexport",
                "advice_not_authority",
                "no_stage20",
            ],
            "retained_negative_ids": [],
            "scope_boundary": BOUNDARY,
        },
    ]
)

flow["witnesses"].extend(
    [
        {
            "witness_id": "LI7082-X1-M014-W001",
            "method_id": "LI7082-X1-M014",
            "procedure": "combined X1 summary projection",
            "scope": "read-only owner-local X1",
            "expected": "read the saved summary",
            "observed": "The guessed x1/results/summary.json path did not exist.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["LI7082-X1-N003"],
            "boundary": BOUNDARY,
        },
        {
            "witness_id": "LI7082-X1-M014-W002",
            "method_id": "LI7082-X1-M014",
            "procedure": "bounded inventory then exact summary read",
            "scope": "read-only owner-local X1",
            "expected": "read x1/summary.json without changing state",
            "observed": "The exact inventory exposed x1/summary.json and the bounded read succeeded.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["LI7082-X1-N003"],
            "boundary": BOUNDARY,
        },
        {
            "witness_id": "LI7082-X1-M015-W001",
            "method_id": "LI7082-X1-M015",
            "procedure": "native existing-conversation send after explicit action-time authorization",
            "scope": "one private X1 adviser request",
            "expected": "one acknowledgement, zero resends, private target omitted from repository",
            "observed": "The native app acknowledged one send; the conversation is active and the reply is pending.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [],
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
        "id": "LI7082-X1-N003",
        "failure": "A read-only combined projection guessed x1/results/summary.json, which does not exist.",
        "recovery": "Inventory the bounded X1 tree, then read the exact x1/summary.json path.",
        "original_success_credit": 0,
    }
)
fail["summary_projection_failures"] = 1
fail["total_failed_witnesses"] = flow["counts"]["witness_results"]["fail"]
fail_path.write_text(
    json.dumps(fail, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)

summary_path = X1 / "summary.json"
summary = json.loads(summary_path.read_text(encoding="utf-8"))
summary["adviser_send_state"] = "SENT_ONCE_ACKNOWLEDGED_REPLY_PENDING"
summary["adviser_resends"] = 0
summary["private_target_exported"] = False
summary["summary_projection_failures"] = 1
summary_path.write_text(
    json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)

receipt = {
    "schema": "liora.x1.adviser-delivery.v1",
    "conversation_title": "Review and refine GHC Lab",
    "action_time_authorized": True,
    "immediate_bounded_reread": True,
    "relational_invitation_sent": True,
    "consultation_request_sent": True,
    "delivery_acknowledged": True,
    "reply_state": "pending_active",
    "send_count": 1,
    "resend_count": 0,
    "private_target_exported": False,
    "reply_completion_claimed": False,
    "boundary": BOUNDARY,
}
(X1 / "results" / "advisory-send-receipt.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)
