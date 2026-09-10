"""Run Ilyra v690-v2 exact-final owner-scoped canonical validation once."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = "docs/ilyra-fen/v690-v2/"
BRANCH = "codex/GHC-Family/ilyra-fen-main"
PLANNING = "8c4eef447c296e4d956c75ff16e6205bf842df0b"
X1 = "8e2a010330d4e31486dd3059ed1be9e2e744f9c1"
X2 = "e85f3a2cfe5260ff2b9d6e953a80513d383650c5"
SOURCE = "9936e2855b72bddfecdea77abdd6f083f14a09f1"


def command(*args: str, text: bool = True) -> Any:
    return subprocess.check_output(args, cwd=ROOT, text=text)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def blobs(commit: str) -> dict[str, bytes]:
    raw = command("git", "ls-tree", "-r", "-z", "--format=%(objectname)%x09%(path)", commit, text=False)
    entries = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        object_id, encoded_path = record.split(b"\t", 1)
        entries.append((object_id.decode("ascii"), encoded_path.decode("utf-8")))
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    result: dict[str, bytes] = {}
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
        result[path] = data
    process.stdin.close()
    if process.wait(timeout=60) != 0:
        assert process.stderr is not None
        raise RuntimeError(process.stderr.read().decode("utf-8", errors="replace"))
    return result


def replay_manifest(layer: dict[str, bytes], manifest_path: str) -> int:
    manifest = json.loads(layer[manifest_path])
    for row in manifest["entries"]:
        data = layer[row["path"]]
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise RuntimeError(f"manifest mismatch: {manifest_path}: {row['path']}")
    return len(manifest["entries"])


def privacy_scan(layer: dict[str, bytes]) -> tuple[int, dict[str, int], list[dict[str, str]]]:
    suffixes = {".json", ".md", ".html", ".py", ".yaml", ".yml", ".txt"}
    patterns = {
        "local_profile_path": re.compile(r"C:\\\\Users\\\\hamis", re.IGNORECASE),
        "email_address": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
        "network_address": re.compile(r"(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])"),
        "credential_like_secret": re.compile(
            r"(?:api[_-]?key|secret|password)\s*[:=]\s*[A-Za-z0-9_-]{12,}", re.IGNORECASE
        ),
        "contact_phone": re.compile(
            r"(?:phone|tel|mobile|contact)[^\n]{0,24}\+?[0-9][0-9 ()-]{7,}[0-9]",
            re.IGNORECASE,
        ),
    }
    counts = {name: 0 for name in patterns}
    candidates = []
    text_files = 0
    for path, data in layer.items():
        if not path.startswith(BASE) and not path.startswith(
            ("scripts/ghc_family_obligation_graph_", "scripts/ghc_family_ilyra_v690_v2_", "tests/test_ghc_family_ilyra_v690_v2_")
        ):
            continue
        if Path(path).suffix.lower() not in suffixes:
            continue
        text_files += 1
        text = data.decode("utf-8", errors="ignore")
        for name, pattern in patterns.items():
            for match in pattern.finditer(text):
                counts[name] += 1
                candidates.append({"class": name, "path": path, "sample_sha256": hashlib.sha256(match.group().encode()).hexdigest()})
    return text_files, counts, candidates


def run_tests() -> tuple[int, int]:
    sys.path.insert(0, str(ROOT))
    from tests.test_ghc_family_ilyra_v690_v2_final import IlyraV690V2FinalTests
    from tests.test_ghc_family_ilyra_v690_v2_plan import IlyraV690V2PlanTests
    from tests.test_ghc_family_ilyra_v690_v2_x1 import IlyraV690V2X1Tests
    from tests.test_ghc_family_ilyra_v690_v2_x2 import IlyraV690V2X2Tests

    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    for name in loader.getTestCaseNames(IlyraV690V2PlanTests):
        if name != "test_planning_only_no_production_evaluator":
            suite.addTest(IlyraV690V2PlanTests(name))
    for name in loader.getTestCaseNames(IlyraV690V2X1Tests):
        if name not in {"test_x2_is_absent_at_x1", "test_x1_manifest_raw_worktree_bytes"}:
            suite.addTest(IlyraV690V2X1Tests(name))
    suite.addTests(loader.loadTestsFromTestCase(IlyraV690V2X2Tests))
    suite.addTests(loader.loadTestsFromTestCase(IlyraV690V2FinalTests))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    failures = len(result.failures) + len(result.errors)
    if not result.wasSuccessful():
        raise RuntimeError(f"owner tests failed: {failures}")
    return result.testsRun, failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt-dir", required=True)
    args = parser.parse_args()
    expected = args.expected_head
    receipt_dir = Path(args.receipt_dir).resolve()
    marker = receipt_dir / "canonical-invocation.json"
    receipt = receipt_dir / "exact-final-owner-scoped-canonical.json"
    if marker.exists() or receipt.exists():
        raise SystemExit("canonical invocation or receipt already exists; refusing replay")
    write_json(
        marker,
        {
            "expected_head": expected,
            "invocation_count": 1,
            "owner": "Ilyra Fen",
            "phase": "v690-v2",
            "replay_count": 0,
            "state": "STARTED",
        },
    )
    checks = []

    def check(name: str, passed: bool, observed: Any) -> None:
        checks.append({"name": name, "observed": observed, "passed": bool(passed)})
        if not passed:
            raise RuntimeError(f"canonical check failed: {name}: {observed}")

    try:
        head = command("git", "rev-parse", "HEAD").strip()
        check("exact_head", head == expected, head)
        check("branch", command("git", "branch", "--show-current").strip() == BRANCH, command("git", "branch", "--show-current").strip())
        check("clean_before", command("git", "status", "--porcelain=v1").strip() == "", command("git", "status", "--porcelain=v1"))
        upstream = command("git", "rev-parse", "@{upstream}").strip()
        tracking = command("git", "rev-parse", "refs/remotes/origin/codex/GHC-Family/ilyra-fen-main").strip()
        live_line = command("git", "ls-remote", "--heads", "origin", "refs/heads/codex/GHC-Family/ilyra-fen-main").strip()
        live = live_line.split("\t")[0]
        check("four_way_equality", len({head, upstream, tracking, live}) == 1, {"local": head, "upstream": upstream, "tracking": tracking, "live": live})
        divergence = command("git", "rev-list", "--left-right", "--count", "HEAD...@{upstream}").strip().split()
        check("zero_divergence", divergence == ["0", "0"], divergence)
        history = list(reversed(command("git", "rev-list", head).splitlines()))
        check("four_commits", history == [PLANNING, X1, X2, head], history)
        check("final_parent", command("git", "show", "-s", "--format=%P", head).strip() == X2, command("git", "show", "-s", "--format=%P", head).strip())
        check("zero_merges", command("git", "rev-list", "--merges", head).strip() == "", command("git", "rev-list", "--merges", head))
        layers = {PLANNING: blobs(PLANNING), X1: blobs(X1), X2: blobs(X2), head: blobs(head)}
        manifest_counts = {
            "planning": replay_manifest(layers[PLANNING], BASE + "plan/manifest.json"),
            "x1": replay_manifest(layers[X1], BASE + "x1/manifest.json"),
            "x2": replay_manifest(layers[X2], BASE + "x2/manifest.json"),
            "final": replay_manifest(layers[head], BASE + "final/manifest.json"),
        }
        check("manifest_replays", all(value > 0 for value in manifest_counts.values()), manifest_counts)
        seal = json.loads(layers[head][BASE + "final/content-seal.json"])
        for row in seal["entries"]:
            data = layers[head][row["path"]]
            if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise RuntimeError(f"content seal mismatch: {row['path']}")
        check("content_seal", len(seal["entries"]) == seal["entry_count"], seal["entry_count"])
        owner_paths = [
            path
            for path in layers[head]
            if path.startswith(
                (
                    BASE,
                    "scripts/ghc_family_obligation_graph_",
                    "scripts/ghc_family_ilyra_v690_v2_",
                    "scripts/build_ghc_family_ilyra_v690_v2_",
                    "tests/test_ghc_family_ilyra_v690_v2_",
                )
            )
            or path in {".gitattributes", ".gitignore"}
        ]
        check("owner_file_ceiling", len(owner_paths) < 2000, len(owner_paths))
        json_count = 0
        yaml_count = 0
        ast_count = 0
        for path in owner_paths:
            data = layers[head][path]
            if path.endswith(".json"):
                json.loads(data)
                json_count += 1
            elif path.endswith((".yaml", ".yml")):
                yaml.safe_load(data)
                yaml_count += 1
            elif path.endswith(".py"):
                ast.parse(data.decode("utf-8"))
                ast_count += 1
        check("strict_json", json_count > 0, json_count)
        check("yaml_parses", yaml_count > 0, yaml_count)
        check("python_ast", ast_count > 0, ast_count)
        text_files, privacy_counts, candidates = privacy_scan(layers[head])
        check("privacy_candidates", not candidates, {"files": text_files, "classes": privacy_counts, "candidates": candidates})
        baton = layers[head][BASE + "final/hand-off-baton.md"].decode("utf-8")
        baton_manifest = json.loads(layers[head][BASE + "final/baton-manifest.json"])
        baton_words = len(re.findall(r"\b[\w'-]+\b", baton, flags=re.UNICODE))
        check("baton_hash", hashlib.sha256(baton.encode("utf-8")).hexdigest() == baton_manifest["combined"]["sha256"], baton_manifest["combined"]["sha256"])
        check("baton_word_range", 10_000 <= baton_words <= 100_000, baton_words)
        check("baton_eof", baton.splitlines()[-1] == "EOF ILYRA FEN v690-v2 BATON.", baton.splitlines()[-1])
        final_root = ROOT / BASE / "final"
        check("docx_open", zipfile.is_zipfile(final_root / "overview.docx"), str(final_root / "overview.docx"))
        review = json.loads(layers[head][BASE + "final/visual-review.json"])
        check("rendered_pages", review["pages"] >= 3 and all((final_root / "rendered" / f"page-{page}.png").is_file() for page in review["pages_inspected"]), review)
        tests_run, test_failures = run_tests()
        check("owner_tests", test_failures == 0, {"tests": tests_run, "failures": test_failures})
        terminal = json.loads(layers[head][BASE + "final/terminal-accounting.json"])["effective_total"]
        outcomes = json.loads(layers[head][BASE + "final/completion-ledger.json"])["core_outcomes"]
        check("terminal_counts", all(value >= 0 for value in terminal.values()), terminal)
        check("four_outcomes", outcomes == {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5}, outcomes)
        check("clean_after", command("git", "status", "--porcelain=v1").strip() == "", command("git", "status", "--porcelain=v1"))
        payload = {
            "branch": BRANCH,
            "checks": checks,
            "complete_privacy_or_accessibility_assurance": False,
            "core_outcomes": outcomes,
            "counts": {
                "baton_words": baton_words,
                "checks": len(checks),
                "content_seal_replays": seal["entry_count"],
                "manifest_replays": sum(manifest_counts.values()),
                "owner_files": len(owner_paths),
                "python_ast_parses": ast_count,
                "strict_json_parses": json_count,
                "tests": tests_run,
                "text_privacy_files": text_files,
                "yaml_parses": yaml_count,
            },
            "external_audit": False,
            "final": head,
            "full_repository_suite": False,
            "independent_reproduction": False,
            "invocation_count": 1,
            "manifest_layers": manifest_counts,
            "owner": "Ilyra Fen",
            "phase": "v690-v2",
            "planning": PLANNING,
            "privacy_classes": privacy_counts,
            "replay_count": 0,
            "same_owner_only": True,
            "schema": "ghc.family.exact-final-owner-scoped-canonical.v1",
            "source_is_ancestor": False,
            "source_provenance": SOURCE,
            "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "success_count": 1,
            "terminal_accounting": terminal,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "x1": X1,
            "x2": X2,
        }
        write_json(receipt, payload)
        write_json(
            marker,
            {
                "completed": True,
                "expected_head": expected,
                "invocation_count": 1,
                "owner": "Ilyra Fen",
                "phase": "v690-v2",
                "receipt": str(receipt).replace(str(Path.home()), "[local-user]"),
                "replay_count": 0,
                "state": "SUCCEEDED_NO_REPLAY",
                "success_count": 1,
            },
        )
        print(json.dumps({"status": payload["status"], "checks": len(checks), "tests": tests_run, "json": json_count, "yaml": yaml_count, "manifests": sum(manifest_counts.values()), "baton_words": baton_words}, sort_keys=True))
    except Exception as exc:
        write_json(
            marker,
            {
                "error": str(exc),
                "expected_head": expected,
                "invocation_count": 1,
                "owner": "Ilyra Fen",
                "phase": "v690-v2",
                "replay_count": 0,
                "state": "FAILED_RETAINED_ZERO_SUCCESS_CREDIT",
                "success_count": 0,
            },
        )
        raise


if __name__ == "__main__":
    main()
