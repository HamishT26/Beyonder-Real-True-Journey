#!/usr/bin/env python3
"""Frozen x1 catalogue for Sable Rook's v657-v4 phase."""

from __future__ import annotations


def source(
    source_id: str,
    title: str,
    publisher: str,
    url: str,
    status: str,
    use: str,
) -> dict:
    return {
        "source_id": source_id,
        "title": title,
        "publisher": publisher,
        "url": url,
        "status": status,
        "observed_on": "2026-08-01",
        "use": use,
    }


OFFICIAL_SOURCES = [
    source(
        "OHS-CONSERVATION-GUIDELINES",
        "Guidelines for Conservation",
        "Organ Historical Society",
        "https://organhistoricalsociety.org/wp-content/uploads/2017/09/ConservGuidelines.pdf",
        "stable",
        "pipe-organ conservation vocabulary and reversible documentation context only; no treatment authority or professional conclusion",
    ),
    source(
        "OHS-PIPE-ORGAN-DATABASE",
        "Pipe Organ Database",
        "Organ Historical Society",
        "https://beta.pipeorgandatabase.org/",
        "current",
        "public data-product identity and zero-row adapter readiness only; no query, download, attribution, or empirical inference",
    ),
    source(
        "CCI-INDUSTRIAL-COLLECTIONS",
        "The Care of Industrial Collections",
        "Canadian Conservation Institute",
        "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/industrial-collections.html",
        "current",
        "collection-condition, material, documentation, hazard, and intervention-reservation context only",
    ),
    source(
        "SMITHSONIAN-OPEN-ACCESS",
        "Smithsonian Open Access Developer Tools",
        "Smithsonian Institution",
        "https://www.si.edu/openaccess/devtools",
        "current",
        "public-source and rights metadata vocabulary only; no collection, custody, attribution, or authority claim",
    ),
    source(
        "OSHA-1910-147",
        "29 CFR 1910.147 Control of hazardous energy",
        "United States Occupational Safety and Health Administration",
        "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147",
        "current",
        "hazardous-energy vocabulary only; no workplace procedure, training, isolation, or compliance determination",
    ),
    source(
        "NIST-SP800-61R3",
        "Incident Response Recommendations and Considerations for Cybersecurity Risk Management",
        "National Institute of Standards and Technology",
        "https://csrc.nist.gov/pubs/sp/800/61/r3/final",
        "current",
        "incident, negative-test, recovery, communication, and handover vocabulary only",
    ),
    source(
        "BIPM-SI-BROCHURE",
        "The International System of Units (SI Brochure)",
        "Bureau International des Poids et Mesures",
        "https://www.bipm.org/en/publications/si-brochure",
        "stable",
        "units, dimensions, and quantity-expression obligations only; no measurement or empirical result",
    ),
    source(
        "NIST-SP811",
        "Guide for the Use of the International System of Units",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/pml/special-publication-811",
        "stable",
        "unit-symbol and dimensional-consistency context only; no calibration or measurement authority",
    ),
    source(
        "W3C-PROV-O",
        "PROV-O: The PROV Ontology",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        "entity, activity, attribution, derivation, revision, invalidation, and delegation lineage",
    ),
    source(
        "RFC-3339",
        "RFC 3339: Date and Time on the Internet",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic UTC timestamps, revision windows, expiry, correction, and handover",
    ),
    source(
        "RFC-8785",
        "RFC 8785: JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic contracts, digests, manifests, and receipts",
    ),
    source(
        "W3C-WCAG-22",
        "Web Content Accessibility Guidelines 2.2",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/WCAG22/",
        "current",
        "structural accessibility vocabulary with manual and affected-user evaluation reserved",
    ),
    source(
        "NZ-PRIVACY-PRINCIPLES",
        "Privacy Act 2020 information privacy principles",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        "purpose, collection, fairness, security, access, correction, retention, use, and disclosure reservations only",
    ),
    source(
        "TMR-PRINCIPLES",
        "Principles of Māori Data Sovereignty",
        "Te Mana Raraunga",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "current",
        "authority-reservation context only; Māori data governance remains with Māori authorities",
    ),
    source(
        "LOCAL-CONTEXTS-LABELS",
        "Traditional Knowledge and Biocultural Labels",
        "Local Contexts",
        "https://localcontexts.org/labels/about-the-labels/",
        "current",
        "community-defined provenance and protocol vocabulary with community authority reserved",
    ),
    source(
        "W3C-VC-DM-20",
        "Verifiable Credentials Data Model v2.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-model/",
        "current",
        "synthetic credential vocabulary only; no real issuer, holder, verifier, proof, status, or trust decision",
    ),
    source(
        "W3C-DID-10",
        "Decentralized Identifiers v1.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/did-1.0/",
        "stable",
        "synthetic identifier-document vocabulary only; no live method, resolution, key, controller, or trust claim",
    ),
    source(
        "W3C-BITSTRING-STATUS-10",
        "Bitstring Status List v1.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-bitstring-status-list/",
        "current",
        "synthetic status and privacy-obligation vocabulary only; no live status service, revocation, key, or interoperability event",
    ),
]


