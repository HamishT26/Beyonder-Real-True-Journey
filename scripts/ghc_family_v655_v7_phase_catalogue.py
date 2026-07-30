#!/usr/bin/env python3
"""Orin Thale v655-v7 source, proposal, portfolio, and startup catalogue."""

from __future__ import annotations


OFFICIAL_SOURCES = [
    {
        "source_id": "NZ-MBIE-GEOTECH-M2",
        "title": "Module 2: Geotechnical investigations for earthquake engineering",
        "publisher": "New Zealand Ministry of Business, Innovation and Employment",
        "url": (
            "https://www.building.govt.nz/building-code-compliance/b-stability/"
            "b1-structure/module-2-geotechnical-investigations"
        ),
        "status": "current",
        "use": (
            "investigation planning, ground-condition uncertainty, borehole, test, "
            "professional-review, and NZGD context only; no site investigation, "
            "engineering interpretation, design, consent, or safety claim"
        ),
    },
    {
        "source_id": "NZ-MBIE-GEOTECH-PA17",
        "title": "Practice Advisory 17: Well-planned ground investigations can save costs",
        "publisher": "New Zealand Ministry of Business, Innovation and Employment",
        "url": (
            "https://www.building.govt.nz/building-code-compliance/b-stability/"
            "b1-structure/practice-advisory-17"
        ),
        "status": "current",
        "use": (
            "site-investigation purpose, uncertainty, iteration, and qualified-"
            "professional reservation only"
        ),
    },
    {
        "source_id": "NZ-GNS-NZGD",
        "title": "New Zealand Geotechnical Database",
        "publisher": "Earth Sciences New Zealand / GNS Science",
        "url": (
            "https://www.gns.cri.nz/data-and-resources/"
            "new-zealand-geotechnical-database/"
        ),
        "status": "watch",
        "use": (
            "official database identity, terms, provenance, access, and zero-row "
            "adapter requirements only; no query, download, interpretation, or "
            "completeness claim"
        ),
    },
    {
        "source_id": "AGS-FORMAT-411",
        "title": "AGS Format Version 4.1.1",
        "publisher": "Association of Geotechnical and Geoenvironmental Specialists",
        "url": (
            "https://www.ags.org.uk/content/uploads/2022/02/"
            "AGS4-v-4.1.1-2022.pdf"
        ),
        "status": "stable",
        "use": (
            "synthetic data-group, heading, unit, type, key, and resource-budget "
            "parser vocabulary; no registration, field-data, or conformance claim"
        ),
    },
    {
        "source_id": "USGS-LANDSLIDE-MONITOR",
        "title": "Real-Time Monitoring for Potential Landslides",
        "publisher": "U.S. Geological Survey",
        "url": (
            "https://www.usgs.gov/programs/landslide-hazards/science/"
            "real-time-monitoring-potential-landslides"
        ),
        "status": "current",
        "use": (
            "piezometer and inclinometer monitoring vocabulary only; no instrument "
            "installation, measurement, alert, hazard, or safety inference"
        ),
    },
    {
        "source_id": "USGS-LANDSLIDE-DATA",
        "title": "Data from in-situ landslide monitoring, Trinity County, California",
        "publisher": "U.S. Geological Survey",
        "url": (
            "https://www.usgs.gov/data/"
            "data-situ-landslide-monitoring-trinity-county-california"
        ),
        "status": "stable",
        "use": (
            "primary-source examples of instrument metadata, depth, accuracy, "
            "temperature compensation, and provenance; zero rows are ingested"
        ),
    },
    {
        "source_id": "OGC-SENSORTHINGS-11",
        "title": "OGC SensorThings API Part 1: Sensing Version 1.1",
        "publisher": "Open Geospatial Consortium",
        "url": "https://docs.ogc.org/is/18-088/18-088.html",
        "status": "stable",
        "use": (
            "synthetic Thing, Sensor, ObservedProperty, Datastream, Observation, "
            "location, unit, and version vocabulary; no live service or observation"
        ),
    },
    {
        "source_id": "W3C-PROV-O",
        "title": "PROV-O: The PROV Ontology",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "stable",
        "use": (
            "entity, activity, agent, revision, derivation, custody, correction, "
            "handover, and source lineage vocabulary"
        ),
    },
    {
        "source_id": "RFC-3339",
        "title": "RFC 3339: Date and Time on the Internet: Timestamps",
        "publisher": "RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc3339.html",
        "status": "stable",
        "use": "synthetic UTC lexical timestamp and correction discipline",
    },
    {
        "source_id": "RFC-8785",
        "title": "RFC 8785: JSON Canonicalization Scheme",
        "publisher": "RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "stable",
        "use": "deterministic synthetic event and manifest serialization vocabulary",
    },
    {
        "source_id": "NIST-SP811",
        "title": "NIST SP 811: Guide for the Use of the International System of Units",
        "publisher": "National Institute of Standards and Technology",
        "url": "https://www.nist.gov/publications/guide-use-international-system-units-si",
        "status": "current",
        "use": (
            "unit and conversion discipline; not calibration, field measurement, "
            "laboratory competence, or engineering authority"
        ),
    },
    {
        "source_id": "BIOT-1941",
        "title": "General Theory of Three-Dimensional Consolidation",
        "publisher": "Journal of Applied Physics / AIP Publishing",
        "url": "https://doi.org/10.1063/1.1712886",
        "status": "stable",
        "use": (
            "primary provenance for the typed poroelastic consolidation obligation "
            "board; no parameter, solution, site prediction, or physical confirmation"
        ),
    },
    {
        "source_id": "USACE-SLOPE-1902",
        "title": "EM 1110-2-1902: Slope Stability",
        "publisher": "U.S. Army Corps of Engineers",
        "url": (
            "https://www.publications.usace.army.mil/Portals/76/Publications/"
            "EngineerManuals/EM_1110-2-1902.pdf"
        ),
        "status": "stable",
        "use": (
            "slope-analysis domain, assumptions, mechanism, factor-of-safety, and "
            "professional-review reservation; no site assessment or design"
        ),
    },
    {
        "source_id": "W3C-WCAG-22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "stable",
        "use": (
            "accessible static-report structure with manual, browser, assistive-"
            "technology, Māori-language, and affected-user evaluation reserved"
        ),
    },
    {
        "source_id": "NZ-PRIVACY-ACT-2020",
        "title": "Privacy Act 2020",
        "publisher": "New Zealand Legislation",
        "url": "https://www.legislation.govt.nz/act/public/2020/31/en/latest/",
        "status": "watch",
        "use": (
            "purpose, minimization, access, correction, retention, identifier, "
            "location, and disclosure reservations without legal interpretation"
        ),
    },
    {
        "source_id": "NZ-HSWA-2015",
        "title": "Health and Safety at Work Act 2015",
        "publisher": "New Zealand Legislation",
        "url": "https://www.legislation.govt.nz/act/public/2015/70/en/latest/",
        "status": "watch",
        "use": (
            "workplace duty, unsafe-work, training, fieldwork, and competent-person "
            "reservation without legal interpretation"
        ),
    },
    {
        "source_id": "NZ-HERITAGE-ACT-2014",
        "title": "Heritage New Zealand Pouhere Taonga Act 2014",
        "publisher": "New Zealand Legislation",
        "url": "https://www.legislation.govt.nz/act/public/2014/0026/latest/",
        "status": "watch",
        "use": (
            "archaeological-site, taonga, discovery, permission, and authority "
            "reservation only; no legal or cultural interpretation"
        ),
    },
    {
        "source_id": "W3C-VC-DM-20",
        "title": "Verifiable Credentials Data Model v2.0",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "stable",
        "use": (
            "synthetic calibration-status and site-role credential vocabulary; "
            "no real issuer, holder, verifier, key, proof, status, or trust claim"
        ),
    },
    {
        "source_id": "W3C-DID-10",
        "title": "Decentralized Identifiers (DIDs) v1.0",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/did-core/",
        "status": "stable",
        "use": (
            "synthetic identifier and controller vocabulary only; no live method, "
            "resolver, key, proof, or trust-governance claim"
        ),
    },
    {
        "source_id": "W3C-VC-DI-10",
        "title": "Verifiable Credential Data Integrity 1.0",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/vc-data-integrity/",
        "status": "stable",
        "use": (
            "synthetic proof-envelope and cryptosuite-gap vocabulary; no generated "
            "key, signature, proof, verification, security, or interoperability claim"
        ),
    },
    {
        "source_id": "TMR-PRINCIPLES",
        "title": "Principles of Māori Data Sovereignty",
        "publisher": "Te Mana Raraunga",
        "url": (
            "https://www.temanararaunga.maori.nz/"
            "principles-of-maori-data-sovereignty"
        ),
        "status": "current",
        "use": (
            "Māori rights, interests, land and location data, governance, "
            "jurisdiction, collective benefit, and authority reservation only"
        ),
    },
]


