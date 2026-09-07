#!/usr/bin/env python3
"""Bounded x2 evidence tests for Orin Thale v687-v7."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v687-v7"
X1_ROOT = PHASE / "x1"
X2 = PHASE / "x2"
VALIDATION = PHASE / "validation"
SOURCE = "28dfdf1a3e9a1023f1e83f19fb267e57878b9d0b"
X1 = "7aea73908f8f41ed38473d6e30e5f1bda36588a7"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def norm(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class OrinThaleV687V7X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.truth = load(X2 / "phase-truth.json")
        cls.contracts = load(X2 / "contract-results.json")
        cls.mutations = load(X2 / "mutation-results.json")
        cls.portfolio = load(X2 / "portfolio-results.json")

    def test_lifecycle_starts_at_immutable_x1(self):
        self.assertEqual(git("rev-parse", "HEAD"), X1)
        self.assertEqual(git("rev-parse", "HEAD^"), SOURCE)

    def test_contracts_all_match(self):
        self.assertEqual(self.contracts["count"], 200)
        self.assertTrue(self.contracts["all_complete_outputs_matched"])
        self.assertTrue(all(row["complete_output_matched"] and row["input_preserved"] for row in self.contracts["rows"]))

    def test_outcome_arithmetic_and_labels(self):
        self.assertEqual(set(self.truth["outcomes"]), LABELS)
        self.assertEqual(self.truth["outcomes"], {"completed": 125, "represented": 39, "open_gap": 20, "exact_gate": 16})

    def test_all_mutations_rejected(self):
        self.assertEqual(self.mutations["count"], 1000)
        self.assertEqual(self.mutations["rejected"], 1000)
        self.assertEqual(self.mutations["original_success_credit"], 0)
        self.assertTrue(all(row["rejected"] for row in self.mutations["rows"]))

    def test_portfolio_execution_and_holds(self):
        self.assertEqual(sum(row["executed"] for row in self.portfolio["safe_now"]), 300)
        self.assertEqual(sum(row["executed"] for row in self.portfolio["candidates"]), 250)
        self.assertEqual(sum(row["executed"] for row in self.portfolio["clean_fix_refine"]), 300)
        self.assertEqual(len(self.portfolio["exact_packets"]), 50)
        self.assertEqual(len(self.portfolio["blocked_packets"]), 30)
        self.assertTrue(all(row["state"] == "held_unexecuted" for row in self.portfolio["exact_packets"] + self.portfolio["blocked_packets"]))

    def test_skills_and_runners(self):
        skills = load(X2 / "skill-validation.json")
        runners = load(X2 / "runner-smokes.json")
        self.assertEqual(skills["count"], 10)
        self.assertEqual(runners["count"], 5)
        self.assertTrue(all(row["quick_validation"] == "PASSED" and row["smoke_use"] == "PASSED" for row in skills["skills"]))
        self.assertTrue(all(row["positive_smoke"] == "PASSED" and row["duplicate_key_smoke"] == "REJECTED" for row in runners["rows"]))

    def test_packages_locked_and_smoked(self):
        env = load(X2 / "environment-receipt.json")
        smokes = load(X2 / "package-smokes.json")
        self.assertEqual(env["wheel_count"], 13)
        self.assertTrue(env["require_hashes"] and env["no_index_install"] and env["wheel_only"])
        self.assertEqual(env["direct_additions"], {"astropy": "8.0.1", "asdf": "5.4.0", "uncertainties": "3.2.3"})
        self.assertTrue(all(row["positive"] and row["adverse"] for row in smokes["direct"]))
        self.assertEqual(len(smokes["operational_failures"]), 2)
        self.assertFalse(smokes["failure_erasure"])

    def test_promotion_complete(self):
        receipt = load(X2 / "promotion-receipt.json")
        correction = load(X2 / "promotion-correction-receipt.json")
        self.assertEqual(receipt["status"], "PROMOTED_COLLISION_FREE_VALIDATED_AND_USED")
        self.assertEqual(receipt["skills"], 10)
        self.assertEqual(receipt["runners"], 5)
        self.assertEqual(receipt["overwrites"], 0)
        self.assertTrue(all(row["matched"] for row in receipt["global_runner_smokes"]))
        self.assertEqual(correction["status"], "CORRECTED_PROMOTION_PRIVACY_CLEAN")
        self.assertEqual(correction["original_member_count"], 66)
        self.assertEqual(correction["final_member_count"], 56)
        self.assertTrue(correction["all_source_global_bytes_equal"])

    def test_four_tier_deck(self):
        index = load(X2 / "deck" / "deck-index.json")
        self.assertEqual(index["card_count"], 208)
        self.assertEqual(index["tier_counts"], {"1": 1, "2": 3, "3": 4, "4": 200})
        cards = [load(path) for path in (X2 / "deck" / "cards").glob("*.json")]
        known = {card["card_id"] for card in cards}
        self.assertEqual(len(known), 208)
        self.assertTrue(all(not card["parent_ids"] or all(parent in known for parent in card["parent_ids"]) for card in cards))

    def test_manifest_and_privacy_security(self):
        manifest = load(VALIDATION / "x2-manifest.json")
        exclusions = set(manifest["declared_self_exclusions"])
        actual = exclusions.copy()
        for entry in manifest["entries"]:
            data = norm(ROOT / entry["path"])
            self.assertEqual(len(data), entry["bytes_normalized_lf"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"], entry["path"])
            actual.add(entry["path"])
        staged = load(VALIDATION / "x2-staged-review.json")
        self.assertEqual(actual, set(staged["expected_paths"]))
        self.assertEqual(load(VALIDATION / "x2-privacy.json")["confirmed_count"], 0)
        self.assertEqual(load(VALIDATION / "x2-security.json")["finding_count"], 0)

    def test_x1_immutable(self):
        self.assertEqual(git("diff", "--name-only", f"{X1}..HEAD", "--", "docs/orin-thale/v687-v7/x1", "scripts/build_ghc_family_orin_thale_v687_v7_x1.py", "tests/test_ghc_family_orin_thale_v687_v7_x1.py"), "")

    def test_terminal_boundaries(self):
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(self.truth["route_state"], "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED")
        self.assertEqual(self.truth["canonical_state"], "NOT_INVOKED")


if __name__ == "__main__":
    unittest.main()
