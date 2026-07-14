#!/usr/bin/env python3
"""Frozen rule and mutation model for Eiren Kestrel v643-v7.

The module contains deterministic repository fixtures only. Its canonical
rows and rejected mutations are not empirical, participant, production,
legal, cultural, accessibility-complete, or independent-team evidence.
"""

from __future__ import annotations

from typing import Any


OBSERVED = {
    "V6437-P01": "completed",
    "V6437-P02": "completed",
    "V6437-P03": "completed",
    "V6437-P04": "represented",
    "V6437-P05": "represented",
    "V6437-P06": "exact_gate",
    "V6437-P07": "completed",
    "V6437-P08": "completed",
    "V6437-P09": "completed",
    "V6437-P10": "open_gap",
}


RULES: dict[str, dict[str, Any]] = {
    "V6437-P01": {
        "required": ["claim_text_bound", "domain_bound", "population_bound", "quantifier_declared", "evidence_tier_declared", "promotion_checked", "nonpromotion_visible"],
        "exact": {"evidence_tier": "local_synthetic"},
        "forbidden": ["universalization_claim", "existence_to_uniqueness_promotion", "proxy_to_empirical_promotion"],
    },
    "V6437-P02": {
        "required": ["action_declared", "gauge_group_declared", "gauge_condition_declared", "residual_transform_declared", "observable_declared", "invariance_checked", "boundary_conditions_declared"],
        "exact": {"evidence_class": "formal_synthetic_gauge_contract"},
        "forbidden": ["gauge_choice_physical_claim", "noninvariant_observable_promoted", "gmut_confirmation_claim"],
    },
    "V6437-P03": {
        "required": ["constraints_declared", "propagation_system_declared", "principal_symbol_checked", "damping_parameters_frozen", "stability_region_bounded", "initial_boundary_compatibility", "verification_validation_split"],
        "exact": {"real_observation_rows": 0},
        "forbidden": ["universal_stability_claim", "physical_validation_claim", "empirical_confirmation_claim"],
    },
    "V6437-P04": {
        "required": ["estimand_attributes_bound", "intercurrent_events_enumerated", "strategies_preregistered", "treatment_contrast_bound", "analysis_set_frozen", "missing_data_strategy_declared", "proxy_label"],
        "exact": {"real_arms": 0, "real_participants": 0},
        "forbidden": ["thos_causal_claim", "thos_safety_claim", "thos_superiority_claim"],
    },
    "V6437-P05": {
        "required": ["verifier_scope_bound", "pairwise_subject_derived", "audience_bound", "presentation_minimized", "nonce_domain_separated", "linkability_risk_recorded", "production_boundary"],
        "exact": {"real_keys": 0, "live_presentations": 0},
        "forbidden": ["universal_subject_claim", "collusion_resistance_claim", "production_privacy_claim"],
    },
    "V6437-P06": {
        "required": ["neutral_questions_only", "collective_and_data_scope_bound", "purpose_proposed_not_decided", "benefit_terms_pending", "affected_party_required", "maori_authority_required", "cultural_and_legal_review_required"],
        "exact": {"state": "pending_exact_authority"},
        "forbidden": ["repository_authority_claim", "collective_purpose_decision", "benefit_sharing_decision", "legal_or_cultural_ratification_claim"],
    },
    "V6437-P07": {
        "required": ["codepoints_enumerated", "bidi_controls_classified", "embedding_isolate_balance_checked", "visual_order_compared", "spoof_witness_retained", "unsafe_text_quarantined", "host_unchanged"],
        "exact": {"execution_mode": "synthetic_only"},
        "forbidden": ["unsafe_bidi_accepted", "host_text_pipeline_changed", "exhaustive_security_claim"],
    },
    "V6437-P08": {
        "required": ["name_source_bound", "accname_precedence_modeled", "hidden_reference_semantics_checked", "duplicate_conflict_checked", "empty_name_rejected", "language_declared", "manual_reservation_visible"],
        "exact": {"report_type": "static_html"},
        "forbidden": ["accessibility_complete_claim", "affected_user_evaluation_claim", "screen_reader_equivalence_claim"],
    },
    "V6437-P09": {
        "required": ["constraint_set_declared", "reference_measure_declared", "lagrange_multipliers_bound", "inferential_entropy_labeled", "thermodynamic_preconditions_declared", "units_and_domains_separated", "cross_pillar_nonconversion"],
        "exact": {"model_class": "synthetic_inference_contract"},
        "forbidden": ["entropy_identity_claim", "physical_law_claim", "psyche_law_claim"],
    },
    "V6437-P10": {
        "required": ["vendor_matrix_frozen", "pairwise_identifiers_required", "collusion_adversary_declared", "live_keys_required", "consent_and_privacy_required", "independent_security_review_required", "non_generalization_rule"],
        "exact": {"state": "open", "independent_vendors": 0},
        "forbidden": ["synthetic_collusion_substitute", "unlinkability_proved_claim", "production_interoperability_claim"],
    },
}


