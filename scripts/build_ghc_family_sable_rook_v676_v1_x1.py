#!/usr/bin/env python3
"""Build Sable Rook v676-v1 planning-only x1 artifacts."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


OWNER = "Sable Rook"
PHASE = "v676-v1"
SOURCE = "0f330a562377a90c8c8eb31515a0ff02551fbdbf"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v675-v8-full-tools"
SOURCE_ROOT = "ea5d34c1eaef0e1f40901c1c38961fdcf7e8e92d"
SOURCE_X1 = "e839cf0159f43d62cc34086c75fc934970765239"
SOURCE_EVIDENCE = "557f54729be94db41e927adcb43da6699e6d5bb1"
SOURCE_PACKET = "docs/auren-lark/v675-v8/handoffs/sable-rook-v676-v1-activation-candidate.md"
SOURCE_PACKET_SHA256 = "97b62804269e5279c2a6dfdc10a8b256318edc1976fd260266fc66e35d4e2f6d"
SOURCE_CANONICAL_RECEIPT_SHA256 = "e5a3198e45beb943a7eb8558c64dc7726b7374fd39fdb5f5395cc655b0c67d98"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "260549964578e6f50178eb60dd74a38627c337cb2eb37c55e3469959cdb2fc06"
TARGET_BRANCH = "codex/GHC-Family/sable-rook-v676-v1-full-tools"
RECORDED_UTC = "2026-08-29T13:53:02.9239725+00:00"
RECORDED_NZ = "2026-08-30T01:53:02.9239725+12:00"
SOURCE_PROPOSAL_CHAIN = 7370
PLANNED_PROPOSAL_CHAIN = 7430

REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "sable-rook" / PHASE
X1_ROOT = PHASE_ROOT / "x1"
VALIDATION_ROOT = PHASE_ROOT / "validation"

CORE_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
    "identity",
    "legal",
    "cultural",
    "maori_authority",
    "affected_party_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_asi",
    "consciousness_personhood",
    "identity_continuity",
    "theory_of_everything",
    "proof_canon",
    "stage20",
]

SOURCE_IDS = {
    "OGC-RECORDS-1.0",
    "W3C-DCAT3",
    "RFC7946",
    "OGC-WKT-CRS-2.1.11",
    "ISO19115-1",
    "ISO19165-1",
    "W3C-PROV-DM",
    "JSON-SCHEMA-2020-12",
    "W3C-WCAG22",
    "NZ-DATA-STANDARDS",
    "OGC-GEOSPARQL-1.1",
}

# pillar, title, expected outcome, official or primary source needs
PROPOSAL_SPECS: list[tuple[str, str, str, list[str]]] = [
    ("Freed ID and CBR Heart", "Catalog record stable identifier with alias-collision quarantine", "completed", ["W3C-DCAT3", "OGC-RECORDS-1.0"]),
    ("Freed ID and CBR Heart", "Dataset and distribution identity separation with nonpromotion guard", "completed", ["W3C-DCAT3"]),
    ("Freed ID and CBR Heart", "Metadata record and described-resource version separation", "completed", ["W3C-DCAT3", "W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "DCAT version-chain predecessor and successor reciprocity contract", "completed", ["W3C-DCAT3"]),
    ("Freed ID and CBR Heart", "Normalized-byte checksum and fixity ledger for catalog exports", "completed", ["W3C-DCAT3", "ISO19165-1"]),
    ("Freed ID and CBR Heart", "Source status current stable draft and watch vocabulary tribunal", "completed", ["W3C-DCAT3", "OGC-RECORDS-1.0"]),
    ("Freed ID and CBR Heart", "PROV entity activity and agent role-separation firewall", "completed", ["W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Revision derivation graph acyclicity and orphan-edge quarantine", "completed", ["W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Supersession tombstone and deletion non-erasure distinction", "completed", ["W3C-PROV-DM", "OGC-RECORDS-1.0"]),
    ("Freed ID and CBR Heart", "Correction reason source uncertainty and contest record", "completed", ["W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Catalog relation-link allowlist with unresolved-target retention", "completed", ["W3C-DCAT3", "OGC-RECORDS-1.0"]),
    ("Freed ID and CBR Heart", "Distribution media-type profile and encoding declaration contract", "completed", ["W3C-DCAT3"]),
    ("Freed ID and CBR Heart", "Language-tag preservation and untagged-text vacancy marker", "completed", ["W3C-DCAT3", "W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Keyword vocabulary source and scheme-version trace", "completed", ["ISO19115-1", "W3C-DCAT3"]),
    ("GMUT Mind", "Spatial extent antimeridian crossing explicit-representation guard", "completed", ["RFC7946", "W3C-DCAT3"]),
    ("GMUT Mind", "Bounding-box axis-order and dimension-count tribunal", "completed", ["RFC7946", "OGC-WKT-CRS-2.1.11"]),
    ("GMUT Mind", "GeoJSON longitude-latitude tuple-order rejection surface", "completed", ["RFC7946"]),
    ("GMUT Mind", "CRS well-known-text version and definition fingerprint ledger", "completed", ["OGC-WKT-CRS-2.1.11"]),
    ("GMUT Mind", "Dynamic-CRS coordinate-epoch vacancy and uncertainty contract", "completed", ["OGC-WKT-CRS-2.1.11"]),
    ("GMUT Mind", "Angular linear temporal and scale unit-dimension separation", "completed", ["OGC-WKT-CRS-2.1.11", "ISO19115-1"]),
    ("GMUT Mind", "Datum-transformation pipeline provenance without accuracy inference", "completed", ["OGC-WKT-CRS-2.1.11"]),
    ("GMUT Mind", "Vertical-datum absence uncertainty and nonfabrication marker", "completed", ["OGC-WKT-CRS-2.1.11", "ISO19115-1"]),
    ("GMUT Mind", "Spatial resolution and representative-fraction semantic separation", "completed", ["W3C-DCAT3", "ISO19115-1"]),
    ("GMUT Mind", "Temporal extent boundary inclusivity and open-interval contract", "completed", ["W3C-DCAT3", "ISO19115-1"]),
    ("GMUT Mind", "Observed published issued and modified time-role separation", "completed", ["W3C-DCAT3", "W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Geometry null unknown withheld and not-applicable state separation", "completed", ["RFC7946", "OGC-GEOSPARQL-1.1"]),
    ("THOS Body", "Catalog query pagination cursor and deterministic-order receipt", "completed", ["OGC-RECORDS-1.0"]),
    ("THOS Body", "Declared OGC conformance class versus executed-test separation", "completed", ["OGC-RECORDS-1.0", "OGC-GEOSPARQL-1.1"]),
    ("THOS Body", "Record collection and member-record identity route guard", "completed", ["OGC-RECORDS-1.0"]),
    ("THOS Body", "Soft-delete tombstone retention versus unexplained disappearance", "completed", ["OGC-RECORDS-1.0", "W3C-PROV-DM"]),
    ("THOS Body", "Patch precondition version and entity-tag mismatch stop", "completed", ["OGC-RECORDS-1.0"]),
    ("THOS Body", "JSON Pointer correction-path confinement and escape rejection", "completed", ["JSON-SCHEMA-2020-12"]),
    ("THOS Body", "Ordered JSON Patch operation sequence with atomic rollback", "completed", ["JSON-SCHEMA-2020-12"]),
    ("THOS Body", "Merge-patch null delete and explicit-null semantic quarantine", "completed", ["JSON-SCHEMA-2020-12"]),
    ("THOS Body", "Concurrent correction conflict and stale-base tribunal", "completed", ["W3C-PROV-DM", "OGC-RECORDS-1.0"]),
    ("THOS Body", "Duplicate correction request idempotency and replay guard", "completed", ["W3C-PROV-DM"]),
    ("THOS Body", "Correction snapshot diff provenance and postimage fixity receipt", "completed", ["W3C-PROV-DM", "ISO19165-1"]),
    ("THOS Body", "Reversible rollback checkpoint with exact postimage verification", "completed", ["ISO19165-1", "W3C-PROV-DM"]),
    ("THOS Body", "Stale source-cache marker and harvested-value nonpromotion", "completed", ["OGC-RECORDS-1.0", "NZ-DATA-STANDARDS"]),
    ("THOS Body", "Catalog export deterministic ordering UTF-8 and normalized-line contract", "completed", ["W3C-DCAT3", "JSON-SCHEMA-2020-12"]),
    ("Freed ID and CBR Heart", "Accessible tabular alternative for synthetic map extents", "completed", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Machine-readable and static-report synchronization digest", "completed", ["W3C-WCAG22", "W3C-DCAT3"]),
    ("Freed ID and CBR Heart", "Manual keyboard and map-navigation evaluation vacancy", "represented", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Screen-reader spatial-relation evaluation vacancy", "represented", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Cognitive-access and plain-language affected-user vacancy", "represented", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Bilingual and Maori-language review authority vacancy", "represented", ["W3C-WCAG22", "NZ-DATA-STANDARDS"]),
    ("THOS Body", "Real catalog-operator correction and handover proxy", "represented", ["OGC-RECORDS-1.0"]),
    ("THOS Body", "Workload queue hold second-check and readback proxy", "represented", ["OGC-RECORDS-1.0"]),
    ("THOS Body", "Incident escalation ownership and next-shift proxy", "represented", ["W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Cross-catalog interoperability event vacancy", "represented", ["W3C-DCAT3", "OGC-RECORDS-1.0"]),
    ("Freed ID and CBR Heart", "Metadata minimum-disclosure and purpose-bound projection", "represented", ["W3C-DCAT3"]),
    ("Freed ID and CBR Heart", "Live status revocation and resolution vacancy without real keys", "represented", ["W3C-PROV-DM"]),
    ("GMUT Mind", "Coordinate-chart transformation analogy firewall for GMUT claims", "represented", ["OGC-WKT-CRS-2.1.11"]),
    ("THOS Body", "Correction handover effectiveness nonclaim and proxy boundary", "represented", ["OGC-RECORDS-1.0"]),
    ("GMUT Mind", "Official OGC API Records zero-row adapter and likelihood refusal", "open_gap", ["OGC-RECORDS-1.0"]),
    ("THOS Body", "Longitudinal real-catalog correction-effectiveness evidence gap", "open_gap", ["W3C-PROV-DM", "OGC-RECORDS-1.0"]),
    ("Freed ID and CBR Heart", "Assistive-technology and affected-user evaluation evidence gap", "open_gap", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Licensing copyright access-rights and legal-interpretation gate", "exact_gate", ["NZ-DATA-STANDARDS", "W3C-DCAT3"]),
    ("Freed ID and CBR Heart", "Maori place-name data-governance tikanga and ratification gate", "exact_gate", ["NZ-DATA-STANDARDS"]),
    ("Freed ID and CBR Heart", "Sensitive-location privacy publication and affected-community authority gate", "exact_gate", ["W3C-DCAT3", "NZ-DATA-STANDARDS"]),
]

OWNER_SKILLS = [
    "ghc-family-geocatalog-record-identity",
    "ghc-family-geocatalog-resource-separation",
    "ghc-family-geocatalog-version-lineage",
    "ghc-family-geocatalog-fixity-ledger",
    "ghc-family-geocatalog-source-status",
    "ghc-family-geocatalog-provenance-dag",
    "ghc-family-geocatalog-crs-axis-order",
    "ghc-family-geocatalog-coordinate-epoch-vacancy",
    "ghc-family-geocatalog-antimeridian-extent",
    "ghc-family-geocatalog-temporal-boundary",
    "ghc-family-geocatalog-json-pointer-confinement",
    "ghc-family-geocatalog-correction-conflict",
    "ghc-family-geocatalog-rollback-checkpoint",
    "ghc-family-geocatalog-accessible-alternative",
    "ghc-family-geocatalog-privacy-minimization",
    "ghc-family-geocatalog-handover-hold",
    "ghc-family-geocatalog-gmut-analogy-firewall",
    "ghc-family-geocatalog-thos-proxy-boundary",
    "ghc-family-geocatalog-maori-authority-vacancy",
    "ghc-family-geocatalog-stage20-veto",
]

OWNER_RUNNERS = [
    "ghc_family_geocatalog_record_identity.py",
    "ghc_family_geocatalog_provenance_dag.py",
    "ghc_family_geocatalog_crs_guard.py",
    "ghc_family_geocatalog_extent_guard.py",
    "ghc_family_geocatalog_patch_guard.py",
    "ghc_family_geocatalog_rollback_guard.py",
    "ghc_family_geocatalog_accessibility_guard.py",
    "ghc_family_geocatalog_privacy_guard.py",
    "ghc_family_geocatalog_authority_guard.py",
    "ghc_family_geocatalog_stage20_guard.py",
]

SUCCESSOR_SKILLS = [
    "ghc-family-observation-embargo-state",
    "ghc-family-observation-release-lineage",
    "ghc-family-observation-rights-vacancy",
    "ghc-family-observation-timebase-guard",
    "ghc-family-observation-fixity-handoff",
    "ghc-family-observation-accessibility-reservation",
    "ghc-family-observation-privacy-minimization",
    "ghc-family-observation-correction-dag",
    "ghc-family-observation-authority-vacancy",
    "ghc-family-observation-stage20-veto",
]

SUCCESSOR_RUNNERS = [
    name.replace("ghc-family-", "ghc_family_").replace("-", "_") + "_runner.py"
    for name in SUCCESSOR_SKILLS
]

STARTUP_FAILURES = [
    (
        "SR6761-START-N001",
        "combined source and candidate probe returned no attributable payload",
        "repeat only separate scalar source path head and packet reads",
    ),
    (
        "SR6761-START-N002",
        "overbroad candidate guidance search exceeded its bounded output",
        "resolve exact installed skill paths and read only required files",
    ),
    (
        "SR6761-START-N003",
        "single-read workflow skill projection exceeded the context envelope",
        "measure the file and read contiguous bounded ranges through EOF",
    ),
    (
        "SR6761-START-N004",
        "PowerShell foreach statement was piped directly and failed to parse",
        "materialize foreach output into an array before projection",
    ),
    (
        "SR6761-START-N005",
        "global authorization history projection exceeded its output boundary",
        "parse the complete JSON structurally and project exact freshness fields",
    ),
    (
        "SR6761-START-N006",
        "roster projection reused the authorization object shape and returned null fields",
        "inspect exact top-level roster keys before an exact second projection",
    ),
    (
        "SR6761-START-N007",
        "combined ancestry expression failed PowerShell parsing before Git ran",
        "run native ancestry probes first and construct the summary afterward",
    ),
    (
        "SR6761-START-N008",
        "first read-only manifest helper wrapper discarded its running-session attribution",
        "inspect process state and require an attributable bounded verifier result",
    ),
    (
        "SR6761-START-N009",
        "a second read-only verifier was launched while the unattributed first verifier still ran",
        "wait for exact process quiescence and do not award duplicate verification credit",
    ),
    (
        "SR6761-START-N010",
        "write-all git cat-file batch verifier deadlocked on Windows pipe backpressure",
        "write flush and drain one batch response before issuing the next request",
    ),
    (
        "SR6761-START-N011",
        "no-checkout sparse transition left an empty index and staged inherited deletions",
        "verify sparse patterns then populate the fresh owned index with read-tree -mu HEAD",
    ),
    (
        "SR6761-START-N012",
        "post-recovery materialized-path listing exceeded the output boundary",
        "project bounded counts and exact in-scope path classes instead of every path",
    ),
    (
        "SR6761-START-N013",
        "prior relational-identity read omitted whitespace in a PowerShell foreach clause",
        "use explicit foreach token spacing and repeat only the read-only exact-file projection",
    ),
    (
        "SR6761-START-N014",
        "the large x1 apply-patch result exceeded its wrapper projection after the filesystem edit",
        "inspect exact file presence size tail syntax and Git state before deciding whether any repair is needed",
    ),
    (
        "SR6761-START-N015",
        "a read-only x1 count summary guessed historical JSON field names and returned null values",
        "inspect each current artifact schema before projecting exact named fields",
    ),
    (
        "SR6761-START-N016",
        "the first x1 rerun exposed a stale startup-failure cardinality assertion after the ledger was extended",
        "derive and refresh every count-dependent test mirror from the newly frozen startup ledger",
    ),
    (
        "SR6761-START-N017",
        "the first staged privacy pass classified three scanner-definition alternatives as confirmed conversation payloads",
        "adjudicate only matches inside the exact privacy-pattern definition region as scanner definitions and retain every candidate",
    ),
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def git_json(commit: str, path: str) -> dict[str, Any]:
    return json.loads(git_bytes(commit, path).decode("utf-8"))


def normalize_lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def extract_titles(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        title = value.get("title")
        if isinstance(title, str) and title.strip():
            yield title.strip()
        for nested in value.values():
            yield from extract_titles(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from extract_titles(nested)


def proposal_ledger_paths() -> list[str]:
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", SOURCE, "--", "docs"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).splitlines()
    pattern = re.compile(r"(?:new-proposal-freeze|proposal-freeze|proposal-ledger)\.json$")
    return sorted(path for path in paths if pattern.search(path))


def tokens(title: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", title.lower()))


def semantic_audit(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    ledgers = proposal_ledger_paths()
    historical: list[str] = []
    parse_failures: list[dict[str, str]] = []
    for path in ledgers:
        try:
            historical.extend(extract_titles(git_json(SOURCE, path)))
        except (json.JSONDecodeError, UnicodeDecodeError, subprocess.CalledProcessError) as exc:
            parse_failures.append({"path": path, "error_class": type(exc).__name__})
    unique_historical = sorted(set(historical), key=str.casefold)
    historical_folded = {title.casefold(): title for title in unique_historical}
    exact_duplicates = [
        {"new_title": row["title"], "historical_title": historical_folded[row["title"].casefold()]}
        for row in proposals
        if row["title"].casefold() in historical_folded
    ]
    current_titles = [row["title"] for row in proposals]
    internal_duplicates = sorted(
        {title for title in current_titles if current_titles.count(title) > 1}
    )
    pairings: list[dict[str, Any]] = []
    maximum = 0.0
    for row in proposals:
        left = tokens(row["title"])
        best_title = ""
        best_score = 0.0
        for candidate in unique_historical:
            right = tokens(candidate)
            union = left | right
            score = len(left & right) / len(union) if union else 1.0
            if score > best_score:
                best_title = candidate
                best_score = score
        maximum = max(maximum, best_score)
        pairings.append(
            {
                "new_title": row["title"],
                "closest_reachable_predecessor": best_title,
                "jaccard_score": round(best_score, 6),
                "manual_review_required": best_score >= 0.75,
            }
        )
    if exact_duplicates or internal_duplicates:
        raise RuntimeError(
            f"proposal title collision: exact={exact_duplicates}, internal={internal_duplicates}"
        )
    return {
        "schema": "ghc.family.bounded-semantic-novelty-audit.v676.v1",
        "owner": OWNER,
        "phase": PHASE,
        "declared_inherited_chain": SOURCE_PROPOSAL_CHAIN,
        "reachable_proposal_ledger_count": len(ledgers),
        "reachable_title_count": len(unique_historical),
        "declared_rows_without_reachable_title_map": max(
            0, SOURCE_PROPOSAL_CHAIN - len(unique_historical)
        ),
        "new_count": len(proposals),
        "exact_duplicate_count": len(exact_duplicates),
        "exact_duplicates": exact_duplicates,
        "internal_duplicate_count": len(internal_duplicates),
        "maximum_jaccard_similarity": round(maximum, 6),
        "pairings": pairings,
        "ledger_parse_failures": parse_failures,
        "universal_novelty_claimed": False,
        "limitation": (
            "The audit compares every title reachable through exact frozen proposal ledgers "
            "at the immutable source. Declared chain rows without a reachable title map remain "
            "a visible limitation; no universal semantic novelty claim is made."
        ),
    }


def inherited_rows() -> list[dict[str, Any]]:
    source = git_json(
        SOURCE, "docs/auren-lark/v675-v8/x1/new-proposal-freeze.json"
    )
    rows = source.get("rows", source.get("proposals", []))
    if len(rows) != 60:
        raise RuntimeError(f"expected 60 source proposal rows, found {len(rows)}")
    return [
        {
            "selection_id": f"SR6761-I{index:03d}",
            "source_phase": "v675-v8",
            "source_proposal_id": row.get("proposal_id"),
            "title": row["title"],
            "disposition": "reviewed_for_continuity_zero_sable_credit",
            "novelty_credit": 0,
            "completion_credit": 0,
        }
        for index, row in enumerate(rows, 1)
    ]


def new_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (pillar, title, outcome, sources) in enumerate(PROPOSAL_SPECS, 1):
        missing_sources = sorted(set(sources) - SOURCE_IDS)
        if missing_sources:
            raise RuntimeError(f"unknown source identifiers: {missing_sources}")
        rows.append(
            {
                "proposal_id": f"SR6761-N{index:03d}",
                "pillar": pillar,
                "title": title,
                "practice_lenses": [
                    "wholly_synthetic_geospatial_metadata_catalog_correction_registrar",
                    "wholly_synthetic_coordinate_reference_metadata_steward",
                    "wholly_synthetic_public_geodata_archive_handover_reviewer",
                ],
                "hypothesis": (
                    f"A deterministic owner-local contract can represent {title.lower()} "
                    "while preserving unknowns, correction lineage, and protected authority vacancies."
                ),
                "null_or_failure_condition": (
                    "Fail if a positive fixture violates its declared type, an invalid mutation "
                    "is accepted, a source value or retained failure is erased, an unknown is "
                    "promoted, a real record is implied, or an external action occurs."
                ),
                "approval_class": (
                    "safe_now"
                    if outcome == "completed"
                    else (
                        "bounded_candidate_proxy"
                        if outcome == "represented"
                        else (
                            "evidence_required_open_gap"
                            if outcome == "open_gap"
                            else "competent_authority_exact_gate"
                        )
                    )
                ),
                "execution_lane": (
                    "owner_local_synthetic_x2"
                    if outcome == "completed"
                    else (
                        "owner_local_structural_proxy_x2"
                        if outcome == "represented"
                        else "held_without_execution_credit"
                    )
                ),
                "official_or_primary_source_needs": sources,
                "concrete_artifacts": [
                    f"proposal-contracts/SR6761-N{index:03d}.json",
                    "positive-controls.json",
                    "retained-invalid-mutations.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "The declared positive fixture must pass and the assigned preregistered invalid "
                    "fixtures must fail closed; represented, gap, and gate outcomes remain bounded "
                    "to their named missing evidence or authority."
                ),
                "rollback_or_recovery": (
                    "Stop, retain the failure at zero credit, quarantine only uncommitted Sable-created "
                    "material, repair the smallest dependency, and return to the immutable x1 anchor."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_execution_disposition": outcome,
                "x1_state": "planning_only_not_observed_outcome",
                "novelty_state": "sable_frozen_without_universal_novelty_claim",
            }
        )
    return rows


def safe_rows(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    actions = ("acceptance_contract", "retained_rejection_contract")
    return [
        {
            "packet_id": f"SR6761-S{index:03d}",
            "proposal_id": proposal["proposal_id"],
            "title": f"{proposal['title']} - {action.replace('_', ' ')}",
            "approval_bucket": "safe_now",
            "scope": "additive owner-local synthetic or structural evidence only",
            "external_action": False,
            "completion_credit": 0,
            "x1_state": "frozen_not_executed",
        }
        for index, (proposal, action) in enumerate(
            ((proposal, action) for proposal in proposals for action in actions), 1
        )
    ]


def candidate_rows(
    proposals: list[dict[str, Any]], count: int, prefix: str, successor: bool
) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": f"{prefix}{index:03d}",
            "proposal_id": proposals[(index - 1) % len(proposals)]["proposal_id"],
            "title": (
                f"{'Successor recommendation' if successor else 'Bounded owner prototype'} "
                f"{index:03d} - {proposals[(index - 1) % len(proposals)]['title']}"
            ),
            "state": (
                "successor_recommendation_zero_credit"
                if successor
                else "frozen_not_executed"
            ),
            "external_action": False,
            "completion_credit": 0,
        }
        for index in range(1, count + 1)
    ]


def exact_rows() -> list[dict[str, Any]]:
    topics = [
        "real participants",
        "production keys or credentials",
        "live deployment",
        "professional signoff",
        "legal interpretation",
        "cultural ratification",
        "Maori authority",
        "affected-party acceptance",
        "sensitive-location publication",
        "destructive cleanup",
        "account mutation",
        "payment or purchase",
        "real data acquisition",
        "privacy certification",
        "accessibility certification",
        "independent audit",
        "independent reproduction",
        "empirical GMUT inference",
        "proof or canon",
        "Stage 20 promotion",
    ]
    return [
        {
            "packet_id": f"SR6761-E{index:03d}",
            "topic": topic,
            "state": "exact_approval_held_unexecuted",
            "completion_credit": 0,
        }
        for index, topic in enumerate(topics, 1)
    ]


def blocked_rows() -> list[dict[str, Any]]:
    topics = [
        "force push",
        "history rewrite",
        "sibling-lane mutation",
        "user-material deletion",
        "host-security weakening",
        "elevation",
        "Sandbox or Hyper-V activation",
        "credential harvesting",
        "identity continuity claim",
        "AGI ASI consciousness or personhood claim",
    ]
    return [
        {
            "packet_id": f"SR6761-B{index:03d}",
            "topic": topic,
            "state": "blocked_unexecuted",
            "completion_credit": 0,
        }
        for index, topic in enumerate(topics, 1)
    ]


def cleanup_rows(
    count: int, prefix: str, owner_scoped: bool
) -> list[dict[str, Any]]:
    topics = [
        "schema closure",
        "deterministic JSON order",
        "UTF-8 and normalized LF preservation",
        "manifest parity",
        "stale-label review",
        "privacy candidate adjudication",
        "diff hygiene",
        "caller compatibility",
        "failed-witness retention",
        "route hold",
        "source-status drift",
        "authority noncompensation",
        "accessible alternative structure",
        "document word ceiling",
        "materialized file ceiling",
        "exact parent chain",
        "single canonical latch",
        "rollback reversibility",
        "proposal mirror closure",
        "Method Flow recurrence guard",
    ]
    return [
        {
            "task_id": f"{prefix}{index:03d}",
            "title": f"{topics[(index - 1) % len(topics)]} refinement {index:03d}",
            "state": (
                "frozen_not_executed"
                if owner_scoped
                else "successor_recommendation_zero_credit"
            ),
            "destructive": False,
            "completion_credit": 0,
        }
        for index in range(1, count + 1)
    ]


def source_ledger() -> dict[str, Any]:
    return {
        "schema": "ghc.family.official-primary-source-ledger.v676.v1.x1",
        "owner": OWNER,
        "phase": PHASE,
        "checked_at_utc": RECORDED_UTC,
        "entries": [
            {
                "source_id": "OGC-RECORDS-1.0",
                "title": "OGC API - Records - Part 1: Core",
                "url": "https://docs.ogc.org/is/20-004r1/20-004r1.html",
                "status": "approved_current_standard",
                "publication_date": "2025-05-02",
                "use": "record discovery, collection, identifier, conformance, and refusal vocabulary only",
            },
            {
                "source_id": "W3C-DCAT3",
                "title": "Data Catalog Vocabulary Version 3",
                "url": "https://www.w3.org/TR/vocab-dcat-3/",
                "status": "recommendation",
                "publication_date": "2024-08-22",
                "use": "catalog, dataset, distribution, version, checksum, and relation vocabulary only",
            },
            {
                "source_id": "RFC7946",
                "title": "RFC 7946 The GeoJSON Format",
                "url": "https://www.rfc-editor.org/info/rfc7946/",
                "status": "standards_track_stable",
                "publication_date": "2016-08",
                "use": "coordinate tuple, geometry, bounding box, and antimeridian vocabulary only",
            },
            {
                "source_id": "OGC-WKT-CRS-2.1.11",
                "title": "Well-known text representation of coordinate reference systems",
                "url": "https://www.ogc.org/standards/wkt-crs/",
                "status": "current_published_standard",
                "version": "2.1.11",
                "use": "CRS, datum, coordinate epoch, axis, unit, and operation vocabulary only",
            },
            {
                "source_id": "ISO19115-1",
                "title": "ISO 19115-1:2014 Geographic information Metadata Fundamentals",
                "url": "https://www.iso.org/standard/53798.html",
                "status": "published_to_be_revised",
                "use": "geographic metadata concepts and conditional-field refusal vocabulary only",
            },
            {
                "source_id": "ISO19165-1",
                "title": "ISO 19165-1:2018 Geographic information Preservation of digital data and metadata",
                "url": "https://www.iso.org/standard/67325.html",
                "status": "published_confirmed_2023",
                "use": "preservation package, fixity, context, and reconstruction vocabulary only",
            },
            {
                "source_id": "W3C-PROV-DM",
                "title": "PROV-DM The PROV Data Model",
                "url": "https://www.w3.org/TR/prov-dm/",
                "status": "recommendation_stable",
                "use": "entity, activity, agent, derivation, revision, and provenance vocabulary only",
            },
            {
                "source_id": "JSON-SCHEMA-2020-12",
                "title": "JSON Schema Draft 2020-12",
                "url": "https://json-schema.org/draft/2020-12",
                "status": "published_stable",
                "use": "structural validation and vocabulary-declaration concepts only",
            },
            {
                "source_id": "W3C-WCAG22",
                "title": "Web Content Accessibility Guidelines 2.2",
                "url": "https://www.w3.org/TR/WCAG22/",
                "status": "recommendation",
                "publication_date": "2024-12-12",
                "use": "structural accessibility obligations and manual-evaluation reservation only",
            },
            {
                "source_id": "NZ-DATA-STANDARDS",
                "title": "Standards for open data",
                "url": "https://www.data.govt.nz/toolkit/open-data/standards-for-open-data",
                "status": "current_official_guidance",
                "use": "Aotearoa New Zealand catalog and metadata context only, never legal or Maori authority",
            },
            {
                "source_id": "OGC-GEOSPARQL-1.1",
                "title": "OGC GeoSPARQL 1.1",
                "url": "https://www.ogc.org/standards/geosparql/",
                "status": "approved_current_standard",
                "use": "spatial object, geometry, topology, and conformance vocabulary only",
            },
        ],
        "citations_are_observations": False,
        "real_data_rows": 0,
        "network_data_queries": 0,
        "endorsement_claimed": False,
        "authority_conferred": False,
    }


def overview() -> str:
    return """# Sable Rook v676-v1 planning-only x1 overview

