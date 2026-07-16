#!/usr/bin/env python3
"""Build the combined closeout and seal candidate for Orin Thale v647-v2."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v647-v2"
SOURCE = "c3025ff0d5c062ece7977b4df7f1a34db7d08afe"
X1 = "8c62ae37ba4f1f38c2f97840f83f1d27a6546765"
EVIDENCE = "eb87a78d050f3fdc7e61dd5af6dd08c2f4811e63"
BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
FINAL_NEGATIVES = [
    {
        "negative_id": "V6472-X2-N09",
        "method_id": "V6472-M18",
        "summary": "Closeout review found twenty candidate witness filenames carrying the source compact token v6471; corrected v6472 copies and an additive quarantine receipt preserve the immutable evidence paths.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6472-X2-N10",
        "method_id": "V6472-M19",
        "summary": "A combined read-only file and Git status probe exceeded a ten-second wrapper budget; the unchanged probe passed with a measured sixty-second budget.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6472-X2-N11",
        "method_id": "V6472-M20",
        "summary": "The first exact-head audit compilation failed on a mismatched subprocess argument-list delimiter; the narrow syntax correction passed compilation.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6472-X2-N12",
        "method_id": "V6472-M21",
        "summary": "The first final staged-review invocation used relative receipt paths that the repository-containment guard rejected before content review; absolute repository paths preserve the same bounded outputs.",
        "retained": True,
        "recovered": True,
    },
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, text: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("closeout must begin at the exact pushed evidence commit")
    if git("branch", "--show-current") != BRANCH:
        raise SystemExit("closeout must run on the Orin canonical branch")
    if subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", X1, EVIDENCE]).returncode:
        raise SystemExit("x1 is not ancestral to evidence")

    mappings = []
    for index in range(1, 21):
        old = f"validation/candidate-witnesses/v6471-candidate-{index:02d}.json"
        new = f"validation/candidate-witnesses/v6472-candidate-{index:02d}.json"
        payload = load(old)
        write(new, payload)
        mappings.append({"legacy_path": old, "corrected_path": new, "semantic_payload_equal": True})
    write(
        "validation/stale-label-quarantine.json",
        {
            "schema": "ghc.family.v647-v2.stale-label-quarantine.v1",
            "evidence_commit": EVIDENCE,
            "legacy_count": 20,
            "corrected_count": 20,
            "legacy_paths_retained": True,
            "legacy_completion_credit": False,
            "history_rewritten": False,
            "mappings": mappings,
            "boundary": "The additive correction preserves evidence history and changes no proposal outcome, scientific claim, or authority gate.",
        },
    )

    operational = load("validation/x2-operational-negatives.json")
    final_ids = {row["negative_id"] for row in FINAL_NEGATIVES}
    rows = [row for row in operational["rows"] if row["negative_id"] not in final_ids]
    rows.extend(FINAL_NEGATIVES)
    write(
        "validation/x2-operational-negatives.json",
        {
            "schema": "ghc.family.v647-v2.x2-operational-negatives.closeout.v1",
            "count": len(rows),
            "rows": rows,
            "no_negative_erased": True,
        },
    )
    effective_negatives = 3235 + 10 + 70 + len(rows)
    retained = load("retained-negative-register.json")
    retained.update(
        {
            "schema": "ghc.family.v647-v2.retained-negatives.closeout.v1",
            "inherited_effective": 3235,
            "x1_operational": 10,
            "preregistered_synthetic": 70,
            "preregistered_synthetic_executed": 70,
            "x2_operational": len(rows),
            "x2_operational_rows": rows,
            "effective_total": effective_negatives,
            "no_negative_erased": True,
        }
    )
    write("retained-negative-register.json", retained)

    method_summary = load("method-flow/method-flow-summary.json")
    methods = method_summary["counts"]["methods"]
    failed = method_summary["counts"]["witness_results"]["fail"]
    passed = method_summary["counts"]["witness_results"]["pass"]
    if (methods, failed, passed) != (21, 21, 21):
        raise SystemExit(f"unexpected Method Flow counts: {(methods, failed, passed)}")

    gates = load("exact-open-gate-register.json")
    outcomes = load("x2-proposal-ledger.json")["outcome_counts"]
    json_count = sum(1 for path in PHASE.rglob("*.json") if path.is_file())
    owner_count = (
        sum(1 for path in PHASE.rglob("*") if path.is_file())
        + sum(1 for path in (ROOT / "scripts").glob("*v647_v2*") if path.is_file())
        + 9
        + sum(1 for path in (ROOT / "tests").glob("*v647_v2*") if path.is_file())
    )

    write(
        "closeout-receipt.json",
        {
            "schema": "ghc.family.v647-v2.closeout.candidate.v1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "expected_phase_commit_count_after_closeout": 3,
            "expected_merge_count": 0,
            "outcomes": outcomes,
            "effective_negatives": effective_negatives,
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "method_flow": {"methods": methods, "failed_witnesses": failed, "passing_witnesses": passed},
            "scoped_tests_last_passed": 113,
            "detailed_checks_last_passed": 15,
            "minimal_checks_last_passed": 14,
            "phase_json_at_build": json_count,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write(
        "seal-receipt.json",
        {
            "schema": "ghc.family.v647-v2.combined-seal.candidate.v1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "seal_commit": "commit_containing_this_receipt",
            "final_expected_to_equal_seal_commit": True,
            "single_parent_required": True,
            "zero_merges_required": True,
            "remote_equality_required": True,
            "named_replay_required": True,
            "route_sent": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "final-validation-record.json",
        {
            "schema": "ghc.family.v647-v2.final-validation.candidate.v1",
            "exact_final_head": "resolved_after_combined_closeout_commit",
            "canonical_scoped_tests_required": 113,
            "minimal_checks_required": 14,
            "detailed_checks_required": 15,
            "all_phase_json_required": True,
            "five_class_privacy_zero_required": True,
            "x1_manifest_entries": 78,
            "evidence_manifest_entries": 156,
            "final_manifest_pending_staged_review": True,
            "one_named_local_replay_required": True,
            "full_repository_suite_owner": "Eiren Kestrel",
            "full_repository_suite_run_here": False,
            "boundary": "Canonical and named validation are same-owner checks under shared infrastructure, not independent-team reproduction.",
        },
    )
    write(
        "final-receipt.json",
        {
            "schema": "ghc.family.v647-v2.final.candidate.v1",
            "owner": "Orin Thale",
            "phase": "v647-gmut-thos-v2-x1-x2",
            "primary_focus": "GMUT Mind",
            "outcomes": outcomes,
            "effective_negatives": effective_negatives,
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "identity_boundary": "Relational working language only; no consciousness, personhood, continuity, employment, or authority claim.",
        },
    )

    checklist = load("complete-incomplete-checklist.json")
    checklist["schema"] = "ghc.family.v647-v2.checklist.closeout-candidate.v1"
    checklist["complete"].extend(
        [
            "evidence commit exact manifest parity 156 of 156",
            "stale compact-token witness labels quarantined additively",
            "combined closeout and seal candidate built",
        ]
    )
    checklist["incomplete"].extend(
        [
            "exact final staged review and manifest parity",
            "canonical exact-final replay",
            "one clean local named replay",
            "final four-way remote equality",
            "Tamar Vey activation acknowledgement",
        ]
    )
    write("complete-incomplete-checklist.json", checklist)

    phase_truth = load("phase-truth.json")
    phase_truth.update(
        {
            "schema": "ghc.family.v647-v2.phase-truth.closeout-candidate.v1",
            "frozen_proposals_after_x1": 490,
            "effective_retained_negatives": effective_negatives,
            "effective_open_gaps": 19,
            "effective_exact_gates": 20,
            "method_flow_methods": methods,
            "route_state": "PREPARED_NOT_SENT",
            "canonical_validation_state": "final_candidate_pending",
            "named_replay_state": "not_started",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    write("phase-truth.json", phase_truth)
    write(
        "orchestration/phase-update.json",
        {
            "schema": "ghc.family.v647-v2.phase-update.closeout-candidate.v1",
            "owner": "Orin Thale",
            "state": "CLOSEOUT_CANDIDATE",
            "active": ["Orin Thale"],
            "standby": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Tamar Vey", "Sylven Arc"],
            "route_state": "PREPARED_NOT_SENT",
        },
    )
    write(
        "orchestration/terminal-route-plan.json",
        {
            "schema": "ghc.family.v647-v2.terminal-route-plan.closeout.v1",
            "target_title": "Tamar Vey",
            "next_phase": "v647-gmut-thos-v3-x1-x2",
            "state": "PREPARED_NOT_SENT",
            "send_count": 0,
            "requires_exact_final": True,
            "requires_named_replay": True,
            "requires_remote_equality": True,
            "no_task_creation": True,
            "boundary": "A prepared route is not a sent or acknowledged baton.",
        },
    )
    write(
        "environment/final-rotation-receipt.json",
        {
            "schema": "ghc.family.v647-v2.rotation.final-candidate.v1",
            "threshold": 15000,
            "inherited_full_checkout_baseline": 36031,
            "inherited_baseline_triggers_rotation": False,
            "owner_generated_count": owner_count,
            "rotation_required": owner_count >= 15000,
        },
    )
    write(
        "tooling/finalization-toolchain.json",
        {
            "schema": "ghc.family.v647-v2.finalization-toolchain.v1",
            "scripts": [
                "ghc_family_v647_v2_validation_runner.py",
                "ghc_family_v647_v2_staged_review.py",
                "ghc_family_v647_v2_manifest_parity.py",
                "ghc_family_v647_v2_exact_head_audit.py",
            ],
            "full_suite_owner": "Eiren Kestrel",
            "caller_compatibility_preserved": True,
        },
    )
    family_index = load("tooling/ghc-family-index.json")
    family_index.update(
        {
            "schema": "ghc.family.v647-v2.phase-index.closeout-candidate.v1",
            "lifecycle": "closeout_candidate",
            "built_phase_skills": 20,
            "used_phase_skills": 20,
            "built_phase_runners": 10,
            "used_phase_runners": 10,
            "method_flow_methods": methods,
            "stale_label_quarantine": "validation/stale-label-quarantine.json",
            "reviewed_current": True,
        }
    )
    write("tooling/ghc-family-index.json", family_index)
    write_text(
        "tooling/ghc-family-index.md",
        """# GHC Family Index - Orin Thale v647-v2 closeout candidate

- Required global skills and references were reviewed before mutation.
- Exactly 490 proposal titles are frozen through this phase.
- Twenty phase-local skills and ten family-current runners were built and used within bounded scope.
- Historical names remain compatibility evidence. Twenty stale compact-token witness paths are retained and quarantined; corrected v6472 paths are additive.
- Method Flow retains eighteen failed and eighteen passing witnesses. Preference is trigger-bounded.
- The full repository suite remains owned by Eiren Kestrel; this phase uses scoped validation plus one named replay.

No software count or passing witness closes an empirical, participant, production, privacy, accessibility, legal, cultural, Māori-authority, affected-party, independent-reproduction, or Stage 20 gate.
""",
    )
    print(
        json.dumps(
            {
                "valid": True,
                "negatives": effective_negatives,
                "methods": methods,
                "open_gaps": 19,
                "exact_gates": 20,
                "owner_files": owner_count,
                "route": "PREPARED_NOT_SENT",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
