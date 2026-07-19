#!/usr/bin/env python3
"""Build the combined Sylven Arc v649-v6 closeout and seal.

This runner consumes the one canonical scoped-pass receipt. It does not rerun
tests, the canonical privacy scan, or any detached or named replay.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v649-v6"
SOURCE = "295aa503d3c336273f541504a83b88783563ad90"
X1 = "d82382737868160e1b16c9302ca8a008b6f3153e"
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"
FINAL_NEGATIVES = 5191
FINAL_OPEN_GAPS = 40
FINAL_EXACT_GATES = 41


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(list(args), cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", env=env).stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def changed_paths() -> list[str]:
    paths = set(filter(None, git("diff", "--name-only").splitlines()))
    paths.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    paths.update(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return sorted(path.replace("\\", "/") for path in paths)


def incremental_privacy(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v649_v6_closeout.py",
        "scripts/ghc_family_v649_v6_validate.py",
        "docs/sylven-arc/v649-v6/validation/final-staged-privacy.json",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    scanned = 0
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v649-v6.final-incremental-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "canonical_scan_rerun": False,
        "boundary": "Incremental final-commit path review only; the credited canonical phase scan was not rerun and zero confirmed hits is not complete privacy assurance.",
    }


def update_method_flow() -> dict[str, Any]:
    ledger = PHASE / "method-flow" / "method-flow-ledger.json"
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/final-method-flow-validation.json"))
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(PHASE / "method-flow/final-method-flow-summary.json"),
        "--markdown-output",
        str(PHASE / "method-flow/final-method-flow-summary.md"),
    )
    payload = json.loads(ledger.read_text(encoding="utf-8"))
    counts = {
        "method_count": len(payload["methods"]),
        "failed_witnesses": sum(row["result"] == "fail" for row in payload["witnesses"]),
        "passing_witnesses": sum(row["result"] == "pass" for row in payload["witnesses"]),
        "preferred_methods": sum(row["recommendation_state"] == "preferred" for row in payload["methods"]),
    }
    if counts != {"method_count": 22, "failed_witnesses": 12, "passing_witnesses": 22, "preferred_methods": 22}:
        raise RuntimeError(f"unexpected final Method Flow counts: {counts}")
    write_json("method-flow/final-method-flow-receipt.json", {"schema": "ghc.family.v649-v6.method-flow.final.v1", **counts, "failures_erased": 0, "same_owner_only": True})
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-commit", required=True)
    args = parser.parse_args()
    evidence = args.evidence_commit
    if git("rev-parse", "HEAD") != evidence:
        raise RuntimeError("closeout must begin at the exact evidence head")
    if git("rev-parse", f"{evidence}^") != X1:
        raise RuntimeError("evidence must be the direct child of the frozen x1 commit")
    before = changed_paths()
    expected_receipt = "docs/sylven-arc/v649-v6/validation/canonical-pass-result.json"
    if before != [expected_receipt]:
        raise RuntimeError(f"closeout requires only the canonical receipt to be uncommitted, observed={before}")

    result = load("validation/canonical-pass-result.json")
    if result["evidence_head"] != evidence or result["successful_canonical_pass_number"] != 1:
        raise RuntimeError("canonical receipt does not bind the exact evidence head and sole pass")
    if result["failed_canonical_attempts_before_success"] != 0 or result["post_success_replay"]:
        raise RuntimeError("unexpected canonical attempt or replay state")

    runners = load("x2/runner-use-ledger.json")
    final_runner_items = []
    for row in runners["items"]:
        if row["runner"] == "build_ghc_family_v649_v6_closeout.py":
            final_runner_items.append({**row, "invoked": True, "passed": True, "receipt": "runner-receipts/ghc_family_v649_v6_closeout.json", "pending_reason": None})
        else:
            final_runner_items.append(row)
    write_json("runner-receipts/ghc_family_v649_v6_closeout.json", {
        "schema": "ghc.family.v649-v6.closeout-runner.v1",
        "evidence_head": evidence,
        "canonical_pass_bound": True,
        "tests_rerun": False,
        "canonical_scan_rerun": False,
        "replay_used": False,
        "passed": True,
    })
    write_json("x2/runner-use-ledger-final.json", {
        "schema": "ghc.family.v649-v6.runner-use-final.v1",
        "runner_count": 10,
        "completed_count": 10,
        "pending_count": 0,
        "items": final_runner_items,
    })

    plan = load("validation/final-validation-plan.json")
    write_json("validation/final-validation-plan.json", {
        **plan,
        "selected_test_count": result["tests_selected"],
        "detailed_check_count": result["detailed_checks"],
        "minimal_check_count": result["minimal_checks"],
        "successful_passes_used": 1,
        "failed_canonical_attempts_before_success": 0,
        "post_success_replay": False,
    })
    method_counts = update_method_flow()

    write_json("retained-negative-register-final.json", {
        "schema": "ghc.family.v649-v6.retained-negatives.final.v1",
        "inherited_effective": 5109,
        "x1_operational": 8,
        "synthetic_executed_rejected": 70,
        "x2_operational": 4,
        "effective_final": FINAL_NEGATIVES,
        "negative_erased": False,
    })
    write_json("exact-open-gate-register-final.json", {
        "schema": "ghc.family.v649-v6.gates.final.v1",
        "effective_open_gaps": FINAL_OPEN_GAPS,
        "effective_exact_gates": FINAL_EXACT_GATES,
        "silently_closed": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })

    common = {
        "source_head": SOURCE,
        "x1_commit": X1,
        "evidence_commit": evidence,
        "full_repository_suite": False,
        "post_success_replay": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("closeout/evidence-receipt.json", {
        "schema": "ghc.family.v649-v6.evidence-receipt.v1",
        **common,
        "direct_parent": X1,
        "distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "effective_negatives": FINAL_NEGATIVES,
        "effective_open_gaps": FINAL_OPEN_GAPS,
        "effective_exact_gates": FINAL_EXACT_GATES,
    })
    write_json("closeout/closeout-receipt.json", {
        "schema": "ghc.family.v649-v6.closeout.v1",
        **common,
        "canonical_tests": result["tests_passed"],
        "detailed_checks": result["detailed_checks"],
        "minimal_checks": result["minimal_checks"],
        "canonical_json_parses": result["phase_json_parses"],
        "canonical_privacy_scanned_files": result["privacy_scanned_files"],
        "privacy_confirmed_hits": 0,
        "method_flow": method_counts,
        "effective_negatives": FINAL_NEGATIVES,
        "effective_open_gaps": FINAL_OPEN_GAPS,
        "effective_exact_gates": FINAL_EXACT_GATES,
        "terminal_route": "PREPARED_NOT_SENT",
    })
    write_json("closeout/seal-receipt.json", {
        "schema": "ghc.family.v649-v6.seal.v1",
        **common,
        "final_commit_parent_required": evidence,
        "phase_commit_count_after_final": 3,
        "merge_count_required": 0,
        "final_parent_count_required": 1,
        "canonical_pass_reused_without_rerun": True,
        "exact_final_head_resolution": "the commit containing this receipt, proven live after commit",
    })
    write_json("closeout/final-validation-record.json", {
        "schema": "ghc.family.v649-v6.final-validation.v1",
        **common,
        "canonical_pass": result,
        "final_incremental_review_required": True,
        "final_exact_head_proof_state": "external_read_only_post_commit_gate",
        "tests_rerun_after_success": False,
        "canonical_privacy_scan_rerun_after_success": False,
        "detached_or_named_replay_used": False,
        "terminal_route": "PREPARED_NOT_SENT",
    })

    write_json("orchestration/final-phase-state.json", {
        **load("orchestration/final-phase-state.json"),
        "schema": "ghc.family.v649-v6.orchestration.final.v1",
        "stage": "sealed_candidate",
        "canonical_pass_used": True,
        "successful_passes": 1,
        "replay_used": False,
        "terminal_route": "PREPARED_NOT_SENT",
        "successor_messages_sent": 0,
    })
    write_json("orchestration/terminal-route-receipt.json", {
        "schema": "ghc.family.v649-v6.route.v1",
        "target_title": "Eiren Kestrel",
        "successor_phase": "v649-gmut-thos-v7-x1-x2",
        "state": "PREPARED_NOT_SENT",
        "messages_sent": 0,
        "task_created": False,
        "cross_platform_send": False,
        "send_gate": "exact final clean pushed local-upstream-tracking-live equality",
    })
    write_json("wellbeing-check-final.json", {
        **load("wellbeing-check-final.json"),
        "schema": "ghc.family.v649-v6.wellbeing.final.v1",
        "phase_commits": 3,
        "canonical_passes": 1,
        "replays": 0,
        "host_changes": 0,
        "sibling_contacts": 0,
        "terminal_contact_pending": "Eiren Kestrel only after exact final proof",
    })
    write_json("phase-truth.json", {
        **load("phase-truth.json"),
        "schema": "ghc.family.v649-v6.phase-truth.final.v1",
        "stage": "sealed_candidate",
        "single_pass_used": True,
        "canonical_tests_passed": result["tests_passed"],
        "canonical_detailed_checks": result["detailed_checks"],
        "canonical_minimal_checks": result["minimal_checks"],
        "canonical_json_parses": result["phase_json_parses"],
        "canonical_privacy_files": result["privacy_scanned_files"],
        "effective_negatives": FINAL_NEGATIVES,
        "method_flow_methods": method_counts["method_count"],
        "method_flow_failed_witnesses": method_counts["failed_witnesses"],
        "method_flow_passing_witnesses": method_counts["passing_witnesses"],
        "replay_used": False,
        "terminal_route": "PREPARED_NOT_SENT",
    })
    write_json("closeout/closeout-candidate.json", {
        "schema": "ghc.family.v649-v6.closeout-candidate.final.v1",
        "canonical_successful_pass_used": True,
        "terminal_route": "PREPARED_NOT_SENT",
        "ready_for_final_commit": True,
        "tests_rerun": False,
        "canonical_scan_rerun": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })

    parsed = []
    for path in sorted(PHASE.rglob("*.json")):
        json.loads(path.read_text(encoding="utf-8"))
        parsed.append(path.relative_to(PHASE).as_posix())
    write_json("validation/final-json-integrity.json", {
        "schema": "ghc.family.v649-v6.final-json-integrity.v1",
        "parsed_before_self_receipts": len(parsed),
        "issues": [],
        "tests_rerun": False,
        "canonical_privacy_scan_rerun": False,
    })

    exclusions = [
        "docs/sylven-arc/v649-v6/validation/final-staged-manifest.json",
        "docs/sylven-arc/v649-v6/validation/final-staged-privacy.json",
        "docs/sylven-arc/v649-v6/validation/final-staged-review.json",
    ]
    paths = [path for path in changed_paths() if path not in exclusions]
    entries = [
        {"path": path, "git_blob": git("hash-object", f"--path={path}", path), "bytes": (ROOT / path).stat().st_size}
        for path in paths
        if (ROOT / path).is_file()
    ]
    scan = incremental_privacy(paths + exclusions)
    write_json("validation/final-staged-privacy.json", scan)
    write_json("validation/final-staged-manifest.json", {
        "schema": "ghc.family.v649-v6.final-manifest.v1",
        "hash_domain": "git_hash_object_path_filtered_blob",
        "entries": entries,
        "entry_count": len(entries),
        "self_exclusions": exclusions,
        "coverage_boundary": "All final closeout changes except three declared self-referential receipts.",
    })
    write_json("validation/final-staged-review.json", {
        "schema": "ghc.family.v649-v6.final-staged-review.v1",
        "intended_path_count": len(entries) + 3,
        "manifest_entry_count": len(entries),
        "self_exclusion_count": 3,
        "out_of_scope_paths": [],
        "privacy_confirmed_hits": scan["confirmed_hit_count"],
        "canonical_tests_rerun": False,
        "canonical_scan_rerun": False,
        "replay_used": False,
        "evidence_head": evidence,
        "terminal_route": "PREPARED_NOT_SENT",
    })
    if scan["confirmed_hit_count"]:
        raise RuntimeError("final incremental privacy review found confirmed hits")
    print(json.dumps({
        "evidence_head": evidence,
        "final_paths": len(entries) + 3,
        "final_json_integrity": len(parsed),
        "privacy_confirmed_hits": 0,
        "tests_rerun": False,
        "canonical_scan_rerun": False,
        "passed": True,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
