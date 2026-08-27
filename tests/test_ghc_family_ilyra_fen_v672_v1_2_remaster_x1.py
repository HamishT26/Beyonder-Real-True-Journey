from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
X1 = ROOT / "docs" / "ilyra-fen" / "v672-v1-2-remaster" / "x1"
SOURCE = "f67221fbee56905a770c64533771dd9471fb2fba"


def load(name: str):
    return json.loads((X1 / name).read_text(encoding="utf-8"))


def test_x1_is_planning_only_and_source_anchored() -> None:
    truth = load("phase-truth.json")
    assert truth["state"] == "X1_PLANNING_ONLY"
    assert truth["source"] == SOURCE
    assert truth["x2_executed"] is False
    assert truth["packages_installed"] == 0
    assert truth["global_skills_installed"] == 0
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert not (X1.parent / "x2").exists()
    assert not (X1.parent / "closeout").exists()


def test_parenthetical_remaster_does_not_consume_route_seat() -> None:
    intake = load("activation-intake.json")
    assert intake["parenthetical_remaster"] is True
    assert intake["consumes_round_robin_seat"] is False
    assert intake["next_prospective_edge"] == {
        "title": "Auren Lark",
        "phase": "v672-v2",
        "precontacted": False,
    }
    assert intake["solo"] is True
    assert intake["subagents"] == 0
    assert intake["forks"] == 0


def test_inherited_proposal_revalidation_has_zero_credit() -> None:
    inherited = load("inherited-proposal-revalidation.json")
    assert inherited["declared_chain"] == 5910
    assert inherited["selected_count"] == 40
    assert inherited["novelty_credit"] == 0
    assert inherited["completion_credit"] == 0
    assert len(inherited["rows"]) == 40
    assert all(row["current_novelty_credit"] == 0 for row in inherited["rows"])
    assert all(row["current_completion_credit"] == 0 for row in inherited["rows"])


def test_new_proposals_are_distinct_and_complete() -> None:
    freeze = load("new-proposal-freeze.json")
    rows = freeze["rows"]
    assert freeze["proposal_chain_before"] == 5910
    assert freeze["proposal_chain_after_if_evidence_frozen"] == 5950
    assert len(rows) == 40
    assert len({row["title"].casefold() for row in rows}) == 40
    required = {
        "proposal_id", "title", "hypothesis", "null_or_failure",
        "approval_class", "execution_lane",
        "current_official_or_primary_source_needs", "concrete_artifacts",
        "falsifier_or_acceptance_gate", "rollback_or_recovery",
        "protected_gates", "expected_disposition", "x1_state",
        "completion_credit",
    }
    assert all(required <= set(row) for row in rows)
    assert all(row["x1_state"] == "preregistered_only" for row in rows)
    assert all(row["completion_credit"] == 0 for row in rows)
    assert freeze["outcomes"] == {
        "completed": 28,
        "represented": 8,
        "open_gap": 2,
        "exact_gate": 2,
    }
    assert freeze["universal_novelty_claim"] is False


def test_semantic_neighbor_audit_keeps_universal_gap_visible() -> None:
    audit = load("semantic-neighbor-audit.json")
    assert audit["candidate_count"] == 40
    assert audit["exact_predecessor_rows_compared"] == 40
    assert audit["within_slate_duplicates"] == 0
    assert audit["exact_title_collisions"] == 0
    assert audit["declared_inherited_rows_not_locally_compared"] == 5870
    assert audit["universal_novelty_claim"] is False


def test_portfolio_meets_live_floors_without_treating_caps_as_quotas() -> None:
    portfolio = load("portfolio-freeze.json")
    counts = portfolio["counts"]
    assert counts == {
        "safe_now_owner": 60,
        "candidate_owner": 50,
        "candidate_successor": 20,
        "exact_approval": 20,
        "blocked": 10,
        "skills_owner": 20,
        "runners_owner": 10,
        "skills_successor": 10,
        "runners_successor": 10,
        "clean_fix_refine_owner": 60,
        "clean_fix_refine_successor": 30,
        "package_direct_surfaces": 13,
    }
    assert portfolio["caps_are_ceilings_not_quotas"] is True
    assert portfolio["filler_prohibited"] is True
    assert len(portfolio["bounded_practice_lenses"]) == 3
    assert portfolio["successor_practice_recommendation"]


