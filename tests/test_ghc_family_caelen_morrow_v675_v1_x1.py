from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "caelen-morrow" / "v675-v1"
SOURCE_FINAL = "47ba7b0149713f60729f18f5a36ef78c331ce35f"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}


def load(relative: str) -> dict:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout


def staged_blob(path: str) -> bytes:
    return git("show", f":{path}").replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class TestCaelenMorrowV675V1PlanningOnlyX1(unittest.TestCase):
    def test_01_exact_source_and_owner_intake(self) -> None:
        intake = load("x1/activation-intake.json")
        self.assertEqual(git("rev-parse", "HEAD").decode().strip(), SOURCE_FINAL)
        self.assertEqual(intake["owner"], "Caelen Morrow")
        self.assertEqual(intake["phase"], "v675-v1")
        self.assertEqual(intake["source_final"], SOURCE_FINAL)
        self.assertEqual(intake["source_history"]["phase_commits"], 3)
        self.assertEqual(intake["source_history"]["merges"], 0)
        self.assertTrue(intake["source_clean_zero_divergent_fresh_four_way_equal"])
        self.assertFalse(intake["source_validation_replayed"])
        self.assertEqual(intake["task_creation_count"], 0)
        self.assertEqual(intake["subagent_count"], 0)
        self.assertEqual(intake["successor_precontact_count"], 0)

    def test_02_planning_only_lifecycle(self) -> None:
        truth = load("x1/phase-truth.json")
        self.assertTrue(truth["planning_only"])
        self.assertFalse(truth["x2_started"])
        self.assertFalse(truth["outcomes_observed"])
        self.assertIsNone(truth["observed_outcomes"])
        self.assertEqual(truth["external_actions"], 0)
        self.assertEqual(truth["real_people"], 0)
        self.assertEqual(truth["real_objects"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["full_repository_suite"], "not_run_not_claimed")
        self.assertFalse(truth["successor_contacted"])

    def test_03_new_proposal_contracts(self) -> None:
        freeze = load("x1/new-proposal-freeze.json")
        rows = freeze["rows"]
        self.assertEqual(len(rows), 40)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 40)
        self.assertEqual(len({row["title"] for row in rows}), 40)
        self.assertEqual(Counter(row["expected_disposition"] for row in rows), Counter(OUTCOMES))
        self.assertEqual(freeze["proposal_chain_before"], 7030)
        self.assertEqual(freeze["proposal_chain_after_if_evidence_frozen"], 7070)
        self.assertEqual(freeze["planned_invalid_mutations"], 160)
        required = {
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "official_or_primary_source_needs",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        for index, row in enumerate(rows, 1):
            self.assertEqual(row["proposal_id"], f"CM6751-N{index:03d}")
            self.assertTrue(required <= row.keys())
            self.assertEqual(row["planned_outcome"], row["expected_disposition"])
            self.assertEqual(row["x1_state"], "frozen_not_executed")
            self.assertEqual(row["external_actions"], 0)
            self.assertEqual(row["real_people"], 0)
            self.assertEqual(row["real_records_or_objects"], 0)
            self.assertGreaterEqual(len(row["concrete_artifacts"]), 1)
            self.assertGreaterEqual(len(row["protected_gates"]), 1)

    def test_04_inherited_rows_are_zero_credit(self) -> None:
        inherited = load("x1/inherited-proposal-revalidation.json")
        self.assertEqual(inherited["selected"], 20)
        self.assertEqual(inherited["novelty_credit"], 0)
        self.assertEqual(inherited["completion_credit"], 0)
        self.assertEqual(len(inherited["rows"]), 20)
        for row in inherited["rows"]:
            self.assertEqual(row["source_owner"], "Sylven Arc")
            self.assertEqual(row["source_phase"], "v674-v8")
            self.assertEqual(row["caelen_novelty_credit"], 0)
            self.assertEqual(row["caelen_completion_credit"], 0)
            self.assertEqual(row["state"], "inherited_evidence_only")
            self.assertRegex(row["source_row_sha256"], r"^[0-9a-f]{64}$")

    def test_05_source_bounded_semantic_audit(self) -> None:
        audit = load("x1/semantic-neighbor-audit.json")
        corpus = audit["exact_source_tree_corpus"]
        self.assertEqual(corpus["candidate_git_blob_paths"], 2235)
        self.assertEqual(corpus["malformed_or_missing_blobs"], 0)
        self.assertEqual(corpus["semantic_occurrences"], 9098)
        self.assertEqual(corpus["unique_proposal_ids"], 2975)
        self.assertEqual(corpus["unique_titles"], 2848)
        self.assertFalse(corpus["exact_canonical_row_mapping"])
        self.assertTrue(corpus["canonical_row_mapping_open_gap"])
        self.assertFalse(audit["universal_novelty_claim"])
        self.assertEqual(audit["collisions"], 0)
        self.assertLess(audit["max_jaccard"], audit["collision_threshold"])
        self.assertEqual(len(audit["rows"]), 40)
        self.assertTrue(all(not row["collision"] for row in audit["rows"]))
        self.assertEqual(audit["rejected_initial_slate"]["threshold_collisions"], 8)
        self.assertEqual(audit["rejected_initial_slate"]["novelty_credit"], 0)

    def test_06_portfolio_counts_and_x1_nonexecution(self) -> None:
        portfolio = load("x1/portfolio-freeze.json")
        expected = {
            "inherited_reviews": 20,
            "safe_now": 60,
            "candidates": 30,
            "exact_approval": 20,
            "blocked": 10,
            "skills": 20,
            "runners": 10,
            "tools": 3,
            "clean_fix_refine": 60,
            "successor_skills": 10,
            "successor_runners": 10,
            "successor_clean_fix_refine": 30,
        }
        self.assertEqual(portfolio["counts"], expected)
        self.assertTrue(portfolio["filler_prohibited"])
        self.assertEqual(portfolio["successor_practice_recommendation_count"], 1)
        for key, rows in portfolio["rows"].items():
            self.assertEqual(len(rows), expected[key])
            for row in rows:
                self.assertEqual(row["state"], "frozen_not_executed")
                self.assertEqual(row["execution_count"], 0)
                self.assertEqual(row["completion_credit"], 0)

    def test_07_method_flow_retains_every_startup_failure(self) -> None:
        flow = load("x1/method-flow-startup.json")
        self.assertEqual(flow["execution_authority"], "owner_self_scoped_delta")
        self.assertEqual(len(flow["methods"]), 18)
        self.assertEqual(len(flow["recommendations"]), 18)
        self.assertEqual(len(flow["state_events"]), 54)
        self.assertEqual(len(flow["witnesses"]), 36)
        self.assertEqual(len(flow["negative_rows"]), 18)
        self.assertEqual(Counter(w["result"] for w in flow["witnesses"]), Counter({"fail": 18, "pass": 18}))
        method_ids = {row["method_id"] for row in flow["methods"]}
        witness_ids = {row["witness_id"] for row in flow["witnesses"]}
        negative_ids = {row["negative_id"] for row in flow["negative_rows"]}
        self.assertEqual(len(method_ids), 18)
        self.assertEqual(len(witness_ids), 36)
        self.assertEqual(len(negative_ids), 18)
        for method in flow["methods"]:
            self.assertEqual(method["recommendation_state"], "preferred")
            self.assertTrue(set(method["validation_witness_ids"]) <= witness_ids)
            self.assertTrue(set(method["retained_negative_ids"]) <= negative_ids)
        for witness in flow["witnesses"]:
            self.assertIn(witness["method_id"], method_ids)
            self.assertTrue(witness["same_owner_only"])
            self.assertFalse(witness["independent_reproduction"])
        for negative in flow["negative_rows"]:
            self.assertEqual(negative["result"], "fail")
            self.assertEqual(negative["completion_credit"], 0)
            self.assertTrue(negative["recovery_preserves_failure"])

    def test_08_sources_are_read_only_vocabulary_only(self) -> None:
        ledger = load("x1/source-ledger.json")
        self.assertEqual(ledger["read_only_source_page_checks"], 7)
        self.assertEqual(ledger["api_calls"], 0)
        self.assertEqual(ledger["dataset_or_media_downloads"], 0)
        self.assertEqual(ledger["external_writes"], 0)
        self.assertEqual(ledger["real_rows"], 0)
        self.assertEqual(len(ledger["sources"]), 7)
        self.assertTrue(all(row["url"].startswith("https://") for row in ledger["sources"]))

    def test_09_practice_identity_and_route_boundaries(self) -> None:
        identity = load("x1/identity-and-boundary.json")
        practice = load("x1/practice-lens-selection.json")
        route = load("x1/route-plan.json")
        self.assertIn("relational working language only", identity["identity_boundary"])
        self.assertEqual(practice["primary_pillar"], "Freed ID and CBR Heart")
        self.assertEqual(len(practice["candidates"]), 3)
        self.assertEqual(sum(row.get("selected_for_current_phase", False) for row in practice["candidates"]), 1)
        self.assertEqual(sum(row.get("recommended_to_successor_conditionally", False) for row in practice["candidates"]), 1)
        self.assertEqual(practice["real_people"], 0)
        self.assertFalse(practice["authority_conferred"])
        self.assertEqual(route["delivery_state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["successor_contact_attempts"], 0)
        self.assertFalse(route["task_created"])
        self.assertFalse(route["standby_contacted"])

    def test_10_no_x2_or_cross_owner_path_is_staged(self) -> None:
        paths = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", SOURCE_FINAL).decode().splitlines()
        self.assertGreater(len(paths), 0)
        for path in paths:
            self.assertTrue(
                path.startswith("docs/caelen-morrow/v675-v1/")
                or path
                in {
                    "scripts/build_ghc_family_caelen_morrow_v675_v1_x1.py",
                    "tests/test_ghc_family_caelen_morrow_v675_v1_x1.py",
                }
            )
            self.assertNotIn("/x2/", f"/{path}/")
            self.assertNotIn("_x2.py", path)
        name_status = git("diff", "--cached", "--name-status", SOURCE_FINAL).decode().splitlines()
        self.assertFalse(any(row.startswith("D\t") for row in name_status))

    def test_11_privacy_scan_has_no_confirmed_hit(self) -> None:
        privacy = load("validation/x1-staged-privacy.json")
        self.assertEqual(len(privacy["pattern_classes"]), 5)
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertEqual(privacy["confirmed_hits"], [])
        self.assertEqual(privacy["decode_issues"], [])

    def test_12_manifest_and_staged_review_replay(self) -> None:
        manifest = load("validation/x1-manifest.json")
        review = load("validation/x1-staged-review.json")
        staged = set(git("diff", "--cached", "--name-only", "--diff-filter=ACMR", SOURCE_FINAL).decode().splitlines())
        declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
        self.assertEqual(declared, staged)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(len({row["path"] for row in manifest["entries"]}), manifest["entry_count"])
        for row in manifest["entries"]:
            blob = staged_blob(row["path"])
            self.assertEqual(len(blob), row["bytes"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"])
        self.assertTrue(review["valid"])
        self.assertTrue(review["allowed_owner_scope"])
        self.assertEqual(review["deletions"], [])
        self.assertEqual(review["x2_paths"], [])
        self.assertEqual(review["manifest_issues"], [])
        self.assertFalse(review["outcomes_observed"])

    def test_13_all_owner_json_parses_and_caps_hold(self) -> None:
        json_paths = sorted(OWNER_ROOT.rglob("*.json"))
        self.assertGreaterEqual(len(json_paths), 20)
        for path in json_paths:
            json.loads(path.read_text(encoding="utf-8"))
        owner_files = [path for path in OWNER_ROOT.rglob("*") if path.is_file()]
        owner_files.extend([ROOT / "scripts" / "build_ghc_family_caelen_morrow_v675_v1_x1.py", ROOT / "tests" / "test_ghc_family_caelen_morrow_v675_v1_x1.py"])
        self.assertLessEqual(len(owner_files), 2000)
        for path in owner_files:
            if path.suffix.lower() in {".json", ".md", ".py", ".yaml", ".yml", ".html", ".txt"}:
                words = len(path.read_text(encoding="utf-8").split())
                self.assertLessEqual(words, 100000, path.as_posix())


if __name__ == "__main__":
    unittest.main()
