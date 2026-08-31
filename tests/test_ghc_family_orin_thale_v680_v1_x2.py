#!/usr/bin/env python3
"""Tests for bounded Orin Thale v680-v1 x2 evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v680-v1"
X2 = PHASE / "x2"
VALIDATION = PHASE / "validation"
X1 = "8e6a3b71c307744bb3af45755696cba212b03ed0"
SOURCE = "415fd8fddc06573d8a672e61a496e56f4b7624e8"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class OrinThaleV680V1X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = load(X2 / "proposal-evidence.json")
        cls.positive = load(X2 / "positive-controls.json")
        cls.mutations = load(X2 / "mutations.json")
        cls.portfolio = load(X2 / "portfolio-results.json")
        cls.skills = load(X2 / "skill-smoke-receipts.json")
        cls.runners = load(X2 / "runner-smoke-receipts.json")
        cls.method = load(X2 / "method-flow-ledger.json")
        cls.truth = load(X2 / "phase-truth.json")
        cls.manifest = load(VALIDATION / "evidence-index-manifest.json")
        cls.staged = load(VALIDATION / "evidence-staged-review.json")

    def test_lifecycle_starts_at_immutable_x1(self):
        self.assertEqual(git("rev-parse", "HEAD"), X1)
        self.assertEqual(git("rev-parse", "HEAD^"), SOURCE)

    def test_immutable_x1_has_no_x2_tree(self):
        self.assertEqual(git("ls-tree", "-r", "--name-only", X1, "--", "docs/orin-thale/v680-v1/x2"), "")

    def test_exact_outcomes(self):
        self.assertEqual(self.evidence["outcome_counts"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(len(self.evidence["outcomes"]), 60)
        self.assertEqual({row["outcome"] for row in self.evidence["outcomes"]}, LABELS)

    def test_positive_controls(self):
        self.assertEqual(self.positive["accepted_count"], 60)
        self.assertEqual(len(self.positive["receipts"]), 60)
        self.assertTrue(all(row["accepted"] for row in self.positive["receipts"]))
        self.assertTrue(all(not row["authority_conferred"] for row in self.positive["receipts"]))

    def test_all_preregistered_mutations_rejected(self):
        self.assertEqual(self.mutations["preregistered_count"], 300)
        self.assertEqual(self.mutations["executed_count"], 300)
        self.assertEqual(self.mutations["rejected_count"], 300)
        self.assertEqual(self.mutations["accepted_invalid_count"], 0)
        self.assertTrue(all(row["failed_witness_retained"] for row in self.mutations["receipts"]))

    def test_each_proposal_has_five_rejections(self):
        counts = {}
        for row in self.mutations["receipts"]:
            counts[row["proposal_id"]] = counts.get(row["proposal_id"], 0) + 1
        self.assertEqual(len(counts), 60)
        self.assertEqual(set(counts.values()), {5})

    def test_twenty_skills_validated_and_used(self):
        self.assertEqual(self.skills["skill_count"], 20)
        self.assertEqual(self.skills["validated_count"], 20)
        self.assertEqual(self.skills["smoke_used_count"], 20)
        self.assertTrue(all(not row["global_install"] for row in self.skills["receipts"]))

    def test_ten_runners_passed(self):
        self.assertEqual(self.runners["runner_count"], 10)
        self.assertEqual(self.runners["passed_count"], 10)
        self.assertTrue(all(row["positive_accepted"] and row["invalid_rejected"] for row in self.runners["receipts"]))

    def test_portfolio_execution_boundaries(self):
        self.assertEqual(len(self.portfolio["safe_now"]), 120)
        self.assertEqual(len(self.portfolio["owner_candidates"]), 80)
        self.assertEqual(len(self.portfolio["clean_fix_refine"]), 100)
        self.assertEqual(len(self.portfolio["exact_approval"]), 20)
        self.assertEqual(len(self.portfolio["blocked"]), 10)
        self.assertTrue(all(row["x2_state"] == "unexecuted" for row in self.portfolio["exact_approval"]))
        self.assertTrue(all(row["x2_state"] == "unexecuted" for row in self.portfolio["blocked"]))

    def test_successor_seeds_have_zero_credit(self):
        self.assertEqual(self.portfolio["successor_credit"], 0)
        successor = load(X2 / "successor-recommendations.json")
        self.assertTrue(successor["recipient_not_contacted"])
        self.assertEqual(successor["Orin_completion_credit"], 0)

    def test_real_data_and_action_counts_are_zero(self):
        self.assertEqual(self.evidence["real_data_rows"], 0)
        self.assertEqual(self.truth["real_data_rows"], 0)
        self.assertEqual(self.truth["network_data_queries"], 0)
        self.assertEqual(self.truth["external_writes"], 0)
        self.assertFalse(self.evidence["authority_conferred"])

    def test_method_flow_count_arithmetic(self):
        self.assertEqual(
            self.method["counts"],
            {
                "effective_negatives": 50394,
                "effective_methods": 53231,
                "failed_witnesses": 22055,
                "bounded_passing_witnesses": 35534,
                "open_gaps": 443,
                "exact_gates": 434,
            },
        )

    def test_method_flow_retains_failures(self):
        self.assertEqual(len(self.method["mutation_failed_witnesses"]), 300)
        self.assertFalse(self.method["failure_erasure"])
        self.assertFalse(self.method["recoveries_retroactively_promote_failure"])
        self.assertFalse(self.method["independent_reproduction_claimed"])

    def test_gate_register(self):
        gates = load(X2 / "gate-register.json")
        self.assertEqual(gates["open_gaps"], 443)
        self.assertEqual(gates["exact_gates"], 434)
        self.assertEqual(gates["closed_by_software"], 0)
        self.assertTrue(gates["authority_noncompensation"])

    def test_privacy_scan(self):
        scan = load(VALIDATION / "evidence-privacy-scan.json")
        self.assertEqual(scan["confirmed_hit_count"], 0)
        self.assertEqual(scan["confirmed_hits"], [])
        self.assertEqual(len(scan["privacy_classes"]), 5)

    def test_security_scan(self):
        scan = load(VALIDATION / "evidence-security-scan.json")
        self.assertEqual(scan["finding_count"], 0)
        self.assertEqual(scan["findings"], [])
        self.assertFalse(scan["exhaustive_security_claimed"])

    def test_manifest_hash_and_staged_path_parity(self):
        actual = set(self.manifest["declared_self_exclusions"])
        for entry in self.manifest["entries"]:
            path = ROOT / entry["path"]
            data = normalized(path)
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])
            actual.add(entry["path"])
        self.assertEqual(len(self.manifest["entries"]), self.manifest["entry_count"])
        self.assertEqual(actual, set(self.staged["expected_paths"]))
        self.assertEqual(len(actual), self.staged["expected_path_count"])

    def test_x1_paths_unmodified_in_staged_review(self):
        self.assertEqual(self.staged["x1_paths_modified"], [])

    def test_only_four_core_labels(self):
        self.assertEqual(set(self.evidence["outcome_counts"]), LABELS)

    def test_terminal_verdict(self):
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
