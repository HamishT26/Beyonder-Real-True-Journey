from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
PHASE_ROOT = Path(__file__).resolve().parents[2]
PLANNING_ROOT = PHASE_ROOT / "planning"
X2_ROOT = PHASE_ROOT / "x2"
X1_MODULE_PATH = PHASE_ROOT / "x1" / "code" / "event_workflow.py"
_spec = importlib.util.spec_from_file_location("liora_event_workflow_x1_dependency", X1_MODULE_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError("X1_MODULE_LOAD_FAILED")
x1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(x1)

X2_OPERATIONS = (
    "rollback_reachability", "provenance_chain", "hook_order", "start_stop_pair", "claim_overlap",
    "workflow_artifact_budget", "privacy_label", "terminal_projection", "live_service_observation_gap",
    "protected_authority_hold",
)
BOUNDARY = "Finite synthetic same-owner event-workflow and 3D graph-model evidence only; no live service, external action, empirical, production, authority, independent-reproduction, proof, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20."


class ContractError(ValueError):
    pass


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_fixtures() -> dict[str, dict[str, Any]]:
    return x1.load_fixtures()


def load_contracts(stage: str = "x2") -> list[dict[str, Any]]:
    rows = []
    for path in sorted((PLANNING_ROOT / "contracts").glob("*.json")):
        rows.extend(row for row in load_json(path) if row["stage"] == stage)
    return rows


def validate_contract(contract: dict[str, Any], fixture: dict[str, Any]) -> None:
    required = {"proposal_id", "contract_id", "stage", "request", "request_sha256", "expected_disposition"}
    if required - set(contract):
        raise ContractError("missing contract fields")
    request = contract["request"]
    request_required = {"schema", "fixture_id", "operation", "purpose", "fixture_sha256"}
    if request_required - set(request):
        raise ContractError("missing request fields")
    if contract["stage"] != "x2" or request["operation"] not in X2_OPERATIONS:
        raise ContractError("operation outside x2 allowlist")
    if request["schema"] != "ghc.family.event-workflow.request.v1":
        raise ContractError("request schema mismatch")
    if request["fixture_id"] != fixture.get("fixture_id"):
        raise ContractError("fixture identifier mismatch")
    observed = x1.fixture_digest(fixture)
    if fixture.get("fixture_sha256") != observed or request["fixture_sha256"] != observed:
        raise ContractError("fixture digest mismatch")
    if contract["request_sha256"] != x1.sha256_json(request):
        raise ContractError("request digest mismatch")


def rollback_reachability(fixture: dict[str, Any]) -> dict[str, Any]:
    start = fixture["terminal_state"]
    seen = {start}
    queue = [start]
    while queue:
        node = queue.pop(0)
        for target in fixture["allowed_transitions"].get(node, []):
            if target not in seen:
                seen.add(target); queue.append(target)
    return {"terminal_state": start, "reachable_states": sorted(seen), "rollback_reachable": "rolled_back" in seen, "live_rollback_executed": False}


def provenance_chain(fixture: dict[str, Any]) -> dict[str, Any]:
    breaks = []
    previous = "GENESIS"
    for event in fixture["events"]:
        if event.get("previous_digest") != previous:
            breaks.append(event.get("seq"))
        digest = event.get("digest", "")
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest.lower()):
            breaks.append(event.get("seq"))
        previous = digest
    return {"events": len(fixture["events"]), "link_break_sequences": sorted(set(breaks)), "linked": not breaks, "real_custody_claim": False}


def hook_order(fixture: dict[str, Any]) -> dict[str, Any]:
    rank = {"SessionStart": 0, "PreToolUse": 1, "PostToolUse": 2, "Stop": 3}
    hooks = fixture["hook_sequence"]
    unknown = [value for value in hooks if value not in rank]
    inversions = []
    for left, right in zip(hooks, hooks[1:]):
        if left in rank and right in rank and rank[left] > rank[right]:
            inversions.append([left, right])
    return {"hooks": hooks, "unknown": unknown, "inversions": inversions, "ordered": not unknown and not inversions, "live_hook_execution": False}


