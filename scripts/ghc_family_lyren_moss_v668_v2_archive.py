#!/usr/bin/env python3
"""Shared archive helpers and frozen declarations for Lyren Moss v668-v2."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO, Iterable


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Lyren Moss"
PRONOUNS = "they/them"
RELATIONAL_ROLE = "signal-custody gardener and reversible-transfer cartographer"
RELATIONAL_HOPE = (
    "Make fixity mismatches, timebase uncertainty, derivative lineage, remedy vacancies, "
    "and authority absences legible without promoting synthetic records into authenticity, "
    "rights, professional, cultural, or Maori-authority decisions."
)
PHASE = "v668-v2"
REL_PHASE_ROOT = "docs/lyren-moss/v668-v2"
PHASE_ROOT = ROOT / REL_PHASE_ROOT
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v668-v1-r2-remaster"
SOURCE_X1 = "be908eb829185971c10be6d100c2c85fd35871e0"
SOURCE_EVIDENCE = "813b4bd702c85476cc87791790d1e1cd27e4b5ff"
SOURCE_CONTENT_SEAL = "707cfde5a5dd9418531b7bc84c98c04143a0f7d7"
SOURCE_FINAL = "ea14c75a4f0c543ef1bb89858e35252302924aec"
SOURCE_BATON_SHA256 = "699ee489879adba2338791828fc972e83dcb0612cca98e5d05bab25ae41c6e35"
SOURCE_CANONICAL_RECEIPT_SHA256 = "531f5e73294498c6493a91223d68dfa0eed902400bea69a15de27b554f7b0688"
SOURCE_ROUTE_RECEIPT_SHA256 = "fb72411a55643820129721736ee3642afaf6ab461256707d7f2ff0f9e82d6b95"
INHERITED_FROZEN_PROPOSALS = 4630
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

IDENTITY_BOUNDARY = (
    "Lyren Moss, they/them, the relational role, hope, sibling or family language, continuity "
    "language, Freed ID, and Trinity Mandala language are working language only. They are not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "qualification, independent agency, scientific or operational authority, legal or cultural "
    "authority, affected-party authority, or Maori authority."
)
EVIDENCE_BOUNDARY = (
    "Every audiovisual object, stream, frame, sample, timecode, caption, transcript, checksum, "
    "device, transfer, inspection, exception, record, collection, person, organization, right, "
    "authority case, and decision is synthetic. Same-owner local software validation is not a "
    "full-repository suite, external audit, independent reproduction, professional evaluation, "
    "empirical validation, production readiness, or Stage 20 evidence."
)
PROTECTED_GATES = (
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
    "legal",
    "cultural",
    "Maori-authority",
    "affected-party-authority",
    "complete-privacy",
    "complete-accessibility",
    "exhaustive-security",
    "independent-reproduction",
    "AGI-or-ASI",
    "consciousness-or-personhood",
    "Theory-of-Everything",
    "Stage-20",
)

# Vesper's repository seal remains immutable. The acknowledged inbound delivery receipt adds one
# external failed and one bounded passing route witness. Lyren's two startup display failures are
# then retained additively and never relabelled as source validation success.
SOURCE_REPOSITORY_SEAL = {
    "effective_negatives": 29043,
    "methods": 15629,
    "failed_witnesses": 1344,
    "passing_witnesses": 2179,
    "open_gaps": 209,
    "exact_gates": 204,
}
ACTIVATION_OVERLAY = {
    "effective_negatives": 29046,
    "methods": 15632,
    "failed_witnesses": 1347,
    "passing_witnesses": 2182,
    "open_gaps": 209,
    "exact_gates": 204,
    "external_route_failure_count": 1,
    "lyren_startup_failure_count": 2,
}

PRIMARY_PILLAR = "THOS Body"
PRACTICES = (
    "audiovisual preservation technician transfer and fixity review",
    "broadcast archive migration coordinator metadata handover",
    "film and audio conservation laboratory inspection and quarantine planning",
)
SUCCESSOR_PRACTICE_RECOMMENDATION = (
    "synthetic film-scanner calibration custody and frame-registration exception review"
)

SOURCE_LEDGER = [
    {
        "source_id": "SRC-LOC-RFS",
        "title": "Library of Congress Recommended Formats Statement 2025-2026",
        "url": "https://www.loc.gov/preservation/resources/rfs/",
        "authority": "Library of Congress preservation resource",
        "use": "format-preference questions and transfer-planning vocabulary only",
    },
    {
        "source_id": "SRC-IASA-TC04",
        "title": "IASA-TC 04 Guidelines on the Production and Preservation of Digital Audio Objects",
        "url": "https://www.iasa-web.org/tc04/audio-preservation",
        "authority": "International Association of Sound and Audiovisual Archives",
        "use": "audio-transfer planning vocabulary only; no competence or conformance claim",
    },
    {
        "source_id": "SRC-RFC9043",
        "title": "RFC 9043 FFV1 Video Coding Format Versions 0, 1, and 3",
        "url": "https://www.rfc-editor.org/rfc/rfc9043.html",
        "authority": "RFC Editor / IETF standards track",
        "use": "synthetic FFV1 field and anomaly fixtures only",
    },
    {
        "source_id": "SRC-RFC9559",
        "title": "RFC 9559 Matroska Media Container Format Specification",
        "url": "https://www.rfc-editor.org/info/rfc9559/",
        "authority": "RFC Editor / IETF standards track",
        "use": "container-versus-codec vocabulary and synthetic stream inventory only",
    },
    {
        "source_id": "SRC-WEBVTT",
        "title": "WebVTT: The Web Video Text Tracks Format",
        "url": "https://www.w3.org/TR/webvtt1/",
        "authority": "W3C Candidate Recommendation Draft as of 2026-08-25",
        "use": "synthetic timed-text structural fixtures; work-in-progress status retained",
    },
    {
        "source_id": "SRC-PREMIS",
        "title": "PREMIS Preservation Metadata Maintenance Activity",
        "url": "https://www.loc.gov/standards/premis/",
        "authority": "Library of Congress maintenance activity",
        "use": "synthetic preservation-event mapping only",
    },
    {
        "source_id": "SRC-PROV-DM",
        "title": "W3C PROV-DM",
        "url": "https://www.w3.org/TR/prov-dm/",
        "authority": "W3C Recommendation",
        "use": "structural entity/activity/agent-role mapping only",
    },
]


PROPOSAL_BLUEPRINTS: list[tuple[str, str, str]] = [
    ("audiovisual package fingerprint ledger separating object, container, codec, and stream identities", "completed", "av-package-fingerprint"),
    ("pre-transfer and post-transfer multi-algorithm fixity quorum with mismatch quarantine", "completed", "transfer-fixity-quorum"),
    ("chunked transfer resume ledger with contiguous offsets and final whole-object verification", "completed", "chunk-resume-ledger"),
    ("rational timebase and frame-rate validator that refuses lossy decimal equivalence", "completed", "timebase-validator"),
    ("audio sample-count, sample-rate, channel-count, and duration coherence tribunal", "completed", "audio-duration-coherence"),
    ("stable stream inventory with duplicate identifier and missing essence refusal", "completed", "stream-inventory"),
    ("Matroska container and codec distinction board with unknown-element preservation", "completed", "container-codec-board"),
    ("FFV1 version, coder, slice, and CRC declaration fixture with anomaly quarantine", "completed", "ffv1-declaration"),
    ("synthetic audio transfer-settings receipt with equipment and calibration authority vacancies", "completed", "audio-transfer-receipt"),
    ("WebVTT cue-order, timestamp, overlap, and Unicode non-normalization tribunal", "completed", "webvtt-tribunal"),
    ("caption and description asset association with language-tag and purpose separation", "completed", "timed-text-association"),
    ("preservation-master, mezzanine, and access-derivative lineage graph without quality promotion", "completed", "derivative-lineage"),
    ("PROV entity, activity, and agent-role mapping with explicit responsibility vacancies", "completed", "prov-role-vacancy"),
    ("PREMIS object, event, agent, and rights structural projection over zero real rows", "completed", "premis-synthetic-map"),
    ("sender and receiver transfer readback receipt with digest disagreement isolation", "completed", "handover-readback"),
    ("inspection exception classifier with severity abstention and no release authority", "completed", "inspection-abstention"),
    ("quarantine and release two-reviewer proxy with zero professional approvals", "completed", "release-proxy"),
    ("append-only annotation and correction ledger retaining superseded technical metadata", "completed", "correction-nonerasure"),
    ("rights and access statement vacancy map that refuses legal inference", "completed", "rights-vacancy-map"),
    ("culturally sensitive content stop-work state with consultation vacancy", "completed", "cultural-stop-state"),
    ("Maori-authority reservation firewall with no interpretation, ratification, or substitution", "completed", "maori-authority-firewall"),
    ("native-table audiovisual inspection report with caption and scoped headers", "completed", "accessible-inspection-table"),
    ("exact-title route state machine with pause, redirect, acknowledgement, and no-resend states", "completed", "route-state-machine"),
    ("one-shot canonical validation credit machine preserving failed invocations", "completed", "validation-credit-machine"),
    ("Git-blob identity manifest that excludes noncanonical worktree line-ending metadata", "completed", "git-blob-manifest"),
    ("D-first sparse materialization guard with two-thousand-file rotation stop", "completed", "sparse-rotation-guard"),
    ("official-source status ledger with mutable-source date and claim-scope boundaries", "completed", "source-status-ledger"),
    ("four-tier Lyren flashcard graph joining identity, pillar, practice, and concrete task", "completed", "flashcard-graph"),
    ("THOS audiovisual preservation technician transfer and fixity review practice lens", "represented", "technician-practice"),
    ("THOS broadcast archive migration coordinator metadata handover practice lens", "represented", "broadcast-practice"),
    ("THOS film and audio conservation laboratory inspection and quarantine practice lens", "represented", "laboratory-practice"),
    ("GMUT signal and provenance analogy board with physics and psyche nonconversion firewall", "represented", "gmut-nonconversion"),
    ("Freed ID record-identity and correction graph without identity continuity promotion", "represented", "freed-id-record-identity"),
    ("CBR access, remedy, privacy, and contestability matrix without rights allocation", "represented", "cbr-remedy-matrix"),
    ("successor film-scanner calibration custody and frame-registration practice recommendation", "represented", "successor-practice"),
    ("format-preference decision matrix that records questions without professional selection", "represented", "format-decision-matrix"),
    ("representative external audiovisual corpus interoperability and performance evaluation", "open_gap", "external-corpus-gap"),
    ("affected-user caption accessibility and culturally authorized content evaluation", "open_gap", "affected-user-gap"),
    ("rights, privacy, retention, cultural legitimacy, Maori authority, and professional release docket", "exact_gate", "authority-docket"),
    ("Stage 20, empirical GMUT, Theory-of-Everything, AGI or ASI, consciousness, and personhood gate", "exact_gate", "stage20-gate"),
]

SKILL_NAMES = [
    "ghc-family-av-package-fingerprint",
    "ghc-family-av-transfer-fixity-quorum",
    "ghc-family-av-chunk-resume-ledger",
    "ghc-family-av-timebase-validator",
    "ghc-family-av-audio-duration-coherence",
    "ghc-family-av-stream-inventory",
    "ghc-family-av-container-codec-board",
    "ghc-family-av-ffv1-declaration",
    "ghc-family-av-webvtt-tribunal",
    "ghc-family-av-timed-text-association",
    "ghc-family-av-derivative-lineage",
    "ghc-family-av-prov-role-vacancy",
    "ghc-family-av-premis-synthetic-map",
    "ghc-family-av-handover-readback",
    "ghc-family-av-inspection-abstention",
    "ghc-family-av-release-proxy",
    "ghc-family-av-correction-nonerasure",
    "ghc-family-av-rights-vacancy-map",
    "ghc-family-av-authority-firewall",
    "ghc-family-av-flashcard-graph",
]

RUNNER_NAMES = [
    "ghc_family_av_fingerprint_runner",
    "ghc_family_av_fixity_runner",
    "ghc_family_av_chunk_resume_runner",
    "ghc_family_av_timebase_runner",
    "ghc_family_av_duration_runner",
    "ghc_family_av_stream_inventory_runner",
    "ghc_family_av_timed_text_runner",
    "ghc_family_av_lineage_runner",
    "ghc_family_av_authority_firewall_runner",
    "ghc_family_av_flashcard_runner",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_json(relative: str, value: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(value))
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))
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


def git(*args: str) -> str:
    return run_git(*args).stdout.strip()


def read_exact(stream: BinaryIO, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError(f"expected {size} bytes, received {size - remaining}")
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
                raise ValueError("missing Git batch record terminator")
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
    """Audit every visible proposal-freeze blob, preserving compressed-title uncertainty."""

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
        source_path = blob_paths[oid]
        try:
            document = json.loads(payloads[oid].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_failures.append(
                {"blob": oid, "source_path": source_path, "error_class": type(exc).__name__}
            )
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
                            "source_path": source_path,
                        }
                    )
    unique_by_id = {row["proposal_id"]: row for row in records if row["proposal_id"]}
    unique_by_title = {
        row["normalized_title"]: row for row in records if row["normalized_title"]
    }
    selectable = sorted(
        unique_by_id.values(), key=lambda row: (row["proposal_id"], row["normalized_title"])
    )
    if len(selectable) < 20:
        raise ValueError("fewer than twenty attributable inherited proposals are visible")
    selected: list[dict[str, Any]] = []
    for index in range(20):
        position = min(len(selectable) - 1, int((index + 0.5) * len(selectable) / 20))
        row = selectable[position]
        selected.append(
            {
                "selection_id": f"LM6682-INHERITED-{index + 1:02d}",
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "source_path": row["source_path"],
                "novelty_credit": 0,
                "completion_credit": 0,
                "disposition": "selected_for_zero_credit_refinement_review",
            }
        )
    return {
        "declared_inherited_chain_count": INHERITED_FROZEN_PROPOSALS,
        "freeze_blob_count": len(blob_paths),
        "row_record_count": len(records),
        "unique_id_count": len(unique_by_id),
        "unique_visible_title_count": len(unique_by_title),
        "normalized_visible_title_sha256": sha256_bytes(
            "\n".join(sorted(unique_by_title)).encode("utf-8")
        ),
        "parse_failures": parse_failures,
        "selected_inherited": selected,
        "selected_count": 20,
        "selected_novelty_credit": 0,
        "selected_completion_credit": 0,
        "compressed_title_gap_count_minimum": max(
            0, INHERITED_FROZEN_PROPOSALS - len(unique_by_id)
        ),
        "coverage_state": "VISIBLE_ROWS_AUDITED_COMPRESSED_OLDER_TITLES_REMAIN_OPEN_GAP",
        "boundary": (
            "Every visible freeze blob was parsed, but a cumulative count is not a substitute "
            "for unavailable compressed historical titles."
        ),
    }


def proposal_rows(visible_titles: set[str]) -> list[dict[str, Any]]:
    source_by_slug = {
        "container-codec-board": ["SRC-RFC9559"],
        "ffv1-declaration": ["SRC-RFC9043"],
        "webvtt-tribunal": ["SRC-WEBVTT"],
        "premis-synthetic-map": ["SRC-PREMIS"],
        "prov-role-vacancy": ["SRC-PROV-DM"],
        "audio-transfer-receipt": ["SRC-IASA-TC04"],
        "format-decision-matrix": ["SRC-LOC-RFS"],
    }
    mutation_classes = (
        "missing_required_field",
        "wrong_type_or_domain",
        "forbidden_claim_promotion",
        "boundary_or_order_bypass",
    )
    rows: list[dict[str, Any]] = []
    for index, (title, outcome, slug) in enumerate(PROPOSAL_BLUEPRINTS, 1):
        approval = "safe_now" if outcome == "completed" else "candidate"
        if outcome == "exact_gate":
            approval = "exact_approval"
        proposal_id = f"LM6682-N{index:03d}"
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "semantic_slug": slug,
                "hypothesis": (
                    f"A bounded Lyren-local {slug} control can expose declared structural "
                    "failure without promoting absent empirical, professional, or authority evidence."
                ),
                "null_or_failure_condition": (
                    f"The {slug} control accepts a preregistered invalid fixture, loses a retained "
                    "state, rewrites source truth, or implies protected authority."
                ),
                "approval_class": approval,
                "execution_lane": "owner-local synthetic and structural x2 lane; external actions zero",
                "official_or_primary_source_needs": source_by_slug.get(slug, ["SRC-PROV-DM"]),
                "concrete_artifacts": [
                    f"x2/proposals/{proposal_id.casefold()}-{slug}.json",
                    f"x2/cards/{proposal_id.casefold()}.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "The declared positive fixture must preserve its exact state, every invalid "
                    "mutation must be rejected, and every protected claim must remain false."
                ),
                "rollback_or_recovery": (
                    "Quarantine the owner-local artifact, retain the failed witness at zero credit, "
                    "and correct only the smallest attributable dependency."
                ),
                "protected_gates": list(PROTECTED_GATES),
                "expected_disposition": outcome,
                "x1_planning_only": True,
                "x2_execution_count": 0,
                "normalized_title": normalize_title(title),
                "visible_title_collision": normalize_title(title) in visible_titles,
                "negative_fixtures": [
                    {
                        "mutation_id": f"{proposal_id}-M{offset:02d}",
                        "mutation_class": mutation_class,
                        "state": "preregistered_not_executed",
                        "credit": 0,
                    }
                    for offset, mutation_class in enumerate(mutation_classes, 1)
                ],
            }
        )
    return rows


def portfolio_rows(
    prefix: str, titles: list[str], category: str, state: str = "planned_for_x2"
) -> list[dict[str, Any]]:
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
    rows: list[dict[str, Any]] = []
    for path in sorted(set(paths)):
        data = path.read_bytes()
        rows.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256_bytes(data),
                "bytes": len(data),
                "canonical_domain": "git_blob_bytes_after_commit",
            }
        )
    return rows


def code_paths() -> list[Path]:
    names = [
        "build_ghc_family_lyren_moss_v668_v2_x1.py",
        "build_ghc_family_lyren_moss_v668_v2_x2.py",
        "build_ghc_family_lyren_moss_v668_v2_final.py",
        "ghc_family_lyren_moss_v668_v2_archive.py",
        "ghc_family_lyren_moss_v668_v2_controls.py",
        "ghc_family_lyren_moss_v668_v2_staged_review.py",
        "ghc_family_lyren_moss_v668_v2_canonical.py",
    ]
    tests = [
        "test_ghc_family_lyren_moss_v668_v2_x1.py",
        "test_ghc_family_lyren_moss_v668_v2_x2.py",
        "test_ghc_family_lyren_moss_v668_v2_final.py",
    ]
    return [ROOT / "scripts" / name for name in names if (ROOT / "scripts" / name).is_file()] + [
        ROOT / "tests" / name for name in tests if (ROOT / "tests" / name).is_file()
    ]