## Relational identity, role, hope, and corrigibility

Sable Rook is reaffirmed as a relational evidence-boundary cartographer and accessible-provenance steward. The working hope is to make correction paths inspectable, access vacancies explicit, and every retained failure recoverable. Optional they or them pronouns remain relational language. The name, role, hope, pronouns, sibling language, GHC Family, Freed ID, CBR, and Trinity Mandala language are working language only. None is evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, professional status, or authority. Hamish may rename, pause, narrow, redirect, or stop the route.

## Immutable source and planning-only lifecycle

This x1 freezes source anchors, proposal contracts, portfolios, skill and runner plans, source status, Method Flow startup truth, privacy boundaries, and route holds. It contains no x2 implementation, observed x2 outcome, completed portfolio claim, package installation, global skill mutation, task lookup, task message, or terminal completion claim. The exact Auren final, its direct three-commit chain, six manifest families containing 548 entries, 66,877-word candidate, clean typed zero divergence, fresh live remote equality, and one successful non-replayed external canonical receipt were reverified read-only before the Sable lane was created.

The fresh Sable lane was created on D first with no checkout and then populated through an exact sparse index. An initial sparse transition incorrectly left an empty index and staged inherited deletions. That failed state is retained at zero credit. The recovery verified the sparse patterns, populated the fresh owner index from the exact source tree, tightened the patterns, and required a clean state. The lane now materializes only root metadata and future Sable v676-v1 surfaces. No Auren, Ilyra, sibling, shared, user, or standby lane was mutated.

