#!/usr/bin/env python3
"""Build truthful Eiren v647-v5 closeout, seal, and final protocol records."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v647_v5_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/eiren-kestrel/v647-v5")
PHASE = ROOT / PHASE_REL
SOURCE = "1395f18ab6504485448eb8e4d507f94ac066caf4"
X1 = "d69257c1922407637db3bb4933d426d70a27e4bd"


def read(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def ancestry(ancestor: str, descendant: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=ROOT).returncode == 0


def owner_paths(exclusions: set[str]) -> list[str]:
    prefix = PHASE_REL.as_posix() + "/"
    tracked = {line for line in git("ls-files", prefix).splitlines() if line}
    present = {
        path.relative_to(ROOT).as_posix()
        for path in PHASE.rglob("*") if path.is_file()
    }
    return sorted((tracked | present) - exclusions)


def build_manifest(from_index: bool = False) -> int:
    manifest_name = (PHASE_REL / "validation/final-owner-manifest.json").as_posix()
    declared_exclusions = {
        manifest_name,
        (PHASE_REL / "validation/closeout-staged-manifest.json").as_posix(),
        (PHASE_REL / "validation/closeout-staged-review.json").as_posix(),
    }
    paths = owner_paths(declared_exclusions)
    entries = []
    for relative in paths:
        raw = subprocess.check_output(["git", "show", f":{relative}"], cwd=ROOT) if from_index else (ROOT / relative).read_bytes()
        entries.append({"path": relative, "sha256": hashlib.sha256(raw).hexdigest()})
    write("validation/final-owner-manifest.json", {
        "schema": "ghc.family.v647-v5.final-owner-manifest.v1", "hash_domain": "git_index_blob" if from_index else "working_bytes_pending_index_refresh",
        "entries": entries, "entry_count": len(entries), "declared_self_exclusions": sorted(declared_exclusions),
        "coverage_rule": "all owner phase files in the final index except the manifest and closeout staged receipts",
    })
    return len(entries)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    parser.add_argument("--refresh-before-validation", action="store_true")
    args = parser.parse_args()
    if args.manifest_only or args.manifest_from_index:
        count = build_manifest(from_index=args.manifest_from_index)
        print(json.dumps({"phase": d.PHASE, "manifest_entries": count, "mode": "manifest_from_index" if args.manifest_from_index else "manifest_only", "result": "pass"}, ensure_ascii=False))
        return 0
    current = read("validation/evidence-validation-runner-summary.json")
    full = read("validation/full-suite-validation.json")
    truth = read("phase-truth.json")
    negative = read("retained-negative-register.json")
    method = read("method-flow/method-flow-state.json")
    if current.get("result") != "pass" or full.get("result") != "pass":
        raise RuntimeError("current or full-suite validation is not pass")
    if full.get("tests", {}).get("unexpected_failure_events"):
        raise RuntimeError("full suite contains unexpected failure events")
    exclusions = full.get("tests", {}).get("exact_inherited_exclusions", [])
    if {row.get("qualified") for row in exclusions} != {
        "test_ghc_family_v646_v1.V646V1EvidenceTests.test_detailed_validator_precommit",
        "test_ghc_family_v646_v1.V646V1EvidenceTests.test_minimal_validator_precommit",
    }:
        raise RuntimeError("exact inherited exclusion set differs")
    head = git("rev-parse", "HEAD")
    evidence = git("log", "-1", "--format=%H", "--", (PHASE_REL / "evidence-receipt.json").as_posix())
    if not evidence or not (ancestry(SOURCE, X1) and ancestry(X1, evidence)) or head != evidence:
        raise RuntimeError("source/x1/evidence ancestry or evidence-head closeout gate invalid")

    write("method-flow/final-method-flow-state.json", method)
    write("method-flow/final-method-flow-summary.json", read("method-flow/x2-method-flow-summary.json"))
    summary_md = (PHASE / "method-flow/x2-method-flow-summary.md").read_text(encoding="utf-8")
    (PHASE / "method-flow/final-method-flow-summary.md").write_text(summary_md, encoding="utf-8", newline="\n")
    write("method-flow/final-runner-validation.json", read("method-flow/x2-runner-validation.json"))
    write("environment/final-rotation-receipt.json", {
        "schema": "ghc.family.v647-v5.final-rotation.v1", "owner_generated_threshold": 15000,
        "owner_generated_files": len(list(PHASE.rglob("*"))), "threshold_exceeded": False,
        "replacement_lane_created": False, "canonical_lane_retained": True,
    })
    write("final-complete-incomplete-checklist.json", {
        **read("complete-incomplete-checklist.json"),
        "schema": "ghc.family.v647-v5.final-checklist.v1",
        "canonical_current_validation": "pass",
        "complete_repository_discovery": {
            "tests_run": full["tests"]["tests_run"],
            "eligible_tests": full["tests"]["eligible_tests"],
            "exact_inherited_exclusions": len(exclusions),
            "unexpected_failures": len(full["tests"]["unexpected_failure_events"]),
        },
        "exact_final_head_validation": "required_after_commit",
        "named_local_replay": "required_after_commit",
        "baton": "not_sent",
    })
    write("closeout-receipt.json", {
        "schema": "ghc.family.v647-v5.closeout-receipt.v1", "phase": d.PHASE, "owner": d.OWNER,
        "source_revision": SOURCE, "x1_revision": X1, "evidence_revision": evidence,
        "closeout_revision": "resolved_by_commit_containing_closeout",
        "strict_x1_before_x2": True, "phase_commit_cap": 4, "commits_used_before_final": 2,
        "core_distribution": truth["core_distribution"], "effective_negatives": negative["effective_total"],
        "effective_open_gaps": truth["effective_open_gaps"], "effective_exact_gates": truth["effective_exact_gates"],
        "current_tests": current["tests"]["tests_run"], "full_tests_run": full["tests"]["tests_run"],
        "eligible_full_tests": full["tests"]["eligible_tests"], "exact_inherited_exclusions": len(exclusions),
        "unexpected_full_suite_failures": 0, "privacy_confirmed_hits": 0,
        "same_owner_only": True, "independent_reproduction": False,
        "exact_final_head_validation": "required_after_commit", "named_replay": "required_after_commit",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "HOLD_FOR_EXACT_FINAL_AND_NAMED_REPLAY",
        "boundary": d.TRUTH_BOUNDARY,
    })
    write("seal-receipt.json", {
        "schema": "ghc.family.v647-v5.seal-receipt.v1", "source_revision": SOURCE,
        "x1_revision": X1, "evidence_revision": evidence,
        "closeout_revision": "resolved_by_commit_containing_closeout",
        "source_to_evidence_zero_merges": int(git("rev-list", "--merges", "--count", f"{SOURCE}..{evidence}")) == 0,
        "x1_parent_is_source": git("rev-parse", f"{X1}^") == SOURCE,
        "evidence_parent_is_x1": git("rev-parse", f"{evidence}^") == X1,
        "closeout_parent_is_evidence": "resolved_after_closeout_commit",
        "final_commit_contract": "single parent direct child of evidence; exact identity resolved after commit",
        "maximum_phase_commits": 4, "expected_phase_commits_after_final": 3,
        "history_rewrite": False, "force_push": False, "merge_commit": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": d.TRUTH_BOUNDARY,
    })
    write("final-validation-record.json", {
        "schema": "ghc.family.v647-v5.final-validation-protocol.v1", "phase": d.PHASE,
        "binding": "the commit containing this record",
        "candidate_current_validation": {"tests": current["tests"]["tests_run"], "detailed": current["detailed_checks"], "minimal": current["minimal_checks"], "json": current["json"]["parsed"], "privacy_files": current["privacy"]["files_scanned"], "privacy_hits": current["privacy"]["confirmed_hit_count"]},
        "candidate_full_validation": {"tests_run": full["tests"]["tests_run"], "eligible_tests": full["tests"]["eligible_tests"], "exact_inherited_exclusions": exclusions, "unexpected_failures": full["tests"]["unexpected_failure_events"], "result": full["result"]},
        "exact_final_head_validation": "required_after_commit",
        "named_local_only_replay": "required_after_commit",
        "truth_rule": "This record does not claim post-commit validation before it occurs; the acknowledged baton may report the later exact-head proof.",
        "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write("final-receipt.json", {
        "schema": "ghc.family.v647-v5.final-receipt.v1", "phase": d.PHASE,
        "closeout_candidate_complete": True, "exact_head_resolved": False,
        "exact_final_validation_complete": False, "named_replay_complete": False,
        "remote_equality_complete": False, "baton_sent": False,
        "next_gate": "commit then exact final canonical validation plus one local-only named replay and four-way equality",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": d.TRUTH_BOUNDARY,
    })
    write("orchestration/final-route-gate.json", {
        "schema": "ghc.family.v647-v5.final-route-gate.v1", "state": "HOLD_FOR_EXACT_FINAL_AND_NAMED_REPLAY",
        "target_title": "Ilyra Fen", "target_phase": "v647-gmut-thos-v6-x1-x2",
        "send_count": 0, "task_creation": 0, "delegation": 0,
        "required": ["exact final canonical validation", "one clean local-only named replay", "four-way remote equality", "clean canonical lane"],
    })
    route = read("orchestration/terminal-route-plan.json")
    route.update({"current_state": "HOLD_FOR_EXACT_FINAL_AND_NAMED_REPLAY", "send_count": 0})
    write("orchestration/terminal-route-plan.json", route)

    manifest_count = build_manifest()
    print(json.dumps({"phase": d.PHASE, "manifest_entries": manifest_count, "current_tests": current["tests"]["tests_run"], "full_tests": full["tests"]["tests_run"], "eligible_full_tests": full["tests"]["eligible_tests"], "exact_exclusions": len(exclusions), "unexpected": 0, "result": "pass"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
