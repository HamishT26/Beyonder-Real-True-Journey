from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs/vesper-arlen/v671-v7"
SOURCE_FINAL = "6056e5819a124aab7efbb266bfe5bfd710a942f5"
X1_COMMIT = "d2ab0148e82725c680204d1d5a3fbf98544e57ea"
EVIDENCE_COMMIT = "c7b6801c309ba334bff8ce1a14d0cde0350221cb"


def load(relpath: str):
    return json.loads((PHASE_ROOT / relpath).read_text(encoding="utf-8"))


class VesperArlenV671V7FinalTests(unittest.TestCase):
    def test_final_is_direct_single_parent_child_of_evidence(self) -> None:
        row = subprocess.run(["git", "rev-list", "--parents", "-n", "1", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip().split()
        self.assertEqual(len(row), 2)
        self.assertEqual(row[1], EVIDENCE_COMMIT)

    def test_source_to_final_has_three_phase_commits_and_zero_merges(self) -> None:
        commits = subprocess.run(["git", "rev-list", "--count", f"{SOURCE_FINAL}..HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
        merges = subprocess.run(["git", "rev-list", "--count", "--merges", f"{SOURCE_FINAL}..HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
        self.assertEqual((commits, merges), ("3", "0"))

    def test_exact_x1_and_evidence_ancestry(self) -> None:
        for commit in (X1_COMMIT, EVIDENCE_COMMIT):
            result = subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=ROOT)
            self.assertEqual(result.returncode, 0)

    def test_final_truth_preserves_four_outcomes_and_verdict(self) -> None:
        truth = load("closeout/phase-truth-final.json")
        self.assertEqual(truth["outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["evidence_commit"], EVIDENCE_COMMIT)

    def test_effective_counts_are_preserved(self) -> None:
        receipt = load("closeout/closeout-receipt.json")
        self.assertEqual(receipt["effective_counts"], {"effective_negatives": 34626, "methods": 21169, "failed_witnesses": 6447, "passing_witnesses": 8388, "open_gaps": 269, "exact_gates": 264})

    def test_x2_test_composite_preserves_suite_and_target_changed_refresh(self) -> None:
        receipt = load("validation/x2-test-composite-receipt.json")
        self.assertFalse(receipt["collection_only"]["invoked"])
        self.assertEqual(receipt["owner_suite"]["first_invocation_passed_tests"], 22)
        self.assertEqual(receipt["owner_suite"]["first_invocation_credit"], 1)
        self.assertEqual(receipt["owner_suite"]["second_invocation_passed_tests"], 22)
        self.assertEqual(receipt["owner_suite"]["second_invocation_credit"], 0)
        self.assertEqual(receipt["target_changed_refresh"]["passed_tests"], 22)
        self.assertTrue(receipt["target_changed_refresh"]["unchanged_successful_components_replayed"])
        self.assertFalse(receipt["complete_repository_suite"] or receipt["independent_reproduction"])

    def test_completion_checklist_keeps_protected_work_incomplete(self) -> None:
        checklist = load("closeout/completion-checklist.json")
        self.assertGreaterEqual(len(checklist["complete"]), 17)
        self.assertGreaterEqual(len(checklist["incomplete"]), 12)
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_all_phase_json_documents_parse(self) -> None:
        paths = list(PHASE_ROOT.rglob("*.json"))
        self.assertEqual(len(paths), 195)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_final_overview_is_three_page_equivalent(self) -> None:
        text = (PHASE_ROOT / "final/integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 1600)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("34,626", text)
        self.assertIn("THOS Body", text)

    def test_static_report_retains_structural_accessibility_and_no_script(self) -> None:
        text = (PHASE_ROOT / "x2/accessible-evidence-report.html").read_text(encoding="utf-8")
        for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"'):
            self.assertIn(token, text)
        self.assertNotIn("<script", text.lower())

    def test_baton_integrity_word_floor_and_pre_send_truth(self) -> None:
        path = PHASE_ROOT / "handoffs/lyren-moss-v671-v8-activation-candidate.md"
        data = path.read_bytes()
        text = data.decode("utf-8")
        receipt = load("handoffs/lyren-moss-v671-v8-activation-candidate-receipt.json")
        self.assertEqual(receipt["bytes"], len(data))
        self.assertEqual(receipt["whitespace_words"], len(text.split()))
        self.assertGreaterEqual(receipt["whitespace_words"], 10000)
        self.assertEqual(receipt["sha256"], hashlib.sha256(data).hexdigest())
        self.assertTrue(receipt["prepared_not_sent"])
        self.assertFalse(receipt["sent_by_vesper_arlen"] or receipt["delivery_acknowledged"])

    def test_route_state_uses_exact_current_title_and_rejects_stale_label(self) -> None:
        route = load("route/route-state.json")
        self.assertEqual(route["recipient_exact_title"], "Lyren Moss")
        self.assertEqual(route["stale_rejected_source_owner_labels"], ["Vesper Rowan"])
        self.assertEqual(route["prospective_successor_phase"], "v671-v8")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["sent_by_vesper_arlen"] or route["delivery_acknowledged"] or route["substitution_permitted"])

    def test_final_manifests_have_exact_declared_domains(self) -> None:
        delta = load("validation/final-delta-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        self.assertGreaterEqual(delta["entry_count"], 15)
        self.assertGreater(owner["entry_count"], 230)
        self.assertEqual(delta["domain"], "final_exact_staged_git_blobs")
        self.assertEqual(owner["domain"], "owner_exact_evidence_head_plus_final_staged_git_blobs")

    def test_final_validation_plan_is_one_shot_external_receipt_only(self) -> None:
        plan = load("validation/final-validation-plan.json")
        self.assertEqual(plan["invocation_limit"], 1)
        self.assertFalse(plan["post_success_replay"])
        self.assertTrue(plan["external_receipt_only"])

    def test_environment_receipt_performed_no_update(self) -> None:
        receipt = load("closeout/environment-version-receipt.json")
        self.assertFalse(receipt["updates_performed"])
        self.assertEqual(len(receipt["rows"]), 4)
        self.assertTrue(all(row["source"] == "immutable_x1_version_receipt" for row in receipt["rows"]))

    def test_owner_materialized_file_count_is_below_ceiling(self) -> None:
        files = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
        self.assertLess(len(files), 2000)

    def test_post_evidence_failure_is_retained_with_zero_credit(self) -> None:
        receipt = load("closeout/final-operational-failures.json")
        self.assertEqual(receipt["count"], 2)
        self.assertEqual(receipt["rows"][0]["failure_id"], "VA6717-FINAL-OP-001")
        self.assertEqual(receipt["rows"][1]["failure_id"], "VA6717-FINAL-OP-002")
        self.assertTrue(all(row["completion_credit"] == 0 for row in receipt["rows"]))

    def test_seal_and_route_remain_unsent_at_commit_time(self) -> None:
        seal = load("seal/seal-candidate.json")
        route = load("route/route-state.json")
        self.assertEqual(seal["delivery_state"], "PREPARED_NOT_SENT")
        self.assertTrue(route["prepared_not_sent"])
        self.assertFalse(route["delivery_acknowledged"])


if __name__ == "__main__":
    unittest.main()
