#!/usr/bin/env python3
"""Build the combined v647-v7 closeout and seal-candidate packet."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v647-v7"
SOURCE = "c02273291edcbe408f28647495183e9ed4641995"
X1 = "54bc352a9d57f81229261f0894e3affd35fc7ebc"
EVIDENCE = "8fc7f7b3b779122fc4b27df1bcd97316a952f8a6"
EVIDENCE_NEGATIVES = 3745
FINAL_EFFECTIVE_NEGATIVES = 3749
LIFECYCLE_NEGATIVES = [
    {
        "negative_id": "V6477-LC-N01",
        "failure": "A parallel closeout preflight inherited a ten-second member timeout and returned no attributable result before the slowest Windows shell startup completed.",
        "recovery": "Retain the timeout, isolate each probe, disable login-profile semantics, and use a bounded sixty-second startup envelope.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6477-LC-N02",
        "failure": "A read-only PowerShell inspection string containing a mixed Unicode alternation was rejected as an unterminated quoted string before file access.",
        "recovery": "Retain the parser fault, use a literal single-quoted ASCII search, read exact paths separately, and verify Unicode bytes with Python.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6477-LC-N03",
        "failure": "The first closeout validator retained evidence-boundary Method Flow parity after two lifecycle failures were appended, so its detailed and minimal parity checks failed despite 67 passing tests and a zero-hit privacy scan.",
        "recovery": "Retain the failed receipt, declare evidence and closeout count domains separately, and require exact lifecycle parity in the final validator.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6477-LC-N04",
        "failure": "A compound read-only ripgrep alternation returned early numeric matches and then treated a quote-bearing fragment as an invalid Windows filename.",
        "recovery": "Retain the recurrence witness and use separate literal ASCII search terms without quote-bearing alternation fragments.",
        "result": "retained_then_recovered",
    },
]


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, data: dict) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, text: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def build() -> None:
    truth = load("phase-truth.json")
    validation = load("validation/evidence-validation.json")
    methods = load("method-flow/method-flow-state.json")
    if not validation["valid"] or not truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20":
        raise RuntimeError("evidence validation or terminal abstention is not ready for closeout")
    if methods["counts"]["witness_results"] != {"fail": 10, "pass": 10}:
        raise RuntimeError("Method Flow witness parity is incomplete")

    write_json("validation/lifecycle-operational-negatives.json", {
        "schema": "ghc.family.v647-v7.lifecycle-operational-negatives.v1",
        "evidence_boundary_total": EVIDENCE_NEGATIVES,
        "count": len(LIFECYCLE_NEGATIVES),
        "negatives": LIFECYCLE_NEGATIVES,
        "all_retained": True,
        "erased_negative_count": 0,
    })
    write_json("retained-negative-register-final.json", {
        "schema": "ghc.family.v647-v7.final-retained-negatives.v1",
        "inherited_and_evidence_negatives": EVIDENCE_NEGATIVES,
        "lifecycle_operational_negatives": len(LIFECYCLE_NEGATIVES),
        "effective_total": FINAL_EFFECTIVE_NEGATIVES,
        "erased_negative_count": 0,
        "boundary": "Workflow failures remain operational negatives. Their bounded recovery is not scientific, production, authority, security, or independent-reproduction evidence.",
    })

    write_json("lifecycle/phase-anchor-contract.json", {
        "schema": "ghc.family.v647-v7.phase-anchor-contract.v1", "source_commit": SOURCE,
        "x1_commit": X1, "evidence_commit": EVIDENCE, "expected_phase_commit_count_at_final": 3,
        "maximum_phase_commits": 4, "expected_merge_count": 0, "expected_final_parent_count": 1,
        "history_rewrite_allowed": False, "force_push_allowed": False,
    })
    write_json("closeout-receipt.json", {
        "schema": "ghc.family.v647-v7.closeout.v1", "owner": "Sable Rook", "source_commit": SOURCE,
        "x1_commit": X1, "evidence_commit": EVIDENCE, "outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "safe_now_completed": 30, "candidates_completed": 20, "skills_validated_and_used": 20,
        "runners_invoked": 10, "cleanup_completed": 30, "synthetic_negatives_rejected": 70,
        "effective_negatives": FINAL_EFFECTIVE_NEGATIVES, "effective_open_gaps": 24, "effective_exact_gates": 25,
        "method_fail_witnesses": 10, "method_pass_witnesses": 10,
        "full_repository_suite_run": False, "full_repository_suite_owner": "Eiren Kestrel",
        "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "PREPARED_NOT_SENT",
    })
    write_json("seal-receipt.json", {
        "schema": "ghc.family.v647-v7.seal.v1", "state": "CLOSEOUT_AND_SEAL_CANDIDATE",
        "source_commit": SOURCE, "x1_commit": X1, "evidence_commit": EVIDENCE,
        "final_commit": None, "final_commit_known_at_commit_time": False,
        "postcommit_exact_head_validation_required": True, "named_replay_required": True,
        "remote_equality_required": True, "baton_send_allowed_now": False,
        "boundary": "A commit cannot contain its own not-yet-created identifier. Postcommit proof must be external and read-only.",
    })
    write_json("lifecycle/final-record.json", {
        "schema": "ghc.family.v647-v7.final-record.v1", "state": "POST_COMMIT_REQUIRED",
        "final_commit": None, "exact_final_validated": False, "canonical_clean": False,
        "four_way_remote_equal": False, "named_replay_passed": False,
        "independent_reproduction": False, "baton_sent": False,
    })
    write_json("validation/final-validation-protocol.json", {
        "schema": "ghc.family.v647-v7.final-validation-protocol.v1", "state": "POST_COMMIT_REQUIRED",
        "completed": False, "preclaims_exact_final_head": False,
        "canonical_requirements": ["67 closeout-enabled tests", "detailed validator", "minimal validator", "complete JSON parse", "five-class privacy scan", "owner-manifest parity", "source x1 evidence ancestry", "three phase commits", "zero merges", "one final parent", "clean before and after", "four-way remote equality"],
        "named_replay_requirements": ["one named local-only branch and worktree", "exact final head", "no upstream", "no live remote ref", "same bounded validation once", "clean before and after"],
        "full_repository_suite": "not run; Eiren-only under current refinement",
    })
    write_json("reproduction/same-owner-replay-plan.json", {
        "schema": "ghc.family.v647-v7.same-owner-replay.v1", "state": "PENDING_POST_COMMIT",
        "named_lane_count": 1, "detached": False, "push_allowed": False, "upstream_allowed": False,
        "live_remote_ref_allowed": False, "same_owner_only": True, "independent_reproduction": False,
    })
    write_json("orchestration/successor-baton-preparation.json", {
        "schema": "ghc.family.v647-v7.successor-baton-preparation.v1", "target_existing_task_title": "Orin Thale",
        "target_phase": "v647-gmut-thos-v8-x1-x2", "state": "PREPARED_NOT_SENT",
        "task_creation_authorized": False, "fork_authorized": False, "extra_confirmation_authorized": False,
        "send_only_after": ["exact final validation", "one named replay", "canonical clean", "four-way remote equality"],
    })
    write_json("orchestration/terminal-route-state.json", {
        "schema": "ghc.family.v647-v7.terminal-route-state.v1", "state": "PREPARED_NOT_SENT",
        "message_sent": False, "task_created": False, "task_forked": False, "subagent_spawned": False,
        "standby_sibling_messaged": False, "raw_task_identifier_present": False,
    })
    write_json("final-complete-incomplete-checklist.json", {
        "schema": "ghc.family.v647-v7.final-checklist.v1",
        "complete": ["verified source inheritance", "dedicated x1 freeze", "ten executed proposal surfaces", "six completed outcomes", "two represented outcomes", "one open gap", "one exact gate", "seventy retained synthetic negatives", "thirty safe-now tasks", "twenty candidate prototypes", "twenty phase-local skills", "ten family-compatible runners", "thirty additive cleanup tasks", "threat model", "wellbeing receipt", "accessible static report", "evidence validation"],
        "pending_postcommit": ["exact final identifier", "canonical final validation", "one named local-only replay", "final four-way remote equality", "single Orin baton"],
        "incomplete_external": ["real SPT-3G analysis", "blind matched-budget THOS arms", "production Freed ID", "affected-party legal cultural and Māori authority", "manual and affected-user accessibility review", "independent security review", "independent-team reproduction", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.suffix.lower() not in {".md", ".html"}:
            continue
        words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8", errors="replace")))
        documents.append({"path": path.relative_to(PHASE).as_posix(), "words": words})
    write_json("validation/document-cap-receipt.json", {
        "schema": "ghc.family.v647-v7.document-cap.v1", "document_count": len(documents),
        "maximum_words": max(row["words"] for row in documents), "all_under_6000": all(row["words"] <= 6000 for row in documents),
        "overview_words": next(row["words"] for row in documents if row["path"] == "deliverables/v647-v7-final-integrated-overview.md"),
        "documents": documents,
    })
    write_json("validation/final-validation-candidate.json", {
        "schema": "ghc.family.v647-v7.final-validation-candidate.v1", "evidence_validation_valid": True,
        "evidence_tests": validation["tests"]["tests_run"], "detailed_checks": validation["detailed_check_count"],
        "minimal_checks": validation["minimal_check_count"], "json_parses": validation["json_parse_count"],
        "privacy_files": validation["privacy_file_count"], "privacy_hits": len(validation["privacy_hits"]),
        "closeout_validation_pending": True, "exact_final_validation_pending": True, "named_replay_pending": True,
    })
    truth["lifecycle"] = "closeout_and_seal_candidate"
    truth["route_state"] = "PREPARED_NOT_SENT"
    truth["postcommit_validation_pending"] = True
    truth["effective_negatives"] = FINAL_EFFECTIVE_NEGATIVES
    truth["evidence_boundary_negatives"] = EVIDENCE_NEGATIVES
    truth["lifecycle_operational_negatives"] = len(LIFECYCLE_NEGATIVES)
    write_json("phase-truth.json", truth)
    write_json("tooling/ghc-family-index.json", {
        "schema": "ghc.family.v647-v7.index.v1", "phase": "v647-gmut-thos-v7-x1-x2", "owner": "Sable Rook",
        "lifecycle": "closeout_and_seal_candidate", "source_revision": SOURCE, "x1_commit": X1, "evidence_commit": EVIDENCE,
        "frozen_proposals": 10, "chain_proposals": 540, "outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "effective_negatives": FINAL_EFFECTIVE_NEGATIVES, "open_gaps": 24, "exact_gates": 25,
        "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_text("tooling/ghc-family-index.md", """# GHC Family Index — v647-v7 closeout candidate

Owner: Sable Rook. Ten proposals: 6 completed, 2 represented, 1 open_gap, 1 exact_gate. Effective negatives: 3,749, including four retained closeout workflow failures after the 3,745-negative evidence boundary. Twenty-four open gaps and twenty-five exact gates remain. Exact final validation, one named replay, remote equality, and the single Orin baton remain postcommit gates. Terminal verdict: NOT_READY_FOR_STAGE_20.
""")


if __name__ == "__main__":
    build()
