#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical for Caelen Ash v687-v5."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

from ghc_family_caelen_ash_v687_v5_core import strict_load


ROOT = Path(__file__).resolve().parents[1]
BASE = "docs/caelen-ash/v687-v5"
SOURCE = "5a71b1b7866171aa4ee16664ab7fc434bb6f5593"
X1 = "a3e882fc450322186c71ab430be501f3cb3648a0"
EVIDENCE = "e2de3422d62572b7d1e8fbfa8e84c8a4f9fded72"
BRANCH = "codex/GHC-Family/caelen-ash-v687-v5-full-tools"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, text=True, encoding="utf-8", errors="strict", capture_output=True)


def batch_git_objects(specifications: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert process.stdin is not None and process.stdout is not None
    objects: dict[str, bytes] = {}
    for specification in specifications:
        process.stdin.write((specification + "\n").encode("utf-8"))
        process.stdin.flush()
        header = process.stdout.readline().decode("ascii", errors="strict").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError("unexpected git cat-file header for " + specification)
        size = int(header[2])
        objects[specification] = process.stdout.read(size)
        if process.stdout.read(1) != b"\n":
            raise RuntimeError("missing git cat-file separator")
    process.stdin.close()
    error = process.stderr.read() if process.stderr is not None else b""
    code = process.wait()
    if code:
        raise RuntimeError("git cat-file failed: " + error.decode("utf-8", errors="replace"))
    return objects


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def is_owner(relative: str) -> bool:
    return relative.startswith(BASE + "/") or bool(re.fullmatch(r"(?:scripts|tests)/[^/]*caelen_ash_v687_v5[^/]*\.py", relative))


def replay(anchor: str, relative_manifest: str) -> dict:
    manifest = strict_load(ROOT / relative_manifest)
    specifications = [anchor + ":" + entry["path"] for entry in manifest["entries"]]
    objects = batch_git_objects(specifications)
    mismatches = []
    for entry in manifest["entries"]:
        specification = anchor + ":" + entry["path"]
        actual = hashlib.sha256(normalized(objects[specification])).hexdigest()
        expected = entry["sha256_normalized_lf"]
        if actual != expected:
            mismatches.append({"path": entry["path"], "expected": expected, "actual": actual})
    return {"anchor": anchor, "manifest": relative_manifest, "entries": len(manifest["entries"]), "self_exclusions": len(manifest["self_exclusions"]), "mismatches": mismatches}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt-dir", type=Path, required=True)
    args = parser.parse_args()
    receipt_dir = args.receipt_dir.resolve()
    if receipt_dir.is_relative_to(ROOT):
        raise SystemExit("external receipt directory required")
    receipt_dir.mkdir(parents=True, exist_ok=True)
    latch = receipt_dir / "canonical-latch.json"
    receipt_path = receipt_dir / "exact-final-canonical.json"
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with latch.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump({"owner": "Caelen Ash", "phase": "v687-v5", "expected_head": args.expected_head, "invocation": 1, "started_at": started}, stream, ensure_ascii=False, sort_keys=True)
        stream.write("\n")

    result = {
        "owner": "Caelen Ash",
        "phase": "v687-v5",
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "expected_head": args.expected_head,
        "canonical_invocation_count": 1,
        "canonical_success_count": 0,
        "canonical_replay_count": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "full_repository_suite": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "started_at": started,
    }
    try:
        local = git("rev-parse", "HEAD").stdout.strip()
        upstream = git("rev-parse", "@{u}").stdout.strip()
        tracking = git("rev-parse", "refs/remotes/origin/" + BRANCH).stdout.strip()
        live_lines = [line for line in git("ls-remote", "origin", "refs/heads/" + BRANCH).stdout.splitlines() if line]
        live = live_lines[0].split()[0] if len(live_lines) == 1 else None
        branch = git("branch", "--show-current").stdout.strip()
        divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}").stdout.split()
        clean = not git("status", "--porcelain").stdout.strip()
        parents = git("show", "-s", "--format=%P", "HEAD").stdout.split()
        lifecycle = {
            "x1_parent": git("rev-parse", X1 + "^").stdout.strip(),
            "evidence_parent": git("rev-parse", EVIDENCE + "^").stdout.strip(),
            "final_parents": parents,
            "phase_commits": int(git("rev-list", "--count", SOURCE + ".." + args.expected_head).stdout.strip()),
            "phase_merges": int(git("rev-list", "--merges", "--count", SOURCE + ".." + args.expected_head).stdout.strip()),
        }
        remote = {"local": local, "upstream": upstream, "tracking": tracking, "fresh_live": live, "branch": branch, "divergence": [int(value) for value in divergence], "clean": clean}
        if not (local == args.expected_head == upstream == tracking == live and branch == BRANCH and divergence == ["0", "0"] and clean):
            raise RuntimeError("exact head or remote equality failure")
        if not (lifecycle["x1_parent"] == SOURCE and lifecycle["evidence_parent"] == X1 and parents == [EVIDENCE] and lifecycle["phase_commits"] == 3 and lifecycle["phase_merges"] == 0):
            raise RuntimeError("lifecycle ancestry failure")

        manifests = [
            replay(X1, BASE + "/validation/x1-manifest.json"),
            replay(EVIDENCE, BASE + "/validation/x2-manifest.json"),
            replay(args.expected_head, BASE + "/validation/final-delta-manifest.json"),
            replay(args.expected_head, BASE + "/validation/final-owner-manifest.json"),
        ]
        if any(item["mismatches"] for item in manifests):
            raise RuntimeError("manifest mismatch")
        final_delta = strict_load(ROOT / BASE / "validation" / "final-delta-manifest.json")
        actual_delta = set(git("diff", "--name-only", EVIDENCE + ".." + args.expected_head).stdout.splitlines())
        expected_delta = {entry["path"] for entry in final_delta["entries"]} | set(final_delta["self_exclusions"])
        if actual_delta != expected_delta:
            raise RuntimeError("final delta coverage failure")
        owner_manifest = strict_load(ROOT / BASE / "validation" / "final-owner-manifest.json")
        actual_owner = {line for line in git("ls-tree", "-r", "--name-only", args.expected_head).stdout.splitlines() if is_owner(line)}
        expected_owner = {entry["path"] for entry in owner_manifest["entries"]} | set(owner_manifest["self_exclusions"])
        if actual_owner != expected_owner:
            raise RuntimeError("final owner coverage failure")

        suite = unittest.TestLoader().loadTestsFromNames(["tests.test_ghc_family_caelen_ash_v687_v5_x2", "tests.test_ghc_family_caelen_ash_v687_v5_final"])
        tests = unittest.TestResult()
        suite.run(tests)
        if tests.testsRun != 20 or tests.failures or tests.errors:
            raise RuntimeError("owner test failure")
        json_paths = [ROOT / relative for relative in sorted(actual_owner) if relative.endswith(".json")]
        for path in json_paths:
            strict_load(path)
        privacy = strict_load(ROOT / BASE / "validation" / "final-privacy.json")
        security = strict_load(ROOT / BASE / "validation" / "final-security.json")
        staged_review = strict_load(ROOT / BASE / "validation" / "final-staged-review.json")
        if privacy["confirmed_count"] or security["findings"] or staged_review["state"] != "PASS":
            raise RuntimeError("privacy, security, or staged-review failure")
        baton_index = strict_load(ROOT / BASE / "handoffs" / "baton-index.json")
        baton = (ROOT / BASE / "handoffs" / "future-sibling-09-v687-v6-induction-baton.md").read_bytes()
        baton_text = baton.decode("utf-8")
        if hashlib.sha256(baton).hexdigest() != baton_index["sha256"] or len(baton_text.split()) != baton_index["words"] or not 10_000 <= baton_index["words"] <= 100_000 or not baton_text.rstrip().endswith(baton_index["eof"]):
            raise RuntimeError("baton integrity failure")
        promotion = strict_load(ROOT / BASE / "x2" / "promotion-receipt.json")
        global_validation = strict_load(ROOT / BASE / "x2" / "global-install-validation.json")
        if not promotion["source_global_byte_parity"] or global_validation["global_shared_interfaces_smoked"] != 5:
            raise RuntimeError("global promotion validation failure")

        result.update(
            {
                "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
                "canonical_success_count": 1,
                "tests": {"selected": tests.testsRun, "passed": tests.testsRun},
                "manifests": manifests,
                "manifest_bindings": sum(item["entries"] for item in manifests),
                "manifest_self_exclusions": sum(item["self_exclusions"] for item in manifests),
                "strict_json_documents": len(json_paths),
                "privacy": {"files_scanned": privacy["files_scanned"], "candidates": len(privacy["candidates"]), "confirmed": privacy["confirmed_count"], "complete_privacy": False},
                "security": {"python_files": security["python_files"], "findings": len(security["findings"]), "exhaustive_security": False},
                "baton": {"sha256": baton_index["sha256"], "words": baton_index["words"], "modules": baton_index["modules"]},
                "owner_files": len(actual_owner),
                "final_delta_files": len(actual_delta),
                "lifecycle": lifecycle,
                "remote": remote,
                "completed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
        )
    except Exception as exc:
        result.update({"status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT", "error_type": type(exc).__name__, "error": str(exc), "completed_at": datetime.datetime.now(datetime.timezone.utc).isoformat()})
        with receipt_path.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
        raise
    with receipt_path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "tests": result["tests"], "manifest_bindings": result["manifest_bindings"], "strict_json_documents": result["strict_json_documents"], "owner_files": result["owner_files"], "fresh_four_way_equal": len(set([result["remote"][key] for key in ["local", "upstream", "tracking", "fresh_live"]])) == 1}))


if __name__ == "__main__":
    main()
