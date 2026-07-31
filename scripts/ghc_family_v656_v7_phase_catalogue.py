#!/usr/bin/env python3
"""Frozen x1 catalogue for Neris Solane's v656-v7 phase."""

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
        "USGS-VHP-WHAT-WE-DO",
        "What We Do — Volcano Hazards Program",
        "United States Geological Survey",
        "https://www.usgs.gov/programs/VHP/what-we-do-volcano-hazards-program",
        "current",
        "multi-technique monitoring, observation, warning, assessment, and communication scope vocabulary only",
    ),
    source(
        "GEONET-VOLCANO-HOW",
        "How we monitor volcanoes",
        "GeoNet / Earth Sciences New Zealand",
        "https://www.geonet.org.nz/volcano/how",
        "current",
        "visual, geochemical, seismo-acoustic, deformation, GNSS, InSAR, and environmental-monitoring vocabulary only",
    ),
    source(
        "GEONET-VOLCANO-DATA",
        "Volcano Monitoring data",
        "GeoNet / Earth Sciences New Zealand",
        "https://www.geonet.org.nz/data/types/volcano_monitoring",
        "current",
        "waveform, catalogue, GNSS, camera, time-series, feature-metadata, and Tilde data vocabulary only",
    ),
    source(
        "GEONET-VOLCANO-CAMERA",
        "Camera Images",
        "GeoNet / Earth Sciences New Zealand",
        "https://www.geonet.org.nz/data/types/camera",
        "current",
        "volcano-camera station, view, image interval, archive, and access vocabulary only",
    ),
    source(
        "GEONET-VAL",
        "About Volcanic Alert Levels",
        "GeoNet / Earth Sciences New Zealand",
        "https://www.geonet.org.nz/about/volcano/val",
        "current",
        "New Zealand alert-level vocabulary with every status-setting decision reserved to competent authority",
    ),
    source(
        "USGS-ALERT-SYSTEM",
        "Volcano Alert Level System",
        "United States Geological Survey",
        "https://www.usgs.gov/programs/VHP/alert-level-system",
        "current",
        "ground-hazard alert and aviation-colour-code vocabulary with notification authority reserved",
    ),
    source(
        "USGS-VHP-STRATEGIC-2022-2026",
        "Volcano Hazards Program strategic science plan for 2022–2026",
        "United States Geological Survey",
        "https://www.usgs.gov/publications/volcano-hazards-program-strategic-science-plan-2022-2026",
        "watch",
        "period-bounded monitoring and research priorities; watch-only because the stated plan horizon ends in 2026",
    ),
    source(
        "FDSN-WEBSERVICES-12",
        "FDSN Web Service Specifications 1.2",
        "International Federation of Digital Seismograph Networks",
        "https://www.fdsn.org/webservices/",
        "stable",
        "station, waveform, event, availability, paging, time, and no-data response vocabulary only",
    ),
    source(
        "FDSN-PUBLICATIONS",
        "FDSN data formats and publications",
        "International Federation of Digital Seismograph Networks",
        "https://www.fdsn.org/publications/",
        "current",
        "StationXML, miniSEED 3, source identifier, SeedLink, and citation vocabulary only",
    ),
    source(
        "OGC-SENSORTHINGS-11",
        "OGC SensorThings API Part 1: Sensing Version 1.1",
        "Open Geospatial Consortium",
        "https://docs.ogc.org/is/18-088/18-088.html",
        "stable",
        "thing, sensor, datastream, observed-property, feature-of-interest, and observation vocabulary",
    ),
    source(
        "OGC-SENSORTHINGS-20",
        "OGC SensorThings API Version 2.0 proposed standard",
        "Open Geospatial Consortium",
        "https://www.ogc.org/requests/ogc-seeks-public-comment-on-proposed-ogc-sensorthings-api-version-2-0/",
        "draft",
        "watch-only future alignment; no implementation or conformance claim",
    ),
    source(
        "COPERNICUS-SENTINEL1",
        "Sentinel-1 product documentation",
        "Copernicus Data Space Ecosystem",
        "https://documentation.dataspace.copernicus.eu/Data/Sentinel1.html",
        "current",
        "synthetic SAR product, orbit, burst, processing-level, geometry, and provenance vocabulary only",
    ),
    source(
        "RFC-7946",
        "RFC 7946: The GeoJSON Format",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc7946.html",
        "stable",
        "synthetic geometry, coordinate order, precision, and spatial-boundary vocabulary",
    ),
    source(
        "W3C-PROV-O",
        "PROV-O: The PROV Ontology",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        "entity, activity, agent, derivation, generation, invalidation, revision, and attribution lineage",
    ),
    source(
        "RFC-3339",
        "RFC 3339: Date and Time on the Internet",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic UTC timestamps, intervals, observations, corrections, and handovers",
    ),
    source(
        "RFC-8785",
        "RFC 8785: JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic contract, receipt, and manifest serialization",
    ),
    source(
        "NIST-SP811",
        "NIST SP 811: Guide for the Use of the International System of Units",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/publications/guide-use-international-system-units-si",
        "stable",
        "quantity, unit, symbol, conversion, and uncertainty discipline without real metrology",
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
        "Privacy Act 2020 information privacy principles, including IPP 3A from May 2026",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        "purpose, direct and indirect collection notice, fairness, security, access, correction, retention, use, disclosure, and identifier reservations",
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
    source(
        "C2PA-24",
        "C2PA Content Credentials Technical Specification 2.4",
        "Coalition for Content Provenance and Authenticity",
        "https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html",
        "current",
        "manifest, assertion, ingredient, action, binding, validation, and trust-model vocabulary without signing",
    ),
]


