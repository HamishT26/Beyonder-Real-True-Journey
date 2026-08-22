#!/usr/bin/env python3
"""Bounded x2 tests for Sylven Arc v665-v5."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v665-v5"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import build_ghc_family_sylven_v665_v5_evidence as builder  # noqa: E402
from ghc_family_sylven_v665_v5_runner_core import evaluate  # noqa: E402


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=True
    ).stdout.strip()


def doc(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class SylvenV665V5X2Tests(unittest.TestCase):
    def test_01_exact_x1_start_and_frozen_parent(self):
        self.assertEqual(git("rev-parse", "HEAD"), builder.X1)
        self.assertEqual(git("rev-parse", "HEAD^"), builder.SOURCE_FINAL)
        self.assertEqual(git("branch", "--show-current"), builder.BRANCH)
        self.assertEqual(
            git("diff", "--name-only", builder.X1, "--", "docs/sylven-arc/v665-v5/x1"), ""
        )

    def test_02_x1_manifest_replayed_from_commit(self):
        receipt = doc("x2/ledgers/x1-integrity-replay.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["manifest_entry_count"], 15)
        self.assertEqual(receipt["manifest_mismatches"], [])
        self.assertEqual(receipt["x1_tree_changes_after_freeze"], [])

    def test_03_all_twenty_frozen_proposals_executed(self):
        ledger = doc("x2/ledgers/outcome-ledger.json")
        self.assertEqual(ledger["proposal_count"], 20)
        self.assertEqual(
            ledger["counts"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(set(row["outcome"] for row in ledger["outcomes"]), set(builder.ALLOWED_OUTCOMES))
        self.assertTrue(ledger["valid"])

    def test_04_all_mutations_executed_rejected_and_retained(self):
        ledger = doc("x2/ledgers/mutation-ledger.json")
        self.assertEqual(ledger["preregistered_count"], 100)
        self.assertEqual(ledger["executed_count"], 100)
        self.assertEqual(ledger["rejected_count"], 100)
        self.assertEqual(ledger["accepted_count"], 0)
        self.assertEqual(ledger["failure_erasure_count"], 0)
        self.assertEqual(len(set(ledger["mutation_ids"])), 100)
        self.assertTrue(ledger["valid"])

    def test_05_formal_profiles_are_typed_and_nonpromoting(self):
        for pid in ("sa6655-n008", "sa6655-n009", "sa6655-n010", "sa6655-n011", "sa6655-n012", "sa6655-n015"):
            contract = doc(f"x2/proposals/{pid}/contract.json")
            fixture = contract["positive_fixture"]
            result = evaluate(contract["runner_profile"], fixture)
            self.assertTrue(result["valid"], result)
            self.assertEqual(result["claim_ceiling"], "typed_symbolic_thermal_obligation_only")
            self.assertEqual(result["real_rows_processed"], 0)

    def test_06_open_gap_and_exact_gate_remain_open(self):
        open_receipt = doc("x2/proposals/sa6655-n019/bounded-receipt.json")
        gate_receipt = doc("x2/proposals/sa6655-n020/bounded-receipt.json")
        self.assertEqual(open_receipt["observed_disposition"], "open_gap")
        self.assertEqual(open_receipt["empirical_rows"], 0)
        self.assertEqual(gate_receipt["observed_disposition"], "exact_gate")
        self.assertEqual(gate_receipt["authority_events"], 0)
        source_use = doc("x2/ledgers/source-use-ledger.json")
        self.assertEqual(source_use["live_data_calls"], 0)
        self.assertEqual(source_use["downloaded_empirical_rows"], 0)

    def test_07_ten_skills_read_validated_and_smoke_used(self):
        registry = doc("x2/ledgers/skill-registry.json")
        self.assertEqual(registry["count"], 10)
        self.assertFalse(registry["global_installation_performed"])
        self.assertTrue(all(row["read_through_eof"] for row in registry["skills"]))
        self.assertTrue(all(row["quick_valid"] and row["smoke_valid"] for row in registry["skills"]))
        self.assertTrue(registry["valid"])

    def test_08_ten_family_runners_invoked(self):
        registry = doc("x2/ledgers/runner-registry.json")
        self.assertEqual(registry["count"], 10)
        self.assertTrue(registry["family_current_prefix_preserved"])
        self.assertTrue(all(Path(row["path"]).name.startswith("ghc_family_") for row in registry["runners"]))
        self.assertTrue(all(row["valid"] for row in registry["runners"]))
        self.assertTrue(registry["valid"])

    def test_09_portfolios_and_method_flow_preserve_gates_and_failures(self):
        portfolio = doc("x2/ledgers/portfolio-execution.json")
        self.assertEqual(len(portfolio["safe_now"]), 30)
        self.assertEqual(len(portfolio["bounded_candidates"]), 15)
        self.assertEqual(len(portfolio["exact_approval"]), 10)
        self.assertEqual(len(portfolio["blocked"]), 5)
        self.assertEqual(len(portfolio["clean_fix_refine"]), 30)
        self.assertTrue(all(row["outcome"] == "exact_gate" for row in portfolio["exact_approval"]))
        self.assertTrue(all(row["outcome"] == "open_gap" for row in portfolio["blocked"]))
        flow = doc("x2/ledgers/method-flow-overlay.json")
        self.assertEqual(flow["x2"]["new_failed_witnesses"], 100)
        self.assertEqual(flow["effective_after_x2"]["negatives"], 25662)
        self.assertEqual(flow["effective_after_x2"]["methods"], 9524)
        self.assertEqual(flow["x2"]["failure_erasure_count"], 0)
        self.assertTrue(flow["valid"])

    def test_10_execution_summary_has_zero_real_world_credit(self):
        summary = doc("x2/ledgers/execution-summary.json")
        self.assertEqual(summary["real_rows"], 0)
        self.assertEqual(summary["real_people"], 0)
        self.assertEqual(summary["real_studios_kilns_wares_glazes_or_materials"], 0)
        self.assertEqual(summary["real_keys_or_proofs"], 0)
        self.assertEqual(summary["authority_events"], 0)
        self.assertFalse(summary["full_repository_suite_run"])
        self.assertFalse(summary["independent_reproduction"])
        self.assertEqual(summary["terminal_verdict"], builder.TERMINAL_VERDICT)
        self.assertTrue(summary["valid"])

    def test_11_exact_staged_manifest_privacy_and_diff_hygiene(self):
        result = builder.check_staged()
        self.assertTrue(result["valid"])
        self.assertEqual(result["staged_paths"], len(builder.INTENDED_PATHS))
        self.assertEqual(result["privacy_confirmed_hits"], 0)
        self.assertEqual(result["diff_hygiene_issues"], 0)


if __name__ == "__main__":
    unittest.main()
