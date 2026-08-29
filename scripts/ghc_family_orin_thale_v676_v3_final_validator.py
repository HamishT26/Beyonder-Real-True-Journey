#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Orin v676-v3."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


BRANCH = "codex/GHC-Family/orin-thale-v676-v3-full-tools"
SOURCE = "8f1e9ebc708b5ddc23bee4e407d946fe3e322bf3"
X1 = "3ba3826fb79f836a46a577af2809a5dd6e445350"
EVIDENCE = "b5f7a4dfc6e0b9790c0569f144fbeb4649d79d93"
OWNER_PREFIXES = (
    "docs/orin-thale/v676-v3/",
    "scripts/build_ghc_family_orin_thale_v676_v3_",
    "scripts/ghc_family_orin_thale_v676_v3_",
    "tests/test_ghc_family_orin_thale_v676_v3_",
)
FINAL_SELF_EXCLUSIONS = {
    "docs/orin-thale/v676-v3/validation/final-delta-manifest.json",
    "docs/orin-thale/v676-v3/validation/final-owner-manifest.json",
    "docs/orin-thale/v676-v3/validation/final-staged-review.json",
}
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(rb"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(rb"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(rb"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(rb"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


def command(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", "-C", str(repo), *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def atomic_json(path: Path, value: object, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "x" if exclusive else "w"
    with path.open(mode, encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")


def tree_map(repo: Path, revision: str) -> dict[str, str]:
    result: dict[str, str] = {}
    value = command(repo, "ls-tree", "-r", revision)
    assert isinstance(value, str)
    for line in value.splitlines():
        left, path = line.split("\t", 1)
        mode, kind, oid = left.split()
        if kind == "blob":
            result[path] = oid
    return result


def owner_path(path: str) -> bool:
    return path.startswith(OWNER_PREFIXES)


class BlobReader:
    def __init__(self, repo: Path):
        self.proc = subprocess.Popen(
            ["git", "-C", str(repo), "cat-file", "--batch"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.cache: dict[str, bytes] = {}

    def __enter__(self) -> "BlobReader":
        return self

    def get(self, oid: str) -> bytes:
        if oid not in self.cache:
            assert self.proc.stdin and self.proc.stdout
            self.proc.stdin.write((oid + "\n").encode("ascii"))
            self.proc.stdin.flush()
            header = self.proc.stdout.readline().split()
            if len(header) < 3 or header[1] != b"blob":
                raise RuntimeError(f"object is not a blob: {oid}")
            raw = self.proc.stdout.read(int(header[2]))
            self.proc.stdout.read(1)
            self.cache[oid] = raw
        return self.cache[oid]

    def __exit__(self, exc_type, exc, traceback) -> None:
        assert self.proc.stdin
        self.proc.stdin.close()
        stderr = self.proc.stderr.read().decode("utf-8", "replace") if self.proc.stderr else ""
        code = self.proc.wait()
        if code and exc_type is None:
            raise RuntimeError(stderr)


def normalized(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def changed_owner_paths(repo: Path, start: str, end: str) -> set[str]:
    value = command(repo, "diff", "--name-only", "--diff-filter=ACMR", start, end, "--")
    assert isinstance(value, str)
    return {path for path in value.splitlines() if path and owner_path(path)}


def validate_manifest(
    repo: Path,
    revision: str,
    range_start: str,
    manifest_path: str,
    tree: dict[str, str],
    blobs: BlobReader,
) -> dict[str, Any]:
    manifest = json.loads(blobs.get(tree[manifest_path]).decode("utf-8"))
    entries = manifest["entries"]
    exclusions = {row["path"] for row in manifest["declared_exclusions"]}
    expected = changed_owner_paths(repo, range_start, revision)
    actual = {row["path"] for row in entries} | exclusions
    if actual != expected:
        raise AssertionError(
            f"manifest set mismatch {manifest_path}: missing={sorted(expected-actual)[:8]} extra={sorted(actual-expected)[:8]}"
        )
    if {row["path"] for row in entries} & exclusions:
        raise AssertionError(f"manifest entry/exclusion overlap: {manifest_path}")
    findings = []
    for row in entries:
        path = row["path"]
        oid = tree.get(path)
        if oid != row["git_blob_oid"]:
            findings.append({"path": path, "kind": "git_blob_oid"})
            continue
        raw = blobs.get(oid)
        if hashlib.sha256(normalized(raw)).hexdigest() != row["sha256_normalized_lf"]:
            findings.append({"path": path, "kind": "sha256_normalized_lf"})
    if findings:
        raise AssertionError(f"manifest blob failure {manifest_path}: {findings[:8]}")
    return {
        "revision": revision,
        "range_start": range_start,
        "path": manifest_path,
        "entries": len(entries),
        "declared_exclusions": len(exclusions),
        "set_parity": True,
        "blob_parity": True,
    }


def materialize_owner_tree(target: Path, tree: dict[str, str], blobs: BlobReader) -> int:
    count = 0
    for path, oid in tree.items():
        if not owner_path(path):
            continue
        output = target / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(blobs.get(oid))
        count += 1
    return count


def run_pytest(cwd: Path, test_path: str) -> dict[str, Any]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONUTF8"] = "1"
    args = [sys.executable, "-X", "utf8", "-m", "pytest", "-q", "-p", "no:cacheprovider", test_path]
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=600, env=env)
    output = (result.stdout + "\n" + result.stderr).strip()
    if result.returncode:
        raise AssertionError(f"pytest failed for {test_path}: {output[-5000:]}")
    match = re.search(r"(\d+) passed", output)
    if not match:
        raise AssertionError(f"pytest count unavailable for {test_path}: {output[-1000:]}")
    return {"path": test_path, "passed": int(match.group(1)), "output_tail": output[-500:]}


def direct_parent(repo: Path, child: str, parent: str) -> bool:
    value = command(repo, "rev-parse", child + "^")
    assert isinstance(value, str)
    return value == parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--latch", type=Path, required=True)
    parser.add_argument("--materialization-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    receipt = args.receipt.resolve()
    latch = args.latch.resolve()
    materialization_root = args.materialization_root.resolve()
    expected_final = args.expected_final
    if latch.exists() or receipt.exists():
        raise SystemExit("exclusive canonical latch or receipt already exists; replay refused")

    invocation = {
        "owner": "Orin Thale",
        "phase": "v676-v3",
        "expected_final": expected_final,
        "status": "INVOKED_ONCE_PENDING",
        "invocation_count": 1,
        "success_count": 0,
    }
    atomic_json(latch, invocation, exclusive=True)
    payload: dict[str, Any] = dict(invocation)
    try:
        branch = command(repo, "branch", "--show-current")
        head = command(repo, "rev-parse", "HEAD")
        clean_before = command(repo, "status", "--porcelain=v1") == ""
        upstream = command(repo, "rev-parse", "@{upstream}")
        tracking = command(repo, "rev-parse", "refs/remotes/origin/" + BRANCH)
        live_line = command(repo, "ls-remote", "--heads", "origin", "refs/heads/" + BRANCH)
        assert isinstance(live_line, str)
        live = live_line.split("\t", 1)[0]
        divergence_value = command(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}")
        assert isinstance(divergence_value, str)
        divergence = divergence_value.split()
        if branch != BRANCH or head != expected_final:
            raise AssertionError("exact branch or head mismatch")
        if not clean_before:
            raise AssertionError("lane dirty before canonical invocation")
        if not (head == upstream == tracking == live):
            raise AssertionError("pre-canonical four-way equality failed")
        if divergence != ["0", "0"]:
            raise AssertionError("pre-canonical divergence is not 0/0")

        trees = {X1: tree_map(repo, X1), EVIDENCE: tree_map(repo, EVIDENCE), head: tree_map(repo, head)}
        with BlobReader(repo) as blobs:
            manifests = [
                validate_manifest(repo, X1, SOURCE, "docs/orin-thale/v676-v3/validation/x1-manifest.json", trees[X1], blobs),
                validate_manifest(repo, EVIDENCE, X1, "docs/orin-thale/v676-v3/validation/evidence-manifest.json", trees[EVIDENCE], blobs),
                validate_manifest(repo, head, EVIDENCE, "docs/orin-thale/v676-v3/validation/final-delta-manifest.json", trees[head], blobs),
                validate_manifest(repo, head, SOURCE, "docs/orin-thale/v676-v3/validation/final-owner-manifest.json", trees[head], blobs),
            ]

            materialization_root.mkdir(parents=True, exist_ok=True)
            materialized_root = materialization_root / ("or6763-" + expected_final[:16])
            materialized_root.mkdir(parents=False, exist_ok=False)
            x1_dir = materialized_root / "x1"
            evidence_dir = materialized_root / "evidence"
            materialized = {
                "x1": materialize_owner_tree(x1_dir, trees[X1], blobs),
                "evidence": materialize_owner_tree(evidence_dir, trees[EVIDENCE], blobs),
            }
            tests = [
                run_pytest(x1_dir, "tests/test_ghc_family_orin_thale_v676_v3_x1.py"),
                run_pytest(evidence_dir, "tests/test_ghc_family_orin_thale_v676_v3_x2.py"),
                run_pytest(repo, "tests/test_ghc_family_orin_thale_v676_v3_final.py"),
            ]

            final_tree = trees[head]
            owner_paths = sorted(path for path in final_tree if owner_path(path))
            json_count = 0
            document_count = 0
            python_count = 0
            max_document_words = 0
            security_findings = []
            privacy_candidates = []
            outcome_values = []
            for path in owner_paths:
                raw = blobs.get(final_tree[path])
                if path.endswith(".json"):
                    value = json.loads(raw.decode("utf-8"))
                    json_count += 1
                    stack = [value]
                    while stack:
                        node = stack.pop()
                        if isinstance(node, dict):
                            for key in ("outcome", "expected_disposition"):
                                if key in node and isinstance(node[key], str):
                                    outcome_values.append((path, key, node[key]))
                            stack.extend(node.values())
                        elif isinstance(node, list):
                            stack.extend(node)
                if path.endswith((".md", ".html")):
                    document_count += 1
                    words = len(raw.decode("utf-8").split())
                    max_document_words = max(max_document_words, words)
                    if words > 100_000:
                        raise AssertionError(f"document word ceiling exceeded: {path}")
                if path.endswith(".py"):
                    python_count += 1
                    parsed = ast.parse(raw.decode("utf-8"), filename=path)
                    for node in ast.walk(parsed):
                        if isinstance(node, (ast.Import, ast.ImportFrom)):
                            names = [alias.name for alias in node.names]
                            if any(name in {"requests", "urllib.request", "socket"} for name in names):
                                security_findings.append({"path": path, "kind": "network_import"})
                        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                            security_findings.append({"path": path, "kind": node.func.id})
                if path not in FINAL_SELF_EXCLUSIONS and path.endswith((".json", ".md", ".html", ".py", ".txt")):
                    for name, pattern in PRIVACY_PATTERNS.items():
                        if pattern.search(raw):
                            privacy_candidates.append({"class": name, "path": path})
            unknown_outcomes = [row for row in outcome_values if row[2] not in ALLOWED_OUTCOMES]
            if unknown_outcomes:
                raise AssertionError(f"unknown outcome labels: {unknown_outcomes[:8]}")
            if security_findings:
                raise AssertionError(f"bounded owner-code security findings: {security_findings}")
            review_path = "docs/orin-thale/v676-v3/validation/final-staged-review.json"
            review = json.loads(blobs.get(final_tree[review_path]).decode("utf-8"))
            if review["privacy_candidate_count"] != len(privacy_candidates):
                raise AssertionError(
                    f"privacy candidate count mismatch: staged={review['privacy_candidate_count']} final={len(privacy_candidates)}"
                )
            if review["confirmed_five_class_privacy_or_raw_identifier_hits"] != 0:
                raise AssertionError("confirmed privacy hit in final staged review")

            seal_path = "docs/orin-thale/v676-v3/closeout/content-seal.json"
            content_seal = json.loads(blobs.get(final_tree[seal_path]).decode("utf-8"))
            for row in content_seal["entries"]:
                raw = blobs.get(final_tree[row["path"]])
                if hashlib.sha256(normalized(raw)).hexdigest() != row["sha256_normalized_lf"]:
                    raise AssertionError(f"content seal mismatch: {row['path']}")

            phase_truth = json.loads(blobs.get(final_tree["docs/orin-thale/v676-v3/final/phase-truth.json"]).decode("utf-8"))
            method_flow = json.loads(blobs.get(final_tree["docs/orin-thale/v676-v3/final/method-flow-ledger.json"]).decode("utf-8"))
            route = json.loads(blobs.get(final_tree["docs/orin-thale/v676-v3/orchestration/terminal-route-hold.json"]).decode("utf-8"))
            diff_check = subprocess.run(["git", "-C", str(repo), "diff", "--check", EVIDENCE + ".." + head], capture_output=True)
            detailed_checks = {
                "source_to_x1_direct": direct_parent(repo, X1, SOURCE),
                "x1_to_evidence_direct": direct_parent(repo, EVIDENCE, X1),
                "evidence_to_final_direct": direct_parent(repo, head, EVIDENCE),
                "phase_commit_count_three": int(command(repo, "rev-list", "--count", SOURCE + ".." + head)) == 3,
                "zero_merges": command(repo, "rev-list", "--merges", SOURCE + ".." + head) == "",
                "one_final_parent": len(str(command(repo, "show", "-s", "--format=%P", head)).split()) == 1,
                "owner_below_file_ceiling": len(owner_paths) < 2000,
                "proposal_chain_7510": phase_truth["declared_proposal_chain"] == 7510,
                "outcomes_exact": phase_truth["core_outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
                "effective_negatives_exact": phase_truth["current_overlay"]["effective_negatives"] == 42036,
                "effective_methods_exact": phase_truth["current_overlay"]["effective_methods"] == 31828,
                "failed_witnesses_exact": phase_truth["current_overlay"]["retained_failed_witnesses"] == 13697,
                "passing_witnesses_exact": phase_truth["current_overlay"]["bounded_passing_witnesses"] == 18820,
                "open_gaps_exact": phase_truth["current_overlay"]["open_gaps"] == 353,
                "exact_gates_exact": phase_truth["current_overlay"]["exact_gates"] == 345,
                "method_flow_partition_exact": method_flow["phase_ledger_counts"] == {"methods": 620, "failed": 190, "passing": 430},
                "terminal_not_ready": phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
                "zero_real_rows": phase_truth["real_world_rows"] == 0,
                "zero_participants": phase_truth["participants"] == 0,
                "zero_external_actions": phase_truth["external_actions"] == 0,
                "no_full_repository_suite": phase_truth["full_repository_suite_run"] is False,
                "no_independent_reproduction_claim": phase_truth["independent_reproduction_claimed"] is False,
                "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0,
                "route_names_only_provisional_liora": route["provisional_exact_title"] == "Liora Venn" and route["provisional_phase"] == "v676-v4",
                "diff_hygiene": diff_check.returncode == 0,
            }
            if not all(detailed_checks.values()):
                raise AssertionError(f"detailed checks failed: {[key for key, value in detailed_checks.items() if not value]}")

        clean_after = command(repo, "status", "--porcelain=v1") == ""
        upstream_after = command(repo, "rev-parse", "@{upstream}")
        tracking_after = command(repo, "rev-parse", "refs/remotes/origin/" + BRANCH)
        live_after_line = command(repo, "ls-remote", "--heads", "origin", "refs/heads/" + BRANCH)
        assert isinstance(live_after_line, str)
        live_after = live_after_line.split("\t", 1)[0]
        divergence_after_value = command(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}")
        assert isinstance(divergence_after_value, str)
        divergence_after = divergence_after_value.split()
        if not clean_after or not (head == upstream_after == tracking_after == live_after) or divergence_after != ["0", "0"]:
            raise AssertionError("post-canonical clean/four-way-equality gate failed")

        payload.update(
            {
                "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
                "success_count": 1,
                "branch": branch,
                "exact_final": head,
                "source": SOURCE,
                "x1": X1,
                "evidence": EVIDENCE,
                "tests": tests,
                "selected_tests_passed": sum(row["passed"] for row in tests),
                "manifests": manifests,
                "manifest_entries_total": sum(row["entries"] for row in manifests),
                "manifest_declared_exclusions_total": sum(row["declared_exclusions"] for row in manifests),
                "strict_json_parses": json_count,
                "documents_checked": document_count,
                "maximum_document_words": max_document_words,
                "python_ast_checks": python_count,
                "privacy_candidates": privacy_candidates,
                "privacy_candidate_count": len(privacy_candidates),
                "confirmed_privacy_hits": 0,
                "bounded_security_findings": 0,
                "materialized_lifecycle_owner_files": materialized,
                "materialization_retained_external": True,
                "detailed_checks": detailed_checks,
                "detailed_checks_passed": sum(detailed_checks.values()),
                "detailed_checks_total": len(detailed_checks),
                "clean_before": clean_before,
                "clean_after": clean_after,
                "divergence_before": divergence,
                "divergence_after": divergence_after,
                "four_way_equal_before": True,
                "four_way_equal_after": True,
                "full_repository_suite_run": False,
                "same_owner_shared_infrastructure": True,
                "independent_reproduction": False,
                "canonical_replay_forbidden": True,
            }
        )
        canonical_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        payload["canonical_payload_sha256"] = hashlib.sha256(canonical_bytes).hexdigest()
        atomic_json(receipt, payload)
        atomic_json(latch, {"status": payload["status"], "invocation_count": 1, "success_count": 1, "exact_final": head})
        print(
            json.dumps(
                {
                    "status": payload["status"],
                    "exact_final": head,
                    "selected_tests_passed": payload["selected_tests_passed"],
                    "manifest_entries_total": payload["manifest_entries_total"],
                    "strict_json_parses": json_count,
                    "documents_checked": document_count,
                    "python_ast_checks": python_count,
                    "privacy_candidate_count": len(privacy_candidates),
                    "confirmed_privacy_hits": 0,
                    "bounded_security_findings": 0,
                    "detailed_checks": f"{sum(detailed_checks.values())}/{len(detailed_checks)}",
                    "canonical_payload_sha256": payload["canonical_payload_sha256"],
                },
                sort_keys=True,
            )
        )
        return 0
    except Exception as exc:
        payload.update(
            {
                "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
                "success_count": 0,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "canonical_replay_forbidden_without_explicit_additive_correction": True,
            }
        )
        atomic_json(receipt, payload)
        atomic_json(latch, {"status": payload["status"], "invocation_count": 1, "success_count": 0, "error_type": type(exc).__name__})
        print(json.dumps(payload, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