# number, title, slug, pillar, expected disposition, semantic mechanism, source ids
PROPOSAL_ROWS = [
    (
        1,
        "Synthetic borehole passport with site-token separation, collar datum, "
        "drilling-method placeholder, depth extent, revision lineage, collision "
        "quarantine, and no-fieldwork claim",
        "borehole-passport",
        "Freed ID and THOS Body",
        "completed",
        "borehole referent, site-token separation, datum, method, revision, collision, and fieldwork refusal",
        ["NZ-MBIE-GEOTECH-M2", "W3C-PROV-O", "NZ-PRIVACY-ACT-2020"],
    ),
    (
        2,
        "Geotechnical sample-custody envelope with interval, sample class, split, "
        "seal placeholder, container, transfer, hold, correction, and no-specimen claim",
        "sample-custody-envelope",
        "Freed ID and CBR Heart",
        "completed",
        "sample interval, class, split, seal gap, custody transfer, hold, and specimen refusal",
        ["NZ-MBIE-GEOTECH-M2", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        3,
        "Lithology interval ledger with controlled term, top and base depth, "
        "boundary uncertainty, interbed relation, supersession, and no-ground-model claim",
        "lithology-interval-ledger",
        "GMUT Mind and THOS Body",
        "completed",
        "lithology term, interval boundary, uncertainty, interbed, supersession, and ground-model refusal",
        ["NZ-MBIE-GEOTECH-M2", "AGS-FORMAT-411", "NIST-SP811"],
    ),
    (
        4,
        "SPT and CPT measurement proxy with test-method source, instrument "
        "placeholder, calibration gap, correction factor, refusal state, and no-real-test rule",
        "penetration-test-proxy",
        "THOS Body and GMUT Mind",
        "represented",
        "penetration-test method, instrument, calibration, correction, uncertainty, and real-test proxy",
        ["NZ-MBIE-GEOTECH-M2", "NIST-SP811", "W3C-PROV-O"],
    ),
    (
        5,
        "Piezometer observation envelope with instrument token, datum, screened "
        "interval, calibration gap, temperature field, unit, uncertainty, and no-measurement claim",
        "piezometer-observation-envelope",
        "GMUT Mind and THOS Body",
        "completed",
        "piezometer referent, datum, screened interval, calibration, temperature, unit, and measurement refusal",
        ["USGS-LANDSLIDE-MONITOR", "USGS-LANDSLIDE-DATA", "OGC-SENSORTHINGS-11"],
    ),
    (
        6,
        "Inclinometer survey proxy with casing token, axis orientation, depth "
        "sequence, baseline placeholder, zero drift, repeat cue, and no-displacement claim",
        "inclinometer-survey-proxy",
        "GMUT Mind and THOS Body",
        "completed",
        "inclinometer casing, orientation, depth, baseline, drift, repeat, and displacement refusal",
        ["USGS-LANDSLIDE-MONITOR", "USGS-LANDSLIDE-DATA", "NIST-SP811"],
    ),
    (
        7,
        "Slope-hazard observation docket with crack, seepage, bulge, rockfall, "
        "weather, location-minimum, uncertainty, escalation hold, and no-safety determination",
        "slope-hazard-observation",
        "CBR Heart and THOS Body",
        "completed",
        "slope observation, weather, location minimization, uncertainty, escalation, and safety-decision refusal",
        ["NZ-MBIE-GEOTECH-PA17", "USGS-LANDSLIDE-MONITOR", "USACE-SLOPE-1902"],
    ),
    (
        8,
        "Geotechnical instrument-installation configuration proxy with borehole "
        "relation, depth, grout and seal placeholders, orientation, acceptance gap, and no-installation rule",
        "instrument-installation-proxy",
        "THOS Body",
        "completed",
        "instrument installation configuration, borehole relation, depth, seal, orientation, and physical-action refusal",
        ["USGS-LANDSLIDE-DATA", "OGC-SENSORTHINGS-11", "W3C-PROV-O"],
    ),
    (
        9,
        "Laboratory-test request and result envelope with method placeholder, "
        "sample link, condition, unit, uncertainty, review gap, correction, and no-laboratory claim",
        "laboratory-result-envelope",
        "THOS Body and GMUT Mind",
        "completed",
        "laboratory request, sample link, method, condition, unit, uncertainty, review, and laboratory refusal",
        ["NZ-MBIE-GEOTECH-M2", "AGS-FORMAT-411", "NIST-SP811"],
    ),
    (
        10,
        "Geotechnical depth, unit, overlap, duplicate, and impossible-order tribunal "
        "with deterministic quarantine and no-interpretation promotion",
        "geotechnical-quality-tribunal",
        "GMUT Mind and THOS Body",
        "completed",
        "depth, unit, overlap, duplicate, ordering, quarantine, and interpretation refusal",
        ["AGS-FORMAT-411", "NIST-SP811", "RFC-8785"],
    ),
    (
        11,
        "Deferred field-observation queue ledger with unresolved depth interval, "
        "sealed-sample hold, sensor anomaly, rest threshold, sender-receiver "
        "checksum, and fail-closed ownership transfer",
        "field-log-handover-governor",
        "THOS Body and CBR Heart",
        "completed",
        "field-log workload, unresolved interval, sample hold, alert, break, readback, and release refusal",
        ["NZ-HSWA-2015", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        12,
        "Near-miss evidence-preservation docket for borehole-collapse cue, utility-"
        "strike cue, contamination-exposure cue, immediate pause, record correction, "
        "review queue, and remedy reservation",
        "geotechnical-incident-remedy",
        "CBR Heart",
        "completed",
        "incident, near miss, complaint, correction, hold, remedy, and adjudication refusal",
        ["NZ-HSWA-2015", "NZ-PRIVACY-ACT-2020", "TMR-PRINCIPLES"],
    ),
    (
        13,
        "Accessible borehole-log and monitoring-report audit with heading order, "
        "table association, noncolour state, keyboard order, print fallback, and manual-review reserve",
        "accessible-geotechnical-report",
        "CBR Heart",
        "completed",
        "report heading, table association, noncolour state, keyboard order, fallback, and manual-review reserve",
        ["W3C-WCAG-22", "NZ-MBIE-GEOTECH-M2"],
    ),
    (
        14,
        "Geotechnical location and personal-data envelope with purpose, coordinate "
        "precision ceiling, land-link separation, retention, correction, disclosure, and privacy-complete refusal",
        "geotechnical-privacy-envelope",
        "Freed ID and CBR Heart",
        "completed",
        "purpose, coordinate minimization, land separation, retention, correction, disclosure, and privacy refusal",
        ["NZ-PRIVACY-ACT-2020", "TMR-PRINCIPLES", "W3C-PROV-O"],
    ),
    (
        15,
        "Weather, ground-condition, access, plant, utility, and stop-work hold board "
        "with competent-review gap and no-site-entry authorization",
        "site-access-hold-board",
        "THOS Body and CBR Heart",
        "completed",
        "weather, ground, access, plant, utility, stop-work, competent review, and entry refusal",
        ["NZ-HSWA-2015", "NZ-MBIE-GEOTECH-PA17", "W3C-PROV-O"],
    ),
    (
        16,
        "Utility, contamination, unexpected-ground, archaeological-discovery, "
        "taonga, notification, preservation hold, and no-authority decision board",
        "unexpected-discovery-hold",
        "CBR Heart",
        "completed",
        "utility, contamination, unexpected ground, archaeology, taonga, notification, hold, and authority refusal",
        ["NZ-HERITAGE-ACT-2014", "NZ-HSWA-2015", "TMR-PRINCIPLES"],
    ),
    (
        17,
        "Sample-disposition state machine with custody owner, retained amount, "
        "return placeholder, hold, proposed destruction, approval gap, and no-disposal action",
        "sample-disposition-state",
        "Freed ID and CBR Heart",
        "completed",
        "sample custody, retained amount, return, hold, destruction proposal, approval gap, and disposal refusal",
        ["W3C-PROV-O", "NZ-PRIVACY-ACT-2020", "TMR-PRINCIPLES"],
    ),
    (
        18,
        "Deterministic geotechnical interval normalization tribunal with depth "
        "precision, open-closed boundary, sort key, overlap class, digest, and source-preserving refusal",
        "interval-normalization-tribunal",
        "GMUT Mind",
        "completed",
        "interval precision, boundary convention, sorting, overlap, digest, source preservation, and refusal",
        ["AGS-FORMAT-411", "RFC-8785", "NIST-SP811"],
    ),
    (
        19,
        "Bounded AGS data-group parser tribunal with heading, unit, type, keyset, "
        "duplicate, encoding, line-length, group-count, and resource-budget refusal",
        "ags-parser-tribunal",
        "THOS Body",
        "completed",
        "AGS group, heading, unit, type, keyset, duplicate, encoding, and resource-budget parser",
        ["AGS-FORMAT-411", "RFC-8785"],
    ),
    (
        20,
        "Geotechnical model-lineage DAG with factual, derived, interpreted, design, "
        "source, revision, foreign edge, orphan, duplicate-credit, and nonpromotion quarantine",
        "geotechnical-model-lineage",
        "GMUT Mind and Freed ID",
        "completed",
        "factual, derived, interpreted, design, source, revision, edge, orphan, credit, and nonpromotion lineage",
        ["W3C-PROV-O", "NZ-MBIE-GEOTECH-PA17", "RFC-8785"],
    ),
    (
        21,
        "GMUT typed Biot poroelasticity board with displacement, strain, stress, "
        "pore pressure, fluid content, coupling, boundary, unit, domain, and observation firewall",
        "gmut-biot-poroelasticity",
        "GMUT Mind",
        "completed",
        "typed Biot poroelastic state, coupling, constitutive assumptions, boundary, units, domain, and observation firewall",
        ["BIOT-1941", "NIST-SP811"],
    ),
    (
        22,
        "GMUT typed effective-stress and Mohr-Coulomb obligation board with total "
        "stress, pore pressure, cohesion, friction angle, sign, unit, domain, and prediction firewall",
        "gmut-effective-stress-board",
        "GMUT Mind",
        "completed",
        "typed effective stress, pore pressure, strength parameters, sign, units, domain, and prediction firewall",
        ["NZ-MBIE-GEOTECH-M2", "USACE-SLOPE-1902", "NIST-SP811"],
    ),
    (
        23,
        "GMUT consolidation diffusion obligation board with drainage path, time, "
        "coefficient, boundary and initial conditions, unit, singularity, and site-settlement firewall",
        "gmut-consolidation-diffusion",
        "GMUT Mind",
        "completed",
        "typed consolidation diffusion, drainage, time, coefficient, boundary, initial state, units, and settlement refusal",
        ["BIOT-1941", "NIST-SP811"],
    ),
    (
        24,
        "GMUT slope factor-of-safety domain board with mechanism, strength model, "
        "pore-pressure case, load case, geometry gap, uncertainty, and no-site-stability prediction",
        "gmut-slope-domain-board",
        "GMUT Mind",
        "completed",
        "slope mechanism, strength model, pore pressure, load, geometry, uncertainty, and stability-prediction refusal",
        ["USACE-SLOPE-1902", "NZ-MBIE-GEOTECH-PA17", "NIST-SP811"],
    ),
    (
        25,
        "THOS geotechnical monitoring alarm-triage proxy with instrument token, "
        "threshold source, persistence, confidence, acknowledgement, escalation, handover, and no-hazard decision",
        "thos-monitoring-triage",
        "THOS Body",
        "represented",
        "synthetic monitoring alert, threshold source, persistence, confidence, acknowledgement, handover, and hazard proxy",
        ["OGC-SENSORTHINGS-11", "USGS-LANDSLIDE-MONITOR", "NZ-HSWA-2015"],
    ),
    (
        26,
        "THOS blind matched-budget geotechnical logging protocol with arm isolation, "
        "task budget, correction endpoint, workload and harm monitoring, preregistration, and zero-participant rule",
        "thos-geotechnical-study-protocol",
        "THOS Body",
        "represented",
        "blind matched-budget logging protocol, arm isolation, task budget, endpoints, workload, harm, and participant refusal",
        ["NZ-MBIE-GEOTECH-M2", "NZ-HSWA-2015", "W3C-PROV-O"],
    ),
    (
        27,
        "Freed ID synthetic sensor-metrology evidence bundle with instrument "
        "referent, calibration-artifact digest, method source, uncertainty class, "
        "validity interval, evidence-issuer placeholder, and cryptographic refusal",
        "freed-id-calibration-credential",
        "Freed ID",
        "represented",
        "synthetic metrology evidence, instrument referent, calibration digest, method source, uncertainty, validity, issuer, and cryptographic gaps",
        ["W3C-VC-DM-20", "W3C-DID-10", "W3C-VC-DI-10"],
    ),
    (
        28,
        "Freed ID purpose-scoped field-zone authorization graph with pseudonymous "
        "actor, coarse zone, time window, task capability, delegation chain, "
        "correlation budget, and absent revocation state",
        "freed-id-site-access-profile",
        "Freed ID and CBR Heart",
        "represented",
        "synthetic field-zone capability, pseudonymous actor, purpose, coarse location, delegation, correlation, revocation, and nonproduction proxy",
        ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-ACT-2020"],
    ),
    (
        29,
        "New Zealand Geotechnical Database provenance, terms, schema, uncertainty, "
        "selection, coordinate-privacy, checksum, and zero-row empirical adapter",
        "nzgd-zero-row-adapter",
        "GMUT Mind",
        "open_gap",
        "NZGD source, terms, schema, uncertainty, selection, coordinate privacy, checksum, and zero-row refusal",
        ["NZ-GNS-NZGD", "NZ-MBIE-GEOTECH-M2", "NZ-PRIVACY-ACT-2020"],
    ),
    (
        30,
        "CBR geotechnical land access, hazard notice, disability, privacy, sample "
        "custody, heritage, taonga, remedy, legal, cultural, data-governance, affected-party, and Māori-authority matrix",
        "cbr-geotechnical-authority-matrix",
        "Freed ID and CBR Heart",
        "exact_gate",
        "land access, hazard notice, disability, privacy, custody, heritage, taonga, remedy, legal, cultural, governance, and authority reservation",
        [
            "NZ-PRIVACY-ACT-2020",
            "NZ-HERITAGE-ACT-2014",
            "W3C-WCAG-22",
            "TMR-PRINCIPLES",
        ],
    ),
]


SKILL_IDEAS = [
    "ghc-family-geotechnical-borehole-boundary",
    "ghc-family-geotechnical-sample-custody",
    "ghc-family-geotechnical-instrument-proxy",
    "ghc-family-geotechnical-interval-quality",
    "ghc-family-geotechnical-hazard-handover",
    "ghc-family-geotechnical-accessibility-privacy",
    "ghc-family-geotechnical-land-remedy-reserve",
    "ghc-family-gmut-geomechanics-firewall",
    "ghc-family-thos-freed-geotechnical-profile",
    "ghc-family-geotechnical-evidence-nonpromotion",
]


RUNNER_IDEAS = [
    "ghc_family_geotechnical_borehole_boundary.py",
    "ghc_family_geotechnical_sample_custody.py",
    "ghc_family_geotechnical_instrument_proxy.py",
    "ghc_family_geotechnical_interval_quality.py",
    "ghc_family_geotechnical_hazard_handover.py",
    "ghc_family_geotechnical_accessibility_privacy.py",
    "ghc_family_geotechnical_land_remedy_reserve.py",
    "ghc_family_gmut_geomechanics_firewall.py",
    "ghc_family_thos_freed_geotechnical_profile.py",
    "ghc_family_v655_v7_suite.py",
]


CLEAN_SURFACES = [
    "borehole, site-token, datum, method, depth, interval, and revision vocabulary",
    "sample, split, seal, custody, laboratory, disposition, and correction separation",
    "piezometer, inclinometer, calibration, datum, orientation, unit, and measurement refusal",
    "weather, access, utility, contamination, heritage, taonga, and stop-work holds",
    "field-log workload, unresolved item, readback, pause, and handover states",
    "location, person, land, sample, retention, disclosure, complaint, and remedy privacy",
    "GMUT poroelasticity, effective-stress, consolidation, and slope-domain firewalls",
    "manifest coverage, Git-blob identity, deterministic JSON, and timestamp typing",
    "failure retention, Method Flow recurrence, rollback, and nonpromotion guards",
    "professional, land, affected-party, legal, cultural, and Māori-authority refusal",
]


def _negative(
    number: int,
    signature: str,
    failed: str,
    recovery: str,
    recurrence_guard: str,
) -> dict:
    return {
        "negative_id": f"V6557-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": recurrence_guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "broad_git_worktree_listing_timed_out",
        "The first broad worktree listing exceeded its bounded wrapper and returned no complete lane inventory.",
        "Use exact administrative worktree metadata and literal target-path probes.",
        "Avoid broad worktree enumeration when the exact owner path and branch are supplied.",
    ),
    _negative(
        2,
        "combined_source_status_probe_timed_out",
        "The first source status probe timed out before yielding cleanliness credit.",
        "Split tracked diff-index and untracked ls-files checks into scalar read-only probes.",
        "Keep tracked and untracked source cleanliness checks separate.",
    ),
    _negative(
        3,
        "broad_source_history_probe_timed_out",
        "The first broad source log request timed out without complete lineage output.",
        "Use rev-list count, merge count, ancestry predicates, and direct-parent probes.",
        "Prefer scalar ancestry checks over formatted broad history in archive-backed lanes.",
    ),
    _negative(
        4,
        "whole_activation_display_truncated",
        "The first whole-file activation display was truncated before proving EOF.",
        "Read bounded numbered chunks and prove the exact terminal line count.",
        "Use bounded numbered reads for long committed batons.",
    ),
    _negative(
        5,
        "powershell_foreach_output_piped_without_materialization",
        "A compound PowerShell foreach result was piped directly and failed with an empty-pipe parser error.",
        "Materialize loop output into an array before formatting or serialization.",
        "Never attach a pipeline directly to a compound foreach statement.",
    ),
    _negative(
        6,
        "method_flow_schema_filename_assumed_incorrectly",
        "The first Method Flow schema read guessed a nonexistent filename.",
        "Read the skill's exact required reference path and use references/schema.md.",
        "Never infer a skill schema filename when SKILL.md names it exactly.",
    ),
    _negative(
        7,
        "reflection_schema_filename_assumed_incorrectly",
        "The first Reflection Remaster schema read guessed a nonexistent filename.",
        "Read the skill's exact required reference path and use references/decision-schema.md.",
        "Resolve every skill reference from its complete SKILL.md.",
    ),
    _negative(
        8,
        "second_source_status_bundle_timed_out",
        "A second compact source status bundle also exceeded its wrapper.",
        "Use exact diff-index and untracked-path probes, each with attributable output.",
        "Do not recombine source cleanliness probes after a timeout.",
    ),
    _negative(
        9,
        "owned_worktree_restore_wrapper_timed_out_while_git_continued",
        "The initial owned checkout restore exceeded its wrapper while the original Git process continued consuming CPU.",
        "Do not retry; monitor the exact process and accept it only after exact head, branch, clean tracked state, and untracked reconciliation pass.",
        "After an ambiguous checkout timeout, reconcile process and Git state before any mutation retry.",
    ),
    _negative(
        10,
        "frozen_chain_schema_shape_assumed_incorrectly",
        "The first frozen-chain probe assumed a proposals array that the exact source schema does not contain.",
        "Inspect exact top-level keys and combine prior_proposals with new_proposals.",
        "Inspect inherited JSON shape before constructing semantic audits.",
    ),
    _negative(
        11,
        "recursive_owned_file_count_timed_out_during_active_checkout",
        "A recursive file count exceeded its wrapper while the original checkout was still materializing 57,332 inherited paths.",
        "Use immutable Git tree counts for the inherited baseline and count only Orin-owned additions after checkout.",
        "Never apply the 2,000 owner-file rotation guard to the inherited tree baseline.",
    ),
    _negative(
        12,
        "combined_post_checkout_reconciliation_timed_out",
        "The first combined exact-head, branch, tracked, and untracked reconciliation exceeded its wrapper before yielding attributable results.",
        "Split exact head and branch, tracked diff-index, and untracked ls-files into scalar probes; all corrected probes passed.",
        "Keep post-checkout identity and cleanliness checks separately attributable on large inherited trees.",
    ),
    _negative(
        13,
        "x1_build_receipt_inherited_stale_successor_route_label",
        "The first uncommitted x1 build receipt retained Caelen's prepared-successor label even though Orin's live activation authorizes no downstream edge.",
        "Bind the compact build receipt to the same HELD_NO_DOWNSTREAM_AUTHORITY value as x1 phase truth and rebuild before freeze.",
        "Derive every lifecycle route label from the current exact live authority state.",
    ),
    _negative(
        14,
        "powershell_raw_and_delimiter_word_probe_conflict",
        "The first combined JSON and word-count receipt passed incompatible Raw and Delimiter parameters to Get-Content, so the aggregate emitted no valid word-count result.",
        "Use literal .NET UTF-8 ReadAllText calls for word counting while preserving the successful JSON parse loop.",
        "Do not combine mutually exclusive PowerShell Get-Content parameter sets.",
    ),
]
