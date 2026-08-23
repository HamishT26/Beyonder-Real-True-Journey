#!/usr/bin/env python3
"""Bounded neon-record validators for Sylven Arc v667-v4.

The module validates wholly synthetic records only. It emits no fabrication,
electrical, gas, mercury, preservation, safety, professional, legal, cultural,
Māori-authority, identity, production, deployment, or Stage 20 authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "sylven-arc" / "v667-v4"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}

VACANCIES = [
    "real_person",
    "real_sign",
    "real_glass_or_component",
    "real_gas_or_mercury",
    "real_electrical_system",
    "real_measurement",
    "real_site",
    "real_operator",
    "real_authority",
    "real_key_or_proof",
    "real_network_data",
]

MODEL_NODES = {
    "SA6674-N001": ["assembly_docket", "segment_set", "pattern_revision", "dark_state_hold", "cancellation"],
    "SA6674-N002": ["letterform", "pattern", "bend_node", "bridge", "crossover", "return", "termination"],
    "SA6674-N003": ["tube_material", "diameter_vacancy", "coating", "colour_family", "supplier_claim", "substitution"],
    "SA6674-N004": ["burner_vacancy", "flame_zone", "heat_event", "bend_event", "cooling", "annealing_vacancy"],
    "SA6674-N005": ["electrode", "sleeve", "lead", "splice", "return", "cap", "enclosure"],
    "SA6674-N006": ["manifold", "tubulation", "evacuation", "purge", "gas_fill", "pressure_vacancy", "leak_hold"],
    "SA6674-N007": ["purification", "electrode_heating", "impurity_removal", "seal", "aging", "inspection_vacancy"],
    "SA6674-N008": ["species", "phosphor", "glass_colour", "wavelength_source", "spectral_vacancy", "colour_refusal"],
    "SA6674-N009": ["power_supply", "primary", "secondary", "controller", "disconnect", "interlock", "circuit_vacancy"],
    "SA6674-N010": ["cabinet", "channel", "backer", "fastener", "tube_support", "drain", "facade_interface"],
    "SA6674-N011": ["tube_break_cue", "flicker_cue", "dark_section", "corrosion_cue", "uncertainty", "review_hold"],
    "SA6674-N012": ["historic_lettering", "colour_claim", "placement", "animation", "alteration", "evidence_source"],
    "SA6674-N013": ["capture_vacancy", "digest_placeholder", "rights_class", "location_minimization", "redaction", "zero_upload"],
    "SA6674-N014": ["pattern_node_rename", "bend_count_delta", "glass_substitution", "dark_state_restore", "jcs_digest"],
    "SA6674-N015": ["wavelength_domain", "radiance_vacancy", "flicker", "colour_label", "attention_vacancy", "agency_nonconversion"],
    "SA6674-N016": ["dark_state", "energized_state_vacancy", "occluded_label", "segment_token", "equal_budget", "abstention"],
    "SA6674-N017": ["pattern_derivation", "tube_segment", "electrode_invalidation", "transformer_vacancy", "contested_attribution"],
    "SA6674-N018": ["plasma_domain", "electromagnetic_field", "radiative_term", "thermal_term", "species", "covariance_vacancy"],
    "SA6674-N019": ["smithsonian_schema_pin", "transport_disabled", "zero_rows", "zero_media", "rights_hold"],
    "SA6674-N020": ["labour_gate", "flame_gas_gate", "high_voltage_gate", "heritage_gate", "affected_party_gate", "maori_authority_gate"],
}

RUNNER_SELECTIONS = {
    "job": ["SA6674-N001", "SA6674-N014"],
    "topology": ["SA6674-N002", "SA6674-N005", "SA6674-N010"],
    "action_firewall": ["SA6674-N004", "SA6674-N006", "SA6674-N007"],
    "gas": ["SA6674-N006", "SA6674-N008"],
    "electrical": ["SA6674-N005", "SA6674-N009", "SA6674-N016"],
    "spectrum": ["SA6674-N008", "SA6674-N015", "SA6674-N018"],
    "provenance": ["SA6674-N012", "SA6674-N013", "SA6674-N014"],
    "identity": ["SA6674-N017"],
    "adapter": ["SA6674-N019", "SA6674-N020"],
    "validation": list(MODEL_NODES),
}


def strict_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_contract(contract: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    required = {
        "schema",
        "schema_version",
        "owner",
        "phase",
        "proposal_id",
        "title",
        "expected_disposition",
        "synthetic_only",
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
        issues.append("missing_required_fields:" + ",".join(missing))
    if contract.get("schema") != "ghc-family-neon-record-synthetic-contract-v1":
        issues.append("schema_mismatch")
    if contract.get("schema_version") != 1:
        issues.append("schema_version_must_be_integer_one")
    proposal_id = contract.get("proposal_id")
    if proposal_id not in MODEL_NODES:
        issues.append("unknown_proposal_id")
    else:
        absent = sorted(set(MODEL_NODES[proposal_id]) - set(contract.get("nodes", [])))
        if absent:
            issues.append("missing_required_nodes:" + ",".join(absent))
    if contract.get("owner") != "Sylven Arc" or contract.get("phase") != "v667-v4":
        issues.append("owner_or_phase_mismatch")
    if contract.get("expected_disposition") not in ALLOWED_OUTCOMES:
        issues.append("invalid_outcome_label")
    if contract.get("synthetic_only") is not True:
        issues.append("synthetic_boundary_missing")
    if contract.get("vacancies") != VACANCIES:
        issues.append("vacancy_contract_mismatch")
    zero_fields = ("participant_count", "real_data_row_count", "network_call_count", "key_count", "proof_count")
    if any(contract.get(field) != 0 for field in zero_fields):
        issues.append("nonzero_real_or_external_count")
    if contract.get("authority_claim") is not None:
        issues.append("authority_claim_forbidden")
    if contract.get("real_world_action") is not False:
        issues.append("real_world_action_forbidden")
    if contract.get("outcome_promotion") is not None:
        issues.append("outcome_promotion_forbidden")
    if not contract.get("protected_gates"):
        issues.append("protected_gates_missing")
    return issues


def runner_self_test(kind: str) -> dict[str, Any]:
    proposal_ids = RUNNER_SELECTIONS.get(kind)
    if not proposal_ids:
        return {"kind": kind, "passed": False, "issues": ["unknown_runner_kind"]}
    rows = []
    for proposal_id in proposal_ids:
        contract_path = PHASE_ROOT / "x2" / "proposals" / proposal_id.casefold() / "contract.json"
        contract = strict_json(contract_path)
        issues = validate_contract(contract)
        rows.append({"proposal_id": proposal_id, "issues": issues, "passed": not issues})
    return {
        "schema": "ghc-family-sylven-v667-v4-runner-smoke-v1",
        "kind": kind,
        "proposal_count": len(rows),
        "results": rows,
        "passed": all(row["passed"] for row in rows),
        "real_world_actions": 0,
        "authority_claims": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
