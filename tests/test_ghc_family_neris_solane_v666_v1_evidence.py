from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "neris-solane" / "v666-v1"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str]]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        self.tags.append((tag, dict(attrs)))


class NerisSolaneV666V1EvidenceTests(unittest.TestCase):
    def test_evidence_counts(self) -> None:
        summary = load("evidence/evidence-summary.json")
        self.assertEqual(summary["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(summary["bounded_positives"], 20)
        self.assertEqual(summary["rejecting_mutations"], 100)
        self.assertEqual(summary["accepted_mutations"], 0)
        self.assertEqual(summary["new_frozen_total"], 4190)
        self.assertEqual(summary["effective"], {"negatives": 26158, "methods": 10470, "open_gaps": 183, "exact_gates": 181})
        self.assertFalse(summary["independent_reproduction"])

    def test_inherited_seal_and_overlays_are_separate(self) -> None:
        summary = load("evidence/evidence-summary.json")
        self.assertEqual(summary["repository_sealed_inherited"], {"negatives": 26039, "methods": 10236, "open_gaps": 182, "exact_gates": 180})
        self.assertEqual(summary["inherited_external_overlay"], {"negatives": 2, "methods": 2})
        self.assertEqual(summary["neris_startup_and_x1"], {"negatives": 16, "methods": 16})
        self.assertEqual(summary["neris_x2"], {"mutation_negatives": 100, "methods": 215, "operational_negatives": 0, "operational_methods": 0})
        self.assertEqual(summary["neris_evidence"], {"operational_negatives": 1, "operational_methods": 1})
        overlay = load("method-flow/evidence-operational-overlay.json")
        self.assertEqual(overlay["effective_negatives_after_this_overlay"], 26158)
        self.assertEqual(overlay["effective_methods_after_this_overlay"], 10470)
        self.assertEqual([row["failure_id"] for row in overlay["rows"]], ["NRS6661-EVID-N001"])
        self.assertTrue(overlay["no_failure_erased"])

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
        self.assertEqual(len(review["new_material_threats"]), 0)
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
        self.assertEqual(gaps["open_gap_count"], 183)
        self.assertEqual(gaps["exact_gate_count"], 181)
        self.assertEqual(gaps["new_open_gap"]["proposal_id"], "NRS6661-N019")
        self.assertEqual(gaps["new_exact_gate"]["proposal_id"], "NRS6661-N020")
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
        for term in ("screen-reader", "keyboard", "zoom", "cognitive-accessibility", "Māori-language", "affected-user"):
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

    def test_evidence_manifest_when_present(self) -> None:
        path = PHASE / "validation" / "evidence-content-manifest.json"
        if not path.exists():
            self.skipTest("manifest is generated after staged review")
        manifest = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["phase"], "evidence")
        self.assertEqual(manifest["x1_sha"], "435bfd997f7f56635f6ba63d8da7ea2505059a75")
        self.assertNotIn(
            "docs/neris-solane/v666-v1/validation/evidence-content-manifest.json",
            {row["path"] for row in manifest["entries"]},
        )
        for entry in manifest["entries"]:
            blob = subprocess.check_output(["git", "-C", str(ROOT), "show", ":" + entry["path"]])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])
            self.assertEqual(len(blob), entry["size_bytes"])


if __name__ == "__main__":
    unittest.main()
