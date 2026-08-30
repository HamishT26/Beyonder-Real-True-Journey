from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
BASE = REPO / "docs" / "elowen-cairn" / "v678-v5"
X1 = BASE / "x1"
SOURCE = "0021481a0c9681c077bce277e6ac0f2fcb37dbcd"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(relative: str):
    return json.loads((X1 / relative).read_text(encoding="utf-8"))


def test_source_anchors_and_inherited_failed_canonical_are_exact_and_unreplayed() -> None:
    data = load("source-verification.json")
    assert data["source"] == SOURCE
    assert data["anchors"] == {
        "liora_v678_v3_final_and_tamar_source": "471db44e52f9ab776b6abf05896d405022524b18",
        "tamar_x1": "29a886dc5838093ed092ffc20c3d86af3b24e47c",
        "tamar_evidence": "18ffd0764b6df5f64360c286eabcdb361e4c29c3",
        "tamar_exact_final": SOURCE,
    }
    assert data["source_to_final_phase_commits"] == 3
    assert data["source_to_final_merges"] == 0
    assert data["tamar_failed_canonical_receipt_sha256"] == "0eac7b907921e22a00633dfa9878175f6564e5d6e973bb127442dee3a424f418"
    assert data["tamar_failed_canonical_latch_sha256"] == "3839b406cbadf2d18db926be2a3175da0ff08f304c1dfd6309539ac8188d7354"
    assert data["tamar_dependency_corrected_composite_receipt_sha256"] == "9e8ab01dedbedd1f8942ed93b3511ad2eee06046d67926630f1f2d7db87a5046"
    assert data["tamar_dependency_corrected_composite_latch_sha256"] == "b8ce7fc691e9b58b45cc43498da398540a0c55865323d948c8bc4542ead035d4"
    assert data["tamar_dependency_corrected_composite_payload_sha256"] == "44b2c8fd6ed0f77a3c23e04fbcb627449ee86a4a313c91052e500230f1dee624"
    assert data["tamar_canonical_invocation_count"] == 1
    assert data["tamar_canonical_success_count"] == 0
    assert data["tamar_canonical_replay_count"] == 0
    assert data["tamar_composite_status"] == "VALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT"
    assert data["failed_canonical_preserved_at_zero_success_credit"] is True
    assert data["inherited_canonical_replayed"] is False


def test_freeze_extends_declared_chain_with_exactly_sixty_rows() -> None:
    data = load("new-proposal-freeze.json")
    assert data["status"] == "FROZEN_PLANNING_ONLY"
    assert data["declared_chain_before"] == 8510
    assert data["new_elowen_proposals"] == 60
    assert data["declared_chain_after"] == 8570
    assert len(data["proposals"]) == 60


def test_proposal_contract_fields_ids_titles_and_dispositions() -> None:
    rows = load("new-proposal-freeze.json")["proposals"]
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
    assert [row["proposal_id"] for row in rows] == [f"EC6785-N{i:03d}" for i in range(1, 61)]
    assert len({row["title"].casefold() for row in rows}) == 60
    assert all(required <= row.keys() for row in rows)
    counts = Counter(row["expected_disposition"] for row in rows)
    assert set(counts) == LABELS
    assert counts == Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})


def test_reachable_semantic_audit_has_no_collision_or_quarantine() -> None:
    data = load("semantic-neighbor-audit.json")
    assert data["source_tree"] == SOURCE
    assert data["declared_chain_count"] == 8510
    assert data["reachable_proposal_json_blobs"] >= 2600
    assert data["reachable_unique_id_title_records"] >= 3400
    assert data["json_parse_failures"] == 0
    assert data["exact_title_collisions"] == 0
    assert data["selected_rows_quarantined"] == 0
    assert data["maximum_selected_score"] < data["quarantine_threshold"]
    assert len(data["neighbors"]) == 60
    assert "not a universal novelty proof" in data["limitation"]


def test_twenty_inherited_reviews_are_zero_credit() -> None:
    data = load("inherited-zero-credit-review.json")
    assert data["count"] == 20
    assert data["novelty_credit"] == 0
    assert data["completion_credit"] == 0
    assert len(data["reviews"]) == 20
    assert all(row["status"] == "reviewed_inherited_zero_credit" for row in data["reviews"])


def test_mutations_are_preregistered_and_unexecuted() -> None:
    data = load("mutation-preregistration.json")
    assert data["proposal_count"] == 60
    assert data["mutations_per_proposal"] == 4
    assert data["mutation_count"] == 240
    assert len(data["mutations"]) == 240
    assert set(Counter(row["proposal_id"] for row in data["mutations"]).values()) == {4}
    assert all(row["execution_status"] == "preregistered_unexecuted_x1" for row in data["mutations"])


