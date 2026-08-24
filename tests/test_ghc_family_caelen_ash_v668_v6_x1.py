from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_caelen_ash_v668_v6_archive as archive


PHASE_ROOT = ROOT / "docs" / "caelen-ash" / "v668-v6"


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def all_json_paths() -> list[Path]:
    return sorted(PHASE_ROOT.rglob("*.json"))


def proposal_rows() -> list[dict]:
    index = load("x1/proposal-freeze.json")
    rows: list[dict] = []
    for shard in index["proposal_shards"]:
        relative = Path(shard["path"]).relative_to("docs/caelen-ash/v668-v6").as_posix()
        rows.extend(load(relative)["new_proposals"])
    return rows


def portfolio_rows(category: str) -> list[dict]:
    index = load("x1/portfolio-freeze.json")
    rows: list[dict] = []
    for shard in index["category_shards"][category]:
        relative = Path(shard["path"]).relative_to("docs/caelen-ash/v668-v6").as_posix()
        rows.extend(load(relative)["rows"])
    return rows


def method_flow_rows() -> tuple[dict, dict[str, list[dict]]]:
    index = load("method-flow/x1-ledger.json")
    rows: dict[str, list[dict]] = {
        "methods": [],
        "witnesses": [],
        "state_events": [],
        "recommendations": [],
    }
    for shard in index["logical_shards"]:
        relative = Path(shard["path"]).relative_to("docs/caelen-ash/v668-v6").as_posix()
        document = load(relative)
        for key in rows:
            rows[key].extend(document[key])
    return index, rows


def test_source_anchors_are_exact() -> None:
    source = load("x1/source-intake.json")
    assert source["source_final"] == archive.SOURCE_FINAL
    assert source["source_x1"] == archive.SOURCE_X1
    assert source["source_evidence"] == archive.SOURCE_EVIDENCE
    assert source["source_to_final_commits"] == 3
    assert source["source_to_final_merges"] == 0
    assert source["source_lane_mutated"] is False


def test_x1_is_planning_only() -> None:
    truth = load("x1/phase-truth.json")
    assert truth["lifecycle"] == "x1_planning_only"
    assert truth["x2_implementation_count"] == 0
    assert truth["x2_outcome_claim_count"] == 0
    assert truth["observed_outcome_counts"] is None
    for name in ("x2", "evidence", "final", "closeout", "seal"):
        assert not (PHASE_ROOT / name).exists()


def test_exactly_forty_new_proposals() -> None:
    freeze = load("x1/proposal-freeze.json")
    assert freeze["inherited_frozen_proposals"] == 4790
    assert freeze["new_proposal_count"] == 40
    assert freeze["new_frozen_total"] == 4830
    assert freeze["proposal_shard_count"] == 8
    assert len(proposal_rows()) == 40


def test_expected_outcome_vocabulary_and_counts() -> None:
    freeze = load("x1/proposal-freeze.json")
    assert freeze["allowed_outcomes"] == ["completed", "represented", "open_gap", "exact_gate"]
    assert freeze["expected_outcomes"] == {"completed": 28, "exact_gate": 2, "open_gap": 2, "represented": 8}
    assert {row["expected_disposition"] for row in proposal_rows()} == set(freeze["allowed_outcomes"])


def test_proposal_contract_fields_are_complete() -> None:
    freeze = load("x1/proposal-freeze.json")
    required = {
        "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class",
        "execution_lane", "official_or_primary_source_needs", "concrete_artifacts",
        "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
        "expected_disposition", "negative_fixtures", "semantic_neighbors",
    }
    for row in proposal_rows():
        assert required <= row.keys()
        assert all(row[key] for key in required - {"semantic_neighbors"})
        assert row["x1_planning_only"] is True
        assert row["x2_execution_count"] == 0


