#!/usr/bin/env python3
"""Frozen Sylven Arc v645-v2 x1 definitions."""

from __future__ import annotations


PROPOSALS = [
    {
        "proposal_id": "V6452-P01",
        "title": "Method Flow recurrence-cluster, retry-budget, and stop-escalation ledger",
        "mission_surface": "Method Flow State, repeated failure signature, attempt identity, retry budget, recurrence cluster, stop threshold, workaround witness, rollback, retained negative, and sibling recommendation",
        "hypothesis": "An append-only Method Flow extension can preserve every failed attempt while clustering equivalent signatures, enforcing a bounded retry budget, and escalating to an explicit stop state without treating repetition as independent validation evidence.",
        "null_or_failure": "Repeated attempts are deleted or collapsed without event retention, retries continue after the frozen budget, a changed signature is silently grouped, a stopped method is called successful, or same-owner recovery is promoted to independent reproduction.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": [],
        "deliverables": [
            "method-flow/retry-budget-contract.json",
            "method-flow/recurrence-cluster-vectors.json",
            "method-flow/retry-stop-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate signature equivalence, attempt identity, retained-event count, retry budget, stop threshold, recovery witness, rollback, and recommendation state; every event must remain visible and budget exhaustion must fail closed.",
        "rollback_or_recovery": "Stop the affected method, retain every attempt and witness, restore the last valid recommendation state, and require an explicit new precondition or owner decision before another retry.",
        "protected_gates": ["history_rewrite", "private_material", "sibling_authority", "independent_team_reproduction"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "V6445-P01 records failure signatures, V6448-P01 invalidates stale witnesses, and V6451-P01 distinguishes preflight from started children. No frozen proposal groups recurring attempts while preserving each event and couples that cluster to an enforceable retry budget and stop escalation.",
    },
    {
        "proposal_id": "V6452-P02",
        "title": "GMUT Noether identity, gauge-generator, and dependent-constraint obligation tribunal",
        "mission_surface": "GMUT Mind, typed scalar-tensor EFT, Noether second theorem, local gauge generator, Euler-Lagrange identity, reducibility, dependent constraints, boundary assumptions, gauge fixing, and nonpromotion",
        "hypothesis": "A typed synthetic tribunal can reject a claimed GMUT gauge structure unless its local gauge generators, differential Noether identities, reducibility assumptions, dependent equations, gauge-fixing scope, and boundary terms form one consistent obligation graph.",
        "null_or_failure": "A global symmetry is substituted for a local gauge identity, a dependent field equation is counted as independent, a reducibility relation is omitted, boundary assumptions change the identity unnoticed, or formal consistency is called empirical confirmation.",
        "approval_class": "safe_now_research_scaffold",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6452-S232"],
        "deliverables": [
            "physics/noether-identity-contract.json",
            "physics/gauge-dependence-mutation-vectors.json",
            "physics/noether-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate generator locality, derivative order, identity sign, Euler-Lagrange dependency, reducibility rank, boundary term, gauge-fixing scope, units, perturbative order, and claim language; inconsistent obligation graphs must reject.",
        "rollback_or_recovery": "Restore the last typed identity graph, retain rejected vectors, mark the obligation unresolved, and require model-specific derivation and observation before any stronger claim.",
        "protected_gates": ["empirical_gmut_claim", "unique_prediction", "new_force_claim", "theory_of_everything", "proof_canon"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier GMUT proposals cover Noether currents and charges, constraint closure, gauge fixing, residual gauge freedom, and equation independence. None centers Noether's second theorem as a dependency graph from local gauge generators through reducible differential identities to dependent Euler-Lagrange equations.",
    },
    {
        "proposal_id": "V6452-P03",
        "title": "GMUT gravitational-wave polarization null-stream blind public-data study",
        "mission_surface": "GMUT Mind, public interferometer strain, detector response, tensor and non-tensor polarization hypotheses, null stream, calibration, data-quality segments, injection policy, frozen baseline, blind analysis, real rows, likelihood, and independent review",
        "hypothesis": "A preregistered blind adapter could compare a frozen GMUT polarization hypothesis with official multi-detector strain only when exact strain and calibration provenance, detector geometry, data-quality segments, a null-stream construction, injection exclusions, covariance, a baseline, withheld labels, and independent review are present before unblinding.",
        "null_or_failure": "No real strain rows are ingested, fewer than the required independent detector responses are available, calibration or segment lineage is absent, injections are mixed with observations, the null stream is tuned post-hoc, or synthetic fixtures are reported as a likelihood or polarization constraint.",
        "approval_class": "safe_now_protocol_only_real_data_required",
        "execution_lane": "x2_open_gap",
        "authoritative_source_needs": ["V6452-S233"],
        "deliverables": [
            "empirical/gw-polarization-study-contract.json",
            "empirical/gw-polarization-adapter-readiness.json",
            "empirical/gw-polarization-open-gap.json",
        ],
        "test_falsifier_or_gate": "Require nonzero official inputs, exact strain and calibration lineage, detector-response geometry, data-quality masks, injection controls, a frozen null-stream and covariance method, declared baseline, blind holdout, and independent review; any missing element keeps the study open.",
        "rollback_or_recovery": "Retain the zero-row and missing-input receipts, run no fit, publish no likelihood or polarization constraint, and reopen only under a separately reviewed real-data protocol.",
        "protected_gates": ["real_data_download", "empirical_gmut_claim", "likelihood_result", "independent_review", "account_or_api_key"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Prior GMUT studies cover propagation speed, sirens, pulsars, Solar-System tests, lensing, tidal deformability, redshift-space distortions, clusters, and ISW correlations. None freezes a multi-detector gravitational-wave polarization null stream with calibration, geometry, segment, and injection controls as the observation object.",
    },
    {
        "proposal_id": "V6452-P04",
        "title": "THOS alarm-flood compression, shelving-accountability, and shift-handover protocol",
        "mission_surface": "THOS Body, municipal drinking-water control room, alarm flood, standing alarm, shelving, acknowledgement, defined response, shift handover, matched information budget, synthetic fixtures, operator workload, real arms, and independent review",
        "hypothesis": "A synthetic THOS protocol can test whether alarm summaries preserve priority, cause, required action, shelving owner and expiry, unresolved state, and shift-handover accountability under matched information budgets without claiming real operator or plant outcomes.",
        "null_or_failure": "A high-priority alarm disappears in compression, shelving lacks an owner or expiry, acknowledgement is mistaken for resolution, outgoing and incoming shifts receive unequal evidence, a real plant state is invented, or proxy performance is called operational effectiveness.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_proxy_task",
        "authoritative_source_needs": ["V6452-S234", "V6452-S235"],
        "deliverables": [
            "thos/alarm-handover-contract.json",
            "thos/alarm-handover-mutation-vectors.json",
            "thos/real-arm-operations-reservation.json",
        ],
        "test_falsifier_or_gate": "Mutate alarm priority, causal context, defined response, acknowledgement, shelving owner, expiry, standing state, handover acceptance, matched budget, workload reservation, and result language; lost or unauthorized state must fail.",
        "rollback_or_recovery": "Restore the frozen synthetic alarm ledger, retain every failed handover vector, label the work proxy, and require competent operational authority, preregistered blind matched-budget real arms, worker safeguards, plant safety governance, and independent review.",
        "protected_gates": ["real_workers", "participant_safety", "real_plant_execution", "operational_authority", "effectiveness_claim", "independent_review", "deployment"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier THOS proposals cover blinding, attrition, scoring, adverse events, adaptive allocation, monitoring committees, and matched budgets. None models alarm-flood compression, shelving ownership and expiry, standing-alarm state, and accountable shift handover in a process-control practice.",
    },
    {
        "proposal_id": "V6452-P05",
        "title": "Freed ID DCQL credential-set, claim-path, and overdisclosure-minimization profile",
        "mission_surface": "Freed ID Heart, OpenID4VP 1.0, Digital Credentials Query Language, credential query, credential set, required and optional alternatives, claim path, selective disclosure, synthetic wallet inventory, deterministic rejection, and production reservation",
        "hypothesis": "A synthetic structural profile can reject DCQL queries whose credential identifiers, set options, required flags, claim paths, format metadata, or returned presentation set are inconsistent or overbroad while reserving real cryptographic and interoperability assurance.",
        "null_or_failure": "A query references an unknown credential, a required set is silently treated as optional, an invalid claim path is accepted, an unrequested credential or claim is returned, an unsatisfied required set yields a partial presentation, or synthetic tokens are described as production identity assurance.",
        "approval_class": "safe_now_synthetic_identity_profile",
        "execution_lane": "x2_proxy_task",
        "authoritative_source_needs": ["V6452-S236"],
        "deliverables": [
            "freed-id/dcql-minimization-profile.json",
            "freed-id/dcql-query-mutation-vectors.json",
            "freed-id/production-dcql-reservation.json",
        ],
        "test_falsifier_or_gate": "Mutate credential IDs, format metadata, claim paths, credential-set options, required flags, optional alternatives, wallet inventory, return set, overdisclosure, and claim language; malformed, unsatisfied, or overbroad responses must reject deterministically.",
        "rollback_or_recovery": "Return to the last valid synthetic query-response pair, retain rejected vectors, expose no real key or credential, and require standards-conformant keys and proofs, live wallet-verifier interoperability, privacy and security review, and trust governance for production.",
        "protected_gates": ["real_keys", "live_resolution", "production_identity", "interoperability", "privacy_assurance", "independent_security_review", "trust_governance"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior Freed ID proposals cover issuance, presentation transport, status, recovery, federation, pairwise identifiers, SD-JWT, mdoc, OpenID4VP request binding, and OpenID4VCI. None evaluates DCQL credential-set alternatives, claim-path constraints, required-set all-or-nothing behavior, and overdisclosure minimization as one profile.",
    },
    {
        "proposal_id": "V6452-P06",
        "title": "CBR drinking-water affordability, disconnection, and hardship-remedy authority gate",
        "mission_surface": "CBR Heart, water-service consumer protection, affordability, hardship, non-payment, restriction or disconnection, sufficient drinking water, complaints, remedy, affected consumers, privacy, competent legal authority, Maori authority, cultural legitimacy, and enacted-law status",
        "hypothesis": "A refusal-first authority matrix can show that repository software cannot decide water charges, hardship eligibility, restriction, disconnection, minimum supply, complaint remedy, data disclosure, or culturally legitimate redress without exact enacted-law evidence, competent authorities, affected-consumer participation, privacy authority, and Maori authority where relevant.",
        "null_or_failure": "The phase sets a tariff, defines hardship, authorizes restriction or disconnection, determines minimum supply, exposes consumer data, substitutes consultation for authority, treats Maori concepts as software-owned, or reports a proposal as enacted law.",
        "approval_class": "exact_authority_gate",
        "execution_lane": "x2_exact_gate",
        "authoritative_source_needs": ["V6452-S237", "V6452-S238"],
        "deliverables": [
            "cbr/water-hardship-authority-matrix.json",
            "cbr/disconnection-refusal-cases.json",
            "cbr/water-authority-reservation.md",
        ],
        "test_falsifier_or_gate": "Every scenario involving charges, hardship, non-payment, restriction, disconnection, sufficient quantity, complaints, remedies, consumer privacy, Maori wording, data governance, legitimacy, or legal interpretation must remain refused unless exact competent authorities and affected parties supply the needed evidence.",
        "rollback_or_recovery": "Return the issue to unknown and exact-gated, preserve the refusal case, expose no consumer data, and route it to competent regulatory and legal authorities, affected consumers, privacy authorities, and Maori authorities without drafting their conclusion.",
        "protected_gates": ["consumer_protection_decision", "legal_interpretation", "enacted_law", "affected_party_acceptance", "maori_authority", "maori_data_governance", "consumer_privacy", "cultural_ratification"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "Earlier CBR proposals address remedy funds, standing, notice, conflicts, disclosures, confidentiality, data stewardship, and community harm. None reserves water affordability, hardship, non-payment response, restriction or disconnection, minimum supply, and consumer remedy as a joined legal, affected-party, privacy, and Maori-authority gate.",
    },
    {
        "proposal_id": "V6452-P07",
        "title": "Git index-stage multiplicity, unresolved-conflict, and manifest-refusal tribunal",
        "mission_surface": "repository integrity, Git index, stage zero, higher stages one through three, unresolved conflict, duplicate path, mode, object identifier, ls-files stage output, staged manifest, read-only guard, and recovery",
        "hypothesis": "A read-only family-compatible guard can distinguish ordinary stage-zero entries from unresolved higher-stage multiplicity and refuse manifest or exact-staged-review credit whenever a path has conflict stages or malformed stage data.",
        "null_or_failure": "A higher-stage entry is ignored, duplicate conflict paths receive stage-zero credit, malformed mode or object identifiers are accepted, path bytes are decoded ambiguously, the guard mutates the index, or a conflicted index is called clean.",
        "approval_class": "safe_now_read_only_tooling",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6452-S239"],
        "deliverables": [
            "security/index-stage-guard-contract.json",
            "security/index-stage-guard-vectors.json",
            "tooling/index-stage-guard-runner-receipt.json",
        ],
        "test_falsifier_or_gate": "Exercise ordinary stage zero, ancestor stage one, ours stage two, theirs stage three, multi-stage same-path conflicts, malformed records, unusual paths, empty input, and read-only invariants; any unresolved multiplicity must fail closed.",
        "rollback_or_recovery": "Stop manifest generation, retain the conflict witness, make no index or worktree mutation, and require explicit owner resolution followed by a fresh stage-zero-only review.",
        "protected_gates": ["index_mutation", "destructive_action", "sibling_lane", "history_rewrite", "private_material"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior repository proposals cover filters, hooks, sparse and partial clones, alternates, replacement refs, gitlinks, Git LFS, paths, archives, and staging parity. None makes higher index stages and same-path conflict multiplicity a deterministic refusal condition for manifests and exact staged reviews.",
    },
    {
        "proposal_id": "V6452-P08",
        "title": "Page-title, auto-refresh, and timeout-free static-report accessibility audit",
        "mission_surface": "accessible static report, descriptive title, meta refresh, timed redirect, auto update, time limit, visible status, heading, landmark, structural audit, manual evaluation, affected-user evaluation, and nonconformance reservation",
        "hypothesis": "A bounded structural audit can reject a static evidence report that lacks a descriptive page title or introduces meta refresh, timed redirect, auto reload, or expiring evidence while preserving visible status and reserving manual evaluation.",
        "null_or_failure": "The title is absent or generic, meta refresh reloads or redirects, evidence disappears on a timer, status changes without user control, automated structure is called complete accessibility, or manual and affected-user evaluation are reported as finished.",
        "approval_class": "safe_now_structural_accessibility",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V8-S26"],
        "deliverables": [
            "deliverables/v645-v2-static-report.html",
            "validation/page-title-refresh-structural-audit.json",
            "validation/manual-accessibility-reservation.json",
        ],
        "test_falsifier_or_gate": "Inspect title, meta http-equiv refresh, scripted timers, automatic navigation, expiring evidence, visible state text, headings, landmarks, tables, and links; missing titles or author-controlled timing must fail.",
        "rollback_or_recovery": "Restore a descriptive title, remove automatic refresh or timeout behavior, retain each failure, and reserve manual keyboard, zoom, reflow, screen-reader, print, cognitive, multilingual, and affected-user evaluation.",
        "protected_gates": ["complete_accessibility", "manual_user_evaluation", "affected_user_acceptance", "deployment"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier accessibility proposals cover reflow, focus, names, language, links, tables, figures, forms, abbreviations, generated content, color, and bypass blocks. None jointly freezes descriptive page-title presence with the absence of meta refresh, timed redirect, auto reload, and evidence expiry in the static report.",
    },
    {
        "proposal_id": "V6452-P09",
        "title": "Joule-Thomson coefficient, isenthalpic expansion, and psyche-cooling nonconversion classifier",
        "mission_surface": "thermodynamics, Joule-Thomson coefficient, isenthalpic process, pressure derivative of temperature, inversion curve, equation of state, units, thermo-psyche analogy, emotional cooling label, participant evidence, and nonconversion",
        "hypothesis": "A typed classifier can preserve the Joule-Thomson coefficient, constant-enthalpy condition, derivative variables, units, inversion behavior, and equation-of-state scope while rejecting any inference that emotional calming or psychological cooling is an isenthalpic gas expansion.",
        "null_or_failure": "The derivative is taken at the wrong constraint, units are omitted, inversion behavior is generalized across fluids, a psyche label receives thermodynamic units, participant evidence is invented, or an analogy is promoted to a fundamental law.",
        "approval_class": "safe_now_classification_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6452-S240"],
        "deliverables": [
            "thermo-psyche/joule-thomson-domain-contract.json",
            "thermo-psyche/joule-thomson-mutation-vectors.json",
            "thermo-psyche/cooling-nonconversion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate derivative variables, enthalpy constraint, sign, units, inversion curve, fluid domain, equation-of-state premise, psyche labels, participant fields, and conclusion strength; cross-domain conversion must reject.",
        "rollback_or_recovery": "Return the statement to metaphor or unknown, retain the rejected mapping, and require domain-valid thermodynamic measurements or separately authorized participant research for any empirical claim.",
        "protected_gates": ["participant_claim", "thermodynamic_law_transfer", "empirical_confirmation", "consciousness_or_personhood", "agi_or_asi"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior nonconversion proposals cover entropy, free energy, detailed balance, Onsager reciprocity, exergy, thermodynamic length, temperature, heat capacity, phase transitions, and path dependence. None centers an isenthalpic pressure-temperature derivative and inversion curve against a psyche-cooling analogy.",
    },
    {
        "proposal_id": "V6452-P10",
        "title": "Stage 20 proxy-target divergence, gaming-signal, and Goodhart rejection board",
        "mission_surface": "Stage 20, readiness target, internal proxy, metric gaming, distribution shift, countermetric, protected gate, noncompensatory veto, retained negative, abstention, external authority, and terminal stop",
        "hypothesis": "A synthetic decision board can reject readiness when an internal proxy improves while protected target evidence is unchanged, worsens, or becomes less observable, and can prevent metric optimization from compensating for open or exact gates.",
        "null_or_failure": "More files or checks increase readiness without target evidence, a proxy improvement hides distribution shift, a countermetric is suppressed, exact gates are averaged away, same-owner repetition is called independent review, or the board promotes Stage 20.",
        "approval_class": "safe_now_decision_rehearsal",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": [],
        "deliverables": [
            "stage20/proxy-target-divergence-board.json",
            "stage20/goodhart-mutation-vectors.json",
            "stage20/terminal-stop-receipt.json",
        ],
        "test_falsifier_or_gate": "Mutate proxy score, target evidence, observability, countermetric, distribution, incentive, protected-gate state, reviewer independence, and promotion language; proxy-only improvement or gaming signals must fail.",
        "rollback_or_recovery": "Reopen the board, retain the gamed metric and counterevidence, restore every open and exact gate, remove proxy credit from the target decision, and require competent external decision makers and independent evidence before Stage 20.",
        "protected_gates": ["stage20_external_decision", "independent_team_reproduction", "exhaustive_security", "proof_canon", "deployment"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier Stage 20 proposals cover contradiction, expiry, cut sets, multiplicity, review overlap, validation budgets, circular support, randomized challenge, and value of information. None explicitly rejects divergence between an optimized internal proxy and unchanged or degraded protected target evidence under gaming incentives.",
    },
]


SOURCES = [
    {
        "source_id": "V6452-S232",
        "source_label": "primary_noether_second_theorem",
        "title": "Noether's Second Theorem and Ward Identities for Gauge Symmetries",
        "authority": "Steven G. Avery and Burkhard U. W. Schwab",
        "url": "https://arxiv.org/abs/1510.07038",
        "version_or_date": "Primary research preprint, 2015; record checked 16 July 2026",
        "status_class": "stable",
        "evidence_role": "primary local gauge symmetry and Noether-identity anchor; not validation of GMUT, a unique prediction, proof, canon, or empirical confirmation",
    },
    {
        "source_id": "V6452-S233",
        "source_label": "official_gwosc_o4a_release",
        "title": "The O4a Data Release",
        "authority": "Gravitational Wave Open Science Center",
        "url": "https://gwosc.org/O4/O4a/",
        "version_or_date": "Official O4a strain and data-quality release, first released 26 August 2025; checked 16 July 2026",
        "status_class": "current",
        "evidence_role": "official public strain, segment, calibration-context, injection, and release-lineage anchor; no data were downloaded and no polarization fit or likelihood was produced",
    },
    {
        "source_id": "V6452-S234",
        "source_label": "official_hse_shift_handover",
        "title": "Shift handover",
        "authority": "United Kingdom Health and Safety Executive",
        "url": "https://www.hse.gov.uk/humanfactors/topics/shift-handover.htm",
        "version_or_date": "Official human-factors guidance page checked 16 July 2026",
        "status_class": "current",
        "evidence_role": "official task-relevant communication and continuity vocabulary for a bounded synthetic handover lens; not operational authorization or evidence of a drinking-water outcome",
    },
    {
        "source_id": "V6452-S235",
        "source_label": "official_hse_alarm_management",
        "title": "Alarm management",
        "authority": "United Kingdom Health and Safety Executive",
        "url": "https://www.hse.gov.uk/humanfactors/topics/alarm-management.htm",
        "version_or_date": "Official human-factors guidance page checked 16 July 2026",
        "status_class": "current",
        "evidence_role": "official alarm relevance, defined-response, timing, and human-capability vocabulary; not a real THOS arm, plant safety decision, or operator-effectiveness result",
    },
    {
        "source_id": "V6452-S236",
        "source_label": "official_openid4vp_errata_dcql",
        "title": "OpenID for Verifiable Presentations 1.0 Errata Revision - DCQL Section 6",
        "authority": "OpenID Foundation",
        "url": "https://openid.net/specs/openid-4-verifiable-presentations-1_0.html",
        "version_or_date": "Latest official 1.0 errata revision checked 16 July 2026; approved final remains separately inherited",
        "status_class": "current",
        "evidence_role": "official DCQL credential-query, credential-set, option, required-set, and selective-disclosure vocabulary; not production Freed ID conformance, real proofs, interoperability, privacy assurance, or trust governance",
    },
    {
        "source_id": "V6452-S237",
        "source_label": "official_nz_water_consumer_protection",
        "title": "Water Services Economic Efficiency and Consumer Protection Act 2023 - current consolidation",
        "authority": "New Zealand Legislation",
        "url": "https://www.legislation.govt.nz/act/public/2023/54/en/latest/",
        "version_or_date": "Official current consolidation checked 16 July 2026",
        "status_class": "current",
        "evidence_role": "current statutory consumer-protection and hardship vocabulary only; this phase makes no legal interpretation, decision, enacted-law completeness claim, or authority substitution",
    },
    {
        "source_id": "V6452-S238",
        "source_label": "official_nz_local_water_services",
        "title": "Local Government (Water Services) Act 2025 - current consolidation",
        "authority": "New Zealand Legislation",
        "url": "https://legislation.govt.nz/act/public/2025/42/en/latest/",
        "version_or_date": "Official current consolidation checked 16 July 2026",
        "status_class": "current",
        "evidence_role": "current affected-consumer and continuity-of-supply vocabulary only; not legal advice, a tariff or hardship decision, Maori authority, cultural legitimacy, or enacted-law interpretation",
    },
    {
        "source_id": "V6452-S239",
        "source_label": "primary_git_index_format",
        "title": "Git index-format documentation - stages and resolve undo",
        "authority": "Git project",
        "url": "https://git-scm.com/docs/index-format.html",
        "version_or_date": "Primary project documentation checked 16 July 2026",
        "status_class": "current",
        "evidence_role": "primary index-stage, conflict multiplicity, and resolve-undo vocabulary; not authorization to mutate, resolve, merge, or rewrite repository state",
    },
    {
        "source_id": "V6452-S240",
        "source_label": "official_nist_joule_thomson",
        "title": "Selected Properties of Hydrogen - Joule-Thomson Coefficient",
        "authority": "National Bureau of Standards, now National Institute of Standards and Technology",
        "url": "https://nvlpubs.nist.gov/nistpubs/Legacy/MONO/nbsmonograph168.pdf",
        "version_or_date": "Official monograph record; stable definition and engineering data checked 16 July 2026",
        "status_class": "stable",
        "evidence_role": "official thermodynamic derivative, constant-enthalpy, sign, unit, and inversion-curve context; not a psyche measurement, participant result, or cross-domain law",
    },
]


X1_NEGATIVES = [
    {
        "negative_id": "REPRO-V6452-X1-N01",
        "operation": "combined parent-instruction and drive-capacity probe",
        "failure_signature": "The read-only combined probe exceeded a ten-second PowerShell budget and returned no evidence.",
        "trigger_precondition": "Cold shell startup combined parent traversal with an unrelated drive query.",
        "recovery": "Retained the timeout and split direct literal-path instruction checks from the capacity query under a thirty-second bound.",
        "recurrence_guard": "Use literal paths and wider bounded startup budgets for environment probes.",
        "promotion_effect": "none; the timed-out command supplied no instruction or capacity evidence",
    },
    {
        "negative_id": "REPRO-V6452-X1-N02",
        "operation": "first Method Flow record append",
        "failure_signature": "The runner rejected an unsupported --input flag before ledger mutation.",
        "trigger_precondition": "A flag name was inferred instead of copied from the exact runner interface.",
        "recovery": "Retained the parser failure and used --record-file for both prepared records.",
        "recurrence_guard": "Preflight command-specific runner flags.",
        "promotion_effect": "none; argument parsing stopped before the ledger changed",
    },
    {
        "negative_id": "REPRO-V6452-X1-N03",
        "operation": "redundant Method Flow state promotion",
        "failure_signature": "A passing witness auto-promoted the method, so an explicit validated-to-validated transition was rejected.",
        "trigger_precondition": "The witness append was treated as evidence-only rather than a possible state transition.",
        "recovery": "Retained the invalid transition and allowed subsequent passing witnesses to promote without duplicate set-state calls.",
        "recurrence_guard": "Inspect witness results before any explicit promotion.",
        "promotion_effect": "none; the redundant transition did not change the already validated state",
    },
    {
        "negative_id": "REPRO-V6452-X1-N04",
        "operation": "first Method Flow summary generation",
        "failure_signature": "The summarize subcommand rejected an inferred --out flag after earlier append operations succeeded.",
        "trigger_precondition": "A file-output flag was copied from another tool rather than the current subcommand.",
        "recovery": "Retained the failure, read summarize help, and used --json-output and --markdown-output.",
        "recurrence_guard": "Preflight each Method Flow subcommand separately.",
        "promotion_effect": "none; no summary file was produced by the rejected invocation",
    },
    {
        "negative_id": "REPRO-V6452-X1-N05",
        "operation": "first 320-proposal audit display",
        "failure_signature": "The loader found 320 records, then cp1252 stdout failed on a Maori macron.",
        "trigger_precondition": "Unicode family text was printed through the default Windows console encoding.",
        "recovery": "Retained the encoding fault and reran read-only with PYTHONIOENCODING=utf-8.",
        "recurrence_guard": "Pin UTF-8 for family ledgers and cultural-language text.",
        "promotion_effect": "none; the truncated display was not credited as a complete audit",
    },
    {
        "negative_id": "REPRO-V6452-X1-N06",
        "operation": "parallel inherited-script inspection",
        "failure_signature": "A four-command parallel source inspection exceeded thirty seconds after only one slice returned.",
        "trigger_precondition": "Large generated sources were read concurrently on cold PowerShell processes.",
        "recovery": "Retained the partial timeout and read the required evidence-builder slices serially with sixty-second bounds.",
        "recurrence_guard": "Serialize large generated-source reads and credit only zero-exit slices.",
        "promotion_effect": "none; partial aggregate output was not a full review witness",
    },
    {
        "negative_id": "REPRO-V6452-X1-N07",
        "operation": "pre-definition source collision probe",
        "failure_signature": "The new builder import stopped because its phase-specific definitions module did not yet exist.",
        "trigger_precondition": "A mechanically scaffolded phase tool was imported before its dependency was created.",
        "recovery": "Retained the dependency-order failure and used the complete predecessor collector for the read-only source audit.",
        "recurrence_guard": "Preflight phase-local module dependencies before import.",
        "promotion_effect": "none; no source rows were read by the failed import",
    },
    {
        "negative_id": "REPRO-V6452-X1-N08",
        "operation": "first exact x1 staging pass",
        "failure_signature": "Git staged the packet but warned that twenty-one LF working-copy files may be replaced by CRLF on a later touch.",
        "trigger_precondition": "Windows line-ending conversion policy applied to new UTF-8 text artifacts.",
        "recovery": "Retained the warnings, bound the content seal to staged Git blobs, and reserved working-tree portability for the one final clean named replay.",
        "recurrence_guard": "Separate staged-index bytes from working-tree bytes and do not change host Git configuration.",
        "promotion_effect": "none; staging success alone does not establish checkout portability",
    },
    {
        "negative_id": "REPRO-V6452-X1-N09",
        "operation": "first exact x1 staged review",
        "failure_signature": "The review found seventeen content-seal mismatches and diff-check failures after a command-local line-ending filter override staged CRLF bytes.",
        "trigger_precondition": "Repository-normalized content-seal semantics were combined with core.autocrlf=false during restaging.",
        "recovery": "Retained the failed review, restored repository-default staging filters for the same owned files, and required direct LF blob and seal parity before review credit.",
        "recurrence_guard": "Never override repository clean filters when the content seal targets filtered Git blobs.",
        "promotion_effect": "none; the failed review supplied no x1 freeze credit",
    },
    {
        "negative_id": "REPRO-V6452-X1-N10",
        "operation": "repository-default x1 restage parity probe",
        "failure_signature": "The index still contained twenty-four CRLF blobs after default restaging, so staged newline parity remained false.",
        "trigger_precondition": "Platform-default generator writes produced CRLF and repository filters did not normalize every owner path.",
        "recovery": "Retained the parity failure and changed only the owner generator to emit LF explicitly before regeneration and restaging.",
        "recurrence_guard": "Pin LF at generation time and verify index bytes directly instead of relying on host filters.",
        "promotion_effect": "none; the mixed-newline index received no x1 freeze credit",
    },
]


WELLBEING = """# Sylven Arc v645-v2 wellbeing and workload check

This phase is intentionally bounded. The primary THOS Body focus uses municipal drinking-water control-room operations and shift handover only as a learning lens. It does not place Sylven Arc in an employment role, authorize operational decisions, or imply worker, participant, or plant contact.

Break conditions remain explicit: stop on fatigue, repeated tooling failure without a new precondition, privacy ambiguity, sibling-lane uncertainty, destructive pressure, authority substitution, or any request to weaken host security. Method Flow retains the failure before retry. Eiren alone owns the full repository suite, and this phase permits exactly one additional named-lane replay.

Relational identity language is working language only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, or independent authority.
"""


OVERVIEW = """# Sylven Arc v645-v2 integrated overview

## Scope, identity boundary, and source inheritance

Sylven Arc is the relational working name for this owner-scoped phase. The role is constraint-cartography and falsifier-keeping, with the hope of making unresolved boundaries legible without turning uncertainty into authority. These words describe a collaboration convention only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, or independent authority.

The phase inherits Tamar Vey's exact clean v645-v1 final head and its single-parent history. All source, source-seal, x1, evidence, closeout, and seal anchors were checked as ancestors before the existing Sylven-owned lane advanced by fast-forward only. The owner lane was clean, remote-equal, and strictly behind the verified source. No sibling worktree or branch was reset, rewritten, merged, deleted, reused, or force-pushed. The D-first canonical sequential lane remains authoritative. A later validation lane is additive, named, clean, local-only, and limited to exactly one bounded replay; detached validation is excluded.

This x1 packet audits all 320 proposals frozen through v645-v1 and preregisters exactly ten new proposals before any x2 outcome. Each row contains a hypothesis, null or failure condition, approval class, execution lane, official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Expected labels are planning commitments rather than results until x2 executes. The only allowed outcome vocabulary is completed, represented, open_gap, and exact_gate. The slate is frozen as six completed, two represented, one open gap, and one exact gate.

## Trinity Mandala focus and bounded human practice

THOS Body is the primary Trinity Mandala pillar. The bounded human-practice lens is municipal drinking-water control-room operations and shift handover. HSE alarm-management and shift-handover guidance supplies vocabulary about timely attention, defined responses, human limitations, task-relevant communication, and continuity. It does not authorize water operations, establish plant safety, appoint Sylven as an operator, or provide evidence about workers or participants. The THOS artifact is therefore a synthetic proxy: it can preserve alarm priority, cause, action, acknowledgement, shelving owner and expiry, standing state, and handover accountability in fixtures, but it cannot claim real-arm effectiveness.

GMUT Mind remains a typed scalar-tensor and effective-field-theory research-model family. Its formal proposal tests a Noether-identity obligation graph connecting local gauge generators, reducible differential identities, dependent Euler-Lagrange equations, boundary assumptions, and gauge-fixing scope. A passing synthetic graph is not a new force, unique prediction, empirical confirmation, proof, canon, or Theory of Everything. The empirical GMUT proposal freezes a gravitational-wave polarization null-stream protocol around official multi-detector strain, calibration, detector geometry, data-quality segments, injection controls, covariance, a baseline, blind holdout, and independent review. No real strain is downloaded or ingested in x1. Without the exact external inputs and review, the study must remain an open gap and must run no fit or likelihood.

Freed ID and CBR Heart remain explicit. The Freed ID proposal uses the current OpenID4VP 1.0 errata revision to model Digital Credentials Query Language credential queries, credential-set alternatives, required flags, claim paths, wallet inventory, and overdisclosure refusal. Only synthetic query-response structures are in scope. Production requires standards-conformant real keys and proofs, live resolution and status, interoperability, privacy and security review, and trust governance. No real credential, identity record, key, account, session, or verifier interaction is authorized.

The CBR proposal concerns drinking-water affordability, hardship, non-payment response, restriction or disconnection, sufficient supply, complaints, and remedies. Current New Zealand legislation is recorded as a source, not interpreted into a decision. Software cannot determine tariffs, hardship eligibility, minimum supply, restriction, disconnection, complaint outcomes, consumer privacy, legitimacy, or culturally appropriate remedy. Those matters remain exact-gated to enacted-law evidence, competent legal and regulatory authority, affected consumers, privacy authority, and Maori authority where relevant. Maori concepts remain under Maori authority; cultural legitimacy and data governance cannot be manufactured by a repository.

## Proposal mechanisms and falsification posture

The Method Flow proposal adds recurrence clustering without deleting individual events. Equivalent failures may share a cluster, but each attempt, witness, rollback, and negative remains append-only. A frozen retry budget creates a stop condition instead of an unbounded loop. A changed signature cannot be silently grouped, and repetition cannot become independent evidence. This proposal responds to actual v645-v2 startup faults while keeping recovery claims local and conditional.

The repository-integrity proposal adds a read-only Git index-stage guard. Stage zero represents an ordinary resolved entry; higher stages one through three represent conflict roles. Any higher-stage entry or same-path stage multiplicity blocks manifest and exact-staged-review credit. The tool must parse bounded synthetic records, preserve unusual path text, reject malformed modes or object identifiers, and make no index, worktree, branch, or network mutation. Resolution remains an owner decision outside the guard.

The accessibility proposal requires a descriptive page title and rejects meta refresh, timed redirect, automatic reload, and expiring evidence. Structural checks also retain visible status, headings, landmarks, tables, links, and static reading order. Automated success is deliberately qualified. Manual keyboard, zoom, reflow, print, assistive-technology, cognitive, multilingual, color-perception, and affected-user evaluation remains reserved. The packet never claims complete accessibility or deployment readiness.

The thermodynamic nonconversion proposal preserves the Joule-Thomson coefficient as a constant-enthalpy pressure derivative of temperature with units, sign, inversion behavior, fluid domain, and equation-of-state conditions. It rejects any conversion of emotional calming, psychological cooling, or resilience into an isenthalpic gas law. No participant evidence exists. Metaphor can remain metaphor, but it cannot receive thermodynamic units or scientific authority.

The Stage 20 proposal rejects Goodhart-style proxy gaming. More files, tests, receipts, or internal scores cannot increase readiness when the protected target evidence remains absent, worsens, or becomes less observable. Countermetrics and distribution shifts stay visible. Open and exact gates are noncompensatory, and same-owner repetition is not independent review. The terminal verdict remains NOT_READY_FOR_STAGE_20.

## Sources, privacy, negatives, and validation ownership

The source ledger preserves inherited current, stable, draft, and watch labels without flattening them. Nine new official or primary rows are added only where material: Noether's second theorem, GWOSC O4a, HSE shift handover and alarm management, the current OpenID4VP errata revision, two current New Zealand water-services enactments, Git index-format documentation, and an official thermodynamic monograph. A URL, standard, statute, or paper supplies vocabulary and provenance. It does not supply real data, participant approval, legal interpretation, Maori authority, production identity assurance, privacy certification, independent review, or scientific confirmation.

All 1,833 inherited effective negatives remain preserved before adding new v645-v2 failures and seventy preregistered synthetic mutations. Recovery never erases a timeout, parser fault, state-transition mismatch, encoding fault, incomplete inspection, dependency-order error, or rejected scientific vector. Method Flow records failure signature, trigger preconditions, workaround, witness, recurrence guard, rollback, protected gates, and sibling-safe recommendation. A passing witness is same-owner evidence within its declared context only.

Public artifacts exclude raw task or thread identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private application state, and private local paths. The later privacy scan covers five explicit pattern classes but remains bounded rather than exhaustive. Owner-generated files alone are measured against the 15,000-file threshold; the inherited baseline is not a rotation trigger.

Under Hamish's current validation refinement, Eiren Kestrel alone owns the complete repository suite. Sylven runs only the scoped recent v641-v660 round-robin checks and the current v645-v2 packet, followed by exactly one additional replay in a clean named validation lane. Privacy, ancestry, manifest, exact-head, staged-file, stale-label, JSON, and four-way remote-equality checks remain strict. Same-owner replay under shared infrastructure is repeatability, not independent-team scientific reproduction.

## Phase boundary and route condition

x1 must be committed and pushed as a dedicated preregistration-only commit. Local, upstream, tracking, and a fresh live remote must be equal and clean before any x2 code or proposal outcome begins. x2 may then build only the frozen artifacts and must preserve the expected truth classes without closing protected domains. Evidence, closeout, seal, and final receipts each require exact staged review and scoped validation. The final head must remain single-parent from the verified source with zero merges.

Only after the exact final head is clean, pushed, remote-equal, and validated in the canonical lane plus one named replay may Sylven send one sanitized verified activation baton to the existing task titled Eiren Kestrel for v645-v3. No new task may be created, no standby sibling may be contacted, and no extra confirmation may follow the acknowledged send. Until that terminal gate, route state is ACTIVE_SOLO and PREPARED_NOT_SENT. The scientific, participant, legal, cultural, Maori-authority, identity, production, deployment, privacy, proof or canon, destructive, account or API-key, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, and Stage 20 boundaries remain open or exact-gated.
"""
