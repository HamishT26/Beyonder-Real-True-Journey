#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Caelen v674-v3."""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SOURCE = "0b9ccf8c74f3b0a5f96b8582162df8e2a06edd05"
X1 = "aaff9f4bfe18c2d7dd428cf6cb7b639f3b420b46"
EVIDENCE = "0a50b3d7a13fe3b78302d41b6f8ad61325208ebd"
BRANCH = "codex/GHC-Family/caelen-ash-v674-v3-full-tools"
REPO = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/caelen-ash/v674-v3/"


def git(*args: str, text: bool = True) -> str | bytes:
    return subprocess.check_output(
        ["git", *args], cwd=REPO, text=text, encoding="utf-8" if text else None
    )


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def load_commit_blobs(commit: str, wanted: list[str]) -> dict[str, bytes]:
    if not wanted:
        return {}
    tree = git("ls-tree", "-r", "-z", commit, text=False)
    assert isinstance(tree, bytes)
    object_ids: dict[str, str] = {}
    for record in tree.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        parts = metadata.split()
        if len(parts) == 3 and parts[1] == b"blob":
            object_ids[raw_path.decode("utf-8")] = parts[2].decode("ascii")
    missing = [path for path in wanted if path not in object_ids]
    if missing:
        raise RuntimeError(f"commit tree missing paths: {missing}")
    ordered_ids = [object_ids[path] for path in wanted]
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, error = process.communicate(
        ("\n".join(ordered_ids) + "\n").encode("ascii")
    )
    if process.returncode != 0:
        raise RuntimeError(error.decode("utf-8", errors="replace"))
    stream = io.BytesIO(output)
    result: dict[str, bytes] = {}
    for path, expected_oid in zip(wanted, ordered_ids, strict=True):
        header = stream.readline().decode("ascii").strip().split()
        if len(header) != 3 or header[0] != expected_oid or header[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
        size = int(header[2])
        data = stream.read(size)
        if len(data) != size or stream.read(1) != b"\n":
            raise RuntimeError(f"truncated cat-file payload for {path}")
        result[path] = data
    return result


def commit_json(commit: str, path: str) -> dict[str, Any]:
    return json.loads(load_commit_blobs(commit, [path])[path].decode("utf-8"))


def verify_manifest(commit: str, path: str, domain: str) -> dict[str, int]:
    manifest = commit_json(commit, path)
    entries = manifest["entries"]
    paths = [entry["path"] for entry in entries]
    blobs = load_commit_blobs(commit, paths)
    for entry in entries:
        data = blobs[entry["path"]]
        if domain == "normalized_lf":
            data = normalized(data)
            expected_bytes = entry["bytes_normalized_lf"]
            expected_hash = entry["sha256_normalized_lf"]
        elif domain == "raw_sha256":
            expected_bytes = entry["bytes"]
            expected_hash = entry.get(
                "sha256", entry.get("sha256_git_index_blob")
            )
        else:
            raise RuntimeError(f"unknown manifest domain {domain}")
        if expected_hash is None:
            raise RuntimeError(f"manifest digest key missing: {path}")
        if (
            len(data) != expected_bytes
            or hashlib.sha256(data).hexdigest() != expected_hash
        ):
            raise RuntimeError(f"manifest mismatch: {path} -> {entry['path']}")
    return {
        "entries": len(entries),
        "self_exclusions": len(manifest.get("self_exclusions", [])),
    }


def write_exclusive_receipt(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(
        payload, indent=2, sort_keys=True, ensure_ascii=True
    ) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(encoded)


def canonical(expected_final: str) -> dict[str, Any]:
    local = str(git("rev-parse", "HEAD")).strip()
    if local != expected_final:
        raise RuntimeError(f"expected final mismatch: {local}")
    branch = str(git("branch", "--show-current")).strip()
    if branch != BRANCH:
        raise RuntimeError(f"unexpected branch: {branch}")
    if str(git("status", "--porcelain=v1")).strip():
        raise RuntimeError("canonical worktree is not clean before validation")
    if str(git("rev-parse", "HEAD^")).strip() != EVIDENCE:
        raise RuntimeError("final is not the direct child of evidence")
    if str(git("rev-parse", f"{EVIDENCE}^")).strip() != X1:
        raise RuntimeError("evidence is not the direct child of x1")
    if str(git("rev-parse", f"{X1}^")).strip() != SOURCE:
        raise RuntimeError("x1 is not the direct child of source")
    if str(git("rev-list", "--count", f"{SOURCE}..{expected_final}")).strip() != "3":
        raise RuntimeError("phase commit count is not three")
    if str(git("rev-list", "--merges", f"{SOURCE}..{expected_final}")).strip():
        raise RuntimeError("merge commit found in phase history")
    parent_count = len(
        str(git("show", "-s", "--format=%P", expected_final)).split()
    )
    if parent_count != 1:
        raise RuntimeError("final does not have exactly one parent")

    manifest_results = {
        "x1": verify_manifest(
            X1,
            "docs/caelen-ash/v674-v3/x1/x1-manifest.json",
            "raw_sha256",
        ),
        "x1_staged": verify_manifest(
            X1,
            "docs/caelen-ash/v674-v3/validation/x1-staged-review.json",
            "raw_sha256",
        ),
        "evidence": verify_manifest(
            EVIDENCE,
            "docs/caelen-ash/v674-v3/validation/x2-evidence-manifest.json",
            "normalized_lf",
        ),
        "evidence_staged": verify_manifest(
            EVIDENCE,
            "docs/caelen-ash/v674-v3/validation/x2-staged-review.json",
            "raw_sha256",
        ),
        "final_owner": verify_manifest(
            expected_final,
            "docs/caelen-ash/v674-v3/validation/final-owner-manifest.json",
            "normalized_lf",
        ),
        "final_delta": verify_manifest(
            expected_final,
            "docs/caelen-ash/v674-v3/validation/final-delta-manifest.json",
            "normalized_lf",
        ),
        "final_staged": verify_manifest(
            expected_final,
            "docs/caelen-ash/v674-v3/validation/final-staged-review.json",
            "raw_sha256",
        ),
    }

    changed = str(git("diff", "--name-only", f"{SOURCE}..{expected_final}")).splitlines()
    owner_paths = sorted(
        path
        for path in changed
        if path.startswith(PHASE_PREFIX)
        or "caelen_ash_v674_v3" in path
        or path.startswith("scripts/ghc_family_caelen_v674_v3_")
    )
    if len(owner_paths) >= 2000:
        raise RuntimeError("owner file ceiling reached")
    if len(owner_paths) != len(changed):
        foreign = sorted(set(changed) - set(owner_paths))
        raise RuntimeError(f"non-owner source-to-final paths: {foreign}")
    blobs = load_commit_blobs(expected_final, owner_paths)
    json_parses = 0
    python_compiles = 0
    markdown_documents = 0
    html_documents = 0
    security_findings: list[dict[str, str]] = []
    for path, data in blobs.items():
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_parses += 1
        if path.endswith(".py"):
            source = data.decode("utf-8")
            compile(source, path, "exec")
            python_compiles += 1
            tree = ast.parse(source, filename=path)
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id in {"eval", "exec"}
                ):
                    security_findings.append(
                        {"path": path, "call": node.func.id}
                    )
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "system"
                ):
                    security_findings.append({"path": path, "call": "system"})
        if path.endswith(".md"):
            markdown_documents += 1
            words = len(data.decode("utf-8").split())
            if words > 100000:
                raise RuntimeError(f"document ceiling exceeded: {path}")
        if path.endswith(".html"):
            html_documents += 1
    if security_findings:
        raise RuntimeError(f"bounded AST security findings: {security_findings}")

    patterns = {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:C:\\Users\\|D:\\GHC-Archives)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{32,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }
    scanner_candidates: list[dict[str, str]] = []
    confirmed_hits: list[dict[str, str]] = []
    text_extensions = {".json", ".md", ".html", ".py", ".txt", ".yml", ".yaml"}
    privacy_files = 0
    for path, data in blobs.items():
        if Path(path).suffix.lower() not in text_extensions:
            continue
        privacy_files += 1
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                context = data[max(0, match.start() - 400) : match.end() + 120]
                if path.endswith(".py") and (
                    b"re.compile" in context
                    or b"assertNot" in context
                    or b"patterns" in context
                ):
                    scanner_candidates.append(
                        {
                            "path": path,
                            "class": class_name,
                            "disposition": "scanner_definition_or_rejection_assertion",
                        }
                    )
                else:
                    confirmed_hits.append({"path": path, "class": class_name})
    if confirmed_hits:
        raise RuntimeError(f"confirmed privacy hits: {confirmed_hits}")

    phase_truth = commit_json(
        expected_final,
        "docs/caelen-ash/v674-v3/final/phase-truth.json",
    )
    if phase_truth["outcomes"] != {
        "completed": 42,
        "represented": 12,
        "open_gap": 3,
        "exact_gate": 3,
    }:
        raise RuntimeError("final outcome vocabulary or counts drifted")
    if phase_truth["terminal_verdict"] != "NOT_READY_FOR_STAGE_20":
        raise RuntimeError("terminal veto drifted")
    if phase_truth["effective_counts"] != {
        "effective_negatives": 38612,
        "methods": 26466,
        "failed_witnesses": 10273,
        "bounded_passing_witnesses": 13749,
        "open_gaps": 316,
        "exact_gates": 309,
    }:
        raise RuntimeError("effective Method Flow counts drifted")

    evidence_selection = commit_json(
        EVIDENCE,
        "docs/caelen-ash/v674-v3/x2/lifecycle/evidence-test-selection.json",
    )
    if evidence_selection["immutable_x1_precommit_context"]["passed"] != 12:
        raise RuntimeError("immutable x1 selection drifted")
    if evidence_selection["current_x2_context"]["passed"] != 15:
        raise RuntimeError("immutable x2 selection drifted")
    if evidence_selection["eligible_composite"]["passed"] != 27:
        raise RuntimeError("eligible lifecycle selection drifted")

    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    test_run = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_ghc_family_caelen_ash_v674_v3_final",
            "-v",
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )
    test_output = test_run.stdout + test_run.stderr
    if test_run.returncode != 0 or "Ran 14 tests" not in test_output:
        raise RuntimeError(
            "final owner test selection failed: " + test_output[-6000:]
        )

    minimal_checks = {
        "exact_source": str(git("merge-base", "--is-ancestor", SOURCE, expected_final)).strip() == "",
        "x1_direct_child": str(git("rev-parse", f"{X1}^")).strip() == SOURCE,
        "evidence_direct_child": str(git("rev-parse", f"{EVIDENCE}^")).strip() == X1,
        "final_direct_child": str(git("rev-parse", "HEAD^")).strip() == EVIDENCE,
        "three_phase_commits": str(git("rev-list", "--count", f"{SOURCE}..HEAD")).strip() == "3",
        "zero_merges": not str(git("rev-list", "--merges", f"{SOURCE}..HEAD")).strip(),
        "one_final_parent": parent_count == 1,
        "exact_branch": branch == BRANCH,
        "exact_head": local == expected_final,
        "owner_files_below_cap": len(owner_paths) < 2000,
        "all_json_parsed": json_parses > 0,
        "all_python_compiled": python_compiles > 0,
        "document_caps": markdown_documents > 0,
        "privacy_five_classes": len(patterns) == 5,
        "zero_confirmed_privacy_hits": not confirmed_hits,
        "zero_bounded_ast_findings": not security_findings,
        "exact_four_label_outcomes": set(phase_truth["outcomes"]) == {"completed", "represented", "open_gap", "exact_gate"},
        "stage20_veto": phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "no_complete_repo_claim": not phase_truth["complete_repository_suite"],
        "no_independent_reproduction_claim": not phase_truth["independent_reproduction"],
        "immutable_x1_selection": evidence_selection["immutable_x1_precommit_context"]["passed"] == 12,
        "immutable_x2_selection": evidence_selection["current_x2_context"]["passed"] == 15,
        "seven_manifest_replays": len(manifest_results) == 7,
        "final_tests_fourteen": "Ran 14 tests" in test_output,
        "clean_before_remote_check": not str(git("status", "--porcelain=v1")).strip(),
    }
    failed_minimal = [key for key, value in minimal_checks.items() if not value]
    if failed_minimal:
        raise RuntimeError(f"minimal checks failed: {failed_minimal}")

    local_after = str(git("rev-parse", "HEAD")).strip()
    upstream = str(git("rev-parse", "@{upstream}")).strip()
    tracking = str(
        git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    ).strip()
    live_line = str(
        git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    ).strip()
    live = live_line.split()[0] if live_line else ""
    divergence = str(
        git("rev-list", "--left-right", "--count", "@{upstream}...HEAD")
    ).strip().split()
    if not (local_after == expected_final == upstream == tracking == live):
        raise RuntimeError("final four-way equality failed")
    if divergence != ["0", "0"]:
        raise RuntimeError(f"final divergence is not zero: {divergence}")
    if str(git("status", "--porcelain=v1")).strip():
        raise RuntimeError("canonical worktree is not clean after validation")

    detailed_checks = (
        sum(row["entries"] for row in manifest_results.values())
        + len(owner_paths)
        + json_parses
        + python_compiles
        + markdown_documents
        + html_documents
        + len(minimal_checks)
        + 14
    )
    payload: dict[str, Any] = {
        "schema": "ghc.family.external-canonical-receipt.v674.v3",
        "owner": "Caelen Ash",
        "phase": "v674-v3",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "expected_final": expected_final,
        "branch": BRANCH,
        "canonical_invocations": 1,
        "canonical_successes": 1,
        "replayed": False,
        "owner_tests": {
            "final_current": {"selected": 14, "passed": 14, "failed": 0},
            "immutable_x1": {"selected": 12, "passed": 12, "failed": 0},
            "immutable_x2": {"selected": 15, "passed": 15, "failed": 0},
            "eligible_lifecycle_total": 41,
        },
        "detailed_checks": {"checked": detailed_checks, "failed": 0},
        "minimal_checks": {"checked": len(minimal_checks), "failed": 0},
        "manifest_results": manifest_results,
        "manifest_entries_total": sum(
            row["entries"] for row in manifest_results.values()
        ),
        "manifest_self_exclusions_total": sum(
            row["self_exclusions"] for row in manifest_results.values()
        ),
        "owner_paths": len(owner_paths),
        "json_parses": json_parses,
        "python_compiles": python_compiles,
        "markdown_documents": markdown_documents,
        "html_documents": html_documents,
        "privacy_files": privacy_files,
        "privacy_classes": list(patterns),
        "scanner_definition_candidates": len(scanner_candidates),
        "confirmed_privacy_hits": 0,
        "bounded_ast_security_findings": 0,
        "source_to_final_commits": 3,
        "merge_commits": 0,
        "final_parent_count": 1,
        "clean_before_and_after": True,
        "divergence": [0, 0],
        "four_way_equal": True,
        "complete_repository_suite": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    canonical_bytes = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    payload["canonical_payload_sha256"] = hashlib.sha256(
        canonical_bytes
    ).hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt-path", required=True)
    args = parser.parse_args()
    receipt_path = Path(args.receipt_path)
    if receipt_path.exists():
        print(
            json.dumps(
                {"status": "REFUSED_CANONICAL_LATCH_ALREADY_SPENT"},
                sort_keys=True,
            )
        )
        return 3
    try:
        payload = canonical(args.expected_final)
    except Exception as error:  # one-shot failure remains zero success credit
        payload = {
            "schema": "ghc.family.external-canonical-receipt.v674.v3",
            "owner": "Caelen Ash",
            "phase": "v674-v3",
            "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "expected_final": args.expected_final,
            "canonical_invocations": 1,
            "canonical_successes": 0,
            "replay_forbidden": True,
            "error_type": type(error).__name__,
            "error": str(error),
            "complete_repository_suite": False,
            "independent_reproduction": False,
        }
        write_exclusive_receipt(receipt_path, payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1
    write_exclusive_receipt(receipt_path, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
