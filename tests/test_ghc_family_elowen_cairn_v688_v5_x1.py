#!/usr/bin/env python3
"""Planning-only x1 tests for Elowen Cairn v688-v5."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elowen-cairn" / "v688-v5"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "adadd367036e49cfb5c480f2aa0b598c164cac1c"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> bytes:
    proc = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        raise AssertionError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout


class ElowenV688V5X1Tests(unittest.TestCase):
    def test_source_and_lifecycle(self):
        source = load(X1 / "source-verification.json")
        self.assertEqual(source["source"], SOURCE)
        self.assertEqual(source["phase_commits"], 4)
        self.assertEqual(source["merges"], 0)
        self.assertEqual(source["manifest_bindings"], 893)
        self.assertEqual(source["manifest_replay_failures"], 0)
        self.assertFalse(source["source_canonical_replayed"])

    def test_proposal_counts_and_fields(self):
        new = load(X1 / "new-proposal-freeze.json")
        inherited = load(X1 / "inherited-proposal-freeze.json")
        self.assertEqual(new["count"], 200)
        self.assertEqual(inherited["count"], 200)
        self.assertEqual(new["chain_before"], 16230)
        self.assertEqual(new["chain_after"], 16430)
        required = {"proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "source_refs", "current_official_or_primary_source_needs", "concrete_artifact", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_execution_disposition", "source_status", "operation", "input"}
        for row in new["proposals"]:
            self.assertTrue(required <= set(row))
            self.assertIn(row["expected_execution_disposition"], {"completed", "represented", "open_gap", "exact_gate"})

    def test_expected_dispositions(self):
        rows = load(X1 / "new-proposal-freeze.json")["proposals"]
        self.assertEqual(Counter(row["expected_execution_disposition"] for row in rows), Counter({"completed": 165, "represented": 26, "open_gap": 3, "exact_gate": 6}))

    def test_source_bounded_novelty(self):
        audit = load(X1 / "proposal-chain-audit.json")
        self.assertEqual(audit["source_json_parse_failure_count"], 0)
        self.assertEqual(audit["exact_title_collision_count"], 0)
        self.assertEqual(audit["input_hash_collision_count"], 0)
        self.assertEqual(audit["quarantined_count"], 0)
        self.assertLess(audit["maximum_neighbor_score"], audit["quarantine_threshold"])
        self.assertFalse(audit["universal_novelty_claimed"])

    def test_portfolio_release_profile(self):
        p = load(X1 / "approval-portfolio.json")
        self.assertEqual(len(p["safe_now"]), 300)
        self.assertEqual(len(p["candidates"]), 250)
        self.assertEqual(len(p["clean_fix_refine"]), 300)
        self.assertEqual(len(p["exact_packets"]), 50)
        self.assertEqual(len(p["blocked_packets"]), 30)
        self.assertFalse(p["destructive_cleanup_planned"])
        self.assertEqual(load(X1 / "release-profile-validation.json")["status"], "PASS")

    def test_skills_runners_packages_and_practices(self):
        tools = load(X1 / "tool-package-plan.json")
        practices = load(X1 / "pillar-practice-freeze.json")
        self.assertEqual(len(tools["skills"]), 10)
        self.assertEqual(len(tools["runners"]), 5)
        self.assertEqual(len(tools["packages"]), 3)
        self.assertEqual(len(tools["next_owner_skill_ideas"]), 10)
        self.assertEqual(len(tools["next_owner_runner_ideas"]), 10)
        self.assertEqual(len(practices["own_practices"]), 4)
        self.assertEqual(practices["primary_pillar"], "THOS Body")

    def test_method_flow_non_erasure(self):
        flow = load(X1 / "method-flow-startup.json")
        self.assertEqual(flow["counts"]["methods"], 14)
        self.assertEqual(flow["counts"]["witness_results"], {"fail": 14, "pass": 14})
        self.assertEqual(len(flow["methods"]), 14)
        self.assertTrue(all(row["retained_negative_ids"] for row in flow["methods"]))

    def test_route_is_unresolved_and_identity_unassigned(self):
        route = load(X1 / "route-freeze.json")
        self.assertEqual(route["next"]["owner"], "future-sibling-13-self-chosen")
        self.assertEqual(route["next"]["phase"], "v688-v6")
        self.assertFalse(route["future_identity_preassigned"])
        self.assertEqual(route["successor_contacts"], 0)
        self.assertEqual(route["following"]["owner"], "Sylven Arc")

    def test_x1_phase_truth_is_planning_only(self):
        truth = load(X1 / "phase-truth.json")
        self.assertEqual(truth["state"], "PLANNING_ONLY_X1_PRECOMMIT")
        self.assertFalse(truth["x2_implementation_present"])
        self.assertFalse(truth["x2_outcome_present"])
        self.assertIsNone(truth["observed_outcomes"])
        self.assertEqual(truth["canonical_invocations"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_manifest_replays_staged_blobs(self):
        manifest = load(VALIDATION / "x1-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            data = git("show", f":{row['path']}").replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(len(data), row["bytes_normalized_lf"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256_normalized_lf"])

    def test_staged_review_and_privacy(self):
        review = load(VALIDATION / "x1-staged-review.json")
        privacy = load(VALIDATION / "x1-privacy.json")
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["deletions"], [])
        self.assertEqual(review["outside_owner_paths"], [])
        self.assertEqual(review["x2_paths"], [])
        self.assertFalse(review["x2_implementation_or_outcome"])
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)

    def test_overview_and_caps(self):
        overview = (X1 / "integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1500)
        self.assertLessEqual(len(overview.split()), 100000)
        for term in ("GMUT Mind", "THOS Body", "Freed ID", "CBR", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(term, overview)


if __name__ == "__main__":
    unittest.main()
