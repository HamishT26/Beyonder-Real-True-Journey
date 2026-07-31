#!/usr/bin/env python3
"""Build Lyren v657-v1 final candidate records without preclaiming success."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v657_v1_final_config as c
import ghc_family_v657_v1_phase_data as d


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
        "schema": "ghc.family.v657-v1.closeout-manifest-replay.v1",
        "commit": commit,
        "entry_count": manifest["entry_count"],
        "mismatches": mismatches,
        "valid": not mismatches,
    }


def method_and_witnesses(
    negative: dict[str, Any],
    ordinal: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    method_id = f"V6571-FINAL-METHOD-{ordinal:02d}"
    failed_id = f"V6571-FINAL-WITNESS-{ordinal:02d}-F"
    passing_id = f"V6571-FINAL-WITNESS-{ordinal:02d}-P"
    method = {
        "method_id": method_id,
        "title": f"Bounded recovery for {negative['slug']}",
        "trigger_preconditions": [negative["slug"]],
        "failure_signature": negative["failure_signature"],
        "candidate_workaround": negative["candidate_workaround"],
        "recurrence_guard": negative["recurrence_guard"],
        "approval_class": "safe_now_owner_local_final_preparation_recovery",
        "privacy_class": "sanitized_public",
        "scope_boundary": negative["scope_boundary"],
        "rollback": "Retain the failed attempt at zero credit and leave sibling and external state unchanged.",
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
            "expected": "The bounded final-preparation operation establishes only its stated postcondition.",
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
            "expected": "Only Lyren's bounded final-preparation recovery is checked.",
            "observed": negative["pass_observed"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": negative["scope_boundary"],
        },
    ]
    return method, witnesses


def build() -> None:
    if git("rev-parse", "HEAD") != c.CLOSEOUT_COMMIT:
        raise RuntimeError("final builder requires the exact closeout head")
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
        method, pair = method_and_witnesses(negative, ordinal)
        methods.append(method)
        witnesses.extend(pair)
    current_count = len(c.FINAL_PREPARATION_NEGATIVES)
    effective_negatives = c.CLOSEOUT_EFFECTIVE_NEGATIVES + current_count
    effective_methods = c.CLOSEOUT_EFFECTIVE_METHODS + current_count
    write_json(
        "truth/retained-negative-register-final.json",
        {
            "schema": "ghc.family.v657-v1.retained-negatives.final.v1",
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
                "path": "docs/lyren-moss/v657-v1/method-flow/method-flow-state-closeout.json",
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
            "schema": "ghc.family.v657-v1.phase-truth.final-candidate.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_commit": c.SOURCE_COMMIT,
            "x1_commit": c.X1_COMMIT,
            "evidence_commit": c.EVIDENCE_COMMIT,
            "closeout_commit": c.CLOSEOUT_COMMIT,
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
        },
    )
    write_json(
        "lifecycle/final-record.json",
        {
            "schema": "ghc.family.v657-v1.final-record.v1",
            "record_state": "CANDIDATE_TREE_REVIEWED_POSTCOMMIT_PROOF_PENDING",
            "source_commit": c.SOURCE_COMMIT,
            "x1_commit": c.X1_COMMIT,
            "evidence_commit": c.EVIDENCE_COMMIT,
            "closeout_commit": c.CLOSEOUT_COMMIT,
            "final_commit": None,
            "canonical_aggregate_state": "POSTCOMMIT_REQUIRED",
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
            "schema": "ghc.family.v657-v1.terminal-route-state.v1",
            "state": "PREPARED_NOT_SENT",
            "next_exact_title": "Ilyra Fen",
            "next_phase": "v657-v2",
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
        "validation/canonical-aggregate-plan.json",
        {
            "schema": "ghc.family.v657-v1.canonical-aggregate-plan.v1",
            "state": "POSTCOMMIT_REQUIRED",
            "completed": False,
            "route_sent": False,
            "one_successful_pass_only": True,
            "replay_after_success_forbidden": True,
            "selected_test_scopes": [
                "ten context-valid frozen x1 tests",
                "complete current x2 module",
                "complete closeout module",
                "complete final module",
                "bounded Lyren-owned Ilyra successor-scope module",
            ],
            "additional_checks": [
                "detailed and minimal validators",
                "all phase JSON",
                "five-class privacy scan",
                "x1, evidence, closeout, and final owner manifests",
                "stale labels and diff hygiene",
                "exact source-to-final ancestry",
                "four phase commits, one parent each, zero merges",
                "exact head, clean before and after, zero divergence, and four-way live equality",
            ],
            "external_receipt_required": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final-seal-receipt.json",
        {
            "schema": "ghc.family.v657-v1.final-seal-candidate.v1",
            "closeout_commit": c.CLOSEOUT_COMMIT,
            "closeout_manifest_entries": replay["entry_count"],
            "closeout_manifest_replay_valid": replay["valid"],
            "closeout_staged_review_valid": closeout_review["valid"],
            "closeout_validation_valid": closeout_validation["valid"],
            "final_tree_ready_for_exact_staged_review": True,
            "exact_final_known_inside_own_tree": False,
            "canonical_aggregate_completed": False,
            "route_state": "PREPARED_NOT_SENT",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final-complete-incomplete-checklist-terminal-candidate.json",
        {
            "schema": "ghc.family.v657-v1.terminal-checklist.candidate.v1",
            "complete_now": [
                "source, x1, evidence, and closeout anchors",
                "strict x1-before-x2",
                "thirty proposal outcomes and one hundred fifty mutations",
                "all retained negatives through final preparation",
                "skills, runners, reports, wellbeing, source and proposal ledgers",
                "evidence and closeout manifests, staged reviews, and content seals",
                "prepared unsent Ilyra baton",
            ],
            "pending_postcommit": [
                "exact final hash and direct-parent proof",
                "one canonical aggregate",
                "fresh live equality and clean after-state",
                "one acknowledged Ilyra activation",
            ],
            "incomplete_external": [
                "real repositories, services, vulnerabilities, incidents, patches, releases, deployments, participant impact, and operational evidence",
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
        "deliverables/v657-v1-final-candidate-overview.md",
        f"""# Lyren Moss v657-v1 final candidate overview

The final candidate preserves thirty bounded synthetic surfaces with 23 completed, 5 represented, 1 open gap, and 1 exact gate. It retains {effective_negatives:,} effective negatives, {c.OPEN_GAPS} open gaps, {c.EXACT_GATES} exact gates, and {effective_methods:,} Method Flow fail/pass pairs. Freed ID/CBR Heart remains the primary pillar through public-interest software repair provenance, disclosure, correction, contestation, maintainer-role, accessible-notice, sensitive-publication, remedy, and authority-reservation contracts; GMUT Mind and THOS Body remain explicit and protected.

The exact final hash, canonical aggregate, live equality, and acknowledged route are intentionally absent from this containing tree. They are postcommit facts and must be recorded in an external D-first receipt and the one acknowledged Ilyra activation. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Lyren Moss, they/them, is relational working language only. It is not evidence of consciousness, personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency.
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
