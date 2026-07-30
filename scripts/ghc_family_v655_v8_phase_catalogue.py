#!/usr/bin/env python3
"""Liora Venn v655-v8 source, proposal, portfolio, and startup catalogue."""

from __future__ import annotations


def _source(
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
        "use": use,
    }


OFFICIAL_SOURCES = [
    _source(
        "ESTA-E1-11-2024",
        "ANSI E1.11 – 2024: USITT DMX512-A",
        "Entertainment Services and Technology Association",
        "https://tsp.esta.org/tsp/documents/docs/ANSI%20E1.11%20-%202024.pdf",
        "current",
        (
            "DMX512-A packet, slot, start-code, timing, connector, topology, and "
            "interoperability vocabulary only; no live controller, luminaire, "
            "network, product-conformance, or operational claim"
        ),
    ),
    _source(
        "ESTA-E1-20-2025",
        "ANSI E1.20 – 2025: Remote Device Management over DMX512 Networks",
        "Entertainment Services and Technology Association",
        "https://tsp.esta.org/tsp/documents/published_docs.php",
        "current",
        (
            "RDM discovery, unique-device, starting-address, status, fault, and "
            "configuration vocabulary only; no packet transmission or device change"
        ),
    ),
    _source(
        "ESTA-E1-37-5-2024",
        "ANSI E1.37-5 – 2024: General Purpose Messages for E1.20 RDM",
        "Entertainment Services and Technology Association",
        "https://tsp.esta.org/tsp/documents/published_docs.php",
        "current",
        (
            "general RDM parameter and metadata vocabulary only; no implementation, "
            "firmware, configuration, or interoperability claim"
        ),
    ),
    _source(
        "ESTA-E1-32-2022",
        "ANSI E1.32 – 2022: Guide for the Inspection of Entertainment Industry Incandescent Lamp Luminaires",
        "Entertainment Services and Technology Association",
        "https://tsp.esta.org/tsp/documents/published_docs.php",
        "current",
        (
            "inspection-program and defect-taxonomy context only; no physical "
            "inspection, electrical determination, or competent-person substitution"
        ),
    ),
    _source(
        "NZ-WORKSAFE-EVENT-RISK",
        "Managing risks at events",
        "WorkSafe New Zealand",
        "https://www.worksafe.govt.nz/topic-and-industry/event-management/managing-risks-at-events/",
        "current",
        (
            "event-risk, lighting, equipment, strobe, access, emergency, and worker "
            "consultation reservations only; no event plan or safety determination"
        ),
    ),
    _source(
        "NZ-WORKSAFE-LV",
        "Low and extra low voltage electrical installations",
        "WorkSafe New Zealand",
        "https://www.worksafe.govt.nz/topic-and-industry/electricity/installations-and-networks/low-voltage-electrical-installations/",
        "current",
        (
            "licensed-work, certification, testing, connection, and electrical-safety "
            "gates only; no design, prescribed electrical work, or connection action"
        ),
    ),
    _source(
        "NZ-ELECTRICITY-SAFETY-2010",
        "Electricity (Safety) Regulations 2010",
        "New Zealand Legislation",
        "https://www.legislation.govt.nz/regulation/public/2010/0036/latest/",
        "watch",
        (
            "current legal and competent-worker reservation only; no legal "
            "interpretation, compliance decision, certification, or authorization"
        ),
    ),
    _source(
        "NZ-MBIE-F6-AS1",
        "F6/AS1: Visibility in escape routes",
        "New Zealand Ministry of Business, Innovation and Employment",
        "https://www.building.govt.nz/building-code-compliance/f-safety-of-users/f6-visibility-in-escape-routes/acceptable-solutions-and-verification-methods",
        "current",
        (
            "emergency-lighting separation, visibility, illuminance, documentation, "
            "and testing gates only; no building-code, escape-route, or design decision"
        ),
    ),
    _source(
        "CIE-015-2018",
        "CIE 015:2018 Colorimetry, 4th Edition",
        "International Commission on Illumination",
        "https://www.cie.co.at/publications/colorimetry-4th-edition",
        "stable",
        (
            "standard-observer, illuminant, tristimulus, chromaticity, colour-space, "
            "and colour-difference vocabulary; no photometric calibration or measurement"
        ),
    ),
    _source(
        "CIE-249-2022",
        "CIE 249:2022 Visual Aspects of Time-Modulated Lighting Systems",
        "International Commission on Illumination",
        "https://www.cie.co.at/technical-work/divisions/division1/division-publication",
        "stable",
        (
            "time-modulated-lighting and visual-effect vocabulary only; no human "
            "exposure study, medical conclusion, or safe-strobe threshold decision"
        ),
    ),
    _source(
        "CIE-S017-2020",
        "CIE S 017/E:2020 International Lighting Vocabulary, 2nd Edition",
        "International Commission on Illumination",
        "https://www.cie.co.at/technical-work/divisions/division1/division-publication",
        "stable",
        (
            "lighting, radiometric, photometric, colour, and visual terminology only; "
            "no measurement, calibration, design, or professional conclusion"
        ),
    ),
    _source(
        "W3C-WCAG-22",
        "Web Content Accessibility Guidelines 2.2",
        "W3C",
        "https://www.w3.org/TR/WCAG22/",
        "stable",
        (
            "accessible report structure and non-interference vocabulary with manual, "
            "assistive-technology, affected-user, and venue evaluation reserved"
        ),
    ),
    _source(
        "W3C-WCAG-FLASH",
        "Understanding Success Criterion 2.3.1: Three Flashes or Below Threshold",
        "W3C Web Accessibility Initiative",
        "https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold",
        "current",
        (
            "web-content flash-risk explanation and warning taxonomy only; not a "
            "real performance, audience, clinical, venue, or lighting safety clearance"
        ),
    ),
    _source(
        "W3C-PROV-O",
        "PROV-O: The PROV Ontology",
        "W3C",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        "entity, activity, agent, revision, derivation, cue, custody, and correction lineage",
    ),
    _source(
        "RFC-3339",
        "RFC 3339: Date and Time on the Internet: Timestamps",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic UTC lexical timestamp, time-window, and correction discipline",
    ),
    _source(
        "RFC-8785",
        "RFC 8785: JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic cue, patch, event, and manifest serialization vocabulary",
    ),
    _source(
        "NIST-SP811",
        "NIST SP 811: Guide for the Use of the International System of Units",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/publications/guide-use-international-system-units-si",
        "current",
        (
            "unit, quantity, symbol, and conversion discipline; not real photometry, "
            "colorimetry, electrical metrology, calibration, or competence"
        ),
    ),
    _source(
        "W3C-VC-DM-20",
        "Verifiable Credentials Data Model v2.0",
        "W3C",
        "https://www.w3.org/TR/vc-data-model-2.0/",
        "stable",
        (
            "synthetic fixture-maintenance and role-capability credential vocabulary; "
            "no real issuer, holder, verifier, key, proof, status, or trust claim"
        ),
    ),
    _source(
        "W3C-DID-10",
        "Decentralized Identifiers (DIDs) v1.0",
        "W3C",
        "https://www.w3.org/TR/did-core/",
        "stable",
        (
            "synthetic identifier and controller vocabulary only; v1.1 remains a "
            "candidate recommendation and no live method, resolver, key, or trust exists"
        ),
    ),
    _source(
        "NZ-PRIVACY-ACT-2020",
        "Privacy Act 2020",
        "New Zealand Legislation",
        "https://www.legislation.govt.nz/act/public/2020/31/en/latest/",
        "watch",
        (
            "purpose, minimization, access, correction, retention, recording, "
            "performer, audience, and disclosure reservations without legal interpretation"
        ),
    ),
    _source(
        "TMR-PRINCIPLES",
        "Principles of Māori Data Sovereignty",
        "Te Mana Raraunga",
        "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf",
        "current",
        (
            "Māori rights, interests, governance, jurisdiction, collective benefit, "
            "language, performance-record, and authority reservation only"
        ),
    ),
    _source(
        "LOCAL-CONTEXTS-TK-BC",
        "Traditional Knowledge and Biocultural Labels Usage and Style Guide",
        "Local Contexts",
        "https://localcontexts.org/wp-content/uploads/2023/08/TK-and-BC-Labels-Usage-and-Style-Guide.pdf",
        "current",
        (
            "community-originated notice and provenance reservation only; no label "
            "selection, community decision, cultural authorization, or Māori wording"
        ),
    ),
]


