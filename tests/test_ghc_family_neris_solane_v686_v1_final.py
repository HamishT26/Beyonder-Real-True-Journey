"""Final closeout checks for the exact Neris Solane v686-v1 owner surface."""
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import ghc_family_neris_solane_v686_v1_canonical as validation


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/neris-solane/v686-v1"


def read(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def normalized(path: Path) -> bytes:
    payload = path.read_bytes()
    return payload if path.suffix.lower() == ".pdf" else payload.replace(b"\r\n", b"\n")


class FinalGate(unittest.TestCase):
    def test_lifecycle_anchors_and_state(self):
        truth = read("final/phase-truth.json")
        self.assertEqual(truth["source"], "c6b56f912836a46a0dbb07c13aaf6e731e1b32e2")
        self.assertEqual(truth["x1"], "d16badcebf9d3b9b7c4ee7b8156d27bfc5a42323")
        self.assertEqual(truth["evidence"], "71f45ab2a9bb4ff239f09c79af5b94bc889b5127")
        self.assertEqual(truth["state"], "FINAL_PREPARED_CANONICAL_PENDING")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_outcomes_and_sealed_totals(self):
        truth = read("final/phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 170, "represented": 10, "open_gap": 10, "exact_gate": 10})
        self.assertEqual(truth["repository_seal"], {"effective_negatives": 66667, "effective_methods": 83162, "failed_witnesses": 37515, "bounded_passing_witnesses": 65007, "open_gaps": 602, "exact_gates": 589})
        self.assertEqual(truth["declared_proposal_chain"], 12430)

    def test_baton_is_complete_and_prepared_not_sent(self):
        integrity = read("final/baton-integrity.json")
        self.assertTrue(10000 <= integrity["words"] <= 100000)
        self.assertEqual(integrity["sections"], 13)
        self.assertTrue(integrity["x2_baton_preserved"])
        self.assertEqual(read("final/delivery-state.json")["state"], "PREPARED_NOT_SENT")

    def test_overview_pdf_and_visual_review(self):
        pdf = read("final/overview-pdf-validation.json")
        visual = read("final/overview-visual-review.json")
        self.assertGreaterEqual(pdf["pages"], 3)
        self.assertTrue(pdf["pdf_text_extraction_pass"] and pdf["terminal_verdict_present"])
        self.assertTrue(visual["all_pages_reviewed"])
        self.assertEqual(visual["layout_issues"], [])

    def test_content_seal_has_ten_exact_targets(self):
        seal = read("final/content-seal.json")
        self.assertEqual(len(seal["targets"]), 10)
        for row in seal["targets"]:
            payload = normalized(ROOT / row["path"])
            self.assertEqual((len(payload), hashlib.sha256(payload).hexdigest()), (row["bytes"], row["sha256"]), row["path"])

    def test_final_delta_manifest_replays_working_tree(self):
        replay = validation.replay_manifest("docs/neris-solane/v686-v1/validation/final-manifest.json")
        self.assertTrue(replay["valid"], replay["failures"][:5])

    def test_final_owner_manifest_replays_working_tree(self):
        replay = validation.replay_manifest("docs/neris-solane/v686-v1/validation/final-owner-manifest.json")
        self.assertTrue(replay["valid"], replay["failures"][:5])
        manifest = read("validation/final-owner-manifest.json")
        self.assertEqual(set(manifest["self_exclusions"]), {"docs/neris-solane/v686-v1/validation/final-manifest.json", "docs/neris-solane/v686-v1/validation/final-owner-manifest.json"})

    def test_flashcard_graph_remains_exact(self):
        result = validation.deck_check()
        self.assertTrue(result["valid"], result["failures"][:5])
        self.assertEqual(result["cards"], 208)

    def test_method_flow_links_and_counts_remain_exact(self):
        result = validation.method_check()
        self.assertTrue(result["valid"], result["failures"][:5])
        self.assertEqual(result["counts"], {"methods": 1094, "failed_witnesses": 1144, "bounded_passing_witnesses": 1094, "retained_negatives": 1144})

    def test_package_transaction_remains_three_direct_additions(self):
        install = read("x2/toolchain/installation-receipt.json")
        smoke = read("x2/toolchain/package-smokes.json")
        initial = read("x2/toolchain/package-smoke-initial-failure.json")
        self.assertEqual((install["direct_additions"], len(install["installed_distributions"])), (3, 3))
        self.assertEqual((smoke["positive_passed"], smoke["adverse_rejected"]), (3, 3))
        self.assertEqual(initial["aggregate_success_credit"], 0)

    def test_skill_installation_receipt_has_exact_parity(self):
        receipt = read("x2/global-promotion-installation.json")
        self.assertEqual((receipt["installed_count"], receipt["unique_shared_report_runners"]), (10, 5))
        self.assertTrue(all(row["byte_parity"] and row["post_copy_validation"]["valid"] for row in receipt["skills"]))

    def test_toolbox_validation_and_overlap_adjudication(self):
        self.assertTrue(read("tooling/catalogue-validation.json")["valid"])
        collisions = read("tooling/collisions.json")
        adjudication = read("tooling/collision-adjudication.json")
        self.assertEqual((collisions["finding_count"], len(adjudication["rows"])), (13, 13))
        self.assertFalse(adjudication["silent_winner"])

    def test_checklist_keeps_open_and_exact_work_visible(self):
        checklist = read("final/complete-incomplete-checklist.json")
        self.assertTrue(checklist["open_gap"] and checklist["exact_gate"])
        self.assertIn("exact final commit and push", checklist["pending_terminal"])
        self.assertIn("guarded future-seat-03 creation or reuse", checklist["pending_terminal"])

    def test_external_overlay_does_not_rewrite_repository_seal(self):
        overlay = read("final/external-overlay-before-final.json")
        self.assertEqual(overlay["event_count"], 4)
        self.assertEqual(overlay["repository_seal"]["effective_negatives"], 66667)
        self.assertEqual(overlay["pre_final_activation_baseline"]["effective_negatives"], 66671)
        self.assertEqual(overlay["repository_bytes_rewritten"], 0)

    def test_owner_tree_privacy_security_and_test_definition(self):
        tree = validation.tree_checks()
        self.assertTrue(tree["structure_valid"], tree["structure_failures"][:5])
        self.assertEqual(tree["privacy_confirmed_hits"], 0)
        self.assertEqual(tree["bounded_security_findings"], 0)
        manifest = read("final/test-definition-manifest.json")
        self.assertEqual(manifest["expected_selected_test_count"], 38)
        for row in manifest["tests"]:
            payload = normalized(ROOT / row["path"])
            self.assertEqual((len(payload), hashlib.sha256(payload).hexdigest()), (row["bytes"], row["sha256"]), row["path"])


if __name__ == "__main__":
    unittest.main()
