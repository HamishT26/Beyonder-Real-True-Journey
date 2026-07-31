from __future__ import annotations

import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/neris-solane/v656-v7"
X1 = "f048a624daa5d6035cb01a485d74f43151cc4cd2"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


class V656V7Tests(unittest.TestCase):
    def test_x1_is_ancestor_and_frozen(self) -> None:
        subprocess.run(["git", "merge-base", "--is-ancestor", X1, "HEAD"], cwd=ROOT, check=True)
        frozen = git("diff-tree", "--no-commit-id", "--name-only", "-r", X1).splitlines()
        changed = subprocess.run(
            ["git", "diff", "--name-only", X1, "--", *frozen],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.splitlines()
        self.assertEqual(changed, [])

    def test_outcome_distribution(self) -> None:
        ledger = load("x2/proposal-ledger.json")
        self.assertEqual(ledger["proposal_count"], 30)
        self.assertEqual(ledger["outcome_counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertFalse(ledger["independent_reproduction"])

    def test_mutation_negative_total(self) -> None:
        negatives = load("truth/retained-negative-register-x2.json")
        self.assertEqual(negatives["mutation_count"], 150)
        self.assertEqual(len(negatives["mutation_negatives"]), 150)
        self.assertTrue(negatives["all_retained"])
        self.assertEqual(len({row["negative_id"] for row in negatives["mutation_negatives"]}), 150)

    def test_method_flow_parity(self) -> None:
        flow = load("method-flow/method-flow-state-x2.json")
        negatives = load("truth/retained-negative-register-x2.json")
        expected = 150 + negatives["x2_operational_count"]
        self.assertEqual(flow["counts"]["current_methods"], expected)
        self.assertEqual(flow["counts"]["current_witness_results"], {"fail": expected, "pass": expected})
        self.assertEqual(Counter(row["result"] for row in flow["current_witnesses"]), Counter({"fail": expected, "pass": expected}))

    def test_immutable_x1_tree_has_no_x2_artifacts(self) -> None:
        paths = git(
            "ls-tree",
            "-r",
            "--name-only",
            X1,
            "docs/neris-solane/v656-v7",
        ).splitlines()
        phase_paths = [
            path.removeprefix("docs/neris-solane/v656-v7/")
            for path in paths
        ]
        forbidden = [
            path
            for path in phase_paths
            if path.startswith("surfaces/")
            or path.startswith("runners/")
            or "/x2" in path.lower()
            or path.startswith("closeout")
            or path.startswith("seal")
            or path.startswith("final")
        ]
        self.assertEqual(forbidden, [])

    def test_skill_smoke_receipts(self) -> None:
        receipts = list((PHASE / "skills").glob("*/smoke-receipt.json"))
        self.assertEqual(len(receipts), 10)
        self.assertTrue(all(json.loads(path.read_text(encoding="utf-8"))["valid"] for path in receipts))

    def test_runner_receipts(self) -> None:
        receipts = list((PHASE / "runners").glob("*-receipt.json"))
        self.assertEqual(len(receipts), 10)
        payloads = [json.loads(path.read_text(encoding="utf-8")) for path in receipts]
        self.assertTrue(all(row["valid"] for row in payloads))
        self.assertEqual(sum(row["surface_count"] for row in payloads), 30)
        self.assertEqual(sum(row["rejected_mutation_count"] for row in payloads), 150)

    def test_route_remains_unsent(self) -> None:
        route = load("orchestration/route-state-x1.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["message_sent"])
        self.assertEqual(route["next_exact_title"], "Vesper Arlen")
        self.assertEqual(route["tavian_sol_state"], "ON_STANDBY")

    def test_external_boundaries(self) -> None:
        truth = load("truth/phase-truth-x2.json")
        self.assertFalse(truth["real_data_used"])
        self.assertFalse(truth["independent_reproduction"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(load("truth/open-gap-register-x2.json")["effective_count"], 103)
        self.assertEqual(load("truth/exact-gate-register-x2.json")["effective_count"], 102)

    def test_accessible_static_report_structure(self) -> None:
        text = (PHASE / "deliverables/v656-v7-volcanic-observatory-evidence-report.html").read_text(encoding="utf-8")
        self.assertIn('<html lang="en">', text)
        self.assertIn("<caption>", text)
        self.assertIn('scope="col"', text)
        self.assertNotIn("<script", text.lower())
        self.assertIn("affected-user", text)

    def test_all_json_parses(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 140)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))


def _surface_test(slug: str, proposal_id: str):
    def test(self: V656V7Tests) -> None:
        base = PHASE / "surfaces" / slug
        contract = json.loads((base / "contract.json").read_text(encoding="utf-8"))
        mutations = json.loads((base / "mutation-results.json").read_text(encoding="utf-8"))
        receipt = json.loads((base / "bounded-receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["proposal_id"], proposal_id)
        self.assertTrue(receipt["valid_fixture_passed"])
        self.assertEqual(mutations["mutation_count"], 5)
        self.assertEqual(mutations["rejected_count"], 5)
        self.assertTrue(mutations["all_rejected"])
        self.assertFalse(receipt["real_data_used"])
        self.assertFalse(receipt["authority_granted"])
    return test


_ledger_path = PHASE / "preregistration/proposal-ledger.json"
if _ledger_path.is_file():
    _proposals = json.loads(_ledger_path.read_text(encoding="utf-8"))["proposals"]
    for _proposal in _proposals:
        setattr(
            V656V7Tests,
            f"test_surface_{_proposal['proposal_id'].lower().replace('-', '_')}",
            _surface_test(_proposal["slug"], _proposal["proposal_id"]),
        )


if __name__ == "__main__":
    unittest.main()
