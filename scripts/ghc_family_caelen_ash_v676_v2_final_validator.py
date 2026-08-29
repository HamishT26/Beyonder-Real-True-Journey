#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Caelen Ash v676-v2."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"
SOURCE = "939312172819669aad250cf034d8a6a7efe3df5b"
X1 = "39daa2da64125b839714efa8b7488d8ed9ed364b"
EVIDENCE = "bc7f321d66c094422ddc69275d811eb8ec917f3b"
OWNER_PREFIXES = (
    "docs/caelen-ash/v676-v2/",
    "scripts/build_ghc_family_caelen_ash_v676_v2_",
    "scripts/ghc_family_caelen_ash_v676_v2_",
    "tests/test_ghc_family_caelen_ash_v676_v2_",
)
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(rb"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(rb"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(rb"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(rb"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


def command(repo: Path, *args: str, text: bool = True):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=text)


def atomic_json(path: Path, value: object, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "x" if exclusive else "w"
    with path.open(mode, encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")


def tree_map(repo: Path, revision: str) -> dict[str, str]:
    result = {}
    for line in command(repo, "ls-tree", "-r", revision).splitlines():
        left, path = line.split("\t", 1)
        mode, kind, oid = left.split()
        if kind == "blob":
            result[path] = oid
    return result


class BlobReader:
    def __init__(self, repo: Path):
        self.proc = subprocess.Popen(
            ["git", "-C", str(repo), "cat-file", "--batch"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert self.proc.stdin and self.proc.stdout
        self.cache: dict[str, bytes] = {}

    def get(self, oid: str) -> bytes:
        if oid not in self.cache:
            assert self.proc.stdin and self.proc.stdout
            self.proc.stdin.write((oid + "\n").encode("ascii"))
            self.proc.stdin.flush()
            header = self.proc.stdout.readline().split()
            if len(header) < 3 or header[1] != b"blob":
                raise RuntimeError(f"object {oid} is not a blob")
            raw = self.proc.stdout.read(int(header[2]))
            self.proc.stdout.read(1)
            self.cache[oid] = raw
        return self.cache[oid]

    def close(self) -> None:
        assert self.proc.stdin
        self.proc.stdin.close()
        stderr = self.proc.stderr.read().decode("utf-8", "replace") if self.proc.stderr else ""
        code = self.proc.wait()
        if code:
            raise RuntimeError(stderr)


def normalized(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def validate_manifest(
    repo: Path,
    revision: str,
    manifest_path: str,
    tree: dict[str, str],
    blobs: BlobReader,
) -> dict[str, Any]:
    manifest = json.loads(blobs.get(tree[manifest_path]).decode("utf-8"))
    findings = []
    for row in manifest["entries"]:
        path = row["path"]
        oid = tree.get(path)
        if oid != row["git_blob_oid"]:
            findings.append({"path": path, "kind": "git_blob_oid"})
            continue
        raw = blobs.get(oid)
        if hashlib.sha256(normalized(raw)).hexdigest() != row["sha256_normalized_lf"]:
            findings.append({"path": path, "kind": "sha256_normalized_lf"})
    if findings:
        raise AssertionError(f"manifest failure {manifest_path}: {findings[:5]}")
    return {
        "revision": revision,
        "path": manifest_path,
        "entries": len(manifest["entries"]),
        "declared_exclusions": len(manifest["declared_exclusions"]),
    }


def materialize_owner_tree(target: Path, tree: dict[str, str], blobs: BlobReader) -> int:
    count = 0
    for path, oid in tree.items():
        if not path.startswith(OWNER_PREFIXES):
            continue
        output = target / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(blobs.get(oid))
        count += 1
    return count


def run_pytest(cwd: Path, test_path: str, exclude: str | None = None) -> dict[str, Any]:
    args = [sys.executable, "-X", "utf8", "-m", "pytest", "-q", test_path]
    if exclude:
        args.extend(["-k", f"not {exclude}"])
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=600)
    output = (result.stdout + "\n" + result.stderr).strip()
    if result.returncode:
        raise AssertionError(f"pytest failed for {test_path}: {output[-4000:]}")
    match = re.search(r"(\d+) passed", output)
    if not match:
        raise AssertionError(f"pytest count unavailable for {test_path}")
    return {"path": test_path, "passed": int(match.group(1)), "excluded_lifecycle_test": exclude, "output_tail": output[-500:]}


def direct_parent(repo: Path, child: str, parent: str) -> bool:
    return command(repo, "rev-parse", f"{child}^").strip() == parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--latch", type=Path, required=True)
    parser.add_argument("--temp-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    receipt = args.receipt.resolve()
    latch = args.latch.resolve()
    temp_root = args.temp_root.resolve()
    expected_final = args.expected_final
    if latch.exists() or receipt.exists():
        raise SystemExit("exclusive canonical latch or receipt already exists; replay refused")

    invocation = {
        "owner": "Caelen Ash",
        "phase": "v676-v2",
        "expected_final": expected_final,
        "status": "INVOKED_ONCE_PENDING",
        "invocation_count": 1,
        "success_count": 0,
    }
    atomic_json(latch, invocation, exclusive=True)
    payload: dict[str, Any] = dict(invocation)
    try:
        branch = command(repo, "branch", "--show-current").strip()
        head = command(repo, "rev-parse", "HEAD").strip()
        clean_before = not command(repo, "status", "--porcelain=v1").strip()
        upstream = command(repo, "rev-parse", "@{upstream}").strip()
        tracking = command(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}").strip()
        live_line = command(repo, "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").strip()
        live = live_line.split("\t", 1)[0]
        divergence = command(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").strip().split()
        if branch != BRANCH or head != expected_final:
            raise AssertionError("exact branch or head mismatch")
        if not clean_before:
            raise AssertionError("lane dirty before canonical invocation")
        if not (head == upstream == tracking == live):
            raise AssertionError("pre-canonical four-way equality failed")
        if divergence != ["0", "0"]:
            raise AssertionError("pre-canonical divergence is not 0/0")

        trees = {
            X1: tree_map(repo, X1),
            EVIDENCE: tree_map(repo, EVIDENCE),
            head: tree_map(repo, head),
        }
        blobs = BlobReader(repo)
        manifests = [
            validate_manifest(repo, X1, "docs/caelen-ash/v676-v2/validation/x1-manifest.json", trees[X1], blobs),
            validate_manifest(repo, EVIDENCE, "docs/caelen-ash/v676-v2/validation/evidence-manifest.json", trees[EVIDENCE], blobs),
            validate_manifest(repo, head, "docs/caelen-ash/v676-v2/validation/final-delta-manifest.json", trees[head], blobs),
            validate_manifest(repo, head, "docs/caelen-ash/v676-v2/validation/final-owner-manifest.json", trees[head], blobs),
        ]

        temp_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="ca6762-", dir=temp_root) as temp:
            temp_path = Path(temp)
            x1_dir = temp_path / "x1"
            evidence_dir = temp_path / "evidence"
            materialized = {
                "x1": materialize_owner_tree(x1_dir, trees[X1], blobs),
                "evidence": materialize_owner_tree(evidence_dir, trees[EVIDENCE], blobs),
            }
            tests = [
                run_pytest(x1_dir, "tests/test_ghc_family_caelen_ash_v676_v2_x1.py", "test_x1_runs_on_exact_source_and_owner_branch"),
                run_pytest(evidence_dir, "tests/test_ghc_family_caelen_ash_v676_v2_x2.py", "test_x2_is_built_only_from_immutable_x1"),
                run_pytest(repo, "tests/test_ghc_family_caelen_ash_v676_v2_final.py"),
            ]

        final_tree = trees[head]
        owner_paths = sorted(path for path in final_tree if path.startswith(OWNER_PREFIXES))
        json_count = 0
        document_count = 0
        python_count = 0
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
                text_value = raw.decode("utf-8")
                if len(text_value.split()) > 100_000:
                    raise AssertionError(f"document word cap exceeded: {path}")
            if path.endswith(".py"):
                python_count += 1
                tree = ast.parse(raw.decode("utf-8"), filename=path)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        names = [alias.name for alias in node.names]
                        if any(name in {"requests", "urllib.request", "socket"} for name in names):
                            security_findings.append({"path": path, "kind": "network_import"})
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                        security_findings.append({"path": path, "kind": node.func.id})
            if path.endswith((".json", ".md", ".html", ".py")):
                for name, pattern in PRIVACY_PATTERNS.items():
                    if pattern.search(raw):
                        privacy_candidates.append({"class": name, "path": path})
        unknown_outcomes = [row for row in outcome_values if row[2] not in ALLOWED_OUTCOMES]
        if unknown_outcomes:
            raise AssertionError(f"unknown outcome labels: {unknown_outcomes[:5]}")
        if security_findings:
            raise AssertionError(f"bounded security findings: {security_findings}")
        adjudication = json.loads(blobs.get(final_tree["docs/caelen-ash/v676-v2/validation/final-privacy-adjudication.json"]).decode("utf-8"))
        if adjudication["candidate_count"] != len(privacy_candidates) or adjudication["confirmed_five_class_privacy_or_raw_identifier_hits"] != 0:
            raise AssertionError("privacy candidate adjudication mismatch")

        content_seal = json.loads(blobs.get(final_tree["docs/caelen-ash/v676-v2/closeout/content-seal.json"]).decode("utf-8"))
        for row in content_seal["entries"]:
            raw = blobs.get(final_tree[row["path"]])
            if hashlib.sha256(normalized(raw)).hexdigest() != row["sha256_normalized_lf"]:
                raise AssertionError(f"content seal mismatch: {row['path']}")

        phase_truth = json.loads(blobs.get(final_tree["docs/caelen-ash/v676-v2/final/phase-truth.json"]).decode("utf-8"))
        method_flow = json.loads(blobs.get(final_tree["docs/caelen-ash/v676-v2/final/method-flow-ledger.json"]).decode("utf-8"))
        route = json.loads(blobs.get(final_tree["docs/caelen-ash/v676-v2/handoffs/terminal-route-hold.json"]).decode("utf-8"))
        detailed_checks = {
            "source_to_x1_direct": direct_parent(repo, X1, SOURCE),
            "x1_to_evidence_direct": direct_parent(repo, EVIDENCE, X1),
            "evidence_to_final_direct": direct_parent(repo, head, EVIDENCE),
            "phase_commit_count_three": int(command(repo, "rev-list", "--count", f"{SOURCE}..{head}").strip()) == 3,
            "zero_merges": not command(repo, "rev-list", "--merges", f"{SOURCE}..{head}").strip(),
            "one_final_parent": len(command(repo, "show", "-s", "--format=%P", head).strip().split()) == 1,
            "owner_below_file_ceiling": len(owner_paths) < 2000,
            "proposal_chain_7470": phase_truth["proposal_chain"] == 7470,
            "outcomes_exact": phase_truth["core_outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "negative_overlay_exact": phase_truth["current_overlay"]["effective_negatives"] == 41843,
            "method_overlay_exact": phase_truth["current_overlay"]["effective_methods"] == 31203,
            "failed_overlay_exact": phase_truth["current_overlay"]["retained_failed_witnesses"] == 13504,
            "passing_overlay_exact": phase_truth["current_overlay"]["bounded_passing_witnesses"] == 18388,
            "open_gaps_exact": phase_truth["current_overlay"]["open_gaps"] == 351,
            "exact_gates_exact": phase_truth["current_overlay"]["exact_gates"] == 343,
            "method_flow_counts_exact": method_flow["phase_ledger_counts"] == {"methods": 449, "failed": 181, "passing": 268},
            "terminal_not_ready": phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
            "zero_real_rows": phase_truth["real_world_rows"] == 0,
            "zero_participants": phase_truth["participants"] == 0,
            "no_full_repository_suite": phase_truth["full_repository_suite_run"] is False,
            "no_independent_reproduction_claim": phase_truth["independent_reproduction_claimed"] is False,
            "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0,
            "successor_not_inferred": route["successor_inferred"] is False,
            "diff_hygiene": subprocess.run(["git", "-C", str(repo), "diff", "--check", f"{EVIDENCE}..{head}"], capture_output=True).returncode == 0,
        }
        if not all(detailed_checks.values()):
            raise AssertionError(f"detailed checks failed: {[key for key, value in detailed_checks.items() if not value]}")

        clean_after = not command(repo, "status", "--porcelain=v1").strip()
        upstream_after = command(repo, "rev-parse", "@{upstream}").strip()
        tracking_after = command(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}").strip()
        live_after_line = command(repo, "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").strip()
        live_after = live_after_line.split("\t", 1)[0]
        divergence_after = command(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").strip().split()
        if not clean_after or not (head == upstream_after == tracking_after == live_after) or divergence_after != ["0", "0"]:
            raise AssertionError("post-canonical clean/equality gate failed")
        blobs.close()

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
                "python_ast_checks": python_count,
                "privacy_candidates": privacy_candidates,
                "privacy_candidate_count": len(privacy_candidates),
                "confirmed_privacy_hits": 0,
                "bounded_security_findings": 0,
                "materialized_lifecycle_owner_files": materialized,
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
        print(json.dumps(payload, sort_keys=True))
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
