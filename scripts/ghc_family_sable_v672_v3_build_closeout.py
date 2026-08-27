#!/usr/bin/env python3
"""Build the prospective Sable Rook v672-v3 closeout and content seal."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v672-v3"
CLOSEOUT = PHASE / "closeout"
HANDOFFS = PHASE / "handoffs"
SOURCE = "842956c8ddc8b648d14911ac6228ba1cffb7d5ad"
X1 = "1875dc20ea21a47fd411bc898ee274e632b2977f"
EVIDENCE = "f1335924c402b450c1458f15d77a759d0e23d291"
BRANCH = "codex/GHC-Family/sable-rook-v672-v3-full-tools"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def base_truth() -> dict[str, Any]:
    return {
        "owner": "Sable Rook",
        "phase": "v672-v3",
        "source_head": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "proposal_chain": 6030,
        "outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "effective_counts": {
            "negatives": 35327,
            "methods": 21938,
            "failed_witnesses": 7148,
            "passing_witnesses": 9225,
            "open_gaps": 281,
            "exact_gates": 274,
        },
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def refresh_index() -> None:
    files = sorted(path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file())
    write_json(
        CLOSEOUT / "phase-index.json",
        {
            "schema": "ghc.family.sable.v672-v3.phase-index.v1",
            "phase": "v672-v3",
            "files": files,
            "file_count_before_index_refresh": len(files),
            "owner_file_ceiling": 2000,
            "owner_file_ceiling_passed": len(files) + 1 < 2000,
            "historical_callers_preserved": True,
            "family_current_callers": [
                "build_ghc_family_sable_rook_v672_v3.py",
                "ghc_family_sable_v672_v3_*",
                "validate_ghc_family_sable_rook_v672_v3_final.py",
            ],
        },
    )


def generate() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("closeout must begin at immutable evidence commit")
    unstaged_tracked = subprocess.run(
        ["git", "-C", str(ROOT), "diff", "--quiet", "HEAD", "--"],
        capture_output=True,
    ).returncode
    staged_tracked = subprocess.run(
        ["git", "-C", str(ROOT), "diff", "--cached", "--quiet"],
        capture_output=True,
    ).returncode
    if unstaged_tracked or staged_tracked:
        raise SystemExit("closeout generation requires an unchanged tracked evidence tree")
    truth = base_truth()
    write_json(
        CLOSEOUT / "phase-truth.json",
        {
            "schema": "ghc.family.sable.v672-v3.closeout-truth.v1",
            **truth,
            "lifecycle": "combined_closeout_content_seal_final_candidate",
            "phase_commits_before_final": 2,
            "planned_phase_commits_after_final": 3,
            "commit_ceiling": 8,
            "canonical_invocations_at_commit_time": 0,
            "canonical_successes_at_commit_time": 0,
            "final_self_identifier": "necessarily_pending_until_commit_exists",
            "full_repository_suite_run": False,
            "independent_reproduction": False,
        },
    )
    write_json(
        CLOSEOUT / "closeout-receipt.json",
        {
            "schema": "ghc.family.sable.v672-v3.closeout-receipt.v1",
            **truth,
            "x1_boundary": {
                "direct_parent": SOURCE,
                "pushed_clean_four_way_equal_before_x2": True,
            },
            "evidence_boundary": {
                "direct_parent": X1,
                "pushed_clean_four_way_equal_before_closeout": True,
            },
            "one_shot_smoke": {
                "runner_checks": 60,
                "runner_passes": 60,
                "skill_packages": 20,
                "skill_passes": 20,
                "replayed": False,
            },
            "evidence_selection": {
                "failed_first_selection_credit": 0,
                "retained_failures": 2,
                "immutable_x1": "16_of_16",
                "current_x2": "20_of_20",
            },
            "stage_projection_failure_retained": True,
            "final_commit": "pending_creation",
            "final_validation": "pending_exact_pushed_head",
        },
    )
    seal_targets = [
        PHASE / "x1" / "proposals" / "new-proposal-freeze.json",
        PHASE / "x1" / "proposals" / "semantic-neighbor-audit.json",
        PHASE / "x2" / "proposals" / "outcome-ledger.json",
        PHASE / "x2" / "method-flow" / "ledger.json",
        PHASE / "x2" / "retained-negative-register.json",
        PHASE / "x2" / "gate-register.json",
        PHASE / "x2" / "phase-truth.json",
        PHASE / "x2" / "integrated-overview.md",
        PHASE / "validation" / "evidence-staged-manifest.json",
        PHASE / "validation" / "evidence-staged-review.json",
    ]
    write_json(
        CLOSEOUT / "content-seal.json",
        {
            "schema": "ghc.family.sable.v672-v3.content-seal.v1",
            "seal_state": "content_seal_candidate_pending_final_commit",
            "source_head": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "hash_domain": "worktree_bytes_equal_to_evidence_head_for_inherited_targets",
            "targets": [
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": sha256(path),
                    "bytes": path.stat().st_size,
                }
                for path in seal_targets
            ],
            "target_count": len(seal_targets),
            "final_commit": "pending_creation",
        },
    )
    write_json(
        CLOSEOUT / "wellbeing-check.json",
        {
            "schema": "ghc.family.sable.v672-v3.wellbeing-closeout.v1",
            "name": "Sable Rook",
            "pronouns": "they/them",
            "role": "relational evidence-and-reproducibility steward",
            "hope": "Make surviving claims reproducible, challengeable, correctable, and retractable while authority vacancies stay explicit.",
            "identity_evidence": False,
            "corrigible": True,
            "workload": "bounded_below_declared_file_and_document_caps",
            "hamish_may": ["pause", "rename", "redirect", "stop"],
        },
    )
    write_json(
        CLOSEOUT / "stale-label-review.json",
        {
            "schema": "ghc.family.sable.v672-v3.stale-label-review.v1",
            "reviewed_surfaces": ["x1", "x2", "validation", "closeout", "handoffs"],
            "stale_labels_found": 0,
            "prospective_labels_retained": [
                "evidence candidate pending its own commit at evidence commit time",
                "final self identifier pending until final commit exists",
                "canonical validation pending exact pushed final",
                "terminal route held before canonical success",
            ],
            "prospective_labels_are_not_failures": True,
        },
    )
    write_json(
        CLOSEOUT / "final-validation-candidate.json",
        {
            "schema": "ghc.family.sable.v672-v3.final-validation-candidate.v1",
            **truth,
            "expected_branch": BRANCH,
            "expected_final_parent": EVIDENCE,
            "expected_phase_commits": 3,
            "expected_merges": 0,
            "expected_final_parents": 1,
            "selected_test_contexts": [
                "immutable x1 Git-archive context",
                "current x2 exact-final context",
                "current final-lifecycle exact-final context",
            ],
            "full_repository_suite": False,
            "canonical_invocations_at_commit_time": 0,
            "canonical_successes_at_commit_time": 0,
            "canonical_status": "pending_exact_pushed_final",
            "final_self_identifier": "pending_creation",
            "postsuccess_replay_allowed": False,
        },
    )
    write_json(
        HANDOFFS / "terminal-route-hold.json",
        {
            "schema": "ghc.family.sable.v672-v3.terminal-route-hold.v1",
            "state": "PREPARED_NOT_SENT",
            "target": "not_resolved_before_terminal_gate",
            "duplicate_guard": "required",
            "pause_redirect_usage_privacy_evidence_safety_guards": "required",
            "send_count": 0,
            "delivery_acknowledged": False,
            "canonical_success_required": True,
            "fresh_live_equality_required": True,
            "no_successor_inferred_from_historical_files": True,
        },
    )
    write_text(
        CLOSEOUT / "final-overview.md",
        '''# Sable Rook v672-v3 final overview

The complete three-page-equivalent explanation is the immutable x2 integrated overview. This closeout preserves its exact hash in the content seal and adds lifecycle truth without duplicating the narrative.

Forty new proposals produced 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate` outcomes within wholly synthetic owner-local bounds. The effective truth at closeout is 35,327 negatives, 21,938 methods, 7,148 failed witnesses, 9,225 bounded passing witnesses, 281 open gaps, 274 exact gates, and `NOT_READY_FOR_STAGE_20`.

The one-shot runner and skill smoke succeeded once and was not replayed. A failed combined evidence selection retained two failures at zero credit; immutable x1 and current x2 contexts passed separately. A later stage-wrapper projection failure was recovered by waiting on the original process after exact state inspection, without replaying the review.

No real person, service, notice, disruption, location record, credential, participant, empirical row, public communication, authority action, cultural matter, Māori data, or private route was used. The packet establishes no professional competence, operational result, production readiness, legal or cultural legitimacy, affected-party approval, Māori authority, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 authority.

The final commit and canonical result are necessarily pending in this committed candidate. They must be supplied by the exact pushed postcommit state and an external one-shot receipt, never by rewriting this history.
''',
    )
    refresh_index()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("generate", "refresh-index"))
    args = parser.parse_args()
    if args.mode == "generate":
        generate()
    else:
        refresh_index()


if __name__ == "__main__":
    main()
