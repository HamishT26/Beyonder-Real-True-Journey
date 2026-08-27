from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "vesper-arlen" / "v673-v6"
SOURCE_FINAL = "2400427269b28496acaa07cd6c18f5a2236510f7"
BATON_SHA256 = "530f37686d3decf000331a996a1dc0f3d1aaf6eb327434b1e4f37b9330b22dbc"
ALLOWED_EXPECTED = {"completed", "represented", "open_gap", "exact_gate"}


def load(relative: str):
    return json.loads((OUT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    assert result.returncode == 0, result.stderr.decode("utf-8", "replace")
    return result.stdout


def test_source_and_baton_are_exact() -> None:
    source = load("x1/source-and-provenance.json")
    assert source["source_final"] == SOURCE_FINAL
    assert source["activation_baton_sha256"] == BATON_SHA256
    assert source["activation_baton_words"] == 24125
    blob = git("show", f"{SOURCE_FINAL}:{source['activation_baton']}")
    assert hashlib.sha256(blob).hexdigest() == BATON_SHA256
    assert source["source_canonical_replayed"] is False


def test_x1_is_planning_only() -> None:
    receipt = load("x1/build-receipt.json")
    assert receipt["state"] == "PLANNING_ONLY_X1_BUILT"
    assert receipt["outcomes_observed"] is False
    assert receipt["x2_files_created"] == 0
    x1_tree = git("ls-tree", "-r", "--name-only", "9a5d432a877d5c11ac60e0d331cf27cfb55c482b").decode("utf-8")
    assert "docs/vesper-arlen/v673-v6/x2/" not in x1_tree


def test_forty_proposals_have_complete_preregistration_fields() -> None:
    document = load("x1/proposals.json")
    rows = document["proposals"]
    assert document["proposal_count"] == len(rows) == 40
    required = {
        "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class",
        "execution_lane", "current_official_or_primary_source_need", "concrete_artifacts",
        "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
        "expected_disposition", "outcome_observed", "vesper_novelty_credit",
        "inherited_completion_credit", "primary_pillar", "protected_pillars", "bounded_practice",
    }
    assert all(required <= set(row) for row in rows)
    assert all(row["outcome_observed"] is False for row in rows)
    assert all(row["expected_disposition"] in ALLOWED_EXPECTED for row in rows)
    assert all(row["vesper_novelty_credit"] == 1 and row["inherited_completion_credit"] == 0 for row in rows)
    assert len({row["proposal_id"] for row in rows}) == 40
    assert len({row["title"].casefold() for row in rows}) == 40


def test_expected_disposition_distribution_is_exact() -> None:
    rows = load("x1/proposals.json")["proposals"]
    assert Counter(row["expected_disposition"] for row in rows) == {
        "completed": 28,
        "represented": 8,
        "open_gap": 2,
        "exact_gate": 2,
    }


def test_inherited_rows_are_zero_credit() -> None:
    document = load("x1/inherited-revalidations.json")
    assert len(document["rows"]) == 20
    assert document["novelty_credit"] == document["automatic_completion_credit"] == 0
    assert all(row["vesper_novelty_credit"] == 0 for row in document["rows"])
    assert all(row["automatic_completion_credit"] == 0 for row in document["rows"])
    assert all(row["source_final"] == SOURCE_FINAL for row in document["rows"])


def test_semantic_neighbor_audit_is_source_bounded_and_collision_free() -> None:
    audit = load("x1/semantic-neighbor-audit.json")
    assert audit["collisions"] == 0
    assert len(audit["rows"]) == 40
    corpus = audit["exact_source_tree_corpus"]
    assert corpus["candidate_git_blob_paths"] > 0
    assert corpus["unique_titles"] > 0
    assert corpus["universal_novelty_claim"] is False
    assert corpus["canonical_row_mapping_open_gap"] is True
    assert corpus["exact_canonical_row_mapping"] is False


def test_portfolio_floors_are_exact_and_non_authorizing() -> None:
    document = load("x1/portfolio-freeze.json")
    expected = {
        "safe_now": 60, "candidate": 30, "exact_approval": 20, "blocked": 10,
        "owner_skills": 20, "owner_runners": 10, "successor_skills": 10,
        "successor_runners": 10, "owner_clean_fix_refine": 60,
        "successor_clean_fix_refine": 30, "practice_lenses": 3,
        "successor_practice_recommendations": 1,
    }
    assert document["counts"] == expected
    for key in ("safe_now", "candidate", "exact_approval", "blocked", "owner_skills", "owner_runners", "successor_skills", "successor_runners", "owner_clean_fix_refine", "successor_clean_fix_refine"):
        assert len(document[key]) == expected[key]
    assert len(document["practice_lenses"]) == 3
    assert document["successor_practice_recommendation"]["count"] == 1
    assert all(row["state"] == "exact_approval_unexecuted" for row in document["exact_approval"])
    assert all(row["state"] == "blocked_unexecuted" for row in document["blocked"])


def test_three_tool_candidates_are_plans_not_installations() -> None:
    toolchain = load("x1/selected-toolchain-plan.json")
    assert toolchain["installation_performed_in_x1"] is False
    assert len(toolchain["candidates"]) == 3
    assert {row["name"] for row in toolchain["candidates"]} == {"rfc8785", "jsonpath-ng", "treelib"}
    assert all(row["state"].startswith("candidate_pending") for row in toolchain["candidates"])


def test_method_flow_retains_every_startup_failure_and_passing_guard() -> None:
    flow = load("x1/method-flow-startup.json")
    assert flow["method_count"] == flow["failed_witness_count"] == flow["bounded_passing_witness_count"] == 10
    assert all(row["status"] == "preferred" for row in flow["methods"])
    assert all(row["completion_credit"] == 0 for row in flow["methods"])
    assert all(row["failure_signature"] and row["passing_witness"] and row["recurrence_guard"] and row["rollback"] for row in flow["methods"])


def test_flashcards_have_four_tiers_and_ten_categories() -> None:
    plan = load("x1/flashcard-plan.json")
    assert [row["tier"] for row in plan["tiers"]] == [1, 2, 3, 4]
    assert plan["minimum_categories"] >= 10
    assert plan["outcomes_observed"] is False


def test_route_is_prepared_not_sent() -> None:
    route = load("x1/route-plan.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["activation_target"] is None
    assert route["precontact_performed"] is False
    assert route["prospective_terminal_edge"] == {"exact_title": "Lyren Moss", "phase": "v673-v7"}


def test_official_sources_are_bounded() -> None:
    document = load("x1/official-source-plan.json")
    assert document["network_execution_in_x1"] is False
    assert len(document["sources"]) >= 6
    assert all(row["url"].startswith("https://") for row in document["sources"])
    assert "no observation" in document["boundary"].casefold()


def test_open_gates_are_not_closed_in_x1() -> None:
    gates = load("x1/open-gate-plan.json")
    assert gates["inherited_repository_sealed"] == {"open_gaps": 301, "exact_gates": 294}
    assert gates["planned_new"] == {"open_gaps": 2, "exact_gates": 2}
    assert gates["closure_claimed_in_x1"] is False


def test_index_reference_is_current_and_bounded() -> None:
    text = (ROOT / "ghc-family-index" / "references" / "v673-v6-vesper-arlen.md").read_text(encoding="utf-8")
    assert "planning only" in text
    assert SOURCE_FINAL in text
    assert "PREPARED_NOT_SENT" in text
    assert "NOT_READY_FOR_STAGE_20" in text


def test_all_phase_json_parses() -> None:
    paths = sorted(OUT.rglob("*.json"))
    assert len(paths) >= 15
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_staged_receipts_when_finalized() -> None:
    manifest = load("validation/x1-manifest.json")
    if manifest.get("state") == "PENDING_STAGED_FINALIZATION":
        return
    review = load("validation/x1-staged-review.json")
    privacy = load("validation/x1-staged-privacy.json")
    assert review["state"] == "VALID_X1_EXACT_STAGED_SCOPE"
    assert review["out_of_scope_paths"] == []
    assert review["x2_paths"] == []
    assert review["outcome_paths"] == []
    assert privacy["state"] == "VALID_ZERO_CONFIRMED_PRIVACY_HITS"
    assert privacy["confirmed_hit_count"] == 0
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        blob = git("show", f"9a5d432a877d5c11ac60e0d331cf27cfb55c482b:{row['path']}")
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest() == row["sha256_normalized_lf"]


def test_no_private_absolute_paths_or_task_ids_in_public_artifacts() -> None:
    for path in list(OUT.rglob("*.json")) + list(OUT.rglob("*.md")) + [ROOT / "ghc-family-index" / "references" / "v673-v6-vesper-arlen.md"]:
        text = path.read_text(encoding="utf-8")
        assert "source_" + "thread_id" not in text
        assert "C:" + "\\Users\\" not in text
        assert "private_" + "transcript" not in text


def test_owner_materialized_scope_is_below_ceiling() -> None:
    owner_files = [path for path in OUT.rglob("*") if path.is_file()]
    assert 0 < len(owner_files) < 2000
