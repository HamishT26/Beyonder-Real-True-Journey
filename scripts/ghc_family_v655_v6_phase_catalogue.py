#!/usr/bin/env python3
"""Caelen Ash v655-v6 source, proposal, portfolio, and startup catalogue."""

from __future__ import annotations


OFFICIAL_SOURCES = [
    {
        "source_id": "NZ-RSM-AMATEUR-GURL",
        "title": "Amateur Radio Operators GURL",
        "publisher": "Radio Spectrum Management New Zealand",
        "url": "https://www.rsm.govt.nz/licensing/frequencies-for-anyone/amateur-radio-operators",
        "status": "current",
        "use": (
            "current qualification, callsign, frequency, power, interference, "
            "and licence-condition context only; no transmission or compliance claim"
        ),
    },
    {
        "source_id": "NZ-GAZETTE-AMATEUR-2025",
        "title": (
            "Radiocommunications Regulations (General User Radio Licence for "
            "Amateur Radio Operators) Notice 2025"
        ),
        "publisher": "New Zealand Gazette",
        "url": "https://gazette.govt.nz/notice/id/2025-go3272",
        "status": "watch",
        "use": (
            "current legal-condition and band-table watch source only; all "
            "interpretation and real operation remain reserved"
        ),
    },
    {
        "source_id": "NZ-RSM-PIB46",
        "title": "Radio Operator Certificate and Callsign Rules (PIB 46)",
        "publisher": "Radio Spectrum Management New Zealand",
        "url": (
            "https://www.rsm.govt.nz/assets/Uploads/documents/pibs/"
            "radio-operator-certificate-and-callsign-rules-pib-46.pdf"
        ),
        "status": "current",
        "use": (
            "certificate and callsign vocabulary and source-version checks only; "
            "no qualification, allocation, registry, or identity assertion"
        ),
    },
    {
        "source_id": "NZ-RADIOCOMM-ACT-1989",
        "title": "Radiocommunications Act 1989",
        "publisher": "New Zealand Legislation",
        "url": "https://www.legislation.govt.nz/act/public/1989/0148/latest/",
        "status": "watch",
        "use": (
            "licensing, interference, enforcement, and authority reservation "
            "without legal interpretation"
        ),
    },
    {
        "source_id": "NZ-HEALTH-RF",
        "title": "Exposures to radiofrequency fields near 5G cellsites",
        "publisher": "New Zealand Ministry of Health",
        "url": (
            "https://www.health.govt.nz/publications/"
            "exposures-to-radiofrequency-fields-near-5g-cellsites"
        ),
        "status": "watch",
        "use": (
            "New Zealand RF exposure-standard context and competent-assessment "
            "reservation only; no exposure, siting, or safety determination"
        ),
    },
    {
        "source_id": "NZ-NEMA-VOLUNTEERS",
        "title": "Volunteers crucial to our emergency management system",
        "publisher": "National Emergency Management Agency",
        "url": (
            "https://www.civildefence.govt.nz/about/news-and-events/"
            "news-and-events/volunteers-crucial-to-our-emergency-management-system"
        ),
        "status": "current",
        "use": (
            "public evidence that volunteer emergency-communications roles exist; "
            "no dispatch, emergency-management, volunteer, or response authority"
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
            "and disclosure reservations without legal interpretation"
        ),
    },
    {
        "source_id": "NZ-HSWA-2015",
        "title": "Health and Safety at Work Act 2015",
        "publisher": "New Zealand Legislation",
        "url": "https://www.legislation.govt.nz/act/public/2015/70/en/latest/",
        "status": "watch",
        "use": (
            "workplace duty, training, unsafe-work, and competent-person "
            "reservation without legal interpretation"
        ),
    },
    {
        "source_id": "ITU-RR-2024",
        "title": "Radio Regulations, Edition of 2024",
        "publisher": "International Telecommunication Union",
        "url": "https://www.itu.int/pub/R-REG-RR-2024/",
        "status": "current",
        "use": (
            "amateur-service, international communication, and disaster-relief "
            "context only; no treaty interpretation or operational authority"
        ),
    },
    {
        "source_id": "W3C-VC-DM-20",
        "title": "Verifiable Credentials Data Model v2.0",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "stable",
        "use": (
            "synthetic station-status claim, validity, status, privacy, and "
            "nonproduction credential vocabulary"
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
        "source_id": "W3C-WCAG-22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "stable",
        "use": (
            "accessible static-form structure with manual, assistive-technology, "
            "Māori-language, and affected-user review reserved"
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
            "and handover vocabulary"
        ),
    },
    {
        "source_id": "RFC-3339",
        "title": "RFC 3339 — Date and Time on the Internet: Timestamps",
        "publisher": "RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc3339.html",
        "status": "stable",
        "use": "synthetic UTC lexical timestamp and correction discipline",
    },
    {
        "source_id": "RFC-8785",
        "title": "RFC 8785 — JSON Canonicalization Scheme",
        "publisher": "RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "stable",
        "use": "deterministic synthetic radio-event serialization vocabulary",
    },
    {
        "source_id": "RFC-9052",
        "title": "RFC 9052 — CBOR Object Signing and Encryption: Structures and Process",
        "publisher": "RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc9052.html",
        "status": "watch",
        "use": (
            "synthetic COSE structure vocabulary with known update and errata watch; "
            "no key, signature, security, or interoperability claim"
        ),
    },
    {
        "source_id": "NIST-SP811",
        "title": "NIST SP 811 — Guide for the Use of the International System of Units",
        "publisher": "National Institute of Standards and Technology",
        "url": "https://www.nist.gov/publications/guide-use-international-system-units-si",
        "status": "current",
        "use": (
            "unit and conversion discipline; not instrument calibration, RF "
            "exposure evidence, propagation validation, or measurement authority"
        ),
    },
    {
        "source_id": "FRIIS-1946",
        "title": "A Note on a Simple Transmission Formula",
        "publisher": "Proceedings of the IRE / IEEE",
        "url": "https://doi.org/10.1109/JRPROC.1946.234568",
        "status": "stable",
        "use": (
            "historical free-space transmission-relation provenance and declared "
            "domain only; no real link, reception, coverage, or safety prediction"
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
            "Māori rights, interests, governance, jurisdiction, and authority "
            "reservation only"
        ),
    },
]


# number, title, slug, pillar, expected disposition, semantic mechanism, source ids
PROPOSAL_ROWS = [
    (
        1,
        "Synthetic amateur-radio station passport with station token, "
        "location-precision ceiling, operator-callsign placeholder, licence-status "
        "gap, revision, collision quarantine, and no-transmission rule",
        "amateur-station-passport",
        "Freed ID and CBR Heart",
        "completed",
        "station referent, location minimization, callsign gap, revision, and transmission refusal",
        ["NZ-RSM-AMATEUR-GURL", "NZ-RSM-PIB46", "W3C-PROV-O"],
    ),
    (
        2,
        "Amateur-radio operator authorization provenance card with "
        "certificate-class placeholder, callsign-source reference, privilege-scope "
        "version, expiry gap, visitor state, uncertainty, and no-competency assertion",
        "radio-authorization-provenance",
        "Freed ID and CBR Heart",
        "completed",
        "operator authorization provenance, scope version, expiry gap, and competency refusal",
        ["NZ-RSM-AMATEUR-GURL", "NZ-RSM-PIB46", "NZ-RADIOCOMM-ACT-1989"],
    ),
    (
        3,
        "Radio callsign, club role, message role, station token, and person-identity "
        "crosswalk with namespace source, alias interval, collision, correction, "
        "privacy minimum, and identity-conflation refusal",
        "radio-callsign-role-crosswalk",
        "Freed ID",
        "completed",
        "callsign, role, station, and person referent separation with collision and privacy refusal",
        ["NZ-RSM-PIB46", "NZ-PRIVACY-ACT-2020", "W3C-PROV-O"],
    ),
    (
        4,
        "Amateur band, frequency, emission mode, bandwidth, power ceiling, "
        "licence-source version, designated-use condition, uncertainty, and "
        "tune-or-transmit refusal ledger",
        "radio-spectrum-condition-ledger",
        "CBR Heart and THOS Body",
        "completed",
        "band, mode, bandwidth, power, source-version, and transmit-refusal contract",
        ["NZ-GAZETTE-AMATEUR-2025", "ITU-RR-2024", "NZ-RADIOCOMM-ACT-1989"],
    ),
    (
        5,
        "Radio equipment inventory docket with transceiver token, receive-only flag, "
        "firmware placeholder, serial minimization, accessory relation, custody "
        "state, configuration revision, and operation hold",
        "radio-equipment-inventory",
        "Freed ID and THOS Body",
        "completed",
        "radio equipment referent, configuration, custody, serial minimization, and operation hold",
        ["NZ-RSM-AMATEUR-GURL", "W3C-PROV-O", "NZ-PRIVACY-ACT-2020"],
    ),
    (
        6,
        "Antenna and feedline configuration proxy with antenna class, height "
        "placeholder, connector chain, impedance symbol, routing constraint, "
        "installation gap, weather hold, and no-physical-installation rule",
        "radio-antenna-feedline-proxy",
        "THOS Body and GMUT Mind",
        "represented",
        "antenna, feedline, impedance, routing, installation-gap, and physical-action proxy",
        ["NZ-RSM-AMATEUR-GURL", "NZ-HEALTH-RF", "NIST-SP811"],
    ),
    (
        7,
        "Radiofrequency exposure-control proxy with power placeholder, duty-cycle "
        "symbol, separation zone, public and occupational distinction, "
        "source-version gap, uncertainty, stop condition, and no-safety determination",
        "radiofrequency-exposure-proxy",
        "THOS Body and CBR Heart",
        "represented",
        "RF power, duty-cycle, separation, exposure-source, uncertainty, and safety-decision proxy",
        ["NZ-HEALTH-RF", "NIST-SP811", "NZ-RADIOCOMM-ACT-1989"],
    ),
    (
        8,
        "Standing-wave-ratio and forward-reflected-power measurement proxy with "
        "instrument placeholder, calibration gap, frequency, unit, uncertainty, "
        "repeat cue, mismatch hold, and no-real-measurement rule",
        "radio-swr-power-measurement-proxy",
        "GMUT Mind and THOS Body",
        "represented",
        "standing-wave-ratio and power measurement method, calibration, uncertainty, and real-measurement proxy",
        ["NIST-SP811", "NZ-HEALTH-RF"],
    ),
    (
        9,
        "Station power, battery, charging, fuse, grounding, ventilation, heat, fire "
        "cue, isolation state, competent-review gap, and energization refusal board",
        "radio-station-energy-boundary",
        "THOS Body and CBR Heart",
        "completed",
        "station energy, battery, isolation, heat, fire cue, competent review, and energization refusal",
        ["NZ-HSWA-2015", "NZ-HEALTH-RF", "W3C-PROV-O"],
    ),
    (
        10,
        "Radio station startup and shutdown state machine with antenna-path "
        "placeholder, mode and frequency confirmation, power ceiling, dummy-load "
        "state, readback, abort, and physical-operation refusal",
        "radio-startup-shutdown-state-machine",
        "THOS Body",
        "completed",
        "station startup and shutdown state, readback, abort, and physical-operation refusal",
        ["NZ-RSM-AMATEUR-GURL", "NZ-GAZETTE-AMATEUR-2025"],
    ),
    (
        11,
        "Amateur contact log envelope with synthetic peer token, UTC lexical time, "
        "band, mode, exchanged-report placeholder, source revision, correction "
        "lineage, retention class, and no-contact claim",
        "radio-contact-log-envelope",
        "Freed ID and CBR Heart",
        "completed",
        "synthetic contact log, time, peer minimization, correction, retention, and contact-claim refusal",
        ["NZ-RSM-AMATEUR-GURL", "NZ-RSM-PIB46", "RFC-3339"],
    ),
    (
        12,
        "Emergency-message custody envelope with synthetic originator token, "
        "content-minimum, precedence placeholder, destination role, relay count, "
        "disclosure ceiling, acknowledgement state, and no-dispatch rule",
        "radio-emergency-message-custody",
        "CBR Heart and Freed ID",
        "completed",
        "emergency-message custody, content minimization, relay, acknowledgement, and dispatch refusal",
        ["NZ-GAZETTE-AMATEUR-2025", "NZ-NEMA-VOLUNTEERS", "NZ-PRIVACY-ACT-2020"],
    ),
    (
        13,
        "Phonetic spelling, numeral, timestamp, location-minimization, readback, "
        "mismatch, correction-statement, supersession, and message-integrity "
        "nonclaim ledger",
        "radio-message-readback-lineage",
        "CBR Heart and THOS Body",
        "completed",
        "message spelling, time, location minimization, readback, correction, and integrity nonclaim",
        ["RFC-3339", "W3C-PROV-O", "NZ-PRIVACY-ACT-2020"],
    ),
    (
        14,
        "Synthetic radio-net check-in lattice with session token, participant "
        "pseudonym, role placeholder, check-in state, missed-call marker, correction, "
        "workload ceiling, and no-net-control authority",
        "radio-net-checkin-lattice",
        "THOS Body and Freed ID",
        "completed",
        "synthetic radio-net session, role, check-in, correction, workload, and control-authority refusal",
        ["NZ-NEMA-VOLUNTEERS", "NZ-PRIVACY-ACT-2020", "W3C-PROV-O"],
    ),
    (
        15,
        "Emergency traffic form simulation with message number, precedence "
        "placeholder, origin time, address-minimum, text line budget, callback "
        "placeholder, delivery state, and no-emergency-action rule",
        "radio-emergency-traffic-form",
        "CBR Heart and THOS Body",
        "completed",
        "emergency traffic form, address minimization, delivery state, and emergency-action refusal",
        ["NZ-NEMA-VOLUNTEERS", "NZ-GAZETTE-AMATEUR-2025", "NZ-PRIVACY-ACT-2020"],
    ),
    (
        16,
        "Radio interference observation and referral docket with receive-state "
        "placeholder, frequency and time, symptom vocabulary, device relation, "
        "uncertainty, evidence minimum, escalation route, and no-enforcement decision",
        "radio-interference-referral",
        "CBR Heart and THOS Body",
        "completed",
        "interference observation, uncertainty, evidence minimization, referral, and enforcement refusal",
        ["NZ-RSM-AMATEUR-GURL", "NZ-RADIOCOMM-ACT-1989", "W3C-PROV-O"],
    ),
    (
        17,
        "Digital-mode configuration manifest with application and modem version, "
        "audio device token, sample-rate placeholder, tone and bandwidth setting, "
        "clock source, file digest, and no-live-signal rule",
        "radio-digital-mode-configuration",
        "Freed ID and GMUT Mind",
        "completed",
        "digital-mode configuration, version, sample-rate, clock, digest, and live-signal refusal",
        ["NZ-RSM-AMATEUR-GURL", "RFC-8785", "NIST-SP811"],
    ),
    (
        18,
        "Accessible radio log and message-form audit with heading hierarchy, field "
        "labels, error association, noncolour state, keyboard order, plain-language "
        "readback, print fallback, and affected-user testing gap",
        "accessible-radio-log-audit",
        "CBR Heart",
        "completed",
        "radio log structure, error association, keyboard order, readback, fallback, and testing reserve",
        ["W3C-WCAG-22", "NZ-PRIVACY-ACT-2020"],
    ),
    (
        19,
        "Radio-log privacy and retention envelope with purpose, callsign exposure "
        "class, precise-location suppression, message-content sensitivity, access "
        "and correction state, deletion-basis gap, and privacy-complete refusal",
        "radio-log-privacy-envelope",
        "Freed ID and CBR Heart",
        "completed",
        "radio-log purpose, callsign and location minimization, correction, retention, and privacy refusal",
        ["NZ-PRIVACY-ACT-2020", "NZ-RSM-PIB46", "W3C-PROV-O"],
    ),
    (
        20,
        "Radio incident, complaint, correction, and remedy provenance ledger with "
        "harm placeholder, evidence quality, immediate containment, review gap, "
        "communication minimum, appeal route, and no-rights adjudication",
        "radio-incident-remedy-ledger",
        "CBR Heart",
        "completed",
        "radio incident, complaint, correction, remedy, review gap, and rights-adjudication refusal",
        ["NZ-PRIVACY-ACT-2020", "W3C-WCAG-22", "TMR-PRINCIPLES"],
    ),
    (
        21,
        "Station workload and shift-handover governor with queue class, unresolved "
        "message, equipment hold, break trigger, fatigue placeholder, dual readback, "
        "receiver question log, and automatic-release refusal",
        "radio-shift-handover-governor",
        "THOS Body and CBR Heart",
        "completed",
        "radio workload, unresolved message, equipment hold, fatigue, readback, handover, and release refusal",
        ["NZ-NEMA-VOLUNTEERS", "NZ-HSWA-2015", "W3C-PROV-O"],
    ),
    (
        22,
        "GMUT typed transmission-line telegrapher board with voltage-current state, "
        "per-length resistance, inductance, conductance, capacitance, boundary "
        "condition, unit domain, and observation firewall",
        "gmut-transmission-line-board",
        "GMUT Mind",
        "completed",
        "typed transmission-line state, per-length parameters, boundary conditions, units, and observation firewall",
        ["NIST-SP811"],
    ),
    (
        23,
        "GMUT radiofrequency RLC resonance board with inductance, capacitance, "
        "resistance, angular-frequency domain, quality-factor relation, loss "
        "placeholder, unit contract, and physical-prediction firewall",
        "gmut-radio-rlc-resonance",
        "GMUT Mind",
        "completed",
        "typed RLC resonance, angular-frequency domain, quality factor, loss, units, and prediction firewall",
        ["NIST-SP811"],
    ),
    (
        24,
        "GMUT free-space link-budget board with transmit-power symbol, antenna-gain "
        "placeholders, wavelength, range domain, path-loss relation, unit conversion, "
        "approximation scope, and reception-prediction firewall",
        "gmut-free-space-link-budget",
        "GMUT Mind",
        "completed",
        "free-space link relation, gain placeholders, wavelength, range, units, approximation, and prediction firewall",
        ["FRIIS-1946", "NIST-SP811"],
    ),
    (
        25,
        "THOS synthetic net-control task envelope with objective, message queue, role "
        "placeholders, priority rule, stop condition, workload budget, correction "
        "readback, and live-participant refusal",
        "thos-radio-net-control-proxy",
        "THOS Body",
        "represented",
        "synthetic net-control objective, queue, role, priority, workload, correction, and participant proxy",
        ["NZ-NEMA-VOLUNTEERS", "NZ-RSM-AMATEUR-GURL"],
    ),
    (
        26,
        "THOS radio-message handover graph with queue node, dependency edge, "
        "unresolved item, duplicate-message quarantine, harm stop, receiver "
        "acknowledgement, correction latency, and operational-service refusal",
        "thos-radio-message-handover",
        "THOS Body and CBR Heart",
        "completed",
        "radio-message queue, dependency, duplicate quarantine, harm stop, handover, and service refusal",
        ["NZ-NEMA-VOLUNTEERS", "W3C-PROV-O"],
    ),
    (
        27,
        "Freed ID synthetic amateur-station status credential with issuer and subject "
        "placeholders, callsign claim minimum, privilege-scope placeholder, validity, "
        "proof absence, status gap, and nonproduction refusal",
        "freed-id-radio-status-credential",
        "Freed ID",
        "represented",
        "synthetic amateur-station status credential, claim minimization, validity, proof and status gaps",
        ["W3C-VC-DM-20", "W3C-DID-10", "RFC-9052"],
    ),
    (
        28,
        "Freed ID selective-disclosure radio-role profile with station pseudonym, "
        "operator-qualification predicate placeholder, purpose binding, verifier "
        "class, correlation warning, revocation gap, and nonproduction refusal",
        "freed-id-radio-role-disclosure",
        "Freed ID and CBR Heart",
        "completed",
        "synthetic radio-role selective disclosure, purpose binding, correlation warning, and revocation gap",
        ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-ACT-2020"],
    ),
    (
        29,
        "Real amateur-radio propagation, field-strength, contact-log, interference, "
        "and message-delivery dataset adapter with authorization, calibration, "
        "sampling frame, privacy review, independent analysis, and zero-row "
        "zero-transmission firewall",
        "radio-real-data-zero-row-adapter",
        "GMUT Mind, THOS Body, and CBR Heart",
        "open_gap",
        "real propagation, field-strength, contact-log, interference, and delivery dataset readiness with zero-row refusal",
        ["NZ-RSM-AMATEUR-GURL", "NZ-HEALTH-RF", "NIST-SP811", "W3C-PROV-O"],
    ),
    (
        30,
        "CBR amateur-service governance and spectrum-sharing reservation with "
        "station, callsign, interference, third-party traffic, disaster-relief role, "
        "land and site access, radiofrequency boundary, complaint, remedy, legal, "
        "cultural, tangata-whenua, iwi, hapū, and Māori authority",
        "radio-rights-authority-reservation",
        "CBR Heart",
        "exact_gate",
        "amateur-service governance, spectrum sharing, emergency role, land, remedy, legal, cultural, and Māori-authority reservation",
        [
            "NZ-GAZETTE-AMATEUR-2025",
            "NZ-RADIOCOMM-ACT-1989",
            "ITU-RR-2024",
            "NZ-NEMA-VOLUNTEERS",
            "NZ-PRIVACY-ACT-2020",
            "TMR-PRINCIPLES",
        ],
    ),
]


SKILL_IDEAS = [
    "ghc-family-amateur-station-boundary",
    "ghc-family-radio-equipment-antenna",
    "ghc-family-radio-measurement-safety-proxy",
    "ghc-family-radio-message-custody",
    "ghc-family-radio-net-handover",
    "ghc-family-radio-interference-accessibility",
    "ghc-family-radio-privacy-remedy",
    "ghc-family-gmut-radio-observation-firewall",
    "ghc-family-thos-freed-radio-profile",
    "ghc-family-radio-evidence-nonpromotion",
]


RUNNER_IDEAS = [
    "ghc_family_amateur_station_boundary.py",
    "ghc_family_radio_equipment_antenna.py",
    "ghc_family_radio_measurement_safety_proxy.py",
    "ghc_family_radio_message_custody.py",
    "ghc_family_radio_net_handover.py",
    "ghc_family_radio_interference_accessibility.py",
    "ghc_family_radio_privacy_remedy.py",
    "ghc_family_gmut_radio_observation_firewall.py",
    "ghc_family_thos_freed_radio_profile.py",
    "ghc_family_v655_v6_suite.py",
]


CLEAN_SURFACES = [
    "station, callsign, operator-role, equipment, and revision vocabulary",
    "licence-source, certificate, privilege, and operational-authority separation",
    "band, mode, bandwidth, power, unit, and tune-or-transmit refusal",
    "represented antenna, RF exposure, SWR, power, and measurement boundaries",
    "synthetic contact, emergency-message, readback, and correction lineage",
    "net check-in, interference referral, workload, pause, and handover states",
    "call-sign, location, message-content, retention, complaint, and remedy privacy",
    "manifest coverage, Git-blob identity, deterministic JSON, and timestamp typing",
    "failure retention, Method Flow recurrence, rollback, and nonpromotion guards",
    "spectrum, emergency, land, affected-party, legal, cultural, and Māori-authority refusal",
]


def _negative(
    number: int,
    signature: str,
    failed: str,
    recovery: str,
    recurrence_guard: str,
) -> dict:
    return {
        "negative_id": f"V6556-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": recurrence_guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "broad_archive_discovery_timed_out",
        "The first broad D-drive discovery exceeded its bounded wrapper and returned no complete source location evidence.",
        "Use the exact continuity path supplied by the activation and verify it with one scalar filesystem probe.",
        "Do not recursively enumerate the archive bank when an immutable exact path is already supplied.",
    ),
    _negative(
        2,
        "bundled_exact_path_test_timed_out",
        "The first exact-path PowerShell Test-Path bundle exceeded its bound and returned no existence credit.",
        "Use direct .NET Directory.Exists or File.Exists calls for each literal target.",
        "Keep archive-backed existence checks scalar and literal.",
    ),
    _negative(
        3,
        "combined_source_git_live_audit_timed_out",
        "A combined local Git, tracking, and fresh-live audit timed out before yielding a complete source receipt.",
        "Run branch, head, history, upstream, tracking, divergence, cleanliness, and live remote as separate scalar probes.",
        "Keep archive-backed Git lifecycle checks scalar.",
    ),
    _negative(
        4,
        "bundled_status_tracking_probe_timed_out",
        "A second bundled status and tracking probe also timed out without complete evidence.",
        "Run status alone with a longer bound and keep each remaining Git state check separate.",
        "Do not recombine status and tracking checks after a bundled-probe timeout.",
    ),
    _negative(
        5,
        "powershell_foreach_output_piped_without_materialization",
        "A required-file sizing command piped directly from a compound PowerShell foreach form and failed with an empty-pipe parser error.",
        "Materialize loop output into an array before formatting or serialization.",
        "Never attach a pipeline directly to a compound foreach statement.",
    ),
    _negative(
        6,
        "over_narrow_skill_dependency_path_filter_returned_zero",
        "The first dependency-path filter returned no matches because its separator-sensitive expression was narrower than the actual file list.",
        "Widen only the filename-stem expression while preserving the three explicitly required skill names.",
        "Use file-stem matching for cross-platform path discovery and never broaden the authority scope.",
    ),
    _negative(
        7,
        "novelty_probe_generator_expression_syntax_error",
        "The first all-row novelty probe omitted required generator parentheses when max also received a key argument, so no score was produced.",
        "Parenthesize the generator and rerun the unchanged read-only 2,080-row comparison.",
        "Syntax-check compact generator expressions before using keyword arguments in the same call.",
    ),
    _negative(
        8,
        "worktree_add_wrapper_timed_out_while_checkout_continued",
        "The single authorized worktree-add command exceeded its wrapper while the original Git checkout subprocess continued in the background.",
        "Do not retry; audit exact processes, registration, path, branch, head, and status, then accept the completed original operation only if all anchors match.",
        "After an ambiguous worktree timeout, reconcile process and Git state before any second mutation.",
    ),
    _negative(
        9,
        "windows_literal_glob_rejected_by_ripgrep",
        "A ripgrep source-inspection command passed a Windows wildcard as a literal path and was rejected before reading any phase data.",
        "Run ripgrep from the repository root and apply the wildcard through its supported -g filter.",
        "Use -g for filename selection; do not embed Windows wildcards in a literal ripgrep path.",
    ),
    _negative(
        10,
        "combined_status_and_stale_term_scan_timed_out",
        "A combined untracked-status and stale-term scan exceeded its wrapper before returning either complete result.",
        "Split status from content inspection and use direct bounded line reads for named owner files.",
        "Do not combine archive-backed Git status with multi-file content scanning.",
    ),
]
