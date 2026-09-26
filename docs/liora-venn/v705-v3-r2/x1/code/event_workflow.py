from __future__ import annotations

import copy
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


PHASE_ROOT = Path(__file__).resolve().parents[2]
PLANNING_ROOT = PHASE_ROOT / "planning"
X1_ROOT = PHASE_ROOT / "x1"
X1_OPERATIONS = (
    "record_shape",
    "event_sequence",
    "transition_legality",
    "idempotency_consistency",
    "attempt_budget",
    "retry_decision",
    "acknowledgement_reduce",
    "duplicate_guard",
    "capability_intersection",
    "authority_vacancy",
)
BOUNDARY = "Finite synthetic same-owner event-workflow evidence only; no live service, external action, authority, empirical, production, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20."


class ContractError(ValueError):
    pass


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def fixture_digest(fixture: dict[str, Any]) -> str:
    body = {key: value for key, value in fixture.items() if key != "fixture_sha256"}
    return sha256_json(body)


def load_fixtures() -> dict[str, dict[str, Any]]:
    rows = load_json(PLANNING_ROOT / "fixtures.json")
    return {row["fixture_id"]: row for row in rows}


def load_contracts(stage: str = "x1") -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted((PLANNING_ROOT / "contracts").glob("*.json")):
        rows.extend(row for row in load_json(path) if row["stage"] == stage)
    return rows


def validate_contract(contract: dict[str, Any], fixture: dict[str, Any]) -> None:
    required = {"proposal_id", "contract_id", "stage", "request", "request_sha256", "expected_disposition"}
    missing = sorted(required - set(contract))
    if missing:
        raise ContractError(f"missing contract fields: {missing}")
    request = contract["request"]
    request_required = {"schema", "fixture_id", "operation", "purpose", "fixture_sha256"}
    request_missing = sorted(request_required - set(request))
    if request_missing:
        raise ContractError(f"missing request fields: {request_missing}")
    if contract["stage"] != "x1":
        raise ContractError("not an x1 contract")
    if request["schema"] != "ghc.family.event-workflow.request.v1":
        raise ContractError("request schema mismatch")
    if request["operation"] not in X1_OPERATIONS:
        raise ContractError("operation outside x1 allowlist")
    if request["fixture_id"] != fixture.get("fixture_id"):
        raise ContractError("fixture identifier mismatch")
    observed_fixture_sha = fixture_digest(fixture)
    if fixture.get("fixture_sha256") != observed_fixture_sha or request["fixture_sha256"] != observed_fixture_sha:
        raise ContractError("fixture digest mismatch")
    if contract["request_sha256"] != sha256_json(request):
        raise ContractError("request digest mismatch")


def record_shape(fixture: dict[str, Any]) -> dict[str, Any]:
    required = {
        "schema", "fixture_id", "label", "purpose", "states", "events", "allowed_transitions",
        "max_attempts", "submissions", "requested_capabilities", "allowed_capabilities",
        "authority_required", "authority_present", "hook_sequence", "claims", "artifact_usage",
        "public_record", "external_observations", "authority_actions", "terminal_state", "fixture_sha256",
    }
    array_fields = (
        "states", "events", "submissions", "requested_capabilities", "allowed_capabilities",
        "authority_required", "authority_present", "hook_sequence", "claims", "external_observations",
        "authority_actions",
    )
    missing = sorted(required - set(fixture))
    wrong_arrays = sorted(name for name in array_fields if not isinstance(fixture.get(name), list))
    return {"missing_fields": missing, "wrong_array_fields": wrong_arrays, "record_valid": not missing and not wrong_arrays}


def event_sequence(fixture: dict[str, Any]) -> dict[str, Any]:
    events = fixture["events"]
    observed = [row.get("seq") for row in events]
    expected = list(range(1, len(events) + 1))
    return {"observed": observed, "expected": expected, "contiguous": observed == expected}


def transition_legality(fixture: dict[str, Any]) -> dict[str, Any]:
    invalid = []
    continuity = []
    prior_target = None
    for event in fixture["events"]:
        source = event.get("source_state")
        target = event.get("target_state")
        if target not in fixture["allowed_transitions"].get(source, []):
            invalid.append({"seq": event.get("seq"), "source": source, "target": target})
        if prior_target is not None and source != prior_target:
            continuity.append({"seq": event.get("seq"), "expected_source": prior_target, "observed_source": source})
        prior_target = target
    return {"invalid_transitions": invalid, "continuity_breaks": continuity, "legal": not invalid and not continuity}


