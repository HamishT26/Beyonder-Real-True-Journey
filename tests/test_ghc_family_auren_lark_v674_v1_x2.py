from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v674-v1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"


def load(relative: str) -> dict:
    return json.loads((X2 / relative).read_text(encoding="utf-8"))


def test_strict_x1_gate_is_exact_and_precedes_x2():
    gate = load("lifecycle/x1-gate.json")
    assert gate["state"] == "VALID_STRICT_PLANNING_ONLY_X1_GATE"
    assert gate["source"] == "3ba783297438ee89d5778065e30de737af470855"
    assert gate["x1_commit"] == "763969929943d9c9bcb674999508fe33694fa357"
    assert gate["x1_parent"] == gate["source"]
    assert gate["four_way_equal"] is True
    assert gate["x2_paths_in_frozen_x1"] == 0


def test_sixty_outcomes_use_only_four_labels():
    ledger = load("proposals/outcome-ledger.json")
    assert ledger["proposal_count"] == 60
    assert ledger["proposal_chain"] == 6610
    assert ledger["outcomes"] == {
        "completed": 42,
        "represented": 12,
        "open_gap": 3,
        "exact_gate": 3,
    }
    assert set(ledger["allowed_outcomes"]) == {"completed", "represented", "open_gap", "exact_gate"}
    assert ledger["universal_novelty_claim"] is False


def test_each_proposal_has_exact_evidence_file():
    files = sorted((X2 / "proposals").glob("al6741-n*.json"))
    assert len(files) == 60
    rows = [json.loads(path.read_text(encoding="utf-8")) for path in files]
    assert len({row["proposal_id"] for row in rows}) == 60
    assert all(row["synthetic_only"] and not row["external_action"] for row in rows)
    assert sum(row["completion_credit"] for row in rows) == 42


def test_positive_and_invalid_controls_are_retained():
    positive = load("fixtures/positive-control-ledger.json")
    invalid = load("fixtures/invalid-mutation-ledger.json")
    assert positive["count"] == 60
    assert all(row["accepted"] for row in positive["rows"])
    assert invalid["count"] == 240
    assert invalid["all_rejected"] is True
    assert invalid["completion_credit"] == 0
    assert all(row["failed_input_witness_retained"] for row in invalid["rows"])


def test_portfolio_counts_and_protected_holds():
    owner = load("portfolios/owner-execution.json")
    holds = load("portfolios/protected-holds.json")
    successor = load("portfolios/successor-recommendations.json")
    assert owner["safe_now_count"] == 120
    assert owner["candidate_count"] == 80
    assert owner["clean_fix_refine_count"] == 100
    assert len(holds["exact_approval"]) == 20
    assert len(holds["blocked"]) == 10
    assert all(row["observed_state"] == "held_unexecuted" for row in holds["exact_approval"])
    assert all(row["observed_state"] == "blocked_unexecuted" for row in holds["blocked"])
    assert len(successor["candidate_recommendations"]) == 20
    assert len(successor["clean_fix_refine_recommendations"]) == 30
    assert successor["auren_completion_credit"] == 0
    assert successor["precontact"] is False


def test_practice_is_wholly_synthetic_and_provenance_is_acyclic():
    stations = load("practice/synthetic-station-register.json")
    uncertainty = load("practice/calibration-uncertainty-board.json")
    provenance = load("practice/provenance-dag.json")
    correction = load("practice/model-discrepancy-and-correction.json")
    assert len(stations["records"]) == 12
    assert stations["real_stations"] == 0
    assert stations["coordinates_present"] is False
    assert len(uncertainty["records"]) == 12
    assert uncertainty["measurement_result"] is False
    assert provenance["acyclic"] is True
    assert provenance["endorsement"] is False
    assert correction["empirical_credit"] == 0
    assert correction["scientific_authority"] is False


def test_direct_tools_integrities_smokes_audit_and_cli():
    receipt = load("packages/transaction-receipt.json")
    assert receipt["direct_python_count"] == 7
    assert receipt["direct_node_count"] == 6
    assert receipt["direct_total"] == 13
    assert all(row["hash_match"] and row["used"] for row in receipt["python"])
    assert all(row["lock_integrity_match"] and row["used"] for row in receipt["node"])
    assert len(receipt["runtime_dependencies"]) == 3
    assert receipt["node_override"]["version"] == "3.1.1"
    assert receipt["post_override_audit_vulnerabilities"]["total"] == 0
    assert receipt["codex_cli"]["version"] == "codex-cli 0.150.1"
    assert receipt["codex_cli"]["desktop_app_mutated"] is False
    assert all(receipt["python_functional_smokes"].values())
    assert receipt["node_functional_smokes"]["ajv_cli"]["accept_exit"] == 0
    assert receipt["node_functional_smokes"]["ajv_cli"]["reject_exit"] != 0
    assert receipt["node_functional_smokes"]["cspell"]["accept_exit"] == 0
    assert receipt["node_functional_smokes"]["cspell"]["reject_exit"] != 0
    assert receipt["node_functional_smokes"]["html_validate"]["accept_exit"] == 0
    assert receipt["node_functional_smokes"]["html_validate"]["reject_exit"] != 0


