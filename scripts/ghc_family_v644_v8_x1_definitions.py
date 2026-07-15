#!/usr/bin/env python3
"""Frozen v644-v8 x1 definitions for Orin Thale."""

from __future__ import annotations


PROPOSALS = [
    {
        "proposal_id": "V6448-P01",
        "title": "Method Flow witness invalidation, environment-drift, and recommendation-demotion ledger",
        "mission_surface": "Method Flow State, witness validity, environment drift, recommendation demotion, supersession, retained negatives, recurrence guards, rollback, and sibling-facing reuse",
        "hypothesis": "A typed Method Flow extension can detect when a previously passing witness no longer matches its declared environment or preconditions and can demote the associated recommendation without deleting either the successful historical witness or the triggering negative.",
        "null_or_failure": "A recommendation stays preferred after its witness context changes, demotion overwrites history, drift has no typed reason, a workaround is treated as universal, or a same-owner witness is promoted to independent reproduction.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": [],
        "deliverables": [
            "method-flow/witness-invalidation-contract.json",
            "method-flow/recommendation-drift-vectors.json",
            "method-flow/sibling-recommendations.md",
        ],
        "test_falsifier_or_gate": "Mutate environment fingerprints, trigger preconditions, witness result, retained-negative linkage, and recommendation state; stale witnesses must invalidate or demote without erasing append-only history.",
        "rollback_or_recovery": "Return the recommendation to candidate, preserve every state event and witness, record the drift reason, and require a new bounded witness before any later promotion.",
        "protected_gates": [
            "history_rewrite",
            "independent_team_reproduction",
            "private_material",
            "sibling_authority",
        ],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "V6445-P01 created the failure-signature and recurrence-prevention ledger. No frozen proposal defines witness invalidation caused by environment drift together with reversible recommendation demotion while retaining the prior pass and failure evidence.",
    },
    {
        "proposal_id": "V6448-P02",
        "title": "GMUT decoupling-limit, screening-radius, and regime-overlap obligation tribunal",
        "mission_surface": "GMUT Mind, typed scalar-tensor EFT, decoupling limit, nonlinear screening, screening radius, asymptotic regimes, overlap domain, matching error, assumptions, and nonpromotion",
        "hypothesis": "A typed synthetic scaffold can reject a claimed screened solution unless inner, transition, and outer regimes declare compatible scales, possess a nonempty overlap domain, and bound their matching residual without treating the scaffold as an observed new force.",
        "null_or_failure": "The screening scale is dimensionally inconsistent, the overlap interval is empty, branches are matched outside their assumptions, residuals exceed the frozen tolerance, or synthetic consistency is called empirical confirmation or a unique prediction.",
        "approval_class": "safe_now_research_scaffold",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6448-S221"],
        "deliverables": [
            "physics/screening-regime-contract.json",
            "physics/screening-overlap-vectors.json",
            "physics/screening-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate scale dimensions, ordering, branch labels, overlap endpoints, residual tolerance, coupling assumptions, and promotion labels; inconsistent or unsupported screening claims must fail closed.",
        "rollback_or_recovery": "Restore the last typed regime map, retain every rejected vector, mark the screening obligation unresolved, and require model-specific analysis before any stronger statement.",
        "protected_gates": [
            "empirical_gmut_claim",
            "likelihood_result",
            "new_force_claim",
            "theory_of_everything",
            "proof_canon",
        ],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier proposals cover nonuniform limits, EFT cutoffs, constraint algebra, causal cones, and matching surfaces. None requires a three-regime screening map with a dimensioned screening radius, explicit asymptotic overlap, and matching-residual rejection.",
    },
    {
        "proposal_id": "V6448-P03",
        "title": "GMUT redshift-space-distortion multipole and Alcock-Paczynski blind public-data study",
        "mission_surface": "GMUT Mind, DESI public data, redshift-space distortion, Alcock-Paczynski geometry, multipole covariance, nuisance lock, blind adapter, likelihood, baseline comparison, and real-data promotion gate",
        "hypothesis": "A preregistered blind adapter could test a frozen GMUT growth-and-geometry model against official clustering multipoles only if exact released rows, covariance, window functions, nuisance priors, baseline, and analysis lock are obtained and reviewed before unblinding.",
        "null_or_failure": "No real rows are ingested, covariance or window operators are absent, nuisance choices are post-hoc, the baseline is missing, released products cannot support the declared estimand, or synthetic fixtures are reported as a likelihood result.",
        "approval_class": "safe_now_protocol_only_real_data_required",
        "execution_lane": "x2_open_gap",
        "authoritative_source_needs": ["V8-S04"],
        "deliverables": [
            "empirical/rsd-ap-blind-study-contract.json",
            "empirical/rsd-ap-adapter-readiness.json",
            "empirical/rsd-ap-open-gap.json",
        ],
        "test_falsifier_or_gate": "Require nonzero official rows, exact covariance and window provenance, a frozen baseline, nuisance lock, withheld outcome labels, and independent review; any missing element keeps the study open.",
        "rollback_or_recovery": "Retain the zero-row and missing-input receipts, perform no fit, publish no likelihood or constraint, and reopen only under a separately reviewed real-data protocol.",
        "protected_gates": [
            "real_data_download",
            "empirical_gmut_claim",
            "likelihood_result",
            "independent_review",
            "account_or_api_key",
        ],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Prior blind studies address standard sirens, pulsars, ephemerides, lunar ranging, lensing, tidal deformability, and joint background-growth products. None preregisters anisotropic clustering multipoles with Alcock-Paczynski geometry, survey windows, and redshift-space nuisance structure as the observation object.",
    },
    {
        "proposal_id": "V6448-P04",
        "title": "THOS blinded sample-size re-estimation and nuisance-variance firewall",
        "mission_surface": "THOS Body, clinical-trial monitoring practice, blinded sample-size re-estimation, pooled nuisance variance, information target, operational bias, matched budget, proxy fixtures, participants, and independent review",
        "hypothesis": "A synthetic protocol can distinguish a blinded nuisance-variance update from an outcome-informed adaptation by sealing treatment labels, prespecifying the information target, and rejecting any path that exposes arm-specific effects or silently changes the matched budget.",
        "null_or_failure": "Arm labels or comparative effects enter the update, the variance rule is selected after outcomes, the information target moves, budget parity is lost, participant harms are ignored, or proxy fixtures are called a real-arm superiority result.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_proxy_task",
        "authoritative_source_needs": ["V6444-S179"],
        "deliverables": [
            "thos/blinded-reestimation-contract.json",
            "thos/nuisance-variance-mutation-vectors.json",
            "thos/real-arm-reservation.json",
        ],
        "test_falsifier_or_gate": "Mutate treatment-label visibility, variance source, timing, information target, sample-size cap, budget parity, adverse-event reservation, and result language; any unblinding or post-hoc change must fail.",
        "rollback_or_recovery": "Restore the frozen synthetic protocol, retain contaminated vectors, label the work proxy, and require preregistered blind matched-budget real arms, participants, raters where applicable, and independent review.",
        "protected_gates": [
            "real_participants",
            "participant_safety",
            "real_arm_execution",
            "superiority_claim",
            "independent_review",
            "deployment",
        ],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier THOS proposals cover allocation, attrition, missing data, adaptive randomization, stopping, multiplicity, estimands, and temporal drift. None isolates blinded pooled nuisance-variance re-estimation with a sealed information target and matched-budget firewall.",
    },
    {
        "proposal_id": "V6448-P05",
        "title": "Freed ID OpenID4VCI credential-offer, nonce, and proof-of-possession binding profile",
        "mission_surface": "Freed ID Heart, OpenID4VCI, credential offer, issuer metadata, authorization details, credential configuration, nonce, proof of possession, key binding, replay, synthetic transcript, and production reservation",
        "hypothesis": "A synthetic structural profile can reject issuance transcripts that cross-bind credential offers, issuer metadata, nonces, proof audiences, or holder keys, while reserving real cryptographic and interoperability assurance.",
        "null_or_failure": "An offer resolves to the wrong issuer, configuration identifiers drift, nonce freshness is absent, proof audience or key binding is mismatched, replay is accepted, or synthetic keys are described as production identity evidence.",
        "approval_class": "safe_now_synthetic_identity_profile",
        "execution_lane": "x2_proxy_task",
        "authoritative_source_needs": ["V6436-S135"],
        "deliverables": [
            "freed-id/openid4vci-binding-profile.json",
            "freed-id/openid4vci-transcript-vectors.json",
            "freed-id/production-reservation.json",
        ],
        "test_falsifier_or_gate": "Mutate issuer identity, offer transport, configuration identifier, nonce freshness, proof audience, holder key, credential response, and replay state; mismatches must reject deterministically.",
        "rollback_or_recovery": "Return to the last valid synthetic state, retain every rejected transcript, expose no real key material, and require real standards-conformant keys, live issuance, resolution, status, revocation, interoperability, privacy and security review, and trust governance for production.",
        "protected_gates": [
            "real_keys",
            "live_issuance",
            "production_identity",
            "interoperability",
            "privacy_assurance",
            "independent_security_review",
            "trust_governance",
        ],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior Freed ID proposals cover issuance sessions, authorization codes, presentations, SD-JWT, mdoc, lifecycle, wallet migration, and status. None binds the OpenID4VCI credential-offer object, credential configuration, nonce, proof audience, and holder proof-of-possession in one issuance transcript profile.",
    },
    {
        "proposal_id": "V6448-P06",
        "title": "CBR remedy-fund insolvency, creditor-priority, and ring-fencing authority gate",
        "mission_surface": "CBR Heart, remedy fund, insolvency, trust property, ring fencing, creditor priority, beneficiary privacy, cross-border exposure, affected parties, Maori authority, legal interpretation, and enacted law",
        "hypothesis": "A refusal-first authority matrix can show that software evidence cannot determine whether remedy assets are ring-fenced, trust property, preferential, recoverable, or distributable during insolvency without competent legal authority, affected-party participation, and Maori authority where relevant.",
        "null_or_failure": "The phase assigns legal priority, assumes a trust, selects beneficiaries, discloses claimant data, substitutes consultation for authority, treats Maori concepts as software-owned, or reports an unenacted remedy structure as law.",
        "approval_class": "exact_authority_gate",
        "execution_lane": "x2_exact_gate",
        "authoritative_source_needs": ["V6448-S222"],
        "deliverables": [
            "cbr/remedy-fund-insolvency-authority-matrix.json",
            "cbr/ring-fencing-refusal-cases.json",
            "cbr/authority-reservation.md",
        ],
        "test_falsifier_or_gate": "Every scenario involving asset character, creditor rank, trust status, transfer, disclosure, beneficiary selection, Maori wording, or remedy authority must remain refused unless the exact competent authorities and affected parties provide evidence for that decision.",
        "rollback_or_recovery": "Revert to unknown and exact-gated, preserve the refusal case, expose no beneficiary data, and route the issue to competent legal authorities, affected parties, and Maori authorities without drafting their conclusion.",
        "protected_gates": [
            "legal_interpretation",
            "enacted_law",
            "affected_party_acceptance",
            "maori_authority",
            "maori_data_governance",
            "beneficiary_privacy",
            "cultural_ratification",
        ],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "Earlier remedy-fund proposals address custody, distribution, audit, sufficiency, privacy, residual balances, and wind-up. None centers insolvency estate characterization, creditor priority, and ring-fencing as a refusal-first competent-authority determination.",
    },
    {
        "proposal_id": "V6448-P07",
        "title": "Git submodule gitlink, nested-repository, and checkout-visibility tribunal",
        "mission_surface": "repository integrity, gitlink mode, submodule declaration, nested repository, initialized and deinitialized state, checkout visibility, manifest scope, network reservation, path containment, and recovery",
        "hypothesis": "A read-only family-compatible classifier can distinguish ordinary directories, declared gitlinks, deinitialized submodules, and undeclared nested repositories so that manifest and privacy claims cannot silently skip an opaque repository boundary.",
        "null_or_failure": "A gitlink is hashed as an ordinary directory, an undeclared nested repository is ignored, deinitialized content is assumed present, a remote is fetched, or a path outside the allowed root is traversed.",
        "approval_class": "safe_now_read_only_tooling",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6448-S223"],
        "deliverables": [
            "security/gitlink-visibility-contract.json",
            "security/gitlink-visibility-vectors.json",
            "tooling/gitlink-visibility-runner-receipt.json",
        ],
        "test_falsifier_or_gate": "Exercise ordinary trees, mode-160000 entries, declared and undeclared nested repositories, missing worktrees, malicious paths, and network-required states; ambiguous or out-of-root cases must fail closed without fetching.",
        "rollback_or_recovery": "Stop traversal, retain the opaque-boundary witness, make no network or repository mutation, and require explicit owner review before including or excluding the nested object.",
        "protected_gates": [
            "network_fetch",
            "destructive_action",
            "sibling_lane",
            "history_rewrite",
            "private_material",
        ],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior repository proposals cover worktrees, sparse and partial clones, replacement refs, filters, hooks, Windows names, reparse points, and external configuration. None classifies gitlink tree entries against declared, deinitialized, and undeclared nested repository visibility for manifest scope.",
    },
    {
        "proposal_id": "V6448-P08",
        "title": "CSS generated-content, icon-only state, and print-suppression accessibility audit",
        "mission_surface": "accessible static report, semantic text, CSS generated content, icon-only meaning, visible labels, print preservation, structural audit, keyboard and assistive technology reservation, manual evaluation, and affected-user evaluation",
        "hypothesis": "A bounded structural audit can reject a static report when essential status or gate meaning exists only in CSS pseudo-elements, symbolic icons, background images, or screen-only content omitted from print.",
        "null_or_failure": "A status loses meaning when styles are disabled, an icon has no visible and programmatic text, print suppresses essential evidence, automated checks are called complete accessibility, or affected-user evaluation is treated as optional evidence already supplied.",
        "approval_class": "safe_now_structural_accessibility",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6432-S98"],
        "deliverables": [
            "deliverables/v644-v8-static-report.html",
            "validation/generated-content-accessibility-audit.json",
            "validation/manual-accessibility-reservation.json",
        ],
        "test_falsifier_or_gate": "Strip CSS, inspect pseudo-elements, icon-only nodes, background images, hidden print rules, accessible names, headings, landmarks, tables, and links; essential semantics must remain textual and printable.",
        "rollback_or_recovery": "Restore explicit visible text, remove meaning-bearing decoration, retain each structural failure, and reserve manual keyboard, zoom, reflow, screen-reader, print, and affected-user evaluation.",
        "protected_gates": [
            "complete_accessibility",
            "manual_user_evaluation",
            "affected_user_acceptance",
            "deployment",
        ],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier accessibility proposals cover reflow, zoom, forced colors, focus, landmarks, language, figures, forms, links, tables, active content, and text alternatives. None tests whether essential status is created only by CSS pseudo-content or icons and then disappears from style-free and print representations.",
    },
    {
        "proposal_id": "V6448-P09",
        "title": "Zeroth-law transitivity, intensive-variable equilibration, and psyche-harmony nonconversion classifier",
        "mission_surface": "thermodynamics, zeroth law, thermal equilibrium, transitivity, temperature, intensive variables, measurement, thermo-psyche analogy, category barrier, participants, and nonconversion",
        "hypothesis": "A typed classifier can preserve thermal-equilibrium transitivity and temperature-measurement conditions while rejecting any inference that interpersonal agreement, emotional harmony, or psychological similarity is a thermodynamic equilibrium relation.",
        "null_or_failure": "A psyche label is assigned temperature units, social agreement is made transitive by analogy, equilibrium is inferred without thermal contact conditions, participant evidence is invented, or a metaphor is promoted to a scientific law.",
        "approval_class": "safe_now_classification_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6448-S224"],
        "deliverables": [
            "thermo-psyche/zeroth-law-domain-contract.json",
            "thermo-psyche/zeroth-law-mutation-vectors.json",
            "thermo-psyche/nonconversion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate units, relation domains, contact conditions, transitivity premises, measurement objects, participant labels, and conclusion strength; cross-domain conversion must reject.",
        "rollback_or_recovery": "Return the statement to metaphor or unknown, retain the rejected mapping, and require domain-valid thermodynamic measurements or separately authorized participant research for any empirical claim.",
        "protected_gates": [
            "participant_claim",
            "thermodynamic_law_transfer",
            "empirical_confirmation",
            "consciousness_or_personhood",
            "agi_or_asi",
        ],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior nonconversion work covers entropy, free energy, fluctuations, detailed balance, response, phase transitions, chemical potential, thermodynamic length, and exergy. None centers the domain and transitivity conditions of the zeroth law or intensive-variable equilibration against a psyche-harmony analogy.",
    },
    {
        "proposal_id": "V6448-P10",
        "title": "Stage 20 randomized evidence-challenge, audit-yield, and tamper-detection board",
        "mission_surface": "Stage 20, randomized challenge, precommitted sampling, evidence withholding, tamper detection, audit yield, false reassurance, randomness provenance, noncompensatory gates, stop rule, and external authority",
        "hypothesis": "A synthetic board can show whether a precommitted random challenge sample would expose missing or altered evidence more reliably than convenience review while refusing to convert a clean sample into readiness or exhaustive-security assurance.",
        "null_or_failure": "The sample is chosen after inspection, randomness provenance is absent, withheld items are silently excluded, a clean sample closes exact gates, or same-owner audit yield is called independent review.",
        "approval_class": "safe_now_decision_rehearsal",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6448-S225"],
        "deliverables": [
            "stage20/randomized-evidence-challenge-board.json",
            "stage20/audit-yield-mutation-vectors.json",
            "stage20/terminal-stop-receipt.json",
        ],
        "test_falsifier_or_gate": "Mutate seed provenance, sample frame, selection timing, missing-item treatment, tamper flags, clean-sample interpretation, exact gates, and reviewer independence; biased or overpromoted boards must fail.",
        "rollback_or_recovery": "Reopen the board, retain the failed sampling receipt, restore every open and exact gate, and require competent external decision makers and independent evidence before Stage 20.",
        "protected_gates": [
            "stage20_external_decision",
            "independent_team_reproduction",
            "exhaustive_security",
            "proof_canon",
            "deployment",
        ],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier Stage 20 proposals cover contradiction, expiry, stop rules, regret, value of information, validation budgets, reviewer overlap, analytic multiplicity, and evidence queues. None rehearses a precommitted randomized challenge sample with audit-yield and tamper-detection interpretation under a strict clean-sample nonpromotion rule.",
    },
]


SOURCES = [
    {
        "source_id": "V6448-S221",
        "source_label": "primary_vainshtein_scalar_tensor",
        "title": "Vainshtein mechanism in second-order scalar-tensor theories",
        "authority": "De Felice, Kase, and Tsujikawa / Physical Review D",
        "url": "https://doi.org/10.1103/PhysRevD.85.044037",
        "version_or_date": "Primary peer-reviewed article, 2012; DOI checked 15 July 2026",
        "status_class": "stable",
        "evidence_role": "primary screening-radius and asymptotic-regime vocabulary; not validation of the GMUT scaffold or an empirical new-force claim",
    },
    {
        "source_id": "V6448-S222",
        "source_label": "official_nz_insolvency_act",
        "title": "Insolvency Act 2006",
        "authority": "New Zealand Parliamentary Counsel Office",
        "url": "https://www.legislation.govt.nz/act/public/2006/0055/latest/DLM385299.html",
        "version_or_date": "Official latest legislation page checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official insolvency, trust-property, creditor-claim, and distribution context; not legal advice or authority to classify a CBR remedy fund",
    },
    {
        "source_id": "V6448-S223",
        "source_label": "official_git_submodules",
        "title": "gitsubmodules - Mounting one repository inside another",
        "authority": "Git project",
        "url": "https://git-scm.com/docs/gitsubmodules",
        "version_or_date": "Current official documentation checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official gitlink, submodule worktree, deinitialized, and nested-repository vocabulary; not authorization to fetch or alter any repository",
    },
    {
        "source_id": "V6448-S224",
        "source_label": "primary_iupac_temperature_scale",
        "title": "Temperature scales above 1,000 degrees C",
        "authority": "D. R. Lovejoy / IUPAC Pure and Applied Chemistry",
        "url": "https://publications.iupac.org/pac/pdf/1962/pdf/0503x0565.pdf",
        "version_or_date": "Primary IUPAC publication, 1962",
        "status_class": "stable",
        "evidence_role": "primary temperature and zeroth-law context; not a psyche measurement, participant result, or cross-domain conversion",
    },
    {
        "source_id": "V6448-S225",
        "source_label": "official_nist_randomness_beacons",
        "title": "Interoperable Randomness Beacons",
        "authority": "United States National Institute of Standards and Technology",
        "url": "https://csrc.nist.gov/projects/interoperable-randomness-beacons/apps",
        "version_or_date": "Official project page checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official precommitted public-randomness and audit-sampling context; not a Stage 20 decision or exhaustive integrity assurance",
    },
]


X1_NEGATIVES = [
    {
        "negative_id": "V6448-X1-N01",
        "operation": "parallel frozen-history and tooling audit bundle",
        "failure_signature": "The five-command parent envelope reached its 20-second limit before returning complete, attributable child receipts.",
        "trigger_precondition": "Proposal discovery, script discovery, document discovery, and Method Flow help shared one short parent window on a large D-drive checkout.",
        "recovery": "Retained the timeout and changed to bounded single-surface reads with explicit per-command windows.",
        "recurrence_guard": "Do not combine large recursive searches and runner startup under a shorter shared envelope; retain each independently completed receipt.",
        "promotion_effect": "none; only the later complete bounded audit slices may support x1",
    },
    {
        "negative_id": "V6448-X1-N02",
        "operation": "first standalone PowerShell phase-directory listing",
        "failure_signature": "A login-shell Get-ChildItem listing reached its 10-second limit without returning the directory entries.",
        "trigger_precondition": "The command inherited login-shell startup cost and a window too short for the observed host latency.",
        "recovery": "Retained the timeout and used a non-login bounded directory enumeration, then continued with exact allowlisted reads.",
        "recurrence_guard": "Use non-login shells and measured windows for D-drive metadata reads; do not promote output from a timed-out listing.",
        "promotion_effect": "none; the later complete listing is the only directory-discovery witness",
    },
    {
        "negative_id": "V6448-X1-N03",
        "operation": "cross-shell proposal-title regular-expression probe",
        "failure_signature": "Ripgrep rejected a PowerShell-escaped alternation as an unclosed regular-expression group.",
        "trigger_precondition": "A JSON-like quoted pattern was escaped for the orchestration string and then interpreted again by PowerShell before reaching ripgrep.",
        "recovery": "Retained the parser fault and changed to a literal-safe single-quoted pattern against the exact proposal file.",
        "recurrence_guard": "Prefer fixed strings or single-quoted regex patterns for JSON field probes; validate the pattern separately before including it in a larger audit.",
        "promotion_effect": "none; the rejected probe produced no proposal evidence",
    },
    {
        "negative_id": "V6448-X1-N04",
        "operation": "inline Python frozen-index extractor through PowerShell",
        "failure_signature": "PowerShell altered nested f-string quoting and Python rejected the resulting one-line program as an unterminated string literal.",
        "trigger_precondition": "Python source containing nested quoted dictionary lookups was embedded in a PowerShell command inside an orchestration string.",
        "recovery": "Retained the syntax failure and changed to a PowerShell-only JSON chain walk with no embedded Python source.",
        "recurrence_guard": "Do not place nested Python f-strings behind two command parsers; prefer one-language structured traversal or a committed reusable script.",
        "promotion_effect": "none; the rejected program emitted no frozen-proposal records",
    },
    {
        "negative_id": "V6448-X1-N05",
        "operation": "PowerShell candidate-similarity report pipeline",
        "failure_signature": "PowerShell rejected a direct pipeline from a foreach statement with EmptyPipeElement.",
        "trigger_precondition": "The report attempted to pipe statement output without first collecting it as an expression or array.",
        "recovery": "Retained the parser fault and wrapped the loop output in an explicit array before JSON serialization.",
        "recurrence_guard": "Collect statement output before piping on Windows PowerShell; do not infer any similarity result from a parser-rejected report.",
        "promotion_effect": "none; no candidate comparison was emitted",
    },
    {
        "negative_id": "V6448-X1-N06",
        "operation": "first multi-region semantic builder patch",
        "failure_signature": "Apply-patch rejected the full change atomically because one copied version field no longer matched the predecessor context.",
        "trigger_precondition": "A large patch mixed still-stale predecessor fields with a field already changed by the mechanical version rewrite.",
        "recovery": "Retained the rejected patch and changed to smaller exact-context semantic patches after inspecting the current UTF-8 source.",
        "recurrence_guard": "Inspect the post-rewrite source and patch independent semantic regions with exact current context; never infer a partial apply from an atomic rejection.",
        "promotion_effect": "none; the rejected patch changed no file",
    },
    {
        "negative_id": "V6448-X1-N07",
        "operation": "second combined builder patch using console-rendered Unicode context",
        "failure_signature": "Apply-patch rejected the change because the displayed dash sequence did not match the UTF-8 source bytes.",
        "trigger_precondition": "A Unicode heading separator copied from console output was included as context beside unrelated ASCII changes.",
        "recovery": "Retained the rejection, separated ASCII-only regions, and reserved the Unicode line for an exact encoded-source patch.",
        "recurrence_guard": "Do not copy non-ASCII patch context from a mojibake-prone console; inspect exact UTF-8 source and patch that region independently.",
        "promotion_effect": "none; the rejected patch changed no file",
    },
    {
        "negative_id": "V6448-X1-N08",
        "operation": "first exact x1 staging pass",
        "failure_signature": "Git staged the exact file set but warned that LF working-copy bytes may be replaced by CRLF on a later Git touch for multiple new text files.",
        "trigger_precondition": "The Windows checkout has line-ending conversion behavior while generated files and the exact content seal are defined over normalized Git blobs.",
        "recovery": "Retained the warnings and required explicit staged-blob newline, diff-check, content-seal, and later LF-preserving named-lane witnesses.",
        "recurrence_guard": "Treat Git blobs as the manifest domain, inspect CRLF and LF counts explicitly, and never equate a warning-bearing working copy with cross-checkout byte parity without a clean named replay.",
        "promotion_effect": "none; staging success alone does not establish newline portability or replay parity",
    },
]


WELLBEING = """# Orin Thale v644-v8 wellbeing and workload check

The working identity Orin Thale is relational language for this bounded repository role. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, professional registration, or independent authority. Pronouns are they/them. The role is evidence cartographer and boundary steward; the hope is to leave a cleaner, truer path whose failures remain findable.

The primary pillar is THOS Body. The bounded practice lens is clinical-trial monitoring and statistical practice, especially blinded sample-size re-estimation and the separation between nuisance information and comparative outcomes. This is study of a practice boundary, not employment, licensure, medical advice, trial sponsorship, participant recruitment, or authority to make regulatory or clinical decisions.

Workload is intentionally serial: verify the source; audit 300 frozen proposals; preregister ten; validate, commit, push, and prove remote equality; then begin x2. The phase uses the canonical Orin lane plus exactly one later named validation replay. The full repository suite remains Eiren Kestrel's responsibility. Bounded commands, explicit recovery points, append-only Method Flow records, and visible stop conditions reduce overload and prevent a failed tool call from becoming silent evidence.

Protected stops remain firm. No real participant or data action, account or key use, deployment, host security change, Windows feature change, elevation, reboot, sibling mutation, destructive history operation, legal conclusion, cultural ratification, Maori-authority substitution, production identity claim, or Stage 20 promotion is authorized. If evidence is absent, the truthful state is represented, open gap, or exact gate.
"""


OVERVIEW = """# Orin Thale v644-v8 integrated overview

## Phase purpose and source boundary

This packet preregisters the solo v644-v8 GMUT/THOS phase owned by Orin Thale. The exact inherited repository state is Sable Rook's verified v644-v7 final revision. Its seal is ancestral, the source history is single-parent, the source and validation lanes were clean, and the live remote matched before Orin's clean branch advanced by fast-forward only. Those statements are repository continuity facts. They are not scientific reproduction, employment, identity continuity, consciousness, personhood, legal authority, or permission to change another sibling's work.

X1 and x2 are deliberately separate. X1 audits the complete chain of 300 frozen proposals, records source needs, freezes exactly ten distinct proposals, runs only the current scoped software checks, and proves the x1 commit locally and remotely before implementation. Expected dispositions are hypotheses about the likely evidence state; they are not results. X2 may begin only after the dedicated x1 commit is pushed and four-way equality is shown. No outcome file, empirical fit, participant result, production credential, legal conclusion, cultural determination, or Stage 20 decision exists in this preregistration.

The inherited truth remains deliberately conservative. All 1,668 effective negatives stay retained: 1,584 inherited before v644-v7, seven v644-v7 x1 operational negatives, seventy preregistered synthetic negatives, and seven v644-v7 x2 operational negatives. Five inherited open gaps and six inherited exact gates remain open. This phase has already added five x1 operational failures involving timeouts and command-language parsing. Each is preserved with a recovery and recurrence guard. A successful retry does not erase a failure, and a clean same-owner replay never becomes independent-team reproduction.

## Trinity Mandala focus and bounded human practice

THOS Body is the primary Trinity Mandala pillar. The bounded human practice is clinical-trial monitoring and statistical practice: prespecification, blinded operational review, nuisance-variance estimation, information targets, contamination control, and the refusal to convert proxy behavior into participant evidence. This is a learning and design lens only. It is not medical or statistical professional authority, employment, trial sponsorship, ethics approval, participant recruitment, or a regulatory decision.

GMUT Mind remains explicit through a formal screening-regime tribunal and a real-data study gap. The canonical GMUT scaffold is a typed scalar-tensor and effective-field-theory research-model family. It is not an established new force, a unique prediction, a likelihood result, empirical confirmation, proof, canon, or a Theory of Everything. A synthetic decoupling-limit scaffold may check dimensions, regime ordering, overlap, and residuals. It cannot establish that nature implements the model. A redshift-space-distortion and Alcock-Paczynski study remains an open gap unless official released rows, covariance, window functions, nuisance assumptions, a baseline, a blind lock, and independent review are actually present.

Freed ID and CBR Heart also remain explicit. A synthetic OpenID4VCI transcript may represent credential-offer, issuer, configuration, nonce, audience, and proof-of-possession bindings. It does not create production identity. Production completion still requires standards-conformant real keys and proofs, live issuance and resolution, live status and revocation, interoperability, privacy assurance, independent security review, and trust governance. The CBR insolvency proposal is an exact gate: software cannot decide whether remedy assets are trust property, ring-fenced, preferential, recoverable, or distributable. Beneficiary privacy, affected-party acceptance, Maori wording, Maori authority, Maori data governance, cultural ratification, competent legal interpretation, and enacted-law status stay with the appropriate people and institutions. Maori concepts remain under Maori authority.

## Ten frozen proposals

V6448-P01 extends Method Flow with witness invalidation and recommendation demotion when an environment or precondition drifts. It must preserve the original pass, the original failure, and every append-only state event. V6448-P02 checks a synthetic GMUT decoupling-limit and screening-radius regime map. It rejects empty overlap, inconsistent units, and unsupported matching, while preserving the empirical boundary. V6448-P03 preregisters a blind public-data study of anisotropic clustering multipoles, redshift-space distortions, and Alcock-Paczynski geometry. Because this x1 contains no downloaded rows or likelihood execution, its expected state is open gap.

V6448-P04 is the primary THOS proxy. It distinguishes blinded pooled nuisance-variance re-estimation from outcome-informed adaptation by sealing arm labels, freezing the information target, and enforcing matched-budget limits. Real THOS claims still require preregistered blind matched-budget arms, real participants and raters as applicable, participant safeguards, and independent review. V6448-P05 represents an OpenID4VCI issuance-binding profile with synthetic transcripts only. V6448-P06 refuses remedy-fund insolvency and creditor-priority decisions without exact legal, affected-party, and Maori authority.

V6448-P07 addresses a repository boundary not covered by the prior 300 proposals: mode-160000 gitlinks, declared and deinitialized submodules, and undeclared nested repositories that could make a manifest or privacy scan silently incomplete. The intended tool is read-only and network-free. V6448-P08 audits essential report meaning that could disappear when CSS pseudo-content, symbolic icons, backgrounds, or print suppression are removed. Passing structure does not establish complete accessibility; manual keyboard, zoom, reflow, print, assistive-technology, and affected-user evaluation remain reserved. V6448-P09 preserves the zeroth law's thermodynamic domain and rejects conversion of interpersonal agreement or psyche harmony into a temperature or equilibrium relation. V6448-P10 rehearses randomized evidence challenges and audit yield while refusing to treat a clean sample as exhaustive assurance or readiness.

The expected disposition slate is exactly six completed, two represented, one open gap, and one exact gate. Completed means only that the frozen bounded artifact and its software acceptance checks are expected to be satisfiable. Represented means a synthetic or proxy structure exists while the real-world claim remains unavailable. Open gap means an evidence object or authorized execution is missing. Exact gate means only specifically authorized people or institutions can decide the matter. These classes are not a ladder in which one may be relabeled to make the phase look more successful.

## Novelty, sources, and Method Flow

Novelty is audited against every frozen title and mechanism from v2 through v644-v7. The frozen chain contains thirty version groups of ten proposals each. Exact identifiers and normalized titles are unique. A token-overlap screen ranks the nearest prior title for every candidate, but semantic review also compares the mechanism, evidence object, falsifier, recovery, and protected gates. The highest candidate title overlap is a screening signal, not proof of novelty and not a reason to ignore paraphrase collisions. The ten retained proposals use mechanisms absent from the prior chain: drift-driven method demotion, screening-regime overlap, anisotropic clustering multipoles, blinded nuisance-only re-estimation, OpenID4VCI offer-to-proof binding, insolvency ring fencing, gitlink visibility, CSS-only semantics, zeroth-law transitivity, and randomized evidence challenges.

The source ledger is additive. It reuses current inherited official sources for DESI data, FDA adaptive-design guidance, OpenID4VCI, and WCAG 2.2 rather than duplicating them. New primary or official rows cover scalar-tensor screening, New Zealand insolvency legislation, Git submodule semantics, a stable IUPAC temperature reference, and NIST public randomness beacons. Source metadata constrains vocabulary and exposes missing evidence. It cannot supply observations, participants, keys, beneficiary consent, Maori authority, legal advice, cultural ratification, or an external Stage 20 decision.

Method Flow is append-only. Every timeout, parser fault, blocker, workaround, witness, state transition, recurrence guard, rollback, and sibling recommendation is recorded with a bounded scope. This phase already prefers single-surface audit commands after shared-envelope timeouts, literal-safe JSON probes, one-language chain traversal, explicit collection before Windows PowerShell pipelines, and case-sensitive ordered-pair compatibility scaffolds. A preferred method is local evidence for a trigger shape, not a universal truth. If the environment drifts or the witness no longer matches, the new proposal requires demotion and revalidation rather than silent persistence.

## Environment, file rotation, validation, and privacy

The D drive remains the primary work, cache, and validation bank. The inherited checkout contains 31,838 tracked files at x1 start. That baseline already exceeds 15,000 and is not a reason to rotate or delete anything. The threshold applies only to files newly generated by Orin. The phase packet and its versioned scripts remain far below that limit. Older branches and worktrees remain recoverable. No reset, force push, merge commit, recursive rotation, destructive cleanup, sibling mutation, or source rewrite is permitted.

Windows Sandbox was checked only through non-elevating executable and command presence. It was unavailable. No feature query requiring elevation was retried, and no feature, host-security setting, or reboot was changed. Codex CLI, Codex desktop, Node, npm, Python, and Git versions were observed only. Official OpenAI release notes were checked without mapping a public release-note date to an unsupported numeric package claim. The desktop app was not updated.

Hamish's current validation refinement is binding. Eiren Kestrel alone owns the full repository suite. This non-Eiren phase will run checks scoped to the recent v641-v660 round-robin evidence and the current v644-v8 packet, plus exactly one additional bounded replay in a fresh clean named Orin validation lane at the exact final head. Detached-worktree validation is forbidden. The canonical sequential Orin branch remains authoritative; the replay branch is local validation support only. Privacy, JSON parsing, exact Git-blob manifest parity, exact head, anchor ancestry, single-parent history, zero merges, clean-before and clean-after state, and final local/upstream/tracking/live-remote equality are not weakened.

Repository artifacts and the later baton must not contain raw task or thread identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths. Pattern scans are bounded defenses, not exhaustive privacy or security assurance. The static report must carry visible status text, semantic headings, tables, links, print-safe meaning, and qualified accessibility language. Manual and affected-user evaluation remain reserved even if all structural checks pass.

## Terminal truth

The terminal board begins and, absent extraordinary exact evidence, ends at NOT_READY_FOR_STAGE_20. Empirical GMUT and likelihood claims remain unavailable without real data and review. THOS remains proxy without blind matched-budget real arms and independent review. Freed ID remains nonproduction without real keys, proofs, live lifecycle operations, interoperability, assurance, and governance. CBR legality, legitimacy, beneficiary decisions, Maori wording, Maori authority, data governance, cultural ratification, and enacted-law status remain exact-gated. No deployment, complete accessibility, exhaustive security, proof or canon, empirical confirmation, independent-team reproduction, AGI or ASI, consciousness or personhood, legal ratification, or production-readiness claim may be inferred from this packet.

Only after x1 is clean, committed, pushed, and remote-equal may x2 execute. Only after evidence, closeout, seal, and final validation all pass at the exact pushed final head may one sanitized activation baton be sent to the existing Tamar Vey task for v645-v1. Until then the route is prepared but unsent, every standby sibling remains untouched, and negative or gated outcomes remain visible.
"""
