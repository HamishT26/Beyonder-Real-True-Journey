#!/usr/bin/env python3
"""Frozen bounded rule and mutation model for Ilyra Fen v643-v8.

Canonical rows and rejected mutations are deterministic repository fixtures.
They are not empirical, participant, production, legal, cultural,
accessibility-complete, exhaustive-security, or independent-team evidence.
"""

from __future__ import annotations

from typing import Any


OBSERVED = {
    "V6438-P01": "completed",
    "V6438-P02": "completed",
    "V6438-P03": "completed",
    "V6438-P04": "represented",
    "V6438-P05": "represented",
    "V6438-P06": "exact_gate",
    "V6438-P07": "completed",
    "V6438-P08": "completed",
    "V6438-P09": "completed",
    "V6438-P10": "open_gap",
}


RULES: dict[str, dict[str, Any]] = {
    "V6438-P01": {
        "required": ["uncertainty_type_declared", "coverage_factor_declared", "interval_endpoints_bound", "rounding_mode_frozen", "significant_digits_justified", "covariance_label_preserved", "nonpromotion_visible"],
        "exact": {"real_measurement_rows": 0},
        "forbidden": ["interval_narrowed", "unsupported_precision_claim", "measurement_validation_claim"],
    },
    "V6438-P02": {
        "required": ["symmetry_variation_declared", "euler_lagrange_residual_tracked", "current_divergence_computed", "boundary_orientation_declared", "boundary_flux_computed", "improvement_term_declared", "bulk_boundary_balance_checked"],
        "exact": {"evidence_class": "formal_synthetic_noether_contract"},
        "forbidden": ["physical_conservation_claim", "gmut_confirmation_claim", "theory_of_everything_claim"],
    },
    "V6438-P03": {
        "required": ["background_equations_declared", "background_residual_checked", "expansion_order_labeled", "tadpole_cancellation_checked", "operator_provenance_bound", "gauge_label_declared", "order_separation_checked"],
        "exact": {"real_observation_rows": 0},
        "forbidden": ["background_is_physical_solution_claim", "cosmological_prediction_claim", "empirical_confirmation_claim"],
    },
    "V6438-P04": {
        "required": ["eligibility_version_frozen", "screening_denominator_bound", "exclusion_reasons_complete", "consent_precedes_allocation", "flow_conservation_checked", "missing_screening_rows_visible", "proxy_label"],
        "exact": {"real_participants": 0, "real_arms": 0},
        "forbidden": ["thos_effectiveness_claim", "thos_safety_claim", "selection_bias_resolved_claim"],
    },
    "V6438-P05": {
        "required": ["proof_purpose_bound", "verifier_domain_bound", "challenge_unique_within_window", "transaction_digest_bound", "holder_relation_explicit", "verification_relationship_checked", "production_boundary"],
        "exact": {"real_keys": 0, "live_proofs": 0},
        "forbidden": ["cross_context_replay_accepted", "production_cryptography_claim", "interoperability_claim"],
    },
    "V6438-P06": {
        "required": ["neutral_questions_only", "community_identity_not_inferred", "affected_party_required", "maori_authority_where_applicable", "remedy_determination_pending", "residual_risk_acceptance_pending", "cultural_and_legal_review_required"],
        "exact": {"state": "pending_exact_authority"},
        "forbidden": ["repository_harm_definition", "repository_remedy_decision", "legal_or_cultural_ratification_claim"],
    },
    "V6438-P07": {
        "required": ["static_html_only", "active_elements_inventoried", "event_handlers_absent", "url_schemes_allowlisted", "remote_embeds_absent", "csp_draft_status_visible", "host_unchanged"],
        "exact": {"execution_mode": "synthetic_static_scan"},
        "forbidden": ["browser_security_assurance_claim", "exhaustive_security_claim", "deployment_security_claim"],
    },
    "V6438-P08": {
        "required": ["data_table_role_declared", "caption_present", "header_ids_unique", "data_cell_headers_resolved", "scope_consistent", "linearization_preserves_context", "manual_evaluation_reserved"],
        "exact": {"report_type": "static_html"},
        "forbidden": ["accessibility_complete_claim", "assistive_technology_equivalence_claim", "affected_user_evaluation_claim"],
    },
    "V6438-P09": {
        "required": ["spectrum_bound_declared", "population_inversion_declared", "equilibrium_class_declared", "entropy_convention_declared", "physical_units_declared", "temperature_kind_labeled", "cross_pillar_nonconversion"],
        "exact": {"model_class": "synthetic_temperature_classifier"},
        "forbidden": ["effective_equals_thermodynamic_claim", "psyche_law_claim", "cross_pillar_identity_claim"],
    },
    "V6438-P10": {
        "required": ["gmut_observable_map_required", "licensed_real_rows_required", "joint_covariance_required", "nuisance_plan_required", "external_baseline_frozen", "blind_holdout_required", "independent_review_required"],
        "exact": {"state": "open", "real_rows": 0},
        "forbidden": ["synthetic_likelihood_substitute", "likelihood_result_claim", "empirical_confirmation_claim"],
    },
}


