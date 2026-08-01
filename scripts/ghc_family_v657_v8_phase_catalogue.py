#!/usr/bin/env python3
"""Frozen x1 catalogue for Tamar Vey's v657-v8 phase."""

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
        "LOC-RFS-2025-2026",
        "Library of Congress Recommended Formats Statement 2025-2026",
        "Library of Congress",
        "https://www.loc.gov/preservation/resources/rfs/",
        "current",
        "format-preference and preservation-context vocabulary only; no appraisal, custody, rights, transfer, or preservation decision",
    ),
    source(
        "LOC-BWF-V2-FDD",
        "Broadcast WAVE Audio File Format, Version 2",
        "Library of Congress",
        "https://www.loc.gov/preservation/digital/formats/fdd/fdd000357.shtml",
        "current",
        "Broadcast WAVE structure and metadata context only; no real file conformance or archival-master determination",
    ),
    source(
        "FADGI-AUDIO",
        "Federal Agencies Digital Guidelines Initiative audio digitization guidance",
        "Federal Agencies Digital Guidelines Initiative",
        "https://www.digitizationguidelines.gov/guidelines/digitize-audioperf.html",
        "current",
        "audio signal-chain, performance, metadata, and quality-control vocabulary only; no real transfer or professional determination",
    ),
    source(
        "IASA-TC04",
        "Guidelines on the Production and Preservation of Digital Audio Objects",
        "International Association of Sound and Audiovisual Archives",
        "https://www.iasa-web.org/tc04/audio-preservation",
        "stable",
        "digital-audio preservation, signal extraction, metadata, identifier, ingest, storage, and access context only",
    ),
    source(
        "IASA-ETHICAL",
        "Ethical Principles for Sound and Audiovisual Archives",
        "International Association of Sound and Audiovisual Archives",
        "https://www.iasa-web.org/ethical-principles",
        "stable",
        "documentation, unmodified preservation transfer, and ethical-reservation context only; no rights clearance or authority",
    ),
    source(
        "ARCHIVES-NZ-DIGITAL-STORAGE",
        "Digital storage policy",
        "Archives New Zealand",
        "https://www.archives.govt.nz/manage-information/how-to-manage-your-information/digital/digital-storage-policy",
        "current",
        "storage, preservation, exit-strategy, privacy, security, Māori-data, and cultural-consideration context only",
    ),
    source(
        "ARCHIVES-NZ-AV-STORAGE",
        "Audiovisual storage guidance",
        "Archives New Zealand",
        "https://www.archives.govt.nz/manage-information/how-to-manage-your-information/implementation/care-and-storage-of-physical-records/audiovisual-storage",
        "current",
        "fragile-carrier identification and storage context only; no handling instruction, deposit decision, or professional assessment",
    ),
    source(
        "ARCHIVES-NZ-PRESERVATION",
        "Best practice guidance on digital storage and preservation",
        "Archives New Zealand",
        "https://www.archives.govt.nz/manage-information/how-to-manage-your-information/digital/best-practice-guidance-on-digital-storage-and-preservation",
        "current",
        "fixity, authenticity, reliability, discoverability, accessibility, usability, protection, and preservation context only",
    ),
    source(
        "LOC-PREMIS-3",
        "PREMIS Data Dictionary for Preservation Metadata, version 3.0",
        "Library of Congress",
        "https://www.loc.gov/standards/premis/v3/",
        "stable",
        "synthetic preservation object, event, agent, and rights metadata vocabulary only",
    ),
    source(
        "LOC-API",
        "Library of Congress JSON/YAML API",
        "Library of Congress",
        "https://www.loc.gov/apis/",
        "current",
        "zero-row audiovisual metadata adapter requirements only; no query, download, ingestion, rights inference, or empirical claim",
    ),
    source(
        "BIPM-SI-BROCHURE",
        "The International System of Units (SI Brochure), ninth edition",
        "Bureau International des Poids et Mesures",
        "https://www.bipm.org/en/publications/si-brochure",
        "current",
        "units, dimensions, quantity-expression, and dimensional-consistency obligations only",
    ),
    source(
        "W3C-PROV-O",
        "PROV-O: The PROV Ontology",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        "entity, activity, agent, attribution, derivation, revision, and invalidation lineage",
    ),
    source(
        "RFC-3339",
        "RFC 3339: Date and Time on the Internet",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic timestamps, transfer windows, expiry, correction, and handover",
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
        "RFC-8493",
        "RFC 8493: The BagIt File Packaging Format",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8493.html",
        "stable",
        "synthetic package, payload, tag-manifest, fetch, and completeness vocabulary only",
    ),
    source(
        "W3C-ODRL-22",
        "ODRL Information Model 2.2",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/odrl-model/",
        "stable",
        "synthetic policy-expression vocabulary only; no copyright, consent, licence, permission, prohibition, duty, or remedy decision",
    ),
    source(
        "W3C-WCAG-22",
        "Web Content Accessibility Guidelines 2.2",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/WCAG22/",
        "current",
        "structural accessibility vocabulary with manual, assistive-technology, Māori-language, cognitive, and affected-user evaluation reserved",
    ),
    source(
        "NZ-PRIVACY-PRINCIPLES",
        "Privacy Act 2020 information privacy principles including IPP 3A",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        "purpose, direct and indirect collection notice, fairness, security, access, correction, retention, use, disclosure, and identifier reservations only",
    ),
    source(
        "TMR-PRINCIPLES",
        "Principles of Māori Data Sovereignty",
        "Te Mana Raraunga",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "current",
        "authority-reservation context only; Māori data, knowledge, voice, governance, and decisions remain under Māori authority",
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
        "W3C-VC-DATA-INTEGRITY-10",
        "Verifiable Credential Data Integrity 1.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-integrity/",
        "current",
        "synthetic proof-configuration and verification-step vocabulary only; no real key, proof, cryptographic assurance, or interoperability",
    ),
    source(
        "W3C-DID-10",
        "Decentralized Identifiers v1.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/did-1.0/",
        "stable",
        "synthetic identifier-document vocabulary only; no live method, resolution, key, controller, service, or trust claim",
    ),
    source(
        "NIST-SP800-61R3",
        "Incident Response Recommendations and Considerations for Cybersecurity Risk Management",
        "National Institute of Standards and Technology",
        "https://csrc.nist.gov/pubs/sp/800/61/r3/final",
        "current",
        "incident, retained-negative, containment, recovery, communication, and handover vocabulary only",
    ),
]


