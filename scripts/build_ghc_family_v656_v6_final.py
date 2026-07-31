#!/usr/bin/env python3
"""Build Elaren v656-v6 final candidate records without preclaiming success."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v656_v6_final_config as c
import ghc_family_v656_v6_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
BOUNDARY = (
    "Candidate final-tree record only. Exact final, live equality, canonical "
    "aggregate, and route delivery remain postcommit facts. Same-owner evidence "
    "is not independent reproduction or external authority."
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any, *, compact: bool = False) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(
        payload,
        ensure_ascii=False,
        indent=None if compact else 2,
        separators=(",", ":") if compact else None,
        sort_keys=True,
    )
    path.write_text(text + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def tree_map(commit: str) -> dict[str, str]:
    mapping = {}
    for line in git("ls-tree", "-r", commit).splitlines():
        metadata, path = line.split("\t", 1)
        _, kind, oid = metadata.split()
        if kind == "blob":
            mapping[path] = oid
    return mapping


def replay_manifest(relative: str, commit: str) -> dict[str, Any]:
    manifest = load(relative)
    tree = tree_map(commit)
    mismatches = []
    for entry in manifest["entries"]:
        observed = tree.get(entry["path"])
        if observed != entry["git_blob"]:
            mismatches.append(
                {
                    "path": entry["path"],
                    "expected": entry["git_blob"],
                    "observed": observed,
                }
            )
    return {
        "schema": "ghc.family.v656-v6.closeout-manifest-replay.v1",
        "commit": commit,
        "entry_count": manifest["entry_count"],
        "mismatches": mismatches,
        "valid": not mismatches,
    }


def method_and_witnesses(
    negative: dict[str, Any], ordinal: int
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    method_id = f"V6566-FINAL-METHOD-{ordinal:02d}"
    failed_id = f"V6566-FINAL-WITNESS-{ordinal:02d}-F"
    passing_id = f"V6566-FINAL-WITNESS-{ordinal:02d}-P"
    method = {
        "method_id": method_id,
        "title": f"Bounded recovery for {negative['slug']}",
        "trigger_preconditions": [negative["slug"]],
        "failure_signature": negative["failure_signature"],
        "candidate_workaround": negative["candidate_workaround"],
        "recurrence_guard": negative["recurrence_guard"],
        "approval_class": negative.get(
            "approval_class", "safe_now_owner_local_route_contract_recovery"
        ),
        "privacy_class": "sanitized_public",
        "scope_boundary": negative["scope_boundary"],
        "rollback": negative.get(
            "rollback",
            "Retain the absence at zero credit and do not contact or act for the successor.",
        ),
        "protected_gates": d.PROTECTED_GATES,
        "retained_negative_ids": [negative["negative_id"]],
        "validation_witness_ids": [failed_id, passing_id],
        "recommendation_state": "preferred",
        "supersedes": [],
    }
    witnesses = [
        {
            "witness_id": failed_id,
            "method_id": method_id,
            "result": "fail",
            "procedure": negative["fail_procedure"],
            "expected": negative.get(
                "fail_expected",
                "An existing bounded successor-scope module is discoverable.",
            ),
            "observed": negative["fail_observed"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Zero route-coverage credit.",
        },
        {
            "witness_id": passing_id,
            "method_id": method_id,
            "result": "pass",
            "procedure": negative["pass_procedure"],
            "expected": negative.get(
                "pass_expected",
                "Only Elaren's prepared successor-route contract is checked.",
            ),
            "observed": negative["pass_observed"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": negative["scope_boundary"],
        },
    ]
    return method, witnesses


def build() -> None:
    if git("rev-parse", "HEAD") != c.ORIGINAL_FINAL_COMMIT:
        raise RuntimeError(
            "validation-correction builder requires the exact original final candidate"
        )
    if git("rev-parse", f"{c.ORIGINAL_FINAL_COMMIT}^") != c.CLOSEOUT_COMMIT:
        raise RuntimeError("original final candidate is not the direct child of closeout")
    if git("rev-parse", f"{c.CLOSEOUT_COMMIT}^") != c.EVIDENCE_COMMIT:
        raise RuntimeError("closeout is not the direct child of evidence")
    closeout_review = load("validation/closeout-staged-review.json")
    closeout_validation = load("validation/closeout-validation.json")
    if closeout_review["valid"] is not True or closeout_validation["valid"] is not True:
        raise RuntimeError("closeout state is not valid")
    replay = replay_manifest(
        "validation/closeout-content-manifest.json", c.CLOSEOUT_COMMIT
    )
    if not replay["valid"]:
        raise RuntimeError("closeout manifest replay failed")
    write_json("validation/closeout-manifest-commit-replay.json", replay)

    methods = []
    witnesses = []
    for ordinal, negative in enumerate(c.FINAL_PREPARATION_NEGATIVES, start=1):
        method, method_witnesses = method_and_witnesses(negative, ordinal)
        methods.append(method)
        witnesses.extend(method_witnesses)
    current_count = len(c.FINAL_PREPARATION_NEGATIVES)
    effective_negatives = c.CLOSEOUT_EFFECTIVE_NEGATIVES + current_count
    effective_methods = c.CLOSEOUT_EFFECTIVE_METHODS + current_count
    write_json(
        "truth/retained-negative-register-final.json",
        {
            "schema": "ghc.family.v656-v6.retained-negatives.final.v1",
            "closeout_effective_count": c.CLOSEOUT_EFFECTIVE_NEGATIVES,
            "final_preparation_count": current_count,
            "final_preparation_negatives": c.FINAL_PREPARATION_NEGATIVES,
            "effective_count": effective_negatives,
            "all_retained": True,
        },
        compact=True,
    )
    write_json(
        "method-flow/method-flow-state-final.json",
        {
            "schema": "ghc.family.method-flow-state.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "final_candidate",
            "inherited_anchor": {
                "path": "docs/elaren-kestrel/v656-v6/method-flow/method-flow-state-closeout.json",
                "effective_methods": c.CLOSEOUT_EFFECTIVE_METHODS,
                "effective_fail_witnesses": c.CLOSEOUT_EFFECTIVE_METHODS,
                "effective_pass_witnesses": c.CLOSEOUT_EFFECTIVE_METHODS,
            },
            "current_methods": methods,
            "current_witnesses": witnesses,
            "counts": {
                "current_methods": current_count,
                "current_witness_results": {
                    "fail": current_count,
                    "pass": current_count,
                },
                "effective_methods": effective_methods,
                "effective_witness_results": {
                    "fail": effective_methods,
                    "pass": effective_methods,
                },
            },
            "all_failed_witnesses_retained": True,
            "independent_reproduction": False,
        },
        compact=True,
    )
    outcomes = load("x2/proposal-ledger.json")["outcome_counts"]
    write_json(
        "truth/phase-truth-final-candidate.json",
        {
            "schema": "ghc.family.v656-v6.phase-truth.final-candidate.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_commit": c.SOURCE_COMMIT,
            "x1_commit": c.X1_COMMIT,
            "evidence_commit": c.EVIDENCE_COMMIT,
            "closeout_commit": c.CLOSEOUT_COMMIT,
            "original_final_commit": c.ORIGINAL_FINAL_COMMIT,
            "final_commit": None,
            "outcome_counts": outcomes,
            "effective_negatives": effective_negatives,
            "effective_open_gaps": c.OPEN_GAPS,
            "effective_exact_gates": c.EXACT_GATES,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner_only": True,
            "independent_reproduction": False,
            "canonical_aggregate_completed": False,
            "failed_canonical_attempts": 1,
        },
    )
    write_json(
        "lifecycle/final-record.json",
        {
            "schema": "ghc.family.v656-v6.final-record.v1",
            "record_state": "CANDIDATE_TREE_REVIEWED_POSTCOMMIT_PROOF_PENDING",
            "source_commit": c.SOURCE_COMMIT,
            "x1_commit": c.X1_COMMIT,
            "evidence_commit": c.EVIDENCE_COMMIT,
            "closeout_commit": c.CLOSEOUT_COMMIT,
            "original_final_commit": c.ORIGINAL_FINAL_COMMIT,
            "final_commit": None,
            "canonical_aggregate_state": "FAILED_ZERO_CREDIT_CORRECTION_REQUIRED",
            "route_state": "PREPARED_NOT_SENT",
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v656-v6.terminal-route-state.v1",
            "state": "PREPARED_NOT_SENT",
            "next_exact_title": "Neris Solane",
            "next_phase": "v656-v7",
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "tavian_sol_state": "ON_STANDBY",
            "send_gate": "exact final, clean state, four-way live equality, one successful canonical aggregate, exact-title reread, and one acknowledged send",
            "boundary": "Preparation is not delivery.",
        },
    )
    write_json(
        "validation/canonical-aggregate-failure-01.json",
        {
            "schema": "ghc.family.v656-v6.canonical-aggregate-failure.v1",
            "attempt": 1,
            "exact_head": c.ORIGINAL_FINAL_COMMIT,
            "valid": False,
            "success_credit": 0,
            "tests_run": 73,
            "detailed_checks": 322,
            "minimal_checks": 15,
            "json_parses": 195,
            "privacy_files": 258,
            "privacy_hits": 0,
            "manifest_entries": 730,
            "failed_terminal_checks": ["stale_label_review"],
            "self_referential_tokens": 3,
            "external_receipt_sha256": c.FAILED_CANONICAL_RECEIPT_SHA256,
            "retained_negative_ids": ["V6566-X2-N28"],
            "replayed_after_success": False,
            "boundary": "Failed same-owner aggregate retained at zero credit; no route or independent-reproduction credit.",
        },
    )
    write_json(
        "validation/canonical-aggregate-plan.json",
        {
            "schema": "ghc.family.v656-v6.canonical-aggregate-plan.v1",
            "state": "POSTCORRECTION_COMMIT_REQUIRED",
            "completed": False,
            "route_sent": False,
            "failed_attempts_retained": 1,
            "one_successful_pass_only": True,
            "replay_after_success_forbidden": True,
            "selected_test_scopes": [
                "ten context-valid frozen x1 tests",
                "complete current x2 module",
                "complete closeout module",
                "complete final module",
                "bounded Elaren-owned Neris successor-scope module",
            ],
            "additional_checks": [
                "detailed and minimal validators",
                "all phase JSON",
                "five-class privacy scan",
                "x1, evidence, closeout, and final owner manifests",
                "stale labels and diff hygiene",
                "exact source-to-final ancestry",
                "five phase commits, one parent each, zero merges",
                "exact head, clean before and after, zero divergence, and four-way live equality",
            ],
            "external_receipt_required": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final-seal-receipt.json",
        {
            "schema": "ghc.family.v656-v6.final-seal-candidate.v1",
            "closeout_commit": c.CLOSEOUT_COMMIT,
            "closeout_manifest_entries": replay["entry_count"],
            "closeout_manifest_replay_valid": replay["valid"],
            "closeout_staged_review_valid": closeout_review["valid"],
            "closeout_validation_valid": closeout_validation["valid"],
            "final_tree_ready_for_exact_staged_review": True,
            "exact_final_known_inside_own_tree": False,
            "canonical_aggregate_completed": False,
            "failed_canonical_attempts_retained": 1,
            "route_state": "PREPARED_NOT_SENT",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final-complete-incomplete-checklist-terminal-candidate.json",
        {
            "schema": "ghc.family.v656-v6.terminal-checklist.candidate.v1",
            "complete_now": [
                "source, x1, evidence, and closeout anchors",
                "strict x1-before-x2",
                "thirty proposal outcomes and one hundred fifty mutations",
                "all retained negatives through final preparation",
                "skills, runners, reports, wellbeing, source and proposal ledgers",
                "evidence and closeout manifests, staged reviews, and content seals",
                "prepared unsent Neris baton",
            ],
            "pending_postcommit": [
                "exact final hash and direct-parent proof",
                "one successful canonical aggregate after one retained zero-credit failure",
                "fresh live equality and clean after-state",
                "one acknowledged Neris activation",
            ],
            "incomplete_external": [
                "real wetland, participant, and professional evidence",
                "empirical GMUT and independent scientific review",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID evidence and governance",
                "legal, cultural, affected-party, data-governance, and Māori authority",
                "independent-team reproduction and Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(
        "deliverables/v656-v6-final-candidate-overview.md",
        f"""# Elaren Kestrel v656-v6 final candidate overview

The final candidate preserves thirty bounded synthetic surfaces with 23 completed, 5 represented, 1 open gap, and 1 exact gate. It retains {effective_negatives:,} effective negatives, {c.OPEN_GAPS} open gaps, {c.EXACT_GATES} exact gates, and {effective_methods:,} Method Flow fail/pass pairs. THOS Body remains the primary pillar through a wetland documentation lens; GMUT Mind and Freed ID/CBR Heart remain explicit and protected.

The original final candidate is `{c.ORIGINAL_FINAL_COMMIT}`. Its first canonical aggregate failed solely on a self-referential stale-label scanner rule and earned zero credit; that receipt is retained. The corrected exact final hash, one successful canonical aggregate, live equality, and acknowledged route remain postcommit facts. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Elaren Kestrel, they/them, is relational working language only. It is not evidence of consciousness, personhood, identity continuity, employment, qualification, professional authority, or independent agency.
""",
    )
    print(
        json.dumps(
            {
                "effective_negatives": effective_negatives,
                "effective_method_pairs": effective_methods,
                "closeout_manifest_entries": replay["entry_count"],
                "route": "PREPARED_NOT_SENT",
                "canonical_aggregate": "POSTCOMMIT_REQUIRED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
