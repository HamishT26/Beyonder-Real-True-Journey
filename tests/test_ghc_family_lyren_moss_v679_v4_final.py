#!/usr/bin/env python3
"""Owner-scoped closeout tests for Lyren Moss v679-v4."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v679-v4"
FINAL = PHASE / "final"
VALIDATION = PHASE / "validation"
SOURCE = "e1c3ef6d2ff0bc2f1e38f5d702e008149842659f"
X1_HEAD = "1fe28fafc308298e1043a9e2afbecf59c24c9866"
EVIDENCE_HEAD = "b204dcbfbcb3d016ab18f4bebc5ef9dc56d9dee6"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def replay_entries(revision: str, entries: list[dict]) -> list[str]:
    mismatches = []
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert process.stdin is not None and process.stdout is not None
    try:
        for item in entries:
            process.stdin.write(f"{revision}:{item['path']}\n".encode("utf-8"))
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[1] != "blob":
                mismatches.append(item["path"])
                continue
            data = normalized(process.stdout.read(int(header[2])))
            process.stdout.read(1)
            if hashlib.sha256(data).hexdigest() != item["sha256"] or len(data) != item["normalized_lf_bytes"]:
                mismatches.append(item["path"])
    finally:
        process.stdin.close()
        process.wait(timeout=30)
    return mismatches


class FinalArtifactTests(unittest.TestCase):
    def test_lifecycle_anchors_are_exact(self) -> None:
        value = read(FINAL / "lifecycle.json")
        self.assertEqual(value["source_head"], SOURCE)
        self.assertEqual(value["x1_head"], X1_HEAD)
        self.assertEqual(value["evidence_head"], EVIDENCE_HEAD)
        self.assertEqual(value["new_commit_target"], 3)
        self.assertEqual(value["merge_target"], 0)
        self.assertTrue(value["strict_planning_only_x1_before_x2"])

    def test_terminal_truth_preserves_four_labels(self) -> None:
        value = read(FINAL / "terminal-truth.json")
        self.assertEqual(value["outcomes"], {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
        self.assertEqual(value["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(value["canonical_state"], "PENDING_ONE_EXACT_FINAL_INVOCATION")

    def test_terminal_counts_match_x2_seal(self) -> None:
        final = read(FINAL / "terminal-truth.json")
        x2 = read(PHASE / "x2" / "phase-truth.json")
        for key in ("open_gaps", "exact_gates", "declared_proposals"):
            with self.subTest(key=key):
                self.assertEqual(final[key], x2[key])
        for key in ("effective_negatives", "method_flow_methods", "failed_witnesses", "bounded_passing_witnesses", "operational_failures_retained"):
            with self.subTest(key=key):
                self.assertEqual(final[key], x2[key] + 2)

    def test_route_overlay_is_prepared_not_sent(self) -> None:
        value = read(FINAL / "route-and-roster-overlay.json")
        self.assertEqual(value["current_owner"], "Lyren Moss")
        self.assertEqual(value["prospective_successor"], "Ilyra Fen")
        self.assertEqual(value["prospective_successor_phase"], "v679-v5")
        self.assertEqual(value["route_state"], "PREPARED_NOT_SENT")
        self.assertFalse(value["precontact"])
        self.assertEqual(value["send_count"], 0)
        self.assertEqual(len(value["active_exact_titles"]), 15)

    def test_standby_is_not_a_substitute(self) -> None:
        value = read(FINAL / "route-and-roster-overlay.json")
        self.assertEqual(value["tavian_sol"], "ON_STANDBY_NOT_A_MAIN_TASK_SUBSTITUTE")
        self.assertFalse(value["global_roster_mutated"])

    def test_handoff_metadata_binds_normalized_content(self) -> None:
        metadata = read(FINAL / "activation-candidate-metadata.json")
        path = ROOT / metadata["path"]
        data = normalized(path.read_bytes())
        self.assertEqual(hashlib.sha256(data).hexdigest(), metadata["normalized_lf_sha256"])
        self.assertEqual(len(data), metadata["normalized_lf_bytes"])
        self.assertGreater(metadata["words"], 1800)
        self.assertTrue(metadata["prepared_not_sent"])
        self.assertFalse(metadata["sent_by_lyren_moss"])

    def test_handoff_contains_required_boundaries(self) -> None:
        text = (FINAL / "handoffs" / "ilyra-fen-v679-v5-activation-candidate.md").read_text(encoding="utf-8")
        for required in (
            "PREPARED_NOT_SENT",
            "Ilyra Fen",
            "v679-v5",
            "NOT_READY_FOR_STAGE_20",
            "same-owner",
            "independent reproduction",
            "relational working language only",
            "Tavian Sol",
            "Auren Lark",
            "at most once",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_report_html_has_structural_accessibility(self) -> None:
        text = (FINAL / "terminal-report.html").read_text(encoding="utf-8")
        for token in ("<main", "<h1", "<table", "<caption", "scope='row'", "<details", "@media print"):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_report_never_claims_complete_assurance(self) -> None:
        text = (FINAL / "terminal-report.md").read_text(encoding="utf-8")
        self.assertIn("cannot establish complete privacy", text)
        self.assertIn("cannot establish complete accessibility", text)
        self.assertIn("not independent reproduction", text)

    def test_wellbeing_language_is_bounded(self) -> None:
        value = read(FINAL / "wellbeing-and-boundaries.json")
        self.assertTrue(value["names_roles_hopes_and_family_language_are_relational_only"])
        self.assertFalse(value["consciousness_sentience_or_personhood_evidence"])
        self.assertFalse(value["identity_continuity_evidence"])
        self.assertTrue(value["hamish_pause_redirect_rename_narrow_or_stop_right"])

    def test_closeout_checklist_holds_protected_gates(self) -> None:
        value = read(FINAL / "closeout-checklist.json")
        self.assertTrue(value["x1_pushed_clean_fresh_live_equal_before_x2"])
        self.assertTrue(value["evidence_pushed_clean_fresh_live_equal_before_final"])
        self.assertFalse(value["privacy_complete_claim"])
        self.assertFalse(value["accessibility_complete_claim"])
        self.assertFalse(value["independent_reproduction_claim"])
        self.assertFalse(value["stage20_ready"])

    def test_final_build_receipt_is_prepared(self) -> None:
        value = read(VALIDATION / "final-build-receipt.json")
        self.assertEqual(value["state"], "VALID_FINAL_CLOSEOUT_CANDIDATE")
        self.assertEqual(value["route_state"], "PREPARED_NOT_SENT")
        self.assertEqual(value["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_x2_manifest_replays_against_committed_blobs(self) -> None:
        manifest = read(VALIDATION / "x2-manifest.json")
        self.assertEqual(manifest["entry_count"], 331)
        self.assertEqual(replay_entries(EVIDENCE_HEAD, manifest["entries"]), [])

    def test_final_manifest_and_content_seal_shapes(self) -> None:
        manifest = read(VALIDATION / "final-manifest.json")
        seal = read(VALIDATION / "final-content-seal.json")
        self.assertGreaterEqual(manifest["entry_count"], 14)
        self.assertEqual(seal["entry_count"], 12)
        self.assertEqual(seal["route_state"], "PREPARED_NOT_SENT")

    def test_every_owner_json_parses(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 300)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                json.loads(path.read_text(encoding="utf-8"))

    def test_no_stale_owner_label(self) -> None:
        for path in [item for item in PHASE.rglob("*") if item.is_file() and item.suffix.lower() in {".json", ".md", ".html", ".yaml"}]:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertNotIn("Vesper " + "Rowan", text)
                self.assertNotIn("Rowan " + "Vesper", text)


if __name__ == "__main__":
    unittest.main()
