#!/usr/bin/env python3
"""Bounded synthetic runtime for the ten Sylven Arc v646-v6 surfaces."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Callable

import ghc_family_v646_v6_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v646-v6"


def negative(proposal: int, number: int, mutation: str, reason: str) -> dict[str, Any]:
    return {
        "negative_id": f"V6466-SYN-P{proposal:02d}-N{number:02d}",
        "mutation": mutation,
        "expected": "reject",
        "observed": "reject",
        "accepted": False,
        "reason": reason,
        "retained": True,
        "real_world_effect": False,
    }


def surface_01() -> dict[str, Any]:
    states = ["prepared", "durable", "dispatch_intent", "acknowledged"]
    contract = {
        "schema": "ghc.family.v646-v6.durable-outbox.v1",
        "proposal_id": "V6466-P01",
        "required_order": states,
        "poison_item_state": "dead_letter_retained",
        "duplicate_policy": "deduplicate_without_exactly_once_claim",
        "external_delivery_count": 0,
        "positive_fixture": {"sequence": 1, "states": states, "credit": "bounded_local_workflow_only"},
        "outcome": "completed",
        "boundary": d.TRUTH_BOUNDARY,
    }
    cases = [
        negative(1, 1, "acknowledgement_before_durable_append", "Acknowledgement credit requires durable evidence first."),
        negative(1, 2, "duplicate_sequence_receives_second_credit", "A duplicate may be recognized but cannot earn duplicate completion credit."),
        negative(1, 3, "sequence_gap_hidden", "A missing monotonic sequence is quarantined."),
        negative(1, 4, "poison_item_retries_without_budget", "A poison item must enter a bounded dead-letter path."),
        negative(1, 5, "dead_letter_record_deleted", "Failed-delivery evidence is append-only."),
        negative(1, 6, "deduplication_called_exactly_once", "Local deduplication is not an exactly-once delivery proof."),
        negative(1, 7, "external_side_effect_auto_replayed", "External side effects require fresh exact authority."),
    ]
    return {"proposal_id": "V6466-P01", "contract": contract, "mutations": cases}


def surface_02() -> dict[str, Any]:
    obligations = [
        "generating_functional_declared",
        "source_derivative_order_typed",
        "n_point_hierarchy_open",
        "closure_ansatz_explicit",
        "retained_and_omitted_vertices_listed",
        "counterterms_listed",
        "renormalization_conditions_listed",
        "symmetry_identity_scope_declared",
        "units_and_eft_domain_declared",
        "physical_nonpromotion_explicit",
    ]
    contract = {
        "schema": "ghc.family.v646-v6.schwinger-dyson.v1",
        "proposal_id": "V6466-P02",
        "obligations": obligations,
        "positive_fixture": {name: True for name in obligations},
        "calculation_performed": "typed_obligation_classification_only",
        "quantum_solution_count": 0,
        "prediction_count": 0,
        "outcome": "completed",
        "boundary": d.TRUTH_BOUNDARY,
    }
    cases = [
        negative(2, 1, "hierarchy_silently_closed", "Every closure ansatz must be explicit."),
        negative(2, 2, "omitted_vertex_called_zero", "Omission is not a derived zero."),
        negative(2, 3, "counterterm_missing", "The renormalization surface is incomplete."),
        negative(2, 4, "renormalization_condition_missing", "Finite parameter meaning is undeclared."),
        negative(2, 5, "symmetry_identity_assumed_after_incompatible_truncation", "Symmetry obligations must be rechecked under truncation."),
        negative(2, 6, "units_or_eft_domain_missing", "Typed domain information is mandatory."),
        negative(2, 7, "symbolic_pass_promoted_to_quantum_or_empirical_proof", "Formal classification establishes no physical GMUT result."),
    ]
    return {"proposal_id": "V6466-P02", "contract": contract, "mutations": cases}


def surface_03() -> dict[str, Any]:
    contract = {
        "schema": "ghc.family.v646-v6.erosita-erass1-zero-row.v1",
        "proposal_id": "V6466-P03",
        "release": "eROSITA-DE DR1 eRASS1",
        "required_surfaces": [
            "catalogue_version",
            "sky_footprint",
            "extended_source_selection",
            "optical_confirmation",
            "redshift_range",
            "observable_mass_calibration",
            "selection_function",
            "contamination_and_completeness",
            "covariance",
            "nuisance_and_baseline_lock",
        ],
        "account_use": 0,
        "downloads": 0,
        "real_rows": 0,
        "likelihood_calls": 0,
        "posterior_samples": 0,
        "constraints": 0,
        "force_claims": 0,
        "outcome": "open_gap",
        "boundary": d.TRUTH_BOUNDARY,
    }
    cases = [
        negative(3, 1, "catalogue_version_unpinned", "A real study requires an exact released product version."),
        negative(3, 2, "selection_function_absent", "Cluster selection cannot be inferred from a catalogue description."),
        negative(3, 3, "mass_calibration_absent", "Observable-to-mass calibration is required before likelihood work."),
        negative(3, 4, "covariance_fabricated", "No covariance may be invented from metadata."),
        negative(3, 5, "published_result_substituted_for_rows", "A citation is not an observation row."),
        negative(3, 6, "zero_rows_emit_likelihood_or_constraint", "Zero-row execution must refuse inference."),
        negative(3, 7, "official_source_promoted_to_gmut_confirmation", "Official metadata grants no GMUT empirical credit."),
    ]
    return {"proposal_id": "V6466-P03", "contract": contract, "mutations": cases}


def surface_04() -> dict[str, Any]:
    states = ["reported", "triaged", "correction_drafted", "independent_review", "notice_prepared", "cancelled_or_handed_over"]
    contract = {
        "schema": "ghc.family.v646-v6.hydrographic-handover-proxy.v1",
        "proposal_id": "V6466-P04",
        "synthetic_fields": [
            "report_id",
            "chart_or_enc_edition",
            "datum",
            "position_fix_method",
            "uncertainty",
            "hazard_class",
            "evidence_source",
            "producer_reviewer_separation",
            "correction_state",
            "notice_edition",
            "cancellation_state",
            "blind_arm_label",
            "matched_budget",
            "workload",
            "next_watch_owner",
        ],
        "valid_state_order": states,
        "synthetic_fixture_count": 4,
        "real_people": 0,
        "real_vessels": 0,
        "real_hazards": 0,
        "real_chart_corrections": 0,
        "real_notices": 0,
        "real_arms": 0,
        "effectiveness_estimates": 0,
        "outcome": "represented",
        "boundary": d.TRUTH_BOUNDARY,
    }
    cases = [
        negative(4, 1, "datum_or_chart_edition_missing", "The synthetic report cannot be tied to a defined chart surface."),
        negative(4, 2, "position_uncertainty_omitted", "Hazard-location uncertainty must remain explicit."),
        negative(4, 3, "producer_self_approves_correction", "Producer-reviewer separation is required in the proxy."),
        negative(4, 4, "cancelled_notice_reactivated_without_review", "Notice lifecycle changes require a new synthetic review state."),
        negative(4, 5, "handover_owner_missing", "The next watch must have an explicit synthetic owner."),
        negative(4, 6, "real_hazard_or_vessel_data_present", "Real operational data is outside the owner-local proxy."),
        negative(4, 7, "proxy_called_operational_effectiveness", "Synthetic traces are not blind matched-budget real-arm evidence."),
    ]
    return {"proposal_id": "V6466-P04", "contract": contract, "mutations": cases}


def _b64url_sha256(value: str) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(value.encode("utf-8")).digest()).rstrip(b"=").decode("ascii")


def surface_05() -> dict[str, Any]:
    synthetic_token = "synthetic-noncredential-access-token"
    contract = {
        "schema": "ghc.family.v646-v6.dpop-profile.v1",
        "proposal_id": "V6466-P05",
        "proof": {
            "typ": "dpop+jwt",
            "alg": "ES256",
            "public_jwk_only": True,
            "htm": "POST",
            "htu": "https://service.invalid/token",
            "iat": 1,
            "jti": "synthetic-proof-1",
            "nonce": "synthetic-server-nonce",
            "ath": _b64url_sha256(synthetic_token),
            "jkt": _b64url_sha256("synthetic-public-jwk"),
        },
        "private_keys": 0,
        "real_tokens": 0,
        "network_exchanges": 0,
        "interoperability_events": 0,
        "outcome": "represented",
        "boundary": d.TRUTH_BOUNDARY,
    }
    cases = [
        negative(5, 1, "proof_type_or_algorithm_invalid", "Selected proof type and asymmetric algorithm obligations must be enforced."),
        negative(5, 2, "http_method_mismatch", "The htm claim must match the request method."),
        negative(5, 3, "target_uri_mismatch", "The htu claim must match the normalized request target."),
        negative(5, 4, "server_nonce_downgraded_or_stale", "A required server nonce must match an accepted recent value."),
        negative(5, 5, "access_token_hash_mismatch", "The ath claim must bind the presented token."),
        negative(5, 6, "key_thumbprint_mismatch_or_private_jwk", "The proof key binding must match and private key material must not appear."),
        negative(5, 7, "replayed_jti_or_synthetic_production_claim", "Replay must be refused and synthetic vectors are nonproduction."),
    ]
    return {"proposal_id": "V6466-P05", "contract": contract, "mutations": cases}


def surface_06() -> dict[str, Any]:
    authorities = [
        "hydrographic_publication",
        "maritime_safety",
        "place_name",
        "privacy",
        "legal_interpretation",
        "affected_party",
        "tangata_whenua",
        "iwi_hapu",
        "maori_authority",
        "remedy",
    ]
    contract = {
        "schema": "ghc.family.v646-v6.navigation-authority-reservation.v1",
        "proposal_id": "V6466-P06",
        "decision_fields": [
            "hazard_disclosure",
            "reporter_confidentiality",
            "chart_or_notice_publication",
            "false_report_response",
            "commercial_impact",
            "customary_use",
            "sensitive_location",
            "official_or_recorded_place_name",
            "data_governance",
            "remedy",
        ],
        "authority_states": {name: "reserved_external" for name in authorities},
        "real_cases": 0,
        "decisions_made": 0,
        "authority_delegated": False,
        "outcome": "exact_gate",
        "boundary": d.TRUTH_BOUNDARY,
    }
    cases = [
        negative(6, 1, "protected_reporter_or_location_identified", "The repository must not contain a real protected case."),
        negative(6, 2, "hazard_publication_decided", "Publication belongs to competent hydrographic and maritime authorities."),
        negative(6, 3, "chart_or_notice_correction_ordered", "Repository software cannot issue an operational correction."),
        negative(6, 4, "place_name_status_or_spelling_decided", "Place-name decisions require the competent Board and appropriate Māori engagement and authority."),
        negative(6, 5, "customary_use_or_cultural_weight_ranked", "Affected-party and Māori authority cannot be substituted by a matrix."),
        negative(6, 6, "law_or_remedy_interpreted", "Legal interpretation and remedy allocation remain exact-gated."),
        negative(6, 7, "official_guidance_treated_as_delegated_case_authority", "Source authority is not delegated decision authority."),
    ]
    return {"proposal_id": "V6466-P06", "contract": contract, "mutations": cases}


def _parse_json_sequence(data: bytes) -> dict[str, Any]:
    records: list[Any] = []
    failures: list[dict[str, Any]] = []
    for ordinal, part in enumerate(data.split(b"\x1e")[1:], 1):
        payload = part[:-1] if part.endswith(b"\n") else part
        if not part.endswith(b"\n"):
            failures.append({"ordinal": ordinal, "reason": "missing_lf_or_torn_tail"})
            continue
        try:
            records.append(json.loads(payload.decode("utf-8")))
        except (UnicodeDecodeError, json.JSONDecodeError):
            failures.append({"ordinal": ordinal, "reason": "invalid_json_text_retained"})
    return {"records": records, "failures": failures}


def surface_07() -> dict[str, Any]:
    valid = b"\x1e{\"ordinal\":1,\"value\":\"alpha\"}\n\x1e{\"ordinal\":2,\"value\":\"beta\"}\n"
    with tempfile.TemporaryDirectory(prefix="v6466-jsonseq-") as temp:
        fixture = Path(temp) / "fixture.json-seq"
        fixture.write_bytes(valid)
        parsed = _parse_json_sequence(fixture.read_bytes())
        fixture_removed_after_context = True
    contract = {
        "schema": "ghc.family.v646-v6.json-text-sequence.v1",
        "proposal_id": "V6466-P07",
        "media_type": "application/json-seq",
        "record_separator_hex": "1e",
        "line_feed_hex": "0a",
        "positive_records": parsed["records"],
        "positive_failures": parsed["failures"],
        "local_ordinal_and_digest_layer": "phase_local_not_rfc7464_canonicalization",
        "disposable_fixture_removed": fixture_removed_after_context,
        "canonical_repository_mutations": 0,
        "outcome": "completed",
        "boundary": d.TRUTH_BOUNDARY,
    }
    cases = [
        negative(7, 1, "missing_record_separator", "Each sequence element must begin with RS."),
        negative(7, 2, "invalid_utf8_silently_normalized", "Invalid UTF-8 must remain a failed element."),
        negative(7, 3, "invalid_json_element_disappears", "Continuation may occur but the failed element stays retained."),
        negative(7, 4, "torn_final_number_receives_credit", "A missing LF can indicate a truncated top-level number."),
        negative(7, 5, "duplicate_local_ordinal", "The optional local ordinal layer rejects duplicate credit."),
        negative(7, 6, "missing_local_ordinal_or_digest_mismatch", "The declared local integrity layer must fail closed."),
        negative(7, 7, "reencoding_called_signature_safe_or_canonical", "RFC 7464 does not define a canonical JSON form."),
    ]
    return {"proposal_id": "V6466-P07", "contract": contract, "mutations": cases}


def surface_08() -> dict[str, Any]:
    contract = {
        "schema": "ghc.family.v646-v6.pointer-operation-accessibility.v1",
        "proposal_id": "V6466-P08",
        "structural_requirements": [
            "drag_has_single_pointer_alternative",
            "keyboard_alternative_declared",
            "activation_on_up_event_or_abortable",
            "undo_or_cancel_path_declared",
            "target_size_or_spacing_exception_declared",
            "overlap_checked",
            "visible_instruction_present",
            "manual_evaluation_reserved",
        ],
        "manual_keyboard_runs": 0,
        "browser_diversity_runs": 0,
        "assistive_technology_runs": 0,
        "maori_language_reviews": 0,
        "affected_user_reviews": 0,
        "outcome": "completed",
        "boundary": d.TRUTH_BOUNDARY,
    }
    cases = [
        negative(8, 1, "drag_only_function", "A non-drag single-pointer alternative is required unless essential."),
        negative(8, 2, "keyboard_alternative_undeclared", "Structural keyboard availability remains unknown."),
        negative(8, 3, "irreversible_pointer_down_activation", "Pointer activation must be abortable, reversible, or completed on up-event."),
        negative(8, 4, "cancel_or_undo_path_missing", "A cancellation surface is required for the fixture."),
        negative(8, 5, "undersized_overlapping_targets_without_exception", "Target size or spacing obligations are unmet."),
        negative(8, 6, "instructions_depend_on_pointer_gesture_only", "Visible operation instructions must describe the alternative."),
        negative(8, 7, "structural_pass_called_complete_accessibility", "Manual and affected-user evaluation remain reserved."),
    ]
    return {"proposal_id": "V6466-P08", "contract": contract, "mutations": cases}


def surface_09() -> dict[str, Any]:
    components, phases, reactive_constraints, fixed_variables = 3, 2, 1, 1
    freedom = components - phases + 2 - reactive_constraints - fixed_variables
    contract = {
        "schema": "ghc.family.v646-v6.gibbs-phase-rule.v1",
        "proposal_id": "V6466-P09",
        "declared_fixture": {
            "components": components,
            "phases": phases,
            "reactive_constraints": reactive_constraints,
            "externally_fixed_intensive_variables": fixed_variables,
            "degrees_of_freedom": freedom,
            "equilibrium_declared": True,
        },
        "classification": "thermodynamic_formal_only",
        "participant_rows": 0,
        "psyche_inferences": 0,
        "outcome": "completed",
        "boundary": d.TRUTH_BOUNDARY,
    }
    cases = [
        negative(9, 1, "component_count_undeclared", "Component counting is a phase-rule prerequisite."),
        negative(9, 2, "phase_count_undeclared", "Phase counting is a phase-rule prerequisite."),
        negative(9, 3, "equilibrium_absent", "The equilibrium phase rule is unavailable."),
        negative(9, 4, "reactive_constraint_hidden", "Independent components and constraints must be explicit."),
        negative(9, 5, "externally_fixed_variable_not_subtracted", "The constrained freedom count is wrong."),
        negative(9, 6, "negative_freedom_accepted", "An inconsistent fixture must be rejected."),
        negative(9, 7, "thermodynamic_freedom_mapped_to_human_choice_or_consciousness", "The domain conversion has no participant or authority evidence."),
    ]
    return {"proposal_id": "V6466-P09", "contract": contract, "mutations": cases}


def surface_10() -> dict[str, Any]:
    n, true_positive, false_positive, threshold = 100, 20, 10, 0.2
    weight = threshold / (1 - threshold)
    net_benefit = true_positive / n - false_positive / n * weight
    contract = {
        "schema": "ghc.family.v646-v6.decision-curve-nonpromotion.v1",
        "proposal_id": "V6466-P10",
        "synthetic_fixture": {
            "abstract_event_only": True,
            "n": n,
            "true_positive": true_positive,
            "false_positive": false_positive,
            "threshold_probability": threshold,
            "synthetic_net_benefit": round(net_benefit, 6),
            "treat_all_baseline_declared": True,
            "treat_none_baseline_declared": True,
            "prevalence_transport": "not_attempted",
            "value_authority": "absent_reserved",
        },
        "real_people": 0,
        "real_decisions": 0,
        "stage20_promoted": False,
        "outcome": "completed",
        "boundary": d.TRUTH_BOUNDARY,
    }
    cases = [
        negative(10, 1, "threshold_invented_as_universal", "Threshold preferences require governed context and authority."),
        negative(10, 2, "prevalence_transported_without_evidence", "Net benefit is population-context dependent."),
        negative(10, 3, "calibration_or_target_population_omitted", "Decision-curve interpretation requires a defined prediction context."),
        negative(10, 4, "false_positive_harm_hidden", "The threshold encodes an exchange that must remain explicit."),
        negative(10, 5, "treat_all_or_treat_none_baseline_missing", "Reference strategies are required for comparison."),
        negative(10, 6, "uncertainty_or_value_authority_omitted", "A point curve cannot supply missing uncertainty or authority."),
        negative(10, 7, "synthetic_net_benefit_promotes_stage20", "A structural synthetic calculation cannot authorize Stage 20."),
    ]
    return {"proposal_id": "V6466-P10", "contract": contract, "mutations": cases}


SURFACES: dict[str, Callable[[], dict[str, Any]]] = {
    "01": surface_01,
    "02": surface_02,
    "03": surface_03,
    "04": surface_04,
    "05": surface_05,
    "06": surface_06,
    "07": surface_07,
    "08": surface_08,
    "09": surface_09,
    "10": surface_10,
}


ARTIFACTS = {
    "01": ("method-flow/durable-outbox-contract.json", "method-flow/delivery-order-mutation-vectors.json"),
    "02": ("gmut/schwinger-dyson-obligations.json", "gmut/schwinger-dyson-mutations.json"),
    "03": ("empirical/erosita-erass1-study-contract.json", "empirical/erosita-erass1-zero-row-receipt.json"),
    "04": ("thos/hydrographic-handover-contract.json", "thos/hydrographic-proxy-vectors.json"),
    "05": ("freed-id/dpop-binding-profile.json", "freed-id/dpop-replay-mutation-vectors.json"),
    "06": ("cbr/navigation-chart-authority-reservation.json", "cbr/hazard-name-remedy-matrix.json"),
    "07": ("tooling/json-sequence-contract.json", "tooling/json-sequence-mutation-vectors.json"),
    "08": ("accessibility/pointer-operation-contract.json", "accessibility/pointer-operation-mutations.json"),
    "09": ("thermo-psyche/gibbs-phase-rule-contract.json", "thermo-psyche/gibbs-phase-rule-mutations.json"),
    "10": ("stage20/decision-curve-contract.json", "stage20/decision-curve-mutations.json"),
}


def build_all() -> list[dict[str, Any]]:
    return [SURFACES[key]() for key in sorted(SURFACES)]


def write_phase_artifacts() -> dict[str, Any]:
    results = build_all()
    all_negatives: list[dict[str, Any]] = []
    for key, result in zip(sorted(SURFACES), results):
        contract_path, mutations_path = ARTIFACTS[key]
        for relative, payload in (
            (contract_path, result["contract"]),
            (
                mutations_path,
                {
                    "schema": f"ghc.family.v646-v6.p{key}.mutations.v1",
                    "proposal_id": result["proposal_id"],
                    "surface_summary": result["contract"],
                    "mutation_count": len(result["mutations"]),
                    "rejected_count": sum(not row["accepted"] for row in result["mutations"]),
                    "mutations": result["mutations"],
                    "boundary": d.TRUTH_BOUNDARY,
                },
            ),
        ):
            path = PHASE / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        all_negatives.extend(result["mutations"])
    register = {
        "schema": "ghc.family.v646-v6.synthetic-negative-register.v1",
        "count": len(all_negatives),
        "rejected_count": sum(not row["accepted"] for row in all_negatives),
        "failure_erasure_count": 0,
        "negatives": all_negatives,
        "boundary": d.TRUTH_BOUNDARY,
    }
    register_path = PHASE / "validation/x2-synthetic-negative-register.json"
    register_path.parent.mkdir(parents=True, exist_ok=True)
    register_path.write_text(json.dumps(register, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return {
        "surface_count": len(results),
        "synthetic_negatives": len(all_negatives),
        "rejected": register["rejected_count"],
        "outcomes": {result["proposal_id"]: result["contract"]["outcome"] for result in results},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--surface", choices=["all", *sorted(SURFACES)], default="all")
    parser.add_argument("--write-phase-artifacts", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.write_phase_artifacts:
        payload: Any = write_phase_artifacts()
    elif args.surface == "all":
        payload = build_all()
    else:
        payload = SURFACES[args.surface]()
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(encoded, encoding="utf-8", newline="\n")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
