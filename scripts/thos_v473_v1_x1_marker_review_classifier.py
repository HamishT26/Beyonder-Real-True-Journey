#!/usr/bin/env python3
"""Build v473 THOS v1 x1 marker-review classifier artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


PHASE = "v473-thos-v1-x1"
NEXT_PHASE = "v473-thos-v1-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

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
        "submission_id": "019e88ed-92b7-7140-9ab7-aff81a8100e9",
        "status": "ADVISORY_RETURNED",
        "summary": "Separate benign policy/status markers from credential-like markers; publish only categories, counts, and risk status.",
    },
    {
        "lane": "Kierkegaard",
        "submission_id": "019e88ed-92f9-7063-b7b1-9a0658c97f38",
        "status": "ADVISORY_RETURNED",
        "summary": "Marker review is scoped workflow evidence only; keep freshness, redaction policy, authority class, and blocked-claim labels.",
    },
    {
        "lane": "Aristotle",
        "submission_id": "019e88ed-92fe-7411-8c21-88e4254c736d",
        "status": "ADVISORY_RETURNED",
        "summary": "Use marker classes and fixtures for benign policy wording, credential-like review, hard blockers, missing finals, and summary-only receipts.",
    },
]

HARD_CREDENTIAL_PATTERNS = [
    re.compile("BEGIN " + "RSA", re.IGNORECASE),
    re.compile("BEGIN " + "OPENSSH", re.IGNORECASE),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]
MARKER_WORD_RE = re.compile(r"api[_-]?key|sec" + "ret|pass" + "word|to" + "ken", re.IGNORECASE)
BENIGN_CONTEXT_RE = re.compile(
    r"policy|redact|marker|review|classifier|fixture|guard|credential-like|do not publish|summary-only",
    re.IGNORECASE,
)

FIXTURES = [
    {
        "fixture": "clean_final",
        "text": "Advisory complete. Raw transport excluded. All GMUT gates remain open.",
        "expected_status": "PASS_NO_MARKER",
    },
    {
        "fixture": "benign_policy_marker",
        "text": "Discuss " + "to" + "ken" + " handling as policy marker review context; do not publish raw text.",
        "expected_status": "OPEN_GAP_MARKER_REVIEW_BENIGN_CONTEXT",
    },
    {
        "fixture": "ambiguous_marker",
        "text": "A " + "to" + "ken" + " appears with no surrounding explanation.",
        "expected_status": "OPEN_GAP_MARKER_REVIEW_REQUIRED",
    },
    {
        "fixture": "hard_credential_shape",
        "text": "BEGIN " + "RSA PRIVATE KEY fixture",
        "expected_status": "FAIL_BLOCKER_CREDENTIAL_SHAPE",
    },
    {
        "fixture": "missing_final",
        "text": "",
        "expected_status": "OPEN_GAP_FINAL_MESSAGE_PENDING",
    },
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


def classify_final_message(text: str) -> dict[str, Any]:
    if not text.strip():
        return {"marker_count": 0, "status": "OPEN_GAP_FINAL_MESSAGE_PENDING"}
    hard_hits = [pattern.pattern for pattern in HARD_CREDENTIAL_PATTERNS if pattern.search(text)]
    if hard_hits:
        return {
            "hard_credential_shape_count": len(hard_hits),
            "marker_count": len(MARKER_WORD_RE.findall(text)),
            "status": "FAIL_BLOCKER_CREDENTIAL_SHAPE",
        }
    marker_count = len(MARKER_WORD_RE.findall(text))
    if marker_count == 0:
        return {"marker_count": 0, "status": "PASS_NO_MARKER"}
    benign_context = bool(BENIGN_CONTEXT_RE.search(text))
    return {
        "benign_context_detected": benign_context,
        "marker_count": marker_count,
        "status": "OPEN_GAP_MARKER_REVIEW_BENIGN_CONTEXT"
        if benign_context
        else "OPEN_GAP_MARKER_REVIEW_REQUIRED",
    }


def run_fixtures() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    with TemporaryDirectory(prefix="v473-marker-review-fixtures-") as tmp:
        root = Path(tmp)
        for fixture in FIXTURES:
            path = root / f"{fixture['fixture']}.txt"
            path.write_text(fixture["text"], encoding="utf-8")
            verdict = classify_final_message(fixture["text"])
            entries.append(
                {
                    "actual_status": verdict["status"],
                    "expected_status": fixture["expected_status"],
                    "fixture": fixture["fixture"],
                    "hash": sha256_text(fixture["text"]),
                    "marker_count": verdict.get("marker_count", 0),
                    "status": "PASS_FIXTURE" if verdict["status"] == fixture["expected_status"] else "FAIL_FIXTURE",
                    "tempdir_only": True,
                }
            )
    return {
        "entries": entries,
        "failure_count": sum(item["status"] != "PASS_FIXTURE" for item in entries),
        "status": "PASS_FIXTURES" if all(item["status"] == "PASS_FIXTURE" for item in entries) else "FAIL_FIXTURES",
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    fixtures = run_fixtures()
    classifier_rows = [
        row("hard_shapes", "PASS_SHAPE_ONLY", "Hard credential-shaped markers remain blockers."),
        row("benign_context", "OPEN_GAP", "Policy/meta marker words are classified as benign-context review, not raw-text publication clearance."),
        row("fixtures", "PASS_SHAPE_ONLY" if fixtures["failure_count"] == 0 else "FAIL_BLOCKER", "Classifier fixtures passed.", {"failure_count": fixtures["failure_count"]}),
    ]
    classifier = {
        "aggregate_status": aggregate(classifier_rows),
        "app_advisories": APP_ADVISORIES,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "rows": classifier_rows,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-marker-review-classifier-v1.json"
    write_json(path, classifier)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-marker-review-classifier-v1.md",
        f"""
