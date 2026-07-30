#!/usr/bin/env python3
"""Tests for Eiren Kestrel's dedicated v656-v5 x1 freeze."""

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
from ghc_family_v656_v5_phase_catalogue import X1_OPERATIONAL_NEGATIVES


ROOT = REPO / d.PHASE_ROOT


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


def git_clean_blob(path: Path) -> bytes:
    relative = path.relative_to(REPO).as_posix()
    object_id = git("hash-object", "-w", f"--path={relative}", str(path))
    return subprocess.run(
        ["git", "cat-file", "blob", object_id],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


class EirenKestrelV656V5X1Tests(unittest.TestCase):
    def test_exact_source_or_x1_descendant(self) -> None:
        head = git("rev-parse", "HEAD")
        self.assertEqual(git("merge-base", d.SOURCE_FINAL, head), d.SOURCE_FINAL)

    def test_thirty_complete_preregistrations(self) -> None:
        packet = read_json("preregistration/proposals.json")
        self.assertEqual(packet["proposal_count"], 30)
        self.assertEqual(
            Counter(item["expected_disposition"] for item in packet["proposals"]),
            Counter({"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}),
        )
        required = {
            "proposal_id",
            "title",
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
        for proposal in packet["proposals"]:
            self.assertTrue(required <= proposal.keys())
            self.assertTrue(proposal["official_or_primary_source_needs"])
            self.assertTrue(proposal["protected_gates"])
            self.assertNotIn("observed_outcome", proposal)

    def test_identifiers_titles_and_slugs_are_unique(self) -> None:
        self.assertEqual(len({p["proposal_id"] for p in d.PROPOSALS}), 30)
        self.assertEqual(len({p["title"] for p in d.PROPOSALS}), 30)
        self.assertEqual(len({p["slug"] for p in d.PROPOSALS}), 30)

    def test_semantic_novelty_all_passes(self) -> None:
        audit = read_json("provenance/semantic-novelty-audit.json")
        self.assertEqual(audit["prior_count"], 2290)
        self.assertEqual(audit["new_count"], 30)
        self.assertEqual(audit["comparison_count"], 68700)
        self.assertTrue(audit["all_pass"])
        self.assertTrue(all(row["passes"] for row in audit["rows"]))

    def test_frozen_index_is_exactly_2320(self) -> None:
        index = read_json("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(index["prior_count"], 2290)
        self.assertEqual(index["new_count"], 30)
        self.assertEqual(index["count"], 2320)
        self.assertEqual(len(index["prior_proposals"]), 2290)
        self.assertEqual(len(index["new_proposals"]), 30)

    def test_x1_contains_no_x2_surface_or_observed_outcome(self) -> None:
        self.assertFalse((ROOT / "surfaces").exists())
        self.assertFalse((ROOT / "runners").exists())
        self.assertFalse((ROOT / "seal").exists())
        for path in ROOT.rglob("*.json"):
            if path.name == "x1-file-manifest.json":
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotIn('"observed_outcome"', text)

    def test_negatives_gaps_and_gates_are_additive(self) -> None:
        negatives = read_json("truth/retained-negative-register.json")
        self.assertEqual(negatives["source_effective_count"], 14358)
        self.assertEqual(negatives["x1_operational_count"], len(X1_OPERATIONAL_NEGATIVES))
        self.assertEqual(
            negatives["effective_count"], 14358 + len(X1_OPERATIONAL_NEGATIVES)
        )
        self.assertTrue(negatives["all_retained"])
        self.assertEqual(read_json("truth/open-gap-register.json")["effective_count"], 101)
        self.assertEqual(read_json("truth/exact-gate-register.json")["effective_count"], 100)

    def test_method_flow_retains_failed_and_passing_pairs(self) -> None:
        flow = read_json("method-flow/method-flow-ledger.json")
        self.assertEqual(len(flow["methods"]), 644 + len(X1_OPERATIONAL_NEGATIVES))
        counts = Counter(item["result"] for item in flow["witnesses"])
        self.assertEqual(counts["fail"], 644 + len(X1_OPERATIONAL_NEGATIVES))
        self.assertEqual(counts["pass"], 644 + len(X1_OPERATIONAL_NEGATIVES))
        self.assertEqual(len(flow["current_phase_method_ids"]), len(X1_OPERATIONAL_NEGATIVES))

    def test_route_is_blocked_and_tavian_is_standby(self) -> None:
        roster = read_json("route/fifteen-seat-roster-x1.json")
        self.assertEqual(roster["active_main_task_count"], 15)
        self.assertEqual(roster["current"], {"owner": d.OWNER, "phase": d.PHASE})
        self.assertEqual(roster["next_exact_edge"]["owner"], "Elaren Kestrel")
        self.assertEqual(roster["next_after_successor"]["owner"], "Neris Solane")
        self.assertEqual(roster["standby"][0]["name"], "Tavian Sol")
        self.assertFalse(roster["standby"][0]["eligible_for_main_task_route"])
        self.assertEqual(roster["route_state"], "preregistered_terminal_only_not_contacted")

    def test_privacy_scan_is_clean(self) -> None:
        scan = read_json("validation/x1-privacy-scan.json")
        self.assertEqual(len(scan["classes"]), 5)
        self.assertEqual(scan["confirmed_hit_count"], 0)
        self.assertTrue(scan["valid"])

    def test_manifest_bytes_hashes_and_exact_path_set(self) -> None:
        manifest = read_json("validation/x1-file-manifest.json")
        entries = manifest["entries"]
        self.assertEqual(len(entries), manifest["entry_count"])
        exclusions = {item["path"] for item in manifest["declared_exclusions"]}
        for entry in entries:
            path = REPO / entry["path"]
            self.assertTrue(path.is_file(), entry["path"])
            data = git_clean_blob(path)
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])
        actual = set(
            filter(
                None,
                git("diff", "--name-only", d.SOURCE_FINAL, "HEAD").splitlines(),
            )
        )
        if not actual:
            actual = set(
                filter(None, git("diff", "--name-only").splitlines())
            ) | set(
                filter(
                    None,
                    git("ls-files", "--others", "--exclude-standard").splitlines(),
                )
            )
        self.assertEqual({item["path"] for item in entries} | exclusions, actual)

    def test_identity_and_stage20_boundaries(self) -> None:
        identity = read_json("identity/relational-identity.json")
        self.assertIn("Relational working language only", identity["boundary"])
        truth = read_json("truth/x1-phase-truth.json")
        self.assertFalse(truth["x2_execution_started"])
        self.assertFalse(truth["terminal_route_contacted"])
        self.assertEqual(truth["verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
