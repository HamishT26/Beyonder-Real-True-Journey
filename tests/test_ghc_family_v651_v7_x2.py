from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/vesper-arlen/v651-v7"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class VesperV651V7X2Tests(unittest.TestCase):
    def test_distribution(self) -> None:
        self.assertEqual(load("outcomes/core-outcomes.json")["outcome_counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})

    def test_mutations(self) -> None:
        receipt = load("validation/mutation-execution-receipt.json")
        self.assertEqual((receipt["executed"], receipt["rejected"], receipt["accepted"]), (100, 100, 0))

    def test_negative_accounting(self) -> None:
        register = load("truth/retained-negative-register-x2.json")
        self.assertEqual((register["inherited_effective"], register["x1_operational"], register["x2_operational"], register["synthetic_rejecting_mutations"], register["effective_total"]), (7338, 5, 9, 100, 7452))
        self.assertEqual(register["failures_erased"], 0)

    def test_gates(self) -> None:
        gate = load("gates/exact-open-gate-register.json")
        self.assertEqual((gate["effective_open_gaps"], gate["effective_exact_gates"], gate["silently_closed"]), (59, 60, 0))

    def test_zero_real_world_credit(self) -> None:
        truth = load("truth/evidence-phase-truth.json")
        self.assertEqual((truth["real_data_rows"], truth["participants"], truth["real_keys_or_tokens"], truth["authority_decisions"], truth["production_actions"], truth["future_cli_seats_launched"]), (0, 0, 0, 0, 0, 0))
        self.assertFalse(truth["independent_reproduction"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_portfolios(self) -> None:
        counts = load("portfolios/x2-portfolio-outcomes.json")["counts"]
        self.assertEqual(counts, {"safe_now_completed": 30, "candidate_resolved": 20, "skills_built_validated": 12, "runners_built_invoked": 10, "clean_fix_refine_completed": 30})

    def test_skills(self) -> None:
        receipt = load("tooling/skill-build-receipt.json")
        self.assertEqual((receipt["skill_count"], receipt["initialized"], receipt["quick_validated"], receipt["global_installs"]), (12, 12, 12, 0))
        self.assertTrue(all(row["valid"] for row in receipt["skills"]))

    def test_runners(self) -> None:
        receipt = load("tooling/runner-build-receipt.json")
        self.assertEqual((receipt["runner_count"], receipt["invoked_count"], receipt["unique_surface_coverage"]), (10, 10, 30))
        self.assertFalse(receipt["independent_implementations_claimed"])

    def test_method_flow(self) -> None:
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 14)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 14, "pass": 14})
        self.assertEqual(ledger["counts"]["states"]["preferred"], 14)

    def test_static_report(self) -> None:
        text = (ROOT / "reports/accessible-static-report.html").read_text(encoding="utf-8").casefold()
        for token in ('<html lang="en">', '<main>', '<nav aria-label=', '<caption>', '<th scope="col">', 'manual keyboard', 'not_ready_for_stage_20'):
            self.assertIn(token, text)
        self.assertNotIn("<script", text)

    def test_overview_length(self) -> None:
        text = (ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 2500)
        self.assertLessEqual(len(text.split()), 100000)

    def test_evidence_manifest_shape(self) -> None:
        manifest = load("validation/evidence-staged-manifest.json")
        review = load("validation/evidence-staged-review.json")
        self.assertEqual(manifest["entry_count"] + len(manifest["self_exclusions"]), review["intended_path_count"])
        self.assertEqual(load("validation/evidence-staged-privacy.json")["confirmed_hit_count"], 0)

    def test_detailed_and_minimal(self) -> None:
        from scripts.ghc_family_v651_v7_detailed_validator import validate as detailed
        from scripts.ghc_family_v651_v7_minimal_validator import validate as minimal
        self.assertTrue(detailed()["valid"])
        self.assertTrue(minimal()["valid"])


def make_surface_test(proposal: dict):
    def test(self: VesperV651V7X2Tests) -> None:
        evidence = load(f"proposals/{proposal['slug']}.json")
        self.assertEqual(evidence["proposal_id"], proposal["proposal_id"])
        self.assertEqual(evidence["truth_label"], proposal["expected_disposition"])
        self.assertTrue(evidence["valid_fixture_passed"])
        self.assertIn(evidence["rejected_mutation_count"], {3, 4})
        self.assertFalse(evidence["independent_reproduction"])
        self.assertTrue(all(value is False for value in evidence["protected_claims"].values()))
    return test


for _proposal in load("preregistration/proposals.json")["proposals"]:
    setattr(VesperV651V7X2Tests, f"test_surface_{_proposal['proposal_id'].casefold().replace('-', '_')}", make_surface_test(_proposal))


if __name__ == "__main__":
    unittest.main()