def test_novelty_collisions_and_quarantine_are_zero() -> None:
    freeze = load("x1/proposal-freeze.json")
    assert freeze["visible_title_collision_count"] == 0
    assert freeze["semantic_neighbor_quarantine_count"] == 0
    assert all(not row["visible_title_collision"] for row in proposal_rows())
    assert all(not row["semantic_neighbor_quarantined"] for row in proposal_rows())


def test_compressed_title_gap_is_not_hidden() -> None:
    audit = load("x1/proposal-chain-audit.json")
    assert audit["declared_inherited_chain_count"] == 4790
    assert audit["compressed_title_gap_count_minimum"] > 0
    assert "OPEN_GAP" in audit["coverage_state"]
    assert audit["selected_novelty_credit"] == 0
    assert audit["selected_completion_credit"] == 0


def test_exactly_160_mutations_are_preregistered_only() -> None:
    freeze = load("x1/proposal-freeze.json")
    mutations = [item for row in proposal_rows() for item in row["negative_fixtures"]]
    assert len(mutations) == freeze["negative_mutation_count"] == 160
    assert len({row["mutation_id"] for row in mutations}) == 160
    assert {row["state"] for row in mutations} == {"preregistered_not_executed"}
    assert {row["credit"] for row in mutations} == {0}


def test_portfolio_floors_and_zero_credit() -> None:
    portfolio = load("x1/portfolio-freeze.json")
    expected = {"safe_now": 60, "candidates": 30, "skills": 20, "runners": 10, "clean_fix_refine": 60, "exact_approval": 20, "blocked": 10}
    assert portfolio["category_counts"] == expected
    for key in expected:
        rows = portfolio_rows(key)
        assert len(rows) == expected[key]
        assert all(row["completion_credit"] == 0 for row in rows)
        assert all(row["x1_planning_only"] is True for row in rows)


def test_exact_and_blocked_work_remains_unexecuted() -> None:
    portfolio = load("x1/portfolio-freeze.json")
    assert {row["state"] for row in portfolio_rows("exact_approval")} == {"exact_approval_unexecuted"}
    assert {row["state"] for row in portfolio_rows("blocked")} == {"blocked_unexecuted"}


def test_successor_recommendations_are_zero_credit_and_unexecuted() -> None:
    recommendations = load("x1/successor-recommendations-freeze.json")
    expected = {"candidates": 15, "skills": 10, "runners": 10, "clean_fix_refine": 30}
    assert recommendations["recipient"] == "unresolved_until_terminal_gate"
    assert recommendations["contacted"] is False
    assert recommendations["completion_credit"] == 0
    assert recommendations["execution_count"] == 0
    for key, count in expected.items():
        assert len(recommendations[key]) == count
        assert all(row["completion_credit"] == 0 for row in recommendations[key])
        assert all(row["x2_execution_count"] == 0 for row in recommendations[key])
    assert recommendations["practice"]["count"] == 1
    assert recommendations["practice"]["completion_credit"] == 0


def test_family_current_compatibility_names() -> None:
    inventory = load("x1/compatibility-inventory.json")
    assert len(inventory["planned_skills"]) == 20
    assert len(inventory["planned_runners"]) == 10
    assert all(name.startswith("ghc-family-") for name in inventory["planned_skills"])
    assert all(name.startswith("ghc_family_") for name in inventory["planned_runners"])
    assert inventory["historical_callers_deleted_or_renamed"] == 0
    assert inventory["global_installs_in_x1"] == 0


def test_method_flow_schema_and_counts() -> None:
    index, ledger = method_flow_rows()
    assert index["schema"] == "ghc.family.method-flow-state.v1"
    assert index["execution_authority"] == "owner_self_scoped_delta"
    assert index["logical_shard_count"] == 4
    assert len(ledger["methods"]) == 18
    assert len(ledger["witnesses"]) == 36
    assert index["counts"] == {"failed_witnesses": 18, "methods": 18, "passing_witnesses": 18, "retained_negatives": 18}
    assert all(method["recommendation_state"] == "preferred" for method in ledger["methods"])
    assert all(method["retained_negative_ids"] for method in ledger["methods"])


