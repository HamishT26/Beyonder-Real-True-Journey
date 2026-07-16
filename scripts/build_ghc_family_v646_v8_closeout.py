#!/usr/bin/env python3
"""Build the Ilyra Fen v646-v8 closeout, seal, and final-validation protocol."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v646_v8_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v8"
X1 = "37c0e57d82fa8826d891a5b39f1fcb8ce0812a4a"
EVIDENCE = "64323516c35eddaa57c9be371eac327a24214a76"
VALIDATION_BRANCH = "codex/GHC-Family/ilyra-fen-v646-v8-validation"


def read(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def ancestor(older: str, newer: str = "HEAD") -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", older, newer], cwd=ROOT, check=False).returncode == 0


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder must start at the immutable evidence commit")
    status_lines = [
        line
        for line in subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True, encoding="utf-8"
        ).splitlines()
        if line
    ]
    allowed_local = {
        "scripts/build_ghc_family_v646_v8_closeout.py",
        "scripts/ghc_family_v646_v8_owner_manifest.py",
        "scripts/ghc_family_v646_v8_exact_head_audit.py",
        "scripts/ghc_family_v646_v8_staged_review.py",
        "tests/test_ghc_family_v646_v8_closeout.py",
    }
    outside = [line[3:].replace("\\", "/") for line in status_lines if not (line[3:].replace("\\", "/").startswith("docs/ilyra-fen/v646-v8/") or line[3:].replace("\\", "/") in allowed_local)]
    if outside:
        raise RuntimeError(f"unexpected worktree changes before closeout: {outside}")
    validation = read("validation/canonical-evidence-validation.json")
    if validation["result"] != "pass" or validation["head"] != EVIDENCE:
        raise RuntimeError("canonical evidence validation is not bound to the evidence commit")
    portfolio = read("approval-packets/x2-portfolio-execution.json")
    cleanup = read("maintenance/x2-clean-refine-ledger.json")
    truth = read("phase-truth.json")
    negatives = read("retained-negative-register.json")
    method = read("method-flow/method-flow-state.json")
    local = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{upstream}")
    branch = git("branch", "--show-current")
    tracking = git("rev-parse", f"refs/remotes/origin/{branch}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    live = live_line.split()[0] if live_line else ""
    validation_branch_exists = bool(git("branch", "--list", VALIDATION_BRANCH))
    validation_upstream = subprocess.run(["git", "rev-parse", "--abbrev-ref", f"{VALIDATION_BRANCH}@{{upstream}}"], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
    validation_live = git("ls-remote", "--heads", "origin", f"refs/heads/{VALIDATION_BRANCH}")
    if not (local == upstream == tracking == live == EVIDENCE):
        raise RuntimeError("evidence commit is not four-way remote equal")
    if not validation_branch_exists or validation_upstream.returncode == 0 or validation_live:
        raise RuntimeError("named validation branch is not local-only")
    if cleanup["completed_count"] != 30 or cleanup["pending_lifecycle_count"] != 0:
        raise RuntimeError("all thirty safe cleanup tasks must be lifecycle-complete")

    write("validation/evidence-remote-equality.json", {
        "schema": "ghc.family.v646-v8.evidence-remote-equality.v1",
        "revision": EVIDENCE,
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live_remote": live,
        "divergence": [0, 0],
        "equal": True,
        "canonical_clean_before_closeout": True,
    })
    write("validation/named-lane-preflight.json", {
        "schema": "ghc.family.v646-v8.named-lane-preflight.v1",
        "branch_namespace": "codex/GHC-Family/ilyra-fen-v646-v8-validation",
        "named_not_detached": True,
        "local_only": True,
        "upstream_configured": False,
        "live_remote_ref": False,
        "initial_revision": EVIDENCE,
        "tests_or_replay_run": False,
        "final_replay_reserved": True,
        "independent_reproduction": False,
    })
    write("environment/final-rotation-receipt.json", {
        "schema": "ghc.family.v646-v8.final-rotation.v1",
        "owner_generated_file_threshold": 15000,
        "threshold_scope": "Ilyra-generated additions only",
        "threshold_reached": False,
        "measured_lane_failure_requiring_rotation": False,
        "canonical_lane_retained": True,
        "validation_lane_role": "additive local-only named replay lane",
    })
    write("closeout-receipt.json", {
        "schema": "ghc.family.v646-v8.closeout-receipt.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "source_revision": d.SOURCE_REVISION,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "strict_x1_before_x2": True,
        "phase_commit_count_before_final": 2,
        "phase_commit_cap": 4,
        "x2_commit_count_before_final": 1,
        "x2_commit_cap": 2,
        "core_distribution": truth["core_distribution"],
        "effective_negatives": negatives["effective_total"],
        "effective_open_gaps": truth["effective_open_gaps"],
        "effective_exact_gates": truth["effective_exact_gates"],
        "safe_completed": portfolio["safe_completed"],
        "candidate_completed": portfolio["candidate_completed"],
        "clean_refine_completed": cleanup["completed_count"],
        "skills_built_validated_and_used": 20,
        "runners_built_and_used": 10,
        "exact_packets_executed": 0,
        "blocked_packets_executed": 0,
        "method_failed_witnesses": method["counts"]["witness_results"]["fail"],
        "method_passing_witnesses": method["counts"]["witness_results"]["pass"],
        "canonical_evidence_validation": "pass",
        "exact_final_head_validation": "required_after_commit",
        "named_local_only_replay": "required_after_commit",
        "same_owner_repeatability_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": d.TRUTH_BOUNDARY,
    })
    write("seal-receipt.json", {
        "schema": "ghc.family.v646-v8.seal-receipt.v1",
        "phase": d.PHASE,
        "state": "SEALED_CONTENT_CANDIDATE",
        "source_revision": d.SOURCE_REVISION,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_commit_role": "single-parent commit containing this receipt",
        "source_x1_evidence_ancestry": ancestor(d.SOURCE_REVISION) and ancestor(X1) and ancestor(EVIDENCE),
        "zero_merge_requirement": True,
        "owner_manifest_hash_domain": "Git index blob then exact final Git blob",
        "exact_final_validation_required_after_commit": True,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write("final-validation-record.json", {
        "schema": "ghc.family.v646-v8.final-validation-record.v1",
        "phase": d.PHASE,
        "validated_evidence_commit": EVIDENCE,
        "canonical_evidence_checks": validation["check_count"],
        "canonical_evidence_json_parses": validation["json"]["parsed"],
        "canonical_evidence_privacy_files": validation["privacy"]["files_scanned"],
        "canonical_evidence_confirmed_privacy_hits": validation["privacy"]["confirmed_hit_count"],
        "canonical_evidence_scoped_tests": validation["scoped_tests"]["tests_run"],
        "final_target_role": "single-parent commit containing this record",
        "exact_final_canonical_validation": "required_after_commit",
        "named_local_only_replay": "required_after_commit",
        "named_replay_count_required": 1,
        "full_repository_suite_run_by_ilyra": False,
        "full_repository_suite_owner": "Eiren Kestrel",
        "route_may_send_only_after_all_required_post_commit_checks": True,
        "same_owner_repeatability_only": True,
        "independent_reproduction": False,
    })
    write("final-receipt.json", {
        "schema": "ghc.family.v646-v8.final-receipt.v1",
        "state": "FINAL_CANDIDATE_AWAITING_EXACT_POST_COMMIT_VALIDATION",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "source_revision": d.SOURCE_REVISION,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_commit_role": "single-parent commit containing this record",
        "route_state": "HELD",
        "task_created": False,
        "message_sent": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": d.TRUTH_BOUNDARY,
    })
    write("final-complete-incomplete-checklist.json", {
        "schema": "ghc.family.v646-v8.final-checklist.v1",
        "completed_before_final_commit": ["source and x1 ancestry", "strict x1-before-x2", "ten core outcomes", "30 safe-now tasks", "20 bounded candidates", "20 phase-local skills", "10 family-current runners", "30 additive cleanup tasks", "70 synthetic mutation rejections", "canonical evidence validation", "evidence remote equality", "named local-only lane preflight", "accessible static report", "three-page-equivalent overview"],
        "required_after_final_commit": ["exact final canonical scoped validation", "exact final owner-manifest parity", "exact final ancestry and zero merges", "clean canonical state", "final four-way remote equality", "exactly one clean named local-only replay", "one acknowledged Sable Rook baton"],
        "externally_incomplete": ["real empirical study", "blind matched-budget THOS arms", "production Freed ID", "affected-party legal cultural and Māori authority", "manual affected-user accessibility evaluation", "independent-team reproduction", "deployment", "AGI or ASI", "consciousness or personhood evidence", "Theory-of-Everything proof", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write("orchestration/final-route-gate.json", {
        "schema": "ghc.family.v646-v8.final-route-gate.v1",
        "state": "HELD_UNTIL_POST_COMMIT_VALIDATION",
        "target_title": "Sable Rook",
        "successor_phase": "v647-gmut-thos-v1-x1-x2",
        "send_count": 0,
        "create_count": 0,
        "required": ["exact final canonical pass", "final remote equality", "one named local-only replay", "sanitized baton", "acknowledged send"],
    })
    write("reproduction/same-owner-replay-plan.json", {
        "schema": "ghc.family.v646-v8.same-owner-replay-plan.v1",
        "named_lane_preflight_passed": True,
        "detached": False,
        "pushed": False,
        "upstream": False,
        "live_remote_ref": False,
        "replay_count_before_final": 0,
        "required_replay_count_at_exact_final": 1,
        "full_suite_prohibited_for_ilyra": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    })
    overview = (PHASE / "v646-v8-integrated-overview.md").read_text(encoding="utf-8")
    write_text("deliverables/v646-v8-final-integrated-overview.md", overview + "\n## Lifecycle closeout\n\nThe immutable evidence commit passed the scoped canonical validation and was clean, pushed, and four-way remote-equal before this final lifecycle packet was built. The named validation lane was created additively, is not detached, has no upstream, has no live remote ref, and has run no replay yet. The final commit must remain a single-parent successor, pass the same bounded canonical gates, preserve exact manifest parity, become four-way remote-equal, and then receive exactly one clean named-lane replay. Only an acknowledged single baton after those checks changes the route state.\n")


def main() -> int:
    build()
    print(json.dumps({"phase": d.PHASE, "evidence": EVIDENCE, "cleanup": 30, "route": "HELD_UNTIL_POST_COMMIT_VALIDATION", "verdict": "NOT_READY_FOR_STAGE_20", "result": "pass"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
