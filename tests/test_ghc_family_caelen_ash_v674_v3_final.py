#!/usr/bin/env python3
"""Closeout-candidate tests for Caelen Ash v674-v3."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


SOURCE = "0b9ccf8c74f3b0a5f96b8582162df8e2a06edd05"
X1 = "aaff9f4bfe18c2d7dd428cf6cb7b639f3b420b46"
EVIDENCE = "0a50b3d7a13fe3b78302d41b6f8ad61325208ebd"
BRANCH = "codex/GHC-Family/caelen-ash-v674-v3-full-tools"
ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v674-v3"
FINAL = PHASE / "final"
REPORTS = PHASE / "reports"
HANDOFFS = PHASE / "handoffs"
VALIDATION = PHASE / "validation"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class CaelenAshV674V3FinalTests(unittest.TestCase):
    def test_01_exact_ancestry_and_commit_ceiling(self) -> None:
        head = git("rev-parse", "HEAD")
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        self.assertEqual(git("merge-base", "--is-ancestor", EVIDENCE, head), "")
        self.assertIn(
            int(git("rev-list", "--count", f"{SOURCE}..{head}")),
            {2, 3},
        )
        self.assertEqual(git("rev-list", "--merges", f"{SOURCE}..{head}"), "")
        self.assertEqual(git("branch", "--show-current"), BRANCH)
        if head != EVIDENCE:
            self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE)

    def test_02_final_truth_preserves_outcomes_counts_and_veto(self) -> None:
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual(truth["proposal_chain"], 6730)
        self.assertEqual(
            truth["outcomes"],
            {
                "completed": 42,
                "represented": 12,
                "open_gap": 3,
                "exact_gate": 3,
            },
        )
        self.assertEqual(truth["retained_invalid_mutations"], 240)
        self.assertEqual(
            truth["effective_counts"],
            {
                "effective_negatives": 38612,
                "methods": 26466,
                "failed_witnesses": 10273,
                "bounded_passing_witnesses": 13749,
                "open_gaps": 316,
                "exact_gates": 309,
            },
        )
        self.assertEqual(truth["real_people"], 0)
        self.assertEqual(truth["real_data_rows"], 0)
        self.assertEqual(truth["external_actions"], 0)
        self.assertFalse(truth["complete_repository_suite"])
        self.assertFalse(truth["independent_reproduction"])
        self.assertFalse(truth["empirical_confirmation"])
        self.assertFalse(truth["maori_authority"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_03_method_flow_retains_all_ten_owner_failures(self) -> None:
        flow = load(FINAL / "method-flow-ledger.json")
        negatives = load(FINAL / "retained-negative-register.json")
        self.assertEqual(flow["failure_count"], 10)
        self.assertEqual(len(flow["failures"]), 10)
        self.assertEqual(
            {row["failure_id"] for row in flow["failures"]},
            {
                *(f"CA6743-X1-F{index:03d}" for index in range(1, 9)),
                "CA6743-FINAL-F001",
                "CA6743-FINAL-F002",
            },
        )
        self.assertTrue(
            all(
                row["state"] == "failed_retained_zero_credit"
                and row["success_credit"] == 0
                for row in flow["failures"]
            )
        )
        self.assertEqual(negatives["effective_negatives"], 38612)
        self.assertEqual(negatives["erased"], 0)
        self.assertEqual(negatives["converted_to_original_pass"], 0)

    def test_04_open_and_exact_gates_remain_open(self) -> None:
        gates = load(FINAL / "gate-register.json")
        self.assertEqual(gates["open_gap_count"], 316)
        self.assertEqual(gates["exact_gate_count"], 309)
        self.assertEqual(gates["silently_closed"], 0)
        self.assertFalse(gates["software_can_close_authority_gate"])
        self.assertIn("Maori authority", gates["protected_surfaces"])

    def test_05_exact_and_blocked_packets_remain_unexecuted(self) -> None:
        holds = load(PHASE / "x2" / "portfolios" / "protected-holds.json")
        checklist = load(FINAL / "complete-incomplete-checklist.json")
        self.assertEqual(len(holds["exact_approval_packets"]), 20)
        self.assertEqual(len(holds["blocked_packets"]), 10)
        self.assertEqual(holds["executed_holds"], 0)
        self.assertTrue(
            any("Freed ID" in row for row in checklist["incomplete_or_reserved"])
        )
        self.assertTrue(
            any("Stage 20" in row for row in checklist["incomplete_or_reserved"])
        )

    def test_06_final_overview_and_handoff_meet_document_bounds(self) -> None:
        overview = (REPORTS / "final-integrated-overview.md").read_text(
            encoding="utf-8"
        )
        baton = (
            HANDOFFS / "orin-thale-v674-v4-activation-candidate.md"
        ).read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1000)
        self.assertGreaterEqual(len(baton.split()), 10000)
        self.assertLessEqual(len(baton.split()), 100000)
        self.assertIn("PREPARED_NOT_SENT", baton)
        self.assertIn("NOT_READY_FOR_STAGE_20", baton)
        self.assertIn("relational working language only", baton)
        self.assertIn("Orin Thale", baton)
        self.assertIn("v725-v8", baton)

    def test_07_route_is_prepared_but_not_sent(self) -> None:
        route = load(FINAL / "route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["next_owner"], "Orin Thale")
        self.assertEqual(route["next_phase"], "v674-v4")
        self.assertEqual(route["live_continuation_authority_terminal_label"], "v725-v8")
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["collaboration_subagent_spawned"])
        self.assertFalse(route["precontact"])
        self.assertEqual(route["send_attempts"], 0)
        self.assertFalse(route["delivery_acknowledged"])

    def test_08_final_owner_manifest_replays_normalized_bytes(self) -> None:
        manifest = load(VALIDATION / "final-owner-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(
            manifest["owner_path_total"],
            manifest["entry_count"] + len(manifest["self_exclusions"]),
        )
        self.assertLess(manifest["owner_path_total"], 2000)
        for entry in manifest["entries"]:
            data = normalized((ROOT / entry["path"]).read_bytes())
            self.assertEqual(len(data), entry["bytes_normalized_lf"], entry["path"])
            self.assertEqual(
                hashlib.sha256(data).hexdigest(),
                entry["sha256_normalized_lf"],
                entry["path"],
            )

    def test_09_final_delta_manifest_replays_normalized_bytes(self) -> None:
        manifest = load(VALIDATION / "final-delta-manifest.json")
        self.assertEqual(manifest["parent"], EVIDENCE)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(
            manifest["final_delta_path_total"],
            manifest["entry_count"] + len(manifest["self_exclusions"]),
        )
        for entry in manifest["entries"]:
            data = normalized((ROOT / entry["path"]).read_bytes())
            self.assertEqual(len(data), entry["bytes_normalized_lf"], entry["path"])
            self.assertEqual(
                hashlib.sha256(data).hexdigest(),
                entry["sha256_normalized_lf"],
                entry["path"],
            )

    def test_10_json_python_documents_and_owner_cap_hold(self) -> None:
        json_files = sorted(PHASE.rglob("*.json"))
        self.assertIn(len(json_files), {126, 127})
        for path in json_files:
            load(path)
        for path in [
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v674_v3_closeout.py",
            ROOT / "scripts" / "validate_ghc_family_caelen_ash_v674_v3_final.py",
            ROOT / "tests" / "test_ghc_family_caelen_ash_v674_v3_final.py",
        ]:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        for path in PHASE.rglob("*.md"):
            self.assertLessEqual(
                len(path.read_text(encoding="utf-8").split()), 100000, path
            )
        self.assertLess(len([p for p in PHASE.rglob("*") if p.is_file()]), 2000)

    def test_11_accessible_report_reserves_manual_evaluation(self) -> None:
        html = (REPORTS / "accessible-static-report.html").read_text(
            encoding="utf-8"
        )
        markdown = (REPORTS / "accessible-static-report.md").read_text(
            encoding="utf-8"
        )
        self.assertIn('<html lang="en">', html)
        self.assertIn("<main>", html)
        self.assertIn("<caption>", html)
        self.assertIn("assistive-technology", html)
        self.assertIn("affected-user evaluation", markdown)
        self.assertIn("not complete accessibility conformance", markdown.lower())

    def test_12_public_final_surface_has_no_private_payload(self) -> None:
        patterns = [
            re.compile(rb"(?:C:\\Users\\|D:\\GHC-Archives)", re.I),
            re.compile(
                rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
                re.I,
            ),
            re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
        ]
        hits = []
        for root in [FINAL, REPORTS, HANDOFFS]:
            for path in root.rglob("*"):
                if path.is_file() and any(pattern.search(path.read_bytes()) for pattern in patterns):
                    hits.append(str(path.relative_to(ROOT)))
        self.assertEqual(hits, [])

    def test_13_environment_and_family_index_preserve_compatibility(self) -> None:
        environment = load(FINAL / "environment-receipt.json")
        index = load(FINAL / "ghc-family-index.json")
        self.assertEqual(environment["storage"], "D-first additive sparse owner lane")
        self.assertTrue(environment["versions_verified_only"])
        self.assertFalse(environment["desktop_updated"])
        self.assertFalse(environment["elevation"])
        self.assertFalse(environment["sandbox_or_hyperv_activated"])
        self.assertFalse(environment["host_security_weakened"])
        self.assertEqual(index["runner_prefix"], "ghc_family_caelen_v674_v3_")
        self.assertEqual(index["historical_aliases_deleted"], 0)
        self.assertEqual(index["global_installations"], 0)
        self.assertEqual(index["shared_or_sibling_lanes_mutated"], 0)

    def test_14_sources_are_vocabulary_only_and_frozen_trees_hold(self) -> None:
        ledger = load(FINAL / "source-status-ledger.json")
        self.assertEqual(len(ledger["entries"]), 5)
        self.assertFalse(ledger["citations_are_observations"])
        self.assertEqual(ledger["real_data_rows"], 0)
        self.assertFalse(ledger["authority_delegated"])
        changed = git(
            "diff",
            "--name-only",
            EVIDENCE,
            "--",
            "docs/caelen-ash/v674-v3/x1",
            "docs/caelen-ash/v674-v3/x2",
        )
        self.assertEqual(changed, "")


if __name__ == "__main__":
    unittest.main()
