from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "vesper-arlen" / "v650-v1"
SOURCE = "2275e611e74cbd6f1d84e2d9f018b2eed720a169"
EVIDENCE = "95918f8f6d66a6bc9458cf2a7fffb4e2b9a6d85f"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


class V650V1CorrectionTests(unittest.TestCase):
    def test_lifecycle_negative_and_method_flow(self) -> None:
        negatives = load("lifecycle/retained-negative-register-final.json")
        summary = load("method-flow/method-flow-summary-final.json")
        self.assertEqual((negatives["evidence_effective"], negatives["lifecycle_operational"], negatives["effective_final"]), (5573, 4, 5577))
        self.assertFalse(negatives["negative_erased"])
        self.assertEqual(summary["counts"]["methods"], 26)
        self.assertEqual(summary["counts"]["witness_results"], {"fail": 26, "pass": 26})

    def test_additive_final_validator_preserves_repository_paths(self) -> None:
        evidence = (ROOT / "scripts" / "ghc_family_v650_v1_validate.py").read_text(encoding="utf-8")
        final = (ROOT / "scripts" / "ghc_family_v650_v1_final_validate.py").read_text(encoding="utf-8")
        self.assertIn('repository_path = f"docs/vesper-arlen/v650-v1/{repository_path}"', evidence)
        self.assertNotIn('repository_path = f"docs/vesper-arlen/v650-v1/{repository_path}"', final)
        self.assertIn("ghc_family_v650_v1_final_validate.py", final)

    def test_baton_and_closeout_baseline(self) -> None:
        baton = (PHASE / "handoffs" / "ilyra-fen-v650-v2-activation.md").read_text(encoding="utf-8")
        words = len(baton.split())
        self.assertGreaterEqual(words, 8000)
        self.assertLessEqual(words, 20000)
        self.assertIn("5,577 effective negatives", baton)
        receipt = load("closeout-receipt.json")
        self.assertEqual(receipt["effective_negatives"], 5577)
        self.assertEqual(receipt["post_evidence_operational_negatives"], 4)
        self.assertEqual((receipt["method_fail_witnesses"], receipt["method_pass_witnesses"]), (26, 26))

    def test_manifest_and_staged_review(self) -> None:
        manifest = load("validation/final-owner-manifest.json")
        review = load("validation/final-staged-review.json")
        self.assertEqual(manifest["declared_exclusion_count"], 4)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            self.assertEqual(row["git_blob"], git("hash-object", f"--path={row['repository_path']}", row["repository_path"]))
        self.assertTrue(review["passed"])
        self.assertEqual(review["evidence_frozen_changes"], [])
        self.assertEqual(review["out_of_scope_paths"], [])
        self.assertEqual(review["privacy_confirmed_hits"], 0)

    def test_commit_cap_and_ancestry(self) -> None:
        subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE, "HEAD"], cwd=ROOT, check=True)
        count = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
        self.assertIn(count, {3, 4})
        self.assertEqual(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD"), "0")


if __name__ == "__main__":
    unittest.main()
