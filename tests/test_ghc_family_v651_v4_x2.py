import json
import sys
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v651_v4_phase_data as d  # noqa: E402
import ghc_family_v651_v4_runtime as runtime  # noqa: E402

ROOT = REPO / d.PHASE_ROOT


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class SylvenV651V4X2Tests(unittest.TestCase):
    def test_all_twenty_frozen_proposals_have_exact_outcomes(self):
        ledger = load("outcomes/evidence-ledger.json")
        self.assertTrue(ledger["valid"])
        self.assertEqual(len(ledger["proposals"]), 20)
        expected = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
        self.assertEqual(ledger["outcome_counts"], expected)
        self.assertEqual(Counter(row["observed_disposition"] for row in ledger["proposals"]), Counter(expected))
        self.assertTrue(all(row["accepting_fixture_passed"] for row in ledger["proposals"]))

    def test_runtime_guard_refuses_each_preregistered_mutation_class(self):
        proposal = d.PROPOSALS[0]
        contract = runtime.contract_for(proposal)
        accepting, mutations = runtime.fixtures_for(contract, proposal)
        self.assertEqual(runtime.evaluate(contract, accepting), [])
        self.assertEqual(len(mutations), 5)
        for mutation in mutations:
            self.assertTrue(runtime.evaluate(contract, mutation), mutation["mutation_type"])

    def test_one_hundred_mutations_executed_and_rejected(self):
        summary = load("validation/mutation-execution-summary.json")
        self.assertEqual((summary["preregistered"], summary["executed"], summary["rejected_or_quarantined"], summary["accepted"]), (100, 100, 100, 0))
        self.assertTrue(summary["valid"])

    def test_zero_row_empirical_gap_stays_open(self):
        receipt = load("surfaces/lotss-dr2-zero-row/bounded-receipt.json")
        self.assertEqual(receipt["observed_disposition"], "open_gap")
        for field in ("real_rows", "queries_or_downloads", "likelihood_evaluations", "posterior_samples_or_constraints"):
            self.assertEqual(receipt[field], 0)

    def test_thos_and_freed_id_surfaces_stay_represented(self):
        for slug in ("refrigeration-service", "cold-room-handover", "ecdsa-data-integrity", "fapi2-message-signing"):
            receipt = load(f"surfaces/{slug}/bounded-receipt.json")
            self.assertEqual(receipt["observed_disposition"], "represented")
            self.assertEqual(receipt["real_participants_or_operators"], 0)
            self.assertEqual(receipt["real_keys_proofs_tokens_accounts_or_network_events"], 0)
            self.assertFalse(receipt["independent_reproduction"])

    def test_refrigeration_authority_stays_exact_gated(self):
        receipt = load("surfaces/refrigeration-authority/bounded-receipt.json")
        self.assertEqual(receipt["observed_disposition"], "exact_gate")
        self.assertEqual(receipt["authority_decisions"], 0)
        self.assertIn("Māori authority remain external", receipt["boundary"])

    def test_structural_completions_remain_bounded(self):
        completed = ["robust-mutex", "unix-ancillary", "ghp-calculus", "bssn-system", "zlib-frame", "pax-archive", "capnproto-encoding", "accessible-file-upload", "langmuir-nonconversion", "lsqr", "snmm-g-estimation", "elias-fano", "golomb-rice", "lz4-frame"]
        for slug in completed:
            receipt = load(f"surfaces/{slug}/bounded-receipt.json")
            self.assertEqual(receipt["observed_disposition"], "completed")
            self.assertTrue(receipt["valid"] and receipt["same_owner_only"])
            self.assertFalse(receipt["independent_reproduction"])

    def test_portfolio_floors_executed_without_inherited_credit(self):
        receipt = load("portfolios/expanded-portfolio-execution.json")
        expected = {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40}
        self.assertEqual(receipt["counts"], expected)
        self.assertEqual(receipt["completed_counts"], expected)
        self.assertFalse(receipt["inherited_credit"])
        self.assertFalse(receipt["unsafe_work_manufactured"])
        self.assertTrue(receipt["valid"])

    def test_phase_local_skills_were_validated_and_smoke_used(self):
        summary = load("tooling/skill-validation-summary.json")
        self.assertEqual((summary["initialized"], summary["customized"], summary["official_quick_validated"], summary["smoke_used"]), (20, 20, 20, 20))
        self.assertFalse(summary["global_installation"])
        self.assertFalse(summary["subagent_forward_test"])
        self.assertEqual(len(summary["witness_paths"]), 20)

    def test_ten_family_current_runners_have_passing_witnesses(self):
        inventory = load("tooling/runner-inventory.json")
        self.assertEqual((inventory["count"], inventory["passed"]), (10, 10))
        self.assertTrue(inventory["family_current_naming"])
        self.assertEqual(len(inventory["witness_paths"]), 10)
        self.assertTrue(all(name.startswith("ghc_family_v651_v4_") for name in inventory["planned"]))

    def test_x1_immutable_git_objects_replay_exactly(self):
        receipt = load("provenance/x1-immutability-receipt.json")
        self.assertTrue(receipt["immutable_git_object_parity"])
        self.assertEqual((receipt["entry_count"], receipt["self_exclusion_count"], receipt["issues"]), (96, 3, []))
        self.assertTrue(receipt["valid"])

    def test_negatives_and_authority_gates_are_preserved(self):
        negatives = load("truth/x2-retained-negative-register.json")
        self.assertEqual((negatives["inherited_sealed_and_external"], negatives["x1_operational"], negatives["x2_operational"], negatives["preregistered_synthetic_rejections"]), (6824, 15, 6, 100))
        self.assertEqual(negatives["effective_count"], 6945)
        self.assertEqual(negatives["erasures"], 0)
        self.assertEqual(load("truth/x2-open-gap-register.json")["current_effective_count"], 54)
        self.assertEqual(load("truth/x2-exact-gate-register.json")["current_effective_count"], 55)

    def test_method_flow_retains_failures_and_passing_witnesses(self):
        summary = load("method-flow/method-flow-summary.json")
        self.assertTrue(summary["valid"])
        self.assertEqual(summary["counts"]["methods"], 21)
        self.assertEqual(summary["counts"]["witness_results"], {"fail": 21, "pass": 21})
        self.assertEqual(summary["counts"]["states"]["preferred"], 21)

    def test_truth_route_and_reproduction_boundaries_remain_closed(self):
        truth = load("truth/evidence-phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual((truth["effective_negatives"], truth["open_gaps"], truth["exact_gates"]), (6945, 54, 55))
        self.assertFalse(truth["full_repository_suite_run"] or truth["canonical_final_pass_run"] or truth["independent_reproduction"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        route = load("orchestration/evidence-state.json")
        self.assertEqual((route["route_state"], route["successor"], route["successor_phase"], route["siblings_contacted"]), ("held_until_exact_final", "Eiren Kestrel", "v651-v5", 0))

    def test_static_report_has_structural_accessibility_basics(self):
        text = (ROOT / "reports/evidence-static-report.html").read_text(encoding="utf-8")
        for token in ("<html lang='en'>", "href='#main'", "<main id='main'>", "<caption>", "scope='col'", "scope='row'", "NOT_READY_FOR_STAGE_20", "manual", "affected-user", "not privacy-complete assurance"):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
