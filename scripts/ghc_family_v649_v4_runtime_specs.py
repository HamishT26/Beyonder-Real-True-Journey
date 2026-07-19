#!/usr/bin/env python3
"""Bounded runtime contracts for v649-v4."""

from __future__ import annotations

from typing import Any


CONTRACTS: dict[str, dict[str, Any]] = {
    "V6494-P01": {
        "outcome": "completed",
        "evidence_class": "bounded_synthetic_concurrency_tribunal",
        "paths": ["method-flow/future-completion-contract.json", "method-flow/future-completion-mutations.json"],
        "checks": ["single_assignment", "cancellation_race", "exception_propagation", "callback_order", "waiter_notification", "executor_shutdown", "duplicate_credit"],
        "absences": ["production_executor", "live_threads", "external_workload", "exhaustive_security", "independent_reproduction"],
    },
    "V6494-P02": {
        "outcome": "completed",
        "evidence_class": "typed_symbolic_obligation_board",
        "paths": ["gmut/operator-product-expansion-obligations.json", "gmut/operator-product-expansion-mutations.json"],
        "checks": ["short_distance_domain", "coefficient_distribution", "scaling_degree", "associativity", "microlocal_spectrum", "renormalization", "gauge_scope", "eft_truncation", "units", "observation_firewall"],
        "absences": ["real_data", "likelihood", "force", "prediction", "parameter_constraint", "quantum_completion", "theory_of_everything"],
    },
    "V6494-P03": {
        "outcome": "open_gap",
        "evidence_class": "official_toolkit_zero_solver_run_refusal",
        "paths": ["empirical/einstein-toolkit-study-contract.json", "empirical/einstein-toolkit-zero-solver-run-receipt.json"],
        "checks": ["thorn_interface", "evolved_variables", "gauge", "hyperbolicity", "initial_boundary_conditions", "discretization", "mesh_refinement", "constraint_propagation", "convergence_order", "environment_lock", "benchmark", "solver_run_refusal"],
        "absences": ["toolkit_checkout", "gmut_thorn", "parameter_file", "solver_runs", "constraint_traces", "refinement_triplets", "measured_convergence", "independent_review"],
    },
    "V6494-P04": {
        "outcome": "represented",
        "evidence_class": "synthetic_proxy_protocol",
        "paths": ["thos/seed-germination-assay-contract.json", "thos/seed-germination-assay-vectors.json"],
        "checks": ["sample_draw", "replicate_tray", "count_window", "dormancy_note", "censored_result", "viability_calculation", "retest_rule", "stock_depletion_budget", "result_amendment", "custody_handoff"],
        "absences": ["real_people", "real_seed_lots", "real_germination_assays", "real_biological_results", "real_distribution", "blind_matched_budget_arms", "effectiveness"],
    },
    "V6494-P05": {
        "outcome": "represented",
        "evidence_class": "synthetic_nonproduction_identity_profile",
        "paths": ["freed-id/registration-management-profile.json", "freed-id/registration-management-mutations.json"],
        "checks": ["configuration_endpoint", "registration_access_token", "read", "full_update", "delete", "metadata_replacement", "credential_rotation", "deprovisioning", "replay", "experimental_status", "minimization"],
        "absences": ["real_keys", "real_services", "accounts", "tokens", "interoperability", "privacy_review", "security_review", "trust_governance"],
    },
    "V6494-P06": {
        "outcome": "exact_gate",
        "evidence_class": "passport_dsi_authority_reservation_gate",
        "paths": ["cbr/seed-passport-dsi-risk-gate.json", "cbr/seed-passport-authority-reservation.json"],
        "checks": ["passport_metadata", "collection_site_geolocation", "land_relationship", "digital_sequence_linkage", "reidentification", "purpose", "disclosure", "retention", "material_transfer", "benefit_sharing", "affected_party", "maori_data_governance"],
        "absences": ["affected_party_acceptance", "legal_authority", "cultural_ratification", "maori_authority", "privacy_authority", "dsi_governance_authority", "benefit_sharing_authority", "biological_material_authority"],
    },
    "V6494-P07": {
        "outcome": "completed",
        "evidence_class": "bounded_synthetic_parser",
        "paths": ["formats/netcdf-classic-contract.json", "formats/netcdf-classic-mutations.json"],
        "checks": ["cdf_magic", "dimensions", "attributes", "variables", "padding", "offsets", "record_variables", "size_arithmetic", "external_data", "resource_budget"],
        "absences": ["user_files", "production_decoder", "external_retrieval", "exhaustive_security"],
    },
    "V6494-P08": {
        "outcome": "completed",
        "evidence_class": "structural_accessibility_audit",
        "paths": ["accessibility/error-summary-contract.json", "accessibility/error-summary-mutations.json"],
        "checks": ["heading", "live_status", "focus_target", "error_links", "field_association", "persistent_text", "non_colour_cue", "correction_confirmation", "zoom", "linear_fallback"],
        "absences": ["manual_keyboard_review", "browser_diversity", "assistive_technology_review", "maori_language_review", "affected_user_evaluation", "complete_accessibility"],
    },
    "V6494-P09": {
        "outcome": "completed",
        "evidence_class": "typed_formal_domain_guard",
        "paths": ["thermo-psyche/lippmann-electrocapillary-contract.json", "thermo-psyche/lippmann-electrocapillary-mutations.json"],
        "checks": ["interfacial_tension", "electrode_potential", "reference_electrode", "chemical_potential_constraint", "surface_excess", "sign", "units", "equilibrium_domain", "agency_nonconversion"],
        "absences": ["psyche_measure", "agency_measure", "moral_value", "consciousness", "personhood", "fundamental_law_of_mind"],
    },
    "V6494-P10": {
        "outcome": "completed",
        "evidence_class": "structural_stage20_nonpromotion",
        "paths": ["stage20/pattern-mixture-contract.json", "stage20/pattern-mixture-mutations.json"],
        "checks": ["pattern_mixture", "reference_based_imputation", "delta_adjustment", "missingness", "tipping_point", "estimand_alignment", "combination_rule", "multiplicity", "sensitivity", "nonpromotion"],
        "absences": ["real_participants", "causal_effect", "safety_monitoring", "value_authority", "independent_review", "stage20_authority"],
    },
}
