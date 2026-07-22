from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/vesper-arlen/v651-v7"
X1 = "d55689f393292cea76f8d568d69da27c8f7b3bd6"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def load_x1(relative: str) -> dict:
    text = subprocess.check_output(["git", "show", f"{X1}:docs/vesper-arlen/v651-v7/{relative}"], cwd=REPO, text=True, encoding="utf-8")
    return json.loads(text)


class VesperV651V7X1Tests(unittest.TestCase):
    def test_exact_source(self) -> None:
        source = load("source/source-truth.json")
        self.assertEqual(source["source_head"], "2500d063583194b30f01da429196522baaac7300")
        self.assertTrue(source["local_upstream_tracking_fresh_live_equal"])

    def test_identity_boundary(self) -> None:
        identity = load("identity/relational-identity.json")
        self.assertEqual((identity["owner"], identity["pronouns"]), ("Vesper Arlen", "they/them"))
        self.assertIn("Relational working language only", identity["identity_boundary"])

    def test_exactly_thirty_proposals(self) -> None:
        packet = load("preregistration/proposals.json")
        self.assertEqual(packet["new_proposal_count"], 30)
        self.assertEqual(len(packet["proposals"]), 30)
        self.assertTrue(packet["strict_x1_only"])

    def test_required_proposal_fields(self) -> None:
        required = {
            "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class",
            "execution_lane", "official_or_primary_source_needs", "concrete_artifacts",
            "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
            "expected_disposition", "novelty_basis",
        }
        for row in load("preregistration/proposals.json")["proposals"]:
            self.assertTrue(required <= set(row))
            self.assertTrue(row["official_or_primary_source_needs"])

    def test_expected_distribution_only(self) -> None:
        packet = load("preregistration/proposals.json")
        self.assertEqual(packet["expected_outcomes"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(set(packet["allowed_outcomes"]), {"completed", "represented", "open_gap", "exact_gate"})

    def test_frozen_chain_and_novelty(self) -> None:
        chain = load("provenance/frozen-chain-proposal-index.json")
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertEqual((chain["prior_count"], chain["new_count"], chain["count"]), (1060, 30, 1090))
        self.assertEqual(audit["exact_title_collisions"], [])
        self.assertEqual(audit["inherited_rows_compared"], 1060)
        self.assertTrue(audit["valid"])

    def test_x1_has_no_x2_result(self) -> None:
        truth = load_x1("truth/x1-phase-truth.json")
        self.assertEqual((truth["x2_implementations"], truth["observed_core_outcomes"]), (0, 0))
        paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", X1, "docs/vesper-arlen/v651-v7"], cwd=REPO, text=True, encoding="utf-8").splitlines()
        self.assertNotIn("docs/vesper-arlen/v651-v7/outcomes/core-outcomes.json", paths)
        self.assertNotIn("docs/vesper-arlen/v651-v7/proposals/lsm-tombstone-horizon.json", paths)

    def test_portfolio_floors_and_caps(self) -> None:
        plan = load("portfolios/x1-portfolio-plan.json")
        self.assertTrue(plan["caps_are_ceilings_not_quotas"])
        self.assertGreaterEqual(len(plan["safe_now"]), 30)
        self.assertGreaterEqual(len(plan["candidate"]), 20)
        self.assertGreaterEqual(len(plan["skill_ideas"]), 10)
        self.assertGreaterEqual(len(plan["runner_ideas"]), 10)
        self.assertGreaterEqual(len(plan["clean_fix_refine"]), 30)
        self.assertLessEqual(len(plan["safe_now"]) + len(plan["candidate"]), 1000)

    def test_source_ids_resolve(self) -> None:
        sources = {row["source_id"] for row in load("sources/source-ledger.json")["entries"]}
        for row in load("preregistration/proposals.json")["proposals"]:
            self.assertTrue(set(row["official_or_primary_source_needs"]) <= sources)

    def test_negative_accounting(self) -> None:
        negatives = load("truth/retained-negative-register.json")
        self.assertEqual((negatives["inherited_effective"], negatives["new_x1_operational"], negatives["effective_after_x1"]), (7338, 5, 7343))
        self.assertEqual(negatives["failures_erased"], 0)

    def test_method_flow(self) -> None:
        ledger = load_x1("method-flow/method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 5)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 5, "pass": 5})
        self.assertEqual(ledger["counts"]["states"]["preferred"], 5)
        self.assertTrue(load("method-flow/method-flow-validation.json")["valid"])

    def test_x1_commit_local_manifest(self) -> None:
        manifest = load("validation/x1-staged-manifest.json")
        review = load("validation/x1-staged-review.json")
        privacy = load("validation/x1-staged-privacy.json")
        self.assertEqual(manifest["entry_count"] + len(manifest["self_exclusions"]), review["intended_path_count"])
        self.assertTrue(review["x1_only"])
        self.assertEqual(review["x2_implementation_paths"], [])
        self.assertEqual(privacy["confirmed_hit_count"], 0)

    def test_future_route_stays_unlaunched(self) -> None:
        route = load("workflow/route-decision.json")
        self.assertEqual(route["future_cli_seats"]["state"], "PREPARED_NOT_LAUNCHED")
        self.assertFalse(route["future_cli_seats"]["named"])
        self.assertFalse(route["future_cli_seats"]["launched"])
        self.assertEqual(route["terminal_send_state"], "PREPARED_NOT_SENT")

    def test_environment_was_read_only(self) -> None:
        env = load("environment/environment-version-receipt.json")
        self.assertEqual(env["codex_cli"], "0.145.0")
        self.assertTrue(env["versions_verified_only"])
        for key in ("desktop_updated", "elevated", "host_security_changed", "windows_feature_changed", "sandbox_or_hyper_v_launched", "unrelated_software_installed", "rebooted"):
            self.assertFalse(env[key])


if __name__ == "__main__":
    unittest.main()
