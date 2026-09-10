"""Run Lyren v690-v1 exact-final owner-scoped canonical validation once."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import unittest
from datetime import UTC, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = "docs/lyren-moss/v690-v1/"
BRANCH = "codex/GHC-Family/lyren-moss-main"
SOURCE = "fbd8eb790f2f8bc9c507db0420bdd66d1ec05e2e"
PLANNING = "cd9baca94099be83f5b9a8ae5367e2f63a272614"
X1 = "13048b82fb42c27ff287bf6793c9b52d67a49f96"
X2 = "b716b6694110e4b60154d8d91de1bfdf5b2b7ab1"


def command(*args: str, text: bool = True) -> str | bytes:
    return subprocess.check_output(args, cwd=ROOT, text=text)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def git_blobs(head: str) -> dict[str, bytes]:
    raw = command("git", "ls-tree", "-r", "-z", "--format=%(objectname)%x09%(path)", head, text=False)
    entries = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        object_id, encoded_path = record.split(b"\t", 1)
        path = encoded_path.decode("utf-8")
        if path == "scripts/build_ghc_family_lyren_v690_v1_plan.py" or path.startswith(
            (
                BASE,
                "scripts/ghc_family_error_control_",
                "scripts/ghc_family_lyren_v690_v1_",
                "tests/test_ghc_family_lyren_v690_v1_",
            )
        ):
            entries.append((object_id.decode("ascii"), path))
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    blobs: dict[str, bytes] = {}
    for object_id, path in entries:
        process.stdin.write(object_id.encode("ascii") + b"\n")
        process.stdin.flush()
        header = process.stdout.readline().decode("ascii").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
        size = int(header[2])
        data = process.stdout.read(size)
        terminator = process.stdout.read(1)
        if len(data) != size or terminator != b"\n":
            raise RuntimeError(f"incomplete blob response for {path}")
        blobs[path] = data
    process.stdin.close()
    if process.wait(timeout=30) != 0:
        assert process.stderr is not None
        raise RuntimeError(process.stderr.read().decode("utf-8", errors="replace"))
    return blobs


def manifest_replays(blobs: dict[str, bytes], manifest_path: str) -> int:
    manifest = json.loads(blobs[manifest_path])
    for row in manifest["entries"]:
        data = blobs[row["path"]]
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise RuntimeError(f"manifest mismatch: {manifest_path}: {row['path']}")
    return len(manifest["entries"])


def run_tests() -> tuple[int, int]:
    sys.path.insert(0, str(ROOT))
    from tests.test_ghc_family_lyren_v690_v1_final import LyrenV690V1FinalTests
    from tests.test_ghc_family_lyren_v690_v1_plan import LyrenV690V1PlanTests
    from tests.test_ghc_family_lyren_v690_v1_x1 import LyrenV690V1X1Tests
    from tests.test_ghc_family_lyren_v690_v1_x2 import LyrenV690V1X2Tests

    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(LyrenV690V1PlanTests))
    for name in loader.getTestCaseNames(LyrenV690V1X1Tests):
        if name != "test_strict_x1_before_x2":
            suite.addTest(LyrenV690V1X1Tests(name))
    suite.addTests(loader.loadTestsFromTestCase(LyrenV690V1X2Tests))
    suite.addTests(loader.loadTestsFromTestCase(LyrenV690V1FinalTests))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    failures = len(result.failures) + len(result.errors)
    if not result.wasSuccessful():
        raise RuntimeError(f"owner tests failed: {failures}")
    return result.testsRun, failures


def privacy_scan(blobs: dict[str, bytes]) -> tuple[int, dict[str, int], list[dict[str, str]]]:
    text_suffixes = {".json", ".md", ".html", ".py", ".yaml", ".yml", ".txt"}
    username = Path.home().name
    patterns = {
        "local_profile_path": re.compile(re.escape("C:\\\\Users\\\\" + username), re.IGNORECASE),
        "email_address": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
        "network_address": re.compile(r"(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])"),
        "credential_like_secret": re.compile(r"(?:api[_-]?key|secret|password)\s*[:=]\s*[A-Za-z0-9_-]{12,}", re.IGNORECASE),
        "contact_phone": re.compile(r"(?:phone|tel|mobile|contact)[^\n]{0,24}\+?[0-9][0-9 ()-]{7,}[0-9]", re.IGNORECASE),
    }
    counts = {name: 0 for name in patterns}
    candidates = []
    text_files = 0
    for path, data in blobs.items():
        if Path(path).suffix.lower() not in text_suffixes:
            continue
        text_files += 1
        text = data.decode("utf-8", errors="replace")
        for name, pattern in patterns.items():
            if pattern.search(text):
                counts[name] += 1
                candidates.append({"class": name, "path": path})
    return text_files, counts, candidates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt-dir", required=True)
    args = parser.parse_args()
    receipt_dir = Path(args.receipt_dir).resolve()
    marker = receipt_dir / "canonical-invocation.json"
    receipt = receipt_dir / "exact-final-owner-scoped-canonical.json"
    if marker.exists() or receipt.exists():
        raise SystemExit("canonical invocation or receipt already exists; refusing replay")
    write_json(
        marker,
        {
            "schema": "ghc.family.canonical-invocation-latch.v1",
            "owner": "Lyren Moss",
            "phase": "v690-v1",
            "expected_head": args.expected_head,
            "invoked_at_utc": datetime.now(UTC).isoformat(),
            "invocation_count": 1,
            "success_count": 0,
            "replay_count": 0,
            "state": "RUNNING",
        },
    )
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, observed: object) -> None:
        checks.append({"name": name, "passed": bool(condition), "observed": observed})
        if not condition:
            raise RuntimeError(f"canonical check failed: {name}: {observed}")

    try:
        head = command("git", "rev-parse", "HEAD").strip()
        check("exact_head", head == args.expected_head, head)
        check("clean_worktree", not command("git", "status", "--porcelain").strip(), command("git", "status", "--porcelain").strip())
        branch = command("git", "branch", "--show-current").strip()
        check("branch", branch == BRANCH, branch)
        upstream = command("git", "rev-parse", "@{upstream}").strip()
        tracking = command("git", "rev-parse", f"origin/{BRANCH}").strip()
        live_raw = command("git", "ls-remote", "origin", f"refs/heads/{BRANCH}").strip()
        live = live_raw.split()[0] if live_raw else ""
        check("four_way_equality", len({head, upstream, tracking, live}) == 1, {"local": head, "upstream": upstream, "tracking": tracking, "live": live})
        divergence = command("git", "rev-list", "--left-right", "--count", "@{upstream}...HEAD").strip().split()
        check("zero_divergence", divergence == ["0", "0"], divergence)
        commits = command("git", "rev-list", "--reverse", "HEAD").strip().splitlines()
        check("four_commits", len(commits) == 4, commits)
        check("lifecycle_commits", commits[:3] == [PLANNING, X1, X2], commits)
        check("final_parent", command("git", "rev-parse", "HEAD^").strip() == X2, command("git", "rev-parse", "HEAD^").strip())
        merges = command("git", "rev-list", "--merges", "HEAD").strip().splitlines()
        check("zero_merges", len(merges) == 0, merges)
        parents = [command("git", "show", "-s", "--format=%P", commit).strip().split() for commit in commits]
        check("single_parent_history", [len(row) for row in parents] == [0, 1, 1, 1], [len(row) for row in parents])

        blobs = git_blobs(head)
        check("owner_file_ceiling", len(blobs) < 2000, len(blobs))
        json_count = 0
        yaml_count = 0
        ast_count = 0
        for path, data in blobs.items():
            suffix = Path(path).suffix.lower()
            if suffix == ".json":
                json.loads(data)
                json_count += 1
            elif suffix in {".yaml", ".yml"}:
                yaml.safe_load(data.decode("utf-8"))
                yaml_count += 1
            elif suffix == ".py":
                ast.parse(data.decode("utf-8"), filename=path)
                ast_count += 1
        check("strict_json", json_count > 0, json_count)
        check("yaml_parses", yaml_count > 0, yaml_count)
        check("python_ast", ast_count > 0, ast_count)

        replay_counts = {
            "planning": manifest_replays(blobs, BASE + "plan/manifest.json"),
            "x1": manifest_replays(blobs, BASE + "x1/manifest.json"),
            "x2": manifest_replays(blobs, BASE + "x2/manifest.json"),
            "final": manifest_replays(blobs, BASE + "final/manifest.json"),
        }
        check("manifest_replays", all(value > 0 for value in replay_counts.values()), replay_counts)
        seal = json.loads(blobs[BASE + "final/content-seal.json"])
        for row in seal["entries"]:
            data = blobs[row["path"]]
            if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise RuntimeError(f"content seal mismatch: {row['path']}")
        check("content_seal", len(seal["entries"]) == seal["entry_count"], seal["entry_count"])

        baton = blobs[BASE + "final/hand-off-baton.md"].decode("utf-8")
        baton_words = len(re.findall(r"\b[\w'-]+\b", baton, flags=re.UNICODE))
        check("baton_word_range", 10_000 <= baton_words <= 100_000, baton_words)
        check("baton_eof", baton.rstrip().splitlines()[-1] == "EOF LYREN MOSS v690-v1 BATON.", baton.rstrip().splitlines()[-1])
        baton_manifest = json.loads(blobs[BASE + "final/baton-manifest.json"])
        check("baton_hash", hashlib.sha256(blobs[BASE + "final/hand-off-baton.md"]).hexdigest() == baton_manifest["combined"]["sha256"], baton_manifest["combined"]["sha256"])

        text_files, privacy_counts, candidates = privacy_scan(blobs)
        check("privacy_candidates", not candidates, {"files": text_files, "classes": privacy_counts, "candidates": candidates})
        route = json.loads(blobs[BASE + "final/route-candidate.json"])
        check("route_prepared_not_sent", route["state"] == "PREPARED_NOT_SENT" and not route["precontacted"], route)
        accounting = json.loads(blobs[BASE + "final/terminal-accounting.json"])
        terminal_counts = accounting["successor_visible_after_late_overlay"]
        check("terminal_counts", terminal_counts == {"effective_negatives": 977, "methods": 82, "direct_witnesses": 2487, "failed_witnesses": 688, "passing_witnesses": 1799}, terminal_counts)
        completion = json.loads(blobs[BASE + "final/completion-ledger.json"])
        check("four_outcomes", completion["core_outcomes"] == {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5}, completion["core_outcomes"])
        visual = json.loads(blobs[BASE + "final/visual-review.json"])
        check("visual_review", visual["result"] == "pass" and visual["pages_inspected"] == [1, 2, 3, 4, 5], visual)

        tests_run, test_failures = run_tests()
        check("owner_tests", test_failures == 0, {"tests": tests_run, "failures": test_failures})
        excluded_lint = {
            "scripts/build_ghc_family_lyren_v690_v1_plan.py",
            "tests/test_ghc_family_lyren_v690_v1_plan.py",
        }
        lint_paths = sorted(path for path in blobs if path.endswith(".py") and path not in excluded_lint)
        lint = subprocess.run(
            [sys.executable, "-m", "ruff", "check", *lint_paths],
            cwd=ROOT,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        check("exact_owner_python_lint", lint.returncode == 0, {"files": len(lint_paths), "stdout": lint.stdout, "stderr": lint.stderr, "historical_exclusions": sorted(excluded_lint)})
        check("clean_after", not command("git", "status", "--porcelain").strip(), command("git", "status", "--porcelain").strip())

        payload = {
            "schema": "ghc.family.exact-final-owner-scoped-canonical.v1",
            "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "owner": "Lyren Moss",
            "phase": "v690-v1",
            "branch": BRANCH,
            "source_provenance": SOURCE,
            "source_is_ancestor": False,
            "planning": PLANNING,
            "x1": X1,
            "x2": X2,
            "final": head,
            "invocation_count": 1,
            "success_count": 1,
            "replay_count": 0,
            "checks": checks,
            "counts": {
                "checks": len(checks),
                "tests": tests_run,
                "strict_json_parses": json_count,
                "yaml_parses": yaml_count,
                "python_ast_parses": ast_count,
                "owner_files": len(blobs),
                "text_privacy_files": text_files,
                "privacy_candidates": len(candidates),
                "manifest_replays": sum(replay_counts.values()),
                "content_seal_replays": seal["entry_count"],
                "baton_words": baton_words,
                "rendered_pages": len(visual["pages_inspected"]),
            },
            "manifest_layers": replay_counts,
            "privacy_classes": privacy_counts,
            "terminal_accounting": terminal_counts,
            "core_outcomes": completion["core_outcomes"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner_only": True,
            "full_repository_suite": False,
            "external_audit": False,
            "independent_reproduction": False,
            "complete_privacy_or_accessibility_assurance": False,
        }
        write_json(receipt, payload)
        write_json(
            marker,
            {
                "schema": "ghc.family.canonical-invocation-latch.v1",
                "owner": "Lyren Moss",
                "phase": "v690-v1",
                "expected_head": args.expected_head,
                "invoked_at_utc": load_marker_time(marker),
                "completed_at_utc": datetime.now(UTC).isoformat(),
                "invocation_count": 1,
                "success_count": 1,
                "replay_count": 0,
                "state": "SUCCEEDED_NO_REPLAY",
                "receipt": str(receipt),
            },
        )
        print(json.dumps({"status": payload["status"], "checks": len(checks), "tests": tests_run, "json": json_count, "manifests": sum(replay_counts.values()), "baton_words": baton_words}, sort_keys=True))
    except Exception as exc:
        marker_record = json.loads(marker.read_text(encoding="utf-8"))
        marker_record.update({"state": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT", "success_count": 0, "failure": str(exc), "completed_at_utc": datetime.now(UTC).isoformat()})
        write_json(marker, marker_record)
        raise


def load_marker_time(marker: Path) -> str:
    return json.loads(marker.read_text(encoding="utf-8"))["invoked_at_utc"]


if __name__ == "__main__":
    main()