PROTECTED_GATES = [
    "real_owners_custodians_congregations_builders_technicians_conservators_communities_and_affected_parties",
    "real_pipe_organs_buildings_pipework_wind_systems_actions_consoles_electrical_systems_tools_materials_and_records",
    "real_energization_access_at_height_dismantling_cleaning_tuning_adjustment_repair_restoration_operation_or_return_to_service",
    "real_measurements_calibrations_acoustics_tuning_performance_statistics_likelihoods_predictions_and_empirical_gmut_confirmation",
    "professional_pipe_organ_building_conservation_electrical_structural_fire_accessibility_privacy_workplace_or_worship_authority",
    "sensitive_donor_worship_memorial_location_traditional_knowledge_and_culturally_restricted_information",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_religious_heritage_indigenous_traditional_knowledge_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_treatment_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def proposal(
    number: int,
    title: str,
    slug: str,
    pillar: str,
    mechanism: str,
    sources: list[str],
    expected_disposition: str,
) -> dict:
    approval = "safe_now_bounded_structural_formal_or_synthetic_software"
    execution_lane = "x2_owner_local_bounded_synthetic"
    if expected_disposition == "open_gap":
        approval = "candidate_external_readiness_without_network_call"
        execution_lane = "x2_owner_local_zero_row_readiness"
    elif expected_disposition == "exact_gate":
        approval = "exact_approval_authorized_affected_party_required"
        execution_lane = "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6574-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable synthetic evidence obligations "
            "while refusing unsupported empirical, professional, security, accessibility, privacy, "
            "identity, production, legal, cultural, Māori-authority, or Stage 20 promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, "
            "erases a failure, or crosses a protected participant, object, treatment, empirical, "
            "professional, production, legal, cultural, Māori-authority, identity, or Stage 20 gate."
        ),
        "approval_class": approval,
        "execution_lane": execution_lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": (
            "The valid synthetic fixture passes, five preregistered mutations are rejected, and "
            "the receipt grants no real person, pipe organ, building, treatment, professional, "
            "production, legal, cultural, Māori-authority, identity, accessibility-complete, "
            "privacy-complete, security-complete, independent-reproduction, Theory-of-Everything, "
            "or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real "
            "people, pipe organs, buildings, tools, materials, accounts, records, treatments, "
            "professional decisions, sibling lanes, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Pipe-organ accession boundary with custodial claim, nave-or-loft locator, organ-case scope, minimal contact token, dispute channel, and intervention lock", "pipe-organ-intake-provenance", "Freed ID and CBR Heart", "pipe-organ accession boundary, custodial claim, nave-or-loft locator, case scope, minimal contact token, dispute channel, and intervention lock", ["OHS-CONSERVATION-GUIDELINES", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Pipe-organ builder plate, opus, location, date, attribution-source, conflict quarantine, and authenticity nonclaim ledger", "pipe-organ-identity-ledger", "Freed ID and CBR Heart", "builder plate, opus, location, date, attribution source, conflict quarantine, and authenticity refusal", ["OHS-PIPE-ORGAN-DATABASE", "W3C-PROV-O", "RFC-8785"]),
    ("Pipe-organ mandate-delta register with requested documentation, forbidden intervention, approver placeholder, divergence checkpoint, dual readback, and action lock", "pipe-organ-scope-revision", "CBR Heart and Freed ID", "mandate delta, requested documentation, forbidden intervention, approver placeholder, divergence checkpoint, dual readback, and action lock", ["OHS-CONSERVATION-GUIDELINES", "W3C-PROV-O", "RFC-3339"]),
    ("Pipe-organ division, chest, reservoir, trunk, console, and wind-system topology graph with orphan quarantine and no-disassembly instruction", "pipe-organ-system-topology", "GMUT Mind and Freed ID", "division, chest, reservoir, trunk, console, and wind-system topology with orphan quarantine and disassembly-instruction refusal", ["OHS-CONSERVATION-GUIDELINES", "W3C-PROV-O", "RFC-8785"]),
    ("Pipe-organ stoplist, rank, pipework-source, alteration, uncertainty, and voicing-authority refusal register", "pipe-organ-stop-rank-provenance", "Freed ID and GMUT Mind", "stoplist, rank, pipework source, alteration, uncertainty, and voicing-authority refusal", ["OHS-PIPE-ORGAN-DATABASE", "OHS-CONSERVATION-GUIDELINES", "W3C-PROV-O"]),
    ("Pipe-organ key, action, coupler, relay, and transmission topology board with hybrid-state uncertainty and adjustment refusal", "pipe-organ-action-topology", "GMUT Mind and THOS Body", "key, action, coupler, relay, and transmission topology, hybrid uncertainty, and adjustment refusal", ["OHS-CONSERVATION-GUIDELINES", "W3C-PROV-O", "RFC-8785"]),
    ("Pipe-organ blower, reservoir, regulator, trunk, pressure-unit, stored-energy, and hazardous-operation boundary", "pipe-organ-wind-energy-boundary", "THOS Body and GMUT Mind", "blower, reservoir, regulator, trunk, pressure-unit, stored-energy, and hazardous-operation reservation", ["OSHA-1910-147", "BIPM-SI-BROCHURE", "OHS-CONSERVATION-GUIDELINES"]),
    ("Pipe-organ console, rectifier, motor, switching, combination-action, isolation-state, and no-energization ledger", "pipe-organ-electrical-isolation", "THOS Body and CBR Heart", "console, rectifier, motor, switching, combination-action, isolation state, and energization refusal", ["OSHA-1910-147", "OHS-CONSERVATION-GUIDELINES", "W3C-PROV-O"]),
    ("Pipe-organ case, façade, screen, loft, access-route, structural cue, falling-object hold, and work-at-height refusal", "pipe-organ-case-access-hold", "THOS Body and CBR Heart", "case, façade, screen, loft, access route, structural cue, falling-object hold, and work-at-height refusal", ["CCI-INDUSTRIAL-COLLECTIONS", "OSHA-1910-147", "W3C-PROV-O"]),
    ("Pipe-organ pipework material, scale, mensuration, pitch placeholder, unit domain, uncertainty, and measurement nonclaim docket", "pipe-organ-pipework-measurement", "GMUT Mind", "pipework material, scale, mensuration, pitch placeholder, unit domain, uncertainty, and measurement refusal", ["BIPM-SI-BROCHURE", "NIST-SP811", "OHS-CONSERVATION-GUIDELINES"]),
    ("Pipe-organ temperament, reference pitch, ambient temperature, observation time, calibration hold, and tuning-authority refusal", "pipe-organ-tuning-observation", "GMUT Mind and CBR Heart", "temperament, reference pitch, ambient temperature, observation time, calibration hold, and tuning-authority refusal", ["BIPM-SI-BROCHURE", "NIST-SP811", "RFC-3339"]),
    ("Pipe-organ wind leakage, cipher, noise, response-lag, anomaly cue, diagnosis hold, and serviceability nonclaim board", "pipe-organ-anomaly-board", "THOS Body and GMUT Mind", "wind leakage, cipher, noise, response lag, anomaly cue, diagnosis hold, and serviceability refusal", ["OHS-CONSERVATION-GUIDELINES", "NIST-SP800-61R3", "W3C-PROV-O"]),
    ("Pipe-organ tracker, tubular-pneumatic, electro-pneumatic, direct-electric, hybrid, unknown, and classification-revision register", "pipe-organ-action-classification", "Freed ID and GMUT Mind", "tracker, tubular-pneumatic, electro-pneumatic, direct-electric, hybrid, unknown, and classification revision", ["OHS-PIPE-ORGAN-DATABASE", "W3C-PROV-O", "RFC-8785"]),
    ("Pipe-organ surface-contact reservation with finish-material pairing, swab-zone placeholder, residue and ventilation hazards, chemical-source trail, and no-application gate", "pipe-organ-cleaning-boundary", "THOS Body and CBR Heart", "surface-contact reservation, finish-material pairing, swab-zone placeholder, residue and ventilation hazards, chemical-source trail, and no-application gate", ["CCI-INDUSTRIAL-COLLECTIONS", "OHS-CONSERVATION-GUIDELINES", "W3C-PROV-O"]),
    ("Pipe-organ leather, felt, wood, metal, wire, adhesive, replacement-source, compatibility hold, and procurement refusal ledger", "pipe-organ-material-provenance", "Freed ID and CBR Heart", "leather, felt, wood, metal, wire, adhesive, replacement source, compatibility hold, and procurement refusal", ["CCI-INDUSTRIAL-COLLECTIONS", "OHS-CONSERVATION-GUIDELINES", "W3C-PROV-O"]),
    ("Pipe-organ original-state, alteration chronology, intervention rationale, reversibility claim, supersession, and restoration nonclaim chain", "pipe-organ-alteration-chronology", "Freed ID and CBR Heart", "original-state claim, alteration chronology, intervention rationale, reversibility claim, supersession, and restoration refusal", ["OHS-CONSERVATION-GUIDELINES", "W3C-PROV-O", "RFC-3339"]),
    ("Pipe-organ drawing, photograph, audio-sample, digest, capture context, rights class, redaction, and diagnostic refusal register", "pipe-organ-media-evidence", "Freed ID and CBR Heart", "drawing, photograph, audio sample, digest, capture context, rights class, redaction, and diagnostic refusal", ["SMITHSONIAN-OPEN-ACCESS", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Pipe-organ worship, service, rehearsal, concert, visitation, quiet-time, work-window, conflict hold, and schedule-authority refusal", "pipe-organ-event-window", "CBR Heart and THOS Body", "worship, service, rehearsal, concert, visitation, quiet time, work window, conflict hold, and schedule-authority refusal", ["RFC-3339", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Pipe-organ evidence-amendment graph with superseded assertion hash, replacement fact, dissent branch, responder reservation, and human-adjudication hold", "pipe-organ-correction-chain", "CBR Heart and Freed ID", "evidence amendment, superseded assertion hash, replacement fact, dissent branch, responder reservation, and human-adjudication hold", ["W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES", "RFC-3339"]),
    ("Thermo and Psyche acoustic-power, pressure, energy-flux, entropy-domain, unit, boundary, and agency-nonconversion classifier", "thermo-psyche-acoustic-domain", "GMUT Mind and THOS Body", "acoustic power, pressure, energy flux, entropy domain, unit, boundary, and rejection of psyche, autonomy, justice, consciousness, or personhood conversion", ["BIPM-SI-BROCHURE", "NIST-SP811", "RFC-8785"]),
    ("Accessible pipe-organ condition bulletin with semantic landmarks, plain status, redundant visual cues, alternative delivery, amendment link, and user-review hold", "pipe-organ-accessible-notice", "CBR Heart and THOS Body", "accessible condition bulletin, semantic landmarks, plain status, redundant visual cues, alternative delivery, amendment link, and user-review hold", ["W3C-WCAG-22", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Pipe-organ provenance threat model with tampering, path traversal, injection, raw-identifier, disclosure, replay, recovery, and exhaustive-security refusal", "pipe-organ-threat-recovery", "Freed ID and CBR Heart", "provenance threat model, tampering, path traversal, injection, raw identifier, disclosure, replay, recovery, and exhaustive-security refusal", ["NIST-SP800-61R3", "RFC-8785", "NZ-PRIVACY-PRINCIPLES"]),
    ("Stage 20 source-independence, common-cause, retained-negative, evidence-diversity, reproduction, and nonpromotion board", "stage20-organ-evidence-diversity", "GMUT Mind, THOS Body, and CBR Heart", "source independence, common cause, retained negative, evidence diversity, reproduction, and Stage 20 nonpromotion", ["W3C-PROV-O", "NIST-SP800-61R3", "RFC-8785"]),
    ("GMUT pipe-organ acoustic standing-wave modal dimensional proxy with length, frequency, boundary-condition, mode-index, unit, calibration, and physical-prediction refusal", "gmut-organ-acoustic-modal-proxy", "GMUT Mind", "acoustic standing-wave modal dimensional proxy, length, frequency, boundary condition, mode index, unit, calibration, and physical-prediction refusal", ["BIPM-SI-BROCHURE", "NIST-SP811", "OHS-CONSERVATION-GUIDELINES"]),
    ("GMUT pipe-organ wind-network continuity, covariance, conservation, stability, identifiability, nuisance, boundary, and likelihood-refusal board", "gmut-organ-wind-network", "GMUT Mind", "wind-network continuity, covariance, conservation, stability, identifiability, nuisance, boundary, and likelihood refusal", ["BIPM-SI-BROCHURE", "NIST-SP811", "RFC-8785"]),
    ("THOS pipe-organ documentation handover with custody state, open anomaly, isolation hold, incomplete treatment, workload cue, readback, stop-work, and matched-budget real-arm refusal", "thos-organ-handover", "THOS Body", "documentation handover, custody state, open anomaly, isolation hold, incomplete treatment, workload cue, readback, stop-work, and matched-budget real-arm refusal", ["NIST-SP800-61R3", "RFC-3339", "W3C-PROV-O"]),
    ("Freed ID purpose-scoped organ-record permit with pseudonymous actor, relying audience, exact object scope, minimal claims, expiry, absent proof, and nonauthorization", "freed-id-organ-capability", "Freed ID and CBR Heart", "purpose-scoped organ-record permit, pseudonymous actor, relying audience, exact object scope, minimal claims, expiry, absent proof, and nonauthorization", ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID pipe-organ evidence disclosure, controller, resolution, status, revocation, interoperability, recovery, correlation, and trust-governance gap profile", "freed-id-organ-status-profile", "Freed ID", "evidence disclosure, controller, resolution, status, revocation, interoperability, recovery, correlation, and trust-governance gap profile", ["W3C-VC-DM-20", "W3C-DID-10", "W3C-BITSTRING-STATUS-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Organ Historical Society Pipe Organ Database no-network zero-row adapter with query-purpose, attribution, revision, quality, nuisance, likelihood, and inference refusal", "organ-database-zero-row-adapter", "GMUT Mind and CBR Heart", "Pipe Organ Database no-network zero-row adapter, query purpose, attribution, revision, quality, nuisance, likelihood, and inference refusal", ["OHS-PIPE-ORGAN-DATABASE", "RFC-8785", "W3C-PROV-O"]),
    ("CBR pipe-organ heritage, ownership, custody, worship, memorial, access, privacy, remedy, law, culture, data governance, affected-party, and Māori-authority nonautomation covenant", "cbr-organ-authority-covenant", "CBR Heart", "heritage, ownership, custody, worship, memorial, access, privacy, remedy, law, culture, data governance, affected-party, and Māori-authority nonautomation", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES", "W3C-WCAG-22"]),
]


PROPOSALS = [
    proposal(
        number,
        title,
        slug,
        pillar,
        mechanism,
        sources,
        "completed" if number <= 23 else "represented" if number <= 28 else "open_gap" if number == 29 else "exact_gate",
    )
    for number, (title, slug, pillar, mechanism, sources) in enumerate(PROPOSAL_SPECS, 1)
]


SKILL_SPECS = [
    ("ghc-family-pipe-organ-intake-provenance", "Freeze synthetic pipe-organ intake, custody, identity, scope, correction, and work-start boundaries."),
    ("ghc-family-pipe-organ-system-topology", "Model divisions, chests, actions, wind paths, consoles, and orphan edges without inspection or disassembly instructions."),
    ("ghc-family-pipe-organ-wind-energy-boundary", "Constrain wind pressure, units, stored energy, blowers, reservoirs, isolation, and operation refusal."),
    ("ghc-family-pipe-organ-electrical-isolation", "Fail closed around rectifiers, motors, switching, combination actions, hazardous energy, and energization."),
    ("ghc-family-pipe-organ-material-treatment", "Preserve material, cleaning, replacement, treatment, reversibility, and procurement uncertainty."),
    ("ghc-family-pipe-organ-source-correction", "Preserve source, attribution, alteration, media, revision, correction, contestation, and rights lineage."),
    ("ghc-family-pipe-organ-accessibility-privacy", "Structure accessible notices and minimized records while reserving manual, affected-user, and legal review."),
    ("ghc-family-pipe-organ-thos-handover", "Constrain event windows, workload, open anomalies, stop-work, readback, and synthetic handover."),
    ("ghc-family-pipe-organ-freed-id", "Constrain synthetic capability, disclosure, status, resolution, revocation, interoperability, privacy, and trust claims."),
    ("ghc-family-pipe-organ-authority-reservation", "Fail closed around heritage, worship, ownership, remedy, law, culture, governance, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_pipe_organ_intake_provenance.py", "pipe-organ-intake-provenance"),
    ("ghc_family_pipe_organ_system_topology.py", "pipe-organ-system-topology"),
    ("ghc_family_pipe_organ_wind_energy_boundary.py", "pipe-organ-wind-energy-boundary"),
    ("ghc_family_pipe_organ_electrical_isolation.py", "pipe-organ-electrical-isolation"),
    ("ghc_family_pipe_organ_material_treatment.py", "pipe-organ-material-provenance"),
    ("ghc_family_pipe_organ_source_correction.py", "pipe-organ-correction-chain"),
    ("ghc_family_pipe_organ_accessibility_privacy.py", "pipe-organ-accessible-notice"),
    ("ghc_family_pipe_organ_thos_handover.py", "thos-organ-handover"),
    ("ghc_family_pipe_organ_freed_id.py", "freed-id-organ-capability"),
    ("ghc_family_pipe_organ_authority_reservation.py", "cbr-organ-authority-covenant"),
]


def negative(number: int, slug: str, failure: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6574-X1-N{number:02d}",
        "scope": "startup_and_x1",
        "signature": slug,
        "observed": failure,
        "credit": 0,
        "retained": True,
        "recovery": recovery,
        "recurrence_guard": guard,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


X1_OPERATIONAL_NEGATIVES = [
    negative(1, "broad-worktree-list-timeout", "A broad git worktree list exceeded its useful bound without an attributable result.", "Use exact known D-drive worktree and branch probes.", "Prefer literal target probes over archive-wide enumeration."),
    negative(2, "broad-worktree-directory-timeout", "A broad D-drive worktree-directory listing exceeded its useful bound without a complete result.", "Probe only the exact source and Sable target paths.", "Never enumerate the whole archive when exact paths are known."),
    negative(3, "short-exact-drive-probe-timeout", "The first exact D-drive Test-Path probe exceeded an undersized ten-second startup bound.", "Repeat the same read-only literal-path probe with a measured bounded allowance.", "Calibrate PowerShell startup bounds before treating silence as absence."),
    negative(4, "combined-source-status-wrapper-no-output", "The first combined source status wrapper returned no attributable output.", "Split head, upstream, tracked/index status, and untracked checks into scalar probes.", "Bind each source claim to a separately observable scalar result."),
    negative(5, "unavailable-hidden-shell-command", "An attempted hidden shell-command helper was unavailable and failed before execution.", "Use the installed exec-command surface with literal paths and bounded output.", "Inspect callable tool availability before dispatch."),
    negative(6, "empty-rg-pipeline-inventory", "A broad rg file pipeline produced no useful attributable inventory.", "Use exact bounded directory and file probes.", "Treat empty pipeline output as zero-credit until exact paths are checked."),
    negative(7, "manifest-read-output-truncation", "A massive raw source-manifest read exceeded the useful output budget and truncated evidence.", "Parse each manifest and report only counts, exclusions, and mismatches.", "Summarize large manifests from exact parsed entries rather than printing them."),
    negative(8, "combined-environment-wrapper-no-output", "A combined version and baton-hash wrapper completed without attributable output.", "Separate repository identity, baton digest, CLI, desktop, and runtime probes.", "Do not combine slow version discovery with immutable-source identity checks."),
    negative(9, "unicode-context-patch-mismatch", "A combined overview patch depended on terminal-rendered Unicode context and was rejected without changing the file.", "Anchor the patch on ASCII function boundaries and apply the current UTF-8 wording separately.", "Use ASCII-safe structural anchors when displayed encoding may differ from repository bytes."),
    negative(10, "multi-hunk-send-gate-context-mismatch", "A multi-hunk semantic patch included a stale send-gate context and was rejected atomically.", "Split the patch into observed exact hunks and patch the route field independently.", "Inspect each lifecycle field immediately before including it in a multi-hunk patch."),
    negative(11, "combined-status-build-wrapper-lost-failure-output", "A combined Git-status and x1-build wrapper emitted only the status block and no attributable builder result or phase tree.", "Invoke the builder alone and inspect its exact exit code and stderr.", "Run state inventory and evidence-producing builders as separate bounded commands."),
    negative(12, "premature-phase-tree-probe-after-silent-wrapper", "A follow-up phase-tree inventory assumed the silent wrapper had built the packet and returned repeated missing-path errors.", "Require an explicit zero builder exit before probing generated paths.", "Never infer materialization from wrapper completion or absent stderr."),
    negative(13, "baton-checkout-versus-git-blob-hash-domain", "The first isolated builder bound the checkout-byte digest to the immutable Git-blob check and failed closed.", "Compute and record the exact Git-blob digest separately while preserving the checkout-byte digest.", "Declare and validate Git-blob and checkout-byte hash domains independently."),
    negative(14, "semantic-neighbor-quarantine-six-titles", "The first 2,500-row novelty pass rejected six titles whose generic intake, revision, cleaning, correction, accessibility, or capability wording remained too close to v657-v3 predecessors.", "Rewrite all six titles and mechanisms around pipe-organ-specific accession, mandate-delta, surface-contact, amendment-graph, bulletin, and permit obligations without lowering the threshold.", "Run the complete inherited-title screen before any x1 materialization and quarantine every row at or above 0.60."),
    negative(15, "method-flow-negative-schema-key-mismatch", "The first post-novelty x1 build wrote only preparation artifacts, then failed because the new negative helper exposed failure_signature instead of the inherited builder's required signature and observed fields.", "Align the phase-local negative schema with the reviewed Method Flow builder contract and regenerate the x1 preparation packet.", "Compile and inspect producer-consumer key parity before the first materializing build."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6574-SAFE-{index:03d}",
        "proposal_id": item["proposal_id"],
        "task": f"Build and validate the bounded synthetic contract for {item['slug']}.",
        "approval_class": "safe_now_owner_local_additive",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]


CANDIDATE_TASKS = [
    {
        "task_id": f"V6574-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6574-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, stale-label, and nonpromotion cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
