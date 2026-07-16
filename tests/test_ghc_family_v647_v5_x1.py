from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_v647_v5_definitions as d  # noqa: E402

PHASE = ROOT / "docs/eiren-kestrel/v647-v5"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def frozen_x1_commit() -> str | None:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", "docs/eiren-kestrel/v647-v5/x1-proposals.json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    value = result.stdout.strip()
    return value or None


class V647V5X1Tests(unittest.TestCase):
    def test_exact_ten_and_chain_count(self):
        data = load("x1-proposals.json")
        self.assertEqual((data["prior_frozen_proposal_count"], data["new_frozen_proposal_count"], data["frozen_chain_count_after_x1"]), (510, 10, 520))
        self.assertEqual([row["proposal_id"] for row in data["proposals"]], [f"V6475-P{i:02d}" for i in range(1, 11)])
        self.assertFalse(data["x2_execution_present"])

    def test_required_proposal_fields(self):
        required = {"hypothesis", "null_or_failure", "approval_class", "execution_lane", "current_primary_or_official_source_needs", "concrete_artifacts", "test_falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition", "novelty_against_510_frozen_proposals"}
        for row in load("x1-proposals.json")["proposals"]:
            self.assertFalse([key for key in required if not row.get(key)], row["proposal_id"])

    def test_expected_distribution(self):
        rows = load("x1-proposals.json")["proposals"]
        self.assertEqual({name: sum(row["expected_disposition"] == name for row in rows) for name in d.OUTCOME_CLASSES}, {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})

    def test_portfolio_floors_and_zero_credit(self):
        approval = load("approval-packets/x1-approval-portfolio.json")
        plan = load("prototypes/x1-skill-runner-plan.json")
        cleanup = load("maintenance/x1-clean-refine-plan.json")
        self.assertEqual((approval["safe_now_count"], approval["candidate_count"], plan["skill_count"], plan["runner_count"], cleanup["task_count"]), (30, 20, 20, 10, 30))
        self.assertEqual((approval["exact_approval_count"], approval["blocked_count"]), (10, 5))
        self.assertEqual((approval["completion_credit_before_x2"], plan["completion_credit_before_x2"], cleanup["completion_credit_before_x2"]), (0, 0, 0))

    def test_collision_audits(self):
        proposal = load("provenance/prior-proposal-collision-audit.json")
        portfolio = load("provenance/prior-portfolio-collision-audit.json")
        self.assertTrue(proposal["valid"])
        self.assertEqual((proposal["prior_count"], proposal["exact_collision_count"]), (510, 0))
        self.assertTrue(portfolio["valid"])
        self.assertEqual((portfolio["exact_collision_count"], portfolio["within_current_duplicates"]), (0, []))

    def test_negative_and_method_flow_retention(self):
        negatives = load("validation/x1-operational-negatives.json")
        method = load("method-flow/method-flow-state.json")
        count = len(d.X1_OPERATIONAL_NEGATIVES)
        self.assertEqual((negatives["count"], negatives["observed_effective_after_x1"]), (count, 3493 + count))
        self.assertGreaterEqual(method["counts"]["methods"], count)
        self.assertGreaterEqual(method["counts"]["witness_results"]["fail"], count)
        self.assertGreaterEqual(method["counts"]["witness_results"]["pass"], count)
        x1_ids = {f"V6475-M{i:02d}" for i in range(1, count + 1)}
        x1_methods = [row for row in method["methods"] if row["method_id"] in x1_ids]
        self.assertEqual({row["method_id"] for row in x1_methods}, x1_ids)
        self.assertTrue(all(row["recommendation_state"] == "preferred" for row in x1_methods))

    def test_source_and_authority_boundaries(self):
        source = load("sources/source-ledger.json")
        self.assertEqual((source["real_rows"], source["real_people_or_operations"], source["real_keys_or_tokens"]), (0, 0, 0))
        self.assertFalse(source["authority_delegated"])
        self.assertTrue(all(row["status"] in {"current", "stable", "draft", "watch"} for row in source["sources"]))

    def test_route_prepared_not_sent(self):
        commit = frozen_x1_commit()
        route = (
            json.loads(subprocess.check_output(["git", "show", f"{commit}:docs/eiren-kestrel/v647-v5/orchestration/terminal-route-plan.json"], cwd=ROOT).decode("utf-8"))
            if commit
            else load("orchestration/terminal-route-plan.json")
        )
        self.assertEqual((route["current_state"], route["target_title"], route["send_count"]), ("PREPARED_NOT_SENT", "Ilyra Fen", 0))

    def test_x2_absent(self):
        x1_commit = frozen_x1_commit()
        for relative in ("x2-proposal-ledger.json", "phase-truth.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"):
            repository_relative = f"docs/eiren-kestrel/v647-v5/{relative}"
            if x1_commit:
                result = subprocess.run(["git", "cat-file", "-e", f"{x1_commit}:{repository_relative}"], cwd=ROOT, capture_output=True)
                self.assertNotEqual(result.returncode, 0, relative)
            else:
                self.assertFalse((ROOT / repository_relative).exists(), relative)

    def test_x1_content_seal(self):
        import hashlib
        seal = load("reproduction/x1-content-seal.json")
        self.assertEqual(seal["path_count"], 7)
        x1_commit = frozen_x1_commit()
        for entry in seal["frozen_paths"]:
            repository_relative = f"docs/eiren-kestrel/v647-v5/{entry['path']}"
            raw = (
                subprocess.check_output(["git", "show", f"{x1_commit}:{repository_relative}"], cwd=ROOT)
                if x1_commit
                else (ROOT / repository_relative).read_bytes()
            )
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"])


if __name__ == "__main__":
    unittest.main()
