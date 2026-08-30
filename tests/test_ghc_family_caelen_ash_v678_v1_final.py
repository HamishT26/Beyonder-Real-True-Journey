from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v678-v1"
FINAL = PHASE / "final"
SOURCE = "af26e6c68f43aa104164490edda08f2497f21deb"
X1 = "adb7c5062ac0f8c715a996a131490ca422a48565"
EVIDENCE = "ee149e3d085e9dbd809d9985f8d194ba4e66bcf4"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class CaelenAshV678V1FinalTests(unittest.TestCase):
    def test_truth_is_exact_and_route_held(self) -> None:
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["route_state"], "PREPARED_NOT_SENT")
        self.assertEqual(truth["final_head"], "pending_until_commit")
        self.assertEqual(truth["proposal_chain"], 8330)
        self.assertEqual(truth["counts"]["open_gaps"], 395)
        self.assertEqual(truth["counts"]["exact_gates"], 386)
        self.assertEqual(truth["counts"]["methods"], 43374)
        self.assertFalse(truth["authority_conferred"])
        self.assertFalse(truth["independent_reproduction"])

    def test_counts_and_retained_failures(self) -> None:
        register = load(FINAL / "retained-negative-register.json")
        self.assertEqual(register["effective_total"], 46117)
        self.assertEqual(register["owner_operational_failures"], 47)
        self.assertEqual(register["preregistered_rejected_mutations"], 160)
        self.assertEqual(len(register["operational_rows"]), 47)
        self.assertFalse(register["failure_erasure"])
        self.assertFalse(register["conversion_of_failure_to_pass"])

    def test_gap_and_gate_registers(self) -> None:
        gaps = load(FINAL / "open-gap-register.json")
        gates = load(FINAL / "exact-gate-register.json")
        self.assertEqual((gaps["inherited"], gaps["new"], gaps["effective"]), (392, 3, 395))
        self.assertEqual((gates["inherited"], gates["new"], gates["effective"]), (383, 3, 386))
        self.assertEqual(gaps["silently_closed"], 0)
        self.assertEqual(gates["silently_closed"], 0)

    def test_overview_is_three_page_equivalent(self) -> None:
        words = len((FINAL / "final-integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 1800)
        self.assertLessEqual(words, 100000)

    def test_accessible_static_report_reserves_manual_review(self) -> None:
        text = (FINAL / "accessible-static-report.html").read_text(encoding="utf-8")
        for token in ("<h1>", "<h2", "<table>", "<caption>", "scope=\"col\"", "Manual evaluation", "assistive-technology"):
            self.assertIn(token, text)

    def test_complete_incomplete_boundary(self) -> None:
        data = load(FINAL / "complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(data["complete_within_bounded_scope"]), 10)
        self.assertGreaterEqual(len(data["incomplete_or_reserved"]), 9)
        joined = " ".join(data["incomplete_or_reserved"])
        self.assertIn("Māori authority", joined)
        self.assertIn("independent-team", joined)

    def test_closeout_and_seal_are_honest_candidates(self) -> None:
        closeout = load(FINAL / "closeout-receipt.json")
        seal = load(FINAL / "content-seal.json")
        validation = load(FINAL / "final-validation-candidate.json")
        self.assertEqual(closeout["state"], "PRECOMMIT_CLOSEOUT_CANDIDATE")
        self.assertEqual(closeout["final_head"], "pending_until_commit")
        self.assertEqual(seal["state"], "CONTENT_SEAL_CANDIDATE")
        self.assertTrue(seal["self_identifier_pending"])
        self.assertEqual(validation["canonical_invocations"], 0)
        self.assertEqual(validation["canonical_successes"], 0)
        self.assertFalse(validation["replay_after_success_permitted"])

    def test_route_is_prepared_not_sent(self) -> None:
        route = load(FINAL / "route-plan.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["conditional_successor_title"], "Orin Thale")
        self.assertEqual(route["conditional_successor_phase"], "v678-v2")
        self.assertFalse(route["precontact_permitted"])
        self.assertFalse(route["message_sent"])

    def test_ancestry_candidate_or_final(self) -> None:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, encoding="utf-8").strip()
        for anchor in (SOURCE, X1, EVIDENCE):
            self.assertEqual(subprocess.run(["git", "merge-base", "--is-ancestor", anchor, head], cwd=ROOT).returncode, 0)
        self.assertEqual(subprocess.check_output(["git", "rev-parse", f"{EVIDENCE}^"], cwd=ROOT, text=True, encoding="utf-8").strip(), X1)
        if head != EVIDENCE:
            self.assertEqual(subprocess.check_output(["git", "rev-parse", "HEAD^"], cwd=ROOT, text=True, encoding="utf-8").strip(), EVIDENCE)
            self.assertEqual(int(subprocess.check_output(["git", "rev-list", "--count", f"{SOURCE}..HEAD"], cwd=ROOT, text=True, encoding="utf-8")), 3)
            self.assertEqual(subprocess.check_output(["git", "rev-list", "--merges", f"{SOURCE}..HEAD"], cwd=ROOT, text=True, encoding="utf-8").splitlines(), [])

    def test_all_phase_json_strict_and_file_guard(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 55)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))
        self.assertLess(len([p for p in PHASE.rglob("*") if p.is_file()]), 2000)

    def test_final_staged_receipts_when_present(self) -> None:
        manifest_path = PHASE / "validation" / "final-owner-manifest.json"
        if not manifest_path.exists():
            self.skipTest("final staged review not generated yet")
        owner = load(manifest_path)
        delta = load(PHASE / "validation" / "final-delta-manifest.json")
        review = load(PHASE / "validation" / "final-staged-review.json")
        self.assertEqual(review["state"], "VALID_EXACT_FINAL_STAGED_REVIEW")
        self.assertEqual(owner["entry_count"] + len(owner["declared_self_exclusions"]), owner["owner_path_count"])
        self.assertEqual(delta["entry_count"], review["delta_entries"])
        self.assertEqual(review["confirmed_privacy_hits"], 0)
        self.assertEqual(review["security_findings"], 0)

    def test_diff_hygiene(self) -> None:
        result = subprocess.run(["git", "diff", "--check"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
