#!/usr/bin/env python3
"""Run Tamar v652-v3's single authorized exact-final canonical pass."""

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
PHASE_ROOT = "docs/tamar-vey/v652-v3"
SOURCE = "fa060eec3071694e1aff8eaf7d76d6c4b0f8075e"
X1 = "4e905d2b0637d4db78ac55273c8b52d5cf6c2117"
EVIDENCE = "22c4ca1e7d4473fcf5246867bb729b3748f34441"
BRANCH = "codex/GHC-Family/tamar-vey-full-tools"


def git(*args: str, binary: bool = False, check: bool = True) -> str | bytes:
    proc = subprocess.run(["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout if binary else proc.stdout.decode("utf-8").strip()


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input="".join(oid + "\n" for oid in unique).encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
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


def manifest_check(
    commit: str,
    path: str,
    expected_paths: set[str],
    tree: dict[str, str],
    blobs: dict[str, bytes],
) -> dict[str, Any]:
    manifest = load_at(commit, path)
    declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    issues: list[dict[str, Any]] = []
    if declared != expected_paths:
        issues.append({"kind": "path_set", "missing": sorted(expected_paths - declared), "extra": sorted(declared - expected_paths)})
    for row in manifest["entries"]:
        oid = tree.get(row["path"])
        data = blobs.get(row["git_blob"])
        if oid != row["git_blob"] or data is None or len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            issues.append({"kind": "entry", "path": row["path"]})
    return {
        "path": path,
        "entry_count": len(manifest["entries"]),
        "self_exclusion_count": len(manifest["self_exclusions"]),
        "expected_path_count": len(expected_paths),
        "issues": issues,
        "valid": not issues,
    }


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def selected_tests() -> tuple[unittest.TestSuite, dict[str, Any]]:
    patterns = [
        "test_ghc_family_v652_v2_x1.py",
        "test_ghc_family_v652_v2.py",
        "test_ghc_family_v652_v3_x1.py",
        "test_ghc_family_v652_v3.py",
        "test_ghc_family_v652_v3_closeout.py",
    ]
    loader = unittest.TestLoader()
    selected = unittest.TestSuite()
    raw_counts: dict[str, int] = {}
    eligible_counts: dict[str, int] = {}
    exclusions: list[dict[str, str]] = []
    loader_errors: list[str] = []
    for index, pattern in enumerate(patterns):
        path = REPO / "tests" / pattern
        spec = importlib.util.spec_from_file_location(f"v6523_scoped_{index}", path)
        if spec is None or spec.loader is None:
            loader_errors.append(f"unable to load {pattern}")
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        loaded = loader.loadTestsFromModule(module)
        tests = list(flatten(loaded))
        raw_counts[pattern] = len(tests)
        eligible = []
        for test in tests:
            method = getattr(test, "_testMethodName", "")
            if pattern == "test_ghc_family_v652_v2_x1.py" and method == "test_placeholders_privacy_and_x1_only":
                exclusions.append(
                    {
                        "pattern": pattern,
                        "test": method,
                        "reason": "Inherited x1 lifecycle-local absence assertion; all other inherited and current successor behavior remains selected.",
                    }
                )
            else:
                eligible.append(test)
        eligible_counts[pattern] = len(eligible)
        selected.addTests(eligible)
    loader_errors.extend(loader.errors)
    return selected, {
        "patterns": patterns,
        "raw_counts": raw_counts,
        "eligible_counts": eligible_counts,
        "raw_count": sum(raw_counts.values()),
        "eligible_count": sum(eligible_counts.values()),
        "explicit_lifecycle_exclusions": exclusions,
        "loader_errors": loader_errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head")
    parser.add_argument("--receipt")
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()

    suite, selection = selected_tests()
    selection_ok = (
        selection["raw_count"] == 40
        and selection["eligible_count"] == 39
        and len(selection["explicit_lifecycle_exclusions"]) == 1
        and not selection["loader_errors"]
    )
    if args.preflight:
        print(json.dumps({"selection": selection, "valid": selection_ok}, sort_keys=True))
        return 0 if selection_ok else 1
    if not args.expected_head or not args.receipt:
        raise SystemExit("--expected-head and --receipt are required for the canonical pass")

    head = str(git("rev-parse", "HEAD"))
    clean_before = not str(git("status", "--porcelain=v1", "--untracked-files=all"))
    if head != args.expected_head:
        raise SystemExit({"expected_head": args.expected_head, "observed_head": head})

    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    test_valid = selection_ok and result.testsRun == 39 and not result.failures and not result.errors
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, observed: Any) -> None:
        checks.append({"name": name, "passed": bool(condition), "observed": observed})

    check(
        "scoped_test_selection",
        test_valid,
        {
            **selection,
            "tests_run": result.testsRun,
            "failures": [str(test) for test, _trace in result.failures],
            "errors": [str(test) for test, _trace in result.errors],
        },
    )

    full_tree = tree_map(head)
    owner_paths = set(str(git("diff", "--name-only", SOURCE, head)).splitlines())
    owner_tree = {path: full_tree[path] for path in owner_paths if path in full_tree}
    owner_blobs = batch_blobs(list(owner_tree.values()))

    json_issues = []
    json_count = 0
    for path, oid in sorted(owner_tree.items()):
        if path.startswith(PHASE_ROOT + "/") and path.endswith(".json"):
            json_count += 1
            try:
                json.loads(owner_blobs[oid].decode("utf-8"))
            except Exception as exc:  # noqa: BLE001
                json_issues.append({"path": path, "error": str(exc)})
    check("complete_phase_json", not json_issues, {"parsed": json_count, "issues": json_issues})

    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definition_paths = {
        "scripts/build_ghc_family_v652_v3_preregistration.py",
        "scripts/ghc_family_v652_v3_evidence_validate.py",
        "scripts/ghc_family_v652_v3_closeout_review.py",
        "scripts/ghc_family_v652_v3_final_validate.py",
        f"{PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{PHASE_ROOT}/validation/closeout-staged-privacy.json",
    }
    privacy_candidates, privacy_hits = [], []
    for path, oid in sorted(owner_tree.items()):
        try:
            text = owner_blobs[oid].decode("utf-8")
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
    final_paths = set(str(git("diff-tree", "--no-commit-id", "--name-only", "-r", head)).splitlines())
    manifest_specs = [
        (X1, f"{PHASE_ROOT}/validation/x1-staged-manifest.json", x1_paths),
        (EVIDENCE, f"{PHASE_ROOT}/validation/evidence-staged-manifest.json", evidence_paths),
        (head, f"{PHASE_ROOT}/validation/closeout-delta-manifest.json", final_paths),
        (head, f"{PHASE_ROOT}/validation/final-owner-manifest.json", owner_paths),
    ]
    manifest_oids: list[str] = []
    for commit, path, _expected in manifest_specs:
        manifest_oids.extend(row["git_blob"] for row in load_at(commit, path)["entries"])
    manifest_blobs = batch_blobs(manifest_oids)
    manifests = [
        manifest_check(commit, path, expected, tree_map(commit), manifest_blobs)
        for commit, path, expected in manifest_specs
    ]
    check("manifest_parity", all(row["valid"] for row in manifests), manifests)

    truth = load_at(head, f"{PHASE_ROOT}/final/phase-truth.json")
    outcomes = load_at(head, f"{PHASE_ROOT}/evidence/outcome-ledger.json")
    negatives = load_at(head, f"{PHASE_ROOT}/final/retained-negative-register.json")
    gaps = load_at(head, f"{PHASE_ROOT}/final/open-gap-register.json")
    gates = load_at(head, f"{PHASE_ROOT}/final/exact-gate-register.json")
    method = load_at(head, f"{PHASE_ROOT}/method-flow/method-flow-ledger.json")
    route = load_at(head, f"{PHASE_ROOT}/route/terminal-route-state.json")
    seats = load_at(head, f"{PHASE_ROOT}/provenance/future-cli-placeholder-invariant.json")
    check("outcome_truth", outcomes["counts"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1} and outcomes["proposal_count"] == 30, outcomes["counts"])
    check(
        "negative_retention",
        negatives["effective_at_closeout"] == 8383
        and negatives["x1_operational_count"] == 10
        and negatives["x2_operational_count"] == 5
        and negatives["closeout_operational_count"] == 6
        and negatives["synthetic_mutation_negative_count"] == 150
        and negatives["no_failure_erased"],
        {"effective": negatives["effective_at_closeout"], "x1": negatives["x1_operational_count"], "x2": negatives["x2_operational_count"], "closeout": negatives["closeout_operational_count"]},
    )
    check("method_flow", method["counts"]["methods"] == 21 and method["counts"]["witnesses"] == 42 and method["counts"]["witness_results"] == {"fail": 21, "pass": 21}, method["counts"])
    check("open_and_exact_gates", (gaps["effective_count"], gaps["closed_count"], gates["effective_count"], gates["closed_count"]) == (64, 0, 65, 0), {"open": gaps["effective_count"], "exact": gates["effective_count"]})
    check(
        "terminal_abstention",
        truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
        and not truth["full_repository_suite_run"]
        and not truth["independent_reproduction_claimed"],
        {"verdict": truth["terminal_verdict"], "full_suite": truth["full_repository_suite_run"]},
    )
    check(
        "route_held",
        route["target_exact_title"] == "Sylven Arc"
        and route["target_phase"] == "v652-v4"
        and route["state"] == "PREPARED_NOT_SENT"
        and (route["send_count"], route["create_or_fork_count"], route["standby_contact_count"]) == (0, 0, 0),
        route,
    )
    check(
        "future_cli_unlaunched",
        (seats["prepared_placeholder_count"], seats["named_count"], seats["created_count"], seats["launched_count"]) == (8, 0, 0, 0),
        {key: seats[key] for key in ("prepared_placeholder_count", "named_count", "created_count", "launched_count")},
    )

    baton = str(git("show", f"{head}:{PHASE_ROOT}/handoffs/sylven-arc-v652-v4-activation.md"))
    overview = str(git("show", f"{head}:{PHASE_ROOT}/overview/final-integrated-overview.md"))
    report = str(git("show", f"{head}:{PHASE_ROOT}/reports/final-static-report.html"))
    baton_words = len(re.findall(r"\b\w+\b", baton, flags=re.UNICODE))
    overview_words = len(re.findall(r"\b\w+\b", overview, flags=re.UNICODE))
    check("document_contracts", 10000 <= baton_words <= 100000 and overview_words >= 1500, {"baton_words": baton_words, "overview_words": overview_words})
    report_tokens = ("Skip to main content", "<caption>", "scope='col'", "tabindex='0'", "NOT_READY_FOR_STAGE_20")
    check("structural_accessibility", all(token in report for token in report_tokens), {"required_tokens": report_tokens})

    stale_tokens = ("Orin v652-v3 remains", "ZTF adapter", "archaeology/CBR authority", '"target_exact_title": "Tamar Vey"')
    stale_hits = [token for token in stale_tokens if token in baton or token in overview or token in report]
    check("semantic_stale_label_review", not stale_hits, stale_hits)
    check("owner_growth_threshold", len(owner_paths) < 15000, len(owner_paths))

    source_ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, head], cwd=REPO).returncode == 0
    x1_ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", X1, head], cwd=REPO).returncode == 0
    evidence_ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE, head], cwd=REPO).returncode == 0
    phase_commits = int(str(git("rev-list", "--count", f"{SOURCE}..{head}")))
    merges = str(git("rev-list", "--merges", f"{SOURCE}..{head}"))
    parents = str(git("show", "-s", "--format=%P", head)).split()
    check(
        "lifecycle_ancestry",
        source_ancestor and x1_ancestor and evidence_ancestor and phase_commits == 3 and not merges and parents == [EVIDENCE],
        {"source": source_ancestor, "x1": x1_ancestor, "evidence": evidence_ancestor, "phase_commits": phase_commits, "merges": merges.splitlines() if merges else [], "parents": parents},
    )
    branch = str(git("branch", "--show-current"))
    check("exact_branch_and_head", branch == BRANCH and head == str(git("rev-parse", "HEAD")), {"branch": branch, "head": head})
    diff_check = subprocess.run(["git", "diff", "--check", f"{SOURCE}..{head}"], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check("diff_hygiene", diff_check.returncode == 0, diff_check.stdout.decode("utf-8", errors="replace").splitlines())

    local = str(git("rev-parse", "HEAD"))
    upstream = str(git("rev-parse", "@{u}"))
    tracking_ref = str(git("rev-parse", "--symbolic-full-name", "@{u}"))
    tracking = str(git("rev-parse", tracking_ref))
    live_raw = str(git("ls-remote", "origin", f"refs/heads/{BRANCH}"))
    live = live_raw.split("\t", 1)[0] if live_raw else ""
    divergence = str(git("rev-list", "--left-right", "--count", "HEAD...@{u}"))
    check("four_way_live_equality", len({local, upstream, tracking, live}) == 1 and divergence.replace("\t", " ") == "0 0", {"local": local, "upstream": upstream, "tracking": tracking, "live": live, "divergence": divergence})
    clean_after = not str(git("status", "--porcelain=v1", "--untracked-files=all"))
    check("clean_before_after", clean_before and clean_after, {"before": clean_before, "after": clean_after})

    passed = sum(row["passed"] for row in checks)
    valid = passed == len(checks)
    minimal_names = {
        "scoped_test_selection",
        "complete_phase_json",
        "five_class_privacy_scan",
        "manifest_parity",
        "negative_retention",
        "terminal_abstention",
        "route_held",
        "lifecycle_ancestry",
        "clean_before_after",
        "four_way_live_equality",
    }
    minimal = [row for row in checks if row["name"] in minimal_names]
    receipt = {
        "schema": "ghc.family.v652-v3.exact-final-validation.external.v1",
        "validated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "exact_head": head,
        "branch": BRANCH,
        "checks": checks,
        "passed": passed,
        "total": len(checks),
        "valid": valid,
        "scoped_tests": {
            "passed": result.testsRun - len(result.failures) - len(result.errors),
            "total": result.testsRun,
            "selection": selection,
        },
        "minimal": {
            "passed": sum(row["passed"] for row in minimal),
            "total": len(minimal),
            "valid": all(row["passed"] for row in minimal),
        },
        "json_parse_count": json_count,
        "privacy_scanned_file_count": len(owner_paths),
        "privacy_candidate_count": len(privacy_candidates),
        "privacy_confirmed_hit_count": len(privacy_hits),
        "manifest_entry_total": sum(row["entry_count"] for row in manifests),
        "manifest_contracts": manifests,
        "full_repository_suite_run": False,
        "successful_canonical_pass_count": 1 if valid else 0,
        "replay_after_success": False,
        "same_owner_only": True,
        "independent_team_reproduction": False,
        "boundary": "Single bounded same-owner exact-head canonical pass under shared infrastructure; not full-suite credit, independent-team reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility, professional validation, legal or cultural authority, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, or Stage 20 authority.",
    }
    receipt_path = Path(args.receipt).resolve()
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "head": head,
                "tests": f"{receipt['scoped_tests']['passed']}/{receipt['scoped_tests']['total']}",
                "detailed": f"{passed}/{len(checks)}",
                "minimal": f"{receipt['minimal']['passed']}/{receipt['minimal']['total']}",
                "json": json_count,
                "privacy_scanned": len(owner_paths),
                "privacy_hits": len(privacy_hits),
                "manifest_entries": receipt["manifest_entry_total"],
                "valid": valid,
            },
            sort_keys=True,
        )
    )
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
