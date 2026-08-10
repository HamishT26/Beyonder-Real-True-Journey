"""Lifecycle checks for Neris Solane's v662-v3-2 remaster evidence seal."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = Path("docs/neris-solane/v662-v3-2-remaster")
PHASE = ROOT / PHASE_ROOT
X1 = "9b61b218956031d80da66a59924713778b63f31f"
EVIDENCE_ORIGINAL = "999de05624682c19226c1bd5f57f2682468ff072"
BRANCH = "codex/GHC-Family/neris-solane-v662-v3-2-remaster"
OUTCOMES = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}


def read_json(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8")
    if completed.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {completed.stderr[-1000:]}")
    return completed.stdout.strip()


def git_bytes(revision: str, path: str) -> bytes:
    completed = subprocess.run(["git", "show", f"{revision}:{path}"], cwd=ROOT, check=False, capture_output=True)
    if completed.returncode:
        raise AssertionError(f"missing Git blob {revision}:{path}")
    return completed.stdout


class TestV662V3RemasterX2(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gate = read_json("evidence/x1-to-x2-gate.json")
        cls.outcomes = read_json("evidence/proposal-outcomes.json")
        cls.mutations = read_json("truth/retained-mutation-register-x2.json")
        cls.tools = read_json("tooling/skill-runner-aggregate.json")
        cls.approval = read_json("evidence/approval-packet-receipts.json")
        cls.cfr = read_json("evidence/clean-fix-refine-receipts.json")
        cls.flow = read_json("method-flow/method-flow-state-x2.json")
        cls.operational = read_json("truth/x2-operational-failures.json")
        cls.truth = read_json("truth/x2-phase-truth.json")
        cls.exact = read_json("truth/exact-and-blocked-register-x2.json")
        cls.governance = read_json("governance/live-roster-and-authorization-x2.json")
        cls.manifest = read_json("validation/x2-content-manifest.json")
        cls.privacy = read_json("validation/x2-privacy-scan.json")
        cls.document = read_json("validation/x2-document-cap.json")
        cls.staged = read_json("validation/x2-staged-review.json")
        cls.validation = read_json("validation/x2-validation.json")

    def test_01_evidence_is_direct_single_parent_child_of_x1(self) -> None:
        self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE_ORIGINAL)
        self.assertEqual(git("rev-parse", "HEAD^^"), X1)
        parents = git("rev-list", "--parents", "-n", "1", "HEAD").split()
        self.assertEqual(len(parents), 2)
        self.assertEqual(parents[1], EVIDENCE_ORIGINAL)
        self.assertEqual(git("rev-list", "--count", f"{X1}..HEAD"), "2")
        self.assertEqual(git("rev-list", "--merges", f"{X1}..HEAD"), "")
        self.assertEqual(git("branch", "--show-current"), BRANCH)

    def test_02_x1_gate_and_manifest_are_immutable(self) -> None:
        self.assertEqual(self.gate["x1_freeze"], X1)
        self.assertTrue(self.gate["four_way_equal"])
        self.assertEqual(self.gate["divergence"], {"ahead": 0, "behind": 0})
        self.assertEqual(self.gate["x1_drift"], [])
        self.assertTrue(self.gate["strict_x1_before_x2"])
        x1_manifest = read_json("validation/x1-content-manifest.json")
        for entry in x1_manifest["entries"]:
            self.assertEqual(git_bytes("HEAD", entry["path"]), git_bytes(X1, entry["path"]), entry["path"])

    def test_03_program_preserves_selected_zero_credit_and_new_outcomes(self) -> None:
        self.assertEqual(self.outcomes["program_count"], 40)
        self.assertEqual(self.outcomes["selected_inherited_revalidated"], 20)
        self.assertEqual(self.outcomes["selected_inherited_novelty_credit"], 0)
        self.assertEqual(self.outcomes["selected_inherited_completion_credit"], 0)
        self.assertEqual(self.outcomes["new_unique_executed"], 20)
        self.assertEqual(self.outcomes["observed_outcome_counts"], OUTCOMES)
        self.assertEqual({row["observed_outcome"] for row in self.outcomes["outcomes"]}, set(OUTCOMES))

    def test_04_all_forty_surfaces_have_three_frozen_artifacts(self) -> None:
        new_contracts = list((PHASE / "surfaces").glob("*/contract.json"))
        selected_contracts = list((PHASE / "evidence/selected-revalidation").glob("*/contract.json"))
        self.assertEqual(len(new_contracts), 20)
        self.assertEqual(len(selected_contracts), 20)
        for contract in [*new_contracts, *selected_contracts]:
            self.assertTrue((contract.parent / "mutation-results.json").is_file())
            self.assertTrue((contract.parent / "bounded-receipt.json").is_file())

    def test_05_two_hundred_mutations_are_rejected_and_retained(self) -> None:
        self.assertEqual(self.mutations["count"], 200)
        self.assertEqual(self.mutations["rejected"], 200)
        self.assertEqual(self.mutations["accepted"], 0)
        self.assertEqual(self.mutations["completion_credit"], 0)
        self.assertEqual(len(self.mutations["mutations"]), 200)
        self.assertTrue(all(row["rejected"] and not row["accepted"] for row in self.mutations["mutations"]))
        self.assertEqual(len({row["mutation_id"] for row in self.mutations["mutations"]}), 200)

    def test_06_method_flow_counts_and_witnesses_are_exact(self) -> None:
        self.assertEqual(self.flow["method_count"], 51)
        self.assertEqual(self.flow["failed_witness_count"], 211)
        self.assertEqual(self.flow["passing_witness_count"], 51)
        self.assertEqual(self.flow["effective_negatives"], 23042)
        self.assertEqual(self.flow["effective_methods"], 7636)
        self.assertTrue(self.flow["all_failures_retained"])
        self.assertEqual(len({row["witness_id"] for row in self.flow["witnesses"]}), 262)
        self.assertEqual(self.operational["failure_count"], 6)
        self.assertTrue(self.operational["all_zero_credit"])

    def test_07_ten_skills_and_ten_runners_were_validated_and_used(self) -> None:
        self.assertEqual(self.tools["skills_built_validated_smoke_used"], 10)
        self.assertEqual(self.tools["runners_built_invoked"], 10)
        self.assertEqual(self.tools["global_skill_promotions"], 10)
        self.assertTrue(self.tools["all_valid"])
        self.assertFalse(self.tools["plugin_caches_mutated"])
        skill_files = list((PHASE / "skills").glob("*/SKILL.md"))
        agents_files = list((PHASE / "skills").glob("*/agents/openai.yaml"))
        self.assertEqual(len(skill_files), 10)
        self.assertEqual(len(agents_files), 10)
        self.assertTrue(all(path.parent.name.startswith("ghc-family-") for path in skill_files))
        runner_receipts = list((PHASE / "tooling/runner-receipts").glob("*.json"))
        self.assertEqual(len(runner_receipts), 10)
        for path in runner_receipts:
            row = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(row["valid"] and row["smoke_used"])
            self.assertTrue(row["runner"].startswith("ghc_family_"))

    def test_08_successor_tooling_rows_remain_recommendations(self) -> None:
        self.assertEqual(len(self.tools["successor_skill_ideas"]), 10)
        self.assertEqual(len(self.tools["successor_runner_ideas"]), 10)
        self.assertTrue(all(row["state"] == "recommendation_only" for row in self.tools["successor_skill_ideas"]))
        self.assertTrue(all(row["state"] == "recommendation_only" for row in self.tools["successor_runner_ideas"]))

    def test_09_approval_packet_quantities_and_execution_are_exact(self) -> None:
        self.assertEqual(
            self.approval["counts"],
            {"owner_safe_now": 30, "successor_safe_now": 20, "owner_candidates": 15, "successor_candidates": 15, "owner_exact": 10, "owner_blocked": 5, "safe_total": 50, "candidate_total": 30},
        )
        self.assertEqual(self.approval["executed"], {"owner_safe_now": 30, "owner_candidates": 15, "owner_exact": 0, "owner_blocked": 0, "successor": 0})
        self.assertTrue(all(row["state"] == "completed" for row in self.approval["owner_safe_now"]))
        self.assertTrue(all(row["state"] == "executed_bounded_structural" for row in self.approval["owner_candidates"]))

    def test_10_exact_and_blocked_packets_remain_unexecuted(self) -> None:
        self.assertEqual(self.exact["exact_count"], 10)
        self.assertEqual(self.exact["blocked_count"], 5)
        self.assertEqual(self.exact["executed_count"], 0)
        self.assertTrue(all(row["state"] == "exact_gate" and not row["executed"] for row in self.exact["exact_rows"]))
        self.assertTrue(all(row["state"] == "open_gap" and not row["executed"] for row in self.exact["blocked_rows"]))

    def test_11_clean_fix_refine_is_thirty_completed_plus_thirty_recommended(self) -> None:
        self.assertEqual(self.cfr["counts"], {"owner_completed": 30, "successor_recommendations": 30})
        self.assertEqual(len(self.cfr["owner"]), 30)
        self.assertEqual(len(self.cfr["successor"]), 30)
        self.assertTrue(all(row["state"] == "completed" and row["deletions"] == 0 for row in self.cfr["owner"]))
        self.assertFalse(self.cfr["destructive_cleanup_performed"])
        self.assertEqual(self.cfr["plugin_cache_mutations"], 0)

    def test_12_terminal_truth_preserves_all_counts_and_boundaries(self) -> None:
        self.assertEqual(self.truth["frozen_proposals"], 3530)
        self.assertEqual(self.truth["new_outcomes"], OUTCOMES)
        self.assertEqual(self.truth["effective_negatives"], 23042)
        self.assertEqual(self.truth["effective_methods"], 7636)
        self.assertEqual(self.truth["effective_open_gaps"], 149)
        self.assertEqual(self.truth["effective_exact_gates"], 148)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(self.truth["independent_reproduction"])

    def test_13_roster_and_authorization_snapshot_is_sanitized(self) -> None:
        self.assertEqual(self.governance["current_owner"], "Neris Solane")
        self.assertEqual(self.governance["current_variant"], "v662-v3-2-remaster")
        self.assertEqual(self.governance["canonical_phase"], "v662-v3")
        self.assertEqual(self.governance["active_main_task_count"], 15)
        self.assertEqual(self.governance["standby_collaboration_subagent_count"], 1)
        self.assertFalse(self.governance["raw_task_or_thread_ids_recorded"])
        self.assertFalse(self.governance["private_routes_recorded"])

    def test_14_manifest_replays_exact_committed_git_blobs(self) -> None:
        self.assertEqual(self.manifest["entry_count"], len(self.manifest["entries"]))
        for entry in self.manifest["entries"]:
            payload = git_bytes("HEAD", entry["path"])
            self.assertEqual(len(payload), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(payload).hexdigest(), entry["sha256"], entry["path"])

    def test_15_privacy_document_json_and_staged_reviews_pass(self) -> None:
        self.assertEqual(len(self.privacy["classes"]), 5)
        self.assertEqual(self.privacy["confirmed_hit_count"], 0)
        self.assertFalse(self.privacy["privacy_complete"])
        self.assertTrue(self.document["valid"])
        self.assertEqual(self.document["over_cap"], [])
        self.assertEqual(self.staged["state"], "EXACT_STAGED_REVIEW")
        self.assertTrue(self.staged["valid"])
        self.assertEqual(self.staged["missing"], [])
        self.assertEqual(self.staged["unexpected"], [])
        self.assertTrue(self.validation["valid"])
        self.assertEqual(self.validation["passed"], self.validation["total"])
        self.assertEqual(self.validation["json_errors"], [])

    def test_16_overview_is_substantive_and_route_is_unsent(self) -> None:
        overview = (PHASE / "overview/v662-v3-2-remaster-x2-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1500)
        self.assertIn("relational working language only", overview.lower())
        self.assertIn("māori authority", overview.lower())
        self.assertEqual(self.truth["route"], {"owner": "Vesper Arlen", "phase": "v662-v4", "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"})
        self.assertFalse(self.truth["message_attempted"])
        self.assertFalse(self.truth["message_sent"])


if __name__ == "__main__":
    unittest.main()
