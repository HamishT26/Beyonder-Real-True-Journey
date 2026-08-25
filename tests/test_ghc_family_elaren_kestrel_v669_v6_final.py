from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs/elaren-kestrel/v669-v6"
SOURCE_FINAL = "9cc45691041700cb871f8a72594d55f9e2d9f76a"
X1_COMMIT = "07f934986ddad144e615e7b31276716b646ebba5"
EVIDENCE_COMMIT = "f701d489e7c6a021b0390699e9ceeac5cd00255e"


def load(relpath: str):
    return json.loads((PHASE_ROOT / relpath).read_text(encoding="utf-8"))


class ElarenV669V6FinalTests(unittest.TestCase):
    def test_final_is_direct_single_parent_child_of_evidence(self) -> None:
        row = subprocess.run(
            ["git", "rev-list", "--parents", "-n", "1", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout.strip().split()
        self.assertEqual(len(row), 2)
        self.assertEqual(row[1], EVIDENCE_COMMIT)

    def test_source_to_final_has_three_phase_commits_and_zero_merges(self) -> None:
        commits = subprocess.run(
            ["git", "rev-list", "--count", f"{SOURCE_FINAL}..HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout.strip()
        merges = subprocess.run(
            ["git", "rev-list", "--count", "--merges", f"{SOURCE_FINAL}..HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout.strip()
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
        self.assertEqual(
            receipt["effective_counts"],
            {"effective_negatives": 31477, "methods": 17582, "failed_witnesses": 3298, "passing_witnesses": 4518, "open_gaps": 235, "exact_gates": 230},
        )

    def test_x2_test_composite_is_not_aggregate_success(self) -> None:
        receipt = load("validation/x2-test-composite-receipt.json")
        self.assertEqual(receipt["aggregate_success_credit"], 0)
        self.assertEqual(receipt["composite_dependency_completion"]["completed"], 22)
        self.assertIn("ZERO_AGGREGATE_SUCCESS_CREDIT", receipt["composite_dependency_completion"]["state"])

    def test_completion_checklist_keeps_protected_work_incomplete(self) -> None:
        checklist = load("closeout/completion-checklist.json")
        self.assertGreaterEqual(len(checklist["complete"]), 15)
        self.assertGreaterEqual(len(checklist["incomplete"]), 10)
        self.assertIn("NOT_READY_FOR_STAGE_20", checklist["terminal_verdict"])

    def test_all_phase_json_documents_parse(self) -> None:
        paths = list(PHASE_ROOT.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 185)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_final_overview_is_three_page_equivalent(self) -> None:
        text = (PHASE_ROOT / "final/integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 2200)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("31,476", text)

    def test_static_report_retains_structural_accessibility_and_no_script(self) -> None:
        text = (PHASE_ROOT / "x2/accessible-evidence-report.html").read_text(encoding="utf-8")
        for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"'):
            self.assertIn(token, text)
        self.assertNotIn("<script", text.lower())

    def test_baton_integrity_and_pre_send_truth(self) -> None:
        path = PHASE_ROOT / "handoffs/neris-solane-v669-v7-activation-candidate.md"
        data = path.read_bytes()
        text = data.decode("utf-8")
        receipt = load("handoffs/neris-solane-v669-v7-activation-candidate-receipt.json")
        self.assertEqual(receipt["bytes"], len(data))
        self.assertEqual(receipt["whitespace_words"], len(text.split()))
        self.assertEqual(receipt["sha256"], hashlib.sha256(data).hexdigest())
        self.assertTrue(receipt["prepared_not_sent"])
        self.assertFalse(receipt["sent_by_elaren_kestrel"] or receipt["delivery_acknowledged"])

    def test_route_state_is_prepared_not_sent(self) -> None:
        route = load("route/route-state.json")
        self.assertEqual(route["recipient_exact_title"], "Neris Solane")
        self.assertEqual(route["prospective_successor_phase"], "v669-v7")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["sent_by_elaren_kestrel"] or route["delivery_acknowledged"])

    def test_final_manifests_have_exact_declared_domains(self) -> None:
        delta = load("validation/final-delta-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        self.assertGreaterEqual(delta["entry_count"], 15)
        self.assertGreater(owner["entry_count"], 220)
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

    def test_owner_materialized_file_count_is_below_ceiling(self) -> None:
        files = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
        self.assertLess(len(files), 2000)


if __name__ == "__main__":
    unittest.main()
