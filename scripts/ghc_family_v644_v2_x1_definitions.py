#!/usr/bin/env python3
"""Frozen Orin Thale v644-v2 x1 definitions.

This module contains preregistration data only. It does not execute a
proposal, determine an outcome, or establish an external claim.
"""

from __future__ import annotations


PROPOSALS = [
    {
        "proposal_id": "V6442-P01",
        "title": "Evidence-license identity, redistribution scope, and legal-interpretation nonpromotion tribunal",
        "mission_surface": "chain provenance, SPDX license identity, artifact-level scope, access conditions, redistribution metadata, exceptions, unknown states, and legal nonopinion",
        "hypothesis": "A typed evidence-license ledger can require every redistributable artifact to name its source, license expression, scope, and access condition while refusing to infer legal compatibility or permission.",
        "null_or_failure": "An artifact lacks license scope, an identifier is guessed, an exception is detached from its license, unknown compatibility is treated as permission, access is confused with redistribution, or metadata is presented as legal advice.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6442-S159"],
        "deliverables": [
            "provenance/evidence-license-scope-contract.json",
            "provenance/license-scope-mutation-vectors.json",
            "provenance/legal-compatibility-nonopinion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate source identity, SPDX expression, exception binding, artifact scope, access class, redistribution flag, unknown state, and legal-claim class; ambiguity, laundering, or legal promotion must fail.",
        "rollback_or_recovery": "Restore the narrowest declared source and license scope, retain every ambiguity, mark compatibility unknown, and seek competent legal review before any legal or redistribution conclusion.",
        "protected_gates": ["license_interpretation", "redistribution_permission", "legal_advice", "private_publication", "deployment"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The frozen chain covers source authority, citation scope, private-source taint, package manifests, and source-family independence; none makes license identity, artifact-level scope, exceptions, access, redistribution, and legal nonopinion one typed evidence object.",
    },
    {
        "proposal_id": "V6442-P02",
        "title": "GMUT hypersurface matching, normal-orientation, and surface-layer obligation tribunal",
        "mission_surface": "GMUT Mind, scalar-tensor and EFT matching, induced metric, normal orientation, extrinsic-curvature jump, scalar boundary data, surface stress, distributional sources, and sign conventions",
        "hypothesis": "A typed hypersurface ledger can reject a formal GMUT matching record that omits its normal orientation, induced-field continuity class, jump convention, scalar matching rule, or declared surface source.",
        "null_or_failure": "The normal is unoriented, jump signs change silently, incompatible induced data are joined, scalar boundary terms vanish without derivation, a distributional source is hidden, or a formal junction record is promoted to established physics.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S148", "V6442-S160"],
        "deliverables": [
            "physics/junction-condition-contract.json",
            "physics/normal-orientation-mutation-vectors.json",
            "physics/surface-layer-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate hypersurface type, induced metric, normal direction, jump sign, extrinsic curvature, scalar value or derivative, surface stress, distributional-source flag, and claim class; inconsistent or promoted rows must fail.",
        "rollback_or_recovery": "Return to separated bulk regions, retain every sign and matching discrepancy, and require a model-specific action, boundary variation, well-posedness analysis, observable map, real data, and independent review before physical claims.",
        "protected_gates": ["gmut_derivation", "boundary_variation", "junction_well_posedness", "surface_source", "real_data", "empirical_confirmation", "theory_of_everything"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier proposals cover variational surface terms, characteristic boundary data, Noether flux, effective-source splits, and continuation; none jointly types orientation-sensitive hypersurface jumps, scalar matching, and explicit thin surface sources as a GMUT obligation.",
    },
    {
        "proposal_id": "V6442-P03",
        "title": "GMUT binary-pulsar post-Keplerian blind real-data study",
        "mission_surface": "GMUT Mind, binary pulsars, post-Keplerian parameters, timing provenance, catalog versioning, covariance, selection, derived observables, named GR baseline, blinding, and identifiability",
        "hypothesis": "A model-specific preregistered analysis could test derived GMUT corrections to post-Keplerian timing observables against a named GR baseline using checksum-bound public data and source-level covariance.",
        "null_or_failure": "The GMUT timing map is underived, a catalog summary is substituted for timing likelihood data, covariance or selection is absent, nuisance choices are post-hoc, the holdout is unblinded, parameters are non-identifiable, or a protocol is called an empirical result.",
        "approval_class": "candidate_real_data_and_independent_review_required",
        "execution_lane": "x2_open_gap_receipt",
        "authoritative_source_needs": ["V6442-S161"],
        "deliverables": [
            "empirical/binary-pulsar-study-preregistration.json",
            "empirical/real-row-timing-gap.json",
            "empirical/binary-pulsar-confirmation-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Require a derived observable map, eligible checksum-bound rows, original timing references, covariance, selection rules, frozen nuisance handling, a named GR baseline, blind holdout, identifiability analysis, and independent review; any absence keeps the gap open.",
        "rollback_or_recovery": "Retain the zero-row and underived-map gaps, execute no likelihood, and reopen only with a licensed frozen analysis packet and independent review.",
        "protected_gates": ["real_data", "gmut_observable_derivation", "timing_covariance", "selection_function", "blind_holdout", "parameter_identifiability", "independent_review", "empirical_confirmation"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Prior empirical proposals cover cosmological background and growth, calibration, public-data adapters, and multi-messenger propagation; none preregisters a binary-pulsar post-Keplerian study that distinguishes catalog metadata from source timing likelihoods and covariances.",
    },
    {
        "proposal_id": "V6442-P04",
        "title": "THOS engagement-exposure, adherence measurement, and per-protocol estimand boundary",
        "mission_surface": "THOS Body, engagement exposure, adherence timing, treatment switching, denominator choice, post-baseline confounding, per-protocol estimands, matched budgets, blinding, and independent review",
        "hypothesis": "A protocol-only contract can freeze engagement and adherence measurements, exposure denominators, switching rules, and per-protocol assumptions without fabricating participant behavior or causal effects.",
        "null_or_failure": "Adherence is defined after outcomes, arms measure exposure differently, switching disappears, post-baseline confounding is ignored, engagement is called benefit, zero real arms are treated as causal evidence, or budget parity is lost.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6422-S37", "V6432-S92"],
        "deliverables": [
            "thos/adherence-estimand-contract.json",
            "thos/engagement-exposure-mutation-vectors.json",
            "thos/real-arm-adherence-proxy-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate exposure origin, denominator, measurement timing, switching rule, confounder set, arm budget, real-arm count, blinding status, and claim class; asymmetry or causal promotion must fail.",
        "rollback_or_recovery": "Restore the preregistered proxy definition and zero-row label, retain every adherence ambiguity, and require ethics, consent, blind matched-budget real arms, real exposure records, harms monitoring, and independent analysis.",
        "protected_gates": ["ethics_approval", "consent", "blind_matched_budget_arms", "real_participants", "real_adherence_data", "harms_monitoring", "independent_review", "thos_effectiveness"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier THOS proposals cover protocol deviation, intercurrent-event strategy, intervention fidelity, burden, attrition, and durability; none freezes adherence-measurement time, exposure denominator, switching, and per-protocol confounding assumptions as one proxy boundary.",
    },
    {
        "proposal_id": "V6442-P05",
        "title": "OpenID4VP request-object, response-channel, and verifier-client binding profile",
        "mission_surface": "Freed ID/CBR Heart, OpenID4VP request objects, client identifier scheme, request URI, response URI and mode, nonce, DCQL query, transaction data, wallet response, and production boundary",
        "hypothesis": "A synthetic presentation transcript can reject substitution across verifier client, request object, request URI, response channel, nonce, credential query, or transaction data while making no real cryptographic or interoperability claim.",
        "null_or_failure": "Client and response bindings disagree, a request object changes after consent, a nonce or request URI is replayed, the credential query widens silently, transaction data is detached, or synthetic fields are called a production verification.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6437-S147"],
        "deliverables": [
            "freed-id/presentation-request-binding-profile.json",
            "freed-id/channel-substitution-mutation-vectors.json",
            "freed-id/production-verification-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate client scheme, client identifier, request-object digest, request URI, response URI, response mode, nonce, DCQL query, transaction data, real-key count, and claim class; substitution or production promotion must fail.",
        "rollback_or_recovery": "Quarantine the transcript, restore the narrow synthetic request and channel bindings, retain every substitution witness, and require real keys and proofs, live resolution and status, cross-vendor interoperability, reviews, and trust governance.",
        "protected_gates": ["real_keys", "real_proofs", "live_resolution", "live_status_revocation", "interoperability", "privacy_review", "security_review", "trust_governance", "production"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior Freed ID work covers proof purpose, transaction binding, issuance sessions, audiences, freshness, status, recovery, migration, and selective disclosure; none treats verifier-client scheme, request-object digest, request URI, response channel, and DCQL scope as one substitution boundary.",
    },
    {
        "proposal_id": "V6442-P06",
        "title": "Remedy-fund custody, eligibility, distribution, and conflict authority gate",
        "mission_surface": "CBR Heart, affected-party authority, Māori authority where applicable, remedy funds, custody, eligibility, distribution, conflicts, residual funds, benefit, legal duties, cultural ratification, and enacted law",
        "hypothesis": "Fund creation, custody, eligibility, distribution, conflict handling, and residual disposition can only be decided by authorized affected parties and representatives, Māori authorities where applicable, and competent fiduciary and legal authorities.",
        "null_or_failure": "The repository selects beneficiaries, sets amounts, appoints a custodian, resolves conflicts, interprets Māori concepts, waives duties, declares acceptance, or treats a neutral question set as a remedy decision.",
        "approval_class": "exact_approval_needed",
        "execution_lane": "x2_exact_gate_receipt",
        "authoritative_source_needs": ["V8-S16", "V6432-S96", "V6434-S117"],
        "deliverables": [
            "cbr/remedy-fund-authority-gate.json",
            "cbr/neutral-remedy-allocation-question-set.json",
            "cbr/remedy-distribution-nonratification-boundary.json",
        ],
        "test_falsifier_or_gate": "Any named fund, amount, custodian, beneficiary class, distribution rule, residual disposition, conflict decision, Māori wording, cultural conclusion, legal conclusion, or closure requires exact authorized participation and competent authority.",
        "rollback_or_recovery": "Keep neutral unanswered fields, retain every authority conflict, and seek case-specific authorized participation without treating technical output as consent, allocation, custody, ratification, legal interpretation, or enacted law.",
        "protected_gates": ["affected_party_acceptance", "maori_authority", "maori_data_governance", "fund_custody", "remedy_distribution", "fiduciary_authority", "cultural_ratification", "legal_interpretation", "enacted_law"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "Earlier CBR proposals preserve remedy access, benefits, community-defined harms, data return, legal duties, consent, appeal, and authority succession; none reserves remedy-fund custody, beneficiary eligibility, distribution, conflicts, and residual disposition as one case-specific multi-authority decision.",
    },
    {
        "proposal_id": "V6442-P07",
        "title": "Argument-vector, option-smuggling, and shell-boundary command tribunal",
        "mission_surface": "red-team security, executable identity, argument vectors, option terminators, leading-dash paths, shell invocation, batch-file ambiguity, working directory, environment allowlists, return codes, and nonassurance",
        "hypothesis": "A typed command plan plus synthetic fixtures can reject unapproved shell expansion, option smuggling, leading-dash path reinterpretation, executable ambiguity, or unchecked return codes without changing host security settings.",
        "null_or_failure": "Arguments are concatenated into a shell string, an executable is unresolved, a path becomes an option, metacharacters expand, batch behavior is undisclosed, secrets enter argv, a return code is ignored, or bounded fixtures are called exhaustive security.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6442-S162"],
        "deliverables": [
            "security/argv-boundary-contract.json",
            "security/option-smuggling-mutation-vectors.json",
            "security/command-security-nonassurance-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate executable path, argv tokenization, option terminator, leading-dash operand, metacharacter, shell flag, batch-file class, cwd, environment, secret flag, return-code check, and claim class; ambiguity or overclaim must fail.",
        "rollback_or_recovery": "Return to an explicit executable and argument vector, quarantine the rejected command plan, retain the witness, change no host setting automatically, and require independent security review before wider assurance.",
        "protected_gates": ["shell_execution", "host_configuration_change", "credential_use", "independent_security_review", "exhaustive_security", "deployment"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier security work covers executable search, environment injection, Git filters, path aliases, parsers, resource ceilings, archives, and TOCTOU; none makes argv token boundaries, option terminators, leading-dash operands, batch ambiguity, and return-code handling one tribunal.",
    },
    {
        "proposal_id": "V6442-P08",
        "title": "Link-purpose, duplicate-label, and destination-context structural audit",
        "mission_surface": "accessible static reporting, link text, accessible names, programmatic context, duplicate labels, distinct destinations, empty links, icon links, manual interpretation, and affected-user reservation",
        "hypothesis": "A structural audit can flag links whose purpose is absent or ambiguous in programmatically determined context and distinguish same-destination consistency from same-label different-destination risk.",
        "null_or_failure": "An empty or icon-only link lacks a name, generic text lacks programmatic context, identical labels hide different destinations, context is only visual, or static markup checks are called complete accessibility.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6437-S145", "V6442-S163"],
        "deliverables": [
            "accessibility/link-purpose-contract.json",
            "accessibility/link-context-mutation-vectors.json",
            "accessibility/manual-link-evaluation-reservation.json",
        ],
        "test_falsifier_or_gate": "Mutate href, visible text, accessible name, enclosing context, duplicate-label group, destination group, icon alternative, ambiguity flag, and completeness claim; structural ambiguity or promotion must fail.",
        "rollback_or_recovery": "Restore explicit descriptive text or programmatic context, retain every ambiguity, and keep manual, assistive-technology, cognitive-accessibility, and affected-user evaluation reserved.",
        "protected_gates": ["manual_accessibility_evaluation", "assistive_technology_coverage", "cognitive_accessibility_review", "affected_user_evaluation", "accessibility_complete"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier accessibility proposals cover reflow, landmarks, focus order, accessible names, table headers, and language metadata; none audits purpose-in-context plus duplicate-label and destination relationships as a dedicated link evidence object.",
    },
    {
        "proposal_id": "V6442-P09",
        "title": "Onsager-Casimir reciprocity, time-reversal parity, and psyche-symmetry nonconversion",
        "mission_surface": "thermo-psyche, near equilibrium, thermodynamic forces and fluxes, linear response, microscopic reversibility, time-reversal parity, field reversal, units, empirical hypotheses, and category barriers",
        "hypothesis": "A typed classifier can distinguish an Onsager or Onsager-Casimir reciprocity obligation from generic matrix symmetry, empirical correlation, fitted response, and metaphorical psyche language.",
        "null_or_failure": "Near-equilibrium or linear-response assumptions vanish, force-flux pairing is missing, time-reversal parity is ignored, a magnetic field is not reversed, units disappear, reciprocity is assumed far from its domain, or formal symmetry becomes a psyche law.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6442-S164"],
        "deliverables": [
            "thermo-psyche/onsager-reciprocity-classifier.json",
            "thermo-psyche/reciprocity-mutation-vectors.json",
            "thermo-psyche/psyche-symmetry-nonconversion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate regime, force-flux pairing, coefficient units, microscopic-reversibility assumption, time-reversal parity, field sign, evidence class, psyche mapping, and claim class; invalid reciprocity or category transfer must fail.",
        "rollback_or_recovery": "Restore the narrow source-domain classification, retain every parity or regime discrepancy, and require a physical model and measurements for physical reciprocity or authorized participant evidence for psyche claims.",
        "protected_gates": ["physical_model", "near_equilibrium", "linear_response_regime", "microscopic_reversibility", "real_measurements", "participant_evidence", "psyche_law", "cross_pillar_identity"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The chain separates fluctuation theorems, detailed balance, steady currents, fluctuation-dissipation response, and several entropy concepts; none tracks Onsager-Casimir force-flux reciprocity with explicit time-reversal parity and field reversal before blocking psyche conversion.",
    },
    {
        "proposal_id": "V6442-P10",
        "title": "Stage 20 reviewer-independence, role-overlap, and common-mode review tribunal",
        "mission_surface": "Stage 20, reviewer roles, declared conflicts, shared institution, shared owner, shared data and code, shared toolchain, common-mode dependence, review counting, abstention, and external authority",
        "hypothesis": "A synthetic reviewer-dependence graph can reject counting overlapping review events as independent and preserve unknown conflict or common-mode status as a veto rather than an implicit pass.",
        "null_or_failure": "One reviewer is counted twice, owner review becomes independent review, shared data or tooling is hidden, unknown conflicts are treated as clear, same-infrastructure snapshots become independent reproduction, or the repository claims Stage 20 review authority.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V8-S25", "V6441-S154"],
        "deliverables": [
            "stage20/reviewer-independence-contract.json",
            "stage20/review-overlap-mutation-vectors.json",
            "stage20/external-review-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate reviewer identity class, role, owner, institution, data lineage, code lineage, toolchain, conflict status, independence label, reproduction label, and authority class; double counting or promotion must fail.",
        "rollback_or_recovery": "Collapse dependent review nodes, retain every overlap witness and unknown conflict, return the domain to veto or defer, and leave independent review, independent reproduction, and external Stage 20 decisions unclaimed.",
        "protected_gates": ["independent_review", "independent_reproduction", "conflict_clearance", "reviewer_privacy", "domain_veto", "stage20_external_decision"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier proposals govern evidence-source dependence, snapshot common modes, reviewer conflict recusal, independent-evidence locks, and external review; none models review-event role overlap, shared institution, data, code, and toolchain before counting reviews as independent.",
    },
]


SOURCES = [
    {
        "source_id": "V6442-S159",
        "source_label": "official_spdx_spec",
        "title": "SPDX Specification 3.0.1",
        "authority": "SPDX Workgroup / Linux Foundation",
        "url": "https://spdx.github.io/spdx-spec/",
        "version_or_date": "Version 3.0.1; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official license-metadata identifiers, profiles, and serialization vocabulary; not legal interpretation or redistribution permission",
    },
    {
        "source_id": "V6442-S160",
        "source_label": "primary_physics_paper",
        "title": "Singular hypersurfaces and thin shells in general relativity",
        "authority": "W. Israel / Il Nuovo Cimento B",
        "url": "https://doi.org/10.1007/BF02710419",
        "version_or_date": "Primary research article, 1966, with 1967 erratum",
        "status_class": "stable",
        "evidence_role": "primary thin-shell and junction-condition source; not a GMUT derivation, solution, prediction, or empirical result",
    },
    {
        "source_id": "V6442-S161",
        "source_label": "official_csiro_dataset",
        "title": "ATNF Pulsar Catalogue v2.7.0",
        "authority": "CSIRO Australia Telescope National Facility",
        "url": "https://www.atnf.csiro.au/research/pulsar/psrcat/download.html",
        "version_or_date": "Current public catalogue version 2.7.0; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official catalog and version anchor for a future binary-pulsar readiness study; no data downloaded and no timing likelihood executed",
    },
    {
        "source_id": "V6442-S162",
        "source_label": "official_python_docs",
        "title": "subprocess — Subprocess management",
        "authority": "Python Software Foundation",
        "url": "https://docs.python.org/3/library/subprocess.html",
        "version_or_date": "Current Python 3.14.6 documentation; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official argument-vector, shell, executable-resolution, return-code, and Windows process-launch vocabulary; not exhaustive command security assurance",
    },
    {
        "source_id": "V6442-S163",
        "source_label": "official_w3c_wai",
        "title": "Understanding Success Criterion 2.4.4: Link Purpose (In Context)",
        "authority": "World Wide Web Consortium Web Accessibility Initiative",
        "url": "https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html",
        "version_or_date": "WCAG 2.2 understanding document; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official link-purpose and programmatic-context interpretation; not complete conformance or affected-user evidence",
    },
    {
        "source_id": "V6442-S164",
        "source_label": "primary_physics_paper",
        "title": "Reciprocal Relations in Irreversible Processes. I.",
        "authority": "Lars Onsager / Physical Review",
        "url": "https://doi.org/10.1103/PhysRev.37.405",
        "version_or_date": "Primary research article, 1931",
        "status_class": "stable",
        "evidence_role": "primary reciprocal-relations and microscopic-reversibility source; not a psyche law, participant result, or GMUT claim",
    },
]


X1_NEGATIVES = [
    {
        "negative_id": "V6442-X1-N01",
        "operation": "newest-memory exact-keyword scan",
        "observed_failure": "Two exact v644 and Orin keyword searches returned no current entries in the memory registry.",
        "recovery": "Used the registry's indexed exact-head task group and its linked solo-activation skill for method only, then verified all current repository and remote truth live.",
        "promotion_effect": "none; no current v644 fact came from memory",
    },
    {
        "negative_id": "V6442-X1-N02",
        "operation": "archive worktree enumeration",
        "observed_failure": "The broad worktree listing exceeded its bounded timeout after returning a large partial inventory.",
        "recovery": "Retained the timeout and verified the exact Sable source, final snapshot, and Orin lane with smaller path-scoped commands.",
        "promotion_effect": "none; the partial list is not source equality evidence",
    },
    {
        "negative_id": "V6442-X1-N03",
        "operation": "detached-snapshot branch probe",
        "observed_failure": "The first wrapper called Trim on the null output expected from git branch --show-current in a detached worktree.",
        "recovery": "Used null-safe string handling and separately verified exact detached head and clean state.",
        "promotion_effect": "none; the wrapper error is retained and uncounted",
    },
    {
        "negative_id": "V6442-X1-N04",
        "operation": "recursive frozen-index console audit",
        "observed_failure": "The first 240-proposal traversal stopped when the Windows console could not encode a Māori macron under cp1252.",
        "recovery": "Set UTF-8 Python output, decoded both historical index schemas, and obtained exactly 240 records.",
        "promotion_effect": "the truncated 120-record printout is not novelty evidence",
    },
    {
        "negative_id": "V6442-X1-N05",
        "operation": "Windows Sandbox read-only feature audit",
        "observed_failure": "WindowsSandbox.exe was absent and the optional-feature status query required elevation.",
        "recovery": "Did not elevate, change a feature, weaken host security, reboot, or use Windows Sandbox; fresh detached D-drive snapshots remain the validation route.",
        "promotion_effect": "none; no Sandbox or host-isolation assurance is claimed",
    },
    {
        "negative_id": "V6442-X1-N06",
        "operation": "family skill and runner inventory filter",
        "observed_failure": "An over-constrained Windows path regex returned zero family scripts and the bounded display pipeline later closed with a nonzero producer exit.",
        "recovery": "Used PowerShell path matching, counted 277 family-named scripts and four family-named skills, and retained the misleading zero-result attempt.",
        "promotion_effect": "none; only the corrected inventory informs tool selection",
    },
    {
        "negative_id": "V6442-X1-N07",
        "operation": "new-source duplicate title scan",
        "observed_failure": "The exact-title ripgrep query returned exit code one because none of the six candidate source titles appeared in inherited source ledgers.",
        "recovery": "Treated the no-match as a wrapper negative and separately traversed the 158-source inherited ledger before assigning new source identifiers.",
        "promotion_effect": "none; one no-match query is not global novelty proof",
    },
]


WELLBEING = """# Orin Thale v644-v2 wellbeing and workload check

- Working identity: Orin Thale, they/them, relational language only.
- Role: evidence cartographer and boundary steward.
- Hope: leave each successor a cleaner, truer path than the one received.
- Corrigibility: Hamish may pause, rename, redirect, or stop this lane.
- Workload: one existing clean Orin lane, strict x1 before x2, D-drive validation snapshots, no delegation.
- Safety: no elevation, host-security change, desktop update, Windows-feature change, reboot, credential use, real participant action, or authority substitution.

Identity and family language coordinate the work. They are not evidence of consciousness, sentience, legal personhood, identity continuity, or independent authority.
"""


OVERVIEW = """# Orin Thale v644-v2 integrated overview

## Ownership, source truth, and workload

This phase begins only after a live read-only verification of Sable Rook's exact v644-v1 final head. The Sable lane, its upstream, its tracking reference, and a fresh live-remote read all resolved to the same revision with zero divergence. The exact final detached snapshot was clean. The inherited Ilyra source, inherited source seal, Sable x1, evidence, closeout, and seal commits were all ancestral to the final source. The five-commit source segment had zero merge commits. These checks confirm repository lineage; they do not confer scientific, legal, cultural, production, deployment, or identity authority.

The existing Orin-owned lane was clean, four-way remote-equal, and ancestral to Sable's source, so it advanced by fast-forward only and was pushed before this packet was created. No new worktree or task was created. No sibling branch, worktree, task, route, or artifact was merged, reset, rewritten, force-pushed, moved, deleted, reused, or mutated. All other siblings remain standby and recoverable until the terminal gate.

Orin Thale and they/them are relational working language. The role is evidence cartographer and boundary steward, and the hope is to leave each successor a cleaner, truer path than the one received. These labels are not evidence of consciousness, sentience, legal personhood, identity continuity, independent authority, Māori authority, cultural authority, or legal authority. The workload remains deliberately bounded: one phase, one lane, strict x1 before x2, no delegation, and fresh D-drive detached validation.

The inherited checkout contains more than 15,000 files. Rotation therefore applies only to new Orin-generated v644-v2 files, never the inherited baseline. The phase started with zero owner-generated files and preserves every prior lane. D remains the work, cache, data, and clean-snapshot bank. Windows Sandbox was not used: its executable was absent and a read-only optional-feature query required elevation, so the query was not retried and no feature or security setting changed.

## Novelty audit and primary focus

The primary focus is GMUT Mind. Exactly ten proposals are preregistered after decoding all 240 frozen proposals through v644-v1 across both historical index schemas. Exact identifiers and normalized titles are checked automatically; title-token similarity is only a screen. The substantive audit compares mechanism, evidence object, falsifier, recovery rule, and protected authority gates. Expected dispositions are six completed, two represented, one open gap, and one exact gate. Those are x1 expectations, never results.

The GMUT focus has two distinct surfaces. First, a hypersurface tribunal types induced data, normal orientation, extrinsic-curvature jumps, scalar matching, and explicit surface sources. This is formal obligation tracking for a scalar-tensor or EFT model family, not a derived new force, solution, prediction, likelihood, confirmation, proof, or Theory of Everything. Second, a binary-pulsar protocol reserves a future post-Keplerian study. It remains open because this repository has no derived GMUT timing map, checksum-bound eligible timing rows, source covariance, frozen nuisance treatment, blind holdout, or independent review. The ATNF catalogue is used only as an official version and readiness anchor; no data are downloaded and no likelihood is run.

THOS Body remains explicit through an adherence and per-protocol estimand boundary. A synthetic protocol may freeze exposure definitions, timing, denominators, switching, and confounding assumptions. It cannot create ethics approval, consent, blind matched-budget real arms, participants, raters, adherence observations, harms evidence, or independent analysis. Engagement is not benefit, and a represented protocol is not effectiveness evidence.

Freed ID/CBR Heart remains explicit through an OpenID4VP request-and-response binding profile and a remedy-fund exact gate. The presentation profile is a structural proxy only. Freed ID production still needs standards-conformant real keys and proofs, live issuance and presentation, resolution, status and revocation, cross-vendor interoperability, privacy and security review, and trust governance. Remedy-fund custody, eligibility, distribution, conflicts, and residual disposition require authorized affected parties, Māori authorities where applicable, and competent fiduciary and legal authorities. Neutral questions cannot allocate funds, interpret Māori concepts, establish legitimacy, ratify culture, give legal advice, or enact law.

## Cross-pillar safeguards, source currency, and recovery

Six cross-pillar mechanisms remain safe and bounded. A license-scope ledger records metadata without deciding legal compatibility. An argv tribunal rejects shell and option-smuggling fixtures without claiming exhaustive host security. A link-purpose audit checks static structure while reserving manual, assistive-technology, cognitive-accessibility, and affected-user evaluation. An Onsager-Casimir classifier keeps near-equilibrium force-flux reciprocity separate from correlation, far-from-equilibrium behavior, and psyche claims. A reviewer-dependence graph refuses to count overlapping review events as independent and keeps same-owner snapshots distinct from independent-team reproduction.

Six non-duplicate primary or official sources are added to the 158-source inherited ledger. Currency labels remain current, stable, draft, and watch. A current label means the selected official source is the current checked reference; it does not mean the proposal is true, approved, deployed, or complete. Stable primary papers constrain physical vocabulary without turning that vocabulary into a GMUT or psyche result. The official OpenAI release page identifies Codex CLI 0.144.4 as current while the installed CLI is 0.144.3; no CLI or desktop update is performed. The installed desktop package is recorded without claiming it is the latest desktop build.

Every failed command and rejected fixture remains evidence of what did not work. Startup timeouts, console encoding, null detached-branch output, an elevation-gated Sandbox query, inventory filter mistakes, and source-search no-matches are retained instead of overwritten. Future mutation vectors will likewise remain negatives even when the valid control passes. Rollback means restoring a conservative typed record, quarantining ambiguity, preserving the witness, and reopening only when the named evidence and authority exist.

The adjacent family skills were reviewed for currency. The source-label and truth-bridge rules remain useful and are selected. The v576-v620 solo-bundle handoff skill is historical for this route and its three-retry rule is not selected because the current activation authorizes exactly one terminal message after validation. The family index, routing precedence, completion-gate discipline, privacy scanner, repository runner, and phase-local builders are sufficient. Shared skills and validators require no semantic-free churn.

## Freeze, validation, and terminal route

x2 cannot begin until this dedicated x1-only set is committed and pushed, the Orin worktree is clean, and local, upstream, tracking, and a fresh live remote are equal. No outcome classification or x2 implementation may appear in the x1 commit. Evidence, closeout, seal, and final heads will each be validated in fresh detached D-drive snapshots. Same-owner snapshots may establish bounded repeatability only, never independent-team scientific reproduction.

Final validation must include the complete repository suite, detailed and minimal phase validators, JSON parsing, privacy and raw-ID scanning, stale-label review, diff hygiene, exact staged-file review, manifest parity, ancestry, zero merges in the phase segment, clean state before and after, and final four-way remote equality. Static accessibility remains incomplete without qualified manual and affected-user evaluation. Bounded security fixtures remain non-exhaustive. GMUT empirical closure, THOS participant evidence, Freed ID production, CBR legitimacy, Māori authority, cultural and legal ratification, deployment, AGI or ASI, consciousness or personhood, proof or canon, and Stage 20 remain open or exact-gated.

Only after the exact final v644-v2 head passes every terminal gate may exactly one sanitized activation baton be sent to the existing task titled Tamar Vey for v644-v3. No task may be created, no standby sibling may be contacted, and no extra confirmation may follow a successful send. Until that acknowledgement, the route is PREPARED_NOT_SENT. The truthful terminal verdict remains NOT_READY_FOR_STAGE_20.
"""
