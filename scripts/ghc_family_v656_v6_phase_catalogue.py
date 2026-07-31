#!/usr/bin/env python3
"""Frozen x1 catalogue for Elaren Kestrel's v656-v6 phase."""

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
        "RAMSAR-IF-WIAM",
        "Integrated Framework for wetland inventory, assessment and monitoring",
        "Convention on Wetlands",
        "https://www.ramsar.org/document/resolution-ix1-annex-e-integrated-framework-wetland-inventory-assessment-monitoring-if",
        "stable",
        "multi-scale wetland inventory, assessment, monitoring, and management vocabulary only",
    ),
    source(
        "EPA-WETLAND-MONITORING",
        "Wetlands Monitoring and Assessment",
        "United States Environmental Protection Agency",
        "https://www.epa.gov/wetlands/wetlands-monitoring-and-assessment",
        "current",
        "landscape, rapid, and intensive monitoring levels and reference-condition vocabulary only",
    ),
    source(
        "USGS-WATER-API",
        "USGS Water API Documentation",
        "United States Geological Survey",
        "https://api.water.usgs.gov/docs",
        "current",
        "public hydrology API discovery, endpoint, provenance, and zero-row readiness vocabulary only",
    ),
    source(
        "NOAA-COOPS-API",
        "CO-OPS Data API",
        "National Oceanic and Atmospheric Administration",
        "https://api.tidesandcurrents.noaa.gov/api/prod/",
        "current",
        "water-level and environmental-observation API vocabulary only",
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
        "TDWG-DARWIN-CORE",
        "Darwin Core",
        "Biodiversity Information Standards",
        "https://dwc.tdwg.org/",
        "current",
        "biodiversity occurrence, event, location, taxon, and measurement-or-fact vocabulary",
    ),
    source(
        "TDWG-DWC-REVIEW",
        "Darwin Core public review and maintenance cycle",
        "Biodiversity Information Standards",
        "https://www.tdwg.org/",
        "watch",
        "watch-only maintenance context; no draft term is promoted into a stable contract",
    ),
    source(
        "GBIF-OCCURRENCE-API",
        "GBIF Occurrence API",
        "Global Biodiversity Information Facility",
        "https://techdocs.gbif.org/en/openapi/v1/occurrence",
        "current",
        "public occurrence search, pagination, issue flag, attribution, and zero-row readiness vocabulary",
    ),
    source(
        "GBIF-DATA-QUALITY",
        "GBIF data quality recommendations",
        "Global Biodiversity Information Facility",
        "https://techdocs.gbif.org/en/data-publishing/data-quality-recommendations",
        "current",
        "occurrence-data completeness, coordinates, dates, identifiers, and quality-flag vocabulary only",
    ),
    source(
        "RFC-7946",
        "RFC 7946: The GeoJSON Format",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc7946.html",
        "stable",
        "synthetic geospatial feature, geometry, coordinate-order, precision, and uncertainty-reservation vocabulary",
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
        "Privacy Act 2020 information privacy principles",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        "purpose, notice, fairness, security, access, correction, retention, use, disclosure, and identifier reservations",
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
        "RFC-9943",
        "RFC 9943: An Architecture for Trustworthy and Transparent Digital Supply Chains",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc9943.html",
        "stable",
        "statement, transparency-service, registration-policy, and receipt vocabulary without live services",
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
    "real_people_participants_field_workers_landowners_communities_and_affected_parties",
    "real_wetlands_whenua_waterways_species_samples_sensors_images_and_locations",
    "real_field_sampling_restoration_intervention_hazard_control_and_stop_work_decisions",
    "real_measurements_calibration_statistics_likelihoods_predictions_and_empirical_confirmation",
    "professional_ecology_hydrology_restoration_engineering_health_and_safety_authority",
    "sensitive_species_location_and_culturally_restricted_information",
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
        "proposal_id": f"V6566-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable software obligations while "
            "refusing unsupported ecological, empirical, professional, identity, legal, cultural, "
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
            "and the receipt grants no real-data, fieldwork, professional, production, legal, "
            "cultural, Māori-authority, identity, accessibility-complete, security-complete, "
            "independent-reproduction, Theory-of-Everything, or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real "
            "people, places, wetlands, species, samples, devices, accounts, external services, "
            "sibling lanes, professional decisions, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Wetland monitoring-site passport with synthetic site token, classification hold, boundary geometry, observation window, access reservation, correction lineage, and no-condition claim", "wetland-site-passport", "THOS Body and Freed ID", "wetland monitoring-site passport, synthetic site token, classification hold, boundary geometry, observation window, access reservation, correction lineage, and condition-claim refusal", ["RAMSAR-IF-WIAM", "EPA-WETLAND-MONITORING", "RFC-7946", "W3C-PROV-O"]),
    ("Transect and quadrat sampling-frame contract with synthetic frame token, stratum, inclusion rule, effort placeholder, missing-cell state, relocation refusal, and inference hold", "transect-quadrat-frame", "THOS Body and GMUT Mind", "transect and quadrat frame, stratum, inclusion rule, effort placeholder, missing-cell state, relocation refusal, and inference hold", ["EPA-WETLAND-MONITORING", "TDWG-DARWIN-CORE", "W3C-PROV-O"]),
    ("Wetland water-level and hydroperiod observation series with datum hold, unit, timestamp, censoring, missingness, uncertainty, and no-trend promotion", "hydroperiod-observation-series", "GMUT Mind and THOS Body", "water-level and hydroperiod observation series, datum hold, unit, timestamp, censoring, missingness, uncertainty, and trend-claim refusal", ["NOAA-COOPS-API", "OGC-SENSORTHINGS-11", "RFC-3339", "NIST-SP811"]),
    ("Surface-water and groundwater exchange conceptual ledger with boundary direction, flux placeholder, sign convention, closure residual, model-form hold, and no-causal claim", "surface-groundwater-exchange-ledger", "GMUT Mind", "surface-water and groundwater exchange ledger, boundary direction, flux placeholder, sign convention, closure residual, model-form hold, and causal-claim refusal", ["USGS-WATER-API", "RAMSAR-IF-WIAM", "NIST-SP811"]),
    ("Wetland water-quality observation envelope with analyte token, method hold, result unit, detection-limit state, qualifier, custody link, and no-compliance conclusion", "wetland-water-quality-envelope", "GMUT Mind and THOS Body", "water-quality observation envelope, analyte token, method hold, result unit, detection-limit state, qualifier, custody link, and compliance-conclusion refusal", ["USGS-WATER-API", "OGC-SENSORTHINGS-11", "NIST-SP811", "W3C-PROV-O"]),
    ("Sediment, peat, and soil sample custody docket with synthetic sample token, depth interval, container state, preservation hold, split lineage, disposition, and no-laboratory claim", "sediment-peat-soil-custody", "THOS Body and Freed ID", "sediment, peat, and soil sample custody, synthetic sample token, depth interval, container state, preservation hold, split lineage, disposition, and laboratory-claim refusal", ["RAMSAR-IF-WIAM", "W3C-PROV-O", "RFC-3339"]),
    ("Wetland vegetation stratum and cover observation board with taxon placeholder, growth form, cover interval, observer hold, unknown category, disagreement, and no-condition score", "vegetation-stratum-cover-board", "THOS Body and CBR Heart", "vegetation stratum and cover observation, taxon placeholder, growth form, cover interval, observer hold, unknown category, disagreement, and condition-score refusal", ["TDWG-DARWIN-CORE", "GBIF-DATA-QUALITY", "EPA-WETLAND-MONITORING"]),
    ("Invasive-species observation and quarantine ledger with taxon assertion state, evidence hold, duplicate cue, sensitive-location firewall, competent-review reservation, and no-control action", "invasive-species-quarantine-ledger", "THOS Body and CBR Heart", "invasive-species observation and quarantine, taxon assertion state, evidence hold, duplicate cue, sensitive-location firewall, competent-review reservation, and control-action refusal", ["TDWG-DARWIN-CORE", "GBIF-DATA-QUALITY", "NZ-PRIVACY-PRINCIPLES"]),
    ("Fauna acoustic and visual encounter docket with synthetic event token, modality, effort, confidence, ambiguity, media hold, sensitive-species restriction, and no-abundance inference", "fauna-encounter-docket", "THOS Body and CBR Heart", "fauna acoustic and visual encounter docket, synthetic event token, modality, effort, confidence, ambiguity, media hold, sensitive-species restriction, and abundance-inference refusal", ["TDWG-DARWIN-CORE", "GBIF-DATA-QUALITY", "C2PA-24"]),
    ("Environmental-DNA contamination firewall with synthetic sample token, blank and control placeholders, laboratory hold, taxon-call quarantine, correction lineage, and no-detection claim", "edna-contamination-firewall", "THOS Body and GMUT Mind", "environmental-DNA contamination firewall, synthetic sample token, blank and control placeholders, laboratory hold, taxon-call quarantine, correction lineage, and detection-claim refusal", ["TDWG-DARWIN-CORE", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Earth-observation wetland scene lineage with synthetic asset token, acquisition window, cloud and tide holds, transformation chain, geometry, resolution, and no-change conclusion", "earth-observation-scene-lineage", "GMUT Mind and Freed ID", "earth-observation wetland scene lineage, synthetic asset token, acquisition window, cloud and tide holds, transformation chain, geometry, resolution, and change-conclusion refusal", ["RAMSAR-IF-WIAM", "RFC-7946", "C2PA-24", "W3C-PROV-O"]),
    ("Coordinate and geospatial uncertainty contract with axis order, datum declaration, precision budget, uncertainty radius, generalization cue, antimeridian handling, and sensitive-location hold", "geospatial-uncertainty-contract", "GMUT Mind and CBR Heart", "coordinate and geospatial uncertainty, axis order, datum declaration, precision budget, uncertainty radius, generalization cue, antimeridian handling, and sensitive-location hold", ["RFC-7946", "NIST-SP811", "NZ-PRIVACY-PRINCIPLES"]),
    ("Rainfall, tide, inflow, and outflow boundary-condition ledger with source timestamp, spatial support, gap state, unit conversion, synchronization hold, and no-attribution claim", "hydrologic-boundary-condition-ledger", "GMUT Mind", "rainfall, tide, inflow, and outflow boundary-condition ledger, source timestamp, spatial support, gap state, unit conversion, synchronization hold, and attribution-claim refusal", ["USGS-WATER-API", "NOAA-COOPS-API", "RFC-3339", "NIST-SP811"]),
    ("Nutrient and suspended-solids mass-balance worksheet with compartment, flux direction, unit basis, below-detection state, closure residual, uncertainty, and no-source attribution", "nutrient-solids-mass-balance", "GMUT Mind", "nutrient and suspended-solids mass-balance worksheet, compartment, flux direction, unit basis, below-detection state, closure residual, uncertainty, and source-attribution refusal", ["EPA-WETLAND-MONITORING", "USGS-WATER-API", "NIST-SP811"]),
    ("Dissolved-oxygen diurnal sequence with local-time and UTC pairing, sensor hold, depth, temperature context, gap intervals, hysteresis cue, and no-ecological-status claim", "dissolved-oxygen-diurnal-sequence", "GMUT Mind and THOS Body", "dissolved-oxygen diurnal sequence, local-time and UTC pairing, sensor hold, depth, temperature context, gap intervals, hysteresis cue, and ecological-status refusal", ["OGC-SENSORTHINGS-11", "RFC-3339", "NIST-SP811"]),
    ("Hydroperiod state machine with dry, inundated, uncertain, censored, and missing states, transition evidence, debounce rule, correction path, and no-restoration-success claim", "hydroperiod-state-machine", "THOS Body", "hydroperiod state machine, dry, inundated, uncertain, censored, and missing states, transition evidence, debounce rule, correction path, and restoration-success refusal", ["RAMSAR-IF-WIAM", "OGC-SENSORTHINGS-11", "W3C-PROV-O"]),
    ("Wetland restoration intervention version ledger with objective placeholder, design revision, implementation hold, deviation, monitoring link, rollback cue, and no-effectiveness conclusion", "restoration-intervention-version-ledger", "THOS Body and CBR Heart", "restoration intervention version ledger, objective placeholder, design revision, implementation hold, deviation, monitoring link, rollback cue, and effectiveness-conclusion refusal", ["RAMSAR-IF-WIAM", "EPA-WETLAND-MONITORING", "W3C-PROV-O"]),
    ("Field-instrument readiness and calibration reservation with synthetic device token, range, unit, check date, drift cue, competent-person hold, quarantine, and no-fit-for-use release", "field-instrument-readiness-reserve", "THOS Body", "field-instrument readiness and calibration reservation, synthetic device token, range, unit, check date, drift cue, competent-person hold, quarantine, and fit-for-use refusal", ["OGC-SENSORTHINGS-11", "NIST-SP811", "RFC-3339"]),
    ("Weather, access, and lone-worker field-safety reservation with forecast hold, route placeholder, communication check, stop-work cue, competent assessment, and no-field authorization", "field-safety-reservation", "THOS Body and CBR Heart", "weather, access, and lone-worker safety reservation, forecast hold, route placeholder, communication check, stop-work cue, competent assessment, and field-authorization refusal", ["NZ-PRIVACY-PRINCIPLES", "RFC-3339"]),
    ("Accessible field-note and data-table handover with headings, units, abbreviations, table associations, focus order, correction path, and manual and affected-user review reserved", "accessible-field-note-handover", "THOS Body and CBR Heart", "accessible field-note and data-table handover, headings, units, abbreviations, table associations, focus order, correction path, and manual and affected-user review reservation", ["W3C-WCAG-22", "NIST-SP811"]),
    ("Community wetland observation disagreement and correction ledger with claim token, source class, dissent, uncertainty, response window, attribution hold, and no-consensus promotion", "community-observation-correction-ledger", "CBR Heart and Freed ID", "community wetland observation disagreement and correction ledger, claim token, source class, dissent, uncertainty, response window, attribution hold, and consensus-promotion refusal", ["W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES", "LOCAL-CONTEXTS-LABELS"]),
    ("Sensitive-species and culturally restricted publication firewall with coarse-location option, audience class, authority hold, expiry, correction, audit cue, and fail-closed disclosure", "restricted-publication-firewall", "CBR Heart and Freed ID", "sensitive-species and culturally restricted publication firewall, coarse-location option, audience class, authority hold, expiry, correction, audit cue, and fail-closed disclosure", ["NZ-PRIVACY-PRINCIPLES", "TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "RFC-7946"]),
    ("Wetland stewardship benefit, access, remedy, and redress decision matrix with claimant placeholder, collective interest, non-retaliation hold, disagreement, escalation, and no-authority substitution", "stewardship-remedy-matrix", "CBR Heart", "wetland stewardship benefit, access, remedy, and redress decision matrix, claimant placeholder, collective interest, non-retaliation hold, disagreement, escalation, and authority-substitution refusal", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES"]),
    ("GMUT wetland advection-diffusion-reaction typed proxy with field domains, coefficient units, source and sink signs, boundary conditions, solver hold, and no-real-likelihood claim", "gmut-wetland-adr-proxy", "GMUT Mind", "GMUT wetland advection-diffusion-reaction typed proxy, field domains, coefficient units, source and sink signs, boundary conditions, solver hold, and real-likelihood refusal", ["NIST-SP811", "USGS-WATER-API", "RFC-8785"]),
    ("GMUT shallow-water and porous-exchange typed proxy with state variables, interface flux, sign convention, dimensional audit, closure residual, and no-force or prediction claim", "gmut-shallow-porous-proxy", "GMUT Mind", "GMUT shallow-water and porous-exchange typed proxy, state variables, interface flux, sign convention, dimensional audit, closure residual, and force-or-prediction refusal", ["NIST-SP811", "RAMSAR-IF-WIAM", "RFC-8785"]),
    ("THOS wetland sensor-loss incident choreography with heartbeat, dropout, stale-reading quarantine, alternate observation hold, escalation, rollback, and no-operational-effectiveness claim", "thos-sensor-loss-choreography", "THOS Body", "THOS wetland sensor-loss incident choreography, heartbeat, dropout, stale-reading quarantine, alternate observation hold, escalation, rollback, and operational-effectiveness refusal", ["OGC-SENSORTHINGS-11", "OGC-SENSORTHINGS-20", "RFC-3339"]),
    ("Freed ID wetland-sample disclosure capsule with synthetic identifier, purpose, collection hold, disclosure audience, retention, correction, status placeholder, and no-live-proof claim", "freed-id-sample-disclosure-capsule", "Freed ID and CBR Heart", "Freed ID wetland-sample disclosure capsule, synthetic identifier, purpose, collection hold, disclosure audience, retention, correction, status placeholder, and live-proof refusal", ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID wetland-imagery lineage plan with synthetic asset token, source scene, transformation action, assertion, binding and signer holds, redaction, and no-authenticity claim", "freed-id-imagery-lineage-plan", "Freed ID", "Freed ID wetland-imagery lineage plan, synthetic asset token, source scene, transformation action, assertion, binding and signer holds, redaction, and authenticity-claim refusal", ["C2PA-24", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("GBIF wetland occurrence no-network query tribunal with taxon and geometry filter placeholders, page-stop invariant, sensitive-coordinate suppression, publisher citation capture, and empty-result witness", "gbif-wetland-zero-row-adapter", "Freed ID and GMUT Mind", "GBIF wetland occurrence no-network query tribunal, taxon and geometry filter placeholders, page-stop invariant, sensitive-coordinate suppression, publisher citation capture, and empty-result witness", ["GBIF-OCCURRENCE-API", "TDWG-DARWIN-CORE", "NZ-PRIVACY-PRINCIPLES"]),
    ("CBR wetland whenua, waterway, species, traditional-knowledge, benefit, privacy, access, remedy, legal, cultural, data-governance, and Māori-authority reservation matrix", "cbr-wetland-authority-matrix", "CBR Heart", "wetland whenua, waterway, species, traditional-knowledge, benefit, privacy, access, remedy, legal, cultural, data-governance, and Māori-authority reservation", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES", "RAMSAR-IF-WIAM"]),
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
    ("ghc-family-wetland-site-passport-boundary", "Freeze site identity, geometry, access, and condition-claim boundaries."),
    ("ghc-family-wetland-hydrology-observation-boundary", "Separate observations, units, gaps, uncertainty, and hydrologic inference."),
    ("ghc-family-wetland-sample-custody-boundary", "Preserve synthetic sample lineage while reserving laboratory authority."),
    ("ghc-family-wetland-biodiversity-observation-boundary", "Guard taxon, effort, disagreement, sensitive-location, and abundance claims."),
    ("ghc-family-wetland-geospatial-lineage-boundary", "Track geometry, precision, generalization, remote-scene, and transformation lineage."),
    ("ghc-family-wetland-restoration-nonpromotion", "Version intervention plans without claiming implementation or effectiveness."),
    ("ghc-family-wetland-field-safety-reserve", "Reserve competent field, weather, access, instrument, and stop-work decisions."),
    ("ghc-family-wetland-accessibility-handover", "Generate accessible structural handovers while reserving manual evaluation."),
    ("ghc-family-wetland-freed-id-disclosure-reserve", "Constrain synthetic identity, disclosure, status, proof, and imagery claims."),
    ("ghc-family-wetland-cultural-authority-reserve", "Fail closed around collective interests, restricted knowledge, remedy, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_wetland_site_passport.py", "wetland-site-passport"),
    ("ghc_family_wetland_hydrology_observation.py", "hydroperiod-observation-series"),
    ("ghc_family_wetland_sample_custody.py", "sediment-peat-soil-custody"),
    ("ghc_family_wetland_biodiversity_observation.py", "vegetation-stratum-cover-board"),
    ("ghc_family_wetland_geospatial_lineage.py", "earth-observation-scene-lineage"),
    ("ghc_family_wetland_restoration_nonpromotion.py", "restoration-intervention-version-ledger"),
    ("ghc_family_wetland_field_safety_reserve.py", "field-safety-reservation"),
    ("ghc_family_wetland_accessibility_handover.py", "accessible-field-note-handover"),
    ("ghc_family_wetland_freed_id_disclosure.py", "freed-id-sample-disclosure-capsule"),
    ("ghc_family_wetland_cultural_authority_reserve.py", "cbr-wetland-authority-matrix"),
]


def negative(number: int, signature: str, observed: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6566-X1-N{number:02d}",
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
    negative(1, "nonrepository-source-worktree-probe", "The first source worktree lookup ran from the Codex home directory, exceeded its bound, and then reported that the location was not a Git repository.", "Use the exact literal D-drive source path from the activation packet.", "Resolve the source root before invoking repository-scoped Git."),
    negative(2, "current-auth-state-materialization-race", "A multi-file read initially reported the current auth-state reference missing; a later exact read found and validated the current state.", "Validate the current state directly and retain the transient absence at zero credit.", "Treat mutable current-state references as drift-prone and verify them immediately before use."),
    negative(3, "powershell-foreach-pipeline-parser-fault", "PowerShell rejected a direct foreach block piped into JSON serialization.", "Materialize foreach results into a scalar array before piping.", "Never pipe directly from a PowerShell foreach statement in this host."),
    negative(4, "combined-skill-count-timeout", "A combined line and word count across seventeen required skill files exceeded its bounded window.", "Read required skill files completely in small exact batches.", "Do not aggregate many large skill reads into one cold command."),
    negative(5, "activation-baton-chunk-timeout", "A sixty-line activation-packet display exceeded its bounded output window.", "Use System.IO.File.ReadAllLines with smaller scalar slices while preserving complete EOF coverage.", "Keep large packet display chunks small even when the underlying read is local."),
    negative(6, "powershell-native-command-grouping-parser-fault", "PowerShell rejected an attempted parenthesized native Git command and exit-code projection.", "Run the native command first, then capture LASTEXITCODE in a separate statement.", "Do not group native commands and shell statements inside an expression."),
    negative(7, "worktree-add-wrapper-timeout-after-materialization", "The worktree-add wrapper timed out while checkout continued and ultimately completed successfully.", "Inspect the exact process, lock, path marker, head, branch, and clean state before any retry.", "A wrapper timeout never proves a Git mutation failed or stopped."),
    negative(8, "identity-search-windows-quoting-fault", "The first identity collision search used ambiguous quoting and split Windows paths into invalid arguments.", "Use separate literal patterns and an explicit repository root.", "Keep Windows searches to simple separately quoted patterns."),
    negative(9, "combined-x1-inventory-timeout", "A combined status, branch, head, and catalogue-symbol inventory exceeded its bounded window without a trustworthy aggregate result.", "Split cleanliness, revision, and exact-file searches into separate bounded probes.", "Do not combine large-worktree status enumeration with unrelated source inspection."),
    negative(10, "working-tree-versus-committed-baton-hash-mismatch", "The first x1 build hashed CRLF-normalized working-tree baton bytes against a SHA-256 value that binds the LF committed Git blob and stopped before artifact generation.", "Read the baton blob at the exact Eiren final commit and hash those immutable bytes.", "Match every declared digest to its representation domain before comparison."),
    negative(11, "stale-source-anchor-object-name", "The second x1 preflight used stale or mistyped full names for Eiren's x1 and evidence anchors and Git rejected the nonexistent x1 object before artifact generation.", "Derive the exact anchors from the verified final's actual single-parent log and committed receipts.", "Copy immutable object names from live Git output rather than expanding abbreviated startup notes."),
    negative(12, "inherited-frozen-index-identifier-uniqueness-assumption", "The third x1 preflight found 2,320 inherited rows but rejected twenty repeated historical identifier groups even though all 2,320 titles were unique.", "Preserve every inherited row, report identifier collisions, and bind novelty to row content and title rather than assuming globally unique historical identifiers.", "Inspect frozen-index identifier and title cardinalities separately before choosing a uniqueness invariant."),
    negative(13, "public-data-adapter-semantic-novelty-failure", "The first complete novelty screen found the original proposal 29 title too similar to Eiren's coffee public-data adapter template at 0.6129 and stopped before artifact generation.", "Redesign the surface around a no-network occurrence-query tribunal with geometry and taxon filters, page-stop invariants, sensitive-coordinate suppression, publisher citation capture, and an empty-result witness.", "Domain substitution alone is not a novel reusable-framework proposal."),
    negative(14, "repository-builder-private-receipt-path", "The first artifact privacy scan found one private absolute D-drive receipt path embedded in the x1 builder and blocked the packet.", "Remove the local bank path from repository source and record only the sanitized receipt digest and completed pre-mutation verification.", "Durable tools may bind receipt digests but must not publish private local bank paths."),
    negative(15, "guessed-repository-auth-runner-name", "A post-build runner discovery attempted a nonexistent repository script named ghc_family_auth_permission_state.py after the x1 tests had passed.", "Use the validator path declared by the installed auth-permission-state skill.", "Inspect a selected skill's declared script names instead of deriving a repository filename."),
    negative(16, "guessed-skill-local-roster-validator-name", "A follow-up discovery attempted a nonexistent skill-local validate_roster.py path even though the repository roster runner already existed.", "Use the verified repository ghc_family_roster_check.py runner and the already successful startup validation.", "Do not force symmetry between independently packaged skill and repository runner layouts."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6566-SAFE-{index:03d}",
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
        "task_id": f"V6566-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]

CLEAN_TASKS = [
    {
        "task_id": f"V6566-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, and stale-label cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
