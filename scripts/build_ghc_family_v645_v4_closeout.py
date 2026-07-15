#!/usr/bin/env python3
"""Build the bounded precommit closeout packet for Ilyra Fen v645-v4."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/ilyra-fen/v645-v4"
PHASE = "v645-gmut-thos-v4-x1-x2"
SOURCE = "3bff59204cee9a7f031b032262d45360cc310c8a"
SOURCE_SEAL = "1dfbf310a9313117c692a060b9c4e3a5ad8e1626"
X1 = "a0c2cdfac1fee23c2f5318a148f80198d251efc6"
EVIDENCE = "f7508d831736a884b4b765d54c1e3265dbb8b599"


def write_json(relative: str, payload: dict) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    identity_boundary = (
        "Ilyra Fen, she/they, is relational working language for an evidence-boundary "
        "steward. It is not evidence of consciousness, sentience, legal personhood, "
        "identity continuity, employment, professional qualification, or independent authority."
    )
    claim_boundary = (
        "This bounded software and synthetic evidence makes no empirical GMUT confirmation, "
        "THOS effectiveness, production identity, legal or cultural authority, complete "
        "accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness "
        "or personhood, Theory-of-Everything, or Stage 20 claim."
    )
    write_json(
        "closeout-receipt.json",
        {
            "schema": "ghc.family.v645-v4.closeout-receipt.v1",
            "phase": PHASE,
            "owner": "Ilyra Fen",
            "state": "PRECOMMIT_CLOSEOUT_CANDIDATE",
            "source_revision": SOURCE,
            "source_seal": SOURCE_SEAL,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "phase_commit_count_before_final": 2,
            "phase_commit_cap": 4,
            "core_distribution": {
                "completed": 6,
                "represented": 2,
                "open_gap": 1,
                "exact_gate": 1,
            },
            "expanded_workflow": {
                "safe_now_completed": 30,
                "candidate_prototypes_completed": 20,
                "skills_built_validated_used": 20,
                "runners_built_tested_used": 10,
                "clean_refine_completed": 30,
                "inherited_completion_credit_before_owner_witness": 0,
                "exact_unexecuted": 10,
                "blocked_unexecuted": 5,
            },
            "scoped_repository_tests": {"passed": 77, "total": 77},
            "full_repository_suite_run_by_ilyra": False,
            "full_repository_suite_owner": "Eiren Kestrel",
            "detailed_validation": {"passed": 68, "total": 68},
            "minimal_validation": {"passed": 27, "total": 27},
            "effective_retained_negatives": 2087,
            "open_gaps": 6,
            "exact_gates": 7,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "postcommit_requirements": [
                "exact final-head named local replay",
                "final-head four-way remote equality",
                "exactly one sanitized activation baton to the existing Sable Rook task",
            ],
            "identity_boundary": identity_boundary,
            "boundary": claim_boundary,
        },
    )
    write_json(
        "seal-receipt.json",
        {
            "schema": "ghc.family.v645-v4.seal-receipt.v1",
            "phase": PHASE,
            "state": "PRECOMMIT_SEAL_CANDIDATE",
            "source_revision": SOURCE,
            "source_seal": SOURCE_SEAL,
            "source_seal_ancestral": True,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "x1_and_evidence_four_way_equal_before_successor_stage": True,
            "strict_x1_before_x2": True,
            "source_to_evidence_zero_merges": True,
            "owner_generated_files_under_15000": True,
            "same_owner_repeatability_only": True,
            "independent_team_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "final_head_pending": True,
            "boundary": (
                "The final commit and named replay must still validate this candidate. "
                "This receipt is change-control evidence, not a signature, scientific seal, "
                "professional credential, or authority grant."
            ),
        },
    )
    write_json(
        "final-validation-record.json",
        {
            "schema": "ghc.family.v645-v4.final-validation-record.v1",
            "phase": PHASE,
            "state": "PRECOMMIT_FINAL_CANDIDATE",
            "canonical_evidence_head": EVIDENCE,
            "final_head": "SELF_PENDING_POSTCOMMIT_WITNESS",
            "canonical_scoped_tests": {"passed": 77, "total": 77},
            "canonical_detailed": {"passed": 68, "total": 68},
            "canonical_minimal": {"passed": 27, "total": 27},
            "five_class_privacy_hits": 0,
            "json_parse_issues": 0,
            "retained_negative_count": 2087,
            "open_gap_count": 6,
            "exact_gate_count": 7,
            "final_staged_review_pending": True,
            "named_replay_pending": True,
            "final_remote_equality_pending": True,
            "outbound_message_count": 0,
            "successor_task_count": 0,
            "same_owner_only": True,
            "independent_team_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": (
                "Postcommit evidence belongs in the sanitized terminal baton and task closeout "
                "because a commit cannot truthfully contain its own not-yet-created identifier."
            ),
        },
    )
    write_json(
        "validation/final-scoped-test-receipt.json",
        {
            "schema": "ghc.family.scoped-test-receipt.v1",
            "phase": PHASE,
            "scope": [
                "v645-v2 x1 and x2",
                "v645-v3 x1 and x2",
                "v645-v4 x1 and x2",
            ],
            "tests_run": 77,
            "failures": 0,
            "errors": 0,
            "full_repository_suite": False,
            "full_repository_suite_owner": "Eiren Kestrel",
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        "validation/final-ancestry-candidate.json",
        {
            "schema": "ghc.family.ancestry-candidate.v1",
            "phase": PHASE,
            "source_revision": SOURCE,
            "source_seal": SOURCE_SEAL,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "required_ancestry": [SOURCE_SEAL, SOURCE, X1, EVIDENCE],
            "required_final_parent": EVIDENCE,
            "required_source_to_final_merge_count": 0,
            "required_final_parent_count": 1,
            "state": "postcommit_verification_pending",
        },
    )
    write_json(
        "validation/named-lane-replay-plan.json",
        {
            "schema": "ghc.family.named-lane-replay-plan.v1",
            "phase": PHASE,
            "replay_count_required": 1,
            "named_branch_required": True,
            "detached_worktree_forbidden": True,
            "local_only": True,
            "push_forbidden": True,
            "scope": "the six v645-v2 through v645-v4 scoped test modules plus detailed and minimal validators, JSON, privacy, manifest, ancestry, and clean checks",
            "same_owner_only": True,
            "independent_team_reproduction": False,
            "state": "pending_exact_final_head",
        },
    )
    write_json(
        "orchestration/terminal-route-plan.json",
        {
            "schema": "ghc.family.terminal-route-plan.v1",
            "phase": PHASE,
            "successor": "Sable Rook",
            "successor_phase": "v645-gmut-thos-v5-x1-x2",
            "existing_task_only": True,
            "create_or_fork_task": False,
            "message_count_before_final_validation": 0,
            "message_count_authorized_after_final_validation": 1,
            "standby_siblings_messaged": False,
            "privacy_boundary": "No raw task identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths.",
        },
    )

    # Count the packet after all closeout JSON exists so the precommit receipt is exact.
    json_files = sorted(PHASE_DIR.rglob("*.json"))
    json_errors = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            json_errors.append(path.relative_to(PHASE_DIR).as_posix())
    md_files = sorted(PHASE_DIR.rglob("*.md"))
    word_counts = {
        path.relative_to(PHASE_DIR).as_posix(): len(path.read_text(encoding="utf-8").split())
        for path in md_files
    }
    write_json(
        "validation/final-json-document-receipt.json",
        {
            "schema": "ghc.family.json-document-receipt.v1",
            "phase": PHASE,
            "json_parses_before_this_self_describing_receipt": len(json_files),
            "json_errors": len(json_errors),
            "json_error_files": json_errors,
            "markdown_documents": len(md_files),
            "maximum_words": max(word_counts.values(), default=0),
            "over_6000_words": {key: value for key, value in word_counts.items() if value > 6000},
            "overview_words": word_counts.get("v645-v4-integrated-overview.md", 0),
            "result": "pass" if not json_errors and not any(value > 6000 for value in word_counts.values()) else "fail",
        },
    )
    print(json.dumps({"closeout": "built", "json_before_receipt": len(json_files), "markdown": len(md_files)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
