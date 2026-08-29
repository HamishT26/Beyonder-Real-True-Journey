from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "elaren-kestrel" / "v675-v3"
X1 = PHASE / "x1"
VALIDATION = PHASE / "validation"
SOURCE = "c1e3bd95e950c36d2fc137b5c9693d2c4b632cdc"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def test_activation_and_identity_boundaries() -> None:
    activation = load("x1/activation-intake.json")
    identity = load("x1/identity-and-boundary.json")
    assert activation["source_final"] == SOURCE
    assert activation["activation_state"] == "ACKNOWLEDGED_LIVE_ACTIVATION"
    assert identity["authority_conferred"] is False
    assert "not evidence of consciousness" in identity["identity_boundary"]


def test_source_verification_records_exact_anchors() -> None:
    source = load("x1/source-verification.json")
    assert source["source_final"] == SOURCE
    assert source["source_to_final_commits"] == 3
    assert source["zero_merges"] is True
    assert source["single_parent_commits"] is True
    assert source["source_manifest_issues"] == 0
    assert source["source_canonical_replayed"] is False


def test_forty_proposals_have_complete_planning_contracts() -> None:
    freeze = load("x1/new-proposal-freeze.json")
    rows = freeze["rows"]
    assert len(rows) == 40
    required = {
        "proposal_id",
        "title",
        "hypothesis",
        "null_or_failure_condition",
        "approval_class",
        "execution_lane",
        "official_or_primary_source_needs",
        "concrete_artifacts",
        "falsifier_or_acceptance_gate",
        "rollback_or_recovery",
        "protected_gates",
        "expected_disposition",
    }
    assert all(required <= set(row) for row in rows)
    assert all("observed_outcome" not in row for row in rows)
    assert len({row["proposal_id"] for row in rows}) == 40
    assert len({row["title"] for row in rows}) == 40


def test_planned_outcome_distribution_and_labels() -> None:
    rows = load("x1/new-proposal-freeze.json")["rows"]
    counts = {label: sum(row["expected_disposition"] == label for row in rows) for label in LABELS}
    assert counts == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert {row["expected_disposition"] for row in rows} == LABELS


def test_semantic_audit_is_source_bounded_and_collision_free() -> None:
    audit = load("x1/semantic-neighbor-audit.json")
    assert audit["declared_source_chain"] == 7110
    assert audit["new_titles"] == 40
    assert audit["collisions"] == 0
    assert audit["max_jaccard"] < audit["collision_threshold"]
    assert audit["canonical_row_mapping_open_gap"] is True
    assert audit["universal_novelty_claim"] is False
    assert audit["exact_source_tree_corpus"]["unique_titles"] > 0


def test_inherited_selection_has_zero_elaren_credit() -> None:
    inherited = load("x1/inherited-proposal-revalidation.json")
    assert inherited["row_count"] == 20
    assert inherited["novelty_credit"] == 0
    assert inherited["completion_credit"] == 0
    assert inherited["executed_in_x1"] is False
    assert all(row["elaren_novelty_credit"] == 0 for row in inherited["rows"])


def test_portfolio_counts_are_ceiling_bounded_and_unexecuted() -> None:
    portfolio = load("x1/portfolio-freeze.json")
    assert portfolio["counts"] == {
        "blocked": 10,
        "candidates": 30,
        "clean_fix_refine": 60,
        "exact_approval": 20,
        "inherited_reviews": 20,
        "runners": 10,
        "safe_now": 60,
        "skills": 20,
        "successor_clean_fix_refine": 30,
        "successor_runners": 10,
        "successor_skills": 10,
        "tools": 3,
    }
    for group in portfolio["rows"].values():
        assert all(row["execution_count"] == 0 for row in group)
        assert all(row["completion_credit"] == 0 for row in group)


def test_startup_failures_and_recoveries_are_retained() -> None:
    flow = load("x1/method-flow-startup.json")
    assert flow["counts"] == {
        "failed_witnesses": 5,
        "methods": 5,
        "passing_witnesses": 5,
        "retained_negatives": 5,
        "witnesses": 10,
    }
    assert sum(w["result"] == "fail" for w in flow["witnesses"]) == 5
    assert sum(w["result"] == "pass" for w in flow["witnesses"]) == 5
    assert all(w["independent_reproduction"] is False for w in flow["witnesses"])


def test_x1_route_is_unsent_and_standby_is_untouched() -> None:
    route = load("x1/route-plan.json")
    assert route["prospective_successor_title"] == "Neris Solane"
    assert route["prospective_successor_phase"] == "v675-v4"
    assert route["sent"] is False
    assert route["successor_precontacted"] is False
    assert route["standby_contacted"] is False
    assert route["task_created_or_forked"] is False
    assert route["collaboration_subagent_spawned"] is False


def test_x1_contains_no_x2_outcome_or_closeout_path() -> None:
    truth = load("x1/phase-truth.json")
    manifest = load("validation/x1-manifest.json")
    assert truth["planning_only"] is True
    assert truth["x2_outcomes_present"] is False
    assert truth["observed_outcomes"] is None
    assert not any("/x2/" in row["path"] or "/closeout/" in row["path"] for row in manifest["entries"])


def test_x1_manifest_replays_normalized_candidate_bytes() -> None:
    manifest = load("validation/x1-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    assert manifest["entry_count"] >= 15
    for entry in manifest["entries"]:
        data = normalized(ROOT / entry["path"])
        assert len(data) == entry["bytes"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]


def test_x1_privacy_and_review_pass() -> None:
    privacy = load("validation/x1-staged-privacy.json")
    review = load("validation/x1-staged-review.json")
    assert privacy["valid"] is True
    assert privacy["candidates"] == []
    assert privacy["confirmed"] == []
    assert review["valid"] is True
    assert review["passed"] == review["total"]


def test_all_phase_json_is_strictly_parseable() -> None:
    files = list(PHASE.rglob("*.json"))
    assert len(files) >= 15
    for path in files:
        json.loads(path.read_text(encoding="utf-8"))
