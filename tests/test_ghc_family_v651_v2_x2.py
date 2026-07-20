import json
import sys
import unittest
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs" / "orin-thale" / "v651-v2"
sys.path.insert(0, str(REPO / "scripts"))
import ghc_family_v651_v2_phase_data as data
from ghc_family_v651_v2_runtime import evaluate


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class V651V2X2Tests(unittest.TestCase):
    def test_exact_outcome_distribution(self):
        ledger = load("outcomes/evidence-ledger.json")
        self.assertEqual(ledger["outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(Counter(row["observed_disposition"] for row in ledger["proposals"]), Counter(ledger["outcome_counts"]))

    def test_all_twenty_accepting_fixtures(self):
        for proposal in data.PROPOSALS:
            contract = load(f"surfaces/{proposal['slug']}/contract.json")
            fixture = load(f"surfaces/{proposal['slug']}/accepting-fixture.json")
            self.assertEqual(evaluate(contract, fixture), (True, []), proposal["proposal_id"])

    def test_all_one_hundred_mutations_rejected(self):
        rows = []
        for proposal in data.PROPOSALS:
            result = load(f"surfaces/{proposal['slug']}/mutation-results.json")
            self.assertEqual(result["rejected_count"], 5)
            rows.extend(result["results"])
        self.assertEqual(len(rows), 100)
        self.assertTrue(all(row["passed"] and row["observed"] == "rejected" for row in rows))

    def test_no_external_evidence_events(self):
        for row in load("outcomes/evidence-ledger.json")["proposals"]:
            self.assertEqual((row["real_rows"], row["real_participants_or_operators"], row["real_keys_or_network_events"], row["authority_decisions"]), (0, 0, 0, 0))

    def test_hubble_remains_zero_row_open_gap(self):
        row = load("truth/x2-open-gap-register.json")
        self.assertEqual(row["current_effective_count"], 52)
        self.assertEqual(row["new_gate"]["state"], "open_gap")
        self.assertEqual(sum(row["new_gate"][key] for key in ("rows", "queries", "downloads", "likelihoods", "posterior_samples")), 0)

    def test_localization_authority_remains_exact_gate(self):
        row = load("truth/x2-exact-gate-register.json")
        self.assertEqual(row["current_effective_count"], 53)
        self.assertEqual(row["new_gate"]["state"], "exact_gate")
        self.assertEqual(sum(value for key, value in row["new_gate"].items() if key.endswith("decisions")), 0)

    def test_portfolio_floors(self):
        self.assertEqual(load("portfolios/safe-now-execution.json")["completed"], 40)
        self.assertEqual(load("portfolios/candidate-execution.json")["completed"], 30)
        cleanup = load("portfolios/clean-fix-refine-execution.json")
        self.assertEqual(cleanup["completed"], 40)
        self.assertFalse(cleanup["deleted_user_material"])
        self.assertFalse(cleanup["sibling_mutation"])

    def test_twenty_skills_validated_and_smoke_used(self):
        summary = load("tooling/skill-validation-summary.json")
        self.assertEqual((summary["initialized"], summary["customized"], summary["official_quick_validated"], summary["smoke_used"]), (20, 20, 20, 20))
        self.assertFalse(summary["global_installation"])
        self.assertFalse(summary["subagent_forward_test"])
        self.assertEqual(len(list((ROOT / "tooling" / "skill-witnesses").glob("*.json"))), 20)

    def test_ten_family_current_runners(self):
        inventory = load("tooling/runner-inventory.json")
        self.assertEqual((inventory["count"], inventory["passed"]), (10, 10))
        self.assertTrue(all(name.startswith("ghc_family_") for name in inventory["planned"]))
        self.assertEqual(len(inventory["witness_paths"]), 10)

    def test_method_flow_retains_failures_and_passes(self):
        summary = load("method-flow/method-flow-summary.json")
        validation = load("method-flow/method-flow-validation.json")
        self.assertGreaterEqual(summary["counts"]["methods"], 13)
        self.assertGreaterEqual(summary["counts"]["witness_results"]["fail"], 13)
        self.assertGreaterEqual(summary["counts"]["witness_results"]["pass"], 13)
        self.assertTrue(summary["valid"] and validation["valid"])

    def test_negative_count_and_zero_erasure(self):
        row = load("truth/x2-retained-negative-register.json")
        self.assertEqual(row["effective_count"], 6679)
        self.assertEqual((row["x1_operational"], row["x2_operational"], row["preregistered_synthetic_rejections"]), (9, 5, 100))
        self.assertEqual(row["erasures"], 0)

    def test_x1_commit_objects_remain_exact(self):
        row = load("provenance/x1-immutability-receipt.json")
        self.assertEqual(row["x1_commit"], "06c5545a79e992537b6307eb6a68e6d01204144d")
        self.assertEqual((row["entry_count"], row["self_exclusion_count"]), (73, 3))
        self.assertTrue(row["immutable_git_object_parity"])
        self.assertEqual(row["issues"], [])

    def test_current_phase_validator(self):
        row = load("validation/x2-current-phase-validation.json")
        self.assertEqual((row["passed_count"], row["check_count"]), (83, 83))
        self.assertEqual(row["mutation_rejected_count"], 100)
        self.assertFalse(row["full_repository_suite_run"])
        self.assertFalse(row["independent_reproduction"])

    def test_source_citations_not_observations(self):
        row = load("sources/source-use-receipt.json")
        self.assertEqual((row["real_rows"], row["queries"], row["downloads"], row["participants"], row["real_keys"], row["network_identity_events"], row["authority_decisions"]), (0, 0, 0, 0, 0, 0, 0))
        self.assertFalse(row["citations_are_observations"])

    def test_static_report_reserves_manual_evaluation(self):
        text = (ROOT / "reports" / "evidence-static-report.html").read_text(encoding="utf-8").casefold()
        for phrase in ("skip to evidence", "not_ready_for_stage_20", "manual keyboard", "assistive-technology", "affected-user", "māori-authority"):
            self.assertIn(phrase, text)

    def test_orchestration_stays_solo_and_held(self):
        row = load("orchestration/evidence-state.json")
        self.assertEqual((row["tasks_created"], row["tasks_forked"], row["collaboration_subagents"], row["siblings_contacted"]), (0, 0, 0, 0))
        self.assertEqual(row["route_state"], "held_until_exact_final")

    def test_reproduction_boundary(self):
        row = load("reproduction/canonical-evidence-receipt.json")
        self.assertTrue(row["same_owner"])
        self.assertFalse(row["named_or_detached_replay"])
        self.assertFalse(row["independent_team"])
        self.assertFalse(row["full_repository_suite"])

    def test_terminal_truth(self):
        row = load("truth/evidence-phase-truth.json")
        self.assertEqual(row["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(row["full_repository_suite_run"])
        self.assertFalse(row["canonical_final_pass_run"])
        self.assertFalse(row["independent_reproduction"])


if __name__ == "__main__":
    unittest.main()
