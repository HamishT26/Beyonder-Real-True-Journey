from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
BASE = REPO / "docs" / "sylven-arc" / "v678-v6"
X1 = BASE / "x1"
SOURCE = "d7a2e3d1851d8a9eb6a8707968a47354b44e824a"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(relative: str):
    return json.loads((X1 / relative).read_text(encoding="utf-8"))


def test_source_anchors_and_inherited_dependency_corrected_truth_are_exact() -> None:
    data = load("source-verification.json")
    assert data["source"] == SOURCE
    assert data["anchors"] == {
        "elowen_source": "0021481a0c9681c077bce277e6ac0f2fcb37dbcd",
        "elowen_x1": "c938128b0e6307c4aaed8966340486b8c5315382",
        "elowen_evidence": "04095ca5d8ee6b37f47de2540afa0047f67ca61c",
        "elowen_first_final": "831f948e326e3875ef0d5d7391560297ce0e2ee8",
        "elowen_corrected_final": SOURCE,
    }
    assert data["source_to_final_phase_commits"] == 4
    assert data["source_to_final_merges"] == 0
    assert data["elowen_failed_canonical_receipt_sha256"] == "bfa2115b166ee9eb5f3f9aaac9a4d7f5379e574a24ac4dc60bc7b8accf758ccd"
    assert data["elowen_failed_canonical_latch_sha256"] == "cae4d857e5485817e0a4b281a5872aeeddaed41e2369abf9defdae440191afdf"
    assert data["elowen_failed_canonical_payload_sha256"] == "36f8a96bb375543e02e6095e34002dbef4bb83b78d51d25095b59b889ed66507"
    assert data["elowen_component_receipt_sha256"] == "4080450cf77fd8f8a74963998156bda57e51fbdc3d6a54eb87bfe4b1abeac034"
    assert data["elowen_component_latch_sha256"] == "78a1643b54e382856a062a7992b9e19131223cba3400bb7700ff950694e1dc2d"
    assert data["elowen_component_payload_sha256"] == "cc62ac6fa67a609320190cccf2bcb07694583d813d794b2ab43d5ea2853719ce"
    assert data["elowen_canonical_success_count"] == 0
    assert data["elowen_canonical_replay_count"] == 0
    assert data["elowen_component_success_count"] == 1
    assert data["elowen_component_replay_count"] == 0
    assert data["failed_canonical_preserved_at_zero_success_credit"] is True
    assert data["inherited_validation_replayed"] is False


def test_freeze_extends_declared_chain_with_exactly_sixty_rows() -> None:
    data = load("new-proposal-freeze.json")
    assert data["status"] == "FROZEN_PLANNING_ONLY"
    assert data["declared_chain_before"] == 8570
    assert data["new_sylven_proposals"] == 60
    assert data["declared_chain_after"] == 8630
    assert len(data["proposals"]) == 60


def test_proposal_contract_fields_ids_titles_and_dispositions() -> None:
    rows = load("new-proposal-freeze.json")["proposals"]
    required = {"proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
    assert [row["proposal_id"] for row in rows] == [f"SA6786-N{i:03d}" for i in range(1, 61)]
    assert len({row["title"].casefold() for row in rows}) == 60
    assert all(required <= row.keys() for row in rows)
    counts = Counter(row["expected_disposition"] for row in rows)
    assert set(counts) == LABELS
    assert counts == Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})


def test_reachable_semantic_audit_has_no_collision_or_quarantine() -> None:
    data = load("semantic-neighbor-audit.json")
    assert data["source_tree"] == SOURCE
    assert data["declared_chain_count"] == 8570
    assert data["reachable_proposal_json_blobs"] >= 2679
    assert data["reachable_unique_id_title_records"] >= 4455
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
    assert {key: len(portfolio[key]) for key in ("safe_now", "candidate", "exact_approval", "blocked")} == {"safe_now": 60, "candidate": 30, "exact_approval": 20, "blocked": 10}
    assert all(row["status"] == "planned_unexecuted_x1" for row in portfolio["safe_now"] + portfolio["candidate"])
    assert all(row["status"] == "unexecuted_exact_gate" for row in portfolio["exact_approval"])
    assert all(row["status"] == "blocked_unexecuted" for row in portfolio["blocked"])
    cfr = load("clean-fix-refine-plan.json")
    assert len(cfr["owner_tasks"]) == 60
    assert len(cfr["successor_recommendations"]) == 30
    assert all(row["status"] == "planned_unexecuted_x1" for row in cfr["owner_tasks"])
    assert all(row["credit"] == "zero_sylven_completion_credit" for row in cfr["successor_recommendations"])


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
    assert "synthetic" in successor["recommended_practice"]


def test_startup_failures_and_recoveries_are_retained_separately() -> None:
    data = load("method-flow-startup.json")
    failures = [row for row in data["methods"] if row["truth"] is False]
    passes = [row for row in data["methods"] if row["truth"] is True]
    assert len(failures) == 13
    assert len(passes) == 13
    assert data["new_effective_methods"] == 26
    assert data["current_overlay"] == {"effective_negatives": 47020, "effective_methods": 44590, "retained_failed_witnesses": 18681, "bounded_passing_witnesses": 28994, "open_gaps": 407, "exact_gates": 398}
    pass_ids = {row["method_id"] for row in passes}
    assert all(row["status"] == "failed_zero_credit" and row["recovered_by"] in pass_ids for row in failures)
    assert data["failure_erasure_forbidden"] is True


def test_sources_are_vocabulary_only_and_lenses_are_wholly_synthetic() -> None:
    sources = load("official-source-ledger.json")
    assert len(sources["sources"]) == 7
    assert all(row["url"].startswith("https://") for row in sources["sources"])
    assert "not observations" in sources["source_boundary"]
    lens = load("primary-pillar-and-lens.json")
    assert lens["primary_pillar"] == "THOS Body"
    assert set(lens["secondary_pillars"]) == {"GMUT Mind", "Freed ID and CBR Heart"}
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
    assert route["route_state"] == "HOLD_UNTIL_SYLVEN_V678_V6_TERMINAL_GATE"
    assert route["prospective_successor_title"] == "Caelen Morrow"
    assert route["prospective_successor_phase"] == "v678-v7"
    assert route["successor_inferred"] is False
    assert route["precontact_performed"] is False
    assert route["send_count"] == 0
    identity = (X1 / "identity-and-boundary.md").read_text(encoding="utf-8")
    for phrase in ("relational working language only", "not evidence of consciousness", "Maori authority", "Hamish may rename"):
        assert phrase in identity


def test_no_x2_material_and_no_private_payload_in_x1_docs() -> None:
    assert not (BASE / "x2").exists()
    assert not list((REPO / "scripts").glob("*sylven_arc_v678_v6_x2*"))
    assert not list((REPO / "tests").glob("*sylven_arc_v678_v6_x2*"))
    patterns = [re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"), re.compile(r"(?i)(thread_id|source_thread_id|clientThreadId)"), re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"), re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)]
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