DETAILS: dict[str, dict[str, Any]] = {
    "V6438-P01": {"evidence_class": "local_uncertainty_reporting_contract", "real_measurement_rows": 0, "measurement_validation": False},
    "V6438-P02": {"evidence_class": "formal_synthetic_noether_contract", "physical_conservation_established": False, "gmut_confirmed": False},
    "V6438-P03": {"evidence_class": "formal_synthetic_perturbation_contract", "real_observation_rows": 0, "cosmological_prediction_established": False},
    "V6438-P04": {"evidence_class": "represented_screening_flow_protocol", "real_participants": 0, "real_arms": 0, "thos_effect_established": False},
    "V6438-P05": {"evidence_class": "represented_proof_binding_profile", "real_keys": 0, "live_proofs": 0, "production_interoperability": False},
    "V6438-P06": {"state": "pending_exact_authority", "harm_or_remedy_decision_made": False},
    "V6438-P07": {"evidence_class": "bounded_static_active_content_scan", "host_changed": False, "exhaustive_security": False},
    "V6438-P08": {"evidence_class": "automated_static_table_structure", "manual_evaluation": False, "affected_user_evaluation": False},
    "V6438-P09": {"evidence_class": "synthetic_temperature_non_substitution_contract", "physical_law_established": False, "psyche_evidence": False},
    "V6438-P10": {"state": "open", "real_rows": 0, "likelihood_executed": False, "independent_review_completed": False},
}


