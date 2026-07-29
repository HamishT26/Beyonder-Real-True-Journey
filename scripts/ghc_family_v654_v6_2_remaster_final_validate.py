#!/usr/bin/env python3
"""Run Eiren's one exact-final v654-v6 (2) remaster validation pass."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v654_v6_2_remaster_manifest as manifest
import ghc_family_v654_v6_final_validate as source_validator


REPO = Path(__file__).resolve().parents[1]
ROOT = "docs/eiren-kestrel/v654-v6-2-remaster"
BRANCH = "codex/GHC-Family/eiren-kestrel-v654-v6-2-remaster"
SOURCE = "a6987b3a572254d52721066d19bdbcd0686a8098"
X1 = "37872a3fb9593bd0a8d862164a0ccc44bb946793"
EVIDENCE = "f878615e289d8d383bc54f75c0dca4c75b16b0e4"
ROUTE_STATE = "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"
CURRENT_EXCLUSION = (
    "tests.test_ghc_family_v654_v6_2_remaster_x1."
    "TestV654V6RemasterX1.test_x1_privacy_and_no_x2_surfaces"
)
INHERITED_EXCLUSIONS = (
    "docs/tavian-sol/v654-v6/validation/"
    "inherited-full-repository-suite-exclusions.json"
)
MANIFESTS = (
    (X1, f"{ROOT}/validation/x1-file-manifest.json"),
    (EVIDENCE, f"{ROOT}/validation/evidence-staged-manifest.json"),
    ("FINAL", f"{ROOT}/validation/final-delta-manifest.json"),
    ("FINAL", f"{ROOT}/validation/final-owner-manifest.json"),
)
DEFINITION_PATHS = {
    "scripts/build_ghc_family_v654_v6_2_remaster_x1.py",
    "scripts/ghc_family_v654_v6_2_remaster_manifest.py",
    "scripts/ghc_family_v654_v6_2_remaster_final_validate.py",
    "tests/test_ghc_family_v654_v6_2_remaster_closeout.py",
}


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=check,
    )
    return result.stdout.strip()


def load_at(anchor: str, relative: str) -> Any:
    return json.loads(git("show", f"{anchor}:{relative}"))


def owner_path(relative: str) -> bool:
    return any(relative.startswith(prefix) for prefix in manifest.OWNER_PREFIXES)


def owner_blobs(anchor: str) -> tuple[list[str], dict[str, bytes]]:
    tree = source_validator.tree_blob_map(anchor)
    paths = sorted(path for path in tree if owner_path(path))
    blobs = source_validator.batch_blobs([tree[path] for path in paths])
    return paths, {path: blobs[tree[path]] for path in paths}


def replay_manifest(anchor: str, relative: str) -> dict[str, Any]:
    payload = load_at(anchor, relative)
    tree = source_validator.tree_blob_map(anchor)
    paths = [row["path"] for row in payload["entries"]]
    missing = [path for path in paths if path not in tree]
    available = [path for path in paths if path in tree]
    blobs = source_validator.batch_blobs([tree[path] for path in available])
    issues: list[dict[str, Any]] = [
        {"path": path, "issue": "missing_from_exact_tree"} for path in missing
    ]
    for row in payload["entries"]:
        path = row["path"]
        if path not in tree:
            continue
        content = blobs[tree[path]]
        digest = hashlib.sha256(content).hexdigest()
        if len(content) != row["bytes"] or digest != row["sha256"]:
            issues.append(
                {
                    "path": path,
                    "issue": "bytes_or_sha256_mismatch",
                    "expected_bytes": row["bytes"],
                    "observed_bytes": len(content),
                    "expected_sha256": row["sha256"],
                    "observed_sha256": digest,
                }
            )
    return {
        "anchor": anchor,
        "path": relative,
        "entry_count": len(payload["entries"]),
        "declared_entry_count": payload["entry_count"],
        "issues": issues,
        "valid": payload["entry_count"] == len(payload["entries"])
        and not issues
        and payload.get("valid", True),
    }


def parse_json(paths: list[str], blobs: dict[str, bytes]) -> dict[str, Any]:
    json_paths = [path for path in paths if path.endswith(".json")]
    failures = []
    for path in json_paths:
        try:
            json.loads(blobs[path].decode("utf-8"))
        except Exception as exc:  # pragma: no cover - receipt path
            failures.append({"path": path, "error": type(exc).__name__})
    return {
        "json_count": len(json_paths),
        "failures": failures,
        "valid": not failures,
    }


def privacy_scan(paths: list[str], blobs: dict[str, bytes]) -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
            rb"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]", re.I
        ),
        "credential_or_secret": re.compile(
            rb"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|"
            rb"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|"
            rb"AKIA[0-9A-Z]{16}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"
        ),
        "assigned_private_route_identifier": re.compile(
            rb"[\"'](?:task_id|thread_id|agent_id|agent_path|subagent_path|"
            rb"session_id|callable_id|resume_token)[\"']\s*:\s*"
            rb"[\"'][^\"']+[\"']",
            re.I,
        ),
        "private_application_material": re.compile(
            rb"(?:<codex_delegation>|source_thread_id|"
            rb"Screenshot\s+\d{4}-\d{2}-\d{2})",
            re.I,
        ),
    }
    candidates = []
    confirmed = []
    scanned = 0
    text_suffixes = {".py", ".json", ".md", ".txt", ".yaml", ".yml"}
    for path in paths:
        if Path(path).suffix.lower() not in text_suffixes:
            continue
        content = blobs[path]
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(content):
                row = {
                    "path": path,
                    "class": label,
                    "disposition": (
                        "scanner_definition"
                        if path in DEFINITION_PATHS
                        else "confirmed_payload_hit"
                    ),
                }
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "scanned_file_count": scanned,
        "classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "valid": not confirmed,
        "boundary": (
            "Five-class exact owner-tree scan with explicit scanner-definition "
            "quarantine; not privacy-complete assurance."
        ),
    }


def parent_count(anchor: str) -> int:
    return len(git("show", "-s", "--format=%P", anchor).split())


def write_receipt(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--external-receipt", type=Path, required=True)
    args = parser.parse_args()
    expected_head = args.expected_head
    receipt_path = args.external_receipt.resolve()

    existing: dict[str, Any] = {}
    if receipt_path.exists():
        existing = json.loads(receipt_path.read_text(encoding="utf-8"))
        if existing.get("canonical_success_count", 0) >= 1:
            raise SystemExit(
                "canonical success already recorded; post-success replay is prohibited"
            )
    attempts = list(existing.get("attempts", []))
    attempt_number = len(attempts) + 1
    checks: list[dict[str, Any]] = []
    started = utc_now()

    def check(name: str, passed: bool, observed: Any) -> None:
        checks.append(
            {"name": name, "passed": bool(passed), "observed": observed}
        )

    full_suite: dict[str, Any] = {
        "full_repository_suite_run": False,
        "passed": False,
    }
    manifest_rows: list[dict[str, Any]] = []
    json_receipt: dict[str, Any] = {}
    privacy_receipt: dict[str, Any] = {}
    error: dict[str, str] | None = None

    try:
        head = git("rev-parse", "HEAD")
        branch = git("branch", "--show-current")
        status_before = git(
            "status", "--porcelain=v1", "--untracked-files=all"
        )
        upstream = git("rev-parse", "@{upstream}")
        tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
        live_row = git("ls-remote", "origin", f"refs/heads/{BRANCH}")
        fresh_live = live_row.split()[0] if live_row else None
        divergence = git(
            "rev-list", "--left-right", "--count", "HEAD...@{upstream}"
        )

        check("exact_head", head == expected_head, head)
        check("exact_branch", branch == BRANCH, branch)
        check("clean_before", status_before == "", status_before.splitlines())
        check(
            "four_way_live_equality",
            len({head, upstream, tracking, fresh_live}) == 1,
            {
                "local": head,
                "upstream": upstream,
                "tracking": tracking,
                "fresh_live": fresh_live,
            },
        )
        check("zero_divergence", divergence == "0\t0", divergence)
        check("final_parent_is_evidence", git("rev-parse", "HEAD^") == EVIDENCE, git("rev-parse", "HEAD^"))
        check("final_one_parent", parent_count(head) == 1, parent_count(head))
        check("evidence_parent_is_x1", git("rev-parse", f"{EVIDENCE}^") == X1, git("rev-parse", f"{EVIDENCE}^"))
        check("x1_parent_is_source", git("rev-parse", f"{X1}^") == SOURCE, git("rev-parse", f"{X1}^"))
        check(
            "three_remaster_commits",
            git("rev-list", "--count", f"{SOURCE}..{head}") == "3",
            git("rev-list", "--count", f"{SOURCE}..{head}"),
        )
        merges = git("rev-list", "--min-parents=2", f"{SOURCE}..{head}")
        check("zero_merges", merges == "", merges.splitlines())
        check(
            "all_phase_commits_single_parent",
            all(parent_count(anchor) == 1 for anchor in (X1, EVIDENCE, head)),
            {anchor: parent_count(anchor) for anchor in (X1, EVIDENCE, head)},
        )

        truth = load_at(head, f"{ROOT}/truth/final-phase-truth.json")
        metadata = load_at(
            head,
            f"{ROOT}/handoffs/elaren-kestrel-v654-v7-activation-metadata.json",
        )
        baton = git(
            "show",
            f"{head}:{ROOT}/handoffs/elaren-kestrel-v654-v7-activation.md",
        )
        check(
            "final_truth",
            truth["outcomes"]
            == {
                "completed": 23,
                "represented": 5,
                "open_gap": 1,
                "exact_gate": 1,
            }
            and truth["effective_negative_count"] == 11871
            and truth["open_gap_count"] == 86
            and truth["exact_gate_count"] == 85
            and truth["method_count"] == 130
            and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
            {
                "outcomes": truth["outcomes"],
                "effective_negatives": truth["effective_negative_count"],
                "open_gaps": truth["open_gap_count"],
                "exact_gates": truth["exact_gate_count"],
                "methods": truth["method_count"],
                "verdict": truth["terminal_verdict"],
            },
        )
        check(
            "route_prepared_for_exact_existing_main_task",
            metadata["recipient"] == "Elaren Kestrel"
            and metadata["phase"] == "v654-v7"
            and metadata["endpoint_kind"] == "main_task"
            and metadata["next_recipient"] == "Neris Solane"
            and metadata["next_phase"] == "v654-v8"
            and metadata["delivery_state"] == ROUTE_STATE
            and metadata["contact_count"] == 0
            and metadata["send_cap"] == 1,
            metadata,
        )
        baton_words = len(re.findall(r"\b[\w'-]+\b", baton, re.UNICODE))
        check(
            "baton_word_and_sanitization_gate",
            10000 <= baton_words <= 100000
            and "source_" + "thread_id" not in baton.casefold()
            and not re.search(r"(?i)[A-Z]:\\Users\\", baton),
            {
                "word_count": baton_words,
                "sha256": hashlib.sha256(baton.encode("utf-8")).hexdigest(),
            },
        )

        manifest_rows = [
            replay_manifest(
                expected_head if anchor == "FINAL" else anchor,
                relative,
            )
            for anchor, relative in MANIFESTS
        ]
        check(
            "four_manifest_contracts",
            all(row["valid"] for row in manifest_rows),
            manifest_rows,
        )

        paths, blobs = owner_blobs(head)
        json_receipt = parse_json(paths, blobs)
        privacy_receipt = privacy_scan(paths, blobs)
        check(
            "owner_file_cap",
            len(paths) < 2000,
            {"owner_file_count": len(paths), "cap": 2000},
        )
        check(
            "owner_json_parse",
            json_receipt["valid"],
            {
                "json_count": json_receipt["json_count"],
                "failures": json_receipt["failures"],
            },
        )
        check(
            "owner_five_class_privacy",
            privacy_receipt["valid"],
            {
                "scanned_file_count": privacy_receipt["scanned_file_count"],
                "confirmed_hit_count": privacy_receipt["confirmed_hit_count"],
                "confirmed_hits": privacy_receipt["confirmed_hits"],
            },
        )

        inherited = load_at(head, INHERITED_EXCLUSIONS)
        exclusions = set(inherited["effective_exact_exclusions"])
        exclusions.add(CURRENT_EXCLUSION)
        check(
            "exact_lifecycle_exclusions",
            inherited["effective_exact_exclusion_count"] == 57
            and len(exclusions) == 58,
            {
                "inherited": inherited["effective_exact_exclusion_count"],
                "current": 1,
                "effective": len(exclusions),
            },
        )

        preflight_passed = all(row["passed"] for row in checks)
        if preflight_passed:
            full_suite = source_validator.run_full_repository_suite(exclusions)
            check(
                "one_complete_repository_suite",
                full_suite["passed"]
                and full_suite["canonical_successful_passes"] == 1
                and not full_suite["post_success_replay"],
                {
                    key: full_suite.get(key)
                    for key in (
                        "tests_discovered",
                        "tests_excluded",
                        "tests_run",
                        "expected_tests_run",
                        "failures",
                        "errors",
                        "skipped",
                        "module_count",
                        "passed",
                    )
                },
            )
        else:
            check(
                "one_complete_repository_suite",
                False,
                "not run because an exact preflight gate failed",
            )

        status_after = git(
            "status", "--porcelain=v1", "--untracked-files=all"
        )
        check("clean_after", status_after == "", status_after.splitlines())
    except Exception as exc:  # pragma: no cover - retained in external receipt
        error = {"type": type(exc).__name__, "message": str(exc)}
        check("validator_exception_free", False, error)

    successful = (
        error is None
        and bool(full_suite.get("passed"))
        and all(row["passed"] for row in checks)
    )
    attempt = {
        "attempt": attempt_number,
        "started_at": started,
        "finished_at": utc_now(),
        "expected_head": expected_head,
        "checks": checks,
        "manifest_replays": manifest_rows,
        "owner_json_parse": json_receipt,
        "owner_privacy_scan": privacy_receipt,
        "full_repository_suite": full_suite,
        "error": error,
        "successful": successful,
        "credited": successful,
    }
    attempts.append(attempt)
    success_count = sum(1 for row in attempts if row.get("successful"))
    receipt = {
        "schema": "ghc.family.v654-v6-2-remaster.external-final-validation.v1",
        "phase": "v654-v6-2-remaster",
        "owner": "Eiren Kestrel",
        "branch": BRANCH,
        "expected_head": expected_head,
        "attempts": attempts,
        "attempt_count": len(attempts),
        "canonical_success_count": success_count,
        "post_success_replay": False,
        "valid": success_count == 1 and successful,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": (
            "One complete same-owner repository pass under exact lifecycle "
            "exclusions and shared infrastructure. It is not independent "
            "reproduction, empirical validation, external audit, production "
            "certification, professional, legal, cultural or Maori authority, "
            "privacy-complete or accessibility-complete assurance, exhaustive "
            "security, consciousness or personhood evidence, Theory-of-"
            "Everything proof, AGI or ASI evidence, or Stage 20 authority."
        ),
    }
    write_receipt(receipt_path, receipt)
    print(
        json.dumps(
            {
                "attempt": attempt_number,
                "successful": successful,
                "canonical_success_count": success_count,
                "checks_passed": sum(row["passed"] for row in checks),
                "checks_total": len(checks),
                "tests_run": full_suite.get("tests_run", 0),
                "tests_excluded": full_suite.get("tests_excluded", 0),
                "owner_json": json_receipt.get("json_count", 0),
                "privacy_hits": privacy_receipt.get("confirmed_hit_count", 0),
                "manifest_entries": sum(
                    row.get("entry_count", 0) for row in manifest_rows
                ),
            },
            sort_keys=True,
        )
    )
    return 0 if successful else 1


if __name__ == "__main__":
    sys.exit(main())
