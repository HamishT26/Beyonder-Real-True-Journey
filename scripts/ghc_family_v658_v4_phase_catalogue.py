#!/usr/bin/env python3
"""Frozen x1 catalogue for Eiren Kestrel's solo v658-v4 phase."""

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
        "observed_on": "2026-08-02",
        "use": use,
    }


OFFICIAL_SOURCES = [
    source(
        "WMO-GHP-168",
        "Guide to Hydrological Practices, Volume I: Hydrology - From Measurement to Hydrological Information",
        "World Meteorological Organization",
        "https://community.wmo.int/site/knowledge-hub/programmes-and-initiatives/water-resources-assessment/hydrology-publications",
        "current_catalogue",
        "hydrological observing-network, station, stage, discharge, uncertainty, metadata, quality, and publication vocabulary only; no field method, measurement, forecast, or professional endorsement",
    ),
    source(
        "WMO-MSG-1044",
        "Manual on Stream Gauging, Volumes I and II",
        "World Meteorological Organization",
        "https://community.wmo.int/site/knowledge-hub/programmes-and-initiatives/water-resources-assessment/hydrology-publications",
        "current_catalogue",
        "stream-gauging, cross-section, velocity, discharge-computation, rating, field-note, and quality vocabulary only; no real gauging instruction, safety decision, or conformance claim",
    ),
    source(
        "USGS-STREAMGAGING-BASICS",
        "Streamgaging Basics",
        "U.S. Geological Survey",
        "https://www.usgs.gov/mission-areas/water-resources/science/streamgaging-basics",
        "current",
        "stage, discharge, station, sensor, cross-section, and stage-discharge relationship context only; no real measurement, rating, publication, or safety result",
    ),
    source(
        "USGS-TM3-A8",
        "Discharge measurements at gaging stations",
        "U.S. Geological Survey",
        "https://pubs.usgs.gov/publication/tm3A8",
        "published",
        "discharge-measurement note, instrument, subsection, uncertainty, and review vocabulary only; no field procedure, operational release, or professional competence",
    ),
    source(
        "OGC-OMS-3",
        "Observations, Measurements, and Samples",
        "Open Geospatial Consortium",
        "https://www.ogc.org/publications/standard/om/",
        "current",
        "feature-of-interest, observation, procedure, observed-property, result, sampling, and metadata vocabulary only; no implementation-conformance or real-observation claim",
    ),
    source(
        "OGC-SENSORTHINGS-11",
        "OGC SensorThings API Part 1: Sensing, version 1.1",
        "Open Geospatial Consortium",
        "https://www.ogc.org/standards/sensorthings/",
        "current",
        "thing, location, datastream, sensor, observed-property, observation, and feature-of-interest vocabulary only; no live endpoint, device, tasking, interoperability, or security claim",
    ),
    source(
        "OGC-WATERML-20",
        "OGC WaterML 2.0",
        "Open Geospatial Consortium",
        "https://www.ogc.org/standards/waterml/",
        "current",
        "water-observation timeseries, ratings, gaugings, and sections exchange vocabulary only; no network transport, schema conformance, or real-row interoperability result",
    ),
    source(
        "OGC-OM-TIMESERIES",
        "Timeseries Profile of Observations and Measurements",
        "Open Geospatial Consortium",
        "https://docs.ogc.org/is/15-043r3/15-043r3.html",
        "published",
        "timeseries domain, interpolation, metadata, phenomenon-time, result-time, and observation-context vocabulary only; no conformance or operational release",
    ),
    source(
        "W3C-PROV",
        "PROV-O: The PROV Ontology",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        "entity, activity, agent-placeholder, derivation, revision, invalidation, generation, and attribution lineage",
    ),
    source(
        "W3C-WCAG-22",
        "Web Content Accessibility Guidelines 2.2",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/WCAG22/",
        "current",
        "machine-checkable accessibility structure and notice vocabulary; manual, assistive-technology, Māori-language, cognitive, and affected-user evaluation remain reserved",
    ),
    source(
        "W3C-VC-DM-20",
        "Verifiable Credentials Data Model v2.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-model-2.0/",
        "current",
        "synthetic issuer, holder, subject, validity, status, evidence, terms, and disclosure vocabulary only; no live identity, proof, trust, or interoperability",
    ),
    source(
        "W3C-DATA-INTEGRITY",
        "Verifiable Credential Data Integrity 1.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-integrity/",
        "current",
        "synthetic proof-configuration and verification-result vocabulary only; no key, signature, proof, security, trust, or interoperability claim",
    ),
    source(
        "RFC-3339",
        "Date and Time on the Internet: Timestamps",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic observation, correction, validity, expiry, synchronization, and handover timestamps",
    ),
    source(
        "RFC-8785",
        "JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic JSON representation vocabulary only; no cryptographic, signing, or production assurance",
    ),
    source(
        "NIST-SP811",
        "Guide for the Use of the International System of Units",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/publications/guide-use-international-system-units-si",
        "stable",
        "quantity, unit, symbol, rounding, conversion, time, length, area, velocity, flow, and uncertainty discipline only; no real metrology or calibration",
    ),
    source(
        "NZ-PRIVACY-PRINCIPLES",
        "Privacy principles",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        "purpose, minimization, source, notice, access, correction, retention, use, disclosure, and identifier reservations only; no legal advice or compliance finding",
    ),
    source(
        "NZ-NPS-FM",
        "National Policy Statement for Freshwater Management 2020",
        "New Zealand Ministry for the Environment",
        "https://environment.govt.nz/acts-and-regulations/national-policy-statements/national-policy-statement-freshwater-management/",
        "in_force_current_watch",
        "freshwater-monitoring, reporting, Te Mana o te Wai, local-authority, and affected-community reservation context only; no legal interpretation, monitoring decision, or authority transfer",
    ),
    source(
        "TE-MANA-RARAUNGA",
        "Principles of Māori Data Sovereignty",
        "Te Mana Raraunga",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "current",
        "Māori data-rights, interests, governance, jurisdiction, language, collective benefit, and authority reservation only; never a substitute for tangata whenua, iwi, hapū, or Māori authority",
    ),
    source(
        "LOCAL-CONTEXTS-TK",
        "Traditional Knowledge Labels",
        "Local Contexts",
        "https://localcontexts.org/labels/traditional-knowledge-labels/",
        "current_watch",
        "community-defined traditional-knowledge notice and authority-reservation context only; no label selection, wording, application, or community decision",
    ),
]


