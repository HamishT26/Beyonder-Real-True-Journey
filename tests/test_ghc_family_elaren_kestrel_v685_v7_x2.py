"""Owner-scoped x2 tests for Elaren Kestrel v685-v7."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from scripts.ghc_family_elaren_kestrel_v685_v7_contracts import (
    execute_proposal,
    positive_fixture,
    validate_fixture,
)
from scripts.ghc_family_elaren_kestrel_v685_v7_runner_bank import run_contract

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elaren-kestrel" / "v685-v7"
X1 = BASE / "x1"
X2 = BASE / "x2"
SOURCE = "5d9ea649ab451f9b6790c75f774ba9e4faf07363"
X1_SHA = "0902e28aa1006b44a247e3d480797a4472bc1e58"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ElarenKestrelV685V7X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.proposals = load(X1 / "new-proposals.json")["proposals"]
        cls.evidence = load(X2 / "proposal-evidence.json")
        cls.mutations = load(X2 / "rejecting-mutations.json")
        cls.portfolio = load(X2 / "portfolio-execution.json")
        cls.skills = load(X2 / "skill-execution.json")
        cls.runners = load(X2 / "runner-execution.json")
        cls.promotions = load(X2 / "global-promotion-installation.json")
        cls.packages = load(X2 / "package-execution-summary.json")
        cls.flow = load(X2 / "method-flow-ledger.json")
        cls.truth = load(X2 / "phase-truth.json")
        cls.deck = load(X2 / "flashcards" / "deck-index.json")

    def test_01_x1_is_direct_source_child_and_ancestral(self) -> None:
        self.assertEqual(
            subprocess.run(["git", "rev-parse", f"{X1_SHA}^"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip(),
            SOURCE,
        )
        self.assertEqual(subprocess.run(["git", "merge-base", "--is-ancestor", X1_SHA, "HEAD"], cwd=ROOT).returncode, 0)

    def test_02_all_two_hundred_positive_contracts_pass(self) -> None:
        self.assertEqual(len(self.proposals), 200)
        for proposal in self.proposals:
            self.assertTrue(validate_fixture(proposal, positive_fixture(proposal))["accepted"], proposal["proposal_id"])

    def test_03_all_one_thousand_mutations_reject(self) -> None:
        self.assertEqual(self.mutations["executed_count"], 1000)
        self.assertEqual(self.mutations["rejected_count"], 1000)
        self.assertEqual(self.mutations["accepted_count"], 0)
        self.assertTrue(self.mutations["zero_completion_credit"])
        self.assertFalse(any(row["accepted"] for row in self.mutations["mutations"]))

    def test_04_outcomes_use_exact_four_labels(self) -> None:
        expected = {"completed": 170, "represented": 10, "open_gap": 10, "exact_gate": 10}
        self.assertEqual(self.evidence["outcome_counts"], expected)
        self.assertEqual(self.truth["outcomes"], expected)
        self.assertEqual(set(expected), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertEqual(len(self.evidence["outcomes"]), 200)

    def test_05_portfolio_executes_required_local_work_only(self) -> None:
        self.assertEqual(len(self.portfolio["safe_now"]), 300)
        self.assertEqual(len(self.portfolio["candidates"]), 250)
        self.assertEqual(len(self.portfolio["clean_fix_refine"]), 300)
        self.assertEqual(len(self.portfolio["exact_packets"]), 50)
        self.assertEqual(len(self.portfolio["blocked_packets"]), 30)
        self.assertTrue(all(not row["executed"] for row in self.portfolio["exact_packets"] + self.portfolio["blocked_packets"]))
        self.assertFalse(self.portfolio["destructive_cleanup"])

    def test_06_twenty_local_skills_pass_bounded_checks(self) -> None:
        self.assertEqual(self.skills["skill_count"], 20)
        self.assertTrue(all(row["official_quick_validate"] for row in self.skills["results"]))
        self.assertTrue(all(row["positive_fixture_accepted"] and row["adverse_fixture_rejected"] for row in self.skills["results"]))
        self.assertFalse(self.skills["global_installation"])

    def test_07_ten_local_runners_accept_and_reject(self) -> None:
        self.assertEqual(self.runners["runner_count"], 10)
        self.assertTrue(all(row["positive_passed"] and row["adverse_rejected"] for row in self.runners["results"]))
        for index in range(1, 11):
            self.assertTrue(run_contract(index, "positive")["accepted"])
            self.assertFalse(run_contract(index, "adverse")["accepted"])

    def test_08_global_promotions_are_exact_and_additive(self) -> None:
        self.assertEqual(self.promotions["status"], "PASS")
        self.assertEqual(self.promotions["installed_skill_count"], 10)
        self.assertEqual(self.promotions["unique_shared_runner_count"], 5)
        self.assertTrue(self.promotions["additive"])
        self.assertFalse(self.promotions["historical_skills_deleted"])
        self.assertFalse(self.promotions["plugin_cache_mutated"])
        self.assertTrue(all(row["byte_parity"] and row["quick_validate"] for row in self.promotions["skills"]))

    def test_09_package_transaction_is_thirteen_and_isolated(self) -> None:
        self.assertEqual(self.packages["direct_package_count"], 13)
        self.assertFalse(self.packages["shared_environment_mutation"])
        self.assertEqual(self.packages["initial_advisory_findings"], 7)
        self.assertEqual(self.packages["initial_advisory_success_credit"], 0)
        self.assertEqual(self.packages["advisory_recovery"], "PASS")
        self.assertEqual(self.packages["final_known_vulnerabilities"], 0)

    def test_10_package_smoke_composite_preserves_failed_aggregate(self) -> None:
        self.assertEqual(self.packages["initial_smoke_status"], "FAIL")
        self.assertEqual(self.packages["initial_smoke_success_credit"], 0)
        self.assertEqual(self.packages["isolated_smoke_recovery"], "PASS")
        self.assertEqual(self.packages["component_smoke_status"], "PASS_DEPENDENCY_CORRECTED_COMPOSITE")

    def test_11_flashcard_hierarchy_is_exact(self) -> None:
        self.assertEqual(self.deck["card_count"], 208)
        self.assertEqual(self.deck["tier_counts"], {"1": 1, "2": 3, "3": 4, "4": 200})
        self.assertEqual(len(self.deck["card_ids"]), 208)
        self.assertEqual(len(set(self.deck["card_ids"])), 208)
        cards = [load(path) for path in sorted((X2 / "flashcards" / "cards").glob("*.json"))]
        self.assertEqual(len(cards), 208)
        self.assertTrue(all(card["owner"] == "Elaren Kestrel" for card in cards))

    def test_12_baton_index_has_thirteen_sections(self) -> None:
        index = load(X2 / "flashcards" / "baton-index.json")
        self.assertEqual(index["section_count"], 13)
        self.assertEqual(len(index["sections"]), 13)
        self.assertFalse(load(X2 / "flashcards" / "stable-prefix.json")["cache_or_retention_claimed"])
        self.assertFalse(load(X2 / "flashcards" / "volatile-index.json")["implicit_completion"])

    def test_13_method_flow_counts_and_failure_retention(self) -> None:
        self.assertEqual(self.flow["counts"], {"methods": 1129, "failed": 1027, "passing": 1131})
        self.assertFalse(self.flow["recovery_erases_failure"])
        ids = {row["witness_id"] for row in self.flow["witnesses"]["failed"]}
        self.assertIn("EL6857-X2-N014-DETAIL-01", ids)
        self.assertIn("EL6857-X2-N015-DETAIL-03", ids)
        self.assertIn("EL6857-X2-N016-DETAIL-01", ids)
        self.assertIn("EL6857-X2-N017-DETAIL-02", ids)
        self.assertIn("EL6857-X2-N018-DETAIL-01", ids)
        self.assertEqual(len(ids), 1027)

    def test_14_effective_totals_are_additive(self) -> None:
        self.assertEqual(
            self.truth["totals"],
            {
                "effective_negatives": 64404,
                "effective_methods": 80969,
                "failed_witnesses": 35252,
                "bounded_passing_witnesses": 62814,
                "open_gaps": 582,
                "exact_gates": 569,
            },
        )
        self.assertEqual(self.truth["declared_proposal_chain"], 12030)

    def test_15_all_x2_json_documents_parse(self) -> None:
        paths = sorted(X2.rglob("*.json"))
        self.assertEqual(len(paths), 248)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_16_source_use_is_vocabulary_only(self) -> None:
        source = load(X2 / "source-use-receipt.json")
        self.assertEqual(source["real_rows_ingested"], 0)
        self.assertEqual(source["network_device_calls"], 0)
        self.assertFalse(source["citations_are_observations"])

    def test_17_complete_incomplete_gate(self) -> None:
        gate = load(X2 / "complete-incomplete-checklist.json")
        self.assertTrue(gate["required_work_complete"])
        self.assertTrue(gate["exact_and_blocked_unexecuted"])
        self.assertIn("future seat 02 creation", gate["incomplete_by_lifecycle"])

    def test_18_phase_remains_zero_row_and_not_stage20(self) -> None:
        self.assertEqual(self.truth["real_rows"], 0)
        self.assertEqual(self.truth["real_devices"], 0)
        self.assertEqual(self.truth["real_people"], 0)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_19_component_contract_reexecution_matches_committed_plan(self) -> None:
        sample = self.proposals[0]
        outcome, mutations = execute_proposal(sample)
        self.assertTrue(outcome["bounded_positive_accepted"])
        self.assertEqual(outcome["invalid_mutations_rejected"], 5)
        self.assertFalse(any(row["accepted"] for row in mutations))

    def test_20_no_successor_creation_is_claimed_in_x2(self) -> None:
        compact = (X2 / "flashcards" / "compact-activation.md").read_text(encoding="utf-8")
        self.assertIn("Prepared only", compact)
        self.assertIn("Future Seat 02", compact)
        self.assertIn("Neris Solane v686-v1", compact)


if __name__ == "__main__":
    unittest.main()
