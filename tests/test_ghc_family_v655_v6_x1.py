from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/caelen-ash/v655-v6"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def prospective_blob(path: Path) -> bytes:
    repository_relative = path.relative_to(ROOT).as_posix()
    oid = subprocess.run(
        [
            "git",
            "hash-object",
            "-w",
            f"--path={repository_relative}",
            repository_relative,
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()
    return subprocess.run(
        ["git", "cat-file", "blob", oid],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


class CaelenAshV655V6X1Tests(unittest.TestCase):
    def test_exact_source_anchor(self) -> None:
        anchor = load("provenance/source-anchor.json")
        self.assertEqual(
            anchor["source_final"],
            "c641ac3c4d0f0b38cb897db931d689de6ea5aa0c",
        )
        self.assertEqual(
            anchor["source_x1_freeze"],
            "a92d0a6c8a5d2620074c1bc505fa8345c8f90373",
        )
        self.assertEqual(
            anchor["source_x1_final"],
            "a92d0a6c8a5d2620074c1bc505fa8345c8f90373",
        )
        self.assertEqual(
            anchor["source_evidence"],
            "ee10e567ce363e5a8bf710532c5a53d0a411defa",
        )
        self.assertEqual(
            anchor["source_evidence_correction"],
            None,
        )
        self.assertEqual(anchor["source_phase_commits"], 3)
        self.assertEqual(anchor["source_merge_count"], 0)
        self.assertTrue(anchor["source_clean_and_four_way_equal"])
        self.assertFalse(anchor["source_full_repository_suite_run"])

    def test_thirty_complete_preregistrations(self) -> None:
        ledger = load("preregistration/proposals.json")
        self.assertEqual(ledger["proposal_count"], 30)
        self.assertEqual(len(ledger["proposals"]), 30)
        self.assertEqual(
            ledger["expected_disposition_counts"],
            {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
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
        for proposal in ledger["proposals"]:
            self.assertTrue(required <= set(proposal))
            self.assertTrue(proposal["official_or_primary_source_needs"])
            self.assertEqual(len(proposal["concrete_artifacts"]), 3)

    def test_semantic_novelty_and_frozen_chain(self) -> None:
        novelty = load("provenance/semantic-novelty-audit.json")
        frozen = load("provenance/frozen-chain-proposal-index.json")
        self.assertTrue(novelty["valid"])
        self.assertEqual(len(novelty["rows"]), 30)
        self.assertTrue(all(row["token_jaccard"] < 0.60 for row in novelty["rows"]))
        self.assertEqual((frozen["prior_count"], frozen["new_count"]), (2080, 30))
        self.assertEqual(frozen["count"], 2110)
        prior_ids = {row["proposal_id"] for row in frozen["prior_proposals"]}
        new_ids = [row["proposal_id"] for row in frozen["new_proposals"]]
        self.assertEqual(len(new_ids), len(set(new_ids)))
        self.assertFalse(prior_ids & set(new_ids))

    def test_source_status_classes_and_references(self) -> None:
        sources = load("sources/official-source-ledger.json")
        proposals = load("preregistration/proposals.json")
        self.assertEqual(set(sources["statuses"]), {"current", "stable", "watch"})
        self.assertTrue(set(sources["statuses"]) <= set(sources["counts"]))
        source_ids = {row["source_id"] for row in sources["sources"]}
        used = {
            source_id
            for proposal in proposals["proposals"]
            for source_id in proposal["official_or_primary_source_needs"]
        }
        self.assertTrue(used <= source_ids)

    def test_x1_has_no_execution_or_observed_outcomes(self) -> None:
        proposals = load("preregistration/proposals.json")
        truth = load("truth/x1-phase-truth.json")
        mutations = load("validation/preregistered-mutation-plan.json")
        self.assertTrue(proposals["x1_only"])
        self.assertFalse(proposals["observed_outcomes_present"])
        self.assertEqual(truth["lifecycle"], "x1_frozen_not_executed")
        self.assertEqual(truth["observed_outcome_count"], 0)
        self.assertEqual(mutations["count"], 150)
        self.assertEqual(mutations["x1_execution_count"], 0)
        self.assertTrue(
            all(row["execution_state"] == "frozen_unexecuted" for row in mutations["mutations"])
        )

    def test_portfolio_and_owner_caps(self) -> None:
        portfolio = load("portfolios/expanded-portfolio-plan.json")
        self.assertEqual(
            portfolio["counts"],
            {
                "safe_now": 30,
                "candidate": 30,
                "skills": 10,
                "runners": 10,
                "clean_fix_refine": 30,
            },
        )
        self.assertEqual(portfolio["safe_candidate_task_cap"], 1000)
        self.assertLess(
            sum(1 for path in PHASE.rglob("*") if path.is_file()),
            2000,
        )

    def test_negatives_gaps_and_gates_preserved(self) -> None:
        negatives = load("truth/retained-negative-register.json")
        gaps = load("truth/open-gap-register.json")
        gates = load("truth/exact-gate-register.json")
        self.assertEqual(negatives["source_effective"], 13077)
        self.assertEqual(negatives["source_sealed_repository_count"], 13075)
        self.assertEqual(negatives["source_live_overlay_count"], 2)
        self.assertEqual(len(negatives["source_live_overlay"]), 2)
        self.assertEqual(negatives["x1_operational_count"], 10)
        self.assertEqual(negatives["effective_after_x1"], 13087)
        self.assertTrue(negatives["no_failure_erased"])
        self.assertEqual(gaps["inherited_count"], 93)
        self.assertEqual(gates["inherited_count"], 92)
        self.assertEqual(gaps["closed_in_x1"], 0)
        self.assertEqual(gates["closed_in_x1"], 0)

    def test_method_flow_pair_parity(self) -> None:
        ledger = load("method-flow/method-flow-ledger.json")
        validation = load("method-flow/method-flow-validation.json")
        counts = ledger["counts"]
        self.assertEqual(counts["methods"], 289)
        self.assertEqual(counts["witness_results"], {"fail": 289, "pass": 289})
        self.assertEqual(len(ledger["current_phase_method_ids"]), 10)
        self.assertTrue(validation["valid"])

    def test_route_is_prepared_not_sent(self) -> None:
        roster = load("route/sixteen-seat-roster-x1.json")
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual(roster["current"]["owner"], "Caelen Ash")
        self.assertEqual(roster["next"]["owner"], "Orin Thale")
        self.assertEqual(roster["contact_count"], 0)
        self.assertEqual(
            truth["terminal_route"],
            "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
        )
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_manifest_and_privacy_receipts(self) -> None:
        manifest = load("validation/x1-file-manifest.json")
        privacy = load("validation/x1-privacy-scan.json")
        self.assertGreaterEqual(manifest["entry_count"], 20)
        self.assertEqual(
            manifest["content_basis"],
            "prospective_normalized_git_blob",
        )
        for row in manifest["entries"]:
            path = ROOT / row["path"]
            self.assertTrue(path.is_file())
            content = prospective_blob(path)
            self.assertEqual(len(content), row["bytes"])
            self.assertEqual(hashlib.sha256(content).hexdigest(), row["sha256"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertEqual(privacy["confirmed_hits"], [])

    def test_identity_and_authority_boundaries(self) -> None:
        identity = load("identity/relational-identity.json")
        truth = load("truth/x1-phase-truth.json")
        self.assertIn("Relational working language only", identity["boundary"])
        self.assertFalse(truth["independent_reproduction_claimed"])
        self.assertFalse(truth["theory_of_everything_claimed"])
        self.assertFalse(truth["agi_or_asi_claimed"])
        self.assertFalse(truth["consciousness_or_personhood_claimed"])


if __name__ == "__main__":
    unittest.main()
