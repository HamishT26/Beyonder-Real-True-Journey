from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
sys.path.insert(0, str(SCRIPTS))

from ghc_family_caelen_ash_v676_v2_core import (  # noqa: E402
    parse_rational_unit,
    validate_playback_graph,
    validate_proposal,
    validate_provenance,
)


BASE = REPO / "docs" / "caelen-ash" / "v676-v2"
X2 = BASE / "x2"
X1 = "39daa2da64125b839714efa8b7488d8ed9ed364b"
BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO), *args], text=True).strip()


def test_x2_is_built_only_from_immutable_x1() -> None:
    assert git("branch", "--show-current") == BRANCH
    head = git("rev-parse", "HEAD")
    if head == X1:
        assert git("diff", "--cached", "--name-only") or git("status", "--porcelain=v1")
    else:
        assert git("rev-parse", "HEAD^") == X1


def test_exact_core_outcome_counts_and_vocabulary() -> None:
    data = load(X2 / "proposal-outcomes.json")
    assert set(data["outcome_vocabulary"]) == LABELS
    counts = Counter(row["outcome"] for row in data["outcomes"])
    assert counts == Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
    assert data["counts"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}


def test_all_forty_contracts_are_zero_row_and_structurally_valid() -> None:
    paths = sorted((X2 / "contracts").glob("CA6762-N*.json"))
    assert len(paths) == 40
    for path in paths:
        row = load(path)
        assert validate_proposal(row) == []
        assert row["rows"] == []
        assert row["real_world_authority"] is False
        assert row["source_id"] != row["derivative_id"]
        assert row["network_calls"] == 0
        assert row["external_actions"] == 0


def test_all_forty_positive_controls_pass_without_broader_credit() -> None:
    data = load(X2 / "positive-controls.json")
    assert data["count"] == 40
    assert data["all_accepted"] is True
    assert len(data["receipts"]) == 40
    assert all(row["accepted"] and row["real_world_rows"] == 0 for row in data["receipts"])
    assert all(row["credit_boundary"] == "bounded owner-local synthetic structure only" for row in data["receipts"])


def test_all_160_preregistered_mutations_are_retained_and_rejected() -> None:
    data = load(X2 / "rejected-mutations.json")
    assert data["count"] == 160
    assert data["all_rejected"] is True
    assert data["zero_credit_negatives"] == 160
    assert len(data["receipts"]) == 160
    counts = Counter(row["proposal_id"] for row in data["receipts"])
    assert set(counts.values()) == {4}
    assert all(row["rejected"] and row["validator_errors"] for row in data["receipts"])
    assert all(row["zero_credit_negative"] is True for row in data["receipts"])


def test_twenty_phase_local_skills_are_built_quick_validated_and_smoke_used() -> None:
    data = load(X2 / "skill-smoke-summary.json")
    assert data["count"] == 20
    assert data["all_quick_validated"] is True
    assert data["all_smoke_used"] is True
    assert data["global_installs"] == 0
    skill_dirs = [path for path in (X2 / "skills").iterdir() if path.is_dir()]
    assert len(skill_dirs) == 20
    for path in skill_dirs:
        assert (path / "SKILL.md").is_file()
        assert (path / "skill.json").is_file()
        assert (path / "smoke-receipt.json").is_file()


def test_ten_family_current_runners_are_built_invoked_and_witnessed() -> None:
    data = load(X2 / "runner-smoke-receipts.json")
    assert data["count"] == 10
    assert data["all_positive_accepted"] is True
    assert data["all_invalid_rejected"] is True
    assert all(row["family_current_name"] for row in data["receipts"])
    assert all(row["invocation_count"] == 2 for row in data["receipts"])
    for row in data["receipts"]:
        assert (SCRIPTS / row["runner"]).is_file()


def test_each_runner_can_be_smoke_invoked_again_in_isolation() -> None:
    rows = load(X2 / "runner-smoke-receipts.json")["receipts"]
    for row in rows:
        positive = json.loads(subprocess.check_output([sys.executable, "-X", "utf8", str(SCRIPTS / row["runner"]), "--smoke"], text=True, cwd=REPO))
        invalid = json.loads(subprocess.check_output([sys.executable, "-X", "utf8", str(SCRIPTS / row["runner"]), "--smoke", "--invalid"], text=True, cwd=REPO))
        assert positive["accepted"] is True
        assert invalid["accepted"] is False
        assert positive["expectation_met"] is True and invalid["expectation_met"] is True


def test_substantive_tools_accept_positive_and_reject_invalid_fixtures() -> None:
    assert parse_rational_unit("15/2", "in/s")["accepted"] is True
    assert parse_rational_unit("7.5", "in/s")["accepted"] is False
    assert validate_playback_graph(["a", "b"], [("a", "b")])["accepted"] is True
    assert validate_playback_graph(["a", "b"], [("a", "b"), ("b", "a")])["accepted"] is False
    assert validate_provenance("SYNTH-A", "SYNTH-B", ["capture"])["accepted"] is True
    assert validate_provenance("SYNTH-A", "SYNTH-A", ["capture"])["accepted"] is False


