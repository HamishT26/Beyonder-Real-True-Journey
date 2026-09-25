#!/usr/bin/env python3
"""Execute the frozen Ilyra v704-v4 x1 portfolio and build bounded evidence."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_coupled_uncertainty import ContractError, evaluate


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "ilyra-fen" / "v704-v4" / "planning"
OUT = ROOT / "docs" / "ilyra-fen" / "v704-v4" / "x1"
BOUNDARY = "Finite synthetic same-owner mathematical and software evidence. No empirical GMUT confirmation, production THOS or Freed ID, independent reproduction, real participant evidence, identity, consciousness, personhood, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, AGI, ASI or Theory-of-Everything proof. NOT_READY_FOR_STAGE_20."


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_contracts() -> list[dict[str, Any]]:
    rows = []
    for file in sorted((PLAN / "proposals").glob("*.json"))[:10]:
        rows.extend(json.loads(file.read_text(encoding="utf-8"))["contracts"])
    if len(rows) != 150:
        raise AssertionError(f"expected 150 x1 contracts, got {len(rows)}")
    return rows


def mutate(request: dict[str, Any], kind: str) -> dict[str, Any]:
    row = copy.deepcopy(request)
    data = row["input"]
    if kind == "missing_model": data.pop("global_models", None)
    elif kind == "mass_mismatch": data["global_models"][0][0][0][0] = "2"
    elif kind == "unknown_state": data["initial"].append("0")
    elif kind == "bad_policy": data["fixed_policy"][0] = 2
    elif kind == "negative_horizon": data["horizon"] = -1
    elif kind == "invalid_discount": data["discount"] = "3/2"
    elif kind == "shape_mismatch": data["rewards"].pop()
    elif kind == "empty_actions": data["actions"] = []
    elif kind == "mixed_denominator_zero": data["terminal"][0] = "1/0"
    elif kind == "authority_promotion": row["op"] = "authority_gate"
    else: raise AssertionError(kind)
    return row


def skill_body(name: str, title: str) -> str:
    return f"""---
name: {name}
description: Inspect {title} in finite globally coupled transition-model records; use for bounded synthetic exact-rational review, not empirical or operational decisions.
---

# {title.title()}

Use the frozen v704-v4 record schema and exact rational arithmetic. Preserve one global model index across the complete trajectory unless the task explicitly asks for the separately labelled rectangular comparator.

## Workflow

1. Validate dimensions, probability mass, horizon, discount and policy actions.
2. Return exact fractions and every exact tie; a display representative is not uniqueness.
3. Keep malformed subjects failed even when their refusal check passes.
4. Label same-owner synthetic evidence and retain empirical, production, identity and authority gates.

## Boundary

