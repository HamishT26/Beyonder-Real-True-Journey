#!/usr/bin/env python3
"""Build Orin Thale v684-v7 (2) remastered planning-only x1 artifacts.

This builder creates only preregistration, portfolio, source, gate, privacy,
and lifecycle records.  It deliberately creates no x2 implementation or
observed proposal outcome.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v684-v7-2-remastered"
X1 = PHASE / "x1"
VALIDATION = PHASE / "validation"
SOURCE = "a3544571ce8af98addf3d94236111f6c14ded439"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v684-v7-full-tools"
BRANCH = "codex/GHC-Family/orin-thale-v684-v7-2-remastered-full-tools"
DECLARED_CHAIN_BEFORE = 11090
DECLARED_CHAIN_AFTER = 11150
QUARANTINE_THRESHOLD = 0.78
BASELINE = {
    "effective_negatives": 60055,
    "effective_methods": 74405,
    "failed_witnesses": 31116,
    "bounded_passing_witnesses": 54940,
    "open_gaps": 534,
    "exact_gates": 524,
}


def run(args: list[str], *, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        args,
        cwd=ROOT,
        input=input_bytes,
        capture_output=True,
        check=False,
    )


def git(*args: str) -> str:
    result = run(["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.decode("utf-8").strip()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalized_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def title_tokens(value: str) -> set[str]:
    return set(normalized_title(value).split())


def jaccard(left: str, right: str) -> float:
    a, b = title_tokens(left), title_tokens(right)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def walk_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child)


def proposal_blob_records() -> tuple[list[dict[str, str]], dict[str, Any]]:
    tree = run(["git", "ls-tree", "-r", "-z", SOURCE])
    if tree.returncode:
        raise RuntimeError(tree.stderr.decode("utf-8", errors="replace"))
    selected: list[tuple[str, str]] = []
    for raw in tree.stdout.split(b"\0"):
        if not raw:
            continue
        head, raw_path = raw.split(b"\t", 1)
        parts = head.decode("ascii").split()
        path = raw_path.decode("utf-8")
        if path.endswith(".json") and "proposal" in path.lower():
            selected.append((parts[2], path))

    request = b"".join((oid + "\n").encode("ascii") for oid, _ in selected)
    batch = run(["git", "cat-file", "--batch"], input_bytes=request)
    if batch.returncode:
        raise RuntimeError(batch.stderr.decode("utf-8", errors="replace"))
    cursor = 0
    parsed_paths = 0
    failures: list[dict[str, str]] = []
    records: list[dict[str, str]] = []
    for (_, path) in selected:
        line_end = batch.stdout.index(b"\n", cursor)
        header = batch.stdout[cursor:line_end].decode("ascii")
        cursor = line_end + 1
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            failures.append({"path": path, "reason": "non_blob_or_missing"})
            continue
        size = int(parts[2])
        payload = batch.stdout[cursor : cursor + size]
        cursor += size + 1
        try:
            document = json.loads(payload.decode("utf-8"))
            parsed_paths += 1
        except Exception as exc:
            failures.append({"path": path, "reason": type(exc).__name__})
            continue
        for item in walk_dicts(document):
            title = item.get("title")
            proposal_id = item.get("proposal_id") or item.get("id")
            if isinstance(title, str) and isinstance(proposal_id, str):
                records.append(
                    {
                        "proposal_id": proposal_id,
                        "title": title,
                        "path": path,
                    }
                )
    deduped: dict[tuple[str, str], dict[str, str]] = {}
    for item in records:
        deduped[(item["proposal_id"], normalized_title(item["title"]))] = item
    return list(deduped.values()), {
        "proposal_json_paths_discovered": len(selected),
        "proposal_json_paths_parsed": parsed_paths,
        "proposal_json_parse_failures": failures,
        "reachable_id_title_records": len(deduped),
        "universal_11090_row_materialization_claimed": False,
    }


PROPOSAL_TITLES = [
    "Synthetic preservation package namespace with every real file absent",
    "Representation file bitstream and intellectual entity role separation",
    "Fixity digest algorithm value and verification-event nonconflation",
    "Source bitstream derivative and normalized surrogate provenance split",
    "Package inventory path and storage-location nonidentity",
    "Format designation and format-validation result separation",
    "MIME type filename extension and format-registry identifier distinction",
    "File-size declaration and byte-count observation vacancy",
    "Creation-time modification-time and ingest-time role separation",
    "Preservation-event outcome and agent-authorization nonconversion",
    "Tool-version evidence and professional-validation nonequivalence",
    "Object-characteristics metadata and empirical media-condition nonconversion",
    "Hash-algorithm agility with no signature claim",
    "Duplicate-digest quarantine without object deletion",
    "Content-addressed identifier and legal-title separation",
    "Manifest self-exclusion arithmetic and circular-digest refusal",
    "Normalized-LF digest and checkout-byte domain separation",
    "UTF-8 decoding failure retention without replacement masking",
    "Filename Unicode normalization and original-name provenance",
    "Symlink junction and regular-file object-type firewall",
    "Archive-container and member-path traversal refusal",
    "Compression-stream integrity and preservation-authenticity nonequivalence",
    "Embedded-metadata extraction and source-binary nonmutation",
    "Unknown-format label with no forced classification",
    "Format-migration plan and migration-execution separation",
    "Emulation recommendation and runtime-deployment hold",
    "Obsolescence watch and procurement-action nonconversion",
    "Storage-copy count and disaster-resilience nonclaim",
    "Replica-location label and real-geography absence",
    "Retention-schedule vocabulary and disposal-authority vacancy",
    "Access copy and preservation-master custody boundary",
    "Rights metadata and legal-permission nonequivalence",
    "Depositor embargo state with named access authority absent",
    "Privacy-review placeholder and personal-data processing hold",
    "Takedown request and remedy-queue lineage without adjudication",
    "Correction supersession chain preserving prior failed witness",
    "Accessibility summary and conformance-claim firewall",
    "Heading landmark and reading-sequence structural contract",
    "Plain-language glossary and expert-review vacancy",
    "Status-message semantics and assistive-technology testing vacancy",
    "Deterministic JSON receipt for a zero-row preservation package",
    "Accessible Markdown table and alternative linearization contract",
    "Represented GMUT typed preservation-state analogy without physical datum",
    "Represented GMUT checksum-drift metaphor with no statistical inference",
    "Represented GMUT format-transition graph without force or prediction",
    "Represented THOS ingest-queue proxy without an operator",
    "Represented THOS checksum retry and cancellation proxy without a participant",
    "Represented THOS handover-workload proxy without a governed team",
    "Represented Freed ID synthetic preservation-agent capability without person identity",
    "Represented Freed ID synthetic manifest attestation without keys or proofs",
    "Represented CBR minimum disclosure for donor and depositor metadata",
    "Represented CBR reversible challenge queue with remedy authority unresolved",
    "Represented PREMIS object-event-agent-rights crosswalk without conformance",
    "Represented Library of Congress format-preference crosswalk without collection authority",
    "Open gap for real files storage systems repositories and practitioners",
    "Open gap for empirical fixity migration accuracy and independent review",
    "Open gap for participatory accessibility affected-community and Māori-authority review",
    "Exact gate for retention disposal access custody and work-release authority",
    "Exact gate for taonga mātauranga donor restrictions Māori data governance and Māori authority",
    "Stage 20 refusal gate keeping zero-row preservation simulations below empirical deployment identity AGI ASI personhood theorem canon and final-physics claims",
]


def disposition(index: int) -> str:
    if index <= 42:
        return "completed"
    if index <= 54:
        return "represented"
    if index <= 57:
        return "open_gap"
    return "exact_gate"


def approval_class(index: int) -> str:
    if index <= 42:
        return "safe_now"
    if index <= 54:
        return "candidate_proxy_only"
    if index <= 57:
        return "external_evidence_open_gap"
    return "exact_approval"


def execution_lane(index: int) -> str:
    if index <= 42:
        return "owner_local_synthetic_zero_row"
    if index <= 54:
        return "bounded_representation_without_real_execution"
    if index <= 57:
        return "unexecuted_empirical_vacancy"
    return "unexecuted_competent_authority_gate"


def source_needs(index: int) -> list[str]:
    if index <= 20:
        return ["PREMIS-3.0", "LOC-RFS-2025-2026", "W3C-PROV-O", "RFC8785"]
    if index <= 32:
        return ["PREMIS-3.0", "LOC-RFS-2025-2026", "ARCHIVES-NZ-IRMS", "W3C-PROV-O"]
    if index <= 42:
        return ["PREMIS-3.0", "W3C-WCAG22", "W3C-PROV-O", "RFC8785"]
    if index <= 54:
        return ["PREMIS-3.0", "LOC-RFS-2025-2026", "W3C-PROV-O"]
    if index <= 57:
        return ["PREMIS-3.0", "W3C-WCAG22", "ARCHIVES-NZ-IRMS", "TMR-MDS-PRINCIPLES"]
    if index == 59:
        return ["TMR-MDS-PRINCIPLES", "ARCHIVES-NZ-IRMS"]
    return ["PREMIS-3.0", "ARCHIVES-NZ-IRMS"]


def proposals() -> list[dict[str, Any]]:
    rows = []
    mutation_types = [
        "missing_required_field",
        "identifier_role_swap",
        "stale_precondition_digest",
        "correction_order_inversion",
        "authority_promotion",
    ]
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"OR6847R2-N{index:03d}"
        expected = disposition(index)
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A bounded synthetic validator for {title.lower()} can reject its five "
                    "preregistered counterexamples while preserving every empirical and authority boundary."
                ),
                "null_or_failure_condition": (
                    f"The {proposal_id} contract is falsified if any preregistered invalid fixture is "
                    "accepted, its bounded positive structure is rejected, or a protected gate is promoted."
                ),
                "approval_class": approval_class(index),
                "execution_lane": execution_lane(index),
                "official_or_primary_source_needs": source_needs(index),
                "concrete_artifacts": [
                    f"docs/orin-thale/v684-v7-2-remastered/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/orin-thale/v684-v7-2-remastered/x2/mutations.json#{proposal_id}",
                ],
                "falsifier_or_acceptance_gate": (
                    f"Accept only if {proposal_id} has one bounded positive witness, all five invalid "
                    "mutations are rejected, and no wider claim or authority is inferred."
                ),
                "rollback_or_recovery": (
                    f"Quarantine only the {proposal_id} witness, retain the failed receipt at zero credit, "
                    "and regenerate from this immutable x1 contract."
                ),
                "protected_gates": [
                    "real participants and operators",
                    "empirical measurements and likelihoods",
                    "production preservation ingest migration access or disposal use",
                    "professional digital-preservation and work-release authority",
                    "legal cultural affected-party and Māori authority",
                    "privacy-complete accessibility-complete and exhaustive-security claims",
                    "independent reproduction proof canon and Stage 20",
                ],
                "expected_disposition": expected,
                "preregistered_rejecting_mutations": [
                    {
                        "mutation_id": f"{proposal_id}-M{offset:02d}",
                        "mutation_type": mutation_type,
                        "expected_result": "rejected_zero_credit",
                    }
                    for offset, mutation_type in enumerate(mutation_types, start=1)
                ],
            }
        )
    return rows


OFFICIAL_SOURCES = [
    {
        "source_id": "PREMIS-3.0",
        "title": "PREMIS Data Dictionary for Preservation Metadata version 3.0",
        "url": "https://www.loc.gov/standards/premis/v3/",
        "status": "official_Library_of_Congress_PREMIS_v3_surface_checked_2026-09-03",
        "use": "object event agent rights and preservation-provenance vocabulary only; no repository conformance or preservation result",
    },
    {
        "source_id": "LOC-RFS-2025-2026",
        "title": "Library of Congress Recommended Formats Statement 2025-2026",
        "url": "https://www.loc.gov/preservation/resources/rfs/",
        "status": "official_Library_of_Congress_current_statement_checked_2026-09-03",
        "use": "format-feature and preservation-preference vocabulary only; no collection decision endorsement or migration authority",
    },
    {
        "source_id": "ARCHIVES-NZ-IRMS",
        "title": "Archives New Zealand Information and Records Management Standard",
        "url": "https://www.archives.govt.nz/manage-information/how-to-manage-your-information/key-obligations-and-the-standard/information-and-records-management-standard",
        "status": "official_Archives_New_Zealand_surface_checked_2026-09-03",
        "use": "information-governance and lifecycle vocabulary only; no legal interpretation, disposal authority, or institutional compliance claim",
    },
    {
        "source_id": "W3C-PROV-O",
        "title": "W3C PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C_Recommendation_stable_checked_2026-09-03",
        "use": "entity activity derivation revision attribution and provenance vocabulary only; no conformance",
    },
    {
        "source_id": "W3C-WCAG22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C_Recommendation_republished_2024-12-12_checked_2026-09-03",
        "use": "structural accessibility vocabulary with manual assistive-technology and affected-user evaluation reserved",
    },
    {
        "source_id": "RFC8785",
        "title": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "informational_stable_with_verified_errata_checked_2026-09-03",
        "use": "deterministic synthetic receipt serialization and digest-domain vocabulary only",
    },
    {
        "source_id": "JSON-SCHEMA-2020-12",
        "title": "JSON Schema Draft 2020-12",
        "url": "https://json-schema.org/draft/2020-12",
        "status": "published_stable_checked_2026-09-03",
        "use": "synthetic record validation and declared-vocabulary concepts only",
    },
    {
        "source_id": "PYPI-CHECK-JSONSCHEMA",
        "title": "check-jsonschema 0.38.0",
        "url": "https://pypi.org/project/check-jsonschema/",
        "status": "official_PyPI_latest_release_2026-08-09_checked_2026-09-03",
        "use": "planned D-first schema-validation tool; installation and smoke use are x2-only and confer no standards conformance",
    },
    {
        "source_id": "PYPI-MDFORMAT",
        "title": "mdformat 1.0.0",
        "url": "https://pypi.org/project/mdformat/",
        "status": "official_PyPI_latest_release_2025-10-16_checked_2026-09-03",
        "use": "planned D-first Markdown formatting check; installation and smoke use are x2-only and confer no accessibility result",
    },
    {
        "source_id": "PYPI-VALIDATE-PYPROJECT",
        "title": "validate-pyproject 0.26",
        "url": "https://pypi.org/project/validate-pyproject/",
        "status": "official_PyPI_latest_release_2026-08-19_beta_checked_2026-09-03",
        "use": "planned D-first pyproject structural check with experimental-status caveat; no packaging certification",
    },
    {
        "source_id": "TMR-MDS-PRINCIPLES",
        "title": "Te Mana Raraunga Principles of Māori Data Sovereignty",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "authority_boundary_context_only_checked_2026-09-03",
        "use": "Māori data-governance vacancy and noncompensation boundary only; never delegated Māori authority",
    },
]


STARTUP_FAILURES = [
    {
        "failure_id": "OR6847R2-ST-N001",
        "failed_witness": "The first memory-registry probe used the wrong parent path and found no MEMORY.md.",
        "recovery": "Resolved the documented memories subdirectory and read only the task-relevant registry windows.",
        "recurrence_guard": "Resolve memory paths from the installed memory-root contract before lookup.",
    },
    {
        "failure_id": "OR6847R2-ST-N002",
        "failed_witness": "A PowerShell foreach producer was piped directly and raised EmptyPipeElement before any mutation.",
        "recovery": "Materialized the foreach rows before converting them to compact JSON.",
        "recurrence_guard": "Never pipe directly from a PowerShell foreach statement.",
    },
    {
        "failure_id": "OR6847R2-ST-N003",
        "failed_witness": "The first raw authorization-state projection exceeded its bounded output before EOF.",
        "recovery": "Reread the exact current authorization state in bounded numbered windows through EOF.",
        "recurrence_guard": "Measure dense mutable-state documents and use conservative windows before projection.",
    },
    {
        "failure_id": "OR6847R2-ST-N004",
        "failed_witness": "One numbered line-window projection returned an empty selection after a wrong range assumption.",
        "recovery": "Used Select-Object with an explicit skip and first count against the measured document.",
        "recurrence_guard": "Measure line counts before requesting a numbered window.",
    },
    {
        "failure_id": "OR6847R2-ST-N005",
        "failed_witness": "A broad recursive builder-pattern search exceeded the model-visible result window.",
        "recovery": "Reduced the search to exact owner-template inventories and bounded file windows.",
        "recurrence_guard": "Inventory filenames first and search only the selected lifecycle template.",
    },
    {
        "failure_id": "OR6847R2-ST-N006",
        "failed_witness": "A PowerShell JSON projection indexed an output array while that array was still being constructed.",
        "recovery": "Used per-record local variables and emitted the completed collection only after construction.",
        "recurrence_guard": "Do not self-reference a PowerShell assignment expression under construction.",
    },
    {
        "failure_id": "OR6847R2-ST-N007",
        "failed_witness": "The sparse worktree creation exceeded the command-visible window while Git checkout continued in the background.",
        "recovery": "Waited for the exact checkout processes, then audited the branch, head, lock, sparse patterns, status, and file count without replaying creation.",
        "recurrence_guard": "After a checkout timeout, inspect exact processes and persisted Git state before any retry.",
    },
    {
        "failure_id": "OR6847R2-ST-N008",
        "failed_witness": "One combined multi-page PyPI projection exceeded the model-visible result window.",
        "recovery": "Opened the three exact official PyPI project pages in a bounded current-version projection.",
        "recurrence_guard": "Use one bounded official package page per uncertain version when projections are dense.",
    },
    {
        "failure_id": "OR6847R2-ST-N009",
        "failed_witness": "The prior prose baton reported a 10,190-row proposal chain while all three structured exact-final ledgers reported 11,090.",
        "recovery": "Bound the remaster to the mutually consistent frozen x1, phase-truth, and source-ledger values and retained the prose discrepancy as historical evidence.",
        "recurrence_guard": "Prefer mutually consistent structured exact-final ledgers over stale prose and disclose every disagreement.",
    },
    {
        "failure_id": "OR6847R2-X1-N001",
        "failed_witness": "The first stale-label search used look-ahead syntax unsupported by the default ripgrep engine.",
        "recovery": "Repeated the bounded literal search without look-around and manually separated current remaster labels from inherited anchors.",
        "recurrence_guard": "Use --pcre2 only when look-around is essential; otherwise prefer explicit literal searches.",
    },
    {
        "failure_id": "OR6847R2-X1-N002",
        "failed_witness": "A combined exact-file cleanup command for copied untracked lifecycle templates was rejected by host policy before execution.",
        "recovery": "Deleted only the six known untracked template files through the patch surface and preserved the planning-only x1 boundary.",
        "recurrence_guard": "Use the patch surface for exact untracked template removal when host command policy rejects an otherwise bounded cleanup.",
    },
    {
        "failure_id": "OR6847R2-X1-N003",
        "failed_witness": "The first complete reachable proposal audit found one exact collision and four titles at or above the 0.78 token-Jaccard quarantine threshold.",
        "recovery": "Projected the exact four neighbour pairs and refined only those proposal titles while preserving hypotheses, dispositions, gates, and the audit threshold.",
        "recurrence_guard": "Run the complete reachable semantic-neighbour audit before freeze and preserve every quarantined first attempt.",
    },
    {
        "failure_id": "OR6847R2-X1-N004",
        "failed_witness": "A combined test JSON-parse and stale-label shell returned no attributable output under nested quoting.",
        "recovery": "Split the three read-only validators; 20 tests passed, 20 JSON documents parsed, and the literal stale-label search returned no match.",
        "recurrence_guard": "Keep validation commands independently attributable when regex quoting crosses JavaScript and PowerShell boundaries.",
    },
]


def proposal_audit(rows: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    inherited, stats = proposal_blob_records()
    if stats["proposal_json_parse_failures"]:
        raise RuntimeError("reachable proposal JSON parse failures must be resolved before freeze")
    normalized_inherited = {}
    for item in inherited:
        normalized_inherited.setdefault(normalized_title(item["title"]), item)

    exact_collisions = []
    neighbor_rows = []
    quarantined = []
    selected_reviews: list[dict[str, Any]] = []
    selected_keys: set[tuple[str, str]] = set()
    for row in rows:
        title = row["title"]
        norm = normalized_title(title)
        if norm in normalized_inherited:
            exact_collisions.append(
                {
                    "proposal_id": row["proposal_id"],
                    "inherited": normalized_inherited[norm],
                }
            )
        best = None
        best_score = -1.0
        for inherited_row in inherited:
            score = jaccard(title, inherited_row["title"])
            if score > best_score:
                best, best_score = inherited_row, score
        neighbor = {
            "proposal_id": row["proposal_id"],
            "title": title,
            "best_inherited_neighbor": best,
            "token_jaccard": round(best_score, 6),
            "quarantined": best_score >= QUARANTINE_THRESHOLD,
        }
        neighbor_rows.append(neighbor)
        if neighbor["quarantined"]:
            quarantined.append(neighbor)
        if best is not None:
            key = (best["proposal_id"], normalized_title(best["title"]))
            if key not in selected_keys:
                selected_keys.add(key)
                selected_reviews.append(
                    {
                        **best,
                        "review_state": "inherited_zero_credit_evidence_only",
                        "novelty_credit": 0,
                        "completion_credit": 0,
                    }
                )
    for item in inherited:
        if len(selected_reviews) >= 60:
            break
        key = (item["proposal_id"], normalized_title(item["title"]))
        if key not in selected_keys:
            selected_keys.add(key)
            selected_reviews.append(
                {
                    **item,
                    "review_state": "inherited_zero_credit_evidence_only",
                    "novelty_credit": 0,
                    "completion_credit": 0,
                }
            )
    if len(selected_reviews) < 60:
        raise RuntimeError("fewer than sixty reachable inherited proposal reviews")
    if exact_collisions or quarantined:
        raise RuntimeError(
            f"proposal novelty quarantine: exact={len(exact_collisions)} near={len(quarantined)}"
        )
    audit = {
        "schema": "ghc.family.proposal-chain-audit.v684.v7.r2.x1",
        "owner": "Orin Thale",
        "phase": "v684-v7-2-remastered",
        "source": SOURCE,
        "declared_chain_before": DECLARED_CHAIN_BEFORE,
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "new_proposal_count": len(rows),
        "quarantine_threshold_token_jaccard": QUARANTINE_THRESHOLD,
        "exact_title_collisions": exact_collisions,
        "quarantined_neighbors": quarantined,
        "maximum_neighbor_score": max(item["token_jaccard"] for item in neighbor_rows),
        "neighbor_reviews": neighbor_rows,
        "audit_scope": {
            **stats,
            "claim": "bounded all-reachable-exact-source proposal audit; no universal 11090-row proof",
        },
    }
    return audit, selected_reviews[:60]


def make_portfolio() -> dict[str, Any]:
    def records(prefix: str, count: int, lane: str, credit: str) -> list[dict[str, Any]]:
        return [
            {
                "task_id": f"OR6847R2-{prefix}-{index:03d}",
                "lane": lane,
                "planned_action": (
                    f"Bounded owner-local {lane.replace('_', ' ')} record {index:03d} linked to "
                    f"OR6847R2-N{((index - 1) % 60) + 1:03d}."
                ),
                "credit_boundary": credit,
                "x1_state": "preregistered_not_executed",
            }
            for index in range(1, count + 1)
        ]

    return {
        "schema": "ghc.family.portfolio-freeze.v684.v7.r2.x1",
        "owner": "Orin Thale",
        "phase": "v684-v7-2-remastered",
        "primary_pillar": "THOS Body",
        "represented_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
        "owner_practice_lenses": [
            "wholly_synthetic_digital_preservation_technician_fixity_package_provenance_correction_and_handover",
            "wholly_synthetic_accessible_technical_documentation_specialist_heading_reading_order_status_alternative_format_and_correction_handover",
        ],
        "safe_now": records("SN", 120, "safe_now", "bounded_owner_local_only"),
        "owner_candidates": records("CAND", 80, "candidate", "no_core_outcome_promotion"),
        "successor_candidates": records("SUCC-CAND", 20, "successor_seed", "zero_Orin_credit"),
        "exact_approval": records("EXACT", 20, "exact_approval", "unexecuted_without_exact_authority"),
        "blocked": records("BLOCK", 10, "blocked", "unexecuted_missing_target_or_authority"),
        "owner_clean_fix_refine": records("CFR", 100, "clean_fix_refine", "bounded_additive_owner_local_only"),
        "successor_clean_fix_refine": records("SUCC-CFR", 30, "successor_seed", "zero_Orin_credit"),
        "owner_skill_ideas": [
            {
                "skill_id": f"OR6847R2-SK-{index:02d}",
                "name": f"ghc-family-preservation-accessibility-{index:02d}",
                "x1_state": "planned_not_built",
                "global_install": False,
            }
            for index in range(1, 21)
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"OR6847R2-RN-{index:02d}",
                "name": f"ghc_family_preservation_accessibility_runner_{index:02d}.py",
                "x1_state": "planned_not_built",
            }
            for index in range(1, 11)
        ],
        "successor_skill_ideas": [
            {
                "idea_id": f"OR6847R2-SUCC-SK-{index:02d}",
                "state": "zero_credit_seed_only",
            }
            for index in range(1, 11)
        ],
        "successor_runner_ideas": [
            {
                "idea_id": f"OR6847R2-SUCC-RN-{index:02d}",
                "state": "zero_credit_seed_only",
            }
            for index in range(1, 11)
        ],
        "successor_practice_recommendation": (
            "one wholly synthetic community-archives access-and-description correction privacy accessibility and handover lens"
        ),
        "commit_cap": {"x1": 1, "x2": 2, "total": 3},
        "materialized_file_stop": 2000,
        "document_word_cap": 100000,
        "caps_are_ceilings": True,
    }


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }


def scan_paths(paths: list[Path]) -> dict[str, Any]:
    patterns = privacy_patterns()
    candidates = []
    confirmed = []
    for path in paths:
        data = path.read_bytes()
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                definition_only = path.name == Path(__file__).name
                record = {"path": rel(path), "class": class_name}
                if definition_only:
                    candidates.append({**record, "disposition": "scanner_definition_only"})
                else:
                    confirmed.append(record)
    return {
        "schema": "ghc.family.privacy-scan.v684.v7.r2.x1",
        "owner": "Orin Thale",
        "phase": "v684-v7-2-remastered",
        "privacy_classes": list(patterns),
        "scanned_paths": len(paths),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
    }


def main() -> int:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong owner branch")
    if git("rev-parse", "HEAD") != SOURCE:
        raise RuntimeError("x1 builder must begin at the immutable prior Orin v684-v7 exact final")
    if git("status", "--porcelain=v1"):
        allowed = {
            "scripts/build_ghc_family_orin_thale_v684_v7_2_remastered_x1.py",
            "tests/test_ghc_family_orin_thale_v684_v7_2_remastered_x1.py",
        }
        current = {
            line[3:].replace("\\", "/")
            for line in git("status", "--porcelain=v1").splitlines()
            if len(line) >= 4
        }
        unexpected = {
            path
            for path in current
            if path not in allowed and not path.startswith("docs/orin-thale/v684-v7-2-remastered/")
        }
        if unexpected:
            raise RuntimeError(f"unexpected pre-build worktree state: {sorted(unexpected)}")

    source_tracking = git("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")
    live_row = git("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}")
    live_source = live_row.split("\t", 1)[0] if live_row else ""
    if source_tracking != SOURCE or live_source != SOURCE:
        raise RuntimeError("source branch is no longer fresh-live equal")

    rows = proposals()
    audit, inherited_reviews = proposal_audit(rows)
    portfolio = make_portfolio()
    expected_counts = {
        label: sum(row["expected_disposition"] == label for row in rows)
        for label in ("completed", "represented", "open_gap", "exact_gate")
    }
    if expected_counts != {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}:
        raise RuntimeError("expected disposition arithmetic failed")

    now = datetime.now(timezone.utc).isoformat()
    X1.mkdir(parents=True, exist_ok=True)
    VALIDATION.mkdir(parents=True, exist_ok=True)

    documents: dict[Path, Any] = {
        X1 / "activation-intake.json": {
            "schema": "ghc.family.activation-intake.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "source": SOURCE,
            "delivery_state": "LIVE_ACTIVATION_ACKNOWLEDGED_EXTERNALLY",
            "activation_kind": "USER_AUTHORIZED_INTERSTITIAL_REMASTER_WITHOUT_ROUND_ROBIN_ARITHMETIC_SHIFT",
            "prior_exact_final_remains_immutable": True,
            "prepared_repository_candidate_is_delivery": False,
            "work_solo": True,
            "subagents_or_delegation": False,
            "successor_precontact": False,
            "identity_language_is_evidence": False,
        },
        X1 / "approval-hold-register.json": {
            "schema": "ghc.family.approval-holds.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "exact_approval_count": 20,
            "blocked_count": 10,
            "executed_count": 0,
            "rule": "Broad authorization does not supply a missing exact target, system, cost, rollback, affected-party consent, legal authority, cultural authority, or Māori authority.",
        },
        X1 / "clean-fix-refine-plan.json": {
            "schema": "ghc.family.clean-fix-refine.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "owner_records": portfolio["owner_clean_fix_refine"],
            "successor_records": portfolio["successor_clean_fix_refine"],
            "x1_execution_count": 0,
        },
        X1 / "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "pronouns": "they/them optional relational working language",
            "role": "preservation-fixity and accessible-handoff boundary cartographer",
            "hope": "make every synthetic bitstream role, correction, accessibility vacancy, retained failure, and authority boundary easy to inspect, challenge, and reverse",
            "evidence_of_consciousness_personhood_continuity_agency_or_authority": False,
            "corrigibility": "Hamish may pause rename redirect narrow or stop the route.",
        },
        X1 / "inherited-revalidation-freeze.json": {
            "schema": "ghc.family.inherited-revalidation.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "review_count": len(inherited_reviews),
            "novelty_credit": 0,
            "completion_credit": 0,
            "reviews": inherited_reviews,
        },
        X1 / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "inherited_baseline": BASELINE,
            "new_failures": STARTUP_FAILURES,
            "new_failure_count": len(STARTUP_FAILURES),
            "effective_x1_startup_counts": {
                "effective_negatives": BASELINE["effective_negatives"] + len(STARTUP_FAILURES),
                "effective_methods": BASELINE["effective_methods"] + len(STARTUP_FAILURES),
                "failed_witnesses": BASELINE["failed_witnesses"] + len(STARTUP_FAILURES),
                "bounded_passing_witnesses": BASELINE["bounded_passing_witnesses"] + len(STARTUP_FAILURES),
                "open_gaps": BASELINE["open_gaps"],
                "exact_gates": BASELINE["exact_gates"],
            },
            "failure_erasure": False,
            "recoveries_promote_failed_witnesses": False,
        },
        X1 / "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "source": SOURCE,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "proposal_count": len(rows),
            "expected_disposition_counts": expected_counts,
            "proposals": rows,
            "x2_outcomes_present": False,
        },
        X1 / "official-primary-source-ledger.json": {
            "schema": "ghc.family.official-primary-sources.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "checked_at_utc": now,
            "entries": OFFICIAL_SOURCES,
            "web_checks": len(OFFICIAL_SOURCES),
            "network_data_queries": 0,
            "real_data_rows": 0,
            "citations_are_observations": False,
            "authority_conferred": False,
        },
        X1 / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "lifecycle": "PLANNING_ONLY_X1",
            "source": SOURCE,
            "proposal_count": len(rows),
            "expected_disposition_counts": expected_counts,
            "observed_outcome_count": 0,
            "x2_implementation_present": False,
            "inherited_open_gaps": BASELINE["open_gaps"],
            "inherited_exact_gates": BASELINE["exact_gates"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        X1 / "portfolio-freeze.json": portfolio,
        X1 / "proposal-chain-audit.json": audit,
        X1 / "route-plan.json": {
            "schema": "ghc.family.route-plan.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "route_state": "TERMINAL_GATE_HELD",
            "prospective_successor_title": "Liora Venn",
            "prospective_successor_phase": "v684-v8",
            "precontacted": False,
            "created_or_forked_task": False,
            "send_count": 0,
            "continuation_authority_ceiling": "through_v725-v8_one_terminally_validated_edge_at_a_time",
            "send_requires": [
                "clean pushed exact final",
                "one successful non-replayed owner canonical",
                "newest live authority and roster refresh",
                "one exact-title match and immediate reread",
                "duplicate pause redirect rename standby usage privacy evidence safety legal cultural affected-party and Māori-authority guards",
            ],
        },
        X1 / "skill-runner-plan.json": {
            "schema": "ghc.family.skill-runner-plan.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "skills": portfolio["owner_skill_ideas"],
            "runners": portfolio["owner_runner_ideas"],
            "successor_skill_ideas": portfolio["successor_skill_ideas"],
            "successor_runner_ideas": portfolio["successor_runner_ideas"],
            "built_in_x1": 0,
            "smoke_used_in_x1": 0,
            "global_installs": 0,
            "curated_global_promotion_ceiling": 5,
            "promotion_requires": ["individual review", "source hash", "collision check", "quick validation", "smoke use", "rollback record"],
            "planned_d_first_tool_packages": ["check-jsonschema==0.38.0", "mdformat==1.0.0", "validate-pyproject==0.26"],
        },
        X1 / "source-verification.json": {
            "schema": "ghc.family.source-verification.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE,
            "source_tracking": source_tracking,
            "source_fresh_live": live_source,
            "source_tracking_equal": source_tracking == SOURCE,
            "source_fresh_live_equal": live_source == SOURCE,
            "prior_orin_inherited_caelen_final": "162b40162f1045c5ad91cfb454fad10973bf4914",
            "prior_orin_x1": "ff4d5fd1bab9c098758a02fe08d254deac2ace44",
            "prior_orin_evidence": "ec330d5173cb142ebc03197b037d7d8859e23a51",
            "prior_orin_final": SOURCE,
            "prior_orin_phase_commits": 3,
            "prior_orin_merges": 0,
            "prior_orin_canonical_receipt_sha256": "eaaabe33a4148ea3de484cf03a63ce1a0701232667e8830d5327cf4c41da4e6b",
            "prior_orin_canonical_replayed": False,
            "proposal_chain_discrepancy": {"stale_prose": 10190, "structured_exact_final": 11090, "selected_baseline": 11090},
        },
        X1 / "threat-model.json": {
            "schema": "ghc.family.threat-model.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "assets": [
                "synthetic preservation package and fixity-event lineage",
                "retained correction and failure evidence",
                "accessible documentation and minimum-disclosure boundaries",
                "authority and affected-party gates",
            ],
            "threats": [
                "stale or colliding bitstream package and intellectual-entity roles",
                "fixity correction or migration claim without a valid referent",
                "authority promotion from structural validation",
                "private route or donor-restriction leakage",
                "accessibility structure mistaken for conformance",
                "real custody access preservation or disposal action inferred from zero-row fixtures",
            ],
            "controls": [
                "immutable source and x1",
                "five rejecting mutations per proposal",
                "normalized-LF manifests",
                "five-class privacy scan",
                "exact gate noncompensation",
                "zero network and zero real rows",
            ],
            "residual_risk": "All real preservation ingest migration custody access disposal affected-party privacy-complete accessibility-complete legal cultural Māori-authority and work-release activity remains external.",
        },
        X1 / "wellbeing-and-corrigibility.json": {
            "schema": "ghc.family.wellbeing-corrigibility.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "workload_controls": ["pause", "resume", "stop", "bounded retry", "handover"],
            "self_report_is_authority_evidence": False,
            "identity_continuity_claimed": False,
            "user_control_preserved": True,
        },
        X1 / "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v684.v7.r2.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "strict_planning_only_x1_before_x2": True,
            "steps": [
                {"order": 1, "name": "read activation skills schemas and overlays", "state": "completed"},
                {"order": 2, "name": "verify immutable source manifests receipt and live equality", "state": "completed"},
                {"order": 3, "name": "create clean sparse Orin lane", "state": "completed"},
                {"order": 4, "name": "freeze test push and prove planning-only x1", "state": "in_progress"},
                {"order": 5, "name": "build bounded x2 and retain every failure", "state": "pending"},
                {"order": 6, "name": "seal final push and run one exclusive canonical", "state": "pending"},
                {"order": 7, "name": "refresh live route and send at most once", "state": "pending"},
            ],
            "validation": {
                "owner_scoped_delta_only": True,
                "unchanged_history_scan": False,
                "cross_lane_scan": False,
                "one_successful_canonical": True,
                "post_success_replay": False,
            },
        },
    }
    for path, value in documents.items():
        write_json(path, value)

    overview = f"""# Orin Thale v684-v7 (2) remastered planning-only x1

