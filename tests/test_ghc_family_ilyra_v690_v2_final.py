"""Final artifact tests for Ilyra Fen v690-v2."""

from __future__ import annotations

import hashlib
import json
import re
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v690-v2"
FINAL = BASE / "final"


def load(name: str):
    return json.loads((FINAL / name).read_text(encoding="utf-8"))


class IlyraV690V2FinalTests(unittest.TestCase):
    def test_exact_lifecycle_anchors(self):
        lifecycle = load("lifecycle.json")
        self.assertEqual(lifecycle["planning"], "8c4eef447c296e4d956c75ff16e6205bf842df0b")
        self.assertEqual(lifecycle["x1"], "8e2a010330d4e31486dd3059ed1be9e2e744f9c1")
        self.assertEqual(lifecycle["x2"], "e85f3a2cfe5260ff2b9d6e953a80513d383650c5")
        self.assertEqual(lifecycle["expected_parent_of_final"], lifecycle["x2"])
        self.assertFalse(lifecycle["source_is_ancestor"])
        self.assertTrue(lifecycle["strict_x1_before_x2"])

    def test_exact_outcome_and_completion_counts(self):
        ledger = load("completion-ledger.json")
        self.assertEqual(
            ledger["core_outcomes"],
            {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5},
        )
        self.assertEqual(ledger["inherited_zero_credit"], 200)
        self.assertEqual(ledger["new_proposals"], 200)
        self.assertEqual(ledger["local_skills"], 20)
        self.assertEqual(ledger["local_runners"], 10)

    def test_terminal_accounting_is_additive(self):
        accounting = load("terminal-accounting.json")
        self.assertEqual(
            accounting["effective_total"],
            {
                "effective_negatives": 1268,
                "methods": 105,
                "direct_witnesses": 3507,
                "failed_witnesses": 979,
                "passing_witnesses": 2528,
            },
        )
        self.assertEqual(accounting["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_baton_modules_hash_range_and_eof(self):
        manifest = load("baton-manifest.json")
        self.assertEqual(manifest["module_count"], 13)
        self.assertTrue(manifest["range"]["in_range"])
        baton = (FINAL / "hand-off-baton.md").read_bytes()
        self.assertEqual(len(baton), manifest["combined"]["bytes"])
        self.assertEqual(hashlib.sha256(baton).hexdigest(), manifest["combined"]["sha256"])
        self.assertEqual(
            len(re.findall(r"\b[\w'-]+\b", baton.decode("utf-8"), flags=re.UNICODE)),
            manifest["combined"]["words"],
        )
        self.assertEqual(baton.decode("utf-8").splitlines()[-1], "EOF ILYRA FEN v690-v2 BATON.")
        for row in manifest["modules"]:
            data = (ROOT / row["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])

    def test_documents_are_openable_and_rendered(self):
        docx = FINAL / "overview.docx"
        self.assertTrue(zipfile.is_zipfile(docx))
        with zipfile.ZipFile(docx) as archive:
            self.assertIn("word/document.xml", archive.namelist())
        review = load("visual-review.json")
        self.assertGreaterEqual(review["pages"], 3)
        self.assertEqual(review["pages"], len(review["pages_inspected"]))
        self.assertFalse(review["clipping"])
        self.assertFalse(review["overlap"])
        self.assertTrue((FINAL / "rendered" / "overview.pdf").is_file())
        for page in review["pages_inspected"]:
            self.assertTrue((FINAL / "rendered" / f"page-{page}.png").is_file())

    def test_route_remains_prepared_not_sent(self):
        route = load("route-candidate.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["to_exact_title"], "Mira Fenwick")
        self.assertEqual(route["to_phase"], "v690-v3")
        self.assertFalse(route["precontacted"])
        self.assertIsNone(route["native_acknowledgement"])

    def test_deck_and_promotions(self):
        deck = json.loads((BASE / "x2" / "deck" / "deck-index.json").read_text(encoding="utf-8"))
        promotion = json.loads(
            (BASE / "x2" / "tooling" / "global-promotion.json").read_text(encoding="utf-8")
        )
        self.assertEqual(deck["card_count"], 213)
        self.assertEqual(promotion["skills"], 5)
        self.assertEqual(promotion["runners"], 5)
        self.assertTrue(promotion["no_overwrite"])

    def test_content_seal_and_final_manifest(self):
        seal = load("content-seal.json")
        manifest = load("manifest.json")
        self.assertEqual(seal["entry_count"], len(seal["entries"]))
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for payload in (seal, manifest):
            for row in payload["entries"]:
                data = (ROOT / row["path"]).read_bytes()
                self.assertEqual(len(data), row["bytes"], row["path"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])


if __name__ == "__main__":
    unittest.main()
