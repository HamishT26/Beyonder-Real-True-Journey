from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "lyren-moss" / "v675-v6"
FINAL = BASE / "final"
VALIDATION = BASE / "validation"
CLOSEOUT = BASE / "closeout"
BATON = BASE / "handoffs" / "ilyra-fen-v675-v7-activation-candidate.md"
SOURCE_FINAL = "0aa1f2b1250e5540650b683d221f92e8762cd991"
X1_COMMIT = "920c8e89dff0c4625087a52a3dc5ee2916b0b659"
EVIDENCE_COMMIT = "78b4cbd6bc91cc422d99497bbb4b59e5dfac9eb6"
BRANCH = "codex/GHC-Family/lyren-moss-v675-v6-full-tools"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class LyrenV675V6FinalTests(unittest.TestCase):
    def test_lifecycle_head_is_evidence_or_direct_final_child(self) -> None:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
        self.assertEqual(BRANCH, branch)
        self.assertEqual(0, subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE_COMMIT, head], cwd=ROOT).returncode)
        count = int(subprocess.check_output(["git", "rev-list", "--count", f"{EVIDENCE_COMMIT}..{head}"], cwd=ROOT, text=True).strip())
        self.assertLessEqual(count, 1)
        self.assertEqual(X1_COMMIT, subprocess.check_output(["git", "rev-parse", f"{EVIDENCE_COMMIT}^"], cwd=ROOT, text=True).strip())
        self.assertEqual(SOURCE_FINAL, subprocess.check_output(["git", "rev-parse", f"{X1_COMMIT}^"], cwd=ROOT, text=True).strip())

    def test_final_json_and_closeout_json_parse(self) -> None:
        paths = list(FINAL.glob("*.json")) + list(CLOSEOUT.glob("*.json"))
        paths += list(VALIDATION.glob("final-*.json"))
        self.assertGreaterEqual(len(paths), 15)
        for path in paths:
            with self.subTest(path=path.name):
                json.loads(path.read_text(encoding="utf-8"))

    def test_exact_core_outcomes_and_labels(self) -> None:
        truth = load(FINAL / "phase-truth.json")
        self.assertEqual(ALLOWED, set(truth["allowed_outcome_labels"]))
        self.assertEqual({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}, truth["outcomes"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])

    def test_final_working_truth(self) -> None:
        truth = load(FINAL / "phase-truth.json")["sealed_working_truth"]
        self.assertEqual(41113, truth["effective_negatives"])
        self.assertEqual(29405, truth["method_flow_methods"])
        self.assertEqual(12774, truth["failed_witnesses"])
        self.assertEqual(16856, truth["bounded_passing_witnesses"])
        self.assertEqual(341, truth["open_gaps"])
        self.assertEqual(333, truth["exact_gates"])
        self.assertEqual(7270, truth["declared_proposals"])

    def test_retained_negative_arithmetic(self) -> None:
        data = load(FINAL / "retained-negative-register.json")
        self.assertEqual(40947, data["source_repository_negatives"])
        self.assertEqual(40948, data["source_activation_overlay_negatives"])
        self.assertEqual(5, data["lyren_operational_failures"])
        self.assertEqual(160, data["lyren_invalid_mutations"])
        self.assertEqual(41113, data["final_effective_negatives"])
        self.assertEqual(0, data["failures_erased"])

    def test_open_and_exact_gates(self) -> None:
        data = load(FINAL / "open-exact-gate-register.json")
        self.assertEqual(341, data["open_gaps"])
        self.assertEqual(333, data["exact_gates"])
        self.assertEqual(2, len(data["phase_open_gaps"]))
        self.assertEqual(2, len(data["phase_exact_gates"]))

    def test_baton_word_floor_and_commit_time_markers(self) -> None:
        text = BATON.read_text(encoding="utf-8")
        words = len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))
        self.assertGreaterEqual(words, 10_000)
        self.assertLessEqual(words, 100_000)
        self.assertIn("PREPARED_NOT_SENT = true", text)
        self.assertIn("sent_by_lyren_moss: false", text)
        self.assertIn("SENT_BY_LYREN_MOSS = false", text)
        self.assertIn("Ilyra Fen", text)
        self.assertIn("v675-v7", text)

    def test_route_state_is_prepared_not_sent(self) -> None:
        route = load(FINAL / "route-state.json")
        self.assertEqual("PREPARED_NOT_SENT", route["state"])
        self.assertEqual("Ilyra Fen", route["prospective_successor"])
        self.assertEqual("v675-v7", route["prospective_phase"])
        self.assertFalse(route["precontacted"])
        self.assertFalse(route["sent_by_lyren_moss"])
        self.assertFalse(route["delivery_acknowledged"])

    def test_closeout_receipt_does_not_claim_precommit_canonical_success(self) -> None:
        receipt = load(CLOSEOUT / "closeout-receipt.json")
        self.assertEqual("commit_containing_this_receipt", receipt["exact_final"])
        self.assertFalse(receipt["canonical_validation_invoked"])
        self.assertFalse(receipt["canonical_success_claimed"])
        self.assertFalse(receipt["successor_contacted"])
        self.assertFalse(receipt["sent_by_lyren_moss"])
        self.assertGreaterEqual(receipt["baton_words"], 10_000)

    def test_final_delta_manifest_replays_index(self) -> None:
        manifest = load(VALIDATION / "final-delta-manifest.json")
        self.assertGreaterEqual(manifest["entry_count"], 14)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(6, len(manifest["self_exclusions"]))
        for entry in manifest["entries"]:
            with self.subTest(path=entry["path"]):
                row = subprocess.check_output(["git", "ls-files", "-s", "--", entry["path"]], cwd=ROOT, text=True).split()
                self.assertEqual(entry["git_blob"], row[1])
                blob = subprocess.check_output(["git", "cat-file", "blob", row[1]], cwd=ROOT)
                self.assertEqual(entry["sha256"], hashlib.sha256(blob).hexdigest())

    def test_final_owner_manifest_replays_evidence_and_index(self) -> None:
        manifest = load(VALIDATION / "final-owner-manifest.json")
        self.assertEqual(119, manifest["immutable_entry_count"])
        self.assertEqual(manifest["immutable_entry_count"] + manifest["final_delta_entry_count"], manifest["total_manifest_entries"])
        for entry in manifest["immutable_entries"]:
            with self.subTest(immutable=entry["path"]):
                oid = subprocess.check_output(["git", "rev-parse", f"{EVIDENCE_COMMIT}:{entry['path']}"], cwd=ROOT, text=True).strip()
                self.assertEqual(entry["git_blob"], oid)
        for entry in manifest["final_delta_entries"]:
            with self.subTest(final=entry["path"]):
                oid = subprocess.check_output(["git", "ls-files", "-s", "--", entry["path"]], cwd=ROOT, text=True).split()[1]
                self.assertEqual(entry["git_blob"], oid)

    def test_content_seal_replays_delta(self) -> None:
        seal = load(CLOSEOUT / "content-seal.json")
        self.assertEqual(seal["entry_count"], len(seal["entries"]))
        self.assertGreaterEqual(seal["baton_words"], 10_000)
        for entry in seal["entries"]:
            oid = subprocess.check_output(["git", "ls-files", "-s", "--", entry["path"]], cwd=ROOT, text=True).split()[1]
            self.assertEqual(entry["git_blob"], oid)

    def test_final_staged_review_and_privacy(self) -> None:
        review = load(VALIDATION / "final-staged-review.json")
        privacy = load(VALIDATION / "final-staged-privacy.json")
        self.assertEqual(0, review["deletions"])
        self.assertEqual(0, review["renames"])
        self.assertEqual(0, review["confirmed_privacy_hits"])
        self.assertTrue(review["within_file_ceiling"])
        self.assertTrue(review["within_commit_ceiling"])
        self.assertFalse(review["canonical_aggregate_invoked"])
        self.assertEqual(0, privacy["confirmed_hit_count"])
        self.assertFalse(privacy["complete_privacy_claim"])

    def test_accessible_report_keeps_scope_boundary(self) -> None:
        text = (FINAL / "accessible-report.html").read_text(encoding="utf-8")
        for token in ("<main", "<h1>", "<h2>", "<caption>", "scope=\"col\"", "Skip to main content", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, text)
        self.assertIn("not an affected-user accessibility evaluation", text)

    def test_complete_incomplete_checklist(self) -> None:
        data = load(FINAL / "complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(data["completed_local"]), 10)
        self.assertGreaterEqual(len(data["incomplete_or_protected"]), 7)
        self.assertFalse(data["terminal_ready"])

    def test_no_private_material_in_owner_docs(self) -> None:
        forbidden = ("source_thread_id", "clientThreadId", "threadId", "C:\\Users\\", "D:\\GHC-Archives\\", "api_key", "access_token", "refresh_token", "OMEGA44TOKEN-")
        paths = [path for path in BASE.rglob("*") if path.is_file() and path.suffix.lower() in {".json", ".md", ".html"}]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                with self.subTest(path=path.name, token=token):
                    self.assertNotIn(token, text)

    def test_no_crlf_in_final_delta_text(self) -> None:
        paths = [path for path in FINAL.rglob("*") if path.is_file()]
        paths += [BATON, CLOSEOUT / "closeout-receipt.json", CLOSEOUT / "content-seal.json"]
        paths += [VALIDATION / name for name in ("final-delta-manifest.json", "final-owner-manifest.json", "final-staged-review.json", "final-staged-privacy.json")]
        paths += [ROOT / "scripts" / "build_ghc_family_lyren_moss_v675_v6_final.py", ROOT / "scripts" / "validate_ghc_family_lyren_moss_v675_v6_final.py", ROOT / "tests" / "test_ghc_family_lyren_moss_v675_v6_final.py"]
        for path in paths:
            with self.subTest(path=path.name):
                self.assertNotIn(b"\r\n", path.read_bytes())

    def test_changed_python_ast_parses(self) -> None:
        paths = [ROOT / "scripts" / "build_ghc_family_lyren_moss_v675_v6_final.py", ROOT / "scripts" / "validate_ghc_family_lyren_moss_v675_v6_final.py", ROOT / "tests" / "test_ghc_family_lyren_moss_v675_v6_final.py"]
        for path in paths:
            with self.subTest(path=path.name):
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_owner_file_and_commit_ceilings(self) -> None:
        owner_files = [path for path in BASE.rglob("*") if path.is_file()]
        owner_files += list((ROOT / "scripts").glob("*lyren_moss_v675_v6*.py"))
        owner_files += list((ROOT / "tests").glob("*lyren_moss_v675_v6*.py"))
        self.assertLess(len(owner_files), 2000)
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        commits = int(subprocess.check_output(["git", "rev-list", "--count", f"{SOURCE_FINAL}..{head}"], cwd=ROOT, text=True).strip())
        self.assertLessEqual(commits + (1 if head == EVIDENCE_COMMIT else 0), 8)

    def test_validation_plan_is_owner_scoped_not_independent(self) -> None:
        plan = load(FINAL / "validation-plan.json")
        self.assertIn("exact Lyren", plan["scope"])
        self.assertFalse(plan["full_repository_suite"])
        self.assertFalse(plan["independent_reproduction"])
        self.assertFalse(plan["external_audit"])
        self.assertTrue(plan["one_success_no_replay"])

    def test_boundary_language(self) -> None:
        overview = (FINAL / "integrated-overview.md").read_text(encoding="utf-8")
        self.assertIn("relational identity and family language", overview.casefold())
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)
        self.assertIn("not universal novelty proof", BATON.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