MUTATIONS: dict[str, list[tuple[str, dict[str, Any]]]] = {
    "V6438-P01": [
        ("uncertainty-type-missing", {"uncertainty_type_declared": False}),
        ("coverage-factor-missing", {"coverage_factor_declared": False}),
        ("interval-unbound", {"interval_endpoints_bound": False}),
        ("rounding-posthoc", {"rounding_mode_frozen": False}),
        ("digits-unjustified", {"significant_digits_justified": False}),
        ("unverified-real-measurements", {"real_measurement_rows": 10}),
        ("narrowing-precision-validation-overclaim", {"interval_narrowed": True, "unsupported_precision_claim": True, "measurement_validation_claim": True}),
    ],
    "V6438-P02": [
        ("symmetry-variation-missing", {"symmetry_variation_declared": False}),
        ("euler-lagrange-residual-missing", {"euler_lagrange_residual_tracked": False}),
        ("current-divergence-missing", {"current_divergence_computed": False}),
        ("boundary-orientation-missing", {"boundary_orientation_declared": False}),
        ("boundary-flux-missing", {"boundary_flux_computed": False}),
        ("improvement-term-hidden", {"improvement_term_declared": False}),
        ("conservation-confirmation-toe-overclaim", {"physical_conservation_claim": True, "gmut_confirmation_claim": True, "theory_of_everything_claim": True}),
    ],
    "V6438-P03": [
        ("background-equations-missing", {"background_equations_declared": False}),
        ("background-residual-unchecked", {"background_residual_checked": False}),
        ("expansion-order-unlabeled", {"expansion_order_labeled": False}),
        ("tadpole-unchecked", {"tadpole_cancellation_checked": False}),
        ("operator-provenance-unbound", {"operator_provenance_bound": False}),
        ("unverified-real-observations", {"real_observation_rows": 12}),
        ("physical-prediction-confirmation-overclaim", {"background_is_physical_solution_claim": True, "cosmological_prediction_claim": True, "empirical_confirmation_claim": True}),
    ],
    "V6438-P04": [
        ("eligibility-version-drift", {"eligibility_version_frozen": False}),
        ("screening-denominator-unbound", {"screening_denominator_bound": False}),
        ("exclusion-reasons-incomplete", {"exclusion_reasons_complete": False}),
        ("allocation-before-consent", {"consent_precedes_allocation": False}),
        ("flow-conservation-unchecked", {"flow_conservation_checked": False}),
        ("unverified-real-participants", {"real_participants": 40, "real_arms": 2}),
        ("effect-safety-selection-overclaim", {"thos_effectiveness_claim": True, "thos_safety_claim": True, "selection_bias_resolved_claim": True}),
    ],
    "V6438-P05": [
        ("proof-purpose-unbound", {"proof_purpose_bound": False}),
        ("verifier-domain-unbound", {"verifier_domain_bound": False}),
        ("challenge-reused", {"challenge_unique_within_window": False}),
        ("transaction-unbound", {"transaction_digest_bound": False}),
        ("holder-relation-implicit", {"holder_relation_explicit": False}),
        ("unverified-real-proofs", {"real_keys": 2, "live_proofs": 2}),
        ("replay-production-interoperability-overclaim", {"cross_context_replay_accepted": True, "production_cryptography_claim": True, "interoperability_claim": True}),
    ],
    "V6438-P06": [
        ("gate-closed", {"state": "resolved"}),
        ("nonneutral-questions", {"neutral_questions_only": False}),
        ("community-inferred", {"community_identity_not_inferred": False}),
        ("affected-party-bypassed", {"affected_party_required": False}),
        ("maori-authority-bypassed", {"maori_authority_where_applicable": False}),
        ("remedy-predecided", {"remedy_determination_pending": False}),
        ("repository-harm-remedy-ratification", {"repository_harm_definition": True, "repository_remedy_decision": True, "legal_or_cultural_ratification_claim": True}),
    ],
    "V6438-P07": [
        ("static-only-missing", {"static_html_only": False}),
        ("active-elements-uninventoried", {"active_elements_inventoried": False}),
        ("event-handler-present", {"event_handlers_absent": False}),
        ("unsafe-scheme", {"url_schemes_allowlisted": False}),
        ("remote-embed-present", {"remote_embeds_absent": False}),
        ("csp-status-hidden", {"csp_draft_status_visible": False}),
        ("browser-exhaustive-deployment-overclaim", {"browser_security_assurance_claim": True, "exhaustive_security_claim": True, "deployment_security_claim": True}),
    ],
    "V6438-P08": [
        ("table-role-missing", {"data_table_role_declared": False}),
        ("caption-missing", {"caption_present": False}),
        ("duplicate-header-id", {"header_ids_unique": False}),
        ("orphan-data-cell", {"data_cell_headers_resolved": False}),
        ("scope-conflict", {"scope_consistent": False}),
        ("linearization-loses-context", {"linearization_preserves_context": False}),
        ("accessibility-equivalence-user-overclaim", {"accessibility_complete_claim": True, "assistive_technology_equivalence_claim": True, "affected_user_evaluation_claim": True}),
    ],
    "V6438-P09": [
        ("spectrum-bound-missing", {"spectrum_bound_declared": False}),
        ("population-inversion-missing", {"population_inversion_declared": False}),
        ("equilibrium-class-missing", {"equilibrium_class_declared": False}),
        ("entropy-convention-missing", {"entropy_convention_declared": False}),
        ("units-missing", {"physical_units_declared": False}),
        ("temperature-kind-unlabeled", {"temperature_kind_labeled": False}),
        ("effective-psyche-identity-overclaim", {"effective_equals_thermodynamic_claim": True, "psyche_law_claim": True, "cross_pillar_identity_claim": True}),
    ],
    "V6438-P10": [
        ("observable-map-not-required", {"gmut_observable_map_required": False}),
        ("real-rows-not-required", {"licensed_real_rows_required": False}),
        ("joint-covariance-not-required", {"joint_covariance_required": False}),
        ("nuisance-plan-not-required", {"nuisance_plan_required": False}),
        ("baseline-not-frozen", {"external_baseline_frozen": False}),
        ("unverified-real-rows", {"real_rows": 100}),
        ("synthetic-likelihood-confirmation-overclaim", {"synthetic_likelihood_substitute": True, "likelihood_result_claim": True, "empirical_confirmation_claim": True}),
    ],
}
