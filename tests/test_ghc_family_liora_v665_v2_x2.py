from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/liora-venn/v665-v2"
BUILDER_PATH = ROOT / "scripts/build_ghc_family_v665_v2_evidence.py"
X1 = "1a5fe2e58c3e9fa3ae51a04d0971f30106cbcf38"
BRANCH = "codex/GHC-Family/liora-venn-v665-v2-full-tools"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load_builder():
    spec = importlib.util.spec_from_file_location("liora_v665_v2_evidence_builder", BUILDER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=True
    ).stdout.strip()


class LioraV665V2X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = load_builder()

    def test_01_exact_x1_boundary_and_owner_branch(self) -> None:
        self.assertEqual(git("rev-parse", "HEAD"), X1)
        self.assertEqual(git("branch", "--show-current"), BRANCH)
        self.assertEqual(int(git("rev-list", "--count", f"f4abecafb107f4ac840c09b46a6b30079171816d..{X1}")), 1)
        self.assertEqual(int(git("rev-list", "--count", "--merges", f"f4abecafb107f4ac840c09b46a6b30079171816d..{X1}")), 0)

    def test_02_exact_outcomes_and_labels(self) -> None:
        ledger = read("x2/ledgers/outcome-ledger.json")
        self.assertTrue(ledger["valid"])
        self.assertEqual(ledger["proposal_count"], 20)
        self.assertEqual(ledger["counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(set(ledger["allowed_outcomes"]), ALLOWED)
        self.assertEqual({row["outcome"] for row in ledger["outcomes"]}, ALLOWED)
        self.assertEqual(ledger["unknown_outcome_labels"], [])
        self.assertEqual(ledger["inherited_rows_recredited"], 0)

    def test_03_every_proposal_has_exact_contract_mutation_and_receipt(self) -> None:
        ledger = read("x2/ledgers/outcome-ledger.json")
        for row in ledger["outcomes"]:
            folder = PHASE / "x2/proposals" / row["proposal_id"].casefold()
            contract = json.loads((folder / "contract.json").read_text(encoding="utf-8"))
            mutations = json.loads((folder / "mutation-results.json").read_text(encoding="utf-8"))
            receipt = json.loads((folder / "bounded-receipt.json").read_text(encoding="utf-8"))
            self.assertTrue(contract["valid"] and mutations["valid"] and receipt["valid"])
            self.assertEqual(contract["proposal_id"], row["proposal_id"])
            self.assertEqual(mutations["mutation_count"], 5)
            self.assertEqual(mutations["rejected_count"], 5)
            self.assertEqual(mutations["accepted_mutation_count"], 0)
            self.assertEqual(receipt["observed_disposition"], row["outcome"])
            self.assertEqual(receipt["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
            self.assertFalse(receipt["independent_reproduction"])

    def test_04_all_one_hundred_mutations_are_retained_rejections(self) -> None:
        ledger = read("x2/ledgers/mutation-ledger.json")
        self.assertTrue(ledger["valid"])
        self.assertEqual(ledger["preregistered_count"], 100)
        self.assertEqual(ledger["executed_count"], 100)
        self.assertEqual(ledger["rejected_count"], 100)
        self.assertEqual(ledger["accepted_count"], 0)
        self.assertEqual(ledger["failure_erasure_count"], 0)
        self.assertEqual(len(ledger["mutation_ids"]), len(set(ledger["mutation_ids"])))

    def test_05_positive_fixtures_are_bounded_and_zero_data(self) -> None:
        ledger = read("x2/ledgers/outcome-ledger.json")
        for row in ledger["outcomes"]:
            contract = read(f"x2/proposals/{row['proposal_id'].casefold()}/contract.json")
            fixture = contract["positive_fixture"]
            result = self.builder.evaluate(contract["runner_profile"], fixture)
            self.assertTrue(result["valid"], (row["proposal_id"], result["errors"]))
            self.assertTrue(fixture["synthetic"])
            self.assertEqual(fixture["real_rows"], 0)
            self.assertEqual(fixture["authority_events"], 0)
            self.assertEqual(fixture["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_06_method_flow_is_additive_and_no_failure_is_erased(self) -> None:
        flow = read("x2/ledgers/method-flow-overlay.json")
        self.assertTrue(flow["valid"])
        self.assertEqual(flow["source_activation"], {"negatives": 25_187, "methods": 9_049})
        self.assertEqual(flow["startup_after_x1"]["new_failures"], 13)
        self.assertEqual(flow["x2"]["mutation_failed_witnesses"], 100)
        self.assertEqual(flow["x2"]["operational_failed_witnesses"], 1)
        self.assertEqual(flow["x2"]["new_failed_witnesses"], 101)
        self.assertEqual(flow["x2"]["new_methods"], 101)
        self.assertEqual(flow["x2"]["failure_erasure_count"], 0)
        self.assertEqual(flow["effective_after_x2"], {"negatives": 25_301, "methods": 9_163})
        self.assertEqual(len(flow["methods"]), 101)
        self.assertTrue(all(not row["failed_witness_erased"] for row in flow["methods"]))

    def test_07_ten_phase_local_skills_read_validated_and_smoked(self) -> None:
        registry = read("x2/ledgers/skill-registry.json")
        self.assertTrue(registry["valid"])
        self.assertEqual(registry["count"], 10)
        self.assertFalse(registry["global_installation_performed"])
        for row in registry["skills"]:
            self.assertTrue(row["read_through_eof"] and row["quick_valid"] and row["smoke_valid"])
            raw = (ROOT / row["path"]).read_bytes()
            self.assertEqual(self.builder.sha256(raw), row["sha256"])
            self.assertIn(b"NOT_READY_FOR_STAGE_20", raw)

    def test_08_ten_family_compatible_runners_invoked(self) -> None:
        registry = read("x2/ledgers/runner-registry.json")
        self.assertTrue(registry["valid"])
        self.assertEqual(registry["count"], 10)
        self.assertTrue(registry["family_current_prefix_preserved"])
        for row in registry["runners"]:
            self.assertTrue(row["path"].startswith("scripts/ghc_family_"))
            receipt = json.loads((ROOT / row["receipt"]).read_text(encoding="utf-8"))
            self.assertTrue(receipt["valid"])
            self.assertEqual(receipt["return_code"], 0)
            self.assertTrue(receipt["stderr_empty"])

    def test_09_source_use_is_version_and_vocabulary_only(self) -> None:
        ledger = read("x2/ledgers/source-use-ledger.json")
        self.assertTrue(ledger["valid"])
        self.assertEqual(ledger["source_count"], 10)
        self.assertEqual(ledger["downloaded_empirical_rows"], 0)
        self.assertEqual(ledger["live_data_calls"], 0)
        self.assertEqual(ledger["parsed_real_objects_or_files"], 0)
        self.assertTrue(ledger["version_and_vocabulary_only"])
        self.assertFalse(ledger["conformance_claim"])

    def test_10_open_gap_and_exact_gate_are_preserved(self) -> None:
        open_receipt = read("x2/proposals/lv6652-n019/bounded-receipt.json")
        exact_receipt = read("x2/proposals/lv6652-n020/bounded-receipt.json")
        self.assertEqual(open_receipt["observed_disposition"], "open_gap")
        self.assertIn("zero-equation", open_receipt["disposition_reason"])
        self.assertEqual(exact_receipt["observed_disposition"], "exact_gate")
        for term in ["tangata whenua", "iwi", "hapū", "Māori"]:
            self.assertIn(term, exact_receipt["disposition_reason"])

    def test_11_boundary_matrix_is_nonpromoting(self) -> None:
        boundary = read("x2/ledgers/boundary-matrix.json")
        self.assertTrue(boundary["valid"])
        self.assertIn("no real equations", boundary["GMUT"])
        self.assertIn("representation only", boundary["THOS"])
        self.assertIn("synthetic and nonproduction", boundary["Freed_ID"])
        self.assertIn("exact-gated", boundary["CBR"])
        self.assertEqual(boundary["same_owner"], "not independent reproduction")

    def test_12_execution_summary_is_exact(self) -> None:
        summary = read("x2/ledgers/execution-summary.json")
        self.assertTrue(summary["valid"])
        self.assertEqual(summary["proposal_count"], 20)
        self.assertEqual(summary["mutations"], {"executed": 100, "rejected": 100, "accepted": 0})
        self.assertEqual(summary["operational_failures_retained"], 1)
        self.assertEqual(summary["skills"]["smoke_used"], 10)
        self.assertEqual(summary["runners"]["invoked"], 10)
        for key in ["real_rows", "real_people", "real_vessels", "real_chart_cells", "authority_events"]:
            self.assertEqual(summary[key], 0)
        self.assertFalse(summary["full_repository_suite_run"])
        self.assertFalse(summary["independent_reproduction"])

    def test_13_staged_manifest_matches_exact_blobs(self) -> None:
        result = self.builder.check_staged()
        self.assertTrue(result["valid"])
        self.assertEqual(result["staged_paths"], len(self.builder.INTENDED_PATHS))
        manifest = read("x2/validation/evidence-content-manifest.json")
        review = read("x2/validation/evidence-staged-review.json")
        candidate = read("x2/validation/evidence-stage-candidate.json")
        self.assertEqual(manifest["entry_count"], len(self.builder.BASE_PATHS))
        self.assertEqual(manifest["declared_self_exclusion_count"], 3)
        self.assertTrue(manifest["coverage_valid"] and review["valid"] and candidate["valid"])
        self.assertEqual(review["confirmed_privacy_or_raw_identifier_hits"], 0)
        self.assertEqual(review["x1_paths_modified"], [])
        self.assertEqual(review["source_or_sibling_paths_modified"], [])

    def test_14_owner_delta_has_no_private_absolute_paths_or_task_ids(self) -> None:
        windows_path = re.compile(r"(?i)[a-z]:\\(?:users|ghc-archives)\\")
        unix_markers = ["/" + "home/", "/" + "users/"]
        raw_id = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
        for relative in git("diff", "--cached", "--name-only").splitlines():
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIsNone(windows_path.search(text), relative)
            self.assertFalse(any(marker in text.casefold() for marker in unix_markers), relative)
            self.assertIsNone(raw_id.search(text), relative)

    def test_15_utf8_lf_diff_hygiene_and_terminal_verdict(self) -> None:
        paths = git("diff", "--cached", "--name-only").splitlines()
        self.assertEqual(sorted(paths), self.builder.INTENDED_PATHS)
        terminal_count = 0
        for relative in paths:
            raw = (ROOT / relative).read_bytes()
            raw.decode("utf-8")
            self.assertNotIn(b"\r\n", raw, relative)
            terminal_count += b"NOT_READY_FOR_STAGE_20" in raw
        self.assertGreater(terminal_count, 0)


if __name__ == "__main__":
    unittest.main()
