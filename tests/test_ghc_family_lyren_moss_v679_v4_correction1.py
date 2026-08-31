#!/usr/bin/env python3
"""Dependency-correction tests for Lyren Moss v679-v4."""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_lyren_moss_v679_v4_canonical import replay_manifest  # noqa: E402


PHASE = ROOT / "docs" / "lyren-moss" / "v679-v4"
FINAL = PHASE / "final"
CORRECTION = PHASE / "correction1"
VALIDATION = PHASE / "validation"
INITIAL_FINAL = "20923e75fe7490f43ed585ee97dca596b9ca7adc"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class CorrectionTests(unittest.TestCase):
    def test_preflight_failure_has_zero_canonical_credit(self) -> None:
        value = read(CORRECTION / "preflight-failure.json")
        self.assertEqual(value["classification"], "FAILED_NONCANONICAL_PREFLIGHT_ZERO_CANONICAL_CREDIT")
        self.assertEqual(value["canonical_invocations"], 0)
        self.assertEqual(value["canonical_success_credit"], 0)
        self.assertFalse(value["canonical_latch_created"])
        self.assertTrue(value["failure_retained"])

    def test_corrected_lifecycle_is_additive(self) -> None:
        value = read(CORRECTION / "lifecycle.json")
        self.assertEqual(value["retained_initial_final"], INITIAL_FINAL)
        self.assertEqual(value["prospective_corrected_final_parent"], INITIAL_FINAL)
        self.assertEqual(value["source_to_corrected_final_commit_target"], 4)
        self.assertEqual(value["merge_target"], 0)
        self.assertTrue(value["initial_final_remains_ancestral_and_immutable"])

    def test_corrected_terminal_adds_one_retained_failure(self) -> None:
        original = read(FINAL / "terminal-truth.json")
        corrected = read(CORRECTION / "terminal-overlay.json")
        for key in ("operational_failures_retained", "effective_negatives", "method_flow_methods", "failed_witnesses", "bounded_passing_witnesses"):
            with self.subTest(key=key):
                self.assertEqual(corrected[key], original[key] + 2)
        self.assertEqual(corrected["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_x1_historical_manifest_aliases_replay(self) -> None:
        manifest = read(VALIDATION / "x1-manifest.json")
        self.assertEqual(manifest["entry_count"], 20)
        self.assertEqual(replay_manifest(INITIAL_FINAL, manifest["entries"]), [])

    def test_corrected_handoff_is_content_addressed_and_unsent(self) -> None:
        metadata = read(CORRECTION / "activation-candidate-metadata.json")
        data = normalize((ROOT / metadata["path"]).read_bytes())
        self.assertEqual(hashlib.sha256(data).hexdigest(), metadata["normalized_lf_sha256"])
        self.assertEqual(len(data), metadata["normalized_lf_bytes"])
        self.assertGreater(metadata["words"], 2100)
        self.assertTrue(metadata["prepared_not_sent"])
        self.assertFalse(metadata["sent_by_lyren_moss"])

    def test_corrected_route_remains_held(self) -> None:
        value = read(CORRECTION / "route-overlay.json")
        self.assertEqual(value["prospective_successor"], "Ilyra Fen")
        self.assertEqual(value["prospective_successor_phase"], "v679-v5")
        self.assertEqual(value["route_state"], "PREPARED_NOT_SENT")
        self.assertFalse(value["precontact"])
        self.assertEqual(value["send_count"], 0)

    def test_corrected_manifest_and_seal_shapes(self) -> None:
        manifest = read(VALIDATION / "corrected-final-manifest.json")
        seal = read(VALIDATION / "corrected-content-seal.json")
        self.assertGreaterEqual(manifest["entry_count"], 11)
        self.assertEqual(seal["entry_count"], 10)
        self.assertEqual(seal["route_state"], "PREPARED_NOT_SENT")

    def test_every_correction_json_parses(self) -> None:
        paths = list(CORRECTION.rglob("*.json")) + [
            VALIDATION / "correction1-build-receipt.json",
            VALIDATION / "corrected-final-manifest.json",
            VALIDATION / "corrected-content-seal.json",
        ]
        self.assertGreaterEqual(len(paths), 9)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                json.loads(path.read_text(encoding="utf-8"))

    def test_no_self_referential_stale_label(self) -> None:
        for path in [item for item in CORRECTION.rglob("*") if item.is_file()] + [Path(__file__), ROOT / "scripts" / "ghc_family_lyren_moss_v679_v4_canonical.py"]:
            if path.suffix.lower() not in {".json", ".md", ".py"}:
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("Vesper " + "Rowan", text)
            self.assertNotIn("Rowan " + "Vesper", text)


if __name__ == "__main__":
    unittest.main()
