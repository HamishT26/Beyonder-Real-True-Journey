from __future__ import annotations

import hashlib
import io
import json
import subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from scripts.ghc_family_caelen_morrow_v673_v2_accordion_record import (
    synthetic_record,
    validate_record,
    with_component_state,
)
from scripts.ghc_family_caelen_morrow_v673_v2_authority_gate import (
    evaluate,
    gate_inventory,
    split_estimate_authorization,
)
from scripts.ghc_family_caelen_morrow_v673_v2_transition_graph import (
    state_machine_receipt,
    topological_order,
    transition,
)

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "caelen-morrow" / "v673-v2"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def batch_index_blobs(paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, stderr = process.communicate(input=("\n".join(f":{path}" for path in paths) + "\n").encode("utf-8"), timeout=240)
    assert process.returncode == 0, stderr.decode("utf-8", errors="replace")
    stream = io.BytesIO(output)
    result: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().decode("utf-8").strip().split()
        assert len(header) == 3 and header[1] == "blob"
        size = int(header[2])
        result[path] = stream.read(size)
        assert stream.read(1) == b"\n"
    assert not stream.read()
    return result


def test_outcomes_are_exact() -> None:
    ledger = load("x2/proposal-ledger.json")
    assert Counter(row["outcome"] for row in ledger["rows"]) == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}


def test_x1_dispositions_equal_x2_outcomes() -> None:
    x1 = {row["proposal_id"]: row["expected_disposition"] for row in load("x1/proposals.json")["proposals"]}
    x2 = {row["proposal_id"]: row["outcome"] for row in load("x2/proposal-ledger.json")["rows"]}
    assert x1 == x2


def test_all_proposal_artifacts_are_present() -> None:
    for row in load("x1/proposals.json")["proposals"]:
        for relative in row["concrete_artifacts"]:
            assert (OWNER_ROOT / relative).is_file()


def test_positive_controls_are_exact() -> None:
    payload = load("x2/positive-controls.json")
    assert payload["count"] == 36
    assert all(row["passed"] and row["real_rows"] == 0 for row in payload["rows"])


def test_all_160_mutations_are_rejected() -> None:
    payload = load("x2/rejecting-mutations.json")
    assert payload["count"] == payload["rejected"] == 160
    assert payload["accepted"] == 0
    assert all(not row["accepted"] and row["retained"] and row["credit"] == 0 for row in payload["rows"])


def test_synthetic_record_passes() -> None:
    assert validate_record(synthetic_record())["valid"] is True


def test_nonzero_real_row_fails() -> None:
    record = synthetic_record()
    record["real_world_rows"] = 1
    result = validate_record(record)
    assert result["valid"] is False
    assert "real_world_rows_must_be_zero" in result["issues"]


@given(st.text(min_size=0, max_size=30).filter(lambda value: not value.startswith("acc-syn-") or len(value) != 11))
def test_arbitrary_nonconforming_record_ids_fail(record_id: str) -> None:
    record = synthetic_record()
    record["record_id"] = record_id
    assert validate_record(record)["valid"] is False


def test_component_update_is_copy_on_write() -> None:
    original = synthetic_record()
    updated = with_component_state(original, "register_switches", "quarantined")
    assert "register_switches" not in original["component_states"]
    assert updated["component_states"]["register_switches"] == "quarantined"


def test_invalid_component_state_raises() -> None:
    with pytest.raises(ValueError):
        with_component_state(synthetic_record(), "bellows", "repaired")


def test_transition_accepts_closed_vocabulary_edge() -> None:
    assert transition("planned", "represented")["accepted"] is True


@given(st.text(min_size=0, max_size=20), st.text(min_size=0, max_size=20))
def test_unknown_or_invalid_transitions_never_gain_real_effect(current: str, target: str) -> None:
    result = transition(current, target)
    if result["accepted"]:
        assert result["real_world_effect"] is False
        assert result["authority_effect"] is False


def test_dag_returns_deterministic_order() -> None:
    result = topological_order(["case", "bellows", "reed"], [("case", "bellows"), ("bellows", "reed")])
    assert result["valid"] is True
    assert result["order"] == ["case", "bellows", "reed"]


def test_cycle_is_rejected() -> None:
    assert topological_order(["a", "b"], [("a", "b"), ("b", "a")])["valid"] is False


def test_authority_gate_allows_named_safe_action() -> None:
    result = evaluate("validate_schema")
    assert result["permitted"] is True
    assert result["real_world_authority"] is False


@pytest.mark.parametrize("action", gate_inventory()["protected_classes"])
def test_every_protected_action_is_exact_gated(action: str) -> None:
    result = evaluate(action)
    assert result["permitted"] is False
    assert result["state"] == "exact_gate"


def test_unknown_action_is_open_gap() -> None:
    result = evaluate("invented_action")
    assert result["permitted"] is False
    assert result["state"] == "open_gap"


def test_estimate_never_becomes_authorization() -> None:
    result = split_estimate_authorization({"schema": "ghc.family.synthetic-estimate.v1", "synthetic": True, "scope_tokens": ["reed"], "estimate_status": "represented_only", "authorization_status": "absent_exact_gate"})
    assert result["valid"] is True
    assert result["estimate_is_authorization"] is False
    assert result["authorization_executed"] is False


