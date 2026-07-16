from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_v646_v7_definitions as d  # noqa: E402

PHASE = ROOT / "docs/eiren-kestrel/v646-v7"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V646V7CloseoutTests(unittest.TestCase):
    def test_closeout_anchors_and_counts(self):
        receipt = load("closeout-receipt.json")
        self.assertEqual(receipt["source_revision"], "327d0b8b6fca08d371d4dedd03e74a0bb7608c80")
        self.assertEqual(receipt["x1_revision"], "4604a34c48ba73f7d01f77e5a0bbf91a84145303")
        self.assertEqual(receipt["evidence_revision"], "0ebc21bb089929a2d854ad6010174b82c6c00447")
        self.assertEqual(receipt["core_distribution"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(receipt["effective_negatives"], 2977 + len(d.X1_OPERATIONAL_NEGATIVES) + 70 + len(d.X2_OPERATIONAL_NEGATIVES))

    def test_full_suite_exact_exclusions_only(self):
        full = load("validation/full-suite-validation.json")
        exclusions = full["tests"]["exact_inherited_exclusions"]
        self.assertGreaterEqual(full["tests"]["tests_run"], 1161)
        self.assertEqual(full["tests"]["eligible_tests"], full["tests"]["tests_run"] - len(exclusions))
        self.assertEqual(len(exclusions), 2)
        self.assertEqual(full["tests"]["unexpected_failure_events"], [])
        self.assertEqual(full["result"], "pass")

    def test_protocol_does_not_preclaim_post_commit_validation(self):
        final = load("final-validation-record.json")
        receipt = load("final-receipt.json")
        self.assertEqual(final["exact_final_head_validation"], "required_after_commit")
        self.assertEqual(final["named_local_only_replay"], "required_after_commit")
        self.assertFalse(receipt["exact_head_resolved"])
        self.assertFalse(receipt["baton_sent"])

    def test_route_remains_held_and_unsent(self):
        gate = load("orchestration/final-route-gate.json")
        route = load("orchestration/terminal-route-plan.json")
        self.assertEqual(gate["state"], "HOLD_FOR_EXACT_FINAL_AND_NAMED_REPLAY")
        self.assertEqual((gate["target_title"], gate["send_count"], gate["task_creation"], gate["delegation"]), ("Ilyra Fen", 0, 0, 0))
        self.assertEqual((route["current_state"], route["send_count"]), ("HOLD_FOR_EXACT_FINAL_AND_NAMED_REPLAY", 0))

    def test_seal_is_single_parent_contract(self):
        seal = load("seal-receipt.json")
        self.assertTrue(seal["source_to_evidence_zero_merges"])
        self.assertTrue(seal["x1_parent_is_source"])
        self.assertTrue(seal["evidence_parent_is_x1"])
        self.assertEqual(seal["maximum_phase_commits"], 4)
        self.assertIn(seal["expected_phase_commits_after_final"], {3, 4})
        self.assertFalse(seal["history_rewrite"])
        self.assertFalse(seal["force_push"])

    def test_owner_manifest_working_bytes(self):
        manifest = load("validation/final-owner-manifest.json")
        self.assertGreaterEqual(manifest["entry_count"], 150)
        for entry in manifest["entries"]:
            if manifest["hash_domain"] == "git_index_blob":
                raw = subprocess.check_output(["git", "show", f":{entry['path']}"], cwd=ROOT)
            else:
                raw = (ROOT / entry["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])

    def test_method_flow_and_stage20_boundary(self):
        method = load("method-flow/final-method-flow-state.json")
        truth = load("phase-truth.json")
        self.assertEqual(method["counts"]["methods"], len(d.X1_OPERATIONAL_NEGATIVES) + len(d.X2_OPERATIONAL_NEGATIVES))
        self.assertEqual(method["counts"]["witness_results"]["fail"], method["counts"]["witness_results"]["pass"])
        self.assertGreaterEqual(method["counts"]["witness_results"]["fail"], method["counts"]["methods"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])


if __name__ == "__main__":
    unittest.main()
