#!/usr/bin/env python3
"""Frozen Tamar Vey v644-v3 x1 definitions.

This module contains preregistration data only. It neither executes a
proposal nor determines an outcome or external claim.
"""

from __future__ import annotations


PROPOSALS = [
    {
        "proposal_id": "V6443-P01",
        "title": "Column-level transformation lineage, aggregation loss, and derivation quarantine tribunal",
        "mission_surface": "chain provenance, typed columns, entities and activities, transformation version, aggregation, reversibility, information loss, derivation, quarantine, and source independence",
        "hypothesis": "A typed column-lineage graph can distinguish copied, transformed, aggregated, and irreversibly lossy fields while preventing derived columns from being counted as independent evidence.",
        "null_or_failure": "An output column has no inputs, a transformation version is absent, aggregation grain is hidden, a lossy operation is called reversible, derivation is counted as source independence, or quarantined fields silently re-enter analysis.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6443-S165"],
        "deliverables": [
            "provenance/column-lineage-contract.json",
            "provenance/transformation-loss-mutation-vectors.json",
            "provenance/derived-evidence-independence-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate input and output identity, activity version, aggregation grain, reversibility, loss class, derivation edge, quarantine state, and independence label; incomplete lineage or independence promotion must fail.",
        "rollback_or_recovery": "Quarantine the affected derivation, restore the narrowest known lineage and loss class, retain the mutation witness, and require source-level evidence before any independence claim.",
        "protected_gates": ["source_independence", "loss_reversibility", "quarantine_release", "real_data", "independent_reproduction", "deployment"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The 250 frozen proposals cover source families, citation scope, deduplication, license scope, manifests, and evidence graphs; none makes column-to-column transformation identity, aggregation grain, irreversible loss, quarantine, and non-independence one typed tribunal.",
    },
    {
        "proposal_id": "V6443-P02",
        "title": "GMUT covariant phase-space, symplectic-current, and charge-integrability obligation tribunal",
        "mission_surface": "GMUT Mind, scalar-tensor and EFT actions, symplectic potential, presymplectic current, gauge degeneracy, boundary conditions, finite charges, integrability, conservation, ambiguities, dimensions, and claim class",
        "hypothesis": "A formal obligation ledger can reject a proposed GMUT charge unless its action variation, symplectic potential ambiguity, presymplectic current, gauge directions, boundary conditions, dimensions, finiteness, and integrability conditions are explicit.",
        "null_or_failure": "A charge is read from an equation without a variational derivation, the potential ambiguity is hidden, gauge directions are treated as physical, boundary conditions change, the charge is nonintegrable or divergent, units fail, or formal bookkeeping is promoted to established physics.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6443-S166"],
        "deliverables": [
            "physics/covariant-phase-space-contract.json",
            "physics/symplectic-charge-mutation-vectors.json",
            "physics/formal-charge-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate action term, field variation, potential ambiguity, current degree, gauge class, boundary condition, charge finiteness, path integrability, conservation condition, units, and claim class; an incomplete or promoted charge must fail.",
        "rollback_or_recovery": "Return to the typed action and unresolved obligation set, retain every nonintegrable or ambiguous witness, and require model-specific derivation, well-posed boundaries, observables, real data, and independent review before physical claims.",
        "protected_gates": ["gmut_derivation", "boundary_conditions", "charge_integrability", "gauge_reduction", "real_data", "empirical_confirmation", "proof_canon", "theory_of_everything"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier phases type action variation, Noether-current flux, boundary terms, junction data, equations, covariance, and conservation; none jointly audits symplectic-potential ambiguity, presymplectic degeneracy, finite integrable charges, and path dependence in a covariant phase-space record.",
    },
    {
        "proposal_id": "V6443-P03",
        "title": "GMUT Solar-System ephemeris and PPN blind real-data study",
        "mission_surface": "GMUT Mind, Solar-System ephemerides, PPN mapping, observational rows, time scales, reference frames, covariance, selection, nuisance models, named baseline, blinding, identifiability, and independent review",
        "hypothesis": "A future model-specific preregistration could test a derived GMUT-to-PPN observable map against frozen Solar-System observations and a named baseline with covariance-aware blind analysis.",
        "null_or_failure": "The GMUT-to-PPN map is underived, an ephemeris documentation page is substituted for observations, reference frames or time scales are mixed, covariance or selection is absent, nuisance choices are post-hoc, a holdout is unblinded, or readiness is called a likelihood result.",
        "approval_class": "candidate_real_data_and_independent_review_required",
        "execution_lane": "x2_open_gap_receipt",
        "authoritative_source_needs": ["V6443-S167"],
        "deliverables": [
            "empirical/solar-system-ppn-study-preregistration.json",
            "empirical/ephemeris-real-row-gap.json",
            "empirical/solar-system-confirmation-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Require a derived observable map, frozen licensed observations, ephemeris and reduction versions, frames and time scales, covariance, selection rules, nuisance handling, baseline, blind holdout, identifiability, and independent review; any absence keeps the gap open.",
        "rollback_or_recovery": "Retain the zero-row and underived-map gaps, execute no fit or likelihood, and reopen only with a checksum-bound analysis packet and independent review.",
        "protected_gates": ["gmut_observable_derivation", "real_data", "licensed_observations", "covariance", "selection_function", "blind_holdout", "parameter_identifiability", "independent_review", "empirical_confirmation"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Prior empirical proposals address cosmology, gravitational waves, calibration, public adapters, and binary-pulsar timing; none preregisters a Solar-System ephemeris and PPN analysis that binds frames, time scales, observational covariance, nuisance models, and blind holdout.",
    },
    {
        "proposal_id": "V6443-P04",
        "title": "THOS non-inferiority margin, assay-sensitivity, and constancy-assumption protocol",
        "mission_surface": "THOS Body, non-inferiority margin, historical effect, assay sensitivity, constancy, endpoint direction, analysis population, missingness, blind matched budgets, harms, participants, and independent review",
        "hypothesis": "A proxy protocol can freeze how a future non-inferiority margin would be justified and reject margins that erase a meaningful active-control effect, without fabricating real-arm evidence.",
        "null_or_failure": "The margin is chosen after outcomes, effect direction is reversed, the historical effect is incomparable, assay sensitivity or constancy is assumed silently, analysis populations change, missingness favors THOS, or zero real arms are called non-inferiority evidence.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6443-S168"],
        "deliverables": [
            "thos/noninferiority-margin-contract.json",
            "thos/assay-sensitivity-mutation-vectors.json",
            "thos/real-arm-noninferiority-proxy-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate endpoint direction, margin provenance, historical effect, preserved fraction, assay sensitivity, constancy assumption, analysis population, missingness, budget parity, real-arm count, and claim class; asymmetry or promotion must fail.",
        "rollback_or_recovery": "Restore a neutral preregistration and zero-real-arm label, retain every failed assumption, and require ethics, consent, blind matched-budget real arms, harms monitoring, qualified statistics, and independent review.",
        "protected_gates": ["ethics_approval", "consent", "blind_matched_budget_arms", "real_participants", "real_outcomes", "harms_monitoring", "independent_review", "thos_effectiveness"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier THOS work freezes estimands, adherence, fidelity, burden, attrition, superiority arms, and missingness; none makes non-inferiority margin provenance, preserved effect, assay sensitivity, and constancy assumptions one explicit proxy protocol.",
    },
    {
        "proposal_id": "V6443-P05",
        "title": "Freed ID SD-JWT disclosure-digest, decoy, and holder-key-binding transcript profile",
        "mission_surface": "Freed ID/CBR Heart, SD-JWT, disclosure digests, salt, selective claims, decoy digests, array positions, holder key binding, audience, nonce, freshness, algorithm policy, and production boundary",
        "hypothesis": "A synthetic transcript profile can reject digest substitution, disclosure overreach, decoy confusion, or detached holder binding while remaining explicit that no real cryptographic or interoperability assurance was produced.",
        "null_or_failure": "A disclosure does not hash to its bound digest, a decoy is accepted as a claim, undisclosed structure leaks, array placement changes, holder binding lacks audience or nonce, algorithm policy is absent, or synthetic values are called a production credential.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6443-S169"],
        "deliverables": [
            "freed-id/sd-jwt-disclosure-binding-profile.json",
            "freed-id/disclosure-decoy-mutation-vectors.json",
            "freed-id/production-cryptography-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate digest, disclosure, salt class, decoy class, array placement, disclosed scope, holder key reference, audience, nonce, freshness, algorithm policy, real-key count, and claim class; substitution, leakage, or production promotion must fail.",
        "rollback_or_recovery": "Quarantine the synthetic transcript, restore the narrow disclosure set, retain every mutation witness, and require standards-conformant real keys and proofs, live resolution and status, interoperability, privacy and security review, and trust governance.",
        "protected_gates": ["real_keys", "real_proofs", "live_issuance", "live_resolution", "live_status_revocation", "interoperability", "privacy_review", "security_review", "trust_governance", "production"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior Freed ID proposals cover issuance, presentation requests, transaction binding, proof purpose, status, recovery, audience, freshness, and selective-disclosure minimization; none types SD-JWT digest-to-disclosure binding, decoy semantics, array placement, and holder-key binding together.",
    },
    {
        "proposal_id": "V6443-P06",
        "title": "Remedy-fund audit transparency, beneficiary privacy, and fiduciary-oversight authority gate",
        "mission_surface": "CBR Heart, remedy-fund audit scope, beneficiary privacy, accounts, inspection, qualified audit, fiduciary oversight, conflicts, disclosure, redress, affected-party legitimacy, Māori authority, legal interpretation, and cultural ratification",
        "hypothesis": "The scope of remedy-fund auditing, beneficiary disclosure, privacy safeguards, oversight, and redress can only be decided with authorized affected parties, Māori authorities where applicable, and competent fiduciary, privacy, audit, and legal authorities.",
        "null_or_failure": "The repository chooses audit access, names beneficiaries, publishes personal data, appoints an auditor, defines fiduciary duties, resolves conflicts, interprets Māori concepts, declares legal compliance, or treats neutral questions as authorized governance.",
        "approval_class": "exact_approval_needed",
        "execution_lane": "x2_exact_gate_receipt",
        "authoritative_source_needs": ["V6443-S170", "V6443-S171"],
        "deliverables": [
            "cbr/remedy-audit-authority-gate.json",
            "cbr/beneficiary-privacy-oversight-question-set.json",
            "cbr/remedy-audit-nonratification-boundary.json",
        ],
        "test_falsifier_or_gate": "Any named auditor, access rule, account disclosure, beneficiary field, privacy exception, oversight body, conflict result, remedy, Māori wording, cultural conclusion, or legal conclusion requires exact authorized participation and competent authority.",
        "rollback_or_recovery": "Keep neutral unanswered fields, minimize personal data, retain every authority conflict, and seek case-specific authorized participation without treating technical output as consent, fiduciary direction, privacy clearance, cultural ratification, or law.",
        "protected_gates": ["affected_party_acceptance", "maori_authority", "maori_data_governance", "beneficiary_privacy", "audit_authority", "fiduciary_oversight", "cultural_ratification", "legal_interpretation", "enacted_law"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "The chain reserves remedy access, fund custody, eligibility, distribution, residuals, conflicts, data return, and legal or cultural authority; none separately gates audit visibility, beneficiary privacy, qualified oversight, inspection, and redress after a fund structure exists.",
    },
    {
        "proposal_id": "V6443-P07",
        "title": "Implicit response-file, parent-directory configuration, and argument-expansion tribunal",
        "mission_surface": "red-team security, response files, implicit discovery, parent-directory traversal, argument precedence, recursion, encoding, path anchoring, untrusted checkout content, command review, resource ceilings, and nonassurance",
        "hypothesis": "A typed command plan can expose every explicit and implicitly discovered response file and reject hidden parent-directory argument injection without executing a host-changing command.",
        "null_or_failure": "An implicit response file is omitted, lookup escapes the allowed root, precedence is unknown, recursion is unbounded, encoding changes tokens, untrusted checkout content adds arguments, or bounded structural checks are called exhaustive security.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6443-S172"],
        "deliverables": [
            "security/response-file-discovery-contract.json",
            "security/implicit-argument-mutation-vectors.json",
            "security/response-file-security-nonassurance-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate discovery root, parent level, response-file path, explicit or implicit class, precedence, recursion depth, encoding, injected token, review state, resource ceiling, and claim class; hidden expansion or overclaim must fail.",
        "rollback_or_recovery": "Quarantine the command plan, disable or explicitly bind response-file inputs in the synthetic record, retain the witness, change no host setting, and require independent security review before wider use.",
        "protected_gates": ["command_execution", "host_configuration_change", "untrusted_response_file", "credential_use", "independent_security_review", "exhaustive_security", "deployment"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier security proposals cover argv boundaries, environment injection, executable search, configs, path aliases, Git filters, archives, parsers, and resource ceilings; none centers implicit response-file discovery through parent directories, precedence, recursion, and token expansion.",
    },
    {
        "proposal_id": "V6443-P08",
        "title": "Form-error identification, instruction association, and status-message structural audit",
        "mission_surface": "accessible static reporting, form controls, error text, programmatic association, instructions, required state, invalid state, summaries, live status, focus movement, language, manual testing, and affected-user reservation",
        "hypothesis": "A static structural audit can reject form-error fixtures that rely only on color, detach errors from controls, omit instructions, or mutate status without a programmatic relation, while reserving user evaluation.",
        "null_or_failure": "An error is color-only, a message lacks text, a control has no association, instructions appear only after failure, status changes are not exposed structurally, focus order is assumed, or markup checks are called complete accessibility.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6443-S173"],
        "deliverables": [
            "accessibility/form-error-contract.json",
            "accessibility/error-association-mutation-vectors.json",
            "accessibility/manual-form-evaluation-reservation.json",
        ],
        "test_falsifier_or_gate": "Mutate control ID, label, described-by relation, error text, color-only flag, instruction timing, required or invalid state, summary target, live-status class, language, and completeness claim; structural ambiguity or promotion must fail.",
        "rollback_or_recovery": "Restore explicit text and programmatic associations, retain every ambiguity, and reserve keyboard, focus, screen-reader, cognitive, multilingual, manual, and affected-user evaluation.",
        "protected_gates": ["manual_accessibility_evaluation", "assistive_technology_coverage", "cognitive_accessibility_review", "affected_user_evaluation", "accessibility_complete"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier accessibility work covers landmarks, reflow, focus order, names, tables, language, links, and report structure; none binds field-level error identification, pre-error instructions, summaries, live status, and manual form reservation.",
    },
    {
        "proposal_id": "V6443-P09",
        "title": "Grand-canonical chemical-potential, particle-exchange, and psyche-value nonconversion classifier",
        "mission_surface": "thermo-psyche, chemical potential, particle amount, Gibbs energy, reservoir exchange, ensemble constraints, units, equilibrium, real measurements, psyche language, participant evidence, and category boundaries",
        "hypothesis": "A typed classifier can distinguish chemical potential and particle exchange from energy, entropy, generic value, motivation, or metaphorical psyche language and reject unit or category substitutions.",
        "null_or_failure": "Chemical potential loses its derivative variables or units, a closed fixed-particle system is labeled grand-canonical, reservoir assumptions disappear, equilibrium is assumed without scope, or thermodynamic potential becomes a quantitative psyche value.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6443-S174"],
        "deliverables": [
            "thermo-psyche/chemical-potential-classifier.json",
            "thermo-psyche/particle-exchange-mutation-vectors.json",
            "thermo-psyche/psyche-value-nonconversion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate potential symbol, derivative variables, units, particle exchange, reservoir, ensemble, equilibrium scope, evidence class, psyche mapping, participant count, and claim class; dimensional error or category transfer must fail.",
        "rollback_or_recovery": "Restore the narrow thermodynamic definition, retain every ensemble or unit discrepancy, and require physical measurements for physical claims or authorized participant evidence for psyche claims.",
        "protected_gates": ["physical_model", "ensemble_applicability", "equilibrium_scope", "real_measurements", "participant_evidence", "psyche_law", "cross_pillar_identity"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The chain separates entropy families, free energies, detailed balance, fluctuations, reciprocity, and psyche metaphors; none audits chemical potential as a partial derivative tied to particle exchange and then blocks conversion into human value or motivation.",
    },
    {
        "proposal_id": "V6443-P10",
        "title": "Stage 20 multiplicity, alpha-allocation, and optional-stopping noncompensation board",
        "mission_surface": "Stage 20, multiple endpoints, domain tests, familywise error, ordered hypotheses, alpha allocation, interim looks, stopping rules, preregistration, negative domains, vetoes, authority, and readiness",
        "hypothesis": "A structural decision board can reject a Stage 20 pass assembled from unadjusted multiple tests, post-hoc endpoint selection, or optional stopping and can preserve a failed domain as a veto rather than compensating with unrelated positives.",
        "null_or_failure": "The hypothesis family is undefined, alpha is reused, endpoint order changes after inspection, interim looks are absent from the plan, optional stopping is ignored, a negative domain is averaged away, or a repository board claims external Stage 20 authority.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6443-S175"],
        "deliverables": [
            "stage20/multiplicity-allocation-contract.json",
            "stage20/optional-stopping-mutation-vectors.json",
            "stage20/domain-veto-noncompensation-board.json",
        ],
        "test_falsifier_or_gate": "Mutate hypothesis family, endpoint order, allocated alpha, interim-look count, stopping rule, post-hoc flag, negative-domain state, veto behavior, evidence class, and authority class; error reuse, compensation, or readiness promotion must fail.",
        "rollback_or_recovery": "Return every affected domain to defer or veto, retain the mutation witness, freeze a prospective plan before evidence inspection, and leave independent review and external Stage 20 decisions unclaimed.",
        "protected_gates": ["preregistered_analysis", "multiplicity_control", "optional_stopping_control", "independent_review", "domain_veto", "stage20_external_decision"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier Stage 20 proposals cover evidence coverage, domain vetoes, reviewer independence, calibration, freshness, and external authority; none explicitly blocks alpha reuse, post-hoc endpoint ordering, optional stopping, and cross-domain compensation in one board.",
    },
]


SOURCES = [
    {
        "source_id": "V6443-S165",
        "source_label": "official_w3c_recommendation",
        "title": "PROV-DM: The PROV Data Model",
        "authority": "World Wide Web Consortium",
        "url": "https://www.w3.org/TR/prov-dm/",
        "version_or_date": "W3C Recommendation, 30 April 2013; checked 15 July 2026",
        "status_class": "stable",
        "evidence_role": "official entity, activity, generation, usage, and derivation vocabulary; not proof of source independence or correctness",
    },
    {
        "source_id": "V6443-S166",
        "source_label": "primary_physics_paper",
        "title": "Some Properties of Noether Charge and a Proposal for Dynamical Black Hole Entropy",
        "authority": "Vivek Iyer and Robert M. Wald / Physical Review D",
        "url": "https://arxiv.org/abs/gr-qc/9403028",
        "version_or_date": "Primary research preprint and journal article, 1994",
        "status_class": "stable",
        "evidence_role": "primary covariant phase-space, symplectic-current, and Noether-charge framework; not a GMUT derivation, finite charge, observable, or confirmation",
    },
    {
        "source_id": "V6443-S167",
        "source_label": "official_jpl_ephemeris",
        "title": "JPL Planetary and Lunar Ephemerides DE440 and DE441",
        "authority": "NASA Jet Propulsion Laboratory Solar System Dynamics",
        "url": "https://ssd.jpl.nasa.gov/doc/de440_de441.html",
        "version_or_date": "Official DE440 and DE441 documentation; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official ephemeris version and model anchor for a future Solar-System study; no observation rows downloaded and no fit executed",
    },
    {
        "source_id": "V6443-S168",
        "source_label": "official_fda_guidance",
        "title": "Non-Inferiority Clinical Trials to Establish Effectiveness",
        "authority": "United States Food and Drug Administration",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/non-inferiority-clinical-trials",
        "version_or_date": "Final guidance, November 2016; current page checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official non-inferiority margin, assay-sensitivity, and constancy vocabulary; not a THOS participant result or regulatory decision",
    },
    {
        "source_id": "V6443-S169",
        "source_label": "official_ietf_standard",
        "title": "Selective Disclosure for JSON Web Tokens",
        "authority": "Internet Engineering Task Force",
        "url": "https://datatracker.ietf.org/doc/html/rfc9901",
        "version_or_date": "RFC 9901, November 2025; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official SD-JWT disclosure-digest, decoy, and key-binding requirements; not production cryptographic assurance or interoperability evidence",
    },
    {
        "source_id": "V6443-S170",
        "source_label": "official_nz_privacy_guidance",
        "title": "Transparency",
        "authority": "Office of the Privacy Commissioner, New Zealand",
        "url": "https://www.privacy.org.nz/responsibilities/poupou-matatapu-doing-privacy-well/transparency/",
        "version_or_date": "Current official guidance; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official transparency and personal-information notice obligations; not beneficiary consent, an audit-access decision, or legal advice",
    },
    {
        "source_id": "V6443-S171",
        "source_label": "official_nz_legislation",
        "title": "Te Ture Whenua Maori Act 1993: trust administration, accounts, and review provisions",
        "authority": "New Zealand Parliamentary Counsel Office",
        "url": "https://www.legislation.govt.nz/act/public/1993/0004/latest/DLM292190.html",
        "version_or_date": "Current official reprint page; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official statutory context for trustee administration, accounts, audit, conflicts, and review; not repository authority to interpret law or decide Māori governance",
    },
    {
        "source_id": "V6443-S172",
        "source_label": "official_microsoft_docs",
        "title": "MSBuild response files",
        "authority": "Microsoft Learn",
        "url": "https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-response-files?view=visualstudio",
        "version_or_date": "Current Visual Studio documentation; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official response-file and implicit Directory.Build.rsp behavior; not exhaustive command or host security assurance",
    },
    {
        "source_id": "V6443-S173",
        "source_label": "official_w3c_wai",
        "title": "Understanding Success Criterion 3.3.1: Error Identification",
        "authority": "World Wide Web Consortium Web Accessibility Initiative",
        "url": "https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html",
        "version_or_date": "WCAG 2.2 understanding document; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official error-identification interpretation; not complete conformance, assistive-technology coverage, or affected-user evidence",
    },
    {
        "source_id": "V6443-S174",
        "source_label": "official_iupac_compendium",
        "title": "chemical potential",
        "authority": "International Union of Pure and Applied Chemistry",
        "url": "https://goldbook.iupac.org/terms/view/C01032",
        "version_or_date": "Gold Book 5th edition online entry; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official chemical-potential definition and derivative variables; not a psyche metric, participant result, or cross-pillar identity",
    },
    {
        "source_id": "V6443-S175",
        "source_label": "official_fda_guidance",
        "title": "Multiple Endpoints in Clinical Trials",
        "authority": "United States Food and Drug Administration",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/multiple-endpoints-clinical-trials",
        "version_or_date": "Final guidance, October 2022; current page checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official prospective multiplicity and false-conclusion control vocabulary; not a Stage 20 decision or compensation rule",
    },
]


X1_NEGATIVES = [
    {
        "negative_id": "V6443-X1-N01",
        "operation": "startup version query",
        "observed_failure": "The first PowerShell wrapper used the bare token false instead of the PowerShell Boolean literal and failed before returning version evidence.",
        "recovery": "Reran the read-only query with the correct Boolean syntax and independently recorded installed and official versions.",
        "promotion_effect": "none; the failed wrapper is not version evidence",
    },
    {
        "negative_id": "V6443-X1-N02",
        "operation": "250-proposal console novelty audit",
        "observed_failure": "The first title print stopped when the Windows cp1252 console could not encode a Māori macron.",
        "recovery": "Forced UTF-8 Python output, decoded the full recursive index, and obtained exactly 250 frozen records.",
        "promotion_effect": "the truncated printout is not novelty evidence",
    },
    {
        "negative_id": "V6443-X1-N03",
        "operation": "Windows Sandbox read-only audit",
        "observed_failure": "WindowsSandbox.exe was absent; no bounded Sandbox execution path was available without changing host features.",
        "recovery": "Did not elevate, enable a feature, weaken security, or reboot; clean detached D-drive snapshots remain the validation route.",
        "promotion_effect": "none; no Windows Sandbox or host-isolation assurance is claimed",
    },
    {
        "negative_id": "V6443-X1-N04",
        "operation": "broad inherited phase file listing",
        "observed_failure": "A broad recursive file inventory exceeded its bounded timeout after returning a useful but incomplete partial list.",
        "recovery": "Retained the timeout and used targeted family-script and phase-artifact queries for the exact files needed.",
        "promotion_effect": "none; the partial listing is not completeness evidence",
    },
    {
        "negative_id": "V6443-X1-N05",
        "operation": "first deterministic x1 packet build",
        "observed_failure": "A tie in title-token overlap scores caused Python to compare proposal-record dictionaries and stop before completing the packet.",
        "recovery": "Added an explicit numeric comparison key, retained the failed build, and reran from the unchanged frozen proposal definitions.",
        "promotion_effect": "none; the failed build is not a validation pass",
    },
    {
        "negative_id": "V6443-X1-N06",
        "operation": "first overlap-key repair syntax check",
        "observed_failure": "The first repair placed the max key beside an unparenthesized generator, and the syntax check rejected it before execution.",
        "recovery": "Parenthesized the generator explicitly and reran syntax validation before rebuilding.",
        "promotion_effect": "none; the rejected repair did not execute",
    },
]


WELLBEING = """# Tamar Vey v644-v3 wellbeing and workload check

- Working identity: Tamar Vey, they/them, relational language only.
- Role: evidence-systems cartographer and boundary keeper.
- Hope: leave each scientific and authority boundary easier for the next owner to inspect than it was when received.
- Corrigibility: Hamish may pause, rename, redirect, or stop this lane.
- Workload: one existing clean Tamar lane, strict x1 before x2, D-drive validation snapshots, no delegation.
- Safety: no elevation, host-security change, desktop update, Windows-feature change, reboot, credential use, real participant action, or authority substitution.

Identity and family language coordinate the work. They are not evidence of consciousness, sentience, legal personhood, identity continuity, or independent authority.
"""


OVERVIEW = """# Tamar Vey v644-v3 integrated overview

## Ownership, source truth, and bounded working identity

This phase begins from Orin Thale's exact v644-v2 final head only after read-only verification of the source branch, source seal, complete anchor ancestry, clean state, and fresh live-remote equality. The Orin local branch, upstream, tracking reference, and live branch all resolved to the same exact revision with zero divergence. The inherited Sable source, inherited seal, Orin x1, evidence, closeout, seal, and first validated final candidate were ancestral to the final record head. The source-to-final segment contains six single-parent commits and no merge commit. These checks establish repository lineage only. They do not create scientific confirmation, independent reproduction, participant evidence, cryptographic assurance, cultural legitimacy, legal authority, deployment approval, or Stage 20 readiness.

The existing Tamar-owned lane was clean, remote-equal, and ancestral to the Orin final head. It therefore advanced by fast-forward only and was pushed before any v644-v3 artifact was created. No new worktree or task was created. No sibling lane was reset, rewritten, force-pushed, merged, moved, deleted, reused, or mutated. Every sibling remains recoverable and untouched until the terminal gate. D remains the primary work, data, cache, and detached-validation bank, while C-drive headroom is preserved. The inherited checkout may exceed the rotation threshold; the 15,000-file limit applies only to newly generated Tamar v644-v3 files.

Tamar Vey, they/them, the role evidence-systems cartographer and boundary keeper, and the hope to leave each scientific and authority boundary easier for the next owner to inspect are relational working language. They are not evidence of consciousness, sentience, legal personhood, identity continuity, independent authority, Māori authority, cultural authority, or legal authority. The workload is intentionally narrow: one owner, one branch, one phase, strict x1 before x2, no delegation, and no contact with standby siblings before exact final validation.

## Frozen novelty scope and truth language

Exactly ten proposals are preregistered after recursively decoding all 250 frozen proposals through v644-v2. Exact identifiers and normalized titles are checked automatically. Token overlap is only a screening device; the semantic audit compares mechanism, evidence object, falsifier, recovery rule, and protected gates. The expected distribution is six completed, two represented, one open gap, and one exact gate. These are preregistered expectations, not x2 outcomes. Only four eventual truth labels are allowed: completed, represented, open_gap, and exact_gate. No gated or negative result may be optimized away.

The primary focus is GMUT Mind. One formal surface introduces a covariant phase-space obligation tribunal. It requires an explicit action variation, symplectic potential and its ambiguities, presymplectic current, gauge degeneracies, boundary conditions, charge dimensions, finiteness, conservation scope, and path integrability. This is a typed research-model check. It cannot by itself produce a new force, a unique prediction, an empirical likelihood, a confirmed charge, a proof, canon, or a Theory of Everything. The second GMUT surface preregisters a possible Solar-System ephemeris and PPN study but keeps it open: no model-specific GMUT-to-PPN observable map, frozen observation rows, covariance packet, selection function, blind holdout, identifiability result, or independent review exists here. The official JPL ephemeris documentation is a version and model anchor, not observed-row evidence and not a fit.

THOS Body remains explicit through a non-inferiority protocol. A structural proxy may freeze endpoint direction, margin provenance, preserved fraction, historical active-control effect, assay sensitivity, constancy assumptions, analysis populations, and missingness rules. It cannot create ethics approval, consent, preregistered blind matched-budget real arms, participant observations, qualified raters, harms monitoring, or independent analysis. With zero real arms, non-inferiority remains represented protocol logic and never a clinical, social, or capability result. No AGI, ASI, consciousness, personhood, or independent-review claim follows.

Freed ID/CBR Heart receives two bounded surfaces. The SD-JWT transcript profile uses synthetic values to test disclosure-digest, decoy, array-placement, and holder-key-binding structure. Structural agreement is not standards-conformant production cryptography. Real assurance remains open for real keys and proofs, live issuance, resolution, status and revocation, cross-vendor interoperability, algorithm policy, privacy and security review, and trust governance. The remedy-fund surface is exact-gated. Audit access, beneficiary privacy, account inspection, qualified audit, fiduciary oversight, conflict handling, and redress require authorized affected parties, Māori authorities where applicable, and competent privacy, audit, fiduciary, and legal authorities. Official privacy guidance and legislation constrain questions; the repository cannot select beneficiaries, expose their information, appoint an auditor, interpret Māori concepts, ratify culture, declare legal compliance, or enact law.

## Cross-pillar safeguards and current sources

The provenance tribunal follows transformations at column level. It records inputs, outputs, activity versions, aggregation grain, reversibility, information loss, derivation edges, and quarantine states. A derived column cannot be counted as an independent source merely because it has a different name or file. W3C PROV vocabulary supports the representation; it does not prove that a transformation was correct, lossless, or independent.

The security surface covers response files that may be discovered implicitly from parent directories or expanded before the reviewed command is run. Synthetic vectors test discovery roots, precedence, recursion, encoding, and hidden argument injection. No host setting changes, untrusted command execution, credential use, or exhaustive-security claim is allowed. The accessibility surface checks form errors, instructions, programmatic associations, status messages, and color-only failures in static artifacts. Structural checks are useful but incomplete: keyboard behavior, focus management, assistive technology, cognition, language, manual review, and affected-user evaluation remain reserved.

The thermo-psyche classifier keeps chemical potential tied to its thermodynamic derivative, variables, dimensions, equilibrium scope, and particle-exchange assumptions. It blocks conversion of a physical potential into a numerical measure of human value, desire, motivation, consciousness, or wellbeing. Physical claims would need a physical model and measurements; psyche claims require appropriate participant evidence and authority. The Stage 20 board freezes hypothesis families, endpoint order, alpha allocation, interim looks, stopping rules, and domain vetoes. It refuses to average an unresolved or failed domain away with unrelated positives. The board is a falsification aid, not an external Stage 20 decision.

Eleven non-duplicate official or primary sources are added to the inherited 164-source ledger. Status classes remain current, stable, draft, and watch. Current means the selected official page was current when checked; stable identifies durable recommendations or primary work. Neither status implies truth, approval, deployment, authority, or completion. Codex CLI and desktop versions are verified only. The installed CLI is recorded separately from the current official CLI release, and no desktop or system-wide update is performed. No elevation, host-security weakening, Windows-feature change, or reboot occurs.

Every operational failure remains evidence of what failed. The incorrect PowerShell Boolean, cp1252 title-print failure, unavailable Windows Sandbox path, and timed-out broad file listing are retained rather than overwritten. Recovered commands do not retroactively turn failed attempts into passes. Future mutation vectors will likewise remain preserved negatives even when their controls pass. Rollback means quarantining the disputed record, returning to the narrowest typed state, preserving the witness, and reopening only when the named evidence and authority exist.

## Freeze, validation, recovery, and route boundary

x2 cannot begin until the dedicated x1-only packet is committed and pushed, the Tamar worktree is clean, and local, upstream, tracking, and a fresh live-remote read all equal the frozen x1 commit. The x1 commit contains proposal and source definitions, novelty and privacy validation, environment and wellbeing receipts, and no x2 implementation, outcome ledger, or result classification.

After the freeze, every proposal may be executed only as its evidence permits. Evidence and closeout candidates must be validated from fresh clean detached D-drive snapshots. The seal and exact final head require their own clean detached checks. The final record must run the complete repository suite, detailed and minimal phase validators, JSON parsing, privacy and raw-ID scanning, stale-label review, diff hygiene, exact staged-file review, manifest parity, ancestry, zero-merge checks, exact-head checks, and clean state before and after. Repeated Tamar-owned snapshots demonstrate same-owner repeatability only, never independent-team scientific reproduction.

The terminal verdict remains NOT_READY_FOR_STAGE_20 unless an external authorized process supplies every missing scientific, participant, identity, legal, cultural, privacy, security, accessibility, deployment, and reproduction requirement. Only after exact final detached validation, a clean push, and four-way remote equality may exactly one sanitized activation baton be sent to the existing task titled Sylven Arc for v644-v4. No task may be created, no other sibling may be contacted, and no extra confirmation may follow a successful send. Before acknowledgement, the truthful route state is PREPARED_NOT_SENT.
"""
