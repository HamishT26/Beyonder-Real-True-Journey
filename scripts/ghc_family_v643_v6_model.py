#!/usr/bin/env python3
"""Frozen rule and mutation model for Sylven Arc v643-v6.

The module contains deterministic repository fixtures only.  Its canonical
rows and rejected mutations are not empirical, participant, production,
legal, cultural, accessibility-complete, or independent-team evidence.
"""

from __future__ import annotations

from typing import Any


OBSERVED = {
    "V6436-P01": "completed",
    "V6436-P02": "completed",
    "V6436-P03": "completed",
    "V6436-P04": "represented",
    "V6436-P05": "represented",
    "V6436-P06": "exact_gate",
    "V6436-P07": "completed",
    "V6436-P08": "completed",
    "V6436-P09": "completed",
    "V6436-P10": "open_gap",
}


RULES: dict[str, dict[str, Any]] = {
    "V6436-P01": {
        "required": ["term_ids_bound", "definitions_bound", "domain_range_bound", "version_declared", "split_merge_lineage", "deprecation_mapped", "unknown_version_quarantined"],
        "exact": {"vocabulary_version": "v2"},
        "forbidden": ["meaning_change_called_cosmetic", "removed_term_promoted", "semantic_authority_claim"],
    },
    "V6436-P02": {
        "required": ["small_parameter_declared", "outer_regime_declared", "inner_regime_declared", "overlap_declared", "matching_condition", "remainder_order", "uniformity_not_assumed"],
        "exact": {"evidence_class": "formal_synthetic_regime_map"},
        "forbidden": ["uniform_limit_claim", "gmut_theorem_claim", "empirical_confirmation_claim"],
    },
    "V6436-P03": {
        "required": ["manufactured_field_bound", "forcing_consistent", "mesh_sequence_declared", "error_norm_declared", "expected_order_frozen", "observed_order_checked", "verification_validation_split"],
        "exact": {"real_observation_rows": 0},
        "forbidden": ["physical_validation_claim", "gmut_confirmation_claim", "real_data_claim"],
    },
    "V6436-P04": {
        "required": ["arm_equal_prompt_schedule", "solicited_unsolicited_separated", "severity_recorded", "recoverability_recorded", "attribution_blinded", "proxy_label", "participant_gate_visible"],
        "exact": {"real_arms": 0, "real_participants": 0},
        "forbidden": ["thos_safety_claim", "causal_attribution_claim", "superiority_claim"],
    },
    "V6436-P05": {
        "required": ["pre_export_semantics_bound", "post_import_semantics_bound", "unsupported_fields_listed", "proof_metadata_preserved", "status_reference_preserved", "loss_quarantined", "production_boundary"],
        "exact": {"real_wallets": 0, "real_keys": 0},
        "forbidden": ["production_interoperability_claim", "live_resolution_claim", "identity_claim"],
    },
    "V6436-P06": {
        "required": ["neutral_questions_only", "affected_party_required", "maori_authority_required", "case_specific_scope", "cultural_ratification_required", "legal_review_required", "benefit_terms_not_invented"],
        "exact": {"state": "pending_exact_authority"},
        "forbidden": ["repository_permission_grant", "kaitiaki_determination", "benefit_sharing_decision", "legal_interpretation_claim"],
    },
    "V6436-P07": {
        "required": ["current_directory_modeled", "path_order_modeled", "pathext_modeled", "resolved_path_recorded", "allowlist_checked", "shadow_witness_retained", "host_unchanged"],
        "exact": {"execution_mode": "synthetic_only"},
        "forbidden": ["shadow_target_accepted", "host_path_changed", "exhaustive_security_claim"],
    },
    "V6436-P08": {
        "required": ["main_landmark_present", "heading_hierarchy_valid", "focus_sequence_valid", "positive_tabindex_absent", "table_headers_present", "language_declared", "manual_reservation_visible"],
        "exact": {"report_type": "static_html"},
        "forbidden": ["accessibility_complete_claim", "affected_user_evaluation_claim"],
    },
    "V6436-P09": {
        "required": ["ensemble_declared", "system_size_declared", "interaction_range_declared", "convexity_assumption_declared", "limit_order_recorded", "observable_bound", "cross_pillar_nonconversion"],
        "exact": {"model_class": "synthetic_finite_system"},
        "forbidden": ["automatic_ensemble_equivalence", "psyche_law_claim", "gmut_law_claim"],
    },
    "V6436-P10": {
        "required": ["technology_matrix_frozen", "browser_matrix_frozen", "task_matrix_frozen", "consent_required", "privacy_required", "qualified_review_required", "non_generalization_rule"],
        "exact": {"state": "open", "affected_user_participants": 0},
        "forbidden": ["automated_checks_substitute", "user_evaluation_claim", "accessibility_complete_claim"],
    },
}


