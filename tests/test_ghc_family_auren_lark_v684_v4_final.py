from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v684-v4"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
HANDOFF = BASE / "handoffs" / "sable-rook-v684-v5-activation-candidate.md"
VALIDATION = BASE / "validation"
SOURCE = "0134e277a7f573e24e697037749d61d577163637"
X1 = "d1ea9dba1fab7d6726f11a15caf67a8531b70e4a"
EVIDENCE = "c41a5453dce2202324235bdcd820f52e846d834d"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class AurenV684V4FinalTests(unittest.TestCase):
    def test_final_summary(self) -> None:
        summary = load(FINAL / "final-summary.json")
        self.assertEqual((summary["source"], summary["x1"], summary["evidence"]), (SOURCE, X1, EVIDENCE))
        self.assertEqual(summary["outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(summary["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(summary["same_owner_not_independent_reproduction"])

    def test_final_metrics(self) -> None:
        metrics = load(FINAL / "final-metrics.json")
        self.assertEqual(metrics["effective_negatives"], 59084)
        self.assertEqual(metrics["effective_methods"], 73654)
        self.assertEqual(metrics["failed_witnesses"], 30745)
        self.assertEqual(metrics["bounded_passing_witnesses"], 54189)
        self.assertEqual((metrics["open_gaps"], metrics["exact_gates"]), (525, 515))
        self.assertEqual(metrics["proposal_chain"], 10910)

    def test_claim_boundaries(self) -> None:
        matrix = load(FINAL / "claim-boundary-matrix.json")
        required = {"empirical", "professional", "production", "legal", "cultural", "Maori authority", "independent reproduction", "AGI/ASI", "consciousness/personhood", "Theory of Everything", "Stage 20"}
        self.assertTrue(required <= set(matrix["open_or_exact_gated"]))

    def test_relational_language(self) -> None:
        text = (FINAL / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertIn("relational working language only", text)
        self.assertIn("not evidence of consciousness", text)
        self.assertIn("Maori authority", text)
        self.assertIn("Hamish may rename, pause, narrow, redirect, or stop", text)

    def test_historical_manifest_replays(self) -> None:
        replay = load(CLOSEOUT / "historical-manifest-replay.json")
        self.assertTrue(replay["x1"]["valid"])
        self.assertTrue(replay["evidence"]["valid"])
        self.assertEqual((replay["x1"]["declared"], replay["evidence"]["declared"]), (22, 73))

    def test_ancestry_plan(self) -> None:
        ancestry = load(CLOSEOUT / "ancestry.json")
        self.assertEqual(ancestry["required_final_parent"], EVIDENCE)
        self.assertEqual(ancestry["required_source_to_final_commits"], 3)
        self.assertEqual(ancestry["required_merges"], 0)

    def test_route_prepared_not_sent(self) -> None:
        route = load(CLOSEOUT / "route-readiness.json")
        self.assertTrue(route["prepared_not_sent"])
        self.assertFalse(route["successor_precontacted"])
        self.assertEqual(route["prospective_successor"], {"exact_title": "Sable Rook", "phase": "v684-v5"})
        self.assertEqual(route["prospective_next_reminder"], {"exact_title": "Caelen Ash", "phase": "v684-v6"})

    def test_baton_word_bounds_and_state(self) -> None:
        text = HANDOFF.read_text(encoding="utf-8")
        words = len(re.findall(r"\S+", text))
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertIn("PREPARED_BY_AUREN_LARK = true", text)
        self.assertIn("SENT_BY_AUREN_LARK = false", text)
        self.assertIn("Sable Rook", text)
        self.assertIn("Caelen Ash", text)

    def test_content_seal_replays(self) -> None:
        seal = load(CLOSEOUT / "content-seal.json")
        self.assertEqual(seal["target_count"], len(seal["targets"]))
        self.assertGreaterEqual(seal["target_count"], 10)
        for row in seal["targets"]:
            data = (ROOT / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_final_delta_manifest_replays(self) -> None:
        manifest = load(VALIDATION / "final-delta-manifest.json")
        self.assertEqual(manifest["evidence"], EVIDENCE)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            data = (ROOT / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_final_owner_manifest_replays(self) -> None:
        manifest = load(VALIDATION / "final-owner-manifest.json")
        self.assertEqual(manifest["source"], SOURCE)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertLess(manifest["entry_count"], 2000)
        for row in manifest["entries"]:
            data = (ROOT / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_all_phase_json_parses(self) -> None:
        paths = sorted(BASE.rglob("*.json"))
        self.assertGreater(len(paths), 30)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_four_label_outcome_ledger(self) -> None:
        outcome = load(BASE / "x2" / "outcome-ledger.json")
        self.assertEqual(set(outcome["counts"]), ALLOWED)
        self.assertEqual(sum(outcome["counts"].values()), 60)

    def test_held_approvals_remain_unexecuted(self) -> None:
        holds = load(BASE / "x2" / "approval-hold-state.json")
        self.assertEqual((holds["exact_executed"], holds["blocked_executed"]), (0, 0))

    def test_skills_and_runners_remain_phase_local(self) -> None:
        skills = load(BASE / "x2" / "skill-use-receipts.json")
        runners = load(BASE / "x2" / "runner-use-receipts.json")
        self.assertTrue(skills["phase_local_only"])
        self.assertTrue(runners["phase_local_only"])
        self.assertEqual(skills["summary"]["valid_count"], 20)
        self.assertEqual(runners["valid_count"], 10)

    def test_final_privacy_scan(self) -> None:
        scan = load(VALIDATION / "final-privacy-scan.json")
        self.assertEqual(scan["confirmed_hit_count"], 0)
        self.assertTrue(scan["bounded_not_complete_privacy_assurance"])

    def test_static_html_structure(self) -> None:
        text = (FINAL / "final-report.html").read_text(encoding="utf-8").lower()
        for token in ("<!doctype html>", '<html lang="en">', "<main", "skip to main content", "not ready for stage 20"):
            self.assertIn(token, text)

    def test_terminal_gate(self) -> None:
        gate = load(CLOSEOUT / "terminal-gate.json")
        self.assertEqual(gate["repository_state"], "CLOSEOUT_PREPARED_PENDING_EXACT_COMMIT_AND_EXTERNAL_CANONICAL")
        self.assertEqual(gate["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertLess(gate["baton_words"], 100001)

    def test_method_flow_closeout_does_not_rewrite_evidence(self) -> None:
        flow = load(CLOSEOUT / "method-flow-final.json")
        self.assertEqual(flow["effective_negatives"], 59084)
        self.assertEqual(len(flow["final_operational_failures"]), 1)
        self.assertTrue(flow["repository_counts_exclude_later_external_canonical_and_route_events"])
        self.assertTrue(flow["all_failures_retained_zero_credit"])

    def test_no_delivery_claim_in_repository(self) -> None:
        route = load(CLOSEOUT / "route-readiness.json")
        baton = HANDOFF.read_text(encoding="utf-8")
        self.assertTrue(route["prepared_not_sent"])
        self.assertIn("does not establish delivery", baton)


if __name__ == "__main__":
    unittest.main()
