from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.ghc_family_elowen_cairn_v667_v3_core import validate_contract


PHASE_ROOT = ROOT / "docs" / "elowen-cairn" / "v667-v3"


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


class ElowenCairnV667V3X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outcomes = load("x2/proposal-outcomes.json")
        cls.mutations = load("x2/rejecting-mutations.json")
        cls.evidence = load("evidence/immutable-evidence-candidate.json")
        cls.portfolio = load("x2/portfolio-execution.json")
        cls.method = load("method-flow/x2-method-flow-ledger.json")

    def test_01_twenty_contract_directories_exist(self):
        paths = list((PHASE_ROOT / "x2" / "proposals").glob("*/contract.json"))
        self.assertEqual(len(paths), 20)

    def test_02_all_positive_contracts_validate(self):
        for index in range(1, 21):
            contract = load(f"x2/proposals/ec6673-n{index:03d}/contract.json")
            self.assertEqual(validate_contract(contract), [], contract["proposal_id"])

    def test_03_core_outcome_counts_are_exact(self):
        self.assertEqual(
            self.outcomes["counts"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(len(self.outcomes["outcomes"]), 20)

    def test_04_only_four_core_labels_are_used(self):
        labels = {row["final_disposition"] for row in self.outcomes["outcomes"]}
        self.assertEqual(labels, {"completed", "represented", "open_gap", "exact_gate"})

    def test_05_all_one_hundred_mutations_are_rejected(self):
        self.assertEqual(self.mutations["mutation_count"], 100)
        self.assertEqual(self.mutations["accepted_mutation_count"], 0)
        self.assertTrue(all(not row["accepted"] for row in self.mutations["mutations"]))

    def test_06_mutation_classes_fail_closed(self):
        observed = {failure for row in self.mutations["mutations"] for failure in row["validator_failures"]}
        self.assertTrue(
            {
                "missing_required_node",
                "wrong_type_or_invalid_range",
                "provenance_or_authority_smuggling",
                "real_world_or_production_action",
                "outcome_or_conformance_promotion",
            }.issubset(observed)
        )

    def test_07_all_counts_remain_zero_real_world(self):
        for index in range(1, 21):
            contract = load(f"x2/proposals/ec6673-n{index:03d}/contract.json")
            self.assertEqual(contract["participant_count"], 0)
            self.assertEqual(contract["real_data_row_count"], 0)
            self.assertEqual(contract["network_call_count"], 0)
            self.assertEqual(contract["key_count"], 0)
            self.assertEqual(contract["proof_count"], 0)

    def test_08_adapter_is_disabled_and_zero_row(self):
        adapter = load("x2/adapter/vam-api-v2-zero-row-adapter.json")
        self.assertFalse(adapter["transport_enabled"])
        self.assertEqual(adapter["request_count"], 0)
        self.assertEqual(adapter["download_count"], 0)
        self.assertEqual(adapter["row_count"], 0)
        self.assertEqual(adapter["status"], "open_gap")

    def test_09_exact_gate_is_unexecuted(self):
        gate = load("evidence/exact-gate-register.json")
        self.assertEqual(gate["new_count"], 1)
        self.assertFalse(gate["new_rows"][0]["executed"])

    def test_10_ten_phase_local_skills_have_frontmatter(self):
        skills = list((PHASE_ROOT / "x2" / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 10)
        for path in skills:
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\nname:"))
            self.assertIn("\ndescription:", text)
            self.assertIn("## Stop conditions", text)

    def test_11_ten_runner_smokes_pass(self):
        receipts = list((PHASE_ROOT / "x2" / "runner-smoke").glob("*.json"))
        self.assertEqual(len(receipts), 10)
        self.assertTrue(all(json.loads(path.read_text(encoding="utf-8"))["passed"] for path in receipts))

    def test_12_owner_portfolio_execution_is_exact(self):
        self.assertEqual(self.portfolio["executed_count"], 95)
        self.assertTrue(all(row["external_action_count"] == 0 for row in self.portfolio["executed_rows"]))

    def test_13_successor_exact_and_blocked_items_are_not_executed(self):
        self.assertTrue(
            all(
                row["status"] in {"recommendation_only_not_executed", "protected_unexecuted"}
                for row in self.portfolio["held_rows"]
            )
        )
        self.assertTrue(all(row["completion_credit"] == 0 for row in self.portfolio["held_rows"]))

    def test_14_method_flow_has_all_rows_and_retains_failures(self):
        self.assertEqual(self.method["phase_method_count"], 222)
        self.assertEqual(self.method["effective_method_count"], 12792)
        self.assertEqual(self.method["phase_failed_witness_count"], 107)
        self.assertTrue(self.method["valid"])
        self.assertTrue(all(not row["failure_erased"] for row in self.method["rows"]))

    def test_15_negative_gap_and_gate_counts_are_additive(self):
        negatives = load("evidence/retained-negative-register.json")
        gaps = load("evidence/open-gap-register.json")
        gates = load("evidence/exact-gate-register.json")
        self.assertEqual(negatives["effective_count"], 27330)
        self.assertEqual(negatives["failure_erased_count"], 0)
        self.assertEqual(gaps["effective_count"], 193)
        self.assertEqual(gates["effective_count"], 191)

    def test_16_evidence_boundary_and_verdict_are_exact(self):
        self.assertEqual(self.evidence["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(self.evidence["same_owner_only"])
        self.assertEqual(self.evidence["real_people"], 0)
        self.assertEqual(self.evidence["real_objects"], 0)
        self.assertEqual(self.evidence["network_calls"], 0)
        self.assertEqual(self.evidence["external_actions"], 0)

    def test_17_static_report_has_structural_accessibility(self):
        text = (PHASE_ROOT / "x2" / "static-report.html").read_text(encoding="utf-8")
        for token in ("<h1>", "<main>", "<section", "<table>", "<caption>", "scope='row'", "scope=\"col\""):
            self.assertIn(token, text)
        self.assertIn("Manual browser, assistive-technology", text)

    def test_18_all_phase_json_documents_parse(self):
        parsed = 0
        for path in PHASE_ROOT.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))
            parsed += 1
        self.assertGreaterEqual(parsed, 90)


if __name__ == "__main__":
    unittest.main()
