from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs" / "liora-venn" / "v674-v5" / "x2"
X1_HEAD = "8f1db387ab28e3b53e3aaadef33a044f2e023386"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class LioraV674V5X2Tests(unittest.TestCase):
    def test_head_is_immutable_x1_before_evidence_commit(self):
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True, encoding="utf-8").strip()
        self.assertEqual(head, X1_HEAD)

    def test_exact_outcome_partition_and_zero_real_rows(self):
        truth = load("phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 42, "exact_gate": 3, "open_gap": 3, "represented": 12})
        self.assertEqual(truth["real_data_rows"], 0)
        self.assertEqual(truth["external_action_count"], 0)
        self.assertFalse(truth["independent_reproduction"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["successor_contacted"])

    def test_sixty_contracts_and_witnesses_match_x1(self):
        contracts = sorted((ROOT / "contracts").glob("*.json"))
        witnesses = sorted((ROOT / "witnesses").glob("*.json"))
        self.assertEqual(len(contracts), 60)
        self.assertEqual(len(witnesses), 60)
        outcomes = Counter(json.loads(path.read_text(encoding="utf-8"))["observed_outcome"] for path in witnesses)
        self.assertEqual(outcomes, Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}))
        self.assertTrue(all(json.loads(path.read_text(encoding="utf-8"))["real_data_rows"] == 0 for path in witnesses))

    def test_all_preregistered_mutations_executed_and_rejected(self):
        corpus = load("mutations/mutation-corpus.json")
        receipt = load("mutations/mutation-receipt.json")
        self.assertEqual(corpus["row_count"], 240)
        self.assertEqual(receipt["executed"], 240)
        self.assertEqual(receipt["rejected"], 240)
        self.assertEqual(receipt["accepted_invalid"], 0)
        self.assertEqual(receipt["retained_zero_credit"], 240)

    def test_twenty_skills_quick_validated_read_and_smoke_used(self):
        receipt = load("skills/skill-validation-and-smoke-receipt.json")
        self.assertEqual(receipt["skill_count"], 20)
        self.assertEqual(receipt["quick_validated"], 20)
        self.assertEqual(receipt["smoke_used"], 20)
        self.assertEqual(receipt["global_installations"], 0)
        for row in receipt["skills"]:
            self.assertTrue(row["complete_file_read_confirmed_before_smoke"])
            self.assertEqual(len(row["assigned_proposals"]), 3)
            raw = (REPO / row["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row["sha256"])

    def test_ten_family_current_runners_were_used(self):
        receipt = load("runners/runner-validation-and-use-receipt.json")
        self.assertEqual(receipt["runner_count"], 10)
        for row in receipt["runners"]:
            self.assertTrue(row["expectation_matches"])
            self.assertTrue(row["smoke_used"])
            self.assertEqual(row["accepted_positive"], 6)
            self.assertEqual(row["rejected_invalid"], 24)
            raw = (REPO / row["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row["sha256"])

    def test_portfolio_execution_and_holds(self):
        expected = {
            "safe-now-ledger.json": (120, Counter({"completed": 120})),
            "candidate-ledger.json": (80, Counter({"completed": 60, "represented": 20})),
            "clean-fix-refine-ledger.json": (100, Counter({"completed": 100})),
            "exact-approval-ledger.json": (20, Counter({"held": 20})),
            "blocked-ledger.json": (10, Counter({"held": 10})),
            "successor-recommendations.json": (60, Counter({"held": 60})),
        }
        for name, (count, statuses) in expected.items():
            rows = load(f"portfolios/{name}")["rows"]
            self.assertEqual(len(rows), count)
            self.assertEqual(Counter(row["status"] for row in rows), statuses)
            self.assertTrue(all(row["real_data_rows"] == 0 and row["external_action_count"] == 0 for row in rows))

    def test_failure_gap_gate_and_method_counts_are_additive(self):
        negatives = load("retained-negative-register.json")
        self.assertEqual(negatives["activation_effective_negatives"], 38863)
        self.assertEqual(negatives["x1_operational_failures"], 14)
        self.assertEqual(negatives["x2_operational_failures"], 2)
        self.assertEqual(negatives["rejected_mutations"], 240)
        self.assertEqual(negatives["effective_negatives"], 39119)
        self.assertTrue(negatives["no_failure_erased_or_promoted"])
        gates = load("gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 322)
        self.assertEqual(gates["effective_exact_gates"], 315)
        methods = load("method-flow/ledger.json")
        self.assertEqual(methods["effective_methods"], methods["inherited_effective_methods"] + methods["phase_method_additions"])
        self.assertFalse(methods["recoveries_rewrite_failures"])

    def test_evidence_manifest_matches_current_bytes(self):
        manifest = load("validation/evidence-owner-manifest.json")
        for entry in manifest["entries"]:
            raw = (REPO / entry["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])
            self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_staged_review_matches_index_and_has_no_confirmed_hit(self):
        review = load("validation/evidence-staged-review.json")
        self.assertEqual(review["status"], "passed")
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["unresolved_privacy_candidates"], [])
        self.assertEqual(review["confirmed_privacy_hits"], [])
        for entry in review["entries"]:
            raw = subprocess.check_output(["git", "show", f":{entry['path']}"], cwd=REPO)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])

    def test_all_json_python_markdown_html_and_caps(self):
        owner_files = [path for path in ROOT.rglob("*") if path.is_file()]
        owner_files.extend(REPO / f"scripts/ghc_family_liora_v674_v5_{name}.py" for name in [
            "contract_core", "lifecycle_state", "correction_lineage", "vacancy_visibility", "unit_uncertainty",
            "source_status", "nonclaim_firewall", "authority_gate", "minimum_disclosure", "handover_readback", "mutation_rejection"
        ])
        owner_files.extend([REPO / "scripts/build_ghc_family_liora_venn_v674_v5_x2.py", REPO / "tests/test_ghc_family_liora_venn_v674_v5_x2.py"])
        self.assertLess(len(owner_files), 2000)
        for path in owner_files:
            text = path.read_text(encoding="utf-8")
            self.assertLessEqual(len(text.split()), 100000, path)
            if path.suffix == ".json":
                json.loads(text)


if __name__ == "__main__":
    unittest.main()
