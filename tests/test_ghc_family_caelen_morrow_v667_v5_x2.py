from __future__ import annotations

import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts.ghc_family_caelen_morrow_v667_v5_core import MODEL_NODES, PHASE_ROOT, ROOT, validate_contract


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


class CaelenMorrowV667V5X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.outcomes = load("x2/proposal-outcomes.json")
        cls.mutations = load("x2/rejecting-mutations.json")
        cls.registry = load("x2/skill-runner-registry.json")
        cls.portfolio = load("x2/portfolio-execution.json")
        cls.evidence = load("evidence/immutable-evidence-candidate.json")
        cls.negatives = load("evidence/retained-negative-register.json")
        cls.methods = load("method-flow/x2-method-flow-ledger.json")
        cls.gaps = load("evidence/open-gap-register.json")
        cls.gates = load("evidence/exact-gate-register.json")
        cls.flashcards = load("x2/flashcards/execution-receipts.json")

    def test_twenty_positive_contracts_validate(self) -> None:
        self.assertEqual(20, len(MODEL_NODES))
        for proposal_id in MODEL_NODES:
            contract = load(f"x2/proposals/{proposal_id.casefold()}/contract.json")
            self.assertEqual([], validate_contract(contract), proposal_id)
            self.assertTrue(contract["synthetic_only"])
            self.assertIsNone(contract["navigation_output"])

    def test_one_hundred_preregistered_mutations_are_rejected(self) -> None:
        self.assertEqual(100, self.mutations["mutation_count"])
        self.assertEqual(0, self.mutations["accepted_mutation_count"])
        self.assertEqual(100, self.mutations["retained_zero_credit_count"])
        self.assertTrue(all(not row["accepted"] and row["failed_witness_retained"] for row in self.mutations["mutations"]))
        self.assertTrue(all(row["validator_failures"] for row in self.mutations["mutations"]))

    def test_outcomes_use_exact_four_label_partition(self) -> None:
        self.assertEqual({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}, self.outcomes["counts"])
        counts = Counter(row["final_disposition"] for row in self.outcomes["outcomes"])
        self.assertEqual(self.outcomes["counts"], dict(counts))
        self.assertEqual("NOT_READY_FOR_STAGE_20", self.outcomes["terminal_verdict"])

    def test_zero_real_or_operational_counts(self) -> None:
        for key in ["real_people", "real_vessels", "real_voyages", "real_observations", "real_instruments", "real_almanac_values", "real_times", "real_angles", "real_coordinates", "real_positions", "real_routes", "network_calls", "downloads", "keys", "proofs", "external_actions"]:
            self.assertEqual(0, self.evidence[key], key)
        self.assertTrue(self.evidence["same_owner_only"])

    def test_flashcard_deck_and_mutations(self) -> None:
        self.assertEqual(233, self.flashcards["build"]["result"]["card_count"])
        self.assertEqual(13, self.flashcards["build"]["result"]["section_count"])
        self.assertTrue(all(row["passed"] for row in self.flashcards.values()))
        mutation = load("x2/flashcards/mutation-receipt.json")
        self.assertEqual(60, mutation["mutation_count"])
        self.assertEqual(60, mutation["rejected_count"])
        self.assertTrue(all(row["rejected"] for row in mutation["cases"]))

    def test_ten_phase_local_skills_are_complete_and_not_installed(self) -> None:
        self.assertEqual(10, self.registry["skill_count"])
        self.assertEqual(10, self.registry["skill_smoke_passes"])
        self.assertEqual(0, self.registry["global_install_count"])
        for row in self.registry["skills"]:
            path = ROOT / row["path"]
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith(f"---\nname: {row['name']}\n"))
            self.assertNotIn("TODO", text)
            self.assertFalse(row["global_install"])
            self.assertTrue(row["initialized_with_supported_skill_creator"])

    def test_ten_family_current_runners_smoke_pass(self) -> None:
        self.assertEqual(10, self.registry["runner_count"])
        self.assertEqual(10, self.registry["runner_smoke_passes"])
        for kind in ["core", "sight", "temporal", "angular", "corrections", "provenance", "identity", "adapter", "validation", "canonical"]:
            row = load(f"x2/runner-smoke/{kind}.json")
            self.assertTrue(row["passed"], kind)
            self.assertEqual(0, row["exit_code"])

    def test_portfolio_executes_ninety_five_and_holds_one_hundred(self) -> None:
        self.assertEqual(95, self.portfolio["executed_count"])
        self.assertEqual(100, self.portfolio["held_count"])
        self.assertEqual(0, self.portfolio["external_action_count"])
        self.assertTrue(all(row["completion_credit"] == 0 for row in self.portfolio["held_rows"]))

    def test_method_flow_retains_every_failure_and_recovery(self) -> None:
        self.assertEqual(291, self.methods["phase_method_count"])
        self.assertEqual(13404, self.methods["effective_method_count"])
        self.assertEqual(176, self.methods["phase_failed_witness_count"])
        self.assertEqual(291, self.methods["phase_bounded_passing_witness_count"])
        self.assertTrue(self.methods["valid"])
        self.assertTrue(all(not row["failure_erased"] for row in self.methods["rows"]))

    def test_negative_gap_and_gate_accounting(self) -> None:
        self.assertEqual(176, self.negatives["phase_additive_count"])
        self.assertEqual(27712, self.negatives["effective_count"])
        self.assertEqual(0, self.negatives["failure_erased_count"])
        self.assertEqual(195, self.gaps["effective_count"])
        self.assertEqual(193, self.gates["effective_count"])
        self.assertFalse(self.gates["new_rows"][0]["executed"])

    def test_skill_creator_quick_validation_retains_failed_first_attempt(self) -> None:
        receipt = load("validation/skill-quick-validation-receipt.json")
        self.assertEqual(10, receipt["first_attempt"]["failed_count"])
        self.assertEqual(0, receipt["first_attempt"]["success_credit"])
        self.assertEqual(10, receipt["recovery"]["passed_count"])
        self.assertEqual(0, receipt["recovery"]["failed_count"])
        self.assertFalse(receipt["full_x2_builder_replayed"])
        self.assertEqual(10, self.registry["supported_quick_validate"]["utf8_recovery_passed_package_count"])

    def test_disabled_almanac_adapter_is_open_gap(self) -> None:
        adapter = load("x2/adapter/linz-usno-almanac-zero-row.json")
        self.assertFalse(adapter["transport_enabled"])
        self.assertEqual(0, adapter["request_count"])
        self.assertEqual(0, adapter["download_count"])
        self.assertEqual(0, adapter["row_count"])
        self.assertEqual(0, adapter["almanac_value_count"])
        self.assertEqual("open_gap", adapter["status"])
        self.assertFalse(adapter["navigation_authority_claim"])

    def test_accessible_report_has_structural_landmarks_and_reservations(self) -> None:
        report = (PHASE_ROOT / "reports" / "accessible-report.html").read_text(encoding="utf-8")
        for fragment in ["<!doctype html>", "<html lang=\"en\">", "Skip to main content", "<main id=\"main\">", "<table>", "<caption>", "scope=\"col\"", "NOT_READY_FOR_STAGE_20"]:
            self.assertIn(fragment, report)
        self.assertIn("assistive-technology", report)
        self.assertIn("affected-user evaluation remain reserved", report)

    def test_environment_receipt_is_verify_only(self) -> None:
        receipt = load("environment/version-receipt.json")
        self.assertEqual("verify_only_no_updates_or_installs", receipt["action"])
        self.assertEqual([], receipt["packages_installed"])
        self.assertFalse(receipt["codex_desktop_updated"])
        self.assertFalse(receipt["sandbox_or_hyper_v_changed"])
        self.assertFalse(receipt["host_security_weakened"])
        self.assertFalse(receipt["windows_features_changed"])
        self.assertFalse(receipt["rebooted"])

    def test_x1_commit_tree_remains_immutable(self) -> None:
        changed = subprocess.check_output([
            "git", "-C", str(ROOT), "diff", "--name-only",
            "b7b73cc81266e28ae9cbb1e4c429d2e93be30999", "--", "docs/caelen-morrow/v667-v5/x1",
        ]).decode("utf-8").strip().splitlines()
        self.assertEqual([], changed)

    def test_all_phase_json_parses_and_file_cap_holds(self) -> None:
        files = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
        self.assertLessEqual(len(files), 2000)
        json_files = [path for path in files if path.suffix == ".json"]
        self.assertGreaterEqual(len(json_files), 100)
        for path in json_files:
            json.loads(path.read_text(encoding="utf-8"))

    def test_truth_boundaries_remain_explicit(self) -> None:
        summary = (PHASE_ROOT / "evidence" / "evidence-summary.md").read_text(encoding="utf-8")
        self.assertIn("GMUT Mind is primary", summary)
        self.assertIn("no force, prediction, likelihood", summary)
        self.assertIn("zero-participant", summary)
        self.assertIn("synthetic and nonproduction", summary)
        self.assertIn("Māori authority", summary)
        self.assertIn("NOT_READY_FOR_STAGE_20", summary)


if __name__ == "__main__":
    unittest.main()
