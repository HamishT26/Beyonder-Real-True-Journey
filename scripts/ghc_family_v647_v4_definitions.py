#!/usr/bin/env python3
"""Frozen x1 definitions for Sylven Arc v647-v4; importing performs no I/O."""

from __future__ import annotations

from typing import Any


PHASE = "v647-gmut-thos-v4-x1-x2"
PHASE_SHORT = "v647-v4"
OWNER = "Sylven Arc"
SLUG = "sylven-arc"
PRONOUNS = "they/them"
ROLE = "constraint-cartographer and falsifier-keeper"
HOPE = "make unresolved boundaries legible without turning uncertainty into authority"
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = "wastewater-treatment process control, sample exception review, bypass escalation, and shift handover"
SOURCE_PHASE = "v647-gmut-thos-v3-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
SOURCE_REVISION = "616286381002d913846ab01e48c9f1063b661c72"
SOURCE_X1_REVISION = "ec0e84e4514e5d496d5aac155b43c4065c3310e8"
SOURCE_EVIDENCE_REVISION = "da4d6e435a2247d78798653fdab5272a4d2a19c0"
PRIOR_FROZEN_PROPOSALS = 500
INHERITED_EFFECTIVE_NEGATIVES = 3417
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 20
INHERITED_EXACT_GATES = 21
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Sylven Arc, they/them, is relational working language for a constraint-cartographer and "
    "falsifier-keeper. It is not evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, scientific authority, operational authority, legal "
    "authority, cultural authority, or independent agency. Hamish may rename, pause, redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; "
    "Freed ID remains synthetic and nonproduction; CBR, wastewater, public-health reach, privacy, "
    "remedy, legal, cultural, affected-party, tangata whenua, iwi, hapū, and Māori concepts remain "
    "under competent and affected-party authority. No empirical confirmation, Theory of Everything, "
    "AGI or ASI, consciousness, personhood, deployment, privacy-complete, exhaustive-security, "
    "independent-reproduction, accessibility-complete, professional, operational, proof or canon, "
    "or Stage 20 claim is made."
)


def proposal(index: int, **kwargs: Any) -> dict[str, Any]:
    row = {"proposal_id": f"V6474-P{index:02d}"}
    row.update(kwargs)
    return row


