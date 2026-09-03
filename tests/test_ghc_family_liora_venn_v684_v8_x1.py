#!/usr/bin/env python3
"""Lifecycle-local tests for Liora Venn v684-v8 planning-only x1."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "liora-venn" / "v684-v8"
X1 = PHASE / "x1"
VALIDATION = PHASE / "validation"
SOURCE = "de8e8830bd7cb3a9aa49b2eb5efadaf17e57d513"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class LioraVennV684V8X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.freeze = load(X1 / "new-proposal-freeze.json")
        cls.audit = load(X1 / "proposal-chain-audit.json")
        cls.portfolio = load(X1 / "portfolio-freeze.json")
        cls.truth = load(X1 / "phase-truth.json")
        cls.method = load(X1 / "method-flow-startup.json")
        cls.flashcards = load(X1 / "flashcard-freeze.json")
        cls.manifest = load(VALIDATION / "x1-index-manifest.json")
        cls.staged = load(VALIDATION / "x1-staged-review.json")
        cls.privacy = load(VALIDATION / "x1-privacy-scan.json")

    def test_x1_only_lifecycle(self):
        self.assertEqual(git("rev-parse", "HEAD"), SOURCE)
        self.assertFalse((PHASE / "x2").exists())
        self.assertFalse((PHASE / "final").exists())

    def test_proposal_count_and_unique_ids(self):
        rows = self.freeze["proposals"]
        self.assertEqual(len(rows), 60)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 60)
        self.assertEqual(len({row["title"].lower() for row in rows}), 60)

    def test_every_required_proposal_field(self):
        required = {
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "official_or_primary_source_needs",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for row in self.freeze["proposals"]:
            self.assertTrue(required <= set(row), row["proposal_id"])
            self.assertIn(row["expected_disposition"], LABELS)

    def test_expected_disposition_arithmetic(self):
        self.assertEqual(
            self.freeze["expected_disposition_counts"],
            {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        )

    def test_mutation_preregistration(self):
        mutations = [
            mutation
            for row in self.freeze["proposals"]
            for mutation in row["preregistered_rejecting_mutations"]
        ]
        self.assertEqual(len(mutations), 300)
        self.assertEqual(len({item["mutation_id"] for item in mutations}), 300)
        self.assertTrue(all(item["expected_result"] == "rejected_zero_credit" for item in mutations))

    def test_novelty_audit_has_no_collision_or_quarantine(self):
        self.assertEqual(self.audit["exact_title_collisions"], [])
        self.assertEqual(self.audit["quarantined_neighbors"], [])
        self.assertLess(self.audit["maximum_neighbor_score"], 0.78)
        self.assertEqual(self.audit["audit_scope"]["proposal_json_parse_failures"], [])

    def test_declared_chain_arithmetic(self):
        self.assertEqual(self.freeze["declared_chain_before"], 11150)
        self.assertEqual(self.freeze["declared_chain_after_if_committed"], 11210)
        self.assertEqual(self.freeze["declared_chain_after_if_committed"] - self.freeze["declared_chain_before"], 60)

    def test_inherited_reviews_are_zero_credit(self):
        data = load(X1 / "inherited-revalidation-freeze.json")
        self.assertEqual(data["review_count"], 60)
        self.assertEqual(data["novelty_credit"], 0)
        self.assertEqual(data["completion_credit"], 0)
        self.assertTrue(all(item["completion_credit"] == 0 for item in data["reviews"]))

    def test_portfolio_floors(self):
        self.assertEqual(len(self.portfolio["safe_now"]), 120)
        self.assertEqual(len(self.portfolio["owner_candidates"]), 80)
        self.assertEqual(len(self.portfolio["successor_candidates"]), 20)
        self.assertEqual(len(self.portfolio["exact_approval"]), 20)
        self.assertEqual(len(self.portfolio["blocked"]), 10)
        self.assertEqual(len(self.portfolio["owner_clean_fix_refine"]), 100)
        self.assertEqual(len(self.portfolio["successor_clean_fix_refine"]), 30)

    def test_skill_and_runner_plans(self):
        self.assertEqual(len(self.portfolio["owner_skill_ideas"]), 20)
        self.assertEqual(len(self.portfolio["owner_runner_ideas"]), 10)
        self.assertEqual(len(self.portfolio["successor_skill_ideas"]), 10)
        self.assertEqual(len(self.portfolio["successor_runner_ideas"]), 10)
        self.assertTrue(all(not item["global_install"] for item in self.portfolio["owner_skill_ideas"]))

    def test_primary_and_represented_pillars(self):
        self.assertEqual(self.portfolio["primary_pillar"], "Freed ID and CBR Heart")
        self.assertEqual(set(self.portfolio["represented_pillars"]), {"GMUT Mind", "THOS Body", "Freed ID and CBR Heart"})
        self.assertEqual(len(self.portfolio["owner_practice_lenses"]), 1)

    def test_method_flow_retains_every_startup_failure(self):
        self.assertEqual(self.method["new_failure_count"], 16)
        self.assertEqual(len(self.method["new_failures"]), 16)
        self.assertFalse(self.method["failure_erasure"])
        self.assertFalse(self.method["recoveries_promote_failed_witnesses"])

    def test_method_flow_count_arithmetic(self):
        counts = self.method["effective_x1_startup_counts"]
        self.assertEqual(counts["effective_negatives"], 60394)
        self.assertEqual(counts["effective_methods"], 75142)
        self.assertEqual(counts["failed_witnesses"], 31455)
        self.assertEqual(counts["bounded_passing_witnesses"], 55677)
        self.assertEqual(len(self.method["source_external_overlay_witnesses"]), 3)
        self.assertTrue(all(not row["failed_witness_promoted"] for row in self.method["source_external_overlay_witnesses"]))

    def test_official_sources_are_vocabulary_only(self):
        data = load(X1 / "official-primary-source-ledger.json")
        self.assertEqual(len(data["entries"]), 8)
        self.assertEqual(data["real_data_rows"], 0)
        self.assertEqual(data["network_data_queries"], 0)
        self.assertFalse(data["citations_are_observations"])
        self.assertFalse(data["authority_conferred"])

    def test_no_observed_outcomes_in_x1(self):
        self.assertEqual(self.truth["lifecycle"], "PLANNING_ONLY_X1")
        self.assertEqual(self.truth["observed_outcome_count"], 0)
        self.assertFalse(self.truth["x2_implementation_present"])
        self.assertFalse(self.freeze["x2_outcomes_present"])

    def test_route_is_held(self):
        route = load(X1 / "route-plan.json")
        self.assertEqual(route["route_state"], "TERMINAL_GATE_HELD")
        self.assertEqual(route["prospective_successor_title"], "Tamar Vey")
        self.assertEqual(route["prospective_successor_phase"], "v685-v1")
        self.assertEqual(route["send_count"], 0)
        self.assertFalse(route["precontacted"])
        self.assertFalse(route["created_or_forked_task"])

    def test_approval_work_is_unexecuted(self):
        approval = load(X1 / "approval-hold-register.json")
        self.assertEqual(approval["exact_approval_count"], 20)
        self.assertEqual(approval["blocked_count"], 10)
        self.assertEqual(approval["executed_count"], 0)

    def test_four_tier_flashcards_are_content_addressed_and_resolved(self):
        cards = self.flashcards["cards"]
        self.assertEqual(self.flashcards["hierarchy"], "owner_to_pillar_to_practice_to_task_evidence")
        self.assertEqual(self.flashcards["tier_counts"], {"owner": 1, "pillar": 3, "practice": 3, "task_evidence": 60})
        self.assertEqual(len(cards), 67)
        self.assertEqual(len({card["card_id"] for card in cards}), 67)
        identifiers = {card["card_id"] for card in cards}
        for card in cards:
            parent = card["parent_card_id"]
            self.assertTrue(parent is None or parent in identifiers, card["card_id"])
            payload = {key: value for key, value in card.items() if key != "content_sha256"}
            encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            self.assertEqual(card["content_sha256"], hashlib.sha256(encoded).hexdigest(), card["card_id"])
        self.assertFalse(self.flashcards["x2_evidence_present"])
        self.assertEqual(self.flashcards["erased_cards"], 0)

    def test_manifest_hash_and_path_parity(self):
        entries = self.manifest["entries"]
        exclusions = set(self.manifest["declared_self_exclusions"])
        self.assertEqual(len(entries), self.manifest["entry_count"])
        actual = set(exclusions)
        for entry in entries:
            path = ROOT / entry["path"]
            value = normalized(path)
            self.assertEqual(len(value), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(value).hexdigest(), entry["sha256"], entry["path"])
            actual.add(entry["path"])
        self.assertEqual(actual, set(self.staged["expected_paths"]))
        self.assertEqual(len(actual), self.staged["expected_path_count"])

    def test_privacy_scan_has_no_confirmed_hit(self):
        self.assertEqual(self.privacy["confirmed_hit_count"], 0)
        self.assertEqual(self.privacy["confirmed_hits"], [])
        self.assertEqual(len(self.privacy["privacy_classes"]), 5)

    def test_caps_and_terminal_verdict(self):
        self.assertEqual(self.portfolio["materialized_file_stop"], 2000)
        self.assertEqual(self.portfolio["document_word_cap"], 100000)
        self.assertEqual(self.portfolio["commit_cap"]["total"], 3)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
