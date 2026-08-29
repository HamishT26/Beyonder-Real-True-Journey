from __future__ import annotations

import json
import py_compile
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1 = ROOT / "docs" / "lyren-moss" / "v675-v6" / "x1"
VALIDATION = ROOT / "docs" / "lyren-moss" / "v675-v6" / "validation"
SOURCE_FINAL = "0aa1f2b1250e5540650b683d221f92e8762cd991"
BRANCH = "codex/GHC-Family/lyren-moss-v675-v6-full-tools"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(name: str):
    return json.loads((X1 / name).read_text(encoding="utf-8"))


class LyrenV675V6X1Tests(unittest.TestCase):
    def test_exact_source_head_and_branch(self) -> None:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
        self.assertEqual(SOURCE_FINAL, head)
        self.assertEqual(BRANCH, branch)

    def test_all_x1_json_parses(self) -> None:
        paths = sorted(X1.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 17)
        for path in paths:
            with self.subTest(path=path.name):
                json.loads(path.read_text(encoding="utf-8"))

    def test_proposal_freeze(self) -> None:
        data = load("new-proposal-freeze.json")
        rows = data["rows"]
        self.assertEqual(40, len(rows))
        self.assertEqual(40, len({row["title"].casefold() for row in rows}))
        self.assertEqual(7230, data["declared_chain_before"])
        self.assertEqual(7270, data["declared_chain_after"])
        self.assertFalse(data["x2_completion_claimed"])
        self.assertEqual(ALLOWED, {row["planned_outcome"] for row in rows})

    def test_planned_outcome_distribution(self) -> None:
        truth = load("phase-truth.json")
        self.assertEqual(
            {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            truth["planned_outcomes"],
        )
        self.assertEqual(ALLOWED, set(truth["allowed_outcome_labels"]))

    def test_semantic_audit_is_source_bounded(self) -> None:
        audit = load("semantic-neighbor-audit.json")
        self.assertEqual(40, audit["new_titles"])
        self.assertEqual(0, audit["collisions"])
        self.assertFalse(audit["universal_novelty_claim"])
        self.assertTrue(audit["canonical_row_mapping_open_gap"])
        corpus = audit["exact_source_tree_corpus"]
        self.assertGreaterEqual(corpus["candidate_git_blob_paths"], 2409)
        self.assertGreaterEqual(corpus["semantic_occurrences"], 9804)
        self.assertGreaterEqual(corpus["unique_titles"], 3014)
        self.assertEqual(0, corpus["malformed_or_missing_blobs"])

    def test_inherited_revalidations_are_zero_credit(self) -> None:
        data = load("inherited-proposal-revalidation.json")
        self.assertEqual(20, data["count"])
        self.assertEqual(0, data["novelty_credit"])
        self.assertEqual(0, data["automatic_completion_credit"])
        self.assertTrue(all("zero_current_novelty" in row["credit"] for row in data["rows"]))

    def test_portfolio_floors(self) -> None:
        data = load("portfolio-freeze.json")
        self.assertEqual(data["floors"], data["count_integrity"])
        self.assertEqual(60, len(data["safe_now_tasks"]))
        self.assertEqual(30, len(data["candidate_tasks"]))
        self.assertEqual(20, len(data["exact_approval_packets"]))
        self.assertEqual(10, len(data["blocked_packets"]))
        self.assertEqual(20, len(data["owner_skill_ideas"]))
        self.assertEqual(10, len(data["owner_runner_ideas"]))
        self.assertEqual(10, len(data["successor_skill_ideas"]))
        self.assertEqual(10, len(data["successor_runner_ideas"]))
        self.assertEqual(60, len(data["owner_clean_fix_refine"]))
        self.assertEqual(30, len(data["successor_clean_fix_refine"]))

    def test_practice_lens_cardinality(self) -> None:
        data = load("practice-lens-selection.json")
        self.assertEqual(3, len(data["owner_practices"]))
        self.assertEqual(1, len(data["successor_practice_recommendations"]))
        self.assertFalse(data["real_practice_or_professional_claim"])

    def test_three_d_isolated_tools(self) -> None:
        data = load("skill-runner-tool-plan.json")
        tools = {row["name"]: row for row in data["tools"]}
        self.assertEqual({"Pint", "portion", "cattrs"}, set(tools))
        self.assertEqual("0.25.3", tools["Pint"]["version"])
        self.assertEqual("2.6.2", tools["portion"]["version"])
        self.assertEqual("26.1.0", tools["cattrs"]["version"])
        self.assertIn("D-isolated", data["installation"])
        self.assertNotIn("C:\\Users", json.dumps(data))

    def test_source_verification_chain(self) -> None:
        data = load("source-verification.json")
        self.assertEqual(SOURCE_FINAL, data["head_at_x1_build"])
        self.assertEqual("65f67b6c31fe20c02fb865b79e47ab424c159bf9", data["source_parent_chain"]["x1_parent"])
        self.assertEqual("4a44f38af8c04c524ea9c80904fa4e1d71a355d5", data["source_parent_chain"]["evidence_parent"])
        self.assertEqual("5073b0d6a640302b3674e52e7093439c53ec9b5f", data["source_parent_chain"]["final_parent"])
        self.assertEqual(3, data["phase_commit_count"])
        self.assertEqual(0, data["phase_merge_count"])
        self.assertFalse(data["inherited_validation_replay"])

    def test_retained_startup_failures_and_overlay(self) -> None:
        data = load("method-flow-startup.json")
        self.assertEqual(5, len(data["methods"]))
        self.assertTrue(all(row["credit"] == "zero" for row in data["methods"]))
        self.assertFalse(data["failure_erasure"])
        self.assertEqual(40953, data["working_overlay"]["effective_negatives"])
        self.assertEqual(29205, data["working_overlay"]["method_flow_methods"])
        self.assertEqual(12614, data["working_overlay"]["failed_witnesses"])
        self.assertEqual(16656, data["working_overlay"]["bounded_passing_witnesses"])

    def test_sealed_and_overlay_counts_are_separate(self) -> None:
        data = load("source-count-overlay.json")
        self.assertEqual(40947, data["repository_sealed_source"]["effective_negatives"])
        self.assertEqual(40948, data["activation_external_overlay"]["effective_negatives"])
        self.assertEqual(40953, data["lyren_x1_working_overlay"]["effective_negatives"])
        self.assertFalse(data["sealed_source_rewritten"])

    def test_route_is_prospective_only(self) -> None:
        data = load("route-plan.json")
        self.assertEqual("Ilyra Fen", data["prospective_successor"])
        self.assertEqual("v675-v7", data["prospective_phase"])
        self.assertFalse(data["precontacted"])
        self.assertFalse(data["delivery_claimed"])
        self.assertTrue(data["terminal_only"])

    def test_x1_only_no_x2_materialization(self) -> None:
        self.assertFalse((ROOT / "docs" / "lyren-moss" / "v675-v6" / "x2").exists())
        truth = load("phase-truth.json")
        self.assertFalse(truth["x2_started"])
        self.assertFalse(truth["canonical_validation_started"])
        self.assertFalse(truth["successor_contacted"])

    def test_no_crlf_in_owner_text(self) -> None:
        paths = list(X1.rglob("*.json")) + list(X1.rglob("*.md"))
        paths += [
            ROOT / "scripts" / "build_ghc_family_lyren_moss_v675_v6_x1.py",
            ROOT / "tests" / "test_ghc_family_lyren_moss_v675_v6_x1.py",
        ]
        for path in paths:
            with self.subTest(path=path.name):
                self.assertNotIn(b"\r\n", path.read_bytes())

    def test_privacy_boundary_strings_absent(self) -> None:
        forbidden = (
            "C:\\Users\\",
            "source_thread_id",
            "threadId",
            "clientThreadId",
            "api_key",
            "access_token",
            "refresh_token",
        )
        paths = list(X1.rglob("*.json")) + list(X1.rglob("*.md"))
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                with self.subTest(path=path.name, token=token):
                    self.assertNotIn(token, text)

    def test_materialized_and_owner_file_ceiling(self) -> None:
        owner_files = [path for path in (ROOT / "docs" / "lyren-moss" / "v675-v6").rglob("*") if path.is_file()]
        owner_files += [ROOT / "scripts" / "build_ghc_family_lyren_moss_v675_v6_x1.py"]
        owner_files += [ROOT / "tests" / "test_ghc_family_lyren_moss_v675_v6_x1.py"]
        self.assertLess(len(owner_files), 2000)

    def test_builder_compiles(self) -> None:
        py_compile.compile(
            str(ROOT / "scripts" / "build_ghc_family_lyren_moss_v675_v6_x1.py"),
            doraise=True,
        )

    def test_overview_keeps_terminal_boundary(self) -> None:
        text = (X1 / "integrated-overview.md").read_text(encoding="utf-8")
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("not a universal novelty proof", text)
        self.assertIn("no precontact", text.casefold())

    def test_x1_manifest_replays_index_blobs(self) -> None:
        manifest_path = VALIDATION / "x1-manifest.json"
        self.assertTrue(manifest_path.is_file())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(manifest["entry_count"], 20)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            with self.subTest(path=entry["path"]):
                index = subprocess.check_output(
                    ["git", "ls-files", "-s", "--", entry["path"]], cwd=ROOT, text=True
                ).split()[1]
                self.assertEqual(entry["git_blob"], index)
                blob = subprocess.check_output(["git", "cat-file", "blob", index], cwd=ROOT)
                import hashlib
                self.assertEqual(entry["sha256"], hashlib.sha256(blob).hexdigest())

    def test_x1_staged_review_and_privacy(self) -> None:
        review = json.loads((VALIDATION / "x1-staged-review.json").read_text(encoding="utf-8"))
        privacy = json.loads((VALIDATION / "x1-staged-privacy.json").read_text(encoding="utf-8"))
        self.assertEqual(0, review["deletions"])
        self.assertEqual(0, review["renames"])
        self.assertEqual(0, review["x2_entries"])
        self.assertTrue(review["within_file_ceiling"])
        self.assertFalse(review["canonical_aggregate_invoked"])
        self.assertEqual(0, privacy["confirmed_hit_count"])
        self.assertFalse(privacy["complete_privacy_claim"])


if __name__ == "__main__":
    unittest.main()
