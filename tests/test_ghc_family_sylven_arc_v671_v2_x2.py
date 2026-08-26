"""Owner-scoped tests for Sylven Arc v671-v2 x2 evidence."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_sylven_arc_v671_v2_signwork import (  # noqa: E402
    CHAIN_AFTER,
    CORE_LABELS,
    INHERITED,
    OWNER_ROOT,
    PROTECTED_GATES,
    RUNNER_BINDINGS,
    X1_COMMIT,
    load_json,
    proposal_rows,
    validate_contract,
)


class SylvenArcV671V2X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = ROOT / OWNER_ROOT

    def test_x1_commit_is_exact_direct_parent_and_immutable(self):
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
        self.assertEqual(head, X1_COMMIT)
        changed = subprocess.run(["git", "diff", "--name-only", X1_COMMIT, "--", "docs/sylven-arc/v671-v2/x1", "scripts/build_ghc_family_sylven_arc_v671_v2_x1.py", "tests/test_ghc_family_sylven_arc_v671_v2_x1.py"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()
        self.assertEqual(changed, [])

    def test_frozen_proposals_are_exact_and_outcomes_use_four_labels(self):
        rows = proposal_rows(ROOT)
        self.assertEqual(len(rows), 40)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 40)
        self.assertEqual({row["expected_disposition"] for row in rows}, set(CORE_LABELS))
        truth = load_json(self.root / "x2/phase-truth-evidence.json")
        self.assertEqual(truth["proposal_chain"], CHAIN_AFTER)
        self.assertEqual(truth["outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})

    def test_all_contracts_are_structurally_valid_synthetic_and_non_authoritative(self):
        rows = proposal_rows(ROOT)
        contracts = sorted((self.root / "x2/contracts").glob("*.json"))
        self.assertEqual(len(contracts), 40)
        by_id = {row["proposal_id"]: row for row in rows}
        for path in contracts:
            payload = load_json(path)
            self.assertIn(payload["proposal_id"], by_id)
            self.assertTrue(validate_contract(payload, payload["proposal_id"])["passed"])
            self.assertTrue(payload["synthetic_only"])
            self.assertFalse(payload["authoritative"])
            self.assertTrue(all(value == 0 for value in payload["zero_counters"].values()))
            self.assertEqual(set(payload["protected_gates"]), set(PROTECTED_GATES))
            self.assertEqual(payload["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_160_preregistered_mutations_are_rejected_and_retained(self):
        ledgers = sorted((self.root / "x2/mutations").glob("mutation-ledger-*.json"))
        self.assertEqual(len(ledgers), 8)
        rows = [row for path in ledgers for row in load_json(path)["rows"]]
        self.assertEqual(len(rows), 160)
        self.assertEqual(len({row["mutation_id"] for row in rows}), 160)
        self.assertTrue(all(row["attempted"] and not row["accepted"] for row in rows))
        self.assertTrue(all(row["completion_credit"] == 0 and row["retained_failed_witness"] for row in rows))
        self.assertTrue(all(row["validation_failures"] for row in rows))

    def test_positive_controls_and_outcome_credit_are_bounded(self):
        positive = load_json(self.root / "x2/positive-controls.json")
        outcomes = load_json(self.root / "x2/outcome-ledger.json")
        self.assertEqual(positive["count"], 36)
        self.assertTrue(all(row["validation"]["passed"] for row in positive["rows"]))
        self.assertEqual(outcomes["counts"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        for row in outcomes["rows"]:
            self.assertEqual(row["completion_credit"], 1 if row["outcome"] == "completed" else 0)

    def test_flashcards_have_four_tiers_and_at_least_ten_sections(self):
        deck = load_json(self.root / "x2/flashcard-deck.json")
        cards = sorted((self.root / "x2/cards").glob("*.json"))
        self.assertEqual(deck["card_count"], 40)
        self.assertFalse(deck["authoritative"])
        self.assertEqual(len(cards), 40)
        for path in cards:
            card = load_json(path)
            self.assertEqual(len(card["tiers"]), 4)
            self.assertGreaterEqual(len(card["sections"]), 10)
            self.assertFalse(card["authoritative"])

    def test_portfolio_execution_is_exact_and_protected_work_is_held(self):
        expected = {
            "safe_now": 60,
            "candidates": 30,
            "clean_fix_refine": 60,
            "skills_built": 10,
            "skills_represented": 10,
            "runners": 10,
            "exact_approval": 20,
            "blocked": 10,
            "successor_skills": 10,
            "successor_runners": 10,
            "successor_clean_fix_refine": 30,
        }
        for kind, count in expected.items():
            payload = load_json(self.root / f"x2/portfolio-execution/{kind}.json")
            self.assertEqual(payload["count"], count)
            self.assertEqual(len(payload["rows"]), count)
            self.assertTrue(all(row["external_actions"] == 0 for row in payload["rows"]))
        for kind in ("exact_approval", "blocked"):
            payload = load_json(self.root / f"x2/portfolio-execution/{kind}.json")
            self.assertTrue(all(row["x2_state"] == "held_unexecuted" and row["completion_credit"] == 0 for row in payload["rows"]))

    def test_ten_owner_local_skills_and_runners_were_validated_and_smoke_used(self):
        runner_receipt = load_json(self.root / "tools/runner-smoke-receipt.json")
        skill_receipt = load_json(self.root / "tools/skill-smoke-receipt.json")
        quick = load_json(self.root / "tools/skill-quick-validation-receipt.json")
        self.assertEqual(runner_receipt["count"], len(RUNNER_BINDINGS))
        self.assertEqual(skill_receipt["count"], len(RUNNER_BINDINGS))
        self.assertEqual(quick["count"], len(RUNNER_BINDINGS))
        self.assertEqual(runner_receipt["failures"], 0)
        self.assertEqual(skill_receipt["failures"], 0)
        self.assertEqual(quick["failures"], 0)
        self.assertTrue(all(row["returncode"] == 0 and row["result"]["passed"] for row in runner_receipt["rows"]))
        self.assertTrue(all(row["smoke_runner_passed"] and not row["global_installation"] for row in skill_receipt["rows"]))
        self.assertTrue(all(row["passed"] for row in quick["rows"]))

    def test_method_flow_counts_retain_failures_and_recoveries_additively(self):
        ledger = load_json(self.root / "method-flow/evidence-ledger.json")
        summary = load_json(self.root / "method-flow/evidence-summary.json")
        self.assertEqual(ledger["new_method_count"], 178)
        self.assertEqual(ledger["new_failed_witnesses"], 178)
        self.assertEqual(ledger["new_bounded_recoveries"], 178)
        self.assertEqual(ledger["new_positive_witnesses"], 36)
        self.assertEqual(len(ledger["rows"]), 178)
        self.assertTrue(all(row["retained"] and row["completion_credit"] == 0 for row in ledger["rows"]))
        self.assertEqual(summary["effective_negatives"], INHERITED["effective_negatives"] + 178)
        self.assertEqual(summary["methods"], INHERITED["methods"] + 178)
        self.assertEqual(summary["failed_witnesses"], INHERITED["failed_witnesses"] + 178)
        self.assertEqual(summary["passing_witnesses"], INHERITED["passing_witnesses"] + 178 + 36)
        self.assertFalse(summary["repository_source_seal_rewritten"])

    def test_x1_failed_aggregate_is_not_laundered(self):
        receipt = load_json(self.root / "x2/x1-test-composite.json")
        self.assertEqual(receipt["original_aggregate"]["aggregate_success_credit"], 0)
        self.assertFalse(receipt["original_aggregate"]["replayed"])
        self.assertEqual(receipt["isolated_recovery"]["passed"], 2)
        self.assertEqual(receipt["isolated_recovery"]["successful_observations_replayed"], 0)
        self.assertFalse(receipt["canonical_validation"])

    def test_open_gaps_exact_gates_and_zero_call_adapter_remain_visible(self):
        gates = load_json(self.root / "x2/open-exact-gate-register.json")
        adapter = load_json(self.root / "x2/source-adapter-status.json")
        truth = load_json(self.root / "x2/phase-truth-evidence.json")
        self.assertEqual(gates["effective_open_gaps"], INHERITED["open_gaps"] + 2)
        self.assertEqual(gates["effective_exact_gates"], INHERITED["exact_gates"] + 2)
        self.assertFalse(adapter["enabled"])
        self.assertEqual(sum(adapter[key] for key in ("network_calls", "downloads", "rows", "images")), 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_privacy_security_and_evidence_validation_are_bounded_and_valid(self):
        privacy = load_json(self.root / "validation/evidence-privacy-scan.json")
        security = load_json(self.root / "validation/evidence-python-security-review.json")
        receipt = load_json(self.root / "validation/evidence-validation-receipt.json")
        staged_privacy = load_json(self.root / "validation/evidence-staged-privacy.json")
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(security["valid"])
        self.assertEqual(security["finding_count"], 0)
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["json_issues"], [])
        self.assertLess(receipt["materialized_files"], receipt["file_guard"])
        self.assertTrue(staged_privacy["valid"])
        self.assertEqual(staged_privacy["confirmed_hit_count"], 0)

    def test_evidence_staged_review_and_exact_git_blob_manifest(self):
        review = load_json(self.root / "validation/evidence-staged-review.json")
        manifest = load_json(self.root / "validation/evidence-manifest.json")
        self.assertTrue(review["valid"])
        self.assertTrue(review["x1_immutable"])
        self.assertEqual(review["frozen_x1_mutations"], [])
        self.assertEqual(review["out_of_scope"], [])
        self.assertEqual(manifest["hash_domain"], "exact_staged_git_blob")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            blob = subprocess.run(["git", "show", f":{entry['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
            self.assertEqual(len(blob), entry["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])

    def test_overview_preserves_scientific_professional_authority_and_stage20_boundaries(self):
        text = (self.root / "x2/integrated-evidence-overview.md").read_text(encoding="utf-8")
        required = [
            "synthetic signwriting", "zero-participant", "zero-key", "NOT_READY_FOR_STAGE_20",
            "Theory-of-Everything", "consciousness", "professional", "Maori authority",
            "independent reproduction", "complete privacy",
        ]
        for phrase in required:
            self.assertIn(phrase, text)
        self.assertRegex(text, r"complete privacy or accessibility assurance")
        self.assertFalse(re.search(r"\b(?:proved|confirmed) the Theory of Everything\b", text, re.I))


if __name__ == "__main__":
    unittest.main()
