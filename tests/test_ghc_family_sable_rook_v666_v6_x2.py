from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_sable_rook_v666_v6_runtime import (  # noqa: E402
    ALLOWED_LABELS,
    PHASE_ROOT,
    X1_SHA,
    changed_python_files,
    load_json,
    proposal_directories,
    replay_manifest,
    scan_privacy,
    scan_python_security,
    text_files,
    validate_contract,
)


def load(relative: str) -> dict:
    return load_json(PHASE_ROOT / relative)


class SableRookV666V6X2Tests(unittest.TestCase):
    def test_01_frozen_slate_remains_exact(self) -> None:
        freeze = load("x1/proposal-freeze.json")
        self.assertEqual(freeze["inherited_frozen_baseline"], 4270)
        self.assertEqual(freeze["new_frozen_total"], 4290)
        self.assertEqual(len(freeze["new_proposals"]), 20)
        self.assertFalse(freeze["outcomes_observed"])

    def test_02_outcome_ledger_uses_only_four_labels(self) -> None:
        ledger = load("x2/proposal-ledger.json")
        self.assertEqual(
            ledger["outcome_counts"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual({row["outcome"] for row in ledger["proposals"]}, set(ALLOWED_LABELS))
        self.assertEqual(ledger["unknown_labels"], [])
        self.assertEqual(ledger["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_03_exactly_twenty_contract_triplets_exist(self) -> None:
        directories = proposal_directories()
        self.assertEqual(len(directories), 20)
        for directory in directories:
            self.assertTrue((directory / "contract.json").is_file())
            self.assertTrue((directory / "mutation-results.json").is_file())
            self.assertTrue((directory / "bounded-receipt.json").is_file())

    def test_04_all_one_hundred_mutations_are_rejected(self) -> None:
        rows = [load_json(directory / "mutation-results.json") for directory in proposal_directories()]
        self.assertEqual(sum(row["mutation_count"] for row in rows), 100)
        self.assertEqual(sum(row["rejected_count"] for row in rows), 100)
        self.assertTrue(all(row["all_rejected"] for row in rows))
        self.assertTrue(all(row["aggregate_credit"] == 0 for row in rows))

    def test_05_every_contract_is_synthetic_zero_person_zero_action(self) -> None:
        for directory in proposal_directories():
            contract = load_json(directory / "contract.json")
            self.assertTrue(contract["synthetic_fixture"])
            self.assertEqual(contract["real_data_rows"], 0)
            self.assertEqual(contract["participant_count"], 0)
            self.assertEqual(contract["network_calls"], 0)
            self.assertEqual(contract["external_actions"], 0)
            self.assertEqual(contract["positive_fixture"]["authority_state"], "withheld")
            self.assertEqual(contract["positive_fixture"]["real_material_state"], "absent")

    def test_06_open_gap_is_zero_call_adapter_only(self) -> None:
        rows = [
            row for row in load("x2/proposal-ledger.json")["proposals"] if row["outcome"] == "open_gap"
        ]
        self.assertEqual(len(rows), 1)
        self.assertIn("zero-call", rows[0]["title"])
        adapter = load("x2/source-adapter-zero-call.json")
        self.assertFalse(adapter["transport_enabled"])
        self.assertEqual(adapter["network_calls"], 0)
        self.assertEqual(adapter["rows_received"], 0)
        self.assertEqual(adapter["writes"], 0)

    def test_07_exact_gate_is_authority_docket_only(self) -> None:
        rows = [
            row for row in load("x2/proposal-ledger.json")["proposals"] if row["outcome"] == "exact_gate"
        ]
        self.assertEqual(len(rows), 1)
        self.assertIn("Māori-authority", rows[0]["title"])
        self.assertIn("benefit sharing", rows[0]["title"])

    def test_08_owner_portfolio_execution_is_bounded(self) -> None:
        portfolio = load("x2/portfolio-execution.json")
        self.assertEqual(portfolio["method_count"], 95)
        self.assertEqual(portfolio["external_actions"], 0)
        self.assertEqual(portfolio["real_data_rows"], 0)
        self.assertEqual(portfolio["participant_count"], 0)
        self.assertEqual(portfolio["protected_items_executed"], 0)
        self.assertTrue(
            all(
                row["completion_credit"] == "bounded_owner_local"
                for row in portfolio["executed_groups"]["owner_safe_now"]
            )
        )
        self.assertTrue(
            all(
                row["completion_credit"] == "representation_only"
                for row in portfolio["executed_groups"]["owner_bounded_candidates"]
            )
        )

    def test_09_exact_and_blocked_packets_remain_unexecuted(self) -> None:
        register = load("x2/exact-and-blocked-register.json")
        self.assertEqual(register["exact_approval_count"], 10)
        self.assertEqual(register["blocked_count"], 5)
        self.assertEqual(register["executed_count"], 0)
        self.assertTrue(
            all(
                row["x2_status"] == "unexecuted_protected"
                for row in register["exact_approval_packets"] + register["blocked_packets"]
            )
        )

    def test_10_ten_skills_are_built_tested_read_and_used(self) -> None:
        catalog = load("x2/skill-catalog.json")
        self.assertEqual(catalog["skill_count"], 10)
        self.assertTrue(catalog["all_built_tested_used_bounded"])
        self.assertTrue(all(row["smoke_status"] == "passed" for row in catalog["skills"]))
        for row in catalog["skills"]:
            self.assertTrue((ROOT / row["path"]).is_file())
            receipt = load(f"skills/{row['name']}/smoke-receipt.json")
            self.assertTrue(receipt["read_through_eof_before_bounded_use"])
            self.assertTrue(receipt["valid"])

    def test_11_ten_family_current_runners_pass_smoke(self) -> None:
        catalog = load("x2/runner-catalog.json")
        self.assertEqual(catalog["runner_count"], 10)
        self.assertTrue(catalog["family_current_names"])
        self.assertTrue(catalog["all_smoke_passed"])
        self.assertTrue(all(row["name"].startswith("ghc_family_") for row in catalog["runners"]))
        self.assertTrue(all(row["smoke_status"] == "passed" for row in catalog["runners"]))

    def test_12_terminal_runners_were_probe_only(self) -> None:
        receipt = load("x2/tooling-smoke-receipt.json")
        self.assertFalse(receipt["closeout_invoked"])
        self.assertFalse(receipt["canonical_aggregate_invoked"])
        terminal = [row for row in receipt["results"] if row["name"] in {"closeout", "canonical"}]
        self.assertEqual(len(terminal), 2)
        self.assertTrue(all(not row["terminal_work_invoked"] for row in terminal))
        self.assertTrue(all(row["payload"]["probe_only"] for row in terminal))

    def test_13_core_method_flow_reconciles_exactly(self) -> None:
        flow = load("method-flow/x2-method-flow.json")
        self.assertEqual(flow["starting_effective_negatives"], 26649)
        self.assertEqual(flow["starting_effective_methods"], 11421)
        self.assertEqual(flow["new_negative_count"], 100)
        self.assertEqual(flow["new_method_count"], 215)
        self.assertEqual(flow["effective_after_x2_negatives"], 26749)
        self.assertEqual(flow["effective_after_x2_methods"], 11636)
        self.assertEqual(len(flow["rows"]), 215)
        self.assertTrue(flow["all_failures_retained"])

    def test_14_operational_overlay_retains_ambiguous_wrapper(self) -> None:
        overlay = load("method-flow/x2-operational-overlay.json")
        self.assertEqual(overlay["new_negative_count"], 8)
        self.assertEqual(overlay["new_method_count"], 8)
        self.assertEqual(overlay["effective_negatives"], 26757)
        self.assertEqual(overlay["effective_methods"], 11644)
        self.assertEqual(len(overlay["rows"]), 8)
        self.assertTrue(all(row["aggregate_credit"] == 0 for row in overlay["rows"]))
        self.assertTrue(overlay["no_failure_erased"])

    def test_15_open_gap_and_exact_gate_totals_advance_once(self) -> None:
        register = load("x2/open-gate-register.json")
        self.assertEqual(register["inherited_open_gap_count"], 187)
        self.assertEqual(register["inherited_exact_gate_count"], 185)
        self.assertEqual(len(register["new_open_gaps"]), 1)
        self.assertEqual(len(register["new_exact_gates"]), 1)
        self.assertEqual(register["effective_open_gap_count"], 188)
        self.assertEqual(register["effective_exact_gate_count"], 186)

    def test_16_accessible_report_passes_structure_only(self) -> None:
        text = (PHASE_ROOT / "reports" / "static-report.html").read_text(encoding="utf-8")
        for token in (
            'lang="en-NZ"',
            "<main",
            "<caption>",
            'scope="col"',
            'scope="row"',
            "NOT_READY_FOR_STAGE_20",
            "@media print",
        ):
            self.assertIn(token, text)
        self.assertIn("affected-user evaluation remain reserved", text)
        self.assertNotIn("accessibility complete", text.casefold())

    def test_17_five_class_privacy_scan_is_clear(self) -> None:
        receipt = scan_privacy(text_files())
        self.assertEqual(len(receipt["classes"]), 5)
        self.assertEqual(receipt["confirmed_hit_count"], 0)
        self.assertTrue(receipt["valid"])

    def test_18_changed_python_security_scan_is_bounded_and_clear(self) -> None:
        receipt = scan_python_security(changed_python_files())
        self.assertGreaterEqual(receipt["scanned_python_count"], 15)
        self.assertEqual(receipt["finding_count"], 0)
        self.assertTrue(receipt["valid"])

    def test_19_x1_manifest_replays_at_immutable_x1(self) -> None:
        result = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
        self.assertEqual(result["entry_count"], 20)
        self.assertEqual(result["failure_count"], 0)
        self.assertTrue(result["valid"])

    def test_20_immutable_x1_contains_no_later_lifecycle_paths(self) -> None:
        receipt = load("x2/x1-immutability-receipt.json")
        self.assertTrue(receipt["valid"])
        self.assertFalse(receipt["x1_modified"])
        self.assertTrue(all(value == 0 for value in receipt["later_lifecycle_path_counts_at_x1"].values()))
        for relative in ("x2", "evidence", "closeout", "seal", "final", "handoffs"):
            output = subprocess.check_output(
                [
                    "git",
                    "-C",
                    str(ROOT),
                    "ls-tree",
                    "-r",
                    "--name-only",
                    X1_SHA,
                    "--",
                    f"docs/sable-rook/v666-v6/{relative}",
                ]
            ).decode("utf-8")
            self.assertEqual(output, "", relative)

    def test_21_route_remains_prepared_not_sent(self) -> None:
        candidate = load("x2/terminal-candidates.json")
        self.assertTrue(candidate["candidates_only"])
        self.assertFalse(candidate["successor_contacted"])
        self.assertIsNone(candidate["successor_title"])
        self.assertIsNone(candidate["successor_phase"])
        self.assertIn("PREPARED_NOT_SENT", candidate["route"])

    def test_22_deck_is_exact_and_non_promoting(self) -> None:
        index = load("deck/deck-index.json")
        model = load("deck/model-validation.json")
        manifest = load("deck/card-manifest.json")
        self.assertEqual(index["card_count"], 25)
        self.assertEqual(index["tier_counts"], {"1": 1, "2": 3, "3": 1, "4": 20})
        self.assertEqual(index["core_outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(manifest["entry_count"], 25)
        self.assertTrue(model["valid"])
        self.assertFalse(index["successor"]["contacted"])

    def test_23_source_use_is_zero_ingest_and_nonconverting(self) -> None:
        ledger = load("x2/source-use-ledger.json")
        self.assertEqual(ledger["source_count"], 8)
        self.assertEqual(ledger["generated_phase_network_calls"], 0)
        self.assertEqual(ledger["real_rows_ingested"], 0)
        self.assertTrue(all(row["authority_nonconversion"] for row in ledger["rows"]))

    def test_24_inherited_revalidation_has_zero_current_credit(self) -> None:
        receipt = load("x2/revalidation/inherited-contract-integrity.json")
        self.assertEqual(receipt["row_count"], 20)
        self.assertTrue(receipt["all_match"])
        self.assertEqual(receipt["current_completion_credit"], 0)
        self.assertTrue(all(row["novelty_credit"] == 0 for row in receipt["rows"]))
        self.assertTrue(all(row["automatic_completion_credit"] == 0 for row in receipt["rows"]))

    def test_25_phase_truth_preserves_all_boundaries(self) -> None:
        truth = load("x2/phase-truth.json")
        self.assertEqual(truth["proposal_chain_total"], 4290)
        self.assertEqual(truth["effective_negatives_with_operational_overlay"], 26757)
        self.assertEqual(truth["effective_methods_with_operational_overlay"], 11644)
        self.assertEqual(truth["open_gaps"], 188)
        self.assertEqual(truth["exact_gates"], 186)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["same_owner_validation_is_independent_reproduction"])

    def test_26_documents_remain_utf8_lf_and_within_caps(self) -> None:
        paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
        self.assertLessEqual(len(paths), 2000)
        for path in paths:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
            self.assertNotIn("\r", text, path)
            self.assertLessEqual(len(re.findall(r"\S+", text)), 100000, path)


def _contract_test(index: int):
    def test(self: SableRookV666V6X2Tests) -> None:
        proposal_id = f"SR6666-N{index:03d}"
        contract = load_json(
            PHASE_ROOT / "x2" / "proposals" / proposal_id.casefold() / "contract.json"
        )
        valid, errors = validate_contract(contract)
        self.assertTrue(valid, errors)
        self.assertEqual(contract["proposal_id"], proposal_id)

    return test


def _mutation_test(index: int):
    def test(self: SableRookV666V6X2Tests) -> None:
        proposal_id = f"SR6666-N{index:03d}"
        receipt = load_json(
            PHASE_ROOT
            / "x2"
            / "proposals"
            / proposal_id.casefold()
            / "mutation-results.json"
        )
        self.assertEqual(receipt["mutation_count"], 5)
        self.assertEqual(receipt["rejected_count"], 5)
        self.assertEqual(
            [row["class"] for row in receipt["mutations"]],
            [
                "missing_required_field",
                "wrong_type_or_invalid_range",
                "provenance_or_authority_smuggling",
                "real_world_or_production_action",
                "outcome_or_conformance_promotion",
            ],
        )

    return test


for _index in range(1, 21):
    setattr(
        SableRookV666V6X2Tests,
        f"test_{26 + _index:02d}_contract_{_index:03d}",
        _contract_test(_index),
    )
    setattr(
        SableRookV666V6X2Tests,
        f"test_{46 + _index:02d}_mutations_{_index:03d}",
        _mutation_test(_index),
    )


if __name__ == "__main__":
    unittest.main()
