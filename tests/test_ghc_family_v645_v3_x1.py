#!/usr/bin/env python3
"""Structural tests for Eiren Kestrel v645-v3 x1."""

from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_v645_v3_definitions import (  # noqa: E402
    BLOCKED_PACKETS,
    EIREN_CANDIDATE,
    EIREN_CLEAN,
    EIREN_RUNNERS,
    EIREN_SAFE_NOW,
    EIREN_SKILLS,
    EXACT_PACKETS,
    PROPOSALS,
    SOURCES,
    SUCCESSOR_CANDIDATE,
    SUCCESSOR_CLEAN,
    SUCCESSOR_RUNNERS,
    SUCCESSOR_SAFE_NOW,
    SUCCESSOR_SKILLS,
)

PHASE_DIR = ROOT / "docs/eiren-kestrel/v645-v3"


class V645V3X1Tests(unittest.TestCase):
    def test_research_spine(self) -> None:
        self.assertEqual(len(PROPOSALS), 10)
        self.assertEqual(len({p["proposal_id"] for p in PROPOSALS}), 10)
        self.assertEqual(len({p["title"].casefold() for p in PROPOSALS}), 10)
        self.assertEqual(
            Counter(p["expected_disposition"] for p in PROPOSALS),
            Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}),
        )
        required = {"hypothesis", "null_or_failure", "approval_class", "execution_lane", "authoritative_source_needs", "deliverables", "test_falsifier_or_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        for item in PROPOSALS:
            self.assertTrue(required.issubset(item), item["proposal_id"])

    def test_approval_counts(self) -> None:
        self.assertEqual((len(EIREN_SAFE_NOW), len(SUCCESSOR_SAFE_NOW)), (15, 15))
        self.assertEqual((len(EIREN_CANDIDATE), len(SUCCESSOR_CANDIDATE)), (10, 10))
        self.assertEqual((len(EXACT_PACKETS), len(BLOCKED_PACKETS)), (10, 5))
        all_ids = [p["packet_id"] for group in (EIREN_SAFE_NOW, SUCCESSOR_SAFE_NOW, EIREN_CANDIDATE, SUCCESSOR_CANDIDATE, EXACT_PACKETS, BLOCKED_PACKETS) for p in group]
        self.assertEqual(len(all_ids), len(set(all_ids)))

    def test_skill_runner_clean_counts(self) -> None:
        self.assertEqual((len(EIREN_SKILLS), len(SUCCESSOR_SKILLS)), (10, 10))
        self.assertEqual((len(EIREN_RUNNERS), len(SUCCESSOR_RUNNERS)), (5, 5))
        self.assertEqual((len(EIREN_CLEAN), len(SUCCESSOR_CLEAN)), (15, 15))
        for name, _ in EIREN_SKILLS + SUCCESSOR_SKILLS:
            self.assertRegex(name, r"^[a-z0-9-]{1,63}$")
        for name, _ in EIREN_RUNNERS + SUCCESSOR_RUNNERS:
            self.assertRegex(name, r"^ghc_family_[a-z0-9_]+\.py$")

    def test_sources_are_primary_or_official(self) -> None:
        self.assertGreaterEqual(len(SOURCES), 19)
        for source in SOURCES:
            self.assertIn(source["status"], {"current", "stable", "draft", "watch"})
            self.assertTrue(source["url"].startswith("https://"))
            self.assertRegex(source["authority"].lower(), r"official|primary|final specification")

    def test_generated_artifacts(self) -> None:
        required = [
            "x1-proposals.json",
            "approval-packets/x1-approval-portfolio.json",
            "prototypes/x1-skill-runner-plan.json",
            "maintenance/x1-clean-refine-plan.json",
            "method-flow/method-flow-state.json",
            "sandbox/x1-sandbox-plan.json",
            "validation/x1-structural.json",
        ]
        for rel in required:
            self.assertTrue((PHASE_DIR / rel).is_file(), rel)
        structural = json.loads((PHASE_DIR / "validation/x1-structural.json").read_text(encoding="utf-8"))
        self.assertTrue(structural["valid"])
        self.assertTrue(all(structural["checks"].values()))

    def test_method_flow_preserves_failures_and_passing_witnesses(self) -> None:
        ledger = json.loads((PHASE_DIR / "method-flow/method-flow-state.json").read_text(encoding="utf-8"))
        counts = ledger["counts"]
        self.assertGreaterEqual(counts.get("method_count", counts.get("methods", 0)), 6)
        self.assertGreaterEqual(counts.get("failed_witness_count", counts.get("witness_results", {}).get("fail", 0)), 6)
        self.assertGreaterEqual(counts.get("passing_witness_count", counts.get("witness_results", {}).get("pass", 0)), 6)
        self.assertGreaterEqual(counts.get("preferred_method_count", counts.get("states", {}).get("preferred", 0)), 6)
        passing = {w["witness_id"] for w in ledger["witnesses"] if w["result"] == "pass"}
        for method in ledger["methods"]:
            self.assertTrue(passing.intersection(method["validation_witness_ids"]))


if __name__ == "__main__":
    unittest.main()
