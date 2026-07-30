#!/usr/bin/env python3
"""Elowen Cairn v656-v2 source, proposal, portfolio, and startup catalogue."""

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
        "WORLD-SAILING-ERS-2025-2028",
        "Equipment Rules of Sailing 2025-2028",
        "World Sailing",
        "https://www.sailing.org/inside-world-sailing/rules-regulations/equipment-rules-of-%20sailing",
        "current",
        (
            "current sailing-equipment definition, measurement, control, and inspection "
            "vocabulary only; no class compliance, inspection, certification, or real-sail claim"
        ),
    ),
    _source(
        "WORLD-SAILING-OSR-2026-2027",
        "Offshore Special Regulations 2026-2027",
        "World Sailing",
        "https://www.sailing.org/inside-world-sailing/rules-regulations/offshore-special-regulations/",
        "watch",
        (
            "current heavy-weather sail and responsibility context only; Version 2 is "
            "published for 1 January 2027, so no future rule is promoted into current use"
        ),
    ),
    _source(
        "ASTM-D5034-21R25",
        "D5034-21(2025) Standard Test Method for Breaking Strength and Elongation of Textile Fabrics",
        "ASTM International",
        "https://store.astm.org/standards/d5034",
        "current",
        (
            "textile specimen, breaking-force, elongation, method, unit, and laboratory-"
            "comparability vocabulary only; no test was performed and no material claim is made"
        ),
    ),
    _source(
        "NZ-WORKSAFE-MACHINERY-2026",
        "Safe use of machinery",
        "WorkSafe New Zealand",
        "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/",
        "current",
        (
            "June 2026 machinery-risk, guarding, training, and competent-person reservations "
            "only; no sewing-machine, cutting-tool, loft, workplace, or safety determination"
        ),
    ),
    _source(
        "NZ-WORKSAFE-LOCKOUT",
        "Keeping workers safe with machine lockouts",
        "WorkSafe New Zealand",
        "https://www.worksafe.govt.nz/topic-and-industry/machinery/keeping-workers-safe-with-machine-lockouts/",
        "current",
        (
            "isolation, lockout, tagout, restart, shift-change, training, and competent-person "
            "reservations only; no real lockout procedure or authorization"
        ),
    ),
    _source(
        "NIST-SP811",
        "NIST SP 811: Guide for the Use of the International System of Units",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/publications/guide-use-international-system-units-si",
        "stable",
        (
            "quantity, unit, symbol, conversion, length, area, force, stress, time, and "
            "angle discipline only; no real metrology, calibration, or material measurement"
        ),
    ),
    _source(
        "W3C-PROV-O",
        "PROV-O: The PROV Ontology",
        "W3C",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        "entity, activity, revision, derivation, custody, correction, and repair lineage",
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
        "W3C-WCAG-22",
        "Web Content Accessibility Guidelines 2.2",
        "W3C",
        "https://www.w3.org/TR/WCAG22/",
        "stable",
        (
            "structural accessibility vocabulary with manual, browser, assistive-technology, "
            "Māori-language, cognitive, low-vision, and affected-user evaluation reserved"
        ),
    ),
    _source(
        "NZ-PRIVACY-PRINCIPLES",
        "Privacy Act 2020 information privacy principles",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        (
            "purpose, source, direct and indirect notice, fair collection, security, access, "
            "correction, accuracy, retention, use, disclosure, and identifier reservations; "
            "no legal advice"
        ),
    ),
    _source(
        "W3C-VC-DM-20",
        "Verifiable Credentials Data Model v2.0",
        "W3C",
        "https://www.w3.org/TR/vc-data-model-2.0/",
        "stable",
        "synthetic evidence vocabulary only; no real issuer, holder, verifier, or trust claim",
    ),
    _source(
        "W3C-DID-10",
        "Decentralized Identifiers (DIDs) v1.0",
        "W3C",
        "https://www.w3.org/TR/did-core/",
        "stable",
        "synthetic identifier vocabulary only; no live resolver, key, controller, or service",
    ),
    _source(
        "W3C-DATA-INTEGRITY-10",
        "Verifiable Credential Data Integrity 1.0",
        "W3C",
        "https://www.w3.org/TR/vc-data-integrity/",
        "stable",
        "proof-configuration vocabulary only; no real key, proof, assurance, or security review",
    ),
    _source(
        "W3C-BITSTRING-STATUS-10",
        "Bitstring Status List v1.0",
        "W3C",
        "https://www.w3.org/TR/vc-bitstring-status-list/",
        "stable",
        "synthetic status vocabulary only; no live issuance, revocation, or interoperability",
    ),
    _source(
        "TMR-PRINCIPLES",
        "Principles of Māori Data Sovereignty",
        "Te Mana Raraunga",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "current",
        (
            "Māori rights, interests, governance, jurisdiction, language, collective benefit, "
            "and authority reservation only; never a substitute for Māori authority"
        ),
    ),
    _source(
        "LOCAL-CONTEXTS-TK-BC",
        "Traditional Knowledge and Biocultural Labels Usage and Style Guide",
        "Local Contexts",
        "https://localcontexts.org/wp-content/uploads/2023/08/TK-and-BC-Labels-Usage-and-Style-Guide.pdf",
        "current",
        (
            "community-originated notice and provenance reservation only; no label selection, "
            "community decision, cultural authorization, or Māori wording"
        ),
    ),
]