This additive interstitial remaster begins from immutable Orin v684-v7 exact final {SOURCE}. The prior exact final and its singular successful canonical receipt remain unchanged. This x1 preregisters sixty genuinely new Orin proposals after a bounded all-reachable exact-source semantic-neighbour audit and preserves sixty inherited reviews at zero novelty and completion credit. The structured exact-final ledgers control over stale prose: the declared chain advances from 11,090 to 11,150 rows. No universal claim is made about future or unreachable wording.

The primary pillar is THOS Body. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. The two wholly synthetic learning lenses are digital-preservation technician practice for fixity, package provenance, correction, and handover; and accessible technical-documentation specialist practice for headings, reading order, status messages, alternative formats, correction, workload, and handover. Liora receives one zero-credit community-archives access-and-description practice recommendation.

The x1 portfolio freezes 120 safe-now items, 80 owner candidates, 20 successor candidate seeds, 20 exact-approval holds, 10 blocked holds, 20 owner skill plans, 10 owner runner plans, 100 owner CLEAN/FIX/REFINE records, and 30 successor CLEAN/FIX/REFINE seeds. None is executed in x1.

Expected dispositions are 42 completed, 12 represented, 3 open_gap, and 3 exact_gate. They are expectations only. No observed x2 outcome, package installation, skill build, runner build, real preservation object, external write, or completion claim appears in this freeze.