def test_method_flow_has_one_failed_and_passing_witness_per_method() -> None:
    flow = load("x2/method-flow-evidence.json")
    assert flow["method_count"] == 210
    assert flow["failed_witness_count"] == flow["passing_witness_count"] == 210
    assert len(flow["witnesses"]) == 420
    assert all(row["retained"] for row in flow["witnesses"])


def test_skill_packages_are_validated_and_not_global() -> None:
    receipt = load("x2/skills/validation-receipt.json")
    assert receipt["skill_count"] == 20
    assert receipt["global_installations"] == 0
    assert all(row["quick_validation_passed"] and row["accepting_smoke_passed"] and row["rejecting_smoke_passed"] for row in receipt["rows"])


def test_runners_are_smoke_used_and_not_global() -> None:
    receipt = load("x2/runners/validation-receipt.json")
    assert receipt["runner_count"] == 10
    assert receipt["global_installations"] == 0
    assert all(row["smoke_passed"] and row["rejecting_fixture_passed"] for row in receipt["rows"])


def test_substantive_tools_have_rejecting_and_accepting_witnesses() -> None:
    receipt = load("x2/tools/tool-receipts.json")
    assert receipt["tool_count"] == 3
    assert receipt["all_passed"] is True
    assert receipt["check_count"] == 10


def test_flashcards_are_content_addressed_navigation_only() -> None:
    deck = load("x2/flashcards/deck.json")
    assert deck["card_count"] == 60
    assert deck["tier_count"] == 4
    assert deck["module_count"] == 13
    assert len({card["content_address"] for card in deck["cards"]}) == 60
    assert all(not card["identity_continuity_claim"] and not card["cache_or_cognition_claim"] for card in deck["cards"])


def test_official_sources_are_vocabulary_only() -> None:
    sources = load("x2/source-status.json")
    assert len(sources["sources"]) == 4
    assert sources["network_calls_in_phase_artifacts"] == 0
    assert "no observation" in sources["boundary"].lower()


def test_disabled_adapter_has_zero_transport_and_rows() -> None:
    adapter = load("x2/adapters/public-collection-adapter.json")
    assert adapter["transport_enabled"] is False
    assert adapter["network_calls"] == adapter["real_rows"] == 0
    assert adapter["outcome"] == "open_gap"


def test_gmut_has_no_empirical_claim() -> None:
    gmut = load("x2/gmut/symbolic-operator-atlas.json")
    assert gmut["observations"] == gmut["likelihoods"] == gmut["constraints"] == 0
    assert gmut["prediction_claim"] is False


def test_thos_has_zero_participants_and_real_arms() -> None:
    thos = load("x2/thos/proxy-evidence.json")
    assert thos["participants"] == thos["operators"] == thos["real_arms"] == 0
    assert thos["state"] == "represented"


def test_freed_id_has_no_real_lifecycle() -> None:
    freed = load("x2/freed-id/synthetic-boundary.json")
    assert freed["real_keys"] == freed["proofs"] == freed["issuance"] == freed["revocations"] == 0
    assert freed["state"] == "represented_nonproduction"


def test_cbr_authority_remains_exact_gated() -> None:
    cbr = load("x2/cbr/authority-boundary.json")
    assert cbr["state"] == "exact_gate"
    assert cbr["executed"] is False
    assert cbr["maori_authority"] is False


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        self.tags.append(tag)


def test_accessible_companion_has_structural_landmarks() -> None:
    parser = StructureParser()
    parser.feed((OWNER_ROOT / "x2/accessibility/handover-companion.html").read_text(encoding="utf-8"))
    for tag in ["header", "nav", "main", "section", "table", "caption"]:
        assert tag in parser.tags


def test_portfolio_keeps_holds_unexecuted() -> None:
    portfolio = load("x2/portfolio-evidence.json")
    assert portfolio["exact_approval"]["executed"] == 0
    assert portfolio["blocked"]["executed"] == 0
    assert portfolio["skills"]["quick_validated_and_smoke_used"] == 20


def test_environment_receipt_performed_no_install_or_update() -> None:
    receipt = load("x2/environment-version-receipt.json")
    assert receipt["installations_performed"] == receipt["updates_performed"] == 0
    assert receipt["versions"]["pytest"]["available"] is True
    assert receipt["versions"]["ruff"]["available"] is True
    assert receipt["versions"]["mypy"]["available"] is True


def test_evidence_manifest_replays_when_present() -> None:
    path = OWNER_ROOT / "validation/evidence-manifest.json"
    if not path.exists():
        return
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert manifest["entry_count"] == len(manifest["entries"])
    blobs = batch_index_blobs([row["path"] for row in manifest["entries"]])
    for row in manifest["entries"]:
        blob = blobs[row["path"]]
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest() == row["sha256"]


def test_state_machine_receipt_has_one_terminal_state() -> None:
    receipt = state_machine_receipt()
    assert receipt["terminal"] == ["closed_synthetic"]
