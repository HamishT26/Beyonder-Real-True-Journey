"""Run the one-shot v690-v2 dependency-corrected exact-final composite."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any

import yaml

from scripts.ghc_family_ilyra_v690_v2_canonical import (
    BASE,
    BRANCH,
    PLANNING,
    SOURCE,
    X1,
    X2,
    blobs,
    command,
    privacy_scan,
    replay_manifest,
    run_tests,
    write_json,
)

ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY_FAILED_FINAL = "a53241d465e2236f79375db2fdff04117e1e6a04"
CORRECTION_PATH = BASE + "correction/dependency-correction.json"
COMPOSITE_PATH = "scripts/ghc_family_ilyra_v690_v2_dependency_corrected_composite.py"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt-dir", required=True)
    args = parser.parse_args()
    expected = args.expected_head
    receipt_dir = Path(args.receipt_dir).resolve()
    marker = receipt_dir / "dependency-corrected-composite-invocation.json"
    receipt = receipt_dir / "dependency-corrected-exact-final-owner-scoped-composite.json"
    if marker.exists() or receipt.exists():
        raise SystemExit("dependency-corrected composite latch exists; refusing replay")
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
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any) -> None:
        checks.append({"name": name, "observed": observed, "passed": bool(passed)})
        if not passed:
            raise RuntimeError(f"composite check failed: {name}: {observed}")

    try:
        head = command("git", "rev-parse", "HEAD").strip()
        branch = command("git", "branch", "--show-current").strip()
        check("exact_head", head == expected, head)
        check("branch", branch == BRANCH, branch)
        status_before = command("git", "status", "--porcelain=v1")
        check("clean_before", status_before.strip() == "", status_before)
        upstream = command("git", "rev-parse", "@{upstream}").strip()
        tracking = command(
            "git", "rev-parse", "refs/remotes/origin/codex/GHC-Family/ilyra-fen-main"
        ).strip()
        live_line = command(
            "git",
            "ls-remote",
            "--heads",
            "origin",
            "refs/heads/codex/GHC-Family/ilyra-fen-main",
        ).strip()
        live = live_line.split("\t")[0]
        equality = {
            "live": live,
            "local": head,
            "tracking": tracking,
            "upstream": upstream,
        }
        check("four_way_equality", len(set(equality.values())) == 1, equality)
        divergence = command(
            "git", "rev-list", "--left-right", "--count", "HEAD...@{upstream}"
        ).strip().split()
        check("zero_divergence", divergence == ["0", "0"], divergence)
        history = list(reversed(command("git", "rev-list", head).splitlines()))
        check(
            "five_commit_history",
            history == [PLANNING, X1, X2, DEPENDENCY_FAILED_FINAL, head],
            history,
        )
        final_parent = command("git", "show", "-s", "--format=%P", head).strip()
        check("correction_parent", final_parent == DEPENDENCY_FAILED_FINAL, final_parent)
        merges = command("git", "rev-list", "--merges", head)
        check("zero_merges", merges.strip() == "", merges)
        delta = command(
            "git", "diff", "--name-only", DEPENDENCY_FAILED_FINAL + ".." + head
        ).splitlines()
        check("correction_delta", delta == [CORRECTION_PATH, COMPOSITE_PATH], delta)

        layers = {
            PLANNING: blobs(PLANNING),
            X1: blobs(X1),
            X2: blobs(X2),
            DEPENDENCY_FAILED_FINAL: blobs(DEPENDENCY_FAILED_FINAL),
            head: blobs(head),
        }
        manifest_counts = {
            "planning": replay_manifest(layers[PLANNING], BASE + "plan/manifest.json"),
            "x1": replay_manifest(layers[X1], BASE + "x1/manifest.json"),
            "x2": replay_manifest(layers[X2], BASE + "x2/manifest.json"),
            "final": replay_manifest(
                layers[DEPENDENCY_FAILED_FINAL], BASE + "final/manifest.json"
            ),
        }
        check(
            "manifest_replays",
            all(value > 0 for value in manifest_counts.values()),
            manifest_counts,
        )
        seal = json.loads(
            layers[DEPENDENCY_FAILED_FINAL][BASE + "final/content-seal.json"]
        )
        for row in seal["entries"]:
            data = layers[DEPENDENCY_FAILED_FINAL][row["path"]]
            if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise RuntimeError(f"content seal mismatch: {row['path']}")
        check("immutable_content_seal", len(seal["entries"]) == seal["entry_count"], seal["entry_count"])

        correction = json.loads(layers[head][CORRECTION_PATH])
        check(
            "failed_canonical_retained",
            correction["canonical_failure"]["success_count"] == 0
            and correction["canonical_failure"]["replay_count"] == 0,
            correction["canonical_failure"],
        )
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
        check(
            "privacy_candidates",
            not candidates,
            {"candidates": candidates, "classes": privacy_counts, "files": text_files},
        )

        baton = layers[head][BASE + "final/hand-off-baton.md"]
        baton_manifest = json.loads(layers[head][BASE + "final/baton-manifest.json"])
        baton_text = baton.decode("utf-8")
        baton_words = len(re.findall(r"\b[\w'-]+\b", baton_text))
        check(
            "baton_hash",
            hashlib.sha256(baton).hexdigest() == baton_manifest["combined"]["sha256"],
            baton_manifest["combined"]["sha256"],
        )
        check("baton_word_range", 10_000 <= baton_words <= 100_000, baton_words)
        check(
            "baton_eof",
            baton_text.splitlines()[-1] == "EOF ILYRA FEN v690-v2 BATON.",
            baton_text.splitlines()[-1],
        )
        final_root = ROOT / BASE / "final"
        check("docx_open", zipfile.is_zipfile(final_root / "overview.docx"), "overview.docx")
        review = json.loads(layers[head][BASE + "final/visual-review.json"])
        check(
            "rendered_pages",
            review["pages"] >= 3
            and all(
                (final_root / "rendered" / f"page-{page}.png").is_file()
                for page in review["pages_inspected"]
            ),
            review,
        )
        tests_run, test_failures = run_tests()
        check(
            "owner_tests",
            test_failures == 0,
            {"failures": test_failures, "tests": tests_run},
        )
        terminal = json.loads(
            layers[head][BASE + "final/terminal-accounting.json"]
        )["effective_total"]
        outcomes = json.loads(
            layers[head][BASE + "final/completion-ledger.json"]
        )["core_outcomes"]
        check(
            "four_outcomes",
            outcomes
            == {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5},
            outcomes,
        )
        status_after = command("git", "status", "--porcelain=v1")
        check("clean_after", status_after.strip() == "", status_after)
        retained_correction_failures = len(correction["retained_failures"])
        overlay = {
            "direct_witnesses": terminal["direct_witnesses"]
            + retained_correction_failures * 2,
            "effective_negatives": terminal["effective_negatives"]
            + retained_correction_failures,
            "failed_witnesses": terminal["failed_witnesses"]
            + retained_correction_failures,
            "methods": terminal["methods"] + retained_correction_failures,
            "passing_witnesses": terminal["passing_witnesses"]
            + retained_correction_failures,
        }
        payload = {
            "branch": BRANCH,
            "canonical_success_count": 0,
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
            "dependency_failed_final": DEPENDENCY_FAILED_FINAL,
            "external_audit": False,
            "final": head,
            "full_repository_suite": False,
            "independent_reproduction": False,
            "invocation_count": 1,
            "manifest_layers": manifest_counts,
            "owner": "Ilyra Fen",
            "phase": "v690-v2",
            "privacy_classes": privacy_counts,
            "replay_count": 0,
            "same_owner_only": True,
            "schema": "ghc.family.dependency-corrected-exact-final-owner-scoped-composite.v1",
            "source_is_ancestor": False,
            "source_provenance": SOURCE,
            "status": "VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_OWNER_SCOPED_COMPOSITE",
            "success_count": 1,
            "successor_visible_overlay": overlay,
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
                "replay_count": 0,
                "state": "SUCCEEDED_NO_REPLAY",
                "success_count": 1,
            },
        )
        print(
            json.dumps(
                {
                    "baton_words": baton_words,
                    "checks": len(checks),
                    "json": json_count,
                    "manifests": sum(manifest_counts.values()),
                    "status": payload["status"],
                    "tests": tests_run,
                    "yaml": yaml_count,
                },
                sort_keys=True,
            )
        )
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
                "state": "FAILED_RETAINED_ZERO_COMPOSITE_SUCCESS_CREDIT",
                "success_count": 0,
            },
        )
        raise


if __name__ == "__main__":
    main()
