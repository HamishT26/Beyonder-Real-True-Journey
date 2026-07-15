"""Bounded x2 tests for Sable Rook v645-v5."""

from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v645-v5"
sys.path.insert(0, str(ROOT / "scripts"))


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V645V5EvidenceTests(unittest.TestCase):
    def test_ten_core_proposals(self):
        self.assertEqual(len(load("x2-proposal-ledger.json")["proposals"]), 10)

    def test_outcome_distribution(self):
        rows = load("x2-proposal-ledger.json")["proposals"]
        self.assertEqual(Counter(row["outcome"] for row in rows), Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))

    def test_core_artifacts_exist(self):
        for row in load("x2-proposal-ledger.json")["proposals"]:
            for artifact in row["artifacts"]:
                self.assertTrue((PHASE / artifact).is_file(), artifact)

    def test_desi_zero_row(self):
        row = load("gmut/desi-bao-zero-row-receipt.json")
        self.assertEqual((row["real_rows_ingested"], row["likelihood_evaluations"], row["constraints_reported"]), (0, 0, 0))

    def test_thos_proxy_only(self):
        row = load("thos/learning-decay-proxy-vectors.json")
        self.assertEqual((row["real_participants"], row["real_operators"], row["real_arms"]), (0, 0, 0))

    def test_freed_id_nonproduction(self):
        row = load("freed-id/verifier-attestation-profile.json")
        self.assertEqual((row["details"]["real_keys"], row["details"]["live_services"]), (0, 0))

    def test_cbr_authority_reserved(self):
        row = load("cbr/aviation-occurrence-reservation.json")
        self.assertTrue(all(value == "unresolved_exact_gate" for value in row["details"]["authority_status"].values()))

    def test_synthetic_negatives(self):
        row = load("validation/synthetic-mutation-negative-register.json")
        self.assertEqual(row["count"], 70)
        self.assertTrue(row["all_rejected"] and row["all_retained"])

    def test_portfolios(self):
        counts = load("approval-packets/x2-execution-ledger.json")["counts"]
        self.assertEqual(counts, {"safe_now_completed": 20, "candidate_completed": 12, "exact_unexecuted": 10, "blocked_unexecuted": 5})

    def test_predecessor_credit_zero(self):
        self.assertEqual(load("approval-packets/x2-execution-ledger.json")["predecessor_completion_credit"], 0)

    def test_cleanup(self):
        row = load("maintenance/x2-clean-refine-ledger.json")
        self.assertEqual(row["counts"]["completed"], 20)
        self.assertEqual(row["destructive_change_count"], 0)

    def test_skills_used(self):
        row = load("prototypes/skill-runner-execution-ledger.json")
        self.assertEqual(row["counts"]["skills_used"], 12)
        self.assertTrue(all(skill["invoked"] for skill in row["skills"]))

    def test_runners_used(self):
        row = load("prototypes/skill-runner-execution-ledger.json")
        self.assertEqual(row["counts"]["runners_used"], 6)
        self.assertTrue(all(runner["result"] == "pass" for runner in row["runners"]))

    def test_method_failures_preserved(self):
        row = load("method-flow/method-flow-state-x2.json")
        self.assertEqual(row["counts"]["witness_results"]["fail"], row["counts"]["methods"])
        self.assertEqual(row["counts"]["witness_results"]["pass"], row["counts"]["methods"])

    def test_negative_total_sums(self):
        counts = load("retained-negative-register.json")["counts"]
        total = counts["inherited_effective"] + counts["v645_v5_x1_operational"] + counts["v645_v5_x2_operational"] + counts["v645_v5_synthetic"]
        self.assertEqual(counts["effective_total"], total)

    def test_gate_counts(self):
        row = load("exact-open-gate-register.json")
        self.assertEqual(row["effective"], {"open_gaps": 7, "exact_gates": 8})
        self.assertTrue(row["none_silently_closed"])

    def test_terminal_verdict(self):
        self.assertEqual(load("phase-truth.json")["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_protected_claims_false(self):
        self.assertTrue(all(value is False for value in load("phase-truth.json")["protected_claims"].values()))

    def test_report_structure(self):
        text = (PHASE / "deliverables/v645-v5-static-report.html").read_text(encoding="utf-8")
        for marker in ['<html lang="en">', 'href="#main"', '<main id="main">', '<caption>', 'Manual and affected-user evaluation remain reserved']:
            self.assertIn(marker, text)

    def test_overview_word_range(self):
        count = len((PHASE / "v645-v5-integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(count, 1500)
        self.assertLessEqual(count, 6000)

    def test_all_json_parses(self):
        for path in PHASE.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

    def test_source_status_vocabulary(self):
        self.assertTrue(all(row["status"] in {"current", "stable", "draft", "watch"} for row in load("sources/source-ledger.json")["sources"]))

    def test_sandbox_fail_closed(self):
        row = load("sandbox/sandbox-readonly-audit.json")
        self.assertFalse(row["launched"] or row["elevated"] or row["feature_changed"])

    def test_identity_boundary(self):
        self.assertIn("relational working language", load("phase-truth.json")["identity_boundary"])

    def test_same_owner_not_independent(self):
        row = load("reproduction/same-owner-repeatability-boundary.json")
        self.assertTrue(row["same_owner_shared_infrastructure"])
        self.assertFalse(row["independent_team"] or row["scientific_reproduction"])


if __name__ == "__main__":
    unittest.main()
