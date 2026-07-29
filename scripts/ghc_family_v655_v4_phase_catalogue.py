#!/usr/bin/env python3
"""Auren Lark v655-v4 source, proposal, portfolio, and startup catalogue."""

from __future__ import annotations


OFFICIAL_SOURCES = [
    {
        "source_id": "CITES-SC78-DOC56",
        "title": (
            "CITES SC78 Doc. 56 — Simplified procedures for permits and "
            "certificates"
        ),
        "publisher": "CITES Secretariat",
        "url": (
            "https://cites.org/sites/default/files/documents/SC/78/agenda/"
            "E-SC78-56.pdf"
        ),
        "status": "watch",
        "use": (
            "musical-instrument material and cross-border certificate context; "
            "watch because Party implementation and simplified procedures evolve"
        ),
    },
    {
        "source_id": "WORKSAFE-WOOD-DUST",
        "title": "Wood dust: controlling the risks",
        "publisher": "WorkSafe New Zealand",
        "url": (
            "https://www.worksafe.govt.nz/topic-and-industry/dust/"
            "wood-dust-controlling-the-risks/"
        ),
        "status": "current",
        "use": (
            "wood-dust hazard and control context; no real cutting, routing, "
            "turning, sanding, exposure monitoring, or health work"
        ),
    },
    {
        "source_id": "WORKSAFE-ORGANIC-SOLVENTS",
        "title": "Organic solvents",
        "publisher": "WorkSafe New Zealand",
        "url": (
            "https://www.worksafe.govt.nz/topic-and-industry/"
            "hazardous-substances/guidance/substances/organic-solvents/"
        ),
        "status": "current",
        "use": (
            "adhesive, lacquer, cleaning, resin, and solvent hazard context; "
            "no substance handling or safety determination"
        ),
    },
    {
        "source_id": "NZ-HSWA-2015",
        "title": "Health and Safety at Work Act 2015",
        "publisher": "New Zealand Legislation",
        "url": "https://www.legislation.govt.nz/act/public/2015/70/en/latest/",
        "status": "watch",
        "use": (
            "workplace duty, risk, training, and unsafe-work reservation; watch "
            "because a 2026 amendment has a future commencement"
        ),
    },
    {
        "source_id": "NZ-CGA-1993",
        "title": "Consumer Guarantees Act 1993",
        "publisher": "New Zealand Legislation",
        "url": "https://www.legislation.govt.nz/act/public/1993/0091/latest/",
        "status": "current",
        "use": (
            "repair service, care and skill, time, price, correction, and remedy "
            "context without legal interpretation or rights adjudication"
        ),
    },
    {
        "source_id": "NZ-OPC-PRIVACY-2020",
        "title": "Privacy Act 2020 information privacy principles",
        "publisher": "Office of the Privacy Commissioner New Zealand",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "current",
        "use": (
            "purpose, minimization, collection, storage, access, correction, "
            "retention, use, disclosure, and identifier reservations"
        ),
    },
    {
        "source_id": "W3C-VC-DM-20",
        "title": "Verifiable Credentials Data Model v2.0",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/vc-data-model/",
        "status": "stable",
        "use": (
            "synthetic repair-status issuer, subject, evidence, privacy, and "
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
            "calibration, acoustic evidence, or measurement authority"
        ),
    },
    {
        "source_id": "RFC-8785",
        "title": "RFC 8785 — JSON Canonicalization Scheme",
        "publisher": "RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "stable",
        "use": "deterministic synthetic repair-record canonicalization vocabulary",
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
        "Stringed-instrument repair intake passport with presented-owner claim "
        "placeholder, instrument class, requested work, visible condition, loose "
        "parts, privacy minimum, custody boundary, and no-work-start rule",
        "instrument-repair-intake-boundary",
        "CBR Heart and Freed ID",
        "completed",
        "instrument repair intake, presented ownership, scope, and custody boundary",
        ["CITES-SC78-DOC56", "NZ-OPC-PRIVACY-2020", "W3C-PROV-O"],
    ),
    (
        2,
        "Instrument condition and prior-intervention provenance map with region, "
        "material claim placeholder, crack or deformation signal, prior repair, "
        "image-reference placeholder, uncertainty, and diagnosis refusal",
        "instrument-condition-provenance",
        "Freed ID and THOS Body",
        "completed",
        "instrument condition, prior intervention, uncertainty, and diagnosis refusal",
        ["CITES-SC78-DOC56", "W3C-PROV-O", "NZ-OPC-PRIVACY-2020"],
    ),
    (
        3,
        "Repair authorization-delta ledger with baseline scope, consent-token "
        "placeholder, dependency impact, quoted ceiling, expiry, rollback anchor, "
        "unsigned-delta quarantine, and default-deny application",
        "repair-work-order-revision-graph",
        "Freed ID and CBR Heart",
        "completed",
        "repair authorization delta, expiry, rollback, and unsigned-change refusal",
        ["W3C-PROV-O", "NZ-CGA-1993", "RFC-8785"],
    ),
    (
        4,
        "Tonewood, veneer, binding, finish, and adhesive provenance ledger with "
        "species claim placeholder, supplier reference, stock or batch, CITES "
        "status gap, substitution, uncertainty, and release hold",
        "instrument-material-provenance",
        "THOS Body and Freed ID",
        "completed",
        "instrument material, finish, adhesive, and substitution provenance",
        ["CITES-SC78-DOC56", "WORKSAFE-WOOD-DUST", "W3C-PROV-O"],
    ),
    (
        5,
        "Instrument, case, neck, bridge, tailpiece, pickup, machine-head, and "
        "repair-job identifier crosswalk with namespace source, collision, "
        "component mismatch, revision, and identity-conflation refusal",
        "instrument-component-identifier-crosswalk",
        "Freed ID",
        "completed",
        "instrument, component, case, and repair-job identifier separation",
        ["CITES-SC78-DOC56", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        6,
        "Neck-relief, action, nut-slot, and saddle-height measurement proxy with "
        "string position, reference state, tool placeholder, unit, uncertainty, "
        "repeat cue, and real-measurement refusal",
        "instrument-setup-measurement-proxy",
        "THOS Body",
        "represented",
        "instrument setup geometry and measurement proxy",
        ["NIST-SP811", "NZ-HSWA-2015"],
    ),
    (
        7,
        "String-gauge, scale-length, pitch, break-angle, and tension proxy with "
        "declared equation, unit domain, material placeholder, tuning state, "
        "uncertainty, stop threshold, and real-load refusal",
        "string-tension-setup-proxy",
        "THOS Body and GMUT Mind",
        "represented",
        "string setup, pitch, geometry, and tension proxy",
        ["NIST-SP811", "NZ-HSWA-2015"],
    ),
    (
        8,
        "Fret-level, crown, dress, and replacement proxy with fret position, "
        "reference plane placeholder, tooling state, material-removal ceiling, "
        "dust cue, abort, and physical-operation refusal",
        "fret-work-proxy",
        "THOS Body",
        "represented",
        "fret-work geometry, tooling, removal ceiling, and abort proxy",
        ["WORKSAFE-WOOD-DUST", "NZ-HSWA-2015", "NIST-SP811"],
    ),
    (
        9,
        "Glue-joint, cleat, clamp, caul, heat, humidity, and cure proxy with "
        "adhesive batch placeholder, surface state, pressure placeholder, "
        "ventilation gap, release condition, abort, and real-repair refusal",
        "adhesive-clamping-repair-proxy",
        "THOS Body",
        "represented",
        "adhesive, clamping, cure, ventilation, and repair-operation proxy",
        ["WORKSAFE-ORGANIC-SOLVENTS", "NZ-HSWA-2015", "W3C-PROV-O"],
    ),
    (
        10,
        "THOS reversible-care transfer map with intervention sequence, undo "
        "boundary, material wait state, unresolved uncertainty, next-observation "
        "cue, handling restriction, receiver question log, correction callback, "
        "and performance-claim refusal",
        "thos-instrument-repair-handover",
        "THOS Body and CBR Heart",
        "completed",
        "reversible repair care transfer, wait-state, receiver question, and callback contract",
        ["W3C-PROV-O", "W3C-WCAG-22", "NZ-CGA-1993"],
    ),
    (
        11,
        "String, fret, nut, saddle, bridge, pickup, finish, adhesive, and timber "
        "compatibility matrix with evidence source, unknown state, conflict, "
        "substitution, escalation, and suitability refusal",
        "instrument-component-compatibility-matrix",
        "THOS Body",
        "completed",
        "instrument component, material, finish, and adhesive compatibility firewall",
        ["CITES-SC78-DOC56", "WORKSAFE-WOOD-DUST", "W3C-PROV-O"],
    ),
    (
        12,
        "Scale-length and fret-position lineage with nominal scale, compensation "
        "placeholder, fret index, coordinate origin, unit, rounding rule, "
        "revision, and intonation-performance refusal",
        "scale-fret-position-lineage",
        "GMUT Mind and THOS Body",
        "completed",
        "scale-length, fret-position, unit, rounding, and revision lineage",
        ["NIST-SP811", "W3C-PROV-O"],
    ),
    (
        13,
        "Neck angle, relief, action, radius, string spacing, and bridge geometry "
        "contract with reference plane, sign, unit, conversion, tolerance-source "
        "placeholder, uncertainty, and pass-fail refusal",
        "instrument-geometry-unit-contract",
        "GMUT Mind and THOS Body",
        "completed",
        "instrument geometry, sign, unit, reference, and uncertainty obligations",
        ["NIST-SP811", "RFC-8785"],
    ),
    (
        14,
        "Finish, solvent, cleaning-agent, resin, dye, and adhesive batch ledger "
        "with safety-data-source placeholder, container label, material relation, "
        "test coupon, ventilation state, waste route, and treatment refusal",
        "finish-solvent-adhesive-ledger",
        "THOS Body",
        "completed",
        "finish, solvent, adhesive, test-coupon, and hazardous-substance boundary",
        ["WORKSAFE-ORGANIC-SOLVENTS", "NZ-HSWA-2015", "W3C-PROV-O"],
    ),
    (
        15,
        "Alternative-component decision matrix with requested function, candidate "
        "part lineage, exclusion rules, reversible-trial state, material-document "
        "gap, price and time disclosure, explicit accept-or-reject placeholder, "
        "and default-deny outcome",
        "instrument-part-substitution-docket",
        "CBR Heart and THOS Body",
        "completed",
        "alternative component comparison, reversible trial, disclosure, and default denial",
        ["CITES-SC78-DOC56", "NZ-CGA-1993", "W3C-PROV-O"],
    ),
    (
        16,
        "Returned-service anomaly learning record with symptom placeholder, prior "
        "repair assumption, contradictory evidence, containment action, new-test "
        "need, remedial options, attribution uncertainty, and complaint handoff",
        "instrument-repair-correction-lineage",
        "CBR Heart and Freed ID",
        "completed",
        "returned-service anomaly, contradiction, containment, learning, and remedy routing",
        ["NZ-CGA-1993", "W3C-PROV-O", "NZ-OPC-PRIVACY-2020"],
    ),
    (
        17,
        "Removed-string, fret, nut, saddle, pickup, hardware, finish sample, and "
        "wood-fragment custody record with job link, component state, dust or "
        "solvent cue, evidence preservation, return choice placeholder, disposal "
        "hold, and reuse refusal",
        "removed-component-custody",
        "THOS Body and CBR Heart",
        "completed",
        "removed instrument component custody, evidence, return, and disposal boundary",
        ["WORKSAFE-ORGANIC-SOLVENTS", "W3C-PROV-O", "NZ-CGA-1993"],
    ),
    (
        18,
        "Bench-capacity reservation lattice with job hazard band, jig and tool "
        "contention, cure or settling interval, contamination separation, maximum "
        "concurrent operations, pause token, shift ownership, and "
        "automatic-dispatch prohibition",
        "instrument-workshop-queue-governor",
        "THOS Body",
        "completed",
        "bench capacity, resource contention, separation, pause, and dispatch prohibition",
        ["NZ-HSWA-2015", "WORKSAFE-WOOD-DUST", "W3C-WCAG-22"],
    ),
    (
        19,
        "Minimum-contact data map with repair-purpose link, ownership-evidence "
        "placeholder, communication channel, optional-field suppression, access-log "
        "reservation, correction workflow, deletion-decision gap, and "
        "privacy-completeness refusal",
        "instrument-job-privacy-envelope",
        "CBR Heart and Freed ID",
        "completed",
        "repair contact necessity, optional-field suppression, access, correction, and deletion boundary",
        ["NZ-OPC-PRIVACY-2020", "NZ-CGA-1993"],
    ),
    (
        20,
        "Repair-event state-machine serialization with allowed transition table, "
        "monotonic revision, duplicate-event identifier rejection, Unicode "
        "normalization declaration, numeric lexical domain, deterministic snapshot, "
        "and signature-proof refusal",
        "instrument-repair-canonical-json",
        "Freed ID",
        "completed",
        "repair event transition, monotonic revision, lexical, and deterministic snapshot contract",
        ["RFC-8785", "W3C-PROV-O"],
    ),
    (
        21,
        "Repair-media transformation provenance contract with original-byte "
        "identifier, derivative identifier, crop or redaction step, orientation, "
        "encoding, digest algorithm, mismatch quarantine, and proof refusal",
        "instrument-repair-digest-docket",
        "Freed ID",
        "completed",
        "repair media derivation, transformation, digest, and mismatch quarantine",
        ["RFC-9530", "RFC-8785"],
    ),
    (
        22,
        "GMUT ideal-string modal board with length, linear-density placeholder, "
        "tension symbol, boundary condition, mode index, frequency relation, unit "
        "domain, approximation scope, and observation firewall",
        "gmut-ideal-string-modal-board",
        "GMUT Mind",
        "completed",
        "ideal-string modal relation, unit, approximation, and observation firewall",
        ["NIST-SP811"],
    ),
    (
        23,
        "GMUT coupled string-bridge-soundboard graph with string state, bridge "
        "transfer edge, body-mode placeholder, damping symbol, coupling matrix, "
        "boundary condition, unit, and physical-prediction firewall",
        "gmut-string-body-coupling-board",
        "GMUT Mind",
        "completed",
        "coupled string, bridge, and soundboard relation with prediction firewall",
        ["NIST-SP811"],
    ),
    (
        24,
        "GMUT fret-temperament typed board with scale length, fret index, interval "
        "ratio, equal-temperament placeholder, compensation term, logarithm "
        "domain, unit, and empirical-intonation firewall",
        "gmut-fret-temperament-board",
        "GMUT Mind",
        "completed",
        "fret-temperament type domain, ratio, logarithm, and empirical firewall",
        ["NIST-SP811"],
    ),
    (
        25,
        "Freed ID synthetic component-custody claim set with pseudonymous repair "
        "object, role-scoped claim groups, selective-disclosure placeholder, "
        "holder-binding gap, expiry, status gap, unlinkability warning, and "
        "nonproduction refusal",
        "freed-id-instrument-repair-status",
        "Freed ID",
        "represented",
        "synthetic selective-disclosure component custody claim profile",
        ["W3C-VC-DM-20", "NZ-OPC-PRIVACY-2020", "W3C-PROV-O"],
    ),
    (
        26,
        "CBR instrument-repair decision and remedy provenance ledger with "
        "information request, alternative, price and timing effect placeholder, "
        "accessibility need, correction, complaint route, reviewer gap, and "
        "no-rights-adjudication rule",
        "cbr-instrument-repair-remedy",
        "CBR Heart",
        "completed",
        "instrument repair decision, correction, complaint, and remedy provenance",
        ["NZ-CGA-1993", "NZ-OPC-PRIVACY-2020", "W3C-WCAG-22"],
    ),
    (
        27,
        "Multi-format repair handover accessibility map with heading hierarchy, "
        "step-status text, tactile-diagram placeholder, keyboard path, focus order, "
        "warning redundancy, caption reserve, and affected-user testing gap",
        "accessible-instrument-repair-report",
        "CBR Heart",
        "completed",
        "multi-format repair handover structure, navigation, redundant warnings, and testing reserve",
        ["W3C-WCAG-22", "NIST-SP811", "NZ-CGA-1993"],
    ),
    (
        28,
        "Instrument setup and acoustics evidence-escalation stop card with "
        "observation provenance, sample-selection rule, calibration gap, absent "
        "blinded comparison, uncertainty model, external-review placeholder, "
        "claim ceiling, and promotion veto",
        "stage20-instrument-evidence-nonpromotion",
        "GMUT Mind and CBR Heart",
        "completed",
        "instrument setup and acoustics evidence escalation, claim ceiling, and promotion veto",
        ["NIST-SP811", "W3C-PROV-O"],
    ),
    (
        29,
        "Real luthiery workshop validation adapter with practitioner and site "
        "authorization, real instruments and materials, calibrated tools, safety "
        "review, owner consent, CITES assessment, affected-user evaluation, "
        "independent review, and zero-item zero-action firewall",
        "real-luthiery-validation-adapter",
        "THOS Body, Freed ID, and CBR Heart",
        "open_gap",
        "real luthiery workshop evidence readiness",
        [
            "WORKSAFE-WOOD-DUST",
            "WORKSAFE-ORGANIC-SOLVENTS",
            "NZ-HSWA-2015",
            "CITES-SC78-DOC56",
        ],
    ),
    (
        30,
        "Instrument ownership, repair choice, affordability, accessibility, "
        "privacy, complaint, remedy, language, taonga and culturally significant "
        "instrument status, knowledge, recording, material provenance, "
        "data-governance, tangata-whenua, iwi, hapū, and Māori-authority reservation",
        "instrument-rights-authority-reservation",
        "CBR Heart",
        "exact_gate",
        "instrument repair affected-party, taonga, cultural, and Māori-authority reservation",
        [
            "TMR-PRINCIPLES",
            "NZ-OPC-PRIVACY-2020",
            "NZ-CGA-1993",
            "CITES-SC78-DOC56",
        ],
    ),
]


SKILL_IDEAS = [
    "ghc-family-instrument-repair-intake-boundary",
    "ghc-family-instrument-material-provenance",
    "ghc-family-instrument-setup-proxy",
    "ghc-family-fret-tooling-boundary",
    "ghc-family-adhesive-finish-safety-boundary",
    "ghc-family-instrument-component-compatibility",
    "ghc-family-instrument-repair-correction",
    "ghc-family-instrument-job-privacy",
    "ghc-family-instrument-job-accessibility",
    "ghc-family-instrument-identifier-profile",
]


RUNNER_IDEAS = [
    "ghc_family_instrument_repair_intake_boundary.py",
    "ghc_family_instrument_material_provenance.py",
    "ghc_family_instrument_setup_proxy.py",
    "ghc_family_fret_tooling_boundary.py",
    "ghc_family_adhesive_finish_safety_boundary.py",
    "ghc_family_instrument_component_compatibility.py",
    "ghc_family_instrument_repair_correction.py",
    "ghc_family_instrument_job_privacy.py",
    "ghc_family_instrument_job_accessibility.py",
    "ghc_family_v655_v4_suite.py",
]


CLEAN_SURFACES = [
    "instrument job and revision vocabulary",
    "component material and CITES provenance",
    "geometry sign unit and reference declarations",
    "represented tool measurement and load boundaries",
    "wood dust solvent adhesive and finish safety reservations",
    "owner and repair-contact information minimization",
    "rework correction complaint and remedy lineage",
    "manifest coverage and Git-blob identity",
    "failure retention and recurrence guards",
    "legal cultural taonga and Māori-authority refusal",
]


def _negative(
    number: int,
    signature: str,
    failed: str,
    recovery: str,
    recurrence_guard: str,
) -> dict:
    return {
        "negative_id": f"V6554-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": recurrence_guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "activation_blob_display_exceeded_context",
        "The first exact activation-blob probe exceeded the display context and did not prove a complete read.",
        "Resolve the exact blob hash, measure it, and emit bounded numbered ranges through EOF.",
        "Measure long Git blobs before display and use bounded exact ranges.",
    ),
    _negative(
        2,
        "activation_measurement_wrapper_timeout",
        "The first bounded activation measurement exceeded its short wrapper without yielding a receipt.",
        "Use direct Git plumbing with a longer bounded timeout and scalar output.",
        "Allow archive-backed Git plumbing an evidence-proportionate bounded timeout.",
    ),
    _negative(
        3,
        "process_argument_list_api_unavailable",
        "The direct process reader assumed a ProcessStartInfo ArgumentList API absent from the installed runtime.",
        "Use the compatible Arguments property with the already-verified object hash.",
        "Inspect the runtime API surface before using newer process-construction members.",
    ),
    _negative(
        4,
        "memory_linked_solo_activation_skill_missing",
        "A memory-linked family solo-activation skill path no longer existed and could not govern the phase.",
        "Use the present family-current skills named by the fully read Index and activation baton.",
        "Treat memory tool pointers as historical until live filesystem verification passes.",
    ),
    _negative(
        5,
        "skill_discovery_regex_false_zero",
        "An overconstrained skill-path regular expression returned no match even though the required directories existed.",
        "Enumerate the narrow skill root by exact directory name and read the resolved files.",
        "Prefer exact skill directory probes over fragile separator-heavy path expressions.",
    ),
    _negative(
        6,
        "source_status_aggregate_timeout",
        "The first full source status probe exceeded sixty seconds and returned no cleanliness evidence.",
        "Split tracked, staged, and untracked source checks into scalar Git witnesses.",
        "Use separate cleanliness probes on archive-backed worktrees.",
    ),
    _negative(
        7,
        "ancestry_wrapper_powershell_parser_error",
        "A combined ancestry object embedded command-and-status syntax that PowerShell rejected before Git execution.",
        "Run the ancestry command first, store its exit status, then build the scalar object.",
        "Never embed semicolon-bearing command/status expressions inside a PowerShell hash value.",
    ),
    _negative(
        8,
        "guessed_terminal_receipt_directory_absent",
        "A guessed external terminal-receipt directory did not exist and provided no evidence.",
        "Use the live activation plus a bounded filename-only search; never invent a route path.",
        "Resolve external receipt locations before reading and keep missing guesses at zero credit.",
    ),
    _negative(
        9,
        "broad_validation_bank_hash_search_timeout",
        "A broad recursive hash search of the validation bank exceeded two minutes without results.",
        "Use the known source task event tail and exact committed receipts instead of repeating a broad search.",
        "Avoid recursive archive-wide searches when a bounded authoritative source is available.",
    ),
    _negative(
        10,
        "parallel_foreach_reader_parser_error",
        "Two parallel small-file readers omitted required PowerShell foreach spacing and both failed before reading.",
        "Use the explicit foreach ($item in $items) form and read each declared file once.",
        "Keep the validated explicit-space PowerShell loop form in generated wrappers.",
    ),
    _negative(
        11,
        "evidence_projection_extra_brace_parser_error",
        "A compact evidence-receipt projection contained an extra closing brace and returned no schema evidence.",
        "Project the required receipts independently with simpler scalar expressions.",
        "Prefer short one-purpose structured projections over nested one-line aggregations.",
    ),
    _negative(
        12,
        "frozen_chain_projection_invalid_cmdlet_token",
        "The first frozen-chain title projection used Select-Object-First as an invalid command token.",
        "Use Select-Object -First and separately project prior and new proposal arrays.",
        "Keep cmdlet parameters separated from command names in PowerShell.",
    ),
    _negative(
        13,
        "source_session_tail_projection_timeout",
        "A 600-line structured source-session tail projection exceeded two minutes.",
        "Search for narrow terminal vocabulary first and parse only the matched assistant events.",
        "Filter large event streams lexically before structured parsing.",
    ),
    _negative(
        14,
        "terminal_event_search_overconstrained_zero_result",
        "The first narrowed terminal-event expression was too restrictive and returned no closeout text.",
        "Search a small set of exact terminal phrases and parse the resulting assistant events.",
        "Validate event-line shape before combining multiple structural regex assumptions.",
    ),
    _negative(
        15,
        "worktree_add_wrapper_timeout_during_initialization",
        "The one authorized worktree-add wrapper timed out while Git continued initializing the correct lane.",
        "Audit path, registration, branch, head, processes, and lock state; wait for the one checkout to settle without retry.",
        "Never replay an ambiguous worktree mutation; reconcile its exact state first.",
    ),
    _negative(
        16,
        "worktree_audit_spacing_expression_errors",
        "The first worktree audit used invalid joined command tokens in two scalar expressions.",
        "Use explicit spaces in Join-Path and Select-Object parameter forms, then inspect the existing lane only.",
        "Use validated literal scalar syntax for post-timeout mutation audits.",
    ),
    _negative(
        17,
        "new_lane_tracked_cleanliness_timeout",
        "The first tracked cleanliness scan of the newly materialized archive-backed lane exceeded sixty seconds.",
        "Run one longer unified porcelain status after checkout processes have fully settled.",
        "Allow first-touch filesystem scanning to settle before exact cleanliness validation.",
    ),
    _negative(
        18,
        "new_lane_untracked_enumeration_timeout",
        "The first untracked enumeration of the new lane exceeded two minutes and returned no receipt.",
        "Use the same longer unified porcelain status and require an empty result before writing x1.",
        "Do not run parallel first-touch index and untracked scans on a freshly populated archive lane.",
    ),
    _negative(
        19,
        "phase_data_reader_spacing_error",
        "The first exact phase-data reader joined Resolve-Path and its argument into an invalid command token.",
        "Use the explicit Resolve-Path argument form and read the file through EOF once.",
        "Keep PowerShell cmdlet names and arguments separated in bounded readers.",
    ),
    _negative(
        20,
        "test_reader_spacing_error_recurrence",
        "A later bounded test-file reader repeated the joined Resolve-Path token and emitted only null-array diagnostics.",
        "Use the already validated explicit Resolve-Path argument form and avoid further diagnostic replay.",
        "Apply the cmdlet-spacing guard to every bounded reader, not only the first recovered file.",
    ),
    _negative(
        21,
        "first_full_chain_novelty_audit_rejected_template_overlap",
        "The first 2,020-row novelty audit rejected ten luthiery titles whose semantic skeleton still mirrored Ilyra surfaces.",
        "Redesign the mechanisms, not merely their domain nouns, then rerun only the frozen novelty audit.",
        "Compare both title tokens and mechanism shape against the full inherited chain before freezing x1.",
    ),
    _negative(
        22,
        "x1_receipt_projection_foreach_parser_recurrence",
        "A parallel x1 receipt-summary wrapper repeated the compact foreach spacing defect after the focused tests passed.",
        "Retain the failure, rebuild the deterministic ledger, and project receipts with explicit loop and path syntax.",
        "Ban compressed foreach and Resolve-Path tokens from receipt-summary wrappers.",
    ),
    _negative(
        23,
        "receipt_join_path_token_recurrence_three",
        "Three receipt projections joined Join-Path with its arguments, emitted non-terminating errors, and produced null summaries.",
        "Use direct literal receipt paths for all remaining scalar reads and reject null projections.",
        "Do not construct known receipt paths dynamically in compact PowerShell wrappers.",
    ),
    _negative(
        24,
        "x1_stale_term_windows_wildcard_path_rejected",
        "The first x1 stale-term audit passed wildcard script and test paths directly to ripgrep and returned only partial evidence.",
        "Search the script, test, and phase directory roots with explicit ripgrep -g filters and exclusions.",
        "Never use wildcard characters in positional Windows path arguments for ripgrep.",
    ),
    _negative(
        25,
        "focused_x1_pytest_dependency_absent",
        "The first focused x1 test launch selected pytest, but the active Python environment had no pytest module and ran zero tests.",
        "Invoke the dependency-free unittest file directly with the same bytecode and UTF-8 guards.",
        "Inspect the test harness entrypoint before selecting an optional test runner.",
    ),
    _negative(
        26,
        "focused_x1_unittest_stale_expected_counts",
        "The first dependency-free focused run executed all eleven tests but two assertions still expected twenty-four current-phase witnesses.",
        "Update every explicit current-phase and cumulative count assertion for the retained N25 witness, then rebuild before rerunning.",
        "Search the whole focused test for every phase-local count whenever a retained negative changes the ledger.",
    ),
    _negative(
        27,
        "x1_receipt_summary_guessed_paths_returned_null",
        "A parallel receipt summary guessed two nonexistent JSON paths, emitted non-terminating errors, and serialized null counts.",
        "Discover the committed-intent paths from the generated manifest and read only those literal files with terminating errors.",
        "Treat any null receipt projection as failure and never infer generated filenames from directory semantics.",
    ),
    _negative(
        28,
        "combined_x1_index_cleanliness_probe_timeout",
        "The combined staged-whitespace, unstaged-tracked, and untracked audit exceeded its short wrapper without a complete receipt.",
        "Run the three read-only index and worktree checks separately with archive-aware bounded timeouts.",
        "Do not combine multiple first-pass archive-backed Git scans under one short timeout.",
    ),
]