DETAILS: dict[str, dict[str, Any]] = {
    "V6437-P01": {"evidence_class": "local_claim_scope_contract", "scientific_authority_established": False},
    "V6437-P02": {"evidence_class": "formal_synthetic_gauge_contract", "gauge_invariant_prediction_established": False, "gmut_confirmed": False},
    "V6437-P03": {"evidence_class": "synthetic_constraint_contract", "universal_stability_proved": False, "real_observation_rows": 0},
    "V6437-P04": {"evidence_class": "represented_estimand_protocol", "real_arms": 0, "real_participants": 0, "thos_effect_established": False},
    "V6437-P05": {"evidence_class": "represented_pairwise_subject_profile", "real_keys": 0, "live_presentations": 0, "production_unlinkability": False},
    "V6437-P06": {"state": "pending_exact_authority", "collective_or_cultural_decision_made": False},
    "V6437-P07": {"evidence_class": "bounded_synthetic_unicode_quarantine", "host_changed": False, "exhaustive_security": False},
    "V6437-P08": {"evidence_class": "automated_static_name_provenance", "manual_evaluation": False, "affected_user_evaluation": False},
    "V6437-P09": {"evidence_class": "synthetic_non_substitution_contract", "physical_law_established": False, "psyche_evidence": False},
    "V6437-P10": {"state": "open", "independent_vendors": 0, "live_keys": 0, "production_interoperability": False},
}


