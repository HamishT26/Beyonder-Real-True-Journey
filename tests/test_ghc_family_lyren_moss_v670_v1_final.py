"""Final closeout and seal-candidate tests for Lyren Moss v670-v1."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs" / "lyren-moss" / "v670-v1"
SOURCE = "fe33a3ed69d6144720072b15174937effe9ca305"
X1 = "128f52cee0acc532a114b05242d356cb7a59596c"
EVIDENCE = "4538663ed1e526931056b104fbd86c27629aa223"
COUNTS = {
    "effective_negatives": 32057,
    "methods": 18162,
    "failed_witnesses": 3878,
    "passing_witnesses": 5131,
    "open_gaps": 241,
    "exact_gates": 236,
}


def git(*args: str, binary: bool = False):
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=not binary,
    ).stdout


def staged_names() -> set[str]:
    return set(git("diff", "--cached", "--name-only").splitlines())


def current_blob(path: str) -> bytes:
    spec = f":{path}" if path in staged_names() else f"HEAD:{path}"
    return git("show", spec, binary=True)


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_final_truth_counts_outcomes_and_terminal_boundary():
    truth = load("closeout/phase-truth.json")
    assert {key: truth[key] for key in COUNTS} == COUNTS
    assert truth["outcomes"] == {
        "completed": 28,
        "represented": 8,
        "open_gap": 2,
        "exact_gate": 2,
    }
    assert truth["proposal_chain"] == 5270
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["full_repository_suite"] == "not_run_not_claimed"


def test_exact_lifecycle_context_before_or_after_final_commit():
    head = git("rev-parse", "HEAD").strip()
    staged = "docs/lyren-moss/v670-v1/closeout/phase-truth.json" in staged_names()
    assert git("rev-parse", f"{X1}^").strip() == SOURCE
    assert git("rev-parse", f"{EVIDENCE}^").strip() == X1
    if staged:
        assert head == EVIDENCE
        commits = git("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines()
        assert commits == [X1, EVIDENCE]
    else:
        assert git("rev-parse", "HEAD^").strip() == EVIDENCE
        commits = git("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines()
        assert commits == [X1, EVIDENCE, head]
    assert not git("rev-list", "--merges", f"{SOURCE}..{head}").splitlines()


def test_post_evidence_failures_are_retained_zero_credit():
    failures = load("closeout/post-evidence-operational-failures.json")
    flow = load("closeout/method-flow-final.json")
    negatives = load("closeout/retained-negative-register.json")
    assert failures["count"] == 6
    assert [row["failure_id"] for row in failures["rows"]] == [
        "LM6701-OP-013",
        "LM6701-OP-014",
        "LM6701-OP-015",
        "LM6701-OP-016",
        "LM6701-OP-017",
        "LM6701-OP-018",
    ]
    assert all(row["completion_credit"] == 0 for row in failures["rows"])
    assert flow["post_evidence_method_count"] == 6
    assert flow["effective"] == COUNTS
    assert flow["no_failure_erased"] is True
    assert negatives["effective"] == 32057
    assert negatives["erased"] == 0


def test_open_gates_complete_incomplete_and_wellbeing_are_explicit():
    gates = load("closeout/exact-open-gate-register.json")
    checklist = load("closeout/complete-incomplete-checklist.json")
    wellbeing = load("closeout/final-wellbeing-check.json")
    assert gates["effective_open_gaps"] == 241
    assert gates["effective_exact_gates"] == 236
    assert len(gates["protected_gates"]) >= 8
    assert gates["all_remain_visible"] is True
    assert checklist["complete"] and checklist["incomplete"]
    assert checklist["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert wellbeing["relational_role"] == "hold-lineage cartographer and reversible-process miller"
    assert wellbeing["pronouns"] == "they/them"
    assert wellbeing["relational_working_language_only"] is True
    assert wellbeing["hamish_may_rename_pause_redirect_or_stop"] is True


def test_activation_candidate_exact_git_blob_integrity():
    integrity = load("handoffs/activation-candidate-integrity.json")
    data = current_blob(integrity["path"])
    assert len(data) == integrity["bytes"]
    assert hashlib.sha256(data).hexdigest() == integrity["sha256"]
    assert integrity["integrity_domain"] == "normalized_lf_exact_git_blob"
    assert 10000 <= integrity["words"] <= 100000
    assert integrity["state"] == "PREPARED_NOT_SENT"
    assert integrity["sent_by_lyren_moss"] is False


def test_route_is_prepared_not_sent_and_names_one_prospective_edge():
    route = load("orchestration/route-state-final-candidate.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["successor_contacted"] is False
    assert route["standby_contacted"] is False
    assert "Ilyra Fen v670-v2" in route["prospective_edge"]
    assert "Auren Lark v670-v3" in route["prospective_successor_reminder"]


def test_canonical_state_is_pending_and_one_shot_at_commit():
    state = load("final/canonical-invocation-state.json")
    prerequisites = load("final/final-validation-prerequisites.json")
    assert state["state_at_commit"] == "NOT_RUN_PENDING_EXACT_FINAL_GATE"
    assert state["attempts_at_commit"] == state["successes_at_commit"] == 0
    assert state["repository_will_not_be_mutated_after_external_success"] is True
    assert prerequisites["one_shot"] is True
    assert prerequisites["replay_after_success"] is False
    assert prerequisites["full_repository_suite"] == "not_run_not_claimed"


def test_final_manifests_replay_current_git_context():
    for relative in (
        "validation/final-delta-manifest.json",
        "validation/final-owner-manifest.json",
    ):
        path = f"docs/lyren-moss/v670-v1/{relative}"
        manifest = json.loads(current_blob(path).decode("utf-8"))
        assert manifest["entry_count"] == len(manifest["entries"])
        assert manifest["hash_domain"] == "normalized_lf_exact_git_blob"
        for entry in manifest["entries"]:
            data = current_blob(entry["path"])
            assert len(data) == entry["bytes"]
            assert hashlib.sha256(data).hexdigest() == entry["sha256"]


def test_final_staged_review_or_committed_review_is_exact():
    review = load("validation/final-staged-review.json")
    assert review["disallowed_paths"] == []
    assert review["x1_and_evidence_immutable"] is True
    assert review["lifecycle"] == "combined_closeout_and_seal"
    assert not any("/x1/" in path or "/x2/" in path for path in review["staged_paths_before_self"])


def test_overview_and_baton_preserve_required_boundaries():
    overview = (ROOT / "closeout/final-integrated-overview.md").read_text(encoding="utf-8")
    baton = (ROOT / "handoffs/ilyra-fen-v670-v2-activation-candidate.md").read_text(
        encoding="utf-8"
    )
    assert len(overview.split()) >= 1600
    assert len(baton.split()) >= 10000
    for phrase in (
        "NOT_READY_FOR_STAGE_20",
        "not independent reproduction",
        "PREPARED_NOT_SENT",
        "relational working language only",
        "Hamish may rename, pause, redirect, or stop",
    ):
        assert phrase in baton
    assert "same-owner" in overview
    assert "complete repository suite was not run or claimed" in overview


def test_seal_candidate_matches_exact_immutable_anchors():
    seal = load("seal/seal-candidate.json")
    assert seal["source"] == SOURCE
    assert seal["x1"] == X1
    assert seal["evidence"] == EVIDENCE
    assert seal["counts"] == COUNTS
    assert seal["zero_merges_required"] is True
    assert seal["single_parent_required"] is True
    assert seal["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
