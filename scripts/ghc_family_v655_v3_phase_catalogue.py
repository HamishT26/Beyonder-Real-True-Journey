#!/usr/bin/env python3
"""Ilyra Fen v655-v3 source, proposal, portfolio, and startup catalogue."""

from __future__ import annotations


OFFICIAL_SOURCES = [
    {
        "source_id": "ISO-21987-2017",
        "title": "ISO 21987:2017 — Ophthalmic optics — Mounted spectacle lenses",
        "publisher": "International Organization for Standardization",
        "url": "https://www.iso.org/standard/65161.html",
        "status": "watch",
        "use": (
            "mounted-spectacle-lens order, requirement, and test-method scope; "
            "watch because a replacement is under development"
        ),
    },
    {
        "source_id": "NZ-GAZETTE-ODOB-2024",
        "title": (
            "Scopes of Practice and Prescribed Qualifications for Optometrists "
            "and Dispensing Opticians 2024"
        ),
        "publisher": "New Zealand Gazette",
        "url": "https://gazette.govt.nz/notice/id/2024-sl4611",
        "status": "current",
        "use": (
            "professional-scope and qualification boundary; the phase performs "
            "no optical dispensing or health-practitioner work"
        ),
    },
    {
        "source_id": "NZ-HPCA-2003",
        "title": "Health Practitioners Competence Assurance Act 2003",
        "publisher": "New Zealand Legislation",
        "url": "https://www.legislation.govt.nz/act/public/2003/48/en/latest/",
        "status": "current",
        "use": "scope-of-practice, registration, and competence reservation",
    },
    {
        "source_id": "NZ-OPC-HIPC-2026",
        "title": "Health Information Privacy Code 2020 in force 1 May 2026",
        "publisher": "Office of the Privacy Commissioner New Zealand",
        "url": (
            "https://www.privacy.org.nz/privacy-principles/codes-of-practice/"
            "hipc2020/"
        ),
        "status": "current",
        "use": (
            "health-information collection, purpose, security, access, "
            "correction, retention, and disclosure reservations"
        ),
    },
    {
        "source_id": "NZ-HDC-CODE",
        "title": "Code of Health and Disability Services Consumers' Rights",
        "publisher": "Health and Disability Commissioner New Zealand",
        "url": (
            "https://www.hdc.org.nz/your-rights/about-the-code/"
            "code-of-health-and-disability-services-consumers-rights/"
        ),
        "status": "current",
        "use": (
            "communication, informed choice, dignity, complaint, and remedy "
            "reservations without legal adjudication"
        ),
    },
    {
        "source_id": "W3C-VC-DM-20",
        "title": "Verifiable Credentials Data Model v2.0",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/vc-data-model/",
        "status": "stable",
        "use": (
            "synthetic issuer, subject, status, evidence, privacy, and "
            "nonproduction credential vocabulary"
        ),
    },
    {
        "source_id": "W3C-WCAG-22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "stable",
        "use": (
            "accessible static-report structure with manual and affected-user "
            "evaluation reserved"
        ),
    },
    {
        "source_id": "W3C-PROV-O",
        "title": "PROV-O: The PROV Ontology",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "stable",
        "use": "entity, activity, agent, revision, derivation, and custody vocabulary",
    },
    {
        "source_id": "NIST-SP811",
        "title": "NIST SP 811 — Guide for the Use of the International System of Units",
        "publisher": "National Institute of Standards and Technology",
        "url": "https://www.nist.gov/publications/guide-use-international-system-units-si",
        "status": "current",
        "use": (
            "unit declaration and conversion discipline; not instrument "
            "calibration or optical measurement evidence"
        ),
    },
    {
        "source_id": "RFC-8785",
        "title": "RFC 8785 — JSON Canonicalization Scheme",
        "publisher": "RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "stable",
        "use": "deterministic synthetic job-record canonicalization vocabulary",
    },
    {
        "source_id": "RFC-9530",
        "title": "RFC 9530 — Digest Fields",
        "publisher": "RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc9530.html",
        "status": "stable",
        "use": (
            "content versus representation digest distinctions and integrity "
            "failure vocabulary"
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


PROPOSAL_ROWS = [
    (
        1,
        "Spectacle-lens laboratory job-intake envelope with presented order, "
        "requesting-party placeholder, job purpose, frame and lens scope, privacy "
        "minimum, custody boundary, and no-work-start rule",
        "optical-job-intake-boundary",
        "Freed ID and CBR Heart",
        "completed",
        "spectacle-lens job intake, purpose, and custody boundary",
        ["ISO-21987-2017", "NZ-OPC-HIPC-2026", "W3C-PROV-O"],
    ),
    (
        2,
        "Optical prescription-transcription provenance record with source type, "
        "field-by-field lexical value, sign, unit, eye side, author placeholder, "
        "revision, ambiguity, and interpretation refusal",
        "prescription-transcription-provenance",
        "Freed ID and CBR Heart",
        "completed",
        "prescription transcription provenance and ambiguity refusal",
        ["ISO-21987-2017", "NIST-SP811", "NZ-OPC-HIPC-2026"],
    ),
    (
        3,
        "Optical job-revision graph with original order, authorized-change "
        "placeholder, changed field, reason, timestamp, supersession, stale-copy "
        "quarantine, and silent-overwrite refusal",
        "optical-job-revision-graph",
        "Freed ID and CBR Heart",
        "completed",
        "optical job revision and stale-copy quarantine",
        ["W3C-PROV-O", "NZ-OPC-HIPC-2026", "RFC-8785"],
    ),
    (
        4,
        "Lens-blank lot and coating provenance ledger with supplier reference, "
        "material class, refractive-index declaration, treatment, diameter, lot, "
        "expiry placeholder, substitution, and release hold",
        "lens-blank-lot-provenance",
        "THOS Body",
        "completed",
        "lens blank lot, coating, and substitution provenance",
        ["ISO-21987-2017", "W3C-PROV-O"],
    ),
    (
        5,
        "Frame-order identifier crosswalk with frame model, eye size, bridge, "
        "temple, tracing revision, presented identifier, collision, component "
        "mismatch, and identity-conflation refusal",
        "frame-order-identifier-crosswalk",
        "Freed ID and CBR Heart",
        "completed",
        "frame, order, tracing, and component identifier separation",
        ["ISO-21987-2017", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        6,
        "Pupillary-distance and fitting-height measurement proxy with binocular "
        "and monocular distinction, eye side, reference posture, instrument "
        "placeholder, unit, uncertainty, recheck, and real-measurement refusal",
        "pd-height-measurement-proxy",
        "THOS Body",
        "represented",
        "pupillary-distance and fitting-height measurement proxy",
        ["ISO-21987-2017", "NIST-SP811", "NZ-GAZETTE-ODOB-2024"],
    ),
    (
        7,
        "Focimeter verification proxy with instrument identifier placeholder, "
        "calibration status, reference lens, sphere, cylinder, axis, addition, "
        "prism, repeatability, and measured-result refusal",
        "focimeter-verification-proxy",
        "THOS Body",
        "represented",
        "focimeter status and mounted-lens verification proxy",
        ["ISO-21987-2017", "NIST-SP811", "NZ-GAZETTE-ODOB-2024"],
    ),
    (
        8,
        "Lens blocking and edging proxy with tracing digest, block centre, axis "
        "mark, bevel mode, minimum-edge placeholder, machine state, dry-run, "
        "abort, and physical-machining refusal",
        "lens-edging-proxy",
        "THOS Body",
        "represented",
        "lens blocking, tracing, edging, and abort proxy",
        ["ISO-21987-2017", "W3C-PROV-O"],
    ),
    (
        9,
        "Mounted-lens alignment and stress proxy with optical-centre relation, "
        "axis orientation, seating state, frame strain placeholder, cosmetic "
        "observation, rework route, and fit-quality refusal",
        "mounted-lens-alignment-proxy",
        "THOS Body",
        "represented",
        "mounted-lens alignment, seating, and stress proxy",
        ["ISO-21987-2017", "NZ-GAZETTE-ODOB-2024"],
    ),
    (
        10,
        "THOS optical-job handover packet with order revision, component lineage, "
        "inspection placeholders, unresolved deviation, usage-warning placeholder, "
        "plain-language readback, correction route, and no-dispensing claim",
        "thos-optical-job-handover",
        "THOS Body",
        "completed",
        "optical job evidence handover and readback structure",
        ["ISO-21987-2017", "NZ-HDC-CODE", "W3C-PROV-O"],
    ),
    (
        11,
        "Lens material, frame, coating, tint, drill, groove, and mounting-method "
        "compatibility matrix with evidence source, unknown state, conflict, "
        "substitution, escalation, and suitability refusal",
        "lens-frame-compatibility-matrix",
        "THOS Body",
        "completed",
        "lens frame coating and mounting compatibility firewall",
        ["ISO-21987-2017", "W3C-PROV-O"],
    ),
    (
        12,
        "Progressive-lens layout lineage with design identifier placeholder, "
        "fitting cross, reference points, corridor class, inset placeholder, "
        "engraving observation, revision, and design-performance refusal",
        "progressive-layout-lineage",
        "THOS Body",
        "completed",
        "progressive lens layout and reference-point lineage",
        ["ISO-21987-2017", "W3C-PROV-O"],
    ),
    (
        13,
        "Optical-centre, prism, decentration, base-direction, sign, and unit "
        "contract with source quantity, conversion step, tolerance-source "
        "placeholder, uncertainty, and pass-fail refusal",
        "optical-centre-prism-units",
        "GMUT Mind",
        "completed",
        "optical centre prism decentration and unit obligations",
        ["ISO-21987-2017", "NIST-SP811"],
    ),
    (
        14,
        "Tint and transmission batch ledger with recipe revision, material, "
        "coating compatibility, bath placeholder, time, temperature, reference "
        "sample, observation, and spectral-performance refusal",
        "tint-transmission-batch-ledger",
        "THOS Body",
        "completed",
        "tint transmission batch lineage and performance firewall",
        ["ISO-21987-2017", "W3C-PROV-O", "NIST-SP811"],
    ),
    (
        15,
        "Optical supplier substitution docket with ordered component, offered "
        "component, equivalence claim placeholder, material, coating, geometry, "
        "cost disclosure hold, authorization gap, and auto-substitution refusal",
        "optical-substitution-docket",
        "Freed ID and CBR Heart",
        "completed",
        "optical supplier substitution and authorization boundary",
        ["ISO-21987-2017", "NZ-HDC-CODE", "W3C-PROV-O"],
    ),
    (
        16,
        "Optical remake and correction lineage with reported issue placeholder, "
        "original job, inspection evidence gap, root-cause hypothesis, corrective "
        "change, supersession, remedy hold, and blame refusal",
        "optical-remake-correction-lineage",
        "Freed ID and CBR Heart",
        "completed",
        "optical remake correction provenance and remedy hold",
        ["NZ-HDC-CODE", "NZ-OPC-HIPC-2026", "W3C-PROV-O"],
    ),
    (
        17,
        "Returned-lens quarantine record with job link, reason placeholder, "
        "personal-data minimum, component state, contamination cue, evidence "
        "preservation, disposal hold, and reuse refusal",
        "returned-lens-quarantine",
        "Freed ID and CBR Heart",
        "completed",
        "returned optical component quarantine and privacy boundary",
        ["NZ-OPC-HIPC-2026", "W3C-PROV-O"],
    ),
    (
        18,
        "Optical laboratory queue and workload governor with revision age, "
        "component dependency, represented hazard, work-in-progress ceiling, "
        "fatigue placeholder, pause, owner handover, and auto-release refusal",
        "optical-queue-workload-governor",
        "THOS Body",
        "completed",
        "optical job queue workload and release governor",
        ["NZ-GAZETTE-ODOB-2024", "W3C-PROV-O"],
    ),
    (
        19,
        "Optical health-information minimization envelope with field purpose, "
        "sensitivity class, role placeholder, disclosure route, access and "
        "correction state, retention basis gap, and privacy-complete refusal",
        "optical-health-privacy-envelope",
        "Freed ID and CBR Heart",
        "completed",
        "optical health-information purpose and minimization boundary",
        ["NZ-OPC-HIPC-2026", "NZ-HDC-CODE"],
    ),
    (
        20,
        "Canonical optical job-record tribunal with deterministic JSON property "
        "order, Unicode preservation, duplicate-key rejection, signed-value "
        "placeholder, revision digest, and cryptographic-proof refusal",
        "optical-job-canonical-json",
        "Freed ID and CBR Heart",
        "completed",
        "deterministic optical job JSON and duplicate-key refusal",
        ["RFC-8785", "RFC-9530", "NZ-OPC-HIPC-2026"],
    ),
    (
        21,
        "Optical artifact content-versus-representation digest docket with "
        "algorithm, byte domain, media type, transformation, mismatch, unsupported "
        "algorithm, and integrity-complete refusal",
        "optical-artifact-digest-docket",
        "THOS Body",
        "completed",
        "optical artifact digest domain and mismatch refusal",
        ["RFC-9530", "RFC-8785"],
    ),
    (
        22,
        "GMUT paraxial ABCD-ray matrix board with height-angle state, translation "
        "and refraction matrices, determinant obligation, composition order, unit "
        "domain, approximation scope, and observation firewall",
        "gmut-paraxial-abcd-board",
        "GMUT Mind",
        "completed",
        "paraxial ABCD ray-transfer matrix obligation board",
        ["NIST-SP811", "ISO-21987-2017"],
    ),
    (
        23,
        "GMUT lensmaker relation board with curvature sign, refractive-index "
        "reference, thickness, surrounding medium, thin-lens limit, unit, "
        "singularity guard, and physical-prediction firewall",
        "gmut-lensmaker-relation",
        "GMUT Mind",
        "completed",
        "lensmaker relation sign unit and approximation firewall",
        ["NIST-SP811", "ISO-21987-2017"],
    ),
    (
        24,
        "GMUT chromatic-dispersion typed board with wavelength, material-index "
        "function, Abbe-number placeholder, reference lines, unit, interpolation "
        "domain, uncertainty, and empirical-performance firewall",
        "gmut-chromatic-dispersion-board",
        "GMUT Mind",
        "completed",
        "chromatic dispersion type domain and empirical firewall",
        ["NIST-SP811", "ISO-21987-2017"],
    ),
    (
        25,
        "Freed ID synthetic optical-job status credential profile with issuer and "
        "subject placeholders, job pseudonym, status, evidence digest, validity, "
        "purpose, correlation warning, revocation gap, and nonproduction refusal",
        "freed-id-optical-job-status",
        "Freed ID and CBR Heart",
        "represented",
        "synthetic verifiable optical job status credential profile",
        ["W3C-VC-DM-20", "NZ-OPC-HIPC-2026", "RFC-9530"],
    ),
    (
        26,
        "CBR optical-job decision and remedy provenance ledger with information "
        "request, alternative, affordability impact placeholder, disability "
        "access, correction, complaint route, reviewer gap, and no-rights "
        "adjudication rule",
        "cbr-optical-remedy-provenance",
        "Freed ID and CBR Heart",
        "completed",
        "optical decision correction complaint and remedy provenance",
        ["NZ-HDC-CODE", "NZ-OPC-HIPC-2026", "W3C-PROV-O"],
    ),
    (
        27,
        "Accessible optical-job status and measurement explainer with semantic "
        "table, units in headers, plain-language stage, noncolour hold state, "
        "error association, reflow, print fallback, and manual-evaluation reserve",
        "accessible-optical-job-report",
        "THOS Body",
        "completed",
        "accessible optical job status and measurement structure",
        ["W3C-WCAG-22", "NZ-HDC-CODE"],
    ),
    (
        28,
        "Stage 20 optical-quality evidence nonpromotion board with denominator, "
        "instrument status, tolerance source, remake selection, missingness, "
        "subgroup, uncertainty, independent-review gap, and terminal abstention",
        "stage20-optical-quality-nonpromotion",
        "GMUT Mind",
        "completed",
        "optical quality evidence denominator and nonpromotion board",
        ["ISO-21987-2017", "NZ-GAZETTE-ODOB-2024"],
    ),
    (
        29,
        "Real optical laboratory validation adapter with practitioner and site "
        "authorization, real orders, calibrated instruments, standards access, "
        "privacy review, affected-user evaluation, independent review, and "
        "zero-row zero-action firewall",
        "real-optical-lab-adapter",
        "THOS Body",
        "open_gap",
        "real optical laboratory evidence readiness",
        [
            "ISO-21987-2017",
            "NZ-GAZETTE-ODOB-2024",
            "NZ-HPCA-2003",
            "NZ-OPC-HIPC-2026",
        ],
    ),
    (
        30,
        "Optical access, informed choice, disability accommodation, health "
        "privacy, affordability, complaint, remedy, language, affected-party, "
        "legal, cultural, data-governance, tangata-whenua, iwi, hapū, and Māori-"
        "authority reservation",
        "optical-rights-authority-reservation",
        "Freed ID and CBR Heart",
        "exact_gate",
        "optical health rights affected-party and Māori-authority reservation",
        ["NZ-HDC-CODE", "NZ-OPC-HIPC-2026", "TMR-PRINCIPLES", "NZ-HPCA-2003"],
    ),
]


SKILL_IDEAS = [
    "ghc-family-optical-job-intake-boundary",
    "ghc-family-prescription-transcription-provenance",
    "ghc-family-lens-lot-traceability",
    "ghc-family-optical-measurement-proxy",
    "ghc-family-lens-compatibility-firewall",
    "ghc-family-optical-remake-correction",
    "ghc-family-optical-job-privacy",
    "ghc-family-optical-job-accessibility",
    "ghc-family-optical-identifier-profile",
    "ghc-family-optical-evidence-firewall",
]


RUNNER_IDEAS = [
    "ghc_family_optical_job_intake_boundary.py",
    "ghc_family_prescription_transcription_provenance.py",
    "ghc_family_lens_lot_traceability.py",
    "ghc_family_optical_measurement_proxy.py",
    "ghc_family_lens_compatibility_firewall.py",
    "ghc_family_optical_remake_correction.py",
    "ghc_family_optical_job_privacy.py",
    "ghc_family_optical_job_accessibility.py",
    "ghc_family_optical_identifier_profile.py",
    "ghc_family_v655_v3_suite.py",
]


CLEAN_SURFACES = [
    "optical order and revision vocabulary",
    "unit sign and eye-side declarations",
    "lens frame and coating provenance",
    "represented instrument-state boundaries",
    "health-information minimization",
    "remake correction and remedy lineage",
    "manifest coverage and Git-blob identity",
    "failure retention and recurrence guards",
    "source status and replacement watch",
    "legal cultural and Māori-authority refusal",
]


def _negative(
    number: int,
    signature: str,
    failed: str,
    recovery: str,
    recurrence_guard: str,
) -> dict:
    return {
        "negative_id": f"V6553-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": recurrence_guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "oversized_activation_baton_display_truncated",
        "The first whole-baton display exceeded the tool output envelope and did not prove an EOF read.",
        "Read the exact immutable Git blob in bounded line ranges through the final line.",
        "Use bounded immutable-blob ranges for long activation files.",
    ),
    _negative(
        2,
        "combined_auth_roster_display_truncated",
        "The first combined permission, roster, and schema display truncated before every selected file reached EOF.",
        "Reread each required file separately with bounded exact UTF-8 reads.",
        "Do not combine multiple long policy files into one evidence display.",
    ),
    _negative(
        3,
        "auth_state_tail_display_compacted",
        "The first large tail read of the authorization state was interrupted by context compaction and earned no EOF credit.",
        "Reread the remaining state in two explicit bounded ranges.",
        "Split long JSON state tails before context or output limits are approached.",
    ),
    _negative(
        4,
        "auth_state_get_content_probe_timeout",
        "A bounded Get-Content authorization-state probe timed out without returning data.",
        "Use System.IO.File.ReadAllLines for the exact known file and bounded range.",
        "Prefer direct .NET reads for archive-backed or security-scanned policy files.",
    ),
    _negative(
        5,
        "auth_state_second_get_content_probe_timeout",
        "A second independent Get-Content authorization-state range timed out without returning data.",
        "Use the same direct .NET exact-path method and retain this distinct timeout.",
        "Do not repeat a timed-out file cmdlet when the direct .NET method is available.",
    ),
    _negative(
        6,
        "auth_schema_get_content_probe_timeout",
        "The Get-Content authorization-schema probe timed out without returning schema evidence.",
        "Read the exact schema through System.IO.File.ReadAllText.",
        "Use one direct exact-path read for small required schemas.",
    ),
    _negative(
        7,
        "windows_rg_wildcard_path_rejected",
        "A read-only rg command passed Windows wildcard paths as literal path arguments and returned no complete inspection.",
        "Use rg directory roots with a -g filename glob.",
        "Use ripgrep glob options rather than shell-style wildcard path arguments on Windows.",
    ),
    _negative(
        8,
        "inherited_json_stale_field_projection",
        "A read-only inherited-count projection used stale JSON property names and returned null diagnostic values.",
        "Enumerate actual top-level properties before projecting scalar counts.",
        "Inspect current receipt schemas rather than assuming fields from an earlier phase.",
    ),
    _negative(
        9,
        "second_windows_rg_wildcard_path_rejected",
        "A second read-only dependency scan repeated the Windows wildcard path error and produced no dependency evidence.",
        "Run the corrected directory-root and -g query and retain the recurrence separately.",
        "Apply the Windows rg glob guard to every phase-specific search.",
    ),
    _negative(
        10,
        "catalogue_match_count_wildcard_error",
        "A practice-specific match-count audit included an invalid wildcard test path and returned only partial script evidence.",
        "Rerun bounded searches against directory roots with explicit -g filters.",
        "Never credit partial multi-path search output when any requested path failed.",
    ),
    _negative(
        11,
        "workflow_validator_obsolete_request_option",
        "An extra workflow validation command used an obsolete --request option and failed before changing any file.",
        "Inspect the valid phase-local receipt already emitted by the x1 builder and use the current positional-input CLI only for a future changed request.",
        "Read the current workflow runner help before constructing an independent validation command.",
    ),
    _negative(
        12,
        "x1_privacy_receipt_stale_file_count_projection",
        "A read-only privacy summary requested file_count instead of the receipt's current scanned_file_count property and returned a null diagnostic.",
        "Enumerate exact top-level receipt properties and project scanned_file_count.",
        "Bind every scalar summary to the current receipt schema rather than a remembered alias.",
    ),
]
