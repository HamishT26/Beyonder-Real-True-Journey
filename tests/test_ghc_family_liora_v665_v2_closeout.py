from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/liora-venn/v665-v2"
BUILDER_PATH = ROOT / "scripts/build_ghc_family_v665_v2_closeout.py"
SOURCE = "f4abecafb107f4ac840c09b46a6b30079171816d"
X1 = "1a5fe2e58c3e9fa3ae51a04d0971f30106cbcf38"
EVIDENCE = "420f73d2bb5c7570a886cd04a37d81bf03449bf2"
BRANCH = "codex/GHC-Family/liora-venn-v665-v2-full-tools"


def load_builder():
    spec = importlib.util.spec_from_file_location("liora_v665_v2_closeout_builder", BUILDER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(*args: str, check: bool = True) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=check
    ).stdout.strip()


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def committed(path: str) -> bytes:
    return subprocess.run(["git", "show", f"HEAD:{path}"], cwd=ROOT, capture_output=True, check=True).stdout


def indexed(path: str) -> bytes:
    return subprocess.run(["git", "show", f":{path}"], cwd=ROOT, capture_output=True, check=True).stdout


class LioraV665V2CloseoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = load_builder()
        cls.head = git("rev-parse", "HEAD")
        cls.staged_mode = cls.head == EVIDENCE

    def bytes_for_final_entry(self, path: str) -> bytes:
        return indexed(path) if self.staged_mode and path in self.builder.INTENDED_PATHS else committed(path)

    def test_01_immutable_lifecycle_anchors(self) -> None:
        self.assertEqual(git("branch", "--show-current"), BRANCH)
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), X1)
        self.assertEqual(int(git("rev-list", "--count", "--merges", f"{SOURCE}..{EVIDENCE}")), 0)

    def test_02_closeout_is_staged_or_direct_final_child(self) -> None:
        if self.staged_mode:
            self.assertEqual(sorted(git("diff", "--cached", "--name-only").splitlines()), self.builder.INTENDED_PATHS)
        else:
            self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE)
            self.assertEqual(len(git("show", "-s", "--format=%P", "HEAD").split()), 1)
            self.assertEqual(int(git("rev-list", "--count", f"{SOURCE}..HEAD")), 3)
            self.assertEqual(int(git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD")), 0)

    def test_03_phase_truth_is_exact_and_bounded(self) -> None:
        truth = read("closeout/phase-truth.json")
        self.assertTrue(truth["valid"])
        self.assertEqual(truth["frozen_proposal_chain"], 4_050)
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["mutations"], {"preregistered": 100, "executed": 100, "rejected": 100, "accepted": 0})
        self.assertEqual(truth["effective_negatives"], 25_307)
        self.assertEqual(truth["effective_method_flow_methods"], 9_169)
        self.assertEqual(truth["open_gaps"], 176)
        self.assertEqual(truth["exact_gates"], 174)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_04_method_flow_retains_every_failure(self) -> None:
        flow = read("closeout/method-flow-final.json")
        self.assertTrue(flow["valid"])
        self.assertEqual(flow["startup"], {"failed_witnesses": 13, "bounded_recoveries": 13})
        self.assertEqual(flow["x2_mutations"], {"failed_witnesses": 100, "bounded_recoveries": 100})
        self.assertEqual(flow["x2_operational"], {"failed_witnesses": 1, "bounded_recoveries": 1})
        self.assertEqual(flow["closeout_operational"]["failed_witnesses"], 6)
        self.assertEqual(flow["closeout_operational"]["bounded_recoveries"], 6)
        self.assertEqual(len(flow["closeout_operational"]["methods"]), 6)
        self.assertTrue(all(row["status"] == "retained_zero_credit" for row in flow["closeout_operational"]["methods"]))
        self.assertEqual(flow["failed_witness_erasure_count"], 0)
        self.assertFalse(flow["source_repository_count_rewritten"])

    def test_05_delivery_remains_prepared_not_sent(self) -> None:
        state = read("closeout/delivery-state.json")
        self.assertTrue(state["valid"])
        self.assertEqual(state["state"], "PREPARED_NOT_SENT")
        self.assertFalse(state["sent_by_liora_venn"])
        self.assertEqual(state["target_exact_title"], "Tamar Vey")
        self.assertEqual(state["target_phase"], "v665-v3")
        self.assertFalse(state["task_created"] or state["fork_created"] or state["collaboration_subagent_spawned"] or state["standby_contacted"])

    def test_06_outcome_ledger_is_immutable_and_exact(self) -> None:
        ledger = read("x2/ledgers/outcome-ledger.json")
        self.assertTrue(ledger["valid"])
        self.assertEqual(ledger["counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(ledger["unknown_outcome_labels"], [])
        self.assertEqual(ledger["inherited_rows_recredited"], 0)

    def test_07_mutation_ledger_is_immutable_and_exact(self) -> None:
        ledger = read("x2/ledgers/mutation-ledger.json")
        self.assertTrue(ledger["valid"])
        self.assertEqual(ledger["executed_count"], 100)
        self.assertEqual(ledger["rejected_count"], 100)
        self.assertEqual(ledger["accepted_count"], 0)
        self.assertEqual(ledger["failure_erasure_count"], 0)

    def test_08_skill_registry_has_ten_eof_reads(self) -> None:
        registry = read("x2/ledgers/skill-registry.json")
        self.assertTrue(registry["valid"])
        self.assertEqual(registry["count"], 10)
        self.assertFalse(registry["global_installation_performed"])
        self.assertTrue(all(row["read_through_eof"] and row["quick_valid"] and row["smoke_valid"] for row in registry["skills"]))

    def test_09_runner_registry_has_ten_family_surfaces(self) -> None:
        registry = read("x2/ledgers/runner-registry.json")
        self.assertTrue(registry["valid"])
        self.assertEqual(registry["count"], 10)
        self.assertTrue(registry["family_current_prefix_preserved"])
        self.assertTrue(all(row["path"].startswith("scripts/ghc_family_") and row["valid"] for row in registry["runners"]))

    def test_10_owner_manifest_matches_virtual_or_final_blobs(self) -> None:
        manifest = read("validation/final-owner-manifest.json")
        self.assertTrue(manifest["coverage_valid"])
        self.assertEqual(manifest["entry_count"], 148)
        self.assertEqual(manifest["declared_self_exclusion_count"], 4)
        for entry in manifest["entries"]:
            raw = self.bytes_for_final_entry(entry["path"])
            self.assertEqual(self.builder.sha256(raw), entry["sha256"], entry["path"])
            self.assertEqual(len(raw), entry["size"], entry["path"])

    def test_11_delta_manifest_matches_exact_final_base(self) -> None:
        manifest = read("validation/final-delta-manifest.json")
        self.assertTrue(manifest["coverage_valid"])
        self.assertEqual(manifest["entry_count"], 8)
        self.assertEqual(manifest["declared_self_exclusion_count"], 4)
        for entry in manifest["entries"]:
            raw = self.bytes_for_final_entry(entry["path"])
            self.assertEqual(self.builder.sha256(raw), entry["sha256"], entry["path"])

    def test_12_final_review_has_no_scope_or_privacy_hit(self) -> None:
        review = read("validation/final-staged-review.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["source_to_final_path_count"], 152)
        self.assertEqual(review["final_delta_path_count"], 12)
        self.assertEqual(review["confirmed_privacy_or_raw_identifier_hits"], [])
        self.assertEqual(review["immutable_x1_or_evidence_paths_modified"], [])
        self.assertEqual(review["source_or_sibling_paths_modified"], [])

    def test_13_canonical_contract_is_prepared_once(self) -> None:
        contract = read("validation/final-canonical-contract.json")
        self.assertTrue(contract["valid"])
        self.assertEqual(contract["expected_test_count"], 18)
        self.assertEqual(contract["successful_invocation_limit"], 1)
        self.assertTrue(contract["replay_after_success_forbidden"])
        self.assertEqual(contract["canonical_state"], "PREPARED_NOT_RUN")
        self.assertFalse(contract["full_repository_suite"])
        self.assertTrue(contract["same_owner_not_independent_reproduction"])

    def test_14_owner_delta_has_no_private_path_or_raw_task_id(self) -> None:
        paths = sorted(git("diff", "--name-only", f"{SOURCE}..HEAD").splitlines()) if not self.staged_mode else sorted(set(git("diff", "--name-only", f"{SOURCE}..HEAD").splitlines()) | set(self.builder.INTENDED_PATHS))
        windows = re.compile(r"(?i)[a-z]:\\(?:users|ghc-archives)\\")
        raw_id = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
        unix_markers = ["/" + "home/", "/" + "users/"]
        for path in paths:
            raw = self.bytes_for_final_entry(path)
            text = raw.decode("utf-8")
            for match in windows.finditer(text):
                line = text.splitlines()[text.count("\n", 0, match.start())]
                self.assertTrue(path.endswith(".py") and "re.compile" in line, path)
            for match in raw_id.finditer(text):
                line = text.splitlines()[text.count("\n", 0, match.start())]
                self.assertTrue(path.endswith(".py") and ("re.compile" in line or "raw_id" in line), path)
            self.assertFalse(any(marker in text.casefold() for marker in unix_markers), path)

    def test_15_all_owner_text_is_utf8_lf_and_json_or_markdown_is_structural(self) -> None:
        manifest = read("validation/final-owner-manifest.json")
        paths = [row["path"] for row in manifest["entries"]] + manifest["declared_self_exclusions"]
        for path in paths:
            raw = indexed(path) if self.staged_mode and path in self.builder.INTENDED_PATHS else committed(path)
            text = raw.decode("utf-8")
            self.assertNotIn(b"\r\n", raw, path)
            if path.endswith(".json"):
                json.loads(text)
            elif path.endswith(".md"):
                skill_front_matter = path.endswith("/SKILL.md") and text.startswith("---\n") and "\n# " in text
                self.assertTrue(text.startswith("#") or skill_front_matter, path)

    def test_16_changed_python_compiles_and_avoids_unsafe_calls(self) -> None:
        manifest = read("validation/final-owner-manifest.json")
        python_paths = [row["path"] for row in manifest["entries"] if row["path"].endswith(".py")]
        self.assertGreaterEqual(len(python_paths), 1)
        for path in python_paths:
            raw = self.bytes_for_final_entry(path)
            text = raw.decode("utf-8")
            compile(text, path, "exec")
            tree = ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, {"eval", "exec"}, (path, node.lineno))

    def test_17_file_word_and_commit_caps_are_ceiling_checks(self) -> None:
        review = read("validation/final-staged-review.json")
        self.assertLessEqual(review["source_to_final_path_count"], review["file_cap"])
        self.assertLessEqual(review["source_to_final_word_count"], review["word_cap"])
        if not self.staged_mode:
            self.assertEqual(int(git("rev-list", "--count", f"{SOURCE}..HEAD")), 3)

    def test_18_baton_is_sanitized_and_nonpromoting(self) -> None:
        text = (PHASE / "handoffs/tamar-vey-v665-v3-activation-prepared.md").read_text(encoding="utf-8")
        self.assertIn("prepared, not sent", text.casefold())
        self.assertIn("SENT_BY_LIORA_VENN = false", text)
        self.assertIn("Tamar Vey", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("Māori", text)
        self.assertIn("full repository suite was not run", text.casefold())
        self.assertNotIn("READY_FOR_STAGE_20", text.replace("NOT_READY_FOR_STAGE_20", ""))


if __name__ == "__main__":
    unittest.main()
