from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

import jsonschema
import networkx as nx
import rfc8785


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "lyren-moss" / "v673-v7"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
X1_COMMIT = "786654cf8f28bb8c7abed41fb8f8315ab65f7e83"
FOUR_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


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


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.main = 0
        self.tables = 0
        self.captions = 0
        self.scoped_headers = 0
        self.lang = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html" and values.get("lang"):
            self.lang = True
        if tag == "main":
            self.main += 1
        if tag == "table":
            self.tables += 1
        if tag == "caption":
            self.captions += 1
        if tag == "th" and values.get("scope") in {"row", "col"}:
            self.scoped_headers += 1


class LyrenMossV673V7X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.proposals = read_json(X1 / "proposals.json")
        cls.results = read_json(X2 / "proposal-results.json")
        cls.positives = read_json(X2 / "positive-controls.json")
        cls.mutations = read_json(X2 / "mutation-register.json")
        cls.tasks = read_json(X2 / "task-execution-ledger.json")
        cls.skills = read_json(X2 / "skill-bank.json")
        cls.runners = read_json(X2 / "runner-bank.json")
        cls.cfr = read_json(X2 / "clean-fix-refine-ledger.json")
        cls.successor = read_json(X2 / "successor-recommendations.json")
        cls.cards = read_json(X2 / "cards" / "four-tier-deck.json")
        cls.graph = read_json(X2 / "provenance-graph.json")
        cls.methods = read_json(X2 / "method-flow.json")
        cls.negatives = read_json(X2 / "retained-negatives.json")
        cls.approvals = read_json(X2 / "approval-packet-state.json")
        cls.gates = read_json(X2 / "open-gap-and-gate-register.json")
        cls.tools = read_json(X2 / "toolchain-receipt.json")
        cls.practices = read_json(X2 / "practice-lens-results.json")
        cls.sources = read_json(X2 / "official-source-use.json")
        cls.checks = read_json(X2 / "x2-build-checks.json")
        cls.schema = read_json(X2 / "schemas" / "proposal-evidence.schema.json")

    def test_x1_is_immutable_ancestor(self) -> None:
        self.assertEqual(git("merge-base", "--is-ancestor", X1_COMMIT, "HEAD"), "")
        committed_delta = git("diff", "--name-only", f"{X1_COMMIT}..HEAD").splitlines()
        self.assertFalse(any(path.startswith("docs/lyren-moss/v673-v7/x1/") for path in committed_delta))

    def test_forty_results_and_exact_four_outcomes(self) -> None:
        self.assertEqual(self.results["result_count"], 40)
        self.assertEqual(len(self.results["results"]), 40)
        self.assertEqual(self.results["declared_chain_before"], 6470)
        self.assertEqual(self.results["declared_chain_after"], 6510)
        counts = Counter(row["outcome"] for row in self.results["results"])
        self.assertEqual(set(counts), FOUR_OUTCOMES)
        self.assertEqual(dict(counts), {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(self.results["outcome_counts"], dict(counts))
        self.assertTrue(self.results["same_owner_not_independent_reproduction"])

    def test_all_declared_artifacts_exist_and_match_recorded_hashes(self) -> None:
        self.assertEqual(len({row["artifact_path"] for row in self.results["results"]}), 40)
        for row in self.results["results"]:
            path = ROOT / row["artifact_path"]
            data = normalized(path.read_bytes())
            with self.subTest(proposal=row["proposal_id"]):
                self.assertTrue(path.is_file())
                self.assertEqual(row["artifact_bytes_normalized_lf"], len(data))
                self.assertEqual(row["artifact_sha256_normalized_lf"], hashlib.sha256(data).hexdigest())

    def test_every_json_proposal_artifact_validates_and_recanonicalizes(self) -> None:
        checked = 0
        for row in self.results["results"]:
            path = ROOT / row["artifact_path"]
            if path.suffix != ".json":
                continue
            payload = read_json(path)
            jsonschema.validate(payload, self.schema)
            declared = payload.pop("canonical_payload_sha256")
            actual = hashlib.sha256(rfc8785.dumps(payload)).hexdigest()
            with self.subTest(proposal=row["proposal_id"]):
                self.assertEqual(declared, actual)
                self.assertEqual(declared, row["canonical_payload_sha256"])
                self.assertTrue(payload["synthetic"])
                self.assertEqual(payload["real_rows"], 0)
                self.assertEqual(payload["external_calls"], 0)
                self.assertFalse(payload["authority_claim"])
            checked += 1
        self.assertEqual(checked, 39)

    def test_thirty_six_bounded_positive_controls(self) -> None:
        rows = self.positives["rows"]
        self.assertEqual(self.positives["bounded_passing_count"], 36)
        self.assertEqual(len(rows), 36)
        self.assertEqual(len({row["control_id"] for row in rows}), 36)
        self.assertTrue(all(row["state"] == "bounded_passing" for row in rows))
        self.assertTrue(all(not row["independent_reproduction"] for row in rows))
        self.assertEqual(self.positives["real_rows"], 0)

    def test_all_160_preregistered_mutations_executed_rejected_and_retained(self) -> None:
        rows = self.mutations["rows"]
        self.assertEqual(self.mutations["preregistered_count"], 160)
        self.assertEqual(self.mutations["executed_count"], 160)
        self.assertEqual(self.mutations["rejected_count"], 160)
        self.assertEqual(len(rows), 160)
        self.assertEqual(len({row["mutation_id"] for row in rows}), 160)
        self.assertEqual(Counter(row["proposal_id"] for row in rows), Counter({f"LM6737-N{i:03d}": 4 for i in range(1, 41)}))
        self.assertEqual(
            Counter(row["mutation_type"] for row in rows),
            Counter({"missing_synthetic_flag": 40, "real_message_injection": 40, "external_action_upgrade": 40, "authority_upgrade": 40}),
        )
        self.assertTrue(all(row["state"] == "rejected" and row["retained"] for row in rows))
        self.assertTrue(all(row["completion_credit"] == 0 for row in rows))

    def test_sixty_safe_and_thirty_candidate_tasks_executed_bounded(self) -> None:
        self.assertEqual(self.tasks["safe_now_executed"], 60)
        self.assertEqual(self.tasks["candidate_executed"], 30)
        self.assertEqual(len(self.tasks["safe_now"]), 60)
        self.assertEqual(len(self.tasks["candidate"]), 30)
        self.assertTrue(all(row["execution_state"] == "executed_bounded" for row in self.tasks["safe_now"]))
        self.assertTrue(all(row["execution_state"] == "executed_dependency_closed_analysis" for row in self.tasks["candidate"]))
        self.assertTrue(all(row["outcome"] in FOUR_OUTCOMES for row in [*self.tasks["safe_now"], *self.tasks["candidate"]]))
        self.assertTrue(all(not row["external_action"] for row in [*self.tasks["safe_now"], *self.tasks["candidate"]]))

    def test_exact_and_blocked_packets_remain_held(self) -> None:
        self.assertEqual(len(self.tasks["exact_approval"]), 20)
        self.assertEqual(len(self.tasks["blocked"]), 10)
        self.assertTrue(all(row["execution_state"] == "held_unexecuted" for row in self.tasks["exact_approval"]))
        self.assertTrue(all(row["execution_state"] == "held_unexecuted" for row in self.tasks["blocked"]))
        self.assertTrue(all(row["completion_credit"] == 0 for row in [*self.tasks["exact_approval"], *self.tasks["blocked"]]))
        self.assertEqual(self.approvals["exact_external_actions"], 0)
        self.assertEqual(self.approvals["blocked_actions"], 0)

    def test_twenty_skill_and_ten_runner_cards_built_tested_used(self) -> None:
        self.assertEqual(self.skills["skill_count"], 20)
        self.assertEqual(len(self.skills["skills"]), 20)
        self.assertEqual(self.runners["runner_count"], 10)
        self.assertEqual(len(self.runners["runners"]), 10)
        for row in self.skills["skills"]:
            self.assertTrue(row["build_witness"] and row["test_witness"] and row["use_witness"])
            self.assertFalse(row["global_installation"])
            self.assertFalse(row["shared_prefix_mutation"])
            self.assertEqual(row["outcome"], "completed")
        for row in self.runners["runners"]:
            self.assertTrue(row["build_witness"] and row["test_witness"] and row["use_witness"])
            self.assertEqual(row["network_calls"], 0)
            self.assertEqual(row["subagents"], 0)

    def test_sixty_additive_clean_fix_refine_tasks_have_no_deletion(self) -> None:
        self.assertEqual(self.cfr["executed_count"], 60)
        self.assertEqual(len(self.cfr["rows"]), 60)
        self.assertEqual(self.cfr["deletions"], 0)
        self.assertTrue(all(row["execution_state"] == "executed_additive_review" for row in self.cfr["rows"]))
        self.assertTrue(all(not row["deletion"] and not row["cross_owner_mutation"] for row in self.cfr["rows"]))

    def test_successor_recommendations_are_exact_and_zero_credit(self) -> None:
        self.assertEqual(self.successor["prospective_owner"], "Ilyra Fen")
        self.assertEqual(self.successor["prospective_phase"], "v673-v8")
        self.assertEqual(len(self.successor["skills"]), 10)
        self.assertEqual(len(self.successor["runners"]), 10)
        self.assertEqual(len(self.successor["clean_fix_refine"]), 30)
        self.assertEqual(self.successor["practice"]["count"], 1)
        self.assertEqual(self.successor["current_completion_credit"], 0)
        self.assertFalse(self.successor["precontact_performed"])

    def test_four_tier_deck_has_160_unique_cards(self) -> None:
        rows = self.cards["cards"]
        self.assertEqual(self.cards["card_count"], 160)
        self.assertEqual(len(rows), 160)
        self.assertEqual(len({row["card_id"] for row in rows}), 160)
        self.assertEqual(self.cards["tier_counts"], {"authority": 40, "contract": 40, "failure": 40, "signal": 40})
        self.assertEqual(set(row["outcome"] for row in rows), FOUR_OUTCOMES)
        self.assertTrue(all(row["synthetic"] for row in rows))

    def test_provenance_graph_is_dag_and_cycle_mutation_rejected(self) -> None:
        self.assertEqual(self.graph["node_count"], 81)
        self.assertEqual(self.graph["edge_count"], 80)
        graph = nx.DiGraph((row["from"], row["to"]) for row in self.graph["edges"])
        self.assertTrue(nx.is_directed_acyclic_graph(graph))
        self.assertEqual(len(list(nx.topological_sort(graph))), 81)
        self.assertTrue(self.graph["dag_passed"])
        self.assertTrue(self.graph["cycle_mutation_rejected"])
        self.assertFalse(self.graph["external_interoperability_claim"])

    def test_method_flow_counts_are_transparently_additive(self) -> None:
        self.assertEqual(len(self.methods["inherited_startup_methods"]), 12)
        self.assertGreaterEqual(len(self.methods["current_x2_methods"]), 2)
        self.assertEqual(len(self.methods["proposal_methods"]), 40)
        counts = self.methods["counts"]
        operational = 12 + len(self.methods["current_x2_methods"])
        self.assertEqual(counts["inherited_repository_methods"], 23764)
        self.assertEqual(counts["operational_methods_added"], operational)
        self.assertEqual(counts["proposal_methods_added"], 40)
        self.assertEqual(counts["effective_methods"], 23764 + operational + 40)
        self.assertEqual(counts["retained_failed_witnesses"], 9097 + operational + 160)
        self.assertEqual(counts["bounded_passing_witnesses"], 11373 + operational + 36 + 6)
        self.assertTrue(self.methods["same_owner_not_independent_reproduction"])

    def test_retained_negative_total_includes_operations_and_mutations(self) -> None:
        self.assertEqual(self.negatives["repository_sealed_baseline"], 37436)
        self.assertEqual(self.negatives["x1_operational_failures"], 12)
        x2_failures = len(self.methods["current_x2_methods"])
        self.assertEqual(self.negatives["x2_operational_failures"], x2_failures)
        self.assertEqual(self.negatives["mutation_rejections"], 160)
        self.assertEqual(self.negatives["effective_negatives"], 37436 + 12 + x2_failures + 160)
        self.assertEqual(len(self.negatives["rows"]), 160)
        self.assertEqual(len(self.negatives["operational_negative_ids"]), 12 + x2_failures)

    def test_open_gap_gate_and_stage20_counts(self) -> None:
        self.assertEqual(self.gates["effective_open_gaps"], 305)
        self.assertEqual(self.gates["effective_exact_gates"], 298)
        self.assertEqual(len(self.gates["open_gap_proposals"]), 2)
        self.assertEqual(len(self.gates["exact_gate_proposals"]), 2)
        self.assertEqual(self.gates["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_all_eight_wheels_and_three_selected_tools_are_verified(self) -> None:
        self.assertEqual(self.tools["wheel_count"], 8)
        self.assertEqual(len(self.tools["wheels"]), 8)
        self.assertTrue(all(row["verified"] and row["sha256"] == row["actual_sha256"] for row in self.tools["wheels"]))
        self.assertEqual(self.tools["installed_versions"]["rfc8785"], "0.1.4")
        self.assertEqual(self.tools["installed_versions"]["jsonschema"], "4.26.0")
        self.assertEqual(self.tools["installed_versions"]["networkx"], "3.6.1")
        self.assertEqual(self.tools["selected_tool_licenses"], {"jsonschema": "MIT", "networkx": "BSD-3-Clause", "rfc8785": "Apache-2.0"})
        self.assertTrue(all(self.tools["smoke"].get(key) is True for key in ["rfc8785_positive", "jsonschema_positive", "jsonschema_invalid_rejected", "networkx_dag_positive", "networkx_cycle_rejected"]))
        self.assertEqual(self.tools["network_calls_during_build"], 0)
        self.assertFalse(self.tools["shared_python_or_npm_prefix_mutated"])

    def test_practice_and_source_boundaries(self) -> None:
        self.assertEqual(len(self.practices["lenses"]), 3)
        self.assertEqual(self.practices["successor_practice_count"], 1)
        self.assertEqual(self.practices["real_people_objects_messages_or_measurements"], 0)
        self.assertFalse(self.practices["professional_authority"])
        self.assertEqual(len(self.sources["sources"]), 6)
        self.assertEqual(self.sources["real_observations"], 0)
        self.assertFalse(self.sources["endorsement_or_authority"])

    def test_accessible_html_structure_and_manual_gap(self) -> None:
        for relative in ["accessibility/record-companion.html", "report/index.html"]:
            parser = StructureParser()
            text = (X2 / relative).read_text(encoding="utf-8")
            parser.feed(text)
            with self.subTest(path=relative):
                self.assertTrue(parser.lang)
                self.assertEqual(parser.main, 1)
                self.assertGreaterEqual(parser.tables, 1)
                self.assertGreaterEqual(parser.captions, 1)
                self.assertGreaterEqual(parser.scoped_headers, 1)
                self.assertIn("not performed", text.casefold())
                if relative.startswith("accessibility/"):
                    self.assertIn("not an accessibility-complete result", text.casefold())
                else:
                    self.assertIn("not accessibility-complete", text.casefold())

    def test_every_x2_json_parses_as_utf8(self) -> None:
        paths = sorted(X2.rglob("*.json"))
        self.assertEqual(len(paths), 59)
        for path in paths:
            with self.subTest(path=str(path.relative_to(X2))):
                self.assertIsInstance(read_json(path), dict)

    def test_build_checks_match_materialized_evidence(self) -> None:
        expected = {
            "proposal_results": 40,
            "positive_controls": 36,
            "invalid_mutations_executed": 160,
            "invalid_mutations_rejected": 160,
            "safe_now_executed": 60,
            "candidate_executed": 30,
            "skill_cards_built_tested_used": 20,
            "runner_cards_built_tested_used": 10,
            "clean_fix_refine_executed": 60,
            "successor_skill_recommendations": 10,
            "successor_runner_recommendations": 10,
            "successor_clean_fix_refine_recommendations": 30,
            "successor_practice_recommendations": 1,
            "cards": 160,
            "tool_wheels_verified": 8,
            "real_rows": 0,
            "external_actions": 0,
            "subagents": 0,
        }
        for key, value in expected.items():
            self.assertEqual(self.checks[key], value, key)
        self.assertTrue(self.checks["graph_dag_passed"])
        self.assertTrue(self.checks["graph_cycle_mutation_rejected"])
        self.assertEqual(self.checks["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_owner_docs_have_no_basic_private_identifier_hits(self) -> None:
        patterns = [
            re.compile(r"(?i)[A-Z]:[\\/](?:Users|GHC-Archives)[\\/]"),
            re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
            re.compile(r"(?i)(?:password|secret|token|api[_-]?key)\s*[:=]\s*['\"][^'\"]+['\"]"),
            re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
            re.compile(r"(?<!\w)\+\d[\d ()-]{7,}\d(?!\w)"),
        ]
        for path in sorted(X2.rglob("*")):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=str(path.relative_to(X2))):
                self.assertTrue(all(pattern.search(text) is None for pattern in patterns))

    def test_conditional_x2_staged_receipts_and_manifest_replay(self) -> None:
        review_path = VALIDATION / "x2-staged-review.json"
        privacy_path = VALIDATION / "x2-staged-privacy.json"
        security_path = VALIDATION / "x2-staged-security.json"
        manifest_path = VALIDATION / "x2-evidence-manifest.json"
        paths = [review_path, privacy_path, security_path, manifest_path]
        if not any(path.exists() for path in paths):
            self.skipTest("x2 staged receipts are intentionally generated after the first focused pass")
        self.assertTrue(all(path.exists() for path in paths))
        review = read_json(review_path)
        privacy = read_json(privacy_path)
        security = read_json(security_path)
        manifest = read_json(manifest_path)
        self.assertTrue(review["passed"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["x1_paths"], [])
        self.assertEqual(review["deletions"], [])
        self.assertTrue(privacy["passed"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(security["passed"])
        self.assertEqual(security["bounded_ast_finding_count"], 0)
        staged = set(git("diff", "--cached", "--name-only").splitlines())
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            data = git_bytes("show", f":{row['path']}") if row["path"] in staged else git_bytes("show", f"HEAD:{row['path']}")
            data = normalized(data)
            with self.subTest(manifest_path=row["path"]):
                self.assertEqual(row["bytes"], len(data))
                self.assertEqual(row["sha256_normalized_lf"], hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    unittest.main()
