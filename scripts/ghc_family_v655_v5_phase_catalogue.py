#!/usr/bin/env python3
"""Sable Rook v655-v5 source, proposal, portfolio, and startup catalogue."""

from __future__ import annotations


OFFICIAL_SOURCES = [
    {
        "source_id": "WORKSAFE-ARBORICULTURE",
        "title": "Safety and health in arboriculture",
        "publisher": "WorkSafe New Zealand",
        "url": (
            "https://www.worksafe.govt.nz/topic-and-industry/forestry/"
            "health-and-safety-in-the-arboriculture-industry/"
            "safety-and-health-in-arboriculture/"
        ),
        "status": "watch",
        "use": (
            "arboriculture hazard, competence, worksite, weather-stop, rescue, "
            "tool, and handover context; explicitly watch because the page says "
            "the code predates the current work-health-and-safety legislation"
        ),
    },
    {
        "source_id": "WORKSAFE-TREES-POWER",
        "title": "Maintenance of trees around powerlines",
        "publisher": "WorkSafe New Zealand",
        "url": (
            "https://www.worksafe.govt.nz/topic-and-industry/forestry/"
            "maintenance-of-trees-around-powerlines/"
        ),
        "status": "watch",
        "use": (
            "powerline-proximity and competent-authority reservation only; no "
            "electrical, utility, pruning, access, or clearance decision"
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
        "source_id": "NZ-BIOSECURITY-1993",
        "title": "Biosecurity Act 1993",
        "publisher": "New Zealand Legislation",
        "url": (
            "https://www.legislation.govt.nz/act/public/1993/0095/"
            "latest/DLM316745.html"
        ),
        "status": "watch",
        "use": (
            "pest, organism, movement, notification, and authority reservation; "
            "no diagnosis, direction, treatment, destruction, or legal decision"
        ),
    },
    {
        "source_id": "MPI-EXOTIC-PESTS",
        "title": "Exotic pests and diseases in New Zealand",
        "publisher": "Ministry for Primary Industries",
        "url": (
            "https://www.mpi.govt.nz/biosecurity/"
            "exotic-pests-and-diseases-in-new-zealand"
        ),
        "status": "current",
        "use": (
            "symptom-observation, reporting, and referral context only; no "
            "species, pest, disease, treatment, or biosecurity determination"
        ),
    },
    {
        "source_id": "NZ-RMA-1991",
        "title": "Resource Management Act 1991",
        "publisher": "New Zealand Legislation",
        "url": "https://www.legislation.govt.nz/act/public/1991/69/en/latest/",
        "status": "watch",
        "use": (
            "land, environment, heritage, consent, and affected-party reservation "
            "without legal interpretation or planning authority"
        ),
    },
    {
        "source_id": "NZ-OPC-PRIVACY-2020",
        "title": "Privacy Act 2020 information privacy principles",
        "publisher": "Office of the Privacy Commissioner New Zealand",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "current",
        "use": (
            "purpose, minimization, collection, access, correction, retention, "
            "location, and identifier reservations"
        ),
    },
    {
        "source_id": "W3C-VC-DM-20",
        "title": "Verifiable Credentials Data Model v2.0",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/vc-data-model/",
        "status": "stable",
        "use": (
            "synthetic tree-asset status claim, evidence, privacy, and "
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
            "accessible static-report and map-alternative structure with manual, "
            "assistive-technology, Māori-language, and affected-user review reserved"
        ),
    },
    {
        "source_id": "W3C-PROV-O",
        "title": "PROV-O: The PROV Ontology",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "stable",
        "use": "entity, activity, agent, revision, derivation, custody, and correction vocabulary",
    },
    {
        "source_id": "NIST-SP811",
        "title": "NIST SP 811 — Guide for the Use of the International System of Units",
        "publisher": "National Institute of Standards and Technology",
        "url": "https://www.nist.gov/publications/guide-use-international-system-units-si",
        "status": "current",
        "use": (
            "unit and conversion discipline; not calibration, tree-risk evidence, "
            "biomechanical validation, or measurement authority"
        ),
    },
    {
        "source_id": "RFC-8785",
        "title": "RFC 8785 — JSON Canonicalization Scheme",
        "publisher": "RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "stable",
        "use": "deterministic synthetic tree-event serialization vocabulary",
    },
    {
        "source_id": "RFC-9530",
        "title": "RFC 9530 — Digest Fields",
        "publisher": "RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc9530.html",
        "status": "stable",
        "use": "content and representation digest distinction and mismatch quarantine",
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
    {
        "source_id": "ESO-SCIENCE-ARCHIVE",
        "title": "ESO Science Archive",
        "publisher": "European Southern Observatory",
        "url": "https://www.eso.org/public/science/archive/",
        "status": "current",
        "use": (
            "official archive, raw, calibration, processed-product, provenance, "
            "selection, and zero-row adapter context; no query or download"
        ),
    },
    {
        "source_id": "ADAMS-POSITIVITY-2006",
        "title": "Causality, analyticity and an IR obstruction to UV completion",
        "publisher": "Journal of High Energy Physics / arXiv",
        "url": "https://arxiv.org/abs/hep-th/0602178",
        "status": "stable",
        "use": (
            "forward-limit analyticity, unitarity, crossing, subtraction, and "
            "positivity obligations; no UV completion or GMUT proof"
        ),
    },
    {
        "source_id": "KHOURY-WELTMAN-2004",
        "title": "Chameleon fields: Awaiting surprises for tests of gravity in space",
        "publisher": "Physical Review Letters / arXiv",
        "url": "https://arxiv.org/abs/astro-ph/0309300",
        "status": "stable",
        "use": (
            "effective-potential, density, effective-mass, and thin-shell "
            "obligations; no force detection, constraint, or confirmation"
        ),
    },
]


# number, title, slug, pillar, expected disposition, semantic mechanism, source ids
PROPOSAL_ROWS = [
    (
        1,
        "Urban-tree inventory passport with botanical-name claim placeholder, "
        "asset tag, site-zone token, coordinate precision ceiling, management "
        "boundary, revision, collision quarantine, and no-identification rule",
        "tree-inventory-passport",
        "Freed ID and CBR Heart",
        "completed",
        "tree inventory referent, location minimization, revision, and identification refusal",
        ["W3C-PROV-O", "NZ-OPC-PRIVACY-2020", "RFC-8785"],
    ),
    (
        2,
        "Tree inspection episode lattice with crown, stem, root-zone, site, "
        "visible-observation, inaccessible-region, image-reference placeholder, "
        "uncertainty, inference split, and diagnosis refusal",
        "tree-inspection-observation-lattice",
        "THOS Body and Freed ID",
        "completed",
        "tree inspection observation, inaccessible-region, uncertainty, and diagnosis firewall",
        ["WORKSAFE-ARBORICULTURE", "W3C-PROV-O", "NZ-OPC-PRIVACY-2020"],
    ),
    (
        3,
        "Arboriculture work-scope delta graph with baseline intervention, "
        "branch-zone placeholder, dependency edge, quote and duration effect, "
        "expiry, correction readback, unsigned-delta quarantine, and no-work rule",
        "arboriculture-work-scope-delta",
        "THOS Body and CBR Heart",
        "completed",
        "arboriculture work-scope dependency, expiry, correction, and unsigned-change refusal",
        ["W3C-PROV-O", "NZ-HSWA-2015", "RFC-8785"],
    ),
    (
        4,
        "Protected root-zone and utility-conflict map with trunk reference, radial "
        "zone placeholder, utility owner gap, excavation relation, uncertainty, "
        "permit placeholder, conflict hold, and clearance refusal",
        "root-zone-utility-conflict-map",
        "THOS Body and CBR Heart",
        "completed",
        "root-zone geometry, utility conflict, uncertainty, and clearance refusal",
        ["WORKSAFE-TREES-POWER", "NZ-RMA-1991", "NIST-SP811"],
    ),
    (
        5,
        "Pruning-specification intent graph with objective, branch-union "
        "placeholder, retained-crown relation, cut-type vocabulary, seasonal "
        "assumption, review hold, rollback anchor, and physical-pruning refusal",
        "pruning-intent-graph",
        "THOS Body",
        "completed",
        "pruning intent, branch relation, review hold, and physical-operation refusal",
        ["WORKSAFE-ARBORICULTURE", "W3C-PROV-O", "NZ-HSWA-2015"],
    ),
    (
        6,
        "Decay-cavity and diagnostic-instrument measurement proxy with method "
        "placeholder, reference plane, unit, calibration gap, inaccessible zone, "
        "uncertainty, repeat cue, interpretation hold, and real-measurement refusal",
        "tree-decay-measurement-proxy",
        "THOS Body",
        "represented",
        "tree decay measurement method, calibration, uncertainty, and interpretation proxy",
        ["NIST-SP811", "WORKSAFE-ARBORICULTURE"],
    ),
    (
        7,
        "Crown sail-area, wind exposure, stem lever-arm, bending-moment, support, "
        "gust, damping, unit, model-domain, uncertainty, and real-load refusal proxy",
        "tree-wind-load-proxy",
        "THOS Body and GMUT Mind",
        "represented",
        "tree wind-load geometry, force-domain, uncertainty, and real-load proxy",
        ["NIST-SP811", "WORKSAFE-ARBORICULTURE"],
    ),
    (
        8,
        "Climb, rope, anchor, rigging, MEWP, aerial-rescue, second-person, weather, "
        "competence, equipment-inspection, abort, and real-access-operation proxy",
        "tree-access-rescue-proxy",
        "THOS Body",
        "represented",
        "tree access, rigging, rescue, competence, weather, and abort proxy",
        ["WORKSAFE-ARBORICULTURE", "NZ-HSWA-2015"],
    ),
    (
        9,
        "Chainsaw, chipper, stump-grinder, hand-tool, PPE, maintenance, guard, "
        "noise, contamination, authorization, isolation, and real-tool-operation proxy",
        "arboriculture-tooling-proxy",
        "THOS Body",
        "represented",
        "arboriculture tooling, maintenance, authorization, isolation, and operation proxy",
        ["WORKSAFE-ARBORICULTURE", "NZ-HSWA-2015"],
    ),
    (
        10,
        "THOS storm-damage triage and handover map with observation time, unstable "
        "zone placeholder, public exclusion, weather state, unresolved hazard, "
        "priority rationale, pause token, receiver question, and emergency-authority refusal",
        "thos-tree-storm-handover",
        "THOS Body and CBR Heart",
        "completed",
        "storm-damage observation, exclusion, priority rationale, pause, and handover contract",
        ["WORKSAFE-ARBORICULTURE", "W3C-PROV-O", "W3C-WCAG-22"],
    ),
    (
        11,
        "Tree symptom and pest-observation referral board with visible sign, host "
        "claim placeholder, image provenance, distribution uncertainty, hygiene "
        "hold, report route, duplicate report, and diagnosis-treatment refusal",
        "tree-pest-observation-referral",
        "THOS Body and CBR Heart",
        "completed",
        "tree pest symptom observation, reporting, hygiene hold, and diagnosis refusal",
        ["MPI-EXOTIC-PESTS", "NZ-BIOSECURITY-1993", "W3C-PROV-O"],
    ),
    (
        12,
        "Nursery-stock provenance and planting-candidate docket with supplier, lot, "
        "species claim placeholder, root condition, transport interval, substitution, "
        "site-evidence gap, quarantine, and suitability refusal",
        "nursery-stock-provenance-docket",
        "Freed ID and THOS Body",
        "completed",
        "nursery stock provenance, substitution, site-evidence gap, and suitability refusal",
        ["NZ-BIOSECURITY-1993", "MPI-EXOTIC-PESTS", "W3C-PROV-O"],
    ),
    (
        13,
        "Soil, mulch, irrigation, compaction, excavation, and amendment event "
        "lineage with source lot, quantity unit, application zone, weather, "
        "observation cue, conflict, correction, and efficacy refusal",
        "tree-site-intervention-lineage",
        "THOS Body and Freed ID",
        "completed",
        "tree-site intervention provenance, unit, correction, and efficacy refusal",
        ["NIST-SP811", "W3C-PROV-O", "NZ-RMA-1991"],
    ),
    (
        14,
        "Tree-protection-zone survey contract with coordinate reference placeholder, "
        "trunk and canopy referents, radial and polygon forms, unit, precision, "
        "revision, boundary conflict, and legal-boundary refusal",
        "tree-protection-zone-survey",
        "GMUT Mind and CBR Heart",
        "completed",
        "tree-protection coordinate, geometry, precision, revision, and legal-boundary refusal",
        ["NIST-SP811", "NZ-RMA-1991", "RFC-8785"],
    ),
    (
        15,
        "Habitat-feature reservation ledger with nest, roost, cavity, epiphyte, "
        "seasonal presence placeholder, observation provenance, access limit, "
        "ecology-review gap, work hold, and wildlife-decision refusal",
        "tree-habitat-feature-reservation",
        "CBR Heart and THOS Body",
        "completed",
        "tree habitat observation, seasonal uncertainty, ecology-review gap, and work hold",
        ["NZ-RMA-1991", "W3C-PROV-O", "NZ-OPC-PRIVACY-2020"],
    ),
    (
        16,
        "Tree-risk statement decomposition with target placeholder, occupancy "
        "assumption, likelihood and consequence placeholders, time horizon, evidence "
        "source, uncertainty, reviewer gap, and public-safety judgment refusal",
        "tree-risk-claim-decomposition",
        "THOS Body and CBR Heart",
        "completed",
        "tree-risk claim decomposition, uncertainty, review gap, and safety-judgment refusal",
        ["WORKSAFE-ARBORICULTURE", "NZ-HSWA-2015", "W3C-PROV-O"],
    ),
    (
        17,
        "Arboriculture nonconformance and reinspection lineage with planned state, "
        "observed deviation, containment, affected zone, correction option, "
        "reinspection trigger, attribution uncertainty, and release refusal",
        "tree-work-nonconformance-lineage",
        "THOS Body and Freed ID",
        "completed",
        "arboriculture nonconformance, containment, correction, reinspection, and release refusal",
        ["W3C-PROV-O", "NZ-HSWA-2015"],
    ),
    (
        18,
        "Removed limb, wood chip, fruiting body, leaf, soil, and diagnostic sample "
        "custody record with source tree, zone, container, biosecurity hold, return "
        "or disposal placeholder, evidence preservation, and reuse refusal",
        "tree-material-custody-record",
        "THOS Body and CBR Heart",
        "completed",
        "removed tree material custody, biosecurity hold, evidence, and disposal boundary",
        ["NZ-BIOSECURITY-1993", "MPI-EXOTIC-PESTS", "W3C-PROV-O"],
    ),
    (
        19,
        "Arboriculture worksite capacity governor with exclusion zone, pedestrian "
        "and traffic interface, utility gap, crew-role placeholder, rescue coverage, "
        "weather ceiling, concurrent-operation limit, pause, and auto-dispatch prohibition",
        "tree-worksite-capacity-governor",
        "THOS Body",
        "completed",
        "arboriculture worksite interface, capacity, weather, rescue, pause, and dispatch refusal",
        ["WORKSAFE-ARBORICULTURE", "WORKSAFE-TREES-POWER", "NZ-HSWA-2015"],
    ),
    (
        20,
        "Tree-site data minimization map with location precision tiers, owner and "
        "occupant placeholders, public-interest cue, optional-field suppression, "
        "role access, correction, retention decision gap, and privacy-completeness refusal",
        "tree-site-privacy-envelope",
        "CBR Heart and Freed ID",
        "completed",
        "tree-site location necessity, precision minimization, access, correction, and retention boundary",
        ["NZ-OPC-PRIVACY-2020", "NZ-RMA-1991"],
    ),
    (
        21,
        "Tree-observation bitemporal validity tribunal with observed-at, asserted-at, "
        "valid-from, valid-through, supersession relation, retroactive correction, "
        "overlapping-interval quarantine, open-ended interval, and timestamp-proof refusal",
        "tree-observation-bitemporal-validity",
        "Freed ID",
        "completed",
        "tree observation valid time, assertion time, supersession, overlap quarantine, and timestamp refusal",
        ["RFC-8785", "W3C-PROV-O"],
    ),
    (
        22,
        "GMUT forward-limit dispersion and positivity obligation board with "
        "crossing channel, analyticity domain, pole subtraction, contour, "
        "unitarity assumption, EFT cutoff, coefficient sign, and observation firewall",
        "gmut-forward-dispersion-positivity",
        "GMUT Mind",
        "completed",
        "forward-limit dispersion, analyticity, subtraction, positivity, EFT, and observation firewall",
        ["ADAMS-POSITIVITY-2006", "NIST-SP811"],
    ),
    (
        23,
        "GMUT chameleon effective-potential and thin-shell obligation board with "
        "matter density, coupling placeholder, field minimum, effective mass, body "
        "radius, shell fraction, environment, EFT domain, unit, and force-detection firewall",
        "gmut-chameleon-thin-shell",
        "GMUT Mind",
        "completed",
        "chameleon effective potential, density dependence, thin shell, EFT domain, and force firewall",
        ["KHOURY-WELTMAN-2004", "NIST-SP811"],
    ),
    (
        24,
        "Thermo-Psyche van't Hoff osmotic-pressure classifier with solute amount, "
        "solution volume, absolute temperature, gas constant, dilution and activity "
        "domain, unit, correction, and agency-nonconversion barrier",
        "thermo-osmotic-pressure-nonconversion",
        "GMUT Mind and THOS Body",
        "completed",
        "osmotic-pressure variable, dilution domain, activity correction, unit, and agency nonconversion",
        ["NIST-SP811"],
    ),
    (
        25,
        "GMUT ESO Science Archive raw, calibration, processed-product, instrument, "
        "observation, provenance, selection, checksum, covariance, proprietary-state, "
        "query, download, zero-row, and likelihood-refusal adapter",
        "gmut-eso-archive-zero-row-adapter",
        "GMUT Mind",
        "open_gap",
        "ESO archive schema and provenance readiness with zero-row likelihood refusal",
        ["ESO-SCIENCE-ARCHIVE", "W3C-PROV-O", "NIST-SP811"],
    ),
    (
        26,
        "Freed ID synthetic tree-inspection confidence-method profile with method "
        "identifier, assessment subject, evidence reference, score-domain placeholder, "
        "uncertainty band, calibration gap, reviewer gap, proof and status gaps, and nonproduction refusal",
        "freed-id-tree-confidence-method",
        "Freed ID",
        "represented",
        "synthetic tree-inspection confidence method, evidence, uncertainty, calibration, and review profile",
        ["W3C-VC-DM-20", "W3C-PROV-O", "NIST-SP811"],
    ),
    (
        27,
        "CBR tree-work notice, alternative, access, affordability, disability, "
        "location privacy, correction, complaint, remedy, reviewer, and "
        "no-rights-adjudication provenance ledger",
        "cbr-tree-work-remedy-ledger",
        "CBR Heart",
        "completed",
        "tree-work notice, access, correction, complaint, remedy provenance, and rights refusal",
        ["NZ-OPC-PRIVACY-2020", "W3C-WCAG-22", "NZ-RMA-1991"],
    ),
    (
        28,
        "Accessible tree-inspection report and map-alternative audit with heading "
        "hierarchy, feature identifiers, text coordinates, status redundancy, table "
        "fallback, keyboard order, warning relation, and affected-user testing gap",
        "accessible-tree-inspection-report",
        "CBR Heart",
        "completed",
        "tree report structure, map alternative, keyboard order, redundant warnings, and testing reserve",
        ["W3C-WCAG-22", "NZ-OPC-PRIVACY-2020", "NIST-SP811"],
    ),
    (
        29,
        "Stage 20 tree-evidence promotion veto with observation provenance, "
        "sampling frame, calibration gap, absent blinded comparison, model-selection "
        "record, uncertainty, external-review placeholder, claim ceiling, and retained negatives",
        "stage20-tree-evidence-nonpromotion",
        "GMUT Mind, THOS Body, and CBR Heart",
        "completed",
        "tree evidence provenance, sampling, calibration, uncertainty, review, claim ceiling, and nonpromotion",
        ["W3C-PROV-O", "NIST-SP811", "WORKSAFE-ARBORICULTURE"],
    ),
    (
        30,
        "Tree ownership and stewardship, access, public safety, affordability, "
        "privacy, disability, habitat, heritage, land, place names, significant and "
        "taonga species, mātauranga, data governance, tangata whenua, iwi, hapū, "
        "affected-party, legal, cultural, and Māori-authority reservation",
        "tree-rights-authority-reservation",
        "CBR Heart",
        "exact_gate",
        "tree stewardship, land, heritage, habitat, taonga, affected-party, legal, cultural, and Māori-authority reservation",
        ["TMR-PRINCIPLES", "NZ-RMA-1991", "NZ-OPC-PRIVACY-2020", "NZ-BIOSECURITY-1993"],
    ),
]


SKILL_IDEAS = [
    "ghc-family-tree-inventory-boundary",
    "ghc-family-tree-inspection-provenance",
    "ghc-family-arboriculture-work-scope-guard",
    "ghc-family-tree-measurement-proxy",
    "ghc-family-tree-biosecurity-boundary",
    "ghc-family-tree-worksite-handover",
    "ghc-family-tree-record-privacy",
    "ghc-family-tree-report-accessibility",
    "ghc-family-tree-asset-identifier-profile",
    "ghc-family-gmut-observation-firewall",
]


RUNNER_IDEAS = [
    "ghc_family_tree_inventory_boundary.py",
    "ghc_family_tree_inspection_provenance.py",
    "ghc_family_arboriculture_work_scope_guard.py",
    "ghc_family_tree_measurement_proxy.py",
    "ghc_family_tree_biosecurity_boundary.py",
    "ghc_family_tree_worksite_handover.py",
    "ghc_family_tree_record_privacy.py",
    "ghc_family_tree_report_accessibility.py",
    "ghc_family_tree_asset_identifier_profile.py",
    "ghc_family_v655_v5_suite.py",
]


CLEAN_SURFACES = [
    "tree asset, episode, site, and revision vocabulary",
    "observation, inference, diagnosis, and authority separation",
    "coordinate precision, unit, reference, and location minimization",
    "represented measurement, load, access, rescue, and tooling boundaries",
    "pest symptom, biosecurity hold, reporting, and treatment refusal",
    "worksite weather, utility, exclusion, capacity, and handover states",
    "correction, reinspection, complaint, and remedy lineage",
    "manifest coverage, Git-blob identity, and deterministic JSON",
    "failure retention, Method Flow recurrence, and rollback guards",
    "land, habitat, heritage, taonga, legal, cultural, and Māori-authority refusal",
]


def _negative(
    number: int,
    signature: str,
    failed: str,
    recovery: str,
    recurrence_guard: str,
) -> dict:
    return {
        "negative_id": f"V6555-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": recurrence_guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "parallel_startup_probes_timed_out_without_output",
        "The first three parallel memory and archive locator probes exceeded their short wrappers and returned no evidence.",
        "Rerun only isolated scalar probes with an archive-aware startup bound.",
        "Do not bundle first-touch archive and memory probes under a ten-second shell budget.",
    ),
    _negative(
        2,
        "powershell_foreach_output_piped_without_materialization",
        "The first target-path receipt piped directly from a PowerShell foreach block and failed before reading any path.",
        "Materialize loop output into an array before JSON projection.",
        "Never attach a pipeline directly to a PowerShell foreach statement.",
    ),
    _negative(
        3,
        "bundled_git_state_probe_timed_out",
        "A combined branch, head, upstream, and status probe timed out before yielding a complete source-state receipt.",
        "Run branch, head, upstream, cleanliness, and live remote as separate scalar probes.",
        "Keep archive-backed Git lifecycle checks scalar.",
    ),
    _negative(
        4,
        "powershell_revision_expression_corrupted_cat_file_probe",
        "A commit-existence probe used an unquoted revision suffix that PowerShell reinterpreted, so Git returned no existence credit.",
        "Use the already-proven exact HEAD and quote any revision expression passed to Git.",
        "Quote Git revision expressions containing braces or other PowerShell metacharacters.",
    ),
    _negative(
        5,
        "proposal_domain_probe_foreach_pipeline_recurrence",
        "The first semantic-domain title probe repeated the direct foreach-to-pipeline parser fault and produced no novelty evidence.",
        "Materialize every term result before serializing the domain audit.",
        "Apply the foreach materialization guard to all novelty probes, not only path receipts.",
    ),
    _negative(
        6,
        "long_source_inventory_mixed_duplicate_output",
        "The first broad current-phase inventory returned a useful file list but mixed it with a second long filter surface, reducing attribution clarity.",
        "Keep later inventories single-purpose and use exact literal paths for lifecycle evidence.",
        "Do not combine full phase listings with broad repository filters when one narrow inventory is sufficient.",
    ),
    _negative(
        7,
        "powershell_domain_probe_foreach_pipeline_second_recurrence",
        "A later candidate-domain probe again placed a pipeline after foreach and failed before reading the frozen chain.",
        "Use the validated materialized-array form for every remaining semantic query.",
        "Treat compressed loop serialization as banned in this phase.",
    ),
    _negative(
        8,
        "first_x1_novelty_audit_rejected_two_template_overlaps",
        "The first full 2,050-row x1 novelty audit rejected the canonical tree-event snapshot and selective-disclosure tree-asset profile because their semantic skeletons still overlapped Auren surfaces.",
        "Replace the mechanisms with bitemporal validity and VC confidence-method contracts, then rerun only the frozen x1 builder.",
        "When a nearest-neighbour score fails, redesign the state model or standards mechanism rather than renaming its domain nouns.",
    ),
    _negative(
        9,
        "first_focused_x1_test_run_retained_five_stale_assertions",
        "The first focused x1 run executed all eleven tests; five assertions still expected Auren's predecessor anchors, frozen count, negative baseline, Method Flow total, and successor title.",
        "Bind those assertions to the exact v655-v5 source and dynamic current-phase count contract, rebuild, and rerun the focused test once.",
        "After cloning a lifecycle test, audit every explicit hash, cumulative count, owner, phase, and next-route assertion before credit.",
    ),
    _negative(
        10,
        "combined_x1_review_help_status_and_count_probe_timed_out",
        "A combined PowerShell probe invoked the staged-review script with an unsupported help assumption and bundled status and file-count work; the wrapper timed out before yielding review evidence.",
        "Read the review script directly, then run each exact bounded probe separately with its observed interface.",
        "Do not infer argparse support or combine an unknown script invocation with unrelated repository inspection.",
    ),
    _negative(
        11,
        "short_timeout_truncated_staged_review_source_read",
        "The first bounded direct read of the x1 staged-review source exceeded a twenty-second wrapper allowance after returning only its opening section.",
        "Retain the partial read as zero credit and reread the remaining exact line window with a measured sixty-second allowance.",
        "Use line-window reads and the observed startup envelope for repository files on this volume.",
    ),
]
