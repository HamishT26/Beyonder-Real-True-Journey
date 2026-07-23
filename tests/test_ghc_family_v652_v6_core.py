"""Bounded x2 tests for Tavian Sol v652-v6."""
import json
import unittest
from collections import Counter
from pathlib import Path

from scripts import ghc_family_v652_v6_core as core
from scripts import ghc_family_v652_v6_phase_data as d

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tavian-sol/v652-v6"


class TestTavianV652V6Core(unittest.TestCase):
    def receipts(self):
        return [json.loads((ROOT / "surfaces" / p["slug"] / "bounded-receipt.json").read_text(encoding="utf-8")) for p in d.PROPOSALS]

    def test_all_baselines_accept(self):
        self.assertTrue(all(core.execute_proposal(p)["bounded_receipt"]["baseline_accepted"] for p in d.PROPOSALS))

    def test_all_mutations_reject_or_quarantine(self):
        rows = [m for p in d.PROPOSALS for m in core.execute_proposal(p)["mutation_results"]["rows"]]
        self.assertEqual(len(rows), 150)
        self.assertTrue(all(row["passed"] for row in rows))
        self.assertTrue(all(row["decision"] in {"reject", "quarantine"} for row in rows))

    def test_outcome_vocabulary_and_counts(self):
        counts = Counter(row["observed_outcome"] for row in self.receipts())
        self.assertEqual(dict(counts), {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})

    def test_real_world_counters_zero(self):
        for row in self.receipts():
            self.assertTrue(all(value == 0 for value in row["real_world_counters"].values()))

    def test_every_surface_has_three_artifacts(self):
        for proposal in d.PROPOSALS:
            target = ROOT / "surfaces" / proposal["slug"]
            self.assertEqual({p.name for p in target.iterdir()}, {"contract.json", "mutation-results.json", "bounded-receipt.json"})

    def test_gmut_boundaries(self):
        for proposal in d.PROPOSALS[12:17]:
            contract = json.loads((ROOT / "surfaces" / proposal["slug"] / "contract.json").read_text(encoding="utf-8"))
            self.assertIn("theory_of_everything", contract["protected_gates"])
            self.assertIn("observation", contract["title"].casefold())

    def test_environmental_monitoring_proxies_represented(self):
        for proposal in d.PROPOSALS[23:25]:
            receipt = json.loads((ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["observed_outcome"], "represented")
            self.assertEqual(receipt["real_world_counters"]["real_buoys"], 0)
            self.assertEqual(receipt["real_world_counters"]["real_monitors"], 0)
            self.assertEqual(receipt["real_world_counters"]["real_observations"], 0)

    def test_identity_profiles_represented(self):
        for proposal in d.PROPOSALS[25:28]:
            receipt = json.loads((ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["observed_outcome"], "represented")
            self.assertEqual(receipt["real_world_counters"]["real_keys"], 0)
            self.assertEqual(receipt["real_world_counters"]["real_services"], 0)
            self.assertEqual(receipt["real_world_counters"]["real_network_exchanges"], 0)

    def test_suzaku_open_gap(self):
        receipt = json.loads((ROOT / "surfaces" / "suzaku-zero-row" / "bounded-receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["observed_outcome"], "open_gap")
        self.assertEqual(receipt["real_world_counters"]["downloads"], 0)
        self.assertEqual(receipt["real_world_counters"]["likelihoods"], 0)

    def test_community_marine_authority_exact_gate(self):
        receipt = json.loads((ROOT / "surfaces" / "community-marine-observation-authority" / "bounded-receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["observed_outcome"], "exact_gate")
        self.assertEqual(receipt["real_world_counters"]["real_decisions"], 0)

    def test_portfolio_resolution(self):
        payload = json.loads((ROOT / "portfolios" / "expanded-portfolio-evidence.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["resolved_counts"], {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30})
        self.assertFalse(payload["inherited_completion_credit"])

    def test_skills_local_and_validated(self):
        payload = json.loads((ROOT / "skills" / "skill-build-receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["skill_count"], 10)
        self.assertEqual(payload["validated_count"], 10)
        self.assertEqual(payload["smoke_used_count"], 10)
        self.assertFalse(payload["globally_installed"])
        self.assertFalse(payload["subagent_forward_test"])
        portfolio = json.loads((ROOT / "portfolios" / "expanded-portfolio-evidence.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(row["name_normalized_for_skill_creator"] for row in portfolio["skills"]), 1)


if __name__ == "__main__":
    unittest.main()