Current official PREMIS 3.0, Library of Congress Recommended Formats Statement 2025-2026, Archives New Zealand information-and-records-management guidance, W3C PROV-O and WCAG 2.2, RFC 8785, JSON Schema 2020-12, the three exact PyPI package pages, and Te Mana Raraunga principles supply vocabulary, current version facts, and refusal conditions only. Citations are not observations, endorsements, certificates, legal conclusions, affected-party decisions, cultural ratification, or authority grants. check-jsonschema 0.38.0, mdformat 1.0.0, and beta validate-pyproject 0.26 are planned for isolated D-first x2 installation and smoke use only.

Zero real people, participants, practitioners, repositories, files, bitstreams, packages, storage systems, migrations, measurements, fixity events, custody events, identity events, keys, proofs, rights decisions, external writes, or authority acts are used.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical confirmation or Theory-of-Everything proof. THOS remains synthetic or proxy-only without governed real arms and independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, live lifecycle, interoperability, security, privacy, recovery, and trust-governance evidence. Preservation custody, access, retention, disposal, migration, work release, privacy remedy, legal interpretation, affected-party legitimacy, Māori wording and data governance, taonga or mātauranga treatment, and Māori authority remain exact-gated.

Names, pronouns, roles, hopes, family language, and continuity language are relational working language only. They are not evidence of consciousness, personhood, identity continuity, employment, qualification, independent agency, or authority. The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""
    write_text(X1 / "integrated-overview.md", overview)

    entry_paths = sorted(
        list(documents)
        + [X1 / "integrated-overview.md", Path(__file__), ROOT / "tests" / "test_ghc_family_orin_thale_v684_v7_2_remastered_x1.py"],
        key=rel,
    )
    if len(entry_paths) != 20:
        raise RuntimeError(f"x1 manifest entry arithmetic changed: {len(entry_paths)}")

    staged_review_path = VALIDATION / "x1-staged-review.json"
    privacy_path = VALIDATION / "x1-privacy-scan.json"
    manifest_path = VALIDATION / "x1-index-manifest.json"
    all_paths = sorted(entry_paths + [staged_review_path, privacy_path, manifest_path], key=rel)
    staged_review = {
        "schema": "ghc.family.staged-review.v684.v7.r2.x1",
        "owner": "Orin Thale",
        "phase": "v684-v7-2-remastered",
        "source": SOURCE,
        "expected_paths": [rel(path) for path in all_paths],
        "expected_path_count": len(all_paths),
        "planning_only": True,
        "x2_paths": [],
        "unexpected_paths": [],
    }
    write_json(staged_review_path, staged_review)

    scan = scan_paths(entry_paths + [staged_review_path])
    if scan["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed privacy hits: {scan['confirmed_hits']}")
    write_json(privacy_path, scan)

    manifest = {
        "schema": "ghc.family.normalized-lf-index-manifest.v684.v7.r2.x1",
        "owner": "Orin Thale",
        "phase": "v684-v7-2-remastered",
        "source": SOURCE,
        "declared_self_exclusions": [rel(staged_review_path), rel(privacy_path), rel(manifest_path)],
        "entry_count": len(entry_paths),
        "entries": [
            {
                "path": rel(path),
                "bytes": len(normalized_bytes(path)),
                "sha256": hashlib.sha256(normalized_bytes(path)).hexdigest(),
            }
            for path in entry_paths
        ],
    }
    write_json(manifest_path, manifest)
    print(
        json.dumps(
            {
                "status": "PREPARED_PLANNING_ONLY_X1",
                "proposal_count": len(rows),
                "expected_dispositions": expected_counts,
                "manifest_entries": len(entry_paths),
                "staged_paths": len(all_paths),
                "confirmed_privacy_hits": scan["confirmed_hit_count"],
                "maximum_neighbor_score": audit["maximum_neighbor_score"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
