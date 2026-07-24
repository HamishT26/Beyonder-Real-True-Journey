#!/usr/bin/env python3
"""Run Tamar Vey's one exact-final canonical scoped v654-v1 validation."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import io
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tamar-vey/v654-v1"
BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
SOURCE = "180a9b42330be6494e6a1ea3700e001860cffb3d"
X1 = "e5d685fb3a4a84af32fe5914eb0f8d069c854e97"
EVIDENCE = "136d55ba5af1f4f596da0c47d9be931a785cdb18"
EXPECTED = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
TEST_MODULES = [
    "tests.test_ghc_family_v654_v1_x1",
    "tests.test_ghc_family_v654_v1",
    "tests.test_ghc_family_v654_v1_closeout",
    "tests.test_ghc_family_v653_v8_core",
    "tests.test_ghc_family_v653_v8_validation",
    "tests.test_ghc_family_v653_v8_closeout",
]
RUNNERS = {
    "scripts/ghc_family_ceramic_material_ledger.py",
    "scripts/ghc_family_kiln_state_boards.py",
    "scripts/ghc_family_worker_boundary_boards.py",
    "scripts/ghc_family_food_waste_release_refusal.py",
    "scripts/ghc_family_gmut_heat_phase_fields.py",
    "scripts/ghc_family_thos_ceramics_proxy.py",
    "scripts/ghc_family_freed_id_ceramic_profiles.py",
    "scripts/ghc_family_accessible_ceramics_audit.py",
}


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=REPO, check=True, capture_output=True
    ).stdout


def git(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def owner_path(path: str) -> bool:
    return (
        path.startswith("docs/tamar-vey/v654-v1/")
        or path.startswith("scripts/ghc_family_v654_v1_")
        or path.startswith("scripts/build_ghc_family_v654_v1_")
        or path.startswith("tests/test_ghc_family_v654_v1")
        or path in RUNNERS
    )


def tree_objects(head: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in git_bytes("ls-tree", "-r", "-z", head).split(b"\0"):
        if not raw:
            continue
        metadata, path_bytes = raw.split(b"\t", 1)
        _, kind, oid = metadata.decode("ascii").split()
        if kind == "blob":
            result[path_bytes.decode("utf-8")] = oid
    return result


def batch_blobs(rows: dict[str, str]) -> dict[str, bytes]:
    ordered = list(rows.items())
    request = b"".join(f"{oid}\n".encode("ascii") for _, oid in ordered)
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    raw, _ = process.communicate(input=request, timeout=60)
    if process.returncode != 0:
        raise RuntimeError("git cat-file --batch failed")
    output: dict[str, bytes] = {}
    cursor = 0
    for path, oid in ordered:
        newline = raw.find(b"\n", cursor)
        if newline < 0:
            raise RuntimeError(f"missing cat-file header for {path}")
        header = raw[cursor:newline].decode("ascii")
        cursor = newline + 1
        parts = header.split()
        if len(parts) != 3 or parts[0] != oid or parts[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
        size = int(parts[2])
        payload = raw[cursor : cursor + size]
        cursor += size
        if len(payload) != size or raw[cursor : cursor + 1] != b"\n":
            raise RuntimeError(f"truncated blob for {path}")
        cursor += 1
        output[path] = payload
    if cursor != len(raw):
        raise RuntimeError("unexpected trailing cat-file output")
    return output


def load_blob(blobs: dict[str, bytes], path: str) -> Any:
    return json.loads(blobs[path].decode("utf-8"))


def verify_manifest(
    commit: str, path: str, expected_schema: str | None = None
) -> dict[str, Any]:
    payload = json.loads(git("show", f"{commit}:{path}"))
    if expected_schema and payload.get("schema") != expected_schema:
        return {
            "path": path,
            "entries": len(payload.get("entries", [])),
            "mismatches": ["schema"],
        }
    objects = tree_objects(commit)
    requested = {
        row["path"]: objects.get(row["path"], "")
        for row in payload.get("entries", [])
        if objects.get(row["path"])
    }
    blobs = batch_blobs(requested)
    mismatches: list[str] = []
    for row in payload.get("entries", []):
        observed_oid = objects.get(row["path"])
        if observed_oid != row["git_blob"]:
            mismatches.append(f"{row['path']}:oid")
            continue
        data = blobs[row["path"]]
        if "bytes" in row and len(data) != row["bytes"]:
            mismatches.append(f"{row['path']}:bytes")
        if "sha256" in row and hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches.append(f"{row['path']}:sha256")
    return {
        "path": path,
        "entries": len(payload.get("entries", [])),
        "self_exclusions": len(payload.get("self_exclusions", [])),
        "mismatches": mismatches,
    }


def privacy_scan(paths: list[str], blobs: dict[str, bytes]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)(source_thread_id|thread_id)\s*[:=]"
        ),
        "private_absolute_local_path": re.compile(
            r"(?i)[A-Z]:\\Users\\[^\s\"']+"
        ),
        "credential_or_secret": re.compile(
            r"(?i)(?:(?:api[_-]?key|client_secret|private_key)\s*[:=]\s*"
            r"[\"']?[A-Za-z0-9._-]{8,}|bearer\s+[A-Za-z0-9._-]{12,})"
        ),
        "private_route_or_callable": re.compile(
            r"(?i)(private_route|callable_identifier|"
            r"browser_send_submitted_response_active)"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(session_stream|raw_transcript|conversation_export)"
        ),
    }
    definitions = {
        "scripts/ghc_family_v654_v1_x1_validate.py",
        "scripts/ghc_family_v654_v1_evidence_validate.py",
        "scripts/build_ghc_family_v654_v1_preregistration.py",
        "scripts/ghc_family_v654_v1_final_staged_review.py",
        "scripts/ghc_family_v654_v1_final_validate.py",
        "docs/tamar-vey/v654-v1/validation/x1-staged-privacy.json",
        "docs/tamar-vey/v654-v1/validation/evidence-privacy.json",
        "docs/tamar-vey/v654-v1/validation/final-privacy-receipt.json",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    scanned = 0
    for path in paths:
        try:
            text = blobs[path].decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if not pattern.search(text):
                continue
            disposition = (
                "scanner_definition"
                if path in definitions
                else "confirmed_payload_hit"
            )
            row = {
                "path": path,
                "pattern_class": pattern_class,
                "disposition": disposition,
            }
            candidates.append(row)
            if disposition == "confirmed_payload_hit":
                confirmed.append(row)
    return {
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": (
            "Five structural classes with scanner-definition quarantine; "
            "zero confirmed hits is not complete privacy assurance."
        ),
    }


def run_tests_once() -> dict[str, Any]:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    import_errors: list[str] = []
    for module_name in TEST_MODULES:
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            import_errors.append(f"{module_name}:{type(exc).__name__}:{exc}")
            continue
        suite.addTests(loader.loadTestsFromModule(module))
    count = suite.countTestCases()
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    return {
        "modules": TEST_MODULES,
        "count": count,
        "passed": (
            count == 58
            and not import_errors
            and result.wasSuccessful()
            and result.testsRun == count
        ),
        "tests_run": result.testsRun,
        "failures": [
            f"{case.id()}:{message.splitlines()[-1] if message else 'failure'}"
            for case, message in result.failures
        ],
        "errors": [
            f"{case.id()}:{message.splitlines()[-1] if message else 'error'}"
            for case, message in result.errors
        ],
        "skipped": len(result.skipped),
        "import_errors": import_errors,
        "output_tail": stream.getvalue().splitlines()[-12:],
        "full_repository_suite": False,
        "successful_replay": False,
    }


def detailed_checks(blobs: dict[str, bytes]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, observed: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed})

    outcome = load_blob(blobs, "docs/tamar-vey/v654-v1/evidence/outcome-ledger.json")
    for row in outcome["rows"]:
        slug = next(
            item["slug"]
            for item in load_blob(
                blobs, "docs/tamar-vey/v654-v1/preregistration/proposal-ledger.json"
            )["proposals"]
            if item["proposal_id"] == row["proposal_id"]
        )
        prefix = f"docs/tamar-vey/v654-v1/surfaces/{slug}"
        contract = load_blob(blobs, f"{prefix}/contract.json")
        mutation = load_blob(blobs, f"{prefix}/mutation-results.json")
        receipt = load_blob(blobs, f"{prefix}/bounded-receipt.json")
        add(
            f"{row['proposal_id']}_contract",
            contract["proposal_id"] == row["proposal_id"],
            contract["proposal_id"],
        )
        add(
            f"{row['proposal_id']}_mutations",
            len(mutation["results"]) == 5
            and all(not item["accepted"] for item in mutation["results"]),
            len(mutation["results"]),
        )
        add(
            f"{row['proposal_id']}_receipt",
            receipt["acceptance_gate_passed"]
            and receipt["observed_outcome"] == row["observed_outcome"]
            and set(receipt["real_world_counters"].values()) == {0},
            receipt["observed_outcome"],
        )
    skills = load_blob(
        blobs, "docs/tamar-vey/v654-v1/skills/skill-suite-receipt.json"
    )
    runners = load_blob(
        blobs, "docs/tamar-vey/v654-v1/tools/runner-suite-receipt.json"
    )
    portfolios = load_blob(
        blobs, "docs/tamar-vey/v654-v1/evidence/portfolio-execution-ledger.json"
    )
    gaps = load_blob(
        blobs, "docs/tamar-vey/v654-v1/final/exact-open-gate-register.json"
    )
    negatives = load_blob(
        blobs, "docs/tamar-vey/v654-v1/final/retained-negative-register.json"
    )
    methods = load_blob(
        blobs, "docs/tamar-vey/v654-v1/method-flow/final-method-flow-ledger.json"
    )
    truth = load_blob(blobs, "docs/tamar-vey/v654-v1/final/phase-truth.json")
    route = load_blob(
        blobs,
        "docs/tamar-vey/v654-v1/route/future-sibling-task-delivery-state.json",
    )
    add("outcomes", outcome["counts"] == EXPECTED, outcome["counts"])
    add("mutations", outcome["mutation_rejected_total"] == 150, 150)
    add("skills", skills["skill_count"] == 10 and skills["valid"], 10)
    add("runners", runners["runner_count"] == 10 and runners["valid"], 10)
    add(
        "portfolios",
        portfolios["counts"]
        == {
            "safe_now": 30,
            "candidate": 30,
            "skills": 10,
            "runners": 10,
            "clean_fix_refine": 30,
        },
        portfolios["counts"],
    )
    add("open_gaps", gaps["effective_open_gaps"] == 78, 78)
    add("exact_gates", gaps["effective_exact_gates"] == 79, 79)
    add("negatives", negatives["effective_total"] == 10790, 10790)
    add(
        "methods",
        len(methods["methods"]) == 31
        and Counter(row["recommendation_state"] for row in methods["methods"])
        == {"preferred": 31},
        len(methods["methods"]),
    )
    add(
        "method_witnesses",
        Counter(row["result"] for row in methods["witnesses"])
        == {"fail": 31, "pass": 31},
        len(methods["witnesses"]),
    )
    add(
        "truth",
        truth["outcomes"] == EXPECTED
        and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        truth["terminal_verdict"],
    )
    add(
        "route",
        route["state"] == "PREPARED_NOT_CREATED"
        and route["task_created_count"] == 0,
        route["state"],
    )
    overview = blobs[
        "docs/tamar-vey/v654-v1/overview/v654-v1-final-integrated-overview.md"
    ].decode("utf-8")
    report = blobs[
        "docs/tamar-vey/v654-v1/reports/v654-v1-static-report.html"
    ].decode("utf-8")
    add("overview", 1500 <= len(overview.split()) <= 6000, len(overview.split()))
    add(
        "report",
        all(
            token in report
            for token in (
                "<main>",
                'scope="col"',
                'scope="row"',
                "prefers-reduced-motion",
                "@media print",
            )
        ),
        len(report),
    )
    add(
        "source_ledger",
        len(
            load_blob(
                blobs, "docs/tamar-vey/v654-v1/sources/source-ledger.json"
            )["sources"]
        )
        == 20,
        20,
    )
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt_path = Path(args.receipt).resolve()
    if str(receipt_path).casefold().startswith(str(REPO).casefold()):
        raise RuntimeError("final receipt must remain outside the repository")

    started = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    before_head = git("rev-parse", "HEAD")
    before_status = git("status", "--porcelain=v1", "--untracked-files=all")
    branch = git("branch", "--show-current")
    if before_head != args.expected_head or before_status or branch != BRANCH:
        raise RuntimeError(
            f"invalid exact-final precondition: head={before_head} "
            f"clean={not before_status} branch={branch}"
        )
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_row = git("ls-remote", "origin", f"refs/heads/{BRANCH}")
    fresh_live = live_row.split()[0] if live_row else None
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}")
    four_way = len({before_head, upstream, tracking, fresh_live}) == 1
    if not four_way or divergence != "0\t0":
        raise RuntimeError(
            f"invalid exact-final equality: {before_head} {upstream} "
            f"{tracking} {fresh_live} divergence={divergence!r}"
        )

    objects = tree_objects(before_head)
    owner_objects = {
        path: oid for path, oid in objects.items() if owner_path(path)
    }
    blobs = batch_blobs(owner_objects)
    json_failures: list[dict[str, str]] = []
    json_count = 0
    for path, payload in blobs.items():
        if not path.startswith("docs/tamar-vey/v654-v1/") or not path.endswith(
            ".json"
        ):
            continue
        json_count += 1
        try:
            json.loads(payload.decode("utf-8"))
        except Exception as exc:
            json_failures.append({"path": path, "error": type(exc).__name__})
    privacy = privacy_scan(sorted(owner_objects), blobs)

    manifests = [
        verify_manifest(
            X1,
            "docs/tamar-vey/v654-v1/validation/x1-staged-manifest.json",
        ),
        verify_manifest(
            EVIDENCE,
            "docs/tamar-vey/v654-v1/validation/evidence-manifest.json",
        ),
        verify_manifest(
            before_head,
            "docs/tamar-vey/v654-v1/validation/final-delta-manifest.json",
            "ghc.family.v654-v1.final-delta-manifest.v1",
        ),
        verify_manifest(
            before_head,
            "docs/tamar-vey/v654-v1/validation/final-owner-manifest.json",
            "ghc.family.v654-v1.final-owner-manifest.v1",
        ),
    ]
    manifest_valid = all(not row["mismatches"] for row in manifests)

    parent = git("rev-parse", "HEAD^")
    evidence_parent = git("rev-parse", f"{EVIDENCE}^")
    x1_parent = git("rev-parse", f"{X1}^")
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
    merge_rows = [
        row
        for row in git("rev-list", "--merges", f"{SOURCE}..HEAD").splitlines()
        if row
    ]
    ancestry = {
        anchor: subprocess.run(
            ["git", "merge-base", "--is-ancestor", anchor, "HEAD"],
            cwd=REPO,
        ).returncode
        == 0
        for anchor in (SOURCE, X1, EVIDENCE)
    }
    diff_hygiene = subprocess.run(
        ["git", "diff", "--check", SOURCE, "HEAD"],
        cwd=REPO,
        capture_output=True,
    )
    stale = load_blob(
        blobs, "docs/tamar-vey/v654-v1/validation/stale-label-review-final.json"
    )

    detailed = detailed_checks(blobs)
    detailed_passed = sum(row["passed"] for row in detailed)
    tests = run_tests_once()

    minimal = [
        ("outcomes", load_blob(blobs, "docs/tamar-vey/v654-v1/final/phase-truth.json")["outcomes"] == EXPECTED),
        ("negative_total", load_blob(blobs, "docs/tamar-vey/v654-v1/final/phase-truth.json")["effective_negatives"] == 10790),
        ("open_gaps", load_blob(blobs, "docs/tamar-vey/v654-v1/final/phase-truth.json")["effective_open_gaps"] == 78),
        ("exact_gates", load_blob(blobs, "docs/tamar-vey/v654-v1/final/phase-truth.json")["effective_exact_gates"] == 79),
        ("method_count", load_blob(blobs, "docs/tamar-vey/v654-v1/final/phase-truth.json")["method_flow_methods"] == 31),
        ("zero_rows", load_blob(blobs, "docs/tamar-vey/v654-v1/final/phase-truth.json")["real_data_rows"] == 0),
        ("no_full_suite", not load_blob(blobs, "docs/tamar-vey/v654-v1/final/phase-truth.json")["full_repository_suite_run"]),
        ("no_independent_reproduction", not load_blob(blobs, "docs/tamar-vey/v654-v1/final/phase-truth.json")["independent_team_reproduction"]),
        ("verdict", load_blob(blobs, "docs/tamar-vey/v654-v1/final/phase-truth.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"),
        ("task_uncreated", load_blob(blobs, "docs/tamar-vey/v654-v1/route/future-sibling-task-delivery-state.json")["task_created_count"] == 0),
        ("direct_parents", parent == EVIDENCE and evidence_parent == X1 and x1_parent == SOURCE),
        ("phase_commit_count", phase_commits == 3),
        ("zero_merges", not merge_rows),
        ("ancestry", all(ancestry.values())),
        ("json", not json_failures),
        ("privacy", privacy["confirmed_hit_count"] == 0),
        ("manifests", manifest_valid),
        ("stale_labels", stale["valid"]),
        ("diff_hygiene", diff_hygiene.returncode == 0),
        ("four_way", four_way and divergence == "0\t0"),
    ]
    minimal_rows = [
        {"name": name, "passed": bool(passed)} for name, passed in minimal
    ]
    after_head = git("rev-parse", "HEAD")
    after_status = git("status", "--porcelain=v1", "--untracked-files=all")
    exact_stable = (
        after_head == before_head == args.expected_head
        and not before_status
        and not after_status
    )
    valid = all(
        [
            tests["passed"],
            detailed_passed == len(detailed),
            all(row["passed"] for row in minimal_rows),
            not json_failures,
            privacy["confirmed_hit_count"] == 0,
            manifest_valid,
            phase_commits == 3,
            not merge_rows,
            all(ancestry.values()),
            parent == EVIDENCE,
            evidence_parent == X1,
            x1_parent == SOURCE,
            diff_hygiene.returncode == 0,
            stale["valid"],
            exact_stable,
            four_way,
            divergence == "0\t0",
        ]
    )
    receipt = {
        "schema": "ghc.family.v654-v1.external-final-validation.v1",
        "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "expected_head": args.expected_head,
        "observed_head_before": before_head,
        "observed_head_after": after_head,
        "branch": branch,
        "clean_before": not before_status,
        "clean_after": not after_status,
        "local": before_head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": fresh_live,
        "divergence": divergence,
        "four_way_equal": four_way,
        "tests": tests,
        "detailed_checks": {
            "passed": detailed_passed,
            "total": len(detailed),
            "failures": [row for row in detailed if not row["passed"]],
        },
        "minimal_checks": {
            "passed": sum(row["passed"] for row in minimal_rows),
            "total": len(minimal_rows),
            "rows": minimal_rows,
        },
        "json_parse_count": json_count,
        "json_failures": json_failures,
        "privacy": privacy,
        "manifests": manifests,
        "manifest_valid": manifest_valid,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final": before_head,
        "direct_parent": parent,
        "evidence_parent": evidence_parent,
        "x1_parent": x1_parent,
        "ancestry": ancestry,
        "phase_commit_count": phase_commits,
        "merge_count": len(merge_rows),
        "one_final_parent": len(git("show", "-s", "--format=%P", "HEAD").split()) == 1,
        "diff_hygiene": diff_hygiene.returncode == 0,
        "stale_label_review": stale["valid"],
        "exact_head_stable": exact_stable,
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren-only inherited policy",
        "canonical_scoped_pass_attempt_count": 1,
        "canonical_scoped_success_count": 1 if valid else 0,
        "post_success_replay_count": 0,
        "same_owner_only": True,
        "independent_team_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": valid,
        "boundary": (
            "One bounded same-owner canonical scoped pass under shared "
            "infrastructure; not the full repository suite, independent-team "
            "reproduction, external audit, production certification, exhaustive "
            "security, complete privacy or accessibility, professional validation, "
            "legal or cultural authority, Māori-authority review, empirical GMUT "
            "confirmation, Theory-of-Everything proof, AGI or ASI evidence, "
            "consciousness or personhood evidence, or Stage 20 authority."
        ),
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "valid": valid,
                "head": before_head,
                "tests": f"{tests['tests_run']}/{tests['count']}",
                "detailed": f"{detailed_passed}/{len(detailed)}",
                "minimal": (
                    f"{sum(row['passed'] for row in minimal_rows)}/"
                    f"{len(minimal_rows)}"
                ),
                "json": json_count,
                "privacy_files": privacy["scanned_file_count"],
                "privacy_hits": privacy["confirmed_hit_count"],
                "manifest_entries": sum(row["entries"] for row in manifests),
                "route": "ELIGIBLE_TO_CREATE_ONE_TASK" if valid else "BLOCKED",
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()
