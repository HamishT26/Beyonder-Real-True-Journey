from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from scripts.ghc_family_lyren_moss_v666_v3_runtime import PHASE_ROOT, validate_contract


ROOT = Path(__file__).resolve().parents[1]
X1_SHA = "e121ea6e207ea032edb1a0825ed86b1334481213"


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


class LyrenV666V3X2Tests(unittest.TestCase):
    def test_exact_outcomes(self):
        ledger = load("x2/proposal-ledger.json")
        self.assertEqual(ledger["outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(len(ledger["proposals"]), 20)
        self.assertEqual(ledger["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_contracts_pass_and_mutations_fail_closed(self):
        directories = sorted((PHASE_ROOT / "x2" / "proposals").glob("lyr6663-n*"))
        self.assertEqual(len(directories), 20)
        rejected = 0
        for directory in directories:
            contract = json.loads((directory / "contract.json").read_text(encoding="utf-8"))
            valid, errors = validate_contract(contract)
            self.assertTrue(valid, errors)
            mutations = json.loads((directory / "mutation-results.json").read_text(encoding="utf-8"))["mutations"]
            self.assertEqual(len(mutations), 5)
            self.assertTrue(all(row["rejected"] and not row["accepted"] for row in mutations))
            rejected += len(mutations)
        self.assertEqual(rejected, 100)

    def test_method_flow_exact(self):
        flow = load("method-flow/x2-method-flow.json")
        self.assertEqual(flow["new_negative_count"], 100)
        self.assertEqual(flow["new_method_count"], 215)
        self.assertEqual(len(flow["rows"]), 215)
        self.assertEqual(flow["effective_after_x2_negatives"], 26388)
        self.assertEqual(flow["effective_after_x2_methods"], 10930)
        self.assertEqual(flow["failed_witness_count"], 100)

    def test_exact_replacement_immutable_x1_tree_has_no_later_paths(self):
        for name in ("x2", "evidence", "closeout", "seal", "final", "handoffs"):
            tree_rows = subprocess.check_output(
                [
                    "git",
                    "-C",
                    str(ROOT),
                    "ls-tree",
                    "-r",
                    "--name-only",
                    X1_SHA,
                    "--",
                    f"docs/lyren-moss/v666-v3/{name}",
                ],
                text=True,
            ).strip()
            self.assertEqual(tree_rows, "", name)

    def test_skills_and_runners_built(self):
        skills = load("x2/skill-catalog.json")
        runners = load("x2/runner-catalog.json")
        smoke = load("x2/tooling-smoke-receipt.json")
        self.assertEqual(skills["skill_count"], 10)
        self.assertTrue(skills["all_built_tested_used_bounded"])
        self.assertEqual(runners["runner_count"], 10)
        self.assertTrue(all(row["smoke_status"] == "passed" for row in runners["runners"]))
        self.assertEqual(smoke["passed_count"], 10)
        self.assertFalse(smoke["canonical_aggregate_invoked"])

    def test_portfolio_execution_and_protected_items(self):
        portfolio = load("x2/portfolio-execution.json")
        self.assertEqual(portfolio["method_count"], 95)
        self.assertEqual(portfolio["method_breakdown"], {"owner_safe_now": 30, "owner_candidates": 15, "owner_skills": 10, "owner_runners": 10, "owner_clean_fix_refine": 30})
        self.assertEqual(portfolio["external_actions"], 0)
        self.assertEqual(portfolio["protected_items_executed"], 0)
        self.assertTrue(all(row["completion_credit"] == 0 for rows in portfolio["successor_prepared_groups"].values() for row in rows))
        self.assertTrue(all(row["completion_credit"] == 0 for rows in portfolio["protected_unexecuted_groups"].values() for row in rows))

    def test_zero_call_and_trinity_boundaries(self):
        adapter = load("x2/source-adapter-zero-call.json")
        trinity = load("x2/trinity-representations.json")
        self.assertFalse(adapter["transport_enabled"])
        self.assertEqual(adapter["network_calls"], 0)
        self.assertEqual(adapter["rows_received"], 0)
        self.assertEqual(adapter["status"], "open_gap")
        self.assertEqual(trinity["primary_pillar"], "THOS Body")
        self.assertEqual(trinity["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_nonterminal_runners_pass(self):
        for name in ("contracts", "mutations", "json", "privacy", "security", "manifests", "accessibility", "truth"):
            completed = subprocess.run(
                ["python", str(ROOT / "scripts" / f"ghc_family_lyren_moss_v666_v3_{name}.py")],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="strict",
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(json.loads(completed.stdout)["valid"])

    def test_all_owner_text_is_utf8_lf(self):
        for path in PHASE_ROOT.rglob("*"):
            if path.is_file():
                raw = path.read_bytes()
                self.assertNotIn(b"\r", raw, str(path))
                raw.decode("utf-8")


if __name__ == "__main__":
    unittest.main()
