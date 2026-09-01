#!/usr/bin/env python3
"""Precommit and exact-final tests for Orin Thale v681-v8."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v681-v8"
FINAL = PHASE / "final"
VALIDATION = PHASE / "validation"
SOURCE = "7327e6cb3972e93a4d6a27e45ad2ba3445a4d6ce"
X1 = "705429c7b30d6b25065cd9e758024eed3474c70d"
EVIDENCE = "16eaac80d15f7927b012c97384d91d17b32a555e"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class OrinThaleV681V8FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.truth = load(FINAL / "phase-truth.json")
        cls.method = load(FINAL / "method-flow-ledger.json")
        cls.source = load(FINAL / "source-and-proposal-ledger.json")
        cls.delta = load(VALIDATION / "final-delta-manifest.json")
        cls.owner = load(VALIDATION / "final-owner-manifest.json")
        cls.staged = load(VALIDATION / "final-staged-review.json")

    def test_precommit_lifecycle(self):
        self.assertEqual(git("rev-parse", "HEAD"), EVIDENCE)

    def test_source_x1_evidence_direct_ancestry(self):
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)

    def test_exact_outcomes(self):
        self.assertEqual(self.truth["outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(set(self.truth["outcomes"]), LABELS)

    def test_declared_proposal_chain(self):
        self.assertEqual(self.source["declared_chain_before"], 10130)
        self.assertEqual(self.source["declared_chain_after"], 10190)
        self.assertEqual(self.source["new_proposal_count"], 60)

    def test_effective_counts(self):
        self.assertEqual(
            self.truth["counts"],
            {
                "effective_negatives": 55171,
                "effective_methods": 64373,
                "failed_witnesses": 26832,
                "bounded_passing_witnesses": 45895,
                "open_gaps": 488,
                "exact_gates": 479,
            },
        )

    def test_failures_not_erased_or_promoted(self):
        negative = load(FINAL / "retained-negative-register.json")
        self.assertEqual(negative["erased_or_promoted"], 0)
        self.assertEqual(negative["startup_failures"], 16)
        self.assertEqual(negative["preregistered_rejected_mutations"], 300)
        self.assertEqual(negative["new_x2_operational_failures"], 3)
        self.assertEqual(negative["new_closeout_failures"], 4)
        self.assertEqual(len(negative["closeout_failures"]), 4)
        self.assertEqual(len(self.method["closeout_failures"]), 4)
        self.assertFalse(self.method["failure_erasure"])

    def test_gap_and_gate_registers(self):
        gaps = load(FINAL / "open-gap-register.json")
        gates = load(FINAL / "exact-gate-register.json")
        self.assertEqual(gaps["effective"], 488)
        self.assertEqual(gates["effective"], 479)
        self.assertEqual(gaps["closed_by_software"], 0)
        self.assertEqual(gates["closed_by_software"], 0)

    def test_evidence_receipt(self):
        receipt = load(FINAL / "evidence-receipt.json")
        self.assertEqual(receipt["positive_controls"], 60)
        self.assertEqual(receipt["mutations_executed"], 300)
        self.assertEqual(receipt["mutations_rejected"], 300)
        self.assertEqual(receipt["skills_used"], 20)
        self.assertEqual(receipt["runners_used"], 10)
        self.assertFalse(receipt["independent_reproduction"])

    def test_complete_incomplete_boundaries(self):
        checklist = load(FINAL / "complete-incomplete-checklist.json")
        self.assertEqual(checklist["unexecuted"], {"exact_approval": 20, "blocked": 10})
        self.assertGreater(len(checklist["incomplete_external"]), 5)

    def test_handoff_word_bounds(self):
        path = FINAL / "liora-venn-v682-v1-activation-candidate.md"
        words = len(path.read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)

    def test_handoff_is_prepared_not_sent(self):
        text = (FINAL / "liora-venn-v682-v1-activation-candidate.md").read_text(encoding="utf-8")
        self.assertIn("PREPARED_BY_ORIN_THALE = true", text)
        self.assertIn("SENT_BY_ORIN_THALE = false", text)
        route = load(FINAL / "route-plan.json")
        self.assertEqual(route["route_state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["precontacted"])
        self.assertEqual(route["send_count"], 0)

    def test_content_seal(self):
        seal = load(FINAL / "content-seal.json")
        self.assertEqual(seal["target_count"], len(seal["targets"]))
        for entry in seal["targets"]:
            data = normalized(ROOT / entry["path"])
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_final_delta_manifest(self):
        actual = set(self.delta["declared_self_exclusions"])
        for entry in self.delta["entries"]:
            data = normalized(ROOT / entry["path"])
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])
            actual.add(entry["path"])
        self.assertEqual(actual, set(self.staged["expected_paths"]))
        self.assertEqual(len(actual), self.staged["expected_path_count"])

    def test_final_owner_manifest(self):
        exclusions = set(self.owner["declared_self_exclusions"])
        actual = exclusions | {entry["path"] for entry in self.owner["entries"]}
        self.assertEqual(len(actual), self.owner["owner_path_count"])
        self.assertEqual(len(self.owner["entries"]), self.owner["entry_count"])
        for entry in self.owner["entries"]:
            data = normalized(ROOT / entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_privacy_scan(self):
        scan = load(VALIDATION / "final-privacy-scan.json")
        self.assertEqual(scan["confirmed_hit_count"], 0)
        self.assertEqual(scan["confirmed_hits"], [])
        self.assertEqual(len(scan["privacy_classes"]), 5)

    def test_security_scan(self):
        scan = load(VALIDATION / "final-security-scan.json")
        self.assertEqual(scan["finding_count"], 0)
        self.assertEqual(scan["findings"], [])
        self.assertFalse(scan["exhaustive_security_claimed"])

    def test_all_phase_json_parse(self):
        paths = list(PHASE.rglob("*.json"))
        self.assertGreater(len(paths), 50)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_document_word_ceiling_and_hygiene(self):
        for path in list(PHASE.rglob("*.md")) + list(PHASE.rglob("*.html")):
            text = path.read_text(encoding="utf-8")
            self.assertLessEqual(len(text.split()), 100000, str(path))
            self.assertFalse(any(line.endswith((" ", "\t")) for line in text.splitlines()), str(path))

    def test_owner_file_ceiling(self):
        self.assertLess(self.owner["owner_path_count"], 2000)

    def test_terminal_verdict_and_validation_state(self):
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        candidate = load(FINAL / "final-validation-candidate.json")
        self.assertEqual(candidate["canonical_state"], "PENDING_NOT_INVOKED")
        self.assertFalse(candidate["complete_repository_suite"])


if __name__ == "__main__":
    unittest.main()