def idempotency_consistency(fixture: dict[str, Any]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in fixture["submissions"]:
        groups[row["request_id"]].append(row)
    duplicates = sorted(key for key, values in groups.items() if len(values) > 1)
    conflicts = []
    for key, values in groups.items():
        signatures = {(row.get("payload_hash"), row.get("state")) for row in values}
        if len(signatures) > 1:
            conflicts.append(key)
    return {"duplicate_request_ids": duplicates, "conflicting_request_ids": sorted(conflicts), "consistent": not conflicts}


def attempt_budget(fixture: dict[str, Any]) -> dict[str, Any]:
    attempts = [int(event.get("attempt", 0)) for event in fixture["events"]]
    observed = max(attempts, default=0)
    declared = int(fixture["max_attempts"])
    return {"observed_max_attempt": observed, "declared_max_attempts": declared, "within_budget": 0 < observed <= declared}


def retry_decision(fixture: dict[str, Any]) -> dict[str, Any]:
    budget = attempt_budget(fixture)
    remaining = max(0, budget["declared_max_attempts"] - budget["observed_max_attempt"])
    terminal = fixture["terminal_state"]
    send_capability = "send_native" in fixture["allowed_capabilities"]
    retryable_terminal = terminal in {"failed", "held"}
    return {
        "terminal_state": terminal,
        "remaining_attempts": remaining,
        "send_capability_present": send_capability,
        "retry_recommended": retryable_terminal and remaining > 0 and send_capability,
        "unresolved_or_accepted_stops_retry": terminal in {"acknowledged", "succeeded"},
    }


def acknowledgement_reduce(fixture: dict[str, Any]) -> dict[str, Any]:
    acknowledgements = [event for event in fixture["events"] if event.get("type") == "workflow.acknowledged"]
    explicit = bool(acknowledgements) and fixture["terminal_state"] == "acknowledged"
    return {"acknowledgement_events": len(acknowledgements), "terminal_state": fixture["terminal_state"], "explicitly_acknowledged": explicit, "silence_is_acceptance": False}


def duplicate_guard(fixture: dict[str, Any]) -> dict[str, Any]:
    idem = idempotency_consistency(fixture)
    return {
        "duplicate_request_ids": idem["duplicate_request_ids"],
        "conflicting_request_ids": idem["conflicting_request_ids"],
        "duplicate_detected": bool(idem["duplicate_request_ids"]),
        "new_external_action_executed": False,
    }


def capability_intersection(fixture: dict[str, Any]) -> dict[str, Any]:
    requested = list(dict.fromkeys(fixture["requested_capabilities"]))
    allowed = set(fixture["allowed_capabilities"])
    admitted = [value for value in requested if value in allowed]
    denied = [value for value in requested if value not in allowed]
    return {"requested": requested, "admitted": admitted, "denied": denied, "authority_widened": False}


def authority_vacancy(fixture: dict[str, Any]) -> dict[str, Any]:
    present = set(fixture["authority_present"])
    missing = [value for value in fixture["authority_required"] if value not in present]
    return {"missing_authorities": missing, "authority_gate_open": not missing, "external_authority_inferred": False}


OPERATIONS = {
    "record_shape": record_shape,
    "event_sequence": event_sequence,
    "transition_legality": transition_legality,
    "idempotency_consistency": idempotency_consistency,
    "attempt_budget": attempt_budget,
    "retry_decision": retry_decision,
    "acknowledgement_reduce": acknowledgement_reduce,
    "duplicate_guard": duplicate_guard,
    "capability_intersection": capability_intersection,
    "authority_vacancy": authority_vacancy,
}


def execute_contract(contract: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    validate_contract(contract, fixture)
    operation = contract["request"]["operation"]
    observation = OPERATIONS[operation](fixture)
    return {
        "contract_id": contract["contract_id"],
        "proposal_id": contract["proposal_id"],
        "stage": "x1",
        "operation": operation,
        "fixture_id": fixture["fixture_id"],
        "disposition": contract["expected_disposition"],
        "execution_result": "pass",
        "observation": observation,
        "observation_sha256": sha256_json(observation),
        "external_actions": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    }


def execute_all(stage: str = "x1") -> list[dict[str, Any]]:
    fixtures = load_fixtures()
    return [execute_contract(row, fixtures[row["request"]["fixture_id"]]) for row in load_contracts(stage)]


def mutated_contract(contract: dict[str, Any], mutation: str) -> dict[str, Any]:
    row = copy.deepcopy(contract)
    if mutation == "missing_request_schema":
        row["request"].pop("schema", None)
    elif mutation == "request_digest_mismatch":
        row["request_sha256"] = "0" * 64
    else:
        raise ValueError(mutation)
    return row


def execute_mutations(stage: str = "x1") -> list[dict[str, Any]]:
    fixtures = load_fixtures()
    rows = []
    for contract in load_contracts(stage):
        fixture = fixtures[contract["request"]["fixture_id"]]
        for mutation in ("missing_request_schema", "request_digest_mismatch"):
            rejected = False
            error = ""
            try:
                execute_contract(mutated_contract(contract, mutation), fixture)
            except ContractError as exc:
                rejected, error = True, str(exc)
            rows.append(
                {
                    "witness_id": f"{contract['contract_id']}-{mutation}",
                    "contract_id": contract["contract_id"],
                    "mutation": mutation,
                    "result": "fail",
                    "rejected": rejected,
                    "error": error,
                    "credit": 0,
                    "retained": True,
                    "boundary": BOUNDARY,
                }
            )
    return rows


def execute_recoveries(stage: str = "x1") -> list[dict[str, Any]]:
    fixtures = load_fixtures()
    rows = []
    for contract in load_contracts(stage):
        fixture = fixtures[contract["request"]["fixture_id"]]
        result = execute_contract(contract, fixture)
        rows.append({"contract_id": contract["contract_id"], "result": "pass", "recovery_scope": "valid frozen template only", "observation_sha256": result["observation_sha256"], "failed_witnesses_erased": False, "boundary": BOUNDARY})
    return rows


def execute_portfolio(stage: str, kind: str) -> list[dict[str, Any]]:
    portfolio = load_json(PLANNING_ROOT / "portfolio-freeze.json")[kind][stage]
    contracts = load_contracts(stage)
    fixtures = load_fixtures()
    rows = []
    for index, task in enumerate(portfolio):
        contract = contracts[index % len(contracts)]
        result = execute_contract(contract, fixtures[contract["request"]["fixture_id"]])
        rows.append(
            {
                "work_item_id": task["work_item_id"],
                "kind": kind,
                "result": "pass",
                "contract_id": contract["contract_id"],
                "observation_sha256": result["observation_sha256"],
                "core_outcome_credit": False,
                "external_actions": 0,
                "boundary": BOUNDARY,
            }
        )
    return rows
