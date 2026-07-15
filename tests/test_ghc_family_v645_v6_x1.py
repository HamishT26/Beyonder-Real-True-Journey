from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v645-v6"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def test_exactly_ten_distinct_proposals() -> None:
    data = load("x1-proposals.json")
    assert len(data["proposals"]) == 10
    assert len({row["title"] for row in data["proposals"]}) == 10
    assert data["prior_frozen_proposal_count"] == 360
    assert data["frozen_chain_count_after_x1"] == 370


def test_proposals_have_all_preregistered_fields() -> None:
    required = {
        "hypothesis", "null_or_failure", "approval_class", "execution_lane",
        "current_primary_or_official_source_needs", "concrete_artifacts",
        "test_falsifier_or_acceptance_gate", "rollback_or_recovery",
        "protected_gates", "expected_disposition",
    }
    for row in load("x1-proposals.json")["proposals"]:
        assert required <= set(row)
        assert all(row[field] for field in required)


def test_expected_distribution_and_x1_separation() -> None:
    data = load("x1-proposals.json")
    states = [row["expected_disposition"] for row in data["proposals"]]
    assert {state: states.count(state) for state in set(states)} == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
    assert data["x2_execution_present"] is False
    assert not (PHASE / "phase-truth.json").exists()
    assert not (PHASE / "x2-proposal-ledger.json").exists()


def test_novelty_and_portfolio_collisions_are_zero() -> None:
    assert load("provenance/prior-proposal-collision-audit.json")["exact_title_collision_count"] == 0
    assert load("provenance/prior-portfolio-collision-audit.json")["exact_collision_count"] == 0
    assert len(load("provenance/rejected-candidate-register.json")["candidates"]) == 1


def test_portfolio_and_inherited_packet_counts() -> None:
    data = load("approval-packets/x1-approval-portfolio.json")
    assert data["counts"] == {"safe_now": 20, "candidates": 12, "inherited_exact": 10, "inherited_blocked": 5}
    assert data["completion_credit_before_x2"] == 0


def test_method_flow_retains_fail_and_pass_witnesses() -> None:
    data = load("method-flow/method-flow-state.json")
    assert data["counts"]["methods"] == 6
    assert data["counts"]["states"]["preferred"] == 6
    assert data["counts"]["witness_results"] == {"fail": 6, "pass": 6}
    assert load("method-flow/runner-validation.json")["valid"] is True


def test_negative_baseline_is_preserved() -> None:
    data = load("validation/x1-operational-negatives.json")
    assert data["inherited_effective"] == 2172
    assert data["preregistered_synthetic"] == 70
    assert data["new_operational_count"] == 6
    assert data["effective_after_x1"] == 2248


def test_focus_and_practice_are_bounded() -> None:
    data = load("focus/primary-focus-receipt.json")
    assert data["primary_trinity_pillar"] == "GMUT Mind"
    assert "maritime" in data["bounded_human_practice"]
    assert "professional competence" in data["not_claimed"]


def test_sources_are_current_family_states_and_zero_row() -> None:
    data = load("sources/source-ledger.json")
    assert all(row["status"] in {"current", "stable", "draft", "watch"} for row in data["sources"])
    assert data["real_data_rows_ingested"] == 0
    assert data["likelihood_evaluations"] == 0


def test_route_is_not_sent() -> None:
    data = load("orchestration/terminal-route-plan.json")
    assert data["current_state"] == "PREPARED_NOT_SENT"
    assert data["send_count"] == 0


if __name__ == "__main__":
    tests = sorted((name, value) for name, value in globals().items() if name.startswith("test_") and callable(value))
    failures: list[str] = []
    for name, function in tests:
        try:
            function()
        except Exception as exc:  # pragma: no cover - direct runner failure surface
            failures.append(f"{name}: {type(exc).__name__}: {exc}")
    print(f"{len(tests) - len(failures)}/{len(tests)} v645-v6 x1 scoped tests passed")
    if failures:
        print("\n".join(failures))
        raise SystemExit(1)
