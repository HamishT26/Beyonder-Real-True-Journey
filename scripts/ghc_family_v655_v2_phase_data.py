#!/usr/bin/env python3
"""Frozen x1 data for Lyren Moss's v655-v2 phase."""

from __future__ import annotations


PHASE = "v655-v2"
PHASE_CODE = "V6552"
OWNER = "Lyren Moss"
PRONOUNS = "they/them"
ROLE = "relational repair-traceability lantern and reversible-evidence gardener"
HOPE = (
    "make community repair decisions kind, inspectable, and reversible while "
    "keeping electrical safety, ownership, privacy, legal, cultural, and "
    "affected-party decisions with their proper authorities"
)
BRANCH = "codex/GHC-Family/lyren-moss-v655-v2-full-tools"
PHASE_ROOT = "docs/lyren-moss/v655-v2"

SOURCE_OWNER = "Vesper Arlen"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v655-v1-full-tools"
SOURCE_X1_FREEZE = "508242e41a66442961465954f492f25e5005ea97"
SOURCE_X1_FINAL = SOURCE_X1_FREEZE
SOURCE_EVIDENCE = "607ae7208a775dc816eebf595c79307b38b9ade2"
SOURCE_EVIDENCE_CORRECTION = None
SOURCE_FINAL = "e1534547a8e6b053e90bbb1eed0966402ef03908"
PRIOR_FROZEN = 1960
SOURCE_SEALED_REPOSITORY_NEGATIVES = 12389
SOURCE_LIVE_OVERLAY = [
    {
        "negative_id": "V6551-POSTSEAL-N01",
        "signature": "task_list_query_option_rejected",
        "failed": (
            "The post-seal exact-title task lookup advertised a query option that "
            "the live host rejected, so the attempt earned zero route credit."
        ),
        "recovery": (
            "Use one bounded unfiltered task listing and local exact-title "
            "filtering; do not compensate with a duplicate send."
        ),
        "recurrence_guard": (
            "Treat task-list query support as host-specific and retain one "
            "rejected-option witness without replaying a successful activation."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    }
]
SOURCE_EFFECTIVE_NEGATIVES = 12390
SOURCE_OPEN_GAPS = 89
SOURCE_EXACT_GATES = 88
SOURCE_METHODS_SEALED = 198
SOURCE_METHODS = 198

PRIMARY_FOCUS = "THOS Body through bounded community repair-café practice"
BOUNDED_PRACTICE = (
    "community repair-café intake, appliance safety triage, reversible diagnostic "
    "planning, parts provenance, privacy-aware handover, and end-of-life routing, "
    "used only as a bounded synthetic workflow and evidence-assurance lens; no "
    "real appliance energization, disassembly, repair, test measurement, battery "
    "handling, warranty decision, return-to-service decision, legal advice, "
    "cultural decision, or Māori authority"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_empirical_data_and_likelihood",
    "real_participants_affected_parties_and_communities",
    "professional_electrical_battery_safety_repair_data_security_identity_and_governance_authority",
    "production_repair_release_media_sanitization_parts_supply_and_warranty_decisions",
    "real_appliance_operation_disassembly_measurement_energization_and_return_to_service",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_and_maori_authority",
    "affected_party_acceptance_remedy_and_beneficiary_privacy",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

OFFICIAL_SOURCES = [
    {
        "source_id": "CCI-BOOKS-11-7",
        "title": "Basic Care of Books — CCI Notes 11/7",
        "publisher": "Canadian Conservation Institute",
        "url": "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/basic-care-books.html",
        "status": "current",
        "use": "book structure, handling, storage, enclosure, cleaning, and competence-hold vocabulary",
    },
    {
        "source_id": "LOC-BOOK-CARE",
        "title": "Preserving Your Books",
        "publisher": "Library of Congress",
        "url": "https://guides.loc.gov/preserving-your-books",
        "status": "current",
        "use": "preventive handling and storage boundaries for valued books",
    },
    {
        "source_id": "LOC-PAPER-CARE",
        "title": "Care, Handling, and Storage of Works on Paper",
        "publisher": "Library of Congress",
        "url": "https://www.loc.gov/preservation/care/paper.html",
        "status": "current",
        "use": "paper handling, marking, storage, adhesive, fastener, and conservator-referral boundaries",
    },
    {
        "source_id": "ISO-9706-2025",
        "title": "ISO 9706:2025 — Paper for documents — Requirements for permanence",
        "publisher": "International Organization for Standardization",
        "url": "https://www.iso.org/standard/88908.html",
        "status": "current",
        "use": "paper-permanence scope and explicit hostile-condition limitation",
    },
    {
        "source_id": "W3C-PROV-O",
        "title": "PROV-O: The PROV Ontology",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "stable",
        "use": "entity, activity, agent, derivation, revision, and provenance-interchange vocabulary",
    },
    {
        "source_id": "IIIF-PRESENTATION-3",
        "title": "IIIF Presentation API 3.0",
        "publisher": "International Image Interoperability Framework",
        "url": "https://iiif.io/api/presentation/3.0/",
        "status": "stable",
        "use": "compound-object image, canvas, range, annotation, language, and versioning vocabulary",
    },
    {
        "source_id": "ISBN-MANUAL-7",
        "title": "ISBN Users' Manual, seventh edition",
        "publisher": "International ISBN Agency",
        "url": "https://www.isbn-international.org/index.php/content/isbn-users-manual/29",
        "status": "watch",
        "use": "edition and manifestation identifier vocabulary; watch-only, nonproduction compatibility",
    },
    {
        "source_id": "DOI-HANDBOOK",
        "title": "DOI Handbook",
        "publisher": "DOI Foundation",
        "url": "https://www.doi.org/doi-handbook/html/",
        "status": "current",
        "use": "persistent referent, resolution, registry, metadata, and identifier-governance boundaries",
    },
    {
        "source_id": "IETF-RFC8141",
        "title": "RFC 8141 — Uniform Resource Names",
        "publisher": "RFC Editor / IETF",
        "url": "https://www.rfc-editor.org/rfc/rfc8141",
        "status": "stable",
        "use": "persistent location-independent identifier syntax and namespace boundaries",
    },
    {
        "source_id": "W3C-WCAG-22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "stable",
        "use": "accessible static-report structure and manual-evaluation reservations",
    },
    {
        "source_id": "NZ-OPC-PRINCIPLES",
        "title": "New Zealand Privacy Act 2020 principles",
        "publisher": "Office of the Privacy Commissioner New Zealand",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "current",
        "use": "purpose, collection, notification, security, access, correction, retention, and disclosure reservations",
    },
    {
        "source_id": "TMR-PRINCIPLES",
        "title": "Principles of Māori Data Sovereignty",
        "publisher": "Te Mana Raraunga",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "current",
        "use": "Māori rights, interests, governance, and authority reservation only",
    },
]


def _proposal(
    number: int,
    title: str,
    slug: str,
    pillar: str,
    disposition: str,
    mechanism: str,
    sources: list[str],
) -> dict:
    if disposition == "completed":
        approval = "safe_now_bounded_structural_or_synthetic_software"
        lane = "x2_owner_local_bounded"
        acceptance = (
            "The valid fixture passes, all five preregistered mutations are rejected, "
            "and the receipt makes no real-treatment, external, production, participant, "
            "authority, effectiveness, or completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real appliances, "
            "batteries, tools, electrical measurements, volunteers, visitors, "
            "premises, safety decisions, and repair operation stay absent."
        )
    elif disposition == "open_gap":
        approval = "candidate_real_material_participant_and_professional_evidence_required"
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-appliance, zero-tool, zero-measurement, zero-participant "
            "refusal receipt and leave the empirical, professional, safety, and "
            "authorization gap open."
        )
    else:
        approval = "exact_affected_party_legal_cultural_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved ownership, custody, repair, access, return, remedy, "
            "language, sovereignty, and governance reservations only; make no legal, "
            "cultural, Māori-authority, donor, descendant, iwi, or affected-party decision."
        )
    return {
        "proposal_id": f"{PHASE_CODE}-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable obligations while "
            "refusing unsupported treatment, identity, scientific, operational, or "
            "authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen "
            "mutation, erases a failure, or exceeds its evidence, treatment, privacy, "
            "or authority lane."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": acceptance,
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and "
            "leave appliances, batteries, tools, parts, accounts, siblings, participants, "
            "production, professional, legal, cultural, Māori-authority, and external "
            "state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
    }