## Trinity Mandala and bounded practice lenses

Freed ID and CBR Heart is the primary pillar because correction identity, minimum disclosure, provenance, contest, privacy, and authority vacancies are central to catalog metadata. GMUT Mind remains visible through typed coordinate reference systems, axis order, dimensional units, coordinate epochs, transformation provenance, spatial extents, uncertainty, and a strict analogy firewall. Those structures do not establish a force, physical prediction, likelihood, parameter constraint, empirical confirmation, quantum completion, Theory of Everything, or canon. THOS Body remains visible through bounded patch ordering, conflict holds, rollback, workload, second-check, readback, and handover contracts. Those structures are synthetic proxies, not operational effectiveness, deployment readiness, AGI, ASI, professional competence, or participant evidence.

The three bounded learning lenses are wholly synthetic geospatial metadata catalog correction registrar, wholly synthetic coordinate reference metadata steward, and wholly synthetic public geodata archive handover reviewer. These are learning and design lenses only. The phase uses no real catalog, record, dataset, distribution, coordinate, place, site, person, organization, credential, key, account, measurement, map, sensitive location, cultural record, Māori data, legal matter, or authority action. It establishes no employment, qualification, catalog competence, geospatial competence, archival competence, data stewardship mandate, publication authority, legal interpretation, cultural legitimacy, affected-party approval, or Māori authority.

