#!/usr/bin/env python3
"""Frozen x1 catalogue for Caelen Ash's v657-v5 phase."""

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
        "AZA-ACCREDITATION-2026",
        "2026 Accreditation Standards and Related Policies",
        "Association of Zoos and Aquariums",
        "https://www.aza.org/accred-materials",
        "current",
        "animal-welfare, records, facility-program, and review vocabulary only; no accreditation, inspection, employment, or professional authority",
    ),
    source(
        "AZA-ANIMAL-CARE-MANUALS",
        "Animal Care Manuals",
        "Association of Zoos and Aquariums",
        "https://www.aza.org/animal-care-manuals",
        "current",
        "species-care source and expert-review vocabulary only; no real husbandry, diagnosis, treatment, or welfare conclusion",
    ),
    source(
        "WOAH-AQUATIC-CODE",
        "Aquatic Animal Health Code",
        "World Organisation for Animal Health",
        "https://www.woah.org/en/what-we-do/standards/codes-and-manuals/",
        "current",
        "aquatic-health, welfare, surveillance, trade, and competent-authority vocabulary only; no veterinary or biosecurity decision",
    ),
    source(
        "EPA-DISSOLVED-OXYGEN",
        "Indicators: Dissolved Oxygen",
        "United States Environmental Protection Agency",
        "https://www.epa.gov/national-aquatic-resource-surveys/indicators-dissolved-oxygen",
        "current",
        "water-parameter and calibrated-observation vocabulary only; no aquarium threshold, diagnosis, measurement, or animal-care decision",
    ),
    source(
        "MPI-ORNAMENTAL-AQUATIC-IHS",
        "Ornamental fish and marine invertebrates 2021 - Import Health Standard",
        "New Zealand Ministry for Primary Industries",
        "https://www.mpi.govt.nz/dmsdocument/17425-Ornamental-fish-and-marine-invertebrates-from-all-countries-Import-Health-Standard/",
        "current",
        "biosecurity and ornamental-aquatic import-document vocabulary only; no import, clearance, legal interpretation, or operational direction",
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
        "incident, retained-negative, recovery, communication, and handover vocabulary only",
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
        "synthetic UTC timestamps, observation windows, expiry, correction, and handover",
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
    "real_animals_veterinarians_aquarists_keepers_facility_operators_regulators_communities_and_affected_parties",
    "real_aquariums_tanks_life_support_systems_pumps_valves_filters_skimmers_uv_ozone_electrical_chemical_and_water_systems",
    "real_feeding_handling_transfer_quarantine_acclimation_enrichment_diagnosis_treatment_medication_euthanasia_or_life_support_operation",
    "real_water_samples_measurements_calibrations_thresholds_alarms_welfare_assessments_likelihoods_predictions_and_empirical_gmut_confirmation",
    "professional_veterinary_aquarium_husbandry_animal_welfare_biosecurity_electrical_chemical_structural_accessibility_privacy_or_workplace_authority",
    "sensitive_species_location_provenance_trade_health_welfare_visitor_staff_traditional_knowledge_and_culturally_restricted_information",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_animal_welfare_biosecurity_trade_indigenous_traditional_knowledge_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_animal_care_acceptance",
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
        "proposal_id": f"V6575-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable synthetic evidence obligations "
            "while refusing unsupported empirical, animal-welfare, professional, security, "
            "accessibility, privacy, identity, production, legal, cultural, Māori-authority, or "
            "Stage 20 promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, "
            "erases a failure, or crosses a protected animal, participant, facility, treatment, "
            "empirical, professional, production, legal, cultural, Māori-authority, identity, or "
            "Stage 20 gate."
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
            "the receipt grants no real animal, person, aquarium, tank, sample, feeding, handling, "
            "transfer, quarantine, diagnosis, treatment, professional, production, legal, cultural, "
            "Māori-authority, identity, accessibility-complete, privacy-complete, security-complete, "
            "independent-reproduction, Theory-of-Everything, or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real "
            "animals, people, aquariums, tanks, water, tools, chemicals, accounts, records, care "
            "decisions, sibling lanes, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Aquarium accession and animal-group custody passport with synthetic group token, exhibit-zone scope, responsible-role placeholder, dispute channel, and no-care-action lock", "aquarium-intake-provenance", "Freed ID and CBR Heart", "aquarium accession, synthetic animal-group custody, exhibit-zone scope, responsible-role placeholder, dispute channel, and care-action refusal", ["AZA-ACCREDITATION-2026", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Aquarium taxonomic-claim ledger with common-name source, scientific-name placeholder, life-stage uncertainty, conflict quarantine, revision, and identification nonclaim", "aquarium-taxonomy-claim", "GMUT Mind and Freed ID", "aquarium taxonomic claim, source, life-stage uncertainty, conflict quarantine, revision, and identification refusal", ["AZA-ANIMAL-CARE-MANUALS", "WOAH-AQUATIC-CODE", "W3C-PROV-O"]),
    ("Aquarium exhibit, tank, sump, refuge, overflow, return, and isolation-zone topology graph with orphan quarantine and no-plumbing instruction", "aquarium-exhibit-topology", "GMUT Mind and THOS Body", "aquarium exhibit, tank, sump, refuge, overflow, return, and isolation-zone topology with orphan quarantine and plumbing-instruction refusal", ["AZA-ACCREDITATION-2026", "W3C-PROV-O", "RFC-8785"]),
    ("Aquarium pump, valve, filter, skimmer, ultraviolet, ozone, heat-exchange, sensor, and bypass life-support topology with command refusal", "aquarium-life-support-topology", "THOS Body and GMUT Mind", "aquarium pump, valve, filter, skimmer, ultraviolet, ozone, heat-exchange, sensor, and bypass topology with operation-command refusal", ["AZA-ACCREDITATION-2026", "OSHA-1910-147", "W3C-PROV-O"]),
    ("Aquarium water-observation chain with synthetic sample token, tank-zone relation, collection-time placeholder, custody, method hold, qualifier, and no-result claim", "aquarium-water-observation", "GMUT Mind and Freed ID", "aquarium water-observation chain, synthetic sample token, tank-zone relation, custody, method hold, qualifier, and result refusal", ["EPA-DISSOLVED-OXYGEN", "W3C-PROV-O", "RFC-3339"]),
    ("Aquarium temperature, salinity, dissolved-oxygen, pH, alkalinity, nitrogen-species, unit, uncertainty, calibration, and threshold-authority refusal envelope", "aquarium-parameter-envelope", "GMUT Mind", "aquarium temperature, salinity, dissolved oxygen, pH, alkalinity, nitrogen-species, unit, uncertainty, calibration hold, and threshold-authority refusal", ["EPA-DISSOLVED-OXYGEN", "BIPM-SI-BROCHURE", "NIST-SP811"]),
    ("Aquarium life-support setpoint and alarm reservation with source placeholder, species-context hold, hysteresis, acknowledgement, escalation, and no-control release", "aquarium-setpoint-alarm-hold", "THOS Body and GMUT Mind", "aquarium life-support setpoint and alarm reservation, species-context hold, hysteresis, acknowledgement, escalation, and control-release refusal", ["AZA-ANIMAL-CARE-MANUALS", "NIST-SP800-61R3", "RFC-3339"]),
    ("Aquarium motor, heater, ultraviolet, ozone, lighting, panel, wet-location, isolation-state, and no-energization board", "aquarium-electrical-isolation", "THOS Body and CBR Heart", "aquarium motor, heater, ultraviolet, ozone, lighting, panel, wet-location, isolation state, and energization refusal", ["OSHA-1910-147", "AZA-ACCREDITATION-2026", "W3C-PROV-O"]),
    ("Aquarium pressurized line, compressed gas, ozone, disinfectant, dosing vessel, stored-energy, exposure, and no-chemical-application boundary", "aquarium-energy-chemical-boundary", "THOS Body and CBR Heart", "aquarium pressurized line, compressed gas, ozone, disinfectant, dosing vessel, stored energy, exposure, and chemical-application refusal", ["OSHA-1910-147", "AZA-ACCREDITATION-2026", "W3C-PROV-O"]),
    ("Aquarium feed-item provenance, lot placeholder, storage state, ration placeholder, species relation, expiry cue, substitution hold, and no-feeding instruction", "aquarium-feed-provenance", "Freed ID and CBR Heart", "aquarium feed provenance, lot placeholder, storage state, ration placeholder, species relation, expiry cue, substitution hold, and feeding-instruction refusal", ["AZA-ANIMAL-CARE-MANUALS", "W3C-PROV-O", "RFC-3339"]),
    ("Aquarium medication and treatment reservation with diagnosis absence, veterinary-order placeholder, dose and route hold, withdrawal cue, monitoring gap, and no-treatment command", "aquarium-treatment-reservation", "CBR Heart and THOS Body", "aquarium medication and treatment reservation, diagnosis absence, veterinary-order placeholder, dose and route hold, monitoring gap, and treatment-command refusal", ["WOAH-AQUATIC-CODE", "AZA-ANIMAL-CARE-MANUALS", "W3C-PROV-O"]),
    ("Aquarium quarantine, acclimation, transfer, source-water, destination-water, container, health-review, release, and no-animal-movement docket", "aquarium-transfer-quarantine", "THOS Body and CBR Heart", "aquarium quarantine, acclimation, transfer, source-water, destination-water, container, health-review, release, and animal-movement refusal", ["WOAH-AQUATIC-CODE", "MPI-ORNAMENTAL-AQUATIC-IHS", "W3C-PROV-O"]),
    ("Aquarium behaviour and welfare observation vocabulary with synthetic event token, context window, observer role, uncertainty, escalation, and diagnosis refusal", "aquarium-welfare-observation", "THOS Body and CBR Heart", "aquarium behaviour and welfare observation, synthetic event token, context window, observer role, uncertainty, escalation, and diagnosis refusal", ["AZA-ACCREDITATION-2026", "AZA-ANIMAL-CARE-MANUALS", "RFC-3339"]),
    ("Aquarium morbidity and mortality event record with animal-group token, discovery window, scene hold, evidence custody, veterinary reservation, correction, and no-cause claim", "aquarium-morbidity-event", "CBR Heart and Freed ID", "aquarium morbidity and mortality event, animal-group token, discovery window, scene hold, evidence custody, veterinary reservation, correction, and cause refusal", ["WOAH-AQUATIC-CODE", "NIST-SP800-61R3", "W3C-PROV-O"]),
    ("Aquarium cross-contamination and biosecurity boundary with equipment zone, water path, organism-transfer cue, quarantine state, decontamination hold, and clearance refusal", "aquarium-biosecurity-boundary", "THOS Body and CBR Heart", "aquarium cross-contamination and biosecurity boundary, equipment zone, water path, organism-transfer cue, quarantine state, decontamination hold, and clearance refusal", ["WOAH-AQUATIC-CODE", "MPI-ORNAMENTAL-AQUATIC-IHS", "W3C-PROV-O"]),
    ("Aquarium water-change and make-up-water planning envelope with source placeholder, volume and rate units, mixing hold, temperature and salinity relation, discharge gate, and no-execution instruction", "aquarium-water-change-plan", "GMUT Mind and THOS Body", "aquarium water-change and make-up-water plan, source placeholder, volume and rate units, mixing hold, parameter relation, discharge gate, and execution refusal", ["BIPM-SI-BROCHURE", "NIST-SP811", "AZA-ANIMAL-CARE-MANUALS"]),
    ("Aquarium animal and specimen provenance register with acquisition source, permit placeholder, import-health relation, trade-status watch, disclosure class, and legality nonclaim", "aquarium-specimen-provenance", "Freed ID and CBR Heart", "aquarium animal and specimen provenance, acquisition source, permit placeholder, import-health relation, trade-status watch, disclosure class, and legality refusal", ["MPI-ORNAMENTAL-AQUATIC-IHS", "WOAH-AQUATIC-CODE", "W3C-PROV-O"]),
    ("Aquarium habitat and enrichment change proposal with substrate, structure, refuge, lighting, flow, species-context hold, approval placeholder, rollback, and no-modification instruction", "aquarium-habitat-change", "THOS Body and CBR Heart", "aquarium habitat and enrichment change proposal, substrate, structure, refuge, lighting, flow, species-context hold, approval placeholder, rollback, and modification refusal", ["AZA-ANIMAL-CARE-MANUALS", "AZA-ACCREDITATION-2026", "W3C-PROV-O"]),
    ("Aquarium public-viewing, animal-rest, maintenance-window, feeding-display, event, conflict, quiet-period, and schedule-authority refusal ledger", "aquarium-public-window", "CBR Heart and THOS Body", "aquarium public-viewing, animal-rest, maintenance-window, feeding-display, event, conflict, quiet-period, and schedule-authority refusal", ["AZA-ACCREDITATION-2026", "RFC-3339", "W3C-PROV-O"]),
    ("Aquarium observation-media register with synthetic asset token, animal and visitor visibility, capture context, rights, redaction, disclosure, and behavioural-inference refusal", "aquarium-media-privacy", "Freed ID and CBR Heart", "aquarium observation media, synthetic asset token, animal and visitor visibility, capture context, rights, redaction, disclosure, and behavioural-inference refusal", ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-8785"]),
    ("Aquarium evidence-amendment graph with superseded observation digest, replacement fact, keeper-dissent branch, responder reservation, readback, and human-adjudication hold", "aquarium-correction-chain", "CBR Heart and Freed ID", "aquarium evidence amendment, superseded observation digest, replacement fact, keeper-dissent branch, responder reservation, readback, and human-adjudication hold", ["W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES", "RFC-3339"]),
    ("Accessible aquarium operations bulletin with exhibit status, animal-care hold, plain language, redundant cues, alternative delivery, amendment link, and affected-user review reservation", "aquarium-accessible-notice", "CBR Heart and THOS Body", "accessible aquarium operations bulletin, exhibit status, animal-care hold, plain language, redundant cues, alternative delivery, amendment link, and affected-user review reservation", ["W3C-WCAG-22", "NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O"]),
    ("Aquarium record and life-support threat model with tampering, injection, replay, unsafe command, raw identifier, disclosure, recovery, and exhaustive-security refusal", "aquarium-threat-recovery", "Freed ID, THOS Body, and CBR Heart", "aquarium record and life-support threat model, tampering, injection, replay, unsafe command, raw identifier, disclosure, recovery, and exhaustive-security refusal", ["NIST-SP800-61R3", "RFC-8785", "NZ-PRIVACY-PRINCIPLES"]),
    ("GMUT aquarium recirculating-network dimensional proxy with tank and sump nodes, flow edges, continuity residual, pump placeholder, loss term, boundary, stability, and zero-likelihood claim", "gmut-aquarium-flow-network", "GMUT Mind", "aquarium recirculating-network dimensional proxy, tank and sump nodes, flow edges, continuity residual, pump placeholder, loss term, boundary, stability, and likelihood refusal", ["BIPM-SI-BROCHURE", "NIST-SP811", "RFC-8785"]),
    ("GMUT aquarium oxygen and thermal mass-balance proxy with dissolved-gas state, heat-capacity placeholder, source and sink terms, units, covariance, identifiability, and prediction refusal", "gmut-aquarium-oxygen-thermal", "GMUT Mind", "aquarium oxygen and thermal mass-balance proxy, dissolved-gas state, heat-capacity placeholder, source and sink terms, units, covariance, identifiability, and prediction refusal", ["EPA-DISSOLVED-OXYGEN", "BIPM-SI-BROCHURE", "NIST-SP811"]),
    ("THOS aquarium shift handover with animal-group status, life-support alarm, isolation hold, unresolved welfare cue, workload limit, readback, stop-work, and matched-budget real-arm refusal", "thos-aquarium-handover", "THOS Body", "aquarium shift handover, animal-group status, life-support alarm, isolation hold, unresolved welfare cue, workload limit, readback, stop-work, and matched-budget real-arm refusal", ["AZA-ACCREDITATION-2026", "NIST-SP800-61R3", "RFC-3339"]),
    ("Freed ID aquarium observation-batch provenance capsule with creator-role placeholder, record-chain digest, recipient minimization, retention epoch, absent signature, and verification refusal", "freed-id-aquarium-batch-provenance", "Freed ID and CBR Heart", "observation-batch provenance capsule with creator-role placeholder, record-chain digest, recipient minimization, retention epoch, absent signature, and verification refusal", ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID aquarium-record disclosure and status profile with controller, resolution, revocation, interoperability, recovery, correlation, trust-governance gaps, and nonproduction boundary", "freed-id-aquarium-status", "Freed ID", "aquarium-record disclosure and status profile, controller, resolution, revocation, interoperability, recovery, correlation, trust-governance gaps, and nonproduction boundary", ["W3C-VC-DM-20", "W3C-DID-10", "W3C-BITSTRING-STATUS-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("AZA and WOAH aquarium guidance no-network zero-row adapter with source edition, species-scope placeholder, welfare and health field quarantine, revision watch, attribution, and inference refusal", "aquarium-guidance-zero-row-adapter", "THOS Body and CBR Heart", "AZA and WOAH aquarium guidance no-network zero-row adapter, source edition, species-scope placeholder, welfare and health field quarantine, revision watch, attribution, and inference refusal", ["AZA-ANIMAL-CARE-MANUALS", "WOAH-AQUATIC-CODE", "RFC-8785", "W3C-PROV-O"]),
    ("CBR aquarium animal welfare, biosecurity, acquisition, trade, public access, privacy, remedy, law, culture, data governance, affected-party, and Māori-authority nonautomation covenant", "cbr-aquarium-authority-covenant", "CBR Heart", "aquarium animal welfare, biosecurity, acquisition, trade, public access, privacy, remedy, law, culture, data governance, affected-party, and Māori-authority nonautomation", ["MPI-ORNAMENTAL-AQUATIC-IHS", "TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES"]),
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
    ("ghc-family-aquarium-intake-provenance", "Freeze synthetic aquarium intake, animal-group identity, custody, scope, correction, and care-action boundaries."),
    ("ghc-family-aquarium-life-support-topology", "Model tanks, sumps, pumps, valves, filtration, sensors, bypasses, and orphan edges without operating instructions."),
    ("ghc-family-aquarium-water-observation", "Constrain sample tokens, parameter units, uncertainty, calibration holds, thresholds, and measurement nonclaims."),
    ("ghc-family-aquarium-energy-isolation", "Fail closed around wet-location electrical state, stored pressure, ozone, chemicals, dosing, and energization."),
    ("ghc-family-aquarium-welfare-observation", "Separate bounded animal observation from diagnosis, treatment, welfare conclusion, and care authority."),
    ("ghc-family-aquarium-biosecurity-hold", "Preserve quarantine, transfer, cross-contamination, provenance, import-health, and clearance reservations."),
    ("ghc-family-aquarium-source-correction", "Preserve observation, media, source, amendment, dissent, correction, disclosure, and human-adjudication lineage."),
    ("ghc-family-aquarium-accessibility-privacy", "Structure accessible notices and minimized records while reserving manual, affected-user, and legal review."),
    ("ghc-family-aquarium-thos-handover", "Constrain life-support alarms, animal-status cues, workload, stop-work, readback, and synthetic shift handover."),
    ("ghc-family-aquarium-authority-reservation", "Fail closed around welfare, biosecurity, trade, remedy, law, culture, governance, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_aquarium_intake_provenance.py", "aquarium-intake-provenance"),
    ("ghc_family_aquarium_life_support_topology.py", "aquarium-life-support-topology"),
    ("ghc_family_aquarium_water_observation.py", "aquarium-water-observation"),
    ("ghc_family_aquarium_energy_isolation.py", "aquarium-electrical-isolation"),
    ("ghc_family_aquarium_welfare_observation.py", "aquarium-welfare-observation"),
    ("ghc_family_aquarium_biosecurity_hold.py", "aquarium-biosecurity-boundary"),
    ("ghc_family_aquarium_source_correction.py", "aquarium-correction-chain"),
    ("ghc_family_aquarium_accessibility_privacy.py", "aquarium-accessible-notice"),
    ("ghc_family_aquarium_thos_handover.py", "thos-aquarium-handover"),
    ("ghc_family_aquarium_authority_reservation.py", "cbr-aquarium-authority-covenant"),
]


def negative(number: int, slug: str, failure: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6575-X1-N{number:02d}",
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
    negative(1, "combined-source-state-wrapper-no-attributable-output", "The first combined branch, head, upstream, status, and baton-existence wrapper completed without attributable output.", "Split immutable head, live equality, tracked state, untracked state, and baton probes into bounded scalar calls.", "Do not bind slow Git status and network-independent source claims to one short wrapper."),
    negative(2, "default-console-decoding-mojibake", "The first baton metadata probe rendered its UTF-8 heading with a mojibake em dash.", "Read the baton explicitly as UTF-8 in bounded ordered chunks and verify its exact Git blob.", "Declare text encoding for every induction, baton, and lifecycle read."),
    negative(3, "baton-middle-chunk-output-truncation", "A 300-line middle baton chunk exceeded the useful output budget and hid part of the ordered proposal text.", "Reread only the affected range as two 150-line UTF-8 chunks.", "Size long document reads by byte and token budget before dispatch."),
    negative(4, "skill-file-regex-inventory-empty", "The first recursive SKILL.md filename filter produced no attributable matches despite installed family controls.", "Enumerate only the top-level skill directories, select exact names, and then read each required SKILL.md and reference directly.", "Treat an empty discovery pipeline as zero-credit until exact known paths are checked."),
    negative(5, "powershell-foreach-direct-pipeline-parser-error", "A read-only reference metadata probe used a direct foreach-to-pipeline form that PowerShell rejected before execution.", "Materialize foreach output into a bounded array before piping it to JSON serialization.", "Materialize compound PowerShell iteration results before downstream pipelines."),
    negative(6, "manifest-exclusion-object-shape-assumption", "The first cross-manifest exclusion parser assumed every exclusion was an object with a path field; four x1 string exclusions generated null-key diagnostics.", "Inspect exclusion shapes and normalize string and object forms separately without replaying successful blob comparisons.", "Inspect JSON key and value shapes before generic traversal."),
    negative(7, "x1-exclusion-path-domain-false-missing", "The first isolated x1 exclusion check treated phase-relative paths as repository-relative and falsely reported four missing files.", "Prefix x1 lifecycle exclusions with the declared phase root, then verify the normalized tree paths.", "Bind every path comparison to its declared path domain."),
    negative(8, "candidate-practice-neighbor-collisions", "Horology, garment or costume, observatory, planetarium, bookbinding, darkroom, and seed-bank practice candidates collided with inherited proposal families and received no novelty credit.", "Select the aquarium life-support and animal-observation lens, then run every title against all 2,530 frozen rows at the unchanged threshold.", "Perform domain and lexical neighbor screening before writing proposal dossiers."),
    negative(9, "direct-cites-appendices-open-internal-error", "A direct read-only open of the CITES appendices page returned an internal tool error and no source evidence.", "Do not rely on the failed page; keep trade legality exact-gated and use only successfully resolved official sources.", "A failed source open never becomes citation or current-status credit."),
    negative(10, "direct-aza-standards-open-internal-error", "A direct read-only open of the guessed AZA standards URL returned an internal tool error and no source evidence.", "Resolve the official AZA accreditation materials and animal-care manual pages through bounded official-domain search.", "Verify official document locations through a successful current page before recording status."),
    negative(11, "guessed-workflow-schema-filename-missing", "A read-only lookup guessed workflow-plan.schema.json, which is not an installed reference and produced no schema evidence.", "Enumerate the exact skill directory and read workflow-plan-schema.md before constructing the request.", "Resolve installed reference filenames before reading them."),
    negative(12, "unicode-regex-double-quoted-powershell-parse-error", "A read-only mojibake scan used a double-quoted Unicode alternation that PowerShell rejected before execution.", "Repeat the bounded scan with a single-quoted literal pattern.", "Use single-quoted literal patterns for Unicode regex probes in PowerShell."),
    negative(13, "unicode-rendered-large-patch-context-mismatch", "The first large workflow rewrite hunk did not apply because the console-rendered Unicode context did not byte-match the UTF-8 source.", "Use exact ASCII function markers, retain the inherited block as noncalled compatibility text, and add the current implementation at a stable boundary.", "Keep semantic patch contexts short and ASCII-stable when inherited text contains non-ASCII characters."),
    negative(14, "mixed-unicode-multihunk-patch-context-mismatch", "A later mixed cleanup hunk was rejected at the inherited index heading even though its ASCII subchanges were valid.", "Apply ASCII-only semantic hunks separately and audit the remaining Unicode line by code point.", "Do not combine independent ASCII edits with a Unicode-sensitive context line."),
    negative(15, "unicode-heading-single-hunk-context-mismatch", "A one-line heading patch still failed because the patch channel rendered the em dash differently from the UTF-8 source context.", "Retain the generated-content correction in the current overview and remove the unused legacy block with an ASCII marker-bounded cleanup.", "Avoid depending on a non-ASCII glyph as the sole patch anchor."),
    negative(16, "source-x1-gap-register-key-shape-mismatch", "The first x1 builder run expected an effective_count key in Sable's preregistration gap register and stopped before proposal artifacts were written.", "Read Sable's realized x2 gap and exact-gate registers, which carry the sealed effective counts of 108 and 107.", "Select inherited truth registers by lifecycle state and inspect their keys before scalar comparison."),
    negative(17, "proposal-27-semantic-neighbor-rejection", "The first 2,530-row novelty audit rejected proposal 27 at Jaccard 0.7083 against Sable's purpose-scoped organ-record permit.", "Replace the inherited permit pattern with an observation-batch provenance capsule and rerun the unchanged 0.60 audit.", "Do not reuse a predecessor's purpose, audience, scope, expiry, and nonauthorization mechanism bundle."),
    negative(18, "cp1252-proposal-title-output-fault", "A bounded proposal-title diagnostic encountered an unencodable Māori character under the default CP1252 console after printing earlier rows.", "Use UTF-8 output or ASCII-safe JSON diagnostics and do not treat the partial listing as complete.", "Set UTF-8 explicitly before emitting proposal text that may contain Māori orthography."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6575-SAFE-{index:03d}",
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
        "task_id": f"V6575-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6575-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, stale-label, and nonpromotion cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