_P = [
    (1, "Book-repair intake object, presented-custody claim, edition-copy identifier, component count, condition boundary, privacy minimization, and work-start refusal", "book-repair-intake", "THOS Body", "completed", "book-repair intake and custody boundary", ["CCI-BOOKS-11-7", "LOC-BOOK-CARE", "W3C-PROV-O", "NZ-OPC-PRINCIPLES"]),
    (2, "Book textblock collation map with gathering signature, leaf sequence, singleton, insert, cancellation, missing-leaf signal, and resewing hold", "textblock-collation-map", "THOS Body", "completed", "textblock collation and resewing hold", ["CCI-BOOKS-11-7", "W3C-PROV-O"]),
    (3, "Book paper-grain and fold-orientation ledger with sheet mark, machine direction placeholder, fold axis, section nesting, mismatch signal, and imposition refusal", "paper-grain-fold-ledger", "THOS Body", "completed", "paper grain and fold orientation", ["ISO-9706-2025", "CCI-BOOKS-11-7"]),
    (4, "Book pagination, foliation, catchword, and plate anomaly crosswalk with source mark, inferred sequence, uncertainty, reversible note, and renumbering refusal", "pagination-anomaly-crosswalk", "THOS Body", "completed", "pagination and foliation anomaly crosswalk", ["W3C-PROV-O", "LOC-BOOK-CARE"]),
    (5, "Book sewing-support architecture board with stitch pattern, support count, station position, thread path, board attachment placeholder, and structural-claim hold", "sewing-support-architecture", "THOS Body", "completed", "sewing support architecture", ["CCI-BOOKS-11-7", "LOC-BOOK-CARE"]),
    (6, "Bookbinding thread and needle lot record with material, gauge, coating placeholder, sharps condition, substitution, operator-competence hold, and disposal note", "thread-needle-lot-record", "THOS Body", "represented", "thread needle and sharps record", ["CCI-BOOKS-11-7"]),
    (7, "Book board-cut geometry tribunal with board lot, grain, height, width, square diagonal, edge condition, tool-status placeholder, and cut authorization refusal", "board-cut-geometry", "THOS Body", "represented", "board cut geometry and tool hold", ["CCI-BOOKS-11-7", "ISO-9706-2025"]),
    (8, "Book spine-lining layer graph with adhesive interface, material sequence, overlap, dry-state, reversibility placeholder, conflict, and layer-order refusal", "spine-lining-layer-graph", "THOS Body", "completed", "spine lining layer order", ["CCI-BOOKS-11-7", "LOC-BOOK-CARE"]),
    (9, "Bookbinding adhesive batch ledger with type, recipe source, lot, preparation time, open time, viscosity proxy, contamination signal, and use refusal", "adhesive-batch-ledger", "THOS Body", "represented", "adhesive batch and open-time hold", ["CCI-BOOKS-11-7", "LOC-PAPER-CARE"]),
    (10, "Book press-stack load proxy with platen area, stack order, interleaf, load placeholder, duration, release condition, pinch-zone hold, and force-claim refusal", "press-stack-load-proxy", "THOS Body", "represented", "press stack load and release proxy", ["CCI-BOOKS-11-7", "LOC-BOOK-CARE"]),
    (11, "Book paper-conditioning envelope with relative-humidity record, temperature, dwell interval, material class, sensor status placeholder, excursion, and treatment hold", "paper-conditioning-envelope", "THOS Body", "represented", "paper conditioning and excursion hold", ["CCI-BOOKS-11-7", "ISO-9706-2025"]),
    (12, "Book covering-material provenance ledger with cloth, paper, leather or synthetic class, supplier lot, colour note, coating, backing, substitution, and suitability refusal", "covering-material-provenance", "THOS Body", "completed", "covering material provenance", ["CCI-BOOKS-11-7", "W3C-PROV-O"]),
    (13, "Book endpaper attachment map with construction type, attachment edge, sewing relation, adhesive interface, grain orientation, revision, and hidden-structure refusal", "endpaper-attachment-map", "THOS Body", "completed", "endpaper attachment structure", ["CCI-BOOKS-11-7", "W3C-PROV-O"]),
    (14, "Book joint, hinge, and square clearance board with board thickness, spine geometry, opening-angle placeholder, rub signal, tolerance source, and release refusal", "joint-hinge-clearance", "THOS Body", "completed", "joint hinge and square clearance", ["CCI-BOOKS-11-7", "LOC-BOOK-CARE"]),
    (15, "Book trim and crop protection map with text-block edge, deckle or witness mark, annotation clearance, bleed boundary, cut-line placeholder, and irreversible-action hold", "trim-crop-protection", "THOS Body", "completed", "trim crop and annotation protection", ["LOC-PAPER-CARE", "CCI-BOOKS-11-7"]),
    (16, "Book paper-repair tissue and paste compatibility docket with tear type, fibre direction, tissue lot, adhesive class, reversibility-claim placeholder, and intervention refusal", "repair-tissue-compatibility", "THOS Body", "completed", "repair tissue and paste compatibility", ["LOC-PAPER-CARE", "CCI-BOOKS-11-7"]),
    (17, "Book detached-fragment custody envelope with fragment identifier, source location, image reference, enclosure, match confidence, reunification proposal, and attachment refusal", "detached-fragment-custody", "THOS Body", "completed", "detached fragment custody", ["W3C-PROV-O", "CCI-BOOKS-11-7"]),
    (18, "Book before-and-after image derivative manifest with capture purpose, view, scale reference, colour-target placeholder, crop, redaction, checksum, and publication hold", "repair-image-derivative-manifest", "THOS Body", "completed", "repair image derivative provenance", ["IIIF-PRESENTATION-3", "W3C-PROV-O", "NZ-OPC-PRINCIPLES"]),
    (19, "Book edition, impression, issue, state, copy, and repair-event identifier crosswalk with source vocabulary, collision, supersession, and identity-conflation refusal", "edition-copy-identifier-crosswalk", "THOS Body", "completed", "edition copy and repair identifier separation", ["ISBN-MANUAL-7", "DOI-HANDBOOK", "IETF-RFC8141"]),
    (20, "Bookbinding workstation hazard and stop-work board with blade-guard placeholder, awl and needle state, press clearance, ventilation, spill, fatigue signal, and competence refusal", "workstation-stop-work-board", "THOS Body", "completed", "bookbinding workstation stop-work boundary", ["CCI-BOOKS-11-7"]),
    (21, "GMUT folded-sheet kinematics field with crease graph, panel orientation, fold-angle symbol, self-contact boundary, thickness limit, unit, and observation firewall", "gmut-folded-sheet-kinematics", "GMUT Mind", "completed", "folded sheet kinematics firewall", ["W3C-PROV-O", "ISO-9706-2025"]),
    (22, "GMUT adhesive-penetration paper field with pore proxy, viscosity symbol, capillary pressure, diffusion term, boundary flux, cure clock, unit, and empirical firewall", "gmut-adhesive-penetration-field", "GMUT Mind", "completed", "adhesive penetration field firewall", ["W3C-PROV-O", "LOC-PAPER-CARE"]),
    (23, "GMUT sewn-textblock network field with gathering node, stitch edge, support coupling, pretension symbol, opening load, boundary condition, unit, and observation firewall", "gmut-sewn-textblock-network", "GMUT Mind", "completed", "sewn textblock network firewall", ["W3C-PROV-O", "CCI-BOOKS-11-7"]),
    (24, "THOS typed book-repair task envelope with objective, object scope, evidence inputs, reversible outputs, dependency, privacy class, authority ceiling, rollback, and acceptance predicate", "thos-book-repair-task-envelope", "THOS Body", "completed", "typed book repair task envelope", ["W3C-PROV-O", "NZ-OPC-PRINCIPLES"]),
    (25, "THOS bookbinding dry-time dependency scheduler with operation graph, material compatibility, earliest start, hold interval, stale-sensor signal, cancellation, and no-auto-release invariant", "thos-dry-time-scheduler", "THOS Body", "completed", "dry-time dependency scheduler", ["W3C-PROV-O", "CCI-BOOKS-11-7"]),
    (26, "Freed ID ISBN, DOI, URN, IIIF, shelfmark, edition, and copy relation profile with namespace source, referent class, resolver status, collision, privacy, and nonproduction refusal", "freed-id-book-namespace-profile", "Freed ID and CBR Heart", "completed", "book identifier namespace and referent separation", ["ISBN-MANUAL-7", "DOI-HANDBOOK", "IETF-RFC8141", "IIIF-PRESENTATION-3"]),
    (27, "CBR book-repair decision provenance ledger with owner-instruction placeholder, treatment alternative, material loss, rights note, reviewer gap, return condition, correction, and remedy hold", "cbr-repair-decision-provenance", "Freed ID and CBR Heart", "completed", "repair decision provenance and remedy hold", ["W3C-PROV-O", "NZ-OPC-PRINCIPLES"]),
    (28, "Accessible book-repair record and handling-direction explainer with structure terms, plain-language summary, reading order, status message, nonvisual cue, help route, and manual-evaluation reservation", "accessible-repair-record", "THOS Body", "completed", "accessible repair record structure", ["W3C-WCAG-22", "CCI-BOOKS-11-7"]),
    (29, "Real bookbinding material test and conservator review adapter with object authorization, specimen plan, instrument calibration, participant role, independent review, and zero-action firewall", "real-material-conservator-adapter", "THOS Body", "open_gap", "real material and conservator evidence readiness", ["CCI-BOOKS-11-7", "ISO-9706-2025", "W3C-PROV-O"]),
    (30, "Affected-party, donor, descendant, iwi and Māori authority reservation for taonga books, whakapapa content, language, digitization, repair, access, return, remedy, and data governance", "taonga-book-authority-reservation", "Freed ID and CBR Heart", "exact_gate", "taonga book affected-party and Māori authority reservation", ["TMR-PRINCIPLES", "NZ-OPC-PRINCIPLES", "CCI-BOOKS-11-7"]),
]
PROPOSALS = [_proposal(*row) for row in _P]

