from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v648_v5_definitions as d  # noqa: E402


PHASE = ROOT / "docs" / "sable-rook" / d.PHASE_SLUG


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


class TestGhcFamilyV648V5X1(unittest.TestCase):
    def test_identity_source_and_phase_boundary(self) -> None:
        identity = load("identity-receipt.json")
        startup = load("environment/startup-receipt.json")
        truth = load("phase-truth.json")
        self.assertEqual(identity["owner"], "Sable Rook")
        self.assertEqual(identity["pronouns"], "they/them")
        self.assertIn("Relational working language only", identity["identity_boundary"])
        self.assertEqual(startup["source_head"], d.SOURCE_COMMIT)
        self.assertTrue(startup["source_ancestry"])
        self.assertEqual(startup["source_phase_commits"], 3)
        self.assertEqual(startup["source_merges"], 0)
        self.assertTrue(startup["owner_fast_forwarded_only"])
        self.assertEqual(truth["stage"], "x1_frozen_not_executed")
        self.assertFalse(truth["x2_started"])
        self.assertIsNone(truth["observed_distribution"])
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_exact_ten_proposals_and_required_fields(self) -> None:
        packet = load("x1-proposals.json")
        proposals = packet["proposals"]
        required = {
            "proposal_id",
            "title",
            "pillar",
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "source_needs",
            "artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        self.assertEqual(len(proposals), 10)
        self.assertEqual(len({row["proposal_id"] for row in proposals}), 10)
        self.assertEqual(packet["prior_frozen_proposal_count"], 600)
        self.assertEqual(packet["frozen_total_after_x1"], 610)
        self.assertEqual(packet["outcome_classes"], d.OUTCOME_CLASSES)
        for proposal in proposals:
            self.assertTrue(required.issubset(proposal))
            self.assertTrue(proposal["source_needs"])
            self.assertTrue(proposal["artifacts"])
            self.assertTrue(proposal["protected_gates"])
            self.assertIn(proposal["expected_disposition"], d.OUTCOME_CLASSES)
        expected = {label: 0 for label in d.OUTCOME_CLASSES}
        for proposal in proposals:
            expected[proposal["expected_disposition"]] += 1
        self.assertEqual(
            expected,
            {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        )

    def test_frozen_corpus_and_novelty_audit(self) -> None:
        index = load("provenance/frozen-chain-proposal-index.json")
        audit = load("provenance/proposal-collision-audit.json")
        self.assertEqual(index["prior_count"], 600)
        self.assertEqual(index["new_count"], 10)
        self.assertEqual(index["count"], 610)
        self.assertEqual(len(index["prior_proposals"]), 600)
        self.assertEqual(len(index["new_proposals"]), 10)
        self.assertEqual(len(audit["rows"]), 10)
        self.assertLess(audit["maximum_observed_jaccard"], audit["threshold"])
        self.assertTrue(
            all(row["jaccard"] < row["threshold"] for row in audit["rows"])
        )

    def test_source_ledger_uses_four_status_classes(self) -> None:
        ledger = load("sources/source-ledger.json")
        self.assertEqual(
            ledger["allowed_statuses"], ["current", "stable", "draft", "watch"]
        )
        self.assertEqual(set(ledger["status_counts"]), set(ledger["allowed_statuses"]))
        self.assertTrue(all(value >= 1 for value in ledger["status_counts"].values()))
        for source in ledger["sources"]:
            self.assertIn(source["status"], ledger["allowed_statuses"])
            self.assertEqual(source["evidence_credit"], "design_or_protocol_support_only")
            self.assertTrue(source["not_observation"])

    def test_expanded_portfolios_are_new_and_frozen(self) -> None:
        safe = load("approval-packets/x1-safe-now-portfolio.json")
        candidates = load("prototypes/x1-candidate-plan.json")
        pack = load("prototypes/x1-skill-runner-plan.json")
        cleanup = load("maintenance/x1-clean-refine-plan.json")
        self.assertEqual(safe["count"], 30)
        self.assertEqual(candidates["count"], 20)
        self.assertEqual(pack["skill_count"], 20)
        self.assertEqual(pack["runner_count"], 10)
        self.assertEqual(cleanup["count"], 30)
        self.assertEqual(safe["inherited_completion_credit"], 0)
        self.assertEqual(candidates["inherited_completion_credit"], 0)
        for row in safe["items"] + candidates["items"] + cleanup["items"]:
            self.assertEqual(row["origin"], "sable_v648_v5_new")
            self.assertEqual(row["x1_state"], "frozen_not_executed")
            self.assertFalse(row["x2_completion_credit"])
        for row in pack["skills"] + pack["runners"]:
            self.assertEqual(row["origin"], "sable_v648_v5_new")
            self.assertFalse(row["x2_use_credit"])

    def test_negatives_and_gates_remain_honest(self) -> None:
        negatives = load("retained-negative-register.json")
        operational = load("validation/x1-operational-negatives.json")
        synthetic = load("validation/x1-synthetic-mutation-plan.json")
        gates = load("exact-open-gate-register.json")
        self.assertEqual(operational["count"], 6)
        self.assertEqual(negatives["inherited_effective"], 4299)
        self.assertEqual(negatives["effective_at_x1"], 4305)
        self.assertEqual(
            negatives["projected_if_all_synthetic_execute_and_reject"], 4375
        )
        self.assertFalse(negatives["negative_erased"])
        self.assertEqual(synthetic["count"], 70)
        self.assertEqual(synthetic["executed_count"], 0)
        self.assertEqual(synthetic["rejected_count"], 0)
        self.assertTrue(all(not row["executed"] for row in synthetic["mutations"]))
        self.assertEqual(gates["inherited_open_gaps"], 30)
        self.assertEqual(gates["inherited_exact_gates"], 31)
        self.assertEqual(gates["closed_in_x1"], 0)

    def test_method_flow_preserves_failures_and_passing_witnesses(self) -> None:
        ledger = load("method-flow/method-flow-ledger.json")
        validation = load("method-flow/method-flow-validation.json")
        self.assertEqual(len(ledger["methods"]), 6)
        self.assertEqual(len(ledger["witnesses"]), 12)
        self.assertEqual(
            sum(row["result"] == "fail" for row in ledger["witnesses"]), 6
        )
        self.assertEqual(
            sum(row["result"] == "pass" for row in ledger["witnesses"]), 6
        )
        self.assertTrue(
            all(row["recommendation_state"] == "preferred" for row in ledger["methods"])
        )
        self.assertTrue(validation["valid"])

    def test_no_x2_implementation_or_observed_core_outcome(self) -> None:
        review = load("validation/x1-review.json")
        staged = load("validation/x1-staged-review.json")
        self.assertEqual(review["x2_implementation_count"], 0)
        self.assertEqual(review["x2_observed_outcome_count"], 0)
        self.assertEqual(staged["x2_implementation_paths"], [])
        self.assertEqual(staged["x2_outcome_paths"], [])
        self.assertTrue(staged["x1_only"])
        forbidden_keys = {"observed_disposition", "actual_outcome", "completed_at"}
        for path in PHASE.rglob("*.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))
            stack = [payload]
            while stack:
                value = stack.pop()
                if isinstance(value, dict):
                    self.assertTrue(forbidden_keys.isdisjoint(value))
                    stack.extend(value.values())
                elif isinstance(value, list):
                    stack.extend(value)

    def test_x1_manifest_matches_filtered_git_blob_domain(self) -> None:
        manifest = load("validation/x1-staged-manifest.json")
        review = load("validation/x1-staged-review.json")
        entries = manifest["entries"]
        self.assertEqual(manifest["entry_count"], len(entries))
        self.assertEqual(len(manifest["self_exclusions"]), 3)
        for entry in entries:
            observed = git(
                "hash-object", f"--path={entry['path']}", entry["path"]
            )
            self.assertEqual(observed, entry["git_blob"], entry["path"])
        current = set(filter(None, git("diff", "--name-only").splitlines()))
        current.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
        current.update(
            filter(None, git("ls-files", "--others", "--exclude-standard").splitlines())
        )
        covered = {row["path"] for row in entries} | set(manifest["self_exclusions"])
        self.assertEqual({path.replace("\\", "/") for path in current}, covered)
        self.assertEqual(review["intended_path_count"], len(covered))

    def test_privacy_document_caps_and_route_hold(self) -> None:
        privacy = load("validation/x1-staged-privacy.json")
        orchestration = load("orchestration/phase-state.json")
        plan = load("validation/single-pass-validation-plan.json")
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertEqual(len(privacy["pattern_classes"]), 5)
        self.assertEqual(orchestration["subagents"], 0)
        self.assertEqual(orchestration["tasks_created"], 0)
        self.assertEqual(orchestration["cross_platform_messages"], 0)
        self.assertEqual(orchestration["terminal_route"], "PREPARED_NOT_SENT")
        self.assertEqual(plan["canonical_successful_pass_budget"], 1)
        self.assertFalse(plan["full_repository_suite"])
        self.assertFalse(plan["detached_replay"])
        self.assertFalse(plan["named_replay"])
        for path in list(PHASE.rglob("*.md")) + list(PHASE.rglob("*.html")):
            words = len(path.read_text(encoding="utf-8").split())
            self.assertLessEqual(words, 6000, path.as_posix())


if __name__ == "__main__":
    unittest.main()
