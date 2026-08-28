from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v674-v2"
X1 = PHASE / "x1"
SOURCE = "6f079df9a056f00e80392b7e036abc023db5fa88"


def load(name: str) -> dict:
    return json.loads((X1 / name).read_text(encoding="utf-8"))


class SableRookV674V2X1Tests(unittest.TestCase):
    def test_exact_source_and_planning_only_boundary(self) -> None:
        intake = load("activation-intake.json")
        self.assertEqual(intake["source_final"], SOURCE)
        self.assertEqual(intake["source_packet_sha256"], "88abed13dda8524f437ac414747075cc9f42047520bcc502a503daab394fd871")
        self.assertTrue(intake["source_verified_clean_four_way_equal"])
        self.assertFalse((PHASE / "x2").exists())
        self.assertEqual(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), SOURCE)

    def test_inherited_reviews_are_zero_credit(self) -> None:
        data = load("inherited-revalidation-freeze.json")
        self.assertEqual(data["row_count"], 60)
        self.assertEqual(len(data["rows"]), 60)
        self.assertTrue(all(row["novelty_credit"] == 0 and row["completion_credit"] == 0 for row in data["rows"]))
        self.assertEqual(len({row["source_proposal_id"] for row in data["rows"]}), 60)

    def test_new_proposals_and_expected_outcomes(self) -> None:
        data = load("new-proposal-freeze.json")
        self.assertEqual(data["source_proposal_chain"], 6610)
        self.assertEqual(data["proposal_chain_if_x2_evidence_frozen"], 6670)
        self.assertEqual(data["proposal_count"], 60)
        self.assertEqual(data["expected_outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertFalse(data["outcomes_observed"])
        self.assertFalse(data["universal_novelty_claim"])
        required = {
            "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class",
            "execution_lane", "official_or_primary_source_needs", "concrete_artifact",
            "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
            "expected_execution_disposition", "x1_state",
        }
        self.assertTrue(all(required <= set(row) for row in data["proposals"]))
        self.assertEqual(len({row["title"].casefold() for row in data["proposals"]}), 60)
        self.assertTrue(all(row["x1_state"] == "planning_only_not_observed_outcome" for row in data["proposals"]))

    def test_portfolio_floors_and_holds(self) -> None:
        data = load("portfolio-freeze.json")
        self.assertEqual(len(data["safe_now"]), 120)
        self.assertEqual(len(data["owner_candidates"]), 80)
        self.assertEqual(len(data["successor_candidates"]), 20)
        self.assertEqual(len(data["exact_approval"]), 20)
        self.assertEqual(len(data["blocked"]), 10)
        self.assertEqual(len(data["owner_skill_ideas"]), 20)
        self.assertEqual(len(data["owner_runner_ideas"]), 10)
        self.assertEqual(len(data["successor_skill_ideas"]), 10)
        self.assertEqual(len(data["successor_runner_ideas"]), 10)
        self.assertEqual(len(data["owner_clean_fix_refine"]), 100)
        self.assertEqual(len(data["successor_clean_fix_refine"]), 30)
        self.assertTrue(all(row["completion_credit"] == 0 for row in data["exact_approval"] + data["blocked"]))
        self.assertTrue(data["caps_are_ceilings"])
        self.assertEqual(data["materialized_file_stop"], 2000)

    def test_identity_and_authority_boundary(self) -> None:
        data = load("identity-and-boundary.json")
        self.assertFalse(data["identity_evidence"])
        self.assertFalse(data["authority_evidence"])
        self.assertTrue(data["corrigible"])
        self.assertIn("maori_authority", data["protected_gates"])
        self.assertIn("stage20", data["protected_gates"])

    def test_sources_are_vocabulary_not_observations(self) -> None:
        data = load("source-ledger.json")
        self.assertEqual(len(data["entries"]), 4)
        self.assertFalse(data["citations_are_observations"])
        self.assertEqual(data["real_data_rows"], 0)
        self.assertFalse(data["endorsement_claimed"])
        webvtt = next(row for row in data["entries"] if row["source_id"] == "W3C-WEBVTT-2026")
        self.assertEqual(webvtt["status"], "candidate_recommendation_draft")

    def test_failures_are_retained_and_recoveries_additive(self) -> None:
        data = load("method-flow-startup.json")
        self.assertEqual(data["startup_failure_count"], 14)
        self.assertEqual(len(data["failures"]), 14)
        self.assertTrue(all(row["state"] == "failed_retained_zero_credit" and row["success_credit"] == 0 for row in data["failures"]))

    def test_route_is_held(self) -> None:
        data = load("route-roster-plan.json")
        self.assertEqual(data["current_owner"], "Sable Rook")
        self.assertEqual(data["current_phase"], "v674-v2")
        self.assertEqual(data["next_owner"], "Caelen Ash")
        self.assertEqual(data["next_phase"], "v674-v3")
        self.assertFalse(data["precontact"])
        self.assertEqual(data["send_attempts"], 0)
        self.assertFalse(data["create_task"])

    def test_x1_manifest_exact_bytes(self) -> None:
        manifest = load("x1-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes()
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_overview_and_privacy_shape(self) -> None:
        text = (X1 / "integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 700)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("relational working language only", text)
        self.assertNotRegex(text, re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I))
        self.assertNotIn("C:\\Users\\", text)
        self.assertNotIn("D:\\GHC-Archives", text)

    def test_exact_staged_review_when_present(self) -> None:
        path = PHASE / "validation" / "x1-staged-review.json"
        if not path.exists():
            self.skipTest("staged review is generated only after exact staging")
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["state"], "VALID_EXACT_X1_STAGED_REVIEW")
        self.assertFalse(data["x2_paths_present"])
        self.assertEqual(data["confirmed_privacy_hits"], 0)
        self.assertEqual(data["out_of_scope_paths"], [])
        self.assertTrue(data["diff_hygiene"])
        for entry in data["entries"]:
            blob = subprocess.check_output(["git", "show", f":{entry['path']}"], cwd=ROOT)
            self.assertEqual(len(blob), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256_git_index_blob"], entry["path"])


if __name__ == "__main__":
    unittest.main()
