#!/usr/bin/env python3
"""Owner-scoped tests for the immutable-planning Liora Venn v668-v8 x1 surface."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
import unittest
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_liora_venn_v668_v8_x1 as builder  # noqa: E402
import ghc_family_liora_venn_v668_v8_archive as archive  # noqa: E402


def git(*args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=not binary,
    )
    return result.stdout if binary else result.stdout.strip()


class LioraV668V8X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        commits = str(git("rev-list", "--reverse", f"{archive.SOURCE_FINAL}..HEAD")).splitlines()
        cls.x1_commit = commits[0] if commits else None

    @classmethod
    def read_bytes(cls, relative: str) -> bytes:
        if cls.x1_commit:
            return git("show", f"{cls.x1_commit}:{relative}", binary=True)  # type: ignore[return-value]
        return (ROOT / relative).read_bytes()

    @classmethod
    def read_json(cls, relative: str) -> dict:
        return json.loads(cls.read_bytes(relative).decode("utf-8"))

    @classmethod
    def x1_paths(cls) -> list[str]:
        if cls.x1_commit:
            return str(git("ls-tree", "-r", "--name-only", cls.x1_commit, "--", archive.REL_PHASE_ROOT)).splitlines()
        return sorted(path.relative_to(ROOT).as_posix() for path in archive.PHASE_ROOT.rglob("*") if path.is_file())

    def proposal_rows(self) -> list[dict]:
        freeze = self.read_json(f"{archive.REL_PHASE_ROOT}/x1/proposal-freeze.json")
        rows: list[dict] = []
        for shard in freeze["shards"]:
            rows.extend(self.read_json(shard["path"])["rows"])
        return rows

    def test_01_branch_source_and_planning_tree(self) -> None:
        self.assertEqual(git("branch", "--show-current"), archive.BRANCH)
        self.assertEqual(git("merge-base", "--is-ancestor", archive.SOURCE_FINAL, "HEAD",), "")
        if self.x1_commit:
            self.assertEqual(git("rev-parse", f"{self.x1_commit}^"), archive.SOURCE_FINAL)
            self.assertEqual(git("rev-list", "--count", f"{archive.SOURCE_FINAL}..{self.x1_commit}"), "1")
            self.assertEqual(git("rev-list", "--merges", f"{archive.SOURCE_FINAL}..{self.x1_commit}"), "")
        else:
            self.assertEqual(git("rev-parse", "HEAD"), archive.SOURCE_FINAL)
        paths = self.x1_paths()
        self.assertTrue(paths)
        for forbidden in ("/x2/", "/evidence/", "/final/", "/closeout/", "/seal/", "/skills/", "/runners/"):
            self.assertFalse(any(forbidden in f"/{path}/" for path in paths), forbidden)

    def test_02_phase_truth_is_planning_only(self) -> None:
        truth = self.read_json(f"{archive.REL_PHASE_ROOT}/x1/phase-truth.json")
        self.assertEqual(truth["lifecycle_stage"], "x1_planning_only")
        self.assertEqual(truth["source_commit"], archive.SOURCE_FINAL)
        self.assertIsNone(truth["x1_commit"])
        self.assertFalse(truth["x2_started"])
        self.assertEqual(truth["completion_claims"], 0)
        self.assertEqual(truth["terminal_verdict"], archive.TERMINAL_VERDICT)
        self.assertEqual(set(truth["expected_outcomes"]), set(archive.ALLOWED_OUTCOMES))
        self.assertEqual(truth["observed_outcomes"], {label: 0 for label in archive.ALLOWED_OUTCOMES})

    def test_03_proposal_freeze_counts_and_labels(self) -> None:
        rows = self.proposal_rows()
        self.assertEqual(len(rows), 40)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 40)
        self.assertEqual(len({row["semantic_slug"] for row in rows}), 40)
        self.assertEqual(Counter(row["expected_disposition"] for row in rows), Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}))
        self.assertEqual({row["expected_disposition"] for row in rows}, set(archive.ALLOWED_OUTCOMES))
        self.assertTrue(all(row["observed_disposition"] is None and row["x1_completion_credit"] == 0 for row in rows))
        self.assertEqual(sum(len(row["negative_fixtures"]) for row in rows), 160)
        self.assertTrue(all(len({mutation["mutation_id"] for mutation in row["negative_fixtures"]}) == 4 for row in rows))

    def test_04_every_proposal_has_complete_preregistration(self) -> None:
        required = {
            "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane",
            "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition", "semantic_neighbors",
        }
        for row in self.proposal_rows():
            self.assertTrue(required <= set(row), row["proposal_id"])
            self.assertTrue(all(row[field] for field in required - {"semantic_neighbors"}), row["proposal_id"])
            self.assertEqual(set(row["protected_gates"]), set(archive.PROTECTED_GATES))
            self.assertFalse(row["visible_title_collision"])
            self.assertFalse(row["semantic_neighbor_quarantined"])
            self.assertLess(row["semantic_neighbors"][0]["score"], 0.75)

    def test_05_novelty_inventory_is_honest_and_reproducible(self) -> None:
        novelty = self.read_json(f"{archive.REL_PHASE_ROOT}/x1/semantic-novelty-audit.json")
        audit = novelty["audit"]
        self.assertEqual(audit["declared_inherited_chain_count"], 4870)
        self.assertEqual(audit["unique_proposal_ids"], builder.EXPECTED_RECOVERED_PROPOSALS)
        self.assertEqual(audit["unique_normalized_titles"], 1299)
        self.assertEqual(audit["normalized_title_sha256"], builder.EXPECTED_CORPUS_SHA256)
        self.assertEqual(audit["cooperage_keyword_hit_count"], 0)
        self.assertEqual(audit["parse_failures"], [])
        self.assertEqual(audit["scan_failures"], [])
        self.assertEqual(audit["unrecovered_compressed_title_minimum"], 3570)
        rows = []
        for shard in novelty["historical_corpus_shards"]:
            rows.extend(self.read_json(shard["path"])["rows"])
        self.assertEqual(len(rows), 1300)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 1300)
        digest = hashlib.sha256("\n".join(sorted({row["normalized_title"] for row in rows if row["normalized_title"]})).encode("utf-8")).hexdigest()
        self.assertEqual(digest, builder.EXPECTED_CORPUS_SHA256)

    def test_06_portfolio_floors_and_holds(self) -> None:
        expected = {"safe_now": 60, "candidates": 30, "skills": 20, "runners": 10, "clean_fix_refine": 60, "exact_approval": 20, "blocked": 10}
        for name, count in expected.items():
            rows = self.read_json(f"{archive.REL_PHASE_ROOT}/x1/portfolios/{name}.json")["rows"]
            self.assertEqual(len(rows), count, name)
            self.assertTrue(all(row["completion_credit"] == 0 and row["x1_planning_only"] for row in rows))
            self.assertTrue(all(row["x2_execution_count"] == 0 and row["external_actions"] == 0 and row["authority_actions"] == 0 for row in rows))
        self.assertTrue(all(row["state"] == "held_unexecuted" for row in self.read_json(f"{archive.REL_PHASE_ROOT}/x1/portfolios/exact_approval.json")["rows"]))
        self.assertTrue(all(row["state"] == "blocked_unexecuted" for row in self.read_json(f"{archive.REL_PHASE_ROOT}/x1/portfolios/blocked.json")["rows"]))

    def test_07_successor_recommendations_are_zero_credit_seeds(self) -> None:
        document = self.read_json(f"{archive.REL_PHASE_ROOT}/x1/successor-recommendations-freeze.json")
        self.assertEqual(document["state"], "zero_credit_seed_only")
        self.assertEqual({key: len(document[key]) for key in ("candidates", "skills", "runners", "clean_fix_refine")}, {"candidates": 15, "skills": 10, "runners": 10, "clean_fix_refine": 30})
        for key in ("candidates", "skills", "runners", "clean_fix_refine"):
            self.assertTrue(all(row["completion_credit"] == 0 and row["state"] == "recommended_zero_credit" for row in document[key]))
        self.assertEqual(document["practice"]["completion_credit"], 0)

    def test_08_source_ledger_preserves_credit_boundaries(self) -> None:
        rows = self.read_json(f"{archive.REL_PHASE_ROOT}/x1/source-ledger.json")["sources"]
        self.assertEqual(len(rows), 9)
        self.assertEqual(len({row["source_id"] for row in rows}), 9)
        self.assertTrue(all(row["url"].startswith("https://") and row["use"] and row["credit_boundary"] for row in rows))
        self.assertEqual({row["source_id"] for row in rows}, {row["source_id"] for row in archive.SOURCE_LEDGER})

    def test_09_method_flow_shards_are_complete_and_append_only(self) -> None:
        index = self.read_json(f"{archive.REL_PHASE_ROOT}/method-flow/x1-ledger-index.json")
        methods, witnesses, events, recommendations = [], [], [], []
        for descriptor in index["shards"]:
            shard = self.read_json(descriptor["path"])
            self.assertEqual(shard["schema"], "ghc.family.method-flow-state.v1")
            self.assertEqual(shard["owner"], archive.OWNER)
            self.assertEqual(shard["phase"], archive.PHASE)
            methods.extend(shard["methods"])
            witnesses.extend(shard["witnesses"])
            events.extend(shard["state_events"])
            recommendations.extend(shard["recommendations"])
        count = len(builder.PREFREEZE_FAILURES)
        self.assertEqual((len(methods), len(witnesses), len(events), len(recommendations)), (count, count * 2, count * 4, count))
        self.assertEqual(len({row["method_id"] for row in methods}), count)
        self.assertEqual(Counter(row["result"] for row in witnesses), Counter({"fail": count, "pass": count}))
        self.assertEqual(len({negative for row in methods for negative in row["retained_negative_ids"]}), count)
        required_method = {"method_id", "title", "failure_signature", "trigger_preconditions", "privacy_class", "approval_class", "candidate_workaround", "validation_witness_ids", "recurrence_guard", "rollback", "recommendation_state", "supersedes", "protected_gates", "retained_negative_ids", "scope_boundary"}
        required_witness = {"witness_id", "method_id", "procedure", "scope", "expected", "observed", "result", "same_owner_only", "independent_reproduction", "retained_negative_ids", "boundary"}
        self.assertTrue(all(required_method <= set(row) for row in methods))
        self.assertTrue(all(required_witness <= set(row) for row in witnesses))
        grouped: dict[str, list[tuple[object, str]]] = defaultdict(list)
        for row in events:
            grouped[row["method_id"]].append((row["before"], row["after"]))
        expected_transitions = [(None, "observed"), ("observed", "candidate"), ("candidate", "validated"), ("validated", "preferred")]
        self.assertTrue(all(transitions == expected_transitions for transitions in grouped.values()))

    def test_10_overlay_arithmetic_retains_every_failure(self) -> None:
        summary = self.read_json(f"{archive.REL_PHASE_ROOT}/method-flow/x1-summary.json")
        count = len(builder.PREFREEZE_FAILURES)
        self.assertEqual(count, 34)
        self.assertEqual(summary["new_prefreeze_failures"], count)
        self.assertEqual(summary["new_bounded_recoveries"], count)
        self.assertEqual(summary["x1_overlay"], {"effective_negatives": 30142 + count, "methods": 16568 + count, "failed_witnesses": 2283 + count, "passing_witnesses": 3110 + count, "open_gaps": 221, "exact_gates": 216})
        self.assertFalse(summary["failure_erasure"])
        self.assertEqual(summary["canonical_credit"], 0)

    def test_11_route_and_workflow_remain_unexecuted(self) -> None:
        route = self.read_json(f"{archive.REL_PHASE_ROOT}/x1/route-state.json")
        self.assertEqual(route["state"], "NOT_PREPARED_NOT_SENT")
        self.assertFalse(route["successor_contacted"] or route["successor_precontacted"] or route["successor_task_created"])
        workflow = self.read_json(f"{archive.REL_PHASE_ROOT}/x1/workflow-plan-freeze.json")
        self.assertTrue(workflow["strict_x1_before_x2"])
        self.assertFalse(workflow["x2_started"])
        self.assertFalse(workflow["full_repository_suite_authorized"])
        self.assertEqual(workflow["canonical_invocation_count"], 0)
        self.assertFalse(workflow["success_replay_allowed"])

    def test_12_git_blob_manifest_replays_exactly(self) -> None:
        manifest_path = f"{archive.REL_PHASE_ROOT}/validation/x1-manifest.json"
        staged_review_path = f"{archive.REL_PHASE_ROOT}/validation/x1-staged-review.json"
        manifest = self.read_json(manifest_path)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["self_exclusions"], [manifest_path, staged_review_path])
        for row in manifest["entries"]:
            blob = git("cat-file", "blob", row["git_blob_oid"], binary=True)
            self.assertEqual(len(blob), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"], row["path"])
            if self.x1_commit:
                self.assertEqual(git("rev-parse", f"{self.x1_commit}:{row['path']}"), row["git_blob_oid"], row["path"])
            else:
                result = subprocess.run(["git", "-C", str(ROOT), "hash-object", f"--path={row['path']}", "--stdin"], input=(ROOT / row["path"]).read_bytes(), check=True, capture_output=True)
                self.assertEqual(result.stdout.decode("ascii").strip(), row["git_blob_oid"], row["path"])
        allowlist = self.read_json(f"{archive.REL_PHASE_ROOT}/validation/x1-staged-allowlist.json")["paths"]
        self.assertEqual(set(allowlist), {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"]))

    def test_13_documents_stay_under_declared_ceilings(self) -> None:
        paths = self.x1_paths()
        self.assertLessEqual(len(paths) + 3, 2000)
        total = 0
        for path in paths:
            text = self.read_bytes(path).decode("utf-8")
            words = len(re.findall(r"\b\w+[\w'-]*\b", text))
            self.assertLessEqual(words, 6000, path)
            total += words
        self.assertLessEqual(total, 100000)

    def test_14_no_private_route_or_raw_identifier_payload(self) -> None:
        paths = self.x1_paths() + ["scripts/ghc_family_liora_venn_v668_v8_archive.py", "scripts/build_ghc_family_liora_venn_v668_v8_x1.py", "scripts/validate_ghc_family_liora_venn_v668_v8_x1.py", "tests/test_ghc_family_liora_venn_v668_v8_x1.py"]
        combined = "\n".join(self.read_bytes(path).decode("utf-8") for path in paths)
        forbidden_tokens = ["<" + "codex" + "_delegation", "source" + "_thread" + "_id", "session" + "_meta.payload.id", "response" + "_item"]
        self.assertTrue(all(token.casefold() not in combined.casefold() for token in forbidden_tokens))
        self.assertNotIn("C:" + chr(92), combined)
        self.assertNotIn("D:" + chr(92), combined)
        self.assertIsNone(re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", combined, re.IGNORECASE))

    def test_15_changed_python_has_no_high_risk_execution_surface(self) -> None:
        for relative in ("scripts/ghc_family_liora_venn_v668_v8_archive.py", "scripts/build_ghc_family_liora_venn_v668_v8_x1.py", "scripts/validate_ghc_family_liora_venn_v668_v8_x1.py", "tests/test_ghc_family_liora_venn_v668_v8_x1.py"):
            tree = ast.parse(self.read_bytes(relative).decode("utf-8"), filename=relative)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
                    self.assertFalse(any(name.split(".")[0] in {"requests", "socket", "urllib", "http", "ftplib"} for name in names), relative)
                if isinstance(node, ast.Call):
                    self.assertFalse(any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords), relative)

    def test_16_boundaries_and_verdict_are_present(self) -> None:
        overview = self.read_bytes(f"{archive.REL_PHASE_ROOT}/x1/integrated-overview.md").decode("utf-8")
        for token in (archive.TERMINAL_VERDICT, archive.SOURCE_TERMINAL_STATUS, "same-owner", "Māori authority", "Theory of Everything", "not independent reproduction"):
            self.assertIn(token, overview)


if __name__ == "__main__":
    unittest.main()
