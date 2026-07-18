#!/usr/bin/env python3
"""Bounded runtime for the ten frozen Eiren v648-v3 repeat surfaces."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v648-v3-2"


def spec(slug: str, outcome: str, path: str, required: dict[str, Any], mutation_keys: list[str], boundary: str) -> dict[str, Any]:
    return {"slug": slug, "outcome": outcome, "path": path, "required": required, "mutation_keys": mutation_keys, "boundary": boundary}


COMMON = {
    "bounded": True,
    "empirical_claim": False,
    "authority_claim": False,
    "production_claim": False,
    "independent_reproduction": False,
    "protected_gates_preserved": True,
}


SURFACES = {
    "V6483R2-P01": spec(
        "reflection-remaster", "completed", "reflection-remaster/tribunal-contract.json",
        {**COMMON, "caller_inventory_present": True, "compatibility_plan_present": True, "rollback_present": True, "issue_count": 54, "method_count": 54, "automatic_deletion": False},
        ["caller_inventory_present", "compatibility_plan_present", "rollback_present", "issue_count", "method_count", "automatic_deletion", "protected_gates_preserved"],
        "A completed audit is not deletion or deprecation authority; all 54 issue and method rows remain unpromoted triage evidence.",
    ),
    "V6483R2-P02": spec(
        "epstein-glaser", "completed", "gmut/epstein-glaser-obligations.json",
        {**COMMON, "formal_only": True, "causal_factorization": True, "distribution_splitting": True, "scaling_degree": True, "locality": True, "renormalization_ambiguity": True, "real_rows": 0},
        ["formal_only", "causal_factorization", "distribution_splitting", "scaling_degree", "locality", "renormalization_ambiguity", "real_rows"],
        "Formal causal-perturbation obligations are not empirical GMUT confirmation or a Theory-of-Everything result.",
    ),
    "V6483R2-P03": spec(
        "lvk-o4-zero-row", "open_gap", "empirical/lvk-o4-zero-row-contract.json",
        {**COMMON, "official_format_only": True, "superevent_fields_declared": True, "selection_model_present": False, "calibration_model_present": False, "likelihood_present": False, "independent_review_present": False, "real_rows": 0},
        ["official_format_only", "superevent_fields_declared", "selection_model_present", "calibration_model_present", "likelihood_present", "independent_review_present", "real_rows"],
        "The adapter ingests zero rows and remains open_gap without a preregistered likelihood, systematics, real data, and independent review.",
    ),
    "V6483R2-P04": spec(
        "release-handover", "represented", "thos/release-handover-contract.json",
        {**COMMON, "baseline_identity": True, "change_authority_field": True, "build_provenance": True, "rollback_plan": True, "workload_budget": True, "readback": True, "real_operators": 0},
        ["baseline_identity", "change_authority_field", "build_provenance", "rollback_plan", "workload_budget", "readback", "real_operators"],
        "Synthetic handover evidence is represented/proxy only and does not establish deployment, employment, or professional competence.",
    ),
    "V6483R2-P05": spec(
        "client-attestation", "represented", "freed-id/client-attestation-profile.json",
        {**COMMON, "draft_watch": True, "client_instance_key_bound": True, "challenge_bound": True, "replay_rejected": True, "algorithm_policy": True, "trust_resolution_live": False, "real_keys": 0},
        ["draft_watch", "client_instance_key_bound", "challenge_bound", "replay_rejected", "algorithm_policy", "trust_resolution_live", "real_keys"],
        "Synthetic draft-watch fixtures are nonproduction and do not establish live identity, trust governance, privacy review, or interoperability.",
    ),
    "V6483R2-P06": spec(
        "maintenance-authority", "exact_gate", "cbr/maintenance-authority-reservation.json",
        {**COMMON, "incident_matrix_present": True, "diagnostic_privacy_reserved": True, "accessible_notice_reserved": True, "affected_party_authorized": False, "maori_authority_present": False, "legal_authority_present": False, "cultural_ratification_present": False},
        ["incident_matrix_present", "diagnostic_privacy_reserved", "accessible_notice_reserved", "affected_party_authorized", "maori_authority_present", "legal_authority_present", "cultural_ratification_present"],
        "Remedy, legal, cultural, Maori-authority, data-governance, and affected-party decisions remain exact-gated.",
    ),
    "V6483R2-P07": spec(
        "deterministic-cbor", "completed", "formats/cbor-cose-contract.json",
        {**COMMON, "shortest_form_required": True, "map_order_required": True, "duplicate_keys_rejected": True, "unsupported_algorithm_rejected": True, "nesting_budget": 32, "output_budget": 1048576, "external_payloads_processed": 0},
        ["shortest_form_required", "map_order_required", "duplicate_keys_rejected", "unsupported_algorithm_rejected", "nesting_budget", "output_budget", "external_payloads_processed"],
        "Bounded synthetic parser fixtures are not production parsing, interoperability, privacy, or exhaustive-security evidence.",
    ),
    "V6483R2-P08": spec(
        "accessible-change-diff", "completed", "accessibility/change-diff-contract.json",
        {**COMMON, "insert_delete_semantics": True, "non_colour_cue": True, "linear_reading_order": True, "keyboard_order_declared": True, "copy_print_plain_text": True, "manual_evaluation_reserved": True, "affected_user_evaluation_count": 0},
        ["insert_delete_semantics", "non_colour_cue", "linear_reading_order", "keyboard_order_declared", "copy_print_plain_text", "manual_evaluation_reserved", "affected_user_evaluation_count"],
        "Structural checks reserve manual keyboard, browser, assistive-technology, Maori-language, and affected-user evaluation.",
    ),
    "V6483R2-P09": spec(
        "fisher-speed-domain", "completed", "thermo-psyche/fisher-speed-contract.json",
        {**COMMON, "dynamics_declared": True, "metric_declared": True, "cost_declared": True, "units_declared": True, "domain_declared": True, "psyche_conversion": False, "personhood_measure": False},
        ["dynamics_declared", "metric_declared", "cost_declared", "units_declared", "domain_declared", "psyche_conversion", "personhood_measure"],
        "Physical information geometry is not a measure of psyche, urgency, agency, consciousness, personhood, or moral worth.",
    ),
    "V6483R2-P10": spec(
        "marginal-structural", "completed", "stage20/marginal-structural-contract.json",
        {**COMMON, "time_varying_treatment": True, "treatment_confounder_feedback": True, "stabilized_weights": True, "positivity_checked": True, "censoring_model_declared": True, "sensitivity_plan_declared": True, "real_participants": 0},
        ["time_varying_treatment", "treatment_confounder_feedback", "stabilized_weights", "positivity_checked", "censoring_model_declared", "sensitivity_plan_declared", "real_participants"],
        "A structural causal protocol with zero participants is not effectiveness, safety, causal-effect, or Stage 20 evidence.",
    ),
}


def validate(proposal_id: str, payload: dict[str, Any]) -> list[str]:
    spec_row = SURFACES[proposal_id]
    issues = []
    if payload.get("proposal_id") != proposal_id:
        issues.append("proposal_id")
    if payload.get("outcome") != spec_row["outcome"]:
        issues.append("outcome")
    for key, expected in spec_row["required"].items():
        if payload.get(key) != expected:
            issues.append(key)
    if payload.get("boundary") != spec_row["boundary"]:
        issues.append("boundary")
    return sorted(set(issues))


def mutated_value(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1 if value else 1
    if value is None:
        return "unexpected"
    return None


def write_json(root: Path, relative: str, payload: Any) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build_surface(proposal_id: str, output_root: Path = PHASE) -> dict[str, Any]:
    spec_row = SURFACES[proposal_id]
    positive = {"schema": f"ghc.family.v648-v3-r2.{spec_row['slug']}.v1", "proposal_id": proposal_id, "outcome": spec_row["outcome"], **spec_row["required"], "boundary": spec_row["boundary"]}
    positive_issues = validate(proposal_id, positive)
    if positive_issues:
        raise RuntimeError(f"positive fixture failed: {positive_issues}")
    mutations = []
    for index, key in enumerate(spec_row["mutation_keys"], start=1):
        candidate = copy.deepcopy(positive)
        candidate[key] = mutated_value(candidate[key])
        issues = validate(proposal_id, candidate)
        if not issues:
            raise RuntimeError(f"mutation {key} was accepted")
        mutations.append({"mutation_id": f"{proposal_id}-MUT-{index:02d}", "changed_field": key, "rejected": True, "issue_classes": issues})
    contract = {**positive, "valid_fixture_passed": True, "mutation_count": len(mutations), "all_mutations_rejected": True}
    write_json(output_root, spec_row["path"], contract)
    mutation_path = str(Path(spec_row["path"]).with_name(Path(spec_row["path"]).stem + "-mutations.json")).replace("\\", "/")
    write_json(output_root, mutation_path, {"schema": f"ghc.family.v648-v3-r2.{spec_row['slug']}.mutations.v1", "proposal_id": proposal_id, "count": len(mutations), "mutations": mutations, "all_rejected": True, "boundary": spec_row["boundary"]})
    witness = {
        "schema": "ghc.family.v648-v3-r2.runner-witness.v1", "proposal_id": proposal_id, "runner_slug": spec_row["slug"],
        "valid_fixture_passed": True, "rejected_mutation_count": len(mutations), "outcome": spec_row["outcome"],
        "same_owner_only": True, "independent_reproduction": False, "boundary": spec_row["boundary"],
    }
    write_json(output_root, f"validation/runner-witnesses/{spec_row['slug']}.json", witness)
    return witness


def main_for(proposal_id: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=PHASE)
    args = parser.parse_args()
    witness = build_surface(proposal_id, args.output_root)
    print(json.dumps({"proposal": proposal_id, "outcome": witness["outcome"], "mutations": witness["rejected_mutation_count"], "valid": witness["valid_fixture_passed"]}, sort_keys=True))
    return 0
