from __future__ import annotations

import json
import re
import sys
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/orin-thale/v651-v2"
sys.path.insert(0, str(REPO / "scripts"))

import ghc_family_v651_v2_phase_data as d  # noqa: E402


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class V651V2X1Tests(unittest.TestCase):
    def test_exact_twenty_proposals_and_required_fields(self):
        payload = load("preregistration/proposals.json")
        self.assertEqual(payload["state"], "frozen_x1_only")
        self.assertFalse(payload["observed_outcomes_present"])
        self.assertEqual(payload["count"], 20)
        required = {
            "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class",
            "execution_lane", "official_or_primary_source_needs", "concrete_artifacts",
            "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
            "expected_disposition",
        }
        for proposal in payload["proposals"]:
            self.assertTrue(required <= set(proposal))
            self.assertTrue(proposal["protected_gates"])
            self.assertIn(proposal["expected_disposition"], d.OUTCOME_CLASSES)
        self.assertEqual(
            Counter(p["expected_disposition"] for p in payload["proposals"]),
            Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}),
        )

    def test_novelty_chain_and_rejected_collisions(self):
        audit = load("provenance/semantic-novelty-audit.json")
        index = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(audit["inherited_count"], 920)
        self.assertEqual(len(audit["rows"]), 20)
        self.assertTrue(audit["all_pass"])
        self.assertTrue(all(row["passes"] and row["manual_mechanism_review"] == "distinct" for row in audit["rows"]))
        self.assertGreaterEqual(len(audit["rejected_collisions"]), 20)
        self.assertEqual(index["prior_count"], 920)
        self.assertEqual(index["new_count"], 20)
        self.assertEqual(index["count"], 940)

    def test_x1_contains_no_x2_outcomes_or_surface_execution(self):
        truth = load("truth/x1-phase-truth.json")
        receipt = load("validation/x1-build-receipt.json")
        self.assertIsNone(truth["observed_outcomes"])
        self.assertFalse(truth["x2_started"])
        self.assertFalse(receipt["x2_artifacts_written"])
        self.assertFalse(receipt["observed_outcomes_written"])
        self.assertFalse((ROOT / "surfaces").exists())
        self.assertFalse((ROOT / "outcomes").exists())

    def test_portfolio_floors_are_frozen_without_credit(self):
        payload = load("portfolios/expanded-portfolio-plan.json")
        self.assertEqual(payload["state"], "frozen_not_executed")
        self.assertEqual(payload["counts"], {"candidate": 30, "clean_fix_refine": 40, "runners": 10, "safe_now": 40, "skills": 20})
        for rows in payload["portfolios"].values():
            self.assertTrue(all(not row["completion_credit"] and not row["inherited_completion_credit"] for row in rows))
        held = load("truth/held-approval-packets.json")
        self.assertEqual((held["exact_approval_count"], held["blocked_count"], held["executed_count"]), (10, 5, 0))

    def test_sources_and_authority_boundaries(self):
        ledger = load("sources/source-ledger.json")
        self.assertEqual(ledger["count"], 24)
        self.assertEqual(ledger["real_data_rows"], 0)
        self.assertEqual(ledger["participants_or_operators"], 0)
        self.assertEqual(ledger["production_identity_events"], 0)
        self.assertEqual(ledger["authority_decisions"], 0)
        self.assertTrue(set(ledger["status_counts"]) <= set(d.SOURCE_STATUS_CLASSES))
        self.assertEqual(load("truth/open-gap-register.json")["current_effective_count"], 51)
        self.assertEqual(load("truth/exact-gate-register.json")["current_effective_count"], 52)

    def test_workflow_reflection_and_method_flow(self):
        workflow = load("workflow/workflow-plan-refinement.json")
        reflection = load("reflection-remaster/reflection-remaster-issues.json")
        method = load("method-flow/method-flow-summary.json")
        self.assertTrue(workflow["valid"])
        self.assertFalse(workflow["requires_user_confirmation"])
        self.assertEqual(workflow["issues"], [])
        self.assertEqual(reflection["issue_count"], 0)
        self.assertGreaterEqual(method["counts"]["methods"], 8)
        self.assertGreaterEqual(method["counts"]["witness_results"]["fail"], 8)
        self.assertGreaterEqual(method["counts"]["witness_results"]["pass"], 6)
        active = sum(method["counts"]["states"][state] for state in ("candidate", "validated", "preferred"))
        self.assertEqual(active, method["counts"]["methods"])

    def test_mutation_plan_is_preregistered_not_executed(self):
        payload = load("validation/preregistered-mutation-plan.json")
        self.assertEqual(payload["count"], 100)
        self.assertEqual(payload["executed_count"], 0)
        self.assertEqual(payload["state"], "frozen_x1_only")
        self.assertTrue(all(row["x1_state"] == "preregistered_not_executed" for row in payload["mutations"]))

    def test_overview_report_and_privacy_surface(self):
        overview = (ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8")
        report = (ROOT / "reports/x1-accessible-static-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", overview)), 1500)
        folded = overview.casefold()
        for needle in ("not_ready_for_stage_20", "same-owner", "māori authority", "manual keyboard"):
            self.assertIn(needle, folded)
        for needle in ('lang="en"', 'href="#main"', '<caption>', 'scope="col"', 'tabindex="0"'):
            self.assertIn(needle, report)
        public_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in ROOT.rglob("*") if path.is_file())
        self.assertIsNone(re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", public_text, re.I))
        self.assertNotIn("file://", public_text.casefold())


if __name__ == "__main__":
    unittest.main()
