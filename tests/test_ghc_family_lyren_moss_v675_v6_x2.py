from __future__ import annotations

import hashlib
import json
import os
import py_compile
import runpy
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "lyren-moss" / "v675-v6"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
X1_COMMIT = "920c8e89dff0c4625087a52a3dc5ee2916b0b659"
SOURCE_FINAL = "0aa1f2b1250e5540650b683d221f92e8762cd991"
BRANCH = "codex/GHC-Family/lyren-moss-v675-v6-full-tools"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(name: str):
    return json.loads((X2 / name).read_text(encoding="utf-8"))


class LyrenV675V6X2Tests(unittest.TestCase):
    def test_lifecycle_head_is_x1_or_direct_evidence_child(self) -> None:
        branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        count = int(subprocess.check_output(["git", "rev-list", "--count", f"{X1_COMMIT}..{head}"], cwd=ROOT, text=True).strip())
        ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", X1_COMMIT, head], cwd=ROOT).returncode == 0
        self.assertEqual(BRANCH, branch)
        self.assertTrue(ancestor)
        self.assertLessEqual(count, 1)
        self.assertEqual(SOURCE_FINAL, subprocess.check_output(["git", "rev-parse", f"{X1_COMMIT}^"], cwd=ROOT, text=True).strip())

    def test_all_x2_json_parses(self) -> None:
        paths = sorted(X2.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 56)
        for path in paths:
            with self.subTest(path=path.as_posix()):
                json.loads(path.read_text(encoding="utf-8"))

    def test_forty_contracts_and_outcomes(self) -> None:
        contract_paths = sorted((X2 / "proposal-contracts").glob("*.json"))
        self.assertEqual(40, len(contract_paths))
        rows = load("proposal-outcomes.json")["rows"]
        self.assertEqual(40, len(rows))
        counts = Counter(row["core_outcome"] for row in rows)
        self.assertEqual({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}, dict(counts))
        self.assertEqual(ALLOWED, set(counts))
        self.assertTrue(all(row["synthetic_only"] and row["external_actions"] == 0 for row in rows))

    def test_every_contract_has_four_exact_rejections(self) -> None:
        rows = load("proposal-outcomes.json")["rows"]
        for row in rows:
            with self.subTest(proposal=row["proposal_id"]):
                mutations = row["rejecting_mutations"]
                self.assertEqual(4, len(mutations))
                self.assertTrue(all(item["rejected"] for item in mutations))
                self.assertTrue(all(item["completion_credit"] == 0 for item in mutations))

    def test_one_hundred_sixty_mutations_retained(self) -> None:
        data = load("rejecting-mutations.json")
        self.assertEqual(160, len(data["rows"]))
        self.assertEqual(160, data["preregistered"])
        self.assertEqual(160, data["executed"])
        self.assertEqual(160, data["rejected"])
        self.assertEqual(0, data["completion_credit"])
        self.assertTrue(data["retained"])
        reasons = Counter(row["actual_failure_code"] for row in data["rows"])
        self.assertEqual({"synthetic_identity": 40, "interval_domain": 40, "unit_domain": 40, "datum_ambiguity": 40}, dict(reasons))

    def test_positive_controls(self) -> None:
        data = load("positive-controls.json")
        self.assertEqual(40, data["executed"])
        self.assertEqual(40, data["passed"])
        self.assertTrue(all(row["passed"] for row in data["rows"]))
        self.assertTrue(all(row["normalized"]["synthetic_only"] for row in data["rows"]))

    def test_portfolio_execution_counts(self) -> None:
        data = load("portfolio-outcomes.json")
        self.assertEqual(
            {
                "safe_now_executed": 60,
                "candidates_evaluated": 30,
                "exact_packets_protected": 20,
                "blocked_packets_retained": 10,
                "owner_clean_fix_refine_executed": 60,
                "successor_clean_fix_refine_recommended": 30,
            },
            data["counts"],
        )
        self.assertTrue(all(row["executed"] for row in data["safe_now_tasks"]))
        self.assertTrue(all(row["executed"] for row in data["candidate_tasks"]))
        self.assertTrue(all(not row["executed"] for row in data["exact_approval_packets"]))
        self.assertTrue(all(not row["executed"] for row in data["blocked_packets"]))

    def test_twenty_repo_local_skills(self) -> None:
        skills = sorted((X2 / "skills").glob("*/SKILL.md"))
        data = load("skill-creator-validation.json")
        self.assertEqual(20, len(skills))
        self.assertEqual(20, data["built"])
        self.assertEqual(20, data["validated"])
        self.assertEqual(0, data["globally_installed"])
        self.assertFalse(data["shared_skill_bank_mutated"])
        for path in skills:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.parent.name):
                self.assertTrue(text.startswith("---\nname: "))
                self.assertIn("description:", text)
                self.assertIn("## Boundary", text)

    def test_skill_usage(self) -> None:
        data = load("skill-usage.json")
        self.assertEqual(20, data["used"])
        self.assertEqual(20, len(data["rows"]))
        self.assertTrue(all(row["validated"] and row["used"] for row in data["rows"]))

    def test_ten_repo_local_runners_compile_and_smoke(self) -> None:
        paths = sorted((X2 / "runners").glob("*.py"))
        data = load("runner-validation.json")
        self.assertEqual(10, len(paths))
        self.assertEqual(10, data["compiled"])
        self.assertEqual(10, data["smoke_passed"])
        sys.pycache_prefix = os.environ.get("PYTHONPYCACHEPREFIX")
        for index, path in enumerate(paths, 1):
            with self.subTest(path=path.name):
                py_compile.compile(str(path), doraise=True)
                namespace = runpy.run_path(str(path), run_name=f"x2_test_runner_{index}")
                result = namespace["evaluate"]({"synthetic_only": True, "external_actions": 0})
                self.assertTrue(result["passed"])

    def test_three_isolated_tool_versions_and_hashes(self) -> None:
        data = load("tool-validation.json")
        self.assertEqual({"Pint": "0.25.3", "portion": "2.6.2", "cattrs": "26.1.0"}, data["versions"])
        self.assertEqual("27eb25143bd5de9fcc4d5a4b484f16faf6b4615aa93ece6b3373a8c1a3c1b97d", data["wheel_sha256"]["Pint"])
        self.assertEqual("86be115afafa776174dc5eac82afb6496c9fa3684f5b3a844c3139535c51085e", data["wheel_sha256"]["portion"])
        self.assertEqual("d1e0804c42639494d469d08d4f26d6b9de9b8ab26b446db7b5f8c2e97f7c3096", data["wheel_sha256"]["cattrs"])
        self.assertFalse(data["shared_prefix_mutated"])
        self.assertEqual(1500.0, data["pint_smoke"]["converted_millimetres"])

    def test_provenance_graph_and_intervals(self) -> None:
        graph = load("datum-provenance-state-graph.json")
        self.assertEqual(40, graph["node_count"])
        self.assertEqual(39, graph["edge_count"])
        self.assertEqual(1, graph["root_count"])
        self.assertEqual(0, graph["overlaps"])
        self.assertEqual(0, graph["real_entities"])
        self.assertEqual("[10,410)", graph["timeline"])
        self.assertEqual(40, len({row["sha256"] for row in graph["nodes"]}))

    def test_source_adapter_is_transport_disabled(self) -> None:
        data = load("source-adapter.json")
        self.assertEqual("disabled", data["transport"])
        self.assertEqual(0, data["network_calls"])
        self.assertEqual(0, data["external_rows"])
        self.assertEqual(0, data["writes"])

    def test_source_application_is_context_only(self) -> None:
        data = load("source-application-ledger.json")
        self.assertEqual(6, len(data["rows"]))
        self.assertTrue(all(not row["empirical_credit"] for row in data["rows"]))
        self.assertEqual(0, data["real_rows"])
        self.assertEqual(0, data["external_actions"])

    def test_flashcard_deck(self) -> None:
        data = load("freed-id-flashcard-deck.json")
        self.assertEqual(40, data["card_count"])
        self.assertEqual(40, len(data["cards"]))
        self.assertEqual(ALLOWED, {row["core_outcome"] for row in data["cards"]})
        self.assertTrue(all(not row["credential_claim"] for row in data["cards"]))
        self.assertFalse(data["memory_or_identity_continuity_claim"])

    def test_x2_working_overlay(self) -> None:
        overlay = load("phase-truth.json")["working_overlay"]
        self.assertEqual(41113, overlay["effective_negatives"])
        self.assertEqual(29405, overlay["method_flow_methods"])
        self.assertEqual(12774, overlay["failed_witnesses"])
        self.assertEqual(16856, overlay["bounded_passing_witnesses"])
        self.assertEqual(341, overlay["open_gaps"])
        self.assertEqual(333, overlay["exact_gates"])
        self.assertEqual(7270, overlay["declared_proposals"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", overlay["terminal_verdict"])

    def test_source_seal_is_not_rewritten(self) -> None:
        data = load("source-count-overlay.json")
        self.assertEqual(40947, data["vesper_repository_seal"]["effective_negatives"])
        self.assertEqual(40948, data["activation_overlay"]["effective_negatives"])
        self.assertEqual(40953, data["lyren_x1_overlay"]["effective_negatives"])
        self.assertEqual(41113, data["lyren_x2_overlay"]["effective_negatives"])
        self.assertFalse(data["source_seal_rewritten"])

    def test_method_flow_retains_failures(self) -> None:
        data = load("method-flow.json")
        self.assertEqual(205, data["phase_rows"])
        self.assertFalse(data["failure_erasure"])
        failed = [row for row in data["rows"] if row.get("failed_witness")]
        passing = [row for row in data["rows"] if row.get("bounded_passing_witness")]
        self.assertEqual(160, len(failed))
        self.assertEqual(200, len(passing))

    def test_accessible_report_structure_and_boundary(self) -> None:
        text = (X2 / "accessible-report.html").read_text(encoding="utf-8")
        for token in ("<main", "<h1>", "<h2>", "<caption>", "scope=\"col\"", "scope='row'", "Skip to main content", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, text)
        self.assertIn("not an affected-user accessibility evaluation", text)

    def test_completion_checklist_preserves_terminal_false(self) -> None:
        data = load("completion-checklist.json")
        self.assertTrue(all(value for key, value in data["checks"].items() if key != "terminal_ready"))
        self.assertFalse(data["checks"]["terminal_ready"])
        self.assertEqual("NOT_READY_FOR_STAGE_20", data["terminal_verdict"])

    def test_no_successor_contact_or_canonical_claim(self) -> None:
        truth = load("phase-truth.json")
        self.assertFalse(truth["canonical_validation_invoked"])
        self.assertFalse(truth["successor_contacted"])
        self.assertEqual("x2_evidence_built_not_final", truth["lifecycle"])

    def test_no_crlf_in_x2_owner_text(self) -> None:
        paths = [path for path in X2.rglob("*") if path.is_file()]
        paths += [ROOT / "scripts" / "build_ghc_family_lyren_moss_v675_v6_x2.py", ROOT / "tests" / "test_ghc_family_lyren_moss_v675_v6_x2.py"]
        for path in paths:
            with self.subTest(path=path.as_posix()):
                self.assertNotIn(b"\r\n", path.read_bytes())

    def test_owner_docs_have_no_private_route_or_path_material(self) -> None:
        forbidden = ("source_thread_id", "clientThreadId", "threadId", "C:\\Users\\", "D:\\GHC-Archives\\", "api_key", "access_token", "refresh_token")
        for path in [item for item in X2.rglob("*") if item.is_file()]:
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                with self.subTest(path=path.name, token=token):
                    self.assertNotIn(token, text)

    def test_owner_file_ceiling(self) -> None:
        owner_files = [path for path in BASE.rglob("*") if path.is_file()]
        owner_files += [path for path in (ROOT / "scripts").glob("*lyren_moss_v675_v6*.py")]
        owner_files += [path for path in (ROOT / "tests").glob("*lyren_moss_v675_v6*.py")]
        self.assertLess(len(owner_files), 2000)

    def test_evidence_manifest_replays_staged_and_x1_blobs(self) -> None:
        manifest = json.loads((VALIDATION / "evidence-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(23, manifest["immutable_x1_count"])
        self.assertGreaterEqual(manifest["staged_x2_count"], 90)
        for entry in manifest["staged_x2_entries"]:
            with self.subTest(staged=entry["path"]):
                row = subprocess.check_output(["git", "ls-files", "-s", "--", entry["path"]], cwd=ROOT, text=True).split()
                self.assertEqual(entry["git_blob"], row[1])
                blob = subprocess.check_output(["git", "cat-file", "blob", row[1]], cwd=ROOT)
                self.assertEqual(entry["sha256"], hashlib.sha256(blob).hexdigest())
        for entry in manifest["immutable_x1_entries"]:
            with self.subTest(x1=entry["path"]):
                oid = subprocess.check_output(["git", "rev-parse", f"{X1_COMMIT}:{entry['path']}"], cwd=ROOT, text=True).strip()
                self.assertEqual(entry["git_blob"], oid)

    def test_evidence_staged_review_and_privacy(self) -> None:
        review = json.loads((VALIDATION / "evidence-staged-review.json").read_text(encoding="utf-8"))
        privacy = json.loads((VALIDATION / "evidence-staged-privacy.json").read_text(encoding="utf-8"))
        self.assertEqual(0, review["deletions"])
        self.assertEqual(0, review["renames"])
        self.assertEqual(0, review["confirmed_privacy_hits"])
        self.assertTrue(review["within_file_ceiling"])
        self.assertFalse(review["canonical_aggregate_invoked"])
        self.assertEqual(0, privacy["confirmed_hit_count"])
        self.assertFalse(privacy["complete_privacy_claim"])


if __name__ == "__main__":
    unittest.main()
