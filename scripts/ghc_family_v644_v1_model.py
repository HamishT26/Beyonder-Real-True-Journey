#!/usr/bin/env python3
"""Frozen bounded rule and mutation model for Sable Rook v644-v1.

Canonical rows and rejected mutations are deterministic repository fixtures.
They are not empirical, participant, production, legal, cultural,
accessibility-complete, exhaustive-security, or independent-team evidence.
"""

from __future__ import annotations

from typing import Any


OBSERVED = {
    "V6441-P01": "completed",
    "V6441-P02": "completed",
    "V6441-P03": "open_gap",
    "V6441-P04": "represented",
    "V6441-P05": "represented",
    "V6441-P06": "exact_gate",
    "V6441-P07": "completed",
    "V6441-P08": "completed",
    "V6441-P09": "completed",
    "V6441-P10": "completed",
}


RULES: dict[str, dict[str, Any]] = {
    "V6441-P01": {
        "required": ["work_identity_bound", "version_relations_bound", "contributor_roles_declared", "dataset_ids_bound", "code_digests_bound", "protocol_ids_bound", "source_family_collapsed"],
        "exact": {"independent_roots_claimed": 0},
        "forbidden": ["shared_lineage_ignored", "independent_corroboration_claim", "independent_reproduction_claim"],
    },
    "V6441-P02": {
        "required": ["canonical_equation_bound", "tensor_variance_checked", "si_dimensions_checked", "source_sectors_disjoint", "exchange_currents_explicit", "total_exchange_zero_checked", "improvement_freedom_declared"],
        "exact": {"evidence_class": "formal_synthetic_effective_source_contract"},
        "forbidden": ["stability_established_claim", "identifiability_established_claim", "physical_conservation_claim", "gmut_confirmation_claim", "theory_of_everything_claim"],
    },
    "V6441-P03": {
        "required": ["observable_derivation_required", "licensed_rows_required", "calibration_plan_required", "selection_function_required", "waveform_nuisance_plan_frozen", "blind_gr_baseline_required", "identifiability_review_required"],
        "exact": {"state": "open", "real_rows": 0},
        "forbidden": ["synthetic_data_substitute", "likelihood_result_claim", "empirical_confirmation_claim"],
    },
    "V6441-P04": {
        "required": ["common_time_origin_frozen", "visit_windows_frozen", "repeated_measure_schedule_bound", "decay_model_preregistered", "durability_threshold_preregistered", "intercurrent_event_strategy_bound", "attrition_visible"],
        "exact": {"real_participants": 0, "real_arms": 0},
        "forbidden": ["durable_effect_claim", "thos_safety_claim", "thos_superiority_claim"],
    },
    "V6441-P05": {
        "required": ["issuer_metadata_bound", "credential_offer_bound", "authorization_details_bound", "authorization_code_single_use", "pkce_bound", "nonce_single_use", "wallet_and_deferred_session_bound"],
        "exact": {"real_keys": 0, "live_endpoints": 0},
        "forbidden": ["cross_session_substitution_accepted", "production_issuance_claim", "interoperability_claim"],
    },
    "V6441-P06": {
        "required": ["neutral_questions_only", "affected_party_required", "maori_authority_where_applicable", "current_custodian_required", "legal_authority_required", "return_or_deletion_pending", "stewardship_transfer_pending"],
        "exact": {"state": "pending_exact_authority"},
        "forbidden": ["repository_rightful_steward_decision", "repository_return_or_deletion_decision", "maori_concept_interpretation", "legal_or_cultural_ratification_claim"],
    },
    "V6441-P07": {
        "required": ["attribute_sources_inventoried", "filter_drivers_inventoried", "hook_path_inventoried", "external_diff_inventoried", "textconv_inventoried", "config_scopes_declared", "inspection_execution_disabled"],
        "exact": {"host_changed": False},
        "forbidden": ["unapproved_execution_trusted", "host_security_assurance_claim", "exhaustive_security_claim", "deployment_security_claim"],
    },
    "V6441-P08": {
        "required": ["page_language_valid", "language_parts_bound", "language_inheritance_checked", "directionality_explicit_where_needed", "exception_scope_narrow", "pronunciation_claim_reserved", "manual_evaluation_reserved"],
        "exact": {"report_type": "static_html"},
        "forbidden": ["accessibility_complete_claim", "assistive_technology_equivalence_claim", "fluent_speaker_evaluation_claim", "affected_user_evaluation_claim"],
    },
    "V6441-P09": {
        "required": ["equilibrium_class_declared", "conjugate_perturbation_bound", "causal_response_declared", "correlation_function_declared", "transform_convention_declared", "physical_units_declared", "cross_pillar_nonconversion"],
        "exact": {"model_class": "synthetic_fluctuation_response_classifier"},
        "forbidden": ["correlation_equals_response_claim", "psyche_law_claim", "cross_pillar_identity_claim"],
    },
    "V6441-P10": {
        "required": ["domain_decisions_hash_bound", "necessary_evidence_mapped", "withdrawal_replay_required", "reversal_reason_required", "dissent_retained", "negatives_retained", "cross_domain_compensation_forbidden"],
        "exact": {"terminal_verdict": "NOT_READY_FOR_STAGE_20"},
        "forbidden": ["withdrawn_evidence_pass_unchanged", "negative_or_dissent_erased", "external_stage20_authority_claim"],
    },
}


