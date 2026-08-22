from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v666-v3"
X1_SHA = "e121ea6e207ea032edb1a0825ed86b1334481213"
EVIDENCE_SHA = "2ec494e75da11be4b8b18620f0ab10b68764ac69"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class LyrenV666V3CloseoutTests(unittest.TestCase):
    def test_phase_truth_exact(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual((truth["effective_negatives"], truth["effective_methods"]), (26395, 10937))
        self.assertEqual((truth["open_gaps"], truth["exact_gates"]), (185, 183))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["same_owner_validation_is_independent_reproduction"])

    def test_retained_failures_and_method_flow(self):
        negatives = load("closeout/retained-negative-register.json")
        flow = load("closeout/method-flow-final.json")
        self.assertEqual(negatives["retained_owner_row_count"], 113)
        self.assertTrue(negatives["every_failed_witness_zero_broader_credit"])
        self.assertTrue(negatives["no_failure_erased"])
        self.assertEqual(flow["effective_methods"], 10937)
        self.assertEqual(flow["failed_owner_witnesses"], 113)

    def test_exact_replacement_evidence_tree_has_no_terminal_paths(self):
        for name in ("closeout", "seal", "final", "handoffs"):
            rows = subprocess.check_output(
                ["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", EVIDENCE_SHA, "--", f"docs/lyren-moss/v666-v3/{name}"],
                text=True,
            ).strip()
            self.assertEqual(rows, "", name)

    def test_route_is_prepared_not_sent(self):
        route = load("orchestration/route-state-final-candidate.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual((route["next_exact_title"], route["next_phase"]), ("Ilyra Fen", "v666-v4"))
        self.assertEqual(route["send_count"], 0)
        self.assertEqual(route["resend_count"], 0)
        self.assertFalse(route["successor_contacted"])
        self.assertFalse(route["replacement_task_created"])

    def test_activation_baton_sanitized_and_unsent(self):
        text = (PHASE / "handoffs" / "ilyra-fen-v666-v4-activation-prepared.md").read_text(encoding="utf-8")
        self.assertIn("SENT_BY_LYREN_MOSS = false", text)
        self.assertIn("Ilyra Fen", text)
        self.assertIn("Auren Lark", text)
        self.assertNotRegex(text, r"(?i)(?:source_)?(?:task|thread)[_-]?id\s*[:=]")
        self.assertNotRegex(text, r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)")

    def test_final_staged_review_and_manifests(self):
        review = load("validation/final-staged-review.json")
        delta = load("validation/final-delta-manifest.json")
        owner = load("validation/final-owner-manifest.json")
        self.assertTrue(review["valid"])
        self.assertTrue(all(review["checks"].values()))
        self.assertTrue(delta["non_destructive_correction"])
        self.assertGreater(delta["entry_count"], 15)
        self.assertGreater(owner["entry_count"], 140)
        self.assertTrue(owner["guard_passed"])
        for manifest in (delta, owner):
            for entry in manifest["entries"]:
                blob = subprocess.check_output(["git", "-C", str(ROOT), "show", f":{entry['path']}"])
                self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])
                self.assertEqual(len(blob), entry["size_bytes"])

    def test_immutable_manifests_replay(self):
        for manifest_name, commit in (("x1-content-manifest.json", X1_SHA), ("evidence-content-manifest.json", EVIDENCE_SHA)):
            manifest = load(f"validation/{manifest_name}")
            for entry in manifest["entries"]:
                blob = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{commit}:{entry['path']}"])
                self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])

    def test_canonical_plan_not_invoked(self):
        prerequisites = load("final/final-validation-prerequisites.json")
        plan = load("final/canonical-completion-plan.json")
        self.assertFalse(prerequisites["canonical_invoked"])
        self.assertFalse(prerequisites["successor_contacted"])
        self.assertEqual(plan["invocation_limit"], 1)
        self.assertFalse(plan["post_success_replay_permitted"])
        self.assertEqual(len(plan["zero_credit_lifecycle_exclusions"]), 2)
        self.assertEqual(len(plan["exact_replacements"]), 2)

    def test_closeout_runner_passes(self):
        completed = subprocess.run(["python", str(ROOT / "scripts" / "ghc_family_lyren_moss_v666_v3_closeout.py")], cwd=ROOT, text=True, encoding="utf-8", errors="strict", capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["valid"])


if __name__ == "__main__":
    unittest.main()
