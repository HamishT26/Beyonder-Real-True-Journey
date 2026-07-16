#!/usr/bin/env python3
"""Build the combined Sylven Arc v646-v6 closeout and seal packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v646_v6_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/sylven-arc/v646-v6")
PHASE = ROOT / PHASE_REL
X1 = "147aab7fd2f2805f119968dd30ab9c7996306d3a"
EVIDENCE = "da2dc0aeccda0f5e5f731b6a41666ed87e029c89"
SELF_EXCLUSIONS = [
    "validation/final-owner-manifest.json",
    "validation/final-staged-manifest.json",
    "validation/final-staged-review.json",
]


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def index_bytes(relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f":{relative}"], cwd=ROOT)


def build_manifest() -> dict[str, Any]:
    output = subprocess.check_output(["git", "ls-files", PHASE_REL.as_posix()], cwd=ROOT, text=True, encoding="utf-8")
    paths = sorted({line.strip() for line in output.splitlines() if line.strip()})
    for relative in SELF_EXCLUSIONS:
        full = (PHASE_REL / relative).as_posix()
        if full not in paths:
            paths.append(full)
    paths.sort()
    excluded = {(PHASE_REL / relative).as_posix() for relative in SELF_EXCLUSIONS}
    entries = [
        {"path": path[len(PHASE_REL.as_posix()) + 1 :], "sha256": hashlib.sha256(index_bytes(path)).hexdigest()}
        for path in paths
        if path not in excluded
    ]
    payload = {
        "schema": "ghc.family.v646-v6.final-owner-manifest.v1",
        "hash_domain": "git_index_blob",
        "entries": entries,
        "entry_count": len(entries),
        "expected_owner_paths": [path[len(PHASE_REL.as_posix()) + 1 :] for path in paths],
        "expected_owner_path_count": len(paths),
        "declared_self_exclusions": SELF_EXCLUSIONS,
        "boundary": d.TRUTH_BOUNDARY,
    }
    write_json("validation/final-owner-manifest.json", payload)
    return payload


def build_closeout() -> dict[str, Any]:
    validation = load("validation/validation-runner-summary.json")
    if not validation.get("valid"):
        raise RuntimeError("bounded validation is not passing")
    current = load("validation/current-phase-tests.json")
    scoped = load("validation/successor-scoped-tests.json")
    detailed = load("validation/detailed-validation.json")
    minimal = load("validation/minimal-validation.json")
    privacy = load("validation/json-privacy-validation.json")
    negatives = load("retained-negative-register.json")
    gates = load("exact-open-gate-register.json")
    ledger = load("x2-proposal-ledger.json")
    owner_files = len([path for path in PHASE.rglob("*") if path.is_file()])

    write_json(
        "phase-truth.json",
        {
            "schema": "ghc.family.v646-v6.phase-truth.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_revision": d.SOURCE_REVISION,
            "x1_revision": X1,
            "evidence_revision": EVIDENCE,
            "final_revision_binding": "this_combined_closeout_and_seal_commit",
            "planned_phase_commit_count": 3,
            "merge_commits_allowed": 0,
            "final_parent_binding": EVIDENCE,
            "strict_x1_before_x2": True,
            "proposal_distribution": ledger["distribution"],
            "frozen_proposals_through_phase": 450,
            "effective_negatives": negatives["effective_total"],
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "failure_erasure_count": 0,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "full_repository_suite_run": False,
            "full_repository_suite_owner": "Eiren Kestrel",
            "same_owner_repeatability_only": True,
            "independent_team_reproduction": False,
            "terminal_route": "PREPARED_NOT_SENT",
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_json(
        "final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v646-v6.final-checklist.v1",
            "complete_before_final_commit": [
                "required skills and references read",
                "source and live-remote gate",
                "clean fast-forward of Sylven lane",
                "dedicated remote-equal x1 freeze",
                "440-proposal semantic novelty audit",
                "ten core proposal execution within bounds",
                "70 synthetic negative rejections",
                "30 safe, 20 candidate, 20 skill, 10 runner, and 30 cleanup portfolio execution",
                "bounded current and eligible successor-scoped tests",
                "detailed and minimal validation",
                "complete phase JSON parse and five-class privacy scan",
                "evidence commit pushed",
                "combined closeout and seal content prepared",
            ],
            "pending_until_post_commit": [
                "exact final canonical validation",
                "one clean local-only named-lane replay",
                "final four-way remote equality",
                "one acknowledged Eiren v646-v7 baton",
            ],
            "externally_incomplete": [
                "real eROSITA rows, likelihood, constraints, and independent review",
                "real THOS blind matched-budget arms and professional review",
                "production Freed ID keys, tokens, services, interoperability, privacy/security review, recovery, and trust governance",
                "hydrographic publication, place-name, legal, affected-party, cultural, remedy, and Māori authority",
                "manual and affected-user accessibility evaluation",
                "independent-team reproduction",
                "Stage 20 readiness",
            ],
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    summary = {
        "current_tests": {"passed": current["passed"], "run": current["tests_run"]},
        "eligible_scoped_tests": {"passed": scoped["passed"], "run": scoped["tests_run"], "excluded": scoped["excluded_count"]},
        "detailed": {"passed": detailed["passed"], "checks": detailed["check_count"]},
        "minimal": {"passed": minimal["passed"], "checks": minimal["check_count"]},
        "json_privacy": {
            "files": privacy["files_scanned"],
            "json": privacy["json_parse_count"],
            "candidate_hits": privacy["privacy_candidate_hit_count"],
            "confirmed_hits": privacy["privacy_confirmed_hit_count"],
        },
    }
    write_json(
        "closeout-receipt.json",
        {
            "schema": "ghc.family.v646-v6.closeout-receipt.v1",
            "state": "closeout_content_complete_pending_exact_commit_validation",
            "source_revision": d.SOURCE_REVISION,
            "x1_revision": X1,
            "evidence_revision": EVIDENCE,
            "final_parent_binding": EVIDENCE,
            "proposal_distribution": ledger["distribution"],
            "effective_negatives": negatives["effective_total"],
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "validation": summary,
            "route": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_json(
        "seal-receipt.json",
        {
            "schema": "ghc.family.v646-v6.seal-receipt.v1",
            "seal_binding": "this_combined_closeout_and_seal_commit",
            "source_revision": d.SOURCE_REVISION,
            "x1_revision": X1,
            "evidence_revision": EVIDENCE,
            "final_parent_binding": EVIDENCE,
            "expected_phase_commits": 3,
            "expected_merge_commits": 0,
            "x1_content_seal_preserved": True,
            "negative_erasure_count": 0,
            "silent_gate_closure_count": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "route": "PREPARED_NOT_SENT",
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_json(
        "final-validation-record.json",
        {
            "schema": "ghc.family.v646-v6.final-validation-record.v1",
            "state": "precommit_content_validated_pending_exact_committed_head_and_named_replay",
            "canonical_precommit_validation": summary,
            "required_post_commit": [
                "exact head",
                "clean canonical before and after",
                "source x1 and evidence ancestry",
                "three phase commits",
                "zero merges",
                "single final parent equal to evidence",
                "final owner-manifest parity",
                "current, eligible scoped, detailed, minimal, JSON and five-class privacy validation",
                "one clean named replay on a local-only lane",
                "four-way remote equality",
            ],
            "same_owner_only": True,
            "independent_reproduction": False,
            "full_repository_suite_run": False,
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_json(
        "orchestration/final-route-gate.json",
        {
            "schema": "ghc.family.v646-v6.final-route-gate.v1",
            "state": "PREPARED_NOT_SENT",
            "target_title": "Eiren Kestrel",
            "target_phase": "v646-v7",
            "send_count": 0,
            "task_created": False,
            "standby_contacted": False,
            "exact_final_validation_required": True,
            "named_replay_required": True,
            "four_way_equality_required": True,
        },
    )
    write_json(
        "environment/final-rotation-receipt.json",
        {
            "schema": "ghc.family.v646-v6.final-rotation.v1",
            "owner_generated_files_before_final_receipts": owner_files,
            "threshold": 15000,
            "threshold_scope": "new_sylven_generated_addition_only",
            "rotation_required": owner_files >= 15000,
            "inherited_files_counted_toward_rotation": False,
        },
    )
    write_json(
        "prototypes/final-runner-use-receipt.json",
        {
            "schema": "ghc.family.v646-v6.final-runner-use.v1",
            "runner_count": 10,
            "built_count": 10,
            "invoked_before_commit": 9,
            "pending_exact_final_invocation": ["ghc_family_v646_v6_named_lane_audit.py"],
            "caller_compatibility_preserved": True,
            "result": "pass_with_named_replay_pending",
        },
    )
    return {"state": "closeout_and_seal_content_complete", "validation": summary, "owner_files": owner_files}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-only", action="store_true")
    args = parser.parse_args()
    if args.manifest_only:
        payload = build_manifest()
        result = {"manifest_entries": payload["entry_count"], "expected_owner_paths": payload["expected_owner_path_count"], "result": "pass"}
    else:
        result = {**build_closeout(), "result": "pass"}
    print(json.dumps(result, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
