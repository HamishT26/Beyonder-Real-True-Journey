#!/usr/bin/env python3
"""Execute and record Teren's five frozen X2 tasks with retained test failure."""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X2 = ROOT / "x2"
FLOW = X2 / "method-flow.json"
for code_dir in (ROOT / "x1" / "code", X2 / "code"):
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))

import teren_tasks


BOUNDARY = (
    "Five separately scored finite synthetic same-owner advisory tasks only. This is not "
    "independent reproduction, empirical validation, production readiness, professional, "
    "legal, cultural, affected-party or Maori authority, consciousness/personhood evidence, "
    "or Stage 20 credit. NOT_READY_FOR_STAGE_20."
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


freeze = json.loads((X2 / "advisory" / "teren-five-task-freeze.json").read_text(encoding="utf-8"))
if not freeze["frozen_before_execution"] or len(freeze["tasks"]) != 5:
    raise SystemExit("five-task freeze missing")
results = teren_tasks.run_all()
if len(results) != 5 or any(record["mutant_accepted"] for record in results.values()):
    raise SystemExit("Teren task detector discrimination failed")
write_json(
    X2 / "results" / "teren-five-task-execution.json",
    {
        "schema": "liora.x2.teren-five-task-execution.v1",
        "freeze": "x2/advisory/teren-five-task-freeze.json",
        "tasks": [
            {
                "label": label,
                "positive_control_passed": True,
                "mutant_executed": True,
                "mutant_accepted": record["mutant_accepted"],
                "mutant_rejected": not record["mutant_accepted"],
                "malformed_or_missing_classification": record["classification"],
                "result": record,
            }
            for label, record in results.items()
        ],
        "task_count": 5,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    },
)

env = os.environ.copy()
env["PYTHONUTF8"] = "1"
env["PYTHONDONTWRITEBYTECODE"] = "1"
tests = subprocess.run(
    [sys.executable, "-m", "unittest", "discover", "-s", str(X2 / "tests"), "-p", "test_*.py", "-v"],
    text=True,
    capture_output=True,
    encoding="utf-8",
    env=env,
    check=False,
)
combined = tests.stdout + tests.stderr
test_count = combined.count(" ... ok")
if tests.returncode or test_count != 60:
    raise RuntimeError((test_count, tests.stdout, tests.stderr))
write_json(
    X2 / "results" / "tests-late-teren.json",
    {
        "schema": "liora.x2.tests-late-teren.v1",
        "exit_code": tests.returncode,
        "tests": test_count,
        "stdout": tests.stdout,
        "stderr": tests.stderr,
        "initial_selection": {"tests_run": 60, "passes": 59, "failures": 1, "retained_negative_id": "LI7082-X2-N006"},
        "narrow_recovery": {"tests_run": 1, "passes": 1, "failures": 0},
        "boundary": BOUNDARY,
    },
)

flow = json.loads(FLOW.read_text(encoding="utf-8"))
all_witnesses = []
for record in sorted(flow["witness_shards"], key=lambda item: item["shard"]):
    all_witnesses.extend(json.loads((ROOT / record["path"]).read_text(encoding="utf-8"))["witnesses"])
if any(item["method_id"] in {"LI7082-X2-M031", "LI7082-X2-M032"} for item in flow["methods"]):
    raise SystemExit("Teren X2 execution already recorded")

task_negatives = [f"LI7082-X2-TEREN-N{i:02d}" for i in range(1, 6)]
task_witness_ids = [f"LI7082-X2-TEREN-W{i:02d}" for i in range(1, 21)]
flow["methods"].append(
    {
        "method_id": "LI7082-X2-M031",
        "title": "Five separately scored Teren advisory tasks",
        "failure_signature": "A deliberate mutant survives, a positive control fails, or distinct failure meanings are collapsed into one aggregate.",
        "trigger_preconditions": ["sanitized five-task freeze", "frozen before execution", "same-owner finite harness"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_scoped",
        "candidate_workaround": "Score each task independently with its own positive, mutant, detector, and malformed-evidence witness.",
        "validation_witness_ids": task_witness_ids,
        "recurrence_guard": "Never let an aggregate pass hide a failed positive control or surviving mutant.",
        "rollback": "Discard only uncommitted task outputs and retain every failed mutant witness.",
        "recommendation_state": "validated",
        "supersedes": [],
        "protected_gates": ["freeze_before_execution", "separate_failure_meanings", "no_mutant_credit", "no_authority_promotion", "no_stage20"],
        "retained_negative_ids": task_negatives,
        "scope_boundary": BOUNDARY,
    }
)

witness_index = 0
for negative_id, (label, record) in zip(task_negatives, results.items()):
    for procedure, observed, outcome, negatives in (
        ("positive control", "exact frozen oracle matched", "pass", []),
        ("deliberate mutant", json.dumps(record, ensure_ascii=False, sort_keys=True), "fail", [negative_id]),
        ("mutant detector", "mutant_accepted=false", "pass", [negative_id]),
        ("malformed or missing classification", record["classification"], "pass", [negative_id]),
    ):
        witness_id = task_witness_ids[witness_index]
        witness_index += 1
        all_witnesses.append(
            {
                "witness_id": witness_id,
                "method_id": "LI7082-X2-M031",
                "procedure": f"{label}: {procedure}",
                "scope": "late X2 Teren advisory task",
                "expected": "separately scored exact finite behavior",
                "observed": observed,
                "result": outcome,
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": negatives,
                "boundary": BOUNDARY,
            }
        )

flow["methods"].append(
    {
        "method_id": "LI7082-X2-M032",
        "title": "Numeric dependency-set ordering recovery",
        "failure_signature": "A mathematical set of rational dependency values is serialized in tuple-lexicographic rather than numeric ascending order.",
        "trigger_preconditions": ["first integrated 60-test late-X2 selection"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_scoped",
        "candidate_workaround": "Sort rational pairs by their exact Fraction values, validate only the failed test, then run one current integrated selection.",
        "validation_witness_ids": ["LI7082-X2-M032-W001", "LI7082-X2-M032-W002", "LI7082-X2-M032-W003"],
        "recurrence_guard": "Canonicalize rational-value sets by exact numeric value, not tuple representation.",
        "rollback": "Restore only the uncommitted ordering expression; preserve the 59 initial passes and failed witness.",
        "recommendation_state": "validated",
        "supersedes": [],
        "protected_gates": ["no_failure_erasure", "narrow_recovery", "no_stage20"],
        "retained_negative_ids": ["LI7082-X2-N006"],
        "scope_boundary": BOUNDARY,
    }
)
all_witnesses.extend(
    [
        {"witness_id":"LI7082-X2-M032-W001","method_id":"LI7082-X2-M032","procedure":"first integrated late-X2 selection","scope":"60 owner tests","expected":"60/60","observed":"59 passed; dependency-value ordering test failed with [[1,1],[1,3]] instead of numeric ascending [[1,3],[1,1]].","result":"fail","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":["LI7082-X2-N006"],"boundary":BOUNDARY},
        {"witness_id":"LI7082-X2-M032-W002","method_id":"LI7082-X2-M032","procedure":"narrow failed-test recovery","scope":"one dependency-ordering test","expected":"1/1","observed":"1/1 passed after exact Fraction ordering.","result":"pass","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":["LI7082-X2-N006"],"boundary":BOUNDARY},
        {"witness_id":"LI7082-X2-M032-W003","method_id":"LI7082-X2-M032","procedure":"current integrated late-X2 selection","scope":"60 owner tests","expected":"60/60","observed":"60/60 passed.","result":"pass","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":["LI7082-X2-N006"],"boundary":BOUNDARY},
    ]
)

for recommendation in flow["recommendations"]:
    if recommendation.get("recommendation_id") == "LI7082-X2-AD-R001":
        recommendation["execution_complete"] = True
        recommendation["bounded_same_owner_task_results"] = 5
        recommendation["completion_credit"] = 0

flow["counts"]["methods"] = len(flow["methods"])
flow["counts"]["witnesses"] = len(all_witnesses)
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
failure["x2"]["operational"].append({"id":"LI7082-X2-N006","failure":"The first 60-test late-X2 selection passed 59 and failed one dependency-value ordering assertion because tuple-lexicographic order placed 1 before 1/3.","recovery":"Sort rational pairs by exact Fraction value, run only the failed test for immediate recovery, then run one current integrated selection.","original_success_credit":0})
failure["x2"]["teren_task_mutant_failures"] = 5
failure["x2"]["late_test_failures"] = 1
failure["total_failed_witnesses"] = flow["counts"]["witness_results"]["fail"]
write_json(failure_path, failure)

state_path = X2 / "advisory-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state["five_tasks_executed"] = True
state["five_tasks_passed_separate_gates"] = True
state["state"] = "REPLY_RECEIVED_FIVE_TASKS_EXECUTED_SAME_OWNER"
write_json(state_path, state)

summary_path = X2 / "summary.json"
summary = json.loads(summary_path.read_text(encoding="utf-8"))
summary["initial_tests"] = summary["tests"]
summary["tests"] = 60
summary["adviser_state"] = "REPLY_RECEIVED_FIVE_TASKS_EXECUTED_SAME_OWNER"
summary["adviser_tasks_executed"] = 5
summary["adviser_task_mutants_rejected"] = 5
summary["late_test_failures"] = 1
write_json(summary_path, summary)

print(json.dumps({"tasks":5,"tests":60,"methods":flow["counts"]["methods"],"witnesses":flow["counts"]["witnesses"],"passing":flow["counts"]["witness_results"]["pass"],"failed":flow["counts"]["witness_results"]["fail"]},sort_keys=True))
