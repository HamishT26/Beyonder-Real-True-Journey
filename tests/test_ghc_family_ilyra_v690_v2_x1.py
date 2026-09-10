"""X1 tests for Ilyra Fen v690-v2."""

from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from scripts.ghc_family_obligation_graph_x1 import run

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "ilyra-fen" / "v690-v2" / "plan"
X1 = ROOT / "docs" / "ilyra-fen" / "v690-v2" / "x1"


class IlyraV690V2X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        payload = json.loads((PLAN / "new-proposals.json").read_text(encoding="utf-8"))
        cls.rows = [row for row in payload["proposals"] if row["lane"] == "x1"]

    def test_exact_safe_envelopes(self):
        self.assertEqual(len(self.rows), 100)
        for row in self.rows:
            request = copy.deepcopy(row["request"])
            original = copy.deepcopy(request)
            self.assertEqual(run(request), row["expected"], row["proposal_id"])
            self.assertEqual(request, original, row["proposal_id"])

    def test_candidate_subjects_remain_failed(self):
        for row in self.rows:
            subject = copy.deepcopy(row["candidate_subject"])
            original = copy.deepcopy(subject)
            self.assertEqual(run(subject), row["candidate_expected"], row["proposal_id"])
            self.assertEqual(subject, original, row["proposal_id"])

    def test_boolean_case_identifier_is_refused(self):
        request = copy.deepcopy(self.rows[0]["request"])
        request["payload"]["case_id"] = True
        self.assertEqual(run(request)["error"], "invalid_case_id")

    def test_unknown_operation_is_refused(self):
        result = run({"operation": "route_message", "payload": {}})
        self.assertEqual(result, {"ok": False, "error": "unknown_operation", "original_success_credit": 0})

    def test_x2_is_absent_at_x1(self):
        self.assertFalse((ROOT / "scripts" / "ghc_family_obligation_graph_x2.py").exists())
        self.assertFalse((ROOT / "docs" / "ilyra-fen" / "v690-v2" / "x2").exists())

    def test_x1_evidence_counts(self):
        results = json.loads((X1 / "results.json").read_text(encoding="utf-8"))
        candidates = json.loads((X1 / "candidate-subjects.json").read_text(encoding="utf-8"))
        refinements = json.loads((X1 / "refinements.json").read_text(encoding="utf-8"))
        self.assertEqual(results["count"], 100)
        self.assertTrue(all(row["passed"] for row in results["records"]))
        self.assertEqual(candidates["count"], 100)
        self.assertTrue(all(row["subject_result"] == "fail" for row in candidates["records"]))
        self.assertEqual(refinements["count"], 100)
        self.assertTrue(all(row["lossless_equal"] for row in refinements["records"]))

    def test_retained_failure_and_method_accounting(self):
        flow = json.loads((X1 / "method-flow.json").read_text(encoding="utf-8"))
        negative = json.loads((X1 / "negative-index.json").read_text(encoding="utf-8"))
        self.assertEqual(flow["counts"]["methods"], 11)
        self.assertEqual(flow["counts"]["failed"], 140)
        self.assertEqual(flow["counts"]["passing"], 343)
        self.assertEqual(flow["counts"]["witnesses"], 483)
        self.assertEqual(negative["count"], 140)
        self.assertTrue(all(witness["independent_reproduction"] is False for witness in flow["witnesses"]))

    def test_toolchain_and_skills(self):
        install = json.loads((X1 / "toolchain" / "install-result.json").read_text(encoding="utf-8"))
        correction = json.loads((X1 / "toolchain" / "dependency-correction.json").read_text(encoding="utf-8"))
        skills = json.loads((X1 / "skills-validation.json").read_text(encoding="utf-8"))
        self.assertFalse(install["install_invoked_this_run"])
        self.assertEqual(correction["transitive"]["version"], "2.5.3")
        self.assertEqual(skills["count"], 10)
        self.assertTrue(all(row["official_quick_validate"] for row in skills["records"]))

    def test_x1_manifest_raw_worktree_bytes(self):
        manifest = json.loads((X1 / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            data = (ROOT / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])


if __name__ == "__main__":
    unittest.main()
