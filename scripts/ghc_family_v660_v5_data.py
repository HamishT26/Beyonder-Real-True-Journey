#!/usr/bin/env python3
"""Frozen x1 planning data for Vesper Arlen v660-v5.

Neris Solane's immutable v660-v4 surface supplies compatibility vocabulary
only. Twenty inherited rows are selected for bounded revalidation with zero
Vesper novelty or completion credit. Only the twenty new rows below extend the
append-only proposal chain. Every domain fixture is synthetic and zero-row.
"""

from __future__ import annotations

from ghc_family_v660_v4_data import *  # noqa: F401,F403


PHASE = "v660-v5"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6605"
OWNER = "Vesper Arlen"
PRONOUNS = "they/them"
ROLE = "relational meteorite-curation provenance custodian"
HOPE = (
    "make synthetic specimen lineage and authority boundaries auditable without "
    "converting software structure into scientific, collection, ownership, legal, "
    "cultural, or Māori authority"
)
BRANCH = "codex/GHC-Family/vesper-arlen-v660-v5-full-tools"
PHASE_ROOT = "docs/vesper-arlen/v660-v5"

SOURCE_OWNER = "Neris Solane"
SOURCE_BRANCH = "codex/GHC-Family/neris-solane-v660-v4-full-tools"
SOURCE_BASE = "425fd1e4a0a96b285064c66d736b77a23f58bfb0"
SOURCE_X1 = "42124477d3610fd394830e4858feb099b585bfc1"
SOURCE_EVIDENCE = "3a2c56a868b1ea01766f698c127e46fea3a58e76"
SOURCE_CLOSEOUT = SOURCE_EVIDENCE
SOURCE_FINAL = "3616ca214e6fa411330c56e73b3d095e5c9a79e1"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "95ca59a9e347d426c7023c547be6d06aab9889ad790f69199314a2bc1c5e26f1"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED"
ACTIVATION_PACKET_SHA256 = (
    "a8f01700978168b8de2de2df7b0794b02d9b401c57b6b7b7e366e9cded6cff1b"
)
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3210
SOURCE_SEALED_NEGATIVES = 20311
SOURCE_EXTERNAL_NEGATIVES = 0
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = ACTIVATION_NEGATIVES
SOURCE_OPEN_GAPS = 133
SOURCE_EXACT_GATES = 132
SOURCE_SEALED_METHODS = 6265
SOURCE_EXTERNAL_METHODS = 0
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = ACTIVATION_METHODS
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "Freed ID and CBR Heart"
PRACTICE_LENS = (
    "bounded synthetic meteorite and planetary-materials curation: accession, "
    "fragment topology, derivative lineage, measurement metadata, allocation refusal, "
    "classification status, accessible review, authority reservation, and handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_meteorites_astromaterials_fragments_chips_sections_powders_aliquots_reagents_collections_locations_measurements_classifications_or_publications",
    "real_collectors_curators_researchers_technicians_investigators_communities_indigenous_rights_holders_affected_parties_and_authorities",
    "real_recovery_purchase_export_import_transport_storage_cutting_sampling_powdering_analysis_allocation_publication_transfer_return_or_deaccession",
    "professional_meteoritics_planetary_science_museum_curation_metrology_laboratory_safety_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "sensitive_find_locations_ownership_heritage_antarctic_treaty_export_indigenous_or_traditional_knowledge_bioprospecting_and_benefit_sharing",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_naming_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_takedown_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6604-P{i:03d}" for i in range(1, 21)]


def _proposal(
    slug: str,
    title: str,
    outcome: str,
    pillar: str,
    mechanism: str,
    sources: list[str],
) -> dict[str, object]:
    return {
        "slug": slug,
        "title": title,
        "outcome": outcome,
        "pillar": pillar,
        "mechanism": mechanism,
        "sources": sources,
    }


