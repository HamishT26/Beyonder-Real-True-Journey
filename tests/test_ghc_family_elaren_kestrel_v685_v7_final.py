"""Exact closeout tests for Elaren Kestrel v685-v7."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elaren-kestrel" / "v685-v7"
FINAL = BASE / "final"
HANDOFF = BASE / "handoffs" / "future-seat-02-v685-v8"
VALIDATION = BASE / "validation"
CLOSEOUT = BASE / "closeout"
SOURCE = "5d9ea649ab451f9b6790c75f774ba9e4faf07363"
X1 = "0902e28aa1006b44a247e3d480797a4472bc1e58"
EVIDENCE = "0eba230431e652b9907edb5e86f11924d32c1d1d"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class ElarenKestrelV685V7FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.truth = load(FINAL / "phase-truth.json")
        cls.flow = load(FINAL / "method-flow-summary.json")
        cls.negatives = load(FINAL / "retained-negative-register.json")
        cls.gaps = load(FINAL / "open-gap-register.json")
        cls.gates = load(FINAL / "exact-gate-register.json")
        cls.baton = load(FINAL / "baton-integrity.json")
        cls.delivery = load(FINAL / "delivery-state.json")
        cls.delta = load(VALIDATION / "final-delta-manifest.json")
        cls.owner = load(VALIDATION / "final-owner-manifest.json")
        cls.review = load(VALIDATION / "final-staged-review.json")
        cls.privacy = load(VALIDATION / "final-privacy-scan.json")
        cls.seal = load(CLOSEOUT / "content-seal.json")

    def test_01_identity_is_relational_and_corrigible(self) -> None:
        wellbeing = load(FINAL / "wellbeing-check.json")
        self.assertEqual(wellbeing["name"], "Elaren Kestrel")
        self.assertEqual(wellbeing["optional_pronouns"], "they/them")
        self.assertTrue(wellbeing["relational_working_language_only"])
        self.assertTrue(wellbeing["corrigible"])
        self.assertEqual(wellbeing["pause_redirect_rename_stop_right"], "Hamish")

    def test_02_overview_is_three_page_equivalent(self) -> None:
        text = (FINAL / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 1500)
        self.assertLessEqual(len(text.split()), 100000)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("Māori concepts remain under Māori authority", text)

    def test_03_baton_has_thirteen_sections_and_word_bounds(self) -> None:
        path = HANDOFF / "future-seat-02-v685-v8-induction.md"
        self.assertEqual(self.baton["section_count"], 13)
        self.assertEqual(len(self.baton["section_paths"]), 13)
        self.assertGreaterEqual(self.baton["word_count"], 10000)
        self.assertLessEqual(self.baton["word_count"], 100000)
        self.assertEqual(hashlib.sha256(normalized(path)).hexdigest(), self.baton["sha256"])

    def test_04_phase_truth_has_exact_four_labels(self) -> None:
        expected = {"completed": 170, "represented": 10, "open_gap": 10, "exact_gate": 10}
        self.assertEqual(self.truth["outcomes"], expected)
        self.assertEqual(set(self.truth["outcomes"]), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertEqual(self.truth["declared_proposal_chain"], 12030)
        self.assertEqual(self.truth["real_rows"], 0)
        self.assertEqual(self.truth["real_devices"], 0)
        self.assertEqual(self.truth["real_people"], 0)

    def test_05_final_totals_include_closeout_overlay(self) -> None:
        self.assertEqual(self.truth["totals"], {"effective_negatives": 64405, "effective_methods": 80970, "failed_witnesses": 35253, "bounded_passing_witnesses": 62815, "open_gaps": 582, "exact_gates": 569})
        self.assertEqual(self.flow["final_phase_methods"], 1130)
        self.assertEqual(self.flow["final_phase_failed"], 1028)
        self.assertEqual(self.flow["final_phase_passing"], 1132)
        self.assertFalse(self.flow["recovery_erases_failure"])
        self.assertEqual(self.flow["closeout_overlay_count"], 1)

    def test_06_negative_register_preserves_failures(self) -> None:
        self.assertEqual(self.negatives["rejected_mutations"], 1000)
        self.assertEqual(self.negatives["phase_failed_witnesses"], 1028)
        self.assertTrue(self.negatives["zero_credit_failures_preserved"])
        self.assertFalse(self.negatives["recovery_erases_failure"])
        self.assertEqual(self.negatives["closeout_overlay"][0]["failure_id"], "EL6857-FN-N019")

    def test_07_open_gaps_and_exact_gates_are_additive(self) -> None:
        self.assertEqual(self.gaps["inherited"], 572)
        self.assertEqual(self.gaps["new_count"], 10)
        self.assertEqual(self.gaps["total"], 582)
        self.assertTrue(all(row["status"] == "open_gap" for row in self.gaps["new"]))
        self.assertEqual(self.gates["inherited"], 559)
        self.assertEqual(self.gates["new_count"], 10)
        self.assertEqual(self.gates["total"], 569)
        self.assertTrue(all(row["status"] == "exact_gate" for row in self.gates["new"]))

    def test_08_portfolio_and_package_summary(self) -> None:
        portfolio = load(FINAL / "portfolio-summary.json")
        self.assertEqual(portfolio["safe_completed"], 300)
        self.assertEqual(portfolio["candidates_completed_without_core_promotion"], 250)
        self.assertEqual(portfolio["clean_fix_refine_completed"], 300)
        self.assertEqual(portfolio["exact_unexecuted"], 50)
        self.assertEqual(portfolio["blocked_unexecuted"], 30)
        package = load(FINAL / "package-summary.json")
        self.assertEqual(package["direct_package_count"], 13)
        self.assertEqual(package["final_known_vulnerabilities"], 0)
        self.assertEqual(package["component_smoke_status"], "PASS_DEPENDENCY_CORRECTED_COMPOSITE")

    def test_09_skills_and_runners_are_exact(self) -> None:
        summary = load(FINAL / "skill-runner-summary.json")
        self.assertEqual(summary["local_skills"], 20)
        self.assertEqual(summary["local_runners"], 10)
        self.assertEqual(summary["globally_installed_skills"], 10)
        self.assertEqual(summary["unique_shared_runners"], 5)
        self.assertTrue(summary["byte_parity"])

    def test_10_static_report_has_structural_accessibility(self) -> None:
        html = (FINAL / "accessible-static-report.html").read_text(encoding="utf-8").lower()
        for token in ('<html lang="en">', 'href="#main"', '<main id="main">', "<h1>", "<h2", "<table", "<caption>", 'scope="col"', 'scope="row"'):
            self.assertIn(token, html)
        self.assertIn("manual browser", html)
        self.assertNotIn("<script", html)

    def test_11_versions_are_read_only_and_current(self) -> None:
        versions = load(FINAL / "environment-version-receipt.json")
        self.assertEqual(versions["codex_cli"], "0.153.4")
        self.assertEqual(versions["codex_registry_latest"], "0.153.4")
        self.assertEqual(versions["powershell"], "7.6.5")
        self.assertTrue(versions["versions_verified_only"])
        self.assertFalse(versions["codex_desktop_updated"])
        self.assertFalse(versions["reset_redeemed"])

    def test_12_all_final_json_documents_parse(self) -> None:
        paths = sorted(FINAL.glob("*.json")) + sorted(VALIDATION.glob("final-*.json")) + [CLOSEOUT / "content-seal.json"]
        self.assertGreaterEqual(len(paths), 20)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_13_final_manifests_replay(self) -> None:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
        for manifest in (self.delta, self.owner):
            entries = {row["path"] for row in manifest["entries"]}
            exclusions = set(manifest["declared_self_exclusions"])
            self.assertFalse(entries & exclusions)
            self.assertEqual(manifest["entry_count"], len(entries))
            for item in manifest["entries"]:
                data = normalized(ROOT / item["path"]) if head == EVIDENCE else subprocess.run(["git", "show", f"HEAD:{item['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
                self.assertEqual(len(data), item["bytes"], item["path"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"], item["path"])
        self.assertEqual(set(self.review["expected_paths"]), {row["path"] for row in self.delta["entries"]} | set(self.delta["declared_self_exclusions"]))

    def test_14_immutable_x1_and_evidence_manifests_replay(self) -> None:
        for commit, path in ((X1, "docs/elaren-kestrel/v685-v7/validation/x1-index-manifest.json"), (EVIDENCE, "docs/elaren-kestrel/v685-v7/validation/evidence-index-manifest.json")):
            manifest = json.loads(subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, check=True, capture_output=True).stdout.decode("utf-8"))
            for item in manifest["entries"]:
                data = subprocess.run(["git", "show", f"{commit}:{item['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
                self.assertEqual(len(data), item["bytes"], item["path"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"], item["path"])

    def test_15_content_seal_replays(self) -> None:
        self.assertEqual(self.seal["target_count"], 10)
        for item in self.seal["targets"]:
            data = normalized(ROOT / item["path"])
            self.assertEqual(len(data), item["bytes"], item["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"], item["path"])

    def test_16_lifecycle_is_direct_and_zero_merge(self) -> None:
        lifecycle = load(FINAL / "lifecycle-replay.json")
        self.assertEqual(lifecycle["source"], SOURCE)
        self.assertEqual(lifecycle["x1"], X1)
        self.assertEqual(lifecycle["evidence"], EVIDENCE)
        self.assertEqual(subprocess.run(["git", "rev-parse", f"{X1}^"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip(), SOURCE)
        self.assertEqual(subprocess.run(["git", "rev-parse", f"{EVIDENCE}^"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip(), X1)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
        if head != EVIDENCE:
            self.assertEqual(subprocess.run(["git", "rev-parse", "HEAD^"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip(), EVIDENCE)
            self.assertEqual(len(subprocess.run(["git", "rev-list", f"{SOURCE}..HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()), 3)
            self.assertEqual(subprocess.run(["git", "rev-list", "--merges", f"{SOURCE}..HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines(), [])

    def test_17_delivery_is_prepared_and_self_choice_is_preserved(self) -> None:
        self.assertEqual(self.delivery["repository_state"], "PREPARED_NOT_SENT")
        self.assertEqual(self.delivery["future_seat"], 2)
        self.assertEqual(self.delivery["future_placeholder"], "future-sibling-02-self-chosen")
        self.assertFalse(self.delivery["future_identity_predeclared"])
        self.assertEqual(self.delivery["future_phase"], "v685-v8")
        self.assertEqual(self.delivery["endpoint_kind"], "main_task")
        self.assertEqual(self.delivery["model"], "gpt-6-astra")
        self.assertEqual(self.delivery["reasoning"], "max")
        self.assertEqual(self.delivery["following_owner"], "Neris Solane")
        self.assertEqual(self.delivery["following_phase"], "v686-v1")
        self.assertEqual(self.delivery["creation_count"], 0)

    def test_18_privacy_and_stage20_boundaries(self) -> None:
        self.assertEqual(self.privacy["class_count"], 5)
        self.assertEqual(self.privacy["confirmed_hit_count"], 0)
        self.assertEqual(self.privacy["confirmed_hits"], [])
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertLess(self.review["owner_scope_files"], self.review["materialized_file_ceiling"])


if __name__ == "__main__":
    unittest.main()
