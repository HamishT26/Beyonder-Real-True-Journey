#!/usr/bin/env python3
"""Frozen v645-v1 x1 definitions for Tamar Vey."""

from __future__ import annotations


PROPOSALS = [
    {
        "proposal_id": "V6451-P01",
        "title": "Method Flow child-process start attestation, evidence-credit, and preflight-failure ledger",
        "mission_surface": "Method Flow State, parser failure, launcher preflight, child-process start, evidence credit, exit receipt, retained negative, recurrence guard, rollback, and sibling-safe recommendation",
        "hypothesis": "A typed Method Flow extension can distinguish a parser or launcher failure that executes no evidence-producing child command from a started child process and can withhold replay credit unless a bounded start and completion receipt exist, while retaining every failed attempt.",
        "null_or_failure": "A parser-failed wrapper receives replay credit, a missing start marker is inferred from intent, a timed-out child is called complete, a retry erases the original negative, or a same-owner start receipt is promoted to independent reproduction.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": [],
        "deliverables": [
            "method-flow/child-start-credit-contract.json",
            "method-flow/child-start-credit-vectors.json",
            "method-flow/sibling-recommendations.md",
        ],
        "test_falsifier_or_gate": "Mutate parser outcome, launcher outcome, child start token, command fingerprint, completion receipt, timeout state, retained-negative link, and replay count; only one actually started and successfully completed bounded child may receive replay credit.",
        "rollback_or_recovery": "Return the attempt to zero-credit observed failure, retain its negative, repair only the wrapper or launcher, and require a new bounded child-start and completion witness before promotion.",
        "protected_gates": [
            "history_rewrite",
            "private_material",
            "sibling_authority",
            "independent_team_reproduction",
        ],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "V6445-P01 records failure signatures and V6448-P01 invalidates stale witnesses. No prior frozen proposal assigns evidence credit using an explicit boundary between parser or launcher preflight failure and an actually started evidence-producing child process.",
    },
    {
        "proposal_id": "V6451-P02",
        "title": "GMUT adiabatic-mode, soft-limit, and gauge-artifact obligation tribunal",
        "mission_surface": "GMUT Mind, typed scalar-tensor EFT, cosmological perturbations, adiabatic mode, long-wavelength limit, residual gauge transformation, curvature conservation, soft relation, assumptions, and nonpromotion",
        "hypothesis": "A typed synthetic tribunal can reject a claimed cosmological soft-limit relation unless the long-wavelength mode, residual gauge transformation, regularity assumptions, constraint equations, and conserved quantity are stated consistently without treating the relation as an observed GMUT prediction.",
        "null_or_failure": "A gauge artifact is counted as a physical mode, the long-wavelength limit is taken outside declared regularity assumptions, entropy or anisotropic-stress terms are silently omitted, dimensions or perturbative orders conflict, or synthetic consistency is called empirical confirmation.",
        "approval_class": "safe_now_research_scaffold",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6451-S226"],
        "deliverables": [
            "physics/adiabatic-soft-limit-contract.json",
            "physics/soft-limit-mutation-vectors.json",
            "physics/soft-limit-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate wave-number scaling, gauge generator, regularity, constraint satisfaction, entropy source, anisotropic stress, conserved-variable definition, perturbative order, and promotion language; inconsistent or unsupported relations must fail closed.",
        "rollback_or_recovery": "Restore the last typed assumption set, retain every rejected vector, mark the soft-limit obligation unresolved, and require model-specific analysis and real observations before any stronger statement.",
        "protected_gates": [
            "empirical_gmut_claim",
            "likelihood_result",
            "unique_prediction",
            "new_force_claim",
            "theory_of_everything",
            "proof_canon",
        ],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier GMUT proposals cover gauge fixing, perturbative order, constraints, causal cones, matching, screening, and identifiability. None centers cosmological adiabatic residual modes and the assumptions needed to turn a long-wavelength gauge transformation into a soft-limit obligation.",
    },
    {
        "proposal_id": "V6451-P03",
        "title": "GMUT late-time integrated Sachs-Wolfe galaxy-cross-correlation blind public-data study",
        "mission_surface": "GMUT Mind, Planck public products, late-time integrated Sachs-Wolfe effect, galaxy tracer, sky mask, selection kernel, cross spectrum, covariance, baseline, blind analysis lock, real rows, likelihood, and promotion gate",
        "hypothesis": "A preregistered blind adapter could compare a frozen GMUT late-time potential-evolution model with an official CMB-galaxy cross-correlation only if exact maps or released spectra, masks, tracer kernels, covariance, nuisance assumptions, a baseline, and an independent review lock are present before unblinding.",
        "null_or_failure": "No real rows or maps are ingested, mask or tracer-window provenance is absent, cross-covariance is improvised, foreground or look-elsewhere choices are post-hoc, the baseline is missing, or synthetic fixtures are reported as a likelihood or constraint.",
        "approval_class": "safe_now_protocol_only_real_data_required",
        "execution_lane": "x2_open_gap",
        "authoritative_source_needs": ["V6451-S227", "V8-S03"],
        "deliverables": [
            "empirical/isw-cross-correlation-study-contract.json",
            "empirical/isw-adapter-readiness.json",
            "empirical/isw-real-row-open-gap.json",
        ],
        "test_falsifier_or_gate": "Require nonzero official inputs, exact map and mask lineage, tracer selection kernels, covariance, frozen nuisance treatment, a declared baseline, withheld decision labels, and independent review; any missing element keeps the study open.",
        "rollback_or_recovery": "Retain the zero-row and missing-input receipts, run no fit, publish no likelihood or parameter constraint, and reopen only under a separately reviewed real-data protocol.",
        "protected_gates": [
            "real_data_download",
            "empirical_gmut_claim",
            "likelihood_result",
            "independent_review",
            "account_or_api_key",
        ],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Prior blind GMUT studies cover sirens, pulsars, Solar-System tests, lensing, tidal deformability, growth multipoles, and background-plus-growth likelihoods. None uses the late-time integrated Sachs-Wolfe CMB-galaxy cross-correlation with coupled sky masks and tracer kernels as the frozen observation object.",
    },
    {
        "proposal_id": "V6451-P04",
        "title": "THOS independent data-monitoring firewall, operational-bias, and recommendation-minimization protocol",
        "mission_surface": "THOS Body, clinical-trial monitoring, independent data monitoring committee, open and closed sessions, unblinded statistician, sponsor firewall, operational bias, recommendation minimization, matched budget, proxy fixtures, participants, and independent review",
        "hypothesis": "A synthetic protocol can distinguish a bounded monitoring recommendation from leakage of comparative interim data by sealing role permissions, separating open and closed materials, minimizing recommendation content, and rejecting operational changes that reveal arm-specific trends or break matched-budget parity.",
        "null_or_failure": "Unblinded tables reach operational staff, recommendation wording reveals comparative effects, sponsor queries reconstruct interim outcomes, role conflicts are ignored, budget parity changes, participant safeguards are omitted, or proxy messages are called a real-arm superiority result.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_proxy_task",
        "authoritative_source_needs": ["V6451-S228"],
        "deliverables": [
            "thos/data-monitoring-firewall-contract.json",
            "thos/recommendation-leakage-mutation-vectors.json",
            "thos/real-arm-monitoring-reservation.json",
        ],
        "test_falsifier_or_gate": "Mutate role membership, session visibility, report granularity, recommendation text, sponsor query paths, operational response, adverse-event reservation, matched budget, and result language; any reconstructable comparative signal or unauthorized adaptation must fail.",
        "rollback_or_recovery": "Restore the frozen synthetic role matrix, retain contaminated messages, label the work proxy, and require preregistered blind matched-budget real arms, participant safeguards, competent monitoring authority, and independent review.",
        "protected_gates": [
            "real_participants",
            "participant_safety",
            "real_arm_execution",
            "clinical_authority",
            "superiority_claim",
            "independent_review",
            "deployment",
        ],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier THOS proposals cover blinding, scorers, adjudication, adverse events, adaptations, stopping, nuisance re-estimation, and matched budgets. None models the information boundary between an independent monitoring committee's closed session and a minimized sponsor-facing recommendation channel.",
    },
    {
        "proposal_id": "V6451-P05",
        "title": "Freed ID OpenID Federation trust-chain, entity-statement expiry, and policy-operator profile",
        "mission_surface": "Freed ID Heart, OpenID Federation, entity configuration, subordinate statement, trust anchor, trust chain, expiry, authority hints, metadata policy, policy operators, key rollover, synthetic transcript, and production reservation",
        "hypothesis": "A synthetic structural profile can reject federation chains whose issuer-subject linkage, signature-key reference, expiry ordering, authority-hint path, trust anchor, or metadata-policy operator application is inconsistent while reserving real cryptographic and interoperability assurance.",
        "null_or_failure": "A chain skips an authority edge, trusts an expired statement, applies an unsupported policy operator, accepts a key rollover without linkage, chooses an undeclared trust anchor, or describes synthetic signatures as production identity assurance.",
        "approval_class": "safe_now_synthetic_identity_profile",
        "execution_lane": "x2_proxy_task",
        "authoritative_source_needs": ["V6451-S229"],
        "deliverables": [
            "freed-id/federation-trust-chain-profile.json",
            "freed-id/federation-chain-mutation-vectors.json",
            "freed-id/production-federation-reservation.json",
        ],
        "test_falsifier_or_gate": "Mutate issuer, subject, authority hints, trust anchor, statement expiry, signing key, key rollover, chain ordering, policy operator, metadata result, and replay state; malformed or unsupported chains must reject deterministically.",
        "rollback_or_recovery": "Return to the last valid synthetic chain, retain every rejected transcript, expose no real key material, and require standards-conformant real keys and proofs, live federation resolution, interoperability, privacy and security review, and trust governance for production.",
        "protected_gates": [
            "real_keys",
            "live_resolution",
            "production_identity",
            "interoperability",
            "privacy_assurance",
            "independent_security_review",
            "trust_governance",
        ],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior Freed ID proposals cover DID control, issuer and verifier sessions, presentations, status, recovery, migration, pairwise identifiers, OpenID4VP, OpenID4VCI, SD-JWT, and mdoc. None evaluates a multilevel OpenID Federation trust chain with expiring entity statements and ordered metadata-policy operators.",
    },
    {
        "proposal_id": "V6451-P06",
        "title": "CBR remedy-fund investment mandate, inflation-risk, and loss-allocation authority gate",
        "mission_surface": "CBR Heart, public-interest fund administration, fiduciary governance, investment mandate, inflation preservation, liquidity, risk, loss allocation, beneficiary privacy, conflicts, affected parties, Maori authority, legal interpretation, and enacted law",
        "hypothesis": "A refusal-first authority matrix can show that software evidence cannot select a remedy-fund investment mandate, risk tolerance, inflation objective, liquidity reserve, service provider, or loss-allocation rule without competent fiduciary and legal authority, affected-party participation, and Maori authority where relevant.",
        "null_or_failure": "The phase recommends an asset allocation, sets a return target, assigns losses, chooses custodians or advisers, reveals beneficiary data, substitutes consultation for authority, treats Maori concepts as software-owned, or reports a proposed mandate as enacted law.",
        "approval_class": "exact_authority_gate",
        "execution_lane": "x2_exact_gate",
        "authoritative_source_needs": ["V6444-S181", "V6443-S171"],
        "deliverables": [
            "cbr/remedy-fund-investment-authority-matrix.json",
            "cbr/inflation-loss-allocation-refusal-cases.json",
            "cbr/fiduciary-authority-reservation.md",
        ],
        "test_falsifier_or_gate": "Every scenario involving investment objective, risk, liquidity, inflation, delegation, fees, conflicts, loss allocation, disclosure, beneficiary selection, Maori wording, or remedy authority must remain refused unless exact competent authorities and affected parties provide evidence for that decision.",
        "rollback_or_recovery": "Revert to unknown and exact-gated, preserve the refusal case, expose no beneficiary data, and route the issue to competent fiduciary and legal authorities, affected parties, and Maori authorities without drafting their conclusion.",
        "protected_gates": [
            "fiduciary_decision",
            "legal_interpretation",
            "enacted_law",
            "affected_party_acceptance",
            "maori_authority",
            "maori_data_governance",
            "beneficiary_privacy",
            "cultural_ratification",
        ],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "Earlier remedy-fund proposals address custody, distribution, audit, sufficiency, unclaimed balances, wind-up, insolvency, creditor priority, and beneficiary privacy. None reserves the investment mandate, inflation objective, liquidity-risk tradeoff, delegated management, and loss allocation to exact fiduciary, legal, affected-party, and Maori authority.",
    },
    {
        "proposal_id": "V6451-P07",
        "title": "Git LFS pointer, materialized-object, and missing-content boundary tribunal",
        "mission_surface": "repository integrity, Git LFS pointer, version line, object identifier, declared size, Git blob, materialized working-tree object, missing local object, smudge reservation, network prohibition, manifest scope, privacy scan, and recovery",
        "hypothesis": "A read-only family-compatible classifier can distinguish ordinary Git blobs, valid and malformed LFS pointers, materialized LFS content, and pointer-only missing-content states so a manifest or privacy claim cannot silently treat a small pointer as the referenced large object.",
        "null_or_failure": "A pointer is hashed as if it were materialized content, malformed keys or sizes are accepted, missing objects are called complete, the classifier fetches from a network, or an out-of-root object path is traversed.",
        "approval_class": "safe_now_read_only_tooling",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6451-S230"],
        "deliverables": [
            "security/git-lfs-boundary-contract.json",
            "security/git-lfs-pointer-mutation-vectors.json",
            "tooling/git-lfs-boundary-runner-receipt.json",
        ],
        "test_falsifier_or_gate": "Exercise ordinary blobs, canonical pointers, wrong versions, non-SHA-256 identifiers, size mismatches, extension lines, oversized pointers, missing objects, materialized content, malicious paths, and network-required states; ambiguity must fail closed without fetching.",
        "rollback_or_recovery": "Stop classification, retain the opaque-content witness, make no network or repository mutation, and require explicit owner review before including or excluding the referenced object from a manifest or privacy claim.",
        "protected_gates": [
            "network_fetch",
            "destructive_action",
            "sibling_lane",
            "history_rewrite",
            "private_material",
        ],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior repository proposals cover clean and smudge filters generally, partial clones, sparse checkouts, object alternates, replacement refs, gitlinks, hooks, paths, and archives. None classifies the canonical Git LFS pointer grammar against local materialization and missing-content states for manifest and privacy scope.",
    },
    {
        "proposal_id": "V6451-P08",
        "title": "Color-only status, contrast-token, and monochrome-redundancy accessibility audit",
        "mission_surface": "accessible static report, status text, use of color, text contrast, non-text contrast, design token, monochrome representation, visible cue, structural audit, manual evaluation, affected-user evaluation, and nonconformance reservation",
        "hypothesis": "A bounded structural audit can reject a static report when completion, warning, gap, or gate meaning is conveyed only by hue or when declared foreground-background tokens fail frozen contrast calculations, while preserving visible textual status and a monochrome cue.",
        "null_or_failure": "A red or green state has no text label, adjacent graphical states rely only on hue, a contrast token is missing or below the frozen ratio, automated calculations are called complete accessibility, or manual and affected-user evaluation are treated as already supplied.",
        "approval_class": "safe_now_structural_accessibility",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6432-S98"],
        "deliverables": [
            "deliverables/v645-v1-static-report.html",
            "validation/color-contrast-structural-audit.json",
            "validation/manual-accessibility-reservation.json",
        ],
        "test_falsifier_or_gate": "Remove color, convert the report to a monochrome state map, inspect visible status text and redundant marks, calculate frozen token contrasts, and inspect headings, landmarks, tables, and links; color-dependent or under-contrast fixtures must fail.",
        "rollback_or_recovery": "Restore explicit visible text and redundant shapes or borders, replace failing color tokens, retain each structural failure, and reserve manual keyboard, zoom, reflow, screen-reader, print, color-perception, and affected-user evaluation.",
        "protected_gates": [
            "complete_accessibility",
            "manual_user_evaluation",
            "affected_user_acceptance",
            "deployment",
        ],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier accessibility proposals cover reflow, forced colors, print, focus, names, landmarks, figures, forms, links, tables, abbreviations, active content, and CSS-generated meaning. None freezes explicit color tokens, calculates their contrast, and requires status meaning to survive a monochrome representation with a visible non-color cue.",
    },
    {
        "proposal_id": "V6451-P09",
        "title": "Heat-capacity response, convexity stability, and psyche-resilience nonconversion classifier",
        "mission_surface": "thermodynamics, heat capacity, temperature derivative, extensive energy, constant-pressure and constant-volume conditions, convexity, stability, phase behavior, thermo-psyche analogy, resilience label, participant evidence, and nonconversion",
        "hypothesis": "A typed classifier can preserve heat-capacity definitions, constraint conditions, units, and stability caveats while rejecting any inference that emotional resilience, social adaptability, or psychological coping is a heat capacity or thermodynamic convexity relation.",
        "null_or_failure": "A psyche label receives joules per kelvin, constant-pressure and constant-volume quantities are interchanged, a negative response is interpreted without domain conditions, participant evidence is invented, or an analogy is promoted to a fundamental law.",
        "approval_class": "safe_now_classification_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6451-S231"],
        "deliverables": [
            "thermo-psyche/heat-capacity-domain-contract.json",
            "thermo-psyche/heat-capacity-mutation-vectors.json",
            "thermo-psyche/resilience-nonconversion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate units, derivative variables, pressure or volume constraints, sign, stability premises, phase domain, psyche labels, participant fields, and conclusion strength; cross-domain conversion must reject.",
        "rollback_or_recovery": "Return the statement to metaphor or unknown, retain the rejected mapping, and require domain-valid thermodynamic measurements or separately authorized participant research for any empirical claim.",
        "protected_gates": [
            "participant_claim",
            "thermodynamic_law_transfer",
            "empirical_confirmation",
            "consciousness_or_personhood",
            "agi_or_asi",
        ],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior nonconversion proposals cover entropy, free energy, detailed balance, fluctuation response, phase transitions, chemical potential, thermodynamic length, exergy, temperature, and the zeroth law. None centers heat-capacity derivatives, their constraint variables, and convexity or stability conditions against a psyche-resilience analogy.",
    },
    {
        "proposal_id": "V6451-P10",
        "title": "Stage 20 circular-support, self-citation, and bootstrap-evidence rejection board",
        "mission_surface": "Stage 20, assurance argument, directed support graph, circular justification, self-citation, bootstrap evidence, strongly connected component, external root, noncompensatory gate, retained negative, stop rule, and external authority",
        "hypothesis": "A synthetic decision board can reject a readiness argument whose apparent support is generated only by a cycle of mutually citing receipts, while preserving legitimate acyclic derivations and refusing to let repeated internal references substitute for an external evidence root.",
        "null_or_failure": "A strongly connected support component is counted as multiple independent roots, a receipt cites its own derived output, duplicate internal references increase assurance, exact gates are closed by graph density, or same-owner structure is called independent review.",
        "approval_class": "safe_now_decision_rehearsal",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6446-S214"],
        "deliverables": [
            "stage20/circular-support-rejection-board.json",
            "stage20/support-graph-mutation-vectors.json",
            "stage20/terminal-stop-receipt.json",
        ],
        "test_falsifier_or_gate": "Mutate support edges, self-loops, derived-artifact roots, duplicated citations, strongly connected components, withdrawn sources, exact gates, and reviewer labels; rootless cycles or overpromoted boards must fail.",
        "rollback_or_recovery": "Reopen the board, retain the failed support graph, collapse circular components to zero independent-root credit, restore every open and exact gate, and require competent external decision makers and independent evidence before Stage 20.",
        "protected_gates": [
            "stage20_external_decision",
            "independent_team_reproduction",
            "exhaustive_security",
            "proof_canon",
            "deployment",
        ],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier Stage 20 proposals cover contradiction, expiry, cut sets, stop rules, regret, value of information, validation budgets, reviewer overlap, multiplicity, sampling, and evidence queues. None rejects a directed assurance graph whose only apparent roots are self-citation or mutually bootstrapped derived receipts.",
    },
]


SOURCES = [
    {
        "source_id": "V6451-S226",
        "source_label": "primary_adiabatic_modes",
        "title": "Adiabatic Modes in Cosmology",
        "authority": "Steven Weinberg / Physical Review D",
        "url": "https://arxiv.org/abs/astro-ph/0302326",
        "version_or_date": "Primary research preprint and peer-reviewed article, 2003; record checked 16 July 2026",
        "status_class": "stable",
        "evidence_role": "primary long-wavelength adiabatic-mode and gauge-assumption anchor; not validation of the GMUT scaffold, a unique prediction, or empirical confirmation",
    },
    {
        "source_id": "V6451-S227",
        "source_label": "official_nasa_planck_products",
        "title": "LAMBDA - The Planck Mission",
        "authority": "NASA Goddard Space Flight Center / LAMBDA",
        "url": "https://lambda.gsfc.nasa.gov/product/planck/",
        "version_or_date": "Official public-product page checked 16 July 2026",
        "status_class": "current",
        "evidence_role": "official Planck product and archive provenance for a preregistered ISW adapter; not downloaded rows, a cross-correlation result, or a GMUT likelihood",
    },
    {
        "source_id": "V6451-S228",
        "source_label": "official_fda_dmc_guidance",
        "title": "Establishment and Operation of Clinical Trial Data Monitoring Committees",
        "authority": "United States Food and Drug Administration",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/establishment-and-operation-clinical-trial-data-monitoring-committees",
        "version_or_date": "Final guidance, March 2006; official page checked 16 July 2026",
        "status_class": "stable",
        "evidence_role": "official DMC role, responsibility, and operating-procedure vocabulary; not ethics approval, monitoring authority, participant evidence, or a THOS result",
    },
    {
        "source_id": "V6451-S229",
        "source_label": "official_openid_federation",
        "title": "OpenID Federation 1.0",
        "authority": "OpenID Foundation",
        "url": "https://openid.net/specs/openid-federation-1_0.html",
        "version_or_date": "Final Specification approved 17 February 2026; checked 16 July 2026",
        "status_class": "stable",
        "evidence_role": "official entity-statement, trust-chain, trust-anchor, expiry, and metadata-policy vocabulary; not production Freed ID conformance, cryptographic assurance, interoperability, or trust governance",
    },
    {
        "source_id": "V6451-S230",
        "source_label": "primary_git_lfs_specification",
        "title": "Git LFS Specification",
        "authority": "Git Large File Storage project",
        "url": "https://github.com/git-lfs/git-lfs/blob/main/docs/spec.md",
        "version_or_date": "Primary project specification, current main record checked 16 July 2026",
        "status_class": "current",
        "evidence_role": "primary pointer grammar, object identifier, size, and materialization behavior; not authorization to fetch, mutate, or migrate repository content",
    },
    {
        "source_id": "V6451-S231",
        "source_label": "official_iupac_heat_capacity",
        "title": "IUPAC Gold Book - heat capacity, C",
        "authority": "International Union of Pure and Applied Chemistry",
        "url": "https://goldbook.iupac.org/terms/view/H02753",
        "version_or_date": "Stable Compendium of Chemical Terminology entry; checked 16 July 2026",
        "status_class": "stable",
        "evidence_role": "official heat-capacity definition and unit context; not a psyche measurement, participant result, or cross-domain law",
    },
]


X1_NEGATIVES = [
    {
        "negative_id": "REPRO-V6451-X1-N01",
        "operation": "parallel cold-start skill and memory read batch",
        "failure_signature": "The batch exceeded the ten-second shell startup budget before any required document content returned.",
        "trigger_precondition": "Four concurrent cold PowerShell reads each used a ten-second timeout.",
        "recovery": "Retained the timeout, initialized Method Flow, and read each mandatory document serially with a thirty-second bounded timeout.",
        "recurrence_guard": "Serialize required cold-start skill reads and allow at least thirty seconds per PowerShell process.",
        "promotion_effect": "none; the timed-out batch produced no guidance evidence",
    },
    {
        "negative_id": "REPRO-V6451-X1-N02",
        "operation": "parallel repository discovery with a no-match query",
        "failure_signature": "The aggregate call failed when ripgrep correctly returned exit code one for no AGENTS.md matches.",
        "trigger_precondition": "Promise-style aggregation treated an acceptable no-match result as a fatal shell error.",
        "recovery": "Retained the failure, ran discovery independently, and normalized ripgrep exit code one to an explicit zero-file result.",
        "recurrence_guard": "Normalize no-match exit codes before aggregating discovery commands whose empty result is valid.",
        "promotion_effect": "none; the failed aggregate returned no repository-instruction result",
    },
    {
        "negative_id": "REPRO-V6451-X1-N03",
        "operation": "ripgrep search with a Windows wildcard path argument",
        "failure_signature": "Ripgrep received the wildcard path literally and returned an invalid filename or directory error after an earlier receipt had printed.",
        "trigger_precondition": "A shell wildcard was placed in the path position instead of using a directory path plus ripgrep's glob filter.",
        "recovery": "Retained the partial failure and changed to an explicit scripts directory with a -g filename filter.",
        "recurrence_guard": "On Windows, pass a real directory to ripgrep and express filename wildcards through -g; do not credit output from an overall failed aggregate as a complete discovery witness.",
        "promotion_effect": "none; the failed aggregate did not complete scoped-command discovery",
    },
    {
        "negative_id": "REPRO-V6451-X1-N04",
        "operation": "first x1 preregistration build",
        "failure_signature": "The builder rejected expected_files_present because the x1 staged-review receipt cannot exist before the first exact staging pass.",
        "trigger_precondition": "The staged-review output was required as an ordinary pre-build input rather than deferred until the staged file set existed.",
        "recovery": "Retained the failed build and deferred only the staged-review self-output during the pre-stage build, with a required exact staged review and final rebuild before commit.",
        "recurrence_guard": "Treat a receipt whose subject is the staged file set as a deferred self-output until staging exists; never mark it passed without an actual staged-blob review.",
        "promotion_effect": "none; the rejected builder run did not establish a valid x1 packet",
    },
    {
        "negative_id": "REPRO-V6451-X1-N05",
        "operation": "first exact x1 staging pass",
        "failure_signature": "Git staged the exact file set but warned that LF working-copy bytes may be replaced by CRLF on a later Git touch for twelve new text files.",
        "trigger_precondition": "The Windows checkout applies line-ending conversion behavior while generated artifacts and content seals are defined over normalized Git blobs.",
        "recovery": "Retained the warnings, verified the exact staged Git blobs and content seal, and reserved LF-preserving validation for the one later clean named replay.",
        "recurrence_guard": "Treat the Git index as the committed manifest domain, record working-copy line-ending warnings, and do not claim cross-checkout byte parity without the clean named replay.",
        "promotion_effect": "none; staging success alone does not establish working-tree newline portability",
    },
    {
        "negative_id": "REPRO-V6451-X1-N06",
        "operation": "first stale-label fixed-string probe",
        "failure_signature": "Windows native argument marshaling split a quoted ripgrep fixed-string pattern with spaces into multiple path arguments.",
        "trigger_precondition": "A quote-bearing multiword JSON fragment was passed from PowerShell to a native executable as the pattern argument.",
        "recovery": "Retained the invalid probe and changed to PowerShell Select-String with SimpleMatch over the explicit owner-scoped files.",
        "recurrence_guard": "Use structured PowerShell string matching for quote-bearing multiword JSON fragments; never credit a zero-hit result when the native tool reports path errors.",
        "promotion_effect": "none; the invalid probe produced no stale-label evidence",
    },
]


WELLBEING = """# Tamar Vey v645-v1 wellbeing and workload check

The working identity Tamar Vey is relational language for this bounded repository role. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, professional registration, or independent authority. Pronouns are they/them. The role is evidence-systems cartographer and boundary keeper; the hope is to leave every decision legible, every failure recoverable, and every authority boundary intact.

The primary Trinity Mandala pillar is Freed ID/CBR Heart. The bounded human-practice lens is public-interest fund administration and fiduciary governance, especially the separation between auditable information, professional advice, affected-party participation, and decisions that only authorized fiduciaries, legal authorities, beneficiaries, and Maori authorities may make. This is study of a practice boundary, not employment, licensure, financial advice, investment management, legal advice, fund custody, beneficiary representation, or authority to move or allocate money.

Workload is intentionally serial: verify and fast-forward the canonical lane; audit 310 frozen proposals; preregister ten; validate, commit, push, and prove remote equality; then begin x2. Hamish's current refinement reserves the full repository suite to Eiren Kestrel. Tamar runs only scoped recent-round checks and exactly one later bounded replay in a clean named Tamar lane. Detached validation is not used. Bounded commands, append-only Method Flow records, and visible stop conditions prevent a failed wrapper from becoming silent evidence.

Protected stops remain firm. No participant or real-data action, account or key use, deployment, host-security change, Windows feature change, elevation, reboot, sibling mutation, destructive history operation, investment decision, legal conclusion, cultural ratification, Maori-authority substitution, production identity claim, or Stage 20 promotion is authorized. When evidence or authority is absent, the truthful state is represented, open gap, or exact gate.
"""


OVERVIEW = """# Tamar Vey v645-v1 integrated overview

## Purpose, source, and identity boundary

This packet preregisters the solo v645-v1 GMUT/THOS phase owned by Tamar Vey. The exact inherited repository state is Orin Thale's verified v644-v8 final revision. Orin's seal and every supplied phase anchor are ancestral; the source history is single-parent with zero merges; the source worktree was clean; and local, upstream, tracking, and the fresh live remote all matched before Tamar's clean canonical branch advanced by fast-forward only. Tamar then pushed that safe fast-forward and re-established four-way equality before any phase mutation. These are repository-continuity facts. They are not consciousness, personhood, employment, identity continuity, scientific reproduction, professional standing, legal authority, or permission to change another sibling's lane.

X1 and x2 are deliberately separate. X1 audits the complete chain of 310 frozen proposals, records source needs and current source status, freezes exactly ten distinct proposals, runs only the non-Eiren scoped software checks, and proves the x1 commit locally and remotely before implementation. Expected dispositions are preregistration hypotheses, never results. X2 may begin only after the dedicated x1 commit is pushed and local, upstream, tracking, and live-remote equality are all demonstrated. No x2 outcome file, empirical fit, participant result, production credential, investment recommendation, legal conclusion, cultural determination, deployment decision, or Stage 20 promotion exists in this freeze.

The inherited negative record remains deliberately intact. All 1,750 inherited effective negatives stay preserved: 1,668 inherited before v644-v8, eight v644-v8 x1 operational negatives, seventy preregistered synthetic negatives, and four v644-v8 x2 or terminal operational negatives. Five inherited open gaps and six inherited exact gates remain open. This phase adds two x1 operational failures: a cold parallel-read timeout and an aggregate-discovery failure caused by an acceptable no-match exit code. Both were recorded before retry, linked to Method Flow witnesses, and promoted only after bounded passing recoveries. Success does not erase failure. A same-owner witness remains same-owner evidence under shared infrastructure.

## Trinity Mandala and bounded human practice

Freed ID and CBR Heart is the primary Trinity Mandala pillar. The bounded practice lens is public-interest fund administration and fiduciary governance: documentation, conflicts, delegation, liquidity, prudent process, beneficiary information, affected-party participation, and the refusal to turn technical evidence into investment or legal authority. This is a learning and design lens only. It is not employment, professional registration, investment management, financial advice, legal advice, beneficiary representation, fund custody, payment authority, or Maori authority.

GMUT Mind remains explicit through a formal soft-limit tribunal and a real-data study gap. The canonical GMUT scaffold is a typed scalar-tensor and effective-field-theory research-model family. It is not an established force, unique prediction, likelihood result, empirical confirmation, proof, canon, or Theory of Everything. A synthetic adiabatic-mode scaffold may check perturbative order, wave-number scaling, residual gauge transformations, constraint satisfaction, regularity assumptions, and conserved-variable definitions. It cannot establish that nature implements the model. The late-time integrated Sachs-Wolfe study remains an open gap unless official maps or released spectra, masks, tracer windows, covariance, nuisance assumptions, a baseline, a blind lock, and independent review are actually present.

THOS Body remains explicit through a synthetic independent data-monitoring firewall. The design can distinguish open and closed session materials, role permissions, minimized recommendations, and operational changes that risk reconstructing comparative interim information. It cannot supply participants, an ethics approval, competent monitoring authority, a real matched-budget arm, participant-safety evidence, clinical effectiveness, or independent review. Real THOS confirmation still requires preregistered blind matched-budget real arms, real participants and raters where applicable, participant safeguards, and independent review.

Freed ID is represented structurally through an OpenID Federation trust-chain profile. Synthetic entity configurations, subordinate statements, expiry, authority hints, trust anchors, keys, and metadata-policy operators may be mutation-tested. They do not create a production identity system. Production completion still requires standards-conformant real keys and proofs, live issuance and resolution, live status and revocation where relevant, interoperability, privacy assurance, independent security review, and trust governance. The CBR investment-mandate proposal is an exact gate. Software cannot select asset allocation, risk tolerance, inflation objectives, liquidity, advisers, fees, or loss-allocation rules. Beneficiary privacy, affected-party acceptance, Maori wording, Maori authority, Maori data governance, cultural ratification, competent fiduciary and legal interpretation, and enacted-law status remain with the appropriate people and institutions. Maori concepts remain under Maori authority.

## Ten frozen proposals

V6451-P01 extends Method Flow with child-process start attestation. It assigns zero evidence credit to parser or launcher failures that never begin an evidence-producing child and requires a bounded start and completion receipt before replay credit. V6451-P02 checks long-wavelength adiabatic modes, residual gauge transformations, conserved quantities, and soft-limit assumptions in a typed GMUT scaffold. It rejects inconsistent scaling and unsupported promotion. V6451-P03 preregisters a blind public-data study of the late-time integrated Sachs-Wolfe CMB-galaxy cross-correlation. Because x1 downloads no maps and ingests zero real rows, its expected state is open gap.

V6451-P04 represents a THOS monitoring firewall with synthetic role and message fixtures only. It prevents unblinded comparative information from leaking through sponsor-facing recommendations and preserves matched-budget and participant-safety reservations. V6451-P05 represents an OpenID Federation trust-chain profile with synthetic statements and placeholder keys only. V6451-P06 refuses remedy-fund investment, inflation-risk, liquidity, delegation, and loss-allocation decisions without exact fiduciary, legal, affected-party, beneficiary, and Maori authority.

V6451-P07 addresses a repository boundary absent from the prior 310 proposals: a small Git LFS pointer is not the referenced large object. The intended classifier is read-only and network-free, distinguishes ordinary blobs, canonical and malformed pointers, materialized objects, and missing-content states, and refuses manifest or privacy completeness when content is unavailable. V6451-P08 audits color-only status and frozen contrast tokens while requiring visible text and monochrome redundancy. Passing calculations cannot establish complete accessibility; manual keyboard, zoom, reflow, screen-reader, print, color-perception, and affected-user evaluation remain reserved. V6451-P09 preserves heat-capacity units and constraint variables and rejects conversion of psyche resilience into a thermodynamic response function. V6451-P10 rejects Stage 20 arguments whose apparent support comes only from self-citation or mutually bootstrapped receipts.

The expected disposition slate is exactly six completed, two represented, one open gap, and one exact gate. Completed means only that the bounded artifact and its software acceptance checks are expected to be satisfiable. Represented means a synthetic or proxy structure exists while the real-world claim remains unavailable. Open gap means an evidence object, dataset, reviewer, or environment is absent. Exact gate means only specifically authorized people or institutions can decide the matter. These four labels are not a success ladder and may not be relabeled to improve the distribution.

## Novelty, sources, and Method Flow

Novelty is audited against every frozen identifier and title from v2 through v644-v8. The inherited chain contains thirty-one version groups of ten proposals each. Exact identifiers and normalized titles are unique. A token-overlap screen ranks the nearest prior title for every candidate, but semantic review also compares the mechanism, evidence object, falsifier, rollback, and protected gates. The ten retained mechanisms are absent from the prior chain: child-start evidence credit, cosmological adiabatic soft limits, ISW cross-correlation inputs, DMC recommendation-channel firewalls, federation trust-chain policy processing, remedy-fund investment and loss allocation, Git LFS materialization scope, color-token and monochrome redundancy, heat-capacity nonconversion, and circular-support rejection.

The source ledger is additive. It reuses inherited official sources for Planck cosmology, WCAG 2.2, New Zealand trust administration, Maori trust context, and NIST assurance reasoning. Six new primary or official rows cover adiabatic modes, NASA Planck products, FDA DMC guidance, the final OpenID Federation 1.0 specification, the Git LFS project specification, and IUPAC heat-capacity terminology. Every source remains labeled current, stable, draft, or watch. Source metadata constrains vocabulary and exposes missing evidence. It cannot provide observations, participants, real keys, fund authority, beneficiary consent, Maori authority, legal advice, cultural ratification, complete accessibility, exhaustive security, or an external Stage 20 decision.

Method Flow is append-only. Every timeout, parser or tool assumption fault, blocker, workaround, witness, state transition, recurrence guard, rollback, and sibling recommendation is recorded with bounded scope. The first preferred method serializes mandatory cold-start reads with a sufficient bounded timeout. The second normalizes ripgrep's no-match exit code when absence is a valid discovery result. A preferred method is local evidence for matching preconditions, not a universal truth. If the environment or trigger changes, the recommendation must be revalidated rather than silently reused.

## Environment, validation, privacy, and rotation

D remains the primary work, cache, and validation bank. The inherited baseline exceeds the 15,000-file threshold, but that baseline is not a rotation trigger. The threshold applies only to files newly generated by Tamar, and this packet remains far below it. Existing branches and worktrees stay recoverable. No reset, force push, merge commit, history rewrite, recursive cleanup, sibling mutation, destructive migration, or source replacement is authorized.

Windows Sandbox was audited only through read-only executable and command presence and was unavailable. No elevation, feature enablement, host-security change, or reboot occurred. Codex CLI, desktop packages, Node, npm, Python, and Git were observed only. Official OpenAI release notes were checked without mapping public prose to an unsupported numeric package claim. Neither Codex nor the desktop app was updated.

Hamish's current validation refinement is binding. Eiren Kestrel alone owns the full repository suite. This non-Eiren phase runs tests scoped to recent v641-v660 round-robin evidence and the current v645-v1 packet, then exactly one additional bounded replay in a clean named Tamar validation branch and worktree at the exact final head. Detached-worktree validation is forbidden. The canonical sequential Tamar branch remains authoritative; the named lane is local validation support only. Privacy, JSON parsing, exact manifest parity, exact head, source and seal ancestry, single-parent history, zero merges, clean-before and clean-after state, and final local, upstream, tracking, and live-remote equality remain mandatory.

Repository artifacts and the later baton contain no raw task or thread identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths. Pattern scans are bounded defenses, not exhaustive privacy or security assurance. The static report must carry visible status text, semantic headings, tables, links, printable meaning, and qualified accessibility language. Manual and affected-user evaluation remain reserved even if every structural check passes.

## Terminal boundary

The terminal board begins and, absent extraordinary exact evidence, ends at NOT_READY_FOR_STAGE_20. Empirical GMUT and likelihood claims remain unavailable without real data and review. THOS remains proxy without blind matched-budget real arms and independent review. Freed ID remains nonproduction without real keys, proofs, live lifecycle operations, interoperability, assurance, and governance. CBR investment, legality, legitimacy, beneficiary decisions, Maori wording, Maori authority, data governance, cultural ratification, and enacted-law status remain exact-gated. No deployment, complete accessibility, exhaustive security, proof or canon, empirical confirmation, independent-team reproduction, AGI or ASI, consciousness or personhood, legal ratification, fiduciary decision, or production-readiness claim may be inferred from this packet.

Only after x1 is clean, committed, pushed, and remote-equal may x2 execute. Only after evidence, closeout, seal, exact-final named-lane validation, and final equality all pass may one sanitized activation baton be sent to the existing Sylven Arc task for v645-v2. Until then the route is prepared but unsent, every standby sibling remains untouched, and every negative, gap, and exact gate remains visible.
"""
