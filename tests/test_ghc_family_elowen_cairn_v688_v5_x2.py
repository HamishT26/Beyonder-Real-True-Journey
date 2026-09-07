#!/usr/bin/env python3
"""Owner-local x2 evidence tests for Elowen Cairn v688-v5."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_go_sgf_core as core  # noqa: E402

BASE = ROOT / "docs" / "elowen-cairn" / "v688-v5"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
SOURCE = "adadd367036e49cfb5c480f2aa0b598c164cac1c"
X1_COMMIT = "a4fffe1213f944e0017a8dd81f227d98785d43d1"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> bytes:
    proc = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        raise AssertionError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout


class ElowenV688V5X2Tests(unittest.TestCase):
    def test_all_frozen_contracts(self):
        proposals = load(X1 / "new-proposal-freeze.json")["proposals"]
        self.assertEqual(len(proposals), 200)
        failures = []
        for row in proposals:
            check = core.validate_against_freeze(row["input"], row["expected_acceptance"], row["expected_error"])
            if not check["valid"]:
                failures.append(row["proposal_id"])
        self.assertEqual(failures, [])

    def test_contract_materialization(self):
        combined = load(X2 / "contract-results.json")
        files = sorted((X2 / "contracts").glob("*.json"))
        self.assertEqual(combined["count"], 200)
        self.assertEqual(combined["valid_count"], 200)
        self.assertEqual(len(files), 200)
        self.assertTrue(all(row["contract_valid"] and row["input_unchanged"] for row in combined["results"]))

    def test_rejecting_output_mutations(self):
        data = load(X2 / "rejecting-output-mutations.json")
        self.assertEqual(data["count"], 200)
        self.assertEqual(data["detected_count"], 200)
        self.assertTrue(all(row["completion_credit"] == 0 for row in data["mutations"]))

    def test_portfolio_execution_and_holds(self):
        data = load(X2 / "portfolio-results.json")
        self.assertEqual(data["safe_passed"], 300)
        self.assertEqual(data["candidate_rejections"], 250)
        self.assertEqual(data["cfr_passed"], 300)
        self.assertEqual(data["exact_executed"], 0)
        self.assertEqual(data["blocked_executed"], 0)
        self.assertEqual(len(data["exact_packets"]), 50)
        self.assertEqual(len(data["blocked_packets"]), 30)

    def test_strict_json_and_field_closure(self):
        with self.assertRaisesRegex(ValueError, "DUPLICATE_KEY"):
            core.strict_loads('{"operation":"property_identifier","identifier":"FF","identifier":"GM"}')
        payload = {"operation": "property_identifier", "identifier": "FF", "execute": True}
        self.assertEqual(core.evaluate(payload), core.err("FIELD_SET"))

    def test_package_transaction(self):
        data = load(X2 / "package-transaction.json")
        self.assertEqual(data["status"], "COMPLETE")
        self.assertTrue(data["smoke_valid"])
        self.assertEqual(data["installed_versions"], {"networkx": "3.6.1", "sgfmill": "1.1.1", "wcwidth": "0.8.3"})
        self.assertEqual(data["positive_smoke_count"], 3)
        self.assertEqual(data["adverse_smoke_count"], 3)
        self.assertTrue(data["advisory_query_complete"])
        self.assertFalse(data["independent_reproduction"])

    def test_skill_and_runner_promotion(self):
        data = load(X2 / "promotion-receipt.json")
        self.assertEqual(data["status"], "COMPLETE")
        self.assertEqual(data["skills_promoted"], 10)
        self.assertEqual(data["runners_promoted"], 5)
        self.assertEqual(data["overwrites"], 0)
        self.assertEqual(data["deletions"], 0)
        self.assertEqual(len(data["files"]), data["parity_files"])
        self.assertTrue(all(row["byte_equal"] for row in data["files"]))

    def test_local_skills_are_complete(self):
        skills = sorted(path for path in (BASE / "skills").iterdir() if path.is_dir())
        self.assertEqual(len(skills), 10)
        for skill in skills:
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\nname: ghc-family-"))
            self.assertNotIn("TODO", text)
            metadata = (skill / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn("default_prompt:", metadata)
            self.assertIn("$" + skill.name, metadata)
            self.assertTrue((skill / "scripts" / "ghc_family_go_skill.py").is_file())
            self.assertTrue((skill / "scripts" / "ghc_family_go_sgf_core.py").is_file())

    def test_family_current_runners_exist(self):
        names = ["ghc_family_go_board_topology.py", "ghc_family_go_capture_rules.py", "ghc_family_sgf_tree_records.py", "ghc_family_go_evidence_access.py", "ghc_family_go_contract_suite.py"]
        self.assertTrue(all((ROOT / "scripts" / name).is_file() for name in names))

    def test_method_flow_and_non_erasure(self):
        flow = load(X2 / "method-flow" / "ledger.json")
        self.assertEqual(flow["counts"]["methods"], 58)
        self.assertEqual(flow["counts"]["witness_results"], {"fail": 497, "pass": 497})
        self.assertEqual(len(flow["methods"]), 58)
        self.assertEqual(len(flow["witnesses"]), 994)
        self.assertTrue(all(row["retained_negative_ids"] for row in flow["methods"]))
        self.assertFalse(flow["repository_scan"])
        self.assertFalse(flow["cross_lane_scan"])
        self.assertFalse(flow["unchanged_history_scan"])
        self.assertFalse(flow["sibling_lane_mutation"])

    def test_phase_truth_and_effective_counts(self):
        truth = load(X2 / "phase-truth.json")
        self.assertEqual(truth["source"], SOURCE)
        self.assertEqual(truth["x1"], X1_COMMIT)
        self.assertEqual(truth["outcomes"], {"completed": 165, "represented": 26, "open_gap": 3, "exact_gate": 6})
        self.assertEqual(truth["effective_counts"], {"proposals": 16430, "negatives": 84351, "methods": 94003, "failed_witnesses": 55199, "passing_witnesses": 86052, "open_gaps": 758, "exact_gates": 765})
        self.assertEqual(truth["real_people_or_records"], 0)
        self.assertEqual(truth["canonical_invocations"], 0)
        self.assertEqual(truth["successor_contacts"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_open_and_exact_gates(self):
        gaps = load(X2 / "open-gap-register.json")
        gates = load(X2 / "exact-gate-register.json")
        self.assertEqual(gaps["effective_count"], 758)
        self.assertEqual(gates["effective_count"], 765)
        self.assertEqual(len(gaps["phase_new"]), 3)
        self.assertEqual(len(gates["phase_new"]), 6)
        self.assertEqual(gaps["silently_closed"], 0)
        self.assertEqual(gates["silently_closed"], 0)

    def test_deck_graph_and_manifest(self):
        index = load(X2 / "deck" / "deck-index.json")
        manifest = load(X2 / "deck" / "card-manifest.json")
        self.assertEqual(index["card_count"], 266)
        self.assertEqual(manifest["entry_count"], 266)
        cards = {}
        for row in manifest["entries"]:
            path = ROOT / row["path"]
            data = path.read_bytes()
            self.assertEqual(len(data), row["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])
            card = json.loads(data)
            cards[card["card_id"]] = card
        for card in cards.values():
            self.assertEqual(len(card["parent_ids"]), 0 if card["tier"] == 1 else 1)
            for parent in card["parent_ids"]:
                self.assertIn(parent, cards)
                self.assertEqual(cards[parent]["tier"], card["tier"] - 1)

    def test_accessible_report_structure(self):
        text = (X2 / "integrated-overview.html").read_text(encoding="utf-8")
        for token in ('lang="en"', "<title>", "<main>", "<caption>", 'scope="col"'):
            self.assertIn(token, text)
        self.assertIn("Manual browser", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_evidence_manifest_and_staged_review(self):
        manifest = load(VALIDATION / "evidence-manifest.json")
        review = load(VALIDATION / "evidence-staged-review.json")
        privacy = load(VALIDATION / "evidence-privacy.json")
        for row in manifest["entries"]:
            data = git("show", f":{row['path']}").replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(len(data), row["bytes_normalized_lf"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256_normalized_lf"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["deletions"], [])
        self.assertEqual(review["outside_owner_paths"], [])
        self.assertEqual(review["x1_mutations"], [])
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)

    def test_owner_file_and_document_caps(self):
        owner_files = [path for path in BASE.rglob("*") if path.is_file()]
        self.assertLess(len(owner_files), 2000)
        for path in owner_files:
            if path.suffix.lower() in {".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000)


if __name__ == "__main__":
    unittest.main()
