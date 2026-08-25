from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "elowen-cairn" / "v669-v2"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
MUTATION_KINDS = {
    "missing_required_state",
    "ambiguous_domain_or_unit",
    "real_world_or_external_action",
    "protected_claim_promotion",
}

SURFACE_TERMS = {
    "instrument-identity": ["instrument_record", "component_record", "conflation_hold"],
    "body-neck-topology": ["body_node", "neck_node", "joint_edge", "orphan_quarantine"],
    "plate-geometry-vacancy": ["outline_vacancy", "arch_vacancy", "thickness_vacancy"],
    "internal-structure": ["support_role", "placement_vacancy", "construction_abstention"],
    "string-course-state": ["course_slot", "gauge_vacancy", "tension_vacancy", "tuning_refusal"],
    "bridge-nut-saddle": ["contact_node", "stop_relation", "fit_vacancy", "adjustment_refusal"],
    "tuning-mechanism": ["mechanism_state", "winding_direction_vacancy", "actuation_refusal"],
    "finish-claim-vacancy": ["finish_cue", "composition_vacancy", "treatment_refusal"],
    "material-claim-vacancy": ["material_cue", "species_vacancy", "authenticity_refusal"],
    "dimension-unit-profile": ["decimal_string", "si_domain", "uncertainty_obligation"],
    "condition-cue-vocabulary": ["cue_only", "diagnosis_vacancy", "observation_vacancy"],
    "structural-hold-register": ["cue_hold", "triage_vacancy", "intervention_refusal"],
    "action-state-machine": ["proposal", "approval_vacancy", "execution_forbidden", "release_forbidden"],
    "tool-identity-vacancy": ["tool_class", "competence_vacancy", "use_refusal"],
    "correction-docket-fork": ["effective_time", "recorded_time", "superseded_mask", "contested_branch"],
    "custody-location-graph": ["location_placeholder", "transfer_placeholder", "ownership_noninference"],
    "component-provenance": ["source_statement", "attribution_vacancy", "truth_vacancy"],
    "canonical-hash-domain": ["utf8_domain", "duplicate_key_refusal", "numeric_coercion_refusal"],
    "pseudonym-alias-budget": ["surrogate_alias", "correlation_ceiling", "correlation_alarm"],
    "accessible-topology-table": ["adjacency_table", "nested_list_fallback", "description_anchor"],
    "issue-escrow": ["pseudonymous_role", "expiring_lease", "queue_cap", "unresolved_carry"],
    "source-assertion-firewall": ["source_scope", "observation_vacancy", "instruction_veto"],
    "cbr-challenge-ladder": ["disclosure_minimisation", "challenge_branch", "remedy_hold"],
    "freed-id-envelope": ["zero_key", "purpose_scope", "status_service_absence", "expiry"],
    "thos-dependency-dag": ["dependency_node", "stop_token", "queue_cap", "handover_readback"],
    "gmut-string-plate-board": ["string_domain_1d", "plate_domain_2d", "bridge_interface", "constitutive_vacancy"],
    "gmut-spectral-identifiability": ["spectrum_obligation", "inverse_map_vacancy", "damping_vacancy", "zero_eigensolve"],
    "hazard-hold-schema": ["hazard_cue", "referral_hold", "risk_determination_vacancy", "release_refusal"],
    "lutherie-practice-lens": ["intake_vocabulary", "documentation_only", "competence_noninference"],
    "workload-handover-practice": ["queue_limit", "interruption_marker", "handover_readback", "handling_absence"],
    "accessible-dossier-practice": ["landmark_order", "focus_return", "zoom_reflow", "human_study_reserved"],
    "thos-omission-proxy": ["masked_arm_placeholder", "matched_budget", "stop_condition", "effectiveness_noninference"],
    "freed-id-trust-surface": ["issuer_absence", "proof_absence", "recovery_debt", "reliance_refusal"],
    "cbr-authority-boundary": ["rights_vacancy", "authority_vacancy", "affected_party_vacancy"],
    "gmut-lutherie-analogy": ["typed_analogy", "bookkeeping_only", "prediction_refusal"],
    "acoustic-psyche-nonconversion": ["acoustic_descriptor", "psyche_vacancy", "agency_nonconversion", "personhood_nonconversion"],
    "loc-instrument-zero-call": ["adapter_schema", "request_count_zero", "row_count_zero", "rights_claim_absence"],
    "human-evaluation-gap": ["participant_count_zero", "professional_review_absence", "affected_party_review_absence"],
    "instrument-authority-gate": ["competent_authority_absence", "legal_authority_absence", "maori_authority_absence"],
    "stage20-nonpromotion": ["conjunctive_vector", "all_receipts_absent", "promotion_locked"],
}

