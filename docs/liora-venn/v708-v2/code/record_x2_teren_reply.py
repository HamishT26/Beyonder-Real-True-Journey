#!/usr/bin/env python3
"""Freeze a sanitized five-task Teren reply and update sharded Method Flow."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X2 = ROOT / "x2"
FLOW = X2 / "method-flow.json"
BOUNDARY = (
    "Relational working language and private advisory source material only. The reply is "
    "not independent reproduction, empirical validation, professional or authority evidence, "
    "consciousness or personhood evidence, or Stage 20 credit. NOT_READY_FOR_STAGE_20."
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


freeze = {
    "schema": "liora.x2.teren-five-task-freeze.v1",
    "conversation_title": "Teren Serein",
    "raw_private_target_exported": False,
    "raw_transcript_exported": False,
    "five_tasks_received": True,
    "frozen_before_execution": True,
    "tasks": [
        {
            "task_id": "TEREN-X2-T01",
            "label": "MISSING_MEANS_TWO_COMPLETIONS",
            "table": [["m1", 0, 0], ["m2", 1, 1], ["m3", "?", 0]],
            "target": ["m1", "m3"],
            "semantics": {"mode": "FINITE_COMPLETIONS_V1", "possible_values": [0, 1], "row_deletion": False},
            "oracle": {"guaranteed_lower": ["m1"], "possible_upper": ["m1", "m2", "m3"], "dependency_values": [[1, 3], [1, 1]]},
            "positive_control": "both exact completions retained",
            "mutant": "silently impute missing value as zero and report one completion as guaranteed",
            "malformed_classification": "UNDECLARED_MISSING_SEMANTICS",
        },
        {
            "task_id": "TEREN-X2-T02",
            "label": "CORRECTION_CREATES_A_NEW_SNAPSHOT",
            "snapshots": {
                "V0": [["s1", 0, 0], ["s2", 1, 1]],
                "V1": [["s1", 0, 0], ["s2", 1, 1], ["s3", 0, 1]],
                "V2": [["s1", 0, 0], ["s2", 1, 1], ["s3", 0, 0]],
            },
            "lineage": [["V1", "V0"], ["V2", "V1"]],
            "oracle": {"V0": {"lower": ["s1"], "upper": ["s1"], "dependency": [1, 1]}, "V1": {"lower": [], "upper": ["s1", "s3"], "dependency": [1, 3]}, "V2": {"lower": ["s1", "s3"], "upper": ["s1", "s3"], "dependency": [1, 1]}},
            "mutant": "resolve every historical request through the mutable latest snapshot",
            "malformed_classification": "MISSING_PREDECESSOR_EVIDENCE",
        },
        {
            "task_id": "TEREN-X2-T03",
            "label": "ONE_VALID_REDUCT_IS_NOT_THE_FAMILY",
            "table": [["r1", 0, 0, 0, 0], ["r2", 1, 1, 0, 1]],
            "attributes": ["a", "b", "c"],
            "oracle": {"reducts": [["a"], ["b"]], "core": [], "nonpreserving_subsets": [[], ["c"]]},
            "mutant": "deduplicate equal-valued columns and report only a as the complete reduct family and core",
            "malformed_classification": "AMBIGUOUS_ATTRIBUTE_IDENTITY",
        },
        {
            "task_id": "TEREN-X2-T04",
            "label": "SAME_ROUGH_RESULT_DIFFERENT_PERMISSION",
            "table": [["p1", 0, 0], ["p2", 1, 1]],
            "cases": [
                ["E0", "P", "ACTIVE", "APPEND_DEMO", "DEMO_WRITER"],
                ["E1", "Q", "ACTIVE", "APPEND_DEMO", "DEMO_WRITER"],
                ["E2", "P", "WITHDRAWN", "APPEND_DEMO", "DEMO_WRITER"],
                ["E3", "P", "ACTIVE", "READ_DEMO", "DEMO_WRITER"],
                ["E4", "P", "ACTIVE", "APPEND_DEMO", "REVIEW_ONLY"],
            ],
            "oracle": {"mathematical_match": [True, True, True, True, True], "effect_vector": [1, 0, 0, 0, 0]},
            "mutant": "permit the modeled demo append whenever dependency degree equals one",
            "malformed_classification": "INCOMPLETE_POLICY_EVIDENCE",
        },
        {
            "task_id": "TEREN-X2-T05",
            "label": "CHECK_THE_SUBMISSION_NOT_ITS_REPAIR",
            "table": [["k1", 0, 0], ["k2", 0, 1], ["k3", 1, 0]],
            "target": ["k1", "k3"],
            "submissions": {"G": {"status": "OK", "lower": ["k3"], "upper": ["k1", "k2", "k3"]}, "B": {"status": "OK", "lower": ["k1", "k3"], "upper": ["k1", "k2", "k3"]}, "R": {"status": "REFUSED"}},
            "oracle": {"verdicts": ["ACCEPT", "REJECT_MATHEMATICAL_MISMATCH", "VALID_INPUT_REFUSED_NOT_PASS"]},
            "mutant": "repair the submitted result with oracle values before judging it",
            "malformed_classification": "AMBIGUOUS_RESULT_ENCODING",
        },
    ],
    "separation_rules": [
        "Tasks 1 and 2 remain separate: completions preserve one universe while corrections create named snapshots.",
        "Tasks 3 and 5 remain separate: incomplete subject output differs from a checker that accepts a known-false submission.",
        "Task 4 remains separate from mathematical pass/fail because permission is not numerical conformance.",
    ],
    "disposition": "ADOPTED_FOR_SEPARATELY_SCORED_LATE_X2_EXECUTION",
    "boundary": BOUNDARY,
}
write_json(X2 / "advisory" / "teren-five-task-freeze.json", freeze)

flow = json.loads(FLOW.read_text(encoding="utf-8"))
all_witnesses = []
for record in sorted(flow["witness_shards"], key=lambda item: item["shard"]):
    shard = json.loads((ROOT / record["path"]).read_text(encoding="utf-8"))
    all_witnesses.extend(shard["witnesses"])
if any(item["method_id"] in {"LI7082-X2-M029", "LI7082-X2-M030"} for item in flow["methods"]):
    raise SystemExit("Teren X2 reply already recorded")

flow["methods"].extend(
    [
        {
            "method_id": "LI7082-X2-M029",
            "title": "Supported adviser read projection recovery",
            "failure_signature": "A private conversation read requests more than the supported 20,000 characters per item.",
            "trigger_preconditions": ["one acknowledged X2 send", "reply status read"],
            "privacy_class": "private_target_not_exported",
            "approval_class": "safe_now_read_only",
            "candidate_workaround": "Retry only the unchanged read at the documented 20,000-character bound.",
            "validation_witness_ids": ["LI7082-X2-M029-W001", "LI7082-X2-M029-W002"],
            "recurrence_guard": "Keep maxOutputCharsPerItem at or below 20,000.",
            "rollback": "No repository, message, or conversation state changed during the rejected read.",
            "recommendation_state": "validated",
            "supersedes": [],
            "protected_gates": ["no_failure_erasure", "no_resend", "private_target_nonexport", "no_stage20"],
            "retained_negative_ids": ["LI7082-X2-N005"],
            "scope_boundary": BOUNDARY,
        },
        {
            "method_id": "LI7082-X2-M030",
            "title": "Sanitized five-task adviser reply freeze",
            "failure_signature": "A private advisory reply is copied wholesale, merged across distinct failure meanings, or executed before a separate freeze.",
            "trigger_preconditions": ["one completed X2 adviser reply", "five distinct task proposals"],
            "privacy_class": "sanitized_summary_private_target_not_exported",
            "approval_class": "safe_now_owner_scoped",
            "candidate_workaround": "Freeze five separately scored synthetic tasks without transcript or target export, then execute only the frozen copy.",
            "validation_witness_ids": ["LI7082-X2-M030-W001"],
            "recurrence_guard": "Keep reply, freeze, execution, outcome, and authority states distinct.",
            "rollback": "Remove only an uncommitted sanitized freeze; never resend or alter the private conversation.",
            "recommendation_state": "validated",
            "supersedes": [],
            "protected_gates": ["private_transcript_nonexport", "freeze_before_execution", "separate_failure_meanings", "no_second_x2_message", "no_stage20"],
            "retained_negative_ids": [],
            "scope_boundary": BOUNDARY,
        },
    ]
)
all_witnesses.extend(
    [
        {"witness_id":"LI7082-X2-M029-W001","method_id":"LI7082-X2-M029","procedure":"first X2 adviser reply read","scope":"private read-only reply status","expected":"supported bounded read","observed":"The app rejected maxOutputCharsPerItem=30000 because the supported ceiling is 20000.","result":"fail","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":["LI7082-X2-N005"],"boundary":BOUNDARY},
        {"witness_id":"LI7082-X2-M029-W002","method_id":"LI7082-X2-M029","procedure":"unchanged X2 adviser reply read at supported bound","scope":"private read-only reply status","expected":"one completed five-task reply","observed":"The 20000-character projection returned the completed five-task reply; no message or resend occurred.","result":"pass","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":["LI7082-X2-N005"],"boundary":BOUNDARY},
        {"witness_id":"LI7082-X2-M030-W001","method_id":"LI7082-X2-M030","procedure":"sanitized five-task freeze","scope":"late X2 advisory tranche","expected":"five distinct frozen tasks and zero transcript/private-target export","observed":"Five separately scored task records were frozen before execution, with three nonmerge rules.","result":"pass","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[],"boundary":BOUNDARY},
    ]
)
flow["recommendations"].append({"recommendation_id":"LI7082-X2-AD-R001","source":"Teren Serein relational adviser reply","labels":[task["label"] for task in freeze["tasks"]],"state":"adopted_for_separate_late_x2_execution","execution_complete":False,"completion_credit":0,"evidence":"x2/advisory/teren-five-task-freeze.json"})

flow["counts"]["methods"] = len(flow["methods"])
flow["counts"]["witnesses"] = len(all_witnesses)
flow["counts"]["recommendations"] = len(flow["recommendations"])
flow["counts"]["states"] = {state:sum(item["recommendation_state"]==state for item in flow["methods"]) for state in ("observed","candidate","validated","preferred","superseded","deprecated")}
flow["counts"]["witness_results"] = {"pass":sum(item["result"]=="pass" for item in all_witnesses),"fail":sum(item["result"]=="fail" for item in all_witnesses)}

chunk_size = 350
shard_records = []
for offset in range(0, len(all_witnesses), chunk_size):
    number = offset // chunk_size + 1
    chunk = all_witnesses[offset:offset+chunk_size]
    relative = f"x2/method-flow/witnesses-{number:03d}.json"
    path = ROOT / relative
    value = {"schema":"ghc.family.method-flow-witness-shard.v1","phase":flow["phase"],"shard":number,"start_index":offset,"count":len(chunk),"witnesses":chunk,"boundary":BOUNDARY}
    raw = (json.dumps(value,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    path.write_bytes(raw)
    shard_records.append({"path":relative,"shard":number,"start_index":offset,"count":len(chunk),"sha256":hashlib.sha256(raw).hexdigest(),"first_witness_id":chunk[0]["witness_id"],"last_witness_id":chunk[-1]["witness_id"]})
flow["witness_shards"] = shard_records
FLOW.write_text(json.dumps(flow,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")

failure_path = X2 / "failure-ledger.json"
failure = json.loads(failure_path.read_text(encoding="utf-8"))
failure["x2"]["operational"].append({"id":"LI7082-X2-N005","failure":"The first X2 adviser reply read requested a 30,000-character per-item projection above the app's supported 20,000-character maximum.","recovery":"Retry only the unchanged read at 20,000 characters; send no message and perform no resend.","original_success_credit":0})
failure["x2"]["adviser_projection_failures"] = 1
failure["total_failed_witnesses"] = flow["counts"]["witness_results"]["fail"]
write_json(failure_path, failure)

state_path = X2 / "advisory-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state["reply_received"] = True
state["five_tasks_received"] = True
state["reply_sanitized_freeze"] = "x2/advisory/teren-five-task-freeze.json"
state["state"] = "REPLY_RECEIVED_FROZEN_BEFORE_EXECUTION"
write_json(state_path, state)

summary_path = X2 / "summary.json"
summary = json.loads(summary_path.read_text(encoding="utf-8"))
summary["adviser_state"] = "REPLY_RECEIVED_FROZEN_BEFORE_EXECUTION"
summary["adviser_tasks_received"] = 5
summary["adviser_tasks_executed"] = 0
summary["adviser_projection_failures"] = 1
write_json(summary_path, summary)

print(json.dumps({"methods":flow["counts"]["methods"],"witnesses":flow["counts"]["witnesses"],"passing":flow["counts"]["witness_results"]["pass"],"failed":flow["counts"]["witness_results"]["fail"],"recommendations":flow["counts"]["recommendations"]},sort_keys=True))