MUTATIONS: dict[str, list[tuple[str, dict[str, Any]]]] = {
    "V6437-P01": [
        ("claim-unbound", {"claim_text_bound": False}),
        ("domain-unbound", {"domain_bound": False}),
        ("population-unbound", {"population_bound": False}),
        ("quantifier-missing", {"quantifier_declared": False}),
        ("evidence-tier-promoted", {"evidence_tier": "empirical", "promotion_checked": False}),
        ("nonpromotion-hidden", {"nonpromotion_visible": False}),
        ("triple-promotion-overclaim", {"universalization_claim": True, "existence_to_uniqueness_promotion": True, "proxy_to_empirical_promotion": True}),
    ],
    "V6437-P02": [
        ("action-missing", {"action_declared": False}),
        ("gauge-group-missing", {"gauge_group_declared": False}),
        ("gauge-condition-missing", {"gauge_condition_declared": False}),
        ("residual-transform-missing", {"residual_transform_declared": False}),
        ("observable-missing", {"observable_declared": False}),
        ("invariance-unchecked", {"invariance_checked": False}),
        ("gauge-and-confirmation-overclaim", {"gauge_choice_physical_claim": True, "noninvariant_observable_promoted": True, "gmut_confirmation_claim": True}),
    ],
    "V6437-P03": [
        ("constraints-missing", {"constraints_declared": False}),
        ("propagation-system-missing", {"propagation_system_declared": False}),
        ("principal-symbol-unchecked", {"principal_symbol_checked": False}),
        ("damping-posthoc", {"damping_parameters_frozen": False}),
        ("stability-region-unbound", {"stability_region_bounded": False}),
        ("boundary-incompatible", {"initial_boundary_compatibility": False}),
        ("stability-physical-empirical-overclaim", {"universal_stability_claim": True, "physical_validation_claim": True, "empirical_confirmation_claim": True}),
    ],
    "V6437-P04": [
        ("estimand-unbound", {"estimand_attributes_bound": False}),
        ("intercurrent-events-missing", {"intercurrent_events_enumerated": False}),
        ("strategy-posthoc", {"strategies_preregistered": False}),
        ("contrast-unbound", {"treatment_contrast_bound": False}),
        ("analysis-set-posthoc", {"analysis_set_frozen": False}),
        ("unverified-real-participants", {"real_arms": 2, "real_participants": 40}),
        ("thos-causal-safety-superiority-overclaim", {"thos_causal_claim": True, "thos_safety_claim": True, "thos_superiority_claim": True}),
    ],
    "V6437-P05": [
        ("verifier-scope-unbound", {"verifier_scope_bound": False}),
        ("pairwise-subject-missing", {"pairwise_subject_derived": False}),
        ("audience-unbound", {"audience_bound": False}),
        ("presentation-overdisclosed", {"presentation_minimized": False}),
        ("nonce-domain-reused", {"nonce_domain_separated": False}),
        ("unverified-live-material", {"real_keys": 2, "live_presentations": 2}),
        ("universal-collusion-production-overclaim", {"universal_subject_claim": True, "collusion_resistance_claim": True, "production_privacy_claim": True}),
    ],
    "V6437-P06": [
        ("gate-closed", {"state": "resolved"}),
        ("nonneutral-output", {"neutral_questions_only": False}),
        ("collective-scope-unbound", {"collective_and_data_scope_bound": False}),
        ("purpose-predecided", {"purpose_proposed_not_decided": False}),
        ("affected-party-bypassed", {"affected_party_required": False}),
        ("maori-authority-bypassed", {"maori_authority_required": False}),
        ("repository-decides-authority", {"repository_authority_claim": True, "collective_purpose_decision": True, "benefit_sharing_decision": True, "legal_or_cultural_ratification_claim": True}),
    ],
    "V6437-P07": [
        ("codepoints-hidden", {"codepoints_enumerated": False}),
        ("controls-unclassified", {"bidi_controls_classified": False}),
        ("balance-unchecked", {"embedding_isolate_balance_checked": False}),
        ("visual-order-unchecked", {"visual_order_compared": False}),
        ("spoof-witness-discarded", {"spoof_witness_retained": False}),
        ("unsafe-text-not-quarantined", {"unsafe_text_quarantined": False}),
        ("bidi-host-security-overclaim", {"unsafe_bidi_accepted": True, "host_text_pipeline_changed": True, "exhaustive_security_claim": True}),
    ],
    "V6437-P08": [
        ("name-source-unbound", {"name_source_bound": False}),
        ("precedence-unmodeled", {"accname_precedence_modeled": False}),
        ("hidden-reference-unchecked", {"hidden_reference_semantics_checked": False}),
        ("duplicate-conflict-unchecked", {"duplicate_conflict_checked": False}),
        ("empty-name-accepted", {"empty_name_rejected": False}),
        ("manual-reservation-hidden", {"manual_reservation_visible": False}),
        ("accessibility-user-equivalence-overclaim", {"accessibility_complete_claim": True, "affected_user_evaluation_claim": True, "screen_reader_equivalence_claim": True}),
    ],
    "V6437-P09": [
        ("constraint-set-missing", {"constraint_set_declared": False}),
        ("reference-measure-missing", {"reference_measure_declared": False}),
        ("multipliers-unbound", {"lagrange_multipliers_bound": False}),
        ("inferential-label-missing", {"inferential_entropy_labeled": False}),
        ("thermodynamic-preconditions-missing", {"thermodynamic_preconditions_declared": False}),
        ("units-domains-conflated", {"units_and_domains_separated": False}),
        ("entropy-physical-psyche-overclaim", {"entropy_identity_claim": True, "physical_law_claim": True, "psyche_law_claim": True}),
    ],
    "V6437-P10": [
        ("vendor-matrix-missing", {"vendor_matrix_frozen": False}),
        ("pairwise-identifiers-missing", {"pairwise_identifiers_required": False}),
        ("collusion-adversary-missing", {"collusion_adversary_declared": False}),
        ("live-keys-not-required", {"live_keys_required": False}),
        ("consent-privacy-bypassed", {"consent_and_privacy_required": False}),
        ("unverified-vendors", {"independent_vendors": 2}),
        ("synthetic-proof-production-overclaim", {"synthetic_collusion_substitute": True, "unlinkability_proved_claim": True, "production_interoperability_claim": True}),
    ],
}