PROTECTED_GATES = [
    "real_people_participants_observers_duty_staff_communities_and_affected_parties",
    "real_volcanoes_whenua_geohazard_sites_stations_samples_images_and_locations",
    "real_monitoring_fieldwork_sampling_aircraft_access_hazard_control_warning_and_stop_work_decisions",
    "real_measurements_calibration_statistics_likelihoods_forecasts_predictions_and_empirical_confirmation",
    "professional_volcanology_seismology_geodesy_geochemistry_aviation_emergency_management_engineering_and_health_and_safety_authority",
    "sensitive_monitoring_location_and_culturally_restricted_information",
    "production_identity_live_keys_proofs_resolution_status_revocation_interoperability_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_indigenous_traditional_knowledge_data_governance_and_maori_authority",
    "affected_party_acceptance_access_benefit_remedy_and_collective_governance",
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
        "proposal_id": f"V6567-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable software obligations while "
            "refusing unsupported geohazard, empirical, professional, identity, legal, cultural, "
            "Māori-authority, production, deployment, or Stage 20 promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, "
            "erases a failure, or crosses a protected empirical, participant, professional, "
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
            "and the receipt grants no real-data, fieldwork, professional, warning, production, "
            "legal, cultural, Māori-authority, identity, accessibility-complete, security-complete, "
            "independent-reproduction, Theory-of-Everything, or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real "
            "people, volcanoes, whenua, stations, samples, devices, accounts, external services, "
            "sibling lanes, hazard decisions, professional decisions, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Volcanic monitoring-site registry with synthetic volcano token, observatory-jurisdiction hold, geometry, observation window, access reservation, correction lineage, and no-hazard-status claim", "volcano-site-registry", "THOS Body and Freed ID", "volcanic monitoring-site registry, synthetic volcano token, observatory-jurisdiction hold, geometry, observation window, access reservation, correction lineage, and hazard-status refusal", ["USGS-VHP-WHAT-WE-DO", "GEONET-VOLCANO-HOW", "RFC-7946", "W3C-PROV-O"]),
    ("Volcanic sensor-station channel docket with network, station, location, channel, orientation, sample-rate, response hold, epoch, and no-fit-for-monitoring release", "volcano-station-channel-docket", "THOS Body and Freed ID", "volcanic sensor-station channel docket, network, station, location, channel, orientation, sample-rate, response hold, epoch, and fit-for-monitoring refusal", ["FDSN-PUBLICATIONS", "FDSN-WEBSERVICES-12", "RFC-3339"]),
    ("Volcanic waveform segment envelope with source identifier, UTC interval, sample count, gap and overlap state, quality flag, checksum, and no-event classification", "volcano-waveform-segment", "GMUT Mind and THOS Body", "volcanic waveform segment envelope, source identifier, UTC interval, sample count, gap and overlap state, quality flag, checksum, and event-classification refusal", ["FDSN-WEBSERVICES-12", "FDSN-PUBLICATIONS", "RFC-3339", "RFC-8785"]),
    ("Volcanic event-catalogue revision ledger with synthetic origin, magnitude-type placeholder, analyst hold, uncertainty, supersession, and no-eruption forecast", "volcano-event-revision-ledger", "GMUT Mind and THOS Body", "volcanic event-catalogue revision ledger, synthetic origin, magnitude-type placeholder, analyst hold, uncertainty, supersession, and eruption-forecast refusal", ["FDSN-WEBSERVICES-12", "GEONET-VOLCANO-DATA", "W3C-PROV-O"]),
    ("Volcanic tremor RSAM and SSAM window board with band definition, aggregation interval, clipping, missingness, instrument-state hold, and no-unrest inference", "volcano-tremor-window-board", "GMUT Mind", "volcanic tremor RSAM and SSAM window board, band definition, aggregation interval, clipping, missingness, instrument-state hold, and unrest-inference refusal", ["GEONET-VOLCANO-HOW", "GEONET-VOLCANO-DATA", "NIST-SP811"]),
    ("Volcanic infrasound association ledger with synthetic array token, geometry hold, arrival time, frequency band, confidence, competing-source cue, and no-explosion confirmation", "volcano-infrasound-association", "GMUT Mind and THOS Body", "volcanic infrasound association ledger, synthetic array token, geometry hold, arrival time, frequency band, confidence, competing-source cue, and explosion-confirmation refusal", ["GEONET-VOLCANO-HOW", "USGS-VHP-WHAT-WE-DO", "RFC-3339"]),
    ("Volcanic GNSS deformation series with reference-frame hold, component units, covariance placeholder, equipment-change epoch, offset quarantine, and no-uplift interpretation", "volcano-gnss-deformation-series", "GMUT Mind and THOS Body", "volcanic GNSS deformation series, reference-frame hold, component units, covariance placeholder, equipment-change epoch, offset quarantine, and uplift-interpretation refusal", ["GEONET-VOLCANO-HOW", "GEONET-VOLCANO-DATA", "NIST-SP811", "RFC-3339"]),
    ("Volcanic InSAR scene-pair lineage with synthetic asset tokens, orbit and burst metadata, temporal and perpendicular baselines, atmosphere hold, unwrapping state, and no-deformation conclusion", "volcano-insar-scene-lineage", "GMUT Mind and Freed ID", "volcanic InSAR scene-pair lineage, synthetic asset tokens, orbit and burst metadata, temporal and perpendicular baselines, atmosphere hold, unwrapping state, and deformation-conclusion refusal", ["COPERNICUS-SENTINEL1", "GEONET-VOLCANO-HOW", "W3C-PROV-O", "C2PA-24"]),
    ("Volcanic tilt and lake-levelling observation docket with benchmark, datum, axis, unit, drift cue, calibration hold, correction path, and no-inflation conclusion", "volcano-tilt-levelling-docket", "GMUT Mind and THOS Body", "volcanic tilt and lake-levelling observation docket, benchmark, datum, axis, unit, drift cue, calibration hold, correction path, and inflation-conclusion refusal", ["GEONET-VOLCANO-HOW", "OGC-SENSORTHINGS-11", "NIST-SP811"]),
    ("Volcanic gas sample and flux custody envelope with synthetic sample token, species, method hold, blank state, wind placeholder, unit, uncertainty, and no-emission-rate claim", "volcano-gas-custody-envelope", "THOS Body and Freed ID", "volcanic gas sample and flux custody envelope, synthetic sample token, species, method hold, blank state, wind placeholder, unit, uncertainty, and emission-rate-claim refusal", ["GEONET-VOLCANO-HOW", "USGS-VHP-WHAT-WE-DO", "W3C-PROV-O", "NIST-SP811"]),
    ("Volcanic fumarole, spring, and crater-lake time-series contract with feature token, observed property, interval, censoring, instrument state, missingness, and no-hazard trend", "volcano-feature-timeseries", "GMUT Mind and THOS Body", "volcanic fumarole, spring, and crater-lake time-series contract, feature token, observed property, interval, censoring, instrument state, missingness, and hazard-trend refusal", ["GEONET-VOLCANO-HOW", "GEONET-VOLCANO-DATA", "OGC-SENSORTHINGS-11"]),
    ("Volcanic camera sequence provenance board with station and view tokens, capture interval, occlusion, clock hold, transformation chain, correction, and no-eruption detection", "volcano-camera-provenance", "Freed ID and THOS Body", "volcanic camera sequence provenance board, station and view tokens, capture interval, occlusion, clock hold, transformation chain, correction, and eruption-detection refusal", ["GEONET-VOLCANO-CAMERA", "W3C-PROV-O", "C2PA-24", "RFC-3339"]),
    ("Volcanic thermal-satellite observation lineage with sensor and product token, pixel footprint, cloud and saturation states, transformation chain, uncertainty, and no-anomaly confirmation", "volcano-thermal-scene-lineage", "GMUT Mind and Freed ID", "volcanic thermal-satellite observation lineage, sensor and product token, pixel footprint, cloud and saturation states, transformation chain, uncertainty, and anomaly-confirmation refusal", ["USGS-VHP-WHAT-WE-DO", "RFC-7946", "W3C-PROV-O", "C2PA-24"]),
    ("Volcanic ash-plume observation envelope with source class, observation time, geometry and altitude units, confidence, aviation-authority hold, and no-VONA issuance", "volcano-ash-observation-envelope", "THOS Body and CBR Heart", "volcanic ash-plume observation envelope, source class, observation time, geometry and altitude units, confidence, aviation-authority hold, and VONA-issuance refusal", ["USGS-ALERT-SYSTEM", "USGS-VHP-WHAT-WE-DO", "RFC-7946", "NIST-SP811"]),
    ("Volcanic lahar and rainfall trigger ledger with synthetic gauge token, window, threshold placeholder, missing-data state, false-trigger cue, competent-review hold, and no-warning release", "volcano-lahar-trigger-ledger", "GMUT Mind and THOS Body", "volcanic lahar and rainfall trigger ledger, synthetic gauge token, window, threshold placeholder, missing-data state, false-trigger cue, competent-review hold, and warning-release refusal", ["USGS-VHP-WHAT-WE-DO", "OGC-SENSORTHINGS-11", "RFC-3339"]),
    ("Volcanic rock, ash, and water sample custody docket with synthetic specimen token, locality-privacy hold, depth or interval, split lineage, laboratory reservation, and no-composition claim", "volcano-sample-custody", "THOS Body and Freed ID", "volcanic rock, ash, and water sample custody docket, synthetic specimen token, locality-privacy hold, depth or interval, split lineage, laboratory reservation, and composition-claim refusal", ["USGS-VHP-WHAT-WE-DO", "GEONET-VOLCANO-HOW", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Observatory device commissioning quarantine card with synthetic asset, calibration epoch, drift flag, measurement span, maintainer hold, and release forbidden", "volcano-instrument-readiness", "THOS Body", "volcanic monitoring-instrument readiness reservation, synthetic device token, quantity, range, unit, calibration epoch, drift cue, quarantine, and fit-for-use refusal", ["OGC-SENSORTHINGS-11", "NIST-SP811", "RFC-3339"]),
    ("Volcanic telemetry-dropout incident choreography with heartbeat, stale-data quarantine, fallback-channel hold, escalation, recovery, correction readback, and no-operational-effectiveness claim", "volcano-telemetry-incident", "THOS Body", "volcanic telemetry-dropout incident choreography, heartbeat, stale-data quarantine, fallback-channel hold, escalation, recovery, correction readback, and operational-effectiveness refusal", ["OGC-SENSORTHINGS-11", "OGC-SENSORTHINGS-20", "RFC-3339"]),
    ("Volcanic observatory duty-shift handover with data freshness, anomaly queue, unresolved disagreement, instrument hold, alert-authority reservation, workload cue, and no-decision substitution", "volcano-duty-handover", "THOS Body and CBR Heart", "volcanic observatory duty-shift handover, data freshness, anomaly queue, unresolved disagreement, instrument hold, alert-authority reservation, workload cue, and decision-substitution refusal", ["USGS-VHP-WHAT-WE-DO", "GEONET-VOLCANO-HOW", "W3C-PROV-O"]),
    ("Volcanic alert-level transition audit with source notice, previous and current values, issue time, reason placeholder, competent-authority hold, supersession, and no-status setting", "volcano-alert-transition-audit", "THOS Body and CBR Heart", "volcanic alert-level transition audit, source notice, previous and current values, issue time, reason placeholder, competent-authority hold, supersession, and status-setting refusal", ["GEONET-VAL", "USGS-ALERT-SYSTEM", "W3C-PROV-O", "RFC-3339"]),
    ("Accessible volcanic public-update structure with headings, status provenance, plain-language placeholder, table associations, nonvisual cues, correction path, and manual and affected-user review reserved", "volcano-accessible-update", "THOS Body and CBR Heart", "accessible volcanic public-update structure, headings, status provenance, plain-language placeholder, table associations, nonvisual cues, correction path, and manual and affected-user review reservation", ["W3C-WCAG-22", "USGS-VHP-WHAT-WE-DO", "GEONET-VAL"]),
    ("Volcano public-report contestation docket with pseudonymous token, minimised context, conflicting account, uncertainty interval, response deadline, and consensus refusal", "volcano-community-correction", "CBR Heart and Freed ID", "community volcanic observation disagreement and correction ledger, report token, source class, privacy minimization, dissent, uncertainty, response window, and consensus-promotion refusal", ["W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES", "USGS-VHP-WHAT-WE-DO"]),
    ("Volcano-location publication deny-list with spatial coarsening, knowledge restriction, audience grant, authority checkpoint, expiry, disclosure audit, and correction", "volcano-restricted-publication", "CBR Heart and Freed ID", "sensitive volcanic monitoring-location and culturally restricted publication firewall, generalization option, audience class, authority hold, expiry, correction, audit cue, and fail-closed disclosure", ["NZ-PRIVACY-PRINCIPLES", "TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "RFC-7946"]),
    ("GMUT synthetic magma-pathway coefficient dimensionality harness with typed domains, transport and reaction parameters, boundary signs, solver quarantine, and likelihood refusal", "gmut-volcanic-conduit-proxy", "GMUT Mind", "GMUT volcanic conduit advection-diffusion-reaction typed proxy, field domains, coefficient units, source and sink signs, boundary conditions, solver hold, and real-likelihood refusal", ["NIST-SP811", "RFC-8785", "USGS-VHP-STRATEGIC-2022-2026"]),
    ("GMUT volcanic elastic and poroelastic deformation typed proxy with state variables, tensor units, interface sign convention, dimensional audit, covariance hold, and no-pressure prediction", "gmut-volcanic-deformation-proxy", "GMUT Mind", "GMUT volcanic elastic and poroelastic deformation typed proxy, state variables, tensor units, interface sign convention, dimensional audit, covariance hold, and pressure-prediction refusal", ["NIST-SP811", "GEONET-VOLCANO-HOW", "RFC-8785"]),
    ("THOS volcanic multi-sensor incident choreography with heartbeat, cross-channel disagreement, stale-input quarantine, escalation, rollback, and no-hazard-decision claim", "thos-volcanic-multisensor-choreography", "THOS Body", "THOS volcanic multi-sensor incident choreography, heartbeat, cross-channel disagreement, stale-input quarantine, escalation, rollback, and hazard-decision refusal", ["USGS-VHP-WHAT-WE-DO", "GEONET-VOLCANO-HOW", "OGC-SENSORTHINGS-11"]),
    ("Freed ID synthetic seismometer consent-and-status envelope with purpose code, audience grant, minimised collection, retention clock, correction, and proof disabled", "freed-id-volcano-sensor-capsule", "Freed ID and CBR Heart", "Freed ID volcanic sensor disclosure capsule, synthetic identifier, purpose, collection hold, audience, retention, correction, status placeholder, and live-proof refusal", ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID remote-sensing asset transformation docket with source frame, edit graph, assertion quarantine, signer disabled, privacy mask, and authenticity refusal", "freed-id-volcano-imagery-plan", "Freed ID", "Freed ID volcanic imagery lineage plan, synthetic asset token, source scene, transformation action, assertion, binding and signer holds, redaction, and authenticity-claim refusal", ["C2PA-24", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("FDSN and GeoNet volcanic-data no-network query tribunal with station, channel, time, and feature placeholders, page-stop invariant, no-data response, citation capture, and zero-row witness", "volcano-zero-row-adapter", "Freed ID and GMUT Mind", "FDSN and GeoNet volcanic-data no-network query tribunal, station, channel, time, and feature placeholders, page-stop invariant, no-data response, citation capture, and zero-row witness", ["FDSN-WEBSERVICES-12", "GEONET-VOLCANO-DATA", "NZ-PRIVACY-PRINCIPLES"]),
    ("CBR observatory non-automation covenant for place relationships, eruption-risk communication, protected mātauranga, equitable benefit, redress, governance, law, culture, and Māori decision authority", "cbr-volcano-authority-matrix", "CBR Heart", "volcanic whenua, geohazard, monitoring, traditional-knowledge, alert, benefit, privacy, access, remedy, legal, cultural, data-governance, and Māori-authority reservation", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES", "GEONET-VAL"]),
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
    ("ghc-family-volcano-site-registry-boundary", "Freeze synthetic site identity, geometry, jurisdiction, access, and hazard-status boundaries."),
    ("ghc-family-volcano-seismic-waveform-boundary", "Separate station metadata, waveform quality, catalogue revision, tremor, and inference."),
    ("ghc-family-volcano-deformation-lineage-boundary", "Track GNSS, InSAR, tilt, datum, frame, covariance, and nonpromotion."),
    ("ghc-family-volcano-geochemistry-custody-boundary", "Preserve gas, water, rock, ash, sample, and method lineage while reserving laboratory authority."),
    ("ghc-family-volcano-imagery-provenance-boundary", "Track camera, thermal, SAR, transformation, occlusion, and authenticity holds."),
    ("ghc-family-volcano-alert-nonpromotion", "Audit alert and ash-message structure without issuing warnings or substituting authority."),
    ("ghc-family-volcano-telemetry-incident-handover", "Handle stale telemetry, cross-channel disagreement, escalation, rollback, and duty handover."),
    ("ghc-family-volcano-accessibility-update", "Generate accessible structural updates while reserving manual and affected-user evaluation."),
    ("ghc-family-volcano-freed-id-disclosure-reserve", "Constrain synthetic sensor identity, disclosure, status, proof, and imagery claims."),
    ("ghc-family-volcano-cultural-authority-reserve", "Fail closed around whenua, restricted knowledge, benefit, remedy, governance, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_volcano_site_registry.py", "volcano-site-registry"),
    ("ghc_family_volcano_seismic_waveform.py", "volcano-waveform-segment"),
    ("ghc_family_volcano_deformation_lineage.py", "volcano-gnss-deformation-series"),
    ("ghc_family_volcano_geochemistry_custody.py", "volcano-gas-custody-envelope"),
    ("ghc_family_volcano_imagery_provenance.py", "volcano-camera-provenance"),
    ("ghc_family_volcano_alert_nonpromotion.py", "volcano-alert-transition-audit"),
    ("ghc_family_volcano_telemetry_handover.py", "volcano-telemetry-incident"),
    ("ghc_family_volcano_accessibility_update.py", "volcano-accessible-update"),
    ("ghc_family_volcano_freed_id_disclosure.py", "freed-id-volcano-sensor-capsule"),
    ("ghc_family_volcano_cultural_authority_reserve.py", "cbr-volcano-authority-matrix"),
]


def negative(number: int, signature: str, observed: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6567-X1-N{number:02d}",
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


X1_OPERATIONAL_NEGATIVES = [
    negative(1, "powershell-host-no-output-timeout", "The first memory, skill, and trivial date probes through the default PowerShell tool host repeatedly exceeded their bounds without producing output.", "Switch to the Node-backed filesystem and direct child-process surface, then use no-profile PowerShell only for narrow Windows-native inspection.", "Test the shell host with one trivial bounded probe and change command surface after a no-output timeout instead of repeating compound reads."),
    negative(2, "combined-node-source-state-outer-timeout", "A combined source head, branch, upstream, status, divergence, and shallow-state probe exceeded the Node tool's thirty-second outer bound.", "Split revision, tracked cleanliness, complete cleanliness, tracking equality, and live-remote checks into isolated scalar probes with explicit outer bounds.", "Never combine large-worktree status traversal with unrelated revision and remote checks under the default outer timeout."),
    negative(3, "archive-wide-external-receipt-search-timeout", "A breadth-first search across the D-drive archive for an external exact-final receipt exceeded its two-minute bound.", "Narrow verification to the exact source worktree, committed receipts, known validation roots, and declared receipt digests.", "Do not recursively search the full archive when exact branches, paths, hashes, and manifest contracts already delimit the evidence."),
    negative(4, "phase-root-limited-manifest-tree-map", "The first 732-entry manifest audit scoped Git tree maps to the phase directory and falsely reported missing script and test blobs.", "Build each manifest comparison map from the complete declared commit tree while retaining the manifest entry allowlist.", "Manifest entries may span phase docs, scripts, and tests; scope by the manifest paths, not by one directory prefix."),
    negative(5, "incomplete-worktree-status-output-overflow", "An early status probe ran while the original large checkout was still populating the worktree and exceeded its four-megabyte output cap.", "Inspect the original Git PID and worktree index, wait for that one checkout to end, then run one full clean-state probe.", "Do not interpret a partially populated worktree status as final state or retry worktree creation while the original process remains active."),
    negative(6, "wmic-process-inspection-unavailable", "The legacy WMIC process-inspection command was unavailable and returned ENOENT.", "Use tasklist plus no-profile Get-CimInstance for bounded Windows process inspection.", "Detect the available Windows process-inspection surface before relying on legacy WMIC."),
    negative(7, "combined-version-probe-spawn-invalid", "A combined Git, Python, Node, Codex, and desktop-package version probe failed process-spawn validation before returning evidence.", "Run each executable separately and read package metadata through a literal path.", "Keep Windows command wrappers and executable probes isolated so one invalid launch cannot erase all version evidence."),
    negative(8, "bundled-codex-executable-direct-spawn-denied", "Direct execution of the desktop-bundled Codex binary was denied by the application package boundary.", "Use the installed npm package metadata for CLI version and the verified WindowsApps package path for desktop version without executing the packaged binary.", "Treat desktop package inspection as status-only and never bypass application-package execution controls."),
    negative(9, "semantic-title-jaccard-collision", "The first x1 build stopped because seven new proposal titles met or exceeded the 0.60 token-set Jaccard collision threshold against inherited wetland-era titles.", "Retain the failed build, revise only the seven colliding titles with domain-specific vocabulary, and rerun the isolated x1 builder.", "Run inherited-title collision screening before freezing x1 and treat domain substitution inside an inherited sentence frame as a collision rather than novelty."),
    negative(10, "windows-console-unicode-inspection-failure", "The first proposal-title inspection attempted to print Māori text through the default Windows cp1252 console and raised UnicodeEncodeError.", "Repeat the narrow inspection with JSON ASCII escaping or an explicitly UTF-8 output surface.", "Use UTF-8 output or JSON ASCII escaping whenever Windows command output may contain Māori or other non-cp1252 text."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6567-SAFE-{index:03d}",
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
        "task_id": f"V6567-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6567-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, and stale-label cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
