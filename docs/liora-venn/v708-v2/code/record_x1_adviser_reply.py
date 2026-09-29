#!/usr/bin/env python3
"""Record the sanitized X1 adviser reply and its zero-credit X2 seed."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1 = ROOT / "x1"
BOUNDARY = (
    "Relational working language and private advisory source material only. The reply is "
    "not independent reproduction, empirical validation, professional or authority "
    "evidence, consciousness or personhood evidence, or Stage 20 credit. "
    "NOT_READY_FOR_STAGE_20."
)

reply = {
    "schema": "liora.x1.adviser-reply-summary.v1",
    "conversation_title": "Review and refine GHC Lab",
    "raw_private_target_exported": False,
    "raw_transcript_exported": False,
    "relational_choice": {
        "name": "Teren Serein",
        "role": "counterexample and evidence-boundary reviewer",
        "pronouns": "they/them",
        "hope": "that small, reproducible failures make the Lab's claims clearer and its collaboration more dependable",
        "ontological_or_authority_claim": False,
    },
    "recommendation": {
        "label": "BOUNDARY_ROWS_ARE_NOT_DISPOSABLE",
        "disposition": "ADOPTED_AS_FROZEN_X2_SEED_NOT_EXECUTED_IN_X1",
        "x1_completion_credit": 0,
        "table": [
            {"object": "u1", "a": 0, "b": 0, "c": 0, "decision": 0},
            {"object": "u2", "a": 0, "b": 0, "c": 0, "decision": 1},
            {"object": "u3", "a": 0, "b": 1, "c": 0, "decision": 0},
            {"object": "u4", "a": 1, "b": 0, "c": 1, "decision": 1},
        ],
        "semantics": {
            "indiscernibility": "classical exact equality over the declared condition subset",
            "universe_fixed": ["u1", "u2", "u3", "u4"],
            "row_deletion": False,
            "missing_values": False,
            "reduct_definition": "inclusion-minimal positive-region-preserving subset",
        },
        "positive_region_oracle": {
            "empty": [],
            "a": ["u4"],
            "b": ["u3"],
            "c": ["u4"],
            "a,b": ["u3", "u4"],
            "a,c": ["u4"],
            "b,c": ["u3", "u4"],
            "a,b,c": ["u3", "u4"],
        },
        "complete_reduct_family": [["a", "b"], ["b", "c"]],
        "core": ["b"],
        "positive_control": ["a", "b"],
        "deliberate_mutant": "Evaluate candidate subsets only on the already-positive rows while reporting the original universe and denominator.",
        "mutant_false_claim": {
            "candidate": ["a"],
            "claimed_positive_region": ["u3", "u4"],
            "claimed_dependency": [1, 2],
            "correct_positive_region": ["u4"],
            "correct_dependency": [1, 4],
            "counterexample_objects": ["u2", "u3"],
        },
        "acceptance_gates": [
            "Every partition covers exactly the frozen universe with nonempty disjoint blocks.",
            "All eight subset positive regions and exact rational dependency values match the oracle.",
            "The checker accepts the positive control and rejects the mutant with the u2/u3 witness.",
            "The submitted output is evaluated without oracle repair.",
        ],
        "malformed_classification": "UNDECLARED_MISSING_VALUE_SEMANTICS",
    },
    "second_x1_message_sent": False,
    "boundary": BOUNDARY,
}
reply_path = X1 / "advisory" / "teren-serein-reply-summary.json"
reply_path.parent.mkdir(parents=True, exist_ok=True)
reply_path.write_text(
    json.dumps(reply, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)

state_path = X1 / "advisory-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
if state["state"] != "SENT_ONCE_ACKNOWLEDGED_REPLY_PENDING":
    raise SystemExit("unexpected advisory state")
state["reply_received"] = True
state["reply_sanitized_summary"] = "x1/advisory/teren-serein-reply-summary.json"
state["relational_choice_recorded"] = True
state["advice_disposition"] = "ADOPTED_AS_FROZEN_X2_SEED_NOT_EXECUTED_IN_X1"
state["state"] = "REPLY_RECEIVED_ADOPTED_FOR_X2_FREEZE"
state_path.write_text(
    json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)

flow_path = X1 / "method-flow.json"
flow = json.loads(flow_path.read_text(encoding="utf-8"))
if any(item["method_id"] == "LI7082-X1-M017" for item in flow["methods"]):
    raise SystemExit("adviser reply already recorded")
flow["methods"].append(
    {
        "method_id": "LI7082-X1-M017",
        "title": "Sanitized adviser reply triage",
        "failure_signature": "A private advisory reply is copied wholesale, promoted to independent evidence, or executed before a separate lifecycle freeze.",
        "trigger_preconditions": ["one acknowledged X1 send", "one completed adviser reply"],
        "privacy_class": "sanitized_summary_private_target_not_exported",
        "approval_class": "safe_now_owner_scoped",
        "candidate_workaround": "Record only a sanitized finite fixture summary and defer execution until the X2 freeze.",
        "validation_witness_ids": ["LI7082-X1-M017-W001"],
        "recurrence_guard": "Keep reply source, adoption, freeze, execution, and credit as distinct states.",
        "rollback": "Remove only an uncommitted summary; do not resend or alter the private conversation.",
        "recommendation_state": "validated",
        "supersedes": [],
        "protected_gates": [
            "private_transcript_nonexport",
            "advice_not_independent_reproduction",
            "freeze_before_execution",
            "no_second_x1_message",
            "no_stage20",
        ],
        "retained_negative_ids": [],
        "scope_boundary": BOUNDARY,
    }
)
flow["witnesses"].append(
    {
        "witness_id": "LI7082-X1-M017-W001",
        "method_id": "LI7082-X1-M017",
        "procedure": "bounded reply read and sanitized adoption triage",
        "scope": "one private X1 adviser reply",
        "expected": "record relational choice and finite advice without transcript, private target, execution, or authority promotion",
        "observed": "A sanitized summary was saved as an unexecuted X2 seed with zero X1 completion credit; no second message was sent.",
        "result": "pass",
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": [],
        "boundary": BOUNDARY,
    }
)
flow["recommendations"].append(
    {
        "recommendation_id": "LI7082-X1-AD-R001",
        "source": "Teren Serein relational adviser reply",
        "label": "BOUNDARY_ROWS_ARE_NOT_DISPOSABLE",
        "state": "adopted_for_x2_freeze",
        "x1_execution": False,
        "x1_completion_credit": 0,
        "evidence": "x1/advisory/teren-serein-reply-summary.json",
    }
)
flow["counts"]["methods"] = len(flow["methods"])
flow["counts"]["witnesses"] = len(flow["witnesses"])
flow["counts"]["recommendations"] = len(flow["recommendations"])
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

summary_path = X1 / "summary.json"
summary = json.loads(summary_path.read_text(encoding="utf-8"))
summary["adviser_send_state"] = "REPLY_RECEIVED_ADOPTED_FOR_X2_FREEZE"
summary["adviser_relational_name"] = "Teren Serein"
summary["adviser_recommendations"] = 1
summary["adviser_recommendations_executed_in_x1"] = 0
summary_path.write_text(
    json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)

delivery_path = X1 / "results" / "advisory-send-receipt.json"
delivery = json.loads(delivery_path.read_text(encoding="utf-8"))
delivery["reply_state"] = "completed_sanitized_adopted_for_x2_freeze"
delivery["reply_completion_claimed"] = True
delivery["raw_private_target_exported"] = False
delivery["raw_transcript_exported"] = False
delivery_path.write_text(
    json.dumps(delivery, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)