def test_method_flow_never_erases_failures() -> None:
    summary = load("method-flow/x1-summary.json")
    _, ledger = method_flow_rows()
    assert summary["failure_count"] == 18
    assert summary["all_failures_retained"] is True
    assert summary["correction_erases_failure"] is False
    assert sum(w["result"] == "fail" for w in ledger["witnesses"]) == 18
    assert all(w["independent_reproduction"] is False for w in ledger["witnesses"])


def test_overlay_arithmetic_is_additive() -> None:
    truth = load("x1/phase-truth.json")
    source = truth["activation_overlay"]
    x1 = truth["x1_overlay"]
    for key in ("effective_negatives", "methods", "failed_witnesses", "passing_witnesses"):
        assert x1[key] == source[key] + 18
    assert x1["open_gaps"] == source["open_gaps"]
    assert x1["exact_gates"] == source["exact_gates"]


def test_source_ledger_is_official_and_zero_download() -> None:
    ledger = load("x1/source-ledger.json")
    assert ledger["downloads"] == 0
    assert ledger["empirical_credit"] == 0
    assert len(ledger["sources"]) >= 6
    assert all(row["url"].startswith("https://") for row in ledger["sources"])
    assert all(row["credit_boundary"] for row in ledger["sources"])


def test_identity_and_authority_boundaries_are_explicit() -> None:
    wellbeing = load("x1/wellbeing-and-corrigibility.json")
    truth = load("x1/phase-truth.json")
    assert "not evidence of consciousness" in wellbeing["identity_boundary"]
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert set(truth["protected_gates"]) == set(archive.PROTECTED_GATES)
    assert truth["primary_pillar"] == "THOS Body"


def test_workflow_plan_preserves_terminal_route_hold() -> None:
    plan = load("x1/workflow-plan.json")
    route = load("x1/route-plan.json")
    assert plan["stale_plan_rejected"] is True
    assert route["successor_contacted"] is False
    assert route["successor_inferred_from_history"] is False
    assert route["terminal_gate_required"] is True
    assert route["maximum_sends"] == 1


def test_phase_document_word_caps_and_overview_floor() -> None:
    documents = sorted(path for path in PHASE_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".json", ".txt", ".html"})
    assert documents
    counts = {path.relative_to(PHASE_ROOT).as_posix(): archive.word_count(path) for path in documents}
    assert all(count <= 6000 for count in counts.values())
    assert counts["x1/integrated-overview.md"] >= 1200


def test_all_phase_json_parses() -> None:
    paths = all_json_paths()
    assert len(paths) >= 15
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_x1_manifest_matches_git_blob_domain() -> None:
    manifest = load("x1/x1-manifest.json")
    paths = [ROOT / row["path"] for row in manifest["entries"]]
    replay = {row["path"]: row for row in archive.manifest_rows(paths)}
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        assert replay[row["path"]]["git_blob_oid"] == row["git_blob_oid"]
        assert replay[row["path"]]["sha256"] == row["sha256"]
        assert replay[row["path"]]["bytes"] == row["bytes"]
    assert manifest["self_exclusions"] == ["docs/caelen-ash/v668-v6/x1/x1-manifest.json"]
    allowlist = load("validation/x1-staged-allowlist.json")
    assert "docs/caelen-ash/v668-v6/validation/x1-staged-allowlist.json" in allowlist["intended_paths_before_manifest"]


def test_public_artifacts_exclude_private_identifier_shapes() -> None:
    forbidden = [
        re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        re.compile(r"(?:C|D):\\Users\\", re.I),
        re.compile(r"(?:thread|task|session|callable)[_-]?id\s*[:=]", re.I),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ]
    for path in sorted(PHASE_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt", ".html"}:
            continue
        text = path.read_text(encoding="utf-8")
        assert not any(pattern.search(text) for pattern in forbidden), path


def test_materialized_owner_surface_below_file_ceiling() -> None:
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    assert len(files) < 2000
