#!/usr/bin/env python3
"""Run the single exact-final canonical validation for Ilyra Fen v650-v2."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / "v650-v2"
BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
SOURCE = "f47cd5145647965935f80d67751f0e09d9740540"
X1 = "d70cbab27e64e12d634e0d9b94b73f50aa507ad1"
EVIDENCE = "2c54ccf284f3a9faf7c3cd5809b83af46faa7594"
TEST_MODULES = [
    "tests.test_ghc_family_v650_v1_x1",
    "tests.test_ghc_family_v650_v2_x1",
    "tests.test_ghc_family_v650_v2_x2",
    "tests.test_ghc_family_v650_v2_closeout",
]
PRIVACY = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}


def run(*args: str, check: bool = True, timeout: int = 240) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def git(*args: str, check: bool = True) -> str:
    return run("git", *args, check=check).stdout.strip()


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def record(rows: list[dict[str, Any]], name: str, passed: bool, observed: Any) -> None:
    rows.append({"name": name, "passed": bool(passed), "observed": observed})


def run_selected_tests() -> dict[str, Any]:
    result = run(sys.executable, "-m", "unittest", *TEST_MODULES, check=False, timeout=240)
    output = result.stdout + result.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests?", output)
    return {
        "modules": TEST_MODULES,
        "test_count": int(match.group(1)) if match else 0,
        "returncode": result.returncode,
        "passed": result.returncode == 0,
        "failure_or_error_lines": [
            line.strip()
            for line in output.splitlines()
            if line.startswith(("FAIL:", "ERROR:"))
        ],
    }


def check_manifest(relative: str, anchor: str, owner_coverage: bool = False) -> dict[str, Any]:
    payload = load(relative)
    mismatches: list[str] = []
    for row in payload["entries"]:
        actual = git("rev-parse", f"{anchor}:{row['path']}", check=False)
        if actual != row["git_blob"]:
            mismatches.append(row["path"])
    coverage_missing: list[str] = []
    coverage_extra: list[str] = []
    if owner_coverage:
        actual_paths = set(git("ls-tree", "-r", "--name-only", anchor, "docs/ilyra-fen/v650-v2").splitlines())
        declared = {row["path"] for row in payload["entries"]} | set(payload["self_exclusions"])
        coverage_missing = sorted(actual_paths - declared)
        coverage_extra = sorted(declared - actual_paths)
    return {
        "entry_count": len(payload["entries"]),
        "self_exclusion_count": len(payload["self_exclusions"]),
        "mismatches": mismatches,
        "coverage_missing": coverage_missing,
        "coverage_extra": coverage_extra,
        "passed": not mismatches and not coverage_missing and not coverage_extra,
    }


def parse_json() -> dict[str, Any]:
    paths = sorted(PHASE.rglob("*.json"))
    errors: list[str] = []
    for path in paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(PHASE).as_posix()}: {type(exc).__name__}")
    return {"count": len(paths), "errors": errors, "passed": not errors}


def privacy_scan() -> dict[str, Any]:
    paths = sorted(path for path in PHASE.rglob("*") if path.is_file())
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    definition_names = {"final-owner-privacy.json", "x1-staged-privacy.json", "evidence-staged-privacy.json"}
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(PHASE).as_posix()
        for name, pattern in PRIVACY.items():
            if pattern.search(text):
                disposition = "scanner_definition" if path.name in definition_names else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "file_count": len(paths),
        "pattern_class_count": len(PRIVACY),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "passed": not confirmed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external-output", required=True)
    args = parser.parse_args()
    output = Path(args.external_output).resolve()
    try:
        output.relative_to(ROOT.resolve())
    except ValueError:
        pass
    else:
        raise RuntimeError("exact-final receipt must remain outside the repository")
    output.parent.mkdir(parents=True, exist_ok=True)

    head = git("rev-parse", "HEAD")
    tests = run_selected_tests()
    json_result = parse_json()
    privacy = privacy_scan()
    x1_manifest = check_manifest("validation/x1-staged-manifest.json", X1)
    evidence_manifest = check_manifest("validation/evidence-staged-manifest.json", EVIDENCE)
    owner_manifest = check_manifest("validation/final-owner-manifest.json", head, owner_coverage=True)
    final_staged_manifest = check_manifest("validation/final-staged-manifest.json", head)
    detailed: list[dict[str, Any]] = []
    minimal: list[dict[str, Any]] = []

    local = head
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git("ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    dirty = git("status", "--porcelain=v1", "--untracked-files=all")
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merge_count = int(git("rev-list", "--merges", "--count", f"{SOURCE}..{head}"))
    parent_count = len(git("show", "-s", "--format=%P", head).split())
    ancestry = {
        "source": run("git", "merge-base", "--is-ancestor", SOURCE, head, check=False).returncode == 0,
        "x1": run("git", "merge-base", "--is-ancestor", X1, head, check=False).returncode == 0,
        "evidence": run("git", "merge-base", "--is-ancestor", EVIDENCE, head, check=False).returncode == 0,
    }
    truth = load("phase-truth-final.json")
    outcomes = load("x2/core-outcome-ledger.json")
    negatives = load("x2/retained-negative-register.json")
    gates = load("x2/gate-register.json")
    documents = load("validation/final-document-cap-receipt.json")
    owner_threshold = load("validation/final-owner-file-threshold.json")
    privacy_receipt = load("validation/final-owner-privacy.json")
    staged_review = load("validation/final-staged-review.json")
    method_summary = load("method-flow/method-flow-summary-x2.json")
    workflow = load("workflow/workflow-plan-refinement.json")
    route = load("orchestration/phase-state-closeout.json")

    detail_values = [
        ("selected tests", tests["passed"], tests),
        ("all phase JSON parses", json_result["passed"], json_result),
        ("live privacy scan", privacy["passed"], privacy),
        ("committed privacy receipt", privacy_receipt["confirmed_hit_count"] == 0, privacy_receipt["confirmed_hit_count"]),
        ("x1 commit-local manifest", x1_manifest["passed"], x1_manifest),
        ("evidence commit-local manifest", evidence_manifest["passed"], evidence_manifest),
        ("final owner manifest", owner_manifest["passed"], owner_manifest),
        ("final staged manifest", final_staged_manifest["passed"], final_staged_manifest),
        ("exact staged review", staged_review["passed"], staged_review),
        ("source ancestry", ancestry["source"], ancestry["source"]),
        ("x1 ancestry", ancestry["x1"], ancestry["x1"]),
        ("evidence ancestry", ancestry["evidence"], ancestry["evidence"]),
        ("three phase commits", phase_commits == 3, phase_commits),
        ("zero merge commits", merge_count == 0, merge_count),
        ("single final parent", parent_count == 1, parent_count),
        ("final directly follows evidence", git("rev-parse", "HEAD^") == EVIDENCE, git("rev-parse", "HEAD^")),
        ("canonical branch", git("branch", "--show-current") == BRANCH, git("branch", "--show-current")),
        ("clean state", dirty == "", dirty),
        ("four-way equality", len({local, upstream, tracking, live}) == 1, {"local": local, "upstream": upstream, "tracking": tracking, "live": live}),
        ("outcome distribution", outcomes["distribution"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}, outcomes["distribution"]),
        ("negative total", negatives["effective_at_evidence"] == 5690, negatives["effective_at_evidence"]),
        ("all mutations retained", load("x2/synthetic-mutation-results.json")["rejected_count"] == 100, load("x2/synthetic-mutation-results.json")["rejected_count"]),
        ("open gaps preserved", gates["effective_open_gaps"] == 44, gates["effective_open_gaps"]),
        ("exact gates preserved", gates["effective_exact_gates"] == 45, gates["effective_exact_gates"]),
        ("no gate silently closed", gates["silently_closed"] == 0, gates["silently_closed"]),
        ("Method Flow parity", method_summary["counts"]["witness_results"] == {"fail": 11, "pass": 11}, method_summary["counts"]),
        ("workflow valid", workflow["valid"] is True, workflow["valid"]),
        ("document cap", documents["all_under_20000"] is True, documents),
        ("baton word range", documents["baton_within_8000_20000"] is True, documents["baton_words"]),
        ("owner threshold", owner_threshold["below_threshold"] is True, owner_threshold),
        ("route held", route["terminal_route"] == "PREPARED_NOT_SENT", route["terminal_route"]),
        ("terminal verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"]),
        ("no full suite", truth["full_repository_suite"] is False, truth["full_repository_suite"]),
        ("no replay", truth["replay_used"] is False, truth["replay_used"]),
        ("same-owner only", truth["same_owner_only"] is True and truth["independent_reproduction"] is False, {"same_owner_only": truth["same_owner_only"], "independent_reproduction": truth["independent_reproduction"]}),
    ]
    for name, passed, observed in detail_values:
        record(detailed, name, passed, observed)

    minimal_values = [
        ("tests", tests["passed"]),
        ("json", json_result["passed"]),
        ("privacy", privacy["passed"]),
        ("x1 manifest", x1_manifest["passed"]),
        ("evidence manifest", evidence_manifest["passed"]),
        ("owner manifest", owner_manifest["passed"]),
        ("staged manifest", final_staged_manifest["passed"]),
        ("source ancestor", ancestry["source"]),
        ("x1 ancestor", ancestry["x1"]),
        ("evidence ancestor", ancestry["evidence"]),
        ("commit cap", phase_commits <= 4),
        ("exact cadence", phase_commits == 3),
        ("zero merges", merge_count == 0),
        ("one parent", parent_count == 1),
        ("clean", dirty == ""),
        ("remote equal", len({local, upstream, tracking, live}) == 1),
        ("negatives", negatives["effective_at_evidence"] == 5690),
        ("gates", gates["effective_open_gaps"] == 44 and gates["effective_exact_gates"] == 45),
        ("not Stage 20", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"),
        ("route held before send", route["terminal_route"] == "PREPARED_NOT_SENT"),
    ]
    for name, passed in minimal_values:
        record(minimal, name, passed, passed)

    passed = tests["passed"] and all(row["passed"] for row in detailed) and all(row["passed"] for row in minimal)
    payload = {
        "schema": "ghc.family.v650-v2.exact-final-external-validation.v1",
        "exact_head": head,
        "branch": BRANCH,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "tests": tests,
        "detailed": {"count": len(detailed), "passed_count": sum(row["passed"] for row in detailed), "checks": detailed},
        "minimal": {"count": len(minimal), "passed_count": sum(row["passed"] for row in minimal), "checks": minimal},
        "json": json_result,
        "privacy": privacy,
        "manifests": {"x1": x1_manifest, "evidence": evidence_manifest, "owner": owner_manifest, "final_staged": final_staged_manifest},
        "topology": {"phase_commits": phase_commits, "merge_commits": merge_count, "final_parent_count": parent_count, "ancestry": ancestry},
        "four_way_equal": len({local, upstream, tracking, live}) == 1,
        "clean_before_and_after": dirty == "" and git("status", "--porcelain=v1", "--untracked-files=all") == "",
        "successful_canonical_passes_used": 1 if passed else 0,
        "replay_used": False,
        "full_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "passed": passed,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"passed": passed, "head": head, "tests": tests["test_count"], "detailed": len(detailed), "minimal": len(minimal), "json": json_result["count"], "privacy_files": privacy["file_count"]}, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
