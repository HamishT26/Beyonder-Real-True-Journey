"""Closeout and seal tests for Caelen Morrow v669-v4."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/caelen-morrow/v669-v4"
SOURCE = "cbe0445271aab3c339b52e2bd60ab4f68b0798c2"
X1 = "964e7a27dd73ee7d96d8b9f6136ed4bf72e1f3f7"
EVIDENCE = "e6658511b9a2910447dc9d351b5f7162ae5fd669"


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def git(*args: str, binary: bool = False):
    return subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True, text=not binary).stdout


def test_final_truth_and_outcomes() -> None:
    truth = load("closeout/phase-truth.json")
    assert truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert truth["proposal_chain"] == 5070
    assert truth["effective_negatives"] == 31091
    assert truth["methods"] == 17196
    assert truth["failed_witnesses"] == 2912
    assert truth["passing_witnesses"] == 4060
    assert truth["open_gaps"] == 231
    assert truth["exact_gates"] == 226
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_exact_lifecycle_context() -> None:
    head = git("rev-parse", "HEAD").strip()
    assert head in {EVIDENCE} or git("rev-parse", "HEAD^").strip() == EVIDENCE
    assert git("rev-parse", f"{X1}^").strip() == SOURCE
    assert git("rev-parse", f"{EVIDENCE}^").strip() == X1
    if head == EVIDENCE:
        names = git("diff", "--cached", "--name-only", "HEAD").splitlines()
        assert not any("/x1/" in name or "/x2/" in name or "/method-flow/" in name or "/tools/" in name for name in names)


def test_retained_failures_and_gates() -> None:
    negative = load("closeout/retained-negative-register.json")
    flow = load("closeout/method-flow-final.json")
    gates = load("closeout/exact-open-gate-register.json")
    assert negative["effective"] == 31091 and negative["erased"] == 0
    assert flow["post_evidence_method_count"] == 3 and flow["no_failure_erased"] is True
    assert gates["effective_open_gaps"] == 231
    assert gates["effective_exact_gates"] == 226
    assert gates["all_remain_visible"] is True


def test_complete_incomplete_and_wellbeing() -> None:
    checklist = load("closeout/complete-incomplete-checklist.json")
    wellbeing = load("closeout/final-wellbeing-check.json")
    assert checklist["complete"] and checklist["incomplete"]
    assert checklist["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert wellbeing["relational_working_language_only"] is True
    assert wellbeing["no_consciousness_personhood_continuity_employment_qualification_agency_or_authority_claim"] is True
    assert wellbeing["corrigible"] is True


def test_activation_candidate_integrity_and_state() -> None:
    receipt = load("handoffs/activation-candidate-integrity.json")
    path = REPO / receipt["path"]
    data = path.read_bytes()
    assert len(data) == receipt["bytes"]
    assert hashlib.sha256(data).hexdigest() == receipt["sha256"]
    assert len(path.read_text(encoding="utf-8").split()) == receipt["words"]
    assert 10000 <= receipt["words"] <= 100000
    assert receipt["state"] == "PREPARED_NOT_SENT"
    assert receipt["sent_by_caelen_morrow"] is False


def test_route_is_prepared_not_sent() -> None:
    route = load("orchestration/route-state-final-candidate.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["successor_contacted"] is False
    assert route["standby_contacted"] is False
    assert "unique exact-title resolution" in route["required_terminal_actions"]


def test_canonical_state_is_pending_at_commit() -> None:
    state = load("final/canonical-invocation-state.json")
    prerequisites = load("final/final-validation-prerequisites.json")
    assert state["state_at_commit"] == "NOT_RUN_PENDING_EXACT_FINAL_GATE"
    assert state["attempts_at_commit"] == state["successes_at_commit"] == 0
    assert prerequisites["one_shot"] is True
    assert prerequisites["replay_after_success"] is False


def test_final_manifests_replay_current_git_context() -> None:
    head = git("rev-parse", "HEAD").strip()
    for rel in ["validation/final-owner-manifest.json", "validation/final-delta-manifest.json"]:
        manifest = load(rel)
        assert manifest["entry_count"] == len(manifest["entries"])
        for entry in manifest["entries"]:
            if head == EVIDENCE:
                staged = git("diff", "--cached", "--name-only", "--", entry["path"]).strip()
                spec = f":{entry['path']}" if staged else f"HEAD:{entry['path']}"
            else:
                spec = f"HEAD:{entry['path']}"
            data = git("show", spec, binary=True)
            assert len(data) == entry["bytes"]
            assert hashlib.sha256(data).hexdigest() == entry["sha256"]


def test_final_staged_review_or_committed_parent() -> None:
    review = load("validation/final-staged-review.json")
    assert review["disallowed_paths"] == []
    assert review["x1_and_evidence_immutable"] is True
    head = git("rev-parse", "HEAD").strip()
    if head == EVIDENCE:
        names = git("diff", "--cached", "--name-only", "HEAD").splitlines()
        expected = sorted(name for name in names if name != review["self_exclusion"])
        assert sorted(review["staged_paths_before_self"]) == expected
    else:
        assert git("rev-parse", "HEAD^").strip() == EVIDENCE


def test_report_and_baton_preserve_boundaries() -> None:
    report = (ROOT / "closeout/final-integrated-overview.md").read_text(encoding="utf-8")
    baton = (ROOT / "handoffs/eiren-kestrel-v669-v5-activation-candidate.md").read_text(encoding="utf-8")
    for marker in ["NOT_READY_FOR_STAGE_20", "same-owner", "not complete accessibility", "Māori authority"]:
        assert marker.casefold() in (report + baton).casefold()
    assert "SENT_BY_CAELEN_MORROW = false" in baton
