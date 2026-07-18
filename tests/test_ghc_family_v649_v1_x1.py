from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "eiren-kestrel" / "v649-v1"


class EirenV649V1X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.proposals = json.loads((PHASE / "x1-proposals.json").read_text(encoding="utf-8"))

    def test_exactly_ten_complete_proposals(self) -> None:
        rows = self.proposals["proposals"]
        self.assertEqual(len(rows), 10)
        required = {
            "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class",
            "execution_lane", "official_or_primary_source_needs", "concrete_artifacts",
            "test_falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
            "expected_disposition", "novelty_against_prior_frozen_proposals",
        }
        for row in rows:
            self.assertTrue(required.issubset(row))
            self.assertTrue(row["official_or_primary_source_needs"])
            self.assertTrue(row["concrete_artifacts"])
            self.assertTrue(row["protected_gates"])

    def test_expected_disposition_vocabulary_and_distribution(self) -> None:
        values = [row["expected_disposition"] for row in self.proposals["proposals"]]
        self.assertEqual(set(values), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertEqual({v: values.count(v) for v in set(values)}, {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})

    def test_frozen_chain_and_collision_audit(self) -> None:
        index = json.loads((PHASE / "provenance" / "frozen-chain-proposal-index.json").read_text(encoding="utf-8"))
        audit = json.loads((PHASE / "provenance" / "proposal-collision-audit.json").read_text(encoding="utf-8"))
        self.assertEqual((index["prior_count"], index["new_count"], index["count"]), (640, 10, 650))
        self.assertEqual(audit["exact_collision_count"], 0)
        self.assertTrue(all(row["decision"] == "distinct" for row in audit["audits"]))

    def test_portfolio_floors_are_new_and_frozen(self) -> None:
        specs = [("safe-now-plan.json", "tasks", 30), ("candidate-plan.json", "candidates", 20), ("skill-plan.json", "skills", 20), ("runner-plan.json", "runners", 10), ("clean-fix-refine-plan.json", "tasks", 30)]
        for name, key, expected in specs:
            payload = json.loads((PHASE / "portfolios" / name).read_text(encoding="utf-8"))
            self.assertGreaterEqual(payload["count"], expected)
            self.assertEqual(payload["count"], len(payload[key]))
        skills = json.loads((PHASE / "portfolios" / "skill-plan.json").read_text(encoding="utf-8"))["skills"]
        self.assertTrue(all(re.fullmatch(r"[a-z0-9-]{1,63}", row["name"]) for row in skills))
        runners = json.loads((PHASE / "portfolios" / "runner-plan.json").read_text(encoding="utf-8"))["runners"]
        self.assertTrue(all(row["name"].startswith("ghc_family_v649_v1_") for row in runners))

    def test_x1_has_seventy_unexecuted_mutations(self) -> None:
        payload = json.loads((PHASE / "validation" / "x1-synthetic-mutation-plan.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["count"], 70)
        self.assertFalse(payload["executed"])
        self.assertTrue(all(row["status"] == "preregistered_not_executed" for row in payload["mutations"]))

    def test_strict_x1_before_x2(self) -> None:
        truth = json.loads((PHASE / "phase-truth.json").read_text(encoding="utf-8"))
        review = json.loads((PHASE / "validation" / "x1-staged-review.json").read_text(encoding="utf-8"))
        self.assertFalse(truth["x2_started"])
        self.assertFalse(truth["outcomes_executed"])
        self.assertTrue(review["x1_only_passed"])
        self.assertEqual(review["x2_implementation_or_outcome_paths"], [])

    def test_identity_and_authority_boundaries(self) -> None:
        text = (PHASE / "x1-preregistration.md").read_text(encoding="utf-8")
        for phrase in ["not evidence of consciousness", "Maori authority", "NOT_READY_FOR_STAGE_20", "zero rows", "synthetic learning and design lens only"]:
            self.assertIn(phrase, text)

    def test_sources_keep_status_distinctions(self) -> None:
        sources = json.loads((PHASE / "sources" / "source-ledger.json").read_text(encoding="utf-8"))["sources"]
        self.assertGreaterEqual(len(sources), 15)
        statuses = {row["status"] for row in sources}
        self.assertTrue({"current", "stable"}.issubset(statuses))
        self.assertTrue(statuses.issubset({"current", "stable", "draft", "watch", "stable_with_errata_watch"}))

    def test_inherited_truth_is_preserved(self) -> None:
        negatives = json.loads((PHASE / "retained-negative-register.json").read_text(encoding="utf-8"))
        gates = json.loads((PHASE / "exact-open-gate-register.json").read_text(encoding="utf-8"))
        self.assertEqual(negatives["inherited_effective"], 4665)
        self.assertEqual(negatives["current_effective"], 4667)
        self.assertEqual((gates["inherited_open_gaps"], gates["inherited_exact_gates"]), (34, 35))
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (35, 36))

    def test_documents_under_word_cap(self) -> None:
        for path in PHASE.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".html"}:
                words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8")))
                self.assertLessEqual(words, 6000, str(path.relative_to(ROOT)))


if __name__ == "__main__":
    unittest.main()