# number, title, slug, pillar, expected disposition, semantic mechanism, source ids
PROPOSAL_ROWS = [
    (
        1,
        "Sailmaking job-intake and scope passport with synthetic sail token, stated purpose, presented dimensions, condition note, custody handover, correction path, and no-real-sail claim",
        "sail-job-intake-passport",
        "Freed ID and CBR Heart",
        "completed",
        "job scope, synthetic sail token, presented dimension, condition, custody, correction, and real-sail refusal",
        ["W3C-PROV-O", "RFC-3339", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        2,
        "Sail coordinate-frame and measurement-basis contract with tack, clew, head, luff, leech, foot, datum, unit, uncertainty, revision, and no-inspection assertion",
        "sail-coordinate-frame",
        "GMUT Mind",
        "completed",
        "sail corner, edge, datum, unit, uncertainty, coordinate frame, revision, and inspection refusal",
        ["WORLD-SAILING-ERS-2025-2028", "NIST-SP811", "W3C-PROV-O"],
    ),
    (
        3,
        "Panel-topology adjacency map with seam graph, orientation edge, boundary class, overlap placeholder, orphan quarantine, reversible edit, and no-cutting command",
        "panel-topology-map",
        "GMUT Mind and THOS Body",
        "completed",
        "panel graph, seam adjacency, orientation, boundary, overlap, orphan quarantine, rollback, and cutting refusal",
        ["W3C-PROV-O", "RFC-8785", "NIST-SP811"],
    ),
    (
        4,
        "Sailcloth roll and lot provenance envelope with synthetic material class, weave direction, finish placeholder, roll width, defect cue, substitution hold, and no-property claim",
        "sailcloth-roll-provenance",
        "Freed ID and GMUT Mind",
        "completed",
        "cloth roll, lot, material class, weave direction, finish, width, defect, substitution, and material-property refusal",
        ["ASTM-D5034-21R25", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        5,
        "Warp, fill, bias, radial, crosscut, and load-path annotation tribunal with declared convention, conflict quarantine, confidence, correction, and zero-strength inference",
        "cloth-orientation-tribunal",
        "GMUT Mind",
        "completed",
        "warp, fill, bias, radial, crosscut, load-path annotation, conflict, confidence, and strength-inference refusal",
        ["ASTM-D5034-21R25", "NIST-SP811", "W3C-PROV-O"],
    ),
    (
        6,
        "Seam allowance, overlap, stitch-row, turnback, and edge-finish geometry board with typed length, tolerance placeholder, dependency, supersession, and no-machine instruction",
        "seam-geometry-board",
        "GMUT Mind and THOS Body",
        "completed",
        "seam allowance, overlap, stitch row, turnback, edge finish, length, tolerance, dependency, and machine-instruction refusal",
        ["NIST-SP811", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        7,
        "Corner reinforcement layer-stack contract with patch polygon, layer order, fibre orientation, boundary transition, duplicate quarantine, and no-load certification",
        "corner-layer-stack",
        "GMUT Mind",
        "completed",
        "corner patch, layer stack, polygon, fibre orientation, boundary transition, duplicate, and load-certification refusal",
        ["ASTM-D5034-21R25", "NIST-SP811", "W3C-PROV-O"],
    ),
    (
        8,
        "Reef, cringle, ring, webbing, and reinforcement interface ledger with synthetic hardware token, intended relation, backing zone, review hold, and no-installation action",
        "reef-hardware-interface",
        "THOS Body and GMUT Mind",
        "completed",
        "reef point, cringle, ring, webbing, reinforcement, interface, backing zone, hold, and installation refusal",
        ["WORLD-SAILING-OSR-2026-2027", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        9,
        "Batten-pocket and closure topology envelope with pocket axis, entry side, end stop, drainage cue, chafe note, conflict quarantine, and no-fit claim",
        "batten-pocket-topology",
        "GMUT Mind and THOS Body",
        "completed",
        "batten pocket, axis, entry, end stop, drainage, chafe, conflict, and fit refusal",
        ["WORLD-SAILING-ERS-2025-2028", "W3C-PROV-O", "NIST-SP811"],
    ),
    (
        10,
        "Luff, foot, and leech attachment route ledger with rope, tape, slide, slug, bolt-rope, track placeholder, discontinuity quarantine, and no-rig compatibility claim",
        "edge-attachment-route",
        "THOS Body and GMUT Mind",
        "completed",
        "luff, foot, leech, rope, tape, slide, slug, track, discontinuity, and rig-compatibility refusal",
        ["WORLD-SAILING-ERS-2025-2028", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        11,
        "Cut-plan nesting and remnant lineage board with cloth width, panel polygon, grain constraint, keep-out zone, waste proxy, revision, and no-cutter control",
        "cut-plan-nesting-board",
        "GMUT Mind and THOS Body",
        "completed",
        "cut plan, nesting, cloth width, panel polygon, grain constraint, keep-out, remnant, and cutter-control refusal",
        ["NIST-SP811", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        12,
        "Template, batten, spline, fairing, notch, and registration-mark version contract with dependency pin, correction note, supersession, rollback, and no-shape-quality claim",
        "template-version-contract",
        "GMUT Mind",
        "completed",
        "template, spline, fairing, notch, registration mark, dependency, supersession, rollback, and shape-quality refusal",
        ["NIST-SP811", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        13,
        "Thread, needle, tape, adhesive, webbing, and hardware bill with synthetic lot, compatibility placeholder, expiry cue, substitution hold, and no-material approval",
        "sail-material-bill",
        "THOS Body and Freed ID",
        "completed",
        "thread, needle, tape, adhesive, webbing, hardware, lot, compatibility, expiry, substitution, and material-approval refusal",
        ["ASTM-D5034-21R25", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        14,
        "Sewing, cutting, heating, pressing, and handling state board with equipment placeholder, guard and isolation reservation, stop-work cue, handover, and no-safety determination",
        "loft-equipment-state-board",
        "THOS Body and CBR Heart",
        "completed",
        "sewing, cutting, heating, pressing, equipment, guarding, isolation, stop work, handover, and safety-decision refusal",
        ["NZ-WORKSAFE-MACHINERY-2026", "NZ-WORKSAFE-LOCKOUT", "W3C-PROV-O"],
    ),
    (
        15,
        "GMUT anisotropic sail-membrane weak-form proxy with typed chart, metric, strain placeholder, constitutive tensor, boundary condition, domain, identifiability hold, and zero empirical fit",
        "gmut-anisotropic-membrane-proxy",
        "GMUT Mind",
        "represented",
        "typed membrane chart, metric, strain, constitutive tensor, boundary condition, domain, identifiability, and empirical-fit refusal",
        ["NIST-SP811", "ASTM-D5034-21R25"],
    ),
    (
        16,
        "GMUT seam-interface jump-condition board with panel charts, interface normal, traction placeholder, continuity class, residual, covariance hold, and no-stability theorem",
        "gmut-seam-interface-board",
        "GMUT Mind",
        "completed",
        "panel chart, seam interface, normal, traction placeholder, continuity, residual, covariance, and stability-theorem refusal",
        ["NIST-SP811", "W3C-PROV-O"],
    ),
    (
        17,
        "GMUT corner-singularity refinement ledger with patch hierarchy, local coordinate, mesh placeholder, convergence obligation, unresolved exponent, and no-prediction claim",
        "gmut-corner-refinement-ledger",
        "GMUT Mind",
        "completed",
        "corner singularity, patch hierarchy, local coordinate, mesh, convergence obligation, exponent gap, and prediction refusal",
        ["NIST-SP811", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        18,
        "GMUT prestress, pressure, curvature, and shape-family dimensional firewall with quantity kind, unit, sign convention, parameter domain, and zero-force discovery claim",
        "gmut-prestress-shape-firewall",
        "GMUT Mind",
        "completed",
        "prestress, pressure, curvature, shape family, quantity kind, unit, sign, domain, and force-discovery refusal",
        ["NIST-SP811", "RFC-8785"],
    ),
    (
        19,
        "Repair-patch topology and damage-boundary contract with synthetic tear path, stop-hole reservation, patch extent, orientation, edge distance, evidence hold, and no-repair authorization",
        "repair-patch-topology",
        "GMUT Mind and THOS Body",
        "completed",
        "tear path, damage boundary, stop-hole reservation, patch extent, orientation, edge distance, and repair-authorization refusal",
        ["W3C-PROV-O", "ASTM-D5034-21R25", "NIST-SP811"],
    ),
    (
        20,
        "Inspection defect and evidence ledger with synthetic image-free location token, defect class, severity placeholder, uncertainty, correction, escalation, and no-serviceability decision",
        "sail-defect-evidence-ledger",
        "CBR Heart and THOS Body",
        "completed",
        "image-free location, defect class, severity placeholder, uncertainty, correction, escalation, and serviceability refusal",
        ["WORLD-SAILING-ERS-2025-2028", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        21,
        "Accessible sailmaking job-state and error-summary audit with noncolour status, focus order, keyboard path, zoom, print order, plain-language note, and reserved human evaluation",
        "accessible-loft-status-audit",
        "CBR Heart and THOS Body",
        "completed",
        "job state, error summary, noncolour status, focus order, keyboard, zoom, print, plain language, and human-evaluation reservation",
        ["W3C-WCAG-22", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        22,
        "Unfinished sail-job relay invariant with active-step pin, loose-part inventory, machine isolation placeholder, custody acknowledgement, unresolved-risk escrow, and resume prohibition",
        "unfinished-sail-relay",
        "THOS Body and CBR Heart",
        "completed",
        "active step, loose part, machine isolation, custody acknowledgement, unresolved risk, handover, and resume prohibition",
        ["NZ-WORKSAFE-LOCKOUT", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        23,
        "Workload, fatigue-cue, queue, interruption, rest, skill-boundary, escalation, and shift-handover docket with zero worker monitoring and no fitness determination",
        "sail-loft-workload-docket",
        "CBR Heart and THOS Body",
        "completed",
        "workload, fatigue cue, queue, interruption, rest, skill boundary, escalation, handover, and worker-monitoring refusal",
        ["NZ-WORKSAFE-MACHINERY-2026", "NZ-PRIVACY-PRINCIPLES", "RFC-3339"],
    ),
    (
        24,
        "THOS sailmaking error-recovery study design with sealed comparison lanes, matched action budget, topology-error endpoint, stop conditions, synthetic cases, and no participants",
        "thos-sailmaking-study-protocol",
        "THOS Body",
        "represented",
        "sailmaking error recovery, sealed lanes, matched action budget, topology-error endpoint, stop conditions, and participant refusal",
        ["W3C-PROV-O", "RFC-3339", "NZ-WORKSAFE-MACHINERY-2026"],
    ),
    (
        25,
        "THOS synthetic panel-to-seam mismatch triage proxy with panel token, expected neighbor, presented edge, confidence, quarantine, escalation, readback, and no-production decision",
        "thos-panel-mismatch-proxy",
        "THOS Body",
        "represented",
        "synthetic panel mismatch, expected neighbor, presented edge, confidence, quarantine, escalation, readback, and production-decision refusal",
        ["W3C-PROV-O", "RFC-8785", "NZ-WORKSAFE-MACHINERY-2026"],
    ),
    (
        26,
        "Freed ID synthetic sail-repair evidence credential with job referent, pattern revision, material digest, custody chain, validity interval, issuer placeholder, and proof refusal",
        "freed-id-sail-repair-credential",
        "Freed ID",
        "represented",
        "synthetic sail-repair evidence, job referent, pattern revision, material digest, custody, validity, issuer, and proof refusal",
        ["W3C-VC-DM-20", "W3C-DATA-INTEGRITY-10", "W3C-DID-10"],
    ),
    (
        27,
        "Freed ID synthetic sailcloth-lot selective-disclosure envelope with provenance graph partition, disclosed seam digest, concealed supplier placeholder, challenge nonce, verifier-purpose record, and no cryptographic proof",
        "freed-id-sailcloth-disclosure-envelope",
        "Freed ID and CBR Heart",
        "represented",
        "synthetic sailcloth-lot selective disclosure, provenance partition, seam digest, concealed supplier, challenge nonce, verifier purpose, and proof refusal",
        ["W3C-VC-DM-20", "W3C-DATA-INTEGRITY-10", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        28,
        "Sail owner, designer, maker, repairer, vessel, class, pattern, measurement, defect-note, disclosure, retention, access, correction, complaint, and minimization envelope",
        "sail-job-privacy-envelope",
        "CBR Heart and Freed ID",
        "completed",
        "owner, designer, maker, repairer, vessel, class, pattern, measurement, disclosure, retention, access, correction, complaint, minimization, and privacy-complete refusal",
        ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "W3C-WCAG-22"],
    ),
    (
        29,
        "Real sailcloth testing, loft measurement, sail inspection, operator workload, accessibility, and sea-trial adapter with zero people, zero sail, zero machine, zero query, zero measurement, and zero rows",
        "sailmaking-zero-row-adapter",
        "GMUT Mind and THOS Body",
        "open_gap",
        "real sailcloth test, loft measurement, sail inspection, workload, accessibility, sea trial, authorization, and zero-row refusal",
        ["ASTM-D5034-21R25", "WORLD-SAILING-ERS-2025-2028", "NZ-WORKSAFE-MACHINERY-2026"],
    ),
    (
        30,
        "CBR sail, vessel, voyage, place, design knowledge, collective interest, tikanga, disability, privacy, access, return, remedy, legal, cultural, data-governance, affected-party, and Māori-authority matrix",
        "cbr-sail-authority-matrix",
        "Freed ID and CBR Heart",
        "exact_gate",
        "sail, vessel, voyage, place, design knowledge, collective interest, tikanga, disability, privacy, access, return, remedy, legal, cultural, governance, affected-party, and Māori-authority reservation",
        ["NZ-PRIVACY-PRINCIPLES", "W3C-WCAG-22", "TMR-PRINCIPLES", "LOCAL-CONTEXTS-TK-BC"],
    ),
]


SKILL_IDEAS = [
    "ghc-family-sailmaking-custody-boundary",
    "ghc-family-sailmaking-panel-topology-integrity",
    "ghc-family-sailmaking-material-substitution-reserve",
    "ghc-family-sailmaking-equipment-stop-work-boundary",
    "ghc-family-sailmaking-repair-handover",
    "ghc-family-sailmaking-accessibility-workload-boundary",
    "ghc-family-sail-privacy-authority-reserve",
    "ghc-family-gmut-anisotropic-membrane-firewall",
    "ghc-family-thos-freed-sailmaking-profile",
    "ghc-family-sailmaking-evidence-nonpromotion",
]


RUNNER_IDEAS = [
    "ghc_family_sailmaking_custody_boundary.py",
    "ghc_family_sailmaking_panel_topology_integrity.py",
    "ghc_family_sailmaking_material_substitution_reserve.py",
    "ghc_family_sailmaking_equipment_stop_work_boundary.py",
    "ghc_family_sailmaking_repair_handover.py",
    "ghc_family_sailmaking_accessibility_workload_boundary.py",
    "ghc_family_sail_privacy_authority_reserve.py",
    "ghc_family_gmut_anisotropic_membrane_firewall.py",
    "ghc_family_thos_freed_sailmaking_profile.py",
    "ghc_family_v656_v2_suite.py",
]


CLEAN_SURFACES = [
    "sail job, synthetic sail token, purpose, presented dimensions, custody, correction, and return vocabulary",
    "tack, clew, head, luff, leech, foot, datum, unit, uncertainty, and coordinate-frame discipline",
    "panel, seam, adjacency, grain direction, orientation, overlap, notch, and reversible topology",
    "cloth roll, lot, thread, needle, tape, adhesive, webbing, hardware, substitution, and property refusal",
    "reef, cringle, ring, batten pocket, attachment route, reinforcement, interface, and compatibility holds",
    "cut plan, nesting, remnant, template, spline, fairing, registration mark, and zero-machine control",
    "damage boundary, repair patch, defect note, condition, escalation, evidence, and serviceability refusal",
    "guarding, isolation, stop work, workload, fatigue cue, queue, rest, readback, and shift handover",
    "GMUT membrane chart, seam jump, corner refinement, prestress, curvature, unit, and observation firewall",
    "privacy, remedy, design knowledge, collective interest, legal, cultural, affected-party, and Māori-authority refusal",
]


def _negative(
    number: int,
    signature: str,
    failed: str,
    recovery: str,
    recurrence_guard: str,
) -> dict:
    return {
        "negative_id": f"V6562-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": recurrence_guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "broad_memory_registry_search_timed_out",
        "The first broad MEMORY.md registry search exceeded its bounded wrapper without usable current-phase evidence.",
        "Stop the broad scan and use bounded literal line windows plus the live activation.",
        "Never broaden a large memory registry scan after a bounded timeout.",
    ),
    _negative(
        2,
        "narrow_memory_registry_search_timed_out",
        "A narrower exact-term MEMORY.md search also timed out and earned zero evidence credit.",
        "Read only the known relevant line windows through the direct file surface.",
        "Prefer exact line windows when the registry search surface is slow.",
    ),
    _negative(
        3,
        "memory_file_probe_timed_out",
        "An initial bounded Get-Item memory probe timed out before returning a scalar result.",
        "Retry only the scalar file probe with a longer bound; do not repeat content scans.",
        "Separate metadata availability probes from content searches.",
    ),
    _negative(
        4,
        "foreach_pipeline_empty_element_parser_fault",
        "The first PowerShell skill-inventory wrapper piped directly from foreach and failed with EmptyPipeElement.",
        "Materialize the foreach output before piping it to formatting.",
        "Never attach a pipeline directly to an unparenthesized foreach statement.",
    ),
    _negative(
        5,
        "foreach_paths_missing_space_parser_fault",
        "A later wrapper used foreach($p in$paths) and failed before any requested file read.",
        "Use explicit foreach ($item in $items) syntax.",
        "Keep whitespace around PowerShell foreach and in tokens.",
    ),
    _negative(
        6,
        "foreach_relatives_missing_space_parser_fault",
        "A second wrapper used foreach($rel in$rels) and failed before reading source artifacts.",
        "Use explicit foreach ($item in $items) syntax or a structured reader.",
        "Run parser-sensitive loops as separate, conventionally spaced statements.",
    ),
    _negative(
        7,
        "source_size_wrapper_missing_space_parser_fault",
        "The first source-artifact size wrapper repeated the missing-space foreach syntax and returned no evidence.",
        "Use literal-path scalar size probes with conventional loop spacing.",
        "Reuse the corrected loop form rather than reconstructing it.",
    ),
    _negative(
        8,
        "combined_phase_mechanics_inventory_timed_out",
        "A combined recursive scripts, tests, docs, and receipt inventory exceeded 30 seconds without a complete result.",
        "Split the inventory into directory-local literal probes.",
        "Do not combine multiple large D-drive inventories in one evidentiary wrapper.",
    ),
    _negative(
        9,
        "recursive_document_inventory_timed_out",
        "The split recursive documentation inventory still timed out after yielding only partial paths.",
        "Stop the recursion and read exact committed artifact paths named by the activation.",
        "Use exact-file contracts rather than recursive documentation scans on the large worktree.",
    ),
    _negative(
        10,
        "worktree_add_wrapper_timed_out_during_checkout",
        "The worktree-add wrapper timed out after creating the branch and beginning a large checkout.",
        "Do not retry; inspect registration, branch, HEAD, locks, processes, and status before resuming.",
        "Treat timed-out Git mutations as indeterminate until exact post-state is resolved.",
    ),
    _negative(
        11,
        "worktree_poststate_path_probe_timed_out",
        "The first literal lane-path post-state probe timed out while Git was still materializing files.",
        "Use worktree registration and process evidence, then wait for checkout completion.",
        "Avoid filesystem enumeration while an initializing worktree is actively materializing.",
    ),
    _negative(
        12,
        "worktree_process_probe_with_path_timed_out",
        "The first process probe requested executable Path metadata and timed out during checkout contention.",
        "Query only process IDs, names, start times, and responsiveness.",
        "Omit expensive process Path properties during D-drive contention.",
    ),
    _negative(
        13,
        "sequential_wait_process_wrapper_timed_out",
        "A monitoring wrapper applied a per-process wait sequentially and exceeded its aggregate bound.",
        "Poll the process set once or wait on a single controlling condition.",
        "Do not multiply a timeout by iterating it across process IDs.",
    ),
    _negative(
        14,
        "parallel_d_drive_completion_probes_timed_out",
        "Three simultaneous D-drive completion probes timed out while checkout I/O remained saturated.",
        "Reduce contention and use one scalar native process-list check.",
        "Never parallelize metadata probes against a saturated checkout surface.",
    ),
    _negative(
        15,
        "quiet_window_process_check_timed_out",
        "A quiet-window wrapper slept and then used the slow process provider, exceeding its bound without a result.",
        "Use the native bounded task-list scalar and then one exact Git status check.",
        "Prefer the cheapest scalar process surface after an intentional quiet window.",
    ),
    _negative(
        16,
        "unicode_source_console_render_fault",
        "The first inherited source-metadata extraction failed when the console code page could not render Māori characters.",
        "Enable UTF-8 and serialize structured output with explicit Unicode-safe handling.",
        "Set UTF-8 before emitting source metadata that can contain Māori text.",
    ),
    _negative(
        17,
        "reflection_validation_filename_assumption",
        "A combined receipt probe guessed a reflection-remaster validation filename that the current runner does not emit.",
        "List the exact phase reflection directory and read its inventory, issues, methods, and report artifacts.",
        "Resolve current runner outputs before querying convenience receipt names.",
    ),
    _negative(
        18,
        "corrected_builder_monitor_wrapper_timed_out",
        "The first corrected-builder monitor returned log metadata but exceeded its wrapper before the full probe completed.",
        "Use one native task-count scalar plus the exact final receipt and log lengths.",
        "Keep background-builder monitor probes scalar and independently attributable.",
    ),
]
