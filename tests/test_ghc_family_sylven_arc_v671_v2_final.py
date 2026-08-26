"""Exact-final owner-scoped lifecycle tests for Sylven Arc v671-v2."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_sylven_arc_v671_v2_signwork import (  # noqa: E402
    CHAIN_AFTER,
    CORE_LABELS,
    OWNER_ROOT,
    SOURCE_FINAL,
    X1_COMMIT,
    load_json,
)
from build_ghc_family_sylven_arc_v671_v2_final import EVIDENCE_COMMIT  # noqa: E402


EXPECTED_FINAL = os.environ.get("GHC_EXPECTED_FINAL", "")


def git_text(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def verify_manifest(path: Path, commit: str) -> None:
    manifest = load_json(path)
    if manifest["entry_count"] != len(manifest["entries"]):
        raise AssertionError(path)
    for entry in manifest["entries"]:
        blob = subprocess.run(["git", "show", f"{commit}:{entry['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
        if len(blob) != entry["bytes"] or hashlib.sha256(blob).hexdigest() != entry["sha256"]:
            raise AssertionError(entry["path"])


class SylvenArcV671V2FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = ROOT / OWNER_ROOT

    def test_01_exact_final_environment_binding(self):
        self.assertRegex(EXPECTED_FINAL, r"^[0-9a-f]{40}$")
        self.assertEqual(git_text("rev-parse", "HEAD"), EXPECTED_FINAL)

    def test_02_direct_single_parent_chain(self):
        self.assertEqual(git_text("rev-parse", f"{X1_COMMIT}^"), SOURCE_FINAL)
        self.assertEqual(git_text("rev-parse", f"{EVIDENCE_COMMIT}^"), X1_COMMIT)
        self.assertEqual(git_text("rev-parse", f"{EXPECTED_FINAL}^"), EVIDENCE_COMMIT)
        self.assertEqual(len(git_text("rev-list", "--parents", "-n", "1", EXPECTED_FINAL).split()), 2)

    def test_03_exactly_three_phase_commits_and_zero_merges(self):
        self.assertEqual(int(git_text("rev-list", "--count", f"{SOURCE_FINAL}..{EXPECTED_FINAL}")), 3)
        merges = git_text("rev-list", "--merges", f"{SOURCE_FINAL}..{EXPECTED_FINAL}")
        self.assertEqual(merges, "")

    def test_04_x1_exact_git_blob_manifest_replays(self):
        verify_manifest(self.root / "validation/x1-manifest.json", X1_COMMIT)

    def test_05_evidence_exact_git_blob_manifest_replays(self):
        verify_manifest(self.root / "validation/evidence-manifest.json", EVIDENCE_COMMIT)

    def test_06_final_owner_and_delta_manifests_replay(self):
        verify_manifest(self.root / "validation/final-owner-manifest.json", EXPECTED_FINAL)
        verify_manifest(self.root / "validation/final-delta-manifest.json", EXPECTED_FINAL)

    def test_07_phase_truth_has_exact_outcomes_and_terminal_verdict(self):
        truth = load_json(self.root / "closeout/phase-truth.json")
        self.assertEqual(truth["proposal_chain"], CHAIN_AFTER)
        self.assertEqual(truth["outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["source_final"], SOURCE_FINAL)
        self.assertEqual(truth["x1"], X1_COMMIT)
        self.assertEqual(truth["evidence"], EVIDENCE_COMMIT)

    def test_08_final_counts_are_additive_and_failures_not_erased(self):
        truth = load_json(self.root / "closeout/phase-truth.json")
        self.assertEqual(truth["effective_negatives"], 33707)
        self.assertEqual(truth["methods"], 20024)
        self.assertEqual(truth["failed_witnesses"], 5528)
        self.assertEqual(truth["passing_witnesses"], 7099)
        self.assertEqual(truth["open_gaps"], 259)
        self.assertEqual(truth["exact_gates"], 254)
        self.assertEqual(load_json(self.root / "closeout/retained-negative-register.json")["erased"], 0)

    def test_09_final_method_flow_retains_every_owner_failure(self):
        ledger = load_json(self.root / "closeout/method-flow-final.json")
        self.assertEqual(ledger["row_count"], 182)
        self.assertEqual(len(ledger["rows"]), 182)
        self.assertTrue(ledger["all_failures_retained"])
        self.assertTrue(ledger["all_recoveries_paired"])
        self.assertTrue(all(row["retained"] and row["completion_credit"] == 0 for row in ledger["rows"]))

    def test_10_x1_and_x2_failed_aggregates_keep_zero_credit(self):
        x1 = load_json(self.root / "x2/x1-test-composite.json")
        x2 = load_json(self.root / "closeout/x2-test-composite.json")
        self.assertEqual(x1["original_aggregate"]["aggregate_success_credit"], 0)
        self.assertEqual(x2["original_aggregate"]["aggregate_success_credit"], 0)
        self.assertFalse(x1["original_aggregate"]["replayed"])
        self.assertFalse(x2["original_aggregate"]["replayed"])
        self.assertEqual(x1["composite_observations"], {"passed": 24, "failed": 0})
        self.assertEqual(x2["composite_observations"], {"passed": 14, "failed": 0})

    def test_11_forty_proposals_and_four_labels_remain_exact(self):
        freeze = load_json(self.root / "x1/new-proposal-freeze.json")
        outcomes = load_json(self.root / "x2/outcome-ledger.json")
        self.assertEqual(len(freeze["rows"]), 40)
        self.assertEqual(len(outcomes["rows"]), 40)
        self.assertEqual(set(outcomes["counts"]), set(CORE_LABELS))

    def test_12_all_160_rejecting_mutations_remain_zero_credit(self):
        rows = [row for path in sorted((self.root / "x2/mutations").glob("*.json")) for row in load_json(path)["rows"]]
        self.assertEqual(len(rows), 160)
        self.assertTrue(all(not row["accepted"] and row["completion_credit"] == 0 for row in rows))

    def test_13_flashcard_deck_and_cards_remain_lossy_non_authoritative(self):
        deck = load_json(self.root / "x2/flashcard-deck.json")
        self.assertEqual(deck["card_count"], 40)
        self.assertFalse(deck["authoritative"])
        cards = sorted((self.root / "x2/cards").glob("*.json"))
        self.assertEqual(len(cards), 40)
        self.assertTrue(all(load_json(path)["lossy_projection"] and not load_json(path)["authoritative"] for path in cards))

    def test_14_tools_are_owner_local_smoke_used_and_not_globally_installed(self):
        runners = load_json(self.root / "tools/runner-smoke-receipt.json")
        skills = load_json(self.root / "tools/skill-smoke-receipt.json")
        quick = load_json(self.root / "tools/skill-quick-validation-receipt.json")
        self.assertEqual((runners["count"], skills["count"], quick["count"]), (10, 10, 10))
        self.assertEqual((runners["failures"], skills["failures"], quick["failures"]), (0, 0, 0))
        self.assertTrue(all(not row["global_installation"] for row in skills["rows"]))

    def test_15_exact_approval_and_blocked_portfolios_remain_held(self):
        for name, count in (("exact_approval", 20), ("blocked", 10)):
            payload = load_json(self.root / f"x2/portfolio-execution/{name}.json")
            self.assertEqual(payload["count"], count)
            self.assertTrue(all(row["x2_state"] == "held_unexecuted" and row["completion_credit"] == 0 for row in payload["rows"]))

    def test_16_open_gaps_exact_gates_and_zero_call_adapter_are_visible(self):
        gates = load_json(self.root / "closeout/open-exact-gate-register.json")
        adapter = load_json(self.root / "x2/source-adapter-status.json")
        self.assertEqual(gates["effective_open_gaps"], 259)
        self.assertEqual(gates["effective_exact_gates"], 254)
        self.assertFalse(adapter["enabled"])
        self.assertEqual(sum(adapter[key] for key in ("network_calls", "downloads", "rows", "images")), 0)

    def test_17_final_staged_reviews_are_valid_and_no_frozen_stage_changed(self):
        review = load_json(self.root / "validation/final-staged-review.json")
        privacy = load_json(self.root / "validation/final-staged-privacy.json")
        stale = load_json(self.root / "validation/stale-label-review.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["immutable_x1_x2_mutations"], [])
        self.assertEqual(review["out_of_scope"], [])
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(stale["valid"])
        self.assertEqual(stale["stale_labels_found"], [])

    def test_18_content_seal_canonical_payload_digest_is_exact(self):
        seal = load_json(self.root / "seal/content-seal.json")
        digest = hashlib.sha256(json.dumps(seal["canonical_payload"], sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        self.assertEqual(digest, seal["canonical_payload_sha256"])
        self.assertTrue(seal["immutable_after_commit"])

    def test_19_complete_incomplete_checklist_preserves_unmet_real_world_work(self):
        checklist = load_json(self.root / "closeout/complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(checklist["complete"]), 8)
        self.assertGreaterEqual(len(checklist["incomplete"]), 8)
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_20_environment_receipt_is_read_only_and_did_not_install(self):
        receipt = load_json(self.root / "closeout/environment-version-receipt.json")
        self.assertTrue(receipt["read_only_version_checks"])
        self.assertEqual(receipt["installations"], 0)
        self.assertEqual(receipt["updates"], 0)
        self.assertGreaterEqual(len(receipt["rows"]), 5)

    def test_21_static_report_has_structural_accessibility_scaffolding(self):
        text = (self.root / "closeout/static-report.html").read_text(encoding="utf-8")
        for fragment in ('<html lang="en">', '<title>', 'Skip to main content', '<main id="main">', '<caption>', '<th scope="col">', "NOT_READY_FOR_STAGE_20"):
            self.assertIn(fragment, text)
        self.assertNotIn("<script", text.lower())

    def test_22_overview_keeps_scientific_professional_and_authority_nonclaims(self):
        text = (self.root / "closeout/final-integrated-overview.md").read_text(encoding="utf-8")
        for phrase in ("participant-free proxy", "zero-key", "Theory of Everything", "complete privacy or accessibility assurance", "independent reproduction", "Maori authority", "consciousness", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(phrase, text)

    def test_23_route_is_prepared_not_sent_and_tavian_is_not_endpoint(self):
        route = load_json(self.root / "orchestration/route-state.json")
        baton = (self.root / "handoffs/caelen-morrow-v671-v3-activation-candidate.md").read_text(encoding="utf-8")
        self.assertEqual(route["delivery_state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["successor_contact_count"], 0)
        self.assertFalse(route["sent_by_sylven_arc"])
        self.assertIn("Caelen Morrow", baton)
        self.assertIn("SENT_BY_SYLVEN_ARC = false", baton)
        self.assertIn("Tavian Sol", baton)

    def test_24_canonical_prerequisite_is_pending_before_external_invocation(self):
        receipt = load_json(self.root / "final/final-validation-prerequisites.json")
        lifecycle = load_json(self.root / "closeout/lifecycle-replay.json")
        self.assertEqual(receipt["state"], "PENDING_EXTERNAL_EXACT_FINAL_CANONICAL")
        self.assertEqual(receipt["canonical_invocations"], 0)
        self.assertEqual(receipt["canonical_successes"], 0)
        self.assertEqual(receipt["canonical_invocation_budget"], 1)
        self.assertFalse(receipt["post_success_replay"])
        self.assertEqual(lifecycle["canonical_invocations"], 0)


if __name__ == "__main__":
    unittest.main()