PROTECTED_GATES = [
    "real_hydrologists_hydrographers_technicians_engineers_landowners_workers_communities_and_affected_parties",
    "real_rivers_streams_catchments_stations_reaches_controls_benchmarks_sensors_loggers_telemetry_equipment_and_records",
    "real_site_access_survey_installation_measurement_gauging_calibration_maintenance_repair_sampling_publication_or_forecast",
    "flood_swift_water_electrical_traffic_height_weather_biosecurity_contamination_and_remote_field_safety",
    "professional_hydrology_hydrometry_surveying_engineering_science_safety_privacy_security_or_accessibility_authority",
    "water_allocation_resource_consent_land_access_property_emergency_warning_liability_or_legal_interpretation",
    "freshwater_relationships_sensitive_locations_traditional_knowledge_taonga_collective_interests_and_community_protocols",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_language_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "empirical_gmut_prediction_constraint_force_flow_or_material_law",
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
) -> dict:
    if number <= 23:
        expected_disposition = "completed"
        approval = "safe_now_bounded_structural_formal_or_synthetic_software"
        lane = "x2_owner_local_bounded_synthetic"
    elif number <= 28:
        expected_disposition = "represented"
        approval = "candidate_proxy_protocol_or_nonproduction_schema"
        lane = "x2_owner_local_representation_only"
    elif number == 29:
        expected_disposition = "open_gap"
        approval = "candidate_external_standards_readiness_without_network_or_real_rows"
        lane = "x2_owner_local_zero_row_readiness"
    else:
        expected_disposition = "exact_gate"
        approval = "outside_hamish_authority_affected_party_land_water_legal_cultural_and_maori_authority_required"
        lane = "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6584-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable synthetic obligations while refusing unsupported "
            "real-water, empirical, participant, professional, safety, production, legal, cultural, Māori-authority, "
            "privacy-complete, accessibility-complete, identity, Theory-of-Everything, or Stage 20 promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, erases a failure, or "
            "crosses a protected person, waterbody, station, land, instrument, measurement, safety, rights, professional, "
            "empirical, production, legal, cultural, Māori-authority, identity, privacy, accessibility, security, "
            "Theory-of-Everything, or Stage 20 gate."
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
            "The valid synthetic fixture passes, five preregistered mutations are rejected, and the receipt grants no "
            "real person, river, stream, station, land, sensor, record, measurement, field action, safety, professional, "
            "production, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-"
            "security, independent-reproduction, Theory-of-Everything, or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real people, waterbodies, land, "
            "stations, instruments, records, sibling lanes, external systems, rights, safety, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Hydrometric scope card with synthetic reach token, observed-property list, unknown station state, evidence ceiling, access refusal, abort predicate, and zero-field action", "hydrometry-scope-card", "THOS Body and CBR Heart", "hydrometric purpose, synthetic reach token, observed-property list, unknown station state, evidence ceiling, access refusal, abort predicate, and zero-field-action lock", ["WMO-GHP-168", "OGC-OMS-3", "W3C-PROV"]),
    ("Stream-gauge station, reach, cross-section, control, sensor, and recorder identity passport with alias-collision quarantine", "hydrometry-station-passport", "Freed ID and GMUT Mind", "station, reach, cross-section, control, sensor, recorder, synthetic identifier alias, correction, and collision quarantine", ["WMO-GHP-168", "OGC-OMS-3", "W3C-PROV"]),
    ("Gauge datum, benchmark, reference mark, elevation placeholder, survey lineage, disturbance cue, and no-geodetic conclusion", "hydrometry-datum-lineage", "Freed ID and GMUT Mind", "gauge datum, benchmark, reference mark, elevation placeholder, survey lineage, disturbance cue, uncertainty, and geodetic-conclusion refusal", ["WMO-MSG-1044", "W3C-PROV", "NIST-SP811"]),
    ("Water-level sensor, data logger, power, telemetry, enclosure, port, channel, firmware placeholder, and dependency topology", "hydrometry-sensor-topology", "THOS Body and Freed ID", "water-level sensor, data logger, power, telemetry, enclosure, port, channel, firmware placeholder, dependency, and operation refusal", ["OGC-SENSORTHINGS-11", "WMO-GHP-168", "W3C-PROV"]),
    ("Stage observation series with unit, datum link, phenomenon time, result time, interval, qualifier, and no-water-level claim", "hydrometry-stage-series", "GMUT Mind", "stage observation series, unit, datum link, phenomenon time, result time, interval, qualifier, missingness, and water-level-claim refusal", ["OGC-OM-TIMESERIES", "OGC-WATERML-20", "RFC-3339"]),
    ("Staff-gauge comparison and readback docket with observed-difference placeholder, correction path, uncertainty, and no-accuracy determination", "hydrometry-staff-gauge-readback", "THOS Body and GMUT Mind", "staff-gauge comparison, readback, observed-difference placeholder, correction path, uncertainty, evidence hold, and accuracy-determination refusal", ["WMO-MSG-1044", "USGS-STREAMGAGING-BASICS", "W3C-PROV"]),
    ("Pressure-transducer configuration with vent state, range, barometric-compensation placeholder, drift cue, and no-calibration verdict", "hydrometry-pressure-transducer", "GMUT Mind and THOS Body", "pressure-transducer configuration, vent state, range, barometric-compensation placeholder, drift cue, uncertainty, and calibration-verdict refusal", ["WMO-GHP-168", "OGC-SENSORTHINGS-11", "NIST-SP811"]),
    ("Radar and ultrasonic stage-sensor interface with mounting reference, beam path, dead-zone placeholder, obstruction cue, and no-installation instruction", "hydrometry-noncontact-sensor", "THOS Body and GMUT Mind", "radar and ultrasonic stage-sensor interface, mounting reference, beam path, dead-zone placeholder, obstruction cue, mismatch hold, and installation-instruction refusal", ["USGS-STREAMGAGING-BASICS", "OGC-SENSORTHINGS-11", "W3C-PROV"]),
    ("Stilling-well, intake, orifice, float, pulley, encoder, equalization, blockage cue, and no-maintenance instruction topology", "hydrometry-stilling-well-topology", "THOS Body", "stilling well, intake, orifice, float, pulley, encoder, equalization, blockage cue, dependency, and maintenance-instruction refusal", ["USGS-STREAMGAGING-BASICS", "WMO-GHP-168", "W3C-PROV"]),
    ("Channel cross-section, bank edge, vertical, subsection, stationing, depth placeholder, bed-profile uncertainty, and no-survey claim", "hydrometry-cross-section", "GMUT Mind", "channel cross-section, bank edge, vertical, subsection, stationing, depth placeholder, bed-profile uncertainty, and survey-claim refusal", ["WMO-MSG-1044", "USGS-TM3-A8", "NIST-SP811"]),
    ("Current-meter instrument equation, rotation count, elapsed time, depth position, calibration placeholder, and no-velocity conclusion", "hydrometry-current-meter", "GMUT Mind and THOS Body", "current-meter instrument equation, rotation count, elapsed time, depth position, calibration placeholder, uncertainty, and velocity-conclusion refusal", ["WMO-MSG-1044", "USGS-TM3-A8", "NIST-SP811"]),
    ("ADCP transect, ensemble, bin, beam, bottom track, edge estimate, moving-bed-test reservation, and no-discharge verdict", "hydrometry-adcp-transect", "GMUT Mind and THOS Body", "ADCP transect, ensemble, bin, beam, bottom track, edge estimate, moving-bed-test reservation, uncertainty, and discharge-verdict refusal", ["WMO-MSG-1044", "USGS-TM3-A8", "W3C-PROV"]),
    ("Midsection discharge computation graph with width, depth, velocity placeholders, subsection sum, unit, residual, and zero measured-flow claim", "hydrometry-discharge-graph", "GMUT Mind", "midsection discharge computation graph, width, depth, velocity placeholders, subsection sum, unit, residual, and measured-flow-claim refusal", ["WMO-MSG-1044", "USGS-TM3-A8", "NIST-SP811"]),
    ("Rating-curve version, segment, hydraulic control, breakpoint, shift, validity interval, supersession, and no-operational release", "hydrometry-rating-lineage", "GMUT Mind and Freed ID", "rating-curve version, segment, hydraulic control, breakpoint, shift, validity interval, supersession, provenance, and operational-release refusal", ["OGC-WATERML-20", "USGS-STREAMGAGING-BASICS", "W3C-PROV"]),
    ("Rating-table interpolation and extrapolation domain with stage bounds, gap state, uncertainty cue, and no-flood-flow estimate", "hydrometry-rating-domain", "GMUT Mind", "rating-table interpolation and extrapolation domain, stage bounds, gap state, uncertainty cue, model-form hold, and flood-flow-estimate refusal", ["OGC-WATERML-20", "OGC-OM-TIMESERIES", "USGS-STREAMGAGING-BASICS"]),
    ("Channel-control change observations for vegetation, debris, ice, scour, deposition, backwater, hysteresis, and no-causal diagnosis", "hydrometry-control-change", "GMUT Mind and THOS Body", "channel-control change observations, vegetation, debris, ice, scour, deposition, backwater, hysteresis, uncertainty, and causal-diagnosis refusal", ["USGS-STREAMGAGING-BASICS", "WMO-GHP-168", "W3C-PROV"]),
    ("Hydrometric quality-control rail for gap, spike, flatline, repetition, reversal, rate-of-change, quarantine, and no-data repair", "hydrometry-quality-rail", "THOS Body and GMUT Mind", "hydrometric gap, spike, flatline, repetition, reversal, rate-of-change, quarantine, correction lineage, and data-repair refusal", ["WMO-GHP-168", "OGC-OM-TIMESERIES", "W3C-PROV"]),
    ("Recorder clock and observation timebase ledger with UTC offset, drift placeholder, sync event, interval, ambiguity, and no-time correction", "hydrometry-timebase", "GMUT Mind and Freed ID", "recorder clock, observation timebase, UTC offset, drift placeholder, sync event, interval, ambiguity, and time-correction refusal", ["RFC-3339", "OGC-OM-TIMESERIES", "W3C-PROV"]),
    ("Hydrometric uncertainty budget with source class, random and systematic placeholders, precision, rounding, qualifier, and no-accuracy claim", "hydrometry-uncertainty-budget", "GMUT Mind", "hydrometric uncertainty budget, source class, random and systematic placeholders, precision, rounding, qualifier, and accuracy-claim refusal", ["NIST-SP811", "WMO-GHP-168", "USGS-TM3-A8"]),
    ("Hydrometric field-note provenance with synthetic visit token, observation placeholder, attachment absence, correction lineage, and no-field evidence", "hydrometry-field-note-lineage", "Freed ID and THOS Body", "hydrometric field-note provenance, synthetic visit token, observation placeholder, attachment absence, correction lineage, invalidation, and field-evidence refusal", ["WMO-MSG-1044", "W3C-PROV", "RFC-3339"]),
    ("Station maintenance, calibration, inspection, fault, replacement, firmware, service-event history, and no-professional competence claim", "hydrometry-maintenance-history", "THOS Body and Freed ID", "station maintenance, calibration, inspection, fault, replacement, firmware, service-event history, evidence hold, and professional-competence refusal", ["WMO-GHP-168", "OGC-SENSORTHINGS-11", "W3C-PROV"]),
    ("GMUT typed stage-discharge observation operator with state, domain, control placeholder, residual, identifiability hold, and empirical firewall", "hydrometry-gmut-operator", "GMUT Mind", "typed stage-discharge observation operator, state, domain, hydraulic-control placeholder, residual, identifiability hold, unit discipline, and empirical firewall", ["OGC-WATERML-20", "NIST-SP811", "RFC-8785"]),
    ("Structurally accessible stage-rating change atlas with scoped tables, provenance links, noncolour quality flags, reflow and print fallback, and manual-evaluation reservation", "hydrometry-accessible-atlas", "CBR Heart and THOS Body", "accessible stage-rating change atlas, scoped tables, provenance links, noncolour quality flags, reflow, print fallback, and manual-evaluation reservation", ["W3C-WCAG-22", "W3C-PROV", "NZ-PRIVACY-PRINCIPLES"]),
    ("THOS synthetic hydrographer field-to-office evidence relay with orphan-note quarantine, reciprocal readback, interruption budget, escalation timer, and no-worker outcome", "thos-hydrometry-evidence-relay", "THOS Body", "synthetic field-to-office evidence relay, orphan-note quarantine, reciprocal readback, interruption budget, escalation timer, handover, and worker-outcome refusal", ["RFC-3339", "W3C-PROV", "W3C-WCAG-22"]),
    ("THOS synthetic telemetry outage, missing-interval triage, backfill quarantine, resumption, workload, recovery, and no-effectiveness estimate", "thos-hydrometry-outage-recovery", "THOS Body and CBR Heart", "synthetic telemetry outage, missing-interval triage, backfill quarantine, resumption, workload, recovery, escalation, and effectiveness-estimate refusal", ["OGC-SENSORTHINGS-11", "RFC-3339", "W3C-PROV"]),
    ("Freed ID synthetic hydrometric sensor-event statement with device placeholder, event digest, validity, status, expiry, revocation hold, and no-live-proof claim", "freed-id-hydrometry-sensor-event", "Freed ID", "synthetic hydrometric sensor-event statement, device placeholder, event digest, validity, status, expiry, revocation hold, and live-proof refusal", ["W3C-VC-DM-20", "W3C-DATA-INTEGRITY", "RFC-3339"]),
    ("Freed ID hydrometric coarse-location escrow policy with spatial-generalization ladder, release-purpose lease, redaction lineage, challenge route, and no-access authorization", "freed-id-hydrometry-location-escrow", "Freed ID and CBR Heart", "hydrometric coarse-location escrow, spatial-generalization ladder, release-purpose lease, redaction lineage, challenge route, remedy pointer, and access-authorization refusal", ["NZ-PRIVACY-PRINCIPLES", "W3C-VC-DM-20", "W3C-PROV"]),
    ("Freed ID hydrometric observation-amendment challenge receipt with prior digest, reason class, review placeholder, invalidation, and no-trust decision", "freed-id-hydrometry-amendment", "Freed ID and THOS Body", "hydrometric observation-amendment challenge receipt, prior digest, reason class, review placeholder, invalidation, correction, and trust-decision refusal", ["W3C-VC-DM-20", "RFC-8785", "W3C-PROV"]),
    ("WMO, OGC OMS, SensorThings, and WaterML hydrometric capability matrix with offline fixtures, version watch, disabled transport, and zero real rows", "hydrometry-standards-capability", "All pillars", "external WMO, OGC OMS, SensorThings, and WaterML capability matrix, offline fixtures, version watch, disabled transport, and zero-real-row boundary", ["WMO-GHP-168", "OGC-OMS-3", "OGC-SENSORTHINGS-11", "OGC-WATERML-20"]),
    ("CBR freshwater station access, land and water relationship, worker safety, sensitive location, publication, remedy, tangata whenua, iwi, hapū, and Māori-data authority covenant", "cbr-hydrometry-authority-covenant", "CBR Heart across all pillars", "freshwater station access, land and water relationship, worker safety, sensitive location, publication, remedy, tangata whenua, iwi, hapū, Māori data, and Māori-authority reservation", ["NZ-NPS-FM", "NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA", "LOCAL-CONTEXTS-TK"]),
]


