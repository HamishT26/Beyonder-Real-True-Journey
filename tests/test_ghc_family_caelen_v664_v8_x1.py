"""Owner-scoped tests for Caelen Ash v664-v8's planning-only x1 freeze."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/caelen-ash/v664-v8"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}
X1_HEAD = "0832a8260dec6c5d776a6b22f6cf9b2c9e81d705"


def strict_json(path: Path):
    def reject_duplicates(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate key {key} in {path}")
            value[key] = item
        return value

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


class CaelenV664V8X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.charter = strict_json(PHASE / "x1/phase-charter.json")
        cls.freeze = strict_json(PHASE / "x1/proposal-freeze.json")
        cls.audit = strict_json(PHASE / "x1/novelty-audit.json")
        cls.portfolio = strict_json(PHASE / "x1/portfolio-freeze.json")
        cls.sources = strict_json(PHASE / "x1/source-ledger.json")
        cls.source_verification = strict_json(PHASE / "x1/source-verification.json")
        cls.methods = strict_json(PHASE / "x1/startup-method-flow.json")
        cls.threats = strict_json(PHASE / "x1/threat-model-plan.json")
        cls.workflow = strict_json(PHASE / "x1/workflow-plan.json")
        cls.overview = (PHASE / "x1/x1-overview.md").read_text(encoding="utf-8")

    def test_01_identity_is_relational(self) -> None:
        self.assertEqual(self.charter["owner"], "Caelen Ash")
        self.assertEqual(self.charter["optional_pronouns"], "they/them")
        boundary = self.charter["identity_boundary"]
        for term in ("consciousness", "legal personhood", "employment", "authority"):
            self.assertIn(term, boundary)

    def test_02_exact_source_and_lane(self) -> None:
        self.assertEqual(
            self.source_verification["anchors"]["sable_exact_final"],
            "682666c064b14f09def75fb46f3bafb0e987a7a2",
        )
        self.assertEqual(
            self.source_verification["current_branch"],
            "codex/GHC-Family/caelen-ash-v664-v8-full-tools",
        )
        self.assertTrue(self.source_verification["valid"])

    def test_03_source_history(self) -> None:
        self.assertEqual(self.source_verification["source_to_final_commit_count"], 4)
        self.assertEqual(self.source_verification["source_to_final_merge_count"], 0)
        self.assertEqual(self.source_verification["final_parent_count"], 1)
        self.assertTrue(all(row["valid"] for row in self.source_verification["direct_parent_checks"]))

    def test_04_source_manifest_replay(self) -> None:
        rows = self.source_verification["manifest_replays"]
        self.assertEqual([row["entry_count"] for row in rows], [197, 12])
        self.assertEqual(sum(row["mismatch_count"] for row in rows), 0)
        self.assertTrue(all(row["valid"] for row in rows))

    def test_05_receipt_digests(self) -> None:
        digests = self.source_verification["receipt_digests"]
        self.assertEqual(len(digests["retained_failed_canonical"]), 64)
        self.assertEqual(len(digests["successful_corrected_canonical"]), 64)
        self.assertNotEqual(
            digests["retained_failed_canonical"], digests["successful_corrected_canonical"]
        )

    def test_06_exact_corpus(self) -> None:
        self.assertEqual(self.audit["corpus_row_count"], 3_990)
        self.assertEqual(
            self.audit["corpus_canonical_sha256"],
            "c5607c0d9b8ba0a8c53a08a2fd9d6a47796a6bb33ba69329fad226e2eab356e7",
        )
        self.assertEqual(self.freeze["inherited_frozen_baseline"], 3_990)
        self.assertEqual(self.freeze["new_frozen_total"], 4_010)

    def test_07_novelty_screen(self) -> None:
        self.assertTrue(self.audit["valid"])
        self.assertEqual(self.audit["exact_inherited_collisions"], [])
        self.assertEqual(self.audit["new_pair_collisions_at_or_above_0_70"], [])
        self.assertLess(self.audit["maximum_inherited_token_jaccard_similarity"], 0.60)
        self.assertLess(self.audit["maximum_new_pair_token_jaccard_similarity"], 0.70)
        self.assertEqual(self.audit["rejected_lens"]["proposal_credit"], 0)

    def test_08_twenty_complete_proposal_contracts(self) -> None:
        rows = self.freeze["new_proposals"]
        self.assertEqual(len(rows), 20)
        required = {
            "proposal_id",
            "title",
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "current_official_or_primary_source_needs",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for row in rows:
            self.assertTrue(required <= set(row))
            self.assertIn(row["expected_disposition"], ALLOWED)
            self.assertEqual(len(row["protected_gates"]), 15)

    def test_09_expected_not_observed_outcomes(self) -> None:
        counts = Counter(row["expected_disposition"] for row in self.freeze["new_proposals"])
        self.assertEqual(
            counts, Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        )
        self.assertFalse(self.freeze["observed_outcomes_present"])
        self.assertFalse(self.freeze["x2_implementation_present"])

    def test_10_selected_inherited_zero_credit(self) -> None:
        rows = self.freeze["selected_inherited"]
        self.assertEqual(len(rows), 20)
        for row in rows:
            self.assertFalse(row["novelty_credit"])
            self.assertFalse(row["automatic_completion_credit"])
            self.assertFalse(row["caelen_new_outcome_credit"])

    def test_11_primary_and_protected_pillars(self) -> None:
        self.assertEqual(self.charter["primary_pillar"], "THOS Body")
        self.assertEqual(self.charter["protected_pillars"], ["GMUT Mind", "Freed ID and CBR Heart"])
        self.assertIn("synthetic orchestral", self.charter["bounded_practice"])

    def test_12_sources_are_zero_observation(self) -> None:
        self.assertEqual(self.sources["source_count"], 10)
        for row in self.sources["sources"]:
            self.assertTrue(row["official_or_primary"])
            self.assertEqual(row["live_data_calls"], 0)
            self.assertEqual(row["downloaded_score_rows"], 0)
            self.assertEqual(row["parsed_score_files"], 0)
            self.assertEqual(row["rehearsal_observations"], 0)

    def test_13_portfolio_counts(self) -> None:
        self.assertEqual(
            self.portfolio["counts"],
            {
                "owner_safe_now": 30,
                "owner_candidates": 15,
                "owner_skill_ideas": 10,
                "owner_runner_ideas": 10,
                "owner_clean_fix_refine": 30,
                "exact_approval_packets": 10,
                "blocked_packets": 5,
                "successor_safe_now_recommendations": 20,
                "successor_candidate_recommendations": 15,
                "successor_skill_recommendations": 10,
                "successor_runner_recommendations": 10,
                "successor_clean_fix_refine_recommendations": 30,
            },
        )
        self.assertTrue(self.portfolio["valid"])

    def test_14_exact_and_blocked_are_unexecuted(self) -> None:
        rows = self.portfolio["exact_approval_packets"] + self.portfolio["blocked_packets"]
        self.assertEqual(len(rows), 15)
        self.assertTrue(all(row["status"] == "unexecuted" for row in rows))
        self.assertTrue(all(row["caelen_execution_credit"] == 0 for row in rows))

    def test_15_successor_recommendations_have_zero_credit(self) -> None:
        keys = [key for key in self.portfolio if key.startswith("successor_")]
        self.assertEqual(len(keys), 5)
        for key in keys:
            self.assertTrue(
                all(row["current_owner_completion_credit_if_executed"] == 0 for row in self.portfolio[key])
            )

    def test_16_method_flow_arithmetic(self) -> None:
        self.assertEqual(
            self.methods["user_delivered_activation_baseline"],
            {"effective_negatives": 24_941, "effective_methods": 8_955, "rewritten": False},
        )
        self.assertEqual(
            self.methods["effective_starting_overlay"],
            {"effective_negatives": 24_942, "effective_methods": 8_956},
        )
        self.assertEqual(self.methods["new_method_count"], 7)
        self.assertEqual(self.methods["new_failed_witness_count"], 7)
        self.assertEqual(self.methods["new_passing_witness_count"], 7)
        self.assertEqual(self.methods["effective_negatives_after_startup"], 24_949)
        self.assertEqual(self.methods["effective_methods_after_startup"], 8_963)
        self.assertEqual(self.methods["failure_erasure_count"], 0)

    def test_17_each_failure_is_retained(self) -> None:
        self.assertEqual(len(self.methods["methods"]), 7)
        for row in self.methods["methods"]:
            self.assertEqual(row["failed_witness_credit"], "zero")
            self.assertTrue(row["failed_witness"])
            self.assertTrue(row["passing_witness"])

    def test_18_threats_and_recovery(self) -> None:
        self.assertEqual(len(self.threats["threats"]), 12)
        self.assertTrue(self.threats["valid"])
        self.assertIn("retain the negative", self.threats["recovery"])

    def test_19_workflow_gates_x2(self) -> None:
        statuses = {row["step_id"]: row["status"] for row in self.workflow["steps"]}
        self.assertEqual(statuses["P5"], "blocked_until_x1_remote_equal")
        self.assertEqual(statuses["P7"], "blocked_until_clean_pushed_final")
        self.assertEqual(statuses["P8"], "blocked_until_terminal_gate")

    def test_20_strict_x1_boundary(self) -> None:
        self.assertTrue(self.charter["strict_lifecycle"]["x1_before_x2"])
        self.assertFalse(self.charter["strict_lifecycle"]["x1_contains_x2_implementation"])
        self.assertFalse(self.charter["strict_lifecycle"]["x1_contains_observed_outcomes"])
        x1_tree_x2 = subprocess.run(
            [
                "git",
                "ls-tree",
                "-r",
                "--name-only",
                X1_HEAD,
                "--",
                "docs/caelen-ash/v664-v8/x2",
            ],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            check=True,
            text=True,
            encoding="utf-8",
        ).stdout.splitlines()
        self.assertEqual(x1_tree_x2, [])

    def test_21_terminal_boundaries(self) -> None:
        self.assertEqual(self.charter["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(self.charter["successor"]["state"], "PREPARED_NOT_SENT")
        self.assertEqual(self.charter["successor"]["authorized_exact_title_after_terminal_gate"], "Orin Thale")
        self.assertFalse(self.charter["successor"]["precontacted"])

    def test_22_overview_refuses_promotion(self) -> None:
        required = [
            "planning-only",
            "no x2 implementation",
            "no observed outcome",
            "PREPARED_NOT_SENT",
            "NOT_READY_FOR_STAGE_20",
            "Māori concepts remain under Māori authority",
            "not evidence of consciousness",
        ]
        for phrase in required:
            self.assertIn(phrase, self.overview)

    def test_23_all_phase_json_strictly_parse(self) -> None:
        for path in sorted(PHASE.rglob("*.json")):
            strict_json(path)

    def test_24_no_raw_identifier_or_private_absolute_path(self) -> None:
        raw_identifier = re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        )
        private_path = re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]")
        for path in sorted([*PHASE.rglob("*"), ROOT / "scripts/build_ghc_family_v664_v8_x1.py", Path(__file__)]):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(raw_identifier.search(text), str(path))
            self.assertIsNone(private_path.search(text), str(path))

    def test_25_generated_text_has_single_terminal_newline(self) -> None:
        for path in sorted(PHASE.rglob("*")):
            if path.is_file():
                raw = path.read_bytes()
                self.assertTrue(raw.endswith(b"\n"), str(path))
                self.assertFalse(raw.endswith(b"\n\n"), str(path))


if __name__ == "__main__":
    unittest.main()
