from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
OUT = ROOT / "docs" / "vesper-arlen" / "v673-v6"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
toolbank = os.environ.get("VESPER_V6736_TOOLBANK")
if toolbank:
    sys.path.insert(0, str(Path(toolbank) / "site-packages"))

from ghc_family_sextant_contracts import (  # noqa: E402
    canonical_digest,
    component_tree_receipt,
    jsonpath_values,
    mutation_cases,
    package_versions,
    structural_html_audit,
    synthetic_record,
    validate_outcome_ledger,
    validate_synthetic_record,
)
from ghc_family_sextant_runners import RUNNERS  # noqa: E402


def load(relative: str):
    return json.loads((OUT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    assert result.returncode == 0, result.stderr.decode("utf-8", "replace")
    return result.stdout


def test_toolbank_is_explicit_and_available() -> None:
    assert toolbank, "VESPER_V6736_TOOLBANK must identify the D-isolated test bank"
    assert Path(toolbank).drive.upper() == "D:"
    assert package_versions() == {"rfc8785": "0.1.4", "jsonpath-ng": "1.8.0", "treelib": "1.8.0", "six": "1.17.0"}


def test_positive_record_contract_accepts_only_synthetic_fixture() -> None:
    record = synthetic_record("VA6736-N001", 1)
    result = validate_synthetic_record(record)
    assert result.accepted
    assert result.errors == ()
    assert record["real_rows"] == record["network_calls"] == record["external_actions"] == 0
    assert record["authority_claim"] is False


def test_all_four_preregistered_mutations_are_rejected() -> None:
    cases = mutation_cases(synthetic_record("VA6736-N001", 1))
    assert len(cases) == 4
    results = [validate_synthetic_record(case["record"]) for case in cases]
    assert all(not result.accepted and result.errors for result in results)
    assert {case["mutation"] for case in cases} == {"missing_synthetic_flag", "real_row_injection", "authority_upgrade", "unit_domain_escape"}


def test_canonicalization_is_order_invariant() -> None:
    first = canonical_digest({"b": 2, "a": [1, {"x": "y"}]})
    second = canonical_digest({"a": [1, {"x": "y"}], "b": 2})
    assert first == second
    assert first["canonical_utf8"] == '{"a":[1,{"x":"y"}],"b":2}'


def test_jsonpath_query_extracts_all_outcomes() -> None:
    ledger = load("x2/proposal-ledger.json")
    values = jsonpath_values(ledger, "$.rows[*].outcome")
    assert len(values) == 40
    assert Counter(values) == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}


def test_component_tree_is_bounded_and_synthetic() -> None:
    receipt = component_tree_receipt()
    assert receipt["node_count"] == 9
    assert receipt["edge_count"] == 8
    assert receipt["depth"] == 2
    assert receipt["real_instrument"] is False


def test_proposal_ledger_has_only_four_outcomes() -> None:
    ledger = load("x2/proposal-ledger.json")
    assert ledger["proposal_count"] == len(ledger["rows"]) == 40
    assert ledger["outcome_counts"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert validate_outcome_ledger(ledger["rows"]).accepted
    assert all(row["real_rows"] == row["network_calls"] == row["external_actions"] == 0 for row in ledger["rows"])
    assert all(row["independent_reproduction"] is False for row in ledger["rows"])


def test_expected_and_observed_outcomes_match_without_upgrade() -> None:
    ledger = load("x2/proposal-ledger.json")
    assert all(row["outcome"] == row["expected_disposition"] for row in ledger["rows"])


def test_thirty_six_positive_controls_pass() -> None:
    document = load("x2/positive-controls.json")
    assert document["count"] == document["passed"] == 36
    assert all(row["accepted"] and row["bounded_passing_witness"] and not row["errors"] for row in document["rows"])


def test_all_160_mutations_are_rejected_and_retained() -> None:
    document = load("x2/rejecting-mutations.json")
    assert document["count"] == document["rejected"] == 160
    assert document["completion_credit"] == 0
    assert all(row["accepted"] is False and row["errors"] and row["retained"] and row["completion_credit"] == 0 for row in document["rows"])
    assert Counter(row["mutation"] for row in document["rows"]) == {"missing_synthetic_flag": 40, "real_row_injection": 40, "authority_upgrade": 40, "unit_domain_escape": 40}


def test_every_proposal_has_exactly_four_mutations() -> None:
    rows = load("x2/rejecting-mutations.json")["rows"]
    assert set(Counter(row["proposal_id"] for row in rows).values()) == {4}
    assert len(Counter(row["proposal_id"] for row in rows)) == 40


def test_tool_receipt_has_exact_hashes_and_no_shared_install() -> None:
    receipt = load("x2/tools/tool-receipts.json")
    assert receipt["d_isolated"] is True
    assert receipt["all_wheel_hashes_match_current_pypi_metadata"] is True
    assert receipt["shared_python_prefix_install_invoked"] is False
    assert receipt["shared_npm_prefix_install_invoked"] is False
    assert receipt["versions"] == {"rfc8785": "0.1.4", "jsonpath-ng": "1.8.0", "treelib": "1.8.0", "six": "1.17.0"}
    assert all(row["matched"] and row["expected_sha256"] == row["actual_sha256"] for row in receipt["wheel_checks"])
    assert receipt["supply_chain_audit"] is receipt["exhaustive_security"] is False


def test_ten_family_current_runners_pass_and_are_used() -> None:
    receipt = load("x2/runners/validation-receipt.json")
    assert len(RUNNERS) == receipt["runner_count"] == receipt["passed"] == 10
    assert all(row["tested"] and row["used"] and row["passed"] for row in receipt["rows"])
    assert all(row["runner"].startswith("ghc_family_") for row in receipt["rows"])


def test_twenty_phase_local_skills_are_built_tested_and_used() -> None:
    receipt = load("x2/skills/validation-receipt.json")
    assert receipt["skill_count"] == receipt["passed"] == 20
    assert all(row["built"] and row["smoke_tested"] and row["used"] and row["globally_installed"] is False for row in receipt["rows"])
    skill_files = sorted((OUT / "x2" / "skills").glob("*/SKILL.md"))
    assert len(skill_files) == 20
    assert all("## Boundaries" in path.read_text(encoding="utf-8") for path in skill_files)


def test_portfolio_execution_and_reservations_are_exact() -> None:
    evidence = load("x2/portfolio-evidence.json")
    assert len(evidence["safe_now"]) == 60
    assert len(evidence["candidate"]) == 30
    assert len(evidence["exact_approval"]) == 20
    assert len(evidence["blocked"]) == 10
    assert len(evidence["owner_clean_fix_refine"]) == 60
    assert len(evidence["successor_clean_fix_refine"]) == 30
    assert evidence["exact_or_blocked_executed"] == 0
    assert evidence["unsafe_filler_created"] is False
    assert all(row["state"] == "exact_approval_unexecuted" for row in evidence["exact_approval"])
    assert all(row["state"] == "blocked_unexecuted" for row in evidence["blocked"])


def test_successor_recommendations_have_zero_current_credit() -> None:
    evidence = load("x2/portfolio-evidence.json")
    for key in ("successor_skills", "successor_runners", "successor_clean_fix_refine"):
        assert len(evidence[key]) == 10 if key != "successor_clean_fix_refine" else len(evidence[key]) == 30
        assert all(row["completion_credit"] == 0 for row in evidence[key])
    assert evidence["successor_practice_recommendation"]["count"] == 1
    assert evidence["successor_practice_recommendation"]["completion_credit"] == 0


def test_accessibility_is_structural_not_complete() -> None:
    html = (OUT / "x2" / "accessibility" / "record-companion.html").read_text(encoding="utf-8")
    audit = structural_html_audit(html)
    assert audit["structural_pass"]
    assert audit["passed"] == audit["total"] == 9
    assert audit["accessibility_complete"] is False
    stored = load("x2/accessibility/structural-audit.json")
    assert stored == audit


def test_official_adapter_is_transport_disabled_and_zero_row() -> None:
    adapter = load("x2/adapters/official-catalog-zero-row.json")["adapter"]
    assert adapter == {"catalog_claim": False, "credentials": False, "queries": 0, "rows": 0, "transport_enabled": False}


def test_maori_authority_reservation_makes_no_decision() -> None:
    reservation = load("x2/cbr/maori-authority-reservation.json")["maori_authority"]
    assert reservation["decision_made"] is False
    assert reservation["authority_vacancy"] is True
    assert reservation["terms_used_as_authority_claims"] == []


def test_exact_gate_and_stage20_veto_remain_closed() -> None:
    gate = load("x2/gates/competent-authority-gate.json")
    veto = load("x2/gates/stage20-veto.json")
    assert gate["outcome"] == veto["outcome"] == "exact_gate"
    assert gate["real_rows"] == veto["real_rows"] == 0
    assert "Stage 20" in veto["vetoes"]


def test_method_flow_preserves_activation_and_new_failures() -> None:
    flow = load("x2/method-flow-evidence.json")
    assert flow["activation_baseline"]["effective_negatives"] == 37254
    assert flow["new_operational_methods"] == 14
    assert flow["new_rejecting_mutation_methods"] == 160
    assert flow["new_positive_controls"] == 36
    assert flow["new_runner_witnesses"] == 10
    totals = flow["effective_totals_at_evidence"]
    assert totals == {"effective_negatives": 37428, "method_flow_methods": 23756, "failed_witnesses": 9089, "bounded_passing_witnesses": 11365}


def test_negative_register_erases_nothing() -> None:
    register = load("x2/retained-negative-register.json")
    assert register == {"owner": "Vesper Arlen", "phase": "v673-v6", "activation_external_overlay": 37254, "vesper_operational": 14, "executed_rejecting_mutations": 160, "effective_negatives": 37428, "erased": 0, "completion_credit_from_negatives": 0}


def test_open_and_exact_gates_are_additive() -> None:
    register = load("x2/open-exact-gate-register.json")
    assert register["activation"] == {"open_gaps": 301, "exact_gates": 294}
    assert register["new"] == {"open_gaps": 2, "exact_gates": 2}
    assert register["effective"] == {"open_gaps": 303, "exact_gates": 296}
    assert register["silently_closed"] == 0


def test_phase_truth_is_bounded_and_not_stage20() -> None:
    truth = load("x2/phase-truth.json")
    assert truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert truth["declared_proposal_chain"] == {"source": 6430, "new": 40, "result": 6470, "universal_novelty_claim": False}
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["same_owner_evidence"] is True
    assert truth["independent_reproduction"] is False
    assert truth["complete_repository_suite_run"] is False


def test_flashcard_deck_has_four_tiers_and_ten_categories() -> None:
    deck = load("x2/flashcards/deck.json")
    assert deck["card_count"] == len(deck["cards"]) == 50
    assert len(deck["tiers"]) == 4
    assert len(deck["categories"]) == 10


def test_all_x2_json_parses() -> None:
    paths = sorted((OUT / "x2").rglob("*.json"))
    assert len(paths) >= 60
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_no_private_patterns_in_public_x2_text() -> None:
    forbidden = ["source_" + "thread_id", "C:" + "\\Users\\", "private_" + "transcript"]
    for path in [p for p in (OUT / "x2").rglob("*") if p.is_file()]:
        text = path.read_text(encoding="utf-8")
        assert all(term not in text for term in forbidden)


def test_evidence_manifest_when_finalized() -> None:
    manifest = load("validation/evidence-manifest.json")
    if manifest.get("state") == "PENDING_STAGED_FINALIZATION":
        return
    review = load("validation/x2-staged-review.json")
    privacy = load("validation/x2-staged-privacy.json")
    assert review["state"] == "VALID_X2_EXACT_STAGED_SCOPE"
    assert review["out_of_scope_paths"] == []
    assert review["x1_artifact_modified_paths"] == []
    assert review["x1_compatibility_test_paths"] == ["tests/test_ghc_family_vesper_arlen_v673_v6_x1.py"]
    assert privacy["state"] == "VALID_ZERO_CONFIRMED_PRIVACY_HITS"
    assert privacy["confirmed_hit_count"] == 0
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        blob = git("show", f":{row['path']}")
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest() == row["sha256_normalized_lf"]


def test_x1_commit_remains_direct_parent_during_evidence_build() -> None:
    assert git("rev-parse", "HEAD").decode().strip() == "9a5d432a877d5c11ac60e0d331cf27cfb55c482b"
    assert not git("status", "--porcelain", "--", "docs/vesper-arlen/v673-v6/x1").decode().strip()


def test_owner_scope_stays_below_file_ceiling() -> None:
    owner_files = [path for path in OUT.rglob("*") if path.is_file()]
    assert 0 < len(owner_files) < 2000
