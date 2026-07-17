from __future__ import annotations

import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_v648_v1_definitions import (  # noqa: E402
    CANDIDATE_TITLES,
    CLEAN_TASK_TITLES,
    OUTCOME_CLASSES,
    PROPOSALS,
    RUNNER_TITLES,
    SAFE_TASK_TITLES,
    SKILL_SPECS,
    SOURCES,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = ROOT / "docs" / "tamar-vey" / "v648-v1"
SOURCE_FINAL = "4ada48d3142a6d33e4c723184edbb84e59e22aa4"


class V648V1X1Tests(unittest.TestCase):
    def test_exactly_ten_distinct_proposals(self) -> None:
        self.assertEqual(len(PROPOSALS), 10)
        self.assertEqual(len({row["title"].casefold() for row in PROPOSALS}), 10)

    def test_expected_distribution_and_vocabulary(self) -> None:
        counts = Counter(row["expected_disposition"] for row in PROPOSALS)
        self.assertEqual(counts, Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))
        self.assertEqual(set(counts), set(OUTCOME_CLASSES))

    def test_required_preregistration_fields(self) -> None:
        required = {
            "hypothesis",
            "null_or_failure",
            "approval_class",
            "execution_lane",
            "current_primary_or_official_source_needs",
            "concrete_artifacts",
            "test_falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for row in PROPOSALS:
            self.assertTrue(required.issubset(row), row["proposal_id"])

    def test_portfolio_floors(self) -> None:
        self.assertEqual((len(SAFE_TASK_TITLES), len(CANDIDATE_TITLES), len(SKILL_SPECS), len(RUNNER_TITLES), len(CLEAN_TASK_TITLES)), (30, 20, 20, 10, 30))

    def test_sources_and_negatives(self) -> None:
        self.assertEqual(len(SOURCES), 19)
        self.assertGreaterEqual(len(X1_OPERATIONAL_NEGATIVES), 4)
        self.assertTrue(all(row["retained"] for row in X1_OPERATIONAL_NEGATIVES))

    def test_generated_packet_is_x1_only(self) -> None:
        payload = json.loads((PHASE / "x1-proposals.json").read_text(encoding="utf-8"))
        self.assertFalse(payload["x2_execution_present"])
        self.assertEqual(payload["prior_frozen_proposal_count"], 550)
        self.assertEqual(payload["frozen_chain_count_after_x1"], 560)
        current = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
        phase_commits = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-list", "--reverse", f"{SOURCE_FINAL}..{current}"], text=True
        ).splitlines()
        if phase_commits:
            x1_commit = phase_commits[0]
            for relative in ("docs/tamar-vey/v648-v1/x2-proposal-ledger.json", "docs/tamar-vey/v648-v1/closeout-receipt.json"):
                probe = subprocess.run(
                    ["git", "-C", str(ROOT), "cat-file", "-e", f"{x1_commit}:{relative}"],
                    check=False,
                    capture_output=True,
                )
                self.assertNotEqual(probe.returncode, 0, relative)
        else:
            self.assertFalse((PHASE / "x2-proposal-ledger.json").exists())
            self.assertFalse((PHASE / "closeout-receipt.json").exists())


if __name__ == "__main__":
    unittest.main()
