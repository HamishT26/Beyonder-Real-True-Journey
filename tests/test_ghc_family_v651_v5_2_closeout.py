import json
import re
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v651-v5-2-remaster"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class EirenV651V5RemasterCloseoutTests(unittest.TestCase):
    def test_final_truth(self):
        truth = load("final/phase-truth.json")
        self.assertEqual(truth["outcome_counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["effective_negatives"], 7219)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_gates_and_failures_are_retained(self):
        negatives = load("final/retained-negative-register.json")
        self.assertTrue(negatives["no_failure_erased"])
        self.assertEqual(negatives["effective"], 7219)
        gates = load("final/gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 56)
        self.assertEqual(gates["effective_exact_gates"], 57)
        self.assertEqual(gates["silently_closed"], 0)

    def test_baton_contract_and_route(self):
        path = ROOT / "handoffs/elaren-kestrel-v651-v6-activation.md"
        text = path.read_text(encoding="utf-8")
        words = len(re.findall(r"\b[\w'-]+\b", text))
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertIn("PREPARED_NOT_SENT_AT_COMMIT", text)
        route = load("orchestration/final-orchestration.json")
        self.assertEqual(route["target_exact_title"], "Elaren Kestrel")
        self.assertEqual(route["target_phase"], "v651-v6")
        self.assertEqual(route["send_count"], 0)

    def test_no_cli_sibling_and_no_task_creation(self):
        route = load("orchestration/final-orchestration.json")
        self.assertEqual(route["cli_siblings_spawned"], 0)
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["collaboration_subagent"])

    def test_overview_and_static_report(self):
        overview = (ROOT / "overview/final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", overview)), 1500)
        report = (ROOT / "reports/final-static-report.html").read_text(encoding="utf-8")
        self.assertIn("Manual keyboard", report)
        self.assertIn("affected-user", report)
        self.assertIn("external exact-final receipt", report)

    def test_validation_plan_is_single_pass(self):
        plan = load("validation/final-validation-plan.json")
        self.assertTrue(plan["complete_repository_suite"])
        self.assertEqual(plan["credited_successful_aggregate_limit"], 1)
        self.assertFalse(plan["post_success_replay"])
        self.assertFalse(plan["detached_or_named_replay"])

    def test_environment_was_observed_only(self):
        environment = load("final/environment-receipt.json")
        self.assertEqual(environment["codex_cli"], "0.144.5")
        self.assertTrue(environment["versions_verified_only"])
        self.assertFalse(environment["desktop_updated"])
        self.assertFalse(environment["host_security_changed"])

    def test_final_manifest_contracts_exist(self):
        delta = load("validation/final-delta-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        review = load("validation/final-staged-review.json")
        self.assertGreater(delta["entry_count"], 0)
        self.assertGreater(owner["entry_count"], 0)
        self.assertEqual(len(delta["self_exclusions"]), 5)
        self.assertEqual(len(owner["self_exclusions"]), 5)
        self.assertTrue(review["valid"])

    def test_final_delta_manifest_is_cumulative_through_staged_correction(self):
        evidence = "c67ce592463450ccf9aee7d460210cddb467c5ca"
        committed = set(filter(None, subprocess.check_output(["git", "diff", "--name-only", evidence, "HEAD"], cwd=REPO, text=True, encoding="utf-8").splitlines()))
        staged = set(filter(None, subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=REPO, text=True, encoding="utf-8").splitlines()))
        manifest = load("validation/final-delta-manifest.json")
        declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
        self.assertEqual(declared, committed | staged)


if __name__ == "__main__":
    unittest.main()
