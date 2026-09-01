from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v681-v5"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "d2f8f60dfaa4c7bd825ae04d57ba0e76bbb7a151"
BRANCH = "codex/GHC-Family/auren-lark-v681-v5-full-tools"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


class AurenX1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        module_path = ROOT / "scripts" / "build_ghc_family_auren_lark_v681_v5_x1.py"
        spec = importlib.util.spec_from_file_location("auren_x1", module_path)
        assert spec and spec.loader
        cls.builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.builder)
        cls.proposals = load_json(X1 / "new-proposal-freeze.json")
        cls.portfolio = load_json(X1 / "portfolio-freeze.json")

    def test_exact_source_and_branch(self) -> None:
        head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
        branch = subprocess.run(["git", "-C", str(ROOT), "branch", "--show-current"], check=True, capture_output=True, text=True).stdout.strip()
        self.assertEqual(head, SOURCE)
        self.assertEqual(branch, BRANCH)

    def test_planning_only_has_no_x2(self) -> None:
        self.assertFalse((BASE / "x2").exists())
        truth = load_json(X1 / "phase-truth.json")
        self.assertFalse(truth["x2_started"])
        self.assertIsNone(truth["observed_outcomes"])

    def test_sixty_unique_proposals(self) -> None:
        rows = self.proposals["proposals"]
        self.assertEqual(len(rows), 60)
        self.assertEqual(len({row["proposal_id"] for row in rows}), 60)
        self.assertEqual(len({row["title"] for row in rows}), 60)

    def test_four_exact_outcome_labels(self) -> None:
        counts = Counter(row["expected_disposition"] for row in self.proposals["proposals"])
        self.assertEqual(counts, Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}))
        self.assertEqual(set(counts), {"completed", "represented", "open_gap", "exact_gate"})

    def test_five_preregistered_mutations_each(self) -> None:
        rows = self.proposals["proposals"]
        self.assertTrue(all(len(row["preregistered_rejecting_mutations"]) == 5 for row in rows))
        self.assertEqual(sum(len(row["preregistered_rejecting_mutations"]) for row in rows), 300)

    def test_bounded_proposal_audit(self) -> None:
        audit = load_json(X1 / "proposal-chain-audit.json")
        self.assertEqual(audit["source"], SOURCE)
        self.assertEqual(audit["exact_title_collisions"], [])
        self.assertEqual(audit["quarantined_neighbors"], [])
        self.assertGreater(audit["audit_scope"]["reachable_id_title_records"], 0)
        self.assertFalse(audit["audit_scope"]["universal_declared_chain_materialization_claimed"])

    def test_inherited_reviews_are_zero_credit(self) -> None:
        inherited = load_json(X1 / "inherited-revalidation-freeze.json")
        self.assertEqual(inherited["count"], 20)
        self.assertTrue(all(row["completion_credit"] == 0 for row in inherited["reviews"]))

    def test_portfolio_floors_and_ceilings(self) -> None:
        self.assertEqual(len(self.portfolio["safe_now"]), 120)
        self.assertEqual(len(self.portfolio["owner_candidates"]), 80)
        self.assertEqual(len(self.portfolio["exact_approval"]), 20)
        self.assertEqual(len(self.portfolio["blocked"]), 10)
        self.assertEqual(len(self.portfolio["owner_clean_fix_refine"]), 100)
        self.assertEqual(len(self.portfolio["successor_candidates"]), 20)
        self.assertEqual(len(self.portfolio["successor_clean_fix_refine"]), 30)
        self.assertEqual(self.portfolio["materialized_file_stop"], 2000)
        self.assertTrue(self.portfolio["caps_are_ceilings"])

    def test_holds_are_unexecuted(self) -> None:
        holds = load_json(X1 / "approval-hold-register.json")
        self.assertEqual(holds["exact_approval_count"], 20)
        self.assertEqual(holds["blocked_count"], 10)
        self.assertEqual(holds["executed"], 0)
        self.assertTrue(all(row["state"] == "preregistered_not_executed" for row in self.portfolio["exact_approval"] + self.portfolio["blocked"]))

    def test_skills_and_runners_are_planning_only(self) -> None:
        plan = load_json(X1 / "skill-runner-plan.json")
        self.assertEqual(len(plan["skills"]), 20)
        self.assertEqual(len(plan["runners"]), 10)
        self.assertFalse(plan["global_install"])
        self.assertFalse(plan["x2_implementation_present"])

    def test_primary_sources_confer_no_authority(self) -> None:
        sources = load_json(X1 / "official-primary-source-ledger.json")
        self.assertEqual(sources["external_source_entries"], 11)
        self.assertEqual(sources["real_data_rows"], 0)
        self.assertEqual(sources["network_data_queries"], 0)
        self.assertFalse(sources["authority_conferred"])

    def test_identity_is_relational_only(self) -> None:
        identity = load_json(X1 / "identity-and-boundary.json")
        self.assertEqual(identity["name"], "Auren Lark")
        self.assertEqual(identity["role"], "Stewardship State Cartographer")
        self.assertTrue(identity["relational_working_language_only"])
        self.assertIn("consciousness", identity["not_evidence_of"])

    def test_route_is_not_precontacted(self) -> None:
        route = load_json(X1 / "route-plan.json")
        self.assertEqual(route["prospective_successor_title"], "Sable Rook")
        self.assertEqual(route["next_expected_phase"], "v681-v6")
        self.assertFalse(route["recipient_contacted"])
        self.assertTrue(route["terminal_gate_required"])

    def test_startup_failures_are_retained(self) -> None:
        flow = load_json(X1 / "method-flow-startup.json")
        self.assertEqual(len(flow["startup_failures"]), 16)
        self.assertTrue(all(row["initial_credit"] == 0 for row in flow["startup_failures"]))
        self.assertFalse(flow["failure_erasure"])
        self.assertEqual(flow["current_after_startup"]["effective_negatives"], 53912)
        self.assertEqual(flow["current_after_startup"]["effective_methods"], 61519)

    def test_manifest_replays_normalized_lf(self) -> None:
        manifest = load_json(VALIDATION / "x1-index-manifest.json")
        self.assertEqual(manifest["entry_count"], 20)
        self.assertEqual(len(manifest["declared_self_exclusions"]), 3)
        for row in manifest["entries"]:
            data = normalized(ROOT / row["path"])
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])

    def test_privacy_and_staged_review(self) -> None:
        privacy = load_json(VALIDATION / "x1-privacy-scan.json")
        staged = load_json(VALIDATION / "x1-staged-review.json")
        self.assertEqual(privacy["confirmed_hits"], [])
        self.assertEqual(privacy["scanned_files"], 20)
        self.assertEqual(staged["lifecycle"], "planning_only_x1")
        self.assertEqual(staged["x2_paths"], [])
        self.assertEqual(staged["path_count"], 23)

    def test_terminal_verdict_remains_closed(self) -> None:
        truth = load_json(X1 / "phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["declared_chain_after_if_committed"], 10010)


if __name__ == "__main__":
    unittest.main()
