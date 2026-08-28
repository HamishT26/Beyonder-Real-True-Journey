from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs" / "auren-lark" / "v674-v1"
X1 = PHASE / "x1"
BUILDER_PATH = REPO / "scripts" / "build_ghc_family_auren_lark_v674_v1_x1.py"

spec = importlib.util.spec_from_file_location("auren_v674_v1_x1", BUILDER_PATH)
builder = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(builder)


def load(name: str):
    return json.loads((X1 / name).read_text(encoding="utf-8"))


def test_builder_source_and_packet_are_exact():
    assert builder.SOURCE == "3ba783297438ee89d5778065e30de737af470855"
    assert builder.SOURCE_PACKET_SHA256 == "12a1def1734aea3eb431b9d591ae6e55a736dad589a47e5e41b5f8be77cd4296"


def test_x1_exists_and_x2_is_absent():
    assert X1.is_dir()
    assert not (PHASE / "x2").exists()


def test_activation_intake_preserves_bad_digest_and_correction():
    intake = load("activation-intake.json")
    assert intake["hamish_correction_received"] is True
    assert intake["routed_erroneous_packet_sha256"].startswith("ba785c")
    assert intake["subagents_forks_or_new_tasks"] is False


def test_relational_boundary_is_explicit():
    identity = load("identity-and-boundary.json")
    assert identity["relational_working_language_only"] is True
    assert "consciousness" in identity["not_evidence_of"]
    assert "Maori_authority" in identity["not_evidence_of"]


def test_sixty_inherited_rows_are_zero_credit_and_distinct():
    freeze = load("inherited-revalidation-freeze.json")
    assert freeze["row_count"] == 60
    assert freeze["novelty_credit"] == 0
    assert freeze["completion_credit"] == 0
    assert len({row["title"].casefold() for row in freeze["rows"]}) == 60
    assert all(row["novelty_credit"] == row["completion_credit"] == 0 for row in freeze["rows"])


def test_sixty_new_rows_and_expected_outcomes():
    freeze = load("new-proposal-freeze.json")
    assert freeze["proposal_count"] == 60
    assert freeze["proposal_chain_if_x2_evidence_frozen"] == 6610
    assert freeze["expected_outcomes"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    assert freeze["outcomes_observed"] is False
    assert set(freeze["allowed_outcomes"]) == {"completed", "represented", "open_gap", "exact_gate"}


def test_new_titles_are_distinct_and_planning_only():
    rows = load("new-proposal-freeze.json")["proposals"]
    assert len({row["title"].casefold() for row in rows}) == 60
    assert all(row["x1_state"] == "planning_only_not_observed_outcome" for row in rows)
    assert all(row["expected_execution_disposition"] in builder.CORE_OUTCOMES for row in rows)


def test_portfolio_counts_match_live_authority():
    portfolio = load("portfolio-freeze.json")
    assert len(portfolio["safe_now"]) == 120
    assert len(portfolio["owner_candidates"]) == 80
    assert len(portfolio["successor_candidates"]) == 20
    assert len(portfolio["exact_approval"]) == 20
    assert len(portfolio["blocked"]) == 10
    assert len(portfolio["owner_skill_ideas"]) == 20
    assert len(portfolio["successor_skill_ideas"]) == 10
    assert len(portfolio["owner_runner_ideas"]) == 10
    assert len(portfolio["successor_runner_ideas"]) == 10
    assert len(portfolio["owner_clean_fix_refine"]) == 100
    assert len(portfolio["successor_clean_fix_refine"]) == 30


def test_safe_rows_are_split_without_external_authority():
    rows = load("portfolio-freeze.json")["safe_now"]
    counts = Counter(row["execution_lane"] for row in rows)
    assert counts == {"immediate_x1_safe": 20, "x2_build_task": 100}
    assert all(row["approval_bucket"] == "safe_now" for row in rows)


def test_exact_and_blocked_rows_remain_unexecuted():
    portfolio = load("portfolio-freeze.json")
    assert all(row["state"].startswith("held_unexecuted") for row in portfolio["exact_approval"])
    assert all(row["state"] == "visible_and_unexecuted" for row in portfolio["blocked"])


def test_toolchain_is_exact_thirteen_and_x1_does_not_install():
    plan = load("toolchain-plan.json")
    assert plan["x1_installation_performed"] is False
    assert len(plan["python"]) == 7
    assert len(plan["node"]) == 6
    assert plan["codex_cli"]["registry_latest"] == "0.150.1"
    assert plan["codex_cli"]["excluded_alpha"].startswith("0.151.0-alpha")
    assert all(len(row["sha256"]) == 64 for row in plan["python"])
    assert all(row["integrity"].startswith("sha512-") for row in plan["node"])


def test_route_schedule_has_416_slots_and_current_edge():
    route = load("route-roster-plan.json")
    assert route["assignment_count"] == 416
    assert route["assignments"][0]["phase"] == "v674-v1"
    assert route["assignments"][0]["owner"] == "Auren Lark"
    assert route["assignments"][1]["owner"] == "Sable Rook"
    assert route["assignments"][-1]["phase"] == "v725-v8"
    assert route["delivery_claim"] is False


def test_future_route_correction_is_resolved_and_current_edge_is_unchanged():
    register = load("route-clarification-register.json")
    row = register["clarifications"][0]
    assert row["state"] == "resolved_by_newer_hamish_live_instruction"
    assert row["current_exact_sequence"] == [
        "Elowen Cairn v674-v7",
        "Sylven Arc v674-v8",
        "Caelen Morrow v675-v1",
        "Eiren Kestrel v675-v2",
    ]
    assert "Sable Rook v674-v2" in row["current_edge"]
    assert row["truth_effect"] == "resolved correction; not an open gap or exact gate"


def test_method_flow_retains_every_startup_failure_at_zero_credit():
    ledger = load("method-flow-startup.json")
    assert ledger["startup_failure_count"] == 19
    assert all(row["success_credit"] == 0 and row["failure_retained"] for row in ledger["startup_failures"])
    assert ledger["source_repository_truth_unchanged"]["verdict"] == "NOT_READY_FOR_STAGE_20"


def test_source_ledger_claims_no_endorsement_or_empirical_credit():
    ledger = load("source-ledger.json")
    assert ledger["endorsement_or_artifact_validation"] is False
    assert ledger["empirical_or_professional_credit"] == 0
    assert ledger["package_registry_rows"] == 13


def test_manifest_replays_working_tree_bytes():
    manifest = load("x1-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    assert manifest["self_excluded"].endswith("x1-manifest.json")
    for entry in manifest["entries"]:
        raw = (REPO / entry["path"]).read_bytes()
        import hashlib

        assert len(raw) == entry["bytes"]
        assert hashlib.sha256(raw).hexdigest() == entry["sha256"]


def test_all_phase_json_parses_and_uses_no_other_core_outcome_labels():
    for path in PHASE.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    allowed = set(builder.CORE_OUTCOMES)
    outcomes = {row["expected_execution_disposition"] for row in load("new-proposal-freeze.json")["proposals"]}
    assert outcomes <= allowed


def test_overview_preserves_terminal_verdict_and_practice_limits():
    text = (X1 / "integrated-overview.md").read_text(encoding="utf-8")
    assert "NOT_READY_FOR_STAGE_20" in text
    assert "No real station" in text
    assert "not employment" in text
    assert len(text.split()) >= 1200
