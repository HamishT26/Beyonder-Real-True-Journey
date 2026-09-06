from __future__ import annotations

import hashlib
import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sable-rook" / "v687-v3"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
X1_COMMIT = "1a57a093dff78bcb217de33f9c5f282d3ee8bf17"
BRANCH = "codex/GHC-Family/sable-rook-v687-v3-full-tools"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, text=True, encoding="utf-8", capture_output=True).stdout.strip()


class SableRookV687V3X2Tests(unittest.TestCase):
    def test_01_exact_x1_head_and_branch(self):
        self.assertEqual(git("rev-parse", "HEAD"), X1_COMMIT)
        self.assertEqual(git("branch", "--show-current"), BRANCH)

    def test_02_no_x1_drift(self):
        changed = git("diff", "--name-only", X1_COMMIT, "--", "docs/sable-rook/v687-v3/x1", "docs/sable-rook/v687-v3/method-flow", "docs/sable-rook/v687-v3/workflow-refinement", "docs/sable-rook/v687-v3/reflection-remaster", "docs/sable-rook/v687-v3/tooling", "scripts/build_ghc_family_sable_rook_v687_v3_x1.py", "tests/test_ghc_family_sable_rook_v687_v3_x1.py")
        self.assertEqual(changed, "")

    def test_03_positive_controls(self):
        data = load(X2 / "contract-results.json")
        self.assertEqual(data["passed"], 200)
        self.assertEqual(data["total"], 200)
        self.assertTrue(all(row["complete_output_match"] for row in data["entries"]))

    def test_04_rejecting_mutations(self):
        data = load(X2 / "mutation-results.json")
        self.assertEqual(data["rejected"], 1000)
        self.assertEqual(data["accepted"], 0)
        self.assertTrue(all(row["original_success_credit"] == 0 for row in data["entries"]))

    def test_05_outcomes(self):
        ledger = load(X2 / "outcome-ledger.json")
        self.assertEqual(ledger["counts"], {"completed": 160, "represented": 20, "open_gap": 10, "exact_gate": 10})
        self.assertEqual(set(ledger["allowed_labels"]), {"completed", "represented", "open_gap", "exact_gate"})

    def test_06_package_wheels(self):
        receipt = load(X2 / "package-receipt.json")
        self.assertEqual(receipt["distribution_count"], 3)
        self.assertTrue(all(row["match"] for row in receipt["wheels"]))
        self.assertEqual(receipt["versions"], {"rfc8785": "0.1.4", "confusable-homoglyphs": "3.3.1", "blake3": "1.0.9"})

    def test_07_package_smokes(self):
        receipt = load(X2 / "package-receipt.json")
        self.assertTrue(all(receipt["positive_smokes"].values()))
        self.assertTrue(all(receipt["adverse_smokes"].values()))
        self.assertFalse(receipt["system_python_mutated"])
        self.assertFalse(receipt["shared_prefix_mutated"])

    def test_08_advisory_snapshot_boundary(self):
        snapshot = load(X2 / "package-advisory-snapshot.json")
        self.assertEqual(len(snapshot["entries"]), 3)
        self.assertTrue(snapshot["snapshot_only"])
        self.assertFalse(snapshot["exhaustive_security"])

    def test_09_skills_built_validated_used(self):
        receipt = load(X2 / "skill-validation.json")
        self.assertEqual(receipt["quick_validated"], 10)
        self.assertEqual(receipt["smoke_used"], 10)
        self.assertEqual(receipt["total"], 10)

    def test_10_skill_scaffolds_replaced(self):
        skills = list((BASE / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 10)
        for path in skills:
            self.assertNotIn("TODO", path.read_text(encoding="utf-8"))

    def test_11_skill_manifests(self):
        manifests = list((BASE / "skills").glob("*/manifest.json"))
        self.assertEqual(len(manifests), 10)
        for path in manifests:
            manifest = load(path)
            self.assertGreaterEqual(manifest["entry_count"], 4)
            for entry in manifest["entries"]:
                data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_12_runners_built_and_used(self):
        receipt = load(X2 / "runner-use.json")
        self.assertEqual(receipt["passed"], 10)
        self.assertEqual(receipt["total"], 10)
        self.assertTrue(all(row["output_match"] for row in receipt["entries"]))

    def test_13_portfolio_execution(self):
        receipt = load(X2 / "portfolio-execution.json")
        self.assertEqual(len(receipt["safe"]), 300)
        self.assertEqual(len(receipt["candidates"]), 250)
        self.assertEqual(len(receipt["clean_fix_refine"]), 300)
        self.assertEqual(len(receipt["exact"]), 50)
        self.assertEqual(len(receipt["blocked"]), 30)

    def test_14_candidates_receive_no_invalid_credit(self):
        receipt = load(X2 / "portfolio-execution.json")
        self.assertTrue(all(not row["candidate_accepted"] and row["invalid_candidate_success_credit"] == 0 for row in receipt["candidates"]))

    def test_15_exact_and_blocked_remain_held(self):
        receipt = load(X2 / "portfolio-execution.json")
        self.assertTrue(all(row["state"] == "HELD_UNEXECUTED" for row in receipt["exact"] + receipt["blocked"]))

    def test_16_counts(self):
        counts = load(X2 / "evidence-counts.json")["x2_effective"]
        self.assertEqual(counts["effective_negatives"], 77888)
        self.assertEqual(counts["effective_methods"], 93040)
        self.assertEqual(counts["failed_witnesses"], 48736)
        self.assertEqual(counts["bounded_passing_witnesses"], 77035)
        self.assertEqual(counts["open_gaps"], 674)
        self.assertEqual(counts["exact_gates"], 659)

    def test_17_x1_manifest_replay(self):
        receipt = load(X2 / "x1-manifest-replay.json")
        self.assertTrue(receipt["passed"])
        self.assertEqual(receipt["entries"], 62)

    def test_18_content_seal(self):
        seal = load(X2 / "content-seal.json")
        self.assertEqual(seal["target_count"], 9)
        for entry in seal["targets"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_19_privacy(self):
        scan = load(VALIDATION / "x2-privacy-scan.json")
        self.assertEqual(len(scan["pattern_classes"]), 5)
        self.assertEqual(scan["confirmed_hit_count"], 0)

    def test_20_bounded_ast_security(self):
        scan = load(VALIDATION / "x2-ast-security.json")
        self.assertEqual(scan["finding_count"], 0)
        self.assertFalse(scan["exhaustive_security"])

    def test_21_x2_manifest_working(self):
        manifest = load(VALIDATION / "x2-manifest.json")
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(len(data), entry["bytes_normalized_lf"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_22_x2_method_flow_valid(self):
        receipt = load(X2 / "method-flow" / "validation.json")
        self.assertTrue(receipt["valid"])

    def test_23_all_json_parses(self):
        paths = list(BASE.rglob("*.json"))
        self.assertGreater(len(paths), 75)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_24_file_ceiling(self):
        owner_files = [path for path in BASE.rglob("*") if path.is_file()]
        owner_files += list((ROOT / "scripts").glob("*sable_rook_v687_v3*.py"))
        owner_files += list((ROOT / "tests").glob("*sable_rook_v687_v3*.py"))
        self.assertLess(len(set(owner_files)), 2000)

    def test_25_document_cap(self):
        for path in BASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000)

    def test_26_phase_truth(self):
        truth = load(X2 / "phase-truth.json")
        self.assertEqual(truth["state"], "X2_EVIDENCE_CANDIDATE")
        self.assertFalse(truth["successor_contacted"])
        self.assertFalse(truth["future_seat_created"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_27_accessibility_reserved(self):
        receipt = load(X2 / "accessibility-reservation.json")
        self.assertTrue(receipt["manual_keyboard_reserved"])
        self.assertTrue(receipt["affected_user_evaluation_reserved"])
        self.assertFalse(receipt["complete_conformance_claimed"])

    def test_28_pillars(self):
        pillars = load(X2 / "pillar-synthesis.json")
        self.assertEqual(pillars["primary"], "Freed ID and CBR Heart")
        self.assertIn("research-model", pillars["GMUT Mind"])
        self.assertIn("proxy", pillars["THOS Body"])

    def test_29_staged_review_shape(self):
        review = load(VALIDATION / "x2-staged-review.json")
        self.assertIn(review["state"], {"PREPARED_NOT_STAGED", "PASS"})

    def test_30_no_route_or_authority_promotion(self):
        truth = load(X2 / "phase-truth.json")
        self.assertFalse(truth["successor_contacted"])
        self.assertEqual(set(load(X2 / "outcome-ledger.json")["allowed_labels"]), {"completed", "represented", "open_gap", "exact_gate"})


if __name__ == "__main__":
    unittest.main()