PROPOSALS = [proposal(index, *spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)]


SKILL_SPECS = [
    ("ghc-family-hydrometry-scope-identity", "Constrain synthetic hydrometric scope, station identity, reach, control, datum, alias, evidence ceiling, and zero-field-action states."),
    ("ghc-family-hydrometry-sensor-topology", "Constrain sensors, recorders, power, telemetry, pressure, noncontact interfaces, stilling-well topology, dependencies, and operation refusal."),
    ("ghc-family-hydrometry-stage-time", "Constrain stage series, datum links, phenomenon and result time, recorder clocks, intervals, drift placeholders, qualifiers, and correction lineage."),
    ("ghc-family-hydrometry-gauging-computation", "Constrain cross-sections, current meters, ADCP structures, subsection computation, units, residuals, and measured-flow refusal."),
    ("ghc-family-hydrometry-rating-quality", "Constrain rating lineage, interpolation domain, control change, uncertainty, quality flags, quarantine, and operational-release refusal."),
    ("ghc-family-hydrometry-field-maintenance", "Constrain synthetic field-note, readback, maintenance, calibration, fault, replacement, correction, and professional-boundary records."),
    ("ghc-family-hydrometry-gmut-firewall", "Keep stage-discharge operators, residuals, identifiability, units, domains, and control placeholders within typed synthetic research bounds."),
    ("ghc-family-hydrometry-thos-relay", "Constrain synthetic evidence relay, orphan quarantine, telemetry outage, workload, interruption, readback, recovery, escalation, and handover."),
    ("ghc-family-hydrometry-freed-id", "Constrain synthetic sensor-event statements, location escrow, amendment challenges, status, expiry, correction, privacy, and nonproduction boundaries."),
    ("ghc-family-hydrometry-authority-reservation", "Fail closed around water and land relationships, site access, worker safety, sensitive locations, publication, affected parties, law, culture, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_hydrometry_scope_identity.py", "hydrometry-scope-card"),
    ("ghc_family_hydrometry_sensor_topology.py", "hydrometry-sensor-topology"),
    ("ghc_family_hydrometry_stage_time.py", "hydrometry-stage-series"),
    ("ghc_family_hydrometry_gauging_computation.py", "hydrometry-cross-section"),
    ("ghc_family_hydrometry_rating_quality.py", "hydrometry-rating-lineage"),
    ("ghc_family_hydrometry_field_maintenance.py", "hydrometry-field-note-lineage"),
    ("ghc_family_hydrometry_gmut_firewall.py", "hydrometry-gmut-operator"),
    ("ghc_family_hydrometry_thos_relay.py", "thos-hydrometry-evidence-relay"),
    ("ghc_family_hydrometry_freed_id.py", "freed-id-hydrometry-sensor-event"),
    ("ghc_family_hydrometry_authority_reservation.py", "cbr-hydrometry-authority-covenant"),
]


