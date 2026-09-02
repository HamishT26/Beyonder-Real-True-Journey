from __future__ import annotations

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v684-v4"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
X1_SHA = "d1ea9dba1fab7d6726f11a15caf67a8531b70e4a"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(name: str):
    return json.loads((X2 / name).read_text(encoding="utf-8"))


class AurenV684V4X2Tests(unittest.TestCase):
    def test_x1_git_blob_replay(self) -> None:
        data = load("x1-git-blob-replay.json")
        self.assertEqual(data["x1"], X1_SHA)
        self.assertTrue(data["valid"])
        self.assertEqual(data["declared"], data["verified"])
        self.assertEqual(data["source_parent"], "0134e277a7f573e24e697037749d61d577163637")

    def test_contract_execution_count(self) -> None:
        ledger = load("contract-execution-ledger.json")
        self.assertEqual(ledger["entry_count"], 60)
        self.assertEqual(len(ledger["entries"]), 60)
        self.assertEqual(len({row["proposal_id"] for row in ledger["entries"]}), 60)

    def test_four_exact_outcome_labels(self) -> None:
        ledger = load("outcome-ledger.json")
        self.assertEqual(set(ledger["allowed_labels"]), ALLOWED)
        self.assertEqual(ledger["counts"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(Counter(row["outcome"] for row in ledger["entries"]), Counter(ledger["counts"]))

    def test_positive_controls(self) -> None:
        controls = load("positive-controls.json")
        self.assertEqual(controls["entry_count"], 60)
        self.assertEqual(controls["passed"], 60)
        self.assertTrue(all(row["accepted"] for row in controls["entries"]))
        self.assertTrue(all(row["evidence_scope"] == "bounded_synthetic_structure_only" for row in controls["entries"]))

    def test_all_invalid_mutations_rejected(self) -> None:
        mutations = load("rejecting-mutations.json")
        self.assertEqual(mutations["entry_count"], 300)
        self.assertEqual(mutations["rejected"], 300)
        self.assertEqual(mutations["completion_credit"], 0)
        self.assertTrue(all(row["rejected"] and row["completion_credit"] == 0 for row in mutations["entries"]))
        self.assertEqual(len({row["mutation_id"] for row in mutations["entries"]}), 300)

    def test_safe_and_candidate_execution(self) -> None:
        safe = load("safe-now-execution.json")
        candidates = load("candidate-execution.json")
        self.assertEqual((safe["entry_count"], safe["completed"]), (120, 120))
        self.assertTrue(all(not row["real_world_action"] for row in safe["entries"]))
        self.assertEqual((candidates["owner_entry_count"], candidates["owner_completed"]), (80, 80))
        self.assertEqual(candidates["successor_entry_count"], 20)
        self.assertEqual(candidates["successor_executed"], 0)

    def test_exact_and_blocked_packets_remain_held(self) -> None:
        holds = load("approval-hold-state.json")
        self.assertEqual((holds["exact_count"], holds["exact_executed"]), (20, 0))
        self.assertEqual((holds["blocked_count"], holds["blocked_executed"]), (10, 0))
        self.assertTrue(all(row["status"] == "held_unexecuted" for row in holds["exact_entries"]))
        self.assertTrue(all(row["status"] == "blocked_unexecuted" for row in holds["blocked_entries"]))

    def test_clean_fix_refine_execution(self) -> None:
        cfr = load("clean-fix-refine-execution.json")
        self.assertEqual((cfr["owner_entry_count"], cfr["owner_completed"]), (100, 100))
        self.assertEqual((cfr["successor_entry_count"], cfr["successor_executed"]), (30, 0))
        self.assertTrue(all(not row["destructive_action"] for row in cfr["owner_entries"]))

    def test_twenty_phase_local_skills_built_and_used(self) -> None:
        receipts = load("skill-use-receipts.json")
        self.assertEqual(receipts["summary"]["skill_count"], 20)
        self.assertEqual(receipts["summary"]["valid_count"], 20)
        self.assertEqual(receipts["summary"]["invalid_count"], 0)
        self.assertTrue(receipts["phase_local_only"])
        self.assertEqual(len(list((X2 / "skills").glob("*/SKILL.md"))), 20)
        self.assertEqual(len(list((X2 / "skills").glob("*/agents/openai.yaml"))), 20)

    def test_ten_phase_local_runners_built_and_used(self) -> None:
        receipts = load("runner-use-receipts.json")
        self.assertEqual(receipts["runner_count"], 10)
        self.assertEqual(receipts["valid_count"], 10)
        self.assertTrue(receipts["phase_local_only"])
        self.assertTrue(all(row["valid"] for row in receipts["receipts"]))
        self.assertEqual(len(list((X2 / "runners").glob("ghc_family_*_runner.py"))), 10)

    def test_no_global_installs_claimed(self) -> None:
        tools = load("bounded-tools.json")
        self.assertEqual(tools["new_global_package_installs"], 0)
        self.assertEqual(tools["new_global_skill_installs"], 0)
        self.assertIn("ceilings, not quotas", tools["reason"])

    def test_four_tier_flashcards(self) -> None:
        deck = json.loads((X2 / "flashcards" / "deck.json").read_text(encoding="utf-8"))
        self.assertEqual(deck["card_count"], 60)
        self.assertEqual(len(deck["cards"]), 60)
        self.assertTrue(all({"tier_1", "tier_2", "tier_3", "tier_4"} <= set(card) for card in deck["cards"]))
        self.assertEqual({card["outcome"] for card in deck["cards"]}, ALLOWED)

    def test_source_use_is_not_endorsement(self) -> None:
        receipt = load("source-use-receipt.json")
        self.assertEqual(receipt["source_count"], 7)
        self.assertFalse(receipt["endorsement_or_artifact_validation"])
        self.assertFalse(receipt["conformance_claim"])

    def test_method_flow_totals(self) -> None:
        flow = load("method-flow-x2.json")
        self.assertEqual(flow["new_failed_witnesses"], 303)
        self.assertEqual(flow["new_bounded_passing_witnesses"], 390)
        self.assertEqual(flow["new_methods"], 693)
        self.assertEqual(flow["effective_negatives"], 59083)
        self.assertEqual(flow["effective_methods"], 73653)
        self.assertEqual(flow["failed_witnesses"], 30744)
        self.assertEqual(flow["bounded_passing_witnesses"], 54189)
        self.assertEqual(len(flow["operational_failures"]), 3)
        self.assertTrue(flow["failed_witnesses_retained_zero_credit"])

    def test_evidence_truth_preserves_gates(self) -> None:
        truth = load("evidence-truth.json")
        self.assertEqual(truth["state"], "IMMUTABLE_X2_EVIDENCE_PREPARED")
        self.assertEqual(truth["open_gaps"], 525)
        self.assertEqual(truth["exact_gates"], 515)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(truth["same_owner_not_independent_reproduction"])
        for key in (
            "empirical_confirmation", "professional_authority", "production_readiness",
            "legal_or_cultural_ratification", "maori_authority", "privacy_complete",
            "accessibility_complete", "exhaustive_security", "independent_reproduction",
            "agi_or_asi", "consciousness_or_personhood", "theory_of_everything_proof", "stage20_authority",
        ):
            self.assertFalse(truth[key], key)

    def test_privacy_scan(self) -> None:
        scan = json.loads((VALIDATION / "evidence-privacy-scan.json").read_text(encoding="utf-8"))
        self.assertEqual(scan["confirmed_hit_count"], 0)
        self.assertTrue(scan["bounded_not_complete_privacy_assurance"])

    def test_evidence_manifest_replays_worktree_bytes(self) -> None:
        manifest = json.loads((VALIDATION / "evidence-index-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["x1"], X1_SHA)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertGreaterEqual(manifest["entry_count"], 70)
        for row in manifest["entries"]:
            data = (ROOT / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_strict_evidence_before_final(self) -> None:
        self.assertFalse((BASE / "final").exists())
        self.assertFalse((BASE / "closeout").exists())
        self.assertFalse((BASE / "handoffs").exists())

    def test_owner_file_ceiling(self) -> None:
        files = [path for path in BASE.rglob("*") if path.is_file()]
        self.assertLess(len(files), 2000)

    def test_overview_boundaries(self) -> None:
        text = (X2 / "integrated-evidence.md").read_text(encoding="utf-8")
        self.assertIn("relational working language only", text)
        self.assertIn("No coordinate, location, measurement", text)
        self.assertIn("Same-owner validation under shared infrastructure is not independent reproduction", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)


if __name__ == "__main__":
    unittest.main()
