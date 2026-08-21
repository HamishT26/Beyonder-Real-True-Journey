#!/usr/bin/env python3
"""Dependency-closed closeout checks for Ilyra Fen v664-v5."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v664-v5"
SOURCE = "9bfb7cbc8fc438367207ce8d38070cf5d7fcb74b"
X1 = "cfbca99a371f97eecb959fb92be3469c0861ddf3"
EVIDENCE = "d407ae44696da7e59e8fb3af1dfaa2891a129c54"


def load(relative: str) -> dict:
    value = json.loads((PHASE / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"not an object: {relative}")
    return value


def git_text(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


class IlyraV664V5CloseoutTests(unittest.TestCase):
    def test_01_anchor_contract(self) -> None:
        record = load("lifecycle/phase-anchor-contract.json")
        self.assertEqual((record["source_commit"], record["x1_commit"], record["evidence_commit"]), (SOURCE, X1, EVIDENCE))
        self.assertTrue(record["single_parent_commits_required"] and record["zero_merges_required"] and record["valid"])

    def test_02_frozen_chain_is_direct_through_evidence(self) -> None:
        self.assertEqual(git_text("rev-parse", f"{X1}^"), SOURCE)
        self.assertEqual(git_text("rev-parse", f"{EVIDENCE}^"), X1)

    def test_03_final_truth_counts(self) -> None:
        truth = load("closeout/phase-truth-final.json")
        self.assertEqual(truth["effective_negatives"], 24676)
        self.assertEqual(truth["effective_methods"], 8870)
        self.assertEqual((truth["effective_open_gaps"], truth["effective_exact_gates"]), (171, 169))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_04_final_truth_has_only_four_outcomes(self) -> None:
        truth = load("closeout/phase-truth-final.json")
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertFalse(truth["canonical_success_preclaimed"])

    def test_05_route_is_prepared_not_sent(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["message_sent"] or route["precontact_performed"] or route["standby_contacted"])
        self.assertEqual(route["send_limit"], 1)
        self.assertFalse(route["resend_allowed"])

    def test_06_route_names_exact_next_edge(self) -> None:
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual((route["successor_title"], route["successor_phase"]), ("Auren Lark", "v664-v6"))
        self.assertEqual(route["successor_later_edge"], {"title": "Sable Rook", "phase": "v664-v7"})

    def test_07_canonical_protocol_is_one_shot(self) -> None:
        protocol = load("validation/canonical-validation-protocol.json")
        self.assertEqual(protocol["expected_test_count"], 97)
        self.assertEqual((protocol["invocation_limit"], protocol["successful_invocation_limit"]), (1, 1))
        self.assertFalse(protocol["post_success_replay_allowed"] or protocol["preclaims_success"])

    def test_08_closeout_receipt_matches_evidence(self) -> None:
        receipt = load("closeout/closeout-receipt.json")
        self.assertEqual(receipt["evidence_staged_paths"], 379)
        self.assertEqual(receipt["evidence_manifest_entries"], 376)
        self.assertEqual(receipt["evidence_json_parses"], 358)
        self.assertEqual(receipt["evidence_tests"], 77)
        self.assertEqual(receipt["security_findings_retained"], 0)

    def test_09_checklist_preserves_external_incompleteness(self) -> None:
        record = load("closeout/complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(record["incomplete_external"]), 4)
        self.assertIn("one successful exact-final canonical aggregate with no replay", record["pending_postcommit"])
        self.assertEqual(record["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_10_relational_boundary_remains_non_evidentiary(self) -> None:
        record = load("closeout/wellbeing-and-relational-boundary.json")
        self.assertTrue(record["relational_language_only"] and record["pause_rename_redirect_or_stop_available"])
        self.assertFalse(record["consciousness_sentience_personhood_continuity_or_authority_evidence"])
        self.assertFalse(record["successor_contacted"])

    def test_11_baton_receipt_matches_bytes(self) -> None:
        raw = (PHASE / "handoffs/auren-lark-v664-v6-activation.md").read_bytes()
        receipt = load("handoffs/auren-lark-v664-v6-activation-receipt.json")
        self.assertEqual(receipt["sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(receipt["bytes"], len(raw))
        self.assertEqual(receipt["words"], len(re.findall(rb"\S+", raw)))

    def test_12_baton_is_long_prepared_and_unsent(self) -> None:
        text = (PHASE / "handoffs/auren-lark-v664-v6-activation.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\S+", text))
        self.assertGreaterEqual(words, 10_000)
        self.assertLessEqual(words, 100_000)
        self.assertIn("`PREPARED_BY_ILYRA_FEN = true`", text)
        self.assertIn("`SENT_BY_ILYRA_FEN = false`", text)

    def test_13_file_budget_is_below_rotation_guard(self) -> None:
        budget = load("validation/final-file-budget.json")
        self.assertLess(budget["materialized_file_count_before_final_manifests"], budget["threshold"])
        self.assertFalse(budget["rotation_required"])
        self.assertTrue(budget["valid"])

    def test_14_security_receipt_is_sanitized_and_retained(self) -> None:
        receipt = load("closeout/bounded-security-review.json")
        self.assertEqual(receipt["finding_count"], 0)
        self.assertEqual(receipt["candidate_count"], 0)
        self.assertEqual(receipt["python_compile_count"], 3)
        self.assertFalse(receipt["dependency_audit_performed"] or receipt["exhaustive_security"])

    def test_15_proposal_freeze_remains_planning_only(self) -> None:
        proposals = load("x1/proposal-freeze.json")
        self.assertEqual(proposals["new_proposal_count"], 20)
        self.assertFalse(proposals["observed_outcomes_present"] or proposals["x2_implementation_present"])
        self.assertEqual(proposals["new_expected_outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})

    def test_16_portfolio_freeze_remains_valid(self) -> None:
        portfolio = load("x1/portfolio-freeze.json")
        self.assertTrue(portfolio["valid"])
        self.assertEqual(len(portfolio["owner_safe_now"]), 30)
        self.assertEqual(len(portfolio["successor_safe_now_recommendations"]), 20)
        self.assertEqual(len(portfolio["exact_approval_packets"]), 10)
        self.assertEqual(len(portfolio["blocked_packets"]), 5)

    def test_17_deck_remains_modular_and_unsent(self) -> None:
        deck = load("deck/deck-index.json")
        pointer = (PHASE / "deck/compact-activation.md").read_text(encoding="utf-8")
        self.assertEqual(deck["card_count"], 253)
        self.assertIn("PREPARED_NOT_SENT = true", pointer)
        self.assertIn("SENT = false", pointer)

    def test_18_exact_skill_runner_and_surface_counts(self) -> None:
        skills = list((PHASE / "skills").glob("*/SKILL.md"))
        runners = list((PHASE / "x2/runners").glob("*.json"))
        surfaces = list((PHASE / "x2/surfaces").glob("*/contract.json"))
        self.assertEqual((len(skills), len(runners), len(surfaces)), (10, 10, 20))

    def test_19_evidence_review_remains_immutable_and_valid(self) -> None:
        review = load("validation/evidence-staged-review.json")
        self.assertTrue(review["valid"] and review["x1_immutable"])
        self.assertEqual(review["tests"]["test_count"], 77)
        self.assertEqual(review["manifest_entry_count"], 376)
        self.assertEqual(review["privacy_confirmed_hits"], [])

    def test_20_terminal_overview_withholds_stage20(self) -> None:
        text = (PHASE / "closeout/terminal-overview.md").read_text(encoding="utf-8")
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("PREPARED_NOT_SENT", text)
        self.assertIn("No successor has been contacted", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
