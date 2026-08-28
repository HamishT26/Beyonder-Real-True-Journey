from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "lyren-moss" / "v673-v7"
CLOSEOUT = BASE / "closeout"
VALIDATION = BASE / "validation"
HANDOFF = BASE / "handoffs" / "ilyra-fen-v673-v8-activation-candidate.md"
SOURCE_FINAL = "7fe824e31286b3348d42103812a85e0e3e02a4c6"
X1_COMMIT = "786654cf8f28bb8c7abed41fb8f8315ab65f7e83"
EVIDENCE_COMMIT = "ea787fa029afd2b0c41108c03fd986c253b1bfc4"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_bytes(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def git(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def blob(path: str) -> bytes:
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    return git_bytes("show", f":{path}") if path in staged else git_bytes("show", f"HEAD:{path}")


class LyrenMossV673V7FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = read_json(CLOSEOUT / "terminal-summary.json")
        cls.lifecycle = read_json(CLOSEOUT / "lifecycle.json")
        cls.route = read_json(CLOSEOUT / "route-state.json")
        cls.canonical = read_json(CLOSEOUT / "canonical-plan.json")
        cls.safe = read_json(CLOSEOUT / "final-safe-task-state.json")
        cls.tools = read_json(CLOSEOUT / "tool-closeout.json")
        cls.receipt = read_json(CLOSEOUT / "build-receipt.json")
        cls.closeout_methods = read_json(CLOSEOUT / "method-flow-closeout.json")

    def test_immutable_lifecycle_anchors(self) -> None:
        self.assertEqual(git("rev-parse", f"{X1_COMMIT}^"), SOURCE_FINAL)
        self.assertEqual(git("rev-parse", f"{EVIDENCE_COMMIT}^"), X1_COMMIT)
        head = git("rev-parse", "HEAD")
        self.assertIn(head, {EVIDENCE_COMMIT, git("rev-parse", "HEAD")})
        if head != EVIDENCE_COMMIT:
            self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE_COMMIT)
            self.assertEqual(int(git("rev-list", "--count", f"{SOURCE_FINAL}..HEAD")), 3)
            self.assertEqual(git("rev-list", "--merges", f"{SOURCE_FINAL}..HEAD"), "")

    def test_closeout_is_additive_and_preserves_self_commit_truth(self) -> None:
        self.assertEqual(self.lifecycle["source"], SOURCE_FINAL)
        self.assertEqual(self.lifecycle["x1"], X1_COMMIT)
        self.assertEqual(self.lifecycle["evidence"], EVIDENCE_COMMIT)
        self.assertEqual(self.lifecycle["final"], "SELF_COMMIT_PENDING")
        self.assertEqual(self.lifecycle["new_commit_count_at_final"], 3)
        self.assertEqual(self.lifecycle["merge_count_at_final"], 0)
        self.assertTrue(self.lifecycle["one_parent_each"])
        self.assertTrue(self.lifecycle["x1_before_x2"])
        self.assertFalse(self.lifecycle["history_rewrite"])

    def test_exact_program_counts_and_terminal_verdict(self) -> None:
        self.assertEqual(self.summary["proposal_chain"], 6510)
        self.assertEqual(self.summary["outcome_counts"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(self.summary["positive_controls"], 36)
        self.assertEqual(self.summary["invalid_mutations_executed_rejected_retained"], 160)
        added = self.closeout_methods["method_count"]
        self.assertGreaterEqual(added, 1)
        self.assertEqual(self.summary["effective_negatives"], 37612 + added)
        self.assertEqual(self.summary["effective_methods"], 23820 + added)
        self.assertEqual(self.summary["retained_failed_witnesses"], 9273 + added)
        self.assertEqual(self.summary["bounded_passing_witnesses"], 11431 + added)
        self.assertEqual(self.summary["open_gaps"], 305)
        self.assertEqual(self.summary["exact_gates"], 298)
        self.assertEqual(self.summary["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(self.summary["same_owner_not_independent_reproduction"])

    def test_route_is_prepared_not_sent_and_exact(self) -> None:
        self.assertEqual(self.route["state"], "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED")
        self.assertEqual(self.route["prospective_exact_title"], "Ilyra Fen")
        self.assertEqual(self.route["prospective_phase"], "v673-v8")
        self.assertEqual(self.route["prospective_ilyra_next_title"], "Auren Lark")
        self.assertEqual(self.route["prospective_ilyra_next_phase"], "v674-v1")
        self.assertFalse(self.route["precontact_performed"])
        self.assertEqual(self.route["send_attempts"], 0)
        self.assertFalse(self.route["sent_by_lyren_moss"])
        self.assertEqual(self.route["tavian_state"], "ON_STANDBY")
        self.assertFalse(self.route["task_or_fork_created"])

    def test_activation_candidate_is_long_sanitized_and_commit_time_truthful(self) -> None:
        text = HANDOFF.read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\S+", text)), 900)
        self.assertIn("prepared_not_sent: true", text.casefold())
        self.assertIn("sent_by_lyren_moss: false", text.casefold())
        self.assertIn("Ilyra Fen", text)
        self.assertIn("Auren Lark", text)
        self.assertIn("v673-v8", text)
        self.assertIn("v674-v1", text)
        self.assertIn("through v675-v8", text)
        self.assertNotIn("sent_by_lyren_moss: true", text.casefold())

    def test_canonical_plan_is_one_shot_and_not_preclaimed(self) -> None:
        self.assertEqual(self.canonical["state"], "NOT_INVOKED_PRE_FINAL")
        self.assertEqual(self.canonical["expected_status"], "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL")
        self.assertTrue(self.canonical["exclusive_receipt_required"])
        self.assertTrue(self.canonical["one_invocation"])
        self.assertTrue(self.canonical["no_replay_after_success"])
        self.assertFalse(self.canonical["complete_repository_suite"])
        self.assertFalse(self.canonical["external_audit"])
        self.assertFalse(self.canonical["independent_reproduction"])

    def test_pending_terminal_tasks_do_not_receive_completion_credit(self) -> None:
        self.assertEqual(self.safe["safe_task_59"]["outcome"], "represented")
        self.assertEqual(self.safe["safe_task_60"]["outcome"], "represented")
        self.assertEqual(self.safe["external_actions"], 0)
        self.assertEqual(self.safe["completion_credit_for_pending_terminal_events"], 0)

    def test_tool_closeout_preserves_isolation_and_exact_versions(self) -> None:
        self.assertEqual(self.tools["wheel_count"], 8)
        self.assertEqual(self.tools["installed_versions"], {"jsonschema": "4.26.0", "networkx": "3.6.1", "rfc8785": "0.1.4"})
        self.assertTrue(self.tools["all_wheel_hashes_verified"])
        self.assertFalse(self.tools["shared_prefix_mutated"])

    def test_build_receipt_did_not_mutate_evidence_or_contact_successor(self) -> None:
        self.assertEqual(self.receipt["mode"], "additive_terminal_closeout_candidate")
        self.assertFalse(self.receipt["x1_or_x2_mutation"])
        self.assertFalse(self.receipt["successor_contact"])
        self.assertFalse(self.receipt["sent_by_lyren_moss"])
        self.assertEqual(self.receipt["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_terminal_overlay_does_not_replace_planning_index(self) -> None:
        text = (CLOSEOUT / "family-index-terminal-overlay.md").read_text(encoding="utf-8")
        self.assertIn("additive terminal overlay", text.casefold())
        self.assertIn("does not rewrite", text.casefold())
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_validator_has_exclusive_receipt_and_replay_refusal(self) -> None:
        text = (ROOT / "scripts" / "validate_ghc_family_lyren_moss_v673_v7_final.py").read_text(encoding="utf-8")
        self.assertIn("exclusive canonical receipt directory already exists; replay refused", text)
        self.assertIn("invocation_count", text)
        self.assertIn("SUCCEEDED_NO_REPLAY", text)
        self.assertIn("VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", text)

    def test_no_basic_private_identifiers_in_closeout_or_handoff(self) -> None:
        patterns = [
            re.compile(r"(?i)[A-Z]:[\\/](?:Users|GHC-Archives)[\\/]"),
            re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
            re.compile(r"(?i)(?:password|secret|token|api[_-]?key)\s*[:=]\s*['\"][^'\"]+['\"]"),
            re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
            re.compile(r"(?<!\w)\+\d[\d ()-]{7,}\d(?!\w)"),
        ]
        paths = [path for path in CLOSEOUT.rglob("*") if path.is_file()] + [HANDOFF]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertTrue(all(pattern.search(text) is None for pattern in patterns))

    def test_all_closeout_json_parses_utf8(self) -> None:
        paths = sorted(CLOSEOUT.glob("*.json"))
        self.assertEqual(len(paths), 8)
        for path in paths:
            self.assertIsInstance(read_json(path), dict)

    def test_conditional_final_staged_receipts(self) -> None:
        paths = [
            VALIDATION / "final-staged-review.json",
            VALIDATION / "final-staged-privacy.json",
            VALIDATION / "final-staged-security.json",
        ]
        if not any(path.exists() for path in paths):
            self.skipTest("final staged receipts are generated after the first focused pass")
        self.assertTrue(all(path.exists() for path in paths))
        review, privacy, security = (read_json(path) for path in paths)
        self.assertTrue(review["passed"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["immutable_x1_x2_paths"], [])
        self.assertEqual(review["deletions"], [])
        self.assertTrue(privacy["passed"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(security["passed"])
        self.assertEqual(security["bounded_ast_finding_count"], 0)

    def test_conditional_final_manifests_and_content_seal_replay(self) -> None:
        paths = [
            VALIDATION / "final-delta-manifest.json",
            VALIDATION / "final-owner-manifest.json",
            VALIDATION / "final-content-seal.json",
        ]
        if not any(path.exists() for path in paths):
            self.skipTest("final manifests are generated after staged review")
        self.assertTrue(all(path.exists() for path in paths))
        for path in paths:
            document = read_json(path)
            self.assertEqual(document["entry_count"], len(document["entries"]))
            for row in document["entries"]:
                data = normalized(blob(row["path"]))
                with self.subTest(manifest=path.name, entry=row["path"]):
                    self.assertEqual(row["bytes"], len(data))
                    self.assertEqual(row["sha256_normalized_lf"], hashlib.sha256(data).hexdigest())
        delta = read_json(paths[0])
        self.assertFalse(any(row["path"].startswith(("docs/lyren-moss/v673-v7/x1/", "docs/lyren-moss/v673-v7/x2/")) for row in delta["entries"]))
        owner = read_json(paths[1])
        self.assertTrue(owner["within_file_ceiling"])
        self.assertLess(owner["entry_count"] + len(owner["self_exclusions"]), owner["file_ceiling"])


if __name__ == "__main__":
    unittest.main()