def test_package_allowlist_is_exact_and_d_first() -> None:
    portfolio = load("portfolio-freeze.json")
    packages = portfolio["package_allowlist"]
    assert len(packages) == 13
    assert len({(row["ecosystem"], row["name"].casefold()) for row in packages}) == 13
    assert any(row["name"] == "PyYAML" and row["version"] == "6.0.3" for row in packages)
    assert all(row["version"] and row["integrity"] for row in packages)
    assert all(row["integrity"].startswith(("sha256:", "sha512-")) for row in packages)
    transaction = portfolio["package_transaction"]
    assert transaction["state"] == "planned_only"
    assert transaction["python_environment"].startswith("D:/")
    assert transaction["node_environment"].startswith("D:/")
    assert transaction["system_python_mutation"] is False
    assert transaction["npm_global_prefix_mutation"] is False
    assert transaction["wheel_only"] is True
    assert transaction["hash_required"] is True
    assert transaction["npm_ignore_scripts"] is True


def test_skill_promotions_are_collision_guarded_plans_only() -> None:
    portfolio = load("portfolio-freeze.json")
    assert len(portfolio["global_skill_promotions"]) == 5
    assert len(set(portfolio["global_skill_promotions"])) == 5
    assert portfolio["composite_global_skill"] == "ghc-family-d-first-structured-evidence-toolchain"


def test_exact_and_blocked_packets_remain_unexecuted() -> None:
    rows = load("portfolio-freeze.json")["rows"]
    exact = [row for row in rows if row.get("approval_class") == "exact_approval"]
    blocked = [row for row in rows if row.get("approval_class") == "blocked"]
    assert len(exact) == 20
    assert len(blocked) == 10
    assert all(row["x1_state"] == "visible_unexecuted" for row in exact + blocked)
    assert all(row["completion_credit"] == 0 for row in exact + blocked)


def test_source_seal_and_external_overlay_are_separate() -> None:
    counts = load("source-count-overlay.json")
    source = counts["repository_sealed_source"]
    overlay = counts["activation_overlay"]
    assert source["effective_negatives"] == 35007
    assert source["effective_methods"] == 21553
    assert counts["external_startup_overlay_count"] == 12
    assert overlay["effective_negatives"] == 35019
    assert overlay["effective_methods"] == 21565
    assert overlay["effective_failed_witnesses"] == 6840
    assert overlay["effective_passing_witnesses"] == 8856
    assert overlay["open_gaps"] == 274
    assert counts["source_seal_rewritten"] is False


def test_method_flow_retains_every_startup_failure() -> None:
    method = load("method-flow-startup.json")
    assert len(method["failed_witnesses"]) == 12
    assert all(row["status"] == "failed_retained_zero_credit" for row in method["failed_witnesses"])
    assert "never erases" in method["recovery_rule"]


def test_route_is_prospective_and_single_send_guarded() -> None:
    route = load("route-plan.json")
    assert route["state"] == "PROSPECTIVE_NOT_CONTACTED"
    assert route["target_exact_title"] == "Auren Lark"
    assert route["target_phase"] == "v672-v2"
    assert route["precontacted"] is False
    assert route["substitute_permitted"] is False
    assert route["resend_permitted"] is False
    assert len(route["required_terminal_gates"]) >= 8


def test_identity_and_claim_boundaries_remain_explicit() -> None:
    boundary = load("identity-and-boundary.json")
    assert boundary["relational_language_only"] is True
    assert "consciousness" in boundary["not_evidence_of"]
    assert "Maori authority" in boundary["not_evidence_of"]
    assert "independent-reproduction" in boundary["protected_boundaries"]
    assert boundary["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_threat_model_covers_install_and_route_risks() -> None:
    model = load("threat-model.json")
    threats = set(model["threats"])
    assert {"dependency confusion", "unhashed artifact", "npm lifecycle script", "canonical replay", "route duplicate", "privacy leakage"} <= threats
    assert "non-exhaustive privacy and security review" in model["residual"]


def test_build_receipt_covers_every_pre_receipt_file() -> None:
    receipt = load("build-receipt.json")
    manifest = receipt["manifest"]
    paths = {row["path"] for row in manifest}
    expected = {
        path.relative_to(ROOT).as_posix()
        for path in X1.iterdir()
        if path.is_file() and path.name != "build-receipt.json"
    }
    assert paths == expected
    assert receipt["file_count_before_receipt"] == len(expected)
    assert receipt["x2_mutations"] == 0
    assert receipt["source_mutations"] == 0


def test_overview_is_substantive_but_below_document_ceiling() -> None:
    words = (X1 / "integrated-overview.md").read_text(encoding="utf-8").split()
    assert len(words) >= 700
    assert len(words) <= 6000
