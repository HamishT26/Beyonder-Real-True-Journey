#!/usr/bin/env python3
"""One-shot exact-final canonical completion for Lyren Moss v666-v3."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import io
import json
import re
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v666-v3"
BRANCH = "codex/GHC-Family/lyren-moss-v666-v3-full-tools"
SOURCE_SHA = "96509c5b28628a6b62628dea277d1240b945b2ca"
X1_SHA = "e121ea6e207ea032edb1a0825ed86b1334481213"
EVIDENCE_SHA = "2ec494e75da11be4b8b18620f0ab10b68764ac69"
INITIAL_FINAL_SHA = "b7a389e1933432764874c9927488034f92d939a0"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{commit}:{path}"])


def replay(relative: str, commit: str) -> dict[str, Any]:
    manifest = load(relative)
    failures = []
    for entry in manifest["entries"]:
        try:
            raw = blob(commit, entry["path"])
        except subprocess.CalledProcessError as exc:
            failures.append({"path": entry["path"], "error": f"missing:{exc.returncode}"})
            continue
        if hashlib.sha256(raw).hexdigest() != entry["sha256"] or len(raw) != entry["size_bytes"]:
            failures.append({"path": entry["path"], "error": "sha_or_size"})
    return {"manifest": relative, "commit": commit, "entries": len(manifest["entries"]), "failures": failures, "valid": not failures}


def selected_suite() -> tuple[unittest.TestSuite, list[str], list[str]]:
    modules = [
        "tests.test_ghc_family_lyren_moss_v666_v3_x1",
        "tests.test_ghc_family_lyren_moss_v666_v3_x2",
        "tests.test_ghc_family_lyren_moss_v666_v3_evidence",
        "tests.test_ghc_family_lyren_moss_v666_v3_closeout",
    ]
    exclusions = {
        "tests.test_ghc_family_lyren_moss_v666_v3_x1.LyrenV666V3X1Tests.test_x2_and_later_paths_do_not_exist",
        "tests.test_ghc_family_lyren_moss_v666_v3_evidence.LyrenV666V3EvidenceTests.test_closeout_and_later_paths_absent",
    }
    suite = unittest.TestSuite()
    selected, excluded = [], []
    loader = unittest.TestLoader()
    for module_name in modules:
        discovered = loader.loadTestsFromModule(importlib.import_module(module_name))
        stack = list(discovered)
        while stack:
            test = stack.pop(0)
            if isinstance(test, unittest.TestSuite):
                stack[0:0] = list(test)
                continue
            test_id = test.id()
            if test_id in exclusions:
                excluded.append(test_id)
            else:
                selected.append(test_id)
                suite.addTest(test)
    return suite, selected, excluded


def owner_paths(final: str) -> list[str]:
    paths = git("ls-tree", "-r", "--name-only", final).splitlines()
    return sorted(path for path in paths if path.startswith("docs/lyren-moss/v666-v3/") or re.fullmatch(r"scripts/(?:build_)?ghc_family_lyren_moss_v666_v3[^/]*\.py", path) or re.fullmatch(r"tests/test_ghc_family_lyren_moss_v666_v3[^/]*\.py", path))


def canonical_payload(final: str) -> dict[str, Any]:
    local = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git("ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = git("rev-list", "--left-right", "--count", "@{upstream}...HEAD").split()
    clean = not git("status", "--porcelain=v1")
    phase_commits = int(git("rev-list", "--count", f"{SOURCE_SHA}..{final}"))
    merges_text = git("rev-list", "--merges", f"{SOURCE_SHA}..{final}")
    phase_rows = [row for row in git("rev-list", "--parents", f"{SOURCE_SHA}..{final}").splitlines() if row]
    parent_counts = [len(row.split()) - 1 for row in phase_rows]
    manifests = [
        replay("validation/x1-content-manifest.json", X1_SHA),
        replay("validation/evidence-content-manifest.json", EVIDENCE_SHA),
        replay("validation/final-delta-manifest.json", final),
        replay("validation/final-owner-manifest.json", final),
    ]
    suite, selected_ids, excluded_ids = selected_suite()
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    paths = owner_paths(final)
    json_failures, json_count = [], 0
    privacy_patterns = {
        "raw_task_or_thread_identifier": re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
        "session_identifier_value": re.compile(r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_callable_identifier_value": re.compile(r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
    }
    privacy_candidates, privacy_files = [], 0
    python_findings, python_files = [], 0
    for path in paths:
        raw = blob(final, path)
        if path.endswith(".json"):
            try:
                json.loads(raw.decode("utf-8"))
                json_count += 1
            except Exception as exc:
                json_failures.append({"path": path, "error": type(exc).__name__})
        if Path(path).suffix.casefold() in {".json", ".md", ".html", ".txt"}:
            text = raw.decode("utf-8")
            privacy_files += 1
            for class_name, pattern in privacy_patterns.items():
                if pattern.search(text):
                    privacy_candidates.append({"path": path, "class": class_name})
        if path.endswith(".py"):
            python_files += 1
            tree = ast.parse(raw.decode("utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    name = node.func.id if isinstance(node.func, ast.Name) else (f"{node.func.value.id}.{node.func.attr}" if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) else "")
                    if name in {"eval", "exec", "compile", "os.system", "pickle.loads", "yaml.load"}:
                        python_findings.append({"path": path, "line": node.lineno, "call": name})
                    for keyword in node.keywords:
                        if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                            python_findings.append({"path": path, "line": node.lineno, "call": "shell=True"})
    truth = load("closeout/phase-truth.json")
    route = load("orchestration/route-state-final-candidate.json")
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    detailed = {
        "exact_expected_head": local == final,
        "clean": clean,
        "four_way_equal": local == upstream == tracking == live == final,
        "zero_divergence": divergence == ["0", "0"],
        "source_to_final_four_commits": phase_commits == 4,
        "source_to_final_zero_merges": not merges_text,
        "all_phase_commits_single_parent": parent_counts == [1, 1, 1, 1],
        "x1_direct_child_source": git("rev-parse", f"{X1_SHA}^") == SOURCE_SHA,
        "evidence_direct_child_x1": git("rev-parse", f"{EVIDENCE_SHA}^") == X1_SHA,
        "initial_final_direct_child_evidence": git("rev-parse", f"{INITIAL_FINAL_SHA}^") == EVIDENCE_SHA,
        "corrected_final_direct_child_initial_final": git("rev-parse", f"{final}^") == INITIAL_FINAL_SHA,
        "all_manifests_replay": all(row["valid"] for row in manifests),
        "all_owner_json_parse": not json_failures,
        "five_class_privacy_zero_candidates": not privacy_candidates,
        "bounded_changed_python_zero_findings": not python_findings,
        "owner_materialization_below_2000": materialized < 2000,
        "truth_counts_exact": truth["outcome_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1} and truth["effective_negatives"] == 26395 and truth["effective_methods"] == 10937,
        "gaps_and_gates_exact": truth["open_gaps"] == 185 and truth["exact_gates"] == 183,
        "terminal_not_ready": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0 and not route["successor_contacted"],
        "complete_repository_suite_not_run": not truth["complete_repository_suite_run"],
        "same_owner_not_independent": not truth["same_owner_validation_is_independent_reproduction"],
    }
    minimal = {
        "selected_tests_pass": result.wasSuccessful(), "selected_tests_nonzero": len(selected_ids) > 0,
        "two_lifecycle_exclusions": len(excluded_ids) == 2, "exact_replacements_selected": all(any(name in item for item in selected_ids) for name in ("test_exact_replacement_immutable_x1_tree_has_no_later_paths", "test_exact_replacement_evidence_tree_has_no_terminal_paths")),
        "manifests_four": len(manifests) == 4, "manifest_failures_zero": all(not row["failures"] for row in manifests),
        "json_failures_zero": not json_failures, "privacy_candidates_zero": not privacy_candidates, "security_findings_zero": not python_findings,
        "four_way_equal": detailed["four_way_equal"], "history_exact": detailed["source_to_final_four_commits"] and detailed["source_to_final_zero_merges"] and detailed["all_phase_commits_single_parent"],
        "truth_exact": detailed["truth_counts_exact"], "protected_gates_retained": detailed["gaps_and_gates_exact"],
        "route_unsent": detailed["route_prepared_not_sent"], "not_stage_20": detailed["terminal_not_ready"],
    }
    return {
        "expected_final": final, "heads": {"local": local, "upstream": upstream, "tracking": tracking, "fresh_live": live}, "divergence": {"behind": int(divergence[0]), "ahead": int(divergence[1])},
        "history": {"source": SOURCE_SHA, "x1": X1_SHA, "evidence": EVIDENCE_SHA, "retained_nonterminal_initial_final": INITIAL_FINAL_SHA, "corrected_final": final, "phase_commit_count": phase_commits, "merge_count": 0 if not merges_text else len(merges_text.splitlines()), "parent_counts": parent_counts},
        "tests": {"selected_count": len(selected_ids), "selected_ids": selected_ids, "excluded_zero_credit_count": len(excluded_ids), "excluded_ids": excluded_ids, "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped), "successful": result.wasSuccessful(), "output": stream.getvalue()},
        "manifests": manifests, "manifest_entry_total": sum(row["entries"] for row in manifests),
        "json": {"parsed": json_count, "failures": json_failures}, "privacy": {"classes": list(privacy_patterns), "files": privacy_files, "candidates": privacy_candidates, "confirmed_hits": len(privacy_candidates), "claim_boundary": "bounded five-class owner-text scan only; not privacy-complete"},
        "security": {"python_files": python_files, "findings": python_findings, "claim_boundary": "bounded AST scan only; not exhaustive security"},
        "materialized_files": materialized, "owner_file_count": len(paths), "detailed_checks": detailed, "detailed_passed": sum(detailed.values()), "detailed_total": len(detailed),
        "minimal_checks": minimal, "minimal_passed": sum(minimal.values()), "minimal_total": len(minimal),
        "complete_repository_suite_run": False, "independent_reproduction": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt-dir", required=True)
    args = parser.parse_args()
    receipt_dir = Path(args.receipt_dir).resolve()
    receipt_dir.mkdir(parents=True, exist_ok=True)
    state_path = receipt_dir / f"canonical-state-{args.expected_final}.json"
    receipt_path = receipt_dir / f"canonical-completion-{args.expected_final}.json"
    if state_path.exists() or receipt_path.exists():
        raise SystemExit("canonical invocation already recorded; replay refused")
    state = {"schema": "ghc.family.lyren-moss.v666-v3.canonical-state.v1", "owner": "Lyren Moss", "phase": "v666-v3", "expected_final": args.expected_final, "invocation_count": 1, "success_count": 0, "post_success_replay": False, "status": "invoked", "invoked_at_utc": now()}
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    try:
        payload = canonical_payload(args.expected_final)
        success = payload["tests"]["successful"] and all(payload["detailed_checks"].values()) and all(payload["minimal_checks"].values())
        canonical_bytes = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        receipt = {"schema": "ghc.family.lyren-moss.v666-v3.canonical-completion-receipt.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": now(), "invocation_count": 1, "success_count": 1 if success else 0, "post_success_replay": False, "success": success, "canonical_payload_sha256": hashlib.sha256(canonical_bytes).hexdigest(), "payload": payload}
    except Exception as exc:
        receipt = {"schema": "ghc.family.lyren-moss.v666-v3.canonical-completion-receipt.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": now(), "invocation_count": 1, "success_count": 0, "post_success_replay": False, "success": False, "exception": {"type": type(exc).__name__, "message": str(exc)}}
    receipt_text = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    receipt_path.write_text(receipt_text, encoding="utf-8", newline="\n")
    state.update({"success_count": 1 if receipt["success"] else 0, "status": "success" if receipt["success"] else "failed", "completed_at_utc": now(), "receipt_sha256": hashlib.sha256(receipt_text.encode("utf-8")).hexdigest()})
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"success": receipt["success"], "receipt_sha256": state["receipt_sha256"], "canonical_payload_sha256": receipt.get("canonical_payload_sha256"), "selected_tests": receipt.get("payload", {}).get("tests", {}).get("selected_count"), "detailed": [receipt.get("payload", {}).get("detailed_passed"), receipt.get("payload", {}).get("detailed_total")], "minimal": [receipt.get("payload", {}).get("minimal_passed"), receipt.get("payload", {}).get("minimal_total")], "manifest_entries": receipt.get("payload", {}).get("manifest_entry_total"), "json_parsed": receipt.get("payload", {}).get("json", {}).get("parsed"), "privacy_files": receipt.get("payload", {}).get("privacy", {}).get("files"), "security_python_files": receipt.get("payload", {}).get("security", {}).get("python_files")}, sort_keys=True))
    if not receipt["success"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
