#!/usr/bin/env python3
"""Frozen x1 planning data for Elaren Kestrel v660-v3.

Eiren Kestrel's immutable v660-v2 data surface supplies compatibility
vocabulary only.  Twenty inherited rows are selected for bounded revalidation
with zero Elaren novelty or completion credit.  Only the twenty new rows below
extend the append-only proposal chain.
"""

from __future__ import annotations

from ghc_family_v660_v2_data import *  # noqa: F401,F403


PHASE = "v660-v3"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6603"
OWNER = "Elaren Kestrel"
PRONOUNS = "they/them"
ROLE = "relational symbiosis-model cartographer and evidence-boundary keeper"
HOPE = (
    "keep every model auditable while real organisms, people, places, and "
    "knowledge remain under competent care and authority"
)
BRANCH = "codex/GHC-Family/elaren-kestrel-v660-v3-full-tools"
PHASE_ROOT = "docs/elaren-kestrel/v660-v3"

SOURCE_OWNER = "Eiren Kestrel"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v660-v2-full-tools"
SOURCE_TAMAR = "718b7282aa5921a405e7576561026f4cd1094e17"
SOURCE_X1 = "ba1589880e23fe0c5c615c4cd1e7d5f47c5fe96b"
SOURCE_EVIDENCE = "6be114325b4d2e31c9d90b7da3c0fa6462bf7107"
SOURCE_CLOSEOUT = SOURCE_EVIDENCE
SOURCE_FINAL = "6608caa62705bffd485e734e9b6a576c99b2862e"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = "69b2e6af050fb7d5431b3ab5e2b7c47cf5b9dcc93fa557e8f06568dc9b330f6f"
SOURCE_RECOVERY_DECLARED_SHA256 = "2bbcdbb1dc9da99df2b60a8f1edf1db604064cb92847eb0fd15f2de3255c7f43"
SOURCE_RECOVERY_OBSERVED_SHA256 = "2bbcbdb1dc9da99df2b60a8f1edf1db604064cb92847eb0fd15f2de3255c7f43"
SOURCE_COMPOSITE_RECEIPT_SHA256 = "95a6b9e49c2a6e1b784db272a45263324e73e7527b859cb1ec2c73c885bf2822"
ACTIVATION_PACKET_SHA256 = "b7328f409910d9dbc0bb80cd55039e2f2ba77ed4c3868bd48ba827072885d9c1"
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3170
SOURCE_SEALED_NEGATIVES = 20056
SOURCE_EXTERNAL_NEGATIVES = 5
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = ACTIVATION_NEGATIVES
SOURCE_OPEN_GAPS = 131
SOURCE_EXACT_GATES = 130
SOURCE_SEALED_METHODS = 6170
SOURCE_EXTERNAL_METHODS = 5
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = ACTIVATION_METHODS
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "bounded synthetic lichenarium curation and collection-informatics records, "
    "morphology topology, imaging provenance, measurement obligations, "
    "taxonomic abstention, locality protection, accessibility, and handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_lichen_fungi_algae_photobionts_specimens_vouchers_types_sequences_slides_reagents_locations_images_measurements_or_collection_records",
    "real_collectors_curators_taxonomists_lichenologists_mycologists_technicians_landholders_communities_affected_parties_and_authorities",
    "real_collection_access_handling_sampling_sectioning_microscopy_chemistry_chromatography_sequencing_identification_publication_transfer_or_disposal",
    "professional_taxonomic_collection_conservation_biosafety_chemical_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "sensitive_locality_disclosure_bioprospecting_traditional_knowledge_and_benefit_sharing",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_naming_nomenclatural_taxonomic_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_takedown_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6602-P{i:03d}" for i in range(1, 21)]


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
        "lichen-packet-identity-capsule",
        "Synthetic lichen packet identity capsule with immutable surrogate label lineage, split-lot accounting, quarantine cause, and accession refusal",
        "completed",
        "Freed ID and CBR Heart",
        "surrogate packet and label identifiers, split-lot lineage, custody events, correction retention, quarantine causes, and accession refusal",
        ["TDWG-DWC-2026", "TDWG-LATIMER-1", "LOC-PREMIS-3", "W3C-PROV"],
    ),
    _proposal(
        "lichen-morphology-incidence-hypergraph",
        "Thallus lobe-isidium-soredium incidence hypergraph with occlusion masks, uncertain edges, and morphology abstention",
        "completed",
        "GMUT Mind and CBR Heart",
        "typed surrogate morphology nodes, hyperedges, occlusion masks, uncertain incidence, contradiction retention, and morphology abstention",
        ["TDWG-DWC-2026", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "lichen-substrate-contact-mosaic",
        "Substrate-contact mosaic separating bark, rock, soil, moss, overlap, detached state, and unsupported ecology inference",
        "completed",
        "GMUT Mind and CBR Heart",
        "surrogate substrate cells, overlap and detached states, provenance, missingness, and a firewall against ecological inference",
        ["TDWG-DWC-2026", "GBIF-SENSITIVE", "W3C-PROV"],
    ),
    _proposal(
        "lichen-multiband-capture-covenant",
        "Cross-polarized ultraviolet and visible-light capture covenant with geometry digest, calibration blanks, derivative lineage, and comparison hold",
        "completed",
        "GMUT Mind and Freed ID",
        "synthetic capture geometry, modality declarations, calibration blanks, derivative lineage, digest checks, and zero-observation comparison holds",
        ["TDWG-AUDUBON", "NIST-SI", "NIST-UNCERTAINTY", "LOC-PREMIS-3"],
    ),
    _proposal(
        "lichen-reflectance-uncertainty-budget",
        "Lichen reflectance bandpass and pigment-proxy uncertainty budget with instrument-response placeholders, covariance, and zero spectra",
        "completed",
        "GMUT Mind",
        "typed bandpass, instrument response, unit, covariance, missingness, zero-spectrum, and no-pigment-inference obligations",
        ["NIST-SI", "NIST-UNCERTAINTY", "TDWG-AUDUBON"],
    ),
    _proposal(
        "lichen-cross-section-observation-grammar",
        "Layer-aware lichen cross-section observation grammar for cortex, photobiont zone, medulla, rhizines, ambiguity, and zero slides",
        "completed",
        "GMUT Mind and CBR Heart",
        "surrogate layer assertions, ambiguity and contradiction states, scale placeholders, zero slides, and diagnostic abstention",
        ["TDWG-DWC-2026", "NIST-SI", "W3C-PROV"],
    ),
    _proposal(
        "lichen-chemistry-authorization-firewall",
        "Chemical spot-test and thin-layer chromatography authorization firewall with reagent hazards, specimen-sacrifice budget, and zero reactions",
        "completed",
        "THOS Body and CBR Heart",
        "synthetic reagent and procedure declarations, destructive-sampling budget, hazard and authority holds, zero reactions, and execution refusal",
        ["W3C-PROV", "LOC-PREMIS-3", "NIST-UNCERTAINTY"],
    ),
    _proposal(
        "lichen-taxon-assertion-braid",
        "Taxon-name assertion braid linking determination event, identifier-competence placeholder, synonym source, confidence, contradiction, and no accepted name",
        "completed",
        "CBR Heart and Freed ID",
        "surrogate determination assertions, name-use sources, competence holds, confidence, contradiction, supersession, and accepted-name abstention",
        ["TDWG-DWC-2026", "IAPT-MADRID-WATCH", "W3C-PROV"],
    ),
    _proposal(
        "lichen-sensitive-locality-transformer",
        "Sensitive-locality disclosure transformer with coordinate coarsening, threat class, purpose binding, revocation, and zero real locations",
        "completed",
        "CBR Heart and Freed ID",
        "surrogate locality classes, coarsening transforms, purpose binding, expiry and revocation, zero real coordinates, and disclosure refusal",
        ["GBIF-SENSITIVE", "TDWG-DWC-2026", "NZ-PRIVACY", "LOCAL-CONTEXTS-TK"],
    ),
    _proposal(
        "lichen-type-status-evidence-escrow",
        "Nomenclatural type-status evidence escrow with protologue anchor, repository assertion, duplicate status, citation conflict, and no type designation",
        "completed",
        "CBR Heart and Freed ID",
        "surrogate protologue and repository assertions, duplicate-status claims, citation conflicts, correction lineage, and no type designation",
        ["IAPT-MADRID-WATCH", "TDWG-DWC-2026", "LOC-PREMIS-3"],
    ),
    _proposal(
        "lichen-microhabitat-bitemporal-dossier",
        "Bitemporal microhabitat weathering dossier separating collection-time claims from later corrections, missingness, and no ecological conclusion",
        "completed",
        "GMUT Mind and CBR Heart",
        "transaction and asserted-event times, surrogate microhabitat fields, correction lineage, missingness, and no ecological conclusion",
        ["TDWG-DWC-2026", "W3C-PROV", "GBIF-SENSITIVE"],
    ),
    _proposal(
        "lichen-microscopy-provenance-lattice",
        "Microscopy scale-and-focus provenance lattice with objective metadata, stage-calibration placeholders, focus-stack lineage, and no diagnostic microscopy",
        "completed",
        "GMUT Mind and Freed ID",
        "synthetic objective and scale metadata, calibration placeholders, focus-stack derivation, ambiguity flags, zero slides, and diagnostic refusal",
        ["NIST-SI", "NIST-UNCERTAINTY", "TDWG-AUDUBON", "W3C-PROV"],
    ),
    _proposal(
        "lichen-barcode-pairing-envelope",
        "Nonproduction fungal and photobiont barcode-pairing envelope with primer declaration, contamination controls, zero sequences, and taxonomy firewall",
        "completed",
        "Freed ID and GMUT Mind",
        "surrogate voucher links, primer and contamination-control declarations, zero sequence material, pairing constraints, and taxonomy abstention",
        ["NCBI-BARCODE", "TDWG-DWC-2026", "W3C-PROV"],
    ),
    _proposal(
        "gmut-symbiosis-exchange-obligations",
        "Typed GMUT symbiosis-exchange obligation system for coupled fields, interface flux, unit consistency, boundary data, and likelihood firewall",
        "completed",
        "GMUT Mind",
        "typed symbolic fungal and photobiont field roles, interface flux, dimensions, boundary conditions, covariance placeholders, and zero-likelihood firewall",
        ["NIST-SI", "NIST-UNCERTAINTY"],
    ),
    _proposal(
        "gmut-lichen-radiative-hydration-proxy",
        "GMUT lichen radiative-hydration response proxy with latent-state identifiability, spectral placeholders, zero coefficients, and empirical abstention",
        "represented",
        "GMUT Mind",
        "symbolic hydration and radiative latent states, identifiability obligations, spectral placeholders, zero coefficients, zero likelihood rows, and empirical abstention",
        ["NIST-SI", "NIST-UNCERTAINTY", "TDWG-AUDUBON"],
    ),
    _proposal(
        "thos-lichenarium-backlog-portrait",
        "THOS lichenarium backlog phase portrait with queue debt, freezer and cabinet dependency placeholders, stop tokens, and zero operators",
        "represented",
        "THOS Body",
        "synthetic intake queues, debt states, storage-dependency placeholders, workload ceilings, stop tokens, escalation clocks, and zero operators",
        ["TDWG-LATIMER-1", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "thos-lichen-determination-card-trial",
        "Blind matched-budget synthetic determination-card protocol comparing topology-first and narrative-first views with sealed scoring and zero participants",
        "represented",
        "THOS Body",
        "future blind matched-budget protocol, randomized synthetic cards, sealed scoring, stop and withdrawal rules, zero participants, and no effectiveness claim",
        ["WCAG22", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "lichen-morphology-access-matrix",
        "Multimodal lichen morphology access matrix reserving tactile diagrams, monochrome keys, speech navigation, language support, and affected-user review",
        "represented",
        "CBR Heart and THOS Body",
        "static multimodal structure and reservations for tactile, monochrome, speech, language, manual, and affected-user evaluation with zero sessions",
        ["WCAG22", "TDWG-AUDUBON", "TE-MANA-RARAUNGA"],
    ),
    _proposal(
        "real-lichen-evidence-vault",
        "Zero-row lichen evidence vault requiring authenticated vouchers, accountable curators, calibrated instruments, governed sampling, and independent taxonomic review",
        "open_gap",
        "All pillars",
        "zero authenticated vouchers, accountable professionals, calibrated observations, governed samples, sequences, outcomes, or independent taxonomic-review rows",
        ["TDWG-DWC-2026", "NIST-UNCERTAINTY", "NCBI-BARCODE", "IAPT-MADRID-WATCH"],
    ),
    _proposal(
        "lichen-knowledge-authority-register",
        "Unoccupied knowledge-authority register for Indigenous names, mātauranga, bioprospecting limits, benefit sharing, takedown, and Māori non-substitution",
        "exact_gate",
        "CBR Heart",
        "unoccupied affected-party, landholder, community, traditional-knowledge, benefit-sharing, takedown, remedy, tangata whenua, iwi, hapū, and Māori-authority reservations",
        ["TE-MANA-RARAUNGA", "LOCAL-CONTEXTS-TK", "NZ-PRIVACY", "W3C-PROV"],
    ),
]

SELF_SAFE_CATEGORIES = [
    "Eiren source head and fresh equality",
    "activation packet and external receipt digests",
    "three-thousand-one-hundred-seventy-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity boundary",
    "bounded Eiren-to-Elaren live override",
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
    {"task_id": f"V6603-SAFE-{i:03d}", "title": f"Validate {name} inside the Elaren-owned v660-v3 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6604-REC-SAFE-{i:03d}", "title": f"Reassess {name} for Neris-only v660-v4", "recipient": "Neris Solane", "completion_credit": 0}
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "lichen packet identity capsule",
    "lichen morphology incidence hypergraph",
    "lichen multiband capture covenant",
    "lichen reflectance uncertainty budget",
    "lichen chemistry authorization firewall",
    "lichen taxon assertion braid",
    "lichen sensitive-locality transformer",
    "lichen microscopy provenance lattice",
    "GMUT symbiosis exchange obligations",
    "lichen knowledge-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6603-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6604-REC-CAND-{i:03d}", "title": f"Consider a distinct Neris-owned refinement of {name}", "recipient": "Neris Solane", "completion_credit": 0}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6603-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate(
        [
            "Access, collect, handle, sample, section, stain, chemically test, sequence, transfer, publish, release, or dispose of any real specimen or material",
            "Make a real taxonomic determination, accepted-name, type-status, synonymy, identification, rarity, locality, ecological, or conservation decision",
            "Use real reagents, chromatography, microscopy, sequencing, storage, biosafety, chemical, occupational, or public-safety systems",
            "Disclose precise sensitive localities, protected knowledge, private records, beneficiary data, or restricted collection information",
            "Make a professional lichenology, mycology, taxonomy, curation, collection-management, conservation, privacy, security, translation, or accessibility determination",
            "Publish a production barcode, repository assertion, identifier, credential, signed statement, proof, or interoperable collection record",
            "Allocate ownership, custody, legal, intellectual-property, bioprospecting, benefit-sharing, takedown, remedy, or beneficiary authority",
            "Make a mātauranga, tikanga, wording, naming, tangata whenua, iwi, hapū, Māori data-governance, or Māori-authority decision",
            "Run a real participant study, operator trial, workplace workflow, professional review, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Elaren-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {"task_id": f"V6603-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
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
    ("ghc-family-lichen-packet-identity", "Preserve surrogate packet, label, split-lot, custody, correction, quarantine, and accession-refusal states."),
    ("ghc-family-lichen-morphology-hypergraph", "Represent typed surrogate morphology incidence, occlusion, ambiguity, contradiction, and abstention."),
    ("ghc-family-lichen-capture-covenant", "Bind synthetic multiband geometry, calibration blanks, derivative lineage, digests, and comparison holds."),
    ("ghc-family-lichen-uncertainty-budget", "Keep bandpass, response, unit, covariance, missingness, zero-row, and inference-firewall obligations typed."),
    ("ghc-family-lichen-sampling-firewall", "Reserve reagent, destructive-sampling, safety, competent-authority, and zero-execution gates."),
    ("ghc-family-lichen-taxonomy-assertion", "Track determination assertions, name sources, confidence, contradiction, correction, and taxonomic abstention."),
    ("ghc-family-lichen-locality-firewall", "Bound coarsening, purpose, expiry, revocation, zero-location, disclosure, and protected-knowledge states."),
    ("ghc-family-gmut-symbiosis-obligations", "Keep coupled-field roles, interface flux, units, covariance, boundary data, and likelihood obligations nonempirical."),
    ("ghc-family-thos-lichenarium-backlog", "Track synthetic queue debt, storage dependencies, workload ceilings, stop tokens, escalation, and zero operators."),
    ("ghc-family-lichen-knowledge-authority", "Reserve Indigenous names, mātauranga, bioprospecting, benefit sharing, remedy, and Māori authority."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": f"ghc-family-neris-v660-v4-recommendation-{i:02d}", "purpose": purpose, "recipient": "Neris Solane", "completion_credit": 0}
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
    ("ghc_family_lichen_packet_identity.py", "lichen-packet-identity-capsule"),
    ("ghc_family_lichen_morphology_hypergraph.py", "lichen-morphology-incidence-hypergraph"),
    ("ghc_family_lichen_capture_covenant.py", "lichen-multiband-capture-covenant"),
    ("ghc_family_lichen_uncertainty_budget.py", "lichen-reflectance-uncertainty-budget"),
    ("ghc_family_lichen_sampling_firewall.py", "lichen-chemistry-authorization-firewall"),
    ("ghc_family_lichen_taxonomy_assertion.py", "lichen-taxon-assertion-braid"),
    ("ghc_family_lichen_locality_firewall.py", "lichen-sensitive-locality-transformer"),
    ("ghc_family_gmut_symbiosis_obligations.py", "gmut-symbiosis-exchange-obligations"),
    ("ghc_family_thos_lichenarium_backlog.py", "thos-lichenarium-backlog-portrait"),
    ("ghc_family_lichen_knowledge_authority.py", "lichen-knowledge-authority-register"),
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": f"ghc_family_neris_v660_v4_recommendation_{i:02d}.py", "purpose": purpose, "recipient": "Neris Solane", "completion_credit": 0}
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
    {"task_id": f"V6603-CLEAN-{i:03d}", "title": f"Review and refine {name}", "state": "planned_x2_additive_only"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6604-REC-CLEAN-{i:03d}", "title": f"Reassess {name} additively in Neris v660-v4", "recipient": "Neris Solane", "completion_credit": 0}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("TDWG-DWC-2026", "official_tdwg_darwin_core", "https://dwc.tdwg.org/list/", "Darwin Core 2026-05-26 vocabulary for synthetic material, occurrence, event, identification, location, and measurement fields only; no real specimen, identification, or publication claim."),
    ("TDWG-LATIMER-1", "official_tdwg_latimer_core", "https://ltc.tdwg.org/", "Latimer Core 1.0 collection-description vocabulary only; no real collection inventory, custody, institutional authority, or interoperability claim."),
    ("TDWG-AUDUBON", "official_tdwg_audiovisual_core", "https://ac.tdwg.org/introduction/2013-10-23", "Biodiversity multimedia metadata vocabulary only; no image authenticity, rights, calibration, diagnosis, or conformance claim."),
    ("GBIF-SENSITIVE", "official_gbif", "https://docs.gbif.org/sensitive-species-best-practices/master/en/", "Sensitive-occurrence generalization and withholding vocabulary only; no real locality, sensitivity, disclosure, legal, or conservation decision."),
    ("IAPT-MADRID-WATCH", "official_iapt", "https://www.iapt-taxon.org/nomen/main.php", "Nomenclatural-code and type vocabulary under a visible 2025 Madrid-Code transition; watch status only and no taxonomic, nomenclatural, or professional determination."),
    ("NCBI-BARCODE", "official_ncbi_genbank", "https://www.ncbi.nlm.nih.gov/genbank/barcode/", "Voucher, primer, trace, locus, sequence-submission, and barcode metadata vocabulary only; zero sequences and no identification or submission claim."),
    ("LOC-PREMIS-3", "official_library_of_congress", "https://www.loc.gov/standards/premis/", "Preservation object, event, agent-placeholder, rights, relationship, fixity, and outcome-detail vocabulary only."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent-placeholder, generation, derivation, revision, invalidation, and qualified-provenance vocabulary only."),
    ("W3C-ANNOTATION", "official_w3c", "https://www.w3.org/TR/annotation-model/", "Annotation body, target, motivation, selector, state, provenance, and lifecycle vocabulary only."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Accessible structure, text-alternative, noncolour, navigation, status, and interaction vocabulary with manual and affected-user evaluation reserved."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/publications/international-system-units-si2019-edition", "SI quantity, unit, symbol, and reporting vocabulary only; no measured specimen or physical result."),
    ("NIST-UNCERTAINTY", "official_nist", "https://www.nist.gov/pml/nist-technical-note-1297/nist-guidelines-evaluating-and-expressing-uncertainty-nist-measurement", "Measurement-model and uncertainty-reporting vocabulary only; no measurement, calibration certificate, or empirical result."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "New Zealand privacy-principle vocabulary only; no legal, compliance, collection, disclosure, or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary only; no Māori authority, ratification, wording, naming, tikanga, or mātauranga claim."),
    ("LOCAL-CONTEXTS-TK", "primary_local_contexts", "https://localcontexts.org/labels/traditional-knowledge-labels/", "Community-defined traditional-knowledge access, use, provenance, permission, and authority-reservation context only; no label is selected or applied."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection and ancestry vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]
SOURCE_STATUS = {
    "TDWG-DWC-2026": "current",
    "TDWG-LATIMER-1": "stable",
    "TDWG-AUDUBON": "stable",
    "GBIF-SENSITIVE": "current",
    "IAPT-MADRID-WATCH": "watch",
    "NCBI-BARCODE": "stable",
    "LOC-PREMIS-3": "stable",
    "W3C-PROV": "stable",
    "W3C-ANNOTATION": "stable",
    "WCAG22": "current",
    "NIST-SI": "stable",
    "NIST-UNCERTAINTY": "stable",
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
    _startup_failure(
        "V6603-X1-N001",
        "broad-source-receipt-digest-search-exceeded-bounded-runtime",
        "Terminate only the exact owner-started search, retain zero credit, and narrow receipt discovery to declared phase and D-first receipt locations.",
    ),
    _startup_failure(
        "V6603-X1-N002",
        "first-inline-source-manifest-replay-lost-python-string-quotes",
        "Retain the SyntaxError and rerun the same read-only manifest dependency through UTF-8 Python standard input.",
    ),
    _startup_failure(
        "V6603-X1-N003",
        "receipt-hash-projection-piped-directly-from-powershell-foreach",
        "Retain the EmptyPipeElement parser fault, materialize rows, and then serialize the bounded receipt projection.",
    ),
    _startup_failure(
        "V6603-X1-N004",
        "declared-source-recovery-digest-does-not-match-only-recovery-file",
        "Retain the declared-versus-observed digest mismatch, verify the recovery content read-only, and classify the cryptographic link as inherited bounded evidence rather than exact parity.",
    ),
    _startup_failure(
        "V6603-X1-N005",
        "first-multi-section-builder-patch-rejected-atomically-on-encoding-sensitive-context",
        "Retain the rejected patch at zero credit and apply bounded ASCII-safe hunks without changing the intended x1 semantics.",
    ),
    _startup_failure(
        "V6603-X1-N006",
        "first-multi-section-x1-test-patch-rejected-atomically-on-encoding-sensitive-context",
        "Retain the rejected patch at zero credit, exclude the encoding-sensitive assertion from the hunk, and apply exact ASCII-safe test updates.",
    ),
    _startup_failure(
        "V6603-X1-N007",
        "first-x1-test-run-found-family-current-receipts-not-yet-materialized",
        "Retain the 21-pass and two-missing-receipt errors at zero credit, run only the declared family-current receipt builders, refresh x1 manifests, and rerun the scoped x1 suite.",
    ),
    _startup_failure(
        "V6603-X1-N008",
        "deliberately-invalid-workflow-route-fixture-was-rejected-by-one-policy-check",
        "Retain the 19-of-20 rejection fixture at zero credit and keep the separately generated terminal-gated Neris route request at 20-of-20.",
    ),
    _startup_failure(
        "V6603-X1-N009",
        "second-x1-test-run-found-the-family-index-receipt-not-yet-materialized",
        "Retain the 22-pass and one-missing-index error at zero credit, run the family-index builder into the phase-local tooling directory, refresh manifests, and rerun the scoped suite.",
    ),
    _startup_failure(
        "V6603-X1-N010",
        "first-index-derived-x1-review-queried-an-absent-privacy-count-key",
        "Retain the KeyError at zero credit, inspect the receipt schema, and use its declared files_scanned field for the read-only review.",
    ),
    _startup_failure(
        "V6603-X1-N011",
        "first-stale-label-scan-treated-selected-inherited-stained-glass-rows-as-current-domain-drift",
        "Retain the 56-candidate false-positive screen at zero credit, require every stained-glass row to remain explicitly selected inherited zero-credit evidence, and scope current-route drift checks to source and route fields.",
    ),
]

# X2 failures may be appended only after the immutable x1 commit is pushed and
# proved clean and four-way equal.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
