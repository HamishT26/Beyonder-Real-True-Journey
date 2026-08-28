from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs" / "caelen-ash" / "v674-v3"
X1_ROOT = ROOT / "x1"
X2_ROOT = ROOT / "x2"
VALIDATION = ROOT / "validation"
X1 = "aaff9f4bfe18c2d7dd428cf6cb7b639f3b420b46"
CORE = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class CaelenV674V3X2Tests(unittest.TestCase):
    def test_head_is_exact_immutable_x1_before_evidence_commit(self):
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
        ).strip()
        self.assertEqual(head, X1)

    def test_frozen_x1_is_unchanged(self):
        changed = subprocess.check_output(
            [
                "git",
                "diff",
                "--name-only",
                X1,
                "--",
                "docs/caelen-ash/v674-v3/x1",
            ],
            cwd=REPO,
            text=True,
        ).splitlines()
        self.assertEqual(changed, [])

    def test_phase_truth_has_exact_outcomes_and_verdict(self):
        truth = load(X2_ROOT / "phase-truth.json")
        self.assertEqual(
            truth["outcomes"],
            {
                "completed": 42,
                "represented": 12,
                "open_gap": 3,
                "exact_gate": 3,
            },
        )
        self.assertEqual(set(truth["outcomes"]), CORE)
        self.assertEqual(truth["proposal_chain"], 6730)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_sixty_proposal_evidence_files_match_frozen_ids(self):
        frozen = load(X1_ROOT / "new-proposal-freeze.json")["proposals"]
        files = sorted((X2_ROOT / "proposals").glob("*.json"))
        rows = [load(path) for path in files]
        self.assertEqual(len(rows), 60)
        self.assertEqual(
            {row["proposal_id"] for row in rows},
            {row["proposal_id"] for row in frozen},
        )
        self.assertTrue(
            all(
                row["observed_disposition"]
                == row["expected_execution_disposition"]
                for row in rows
            )
        )

    def test_positive_controls_are_exactly_sixty(self):
        ledger = load(
            X2_ROOT / "fixtures" / "positive-control-ledger.json"
        )
        self.assertEqual(ledger["count"], 60)
        self.assertEqual(ledger["passed"], 60)
        self.assertTrue(all(row["accepted"] for row in ledger["rows"]))

    def test_all_240_mutations_remain_rejected_zero_credit(self):
        ledger = load(
            X2_ROOT / "fixtures" / "invalid-mutation-ledger.json"
        )
        self.assertEqual(ledger["count"], 240)
        self.assertEqual(ledger["rejected"], 240)
        self.assertEqual(ledger["success_credit"], 0)
        self.assertTrue(
            all(
                not row["accepted"]
                and row["result"] == "rejected"
                and row["success_credit"] == 0
                for row in ledger["rows"]
            )
        )

    def test_each_proposal_retains_four_mutations(self):
        rows = [
            load(path)
            for path in (X2_ROOT / "proposals").glob("*.json")
        ]
        self.assertTrue(
            all(len(row["invalid_mutations"]) == 4 for row in rows)
        )

    def test_twenty_skills_were_validated_and_smoke_used_locally(self):
        receipt = load(X2_ROOT / "tools" / "skill-use-receipt.json")
        self.assertEqual(receipt["count"], 20)
        self.assertEqual(receipt["global_installations"], 0)
        self.assertTrue(
            all(
                row["quick_validate_exit"] == 0
                and row["phase_local_only"]
                and not row["global_installation"]
                for row in receipt["validation_rows"]
            )
        )
        self.assertTrue(
            all(
                row["smoke_use_exit"] == 0 and row["smoke_used"]
                for row in receipt["smoke_rows"]
            )
        )
        self.assertEqual(
            len(list((X2_ROOT / "tools" / "skills").glob("*/SKILL.md"))),
            20,
        )

    def test_ten_family_runners_accept_and_reject_as_preregistered(self):
        receipt = load(X2_ROOT / "tools" / "runner-smoke-receipt.json")
        self.assertEqual(receipt["count"], 10)
        self.assertTrue(
            all(
                row["accept_exit"] == 0
                and row["reject_exit"] == 2
                and row["smoke_used"]
                and not row["installed_on_path"]
                for row in receipt["rows"]
            )
        )

    def test_owner_portfolio_executes_only_bounded_rows(self):
        portfolio = load(
            X2_ROOT / "portfolios" / "owner-execution.json"
        )
        self.assertEqual(
            sum(row["state"] == "completed" for row in portfolio["safe_now_packets"]),
            120,
        )
        self.assertEqual(
            sum(row["state"] == "completed" for row in portfolio["owner_candidates"]),
            60,
        )
        self.assertEqual(
            sum(row["state"] == "represented" for row in portfolio["owner_candidates"]),
            20,
        )
        self.assertEqual(
            sum(row["state"] == "completed" for row in portfolio["owner_clean_fix_refine"]),
            100,
        )
        self.assertEqual(portfolio["external_actions"], 0)
        self.assertEqual(portfolio["destructive_actions"], 0)
        self.assertEqual(portfolio["real_rows"], 0)

    def test_exact_and_blocked_packets_remain_unexecuted(self):
        holds = load(
            X2_ROOT / "portfolios" / "protected-holds.json"
        )
        self.assertEqual(holds["executed_holds"], 0)
        self.assertEqual(len(holds["exact_approval_packets"]), 20)
        self.assertEqual(len(holds["blocked_packets"]), 10)
        self.assertTrue(
            all(
                row["state"] == "exact_approval_required_unexecuted"
                for row in holds["exact_approval_packets"]
            )
        )
        self.assertTrue(
            all(
                row["state"] == "blocked_unexecuted"
                for row in holds["blocked_packets"]
            )
        )

    def test_practice_artifacts_are_zero_row_authority_nonclaims(self):
        truth = load(X2_ROOT / "phase-truth.json")
        self.assertEqual(truth["real_data_rows"], 0)
        self.assertEqual(truth["real_people"], 0)
        self.assertEqual(truth["real_keys_or_proofs"], 0)
        self.assertEqual(truth["network_calls"], 0)
        self.assertEqual(truth["external_actions"], 0)
        for key in (
            "empirical_confirmation",
            "professional_authority",
            "production_readiness",
            "legal_or_cultural_authority",
            "maori_authority",
            "independent_reproduction",
        ):
            self.assertFalse(truth[key], key)

    def test_lifecycle_selection_keeps_x1_context_separate(self):
        selection = load(
            X2_ROOT / "lifecycle" / "evidence-test-selection.json"
        )
        self.assertEqual(
            selection["immutable_x1_precommit_context"]["passed"], 12
        )
        self.assertIn(
            selection["current_x2_context"]["state"],
            {"pending_current_x2_selection", "valid_current_x2_selection"},
        )
        self.assertFalse(selection["full_repository_suite"])
        self.assertFalse(selection["independent_reproduction"])

    def test_evidence_manifest_matches_normalized_lf_bytes(self):
        manifest = load(VALIDATION / "x2-evidence-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            data = (REPO / entry["path"]).read_bytes().replace(
                b"\r\n", b"\n"
            )
            self.assertEqual(
                len(data), entry["bytes_normalized_lf"], entry["path"]
            )
            self.assertEqual(
                hashlib.sha256(data).hexdigest(),
                entry["sha256_normalized_lf"],
                entry["path"],
            )

    def test_all_phase_json_and_document_caps_hold(self):
        for path in ROOT.rglob("*.json"):
            load(path)
        for path in ROOT.rglob("*.md"):
            self.assertLessEqual(
                len(path.read_text(encoding="utf-8").split()), 100000
            )
        self.assertLess(
            len(list(ROOT.rglob("*"))),
            2000,
        )


if __name__ == "__main__":
    unittest.main()
