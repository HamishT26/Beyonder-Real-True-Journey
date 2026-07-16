from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v647-v1"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V647V1EvidenceTests(unittest.TestCase):
    def test_core_outcomes(self) -> None:
        rows = load("x2-proposal-ledger.json")["rows"]
        self.assertEqual(len(rows), 10)
        self.assertEqual(Counter(row["outcome"] for row in rows), Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))

    def test_all_mutations_rejected(self) -> None:
        payload = load("validation/preregistered-synthetic-negatives.json")
        self.assertEqual((payload["count"], payload["executed"], payload["rejected"]), (70, 70, 70))
        self.assertTrue(all(row["retained"] and row["observed"] == "reject" for row in payload["rows"]))

    def test_zero_row_adapter(self) -> None:
        fixture = load("empirical/chime-frb-study-contract.json")["positive_fixture"]
        for key in ("downloads", "catalog_rows", "injection_rows", "likelihood_calls", "posterior_samples", "parameter_constraints", "empirical_claims"):
            self.assertEqual(fixture[key], 0)

    def test_represented_surfaces_have_no_real_witnesses(self) -> None:
        thos = load("thos/food-cold-chain-contract.json")["positive_fixture"]
        self.assertEqual((thos["real_people"], thos["real_lots"], thos["real_sensors"], thos["real_actions"]), (0, 0, 0, 0))
        identity = load("freed-id/controlled-identifier-profile.json")["positive_fixture"]
        self.assertFalse(identity["physical_identity_binding"])
        self.assertFalse(identity["production"])

    def test_authority_matrix_is_reserved(self) -> None:
        fixture = load("cbr/food-recall-authority-reservation.json")["positive_fixture"]
        reserved = [value for key, value in fixture.items() if key != "case_data"]
        self.assertTrue(all(value == "reserved" for value in reserved))
        self.assertEqual(fixture["case_data"], "none")

    def test_portfolio_counts(self) -> None:
        self.assertEqual(load("approval-packets/x2-portfolio-execution.json")["completed"], 30)
        self.assertEqual(load("prototypes/x2-candidate-execution.json")["completed"], 20)
        self.assertEqual(load("maintenance/x2-clean-refine-ledger.json")["completed"], 30)

    def test_skills_initialized_validated_and_used(self) -> None:
        receipt = load("skills/skill-build-receipt.json")
        self.assertEqual((receipt["count"], receipt["quick_validated"], receipt["smoke_used"]), (20, 20, 20))
        self.assertEqual(receipt["global_installations"], 0)

    def test_gates_and_terminal_verdict(self) -> None:
        gates = load("exact-open-gate-register.json")
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (18, 19))
        self.assertEqual(load("phase-truth.json")["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_accessibility_reservations(self) -> None:
        contract = load("accessibility/long-form-structure-contract.json")
        self.assertTrue(contract["positive_fixture"]["manual_evaluation_reserved"])
        report = (PHASE / "deliverables" / "v647-v1-static-report.html").read_text(encoding="utf-8")
        self.assertIn("Skip to main evidence", report)
        self.assertIn("<caption>", report)
        self.assertNotIn("http-equiv=\"refresh\"", report.casefold())

    def test_retained_negative_arithmetic(self) -> None:
        negative = load("retained-negative-register.json")
        expected = negative["inherited_effective"] + negative["x1_operational"] + negative["preregistered_synthetic"] + negative["x2_operational"]
        self.assertEqual(negative["effective_total"], expected)
        self.assertTrue(negative["no_negative_erased"])


if __name__ == "__main__":
    unittest.main()
