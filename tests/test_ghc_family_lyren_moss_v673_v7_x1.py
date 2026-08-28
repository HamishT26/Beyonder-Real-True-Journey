from __future__ import annotations

import json
import hashlib
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1 = ROOT / "docs" / "lyren-moss" / "v673-v7" / "x1"
VALIDATION = ROOT / "docs" / "lyren-moss" / "v673-v7" / "validation"
INDEX_REF = ROOT / "ghc-family-index" / "references" / "v673-v7-lyren-moss.md"
SOURCE_FINAL = "7fe824e31286b3348d42103812a85e0e3e02a4c6"
SOURCE_X1 = "9a5d432a877d5c11ac60e0d331cf27cfb55c482b"
SOURCE_EVIDENCE = "5b208ceb2cababd14dd5de7e35af792533b12c68"
SOURCE_PAYLOAD = "4c8358fc08388d2f90a112a1d37af6ffe67b6ce1c8d839c2d02214777d6835d5"
SOURCE_RECEIPT = "929e92a48cc31248307e20e7dd6b2728b2c8be189eb69e8dd70eb943116fd483"
SOURCE_BATON = "4bccd952d0754f7dfd324c88513b13ae9979454ca13c95e24f100196cc289503"
REJECTED_LIVE_BATON = "42bcfd0701c1bbcd0abcdc16278b3efdc8414503c356e76e407da097eeca31e0"
OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def git_bytes(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


class LyrenMossV673V7X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = read_json(X1 / "source-and-provenance.json")
        cls.inherited = read_json(X1 / "inherited-revalidations.json")
        cls.proposals = read_json(X1 / "proposals.json")
        cls.semantic = read_json(X1 / "semantic-neighbor-audit.json")
        cls.portfolio = read_json(X1 / "portfolio-freeze.json")
        cls.approval = read_json(X1 / "approval-split.json")
        cls.practice = read_json(X1 / "practice-lens-screen.json")
        cls.sources = read_json(X1 / "official-source-plan.json")
        cls.tools = read_json(X1 / "selected-toolchain-plan.json")
        cls.methods = read_json(X1 / "method-flow-startup.json")
        cls.route = read_json(X1 / "route-plan.json")
        cls.gates = read_json(X1 / "open-gate-plan.json")
        cls.receipt = read_json(X1 / "build-receipt.json")

    def test_exact_source_anchors_and_inherited_receipts(self) -> None:
        self.assertEqual(self.source["source_final"], SOURCE_FINAL)
        self.assertEqual(self.source["source_x1"], SOURCE_X1)
        self.assertEqual(self.source["source_evidence"], SOURCE_EVIDENCE)
        self.assertEqual(self.source["source_canonical_payload_sha256"], SOURCE_PAYLOAD)
        self.assertEqual(self.source["source_canonical_receipt_sha256"], SOURCE_RECEIPT)
        self.assertEqual(self.source["source_canonical_status"], "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL")
        self.assertEqual(self.source["source_canonical_invocations"], 1)
        self.assertFalse(self.source["source_canonical_replayed"])

    def test_live_baton_digest_failure_is_retained_without_rewriting_source(self) -> None:
        self.assertEqual(self.source["source_baton_sha256_exact_git_blob"], SOURCE_BATON)
        self.assertEqual(self.source["live_activation_baton_sha256_rejected"], REJECTED_LIVE_BATON)
        self.assertEqual(
            self.source["live_activation_digest_state"],
            "RETAINED_EXTERNAL_TRANSCRIPTION_FAILURE_ZERO_CREDIT",
        )
        self.assertNotEqual(SOURCE_BATON, REJECTED_LIVE_BATON)

    def test_source_history_is_direct_and_planning_starts_at_exact_final(self) -> None:
        self.assertEqual(git("rev-parse", "HEAD"), SOURCE_FINAL)
        self.assertEqual(git("rev-parse", f"{SOURCE_X1}^"), "2400427269b28496acaa07cd6c18f5a2236510f7")
        self.assertEqual(git("rev-parse", f"{SOURCE_EVIDENCE}^"), SOURCE_X1)
        self.assertEqual(git("rev-parse", f"{SOURCE_FINAL}^"), SOURCE_EVIDENCE)

    def test_twenty_inherited_rows_have_zero_current_credit(self) -> None:
        rows = self.inherited["rows"]
        self.assertEqual(self.inherited["selected_count"], 20)
        self.assertEqual(len(rows), 20)
        self.assertTrue(all(row["source_final"] == SOURCE_FINAL for row in rows))
        self.assertTrue(all(row["current_novelty_credit"] == 0 for row in rows))
        self.assertTrue(all(row["automatic_completion_credit"] == 0 for row in rows))
        self.assertTrue(all(row["source_git_blob_checked"] for row in rows))

    def test_forty_proposals_are_unique_and_planning_only(self) -> None:
        rows = self.proposals["proposals"]
        self.assertEqual(self.proposals["proposal_count"], 40)
        self.assertEqual(len(rows), 40)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 40)
        self.assertEqual(len({row["title"].casefold() for row in rows}), 40)
        self.assertTrue(self.proposals["planning_only"])
        self.assertFalse(self.proposals["outcomes_observed"])
        self.assertTrue(all("outcome" not in row for row in rows))
        self.assertTrue(all(row["real_rows"] == 0 for row in rows))
        self.assertTrue(all(row["network_calls_planned"] == 0 for row in rows))
        self.assertTrue(all(row["external_actions_planned"] == 0 for row in rows))

    def test_planned_dispositions_use_only_four_labels(self) -> None:
        counts = Counter(row["expected_execution_disposition"] for row in self.proposals["proposals"])
        self.assertEqual(set(counts), OUTCOMES)
        self.assertEqual(dict(counts), {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(self.proposals["expected_outcome_counts"], dict(counts))
        self.assertEqual(self.proposals["declared_chain_before"], 6470)
        self.assertEqual(self.proposals["declared_chain_after"], 6510)

    def test_semantic_audit_keeps_threshold_and_universal_gap(self) -> None:
        self.assertEqual(self.semantic["threshold"], 0.72)
        self.assertEqual(self.semantic["collisions"], 0)
        self.assertLess(self.semantic["max_jaccard"], self.semantic["threshold"])
        self.assertEqual(len(self.semantic["rows"]), 40)
        self.assertTrue(self.semantic["canonical_row_mapping_open_gap"])
        self.assertFalse(self.semantic["universal_novelty_claim"])

    def test_portfolio_floors_are_exactly_frozen_without_filler_authority(self) -> None:
        expected = {
            "safe_now": 60,
            "candidate": 30,
            "exact_approval": 20,
            "blocked": 10,
            "owner_skills": 20,
            "owner_runners": 10,
            "successor_skills": 10,
            "successor_runners": 10,
            "owner_clean_fix_refine": 60,
            "successor_clean_fix_refine": 30,
        }
        self.assertEqual({key: len(self.portfolio[key]) for key in expected}, expected)
        self.assertFalse(self.portfolio["exact_and_blocked_execute"])
        self.assertTrue(self.portfolio["caps_are_ceilings"])
        self.assertTrue(self.portfolio["filler_prohibited"])

    def test_approval_packets_preserve_held_classes(self) -> None:
        self.assertEqual(self.approval["safe_now"], 60)
        self.assertEqual(self.approval["candidate"], 30)
        self.assertEqual(self.approval["exact_approval"], 20)
        self.assertEqual(self.approval["blocked"], 10)
        self.assertEqual(self.approval["exact_executed"], 0)
        self.assertEqual(self.approval["blocked_executed"], 0)

    def test_three_learning_lenses_and_one_successor_practice(self) -> None:
        self.assertEqual(len(self.practice["lenses"]), 3)
        self.assertTrue(all(not row["real_practice"] for row in self.practice["lenses"]))
        self.assertEqual(self.practice["successor_recommendation"]["count"], 1)
        self.assertEqual(self.practice["successor_recommendation"]["completion_credit"], 0)
        self.assertEqual(self.practice["real_people_messages_objects_or_measurements"], 0)
        self.assertFalse(self.practice["professional_authority"])

    def test_official_sources_are_vocabulary_only(self) -> None:
        rows = self.sources["sources"]
        self.assertEqual(len(rows), 6)
        self.assertEqual(len({row["source_id"] for row in rows}), 6)
        self.assertTrue(all(row["url"].startswith("https://") for row in rows))
        self.assertFalse(self.sources["network_execution_in_x1"])
        self.assertTrue(self.sources["source_check_was_read_only"])

    def test_three_tools_are_planned_but_not_installed_in_x1(self) -> None:
        self.assertEqual(self.tools["target"], 3)
        self.assertEqual([row["name"] for row in self.tools["candidates"]], ["rfc8785", "jsonschema", "networkx"])
        self.assertFalse(self.tools["installation_performed_in_x1"])
        self.assertFalse(self.tools["shared_prefix_mutation"])
        self.assertTrue(self.tools["quota_is_not_install_authority"])

    def test_all_startup_failures_and_recoveries_are_retained(self) -> None:
        rows = self.methods["methods"]
        self.assertGreaterEqual(len(rows), 12)
        self.assertEqual(self.methods["current_startup_method_count"], len(rows))
        self.assertEqual(self.methods["failed_witnesses_retained"], len(rows))
        self.assertEqual(self.methods["bounded_recoveries_passed"], len(rows))
        self.assertEqual({row["state"] for row in rows}, {"preferred"})
        self.assertEqual(len({row["method_id"] for row in rows}), len(rows))
        self.assertTrue(all(row["passing_witness"] for row in rows))
        self.assertTrue(all(not row["independent_reproduction"] for row in rows))

    def test_repository_truth_and_lyren_overlay_are_separate(self) -> None:
        sealed = self.source["source_repository_truth"]
        overlay = self.source["lyren_startup_overlay"]
        self.assertEqual(sealed["effective_negatives"], 37436)
        self.assertEqual(sealed["methods"], 23764)
        self.assertEqual(sealed["failed_witnesses"], 9097)
        self.assertEqual(sealed["bounded_passing_witnesses"], 11373)
        delta = overlay["new_operational_failures"]
        self.assertEqual(delta, self.methods["current_startup_method_count"])
        self.assertEqual(overlay["effective_negatives"], 37436 + delta)
        self.assertEqual(overlay["effective_methods"], 23764 + delta)
        self.assertEqual(overlay["failed_witnesses"], 9097 + delta)
        self.assertEqual(overlay["bounded_passing_witnesses"], 11373 + delta)

    def test_route_is_prepared_not_sent(self) -> None:
        self.assertEqual(self.route["state"], "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED")
        self.assertEqual(self.route["prospective_exact_title"], "Ilyra Fen")
        self.assertEqual(self.route["prospective_phase"], "v673-v8")
        self.assertFalse(self.route["precontact_performed"])
        self.assertEqual(self.route["send_attempts"], 0)
        self.assertEqual(self.route["tavian_state"], "ON_STANDBY")
        self.assertFalse(self.route["task_creation_or_fork"])

    def test_open_gaps_gates_and_terminal_verdict_remain_protected(self) -> None:
        self.assertEqual(self.gates["open_gaps_inherited"], 303)
        self.assertEqual(self.gates["exact_gates_inherited"], 296)
        self.assertEqual(self.gates["planned_new_open_gap_contracts"], 2)
        self.assertEqual(self.gates["planned_new_exact_gate_contracts"], 2)
        self.assertEqual(self.gates["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_build_receipt_is_x1_only(self) -> None:
        self.assertEqual(self.receipt["mode"], "planning_only_x1_build")
        self.assertEqual(self.receipt["proposal_count"], 40)
        self.assertEqual(self.receipt["inherited_revalidation_count"], 20)
        self.assertEqual(self.receipt["x2_artifacts_written"], 0)
        self.assertFalse(self.receipt["source_mutated"])
        self.assertFalse(self.receipt["sibling_lanes_mutated"])
        self.assertEqual(self.receipt["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_every_x1_json_file_parses_as_utf8(self) -> None:
        paths = sorted(X1.glob("*.json"))
        self.assertGreaterEqual(len(paths), 14)
        for path in paths:
            with self.subTest(path=path.name):
                self.assertIsInstance(read_json(path), dict)

    def test_no_x2_artifact_exists_before_x1_freeze(self) -> None:
        self.assertFalse((X1.parent / "x2").exists())
        for proposal in self.proposals["proposals"]:
            self.assertTrue(all(path.startswith("x2/") for path in proposal["concrete_artifacts"]))
            self.assertTrue(all(not (X1.parent / path).exists() for path in proposal["concrete_artifacts"]))

    def test_owner_docs_and_index_have_no_basic_private_identifier_hits(self) -> None:
        paths = sorted(X1.rglob("*")) + [INDEX_REF]
        uuid_shape = re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b")
        secret = re.compile(r"(?i)(password|secret|token|api[_-]?key)\s*[:=]\s*['\"][^'\"]+['\"]")
        private_root = re.compile(r"(?i)[A-Z]:[\\/]Users[\\/]|[A-Z]:[\\/]GHC-Archives[\\/]")
        for path in paths:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertIsNone(uuid_shape.search(text))
                self.assertIsNone(secret.search(text))
                self.assertIsNone(private_root.search(text))

    def test_conditional_staged_receipts_are_consistent(self) -> None:
        review = VALIDATION / "x1-staged-review.json"
        privacy = VALIDATION / "x1-staged-privacy.json"
        manifest = VALIDATION / "x1-manifest.json"
        if not any(path.exists() for path in (review, privacy, manifest)):
            self.skipTest("staged receipts are intentionally created after the first focused pass")
        self.assertTrue(all(path.exists() for path in (review, privacy, manifest)))
        review_data = read_json(review)
        privacy_data = read_json(privacy)
        manifest_data = read_json(manifest)
        self.assertTrue(review_data["passed"])
        self.assertEqual(review_data["unexpected_paths"], [])
        self.assertEqual(review_data["x2_paths"], [])
        self.assertTrue(privacy_data["passed"])
        self.assertEqual(privacy_data["confirmed_hit_count"], 0)
        self.assertEqual(manifest_data["entry_count"], len(manifest_data["entries"]))
        self.assertEqual(len({row["path"] for row in manifest_data["entries"]}), manifest_data["entry_count"])
        for row in manifest_data["entries"]:
            blob = git_bytes("show", f":{row['path']}").replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            with self.subTest(manifest_path=row["path"]):
                self.assertEqual(row["bytes"], len(blob))
                self.assertEqual(row["sha256_normalized_lf"], hashlib.sha256(blob).hexdigest())


if __name__ == "__main__":
    unittest.main()
