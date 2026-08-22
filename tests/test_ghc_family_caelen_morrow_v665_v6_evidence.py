from __future__ import annotations

import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-morrow" / "v665-v6"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str]]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        self.tags.append((tag, dict(attrs)))


class CaelenMorrowV665V6EvidenceTests(unittest.TestCase):
    def test_evidence_counts(self) -> None:
        summary = load("evidence/evidence-summary.json")
        self.assertEqual(summary["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(summary["bounded_positives"], 20)
        self.assertEqual(summary["rejecting_mutations"], 100)
        self.assertEqual(summary["accepted_mutations"], 0)
        self.assertEqual(summary["effective"], {"negatives": 25793, "methods": 9765, "open_gaps": 180, "exact_gates": 178})
        self.assertFalse(summary["independent_reproduction"])

    def test_inherited_seal_and_overlays_are_separate(self) -> None:
        summary = load("evidence/evidence-summary.json")
        self.assertEqual(summary["repository_sealed_inherited"], {"negatives": 25668, "methods": 9530, "open_gaps": 179, "exact_gates": 177})
        self.assertEqual(summary["inherited_external_overlay"], {"negatives": 4, "methods": 4})
        self.assertEqual(summary["caelen_startup"], {"negatives": 16, "methods": 16})
        self.assertEqual(summary["caelen_x2"]["operational_negatives"], 5)

    def test_environment_receipt_is_version_only(self) -> None:
        receipt = load("evidence/environment-version-receipt.json")
        self.assertTrue(receipt["version_checks_only"])
        self.assertEqual(receipt["software_installed"], 0)
        self.assertEqual(receipt["software_updated"], 0)
        self.assertFalse(receipt["host_security_changed"])
        self.assertFalse(receipt["sandbox_or_hyper_v_changed"])
        self.assertFalse(receipt["elevation_used"])
        self.assertFalse(receipt["rebooted"])
        self.assertFalse(receipt["private_host_or_path_recorded"])

    def test_threat_review_retains_residual_risk(self) -> None:
        review = load("evidence/threat-model-review.json")
        self.assertEqual(review["threat_count"], 10)
        self.assertEqual(len(review["new_material_threats"]), 2)
        self.assertTrue(review["residual_risks_visible"])
        self.assertTrue(review["authority_gates_unchanged"])
        self.assertIn("not exhaustive security", review["security_claim"])

    def test_complete_incomplete_are_distinct(self) -> None:
        checklist = load("evidence/complete-incomplete-checklist.json")
        self.assertTrue(checklist["complete_bounded"])
        self.assertTrue(checklist["incomplete_lifecycle"])
        self.assertTrue(checklist["incomplete_protected"])
        self.assertFalse(checklist["successor_contacted"])
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_open_and_exact_gates(self) -> None:
        gaps = load("evidence/authority-and-evidence-gaps.json")
        self.assertEqual(gaps["open_gap_count"], 180)
        self.assertEqual(gaps["exact_gate_count"], 178)
        self.assertEqual(gaps["new_open_gap"]["proposal_id"], "CM6656-N019")
        self.assertEqual(gaps["new_exact_gate"]["proposal_id"], "CM6656-N020")
        self.assertTrue(gaps["no_gate_promoted"])

    def test_portfolio_evidence(self) -> None:
        receipt = load("evidence/portfolio-evidence-receipt.json")
        self.assertEqual(receipt["safe_now_completed_bounded"], 30)
        self.assertEqual(receipt["exact_approval_unexecuted"], 10)
        self.assertEqual(receipt["blocked_unexecuted"], 5)
        self.assertEqual(receipt["phase_local_skills_built_validated_smoke_used"], 10)
        self.assertEqual(receipt["family_current_runners_built_validated_smoke_used"], 10)
        self.assertEqual(receipt["global_installations"], 0)

    def test_overview_is_three_page_equivalent_and_sanitized(self) -> None:
        text = (PHASE / "reports" / "integrated-evidence-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\S+", text)), 1800)
        for marker in (
            "NOT_READY_FOR_STAGE_20",
            "## Outcome and evidence boundary",
            "## Method Flow and retained failures",
            "## Complete, incomplete, and terminal route",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("source_" + "thread_id", text)
        self.assertNotRegex(text, r"[A-Z]:\\")

    def test_static_report_structure(self) -> None:
        text = (PHASE / "reports" / "static-report.html").read_text(encoding="utf-8")
        parser = StructureParser()
        parser.feed(text)
        tags = [tag for tag, attrs in parser.tags]
        html_attrs = next(attrs for tag, attrs in parser.tags if tag == "html")
        self.assertEqual(html_attrs.get("lang"), "en-NZ")
        self.assertEqual(tags.count("h1"), 1)
        self.assertIn("main", tags)
        self.assertIn("nav", tags)
        self.assertGreaterEqual(tags.count("caption"), 2)
        self.assertIn("prefers-reduced-motion", text)
        self.assertIn("skip-link", text)
        self.assertNotIn("<script", text.casefold())
        self.assertNotIn("<form", text.casefold())

    def test_manual_accessibility_reservations_visible(self) -> None:
        text = (PHASE / "reports" / "static-report.html").read_text(encoding="utf-8")
        for term in ("screen-reader", "refreshable-braille-display", "cognitive-accessibility", "Māori-language", "affected-user"):
            self.assertIn(term, text)

    def test_wellbeing_is_bounded(self) -> None:
        receipt = load("evidence/wellbeing-workload-check.json")
        self.assertEqual(receipt["real_worker_observations"], 0)
        self.assertFalse(receipt["fatigue_inference"])
        self.assertFalse(receipt["personhood_or_emotion_claim"])

    def test_all_phase_json_parses(self) -> None:
        paths = sorted(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 90)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
