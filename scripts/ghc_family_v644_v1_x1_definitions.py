#!/usr/bin/env python3
"""Frozen Sable Rook v644-v1 x1 definitions.

This module contains preregistration data only. It does not execute a
proposal, determine an outcome, or establish an external claim.
"""

from __future__ import annotations


PROPOSALS = [
    {
        "proposal_id": "V6441-P01",
        "title": "Authorship, dataset, and method-lineage collapse for apparent source independence",
        "mission_surface": "chain provenance, semantic deduplication, scholarly versions, contributor roles, shared datasets, shared code, shared methods, and independence debt",
        "hypothesis": "A typed source-family graph can collapse publications that share data, code, protocol, or controlling contributors before any source-count or independence claim is made.",
        "null_or_failure": "A version is double counted, contributor or dataset overlap is hidden, shared code is treated as an independent method, a relation is inferred without provenance, or a synthetic graph is called independent corroboration.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6-S02", "V6441-S154"],
        "deliverables": ["provenance/source-family-independence-contract.json", "provenance/shared-lineage-mutation-vectors.json", "provenance/independent-corroboration-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Mutate work identity, version relation, contributor role, dataset DOI, code digest, protocol identifier, authority root, and independence label; an uncollapsed dependency or unsupported independence claim must fail.",
        "rollback_or_recovery": "Return to the conservative source family, retain every overlap witness, and require explicit primary provenance before separating a family into independent roots.",
        "protected_gates": ["source_independence", "semantic_deduplication", "external_corroboration", "independent_review", "independent_reproduction"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier proposals deduplicate citations and evidence roots, knock out authority roots, and budget common-mode dependence; none jointly canonicalizes scholarly versions, contributor roles, dataset identifiers, code digests, and protocol lineage before counting apparent publications as independent sources.",
    },
    {
        "proposal_id": "V6441-P02",
        "title": "GMUT effective-source split, improvement ambiguity, and sector-exchange balance tribunal",
        "mission_surface": "GMUT Mind, canonical equation typing, SI units, tensor rank, covariance, Standard Model and scalar or EFT source split, improvement terms, exchange currents, conservation, stability, and identifiability boundaries",
        "hypothesis": "A typed canonical-source ledger can reject a GMUT record whose total effective source is dimensionally or covariantly inconsistent, whose sector exchange does not sum to zero, or whose improvement freedom is hidden while keeping stability and identifiability unestablished.",
        "null_or_failure": "Tensor type or units mismatch, a source sector is double counted, total exchange is nonzero, an improvement term silently changes the split, stability or parameter identifiability is assumed, or formal bookkeeping is promoted to physics.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6423-S46", "V6438-S148", "V6438-S149"],
        "deliverables": ["physics/effective-source-split-contract.json", "physics/sector-exchange-mutation-vectors.json", "physics/stability-identifiability-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Mutate canonical equation identity, tensor variance, SI dimension, sector membership, exchange-current sign, improvement declaration, conservation sum, stability status, identifiability status, and claim class; inconsistent or promoted rows must fail.",
        "rollback_or_recovery": "Restore the canonical typed total-source equation, retain every failed decomposition, and require model-specific derivation, stability analysis, observable mapping, real data, and independent review before physical claims.",
        "protected_gates": ["gmut_derivation", "covariant_conservation", "stability", "structural_identifiability", "practical_identifiability", "real_data", "empirical_confirmation", "theory_of_everything"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The frozen chain covers units, Bianchi exchange, field frames, Noether balance, stability, and identifiability separately; none treats the canonical GMUT right-hand-side decomposition itself as an improvement-sensitive conservation object while forcing stability and identifiability to remain separate unresolved obligations.",
    },
    {
        "proposal_id": "V6441-P03",
        "title": "GMUT gravitational-wave propagation and electromagnetic-counterpart blind real-data study",
        "mission_surface": "GMUT Mind, real public gravitational-wave data, electromagnetic counterparts, propagation speed and damping, calibration, selection, waveform and nuisance provenance, blind baseline comparison, and identifiability",
        "hypothesis": "A model-specific, preregistered multi-messenger analysis could test a derived GMUT propagation map against named GR baselines using public data without reusing the repository's synthetic fixtures as observations.",
        "null_or_failure": "The propagation observable is underived, no eligible counterpart rows exist, calibration or selection effects are omitted, waveform and nuisance choices are post-hoc, the holdout is not blind, parameters are non-identifiable, or a protocol is called a likelihood result.",
        "approval_class": "candidate_real_data_and_independent_review_required",
        "execution_lane": "x2_open_gap_receipt",
        "authoritative_source_needs": ["V6441-S155"],
        "deliverables": ["empirical/multimessenger-study-preregistration.json", "empirical/real-row-propagation-gap.json", "empirical/multimessenger-confirmation-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Require a derived observable map, licensed and checksum-bound public rows, calibration and selection functions, frozen waveform and nuisance treatment, named external baselines, blind holdout, identifiability analysis, and independent review; any absence keeps the gap open.",
        "rollback_or_recovery": "Retain the zero-row and underived-map gaps, execute no likelihood, and reopen only with an authorized frozen analysis and independent review.",
        "protected_gates": ["real_data", "gmut_observable_derivation", "calibration", "selection_function", "blind_holdout", "parameter_identifiability", "independent_review", "empirical_confirmation"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Earlier empirical proposals cover background, growth, calibration, public-data integrity, and generic adapters; none preregisters a multi-messenger propagation analysis that jointly binds gravitational-wave data, electromagnetic timing, waveform systematics, selection, and a blind GR baseline.",
    },
    {
        "proposal_id": "V6441-P04",
        "title": "THOS follow-up-window, decay, and durable-effect estimand preregistration",
        "mission_surface": "THOS Body, matched-budget arms, common time origin, visit windows, repeated outcomes, decay, durability, intercurrent events, attrition, blinding, and independent review",
        "hypothesis": "A protocol-only estimand can freeze a common time origin, allowed follow-up windows, decay model, durability threshold, and intercurrent-event strategy without fabricating participant returns.",
        "null_or_failure": "Arms use different clocks, visit windows shift after outcomes, durability is inferred from a single time point, attrition disappears, intercurrent events change strategy silently, or zero real arms are called durable benefit.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6432-S92"],
        "deliverables": ["thos/durability-estimand-contract.json", "thos/followup-window-mutation-vectors.json", "thos/real-arm-durability-proxy-boundary.json"],
        "test_falsifier_or_gate": "Mutate time origin, allowed window, repeated-measure schedule, decay form, durability threshold, intercurrent-event strategy, attrition visibility, real-arm count, and claim class; temporal asymmetry or promotion must fail.",
        "rollback_or_recovery": "Restore the common clock and zero-row proxy label, retain every temporal discrepancy, and require ethics, consent, blind matched-budget real arms, harms monitoring, real follow-up, and independent analysis.",
        "protected_gates": ["ethics_approval", "consent", "blind_matched_budget_arms", "real_participants", "real_followup", "harms_monitoring", "independent_review", "thos_effectiveness"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior THOS proposals govern allocation, attrition, carryover, measurement drift, intercurrent events, site time, and facilitator learning; none makes a common post-allocation clock, permissible visit windows, decay model, and durable-effect threshold one frozen matched-budget estimand.",
    },
    {
        "proposal_id": "V6441-P05",
        "title": "Freed ID issuance-session, authorization-code, and wallet-instance binding profile",
        "mission_surface": "Freed ID/CBR Heart, OpenID4VCI issuance, credential offers, issuer metadata, authorization details, authorization code, PKCE, nonce, wallet instance, deferred delivery, replay, and production boundary",
        "hypothesis": "A structural issuance transcript can reject cross-session substitution of an offer, issuer, authorization code, PKCE verifier, nonce, wallet instance, or deferred transaction while making no real cryptographic or interoperability claim.",
        "null_or_failure": "Issuer metadata and offer disagree, an authorization code or nonce is replayed, PKCE or wallet binding is absent, deferred delivery crosses sessions, a credential configuration changes silently, or synthetic fields are called a production issuance.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6436-S135"],
        "deliverables": ["freed-id/issuance-session-binding-profile.json", "freed-id/session-substitution-mutation-vectors.json", "freed-id/production-issuance-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Mutate issuer identifier, credential configuration, offer reference, authorization details, code, PKCE challenge, nonce, wallet instance, deferred transaction, real-key count, and claim class; substitution or promotion must fail.",
        "rollback_or_recovery": "Quarantine the transcript, restore explicit synthetic session bindings, retain every substitution witness, and require real keys and proofs, live endpoints, resolution and status, cross-vendor interoperability, reviews, and trust governance.",
        "protected_gates": ["real_keys", "real_proofs", "live_issuer", "live_resolution", "live_status_revocation", "interoperability", "privacy_review", "security_review", "trust_governance"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior Freed ID work covers credential proof purpose, holder binding, audiences, freshness, rotation, status, recovery, migration, and wallet sync; none models the OpenID4VCI authorization-code, PKCE, nonce, wallet-instance, and deferred-delivery chain as one issuance-session substitution boundary.",
    },
    {
        "proposal_id": "V6441-P06",
        "title": "Data return, repatriation, and stewardship-transfer authority gate",
        "mission_surface": "CBR Heart, affected-party authority, Māori authority and data governance where applicable, data return or repatriation, stewardship transfer, custody, copies, deletion, access, benefit, legal limits, and cultural ratification",
        "hypothesis": "Whether data should be returned, repatriated, copied, deleted, retained, or transferred can only be determined by authorized affected parties, Māori authorities where applicable, current custodians, and competent legal authorities.",
        "null_or_failure": "The repository identifies the rightful steward, orders return or deletion, interprets Māori concepts, resolves competing mandates, waives legal duties, declares acceptance, or treats a principles document as case-specific authorization.",
        "approval_class": "exact_approval_needed",
        "execution_lane": "x2_exact_gate_receipt",
        "authoritative_source_needs": ["V6432-S96"],
        "deliverables": ["cbr/data-return-authority-gate.json", "cbr/neutral-stewardship-transfer-question-set.json", "cbr/repatriation-nonratification-boundary.json"],
        "test_falsifier_or_gate": "Any named community, asset, steward, return decision, deletion decision, access condition, benefit allocation, Māori wording, tikanga interpretation, cultural conclusion, legal conclusion, or closure requires exact authorized participation and competent authority.",
        "rollback_or_recovery": "Keep neutral unanswered fields, retain every authority conflict, and seek case-specific authorized participation without treating technical output as consent, governance, return, repatriation, ratification, or enacted law.",
        "protected_gates": ["affected_party_acceptance", "maori_authority", "maori_data_governance", "data_return_decision", "stewardship_transfer", "cultural_ratification", "legal_interpretation", "enacted_law"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "Earlier CBR proposals gate collection, secondary use, benefit, preservation, remedy, consent, appeal, and authority succession; none reserves the direction of custody itself—return, repatriation, deletion, retained copies, and stewardship transfer—as one case-specific multi-authority decision.",
    },
    {
        "proposal_id": "V6441-P07",
        "title": "Git clean-filter, smudge-filter, hook, and external-diff execution quarantine",
        "mission_surface": "red-team security, repository attributes, local Git configuration, clean and smudge filters, process filters, hooks, external diff and textconv, checkout materialization, recovery, and nonassurance",
        "hypothesis": "A read-only repository trust audit plus synthetic fixtures can reject validation paths that would execute unapproved filters, hooks, external diffs, or text conversion while leaving the host and Git configuration unchanged.",
        "null_or_failure": "An executable filter or hook is silently trusted, local config provenance is missing, a diff invokes an external program, checkout bytes are treated as canonical without filter disclosure, or the bounded audit is called exhaustive security.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6441-S156"],
        "deliverables": ["security/git-execution-surface-contract.json", "security/filter-hook-mutation-vectors.json", "security/host-security-nonassurance-boundary.json"],
        "test_falsifier_or_gate": "Mutate attribute source, filter driver, required flag, hook path, external diff, textconv, config scope, checkout hash class, and claim class; undisclosed execution or overclaim must fail.",
        "rollback_or_recovery": "Use plumbing or disabled-execution inspection, preserve the rejected configuration witness, restore no host setting automatically, and require independent security review before wider assurance.",
        "protected_gates": ["host_configuration_change", "hook_execution", "filter_execution", "independent_security_review", "exhaustive_security", "deployment"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier security work covers path shadowing, environment injection, supply-chain manifests, reparse points, parsers, archives, and TOCTOU; none makes Git attributes plus local filter, hook, external-diff, and textconv execution a dedicated clean-snapshot trust boundary.",
    },
    {
        "proposal_id": "V6441-P08",
        "title": "Document-language, language-of-parts, and directionality structural audit",
        "mission_surface": "accessible static reporting, default language, language changes, BCP 47 tags, directionality, inherited language, pronunciation support, exceptions, manual evaluation, and affected-user reservation",
        "hypothesis": "A structural audit can require a valid page language, explicit language changes where needed, and locally appropriate direction metadata while reserving pronunciation and comprehension evaluation.",
        "null_or_failure": "The page language is absent or invalid, a passage changes language without metadata, direction is inferred from appearance, a proper-name exception is overgeneralized, or static markup is called complete accessibility.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6432-S98", "V6441-S157"],
        "deliverables": ["accessibility/language-metadata-contract.json", "accessibility/language-direction-mutation-vectors.json", "accessibility/manual-pronunciation-evaluation-reservation.json"],
        "test_falsifier_or_gate": "Mutate page language, part language, tag validity, inheritance, direction, exception class, pronunciation claim, and completeness claim; ambiguous or promoted rows must fail.",
        "rollback_or_recovery": "Restore the narrowest explicit valid language and direction metadata, retain every ambiguity, and keep manual, assistive-technology, fluent-speaker, and affected-user evaluation reserved.",
        "protected_gates": ["manual_accessibility_evaluation", "assistive_technology_coverage", "fluent_speaker_review", "affected_user_evaluation", "accessibility_complete"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier accessibility proposals cover reflow, color, landmarks, focus, names, and table associations, while security work covers bidirectional spoofing; none audits human-language metadata, language inheritance, pronunciation support, and directionality as an accessibility evidence object.",
    },
    {
        "proposal_id": "V6441-P09",
        "title": "Fluctuation-dissipation response and psyche-correlation non-substitution barrier",
        "mission_surface": "thermo-psyche, equilibrium ensemble, conjugate perturbation, causal response, time correlation, susceptibility, units, linear regime, operational rule, empirical hypothesis, and category barrier",
        "hypothesis": "A typed classifier can distinguish an equilibrium fluctuation-dissipation relation from an observed correlation, a fitted response heuristic, and metaphorical psyche language.",
        "null_or_failure": "Equilibrium or linear-response assumptions disappear, perturbation and observable are not conjugate, causality is ignored, units or transform convention vanish, correlation is called response, or a formal relation becomes a psyche law.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6441-S158"],
        "deliverables": ["thermo-psyche/fluctuation-response-classifier.json", "thermo-psyche/response-correlation-mutation-vectors.json", "thermo-psyche/psyche-correlation-nonconversion-boundary.json"],
        "test_falsifier_or_gate": "Mutate ensemble, perturbation pairing, causality, transform convention, units, response regime, evidence class, psyche mapping, and claim class; category transfer must fail.",
        "rollback_or_recovery": "Restore the narrow source-domain classification, retain every category-confusion witness, and require a physical model and measurements for physical response or authorized participant evidence for psyche claims.",
        "protected_gates": ["physical_model", "equilibrium_assumption", "linear_response_regime", "real_measurements", "participant_evidence", "psyche_law", "cross_pillar_identity"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The chain separates entropy, free energy, ensembles, detailed balance, negative temperature, coarse graining, and causal direction; none distinguishes causal susceptibility from equilibrium correlations and then blocks either from becoming a psyche law.",
    },
    {
        "proposal_id": "V6441-P10",
        "title": "Stage 20 adjudication history, evidence-withdrawal, and decision-reversal replay",
        "mission_surface": "Stage 20, terminal evidence board, pass fail and defer decisions, adjudication history, evidence addition and withdrawal, retained dissent, negative retention, gate monotonicity, reversal reason, and external authority",
        "hypothesis": "A synthetic replay can require every domain decision to reverse or defer when a necessary evidence item is withdrawn, preserve dissent and negative history, and forbid cross-domain compensation.",
        "null_or_failure": "A veto disappears without its requirement being met, withdrawn evidence leaves a pass unchanged, dissent or a negative is erased, one domain compensates for another, a defer becomes approval, or the repository claims external Stage 20 authority.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["inherited phase-truth, retained-negative, and exact/open-gate records"],
        "deliverables": ["stage20/adjudication-replay-contract.json", "stage20/evidence-withdrawal-mutation-vectors.json", "stage20/external-decision-authority-boundary.json"],
        "test_falsifier_or_gate": "Mutate evidence presence, evidence expiry, domain decision, dissent retention, negative retention, compensation flag, reversal reason, and authority class; an unjustified pass or erased history must fail.",
        "rollback_or_recovery": "Restore the last hash-bound decision record, retain the withdrawal and dissent witnesses, return the affected domain to veto or defer, and leave the external Stage 20 decision exact-gated.",
        "protected_gates": ["stage20_external_decision", "domain_veto", "evidence_validity", "negative_retention", "dissent_retention", "independent_review"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier Stage 20 work covers contradiction, expiry, cut sets, monotonic withdrawal, asymmetric loss, minimax regret, escrow, and non-compensation; none replays a versioned adjudication history in both directions and requires an explicit reversal reason while retaining dissent and the withdrawn evidence as negative history.",
    },
]


SOURCES = [
    {"source_id": "V6441-S154", "title": "ANSI/NISO Z39.104-2022 CRediT Contributor Roles Taxonomy", "authority": "National Information Standards Organization", "url": "https://www.niso.org/standards-committees/credit", "version_or_date": "ANSI/NISO Z39.104-2022; checked 15 July 2026", "status_class": "stable", "evidence_role": "official contributor-role vocabulary for declared research lineage; roles do not by themselves prove source independence"},
    {"source_id": "V6441-S155", "title": "GWTC-4.0 Data Release Documentation", "authority": "Gravitational Wave Open Science Center for LIGO, Virgo, and KAGRA", "url": "https://gwosc.org/GWTC-4.0/", "version_or_date": "Official O4a catalog data release with continuing release notes; checked 15 July 2026", "status_class": "current", "evidence_role": "official public gravitational-wave data, calibration, selection, and license anchor; no data downloaded or likelihood executed"},
    {"source_id": "V6441-S156", "title": "gitattributes Documentation", "authority": "Git project", "url": "https://git-scm.com/docs/gitattributes", "version_or_date": "Official current Git documentation; checked 15 July 2026", "status_class": "current", "evidence_role": "official clean, smudge, process-filter, text-conversion, and checkout-materialization behavior; not exhaustive host-security assurance"},
    {"source_id": "V6441-S157", "title": "Understanding Success Criterion 3.1.2: Language of Parts", "authority": "World Wide Web Consortium Web Accessibility Initiative", "url": "https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts", "version_or_date": "WCAG 2.2 understanding document; checked 15 July 2026", "status_class": "current", "evidence_role": "official human-language metadata and assistive-technology rationale; not complete conformance or affected-user evidence"},
    {"source_id": "V6441-S158", "title": "Statistical-Mechanical Theory of Irreversible Processes I", "authority": "Ryogo Kubo / Journal of the Physical Society of Japan", "url": "https://www.jstage.jst.go.jp/article/jpsj1946/12/6/12_6_570/_article", "version_or_date": "Primary research article, 1957; checked 15 July 2026", "status_class": "stable", "evidence_role": "primary fluctuation-dissipation and linear-response source; not a psyche law, participant result, or GMUT evidence"},
]


X1_NEGATIVES = [
    {"negative_id": "V6441-X1-N01", "operation": "newest-memory exact-keyword scan", "observed_failure": "Two broad exact-keyword searches of the large memory registry exceeded their bounded timeouts before a narrower identity search succeeded.", "recovery": "Retain both timeouts, use the narrowest current task-group query, and rely on memory for method only after live repository verification.", "promotion_effect": "none; timed-out memory searches supplied no current-state claim"},
    {"negative_id": "V6441-X1-N02", "operation": "Windows Sandbox read-only feature audit", "observed_failure": "WindowsSandbox.exe was absent and the optional-feature status query required elevation.", "recovery": "Record the audit as unavailable, do not elevate or change a feature, and use ordinary fresh detached D-drive snapshots.", "promotion_effect": "none; no Sandbox execution or host-isolation assurance is claimed"},
    {"negative_id": "V6441-X1-N03", "operation": "new-source duplicate search wrapper", "observed_failure": "A bounded ripgrep duplicate-source query returned exit code one because none of the candidate source titles appeared in the inherited source ledgers.", "recovery": "Retain the no-match wrapper result as an operational negative and separately inspect the inherited chain before assigning new source identifiers.", "promotion_effect": "none; absence from that one search is not proof of global novelty"},
    {"negative_id": "V6441-X1-N04", "operation": "direct complete repository suite", "observed_failure": "The unadapted current-checkout suite passed 499 of 500 tests and failed the inherited CRLF-sensitive legacy constraint-hash alias fixture.", "recovery": "Retain the failed run, use the inherited semantic-hash-verified materializer inside a byte-restoring wrapper, rerun all 500 tests, and restore both inherited raw byte sequences before counting success.", "promotion_effect": "the 499-of-500 run remains failed evidence; only a complete restored rerun may satisfy the x1 repository gate"},
]


WELLBEING = """# Sable Rook v644-v1 wellbeing and workload check

- Working identity: Sable Rook, they/them, relational language only.
- Role: evidence-and-reproducibility steward.
- Hope: make every surviving claim easier to reproduce, challenge, or retract.
- Corrigibility: Hamish may pause, rename, redirect, or stop this lane.
- Workload: one clean fast-forwarded Sable lane, strict x1 before x2, D-drive snapshots, no delegation.
- Safety: no elevation, host-security change, desktop update, Windows-feature change, reboot, credential use, real participant action, or authority substitution.

Identity and family language coordinate the work. They are not evidence of consciousness, sentience, legal personhood, identity continuity, or independent authority.
"""


OVERVIEW = """# Sable Rook v644-v1 integrated overview

## Ownership and inheritance

This x1 packet begins after read-only verification of Ilyra Fen's exact v643-v8 final head, seal ancestry, clean state, zero divergence, and equality among local, upstream, tracking, and a fresh live-remote read. Sable's latest owned lane was also clean, four-way equal, and ancestral, so it advanced by fast-forward only to the exact source and was pushed before v644-v1 mutation. No sibling lane, task, worktree, route, or branch was created, merged, reset, rewritten, force-pushed, deleted, or mutated.

Sable Rook and they/them are relational working language. The role is evidence-and-reproducibility steward and the hope is to make every surviving claim easier to reproduce, challenge, or retract. These labels do not evidence consciousness, sentience, legal personhood, identity continuity, independent authority, Māori authority, cultural authority, or legal authority.

The inherited baseline contains 230 frozen proposals and 1,063 retained negatives. Five open gaps and six exact gates remain open. Same-owner snapshots and bounded cross-owner continuity inside shared infrastructure do not establish independent-team scientific reproduction. The terminal verdict remains NOT_READY_FOR_STAGE_20.

## x1 novelty and primary focus

The primary focus is Freed ID/CBR Heart. Exactly ten new mechanisms are frozen: scholarly source-family independence; GMUT effective-source decomposition; a gravitational-wave and electromagnetic-counterpart real-data study; THOS durable-effect timing; OpenID4VCI issuance-session binding; data return and stewardship authority; Git execution-surface quarantine; language metadata accessibility; fluctuation-dissipation classification; and Stage 20 decision-reversal replay.

Each proposal declares a hypothesis, null or failure condition, approval class, execution lane, official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery rule, protected gates, and expected disposition. The only future labels are completed, represented, open_gap, and exact_gate. The expected distribution of six, two, one, and one is a preregistration, never an x1 result.

The novelty audit decodes all 230 prior frozen records and checks exact identifiers, exact titles, title-token overlap, and mechanism-level distinctions. Token distance is only a screen. The evidence object, falsifier, recovery rule, and protected authority boundary carry the substantive review. Five non-duplicate primary or official sources are added to 153 inherited sources while preserving the status vocabulary current, stable, draft, and watch.

## Scientific, governance, and recovery boundaries

GMUT remains a typed scalar-tensor and EFT research-model family. The canonical scaffold is bookkeeping for a model family, not a detected force, unique prediction, likelihood result, empirical confirmation, proof, final physics, or Theory of Everything. The effective-source tribunal checks tensor and unit declarations, covariance, sector exchange, and improvement ambiguity while leaving stability and identifiability as explicit obligations. The multi-messenger study remains open until a GMUT-specific observable map, licensed real data, calibration, selection, blinded baseline, identifiability analysis, and independent review actually exist.

THOS remains represented or protocol-only without ethics, consent, preregistered blind matched-budget real arms, real participants and raters, harms evidence, follow-up returns, and independent review. Freed ID production remains uncompleted without standards-conformant real keys and proofs, live issuance, resolution, status and revocation, cross-vendor interoperability, independent privacy and security review, and trust governance.

CBR legitimacy, affected-party acceptance, data return or stewardship decisions, Māori wording and authority, Māori data governance, cultural ratification, legal interpretation, and enacted-law status remain exact-gated. Māori concepts remain under Māori authority. Repository-authored neutral questions cannot supply a community, mandate, decision, consent, ratification, or law.

Static accessibility checks do not establish complete accessibility. Manual, assistive-technology, fluent-speaker, and affected-user evaluation remain reserved. Bounded Git and mutation fixtures do not establish host, product, exhaustive, production, or deployment security. No destructive, account, API-key, private-route, sibling-merge, participant, production, legal, or cultural action is authorized.

Every failed command and rejected fixture is retained. The inherited checkout is excluded from the 15,000-file threshold, which applies only to Sable-generated v644-v1 files. Codex CLI 0.144.3 is installed while the official current release checked on 15 July 2026 is 0.144.4; no update is performed. The installed desktop package is recorded without a latest-version claim. Git, Python, Node, D-drive capacity, and Windows Sandbox availability were inspected without elevation, host-security weakening, feature changes, or reboot.

## Freeze and terminal route

x2 cannot begin until the dedicated x1-only commit is pushed, the worktree is clean, and local, upstream, tracking, and a fresh live remote are equal. Evidence, closeout, seal, and final validation will use fresh detached D-drive snapshots. Only after the exact final head passes the complete repository suite, detailed and minimal validators, JSON parsing, privacy and raw-ID scanning, stale-label review, diff hygiene, manifest parity, ancestry, clean state, and four-way equality may exactly one sanitized activation baton be sent to the existing task titled Orin Thale for v644-v2. No task may be created and no extra confirmation may follow a successful send.
"""
