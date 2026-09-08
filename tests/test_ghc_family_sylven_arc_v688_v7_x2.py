#!/usr/bin/env python3
"""Owner-scoped tests for the Sylven Arc v688-v7 x2 evidence packet."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/sylven-arc/v688-v7"
X2 = BASE / "x2"
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_chess_records_core as core


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")


class TestSylvenArcV688V7X2(unittest.TestCase):
    def test_01_frozen_proposal_shape(self):
        packet = load(BASE / "x1/new-proposals.json")
        self.assertEqual(packet["count"], 200)
        self.assertEqual(packet["chain_after"], 16830)
        self.assertTrue(all(item["planning_only"] for item in packet["proposals"]))

    def test_02_all_frozen_contracts_match_core(self):
        proposals = load(BASE / "x1/new-proposals.json")["proposals"]
        self.assertEqual(sum(core.matches_contract(item, core.evaluate(item["input"])) for item in proposals), 200)

    def test_03_contract_artifact_count(self):
        self.assertEqual(len(list((X2 / "contracts").glob("*.json"))), 200)

    def test_04_contract_artifacts_match_expected_and_observed(self):
        proposals = load(BASE / "x1/new-proposals.json")["proposals"]
        for index, proposal in enumerate(proposals, 1):
            record = load(X2 / "contracts" / f"{index:03d}.json")
            self.assertEqual(record["proposal_id"], proposal["proposal_id"])
            self.assertEqual(record["expected"], core.expected_envelope(proposal))
            self.assertEqual(record["observed"], core.evaluate(proposal["input"]))
            self.assertTrue(record["matches"] and record["input_unchanged"])

    def test_05_outcomes_are_exact(self):
        self.assertEqual(load(X2 / "phase-truth.json")["outcomes"], {"completed": 176, "represented": 11, "open_gap": 3, "exact_gate": 10})

    def test_06_portfolio_shape_and_predicates(self):
        receipt = load(X2 / "portfolio-results.json")
        self.assertEqual(receipt["counts"], {"safe_now": 300, "candidates": 250, "clean_fix_refine": 300})
        self.assertEqual(len(receipt["rows"]), 850)
        self.assertTrue(all(item["predicate_pass"] for item in receipt["rows"]))

    def test_07_exact_and_blocked_packets_remain_unexecuted(self):
        receipt = load(X2 / "portfolio-results.json")
        self.assertEqual(receipt["exact_packets_unexecuted"], 50)
        self.assertEqual(receipt["blocked_packets_unexecuted"], 30)

    def test_08_negative_controls_are_retained(self):
        receipt = load(X2 / "negative-controls.json")
        self.assertEqual(receipt["count"], 493)
        self.assertEqual(receipt["new_unique_negative_count"], 511)
        self.assertTrue(all(item["completion_credit"] == 0 for item in receipt["negative_records"]))

    def test_09_correction_overlay_retains_two_failures(self):
        receipt = load(X2 / "correction1/recovery-receipt.json")
        self.assertEqual(receipt["state"], "VALID_ADDITIVE_RECOVERY")
        self.assertEqual(len(receipt["retained_failures"]), 2)
        self.assertEqual(receipt["successful_base_contracts_replayed"], 0)

    def test_10_method_flow_base_is_valid(self):
        ledger = load(X2 / "method-flow/ledger.json")
        validation = load(X2 / "method-flow/validation.json")
        self.assertEqual(ledger["counts"], {"methods": 53, "witnesses": 609, "failed_witnesses": 541, "passing_witnesses": 68, "state_events": 53, "recommendations": 53})
        self.assertTrue(validation["valid"])

    def test_11_method_flow_overlay_is_additive(self):
        overlay = load(X2 / "correction1/method-flow-overlay.json")
        self.assertEqual(overlay["correction_counts"], {"methods": 2, "witnesses": 4, "failed_witnesses": 2, "passing_witnesses": 2, "state_events": 2, "recommendations": 2})
        self.assertEqual(overlay["combined_counts"], {"methods": 55, "witnesses": 613, "failed_witnesses": 543, "passing_witnesses": 70, "state_events": 55, "recommendations": 55})
        self.assertEqual(overlay["failed_witnesses_erased"], 0)

    def test_12_package_transaction_is_isolated(self):
        receipt = load(X2 / "package-transaction.json")
        self.assertEqual(receipt["state"], "COMPLETE")
        self.assertEqual(receipt["direct_count"], 3)
        self.assertFalse(receipt["global_python_mutated"])
        self.assertEqual(set(receipt["smokes"]["smokes"]), {"chess", "lark", "networkx"})

    def test_13_advisory_snapshot_is_bounded(self):
        receipt = load(X2 / "package-advisory-snapshot.json")
        self.assertEqual(receipt["query_count"], 3)
        self.assertFalse(receipt["exhaustive_security"])

    def test_14_local_tool_validation(self):
        receipt = load(X2 / "local-tool-validation.json")
        self.assertEqual(receipt["state"], "VALID_LOCAL_OWNER_TOOLS")
        self.assertEqual((receipt["skill_count"], receipt["runner_count"]), (10, 5))
        self.assertEqual((receipt["accepting_smoke_count"], receipt["adverse_rejection_count"]), (40, 40))

    def test_15_promotion_byte_parity_and_no_overwrite(self):
        receipt = load(X2 / "promotion-receipt.json")
        self.assertEqual(receipt["state"], "PROMOTED_VALIDATED_BYTE_EQUAL")
        self.assertEqual(receipt["overwrites"], 0)
        self.assertTrue(all(item["byte_equal"] for item in receipt["parity"]))

    def test_16_skill_packages_have_no_todo(self):
        folders = list((BASE / "skills").iterdir())
        self.assertEqual(len(folders), 10)
        for folder in folders:
            text = (folder / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("TODO", text)
            self.assertTrue((folder / "agents/openai.yaml").is_file())
            self.assertTrue((folder / "scripts/ghc_family_chess_record_skill.py").is_file())

    def test_17_family_current_runner_shape(self):
        plan = load(BASE / "x1/tool-package-plan.json")
        self.assertEqual(len(plan["runners"]), 5)
        for item in plan["runners"]:
            text = (ROOT / "scripts" / item["name"]).read_text(encoding="utf-8")
            self.assertIn("ghc_family_chess_records_core", text)
            self.assertTrue(item["name"].startswith("ghc_family_"))

    def test_18_four_tier_deck_shape(self):
        deck = load(X2 / "deck/deck-index.json")
        self.assertEqual(deck["card_count"], 263)
        self.assertEqual(deck["tier_counts"], {"1": 1, "2": 3, "3": 4, "4": 255})
        self.assertTrue(deck["acyclic_parent_graph"])

    def test_19_card_content_addresses_and_parents(self):
        deck = load(X2 / "deck/deck-index.json")
        identifiers = set(deck["cards"])
        for identifier in identifiers:
            card = load(X2 / "deck/cards" / f"{identifier}.json")
            material = dict(card)
            material.pop("card_id")
            self.assertEqual(identifier, "ghc-card-" + hashlib.sha256(canonical(material)).hexdigest()[:24])
            self.assertTrue(all(parent in identifiers for parent in card["parent_ids"]))

    def test_20_card_manifest_replays(self):
        manifest = load(X2 / "deck/card-manifest.json")
        for item in manifest["entries"]:
            path = ROOT / item["path"]
            self.assertTrue(path.is_file())
            self.assertEqual(len(path.read_bytes()), item["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["sha256"])

    def test_21_effective_counts_are_exact(self):
        self.assertEqual(load(X2 / "phase-truth.json")["effective_counts"], {"proposals": 16830, "negatives": 85417, "methods": 94117, "failed_witnesses": 56295, "passing_witnesses": 86180, "open_gaps": 765, "exact_gates": 785})

    def test_22_terminal_boundaries_hold(self):
        truth = load(X2 / "phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["canonical_invocations"], 0)
        self.assertEqual(truth["successor_contacts"], 0)

    def test_23_accessible_report_structure(self):
        text = (X2 / "accessible-report.html").read_text(encoding="utf-8")
        for token in ("<main>", "<h1>", "<nav", "<table>", "<caption>", 'scope="col"', 'scope="row"', "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, text)
        self.assertIn("assistive-technology", text)

    def test_24_no_real_or_external_execution_claims(self):
        portfolio = load(X2 / "portfolio-results.json")
        wellbeing = load(X2 / "workload-wellbeing.json")
        self.assertEqual(portfolio["real_games"], 0)
        self.assertEqual(portfolio["participant_records"], 0)
        self.assertEqual(wellbeing["subagents"], 0)
        self.assertEqual(wellbeing["delegation"], 0)


if __name__ == "__main__":
    unittest.main()
