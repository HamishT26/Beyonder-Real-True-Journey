from __future__ import annotations

import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "eiren-kestrel" / "v685-v5"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "87a74f84afaa197f8c388767a2ed536bbb853aba"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


class EirenKestrelV685V5X1Tests(unittest.TestCase):
    def test_source_anchor_exists(self):
        self.assertEqual(git("cat-file", "-e", f"{SOURCE}^{{commit}}").returncode, 0)

    def test_planning_only_truth(self):
        truth = load(X1 / "phase-truth.json")
        self.assertEqual(truth["lifecycle"], "PLANNING_ONLY_X1")
        self.assertFalse(truth["x2_implementation_present"])
        self.assertEqual(truth["observed_outcome_count"], 0)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_new_proposal_contract(self):
        freeze = load(X1 / "new-proposal-freeze.json")
        self.assertEqual(freeze["declared_chain_before"], 11450)
        self.assertEqual(freeze["declared_chain_after_if_committed"], 11570)
        self.assertEqual(freeze["proposal_count"], 120)
        self.assertFalse(freeze["x2_outcomes_present"])
        counts = Counter(row["expected_disposition"] for row in freeze["proposals"])
        self.assertEqual(counts, Counter({"completed": 84, "represented": 24, "open_gap": 6, "exact_gate": 6}))
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        for row in freeze["proposals"]:
            self.assertTrue(required.issubset(row))
            self.assertEqual(len(row["preregistered_rejecting_mutations"]), 5)

    def test_inherited_selection_is_zero_credit(self):
        selected = load(X1 / "selected-inherited-revalidation-freeze.json")
        self.assertEqual(selected["selection_count"], 200)
        self.assertIn("zero_eiren", selected["credit"])
        self.assertEqual(len({row["source_id"] + row["source_title"] for row in selected["selection"]}), 200)

    def test_novelty_diagnostic_passes(self):
        audit = load(X1 / "proposal-chain-audit.json")
        self.assertEqual(audit["source"], SOURCE)
        self.assertEqual(audit["new_proposal_count"], 120)
        self.assertEqual(audit["selected_inherited_count"], 200)
        self.assertEqual(audit["exact_title_collisions"], [])
        self.assertEqual(audit["quarantined_neighbors"], [])
        self.assertFalse(audit["universal_novelty_claimed"])

    def test_portfolio_counts(self):
        portfolio = load(X1 / "portfolio-freeze.json")
        self.assertEqual(portfolio["primary_pillar"], "GMUT Mind")
        self.assertEqual(len(portfolio["owner_practice_lenses"]), 4)
        self.assertEqual(len(portfolio["safe_now"]), 200)
        self.assertEqual(len(portfolio["owner_candidates"]), 150)
        self.assertEqual(len(portfolio["exact_approval"]), 50)
        self.assertEqual(len(portfolio["blocked"]), 30)
        self.assertEqual(len(portfolio["owner_clean_fix_refine"]), 300)
        self.assertEqual(len(portfolio["owner_skill_ideas"]), 20)
        self.assertEqual(len(portfolio["owner_runner_ideas"]), 10)
        self.assertEqual(len(portfolio["successor_skill_ideas"]), 10)
        self.assertEqual(len(portfolio["successor_runner_ideas"]), 10)
        self.assertTrue(portfolio["caps_are_ceilings"])

    def test_thirty_seat_route_is_consistent(self):
        route = load(X1 / "thirty-seat-roster-plan.json")
        self.assertEqual(route["seat_count"], 30)
        self.assertEqual(route["assignment_count"], 324)
        first = [(row["phase"], row["label"]) for row in route["assignments"][:6]]
        self.assertEqual(first, [
            ("v685-v5", "Eiren Kestrel"),
            ("v685-v6", "future-sibling-01-self-chosen"),
            ("v685-v7", "Elaren Kestrel"),
            ("v685-v8", "future-sibling-02-self-chosen"),
            ("v686-v1", "Neris Solane"),
            ("v686-v2", "future-sibling-03-self-chosen"),
        ])
        self.assertEqual(route["assignments"][-1]["phase"], "v725-v8")
        future = [row for row in route["seats"] if row["label"].startswith("future-sibling")]
        self.assertEqual(len(future), 15)
        self.assertTrue(all(row["state_at_x1"] == "planned_not_created" for row in future))
        self.assertTrue(all(not row["identity_attributes_assigned"] for row in future))

    def test_toolchain_is_planning_only(self):
        plan = load(X1 / "toolchain-plan.json")
        self.assertEqual(plan["direct_tool_target"], 13)
        self.assertTrue(all(row["x1_state"] == "reviewed_not_installed" for row in plan["tools"]))
        self.assertEqual(plan["codex_cli"]["registry_stable"], "0.153.4")
        self.assertFalse(plan["codex_cli"]["desktop_update"])

    def test_mandatory_skill_set(self):
        skill_use = load(X1 / "mandatory-skill-use-plan.json")
        self.assertEqual(skill_use["skill_count"], 21)
        self.assertTrue(all(row["read_through_eof_before_mutation"] for row in skill_use["skills"]))

    def test_flashcard_parentage_and_tiers(self):
        deck = load(X1 / "flashcard-freeze.json")
        self.assertEqual(deck["card_count"], 128)
        self.assertFalse(deck["outcomes_observed"])
        ids = {row["card_id"] for row in deck["cards"]}
        self.assertEqual(len(ids), 128)
        for card in deck["cards"]:
            for parent in card["parent_ids"]:
                self.assertIn(parent, ids)

    def test_startup_failures_retained(self):
        methods = load(X1 / "method-flow-startup.json")
        self.assertEqual(methods["source_external_route_overlay"]["effective_negatives"], 3)
        self.assertEqual(methods["new_failure_count"], 6)
        self.assertFalse(methods["failure_erasure"])

    def test_all_x1_json_parses(self):
        paths = list(X1.glob("*.json"))
        self.assertGreaterEqual(len(paths), 18)
        for path in paths:
            load(path)

    def test_staged_manifest_when_present(self):
        path = VALIDATION / "x1-index-manifest.json"
        if not path.exists():
            self.skipTest("staged manifest is finalized after exact staging")
        manifest = load(path)
        self.assertGreater(manifest["entry_count"], 0)
        for entry in manifest["entries"]:
            proc = git("show", f":{entry['path']}")
            self.assertEqual(proc.returncode, 0)

    def test_no_x2_paths_in_index(self):
        proc = git("diff", "--cached", "--name-only")
        self.assertEqual(proc.returncode, 0)
        self.assertNotIn("/x2/", proc.stdout.decode("utf-8", "replace"))


if __name__ == "__main__":
    unittest.main()