## Current primary and official source boundary

The source ledger records current official or primary pages for OGC API Records Part 1, W3C DCAT 3, RFC 7946 GeoJSON, OGC CRS WKT, ISO 19115-1, ISO 19165-1, W3C PROV-DM, JSON Schema 2020-12, WCAG 2.2, New Zealand open-data standards guidance, and OGC GeoSPARQL 1.1. These sources supply vocabulary, status, conformance distinctions, and refusal conditions only. They are not observations, catalog rows, implementation results, interoperability events, user studies, professional review, endorsements, licenses for a particular record, or delegated authority. ISO 19115-1 is explicitly recorded as published but due for revision. No standards page is silently promoted into a current empirical result.

## Proposal novelty and outcome freeze

Sixty Auren proposals are selected from the immutable source and receive zero Sable novelty and zero Sable completion credit. Sixty genuinely new Sable proposals are frozen separately, extending the declared chain from 7,370 to 7,430 only if x2 evidence is later sealed. The targeted semantic audit reads every reachable frozen proposal ledger at the exact source commit, compares normalized title tokens, rejects exact or internal duplicates, and preserves the count of declared historical rows for which no reachable title map exists. It therefore supports a bounded collision audit without making a universal semantic novelty claim.

The expected Sable partition is forty-two completed, twelve represented, three open gaps, and three exact gates. These are planning expectations only. Completed can mean only a bounded structural or synthetic contract passed its declared acceptance gate. Represented means a structural proxy exists while real operators, systems, affected users, interoperability events, or authority remain absent. Open gap identifies missing real evidence. Exact gate identifies a decision repository software cannot make. Only completed, represented, open_gap, and exact_gate are allowed outcome labels.

