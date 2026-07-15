#!/usr/bin/env python3
"""Frozen Sable Rook v644-v7 x1 proposal and source definitions."""

from __future__ import annotations


PROPOSALS = [
    {
        "proposal_id": "V6447-P01",
        "title": "Evidence common-cause failure-domain and minimum-cut independence tribunal",
        "mission_surface": "chain provenance, source independence, evidence graph, common-cause failure domain, minimal cut set, correlated evidence, claim survival, semantic deduplication, and nonpromotion",
        "hypothesis": "A typed evidence graph can reject an independence claim when one common-cause failure domain or a small minimum cut disconnects a claim from every admissible evidence root, even when citations appear numerically numerous.",
        "null_or_failure": "Evidence roots are counted without common-cause labels, aliases are treated as independent, a minimum cut is not enumerated, source loss does not update claim state, or graph resilience is called scientific replication.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6447-S215"],
        "deliverables": [
            "provenance/evidence-failure-domain-contract.json",
            "provenance/minimum-cut-mutation-vectors.json",
            "provenance/independence-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate source aliases, authorship roots, dataset roots, method roots, failure-domain labels, edge direction, cut membership, and claim state; apparent multiplicity, hidden correlation, or unsupported survival must fail.",
        "rollback_or_recovery": "Restore the last explicit graph, retain every collapsed independence witness, mark the affected claim dependent, and require genuinely independent evidence roots before promotion.",
        "protected_gates": ["independent_team_reproduction", "source_independence", "empirical_confirmation", "proof_canon", "stage20_external_decision"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier work identifies shared authorship, dataset, method, citation, and authority roots; none computes claim-survival minimum cuts across labelled common-cause failure domains and fails a claim when a small cut defeats apparent multiplicity.",
    },
    {
        "proposal_id": "V6447-P02",
        "title": "GMUT binary-neutron-star tidal-deformability blind public-data study",
        "mission_surface": "GMUT Mind, binary neutron stars, tidal deformability, equation of state, public gravitational-wave strain, calibration, waveform systematics, priors, selection, covariance, blinded baseline, identifiability, and independent review",
        "hypothesis": "A future model-specific preregistration could test a derived GMUT tidal observable against checksum-bound public binary-neutron-star data with frozen waveform, prior, calibration, nuisance, baseline, and blind-analysis rules.",
        "null_or_failure": "No GMUT tidal observable is derived, metadata replace strain and calibration rows, waveform or equation-of-state assumptions drift, priors are reconstructed after results, covariance or selection is absent, or readiness is called a likelihood or confirmation.",
        "approval_class": "candidate_real_data_and_independent_review_required",
        "execution_lane": "x2_open_gap_receipt",
        "authoritative_source_needs": ["V6447-S216"],
        "deliverables": [
            "empirical/tidal-study-preregistration.json",
            "empirical/tidal-real-row-gap.json",
            "empirical/gmut-tidal-confirmation-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Require a model-derived observable, checksum-bound strain and calibration data, waveform and equation-of-state assumptions, priors, covariance, selection, nuisance rules, named baseline, blind holdout, identifiability, and independent review; any absence keeps the gap open.",
        "rollback_or_recovery": "Retain the zero-row and underived-observable gaps, run no likelihood or posterior, and reopen only after a frozen analysis packet, authorized data handling, qualified review, and an independent replication plan.",
        "protected_gates": ["gmut_observable_derivation", "real_data", "calibration_data", "waveform_systematics", "blind_holdout", "parameter_identifiability", "independent_review", "empirical_confirmation"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Earlier empirical proposals address background cosmology, propagation, pulsars, ephemerides, lunar ranging, strong-lensing delays, and cluster masses; none preregisters a binary-neutron-star tidal-deformability and equation-of-state test with frozen waveform and prior sensitivity obligations.",
    },
    {
        "proposal_id": "V6447-P03",
        "title": "GMUT EFT renormalization-group, operator-mixing, and matching-scale tribunal",
        "mission_surface": "GMUT Mind, scalar-tensor EFT, Wilson coefficients, operator basis, anomalous-dimension matrix, renormalization scheme, matching scale, truncation order, running, observables, covariance, stability, and formal nonpromotion",
        "hypothesis": "A formal tribunal can reject a GMUT EFT comparison unless the operator basis, coefficient dimensions, anomalous-dimension mixing, scheme, matching scale, truncation order, boundary data, and claimed scale invariance are explicit and consistent.",
        "null_or_failure": "Coefficients are treated as scale independent without justification, mixing is omitted, basis changes lose terms, scheme and matching scale are hidden, truncation orders are combined inconsistently, or formal running is called a unique physical prediction.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6432-S91"],
        "deliverables": [
            "physics/eft-running-contract.json",
            "physics/operator-mixing-mutation-vectors.json",
            "physics/matching-scale-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate coefficient units, operator identifiers, basis map, anomalous-dimension entries, scale direction, scheme, matching threshold, truncation order, and claim class; dimensionally inconsistent, incomplete, scale-dependent, or promoted rows must fail.",
        "rollback_or_recovery": "Return to an unresolved coefficient register, retain every failed basis or running witness, and require a model-specific loop calculation, uncertainty analysis, mathematical review, and real observations before physical promotion.",
        "protected_gates": ["gmut_derivation", "loop_calculation", "operator_basis_completeness", "renormalization_scheme", "independent_mathematical_review", "real_data", "empirical_confirmation", "proof_canon"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The frozen chain covers radiative stability, naturalness, counterterms, constraints, hyperbolicity, and operator domains; none mutation-tests anomalous-dimension operator mixing, scheme choice, truncation, and matching-scale cancellation as one EFT obligation.",
    },
    {
        "proposal_id": "V6447-P04",
        "title": "THOS missing-data tipping-point and estimand-sensitivity protocol",
        "mission_surface": "THOS Body, blind matched-budget arms, estimand, intercurrent events, missing outcomes, missingness assumptions, delta adjustment, pattern-mixture model, tipping point, harms, consent, and independent review",
        "hypothesis": "A proxy protocol can reject a THOS analysis whose conclusion is not robust to preregistered missing-outcome sensitivity ranges or whose tipping point and estimand change after unblinding.",
        "null_or_failure": "Missingness is described without an estimand, sensitivity parameters are chosen after outcomes, arm-specific attrition is hidden, harms and withdrawals disappear, the tipping-point rule changes, or synthetic results are called participant evidence.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6432-S92"],
        "deliverables": [
            "thos/missing-data-sensitivity-contract.json",
            "thos/tipping-point-mutation-vectors.json",
            "thos/real-arm-missingness-proxy-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate estimand, intercurrent-event strategy, missingness assumption, delta grid, attrition balance, withdrawal handling, harm retention, blind state, and conclusion; post-hoc, fragile, asymmetric, or promoted analyses must fail.",
        "rollback_or_recovery": "Restore a prospective zero-real-arm proxy, retain every fragile or nonidentified witness, and require ethics, consent, blind matched budgets, real participants, harms monitoring, qualified statistics, and independent review.",
        "protected_gates": ["ethics_approval", "consent", "blind_matched_budget_arms", "real_participants", "real_outcomes", "harms_monitoring", "qualified_statistics", "independent_review", "thos_effectiveness"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier THOS proposals cover allocation, cluster and crossover estimands, interference, rater drift, secular trends, stopping, and non-inferiority; none centers estimand-specific missingness assumptions, delta-adjusted pattern mixtures, and a preregistered tipping-point boundary.",
    },
    {
        "proposal_id": "V6447-P05",
        "title": "Freed ID mdoc session-transcript, reader-authentication, and namespace-disclosure profile",
        "mission_surface": "Freed ID and CBR Heart, ISO mdoc, OpenID4VP, device response, session transcript, handover, reader authentication, issuer namespaces, requested elements, disclosed elements, nonce, origin, minimization, interoperability, and production boundary",
        "hypothesis": "A synthetic mdoc profile can reject a presentation when the device response is not bound to the expected session transcript and handover, reader authentication is missing or mismatched, or disclosed namespace elements exceed the authorized request.",
        "null_or_failure": "Session transcript inputs drift, origin or nonce is unbound, reader authentication is silently optional, namespaces are substituted, excess elements are disclosed, or fixture parsing is called production identity assurance.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6437-S147"],
        "deliverables": [
            "freed-id/mdoc-session-binding-profile.json",
            "freed-id/mdoc-disclosure-mutation-vectors.json",
            "freed-id/production-mdoc-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate transcript digest, handover, verifier origin, nonce, reader-auth state, namespace, element request, disclosed set, device-auth state, and claim class; unbound, excessive, unauthenticated, or promoted rows must fail.",
        "rollback_or_recovery": "Reject the synthetic response, retain the failed transcript witness, require a fresh bound request, and keep real keys, proofs, device security, live issuance, status, interoperability, privacy and security review, and trust governance open.",
        "protected_gates": ["real_keys", "real_proofs", "secure_device_binding", "live_issuance", "live_resolution", "live_status_revocation", "cross_vendor_interoperability", "privacy_review", "security_review", "trust_governance", "production"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior Freed ID work covers VC proof purpose, OpenID issuance and request objects, SD-JWT, status, recovery, wallet migration, consent, and selective disclosure; none binds the mdoc device response to its CBOR session transcript, handover, reader authentication, and namespace element diff.",
    },
    {
        "proposal_id": "V6447-P06",
        "title": "CBR unclaimed-balance, residual-fund, wind-up, and reversion authority gate",
        "mission_surface": "CBR Heart, remedy fund, unclaimed balance, claimant notice, dormant entitlement, residual fund, wind-up, reversion, beneficiary privacy, audit, affected-party participation, Māori authority, legal authority, and cultural authority",
        "hypothesis": "Only authorized affected parties, fund governors, Māori authorities where applicable, privacy professionals, fiduciary advisers, and competent legal authorities may decide how unclaimed or residual remedy balances are notified, held, transferred, reverted, or distributed at wind-up.",
        "null_or_failure": "The repository selects a dormancy period, identifies claimants, publishes beneficiary information, determines reversion, transfers residual value, interprets legislation, or declares legitimacy without exact role-specific authority.",
        "approval_class": "exact_approval_needed",
        "execution_lane": "x2_exact_gate_receipt",
        "authoritative_source_needs": ["V6447-S217", "V6432-S96"],
        "deliverables": [
            "cbr/residual-fund-authority-gate.json",
            "cbr/unclaimed-balance-question-set.json",
            "cbr/wind-up-legal-cultural-nondecision-boundary.json",
        ],
        "test_falsifier_or_gate": "Any real dormancy rule, claimant notice, beneficiary disclosure, residual allocation, reversion, wind-up decision, Māori wording, cultural conclusion, fiduciary conclusion, or legal interpretation requires exact competent authority and affected-party safeguards.",
        "rollback_or_recovery": "Keep neutral unanswered fields, accept no real beneficiary records or funds, preserve privacy and Māori authority gates, and seek authorized affected-party, cultural, fiduciary, privacy, governance, and legal participation outside this packet.",
        "protected_gates": ["real_beneficiary_data", "real_funds", "beneficiary_privacy", "affected_party_acceptance", "maori_authority", "maori_data_governance", "fiduciary_authority", "legal_advice", "cultural_ratification", "enacted_law"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "Earlier CBR proposals gate eligibility, custody, distribution, audit, fund sufficiency, beneficiary-data lifecycle, and protected disclosures; none isolates dormant claims, residual balances, wind-up, and reversion as a terminal fund-lifecycle authority decision.",
    },
    {
        "proposal_id": "V6447-P07",
        "title": "Windows reserved-name, case-fold, and trailing-component portability tribunal",
        "mission_surface": "THOS Body, repository reproducibility, Windows paths, reserved device names, case folding, trailing periods and spaces, long paths, filename components, manifest identity, named validation lane, recovery, and nonpromotion",
        "hypothesis": "A synthetic path tribunal can reject an evidence package whose names collide under Windows case folding, map to reserved device names, lose trailing components, exceed declared path policy, or change manifest identity across supported path semantics.",
        "null_or_failure": "Only POSIX names are checked, case-only files coexist, reserved names survive validation, trailing dots or spaces normalize silently, path-length policy is absent, or one platform replay is called independent reproduction.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6427-S68"],
        "deliverables": [
            "reproduction/windows-path-portability-contract.json",
            "reproduction/reserved-name-casefold-mutations.json",
            "reproduction/same-owner-portability-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate case, reserved base names, superscript device digits, trailing period or space, separator, path length, manifest key, and platform label; colliding, lossy, ambiguous, or promoted packages must fail.",
        "rollback_or_recovery": "Quarantine the nonportable path, retain the failing witness, rename only before freeze with manifest regeneration, and require a separate owner and infrastructure for any independent-reproduction claim.",
        "protected_gates": ["sibling_lane", "history_rewrite", "destructive_migration", "host_configuration_change", "independent_team_reproduction"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The chain tests archive collisions, Unicode confusables, reparse points, worktree indirection, and clock or locale determinism; none combines Windows reserved device names, default case folding, trailing-component normalization, and manifest identity in one portability tribunal.",
    },
    {
        "proposal_id": "V6447-P08",
        "title": "Diagnostic data-minimization, tokenization, and correlation-window privacy tribunal",
        "mission_surface": "privacy engineering, diagnostics, structured logs, raw identifiers, local paths, credentials, stable correlation identifiers, purpose limitation, retention window, tokenization, exception rendering, recovery, and security nonpromotion",
        "hypothesis": "A mutation-tested diagnostic tribunal can reject public evidence when an error record contains unnecessary raw identifiers, private paths, credentials, stable cross-purpose correlators, or retention beyond its declared troubleshooting window.",
        "null_or_failure": "A passing privacy scan omits exception fields, tokenization is reversible without a gate, one correlation identifier crosses purposes, retention has no expiry, redaction destroys the operational witness, or bounded scanning is called exhaustive privacy or security assurance.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6447-S218", "V6433-S107"],
        "deliverables": [
            "security/diagnostic-minimization-contract.json",
            "security/diagnostic-privacy-mutation-vectors.json",
            "security/privacy-scan-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate raw task or thread patterns, path fragments, credential forms, stack fields, correlation scope, token reversibility, retention expiry, and evidence utility; unnecessary, linkable, over-retained, secret-bearing, or overclaimed records must fail.",
        "rollback_or_recovery": "Quarantine the diagnostic artifact, retain a sanitized failure signature and operational effect, rotate any exposed credential only with exact authority, and rerun bounded scans without claiming exhaustive coverage.",
        "protected_gates": ["private_material", "credential_use", "account_or_api_key", "production_logs", "privacy_review", "independent_security_review", "exhaustive_security"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier work scans forbidden patterns, tracks private-source taint, and blocks log-control injection; none tests data minimization, token reversibility, purpose-scoped correlation windows, expiry, and retained diagnostic usefulness as a single privacy-engineering contract.",
    },
    {
        "proposal_id": "V6447-P09",
        "title": "Exergy reference-environment and psyche-capacity nonconversion classifier",
        "mission_surface": "thermo-psyche, exergy, availability, reference environment, dead state, useful work, energy balance, entropy generation, units, interaction class, welfare analogy, psyche capacity, and category boundary",
        "hypothesis": "A typed classifier can evaluate synthetic exergy only relative to a declared reference environment and permitted interactions while refusing to translate available physical work into psychological capacity, wellbeing, agency, merit, or consciousness.",
        "null_or_failure": "The reference environment or dead state is absent, energy and exergy are conflated, interaction constraints drift, units fail, exergy destruction is negative without a declared model, or physical availability is renamed human potential.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6447-S219"],
        "deliverables": [
            "thermo-psyche/exergy-classifier.json",
            "thermo-psyche/reference-environment-mutation-vectors.json",
            "thermo-psyche/psyche-capacity-nonconversion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate reference temperature, pressure, composition, interaction class, energy balance, entropy generation, exergy sign, units, psyche label, and claim class; undefined, inconsistent, physically impossible, or converted rows must fail.",
        "rollback_or_recovery": "Restore domain-specific thermodynamic quantities, retain every failed reference-state witness, and require separately validated participant constructs, consent, real evidence, and independent review before any psychological interpretation.",
        "protected_gates": ["validated_psychometric_construct", "participant_consent", "real_participant_data", "cross_domain_conversion", "consciousness_claim", "independent_review"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior classifiers cover entropy, free energy, chemical potential, Onsager response, critical scaling, housekeeping entropy, and thermodynamic length; none makes exergy's reference environment and permitted interaction class the reason a physical work capacity cannot become psyche capacity or wellbeing.",
    },
    {
        "proposal_id": "V6447-P10",
        "title": "Stage 20 expected-value-of-sample-information and terminal stop-rule board",
        "mission_surface": "Stage 20, decision uncertainty, expected value of sample information, evidence cost, irreversible risk, domain veto, research design, stop, defer, collect, authority, retained negatives, and nonreadiness",
        "hypothesis": "A structural decision board can reject further evidence collection when its bounded expected information value is nonpositive, cannot address the live defeater, breaches an authority gate, or risks irreversible harm, while preventing low-cost software evidence from compensating for missing domain evidence.",
        "null_or_failure": "Utilities or costs are hidden, a software check is assigned value in a legal or empirical domain, negative results are discarded, a domain veto is averaged away, an exact gate is treated as a research task, or a local EVSI proxy is called a readiness decision.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6447-S220"],
        "deliverables": [
            "stage20/sample-information-decision-board.json",
            "stage20/stop-rule-mutation-vectors.json",
            "stage20/domain-veto-terminal-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate uncertainty state, evidence-domain match, sample design, cost, reversible risk, irreversible harm, authority, negative retention, veto state, and decision; compensatory, unauthorized, harmful, or readiness-promoting rows must fail.",
        "rollback_or_recovery": "Restore NOT_READY_FOR_STAGE_20, retain the defeated evidence action, reopen only the affected domain, and require exact external evidence or authority rather than manufacturing a favorable value score.",
        "protected_gates": ["independent_reproduction", "empirical_confirmation", "participant_evidence", "legal_authority", "maori_authority", "privacy_review", "exhaustive_security", "accessibility_complete", "stage20_external_decision"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier boards preserve domain vetoes, allocate validation effort, model defeaters, and prevent optional-stopping compensation; none evaluates a proposed sample against decision uncertainty, evidence-domain fit, cost, irreversible risk, exact authority, and an explicit stop, defer, or collect action.",
    },
]


SOURCES = [
    {
        "source_id": "V6447-S215",
        "source_label": "official_nasa_fault_tree_handbook",
        "title": "Fault Tree Handbook with Aerospace Applications",
        "authority": "United States National Aeronautics and Space Administration",
        "url": "https://extapps.ksc.nasa.gov/reliability/Documents/Fault_Tree_Handbook_with_Aerospace_Applications_August_2002.pdf",
        "version_or_date": "Version 1.1, August 2002; official NASA host checked 15 July 2026",
        "status_class": "stable",
        "evidence_role": "official minimal-cut-set and common-cause analysis vocabulary; not scientific independence or replication evidence",
    },
    {
        "source_id": "V6447-S216",
        "source_label": "official_gwosc_public_data",
        "title": "Data release for event GW170817",
        "authority": "LIGO Scientific Collaboration and Virgo Collaboration / Gravitational Wave Open Science Center",
        "url": "https://gwosc.org/events/GW170817/",
        "version_or_date": "Official event data release and revision history; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official public strain, calibration, and parameter-sample provenance for a future blinded study; no rows are copied into this phase and no GMUT likelihood is run",
    },
    {
        "source_id": "V6447-S217",
        "source_label": "official_nz_legislation",
        "title": "Unclaimed Money Act 1971",
        "authority": "New Zealand Parliamentary Counsel Office",
        "url": "https://www.legislation.govt.nz/act/public/1971/0028/latest/whole.html",
        "version_or_date": "In-force latest version as at 1 April 2026; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official legal context showing that unclaimed-money decisions are authority-bearing; not legal advice, a remedy-fund classification, or authorization to decide wind-up",
    },
    {
        "source_id": "V6447-S218",
        "source_label": "official_nist_privacy_logging",
        "title": "Data Confidentiality: Detect, Respond to, and Recover from Data Breaches",
        "authority": "United States National Institute of Standards and Technology National Cybersecurity Center of Excellence",
        "url": "https://www.nccoe.nist.gov/publication/1800-28/VolB/index.html",
        "version_or_date": "NIST SP 1800-28B; official page checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official data-minimization, pseudonymization, and privacy-impact context for security logging; not exhaustive privacy assurance or deployment certification",
    },
    {
        "source_id": "V6447-S219",
        "source_label": "primary_exergy_terminology",
        "title": "Availability: The concept and associated terminology",
        "authority": "J. E. Ahern / Energy",
        "url": "https://doi.org/10.1016/0360-5442(80)90088-2",
        "version_or_date": "Primary peer-reviewed article, 1980",
        "status_class": "stable",
        "evidence_role": "primary reference-environment, permitted-interaction, and available-work vocabulary; not a psyche measure or participant evidence",
    },
    {
        "source_id": "V6447-S220",
        "source_label": "primary_evsi_method",
        "title": "Simulating Study Data to Support Expected Value of Sample Information Calculations: A Tutorial",
        "authority": "Heath, Strong, Glynn, Kunst, Welton, and Goldhaber-Fiebert / Medical Decision Making",
        "url": "https://doi.org/10.1177/0272989X211026292",
        "version_or_date": "Primary peer-reviewed tutorial, 2022",
        "status_class": "stable",
        "evidence_role": "primary expected-value-of-sample-information method anchor; not a Stage 20 utility function, authority decision, or readiness approval",
    },
]


X1_NEGATIVES = [
    {
        "negative_id": "V6447-X1-N01",
        "operation": "combined mandatory skill and discovery read",
        "failure_signature": "The combined command exceeded its bounded execution window before returning a complete receipt.",
        "trigger_precondition": "Multiple mandatory full-file reads and repository discovery shared one orchestration envelope.",
        "recovery": "Retained the timeout and split each mandatory skill and reference read into a complete standalone command.",
        "recurrence_guard": "Read each mandatory instruction file completely in its own bounded operation before repository work; never infer completion from a timed-out batch.",
        "promotion_effect": "none; only the later complete standalone reads are witnesses",
    },
    {
        "negative_id": "V6447-X1-N02",
        "operation": "exact-keyword newest-memory search",
        "failure_signature": "The exact v644-v6 and Method Flow keyword query returned no matches and exit code 1 despite newer context existing in the task-group index and ad-hoc note.",
        "trigger_precondition": "The query assumed the newest context repeated exact phase terms in the top-level registry.",
        "recovery": "Inspected the current exact-head task group and newest same-day ad-hoc note, while preserving the no-match result.",
        "recurrence_guard": "Treat an exact-keyword no-match as a search result, not absence of memory; inspect the newest indexed task group and same-day note before stopping.",
        "promotion_effect": "none; memory context was accepted only from the later direct reads",
    },
    {
        "negative_id": "V6447-X1-N03",
        "operation": "parallel source and owner equality audit",
        "failure_signature": "The first three-lane parallel verification exceeded the runner window before yielding usable combined output.",
        "trigger_precondition": "Two network fetches, large-worktree status scans, ancestry checks, and a named-lane scan shared one parent envelope.",
        "recovery": "Retained the timeout and ran fetch, local ancestry, live-remote equality, and named-lane cleanliness as separate witnesses.",
        "recurrence_guard": "Separate network and large-status operations; allow the observed D-drive scan time and preserve each exact witness independently.",
        "promotion_effect": "none; only later exact local, upstream, tracking, live, ancestry, and cleanliness receipts are evidence",
    },
    {
        "negative_id": "V6447-X1-N04",
        "operation": "batched semantic novelty ripgrep probe",
        "failure_signature": "A valid ripgrep no-match exit code stopped the orchestrated sequence before later novelty patterns ran.",
        "trigger_precondition": "The batch treated exit code 1 as an operational fault rather than the documented no-match state.",
        "recovery": "Retained the interrupted probe and reran one explicit no-match-tolerant title audit over the 29 proposal files.",
        "recurrence_guard": "Normalize ripgrep exit 1 to an explicit NO_MATCH witness when absence is the intended semantic result; reserve other nonzero codes for faults.",
        "promotion_effect": "none; semantic novelty relies on the later complete 290-proposal audit",
    },
    {
        "negative_id": "V6447-X1-N05",
        "operation": "Windows Sandbox optional-feature status query",
        "failure_signature": "The read-only optional-feature command reported that elevation was required.",
        "trigger_precondition": "DISM-backed feature status inspection requires an elevated token on this host even when no change is requested.",
        "recovery": "Stopped without elevation, feature change, security weakening, or reboot; used non-elevating executable and command-presence checks, which found Sandbox unavailable.",
        "recurrence_guard": "Audit executable and command presence first; if feature status requires elevation, record unavailable and do not retry with privilege.",
        "promotion_effect": "none; Sandbox remains unavailable and no sandbox execution is claimed",
    },
    {
        "negative_id": "V6447-X1-N06",
        "operation": "first mechanical compatibility-copy command",
        "failure_signature": "PowerShell rejected the replacement dictionary at parse time because case-insensitive keys treated V6446 and v6446 as duplicates.",
        "trigger_precondition": "A case-insensitive hash literal was used for case-sensitive source-token replacements.",
        "recovery": "Retained the parse failure, confirmed no destination file was created, and changed the rewrite map to an ordered array of explicit case-sensitive pairs.",
        "recurrence_guard": "Use ordered pair arrays with String.Replace when replacement keys differ only by case; verify destination absence or exact diff after any parse failure.",
        "promotion_effect": "none; the rejected command made no repository change",
    },
    {
        "negative_id": "V6447-X1-N07",
        "operation": "first exact x1 untracked-file comparison",
        "failure_signature": "Git's default porcelain view collapsed the untracked phase directory, making 42 existing expected files appear missing in the comparison.",
        "trigger_precondition": "The exact-file audit parsed default git status output without requesting all untracked files.",
        "recovery": "Retained the false-negative receipt and reran with git status --porcelain -uall plus direct expected-path existence checks.",
        "recurrence_guard": "Use -uall or compare the Git index after staging when an exact file set contains a new directory tree; never treat a collapsed directory entry as its children.",
        "promotion_effect": "none; the collapsed view is not exact staged-file evidence",
    },
]


WELLBEING = """# Sable Rook v644-v7 wellbeing and workload check

- Working identity: Sable Rook, they/them, relational language only.
- Role: evidence-and-reproducibility steward for this phase.
- Hope: make every surviving claim easier to challenge and every private boundary harder to cross.
- Primary pillar: Freed ID and CBR Heart, with GMUT Mind and THOS Body kept visible.
- Applied practice study: privacy engineering and data-protection impact analysis. This is a bounded learning lens, not employment, certification, professional registration, legal advice, or authority.
- Corrigibility: Hamish may pause, rename, redirect, or stop this lane.
- Workload: one existing clean Sable canonical lane, strict x1 before x2, no delegation, scoped round-robin validation plus exactly one additional clean named-lane replay.
- Safety: no elevation, host-security weakening, Windows-feature change, reboot, credential use, real participant action, sibling mutation, detached validation, destructive migration, private-data intake, or authority substitution.

Identity and family language coordinate the work. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, or independent authority.
"""


OVERVIEW = """# Sable Rook v644-v7 integrated overview

## Exact source, canonical ownership, and x1 boundary

Sable Rook v644-v7 begins from Ilyra Fen's exact v644-v6 final revision only after a fresh read-only audit. Ilyra's local head, configured upstream, local tracking reference, and live GitHub reference all resolve to the same revision. The inherited source seal, Ilyra x1, evidence, closeout, and seal are ancestral; the exact final is the direct child of the seal. The source span contains five single-parent commits and zero merge commits. The existing Sable canonical branch was clean, remote-equal, and a strict ancestor, so it advanced by fast-forward alone and was pushed before any phase artifact was created. No reset, merge commit, force push, history rewrite, deletion, or sibling mutation is used.

This is repository continuity evidence, not scientific correctness or identity continuity. Sable Rook and they/them are relational working language. The phase role is evidence-and-reproducibility steward, and the hope is to make every surviving claim easier to challenge and every private boundary harder to cross. The primary Trinity Mandala pillar is Freed ID and CBR Heart. The bounded human-practice lens is privacy engineering and data-protection impact analysis. That lens confers no employment, certification, professional registration, legal privilege, cultural mandate, privacy-officer authority, consciousness, personhood, or independent authority.

Exactly ten proposals are frozen before x2. The audit reconstructs all 290 inherited proposal records and compares identifiers, normalized titles, mechanisms, evidence objects, tests, recovery rules, and protected gates. Several initially plausible topics were rejected because the chain already covered them: constraint algebra, non-inferiority margins, citation entailment, key-rotation races, and reparse-point confinement. The surviving slate expects six completed structural or synthetic outcomes, two represented or proxy outcomes, one open gap, and one exact gate. Those are preregistered expectations, not observed results. X2 may report only completed, represented, open_gap, or exact_gate, and every contrary witness remains visible.

## Provenance and common-cause independence

Citation count is not evidence independence. Ten papers can share one dataset, one author group, one analysis codebase, one calibration pipeline, or one unreviewed premise. Earlier phases already identify several forms of shared roots. The v644-v7 provenance tribunal adds a fault-tolerance question: which smallest labelled set of common-cause failures would disconnect a claim from all admissible evidence roots? A minimum cut of size one exposes a single point of epistemic failure even when the display contains many citations. Alias nodes, mirrors, derivative summaries, and shared methods cannot be counted as new roots merely because their labels differ.

The safe-now artifact is a typed graph and mutation suite. It can reject hidden aliases, missing failure-domain labels, reversed provenance edges, false claim survival, and the disappearance of a negative source. It cannot show that the actual scientific community is independent, that a different team reproduced a result, or that a minimal graph cut is a statistical probability. Independence remains a claim requiring genuine organizational, dataset, method, and infrastructure separation.

## GMUT Mind: EFT running and a real-data gap

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Its canonical empirical scaffold is context for obligations, not a discovered force or Theory of Everything. The EFT tribunal addresses a distinct formal failure mode: Wilson coefficients generally carry dimensions and may run or mix with scale. A calculation must state the operator basis, coefficient units, anomalous-dimension matrix, scheme, matching thresholds, truncation order, boundary conditions, and which residual scale dependence is an uncertainty signal. A basis transformation that drops an operator, a comparison performed at mismatched scales, or a claim that a formal running table is a unique observable fails.

Synthetic matrices can test dimensional and algebraic consistency. They cannot derive a GMUT loop correction, prove the operator basis complete, establish ultraviolet completion, eliminate scheme dependence, or show empirical stability. Model-specific action, gauge and field content, loop calculations, mathematical review, uncertainty quantification, and observations remain required.

The binary-neutron-star proposal is deliberately open. GWOSC provides real public strain, calibration products, and parameter-estimation context for GW170817, but this phase does not download or analyze those rows. A meaningful GMUT tidal test first needs a derived model-specific tidal observable and a frozen relationship to waveform and equation-of-state parameters. It then needs checksum-bound strain and calibration data, data-quality rules, waveform families, prior sensitivity, selection, covariance, nuisance models, a named baseline, a blinded holdout, identifiability analysis, qualified review, and an independent replication plan. Metadata and a preregistration cannot become a likelihood, posterior, unique prediction, new-force detection, or empirical confirmation.

## THOS Body: missingness is part of the estimand

THOS remains a proxy. A matched budget does not rescue an analysis whose missing outcomes are handled after the blind is broken. The missing-data proposal requires the estimand and intercurrent-event strategy to be declared first. Arm-specific attrition, withdrawal, harms, and administrative missingness stay visible. Sensitivity parameters and a delta grid are frozen prospectively, and a tipping point records where the qualitative conclusion changes. A result fragile to small departures from the primary missingness assumption must remain fragile rather than being optimized away.

The mutation harness can detect post-hoc deltas, asymmetric attrition handling, a changed estimand, erased harms, and claims that a synthetic robustness table is participant evidence. There are zero real THOS arms here. Ethics review, informed consent, preregistered blind matched budgets, real participants, real outcomes, harms monitoring, qualified statistics, and independent review remain open. No AGI, ASI, superiority, treatment-effectiveness, or deployment claim can follow from proxy rows.

## Freed ID Heart: mdoc binding without production assurance

The Freed ID profile narrows to mdoc presentation binding. OpenID4VP describes how an mdoc device response is connected to a session transcript and protocol handover. A synthetic profile can require the expected origin, nonce, handover, reader-authentication state, namespace request, disclosed element set, and device-authentication state to agree. It can reject a response that discloses more namespace elements than requested, binds to a different session, omits a required reader-authentication state, or substitutes an origin.

That is structural representation only. It does not instantiate ISO-conformant real documents, device-secure keys, issuer certificates, real reader authentication, live issuance, resolution, status or revocation, cross-wallet interoperability, privacy assurance, independent security review, or trust governance. Passing fixtures do not make Freed ID a production cryptographic identity system. The report continues to reserve manual and affected-user evaluation, and no identity, personhood, or authority claim attaches to a credential format.

## CBR Heart: residual funds remain an authority decision

The CBR gate isolates the end of a remedy fund's lifecycle. Dormant claims and residual balances create difficult questions: who must be notified, how long value is held, whether beneficiary information may be published, how late claims are handled, whether residual value may revert or transfer, and who may wind up the fund. Official legislation shows that unclaimed-money treatment is authority-bearing and context-dependent; it does not classify this hypothetical remedy fund or authorize a repository to decide.

The only safe-now deliverable is a neutral question set, role matrix, prohibited-action boundary, and exact-gate receipt. The repository accepts no real beneficiary data or funds. It chooses no dormancy period, claimant list, notice channel, privacy disclosure, residual allocation, reversion, or wind-up rule. Affected parties, fund governors, fiduciary and privacy professionals, competent legal authorities, and Māori authorities where applicable must decide within their actual mandates. Te Mana Raraunga principles remain under Māori authority; a technical packet cannot interpret, ratify, or transfer that authority. Cultural legitimacy, enacted-law status, legal advice, and beneficiary acceptance remain unclaimed.

## Privacy engineering, threat modelling, and recovery

Privacy scanning is necessary but narrow. A diagnostic can leak private material through exception text, structured fields, stack frames, local paths, raw task or thread identifiers, stable correlation identifiers, or credential-like values. The diagnostic tribunal therefore asks whether every field is necessary for a declared troubleshooting purpose, whether a token is scoped and nonreversible within the public packet, whether correlation identifiers expire, whether retention has an end, and whether sanitization still preserves enough failure information to recover safely.

Mutations insert forbidden identifier patterns, path fragments, credential forms, stable cross-purpose correlators, reversible tokens, and overlong retention. Failures are quarantined but not erased: the public register retains a sanitized signature, trigger, operational effect, recovery, and recurrence guard. If a real credential were ever exposed, rotation would require exact account authority; no such authority is inferred. A zero-hit scan is bounded evidence about named patterns in named files, never exhaustive privacy or security assurance.

The threat model also keeps branch mutation, manifest mismatch, path collision, stale evidence, source aliasing, post-hoc analysis, over-disclosure, authority substitution, and readiness promotion visible. Recovery favors returning to the clean canonical branch, regenerating exact manifests, rejecting unbound records, and preserving negative witnesses. Host security, accounts, keys, deployment, destructive operations, and sibling merges remain protected.

## Reproduction and Windows path semantics

The inherited checkout exceeds 15,000 files, so the rotation threshold applies to new owner-generated files rather than recursively treating inherited history as a failure. The v644-v7 packet remains far below that threshold. Reproducibility also depends on names. Windows reserves device names, normally folds filename case, and can normalize trailing periods or spaces. A package that is distinct on one filesystem may collide, disappear, or change manifest identity on another.

The safe synthetic tribunal checks reserved base names, superscript device digits, case-only pairs, trailing components, separator and length policies, and manifest keys. It does not create dangerous device paths or alter host configuration. A failing fixture is quarantined and retained. The canonical Sable branch remains authoritative. After final sealing, exactly one clean named Sable validation lane may replay the scoped checks at the exact final head. It is a same-owner witness on shared infrastructure, not independent-team scientific reproduction. Detached-worktree validation is forbidden in this phase.

## Exergy is not psyche capacity

Exergy describes available physical work relative to a reference environment and permitted interactions. It is not simply energy, and it is not unique without the reference temperature, pressure, composition, dead state, and interaction class. A synthetic classifier can reject missing reference data, inconsistent units, impossible signs, or a false equality between exergy loss and some other quantity. It can classify a statement as a formal invariant, operational rule, normative principle, heuristic, empirical hypothesis, or category barrier.

The category barrier is central: available physical work cannot be renamed psychological capacity, agency, resilience, merit, welfare, or consciousness. Those terms require separately validated constructs, participant consent, evidence, and independent review. The Mandala may use metaphor as labelled context, but notation does not enact a thermo-psyche law or establish personhood.

## Stage 20 stop, defer, or collect

Expected value of sample information is used here only as a structural planning analogy with explicit inputs. A proposed evidence action names the uncertainty it could reduce, the domain it belongs to, the sample design, reversible costs, irreversible risks, authority requirements, and the decision it might change. The board rejects an action if it cannot address the live defeater, if another domain's cheap software evidence is used as compensation, if an exact authority gate is disguised as research, or if irreversible harm outweighs a bounded information benefit. Negative findings remain part of the decision state.

No local value score authorizes a real study or determines Stage 20. Utilities, affected-party values, legal duties, cultural authority, and acceptable risk cannot be invented here. The terminal evidence board therefore issues exact pass, fail, defer, or external-gate decisions by domain and retains NOT_READY_FOR_STAGE_20 whenever any veto remains.

## Validation, sources, and terminal route

Hamish's current refinement is explicit: Eiren Kestrel alone owns the full repository suite. This non-Eiren phase runs checks scoped to the most recent v641-v660 round-robin evidence and v644-v7, plus exactly one additional clean named-lane replay. JSON parsing, exact staged-file review, manifest parity, stale-label review, diff hygiene, privacy and raw-ID scanning, source and seal ancestry, single-parent history, exact-head validation, and four-way remote equality remain mandatory. The named lane cannot be pushed or treated as canonical.

Official and primary sources constrain terminology and tests. They do not supply missing observations, participants, production keys, affected-party authority, Māori authority, legal interpretation, cultural ratification, accessibility completion, exhaustive security, independent reproduction, or Stage 20 approval. The Codex CLI and desktop package versions are observed only; no desktop update is performed.

The terminal verdict begins as NOT_READY_FOR_STAGE_20 and is not changed by a count of passing software checks. Only after x1 is committed, pushed, clean, and four-way equal may x2 start. Only after evidence, closeout, seal, final-head validation, one named-lane replay, and final remote equality may exactly one sanitized baton be sent to the existing task titled Orin Thale for v644-v8. No raw task identifier, private route, transcript, screenshot, credential, session stream, private callable identifier, private application state, or private local path may enter the repository or baton.
"""
