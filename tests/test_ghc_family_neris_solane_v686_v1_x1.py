"""Planning-only gates for Neris Solane v686-v1."""
from __future__ import annotations

import ast
import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/neris-solane/v686-v1"


def read(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


class PlanningGate(unittest.TestCase):
    def test_source_and_separate_truth_layers(self):
        source = read("x1/activation-source.json")
        self.assertEqual(source["source"], "c6b56f912836a46a0dbb07c13aaf6e731e1b32e2")
        self.assertEqual(source["source_canonical_invocation_success_replay"], [1, 1, 0])
        self.assertEqual(source["source_manifest_entries_reverified"], 1267)
        self.assertEqual(source["source_repository_seal"]["effective_negatives"], 65519)
        self.assertEqual(source["activation_baseline"]["effective_negatives"], 65523)

    def test_x1_is_planning_only(self):
        truth = read("x1/phase-truth.json")
        self.assertEqual(truth["state"], "PLANNING_ONLY")
        self.assertIs(truth["x2_execution_started"], False)
        self.assertFalse((BASE / "x2").exists())

    def test_inherited_rows_have_zero_credit(self):
        rows = read("x1/inherited-selection.json")["rows"]
        self.assertEqual(len(rows), 200)
        self.assertTrue(all(row["novelty_credit"] == row["execution_credit"] == 0 for row in rows))

    def test_new_proposals_have_exact_four_label_profile(self):
        rows = read("x1/new-proposals.json")["proposals"]
        self.assertEqual(len(rows), 200)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 200)
        self.assertEqual(len({row["title"] for row in rows}), 200)
        self.assertEqual(
            Counter(row["expected_execution_disposition"] for row in rows),
            {"completed": 170, "represented": 10, "open_gap": 10, "exact_gate": 10},
        )
        self.assertTrue(all(len(row["preregistered_mutations"]) == 5 for row in rows))
        self.assertTrue(all(row["input"] and "expected_result" in row for row in rows))

    def test_portfolio_matches_released_ranges(self):
        portfolio = read("x1/portfolio-plan.json")
        limits = read("x1/workflow-profile.json")["plan_limits"]
        for key, (minimum, maximum) in limits.items():
            self.assertTrue(minimum <= len(portfolio[key]) <= maximum, key)
            self.assertTrue(all(row["execution_credit"] == 0 for row in portfolio[key]))
        self.assertIs(portfolio["destructive_cleanup_planned"], False)
        identifiers = [row["task_id"] for key in limits for row in portfolio[key]]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(Counter(row["category"] for row in portfolio["clean_fix_refine"]), {"CLEAN": 100, "FIX": 100, "REFINE": 100})
        for key in ("exact_packets", "blocked_packets"):
            self.assertTrue(all(not row["operation_executed"] for row in portfolio[key]))
            self.assertEqual(len({row["title"] for row in portfolio[key]}), len(portfolio[key]))

    def test_skill_runner_and_next_owner_plans(self):
        plan = read("x1/skill-runner-plan.json")
        self.assertEqual(len(plan["skills"]), 10)
        self.assertEqual(len(plan["runners"]), 5)
        self.assertEqual(len(plan["global_promotions"]), 10)
        self.assertEqual(len(plan["shared_runner_promotions"]), 5)
        self.assertEqual(len(plan["next_owner_skills"]), 10)
        self.assertEqual(len(plan["next_owner_runners"]), 10)

    def test_three_packages_are_hash_locked_and_deferred(self):
        plan = read("x1/package-plan.json")
        self.assertEqual(plan["direct_additions"], 3)
        self.assertEqual(len(plan["packages"]), 3)
        self.assertTrue(plan["install_after_x1_equality"])
        self.assertTrue(all(row["category"] == "direct" for row in plan["packages"]))
        self.assertTrue(all(len(row["sha256"]) == 64 and row["official_registry_hash_match"] for row in plan["packages"]))
        self.assertTrue(all(row["wheel_traversal_candidates"] == [] for row in plan["packages"]))

    def test_route_creates_or_reuses_only_future_seat_three(self):
        route = read("x1/route-plan.json")
        self.assertEqual((route["next_owner"], route["next_phase"]), ("future-sibling-03-self-chosen", "v686-v2"))
        self.assertEqual((route["following_owner"], route["following_phase"]), ("Vesper Arlen", "v686-v3"))
        self.assertEqual((route["send_count"], route["creation_count_this_task"], route["subagents"]), (0, 0, 0))
        self.assertEqual(route["delivery_state"], "PREPARED_NOT_SENT")

    def test_novelty_is_source_bounded_and_not_quarantined(self):
        audit = read("x1/novelty-audit.json")
        self.assertEqual(audit["comparisons"], 40000)
        self.assertIs(audit["universal_novelty_claimed"], False)
        self.assertFalse(any(row["exact_collision"] or row["quarantine"] for row in audit["rows"]))

    def test_practice_and_authority_boundaries(self):
        identity = read("x1/identity-and-practice.json")
        self.assertEqual(len(identity["practices"]), 4)
        self.assertEqual(identity["priority_pillar"], "Freed ID and CBR Heart")
        self.assertIn("Māori authority", identity["identity_boundary"])
        self.assertGreaterEqual(len(identity["protected_gates"]), 8)

    def test_manifest_replays_normalized_lf_files(self):
        manifest = read("validation/x1-manifest.json")
        allowlist = read("validation/x1-allowlist.json")["paths"]
        entries = manifest["entries"]
        self.assertEqual(len(entries), len(allowlist) - 1)
        self.assertEqual(len({row["path"] for row in entries}), len(entries))
        for row in entries:
            payload = (ROOT / row["path"]).read_bytes().replace(b"\r\n", b"\n")
            self.assertEqual(len(payload), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(payload).hexdigest(), row["sha256"], row["path"])

    def test_builder_syntax(self):
        ast.parse((ROOT / "scripts/build_ghc_family_neris_solane_v686_v1_x1.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