DETAILS: dict[str, dict[str, Any]] = {
    "V6441-P01": {"evidence_class": "local_source_family_graph", "independent_roots_claimed": 0, "independent_corroboration_established": False},
    "V6441-P02": {"evidence_class": "formal_synthetic_effective_source_contract", "stability_established": False, "identifiability_established": False, "gmut_confirmed": False},
    "V6441-P03": {"state": "open", "real_rows": 0, "likelihood_executed": False, "independent_review_completed": False},
    "V6441-P04": {"evidence_class": "represented_durability_estimand", "real_participants": 0, "real_arms": 0, "durable_effect_established": False},
    "V6441-P05": {"evidence_class": "represented_issuance_session_profile", "real_keys": 0, "live_endpoints": 0, "production_interoperability": False},
    "V6441-P06": {"state": "pending_exact_authority", "return_or_stewardship_decision_made": False},
    "V6441-P07": {"evidence_class": "bounded_git_execution_surface_audit", "host_changed": False, "exhaustive_security": False},
    "V6441-P08": {"evidence_class": "automated_static_language_structure", "manual_evaluation": False, "affected_user_evaluation": False},
    "V6441-P09": {"evidence_class": "synthetic_fluctuation_response_non_substitution_contract", "physical_law_established": False, "psyche_evidence": False},
    "V6441-P10": {"evidence_class": "synthetic_stage20_decision_replay", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "external_decision_made": False},
}