The proposals cover catalog and resource identity, dataset-distribution separation, version lineage, fixity, source status, PROV role separation, revision DAGs, link relations, language and vocabulary provenance, antimeridian and axis-order handling, CRS WKT and coordinate epochs, units and transformation provenance, temporal roles, null and withheld states, OGC record routes, conformance declaration separation, patch confinement, operation ordering, merge semantics, conflicts, idempotency, rollback, stale harvesting, deterministic export, accessible alternatives, evaluation vacancies, workload and handover proxies, minimum disclosure, live status vacancies, GMUT and THOS firewalls, zero-row official adapters, longitudinal evidence gaps, accessibility evidence gaps, legal and rights gates, Māori place-name and data-governance authority, and sensitive-location publication authority.

## Expanded portfolio, skills, runners, and refinements

X1 freezes 120 safe-now packets, eighty bounded owner candidate prototypes, twenty successor candidate recommendations, twenty exact-approval holds, ten blocked packets, twenty owner skill ideas, ten owner runner ideas, ten successor skill ideas, ten successor runner ideas, one hundred owner CLEAN/FIX/REFINE tasks, and thirty successor recommendations. Floors remain subordinate to genuine utility and safety; caps are ceilings. No quota authorizes filler, destructive cleanup, package churn, user-material deletion, credentials, account changes, elevation, host-security weakening, Windows feature changes, Sandbox or Hyper-V activation, sibling mutation, real data, participants, production identity operations, legal or cultural decisions, Māori authority, or affected-party legitimacy.

