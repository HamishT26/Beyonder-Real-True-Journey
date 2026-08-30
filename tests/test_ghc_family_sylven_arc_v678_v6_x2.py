from __future__ import annotations

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v678-v6"
X1 = PHASE / "x1"
X2 = PHASE / "x2"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestSylvenArcV678V6X2(unittest.TestCase):
    def test_01_sixty_frozen_proposals_have_sixty_contracts_and_receipts(self):
        proposals = load(X1 / "new-proposal-freeze.json")["proposals"]
        self.assertEqual(len(proposals), 60)
        self.assertEqual(len(list((X2 / "contracts").glob("*.json"))), 60)
        self.assertEqual(len(list((X2 / "evidence").glob("*-receipt.json"))), 60)

    def test_02_contracts_are_zero_row_zero_action_and_non_authoritative(self):
        for path in (X2 / "contracts").glob("*.json"):
            row = load(path)
            self.assertEqual(row["real_world_rows"], 0)
            self.assertEqual(row["external_actions"], 0)
            self.assertEqual(row["measurements"], [])
            self.assertIsNone(row["raw_identifier"])
            self.assertFalse(row["real_world_authority"])
            self.assertFalse(row["empirical_confirmation"])
            self.assertFalse(row["production_ready"])

    def test_03_all_preregistered_mutations_were_rejected_and_retained(self):
        value = load(X2 / "mutation-execution.json")
        self.assertEqual(value["count"], 240)
        self.assertEqual(value["accepted_invalid_mutations"], 0)
        self.assertEqual(len(value["receipts"]), 240)
        self.assertTrue(all(row["status"] == "rejected_retained_zero_credit" for row in value["receipts"]))
        self.assertTrue(all(row["errors"] for row in value["receipts"]))

    def test_04_outcomes_use_only_four_labels_and_exact_counts(self):
        value = load(X2 / "proposal-outcomes.json")
        self.assertEqual(set(value["counts"]), LABELS)
        self.assertEqual(value["counts"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(Counter(row["outcome"] for row in value["outcomes"]), Counter(value["counts"]))

    def test_05_twenty_phase_local_skills_are_bounded_and_not_installed(self):
        value = load(X2 / "skill-validation-and-use.json")
        self.assertEqual(value["count"], 20)
        self.assertEqual(len(list((X2 / "skills").glob("*/SKILL.md"))), 20)
        for receipt in value["receipts"]:
            self.assertTrue(receipt["quick_validate_passed"])
            self.assertTrue(receipt["read_through_eof"])
            self.assertTrue(receipt["smoke_used"])
            self.assertFalse(receipt["global_install"])
            self.assertTrue(receipt["smoke"]["accepted"])

    def test_06_skill_contracts_preserve_zero_world_scope(self):
        for path in (X2 / "skills").glob("*/skill.json"):
            value = load(path)
            self.assertEqual(value["real_world_rows"], 0)
            self.assertEqual(value["external_actions"], 0)
            self.assertFalse(value["global_install"])
            self.assertTrue(value["initialized_with_official_skill_creator"])

    def test_07_ten_family_runners_were_positive_and_rejecting_smoke_used(self):
        value = load(X2 / "runner-validation-and-use.json")
        self.assertEqual(value["count"], 10)
        for receipt in value["receipts"]:
            self.assertEqual(receipt["positive_invocations"], 1)
            self.assertEqual(receipt["invalid_invocations"], 1)
            self.assertTrue(receipt["positive"]["accepted"])
            self.assertTrue(receipt["positive"]["expectation_met"])
            self.assertFalse(receipt["invalid"]["accepted"])
            self.assertTrue(receipt["invalid"]["expectation_met"])

    def test_08_portfolio_counts_and_protected_holds_are_exact(self):
        value = load(X2 / "portfolio-execution.json")
        self.assertEqual(len(value["safe_now"]), 60)
        self.assertEqual(len(value["candidate"]), 30)
        self.assertEqual(len(value["clean_fix_refine"]), 60)
        self.assertEqual(len(value["exact_approval"]), 20)
        self.assertEqual(len(value["blocked"]), 10)
        self.assertTrue(all(row["completion_credit"] == 0 for row in value["exact_approval"] + value["blocked"]))

    def test_09_method_flow_is_additive_and_retains_every_failure(self):
        value = load(X2 / "method-flow-execution.json")
        self.assertTrue(value["failure_erasure_forbidden"])
        self.assertGreater(value["overlay"]["effective_negatives"], value["base"]["effective_negatives"])
        self.assertGreater(value["overlay"]["effective_methods"], value["base"]["effective_methods"])
        self.assertEqual(value["overlay"]["retained_failed_witnesses"], value["base"]["retained_failed_witnesses"] + value["new_failed_witnesses"])

    def test_10_x2_truth_keeps_stage20_and_real_world_open(self):
        value = load(X2 / "x2-truth.json")
        self.assertEqual(value["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(value["real_world_rows"], 0)
        self.assertEqual(value["external_actions"], 0)
        self.assertEqual(value["skills_initialized_validated_read_and_used"], 20)
        self.assertEqual(value["runners_positive_and_rejecting_smoke_used"], 10)

    def test_11_source_ledger_never_converts_citations_to_observations(self):
        value = load(X2 / "source-and-provenance-ledger.json")
        self.assertEqual(value["network_calls_during_x2"], 0)
        self.assertEqual(value["downloaded_rows"], 0)
        self.assertIn("not observations", value["source_use_boundary"])

    def test_12_flashcard_deck_has_four_exact_tiers(self):
        value = load(X2 / "flashcards/deck-index.json")
        self.assertEqual(value["card_count"], 81)
        self.assertEqual(value["tier_counts"], {"1": 15, "2": 3, "3": 3, "4": 60})
        self.assertFalse(value["prompt_cache_guarantee"])
        self.assertFalse(value["identity_continuity_claim"])

    def test_13_flashcard_parent_chain_is_exact(self):
        cards = [load(path) for path in (X2 / "flashcards/cards").glob("*.json")]
        by_id = {card["card_id"]: card for card in cards}
        self.assertEqual(len(by_id), 81)
        for card in cards:
            self.assertIn(card["outcome"], LABELS)
            if card["tier"] == 1:
                self.assertEqual(card["parent_ids"], [])
            else:
                self.assertEqual(len(card["parent_ids"]), 1)
                self.assertEqual(by_id[card["parent_ids"][0]]["tier"], card["tier"] - 1)

    def test_14_flashcard_baton_has_thirteen_sections(self):
        value = load(X2 / "flashcards/baton-index.json")
        self.assertEqual(value["section_count"], 13)
        self.assertEqual(len(value["sections"]), 13)
        self.assertTrue(value["file_backed_packet_preferred"])

    def test_15_flashcard_manifest_replays_exact_bytes(self):
        value = load(X2 / "flashcards/card-manifest.json")
        self.assertEqual(value["self_exclusions"], ["card-manifest.json"])
        for entry in value["entries"]:
            path = X2 / "flashcards" / entry["path"]
            self.assertEqual(path.stat().st_size, entry["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), entry["sha256"])

    def test_16_flashcard_privacy_and_graph_receipts_pass(self):
        privacy = load(X2 / "flashcards/privacy-receipt.json")
        graph = load(X2 / "flashcards/card-graph.json")
        self.assertEqual(privacy["status"], "PASS")
        self.assertEqual(privacy["confirmed_hits"], 0)
        self.assertTrue(graph["acyclic_by_tier"])

    def test_17_accessibility_remains_structural_not_complete(self):
        text = (X2 / "flashcards/accessible-report.html").read_text(encoding="utf-8")
        self.assertIn("<main>", text)
        self.assertIn("<caption>", text)
        self.assertIn("assistive-technology", text)
        self.assertIn("remain reserved", text)

    def test_18_compact_activation_is_not_delivery_or_continuity_evidence(self):
        text = (X2 / "flashcards/compact-activation.md").read_text(encoding="utf-8")
        self.assertIn("not evidence of delivery, continuity, or authority", text)

    def test_19_threat_model_preserves_authority_and_reproduction_gates(self):
        text = (X2 / "threat-model.json").read_text(encoding="utf-8")
        for token in ("professional", "Māori-authority", "independent-reproduction", "Stage 20"):
            self.assertIn(token, text)

    def test_20_no_x2_core_document_claims_real_rows_or_actions(self):
        truth = load(X2 / "x2-truth.json")
        source = load(X2 / "source-and-provenance-ledger.json")
        self.assertEqual((truth["real_world_rows"], truth["external_actions"]), (0, 0))
        self.assertEqual((source["real_world_rows"], source["network_calls_during_x2"]), (0, 0))


if __name__ == "__main__":
    unittest.main()
