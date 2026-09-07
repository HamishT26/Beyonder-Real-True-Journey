#!/usr/bin/env python3
"""Additive root-runner correction tests for Orin v687-v7 x2."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v687-v7"
CORRECTION = PHASE / "x2" / "correction"
VALIDATION = PHASE / "validation"
X1 = "7aea73908f8f41ed38473d6e30e5f1bda36588a7"
FIRST_EVIDENCE = "a29be946caf963315a48f73055f0eb1cae85e482"
ROOT_FILES = ["scripts/ghc_family_spectral_archive_contract.py"] + [f"scripts/ghc_family_spectral_archive_{i:02d}_runner.py" for i in range(1, 6)]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def norm(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class OrinThaleV687V7X2CorrectionTests(unittest.TestCase):
    def test_precommit_parent_is_first_evidence(self):
        self.assertEqual(git("rev-parse", "HEAD"), FIRST_EVIDENCE)
        self.assertEqual(git("rev-parse", "HEAD^"), X1)

    def test_six_root_interfaces_exist(self):
        self.assertTrue(all((ROOT / path).is_file() for path in ROOT_FILES))

    def test_failure_retained_and_counts_advanced(self):
        correction = load(CORRECTION / "root-runner-omission.json")
        truth = load(CORRECTION / "phase-truth-overlay.json")
        self.assertEqual(correction["negative_id"], "OR6877-X2-N006")
        self.assertFalse(correction["original_manifest_rewritten"])
        self.assertEqual(truth["effective_counts"], {"negatives": 82021, "methods": 93194, "failed_witnesses": 52869, "passing_witnesses": 81995, "open_gaps": 732, "exact_gates": 711, "proposals": 15230})
        self.assertEqual(truth["outcomes"], {"completed": 125, "represented": 39, "open_gap": 20, "exact_gate": 16})

    def test_original_x2_manifest_unchanged_at_first_evidence(self):
        self.assertEqual(git("diff", "--name-only", FIRST_EVIDENCE, "--", "docs/orin-thale/v687-v7/validation/x2-manifest.json"), "")

    def test_correction_manifest(self):
        manifest = load(VALIDATION / "x2-correction-manifest.json")
        actual = set(manifest["declared_self_exclusions"])
        for entry in manifest["entries"]:
            data = norm(ROOT / entry["path"])
            self.assertEqual(len(data), entry["bytes_normalized_lf"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"], entry["path"])
            actual.add(entry["path"])
        staged = load(VALIDATION / "x2-correction-staged-review.json")
        self.assertEqual(actual, set(staged["expected_paths"]))

    def test_privacy_security_and_terminal_boundaries(self):
        self.assertEqual(load(VALIDATION / "x2-correction-privacy.json")["confirmed_count"], 0)
        self.assertEqual(load(VALIDATION / "x2-correction-security.json")["finding_count"], 0)
        truth = load(CORRECTION / "phase-truth-overlay.json")
        self.assertEqual(truth["canonical_state"], "NOT_INVOKED")
        self.assertEqual(truth["route_state"], "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
