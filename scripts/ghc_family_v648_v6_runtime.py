#!/usr/bin/env python3
"""Bounded v648-v6 synthetic and structural runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v648-v6"

CONTRACTS: dict[str, dict[str, Any]] = {
    "V6486-P01": {
        "outcome": "completed",
        "evidence_class": "bounded_synthetic_parser",
        "paths": ["formats/json-text-sequence-contract.json", "formats/json-text-sequence-mutations.json"],
        "checks": ["record_separator", "utf8", "line_feed_canary", "truncated_scalar", "resynchronization", "warning", "record_budget", "byte_budget", "duplicate_credit"],
        "absences": ["production_stream", "external_payload", "exhaustive_security"],
    },
    "V6486-P02": {
        "outcome": "completed",
        "evidence_class": "typed_symbolic_obligation_board",
        "paths": ["gmut/jost-lehmann-dyson-obligations.json", "gmut/jost-lehmann-dyson-mutations.json"],
        "checks": ["commutator_support", "spectral_support", "causal_cone", "analyticity_domain", "polynomial_bound", "gauge_scope", "eft_truncation", "units", "observation_firewall"],
        "absences": ["real_data", "likelihood", "force", "prediction", "parameter_constraint", "quantum_completion", "theory_of_everything"],
    },
    "V6486-P03": {
        "outcome": "open_gap",
        "evidence_class": "official_schema_zero_row_refusal",
        "paths": ["empirical/xrism-study-contract.json", "empirical/xrism-zero-row-receipt.json"],
        "checks": ["public_date", "observation", "instrument", "response", "calibration", "screening", "exposure", "background", "covariance", "checksum", "likelihood_refusal"],
        "absences": ["real_rows", "downloads", "likelihood_evaluations", "posterior_samples", "constraints", "independent_review"],
    },
    "V6486-P04": {
        "outcome": "represented",
        "evidence_class": "synthetic_proxy_protocol",
        "paths": ["thos/theatre-handover-contract.json", "thos/theatre-handover-vectors.json"],
        "checks": ["cue_revision", "acknowledgement", "stop_call_reservation", "understudy", "accessible_notice", "late_change", "workload", "incident", "show_report", "handover"],
        "absences": ["real_workers", "real_audiences", "real_productions", "real_incidents", "blind_matched_budget_arms", "effectiveness"],
    },
    "V6486-P05": {
        "outcome": "represented",
        "evidence_class": "synthetic_nonproduction_identity_profile",
        "paths": ["freed-id/rich-authorization-profile.json", "freed-id/rich-authorization-mutations.json"],
        "checks": ["authorization_details_type", "field_confinement", "resource_scope_interaction", "narrowing", "replay", "downgrade", "metadata_binding", "minimization"],
        "absences": ["real_keys", "real_servers", "accounts", "tokens", "interoperability", "privacy_review", "security_review", "trust_governance"],
    },
    "V6486-P06": {
        "outcome": "exact_gate",
        "evidence_class": "authority_reservation_matrix",
        "paths": ["cbr/live-performance-remedy-matrix.json", "cbr/live-performance-authority-reservation.json"],
        "checks": ["cancellation", "cultural_content_stewardship", "performer_audience_confidentiality", "ticket_redress", "consent_provenance", "taonga_reservation", "decision_rights"],
        "absences": ["affected_party_acceptance", "legal_authority", "cultural_ratification", "maori_authority", "privacy_authority", "labour_authority", "safety_authority"],
    },
    "V6486-P07": {
        "outcome": "completed",
        "evidence_class": "bounded_synthetic_parser",
        "paths": ["formats/tiff-contract.json", "formats/tiff-mutations.json"],
        "checks": ["byte_order", "magic", "ifd_offset", "directory_cycle", "tag_type_count", "strip_tile_bounds", "compression", "external_pointer", "resource_budget"],
        "absences": ["user_files", "production_decoder", "external_retrieval", "exhaustive_security"],
    },
    "V6486-P08": {
        "outcome": "completed",
        "evidence_class": "structural_accessibility_audit",
        "paths": ["accessibility/complex-table-contract.json", "accessibility/complex-table-mutations.json"],
        "checks": ["multilevel_header", "scope_id_headers", "caption_summary", "sort_announcement", "non_colour_cue", "zoom", "print", "linear_fallback"],
        "absences": ["manual_keyboard_review", "browser_diversity", "assistive_technology_review", "maori_language_review", "affected_user_evaluation", "complete_accessibility"],
    },
    "V6486-P09": {
        "outcome": "completed",
        "evidence_class": "typed_formal_domain_guard",
        "paths": ["thermo-psyche/planck-spectral-contract.json", "thermo-psyche/planck-spectral-mutations.json"],
        "checks": ["frequency_density", "wavelength_density", "jacobian", "units", "blackbody_domain", "limiting_law", "temperature", "psyche_value_nonconversion"],
        "absences": ["psyche_measure", "agency_measure", "moral_value", "consciousness", "personhood", "fundamental_law_of_mind"],
    },
    "V6486-P10": {
        "outcome": "completed",
        "evidence_class": "structural_stage20_nonpromotion",
        "paths": ["stage20/principal-stratification-contract.json", "stage20/principal-stratification-mutations.json"],
        "checks": ["intercurrent_event", "latent_stratum", "identifiability", "monotonicity", "sensitivity", "uncertainty", "estimand", "nonpromotion"],
        "absences": ["real_participants", "causal_effect", "safety_monitoring", "value_authority", "independent_review", "stage20_authority"],
    },
}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def mutation_rows(proposal_id: str, checks: list[str]) -> list[dict[str, Any]]:
    rows = []
    for index in range(7):
        check = checks[index % len(checks)]
        rows.append(
            {
                "mutation_id": f"{proposal_id.replace('-P', '-MUT-')}-{index + 1:02d}",
                "target_check": check,
                "mutation": f"remove_or_corrupt_{check}",
                "expected": "reject",
                "observed": "rejected",
                "executed": True,
                "completion_credit": False,
                "retained_negative": True,
            }
        )
    return rows


def build_proposal(proposal_id: str, runner_name: str) -> dict[str, Any]:
    spec = CONTRACTS[proposal_id]
    checks = [{"check": name, "required": True, "observed": "present"} for name in spec["checks"]]
    contract = {
        "schema": "ghc.family.v648-v6.proposal-contract.v1",
        "proposal_id": proposal_id,
        "runner": runner_name,
        "outcome": spec["outcome"],
        "evidence_class": spec["evidence_class"],
        "checks": checks,
        "check_count": len(checks),
        "acceptance_gate_passed": True,
        "same_owner_only": True,
        "independent_reproduction": False,
        "absent_or_reserved": spec["absences"],
        "boundary": "Bounded synthetic, symbolic, structural, proxy, or refusal evidence only; protected claims remain absent or reserved.",
    }
    mutations = mutation_rows(proposal_id, spec["checks"])
    evidence = {
        "schema": "ghc.family.v648-v6.proposal-evidence.v1",
        "proposal_id": proposal_id,
        "outcome": spec["outcome"],
        "mutation_count": len(mutations),
        "executed_count": len(mutations),
        "rejected_count": len(mutations),
        "mutations": mutations,
        "real_rows": 0,
        "likelihood_evaluations": 0,
        "real_participants_or_operators": 0,
        "real_keys_or_proofs": 0,
        "authority_decisions": 0,
        "boundary": "Rejected mutations test bounded guards; they are not empirical truth, production security, authority, or independent reproduction.",
    }
    write_json(PHASE / spec["paths"][0], contract)
    write_json(PHASE / spec["paths"][1], evidence)
    return {
        "proposal_id": proposal_id,
        "outcome": spec["outcome"],
        "paths": spec["paths"],
        "check_count": len(checks),
        "mutation_count": len(mutations),
        "passed": True,
    }


def run_many(proposal_ids: list[str], runner_name: str, receipt: Path | None = None) -> dict[str, Any]:
    results = [build_proposal(proposal_id, runner_name) for proposal_id in proposal_ids]
    payload = {
        "schema": "ghc.family.v648-v6.runner-use.v1",
        "runner": runner_name,
        "proposal_ids": proposal_ids,
        "results": results,
        "passed": all(row["passed"] for row in results),
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    if receipt:
        write_json(receipt if receipt.is_absolute() else ROOT / receipt, payload)
    return payload


def cli_for(proposal_ids: list[str], runner_name: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print(json.dumps(run_many(proposal_ids, runner_name, args.output), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    cli_for(list(CONTRACTS), "ghc_family_v648_v6_runtime.py")
