#!/usr/bin/env python3
"""Tamar Vey v656-v1 source, proposal, portfolio, and startup catalogue."""

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
        "ILFORD-BW-FIRST-FILM",
        "Processing Your First Black and White Film",
        "HARMAN technology / ILFORD PHOTO",
        "https://www.ilfordphoto.com/wp/wp-content/uploads/2017/04/Processing-your-first-black-and-white-film.pdf",
        "current",
        (
            "manufacturer-primary sequence, temperature, timing, agitation, fixing, "
            "washing, and drying vocabulary only; no chemical, darkroom, archival, "
            "safety, quality, or professional determination"
        ),
    ),
    _source(
        "KODAK-BW-PROCESSING",
        "Processing KODAK PROFESSIONAL Black-and-White Films",
        "Kodak Alaris / KODAK PROFESSIONAL",
        "https://www.kodakprofessional.com/sites/default/files/wysiwyg/pro/resources/edbwf_0.pdf",
        "current",
        (
            "manufacturer-primary processing, solution, time, temperature, capacity, "
            "and washing context only; no product endorsement or real processing claim"
        ),
    ),
    _source(
        "NZ-WORKSAFE-HAZSUB-PRACTICAL",
        "Your practical guide to working safely with hazardous substances",
        "WorkSafe New Zealand",
        "https://www.worksafe.govt.nz/topic-and-industry/hazardous-substances/guidance/your-practical-guide/",
        "current",
        (
            "inventory, safety-data-sheet, storage, incompatibility, exposure, spill, "
            "and emergency reservation only; no workplace, chemical, or safety decision"
        ),
    ),
    _source(
        "NZ-HSWA-HAZSUB-2017",
        "Health and Safety at Work (Hazardous Substances) Regulations 2017",
        "New Zealand Legislation",
        "https://www.legislation.govt.nz/regulation/public/2017/0131/latest/",
        "watch",
        (
            "current legal and competent-person reservation only; no legal "
            "interpretation, compliance decision, certification, or authorization"
        ),
    ),
    _source(
        "LOC-PHOTO-CARE",
        "Care, Handling and Storage of Photographs",
        "Library of Congress",
        "https://www.loc.gov/preservation/care/photo.html",
        "current",
        (
            "photograph and negative enclosure, temperature, humidity, handling, "
            "storage, and deterioration context only; no conservation treatment claim"
        ),
    ),
    _source(
        "W3C-PROV-O",
        "PROV-O: The PROV Ontology",
        "W3C",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        (
            "entity, activity, agent, revision, derivation, custody, correction, "
            "chemical-batch, exposure, processing, print, and archive lineage"
        ),
    ),
    _source(
        "RFC-3339",
        "RFC 3339: Date and Time on the Internet: Timestamps",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic UTC lexical timestamps, intervals, handovers, and corrections",
    ),
    _source(
        "RFC-8785",
        "RFC 8785: JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic contract, receipt, credential, and manifest serialization",
    ),
    _source(
        "NIST-SP811",
        "NIST SP 811: Guide for the Use of the International System of Units",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/publications/guide-use-international-system-units-si",
        "current",
        (
            "unit, quantity, symbol, conversion, temperature, time, concentration, "
            "distance, and optical-domain discipline; not real metrology or calibration"
        ),
    ),
    _source(
        "W3C-WCAG-22",
        "Web Content Accessibility Guidelines 2.2",
        "W3C",
        "https://www.w3.org/TR/WCAG22/",
        "stable",
        (
            "accessible report and workflow structure with manual, assistive-technology, "
            "cognitive, low-vision, Māori-language, and affected-user evaluation reserved"
        ),
    ),
    _source(
        "W3C-VC-DM-20",
        "Verifiable Credentials Data Model v2.0",
        "W3C",
        "https://www.w3.org/TR/vc-data-model-2.0/",
        "stable",
        (
            "synthetic film-processing evidence and print-access credential vocabulary; "
            "no real issuer, holder, verifier, key, proof, status, or trust claim"
        ),
    ),
    _source(
        "W3C-VC-DM-21",
        "Verifiable Credentials Data Model v2.1",
        "W3C",
        "https://www.w3.org/TR/vc-data-model-2.1/",
        "draft",
        (
            "draft-change watch only; it cannot override the v2.0 Recommendation or "
            "support standards-conformance, interoperability, or production claims"
        ),
    ),
    _source(
        "W3C-DID-10",
        "Decentralized Identifiers (DIDs) v1.0",
        "W3C",
        "https://www.w3.org/TR/did-core/",
        "stable",
        (
            "synthetic identifier and controller vocabulary only; no live method, "
            "resolver, key, controller, service, or trust-governance event"
        ),
    ),
    _source(
        "W3C-DATA-INTEGRITY-10",
        "Verifiable Credential Data Integrity 1.0",
        "W3C",
        "https://www.w3.org/TR/vc-data-integrity/",
        "stable",
        (
            "proof-configuration and verification vocabulary only; no real "
            "cryptographic key, proof, assurance, or independent security review"
        ),
    ),
    _source(
        "W3C-BITSTRING-STATUS-10",
        "Bitstring Status List v1.0",
        "W3C",
        "https://www.w3.org/TR/vc-bitstring-status-list/",
        "stable",
        (
            "synthetic credential-status vocabulary only; no live issuance, status, "
            "revocation, privacy review, wallet, verifier, or interoperability event"
        ),
    ),
    _source(
        "NZ-PRIVACY-PRINCIPLES",
        "Privacy Act 2020 information privacy principles",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        (
            "purpose, source, notice, fair collection, security, access, correction, "
            "accuracy, retention, use, disclosure, and identifier reservations; no legal advice"
        ),
    ),
    _source(
        "NZ-PRIVACY-ACT-2020",
        "Privacy Act 2020",
        "New Zealand Legislation",
        "https://www.legislation.govt.nz/act/public/2020/31/en/latest/",
        "watch",
        (
            "current legislation watch, including later amendments, without legal "
            "interpretation, compliance determination, or photographic-subject decision"
        ),
    ),
    _source(
        "TMR-PRINCIPLES",
        "Principles of Māori Data Sovereignty",
        "Te Mana Raraunga",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "current",
        (
            "Māori rights, interests, governance, jurisdiction, language, images, "
            "collective benefit, and authority reservation only"
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
        "Photographic film-roll intake and custody passport with synthetic roll token, format, emulsion placeholder, frame estimate, receipt condition, owner handover, and no-real-film claim",
        "film-roll-intake-passport",
        "Freed ID and CBR Heart",
        "completed",
        "film-roll token, format, emulsion placeholder, frame estimate, receipt condition, custody handover, and real-film refusal",
        ["W3C-PROV-O", "RFC-8785", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        2,
        "Cassette, canister, spool, and batch inventory envelope with synthetic identifiers, duplicate quarantine, seal state, expiry placeholder, storage cue, and no-material assertion",
        "film-container-inventory",
        "Freed ID and THOS Body",
        "completed",
        "cassette, canister, spool, batch, duplicate, seal, expiry, storage, and material refusal",
        ["ILFORD-BW-FIRST-FILM", "KODAK-BW-PROCESSING", "W3C-PROV-O"],
    ),
    (
        3,
        "Light-tight loading and dark-bag custody board with opening sequence, tool count, transfer state, exposure-risk quarantine, readback, and no-physical-handling claim",
        "light-tight-loading-custody",
        "THOS Body",
        "completed",
        "light-tight loading, dark-bag sequence, tool count, transfer, exposure-risk quarantine, readback, and physical-handling refusal",
        ["ILFORD-BW-FIRST-FILM", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        4,
        "Developer stock and working-solution ledger with product placeholder, dilution ratio, water-volume unit, mixed-at token, age, reuse policy, and no-chemistry action",
        "developer-solution-ledger",
        "THOS Body and GMUT Mind",
        "completed",
        "developer stock, working solution, dilution, water volume, mix time, age, reuse policy, and chemistry-action refusal",
        ["KODAK-BW-PROCESSING", "NIST-SP811", "NZ-WORKSAFE-HAZSUB-PRACTICAL"],
    ),
    (
        5,
        "Developer, stop, fixer, and rinse sequence tribunal with ordered stages, minimum transition, incompatible reversal, omission quarantine, and no-processing execution",
        "chemical-sequence-tribunal",
        "THOS Body",
        "completed",
        "developer, stop, fixer, rinse, ordered stage, transition, reversal, omission quarantine, and processing-execution refusal",
        ["ILFORD-BW-FIRST-FILM", "KODAK-BW-PROCESSING", "RFC-8785"],
    ),
    (
        6,
        "Temperature, immersion-time, inversion, agitation, and drain schedule with typed units, tolerance, clock-source placeholder, deviation hold, and zero real bath",
        "processing-schedule-board",
        "GMUT Mind and THOS Body",
        "completed",
        "temperature, immersion time, inversion, agitation, drain, typed unit, tolerance, deviation hold, and real-bath refusal",
        ["ILFORD-BW-FIRST-FILM", "KODAK-BW-PROCESSING", "NIST-SP811"],
    ),
    (
        7,
        "Chemical capacity, replenishment, carry-over, exhaustion, and reuse-budget board with batch counter, threshold source, uncertainty, release hold, and no-potency claim",
        "chemical-capacity-board",
        "THOS Body and GMUT Mind",
        "completed",
        "chemical capacity, replenishment, carry-over, exhaustion, reuse budget, threshold, uncertainty, hold, and potency refusal",
        ["KODAK-BW-PROCESSING", "NIST-SP811", "W3C-PROV-O"],
    ),
    (
        8,
        "Darkroom vessel, lid, label, funnel, measure, and cross-contamination ledger with dedicated-use cue, rinse state, conflict quarantine, and no-safety determination",
        "vessel-contamination-ledger",
        "THOS Body and CBR Heart",
        "completed",
        "vessel, lid, label, funnel, measure, dedicated use, rinse, cross-contamination quarantine, and safety-decision refusal",
        ["NZ-WORKSAFE-HAZSUB-PRACTICAL", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        9,
        "Darkroom light-leak and safelight configuration envelope with source placeholder, distance, duration, material class, test reservation, fault hold, and zero optical measurement",
        "safelight-configuration-envelope",
        "THOS Body and GMUT Mind",
        "completed",
        "light leak, safelight source, distance, duration, material class, test reservation, fault hold, and optical-measurement refusal",
        ["ILFORD-BW-FIRST-FILM", "NIST-SP811", "W3C-PROV-O"],
    ),
    (
        10,
        "Enlarger setup and negative-carrier ledger with head placeholder, lens token, focal-length unit, filter, aperture, alignment hold, and no-equipment command",
        "enlarger-setup-ledger",
        "GMUT Mind and THOS Body",
        "completed",
        "enlarger head, negative carrier, lens, focal length, filter, aperture, alignment hold, and equipment-command refusal",
        ["NIST-SP811", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        11,
        "Test-strip, base exposure, aperture, filter grade, dodge, burn, and revision plan with dependency lineage, supersession, rollback, and no-print-quality claim",
        "print-exposure-plan",
        "GMUT Mind and CBR Heart",
        "completed",
        "test strip, base exposure, aperture, filter grade, dodge, burn, revision, supersession, rollback, and print-quality refusal",
        ["W3C-PROV-O", "RFC-3339", "NIST-SP811"],
    ),
    (
        12,
        "Contact-sheet frame-selection provenance board with synthetic frame token, inclusion reason, uncertainty, crop reservation, correction, disclosure hold, and no-aesthetic judgment",
        "contact-sheet-selection-board",
        "CBR Heart and Freed ID",
        "completed",
        "contact sheet, frame token, inclusion reason, uncertainty, crop reservation, correction, disclosure hold, and aesthetic-judgment refusal",
        ["W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES", "W3C-WCAG-22"],
    ),
    (
        13,
        "GMUT photographic characteristic-curve obligation board with log exposure, density proxy, toe, straight-line region, shoulder, gradient, domain, unit, and observation firewall",
        "gmut-characteristic-curve-board",
        "GMUT Mind",
        "completed",
        "typed log exposure, density proxy, toe, straight-line region, shoulder, gradient, domain, unit, and observation firewall",
        ["NIST-SP811", "KODAK-BW-PROCESSING"],
    ),
    (
        14,
        "GMUT enlarger diffraction and modulation-transfer obligation board with wavelength placeholder, aperture, spatial frequency, sampling domain, covariance hold, and real-optics firewall",
        "gmut-optical-transfer-board",
        "GMUT Mind",
        "completed",
        "typed wavelength, aperture, diffraction, spatial frequency, modulation transfer, sampling, covariance, and real-optics firewall",
        ["NIST-SP811", "W3C-PROV-O"],
    ),
    (
        15,
        "GMUT developer reaction-diffusion proxy with concentration field, diffusion coefficient, boundary condition, rate placeholder, temperature coupling, identifiability hold, and zero empirical fit",
        "gmut-reaction-diffusion-proxy",
        "GMUT Mind",
        "represented",
        "typed concentration field, diffusion coefficient, boundary condition, rate, temperature coupling, identifiability, and empirical-fit refusal",
        ["NIST-SP811", "KODAK-BW-PROCESSING"],
    ),
    (
        16,
        "Wash, hypo-clear, residual-fixer, water-exchange, duration, and permanence hold docket with method source, uncertainty, retest reservation, and no-archival assurance",
        "wash-permanence-hold",
        "THOS Body and CBR Heart",
        "completed",
        "wash, hypo clear, residual fixer, water exchange, duration, method source, uncertainty, retest, and archival-assurance refusal",
        ["ILFORD-BW-FIRST-FILM", "KODAK-BW-PROCESSING", "LOC-PHOTO-CARE"],
    ),
    (
        17,
        "Drying, dust, water-mark, scratch, curl, cut, and handling ledger with condition code, quarantine, correction, ownership handover, and no-conservation claim",
        "film-drying-condition-ledger",
        "THOS Body and CBR Heart",
        "completed",
        "drying, dust, water mark, scratch, curl, cut, handling, condition, quarantine, correction, handover, and conservation refusal",
        ["ILFORD-BW-FIRST-FILM", "LOC-PHOTO-CARE", "W3C-PROV-O"],
    ),
    (
        18,
        "Negative sleeve, print enclosure, sequence, material placeholder, label, derivative link, duplicate quarantine, and storage-release refusal envelope",
        "photo-enclosure-lineage",
        "Freed ID and CBR Heart",
        "completed",
        "negative sleeve, print enclosure, sequence, material, label, derivative, duplicate quarantine, and storage-release refusal",
        ["LOC-PHOTO-CARE", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        19,
        "Photographic archive condition and environment change log with coarse zone, temperature and humidity placeholders, observation source, drift, review hold, and no-preservation guarantee",
        "photo-archive-condition-log",
        "CBR Heart and GMUT Mind",
        "completed",
        "archive condition, coarse zone, temperature, humidity, observation source, drift, review hold, and preservation-guarantee refusal",
        ["LOC-PHOTO-CARE", "NIST-SP811", "W3C-PROV-O"],
    ),
    (
        20,
        "Accessible darkroom job-state, chemical-stage, error-summary, noncolour warning, focus-order, keyboard, print-order, and manual-user-review audit",
        "accessible-darkroom-status-audit",
        "CBR Heart and THOS Body",
        "completed",
        "job state, chemical stage, error summary, noncolour warning, focus order, keyboard, print order, and manual-user-review reservation",
        ["W3C-WCAG-22", "NZ-WORKSAFE-HAZSUB-PRACTICAL"],
    ),
    (
        21,
        "Darkroom spill, splash, vapour cue, unexpected reaction, pause, exposure-report hold, correction, evidence preservation, and no-emergency determination docket",
        "darkroom-incident-docket",
        "CBR Heart and THOS Body",
        "completed",
        "spill, splash, vapour cue, unexpected reaction, pause, exposure-report hold, correction, evidence preservation, and emergency-decision refusal",
        ["NZ-WORKSAFE-HAZSUB-PRACTICAL", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        22,
        "Silver-bearing fixer, wash-water, container, quantity placeholder, recovery route, discharge hold, custody, competent-review gap, and no-disposal decision ledger",
        "silver-waste-custody-ledger",
        "CBR Heart and THOS Body",
        "completed",
        "silver-bearing fixer, wash water, container, quantity, recovery route, discharge hold, custody, competent review, and disposal-decision refusal",
        ["NZ-WORKSAFE-HAZSUB-PRACTICAL", "NZ-HSWA-HAZSUB-2017", "W3C-PROV-O"],
    ),
    (
        23,
        "Darkroom unfinished-batch relay invariant with active-step pin, earliest-safe-pause clock, custody acknowledgement, unresolved-risk escrow, paired-state reconciliation, and resume prohibition",
        "darkroom-unfinished-batch-relay",
        "THOS Body and CBR Heart",
        "completed",
        "active-step pin, earliest-safe-pause clock, custody acknowledgement, unresolved-risk escrow, paired-state reconciliation, pause budget, and resume prohibition",
        ["NZ-WORKSAFE-HAZSUB-PRACTICAL", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        24,
        "THOS darkroom process-recovery study design with sealed comparison lanes, matched action budget, ordering-error endpoint, fatigue and harm stops, synthetic case registration, and no participants",
        "thos-darkroom-study-protocol",
        "THOS Body",
        "represented",
        "darkroom process-recovery comparison, sealed lanes, matched action budget, ordering-error endpoint, fatigue, harm stop, and participant refusal",
        ["NZ-WORKSAFE-HAZSUB-PRACTICAL", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        25,
        "THOS photographic chemical-mismatch triage proxy with vessel token, expected stage, observed label, confidence, quarantine, escalation, readback, handover, and no-safety decision",
        "thos-chemical-triage-proxy",
        "THOS Body",
        "represented",
        "synthetic chemical mismatch, vessel, expected stage, observed label, confidence, quarantine, escalation, readback, handover, and safety-decision refusal",
        ["NZ-WORKSAFE-HAZSUB-PRACTICAL", "ILFORD-BW-FIRST-FILM", "W3C-PROV-O"],
    ),
    (
        26,
        "Freed ID synthetic film-processing evidence credential with roll referent, recipe revision, batch digest, time-temperature envelope, custody chain, validity interval, issuer placeholder, and proof refusal",
        "freed-id-film-process-credential",
        "Freed ID",
        "represented",
        "synthetic film-processing evidence, roll referent, recipe revision, batch digest, time-temperature envelope, custody, validity, issuer, and proof refusal",
        ["W3C-VC-DM-20", "W3C-DATA-INTEGRITY-10", "W3C-DID-10"],
    ),
    (
        27,
        "Freed ID synthetic print-access capability with unlinkable subject placeholder, derivative allowlist, purpose ceiling, expiry, audience class, non-correlation budget, status gap, and unresolved revocation",
        "freed-id-print-capability",
        "Freed ID and CBR Heart",
        "represented",
        "synthetic print-access capability, unlinkable subject, derivative allowlist, purpose ceiling, expiry, audience, correlation, status, revocation, and nonproduction refusal",
        ["W3C-VC-DM-20", "W3C-BITSTRING-STATUS-10", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        28,
        "Photographic subject, bystander, location, content, frame-note, derivative, retention, access, correction, disclosure, complaint, and data-minimization envelope with privacy-complete refusal",
        "photo-privacy-envelope",
        "CBR Heart and Freed ID",
        "completed",
        "photographic subject, bystander, location, content, frame note, derivative, retention, access, correction, disclosure, complaint, minimization, and privacy-complete refusal",
        ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "W3C-WCAG-22"],
    ),
    (
        29,
        "Real film sensitometry, chemical-bath, operator-workload, accessibility, subject-privacy, and print-evaluation adapter with zero people, zero film, zero chemical, zero query, zero measurement, and zero rows",
        "darkroom-study-zero-row-adapter",
        "GMUT Mind and THOS Body",
        "open_gap",
        "real film sensitometry, chemical bath, operator workload, accessibility, subject privacy, print evaluation, authorization, and zero-row refusal",
        ["KODAK-BW-PROCESSING", "NZ-WORKSAFE-HAZSUB-PRACTICAL", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        30,
        "CBR photographic subject, whānau, place, event, taonga image, tikanga, disability, privacy, access, return, remedy, legal, cultural, data-governance, affected-party, and Māori-authority matrix",
        "cbr-photo-authority-matrix",
        "Freed ID and CBR Heart",
        "exact_gate",
        "photographic subject, whānau, place, event, taonga image, tikanga, disability, privacy, access, return, remedy, legal, cultural, governance, affected-party, and Māori-authority reservation",
        [
            "NZ-PRIVACY-PRINCIPLES",
            "W3C-WCAG-22",
            "TMR-PRINCIPLES",
            "LOCAL-CONTEXTS-TK-BC",
        ],
    ),
]


SKILL_IDEAS = [
    "ghc-family-darkroom-film-custody-boundary",
    "ghc-family-darkroom-chemical-sequence-integrity",
    "ghc-family-darkroom-capacity-waste-reserve",
    "ghc-family-darkroom-optical-exposure-proxy",
    "ghc-family-darkroom-wash-archive-handover",
    "ghc-family-darkroom-accessibility-incident-boundary",
    "ghc-family-photo-privacy-authority-reserve",
    "ghc-family-gmut-photochemical-field-firewall",
    "ghc-family-thos-freed-darkroom-profile",
    "ghc-family-darkroom-evidence-nonpromotion",
]


RUNNER_IDEAS = [
    "ghc_family_darkroom_film_custody_boundary.py",
    "ghc_family_darkroom_chemical_sequence_integrity.py",
    "ghc_family_darkroom_capacity_waste_reserve.py",
    "ghc_family_darkroom_optical_exposure_proxy.py",
    "ghc_family_darkroom_wash_archive_handover.py",
    "ghc_family_darkroom_accessibility_incident_boundary.py",
    "ghc_family_photo_privacy_authority_reserve.py",
    "ghc_family_gmut_photochemical_field_firewall.py",
    "ghc_family_thos_freed_darkroom_profile.py",
    "ghc_family_v656_v1_suite.py",
]


CLEAN_SURFACES = [
    "film roll, cassette, spool, frame, emulsion placeholder, custody, and condition vocabulary",
    "developer, stop, fixer, rinse, dilution, capacity, sequence, and cross-contamination refusal",
    "temperature, time, agitation, drain, wash, residual-fixer, uncertainty, and typed units",
    "light-tight loading, safelight, enlarger, lens, aperture, filter, exposure, and zero-device control",
    "contact sheet, test strip, dodge, burn, derivative, correction, and disclosure lineage",
    "drying, dust, scratch, cut, sleeve, enclosure, archive condition, and preservation holds",
    "spill, exposure cue, silver-bearing waste, recovery route, discharge, and competent-review reservation",
    "workload, unresolved roll, chemical hold, queue, rest, readback, and shift-handover state",
    "GMUT characteristic curve, optical transfer, reaction-diffusion, domain, unit, and observation firewall",
    "subject, whānau, taonga image, privacy, remedy, legal, cultural, and Māori-authority refusal",
]


def _negative(
    number: int,
    signature: str,
    failed: str,
    recovery: str,
    recurrence_guard: str,
) -> dict:
    return {
        "negative_id": f"V6561-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": recurrence_guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "memory_registry_search_timed_out",
        "The first bounded memory-registry search timed out without attributable current-phase evidence.",
        "Stop the memory lookup and use the live activation plus exact committed source.",
        "Do not broaden memory search after a bounded registry timeout.",
    ),
    _negative(
        2,
        "memory_tail_read_timed_out",
        "A bounded memory-tail read timed out before returning usable content.",
        "Treat the memory lookup as unavailable and continue from exact live repository evidence.",
        "Do not retry the same stalled file surface for phase authority.",
    ),
    _negative(
        3,
        "index_skill_get_content_timed_out",
        "The first installed index-skill read through the shell host timed out without complete content.",
        "Read the exact UTF-8 skill through a direct bounded file API.",
        "Use one direct UTF-8 read when the shell content provider stalls.",
    ),
    _negative(
        4,
        "dotnet_sha256_hashdata_unavailable",
        "The first optional skill-read digest helper called an unavailable runtime HashData API after the read attempt.",
        "Keep the complete text read and omit the nonessential digest helper.",
        "Do not assume modern static hashing APIs exist on the host runtime.",
    ),
    _negative(
        5,
        "dotnet_tohexstring_unavailable",
        "A second optional digest formatter called an unavailable runtime ToHexString API although the full skill text was returned.",
        "Credit only the complete text read and stop optional digest retries.",
        "Use no digest formatter when the read itself is the required evidence.",
    ),
    _negative(
        6,
        "startup_cwd_not_a_git_repository",
        "The first repository-location probe assumed the application workspace root was a Git checkout and returned no repository evidence.",
        "Locate the exact D-first owner worktrees by literal directory inspection.",
        "Resolve the intended worktree before invoking repository commands.",
    ),
    _negative(
        7,
        "combined_git_probe_powershell_parser_fault",
        "A combined read-only Git probe embedded native commands inside an invalid PowerShell expression and failed before Git ran.",
        "Run each native command and inspect its exit status as a separate scalar statement.",
        "Never place native Git invocations inside PowerShell parenthesized expression lists.",
    ),
    _negative(
        8,
        "combined_git_probe_timed_out",
        "The corrected combined source-state probe exceeded its bounded wrapper without a complete result.",
        "Split head, branch, equality, index, tracked, and untracked checks into separately attributable probes.",
        "Do not aggregate expensive archive-backed Git checks at a lifecycle boundary.",
    ),
    _negative(
        9,
        "first_source_tracked_probe_timed_out",
        "The first source tracked-tree plumbing probe exceeded its short bound and earned no clean-state credit.",
        "Run the same read-only plumbing check once with a dependency-justified larger bound.",
        "Size archive-backed tracked-tree probes independently from metadata checks.",
    ),
    _negative(
        10,
        "activation_blob_display_truncated",
        "The first full activation-blob display was truncated before the middle proposal inheritance was visible.",
        "Reread the exact Git blob in bounded line windows through EOF.",
        "Use bounded windows for long committed batons and verify the final line.",
    ),
    _negative(
        11,
        "activation_window_still_too_large",
        "The first 140-line activation window still exceeded the display budget by a small amount.",
        "Reduce the exact Git-blob windows to sixty lines and read every window through EOF.",
        "Use conservative windows when individual lines contain long gate lists.",
    ),
    _negative(
        12,
        "meta_tool_box_regex_lookup_missed_directory",
        "The first filename-regex lookup did not resolve the installed Meta Tool Box skill.",
        "List bounded installed skill directories and select the exact matching directory name.",
        "Prefer exact directory-name discovery when a filename regex returns no match.",
    ),
    _negative(
        13,
        "fast_forward_wrapper_timed_out_after_completion",
        "The safe fast-forward command exceeded its wrapper although the Git operation completed.",
        "Audit exact head, branch, worktree registration, process state, lock state, and split cleanliness before any later mutation.",
        "Never retry a timed-out Git mutation before proving its actual postcondition.",
    ),
    _negative(
        14,
        "broad_route_state_search_timed_out",
        "A broad read-only route-state search across repository documents exceeded its bound without usable output.",
        "Search only recent relevant phase builders and committed route artifacts.",
        "Keep route vocabulary searches phase-local and literal.",
    ),
    _negative(
        15,
        "narrow_route_search_named_missing_file",
        "The first narrowed route search referenced a nonexistent historical builder filename and returned no evidence.",
        "Enumerate the exact matching historical builder names before selecting a comparison surface.",
        "Do not infer historical filename conventions across generator generations.",
    ),
    _negative(
        16,
        "combined_builder_patch_unicode_context_mismatch",
        "The first combined builder patch used a Unicode-rendered context line that did not match and was rejected atomically before changing the file.",
        "Split the patch into exact ASCII-context hunks and inspect Unicode lines literally before editing them.",
        "Keep multi-hunk patches independent of terminal-rendered Unicode spellings.",
    ),
    _negative(
        17,
        "x1_builder_login_wrapper_output_truncated",
        "The first x1-builder wrapper returned an unusable over-budget output notice and left no phase packet or running Python process.",
        "Audit the expected receipt and process state, retain zero credit, and use one controlled non-login-shell retry.",
        "Do not infer builder completion from a truncated wrapper response.",
    ),
    _negative(
        18,
        "combined_builder_audit_wmi_probe_timed_out",
        "The first combined post-builder audit used a slow process-command-line query and timed out without a complete result.",
        "Split artifact and process checks and avoid the slow WMI surface.",
        "Use bounded literal artifact checks plus a simple process-name probe.",
    ),
    _negative(
        19,
        "builder_receipt_login_shell_probe_timed_out",
        "The first split receipt probe returned the absence result but its login-shell wrapper still timed out.",
        "Retain the returned absence evidence and move later diagnostics to a non-login shell.",
        "Use non-login shells for bounded D-drive lifecycle probes when the profile stalls.",
    ),
    _negative(
        20,
        "builder_process_login_shell_probe_timed_out",
        "The first simple Python-process probe through the login shell timed out without output.",
        "Repeat once through a non-login shell, which confirmed no Python process remained.",
        "Do not retry a mutation until a non-stalling process check confirms quiescence.",
    ),
    _negative(
        21,
        "first_novelty_gate_rejected_p23",
        "The first controlled x1 build rejected proposal P23 because its workload and handover wording overlapped Liora P20 above the frozen token threshold.",
        "Retain zero credit and recast P23 around an unfinished-batch relay invariant, safe-pause clock, risk escrow, and paired-state reconciliation.",
        "Require every proposal to pass the frozen-chain novelty gate before x1 freeze.",
    ),
    _negative(
        22,
        "workflow_plan_messaging_policy_rejected",
        "The next x1 build stopped because the no-downstream Codex route phrase was not one of the installed workflow validator's accepted structural values.",
        "Keep the no-authority fields explicit while encoding the route class as declared-endpoint-only after a terminal gate.",
        "Validate request vocabulary against the installed schema without converting absent authority into a send.",
    ),
    _negative(
        23,
        "isolated_workflow_validator_confirmed_policy_error",
        "The isolated workflow validator returned needs_refinement on the same messaging boundary and earned no validation credit.",
        "Use its single issue receipt to repair only the rejected request field.",
        "When an orchestration wrapper hides stderr, isolate only the failed validator and retain its failure.",
    ),
    _negative(
        24,
        "receipt_summary_assumed_wrong_novelty_path",
        "The first receipt summary guessed a provenance novelty filename that the builder does not emit at that path.",
        "Enumerate the phase filenames and inspect the exact generated novelty receipt.",
        "Resolve generated receipt names from the owner packet before reading them.",
    ),
    _negative(
        25,
        "broad_x1_git_status_probe_timed_out",
        "A broad recursive Git status summary exceeded its bound after the x1 packet was generated.",
        "Audit process and lock state, then split tracked changes from literal owner-file enumeration.",
        "Do not use broad untracked recursion as the first D-drive staged-boundary probe.",
    ),
    _negative(
        26,
        "receipt_summary_schema_assumption_misreported_collisions",
        "A read-only receipt summary queried absent convenience fields and counted a null collision property as one item although the exact collision receipt reports zero findings.",
        "Inspect the receipt's declared schema fields directly and retain the false summary with zero credit.",
        "Never count a nullable convenience property without first confirming the receipt schema.",
    ),
]
