#!/usr/bin/env python3
"""Run Sylven Arc v656-v3's one exact-final canonical scoped validation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v656_v3_validate as phase_validator


REPO = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/sylven-arc/v656-v3/"
PHASE = REPO / PHASE_PREFIX
BRANCH = "codex/GHC-Family/sylven-arc-v656-v3-full-tools"
SOURCE = "b18aab36fd8193fce55df3d5b7055b94354dda7e"
X1_FREEZE = "ae46f611f3b13b2ae77d0f0a13d35f13049ef75d"
EVIDENCE = "f0de53a52e9f4e99e6dda1ee6d02de8cfb4e7da6"
CURRENT_TEST_TARGETS = [
    "tests.test_ghc_family_v656_v3_x1",
    "tests.test_ghc_family_v656_v3_core",
    (
        "tests.test_ghc_family_v656_v3_validation."
        "SylvenArcV656V3EvidenceTests.test_outcomes_and_mutations"
    ),
    (
        "tests.test_ghc_family_v656_v3_validation."
        "SylvenArcV656V3EvidenceTests.test_all_surface_receipts_exist"
    ),
    (
        "tests.test_ghc_family_v656_v3_validation."
        "SylvenArcV656V3EvidenceTests.test_ten_skills_and_runners_are_valid_and_used"
    ),
    (
        "tests.test_ghc_family_v656_v3_validation."
        "SylvenArcV656V3EvidenceTests.test_all_portfolios_resolved"
    ),
    (
        "tests.test_ghc_family_v656_v3_validation."
        "SylvenArcV656V3EvidenceTests.test_retained_negatives_and_method_flow"
    ),
    (
        "tests.test_ghc_family_v656_v3_validation."
        "SylvenArcV656V3EvidenceTests.test_gaps_and_gates_remain_open"
    ),
    (
        "tests.test_ghc_family_v656_v3_validation."
        "SylvenArcV656V3EvidenceTests.test_external_action_and_promotion_counts"
    ),
    (
        "tests.test_ghc_family_v656_v3_validation."
        "SylvenArcV656V3EvidenceTests.test_overview_and_static_report"
    ),
    (
        "tests.test_ghc_family_v656_v3_validation."
        "SylvenArcV656V3EvidenceTests.test_detailed_and_minimal_validations"
    ),
    "tests.test_ghc_family_v656_v3_closeout",
]
SCANNER_PATHS = {
    "scripts/ghc_family_v656_v3_final_staged_review.py",
    "scripts/ghc_family_v656_v3_final_validate.py",
}
BOUNDARY = (
    "Bounded same-owner validation under shared infrastructure only. It is not "
    "the full repository suite, independent-team reproduction, external audit, "
    "production certification, exhaustive security, complete privacy or "
    "accessibility assurance, professional validation, legal review, cultural "
    "ratification, Māori-authority review, empirical GMUT confirmation, "
    "Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood "
    "evidence, or Stage 20 authority."
)


def environment() -> dict[str, str]:
    result = os.environ.copy()
    result.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    return result


def command(
    args: list[str],
    *,
    check: bool = True,
    text: bool = True,
) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        args,
        cwd=REPO,
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
        env=environment(),
    )


def git(*args: str) -> str:
    return command(["git", *args]).stdout.strip()


def git_bytes(*args: str) -> bytes:
    return command(["git", *args], text=False).stdout


def add(
    checks: list[dict[str, Any]], name: str, passed: bool, detail: Any
) -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def clean_state() -> dict[str, Any]:
    working = git("diff", "--name-only").splitlines()
    staged = git("diff", "--cached", "--name-only").splitlines()
    untracked = git("ls-files", "--others", "--exclude-standard").splitlines()
    return {
        "working": [row for row in working if row],
        "staged": [row for row in staged if row],
        "untracked": [row for row in untracked if row],
        "valid": not working and not staged and not untracked,
    }


def object_rows(prefix: str) -> list[tuple[str, str]]:
    raw = git_bytes("ls-tree", "-r", "-z", "HEAD", "--", prefix)
    rows: list[tuple[str, str]] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        metadata, path = item.split(b"\t", 1)
        _mode, kind, oid = metadata.decode("ascii").split()
        if kind != "blob":
            continue
        rows.append((path.decode("utf-8"), oid))
    return rows


def blob_map(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate(
        "".join(f"{oid}\n" for oid in unique).encode("ascii")
    )
    if process.returncode:
        raise RuntimeError(stderr.decode("utf-8", errors="replace"))
    result: dict[str, bytes] = {}
    offset = 0
    for requested in unique:
        line_end = stdout.index(b"\n", offset)
        header = stdout[offset:line_end].decode("ascii")
        offset = line_end + 1
        actual, kind, size_text = header.split()
        if actual != requested or kind != "blob":
            raise RuntimeError(f"unexpected batch header {header}")
        size = int(size_text)
        content = stdout[offset : offset + size]
        offset += size + 1
        result[requested] = content
    return result


def verify_manifest(relative: str) -> dict[str, Any]:
    payload = json.loads((PHASE / relative).read_text(encoding="utf-8"))
    mismatches: list[dict[str, str]] = []
    for row in payload["entries"]:
        path = row["path"]
        try:
            oid = git("rev-parse", f"HEAD:{path}")
            content = git_bytes("show", f"HEAD:{path}")
        except subprocess.CalledProcessError:
            mismatches.append(
                {"path": path, "reason": "missing_at_head"}
            )
            continue
        actual = {
            "git_blob": oid,
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        }
        for field, value in actual.items():
            if value != row[field]:
                mismatches.append(
                    {
                        "path": path,
                        "reason": field,
                        "expected": str(row[field]),
                        "actual": str(value),
                    }
                )
    return {
        "entry_count": len(payload["entries"]),
        "self_exclusion_count": len(payload.get("self_exclusions", [])),
        "mismatches": mismatches,
        "valid": not mismatches,
    }


def privacy_and_json_scan() -> dict[str, Any]:
    rows = object_rows(PHASE_PREFIX)
    content = blob_map([oid for _path, oid in rows])
    patterns = {
        "raw_uuid": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
            r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"
        ),
        "credential_or_secret": re.compile(
            r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|"
            r"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|"
            r"(?<![A-Za-z0-9])AKIA[0-9A-Z]{16}|"
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"
        ),
        "raw_thread_or_task_identifier": re.compile(
            r"\b(?:thread|task)[_-]?id\s*[:=]\s*[A-Za-z0-9_-]{12,}\b",
            re.I,
        ),
        "private_callable_or_session_stream": re.compile(
            r"\b(?:private_callable_id|session_stream|app_state)\s*[:=]",
            re.I,
        ),
    }
    hits: list[dict[str, str]] = []
    definition_only: list[dict[str, str]] = []
    json_errors: list[dict[str, str]] = []
    json_count = 0
    word_overages: list[dict[str, Any]] = []
    baton_words = 0
    for path, oid in rows:
        raw = content[oid]
        text = raw.decode("utf-8", errors="replace")
        for label, pattern in patterns.items():
            if pattern.search(text):
                row = {"path": path, "class": label}
                if path in SCANNER_PATHS:
                    definition_only.append(row)
                else:
                    hits.append(row)
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(text)
            except Exception as exc:
                json_errors.append({"path": path, "error": type(exc).__name__})
        if path.endswith((".md", ".html")):
            words = len(text.split())
            if words > 100_000:
                word_overages.append({"path": path, "words": words})
        if path.endswith("handoffs/caelen-morrow-v656-v4-activation.md"):
            baton_words = len(text.split())
    return {
        "file_count": len(rows),
        "json_count": json_count,
        "json_errors": json_errors,
        "privacy_confirmed_hits": hits,
        "privacy_definition_only_candidates": definition_only,
        "reader_document_word_overages": word_overages,
        "baton_words": baton_words,
        "valid": (
            not json_errors
            and not hits
            and not word_overages
            and 10_000 <= baton_words <= 100_000
        ),
    }


def test_result() -> dict[str, Any]:
    result = command(
        [sys.executable, "-m", "unittest", "-q", *CURRENT_TEST_TARGETS],
        check=False,
    )
    output = result.stdout + result.stderr
    match = re.search(r"Ran (\d+) tests?", output)
    return {
        "tests_run": int(match.group(1)) if match else 0,
        "failures": len(re.findall(r"^FAIL:", output, re.MULTILINE)),
        "errors": len(re.findall(r"^ERROR:", output, re.MULTILINE)),
        "exit_code": result.returncode,
        "valid": result.returncode == 0 and match is not None,
        "full_repository_suite_run": False,
        "targets": CURRENT_TEST_TARGETS,
        "output_tail": output[-2000:],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    checks: list[dict[str, Any]] = []

    # Preflight gates run before the single canonical test aggregate.
    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    clean_before = clean_state()
    add(checks, "branch", branch == BRANCH, branch)
    add(checks, "clean_before", clean_before["valid"], clean_before)
    add(checks, "head_parent_is_evidence", git("rev-parse", "HEAD^") == EVIDENCE, head)
    add(
        checks,
        "source_x1_evidence_ancestry",
        all(
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", anchor, head],
                cwd=REPO,
                capture_output=True,
            ).returncode
            == 0
            for anchor in [SOURCE, X1_FREEZE, EVIDENCE]
        ),
        {"source": SOURCE, "x1": X1_FREEZE, "evidence": EVIDENCE},
    )
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = int(git("rev-list", "--merges", "--count", f"{SOURCE}..{head}"))
    parent_counts = [
        len(git("show", "-s", "--format=%P", commit).split())
        for commit in git("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines()
    ]
    add(checks, "three_phase_commits", phase_commits == 3, phase_commits)
    add(checks, "zero_merges", merges == 0, merges)
    add(checks, "single_parent_history", parent_counts == [1, 1, 1], parent_counts)

    owner_manifest = verify_manifest("validation/final-owner-manifest.json")
    delta_manifest = verify_manifest("validation/final-staged-manifest.json")
    add(checks, "owner_manifest", owner_manifest["valid"], owner_manifest)
    add(checks, "delta_manifest", delta_manifest["valid"], delta_manifest)
    staged_review = json.loads(
        (PHASE / "validation/final-staged-review.json").read_text(encoding="utf-8")
    )
    add(checks, "staged_review", staged_review["valid"], staged_review)
    closeout_candidate = json.loads(
        (PHASE / "validation/closeout-candidate-validation.json").read_text(
            encoding="utf-8"
        )
    )
    add(checks, "closeout_candidate", closeout_candidate["valid"], closeout_candidate)

    truth = json.loads(
        (PHASE / "truth/phase-truth-final.json").read_text(encoding="utf-8")
    )
    negatives = json.loads(
        (PHASE / "truth/retained-negative-register-final.json").read_text(
            encoding="utf-8"
        )
    )
    methods = json.loads(
        (PHASE / "method-flow/method-flow-ledger-final.json").read_text(
            encoding="utf-8"
        )
    )
    roster = json.loads(
        (PHASE / "orchestration/roster-state.json").read_text(encoding="utf-8")
    )
    route = json.loads(
        (PHASE / "orchestration/auth-permission-state.json").read_text(
            encoding="utf-8"
        )
    )
    add(
        checks,
        "truth_counts",
        truth["effective_negative_count"] == 14_183
        and truth["open_gap_count"] == 99
        and truth["exact_gate_count"] == 98
        and truth["method_count"] == 470
        and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        {
            "negatives": truth["effective_negative_count"],
            "gaps": truth["open_gap_count"],
            "gates": truth["exact_gate_count"],
            "methods": truth["method_count"],
        },
    )
    add(
        checks,
        "negative_retention",
        negatives["effective_final"] == 14_183
        and negatives["final_operational_count"] == 12
        and negatives["no_failure_erased"],
        {
            "effective": negatives["effective_final"],
            "final_operational": negatives["final_operational_count"],
        },
    )
    add(
        checks,
        "method_flow_parity",
        methods["counts"]["methods"]
        == methods["counts"]["witness_results"]["fail"]
        == methods["counts"]["witness_results"]["pass"]
        == 470,
        methods["counts"],
    )
    active_names = [row["name"] for row in roster["active"]]
    add(
        checks,
        "roster",
        roster["active_count"] == 15
        and len(set(active_names)) == 15
        and roster["standby"][0]["name"] == "Tavian Sol"
        and roster["standby"][0]["state"] == "ON_STANDBY",
        {"active": active_names, "standby": roster["standby"]},
    )
    assignments = route["authorized_route"]
    add(
        checks,
        "route_arithmetic",
        len(assignments) == 160
        and assignments[2] == {"phase": "v656-v3", "seat": "Sylven Arc"}
        and assignments[3] == {"phase": "v656-v4", "seat": "Caelen Morrow"}
        and assignments[4] == {"phase": "v656-v5", "seat": "Eiren Kestrel"}
        and assignments[5] == {"phase": "v656-v6", "seat": "Elaren Kestrel"}
        and assignments[-1]["phase"] == "v675-v8",
        {
            "count": len(assignments),
            "start": assignments[:6],
            "end": assignments[-1],
        },
    )
    add(
        checks,
        "route_unsent",
        truth["route_state"] == "PREPARED_NOT_SENT_TERMINAL_GATE"
        and truth["contact_count"] == 0
        and route["authorized_next_exact_title"] == "Caelen Morrow"
        and route["authorized_next_phase"] == "v656-v4",
        {
            "state": truth["route_state"],
            "contacts": truth["contact_count"],
            "next": route["authorized_next_exact_title"],
        },
    )
    owner_scan = privacy_and_json_scan()
    add(checks, "owner_json_privacy_word_scan", owner_scan["valid"], owner_scan)

    preflight_failed = [row for row in checks if not row["passed"]]
    if preflight_failed:
        payload = {
            "schema": "ghc.family.v656-v3.final-validation-receipt.v1",
            "valid": False,
            "stage": "preflight",
            "exact_final_head": head,
            "checks": checks,
            "failed": preflight_failed,
            "canonical_test_aggregate_run": False,
            "replay_after_success": False,
            "boundary": BOUNDARY,
        }
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(json.dumps({"valid": False, "stage": "preflight", "head": head}))
        raise SystemExit(1)

    # Fresh live equality is a final prerequisite and is established immediately
    # before the single canonical aggregate.
    command(
        [
            "git",
            "fetch",
            "origin",
            f"refs/heads/{BRANCH}:refs/remotes/origin/{BRANCH}",
        ]
    )
    upstream = git("rev-parse", "@{u}")
    tracking_ref = f"refs/remotes/origin/{BRANCH}"
    tracking = git("rev-parse", tracking_ref)
    live_lines = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").splitlines()
    live = live_lines[0].split()[0] if len(live_lines) == 1 else ""
    divergence = git("rev-list", "--left-right", "--count", f"{head}...{upstream}")
    equality = {
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "divergence": divergence,
        "valid": head == upstream == tracking == live and divergence == "0\t0",
    }
    add(checks, "four_way_remote_equality", equality["valid"], equality)
    if not equality["valid"]:
        payload = {
            "schema": "ghc.family.v656-v3.final-validation-receipt.v1",
            "valid": False,
            "stage": "remote_equality",
            "exact_final_head": head,
            "checks": checks,
            "canonical_test_aggregate_run": False,
            "replay_after_success": False,
            "boundary": BOUNDARY,
        }
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(json.dumps({"valid": False, "stage": "remote_equality", "head": head}))
        raise SystemExit(1)

    tests = test_result()
    add(checks, "current_phase_scoped_tests", tests["valid"], tests)
    detailed = phase_validator.validate(
        "final", "detailed", "validation/final-owner-manifest.json"
    )
    minimal = phase_validator.validate(
        "final", "minimal", "validation/final-owner-manifest.json"
    )
    add(checks, "detailed_validation", detailed["valid"], detailed)
    add(checks, "minimal_validation", minimal["valid"], minimal)
    clean_after = clean_state()
    add(checks, "clean_after", clean_after["valid"], clean_after)
    add(checks, "exact_head_unchanged", git("rev-parse", "HEAD") == head, head)
    failed = [row for row in checks if not row["passed"]]
    payload = {
        "schema": "ghc.family.v656-v3.final-validation-receipt.v1",
        "valid": not failed,
        "stage": "complete",
        "exact_final_head": head,
        "source": SOURCE,
        "x1": X1_FREEZE,
        "evidence": EVIDENCE,
        "checks": checks,
        "failed": failed,
        "test_result": tests,
        "detailed": {
            "passed": detailed["passed_count"],
            "checks": detailed["check_count"],
            "json": detailed["json_parse_count"],
            "privacy_files": detailed["privacy_file_count"],
            "privacy_hits": len(detailed["privacy_confirmed_hits"]),
            "manifest": detailed["manifest_entry_count"],
        },
        "minimal": {
            "passed": minimal["passed_count"],
            "checks": minimal["check_count"],
            "json": minimal["json_parse_count"],
            "privacy_files": minimal["privacy_file_count"],
            "privacy_hits": len(minimal["privacy_confirmed_hits"]),
            "manifest": minimal["manifest_entry_count"],
        },
        "owner_scan": owner_scan,
        "owner_manifest": owner_manifest,
        "delta_manifest": delta_manifest,
        "remote_equality": equality,
        "canonical_test_aggregate_run": True,
        "canonical_success_credit": not failed,
        "post_success_replay": False,
        "full_repository_suite_run": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT",
        "boundary": BOUNDARY,
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "valid": payload["valid"],
                "head": head,
                "tests": tests["tests_run"],
                "detailed": detailed["passed_count"],
                "minimal": minimal["passed_count"],
                "json": owner_scan["json_count"],
                "privacy_files": owner_scan["file_count"],
                "privacy_hits": len(owner_scan["privacy_confirmed_hits"]),
                "owner_manifest": owner_manifest["entry_count"],
                "delta_manifest": delta_manifest["entry_count"],
                "phase_commits": phase_commits,
                "merges": merges,
            },
            sort_keys=True,
        )
    )
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
