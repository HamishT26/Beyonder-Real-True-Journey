from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from scripts.ghc_family_v647_v7_runtime import SURFACES, accepts, baseline, surface_evidence


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v647-v7"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V647V7EvidenceTests(unittest.TestCase):
    def test_all_surface_baselines_pass(self):
        for surface in SURFACES:
            accepted, reasons = accepts(surface, baseline(surface))
            self.assertTrue(accepted, (surface, reasons))

    def test_every_surface_rejects_seven_mutations(self):
        rows = [surface_evidence(surface) for surface in SURFACES]
        self.assertEqual(70, sum(row["rejected_mutation_count"] for row in rows))
        self.assertTrue(all(item["rejected"] and item["retained"] for row in rows for item in row["mutations"]))

    def test_outcome_distribution(self):
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), Counter(row["outcome"] for row in ledger["proposals"]))
        self.assertEqual(["completed", "represented", "open_gap", "exact_gate"], ledger["allowed_outcomes"])

    def test_x1_seal_has_no_mismatch(self):
        seal = load("reproduction/x1-content-seal.json")
        self.assertEqual("54bc352a9d57f81229261f0894e3affd35fc7ebc", seal["x1_commit"])
        self.assertEqual(0, seal["mismatch_count"])
        self.assertTrue(all(row["equal"] for row in seal["entries"]))

    def test_zero_row_and_zero_authority_boundaries(self):
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(0, ledger["real_rows"])
        self.assertEqual(0, ledger["real_people_or_properties"])
        self.assertEqual(0, ledger["real_keys_tokens_or_servers"])
        self.assertEqual(0, ledger["authority_decisions"])

    def test_expanded_portfolios_execute_inside_bounds(self):
        approval = load("approval-packets/x2-portfolio-execution.json")
        candidates = load("prototypes/x2-candidate-execution.json")
        skills = load("prototypes/skill-build-use-receipt.json")
        runners = load("prototypes/runner-build-use-receipt.json")
        cleanup = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((30, 20, 20, 10, 30), (approval["safe_now_completed"], candidates["built_count"], skills["validated_count"], runners["runner_count"], cleanup["completed_count"]))
        self.assertEqual(0, approval["exact_executed"])
        self.assertEqual(0, approval["blocked_executed"])
        self.assertGreaterEqual(runners["invoked_count"], 9)

    def test_all_skills_are_phase_local_validated_and_used(self):
        receipt = load("prototypes/skill-build-use-receipt.json")
        self.assertEqual(20, receipt["skill_count"])
        self.assertTrue(all(row["initialized_with_skill_creator"] and row["validated_with_quick_validate"] and row["smoke_used"] and not row["installed_globally"] for row in receipt["skills"]))

    def test_negative_and_gate_counts(self):
        negatives = load("retained-negative-register-x2.json")
        gates = load("exact-open-gate-register-x2.json")
        self.assertEqual(3745, negatives["effective_total"])
        self.assertEqual(0, negatives["erased_negative_count"])
        self.assertEqual((24, 25), (gates["effective_open_gaps"], gates["effective_exact_gates"]))

    def test_static_report_reserves_manual_accessibility(self):
        text = (PHASE / "deliverables/v647-v7-static-report.html").read_text(encoding="utf-8").casefold()
        for needle in ("skip to evidence", "<caption>", "scope=\"col\"", "manual keyboard", "not a complete accessibility claim"):
            self.assertIn(needle, text)

    def test_terminal_state_is_not_ready_and_route_is_held(self):
        truth = load("phase-truth.json")
        route = load("orchestration/terminal-route-plan.json")
        self.assertEqual("NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])
        self.assertEqual("PREPARED_NOT_SENT", truth["route_state"])
        self.assertEqual("PREPARED_NOT_SENT", route["state"])


if __name__ == "__main__":
    unittest.main()