def test_twenty_skills_and_ten_runners_were_validated_and_used():
    bank = load("tools/phase-local-tool-bank.json")
    assert bank["skill_count"] == 20
    assert bank["runner_count"] == 10
    assert all(row["quick_validation"] == "passed" and row["tested"] and row["used"] for row in bank["skills"])
    assert all(row["accepting_exit"] == 0 and row["rejecting_exit"] != 0 for row in bank["runners"])
    assert len(bank["successor_skill_recommendations"]) == 10
    assert len(bank["successor_runner_recommendations"]) == 10


def test_skill_cards_have_exact_frontmatter():
    bank = load("tools/phase-local-tool-bank.json")
    for row in bank["skills"]:
        text = (ROOT / row["path"]).read_text(encoding="utf-8")
        assert text.startswith(f"---\nname: {row['name']}\n")
        assert "\ndescription:" in text.split("---", 2)[1]


def test_generated_runners_are_family_named_and_present():
    bank = load("tools/phase-local-tool-bank.json")
    for row in bank["runners"]:
        assert row["name"].startswith("ghc_family_seismic_")
        assert row["name"].endswith("_runner.py")
        assert (ROOT / row["path"]).is_file()


def test_four_tier_flashcard_deck_has_eighteen_categories():
    deck = load("flashcards/four-tier-deck.json")
    assert deck["category_count"] == 18
    assert len(deck["cards"]) == 18
    assert deck["identity_claim"] is False
    assert all(len(row["sensitive_fields"]) == 0 for row in deck["cards"])


def test_route_candidate_is_not_sent_and_carries_successor_reminder():
    route = load("route/sable-candidate.json")
    assert route["target_exact_title"] == "Sable Rook"
    assert route["target_phase"] == "v674-v2"
    assert route["state"] == "PROSPECTIVE_NOT_SENT"
    assert route["send_attempts"] == 0
    assert "Caelen Ash v674-v3" in route["recipient_successor_reminder"]


def test_method_flow_retains_failures_and_effective_truth():
    ledger = load("method-flow/ledger.json")
    truth = load("phase-truth.json")
    assert ledger["x2_operational_failure_count"] == 38
    assert ledger["invalid_mutation_count"] == 240
    assert all(row["success_credit"] == 0 for row in ledger["x2_operational_failures"])
    assert ledger["effective_counts"] == truth["effective_counts"]
    assert truth["outcomes"] == {
        "completed": 42,
        "represented": 12,
        "open_gap": 3,
        "exact_gate": 3,
    }
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["independent_reproduction"] is False
    assert truth["theory_of_everything_proof"] is False


def test_privacy_security_and_owner_scope_are_bounded():
    privacy = json.loads((VALIDATION / "x2-bounded-privacy.json").read_text(encoding="utf-8"))
    security = json.loads((VALIDATION / "x2-bounded-security.json").read_text(encoding="utf-8"))
    scope = json.loads((VALIDATION / "x2-owner-scope.json").read_text(encoding="utf-8"))
    assert privacy["confirmed_hits"] == 0
    assert privacy["complete_privacy_claim"] is False
    assert security["finding_count"] == 0
    assert security["exhaustive_security_claim"] is False
    assert scope["below_ceiling"] is True
    assert scope["owner_path_count"] < 2000
    assert scope["source_or_sibling_mutations"] == 0
    assert scope["deletions"] == 0


def test_owner_manifest_replays_working_bytes():
    manifest = load("owner-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    assert "docs/auren-lark/v674-v1/validation/x2-evidence-manifest.json" in manifest["cycle_exclusions"]
    for row in manifest["entries"]:
        path = ROOT / row["path"]
        assert path.is_file()
        assert path.stat().st_size == row["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256_working_bytes"]


def test_all_phase_json_files_parse_strictly():
    files = sorted(BASE.rglob("*.json"))
    assert len(files) >= 90
    for path in files:
        json.loads(path.read_text(encoding="utf-8"))


def test_global_action_receipt_is_planned_or_exactly_complete():
    receipt = load("global-actions/receipt.json")
    assert receipt["state"] in {
        "PLANNED_NOT_EXECUTED",
        "COMPLETE_EXACT_LOCAL_GLOBAL_BYTE_PARITY",
    }
    if receipt["state"] == "COMPLETE_EXACT_LOCAL_GLOBAL_BYTE_PARITY":
        assert receipt["global_skill_count"] == 10
        assert receipt["overlay_count"] == 7
        assert receipt["memory_note_count"] == 1
        bank = load("tools/phase-local-tool-bank.json")
        assert sum(row["global_installation"] for row in bank["skills"]) == 10
