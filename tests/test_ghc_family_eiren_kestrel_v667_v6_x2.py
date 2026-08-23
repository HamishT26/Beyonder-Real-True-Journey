from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "eiren-kestrel" / "v667-v6"
BUILDER_PATH = ROOT / "scripts" / "build_ghc_family_eiren_kestrel_v667_v6_x2.py"
X1_HEAD = "38aa1b783fd016134b46607894d16e56e5ccac99"


def load_builder():
    spec = importlib.util.spec_from_file_location("eiren_v667_v6_x2", BUILDER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git_text(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    ).stdout


def test_builder_self_validation_passes() -> None:
    receipt = load_builder().validate_tree()
    assert receipt["status"] == "PASS"
    assert receipt["proposal_contracts"] == 20
    assert receipt["rejecting_mutations"] == 100
    assert receipt["revalidations"] == 20
    assert receipt["tools"] == 3
    assert receipt["skills"] == receipt["runners"] == 10
    assert receipt["flashcards"] == 235


def test_outcomes_use_only_the_four_core_labels() -> None:
    outcomes = load("x2/proposal-outcomes.json")
    assert outcomes["counts"] == {
        "completed": 14,
        "exact_gate": 1,
        "open_gap": 1,
        "represented": 4,
    }
    assert set(outcomes["allowed_core_outcomes"]) == {
        "completed", "represented", "open_gap", "exact_gate"
    }
    assert Counter(row["outcome"] for row in outcomes["outcomes"]) == Counter(outcomes["counts"])
    assert outcomes["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_all_twenty_positive_contracts_pass_and_all_mutations_reject() -> None:
    builder = load_builder()
    proposal_dirs = sorted((PHASE_ROOT / "x2" / "proposals").iterdir())
    assert len(proposal_dirs) == 20
    for directory in proposal_dirs:
        contract = json.loads((directory / "contract.json").read_text(encoding="utf-8"))
        mutations = json.loads((directory / "mutation-results.json").read_text(encoding="utf-8"))
        receipt = json.loads((directory / "bounded-receipt.json").read_text(encoding="utf-8"))
        assert builder.contract_error(contract["positive_fixture"]) is None
        assert mutations["mutation_count"] == 5
        assert mutations["accepted_mutation_count"] == 0
        assert all(row["rejected"] and not row["accepted"] for row in mutations["mutations"])
        assert receipt["positive_contract_valid"] is True
        assert receipt["protected_gates_crossed"] == []


def test_selected_inherited_rows_are_read_only_zero_credit_revalidations() -> None:
    summary = load("x2/selected-revalidation-summary.json")
    assert summary["count"] == summary["passed"] == 20
    assert summary["failed"] == 0
    assert summary["eiren_novelty_credit"] == 0
    assert summary["eiren_completion_credit"] == 0
    for row in summary["rows"]:
        assert row["bounded_integrity_revalidation_passed"] is True
        assert row["eiren_novelty_credit"] == 0
        assert row["eiren_completion_credit"] == 0
        assert row["automatic_completion_credit"] == 0


def test_three_tool_transaction_retains_failed_audit_and_one_correction() -> None:
    receipt = load("x2/tooling/three-tool-transaction-receipt.json")
    assert receipt["top_level_program_count"] == 3
    assert {row["name"] for row in receipt["top_level_programs"]} == {
        "check-jsonschema", "nox", "reuse"
    }
    assert all(row["verified"] and len(row["sha256"]) == 64 for row in receipt["artifact_rows"])
    assert receipt["first_post_install_audit"] == {
        "advisory_records": 7,
        "credit": 0,
        "exit": 1,
        "finding_package": "pip",
        "finding_version": "25.0.1",
    }
    assert receipt["installer_remediation"]["to"] == "pip 26.2.1"
    assert receipt["installer_remediation"]["promotion_as_fourth_tool"] is False
    assert receipt["final_post_install_audit"]["invocation_count_after_correction"] == 1
    assert receipt["final_post_install_audit"]["known_vulnerabilities"] == 0
    assert receipt["final_post_install_audit"]["replayed"] is False
    assert receipt["system_or_global_python_changed"] is False
    assert receipt["codex_desktop_updated"] is False


def test_phase_local_skills_and_family_current_runners_are_bounded() -> None:
    skills = load("x2/skills-summary.json")
    runners = load("x2/runners-summary.json")
    assert (skills["planned"], skills["built"], skills["validated"], skills["bounded_smoke_used"]) == (10, 10, 10, 10)
    assert skills["globally_installed"] == 0
    assert (runners["planned"], runners["built"], runners["syntax_validated"], runners["bounded_smoke_used"]) == (10, 10, 10, 10)
    assert runners["globally_installed"] == 0
    receipts = sorted((PHASE_ROOT / "x2" / "runner-smoke").glob("*.json"))
    assert len(receipts) == 10
    for path in receipts:
        receipt = json.loads(path.read_text(encoding="utf-8"))
        assert receipt["status"] == "completed"
        assert receipt["invocation_count"] == 1
        assert receipt["replayed"] is False
        assert receipt["external_writes"] == receipt["real_world_actions"] == 0


def test_owner_portfolio_executes_95_rows_and_keeps_protected_work_closed() -> None:
    portfolio = load("x2/portfolio-execution.json")
    assert portfolio["executed_owner_row_count"] == 95
    assert sum(len(rows) for rows in portfolio["results"].values()) == 95
    assert set(portfolio["outcome_counts"]) <= {"completed", "represented", "open_gap", "exact_gate"}
    assert portfolio["successor_recommendation_count"] == 85
    assert portfolio["successor_recommendations_executed"] == 0
    assert portfolio["exact_approval_count"] == 10
    assert portfolio["exact_approval_executed"] == 0
    assert portfolio["blocked_count"] == 5
    assert portfolio["blocked_executed"] == 0


def test_method_flow_and_retained_counts_reconcile() -> None:
    methods = load("method-flow/x2-method-flow-ledger.json")
    negatives = load("evidence/retained-negative-register.json")
    witnesses = load("evidence/witness-summary.json")
    gates = load("evidence/exact-open-gate-register.json")
    assert methods["phase_method_additions"] == len(methods["methods"]) == 178
    assert methods["provisional_effective_methods"] == 13922
    assert negatives["operational_failure_count"] == 20
    assert negatives["rejecting_mutation_count"] == 100
    assert negatives["phase_negative_additions"] == 120
    assert negatives["provisional_effective_negatives"] == 28032
    assert witnesses["phase_failed_witnesses"] == 120
    assert witnesses["phase_passing_witnesses"] == 158
    assert witnesses["provisional_failed_witnesses"] == 316
    assert witnesses["provisional_passing_witnesses"] == 494
    assert gates["provisional_open_gaps"] == 197
    assert gates["provisional_exact_gates"] == 195
    assert gates["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_freed_id_deck_has_235_bounded_memory_cards() -> None:
    deck = load("deck/deck-index.json")
    assert deck["card_count"] == 235
    assert deck["tier_counts"] == {"tier1": 40, "tier2": 80, "tier3": 80, "tier4": 35}
    assert deck["section_count"] == 15
    assert deck["credential_or_authority_credit"] == 0
    assert len(deck["card_paths"]) == 235
    for path in deck["card_paths"]:
        card = json.loads((ROOT / path).read_text(encoding="utf-8"))
        assert card["status"] == "represented"
        assert card["scope_boundary"]
        assert card["blocked_or_failed_witness_ids"]
        assert card["passing_witness_ids"]


def test_accessible_report_keeps_manual_and_affected_user_review_reserved() -> None:
    reservation = load("report/accessibility-reservation.json")
    assert reservation["automated_structure_present"] is True
    assert reservation["noncolour_states"] is True
    for key in (
        "manual_browser_evaluation", "keyboard_evaluation", "screen_reader_evaluation",
        "magnification_evaluation", "voice_control_evaluation",
        "cognitive_accessibility_evaluation", "print_evaluation", "affected_user_evaluation",
    ):
        assert reservation[key] == "reserved"
    assert reservation["Māori_language_evaluation"] == "reserved_under_Māori_authority"
    assert reservation["accessibility_complete"] is False
    html = (PHASE_ROOT / "report" / "x2-accessible-report.html").read_text(encoding="utf-8")
    assert "<main id=\"main\">" in html
    assert "<caption>" in html
    assert "scope=\"col\"" in html and "scope=\"row\"" in html


def test_x2_content_manifest_replays_exact_bytes() -> None:
    manifest = load("validation/x2-content-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    assert manifest["entry_count"] >= 300
    for row in manifest["entries"]:
        data = (ROOT / row["path"]).read_bytes()
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"]


def test_immutable_x1_commit_contains_no_x2_or_later_lifecycle_paths() -> None:
    paths = [line for line in git_text("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", X1_HEAD).splitlines() if line]
    owner_paths = [path for path in paths if path.startswith("docs/eiren-kestrel/v667-v6/")]
    assert len(paths) == 20
    assert len(owner_paths) == 18
    forbidden = ("/x2/", "/evidence/", "/closeout/", "/seal/", "/route/")
    assert not any(any(marker in path for marker in forbidden) for path in owner_paths)


def test_every_phase_json_document_parses() -> None:
    paths = sorted(PHASE_ROOT.rglob("*.json"))
    assert len(paths) >= 371
    for path in paths:
        assert isinstance(json.loads(path.read_text(encoding="utf-8")), dict)
