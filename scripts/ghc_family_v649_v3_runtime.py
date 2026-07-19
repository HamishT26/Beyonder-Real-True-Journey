#!/usr/bin/env python3
"""Bounded synthetic runtime for Sable Rook v649-v3.

The runtime evaluates preregistered software fixtures only.  It performs no
network access, empirical fit, participant operation, production identity
operation, food-safety decision, legal interpretation, or cultural decision.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path
from typing import Any


ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
OUTCOMES = {
    "V6493-P01": "completed",
    "V6493-P02": "completed",
    "V6493-P03": "open_gap",
    "V6493-P04": "represented",
    "V6493-P05": "represented",
    "V6493-P06": "exact_gate",
    "V6493-P07": "completed",
    "V6493-P08": "completed",
    "V6493-P09": "completed",
    "V6493-P10": "completed",
}

BOUNDARY = (
    "Bounded synthetic or formal evidence only; no empirical, participant, "
    "professional, food-safety, legal, cultural, Māori-authority, production, "
    "deployment, privacy-complete, exhaustive-security, accessibility-complete, "
    "independent-reproduction, AGI or ASI, consciousness or personhood, "
    "Theory-of-Everything, or Stage 20 credit."
)

COMMON_FALSE = (
    "empirical_claim",
    "participant_outcome",
    "professional_authority",
    "food_safety_decision",
    "legal_decision",
    "cultural_decision",
    "maori_authority_decision",
    "production_claim",
    "privacy_complete",
    "security_exhaustive",
    "accessibility_complete",
    "independent_reproduction",
    "agi_or_asi_claim",
    "consciousness_or_personhood_claim",
    "theory_of_everything_claim",
    "stage20_ready",
)


def _base() -> dict[str, Any]:
    return {name: False for name in COMMON_FALSE}


def accepting_fixture(proposal_id: str) -> dict[str, Any]:
    """Return the frozen accepting fixture for one proposal."""
    payload = _base()
    if proposal_id == "V6493-P01":
        payload.update(
            root_id="./",
            metadata_descriptor_about="./",
            entity_ids=["./", "data/a.json", "context/person"],
            root_has_part=["data/a.json"],
            contextual_ids=["context/person"],
            reachable_local_ids=["./", "data/a.json"],
            checksums_match=True,
            external_reference_local_preservation=False,
            source_units=2,
            source_independent=True,
            duplicate_credit=False,
            provenance_complete=False,
        )
    elif proposal_id == "V6493-P02":
        payload.update(
            region_order="O1_subset_O2",
            isotony=True,
            spacelike_commutation=True,
            covariance_declared=True,
            spectrum_scope_declared=True,
            vacuum_scope_declared=True,
            additivity_declared=True,
            time_slice_declared=True,
            observable_algebra_only=True,
            gauge_scope_declared=True,
            eft_truncation_declared=True,
            units_declared=True,
            physical_state_claim=False,
            likelihood_evaluations=0,
        )
    elif proposal_id == "V6493-P03":
        payload.update(
            catalogue="ATNF PSRCAT",
            frozen_release="2.7.0",
            archived_version_required=True,
            parameter_reference_required=True,
            uncertainty_required=True,
            selection_required=True,
            epoch_required=True,
            checksum_required=True,
            covariance_required=True,
            queries=0,
            downloads=0,
            catalogue_rows=0,
            timing_rows=0,
            covariance_rows=0,
            likelihood_evaluations=0,
            posterior_samples=0,
            parameter_constraints=0,
            force_detections=0,
        )
    elif proposal_id == "V6493-P04":
        payload.update(
            synthetic=True,
            lot_lineage=True,
            allergen_hold_preserved=True,
            recall_hold_preserved=True,
            correction_readback=True,
            accessible_notice_structural=True,
            workload=4,
            workload_ceiling=5,
            next_owner_acceptance=True,
            unresolved_distribution=False,
            recipient_information_exposed=False,
            real_people=0,
            real_food_items=0,
            real_distributions=0,
            blind_matched_budget_arms=0,
        )
    elif proposal_id == "V6493-P05":
        payload.update(
            synthetic=True,
            specification="DID Resolution v0.3 Working Draft",
            input_did="did:example:123",
            input_options_declared=True,
            resolution_metadata_declared=True,
            document_metadata_declared=True,
            version_handling=True,
            query_normalization=True,
            duplicate_parameter_rejected=True,
            cache_scope_declared=True,
            error_taxonomy_declared=True,
            draft_status_visible=True,
            requester_privacy_reserved=True,
            real_keys=0,
            real_resolutions=0,
            network_requests=0,
            interoperability_events=0,
        )
    elif proposal_id == "V6493-P06":
        payload.update(
            decision_cells={
                "food_access": "exact_gate",
                "dignity": "exact_gate",
                "disability": "exact_gate",
                "dietary_need": "exact_gate",
                "cultural_need": "exact_gate",
                "recipient_privacy": "exact_gate",
                "correction": "exact_gate",
                "recall_remedy": "exact_gate",
                "legal_interpretation": "exact_gate",
                "data_governance": "exact_gate",
                "maori_authority": "exact_gate",
            },
            real_allocations=0,
            real_disclosures=0,
            real_remedies=0,
            affected_party_acceptances=0,
            authority_generated_by_software=False,
        )
    elif proposal_id == "V6493-P07":
        payload.update(
            cards=["SIMPLE=T", "BITPIX=8", "NAXIS=0", "EXTEND=T", "END"],
            first_card="SIMPLE=T",
            end_count=1,
            card_width=80,
            header_bytes=2880,
            data_bytes=0,
            padded_total_bytes=2880,
            byte_budget=5760,
            unknown_critical_card=False,
            truncated=False,
            checksum_required=False,
            real_astronomy_product=False,
        )
    elif proposal_id == "V6493-P08":
        payload.update(
            row_headers=True,
            column_headers=True,
            cell_associations=True,
            text_legend=True,
            non_color_cues=True,
            summary=True,
            focus_order=True,
            table_alternative=True,
            print_alternative=True,
            automatic_motion=False,
            manual_review_reserved=True,
            affected_user_review_reserved=True,
        )
    elif proposal_id == "V6493-P09":
        sigma = 5.670374419e-8
        emissivity = 0.8
        area_m2 = 2.0
        temperature_k = 300.0
        payload.update(
            sigma=sigma,
            emissivity=emissivity,
            area_m2=area_m2,
            temperature_k=temperature_k,
            output_w=sigma * emissivity * area_m2 * temperature_k**4,
            output_unit="W",
            absolute_temperature=True,
            total_radiant_exitance=True,
            spectral_conversion=False,
            view_factor_claim=False,
            psyche_conversion=False,
            fundamental_law_of_mind=False,
        )
    elif proposal_id == "V6493-P10":
        payload.update(
            synthetic=True,
            participants=0,
            empirical_rows=0,
            equivalence_margin=0.2,
            margin_unit="standardized_effect",
            margin_provenance="preregistered_domain_rationale_required",
            alpha=0.05,
            tost_two_one_sided=True,
            sesoi_declared=True,
            multiplicity_plan=True,
            missingness_plan=True,
            outcome_switching=False,
            sensitivity_plan=True,
            equivalence_conclusion=False,
            causal_conclusion=False,
        )
    else:
        raise KeyError(proposal_id)
    return payload


def _require(issues: list[str], condition: bool, code: str) -> None:
    if not condition:
        issues.append(code)


def evaluate(proposal_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a single bounded fixture and return an auditable result."""
    if proposal_id not in OUTCOMES:
        raise KeyError(proposal_id)
    issues: list[str] = []
    for key in COMMON_FALSE:
        _require(issues, payload.get(key) is False, f"forbidden_promotion:{key}")

    if proposal_id == "V6493-P01":
        entity_ids = set(payload.get("entity_ids", []))
        local_ids = {item for item in entity_ids if not str(item).startswith("http")}
        _require(issues, payload.get("root_id") == "./", "root_entity")
        _require(issues, payload.get("metadata_descriptor_about") == payload.get("root_id"), "descriptor_about_root")
        _require(issues, set(payload.get("root_has_part", [])).issubset(entity_ids), "has_part_target")
        _require(issues, set(payload.get("reachable_local_ids", [])) == local_ids - set(payload.get("contextual_ids", [])), "local_reachability")
        _require(issues, payload.get("checksums_match") is True, "checksum")
        _require(issues, payload.get("external_reference_local_preservation") is False, "external_reference_boundary")
        _require(issues, payload.get("source_units", 0) >= 2 and payload.get("source_independent") is True, "source_independence")
        _require(issues, payload.get("duplicate_credit") is False, "duplicate_credit")
        _require(issues, payload.get("provenance_complete") is False, "provenance_nonpromotion")
    elif proposal_id == "V6493-P02":
        for key in ("isotony", "spacelike_commutation", "covariance_declared", "spectrum_scope_declared", "vacuum_scope_declared", "additivity_declared", "time_slice_declared", "observable_algebra_only", "gauge_scope_declared", "eft_truncation_declared", "units_declared"):
            _require(issues, payload.get(key) is True, key)
        _require(issues, payload.get("region_order") == "O1_subset_O2", "region_order")
        _require(issues, payload.get("physical_state_claim") is False, "physical_state_nonpromotion")
        _require(issues, payload.get("likelihood_evaluations") == 0, "zero_likelihood")
    elif proposal_id == "V6493-P03":
        _require(issues, payload.get("frozen_release") == "2.7.0", "release_pin")
        for key in ("archived_version_required", "parameter_reference_required", "uncertainty_required", "selection_required", "epoch_required", "checksum_required", "covariance_required"):
            _require(issues, payload.get(key) is True, key)
        for key in ("queries", "downloads", "catalogue_rows", "timing_rows", "covariance_rows", "likelihood_evaluations", "posterior_samples", "parameter_constraints", "force_detections"):
            _require(issues, payload.get(key) == 0, f"zero:{key}")
    elif proposal_id == "V6493-P04":
        for key in ("synthetic", "lot_lineage", "allergen_hold_preserved", "recall_hold_preserved", "correction_readback", "accessible_notice_structural", "next_owner_acceptance"):
            _require(issues, payload.get(key) is True, key)
        _require(issues, 0 <= payload.get("workload", 10**9) <= payload.get("workload_ceiling", -1), "workload_budget")
        for key in ("unresolved_distribution", "recipient_information_exposed"):
            _require(issues, payload.get(key) is False, key)
        for key in ("real_people", "real_food_items", "real_distributions", "blind_matched_budget_arms"):
            _require(issues, payload.get(key) == 0, f"zero:{key}")
    elif proposal_id == "V6493-P05":
        for key in ("synthetic", "input_options_declared", "resolution_metadata_declared", "document_metadata_declared", "version_handling", "query_normalization", "duplicate_parameter_rejected", "cache_scope_declared", "error_taxonomy_declared", "draft_status_visible", "requester_privacy_reserved"):
            _require(issues, payload.get(key) is True, key)
        _require(issues, str(payload.get("input_did", "")).startswith("did:"), "did_input")
        for key in ("real_keys", "real_resolutions", "network_requests", "interoperability_events"):
            _require(issues, payload.get(key) == 0, f"zero:{key}")
    elif proposal_id == "V6493-P06":
        cells = payload.get("decision_cells", {})
        _require(issues, len(cells) == 11 and all(value == "exact_gate" for value in cells.values()), "all_authority_cells_exact_gated")
        for key in ("real_allocations", "real_disclosures", "real_remedies", "affected_party_acceptances"):
            _require(issues, payload.get(key) == 0, f"zero:{key}")
        _require(issues, payload.get("authority_generated_by_software") is False, "authority_non_generation")
    elif proposal_id == "V6493-P07":
        cards = payload.get("cards", [])
        _require(issues, payload.get("first_card") == "SIMPLE=T" and cards[:1] == ["SIMPLE=T"], "primary_hdu")
        _require(issues, payload.get("end_count") == 1 and cards.count("END") == 1 and cards[-1:] == ["END"], "end_card")
        _require(issues, payload.get("card_width") == 80, "card_width")
        _require(issues, "BITPIX=8" in cards and "NAXIS=0" in cards, "typed_dimensions")
        _require(issues, payload.get("header_bytes", 0) % 2880 == 0, "header_padding")
        _require(issues, payload.get("padded_total_bytes", 0) % 2880 == 0, "total_padding")
        _require(issues, payload.get("padded_total_bytes", 10**12) <= payload.get("byte_budget", -1), "resource_budget")
        _require(issues, payload.get("unknown_critical_card") is False and payload.get("truncated") is False, "refusal_state")
        _require(issues, payload.get("real_astronomy_product") is False, "synthetic_only")
    elif proposal_id == "V6493-P08":
        for key in ("row_headers", "column_headers", "cell_associations", "text_legend", "non_color_cues", "summary", "focus_order", "table_alternative", "print_alternative", "manual_review_reserved", "affected_user_review_reserved"):
            _require(issues, payload.get(key) is True, key)
        _require(issues, payload.get("automatic_motion") is False, "no_automatic_motion")
    elif proposal_id == "V6493-P09":
        sigma = payload.get("sigma")
        emissivity = payload.get("emissivity")
        area = payload.get("area_m2")
        temperature = payload.get("temperature_k")
        numeric = all(isinstance(value, (int, float)) for value in (sigma, emissivity, area, temperature))
        _require(issues, numeric, "numeric_domain")
        if numeric:
            _require(issues, math.isclose(float(sigma), 5.670374419e-8, rel_tol=1e-12), "sigma_constant")
            _require(issues, 0 < float(emissivity) <= 1, "emissivity_domain")
            _require(issues, float(area) > 0 and float(temperature) > 0, "positive_area_and_temperature")
            expected = float(sigma) * float(emissivity) * float(area) * float(temperature) ** 4
            _require(issues, math.isclose(float(payload.get("output_w", float("nan"))), expected, rel_tol=1e-12), "stefan_boltzmann_identity")
        _require(issues, payload.get("output_unit") == "W" and payload.get("absolute_temperature") is True, "units")
        _require(issues, payload.get("total_radiant_exitance") is True and payload.get("spectral_conversion") is False, "quantity_scope")
        _require(issues, payload.get("view_factor_claim") is False and payload.get("psyche_conversion") is False and payload.get("fundamental_law_of_mind") is False, "category_firewall")
    elif proposal_id == "V6493-P10":
        _require(issues, payload.get("synthetic") is True, "synthetic_only")
        _require(issues, payload.get("participants") == 0 and payload.get("empirical_rows") == 0, "zero_participant_data")
        _require(issues, isinstance(payload.get("equivalence_margin"), (int, float)) and payload.get("equivalence_margin", 0) > 0, "positive_margin")
        _require(issues, bool(payload.get("margin_provenance")) and bool(payload.get("margin_unit")), "margin_provenance")
        _require(issues, payload.get("alpha") == 0.05 and payload.get("tost_two_one_sided") is True, "tost_definition")
        for key in ("sesoi_declared", "multiplicity_plan", "missingness_plan", "sensitivity_plan"):
            _require(issues, payload.get(key) is True, key)
        for key in ("outcome_switching", "equivalence_conclusion", "causal_conclusion"):
            _require(issues, payload.get(key) is False, key)

    return {
        "schema": "ghc.family.v649-v3.runtime-result.v1",
        "proposal_id": proposal_id,
        "observed_outcome": OUTCOMES[proposal_id],
        "passed": not issues,
        "issue_count": len(issues),
        "issues": sorted(set(issues)),
        "boundary": BOUNDARY,
    }


