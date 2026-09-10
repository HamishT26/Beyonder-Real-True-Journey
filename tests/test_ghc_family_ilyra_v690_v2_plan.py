"""Planning-only tests for Ilyra Fen v690-v2."""

from __future__ import annotations

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "ilyra-fen" / "v690-v2" / "plan"


def load(name: str):
    return json.loads((PLAN / name).read_text(encoding="utf-8"))


class IlyraV690V2PlanTests(unittest.TestCase):
    def test_parentless_planning_profile(self):
        profile = load("profile.json")
        source = load("source-provenance.json")
        self.assertEqual(profile["owner"], "Ilyra Fen")
        self.assertEqual(profile["phase"], "v690-v2")
        self.assertEqual(profile["branch"], "codex/GHC-Family/ilyra-fen-main")
        self.assertFalse(source["source_is_ancestor"])
        self.assertEqual(source["final"], "9936e2855b72bddfecdea77abdd6f083f14a09f1")

    def test_two_hundred_inherited_zero_credit(self):
        rows = load("inherited-selections.json")["records"]
        self.assertEqual(len(rows), 200)
        self.assertEqual(len({row["selection_id"] for row in rows}), 200)
        self.assertTrue(all(row["novelty_credit"] == 0 for row in rows))
        self.assertTrue(all(row["execution_credit"] == 0 for row in rows))
        for row in rows:
            encoded = json.dumps(
                row["record"], ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
            ).encode("utf-8")
            self.assertEqual(hashlib.sha256(encoded).hexdigest(), row["source_record_sha256"])

    def test_two_hundred_new_and_exact_outcomes(self):
        rows = load("new-proposals.json")["proposals"]
        self.assertEqual(len(rows), 200)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 200)
        self.assertEqual(Counter(row["lane"] for row in rows), {"x1": 100, "x2": 100})
        self.assertEqual(
            Counter(row["expected_execution_disposition"] for row in rows),
            {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5},
        )
        self.assertEqual(len({json.dumps(row["request"], sort_keys=True) for row in rows}), 200)

    def test_planning_only_no_production_evaluator(self):
        self.assertFalse((ROOT / "scripts" / "ghc_family_obligation_graph_x1.py").exists())
        self.assertFalse((ROOT / "scripts" / "ghc_family_obligation_graph_x2.py").exists())
        payload = load("new-proposals.json")
        self.assertTrue(payload["planning_only"])
        self.assertFalse(payload["production_evaluator_executed"])

    def test_portfolios(self):
        for lane in ("x1", "x2"):
            payload = load(f"portfolio-{lane}.json")
            self.assertEqual(len(payload["safe_tasks"]), 100)
            self.assertEqual(len(payload["candidate_tasks"]), 100)
            self.assertEqual(len(payload["clean_fix_refine_tasks"]), 100)
            self.assertEqual(payload["execution_state"], "frozen_not_executed")

    def test_packages_are_downloaded_not_installed(self):
        payload = load("package-plan.json")
        self.assertEqual(payload["direct_count"], 3)
        self.assertEqual(payload["installation_state"], "downloaded_not_installed_at_planning")
        expected = {
            "54f33de9f4f911d7e84e4191749cac8cc5653f815b06738c54db9a15ab8b1e42",
            "d47fbf302e7d9cbbb9e2555a0d267983d2aa476bac30e90dfbe5669bd57f3762",
            "91feb30971df6ac53d51503970e4aac67e4d9bc7834535f2b7cd3674645003ac",
        }
        self.assertEqual({row["sha256"] for row in payload["packages"]}, expected)
        self.assertTrue(all(not row["unsafe_members"] for row in payload["packages"]))

    def test_workflow_counts_and_route(self):
        self.assertEqual(load("exact-packets.json")["count"], 50)
        self.assertEqual(load("blocked-packets.json")["count"], 30)
        self.assertEqual(load("recent-bundle-review.json")["count"], 10)
        identity = load("identity-practices.json")
        self.assertEqual(len(identity["owner_practices"]), 4)
        self.assertEqual(len(identity["successor_practices"]), 2)
        route = load("route.json")
        self.assertEqual(route["current"]["position"], 8)
        self.assertEqual(route["next"]["owner"], "Mira Fenwick")
        self.assertFalse(route["precontacted"])

    def test_manifest_raw_worktree_bytes(self):
        manifest = load("manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            data = (ROOT / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])


if __name__ == "__main__":
    unittest.main()