SAFE_TASKS = [
    f"Build the bounded contract and five rejecting fixtures for {row['proposal_id']} {row['slug']}"
    for row in PROPOSALS
]
CANDIDATE_TASKS = [
    f"Resolve only the declared evidence lane for {row['proposal_id']} {row['mechanism']}"
    for row in PROPOSALS
]
SKILL_IDEAS = [
    "ghc-family-book-intake-boundary",
    "ghc-family-textblock-collation",
    "ghc-family-paper-grain-fold",
    "ghc-family-spine-layer-order",
    "ghc-family-adhesive-batch-hold",
    "ghc-family-fragment-custody",
    "ghc-family-book-identifier-crosswalk",
    "ghc-family-book-repair-accessibility",
    "ghc-family-bookbinding-task-envelope",
    "ghc-family-bookbinding-evidence-firewall",
]
RUNNER_IDEAS = [
    "ghc_family_book_intake_boundary.py",
    "ghc_family_textblock_collation.py",
    "ghc_family_paper_grain_fold.py",
    "ghc_family_spine_layer_order.py",
    "ghc_family_adhesive_batch_hold.py",
    "ghc_family_fragment_custody.py",
    "ghc_family_book_identifier_crosswalk.py",
    "ghc_family_book_repair_accessibility.py",
    "ghc_family_bookbinding_task_envelope.py",
    "ghc_family_v655_v2_suite.py",
]
CLEAN_TASKS = [
    f"{kind} owner-local {surface} without deletion, sibling mutation, gate weakening, or unsupported promotion"
    for kind in ("CLEAN", "FIX", "REFINE")
    for surface in (
        "book structure vocabulary",
        "textblock collation",
        "material provenance",
        "repair reversibility",
        "privacy boundary",
        "rollback wording",
        "manifest coverage",
        "failure retention",
        "source status",
        "stale-label refusal",
    )
]


