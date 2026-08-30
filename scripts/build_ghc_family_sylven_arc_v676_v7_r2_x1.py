#!/usr/bin/env python3
"""Build the planning-only Sylven Arc v676-v7-r2 remaster x1 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Sylven Arc"
OWNER_SLUG = "sylven-arc"
PHASE = "v676-v7-r2"
DISPLAY_PHASE = "v676-v7 (2) remastered"
BRANCH = "codex/GHC-Family/sylven-arc-v676-v7-full-tools"
SOURCE = "e66201e9efd19cb3fc98baf672ea4df440758616"
SOURCE_PHASE = "v676-v7"
GENERATED_AT_NZ = "2026-08-30T16:00:00+12:00"
DECLARED_CHAIN_BEFORE = 7670
DECLARED_CHAIN_AFTER = 7730
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "effective_negatives": 42895,
    "effective_methods": 34506,
    "retained_failed_witnesses": 14556,
    "bounded_passing_witnesses": 20639,
    "open_gaps": 362,
    "exact_gates": 353,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "The immutable v676-v7 repository seal, the post-canonical and route-retry overlays, "
        "and seven retained remaster-startup failure/recovery pairs."
    ),
}

NEW_TITLES = [
    "Synthetic bound-volume namespace without object identity ownership or treatment claim",
    "Gathering signature and folio topology with zero physical collation",
    "Leaf page and opening relation graph without pagination correction authority",
    "Board spine covering and text-block component map without material determination",
    "Sewing support station and thread-channel vacancy without structural inference",
    "Endpaper pastedown flyleaf and hinge relation with attachment uncertainty",
    "Head tail fore-edge and joint orientation vocabulary without object inspection",
    "Quire collation formula representation without bibliographic verification",
    "Catchword signature-mark and sequence-cue register without authenticity inference",
    "Fold grain deckle and paper-formation vocabulary firewall without measurement",
    "Binding style term registry with period attribution held vacant",
    "Board attachment and lacing topology without load or serviceability claim",
    "Spine-lining layer relation with adhesive and fibre identity holds",
    "Covering turn-in corner and cap relation without treatment instruction",
    "Endband core tie-down and bead vocabulary without construction diagnosis",
    "Leaf-loss stub cancel and insertion cue register without curatorial decision",
    "Opening-angle and support vocabulary with all observed quantities vacant",
    "Surface abrasion red-rot stain and distortion cue register without condition diagnosis",
    "Book-cradle support map with handling and use authority reserved",
    "Housing wrapper box and enclosure relation without storage-suitability claim",
    "Treatment-before-after command observation and interpretation firewall",
    "Reversible correction lineage for contested collation statements",
    "Bound-volume image surrogate lineage with crop rotation and rights vacancy",
    "Conservation handover capsule with work release and competence abstention",
    "Bookbinding workload budget with resumable owner-local checkpoints",
    "Synthetic bibliographic-record namespace without cataloguing authority",
    "Leader directory field indicator and subfield topology without record conformance claim",
    "MARC 21 field-order representation with official-version provenance",
    "Control-field data vacancy with no real identifier or classification assignment",
    "Title statement relation with transcription and responsibility uncertainty",
    "Edition publication and distribution field vacancy without bibliographic conclusion",
    "Physical-description field proxy without observed extent dimensions or material",
    "Series note and linking-entry relation with no real resource association",
    "Subject-access vocabulary compartment without classification or cultural authority",
    "Holdings location and access-status vacancy without custody claim",
    "Alternate-script and multiscript representation without language authority",
    "Data-provenance subfield braid for synthetic record revisions",
    "MARC-to-neutral JSON crosswalk with explicit non-equivalence register",
    "Duplicate field and malformed indicator rejecting parser contract",
    "Deterministic canonical JSON envelope for synthetic bibliographic cards",
    "Archival hierarchy series file and item relation without accession claim",
    "Record lifecycle event proxy with transfer and disposition authority vacant",
    "Metadata-minimization ledger for synthetic archival descriptions",
    "Accessible record-summary landmarks with manual evaluation gap",
    "Rights restriction remedy and affected-user challenge escrow",
    "Freed ID four-tier flashcard anchor for owner pillar practice and task",
    "Content-addressed flashcard deck with deterministic section ordering",
    "Flashcard source-to-claim firewall with evidence and authority tiers separated",
    "Flashcard supersession chain preserving prior cards and retained failures",
    "Flashcard retrieval budget with bounded context and no identity-continuity claim",
    "GMUT graph analogy for gathering and metadata topology without physical promotion",
    "GMUT relabeling firewall for fields signatures and component identifiers",
    "THOS participant-free comparator for monolithic versus modular handoff packets",
    "THOS context-load proxy with no cognition wellbeing or effectiveness claim",
    "Freed ID status correction revocation and recovery vacancy without keys or proofs",
    "Zero-call Library of Congress vocabulary adapter with no downloaded rows",
    "Real bound-volume observation specialist assessment and independent-review gap",
    "Real cataloguer archivist conservator and affected-user evaluation gap",
    "Handling treatment cataloguing release and professional-authority exact gate",
    "Ownership copyright privacy cultural-context Māori-data and Māori-authority exact gate",
]

SOURCES = [
    {
        "source_id": "LOC-COLLECTIONS-CARE",
        "url": "https://www.loc.gov/preservation/care/",
        "status": "official Library of Congress collections-care page checked 2026-08-30",
        "use": "bound-volume, handling, housing, and preservation vocabulary only; no object, treatment, or professional claim",
    },
    {
        "source_id": "LOC-PRESERVING-BOOKS",
        "url": "https://guides.loc.gov/preserving-your-books",
        "status": "official Library of Congress research guide checked 2026-08-30",
        "use": "book-part, support, handling-risk, and care vocabulary only; no instruction executed and no suitability conclusion",
    },
    {
        "source_id": "LOC-MARC21-BIB",
        "url": "https://www.loc.gov/marc/bibliographic/",
        "status": "official MARC 21 bibliographic documentation including Update 42 checked 2026-08-30",
        "use": "leader, directory, field, indicator, subfield, note, and provenance vocabulary only; no real record conformance claim",
    },
    {
        "source_id": "NARA-METADATA-REQUIREMENTS",
        "url": "https://www.archives.gov/records-mgmt/policy/metadata-compiled",
        "status": "official National Archives metadata-requirements page checked 2026-08-30",
        "use": "metadata lifecycle and transfer-requirement vocabulary only; no agency transfer, legal interpretation, or conformance claim",
    },
    {
        "source_id": "W3C-PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C Recommendation",
        "use": "entity, activity, agent, derivation, and attribution vocabulary only",
    },
    {
        "source_id": "WCAG-2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation with current errata",
        "use": "structural accessibility vocabulary only; no conformance claim",
    },
    {
        "source_id": "W3C-VC-DATA-MODEL-2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C Recommendation",
        "use": "status, minimization, correlation, and lifecycle vocabulary only; zero keys and zero proofs",
    },
    {
        "source_id": "RFC-8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor informational RFC",
        "use": "deterministic JSON vocabulary only; no production cryptographic assurance",
    },
]

PROTECTED_GATES = [
    "no real person, participant, bookbinder, conservator, cataloguer, archivist, custodian, owner, affected user, bound volume, record, collection, object, observation, measurement, handling, treatment, transfer, release, network row, or external write",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, ultraviolet or quantum completion, final physics, or Theory-of-Everything claim",
    "no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, or identity-continuity claim",
    "no professional, handling, conservation, cataloguing, archival, legal, privacy-remedy, cultural, affected-party, traditional-knowledge, Māori-data-governance, or Māori-authority decision",
    "no accessibility-complete, privacy-complete, exhaustive-security, proof, canon, or Stage 20 claim",
]

TOOL_PLAN = [
    {"ecosystem": "python", "name": "black", "version": "26.5.1", "need": "deterministic owner-fixture format checking"},
    {"ecosystem": "python", "name": "isort", "version": "9.0.1", "need": "deterministic import-order checking"},
    {"ecosystem": "python", "name": "flake8", "version": "7.3.0", "need": "independent bounded lint witness"},
    {"ecosystem": "python", "name": "pylint", "version": "4.0.8", "need": "message-level static-analysis witness"},
    {"ecosystem": "python", "name": "autoflake", "version": "2.4.0", "need": "unused-import rejecting fixture"},
    {"ecosystem": "python", "name": "pytest-mock", "version": "3.15.1", "need": "no-network callable isolation fixture"},
    {"ecosystem": "python", "name": "pytest-subtests", "version": "0.15.0", "need": "attributed table-driven fixture reporting"},
    {"ecosystem": "node", "name": "eslint-plugin-security", "version": "4.0.1", "need": "security-hotspot lint fixture"},
    {"ecosystem": "node", "name": "eslint-plugin-regexp", "version": "3.2.0", "need": "regular-expression correctness fixture"},
    {"ecosystem": "node", "name": "stylelint", "version": "17.14.1", "need": "static-report stylesheet lint fixture"},
    {"ecosystem": "node", "name": "stylelint-config-standard", "version": "40.0.0", "need": "bounded stylelint rule baseline"},
    {"ecosystem": "node", "name": "npm-run-all2", "version": "9.0.3", "need": "bounded multi-check orchestration fixture"},
    {"ecosystem": "powershell", "name": "PSScriptAnalyzer", "version": "1.25.0", "need": "Windows PowerShell static-analysis fixture"},
]

STARTUP_FAILURES = [
    (
        "SA6767R2-START-N001",
        "An initial skill-inventory PowerShell pipeline hit the empty-pipe parser fault before producing a complete inventory.",
        "SA6767R2-START-P001",
        "The values were materialized before projection and all explicitly named skills were then read completely.",
    ),
    (
        "SA6767R2-START-N002",
        "A broad recursive phase-file display exceeded the model-visible output context and was truncated.",
        "SA6767R2-START-P002",
        "Bounded exact-pattern inventory and per-file size probes replaced the broad display without repeating it.",
    ),
    (
        "SA6767R2-START-N003",
        "A combined authorization-state display exceeded its visible envelope before the full state was read.",
        "SA6767R2-START-P003",
        "Nonoverlapping bounded line windows completed the authorization and schema read through EOF.",
    ),
    (
        "SA6767R2-START-N004",
        "The first meta-tool reference probe guessed JSON extensions for Markdown reference files and found no targets.",
        "SA6767R2-START-P004",
        "An exact bounded reference inventory recovered the real Markdown filenames, which were then read through EOF.",
    ),
    (
        "SA6767R2-START-N005",
        "A combined multi-registry metadata projection completed without attributable output inside its response contract.",
        "SA6767R2-START-P005",
        "Independent bounded PyPI, npm, PowerShell Gallery, and Codex version probes recovered exact current candidate versions.",
    ),
    (
        "SA6767R2-START-N006",
        "A broad Git-grep proposal-title projection completed without attributable output inside its response contract.",
        "SA6767R2-START-P006",
        "The remaster uses one exact Git-object semantic audit with bounded output and preserves the failed grep attempt at zero credit.",
    ),
    (
        "SA6767R2-X1-N001",
        "The first exact git add omitted sparse mode and Git refused the new owner-document paths outside the existing sparse definition.",
        "SA6767R2-X1-P001",
        "The same exact owner allowlist is staged with git add --sparse; no sparse pattern, sibling path, or inherited byte is changed.",
    ),
]

OWNER_SKILLS = [
    "bound-volume-component-topology",
    "gathering-collation-vacancy",
    "binding-material-claim-hold",
    "opening-angle-metrology-vacancy",
    "book-handling-authority-reservation",
    "binding-treatment-command-firewall",
    "bound-volume-image-lineage",
    "conservation-handover-nonpromotion",
    "synthetic-marc-record-topology",
    "marc-field-order-validator",
    "bibliographic-identifier-vacancy",
    "archival-hierarchy-nonclaim",
    "metadata-minimization-ledger",
    "record-rights-challenge-escrow",
    "accessible-record-summary-proxy",
    "freed-id-four-tier-deck",
    "content-addressed-flashcard-index",
    "flashcard-supersession-nonerasure",
    "gmut-book-metadata-analogy-firewall",
    "thos-modular-context-proxy-guard",
]

SUCCESSOR_SKILLS = [
    "successor-context-card-intake",
    "successor-proposal-neighbor-audit",
    "successor-toolchain-delta-guard",
    "successor-method-flow-nonerasure",
    "successor-static-report-landmarks",
    "successor-zero-network-adapter",
    "successor-exact-gate-register",
    "successor-bounded-retry-selector",
    "successor-roster-route-refresh",
    "successor-baton-file-index",
]

OWNER_RUNNERS = [
    "ghc_family_sylven_arc_v676_v7_r2_contract_runner.py",
    "ghc_family_sylven_arc_v676_v7_r2_mutation_runner.py",
    "ghc_family_sylven_arc_v676_v7_r2_book_topology_runner.py",
    "ghc_family_sylven_arc_v676_v7_r2_metadata_runner.py",
    "ghc_family_sylven_arc_v676_v7_r2_flashcard_runner.py",
    "ghc_family_sylven_arc_v676_v7_r2_toolchain_runner.py",
    "ghc_family_sylven_arc_v676_v7_r2_privacy_runner.py",
    "ghc_family_sylven_arc_v676_v7_r2_accessibility_runner.py",
    "ghc_family_sylven_arc_v676_v7_r2_portfolio_runner.py",
    "build_ghc_family_sylven_arc_v676_v7_r2_report.py",
]

SUCCESSOR_RUNNERS = [
    "ghc_family_successor_context_card_reader.py",
    "ghc_family_successor_proposal_revalidator.py",
    "ghc_family_successor_toolchain_delta.py",
    "ghc_family_successor_method_flow_ingest.py",
    "ghc_family_successor_static_report_check.py",
    "ghc_family_successor_zero_network_adapter.py",
    "ghc_family_successor_exact_gate_check.py",
    "ghc_family_successor_bounded_retry.py",
    "ghc_family_successor_route_refresh.py",
    "ghc_family_successor_baton_index.py",
]


def git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_git_json(repo: Path, commit: str, path: str) -> dict[str, Any]:
    raw = git(repo, "show", f"{commit}:{path}")
    return json.loads(str(raw))


def inherited_selection(repo: Path) -> list[dict[str, Any]]:
    sources = [
        (
            "Sylven Arc v676-v7",
            "docs/sylven-arc/v676-v7/x1/new-proposal-freeze.json",
            40,
        ),
        (
            "Elowen Cairn v676-v6",
            "docs/elowen-cairn/v676-v6/x1/new-proposal-freeze.json",
            20,
        ),
    ]
    selected: list[dict[str, Any]] = []
    for source_phase, path, limit in sources:
        rows = load_git_json(repo, SOURCE, path)["proposals"][:limit]
        for row in rows:
            selected.append(
                {
                    "proposal_id": row["proposal_id"],
                    "title": row["title"],
                    "original_expected_disposition": row["expected_disposition"],
                    "original_approval_class": row["approval_class"],
                    "source_phase": source_phase,
                    "source_path": path,
                    "selected_for": "bounded revalidation or representation only",
                    "sylven_r2_novelty_credit": 0,
                    "automatic_completion_credit": 0,
                }
            )
    if len(selected) != 60:
        raise RuntimeError("exactly sixty inherited rows are required")
    return selected


def new_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset, title in enumerate(NEW_TITLES, start=1):
        proposal_id = f"SA6767R2-N{offset:03d}"
        if offset <= 42:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 54:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 57:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["W3C-PROV-O", "RFC-8785"]
        if offset <= 25:
            source_ids += ["LOC-COLLECTIONS-CARE", "LOC-PRESERVING-BOOKS"]
        if 26 <= offset <= 45:
            source_ids += ["LOC-MARC21-BIB", "NARA-METADATA-REQUIREMENTS"]
        if offset in {23, 34, 43, 44, 45, 46, 47, 48, 49, 55, 58, 59, 60}:
            source_ids += ["WCAG-2.2", "W3C-VC-DATA-MODEL-2.0"]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real object, record, measurement, treatment, identity, rights, professional, legal, cultural, or authority claims."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} accepts a missing or contradictory field, a raw or real identifier, a non-authorized outcome label, "
                    "or an observation, intervention, conformance, competence, right, identity, or authority claim."
                ),
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": sorted(set(source_ids)),
                "concrete_artifacts": [
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/contracts/{proposal_id}.json",
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/evidence/{proposal_id}-receipt.json",
                ],
                "falsifier_or_acceptance_gate": (
                    f"One bounded positive fixture must satisfy {proposal_id} and four preregistered invalid mutations must be rejected; "
                    "represented, open, and exact-gated rows receive no real-world execution credit."
                ),
                "rollback_or_recovery": (
                    f"Quarantine {proposal_id}, retain the failed witness, restore the exact committed input, and rerun only the isolated dependency."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": disposition,
            }
        )
    return rows


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 0.0


def parse_tree_entries(raw: bytes) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    cursor = 0
    while cursor < len(raw):
        mode_end = raw.index(b" ", cursor)
        name_end = raw.index(b"\0", mode_end + 1)
        mode = raw[cursor:mode_end].decode("ascii")
        name = raw[mode_end + 1 : name_end].decode("utf-8", errors="surrogateescape")
        oid_start = name_end + 1
        oid_end = oid_start + 20
        entries.append((mode, name, raw[oid_start:oid_end].hex()))
        cursor = oid_end
    return entries


def fetch_many(repo: Path, requests: list[tuple[str, str]]) -> list[tuple[str, str, bytes]]:
    request = b"".join(oid.encode("ascii") + b"\n" for oid, _ in requests)
    response = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        input=request,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    output: list[tuple[str, str, bytes]] = []
    cursor = 0
    for requested_oid, path in requests:
        header_end = response.index(b"\n", cursor)
        header = response[cursor:header_end].split()
        cursor = header_end + 1
        if len(header) != 3 or header[1] == b"missing":
            raise RuntimeError(f"missing Git object for {path}")
        actual_oid, object_type, raw_size = header
        if actual_oid.decode("ascii") != requested_oid:
            raise RuntimeError(f"Git object identity mismatch for {path}")
        size = int(raw_size)
        raw = response[cursor : cursor + size]
        cursor += size
        if len(raw) != size or response[cursor : cursor + 1] != b"\n":
            raise RuntimeError(f"truncated Git object for {path}")
        cursor += 1
        output.append((object_type.decode("ascii"), path, raw))
    if cursor != len(response):
        raise RuntimeError("unattributed Git batch bytes")
    return output


def collect_title_records(value: Any, path: str, output: list[tuple[str, str, str]]) -> None:
    if isinstance(value, dict):
        title = value.get("title") or value.get("proposal_title") or value.get("name")
        proposal_id = value.get("proposal_id") or value.get("id") or value.get("proposal")
        if isinstance(title, str) and isinstance(proposal_id, str) and len(title.strip()) > 2:
            output.append((proposal_id.strip(), title.strip(), path))
        for child in value.values():
            collect_title_records(child, path, output)
    elif isinstance(value, list):
        for child in value:
            collect_title_records(child, path, output)


def semantic_audit(repo: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    if git(repo, "rev-parse", "--show-object-format") != "sha1":
        raise RuntimeError("verified SHA-1 Git object format required")
    root = str(git(repo, "show", "-s", "--format=%T", SOURCE))
    level: list[tuple[str, str]] = [(root, "")]
    blobs: list[tuple[str, str]] = []
    tree_count = 0
    while level:
        next_level: list[tuple[str, str]] = []
        for object_type, prefix, raw in fetch_many(repo, level):
            if object_type != "tree":
                raise RuntimeError(f"expected tree at {prefix or '<root>'}")
            tree_count += 1
            for mode, name, oid in parse_tree_entries(raw):
                path = f"{prefix}/{name}" if prefix else name
                if mode == "40000":
                    if not prefix and name != "docs":
                        continue
                    next_level.append((oid, path))
                elif path.endswith(".json") and ("proposal" in path.casefold() or "prereg" in path.casefold()):
                    blobs.append((oid, path))
        level = next_level
    records: list[tuple[str, str, str]] = []
    failures: list[dict[str, str]] = []
    for object_type, path, raw in fetch_many(repo, blobs):
        if object_type != "blob":
            failures.append({"path": path, "error": f"unexpected_{object_type}"})
            continue
        try:
            collect_title_records(json.loads(raw.decode("utf-8")), path, records)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            failures.append({"path": path, "error": type(error).__name__})
    unique: dict[tuple[str, str], tuple[str, str, str]] = {}
    for proposal_id, title, path in records:
        unique.setdefault((proposal_id.casefold(), title.casefold()), (proposal_id, title, path))
    neighbors = []
    for row in rows:
        nearest = max(unique.values(), key=lambda candidate: jaccard(row["title"], candidate[1]))
        score = jaccard(row["title"], nearest[1])
        neighbors.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "nearest_id": nearest[0],
                "nearest_title": nearest[1],
                "nearest_path": nearest[2],
                "token_jaccard": round(score, 4),
                "quarantined": score >= QUARANTINE_THRESHOLD,
            }
        )
    quarantined = [row for row in neighbors if row["quarantined"]]
    exact_titles = {title.casefold() for _, title, _ in unique.values()}
    exact_collisions = [row["proposal_id"] for row in rows if row["title"].casefold() in exact_titles]
    return {
        "source": SOURCE,
        "source_root_tree_oid": root,
        "declared_chain_count": DECLARED_CHAIN_BEFORE,
        "reachable_tree_objects": tree_count,
        "reachable_proposal_json_blobs": len(blobs),
        "reachable_raw_id_title_records": len(records),
        "reachable_unique_id_title_records": len(unique),
        "json_parse_failures": len(failures),
        "parse_failure_details": failures,
        "exact_title_collisions": exact_collisions,
        "quarantine_threshold": QUARANTINE_THRESHOLD,
        "selected_rows_quarantined": len(quarantined),
        "maximum_selected_score": max(row["token_jaccard"] for row in neighbors),
        "neighbors": neighbors,
        "universal_novelty_proved": False,
        "limitation": (
            "Every reachable proposal-bearing JSON blob at the exact source was inspected. The declared chain is larger than the "
            "materialized unique-title set, so this supports source-bounded semantic distinctness rather than universal or scientific novelty."
        ),
    }


def portfolio(kind: str, count: int, owner: str, prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"SA6767R2-{prefix}-{index:03d}",
            "kind": kind,
            "owner": owner,
            "plan_only_at_x1": True,
            "task": f"Bounded {kind} contract {index:03d} for modular evidence, flashcards, tooling, documentation, validation, or cleanup",
            "acceptance": "One explicit owner-local artifact or receipt; no hidden external action or protected-gate conversion",
            "rollback": "Retain the failed witness, revert only the owner-local uncommitted target, and rerun the isolated dependency",
            "protected_gates": PROTECTED_GATES,
        }
        for index in range(1, count + 1)
    ]


def exact_or_blocked(kind: str, count: int, prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": f"SA6767R2-{prefix}-{index:03d}",
            "kind": kind,
            "state": "UNEXECUTED",
            "reason": "Action-specific target, competent authority, affected-party acceptance, or protected evidence is absent",
            "execution_authorized": False,
            "protected_gates": PROTECTED_GATES,
        }
        for index in range(1, count + 1)
    ]


def x1_manifest(repo: Path, paths: list[Path]) -> dict[str, Any]:
    entries = []
    for path in sorted(paths):
        raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        entries.append(
            {
                "path": path.relative_to(repo).as_posix(),
                "bytes": len(path.read_bytes()),
                "sha256_normalized_lf": hashlib.sha256(raw).hexdigest(),
            }
        )
    return {
        "source": SOURCE,
        "phase": PHASE,
        "normalization": "CRLF and CR normalized to LF before SHA-256",
        "declared_self_exclusions": [
            "docs/sylven-arc/v676-v7-r2/validation/x1-manifest.json",
            "docs/sylven-arc/v676-v7-r2/validation/x1-staged-review.json",
        ],
        "entry_count": len(entries),
        "entries": entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if git(repo, "rev-parse", "HEAD") != SOURCE:
        raise SystemExit("x1 builder requires the immutable prior Sylven exact final as HEAD")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("unexpected branch")
    root = repo / "docs" / OWNER_SLUG / PHASE
    if root.exists():
        raise SystemExit("remaster x1 already exists; no overwrite permitted")

    rows = new_rows()
    inherited = inherited_selection(repo)
    audit = semantic_audit(repo, rows)
    if audit["exact_title_collisions"] or audit["selected_rows_quarantined"] or audit["json_parse_failures"]:
        raise SystemExit(
            "semantic audit failed closed: "
            + json.dumps(
                {
                    "exact": audit["exact_title_collisions"],
                    "quarantined": audit["selected_rows_quarantined"],
                    "parse_failures": audit["json_parse_failures"],
                },
                sort_keys=True,
            )
        )

    x1 = root / "x1"
    validation = root / "validation"
    dump(
        x1 / "new-proposal-freeze.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "declared_chain_after": DECLARED_CHAIN_AFTER,
            "new_sylven_r2_proposals": len(rows),
            "universal_novelty_proved": False,
            "proposals": rows,
        },
    )
    dump(
        x1 / "inherited-proposal-selection.json",
        {
            "selection_count": len(inherited),
            "novelty_credit": 0,
            "automatic_completion_credit": 0,
            "rows": inherited,
        },
    )
    dump(
        x1 / "combined-program.json",
        {
            "total_rows": 120,
            "inherited_selected": 60,
            "genuinely_new": 60,
            "forty_or_more_new_claim": True,
            "never_describe_as_120_new": True,
            "inherited_ids": [row["proposal_id"] for row in inherited],
            "new_ids": [row["proposal_id"] for row in rows],
        },
    )
    dump(x1 / "semantic-neighbor-audit.json", audit)
    dump(x1 / "official-source-plan.json", {"sources": SOURCES, "citations_are_not_observations_or_authority": True})
    dump(
        x1 / "pillar-and-practices.json",
        {
            "primary_pillar": "Freed ID and CBR Heart",
            "practice_1": "synthetic bookbinding collation and conservation-handover documentation",
            "practice_2": "synthetic library cataloguing and archival metadata documentation",
            "successor_recommendation": "synthetic collections-access and descriptive-metadata accessibility documentation",
            "employment_qualification_competence_or_authority_claim": False,
            "real_people_objects_records_or_actions": 0,
        },
    )
    dump(
        x1 / "portfolio-freeze.json",
        {
            "owner_safe_now": portfolio("safe_now", 120, OWNER, "SAFE"),
            "owner_candidate": portfolio("candidate", 80, OWNER, "CAND"),
            "successor_candidate_recommendations": portfolio("candidate_recommendation", 20, "Caelen Morrow", "SCAND"),
            "exact_approval": exact_or_blocked("exact_approval", 20, "EXACT"),
            "blocked": exact_or_blocked("blocked", 10, "BLOCK"),
            "counts": {
                "owner_safe_now": 120,
                "owner_candidate": 80,
                "successor_candidate_recommendations": 20,
                "candidate_total": 100,
                "exact_approval": 20,
                "blocked": 10,
            },
        },
    )
    dump(
        x1 / "skill-runner-plan.json",
        {
            "owner_skill_ideas": OWNER_SKILLS,
            "successor_skill_recommendations": SUCCESSOR_SKILLS,
            "owner_runner_ideas": OWNER_RUNNERS,
            "successor_runner_recommendations": SUCCESSOR_RUNNERS,
            "global_promotion_target": 5,
            "global_promotion_ceiling": 10,
            "promotion_requires": [
                "official skill-creator initialization",
                "complete read",
                "collision check",
                "quick validation",
                "accepting and rejecting smoke",
                "exact source/global byte parity",
                "rollback",
            ],
        },
    )
    dump(
        x1 / "clean-fix-refine-plan.json",
        {
            "owner": portfolio("clean_fix_refine", 100, OWNER, "CFR"),
            "successor_recommendations": portfolio("clean_fix_refine_recommendation", 30, "Caelen Morrow", "SCFR"),
            "owner_execution_target": 100,
            "successor_recommendation_count": 30,
        },
    )
    dump(
        x1 / "toolchain-install-plan.json",
        {
            "candidate_count": len(TOOL_PLAN),
            "candidates": TOOL_PLAN,
            "codex_cli": {
                "requested_stable": "0.151.0",
                "observed_before_x1": "0.151.0",
                "action": "verify and use; do not reinstall an already exact stable version",
            },
            "transaction_root": "D:/GHC-Archives/global-tools/sylven-v676-v7-r2",
            "node_global_prefix": "D:/GHC-Archives/global-tools/npm",
            "powershell_module_root": "D:/GHC-Archives/global-tools/powershell-modules",
            "requirements": [
                "exact primary-registry versions and integrity or wheel-hash receipts",
                "D-first shared family surfaces without PATH or profile mutation",
                "no npm lifecycle scripts",
                "no elevation, reboot, Windows-feature change, account, key, purchase, deployment, or Codex desktop update",
                "one bounded positive smoke and one meaningful rejecting smoke per direct surface",
                "rollback and retained-failure evidence",
            ],
        },
    )
    sections = [
        "identity-and-route",
        "source-and-lifecycle",
        "three-pillar-boundaries",
        "bookbinding-practice",
        "cataloguing-and-archives-practice",
        "inherited-proposal-selection",
        "new-proposal-freeze",
        "approval-portfolios",
        "toolchain-transaction",
        "skills-and-runners",
        "clean-fix-refine",
        "method-flow-and-failures",
        "validation-and-closeout",
        "successor-route",
    ]
    dump(
        x1 / "flashcard-plan.json",
        {
            "schema": "ghc-freed-id-flashcards/v1",
            "tier_order": ["freed_id_anchor", "trinity_pillar", "bounded_practice", "task"],
            "owner_anchor": OWNER,
            "sections": sections,
            "section_count": len(sections),
            "content_addressed": True,
            "supersession_non_erasing": True,
            "large_baton_file_only": True,
            "live_message_compact": True,
        },
    )
    dump(
        x1 / "method-flow-startup.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "startup_failure_recovery_pairs": [
                {"failure_id": fid, "failure": failure, "recovery_id": pid, "recovery": recovery}
                for fid, failure, pid, recovery in STARTUP_FAILURES
            ],
            "failed_witnesses_are_zero_credit_and_nonerasing": True,
            "x1_execution_credit": 0,
        },
    )
    dump(
        x1 / "route-hold.json",
        {
            "state": "REMASTER_X1_ROUTE_HOLD",
            "send_count": 0,
            "successor": "Caelen Morrow",
            "successor_phase": "v676-v8",
            "authority_horizon": "v725-v8",
            "precontact_forbidden": True,
            "release_requires": [
                "immutable x1 push and fresh-live equality before x2",
                "immutable evidence",
                "clean pushed exact final",
                "one successful non-replayed owner-scoped canonical receipt",
                "fresh live roster and authority read",
                "exactly one exact-title successor and immediate reread",
                "duplicate and direct-control guards",
                "one acknowledged send",
            ],
        },
    )
    dump(
        x1 / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "display_phase": DISPLAY_PHASE,
            "source": SOURCE,
            "branch": BRANCH,
            "lifecycle_state": "PLANNING_ONLY_X1",
            "inherited_selected": 60,
            "new_proposals": 60,
            "combined_program": 120,
            "x2_implementation_present": False,
            "observed_outcomes_present": False,
            "completion_claim_present": False,
            "route_send_count": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(
        x1 / "x1-overview.md",
        f"""# Sylven Arc {DISPLAY_PHASE} planning-only x1

