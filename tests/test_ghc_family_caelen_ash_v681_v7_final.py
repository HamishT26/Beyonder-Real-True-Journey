from __future__ import annotations
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v681-v7"
FINAL = PHASE / "final"
VALIDATION = PHASE / "validation"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def replay(manifest):
    for entry in manifest["entries"]:
        data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            return False
    return True


class CaelenAshV681V7FinalTests(unittest.TestCase):
    def test_01_phase_truth_is_exact(self):
        data = load(FINAL / "phase-truth.json")
        self.assertEqual(data["outcomes"], {"completed": 42, "exact_gate": 3, "open_gap": 3, "represented": 12})
        self.assertEqual(data["proposal_chain"], 10130)
        self.assertEqual(data["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_02_effective_counts_are_additive(self):
        data = load(FINAL / "method-flow-final.json")
        self.assertEqual(data["effective_counts"], {"bounded_passing_witnesses": 45182, "effective_methods": 63660, "effective_negatives": 54848, "exact_gates": 476, "failed_witnesses": 26509, "open_gaps": 485})
        self.assertFalse(data["failure_erasure"])

    def test_03_terminal_route_is_held(self):
        data = load(PHASE / "handoffs" / "terminal-route-hold.json")
        self.assertEqual(data["authorized_exact_title"], "Orin Thale")
        self.assertEqual(data["authorized_next_phase"], "v681-v8")
        self.assertFalse(data["sent"])
        self.assertTrue(data["canonical_success_required"])

    def test_04_baton_is_long_form_but_bounded(self):
        text = (PHASE / "handoffs" / "orin-thale-v681-v8-activation-candidate.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\S+", text))
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertIn("PREPARED_BY_CAELEN_ASH = true", text)
        self.assertIn("SENT_BY_CAELEN_ASH = false", text)

    def test_05_content_seal_replays(self):
        seal = load(PHASE / "closeout" / "content-seal.json")
        self.assertEqual(seal["entry_count"], 15)
        self.assertTrue(replay(seal))

    def test_06_final_delta_manifest_replays(self):
        self.assertTrue(replay(load(VALIDATION / "final-delta-manifest.json")))

    def test_07_final_owner_manifest_replays(self):
        manifest = load(VALIDATION / "final-owner-manifest.json")
        self.assertTrue(replay(manifest))
        self.assertLess(manifest["entry_count"] + len(manifest["declared_self_exclusions"]), 2000)

    def test_08_privacy_scan_has_zero_confirmed_hits(self):
        data = load(VALIDATION / "final-privacy-scan.json")
        self.assertEqual(data["confirmed_hits"], [])
        self.assertEqual(len(data["privacy_classes"]), 5)

    def test_09_canonical_is_only_prepared(self):
        data = load(FINAL / "final-validation-candidate.json")
        self.assertEqual(data["state"], "PREPARED_NOT_INVOKED")
        self.assertEqual(data["allowed_invocations"], 1)

    def test_10_exact_ancestry_anchors_are_preserved(self):
        data = load(PHASE / "closeout" / "closeout-receipt.json")
        self.assertEqual(data["source"], "4da1c50b22e1b30b5e7351b0641f350bdc8fbfbe")
        self.assertEqual(data["x1_head"], "f31bb3fb3738136db75dc264325f267dc4068f4a")
        self.assertEqual(data["evidence_head"], "ce01a79bd92c1c8de02df586075eadb0427cfed6")

    def test_11_wellbeing_and_workload_are_bounded(self):
        data = load(FINAL / "wellbeing-and-workload.json")
        self.assertTrue(data["pause_allowed"])
        self.assertTrue(data["caps_are_ceilings"])
        self.assertFalse(data["identity_or_consciousness_evidence"])

    def test_12_documents_remain_within_cap(self):
        for path in PHASE.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}:
                self.assertLessEqual(len(re.findall(r"\S+", path.read_text(encoding="utf-8"))), 100000, str(path))


if __name__ == "__main__":
    unittest.main()
