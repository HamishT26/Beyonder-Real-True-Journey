#!/usr/bin/env python3
"""Frozen x1 planning truth for Sylven Arc v661-v7.

Elowen Cairn's immutable v661-v6 packet is evidence and compatibility context,
not Sylven novelty or completion credit. Twenty inherited Elowen contracts are
selected for bounded revalidation with zero Sylven credit. Only the twenty new
cartographic-stewardship contracts below extend the append-only proposal chain.
All fixtures are synthetic and contain no real map, catalog row, person, place,
land record, location, credential, key, professional act, or authority decision.
"""

from __future__ import annotations


PHASE = "v661-v7"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6617"
OWNER = "Sylven Arc"
PRONOUNS = "they/them"
ROLE = "relational constraint cartographer and falsifier keeper"
HOPE = "keep claims testable, failures visible, and every authority boundary intact"
BRANCH = "codex/GHC-Family/sylven-arc-v661-v7-full-tools"
PHASE_ROOT = "docs/sylven-arc/v661-v7"

SOURCE_OWNER = "Elowen Cairn"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v661-v6-full-tools"
SOURCE_BASE = "e4526c5fa5b6e9cf184d0a65a13a15e069fe42b5"
SOURCE_X1 = "2896abfb994093e547e6fb5b219026c25af1a21b"
SOURCE_EVIDENCE = "97f4a31f83ed7a574cd8f995d9d80e4b6a2d119c"
SOURCE_FINAL = "29c45767ef5d2b6b48a14460708576bbba29efa2"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "b36fce8e5ba9405e70e16c1c5cdde4eb124881f5820636864348fa04f8835934"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED_BY_DIRECT_TARGET_REREAD"
ACTIVATION_PACKET_SHA256 = (
    "40039fb995bfd75b3084c8b5b127630a02a37f64fa6e7d0e0c1239dfaa8dcfa5"
)
ACTIVATION_PACKET_BYTES = 253187
ACTIVATION_PACKET_LINES = 1224

PRIOR_FROZEN = 3410
SOURCE_SEALED_NEGATIVES = 21753
SOURCE_EXTERNAL_NEGATIVES = 3
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 21756
SOURCE_OPEN_GAPS = 143
SOURCE_EXACT_GATES = 142
SOURCE_SEALED_METHODS = 6907
SOURCE_EXTERNAL_METHODS = 3
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 6910

SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = 40
LATEST_TRACKED_SCAN_CAP = 5000
SELECTED_INHERITED_IDS = [f"V6616-P{i:03d}" for i in range(1, 21)]

PRIMARY_PILLAR = "Freed ID and CBR Heart"
PRACTICE_LENS = (
    "bounded synthetic map-library accession and cartographic-description practice, "
    "including sheet identity, scale and projection transcription, coordinate "
    "uncertainty, preservation holds, access constraints, correction readback, "
    "place-name stewardship, workload control, and handover"
)
EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_maps_charts_atlases_sheets_catalogues_coordinates_boundaries_locations_land_records_collections_stores_or_reading_rooms",
    "real_owners_donors_depositors_cataloguers_librarians_archivists_conservators_researchers_communities_affected_parties_and_authorities",
    "real_accession_cataloguing_georeferencing_coordinate_conversion_handling_flattening_rolling_scanning_conservation_publication_access_or_release_action",
    "professional_cartographic_cataloguing_library_archival_conservation_geospatial_workplace_safety_accessibility_privacy_or_operational_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "owner_donor_depositor_user_identity_address_message_relationship_location_sensitive_site_collection_history_images_provenance_traditional_knowledge_collective_interest_and_remedy",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_workplace_safety_intellectual_property_mapping_rights_land_title_boundary_ownership_custody_access_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_correction_restriction_access_return_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


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