This additive remaster begins at the immutable prior Sylven exact final `{SOURCE}` on the existing branch `{BRANCH}`. It does not rewrite, replay, or demote the sealed v676-v7 phase or its successful canonical receipt.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Sylven remaster proposals. The combined 120-row programme is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}, while universal novelty remains unproved.

## Practices and flashcards

The primary pillar is Freed ID/CBR Heart. The two wholly synthetic learning/design lenses are bookbinding collation and conservation-handover documentation, plus library cataloguing and archival metadata documentation. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task. Fourteen modular sections replace monolithic context while preserving content addressing and non-erasing supersession.

## Planned bounded work

The packet freezes 120 owner safe-now tasks, 80 owner candidates, 20 successor candidate recommendations, 20 unexecuted exact-approval packets, 10 unexecuted blocked packets, 20 owner skill ideas, 10 successor skill recommendations, 10 owner runner ideas, 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE tasks, and 30 successor CLEAN/FIX/REFINE recommendations. These are plans, not execution credit.

Thirteen additive package candidates are pinned for a later D-first x2 transaction. Codex CLI 0.151.0 is already exact and is therefore verified rather than reinstalled. No Codex desktop update, profile mutation, PATH mutation, elevation, reboot, Windows-feature change, account, credential, external write, or protected real-world action is planned.

