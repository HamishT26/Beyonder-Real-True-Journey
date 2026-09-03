#!/usr/bin/env python3
"""Owner-scoped x2 evidence tests for Caelen Morrow v685-v4."""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "caelen-morrow" / "v685-v4"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_caelen_morrow_v685_v4_core import (  # noqa: E402
    MUTATION_TYPES,
    make_positive_record,
    mutate_record,
    validate_record,
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> subprocess.CompletedProcess[bytes]:
    proc = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        raise AssertionError(proc.stderr.decode("utf-8", "replace"))
    return proc


class CaelenMorrowV685V4X2Tests(unittest.TestCase):
    def test_positive_contract_and_all_mutation_types(self):
        positive = make_positive_record("CM6854-N001", "synthetic smoke")
        accepted, errors = validate_record(positive)
        self.assertTrue(accepted)
        self.assertEqual(errors, [])
        for mutation_type in MUTATION_TYPES:
            invalid = mutate_record(positive, mutation_type)
            accepted, errors = validate_record(invalid)
            self.assertFalse(accepted, mutation_type)
            self.assertTrue(errors, mutation_type)

    def test_all_proposals_have_exact_outcomes(self):
        outcomes = load(X2 / "proposal-outcomes.json")
        self.assertEqual(outcomes["unknown_labels"], [])
        self.assertEqual(
            outcomes["outcome_counts"],
            {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        )
        self.assertEqual(len(outcomes["outcomes"]), 60)
        self.assertTrue(all(row["evidence_valid"] for row in outcomes["outcomes"]))

    def test_all_300_mutations_are_rejected_and_retained(self):
        receipt = load(X2 / "rejecting-mutations.json")
        self.assertEqual(receipt["mutation_count"], 300)
        self.assertEqual(receipt["accepted_count"], 0)
        self.assertEqual(receipt["rejected_count"], 300)
        self.assertEqual(set(receipt["mutation_type_counts"]), set(MUTATION_TYPES))
        self.assertEqual(set(receipt["mutation_type_counts"].values()), {60})
        self.assertTrue(all(row["retained_failed_witness"] for row in receipt["mutations"]))
        self.assertEqual({row["credit"] for row in receipt["mutations"]}, {"zero"})

    def test_proposal_evidence_is_zero_real_row(self):
        receipt = load(X2 / "proposal-evidence.json")
        self.assertEqual(receipt["proposal_count"], 60)
        self.assertEqual(receipt["real_rows"], 0)
        self.assertTrue(all(row["bounded_record_accepted"] for row in receipt["evidence"]))
        self.assertTrue(all(row["rejecting_mutations_rejected"] == 5 for row in receipt["evidence"]))
        self.assertTrue(all(row["real_rows"] == 0 for row in receipt["evidence"]))
        self.assertEqual({row["authority_credit"] for row in receipt["evidence"]}, {"zero"})

    def test_twenty_skills_were_quick_validated_read_and_smoked(self):
        receipt = load(X2 / "skill-initialization-and-smoke-receipt.json")
        self.assertEqual(receipt["skill_count"], 20)
        self.assertEqual(receipt["quick_validated_count"], 20)
        self.assertEqual(receipt["complete_read_count"], 20)
        self.assertEqual(receipt["accepting_smoke_pass_count"], 20)
        self.assertEqual(receipt["rejecting_smoke_pass_count"], 20)
        self.assertEqual(receipt["global_installation_count"], 0)
        self.assertTrue(all(row["smoke_pass"] for row in receipt["skills"]))
        for row in receipt["skills"]:
            skill = X2 / "skills" / row["skill"] / "SKILL.md"
            normalized = skill.read_text(encoding="utf-8").encode("utf-8")
            self.assertEqual(hashlib.sha256(normalized).hexdigest(), row["sha256"])

    def test_ten_family_current_runners_accept_and_reject(self):
        receipt = load(X2 / "runner-smoke-receipt.json")
        self.assertEqual(receipt["runner_count"], 10)
        self.assertEqual(receipt["positive_pass_count"], 10)
        self.assertEqual(receipt["invalid_rejection_pass_count"], 10)
        self.assertTrue(all(row["smoke_pass"] for row in receipt["runners"]))
        self.assertTrue(all(row["family_current"] for row in receipt["runners"]))

    def test_portfolio_execution_and_holds(self):
        receipt = load(X2 / "portfolio-execution.json")
        self.assertEqual(len(receipt["safe_now"]), 120)
        self.assertEqual(len(receipt["owner_candidates"]), 80)
        self.assertEqual(len(receipt["successor_candidates"]), 20)
        self.assertEqual(len(receipt["owner_clean_fix_refine"]), 100)
        self.assertEqual(len(receipt["successor_clean_fix_refine"]), 30)
        self.assertEqual(len(receipt["exact_approval"]), 20)
        self.assertEqual(len(receipt["blocked"]), 10)
        self.assertEqual(receipt["owner_bounded_completed_count"], 300)
        self.assertEqual(receipt["successor_zero_credit_represented_count"], 50)
        self.assertEqual(receipt["exact_or_blocked_executed_count"], 0)
        self.assertFalse(any(row["executed"] for row in receipt["exact_approval"]))
        self.assertFalse(any(row["executed"] for row in receipt["blocked"]))

    def test_method_flow_arithmetic_and_non_erasure(self):
        receipt = load(X2 / "method-flow-evidence.json")
        counts = receipt["effective_evidence_counts"]
        self.assertEqual(counts["effective_negatives"], 62113)
        self.assertEqual(counts["effective_methods"], 78878)
        self.assertEqual(counts["failed_witnesses"], 33174)
        self.assertEqual(counts["bounded_passing_witnesses"], 59413)
        self.assertEqual(counts["open_gaps"], 552)
        self.assertEqual(counts["exact_gates"], 542)
        self.assertFalse(receipt["failure_erasure"])
        self.assertFalse(receipt["recovery_promotes_failed_witness"])
        self.assertEqual(len(receipt["operational_failures"]), 0)

    def test_zero_row_and_three_pillar_boundaries(self):
        zero = load(X2 / "zero-row-empirical-receipt.json")
        numeric = [value for key, value in zero.items() if key not in {"schema", "owner", "phase"}]
        self.assertEqual(set(numeric), {0})
        board = load(X2 / "three-pillars-board.json")
        self.assertEqual(set(board["pillars"]), {"THOS Body", "GMUT Mind", "Freed ID and CBR Heart"})
        self.assertEqual(board["primary"], "Freed ID and CBR Heart")
        self.assertTrue(board["authority_noncompensation"])
        self.assertTrue(board["empirical_noncompensation"])

    def test_accessible_board_has_structural_landmarks(self):
        text = (X2 / "accessible-evidence-board.html").read_text(encoding="utf-8")
        for token in ('lang="en"', "<title>", "<header>", "<nav", "<main>", "<table>", "<caption>", 'scope="col"'):
            self.assertIn(token, text)
        self.assertIn("Reserved evaluation", text)

    def test_evidence_manifest_replays_exact_index_blobs(self):
        manifest = load(VALIDATION / "evidence-index-manifest.json")
        review = load(VALIDATION / "evidence-staged-review.json")
        privacy = load(VALIDATION / "evidence-privacy-adjudication.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(len(manifest["declared_self_exclusions"]), 3)
        self.assertEqual(set(review["expected_paths"]), {
            row["path"] for row in manifest["entries"]
        } | set(manifest["declared_self_exclusions"]))
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["x1_mutations"], [])
        self.assertEqual(review["outside_owner_paths"], [])
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        for entry in manifest["entries"]:
            blob = git("show", f":{entry['path']}").stdout
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])
            mode = git("ls-files", "-s", "--", entry["path"]).stdout.decode().split()[0]
            self.assertEqual(mode, entry["mode"])

    def test_all_staged_python_parses(self):
        manifest = load(VALIDATION / "evidence-index-manifest.json")
        python_paths = [row["path"] for row in manifest["entries"] if row["path"].endswith(".py")]
        self.assertGreaterEqual(len(python_paths), 13)
        for path in python_paths:
            source = git("show", f":{path}").stdout.decode("utf-8")
            ast.parse(source, filename=path)


if __name__ == "__main__":
    unittest.main()
