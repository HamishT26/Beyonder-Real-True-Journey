#!/usr/bin/env python3
"""Reusable bounded runtime for Ilyra Fen v647-v6 synthetic evidence."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


BOUNDARY = (
    "Synthetic owner-local software evidence only. No real data, participant, professional, legal, cultural, "
    "Māori-authority, identity, production, deployment, exhaustive-security, complete-accessibility, "
    "independent-reproduction, AGI or ASI, consciousness, personhood, Theory-of-Everything, or Stage 20 claim."
)


SURFACES: dict[str, dict[str, Any]] = {
    "watcher": {
        "proposal_id": "V6476-P01", "outcome": "completed",
        "required_true": ["rename_pair_complete", "coalescing_preserves_terminal_state", "overflow_forces_rescan", "rescan_root_bounded", "watermark_monotonic", "cancellation_preserved", "credit_requires_reconciliation"],
    },
    "barnes_rivers": {
        "proposal_id": "V6476-P02", "outcome": "completed",
        "required_true": ["projector_complete", "projector_orthogonal", "source_conserved", "gauge_sector_reserved", "pole_convention_declared", "residue_convention_declared", "eft_nonpromotion"],
    },
    "sdss_dr19": {
        "proposal_id": "V6476-P03", "outcome": "open_gap",
        "required_zero": ["archive_queries", "downloads", "real_rows", "covariance_rows", "likelihood_calls", "posterior_samples", "parameter_constraints"],
    },
    "weather_handover": {
        "proposal_id": "V6476-P04", "outcome": "represented",
        "required_true": ["synthetic_only", "amendment_reason_required", "expiry_checked", "accessible_fallback_declared", "correction_readback_required", "escalation_owned", "next_shift_owner_required"],
    },
    "oauth_token_exchange": {
        "proposal_id": "V6476-P05", "outcome": "represented",
        "required_true": ["synthetic_only", "subject_type_bound", "actor_role_distinct", "target_narrowing_checked", "delegation_cycle_rejected", "expiry_checked", "replay_rejected"],
    },
    "weather_authority": {
        "proposal_id": "V6476-P06", "outcome": "exact_gate",
        "required_zero": ["real_warning_decisions", "real_disclosures", "real_remedies", "legal_interpretations", "cultural_ratifications", "maori_authority_decisions", "affected_party_acceptances"],
    },
    "png_chunk": {
        "proposal_id": "V6476-P07", "outcome": "completed",
        "required_true": ["signature_checked", "length_checked", "crc_checked", "critical_order_checked", "unknown_critical_rejected", "unsafe_ancillary_refused", "decompression_budget_enforced"],
    },
    "treegrid": {
        "proposal_id": "V6476-P08", "outcome": "completed",
        "required_true": ["hierarchy_declared", "row_position_declared", "expansion_owner_declared", "selection_distinct_from_focus", "keyboard_plan_declared", "fallback_preserves_data", "manual_evaluation_reserved"],
    },
    "gibbs_phase_rule": {
        "proposal_id": "V6476-P09", "outcome": "completed",
        "required_true": ["components_declared", "phases_declared", "reaction_rank_declared", "external_constraints_declared", "equilibrium_scope_declared", "variance_arithmetic_checked", "agency_nonconversion"],
    },
    "covariate_shift": {
        "proposal_id": "V6476-P10", "outcome": "completed",
        "required_true": ["source_target_declared", "support_overlap_required", "weight_cap_explicit", "effective_sample_size_reported", "leakage_rejected", "sensitivity_required", "stage20_nonpromotion"],
    },
}


def baseline(surface: str) -> dict[str, Any]:
    spec = SURFACES[surface]
    payload: dict[str, Any] = {"surface": surface, "proposal_id": spec["proposal_id"]}
    payload.update({field: True for field in spec.get("required_true", [])})
    payload.update({field: 0 for field in spec.get("required_zero", [])})
    return payload


def accepts(surface: str, payload: dict[str, Any]) -> bool:
    spec = SURFACES[surface]
    return all(payload.get(field) is True for field in spec.get("required_true", [])) and all(
        payload.get(field) == 0 for field in spec.get("required_zero", [])
    )


def surface_evidence(surface: str) -> dict[str, Any]:
    if surface not in SURFACES:
        raise KeyError(surface)
    spec = SURFACES[surface]
    good = baseline(surface)
    fields = list(spec.get("required_true", [])) + list(spec.get("required_zero", []))
    if len(fields) != 7:
        raise RuntimeError(f"{surface} must expose exactly seven mutation fields")
    mutations = []
    for index, field in enumerate(fields, 1):
        mutated = deepcopy(good)
        mutated[field] = False if field in spec.get("required_true", []) else 1
        rejected = not accepts(surface, mutated)
        mutations.append(
            {
                "negative_id": f"V6476-SYN-{int(spec['proposal_id'][-2:]):02d}-{index:02d}",
                "field": field,
                "mutation": "required_true_to_false" if field in spec.get("required_true", []) else "required_zero_to_one",
                "rejected": rejected,
                "retained": True,
            }
        )
    return {
        "schema": "ghc.family.v647-v6.surface-evidence.v1",
        "surface": surface,
        "proposal_id": spec["proposal_id"],
        "outcome": spec["outcome"],
        "valid_fixture_passed": accepts(surface, good),
        "baseline": good,
        "mutation_count": len(mutations),
        "rejected_mutation_count": sum(row["rejected"] for row in mutations),
        "mutations": mutations,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def cli_main(surface: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = surface_evidence(surface)
    write_json(args.output, payload)
    print(json.dumps({"surface": surface, "valid": payload["valid_fixture_passed"], "rejected": payload["rejected_mutation_count"]}))
    raise SystemExit(0 if payload["valid_fixture_passed"] and payload["rejected_mutation_count"] == 7 else 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("surface", choices=sorted(SURFACES))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = surface_evidence(args.surface)
    write_json(args.output, payload)
    print(json.dumps({"surface": args.surface, "valid": payload["valid_fixture_passed"], "rejected": payload["rejected_mutation_count"]}))
