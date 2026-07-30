#!/usr/bin/env python3
"""Sylven Arc v656-v3 source, proposal, portfolio, and startup catalogue."""

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
        "CVMA-CONSERVATION-2004",
        "Guidelines for the Conservation and Restoration of Stained Glass, Second Edition",
        "Corpus Vitrearum / ICOMOS",
        "https://www.cvma.ac.uk/CVConservationGuidelines2004.pdf",
        "stable_reference",
        (
            "historic-stained-glass research, documentation, context, preventive-conservation, "
            "professional-collaboration, and accessibility-of-records vocabulary only; no "
            "treatment, conservation, custody, competence, or heritage decision"
        ),
    ),
    _source(
        "ISO-9050-2026",
        "ISO 9050:2026 Glass in building - Determination of luminous and solar characteristics of glazing",
        "International Organization for Standardization",
        "https://www.iso.org/standard/88642.html",
        "current",
        (
            "July 2026 glazing, luminous, solar, spectral, quantity, method, and comparison "
            "vocabulary only; no standard text reproduction, specimen, measurement, test, "
            "calculation, compliance, or material-performance claim"
        ),
    ),
    _source(
        "CIE-015-2018",
        "CIE 015:2018 Colorimetry, 4th Edition",
        "International Commission on Illumination",
        "https://www.cie.co.at/publications/colorimetry-4th-edition",
        "current_reference",
        (
            "observer, illuminant, tristimulus, chromaticity, colour-space, and colour-difference "
            "vocabulary only; no colour measurement, appearance judgement, or conservation claim"
        ),
    ),
    _source(
        "ISO-15368-2021",
        "ISO 15368:2021 Optics and photonics - Measurement of reflectance and transmittance",
        "International Organization for Standardization",
        "https://www.iso.org/standard/72598.html",
        "current_reference",
        (
            "spectral transmittance, reflectance, plane-element, and instrument-method "
            "vocabulary only; no test, calibration, material result, or applicability decision"
        ),
    ),
    _source(
        "NZ-WORKSAFE-LEAD",
        "Managing lead-based paint",
        "WorkSafe New Zealand",
        "https://www.worksafe.govt.nz/topic-and-industry/hazardous-substances/guidance/substances/managing-lead-based-paint/",
        "current_context",
        (
            "lead-exposure seriousness, competent assessment, containment, and worker-health "
            "reservation context only; not a stained-glass procedure, exposure assessment, "
            "medical decision, workplace control, or safety authorization"
        ),
    ),
    _source(
        "NIST-SP811",
        "NIST SP 811: Guide for the Use of the International System of Units",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/publications/guide-use-international-system-units-si",
        "stable",
        (
            "quantity, unit, symbol, conversion, length, area, force, stress, temperature, "
            "time, wavelength, and angle discipline only; no real metrology or calibration"
        ),
    ),
    _source(
        "W3C-PROV-O",
        "PROV-O: The PROV Ontology",
        "W3C",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        (
            "entity, activity, agent-placeholder, derivation, revision, attribution, "
            "generation, invalidation, custody, and correction lineage"
        ),
    ),
    _source(
        "RFC-3339",
        "RFC 3339: Date and Time on the Internet: Timestamps",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic UTC lexical timestamps, intervals, treatment revisions, and handovers",
    ),
    _source(
        "RFC-8785",
        "RFC 8785: JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic contract, receipt, statement, and manifest serialization",
    ),
    _source(
        "W3C-WCAG-22",
        "Web Content Accessibility Guidelines 2.2",
        "W3C",
        "https://www.w3.org/TR/WCAG22/",
        "current_recommendation",
        (
            "structural accessibility vocabulary with manual, browser, assistive-technology, "
            "Māori-language, cognitive, low-vision, colour-perception, and affected-user "
            "evaluation reserved"
        ),
    ),
    _source(
        "NZ-PRIVACY-PRINCIPLES",
        "Privacy Act 2020 information privacy principles",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        (
            "purpose, source, notice, fair collection, security, access, correction, accuracy, "
            "retention, use, disclosure, and identifier reservations only; no legal advice"
        ),
    ),
    _source(
        "W3C-VC-DM-20",
        "Verifiable Credentials Data Model v2.0",
        "W3C",
        "https://www.w3.org/TR/vc-data-model-2.0/",
        "current_recommendation",
        (
            "synthetic credential vocabulary only; no conforming credential claim, real "
            "issuer, holder, verifier, proof, trust decision, or interoperability event"
        ),
    ),
    _source(
        "RFC-9943",
        "RFC 9943: An Architecture for Trustworthy and Transparent Digital Supply Chains",
        "IETF / RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc9943.html",
        "current_proposed_standard",
        (
            "June 2026 signed-statement, transparent-statement, receipt, registration-policy, "
            "and transparency-service vocabulary only; no live service, key, signature, "
            "registration, receipt, audit, trust, or non-equivocation claim"
        ),
    ),
    _source(
        "C2PA-2.4",
        "C2PA Content Credentials Technical Specification 2.4",
        "Coalition for Content Provenance and Authenticity",
        "https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html",
        "current",
        (
            "April 2026 manifest, assertion, ingredient-v3, action, binding, validation-result, "
            "and trust-model vocabulary only; no signed manifest, certificate, timestamp, "
            "revocation, validation, trust, or authenticity claim"
        ),
    ),
    _source(
        "MET-COLLECTION-API",
        "The Metropolitan Museum of Art Collection API",
        "The Metropolitan Museum of Art",
        "https://metmuseum.github.io/",
        "current_documented_surface",
        (
            "public collection search, object identifier, object metadata, measurement-field, "
            "rights, and update-date readiness vocabulary only; zero requests, downloads, "
            "objects, images, rows, cultural interpretations, or likelihoods"
        ),
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
        "current_reference",
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
        "Stained-glass panel intake and custody passport with synthetic panel token, architectural-context placeholder, stated scope, condition note, transfer acknowledgement, correction path, and no-real-object claim",
        "glass-panel-intake-passport",
        "Freed ID and CBR Heart",
        "completed",
        "panel intake, synthetic token, context placeholder, scope, condition, custody, correction, and real-object refusal",
        ["CVMA-CONSERVATION-2004", "W3C-PROV-O", "RFC-3339", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        2,
        "Stained-glass panel cell, glass-piece, lead-line, border, opening, and adjacency topology graph with orphan quarantine, reversible edit, and no-fabrication instruction",
        "glass-panel-topology-graph",
        "GMUT Mind and Freed ID",
        "completed",
        "panel cell, glass piece, lead line, border, opening, adjacency, orphan quarantine, rollback, and fabrication refusal",
        ["CVMA-CONSERVATION-2004", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        3,
        "Architectural-opening, panel-side, lancet, light, register, medallion, datum, orientation, scale, unit, uncertainty, and revision coordinate-frame contract",
        "glass-coordinate-frame",
        "GMUT Mind",
        "completed",
        "architectural opening, panel side, lancet, light, register, medallion, datum, orientation, scale, unit, uncertainty, and revision",
        ["CVMA-CONSERVATION-2004", "NIST-SP811", "W3C-PROV-O"],
    ),
    (
        4,
        "Glass-piece material and provenance envelope with synthetic piece token, colour-family declaration, texture, thickness placeholder, maker-mark note, reuse state, substitution hold, and no-authentication claim",
        "glass-piece-provenance",
        "Freed ID and GMUT Mind",
        "completed",
        "glass piece, material, colour family, texture, thickness, maker mark, reuse, substitution, provenance, and authentication refusal",
        ["CVMA-CONSERVATION-2004", "CIE-015-2018", "W3C-PROV-O"],
    ),
    (
        5,
        "Paint, stain, enamel, silver-stain, trace-line, wash, firing-layer placeholder, loss cue, overlap, confidence, and conservation-interpretation refusal map",
        "glass-surface-layer-map",
        "GMUT Mind and CBR Heart",
        "completed",
        "paint, stain, enamel, silver stain, trace line, wash, firing layer, loss, overlap, confidence, and interpretation refusal",
        ["CVMA-CONSERVATION-2004", "CIE-015-2018", "W3C-PROV-O"],
    ),
    (
        6,
        "Lead-came profile and joint network with flange, heart, channel, intersection, solder-joint placeholder, deformation cue, duplicate quarantine, and no-structural-release claim",
        "lead-came-network",
        "GMUT Mind and THOS Body",
        "completed",
        "lead came, flange, heart, channel, joint, intersection, deformation, duplicate quarantine, and structural-release refusal",
        ["CVMA-CONSERVATION-2004", "NZ-WORKSAFE-LEAD", "W3C-PROV-O"],
    ),
    (
        7,
        "Copper-foil edge, overlap, adhesive placeholder, solder-bead relation, joint continuity, contamination cue, repair revision, and no-process authorization board",
        "copper-foil-joint-board",
        "THOS Body and Freed ID",
        "completed",
        "copper foil, edge, overlap, adhesive, solder bead, joint continuity, contamination, revision, and process-authorization refusal",
        ["CVMA-CONSERVATION-2004", "NZ-WORKSAFE-LEAD", "W3C-PROV-O"],
    ),
    (
        8,
        "Detached-fragment inventory and candidate-match ledger with synthetic fragment token, edge signature, painted-feature cue, uncertainty, conflict quarantine, custody, and no-reassembly command",
        "glass-fragment-match-ledger",
        "Freed ID and GMUT Mind",
        "completed",
        "fragment inventory, synthetic token, edge signature, painted feature, candidate match, uncertainty, custody, conflict, and reassembly refusal",
        ["CVMA-CONSERVATION-2004", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        9,
        "Crack, break, loss, bowing, bulge, corrosion, deposit, paint-loss, previous-repair, location, severity-placeholder, confidence, correction, and no-condition-conclusion map",
        "glass-condition-map",
        "GMUT Mind and CBR Heart",
        "completed",
        "crack, break, loss, bowing, bulge, corrosion, deposit, paint loss, previous repair, location, uncertainty, and condition-conclusion refusal",
        ["CVMA-CONSERVATION-2004", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        10,
        "Support-bar, saddle-bar, tie-wire, ferramenta, frame, groove, panel-edge, attachment, movement-placeholder, interference, and no-installation decision ledger",
        "glass-support-interface",
        "GMUT Mind and THOS Body",
        "completed",
        "support bar, saddle bar, tie wire, ferramenta, frame, groove, panel edge, attachment, movement, interference, and installation refusal",
        ["CVMA-CONSERVATION-2004", "NIST-SP811", "W3C-PROV-O"],
    ),
    (
        11,
        "Protective-glazing cavity, vent path, drainage cue, exterior-interior side, condensation placeholder, access constraint, monitoring gap, and no-design-approval board",
        "protective-glazing-cavity-board",
        "GMUT Mind and THOS Body",
        "completed",
        "protective glazing, cavity, vent path, drainage, side, condensation placeholder, access, monitoring gap, and design-approval refusal",
        ["CVMA-CONSERVATION-2004", "NIST-SP811", "W3C-PROV-O"],
    ),
    (
        12,
        "Conservation-intervention delta graph with baseline state, proposed action placeholder, affected element, material note, reversibility reservation, dependency, supersession, rollback, and no-treatment approval",
        "glass-intervention-delta",
        "Freed ID and CBR Heart",
        "completed",
        "baseline, intervention proposal, affected element, material note, reversibility, dependency, supersession, rollback, and treatment-approval refusal",
        ["CVMA-CONSERVATION-2004", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        13,
        "Panel crate, face orientation, support plane, cushion zone, fragment containment, shock and tilt placeholder, seal state, transfer check, and no-transport authorization docket",
        "glass-packing-custody-docket",
        "THOS Body and Freed ID",
        "completed",
        "panel crate, face orientation, support plane, cushion, fragment containment, shock, tilt, seal, transfer, and transport-authorization refusal",
        ["CVMA-CONSERVATION-2004", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        14,
        "Condition-image capture map with synthetic asset token, raking, transmitted, reflected, ultraviolet-placeholder mode, scale cue, viewpoint, rights, redaction, lineage, and no-diagnostic-image claim",
        "glass-condition-image-map",
        "Freed ID and CBR Heart",
        "completed",
        "condition image, synthetic asset, capture mode, scale cue, viewpoint, rights, redaction, lineage, and diagnostic-image refusal",
        ["CVMA-CONSERVATION-2004", "C2PA-2.4", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        15,
        "GMUT heterogeneous stained-glass thin-plate weak-form proxy with typed chart, piecewise stiffness placeholder, came-interface trace, boundary condition, load placeholder, unit, identifiability hold, and zero empirical fit",
        "gmut-glass-plate-proxy",
        "GMUT Mind",
        "represented",
        "heterogeneous thin plate, chart, piecewise stiffness, came interface, trace, boundary condition, load placeholder, unit, identifiability, and empirical-fit refusal",
        ["NIST-SP811", "CVMA-CONSERVATION-2004"],
    ),
    (
        16,
        "GMUT spectral radiative-transfer and colour-observer obligation board with wavelength domain, transmittance symbol, illuminant, observer, piece field, uncertainty, unit, and real-measurement firewall",
        "gmut-glass-spectral-board",
        "GMUT Mind",
        "completed",
        "spectral radiative transfer, wavelength, transmittance, illuminant, observer, piece field, uncertainty, unit, and measurement refusal",
        ["ISO-9050-2026", "ISO-15368-2021", "CIE-015-2018", "NIST-SP811"],
    ),
    (
        17,
        "GMUT lead-came graph coupling ledger with glass-cell state, came-edge state, node equilibrium placeholder, incidence matrix, orientation, interface residual, unit, and stability-theorem refusal",
        "gmut-came-graph-ledger",
        "GMUT Mind",
        "completed",
        "glass cell, came edge, graph coupling, node equilibrium, incidence matrix, orientation, interface residual, unit, and stability-theorem refusal",
        ["NIST-SP811", "W3C-PROV-O"],
    ),
    (
        18,
        "GMUT crack-interface cohesive-zone typing board with crack path, opening placeholder, traction symbol, energy quantity, history variable, irreversibility obligation, domain, unit, and prediction firewall",
        "gmut-glass-crack-interface",
        "GMUT Mind",
        "completed",
        "crack path, cohesive interface, opening, traction, energy, history variable, irreversibility, domain, unit, and prediction refusal",
        ["NIST-SP811", "CVMA-CONSERVATION-2004"],
    ),
    (
        19,
        "Accessible stained-glass condition report with text alternative, topology table, noncolour condition state, focus order, keyboard path, zoom, print order, plain-language note, and reserved human evaluation",
        "accessible-glass-condition-report",
        "CBR Heart and THOS Body",
        "completed",
        "condition report, text alternative, topology table, noncolour state, focus order, keyboard, zoom, print, plain language, and human-evaluation reservation",
        ["W3C-WCAG-22", "CVMA-CONSERVATION-2004"],
    ),
    (
        20,
        "Conservation-material compatibility and cure-reservation ledger with adhesive placeholder, consolidant placeholder, substrate class, batch, expiry, environment cue, test gap, substitution hold, and no-treatment instruction",
        "glass-material-compatibility-ledger",
        "THOS Body and CBR Heart",
        "completed",
        "adhesive, consolidant, substrate, batch, expiry, environment, test gap, substitution, and treatment-instruction refusal",
        ["CVMA-CONSERVATION-2004", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        21,
        "Glass-handling, soldering, heating, extraction, cutting, lifting, and cleaning equipment-state board with competent-person, lead-control, isolation, stop-work, and no-safety determination",
        "glass-equipment-state-board",
        "THOS Body and CBR Heart",
        "completed",
        "handling, soldering, heating, extraction, cutting, lifting, cleaning, equipment state, competent person, lead control, isolation, stop work, and safety-decision refusal",
        ["NZ-WORKSAFE-LEAD", "CVMA-CONSERVATION-2004", "W3C-PROV-O"],
    ),
    (
        22,
        "Conservation queue, interruption, unresolved-fragment, active-treatment-placeholder, exposure cue, workload limit, correction readback, custody acknowledgement, and shift-handover docket",
        "glass-workload-handover",
        "THOS Body and CBR Heart",
        "completed",
        "queue, interruption, unresolved fragment, treatment placeholder, exposure cue, workload, correction, custody acknowledgement, and handover",
        ["CVMA-CONSERVATION-2004", "NZ-WORKSAFE-LEAD", "RFC-3339"],
    ),
    (
        23,
        "Panel loan, removal, temporary storage, installation-return placeholder, condition comparison, discrepancy, acknowledgement, unresolved-risk escrow, and no-custody-transfer authorization board",
        "glass-loan-transfer-board",
        "Freed ID and CBR Heart",
        "completed",
        "panel loan, removal, storage, installation return, condition comparison, discrepancy, acknowledgement, risk escrow, and custody-transfer refusal",
        ["CVMA-CONSERVATION-2004", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        24,
        "THOS stained-glass damage-escalation study design with sealed comparison lanes, matched action budget, topology-error endpoint, fragment-loss endpoint, harm stops, synthetic cases, and no participants",
        "thos-glass-damage-study",
        "THOS Body",
        "represented",
        "damage escalation, sealed lanes, matched action budget, topology error, fragment loss, harm stops, synthetic cases, and participant refusal",
        ["CVMA-CONSERVATION-2004", "W3C-PROV-O", "RFC-3339"],
    ),
    (
        25,
        "THOS synthetic fragment-to-panel mismatch and custody-handover proxy with fragment token, candidate cell, edge cue, confidence, conflict quarantine, escalation, readback, and no-conservation decision",
        "thos-fragment-handover-proxy",
        "THOS Body",
        "represented",
        "synthetic fragment mismatch, candidate cell, edge cue, confidence, quarantine, escalation, readback, custody handover, and conservation-decision refusal",
        ["CVMA-CONSERVATION-2004", "W3C-PROV-O", "RFC-8785"],
    ),
    (
        26,
        "Freed ID synthetic RFC 9943 stained-glass intervention statement envelope with artifact digest, issuer placeholder, registration-policy placeholder, transparent-statement relation, receipt absence, privacy warning, and nonproduction refusal",
        "freed-id-glass-scitt-envelope",
        "Freed ID",
        "represented",
        "synthetic SCITT signed statement, intervention artifact, digest, issuer, registration policy, transparent statement, receipt absence, privacy, and nonproduction refusal",
        ["RFC-9943", "RFC-8785", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        27,
        "Freed ID synthetic C2PA 2.4 condition-image manifest profile with asset token, ingredient-v3 relation, action assertion, redaction state, validation-result placeholder, credential absence, trust refusal, and nonproduction boundary",
        "freed-id-glass-c2pa-profile",
        "Freed ID and CBR Heart",
        "represented",
        "synthetic C2PA manifest, condition image, ingredient v3, action, redaction, validation result, credential absence, trust refusal, and nonproduction boundary",
        ["C2PA-2.4", "RFC-8785", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        28,
        "Panel owner, custodian, donor, building, location, subject, image, maker-attribution placeholder, condition note, treatment note, disclosure, retention, access, correction, complaint, and minimization envelope",
        "glass-record-privacy-envelope",
        "CBR Heart and Freed ID",
        "completed",
        "owner, custodian, donor, building, location, subject, image, attribution, condition, treatment, disclosure, retention, access, correction, complaint, minimization, and privacy-complete refusal",
        ["NZ-PRIVACY-PRINCIPLES", "W3C-PROV-O", "W3C-WCAG-22"],
    ),
    (
        29,
        "Metropolitan Museum Collection API stained-glass object, object-id, classification, measurements, rights, image, metadata-date, provenance-field, and zero-query zero-row readiness adapter",
        "met-glass-zero-row-adapter",
        "GMUT Mind and Freed ID",
        "open_gap",
        "public collection API, stained-glass object, identifier, classification, measurement field, rights, image, update date, provenance, authorization, zero query, and zero row",
        ["MET-COLLECTION-API", "ISO-9050-2026", "NZ-PRIVACY-PRINCIPLES"],
    ),
    (
        30,
        "CBR stained-glass subject, sacred image, taonga possibility, donor and collective interest, building and place, photography, access, restriction, return, repatriation, remedy, legal, cultural, data-governance, affected-party, and Māori-authority matrix",
        "cbr-glass-authority-matrix",
        "Freed ID and CBR Heart",
        "exact_gate",
        "stained-glass subject, sacred image, taonga possibility, donor, collective interest, building, place, photography, access, restriction, return, repatriation, remedy, legal, cultural, governance, affected-party, and Māori-authority reservation",
        ["CVMA-CONSERVATION-2004", "NZ-PRIVACY-PRINCIPLES", "TMR-PRINCIPLES", "LOCAL-CONTEXTS-TK-BC"],
    ),
]


SKILL_IDEAS = [
    "ghc-family-glass-panel-custody-boundary",
    "ghc-family-glass-topology-integrity",
    "ghc-family-glass-fragment-reconciliation",
    "ghc-family-glass-treatment-authority-reserve",
    "ghc-family-glass-image-provenance-boundary",
    "ghc-family-glass-accessibility-handover",
    "ghc-family-glass-privacy-cultural-reserve",
    "ghc-family-gmut-glass-interface-firewall",
    "ghc-family-thos-freed-glass-profile",
    "ghc-family-glass-evidence-nonpromotion",
]


RUNNER_IDEAS = [
    "ghc_family_glass_panel_custody_boundary.py",
    "ghc_family_glass_topology_integrity.py",
    "ghc_family_glass_fragment_reconciliation.py",
    "ghc_family_glass_treatment_authority_reserve.py",
    "ghc_family_glass_image_provenance_boundary.py",
    "ghc_family_glass_accessibility_handover.py",
    "ghc_family_glass_privacy_cultural_reserve.py",
    "ghc_family_gmut_glass_interface_firewall.py",
    "ghc_family_thos_freed_glass_profile.py",
    "ghc_family_v656_v3_suite.py",
]


CLEAN_SURFACES = [
    "panel intake, synthetic token, context, scope, custody, correction, discrepancy, and return vocabulary",
    "panel cell, glass piece, lead line, border, opening, datum, orientation, unit, uncertainty, and topology",
    "glass material, colour declaration, texture, paint layer, stain, enamel, fragment, provenance, and substitution",
    "came, foil, solder-joint placeholder, support bar, tie wire, frame, interface, conflict, and release refusal",
    "condition map, crack, break, loss, bowing, deposit, previous repair, confidence, and conclusion refusal",
    "intervention delta, treatment placeholder, material note, reversibility, supersession, rollback, and approval hold",
    "crate, cushion, support plane, fragment containment, shock and tilt placeholder, seal, custody, and transport refusal",
    "equipment state, lead-control reservation, isolation, stop work, workload, correction, and shift handover",
    "GMUT thin plate, spectral field, graph coupling, crack interface, unit, domain, and observation firewall",
    "privacy, accessibility, sacred image, taonga possibility, donor, collective interest, remedy, legal, cultural, and Māori-authority refusal",
]


def _negative(
    number: int,
    signature: str,
    failed: str,
    recovery: str,
    recurrence_guard: str,
) -> dict:
    return {
        "negative_id": f"V6563-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": recurrence_guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "combined_required_reference_read_truncated",
        "A combined read of three required skill schemas exceeded the visible output bound and did not establish through-EOF evidence.",
        "Reread each required schema separately through EOF before repository mutation.",
        "Never combine selected required references when their complete output may exceed the tool display bound.",
    ),
    _negative(
        2,
        "auth_schema_short_read_timed_out",
        "The first literal read of the authorization schema exceeded its short shell bound and returned no complete evidence.",
        "Reread the same literal file with a longer bounded timeout; the complete schema was then witnessed.",
        "Use a longer scalar read bound for archive-backed or host-startup-sensitive required references.",
    ),
    _negative(
        3,
        "source_worktree_registry_listing_timed_out",
        "A broad Git worktree registry listing exceeded its bound after the exact source topology checks had passed.",
        "Use exact target-path and exact branch-ref probes before additive worktree creation.",
        "Do not require a full worktree-registry dump when the exact path and ref are the decision surface.",
    ),
    _negative(
        4,
        "broad_source_script_inventory_timed_out",
        "A broad scripts inventory returned partial names and exceeded its bound before becoming complete.",
        "Filter the literal scripts directory by the exact v656_v2 phase token.",
        "Use phase-token exact filtering instead of a repository-wide validator inventory.",
    ),
    _negative(
        5,
        "recursive_proposal_file_count_timed_out",
        "A recursive filesystem count of proposal ledgers exceeded its bound without a complete count.",
        "Use the exact Git tree at HEAD to count committed preregistration proposal ledgers.",
        "Prefer Git tree metadata over archive-backed recursive filesystem scans for committed paths.",
    ),
    _negative(
        6,
        "broad_proposal_keyword_scan_timed_out",
        "A broad filesystem keyword scan across proposal ledgers exceeded its bound without attributable novelty evidence.",
        "Use bounded Git grep over committed proposal ledgers and candidate-specific mechanism terms.",
        "Screen one candidate mechanism family at a time through the exact Git tree.",
    ),
    _negative(
        7,
        "novelty_audit_path_assumption_failed",
        "A guessed tooling path for the inherited novelty audit did not exist at HEAD.",
        "List the exact phase tree for novelty and frozen-index names, then read the declared provenance artifacts.",
        "Resolve evidence paths from the exact committed tree instead of owner-version conventions.",
    ),
    _negative(
        8,
        "post_manifest_source_status_timed_out",
        "A later broad source status probe exceeded its bound after earlier clean and exact-manifest witnesses had passed.",
        "Audit residual Git processes and locks, then retain the earlier clean witness and split later hygiene checks.",
        "Do not replay a successful source aggregate or combine cleanliness dimensions after an archive-backed timeout.",
    ),
    _negative(
        9,
        "fresh_lane_untracked_enumeration_timed_out",
        "A full untracked enumeration on the newly materialized 58,432-file Sylven worktree exceeded its bound.",
        "Use the successful worktree creation, exact branch and head, tracked-clean and lock witnesses, then scope later untracked checks to Sylven-owned paths.",
        "Avoid whole-worktree untracked scans immediately after a large checkout; use exact owner roots and staged manifests.",
    ),
    _negative(
        10,
        "combined_generated_validation_projection_truncated",
        "A combined projection of multiple generated validation receipts exceeded the display context and did not establish complete receipt evidence.",
        "Read one compact receipt at a time and project only its validity and bounded count fields.",
        "Never emit full or multi-receipt structured output for large validation artifacts.",
    ),
    _negative(
        11,
        "multi_file_literal_search_timed_out",
        "A bounded multi-file search for x1 count and route constants exceeded its short command bound without returning attributable evidence.",
        "Probe one exact file and one exact pattern family at a time with an archive-aware timeout.",
        "Do not combine unrelated phase constants in one archive-backed search.",
    ),
    _negative(
        12,
        "single_file_context_search_timed_out",
        "A single-file context search combined with file metadata exceeded its command bound before yielding complete context.",
        "Separate metadata from content and use a single literal context probe with a longer bound.",
        "Keep archive-backed metadata and content projections in separate scalar commands.",
    ),
    _negative(
        13,
        "lane_git_tuple_probe_timed_out",
        "A combined tracked-status, repository-root, and branch tuple probe exceeded its short bound and yielded no clean-state evidence.",
        "Retain earlier exact lane witnesses and split later Git dimensions into bounded scalar probes.",
        "Do not aggregate archive-backed Git state dimensions under a short startup-sensitive timeout.",
    ),
    _negative(
        14,
        "short_process_audit_timed_out",
        "A short process audit exceeded its bound before returning a process snapshot.",
        "Repeat the same read-only audit once with a host-startup-aware bound; the bounded snapshot then completed.",
        "Allow host-startup latency for process inventories and never treat a timed-out audit as absence of a blocker.",
    ),
    _negative(
        15,
        "roster_json_projection_timed_out",
        "A broad object projection of the current roster JSON exceeded its bound and returned no complete roster state.",
        "Read the small roster file literally and project exact endpoint and route fields with bounded text probes.",
        "Prefer literal roster records over broad PowerShell object formatting on a resource-constrained host.",
    ),
    _negative(
        16,
        "roster_interstitial_canonical_change_rejected",
        "The first updated roster validation rejected an interstitial variant that incorrectly marked canonical assignments as changed.",
        "Retain the canonical assignment ledger and set the live variant's changes_canonical_assignments field to false.",
        "Represent live route refinement in live_route_override without claiming an interstitial canonical rewrite.",
    ),
    _negative(
        17,
        "codex_cli_update_command_timed_out",
        "The explicitly authorized npm Codex CLI 0.146.0 update command exceeded its bound before returning installation or version evidence.",
        "Audit residual npm and Node processes plus the installed Codex version before deciding whether any retry is needed.",
        "After an update timeout, inspect process and version state before retrying the smallest missing step.",
    ),
]
