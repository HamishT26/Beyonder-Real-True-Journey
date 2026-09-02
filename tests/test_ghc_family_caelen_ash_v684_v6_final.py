from __future__ import annotations

import hashlib
import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "caelen-ash" / "v684-v6"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
VALIDATION = BASE / "validation"
SOURCE = "9a2fcdc6021dcc8226ff7150b990bfe429671680"
X1_COMMIT = "ab50360d737177ab1ebe4564b348a88b540c9ed4"
EVIDENCE_COMMIT = "ca4ac41d8984e8fcec58982bfd6507030dcd1480"
PREVIOUS_FINAL = EVIDENCE_COMMIT
BRANCH = "codex/GHC-Family/caelen-ash-v684-v6-full-tools"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()


def replay_manifest(commit: str, path: str) -> int:
    manifest = json.loads(git("show", f"{commit}:{path}"))
    for entry in manifest["entries"]:
        data = subprocess.run(["git", "show", f"{commit}:{entry['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if hashlib.sha256(data).hexdigest() != entry["sha256_normalized_lf"]:
            raise AssertionError(entry["path"])
    return len(manifest["entries"])


class CaelenAshV684V6FinalTests(unittest.TestCase):
    def test_01_exact_lifecycle_context(self):
        head = git("rev-parse", "HEAD")
        expected = os.environ.get("CA6846_EXPECTED_FINAL")
        if expected:
            self.assertEqual(head, expected)
            self.assertEqual(git("rev-parse", "HEAD^"), PREVIOUS_FINAL)
        else:
            self.assertEqual(head, PREVIOUS_FINAL)
        self.assertEqual(git("branch", "--show-current"), BRANCH)

    def test_02_final_candidate_truth(self):
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual(truth["lifecycle"], "FINAL_CANDIDATE_PRECOMMIT")
        self.assertEqual(truth["exact_final"], "PENDING_COMMIT")
        self.assertEqual(truth["external_canonical"], "PENDING_POSTCOMMIT")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_03_outcome_counts(self):
        summary = load(FINAL / "final-summary.json")
        self.assertEqual(summary["outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(summary["proposal_chain"], 11030)

    def test_04_evidence_counts(self):
        receipt = load(CLOSEOUT / "evidence-receipt.json")
        self.assertEqual(receipt["positive_controls"], {"passed": 60, "total": 60})
        self.assertEqual(receipt["rejecting_mutations"], {"rejected": 300, "total": 300})
        self.assertEqual(receipt["skills"]["quick_validated"], 20)
        self.assertEqual(receipt["runners"], {"passed": 10, "total": 10})

    def test_05_negative_register(self):
        register = load(CLOSEOUT / "retained-negative-register.json")
        self.assertEqual(register["effective_negatives"], 59730)
        self.assertEqual(register["effective_methods"], 73690)
        self.assertEqual(register["retained_failed_witnesses"], 30791)
        self.assertEqual(register["bounded_passing_witnesses"], 54225)
        self.assertEqual(register["final_selection_operational_failures"], 0)
        self.assertEqual(register["final_selection_recoveries"], 0)
        self.assertEqual(register["canonical_preflight_operational_failures"], 0)
        self.assertEqual(register["canonical_preflight_recoveries"], 0)

    def test_06_gate_register(self):
        gates = load(CLOSEOUT / "gate-register.json")
        self.assertEqual(gates["open_gaps"], 531)
        self.assertEqual(gates["exact_gates"], 521)
        self.assertEqual(gates["silently_closed"], 0)

    def test_07_complete_incomplete_truth(self):
        checklist = load(CLOSEOUT / "complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(checklist["complete"]), 10)
        self.assertGreaterEqual(len(checklist["incomplete"]), 9)
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_08_content_seal(self):
        seal = load(CLOSEOUT / "content-seal.json")
        self.assertEqual(seal["entry_count"], 8)
        for entry in seal["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_09_handoff_candidate_range_and_hold(self):
        receipt = load(CLOSEOUT / "handoff-candidate-receipt.json")
        self.assertTrue(receipt["within_range"])
        self.assertGreaterEqual(receipt["words"], 10000)
        self.assertLessEqual(receipt["words"], 100000)
        self.assertEqual(receipt["state"], "PREPARED_NOT_SENT")
        route = load(CLOSEOUT / "route-readiness.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)

    def test_10_final_overview_three_page_equivalent(self):
        words = len((FINAL / "final-integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 1500)
        self.assertLessEqual(words, 100000)

    def test_11_static_report_structure(self):
        text = (FINAL / "final-report.html").read_text(encoding="utf-8")
        for token in ["<title>", "<main>", "<h1>", "<caption>", 'scope="col"', 'scope="row"']:
            self.assertIn(token, text)
        self.assertIn("Manual keyboard", text)

    def test_12_environment_no_mutation(self):
        env = load(FINAL / "environment-version-receipt.json")
        self.assertTrue(env["verified_only"])
        for key in ["desktop_update_performed", "elevation", "host_security_changed", "windows_feature_changed", "sandbox_or_hyper_v_activated", "reboot"]:
            self.assertFalse(env[key])

    def test_13_wellbeing_and_identity_boundary(self):
        wellbeing = load(FINAL / "wellbeing-closeout.json")
        self.assertTrue(wellbeing["corrigibility_preserved"])
        self.assertFalse(wellbeing["identity_coercion"])
        self.assertFalse(wellbeing["consciousness_or_personhood_claim"])

    def test_14_x1_manifest_replay(self):
        self.assertEqual(replay_manifest(X1_COMMIT, "docs/caelen-ash/v684-v6/validation/x1-index-manifest.json"), 77)

    def test_15_evidence_manifest_replay(self):
        self.assertEqual(replay_manifest(EVIDENCE_COMMIT, "docs/caelen-ash/v684-v6/validation/evidence-index-manifest.json"), 201)

    def test_16_final_delta_manifest_working(self):
        manifest = load(VALIDATION / "final-delta-manifest.json")
        self.assertGreaterEqual(manifest["entry_count"], 8)
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_17_final_owner_manifest_working(self):
        manifest = load(VALIDATION / "final-owner-manifest.json")
        self.assertLess(manifest["owner_file_count"], 2000)
        self.assertEqual(manifest["owner_file_count"], manifest["entry_count"] + len(manifest["self_exclusions"]))
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"])

    def test_18_privacy_scan_zero_confirmed(self):
        scan = load(VALIDATION / "final-privacy-scan.json")
        self.assertEqual(len(scan["pattern_classes"]), 5)
        self.assertEqual(scan["confirmed_hit_count"], 0)

    def test_19_all_phase_json_parses(self):
        paths = list(BASE.rglob("*.json"))
        self.assertGreater(len(paths), 200)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_20_document_caps(self):
        for path in BASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000)

    def test_21_staged_review_shape(self):
        review = load(VALIDATION / "final-staged-review.json")
        self.assertIn(review["state"], {"PREPARED_NOT_STAGED", "PASS"})
        if review["state"] == "PASS":
            self.assertEqual(review["manifest_mismatches"], [])
            self.assertEqual(review["missing_paths"], [])
            self.assertEqual(review["out_of_scope_paths"], [])
            self.assertEqual(review["inherited_paths_changed"], [])

    def test_22_no_x1_or_x2_drift(self):
        changed = git(
            "diff", "--name-only", EVIDENCE_COMMIT, "--",
            "docs/caelen-ash/v684-v6/x1", "docs/caelen-ash/v684-v6/x2",
            "docs/caelen-ash/v684-v6/method-flow", "docs/caelen-ash/v684-v6/workflow-refinement",
            "docs/caelen-ash/v684-v6/reflection-remaster", "docs/caelen-ash/v684-v6/tooling",
        )
        self.assertEqual(changed, "")

    def test_23_final_validation_candidate(self):
        candidate = load(CLOSEOUT / "final-validation-candidate.json")
        self.assertEqual(candidate["canonical_invocation_budget"], 1)
        self.assertEqual(candidate["required_parent"], PREVIOUS_FINAL)
        self.assertEqual(candidate["required_phase_commits"], 3)
        self.assertFalse(candidate["replay_after_success"])
        self.assertFalse(candidate["full_repository_suite"])

    def test_24_claim_boundary(self):
        boundary = load(FINAL / "claim-boundary-matrix.json")
        self.assertGreaterEqual(len(boundary["not_established"]), 9)

    def test_25_only_four_labels(self):
        ledger = load(FINAL / "source-and-proposal-ledger.json")
        self.assertEqual(set(ledger["allowed_labels"]), {"completed", "represented", "open_gap", "exact_gate"})


if __name__ == "__main__":
    unittest.main()