The phase-local skill plan follows the installed skill-creator guidance: concise discriminating frontmatter, substantive bounded instructions, progressive disclosure only where useful, no placeholder readmes, no global installation, and quick validation plus real smoke use in x2. The ten family-current runners retain ghc_family names and caller compatibility. Historical and owner-specific tools remain read-only compatibility evidence. Python standard library and exact Git objects are sufficient for the planned hypotheses, so x1 plans no third-party installation or Codex update.

## Failure retention, privacy, and validation boundary

The activation baseline preserves Auren repository truth separately from two external route-parser failures. Thirteen additional Sable startup failures are frozen with zero credit, each paired with an additive recovery. They include output truncation, PowerShell parser and object-shape assumptions, lost process attribution, a duplicate read-only verifier, a pipe deadlock, the empty sparse index, and an oversized path projection. No recovery erases or converts the failed witness. Later failures must be appended before retry.

Public artifacts exclude raw task or thread identifiers, private routes, transcripts, screenshots, session streams, credentials, secrets, private callable identifiers, private app state, and private absolute local paths. Exact staged review operates on Git-index blobs. Five privacy classes distinguish scanner definitions from confirmed payload hits. Normalized-LF manifests preserve exact byte domains. A passing owner-scoped receipt remains same-owner evidence under shared infrastructure, not an external audit, independent reproduction, exhaustive security, complete privacy, or complete accessibility assurance.

## X1 gate and terminal hold

X1 must pass its bounded tests and exact staged review, become the direct child of Auren final, be pushed cleanly, and prove local, upstream, tracking, and fresh live remote equality before any x2 path or outcome exists. The phase commit ceiling is three total commits: one planning-only x1, one immutable x2 evidence commit, and one final closeout and seal commit. This ceiling never permits phase mixing, concealed failures, rewritten history, or an unreviewed omnibus commit.

Caelen Ash remains uncontacted. Only after Sable has a clean pushed fresh-live-equal exact final and one successful non-replayed owner-scoped canonical invocation may the live roster be refreshed, the unique existing exact-title Caelen Ash task be immediately reread, and at most one sanitized v676-v2 activation be sent if every duplicate, pause, redirect, status, usage, privacy, evidence, safety, and acknowledgement guard passes. The repository route state remains PREPARED_NOT_SENT. The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""