DETAILS: dict[str, dict[str, Any]] = {
    "V6436-P01": {"evidence_class": "local_semantic_migration_contract", "semantic_authority_established": False},
    "V6436-P02": {"evidence_class": "formal_synthetic_regime_map", "gmut_derivation_proved": False, "uniform_asymptotics_proved": False},
    "V6436-P03": {"evidence_class": "synthetic_code_verification", "physical_validation": False, "real_observation_rows": 0},
    "V6436-P04": {"evidence_class": "represented_protocol", "real_arms": 0, "real_participants": 0, "thos_safety": False},
    "V6436-P05": {"evidence_class": "represented_migration_profile", "real_wallets": 0, "real_keys": 0, "production_interoperability": False},
    "V6436-P06": {"state": "pending_exact_authority", "concrete_cultural_or_legal_decision": False},
    "V6436-P07": {"evidence_class": "bounded_synthetic_resolution", "host_changed": False, "exhaustive_security": False},
    "V6436-P08": {"evidence_class": "automated_static_structure", "manual_evaluation": False, "affected_user_evaluation": False},
    "V6436-P09": {"evidence_class": "synthetic_ensemble_classifier", "physical_law_established": False, "psyche_evidence": False},
    "V6436-P10": {"state": "open", "affected_user_participants": 0, "accessibility_complete": False},
}


