from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_caelen_ash_v684_v6_contracts import validate_fixture


BASE = ROOT / "docs" / "caelen-ash" / "v684-v6"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
X1_COMMIT = "ab50360d737177ab1ebe4564b348a88b540c9ed4"


def load(name: str):
    return json.loads((X2 / name).read_text(encoding="utf-8"))


class CaelenAshV684V6X2Tests(unittest.TestCase):
    def test_01_exact_x1_parent(self):
        self.assertEqual(
            subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            X1_COMMIT,
        )

    def test_02_sixty_positive_controls(self):
        controls = load("positive-controls.json")
        self.assertEqual(controls["total"], 60)
        self.assertEqual(controls["passed"], 60)
        for row in controls["entries"]:
            passed, errors = validate_fixture(row["fixture"])
            self.assertTrue(passed, errors)

    def test_03_three_hundred_mutations_rejected(self):
        mutations = load("rejecting-mutations.json")
        self.assertEqual(mutations["total"], 300)
        self.assertEqual(mutations["rejected"], 300)
        self.assertTrue(all(item["rejected"] and not item["accepted"] for item in mutations["entries"]))
        self.assertTrue(all(item["completion_credit"] == 0 for item in mutations["entries"]))

    def test_04_outcome_vocabulary_and_counts(self):
        ledger = load("outcome-ledger.json")
        self.assertEqual(set(ledger["allowed_labels"]), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertEqual(ledger["counts"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(len(ledger["entries"]), 60)
        self.assertEqual(Counter(item["outcome"] for item in ledger["entries"]), Counter(ledger["counts"]))

    def test_05_proposal_and_witness_files(self):
        self.assertEqual(len(list((X2 / "proposals").glob("*.json"))), 60)
        self.assertEqual(len(list((X2 / "witnesses").glob("*.json"))), 60)

    def test_06_portfolio_execution(self):
        self.assertEqual(load("safe-now-execution.json")["completed"], 120)
        self.assertEqual(load("candidate-execution.json")["completed"], 80)
        cfr = load("clean-fix-refine-execution.json")
        self.assertEqual(cfr["completed"], 100)
        self.assertEqual(cfr["destructive_actions"], 0)

    def test_07_exact_and_blocked_stay_unexecuted(self):
        holds = load("approval-hold-state.json")
        self.assertEqual(holds["executed"], 0)
        self.assertEqual(holds["retained_unexecuted"], 30)
        self.assertTrue(all(item["state"] == "HELD_UNEXECUTED" for item in holds["exact_approval_packets"]))
        self.assertTrue(all(item["state"] == "BLOCKED_UNEXECUTED" for item in holds["blocked_packets"]))

    def test_08_skills_quick_validated_and_smoke_used(self):
        receipt = load("skill-use-receipts.json")
        self.assertEqual(receipt["total"], 20)
        self.assertEqual(receipt["validated"], 20)
        self.assertEqual(receipt["smoke_used"], 20)
        self.assertTrue(all(item["quick_validation_passed"] and item["smoke_passed"] for item in receipt["entries"]))
        self.assertFalse(receipt["global_installation"])

    def test_09_ten_runners_used(self):
        receipt = load("runner-use-receipts.json")
        self.assertEqual(receipt["total"], 10)
        self.assertEqual(receipt["passed"], 10)
        self.assertTrue(all(item["passed"] for item in receipt["entries"]))

    def test_10_skill_packages_substantive(self):
        skill_dirs = sorted((X2 / "skills").iterdir())
        self.assertEqual(len(skill_dirs), 20)
        for path in skill_dirs:
            text = (path / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## Workflow", text)
            self.assertIn("## Boundaries", text)
            self.assertTrue((path / "agents" / "openai.yaml").exists())

    def test_11_family_current_runners(self):
        runners = sorted((X2 / "runners").glob("ghc_family_*.py"))
        self.assertEqual(len(runners), 10)
        for runner in runners:
            compile(runner.read_text(encoding="utf-8"), runner.name, "exec")

    def test_12_x1_paths_unchanged(self):
        changed = subprocess.run(
            ["git", "diff", "--name-only", X1_COMMIT, "--", f"docs/caelen-ash/v684-v6/x1", f"docs/caelen-ash/v684-v6/method-flow", f"docs/caelen-ash/v684-v6/workflow-refinement", f"docs/caelen-ash/v684-v6/reflection-remaster", f"docs/caelen-ash/v684-v6/tooling"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(changed, "")

    def test_13_x1_manifest_replays(self):
        manifest_raw = subprocess.run(
            ["git", "show", f"{X1_COMMIT}:docs/caelen-ash/v684-v6/validation/x1-index-manifest.json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        manifest = json.loads(manifest_raw)
        for entry in manifest["entries"]:
            data = subprocess.run(
                ["git", "show", f"{X1_COMMIT}:{entry['path']}"], cwd=ROOT, capture_output=True, check=True
            ).stdout
            data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_14_privacy_scan(self):
        scan = json.loads((VALIDATION / "evidence-privacy-scan.json").read_text(encoding="utf-8"))
        self.assertEqual(len(scan["pattern_classes"]), 5)
        self.assertEqual(scan["confirmed_hit_count"], 0)

    def test_15_manifest_matches_working_files(self):
        manifest = json.loads((VALIDATION / "evidence-index-manifest.json").read_text(encoding="utf-8"))
        self.assertGreater(manifest["entry_count"], 150)
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_16_all_phase_json_parses(self):
        for path in BASE.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

    def test_17_owner_file_ceiling(self):
        self.assertLess(len([path for path in BASE.rglob("*") if path.is_file()]), 2000)

    def test_18_document_word_cap(self):
        for path in BASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000)

    def test_19_terminal_truth(self):
        truth = load("evidence-truth.json")
        self.assertTrue(truth["execution_receipts_complete"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["real_rows"], 0)
        self.assertEqual(truth["authority_actions"], 0)

    def test_20_staged_review_shape(self):
        review = json.loads((VALIDATION / "evidence-staged-review.json").read_text(encoding="utf-8"))
        self.assertIn(review["state"], {"PREPARED_NOT_STAGED", "PASS"})
        if review["state"] == "PASS":
            self.assertEqual(review["manifest_mismatches"], [])
            self.assertEqual(review["missing_paths"], [])
            self.assertEqual(review["out_of_scope_paths"], [])
            self.assertEqual(review["x1_paths_changed"], [])


if __name__ == "__main__":
    unittest.main()
