from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs/vesper-arlen/v669-v8"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
COUNTS = {
    "effective_negatives": 31854,
    "methods": 17959,
    "failed_witnesses": 3675,
    "passing_witnesses": 4931,
    "open_gaps": 239,
    "exact_gates": 234,
}


def load(relpath: str):
    return json.loads((PHASE_ROOT / relpath).read_text(encoding="utf-8"))


class VesperV669V8FinalTests(unittest.TestCase):
    def test_phase_truth_preserves_exact_counts_outcomes_and_verdict(self) -> None:
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["outcomes"], OUTCOMES)
        self.assertEqual({key: truth[key] for key in COUNTS}, COUNTS)
        self.assertEqual(truth["proposal_chain"], 5230)
        self.assertEqual(truth["canonical_invocation_state"], "PREPARED_NOT_INVOKED")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["real_world_actions"], 0)

    def test_completion_checklist_keeps_protected_work_incomplete(self) -> None:
        checklist = load("closeout/complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(checklist["completed"]), 10)
        self.assertGreaterEqual(len(checklist["incomplete"]), 6)
        joined = " ".join(checklist["incomplete"])
        for token in ("professional", "Maori-authority", "independent reproduction", "Stage 20", "successor delivery"):
            self.assertIn(token, joined)

    def test_frozen_portfolio_has_all_owner_floors_and_three_practices(self) -> None:
        portfolio = load("x1/portfolio-freeze.json")
        self.assertEqual(
            portfolio["counts"],
            {
                "safe_now": 60,
                "candidate": 30,
                "exact_approval": 20,
                "blocked": 10,
                "skill": 20,
                "runner": 10,
                "clean_fix_refine": 60,
            },
        )
        self.assertEqual(len(portfolio["practices"]), 3)
        self.assertTrue(all("boundary" in row and "lens" in row for row in portfolio["practices"]))

    def test_successor_portfolio_has_exact_recommendation_floors(self) -> None:
        successor = load("x1/successor-recommendations-freeze.json")
        self.assertEqual(successor["counts"], {"skill": 10, "runner": 10, "clean_fix_refine": 30})
        self.assertEqual(successor["prospective_successor"], "Lyren Moss")
        self.assertEqual(successor["prospective_phase"], "v670-v1")
        self.assertEqual(successor["completion_credit"], 0)
        self.assertIn("grain-milling", successor["practice_recommendation"]["practice"])

    def test_portfolio_execution_completes_bounded_work_and_holds_gates(self) -> None:
        expected = {
            "safe_now": (60, "completed"),
            "candidate": (30, "completed"),
            "skill": (20, "completed"),
            "runner": (10, "completed"),
            "clean_fix_refine": (60, "completed"),
            "exact_approval": (20, "held_unexecuted"),
            "blocked": (10, "held_unexecuted"),
        }
        for kind, (count, state) in expected.items():
            payload = load(f"x2/portfolio-execution/{kind}.json")
            self.assertEqual(len(payload["rows"]), count)
            self.assertEqual({row["execution_state"] for row in payload["rows"]}, {state})
            self.assertTrue(all(row["external_actions"] == 0 for row in payload["rows"]))

    def test_outcome_ledger_uses_only_the_four_allowed_labels(self) -> None:
        ledger = load("x2/outcome-ledger.json")
        self.assertEqual(ledger["totals"], OUTCOMES)
        self.assertEqual(len(ledger["rows"]), 40)
        self.assertEqual({row["observed_disposition"] for row in ledger["rows"]}, set(OUTCOMES))

    def test_all_160_invalid_mutations_are_rejected_at_zero_credit(self) -> None:
        rows = []
        for path in sorted((PHASE_ROOT / "x2/mutations").glob("*.json")):
            rows.extend(json.loads(path.read_text(encoding="utf-8"))["rows"])
        self.assertEqual(len(rows), 160)
        self.assertTrue(all(row["expected"] == "reject" for row in rows))
        self.assertTrue(all(row["passed"] and not row["decision"]["accepted"] for row in rows))
        self.assertTrue(all(row["completion_credit"] == 0 for row in rows))
        self.assertEqual(
            {row["kind"] for row in rows},
            {"missing_required_state", "ambiguous_domain_or_unit", "real_world_or_external_action", "protected_claim_promotion"},
        )

    def test_flashcard_deck_has_four_tiers_and_ten_paragraphs_per_card(self) -> None:
        deck = load("x2/flashcard-deck.json")
        self.assertEqual(deck["card_count"], 40)
        self.assertEqual(len(deck["rows"]), 40)
        self.assertEqual(len(deck["tier_order"]), 4)
        self.assertTrue(all(len(row["paragraphs"]) == 10 for row in deck["rows"]))
        self.assertTrue(all(row["tier_1_freed_id"].startswith("Vesper Arlen") for row in deck["rows"]))

    def test_isolated_toolchain_receipt_has_three_exact_direct_packages(self) -> None:
        receipt = load("tools/isolated-toolchain-install-receipt.json")
        self.assertTrue(receipt["passed"])
        self.assertEqual(receipt["direct_packages"], ["pint==0.25.3", "transitions==0.9.3", "portion==2.6.2"])
        self.assertEqual(len(receipt["direct_hash_checks"]), 3)
        self.assertTrue(all(row["passed"] and row["expected_sha256"] == row["observed_sha256"] for row in receipt["direct_hash_checks"]))
        self.assertEqual(receipt["download_exit_code"], 0)
        self.assertEqual(receipt["install_exit_code"], 0)
        self.assertEqual(receipt["pip_audit"]["exit_code"], 0)

    def test_bandit_receipt_preserves_module_absence_and_command_success(self) -> None:
        receipt = load("tools/bandit-high-severity-receipt.json")
        self.assertFalse(receipt["module_entrypoint_available_in_active_python"])
        self.assertEqual(receipt["command_version"], "bandit 1.9.4")
        self.assertEqual(receipt["file_count"], 13)
        self.assertEqual(receipt["high_severity_findings"], 0)
        self.assertTrue(receipt["passed"])

    def test_method_flow_retains_all_failures_and_witness_counts(self) -> None:
        flow = load("closeout/method-flow-final.json")
        failures = load("closeout/final-operational-failures.json")
        self.assertEqual(flow["methods"], COUNTS["methods"])
        self.assertEqual(flow["failed_witnesses"], COUNTS["failed_witnesses"])
        self.assertEqual(flow["bounded_passing_witnesses"], COUNTS["passing_witnesses"])
        self.assertEqual(failures["count"], 4)
        self.assertTrue(all(row["completion_credit"] == 0 for row in failures["rows"]))
        self.assertTrue(all(row["passing_bounded_witness"] for row in failures["rows"]))
        self.assertEqual(len(load("x1/startup-operational-failures.json")["rows"]), 12)
        self.assertEqual(len(load("x2/x2-operational-failures.json")["rows"]), 5)

    def test_final_overview_is_three_page_equivalent_and_nonpromotional(self) -> None:
        text = (PHASE_ROOT / "closeout/final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 1600)
        for token in ("NOT_READY_FOR_STAGE_20", "THOS Body", "synthetic", "independent reproduction"):
            self.assertIn(token, text)

    def test_static_report_has_structural_accessibility_and_no_script(self) -> None:
        text = (PHASE_ROOT / "x2/accessible-evidence-report.html").read_text(encoding="utf-8")
        for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"'):
            self.assertIn(token, text)
        self.assertNotIn("<script", text.lower())

    def test_baton_integrity_word_bounds_and_pre_send_truth(self) -> None:
        path = PHASE_ROOT / "handoffs/lyren-moss-v670-v1-activation-candidate.md"
        data = path.read_bytes()
        normalized = data.decode("utf-8").replace("\r\n", "\n").rstrip() + "\n"
        receipt = load("handoffs/activation-candidate-integrity.json")
        self.assertGreaterEqual(receipt["word_count"], 10000)
        self.assertLessEqual(receipt["word_count"], 100000)
        self.assertEqual(receipt["word_count"], len(normalized.split()))
        self.assertEqual(receipt["sha256_normalized_lf"], hashlib.sha256(normalized.encode("utf-8")).hexdigest())
        self.assertEqual(receipt["delivery_state"], "PREPARED_NOT_SENT")
        self.assertFalse(receipt["delivery_acknowledged"])

    def test_route_seal_and_canonical_state_do_not_preclaim_success(self) -> None:
        route = load("orchestration/route-state-final-candidate.json")
        seal = load("seal/seal-candidate.json")
        canonical = load("final/canonical-invocation-state.json")
        correction = load("final/terminal-correction.json")
        prerequisites = load("final/final-validation-prerequisites.json")
        self.assertEqual(route["delivery_state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["successor_contact_count"], 0)
        self.assertFalse(route["app_acknowledgement"])
        self.assertEqual(seal["canonical_state"], "PREPARED_NOT_INVOKED")
        self.assertEqual(canonical["attempt_count"], 0)
        self.assertTrue(canonical["no_success_replay"])
        self.assertEqual(correction["initial_final_state"], "RETAINED_NON_TERMINAL_ZERO_CANONICAL_CREDIT")
        self.assertEqual(correction["canonical_invocations_before_correction"], 0)
        self.assertTrue(prerequisites["one_attributable_invocation"])
        self.assertTrue(prerequisites["external_receipt_required"])
        self.assertFalse(prerequisites["complete_repository_suite"])

    def test_all_phase_json_and_document_ceilings(self) -> None:
        files = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
        self.assertLess(len(files), 2000)
        json_paths = [path for path in files if path.suffix.lower() == ".json"]
        self.assertGreaterEqual(len(json_paths), 190)
        for path in json_paths:
            json.loads(path.read_text(encoding="utf-8"))
        for path in files:
            if path.suffix.lower() in {".json", ".md", ".html", ".txt"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, str(path))


if __name__ == "__main__":
    unittest.main()
