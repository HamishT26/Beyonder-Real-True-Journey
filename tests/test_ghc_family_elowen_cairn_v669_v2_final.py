from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_elowen_cairn_v669_v2_archive as archive


class ElowenCairnV669V2FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.phase_root = ROOT / archive.REL_PHASE_ROOT
        cls.expected_final = os.environ.get("ELOWEN_EXPECTED_FINAL", "")
        if not re.fullmatch(r"[0-9a-f]{40}", cls.expected_final):
            raise RuntimeError("ELOWEN_EXPECTED_FINAL must bind the exact final head")

    def read_json(self, relative: str) -> dict:
        return json.loads((self.phase_root / relative).read_text(encoding="utf-8"))

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

    def test_01_exact_branch_head_clean_and_tracking_equality(self) -> None:
        self.assertEqual(self.git("branch", "--show-current"), archive.BRANCH)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.expected_final)
        self.assertEqual(self.git("rev-parse", "@{upstream}"), self.expected_final)
        self.assertEqual(self.git("rev-parse", f"refs/remotes/origin/{archive.BRANCH}"), self.expected_final)
        self.assertEqual(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True), "")

    def test_02_three_direct_single_parent_commits_and_zero_merges(self) -> None:
        commits = self.git("rev-list", "--reverse", f"{archive.SOURCE_FINAL}..{self.expected_final}").splitlines()
        self.assertEqual(commits, [archive.FROZEN_X1, archive.FROZEN_EVIDENCE, self.expected_final])
        self.assertEqual(self.git("rev-list", "--count", "--merges", f"{archive.SOURCE_FINAL}..{self.expected_final}"), "0")
        for child, parent in zip(commits, [archive.SOURCE_FINAL, archive.FROZEN_X1, archive.FROZEN_EVIDENCE], strict=True):
            self.assertEqual(self.git("rev-parse", f"{child}^"), parent)
            self.assertEqual(len(self.git("show", "-s", "--format=%P", child).split()), 1)

    def test_03_final_truth_and_outcomes_are_exact(self) -> None:
        truth = self.read_json("closeout/phase-truth.json")
        self.assertEqual(truth["core_outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        for key, value in archive.FINAL_OVERLAY.items():
            self.assertEqual(truth[key], value)
        self.assertEqual(truth["terminal_verdict"], archive.TERMINAL_VERDICT)

    def test_04_final_overview_is_three_page_equivalent_and_bounded(self) -> None:
        text = (self.phase_root / "closeout/final-integrated-overview.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\S+", text))
        self.assertGreaterEqual(words, 1800)
        self.assertLessEqual(words, archive.DOCUMENT_WORD_CEILING)
        for term in ("GMUT", "THOS", "Freed ID", "CBR", "Māori authority", archive.TERMINAL_VERDICT):
            self.assertIn(term, text)

    def test_05_negative_and_method_flow_arithmetic_is_append_only(self) -> None:
        negative = self.read_json("closeout/retained-negative-register.json")
        flow = self.read_json("closeout/method-flow-ledger.json")
        self.assertEqual(negative["effective_negatives"], 30720)
        self.assertEqual(len(flow["methods"]), 196)
        self.assertEqual(flow["effective_method_count"], 16826)
        self.assertEqual(Counter(row["result"] for row in flow["witnesses"]), {"fail": 196, "pass": 196})
        self.assertEqual(negative["final_failures"][0]["failure_id"], "EC6692-FINAL-F034")

    def test_06_open_gaps_and_exact_gates_remain_visible(self) -> None:
        register = self.read_json("closeout/open-exact-gate-register.json")
        self.assertEqual(register["effective_open_gaps"], 227)
        self.assertEqual(register["effective_exact_gates"], 222)
        self.assertEqual(register["new_open_gaps"], ["EC6692-N037", "EC6692-N038"])
        self.assertEqual(register["new_exact_gates"], ["EC6692-N039", "EC6692-N040"])

    def test_07_failed_and_corrected_stage_receipts_remain_distinct(self) -> None:
        failed = self.read_json("validation/evidence-staged-review-failed.json")
        recovery_one = self.read_json("validation/evidence-staged-recovery-failed.json")
        recovery_two = self.read_json("validation/evidence-staged-recovery-failed-2.json")
        composite = self.read_json("validation/evidence-staged-review.json")
        self.assertFalse(failed["all_passed"])
        self.assertFalse(recovery_one["all_passed"])
        self.assertFalse(recovery_two["all_passed"])
        self.assertTrue(composite["all_passed"])
        self.assertEqual(composite["aggregate_all_pass_credit"], 0)
        self.assertEqual(composite["aggregate_checks_passed"], 30)
        self.assertEqual(composite["aggregate_checks_total"], 31)

    def test_08_all_portfolios_are_executed_or_held_as_permitted(self) -> None:
        for category, expected in archive.PORTFOLIO_COUNTS.items():
            ledger = self.read_json(f"x2/portfolio-execution/{category}.json")
            self.assertEqual(ledger["count"], expected)
            self.assertTrue(set(ledger["outcome_counts"]) <= set(archive.ALLOWED_OUTCOMES))
        for category in ("exact_approval", "blocked"):
            ledger = self.read_json(f"x2/portfolio-execution/{category}.json")
            self.assertTrue(all(row["execution_state"] == "held_unexecuted" for row in ledger["rows"]))

    def test_09_skills_and_runners_remain_owner_bounded(self) -> None:
        skills = self.read_json("tools/skill-smoke-receipt.json")
        runners = self.read_json("tools/runner-smoke-receipt.json")
        self.assertEqual(skills["count"], 20)
        self.assertTrue(all(not row["globally_installed"] for row in skills["rows"]))
        self.assertEqual(runners["count"], 10)
        self.assertTrue(all(row["network_calls"] == 0 and row["external_actions"] == 0 for row in runners["rows"]))

    def test_10_lifecycle_replay_and_commit_ceiling_are_exact(self) -> None:
        lifecycle = self.read_json("closeout/lifecycle-replay.json")
        self.assertEqual(lifecycle["source_to_final_commits_after_commit"], 3)
        self.assertEqual(lifecycle["planned_phase_commits"], 3)
        self.assertTrue(lifecycle["strict_x1_before_x2"])
        self.assertTrue(lifecycle["zero_merges_expected"])

    def test_11_complete_incomplete_and_wellbeing_checks_are_explicit(self) -> None:
        checklist = self.read_json("closeout/complete-incomplete-checklist.json")
        wellbeing = self.read_json("closeout/wellbeing-workload-check.json")
        self.assertGreaterEqual(len(checklist["completed"]), 8)
        self.assertTrue(checklist["represented"] and checklist["open_gap"] and checklist["exact_gate"])
        self.assertFalse(wellbeing["health_measurement_claim"])
        self.assertIn("route_ambiguity", wellbeing["stop_conditions"])

    def test_12_static_report_has_structural_accessibility_features(self) -> None:
        report = (self.phase_root / "closeout/static-report.html").read_text(encoding="utf-8")
        required = (
            'href="#main"',
            '<main id="main">',
            '<nav aria-label="Report sections">',
            '<caption>Forty preregistered proposal outcomes</caption>',
            'scope="col"',
            'scope=\'row\'',
            ':focus',
            '@media print',
        )
        self.assertTrue(all(token in report for token in required))
        self.assertIn("remain unperformed", report)

    def test_13_final_owner_and_delta_manifests_replay_head_blobs(self) -> None:
        for relative in ("validation/final-owner-manifest.json", "validation/final-delta-manifest.json"):
            manifest = self.read_json(relative)
            self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
            for row in manifest["entries"]:
                data = subprocess.check_output(["git", "show", f"{self.expected_final}:{row['path']}"], cwd=ROOT)
                oid = subprocess.check_output(["git", "hash-object", "--stdin"], cwd=ROOT, input=data).decode().strip()
                self.assertEqual((len(data), oid, hashlib.sha256(data).hexdigest()), (row["bytes"], row["git_blob_oid"], row["sha256"]))

    def test_14_content_seal_replays_exact_head_blobs(self) -> None:
        seal = self.read_json("seal/content-seal.json")
        payload = {key: value for key, value in seal.items() if key != "payload_sha256"}
        expected_payload = archive.sha256_bytes(archive.canonical_json_bytes(payload))
        self.assertEqual(seal["payload_sha256"], expected_payload)
        for row in seal["files"]:
            data = subprocess.check_output(["git", "show", f"{self.expected_final}:{row['path']}"], cwd=ROOT)
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()), (row["bytes"], row["sha256"]))

    def test_15_closeout_receipt_and_canonical_protocol_are_pending_historical_state(self) -> None:
        closeout = self.read_json("closeout/closeout-receipt.json")
        protocol = self.read_json("validation/canonical-protocol.json")
        self.assertEqual(closeout["status"], "FINAL_CLOSEOUT_CANDIDATE")
        self.assertEqual(closeout["route_state"], "PREPARED_NOT_SENT")
        self.assertEqual(protocol["canonical_invocation_count_before_final"], 0)
        self.assertTrue(protocol["post_success_replay_forbidden"])
        self.assertFalse(protocol["complete_repository_suite"])

    def test_16_stale_label_review_retains_additive_correction(self) -> None:
        review = self.read_json("validation/stale-label-review.json")
        self.assertEqual(review["status"], "PASS_WITH_ADDITIVE_CORRECTION")
        self.assertIn("30 of 31 evidence aggregate checks passed", review["corrected_final_labels"])
        self.assertIn("EC6692-FINAL-F034", review["known_stale_narrative"])

    def test_17_route_is_prepared_not_sent_for_exact_sylven_title(self) -> None:
        route = self.read_json("closeout/route-state-final-candidate.json")
        baton = (self.phase_root / "handoffs/sylven-arc-v669-v3-activation-candidate.md").read_text(encoding="utf-8")
        self.assertEqual(route["delivery_state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["exact_target_title"], "Sylven Arc")
        self.assertEqual(route["next_phase"], "v669-v3")
        self.assertFalse(route["sent_by_elowen_cairn"])
        self.assertIn("SENT_BY_ELOWEN_CAIRN = false", baton)

    def test_18_all_phase_json_parses_and_documents_obey_ceiling(self) -> None:
        json_paths = list(self.phase_root.rglob("*.json"))
        self.assertGreaterEqual(len(json_paths), 120)
        for path in json_paths:
            json.loads(path.read_text(encoding="utf-8"))
        for path in self.phase_root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}:
                self.assertLessEqual(len(re.findall(r"\S+", path.read_text(encoding="utf-8"))), archive.DOCUMENT_WORD_CEILING)

    def test_19_privacy_and_bounded_python_security_hold(self) -> None:
        patterns = [
            re.compile(r"\b019[0-9a-f]{5}-[0-9a-f-]{20,}\b", re.I),
            re.compile(r"(?i)(?:password|secret|api[_-]?key|bearer|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"),
            re.compile(r"(?i)(?:task|thread|session|resume)[_-]?id\s*[:=]\s*['\"][^'\"]+"),
            re.compile(r"[A-Za-z]:\\(?:Users|GHC-Archives)\\"),
        ]
        hits = []
        for path in archive.phase_owner_files():
            if path.suffix.lower() in {".json", ".md", ".html", ".txt", ".py"}:
                text = path.read_text(encoding="utf-8")
                hits.extend((path, pattern.pattern) for pattern in patterns if pattern.search(text))
            if path.suffix == ".py":
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        self.assertFalse(any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords))
        self.assertEqual(hits, [])

    def test_20_scientific_professional_authority_and_stage20_boundaries_hold(self) -> None:
        overview = (self.phase_root / "closeout/final-integrated-overview.md").read_text(encoding="utf-8")
        for phrase in (
            "no real likelihood",
            "participant-free proxy",
            "synthetic and nonproduction",
            "Māori concepts remain under Māori authority",
            "NOT_READY_FOR_STAGE_20",
        ):
            self.assertIn(phrase, overview)


if __name__ == "__main__":
    unittest.main()
