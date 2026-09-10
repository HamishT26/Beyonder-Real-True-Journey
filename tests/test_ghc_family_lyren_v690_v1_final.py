from __future__ import annotations

import hashlib
import json
import re
import unittest
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/lyren-moss/v690-v1"
FINAL = BASE / "final"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


class LyrenV690V1FinalTests(unittest.TestCase):
    def test_lifecycle_anchors_and_commit_ceiling(self):
        record = load(FINAL / "lifecycle.json")
        self.assertEqual(record["planning"], "cd9baca94099be83f5b9a8ae5367e2f63a272614")
        self.assertEqual(record["x1"], "13048b82fb42c27ff287bf6793c9b52d67a49f96")
        self.assertEqual(record["x2"], "b716b6694110e4b60154d8d91de1bfdf5b2b7ab1")
        self.assertEqual(record["commit_count_target"], 4)
        self.assertLessEqual(record["commit_count_target"], record["commit_ceiling"])
        self.assertTrue(record["strict_x1_before_x2"])
        self.assertFalse(record["source_is_ancestor"])

    def test_core_and_supplementary_outcomes(self):
        ledger = load(FINAL / "completion-ledger.json")
        self.assertEqual(ledger["core_outcomes"], {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5})
        self.assertEqual(ledger["supplementary_outcomes"], {"represented": 5})
        self.assertEqual(set(ledger["core_outcomes"]), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertEqual(ledger["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_portfolios_packets_and_tools(self):
        ledger = load(FINAL / "completion-ledger.json")
        self.assertEqual(ledger["proposals"], {"inherited_zero_credit": 200, "new": 200})
        self.assertEqual(ledger["tasks"], {"safe_x1": 100, "candidate_x1": 100, "clean_fix_refine_x1": 100, "safe_x2": 100, "candidate_x2": 100, "clean_fix_refine_x2": 100})
        self.assertEqual(ledger["packets"], {"exact": 50, "blocked": 30, "protected_actions_executed": 0})
        self.assertEqual(ledger["skills"], {"local": 20, "merged_global_installed": 5})
        self.assertEqual(ledger["runners"], {"paired_local": 10, "public_global_installed": 5, "dependency_modules_zero_runner_credit": 2})
        self.assertEqual(ledger["packages"], {"direct": 3, "transitive": 2})

    def test_terminal_accounting_arithmetic(self):
        accounting = load(FINAL / "terminal-accounting.json")
        totals = {}
        for field in ["effective_negatives", "methods", "direct_witnesses", "failed_witnesses", "passing_witnesses"]:
            totals[field] = sum(row[field] for row in accounting["layers"])
        self.assertEqual(totals, accounting["effective_total"])
        self.assertEqual(totals, {"effective_negatives": 973, "methods": 81, "direct_witnesses": 2479, "failed_witnesses": 684, "passing_witnesses": 1795})
        self.assertEqual(totals["failed_witnesses"] + totals["passing_witnesses"], totals["direct_witnesses"])
        self.assertEqual(accounting["successor_visible_after_late_overlay"], {"effective_negatives": 977, "methods": 82, "direct_witnesses": 2487, "failed_witnesses": 688, "passing_witnesses": 1799})

    def test_final_failures_are_retained_zero_credit(self):
        overlay = load(FINAL / "operational-overlay.json")
        self.assertEqual(overlay["counts"], {"retained_negatives": 6, "methods": 1, "witnesses": 12, "failed_witnesses": 6, "passing_witnesses": 6})
        self.assertTrue(all(row["retained"] and row["original_success_credit"] == 0 for row in overlay["retained_negatives"]))
        self.assertEqual(Counter(row["result"] for row in overlay["witnesses"]), {"fail": 6, "pass": 6})

    def test_late_validation_overlay_is_additive(self):
        overlay = load(FINAL / "late-validation-overlay.json")
        self.assertEqual(len(overlay["retained_negatives"]), 4)
        self.assertTrue(all(row["original_success_credit"] == 0 for row in overlay["retained_negatives"]))
        self.assertEqual(Counter(row["result"] for row in overlay["witnesses"]), {"fail": 4, "pass": 4})
        self.assertEqual(overlay["successor_visible_accounting"], {"effective_negatives": 977, "methods": 82, "direct_witnesses": 2487, "failed_witnesses": 688, "passing_witnesses": 1799})

    def test_baton_is_modular_in_range_and_ends_at_eof(self):
        manifest = load(FINAL / "baton-manifest.json")
        baton = (FINAL / "hand-off-baton.md").read_text(encoding="utf-8")
        self.assertEqual(manifest["module_count"], 13)
        self.assertEqual(manifest["combined"]["words"], words(baton))
        self.assertGreaterEqual(words(baton), 10_000)
        self.assertLessEqual(words(baton), 100_000)
        self.assertEqual(baton.rstrip().splitlines()[-1], "EOF LYREN MOSS v690-v1 BATON.")
        self.assertEqual(hashlib.sha256((FINAL / "hand-off-baton.md").read_bytes()).hexdigest(), manifest["combined"]["sha256"])
        for row in manifest["modules"]:
            path = ROOT / row["path"]
            self.assertEqual(path.stat().st_size, row["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row["sha256"])

    def test_route_is_prepared_not_sent(self):
        route = load(FINAL / "route-candidate.json")
        self.assertEqual(route["from"], "Lyren Moss")
        self.assertEqual(route["to_exact_title"], "Ilyra Fen")
        self.assertEqual(route["to_phase"], "v690-v2")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["precontacted"])
        self.assertIsNone(route["native_acknowledgement"])
        self.assertFalse(route["replacement_creation_authorized"])
        self.assertEqual(route["transient_service_recovery_attempts_required"], 5)

    def test_document_build_and_visual_review(self):
        build = load(FINAL / "document-build.json")
        visual = load(FINAL / "visual-review.json")
        self.assertEqual(build["operation_marker"], "invoked_once_before_docx_authoring")
        self.assertEqual(build["render_state"], "VALIDATED_WITH_RETAINED_FAILURES")
        self.assertEqual(build["canonical_render"]["pdf"]["pages"], 5)
        self.assertGreaterEqual(build["canonical_render"]["pdf"]["pages"], build["minimum_pages"])
        self.assertEqual(visual["pages_inspected"], [1, 2, 3, 4, 5])
        self.assertTrue(visual["result"] == "pass" and not visual["clipping"] and not visual["overlap"])
        self.assertFalse(visual["complete_accessibility_claimed"])
        pdf = ROOT / build["canonical_render"]["pdf"]["path"]
        self.assertTrue(pdf.read_bytes().startswith(b"%PDF-"))
        self.assertEqual(hashlib.sha256(pdf.read_bytes()).hexdigest(), build["canonical_render"]["pdf"]["sha256"])

    def test_docx_is_valid_ooxml_package(self):
        path = FINAL / "overview.docx"
        self.assertTrue(zipfile.is_zipfile(path))
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            self.assertIn("word/document.xml", names)
            self.assertIn("[Content_Types].xml", names)
            document_xml = archive.read("word/document.xml").decode("utf-8")
            self.assertIn("Lyren Moss v690-v1", document_xml)
            self.assertIn("973 negatives", document_xml)

    def test_content_seal_replays(self):
        seal = load(FINAL / "content-seal.json")
        self.assertEqual(seal["entry_count"], len(seal["entries"]))
        for row in seal["entries"]:
            path = ROOT / row["path"]
            self.assertTrue(path.is_file(), row["path"])
            self.assertEqual(path.stat().st_size, row["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row["sha256"])

    def test_final_manifest_replays(self):
        manifest = load(FINAL / "manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            path = ROOT / row["path"]
            self.assertTrue(path.is_file(), row["path"])
            self.assertEqual(path.stat().st_size, row["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row["sha256"])

    def test_allowlist_is_complete_for_final_directory(self):
        allowlist = load(FINAL / "allowlist.json")
        actual = {path.relative_to(ROOT).as_posix() for path in FINAL.rglob("*") if path.is_file()}
        self.assertEqual(set(allowlist["allowed_paths"]), actual)
        self.assertTrue(allowlist["additive_owner_scope"])

    def test_four_tier_deck_remains_exact(self):
        deck = load(BASE / "x2/deck/deck-index.json")
        self.assertEqual(deck["counts"], {"1": 1, "2": 3, "3": 4, "4": 205})
        self.assertEqual(len(deck["order"]), 213)
        self.assertEqual(deck["core_outcomes"], {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5})

    def test_global_promotion_is_additive_and_validated(self):
        receipt = load(BASE / "x2/tooling/global-promotion.json")
        self.assertTrue(receipt["passed"])
        self.assertTrue(receipt["no_overwrite"])
        self.assertEqual(receipt["counts"], {"skills": 5, "public_runners": 5, "dependency_modules": 2})
        self.assertTrue(all(row["byte_parity"] and row["validated"] for row in receipt["skills"]))
        self.assertTrue(all(row["byte_parity"] and row["positive_passed"] and row["adverse_passed"] for row in receipt["runners"]))

    def test_source_references_are_primary_or_official(self):
        records = load(FINAL / "source-references.json")["records"]
        self.assertEqual(len(records), 4)
        self.assertTrue(all(row["url"].startswith("https://") for row in records))
        self.assertEqual(Counter(row["kind"] for row in records), {"primary paper": 2, "primary conference paper": 1, "official standard": 1})

    def test_no_raw_local_profile_path_in_text_artifacts(self):
        needle = "C:" + "\\\\Users\\\\" + Path.home().name
        hits = []
        for path in BASE.rglob("*"):
            if (
                path.is_file()
                and path.suffix.lower() in {".json", ".md", ".html", ".py", ".yaml", ".yml", ".txt"}
                and needle.lower() in path.read_text(encoding="utf-8", errors="replace").lower()
            ):
                hits.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
