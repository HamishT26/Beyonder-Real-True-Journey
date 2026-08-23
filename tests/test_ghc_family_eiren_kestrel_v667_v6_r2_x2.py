from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "eiren-kestrel" / "v667-v6-r2"
BUILDER_PATH = ROOT / "scripts" / "build_ghc_family_eiren_kestrel_v667_v6_r2_x2.py"
X1_HEAD = "0ff9e3058d4df62d30035b7d9f5d5ce0939f10a2"


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
    assert receipt["tools"] == 13
    assert receipt["skills"] == receipt["runners"] == 10
    assert receipt["global_skill_promotions"] == 10
    assert receipt["main_family_state_updates"] == 8
    assert receipt["web_reflections"] == 30
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


def test_thirteen_tool_transaction_retains_initial_oracle_failure_and_isolated_recovery() -> None:
    receipt = load("x2/tooling/thirteen-tool-transaction-receipt.json")
    assert receipt["top_level_program_count"] == 13
    assert {row["name"] for row in receipt["top_level_programs"]} == {
        "validate-pyproject", "pyproject-fmt", "deptry", "vulture", "radon", "xenon",
        "codespell", "yamllint", "toml-sort", "pip-licenses", "cyclonedx-bom",
        "check-manifest", "twine",
    }
    assert all(row["verified"] and len(row["sha256"]) == 64 for row in receipt["artifact_rows"])
    assert receipt["install_report"]["entry_count"] == 86
    assert receipt["installed_distribution_count"] == 87
    assert receipt["installer"] == {"name": "pip", "version": "26.2.1", "new_tool_credit": 0}
    assert receipt["audit_infrastructure"] == {"name": "pip-audit", "version": "2.10.1", "new_tool_credit": 0}
    assert receipt["post_install_audit"]["invocation_count"] == 1
    assert receipt["post_install_audit"]["known_vulnerabilities"] == 0
    assert receipt["post_install_audit"]["dependency_rows"] == 87
    assert receipt["post_install_audit"]["replayed"] is False
    assert receipt["initial_smoke_aggregate"]["passed"] == 12
    assert receipt["initial_smoke_aggregate"]["failed"] == 1
    assert receipt["initial_smoke_aggregate"]["aggregate_success_credit"] == 0
    assert receipt["isolated_dependency_recovery"]["tool"] == "pyproject-fmt"
    assert receipt["isolated_dependency_recovery"]["passed"] is True
    assert receipt["isolated_dependency_recovery"]["passing_components_replayed"] == 0
    assert receipt["credit"]["new_tool_surfaces_completed"] == 13
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
    builder = load_builder()
    methods = load("method-flow/x2-method-flow-ledger.json")
    negatives = load("evidence/retained-negative-register.json")
    witnesses = load("evidence/witness-summary.json")
    gates = load("evidence/exact-open-gate-register.json")
    operational = len(builder.X1.STARTUP_FAILURES) + len(builder.X2_FAILURES)
    phase_total = operational + 100
    method_total = operational + 216
    assert methods["phase_method_additions"] == len(methods["methods"]) == method_total
    assert methods["provisional_effective_methods"] == 13926 + method_total
    assert negatives["operational_failure_count"] == operational
    assert negatives["rejecting_mutation_count"] == 100
    assert negatives["phase_negative_additions"] == phase_total
    assert negatives["provisional_effective_negatives"] == 28036 + phase_total
    assert witnesses["phase_failed_witnesses"] == phase_total
    assert witnesses["phase_passing_witnesses"] == method_total
    assert witnesses["provisional_failed_witnesses"] == 320 + phase_total
    assert witnesses["provisional_passing_witnesses"] == 495 + method_total
    assert gates["provisional_open_gaps"] == 198
    assert gates["provisional_exact_gates"] == 196
    assert gates["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_global_promotions_family_state_and_public_reflections_are_bounded() -> None:
    promotions = load("x2/global-state/global-skill-promotion-receipt.json")
    state = load("x2/global-state/main-family-state-update-receipt.json")
    reflections = load("x2/web-reflection-ledger.json")
    assert promotions["promoted"] == promotions["composite_component_completion"] == 10
    assert promotions["first_validator_aggregate"]["passed"] == 3
    assert promotions["first_validator_aggregate"]["failed_before_schema"] == 7
    assert promotions["first_validator_aggregate"]["aggregate_success_credit"] == 0
    assert promotions["isolated_utf8_recovery"]["affected_entries"] == 7
    assert promotions["isolated_utf8_recovery"]["passed"] == 7
    assert promotions["isolated_utf8_recovery"]["previously_passing_entries_replayed"] == 0
    assert state["updated_surface_count"] == 8
    assert state["current_tool_count"] == 41
    assert state["future_new_tool_target"] == 3
    assert reflections["reflection_count"] == 30
    assert reflections["real_observation_count"] == 0
    assert reflections["authority_conferred"] is False
    recovery = load("x2/build-recovery-after-global-boundary.json")
    assert recovery["failed_full_builder_success_credit"] == 0
    assert recovery["failed_first_boundary_recovery_success_credit"] == 0
    assert recovery["failed_second_boundary_recovery_success_credit"] == 0
    assert recovery["recovery_attempt_count"] == 3
    assert recovery["preceding_components_replayed"] == 0
    assert recovery["recovery_passed"] is True
    post_build = load("x2/post-build-operational-recovery.json")
    assert post_build["failed_probe_credit"] == 0
    assert post_build["earlier_x2_components_replayed"] == 0
    assert post_build["status"] == "PASS_BOUNDED_RECOVERY"
    aggregate = load("validation/x2-test-aggregate-failure.json")
    assert aggregate["passed"] == 13 and aggregate["failed"] == 1
    assert aggregate["aggregate_success_credit"] == 0
    assert aggregate["passing_tests_to_replay"] == 0
    isolated_failures = load("validation/x2-test-isolated-recovery-failures.json")
    assert isolated_failures["failed_attempt_count"] == 1
    assert isolated_failures["success_credit"] == 0
    assert isolated_failures["other_thirteen_tests_replayed"] == 0


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
    owner_paths = [path for path in paths if path.startswith("docs/eiren-kestrel/v667-v6-r2/")]
    assert len(paths) == 20
    assert len(owner_paths) == 18
    forbidden = ("/x2/", "/evidence/", "/closeout/", "/seal/", "/route/")
    assert not any(any(marker in path for marker in forbidden) for path in owner_paths)


def test_every_phase_json_document_parses() -> None:
    paths = sorted(PHASE_ROOT.rglob("*.json"))
    assert len(paths) >= 371
    for path in paths:
        assert isinstance(json.loads(path.read_text(encoding="utf-8")), dict)