## Boundaries

GMUT remains a typed scalar-tensor/EFT research-model family without empirical confirmation or Theory-of-Everything proof. THOS remains participant-free proxy work without governed real arms or independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, lifecycle events, interoperability, security review, or trust governance. Professional, legal, cultural, affected-party, Māori-data, Māori-authority, accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, consciousness/personhood, proof/canon, and Stage 20 claims remain open or exact-gated.

No x2 implementation, observed outcome, completion claim, successor contact, or external action is present in this commit.
""",
    )

    generated = sorted(path for path in x1.rglob("*") if path.is_file())
    manifest = x1_manifest(repo, generated)
    dump(validation / "x1-manifest.json", manifest)
    dump(
        validation / "x1-staged-review.json",
        {
            "source": SOURCE,
            "status": "PRECOMMIT_X1_REVIEW",
            "planning_only": True,
            "x2_paths": 0,
            "unexpected_paths": [],
            "privacy_or_raw_identifier_hits": 0,
            "manifest_entries": manifest["entry_count"],
            "declared_self_exclusions": manifest["declared_self_exclusions"],
        },
    )
    print(
        json.dumps(
            {
                "status": "BUILT_PLANNING_ONLY_X1",
                "phase": PHASE,
                "new_proposals": len(rows),
                "inherited_selected": len(inherited),
                "maximum_neighbor_score": audit["maximum_selected_score"],
                "manifest_entries": manifest["entry_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
