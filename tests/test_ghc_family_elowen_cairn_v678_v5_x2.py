from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
BASE = REPO / "docs" / "elowen-cairn" / "v678-v5"
X2 = BASE / "x2"
X1_COMMIT = "c938128b0e6307c4aaed8966340486b8c5315382"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(relative: str):
    return json.loads((X2 / relative).read_text(encoding="utf-8"))


def test_x2_phase_truth_and_outcomes_are_exact() -> None:
    truth = load("phase-truth.json")
    assert truth["x1"] == X1_COMMIT
    assert truth["declared_proposal_chain"] == 8570
    assert truth["outcomes"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["real_world_rows"] == 0
    assert truth["observed_measurements"] == 0
    assert truth["external_actions"] == 0
    outcomes = load("proposal-outcomes.json")
    assert len(outcomes["outcomes"]) == 60
    assert set(row["outcome"] for row in outcomes["outcomes"]) == LABELS
    assert Counter(row["outcome"] for row in outcomes["outcomes"]) == Counter(truth["outcomes"])


def test_all_positive_contracts_are_zero_row_unmeasured_and_non_authority() -> None:
    contracts = sorted((X2 / "contracts").glob("*.json"))
    receipts = sorted((X2 / "evidence").glob("*.json"))
    assert len(contracts) == 60
    assert len(receipts) == 60
    for path in contracts:
        value = json.loads(path.read_text(encoding="utf-8"))
        assert value["surrogate_object_id"].startswith("SYNTH-MARITIME-")
        assert value["raw_identifier"] is None
        assert value["measurements"] == []
        assert value["real_world_rows"] == 0
        assert value["external_actions"] == 0
        for field in (
            "real_world_authority",
            "condition_determined",
            "authenticity_determined",
            "treatment_performed",
            "professional_release",
            "legal_approval",
            "cultural_approval",
            "maori_authority",
            "production_ready",
            "empirical_confirmation",
        ):
            assert value[field] is False
    for path in receipts:
        value = json.loads(path.read_text(encoding="utf-8"))
        assert value["accepted"] is True
        assert value["observed_measurements"] == 0
        assert value["broader_claim_credit"] == 0


def test_all_240_preregistered_mutations_are_rejected_and_retained() -> None:
    paths = sorted((X2 / "mutations").glob("*.json"))
    assert len(paths) == 240
    for path in paths:
        value = json.loads(path.read_text(encoding="utf-8"))
        assert value["execution_status"] == "executed_rejected_zero_credit"
        assert value["accepted"] is False
        assert value["failed_witness_retained"] is True
        assert value["rejection_reasons"]
    summary = load("mutation-summary.json")
    assert summary == {"preregistered": 240, "executed": 240, "rejected": 240, "failed_witnesses_retained": 240}


def test_twenty_phase_local_skills_follow_full_local_lifecycle() -> None:
    summary = load("skill-summary.json")
    assert summary["count"] == 20
    assert summary["global_installs"] == 0
    assert all(
        row["official_initialization"]
        and row["read_through_eof"]
        and row["quick"]
        and row["smoke"]
        and row["global_install"] is False
        for row in summary["skills"]
    )
    read_receipt = load("skill-read-through-receipt.json")
    assert read_receipt["count"] == 20 and read_receipt["before_smoke"] is True
    dirs = [path for path in (X2 / "skills").iterdir() if path.is_dir()]
    assert len(dirs) == 20
    for path in dirs:
        skill = (path / "SKILL.md").read_text(encoding="utf-8")
        contract = json.loads((path / "skill.json").read_text(encoding="utf-8"))
        assert skill.startswith("---\n")
        assert "[TODO:" not in skill
        for heading in ("## Inputs", "## Procedure", "## Refusal conditions", "## Output"):
            assert heading in skill
        assert contract["initialized_with_official_skill_creator"] is True
        assert contract["global_install"] is False
        assert contract["real_world_rows"] == 0
        assert contract["observed_measurements"] == 0
        assert contract["external_actions"] == 0
    receipts = list((X2 / "skill-receipts").glob("*.json"))
    assert len(receipts) == 40
    quick = [json.loads(path.read_text(encoding="utf-8")) for path in receipts if path.name.endswith("-quick.json")]
    assert len(quick) == 20 and all(row["accepted"] and row["output"] == "Skill is valid!" for row in quick)
    interfaces = list((X2 / "skills").glob("*/agents/openai.yaml"))
    assert len(interfaces) == 20
    for path in interfaces:
        interface = yaml.safe_load(path.read_text(encoding="utf-8"))["interface"]
        assert interface["display_name"] and interface["short_description"]


def test_ten_family_current_runners_accept_positive_and_reject_invalid() -> None:
    summary = load("runner-summary.json")
    assert summary["count"] == 10
    assert all(row["positive"] and row["invalid_rejected"] for row in summary["runners"])
    receipts = list((X2 / "runner-receipts").glob("*.json"))
    assert len(receipts) == 20
    positives = [json.loads(path.read_text(encoding="utf-8")) for path in receipts if path.name.endswith("-positive.json")]
    invalids = [json.loads(path.read_text(encoding="utf-8")) for path in receipts if path.name.endswith("-invalid.json")]
    assert len(positives) == len(invalids) == 10
    assert all(row["accepted"] and row["expectation_met"] for row in positives)
    assert all(not row["accepted"] and row["expectation_met"] for row in invalids)


def test_portfolio_floors_execute_without_exact_or_blocked_action() -> None:
    summary = load("portfolio/execution-summary.json")
    assert summary == {
        "safe_now_completed": 60,
        "candidate_completed_without_core_promotion": 30,
        "clean_fix_refine_completed": 60,
        "exact_approval_unexecuted": 20,
        "blocked_unexecuted": 10,
        "real_world_rows": 0,
        "external_actions": 0,
    }
    assert len(list((X2 / "task-receipts" / "safe_now").glob("*.json"))) == 60
    assert len(list((X2 / "task-receipts" / "candidate").glob("*.json"))) == 30
    assert len(list((X2 / "task-receipts" / "clean_fix_refine").glob("*.json"))) == 60
    exact = load("portfolio/exact-approval-packets.json")
    blocked = load("portfolio/blocked-packets.json")
    assert exact["count"] == 20 and all(row["execution_count"] == 0 for row in exact["packets"])
    assert blocked["count"] == 10 and all(row["execution_count"] == 0 for row in blocked["packets"])


def test_method_flow_retains_false_witnesses_and_recoveries() -> None:
    ledger = load("method-flow/ledger.json")
    methods = ledger["methods"]
    failed = [row for row in methods if row["truth"] is False]
    passed = [row for row in methods if row["truth"] is True]
    assert ledger["phase_ledger_counts"] == {"methods": 794, "failed": 267, "passing": 527}
    assert len(methods) == 794 and len(failed) == 267 and len(passed) == 527
    ids = {row["method_id"] for row in methods}
    assert len(ids) == len(methods)
    assert all(row["recovered_by"] in ids for row in failed)
    assert ledger["current_overlay"] == {
        "effective_negatives": 46993,
        "effective_methods": 44536,
        "retained_failed_witnesses": 18654,
        "bounded_passing_witnesses": 28967,
        "open_gaps": 407,
        "exact_gates": 398,
    }
    negatives = load("retained-negative-register.json")
    assert negatives["count"] == 267
    assert negatives["converted_to_pass"] == 0


def test_gap_gate_and_helper_evidence_remain_bounded() -> None:
    gaps = load("open-gap-register.json")
    gates = load("exact-gate-register.json")
    assert gaps["inherited"] == 404 and gaps["new"] == 3 and gaps["current"] == 407
    assert gates["inherited"] == 395 and gates["new"] == 3 and gates["current"] == 398
    assert gates["exact_approval_packets_unexecuted"] == 20
    assert gates["blocked_packets_unexecuted"] == 10
    helper = load("bounded-helper-evidence.json")
    assert all(value["accepted"] for value in helper.values())
    assert helper["component_topology"]["physical_object_claim"] is False
    assert helper["provenance"]["custody_claim"] is False
    assert helper["measurement_vacancy"]["measurement_result"] is False
    assert helper["accessibility"]["accessibility_complete"] is False


def test_no_final_closeout_handoff_or_private_payload_exists_at_evidence() -> None:
    assert not (BASE / "final").exists()
    assert not (BASE / "closeout").exists()
    assert not (BASE / "handoffs").exists()
    assert not list((REPO / "scripts").glob("*elowen_cairn_v678_v5_final*"))
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


def test_all_phase_json_parses_and_documents_remain_below_cap() -> None:
    json_paths = list(BASE.rglob("*.json"))
    assert len(json_paths) >= 600
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    docs = [path for path in BASE.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".html"}]
    assert len(docs) >= 22
    assert max(len(path.read_text(encoding="utf-8").split()) for path in docs) <= 100_000
