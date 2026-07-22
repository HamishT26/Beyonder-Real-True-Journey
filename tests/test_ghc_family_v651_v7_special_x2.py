from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/vesper-arlen/v651-v7-special-cli-prep"
X1 = "07785aa97b0aa46a4fbf0c60109a8ee8e678aacf"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V651V7SpecialX2Tests(unittest.TestCase):
    def test_core_outcomes_use_only_permitted_vocabulary(self) -> None:
        truth = load("truth/phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["effective_negatives"], 7570)
        self.assertEqual((truth["effective_open_gaps"], truth["effective_exact_gates"]), (59, 60))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_eight_prepare_passes_and_launch_refusals(self) -> None:
        batch = load("cli/cli-batch-receipt.json")
        self.assertEqual((batch["seat_count"], batch["prepare_passes"], batch["launch_refusals"]), (8, 8, 8))
        self.assertTrue(batch["all_unnamed"])
        self.assertTrue(batch["all_unlaunched"])
        self.assertEqual(batch["synthetic_mutations_rejected"], 100)

    def test_future_seat_register_contains_no_identity_or_launch(self) -> None:
        register = load("cli/future-seat-register.json")
        self.assertEqual(register["seat_count"], 8)
        self.assertTrue(register["all_unnamed"] and register["all_unlaunched"])
        for number, row in enumerate(register["seats"], 1):
            self.assertEqual(row["seat"], f"future-cli-sibling-{number}-self-chosen")
            self.assertFalse(row["sibling_created"])
            self.assertEqual(row["identity_state"], "unassigned_self_chosen_at_induction")

    def test_route_coverage_preserves_seven_submitted_candidate_differences(self) -> None:
        receipt = load("cli/route-coverage-receipt.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["difference_count"], 7)
        self.assertTrue(receipt["raw_truth_preserved"])
        self.assertTrue(receipt["candidate_is_advisory"])

    def test_capability_contract_stays_prepared_not_launched(self) -> None:
        receipt = load("cli/capability-contract.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["state"], "PREPARED_NOT_LAUNCHED")
        self.assertTrue(all(receipt["checks"].values()))

    def test_method_flow_retains_two_baton_failures(self) -> None:
        summary = load("method-flow/method-flow-summary.json")
        self.assertEqual(summary["counts"]["methods"], 10)
        self.assertEqual(summary["counts"]["states"]["preferred"], 10)
        self.assertEqual(summary["counts"]["witness_results"], {"fail": 12, "pass": 11})
        self.assertIn("V6517-SPECIAL-M06-WFAIL-2", summary["retained_failed_witnesses"])

    def test_baton_and_pointer_pass_persistent_delivery_guard(self) -> None:
        receipt = load("validation/baton-pointer-guard.json")
        self.assertTrue(receipt["valid"])
        self.assertGreaterEqual(receipt["baton_words"], 10000)
        self.assertLessEqual(receipt["baton_words"], 100000)
        self.assertLessEqual(receipt["pointer_words"], 350)
        self.assertEqual(receipt["privacy_hits"], [])

    def test_portfolios_are_resolved_without_inherited_credit(self) -> None:
        ledger = load("portfolios/execution-ledger.json")
        self.assertEqual((ledger["safe_candidate_count"], ledger["clean_fix_refine_count"]), (50, 30))
        self.assertFalse(ledger["inherited_work_credit"])
        self.assertFalse(ledger["unsafe_work_manufactured"])

    def test_tool_use_is_catalogued_without_bulk_promotion(self) -> None:
        skills = load("skills/skill-use-ledger.json")
        runners = load("runners/runner-use-ledger.json")
        promotion = load("tooling/global-promotion-decision.json")
        self.assertEqual(len(skills["uses"]), 12)
        self.assertEqual(len(runners["uses"]), 10)
        self.assertFalse(promotion["bulk_global_install"])
        self.assertEqual(promotion["promotions"], 0)

    def test_official_sources_do_not_overclaim_account_capability(self) -> None:
        ledger = load("sources/source-ledger.json")
        urls = {row.get("url") for row in ledger["sources"] if row.get("kind") == "official"}
        self.assertIn("https://developers.openai.com/codex/cli/", urls)
        self.assertIn("https://developers.openai.com/api/docs/models/gpt-5.6-sol", urls)
        self.assertIn("future account session", ledger["nonclaim"])

    def test_static_report_has_structural_accessibility_markers(self) -> None:
        text = (PHASE / "reports/accessible-static-report.html").read_text(encoding="utf-8")
        for marker in ("<main>", "<caption>", "scope=\"col\"", ":focus-visible", "@media print", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(marker, text)

    def test_environment_is_verify_only(self) -> None:
        receipt = load("environment/environment-version-receipt.json")
        self.assertEqual(receipt["codex_cli"], "0.145.0")
        self.assertFalse(receipt["desktop_updated"])
        self.assertFalse(receipt["elevation"])
        self.assertFalse(receipt["windows_feature_changed"])
        self.assertEqual(receipt["future_cli_processes_launched"], 0)

    def test_x1_anchor_is_ancestral_and_phase_has_no_private_patterns(self) -> None:
        subprocess.run(["git", "merge-base", "--is-ancestor", X1, "HEAD"], cwd=ROOT, check=True)
        text = (PHASE / "handoffs/ilyra-fen-v651-v8-activation.md").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"(?i)\b[A-Z]:[\\/]", text))
        self.assertNotIn("<" + "codex_delegation", text.lower())


if __name__ == "__main__":
    unittest.main()
