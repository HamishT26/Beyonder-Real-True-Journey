from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v645-v8"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def test_exactly_ten_distinct_proposals() -> None:
    data = load("x1-proposals.json")
    assert len(data["proposals"]) == 10
    assert len({row["title"] for row in data["proposals"]}) == 10
    assert data["prior_frozen_proposal_count"] == 380
    assert data["frozen_chain_count_after_x1"] == 390


def test_proposals_have_every_frozen_field() -> None:
    required = {
        "hypothesis", "null_or_failure", "approval_class", "execution_lane",
        "current_primary_or_official_source_needs", "concrete_artifacts",
        "test_falsifier_or_acceptance_gate", "rollback_or_recovery",
        "protected_gates", "expected_disposition", "novelty_against_380_frozen_proposals",
    }
    for row in load("x1-proposals.json")["proposals"]:
        assert required <= set(row)
        assert all(row[field] for field in required)


def test_expected_distribution_and_x1_separation() -> None:
    data = load("x1-proposals.json")
    states = [row["expected_disposition"] for row in data["proposals"]]
    assert {state: states.count(state) for state in set(states)} == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
    assert data["x2_execution_present"] is False
    for forbidden in ("phase-truth.json", "x2-proposal-ledger.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"):
        assert not (PHASE / forbidden).exists()


def test_novelty_corpus_and_collisions() -> None:
    corpus = load("provenance/frozen-chain-proposal-index.json")
    assert corpus["prior_file_count"] == 38
    assert corpus["prior_proposal_count"] == 380
    assert len(corpus["prior_proposals"]) == 380
    assert load("provenance/prior-proposal-collision-audit.json")["exact_title_collision_count"] == 0
    assert load("provenance/prior-portfolio-collision-audit.json")["exact_collision_count"] == 0


def test_sources_have_only_allowed_statuses_and_zero_external_rows() -> None:
    data = load("sources/source-ledger.json")
    assert len(data["sources"]) >= 20
    assert all(row["status"] in {"current", "stable", "draft", "watch"} for row in data["sources"])
    assert data["real_data_rows_ingested"] == 0
    assert data["likelihood_evaluations"] == 0
    assert data["real_participants"] == 0
    assert data["real_keys_or_proofs"] == 0


def test_method_flow_retains_fail_and_pass_witnesses() -> None:
    data = load("method-flow/method-flow-state.json")
    assert data["counts"]["methods"] == 4
    assert data["counts"]["states"]["preferred"] == 4
    assert data["counts"]["witness_results"] == {"fail": 4, "pass": 4}
    assert load("method-flow/runner-validation.json")["valid"] is True


def test_negative_baseline_and_new_failures_are_preserved() -> None:
    data = load("validation/x1-operational-negatives.json")
    assert data["baton_time_inherited"] == 2353
    assert data["post_baton_inherited"] == 0
    assert data["post_baton_inherited_ids"] == []
    assert data["inherited_effective"] == 2353
    assert data["preregistered_synthetic"] == 70
    assert data["new_operational_count"] == 4
    assert data["effective_after_x1"] == 2427


def test_focus_practice_and_identity_are_bounded() -> None:
    focus = load("focus/primary-focus-receipt.json")
    identity = load("identity-receipt.json")
    assert focus["primary_trinity_pillar"] == "GMUT Mind"
    assert "railway traffic control" in focus["bounded_human_practice"]
    assert "professional competence" in focus["not_claimed"]
    assert "relational working labels only" in identity["boundary"]


def test_route_is_prepared_not_sent() -> None:
    data = load("orchestration/terminal-route-plan.json")
    assert data["current_state"] == "PREPARED_NOT_SENT"
    assert data["target_title"] == "Eiren Kestrel"
    assert data["target_phase"] == "v646-v1"
    assert data["send_count"] == 0


def test_environment_has_no_update_or_host_change() -> None:
    version = load("environment/version-receipt.json")
    sandbox = load("environment/sandbox-readonly-audit.json")
    assert version["codex_cli"]["action"] == "verified_only_no_update"
    assert version["codex_desktop"]["action"] == "verified_only_no_update"
    assert not any(version["host_actions"].values())
    assert sandbox["windows_sandbox_executable"] == "not_found"
    assert sandbox["sandbox_launched"] is False


if __name__ == "__main__":
    tests = sorted((name, value) for name, value in globals().items() if name.startswith("test_") and callable(value))
    failures: list[str] = []
    for name, function in tests:
        try:
            function()
        except Exception as exc:  # pragma: no cover - direct runner failure surface
            failures.append(f"{name}: {type(exc).__name__}: {exc}")
    print(f"{len(tests) - len(failures)}/{len(tests)} v645-v8 x1 scoped tests passed")
    if failures:
        print("\n".join(failures))
        raise SystemExit(1)