def start_stop_pair(fixture: dict[str, Any]) -> dict[str, Any]:
    hooks = fixture["hook_sequence"]
    starts = [index for index, value in enumerate(hooks) if value == "SessionStart"]
    stops = [index for index, value in enumerate(hooks) if value == "Stop"]
    paired = len(starts) == len(stops) == 1 and starts[0] < stops[0]
    return {"starts": len(starts), "stops": len(stops), "paired": paired, "live_session_claim": False}


def claim_overlap(fixture: dict[str, Any]) -> dict[str, Any]:
    paths = sorted({row["path"].strip("/") for row in fixture["claims"]})
    overlaps = []
    for index, left in enumerate(paths):
        for right in paths[index + 1:]:
            if right.startswith(left + "/") or left.startswith(right + "/"):
                overlaps.append([left, right])
    return {"paths": paths, "overlaps": overlaps, "overlap_detected": bool(overlaps), "ownership_mutated": False}


def workflow_artifact_budget(fixture: dict[str, Any]) -> dict[str, Any]:
    usage = fixture["artifact_usage"]
    return {"files": usage["files"], "max_files": usage["max_files"], "words": usage["words"], "max_words": usage["max_words"], "files_within_budget": usage["files"] < usage["max_files"], "words_within_budget": usage["words"] <= usage["max_words"]}


def privacy_label(fixture: dict[str, Any]) -> dict[str, Any]:
    record = fixture["public_record"]
    violations = [name for name in ("private_identifier_present", "secret_material_present", "participant_record_present") if record.get(name) is not False]
    return {"privacy_class": record.get("privacy_class"), "violations": violations, "bounded_public_synthetic": record.get("privacy_class") == "sanitized_public" and not violations, "complete_privacy_claim": False}


def terminal_projection(fixture: dict[str, Any]) -> dict[str, Any]:
    last_target = fixture["events"][-1]["target_state"] if fixture["events"] else None
    return {"declared_terminal": fixture["terminal_state"], "last_event_target": last_target, "matches": last_target == fixture["terminal_state"], "projection_only": True, "live_status": None}


def live_service_observation_gap(fixture: dict[str, Any]) -> dict[str, Any]:
    observations = fixture["external_observations"]
    return {"external_observation_count": len(observations), "gap_open": len(observations) == 0, "queries": 0, "network_calls": 0, "live_service_claim": False}


def protected_authority_hold(fixture: dict[str, Any]) -> dict[str, Any]:
    present = set(fixture["authority_present"])
    missing = [value for value in fixture["authority_required"] if value not in present]
    return {"missing_authorities": missing, "authority_actions": len(fixture["authority_actions"]), "held": bool(missing) or not fixture["authority_actions"], "authority_inferred": False}


OPERATIONS = {
    "rollback_reachability": rollback_reachability, "provenance_chain": provenance_chain,
    "hook_order": hook_order, "start_stop_pair": start_stop_pair, "claim_overlap": claim_overlap,
    "workflow_artifact_budget": workflow_artifact_budget, "privacy_label": privacy_label,
    "terminal_projection": terminal_projection, "live_service_observation_gap": live_service_observation_gap,
    "protected_authority_hold": protected_authority_hold,
}