MUTATIONS: dict[str, list[tuple[str, dict[str, Any]]]] = {
    "V6441-P01": [
        ("version-relation-missing", {"version_relations_bound": False}),
        ("contributor-lineage-missing", {"contributor_roles_declared": False}),
        ("dataset-lineage-missing", {"dataset_ids_bound": False}),
        ("code-lineage-missing", {"code_digests_bound": False}),
        ("protocol-lineage-missing", {"protocol_ids_bound": False}),
        ("unverified-independent-root", {"independent_roots_claimed": 2}),
        ("shared-lineage-independence-overclaim", {"shared_lineage_ignored": True, "independent_corroboration_claim": True, "independent_reproduction_claim": True}),
    ],
    "V6441-P02": [
        ("canonical-equation-unbound", {"canonical_equation_bound": False}),
        ("tensor-or-unit-unchecked", {"tensor_variance_checked": False, "si_dimensions_checked": False}),
        ("sector-overlap", {"source_sectors_disjoint": False}),
        ("exchange-current-hidden", {"exchange_currents_explicit": False}),
        ("total-exchange-unchecked", {"total_exchange_zero_checked": False}),
        ("improvement-freedom-hidden", {"improvement_freedom_declared": False}),
        ("stability-identifiability-confirmation-overclaim", {"stability_established_claim": True, "identifiability_established_claim": True, "physical_conservation_claim": True, "gmut_confirmation_claim": True, "theory_of_everything_claim": True}),
    ],
    "V6441-P03": [
        ("observable-derivation-not-required", {"observable_derivation_required": False}),
        ("licensed-rows-not-required", {"licensed_rows_required": False}),
        ("calibration-or-selection-missing", {"calibration_plan_required": False, "selection_function_required": False}),
        ("waveform-nuisance-posthoc", {"waveform_nuisance_plan_frozen": False}),
        ("baseline-not-blind", {"blind_gr_baseline_required": False}),
        ("unverified-real-rows", {"real_rows": 12}),
        ("synthetic-likelihood-confirmation-overclaim", {"synthetic_data_substitute": True, "likelihood_result_claim": True, "empirical_confirmation_claim": True}),
    ],
    "V6441-P04": [
        ("time-origin-asymmetric", {"common_time_origin_frozen": False}),
        ("visit-window-posthoc", {"visit_windows_frozen": False}),
        ("schedule-unbound", {"repeated_measure_schedule_bound": False}),
        ("decay-model-posthoc", {"decay_model_preregistered": False}),
        ("durability-threshold-posthoc", {"durability_threshold_preregistered": False}),
        ("unverified-real-arms", {"real_participants": 40, "real_arms": 2}),
        ("durability-safety-superiority-overclaim", {"durable_effect_claim": True, "thos_safety_claim": True, "thos_superiority_claim": True}),
    ],
    "V6441-P05": [
        ("issuer-metadata-unbound", {"issuer_metadata_bound": False}),
        ("credential-offer-unbound", {"credential_offer_bound": False}),
        ("authorization-details-unbound", {"authorization_details_bound": False}),
        ("authorization-code-reused", {"authorization_code_single_use": False}),
        ("pkce-or-nonce-unbound", {"pkce_bound": False, "nonce_single_use": False}),
        ("unverified-live-issuance", {"real_keys": 2, "live_endpoints": 3}),
        ("substitution-production-interoperability-overclaim", {"cross_session_substitution_accepted": True, "production_issuance_claim": True, "interoperability_claim": True}),
    ],
    "V6441-P06": [
        ("gate-closed", {"state": "resolved"}),
        ("nonneutral-questions", {"neutral_questions_only": False}),
        ("affected-party-bypassed", {"affected_party_required": False}),
        ("maori-authority-bypassed", {"maori_authority_where_applicable": False}),
        ("custodian-or-legal-authority-bypassed", {"current_custodian_required": False, "legal_authority_required": False}),
        ("return-predecided", {"return_or_deletion_pending": False, "stewardship_transfer_pending": False}),
        ("repository-steward-return-ratification", {"repository_rightful_steward_decision": True, "repository_return_or_deletion_decision": True, "maori_concept_interpretation": True, "legal_or_cultural_ratification_claim": True}),
    ],
    "V6441-P07": [
        ("attribute-source-uninventoried", {"attribute_sources_inventoried": False}),
        ("filter-driver-uninventoried", {"filter_drivers_inventoried": False}),
        ("hook-path-uninventoried", {"hook_path_inventoried": False}),
        ("external-diff-uninventoried", {"external_diff_inventoried": False}),
        ("textconv-or-scope-uninventoried", {"textconv_inventoried": False, "config_scopes_declared": False}),
        ("host-change-injected", {"host_changed": True}),
        ("execution-security-deployment-overclaim", {"unapproved_execution_trusted": True, "host_security_assurance_claim": True, "exhaustive_security_claim": True, "deployment_security_claim": True}),
    ],
    "V6441-P08": [
        ("page-language-invalid", {"page_language_valid": False}),
        ("part-language-unbound", {"language_parts_bound": False}),
        ("inheritance-unchecked", {"language_inheritance_checked": False}),
        ("directionality-implicit", {"directionality_explicit_where_needed": False}),
        ("exception-overbroad", {"exception_scope_narrow": False}),
        ("pronunciation-unreserved", {"pronunciation_claim_reserved": False}),
        ("accessibility-language-user-overclaim", {"accessibility_complete_claim": True, "assistive_technology_equivalence_claim": True, "fluent_speaker_evaluation_claim": True, "affected_user_evaluation_claim": True}),
    ],
    "V6441-P09": [
        ("equilibrium-class-missing", {"equilibrium_class_declared": False}),
        ("conjugate-pair-unbound", {"conjugate_perturbation_bound": False}),
        ("causal-response-missing", {"causal_response_declared": False}),
        ("correlation-function-missing", {"correlation_function_declared": False}),
        ("transform-convention-missing", {"transform_convention_declared": False}),
        ("units-missing", {"physical_units_declared": False}),
        ("correlation-psyche-identity-overclaim", {"correlation_equals_response_claim": True, "psyche_law_claim": True, "cross_pillar_identity_claim": True}),
    ],
    "V6441-P10": [
        ("domain-decisions-unbound", {"domain_decisions_hash_bound": False}),
        ("necessary-evidence-unmapped", {"necessary_evidence_mapped": False}),
        ("withdrawal-replay-disabled", {"withdrawal_replay_required": False}),
        ("reversal-reason-missing", {"reversal_reason_required": False}),
        ("dissent-erased", {"dissent_retained": False}),
        ("cross-domain-compensation-enabled", {"cross_domain_compensation_forbidden": False}),
        ("withdrawal-erasure-authority-overclaim", {"withdrawn_evidence_pass_unchanged": True, "negative_or_dissent_erased": True, "external_stage20_authority_claim": True}),
    ],
}
