from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
BASE = REPO / "docs" / "caelen-ash" / "v676-v2"
X1 = BASE / "x1"
SOURCE = "939312172819669aad250cf034d8a6a7efe3df5b"
BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(name: str):
    with (X1 / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO), *args], text=True).strip()


def test_x1_runs_on_exact_source_and_owner_branch() -> None:
    assert git("branch", "--show-current") == BRANCH
    assert git("rev-parse", "HEAD") == SOURCE


def test_source_verification_preserves_exact_anchors() -> None:
    data = load("source-verification.json")
    assert data["source"] == SOURCE
    assert data["anchors"]["sable_x1"] == "18c4e98ead5d81875c1ffaf7cb2238c34d9b5407"
    assert data["anchors"]["sable_evidence"] == "bb04bce8a0f4b3f6d50d839b1ee237da817e369f"
    assert data["anchors"]["sable_first_closeout"] == "e75ca31a34c8569eee5b603fec2ab96a4ac1f77e"
    assert data["phase_commits"] == 4
    assert data["merges"] == 0
    assert data["local_upstream_tracking_fresh_live_equal"] is True
    assert data["inherited_canonical_replayed"] is False


def test_new_proposal_freeze_has_exact_floor_and_chain() -> None:
    data = load("new-proposal-freeze.json")
    assert data["status"] == "FROZEN_PLANNING_ONLY"
    assert data["declared_chain_before"] == 7430
    assert data["new_caelen_proposals"] == 40
    assert data["declared_chain_after"] == 7470
    assert len(data["proposals"]) == 40