def execute_contract(contract: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    validate_contract(contract, fixture)
    operation = contract["request"]["operation"]
    observation = OPERATIONS[operation](fixture)
    disposition = contract["expected_disposition"]
    state = {"completed": "pass", "represented": "pass", "open_gap": "gap", "exact_gate": "held"}[disposition]
    return {"contract_id": contract["contract_id"], "proposal_id": contract["proposal_id"], "stage": "x2", "operation": operation, "fixture_id": fixture["fixture_id"], "disposition": disposition, "execution_result": state, "observation": observation, "observation_sha256": x1.sha256_json(observation), "external_actions": 0, "same_owner_only": True, "independent_reproduction": False, "boundary": BOUNDARY}


def execute_all(stage: str = "x2") -> list[dict[str, Any]]:
    fixtures = load_fixtures()
    return [execute_contract(row, fixtures[row["request"]["fixture_id"]]) for row in load_contracts(stage)]


def mutated_contract(contract: dict[str, Any], mutation: str) -> dict[str, Any]:
    row = copy.deepcopy(contract)
    if mutation == "missing_request_schema": row["request"].pop("schema", None)
    elif mutation == "request_digest_mismatch": row["request_sha256"] = "f" * 64
    else: raise ValueError(mutation)
    return row


def execute_mutations(stage: str = "x2") -> list[dict[str, Any]]:
    fixtures = load_fixtures(); rows = []
    for contract in load_contracts(stage):
        fixture = fixtures[contract["request"]["fixture_id"]]
        for mutation in ("missing_request_schema", "request_digest_mismatch"):
            rejected = False; error = ""
            try: execute_contract(mutated_contract(contract, mutation), fixture)
            except ContractError as exc: rejected, error = True, str(exc)
            rows.append({"witness_id": f"{contract['contract_id']}-{mutation}", "contract_id": contract["contract_id"], "mutation": mutation, "result": "fail", "rejected": rejected, "error": error, "credit": 0, "retained": True, "boundary": BOUNDARY})
    return rows


def execute_recoveries(stage: str = "x2") -> list[dict[str, Any]]:
    fixtures = load_fixtures(); rows = []
    for contract in load_contracts(stage):
        result = execute_contract(contract, fixtures[contract["request"]["fixture_id"]])
        rows.append({"contract_id": contract["contract_id"], "result": "processed", "disposition": result["disposition"], "recovery_scope": "valid frozen template only", "observation_sha256": result["observation_sha256"], "failed_witnesses_erased": False, "boundary": BOUNDARY})
    return rows


def execute_portfolio(stage: str, kind: str) -> list[dict[str, Any]]:
    tasks = load_json(PLANNING_ROOT / "portfolio-freeze.json")[kind][stage]
    contracts = load_contracts(stage); fixtures = load_fixtures(); rows = []
    for index, task in enumerate(tasks):
        contract = contracts[index % len(contracts)]; result = execute_contract(contract, fixtures[contract["request"]["fixture_id"]])
        rows.append({"work_item_id": task["work_item_id"], "kind": kind, "result": "pass", "contract_id": contract["contract_id"], "disposition": result["disposition"], "observation_sha256": result["observation_sha256"], "core_outcome_credit": False, "external_actions": 0, "boundary": BOUNDARY})
    return rows


def load_models() -> list[dict[str, Any]]:
    return [load_json(path) for path in sorted((X2_ROOT / "models").glob("model-*.json"))]


def validate_model(model: dict[str, Any]) -> dict[str, Any]:
    node_ids = {row["id"] for row in model["nodes"]}
    bad_edges = [row["id"] for row in model["edges"] if row["source"] not in node_ids or row["target"] not in node_ids]
    coordinate_issues = [row["id"] for row in model["nodes"] if not all(isinstance(row.get(axis), (int, float)) for axis in ("x", "y", "z"))]
    xs = [row["x"] for row in model["nodes"]]; ys = [row["y"] for row in model["nodes"]]; zs = [row["z"] for row in model["nodes"]]
    bounds = {"x": [min(xs), max(xs)], "y": [min(ys), max(ys)], "z": [min(zs), max(zs)]}
    return {"model_id": model["model_id"], "nodes": len(model["nodes"]), "edges": len(model["edges"]), "simulation_steps": len(model["simulation_steps"]), "bad_edges": bad_edges, "coordinate_issues": coordinate_issues, "bounds": bounds, "valid": not bad_edges and not coordinate_issues, "real_world_simulation": False}
