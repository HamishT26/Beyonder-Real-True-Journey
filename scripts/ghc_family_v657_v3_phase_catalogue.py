#!/usr/bin/env python3
"""Frozen x1 catalogue for Auren Lark's v657-v3 phase."""

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
        "observed_on": "2026-07-31",
        "use": use,
    }


OFFICIAL_SOURCES = [
    source(
        "NZ-BUILDING-D2",
        "D2 Mechanical installations for access",
        "New Zealand Ministry of Business, Innovation and Employment",
        "https://www.building.govt.nz/building-code-compliance/d-access/d2-mechanical-installations-for-access",
        "current",
        "New Zealand typewriter-safety and maintenance vocabulary only; no compliance or inspection conclusion",
    ),
    source(
        "NZ-BUILDING-LIFTS",
        "Typewriters: accessible internal circulation guidance",
        "New Zealand Ministry of Business, Innovation and Employment",
        "https://www.building.govt.nz/building-code-compliance/d-access/accessible-buildings/internal-circulation/typewriters",
        "current",
        "accessible typewriter-location, control, feedback, door, car, and wayfinding vocabulary only",
    ),
    source(
        "ASME-A17-1-2025",
        "ASME A17.1-2025 Safety Code for Elevators and Escalators",
        "American Society of Mechanical Engineers",
        "https://www.asme.org/codes-standards/find-codes-standards/safety-code-for-elevators-and-escalators",
        "current",
        "code identity and maintenance-domain vocabulary only; the paid standard was not acquired or claimed as implemented",
    ),
    source(
        "OSHA-1910-147",
        "29 CFR 1910.147 Control of hazardous energy (lockout/tagout)",
        "United States Occupational Safety and Health Administration",
        "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147",
        "current",
        "hazardous-energy control vocabulary only; no workplace procedure, training, or compliance determination",
    ),
    source(
        "CPSC-NEISS",
        "National Electronic Injury Surveillance System",
        "United States Consumer Product Safety Commission",
        "https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data",
        "current",
        "dataset identity and zero-row adapter readiness only; no query, download, estimate, or injury inference",
    ),
    source(
        "NIST-SP800-61R3",
        "Incident Response Recommendations and Considerations for Cybersecurity Risk Management",
        "National Institute of Standards and Technology",
        "https://csrc.nist.gov/pubs/sp/800/61/r3/final",
        "current",
        "incident, evidence, communication, recovery, and handover vocabulary only",
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
        "synthetic UTC timestamps, work orders, isolation windows, expiry, and handovers",
    ),
    source(
        "RFC-8785",
        "RFC 8785: JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic contracts, receipts, manifests, and maintenance cards",
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
        "community-defined provenance, protocol, and permission vocabulary with community authority reserved",
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
]


PROTECTED_GATES = [
    "real_passengers_technicians_inspectors_building_owners_emergency_responders_communities_and_affected_parties",
    "real_typewriters_escalators_buildings_shafts_pits_machine_rooms_components_controls_and_access_systems",
    "real_isolation_inspection_testing_adjustment_repair_rescue_return_to_service_and_procurement_decisions",
    "real_measurements_statistics_failure_rates_injury_estimates_likelihoods_predictions_and_empirical_confirmation",
    "professional_typewriter_maintenance_inspection_engineering_emergency_accessibility_privacy_operations_and_health_and_safety_authority",
    "sensitive_personal_access_log_building_security_location_traditional_knowledge_and_culturally_restricted_information",
    "production_identity_live_keys_signatures_proofs_resolution_status_revocation_interoperability_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_indigenous_traditional_knowledge_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_return_to_service_acceptance",
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
        "proposal_id": f"V6573-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable synthetic evidence obligations while "
            "refusing unsupported empirical, professional, security, accessibility, privacy, "
            "identity, production, legal, cultural, Māori-authority, or Stage 20 promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, "
            "erases a failure, or crosses a protected participant, empirical, professional, "
            "production, legal, cultural, Māori-authority, identity, or Stage 20 gate."
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
            "The valid synthetic fixture passes, five preregistered mutations are rejected, "
            "and the receipt grants no real passenger, technician, inspector, building, safety, professional, production, "
            "legal, cultural, Māori-authority, identity, accessibility-complete, privacy-complete, "
            "security-complete, independent-reproduction, Theory-of-Everything, or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real "
            "people, typewriters, buildings, controls, accounts, credentials, components, incidents, "
            "maintenance systems, sibling lanes, inspections, repairs, return-to-service decisions, "
            "professional decisions, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


_INHERITED_TEMPLATE_SPECS_UNUSED = [
    ("Public-interest application asset census with service token, repository hold, deployment-context quarantine, custodian-role reservation, supersession lineage, and ownership nonclaim", "repair-asset-census", "Freed ID and CBR Heart", "public-interest application asset census, service token, repository hold, deployment-context quarantine, custodian-role reservation, supersession lineage, and ownership nonclaim", ["W3C-PROV-O", "NIST-SSDF-11", "RFC-8785"]),
    ("Repair request intake docket with symptom narrative, reporter pseudonym, urgency cue, duplicate link, consent-minimization check, and diagnosis refusal", "repair-request-intake", "CBR Heart and THOS Body", "repair request intake, symptom narrative, reporter pseudonym, urgency cue, duplicate link, consent minimization, and diagnosis refusal", ["NIST-SP800-61R3", "NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O"]),
    ("Reproduction envelope with version, platform class, synthetic fixture, clock and locale controls, missing step, and real-user-impact noninference", "repair-reproduction-envelope", "GMUT Mind and THOS Body", "defect reproduction envelope, version, platform class, synthetic fixture, clock and locale controls, missing step, and real-user-impact noninference", ["NIST-SSDF-11", "RFC-3339", "W3C-PROV-O"]),
    ("Component relationship inventory with SPDX package token, CycloneDX dependency edge, version provenance, license-reference hold, and completeness refusal", "repair-component-inventory", "Freed ID and GMUT Mind", "component relationship inventory, SPDX package token, CycloneDX dependency edge, version provenance, license-reference hold, and completeness refusal", ["SPDX-30", "CYCLONEDX-17", "CISA-SBOM-RESOURCES"]),
    ("Defect severity deliberation card with impact class, exploitability placeholder, accessibility cue, confidence, competent-reviewer hold, and priority nonautomation", "repair-severity-card", "CBR Heart and GMUT Mind", "defect severity deliberation, impact class, exploitability placeholder, accessibility cue, confidence, competent-reviewer hold, and priority nonautomation", ["NIST-SP800-61R3", "W3C-WCAG-22", "NIST-SSDF-11"]),
    ("Repair proposal ancestry ledger with issue token, hypothesis branch, rejected alternative, change intent, review checkpoint, and merge-authority reservation", "repair-proposal-ancestry", "Freed ID and CBR Heart", "repair proposal ancestry, issue token, hypothesis branch, rejected alternative, change intent, review checkpoint, and merge-authority reservation", ["W3C-PROV-O", "NIST-SSDF-11", "RFC-8785"]),
    ("Maintainer authorization boundary matrix with repository-role placeholder, least privilege, expiry, dual review, emergency break-glass refusal, and no-appointment claim", "repair-maintainer-boundary", "Freed ID and CBR Heart", "maintainer authorization boundary, repository-role placeholder, least privilege, expiry, dual review, emergency break-glass refusal, and appointment nonclaim", ["NIST-SSDF-11", "RFC-3339", "W3C-VC-DM-20"]),
    ("Change-set provenance envelope with file intent, patch-digest placeholder, build subject, source-material link, review state, and signature nonclaim", "repair-changeset-envelope", "Freed ID and GMUT Mind", "change-set provenance, file intent, patch-digest placeholder, build subject, source-material link, review state, and signature nonclaim", ["SLSA-PROVENANCE-12", "IN-TOTO-SPECS", "RFC-8785"]),
    ("Dependency blast-radius map with direct and transitive distinction, runtime and optional scope, affected artifact set, unknown edge, and deployment-fitness refusal", "repair-blast-radius-map", "GMUT Mind and THOS Body", "dependency blast-radius mapping, direct and transitive distinction, runtime and optional scope, affected artifact set, unknown edge, and deployment-fitness refusal", ["CYCLONEDX-17", "SPDX-30", "CISA-SBOM-RESOURCES"]),
    ("Repair test contract with precondition, failing fixture, expected invariant, regression set, nondeterminism cue, and coverage-completeness refusal", "repair-test-contract", "GMUT Mind and THOS Body", "repair test contract, precondition, failing fixture, expected invariant, regression set, nondeterminism cue, and coverage-completeness refusal", ["NIST-SSDF-11", "W3C-PROV-O", "RFC-8785"]),
    ("Rollback rehearsal docket with restore point, data-shape hold, forward-fix alternative, abort condition, evidence capture, and recovery-readiness refusal", "repair-rollback-rehearsal", "THOS Body and CBR Heart", "rollback rehearsal, restore point, data-shape hold, forward-fix alternative, abort condition, evidence capture, and recovery-readiness refusal", ["NIST-SP800-61R3", "NIST-SSDF-11", "RFC-3339"]),
    ("Accessibility regression witness board with keyboard path, name role and state, focus visibility, noncolour cue, manual-evaluation hold, and complete-accessibility refusal", "repair-accessibility-regression", "THOS Body and CBR Heart", "accessibility regression witness, keyboard path, name role and state, focus visibility, noncolour cue, manual-evaluation hold, and complete-accessibility refusal", ["W3C-WCAG-22", "W3C-PROV-O", "RFC-3339"]),
    ("Privacy regression minimization docket with purpose, data category, retention delta, disclosure path, correction right, legal-review hold, and privacy-complete refusal", "repair-privacy-regression", "CBR Heart and Freed ID", "privacy regression minimization, purpose, data category, retention delta, disclosure path, correction right, legal-review hold, and privacy-complete refusal", ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-3339"]),
    ("Coordinated vulnerability disclosure quarantine with reporter-channel placeholder, embargo clock, affected range, exploit-detail shield, competent-triage hold, and security-verdict refusal", "repair-vulnerability-quarantine", "CBR Heart and THOS Body", "coordinated vulnerability disclosure quarantine, reporter-channel placeholder, embargo clock, affected range, exploit-detail shield, competent-triage hold, and security-verdict refusal", ["NIST-SSDF-11", "NIST-SP800-61R3", "RFC-3339"]),
    ("Patch attestation nonclaim card with SLSA predicate vocabulary, in-toto subject, builder placeholder, material digest, unsigned state, and production-trust refusal", "repair-attestation-nonclaim", "Freed ID and GMUT Mind", "patch attestation nonclaim, SLSA predicate vocabulary, in-toto subject, builder placeholder, material digest, unsigned state, and production-trust refusal", ["SLSA-PROVENANCE-12", "IN-TOTO-SPECS", "RFC-8785"]),
    ("Release approval reservation board with candidate identifier, dependency lock, test-receipt links, risk-acceptance hold, separation of duties, and no-deployment order", "repair-release-reservation", "CBR Heart and THOS Body", "release approval reservation, candidate identifier, dependency lock, test-receipt links, risk-acceptance hold, separation of duties, and deployment-order refusal", ["NIST-SSDF-11", "SLSA-PROVENANCE-12", "W3C-PROV-O"]),
    ("Maintenance-window choreography with freeze start, stakeholder notice, dependency checkpoint, abort trigger, rollback window, readback, and no-operational authorization", "repair-window-choreography", "THOS Body and CBR Heart", "maintenance-window choreography, freeze start, stakeholder notice, dependency checkpoint, abort trigger, rollback window, readback, and operational-authorization refusal", ["NIST-SP800-61R3", "RFC-3339", "W3C-PROV-O"]),
    ("Incident-to-repair handover register with containment state, evidence preservation, unresolved hypothesis, workload cue, next-review checkpoint, and incident-command refusal", "repair-incident-handover", "THOS Body and CBR Heart", "incident-to-repair handover, containment state, evidence preservation, unresolved hypothesis, workload cue, next-review checkpoint, and incident-command refusal", ["NIST-SP800-61R3", "W3C-PROV-O", "RFC-3339"]),
    ("Replacement component equivalence proxy with interface contract, behavioral delta, support-horizon placeholder, migration-cost hold, unknown risk, and procurement refusal", "repair-component-equivalence", "GMUT Mind and CBR Heart", "replacement component equivalence, interface contract, behavioral delta, support-horizon placeholder, migration-cost hold, unknown risk, and procurement refusal", ["SPDX-30", "CYCLONEDX-17", "NIST-SSDF-11"]),
    ("Warranty and license interpretation reservation docket with package context, obligation placeholder, conflicting notice, counsel hold, and legal-conclusion refusal", "repair-legal-reservation", "CBR Heart and Freed ID", "warranty and license interpretation reservation, package context, obligation placeholder, conflicting notice, counsel hold, and legal-conclusion refusal", ["SPDX-30", "W3C-PROV-O", "RFC-3339"]),
    ("Accessible community repair notice with plain-language summary, heading hierarchy, status text, known limitation, correction link, translation hold, and affected-user review", "repair-community-notice", "THOS Body and CBR Heart", "accessible community repair notice, plain-language summary, heading hierarchy, status text, known limitation, correction link, translation hold, and affected-user review reservation", ["W3C-WCAG-22", "NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O"]),
    ("Repair contestation and correction docket with pseudonymous account, competing evidence, uncertainty, response clock, remedy hold, and consensus-promotion refusal", "repair-contestation-docket", "CBR Heart and Freed ID", "repair contestation and correction, pseudonymous account, competing evidence, uncertainty, response clock, remedy hold, and consensus-promotion refusal", ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-3339"]),
    ("Sensitive and culturally restricted maintenance-publication firewall with audience grant, redaction class, community checkpoint, expiry, audit trail, and fail-closed disclosure", "repair-sensitive-publication", "CBR Heart and Freed ID", "sensitive and culturally restricted maintenance-publication firewall, audience grant, redaction class, community checkpoint, expiry, audit trail, and fail-closed disclosure", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES"]),
    ("GMUT Bayesian defect-prior dimensional proxy with likelihood vocabulary, prior provenance, calibration quarantine, sensitivity envelope, and prediction refusal", "gmut-repair-defect-prior", "GMUT Mind", "GMUT Bayesian defect-prior dimensional proxy, likelihood vocabulary, prior provenance, calibration quarantine, sensitivity envelope, and prediction refusal", ["NIST-SSDF-11", "RFC-8785", "W3C-PROV-O"]),
    ("GMUT repairable-system hazard-rate dimensional proxy with observation window, censoring, unit discipline, competing-failure cue, calibration hold, and reliability-claim refusal", "gmut-repair-hazard-rate", "GMUT Mind", "GMUT repairable-system hazard-rate dimensional proxy, observation window, censoring, unit discipline, competing-failure cue, calibration hold, and reliability-claim refusal", ["RFC-3339", "RFC-8785", "W3C-PROV-O"]),
    ("THOS maintainer-shift handover choreography with alert backlog, partial rollback, fatigue and workload cue, safety stop, readback, and operations-decision refusal", "thos-repair-handover", "THOS Body", "THOS maintainer-shift handover choreography, alert backlog, partial rollback, fatigue and workload cue, safety stop, readback, and operations-decision refusal", ["NIST-SP800-61R3", "RFC-3339", "W3C-PROV-O"]),
    ("Freed ID synthetic maintainer-role credential capsule with purpose, audience, minimized claims, expiry, correction, revocation placeholder, and live proof disabled", "freed-id-maintainer-capsule", "Freed ID and CBR Heart", "Freed ID synthetic maintainer-role credential capsule, purpose, audience, minimized claims, expiry, correction, revocation placeholder, and live-proof refusal", ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID synthetic patch provenance card with subject digest, material link, review relation, disclosure shield, unsigned state, and origin nonclaim", "freed-id-patch-card", "Freed ID", "Freed ID synthetic patch provenance card, subject digest, material link, review relation, disclosure shield, unsigned state, and origin nonclaim", ["SLSA-PROVENANCE-12", "IN-TOTO-SPECS", "NZ-PRIVACY-PRINCIPLES"]),
    ("CISA Known Exploited Vulnerabilities no-network query readiness with product placeholder, catalog-version hold, snapshot-digest reservation, zero rows, citation capture, and exploitability refusal", "repair-kev-zero-row", "Freed ID and GMUT Mind", "CISA Known Exploited Vulnerabilities no-network query readiness, product placeholder, catalog-version hold, snapshot-digest reservation, zero rows, citation capture, and exploitability refusal", ["CISA-KEV", "NIST-SSDF-11", "NZ-PRIVACY-PRINCIPLES"]),
    ("CBR public-interest software repair authority non-automation covenant for safety, security, release, maintainer impact, privacy, accessibility, remedy, law, culture, data governance, and Māori authority", "cbr-repair-authority-covenant", "CBR Heart", "public-interest software repair authority non-automation for safety, security, release, maintainer impact, privacy, accessibility, remedy, law, culture, data governance, and Māori authority", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES", "W3C-WCAG-22"]),
]


PROPOSAL_SPECS = [
    ("Typewriter asset passport with synthetic installation token, conveyance class, building hold, controller family, service state, correction lineage, and ownership nonclaim", "typewriter-asset-passport", "THOS Body and Freed ID/CBR Heart", "typewriter asset passport, synthetic installation token, conveyance class, building hold, controller family, service state, correction lineage, and ownership nonclaim", ["NZ-BUILDING-D2", "ASME-A17-1-2025", "W3C-PROV-O"]),
    ("Typewriter service-request intake docket with symptom narrative, caller pseudonym, urgency cue, duplicate link, passenger-impact hold, and diagnosis refusal", "typewriter-service-intake", "THOS Body and CBR Heart", "typewriter service-request intake, symptom narrative, caller pseudonym, urgency cue, duplicate link, passenger-impact hold, and diagnosis refusal", ["NZ-BUILDING-D2", "NIST-SP800-61R3", "NZ-PRIVACY-PRINCIPLES"]),
    ("Typewriter work-order scope and revision ledger with inspection placeholder, task boundary, deviation, parts hold, readback, acceptance reservation, and no-work authorization", "typewriter-work-order-revision", "THOS Body and Freed ID", "typewriter work-order scope and revision ledger, inspection placeholder, task boundary, deviation, parts hold, readback, acceptance reservation, and work-authorization refusal", ["ASME-A17-1-2025", "W3C-PROV-O", "RFC-3339"]),
    ("Out-of-service barrier and tag state board with landing set, notice channel, issue time, issuer-role hold, bypass refusal, correction, and no-isolation claim", "typewriter-out-of-service-hold", "THOS Body and CBR Heart", "out-of-service barrier and tag state, landing set, notice channel, issue time, issuer-role hold, bypass refusal, correction, and isolation-claim refusal", ["NZ-BUILDING-D2", "RFC-3339", "W3C-PROV-O"]),
    ("Typewriter hazardous-energy isolation plan with source classes, disconnect placeholder, stored-energy cue, zero-energy verification hold, handback state, and compliance refusal", "typewriter-energy-isolation", "THOS Body", "typewriter hazardous-energy isolation plan, source classes, disconnect placeholder, stored-energy cue, zero-energy verification hold, handback state, and compliance refusal", ["OSHA-1910-147", "ASME-A17-1-2025", "W3C-PROV-O"]),
    ("Machine-room, pit, and hoistway access reservation with zone token, access basis, companion cue, environmental hazard hold, expiry, and entry-authority refusal", "typewriter-access-reservation", "THOS Body and CBR Heart", "machine-room, pit, and hoistway access reservation, zone token, access basis, companion cue, environmental hazard hold, expiry, and entry-authority refusal", ["NZ-BUILDING-D2", "OSHA-1910-147", "RFC-3339"]),
    ("Typewriter door-zone and interlock inspection-state ledger with entrance token, contact-state placeholder, bypass cue, discrepancy quarantine, correction lineage, and release refusal", "typewriter-door-interlock-state", "THOS Body and GMUT Mind", "typewriter door-zone and interlock inspection-state ledger, entrance token, contact-state placeholder, bypass cue, discrepancy quarantine, correction lineage, and release refusal", ["ASME-A17-1-2025", "NZ-BUILDING-D2", "W3C-PROV-O"]),
    ("Typewriter door-obstruction protective-device check with sensing field, reversal placeholder, dwell interval, blocked-path cue, adjustment hold, and safety-verdict refusal", "typewriter-door-protection-state", "THOS Body and CBR Heart", "typewriter door-obstruction protective-device check, sensing field, reversal placeholder, dwell interval, blocked-path cue, adjustment hold, and safety-verdict refusal", ["NZ-BUILDING-LIFTS", "ASME-A17-1-2025", "RFC-3339"]),
    ("Typewriter brake and traction observation envelope with component token, method hold, direction, speed class, abnormal cue, competent-review reservation, and fitness refusal", "typewriter-brake-traction-state", "THOS Body and GMUT Mind", "typewriter brake and traction observation envelope, component token, method hold, direction, speed class, abnormal cue, competent-review reservation, and fitness refusal", ["ASME-A17-1-2025", "NZ-BUILDING-D2", "W3C-PROV-O"]),
    ("Suspension means and sheave visual-state docket with member token, wear cue, tension-balance placeholder, contamination hold, replacement threshold reservation, and service refusal", "typewriter-suspension-sheave-state", "THOS Body and GMUT Mind", "suspension means and sheave visual-state docket, member token, wear cue, tension-balance placeholder, contamination hold, replacement threshold reservation, and service refusal", ["ASME-A17-1-2025", "W3C-PROV-O", "RFC-8785"]),
    ("Overspeed governor test reservation with device token, rated-speed placeholder, trigger cue, reset state, witnessed-result hold, and no-test certification", "typewriter-governor-test-reservation", "THOS Body and GMUT Mind", "overspeed governor test reservation, device token, rated-speed placeholder, trigger cue, reset state, witnessed-result hold, and test-certification refusal", ["ASME-A17-1-2025", "NZ-BUILDING-D2", "W3C-PROV-O"]),
    ("Typewriter buffer and terminal stopping-device state board with end-of-travel zone, component class, clearance placeholder, contact state, correction hold, and adequacy refusal", "typewriter-terminal-buffer-state", "THOS Body", "typewriter buffer and terminal stopping-device state board, end-of-travel zone, component class, clearance placeholder, contact state, correction hold, and adequacy refusal", ["ASME-A17-1-2025", "NZ-BUILDING-D2", "RFC-8785"]),
    ("Typewriter levelling accuracy and sill-gap measurement envelope with landing token, direction, SI unit, uncertainty, instrument hold, tolerance reservation, and compliance refusal", "typewriter-levelling-gap-envelope", "GMUT Mind and THOS Body", "typewriter levelling accuracy and sill-gap measurement envelope, landing token, direction, SI unit, uncertainty, instrument hold, tolerance reservation, and compliance refusal", ["NZ-BUILDING-LIFTS", "ASME-A17-1-2025", "W3C-PROV-O"]),
    ("Rated-load plate and capacity evidence board with car token, displayed value, unit, source-document hold, discrepancy state, correction path, and loading-authorization refusal", "typewriter-rated-load-board", "THOS Body and CBR Heart", "rated-load plate and capacity evidence board, car token, displayed value, unit, source-document hold, discrepancy state, correction path, and loading-authorization refusal", ["NZ-BUILDING-D2", "ASME-A17-1-2025", "W3C-PROV-O"]),
    ("Typewriter emergency alarm and two-way communication accessibility docket with control location, visual and audible feedback, connection placeholder, fallback hold, manual review, and conformance refusal", "typewriter-emergency-communication", "THOS Body and CBR Heart", "typewriter emergency alarm and two-way communication accessibility docket, control location, visual and audible feedback, connection placeholder, fallback hold, manual review, and conformance refusal", ["NZ-BUILDING-LIFTS", "W3C-WCAG-22", "NZ-BUILDING-D2"]),
    ("Typewriter fire-service and recall interface test reservation with mode token, input placeholder, landing destination, conflicting state, fire-authority hold, restoration cue, and no-certification claim", "typewriter-fire-recall-reservation", "THOS Body and CBR Heart", "typewriter fire-service and recall interface test reservation, mode token, input placeholder, landing destination, conflicting state, fire-authority hold, restoration cue, and certification refusal", ["ASME-A17-1-2025", "NZ-BUILDING-D2", "W3C-PROV-O"]),
    ("Typewriter entrapment incident and passenger-welfare handover with call token, location hold, communication state, medical cue, emergency-controller reservation, readback, and rescue refusal", "typewriter-entrapment-handover", "THOS Body and CBR Heart", "typewriter entrapment incident and passenger-welfare handover, call token, location hold, communication state, medical cue, emergency-controller reservation, readback, and rescue refusal", ["NIST-SP800-61R3", "NZ-BUILDING-D2", "RFC-3339"]),
    ("Typewriter replacement-part provenance and compatibility quarantine with part token, source document, supersession, interface cue, procurement hold, installation reservation, and equivalence refusal", "typewriter-part-provenance", "Freed ID and GMUT Mind", "typewriter replacement-part provenance and compatibility quarantine, part token, source document, supersession, interface cue, procurement hold, installation reservation, and equivalence refusal", ["ASME-A17-1-2025", "W3C-PROV-O", "RFC-8785"]),
    ("Typewriter controller software and configuration change lineage with version token, parameter class, change purpose, backup digest placeholder, review hold, rollback cue, and production-change refusal", "typewriter-control-change-lineage", "Freed ID and THOS Body", "typewriter controller software and configuration change lineage, version token, parameter class, change purpose, backup digest placeholder, review hold, rollback cue, and production-change refusal", ["W3C-PROV-O", "RFC-8785", "ASME-A17-1-2025"]),
    ("Typewriter preventive-maintenance schedule ledger with task family, interval basis, due window, deferral reason, workload cue, escalation hold, and maintenance-sufficiency refusal", "typewriter-maintenance-schedule", "THOS Body and CBR Heart", "typewriter preventive-maintenance schedule ledger, task family, interval basis, due window, deferral reason, workload cue, escalation hold, and maintenance-sufficiency refusal", ["ASME-A17-1-2025", "RFC-3339", "W3C-PROV-O"]),
    ("Accessible typewriter outage and alternative-route notice with heading hierarchy, affected landing set, status provenance, tactile and auditory cue hold, correction path, and affected-user review reserved", "typewriter-outage-accessible-notice", "CBR Heart and THOS Body", "accessible typewriter outage and alternative-route notice, heading hierarchy, affected landing set, status provenance, tactile and auditory cue hold, correction path, and affected-user review reservation", ["NZ-BUILDING-LIFTS", "W3C-WCAG-22", "W3C-PROV-O"]),
    ("Typewriter evidence amendment and supersession graph with field-level delta, origin class, immutable prior, rebuttal edge, review-owner reservation, and decision-rights refusal", "typewriter-record-amendment-graph", "CBR Heart and Freed ID", "typewriter evidence amendment and supersession graph, field-level delta, origin class, immutable prior, rebuttal edge, review-owner reservation, and decision-rights refusal", ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-3339"]),
    ("Typewriter access-log privacy minimization and disclosure firewall with purpose, event class, retention window, role hold, correction right, legal-review reservation, and privacy-complete refusal", "typewriter-access-log-privacy", "CBR Heart and Freed ID", "typewriter access-log privacy minimization and disclosure firewall, purpose, event class, retention window, role hold, correction right, legal-review reservation, and privacy-complete refusal", ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-3339"]),
    ("GMUT traction-rope coupled-oscillator dimensional proxy with car and counterweight domains, stiffness and damping units, boundary signs, calibration quarantine, and motion-prediction refusal", "gmut-typewriter-rope-dynamics", "GMUT Mind", "GMUT traction-rope coupled-oscillator dimensional proxy, car and counterweight domains, stiffness and damping units, boundary signs, calibration quarantine, and motion-prediction refusal", ["ASME-A17-1-2025", "RFC-8785", "W3C-PROV-O"]),
    ("GMUT typewriter braking-energy and thermal-dissipation dimensional proxy with mass and speed placeholders, energy and power units, loss terms, measurement hold, and safety-margin refusal", "gmut-typewriter-braking-thermal", "GMUT Mind", "GMUT typewriter braking-energy and thermal-dissipation dimensional proxy, mass and speed placeholders, energy and power units, loss terms, measurement hold, and safety-margin refusal", ["ASME-A17-1-2025", "RFC-8785", "W3C-PROV-O"]),
    ("THOS typewriter-maintenance shift handover choreography with isolation state, defect queue, parts hold, incomplete test, workload cue, safety stop, readback, and operational-decision refusal", "thos-typewriter-shift-handover", "THOS Body", "THOS typewriter-maintenance shift handover choreography, isolation state, defect queue, parts hold, incomplete test, workload cue, safety stop, readback, and operational-decision refusal", ["NIST-SP800-61R3", "RFC-3339", "W3C-PROV-O"]),
    ("Freed ID synthetic maintenance-access purpose matrix with capability label, typewriter-zone scope, double-bind expiry, disclosure minimum, status hold, and live-authorization refusal", "freed-id-typewriter-purpose-matrix", "Freed ID and CBR Heart", "Freed ID synthetic maintenance-access purpose matrix, capability label, typewriter-zone scope, double-bind expiry, disclosure minimum, status hold, and live-authorization refusal", ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID synthetic typewriter-maintenance record provenance card with subject digest, work-order relation, inspection-state hold, disclosure shield, unsigned state, and origin nonclaim", "freed-id-typewriter-record-card", "Freed ID", "Freed ID synthetic typewriter-maintenance record provenance card, subject digest, work-order relation, inspection-state hold, disclosure shield, unsigned state, and origin nonclaim", ["W3C-VC-DM-20", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("CPSC NEISS elevator and escalator no-network query readiness with product-code placeholder, treatment-year hold, weight and variance reservation, zero rows, citation capture, and injury-inference refusal", "typewriter-neiss-zero-row", "GMUT Mind and CBR Heart", "CPSC NEISS elevator and escalator no-network query readiness, product-code placeholder, treatment-year hold, weight and variance reservation, zero rows, citation capture, and injury-inference refusal", ["CPSC-NEISS", "RFC-8785", "NZ-PRIVACY-PRINCIPLES"]),
    ("CBR typewriter safety, accessibility, outage, privacy, rescue, building access, remedy, law, culture, data governance, affected-party, and Māori-authority non-automation covenant", "cbr-typewriter-authority-covenant", "CBR Heart", "CBR typewriter safety, accessibility, outage, privacy, rescue, building access, remedy, law, culture, data governance, affected-party, and Māori-authority non-automation covenant", ["NZ-BUILDING-D2", "NZ-BUILDING-LIFTS", "TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS"]),
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


_INHERITED_SKILL_SPECS_UNUSED = [
    ("ghc-family-repair-intake-provenance", "Freeze synthetic asset, defect-intake, reproduction, correction, and ownership boundaries."),
    ("ghc-family-repair-component-boundary", "Separate component and dependency structure from inventory completeness, license, procurement, and deployment claims."),
    ("ghc-family-repair-triage-nonpromotion", "Expose impact, severity, exploitability, and priority cues without issuing professional or operational decisions."),
    ("ghc-family-repair-changeset-attestation", "Preserve patch, material, builder, review, unsigned-state, and production-trust boundaries."),
    ("ghc-family-repair-test-rollback-evidence", "Constrain test, nondeterminism, rollback, forward-fix, and recovery-readiness evidence."),
    ("ghc-family-repair-privacy-accessibility", "Structure privacy and accessibility regression witnesses while reserving legal and affected-user evaluation."),
    ("ghc-family-repair-vulnerability-reserve", "Fail closed around vulnerability reporting, embargo, exploit detail, triage, notification, and security authority."),
    ("ghc-family-repair-release-handover", "Constrain maintenance windows, incidents, release reservations, readback, workload, and handover."),
    ("ghc-family-repair-freed-id-disclosure", "Constrain synthetic maintainer identity, purpose, disclosure, status, proof, and patch-lineage claims."),
    ("ghc-family-repair-cultural-authority", "Fail closed around restricted knowledge, community protocol, remedy, governance, and Māori authority."),
]


SKILL_SPECS = [
    ("ghc-family-typewriter-asset-work-order", "Freeze synthetic typewriter asset, service-intake, work-order revision, correction, and ownership boundaries."),
    ("ghc-family-typewriter-isolation-hold", "Separate out-of-service and hazardous-energy hold structure from real isolation, testing, and return-to-service authority."),
    ("ghc-family-typewriter-access-boundary", "Fail closed around machine-room, pit, hoistway, building, passenger, and technician access decisions."),
    ("ghc-family-typewriter-door-safety-state", "Model synthetic door-zone, interlock, and obstruction-protection states without issuing a safety verdict."),
    ("ghc-family-typewriter-motion-component-state", "Constrain brake, traction, suspension, governor, buffer, levelling, and rated-load evidence to typed observations."),
    ("ghc-family-typewriter-emergency-accessibility", "Structure emergency communication, fire-interface, entrapment, outage, and alternative-route records while reserving real evaluation."),
    ("ghc-family-typewriter-part-config-provenance", "Preserve replacement-part and controller-configuration provenance, review, rollback, and production-change boundaries."),
    ("ghc-family-typewriter-schedule-handover", "Constrain preventive-maintenance schedules, workload, incomplete tests, correction readback, and shift handover."),
    ("ghc-family-typewriter-freed-id-provenance", "Constrain synthetic technician-role and maintenance-record identity, disclosure, proof, status, and lineage claims."),
    ("ghc-family-typewriter-authority-reservation", "Fail closed around safety, access, rescue, remedy, law, culture, governance, affected-party, and Māori authority."),
]


_INHERITED_RUNNER_SPECS_UNUSED = [
    ("ghc_family_repair_intake_provenance.py", "repair-request-intake"),
    ("ghc_family_repair_component_boundary.py", "repair-component-inventory"),
    ("ghc_family_repair_triage_nonpromotion.py", "repair-severity-card"),
    ("ghc_family_repair_changeset_attestation.py", "repair-changeset-envelope"),
    ("ghc_family_repair_test_rollback.py", "repair-rollback-rehearsal"),
    ("ghc_family_repair_privacy_accessibility.py", "repair-accessibility-regression"),
    ("ghc_family_repair_vulnerability_reserve.py", "repair-vulnerability-quarantine"),
    ("ghc_family_repair_release_handover.py", "repair-window-choreography"),
    ("ghc_family_repair_freed_id_disclosure.py", "freed-id-maintainer-capsule"),
    ("ghc_family_repair_cultural_authority.py", "cbr-repair-authority-covenant"),
]


RUNNER_SPECS = [
    ("ghc_family_typewriter_asset_work_order.py", "typewriter-work-order-revision"),
    ("ghc_family_typewriter_isolation_hold.py", "typewriter-energy-isolation"),
    ("ghc_family_typewriter_access_boundary.py", "typewriter-access-reservation"),
    ("ghc_family_typewriter_door_safety_state.py", "typewriter-door-interlock-state"),
    ("ghc_family_typewriter_motion_component_state.py", "typewriter-brake-traction-state"),
    ("ghc_family_typewriter_emergency_accessibility.py", "typewriter-emergency-communication"),
    ("ghc_family_typewriter_part_config_provenance.py", "typewriter-control-change-lineage"),
    ("ghc_family_typewriter_schedule_handover.py", "thos-typewriter-shift-handover"),
    ("ghc_family_typewriter_freed_id_provenance.py", "freed-id-typewriter-purpose-matrix"),
    ("ghc_family_typewriter_authority_reservation.py", "cbr-typewriter-authority-covenant"),
]


def negative(number: int, signature: str, observed: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6573-X1-N{number:02d}",
        "scope": "startup_and_x1",
        "signature": signature,
        "observed": observed,
        "credit": 0,
        "retained": True,
        "recovery": recovery,
        "recurrence_guard": guard,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


_INHERITED_X1_OPERATIONAL_NEGATIVES_UNUSED = [
    negative(1, "completion-gate-skill-login-shell-timeout", "The first login-shell read of the selected completion-gate skill exceeded its bound and returned no complete instruction evidence.", "Repeat only the same literal skill read without login-shell startup and continue through EOF.", "Keep instruction reads scalar and disable unnecessary login-shell initialization on bounded Windows probes."),
    negative(2, "powershell-d-candidate-probe-empty-pipe-element", "The first D-drive candidate probe contained an empty PowerShell pipeline element and failed before producing a path result.", "Materialize the bounded candidate list, then inspect each literal path in a separate pipeline.", "Materialize foreach output before piping and validate the expression before combining probes."),
    negative(3, "narrowed-d-candidate-probe-timeout", "A narrowed read-only D-drive candidate probe exceeded its outer bound without a complete source result.", "Use the exact activation branch and repository-relative baton to address one known source worktree directly.", "Prefer exact activation anchors over exploratory directory traversal when the source branch and baton are already supplied."),
    negative(4, "powershell-metadata-size-foreach-pipe-parser", "A metadata-size summary piped directly from foreach and failed during PowerShell parsing.", "Materialize each metadata row first, then pipe the completed array to the formatter.", "Separate collection from formatting in PowerShell metadata audits."),
    negative(5, "powershell-convert-tohexstring-unavailable", "The first external receipt digest sweep used Convert.ToHexString, which was unavailable in the installed PowerShell runtime.", "Repeat the bounded candidate-directory sweep with Get-FileHash SHA256 and retain a no-match result without expanding scope.", "Use Get-FileHash for portable Windows SHA-256 sweeps unless the runtime capability was proved first."),
    negative(6, "broad-external-receipt-filename-search-timeout", "A recursive exact-filename search across the archive exceeded 120 seconds and returned no complete result.", "Stop broad searching, retain the activation-supplied receipt digest, and rely only on exact source equality, ancestry, manifest replay, and the supplied canonical counts.", "Do not search the whole archive for external receipts when the activation provides a digest and repository verification is independently bounded."),
    negative(7, "additive-worktree-timeout-with-partial-checkout", "The additive D-first worktree wrapper timed out after registration, leaving the correct branch and HEAD with an incomplete 60,011-deletion checkout.", "Audit registration, branch, HEAD, process and lock state, then restore the worktree in place from HEAD and prove zero deleted, modified, and untracked files.", "After a mutating timeout, inspect durable state before retrying and recover the exact registered lane without creating a duplicate."),
    negative(8, "combined-post-recovery-audit-timeout", "The first combined HEAD, branch, status, and top-level audit timed out and returned no complete cleanliness proof.", "Run exact HEAD and branch probes separately, then count deleted, modified, and untracked paths with bounded scalar Git commands.", "Keep large-worktree cleanliness checks independent rather than bundling them into one orchestration call."),
    negative(9, "encoding-rendered-patch-context-mismatch", "Three context-rich patches did not match copied files at rendered encoding boundaries and changed nothing.", "Stop context retries, bind the replacement to ASCII-safe function or file anchors, write UTF-8 without a byte-order mark, and inspect the exact result.", "Avoid using terminal-rendered mojibake as patch context; bind edits to ASCII-safe anchors or complete UTF-8 file content."),
    negative(10, "combined-replacement-precondition-mismatch", "A bounded multi-replacement command stopped before writing because one expected Unicode line did not satisfy its regex precondition.", "Inspect exact UTF-8 source lines, then apply only small verified patches whose preconditions are present.", "Require every combined transformation precondition before writing and fall back to audited exact hunks on any mismatch."),
    negative(11, "powershell-composite-unicode-audit-parse-failure", "A composite stale-label audit embedded terminal-rendered Unicode in a PowerShell string and failed during parsing before scanning.", "Split the audit into ASCII-only stale-label patterns and a separate non-ASCII code-point inventory.", "Never copy rendered mojibake into a PowerShell regex literal; keep encoding and stale-label audits separate."),
    negative(12, "sequential-rg-no-match-treated-as-wrapper-failure", "A sequential multi-file audit stopped when an expected no-match ripgrep result returned exit code one.", "Run one bounded search across all declared files and explicitly treat ripgrep exit code one as a valid no-match state.", "Normalize documented search-tool no-match exits before composing sequential audits."),
    negative(13, "powershell-literal-path-existence-foreach-pipe-recurrence", "A literal-path existence audit repeated the PowerShell foreach-to-pipeline parser fault and failed before checking any path.", "Materialize all literal-path result rows first, then pass the completed array to JSON formatting.", "Encode the materialize-before-pipe rule directly in every PowerShell audit that begins with foreach."),
]


X1_OPERATIONAL_NEGATIVES = [
    negative(1, "combined-memory-and-worktree-quick-pass-timeout", "The first combined memory and worktree discovery probe exceeded ten seconds and returned no complete result.", "Split memory registry lookup from exact worktree inspection and increase only the bounded read timeout.", "Keep memory, filesystem, and Git discovery as independent scalar probes."),
    negative(2, "wrong-relative-memory-registry-path", "The first registry read addressed MEMORY.md relative to the current directory and received file-not-found.", "Use the exact memory-root literal path supplied by the desktop context.", "Resolve memory paths from the declared memory base rather than the repository working directory."),
    negative(3, "memory-registry-ripgrep-timeout", "The corrected memory-registry ripgrep probe exceeded ten seconds without a complete result.", "Use bounded Select-String and exact line reads for the small set of relevant entries.", "Prefer exact registry sections over a broad search when continuity keywords are already known."),
    negative(4, "combined-source-state-status-timeout", "A combined source HEAD, branch, status, and remote-state probe exceeded its bound without complete evidence.", "Run exact HEAD, branch, tracked, untracked, upstream, tracking, and live-remote probes separately.", "Split local Git state from network and large-worktree status checks."),
    negative(5, "additive-worktree-wrapper-timeout-after-durable-success", "The D-first additive worktree command exceeded its outer bound after the intended branch, path, and exact HEAD had been created.", "Audit worktree registration, branch, HEAD, process and lock state, and cleanliness; do not retry the mutation.", "After any mutating timeout, inspect durable state before deciding whether recovery is needed."),
    negative(6, "git-process-json-disappearance-race", "A read-only Git process inventory emitted rows but returned nonzero because a process disappeared during property collection.", "Repeat only a scalar Git-process count after quiescence and verify zero active processes and locks.", "Use stable scalar process counts before optional detail collection on short-lived processes."),
    negative(7, "post-checkout-git-diff-quiet-timeout", "The first working-tree diff-quiet check exceeded its bound and produced no complete cleanliness evidence.", "Use bounded porcelain status without untracked files, then a separate untracked-path query.", "Avoid whole-tree diff traversal when exact status categories provide the needed invariant."),
    negative(8, "novelty-foreach-pipe-parser-fault", "The first novelty summary piped directly from a PowerShell foreach expression and failed with an empty pipeline element.", "Materialize proposal rows before formatting and keep novelty computation inside the phase builder.", "Assign foreach output to a variable before every PowerShell pipeline."),
    negative(9, "windows-ripgrep-wildcard-literal-fault", "A test inspection passed a Windows wildcard as a literal ripgrep filename and returned invalid-path syntax.", "Use rg glob options or enumerate exact file paths before searching.", "Never pass an unexpanded Windows wildcard as a positional filename to ripgrep."),
    negative(10, "two-file-symbol-search-timeout", "A narrow two-file symbol search still exceeded fifteen seconds on the large Windows worktree.", "Inspect one exact file at a time with bounded Select-String and a larger read-only timeout.", "Keep large-worktree inspection literal, one file per probe, with explicit bounds."),
    negative(11, "combined-catalogue-inspection-timeout", "A combined multi-pattern catalogue inspection exceeded twenty seconds without output.", "Use one bounded ripgrep call with a small match cap and a longer read-only timeout.", "Prefer indexed exact-pattern probes over full PowerShell line materialization for large files."),
    negative(12, "catalogue-getitem-startup-timeout", "Even a short Get-Item probe exceeded fifteen seconds during transient Windows filesystem latency.", "Allow the filesystem to quiesce and repeat only the exact indexed search with a bounded sixty-second ceiling.", "Treat transient read latency as zero-credit evidence and avoid stacking concurrent filesystem probes."),
    negative(13, "unicode-context-apply-patch-verification-failure", "A large semantic replacement was rejected because terminal-rendered UTF-8 text did not match the file's actual bytes; no file changed.", "Use ASCII-safe declaration anchors and activate new lists without matching rendered Unicode context.", "Never use terminal mojibake as patch context; anchor semantic edits on exact ASCII syntax."),
    negative(14, "unicode-overview-apply-patch-verification-failure", "A broader overview replacement was also rejected at a terminal-rendered Unicode boundary and changed nothing.", "Leave the inherited template function inert, add a new UTF-8 function at an ASCII-only declaration boundary, and select it explicitly.", "Prefer additive UTF-8 replacement functions over repeated context matching when inherited rendered bytes are uncertain."),
    negative(15, "desktop-executable-version-metadata-empty", "The running Codex executable exposed neither file-version nor product-version metadata.", "Read the installed OpenAI.Codex Appx package version without changing package state.", "Use the signed package registry as the desktop version source when executable metadata is empty."),
    negative(16, "multi-file-patch-literal-plus-context-error", "A multi-file count update included a literal patch-prefix character in its expected source context and was rejected without changing either file.", "Split the update by file and use the exact source line without patch-control characters.", "Keep multi-file patches small and inspect literal hunk context before applying."),
    negative(17, "source-closeout-count-mistaken-for-final-sealed-total", "The first Auren source model treated Ilyra's 15,246 closeout count plus two final-preparation failures as external, although the committed final register already retains both and reports 15,248.", "Inspect the authoritative final negative-register fields, preserve 15,248 as the sealed activation baseline, and add no invented external count.", "Read closeout_effective_count, final_preparation_count, and effective_count together before modelling inherited totals."),
    negative(18, "activation-baton-checkout-hash-used-as-git-blob-hash", "The first x1 build stopped before packet writes because the expected baton digest described CRLF checkout bytes rather than the immutable Git blob.", "Measure both domains, bind the builder to the exact source-commit Git-blob SHA-256, and retain the checkout digest as a separate receipt field.", "Declare the hash domain for every historical content seal before validation."),
    negative(19, "semantic-neighbor-threshold-rejected-two-proposals", "The second x1 build stopped before packet writes because proposal 22 scored 0.7000 and proposal 27 scored 0.7619 against Ilyra semantic neighbors, above the frozen 0.60 threshold.", "Rewrite both mechanisms around distinct amendment-graph and purpose-matrix contracts, then rerun the unchanged all-2,440-title tribunal.", "Never lower the novelty threshold to admit a duplicate; rewrite or reject the proposal."),
    negative(20, "stale-label-probe-expanded-frozen-chain-output", "The first current-label search included the one-line 2,440-row frozen proposal index, producing an oversized inherited-history listing that was truncated and could not prove current-label hygiene.", "Exclude declared ancestry and nearest-neighbor evidence files, then scan all remaining current phase surfaces with the unchanged stale-label patterns.", "Separate historical evidence fields from current lifecycle-label scans and cap diagnostic output."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6573-SAFE-{index:03d}",
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
        "task_id": f"V6573-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6573-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, and stale-label cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]


# Active Auren v657-v3 catalogue. The inherited scaffold above remains visible
# for lineage review, but only these reassigned values are imported by phase data.
def auren_source(
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
    auren_source(
        "CCI-INDUSTRIAL-COLLECTIONS",
        "Industrial collections",
        "Canadian Conservation Institute, Government of Canada",
        "https://www.canada.ca/en/conservation-institute/services/care-objects/industrial-collections.html",
        "current",
        "industrial-object care and material-risk vocabulary only; no conservation treatment or professional conclusion",
    ),
    auren_source(
        "CCI-LUBRICATION-15-5",
        "Lubrication for Industrial Collections, CCI Notes 15/5",
        "Canadian Conservation Institute, Government of Canada",
        "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/lubrication-industrial-collections.html",
        "current",
        "lubricant, contact, corrosion, and moving-part vocabulary only; no material choice or application instruction",
    ),
    auren_source(
        "CCI-TRADE-LITERATURE-15-6",
        "Trade Literature for Industrial Collections, CCI Notes 15/6",
        "Canadian Conservation Institute, Government of Canada",
        "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/trade-literature-industrial-collections.html",
        "current",
        "manual, parts-list, manufacturer-claim, comparison, and source-uncertainty vocabulary only",
    ),
    auren_source(
        "CCI-RUBBER-15-7",
        "Rubber Components in Industrial Collections, CCI Notes 15/7",
        "Canadian Conservation Institute, Government of Canada",
        "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/rubber-components-industrial-collections.html",
        "current",
        "rubber ageing, condition, original-part, replica, and storage vocabulary only; no replacement decision",
    ),
    auren_source(
        "SMITHSONIAN-OPEN-ACCESS",
        "Open Access Developer Tools",
        "Smithsonian Institution",
        "https://www.si.edu/openaccess/devtools",
        "current",
        "public collection-metadata and API-readiness vocabulary only; no network query, attribution conclusion, authenticity claim, or rights decision",
    ),
    auren_source(
        "OSHA-1910-147",
        "29 CFR 1910.147 Control of hazardous energy",
        "United States Occupational Safety and Health Administration",
        "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147",
        "current",
        "hazardous-energy vocabulary only; no workplace procedure, training, isolation, or compliance determination",
    ),
    auren_source(
        "NIST-SP800-61R3",
        "Incident Response Recommendations and Considerations for Cybersecurity Risk Management",
        "National Institute of Standards and Technology",
        "https://csrc.nist.gov/pubs/sp/800/61/r3/final",
        "current",
        "incident, evidence, communication, recovery, and handover vocabulary only",
    ),
    auren_source(
        "W3C-PROV-O",
        "PROV-O: The PROV Ontology",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        "entity, activity, attribution, derivation, revision, invalidation, and delegation lineage",
    ),
    auren_source(
        "RFC-3339",
        "RFC 3339: Date and Time on the Internet",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic UTC timestamps, review windows, expiry, corrections, and handovers",
    ),
    auren_source(
        "RFC-8785",
        "RFC 8785: JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic contracts, receipts, manifests, and evidence cards",
    ),
    auren_source(
        "W3C-WCAG-22",
        "Web Content Accessibility Guidelines 2.2",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/WCAG22/",
        "current",
        "structural accessibility vocabulary with manual and affected-user evaluation reserved",
    ),
    auren_source(
        "NZ-PRIVACY-PRINCIPLES",
        "Privacy Act 2020 information privacy principles",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        "purpose, collection, fairness, security, access, correction, retention, use, and disclosure reservations only",
    ),
    auren_source(
        "TMR-PRINCIPLES",
        "Principles of Māori Data Sovereignty",
        "Te Mana Raraunga",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "current",
        "authority-reservation context only; Māori data governance remains with Māori authorities",
    ),
    auren_source(
        "LOCAL-CONTEXTS-LABELS",
        "Traditional Knowledge and Biocultural Labels",
        "Local Contexts",
        "https://localcontexts.org/labels/about-the-labels/",
        "current",
        "community-defined provenance, protocol, and permission vocabulary with community authority reserved",
    ),
    auren_source(
        "W3C-VC-DM-20",
        "Verifiable Credentials Data Model v2.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-model/",
        "current",
        "synthetic credential vocabulary only; no real issuer, holder, verifier, proof, status, or trust decision",
    ),
    auren_source(
        "W3C-DID-10",
        "Decentralized Identifiers v1.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/did-1.0/",
        "stable",
        "synthetic identifier-document vocabulary only; no live method, resolution, key, controller, or trust claim",
    ),
]


PROTECTED_GATES = [
    "real_owners_customers_donors_collectors_repairers_conservators_curators_communities_and_affected_parties",
    "real_typewriters_components_tools_materials_workshops_collections_accounts_and_records",
    "real_operation_energization_disassembly_cleaning_lubrication_adjustment_repair_conservation_packing_shipping_or_release",
    "real_measurements_statistics_authenticity_age_origin_value_performance_reliability_or_empirical_confirmation",
    "professional_typewriter_repair_conservation_electrical_safety_collections_accessibility_privacy_or_workplace_authority",
    "sensitive_personal_contact_ownership_work_log_image_location_traditional_knowledge_and_culturally_restricted_information",
    "production_identity_live_keys_signatures_proofs_resolution_status_revocation_interoperability_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_indigenous_traditional_knowledge_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_treatment_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def auren_proposal(
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
        "proposal_id": f"V6573-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable synthetic evidence "
            "obligations while refusing unsupported empirical, professional, security, "
            "accessibility, privacy, identity, production, legal, cultural, Māori-authority, "
            "or Stage 20 promotion."
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
            "The valid synthetic fixture passes, five preregistered mutations are rejected, "
            "and the receipt grants no real owner, customer, donor, repairer, conservator, "
            "typewriter, treatment, professional, production, legal, cultural, Māori-authority, "
            "identity, accessibility-complete, privacy-complete, security-complete, independent-"
            "reproduction, Theory-of-Everything, or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real "
            "people, typewriters, collections, tools, materials, accounts, records, workshops, "
            "treatments, professional decisions, sibling lanes, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Typewriter intake provenance docket with synthetic case token, presented-custody claim, component count, visible-state boundary, personal-data minimum, correction route, and work-start refusal", "typewriter-intake-provenance", "Freed ID and CBR Heart", "typewriter intake provenance, synthetic case token, presented-custody claim, component count, visible-state boundary, personal-data minimum, correction route, and work-start refusal", ["CCI-INDUSTRIAL-COLLECTIONS", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Typewriter make, model, serial-evidence, manufacture-date placeholder, source class, collision quarantine, authenticity hold, and identification nonclaim ledger", "typewriter-identity-ledger", "Freed ID and CBR Heart", "typewriter make, model, serial evidence, manufacture-date placeholder, source class, collision quarantine, authenticity hold, and identification nonclaim", ["CCI-TRADE-LITERATURE-15-6", "W3C-PROV-O", "RFC-8785"]),
    ("Typewriter work-scope and revision docket with requested action, excluded action, approval placeholder, deviation, correction readback, and no-work authorization", "typewriter-scope-revision", "CBR Heart and Freed ID", "typewriter work scope and revision, requested action, excluded action, approval placeholder, deviation, correction readback, and work-authorization refusal", ["CCI-TRADE-LITERATURE-15-6", "W3C-PROV-O", "RFC-3339"]),
    ("Typewriter received-condition and detachable-accessory inventory with case, cover, key, spool, tool, loose-part token, discrepancy, and valuation refusal", "typewriter-condition-inventory", "Freed ID and THOS Body", "typewriter received-condition and detachable-accessory inventory, case, cover, key, spool, tool, loose-part token, discrepancy, and valuation refusal", ["CCI-INDUSTRIAL-COLLECTIONS", "W3C-PROV-O", "RFC-8785"]),
    ("Typewriter keyboard, keylever, linkage, typebar, type guide, and segment-slot topology graph with orphan quarantine and no-disassembly instruction", "typewriter-keyboard-topology", "GMUT Mind and Freed ID", "typewriter keyboard, keylever, linkage, typebar, type guide, and segment-slot topology graph, orphan quarantine, and disassembly-instruction refusal", ["CCI-TRADE-LITERATURE-15-6", "W3C-PROV-O", "RFC-8785"]),
    ("Typewriter carriage, rail, rack, pinion, escapement, drawband, and return-path state envelope with motion hold and fitness refusal", "typewriter-carriage-state", "GMUT Mind and THOS Body", "typewriter carriage, rail, rack, pinion, escapement, drawband, and return-path state, motion hold, and fitness refusal", ["CCI-TRADE-LITERATURE-15-6", "CCI-LUBRICATION-15-5", "W3C-PROV-O"]),
    ("Typewriter platen, feed roller, paper bail, pressure roller, and rubber-component condition docket with material uncertainty, replacement hold, and serviceability refusal", "typewriter-rubber-state", "THOS Body and CBR Heart", "typewriter platen, feed roller, paper bail, pressure roller, and rubber-component condition, material uncertainty, replacement hold, and serviceability refusal", ["CCI-RUBBER-15-7", "CCI-INDUSTRIAL-COLLECTIONS", "W3C-PROV-O"]),
    ("Typewriter ribbon, spool, eyelet, reverse mechanism, ink class, substitution provenance, contamination hold, and compatibility nonclaim ledger", "typewriter-ribbon-provenance", "Freed ID and GMUT Mind", "typewriter ribbon, spool, eyelet, reverse mechanism, ink class, substitution provenance, contamination hold, and compatibility nonclaim", ["CCI-TRADE-LITERATURE-15-6", "CCI-RUBBER-15-7", "W3C-PROV-O"]),
    ("Typewriter segment and typebar alignment observation envelope with glyph token, strike-position placeholder, collision cue, adjustment hold, and quality-verdict refusal", "typewriter-alignment-observation", "GMUT Mind and THOS Body", "typewriter segment and typebar alignment observation, glyph token, strike-position placeholder, collision cue, adjustment hold, and quality-verdict refusal", ["CCI-TRADE-LITERATURE-15-6", "W3C-PROV-O", "RFC-3339"]),
    ("Typewriter mainspring and drawband energy-state reservation with wind-state placeholder, attachment topology, stored-energy cue, competent-review hold, and adjustment refusal", "typewriter-spring-energy-hold", "THOS Body and GMUT Mind", "typewriter mainspring and drawband energy-state reservation, wind-state placeholder, attachment topology, stored-energy cue, competent-review hold, and adjustment refusal", ["CCI-LUBRICATION-15-5", "CCI-INDUSTRIAL-COLLECTIONS", "OSHA-1910-147"]),
    ("Typewriter tabulator, margin stop, line-space, backspace, and carriage-release state board with setting provenance, conflict quarantine, and operation refusal", "typewriter-control-state", "GMUT Mind and Freed ID", "typewriter tabulator, margin stop, line-space, backspace, and carriage-release state, setting provenance, conflict quarantine, and operation refusal", ["CCI-TRADE-LITERATURE-15-6", "W3C-PROV-O", "RFC-8785"]),
    ("Manual and electric typewriter power-class boundary with cord, switch, motor, capacitor placeholder, hazardous-energy hold, isolation reservation, and no-energization rule", "typewriter-power-boundary", "THOS Body and CBR Heart", "manual and electric typewriter power-class boundary, cord, switch, motor, capacitor placeholder, hazardous-energy hold, isolation reservation, and energization refusal", ["OSHA-1910-147", "CCI-INDUSTRIAL-COLLECTIONS", "W3C-PROV-O"]),
    ("Typewriter fastener, spring, linkage, keytop, type slug, and replacement-part provenance ledger with declared source, interchangeability hold, and procurement refusal", "typewriter-part-provenance", "Freed ID and GMUT Mind", "typewriter fastener, spring, linkage, keytop, type slug, and replacement-part provenance, declared source, interchangeability hold, and procurement refusal", ["CCI-TRADE-LITERATURE-15-6", "W3C-PROV-O", "RFC-8785"]),
    ("Typewriter cleaning-material compatibility docket with substrate class, finish, label source, test-area placeholder, residue cue, ventilation hold, and treatment refusal", "typewriter-cleaning-boundary", "THOS Body and CBR Heart", "typewriter cleaning-material compatibility, substrate class, finish, label source, test-area placeholder, residue cue, ventilation hold, and treatment refusal", ["CCI-INDUSTRIAL-COLLECTIONS", "NIST-SP800-61R3", "W3C-PROV-O"]),
    ("Typewriter lubrication location and material ledger with bearing point, declared lubricant, source document, prior residue, quantity placeholder, migration hold, and no-application instruction", "typewriter-lubrication-ledger", "THOS Body and Freed ID", "typewriter lubrication location and material, bearing point, declared lubricant, source document, prior residue, quantity placeholder, migration hold, and application-instruction refusal", ["CCI-LUBRICATION-15-5", "CCI-TRADE-LITERATURE-15-6", "W3C-PROV-O"]),
    ("Typewriter trade-literature and service-manual evidence register with edition, manufacturer claim, page locator, object variance, supersession, comparison hold, and correctness nonclaim", "typewriter-source-register", "Freed ID and CBR Heart", "typewriter trade-literature and service-manual evidence, edition, manufacturer claim, page locator, object variance, supersession, comparison hold, and correctness nonclaim", ["CCI-TRADE-LITERATURE-15-6", "SMITHSONIAN-OPEN-ACCESS", "W3C-PROV-O"]),
    ("Typewriter original, replacement, reproduction, and unknown-component classification board with evidence basis, uncertainty, reversible label, contestation, and authenticity refusal", "typewriter-component-classification", "CBR Heart and Freed ID", "typewriter original, replacement, reproduction, and unknown-component classification, evidence basis, uncertainty, reversible label, contestation, and authenticity refusal", ["CCI-TRADE-LITERATURE-15-6", "CCI-INDUSTRIAL-COLLECTIONS", "W3C-PROV-O"]),
    ("Imaging evidence register for typewriter received state with asset digest, capture context, view code, scale-reference hold, rights class, redaction, supersession, and diagnostic refusal", "typewriter-imaging-evidence", "Freed ID and CBR Heart", "imaging evidence for typewriter received state, asset digest, capture context, view code, scale-reference hold, rights class, redaction, supersession, and diagnostic refusal", ["SMITHSONIAN-OPEN-ACCESS", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Field correction and contestation chain for typewriter treatment records with prior value digest, replacement assertion, reason code, competing account, response reservation, and decision nonautomation", "typewriter-correction-chain", "CBR Heart and Freed ID", "field correction and contestation for typewriter treatment records, prior value digest, replacement assertion, reason code, competing account, response reservation, and decision nonautomation", ["W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES", "RFC-3339"]),
    ("Deferred-care workload board for typewriter cases with checkpoint class, calendar window, delay cue, dependency hold, capacity signal, escalation reservation, and completeness nonclaim", "typewriter-deferred-care-board", "THOS Body and CBR Heart", "deferred-care workload for typewriter cases, checkpoint class, calendar window, delay cue, dependency hold, capacity signal, escalation reservation, and completeness nonclaim", ["CCI-INDUSTRIAL-COLLECTIONS", "RFC-3339", "W3C-PROV-O"]),
    ("Accessible typewriter service and collection-status notice with heading hierarchy, plain-language state, noncolour cue, correction path, alternate-format hold, and affected-user review reservation", "typewriter-accessible-notice", "CBR Heart and THOS Body", "accessible typewriter service and collection-status notice, heading hierarchy, plain-language state, noncolour cue, correction path, alternate-format hold, and affected-user review reservation", ["W3C-WCAG-22", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Typewriter customer, donor, owner-claim, work-log, and contact-data minimization firewall with purpose, retention, disclosure, correction right, legal-review hold, and privacy-complete refusal", "typewriter-privacy-firewall", "CBR Heart and Freed ID", "typewriter customer, donor, owner-claim, work-log, and contact-data minimization, purpose, retention, disclosure, correction right, legal-review hold, and privacy-complete refusal", ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-3339"]),
    ("Sensitive inscription, correspondence, language, provenance, and culturally restricted typewriter-content publication firewall with audience grant, community checkpoint, remedy, and fail-closed disclosure", "typewriter-cultural-firewall", "CBR Heart and Freed ID", "sensitive inscription, correspondence, language, provenance, and culturally restricted typewriter-content publication, audience grant, community checkpoint, remedy, and fail-closed disclosure", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES"]),
    ("GMUT typewriter key-force and linkage-transmission dimensional proxy with lever domains, force and displacement units, loss placeholder, calibration quarantine, and performance-prediction refusal", "gmut-typewriter-key-linkage", "GMUT Mind", "GMUT typewriter key-force and linkage-transmission dimensional proxy, lever domains, force and displacement units, loss placeholder, calibration quarantine, and performance-prediction refusal", ["CCI-TRADE-LITERATURE-15-6", "RFC-8785", "W3C-PROV-O"]),
    ("GMUT typewriter carriage-motion and escapement energy proxy with mass, displacement, spring-energy, friction placeholders, boundary signs, measurement hold, and reliability-claim refusal", "gmut-typewriter-carriage-energy", "GMUT Mind", "GMUT typewriter carriage-motion and escapement energy proxy, mass, displacement, spring-energy, friction placeholders, boundary signs, measurement hold, and reliability-claim refusal", ["CCI-LUBRICATION-15-5", "RFC-8785", "W3C-PROV-O"]),
    ("THOS typewriter workbench shift handover with custody state, loose-part queue, stored-energy hold, incomplete treatment, workload cue, stop-work, readback, and operational-decision refusal", "thos-typewriter-handover", "THOS Body", "THOS typewriter workbench shift handover, custody state, loose-part queue, stored-energy hold, incomplete treatment, workload cue, stop-work, readback, and operational-decision refusal", ["NIST-SP800-61R3", "RFC-3339", "W3C-PROV-O"]),
    ("Freed ID double-bound typewriter service capability capsule with synthetic subject, declared purpose, audience, object boundary, minimized disclosure, expiration, inactive proof, and authorization nonclaim", "freed-id-typewriter-capability", "Freed ID and CBR Heart", "Freed ID double-bound typewriter service capability, synthetic subject, declared purpose, audience, object boundary, minimized disclosure, expiration, inactive proof, and authorization nonclaim", ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID typewriter evidence disclosure envelope with synthetic record digest, activity linkage, selective field set, correction channel, signer absence, status gap, and provenance nonclaim", "freed-id-typewriter-disclosure", "Freed ID", "Freed ID typewriter evidence disclosure, synthetic record digest, activity linkage, selective field set, correction channel, signer absence, status gap, and provenance nonclaim", ["W3C-VC-DM-20", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Smithsonian Open Access typewriter no-network query readiness with collection-unit placeholder, query-purpose hold, rights filter, pagination budget, zero rows, citation capture, and attribution-or-authenticity refusal", "typewriter-smithsonian-zero-row", "GMUT Mind and CBR Heart", "Smithsonian Open Access typewriter no-network query readiness, collection-unit placeholder, query-purpose hold, rights filter, pagination budget, zero rows, citation capture, and attribution-or-authenticity refusal", ["SMITHSONIAN-OPEN-ACCESS", "RFC-8785", "NZ-PRIVACY-PRINCIPLES"]),
    ("CBR typewriter service, conservation, ownership, authenticity, valuation, privacy, accessibility, remedy, law, culture, data governance, affected-party, and Māori-authority non-automation covenant", "cbr-typewriter-authority-covenant", "CBR Heart", "CBR typewriter service, conservation, ownership, authenticity, valuation, privacy, accessibility, remedy, law, culture, data governance, affected-party, and Māori-authority nonautomation", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES", "W3C-WCAG-22"]),
]


PROPOSALS = [
    auren_proposal(
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
    ("ghc-family-typewriter-intake-custody", "Freeze synthetic typewriter intake, custody, identity, scope, condition, correction, and work-start boundaries."),
    ("ghc-family-typewriter-component-topology", "Model keyboard, carriage, control, spring, fastener, and linkage topology without disassembly or operation instructions."),
    ("ghc-family-typewriter-rubber-ribbon-boundary", "Constrain platen, roller, ribbon, spool, ink, substitution, material, and serviceability evidence."),
    ("ghc-family-typewriter-cleaning-lubrication", "Fail closed around cleaning compatibility, ventilation, lubrication, stored energy, and material application."),
    ("ghc-family-typewriter-source-provenance", "Preserve trade-literature, manual, part, originality, reproduction, image, and source-uncertainty lineage."),
    ("ghc-family-typewriter-treatment-correction", "Constrain work-scope revisions, treatment records, field corrections, contestation, and decision ownership."),
    ("ghc-family-typewriter-accessibility-privacy", "Structure accessible status and minimized personal-data records while reserving affected-user and legal review."),
    ("ghc-family-typewriter-schedule-handover", "Constrain deferred care, capacity, incomplete work, stop-work, readback, workload, and shift handover."),
    ("ghc-family-typewriter-freed-id-provenance", "Constrain synthetic service-role and evidence-disclosure purpose, proof, status, correction, and lineage claims."),
    ("ghc-family-typewriter-authority-reservation", "Fail closed around ownership, authenticity, valuation, conservation, remedy, law, culture, governance, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_typewriter_intake_custody.py", "typewriter-intake-provenance"),
    ("ghc_family_typewriter_component_topology.py", "typewriter-keyboard-topology"),
    ("ghc_family_typewriter_rubber_ribbon.py", "typewriter-rubber-state"),
    ("ghc_family_typewriter_cleaning_lubrication.py", "typewriter-cleaning-boundary"),
    ("ghc_family_typewriter_source_provenance.py", "typewriter-source-register"),
    ("ghc_family_typewriter_treatment_correction.py", "typewriter-correction-chain"),
    ("ghc_family_typewriter_accessibility_privacy.py", "typewriter-accessible-notice"),
    ("ghc_family_typewriter_schedule_handover.py", "thos-typewriter-handover"),
    ("ghc_family_typewriter_freed_id_provenance.py", "freed-id-typewriter-capability"),
    ("ghc_family_typewriter_authority_reservation.py", "cbr-typewriter-authority-covenant"),
]


X1_OPERATIONAL_NEGATIVES = [
    negative(1, "powershell-sha256-hashdata-unavailable", "The first source-baton digest probe called SHA256.HashData, which is unavailable in the installed PowerShell runtime.", "Use SHA256.Create with ComputeHash over exact bytes and dispose the instance.", "Probe runtime crypto helpers before composing a digest receipt."),
    negative(2, "powershell-convert-tohexstring-unavailable", "The follow-up digest probe called Convert.ToHexString, which is also unavailable and produced no usable digest.", "Use BitConverter.ToString, remove separators, and lowercase the result.", "Prefer the verified legacy-compatible hash conversion on this Windows runtime."),
    negative(3, "powershell-foreach-pipe-parser-manifest-inventory", "A manifest-size inventory piped directly from foreach and failed with an empty-pipeline-element parser error.", "Materialize all rows into an array before formatting.", "Never pipe directly from a PowerShell foreach statement."),
    negative(4, "git-cat-file-batch-parent-write-before-read-deadlock", "The first manifest verifier wrote all cat-file requests before draining output and blocked without a complete receipt.", "Terminate the bounded orphan process, then use subprocess communicate to write and drain concurrently.", "Use communicate for every bounded git cat-file batch exchange."),
    negative(5, "archive-wide-canonical-digest-search-timeout", "A recursive archive-wide search for Ilyra's external canonical digest exceeded the useful bound without a complete result.", "Stop the broad search and retain the activation-supplied external digest while independently verifying repository evidence.", "Do not traverse the whole archive for an external receipt when exact activation evidence and bounded repository checks suffice."),
    negative(6, "powershell-inline-hashtable-command-expression-parse-error", "A branch-and-path collision receipt embedded command and conditional expressions inside a hashtable and failed before execution.", "Compute scalar values first and construct the receipt only from bound variables.", "Keep commands and control flow outside PowerShell hashtable literals."),
    negative(7, "powershell-foreach-pipe-parser-size-inventory-recurrence", "A later script-size inventory repeated the direct foreach-to-pipeline parser error and produced no rows.", "Materialize the complete row array, then pipe the array to JSON.", "Encode materialize-before-pipe directly in every multirow audit."),
    negative(8, "python-cp1252-novelty-output-fault", "The first candidate-domain scan hit a Māori title and Python's CP1252 stdout encoder failed after partial output.", "Set PYTHONIOENCODING to UTF-8 and rerun only the bounded read-only title scan.", "Bind UTF-8 stdout before printing repository text on Windows."),
    negative(9, "javascript-backslash-string-literal-invalid-token", "A skill-reference read used an unescaped Windows path inside JavaScript and failed during parsing before the file was read.", "Escape backslashes or use a safely quoted literal path.", "Treat Windows paths as data and validate JavaScript string syntax before tool dispatch."),
    negative(10, "phase-data-unicode-context-patch-mismatch", "The first semantic phase-data patch depended on terminal-rendered Unicode context and was rejected without changing the file.", "Append an ASCII-anchored active override block with exact UTF-8 content.", "Use ASCII-safe patch anchors whenever inherited text crosses a rendered encoding boundary."),
    negative(11, "premature-x2-closeout-final-scaffold-materialization", "The first mechanical scaffold copy created fourteen untracked x2, closeout, final, validator, and receipt scripts before the x1 freeze existed.", "Verify every target is owner-created and untracked, remove only those fourteen future-layer files, and retain only the x1 builder, catalogue, phase data, and x1 test.", "Materialize lifecycle scaffolds just in time after each immutable predecessor commit."),
    negative(12, "x1-test-phase-owner-path-not-renamed", "The first bounded x1 test run addressed docs/ilyra-fen/v657-v3, so one assertion failed and nine tests errored on absent files.", "Correct the copied test fixture to docs/auren-lark/v657-v3, refresh the x1 records, and rerun only the bounded x1 suite.", "After every version rename, verify owner and version path components independently."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6573-SAFE-{index:03d}",
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
        "task_id": f"V6573-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6573-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, and stale-label cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