def test_proposal_ids_titles_and_required_contract_fields_are_unique() -> None:
    rows = load("new-proposal-freeze.json")["proposals"]
    fields = {
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
    assert len({row["proposal_id"] for row in rows}) == 40
    assert len({row["title"].casefold() for row in rows}) == 40
    assert all(fields <= row.keys() for row in rows)
    assert [row["proposal_id"] for row in rows] == [f"CA6762-N{i:03d}" for i in range(1, 41)]


def test_expected_dispositions_use_only_four_labels_and_exact_counts() -> None:
    rows = load("new-proposal-freeze.json")["proposals"]
    counts = Counter(row["expected_disposition"] for row in rows)
    assert set(counts) == LABELS
    assert counts == Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
    assert all(isinstance(row["expected_disposition"], str) for row in rows)


def test_protected_gates_are_present_on_every_proposal() -> None:
    rows = load("new-proposal-freeze.json")["proposals"]
    for row in rows:
        joined = " ".join(row["protected_gates"])
        assert "no empirical GMUT" in joined
        assert "no THOS operational-effectiveness" in joined
        assert "no production Freed ID" in joined
        assert "Maori-authority" in joined
        assert "Stage 20" in joined


def test_reachable_semantic_audit_is_explicitly_bounded() -> None:
    data = load("semantic-neighbor-audit.json")
    assert data["source_tree"] == SOURCE
    assert data["declared_chain_count"] == 7430
    assert data["reachable_proposal_json_blobs"] == 2607
    assert data["reachable_unique_id_title_records"] == 3383
    assert data["json_parse_failures"] == 0
    assert data["maximum_selected_score"] < data["quarantine_threshold"]
    assert data["selected_rows_quarantined"] == 0
    assert len(data["neighbors"]) == 40
    assert "not a universal novelty proof" in data["limitation"]


def test_inherited_reviews_have_zero_novelty_and_completion_credit() -> None:
    data = load("inherited-zero-credit-review.json")
    assert data["count"] == 20
    assert data["novelty_credit"] == 0
    assert data["completion_credit"] == 0
    assert len(data["reviews"]) == 20
    assert all(row["status"] == "reviewed_inherited_zero_credit" for row in data["reviews"])


def test_mutation_plan_has_four_unexecuted_rejections_per_proposal() -> None:
    data = load("mutation-preregistration.json")
    assert data["proposal_count"] == 40
    assert data["mutations_per_proposal"] == 4
    assert data["mutation_count"] == 160
    assert len(data["mutations"]) == 160
    counts = Counter(row["proposal_id"] for row in data["mutations"])
    assert set(counts.values()) == {4}
    assert all(row["execution_status"] == "preregistered_unexecuted_x1" for row in data["mutations"])


def test_portfolio_floors_are_planned_and_unexecuted() -> None:
    data = load("portfolio-freeze.json")
    assert len(data["safe_now"]) == 60
    assert len(data["candidate"]) == 30
    assert len(data["exact_approval"]) == 20
    assert len(data["blocked"]) == 10
    assert all(row["status"] == "planned_unexecuted_x1" for row in data["safe_now"])
    assert all(row["status"] == "planned_unexecuted_x1" for row in data["candidate"])
    assert all(row["status"] == "unexecuted_exact_gate" for row in data["exact_approval"])
    assert all(row["status"] == "blocked_unexecuted" for row in data["blocked"])


def test_skill_and_runner_floor_is_phase_local_and_family_current() -> None:
    data = load("skill-runner-plan.json")
    assert len(data["phase_local_skills"]) == 20
    assert len(data["family_current_runners"]) == 10
    assert len(data["successor_skill_recommendations"]) == 10
    assert len(data["successor_runner_recommendations"]) == 10
    assert all(row["global_install"] is False for row in data["phase_local_skills"])
    names = [row["name"] for row in data["family_current_runners"]]
    assert all(name.startswith(("ghc_family_", "build_ghc_family_")) for name in names)


def test_clean_fix_refine_floor_is_planned_without_successor_credit() -> None:
    data = load("clean-fix-refine-plan.json")
    assert len(data["owner_tasks"]) == 60
    assert len(data["successor_recommendations"]) == 30
    assert all(row["status"] == "planned_unexecuted_x1" for row in data["owner_tasks"])
    assert all(row["credit"] == "zero_caelen_completion_credit" for row in data["successor_recommendations"])


def test_method_flow_retains_every_new_failure_and_bounded_recovery() -> None:
    data = load("method-flow-startup.json")
    failed = [row for row in data["methods"] if row["truth"] is False]
    passed = [row for row in data["methods"] if row["truth"] is True]
    assert len(failed) == 8
    assert len(passed) == 5
    assert data["new_effective_methods"] == 13
    assert data["current_overlay"]["effective_negatives"] == 41670
    assert data["current_overlay"]["retained_failed_witnesses"] == 13331
    assert data["failure_erasure_forbidden"] is True
    pass_ids = {row["method_id"] for row in passed}
    assert all(row["recovered_by"] in pass_ids for row in failed)


def test_source_ledger_uses_official_primary_sources_as_vocabulary_only() -> None:
    data = load("official-source-ledger.json")
    assert len(data["sources"]) == 7
    assert all(row["url"].startswith("https://") for row in data["sources"])
    assert "not observations" in data["source_boundary"]
    assert {row["source_id"] for row in data["sources"]} == {
        "IASA-TC04", "FADGI-AUDIO", "EBU-TECH-3285-V2", "PREMIS-3", "W3C-PROV-O", "WCAG-2.2", "RFC-8785"
    }


def test_primary_pillar_and_three_synthetic_lenses_are_bounded() -> None:
    data = load("primary-pillar-and-lenses.json")
    assert data["primary_pillar"] == "GMUT Mind"
    assert len(data["bounded_wholly_synthetic_learning_lenses"]) == 3
    assert data["real_world_rows_or_actions"] == 0
    assert set(data["secondary_pillars"]) == {"THOS Body", "Freed ID and CBR Heart"}


def test_x1_phase_truth_has_no_executed_outcome_or_x2_claim() -> None:
    data = load("phase-truth.json")
    assert data["status"] == "FROZEN_PLANNING_ONLY"
    assert data["executed_core_outcomes"] == {label: 0 for label in sorted(LABELS)}
    assert data["x2_implementation_present"] is False
    assert data["x2_outcomes_claimed"] is False
    assert data["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_no_x2_directory_or_x2_builder_exists_at_x1() -> None:
    assert not (BASE / "x2").exists()
    assert not list((REPO / "scripts").glob("*caelen_ash_v676_v2_x2*"))
    assert not list((REPO / "tests").glob("*caelen_ash_v676_v2_x2*"))


def test_route_is_held_and_no_successor_is_inferred_or_contacted() -> None:
    data = load("route-hold.json")
    assert data["route_state"] == "HOLD_UNTIL_CAELEN_EXACT_FINAL"
    assert data["successor_inferred"] is False
    assert data["precontact_performed"] is False
    assert data["send_count"] == 0


def test_identity_document_preserves_relational_and_authority_boundaries() -> None:
    value = (X1 / "identity-and-boundary.md").read_text(encoding="utf-8")
    for phrase in ["relational working language only", "not evidence of consciousness", "Māori authority", "Hamish may rename"]:
        assert phrase in value


def test_x1_packet_has_no_private_absolute_path_raw_thread_id_or_secret_marker() -> None:
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


def test_all_x1_json_parses_and_documents_remain_below_word_cap() -> None:
    json_paths = list(X1.glob("*.json"))
    assert len(json_paths) >= 12
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    for path in BASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".html"}:
            assert len(path.read_text(encoding="utf-8").split()) <= 100_000
