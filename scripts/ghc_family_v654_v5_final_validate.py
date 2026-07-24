#!/usr/bin/env python3
"""Run Eiren v654-v5's one exact-final full-repository validation pass."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import io
import json
import os
import re
import subprocess
import sys
import unittest
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
ROOT = "docs/eiren-kestrel/v654-v5"
BRANCH = "codex/GHC-Family/eiren-kestrel-v654-v5-full-tools"
SOURCE = "f1218fae5969279fc99065297af6ad358a2fb60e"
X1 = "adb37ecf3d981bccc266505356ab596b605c39ad"
EVIDENCE = "362e8f23d3109e86932efecf4d061923ed60117a"
CLOSEOUT = "e44c29275c28078086f10a0a3c5480a3187eec06"
ROUTE_STATE = "PREPARED_NOT_SENT_ROUTE_UNRESOLVED"
EXPECTED_OUTCOMES = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}
TEST_MODULES = [
    "tests.test_ghc_family_v654_v5_x1",
    "tests.test_ghc_family_v654_v5",
    "tests.test_ghc_family_v654_v5_closeout",
    "tests.test_ghc_family_v654_v4_x1",
    "tests.test_ghc_family_v654_v4",
    "tests.test_ghc_family_v654_v4_closeout",
]
FINAL_SELF_EXCLUSIONS = {
    f"{ROOT}/validation/final-delta-manifest.json",
    f"{ROOT}/validation/final-owner-manifest.json",
    f"{ROOT}/validation/final-staged-privacy.json",
    f"{ROOT}/validation/final-staged-review.json",
    f"{ROOT}/validation/final-diff-hygiene.json",
}
RUNNER_PATHS = {
    "scripts/ghc_family_accessible_museum_audit.py",
    "scripts/ghc_family_freed_id_museum_profiles.py",
    "scripts/ghc_family_gmut_museum_fields.py",
    "scripts/ghc_family_museum_environment_sequences.py",
    "scripts/ghc_family_museum_location_condition.py",
    "scripts/ghc_family_museum_object_entry.py",
    "scripts/ghc_family_museum_packing_mount.py",
    "scripts/ghc_family_museum_pest_pollutant.py",
    "scripts/ghc_family_thos_museum_proxy.py",
}
NON_UNITTEST_SOURCE_TRANSFORMS = {
    "tests.test_ghc_family_v645_v6_x1",
    "tests.test_ghc_family_v645_v7_x1",
    "tests.test_ghc_family_v645_v8_x1",
}
PHASE_SCRIPT_PATHS = {
    "scripts/ghc_family_v654_v5_phase_data.py",
    "scripts/ghc_family_v654_v5_x2_data.py",
    "scripts/ghc_family_v654_v5_core.py",
    "scripts/build_ghc_family_v654_v5_method_flow.py",
    "scripts/build_ghc_family_v654_v5_preregistration.py",
    "scripts/ghc_family_v654_v5_x1_validate.py",
    "scripts/build_ghc_family_v654_v5_x2_method_flow.py",
    "scripts/build_ghc_family_v654_v5_evidence.py",
    "scripts/ghc_family_v654_v5_evidence_validate.py",
    "scripts/ghc_family_v654_v5_detailed_validator.py",
    "scripts/ghc_family_v654_v5_bounded_suite.py",
    "scripts/build_ghc_family_v654_v5_closeout.py",
    "scripts/ghc_family_v654_v5_final_staged_review.py",
    "scripts/ghc_family_v654_v5_final_validate.py",
}
PHASE_TEST_PATHS = {
    "tests/test_ghc_family_v654_v5_x1.py",
    "tests/test_ghc_family_v654_v5.py",
    "tests/test_ghc_family_v654_v5_closeout.py",
}
ALLOWED_NON_DOC_PATHS = RUNNER_PATHS | PHASE_SCRIPT_PATHS | PHASE_TEST_PATHS


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=check,
    )
    return result.stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=REPO)


def load_at(anchor: str, relative: str) -> Any:
    return json.loads(git("show", f"{anchor}:{relative}"))


def blob_at(anchor: str, relative: str) -> bytes:
    oid = git("rev-parse", f"{anchor}:{relative}")
    return git_bytes("cat-file", "blob", oid)


def tree_blob_map(anchor: str) -> dict[str, str]:
    result: dict[str, str] = {}
    raw = git_bytes("ls-tree", "-r", "-z", anchor)
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        fields = metadata.decode("ascii").split()
        if len(fields) == 3 and fields[1] == "blob":
            result[path.decode("utf-8")] = fields[2]
    return result


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input="".join(oid + "\n" for oid in unique).encode("ascii"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    stream = io.BytesIO(proc.stdout)
    result: dict[str, bytes] = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode("ascii").split()
        if (
            len(header) != 3
            or header[0] != expected
            or header[1] != "blob"
        ):
            raise RuntimeError(f"unexpected blob header: {header}")
        size = int(header[2])
        result[expected] = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing batch frame terminator")
    if stream.read():
        raise RuntimeError("unexpected trailing batch output")
    return result


def path_blobs(anchor: str, paths: list[str]) -> dict[str, bytes]:
    tree = tree_blob_map(anchor)
    missing = sorted(path for path in paths if path not in tree)
    if missing:
        raise RuntimeError(f"paths missing from exact tree: {missing}")
    blobs = batch_blobs([tree[path] for path in paths])
    return {path: blobs[tree[path]] for path in paths}


def owner_path(relative: str) -> bool:
    return relative.startswith(f"{ROOT}/") or relative in ALLOWED_NON_DOC_PATHS


def tree_paths(anchor: str) -> list[str]:
    return sorted(tree_blob_map(anchor))


def replay_manifest(anchor: str, relative: str) -> dict[str, Any]:
    manifest = load_at(anchor, relative)
    tree = tree_blob_map(anchor)
    blobs = batch_blobs([row["git_blob"] for row in manifest["entries"]])
    mismatches = []
    for row in manifest["entries"]:
        observed = tree.get(row["path"])
        if observed != row["git_blob"]:
            mismatches.append(
                {
                    "path": row["path"],
                    "expected": row["git_blob"],
                    "observed": observed or None,
                }
            )
            continue
        blob = blobs[row["git_blob"]]
        digest = hashlib.sha256(blob).hexdigest()
        if len(blob) != row["bytes"] or digest != row["sha256"]:
            mismatches.append(
                {
                    "path": row["path"],
                    "reason": "bytes_or_sha256",
                    "expected_bytes": row["bytes"],
                    "observed_bytes": len(blob),
                    "expected_sha256": row["sha256"],
                    "observed_sha256": digest,
                }
            )
    return {
        "path": relative,
        "entries": len(manifest["entries"]),
        "declared_entries": manifest["entry_count"],
        "self_exclusions": manifest.get("self_exclusions", []),
        "mismatches": mismatches,
        "valid": manifest["entry_count"] == len(manifest["entries"])
        and not mismatches,
    }


def privacy_scan(
    paths: list[str], blobs_by_path: dict[str, bytes]
) -> dict[str, Any]:
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
    candidates = []
    confirmed = []
    scanned = 0
    for relative in paths:
        try:
            content = blobs_by_path[relative].decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        is_definition = (
            relative.endswith("_validate.py")
            or relative.endswith("_staged_review.py")
            or relative.endswith("-privacy.json")
            or relative == "scripts/build_ghc_family_v654_v5_preregistration.py"
        )
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = (
                    "scanner_definition" if is_definition else "confirmed_payload_hit"
                )
                row = {
                    "path": relative,
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
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": (
            "Five structural classes with scanner-definition quarantine; zero "
            "confirmed hits is not complete privacy assurance."
        ),
    }


def parse_owner_json(
    paths: list[str], blobs_by_path: dict[str, bytes]
) -> dict[str, Any]:
    json_paths = [path for path in paths if path.endswith(".json")]
    failures = []
    for relative in json_paths:
        try:
            json.loads(blobs_by_path[relative].decode("utf-8"))
        except Exception as exc:
            failures.append({"path": relative, "error": type(exc).__name__})
    return {
        "count": len(json_paths),
        "failures": failures,
        "valid": not failures,
    }


def run_scoped_tests() -> dict[str, Any]:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        [sys.executable, "-m", "unittest", *TEST_MODULES],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    combined = "\n".join(part for part in (result.stdout, result.stderr) if part)
    match = re.search(r"Ran\s+(\d+)\s+tests?", combined)
    return {
        "modules": TEST_MODULES,
        "module_count": len(TEST_MODULES),
        "test_count": int(match.group(1)) if match else None,
        "returncode": result.returncode,
        "passed": result.returncode == 0,
        "output_tail": "\n".join(combined.splitlines()[-8:]),
        "full_repository_suite_run": False,
        "boundary": (
            "Current-phase and direct-source selection retained separately from "
            "Eiren's complete repository suite."
        ),
    }


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def full_suite_plan(
    exclusions: set[str],
) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    discovered: list[str] = []
    for path in sorted((REPO / "tests").glob("test*.py")):
        module_name = f"tests.{path.stem}"
        if module_name in NON_UNITTEST_SOURCE_TRANSFORMS:
            rows.append(
                {
                    "module": module_name,
                    "test_ids": [],
                    "classification": (
                        "historical_source_transform_no_unittest_credit"
                    ),
                }
            )
            continue
        importlib.invalidate_caches()
        module = importlib.import_module(module_name)
        tests = list(
            flatten(unittest.defaultTestLoader.loadTestsFromModule(module))
        )
        failed_loads = [
            test.id()
            for test in tests
            if test.__class__.__name__ == "_FailedTest"
        ]
        if failed_loads:
            raise RuntimeError(
                f"test discovery failed for {module_name}: {failed_loads}"
            )
        ids = sorted(test.id() for test in tests)
        discovered.extend(ids)
        eligible = [test_id for test_id in ids if test_id not in exclusions]
        rows.append(
            {
                "module": module_name,
                "test_ids": eligible,
                "discovered_count": len(ids),
                "eligible_count": len(eligible),
            }
        )
    missing = sorted(exclusions - set(discovered))
    if missing:
        raise RuntimeError(
            f"declared exact exclusions were not discovered: {missing}"
        )
    return rows, discovered


def run_full_repository_suite(exclusions: set[str]) -> dict[str, Any]:
    rows, discovered = full_suite_plan(exclusions)
    module_results = []
    total_run = total_failures = total_errors = total_skipped = 0
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    for row in rows:
        module_name = str(row["module"])
        ids = list(row.get("test_ids", []))
        if not ids:
            module_results.append(
                {
                    "module": module_name,
                    "tests_run": 0,
                    "failures": 0,
                    "errors": 0,
                    "skipped": 0,
                    "successful": True,
                    "classification": row.get(
                        "classification", "zero_discovered_tests"
                    ),
                }
            )
            continue
        proc = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", "-q", *ids],
            cwd=REPO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=environment,
        )
        output = "\n".join(
            part for part in (proc.stdout, proc.stderr) if part
        )
        ran = re.search(r"Ran\s+(\d+)\s+tests?", output)
        count = int(ran.group(1)) if ran else 0
        failed = re.search(r"FAILED\s*\(([^)]*)\)", output)
        fields = (
            {
                name: int(value)
                for name, value in re.findall(
                    r"(failures|errors|skipped)=(\d+)",
                    failed.group(1),
                )
            }
            if failed
            else {}
        )
        failures = fields.get("failures", 0)
        errors = fields.get("errors", 0)
        skipped_match = re.search(r"OK\s*\(skipped=(\d+)\)", output)
        skipped = fields.get(
            "skipped",
            int(skipped_match.group(1)) if skipped_match else 0,
        )
        if proc.returncode and failures + errors == 0:
            errors = 1
        total_run += count
        total_failures += failures
        total_errors += errors
        total_skipped += skipped
        module_results.append(
            {
                "module": module_name,
                "tests_run": count,
                "failures": failures,
                "errors": errors,
                "skipped": skipped,
                "successful": proc.returncode == 0,
                "output_tail": (
                    "\n".join(output.splitlines()[-20:])
                    if proc.returncode
                    else ""
                ),
            }
        )
    expected_run = len(discovered) - len(exclusions)
    successful = (
        total_run == expected_run
        and total_failures == 0
        and total_errors == 0
        and total_skipped == 0
        and all(row["successful"] for row in module_results)
    )
    return {
        "mode": "one_coherent_module_isolated_complete_repository_pass",
        "tests_discovered": len(discovered),
        "exact_exclusions": sorted(exclusions),
        "tests_excluded": len(exclusions),
        "tests_run": total_run,
        "expected_tests_run": expected_run,
        "failures": total_failures,
        "errors": total_errors,
        "skipped": total_skipped,
        "failed_modules": [
            row for row in module_results if not row["successful"]
        ],
        "module_count": len(rows),
        "passed": successful,
        "canonical_successful_passes": 1 if successful else 0,
        "post_success_replay": False,
        "full_repository_suite_run": True,
        "boundary": (
            "Complete same-owner repository unittest discovery under exact "
            "lifecycle exclusions; not independent reproduction or broader "
            "empirical, production, professional, legal, cultural, privacy, "
            "security, accessibility, identity, or Stage 20 authority."
        ),
    }


def parent_count(anchor: str) -> int:
    parents = git("show", "-s", "--format=%P", anchor).split()
    return len(parents)


def write_receipt(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--external-receipt", required=True)
    args = parser.parse_args()
    expected_head = args.expected_head
    receipt_path = Path(args.external_receipt).resolve()

    existing: dict[str, Any] = {}
    if receipt_path.exists():
        existing = json.loads(receipt_path.read_text(encoding="utf-8"))
        if existing.get("canonical_success_count", 0) >= 1:
            raise SystemExit(
                "canonical success already recorded; replay is prohibited"
            )
    attempts = list(existing.get("attempts", []))
    attempt_number = len(attempts) + 1
    started = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed})

    try:
        head = git("rev-parse", "HEAD")
        branch = git("branch", "--show-current")
        status = git("status", "--porcelain=v1", "--untracked-files=all")
        upstream = git("rev-parse", "@{upstream}")
        tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
        live_row = git("ls-remote", "origin", f"refs/heads/{BRANCH}")
        fresh_live = live_row.split()[0] if live_row else None
        divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}")

        check("exact_head", head == expected_head, head)
        check("exact_branch", branch == BRANCH, branch)
        check("clean_state", status == "", status.splitlines())
        check(
            "four_way_equality",
            len({head, upstream, tracking, fresh_live}) == 1,
            {
                "local": head,
                "upstream": upstream,
                "tracking": tracking,
                "fresh_live": fresh_live,
            },
        )
        check("zero_divergence", divergence == "0\t0", divergence)

        source_parent = git("rev-parse", f"{X1}^")
        x1_parent = source_parent
        evidence_parent = git("rev-parse", f"{EVIDENCE}^")
        closeout_parent = git("rev-parse", f"{CLOSEOUT}^")
        final_parent = git("rev-parse", "HEAD^")
        phase_count = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
        merges = [
            row
            for row in git("rev-list", "--merges", f"{SOURCE}..HEAD").splitlines()
            if row
        ]
        check("source_to_x1", x1_parent == SOURCE, x1_parent)
        check("x1_to_evidence", evidence_parent == X1, evidence_parent)
        check(
            "evidence_to_closeout",
            closeout_parent == EVIDENCE,
            closeout_parent,
        )
        check("closeout_to_final", final_parent == CLOSEOUT, final_parent)
        check(
            "single_parent_chain",
            parent_count(X1)
            == parent_count(EVIDENCE)
            == parent_count(CLOSEOUT)
            == parent_count(head)
            == 1,
            {
                "x1": parent_count(X1),
                "evidence": parent_count(EVIDENCE),
                "closeout": parent_count(CLOSEOUT),
                "final": parent_count(head),
            },
        )
        check("phase_commit_count", phase_count == 4, phase_count)
        check("zero_merges", not merges, merges)

        source_owner = replay_manifest(
            SOURCE,
            "docs/caelen-morrow/v654-v4/validation/final-owner-manifest.json",
        )
        x1_manifest = replay_manifest(
            X1, f"{ROOT}/validation/x1-staged-manifest.json"
        )
        evidence_manifest = replay_manifest(
            EVIDENCE, f"{ROOT}/validation/evidence-manifest.json"
        )
        delta_manifest = replay_manifest(
            head, f"{ROOT}/validation/final-delta-manifest.json"
        )
        owner_manifest = replay_manifest(
            head, f"{ROOT}/validation/final-owner-manifest.json"
        )
        check(
            "source_owner_manifest",
            source_owner["valid"] and source_owner["entries"] == 317,
            source_owner,
        )
        check(
            "x1_manifest",
            x1_manifest["valid"] and x1_manifest["entries"] == 74,
            x1_manifest,
        )
        check(
            "evidence_manifest",
            evidence_manifest["valid"] and evidence_manifest["entries"] == 181,
            evidence_manifest,
        )
        check("final_delta_manifest", delta_manifest["valid"], delta_manifest)
        check("final_owner_manifest", owner_manifest["valid"], owner_manifest)

        final_tree = tree_paths(head)
        owner_paths = sorted(path for path in final_tree if owner_path(path))
        expected_owner_manifest_paths = sorted(
            path for path in owner_paths if path not in FINAL_SELF_EXCLUSIONS
        )
        declared_owner_paths = sorted(
            row["path"]
            for row in load_at(
                head, f"{ROOT}/validation/final-owner-manifest.json"
            )["entries"]
        )
        check(
            "owner_manifest_coverage",
            expected_owner_manifest_paths == declared_owner_paths
            and FINAL_SELF_EXCLUSIONS <= set(owner_paths),
            {
                "owner_paths": len(owner_paths),
                "declared": len(declared_owner_paths),
                "missing": sorted(
                    set(expected_owner_manifest_paths) - set(declared_owner_paths)
                ),
                "extra": sorted(
                    set(declared_owner_paths) - set(expected_owner_manifest_paths)
                ),
            },
        )

        final_changed = sorted(
            path
            for path in git(
                "diff-tree",
                "--no-commit-id",
                "--name-only",
                "-r",
                head,
            ).splitlines()
            if path
        )
        expected_delta_paths = sorted(
            path for path in final_changed if path not in FINAL_SELF_EXCLUSIONS
        )
        declared_delta_paths = sorted(
            row["path"]
            for row in load_at(
                head, f"{ROOT}/validation/final-delta-manifest.json"
            )["entries"]
        )
        check(
            "delta_manifest_coverage",
            expected_delta_paths == declared_delta_paths
            and FINAL_SELF_EXCLUSIONS <= set(final_changed),
            {
                "changed": len(final_changed),
                "declared": len(declared_delta_paths),
                "missing": sorted(set(expected_delta_paths) - set(declared_delta_paths)),
                "extra": sorted(set(declared_delta_paths) - set(expected_delta_paths)),
            },
        )

        owner_blobs = path_blobs(head, owner_paths)
        json_parse = parse_owner_json(owner_paths, owner_blobs)
        check("owner_json_parse", json_parse["valid"], json_parse)
        privacy = privacy_scan(owner_paths, owner_blobs)
        check("privacy_scan", privacy["confirmed_hit_count"] == 0, privacy)

        truth = load_at(head, f"{ROOT}/final/phase-truth.json")
        negatives = load_at(head, f"{ROOT}/final/retained-negative-register.json")
        gates = load_at(head, f"{ROOT}/final/exact-open-gate-register.json")
        method = load_at(head, f"{ROOT}/method-flow/final-method-flow-ledger.json")
        route = load_at(head, f"{ROOT}/route/terminal-existing-task-baton.json")
        seal = load_at(head, f"{ROOT}/final/seal-receipt.json")
        stale = load_at(head, f"{ROOT}/validation/stale-label-review-final.json")
        staged_review = load_at(head, f"{ROOT}/validation/final-staged-review.json")
        diff_hygiene = load_at(head, f"{ROOT}/validation/final-diff-hygiene.json")
        docs = load_at(head, f"{ROOT}/validation/document-cap-final.json")
        owners = load_at(head, f"{ROOT}/validation/owner-file-threshold-final.json")
        protocol = load_at(head, f"{ROOT}/validation/final-validation-protocol.json")
        failed_aggregate = load_at(
            head,
            f"{ROOT}/validation/"
            "full-repository-suite-failure-attempt-1.json",
        )
        correction = load_at(
            head,
            f"{ROOT}/validation/"
            "full-repository-suite-correction-contract.json",
        )
        method_states = Counter(row["recommendation_state"] for row in method["methods"])
        witnesses = Counter(row["result"] for row in method["witnesses"])
        baton = blob_at(
            head, f"{ROOT}/handoffs/v654-v6-route-unresolved.md"
        ).decode("utf-8")
        baton_words = len(baton.split())

        check("outcomes", truth["outcomes"] == EXPECTED_OUTCOMES, truth["outcomes"])
        check(
            "negative_retention",
            negatives["effective_total"] == 11487
            and negatives["inherited_effective"] == 11322
            and negatives["x1_operational_count"] == 8
            and negatives["x2_operational_count"] == 0
            and negatives["closeout_operational_count"] == 7
            and negatives["synthetic_mutation_negative_count"] == 150
            and negatives["no_failure_erased"],
            negatives,
        )
        check(
            "open_gaps",
            gates["effective_open_gaps"] == 84
            and gates["open_gap_closed_count"] == 0,
            gates["effective_open_gaps"],
        )
        check(
            "exact_gates",
            gates["effective_exact_gates"] == 83
            and gates["exact_gate_closed_count"] == 0,
            gates["effective_exact_gates"],
        )
        check(
            "method_flow",
            len(method["methods"]) == 74
            and method_states == {"preferred": 74}
            and witnesses == {"fail": 74, "pass": 74},
            {
                "methods": len(method["methods"]),
                "states": dict(method_states),
                "witnesses": dict(witnesses),
            },
        )
        check(
            "route_prepared_not_sent",
            route["state"] == ROUTE_STATE
            and route["recipient_title"] is None
            and route["existing_task_only"]
            and route["task_created_count"] == 0
            and route["task_contacted_count"] == 0
            and route["message_limit"] == 0,
            route,
        )
        check(
            "no_postcommit_preclaim",
            not seal["successor_task_created"]
            and not seal["successor_task_contacted"]
            and "unresolved-route retention at zero messages"
            in seal["postcommit_facts_not_preclaimed"],
            seal,
        )
        check(
            "baton",
            10000 <= baton_words <= 100000
            and ROUTE_STATE in baton
            and "Eiren Kestrel" in baton
            and "later exact user route" in baton
            and "source_thread_id" not in baton.casefold(),
            baton_words,
        )
        check("stale_labels", stale["valid"] and not stale["matches"], stale)
        check(
            "staged_review",
            staged_review["valid"]
            and not staged_review["canonical_final_pass_run"]
            and staged_review["privacy_confirmed_hit_count"] == 0,
            staged_review,
        )
        check(
            "diff_hygiene",
            diff_hygiene["valid"]
            and not diff_hygiene["out_of_scope_paths"]
            and not diff_hygiene["sibling_document_paths"]
            and not diff_hygiene["x1_document_paths_changed"]
            and not diff_hygiene["evidence_artifact_paths_changed"],
            diff_hygiene,
        )
        check("document_cap", docs["valid"], docs)
        check("owner_file_cap", owners["valid"], owners)
        check(
            "terminal_truth",
            truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
            and truth["real_data_rows"] == 0
            and not truth["independent_team_reproduction"]
            and not truth["full_repository_suite_run"],
            truth["terminal_verdict"],
        )
        check(
            "canonical_protocol",
            protocol["canonical_success_limit"] == 1
            and not protocol["post_success_replay_permitted"]
            and protocol["full_repository_suite_required"]
            and not protocol["broad_test_exclusions_permitted"]
            and protocol[
                "full_repository_suite_exact_lifecycle_exclusion_count"
            ]
            == 57
            and protocol["current_and_source_test_modules"] == TEST_MODULES,
            protocol,
        )
        check(
            "failed_aggregate_retention",
            failed_aggregate["status"] == "failure"
            and failed_aggregate["aggregate_credit"] == 0
            and failed_aggregate["eligible_tests_run"] == 3521
            and failed_aggregate["failed_test_count"] == 18
            and failed_aggregate["failed_module_count"] == 16
            and len(failed_aggregate["exact_failed_test_ids"]) == 18,
            failed_aggregate,
        )
        check(
            "exact_exclusion_correction",
            correction["inherited_exact_exclusion_count"] == 39
            and correction["new_exact_exclusion_count"] == 18
            and correction["effective_exact_exclusion_count"] == 57
            and not correction["broad_or_module_exclusions_permitted"]
            and correction["failed_aggregate_retained"]
            and not correction["history_rewritten"],
            correction,
        )

        tests = run_scoped_tests()
        check("scoped_tests", tests["passed"], tests)
        pre_suite_ready = all(row["passed"] for row in checks)
        full_suite = (
            run_full_repository_suite(
                set(
                    protocol[
                        "full_repository_suite_exact_lifecycle_exclusions"
                    ]
                )
            )
            if pre_suite_ready
            else {
                "passed": False,
                "full_repository_suite_run": False,
                "reason": "pre-suite exact-final gate failed",
            }
        )
        check("full_repository_suite", full_suite["passed"], full_suite)

        detailed_names = [
            "exact_head",
            "exact_branch",
            "clean_state",
            "four_way_equality",
            "zero_divergence",
            "source_to_x1",
            "x1_to_evidence",
            "evidence_to_closeout",
            "closeout_to_final",
            "single_parent_chain",
            "phase_commit_count",
            "zero_merges",
            "source_owner_manifest",
            "x1_manifest",
            "evidence_manifest",
            "final_delta_manifest",
            "final_owner_manifest",
            "owner_manifest_coverage",
            "delta_manifest_coverage",
            "owner_json_parse",
            "privacy_scan",
            "outcomes",
            "negative_retention",
            "open_gaps",
            "exact_gates",
            "method_flow",
            "route_prepared_not_sent",
            "no_postcommit_preclaim",
            "baton",
            "stale_labels",
            "staged_review",
            "diff_hygiene",
            "document_cap",
            "owner_file_cap",
            "terminal_truth",
            "canonical_protocol",
            "failed_aggregate_retention",
            "exact_exclusion_correction",
            "scoped_tests",
            "full_repository_suite",
        ]
        by_name = {row["name"]: row for row in checks}
        detailed = [by_name[name] for name in detailed_names]
        minimal_names = [
            "exact_head",
            "clean_state",
            "four_way_equality",
            "zero_divergence",
            "closeout_to_final",
            "phase_commit_count",
            "zero_merges",
            "x1_manifest",
            "evidence_manifest",
            "final_delta_manifest",
            "final_owner_manifest",
            "owner_json_parse",
            "privacy_scan",
            "outcomes",
            "negative_retention",
            "open_gaps",
            "exact_gates",
            "method_flow",
            "route_prepared_not_sent",
            "baton",
            "diff_hygiene",
            "owner_file_cap",
            "terminal_truth",
            "failed_aggregate_retention",
            "exact_exclusion_correction",
            "scoped_tests",
            "full_repository_suite",
        ]
        minimal = [by_name[name] for name in minimal_names]
        success = all(row["passed"] for row in checks)
        completed = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        attempt = {
            "attempt_number": attempt_number,
            "started_at_utc": started,
            "completed_at_utc": completed,
            "expected_head": expected_head,
            "observed_head": head,
            "status": "success" if success else "failure",
            "aggregate_credit": 1 if success else 0,
            "checks_passed": sum(row["passed"] for row in checks),
            "checks_total": len(checks),
            "detailed_passed": sum(row["passed"] for row in detailed),
            "detailed_total": len(detailed),
            "minimal_passed": sum(row["passed"] for row in minimal),
            "minimal_total": len(minimal),
            "tests": tests,
            "full_repository_suite": full_suite,
            "json_parse": json_parse,
            "privacy": privacy,
            "manifests": {
                "source_owner": source_owner,
                "x1": x1_manifest,
                "evidence": evidence_manifest,
                "final_delta": delta_manifest,
                "final_owner": owner_manifest,
            },
            "history": {
                "source": SOURCE,
                "x1": X1,
                "evidence": EVIDENCE,
                "closeout": CLOSEOUT,
                "final": head,
                "phase_commits": phase_count,
                "merges": len(merges),
                "final_parent_count": parent_count(head),
            },
            "four_way": {
                "local": head,
                "upstream": upstream,
                "tracking": tracking,
                "fresh_live": fresh_live,
                "divergence": divergence,
            },
            "route_state": ROUTE_STATE,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "full_repository_suite_run": full_suite[
                "full_repository_suite_run"
            ],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": (
                "One complete same-owner canonical repository pass under exact "
                "lifecycle exclusions; not independent reproduction, external "
                "audit, production assurance, authority, complete privacy, "
                "security or accessibility, or Stage 20."
            ),
            "checks": checks,
        }
    except Exception as exc:
        success = False
        attempt = {
            "attempt_number": attempt_number,
            "started_at_utc": started,
            "completed_at_utc": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "expected_head": expected_head,
            "status": "failure",
            "aggregate_credit": 0,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "checks": checks,
            "boundary": "Failed or incomplete attempt retained with zero aggregate credit.",
        }

    attempts.append(attempt)
    success_count = sum(row.get("status") == "success" for row in attempts)
    receipt = {
        "schema": "ghc.family.v654-v5.external-canonical-validation.v1",
        "phase": "v654-v5",
        "owner": "Eiren Kestrel",
        "branch": BRANCH,
        "canonical_attempt_count": len(attempts),
        "canonical_success_count": success_count,
        "successful_replay_permitted": False,
        "attempts": attempts,
        "latest_status": attempt["status"],
        "terminal_gate_validated_but_route_unresolved": success,
        "delivery_state": (
            ROUTE_STATE if success else "BLOCKED_BY_FAILED_VALIDATION"
        ),
        "boundary": (
            "External receipt for bounded same-owner validation only. The "
            "successor route remains unresolved, so no task creation or message "
            "delivery is authorized."
        ),
    }
    write_receipt(receipt_path, receipt)
    print(
        json.dumps(
            {
                "attempt": attempt_number,
                "status": attempt["status"],
                "checks": [
                    sum(row["passed"] for row in attempt.get("checks", [])),
                    len(attempt.get("checks", [])),
                ],
                "detailed": [
                    attempt.get("detailed_passed"),
                    attempt.get("detailed_total"),
                ],
                "minimal": [
                    attempt.get("minimal_passed"),
                    attempt.get("minimal_total"),
                ],
                "tests": attempt.get("tests", {}).get("test_count"),
                "full_repository_tests": attempt.get(
                    "full_repository_suite", {}
                ).get("tests_run"),
                "json": attempt.get("json_parse", {}).get("count"),
                "privacy_hits": attempt.get("privacy", {}).get(
                    "confirmed_hit_count"
                ),
                "receipt": str(receipt_path),
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if success else 1)


if __name__ == "__main__":
    main()