def negative(
    number: int,
    slug: str,
    failure: str,
    recovery: str,
    guard: str,
) -> dict:
    return {
        "negative_id": f"V6584-X1-N{number:02d}",
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
    negative(1, "powershell-inline-hashtable-exitcode-parse-fault", "A PowerShell source probe placed command execution and LASTEXITCODE inside one hashtable expression, so parsing failed before Git ran.", "Capture command output and exit code in scalar variables before constructing the receipt object.", "Separate command execution from PowerShell object projection."),
    negative(2, "manifest-replay-powershell-yield-boundary-no-receipt", "The first manifest replay loop crossed the tool yield boundary and returned no attributable receipt; it earned zero manifest credit.", "Audit concrete Git processes and locks, then use one captured ls-tree map per revision with bounded comparison output.", "Require a completed attributable replay receipt before manifest credit."),
    negative(3, "python-c-json-command-quoting-syntax-fault", "An inline Python -c manifest command was mangled by nested JSON and PowerShell quoting and raised a syntax error.", "Send literal source to Python through standard input.", "Use python stdin for multiline repository diagnostics."),
    negative(4, "python-c-native-argument-quote-stripping", "A second Python -c attempt lost embedded quotes through native argument processing and raised a syntax error.", "Pipe the literal script body to python - and rerun only the read-only comparison.", "Do not pass quote-rich multiline code through a native -c argument."),
    negative(5, "stale-global-route-cursor-before-v658-v4", "Global roster, auth, index, reflection, and toolbox snapshots still described the Elowen-to-Sylven cursor even though the newer acknowledged Caelen-to-Eiren baton controlled v658-v4.", "Retain the stale cursor, apply documented precedence to the newest live activation, and defer shared snapshot updates until terminal closeout.", "Compare every shared route cursor against the newest acknowledged live and committed baton before action."),
    negative(6, "unbounded-preregistration-directory-listing-output-truncated", "A broad preregistration directory listing exceeded the output envelope and was truncated, earning no inventory credit.", "Use exact filenames, filtered rg inventories, and bounded counts.", "Never render a large repository directory inventory without a hard bound."),
    negative(7, "frozen-index-records-shape-assumption", "A proposal-index probe assumed a records array and failed because the frozen chain uses prior_proposals plus new_proposals.", "Inspect top-level keys, then concatenate the two declared arrays.", "Inspect JSON keys before traversing inherited ledgers."),
    negative(8, "roster-validator-state-path-guess", "The first roster validation guessed a state subdirectory that does not exist and raised FileNotFoundError.", "Discover the exact skill file inventory and validate references/current-roster.json.", "Resolve referenced paths from SKILL.md or exact inventory before execution."),
    negative(9, "auth-validator-script-name-guess", "The first auth validation guessed a nonexistent script name and earned no validation credit.", "Discover the exact validator filename and invoke validate_auth_permission_state.py with an external D-drive receipt.", "Discover exact skill entrypoints before invoking them."),
    negative(10, "parallel-preflight-wrapper-missing-results", "A parallel preflight wrapper returned empty drive and version results even though its validator branches returned, so it earned no environment credit.", "Run drive and version probes serially through completion.", "Do not combine unrelated preflight branches when each receipt must be attributable."),
    negative(11, "source-status-wrapper-yield-without-clean-receipt", "Combined source status probes yielded without completed tracked-clean results and earned no clean-state credit.", "Use bounded scalar index, untracked, divergence, and live-remote probes, retaining the earlier verified clean receipt.", "Serialize large-worktree terminal Git checks."),
    negative(12, "powershell-upstream-revision-token-mangled", "PowerShell command transport mangled the @{upstream} revision token into an invalid encoded argument.", "Use the explicit origin branch ref for divergence and equality checks.", "Prefer explicit remote refs across command-transport boundaries."),
    negative(13, "git-common-dir-absolute-join-assumption", "A lock audit tried to Join-Path an already absolute git-common-dir and produced an unsupported path format.", "Use the absolute common-dir output directly as a literal path.", "Inspect whether Git paths are absolute before resolving them."),
    negative(14, "post-worktree-composite-inventory-yield", "A post-worktree list and untracked composite probe crossed the yield boundary without attributable output.", "Verify exact head and branch separately and rerun only required scalar cleanliness checks.", "Keep large-worktree registration and cleanliness probes independent."),
    negative(15, "x1-semantic-novelty-rejection", "The first preregistration draft placed V6584-P24 at 0.6111 similarity to Caelen's THOS inspection-handover proposal; the draft earned zero novelty credit.", "Redesign P24 as a field-to-office evidence relay with orphan-note quarantine, reciprocal readback, interruption budget, and escalation timer while preserving the 0.60 threshold.", "Treat novelty rejection as a redesign signal; never weaken the threshold."),
    negative(16, "bounded-rg-inventory-composite-no-output", "Three parallel rg file inventories returned no attributable paths despite exact known files, so the composite earned no inventory credit.", "Use exact Get-Item and filtered Get-ChildItem probes with explicit output limits.", "Require nonempty attributable output before accepting a repository inventory."),
    negative(17, "x1-staged-review-lifecycle-order", "The first exact staged-path comparison found 40 indexed paths but only 38 expected paths because the review and validation receipt were materialized after their expected-set snapshot; it earned zero exact-review credit.", "Rebuild after both lifecycle files exist, restage every changed x1 path, and require exact equality between the materialized expected set and the index.", "Materialize review and receipt layers before the terminal x1 expected-path snapshot."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6584-SAFE-{index:03d}",
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
        "task_id": f"V6584-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6584-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, stale-label, and nonpromotion cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
