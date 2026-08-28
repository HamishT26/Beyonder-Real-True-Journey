#!/usr/bin/env python3
"""Closeout-candidate tests for Sable Rook v674-v2."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


SOURCE = "6f079df9a056f00e80392b7e036abc023db5fa88"
X1 = "81ad6f98f24087777691e96201312e66c37ac844"
EVIDENCE = "1625313186adde8dc94d210376f184bde5dfb0dc"
BRANCH = "codex/GHC-Family/sable-rook-v674-v2-full-tools"
ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v674-v2"
FINAL = PHASE / "final"
REPORTS = PHASE / "reports"
HANDOFFS = PHASE / "handoffs"
VALIDATION = PHASE / "validation"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class SableRookV674V2FinalTests(unittest.TestCase):
    def test_01_exact_ancestry_and_commit_ceiling(self) -> None:
        head = git("rev-parse", "HEAD")
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        self.assertEqual(git("merge-base", "--is-ancestor", EVIDENCE, head), "")
        self.assertIn(int(git("rev-list", "--count", f"{SOURCE}..{head}")), {2, 3})
        self.assertEqual(git("rev-list", "--merges", f"{SOURCE}..{head}"), "")
        self.assertEqual(git("branch", "--show-current"), BRANCH)
        if head != EVIDENCE:
            self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE)

    def test_02_final_truth_preserves_exact_outcomes_and_veto(self) -> None:
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual(truth["proposal_chain"], 6670)
        self.assertEqual(truth["outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(truth["retained_invalid_mutations"], 240)
        self.assertEqual(truth["real_people"], 0)
        self.assertEqual(truth["real_data_rows"], 0)
        self.assertEqual(truth["external_actions"], 0)
        self.assertFalse(truth["complete_repository_suite"])
        self.assertFalse(truth["independent_reproduction"])
        self.assertFalse(truth["empirical_confirmation"])
        self.assertFalse(truth["maori_authority"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_03_method_flow_retains_every_phase_failure(self) -> None:
        flow = load(FINAL / "method-flow-ledger.json")
        negatives = load(FINAL / "retained-negative-register.json")
        self.assertEqual(flow["failure_count"], 18)
        self.assertEqual(len(flow["failures"]), 18)
        self.assertTrue(all(row["state"] == "failed_retained_zero_credit" for row in flow["failures"]))
        self.assertTrue(all(row["success_credit"] == 0 for row in flow["failures"]))
        self.assertEqual(negatives["effective_negatives"], 38362)
        self.assertEqual(negatives["erased"], 0)
        self.assertEqual(negatives["converted_to_original_pass"], 0)

    def test_04_open_and_exact_gates_remain_open(self) -> None:
        gates = load(FINAL / "gate-register.json")
        self.assertEqual(gates["open_gap_count"], 313)
        self.assertEqual(gates["exact_gate_count"], 306)
        self.assertEqual(gates["silently_closed"], 0)
        self.assertFalse(gates["software_can_close_authority_gate"])
        self.assertIn("Maori authority", gates["protected_surfaces"])

    def test_05_exact_and_blocked_packets_remain_unexecuted(self) -> None:
        holds = load(PHASE / "x2" / "portfolios" / "protected-holds.json")
        checklist = load(FINAL / "complete-incomplete-checklist.json")
        self.assertEqual(len(holds["exact_approval"]), 20)
        self.assertEqual(len(holds["blocked"]), 10)
        self.assertEqual(holds["executed"], 0)
        self.assertTrue(any("Freed ID" in row for row in checklist["incomplete_or_reserved"]))
        self.assertTrue(any("Stage 20" in row for row in checklist["incomplete_or_reserved"]))

    def test_06_final_overview_and_handoff_meet_document_bounds(self) -> None:
        overview = (REPORTS / "final-integrated-overview.md").read_text(encoding="utf-8")
        baton = (HANDOFFS / "caelen-ash-v674-v3-activation-candidate.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 700)
        self.assertGreaterEqual(len(baton.split()), 10000)
        self.assertLessEqual(len(baton.split()), 100000)
        self.assertIn("PREPARED_NOT_SENT", baton)
        self.assertIn("NOT_READY_FOR_STAGE_20", baton)
        self.assertIn("relational working language only", baton)
        self.assertIn("Caelen Ash", baton)

    def test_07_route_is_prepared_but_not_sent(self) -> None:
        route = load(FINAL / "route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["next_owner"], "Caelen Ash")
        self.assertEqual(route["next_phase"], "v674-v3")
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["precontact"])
        self.assertEqual(route["send_attempts"], 0)
        self.assertFalse(route["delivery_acknowledged"])

    def test_08_final_owner_manifest_replays_normalized_worktree_bytes(self) -> None:
        manifest = load(VALIDATION / "final-owner-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["owner_path_total"], manifest["entry_count"] + len(manifest["self_exclusions"]))
        self.assertLess(manifest["owner_path_total"], 2000)
        for entry in manifest["entries"]:
            data = normalized((ROOT / entry["path"]).read_bytes())
            self.assertEqual(len(data), entry["bytes_normalized_lf"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"], entry["path"])

    def test_09_final_delta_manifest_replays_normalized_worktree_bytes(self) -> None:
        manifest = load(VALIDATION / "final-delta-manifest.json")
        self.assertEqual(manifest["parent"], EVIDENCE)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["final_delta_path_total"], manifest["entry_count"] + len(manifest["self_exclusions"]))
        for entry in manifest["entries"]:
            data = normalized((ROOT / entry["path"]).read_bytes())
            self.assertEqual(len(data), entry["bytes_normalized_lf"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256_normalized_lf"], entry["path"])

    def test_10_json_python_and_document_surfaces_are_bounded(self) -> None:
        json_files = sorted(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(json_files), 120)
        for path in json_files:
            load(path)
        for path in [
            ROOT / "scripts" / "build_ghc_family_sable_rook_v674_v2_closeout.py",
            ROOT / "scripts" / "validate_ghc_family_sable_rook_v674_v2_final.py",
            ROOT / "tests" / "test_ghc_family_sable_rook_v674_v2_final.py",
        ]:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        for path in PHASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)

    def test_11_accessible_report_reserves_manual_evaluation(self) -> None:
        html = (REPORTS / "accessible-static-report.html").read_text(encoding="utf-8")
        markdown = (REPORTS / "accessible-static-report.md").read_text(encoding="utf-8")
        self.assertIn('<html lang="en">', html)
        self.assertIn("<main>", html)
        self.assertIn("<caption>", html)
        self.assertIn("assistive-technology", html)
        self.assertIn("affected-user evaluation", markdown)
        self.assertIn("not complete accessibility conformance", markdown.lower())

    def test_12_public_final_surface_has_no_private_payload(self) -> None:
        patterns = [
            re.compile(rb"(?:C:\\Users\\|D:\\GHC-Archives)", re.I),
            re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
            re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
        ]
        hits = []
        for root in [FINAL, REPORTS, HANDOFFS]:
            for path in root.rglob("*"):
                if not path.is_file():
                    continue
                data = path.read_bytes()
                if any(pattern.search(data) for pattern in patterns):
                    hits.append(str(path.relative_to(ROOT)))
        self.assertEqual(hits, [])

    def test_13_environment_and_family_index_preserve_compatibility(self) -> None:
        environment = load(FINAL / "environment-receipt.json")
        index = load(FINAL / "ghc-family-index.json")
        self.assertEqual(environment["storage"], "D-first additive sparse owner lane")
        self.assertFalse(environment["desktop_updated"])
        self.assertFalse(environment["elevation"])
        self.assertFalse(environment["sandbox_or_hyperv_activated"])
        self.assertFalse(environment["host_security_weakened"])
        self.assertEqual(index["runner_prefix"], "ghc_family_caption_")
        self.assertEqual(index["historical_aliases_deleted"], 0)
        self.assertEqual(index["global_installations"], 0)

    def test_14_sources_are_vocabulary_only(self) -> None:
        ledger = load(FINAL / "source-status-ledger.json")
        self.assertEqual(len(ledger["entries"]), 4)
        self.assertFalse(ledger["citations_are_observations"])
        self.assertEqual(ledger["real_data_rows"], 0)
        self.assertFalse(ledger["authority_delegated"])


if __name__ == "__main__":
    unittest.main()
