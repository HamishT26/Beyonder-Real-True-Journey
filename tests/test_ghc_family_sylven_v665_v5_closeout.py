#!/usr/bin/env python3
"""Closeout and exact-final tests for Sylven Arc v665-v5."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import build_ghc_family_sylven_v665_v5_closeout as builder  # noqa: E402


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=True
    ).stdout.strip()


def staged() -> set[str]:
    raw = git("diff", "--cached", "--name-only")
    return set(raw.splitlines()) if raw else set()


def phase_blob(path: str) -> bytes:
    revision = ":" if path in staged() else "HEAD:"
    return subprocess.run(
        ["git", "show", f"{revision}{path}"], cwd=ROOT, capture_output=True, check=True
    ).stdout


def doc(relative: str):
    return json.loads(phase_blob(f"docs/sylven-arc/v665-v5/{relative}").decode("utf-8"))


class SylvenV665V5CloseoutTests(unittest.TestCase):
    def test_01_direct_single_parent_lifecycle(self):
        self.assertEqual(git("rev-parse", f"{builder.X1}^"), builder.SOURCE)
        self.assertEqual(git("rev-parse", f"{builder.EVIDENCE}^"), builder.X1)
        if staged():
            self.assertEqual(git("rev-parse", "HEAD"), builder.EVIDENCE)
            prospective_commits = int(git("rev-list", "--count", f"{builder.SOURCE}..HEAD")) + 1
        else:
            self.assertEqual(git("rev-parse", "HEAD^"), builder.EVIDENCE)
            prospective_commits = int(git("rev-list", "--count", f"{builder.SOURCE}..HEAD"))
        self.assertEqual(prospective_commits, 3)
        merges = git("rev-list", "--merges", f"{builder.SOURCE}..HEAD")
        self.assertEqual(merges, "")

    def test_02_phase_truth_exact(self):
        truth = doc("closeout/phase-truth.json")
        self.assertEqual(truth["frozen_proposals_after"], 4110)
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["terminal_verdict"], builder.TERMINAL_VERDICT)
        self.assertTrue(truth["valid"])

    def test_03_zero_real_world_credit(self):
        truth = doc("closeout/phase-truth.json")
        for key in ("real_rows", "real_people", "real_studios_kilns_wares_glazes_or_materials", "real_keys_or_proofs", "authority_events"):
            self.assertEqual(truth[key], 0)
        self.assertTrue(truth["same_owner_validation_only"])
        self.assertFalse(truth["independent_reproduction"])
        self.assertFalse(truth["full_repository_suite_run"])

    def test_04_retained_negative_total_and_no_erasure(self):
        register = doc("closeout/retained-negative-register.json")
        self.assertEqual(register["inherited_repository_sealed_count"], 25551)
        self.assertEqual(register["inherited_source_external_count"], 1)
        self.assertEqual(register["sylven_startup_count"], 10)
        self.assertEqual(register["mutation_count"], 100)
        self.assertEqual(register["x2_operational_count"], 0)
        self.assertEqual(register["closeout_operational_count"], 6)
        self.assertEqual(register["effective_total"], 25668)
        self.assertEqual(register["failure_erasure_count"], 0)
        self.assertTrue(register["valid"])

    def test_05_method_flow_total(self):
        flow = doc("closeout/method-flow-final.json")
        self.assertEqual(flow["source_repository_sealed_methods"], 9413)
        self.assertEqual(flow["source_external_methods"], 1)
        self.assertEqual(flow["startup_methods"], 10)
        self.assertEqual(flow["x2_methods"], 100)
        self.assertEqual(flow["closeout_methods"], 6)
        self.assertEqual(flow["effective_total"], 9530)
        self.assertEqual(flow["failure_erasure_count"], 0)
        self.assertTrue(flow["valid"])

    def test_06_gap_and_gate_totals(self):
        gates = doc("closeout/exact-open-gate-register.json")
        self.assertEqual(gates["open_gap_total"], 179)
        self.assertEqual(gates["exact_gate_total"], 177)
        self.assertEqual(gates["silently_closed_count"], 0)
        self.assertEqual(gates["new_open_gaps"][0]["outcome"], "open_gap")
        self.assertEqual(gates["new_exact_gates"][0]["outcome"], "exact_gate")
        self.assertTrue(gates["valid"])

    def test_07_complete_incomplete_are_both_visible(self):
        checklist = doc("closeout/complete-incomplete-checklist.json")
        self.assertGreaterEqual(checklist["complete_count"], 10)
        self.assertGreaterEqual(checklist["incomplete_count"], 7)
        self.assertTrue(any("independent" in row for row in checklist["incomplete"]))
        self.assertTrue(checklist["valid"])

    def test_08_overview_is_three_page_equivalent(self):
        text = phase_blob("docs/sylven-arc/v665-v5/reports/final-integrated-overview.md").decode("utf-8")
        self.assertTrue(text.startswith("# Sylven Arc v665-v5"))
        self.assertGreaterEqual(len(text.split()), 1500)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("## 11. Retention, Method Flow, and wellbeing", text)

    def test_09_static_report_structural_accessibility(self):
        text = phase_blob("docs/sylven-arc/v665-v5/reports/static-report.html").decode("utf-8")
        for token in ('<!doctype html>', '<html lang="en">', 'href="#main"', '<main id="main">', '<caption>', ':focus'):
            self.assertIn(token, text)
        self.assertNotIn("<script", text.casefold())
        self.assertIn("Manual keyboard", text)

    def test_10_environment_has_no_prohibited_action(self):
        receipt = doc("closeout/environment-version-receipt.json")
        self.assertEqual(receipt["version_action"], "verified_only")
        for key in ("desktop_updated", "privilege_elevation", "host_security_weakened", "sandbox_or_hyper_v_activated", "windows_features_changed", "unrelated_software_installed", "rebooted", "fast_mode_claimed"):
            self.assertFalse(receipt[key])
        self.assertTrue(receipt["valid"])

    def test_11_delivery_is_unresolved_and_unsent(self):
        delivery = doc("closeout/delivery-state.json")
        auth = doc("closeout/auth-roster-receipt.json")
        self.assertEqual(delivery["successor_state"], "PREPARED_NOT_SENT")
        self.assertEqual(delivery["send_count"], 0)
        self.assertEqual(auth["successor_recipient"], "UNRESOLVED_PENDING_FRESH_LIVE_ROUTE_READ")
        self.assertFalse(auth["active_status_alone_assigns_phase"])

    def test_12_final_delta_manifest_replays(self):
        manifest = doc("validation/final-delta-manifest.json")
        self.assertEqual(manifest["entry_count"], len(builder.BASE_PATHS))
        self.assertEqual(manifest["declared_self_exclusion_count"], 4)
        for entry in manifest["entries"]:
            raw = phase_blob(entry["path"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"])
            self.assertEqual(len(raw), entry["size"])
        self.assertTrue(manifest["coverage_valid"])

    def test_13_final_owner_manifest_pathset_and_hashes(self):
        manifest = doc("validation/final-owner-manifest.json")
        expected = sorted([entry["path"] for entry in manifest["entries"]] + manifest["declared_self_exclusions"])
        if staged():
            actual = sorted(git("diff", "--cached", "--name-only", "--diff-filter=ACMR", builder.SOURCE).splitlines())
        else:
            actual = sorted(git("diff", "--name-only", "--diff-filter=ACMR", f"{builder.SOURCE}..HEAD").splitlines())
        self.assertEqual(actual, expected)
        for entry in manifest["entries"]:
            raw = phase_blob(entry["path"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"])
        self.assertTrue(manifest["coverage_valid"])

    def test_14_all_phase_json_is_strict(self):
        paths = git("ls-files", "docs/sylven-arc/v665-v5").splitlines()
        json_paths = [path for path in paths if path.endswith(".json")]
        self.assertGreaterEqual(len(json_paths), 100)
        for path in json_paths:
            json.loads(phase_blob(path).decode("utf-8"))

    def test_15_staged_review_ceiling_privacy_and_diff(self):
        review = doc("validation/final-staged-review.json")
        self.assertEqual(review["confirmed_privacy_or_raw_identifier_hits"], 0)
        self.assertEqual(review["diff_hygiene_issues"], 0)
        self.assertEqual(review["deletion_paths"], [])
        self.assertTrue(review["under_2000_file_ceiling"])
        self.assertTrue(review["under_100000_word_ceiling"])
        self.assertTrue(review["valid"])

    def test_16_x1_and_evidence_manifests_remain_immutable(self):
        for revision, path in ((builder.X1, "docs/sylven-arc/v665-v5/x1/x1-content-manifest.json"), (builder.EVIDENCE, "docs/sylven-arc/v665-v5/x2/validation/evidence-content-manifest.json")):
            manifest = json.loads(subprocess.run(["git", "show", f"{revision}:{path}"], cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8"))
            for entry in manifest["entries"]:
                raw = subprocess.run(["git", "show", f"{revision}:{entry['path']}"], cwd=ROOT, capture_output=True, check=True).stdout
                self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"])

    def test_17_canonical_contract_is_one_shot_and_bounded(self):
        contract = doc("validation/final-canonical-contract.json")
        self.assertEqual(contract["invocation_limit"], 1)
        self.assertTrue(contract["successful_invocation_must_not_be_replayed"])
        self.assertFalse(contract["full_repository_suite"])
        self.assertFalse(contract["independent_reproduction"])
        self.assertTrue(contract["valid"])

    def test_18_exact_staged_check_or_committed_clean_state(self):
        if staged():
            result = builder.check_staged()
            self.assertTrue(result["valid"])
            self.assertEqual(result["privacy_confirmed_hits"], 0)
        else:
            self.assertEqual(git("status", "--porcelain=v1"), "")
            self.assertEqual(git("branch", "--show-current"), builder.BRANCH)


if __name__ == "__main__":
    unittest.main()