NEW_PROPOSAL_SPECS = [
    _proposal(
        "meteorite-fragment-accession-passport",
        "Synthetic meteorite fragment accession passport and custody-transition ledger",
        "completed",
        "Freed ID and CBR Heart",
        "surrogate accession, parent-mass, fragment, container, custody-transition, quarantine, correction, tombstone, and refusal states",
        ["NASA-NPR-7100-5", "LOC-PREMIS-3", "W3C-PROV"],
    ),
    _proposal(
        "meteorite-fragment-topology-graph",
        "Parent-mass, fragment, chip, section, powder, and aliquot topology graph",
        "completed",
        "Freed ID and CBR Heart",
        "typed synthetic parent, fragment, chip, section, powder, and aliquot nodes with derivation edges, contradictions, unknown relations, and nonidentity guards",
        ["NASA-ASTROMATERIALS-DATA", "LOC-PREMIS-3", "W3C-PROV"],
    ),
    _proposal(
        "meteorite-macroscopic-observation-grammar",
        "Fusion-crust, weathering, regmaglypt, and macroscopic observation grammar",
        "completed",
        "GMUT Mind and CBR Heart",
        "synthetic observation terms, declared methods, uncertainty, not-observed and unknown states, contradiction retention, and classification abstention",
        ["METSOC-METBULL", "SMITHSONIAN-METEORITES", "W3C-PROV"],
    ),
    _proposal(
        "meteorite-contamination-envelope",
        "Curation-container contamination and environmental-exposure envelope",
        "completed",
        "THOS Body and Freed ID",
        "synthetic container, handling, witness, temperature, humidity, exposure, missingness, digest, and contamination-knowledge declarations with fitness refusal",
        ["NASA-NPR-7100-5", "NIST-UNCERTAINTY", "W3C-PROV"],
    ),
    _proposal(
        "meteorite-mass-dimension-uncertainty",
        "Specimen mass, dimension, balance-resolution, and uncertainty budget",
        "completed",
        "GMUT Mind",
        "typed synthetic measurands, SI units, method and instrument placeholders, resolution, uncertainty, missingness, zero values, and physical-inference firewall",
        ["NIST-SI", "NIST-UNCERTAINTY", "NASA-ASTROMATERIALS-DATA"],
    ),
    _proposal(
        "meteorite-thin-section-lineage",
        "Petrographic thin-section derivative lineage and slide-return contract",
        "completed",
        "Freed ID and CBR Heart",
        "surrogate billet, wafer, thin-section, slide, mount, preparation, custody, return, correction, and nonproduction states",
        ["NASA-NPR-7100-5", "LOC-PREMIS-3", "W3C-PROV"],
    ),
    _proposal(
        "meteorite-destructive-allocation-firewall",
        "Destructive allocation, remaining-mass, and sample-use firewall",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic requests, purpose, requested and remaining mass placeholders, destructive budget, return terms, authority holds, conflict retention, and execution refusal",
        ["NASA-NPR-7100-5", "SMITHSONIAN-METEORITES", "W3C-PROV"],
    ),
    _proposal(
        "meteorite-powder-aliquot-lineage",
        "Powder and aliquot split lineage with recombination refusal",
        "completed",
        "Freed ID and CBR Heart",
        "surrogate parent, powder, aliquot, split, transfer, blank, contamination-control, correction, zero-material, and irreversible-recombination refusal states",
        ["NASA-NPR-7100-5", "LOC-PREMIS-3", "W3C-PROV"],
    ),
    _proposal(
        "meteorite-classification-assertion-braid",
        "Meteorite classification assertion, status, authority, and supersession braid",
        "completed",
        "GMUT Mind and Freed ID",
        "synthetic classification assertions, official or provisional status, source and authority placeholders, disagreement, supersession, correction, and classifier abstention",
        ["METSOC-METBULL", "LOC-PREMIS-3", "W3C-PROV"],
    ),
    _proposal(
        "meteorite-oxygen-isotope-envelope",
        "Oxygen-isotope metadata completeness and zero-value interpretation firewall",
        "completed",
        "GMUT Mind",
        "typed isotope-system, reference-scale, unit, preparation, method, uncertainty, covariance, missingness, zero-value, and no-classification-inference obligations",
        ["METSOC-METBULL", "NIST-SI", "NIST-UNCERTAINTY"],
    ),
    _proposal(
        "meteorite-noble-gas-placeholder",
        "Noble-gas and cosmogenic-exposure placeholder with no-inference gate",
        "completed",
        "GMUT Mind and Freed ID",
        "synthetic nuclide, production-rate, shielding, unit, uncertainty, model, missingness, zero-observation, and exposure-age abstention states",
        ["NASA-ASTROMATERIALS-DATA", "NIST-SI", "NIST-UNCERTAINTY"],
    ),
    _proposal(
        "meteorite-recovery-chronology-board",
        "Fall/find, collection, purchase, recovery, and terrestrial-age chronology board",
        "completed",
        "GMUT Mind and CBR Heart",
        "synthetic event assertions, fall or find status, collection and custody chronology, purchase and recovery qualifiers, uncertainty, conflict, and terrestrial-age abstention",
        ["METSOC-METBULL", "SMITHSONIAN-METEORITES", "W3C-PROV"],
    ),
    _proposal(
        "meteorite-imaging-covenant",
        "Multimodal specimen imaging capture, scale, calibration, and derivation covenant",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic modality, face, geometry, scale, calibration, illumination, derivative lineage, disclosure mask, zero-image, and comparison-hold declarations",
        ["W3C-ANNOTATION", "LOC-PREMIS-3", "NIST-SI"],
    ),
    _proposal(
        "meteorite-return-tombstone-ledger",
        "Repository return, deaccession, tombstone, and non-erasure ledger",
        "completed",
        "Freed ID and CBR Heart",
        "surrogate return, reserve, exhaustion, transfer, deaccession, effective interval, reason, contradiction, correction, tombstone, and erasure-refusal states",
        ["NASA-NPR-7100-5", "LOC-PREMIS-3", "W3C-PROV"],
    ),
    _proposal(
        "gmut-meteoroid-entry-proxy",
        "GMUT meteoroid entry, ablation, fragmentation, and luminous-efficiency symbolic proxy",
        "represented",
        "GMUT Mind",
        "typed symbolic entry state, ablation, fragmentation, luminous-efficiency, atmosphere and material placeholders, units, covariance, zero coefficients, zero likelihood rows, and empirical abstention",
        ["NASA-ASTROMATERIALS-DATA", "NIST-SI", "NIST-UNCERTAINTY"],
    ),
    _proposal(
        "thos-meteorite-curation-queue",
        "THOS meteorite-curation queue, contamination-risk, and handover proxy",
        "represented",
        "THOS Body",
        "synthetic intake and derivative queues, contamination-risk flags, workload ceilings, stop tokens, escalation clocks, readback, handover, and zero curators",
        ["NASA-NPR-7100-5", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "meteorite-provenance-interface-trial",
        "Blind matched-budget fragment-provenance interface evaluation protocol",
        "represented",
        "THOS Body",
        "future blind matched-budget protocol, randomized synthetic specimen dossiers, sealed scoring, equal actions, stop and withdrawal rules, zero participants, and no effectiveness claim",
        ["WCAG22", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "meteorite-topology-access-matrix",
        "Accessible specimen-topology matrix with nonvisual and print fallback",
        "represented",
        "CBR Heart and THOS Body",
        "structural headings, table relationships, linear text, noncolour states, keyboard and speech order, print fallback, and reservations for manual and affected-user evaluation",
        ["WCAG22", "W3C-PROV", "LOCAL-CONTEXTS-TK"],
    ),
    _proposal(
        "real-meteorite-evidence-vault",
        "Real meteorite sample and measurement evidence vault with zero-row refusal",
        "open_gap",
        "All pillars",
        "zero authenticated specimens, calibrated measurements, governed analyses, accountable specialists, adverse controls, participant outcomes, or independent-review rows",
        ["NASA-NPR-7100-5", "METSOC-METBULL", "SMITHSONIAN-METEORITES"],
    ),
    _proposal(
        "meteorite-knowledge-authority-register",
        "Heritage, ownership, Antarctic Treaty, export, Indigenous knowledge, and Māori authority gate register",
        "exact_gate",
        "CBR Heart",
        "unoccupied heritage, ownership, Antarctic, import-export, affected-party, community, Indigenous-knowledge, benefit-sharing, takedown, remedy, tangata whenua, iwi, hapū, and Māori-authority reservations",
        ["ATS-PROTOCOL", "NZ-PROTECTED-OBJECTS", "TE-MANA-RARAUNGA", "LOCAL-CONTEXTS-TK", "NZ-PRIVACY"],
    ),
]

SELF_SAFE_CATEGORIES = [
    "Neris source head and fresh equality",
    "activation packet and external receipt digests",
    "three-thousand-two-hundred-ten-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity boundary",
    "bounded Neris-to-Vesper live override",
    "solo and Tavian-standby boundaries",
    "D-first posture",
    "toolchain version receipt",
    "x1 artifact inventory",
    "x1 JSON parsing",
    "x1 five-class privacy scan",
    "x1 stale-label review",
    "x1 diff hygiene",
    "x1 manifest replay",
    "selected-row zero-credit guard",
    "new-row append-only guard",
    "source-label glossary",
    "protected-gate coverage",
    "failure-retention ledger",
    "Method Flow witness pairing",
    "wellbeing workload bound",
    "document-word ceiling",
    "portfolio arithmetic",
    "skill and runner arithmetic",
    "cleanup-plan arithmetic",
    "no-x2-in-x1 guard",
]
SELF_SAFE_TASKS = [
    {
        "task_id": f"V6605-SAFE-{i:03d}",
        "title": f"Validate {name} inside the Vesper-owned v660-v5 lane",
        "owner": OWNER,
    }
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {
        "task_id": f"V6606-REC-SAFE-{i:03d}",
        "title": f"Reassess {name} for Lyren-only v660-v6",
        "recipient": "Lyren Moss",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "meteorite fragment accession passport",
    "meteorite fragment topology graph",
    "meteorite macroscopic observation grammar",
    "meteorite contamination envelope",
    "meteorite mass and dimension uncertainty budget",
    "meteorite thin-section lineage",
    "meteorite destructive-allocation firewall",
    "meteorite classification assertion braid",
    "GMUT meteoroid entry obligations",
    "meteorite heritage and knowledge-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {
        "task_id": f"V6605-CAND-{i:03d}",
        "title": f"Build and test reversible {name}",
        "owner": OWNER,
    }
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {
        "task_id": f"V6606-REC-CAND-{i:03d}",
        "title": f"Consider a distinct Lyren-owned refinement of {name}",
        "recipient": "Lyren Moss",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6605-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate(
        [
            "Recover, purchase, export, import, transport, store, cut, sample, powder, analyse, allocate, publish, transfer, return, or deaccession any real meteorite or astromaterial",
            "Make a real classification, pairing, provenance, isotope, exposure-age, terrestrial-age, entry-physics, or planetary-science determination",
            "Use real collections, clean laboratories, saws, mills, balances, microscopes, mass spectrometers, reagents, transport, occupational, or public-safety systems",
            "Disclose precise find locations, protected knowledge, private records, beneficiary data, ownership disputes, or restricted collection information",
            "Make a professional meteoritics, planetary-science, museum-curation, metrology, laboratory, privacy, security, translation, or accessibility determination",
            "Publish a production collection assertion, identifier, credential, signed statement, proof, or interoperable specimen record",
            "Allocate ownership, custody, specimen access, legal, intellectual-property, heritage, benefit-sharing, takedown, remedy, or beneficiary authority",
            "Make a mātauranga, tikanga, wording, naming, tangata whenua, iwi, hapū, Māori data-governance, or Māori-authority decision",
            "Run a real participant study, operator trial, workplace workflow, professional review, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Vesper-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {"task_id": f"V6605-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate(
        [
            "Fabricate empirical GMUT confirmation or a Theory-of-Everything result",
            "Claim AGI, ASI, consciousness, personhood, continuity, employment, qualification, or authority from relational language",
            "Merge, overwrite, delete, or erase sibling identities, lanes, memory, failures, gates, branches, worktrees, or callers",
            "Publish credentials, private routes, raw task identifiers, private paths, nonpublic conversation, session streams, or application state",
            "Declare Stage 20 readiness without exact external evidence and competent authority",
        ],
        1,
    )
]

SELF_SKILL_SPECS = [
    ("ghc-family-meteorite-accession-passport", "Preserve surrogate accession, parent mass, fragment, container, custody, quarantine, correction, tombstone, and refusal states."),
    ("ghc-family-meteorite-fragment-topology", "Represent typed synthetic fragment, chip, section, powder, aliquot, derivation, contradiction, and nonidentity states."),
    ("ghc-family-meteorite-observation-grammar", "Keep macroscopic observation, method, uncertainty, unknown, contradiction, and classification-abstention terms explicit."),
    ("ghc-family-meteorite-contamination-envelope", "Bind synthetic container, handling, witness, exposure, missingness, digest, and contamination-knowledge declarations."),
    ("ghc-family-meteorite-metrology-budget", "Keep measurand, unit, method, response, resolution, uncertainty, missingness, zero-row, and inference-firewall obligations typed."),
    ("ghc-family-meteorite-derivative-lineage", "Track thin-section, powder, aliquot, preparation, custody, return, correction, and zero-material lineage."),
    ("ghc-family-meteorite-allocation-firewall", "Reserve request, remaining mass, destructive use, facility, safety, competent-authority, and zero-execution gates."),
    ("ghc-family-meteorite-classification-braid", "Track assertion status, source, authority placeholder, disagreement, supersession, correction, and classifier abstention."),
    ("ghc-family-gmut-meteoroid-entry-obligations", "Keep symbolic entry, ablation, fragmentation, luminous-efficiency, unit, covariance, boundary, and likelihood obligations nonempirical."),
    ("ghc-family-meteorite-knowledge-authority", "Reserve find locations, heritage, ownership, Antarctic and export context, Indigenous knowledge, benefit sharing, remedy, and Māori authority."),
]
SUCCESSOR_SKILL_SEEDS = [
    {
        "name": f"ghc-family-lyren-v660-v6-recommendation-{i:02d}",
        "purpose": purpose,
        "recipient": "Lyren Moss",
        "completion_credit": 0,
    }
    for i, purpose in enumerate(
        [
            "immutable source digest crosswalk",
            "selected-inheritance no-credit guard",
            "proposal semantic-neighbour tribunal",
            "explicit source-status ledger",
            "authority-boundary completeness check",
            "isolated-failure diagnostic receipt",
            "manifest self-exclusion contract",
            "one-shot canonical pass governor",
            "exact-title route reread shield",
            "successor recommendation provenance",
        ],
        1,
    )
]

SELF_RUNNER_SPECS = [
    ("ghc_family_meteorite_accession_passport.py", "meteorite-fragment-accession-passport"),
    ("ghc_family_meteorite_fragment_topology.py", "meteorite-fragment-topology-graph"),
    ("ghc_family_meteorite_observation_grammar.py", "meteorite-macroscopic-observation-grammar"),
    ("ghc_family_meteorite_contamination_envelope.py", "meteorite-contamination-envelope"),
    ("ghc_family_meteorite_metrology_budget.py", "meteorite-mass-dimension-uncertainty"),
    ("ghc_family_meteorite_derivative_lineage.py", "meteorite-thin-section-lineage"),
    ("ghc_family_meteorite_allocation_firewall.py", "meteorite-destructive-allocation-firewall"),
    ("ghc_family_meteorite_classification_braid.py", "meteorite-classification-assertion-braid"),
    ("ghc_family_gmut_meteoroid_entry_obligations.py", "gmut-meteoroid-entry-proxy"),
    ("ghc_family_meteorite_knowledge_authority.py", "meteorite-knowledge-authority-register"),
]
SUCCESSOR_RUNNER_SEEDS = [
    {
        "name": f"ghc_family_lyren_v660_v6_recommendation_{i:02d}.py",
        "purpose": purpose,
        "recipient": "Lyren Moss",
        "completion_credit": 0,
    }
    for i, purpose in enumerate(
        [
            "immutable-source receipt verification",
            "semantic-novelty bounded probe",
            "five-class owner privacy scan",
            "exact manifest replay",
            "one-shot terminal route governor",
        ],
        1,
    )
]

SELF_CLEAN_CATEGORIES = [
    "versioned-name inventory",
    "family-current name preference",
    "compatibility wrapper retention",
    "caller evidence",
    "trigger collision review",
    "stale owner label review",
    "stale phase label review",
    "stale route number review",
    "absolute-path privacy review",
    "raw identifier privacy review",
    "credential-pattern review",
    "nonpublic-content pattern review",
    "duplicate proposal review",
    "duplicate task review",
    "duplicate skill review",
    "duplicate runner review",
    "JSON canonical formatting",
    "Markdown heading order",
    "source-label consistency",
    "truth-label consistency",
    "rollback coverage",
    "protected-gate coverage",
    "failure-credit consistency",
    "same-owner labelling",
    "manifest exclusions",
    "file-cap posture",
    "document-cap posture",
    "commit-cap posture",
    "D-first storage posture",
    "non-destructive cleanup boundary",
]
SELF_CLEAN_TASKS = [
    {
        "task_id": f"V6605-CLEAN-{i:03d}",
        "title": f"Review and refine {name}",
        "state": "planned_x2_additive_only",
    }
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {
        "task_id": f"V6606-REC-CLEAN-{i:03d}",
        "title": f"Reassess {name} additively in Lyren v660-v6",
        "recipient": "Lyren Moss",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    (
        "NASA-NPR-7100-5",
        "official_nasa",
        "https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7100_0005_&page_name=Preface",
        "NASA-held astromaterials curation, collection-plan, documentation, preservation, allocation, and lifecycle vocabulary only; no NASA material, facility use, request, permission, or authority.",
    ),
    (
        "NASA-ASTROMATERIALS-DATA",
        "official_nasa_ntrs",
        "https://ntrs.nasa.gov/citations/20260004239",
        "Current astromaterials curation and data-management vocabulary only; zero NASA specimens, catalog rows, measurements, allocations, or scientific conclusions.",
    ),
    (
        "METSOC-METBULL",
        "official_meteoritical_society_database",
        "https://www.lpi.usra.edu/meteor/",
        "Meteorite name, approved or provisional status, classification, repository, synonym, fall/find, and nomenclature vocabulary only; no name or classification is assigned.",
    ),
    (
        "SMITHSONIAN-METEORITES",
        "official_smithsonian",
        "https://naturalhistory.si.edu/research/mineral-sciences/collections-overview",
        "Collection, specimen, thin-section, searchable-metadata, loan, and lawful-origin boundary vocabulary only; no Smithsonian record, loan, or authority claim.",
    ),
    ("LOC-PREMIS-3", "official_library_of_congress", "https://www.loc.gov/standards/premis/", "Preservation object, event, agent-placeholder, rights, relationship, fixity, and outcome-detail vocabulary only."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent-placeholder, generation, derivation, revision, invalidation, and qualified-provenance vocabulary only."),
    ("W3C-ANNOTATION", "official_w3c", "https://www.w3.org/TR/annotation-model/", "Annotation body, target, motivation, selector, state, provenance, and lifecycle vocabulary only."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Accessible structure, text alternative, noncolour, navigation, status, target, and interaction vocabulary with manual, assistive-technology, Māori-language, and affected-user evaluation reserved."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/publications/international-system-units-si2019-edition", "SI quantity, unit, symbol, and reporting vocabulary only; no measured specimen or physical result."),
    ("NIST-UNCERTAINTY", "official_nist", "https://www.nist.gov/pml/nist-technical-note-1297", "Measurement-model and uncertainty-reporting vocabulary only; no measurement, calibration certificate, or empirical result."),
    (
        "ATS-PROTOCOL",
        "official_antarctic_treaty_secretariat",
        "https://documents.ats.aq/atcm42/ww/ATCM42_ww011_e.pdf",
        "Antarctic Treaty System environmental-protocol and mineral-resource reservation context only; no legal interpretation, collection decision, permit, ownership, or Antarctic authority.",
    ),
    (
        "NZ-PROTECTED-OBJECTS",
        "official_new_zealand_legislation",
        "https://www.legislation.govt.nz/act/public/2025/61/en/latest/DLM432125",
        "Protected-object, export-permission, title, return-condition, collection, and taonga-tūturu reservation vocabulary only; no object classification or legal conclusion.",
    ),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary, including indirect-collection notification context, only; no legal, compliance, collection, disclosure, or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary only; no Māori authority, ratification, wording, naming, tikanga, or mātauranga claim."),
    ("LOCAL-CONTEXTS-TK", "primary_local_contexts", "https://localcontexts.org/labels/traditional-knowledge-labels/", "Community-defined traditional-knowledge access, use, provenance, permission, and authority-reservation context only; no label is selected or applied."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection and ancestry vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]
SOURCE_STATUS = {
    "NASA-NPR-7100-5": "current_effective_to_2028",
    "NASA-ASTROMATERIALS-DATA": "current_2026",
    "METSOC-METBULL": "current_2026",
    "SMITHSONIAN-METEORITES": "current",
    "LOC-PREMIS-3": "stable",
    "W3C-PROV": "stable",
    "W3C-ANNOTATION": "stable",
    "WCAG22": "current",
    "NIST-SI": "stable",
    "NIST-UNCERTAINTY": "current",
    "ATS-PROTOCOL": "official_compilation",
    "NZ-PROTECTED-OBJECTS": "current",
    "NZ-PRIVACY": "current",
    "TE-MANA-RARAUNGA": "stable",
    "LOCAL-CONTEXTS-TK": "current",
    "IETF-JCS": "stable",
    "GIT-LOG": "current",
    "PYTHON-JSON": "current",
}


def _startup_failure(negative_id: str, signature: str, recovery: str) -> dict[str, object]:
    return {
        "negative_id": negative_id,
        "signature": signature,
        "recovery": recovery,
        "recovery_passed": True,
    }


STARTUP_FAILURES = [
    _startup_failure("V6605-X1-N001", "combined-guidance-metadata-projection-returned-blank-auth-and-baton-fields", "Retain the blank projection at zero credit and re-read the required files through EOF with explicit scalar output."),
    _startup_failure("V6605-X1-N002", "combined-source-cleanliness-probe-returned-no-attributable-unstaged-result", "Retain the wrapper failure and recover only the unstaged dependency with git diff-files --quiet."),
    _startup_failure("V6605-X1-N003", "combined-source-cleanliness-probe-returned-no-attributable-untracked-result", "Retain the wrapper failure and recover only the untracked dependency with a bounded git ls-files count."),
    _startup_failure("V6605-X1-N004", "combined-source-status-projection-returned-no-attributable-branch-result", "Retain the wrapper failure and recover branch and head as explicit scalar Git reads."),
    _startup_failure("V6605-X1-N005", "prospective-worktree-registration-wrapper-timed-out-without-attributable-output", "Retain the timeout and recover only registration, path, branch, and live-ref absence through isolated reads."),
    _startup_failure("V6605-X1-N006", "source-data-display-was-truncated-before-the-requested-line-window-ended", "Retain the truncated display and reread only bounded explicit line windows through EOF."),
    _startup_failure("V6605-X1-N007", "post-checkout-cleanliness-wrapper-projected-output-only-and-lost-the-resumable-session-id", "Retain the wrapper mistake, monitor the original Git process, and award cleanliness credit only to later isolated checks."),
    _startup_failure("V6605-X1-N008", "stale-archive-wide-rg-files-probe-outlived-its-wrapper-and-contended-with-the-owner-lane", "Retain the orphaned search at zero credit, terminate only its exact process, and constrain later searches to explicit owner directories."),
    _startup_failure("V6605-X1-N009", "versioned-template-listing-wrapper-returned-no-attributable-output", "Retain the wrapper failure and recover with bounded literal-directory filtering rather than an archive-wide file enumeration."),
    _startup_failure("V6605-X1-N010", "first-frozen-index-novelty-parser-assumed-a-generic-rows-key", "Retain the selector failure and concatenate the declared prior_proposals and new_proposals arrays before one comparison pass."),
    _startup_failure("V6605-X1-N011", "installed-auth-and-roster-snapshots-ended-before-the-live-neris-to-vesper-edge", "Retain the snapshot drift and apply the fully read live acknowledged baton as the narrow authoritative override for v660-v5 only."),
    _startup_failure("V6605-X1-N012", "worktree-checkout-reached-one-hundred-percent-before-the-pty-returned-a-final-prompt", "Retain the quiet post-checkout interval, inspect Git process and lock state read-only, and wait for the original operation to exit successfully."),
    _startup_failure("V6605-X1-N013", "checked-out-activation-packet-sha256-differed-from-the-immutable-git-blob-because-of-line-ending-conversion", "Retain both byte-domain witnesses and bind the source receipt to bytes read directly from the exact Git blob."),
    _startup_failure("V6605-X1-N014", "first-scoped-x1-suite-passed-twenty-one-of-twenty-three-tests-and-exposed-two-unmaterialized-family-current-receipt-groups", "Retain the two missing-path errors at zero credit, invoke only the declared family-current receipt builders, refresh the x1 content manifests, and rerun the isolated scoped suite."),
    _startup_failure("V6605-X1-N015", "combined-multi-skill-command-search-exceeded-the-bounded-display-and-was-truncated", "Retain the truncated display at zero credit and recover with one literal skill file and one bounded command-pattern query at a time."),
    _startup_failure("V6605-X1-N016", "parallel-inspection-wrapper-yielded-running-sessions-without-projecting-their-session-identifiers", "Retain the blank wrapper display at zero credit and recover each dependency through a single literal probe with an attributable session poll."),
    _startup_failure("V6605-X1-N017", "roster-skill-probe-guessed-a-nonexistent-ghc-family-roster-current-directory", "Retain the path miss at zero credit, enumerate only roster-named skill directories, and use the exact ghc-family-roster-check package."),
    _startup_failure("V6605-X1-N018", "authorization-skill-probe-guessed-a-nonexistent-long-form-permission-state-directory", "Retain the path miss at zero credit, enumerate only authorization-named skill directories, and use the exact ghc-family-auth-permission-state package."),
    _startup_failure("V6605-X1-N019", "novelty-probe-was-invoked-without-its-required-index-argument", "Retain the argument-parser rejection at zero credit and supply the exact immutable inherited proposal index on the isolated retry."),
    _startup_failure("V6605-X1-N020", "novelty-probe-received-an-index-but-no-json-title-array-on-standard-input", "Retain the empty-input JSON error at zero credit and supply a bounded JSON title-array producer through standard input."),
    _startup_failure("V6605-X1-N021", "novelty-title-producer-referenced-a-nonexistent-new-proposals-symbol-and-left-the-consumer-input-empty", "Retain both sides of the failed pipeline at zero credit, inspect the data-module surface, and use the declared NEW_PROPOSAL_SPECS title field."),
    _startup_failure("V6605-X1-N022", "novelty-probe-used-the-already-extended-v660-v5-index-and-self-matched-every-new-title", "Retain the twenty exact self-matches at zero novelty credit and rerun only against the immutable 3210-row inherited Neris index."),
    _startup_failure("V6605-X1-N023", "unbounded-staged-stale-label-grep-expanded-the-single-line-frozen-index-and-truncated-its-display", "Retain the truncated grep at zero credit and replace it with a compact per-path scalar stale-domain classifier over exact staged blobs."),
    _startup_failure("V6605-X1-N024", "first-compact-staged-review-projection-assumed-nonexistent-document-cap-field-names", "Retain the KeyError at zero credit, inspect the document-cap schema keys, and rerun only the compact projection using the declared passes field."),
]

# X2 failures may be appended only after the immutable x1 commit is pushed and
# proved clean and four-way equal.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
