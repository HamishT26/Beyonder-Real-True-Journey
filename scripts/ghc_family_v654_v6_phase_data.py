#!/usr/bin/env python3
"""Frozen Tavian Sol v654-v6 x1 data with no x2 observations."""

from __future__ import annotations


PHASE = "v654-v6"
OWNER = "Tavian Sol"
PRONOUNS = "they/them"
ROLE = "bounded CLI evidence integrator"
HOPE = "make the next handoff easier to trust without blurring any gate"
BRANCH = "codex/GHC-Family/tavian-sol-v654-v6-cli"
PHASE_ROOT = "docs/tavian-sol/v654-v6"

SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v654-v5-full-tools"
SOURCE_HEAD = "0dce8843a215c3b56bc10cc2286db1a924a4043d"
SOURCE_ORIGIN = "f1218fae5969279fc99065297af6ad358a2fb60e"
SOURCE_X1 = "adb37ecf3d981bccc266505356ab596b605c39ad"
SOURCE_X1_INITIAL = SOURCE_X1
SOURCE_EVIDENCE = "362e8f23d3109e86932efecf4d061923ed60117a"
SOURCE_FIRST_CLOSEOUT = "e44c29275c28078086f10a0a3c5480a3187eec06"
SOURCE_EXTERNAL_RECEIPT_SHA256 = (
    "5f1d819deac28cb9c56a8d360577e980294fa636da07da1100e017bd18bd11af"
)
PRIOR_FROZEN = 1810
INHERITED_SEALED_NEGATIVES = 11487
INHERITED_EXTERNAL_NEGATIVES = 23
INHERITED_NEGATIVES = INHERITED_SEALED_NEGATIVES + INHERITED_EXTERNAL_NEGATIVES
INHERITED_OPEN_GAPS = 84
INHERITED_ROUTE_OPEN_GAPS = 0
INHERITED_EXACT_GATES = 83
INHERITED_METHODS = 74
INHERITED_FAILED_WITNESSES = 74
INHERITED_PASSING_WITNESSES = 74
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "digital preservation and research-data stewardship, including package inventories, "
    "fixity, format and dependency records, storage replicas, migration lineage, accessible "
    "status, workload control, and authority reservations, as a synthetic learning and "
    "interface-design lens only"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED_GATES = [
    "empirical_data_and_real_likelihood",
    "real_participants_workers_visitors_or_communities",
    "professional_digital_preservation_archival_records_repository_and_security_authority",
    "production_identity_and_interoperability",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_repatriation_and_maori_authority",
    "affected_party_community_acceptance_and_remedy",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def _proposal(number, title, slug, pillar, disposition, source_ids, mission):
    if disposition == "open_gap":
        approval = "candidate_real_data_access_calibration_provenance_and_independent_review_required"
        lane = "x2_zero_row_readiness_only"
        gate = (
            "Emit a zero-query and zero-row refusal receipt with no account, key, download, "
            "repository connection, ingest, repair, deletion, integrity estimate, likelihood, "
            "posterior, prediction, custody decision, or empirical promotion."
        )
    elif disposition == "exact_gate":
        approval = "exact_affected_party_competent_institutional_tangata_whenua_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        gate = (
            "Emit unresolved decision rights and reservations only; make no ownership, custody, "
            "access, retention, deletion, disclosure, return, repatriation, remedy, legal, cultural, "
            "data-governance, affected-party, or Māori-authority decision."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = (
            "Reject every preregistered mutation and retain represented status with zero real "
            "participant, repository, collection, professional, production, interoperability, or authority credit."
        )
    else:
        approval = "safe_now_bounded_software_symbolic_formal_or_structural"
        lane = "x2_bounded_owner_local"
        gate = (
            "Reject every preregistered mutation and emit only the declared bounded software, "
            "symbolic, formal, structural, or workflow completion."
        )
    return {
        "proposal_id": f"V6546-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": (
            f"A bounded {mission} artifact can expose its declared obligations while refusing "
            "unsupported scientific, operational, identity, accessibility, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a declared {mission} obligation, accepts a preregistered mutation, "
            "erases a failure, crosses an approval boundary, or promotes beyond its evidence lane."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": source_ids,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": (
            "Stop the proposal, retain every failed witness, rewrite no history, and leave external, "
            "sibling, participant, collection, production, professional, legal, cultural, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
        "novelty_against_1810_frozen_proposals": (
            "The complete 1,810-row inherited title audit found no proposal combining the "
            f"digital-preservation mechanism frozen here: {title}."
        ),
    }


_P = [
    (1, "Digital-preservation package inventory with object identifier, payload path, byte length, checksum algorithm, manifest root, missing-file refusal, and custody hold", "preservation-package-inventory", "GMUT Mind", "completed", ["SRC-PREMIS", "SRC-BAGIT"], "package inventory binding and missing-file refusal"),
    (2, "BagIt package tribunal with version declaration, tag-file encoding, payload manifest, tag manifest, fetch reservation, path safety, and incomplete-bag refusal", "bagit-validity-firewall", "GMUT Mind", "completed", ["SRC-BAGIT", "SRC-NIST-SHS"], "BagIt structural validity and incomplete-package refusal"),
    (3, "Fixity verification ledger with algorithm status, expected and observed digest, byte length, event time, retry boundary, mismatch quarantine, and repair nonauthorization", "fixity-mismatch-quarantine", "GMUT Mind", "completed", ["SRC-PREMIS", "SRC-NIST-SHS"], "fixity mismatch quarantine and repair nonauthorization"),
    (4, "File-format identification record with tool and signature version, media-type and registry candidates, confidence placeholder, conflicting-result lineage, and format-claim refusal", "format-identification-conflict", "GMUT Mind", "completed", ["SRC-PREMIS", "SRC-LOC-RFS"], "format-identification conflict and unsupported-claim refusal"),
    (5, "Digital-format risk register with format and version, dependency graph, rendering requirement, openness signal, obsolescence placeholder, review interval, and migration hold", "format-risk-migration-hold", "GMUT Mind", "completed", ["SRC-LOC-RFS", "SRC-NDSA-LEVELS"], "format-risk structure and migration hold"),
    (6, "Preservation migration-event lineage with source and destination identifiers, tool and container version, option set, before-and-after fixity, loss note, and publication hold", "migration-event-lineage", "GMUT Mind", "completed", ["SRC-PREMIS", "SRC-PROV-O"], "migration provenance and publication hold"),
    (7, "Emulation-environment manifest with emulator and firmware placeholders, peripheral graph, dependency hashes, clock mode, licence reservation, and launch refusal", "emulation-environment-reservation", "GMUT Mind", "completed", ["SRC-PREMIS", "SRC-LOC-RFS"], "emulation dependency manifest and launch refusal"),
    (8, "Preservation-replica topology with replica identifier, storage medium, fault domain, encryption placeholder, last-sync state, independence signal, and deletion hold", "replica-fault-domain", "GMUT Mind", "completed", ["SRC-NDSA-LEVELS", "SRC-PREMIS"], "replica fault-domain visibility and deletion hold"),
    (9, "Repository scrub schedule with object-set Merkle root, interval, complete-or-sampled mode, mismatch count, rerun boundary, repair authority reservation, and silent-success refusal", "scrub-repair-reservation", "GMUT Mind", "completed", ["SRC-NDSA-LEVELS", "SRC-NIST-SHS"], "scrub evidence and repair-authority reservation"),
    (10, "Write-protected media-capture record with device and interface, protection mode, source-medium identifier, imaging parameters, output fixity, anomaly log hash, and ingest hold", "write-protect-capture", "GMUT Mind", "completed", ["SRC-PREMIS", "SRC-NIST-SHS"], "write-protected capture lineage and ingest hold"),
    (11, "Preservation timestamp normalization with original lexical value, parser rule, UTC offset, precision, uncertainty, clock source, reversible rendering, and ordering refusal", "timestamp-precision-normalization", "GMUT Mind", "completed", ["SRC-RFC3339", "SRC-PREMIS"], "timestamp precision lineage and ordering refusal"),
    (12, "Archive path-encoding tribunal with original byte representation, Unicode normalization form, case-fold signal, reserved-name collision, reversible mapping, and overwrite refusal", "path-encoding-collision", "GMUT Mind", "completed", ["SRC-BAGIT", "SRC-WCAG22"], "path encoding collision and reversible overwrite refusal"),
    (13, "PREMIS and W3C PROV crosswalk with source semantic unit, target predicate, mapping version, cardinality, lossy flag, authority gap, and export refusal", "premis-prov-crosswalk", "GMUT Mind", "completed", ["SRC-PREMIS", "SRC-PROV-O"], "preservation-metadata crosswalk and lossy-export refusal"),
    (14, "Digital-object rights applicability board with source statement, licence identifier, jurisdiction placeholder, embargo interval, orphan-work gap, permitted-action reservation, and access hold", "rights-applicability-hold", "Freed ID and CBR Heart", "completed", ["SRC-PREMIS", "SRC-PRIVACY-ACT"], "rights applicability and access hold"),
    (15, "Preservation-metadata personal-data minimization ledger with field purpose, sensitivity class, retention basis placeholder, redaction lineage, disclosure boundary, and deletion nonauthorization", "personal-data-minimization", "Freed ID and CBR Heart", "completed", ["SRC-PRIVACY-ACT", "SRC-PREMIS"], "personal-data minimization and disclosure hold"),
    (16, "Encrypted preservation-container custody record with container format, cipher-suite placeholder, key absence, escrow reservation, ciphertext fixity, unlock attempts, and decryption refusal", "encrypted-container-custody", "Freed ID and CBR Heart", "completed", ["SRC-NIST-SHS", "SRC-PREMIS"], "encrypted-container custody and decryption refusal"),
    (17, "Audiovisual preservation-derivative manifest with source bitstream, codec and container, parameter set, frame or sample count, colour and channel semantics, fixity, and quality-claim refusal", "av-derivative-provenance", "GMUT Mind", "completed", ["SRC-LOC-RFS", "SRC-PREMIS"], "audiovisual derivative provenance and quality-claim refusal"),
    (18, "Geospatial preservation record with coordinate-reference-system identifier, axis order, coordinate epoch, extent, no-data semantics, sidecar binding, and transform hold", "geospatial-crs-preservation", "GMUT Mind", "completed", ["SRC-LOC-RFS", "SRC-PROV-O"], "geospatial reference-system binding and transform hold"),
    (19, "Database logical-dump preservation manifest with engine and version, schema hash, table and row-count ledger, collation, transaction boundary, dependency set, and restore-claim refusal", "database-logical-dump", "GMUT Mind", "completed", ["SRC-PREMIS", "SRC-NDSA-LEVELS"], "database logical-dump lineage and restore-claim refusal"),
    (20, "Software-source preservation package with commit-object graph, submodule and vendored dependency manifest, build-environment hash, licence map, generated-artifact boundary, and reproducibility hold", "software-source-archive", "GMUT Mind", "completed", ["SRC-PREMIS", "SRC-LOC-RFS"], "software-source archive lineage and reproducibility hold"),
    (21, "GMUT bit-rot hazard field with storage-medium state, latent-error-rate symbol, inspection interval, redundancy relation, unit and domain typing, and observation firewall", "gmut-bitrot-hazard", "GMUT Mind", "completed", ["SRC-NDSA-LEVELS", "SRC-NIST-SHS"], "typed bit-rot hazard obligations and observation firewall"),
    (22, "GMUT migration-loss transform with representation space, declared invariant set, tolerance symbol, non-invertibility marker, uncertainty term, and empirical-validation firewall", "gmut-migration-loss", "GMUT Mind", "completed", ["SRC-PREMIS", "SRC-LOC-RFS"], "typed migration-loss obligations and empirical firewall"),
    (23, "GMUT digital-object dependency survivability graph with runtime nodes, version constraints, missing-edge state, minimal-environment candidate, nonuniqueness, and proof firewall", "gmut-dependency-survivability", "GMUT Mind", "completed", ["SRC-PREMIS", "SRC-PROV-O"], "typed dependency survivability obligations and proof firewall"),
    (24, "THOS digital-preservation incident triage proxy with detection source, fixity failure, quarantine state, work queue, fatigue limit, two-person readback, and shift handover", "thos-preservation-incident", "THOS Body", "represented", ["SRC-NDSA-LEVELS", "SRC-PREMIS"], "preservation-incident triage and handover proxy"),
    (25, "THOS preservation backlog proxy with package risk class, dependency blocker, work-in-progress ceiling, pause checkpoint, stop-work placeholder, responsibility transfer, and next-shift acknowledgement", "thos-preservation-backlog", "THOS Body", "represented", ["SRC-NDSA-LEVELS", "SRC-WCAG22"], "preservation backlog and responsibility-transfer proxy"),
    (26, "Freed ID synthetic W3C VC 2.0 preservation-exception credential with evidence graph, holder-binding gap, credential-status omission, selective-disclosure absence, revocation reserve, and offline nonproduction boundary", "vc20-preservation-custody", "Freed ID and CBR Heart", "represented", ["SRC-W3C-VC20", "SRC-PRIVACY-ACT"], "synthetic preservation-exception credential with absent trust"),
    (27, "Freed ID synthetic RFC 8392 CWT checksum-challenge envelope with COSE-type placeholder, payload-manifest root, freshness window, verifier gap, detached-key absence, and offline-only rejection", "cwt-storage-audit", "Freed ID and CBR Heart", "represented", ["SRC-RFC8392", "SRC-NIST-SHS"], "synthetic checksum-challenge envelope with key and verifier gaps"),
    (28, "Freed ID synthetic W3C PROV preservation-agent event mapping with entity, activity, agent placeholder, qualified role, source statement, authority gap, correction lineage, and no-interoperability claim", "prov-preservation-agent", "Freed ID and CBR Heart", "represented", ["SRC-PROV-O", "SRC-PREMIS"], "synthetic preservation-agent mapping with authority and interoperability gaps"),
    (29, "GMUT real digital-repository fixity and repair event series with object identifiers, algorithm versions, storage domains, missingness, clock provenance, uncertainty, and zero-row likelihood-refusal adapter", "repository-event-zero-row", "GMUT Mind", "open_gap", ["SRC-PREMIS", "SRC-NDSA-LEVELS", "SRC-NIST-SHS"], "real repository event-data readiness"),
    (30, "CBR Indigenous and culturally sensitive digital-collection reservation for ownership, custody, access, retention, deletion, disclosure, return, repatriation, remedy, affected-community, legal, data-governance, and Māori authority", "digital-authority-reservation", "Freed ID and CBR Heart", "exact_gate", ["SRC-TE-MANA", "SRC-LOCAL-CONTEXTS", "SRC-PRIVACY-ACT"], "digital collection decision rights and Māori-authority reservation"),
]
PROPOSALS = [_proposal(*row) for row in _P]


def _source(source_id, status, kind, title, url, implication):
    return {
        "source_id": source_id,
        "status": status,
        "kind": kind,
        "title": title,
        "url": url,
        "phase_implication": implication,
    }


SOURCES = [
    _source("SRC-PREMIS", "current", "official_library_standard", "PREMIS Data Dictionary for Preservation Metadata version 3.0", "https://www.loc.gov/standards/premis/", "Preservation metadata entities and semantic units only; no repository conformance, custody truth, or professional authority."),
    _source("SRC-BAGIT", "stable", "primary_internet_standard", "RFC 8493 BagIt File Packaging Format version 1.0", "https://www.rfc-editor.org/rfc/rfc8493.html", "Package structure and path rules only; no real transfer integrity, repository acceptance, or operational assurance."),
    _source("SRC-NIST-SHS", "watch", "official_technical_standard", "NIST FIPS 180-4 Secure Hash Standard", "https://csrc.nist.gov/pubs/fips/180-4/upd1/final", "Digest vocabulary only; revision remains watched and no cryptographic implementation, certification, security completeness, or custody decision is established."),
    _source("SRC-LOC-RFS", "current", "official_library_guidance", "Library of Congress Recommended Formats Statement 2025-2026", "https://www.loc.gov/preservation/resources/rfs/", "Format sustainability factors only; no local collection policy, migration decision, or long-term-access guarantee."),
    _source("SRC-NDSA-LEVELS", "current", "professional_practice_guidance", "NDSA Levels of Digital Preservation version 2.1", "https://www.ndsa.org/publications/levels-of-digital-preservation/", "Program-improvement context only; no repository assessment, certification, staffing decision, or professional competence."),
    _source("SRC-PROV-O", "stable", "official_web_standard", "W3C PROV-O Recommendation", "https://www.w3.org/TR/prov-o/", "Provenance vocabulary only; no source truth, agent authority, semantic completeness, or interoperability claim."),
    _source("SRC-RFC3339", "stable", "primary_internet_standard", "RFC 3339 Date and Time on the Internet", "https://www.rfc-editor.org/rfc/rfc3339.html", "Timestamp syntax only; no clock accuracy, ordering truth, or traceability."),
    _source("SRC-WCAG22", "current", "official_web_standard", "W3C Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Structural checks only; manual, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved."),
    _source("SRC-W3C-VC20", "current", "official_web_standard", "W3C Verifiable Credentials Data Model v2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Synthetic field obligations only; no real issuer, holder, subject, key, proof, status, trust, or interoperability event."),
    _source("SRC-RFC8392", "stable", "primary_internet_standard", "RFC 8392 CBOR Web Token", "https://www.rfc-editor.org/rfc/rfc8392.html", "Synthetic token fields only; no real key, token, device, issuance, verification, or production event."),
    _source("SRC-PRIVACY-ACT", "watch", "official_legislation", "Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/0031/latest/contents.html", "Watched legal context only; no privacy compliance, consent, disclosure, retention, deletion, or identity decision."),
    _source("SRC-TE-MANA", "current", "maori_authority_source", "Te Mana Raraunga principles of Māori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data decisions remain under Māori authority; no authority is delegated to the repository."),
    _source("SRC-LOCAL-CONTEXTS", "current", "affected_community_governance_source", "Local Contexts Traditional Knowledge Labels", "https://localcontexts.org/labels/traditional-knowledge-labels/", "Cultural and traditional-knowledge rights reservation only; no label is selected or applied."),
]

SAFE_TASKS = [
    f"Build and validate bounded contract and rejecting fixtures for {p['proposal_id']} {p['slug']}"
    for p in PROPOSALS
]
CANDIDATE_TASKS = [
    f"Resolve only the declared bounded acceptance gate for {p['proposal_id']} {p['mission_surface']}"
    for p in PROPOSALS
]
SKILL_IDEAS = [
    "ghc-family-preservation-package-integrity",
    "ghc-family-bagit-validity-firewall",
    "ghc-family-fixity-mismatch-quarantine",
    "ghc-family-format-risk-reservation",
    "ghc-family-migration-event-lineage",
    "ghc-family-replica-scrub-reservation",
    "ghc-family-preservation-metadata-crosswalk",
    "ghc-family-gmut-preservation-typing",
    "ghc-family-thos-preservation-handover",
    "ghc-family-digital-authority-reservation",
]
RUNNER_IDEAS = [
    "ghc_family_preservation_package_integrity.py",
    "ghc_family_bagit_validity_firewall.py",
    "ghc_family_fixity_mismatch_quarantine.py",
    "ghc_family_format_risk_reservation.py",
    "ghc_family_migration_event_lineage.py",
    "ghc_family_replica_scrub_reservation.py",
    "ghc_family_preservation_metadata_crosswalk.py",
    "ghc_family_gmut_preservation_fields.py",
    "ghc_family_thos_preservation_proxy.py",
    "ghc_family_v654_v6_bounded_suite.py",
]
CLEAN_TASKS = [
    f"{kind} owner-scoped {surface} without deletion, history rewrite, sibling mutation, "
    "gate weakening, or unsupported promotion"
    for kind in ("CLEAN", "FIX", "REFINE")
    for surface in (
        "schema clarity",
        "source status",
        "digest algorithm status",
        "package identifier binding",
        "privacy boundary",
        "authority reservation",
        "rollback wording",
        "accessible structure",
        "manifest coverage",
        "stale-label refusal",
    )
]


def _negative(number, signature, failed, recovery, guard):
    return {
        "negative_id": f"V6546-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


INHERITED_EXTERNAL_NEGATIVE_RECORDS = [
    {
        "negative_id": f"AUTH-STATE-N{index:02d}",
        "source": "ghc-family-auth-permission-state current-state v2",
        "credit": "retained_negative_zero_initial_pass_credit",
    }
    for index in range(1, INHERITED_EXTERNAL_NEGATIVES + 1)
]

X1_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "unsupported_sha256_hashdata_api",
        "The first activation-baton digest probe assumed a static SHA256 HashData API that is unavailable in the current PowerShell runtime, so it returned no digest credit.",
        "Use SHA256.Create().ComputeHash on the exact file bytes, dispose the instance, and compare the resulting lowercase digest with the baton receipt.",
        "Probe runtime support before selecting a static cryptographic helper; preserve raw-byte hashing.",
    ),
    _negative(
        2,
        "bounded_baton_read_timeout",
        "One bounded activation-baton read timed out after returning only lines 1201 through 1222, so the partial output earned no complete-read credit.",
        "Resume at the next unread line with a longer bounded literal-path read and verify the terminal line count.",
        "Read large archive-backed documents in bounded ranges with an explicit continuation cursor and adequate timeout.",
    ),
    _negative(
        3,
        "powershell_foreach_pipeline_parse_error",
        "The first six-skill inventory command piped directly from a foreach block and failed with an empty-pipe parse error before reading any skill metadata.",
        "Materialize the foreach results into an array before piping them to Format-Table.",
        "On Windows PowerShell, materialize foreach output before any trailing pipeline.",
    ),
    _negative(
        4,
        "powershell_foreach_pipeline_parse_error_recurrence",
        "The first ancestry audit repeated the direct foreach-to-pipeline pattern and failed with the same parse error, earning zero ancestry credit.",
        "Apply the validated array-materialization guard, then run parent-count, ancestor, and merge-count checks as bounded read-only probes.",
        "Treat the materialization guard as mandatory for every future foreach result pipeline in this runtime.",
    ),
    _negative(
        5,
        "recursive_agents_inventory_timeout",
        "A recursive filesystem search for AGENTS.md exceeded its archive-backed timeout and returned no instruction-discovery result.",
        "Use the Git index with an exact AGENTS.md glob and verify the clean worktree has no untracked instruction file.",
        "Prefer the repository index over recursive filesystem traversal for tracked instruction-file discovery.",
    ),
    _negative(
        6,
        "phase_data_patch_context_mismatch",
        "The first targeted phase-data patch missed because one context line had already changed during the mechanical phase-name rewrite; no content changed.",
        "Read the exact local line window and apply a narrower context patch to the current text.",
        "After mechanical rewrites, reread the target block before applying semantic patches.",
    ),
    _negative(
        7,
        "powershell_foreach_pipeline_parse_error_second_recurrence",
        "A source-manifest projection again piped directly from a foreach block and failed with the same empty-pipe parse error, earning zero manifest evidence.",
        "Materialize the projection rows into an array before formatting and retain the repeated failure separately.",
        "Require the materialization guard before every foreach result pipeline; do not rely on recollection alone.",
    ),
    _negative(
        8,
        "first_1810_title_novelty_screen_failed",
        "The first complete 1,810-title novelty screen rejected two synthetic identity-profile titles whose token overlap with Eiren's immediately preceding profiles exceeded the frozen threshold.",
        "Keep the standard families and evidence boundaries, but revise only the duplicated mechanisms and vocabulary before rerunning the complete read-only title screen.",
        "Run the complete inherited-title screen before any x1 artifact build and never lower the preregistered threshold to admit a collision.",
    ),
    _negative(
        9,
        "x1_builder_wrapper_timeout_with_late_child_completion",
        "The x1 packet-builder wrapper exceeded its 60-second bound and returned no terminal receipt while the child continued exact Git-blob manifest hashing.",
        "Audit the exact child process and expected artifacts before retrying, wait one bounded interval, and preserve the completed artifact set when the same child exits.",
        "After a builder timeout, inspect process state and exact receipts before any retry; never launch a duplicate while the original child remains live.",
    ),
]

REJECTED_COLLISIONS = [
    {"candidate": "generic digital preservation checklist", "reason": "Too broad to distinguish package, fixity, format, dependency, replica, rights, privacy, and authority mechanisms."},
    {"candidate": "generic checksum verification", "reason": "Split into package manifests, fixity events, scrub schedules, replica topology, and algorithm-status controls."},
    {"candidate": "generic format migration", "reason": "Split into identification conflict, risk review, migration lineage, loss typing, and publication hold."},
    {"candidate": "generic repository backup", "reason": "Split into fault domains, storage media, sync state, independence signals, scrub evidence, and deletion holds."},
    {"candidate": "generic preservation metadata", "reason": "Split into PREMIS event records, PROV crosswalks, timestamps, rights, personal-data minimization, and agent placeholders."},
    {"candidate": "generic software reproducibility", "reason": "Split into source-object graphs, dependencies, build-environment hashes, generated artifacts, and an explicit reproducibility hold."},
    {"candidate": "generic accessibility checklist", "reason": "Limited to structural status and handover surfaces while manual and affected-user evaluation remains reserved."},
    {"candidate": "generic Indigenous data governance", "reason": "Replaced by explicit ownership, custody, access, retention, deletion, disclosure, return, remedy, affected-community, and Māori-authority reservations."},
    {"candidate": "production identity for preservation", "reason": "Narrowed to synthetic VC, CWT, and PROV profiles with absent keys, trust, status, authority, and interoperability."},
    {"candidate": "real repository reliability analysis", "reason": "Requires repository access, event data, operational context, authority, and independent review; narrowed to zero-row readiness."},
]
