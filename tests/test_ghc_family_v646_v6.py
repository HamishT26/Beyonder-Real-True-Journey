from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import ghc_family_v646_v6_definitions as d  # noqa: E402
from ghc_family_v646_v6_runtime import ARTIFACTS  # noqa: E402


PHASE = ROOT / "docs/sylven-arc/v646-v6"
X1 = "147aab7fd2f2805f119968dd30ab9c7996306d3a"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V646V6EvidenceTests(unittest.TestCase):
    def test_x1_anchor_and_content_seal(self):
        self.assertEqual(subprocess.run(["git", "merge-base", "--is-ancestor", X1, "HEAD"], cwd=ROOT).returncode, 0)
        seal = load("reproduction/x1-content-seal.json")
        for row in seal["frozen_paths"]:
            relative = f"docs/sylven-arc/v646-v6/{row['path']}"
            content = subprocess.check_output(["git", "show", f"{X1}:{relative}"], cwd=ROOT)
            self.assertEqual(hashlib.sha256(content).hexdigest(), row["sha256"])

    def test_exact_outcome_distribution(self):
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(ledger["proposal_count"], 10)
        self.assertEqual(ledger["distribution"], {"completed": 6, "exact_gate": 1, "open_gap": 1, "represented": 2})
        self.assertTrue(all(row["outcome"] == row["expected_disposition"] for row in ledger["proposals"]))

    def test_all_core_artifacts_exist(self):
        for pair in ARTIFACTS.values():
            for relative in pair:
                self.assertTrue((PHASE / relative).is_file(), relative)

    def test_seventy_synthetic_negatives(self):
        data = load("validation/x2-synthetic-negative-register.json")
        self.assertEqual(data["count"], 70)
        self.assertEqual(data["rejected_count"], 70)
        self.assertEqual(data["failure_erasure_count"], 0)
        self.assertTrue(all(row["observed"] == "reject" and not row["accepted"] and row["retained"] for row in data["negatives"]))

    def test_effective_negative_accounting(self):
        data = load("retained-negative-register.json")
        self.assertEqual((data["inherited_effective"], data["x1_operational"], data["preregistered_synthetic_executed_and_rejected"], data["x2_operational"]), (2884, 10, 70, 9))
        self.assertEqual(data["terminal_validation_operational"], 4)
        self.assertEqual(data["effective_total"], 2977)
        self.assertTrue(data["no_negative_erased"])

    def test_gate_accounting(self):
        data = load("exact-open-gate-register.json")
        self.assertEqual(data["effective_open_gaps"], 15)
        self.assertEqual(data["effective_exact_gates"], 16)
        self.assertEqual(data["silently_closed"], 0)

    def test_portfolios_execute_at_floors(self):
        portfolio = load("approval-packets/x2-portfolio-execution.json")
        candidates = load("prototypes/x2-candidate-execution.json")
        cleanup = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual((portfolio["safe_now_count"], portfolio["candidate_count"], candidates["count"], cleanup["count"]), (30, 20, 20, 30))
        self.assertTrue(all(row["disposition"] == "completed" and row["evidence_exists"] and not row["protected_gate_crossed"] for row in portfolio["safe_now"] + portfolio["candidates"] + cleanup["tasks"]))

    def test_twenty_phase_local_skills(self):
        receipt = load("prototypes/skill-build-use-receipt.json")
        self.assertEqual((receipt["skill_count"], receipt["built_count"], receipt["validated_count"], receipt["invoked_count"]), (20, 20, 20, 20))
        self.assertTrue(all((PHASE / row["path"]).is_file() and not row["global_skill_install"] for row in receipt["skills"]))

    def test_ten_family_current_runners(self):
        receipt = load("prototypes/runner-build-use-receipt.json")
        self.assertEqual(receipt["runner_count"], 10)
        self.assertEqual(receipt["built_count"], 10)
        self.assertTrue(all(row["family_current_name"] for row in receipt["runners"]))

    def test_source_nonconversion(self):
        receipt = load("sources/source-use-receipt.json")
        self.assertEqual(receipt["check_count"], receipt["passed"])
        self.assertEqual(receipt["result"], "pass")

    def test_no_real_rows_people_operations_keys_or_authority(self):
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(ledger["real_data_rows"], 0)
        self.assertEqual(ledger["real_people_or_operations"], 0)
        self.assertEqual(ledger["real_keys_tokens_or_transactions"], 0)
        self.assertFalse(ledger["authority_delegated"])

    def test_method_flow_retains_fail_and_pass(self):
        x1 = load("method-flow/method-flow-state.json")
        x2 = load("method-flow/x2-method-flow-state.json")
        final = load("method-flow/final-method-flow-state.json")
        self.assertEqual(x1["counts"]["witness_results"], {"fail": 10, "pass": 10})
        self.assertEqual(x2["counts"]["witness_results"], {"fail": 9, "pass": 9})
        self.assertEqual(final["counts"]["witness_results"], {"fail": 4, "pass": 4})
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in x1["methods"] + x2["methods"] + final["methods"]))

    def test_overview_three_page_equivalent(self):
        text = (PHASE / "v646-v6-integrated-overview.md").read_text(encoding="utf-8")
        words = text.split()
        self.assertGreaterEqual(len(words), 1200)
        self.assertLessEqual(len(words), 6000)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_static_report_structural_accessibility(self):
        text = (PHASE / "deliverables/v646-v6-evidence-report.html").read_text(encoding="utf-8")
        for token in ('lang="en"', '<title>', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"', 'assistive-technology', 'affected-user'):
            self.assertIn(token, text)

    def test_threat_model_and_privacy_boundary(self):
        model = load("threat-model.json")
        self.assertGreaterEqual(len(model["threats"]), 8)
        self.assertFalse(model["exhaustive_security_claimed"])
        self.assertFalse(model["privacy_complete_claimed"])

    def test_route_remains_prepared(self):
        route = load("orchestration/terminal-route-plan.json")
        self.assertEqual(route["current_state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)

    def test_terminal_verdict_and_full_suite_boundary(self):
        truth = load("evidence/phase-truth.json")
        env = load("environment/x2-environment-receipt.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_team_reproduction"])
        self.assertFalse(env["full_repository_suite_run"])


if __name__ == "__main__":
    unittest.main()