def test_portfolio_floors_execute_only_bounded_work() -> None:
    data = load(X2 / "portfolio-execution.json")
    assert len(data["safe_now"]) == 60
    assert len(data["candidate"]) == 30
    assert len(data["exact_approval"]) == 20
    assert len(data["blocked"]) == 10
    assert all(row["status"] == "completed" for row in data["safe_now"])
    assert all(row["status"] == "completed" for row in data["candidate"])
    assert all(row["status"] == "unexecuted_exact_gate" for row in data["exact_approval"])
    assert all(row["status"] == "blocked_unexecuted" for row in data["blocked"])
    assert data["core_outcome_counts_unchanged_by_portfolio_status"] is True


def test_clean_fix_refine_floor_and_successor_zero_credit() -> None:
    data = load(X2 / "clean-fix-refine-execution.json")
    assert len(data["owner_tasks"]) == 60
    assert len(data["successor_recommendations"]) == 30
    assert all(row["status"] == "completed" for row in data["owner_tasks"])
    assert data["successor_completion_credit"] == 0


def test_method_flow_has_exact_failed_and_passing_witness_arithmetic() -> None:
    data = load(X2 / "method-flow" / "ledger.json")
    counts = data["phase_ledger_counts"]
    assert counts == {"methods": 447, "failed": 180, "passing": 267}
    assert len(data["methods"]) == 447
    assert data["new_x2_effective_methods"] == 434
    assert data["new_x2_negatives"] == 172
    assert data["new_x2_failed_witnesses"] == 172
    assert data["new_x2_bounded_passing_witnesses"] == 262
    assert data["failure_erasure_forbidden"] is True
    ids = {row["method_id"] for row in data["methods"]}
    for row in data["methods"]:
        if row["truth"] is False:
            assert row["recovered_by"] in ids


def test_effective_overlay_adds_failures_without_rewriting_activation() -> None:
    data = load(X2 / "phase-truth.json")
    overlay = data["current_overlay"]
    assert overlay == {
        "effective_negatives": 41842,
        "effective_methods": 31201,
        "retained_failed_witnesses": 13503,
        "bounded_passing_witnesses": 18387,
        "open_gaps": 351,
        "exact_gates": 343,
    }
    assert data["proposal_chain"] == 7470
    assert data["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_new_open_gaps_and_exact_gates_remain_unclosed() -> None:
    gaps = load(X2 / "open-gap-register.json")
    gates = load(X2 / "exact-gate-register.json")
    assert gaps["inherited_open_gaps"] == 349 and gaps["new_open_gaps"] == 2 and gaps["total_open_gaps"] == 351
    assert gates["inherited_exact_gates"] == 341 and gates["new_exact_gates"] == 2 and gates["total_exact_gates"] == 343
    assert gaps["closure_claimed"] is False
    assert gates["authority_compensation_forbidden"] is True


def test_environment_receipt_changes_no_software_or_host_security() -> None:
    data = load(X2 / "environment-version-receipt.json")
    assert data["python"]["available"] is True
    assert data["software_installed"] == []
    assert data["codex_desktop_updated"] is False
    assert data["host_security_changed"] is False
    assert data["windows_features_changed"] is False
    assert data["rebooted"] is False


def test_static_report_is_text_first_and_reserves_manual_evaluation() -> None:
    value = (X2 / "accessible-report.html").read_text(encoding="utf-8")
    assert "<caption>Core proposal outcomes</caption>" in value
    assert "NOT_READY_FOR_STAGE_20" in value
    assert "Manual keyboard, screen-reader" in value
    assert "<script" not in value.lower()


def test_x2_evidence_has_zero_real_rows_participants_network_calls_and_actions() -> None:
    data = load(X2 / "phase-truth.json")
    assert data["real_world_rows"] == 0
    assert data["participants"] == 0
    assert data["network_calls_during_x2_execution"] == 0
    assert data["external_actions"] == 0


def test_no_final_or_closeout_material_exists_in_evidence_stage() -> None:
    assert not (BASE / "final").exists()
    assert not (BASE / "closeout").exists()
    assert not list(SCRIPTS.glob("*caelen_ash_v676_v2_final*"))
    assert not list((REPO / "tests").glob("*caelen_ash_v676_v2_final*"))


def test_every_owner_json_parses_and_file_count_is_below_rotation_stop() -> None:
    paths = [path for path in BASE.rglob("*") if path.is_file()]
    assert len(paths) < 2000
    json_paths = [path for path in paths if path.suffix.lower() == ".json"]
    assert len(json_paths) >= 140
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_documents_remain_under_word_cap() -> None:
    for path in BASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".html"}:
            assert len(path.read_text(encoding="utf-8").split()) <= 100_000


def test_owner_packet_has_no_private_absolute_path_raw_route_or_secret_value() -> None:
    patterns = [
        re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
        re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
        re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
        re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    ]
    for path in BASE.rglob("*"):
        if not path.is_file():
            continue
        value = path.read_text(encoding="utf-8")
        for pattern in patterns:
            assert pattern.search(value) is None, f"{pattern.pattern} in {path.relative_to(REPO)}"
