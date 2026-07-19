from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / "v649-v2"
SCRIPTS = ROOT / "scripts"
X1_COMMIT = "d20d13d2e17adbf35d0088fb38c66fab470a460f"

sys.path.insert(0, str(SCRIPTS))
from ghc_family_v649_v2_runtime import SURFACES, evaluate, mutation_fixtures, valid_fixture  # noqa: E402


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V649V2EvidenceTests(unittest.TestCase):
    def test_exact_ten_outcome_distribution(self):
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(len(ledger["proposals"]), 10)
        self.assertEqual(ledger["outcome_distribution"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(set(x["observed_outcome"] for x in ledger["proposals"]), {"completed", "represented", "open_gap", "exact_gate"})

    def test_all_surfaces_accept_valid_and_reject_mutations(self):
        self.assertEqual(len(SURFACES), 10)
        for surface in SURFACES:
            self.assertTrue(evaluate(surface, valid_fixture(surface))["accepted"], surface)
            mutations = mutation_fixtures(surface)
            self.assertEqual(len(mutations), 7)
            self.assertTrue(all(not evaluate(surface, row["fixture"])["accepted"] for row in mutations), surface)

    def test_all_seventy_preregistered_mutations_rejected(self):
        receipt = load("validation/x2-synthetic-mutation-results.json")
        self.assertEqual(receipt["count"], 70)
        self.assertEqual(receipt["rejected"], 70)
        self.assertEqual(receipt["accepted"], 0)

    def test_expanded_portfolio_counts(self):
        self.assertEqual(load("portfolios/safe-now-ledger.json")["completed"], 30)
        self.assertEqual(load("portfolios/candidate-ledger.json")["built_tested_invoked"], 20)
        self.assertEqual(load("portfolios/skill-ledger.json")["initialized_customized_smoke_used"], 20)
        self.assertEqual(load("portfolios/runner-ledger.json")["accept_and_reject_witnessed"], 10)
        self.assertEqual(load("maintenance/clean-fix-refine-ledger.json")["completed"], 30)

    def test_skill_packages_are_customized_and_have_two_fixtures(self):
        ledger = load("portfolios/skill-ledger.json")
        for skill in ledger["skills"]:
            folder = PHASE / "skills" / skill["name"]
            text = (folder / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("TODO", text)
            self.assertTrue((folder / "agents" / "openai.yaml").stat().st_size > 0)
            self.assertTrue((folder / "valid-fixture.json").is_file())
            self.assertTrue((folder / "rejecting-fixture.json").is_file())
            self.assertTrue(skill["smoke_used"])

    def test_family_current_runners_exist(self):
        ledger = load("portfolios/runner-ledger.json")
        self.assertEqual(len(ledger["runners"]), 10)
        for row in ledger["runners"]:
            self.assertTrue(row["runner"].startswith("ghc_family_"))
            self.assertTrue((SCRIPTS / row["runner"]).is_file())
            self.assertEqual(row["accepting_returncode"], 0)
            self.assertEqual(row["rejecting_returncode"], 2)

    def test_zero_row_and_authority_gates_remain_zero(self):
        ledger = load("x2-proposal-ledger.json")
        for row in ledger["proposals"]:
            self.assertTrue(all(value == 0 for value in row["real_or_authority_gate_counts"].values()))
        gates = load("exact-open-gate-register-x2.json")
        self.assertEqual(gates["effective_open_gaps"], 36)
        self.assertEqual(gates["effective_exact_gates"], 37)
        self.assertTrue(gates["none_silently_closed"])

    def test_all_negatives_preserved(self):
        negatives = load("retained-negative-register-x2.json")
        self.assertEqual(negatives["inherited_effective"], 4745)
        self.assertEqual(negatives["new_x1_operational"], 4)
        self.assertEqual(negatives["new_x2_operational"], len(negatives["x2_operational_negatives"]))
        self.assertEqual(negatives["preregistered_synthetic_executed_and_rejected"], 70)
        expected = negatives["inherited_effective"] + negatives["new_x1_operational"] + negatives["new_x2_operational"] + negatives["preregistered_synthetic_executed_and_rejected"]
        self.assertEqual(negatives["current_effective"], expected)
        self.assertTrue(negatives["no_negative_erased"])

    def test_x1_git_blob_seal_unchanged(self):
        manifest = load("validation/x1-staged-manifest.json")
        self.assertEqual(manifest["entry_count"], 48)
        for entry in manifest["entries"]:
            proc = subprocess.run(
                ["git", "rev-parse", f"{X1_COMMIT}:{entry['path']}"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertEqual(proc.stdout.strip(), entry["git_blob"], entry["path"])

    def test_source_status_vocabulary_and_no_observation_conversion(self):
        source = load("sources/source-ledger.json")
        self.assertTrue(source["sources"])
        self.assertTrue(all(row["status"] in {"current", "stable", "draft", "watch"} for row in source["sources"]))
        audit = load("sources/source-status-drift-audit.json")
        self.assertFalse(audit["citations_are_empirical_observations"])

    def test_method_flow_preserves_fail_and_pass_witnesses(self):
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertGreaterEqual(ledger["counts"]["witness_results"]["fail"], 8)
        self.assertGreaterEqual(ledger["counts"]["witness_results"]["pass"], 8)
        self.assertEqual(ledger["counts"]["states"]["preferred"], ledger["counts"]["methods"])

    def test_phase_truth_remains_not_ready(self):
        truth = load("phase-truth-x2.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])
        self.assertTrue(truth["same_owner_only"])


if __name__ == "__main__":
    unittest.main()