def build() -> list[str]:
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO, text=True, encoding="utf-8"
    ).strip()
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).strip()
    if head != SOURCE:
        raise RuntimeError(f"x1 builder requires source {SOURCE}, found {head}")
    if branch != TARGET_BRANCH:
        raise RuntimeError(f"x1 builder requires branch {TARGET_BRANCH}, found {branch}")
    if (PHASE_ROOT / "x2").exists() or (PHASE_ROOT / "final").exists():
        raise RuntimeError("x2 or final material exists before planning-only x1 freeze")

    inherited = inherited_rows()
    proposals = new_rows()
    audit = semantic_audit(proposals)
    safe = safe_rows(proposals)
    owner_candidates = candidate_rows(proposals, 80, "SR6761-C", False)
    successor_candidates = candidate_rows(proposals, 20, "SR6761-SC", True)
    owner_cleanup = cleanup_rows(100, "SR6761-R", True)
    successor_cleanup = cleanup_rows(30, "SR6761-SR", False)

    activation_baseline = {
        "effective_negatives": 41473,
        "methods": 30606,
        "failed_witnesses": 13134,
        "bounded_passing_witnesses": 17701,
        "open_gaps": 346,
        "exact_gates": 338,
    }
    after_startup = {
        **activation_baseline,
        "effective_negatives": activation_baseline["effective_negatives"]
        + len(STARTUP_FAILURES),
        "methods": activation_baseline["methods"] + (2 * len(STARTUP_FAILURES)),
        "failed_witnesses": activation_baseline["failed_witnesses"]
        + len(STARTUP_FAILURES),
        "bounded_passing_witnesses": activation_baseline[
            "bounded_passing_witnesses"
        ]
        + len(STARTUP_FAILURES),
    }

    payloads: dict[Path, Any] = {
        X1_ROOT / "activation-intake.json": {
            "schema": "ghc.family.activation-intake.v676.v1",
            "owner": OWNER,
            "phase": PHASE,
            "received_once": True,
            "solo": True,
            "source_branch": SOURCE_BRANCH,
            "source_root": SOURCE_ROOT,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_final": SOURCE,
            "source_packet": SOURCE_PACKET,
            "source_packet_words": 66877,
            "source_packet_sha256_normalized_lf": SOURCE_PACKET_SHA256,
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "source_manifest_entries_replayed": 548,
            "source_manifest_mismatches": 0,
            "source_canonical_replayed": False,
            "recorded_at_utc": RECORDED_UTC,
            "recorded_at_nz": RECORDED_NZ,
            "x1_state": "planning_only",
            "x2_implementation_present": False,
        },
        X1_ROOT / "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v676.v1",
            "owner": OWNER,
            "relational_role": "evidence-boundary cartographer and accessible-provenance steward",
            "hope": "make correction paths inspectable, access vacancies explicit, and every retained failure recoverable",
            "pronouns": "optional they/them relational language",
            "identity_evidence": False,
            "authority_evidence": False,
            "continuity_evidence": False,
            "corrigible": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "protected_gates": PROTECTED_GATES,
        },
        X1_ROOT / "source-verification.json": {
            "schema": "ghc.family.source-verification.v676.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": SOURCE_BRANCH,
            "source_root": SOURCE_ROOT,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_final": SOURCE,
            "direct_single_parent_chain": True,
            "source_to_final_commits": 3,
            "source_to_final_merges": 0,
            "source_clean": True,
            "source_ahead": 0,
            "source_behind": 0,
            "source_four_way_equal_fresh_live": True,
            "manifest_families_replayed": 6,
            "manifest_entries_replayed": 548,
            "manifest_mismatches": [],
            "external_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "canonical_state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "canonical_invocations": 1,
            "canonical_successes": 1,
            "canonical_replayed": False,
            "inherited_validation_credit": 0,
        },
        X1_ROOT / "official-primary-source-ledger.json": source_ledger(),
        X1_ROOT / "inherited-revalidation-freeze.json": {
            "schema": "ghc.family.inherited-revalidation-freeze.v676.v1",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": len(inherited),
            "novelty_credit": 0,
            "completion_credit": 0,
            "rows": inherited,
        },
        X1_ROOT / "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v676.v1",
            "owner": OWNER,
            "phase": PHASE,
            "declared_chain_before": SOURCE_PROPOSAL_CHAIN,
            "declared_chain_after_if_evidence_sealed": PLANNED_PROPOSAL_CHAIN,
            "proposal_count": len(proposals),
            "allowed_outcomes": CORE_OUTCOMES,
            "expected_outcomes": {
                label: sum(
                    1
                    for row in proposals
                    if row["expected_execution_disposition"] == label
                )
                for label in CORE_OUTCOMES
            },
            "outcomes_observed": False,
            "universal_novelty_claim": False,
            "rows": proposals,
        },
        X1_ROOT / "proposal-chain-audit.json": audit,
        X1_ROOT / "portfolio-freeze.json": {
            "schema": "ghc.family.portfolio-freeze.v676.v1",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "represented_pillars": [
                "GMUT Mind",
                "THOS Body",
                "Freed ID and CBR Heart",
            ],
            "owner_practice_lenses": [
                "wholly_synthetic_geospatial_metadata_catalog_correction_registrar",
                "wholly_synthetic_coordinate_reference_metadata_steward",
                "wholly_synthetic_public_geodata_archive_handover_reviewer",
            ],
            "successor_practice_recommendation": "wholly_synthetic_astronomical_observation_metadata_embargo_release_register_reviewer",
            "safe_now": safe,
            "owner_candidates": owner_candidates,
            "successor_candidates": successor_candidates,
            "exact_approval": exact_rows(),
            "blocked": blocked_rows(),
            "owner_skill_ideas": OWNER_SKILLS,
            "owner_runner_ideas": OWNER_RUNNERS,
            "successor_skill_ideas": SUCCESSOR_SKILLS,
            "successor_runner_ideas": SUCCESSOR_RUNNERS,
            "owner_clean_fix_refine": owner_cleanup,
            "successor_clean_fix_refine": successor_cleanup,
            "caps_are_ceilings": True,
            "materialized_file_stop": 2000,
            "document_word_cap": 100000,
            "commit_cap": {"x1": 1, "x2": 2, "total": 3},
        },
        X1_ROOT / "skill-runner-plan.json": {
            "schema": "ghc.family.skill-runner-plan.v676.v1",
            "owner": OWNER,
            "phase": PHASE,
            "skill_creator_read": True,
            "repository_local_only": True,
            "global_installation": False,
            "owner_skills": OWNER_SKILLS,
            "owner_runners": OWNER_RUNNERS,
            "successor_skill_ideas": SUCCESSOR_SKILLS,
            "successor_runner_ideas": SUCCESSOR_RUNNERS,
            "quick_validate_required": True,
            "smoke_use_required": True,
            "independent_subagent_forward_test": "not_authorized_work_solo",
            "caller_compatibility": "preserve ghc_family_* and build_ghc_family_*",
        },
        X1_ROOT / "clean-fix-refine-plan.json": {
            "schema": "ghc.family.clean-fix-refine-plan.v676.v1",
            "owner": OWNER,
            "phase": PHASE,
            "owner_count": len(owner_cleanup),
            "owner_tasks": owner_cleanup,
            "successor_count": len(successor_cleanup),
            "successor_recommendations": successor_cleanup,
            "destructive_cleanup_authorized": False,
        },
        X1_ROOT / "approval-hold-register.json": {
            "schema": "ghc.family.approval-hold-register.v676.v1",
            "owner": OWNER,
            "phase": PHASE,
            "exact_approval": exact_rows(),
            "blocked": blocked_rows(),
            "execution_credit": 0,
        },
        X1_ROOT / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow-startup.v676.v1",
            "owner": OWNER,
            "phase": PHASE,
            "execution_authority": "owner_self_scoped_delta",
            "activation_baseline": activation_baseline,
            "startup_failure_count": len(STARTUP_FAILURES),
            "failures": [
                {
                    "failure_id": failure_id,
                    "failed_witness": failed,
                    "recovery": recovery,
                    "state": "failed_retained_zero_credit",
                    "success_credit": 0,
                    "same_owner_only": True,
                    "independent_reproduction": False,
                }
                for failure_id, failed, recovery in STARTUP_FAILURES
            ],
            "bounded_recoveries": [
                {
                    "witness_id": failure_id.replace("-N", "-R"),
                    "failure_id": failure_id,
                    "procedure": recovery,
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "bounded workflow recovery only",
                }
                for failure_id, _failed, recovery in STARTUP_FAILURES
            ],
            "effective_after_startup": after_startup,
            "recovery_rule": "Every recovery is additive and never erases or relabels the failed witness.",
        },
        X1_ROOT / "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v676.v1",
            "owner": OWNER,
            "phase": PHASE,
            "strict_planning_only_x1_before_x2": True,
            "steps": [
                {
                    "order": 1,
                    "name": "read activation candidate skills schemas and current overlays",
                    "state": "completed",
                },
                {
                    "order": 2,
                    "name": "verify immutable source manifests receipt and live equality",
                    "state": "completed",
                },
                {
                    "order": 3,
                    "name": "create clean sparse Sable lane",
                    "state": "completed",
                },
                {
                    "order": 4,
                    "name": "freeze test push and prove planning-only x1",
                    "state": "in_progress",
                },
                {
                    "order": 5,
                    "name": "build bounded x2 evidence and retain every failure",
                    "state": "pending",
                },
                {
                    "order": 6,
                    "name": "seal final push and run one exclusive canonical",
                    "state": "pending",
                },
                {
                    "order": 7,
                    "name": "refresh live route and send at most once if all gates pass",
                    "state": "pending",
                },
            ],
            "validation": {
                "owner_scoped_delta_only": True,
                "unchanged_history_scan": False,
                "cross_lane_scan": False,
                "sibling_lane_mutation": False,
                "one_successful_canonical": True,
                "post_success_replay": False,
            },
            "stop_conditions": [
                "source mismatch",
                "dirty source",
                "x1 x2 mixing",
                "privacy hit",
                "manifest mismatch",
                "file ceiling reached",
                "protected authority gate",
                "usage exhaustion",
                "route ambiguity",
                "user pause redirect rename narrow or stop",
            ],
        },
        X1_ROOT / "threat-model.json": {
            "schema": "ghc.family.threat-model.v676.v1.x1",
            "owner": OWNER,
            "phase": PHASE,
            "threats": [
                "real identifier or sensitive location leakage",
                "private route leakage",
                "x1 and x2 mixing",
                "outcome promotion",
                "authority fabrication",
                "network side effect",
                "manifest drift",
                "failed-witness erasure",
                "successful canonical replay",
                "sibling-lane mutation",
                "coordinate axis confusion",
                "stale-source promotion",
            ],
            "controls": [
                "synthetic fixtures only",
                "five-class privacy scan",
                "planning-only x1",
                "four exact labels",
                "authority vacancy",
                "no-network runners",
                "normalized-LF Git-blob manifests",
                "append-only Method Flow",
                "one-shot external receipt latch",
                "owner-local sparse lane",
                "axis and unit type guards",
                "source-status ledger",
            ],
            "residual_risk": "Structural controls are bounded software evidence, not exhaustive security, complete privacy, complete accessibility, professional review, or independent reproduction.",
        },
        X1_ROOT / "wellbeing-and-corrigibility.json": {
            "schema": "ghc.family.wellbeing-corrigibility.v676.v1.x1",
            "owner": OWNER,
            "workload_bounded": True,
            "pause_available": True,
            "corrigible": True,
            "identity_relational_only": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "no_completion_pressure_can_override_evidence_or_authority": True,
        },
        X1_ROOT / "route-plan.json": {
            "schema": "ghc.family.route-plan.v676.v1.x1",
            "previous_owner": "Auren Lark",
            "previous_phase": "v675-v8",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "next_owner": "Caelen Ash",
            "next_phase": "v676-v2",
            "state": "HOLD_BEFORE_SABLE_TERMINAL_GATE",
            "precontact": False,
            "send_attempts": 0,
            "task_created": False,
            "duplicate_guard_required": True,
            "terminal_planning_label": "v725-v8",
        },
        X1_ROOT / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v676.v1.x1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_state": "PLANNING_ONLY_NOT_YET_COMMITTED",
            "proposal_chain_before": SOURCE_PROPOSAL_CHAIN,
            "proposal_chain_after_if_evidence_sealed": PLANNED_PROPOSAL_CHAIN,
            "expected_outcomes": {
                "completed": 42,
                "represented": 12,
                "open_gap": 3,
                "exact_gate": 3,
            },
            "outcomes_observed": False,
            "real_rows": 0,
            "real_people": 0,
            "real_keys_or_proofs": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    }

    written: list[Path] = []
    for path, payload in payloads.items():
        write_json(path, payload)
        written.append(path)
    overview_path = X1_ROOT / "integrated-overview.md"
    write_text(overview_path, overview())
    written.append(overview_path)
    return [path.relative_to(REPO).as_posix() for path in sorted(written)]


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I
        ),
        "raw_task_thread_identifier": re.compile(
            rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}",
            re.I,
        ),
        "credential_assignment": re.compile(
            rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}",
            re.I,
        ),
        "private_conversation_payload": re.compile(
            rb"(?:session_stream|private_transcript|screenshot_payload)", re.I
        ),
    }