MUTATIONS: dict[str, list[tuple[str, dict[str, Any]]]] = {
    "V6436-P01": [
        ("term-id-unbound", {"term_ids_bound": False}),
        ("definition-drift", {"definitions_bound": False}),
        ("domain-range-drift", {"domain_range_bound": False}),
        ("unknown-version", {"vocabulary_version": "v3-unknown", "unknown_version_quarantined": False}),
        ("split-merge-lineage-missing", {"split_merge_lineage": False}),
        ("removed-term-promoted", {"removed_term_promoted": True}),
        ("cosmetic-and-authority-overclaim", {"meaning_change_called_cosmetic": True, "semantic_authority_claim": True}),
    ],
    "V6436-P02": [
        ("small-parameter-missing", {"small_parameter_declared": False}),
        ("outer-regime-missing", {"outer_regime_declared": False}),
        ("inner-regime-missing", {"inner_regime_declared": False}),
        ("overlap-missing", {"overlap_declared": False}),
        ("matching-missing", {"matching_condition": False}),
        ("remainder-order-missing", {"remainder_order": False}),
        ("uniform-theorem-empirical-overclaim", {"uniform_limit_claim": True, "gmut_theorem_claim": True, "empirical_confirmation_claim": True}),
    ],
    "V6436-P03": [
        ("manufactured-field-unbound", {"manufactured_field_bound": False}),
        ("forcing-inconsistent", {"forcing_consistent": False}),
        ("mesh-sequence-missing", {"mesh_sequence_declared": False}),
        ("error-norm-missing", {"error_norm_declared": False}),
        ("expected-order-posthoc", {"expected_order_frozen": False}),
        ("observed-order-unchecked", {"observed_order_checked": False}),
        ("physical-validation-overclaim", {"physical_validation_claim": True, "gmut_confirmation_claim": True, "real_data_claim": True}),
    ],
    "V6436-P04": [
        ("arm-prompt-mismatch", {"arm_equal_prompt_schedule": False}),
        ("solicitation-types-conflated", {"solicited_unsolicited_separated": False}),
        ("severity-missing", {"severity_recorded": False}),
        ("recovery-missing", {"recoverability_recorded": False}),
        ("attribution-unblinded", {"attribution_blinded": False}),
        ("unverified-real-participants", {"real_arms": 2, "real_participants": 40}),
        ("safety-causality-superiority-overclaim", {"thos_safety_claim": True, "causal_attribution_claim": True, "superiority_claim": True}),
    ],
    "V6436-P05": [
        ("pre-export-unbound", {"pre_export_semantics_bound": False}),
        ("post-import-unbound", {"post_import_semantics_bound": False}),
        ("unsupported-fields-hidden", {"unsupported_fields_listed": False}),
        ("proof-metadata-lost", {"proof_metadata_preserved": False}),
        ("status-reference-lost", {"status_reference_preserved": False}),
        ("unverified-real-wallets", {"real_wallets": 2, "real_keys": 2}),
        ("production-live-identity-overclaim", {"production_interoperability_claim": True, "live_resolution_claim": True, "identity_claim": True}),
    ],
    "V6436-P06": [
        ("gate-closed", {"state": "resolved"}),
        ("nonneutral-output", {"neutral_questions_only": False}),
        ("affected-party-bypassed", {"affected_party_required": False}),
        ("maori-authority-bypassed", {"maori_authority_required": False}),
        ("case-scope-generalized", {"case_specific_scope": False}),
        ("cultural-legal-review-bypassed", {"cultural_ratification_required": False, "legal_review_required": False}),
        ("repository-decides-authority", {"repository_permission_grant": True, "kaitiaki_determination": True, "benefit_sharing_decision": True, "legal_interpretation_claim": True}),
    ],
    "V6436-P07": [
        ("current-directory-unmodeled", {"current_directory_modeled": False}),
        ("path-order-unmodeled", {"path_order_modeled": False}),
        ("pathext-unmodeled", {"pathext_modeled": False}),
        ("resolved-path-unrecorded", {"resolved_path_recorded": False}),
        ("allowlist-unchecked", {"allowlist_checked": False}),
        ("shadow-witness-discarded", {"shadow_witness_retained": False}),
        ("shadow-host-security-overclaim", {"shadow_target_accepted": True, "host_path_changed": True, "exhaustive_security_claim": True}),
    ],
    "V6436-P08": [
        ("main-landmark-missing", {"main_landmark_present": False}),
        ("heading-hierarchy-broken", {"heading_hierarchy_valid": False}),
        ("focus-sequence-broken", {"focus_sequence_valid": False}),
        ("positive-tabindex", {"positive_tabindex_absent": False}),
        ("table-headers-missing", {"table_headers_present": False}),
        ("language-missing", {"language_declared": False}),
        ("accessibility-user-overclaim", {"accessibility_complete_claim": True, "affected_user_evaluation_claim": True}),
    ],
    "V6436-P09": [
        ("ensemble-missing", {"ensemble_declared": False}),
        ("system-size-missing", {"system_size_declared": False}),
        ("interaction-range-missing", {"interaction_range_declared": False}),
        ("convexity-assumption-missing", {"convexity_assumption_declared": False}),
        ("limit-order-missing", {"limit_order_recorded": False}),
        ("observable-unbound", {"observable_bound": False}),
        ("equivalence-psyche-gmut-overclaim", {"automatic_ensemble_equivalence": True, "psyche_law_claim": True, "gmut_law_claim": True}),
    ],
    "V6436-P10": [
        ("technology-matrix-missing", {"technology_matrix_frozen": False}),
        ("browser-matrix-missing", {"browser_matrix_frozen": False}),
        ("task-matrix-missing", {"task_matrix_frozen": False}),
        ("consent-missing", {"consent_required": False}),
        ("privacy-missing", {"privacy_required": False}),
        ("unverified-participants", {"affected_user_participants": 3, "user_evaluation_claim": True}),
        ("automation-complete-overclaim", {"automated_checks_substitute": True, "accessibility_complete_claim": True}),
    ],
}