# number, title, slug, pillar, expected disposition, semantic mechanism, source ids
PROPOSAL_ROWS = [
    (
        1,
        "Synthetic stage-lighting venue and rig passport with coarse zone token, drawing revision, inventory checksum, ownership handover, and no-real-venue claim",
        "lighting-rig-passport",
        "THOS Body and Freed ID",
        "completed",
        "rig referent, coarse zone, drawing revision, inventory checksum, ownership handover, and venue refusal",
        ["W3C-PROV-O", "RFC-8785", "NZ-PRIVACY-ACT-2020"],
    ),
    (
        2,
        "Luminaire inventory envelope with fixture type, synthetic unit token, mode, footprint, maintenance state, duplicate quarantine, and no-device claim",
        "luminaire-inventory-envelope",
        "THOS Body and Freed ID",
        "completed",
        "luminaire token, type, mode, footprint, maintenance state, duplicate quarantine, and device refusal",
        ["ESTA-E1-11-2024", "ESTA-E1-32-2022", "W3C-PROV-O"],
    ),
    (
        3,
        "DMX universe, address, footprint, overlap, reserved-slot, and merge-precedence tribunal with deterministic quarantine and zero live packets",
        "dmx-address-tribunal",
        "THOS Body",
        "completed",
        "DMX universe, address, footprint, overlap, reserved slot, merge precedence, quarantine, and live-packet refusal",
        ["ESTA-E1-11-2024", "RFC-8785"],
    ),
    (
        4,
        "RDM discovery and configuration proxy with synthetic UID, collision class, device-info placeholder, start-address proposal, status queue, and no-network rule",
        "rdm-discovery-proxy",
        "THOS Body and Freed ID",
        "completed",
        "RDM UID, discovery, collision, device information, address proposal, status queue, and network refusal",
        ["ESTA-E1-20-2025", "ESTA-E1-37-5-2024"],
    ),
    (
        5,
        "Control patch and circuit ledger with console channel, parameter, universe, address, dimmer placeholder, revision lineage, and no-energization claim",
        "control-patch-ledger",
        "THOS Body",
        "completed",
        "console channel, parameter, universe, address, dimmer placeholder, patch revision, and energization refusal",
        ["ESTA-E1-11-2024", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        6,
        "Synthetic power-distribution balance board with supply placeholder, circuit token, phase bucket, declared load, protective-device gap, and licensed-review hold",
        "power-balance-board",
        "THOS Body and CBR Heart",
        "completed",
        "supply placeholder, circuit, phase bucket, declared load, protection gap, licensed review, and electrical-work refusal",
        ["NZ-WORKSAFE-LV", "NZ-ELECTRICITY-SAFETY-2010", "NIST-SP811"],
    ),
    (
        7,
        "Cable and connector route-custody envelope with synthetic cable token, type, endpoint, path zone, strain-relief cue, inspection hold, and no-installation action",
        "cable-route-custody",
        "THOS Body",
        "completed",
        "cable token, connector, endpoint, path zone, strain relief, inspection hold, and installation refusal",
        ["ESTA-E1-11-2024", "ESTA-E1-32-2022", "W3C-PROV-O"],
    ),
    (
        8,
        "Rigging-point and suspended-load reservation board with point token, load placeholder, safety-factor gap, competent-person hold, and no-rigging decision",
        "rigging-load-reservation",
        "THOS Body and CBR Heart",
        "completed",
        "rigging point, suspended load, safety factor, competent review, hold, and rigging-decision refusal",
        ["NZ-WORKSAFE-EVENT-RISK", "W3C-PROV-O", "NIST-SP811"],
    ),
    (
        9,
        "Safety-bond, secondary-suspension, shutter, lens, housing, and fall-risk inspection proxy with defect quarantine and no-physical-inspection claim",
        "luminaire-fall-risk-proxy",
        "THOS Body and CBR Heart",
        "completed",
        "secondary suspension, shutter, lens, housing, defect, quarantine, fall risk, and inspection refusal",
        ["ESTA-E1-32-2022", "NZ-WORKSAFE-EVENT-RISK"],
    ),
    (
        10,
        "Pan, tilt, focus, zoom, shutter, iris, gobo, prism, and frost state ledger with home-state conflict and no-motion command",
        "optical-state-ledger",
        "THOS Body",
        "completed",
        "pan, tilt, focus, zoom, shutter, iris, gobo, prism, frost, home conflict, and motion refusal",
        ["ESTA-E1-11-2024", "ESTA-E1-20-2025", "RFC-8785"],
    ),
    (
        11,
        "Colour filter and LED mix provenance board with source channel, spectral placeholder, observer declaration, transformation lineage, gamut hold, and no-colour-accuracy claim",
        "colour-mix-provenance",
        "GMUT Mind and THOS Body",
        "completed",
        "colour channel, spectrum placeholder, observer, transformation, gamut, lineage, and accuracy refusal",
        ["CIE-015-2018", "CIE-S017-2020", "W3C-PROV-O"],
    ),
    (
        12,
        "Photometric lux and beam proxy with distance, angle, field and beam placeholders, inverse-square obligation, calibration gap, uncertainty, and zero measurement",
        "photometric-beam-proxy",
        "GMUT Mind and THOS Body",
        "represented",
        "distance, angle, illuminance proxy, beam, field, inverse-square obligation, calibration, uncertainty, and measurement refusal",
        ["CIE-S017-2020", "NIST-SP811", "NZ-MBIE-F6-AS1"],
    ),
    (
        13,
        "Frame-rate and lighting-flicker compatibility docket with modulation placeholder, camera-rate declaration, alias-risk class, review hold, and no-shoot clearance",
        "flicker-camera-docket",
        "THOS Body and GMUT Mind",
        "completed",
        "time modulation, frame rate, alias risk, review hold, camera compatibility, and clearance refusal",
        ["CIE-249-2022", "W3C-WCAG-FLASH"],
    ),
    (
        14,
        "Cue stack and dependency ledger with cue number, trigger, fade, delay, follow, target state, rollback, collision quarantine, and no-console execution",
        "cue-stack-ledger",
        "THOS Body",
        "completed",
        "cue number, trigger, fade, delay, follow, target state, dependency, rollback, and execution refusal",
        ["ESTA-E1-11-2024", "RFC-3339", "RFC-8785"],
    ),
    (
        15,
        "Rehearsal change-delta register with request source, before and after state, reason, approval gap, readback, supersession, and no-performance acceptance",
        "rehearsal-change-register",
        "THOS Body and CBR Heart",
        "completed",
        "change request, before state, after state, reason, approval, readback, supersession, and performance refusal",
        ["W3C-PROV-O", "RFC-3339", "NZ-WORKSAFE-EVENT-RISK"],
    ),
    (
        16,
        "Blackout, emergency-lighting, house-light, exit-route, and show-control separation board with fail-closed boundary and no-emergency system command",
        "emergency-lighting-separation",
        "THOS Body and CBR Heart",
        "completed",
        "show blackout, emergency lighting, house light, exit route, fail-closed separation, and emergency-command refusal",
        ["NZ-MBIE-F6-AS1", "NZ-WORKSAFE-EVENT-RISK", "NZ-WORKSAFE-LV"],
    ),
    (
        17,
        "Accessible cue notice and sensory-warning envelope with noncolour state, plain-language summary, strobe declaration, alternative path, acknowledgement, and user-review reserve",
        "accessible-cue-warning",
        "CBR Heart and THOS Body",
        "completed",
        "cue notice, noncolour state, plain language, strobe warning, alternative path, acknowledgement, and user-review reserve",
        ["W3C-WCAG-22", "W3C-WCAG-FLASH", "NZ-WORKSAFE-EVENT-RISK"],
    ),
    (
        18,
        "Heat, ventilation, obstruction, fire cue, flammable-material, and shutdown-hold docket with competent review gap and no-fire-safety determination",
        "thermal-fire-hold-docket",
        "THOS Body and CBR Heart",
        "completed",
        "heat, ventilation, obstruction, flammable material, shutdown hold, competent review, and fire-safety refusal",
        ["ESTA-E1-32-2022", "NZ-WORKSAFE-EVENT-RISK", "NZ-ELECTRICITY-SAFETY-2010"],
    ),
    (
        19,
        "Lighting incident and near-miss evidence-preservation docket with shock cue, falling-object cue, flash complaint, pause, correction, review, and remedy reservation",
        "lighting-incident-remedy",
        "CBR Heart",
        "completed",
        "incident, near miss, shock cue, falling object, flash complaint, pause, correction, remedy, and adjudication refusal",
        ["NZ-WORKSAFE-EVENT-RISK", "NZ-PRIVACY-ACT-2020", "W3C-PROV-O"],
    ),
    (
        20,
        "Workload and shift-handover governor with unresolved cue, patch hold, fault queue, rest threshold, sender-receiver checksum, readback, and release refusal",
        "lighting-shift-handover",
        "THOS Body and CBR Heart",
        "completed",
        "workload, unresolved cue, patch hold, fault queue, rest threshold, checksum, readback, and release refusal",
        ["NZ-WORKSAFE-EVENT-RISK", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        21,
        "GMUT typed inverse-square and beam-field obligation board with radiant source, solid angle, distance domain, illuminance proxy, singularity guard, and observation firewall",
        "gmut-beam-field-board",
        "GMUT Mind",
        "completed",
        "typed source, solid angle, distance, illuminance proxy, inverse-square domain, singularity, and observation firewall",
        ["CIE-S017-2020", "NIST-SP811"],
    ),
    (
        22,
        "GMUT tristimulus and chromaticity transformation board with observer, illuminant, matrix domain, white point, gamut, unit, and perceptual-accuracy firewall",
        "gmut-colour-transform-board",
        "GMUT Mind",
        "completed",
        "typed tristimulus, chromaticity, observer, illuminant, transform, white point, gamut, and perception firewall",
        ["CIE-015-2018", "NIST-SP811"],
    ),
    (
        23,
        "GMUT discrete cue-state transition board with state vector, trigger, guard, timing domain, conflict relation, deterministic rollback, and real-control firewall",
        "gmut-cue-transition-board",
        "GMUT Mind",
        "completed",
        "typed cue state, trigger, guard, timing, conflict, deterministic transition, rollback, and control firewall",
        ["ESTA-E1-11-2024", "RFC-3339", "RFC-8785"],
    ),
    (
        24,
        "THOS cue-follow recovery drill design with sealed comparison lanes, equal action windows, error-correction endpoint, fatigue and harm stop rules, synthetic case registration, and no participants",
        "thos-cue-study-protocol",
        "THOS Body",
        "represented",
        "cue-follow recovery comparison, sealed lanes, equal action windows, correction endpoint, fatigue, harm stop, and participant refusal",
        ["NZ-WORKSAFE-EVENT-RISK", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        25,
        "THOS lighting fault-triage proxy with fixture token, fault source, persistence, confidence, acknowledgement, escalation, handover, and no-safety decision",
        "thos-lighting-fault-triage",
        "THOS Body",
        "represented",
        "synthetic lighting fault, source, persistence, confidence, acknowledgement, escalation, handover, and safety refusal",
        ["ESTA-E1-20-2025", "ESTA-E1-32-2022", "NZ-WORKSAFE-EVENT-RISK"],
    ),
    (
        26,
        "Freed ID synthetic fixture-maintenance evidence bundle with luminaire referent, inspection digest, method source, defect class, validity interval, issuer placeholder, and cryptographic refusal",
        "freed-id-fixture-credential",
        "Freed ID",
        "represented",
        "synthetic maintenance evidence, luminaire referent, inspection digest, defect class, validity, issuer, and cryptographic gaps",
        ["W3C-VC-DM-20", "W3C-DID-10", "ESTA-E1-32-2022"],
    ),
    (
        27,
        "Freed ID console-session grant envelope with unlinkable operator placeholder, command-set allowlist, expiry, provenance chain, purpose ceiling, non-correlation budget, and unresolved revocation",
        "freed-id-lighting-capability",
        "Freed ID and CBR Heart",
        "represented",
        "synthetic console grant, unlinkable operator, command allowlist, expiry, provenance, purpose ceiling, correlation, revocation, and nonproduction proxy",
        ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-ACT-2020"],
    ),
    (
        28,
        "Performance-content, recording, performer, audience, cue-note, complaint, retention, correction, disclosure, and data-minimization envelope with privacy-complete refusal",
        "performance-privacy-envelope",
        "CBR Heart and Freed ID",
        "completed",
        "performance content, recording, performer, audience, cue note, complaint, retention, correction, disclosure, and privacy refusal",
        ["NZ-PRIVACY-ACT-2020", "W3C-PROV-O", "W3C-WCAG-22"],
    ),
    (
        29,
        "Real venue photometry, camera-flicker, operator-workload, accessibility, and audience-response adapter with zero people, zero venue, zero query, zero measurement, and zero rows",
        "venue-study-zero-row-adapter",
        "THOS Body and GMUT Mind",
        "open_gap",
        "real venue, photometry, flicker, operator workload, accessibility, audience response, authorization, and zero-row refusal",
        ["CIE-249-2022", "NZ-WORKSAFE-EVENT-RISK", "W3C-WCAG-FLASH"],
    ),
    (
        30,
        "CBR stage-lighting content, performer, audience, disability, strobe, privacy, remedy, legal, cultural, data-governance, affected-party, Māori-language, and Māori-authority matrix",
        "cbr-lighting-authority-matrix",
        "Freed ID and CBR Heart",
        "exact_gate",
        "content, performer, audience, disability, strobe, privacy, remedy, legal, cultural, governance, language, and authority reservation",
        [
            "NZ-PRIVACY-ACT-2020",
            "W3C-WCAG-22",
            "TMR-PRINCIPLES",
            "LOCAL-CONTEXTS-TK-BC",
        ],
    ),
]


SKILL_IDEAS = [
    "ghc-family-stage-lighting-rig-passport-boundary",
    "ghc-family-stage-lighting-control-patch-integrity",
    "ghc-family-stage-lighting-power-rigging-reserve",
    "ghc-family-stage-lighting-optical-colour-proxy",
    "ghc-family-stage-lighting-cue-rehearsal-handover",
    "ghc-family-stage-lighting-emergency-accessibility-boundary",
    "ghc-family-stage-lighting-incident-workload-privacy",
    "ghc-family-gmut-stage-light-field-firewall",
    "ghc-family-thos-freed-stage-lighting-profile",
    "ghc-family-stage-lighting-evidence-nonpromotion",
]


RUNNER_IDEAS = [
    "ghc_family_stage_lighting_rig_passport_boundary.py",
    "ghc_family_stage_lighting_control_patch_integrity.py",
    "ghc_family_stage_lighting_power_rigging_reserve.py",
    "ghc_family_stage_lighting_optical_colour_proxy.py",
    "ghc_family_stage_lighting_cue_rehearsal_handover.py",
    "ghc_family_stage_lighting_emergency_accessibility_boundary.py",
    "ghc_family_stage_lighting_incident_workload_privacy.py",
    "ghc_family_gmut_stage_light_field_firewall.py",
    "ghc_family_thos_freed_stage_lighting_profile.py",
    "ghc_family_v655_v8_suite.py",
]


CLEAN_SURFACES = [
    "venue, rig, luminaire, universe, address, mode, footprint, and revision vocabulary",
    "RDM discovery, UID, collision, status, configuration proposal, and zero-network separation",
    "patch, circuit, supply, phase, load, protection, cable, and licensed-review holds",
    "rigging point, suspended load, secondary suspension, defect, and competent-review refusal",
    "pan, tilt, focus, shutter, gobo, colour, beam, flicker, and measurement proxies",
    "cue, trigger, fade, dependency, rehearsal delta, readback, rollback, and handover states",
    "blackout, emergency-lighting, exit-route, warning, accessibility, heat, and fire separation",
    "incident, workload, privacy, complaint, retention, disclosure, and remedy reservations",
    "GMUT beam field, colour transform, cue transition, unit, domain, and observation firewalls",
    "professional, electrical, rigging, safety, affected-party, legal, cultural, and Māori-authority refusal",
]


def _negative(
    number: int,
    signature: str,
    failed: str,
    recovery: str,
    recurrence_guard: str,
) -> dict:
    return {
        "negative_id": f"V6558-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": recurrence_guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "memory_rg_search_timed_out",
        "The first bounded ripgrep lookup of the memory registry timed out without usable current-route evidence.",
        "Read the exact registry with the direct Node filesystem API and stop when no current v655 entry is present.",
        "Use a direct bounded file read when the shell search surface is stalled.",
    ),
    _negative(
        2,
        "memory_powershell_get_content_timed_out",
        "A second memory lookup using PowerShell Get-Content timed out before returning attributable lines.",
        "Keep the failure at zero credit and use the direct Node filesystem read only.",
        "Do not retry PowerShell file reads after the shell surface has already stalled.",
    ),
    _negative(
        3,
        "memory_dotnet_read_wrapper_timed_out",
        "A direct .NET memory-file read invoked through PowerShell also timed out without output.",
        "Bypass the stalled shell host and read the exact UTF-8 file through Node.",
        "Separate the file API from a stalled shell host rather than changing the target.",
    ),
    _negative(
        4,
        "powershell_get_location_timed_out",
        "Even the scalar PowerShell Get-Location probe exceeded its bounded window.",
        "Use the trusted desktop request context and Node runtime path values for exact path resolution.",
        "Do not treat a stalled shell prompt as evidence that a repository path is absent.",
    ),
    _negative(
        5,
        "node_auth_wrapper_referenced_unavailable_process",
        "The first auth-state validator wrapper referenced process.env, which is unavailable to model code in the Node REPL, so validation did not run.",
        "Invoke the exact validator without constructing a process environment; the validator then passed.",
        "Do not reference the blocked process global in Node REPL model code.",
    ),
    _negative(
        6,
        "evidence_manifest_working_bytes_compared_to_git_blobs",
        "The first evidence-manifest probe compared checkout working_bytes to normalized Git blob bytes and reported false byte mismatches.",
        "Validate git_blob against the evidence commit tree and working_bytes against the clean checkout in their separately declared domains.",
        "Read each manifest field's hash domain before comparing byte counts.",
    ),
    _negative(
        7,
        "combined_new_lane_reconciliation_timed_out",
        "The first combined post-checkout head, branch, staged, worktree, and untracked probe exceeded its bounded window.",
        "Split exact head and branch metadata from staged and owner-path cleanliness probes; each bounded recovery passed.",
        "Keep identity and cleanliness checks separately attributable on large archive-backed worktrees.",
    ),
    _negative(
        8,
        "whole_tree_diff_index_probe_timed_out",
        "A whole-tree diff-index probe scanned the 57,593-file checkout and timed out without clean-state credit.",
        "Use cached index-to-HEAD comparison plus exact owner-path tracked and untracked probes; all bounded recovery checks passed.",
        "Use owner-path scopes for worktree checks and reserve whole-tree scans for the supervised terminal validator.",
    ),
    _negative(
        9,
        "first_x1_novelty_candidate_exceeded_lexical_ceiling",
        "The first x1 materialization stopped before generated writes because two proposed titles scored 0.809524 and 0.692308 against inherited mechanisms, above the 0.60 lexical ceiling.",
        "Retain the stage-lighting mechanisms but rewrite their preregistration language to state the distinct cue-recovery and console-session obligations before rerunning the changed candidate.",
        "Run the complete inherited-chain lexical audit before any generated x1 artifact and keep every over-ceiling candidate at zero credit.",
    ),
]
