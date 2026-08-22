from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/liora-venn/v665-v2"
BUILDER_PATH = ROOT / "scripts/build_ghc_family_v665_v2_x1.py"
SOURCE_FINAL = "f4abecafb107f4ac840c09b46a6b30079171816d"
BRANCH = "codex/GHC-Family/liora-venn-v665-v2-full-tools"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load_builder():
    spec = importlib.util.spec_from_file_location("liora_v665_v2_x1_builder", BUILDER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def doc(name: str):
    return json.loads((PHASE / "x1" / name).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=True
    ).stdout.strip()


class LioraV665V2X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = load_builder()

    def test_01_exact_source_and_owner_branch(self) -> None:
        self.assertEqual(git("rev-parse", "HEAD"), SOURCE_FINAL)
        self.assertEqual(git("branch", "--show-current"), BRANCH)
        verification = doc("source-verification.json")
        self.assertTrue(verification["valid"])
        self.assertEqual(verification["source_to_final_commit_count"], 4)
        self.assertEqual(verification["source_to_final_merge_count"], 0)
        self.assertEqual(verification["final_parent_count"], 1)
        self.assertTrue(all(row["valid"] for row in verification["direct_parent_checks"]))

    def test_02_corpus_reconstruction_and_novelty(self) -> None:
        audit = doc("novelty-audit.json")
        rebuilt = self.builder.audit_only()
        self.assertTrue(audit["valid"] and rebuilt["valid"])
        self.assertEqual(audit["corpus_row_count"], 4_030)
        self.assertEqual(rebuilt["corpus"], 4_030)
        self.assertEqual(audit["corpus_canonical_sha256"], rebuilt["corpus_sha256"])
        self.assertEqual(audit["exact_inherited_collisions"], [])
        self.assertLess(audit["maximum_inherited_token_jaccard_similarity"], 0.60)
        self.assertLess(audit["maximum_new_pair_token_jaccard_similarity"], 0.70)
        self.assertEqual(audit["rejected_drafts"]["status"], "retained_zero_credit")

    def test_03_planning_only_proposal_contract(self) -> None:
        freeze = doc("proposal-freeze.json")
        proposals = freeze["new_proposals"]
        self.assertEqual(len(proposals), 20)
        self.assertEqual(freeze["inherited_frozen_baseline"], 4_030)
        self.assertEqual(freeze["new_frozen_total"], 4_050)
        self.assertEqual(
            freeze["new_expected_outcomes"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual({row["expected_disposition"] for row in proposals}, ALLOWED)
        self.assertFalse(freeze["observed_outcomes_present"])
        self.assertFalse(freeze["x2_implementation_present"])
        self.assertEqual(freeze["selected_inherited_count"], 20)
        self.assertTrue(all(not row["novelty_credit"] for row in freeze["selected_inherited"]))
        required = {
            "approval_class", "concrete_artifacts", "current_official_or_primary_source_needs",
            "execution_lane", "expected_disposition", "falsifier_or_acceptance_gate", "hypothesis",
            "novelty_credit", "null_or_failure_condition", "proposal_id", "protected_gates",
            "rollback_or_recovery", "title",
        }
        for row in proposals:
            self.assertTrue(required.issubset(row))
            self.assertTrue(row["novelty_credit"])
            self.assertEqual(len(row["concrete_artifacts"]), 3)
            self.assertIn("stage_20", row["protected_gates"])

    def test_04_identity_and_practice_boundaries(self) -> None:
        charter = doc("phase-charter.json")
        self.assertTrue(charter["valid"])
        self.assertEqual(charter["owner"], "Liora Venn")
        self.assertIn("relational", charter["relational_role"])
        self.assertIn("not evidence", charter["identity_boundary"].lower())
        self.assertEqual(charter["allowed_truth_labels"], ["completed", "represented", "open_gap", "exact_gate"])
        self.assertEqual(charter["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertIn("zero real", charter["practice_boundary"])
        self.assertFalse(charter["successor"]["contact_before_terminal_gate"])

    def test_05_startup_method_flow_is_additive(self) -> None:
        flow = doc("startup-method-flow.json")
        self.assertTrue(flow["valid"])
        self.assertEqual(flow["new_method_count"], 13)
        self.assertEqual(flow["new_failed_witness_count"], 13)
        self.assertEqual(flow["new_passing_witness_count"], 13)
        self.assertEqual(flow["failure_erasure_count"], 0)
        self.assertEqual(flow["effective_negatives_after_startup"], 25_200)
        self.assertEqual(flow["effective_methods_after_startup"], 9_062)
        self.assertTrue(all(row["failed_witness_status"] == "retained_zero_credit" for row in flow["methods"]))

    def test_06_primary_or_official_sources_are_zero_data(self) -> None:
        ledger = doc("source-ledger.json")
        self.assertTrue(ledger["valid"])
        self.assertEqual(ledger["source_count"], 10)
        self.assertTrue(all(row["official_or_primary"] for row in ledger["sources"]))
        for row in ledger["sources"]:
            self.assertEqual(row["downloaded_empirical_rows"], 0)
            self.assertEqual(row["live_data_calls"], 0)
            self.assertEqual(row["parsed_real_objects_or_files"], 0)
            self.assertIn(row["status"], ledger["allowed_statuses"])
            self.assertIn("not", row["authority_boundary"].lower())

    def test_07_portfolios_are_exact_and_successor_rows_are_zero_credit(self) -> None:
        freeze = doc("portfolio-freeze.json")
        self.assertTrue(freeze["valid"])
        expected = {
            "owner_safe_now": 30, "owner_candidates": 15, "exact_approval_packets": 10,
            "blocked_packets": 5, "owner_skill_ideas": 10, "owner_runner_ideas": 10,
            "owner_clean_fix_refine": 30, "successor_safe_now_recommendations": 20,
            "successor_candidate_recommendations": 15, "successor_skill_recommendations": 10,
            "successor_runner_recommendations": 10, "successor_clean_fix_refine_recommendations": 30,
        }
        self.assertEqual(freeze["counts"], expected)
        successor_keys = [key for key in freeze if key.startswith("successor_")]
        for key in successor_keys:
            if isinstance(freeze[key], list):
                self.assertTrue(all(not row["current_phase_credit"] for row in freeze[key]))

    def test_08_workflow_blocks_x2_and_canonical_replay(self) -> None:
        workflow = doc("workflow-plan.json")
        self.assertTrue(workflow["valid"])
        states = {row["stage"]: row["state"] for row in workflow["steps"]}
        self.assertEqual(states["x2"], "blocked_until_x1_gate")
        self.assertIn("no replay", states["canonical"])
        self.assertIn("Tamar", states["route"])
        self.assertIn("same-owner scoped validation", workflow["constraints"])
        self.assertIn("no full suite", workflow["constraints"])

    def test_09_threat_model_preserves_protected_gates(self) -> None:
        threat = doc("threat-model-plan.json")
        self.assertTrue(threat["valid"])
        self.assertEqual(len(threat["threats"]), 12)
        text = json.dumps(threat, ensure_ascii=False).casefold()
        for term in ["privacy", "māori", "canonical replay", "professional", "independent reproduction"]:
            self.assertIn(term, text)

    def test_10_x1_staged_manifests_match_exact_blobs(self) -> None:
        self.assertEqual(self.builder.check_staged()["staged_paths"], 15)
        manifest = doc("x1-content-manifest.json")
        review = doc("x1-staged-review.json")
        candidate = doc("x1-stage-candidate.json")
        self.assertEqual(manifest["entry_count"], 12)
        self.assertEqual(manifest["declared_self_exclusion_count"], 3)
        self.assertTrue(manifest["coverage_valid"])
        self.assertTrue(review["valid"] and candidate["valid"])
        self.assertFalse(review["x2_paths_present"])
        self.assertEqual(review["confirmed_privacy_or_raw_identifier_hits"], 0)

    def test_11_owner_text_has_no_private_absolute_paths_or_task_ids(self) -> None:
        paths = [Path(row) for row in git("diff", "--cached", "--name-only").splitlines() if row]
        private_path = re.compile(r"(?i)[a-z]:\\(?:users|ghc-archives)\\")
        unix_markers = ["/" + "home/", "/" + "users/"]
        raw_id = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
        for relative in paths:
            data = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIsNone(private_path.search(data), str(relative))
            self.assertFalse(any(marker in data.casefold() for marker in unix_markers), str(relative))
            self.assertIsNone(raw_id.search(data), str(relative))

    def test_12_utf8_lf_and_terminal_verdict(self) -> None:
        paths = [Path(row) for row in git("diff", "--cached", "--name-only").splitlines() if row]
        verdict_seen = False
        for relative in paths:
            raw = (ROOT / relative).read_bytes()
            raw.decode("utf-8")
            self.assertNotIn(b"\r\n", raw, str(relative))
            verdict_seen = verdict_seen or b"NOT_READY_FOR_STAGE_20" in raw
        self.assertTrue(verdict_seen)


if __name__ == "__main__":
    unittest.main()
