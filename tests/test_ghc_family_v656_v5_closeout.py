#!/usr/bin/env python3
"""Closeout tests for Eiren Kestrel v656-v5."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v656_v5_phase_data as d


ROOT = REPO / d.PHASE_ROOT
SOURCE = d.SOURCE_FINAL
X1 = "e313d47c1bc6386d3dbdf1773d1d7cb4026bc7f9"
EVIDENCE = "f9662c901407a86cf271eef9b54467a782c99455"
CLOSEOUT = "3181608db19f39bb7b91be01fc62e64840a86c5e"


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


class EirenKestrelV656V5CloseoutTests(unittest.TestCase):
    def test_exact_four_commit_single_parent_history(self) -> None:
        head = git("rev-parse", "HEAD")
        self.assertEqual(git("rev-list", "--count", f"{SOURCE}..{head}"), "4")
        self.assertEqual(git("rev-list", "--count", "--merges", f"{SOURCE}..{head}"), "0")
        commits = git("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines()
        self.assertEqual(commits, [X1, EVIDENCE, CLOSEOUT, head])
        self.assertEqual(git("rev-parse", f"{head}^"), CLOSEOUT)
        for commit in commits:
            self.assertEqual(len(git("show", "-s", "--format=%P", commit).split()), 1)

    def test_outcomes_and_truth_are_exact(self) -> None:
        truth = read_json("truth/phase-truth-final.json")
        self.assertEqual(
            truth["outcomes"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        )
        self.assertEqual(truth["effective_negatives"], 14549)
        self.assertEqual(truth["effective_open_gaps"], 101)
        self.assertEqual(truth["effective_exact_gates"], 100)
        self.assertEqual(truth["verdict"], "NOT_READY_FOR_STAGE_20")

    def test_method_flow_is_835_pairs(self) -> None:
        flow = read_json("method-flow/method-flow-ledger-final.json")
        self.assertEqual(flow["counts"]["methods"], 835)
        self.assertEqual(flow["counts"]["witness_results"]["fail"], 835)
        self.assertEqual(flow["counts"]["witness_results"]["pass"], 835)
        self.assertTrue(read_json("method-flow/method-flow-summary-final.json")["no_failure_erased"])

    def test_final_gaps_and_gates_remain_open(self) -> None:
        self.assertEqual(read_json("truth/open-gap-register-final.json")["effective_count"], 101)
        self.assertEqual(read_json("truth/exact-gate-register-final.json")["effective_count"], 100)

    def test_baton_word_count_and_sanitization(self) -> None:
        baton = ROOT / "handoffs/elaren-kestrel-v656-v6-activation.md"
        text = baton.read_text(encoding="utf-8")
        words = text.split()
        self.assertGreaterEqual(len(words), 10000)
        self.assertLessEqual(len(words), 100000)
        self.assertNotIn("source_thread_id", text)
        self.assertNotIn("send_message_to_thread", text)
        self.assertNotIn("C:" + "\\Users\\", text)
        self.assertNotIn("D:" + "\\GHC" + "-Archives", text)

    def test_route_is_prepared_not_sent(self) -> None:
        route = read_json("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["successor_exact_title"], "Elaren Kestrel")
        self.assertEqual(route["successor_phase"], "v656-v6")
        self.assertEqual(route["successor_next_edge"], "Neris Solane v656-v7")
        self.assertEqual(route["contact_count"], 0)
        self.assertEqual(route["tavian_state"], "ON_STANDBY")

    def test_closeout_and_seal_are_bounded(self) -> None:
        closeout = read_json("closeout/closeout-receipt.json")
        seal = read_json("seal/seal-receipt.json")
        self.assertTrue(closeout["valid"])
        self.assertTrue(seal["valid"])
        self.assertFalse(closeout["full_repository_suite_run"])
        self.assertFalse(closeout["independent_reproduction"])
        self.assertFalse(seal["terminal_message_sent"])

    def test_all_owner_json_parses(self) -> None:
        for path in ROOT.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

    def test_final_delta_manifest_exact(self) -> None:
        manifest = read_json("validation/final-staged-manifest.json")
        entries = {item["path"]: item for item in manifest["entries"]}
        exclusions = {item["path"] for item in manifest["declared_exclusions"]}
        actual = set(
            filter(
                None,
                git("diff", "--name-only", EVIDENCE, CLOSEOUT).splitlines(),
            )
        )
        self.assertEqual(set(entries) | exclusions, actual)
        for path, entry in entries.items():
            data = subprocess.run(
                ["git", "show", f"{CLOSEOUT}:{path}"],
                cwd=REPO,
                check=True,
                capture_output=True,
            ).stdout
            self.assertEqual(len(data), entry["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])

    def test_owner_manifest_exact(self) -> None:
        manifest = read_json("validation/final-owner-manifest.json")
        entries = {item["path"]: item for item in manifest["entries"]}
        exclusions = {item["path"] for item in manifest["declared_exclusions"]}
        actual = set(
            filter(None, git("diff", "--name-only", SOURCE, "HEAD").splitlines())
        )
        self.assertEqual(set(entries) | exclusions, actual)
        self.assertLessEqual(len(actual), 2000)
        self.assertEqual(
            Counter(read_json("x2/proposal-ledger.json")["outcomes"]),
            Counter({"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}),
        )


if __name__ == "__main__":
    unittest.main()