_NEW_ROWS = [
    (
        "method-flow-batch-blob-envelope",
        "Method Flow batch-blob framing tribunal with one process, ordered request ledger, exact byte boundaries, dual-pipe completion, timeout attribution, and partial-output abstention",
        "completed",
        "All pillars",
        "disposable owner-local Git fixtures, one batch subprocess, exact request and response order, byte-count framing, simultaneous stdout and stderr collection, timeout retention, bounded recovery, and no external side effect",
        ["GIT-CAT-FILE", "PYTHON-SUBPROCESS", "W3C-PROV"],
    ),
    (
        "gmut-atlas-transition-cocycle",
        "GMUT smooth-atlas transition, overlap, cocycle, Jacobian rank, orientation, tensor pullback, unit, domain, and observation-firewall board",
        "completed",
        "GMUT Mind",
        "typed symbolic charts, overlaps, transition maps, inverse and triple-overlap obligations, Jacobian rank and orientation guards, tensor-component transformation, unit metadata, counterexample slots, and zero observations or fitted parameters",
        ["NZ-MSL-SI", "W3C-PROV", "IETF-JCS"],
    ),
    (
        "ogc-records-zero-row-map-adapter",
        "Official OGC API Records and MARC cartographic-metadata adapter with zero calls, rows, credentials, coordinates, locations, rights conclusions, likelihoods, or empirical claims",
        "open_gap",
        "GMUT Mind and Freed ID",
        "offline request and response schema, landing-page, collection, record and link placeholders, MARC 008, 034 and 255 field mappings, disabled transport, zero rows, zero sensitive locations, and fail-closed inference refusal",
        ["OGC-API-RECORDS", "LOC-MARC255", "LOC-MARC008", "NZ-PRIVACY"],
    ),
    (
        "thos-map-library-intake-handover",
        "THOS map-library accession, condition-hold, scale-readback, projection-uncertainty, retrieval-stop, workload, correction, and shift-handover protocol",
        "represented",
        "THOS Body",
        "synthetic intake tokens, sheet-count and enclosure placeholders, scale and projection readback, uncertainty and condition holds, retrieval refusal, workload ceiling, correction digest, escalation, and zero workers or collection items",
        ["LOC-COLLECTIONS-CARE", "LOC-MARC255", "WCAG22", "W3C-PROV"],
    ),
    (
        "freed-id-cartographic-record-profile",
        "Freed ID nonproduction cartographic-record profile binding surrogate sheet, catalog record, edition, extent, source, correction, access state, and provenance evidence",
        "represented",
        "Freed ID and CBR Heart",
        "synthetic record and sheet identifiers, credential-subject placeholder, evidence and terms-of-use placeholders, source and revision relation, status and revocation vacancy, privacy mask, zero keys, proofs, issuances, presentations, or interoperability",
        ["W3C-VC2", "W3C-PROV", "OGC-API-RECORDS", "NZ-PRIVACY"],
    ),
    (
        "cartographic-rights-authority-matrix",
        "Vacant mandate matrix for land and boundary meaning, sensitive locations, place names, access, title, traditional knowledge, disclosure, remedy, and tangata whenua, iwi, hapū, Māori authority",
        "exact_gate",
        "CBR Heart",
        "unoccupied owner, donor, depositor, community, landholder, title, boundary, safety, privacy, access, legal, cultural, place-name, traditional-knowledge, affected-party, remedy, tangata whenua, iwi, hapū and Māori-authority reservations",
        ["LINZ-NZGB", "NZ-PRIVACY", "TE-MANA-RARAUNGA", "WCAG22"],
    ),
    (
        "marc-cartographic-math-parser",
        "MARC 255 and 034 cartographic-mathematical-data parser tribunal for scale, projection, coordinate order, provenance subfield, malformed punctuation, range, and refusal",
        "completed",
        "Freed ID and CBR Heart",
        "bounded synthetic MARC field fixtures, explicit subfield ordering, scale and projection strings, westernmost and easternmost plus northernmost and southernmost coordinate order, provenance placeholder, malformed and ambiguous input rejection, and no cataloguing authority",
        ["LOC-MARC255", "LOC-MARC008", "JSON-SCHEMA-2020-12"],
    ),
    (
        "accessible-map-record-companion",
        "Structurally accessible cartographic-record companion with heading order, scope-labelled tables, textual extent narrative, noncolour uncertainty, focus order, status messages, and reserved human review",
        "completed",
        "CBR Heart and THOS Body",
        "semantic headings, table captions and headers, coordinate and scale text alternatives, noncolour states, keyboard order, status region, print fallback, plain-text summary, and zero manual, browser-diverse, assistive-technology, Māori-language, cognitive or affected-user sessions",
        ["WCAG22", "LOC-MARC255", "W3C-PROV"],
    ),
    (
        "projection-distortion-nonconversion",
        "Cartographic projection Jacobian, areal and angular distortion, singularity, scale domain, unit, uncertainty, and psyche-nonconversion classifier",
        "completed",
        "GMUT Mind",
        "typed symbolic projection maps, local Jacobians, determinant and metric-distortion placeholders, singularity and domain guards, unit declarations, counterexamples, and explicit rejection of conversion into psyche, agency, justice, consciousness or personhood",
        ["NZ-MSL-SI", "W3C-PROV", "IETF-JCS"],
    ),
    (
        "stage20-cartographic-generalization-board",
        "Stage 20 cartographic-generalization, scale-change, feature-selection, omission, displacement, aggregation, uncertainty, leakage, and nonpromotion board",
        "completed",
        "All pillars",
        "synthetic feature tokens, declared source and target scales, selection and omission reasons, displacement and aggregation flags, uncertainty, sealed holdout, leakage sentinels, retained failures, and absolute nonpromotion",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    (
        "ogc-records-query-refusal",
        "OGC API Records landing-page, collection, link-relation, conformance, query, sort, pagination, cursor, limit, result-count, and write-refusal tribunal",
        "completed",
        "Freed ID and THOS Body",
        "synthetic OpenAPI-like fixtures, declared link relations, collection and record tokens, bounded query and sort fields, opaque cursor, stable page ordering, duplicate and drift quarantine, resource ceilings, and no network or write action",
        ["OGC-API-RECORDS", "JSON-SCHEMA-2020-12", "IETF-JCS"],
    ),
    (
        "coordinate-axis-antimeridian-tribunal",
        "Longitude wrap, latitude range, axis order, antimeridian crossing, polar extent, ring orientation, empty geometry, precision, and sensitive-location refusal tribunal",
        "completed",
        "GMUT Mind and CBR Heart",
        "synthetic coordinate tokens, declared axis order and domain, wrap and crossing state, polar and empty cases, ring and bounding-box consistency, precision budget, ambiguity quarantine, location minimization, and zero real coordinates",
        ["LOC-MARC255", "OGC-API-RECORDS", "NZ-PRIVACY"],
    ),
    (
        "cartographic-assertion-braid",
        "Cartographic title, edition, scale, projection, extent, source, place-label, supplied-versus-transcribed text, correction, contestation, supersession, and authority-abstention braid",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic assertions with source class, confidence-free status, supplied and transcribed separation, correction and supersession, contestation, non-erasure, unresolved ambiguity, and no naming, authenticity, land, title or boundary determination",
        ["W3C-PROV", "LOC-MARC255", "LINZ-NZGB", "TE-MANA-RARAUNGA"],
    ),
    (
        "git-sparse-index-evidence-tribunal",
        "Git sparse-checkout, sparse-index, skip-worktree, pathspec, tracked-blob, staged-allowlist, expansion, and evidence-credit tribunal",
        "completed",
        "All pillars",
        "disposable owner-local repository fixtures, sparse pattern and index state, skip-worktree and tracked-blob checks, literal staged allowlist, expansion and missing-path cases, rollback receipt, and no canonical or sibling mutation",
        ["GIT-SPARSE-CHECKOUT", "GIT-LS-FILES", "W3C-PROV"],
    ),
    (
        "map-record-canonical-query",
        "Canonical map-record filter and sort normalizer with Unicode preservation, explicit field allowlist, stable ordering, duplicate predicate collapse, bounded limits, and no semantic reinterpretation",
        "completed",
        "Freed ID and THOS Body",
        "synthetic filters, explicit allowlisted fields and operators, stable sort and tie-break tokens, Unicode-preserving values, bounded result limit, duplicate and contradictory predicate rejection, canonical JSON digest, and no live query",
        ["OGC-API-RECORDS", "IETF-JCS", "PYTHON-JSON"],
    ),
    (
        "freed-id-map-correction-envelope",
        "Freed ID represented correction envelope for a surrogate map record with prior digest, changed assertion set, evidence placeholder, status vacancy, dispute hold, and no cryptographic proof",
        "represented",
        "Freed ID and CBR Heart",
        "synthetic credential-shaped envelope, record and prior digest placeholders, changed assertion list, evidence and terms-of-use slots, dispute and restriction holds, status and revocation vacancy, zero issuer, key, signature, proof or verification",
        ["W3C-VC2", "W3C-PROV", "IETF-JCS", "NZ-PRIVACY"],
    ),
    (
        "map-report-print-structure",
        "Cartographic static-report print, page-break, repeated table-header, landmark, visible-focus, status-text, reduced-motion, and no-colour-only audit",
        "completed",
        "CBR Heart and THOS Body",
        "structural HTML and CSS assertions, page title, landmark and heading hierarchy, repeated table headers, break controls, visible focus styles, reduced-motion preference, text-coded states, print fallback, and manual evaluation reserve",
        ["WCAG22", "LOC-COLLECTIONS-CARE", "W3C-PROV"],
    ),
    (
        "georeferencing-review-shell",
        "Represented georeferencing control-point, residual, transformation-family, uncertainty, outlier, approval, rollback, and zero-image review shell",
        "represented",
        "THOS Body and GMUT Mind",
        "synthetic control-point identifiers, zero pixel or ground coordinates, transformation-family placeholders, residual and covariance vacancies, outlier and rollback states, independent-review slot, and no image, measurement, fit or publication",
        ["OGC-API-RECORDS", "NZ-MSL-SI", "W3C-PROV"],
    ),
    (
        "gmut-stokes-chart-domain-board",
        "GMUT differential-form pullback, orientation, chart-domain cover, boundary decomposition, Stokes consistency, unit, regularity, and empirical-firewall board",
        "completed",
        "GMUT Mind",
        "typed symbolic forms, chart-domain and overlap tokens, pullback and orientation obligations, boundary decomposition, unit and regularity metadata, exact synthetic counterexamples, and zero physical field, measurement, likelihood or theorem-of-everything claim",
        ["NZ-MSL-SI", "W3C-PROV", "IETF-JCS"],
    ),
    (
        "terminal-evidence-cartography-board",
        "Terminal evidence-cartography board with source class, claim scope, negative lineage, open gap, exact gate, authority vacancy, dependency cut set, and Stage 20 stop",
        "completed",
        "All pillars",
        "typed claim and source nodes, negative and recovery edges, open-gap and exact-gate nodes, authority vacancies, dependency cut set, non-substitution rules, same-owner boundary, and terminal abstention",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
]
NEW_PROPOSAL_SPECS = [_proposal(*row) for row in _NEW_ROWS]

SELF_SAFE_CATEGORIES = [
    "Elowen source head and fresh four-way equality",
    "activation packet and canonical receipt digests",
    "three-thousand-four-hundred-ten-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "mechanism-level cartographic and map-library neighbour review",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity and relational-language boundary",
    "Hamish-authorized Elowen-to-Sylven live edge and terminal-gated later route",
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
    "no-x2-in-x1 guard",
]
SELF_SAFE_TASKS = [
    {
        "task_id": f"V6617-SAFE-{i:03d}",
        "title": f"Validate {name} inside the Sylven-owned v661-v7 lane",
        "owner": OWNER,
    }
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {
        "task_id": f"V6617-REC-SAFE-{i:03d}",
        "title": f"Reassess {name} in the later authorized Caelen Morrow lane",
        "recipient": "Caelen Morrow",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "synthetic map-sheet accession identity capsule",
    "cartographic title, edition, extent, scale, projection and source assertion braid",
    "MARC 255 and 034 parser and malformed-input tribunal",
    "coordinate axis, range, antimeridian, orientation and location-minimization tribunal",
    "OGC API Records link, query, sort and pagination refusal surface",
    "GMUT smooth-atlas transition and Stokes obligation boards",
    "THOS accession, condition-hold, workload, readback and handover proxy",
    "Freed ID cartographic record and correction envelopes",
    "accessible cartographic report and textual-extent companion",
    "CBR land, boundary, place-name, sensitive-location, remedy and Māori-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {
        "task_id": f"V6617-CAND-{i:03d}",
        "title": f"Build and test reversible {name}",
        "owner": OWNER,
    }
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {
        "task_id": f"V6617-REC-CAND-{i:03d}",
        "title": f"Consider a distinct later-owner refinement of {name}",
        "recipient": "Caelen Morrow",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {
        "task_id": f"V6617-EXACT-{i:03d}",
        "title": title,
        "state": "exact_gate_unexecuted",
    }
    for i, title in enumerate(
        [
            "Accession, catalogue, georeference, alter, handle, flatten, roll, scan, conserve, publish, disclose, restrict, release, or dispose of any real map, chart, atlas, sheet, image, record, location, or collection item",
            "Make a real scale, projection, coordinate, boundary, title, land, condition, authenticity, provenance, rights, safety, access, quality, or release determination",
            "Use real owners, donors, depositors, cataloguers, librarians, archivists, conservators, researchers, communities, affected parties, locations, coordinates, images, or personal information",
            "Disclose private identity, address, request, relationship, sensitive location, traditional knowledge, restricted site, collection history, provenance, title, or access record",
            "Make a professional cartographic, library, archival, conservation, geospatial, workplace-safety, privacy, security, translation, or accessibility determination",
            "Publish a production identifier, catalog record, credential, signature, proof, status, interoperability result, geospatial service, or operational record",
            "Allocate land or boundary meaning, title, ownership, custody, attribution, mapping rights, access, remedy, beneficiary, affected-party, or community authority",
            "Make a tikanga, mātauranga, wording, place-name, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, taonga-status, or Māori-authority decision",
            "Run a real participant study, map-room shift, cataloguing trial, safety review, professional assessment, publication trial, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Sylven-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {
        "task_id": f"V6617-BLOCK-{i:03d}",
        "title": title,
        "state": "blocked_unexecuted",
    }
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
    ("ghc-family-map-accession-identity", "Validate purpose-bound synthetic map accession identity, revision, minimization, cancellation, and handling refusal."),
    ("ghc-family-cartographic-assertion-braid", "Check synthetic title, edition, scale, projection, extent, source, correction, contestation, and authority abstention."),
    ("ghc-family-marc-cartographic-parser", "Validate bounded MARC 255 and 034 scale, projection, coordinate, provenance, malformed-input, and refusal fixtures."),
    ("ghc-family-coordinate-domain-guard", "Preserve axis order, range, antimeridian, orientation, precision, location minimization, and ambiguity quarantine."),
    ("ghc-family-ogc-records-refusal", "Check bounded OGC Records landing, collection, link, query, sorting, paging, duplicate, resource, and no-network states."),
    ("ghc-family-map-correction-lineage", "Preserve record, source, assertion, correction, supersession, contestation, restriction, tombstone, and non-erasure."),
    ("ghc-family-map-privacy-access-hold", "Keep identity, request, sensitive location, source, retention, disclosure, access, correction, and remedy data minimized."),
    ("ghc-family-map-accessibility-companion", "Expose structural tables, textual extent, noncolour state, alternatives, focus order, print fallback, and reserved human review."),
    ("ghc-family-gmut-atlas-firewall", "Preserve typed atlas, overlap, cocycle, Jacobian, pullback, unit, regularity, and observation-firewall obligations."),
    ("ghc-family-map-rights-authority", "Keep land, boundary, title, place-name, traditional knowledge, access, remedy, and Māori decision rights unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [
    {
        "name": name.replace("map", "caelen-domain"),
        "recipient": "Caelen Morrow",
        "state": "recommendation_only",
        "completion_credit": 0,
    }
    for name, _ in SELF_SKILL_SPECS
]
SELF_RUNNER_SPECS = [
    (name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py", purpose)
    for name, purpose in SELF_SKILL_SPECS
]
SUCCESSOR_RUNNER_SEEDS = [
    {
        "name": name.replace("map", "caelen_domain"),
        "recipient": "Caelen Morrow",
        "state": "recommendation_only",
        "completion_credit": 0,
    }
    for name, _ in SELF_RUNNER_SPECS
]

SELF_CLEAN_CATEGORIES = [
    "retain every inherited and current negative without folding it into a pass",
    "refresh count mirrors only from authoritative ledgers",
    "preserve Git-blob and logical-text hash-domain declarations",
    "pin UTF-8 before Unicode-emitting diagnostics",
    "split Windows probes into bounded scalar receipts",
    "keep expected-empty branch and remote checks null-safe",
    "preserve family-current callers and historical compatibility surfaces",
    "reject stale owner and phase labels in current-owner artifacts",
    "keep x1 immutable after its four-way-equality gate",
    "keep x2 implementation absent from x1",
    "keep exact and blocked packets visible and unexecuted",
    "keep real maps, people, coordinates, locations, records, and connector rows empty",
    "retain scanner candidates separately from confirmed payload hits",
    "scan only declared public owner surfaces across five classes",
    "refresh owner manifests after every additive lifecycle change",
    "verify deterministic JSON ordering and parsing",
    "verify proposal append-only arithmetic",
    "verify inherited revalidation receives zero novelty and completion credit",
    "verify outcome labels use only the four authorized states",
    "reserve manual and affected-user accessibility evaluation",
    "reserve legal, cultural, land, title, place-name, privacy, and Māori authority",
    "reserve empirical GMUT and professional THOS claims",
    "reserve production Freed ID keys, proofs, status, recovery, and trust governance",
    "reserve privacy-complete and exhaustive-security claims",
    "keep every document under the declared word ceiling",
    "keep owner additions under the declared file ceiling",
    "verify source-to-final single-parent zero-merge ancestry",
    "hold terminal routing until exact final proof",
    "send no precontact or duplicate activation",
    "preserve NOT_READY_FOR_STAGE_20",
]
SELF_CLEAN_TASKS = [
    {
        "task_id": f"V6617-CLEAN-{i:03d}",
        "title": title,
        "owner": OWNER,
        "mode": "additive_review_only",
    }
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {
        "task_id": f"V6617-REC-CLEAN-{i:03d}",
        "title": title,
        "recipient": "Caelen Morrow",
        "completion_credit": 0,
    }
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("LOC-MARC255", "official_library_of_congress", "https://www.loc.gov/marc/bibliographic/bd255.html", "Current MARC 21 cartographic mathematical-data vocabulary for scale, projection, coordinates and provenance only; no cataloguing, interpretation, location, rights or professional conclusion."),
    ("LOC-MARC008", "official_library_of_congress", "https://www.loc.gov/marc/bibliographic/concise/bd008p.html", "Current MARC 21 map fixed-field vocabulary only; zero real records and no cataloguing authority."),
    ("LOC-COLLECTIONS-CARE", "official_library_of_congress", "https://www.loc.gov/preservation/care/", "General collections-care and handling vocabulary only; no real item handling, storage, treatment, conservation or professional recommendation."),
    ("OGC-API-RECORDS", "official_open_geospatial_consortium", "https://ogcapi.ogc.org/records/", "OGC API Records Part 1 discovery and record vocabulary only; disabled transport, zero calls, rows, writes, locations or conformance claim."),
    ("LINZ-NZGB", "official_nz_geographic_board", "https://www.linz.govt.nz/our-work/new-zealand-geographic-board/about-new-zealand-geographic-board/board-documents-policies-and-standards", "Official place-name policy and authority-boundary vocabulary only; no naming, spelling, macron, land, cultural or Māori-authority decision."),
    ("NZ-MSL-SI", "official_nz_metrology_institute", "https://www.measurement.govt.nz/metrology/si-units", "SI quantity and unit vocabulary only; zero measurements, calibrations, uncertainty results or physical confirmation."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent-placeholder, derivation, revision, invalidation and qualified-provenance vocabulary only."),
    ("W3C-VC2", "official_w3c", "https://www.w3.org/TR/vc-data-model-2.0/", "Credential subject, issuer, evidence, terms-of-use, validity, status and privacy vocabulary only; zero keys, proofs, issuances, presentations or production identities."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Accessible structure, alternatives, noncolour, navigation, focus, status and print vocabulary with manual, browser, assistive-technology, Māori-language, cognitive and affected-user evaluation reserved."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary including IPP 3A from May 2026 only; no legal, compliance, collection, disclosure or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary only; no Māori authority, ratification, wording, naming, tikanga, mātauranga, taonga-status or cultural decision."),
    ("JSON-SCHEMA-2020-12", "primary_json_schema_project", "https://json-schema.org/draft/2020-12", "Schema, vocabulary, validation, annotation and fail-closed structural vocabulary only."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity or production claims."),
    ("GIT-CAT-FILE", "official_git_docs", "https://git-scm.com/docs/git-cat-file", "Batch object inspection and exact blob-byte vocabulary for disposable and read-only repository checks."),
    ("GIT-SPARSE-CHECKOUT", "official_git_docs", "https://git-scm.com/docs/git-sparse-checkout", "Sparse working-tree and sparse-index vocabulary for disposable owner-local fixtures only."),
    ("GIT-LS-FILES", "official_git_docs", "https://git-scm.com/docs/git-ls-files", "Tracked, staged and skip-worktree inspection vocabulary only."),
    ("PYTHON-SUBPROCESS", "official_python_docs", "https://docs.python.org/3/library/subprocess.html", "Bounded process, dual-pipe and communicate vocabulary for disposable owner-local fixtures only."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]
SOURCE_STATUS = {
    "LOC-MARC255": "official_page_checked_2026_08_05",
    "LOC-MARC008": "official_page_updated_2025_12_checked_2026_08_05",
    "LOC-COLLECTIONS-CARE": "official_page_checked_2026_08_05",
    "OGC-API-RECORDS": "official_part_1_core_1_0_0_checked_2026_08_05",
    "LINZ-NZGB": "official_policy_page_checked_2026_08_05",
    "NZ-MSL-SI": "current_official_si_units_page",
    "W3C-PROV": "stable_recommendation",
    "W3C-VC2": "recommendation_2025_checked_2026_08_05",
    "WCAG22": "recommendation_2024",
    "NZ-PRIVACY": "current_including_ipp3a_from_2026_05_01",
    "TE-MANA-RARAUNGA": "primary_principles_current",
    "JSON-SCHEMA-2020-12": "current_2020_12",
    "IETF-JCS": "stable_informational_rfc",
    "GIT-CAT-FILE": "current",
    "GIT-SPARSE-CHECKOUT": "current",
    "GIT-LS-FILES": "current",
    "PYTHON-SUBPROCESS": "current",
    "PYTHON-JSON": "current",
}


def _startup_failure(
    negative_id: str, signature: str, recovery: str
) -> dict[str, object]:
    return {
        "negative_id": negative_id,
        "signature": signature,
        "recovery": recovery,
        "recovery_passed": True,
        "completion_credit": 0,
    }


_STARTUP_FAILURE_ROWS = [
    ("memory-registry-broad-search-exceeded-the-ten-second-bound", "Retain the timeout and use exact current-route handles; the bounded search returned no matching v661-v7 memory entry."),
    ("first-activation-packet-display-was-truncated", "Read the exact file through EOF in contiguous bounded UTF-8 windows and verify bytes, lines, words and SHA-256."),
    ("grouped-skill-reference-display-was-truncated", "Read each mandatory skill and named schema separately through EOF."),
    ("method-flow-schema-was-first-requested-under-a-guessed-filename", "Enumerate the skill reference directory and read the exact schema.md through EOF."),
    ("reflection-schema-was-first-requested-under-a-guessed-filename", "Enumerate the skill reference directory and read the exact decision-schema.md through EOF."),
    ("first-skill-metadata-projection-piped-a-foreach-block-without-materialization", "Retain the parser fault and collect the bounded result array before JSON projection."),
    ("broad-external-receipt-content-scan-timed-out", "Recover the exact receipt path from the read-only Elowen terminal record and verify the file directly."),
    ("date-bounded-multi-root-receipt-hash-sweep-timed-out", "Stop broad hashing and use the exact immutable receipt path and declared digest."),
    ("grouped-other-root-receipt-enumeration-timed-out", "Retain the timeout and avoid further broad root enumeration."),
    ("overbroad-tool-metadata-lookup-returned-truncated-output", "Filter tool metadata to exact names before inspecting one tool schema."),
    ("first-source-task-read-included-large-tool-outputs-and-was-truncated", "Read one newest source turn without tool outputs and extract the exact receipt path from its terminal summary."),
    ("login-shell-receipt-scalar-probe-timed-out-before-returning-evidence", "Disable login-shell startup for bounded PowerShell file and Git probes."),
    ("one-git-process-per-manifest-entry-replay-timed-out", "Use one git cat-file batch process, consume both pipes with communicate, and replay all 518 declared entries with zero mismatches."),
    ("combined-branch-remote-worktree-space-preflight-timed-out", "Separate local path and worktree checks from the fresh live-remote existence probe."),
    ("frozen-chain-projection-assumed-a-nonexistent-rows-property", "Inspect the actual index keys and combine prior_proposals with new_proposals for the exact 3,410-title audit."),
    ("domain-occurrence-projection-piped-a-foreach-block-without-materialization", "Retain the PowerShell parser fault and collect the bounded result array before projection."),
    ("first-large-x1-patch-template-was-terminated-by-an-unescaped-markdown-backtick", "Retain the JavaScript composition failure and split the patch into backtick-free bounded hunks."),
    ("second-large-x1-patch-template-repeated-the-unescaped-backtick-failure", "Retain the repeated zero-credit composition fault and apply the one affected line through a quoted line-array patch."),
    ("first-novelty-screen-powershell-pipe-replaced-maori-characters-in-the-displayed-title", "Retain the lossy presentation at zero credit and send exact UTF-8 bytes directly between Python processes."),
    ("direct-python-novelty-child-inherited-cp1252-and-failed-while-printing-maori-text", "Retain the encoding failure and set process-local PYTHONUTF8 for the unchanged read-only probe."),
    ("x1-receipt-refresh-summary-projected-a-nonexistent-scanned-file-count-key", "Retain the post-write projection fault, inspect the actual privacy receipt keys, and use files_scanned without regenerating successful unrelated outputs."),
    ("first-literal-x1-git-add-staged-only-the-four-tracked-code-paths-before-its-presentation-was-truncated", "Inspect the actual index and untracked sets, retain the partial staging at zero credit, regenerate only dependent truth and receipt surfaces, then stage the reviewed literal x1 allowlist."),
    ("broad-cross-repository-family-runner-search-timed-out-before-returning-a-usable-result", "Retain the lookup timeout at zero credit and enumerate only the already-selected exact skill directories and filenames."),
    ("first-targeted-x1-receipt-refresh-module-load-omitted-the-repository-scripts-import-path", "Retain the pre-write import failure at zero credit, prepend the exact owner worktree scripts directory to the process-local module path, and rerun the unchanged targeted refresh."),
    ("literal-x1-allowlist-staging-was-refused-because-the-new-owner-docs-path-was-outside-the-inherited-sparse-checkout-cone", "Retain the refusal at zero credit, preserve inherited sparsity rules, and use Git's scoped sparse-aware staging flag only for the exact reviewed Sylven-owned allowlist."),
]
STARTUP_FAILURES = [
    _startup_failure(f"V6617-X1-N{i:03d}", signature, recovery)
    for i, (signature, recovery) in enumerate(_STARTUP_FAILURE_ROWS, 1)
]

PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