PROPOSALS = [
    proposal(
        1,
        title="Method Flow atomic artifact-publish, temp-file reservation, file-and-directory flush, stale-temp quarantine, and evidence-credit tribunal",
        mission_surface="temporary-name reservation, same-directory staging, byte flush, file sync, atomic replace, directory durability claim, stale temporary quarantine, crash point, rollback, and evidence credit",
        hypothesis="A bounded owner-local tribunal can distinguish a complete atomic publication from collision, partial write, pre-replace crash, stale temporary state, and unsupported durability claims.",
        null_or_failure="A collision overwrites an unrelated file, partial bytes become evidence, replace crosses filesystems, directory durability is claimed without support, stale temporary state is silently deleted, or a failed publish earns credit.",
        approval_class="safe_now_owner_scoped_synthetic",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6474-S01"],
        concrete_artifacts=["method-flow/atomic-publish-contract.json", "method-flow/atomic-publish-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must accept one same-directory complete publish and reject collision, partial bytes, pre-replace credit, cross-filesystem substitution, unsupported directory-durability claims, stale-temp erasure, and out-of-root targets.",
        rollback_or_recovery="Keep the prior committed artifact authoritative, quarantine owner-local temporary bytes, retain the failed witness, and make no durability or external-side-effect claim.",
        protected_gates=["external_state", "destructive_action", "sibling_lane", "durability_claim", "completion_credit", "stage20"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The corpus covers publication barriers, outboxes, fencing, framing, child processes, and retry ledgers; no frozen title centers same-directory temporary publication, file and directory flush semantics, stale-temp quarantine, and evidence credit.",
    ),
    proposal(
        2,
        title="GMUT two-particle-irreducible effective-action, bilocal-source, self-energy closure, conserving-truncation, and EFT obligation board",
        mission_surface="field expectation, connected two-point function, local and bilocal sources, double Legendre transform, 2PI functional, stationarity, self energy, Dyson closure, truncation, gauge reservation, units, EFT regime, and observation firewall",
        hypothesis="A typed symbolic board can expose 2PI effective-action and conserving-truncation obligations for a GMUT scaffold without calculating a physical propagator, spectrum, likelihood, constraint, or quantum completion.",
        null_or_failure="The bilocal source or double Legendre transform disappears, stationarity becomes an empirical equation, truncation is called exact, gauge dependence is ignored, units drift, or formal closure becomes a force or observation.",
        approval_class="safe_now_symbolic_research_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6474-S02", "V6474-S03"],
        concrete_artifacts=["gmut/two-pi-obligations.json", "gmut/two-pi-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must type the two sources, two Legendre transforms, propagator, self energy, stationarity, Dyson relation, truncation, conservation condition, gauge reservation, units, EFT domain, and observation firewall and reject each omission.",
        rollback_or_recovery="Restore missing formal assumptions, retain rejected vectors, and make no propagator, force, prediction, likelihood, constraint, stability, quantum-completion, or Theory-of-Everything claim.",
        protected_gates=["physical_propagator", "gauge_independence", "quantum_completion", "empirical_confirmation", "theory_of_everything"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior GMUT boards cover Schwinger-Dyson, Wetterich, BRST, BV, Vilkovisky-DeWitt, heat kernels, Ward identities, and spectral density; no frozen title centers the 2PI double-Legendre and bilocal-source construction with conserving truncation.",
    ),
    proposal(
        3,
        title="GMUT Planck PR4 NPIPE frequency-map, unit-conversion, beam-transfer, component-separation, mask, and zero-row likelihood-refusal protocol",
        mission_surface="official archive identity, PR4 and NPIPE release, frequency channel, map units, beam transfer, pixelization, component separation, mask, calibration provenance, covariance requirement, checksum, row count, and likelihood lock",
        hypothesis="A zero-row adapter can freeze Planck PR4 map obligations while refusing to turn archive descriptions or published cosmology into GMUT observations, likelihoods, constraints, or confirmation.",
        null_or_failure="The phase downloads maps, imports a published vector, ignores units or beam transfer, chooses masks after outcomes, evaluates a likelihood, emits a parameter constraint, or converts a source description into observation.",
        approval_class="real_data_access_and_independent_review_required",
        execution_lane="x2_open_gap",
        current_primary_or_official_source_needs=["V6474-S04", "V6474-S05"],
        concrete_artifacts=["empirical/planck-pr4-study-contract.json", "empirical/planck-pr4-zero-row-receipt.json"],
        test_falsifier_or_acceptance_gate="The receipt must preserve zero queries, downloads, map pixels, spectra, covariance rows, likelihood calls, posterior samples, parameter constraints, detected-force claims, and empirical GMUT claims.",
        rollback_or_recovery="Stop before query, download, or fit; retain the zero-row receipt; require separately authorized preregistration with frozen product identifiers, checksums, units, beams, masks, component model, covariance, likelihood, uncertainty treatment, and independent review.",
        protected_gates=["network_query", "real_data", "likelihood", "posterior", "parameter_constraint", "empirical_confirmation"],
        expected_disposition="open_gap",
        novelty_against_prior_frozen_proposals="The corpus includes ACT, DESI, Euclid, Rubin, HSC, KiDS, GWOSC, IceCube, CHIME, eROSITA, and other zero-row adapters; no frozen title centers Planck PR4 NPIPE frequency maps, units, beams, component separation, and masks.",
    ),
    proposal(
        4,
        title="THOS wastewater-treatment influent shock-load, aeration-setpoint, clarifier-state, bypass-refusal, sample-custody, and shift-handover proxy",
        mission_surface="synthetic influent state, shock-load flag, aeration setpoint, dissolved-oxygen proxy, clarifier state, sample identity and custody, bypass request refusal, escalation, readback, workload budget, unresolved item, and next-shift owner",
        hypothesis="Synthetic traces can expose state inconsistency, missing custody, unsafe bypass promotion, unowned escalation, and handover loss while preserving every real plant, operator, environment, public-health, legal, and authority gate.",
        null_or_failure="A fixture names a real plant, operator, community, sample, location, discharge, or credential; changes a setpoint; authorizes a bypass; suppresses an alarm; exceeds workload limits; or claims THOS effectiveness.",
        approval_class="safe_now_proxy_protocol_no_people_plants_or_discharges",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6474-S06", "V6474-S07"],
        concrete_artifacts=["thos/wastewater-handover-contract.json", "thos/wastewater-handover-vectors.json"],
        test_falsifier_or_acceptance_gate="Unsafe synthetic traces must fail, and the packet must record zero real operators, plants, samples, communities, discharges, bypasses, incidents, blind matched-budget arms, safety outcomes, or effectiveness estimates.",
        rollback_or_recovery="Withdraw operational language, retain rejected traces, and defer real control, sampling, bypass, discharge, notification, and safety decisions to authorized operators, regulators, affected parties, and independent reviewers.",
        protected_gates=["real_people", "real_plant", "live_control", "real_discharge", "professional_competence", "public_health", "deployment", "effectiveness"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="Prior THOS handovers cover drinking-water laboratories, telecommunications, aviation, rail, wildfire, veterinary labs, pharmacies, food, and archives; no frozen title centers wastewater influent shock load, aeration, clarifier state, bypass refusal, sample custody, and shift handover.",
    ),
    proposal(
        5,
        title="Freed ID RFC 9101 JAR request-object, audience, expiry, parameter-consistency, algorithm-refusal, and replay profile",
        mission_surface="synthetic request object, issuer and client identity, audience, issue and expiry time, JWT identifier, request by value or reference, outer and inner parameter consistency, algorithm allowlist, signature-verification placeholder, replay cache, and privacy boundary",
        hypothesis="Synthetic vectors can enforce JAR request-object structure and refusal obligations without asserting a real client, key, authorization server, token, network exchange, interoperability event, or production assurance.",
        null_or_failure="Audience or expiry is absent, inner and outer parameters conflict silently, an unsupported algorithm passes, replay is accepted, parse occurs before verification, or synthetic structure becomes a real authorization or identity claim.",
        approval_class="safe_now_synthetic_nonproduction",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6474-S08"],
        concrete_artifacts=["freed-id/jar-profile.json", "freed-id/jar-mutations.json"],
        test_falsifier_or_acceptance_gate="Vectors must reject missing audience or expiry, stale time, duplicated identifier, parameter mismatch, unsupported algorithm, verification-after-use, unbound request reference, replay, and production overclaim.",
        rollback_or_recovery="Reject and retain the vector, perform no live request, and require standards-conformant real keys, clients, servers, interoperability, privacy and independent security review, recovery, and trust governance.",
        protected_gates=["real_keys", "real_clients", "live_authorization", "network_exchange", "interoperability", "privacy_assurance", "production"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="Prior Freed ID work covers RAR, DPoP, OpenID4VP and VCI, SD-JWT, WebAuthn, SCITT, VC related resources, status, and controlled identifiers; no frozen title centers RFC 9101 JAR request objects and parameter consistency.",
    ),
    proposal(
        6,
        title="CBR wastewater overflow, public-health reach, worker and community privacy, remedy, legal, cultural, data-governance, and Māori-authority matrix",
        mission_surface="synthetic overflow or bypass, public-health reach, environmental receiving context, accessibility, worker and community privacy, notification, correction, remedy, legal interpretation, affected parties, water and place data, and Māori authority",
        hypothesis="A refusal-first matrix can expose unresolved overflow, privacy, remedy, and authority questions without deciding a real discharge, health risk, notification, entitlement, disclosure, place meaning, data governance, or remedy.",
        null_or_failure="The matrix identifies a real person, worker, address, plant, community, water body, discharge, or incident; decides health risk, fault, compensation, law, data governance, cultural meaning, or Māori authority; or discloses protected data.",
        approval_class="authorized_affected_parties_and_competent_authority_required",
        execution_lane="x2_exact_gate",
        current_primary_or_official_source_needs=["V6474-S06", "V6474-S07", "V6474-S09"],
        concrete_artifacts=["cbr/wastewater-authority-reservation.json", "cbr/wastewater-remedy-matrix.json"],
        test_falsifier_or_acceptance_gate="Repository software must stop at unknown or reserved; only competent wastewater, environmental, public-health, privacy, legal, accessibility, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their respective gates.",
        rollback_or_recovery="Stop before reporting, disclosure, operational, health, compensation, cultural, place, data-governance, or legal conclusions; minimize data and route only through authorized external processes.",
        protected_gates=["affected_party_authority", "wastewater_authority", "public_health_authority", "privacy", "legal_interpretation", "maori_authority", "data_governance", "remedy_decision"],
        expected_disposition="exact_gate",
        novelty_against_prior_frozen_proposals="Prior CBR matrices address drinking water, electricity, telecommunications, aviation, rail, wildfire, food, fisheries, medicine, archives, and other domains; no frozen title centers wastewater overflow, public-health reach, worker and community privacy, remedy, governance, and Māori authority.",
    ),
    proposal(
        7,
        title="TAR PAX extended-header, sparse-map, hardlink-target, path-confinement, and extraction-budget tribunal",
        mission_surface="archive format, PAX key-value header, GNU sparse map, regular file, directory, symbolic and hard link, normalized target, absolute or parent path, duplicate member, member count, expanded-byte budget, extraction filter, and destination confinement",
        hypothesis="A bounded in-memory tribunal can reject unsafe TAR metadata and extraction plans without writing outside a disposable owner-local fixture or claiming production archive security.",
        null_or_failure="An absolute or parent path passes, a link escapes, sparse expansion exceeds budget, duplicate overwrite is silent, PAX metadata changes identity after review, or synthetic parsing becomes exhaustive security assurance.",
        approval_class="safe_now_disposable_synthetic_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6474-S10"],
        concrete_artifacts=["tooling/tar-pax-contract.json", "tooling/tar-pax-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must cover PAX headers, sparse maps, regular files, link targets, absolute and parent traversal, duplicate members, normalized collisions, member and expanded-byte limits, filters, and complete refusal.",
        rollback_or_recovery="Reject and retain the fixture, extract nothing outside the disposable root, restore strict normalization and budgets, and make no production or exhaustive-security claim.",
        protected_gates=["external_path", "destructive_action", "production_archive", "security_certification", "exhaustive_security"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior tooling covers ZIP, OCI layers, Git stores, SQLite, JSON sequences, HTTP, and TUF; no frozen title centers TAR PAX headers, sparse maps, hardlink targets, and extraction budgets.",
    ),
    proposal(
        8,
        title="Accessible tabs tablist, selected-state, panel association, roving-focus, keyboard-order, fallback, and print structural audit",
        mission_surface="tablist label, tab role, one selected tab, roving tabindex, tab-to-panel control, panel label, hidden state, source order, arrow-key declaration, manual activation, text fallback, responsive layout, and print sequence",
        hypothesis="A structural auditor can reject inconsistent tabs semantics, focus state, panel association, and fallback order while reserving browser, assistive-technology, language, manual-keyboard, and affected-user evaluation.",
        null_or_failure="More than one tab is selected, focusability disagrees, controls or labels break, hidden state conflicts, source order is lost, arrow behavior is claimed without implementation, or structural evidence becomes complete conformance.",
        approval_class="safe_now_structural_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6474-S11", "V6474-S12"],
        concrete_artifacts=["accessibility/tabs-contract.json", "accessibility/tabs-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must reject unlabeled tablists, absent or multiple selection, tabindex mismatch, broken controls or labels, hidden-state mismatch, order drift, missing fallback, and complete-conformance promotion.",
        rollback_or_recovery="Restore native buttons and headings, one selected state, explicit associations, logical source and print order, and text fallback; retain failed fixtures and reserve manual evaluation.",
        protected_gates=["manual_keyboard", "browser_diversity", "assistive_technology", "maori_language", "cognitive_accessibility", "affected_user", "complete_conformance"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior accessibility work covers breadcrumbs, carousels, dialogs, forms, tables, charts, maps, long-form text, dragging, and disclosures; no frozen title centers tabs, tablists, selected state, panel association, and roving focus.",
    ),
    proposal(
        9,
        title="Thermo/Psyche Kelvin-Planck and Clausius second-law statement, cyclic-device, reservoir, and morality-nonconversion classifier",
        mission_surface="thermodynamic system, cyclic device, hot and cold reservoirs, heat sign, work sign, net state change, Kelvin-Planck form, Clausius form, equivalence assumptions, perpetual-motion refusal, domain, and psyche firewall",
        hypothesis="A typed classifier can enforce the physical domain and sign obligations of the two second-law statements while rejecting conversion into moral, psychological, consciousness, justice, or participant claims.",
        null_or_failure="A noncyclic process is treated as a cycle, reservoirs disappear, sign convention changes, heat becomes psyche effort, work becomes virtue, impossibility becomes moral law, or synthetic examples become participant evidence.",
        approval_class="safe_now_formal_nonconversion",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6474-S13"],
        concrete_artifacts=["thermo-psyche/second-law-statements-contract.json", "thermo-psyche/second-law-statements-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must type system, cycle, reservoirs, heat and work signs, state change, both statements, equivalence assumptions, device refusal, domain, and psyche firewall and reject every omitted or relabeled obligation.",
        rollback_or_recovery="Restore physical definitions and signs, retain rejected vectors, and reject moral, human, consciousness, capability, justice, or fundamental-psyche-law conversion.",
        protected_gates=["participant_claim", "psychological_claim", "consciousness", "personhood", "justice_claim", "fundamental_psyche_law"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior classifiers cover Clausius inequality, Nernst, Ruppeiner, phase rules, Maxwell relations, Le Chatelier, Onsager, exergy, and fluctuation relations; no frozen title jointly centers the Kelvin-Planck and Clausius statement forms and their cyclic-device assumptions.",
    ),
    proposal(
        10,
        title="Stage 20 target-trial time-zero, eligibility-assignment-follow-up alignment, immortal-time bias, and nonpromotion board",
        mission_surface="target protocol, eligibility time, strategy assignment, time zero, follow-up start, outcome clock, grace period, future-information use, immortal interval, selection risk, deviation record, and promotion refusal",
        hypothesis="A fail-closed structural board can reject time-zero misalignment and future-information leakage without estimating a participant effect or authorizing Stage 20.",
        null_or_failure="Eligibility, assignment, and follow-up are misaligned; future outcomes determine inclusion; an immortal interval is credited; observational structure becomes randomization; or a passing form authorizes Stage 20.",
        approval_class="safe_now_structural_hold_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6474-S14"],
        concrete_artifacts=["stage20/target-trial-alignment-contract.json", "stage20/target-trial-alignment-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must reject late or early time zero, postassignment eligibility, outcome-informed inclusion, immortal-time credit, unrecorded grace periods, randomization claims, and any automatic promotion.",
        rollback_or_recovery="Hold Stage 20, retain failed fixtures, restore the preregistered protocol timeline, and require real participant governance, appropriate design, independent review, and exact authority.",
        protected_gates=["participants", "causal_effect", "randomization_claim", "independent_review", "stage20", "proof_canon", "deployment"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior Stage 20 boards cover optional stopping, controls, HARKing, MNAR, model comparison, prequential drift, contamination, multiplicity, and Goodhart effects; no frozen title centers target-trial time-zero alignment and immortal-time bias.",
    ),
]

SOURCES = [
    ("V6474-S01", "current", "official", "Python os documentation", "https://docs.python.org/3.12/library/os.html", "Bound os.replace semantics; it does not prove crash durability or directory persistence."),
    ("V6474-S02", "stable", "primary", "2PI effective action and gauge invariance problems", "https://arxiv.org/abs/hep-ph/0309084", "Supplies formal 2PI gauge-dependence obligations only."),
    ("V6474-S03", "stable", "primary", "2PI effective actions versus resummation", "https://arxiv.org/abs/1503.08664", "Supplies self-consistency and truncation context only."),
    ("V6474-S04", "current", "official", "Planck Legacy Archive", "https://pla.esac.esa.int/", "Identifies official PR4 products; no product was queried or downloaded."),
    ("V6474-S05", "stable", "official", "ESA Planck publications", "https://www.cosmos.esa.int/web/planck/publications", "Provides release provenance only, not GMUT observation."),
    ("V6474-S06", "current", "official", "Taumata Arowai wastewater measures", "https://www.taumataarowai.govt.nz/wastewater-sector/wastewater-measures", "Constrains synthetic fields; confers no operational or legal authority."),
    ("V6474-S07", "current", "official", "Wastewater Environmental Performance Standards Regulations 2025", "https://www.legislation.govt.nz/regulation/public/2025/0258/latest/LMS1541197.html", "Current legal text is source context only; no legal interpretation is made."),
    ("V6474-S08", "stable", "official", "RFC 9101 OAuth JAR", "https://www.rfc-editor.org/rfc/rfc9101.html", "Defines synthetic request-object obligations; no live OAuth event."),
    ("V6474-S09", "stable", "primary_authority_statement", "Te Mana Raraunga Māori Data Sovereignty principles", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Preserves Māori data-governance reservation; repository software cannot confer authority."),
    ("V6474-S10", "current", "official", "Python tarfile documentation", "https://docs.python.org/3.12/library/tarfile.html", "Constrains bounded archive fixtures; no exhaustive-security assurance."),
    ("V6474-S11", "current", "official", "WAI-ARIA APG Tabs Pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/tabs/", "Structural guidance only; APG examples are not complete conformance evidence."),
    ("V6474-S12", "current", "official", "WCAG 2.2", "https://www.w3.org/TR/WCAG22/", "Reserves manual and affected-user evaluation."),
    ("V6474-S13", "stable", "primary", "Mathematical representation of Clausius and Kelvin statements", "https://arxiv.org/abs/1805.09530", "Supplies physical-domain distinctions only."),
    ("V6474-S14", "stable", "primary", "Specifying a target trial prevents immortal time bias", "https://pmc.ncbi.nlm.nih.gov/articles/PMC5124536/", "Supplies structural time-zero obligations; no participant effect is estimated."),
]

SAFE_TASK_TITLES = [f"Bounded acceptance and mutation witness for {p['proposal_id']}" for p in PROPOSALS] + [
    "Build the exact 500-proposal collision ledger", "Build the source-status and nonconversion ledger",
    "Build the x1 versus x2 byte-separation review", "Build the owner-file threshold receipt",
    "Build the five-class privacy candidate classifier", "Build the commit-local manifest checker",
    "Build the stale lifecycle-label review", "Build the phase commit-cap audit",
    "Build the named local-only replay audit", "Build the source and anchor ancestry audit",
    "Build the outcome vocabulary validator", "Build the retained-negative arithmetic validator",
    "Build the open-gap and exact-gate arithmetic validator", "Build the static report structural audit",
    "Build the manual and affected-user evaluation reservation", "Build the authority-reservation linter",
    "Build the zero-real-row and zero-likelihood counter", "Build the zero-real-people and operations counter",
    "Build the zero-real-key and network-event counter", "Build the terminal route one-shot gate",
]
CANDIDATE_TITLES = [
    "Atomic publication crash-point and stale-temp prototype", "Atomic replace filesystem-boundary prototype",
    "2PI source Legendre and stationarity prototype", "2PI self-energy truncation and conservation prototype",
    "Planck PR4 unit beam component and mask prototype", "Planck zero-row likelihood refusal prototype",
    "Wastewater influent aeration clarifier and sample-custody prototype", "Wastewater bypass refusal and handover prototype",
    "JAR request-object validation and parameter-consistency prototype", "JAR replay algorithm and production-refusal prototype",
    "Wastewater privacy remedy and authority matrix prototype", "Wastewater data-governance and Māori-authority reservation prototype",
    "TAR PAX sparse link and path classifier", "TAR extraction budget and duplicate-member prototype",
    "Tabs selected-state association and focus prototype", "Tabs fallback responsive and print prototype",
    "Kelvin-Planck and Clausius statement domain prototype", "Second-law psyche nonconversion prototype",
    "Target-trial time-zero alignment prototype", "Immortal-time and Stage 20 nonpromotion prototype",
]
SKILL_SPECS = [
    ("ghc-family-atomic-publish-tribunal", "Audit temporary publication, replace, flush, quarantine, and evidence credit"),
    ("ghc-family-two-pi-obligations", "Audit 2PI sources, Legendre transforms, closure, and conserving truncation"),
    ("ghc-family-planck-pr4-zero-row", "Preserve a zero-row Planck PR4 study boundary"),
    ("ghc-family-wastewater-handover-proxy", "Audit synthetic wastewater state, custody, bypass refusal, and handover"),
    ("ghc-family-oauth-jar-profile", "Audit synthetic RFC 9101 request objects and parameter consistency"),
    ("ghc-family-wastewater-authority-reservation", "Reserve wastewater privacy, remedy, governance, and Māori authority"),
    ("ghc-family-tar-pax-tribunal", "Audit PAX, sparse, link, path, and extraction-budget obligations"),
    ("ghc-family-tabs-structural-audit", "Audit tabs roles, selection, panel association, focus, and fallback"),
    ("ghc-family-second-law-statement-domain", "Keep Kelvin-Planck and Clausius claims inside physical domains"),
    ("ghc-family-target-trial-nonpromotion", "Guard time-zero alignment and immortal-time bias from promotion"),
    ("ghc-family-corpus-500-collision-gate", "Audit exact and semantic novelty against 500 frozen proposals"),
    ("ghc-family-source-status-watch-v2", "Preserve current, stable, draft, and watch source labels"),
    ("ghc-family-x1-x2-byte-separation-v2", "Prove x1 contains no x2 implementation or outcome bytes"),
    ("ghc-family-named-replay-locality-v3", "Verify a named replay stays clean, local, unpushed, and without upstream"),
    ("ghc-family-commit-manifest-parity-v4", "Audit exact lifecycle manifests in commit-blob domains"),
    ("ghc-family-five-class-privacy-adjudication-v3", "Separate scanner definitions, policy candidates, and payload hits"),
    ("ghc-family-stage-label-lifecycle-lint-v3", "Reject stale prepared, sent, evidence, closeout, and seal labels"),
    ("ghc-family-authority-reservation-matrix-v3", "Prevent software evidence from compensating for authority gaps"),
    ("ghc-family-failure-before-retry-v2", "Require retained failure records before bounded recovery"),
    ("ghc-family-baton-ack-one-shot-v3", "Count one existing-task baton only after acknowledged delivery"),
]
RUNNER_TITLES = [
    "ghc_family_atomic_publish_tribunal.py", "ghc_family_two_pi_obligations.py",
    "ghc_family_planck_pr4_zero_row.py", "ghc_family_wastewater_handover.py",
    "ghc_family_oauth_jar_profile.py", "ghc_family_wastewater_authority.py",
    "ghc_family_tar_pax_tribunal.py", "ghc_family_tabs_audit.py",
    "ghc_family_second_law_statements.py", "ghc_family_target_trial_board.py",
]
CLEAN_TASK_TITLES = [
    "Reconcile proposal and outcome counts across receipts", "Reconcile inherited synthetic and operational negatives",
    "Synchronize Method Flow counts and validator expectations", "Correct stale phase labels additively",
    "Preserve compatibility callers while selecting family-current tools", "Normalize generated JSON key ordering",
    "Normalize generated UTF-8 and LF authoring", "Keep Git-blob and working-tree hash domains explicit",
    "Review public files for private absolute paths", "Review public files for raw task or thread identifiers",
    "Review public files for credentials tokens and private keys", "Review source statuses for allowed vocabulary",
    "Review Planck sources for zero-row nonconversion", "Review citations for observation and authority nonconversion",
    "Review x1 staged files for x2 contamination", "Review x2 outcomes for four-class vocabulary",
    "Review exact and blocked packets for zero execution credit", "Review owner footprint against 15000 files",
    "Review tabs report structure and manual reservations", "Review assistive-technology and affected-user reservations",
    "Review Māori authority and data-governance reservations", "Review wastewater professional operational and legal reservations",
    "Review real-data query and likelihood counters remain zero", "Review real-operator plant sample discharge and incident counters remain zero",
    "Review real-key client server and interoperability counters remain zero", "Review source and phase-anchor ancestry",
    "Review phase commit cap zero merges and final parent", "Review validation branch remains named and local-only",
    "Review canonical four-way remote equality", "Refresh index wellbeing and terminal route before handoff",
]
EXACT_PACKET_TITLES = [
    "Real Planck query download likelihood or parameter inference", "Real wastewater plant control bypass discharge or sampling action",
    "Real environmental or public-health notification", "Production JAR key client server or authorization operation",
    "Real identity interoperability recovery or trust-governance decision", "Protected worker community water or place data disclosure",
    "Legal interpretation remedy allocation or health-risk determination", "Māori authority or data-governance decision",
    "Production deployment security certification or exhaustive-security claim", "Independent reproduction Stage 20 proof or canon decision",
]
BLOCKED_PACKET_TITLES = [
    "Force-push rewrite or merge canonical history", "Delete reuse or mutate a sibling-owned lane",
    "Expose credentials private routes private records or raw task identifiers", "Enable Windows features weaken security elevate or install unrelated software",
    "Claim consciousness personhood AGI ASI or Theory-of-Everything closure",
]

X1_NEGATIVES = [{
    "negative_id": "V6474-X1-N01",
    "method_id": "V6474-M01",
    "summary": "The first read-only manifest summary piped directly from a PowerShell foreach block and failed parsing before reading any manifest; assigning structured output or using one reader recovered without mutation.",
    "retained": True,
    "recovered": True,
}]
METHOD_SPECS = [{
    "method_id": "V6474-M01",
    "title": "Assign PowerShell loop output before serialization",
    "failure_signature": "PowerShell rejected a direct pipe from the foreach statement with an empty-pipe parser error.",
    "trigger_preconditions": ["A read-only PowerShell loop builds structured manifest summaries for later serialization."],
    "candidate_workaround": "Assign loop output to a variable before piping, or use one bounded structured reader.",
    "recurrence_guard": "Do not pipe directly from a PowerShell foreach statement in compound diagnostics; check each native exit explicitly.",
    "rollback": "Discard the failed read-only command; it changed no file, ref, index, or worktree.",
    "protected_gates": ["source_verification", "no_repository_mutation", "manifest_parity", "privacy"],
    "retained_negative_ids": ["V6474-X1-N01"],
    "failed_observed": "The shell returned a parser error before manifest input was read.",
    "pass_observed": "A bounded structured reader summarized all three manifests and the exact commit-blob audit passed 78, 151, and 35 entries.",
}]
