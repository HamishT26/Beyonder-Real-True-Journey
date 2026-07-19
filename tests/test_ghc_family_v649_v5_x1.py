import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / "v649-v5"


def load(relative):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class TestV649V5X1(unittest.TestCase):
    def test_phase_truth_is_x1_only(self):
        truth = load("phase-truth.json")
        self.assertEqual(truth["stage"], "x1_frozen_not_executed")
        self.assertFalse(truth["x2_started"])
        self.assertIsNone(truth["observed_distribution"])

    def test_exact_proposals_and_total(self):
        packet = load("x1-proposals.json")
        self.assertEqual(packet["new_proposal_count"], 10)
        self.assertEqual(packet["frozen_total_after_x1"], 690)
        self.assertEqual(len(packet["proposals"]), 10)

    def test_required_fields(self):
        required = {"hypothesis","null_or_failure_condition","approval_class","execution_lane","source_needs","artifacts","falsifier_or_acceptance_gate","rollback_or_recovery","protected_gates","expected_disposition"}
        for row in load("x1-proposals.json")["proposals"]:
            self.assertTrue(required.issubset(row))

    def test_exact_expected_distribution(self):
        rows = load("x1-proposals.json")["proposals"]
        counts = {key:sum(row["expected_disposition"] == key for row in rows) for key in ["completed","represented","open_gap","exact_gate"]}
        self.assertEqual(counts, {"completed":6,"represented":2,"open_gap":1,"exact_gate":1})

    def test_unique_ids_and_titles(self):
        rows = load("x1-proposals.json")["proposals"]
        self.assertEqual(len({row["proposal_id"] for row in rows}), 10)
        self.assertEqual(len({row["title"] for row in rows}), 10)

    def test_novelty_audit(self):
        audit = load("provenance/proposal-collision-audit.json")
        self.assertEqual(audit["prior_count"], 680)
        self.assertEqual(len(audit["rows"]), 10)
        self.assertLess(audit["maximum_observed_jaccard"], audit["threshold"])

    def test_frozen_index(self):
        index = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual((index["prior_count"], index["new_count"], index["count"]), (680, 10, 690))

    def test_source_statuses(self):
        ledger = load("sources/source-ledger.json")
        self.assertEqual(ledger["allowed_statuses"], ["current","stable","draft","watch"])
        self.assertEqual(sum(ledger["status_counts"].values()), len(ledger["sources"]))
        self.assertTrue(all(row["not_observation"] for row in ledger["sources"]))

    def test_portfolio_floors(self):
        self.assertEqual(load("approval-packets/x1-safe-now-portfolio.json")["count"], 30)
        self.assertEqual(load("prototypes/x1-candidate-plan.json")["count"], 20)
        plan = load("prototypes/x1-skill-runner-plan.json")
        self.assertEqual((plan["skill_count"], plan["runner_count"]), (20, 10))
        self.assertEqual(load("maintenance/x1-clean-refine-plan.json")["count"], 30)

    def test_mutations_frozen_not_run(self):
        plan = load("validation/x1-synthetic-mutation-plan.json")
        self.assertEqual((plan["count"], plan["executed_count"], plan["rejected_count"]), (70,0,0))
        self.assertFalse(any(row["executed"] for row in plan["mutations"]))

    def test_negatives_retained(self):
        register = load("retained-negative-register.json")
        self.assertEqual(register["inherited_effective"], 5025)
        self.assertEqual(register["x1_operational"], 7)
        self.assertFalse(register["negative_erased"])

    def test_gates_not_closed(self):
        gates = load("exact-open-gate-register.json")
        self.assertEqual((gates["inherited_open_gaps"], gates["inherited_exact_gates"]), (38,39))
        self.assertEqual(gates["closed_in_x1"], 0)

    def test_method_flow(self):
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertEqual(len(ledger["methods"]), 7)
        self.assertEqual(len(ledger["witnesses"]), 14)
        self.assertEqual(sum(row["result"] == "fail" for row in ledger["witnesses"]), 7)
        self.assertEqual(sum(row["result"] == "pass" for row in ledger["witnesses"]), 7)

    def test_privacy(self):
        receipt = load("validation/x1-staged-privacy.json")
        self.assertEqual(len(receipt["pattern_classes"]), 5)
        self.assertEqual(receipt["confirmed_hit_count"], 0)

    def test_manifest(self):
        manifest = load("validation/x1-staged-manifest.json")
        self.assertGreater(manifest["entry_count"], 20)
        self.assertEqual(len(manifest["self_exclusions"]), 3)

    def test_staged_review(self):
        review = load("validation/x1-staged-review.json")
        self.assertTrue(review["x1_only"])
        self.assertEqual(review["x2_implementation_paths"], [])
        self.assertEqual(review["x2_outcome_paths"], [])

    def test_route_not_sent(self):
        self.assertEqual(load("orchestration/phase-state.json")["terminal_route"], "PREPARED_NOT_SENT")

    def test_identity_boundary(self):
        identity = load("identity-receipt.json")
        self.assertIn("Relational working language only", identity["identity_boundary"])
        self.assertIn("Hamish", identity["corrigibility"])

    def test_no_platform_action(self):
        startup = load("environment/startup-receipt.json")
        self.assertFalse(startup["sandbox_or_hyperv_action"])
        self.assertFalse(startup["cross_platform_message_action"])

    def test_document_caps(self):
        for path in PHASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 6000, path)


if __name__ == "__main__":
    unittest.main()