PROTECTED_GATES = [
    "real_archivists_engineers_technicians_performers_speakers_donors_rightsholders_communities_and_affected_parties",
    "real_recordings_magnetic_tapes_carriers_playback_machines_converters_workstations_storage_systems_and_facilities",
    "real_handling_cleaning_repair_playback_transfer_digitization_restoration_ingest_storage_access_disposal_or_return",
    "real_audio_rows_waveforms_measurements_calibrations_likelihoods_predictions_constraints_and_empirical_gmut_confirmation",
    "professional_archival_audio_engineering_conservation_records_management_accessibility_privacy_security_or_workplace_authority",
    "sensitive_voice_identity_location_content_rights_land_heritage_traditional_knowledge_and_culturally_restricted_information",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "copyright_consent_licensing_access_reuse_restriction_remedy_return_repatriation_and_disposal_decisions",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_language_heritage_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_acceptance",
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
    lane = "x2_owner_local_bounded_synthetic"
    if expected_disposition == "open_gap":
        approval = "candidate_external_readiness_without_network_call"
        lane = "x2_owner_local_zero_row_readiness"
    elif expected_disposition == "exact_gate":
        approval = "exact_approval_authorized_affected_party_required"
        lane = "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6578-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable synthetic obligations "
            "while refusing unsupported empirical, participant, professional, safety, security, "
            "accessibility, privacy, identity, production, legal, cultural, Māori-authority, "
            "rights, or Stage 20 promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, "
            "erases a failure, or crosses a protected person, recording, carrier, signal, rights, "
            "empirical, professional, production, legal, cultural, Māori-authority, identity, "
            "privacy, accessibility, security, or Stage 20 gate."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": (
            "The valid synthetic fixture passes, five preregistered mutations are rejected, and "
            "the receipt grants no real person, recording, carrier, signal, measurement, transfer, "
            "rights clearance, professional, production, legal, cultural, Māori-authority, identity, "
            "accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, "
            "Theory-of-Everything, or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real "
            "people, recordings, carriers, machines, signals, records, rights, sibling lanes, "
            "external systems, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Audiovisual transfer request with collection-scope placeholder, purpose minimization, custody precondition, reversible intake state, abort rule, and no-work-start lock", "av-transfer-intake-lock", "Freed ID and CBR Heart", "audiovisual transfer request, purpose minimization, custody precondition, reversible intake, abort, and work-start refusal", ["IASA-TC04", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Magnetic audio carrier identity and condition quarantine with format hypothesis, container relation, label transcription placeholder, uncertainty, correction lineage, and no-authentication rule", "av-carrier-condition-quarantine", "Freed ID and THOS Body", "carrier identity, condition quarantine, format hypothesis, container relation, uncertainty, correction, and authentication refusal", ["ARCHIVES-NZ-AV-STORAGE", "IASA-TC04", "W3C-PROV-O"]),
    ("Playback signal-chain topology with synthetic transport, head, preamplifier, converter, clock, channel map, revision boundary, and no-operation release", "av-playback-topology", "THOS Body and GMUT Mind", "playback topology, component revision, clock, channel map, state quarantine, and operation refusal", ["FADGI-AUDIO", "IASA-TC04", "W3C-PROV-O"]),
    ("Magnetic-head azimuth observation proxy with phase slope, frequency window, reference placeholder, unit, uncertainty, covariance, reversibility, and no-calibration inference", "av-azimuth-phase-proxy", "GMUT Mind", "azimuth phase-slope proxy, frequency window, reference, unit, uncertainty, covariance, reversibility, and calibration refusal", ["FADGI-AUDIO", "BIPM-SI-BROCHURE", "IASA-TC04"]),
    ("Audio sample-clock lineage and drift envelope with nominal rate, observation window, reference epoch, uncertainty, covariance, correction, and no-timing-certification rule", "av-sample-clock-envelope", "GMUT Mind and Freed ID", "sample-clock lineage, drift envelope, reference epoch, uncertainty, covariance, correction, and timing-certification refusal", ["BIPM-SI-BROCHURE", "FADGI-AUDIO", "W3C-PROV-O"]),
    ("Band-limiting and anti-alias obligation board with input bandwidth, transition band, sampling rate, filter placeholder, dimensional checks, and no-fidelity prediction", "av-antialias-obligation", "GMUT Mind", "band limiting, transition band, sampling rate, filter placeholder, dimensional checks, and fidelity-prediction refusal", ["BIPM-SI-BROCHURE", "FADGI-AUDIO", "IASA-TC04"]),
    ("Wow, flutter, and time-base modulation proxy with rate band, deviation convention, windowing, reference tone placeholder, uncertainty, and no-carrier diagnosis", "av-timebase-modulation-proxy", "GMUT Mind", "wow, flutter, time-base modulation, deviation convention, reference placeholder, uncertainty, and carrier-diagnosis refusal", ["FADGI-AUDIO", "BIPM-SI-BROCHURE", "IASA-TC04"]),
    ("Stereo channel polarity, phase coherence, crosstalk cue, assignment ambiguity, correction lineage, and no-content-restoration classifier", "av-channel-coherence", "GMUT Mind and THOS Body", "channel polarity, phase coherence, crosstalk cue, assignment ambiguity, correction, and restoration refusal", ["FADGI-AUDIO", "IASA-TC04", "W3C-PROV-O"]),
    ("Audio reference-level and gain-staging envelope with level convention, impedance placeholder, channel relation, clipping margin, unit, uncertainty, and no-performance grade", "av-reference-level-envelope", "GMUT Mind", "reference level, gain staging, impedance placeholder, clipping margin, units, uncertainty, and performance-grade refusal", ["FADGI-AUDIO", "BIPM-SI-BROCHURE", "IASA-TC04"]),
    ("Noise-floor, signal-to-noise, dynamic-range, weighting-placeholder, silence-window, uncertainty, covariance, and no-authenticity inference board", "av-noise-dynamic-range", "GMUT Mind", "noise floor, signal-to-noise, dynamic range, weighting placeholder, silence window, uncertainty, covariance, and authenticity refusal", ["FADGI-AUDIO", "BIPM-SI-BROCHURE", "IASA-TC04"]),
    ("Audio transfer uncertainty budget with correlated clock, gain, level, timing, channel, dropout, operator-placeholder, and aggregation obligations", "av-uncertainty-covariance", "GMUT Mind", "audio transfer uncertainty budget, correlated sources, covariance, aggregation, and empirical-inference firewall", ["BIPM-SI-BROCHURE", "FADGI-AUDIO", "W3C-PROV-O"]),
    ("Audio degradation identifiability tribunal with carrier, transport, head, electronics, converter, storage, and source-confounding alternatives", "av-identifiability-tribunal", "GMUT Mind", "degradation identifiability, carrier, transport, head, electronics, converter, storage, source confounding, and causal-claim refusal", ["IASA-TC04", "FADGI-AUDIO", "W3C-PROV-O"]),
    ("PCM bit-depth, quantization-step, dither-placeholder, clipping, scaling convention, reversible conversion, and no-audibility claim board", "av-quantization-dither", "GMUT Mind", "PCM bit depth, quantization step, dither placeholder, clipping, scaling, reversible conversion, and audibility-claim refusal", ["LOC-RFS-2025-2026", "FADGI-AUDIO", "BIPM-SI-BROCHURE"]),
    ("PCM frame, block, byte-order, channel-interleave, sample-count, duration-consistency, truncation, and resource-ceiling tribunal", "av-pcm-framing", "THOS Body and GMUT Mind", "PCM framing, byte order, channel interleave, sample count, duration consistency, truncation, and resource-ceiling refusal", ["LOC-BWF-V2-FDD", "FADGI-AUDIO", "RFC-8785"]),
    ("Broadcast WAVE bext and metadata crosswalk with field presence, coding history, originator redaction, time reference, correction, and no-conformance certificate", "av-bwf-metadata-crosswalk", "Freed ID and THOS Body", "Broadcast WAVE metadata crosswalk, field presence, coding history, redaction, time reference, correction, and conformance-certificate refusal", ["LOC-BWF-V2-FDD", "FADGI-AUDIO", "RFC-3339"]),
    ("Multi-algorithm fixity ledger with object scope, algorithm identifier, digest placeholder, verification epoch, mismatch quarantine, and no-authenticity promotion", "av-fixity-ledger", "Freed ID and THOS Body", "multi-algorithm fixity, object scope, digest placeholder, verification epoch, mismatch quarantine, and authenticity-promotion refusal", ["ARCHIVES-NZ-PRESERVATION", "RFC-8785", "W3C-PROV-O"]),
    ("BagIt audiovisual package tribunal with payload inventory, tag manifest, fetch refusal, path confinement, duplicate name, size budget, and completeness boundary", "av-bagit-tribunal", "THOS Body and Freed ID", "BagIt payload, tag manifest, fetch refusal, path confinement, duplicate name, size budget, and completeness boundary", ["RFC-8493", "RFC-8785", "ARCHIVES-NZ-DIGITAL-STORAGE"]),
    ("PREMIS preservation-event graph with synthetic object, event, agent, rights placeholder, outcome, linking identifier, correction, and no-authority claim", "av-premis-event-graph", "Freed ID and CBR Heart", "PREMIS object, event, agent, rights placeholder, outcome, linking identifier, correction, and authority refusal", ["LOC-PREMIS-3", "W3C-PROV-O", "RFC-3339"]),
    ("Audiovisual derivation and invalidation graph with carrier, preservation master, access copy, transcript, event, agent-placeholder, revision, and supersession", "av-prov-derivation", "Freed ID", "audiovisual entity derivation, invalidation, revision, supersession, agent placeholder, and provenance correction", ["W3C-PROV-O", "LOC-PREMIS-3", "RFC-8785"]),
    ("ODRL audiovisual policy-expression parser with asset scope, assignee placeholder, permission, prohibition, duty, conflict, expiry, and no-rights-decision boundary", "av-odrl-policy-parser", "Freed ID and CBR Heart", "ODRL asset, assignee placeholder, permission, prohibition, duty, conflict, expiry, and rights-decision refusal", ["W3C-ODRL-22", "NZ-PRIVACY-PRINCIPLES", "IASA-ETHICAL"]),
    ("Preservation-master and access-derivative separation ledger with transform declaration, checksum scope, loudness-change placeholder, redaction branch, and no-source-overwrite rule", "av-derivative-separation", "Freed ID and THOS Body", "preservation-master and access-derivative separation, transform declaration, fixity scope, redaction branch, and source-overwrite refusal", ["IASA-ETHICAL", "IASA-TC04", "W3C-PROV-O"]),
    ("Audio transcript, caption, speaker-label placeholder, timestamp cue, non-audio alternative, correction route, focus order, and affected-user evaluation reservation", "av-accessibility-transcript", "CBR Heart and THOS Body", "transcript, caption, speaker placeholder, timestamp cue, non-audio alternative, correction, focus order, and affected-user evaluation reservation", ["W3C-WCAG-22", "NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O"]),
    ("Audiovisual incident, dropout, clipping, channel swap, metadata mismatch, correction, evidence preservation, owner, escalation, and shift-handover board", "av-incident-handover", "THOS Body and Freed ID", "audiovisual incident, signal or metadata anomaly, correction, evidence preservation, ownership, escalation, and handover", ["NIST-SP800-61R3", "IASA-TC04", "RFC-3339"]),
    ("THOS audiovisual transfer workload and interruption-recovery proxy with matched synthetic event budget, concealed scoring, abort threshold, reorientation count, and next-shift readback", "thos-av-workload-proxy", "THOS Body", "audiovisual transfer workload, interruption recovery, matched synthetic event budget, concealed scoring, abort threshold, reorientation, and handover", ["NIST-SP800-61R3", "IASA-TC04", "W3C-WCAG-22"]),
    ("Freed ID synthetic audiovisual custody receipt with collection-scope redaction, carrier pseudonym, transfer event, validity window, correction, expiry, and nonproduction boundary", "freed-id-av-custody-receipt", "Freed ID and CBR Heart", "synthetic audiovisual custody credential, scope redaction, pseudonym, transfer event, validity, correction, expiry, and production refusal", ["W3C-VC-DM-20", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID synthetic audiovisual proof-configuration profile with canonicalization boundary, verification relationship, domain, challenge, proof-purpose, algorithm refusal, and no-cryptographic-assurance rule", "freed-id-av-proof-profile", "Freed ID", "synthetic proof configuration, canonicalization, verification relationship, domain, challenge, purpose, algorithm refusal, and cryptographic-assurance refusal", ["W3C-VC-DATA-INTEGRITY-10", "RFC-8785", "W3C-VC-DM-20"]),
    ("Freed ID synthetic archival identifier lifecycle with DID document placeholder, controller separation, resolver refusal, stale cache, status, deactivation, recovery, and trust-governance hold", "freed-id-av-lifecycle", "Freed ID", "synthetic archival identifier lifecycle, controller separation, resolution refusal, stale cache, status, deactivation, recovery, and trust-governance reservation", ["W3C-DID-10", "W3C-VC-DM-20", "NIST-SP800-61R3"]),
    ("Thermo-Psyche magnetic hysteresis, remanence, coercivity, domain-history, signal-memory analogy label, and agency-nonconversion classifier", "thermo-psyche-hysteresis-nonconversion", "GMUT Mind and CBR Heart", "magnetic hysteresis, remanence, coercivity, domain history, signal-memory analogy, and agency nonconversion", ["BIPM-SI-BROCHURE", "IASA-TC04", "W3C-PROV-O"]),
    ("Library of Congress audiovisual API item, resource, format, rights-advisory, contributor, date, language, provenance, and zero-row adapter with no-download and no-rights-inference rule", "loc-av-zero-row-adapter", "GMUT Mind and Freed ID", "Library of Congress audiovisual API schema, provenance, rights advisory, zero-row readiness, download refusal, and rights-inference refusal", ["LOC-API", "LOC-RFS-2025-2026", "W3C-PROV-O"]),
    ("CBR audiovisual voice, performer, donor, community, language, privacy, copyright, consent, access, reuse, restriction, remedy, return, cultural protocol, Māori-data, affected-party, and Māori-authority covenant", "cbr-av-authority-covenant", "CBR Heart", "audiovisual voice, performer, donor, community, language, privacy, rights, consent, access, reuse, restriction, remedy, return, cultural protocol, Māori data, affected-party, and Māori-authority nonautomation", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "ARCHIVES-NZ-DIGITAL-STORAGE", "NZ-PRIVACY-PRINCIPLES", "IASA-ETHICAL"]),
]


PROPOSALS = [
    proposal(
        number,
        title,
        slug,
        pillar,
        mechanism,
        sources,
        "completed"
        if number <= 23
        else "represented"
        if number <= 28
        else "open_gap"
        if number == 29
        else "exact_gate",
    )
    for number, (title, slug, pillar, mechanism, sources) in enumerate(PROPOSAL_SPECS, 1)
]


SKILL_SPECS = [
    ("ghc-family-av-intake-provenance", "Freeze synthetic transfer, carrier, custody, purpose, correction, and no-work-start boundaries."),
    ("ghc-family-av-signal-firewall", "Constrain signal quantities, units, uncertainty, covariance, identifiability, and inference refusal."),
    ("ghc-family-av-carrier-boundary", "Fail closed around real carriers, handling, cleaning, repair, playback, transfer, and professional authority."),
    ("ghc-family-av-package-fixity", "Model synthetic package, manifest, fixity, path, size, mismatch, and completeness boundaries."),
    ("ghc-family-av-preservation-metadata", "Constrain BWF, PREMIS, PROV, derivative, revision, invalidation, and correction surfaces."),
    ("ghc-family-av-shift-handover", "Constrain anomaly, interruption, workload, stop, evidence, ownership, readback, and next-shift handover."),
    ("ghc-family-av-accessibility-privacy", "Structure accessible notices and minimized records while reserving manual and affected-user review."),
    ("ghc-family-av-gmut-firewall", "Keep signal, sampling, modulation, quantization, covariance, and zero-row evidence inside typed research bounds."),
    ("ghc-family-av-freed-id-status", "Constrain synthetic custody, proof, resolution, status, expiry, recovery, and trust without live operations."),
    ("ghc-family-av-authority-reservation", "Fail closed around rights, consent, voice, language, remedy, return, law, culture, governance, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_av_intake_provenance.py", "av-transfer-intake-lock"),
    ("ghc_family_av_signal_firewall.py", "av-uncertainty-covariance"),
    ("ghc_family_av_carrier_boundary.py", "av-carrier-condition-quarantine"),
    ("ghc_family_av_package_fixity.py", "av-bagit-tribunal"),
    ("ghc_family_av_preservation_metadata.py", "av-premis-event-graph"),
    ("ghc_family_av_shift_handover.py", "av-incident-handover"),
    ("ghc_family_av_accessibility_privacy.py", "av-accessibility-transcript"),
    ("ghc_family_av_gmut_firewall.py", "av-antialias-obligation"),
    ("ghc_family_av_freed_id_status.py", "freed-id-av-lifecycle"),
    ("ghc_family_av_authority_reservation.py", "cbr-av-authority-covenant"),
]


def negative(number: int, slug: str, failure: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6578-X1-N{number:02d}",
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
    negative(1, "manifest-verifier-restricted-domain-to-docs", "The first inherited manifest verifier incorrectly limited the tree to documentation paths and reported 4, 23, and 28 false mismatches for scripts and tests.", "Replay each declared path against its exact Git blob across the full tree with cat-file batch checks.", "Never narrow a commit-local manifest to an assumed subtree when the manifest declares repository-relative paths."),
    negative(2, "full-tree-manifest-wrapper-returned-no-attributable-output", "A full-tree manifest wrapper completed without an attributable result, so it earned no verification credit.", "Use bounded cat-file batch-check witnesses and retain per-manifest counts and mismatches.", "Poll every yielded native-command session and preserve all output chunks."),
    negative(3, "guessed-auth-schema-path", "A read-only skill lookup guessed references/schema.md for Auth Permission State, which does not exist.", "Enumerate the exact skill directory and read auth-permission-state-schema.md.", "Never infer reference filenames when an exact skill tree is available."),
    negative(4, "guessed-roster-schema-path", "A read-only skill lookup guessed references/schema.md for Roster Check, which does not exist.", "Enumerate the exact skill directory and read roster-state-schema.md.", "Never infer reference filenames when an exact skill tree is available."),
    negative(5, "activation-baton-single-read-truncation", "The first whole-file activation read exceeded the useful output window and could not prove EOF.", "Read the immutable baton in bounded ordered chunks through its final line.", "Count lines first and use bounded ranges for long activation packets."),
    negative(6, "combined-state-read-output-truncation", "A combined multi-file guidance read exceeded the useful output window and earned no complete-read credit.", "Read each required state and reference independently through EOF.", "Keep exact-head and installed-skill reads attributable to one bounded file at a time."),
    negative(7, "semantic-audit-raw-read-context-overflow", "A raw semantic-novelty audit read exceeded useful context during startup compaction.", "Parse exact keys and rows through bounded scalar and selected-record probes.", "Inspect large JSON by schema and bounded selections rather than raw rendering."),
    negative(8, "parallel-json-probes-yielded-unpolled-inner-sessions", "Five parallel JSON probes yielded inner sessions whose early outputs were not preserved, so their blank wrapper result earned zero credit.", "Poll every returned inner session and concatenate all chunks before attribution.", "Treat session identifiers as incomplete results, never as completed commands."),
    negative(9, "guessed-preregistration-ledger-under-x1", "A read-only lookup guessed x1/proposal-ledger.json, but the exact path is preregistration/proposal-ledger.json.", "Enumerate exact proposal paths with rg --files before parsing.", "Never infer lifecycle subdirectories from historical layouts."),
    negative(10, "combined-preflight-native-command-parser-error", "A combined PowerShell preflight placed native commands and exit-code checks inside expressions and failed before execution.", "Run each native command first, capture LASTEXITCODE into a scalar, then compose the receipt.", "Never embed semicolon-separated native commands inside PowerShell parenthesized expressions or hash values."),
    negative(11, "preflight-wrapper-lost-early-output-chunks", "A yielded preflight wrapper preserved only its final chunk and lost earlier scalar outputs, so it earned no complete receipt credit.", "Accumulate initial and subsequent session output before parsing.", "Always concatenate every exec and poll chunk for long native-command probes."),
    negative(12, "post-worktree-ancestry-parser-error", "The first post-worktree audit repeated the native-command-in-expression PowerShell parser fault before execution.", "Scalarize merge-base status before composing the audit object.", "Apply the scalar native-command guard to every history and equality receipt."),
    negative(13, "overbroad-workflow-json-render-truncated", "A full workflow-refinement JSON rendering exceeded the useful output window and received no complete-read credit.", "Use exact schema keys, counts, policy-check selections, and bounded sections.", "Inspect large lifecycle JSON by declared schema and bounded keys."),
    negative(14, "nist-source-open-internal-error", "The first direct NIST publication page open returned an internal retrieval error.", "Use the stable CSRC final-publication URL already cited by the exact source ledger and make no claim from the failed retrieval.", "Retain failed source retrievals and rely only on independently resolved official pages."),
    negative(15, "cp1252-novelty-output-encoding-failure", "The first complete 2,620-row novelty computation reached output but the CP1252 console could not encode Māori text, so the attempt earned zero audit credit.", "Rerun the same read-only computation with PYTHONIOENCODING=utf-8 and retain the failed output witness.", "Set explicit UTF-8 for Unicode-bearing Python diagnostics before execution."),
    negative(16, "overbroad-test-template-count-replacement", "A mechanical test-template migration replaced both the inherited and effective novelty counts with 2,650 before any test or staging.", "Correct the assertions explicitly to 2,620 inherited and 2,650 effective and retain the failed edit assumption.", "Never chain overlapping numeric replacements; patch semantic fields by name and review the diff immediately."),
    negative(17, "activation-baton-hash-domain-conflation", "The first x1 build bound the activation baton to checkout bytes while the inherited guard correctly required exact committed Git-blob bytes, then failed before packet generation.", "Compute and record the exact Git-blob and checkout SHA-256 domains separately before rerunning.", "Every provenance digest must name and validate its byte domain explicitly."),
    negative(18, "workflow-messaging-boundary-noncanonical-token", "The first generated workflow plan used a truthful custom no-successor phrase where the installed validator requires its canonical existing-task-after-terminal-gate token, so the plan was rejected.", "Use the validator's exact boundary token while preserving the explicit no-successor authorization in the route-state artifact.", "Separate schema vocabulary from phase-specific route state and validate both before credit."),
    negative(19, "stale-domain-scan-included-immutable-frozen-chain", "The first stale-domain scan searched the immutable 2,620-row inherited proposal chain, found legitimate historical optics titles, and truncated its output before an owner-authored conclusion.", "Exclude frozen inherited title payloads and scan only Tamar-authored fields, builders, ledgers, reports, route state, and validation surfaces.", "Scope stale-label review by provenance ownership; never treat inherited evidence vocabulary as a current-owner stale label."),
    negative(20, "name-status-z-alternating-token-parser-assumption", "The first staged-status diagnostic treated Git's NUL-delimited name-status stream as one record per token and falsely classified every path token as a non-added status.", "Use line-based name-status records or parse the alternating status and path tokens as pairs.", "Inspect native output framing before assigning semantic meaning to NUL-delimited tokens."),
    negative(21, "combined-post-stage-wrapper-lost-inner-probe-attribution", "The wrapper that staged the review receipt and then combined diff and status probes yielded after the add, returned only the line-ending warning, and temporarily left two read-only Git probes without attributable completion.", "Wait for the exact read-only Git processes to finish, then run one supervised scalar status or diff probe per session.", "Do not append long read-only audits to a staging command on a large worktree; supervise each postcondition independently."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6578-SAFE-{index:03d}",
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
        "task_id": f"V6578-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6578-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, stale-label, and nonpromotion cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
