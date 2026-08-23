from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "elowen-cairn" / "v667-v3"


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


class ElowenCairnV667V3CloseoutTests(unittest.TestCase):
    def test_01_phase_truth_counts_are_exact(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["core_outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["effective_negatives"], 27333)
        self.assertEqual(truth["effective_methods"], 12795)
        self.assertEqual(truth["effective_open_gaps"], 193)
        self.assertEqual(truth["effective_exact_gates"], 191)

    def test_02_phase_truth_boundaries_are_exact(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["full_repository_suite_run"])
        self.assertTrue(truth["same_owner_evidence"])
        self.assertFalse(truth["independent_reproduction"])

    def test_03_lifecycle_chain_is_direct(self):
        life = load("closeout/lifecycle-replay.json")
        self.assertTrue(life["x1_direct_from_source"])
        self.assertTrue(life["evidence_direct_from_x1"])
        self.assertEqual(life["source_to_evidence_commit_count"], 2)
        self.assertEqual(life["source_to_evidence_merge_count"], 0)

    def test_04_checklist_preserves_incomplete_work(self):
        checklist = load("closeout/complete-incomplete-checklist.json")
        text = " ".join(checklist["incomplete_or_reserved"])
        for token in ("real V&A", "Māori-authority", "empirical GMUT", "external exact-final"):
            self.assertIn(token, text)

    def test_05_versions_are_read_only(self):
        receipt = load("closeout/environment-version-receipt.json")
        self.assertTrue(all(not row["mutation"] for row in receipt["read_only_version_checks"]))
        self.assertFalse(receipt["codex_desktop_updated"])
        self.assertFalse(receipt["software_installed"])
        self.assertFalse(receipt["privilege_elevated"])

    def test_06_owner_file_budget_is_bounded(self):
        budget = load("closeout/owner-file-budget.json")
        self.assertTrue(budget["within_ceiling"])
        self.assertLess(budget["observed_pre_stage_owner_paths"], 2000)
        self.assertEqual(budget["document_word_ceiling"], 100000)

    def test_07_route_remains_prepared_not_sent(self):
        route = load("closeout/route-receipt.json")
        self.assertEqual(route["status"], "PREPARED_NOT_SENT")
        self.assertFalse(route["send_attempted"])
        self.assertFalse(route["acknowledged"])
        self.assertEqual(route["provisional_successor_title"], "Sylven Arc")

    def test_08_seal_is_honestly_pending_external_canonical(self):
        seal = load("seal/seal-candidate.json")
        self.assertEqual(seal["status"], "PREPARED_PENDING_EXACT_FINAL_CANONICAL")
        self.assertEqual(seal["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_09_handoff_candidate_is_sanitized_and_unsent(self):
        text = (PHASE_ROOT / "handoffs" / "sylven-arc-v667-v4-activation-candidate.md").read_text(encoding="utf-8")
        self.assertIn("SENT_BY_ELOWEN_CAIRN = false", text)
        self.assertNotRegex(text, r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")
        self.assertNotRegex(text, r"\b[A-Za-z]:\\")
        self.assertNotIn("source_thread_id", text)

    def test_10_overview_is_three_page_equivalent_and_bounded(self):
        text = (PHASE_ROOT / "closeout" / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\S+", text)), 1800)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("not evidence of consciousness", text)
        self.assertIn("Māori authority", text)

    def test_11_final_staged_manifests_are_valid(self):
        staged = load("validation/final-staged-review.json")
        owner = load("validation/final-owner-manifest.json")
        delta = load("validation/final-delta-manifest.json")
        self.assertTrue(staged["valid"])
        self.assertLess(owner["entry_count"], 2000)
        self.assertGreater(delta["entry_count"], 5)

    def test_12_final_privacy_and_security_candidates_are_zero(self):
        privacy = load("validation/final-privacy-scan.json")
        security = load("validation/final-security-review.json")
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(security["valid"])
        self.assertEqual(security["finding_count"], 0)

    def test_13_stale_label_review_is_valid(self):
        stale = load("closeout/stale-label-review.json")
        self.assertTrue(stale["valid"])
        self.assertEqual(stale["stale_owner_or_phase_candidates"], [])

    def test_14_every_phase_json_document_parses(self):
        paths = list(PHASE_ROOT.rglob("*.json"))
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(paths), 115)


if __name__ == "__main__":
    unittest.main()
