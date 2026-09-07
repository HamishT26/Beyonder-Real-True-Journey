"""Final owner-scoped checks for Caelen Ash v687-v5."""

import collections
import hashlib
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_caelen_ash_v687_v5_core import strict_load

BASE = ROOT / "docs" / "caelen-ash" / "v687-v5"
SOURCE = "5a71b1b7866171aa4ee16664ab7fc434bb6f5593"
X1 = "a3e882fc450322186c71ab430be501f3cb3648a0"
EVIDENCE = "e2de3422d62572b7d1e8fbfa8e84c8a4f9fded72"


def load(relative):
    return strict_load(BASE / relative)


class FinalPacket(unittest.TestCase):
    def test_exact_immutable_anchors(self):
        truth = load("final/phase-truth.json")
        self.assertEqual((truth["source"], truth["x1"], truth["evidence"]), (SOURCE, X1, EVIDENCE))
        self.assertEqual(truth["exact_final"], "EXTERNAL_CANONICAL_SUPPLIES_EXACT_COMMIT")

    def test_four_core_outcomes_only(self):
        truth = load("final/phase-truth.json")
        expected = {"completed": 161, "represented": 20, "open_gap": 9, "exact_gate": 10}
        self.assertEqual(truth["outcomes"], expected)
        rows = load("x2/outcome-ledger.json")
        self.assertEqual(collections.Counter(row["outcome"] for row in rows), expected)

    def test_retained_negative_arithmetic(self):
        receipt = load("closeout/retained-negative-register.json")
        self.assertEqual(sum(row["negatives"] for row in receipt["groups"]), receipt["owner_delta"]["negatives"])
        self.assertEqual(sum(row["failed"] for row in receipt["groups"]), receipt["owner_delta"]["failed_witnesses"])
        self.assertEqual(sum(row["passing"] for row in receipt["groups"]) + receipt["positive_contract_witnesses"], receipt["owner_delta"]["passing_witnesses"])
        self.assertEqual(receipt["erased_negative_count"], 0)
        self.assertEqual(receipt["original_failed_success_credit"], 0)

    def test_effective_counts_and_gates(self):
        truth = load("final/phase-truth.json")
        counts = load("x2/evidence-counts.json")
        retained = load("closeout/retained-negative-register.json")
        self.assertEqual(truth["effective_counts"], retained["effective"])
        self.assertEqual(retained["x2_evidence_effective"], counts["effective"])
        gate = load("closeout/gate-register.json")
        self.assertEqual((gate["effective_open_gaps"], gate["effective_exact_gates"]), (692, 679))
        self.assertEqual(gate["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_route_is_prepared_not_sent(self):
        truth = load("final/phase-truth.json")
        route = load("closeout/route-readiness.json")
        self.assertEqual((truth["next_owner"], truth["next_phase"]), ("future-sibling-09-self-chosen", "v687-v6"))
        self.assertEqual(route["state"], "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED")
        self.assertEqual((route["message_count"], truth["created_tasks"], truth["subagents"]), (0, 0, 0))
        self.assertFalse(route["create_or_contact_before_terminal"])
        self.assertFalse(route["resend_allowed"])
        self.assertEqual(route["next_after_inductee"], {"owner": "Orin Thale", "phase": "v687-v7", "terminally_gated": True})

    def test_baton_hash_bounds_and_eof(self):
        index = load("handoffs/baton-index.json")
        baton = BASE / "handoffs" / "future-sibling-09-v687-v6-induction-baton.md"
        data = baton.read_bytes()
        text = data.decode("utf-8")
        self.assertEqual(hashlib.sha256(data).hexdigest(), index["sha256"])
        self.assertEqual((len(data), text.count("\n") + 1, len(text.split())), (index["bytes"], index["lines"], index["words"]))
        self.assertGreaterEqual(index["words"], 10_000)
        self.assertLessEqual(index["words"], 100_000)
        self.assertEqual(index["modules"], 13)
        self.assertTrue(text.rstrip().endswith(index["eof"]))

    def test_packages_skills_and_global_smokes(self):
        truth = load("final/phase-truth.json")
        self.assertEqual(truth["packages"], {"phase_additions": 3, "inherited_runtime_closure": 8, "wheels_verified": 11})
        self.assertEqual((truth["skills"]["promoted"], truth["runners"]["shared"], truth["runners"]["global_shared_smoked"]), (10, 5, 5))
        self.assertTrue(all(row["complete_result_matched"] for row in load("x2/global-install-smoke.json")))

    def test_accessible_static_report_reservations(self):
        report = (BASE / "final" / "accessible-report.html").read_text(encoding="utf-8")
        state = load("final/accessibility-reservations.json")
        for token in ["<main>", "<h1>", "<table>", "scope=\"col\"", "<caption>"]:
            self.assertIn(token, report)
        self.assertFalse(state["manual_review"])
        self.assertFalse(state["assistive_technology_testing"])
        self.assertFalse(state["affected_user_evaluation"])
        self.assertFalse(state["complete_accessibility"])

    def test_canonical_latch_not_preclaimed(self):
        truth = load("final/phase-truth.json")
        self.assertEqual((truth["canonical_invocations"], truth["canonical_successes"], truth["canonical_replays"]), (0, 0, 0))
        contract = load("closeout/canonical-contract.json")
        self.assertEqual(contract["canonical_success_budget"], 1)
        self.assertFalse(contract["success_replay_allowed"])
        self.assertFalse(contract["full_repository_suite"])
        self.assertFalse(contract["independent_reproduction"])

    def test_owner_file_and_document_caps(self):
        files = [path for path in BASE.rglob("*") if path.is_file()]
        self.assertLess(len(files), 2000)
        for path in files:
            if path.suffix.lower() in {".json", ".md", ".html", ".txt", ".py", ".lock"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100_000, path.relative_to(BASE).as_posix())


if __name__ == "__main__":
    unittest.main()