def _negative(
    number: int,
    signature: str,
    failed: str,
    recovery: str,
    guard: str,
) -> dict:
    return {
        "negative_id": f"{PHASE_CODE}-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "stale_memory_skill_path_missing",
        "A historical memory pointer named a solo-activation skill that is not present in the current skill root, so it earned no instruction-read credit.",
        "Read the current GHC family index and its explicitly routed skills and schemas through EOF.",
        "Treat memory pointers as discovery aids and verify every current skill path before use.",
    ),
    _negative(
        2,
        "broad_worktree_pattern_probe_overenumerated",
        "The first pattern-based worktree lookup matched the word worktree itself and emitted a large archive inventory instead of bounded lane evidence.",
        "Resolve the exact literal worktree path, branch ref, and registration tuple.",
        "Use literal scalar lane identifiers rather than contextual worktree text matching.",
    ),
    _negative(
        3,
        "bounded_filename_search_timeout",
        "The first recursive filename search under the source phase exceeded its bound and returned no complete evidence.",
        "Use the committed Git tree with a path-bounded name filter.",
        "Prefer Git tree plumbing to recursive filesystem enumeration in archive-backed lanes.",
    ),
    _negative(
        4,
        "powershell_raw_byte_manifest_harness_incompatible",
        "The first raw-byte manifest harness used an unavailable hexadecimal conversion API and timed out before producing a usable audit.",
        "Use one persistent Git object stream and byte-exact SHA-256 hashing in the supported Node runtime.",
        "Confirm runtime conversion support before repeating large byte audits and keep one persistent object stream.",
    ),
    _negative(
        5,
        "branch_uniqueness_probe_parser_error",
        "The first PowerShell branch-uniqueness probe embedded command sequencing inside a hash expression and failed to parse.",
        "Run branch, remote, path, and common-Git-dir checks as explicit scalar assignments.",
        "Do not embed native-command sequencing inside PowerShell hash-value expressions.",
    ),
    _negative(
        6,
        "worktree_add_timeout_late_success",
        "The owned worktree-add command exceeded its wrapper bound after registering the exact branch and while checkout was still materializing.",
        "Do not retry; audit registration, branch, HEAD, process and lock state, then wait for zero locks, zero Git processes, and a clean index.",
        "Never replay an ambiguously timed-out Git mutation before exact-state convergence.",
    ),
    _negative(
        7,
        "transitional_process_detail_probe_no_evidence",
        "A process-detail and lock-metadata probe returned no usable output because checkout completed during the observation window.",
        "Re-run scalar lock, process, HEAD, branch, tracked-diff, staged-diff, and untracked checks after convergence.",
        "Treat a no-output transitional diagnostic as zero credit and establish the postcondition independently.",
    ),
    _negative(
        8,
        "workflow_receipt_filename_assumption",
        "A read-only x1 summary assumed workflow-plan-receipt.json after the other ledger reads succeeded, but the current refinement tool emits differently named receipts.",
        "Enumerate the exact phase-local workflow directory and read workflow-plan-validation.json.",
        "Resolve generated receipt names from the current tool output rather than a remembered convenience name.",
    ),
    _negative(
        9,
        "workflow_validation_error_property_assumption",
        "The corrected workflow summary read the valid receipt but counted a nonexistent top-level errors property instead of the nested issue_counts.errors field.",
        "Inspect the exact validation schema and read issue_counts.errors and issue_counts.warnings.",
        "Enumerate current top-level properties before deriving counts from a remembered receipt shape.",
    ),
    _negative(
        10,
        "x1_manifest_working_bytes_ignored_git_filters",
        "The first independent staged-blob audit found three manifest mismatches because mechanically cloned CRLF files were hashed as working bytes while Git staged filtered LF blobs.",
        "Hash prospective Git-filtered blobs, normalize the four owned x1 source files to LF, rebuild the manifest, and repeat exact staged review.",
        "Define manifest identity in the Git blob domain whenever attributes or line-ending filters may apply.",
    ),
    _negative(
        11,
        "prospective_blob_not_materialized",
        "The first filtered-blob manifest build computed object identifiers without writing the prospective objects, so cat-file could not read the first absent object.",
        "Use git hash-object -w with the exact path filter before reading the prospective blob bytes.",
        "Materialize a prospective object before asking Git object plumbing to return its content.",
    ),
]


