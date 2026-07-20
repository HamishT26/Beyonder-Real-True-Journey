from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v650-v3"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V650V3X2Tests(unittest.TestCase):
    def test_exact_outcome_distribution(self):
        ledger = load("x2-evidence-ledger.json")
        self.assertEqual(ledger["proposal_count"], 20)
        self.assertEqual(ledger["distribution"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual({r["disposition"] for r in ledger["proposals"]}, {"completed", "represented", "open_gap", "exact_gate"})

    def test_all_mutations_rejected_and_preserved(self):
        result = load("validation/synthetic-mutation-results.json")
        self.assertEqual(result["count"], 100)
        self.assertEqual(result["executed"], 100)
        self.assertEqual(result["rejected_or_quarantined"], 100)

    def test_open_gap_and_exact_gate_are_nonpromoted(self):
        wmap = load("surfaces/wmap-zero-row/bounded-receipt.json")
        self.assertEqual(wmap["disposition"], "open_gap")
        self.assertEqual(wmap["real_rows"], 0)
        self.assertEqual(wmap["likelihood_evaluations"], 0)
        ferry = load("surfaces/ferry-authority/bounded-receipt.json")
        self.assertEqual(ferry["disposition"], "exact_gate")
        self.assertEqual(ferry["authority_decisions"], 0)

    def test_expanded_portfolios_executed(self):
        self.assertEqual(load("portfolios/safe-now-execution.json")["completed"], 40)
        self.assertEqual(load("portfolios/candidate-execution.json")["completed_within_lane"], 30)
        self.assertEqual(load("portfolios/skill-execution.json")["validated"], 20)
        self.assertEqual(load("portfolios/skill-execution.json")["smoke_used"], 20)
        self.assertEqual(load("portfolios/runner-execution.json")["invoked"], 10)
        self.assertEqual(load("portfolios/clean-fix-refine-execution.json")["completed"], 40)

    def test_skills_are_local_and_substantive(self):
        for row in load("portfolios/skill-execution.json")["skills"]:
            path = PHASE / "skills" / row["name"]
            self.assertTrue((path / "SKILL.md").is_file())
            self.assertTrue((path / "agents/openai.yaml").is_file())
            self.assertIn("Never convert", (path / "SKILL.md").read_text(encoding="utf-8"))
            self.assertFalse(row["global_install"])

    def test_runners_have_pass_and_reject_witnesses(self):
        for row in load("portfolios/runner-execution.json")["runners"]:
            self.assertTrue(row["invoked"])
            self.assertEqual(row["valid_returncode"], 0)
            self.assertEqual(row["mutation_returncode"], 2)
            self.assertTrue(row["valid_output"]["accepted"])
            self.assertFalse(row["mutation_output"]["accepted"])

    def test_negatives_and_gates_are_cumulative(self):
        negatives = load("retained-negative-register-evidence.json")
        self.assertEqual(negatives["activation_baseline"], 5692)
        self.assertEqual(negatives["x1_operational"], 11)
        self.assertEqual(negatives["synthetic_mutations"], 100)
        self.assertEqual(negatives["x2_operational"], 2)
        self.assertEqual(negatives["effective_total"], 5805)
        self.assertEqual(negatives["erased"], 0)
        gates = load("exact-open-gate-register-evidence.json")
        self.assertEqual(gates["effective_open_gaps"], 45)
        self.assertEqual(gates["effective_exact_gates"], 46)

    def test_accessible_report_and_overview(self):
        report = (PHASE / "accessible-report.html").read_text(encoding="utf-8")
        for needle in ('lang="en"', 'href="#main"', '<main id="main">', '<th scope="col">', 'tabindex="0"'):
            self.assertIn(needle, report)
        self.assertNotIn("<script", report.lower())
        words = len((PHASE / "integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 1750)
        self.assertLessEqual(words, 20000)

    def test_x1_frozen_blobs_remain_exact(self):
        manifest = load("validation/x1-staged-manifest.json")
        for row in manifest["entries"]:
            current = subprocess.run(["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(current.returncode, 0, row["path"])
            self.assertEqual(current.stdout.strip(), row["git_blob"], row["path"])

    def test_terminal_truth_remains_held(self):
        truth = load("phase-truth-evidence.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])
        self.assertEqual(load("orchestration/terminal-route-state-evidence.json")["state"], "HELD_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
