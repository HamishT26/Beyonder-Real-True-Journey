from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "liora-venn" / "v680-v2"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
X1_HEAD = "04b3248d8fc62d7f81303eec1d452d6078586db3"
SOURCE = "9f030e7f85282ba3de7c378a8fc072c214396dcb"

sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_ceramics_contracts import MUTATION_TYPES, mutate, positive_fixture, validate


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


class LioraVennV680V2X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.freeze = load(X1 / "new-proposal-freeze.json")
        cls.proposals = cls.freeze["proposals"]
        cls.evidence = load(X2 / "proposal-evidence.json")
        cls.mutations = load(X2 / "mutations.json")
        cls.method = load(X2 / "method-flow-ledger.json")

    def test_lifecycle_starts_at_immutable_x1(self) -> None:
        self.assertEqual(git("rev-parse", "HEAD"), X1_HEAD)
        self.assertEqual(git("show", "-s", "--format=%P", "HEAD"), SOURCE)
        self.assertFalse((BASE / "final").exists())

    def test_all_proposals_have_positive_controls(self) -> None:
        positives = load(X2 / "positive-controls.json")
        self.assertEqual(positives["accepted_count"], 60)
        self.assertEqual(len(positives["receipts"]), 60)
        self.assertTrue(all(row["accepted"] and row["real_rows"] == 0 for row in positives["receipts"]))

    def test_exact_outcomes(self) -> None:
        self.assertEqual(self.evidence["outcome_counts"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(Counter(row["outcome"] for row in self.evidence["outcomes"]), Counter(self.evidence["outcome_counts"]))

    def test_every_mutation_executed_and_rejected(self) -> None:
        self.assertEqual(self.mutations["executed_count"], 300)
        self.assertEqual(self.mutations["rejected_count"], 300)
        self.assertEqual(self.mutations["accepted_invalid_count"], 0)
        self.assertTrue(all(not row["accepted"] and row["failed_witness_retained"] for row in self.mutations["receipts"]))

    def test_five_mutation_types_per_proposal(self) -> None:
        for proposal in self.proposals:
            rows = [row for row in self.mutations["receipts"] if row["proposal_id"] == proposal["proposal_id"]]
            self.assertEqual(len(rows), 5)
            self.assertEqual({row["mutation_type"] for row in rows}, set(MUTATION_TYPES))

    def test_contract_accepts_positive_and_rejects_each_mutation(self) -> None:
        for proposal in self.proposals:
            fixture = positive_fixture(proposal)
            self.assertTrue(validate(proposal, fixture)["accepted"])
            for mutation_type in MUTATION_TYPES:
                self.assertFalse(validate(proposal, mutate(fixture, mutation_type))["accepted"])

    def test_skill_receipts(self) -> None:
        receipt = load(X2 / "skill-smoke-receipts.json")
        self.assertEqual(receipt["skill_count"], 20)
        self.assertEqual(receipt["validated_count"], 20)
        self.assertEqual(receipt["smoke_used_count"], 20)
        self.assertTrue(all(row["read_through_eof"] and not row["global_install"] for row in receipt["receipts"]))

    def test_skill_scaffolds_are_fully_customized(self) -> None:
        skill_files = sorted((BASE / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skill_files), 20)
        for path in skill_files:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("TODO", text)
            for heading in ("## Scope", "## Inputs", "## Steps", "## Refusals", "## Outputs", "## Smoke fixture"):
                self.assertIn(heading, text)

    def test_runner_receipts(self) -> None:
        receipt = load(X2 / "runner-smoke-receipts.json")
        self.assertEqual(receipt["runner_count"], 10)
        self.assertEqual(receipt["passed_count"], 10)
        self.assertTrue(all(row["positive_accepted"] and row["invalid_rejected"] for row in receipt["receipts"]))

    def test_portfolio_results(self) -> None:
        portfolio = load(X2 / "portfolio-results.json")
        self.assertEqual(len(portfolio["safe_now"]), 120)
        self.assertEqual(len(portfolio["owner_candidates"]), 80)
        self.assertEqual(len(portfolio["clean_fix_refine"]), 100)
        self.assertEqual(len(portfolio["exact_approval"]), 20)
        self.assertEqual(len(portfolio["blocked"]), 10)
        self.assertTrue(all(row["state"] == "retained_unexecuted" for row in portfolio["exact_approval"] + portfolio["blocked"]))

    def test_method_flow_counts_and_non_erasure(self) -> None:
        counts = self.method["counts"]
        self.assertEqual(counts["effective_negatives"], 50712)
        self.assertEqual(counts["effective_methods"], 53999)
        self.assertEqual(counts["failed_witnesses"], 22373)
        self.assertEqual(counts["bounded_passing_witnesses"], 36242)
        self.assertEqual(len(self.method["x2_operational_failures"]), 4)
        self.assertEqual(
            [row["failure_id"] for row in self.method["x2_operational_failures"]],
            ["LV6802-X2-N001", "LV6802-X2-N002", "LV6802-X2-N003", "LV6802-X2-N004"],
        )
        self.assertTrue(all(row["initial_credit"] == 0 for row in self.method["x2_operational_failures"]))
        self.assertFalse(self.method["failure_erasure"])
        self.assertFalse(self.method["recoveries_retroactively_promote_failure"])

    def test_gate_counts(self) -> None:
        gates = load(X2 / "gate-register.json")
        self.assertEqual(gates["open_gaps"], 446)
        self.assertEqual(gates["exact_gates"], 437)
        self.assertEqual(gates["new_open_gaps"], 3)
        self.assertEqual(gates["new_exact_gates"], 3)

    def test_sources_do_not_confer_authority(self) -> None:
        receipt = load(X2 / "official-source-use-receipt.json")
        self.assertFalse(receipt["authority_conferred"])
        self.assertFalse(receipt["citations_are_observations"])
        self.assertEqual(receipt["real_data_rows"], 0)

    def test_threat_control_is_zero_real_world(self) -> None:
        receipt = load(X2 / "threat-control-evidence.json")
        self.assertEqual(receipt["external_actions"], 0)
        self.assertEqual(receipt["network_data_queries"], 0)
        self.assertEqual(receipt["real_rows"], 0)
        self.assertFalse(receipt["authority_conferred"])

    def test_privacy_and_security_scans(self) -> None:
        privacy = load(VALIDATION / "evidence-privacy-scan.json")
        security = load(VALIDATION / "evidence-security-scan.json")
        self.assertEqual(privacy["confirmed_hits"], [])
        self.assertEqual(len(privacy["privacy_classes"]), 5)
        self.assertEqual(security["bounded_findings"], 0)
        self.assertEqual(security["ast_errors"], [])

    def test_manifest_replays_worktree_bytes(self) -> None:
        manifest = load(VALIDATION / "evidence-index-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_staged_review_is_x2_only(self) -> None:
        review = load(VALIDATION / "evidence-staged-review.json")
        self.assertEqual(review["lifecycle"], "bounded_x2_evidence")
        self.assertTrue(all("/final/" not in path for path in review["expected_paths"]))
        self.assertTrue(all("/x1/" not in path for path in review["expected_paths"]))

    def test_successor_is_zero_credit_and_uncontacted(self) -> None:
        successor = load(X2 / "successor-recommendations.json")
        self.assertEqual(successor["Liora_completion_credit"], 0)
        self.assertTrue(successor["recipient_not_contacted"])

    def test_terminal_verdict(self) -> None:
        phase = load(X2 / "phase-truth.json")
        self.assertEqual(phase["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