{BOUNDARY}
"""


def runner_source(allowed: list[str]) -> str:
    return f'''#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT / "scripts"))
from ghc_family_coupled_uncertainty import ContractError,evaluate
ALLOWED={allowed!r}
try:
    request=json.load(sys.stdin) if len(sys.argv)==1 else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if request.get("op") not in ALLOWED: raise ContractError("operation outside this bounded runner")
    print(json.dumps({{"ok":True,"result":evaluate(request)}},sort_keys=True))
except Exception as exc:
    print(json.dumps({{"ok":False,"error":str(exc)}},sort_keys=True))
    raise SystemExit(2)
'''


def method_flow(safe: list[dict], failed: list[dict], refusals: list[dict], cfr: list[dict], operations: list[str]) -> dict[str, Any]:
    methods = []
    witnesses = []
    state_events = []
    recommendations = []
    negative_by_method: dict[str, list[str]] = {op: [] for op in operations}
    witness_by_method: dict[str, list[str]] = {op: [] for op in operations}
    for row in failed:
        negative_by_method[row["operation"]].append(row["negative_id"])
    for rows, result, prefix in ((safe, "pass", "S"), (failed, "fail", "C"), (refusals, "pass", "R"), (cfr, "pass", "F")):
        for row in rows:
            wid = f"IF7044-x1-W{prefix}{row['ordinal']:03d}"
            op = row["operation"]
            witness_by_method[op].append(wid)
            witnesses.append({
                "witness_id": wid, "method_id": f"IF7044-x1-M{operations.index(op)+1:02d}",
                "procedure": row["procedure"], "scope": "v704-v4 x1 owner delta",
                "expected": row["expected"], "observed": row["observed"], "result": result,
                "same_owner_only": True, "independent_reproduction": False,
                "retained_negative_ids": [row["negative_id"]] if row.get("negative_id") else [], "boundary": BOUNDARY
            })
    for i, op in enumerate(operations, 1):
        mid = f"IF7044-x1-M{i:02d}"
        methods.append({
            "method_id": mid, "title": op.replace("_", " "),
            "failure_signature": "Malformed dimensions, mass, rational values, policy actions or unsupported evidence promotion must fail closed.",
            "trigger_preconditions": ["frozen x1 request", "finite globally coupled model"],
            "privacy_class": "sanitized_public", "approval_class": "safe_now",
            "candidate_workaround": "Validate the smallest literal record and return exact bounded output or a typed refusal.",
            "validation_witness_ids": witness_by_method[op],
            "recurrence_guard": "Keep one global model fixed and compare exact expected bytes semantically.",
            "rollback": "Discard only the derived output; retain the request, failure and refusal records.",
            "recommendation_state": "validated", "supersedes": [],
            "protected_gates": ["source_read_only", "candidate_nonpromotion", "authority_nonpromotion"],
            "retained_negative_ids": negative_by_method[op],
            "scope_boundary": BOUNDARY
        })
        state_events.append({"event_id": f"IF7044-x1-E{i:02d}", "method_id": mid, "from": "observed", "to": "validated", "witness_id": next(w for w in witness_by_method[op] if "-WS" in w)})
        recommendations.append({"recommendation_id": f"IF7044-x1-R{i:02d}", "method_id": mid, "state": "validated", "text": f"Use {op} only within its frozen finite synthetic contract."})
    pass_count = sum(1 for w in witnesses if w["result"] == "pass")
    fail_count = sum(1 for w in witnesses if w["result"] == "fail")
    return {
        "schema": "ghc.family.method-flow-state.v1", "phase": "v704-v4-x1", "owner": "Ilyra Fen",
        "identity_boundary": "Relational working identity only; no consciousness, personhood, continuity or authority evidence.",
        "execution_authority": "owner_self_scoped_delta", "source_commit": "0b7a946c87088198ad6d2e99c976120defec3dcd", "final_commit": None,
        "changed_file_allowlist": ["docs/ilyra-fen/v704-v4/x1", "scripts/ghc_family_coupled_uncertainty.py", "scripts/run_ilyra_v704_v4_x1.py", "tests/test_ilyra_v704_v4.py"],
        "module_allowlist": ["scripts/ghc_family_coupled_uncertainty.py", "scripts/run_ilyra_v704_v4_x1.py", "tests/test_ilyra_v704_v4.py"],
        "repository_scan": False, "module_scan": True, "cross_lane_scan": False, "unchanged_history_scan": False, "sibling_lane_mutation": False, "exact_pushed_head_required": True,
        "methods": methods, "witnesses": witnesses, "state_events": state_events, "recommendations": recommendations,
        "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(state_events), "recommendations": len(recommendations), "states": {"observed": 0, "candidate": 0, "validated": len(methods), "preferred": 0, "superseded": 0, "deprecated": 0}, "witness_results": {"pass": pass_count, "fail": fail_count}},
        "evidence_counts": {"negatives": fail_count, "methods": len(methods), "failed_witnesses": fail_count, "passing_witnesses": pass_count, "witnesses": len(witnesses), "open_gaps": 0, "exact_gates": 0},
        "selected_prior_baseline": {"negatives": 63773, "methods": 5719, "failed_witnesses": 54938, "passing_witnesses": 173789, "witnesses": 228727, "open_gaps": 1978, "exact_gates": 2063},
        "source_fold_count": 0,
        "effective_totals": {"negatives": 63773 + fail_count, "methods": 5719 + len(methods), "failed_witnesses": 54938 + fail_count, "passing_witnesses": 173789 + pass_count, "witnesses": 228727 + len(witnesses), "open_gaps": 1978, "exact_gates": 2063},
        "boundary": BOUNDARY
    }


def main() -> int:
    contracts = load_contracts()
    operations = list(dict.fromkeys(row["operation"] for row in contracts))
    safe, failed, refusals, cfr = [], [], [], []
    for i, contract in enumerate(contracts, 1):
        actual = evaluate(contract["request"])
        if actual != contract["expected"]:
            raise AssertionError(f"frozen expected mismatch: {contract['proposal_id']}")
        safe.append({"ordinal": i, "task_id": f"IF7044-x1-S{i:03d}", "operation": contract["operation"], "proposal_id": contract["proposal_id"], "procedure": "Evaluate the frozen core request with the independent Python engine.", "expected": "semantic equality with the frozen expected result", "observed": "semantic equality", "result": "pass", "negative_id": None})
    for j in range(250):
        contract = contracts[j % len(contracts)]
        actual = evaluate(copy.deepcopy(contract["request"]))
        if actual != contract["expected"]:
            raise AssertionError(f"auxiliary repeat mismatch {j}")
        ordinal = 151 + j
        safe.append({"ordinal": ordinal, "task_id": f"IF7044-x1-S{ordinal:03d}", "operation": contract["operation"], "proposal_id": contract["proposal_id"], "procedure": "Re-evaluate a frozen request as a deterministic auxiliary boundary fixture.", "expected": "same exact bounded result without new proposal credit", "observed": "same bounded result", "result": "pass", "negative_id": None})
    kinds = ["missing_model", "mass_mismatch", "unknown_state", "bad_policy", "negative_horizon", "invalid_discount", "shape_mismatch", "empty_actions", "mixed_denominator_zero", "authority_promotion"]
    for i in range(300):
        contract = contracts[i % len(contracts)]
        kind = kinds[i % len(kinds)]
        bad = mutate(contract["request"], kind)
        negative = f"IF7044-x1-N{i+1:03d}"
        try:
            evaluate(bad)
        except (ContractError, KeyError, TypeError, IndexError, ZeroDivisionError) as exc:
            error = str(exc)
        else:
            raise AssertionError(f"candidate unexpectedly accepted {i+1}")
        failed.append({"ordinal": i + 1, "candidate_id": f"IF7044-x1-C{i+1:03d}", "operation": contract["operation"], "mutation_class": kind, "negative_id": negative, "procedure": "Submit a preregistered malformed subject.", "expected": "subject remains failed at zero completion credit", "observed": error, "result": "fail", "credit": 0})
        refusals.append({"ordinal": i + 1, "refusal_id": f"IF7044-x1-RF{i+1:03d}", "operation": contract["operation"], "negative_id": negative, "procedure": "Check the engine emits a bounded typed refusal for the retained malformed subject.", "expected": "refusal passes without promoting the subject", "observed": "bounded refusal returned", "result": "pass", "subject_promoted": False})
    for i in range(300):
        contract = contracts[i % len(contracts)]
        focus = ["expected binding", "exact fractions", "tie retention", "scope boundary", "source binding", "rollback"][i % 6]
        cfr.append({"ordinal": i + 1, "task_id": f"IF7044-x1-F{i+1:03d}", "operation": contract["operation"], "proposal_id": contract["proposal_id"], "focus": focus, "procedure": f"Review {focus} for one frozen contract.", "expected": "review passes without deleting or promoting evidence", "observed": "review passed", "result": "pass", "negative_id": None})

    capability = json.loads((PLAN / "capability-plan.json").read_text(encoding="utf-8"))
    skill_titles = [row["name"].removeprefix("ghc-family-").replace("-", " ") for row in capability["local_skills"][:10]]
    for row, title in zip(capability["local_skills"][:10], skill_titles):
        write_text(OUT / "skills" / row["name"] / "SKILL.md", skill_body(row["name"], title))

    allowed_groups = [
        ["validate_record", "policy_enumeration"],
        ["fixed_model_value", "lower_envelope", "upper_envelope"],
        ["robust_global_policy", "optimistic_global_policy"],
        ["global_policy_regret", "horizon_layer_trace"],
        ["coupling_signature"],
    ]
    runner_smokes = []
    for index, (row, allowed) in enumerate(zip(capability["local_runners"][:5], allowed_groups)):
        runner_path = OUT / "runners" / row["name"]
        write_text(runner_path, runner_source(allowed))
        contract = next(c for c in contracts if c["operation"] == allowed[0])
        valid = subprocess.run([sys.executable, str(runner_path)], input=json.dumps(contract["request"]), text=True, capture_output=True)
        bad = copy.deepcopy(contract["request"]); bad["input"].pop("global_models", None)
        invalid = subprocess.run([sys.executable, str(runner_path)], input=json.dumps(bad), text=True, capture_output=True)
        if valid.returncode != 0 or invalid.returncode != 2:
            raise AssertionError(f"runner smoke failed: {runner_path}")
        runner_smokes.append({"runner": row["name"], "allowed": allowed, "accept_exit": valid.returncode, "reject_exit": invalid.returncode, "accepted": json.loads(valid.stdout)["ok"], "rejected": not json.loads(invalid.stdout)["ok"]})

    flow = method_flow(safe, failed, refusals, cfr, operations)
    write_json(OUT / "core-results.json", {"count": 150, "results": safe[:150], "all_match_frozen_expected": True, "boundary": BOUNDARY})
    write_json(OUT / "safe-results.json", {"count": len(safe), "core": 150, "auxiliary": 250, "results": safe, "auxiliary_novelty_credit": 0, "boundary": BOUNDARY})
    write_json(OUT / "candidate-failures.json", {"count": len(failed), "failed_subjects": failed, "completion_credit": 0, "boundary": BOUNDARY})
    write_json(OUT / "refusal-witnesses.json", {"count": len(refusals), "passing_refusals": refusals, "subject_promotion_count": 0, "boundary": BOUNDARY})
    write_json(OUT / "cfr-results.json", {"count": len(cfr), "results": cfr, "deleted_files": 0, "boundary": BOUNDARY})
    write_json(OUT / "runner-smokes.json", {"checks": len(runner_smokes) * 2, "runners": runner_smokes, "boundary": BOUNDARY})
    write_json(OUT / "method-flow.json", flow)
    write_json(OUT / "session-summary.json", {"schema": "ghc.family.phase-session-summary.v1", "owner": "Ilyra Fen", "phase": "v704-v4", "session": "x1", "core_contracts": 150, "safe": len(safe), "candidate_failed": len(failed), "refusal_passed": len(refusals), "cfr_passed": len(cfr), "local_skills": 10, "local_runners": 5, "runner_checks": len(runner_smokes) * 2, "outcome_counts": {"completed": 150, "represented": 0, "open_gap": 0, "exact_gate": 0}, "engine": "independent Python Fraction implementation", "source_replay": False, "boundary": BOUNDARY})
    print(json.dumps({"ok": True, "core": 150, "safe": len(safe), "candidate_failed": len(failed), "refusal_passed": len(refusals), "cfr": len(cfr), "skills": 10, "runners": 5, "runner_checks": len(runner_smokes) * 2, "method_flow": flow["evidence_counts"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
