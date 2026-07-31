#!/usr/bin/env python3
"""Frozen x1 catalogue for Ilyra Fen's v657-v2 phase."""

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
        "New Zealand lift-safety and maintenance vocabulary only; no compliance or inspection conclusion",
    ),
    source(
        "NZ-BUILDING-LIFTS",
        "Lifts: accessible internal circulation guidance",
        "New Zealand Ministry of Business, Innovation and Employment",
        "https://www.building.govt.nz/building-code-compliance/d-access/accessible-buildings/internal-circulation/lifts",
        "current",
        "accessible lift-location, control, feedback, door, car, and wayfinding vocabulary only",
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
    "real_lifts_escalators_buildings_shafts_pits_machine_rooms_components_controls_and_access_systems",
    "real_isolation_inspection_testing_adjustment_repair_rescue_return_to_service_and_procurement_decisions",
    "real_measurements_statistics_failure_rates_injury_estimates_likelihoods_predictions_and_empirical_confirmation",
    "professional_lift_maintenance_inspection_engineering_emergency_accessibility_privacy_operations_and_health_and_safety_authority",
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
        "proposal_id": f"V6572-P{number:02d}",
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
            "people, lifts, buildings, controls, accounts, credentials, components, incidents, "
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
    ("Lift asset passport with synthetic installation token, conveyance class, building hold, controller family, service state, correction lineage, and ownership nonclaim", "lift-asset-passport", "THOS Body and Freed ID/CBR Heart", "lift asset passport, synthetic installation token, conveyance class, building hold, controller family, service state, correction lineage, and ownership nonclaim", ["NZ-BUILDING-D2", "ASME-A17-1-2025", "W3C-PROV-O"]),
    ("Lift service-request intake docket with symptom narrative, caller pseudonym, urgency cue, duplicate link, passenger-impact hold, and diagnosis refusal", "lift-service-intake", "THOS Body and CBR Heart", "lift service-request intake, symptom narrative, caller pseudonym, urgency cue, duplicate link, passenger-impact hold, and diagnosis refusal", ["NZ-BUILDING-D2", "NIST-SP800-61R3", "NZ-PRIVACY-PRINCIPLES"]),
    ("Lift work-order scope and revision ledger with inspection placeholder, task boundary, deviation, parts hold, readback, acceptance reservation, and no-work authorization", "lift-work-order-revision", "THOS Body and Freed ID", "lift work-order scope and revision ledger, inspection placeholder, task boundary, deviation, parts hold, readback, acceptance reservation, and work-authorization refusal", ["ASME-A17-1-2025", "W3C-PROV-O", "RFC-3339"]),
    ("Out-of-service barrier and tag state board with landing set, notice channel, issue time, issuer-role hold, bypass refusal, correction, and no-isolation claim", "lift-out-of-service-hold", "THOS Body and CBR Heart", "out-of-service barrier and tag state, landing set, notice channel, issue time, issuer-role hold, bypass refusal, correction, and isolation-claim refusal", ["NZ-BUILDING-D2", "RFC-3339", "W3C-PROV-O"]),
    ("Lift hazardous-energy isolation plan with source classes, disconnect placeholder, stored-energy cue, zero-energy verification hold, handback state, and compliance refusal", "lift-energy-isolation", "THOS Body", "lift hazardous-energy isolation plan, source classes, disconnect placeholder, stored-energy cue, zero-energy verification hold, handback state, and compliance refusal", ["OSHA-1910-147", "ASME-A17-1-2025", "W3C-PROV-O"]),
    ("Machine-room, pit, and hoistway access reservation with zone token, access basis, companion cue, environmental hazard hold, expiry, and entry-authority refusal", "lift-access-reservation", "THOS Body and CBR Heart", "machine-room, pit, and hoistway access reservation, zone token, access basis, companion cue, environmental hazard hold, expiry, and entry-authority refusal", ["NZ-BUILDING-D2", "OSHA-1910-147", "RFC-3339"]),
    ("Lift door-zone and interlock inspection-state ledger with entrance token, contact-state placeholder, bypass cue, discrepancy quarantine, correction lineage, and release refusal", "lift-door-interlock-state", "THOS Body and GMUT Mind", "lift door-zone and interlock inspection-state ledger, entrance token, contact-state placeholder, bypass cue, discrepancy quarantine, correction lineage, and release refusal", ["ASME-A17-1-2025", "NZ-BUILDING-D2", "W3C-PROV-O"]),
    ("Lift door-obstruction protective-device check with sensing field, reversal placeholder, dwell interval, blocked-path cue, adjustment hold, and safety-verdict refusal", "lift-door-protection-state", "THOS Body and CBR Heart", "lift door-obstruction protective-device check, sensing field, reversal placeholder, dwell interval, blocked-path cue, adjustment hold, and safety-verdict refusal", ["NZ-BUILDING-LIFTS", "ASME-A17-1-2025", "RFC-3339"]),
    ("Lift brake and traction observation envelope with component token, method hold, direction, speed class, abnormal cue, competent-review reservation, and fitness refusal", "lift-brake-traction-state", "THOS Body and GMUT Mind", "lift brake and traction observation envelope, component token, method hold, direction, speed class, abnormal cue, competent-review reservation, and fitness refusal", ["ASME-A17-1-2025", "NZ-BUILDING-D2", "W3C-PROV-O"]),
    ("Suspension means and sheave visual-state docket with member token, wear cue, tension-balance placeholder, contamination hold, replacement threshold reservation, and service refusal", "lift-suspension-sheave-state", "THOS Body and GMUT Mind", "suspension means and sheave visual-state docket, member token, wear cue, tension-balance placeholder, contamination hold, replacement threshold reservation, and service refusal", ["ASME-A17-1-2025", "W3C-PROV-O", "RFC-8785"]),
    ("Overspeed governor test reservation with device token, rated-speed placeholder, trigger cue, reset state, witnessed-result hold, and no-test certification", "lift-governor-test-reservation", "THOS Body and GMUT Mind", "overspeed governor test reservation, device token, rated-speed placeholder, trigger cue, reset state, witnessed-result hold, and test-certification refusal", ["ASME-A17-1-2025", "NZ-BUILDING-D2", "W3C-PROV-O"]),
    ("Lift buffer and terminal stopping-device state board with end-of-travel zone, component class, clearance placeholder, contact state, correction hold, and adequacy refusal", "lift-terminal-buffer-state", "THOS Body", "lift buffer and terminal stopping-device state board, end-of-travel zone, component class, clearance placeholder, contact state, correction hold, and adequacy refusal", ["ASME-A17-1-2025", "NZ-BUILDING-D2", "RFC-8785"]),
    ("Lift levelling accuracy and sill-gap measurement envelope with landing token, direction, SI unit, uncertainty, instrument hold, tolerance reservation, and compliance refusal", "lift-levelling-gap-envelope", "GMUT Mind and THOS Body", "lift levelling accuracy and sill-gap measurement envelope, landing token, direction, SI unit, uncertainty, instrument hold, tolerance reservation, and compliance refusal", ["NZ-BUILDING-LIFTS", "ASME-A17-1-2025", "W3C-PROV-O"]),
    ("Rated-load plate and capacity evidence board with car token, displayed value, unit, source-document hold, discrepancy state, correction path, and loading-authorization refusal", "lift-rated-load-board", "THOS Body and CBR Heart", "rated-load plate and capacity evidence board, car token, displayed value, unit, source-document hold, discrepancy state, correction path, and loading-authorization refusal", ["NZ-BUILDING-D2", "ASME-A17-1-2025", "W3C-PROV-O"]),
    ("Lift emergency alarm and two-way communication accessibility docket with control location, visual and audible feedback, connection placeholder, fallback hold, manual review, and conformance refusal", "lift-emergency-communication", "THOS Body and CBR Heart", "lift emergency alarm and two-way communication accessibility docket, control location, visual and audible feedback, connection placeholder, fallback hold, manual review, and conformance refusal", ["NZ-BUILDING-LIFTS", "W3C-WCAG-22", "NZ-BUILDING-D2"]),
    ("Lift fire-service and recall interface test reservation with mode token, input placeholder, landing destination, conflicting state, fire-authority hold, restoration cue, and no-certification claim", "lift-fire-recall-reservation", "THOS Body and CBR Heart", "lift fire-service and recall interface test reservation, mode token, input placeholder, landing destination, conflicting state, fire-authority hold, restoration cue, and certification refusal", ["ASME-A17-1-2025", "NZ-BUILDING-D2", "W3C-PROV-O"]),
    ("Lift entrapment incident and passenger-welfare handover with call token, location hold, communication state, medical cue, emergency-controller reservation, readback, and rescue refusal", "lift-entrapment-handover", "THOS Body and CBR Heart", "lift entrapment incident and passenger-welfare handover, call token, location hold, communication state, medical cue, emergency-controller reservation, readback, and rescue refusal", ["NIST-SP800-61R3", "NZ-BUILDING-D2", "RFC-3339"]),
    ("Lift replacement-part provenance and compatibility quarantine with part token, source document, supersession, interface cue, procurement hold, installation reservation, and equivalence refusal", "lift-part-provenance", "Freed ID and GMUT Mind", "lift replacement-part provenance and compatibility quarantine, part token, source document, supersession, interface cue, procurement hold, installation reservation, and equivalence refusal", ["ASME-A17-1-2025", "W3C-PROV-O", "RFC-8785"]),
    ("Lift controller software and configuration change lineage with version token, parameter class, change purpose, backup digest placeholder, review hold, rollback cue, and production-change refusal", "lift-control-change-lineage", "Freed ID and THOS Body", "lift controller software and configuration change lineage, version token, parameter class, change purpose, backup digest placeholder, review hold, rollback cue, and production-change refusal", ["W3C-PROV-O", "RFC-8785", "ASME-A17-1-2025"]),
    ("Lift preventive-maintenance schedule ledger with task family, interval basis, due window, deferral reason, workload cue, escalation hold, and maintenance-sufficiency refusal", "lift-maintenance-schedule", "THOS Body and CBR Heart", "lift preventive-maintenance schedule ledger, task family, interval basis, due window, deferral reason, workload cue, escalation hold, and maintenance-sufficiency refusal", ["ASME-A17-1-2025", "RFC-3339", "W3C-PROV-O"]),
    ("Accessible lift outage and alternative-route notice with heading hierarchy, affected landing set, status provenance, tactile and auditory cue hold, correction path, and affected-user review reserved", "lift-outage-accessible-notice", "CBR Heart and THOS Body", "accessible lift outage and alternative-route notice, heading hierarchy, affected landing set, status provenance, tactile and auditory cue hold, correction path, and affected-user review reservation", ["NZ-BUILDING-LIFTS", "W3C-WCAG-22", "W3C-PROV-O"]),
    ("Lift evidence amendment and supersession graph with field-level delta, origin class, immutable prior, rebuttal edge, review-owner reservation, and decision-rights refusal", "lift-record-amendment-graph", "CBR Heart and Freed ID", "lift evidence amendment and supersession graph, field-level delta, origin class, immutable prior, rebuttal edge, review-owner reservation, and decision-rights refusal", ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-3339"]),
    ("Lift access-log privacy minimization and disclosure firewall with purpose, event class, retention window, role hold, correction right, legal-review reservation, and privacy-complete refusal", "lift-access-log-privacy", "CBR Heart and Freed ID", "lift access-log privacy minimization and disclosure firewall, purpose, event class, retention window, role hold, correction right, legal-review reservation, and privacy-complete refusal", ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-3339"]),
    ("GMUT traction-rope coupled-oscillator dimensional proxy with car and counterweight domains, stiffness and damping units, boundary signs, calibration quarantine, and motion-prediction refusal", "gmut-lift-rope-dynamics", "GMUT Mind", "GMUT traction-rope coupled-oscillator dimensional proxy, car and counterweight domains, stiffness and damping units, boundary signs, calibration quarantine, and motion-prediction refusal", ["ASME-A17-1-2025", "RFC-8785", "W3C-PROV-O"]),
    ("GMUT lift braking-energy and thermal-dissipation dimensional proxy with mass and speed placeholders, energy and power units, loss terms, measurement hold, and safety-margin refusal", "gmut-lift-braking-thermal", "GMUT Mind", "GMUT lift braking-energy and thermal-dissipation dimensional proxy, mass and speed placeholders, energy and power units, loss terms, measurement hold, and safety-margin refusal", ["ASME-A17-1-2025", "RFC-8785", "W3C-PROV-O"]),
    ("THOS lift-maintenance shift handover choreography with isolation state, defect queue, parts hold, incomplete test, workload cue, safety stop, readback, and operational-decision refusal", "thos-lift-shift-handover", "THOS Body", "THOS lift-maintenance shift handover choreography, isolation state, defect queue, parts hold, incomplete test, workload cue, safety stop, readback, and operational-decision refusal", ["NIST-SP800-61R3", "RFC-3339", "W3C-PROV-O"]),
    ("Freed ID synthetic maintenance-access purpose matrix with capability label, lift-zone scope, double-bind expiry, disclosure minimum, status hold, and live-authorization refusal", "freed-id-lift-purpose-matrix", "Freed ID and CBR Heart", "Freed ID synthetic maintenance-access purpose matrix, capability label, lift-zone scope, double-bind expiry, disclosure minimum, status hold, and live-authorization refusal", ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID synthetic lift-maintenance record provenance card with subject digest, work-order relation, inspection-state hold, disclosure shield, unsigned state, and origin nonclaim", "freed-id-lift-record-card", "Freed ID", "Freed ID synthetic lift-maintenance record provenance card, subject digest, work-order relation, inspection-state hold, disclosure shield, unsigned state, and origin nonclaim", ["W3C-VC-DM-20", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("CPSC NEISS elevator and escalator no-network query readiness with product-code placeholder, treatment-year hold, weight and variance reservation, zero rows, citation capture, and injury-inference refusal", "lift-neiss-zero-row", "GMUT Mind and CBR Heart", "CPSC NEISS elevator and escalator no-network query readiness, product-code placeholder, treatment-year hold, weight and variance reservation, zero rows, citation capture, and injury-inference refusal", ["CPSC-NEISS", "RFC-8785", "NZ-PRIVACY-PRINCIPLES"]),
    ("CBR lift safety, accessibility, outage, privacy, rescue, building access, remedy, law, culture, data governance, affected-party, and Māori-authority non-automation covenant", "cbr-lift-authority-covenant", "CBR Heart", "CBR lift safety, accessibility, outage, privacy, rescue, building access, remedy, law, culture, data governance, affected-party, and Māori-authority non-automation covenant", ["NZ-BUILDING-D2", "NZ-BUILDING-LIFTS", "TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS"]),
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
    ("ghc-family-lift-asset-work-order", "Freeze synthetic lift asset, service-intake, work-order revision, correction, and ownership boundaries."),
    ("ghc-family-lift-isolation-hold", "Separate out-of-service and hazardous-energy hold structure from real isolation, testing, and return-to-service authority."),
    ("ghc-family-lift-access-boundary", "Fail closed around machine-room, pit, hoistway, building, passenger, and technician access decisions."),
    ("ghc-family-lift-door-safety-state", "Model synthetic door-zone, interlock, and obstruction-protection states without issuing a safety verdict."),
    ("ghc-family-lift-motion-component-state", "Constrain brake, traction, suspension, governor, buffer, levelling, and rated-load evidence to typed observations."),
    ("ghc-family-lift-emergency-accessibility", "Structure emergency communication, fire-interface, entrapment, outage, and alternative-route records while reserving real evaluation."),
    ("ghc-family-lift-part-config-provenance", "Preserve replacement-part and controller-configuration provenance, review, rollback, and production-change boundaries."),
    ("ghc-family-lift-schedule-handover", "Constrain preventive-maintenance schedules, workload, incomplete tests, correction readback, and shift handover."),
    ("ghc-family-lift-freed-id-provenance", "Constrain synthetic technician-role and maintenance-record identity, disclosure, proof, status, and lineage claims."),
    ("ghc-family-lift-authority-reservation", "Fail closed around safety, access, rescue, remedy, law, culture, governance, affected-party, and Māori authority."),
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
    ("ghc_family_lift_asset_work_order.py", "lift-work-order-revision"),
    ("ghc_family_lift_isolation_hold.py", "lift-energy-isolation"),
    ("ghc_family_lift_access_boundary.py", "lift-access-reservation"),
    ("ghc_family_lift_door_safety_state.py", "lift-door-interlock-state"),
    ("ghc_family_lift_motion_component_state.py", "lift-brake-traction-state"),
    ("ghc_family_lift_emergency_accessibility.py", "lift-emergency-communication"),
    ("ghc_family_lift_part_config_provenance.py", "lift-control-change-lineage"),
    ("ghc_family_lift_schedule_handover.py", "thos-lift-shift-handover"),
    ("ghc_family_lift_freed_id_provenance.py", "freed-id-lift-purpose-matrix"),
    ("ghc_family_lift_authority_reservation.py", "cbr-lift-authority-covenant"),
]


def negative(number: int, signature: str, observed: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6572-X1-N{number:02d}",
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
    negative(17, "source-closeout-count-mistaken-for-final-sealed-total", "The first Ilyra source model treated Lyren's 15,246 closeout count plus two final-preparation failures as external, although the committed final register already retains both and reports 15,248.", "Inspect the authoritative final negative-register fields, preserve 15,248 as the sealed activation baseline, and add no invented external count.", "Read closeout_effective_count, final_preparation_count, and effective_count together before modelling inherited totals."),
    negative(18, "activation-baton-checkout-hash-used-as-git-blob-hash", "The first x1 build stopped before packet writes because the expected baton digest described CRLF checkout bytes rather than the immutable Git blob.", "Measure both domains, bind the builder to the exact source-commit Git-blob SHA-256, and retain the checkout digest as a separate receipt field.", "Declare the hash domain for every historical content seal before validation."),
    negative(19, "semantic-neighbor-threshold-rejected-two-proposals", "The second x1 build stopped before packet writes because proposal 22 scored 0.7000 and proposal 27 scored 0.7619 against Lyren semantic neighbors, above the frozen 0.60 threshold.", "Rewrite both mechanisms around distinct amendment-graph and purpose-matrix contracts, then rerun the unchanged all-2,440-title tribunal.", "Never lower the novelty threshold to admit a duplicate; rewrite or reject the proposal."),
    negative(20, "stale-label-probe-expanded-frozen-chain-output", "The first current-label search included the one-line 2,440-row frozen proposal index, producing an oversized inherited-history listing that was truncated and could not prove current-label hygiene.", "Exclude declared ancestry and nearest-neighbor evidence files, then scan all remaining current phase surfaces with the unchanged stale-label patterns.", "Separate historical evidence fields from current lifecycle-label scans and cap diagnostic output."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6572-SAFE-{index:03d}",
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
        "task_id": f"V6572-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6572-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, and stale-label cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