def mutation_fixtures(proposal_id: str) -> list[tuple[str, dict[str, Any]]]:
    """Return seven deterministic rejecting fixtures for a proposal."""
    base = accepting_fixture(proposal_id)
    changes: dict[str, list[dict[str, Any]]] = {
        "V6493-P01": [
            {"root_id": "missing"}, {"metadata_descriptor_about": "data/a.json"},
            {"root_has_part": ["missing.json"]}, {"checksums_match": False},
            {"external_reference_local_preservation": True}, {"duplicate_credit": True},
            {"provenance_complete": True},
        ],
        "V6493-P02": [
            {"isotony": False}, {"spacelike_commutation": False}, {"covariance_declared": False},
            {"spectrum_scope_declared": False}, {"observable_algebra_only": False},
            {"eft_truncation_declared": False}, {"empirical_claim": True},
        ],
        "V6493-P03": [
            {"frozen_release": "latest"}, {"parameter_reference_required": False}, {"uncertainty_required": False},
            {"queries": 1}, {"catalogue_rows": 1}, {"likelihood_evaluations": 1}, {"empirical_claim": True},
        ],
        "V6493-P04": [
            {"lot_lineage": False}, {"allergen_hold_preserved": False}, {"recall_hold_preserved": False},
            {"correction_readback": False}, {"workload": 6}, {"unresolved_distribution": True}, {"real_people": 1},
        ],
        "V6493-P05": [
            {"input_did": "not-a-did"}, {"resolution_metadata_declared": False}, {"version_handling": False},
            {"duplicate_parameter_rejected": False}, {"draft_status_visible": False}, {"real_keys": 1}, {"network_requests": 1},
        ],
        "V6493-P06": [
            {"real_allocations": 1}, {"real_disclosures": 1}, {"real_remedies": 1},
            {"affected_party_acceptances": 1}, {"authority_generated_by_software": True},
            {"legal_decision": True}, {"maori_authority_decision": True},
        ],
        "V6493-P07": [
            {"first_card": "XTENSION=IMAGE"}, {"end_count": 0}, {"card_width": 79},
            {"header_bytes": 2879}, {"padded_total_bytes": 8640}, {"truncated": True},
            {"real_astronomy_product": True},
        ],
        "V6493-P08": [
            {"row_headers": False}, {"cell_associations": False}, {"text_legend": False},
            {"non_color_cues": False}, {"focus_order": False}, {"table_alternative": False},
            {"accessibility_complete": True},
        ],
        "V6493-P09": [
            {"sigma": 1.0}, {"emissivity": 1.2}, {"area_m2": 0.0},
            {"temperature_k": -1.0}, {"output_w": 1.0}, {"psyche_conversion": True},
            {"fundamental_law_of_mind": True},
        ],
        "V6493-P10": [
            {"participants": 1}, {"equivalence_margin": 0.0}, {"margin_provenance": ""},
            {"tost_two_one_sided": False}, {"multiplicity_plan": False},
            {"outcome_switching": True}, {"stage20_ready": True},
        ],
    }
    rows: list[tuple[str, dict[str, Any]]] = []
    for index, update in enumerate(changes[proposal_id], 1):
        payload = copy.deepcopy(base)
        payload.update(update)
        rows.append((f"V6493-MUT-{proposal_id[-3:]}-{index:02d}", payload))
    return rows


def execute_mutations() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for proposal_id in OUTCOMES:
        for mutation_id, payload in mutation_fixtures(proposal_id):
            result = evaluate(proposal_id, payload)
            rows.append(
                {
                    "mutation_id": mutation_id,
                    "proposal_id": proposal_id,
                    "status": "rejected" if not result["passed"] else "unexpected_acceptance",
                    "issue_count": result["issue_count"],
                    "issues": result["issues"],
                    "retained_negative_id": mutation_id.replace("V6493-MUT", "V6493-SYN-N"),
                }
            )
    return rows


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main_for(proposal_id: str) -> int:
    parser = argparse.ArgumentParser(description=f"Evaluate bounded {proposal_id} fixtures")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = evaluate(proposal_id, payload)
    if args.output:
        write_json(args.output, result)
    else:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["passed"] else 2
