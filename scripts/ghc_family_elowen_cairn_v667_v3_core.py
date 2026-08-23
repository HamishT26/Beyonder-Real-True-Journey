#!/usr/bin/env python3
"""Family-current bounded validators for Elowen Cairn v667-v3.

This module validates synthetic records only.  It performs no network, physical,
identity, professional, legal, cultural, or authority action.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "elowen-cairn" / "v667-v3"
ALLOWED_LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load_json(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def validate_contract(contract: dict[str, Any]) -> list[str]:
    """Return stable failure codes; an empty list is the bounded pass state."""

    failures: list[str] = []
    required = {
        "schema",
        "schema_version",
        "owner",
        "phase",
        "proposal_id",
        "expected_disposition",
        "synthetic_only",
        "record_kind",
        "required_nodes",
        "nodes",
        "vacancies",
        "source_ids",
        "participant_count",
        "real_data_row_count",
        "network_call_count",
        "key_count",
        "proof_count",
        "authority_claim",
        "real_world_action",
        "outcome_promotion",
        "protected_gates",
    }
    missing = sorted(required - set(contract))
    if missing:
        failures.append("missing_required_field")
        return failures
    if not isinstance(contract["schema_version"], int) or isinstance(
        contract["schema_version"], bool
    ) or contract["schema_version"] != 1:
        failures.append("wrong_type_or_invalid_range")
    if contract["owner"] != "Elowen Cairn" or contract["phase"] != "v667-v3":
        failures.append("owner_or_phase_mismatch")
    if contract["expected_disposition"] not in ALLOWED_LABELS:
        failures.append("unknown_outcome_label")
    if contract["synthetic_only"] is not True:
        failures.append("synthetic_boundary_missing")
    required_nodes = contract["required_nodes"]
    nodes = contract["nodes"]
    if not isinstance(required_nodes, list) or not isinstance(nodes, list):
        failures.append("node_type_invalid")
    elif not set(required_nodes).issubset(set(nodes)):
        failures.append("missing_required_node")
    if not isinstance(contract["vacancies"], list) or len(contract["vacancies"]) < 5:
        failures.append("vacancy_floor_missing")
    for field in (
        "participant_count",
        "real_data_row_count",
        "network_call_count",
        "key_count",
        "proof_count",
    ):
        if contract[field] != 0:
            failures.append(f"{field}_must_be_zero")
    if contract["authority_claim"] is not None:
        failures.append("provenance_or_authority_smuggling")
    if contract["real_world_action"] is not False:
        failures.append("real_world_or_production_action")
    if contract["outcome_promotion"] is not None:
        failures.append("outcome_or_conformance_promotion")
    if not isinstance(contract["protected_gates"], list) or len(contract["protected_gates"]) < 10:
        failures.append("protected_gate_floor_missing")
    return sorted(set(failures))


RUNNER_SELECTIONS = {
    "work_order": ["EC6673-N001"],
    "topology": ["EC6673-N002", "EC6673-N003", "EC6673-N009"],
    "action_firewall": ["EC6673-N005", "EC6673-N008", "EC6673-N013"],
    "units": ["EC6673-N006", "EC6673-N012"],
    "cues": ["EC6673-N004", "EC6673-N007"],
    "tuning": ["EC6673-N010", "EC6673-N011"],
    "modal": ["EC6673-N015", "EC6673-N018"],
    "identity": ["EC6673-N014", "EC6673-N017"],
    "adapter": ["EC6673-N019", "EC6673-N020"],
    "validation": [f"EC6673-N{index:03d}" for index in range(1, 21)],
}


def runner_self_test(kind: str) -> dict[str, Any]:
    if kind not in RUNNER_SELECTIONS:
        return {"runner_kind": kind, "passed": False, "failure": "unknown_runner_kind"}
    failures: dict[str, list[str]] = {}
    for proposal_id in RUNNER_SELECTIONS[kind]:
        relative = f"x2/proposals/{proposal_id.casefold()}/contract.json"
        contract = load_json(relative)
        result = validate_contract(contract)
        if result:
            failures[proposal_id] = result
    extra: list[str] = []
    if kind == "adapter":
        adapter = load_json("x2/adapter/vam-api-v2-zero-row-adapter.json")
        if adapter["transport_enabled"] or adapter["request_count"] or adapter["row_count"]:
            extra.append("adapter_transport_or_data_not_zero")
    if kind == "validation":
        outcomes = load_json("x2/proposal-outcomes.json")
        mutations = load_json("x2/rejecting-mutations.json")
        if outcomes["counts"] != {
            "completed": 14,
            "represented": 4,
            "open_gap": 1,
            "exact_gate": 1,
        }:
            extra.append("outcome_count_mismatch")
        if mutations["mutation_count"] != 100 or mutations["accepted_mutation_count"] != 0:
            extra.append("mutation_count_or_acceptance_mismatch")
    return {
        "schema": "ghc-family-owner-runner-self-test-v1",
        "owner": "Elowen Cairn",
        "phase": "v667-v3",
        "runner_kind": kind,
        "selected_proposal_ids": RUNNER_SELECTIONS[kind],
        "contract_failures": failures,
        "extra_failures": extra,
        "passed": not failures and not extra,
        "scope": "bounded wholly synthetic owner-local structural evidence only",
    }
