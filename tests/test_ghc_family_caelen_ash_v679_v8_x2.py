from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v679-v8"
X1 = PHASE / "x1"
X2 = PHASE / "x2"
SKILLS = PHASE / "skills"
EXPECTED_X1 = "196de83c91c9d13a76fd4baaf296e2ac15997607"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class CaelenAshV679V8X2Tests(unittest.TestCase):
    def test_x1_is_immutable_ancestor(self) -> None:
        result = subprocess.run(["git", "merge-base", "--is-ancestor", EXPECTED_X1, "HEAD"], cwd=ROOT)
        self.assertEqual(result.returncode, 0)
        changed = subprocess.check_output(["git", "diff", "--name-only", EXPECTED_X1, "HEAD", "--", "docs/caelen-ash/v679-v8/x1"], cwd=ROOT, text=True, encoding="utf-8").splitlines()
        self.assertEqual(changed, [])

    def test_outcomes_exact(self) -> None:
        rows = load(X2 / "proposal-outcomes.json")["rows"]
        self.assertEqual(len(rows), 60)
        counts = {label: sum(row["outcome"] == label for row in rows) for label in ALLOWED}
        self.assertEqual(counts, {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertTrue(all(row["outcome"] in ALLOWED for row in rows))
        self.assertTrue(all(row["protected_gates_preserved"] for row in rows))

    def test_controls_and_mutations(self) -> None:
        controls = load(X2 / "positive-controls.json")["rows"]
        mutations = load(X2 / "rejected-mutations.json")["rows"]
        self.assertEqual(len(controls), 60)
        self.assertTrue(all(row["acceptance_state"] == "VALID_BOUNDED_CONTROL" for row in controls))
        self.assertEqual(len(mutations), 160)
        self.assertTrue(all(not row["accepted"] and row["retained"] for row in mutations))
        self.assertEqual(len({row["mutation_id"] for row in mutations}), 160)

    def test_portfolio_execution_and_holds(self) -> None:
        data = load(X2 / "portfolio-execution.json")
        self.assertEqual(len(data["safe_now"]), 120)
        self.assertEqual(len(data["owner_candidates"]), 80)
        self.assertEqual(len(data["clean_fix_refine"]), 100)
        self.assertEqual(len(data["successor_candidates"]), 20)
        self.assertEqual(len(data["exact_approval"]), 20)
        self.assertEqual(len(data["blocked"]), 10)
        self.assertTrue(all(row["execution_state"] == "completed" for row in data["safe_now"]))
        self.assertTrue(all(row["state"] == "recommendation_only" and row["completion_credit"] == 0 for row in data["successor_candidates"]))

    def test_skills_substantive_validated_and_used(self) -> None:
        receipts = load(X2 / "skill-validation-and-use.json")["rows"]
        self.assertEqual(len(receipts), 20)
        self.assertEqual(len(list(SKILLS.glob("*/SKILL.md"))), 20)
        for row in receipts:
            text = (SKILLS / row["skill"] / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## Workflow", text)
            self.assertIn("## Refusal conditions", text)
            metadata = (SKILLS / row["skill"] / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn("default_prompt:", metadata)
            self.assertIn("$" + row["skill"], metadata)
            self.assertEqual(row["quick_validation"], "passed")
            self.assertEqual(row["smoke_state"], "VALID_BOUNDED_RUNNER_SMOKE")
            self.assertTrue(row["openai_yaml_customized"])
            self.assertFalse(row["global_installation"])

    def test_runners_are_family_current_and_smoke_used(self) -> None:
        receipts = load(X2 / "runner-witnesses.json")["rows"]
        self.assertEqual(len(receipts), 10)
        for row in receipts:
            self.assertTrue(row["runner"].startswith("ghc_family_"))
            self.assertEqual(row["state"], "VALID_BOUNDED_RUNNER_SMOKE")
            path = ROOT / "scripts" / row["runner"]
            result = subprocess.run([sys.executable, "-X", "utf8", str(path), "--self-test"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_method_flow_retains_failures(self) -> None:
        flow = load(X2 / "method-flow-evidence.json")
        self.assertEqual(len(flow["failures"]), 8)
        self.assertEqual(len(flow["passing_recoveries"]), 8)
        self.assertTrue(all(row["success_credit"] == 0 for row in flow["failures"]))
        self.assertEqual(flow["counts"]["effective_negatives"], 50087)
        self.assertEqual(flow["counts"]["methods"], 52534)
        self.assertEqual(flow["counts"]["failed_witnesses"], 21748)
        self.assertEqual(flow["counts"]["bounded_passing_witnesses"], 34837)
        self.assertEqual(flow["counts"]["open_gaps"], 440)
        self.assertEqual(flow["counts"]["exact_gates"], 431)

    def test_truth_and_authority_boundaries(self) -> None:
        truth = load(X2 / "phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["empirical_rows"], 0)
        self.assertFalse(truth["authority_conferred"])
        self.assertFalse(truth["independent_reproduction"])
        self.assertEqual(truth["route_state"], "HELD_PREPARED_NOT_SENT")
        self.assertEqual(truth["outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertFalse(load(X2 / "gmut-analogy-firewall.json")["theory_of_everything_claimed"])
        self.assertFalse(load(X2 / "thos-proxy-boundary.json")["operational_effectiveness_claimed"])
        self.assertFalse(load(X2 / "authority-vacancy-matrix.json")["software_authority"])

    def test_all_phase_json_strict(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 35)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_documents_below_cap_and_file_guard(self) -> None:
        files = [path for path in PHASE.rglob("*") if path.is_file()]
        self.assertLess(len(files), 2000)
        for path in files:
            if path.suffix.lower() in {".md", ".html"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path.as_posix())

    def test_evidence_staged_receipts_when_present(self) -> None:
        manifest_path = PHASE / "validation" / "evidence-index-manifest.json"
        if not manifest_path.exists():
            self.skipTest("evidence staged review not generated yet")
        manifest = load(manifest_path)
        review = load(PHASE / "validation" / "evidence-staged-review.json")
        privacy = load(PHASE / "validation" / "evidence-privacy-scan.json")
        security = load(PHASE / "validation" / "evidence-security-scan.json")
        self.assertEqual(review["state"], "VALID_EXACT_EVIDENCE_STAGED_REVIEW")
        self.assertEqual(manifest["entry_count"], review["reviewed_entries"])
        self.assertEqual(len(manifest["declared_self_exclusions"]), 4)
        self.assertEqual(review["confirmed_privacy_hits"], 0)
        self.assertEqual(privacy["confirmed_hits"], [])
        self.assertEqual(security["bounded_findings"], [])

    def test_diff_hygiene(self) -> None:
        result = subprocess.run(["git", "diff", "--check"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