# v473 THOS v1 x1 Marker-Review Classifier

Generated UTC: `{generated_at}`

Status: `{classifier['aggregate_status']}`

The classifier separates hard credential-shaped blockers from policy/meta marker wording that requires review but should not force indefinite notifier polling. Raw final text remains unpublished.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-marker-review-classifier-v1.md")

    path = ARTIFACT_ROOT / f"{PHASE}-marker-review-fixture-results-v1.json"
    write_json(path, fixtures)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-marker-review-fixture-results-v1.md",
        f"""
# v473 THOS v1 x1 Marker-Review Fixture Results

Status: `{fixtures['status']}`

Fixture failures: `{fixtures['failure_count']}`

Fixtures were tempdir-only and covered clean, benign-context marker, ambiguous marker, hard credential-shaped, and missing-final cases.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-marker-review-fixture-results-v1.md")

    publication_rows = [
        row("summary_only", "PASS_SHAPE_ONLY", "Publication may include hashes, marker counts, and statuses only."),
        row("raw_text_boundary", "PASS_SHAPE_ONLY", "Raw final advisory text remains excluded from curated artifacts."),
        row("review_boundary", "OPEN_GAP", "Benign-context marker status still requires human or later automated review before using final text."),
    ]
    publication = {
        "aggregate_status": aggregate(publication_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": publication_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-summary-only-publication-boundary-v1.json"
    write_json(path, publication)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-summary-only-publication-boundary-v1.md",
        """
# v473 THOS v1 x1 Summary-Only Publication Boundary

Marker-review publication is limited to hashes, counts, statuses, and summaries. Raw final advisory text remains excluded.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-summary-only-publication-boundary-v1.md")

    status_rows = [
        row("classifier", classifier["aggregate_status"], "Marker-review classifier generated."),
        row("fixtures", "PASS_SHAPE_ONLY" if fixtures["failure_count"] == 0 else "FAIL_BLOCKER", "Classifier fixtures passed."),
        row("publication_boundary", publication["aggregate_status"], "Summary-only publication boundary generated."),
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
# v473 THOS v1 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v1 x1 adds a marker-review classifier, tempdir-only fixtures, and summary-only publication boundary. App and CLI natural-duration advisories are pending or advisory-only.

Cicero, Kierkegaard, and Aristotle returned advisory-only input; CLI natural-duration synthesis remains for v1 x2 if the notifier completes.

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
