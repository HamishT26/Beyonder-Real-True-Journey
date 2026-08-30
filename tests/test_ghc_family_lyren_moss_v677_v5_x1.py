"""Planning-only x1 checks for Lyren Moss v677-v5."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs" / "lyren-moss" / "v677-v5"
SCRIPT = REPO / "scripts" / "build_ghc_family_lyren_moss_v677_v5_x1.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("lyren_v677_v5_x1", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_constants_and_new_contracts_are_exact() -> None:
    module = load_builder()
    rows = module.new_rows()
    assert module.SOURCE == "aca9fbd51662312c49850c773d99dab3cc55be04"
    assert module.PHASE == "v677-v5"
    assert len(rows) == 60
    assert len({row["proposal_id"] for row in rows}) == 60
    assert len({row["title"].casefold() for row in rows}) == 60
    assert {row["expected_disposition"] for row in rows} == {
        "completed",
        "represented",
        "open_gap",
        "exact_gate",
    }
    assert sum(row["expected_disposition"] == "completed" for row in rows) == 42
    assert sum(row["expected_disposition"] == "represented" for row in rows) == 12
    assert sum(row["expected_disposition"] == "open_gap" for row in rows) == 3
    assert sum(row["expected_disposition"] == "exact_gate" for row in rows) == 3


def test_generated_x1_is_planning_only_and_count_exact() -> None:
    phase = read_json(ROOT / "x1" / "phase-truth.json")
    combined = read_json(ROOT / "x1" / "combined-program.json")
    portfolio = read_json(ROOT / "x1" / "portfolio-freeze.json")
    assert phase["lifecycle_state"] == "PLANNING_ONLY_X1"
    assert phase["x2_implementation_present"] is False
    assert phase["observed_outcomes_present"] is False
    assert phase["completion_claim_present"] is False
    assert phase["route_send_count"] == 0
    assert combined["total_rows"] == 120
    assert combined["inherited_selected"] == 60
    assert combined["genuinely_new"] == 60
    assert portfolio["counts"] == {
        "blocked": 10,
        "candidate_total": 100,
        "exact_approval": 20,
        "owner_candidate": 80,
        "owner_safe_now": 120,
        "successor_candidate_recommendations": 20,
    }
    assert not (ROOT / "x2").exists()


def test_inherited_selection_has_zero_credit() -> None:
    inherited = read_json(ROOT / "x1" / "inherited-proposal-selection.json")
    assert inherited["selection_count"] == 60
    assert inherited["novelty_credit"] == 0
    assert inherited["automatic_completion_credit"] == 0
    assert all(row["lyren_novelty_credit"] == 0 for row in inherited["rows"])
    assert all(row["automatic_completion_credit"] == 0 for row in inherited["rows"])


def test_semantic_audit_fails_closed_without_collisions() -> None:
    audit = read_json(ROOT / "x1" / "semantic-neighbor-audit.json")
    assert audit["source"] == "aca9fbd51662312c49850c773d99dab3cc55be04"
    assert audit["declared_chain_count"] == 8030
    assert audit["exact_title_collisions"] == []
    assert audit["json_parse_failures"] == 0
    assert audit["selected_rows_quarantined"] == 0
    assert audit["maximum_selected_score"] < audit["quarantine_threshold"]
    assert audit["universal_novelty_proved"] is False


def test_tool_skill_runner_and_cleanup_plans_are_bounded() -> None:
    tools = read_json(ROOT / "x1" / "toolchain-verification-plan.json")
    skill_runner = read_json(ROOT / "x1" / "skill-runner-plan.json")
    clean = read_json(ROOT / "x1" / "clean-fix-refine-plan.json")
    assert tools["candidate_count"] == 25
    assert len(tools["candidates"]) == 25
    assert tools["installation_authorized"] is False
    assert len(skill_runner["owner_skill_ideas"]) == 20
    assert len(skill_runner["successor_skill_recommendations"]) == 10
    assert len(skill_runner["owner_runner_ideas"]) == 10
    assert len(skill_runner["successor_runner_recommendations"]) == 10
    assert len(clean["owner"]) == 100
    assert len(clean["successor_recommendations"]) == 30


def test_flashcard_plan_uses_four_tiers_and_modular_sections() -> None:
    deck = read_json(ROOT / "x1" / "flashcard-plan.json")
    assert deck["tier_order"] == [
        "freed_id_anchor",
        "trinity_pillar",
        "bounded_practice",
        "task",
    ]
    assert deck["section_count"] >= 10
    assert len(deck["sections"]) == deck["section_count"]
    assert deck["content_addressed"] is True
    assert deck["supersession_non_erasing"] is True
    assert deck["large_baton_file_only"] is True
    assert deck["live_message_compact"] is True


def test_exact_and_blocked_packets_remain_unexecuted() -> None:
    portfolio = read_json(ROOT / "x1" / "portfolio-freeze.json")
    rows = portfolio["exact_approval"] + portfolio["blocked"]
    assert len(rows) == 30
    assert all(row["state"] == "UNEXECUTED" for row in rows)
    assert all(row["execution_authorized"] is False for row in rows)


def test_route_hold_prevents_precontact() -> None:
    route = read_json(ROOT / "x1" / "route-hold.json")
    assert route["state"] == "PLANNING_ONLY_X1_ROUTE_HOLD"
    assert route["send_count"] == 0
    assert route["precontact_forbidden"] is True
    assert route["successor"] == "Ilyra Fen"
    assert route["successor_phase"] == "v677-v6"


def test_manifest_covers_generated_x1_files() -> None:
    manifest = read_json(ROOT / "validation" / "x1-manifest.json")
    actual = {
        path.relative_to(REPO).as_posix()
        for path in (ROOT / "x1").rglob("*")
        if path.is_file()
    }
    actual.update(
        {
            "scripts/build_ghc_family_lyren_moss_v677_v5_x1.py",
            "scripts/ghc_family_lyren_moss_v677_v5_x1_manifest.py",
            "tests/test_ghc_family_lyren_moss_v677_v5_x1.py",
        }
    )
    recorded = {row["path"] for row in manifest["entries"]}
    assert recorded == actual
    assert manifest["entry_count"] == len(actual)


def test_no_real_world_execution_or_stage20_promotion() -> None:
    overview = (ROOT / "x1" / "x1-overview.md").read_text(encoding="utf-8")
    assert "No x2 implementation" in overview
    assert "NOT_READY_FOR_STAGE_20" in json.dumps(read_json(ROOT / "x1" / "phase-truth.json"))
    assert "Theory-of-Everything proof" in overview
    assert "Māori-authority" in overview
