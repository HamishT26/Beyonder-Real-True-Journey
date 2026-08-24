#!/usr/bin/env python3
"""Bounded archive/provenance helpers for Vesper Arlen v668-v1-r2.

All records are synthetic, structural, or repository-local.  Nothing in this
module is participant evidence, professional advice, legal or cultural
authority, Maori authority, independent reproduction, or Stage 20 evidence.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, BinaryIO


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v668-v1-r2"
PHASE_ROOT = ROOT / "docs" / "vesper-arlen" / PHASE
REL_PHASE_ROOT = f"docs/vesper-arlen/{PHASE}"
OWNER = "Vesper Arlen"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v668-v1-full-tools"
SOURCE_FINAL = "d3fd3065a4570046335689c62af8faf636be7a86"
SOURCE_X1 = "3e9bf7e7fa9ee1164b77616e09f93127d3b43fd5"
SOURCE_EVIDENCE = "9f1feed93e4b33c8fcb82f0cd818cac8a5594337"
INHERITED_FROZEN_PROPOSALS = 4590
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")
IDENTITY_BOUNDARY = (
    "Vesper Arlen, they/them, and the role causal-custody cartographer are "
    "relational working language only; they are not evidence of consciousness, "
    "sentience, personhood, identity continuity, employment, qualification, "
    "independent agency, or authority."
)
EVIDENCE_BOUNDARY = (
    "Owner-local synthetic and structural evidence only; not empirical, participant, "
    "professional, production, legal, cultural, Maori-authority, privacy-complete, "
    "accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, "
    "consciousness/personhood, Theory-of-Everything, or Stage 20 evidence."
)


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(payload) + b"\n")
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def read_exact(stream: BinaryIO, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError(f"git batch stream ended with {remaining} bytes outstanding")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def git_batch_blobs(oids: Iterable[str]) -> dict[str, bytes]:
    proc = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.stdin is None or proc.stdout is None:
        raise RuntimeError("git batch pipes unavailable")
    result: dict[str, bytes] = {}
    try:
        for oid in oids:
            proc.stdin.write((oid + "\n").encode("ascii"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("ascii", errors="replace").strip()
            fields = header.split()
            if len(fields) < 3 or fields[1] != "blob":
                raise ValueError(f"unexpected git batch header: {header!r}")
            payload = read_exact(proc.stdout, int(fields[2]))
            if proc.stdout.read(1) != b"\n":
                raise ValueError("missing git batch record terminator")
            result[oid] = payload
    finally:
        proc.stdin.close()
        proc.wait(timeout=30)
    if proc.returncode:
        stderr = b"" if proc.stderr is None else proc.stderr.read()
        raise RuntimeError(stderr.decode("utf-8", errors="replace"))
    return result


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.casefold()).strip()


def audit_visible_proposal_chain() -> dict[str, Any]:
    object_lines = run_git("rev-list", "--objects", "--all").stdout.splitlines()
    blob_paths: dict[str, str] = {}
    for line in object_lines:
        if " " not in line:
            continue
        oid, path = line.split(" ", 1)
        if path.endswith("proposal-freeze.json"):
            blob_paths.setdefault(oid, path)
    payloads = git_batch_blobs(sorted(blob_paths))
    records: list[dict[str, str]] = []
    parse_failures: list[dict[str, str]] = []
    for oid in sorted(payloads):
        path = blob_paths[oid]
        try:
            document = json.loads(payloads[oid].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_failures.append({"blob": oid, "source_path": path, "error_class": type(exc).__name__})
            continue
        for key in ("new_proposals", "proposals", "selected_inherited"):
            rows = document.get(key, [])
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                proposal_id = str(row.get("proposal_id") or row.get("id") or "")
                title = str(row.get("title") or row.get("proposal") or "")
                if proposal_id or title:
                    records.append(
                        {
                            "proposal_id": proposal_id,
                            "title": title,
                            "normalized_title": normalize_title(title),
                            "source_path": path,
                        }
                    )
    unique_by_id = {row["proposal_id"]: row for row in records if row["proposal_id"]}
    unique_by_title = {row["normalized_title"]: row for row in records if row["normalized_title"]}
    selectable = sorted(unique_by_id.values(), key=lambda row: (row["proposal_id"], row["normalized_title"]))
    if len(selectable) < 20:
        raise ValueError("fewer than twenty attributable inherited proposals are visible")
    selected: list[dict[str, Any]] = []
    for index in range(20):
        position = min(len(selectable) - 1, int((index + 0.5) * len(selectable) / 20))
        row = selectable[position]
        selected.append(
            {
                "selection_id": f"VA6681R2-INHERITED-{index + 1:02d}",
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "source_path": row["source_path"],
                "novelty_credit": 0,
                "completion_credit": 0,
                "disposition": "selected_for_zero_credit_refinement_review",
            }
        )
    title_digest = sha256_bytes("\n".join(sorted(unique_by_title)).encode("utf-8"))
    return {
        "declared_inherited_chain_count": INHERITED_FROZEN_PROPOSALS,
        "freeze_blob_count": len(blob_paths),
        "row_record_count": len(records),
        "unique_id_count": len(unique_by_id),
        "unique_visible_title_count": len(unique_by_title),
        "normalized_visible_title_sha256": title_digest,
        "parse_failures": parse_failures,
        "selected_inherited": selected,
        "selected_count": len(selected),
        "selected_novelty_credit": 0,
        "selected_completion_credit": 0,
        "compressed_title_gap_count_minimum": max(0, INHERITED_FROZEN_PROPOSALS - len(unique_by_id)),
        "coverage_state": "VISIBLE_ROWS_AUDITED_COMPRESSED_OLDER_TITLES_REMAIN_OPEN_GAP",
        "boundary": "A declared cumulative count is not a substitute for unavailable historical proposal titles.",
    }


PROPOSAL_BLUEPRINTS: list[tuple[str, str, str]] = [
    ("content-addressed accession envelope with duplicate payload and identifier refusal", "completed", "accession-envelope"),
    ("bitemporal custody-event DAG with correction ordering and ancestry-cycle quarantine", "completed", "custody-dag"),
    ("append-only correction tombstones with non-erasure and contested-state preservation", "completed", "correction-tombstones"),
    ("accession namespace tribunal with canonical case, confusable, and collision refusal", "completed", "namespace-tribunal"),
    ("reversible redaction view with source hash, reason code, expiry, and no destructive rewrite", "completed", "redaction-view"),
    ("rights-expression policy lattice with version pinning, conflict visibility, and no legal inference", "completed", "rights-lattice"),
    ("retention-schedule decision trace with authority vacancy and destruction stop precedence", "completed", "retention-trace"),
    ("multi-algorithm fixity quorum with mismatch localization and no authenticity overclaim", "completed", "fixity-quorum"),
    ("BagIt path and manifest tribunal with confinement, duplicate member, and payload-omission refusal", "completed", "bagit-tribunal"),
    ("preservation-action provenance graph with entity, activity, agent-role vacancy, and no competence claim", "completed", "provenance-graph"),
    ("archive packet canonical JSON tribunal with duplicate-key, numeric-domain, and Unicode preservation guards", "completed", "canonical-json"),
    ("transfer checksum handover with sender-receiver readback and mismatch quarantine", "completed", "transfer-handover"),
    ("custody-gap classifier with explicit unknown intervals and no fabricated continuity", "completed", "custody-gap"),
    ("source-note minimization profile with purpose, expiry, contestability, and blank-person fixtures", "completed", "note-minimization"),
    ("role-purpose-access matrix with least privilege, denial reason, and authority abstention", "completed", "access-matrix"),
    ("authority-claim firewall separating structural checks from legal, cultural, and professional decisions", "completed", "authority-firewall"),
    ("multilingual label fallback with language-tag validation and Maori-authority reservation", "completed", "language-fallback"),
    ("accessible provenance table with native semantics, caption, scoped headers, and print fallback", "completed", "accessible-table"),
    ("synthetic disaster-salvage triage queue with reversible priority and stop-work states", "completed", "salvage-queue"),
    ("bounded preservation-risk classifier with calibrated abstention and no real collection scoring", "completed", "risk-classifier"),
    ("quarantine-release two-reviewer proxy with separation of duties and zero real approval", "completed", "release-proxy"),
    ("issue, appeal, and contest ledger with response deadlines represented but not legally interpreted", "completed", "contest-ledger"),
    ("causal route state machine with pause, redirect, exact-title, acknowledgement, and no-resend states", "completed", "route-state"),
    ("skill-promotion collision guard with byte parity, provenance, rollback, and no overwrite", "completed", "skill-promotion"),
    ("D-isolated tool-install transaction with exact pins, script suppression, smoke, and rollback", "completed", "tool-transaction"),
    ("one-shot validation-credit machine retaining failed invocation and prohibiting success replay", "completed", "validation-credit"),
    ("auth-roster additive overlay with explicit precedence, variant isolation, and seat-cycle preservation", "completed", "auth-roster-overlay"),
    ("four-tier Freed ID flashcard graph with deterministic manifest, cross-links, and compact activation", "completed", "flashcard-graph"),
    ("THOS archival exception and shift-handover protocol on synthetic fixtures only", "represented", "thos-handover"),
    ("Freed ID zero-key preservation statement graph with expiry, correction, and revocation placeholders", "represented", "freed-id-graph"),
    ("CBR access, remedy, privacy, and contestability matrix without real rights allocation", "represented", "cbr-matrix"),
    ("GMUT information-provenance analogy board with physical and psyche nonconversion firewall", "represented", "gmut-nonconversion"),
    ("museum collections registrar accession and provenance reconciliation practice lens", "represented", "museum-practice"),
    ("public-library digital-preservation migration and retention handover practice lens", "represented", "library-practice"),
    ("archival conservator disaster-recovery custody and salvage-triage practice lens", "represented", "conservator-practice"),
    ("single successor practice recommendation for audiovisual preservation transfer review", "represented", "successor-practice"),
    ("zero-row external PREMIS interoperability adapter with conformance and real-repository evaluation vacancy", "open_gap", "premis-open-gap"),
    ("compressed historical proposal-title recovery and full-chain semantic novelty audit", "open_gap", "proposal-chain-open-gap"),
    ("public-record retention, disposal, access, privacy, cultural legitimacy, and Maori-authority docket", "exact_gate", "records-authority-gate"),
    ("Stage 20 proof, canon, deployment, AGI or ASI, consciousness, personhood, and Theory-of-Everything gate", "exact_gate", "stage20-gate"),
]


SOURCE_GROUPS = {
    "provenance": ["W3C PROV-DM", "Library of Congress PREMIS 3.0"],
    "serialization": ["RFC 8785 JSON Canonicalization Scheme", "RFC 8493 BagIt"],
    "accessibility": ["W3C WAI-ARIA APG table pattern"],
    "records": ["Archives New Zealand Information and Records Management Standard", "Te Mana Raraunga principles"],
    "toolchain": ["PyPI project metadata", "npm registry package metadata"],
}


def proposal_rows(visible_titles: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    mutation_classes = ("missing_required_field", "wrong_type", "forbidden_claim", "boundary_bypass")
    for index, (title, outcome, slug) in enumerate(PROPOSAL_BLUEPRINTS, 1):
        approval = "safe_now" if outcome == "completed" else "candidate"
        if outcome == "exact_gate":
            approval = "exact_approval"
        source_group = (
            "accessibility" if "accessible" in title else
            "serialization" if any(term in title for term in ("JSON", "BagIt", "checksum", "fixity")) else
            "toolchain" if any(term in title for term in ("skill", "tool-install", "validation")) else
            "records" if any(term in title for term in ("record", "retention", "Maori", "CBR")) else
            "provenance"
        )
        proposal_id = f"VA6681R2-N{index:03d}"
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "semantic_slug": slug,
                "hypothesis": f"A bounded owner-local {slug} control can expose declared structural failures without promoting absent evidence.",
                "null_or_failure_condition": f"The {slug} control accepts a preregistered invalid fixture, loses a retained state, or implies external authority.",
                "approval_class": approval,
                "execution_lane": "owner-local synthetic and structural x2 lane; external calls disabled unless source lookup only",
                "official_or_primary_source_needs": SOURCE_GROUPS[source_group],
                "concrete_artifacts": [f"x2/proposals/{proposal_id.casefold()}-{slug}.json", f"x2/cards/{proposal_id.casefold()}.json"],
                "falsifier_or_acceptance_gate": "All positive fixtures pass, every preregistered invalid mutation is rejected, protected claims remain false, and rollback is attributable.",
                "rollback_or_recovery": "Quarantine the owner-local artifact, retain the failed witness at zero credit, and correct only the smallest dependency.",
                "protected_gates": ["empirical", "participant", "professional", "production", "legal", "cultural", "Maori-authority", "Stage-20"],
                "expected_disposition": outcome,
                "x1_planning_only": True,
                "x2_execution_count": 0,
                "normalized_title": normalize_title(title),
                "visible_title_collision": normalize_title(title) in visible_titles,
                "negative_fixtures": [
                    {"mutation_id": f"{proposal_id}-M{offset:02d}", "mutation_class": kind, "state": "preregistered_not_executed", "credit": 0}
                    for offset, kind in enumerate(mutation_classes, 1)
                ],
            }
        )
    return rows


def portfolio_rows(prefix: str, titles: list[str], category: str, state: str = "planned_for_x2") -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"{prefix}-{index:02d}",
            "title": title,
            "category": category,
            "state": state,
            "completion_credit": 0,
            "x1_planning_only": True,
            "x2_execution_count": 0,
            "scope": "bounded owner-local synthetic or structural control; no destructive cleanup",
        }
        for index, title in enumerate(titles, 1)
    ]


def phase_owner_files() -> list[Path]:
    if not PHASE_ROOT.exists():
        return []
    return sorted(path for path in PHASE_ROOT.rglob("*") if path.is_file())


def manifest_rows(paths: Iterable[Path]) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(paths):
        relative = path.relative_to(ROOT).as_posix()
        data = path.read_bytes()
        rows.append({"path": relative, "sha256": sha256_bytes(data), "bytes": len(data)})
    return rows
