#!/usr/bin/env python3
"""Build v472 THOS v6 x1 runtime reliability guard artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


PHASE = "v472-thos-v6-x1"
NEXT_PHASE = "v472-thos-v6-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
HOME = Path.home()
TMP_ROOT = HOME / ".codex" / ".tmp"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

APP_ADVISORIES = [
    {
        "lane": "Cicero",
        "submission_id": "019e88bb-75f5-74d1-9f34-e25c80e58bd6",
        "status": "ADVISORY_RETURNED",
        "summary": "Publish readiness metadata only; natural runtime supports scoped observation, not permanent reliability.",
    },
    {
        "lane": "Kierkegaard",
        "submission_id": "019e88bb-7621-7450-ba47-397fa2f7d8b7",
        "status": "ADVISORY_RETURNED",
        "summary": "Notifier receipts prove readiness state only; stale-temp cleanup and GMUT claims remain outside this evidence.",
    },
    {
        "lane": "Aristotle",
        "submission_id": "019e88bb-762c-7a41-a323-47069c29e6d1",
        "status": "ADVISORY_RETURNED",
        "summary": "Use final-message, notifier, stale-temp, and publication-lint schemas with expected-negative fixture rows.",
    },
]

CLI_NATURAL_LANES = [
    {"lane": "Arby", "mode": "read_only_non_ephemeral", "completion": "watched_by_notifier"},
    {"lane": "Aster Vale", "mode": "read_only_non_ephemeral", "completion": "watched_by_notifier"},
]

CREDENTIAL_PATTERNS = [
    "BEGIN " + "RSA",
    "BEGIN " + "OPENSSH",
    "api" + r"[_-]?" + "key",
    "sec" + "ret",
    "pass" + "word",
    "to" + "ken",
]
CREDENTIAL_RE = re.compile("|".join(CREDENTIAL_PATTERNS), re.IGNORECASE)
TRANSPORT_RE = re.compile(r"exec\n|succeeded in|ERROR|WARN", re.IGNORECASE)
SEMANTIC_CONTRADICTIONS = [
    (re.compile(r"\bcomplete\b", re.IGNORECASE), re.compile(r"\bblocked\b", re.IGNORECASE)),
    (re.compile(r"\bpublished\b", re.IGNORECASE), re.compile(r"\bnot\s+published\b", re.IGNORECASE)),
    (re.compile(r"\bvalidated\b", re.IGNORECASE), re.compile(r"\bgates?\s+remain\s+open\b", re.IGNORECASE)),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def aggregate(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] == "OPEN_GAP" for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def semantic_contradiction_count(text: str) -> int:
    return sum(1 for left, right in SEMANTIC_CONTRADICTIONS if left.search(text) and right.search(text))


def final_message_verdict(final_text: str, exit_code: int | None, raw_text: str = "") -> dict[str, Any]:
    errors: list[str] = []
    if not final_text.strip():
        errors.append("FINAL_MESSAGE_EMPTY_OR_MISSING")
    if exit_code not in (0, None):
        errors.append("NONZERO_EXIT_CODE")
    if final_text and TRANSPORT_RE.search(final_text):
        errors.append("FINAL_MESSAGE_CONTAINS_TRANSPORT_MARKERS")
    if CREDENTIAL_RE.search(final_text):
        errors.append("FINAL_MESSAGE_CONTAINS_CREDENTIAL_MARKER")
    contradictions = semantic_contradiction_count(final_text)
    if contradictions:
        errors.append("SEMANTIC_CONTRADICTION_CANDIDATE")
    return {
        "contradiction_count": contradictions,
        "errors": errors,
        "final_hash": sha256_text(final_text) if final_text else None,
        "final_length": len(final_text),
        "raw_hash": sha256_text(raw_text) if raw_text else None,
        "status": "PASS_FINAL_MESSAGE_SHAPE" if not errors else "FAIL_FINAL_MESSAGE_SHAPE",
    }


def expected_negative_fixtures() -> dict[str, Any]:
    fixtures = {
        "missing_final": {"final": "", "exit_code": 0, "raw": "transport completed"},
        "nonzero_exit": {"final": "Advisory text.", "exit_code": 1, "raw": "transport failed"},
        "transport_only": {"final": "exec\ncommand succeeded in 5ms", "exit_code": 0, "raw": "exec\ncommand"},
        "credential_marker": {"final": "BEGIN " + "RSA marker fixture", "exit_code": 0, "raw": ""},
        "semantic_conflict": {"final": "The phase is complete but blocked.", "exit_code": 0, "raw": ""},
    }
    entries: list[dict[str, Any]] = []
    with TemporaryDirectory(prefix="v472-v6-final-message-fixtures-") as tmp:
        root = Path(tmp)
        for name, fixture in fixtures.items():
            fixture_path = root / name / "final.txt"
            fixture_path.parent.mkdir(parents=True, exist_ok=True)
            fixture_path.write_text(fixture["final"], encoding="utf-8")
            verdict = final_message_verdict(fixture["final"], fixture["exit_code"], fixture["raw"])
            entries.append(
                {
                    "detected_errors": verdict["errors"],
                    "fixture": name,
                    "status": "EXPECTED_NEGATIVE_CAUGHT" if verdict["errors"] else "FAIL_EXPECTED_NEGATIVE_NOT_CAUGHT",
                    "tempdir_only": True,
                }
            )
    return {
        "entries": entries,
        "failure_count": sum(entry["status"] != "EXPECTED_NEGATIVE_CAUGHT" for entry in entries),
        "status": "PASS_EXPECTED_NEGATIVES"
        if all(entry["status"] == "EXPECTED_NEGATIVE_CAUGHT" for entry in entries)
        else "FAIL_EXPECTED_NEGATIVES",
    }


def inspect_stale_temp() -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    if TMP_ROOT.exists():
        for index, path in enumerate(sorted(TMP_ROOT.glob("plugins-clone-*")), start=1):
            resolved = path.resolve()
            under_root = str(resolved).lower().startswith(str(TMP_ROOT.resolve()).lower())
            stat = path.stat()
            candidates.append(
                {
                    "candidate_id": f"plugin-temp-{index}",
                    "delete_performed": False,
                    "is_dir": path.is_dir(),
                    "last_write_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
                    "path_safety": "UNDER_CODEX_TMP_ROOT" if under_root else "PATH_ESCAPE",
                    "relative_or_redacted_path": "<user-home>/.codex/.tmp/plugins-clone-*",
                    "size_bytes": None,
                }
            )
    status = "PASS_SHAPE_ONLY"
    if any(item["path_safety"] == "PATH_ESCAPE" for item in candidates):
        status = "FAIL_BLOCKER"
    elif candidates:
        status = "OPEN_GAP"
    return {
        "candidates": candidates,
        "delete_performed": False,
        "dry_run_only": True,
        "status": status,
        "visible_count": len(candidates),
    }


def publication_lint_manifest() -> dict[str, Any]:
    return {
        "forbidden_publication_classes": [
            "raw lane transport",
            "raw local temp output",
            "image captures",
            "raw conversation streams",
            "credential-bearing material",
            "external cache files",
        ],
        "required_publication_classes": [
            "curated JSON receipts",
            "curated Markdown summaries",
            "body-preserving helper scripts",
            "hashes and counts instead of raw content",
        ],
        "status": "PASS_SHAPE_ONLY",
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    fixtures = expected_negative_fixtures()
    stale_temp = inspect_stale_temp()
    publication_lint = publication_lint_manifest()
    prior_notice_path = ARTIFACT_ROOT / "v472-thos-v5-x2-cli-lane-completion-notice-v1.json"
    prior_notice = json.loads(prior_notice_path.read_text(encoding="utf-8")) if prior_notice_path.exists() else {}

    final_rows = [
        row(
            "expected_negative_fixtures",
            "PASS_SHAPE_ONLY" if fixtures["failure_count"] == 0 else "FAIL_BLOCKER",
            "Final-message guard catches missing, failed, transport-only, credential-marker, and semantic-conflict fixtures.",
            {"failure_count": fixtures["failure_count"]},
        ),
        row(
            "prior_v5_x2_notice",
            "PASS_SHAPE_ONLY" if prior_notice.get("aggregate_status") == "FINAL_MESSAGES_READY" else "OPEN_GAP",
            "Prior v5 x2 notifier receipt is available as a known-good completion marker.",
            {"status": prior_notice.get("aggregate_status")},
        ),
        row(
            "natural_duration_v6_lanes",
            "OPEN_GAP",
            "Arby and Aster Vale v6 x1 natural-duration lanes are launched and watched by notifier; final receipt may arrive asynchronously.",
            CLI_NATURAL_LANES,
        ),
    ]
    final_guard = {
        "aggregate_status": aggregate(final_rows),
        "app_advisories": APP_ADVISORIES,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "rows": final_rows,
        "fixture_results": fixtures,
    }

    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-final-message-reliability-guard-v1.json"
    write_json(path, final_guard)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-final-message-reliability-guard-v1.md",
        f"""