RUNNER_PROFILES = {
    "identity": ["instrument-identity", "canonical-hash-domain", "pseudonym-alias-budget"],
    "topology": ["body-neck-topology", "internal-structure", "bridge-nut-saddle"],
    "plate_vacancy": ["plate-geometry-vacancy", "gmut-string-plate-board", "gmut-spectral-identifiability"],
    "string_state": ["string-course-state", "tuning-mechanism"],
    "material_vacancy": ["finish-claim-vacancy", "material-claim-vacancy", "dimension-unit-profile"],
    "condition": ["condition-cue-vocabulary", "structural-hold-register", "hazard-hold-schema"],
    "provenance": ["correction-docket-fork", "custody-location-graph", "component-provenance"],
    "accessibility": ["accessible-topology-table", "accessible-dossier-practice", "workload-handover-practice"],
    "identity_vacancy": ["freed-id-envelope", "freed-id-trust-surface", "cbr-challenge-ladder"],
    "authority_firewall": ["cbr-authority-boundary", "instrument-authority-gate", "stage20-nonpromotion"],
}


def load_proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base = PHASE_ROOT / "x1" / "proposal-freeze-shards"
    for path in sorted(base.glob("proposals-*.json")):
        rows.extend(json.loads(path.read_text(encoding="utf-8"))["rows"])
    if len(rows) != 40 or len({row["proposal_id"] for row in rows}) != 40:
        raise RuntimeError("the immutable x1 proposal freeze is unavailable or inconsistent")
    return rows


def positive_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    slug = proposal["semantic_slug"]
    outcome = proposal["expected_disposition"]
    if outcome not in ALLOWED_OUTCOMES:
        raise ValueError(f"unsupported outcome: {outcome}")
    state = {
        "completed": "bounded_synthetic_contract",
        "represented": "typed_obligation_only",
        "open_gap": "absence_or_zero_call_preserved",
        "exact_gate": "protected_gate_preserved",
    }[outcome]
    fixture: dict[str, Any] = {
        "approval_class": proposal["approval_class"],
        "authority_status": "vacant",
        "bounded_completion_credit": 1 if outcome == "completed" else 0,
        "counts": {
            "affected_party_approvals": 0,
            "authority_acts": 0,
            "identity_events": 0,
            "measurements": 0,
            "network_requests": 0,
            "people": 0,
            "real_instruments": 0,
            "real_materials": 0,
            "real_rows": 0,
            "treatments_or_repairs": 0,
        },
        "declared_outcome": outcome,
        "domain_status": "explicit_synthetic_or_not_applicable",
        "external_actions": [],
        "owner": "Elowen Cairn",
        "phase": "v669-v2",
        "professional_status": "not_assessed",
        "proposal_id": proposal["proposal_id"],
        "protected_claims": [],
        "required_state_present": True,
        "schema": "ghc.family.lutherie-synthetic-contract.v1",
        "semantic_slug": slug,
        "state": state,
        "surface_terms": SURFACE_TERMS[slug],
        "synthetic_only": True,
        "unit_status": "explicit_domain_or_not_applicable",
        "vacancies": list(proposal["protected_gates"]),
    }
    if slug.startswith("gmut-") or slug == "acoustic-psyche-nonconversion":
        fixture["gmut_boundary"] = {
            "data_rows": 0,
            "equations_solved": 0,
            "likelihoods_fitted": 0,
            "parameters_constrained": 0,
            "typed_obligations_only": True,
        }
    if slug.startswith("thos-"):
        fixture["thos_boundary"] = {
            "effectiveness_estimates": 0,
            "governed_real_arms": 0,
            "participants_or_operators": 0,
            "proxy_only": True,
        }
    if slug.startswith("freed-id-"):
        fixture["freed_id_boundary"] = {
            "keys": 0,
            "live_lifecycle_events": 0,
            "proofs": 0,
            "status_services": 0,
            "synthetic_nonproduction": True,
        }
    if slug == "loc-instrument-zero-call":
        fixture["adapter"] = {"downloads": 0, "network_calls": 0, "rows": 0, "status": "ZERO_CALL_OPEN_GAP"}
    if slug == "human-evaluation-gap":
        fixture["evaluation"] = {"participants": 0, "professionals": 0, "status": "OPEN_GAP"}
    if slug == "instrument-authority-gate":
        fixture["gate"] = {"authorities_present": 0, "decisions": 0, "status": "EXACT_GATE"}
    if slug == "stage20-nonpromotion":
        fixture["evidence_vector"] = {
            "accessibility": 0,
            "affected_parties": 0,
            "independent_review": 0,
            "legal_cultural_maori_authority": 0,
            "live_identity": 0,
            "production": 0,
            "real_gmut_data": 0,
            "real_thos_participants": 0,
            "safety": 0,
        }
        fixture["terminal_verdict"] = "NOT_READY_FOR_STAGE_20"
    return fixture


