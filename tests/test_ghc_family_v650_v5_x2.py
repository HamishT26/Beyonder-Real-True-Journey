import json
import sys
import unittest
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v650_v5_phase_data as d
import ghc_family_v650_v5_runtime as runtime

ROOT = REPO / d.PHASE_ROOT


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TamarV650V5X2Tests(unittest.TestCase):
    def test_all_twenty_receipts_pass_in_frozen_classes(self):
        ledger = load("x2-evidence-ledger.json")
        self.assertEqual(ledger["proposal_count"], 20)
        self.assertEqual(
            ledger["distribution"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )
        self.assertTrue(all(row["passed"] for row in ledger["proposals"]))
        self.assertEqual(
            Counter(row["outcome"] for row in ledger["proposals"]),
            Counter(ledger["distribution"]),
        )

    def test_runtime_common_guards_fail_closed(self):
        for kind in [
            "missing_required_obligation",
            "wrong_domain_or_type",
            "unsupported_promotion_attempt",
            "resource_or_iteration_budget_exceeded",
            "negative_or_gate_erasure_attempt",
        ]:
            accepted, reason = runtime.common_check(runtime.mutated_fixture(kind))
            self.assertFalse(accepted, kind)
            self.assertEqual(reason, kind)

    def test_one_hundred_mutations_executed_and_rejected(self):
        results = load("validation/x2-synthetic-mutation-results.json")
        self.assertEqual(results["planned_count"], 100)
        self.assertEqual(results["executed_count"], 100)
        self.assertEqual(results["rejected_or_quarantined_count"], 100)
        self.assertEqual(results["completion_credit"], 0)
        self.assertEqual({row["result"] for row in results["mutations"]}, {"rejected"})

    def test_gmut_formal_and_empirical_boundaries(self):
        for slug in ["cpt-theorem", "appelquist-carazzone", "froissart-martin"]:
            witness = load(f"surfaces/{slug}/bounded-receipt.json")["witness"]
            self.assertTrue(witness["passed"])
        empirical = load("surfaces/exoplanet-zero-row/bounded-receipt.json")
        self.assertEqual(empirical["outcome"], "open_gap")
        witness = empirical["witness"]
        self.assertEqual(witness["downloaded_rows"], 0)
        self.assertEqual(witness["likelihood_evaluations"], 0)
        self.assertEqual(witness["posterior_samples"], 0)
        self.assertEqual(witness["empirical_constraints"], 0)

    def test_identity_thos_and_authority_stay_bounded(self):
        for slug in [
            "oauth-server-metadata",
            "oauth-native-app",
            "jwk-thumbprint-uri",
            "book-conservation-proxy",
        ]:
            receipt = load(f"surfaces/{slug}/bounded-receipt.json")
            self.assertEqual(receipt["outcome"], "represented")
        workshop = load("surfaces/book-conservation-proxy/bounded-receipt.json")["witness"]
        self.assertEqual(workshop["real_objects"], 0)
        self.assertEqual(workshop["real_conservators"], 0)
        self.assertEqual(workshop["blind_matched_budget_arms"], 0)
        authority = load("surfaces/conservation-taonga-authority/bounded-receipt.json")
        self.assertEqual(authority["outcome"], "exact_gate")
        self.assertEqual(set(authority["witness"]["gates"].values()), {"reserved"})
        self.assertEqual(authority["witness"]["software_decisions"], 0)

    def test_completed_structural_surfaces_are_bounded(self):
        slugs = [
            "distributed-lease-fencing", "matroska", "apache-avro", "xor-filter",
            "flac", "krawczyk-operator", "openexr", "accessible-split-action",
            "redlich-kwong-nonconversion", "sccs-nonpromotion", "hpack",
        ]
        for slug in slugs:
            receipt = load(f"surfaces/{slug}/bounded-receipt.json")
            self.assertEqual(receipt["outcome"], "completed")
            self.assertTrue(receipt["passed"])
        accessibility = load("surfaces/accessible-split-action/bounded-receipt.json")["witness"]
        self.assertTrue(accessibility["manual_evaluation_reserved"])
        self.assertTrue(accessibility["affected_user_evaluation_reserved"])
        thermo = load("surfaces/redlich-kwong-nonconversion/bounded-receipt.json")["witness"]
        self.assertFalse(thermo["psyche_conversion"])
        self.assertFalse(thermo["agency_conversion"])
        stage20 = load("surfaces/sccs-nonpromotion/bounded-receipt.json")["witness"]
        self.assertFalse(stage20["stage20_promoted"])

    def test_portfolio_floors_completed(self):
        expected = {
            "safe-now-execution.json": 40,
            "candidate-execution.json": 30,
            "skill-execution.json": 20,
            "runner-execution.json": 10,
            "clean-fix-refine-execution.json": 40,
        }
        for name, count in expected.items():
            receipt = load(f"portfolios/{name}")
            self.assertEqual(receipt["count"], count)
            self.assertEqual(receipt["completed"], count)
        self.assertEqual(load("portfolios/clean-fix-refine-execution.json")["destructive_actions"], 0)

    def test_phase_local_skills_validated_and_smoke_used(self):
        execution = load("portfolios/skill-execution.json")
        self.assertFalse(execution["global_install"])
        self.assertEqual(len(execution["skills"]), 20)
        for row in execution["skills"]:
            package = ROOT / row["package"]
            self.assertTrue((package / "SKILL.md").is_file())
            self.assertTrue((package / "agents/openai.yaml").is_file())
            self.assertTrue((package / "references/contract.md").is_file())
            witness = load(row["witness"])
            self.assertTrue(witness["smoke_passed"])
            self.assertFalse(witness["global_install"])
            self.assertEqual(witness["subagent_forward_test"], "forbidden_by_activation")

    def test_family_current_runners_invoked(self):
        execution = load("portfolios/runner-execution.json")
        self.assertEqual(len(execution["runners"]), 10)
        self.assertTrue(all(row["invoked"] for row in execution["runners"]))
        self.assertTrue(all(row["name"].startswith("ghc_family_") for row in execution["runners"]))
        self.assertTrue(all(not row["independent_reproduction"] for row in execution["runners"]))

    def test_negatives_and_gates_are_not_erased(self):
        negatives = load("retained-negative-register.json")
        self.assertEqual(negatives["activation_baseline"], 5925)
        self.assertEqual(negatives["x1_operational"], 22)
        self.assertEqual(negatives["executed_rejected_synthetic_mutations"], 100)
        self.assertEqual(negatives["x2_operational"], 4)
        self.assertEqual(negatives["effective_total"], 6051)
        self.assertEqual(negatives["erased"], 0)
        gates = load("exact-open-gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 47)
        self.assertEqual(gates["effective_exact_gates"], 48)
        self.assertEqual(gates["silently_closed"], 0)

    def test_phase_truth_and_terminal_verdict(self):
        truth = load("phase-truth.json")
        self.assertEqual(truth["state"], "X2_EVIDENCE_COMPLETE_NOT_SEALED")
        self.assertEqual(truth["effective_negatives"], 6051)
        self.assertTrue(truth["same_owner_repeatability"])
        self.assertFalse(truth["independent_team_reproduction"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "HELD_UNTIL_VERIFIED_FINAL")
        self.assertEqual(route["messages_sent"], 0)

    def test_static_report_has_structural_accessibility_basics(self):
        text = (ROOT / "report.html").read_text(encoding="utf-8")
        for token in [
            '<html lang="en">', 'href="#main"', '<main id="main">',
            '<nav aria-label="Report sections">', '<caption>', '<th scope="col">',
            '<th scope="row">', '<summary>', 'NOT_READY_FOR_STAGE_20',
        ]:
            self.assertIn(token, text)
        self.assertIn("not complete accessibility conformance", text.lower())


if __name__ == "__main__":
    unittest.main()