# v472 THOS v6 x1 Final-Message Reliability Guard

Generated UTC: `{generated_at}`

Status: `{final_guard['aggregate_status']}`

The guard catches expected-negative fixtures for missing final output, nonzero exit, transport-only output, credential-marker output, and semantic-conflict output. Arby/Aster v6 x1 natural-duration lanes are launched and watched by notifier, so their final receipt is an asynchronous carry-forward item.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-final-message-reliability-guard-v1.md")

    stale_rows = [
        row("path_safety", "FAIL_BLOCKER" if stale_temp["status"] == "FAIL_BLOCKER" else "PASS_SHAPE_ONLY", "All visible plugin-temp candidates stay under Codex temp root unless a path escape is detected."),
        row("delete_boundary", "PASS_SHAPE_ONLY", "No stale-temp deletion was performed."),
        row("visible_candidates", "OPEN_GAP" if stale_temp["visible_count"] else "PASS_SHAPE_ONLY", "Visible candidates remain inspection-only until separately classified.", {"visible_count": stale_temp["visible_count"]}),
    ]
    stale_manifest = {
        "aggregate_status": aggregate(stale_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "phase_slug": PHASE,
        "rows": stale_rows,
        "stale_temp": stale_temp,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-stale-temp-dry-run-manifest-v1.json"
    write_json(path, stale_manifest)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-stale-temp-dry-run-manifest-v1.md",
        f"""
# v472 THOS v6 x1 Stale-Temp Dry-Run Manifest

Status: `{stale_manifest['aggregate_status']}`

Visible plugin-temp candidates: `{stale_temp['visible_count']}`

This phase performs inspection only. No temp cleanup, cache purge, or external file mutation is performed.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-stale-temp-dry-run-manifest-v1.md")

    notifier_plan = {
        "aggregate_status": "OPEN_GAP_ASYNC_WATCH_ACTIVE",
        "app_advisories": APP_ADVISORIES,
        "generated_at_utc": generated_at,
        "natural_duration_lanes": CLI_NATURAL_LANES,
        "notifier_contract": [
            "watch final-message files without forcing short runtime",
            "write curated completion notices only",
            "exclude raw stdout and stderr from publication",
            "record hashes, byte counts, and marker counts",
        ],
        "phase_slug": PHASE,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-notifier-natural-duration-plan-v1.json"
    write_json(path, notifier_plan)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-notifier-natural-duration-plan-v1.md",
        """
# v472 THOS v6 x1 Notifier Natural-Duration Plan

Arby and Aster Vale may run for as long as needed within the current watcher ceiling. The notifier records final-message readiness markers when they finish, without requiring constant manual polling.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-notifier-natural-duration-plan-v1.md")

    lint_rows = [
        row("publication_classes", "PASS_SHAPE_ONLY", "Publication manifest separates curated receipts from raw transport.", publication_lint),
        row("gmUT_claim_ceiling", "PASS_SHAPE_ONLY", "THOS runtime reliability does not close GMUT gates."),
    ]
    lint_payload = {
        "aggregate_status": aggregate(lint_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "publication_lint": publication_lint,
        "rows": lint_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-publication-lint-boundary-v1.json"
    write_json(path, lint_payload)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-publication-lint-boundary-v1.md",
        """
# v472 THOS v6 x1 Publication Lint Boundary

Only curated JSON, Markdown summaries, and helper scripts belong in publication. Raw lane transport, temp output, external cache files, and credential-bearing material remain excluded.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-publication-lint-boundary-v1.md")

    status_rows = [
        row("final_guard", final_guard["aggregate_status"], "Final-message guard fixtures executed."),
        row("stale_temp", stale_manifest["aggregate_status"], "Stale-temp inspection remained dry-run."),
        row("notifier", "OPEN_GAP", "v6 x1 natural-duration notifier may complete asynchronously."),
        row("publication_lint", lint_payload["aggregate_status"], "Publication boundary manifest generated."),
    ]
    run_status = {
        "aggregate_status": aggregate(status_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": status_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(path, run_status)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md",
        f"""
# v472 THOS v6 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v6 x1 adds final-message reliability fixtures, stale-temp dry-run classification, a natural-duration notifier plan, and publication-boundary lint. Arby and Aster Vale are launched as read-only natural-duration lanes watched by notifier.

Cicero, Kierkegaard, and Aristotle returned advisory-only schema and contradiction-hunt input for v6 x1.

All six GMUT gates remain open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md")
    return written


def main() -> int:
    for path in write_artifacts():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
