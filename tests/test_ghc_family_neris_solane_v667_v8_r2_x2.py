from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from collections import Counter
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_r2_x2.py"
SPEC = importlib.util.spec_from_file_location("_neris_v667_v8_r2_x2", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load Neris x2 builder")
x2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(x2)


class NerisSolaneV667V8R2X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = x2.validate_tree()
        cls.root = x2.PHASE_ROOT
        cls.outcomes = json.loads((cls.root / "x2/proposal-outcomes.json").read_text(encoding="utf-8"))
        cls.mutations = json.loads((cls.root / "x2/rejecting-mutations.json").read_text(encoding="utf-8"))
        cls.revalidations = json.loads((cls.root / "x2/selected-revalidation-summary.json").read_text(encoding="utf-8"))
        cls.tools = json.loads((cls.root / "x2/tooling/thirteen-tool-transaction-receipt.json").read_text(encoding="utf-8"))
        cls.toolchain = json.loads((cls.root / "x2/tooling/toolchain-transaction-receipt.json").read_text(encoding="utf-8"))
        cls.skills = json.loads((cls.root / "x2/skills-summary.json").read_text(encoding="utf-8"))
        cls.runners = json.loads((cls.root / "x2/runners-summary.json").read_text(encoding="utf-8"))
        cls.portfolio = json.loads((cls.root / "x2/portfolio-execution.json").read_text(encoding="utf-8"))["execution"]
        cls.flow = json.loads((cls.root / "method-flow/x2-method-flow-ledger.json").read_text(encoding="utf-8"))
        cls.route = json.loads((cls.root / "x2/route-state.json").read_text(encoding="utf-8"))

    def test_01_tree_validates(self) -> None:
        self.assertEqual(self.summary["status"], "PASS")

    def test_02_exact_x1(self) -> None:
        receipt = json.loads((self.root / "x2/x2-build-receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["x1"], x2.X1_COMMIT)

    def test_03_outcome_count(self) -> None:
        self.assertEqual(len(self.outcomes["outcomes"]), 20)

    def test_04_four_truth_labels(self) -> None:
        self.assertEqual(
            Counter(row["outcome"] for row in self.outcomes["outcomes"]),
            Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}),
        )
        self.assertEqual(self.outcomes["allowed_core_outcomes"], x2.ALLOWED_OUTCOMES)

    def test_05_all_positives_pass(self) -> None:
        self.assertTrue(all(row["positive_passed"] for row in self.outcomes["outcomes"]))

    def test_06_completed_credit_only(self) -> None:
        for row in self.outcomes["outcomes"]:
            self.assertEqual(row["completion_credit"], 1 if row["outcome"] == "completed" else 0)

    def test_07_mutation_count(self) -> None:
        self.assertEqual(self.mutations["mutation_count"], 100)
        self.assertEqual(self.mutations["rejected_count"], 100)

    def test_08_mutation_reasons(self) -> None:
        self.assertTrue(all(row["rejected"] and row["observed_reason"] == row["expected_reason"] for row in self.mutations["mutations"]))

    def test_09_mutation_zero_credit(self) -> None:
        self.assertTrue(all(row["completion_credit"] == 0 for row in self.mutations["mutations"]))

    def test_10_selected_revalidation(self) -> None:
        self.assertEqual(self.revalidations["count"], 20)
        self.assertEqual(self.revalidations["passing_count"], 20)
        self.assertEqual(self.revalidations["completion_credit"], 0)

    def test_11_tool_composite_state(self) -> None:
        self.assertEqual(self.tools["status"], "PASS")
        self.assertEqual(self.tools["direct_tool_count"], 13)
        self.assertEqual(self.tools["pre_remediation_advisory_entries"], 14)

    def test_12_top_level_hashes(self) -> None:
        self.assertTrue(self.tools["top_level_hashes_valid"])
        self.assertEqual(self.tools["wheel_count"], 50)

    def test_13_dependency_and_audit(self) -> None:
        self.assertEqual(self.toolchain["pip_check"]["core"], "No broken requirements found.")
        self.assertEqual(self.toolchain["pip_check"]["wheel-inspect"], "No broken requirements found.")
        self.assertEqual(self.tools["audit_known_vulnerability_count"], 0)

    def test_14_tool_smokes(self) -> None:
        self.assertEqual(self.tools["positive_smoke_count"], 13)
        self.assertEqual(self.tools["negative_rejection_count"], 13)

    def test_15_tool_failure_retained(self) -> None:
        self.assertEqual(len(self.tools["operational_failures"]), 8)
        self.assertEqual(self.tools["operational_recovery_count"], 8)
        self.assertEqual(self.tools["successful_transaction_replay_count"], 0)

    def test_16_deck_count(self) -> None:
        deck = json.loads((self.root / "deck/deck-index.json").read_text(encoding="utf-8"))
        self.assertEqual(deck["card_count"], 320)
        self.assertEqual(deck["tiers"], {"tier1": 40, "tier2": 80, "tier3": 100, "tier4": 100})

    def test_17_deck_files(self) -> None:
        self.assertEqual(len(list((self.root / "deck/cards").rglob("*.json"))), 320)

    def test_18_card_truth_labels(self) -> None:
        for path in (self.root / "deck/cards").rglob("*.json"):
            self.assertIn(json.loads(path.read_text(encoding="utf-8"))["status"], x2.ALLOWED_OUTCOMES)

    def test_19_skills(self) -> None:
        self.assertEqual((self.skills["built"], self.skills["validated"], self.skills["used"]), (10, 10, 10))
        self.assertEqual(self.skills["global_install_count"], 10)

    def test_20_runners(self) -> None:
        self.assertEqual((self.runners["built"], self.runners["validated"], self.runners["used"]), (10, 10, 10))
        self.assertTrue(self.runners["family_current_compatible"])

    def test_21_safe_now_portfolio(self) -> None:
        self.assertEqual(len(self.portfolio["owner_safe_now"]), 30)
        self.assertTrue(all(row["outcome"] == "completed" for row in self.portfolio["owner_safe_now"]))

    def test_22_candidate_portfolio(self) -> None:
        self.assertEqual(len(self.portfolio["owner_candidates"]), 15)
        self.assertTrue(all(row["outcome"] == "represented" for row in self.portfolio["owner_candidates"]))

    def test_23_clean_fix_refine(self) -> None:
        self.assertEqual(len(self.portfolio["owner_clean_fix_refine"]), 30)
        self.assertTrue(all(row["outcome"] == "completed" for row in self.portfolio["owner_clean_fix_refine"]))

    def test_24_successor_recommendations_unexecuted(self) -> None:
        for key in ("successor_safe_now_recommendations", "successor_candidate_recommendations", "successor_skill_recommendations", "successor_runner_recommendations", "successor_clean_fix_refine_recommendations"):
            self.assertTrue(all(row["execution_state"] == "preserved_unexecuted_zero_credit" for row in self.portfolio[key]))

    def test_25_exact_and_blocked_unexecuted(self) -> None:
        for key in ("exact_approval_packets", "blocked_packets"):
            self.assertTrue(all(row["execution_state"] == "preserved_unexecuted_zero_credit" for row in self.portfolio[key]))

    def test_26_method_baseline(self) -> None:
        self.assertEqual(self.flow["activation_baseline"]["effective_negatives"], 28434)
        self.assertEqual(self.flow["activation_baseline"]["methods"], 14710)

    def test_27_method_candidate(self) -> None:
        self.assertEqual(self.flow["evidence_candidate"], {"effective_negatives": 28580, "methods": 14991, "open_gaps": 202, "exact_gates": 200, "failed_witnesses": 864, "passing_witnesses": 1576})

    def test_28_route_stop(self) -> None:
        self.assertFalse(self.route["name_conflict"])
        self.assertEqual(self.route["state"], "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2")
        self.assertEqual(self.route["delivery"], "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2")
        self.assertFalse(self.route["successor_contacted"])

    def test_29_authority_zeroes(self) -> None:
        authority = json.loads((self.root / "x2/authority-boundary.json").read_text(encoding="utf-8"))
        for key, value in authority.items():
            if key.startswith("real_") or key.endswith("_decisions") or key in {"keys_proofs_credentials", "professional_signoffs", "independent_reproductions"}:
                self.assertEqual(value, 0)

    def test_30_report_size(self) -> None:
        self.assertGreaterEqual(self.summary["report_words"], 2500)

    def test_31_manifests(self) -> None:
        immutable = json.loads((self.root / "validation/immutable-x1-manifest.json").read_text(encoding="utf-8"))
        evidence = json.loads((self.root / "validation/evidence-content-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(immutable["entry_count"], 23)
        self.assertEqual(evidence["entry_count"], len(evidence["entries"]))

    def test_32_privacy_and_file_ceiling(self) -> None:
        self.assertEqual(self.summary["privacy_candidates"], 0)
        self.assertLess(self.summary["owner_files"], 2000)

    def test_33_no_final_lifecycle(self) -> None:
        self.assertFalse((self.root / "closeout").exists())
        self.assertFalse((self.root / "seal").exists())
        self.assertFalse((self.root / "handoffs").exists())

    def test_34_terminal_verdict(self) -> None:
        self.assertEqual(self.outcomes["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_35_global_skill_overlays(self) -> None:
        promotion = json.loads((self.root / "x2/global-skill-promotion-receipt.json").read_text(encoding="utf-8"))
        overlays = json.loads((self.root / "x2/global-family-skill-overlay-receipt.json").read_text(encoding="utf-8"))
        self.assertEqual((promotion["status"], promotion["skill_count"], promotion["validated_count"]), ("PASS", 10, 10))
        self.assertEqual((overlays["status"], overlays["skill_count"], overlays["initial_locale_failure_count"], overlays["utf8_validation_pass_count"]), ("PASS_UTF8_DEPENDENCY_CORRECTED", 6, 5, 6))


if __name__ == "__main__":
    unittest.main()
