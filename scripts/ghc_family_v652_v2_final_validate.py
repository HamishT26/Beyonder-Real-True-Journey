#!/usr/bin/env python3
"""Run the single authorized exact-final canonical v652-v2 validation pass."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
PHASE_ROOT = "docs/orin-thale/v652-v2"
SOURCE = "f168bcb798715d61d8b0a9ec2c6646a7af09ce29"
X1 = "3f5b49dc1a380452593c8080c3ae134e654c2079"
EVIDENCE = "d185405470b9205a21d9b018bc0d3f7f44f49444"
CLOSEOUT = "0053eef587ebdc88d8bafbf09b2f214737abd539"
BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"


def git(*args: str, binary: bool = False, check: bool = True) -> str | bytes:
    proc = subprocess.run(["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout if binary else proc.stdout.decode("utf-8").strip()


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=REPO, input="".join(oid + "\n" for oid in unique).encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    stream = io.BytesIO(proc.stdout)
    result: dict[str, bytes] = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode().split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected blob header: {header}")
        size = int(header[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing batch frame terminator")
        result[expected] = data
    if stream.read():
        raise RuntimeError("unexpected trailing batch output")
    return result


def tree_map(commit: str, prefix: str | None = None) -> dict[str, str]:
    args = ["ls-tree", "-r", "-z", commit]
    if prefix:
        args.extend(["--", prefix])
    raw = git(*args, binary=True)
    assert isinstance(raw, bytes)
    result: dict[str, str] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        _mode, kind, oid = meta.decode().split()
        if kind == "blob":
            result[path.decode("utf-8")] = oid
    return result


def load_at(commit: str, path: str) -> Any:
    return json.loads(str(git("show", f"{commit}:{path}")))


def manifest_check(commit: str, path: str, expected_paths: set[str], tree: dict[str, str], blobs: dict[str, bytes]) -> dict[str, Any]:
    manifest = load_at(commit, path)
    declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    issues = []
    if declared != expected_paths:
        issues.append({"kind": "path_set", "missing": sorted(expected_paths - declared), "extra": sorted(declared - expected_paths)})
    for row in manifest["entries"]:
        oid = tree.get(row["path"])
        data = blobs.get(row["git_blob"])
        if oid != row["git_blob"] or data is None or len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            issues.append({"kind": "entry", "path": row["path"]})
    return {"path": path, "entry_count": len(manifest["entries"]), "self_exclusion_count": len(manifest["self_exclusions"]), "expected_path_count": len(expected_paths), "issues": issues, "valid": not issues}


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def selected_tests() -> tuple[unittest.TestSuite, dict[str, Any]]:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    patterns = [
        "test_ghc_family_v652_v1_x1.py",
        "test_ghc_family_v652_v1_x2.py",
        "test_ghc_family_v652_v2_x1.py",
        "test_ghc_family_v652_v2.py",
        "test_ghc_family_v652_v2_closeout.py",
    ]
    counts = {}
    loader_errors = []
    for index, pattern in enumerate(patterns, 1):
        path = REPO / "tests" / pattern
        module_name = f"ghc_family_v652_v2_selected_{index}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot create module spec for {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        discovered = loader.loadTestsFromModule(module)
        count = sum(1 for _ in flatten(discovered))
        counts[pattern] = count
        suite.addTests(discovered)
        loader_errors.extend(loader.errors)
        loader.errors.clear()
    return suite, {"patterns": patterns, "counts": counts, "raw_count": sum(counts.values()), "eligible_count": sum(counts.values()), "inherited_closeout_exclusions": 7, "loader_errors": loader_errors}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    head = str(git("rev-parse", "HEAD"))
    clean_before = str(git("status", "--porcelain=v1")) == ""
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed})

    suite, selection = selected_tests()
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    test_valid = selection["eligible_count"] == 39 and not selection["loader_errors"] and result.testsRun == 39 and not result.failures and not result.errors
    check("scoped_test_selection", test_valid, {"selection": selection, "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "output": stream.getvalue()[-2000:]})

    phase_tree = tree_map(head, PHASE_ROOT)
    owner_paths = set(str(git("diff", "--name-only", f"{SOURCE}..{head}")).splitlines())
    full_tree = tree_map(head)
    all_needed_oids = list(phase_tree.values())
    for manifest_commit, manifest_path in (
        (X1, f"{PHASE_ROOT}/validation/x1-staged-manifest.json"),
        (EVIDENCE, f"{PHASE_ROOT}/validation/evidence-staged-manifest.json"),
        (CLOSEOUT, f"{PHASE_ROOT}/validation/closeout-delta-manifest.json"),
        (CLOSEOUT, f"{PHASE_ROOT}/validation/final-owner-manifest.json"),
        (head, f"{PHASE_ROOT}/validation/correction-delta-manifest.json"),
        (head, f"{PHASE_ROOT}/validation/corrected-owner-manifest.json"),
    ):
        manifest = load_at(manifest_commit, manifest_path)
        all_needed_oids.extend(row["git_blob"] for row in manifest["entries"])
    blobs = batch_blobs(all_needed_oids)

    json_errors = []
    json_count = 0
    for path, oid in phase_tree.items():
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(blobs[oid].decode("utf-8"))
            except Exception as exc:  # noqa: BLE001
                json_errors.append({"path": path, "error": str(exc)})
    check("complete_phase_json", not json_errors, {"parsed": json_count, "errors": json_errors})

    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definition_paths = {
        "scripts/build_ghc_family_v652_v2_preregistration.py", "scripts/ghc_family_v652_v2_x1_validate.py",
        "scripts/ghc_family_v652_v2_evidence_validate.py", "scripts/ghc_family_v652_v2_closeout_review.py",
        "scripts/ghc_family_v652_v2_final_validate.py", f"{PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{PHASE_ROOT}/validation/evidence-staged-privacy.json", f"{PHASE_ROOT}/validation/closeout-staged-privacy.json",
        f"{PHASE_ROOT}/validation/correction-staged-privacy.json",
    }
    privacy_candidates, privacy_hits = [], []
    for path in sorted(owner_paths):
        oid = full_tree[path]
        data = blobs.get(oid)
        if data is None:
            data = batch_blobs([oid])[oid]
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition" if path in definition_paths else "confirmed_payload_hit"
                row = {"path": path, "pattern_class": name, "disposition": disposition}
                privacy_candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    privacy_hits.append(row)
    check("five_class_privacy_scan", not privacy_hits, {"scanned": len(owner_paths), "candidates": len(privacy_candidates), "confirmed_hits": privacy_hits})

    x1_paths = set(str(git("diff-tree", "--no-commit-id", "--name-only", "-r", X1)).splitlines())
    evidence_paths = set(str(git("diff-tree", "--no-commit-id", "--name-only", "-r", EVIDENCE)).splitlines())
    closeout_paths = set(str(git("diff-tree", "--no-commit-id", "--name-only", "-r", CLOSEOUT)).splitlines())
    closeout_owner_paths = set(str(git("diff", "--name-only", f"{SOURCE}..{CLOSEOUT}")).splitlines())
    correction_paths = set(str(git("diff-tree", "--no-commit-id", "--name-only", "-r", head)).splitlines())
    manifests = [
        manifest_check(X1, f"{PHASE_ROOT}/validation/x1-staged-manifest.json", x1_paths, tree_map(X1), blobs),
        manifest_check(EVIDENCE, f"{PHASE_ROOT}/validation/evidence-staged-manifest.json", evidence_paths, tree_map(EVIDENCE), blobs),
        manifest_check(CLOSEOUT, f"{PHASE_ROOT}/validation/closeout-delta-manifest.json", closeout_paths, tree_map(CLOSEOUT), blobs),
        manifest_check(CLOSEOUT, f"{PHASE_ROOT}/validation/final-owner-manifest.json", closeout_owner_paths, tree_map(CLOSEOUT), blobs),
        manifest_check(head, f"{PHASE_ROOT}/validation/correction-delta-manifest.json", correction_paths, full_tree, blobs),
        manifest_check(head, f"{PHASE_ROOT}/validation/corrected-owner-manifest.json", owner_paths, full_tree, blobs),
    ]
    check("manifest_parity", all(row["valid"] for row in manifests), manifests)

    truth = load_at(head, f"{PHASE_ROOT}/final/phase-truth.json")
    negatives = load_at(head, f"{PHASE_ROOT}/final/retained-negative-register.json")
    method = load_at(head, f"{PHASE_ROOT}/method-flow/method-flow-ledger.json")
    outcomes = load_at(head, f"{PHASE_ROOT}/evidence/outcome-ledger.json")
    gaps = load_at(head, f"{PHASE_ROOT}/final/open-gap-register.json")
    gates = load_at(head, f"{PHASE_ROOT}/final/exact-gate-register.json")
    route = load_at(head, f"{PHASE_ROOT}/route/terminal-route-state.json")
    seats = load_at(head, f"{PHASE_ROOT}/provenance/future-cli-placeholder-invariant.json")
    review = load_at(head, f"{PHASE_ROOT}/validation/correction-staged-review.json")
    build = load_at(head, f"{PHASE_ROOT}/validation/closeout-build-receipt.json")

    check("outcome_truth", outcomes["counts"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1} and outcomes["proposal_count"] == 30, outcomes["counts"])
    check("negative_retention", negatives["effective_at_final"] == 8203 and negatives["closeout_operational_count"] == 6 and negatives["terminal_operational_count"] == 1 and negatives["no_failure_erased"], {"effective": negatives["effective_at_final"], "closeout": negatives["closeout_operational_count"], "terminal": negatives["terminal_operational_count"]})
    check("method_flow", method["counts"]["methods"] == 28 and method["counts"]["witnesses"] == 58 and method["counts"]["witness_results"] == {"fail": 30, "pass": 28}, method["counts"])
    check("open_and_exact_gates", (gaps["effective_count"], gaps["closed_count"], gates["effective_count"], gates["closed_count"]) == (63, 0, 64, 0), {"open": gaps["effective_count"], "exact": gates["effective_count"]})
    check("terminal_abstention", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" and not truth["independent_reproduction_claimed"] and not truth["full_repository_suite_run"], truth["terminal_verdict"])
    check("route_held", route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0 and route["create_or_fork_count"] == 0 and route["standby_contact_count"] == 0, route["state"])
    check("future_cli_placeholders", (seats["prepared_placeholder_count"], seats["named_count"], seats["created_count"], seats["launched_count"]) == (8, 0, 0, 0), {key: seats[key] for key in ("prepared_placeholder_count", "named_count", "created_count", "launched_count")})
    check("staged_review", review["valid"] and not review["json_errors"] and review["privacy_confirmed_hits"] == 0, {"valid": review["valid"], "delta": review["delta_path_count"], "owner": review["owner_path_count"]})
    check("document_contract", build["valid"] and 10000 <= build["baton_words"] <= 100000 and build["overview_words"] >= 1500 and not build["document_issues"], {"baton": build["baton_words"], "overview": build["overview_words"], "issues": build["document_issues"]})
    check("owner_growth", len(phase_tree) < 15000, len(phase_tree))

    terminal_values, route_values = [], []
    for path, oid in phase_tree.items():
        if not path.endswith(".json"):
            continue
        payload = json.loads(blobs[oid].decode("utf-8"))
        stack = [payload]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                if "terminal_verdict" in value:
                    terminal_values.append({"path": path, "value": value["terminal_verdict"]})
                if path.endswith("route/terminal-route-state.json") and "state" in value:
                    route_values.append(value["state"])
                stack.extend(value.values())
            elif isinstance(value, list):
                stack.extend(value)
    check("semantic_stale_labels", all(row["value"] == "NOT_READY_FOR_STAGE_20" for row in terminal_values) and route_values == ["PREPARED_NOT_SENT"], {"terminal_values": terminal_values, "route_values": route_values})

    source_ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, head], cwd=REPO).returncode == 0
    x1_ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", X1, head], cwd=REPO).returncode == 0
    evidence_ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE, head], cwd=REPO).returncode == 0
    closeout_ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", CLOSEOUT, head], cwd=REPO).returncode == 0
    phase_commits = int(str(git("rev-list", "--count", f"{SOURCE}..{head}")))
    merges = str(git("rev-list", "--merges", f"{SOURCE}..{head}"))
    parents = str(git("show", "-s", "--format=%P", head)).split()
    check("lifecycle_ancestry", source_ancestor and x1_ancestor and evidence_ancestor and closeout_ancestor and phase_commits == 4 and not merges and parents == [CLOSEOUT], {"source": source_ancestor, "x1": x1_ancestor, "evidence": evidence_ancestor, "closeout": closeout_ancestor, "phase_commits": phase_commits, "merges": merges.splitlines() if merges else [], "parents": parents})
    check("exact_branch_and_head", str(git("branch", "--show-current")) == BRANCH and head == str(git("rev-parse", "HEAD")), {"branch": git("branch", "--show-current"), "head": head})

    diff_check = subprocess.run(["git", "diff", "--check", f"{EVIDENCE}..{head}"], cwd=REPO, capture_output=True)
    check("diff_hygiene", diff_check.returncode == 0, diff_check.stderr.decode("utf-8", errors="replace"))

    local = head
    upstream = str(git("rev-parse", "@{u}"))
    upstream_ref = str(git("rev-parse", "--symbolic-full-name", "@{u}"))
    tracking = str(git("rev-parse", upstream_ref))
    live_raw = str(git("ls-remote", "origin", f"refs/heads/{BRANCH}"))
    live = live_raw.split("\t", 1)[0] if live_raw else ""
    divergence = str(git("rev-list", "--left-right", "--count", "HEAD...@{u}"))
    clean_after = str(git("status", "--porcelain=v1")) == ""
    check("clean_before_after", clean_before and clean_after, {"before": clean_before, "after": clean_after})
    check("four_way_live_equality", len({local, upstream, tracking, live}) == 1 and divergence.replace("\t", " ") == "0 0", {"local": local, "upstream": upstream, "tracking": tracking, "live": live, "divergence": divergence})

    minimal_names = {"scoped_test_selection", "complete_phase_json", "five_class_privacy_scan", "manifest_parity", "negative_retention", "terminal_abstention", "route_held", "lifecycle_ancestry", "clean_before_after", "four_way_live_equality"}
    minimal = [row for row in checks if row["name"] in minimal_names]
    passed = sum(row["passed"] for row in checks)
    valid = passed == len(checks)
    receipt = {
        "schema": "ghc.family.v652-v2.final-canonical-validation.external.v1",
        "validated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "exact_head": head, "branch": BRANCH, "checks": checks, "passed": passed, "total": len(checks), "valid": valid,
        "minimal": {"passed": sum(row["passed"] for row in minimal), "total": len(minimal), "valid": all(row["passed"] for row in minimal)},
        "scoped_tests": {"passed": result.testsRun - len(result.failures) - len(result.errors), "total": result.testsRun, "failures": len(result.failures), "errors": len(result.errors)},
        "json_parse_count": json_count, "privacy_scanned_file_count": len(owner_paths), "privacy_candidate_count": len(privacy_candidates), "privacy_confirmed_hit_count": len(privacy_hits),
        "manifest_entry_total": sum(row["entry_count"] for row in manifests), "manifest_contracts": manifests,
        "full_repository_suite_run": False, "canonical_successful_pass_count": 1 if valid else 0, "replay_after_success": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Single bounded same-owner exact-head canonical pass under shared infrastructure; not full-suite credit, independent-team reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility, professional validation, legal or cultural authority, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, or Stage 20 authority."
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"head": head, "tests": f"{receipt['scoped_tests']['passed']}/{receipt['scoped_tests']['total']}", "detailed": f"{passed}/{len(checks)}", "minimal": f"{receipt['minimal']['passed']}/{receipt['minimal']['total']}", "json": json_count, "privacy_scanned": len(owner_paths), "privacy_hits": len(privacy_hits), "manifest_entries": receipt["manifest_entry_total"], "valid": valid}, sort_keys=True))
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()