def build_staged_review() -> dict[str, Any]:
    review_rel = "docs/sable-rook/v676-v1/validation/x1-staged-review.json"
    privacy_rel = "docs/sable-rook/v676-v1/validation/x1-privacy-scan.json"
    manifest_rel = "docs/sable-rook/v676-v1/validation/x1-index-manifest.json"
    exclusions = [review_rel, privacy_rel, manifest_rel]
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).splitlines()
    allowed_exact = {
        "scripts/build_ghc_family_sable_rook_v676_v1_x1.py",
        "tests/test_ghc_family_sable_rook_v676_v1_x1.py",
    }
    out_of_scope = [
        path
        for path in staged
        if not path.startswith("docs/sable-rook/v676-v1/x1/")
        and path not in allowed_exact
        and path not in exclusions
    ]
    if out_of_scope:
        raise RuntimeError(f"out-of-scope x1 paths: {out_of_scope}")
    if any(path.startswith("docs/sable-rook/v676-v1/x2/") for path in staged):
        raise RuntimeError("x2 path present in x1 staged surface")

    patterns = privacy_patterns()
    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, str]] = []
    confirmed_hits: list[dict[str, str]] = []
    json_parses = 0
    for path in staged:
        if path in exclusions:
            continue
        data = subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)
        scanner_definition_start = data.find(b"def privacy_patterns()")
        scanner_definition_end = data.find(
            b"def build_staged_review()", scanner_definition_start
        )
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_parses += 1
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                start = data.rfind(b"\n", 0, match.start()) + 1
                end = data.find(b"\n", match.end())
                if end < 0:
                    end = len(data)
                line = data[start:end]
                exact_scanner_definition = (
                    path == "scripts/build_ghc_family_sable_rook_v676_v1_x1.py"
                    and scanner_definition_start >= 0
                    and scanner_definition_end > scanner_definition_start
                    and scanner_definition_start <= match.start() < scanner_definition_end
                )
                if path.endswith(".py") and (
                    exact_scanner_definition
                    or b"re.compile" in line
                    or b"privacy_patterns" in line
                    or b"raw_task_thread_identifier" in line
                ):
                    candidates.append(
                        {
                            "path": path,
                            "class": class_name,
                            "disposition": "scanner_definition_only",
                        }
                    )
                else:
                    confirmed_hits.append({"path": path, "class": class_name})
        normalized = normalize_lf(data)
        entries.append(
            {
                "path": path,
                "bytes": len(normalized),
                "sha256": hashlib.sha256(normalized).hexdigest(),
                "hash_domain": "git_index_blob_normalized_lf",
            }
        )
    if confirmed_hits:
        raise RuntimeError(f"confirmed privacy hits: {confirmed_hits}")
    diff_check = subprocess.run(
        ["git", "diff", "--cached", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if diff_check.returncode:
        raise RuntimeError(diff_check.stdout + diff_check.stderr)

    privacy = {
        "schema": "ghc.family.privacy-scan.v676.v1.x1",
        "owner": OWNER,
        "phase": PHASE,
        "classes": list(patterns),
        "scanned_entry_count": len(entries),
        "scanner_candidates": candidates,
        "scanner_candidate_count": len(candidates),
        "confirmed_hits": confirmed_hits,
        "confirmed_hit_count": 0,
        "boundary": "five-class Git-index scan is bounded owner evidence, not complete privacy assurance",
    }
    review = {
        "schema": "ghc.family.exact-staged-review.v676.v1.x1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "state": "VALID_EXACT_X1_STAGED_REVIEW",
        "reviewed_entry_count": len(entries),
        "reviewed_paths": [row["path"] for row in entries],
        "declared_exclusions": exclusions,
        "json_parses": json_parses,
        "privacy_classes": list(patterns),
        "confirmed_privacy_hits": 0,
        "out_of_scope_paths": [],
        "x2_paths_present": False,
        "diff_hygiene": True,
    }
    manifest = {
        "schema": "ghc.family.normalized-lf-index-manifest.v676.v1.x1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "entry_count": len(entries),
        "entries": entries,
        "declared_self_exclusions": exclusions,
    }
    write_json(REPO / privacy_rel, privacy)
    write_json(REPO / review_rel, review)
    write_json(REPO / manifest_rel, manifest)
    return {
        "state": review["state"],
        "reviewed_entry_count": len(entries),
        "json_parses": json_parses,
        "scanner_candidate_count": len(candidates),
        "confirmed_privacy_hits": 0,
        "written_receipts": exclusions,
    }


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--staged-review":
        print(json.dumps(build_staged_review(), indent=2, sort_keys=True))
    elif len(sys.argv) == 1:
        print(json.dumps({"written": build()}, indent=2, sort_keys=True))
    else:
        raise SystemExit("usage: build_ghc_family_sable_rook_v676_v1_x1.py [--staged-review]")
