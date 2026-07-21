from __future__ import annotations

import json
import re
import sys
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v651-v4"
sys.path.insert(0, str(REPO / "scripts"))

import ghc_family_v651_v4_phase_data as d  # noqa: E402


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class V651V4X1Tests(unittest.TestCase):
    def test_exact_twenty_proposals_and_required_fields(self):
        payload = load("preregistration/proposals.json")
        self.assertEqual(payload["state"], "frozen_x1_only")
        self.assertFalse(payload["observed_outcomes_present"])
        self.assertEqual(payload["count"], 20)
        required = {
            "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class",
            "execution_lane", "official_or_primary_source_needs", "concrete_artifacts",
            "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
            "expected_disposition", "novelty_against_960_frozen_proposals",
        }
        for proposal in payload["proposals"]:
            self.assertTrue(required <= set(proposal))
            self.assertIn(proposal["expected_disposition"], d.OUTCOME_CLASSES)
            self.assertTrue(proposal["protected_gates"])
        self.assertEqual(Counter(p["expected_disposition"] for p in payload["proposals"]), Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}))

    def test_all_960_novelty_and_rejected_collisions(self):
        audit = load("provenance/semantic-novelty-audit.json")
        index = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(audit["inherited_count"], 960)
        self.assertEqual(len(audit["rows"]), 20)
        self.assertTrue(audit["all_pass"])
        self.assertTrue(all(row["passes"] and row["manual_mechanism_review"] == "distinct" for row in audit["rows"]))
        self.assertGreaterEqual(len(audit["rejected_collisions"]), 20)
        self.assertEqual((index["prior_count"], index["new_count"], index["count"]), (960, 20, 980))
        collision_register = load("provenance/inherited-proposal-id-collision-register.json")
        self.assertEqual(collision_register["collision_identifier_count"], 20)
        self.assertTrue(collision_register["current_identifiers_unique"])
        self.assertTrue(collision_register["current_identifiers_disjoint_from_inherited"])

    def test_x1_has_no_execution_or_observed_outcomes(self):
        truth = load("truth/x1-phase-truth.json")
        receipt = load("validation/x1-build-receipt.json")
        self.assertIsNone(truth["observed_outcomes"])
        self.assertFalse(truth["x2_started"])
        self.assertFalse(receipt["x2_artifacts_written"])
        self.assertFalse(receipt["observed_outcomes_written"])
        self.assertFalse((ROOT / "surfaces").exists())
        self.assertFalse((ROOT / "outcomes").exists())

    def test_portfolios_are_frozen_without_credit(self):
        payload = load("portfolios/expanded-portfolio-plan.json")
        self.assertEqual(payload["state"], "frozen_not_executed")
        self.assertEqual(payload["counts"], {"candidate": 30, "clean_fix_refine": 40, "runners": 10, "safe_now": 40, "skills": 20})
        for rows in payload["portfolios"].values():
            self.assertTrue(all(not row["completion_credit"] and not row["inherited_completion_credit"] for row in rows))
        self.assertEqual(load("validation/preregistered-mutation-plan.json")["executed_count"], 0)

    def test_sources_provenance_and_gates(self):
        sources = load("sources/source-ledger.json")
        anchors = load("provenance/source-anchor-ledger.json")
        manifests = load("provenance/source-manifest-parity.json")
        self.assertEqual(sources["count"], 23)
        self.assertEqual((sources["real_data_rows"], sources["participants_or_operators"], sources["production_identity_events"], sources["authority_decisions"]), (0, 0, 0, 0))
        self.assertTrue(set(sources["status_counts"]) <= set(d.SOURCE_STATUS_CLASSES))
        self.assertTrue(anchors["ancestry_verified"] and anchors["local_upstream_tracking_live_remote_equal"])
        self.assertEqual((anchors["phase_commit_count"], anchors["merge_count"], anchors["final_parent"]), (4, 0, d.SOURCE_CLOSEOUT))
        self.assertEqual(manifests["total_entries"], 775)
        self.assertTrue(manifests["valid"])
        self.assertEqual(load("truth/open-gap-register.json")["current_effective_count"], 53)
        self.assertEqual(load("truth/exact-gate-register.json")["current_effective_count"], 54)

    def test_workflow_reflection_index_and_method_flow(self):
        workflow = load("workflow/workflow-plan-refinement.json")
        reflection = load("reflection-remaster/reflection-remaster-issues.json")
        index = load("tooling/ghc-family-index.json")
        method = load("method-flow/method-flow-summary.json")
        self.assertTrue(workflow["valid"])
        self.assertFalse(workflow["requires_user_confirmation"])
        self.assertEqual(workflow["issues"], [])
        self.assertEqual(reflection["issue_count"], 0)
        self.assertTrue(index)
        self.assertEqual(method["counts"]["methods"], 15)
        self.assertEqual(method["counts"]["witness_results"], {"fail": 15, "pass": 15})
        self.assertEqual(method["counts"]["states"]["preferred"], 15)

    def test_negative_retention_and_truth(self):
        negatives = load("truth/retained-negative-register.json")
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual((negatives["sealed_inherited"], negatives["external_inherited"]), (6824, 0))
        self.assertEqual(negatives["v651_v4_x1_operational"], 15)
        self.assertEqual(negatives["effective_count"], 6839)
        self.assertEqual(truth["effective_negatives"], 6839)
        self.assertEqual(negatives["erasures"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_overview_report_document_cap_and_privacy(self):
        overview = (ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8")
        report = (ROOT / "reports/x1-accessible-static-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", overview)), 1500)
        folded = overview.casefold()
        for needle in ("not_ready_for_stage_20", "same-owner", "māori authority", "manual"):
            self.assertIn(needle, folded)
        for needle in ('lang="en"', 'href="#main"', '<caption>', 'scope="col"', 'tabindex="0"'):
            self.assertIn(needle, report)
        self.assertTrue(load("validation/x1-document-cap-receipt.json")["all_within_cap"])
        public_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in ROOT.rglob("*") if path.is_file())
        self.assertIsNone(re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", public_text, re.I))
        self.assertNotIn("file://", public_text.casefold())


if __name__ == "__main__":
    unittest.main()
