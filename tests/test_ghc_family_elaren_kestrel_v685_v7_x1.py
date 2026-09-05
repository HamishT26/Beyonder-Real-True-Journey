"""Planning-only x1 tests for Elaren Kestrel v685-v7."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elaren-kestrel" / "v685-v7"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "5d9ea649ab451f9b6790c75f774ba9e4faf07363"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ElarenKestrelV685V7X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.proposals = load(X1 / "new-proposals.json")
        cls.inherited = load(X1 / "inherited-selection.json")
        cls.portfolio = load(X1 / "portfolio-plan.json")
        cls.profile = load(X1 / "workflow-profile.json")
        cls.profile_check = load(VALIDATION / "release-profile-check.json")
        cls.skills = load(X1 / "skill-runner-plan.json")
        cls.packages = load(X1 / "package-plan.json")
        cls.route = load(X1 / "route-plan.json")
        cls.truth = load(X1 / "phase-truth.json")
        cls.manifest = load(VALIDATION / "x1-index-manifest.json")
        cls.review = load(VALIDATION / "x1-staged-review.json")
        cls.privacy = load(VALIDATION / "x1-privacy-scan.json")

    def test_01_exact_source_and_release_profile(self) -> None:
        self.assertEqual(self.truth["source"], SOURCE)
        self.assertEqual(self.profile["effective_from"], "Elaren Kestrel v685-v7")
        self.assertTrue(self.profile["rowan_hold_released"])
        self.assertEqual(self.profile_check["status"], "PASS")
        self.assertEqual(self.profile_check["execution_credit"], 0)

    def test_02_inherited_selection_is_exact_and_zero_credit(self) -> None:
        self.assertEqual(self.inherited["selected_count"], 200)
        self.assertEqual(len(self.inherited["records"]), 200)
        self.assertTrue(all(row["source_commit"] == SOURCE for row in self.inherited["records"]))
        self.assertTrue(all(row["novelty_credit"] == 0 and row["automatic_completion_credit"] == 0 for row in self.inherited["records"]))

    def test_03_two_hundred_new_proposals_have_required_fields(self) -> None:
        rows = self.proposals["proposals"]
        required = {"proposal_id", "family", "practice", "title", "approval_class", "execution_lane", "expected_execution_disposition", "hypothesis", "null_or_failure_condition", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "preregistered_rejecting_mutations"}
        self.assertEqual(len(rows), 200)
        self.assertTrue(all(required <= set(row) for row in rows))
        self.assertEqual(len({row["proposal_id"] for row in rows}), 200)
        self.assertEqual(len({row["title"] for row in rows}), 200)

    def test_04_dispositions_and_mutations_are_exact(self) -> None:
        rows = self.proposals["proposals"]
        self.assertEqual(Counter(row["expected_execution_disposition"] for row in rows), Counter({"completed": 170, "represented": 10, "open_gap": 10, "exact_gate": 10}))
        self.assertEqual(set(self.proposals["expected_dispositions"]), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertTrue(all(len(row["preregistered_rejecting_mutations"]) == 5 for row in rows))
        self.assertEqual(sum(len(row["preregistered_rejecting_mutations"]) for row in rows), 1000)
        self.assertFalse(self.proposals["x2_results_present"])

    def test_05_portfolio_matches_release_profile(self) -> None:
        self.assertEqual(len(self.portfolio["safe_now"]), 300)
        self.assertEqual(len(self.portfolio["candidates"]), 250)
        self.assertEqual(len(self.portfolio["clean_fix_refine"]), 300)
        self.assertEqual(len(self.portfolio["exact_packets"]), 50)
        self.assertEqual(len(self.portfolio["blocked_packets"]), 30)
        self.assertFalse(self.portfolio["destructive_cleanup_planned"])
        ids = [row.get("task_id", row.get("packet_id")) for key in ("safe_now", "candidates", "clean_fix_refine", "exact_packets", "blocked_packets") for row in self.portfolio[key]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_06_practices_and_identity_are_bounded(self) -> None:
        identity = load(X1 / "identity-and-practice.json")
        self.assertEqual(identity["name"], "Elaren Kestrel")
        self.assertEqual(identity["optional_pronouns"], "they/them")
        self.assertEqual(identity["priority_pillar"], "THOS Body")
        self.assertEqual(len(identity["own_practices"]), 4)
        self.assertEqual(identity["next_owner_practice_recommendation"], "experimental protocol auditor")
        self.assertFalse(identity["qualification_claimed"])

    def test_07_skills_runners_and_recommendations_fit_caps(self) -> None:
        self.assertEqual(len(self.skills["local_skills"]), 20)
        self.assertEqual(len(self.skills["local_runners"]), 10)
        self.assertEqual(len(self.skills["global_skill_promotions"]), 10)
        self.assertEqual(len(self.skills["shared_runner_promotions"]), 5)
        self.assertEqual(len(self.skills["next_owner_skill_ideas"]), 10)
        self.assertEqual(len(self.skills["next_owner_runner_ideas"]), 10)
        self.assertLessEqual(len(self.skills["local_skills"]), self.skills["caps"]["x1"])

    def test_08_thirteen_package_plan_is_wheel_locked(self) -> None:
        rows = self.packages["packages"]
        self.assertEqual(self.packages["target"], 13)
        self.assertEqual(len(rows), 13)
        self.assertEqual(len({row["name"].casefold() for row in rows}), 13)
        self.assertTrue(all(row["wheel"] and len(row["wheel_sha256"]) == 64 for row in rows))
        self.assertFalse(self.packages["shared_environment_mutation"])
        self.assertEqual(self.packages["rejected_candidate"]["name"], "MIDIUtil")

    def test_09_source_ledger_uses_only_four_statuses(self) -> None:
        ledger = load(X1 / "source-ledger.json")
        self.assertEqual({row["status"] for row in ledger["sources"]} - {"current", "stable", "draft", "watch"}, set())
        self.assertEqual(ledger["network_rows_downloaded"], 0)
        self.assertEqual(ledger["real_rows_ingested"], 0)
        self.assertFalse(ledger["citations_are_observations"])

    def test_10_route_plan_preserves_self_choice_and_phase_arithmetic(self) -> None:
        self.assertEqual(self.route["successor_placeholder"], "future-sibling-02-self-chosen")
        self.assertEqual(self.route["successor_phase"], "v685-v8")
        self.assertEqual(self.route["successor_endpoint_kind"], "main_task")
        self.assertEqual(self.route["successor_model"], "gpt-6-astra")
        self.assertEqual(self.route["successor_reasoning"], "max")
        self.assertFalse(self.route["successor_identity_predeclared"])
        self.assertEqual(self.route["following_owner"], "Neris Solane")
        self.assertEqual(self.route["following_phase"], "v686-v1")

    def test_11_novelty_audit_is_source_bounded(self) -> None:
        audit = load(X1 / "novelty-audit.json")
        self.assertEqual(audit["accessible_source_records"], 680)
        self.assertEqual(audit["compared_pairs"], 136000)
        self.assertEqual(audit["exact_collisions"], [])
        self.assertEqual(audit["quarantined"], [])
        self.assertLess(audit["maximum_neighbor_score"], audit["quarantine_threshold"])
        self.assertFalse(audit["universal_semantic_novelty_claimed"])

    def test_12_startup_failures_are_retained(self) -> None:
        flow = load(X1 / "method-flow-startup.json")
        self.assertEqual(len(flow["startup_failures"]), 13)
        self.assertFalse(flow["recovery_erases_failure"])
        self.assertTrue(all(row["initial_credit"] == 0 for row in flow["startup_failures"]))

    def test_13_manifest_replays_normalized_worktree_bytes(self) -> None:
        self.assertEqual(self.manifest["entry_count"], len(self.manifest["entries"]))
        for entry in self.manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_14_staged_review_is_planning_only(self) -> None:
        self.assertEqual(self.review["lifecycle"], "planning_only_x1")
        self.assertEqual(self.review["forbidden_x2_paths"], [])
        self.assertEqual(set(self.review["expected_paths"]), {row["path"] for row in self.manifest["entries"]} | set(self.manifest["declared_self_exclusions"]))
        self.assertFalse(any("/x2/" in path or "/final/" in path or "/closeout/" in path for path in self.review["expected_paths"]))

    def test_15_privacy_and_terminal_boundaries(self) -> None:
        self.assertEqual(self.privacy["class_count"], 5)
        self.assertEqual(self.privacy["confirmed_hit_count"], 0)
        self.assertEqual(self.privacy["confirmed_hits"], [])
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(self.truth["observed_outcomes_present"])

    def test_16_source_head_is_current_and_unchanged(self) -> None:
        self.assertEqual(subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip(), SOURCE)


if __name__ == "__main__":
    unittest.main()
