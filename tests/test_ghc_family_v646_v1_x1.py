from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v646-v1"
sys.path.insert(0, str(ROOT / "scripts"))


class V646V1X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.proposals = json.loads((PHASE / "x1-proposals.json").read_text(encoding="utf-8"))
        cls.portfolio = json.loads((PHASE / "approval-packets/x1-approval-portfolio.json").read_text(encoding="utf-8"))
        cls.tools = json.loads((PHASE / "prototypes/x1-skill-runner-plan.json").read_text(encoding="utf-8"))

    def test_strict_x1_counts(self) -> None:
        self.assertEqual(self.proposals["prior_frozen_proposal_count"], 390)
        self.assertEqual(self.proposals["new_frozen_proposal_count"], 10)
        self.assertEqual(self.proposals["frozen_chain_count_after_x1"], 400)
        self.assertFalse(self.proposals["x2_execution_present"])

    def test_expected_distribution(self) -> None:
        self.assertEqual(self.proposals["expected_distribution"], {"completed":6,"represented":2,"open_gap":1,"exact_gate":1})

    def test_expanded_approval_portfolio(self) -> None:
        self.assertEqual(self.portfolio["counts"], {"safe_now":30,"candidates":20,"inherited_exact":10,"inherited_blocked":5})
        self.assertEqual(self.portfolio["completion_credit_before_x2"], 0)
        self.assertEqual(sum(x["origin"] == "predecessor_reframed_seed" for x in self.portfolio["safe_now"]), 15)

    def test_tool_and_cleanup_counts(self) -> None:
        self.assertEqual(len(self.tools["skills"]), 20)
        self.assertEqual(len(self.tools["runners"]), 10)
        cleanup = json.loads((PHASE / "maintenance/x1-clean-refine-plan.json").read_text(encoding="utf-8"))
        self.assertEqual(len(cleanup["tasks"]), 30)
        self.assertEqual(cleanup["destructive_task_count"], 0)

    def test_novelty_audits(self) -> None:
        audit = json.loads((PHASE / "provenance/prior-proposal-collision-audit.json").read_text(encoding="utf-8"))
        portfolio = json.loads((PHASE / "provenance/prior-portfolio-collision-audit.json").read_text(encoding="utf-8"))
        self.assertEqual(audit["exact_title_collision_count"], 0)
        self.assertEqual(len(audit["comparisons"]), 10)
        self.assertEqual(portfolio["exact_collision_count"], 0)

    def test_method_flow_and_negative_accounting(self) -> None:
        receipt = json.loads((PHASE / "method-flow/runner-validation.json").read_text(encoding="utf-8"))
        negatives = json.loads((PHASE / "validation/x1-operational-negatives.json").read_text(encoding="utf-8"))
        self.assertTrue(receipt["valid"])
        self.assertEqual(negatives["effective_after_x1"], 2503)

    def test_x1_review_module(self) -> None:
        spec = importlib.util.spec_from_file_location("review", ROOT / "scripts/ghc_family_v646_v1_x1_review.py")
        module = importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(module)
        self.assertTrue(module.structural()["valid"])
        self.assertTrue(module.privacy_from_worktree()["valid"])

    def test_x2_absent_from_immutable_x1_commit(self) -> None:
        x1_head = "7b7824b7643bfb3a80cf778a10ca65055554b5db"
        paths = set(subprocess.check_output(["git","ls-tree","-r","--name-only",x1_head],cwd=ROOT,text=True).splitlines())
        for name in ("phase-truth.json","x2-proposal-ledger.json","closeout-receipt.json","seal-receipt.json","final-validation-record.json"):
            self.assertNotIn(f"docs/eiren-kestrel/v646-v1/{name}", paths)


if __name__ == "__main__": unittest.main()
