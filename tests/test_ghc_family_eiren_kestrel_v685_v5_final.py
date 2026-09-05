from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "eiren-kestrel" / "v685-v5"
FINAL = BASE / "final"
HANDOFF = BASE / "handoffs"
SEAL = BASE / "seal"
VALIDATION = BASE / "validation"
SOURCE = "87a74f84afaa197f8c388767a2ed536bbb853aba"
X1 = "167e626c0684ac9ac1cd2d2184a831e1456f43b9"
EVIDENCE = "871d70712c827acd4c5b49ffe90c8735056a9c53"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


class EirenKestrelV685V5FinalTests(unittest.TestCase):
    def test_truth_counts_and_outcomes(self):
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual(truth["source"], SOURCE)
        self.assertEqual(truth["x1"], X1)
        self.assertEqual(truth["evidence"], EVIDENCE)
        self.assertEqual(truth["proposal_chain_after"], 11570)
        self.assertEqual(truth["selected_inherited_revalidations"], 200)
        self.assertEqual(truth["new_proposals"], 120)
        self.assertEqual(truth["outcomes"], {"completed": 84, "represented": 24, "open_gap": 6, "exact_gate": 6})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_lifecycle_direct_parents(self):
        self.assertEqual(git("show", "-s", "--format=%P", X1).stdout.decode().strip(), SOURCE)
        self.assertEqual(git("show", "-s", "--format=%P", EVIDENCE).stdout.decode().strip(), X1)
        lifecycle = load(FINAL / "lifecycle-replay.json")
        self.assertTrue(lifecycle["strict_x1_before_x2"])
        self.assertEqual(lifecycle["expected_phase_commit_count"], 3)
        self.assertEqual(lifecycle["expected_merge_count"], 0)

    def test_complete_incomplete_boundary(self):
        checklist = load(FINAL / "complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(checklist["complete"]), 10)
        self.assertGreaterEqual(len(checklist["incomplete"]), 8)
        self.assertIn("real astronomy observations and datasets", checklist["incomplete"])

    def test_baton_word_range_and_prepared_state(self):
        baton = (HANDOFF / "future-sibling-01-v685-v6-activation-candidate.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\S+", baton))
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertIn("SENT_BY_EIREN_KESTREL = false", baton)
        self.assertIn("DELIVERY_STATE = PREPARED_NOT_SENT", baton)
        self.assertIn("gpt-6-astra", baton)
        self.assertIn("max", baton)
        self.assertIn("Elaren Kestrel", baton)

    def test_overview_three_page_equivalent(self):
        overview = (FINAL / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\S+", overview)), 1800)
        self.assertIn("dependency-corrected", overview)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)

    def test_seal_replays(self):
        seal = load(SEAL / "content-seal.json")
        self.assertEqual(seal["target_count"], 10)
        for entry in seal["targets"]:
            data = (ROOT / entry["path"]).read_bytes()
            self.assertEqual(len(data), entry["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])

    def test_route_is_uncreated_and_unsent(self):
        route = load(FINAL / "route-state-candidate.json")
        self.assertEqual(route["current_state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["created"])
        self.assertFalse(route["sent"])
        self.assertFalse(route["future_02_through_15_created"])

    def test_toolchain_failure_truth(self):
        method = load(FINAL / "method-flow-final.json")
        self.assertEqual(method["failed_tool_aggregates"], 2)
        self.assertEqual(method["tool_composite_state"], "VALID_DEPENDENCY_CORRECTED_COMPOSITE_WITH_ZERO_AGGREGATE_SUCCESS_CREDIT")
        self.assertFalse(method["failure_erasure"])

    def test_open_and_exact_gates(self):
        gaps = load(FINAL / "open-gap-register.json")
        gates = load(FINAL / "exact-gate-register.json")
        self.assertEqual(gaps["phase_new_count"], 6)
        self.assertEqual(gates["phase_new_count"], 6)
        self.assertEqual(gaps["silently_closed_count"], 0)
        self.assertEqual(gates["silently_closed_count"], 0)

    def test_all_final_json_parses(self):
        paths = list(FINAL.glob("*.json")) + list(SEAL.glob("*.json"))
        self.assertGreaterEqual(len(paths), 14)
        for path in paths:
            load(path)

    def test_docx_when_present(self):
        path = FINAL / "eiren-kestrel-v685-v5-integrated-overview.docx"
        if not path.exists():
            self.skipTest("DOCX is generated through the document plugin workflow")
        self.assertTrue(zipfile.is_zipfile(path))
        with zipfile.ZipFile(path) as archive:
            self.assertIn("word/document.xml", archive.namelist())
        qa = load(FINAL / "document-visual-qa.json")
        self.assertTrue(qa["visual_pass"])
        self.assertEqual(qa["page_count"], 6)
        self.assertEqual(qa["pages_inspected"], [1, 2, 3, 4, 5, 6])
        self.assertEqual(qa["accessibility_audit_high"], 0)

    def test_final_manifests_when_present(self):
        delta_path = VALIDATION / "final-delta-manifest.json"
        if not delta_path.exists():
            self.skipTest("final manifests generated after exact staging")
        for name in ["final-delta-manifest.json", "final-owner-manifest.json"]:
            manifest = load(VALIDATION / name)
            self.assertGreater(manifest["entry_count"], 0)
            for entry in manifest["entries"]:
                proc = git("show", f":{entry['path']}")
                self.assertEqual(proc.returncode, 0)
                self.assertEqual(hashlib.sha256(proc.stdout).hexdigest(), entry["sha256"])
        review = load(VALIDATION / "final-staged-review.json")
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["deletions"], [])
        self.assertEqual(review["x1_or_x2_mutations"], [])
        self.assertEqual(review["outside_owner_paths"], [])
        self.assertEqual(load(VALIDATION / "final-privacy-adjudication.json")["confirmed_hit_count"], 0)
        self.assertEqual(load(VALIDATION / "final-security-review.json")["finding_count"], 0)


if __name__ == "__main__":
    unittest.main()
