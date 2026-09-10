from __future__ import annotations

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/lyren-moss/v690-v1/plan"


def load(name: str):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


class LyrenV690V1PlanTests(unittest.TestCase):
    def test_source_and_baton(self):
        source = load("source-provenance.json")
        self.assertEqual(source["source"], "fbd8eb790f2f8bc9c507db0420bdd66d1ec05e2e")
        self.assertEqual(source["baton_sha256"], "ebbe82bc74b8c4bc4e99c410bbca4fdba80ca1fe95a9f84b8e1c86156e9f6585")
        self.assertEqual(source["complete_read"]["lines"], 2693)
        self.assertEqual(source["complete_read"]["words"], 74427)
        self.assertEqual(source["complete_read"]["eof_marker"], "EOF ILYAN REED v689-v8 BATON.")

    def test_source_canonical_not_replayed(self):
        source = load("source-provenance.json")
        self.assertEqual(source["canonical_receipt"]["invocations"], 1)
        self.assertEqual(source["canonical_receipt"]["successes"], 1)
        self.assertEqual(source["canonical_receipt"]["replays"], 0)
        self.assertFalse(source["source_canonical_replayed"])

    def test_proposal_counts_and_ids(self):
        proposals = load("new-proposals.json")["proposals"]
        self.assertEqual(len(proposals), 200)
        self.assertEqual(len({row["proposal_id"] for row in proposals}), 200)
        self.assertEqual(proposals[0]["proposal_id"], "LM6901-001")
        self.assertEqual(proposals[-1]["proposal_id"], "LM6901-200")

    def test_exact_outcomes(self):
        proposals = load("new-proposals.json")["proposals"]
        self.assertEqual(
            Counter(row["expected_execution_disposition"] for row in proposals),
            Counter({"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5}),
        )
        self.assertEqual(
            set(row["expected_execution_disposition"] for row in proposals),
            {"completed", "represented", "open_gap", "exact_gate"},
        )

    def test_strict_x1_x2_partition(self):
        proposals = load("new-proposals.json")["proposals"]
        self.assertEqual([row["proposal_id"] for row in proposals if row["lane"] == "x1"], [f"LM6901-{i:03d}" for i in range(1, 101)])
        self.assertEqual([row["proposal_id"] for row in proposals if row["lane"] == "x2"], [f"LM6901-{i:03d}" for i in range(101, 201)])

    def test_inherited_zero_credit(self):
        rows = load("inherited-selections.json")["rows"]
        self.assertEqual(len(rows), 200)
        self.assertTrue(all(row["novelty_credit"] == 0 and row["execution_credit"] == 0 for row in rows))
        self.assertTrue(all(row["source"] == "fbd8eb790f2f8bc9c507db0420bdd66d1ec05e2e" for row in rows))

    def test_portfolio_floors(self):
        for lane in ["x1", "x2"]:
            portfolio = load(f"portfolio-{lane}.json")
            self.assertEqual(len(portfolio["safe"]), 100)
            self.assertEqual(len(portfolio["candidate"]), 100)
            self.assertEqual(len(portfolio["clean_fix_refine"]), 100)
            self.assertTrue(all(not row["host_cleanup"] for row in portfolio["clean_fix_refine"]))

    def test_packet_inventory(self):
        self.assertEqual(len(load("exact-packets.json")["packets"]), 50)
        self.assertEqual(len(load("blocked-packets.json")["packets"]), 30)
        self.assertTrue(all(not row["operation_executed"] for row in load("exact-packets.json")["packets"]))
        self.assertTrue(all(not row["operation_executed"] for row in load("blocked-packets.json")["packets"]))

    def test_skills_and_runners(self):
        plan = load("skills-runners.json")
        self.assertEqual(len(plan["skills"]), 20)
        self.assertEqual(len(plan["runners"]), 10)
        self.assertEqual(len(plan["global_groups"]), 5)
        self.assertGreaterEqual(len(plan["successor_skill_ideas"]), 5)
        self.assertGreaterEqual(len(plan["successor_runner_ideas"]), 5)

    def test_packages_are_hash_locked(self):
        package_plan = load("package-plan.json")
        direct = [row for row in package_plan["packages"] if row["category"] == "direct"]
        transitive = [row for row in package_plan["packages"] if row["category"] == "transitive"]
        self.assertEqual([row["name"] for row in direct], ["bitstring", "reedsolo", "crccheck"])
        self.assertEqual(len(transitive), 2)
        self.assertTrue(all(len(row["sha256"]) == 64 for row in package_plan["packages"]))
        self.assertTrue(package_plan["wheel_only"])
        self.assertTrue(package_plan["hash_required"])

    def test_novelty_review(self):
        novelty = load("novelty-review.json")
        self.assertEqual(len(novelty["rows"]), 200)
        self.assertEqual(novelty["comparisons"], 40000)
        self.assertEqual(novelty["quarantines"], 0)
        self.assertFalse(novelty["universal_novelty"])

    def test_route(self):
        route = load("route.json")
        self.assertEqual(route["owner"], "Lyren Moss")
        self.assertEqual(route["phase"], "v690-v1")
        self.assertEqual(route["next_owner"], "Ilyra Fen")
        self.assertEqual(route["next_phase"], "v690-v2")
        self.assertEqual(route["send_limit"], 1)
        self.assertFalse(route["task_creation"])
        self.assertFalse(route["subagents"])

    def test_identity_boundary(self):
        identity = load("identity-practices.json")
        self.assertEqual(identity["primary_pillar"], "THOS Body")
        self.assertEqual(len(identity["practices"]), 4)
        self.assertEqual(len(identity["next_practices"]), 2)
        for forbidden in ["establishes consciousness", "proves personhood", "Stage 20 ready"]:
            self.assertNotIn(forbidden, identity["boundary"])

    def test_startup_failures_retained(self):
        records = load("startup-failures.json")["records"]
        self.assertEqual(len(records), 5)
        self.assertTrue(all(row["original_success_credit"] == 0 for row in records))

    def test_raw_manifest(self):
        manifest = load("manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(manifest["self_excluded"], "manifest.json")
        for entry in manifest["entries"]:
            path = ROOT / entry["path"]
            self.assertTrue(path.is_file(), entry["path"])
            self.assertEqual(path.stat().st_size, entry["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), entry["sha256"])


if __name__ == "__main__":
    unittest.main()