# The inherited source module remains mechanically traceable above. Lyren's
# genuinely new phase catalogue is isolated here so the x1 novelty surface is
# reviewable without rewriting inherited source vocabulary in place.
from ghc_family_v655_v2_phase_catalogue import (  # noqa: E402
    CLEAN_SURFACES as _LYREN_CLEAN_SURFACES,
    OFFICIAL_SOURCES as _LYREN_OFFICIAL_SOURCES,
    PROPOSAL_ROWS as _LYREN_PROPOSAL_ROWS,
    RUNNER_IDEAS as _LYREN_RUNNER_IDEAS,
    SKILL_IDEAS as _LYREN_SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES as _LYREN_X1_OPERATIONAL_NEGATIVES,
)

OFFICIAL_SOURCES = _LYREN_OFFICIAL_SOURCES
_P = _LYREN_PROPOSAL_ROWS
PROPOSALS = [_proposal(*row) for row in _P]
for _row in PROPOSALS:
    _mechanism = _row["mechanism"]
    _row["hypothesis"] = (
        f"A bounded {_mechanism} contract can expose falsifiable obligations "
        "while refusing unsupported repair, electrical-safety, identity, "
        "operational, legal, cultural, or authority promotion."
    )
    _row["null_or_failure_condition"] = (
        f"The artifact omits a required {_mechanism} obligation, accepts a frozen "
        "mutation, erases a failure, or exceeds its evidence, repair, measurement, "
        "privacy, cultural, or authority lane."
    )
    _row["rollback_or_recovery"] = (
        "Stop, retain the failed witness at zero credit, rewrite no history, and "
        "leave appliances, batteries, tools, parts, premises, accounts, siblings, participants, "
        "production, professional, legal, cultural, Māori-authority, and external "
        "state unchanged."
    )
    if _row["expected_disposition"] == "exact_gate":
        _row["falsifier_or_acceptance_gate"] = (
            "Emit unresolved ownership, consent, repair, disposal, language, access, "
            "correction, remedy, sovereignty, and governance reservations only; make "
            "no legal, cultural, Māori-authority, tangata-whenua, iwi, hapū, or "
            "affected-party decision."
        )
SAFE_TASKS = [
    f"Build the bounded contract and five rejecting fixtures for "
    f"{row['proposal_id']} {row['slug']}"
    for row in PROPOSALS
]
CANDIDATE_TASKS = [
    f"Resolve only the declared evidence lane for {row['proposal_id']} "
    f"{row['mechanism']}"
    for row in PROPOSALS
]
SKILL_IDEAS = _LYREN_SKILL_IDEAS
RUNNER_IDEAS = _LYREN_RUNNER_IDEAS
CLEAN_TASKS = [
    f"{kind} owner-local {surface} without deletion, sibling mutation, "
    "gate weakening, or unsupported promotion"
    for kind in ("CLEAN", "FIX", "REFINE")
    for surface in _LYREN_CLEAN_SURFACES
]
X1_OPERATIONAL_NEGATIVES = _LYREN_X1_OPERATIONAL_NEGATIVES