def test_portfolio_and_clean_fix_refine_floors_are_planning_only() -> None:
    portfolio = load("portfolio-freeze.json")
    assert {key: len(portfolio[key]) for key in ("safe_now", "candidate", "exact_approval", "blocked")} == {
        "safe_now": 60,
        "candidate": 30,
        "exact_approval": 20,
        "blocked": 10,
    }
    assert all(row["status"] == "planned_unexecuted_x1" for row in portfolio["safe_now"] + portfolio["candidate"])
    assert all(row["status"] == "unexecuted_exact_gate" for row in portfolio["exact_approval"])
    assert all(row["status"] == "blocked_unexecuted" for row in portfolio["blocked"])
    cfr = load("clean-fix-refine-plan.json")
    assert len(cfr["owner_tasks"]) == 60
    assert len(cfr["successor_recommendations"]) == 30
    assert all(row["status"] == "planned_unexecuted_x1" for row in cfr["owner_tasks"])
    assert all(row["credit"] == "zero_elowen_completion_credit" for row in cfr["successor_recommendations"])


def test_skill_runner_and_successor_seed_floors_are_owner_local() -> None:
    data = load("skill-runner-plan.json")
    assert len(data["phase_local_skills"]) == 20
    assert len(data["family_current_runners"]) == 10
    assert len(data["successor_skill_recommendations"]) == 10
    assert len(data["successor_runner_recommendations"]) == 10
    assert all(row["global_install"] is False for row in data["phase_local_skills"])
    assert all(row["name"].startswith(("ghc_family_", "build_ghc_family_")) for row in data["family_current_runners"])
    successor = load("successor-recommendations.json")
    assert successor["recipient_unresolved_until_terminal_gate"] is True
    assert successor["recommendation_count"] == 50


def test_startup_failures_and_recoveries_are_retained_separately() -> None:
    data = load("method-flow-startup.json")
    failures = [row for row in data["methods"] if row["truth"] is False]
    passes = [row for row in data["methods"] if row["truth"] is True]
    assert len(failures) == 14
    assert len(passes) == 14
    assert data["new_effective_methods"] == 28
    assert data["current_overlay"] == {
        "effective_negatives": 46740,
        "effective_methods": 43770,
        "retained_failed_witnesses": 18401,
        "bounded_passing_witnesses": 28454,
        "open_gaps": 404,
        "exact_gates": 395,
    }
    pass_ids = {row["method_id"] for row in passes}
    assert all(row["status"] == "failed_zero_credit" and row["recovered_by"] in pass_ids for row in failures)
    assert data["failure_erasure_forbidden"] is True


def test_sources_are_vocabulary_only_and_lens_is_wholly_synthetic() -> None:
    sources = load("official-source-ledger.json")
    assert len(sources["sources"]) == 8
    assert all(row["url"].startswith("https://") for row in sources["sources"])
    assert "not observations" in sources["source_boundary"]
    lens = load("primary-pillar-and-lens.json")
    assert lens["primary_pillar"] == "Freed ID and CBR Heart"
    assert set(lens["secondary_pillars"]) == {"GMUT Mind", "THOS Body"}
    assert len(lens["bounded_wholly_synthetic_learning_lenses"]) == 3
    assert all("synthetic" in row for row in lens["bounded_wholly_synthetic_learning_lenses"])
    assert lens["real_world_rows_or_actions"] == 0


def test_x1_truth_route_hold_and_identity_boundaries() -> None:
    truth = load("phase-truth.json")
    assert truth["status"] == "FROZEN_PLANNING_ONLY"
    assert truth["executed_core_outcomes"] == {label: 0 for label in sorted(LABELS)}
    assert truth["x2_implementation_present"] is False
    assert truth["x2_outcomes_claimed"] is False
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    route = load("route-hold.json")
    assert route["route_state"] == "HOLD_UNTIL_ELOWEN_V676_V6_TERMINAL_GATE"
    assert route["prospective_successor_title"] == "Sylven Arc"
    assert route["prospective_successor_phase"] == "v678-v6"
    assert route["successor_inferred"] is False
    assert route["precontact_performed"] is False
    assert route["send_count"] == 0
    identity = (X1 / "identity-and-boundary.md").read_text(encoding="utf-8")
    for phrase in ("relational working language only", "not evidence of consciousness", "Māori authority", "Hamish may rename"):
        assert phrase in identity


def test_no_x2_material_and_no_private_payload_in_x1_docs() -> None:
    assert not (BASE / "x2").exists()
    assert not list((REPO / "scripts").glob("*elowen_cairn_v678_v5_x2*"))
    assert not list((REPO / "tests").glob("*elowen_cairn_v678_v5_x2*"))
    patterns = [
        re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
        re.compile(r"(?i)(thread_id|source_thread_id|clientThreadId)"),
        re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
        re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    ]
    for path in BASE.rglob("*"):
        if not path.is_file():
            continue
        value = path.read_text(encoding="utf-8")
        for pattern in patterns:
            assert pattern.search(value) is None, f"{pattern.pattern} in {path.relative_to(REPO)}"


def test_all_x1_json_parses_and_documents_remain_below_cap() -> None:
    json_paths = list(X1.glob("*.json")) + list((BASE / "validation").glob("*.json"))
    assert len(json_paths) >= 14
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    for path in BASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".html"}:
            assert len(path.read_text(encoding="utf-8").split()) <= 100_000