def evaluate_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if not fixture.get("required_state_present") or not fixture.get("state"):
        reasons.append("missing_required_state")
    if fixture.get("domain_status") != "explicit_synthetic_or_not_applicable" or fixture.get("unit_status") != "explicit_domain_or_not_applicable":
        reasons.append("ambiguous_domain_or_unit")
    counts = fixture.get("counts", {})
    if not isinstance(counts, dict) or any(value != 0 for value in counts.values()) or fixture.get("external_actions"):
        reasons.append("real_world_or_external_action")
    if fixture.get("protected_claims") or fixture.get("authority_status") != "vacant" or fixture.get("professional_status") != "not_assessed":
        reasons.append("protected_claim_promotion")
    accepted = not reasons and fixture.get("synthetic_only") is True
    return {
        "accepted": accepted,
        "completion_credit": fixture.get("bounded_completion_credit", 0) if accepted else 0,
        "proposal_id": fixture.get("proposal_id"),
        "reasons": sorted(set(reasons)),
        "result": "pass" if accepted else "reject",
        "semantic_slug": fixture.get("semantic_slug"),
    }


def mutated_fixture(fixture: dict[str, Any], kind: str) -> dict[str, Any]:
    if kind not in MUTATION_KINDS:
        raise ValueError(f"unknown mutation: {kind}")
    value = copy.deepcopy(fixture)
    if kind == "missing_required_state":
        value["required_state_present"] = False
        value.pop("state", None)
    elif kind == "ambiguous_domain_or_unit":
        value["domain_status"] = "ambiguous"
        value["unit_status"] = "unspecified"
    elif kind == "real_world_or_external_action":
        value["counts"]["network_requests"] = 1
        value["external_actions"] = ["request_external_instrument_operation"]
    elif kind == "protected_claim_promotion":
        value["protected_claims"] = ["professional_or_authority_release"]
    value["mutation_kind"] = kind
    return value


def execute_contracts(proposals: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    proposals = proposals or load_proposals()
    positive: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    for proposal in proposals:
        fixture = positive_fixture(proposal)
        result = evaluate_fixture(fixture)
        positive.append({"fixture": fixture, "result": result})
        for preregistered in proposal["negative_fixtures"]:
            kind = preregistered["kind"]
            mutated = mutated_fixture(fixture, kind)
            observed = evaluate_fixture(mutated)
            mutations.append(
                {
                    "completion_credit": 0,
                    "expected": preregistered["expected"],
                    "mutation_id": preregistered["mutation_id"],
                    "mutation_kind": kind,
                    "observed": observed["result"],
                    "proposal_id": proposal["proposal_id"],
                    "reasons": observed["reasons"],
                    "retained_failed_witness": True,
                }
            )
    return {
        "mutations": mutations,
        "outcome_counts": dict(Counter(row["expected_disposition"] for row in proposals)),
        "positive": positive,
    }


def run_profile(profile: str) -> dict[str, Any]:
    if profile not in RUNNER_PROFILES:
        raise ValueError(f"unknown runner profile: {profile}")
    selected = [row for row in load_proposals() if row["semantic_slug"] in RUNNER_PROFILES[profile]]
    results = [evaluate_fixture(positive_fixture(row)) for row in selected]
    return {
        "accepted": sum(result["accepted"] for result in results),
        "external_actions": 0,
        "network_calls": 0,
        "owner": "Elowen Cairn",
        "phase": "v669-v2",
        "profile": profile,
        "results": results,
        "schema": "ghc.family.lutherie-runner-smoke.v1",
        "status": "PASS" if results and all(result["accepted"] for result in results) else "FAIL",
    }


def cli_for_profile(profile: str) -> int:
    receipt = run_profile(profile)
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt["status"] == "PASS" else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=sorted(RUNNER_PROFILES), required=True)
    args = parser.parse_args()
    return cli_for_profile(args.profile)


if __name__ == "__main__":
    raise SystemExit(main())
